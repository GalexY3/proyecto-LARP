"""C02 prospective RGB filter-mosaic pilot for LARP. Prereg before outcomes required.
Five virtual linear RGB filters, NOT independently captured spectral bands.
All methods observe 160 equal-cost scalar readings with same regularized decoder.
"""
from __future__ import annotations
import hashlib, json, platform, sys, time
from pathlib import Path
import numpy as np
from scipy import ndimage, linalg
from scipy.stats import qmc
from skimage import data, transform

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from vision_ab_c01 import optimize_spectral
SEEDS=[2029,2039,2053,2063]
SIDE=48; N=160; T=5
DEV=['astronaut','coffee','chelsea','rocket']
TEST=['retina','stereo_motorcycle','hubble_deep_field','immunohistochemistry']
SYNTHETIC_STRESS=['colorwheel']
METHODS=['grid_balanced','poisson_multiclass_proxy','sobol_balanced','spectral_joint','spectral_sub','joint_phase_broken']
FILTERS=np.array([[1,0,0],[0,1,0],[0,0,1],[.5,.5,0],[0,.5,.5]],dtype=float)
SIGMA=.17; LAMBDA=.012
YY,XX=np.mgrid[0:SIDE,0:SIDE]
GRID_COORDS=np.stack(((XX.ravel()+.5)/SIDE,(YY.ravel()+.5)/SIDE),axis=1)
BY,BX=np.mgrid[0:8,0:8]
CENTERS=np.stack(((BX.ravel()+.5)/8,(BY.ravel()+.5)/8),axis=1)
def features(p):
    d=(np.asarray(p)[:,None,:]-CENTERS[None,:,:])**2
    b=np.exp(-d.sum(axis=2)/(2*SIGMA**2))
    b/=np.maximum(1.e-16,b.sum(axis=1,keepdims=True))
    return b
def array(name):
    if name=='stereo_motorcycle': raw=np.asarray(data.stereo_motorcycle()[0])
    else: raw=np.asarray(getattr(data,name)())
    assert raw.ndim==3 and raw.shape[2]>=3,(name,raw.shape)
    raw=raw[:,:,:3].astype(float)/255.0
    h,w=raw.shape[:2];s=min(h,w)
    raw=raw[(h-s)//2:(h+s)//2,(w-s)//2:(w+s)//2]
    return np.clip(transform.resize(raw,(SIDE,SIDE),preserve_range=True,anti_aliasing=True).astype(float),0,1)
def labels_balanced(p,seed):
    # Greedy maximin among existing same-type locations with exact quota 32.
    rng=np.random.default_rng(seed)
    order=rng.permutation(N); lab=np.full(N,-1,int); counts=np.zeros(T,int)
    for i in order:
        opts=np.flatnonzero(counts<N//T)
        score=[]
        for t in opts:
            pts=p[lab==t]
            nearest=np.min(np.sum((pts-p[i])**2,axis=1)) if len(pts) else 2.
            score.append(nearest + rng.uniform(0,1e-8))
        t=opts[np.argmax(score)];lab[i]=t;counts[t]+=1
    assert np.array_equal(np.bincount(lab),np.repeat(32,5))
    return lab
def geometries(seed):
    # Exact 16x10 grid. Label assignment is deterministic balanced modular tiling.
    y,x=np.mgrid[:10,:16]; pgrid=np.stack(((x.ravel()+.5)/16,(y.ravel()+.5)/10),axis=1)
    lg=((x+2*y)%T).ravel()
    assert np.array_equal(np.bincount(lg),np.repeat(32,T))
    sob=qmc.Sobol(d=2,scramble=True,seed=seed).random_base2(8)[:N]
    ls=labels_balanced(sob,seed+100)
    # Validated hard-disk coverage, not native Wei or a true MHU certificate.
    pd=qmc.PoissonDisk(d=2,radius=.063,ncandidates=45,seed=seed+300)
    allpts=pd.fill_space()
    if len(allpts)<N:
        raise RuntimeError(f'Poisson fill_space produced {len(allpts)} < {N}')
    # Farthest-spread subset, avoid truncation-to-cluster bug in C01.
    rng=np.random.default_rng(seed+101)
    initial=int(rng.integers(len(allpts))); chosen=[initial]
    distances=np.sum((allpts-allpts[initial])**2,axis=1)
    for _ in range(N-1):
        distances[chosen[-1]]=-1
        j=int(np.argmax(distances));chosen.append(j)
        distances=np.minimum(distances,np.sum((allpts-allpts[j])**2,axis=1))
    pp=allpts[chosen]
    lp=labels_balanced(pp,seed+200)
    # Matched initial labels and optimization budget between joint/subtype methods.
    lr=np.random.default_rng(seed); lm=np.tile(np.arange(T),N//T);lr.shuffle(lm)
    mj=optimize_spectral(seed,lm,True)
    ms=optimize_spectral(seed,lm,False)
    # Disrupt only cross-type phase, conserve each subtype Fourier magnitudes.
    mb=mj.copy();phase=np.random.default_rng(seed+900).uniform(0,1,(T,2))
    for t in range(T): mb[lm==t]=(mb[lm==t]+phase[t])%1.
    return {'grid_balanced':(pgrid,lg),'poisson_multiclass_proxy':(pp,lp),
        'sobol_balanced':(sob,ls),'spectral_joint':(mj,lm),
        'spectral_sub':(ms,lm),'joint_phase_broken':(mb,lm)}
def obs_operator(p,lab,kept=None):
    if kept is not None: p=p[kept];lab=lab[kept]
    b=features(p); operator=np.einsum('ns,nc->nsc',b,FILTERS[lab]).reshape(len(p),-1)
    # Regularized least squares, identical lambda, feature functions, and budget.
    aa=operator.T@operator + LAMBDA*np.eye(len(CENTERS)*3)
    factor=linalg.cho_factor(aa,lower=True,check_finite=False)
    return operator,b,factor
RECON_B=features(GRID_COORDS)
def reconstruct(ops, measurements):
    a,b,fac=ops
    coef=linalg.cho_solve(fac,a.T@measurements,check_finite=False).reshape(64,3)
    return np.clip((RECON_B@coef).reshape(SIDE,SIDE,3),0,1)
def measure(im,p,lab):
    # One scalar at each point, from one of five virtual RGB filters.
    loc=(p*SIDE-.5).T
    ch=np.stack([ndimage.map_coordinates(im[:,:,c], [loc[1],loc[0]], order=1,mode='nearest') for c in range(3)],axis=-1)
    return np.einsum('nc,nc->n',ch,FILTERS[lab])
def spectrum(p,lab):
    ks=np.array([(i,j) for i in range(-3,4) for j in range(-3,4) if 0<i*i+j*j<=10 and (i>0 or (i==0 and j>0))],float)
    z=np.exp(2j*np.pi*(p@ks.T))
    return dict(low_k_union=float(np.mean(np.abs(z.mean(0))**2)),
                low_k_sub=float(np.mean([np.mean(np.abs(z[lab==t].mean(0))**2) for t in range(5)])))
def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    images={k:array(k) for k in DEV+TEST+SYNTHETIC_STRESS}
    imhash={k:hashlib.sha256(v.tobytes()).hexdigest() for k,v in images.items()}
    measurements=[];geometry=[]
    for seed in SEEDS:
        gs=geometries(seed)
        rng=np.random.default_rng(seed+750)
        missing=np.ones(N,dtype=bool);missing[rng.choice(N,int(.2*N),replace=False)]=False
        for method,(p,l) in gs.items():
            assert p.shape==(N,2) and l.shape==(N,) and np.bincount(l,minlength=5).tolist()==[32]*5
            assert np.isfinite(p).all() and np.all((p>=0)&(p<=1))
            geom=spectrum(p,l)
            from scipy.spatial import cKDTree
            qry=np.random.default_rng(231).random((2400,2)); geom['mean_distance']=float(cKDTree(p).query(qry)[0].mean())
            geometry.append({'seed':seed,'method':method,**geom})
            op=obs_operator(p,l)
            opdrop=obs_operator(p,l,missing)
            for nm,im in images.items():
                y=measure(im,p,l)
                for condition,rec in [('clean',reconstruct(op,y)),
                                      ('drop20',reconstruct(opdrop,y[missing])),
                                      ('noise03',reconstruct(op,np.clip(y+np.random.default_rng(seed+int.from_bytes(hashlib.sha256(nm.encode()).digest()[:4], 'little')).normal(0,.03,N),0,1)))]:
                    measurements.append({'seed':seed,'method':method,'image':nm,
                        'split':'TEST' if nm in TEST else ('DEV' if nm in DEV else 'STRESS'),
                        'condition':condition,'mse':float(np.mean((rec-im)**2)),
                        'mae':float(np.mean(np.abs(rec-im)))})
        print('finished',seed,flush=True)
    data_out={'name':'LARP-VISION C02','seeds':SEEDS,'side':SIDE,'readings':N,'filters':FILTERS.tolist(),
       'dev':DEV,'test':TEST,'synthetic_stress':SYNTHETIC_STRESS,'methods':METHODS,
       'sigma':SIGMA,'ridge':LAMBDA,'image_hash':imhash,'geometry':geometry,'observations':measurements,
       'versions':{'numpy':np.__version__,'python':platform.python_version()}}
    (out/'results_c02.json').write_text(json.dumps(data_out,indent=2))
    print('results saved',out/'results_c02.json')
if __name__=='__main__': run(ROOT)
