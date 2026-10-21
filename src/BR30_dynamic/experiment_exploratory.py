#!/usr/bin/env python3
"""Original Scale3D v2, paired LOCAL/MHU, and independently optimized CVT-per-type.
Exploratory AB research. CVT is Lloyd, NOT Wei 2010 multicolor blue-noise.
All datasets and predictions synthetic, no real physical sensors.
Commands: generate SEED [--iterations 600] ; geometry SEED ; fields SEED
"""
from __future__ import annotations
import argparse, json, math, os, time
from pathlib import Path
import numpy as np
import torch
from scipy.spatial import cKDTree
from scale3d import scale3d_geometry_v2 as original
from scale3d import scale3d_geometry as v1

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'data';OUT.mkdir(exist_ok=True)
N=4096
TYPES=5
M=np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,-1,0],[0,1,-1],[1,0,-1],[2,0,0],[0,2,0],[0,0,2]],dtype=np.float64)

def paths(seed):return OUT/f'geom_{seed}.npz',OUT/f'geom_{seed}.json'

def cvt(initial,labels,seed,steps=24,qsize=16000):
    rng=np.random.default_rng(seed+200099)
    pts=initial.copy(); cells=[np.flatnonzero(labels==t) for t in range(5)]
    t0=time.perf_counter()
    for s in range(steps):
        q=rng.random((qsize,3))
        for indices in cells:
            p=pts[indices]
            _,nearest=cKDTree(p,boxsize=1).query(q,k=1)
            dif=(q-p[nearest]+0.5)%1-0.5
            sums=np.zeros_like(p);np.add.at(sums,nearest,dif)
            cnt=np.bincount(nearest,minlength=len(p))
            pts[indices]=(p+.72*sums/np.maximum(cnt[:,None],1))%1
    return pts,time.perf_counter()-t0

def generate(seed,iterations=600):
    x0=np.random.default_rng(seed)
    init=x0.random((N,3)); labels=x0.permutation(np.repeat(np.arange(5),v1.hamilton_counts(N)))
    arrays={'random':init,'labels':labels}; meta={'seed':seed,'N':N,'iterations':iterations,'scale3d_version':original.VERSION,'cvt_is_wei':False}
    for name,spectral in [('local',False),('mhu',True)]:
        z=original.generate(seed,N,device='cpu',iterations=iterations,spectral=spectral,validate=False)
        pts=z['coordinates'].detach().cpu().numpy()
        assert np.array_equal(labels,z['labels'].detach().cpu().numpy())
        arrays[name]=pts
        meta[name]={'construction':z['construction'],'last_history':z['history'][-1]}
        print('GENERATED',seed,name,z['construction']['elapsed_seconds_including_exact_validation'],flush=True)
    pts,sec=cvt(init,labels,seed)
    arrays['cvt']=pts;meta['cvt']={'seconds':sec,'iterations':24,'qsize_per_step':16000,'algorithm':'Lloyd per species'}
    np.savez_compressed(paths(seed)[0],**arrays)
    paths(seed)[1].write_text(json.dumps(meta,indent=2))
    print('GENERATED',seed,'cvt',sec,flush=True)

def geometry(seed,klist=(8,12,16,24),queries=4000):
    with np.load(paths(seed)[0]) as z: a={k:z[k] for k in z.files}
    lab=a['labels'];q=np.random.default_rng(seed+1181100).random((queries,3))
    modes=np.array([k for k in __import__('itertools').product(range(-3,4),repeat=3) if 0<np.linalg.norm(k)<=2.5],dtype=np.float64)
    out=[]
    for name in ['random','local','mhu','cvt']:
        pts=a[name]
        dd,idx=cKDTree(pts,boxsize=1).query(q,k=max(klist))
        t=lab[idx];r={'seed':seed,'name':name,'N':N,'S_modes':len(modes)}
        for k in klist:
            r[f'coverage{k}']=float(np.stack([(t[:,:k]==s).any(axis=1) for s in range(5)],axis=1).all(axis=1).mean())
        r['radius_for_five_types_mean']=float(np.stack([cKDTree(pts[lab==tt],boxsize=1).query(q,k=1)[0] for tt in range(5)]).max(axis=0).mean())
        for component in [-1,0,1,2,3,4]:
            sub=pts if component==-1 else pts[lab==component]
            sums=np.exp(2j*np.pi*(sub@modes.T)).sum(0)
            r[f'S_{component}']=float(np.mean(np.abs(sums)**2/len(sub)))
        out.append(r)
    (OUT/f'geom_metrics_{seed}.json').write_text(json.dumps(out,indent=2));return out

def target_vals(x,a,m):
    ph=2*np.pi*x@m.T
    return np.cos(ph)@a[:,:,0].T+np.sin(ph)@a[:,:,1].T

def inference(p,lab,q,a,m,k=24,band=.05,drop_mode='none',drop_seed=0):
    rng=np.random.default_rng(drop_seed)
    if drop_mode=='iid40':
        retain=rng.random(len(p))>=.40
    elif drop_mode=='hole18' or drop_mode=='hole28':
        center=np.random.default_rng(drop_seed).random(3)
        d=(p-center+.5)%1-.5
        retain=np.linalg.norm(d,axis=1)>({'hole18':.18,'hole28':.28}[drop_mode])
    else:retain=np.ones(len(p),dtype=bool)
    pp=p[retain];ll=lab[retain]
    d,ids=cKDTree(pp,boxsize=1).query(q,k=k)
    tl=ll[ids]
    vals=target_vals(pp[ids].reshape(-1,3),a,m).reshape(len(q),k,5)
    obs=np.take_along_axis(vals,tl[:,:,None],axis=2)[:,:,0]
    w=np.exp(-.5*(d/band)**2)
    reconstruct=np.zeros((len(q),5))
    for j in range(5):
        wt=w*(tl==j); reconstruct[:,j]=(obs*wt).sum(1)/np.maximum(wt.sum(1),1e-12)
    ans=reconstruct[:,0]*reconstruct[:,1]+reconstruct[:,2]*reconstruct[:,3]+.4*reconstruct[:,0]*reconstruct[:,2]*reconstruct[:,4]
    return ans,int(np.sum(~retain))

def fields(seed,worlds=8,queries=350):
    with np.load(paths(seed)[0]) as z:a={k:z[k] for k in z.files}
    lab=a['labels'];result=[]
    for s in range(worlds):
        worldseed=700000+100*seed+s; rng=np.random.default_rng(worldseed)
        q=rng.random((queries,3))
        coef=rng.standard_normal((5,len(M),2))/np.sqrt(len(M))
        for freq in [1,2,4]:
            mm=M*freq
            tru=target_vals(q,coef,mm)
            y=tru[:,0]*tru[:,1]+tru[:,2]*tru[:,3]+.4*tru[:,0]*tru[:,2]*tru[:,4]
            for mode in ['none','iid40','hole18','hole28']:
                for name in ['random','local','mhu','cvt']:
                    yp,deleted=inference(a[name],lab,q,coef,mm,k=24,band=.05 if freq==1 else .035,drop_mode=mode,drop_seed=worldseed+999)
                    result.append({'geometry_seed':seed,'world_seed':worldseed,'method':name,'freq':freq,'deletion':mode,'deleted':deleted,'mse':float(np.mean((yp-y)**2))})
    (OUT/f'field_metrics_{seed}.json').write_text(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['generate','geometry','fields']);p.add_argument('seed',type=int);p.add_argument('--iterations',type=int,default=600);a=p.parse_args()
    torch.set_num_threads(2)
    if a.command=='generate':generate(a.seed,a.iterations)
    if a.command=='geometry':print(json.dumps(geometry(a.seed),indent=2))
    if a.command=='fields':
        x=fields(a.seed)
        print('FIELDED',a.seed,len(x),'rows',flush=True)
