import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));import br30_previous as br
B=Path(__file__).resolve().parents[1]
g={k:(np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{k}_geometry.npz'))['points'],np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{k}_geometry.npz'))['labels']) for k in ('local','mhu','random')}
for s in [1701,1702,1703]:
 d=np.load(B/'data'/f'cvt_refined_4096_{s}.npz');g[f'cvt_{s}']=(d['points'],d['labels'])
out=[]
for drop in (0,.2,.4,.6):
 for seed in range(9301,9313):
  q,a,m,y=br.ds(seed,300,1)
  for name,(p,t) in g.items():
   # identical dropout mask indices (indices of CVT randomized; controls physical counts, not joint spatial deletions)
   rg=np.random.default_rng(211000+seed);mask=rg.random(len(p))>=drop
   yp=br.infer(p[mask],t[mask],q,a,m,k=16,band=.05)
   out.append({'drop':drop,'seed':seed,'geometry':name,'MSE':float(np.mean((yp-y)**2))})
(B/'data'/'dropout_4096.json').write_text(json.dumps(out,indent=1))
for drop in (0,.2,.4,.6):
 print('drop',drop,{n:round(float(np.mean([x['MSE'] for x in out if x['drop']==drop and x['geometry']==n])),4) for n in g})
