#!/usr/bin/env python3
"""LARP-BR12 exploratory sequential research. Derived generators (not original 3D Scale3D).
Citations: Wei 2010, https://www.liyiwei.org/papers/noise-sig10/ ; prior
BR30 https://github.com/GalexY3/proyecto-LARP . No original Wei code used.
"""
from __future__ import annotations
import argparse,json,time,hashlib
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from scipy import stats
ROOT=Path(__file__).resolve().parents[1]
N=512; CT=np.array([209,109,87,64,43]); assert sum(CT)==N
TYPES=np.repeat(np.arange(5),CT); NAMES=('iid','stratified','cvt_type','local_derived')
M=np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,-1,0],[0,1,-1],[1,0,-1],[2,0,0],[0,2,0],[0,0,2]],float)

def stratified(seed):
    rg=np.random.default_rng(seed); p=np.zeros((N,3))
    for t in range(5):
        ix=np.where(TYPES==t)[0]; n=len(ix);g=int(np.ceil(n**(1/3)))
        cells=np.indices((g,g,g)).reshape(3,-1).T
        sel=rg.choice(len(cells),size=n,replace=False)
        p[ix]=((cells[sel]+rg.uniform(.08,.92,(n,3)))/g+rg.uniform(0,1,(1,3)))%1
    return p

def local_derived(start,iterations=100,step=.025):
    # NEW derived local repulsion; NOT exact original Scale3D optimizer.
    # periodic within-type and union nearest-neighbor soft repulsion, fixed quotient.
    p=start.copy();t=TYPES
    d_h=(1/CT[t])**(1/3)*.73;d_u=(1/N)**(1/3)*.45
    for it in range(iterations):
        vec=np.zeros_like(p)
        # homotypic repulsion using 5 same-type neighbors
        for typ in range(5):
            ix=np.flatnonzero(t==typ); pts=p[ix]
            dist,ids=cKDTree(pts,boxsize=1).query(pts,k=5)
            dif=pts[:,None,:]-pts[ids[:,1:]]
            dif=(dif+.5)%1-.5
            r=np.maximum(dist[:,1:],1e-8); cutoff=d_h[ix][:,None]
            amp=np.maximum(cutoff-r,0)/cutoff
            vec[ix]+=(amp[:,:,None]*dif/r[:,:,None]).sum(1)/4
        dist,ids=cKDTree(p,boxsize=1).query(p,k=9)
        dif=p[:,None,:]-p[ids[:,1:]];dif=(dif+.5)%1-.5
        r=np.maximum(dist[:,1:],1e-8);amp=np.maximum(d_u-r,0)/d_u
        vec+=.5*(amp[:,:,None]*dif/r[:,:,None]).sum(1)/8
        move=(step*(1-it/(iterations+40)))*vec
        p=(p+move)%1
    return p

def cvt_type(start,iterations=15,m=18000,seed=21):
    # independently CVT-Lloyd each species (strong established geometric baseline).
    rg=np.random.default_rng(seed);out=start.copy()
    for _ in range(iterations):
        qry=rg.random((m,3))
        for typ in range(5):
            ix=np.flatnonzero(TYPES==typ);pts=out[ix]
            _,idx=cKDTree(pts,boxsize=1).query(qry,k=1)
            dif=(qry-pts[idx]+.5)%1-.5
            cnt=np.bincount(idx,minlength=len(ix)); accum=np.zeros_like(pts)
            np.add.at(accum,idx,dif)
            delta=accum/np.maximum(cnt[:,None],1)
            out[ix]=(pts+.68*delta)%1
    return out

def generate(seed):
    rg=np.random.default_rng(seed);init=rg.random((N,3));return {
        'iid':init,
        'stratified':stratified(seed+200),
        'cvt_type':cvt_type(stratified(seed+300),seed=seed+400),
        'local_derived':local_derived(init),
    }

def all_query_metrics(geos,seed,k=16,m=2500):
    q=np.random.default_rng(seed).random((m,3));out={}
    for g,p in geos.items():
        dd,idx=cKDTree(p,boxsize=1).query(q,k=k)
        tt=TYPES[idx]
        cover=np.stack([(tt==j).any(1) for j in range(5)],axis=1).all(1).mean()
        rad=np.stack([cKDTree(p[TYPES==j],boxsize=1).query(q,k=1)[0] for j in range(5)],axis=1).max(1)
        # radius of kth nn too, cost proxy k
        out[g]={'cover':float(cover),'rad5_mean':float(rad.mean()),'rad5_p95':float(np.quantile(rad,.95)),
                'kth_radius':float(dd[:,-1].mean()),'rare_type':float((tt==4).any(1).mean())}
    return out

def latent(seed, q, freq):
    rg=np.random.default_rng(seed);A=rg.standard_normal((5,len(M),2))/np.sqrt(len(M))
    MM=np.rint(M*freq).astype(int);phase=q@(2*np.pi*MM.T)
    f=np.cos(phase)@A[:,:,0].T+np.sin(phase)@A[:,:,1].T
    return A,MM,f

def value(pos,A,MM):
    phase=pos@(2*np.pi*MM.T)
    return np.cos(phase)@A[:,:,0].T+np.sin(phase)@A[:,:,1].T

def composed(f):return f[:,0]*f[:,1]+f[:,2]*f[:,3]+.4*f[:,0]*f[:,2]*f[:,4]

def predict(p,q,A,MM,k=16,band=.08,labels=TYPES,mode='global',return_f=False):
    # equal physical sensor budget; global nearest K vs 1 per type different access.
    actual=value(p,A,MM)[np.arange(N),labels]
    if mode=='global':
        dd,idx=cKDTree(p,boxsize=1).query(q,k=k)
        tt=labels[idx];measured=actual[idx]
    elif mode=='type_budget':
        ix=[];dist=[]
        for typ in range(5):
            jj=np.flatnonzero(labels==typ)
            if len(jj)==0:continue
            d,ixs=cKDTree(p[jj],boxsize=1).query(q,k= max(1,k//5))
            ix.append(jj[np.atleast_2d(ixs) if np.ndim(ixs)==2 else ixs[:,None]])
            dist.append(np.atleast_2d(d) if np.ndim(d)==2 else d[:,None])
        idx=np.concatenate(ix,axis=1); dd=np.concatenate(dist,axis=1)
        tt=labels[idx];measured=actual[idx]
    else:raise ValueError(mode)
    weights=np.exp(-.5*(dd/band)**2)
    out=np.zeros((len(q),5))
    for t in range(5):
        w=weights*(tt==t);out[:,t]=np.sum(w*measured,axis=1)/np.maximum(w.sum(axis=1),1e-12)
    return out if return_f else composed(out)

def compare_fields(geos,seed,freq,k=16,band=.08,m=320,mode='global'):
    q=np.random.default_rng(seed*3+1).random((m,3));A,MM,f=latent(seed*3+5,q,freq)
    target=composed(f)
    out={}
    for n,p in geos.items():
        pred=predict(p,q,A,MM,k=k,band=band,mode=mode)
        out[n]=float(np.mean((pred-target)**2))
    return out

def geo_file(seed):return ROOT/'data'/'geometries'/f'{seed}.npz'
def write_geom(seed):
    p=geo_file(seed);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():return
    t0=time.perf_counter(); g=generate(seed)
    np.savez_compressed(p,labels=TYPES,**g)
    print('geometry',seed,'seconds',round(time.perf_counter()-t0,2),flush=True)

def get_geom(seed):
    p=geo_file(seed)
    if not p.exists():write_geom(seed)
    with np.load(p) as z:return {n:z[n] for n in NAMES}

def run(job,first=1201,last=1212):
    seeds=list(range(first,last+1)); raw=[]
    if job=='construct':
        for seed in seeds:write_geom(seed)
        return {'seeds':seeds,'generator':'local_derived (not exact Scale3D); per-type CVT (not Wei)', 'n_geometries_per_method':len(seeds)}
    for seed in seeds:
        g=get_geom(seed)
        if job=='coverage':
            r=all_query_metrics(g,seed+45000)
            raw.extend([dict(seed=seed,method=n,**d) for n,d in r.items()])
        elif job.startswith('field'):
            f={'field_smooth':1,'field_medium':2,'field_rough':5}[job]
            d=compare_fields(g,seed+50000,freq=f)
            raw.extend([dict(seed=seed,method=n,mse=v,freq=f) for n,v in d.items()])
        elif job=='type_budget':
            for mode in ('global','type_budget'):
                d=compare_fields(g,seed+50000,freq=1,mode=mode)
                raw.extend([dict(seed=seed,method=n,mse=v,access=mode) for n,v in d.items()])
        else:raise ValueError(job)
    out=ROOT/'data'/f'{job}_{first}_{last}.json';out.write_text(json.dumps(raw,indent=1))
    return summarize(raw)

def summarize(raw):
    from collections import defaultdict
    groups=defaultdict(list)
    for r in raw:
        for k,v in r.items():
            if k in ('seed','method','freq','access'):continue
            groups[(r['method'],r.get('access','global'),k)].append(v)
    ans={str(key):{'mean':float(np.mean(v)),'sd':float(np.std(v,ddof=1)),'n':len(v)} for key,v in groups.items()}
    return ans

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('job');a.add_argument('--first',type=int,default=1201);a.add_argument('--last',type=int,default=1212); z=a.parse_args()
    print(json.dumps(run(z.job,z.first,z.last),indent=2),flush=True)
