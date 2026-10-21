import sys,time,json
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parents[1]
local=np.load(Path(__file__).resolve().parents[1]/'data/geometrias/local_geometry.npz');typ=local['labels'];orig={g:np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{g}_geometry.npz'))['points'] for g in ['local','mhu','random']}
def cvt(s,niter=8,nq=15000):
 r=np.random.default_rng(s);p=r.random((len(typ),3));ids_list=[np.flatnonzero(typ==i) for i in range(5)]
 for iteration in range(niter):
  q=r.random((nq,3))
  for ids in ids_list:
   pts=p[ids];_,near=cKDTree(pts,boxsize=1).query(q)
   delta=(q-pts[near]+.5)%1-.5
   acc=np.zeros_like(pts);np.add.at(acc,near,delta)
   count=np.bincount(near,minlength=len(ids));p[ids]=(pts+.72*acc/np.maximum(count[:,None],1))%1
 return p
q=np.random.default_rng(880888).random((2500,3))

def metric(p):
 dd,ii=cKDTree(p,boxsize=1).query(q,k=32)
 tt=typ[ii];return {str(k):float(np.all([(tt[:,:k]==t).any(1) for t in range(5)],axis=0).mean()) for k in [8,12,16,24,32]}
results={'original':{n:metric(p) for n,p in orig.items()},'cvt':{}}
for s in range(1701,1707):
 st=time.time();p=cvt(s);results['cvt'][str(s)]=metric(p)
 np.savez_compressed(ROOT/'data'/f'cvt_4096_{s}.npz',points=p,labels=typ)
 print('seed',s,'seconds',round(time.time()-st,2),'cover',results['cvt'][str(s)]['16'],flush=True)
(ROOT/'data'/'fast_4096.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
