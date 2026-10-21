"""AB BR30 dynamic research: new Scale3D v2 realizations versus per-type CVT.

All tests are exploratory; the first preregistration is a *process* registration.
Commit source before running. Only generate with the original vendored code.
Original source source: archived LARP_LOCAL_MHU_DISTRIBUCIONES_REALES.zip.
CVT is per-type Lloyd, NOT Wei 2010. CPU-only environment.
"""
from __future__ import annotations
import argparse, json, time, hashlib
from pathlib import Path
import numpy as np
import torch
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix, csgraph
from scipy.sparse.linalg import eigsh
from original import scale3d_geometry_v2 as s3

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
N=4096
SEEDS=(5201,5202,5203,5204)
CATEGORIES=('random','local','mhu','cvt')
MODE=np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,-1,0],[0,1,-1],[1,0,-1],[2,0,0],[0,2,0],[0,0,2]],dtype=float)

def load(seed,kind):
    with np.load(DATA/f'{kind}_{seed}.npz') as z: return z['points'],z['labels']

def cvt(start,labels,seed,steps=24,nq=16000):
    rng=np.random.default_rng(seed+60000);p=start.copy()
    ids=[np.flatnonzero(labels==c) for c in range(5)]
    for it in range(steps):
        qry=rng.random((nq,3))
        for ii in ids:
            x=p[ii];_,n=cKDTree(x,boxsize=1).query(qry)
            displacement=(qry-x[n]+.5)%1-.5
            sums=np.zeros_like(x); np.add.at(sums,n,displacement)
            counts=np.bincount(n,minlength=len(ii))
            p[ii]=(x+.72*sums/np.maximum(counts[:,None],1))%1
    return p

def build(seed,iterations=600):
    st=time.perf_counter()
    for kind in ('random','local','mhu'):
        dest=DATA/f'{kind}_{seed}.npz'
        if dest.exists(): raise RuntimeError(f'No overwrite of original result: {dest}')
        if kind=='random':
            r=np.random.default_rng(seed)
            p=r.random((N,3)); labels=r.permutation(np.repeat(np.arange(5),s3.v1.hamilton_counts(N)))
            meta={'generator':'numpy PCG64 original initialization','seed':seed,'elapsed':0}
        else:
            result=s3.generate(seed,N,iterations=iterations,spectral=(kind=='mhu'),validate=False)
            p=result['coordinates'].cpu().numpy();labels=result['labels'].cpu().numpy()
            meta=result['construction']; meta['final_loss']=result['history'][-1]['loss']
        np.savez_compressed(dest,points=p,labels=labels)
        (DATA/f'{kind}_{seed}.json').write_text(json.dumps(meta,indent=2))
        print('built',kind,seed,'sec',round(time.perf_counter()-st,2),flush=True)
    r,labels=load(seed,'random')
    p=cvt(r,labels,seed)
    np.savez_compressed(DATA/f'cvt_{seed}.npz',points=p,labels=labels)
    (DATA/f'cvt_{seed}.json').write_text(json.dumps({'generator':'Lloyd per type, not Wei 2010','steps':24,'nq':16000,'seed':seed,'elapsed_cumulative':time.perf_counter()-st},indent=2))
    print('built cvt',seed,'total sec',round(time.perf_counter()-st,2),flush=True)

def cover(points,labels,query,k):
    ds,idx=cKDTree(points,boxsize=1).query(query,k=k)
    ty=labels[idx]
    return float(np.all(np.stack([(ty==t).any(axis=1) for t in range(5)],axis=1),axis=1).mean()),float(ds[:,-1].mean())

def fourier_fields(positions,coeff,freq):
    modes=MODE*freq; phase=2*np.pi*positions@modes.T
    return np.cos(phase)@coeff[:,:,0].T+np.sin(phase)@coeff[:,:,1].T

def target(f):return f[:,0]*f[:,1]+f[:,2]*f[:,3]+.4*f[:,0]*f[:,2]*f[:,4]

def infer(points,labels,query,coeff,freq,k=24,band=.05,drop_mask=None):
    sensor=fourier_fields(points,coeff,freq)[np.arange(len(points)),labels]
    if drop_mask is not None:
        points=points[drop_mask];labels=labels[drop_mask];sensor=sensor[drop_mask]
    ds,idx=cKDTree(points,boxsize=1).query(query,k=min(k,len(points)))
    ll=labels[idx];v=sensor[idx]
    weights=np.exp(-.5*(ds/band)**2)
    estimates=np.zeros((len(query),5))
    for t in range(5):
        w=weights*(ll==t)
        estimates[:,t]=(w*v).sum(axis=1)/np.maximum(w.sum(axis=1),1e-12)
    return target(estimates)

def spectral(points,labels):
    # Same 80-mode finite sample as prior audit, + individual-type Fourier powers.
    from itertools import product
    mm=np.array([m for m in product(range(-3,4),repeat=3) if 0<np.linalg.norm(m)<=2.5])
    def S(p):
        ph=2*np.pi*p@mm.T
        z=np.exp(1j*ph).sum(axis=0)
        return float((np.abs(z)**2/len(p)).mean())
    return {'union80':S(points),**{f'type{t}':S(points[labels==t]) for t in range(5)}}

def network_topology(points,labels,k=12):
    ds,idx=cKDTree(points,boxsize=1).query(points,k=k+1)
    n=len(points);rows=np.repeat(np.arange(n),k);cols=idx[:,1:].reshape(-1)
    A=coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(n,n)).tocsr();A=((A+A.T)>0).astype(float)
    count,ncomps=0,0
    ncomps,comp=csgraph.connected_components(A)
    degrees=np.array(A.sum(axis=1)).ravel()
    D=degrees**-.5
    L=coo_matrix((np.ones(n),(np.arange(n),np.arange(n))),shape=(n,n)).tocsr()-A.multiply(D[:,None]).multiply(D[None,:])
    try:
        eig=np.sort(eigsh(L,k=3,which='SM',return_eigenvectors=False,tol=2e-3,maxiter=2500))
        gap=float(eig[1])
    except Exception:gap=None
    inter=float((labels[rows]!=labels[cols]).mean())
    return {'components':int(ncomps),'mean_degree':float(degrees.mean()),'spectral_gap_normalized':gap,'cross_type_directed_fraction':inter}

def audit(seeds,worlds=8,query_n=350):
    rows=[];queries=np.random.default_rng(991212).random((2500,3))
    for seed in seeds:
        layouts={g:load(seed,g) for g in CATEGORIES}
        for kind,(p,l) in layouts.items():
            geom={'seed':seed,'kind':kind,'type':'geometry','N':len(p)}
            geom.update({f'cover{k}':cover(p,l,queries,k)[0] for k in (8,12,16,24)})
            geom.update(spectral(p,l))
            geom.update(network_topology(p,l,k=12))
            rows.append(geom)
            print('geom',seed,kind,round(geom['cover16'],4),round(geom['union80'],7),geom['spectral_gap_normalized'],flush=True)
        # Environmental perturbations: iid loss or correlated hole of a sphere on a torus.
        for world in range(worlds):
            rng=np.random.default_rng(13370000+seed*101+world)
            q=rng.random((query_n,3))
            coeff=rng.standard_normal((5,len(MODE),2))/np.sqrt(len(MODE))
            for freq in (1,2,4):
                truth=target(fourier_fields(q,coeff,freq))
                for kind,(p,l) in layouts.items():
                    for outage in ('none','independent40','ball_radius_022'):
                        mask=None
                        if outage=='independent40':
                            # same random ordering within label strata, not paired physical location
                            mask=np.random.default_rng(seed*2347+world).random(len(p))>=.40
                        elif outage=='ball_radius_022':
                            center=np.random.default_rng(818100+world).random(3)
                            dd=(p-center+.5)%1-.5
                            mask=(np.linalg.norm(dd,axis=1)>=.22)
                        pred=infer(p,l,q,coeff,freq,k=24,band=.05 if freq==1 else .035,drop_mask=mask)
                        rows.append({'type':'world','seed':seed,'world':world,'kind':kind,'freq':freq,'outage':outage,'mse':float(np.mean((pred-truth)**2)), 'remaining':int(mask.sum()) if mask is not None else len(p)})
        print('evaluated seed',seed,flush=True)
    outfile=DATA/'audit_results.json';outfile.write_text(json.dumps({'config':{'seeds':seeds,'worlds_per_geometry':worlds,'queries_per_world':query_n,'bandwidth_f1':.05,'bandwidth_other':.035},'rows':rows},indent=1))
    summaries=[]
    for typ in ('geometry','world'):
        ss=[r for r in rows if r['type']==typ]
        from collections import defaultdict
        sets=defaultdict(list)
        for r in ss:
            keys=('kind',) if typ=='geometry' else ('kind','freq','outage')
            key=tuple(r[k] for k in keys)
            sets[key].append(r)
        for key,sub in sets.items():
            metrics=('cover8','cover12','cover16','cover24','union80','spectral_gap_normalized','cross_type_directed_fraction') if typ=='geometry' else ('mse','remaining')
            for metric in metrics:
                x=np.array([r[metric] for r in sub if r.get(metric) is not None]);
                if len(x):summaries.append(dict(group=key,metric=metric,n=len(x),mean=float(x.mean()),sd=float(x.std(ddof=1)) if len(x)>1 else None))
    (DATA/'audit_summary.json').write_text(json.dumps(summaries,indent=1))
    print('Wrote',len(rows),'rows',len(summaries),'summaries',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['generate','audit']);ap.add_argument('--seed',type=int,default=SEEDS[0]);ap.add_argument('--seeds',type=int,nargs='+',default=list(SEEDS));ap.add_argument('--steps',type=int,default=600);a=ap.parse_args()
    torch.set_num_threads(2)
    if a.mode=='generate':build(a.seed,a.steps)
    if a.mode=='audit':audit(a.seeds)
