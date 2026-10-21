from itertools import product
from pathlib import Path
import numpy as np,json
B=Path(__file__).resolve().parents[1]
labels=np.load(Path(__file__).resolve().parents[1]/'data/geometrias/local_geometry.npz')['labels']
M=np.array([m for m in product(range(-3,4),repeat=3) if 0<np.linalg.norm(m)<=2.5]);freq_norm=np.linalg.norm(M,axis=1)
g={name:np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{name}_geometry.npz'))['points'] for name in ('local','mhu','random')}
for seed in [1701,1702,1703]:g[f'cvt_{seed}']=np.load(B/'data'/f'cvt_refined_4096_{seed}.npz')['points']
out={}
for name,pts in g.items():
 d={};idxlist=[np.arange(len(pts))]+[np.flatnonzero(labels==t) for t in range(5)]
 for ii,idx in enumerate(idxlist):
  val=np.exp(2j*np.pi*pts[idx]@M.T).sum(0)
  power=(np.abs(val)**2)/len(idx)
  d['all' if ii==0 else f'type{ii-1}']=float(np.mean(power))
 out[name]=d
(B/'data'/'spectrum_finite.json').write_text(json.dumps({'modes':len(M),'metrics':out,'description':'S(k) mean for discrete modes 0<|m|<=2.5; not a proof of HU'},indent=2))
print('modes',len(M));print(json.dumps(out,indent=2))
