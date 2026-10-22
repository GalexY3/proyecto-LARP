"""Exploratory pilot: 3-role sparse fixed-layout sensing for global RGB intensity.
Real skimage example images; train/test scene separation; 2D only.
COSI/MHU here are native-2D PROXIES, not original Scale3D.
No adaptive use of heldout test in layout selection. Evaluation itself exploratory.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import minimize
from scipy.stats import qmc
from skimage import data
from sklearn.linear_model import Ridge

OUT=Path(__file__).resolve().parent
SIDE=24; PIX=SIDE*SIDE; A=3; M=8
WT=np.array([.2126,.7152,.0722]); K=np.array([(i,j) for i in range(-5,6) for j in range(-5,6) if 0<i*i+j*j<=25 and (i>0 or (i==0 and j>0))],float)
B=len(K)
print('Fourier modes',B,flush=True)

def patches(img_name,n,seed,strict=False):
    im=getattr(data,img_name)().astype(np.float32)/255.
    if im.ndim!=3 or im.shape[-1]!=3:raise ValueError(img_name)
    rng=np.random.default_rng(seed)
    yy=rng.integers(0,im.shape[0]-SIDE+1,n);xx=rng.integers(0,im.shape[1]-SIDE+1,n)
    return np.stack([im[y:y+SIDE,x:x+SIDE,:].transpose(2,0,1) for x,y in zip(xx,yy)])

def get_data():
    # Four training scenes; one same-scene new crop set; two wholly heldout scenes.
    train=np.concatenate([patches(name,450,100+i) for i,name in enumerate(['astronaut','coffee','chelsea','immunohistochemistry'])])
    val=np.concatenate([patches(name,150,200+i) for i,name in enumerate(['astronaut','coffee','chelsea','immunohistochemistry'])])
    external={name:patches(name,800,300+i) for i,name in enumerate(['rocket','hubble_deep_field'])}
    return train,val,external

def covariance_train(x):
    xx=x - x.mean(axis=(-2,-1),keepdims=True)
    F=np.fft.fft2(xx,axes=(-2,-1))/PIX
    # Fourier discrete k indices. Spatial sampling e^{2pi ikx} convention.
    F=np.stack([F[:,:,int(k1)%SIDE,int(k2)%SIDE] for k1,k2 in K.astype(int)],axis=1)
    return np.einsum('nka,nkb->kab',F.conj(),F,optimize=True)/len(x)

def spectral_score(P,C,regular=0.000025,derivative=False):
    P=P.reshape(A,M,2)
    ee=np.exp(2j*np.pi*np.einsum('amd,kd->amk',P,K))
    z=ee.mean(1)*WT[:,None]
    target=np.einsum('kab,bk->ak',C,z)
    risk=np.real(np.einsum('ak,ak->',z.conj(),target))
    # Soft local packing of same-role sensors. Applied uniformly to all spectral arms.
    d=P[:,:,None,:]-P[:,None,:,:]
    d-=np.round(d)
    ds=np.einsum('aijd,aijd->aij',d,d)
    exp=np.exp(-ds/(.15**2));mask=(1-np.eye(M))[None,:,:]
    pen=regular*(exp*mask).sum()
    if not derivative:return float(risk+pen)
    # C is hermitian by definition; derivative sign checked by finite differences.
    gr=-(4*np.pi*WT[:,None,None]/M)*np.einsum('amk,kd->amd',np.imag(np.conj(target)[:,None,:]*ee),K)
    gr+=regular*(-4/.15**2)*np.einsum('aij,aijd->aid',exp*mask,d)
    return float(risk+pen),gr.reshape(-1)

def idx(P):
    return (np.clip(np.round(P[:,1]*SIDE-.5),0,SIDE-1).astype(int)*SIDE+np.clip(np.round(P[:,0]*SIDE-.5),0,SIDE-1).astype(int))

def coords(ids):
    ids=np.asarray(ids)
    return np.stack(((ids%SIDE+.5)/SIDE,(ids//SIDE+.5)/SIDE),axis=-1)

def disambiguate(ids):
    ids=ids.reshape(A,M).copy()
    for a in range(A):
        seen=set()
        for j,t in enumerate(ids[a]):
            t=int(t)
            if t in seen:
                x0=coords(np.array([t]))[0]
                pool=np.array([u for u in range(PIX) if u not in seen])
                delta=coords(pool)-x0
                t=int(pool[np.argmin((delta**2).sum(axis=1))])
                ids[a,j]=t
            seen.add(t)
    return ids

def spectral_layout(C,seed,maxiter=135):
    rng=np.random.default_rng(seed)
    init=np.concatenate([sobol_one(seed+a*37) for a in range(A)])
    p0=coords(init.ravel())+rng.normal(0,.013,(A*M,2))
    p0=np.clip(p0,.001,.999)
    res=minimize(spectral_score,p0.reshape(-1),args=(C,.000025,True),jac=True,bounds=[(.0001,.9999)]*(A*M*2),method='L-BFGS-B',options={'maxiter':maxiter,'ftol':1e-11})
    return disambiguate(idx(res.x.reshape(A*M,2))), {'nit':int(res.nit),'success':bool(res.success),'loss':float(res.fun)}

def sobol_one(seed):
    xy=qmc.Sobol(2,scramble=True,seed=seed).random_base2(3)
    return disambiguate_raw(idx(xy))

def disambiguate_raw(ids):
    ids=np.array(ids,dtype=int);available=[i for i in range(PIX) if i not in ids]
    seen=set()
    for j,t in enumerate(ids):
        if t in seen:
            ids[j]=available.pop(0)
        seen.add(ids[j])
    return ids

def fps_one(seed):
    rng=np.random.default_rng(seed); pool=coords(np.arange(PIX)); ix=int(rng.integers(0,PIX));chosen=[ix];dmin=((pool-pool[ix])**2).sum(1)
    for _ in range(M-1):
        dmin[chosen]=-1
        ix=int(np.argmax(dmin));chosen.append(ix)
        dmin=np.minimum(dmin,((pool-pool[ix])**2).sum(1))
    return np.array(chosen)

def strat_one(seed):
    rng=np.random.default_rng(seed)
    # 2 rows x 4 cols of native 24x24 pixels => 8 cells.
    return np.array([int(rng.integers(ry*12,(ry+1)*12))*SIDE+int(rng.integers(cx*6,(cx+1)*6)) for ry in range(2) for cx in range(4)])

def local_one(seed):
    # Iterative max-min approximate blue noise via FPS; separate nearest-neighbor local packing.
    return fps_one(seed)

def greedy_direct(x,seed=2,passes=3):
    # Competing learned layout: optimizes precisely empirical MSE of the fixed unbiased estimator,
    # has SAME training patches as spectral design, no test data.
    rng=np.random.default_rng(seed)
    X=x.reshape(len(x),3,PIX).astype('float32')
    target=np.einsum('a,na->n',WT,X.mean(axis=2))
    ids=np.stack([strat_one(seed+37*a) for a in range(A)])
    sm=np.sum([WT[a]*X[:,a,ids[a]].mean(1) for a in range(A)],axis=0)
    resid=sm-target
    for epoch in range(passes):
        changes=0
        for a,j in rng.permutation(np.array([(a,j) for a in range(A) for j in range(M)])):
            a=int(a);j=int(j);old=int(ids[a,j]);cands=X[:,a,:]
            delta=(WT[a]/M)*(cands-X[:,a,old,None])
            err=np.mean((resid[:,None]+delta)**2,axis=0)
            err[ids[a,np.arange(M)!=j]]=np.inf
            t=int(np.argmin(err))
            if t!=old:
                resid+=delta[:,t];ids[a,j]=t;changes+=1
        if changes==0:break
    return ids,{'train_rmse':float(np.sqrt(np.mean(resid**2))),'passes':epoch+1}

def evaluate(ids,x):
    X=x.reshape(len(x),3,PIX)
    t=np.einsum('a,na->n',WT,X.mean(axis=2))
    y=np.sum([WT[a]*X[:,a,ids[a]].mean(1) for a in range(A)],axis=0)
    return float(np.sqrt(np.mean((t-y)**2))),float(np.mean(y-t))

def ridge_evaluate(ids,train,test):
    xt=np.concatenate([train.reshape(len(train),3,PIX)[:,a,ids[a]] for a in range(A)],axis=1)
    xs=np.concatenate([test.reshape(len(test),3,PIX)[:,a,ids[a]] for a in range(A)],axis=1)
    ytrain=np.einsum('a,na->n',WT,train.mean(axis=(-2,-1)))
    ytest=np.einsum('a,na->n',WT,test.mean(axis=(-2,-1)))
    mod=Ridge(alpha=1.,fit_intercept=True).fit(xt,ytrain)
    return float(np.sqrt(np.mean((mod.predict(xs)-ytest)**2)))

def main():
    from hashlib import sha256
    start=time.time(); train,val,external=get_data();print('data',train.shape,val.shape,[(k,v.shape) for k,v in external.items()],flush=True)
    C=covariance_train(train)
    Cmhu=np.repeat(np.eye(A)[None,:,:]*np.trace(C,axis1=1,axis2=2).mean()/(A),B,axis=0)
    # Stronger task-informed spectral ablation: per-frequency per-role variances, no cross-type covariance.
    Cpower=np.stack([np.diag(np.real(np.diag(c))) for c in C])
    Cshrink=.5*C+.5*Cpower
    designs={}; timing={};metas={}
    arms=['IID','STRAT','FPS','SOBOL','MHU-plain','POWER-DIAG','COSI-FULL','COSI-SHRINK','DIRECT-EMPIRICAL']
    for arm in arms:
        s=time.time()
        for sd in range(7):
            seed=5400+sd
            if arm=='IID':ids=np.stack([np.random.default_rng(seed+a*143).choice(PIX,M,replace=False) for a in range(A)]);meta={}
            elif arm=='STRAT':ids=np.stack([strat_one(seed+13*a) for a in range(A)]);meta={}
            elif arm=='FPS':ids=np.stack([fps_one(seed+13*a) for a in range(A)]);meta={}
            elif arm=='SOBOL':ids=np.stack([sobol_one(seed+13*a) for a in range(A)]);meta={}
            elif arm=='MHU-plain':ids,meta=spectral_layout(Cmhu,seed)
            elif arm=='POWER-DIAG':ids,meta=spectral_layout(Cpower,seed)
            elif arm=='COSI-FULL':ids,meta=spectral_layout(C,seed)
            elif arm=='COSI-SHRINK':ids,meta=spectral_layout(Cshrink,seed)
            elif arm=='DIRECT-EMPIRICAL':ids,meta=greedy_direct(train,seed,passes=3)
            assert all(len(set(ids[a]))==M for a in range(A))
            key=f'{arm}:{sd}';designs[key]=ids.tolist();metas[key]=meta
        timing[arm]=(time.time()-s)/7
        print('completed',arm,round(timing[arm],2),'seconds/layout',flush=True)
    results=[]
    for key,ids in designs.items():
        arm,seed=key.rsplit(':',1); ids=np.asarray(ids)
        z={'method':arm,'seed':int(seed),'ids':ids.tolist(),'train_fixed_RMSE':evaluate(ids,train)[0], 'same_scene_new_crops_RMSE':evaluate(ids,val)[0],
             'rocket_RMSE':evaluate(ids,external['rocket'])[0], 'hubble_RMSE':evaluate(ids,external['hubble_deep_field'])[0],
             'ridge_rocket_RMSE':ridge_evaluate(ids,train,external['rocket']), 'ridge_hubble_RMSE':ridge_evaluate(ids,train,external['hubble_deep_field'])}
        # Loss of 2 out of 8 sensors in each role, with deterministic shared mask trials across arms.
        dropout=[]
        X=external['rocket'].reshape(len(external['rocket']),3,PIX)
        t=np.einsum('a,na->n',WT,X.mean(axis=2));r=np.random.default_rng(20261022)
        for j in range(15):
            keep=np.array([np.sort(r.choice(M,6,replace=False)) for a in range(A)])
            y=np.sum([WT[a]*X[:,a,ids[a,keep[a]]].mean(1) for a in range(A)],axis=0)
            dropout.append(float(np.sqrt(np.mean((t-y)**2))))
        z['rocket_dropout2_RMSE']=float(np.mean(dropout))
        results.append(z)
    summary={arm:{'runtime_s_per_layout':timing[arm],**{k:float(np.mean([z[k] for z in results if z['method']==arm])) for k in ['train_fixed_RMSE','same_scene_new_crops_RMSE','rocket_RMSE','hubble_RMSE','rocket_dropout2_RMSE','ridge_rocket_RMSE','ridge_hubble_RMSE']}} for arm in arms}
    out={'scope':'native 2D real images; exploratory, 7 layout seeds, no independent 3D data','train_scene_names':['astronaut','coffee','chelsea','immunohistochemistry'],'ood_scenes':['rocket','hubble_deep_field'],'input_data':'scikit-image example imagery; native RGB; patch size 24, 8 sensors per R,G,B','train_patches':len(train),'val_patches':len(val),'heldout_patches_each':800,'modes':B,'estimand':'RMSE of equal-weight within-role sparse sample mean to full-image weighted RGB mean; luma proxy WT=(.2126,.7152,.0722)','limitations':['Images are not physical multisensor fields; do not infer performance on air quality or 3D microscopy','The heldout scenes are only two scene-level units; patches overlap and are not independent external replicates','COSI uses train covariance; compare with POWER-DIAG and DIRECT-EMPIRICAL, not only MHU','Selection/adaptation to these results is exploratory and cannot be promoted to blinded confirmation','Mismatched generation/runtime across techniques are explicitly reported'],'summary':summary,'results':results,'metadata':metas,'elapsed_seconds':time.time()-start}
    (OUT/'real_rgb_results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
    print(json.dumps({'elapsed':out['elapsed_seconds'],'summary':summary},indent=2),flush=True)
if __name__=='__main__':main()
