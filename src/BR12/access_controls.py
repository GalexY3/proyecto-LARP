import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import br30_previous as br
base=Path(__file__).resolve().parents[1]
g={n:(np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{n}_geometry.npz'))['points'],np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{n}_geometry.npz'))['labels']) for n in ['local','mhu','random']}
for s in [1701,1702,1703]:
 with np.load(base/'data'/f'cvt_refined_4096_{s}.npz') as z:g[f'cvt_{s}']=(z['points'],z['labels'])
R=[]
for f in [1,2]:
 for seed in range(7101,7121):
  q,a,m,y=br.ds(seed,384,f)
  for name,(p,t) in g.items():
   models={'unstructured_nearest16':br.infer(p,t,q,a,m,k=16,band=.05 if f==1 else .035),
          'oracled_5_per_type':br.infer_nearest_per_type(p,t,q,a,m)}
   for mode,yp in models.items():R.append({'seed':seed,'frequency':f,'model':name,'access':mode,'mse':float(np.mean((yp-y)**2))})
(base/'data'/'access_comparison.json').write_text(json.dumps(R,indent=2))
for f in [1,2]:
 for name in g:
  print(f,name,[(md,round(float(np.mean([r['mse'] for r in R if r['frequency']==f and r['model']==name and r['access']==md])),4)) for md in ('unstructured_nearest16','oracled_5_per_type')])
