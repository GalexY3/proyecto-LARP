"""LARP vision sampling AB pilot, prereg-code 2026-10-29.
No pretrained vision network, no asymptotic HU certificate, no authentic Wei 2010.
Usage: python vision_ab_c01.py [--out DIR]
"""
import argparse, hashlib, json, platform, time
from pathlib import Path
import numpy as np
import scipy
from scipy.spatial import cKDTree, Delaunay
from scipy.stats import qmc
from skimage import data, color, transform
import torch

SEEDS=[1103,1109,1117,1123,1129,1151]
N=160; TYPES=5; SIDE=128
IMAGES=['astronaut','coffee','chelsea','rocket','camera','coins','page','hubble_deep_field','immunohistochemistry','cell','brick','gravel','grass']
DEV=IMAGES[:4]; TEST=IMAGES[4:]
METHODS=['grid','sobol','poisson_disk','cvt_subtypes','mhu_joint','mhu_subtypes']
LOW_K=np.array([(i,j) for i in range(-3,4) for j in range(-3,4) if 0<i*i+j*j<=10 and (i>0 or (i==0 and j>0))],dtype=float)

def to_gray(name):
    arr=np.asarray(getattr(data,name)())
    if arr.ndim==3: arr=color.rgb2gray(arr[...,:3])
    else: arr=arr.astype(float)/float(np.iinfo(arr.dtype).max) if np.issubdtype(arr.dtype,np.integer) else arr.astype(float)
    h,w=arr.shape; s=min(h,w);y=(h-s)//2;x=(w-s)//2
    arr=transform.resize(arr[y:y+s,x:x+s],(SIDE,SIDE),anti_aliasing=True,preserve_range=True)
    return np.clip(arr.astype(np.float64),0,1)

def randomized_grid(seed):
    # 16x10 exact grid. Seed changes only the mapping of subtype labels.
    yy,xx=np.mgrid[:10,:16]
    return np.stack(((xx.ravel()+.5)/16,(yy.ravel()+.5)/10),axis=1)

def sobol(seed):
    return qmc.Sobol(d=2,scramble=True,seed=seed).random_base2(8)[:N]

def poisson(seed):
    # Strong fixed-count blue-noise proxy from SciPy, not original Wei multi-class.
    for radius in [0.030,0.027,0.024,0.020]:
        p=qmc.PoissonDisk(d=2,radius=radius,seed=seed).random(N)
        if len(p)==N: return p
    raise RuntimeError('Poisson generation failed')

def cvt_types(seed,labels):
    # Independent type-wise CVT with equal numerical effort per type.
    p=sobol(seed+2100).copy();rng=np.random.default_rng(seed+2210)
    probes=rng.random((15000,2))
    for _ in range(15):
        for t in range(TYPES):
            idx=np.flatnonzero(labels==t);cent=p[idx]
            nearest=cKDTree(cent).query(probes)[1]
            counts=np.bincount(nearest,minlength=len(idx))
            sx=np.bincount(nearest,weights=probes[:,0],minlength=len(idx))
            sy=np.bincount(nearest,weights=probes[:,1],minlength=len(idx))
            good=counts>0
            cent[good,0]=sx[good]/counts[good]
            cent[good,1]=sy[good]/counts[good]
            p[idx]=cent
    return p

def optimize_spectral(seed,labels,joint):
    # Finite-band spectral loss. A finite-band proxy is never an MHU certificate.
    base=sobol(seed+3100)
    torch.manual_seed(seed)
    p=torch.tensor(base, dtype=torch.float64,requires_grad=True)
    lab=torch.tensor(labels)
    k=torch.tensor(LOW_K,dtype=torch.float64)
    optimizer=torch.optim.Adam([p],lr=0.014)
    for _ in range(95):
        optimizer.zero_grad()
        a=p@k.T * (2*np.pi)
        z=torch.exp(1j*a)
        class_losses=[torch.mean(torch.abs(z[lab==i].mean(0))**2) for i in range(TYPES)]
        class_loss=torch.stack(class_losses).mean()
        union_loss=torch.mean(torch.abs(z.mean(0))**2)
        # finite local repulsion, constant for joint / sub
        delta=p[:,None,:]-p[None,:,:]
        delta=delta-torch.round(delta.detach())  # torus distance for geometry only
        dsq=(delta**2).sum(-1)
        rep=(torch.exp(-dsq/0.00090).sum()-N)/float(N*N)
        loss=class_loss + (union_loss if joint else 0.0) + 0.15*rep
        loss.backward();optimizer.step()
        with torch.no_grad():p.remainder_(1.)
    return p.detach().numpy()

def geom_diagnostics(p,labels):
    a=2*np.pi*p@LOW_K.T
    z=np.exp(1j*a)
    klow=float(np.abs(z.mean(0)).__pow__(2).mean())
    sub=float(np.mean([np.mean(np.abs(z[labels==i].mean(0))**2) for i in range(TYPES)]))
    qry=np.random.default_rng(9).random((2500,2))
    dist=cKDTree(p).query(qry)[0]
    return {'low_k_union':klow,'low_k_subtypes':sub,'mean_distance_to_sample':float(dist.mean()),'p95_distance_to_sample':float(np.percentile(dist,95))}

def sampler(p):
    # Fixed interpolator: nearest fallback outside convex hull; same for every layout.
    query=np.stack(np.meshgrid((np.arange(SIDE)+.5)/SIDE,(np.arange(SIDE)+.5)/SIDE),-1).reshape(-1,2)
    tri=Delaunay(p)
    simplex=tri.find_simplex(query)
    inside=simplex>=0
    inds=np.zeros((len(query),3),dtype=int);w=np.zeros((len(query),3))
    if inside.any():
        s=simplex[inside]; x=query[inside]-tri.transform[s,2]
        bary=np.einsum('ijk,ik->ij',tri.transform[s,:2],x)
        inds[inside]=tri.simplices[s]
        w[inside]=np.stack((bary[:,0],bary[:,1],1-bary.sum(1)),axis=1)
    outside=~inside
    if outside.any():
        nearest=cKDTree(p).query(query[outside])[1]
        inds[outside,0]=nearest;w[outside,0]=1
    return inds,w

def sampling_values(img,p):
    # Bilinear coordinate sampling, equal for all methods; no access to full image at reconstruction.
    from scipy.ndimage import map_coordinates
    xy=(p*SIDE-.5).T
    return map_coordinates(img,[xy[1],xy[0]],order=1,mode='nearest')

def reconstruct(vals,op):
    inds,weights=op
    return np.sum(vals[inds]*weights,axis=1).reshape(SIDE,SIDE)

def dropout_reconstruct(vals,p,dropseed):
    # 30% points lost, same index mask for each arm; regenerate triangulation on remaining.
    rng=np.random.default_rng(dropseed)
    keep=np.ones(N,dtype=bool);keep[rng.choice(N,size=int(.30*N),replace=False)]=False
    return reconstruct(vals[keep],sampler(p[keep]))

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    imgs={n:to_gray(n) for n in IMAGES}
    # No fitting of preprocessing on test images. Pixel values are [0,1].
    output=[]; geometries=[]
    for seed in SEEDS:
        rng=np.random.default_rng(seed)
        labels=np.tile(np.arange(TYPES),N//TYPES)
        rng.shuffle(labels)
        methods={'grid':randomized_grid(seed),'sobol':sobol(seed),'poisson_disk':poisson(seed),
                 'cvt_subtypes':cvt_types(seed,labels),'mhu_joint':optimize_spectral(seed,labels,True),
                 'mhu_subtypes':optimize_spectral(seed,labels,False)}
        for method,p in methods.items():
            if p.shape!=(N,2):raise ValueError('Invalid size')
            diag=geom_diagnostics(p,labels)
            geometries.append({'seed':seed,'method':method,**diag})
            op=sampler(p)
            for name,img in imgs.items():
                vals=sampling_values(img,p)
                tests=[('clean',reconstruct(vals,op)),('drop30',dropout_reconstruct(vals,p,seed+700)),
                       ('noise08',reconstruct(np.clip(vals+np.random.default_rng(seed+9100+IMAGES.index(name)).normal(0,.08,size=N),0,1),op))]
                for condition,pred in tests:
                    diff=pred-img
                    output.append({'seed':seed,'method':method,'image':name,'split':'DEV' if name in DEV else 'TEST',
                                   'condition':condition,'mse':float(np.mean(diff**2)),'mae':float(np.mean(np.abs(diff)))})
        print('finished seed',seed,flush=True)
    results={'protocol':'C01','methods':METHODS,'images':IMAGES,'dev':DEV,'test':TEST,'seeds':SEEDS,
             'N':N,'finite_k':LOW_K.astype(int).tolist(),'results':output,'geometry':geometries,
             'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'torch':torch.__version__,'python':platform.python_version()},
             'image_sha256':{n:hashlib.sha256(imgs[n].tobytes()).hexdigest() for n in IMAGES}}
    (out/'results.json').write_text(json.dumps(results,indent=2))
    print('WROTE',out/'results.json',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default=str(Path(__file__).resolve().parent));args=p.parse_args()
    torch.set_num_threads(2);main(args.out)
