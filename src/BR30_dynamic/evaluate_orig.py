"""Exploratory evaluation with real Scale3D v2 generated points.
Separate fixed external CVT reference geometries from BR12; NOT Wei algorithm.
Geometries are independent draws; CVT not initial-state-paired to original seeds.
"""
from pathlib import Path
from itertools import product
import json,sys
import numpy as np
from scipy.spatial import cKDTree
from experiment import target_vals,inference,M
R=Path(__file__).resolve().parent; D=R/'data'
N=4096
MODES=np.array([k for k in product(range(-3,4),repeat=3) if 0<np.linalg.norm(k)<=2.5],dtype=int)

def load(seed):
 with np.load(D/f'orig_{seed}.npz') as z: base={k:z[k] for k in z.files}
 lab=base['labels'];maps={k:base[k] for k in ('initial','local','mhu')}
 for s in [1701,1702,1703]:
  with np.load(D/f'cvt_refined_4096_{s}.npz') as z:
   c=z['points'];t=z['labels']
  p=np.empty_like(c)
  for j in range(5):p[lab==j]=c[t==j]
  maps[f'cvt_refined_{s}']=p
 return maps,lab

def geometry(seed):
 g,t=load(seed);q=np.random.default_rng(seed+151000).random((3000,3));res=[]
 for name,points in g.items():
  d,ii=cKDTree(points,boxsize=1).query(q,k=24)
  types=t[ii]
  row={'seed':seed,'name':name}
  for k in [8,12,16,24]:row[f'cover_{k}']=float(np.stack([(types[:,:k]==z).any(1) for z in range(5)],axis=1).all(1).mean())
  row['r5_mean']=float(np.stack([cKDTree(points[t==j],boxsize=1).query(q,k=1)[0] for j in range(5)]).max(0).mean())
  for j in [-1,0,1,2,3,4]:
   p=points if j==-1 else points[t==j]
   ph=2*np.pi*p@MODES.T
   r=np.abs(np.exp(1j*ph).sum(0))**2/len(p)
   row['S_union' if j==-1 else f'S_{j}']=float(r.mean())
  res.append(row)
 (D/f'geometry_eval_{seed}.json').write_text(json.dumps(res,indent=2))
 print('GEO',seed,[(x['name'],round(x['cover_16'],4),round(x['S_union'],7)) for x in res],flush=True)
 return res

def predictive(seed,worlds=6):
 g,lab=load(seed);rows=[]
 for s in range(worlds):
  rng=np.random.default_rng(seed*100+s+81000);q=rng.random((350,3));a=rng.standard_normal((5,len(M),2))/np.sqrt(len(M))
  for freq in [1,2,4]:
   mm=M*freq;true=target_vals(q,a,mm);target=true[:,0]*true[:,1]+true[:,2]*true[:,3]+.4*true[:,0]*true[:,2]*true[:,4]
   for deletion in ['none','iid40','hole18','hole28']:
    for name,p in g.items():
     yh,deleted=inference(p,lab,q,a,mm,k=24,band=.05 if freq==1 else .035,drop_mode=deletion,drop_seed=seed*100000+s+901)
     rows.append({'seed':seed,'world':s,'freq':freq,'deletion':deletion,'name':name,'deleted':deleted,'mse':float(np.mean((yh-target)**2))})
 (D/f'predictive_eval_{seed}.json').write_text(json.dumps(rows,indent=1))
 for d in ['none','hole28']:
  print('PRED',seed,'freq1',d,[(name,round(float(np.mean([x['mse'] for x in rows if x['freq']==1 and x['deletion']==d and x['name']==name])),4)) for name in g],flush=True)
if __name__=='__main__':
 for seed in [int(s) for s in sys.argv[1:]]:
  geometry(seed);predictive(seed)
