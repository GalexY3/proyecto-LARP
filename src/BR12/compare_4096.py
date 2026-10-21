from pathlib import Path
import sys,time,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import br30_previous as br
ROOT=Path(__file__).resolve().parents[1]
GEOM={x:(np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{x}_geometry.npz'))['points'],np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{x}_geometry.npz'))['labels']) for x in ('local','mhu','random')}
labels=GEOM['random'][1];rg=np.random.default_rng(150123);pos=np.zeros((4096,3))
for tt in range(5):
 ids=np.where(labels==tt)[0]; count=len(ids); g=int(np.ceil(count**(1/3)))
 cells=np.indices((g,g,g)).reshape(3,-1).T
 selected=rg.permutation(len(cells))[:count]
 pos[ids]=((cells[selected]+rg.uniform(.1,.9,(count,3)))/g + rg.random((1,3)))%1
GEOM['stratified']=(pos,labels)
for seed in range(1701,1707):
 with np.load(ROOT/'data'/f'cvt_4096_{seed}.npz') as arr:GEOM[f'cvt_{seed}']=(arr['points'],arr['labels'])
results=[]
for freq in [1,2,5]:
 for k in [16,24]:
  for seed in range(3101,3113):
   q,a,m,y=br.ds(seed,300,freq)
   for name,(p,t) in GEOM.items():
    pred=br.infer(p,t,q,a,m,k=k,band=.11)
    results.append({'world_seed':seed,'frequency':freq,'neighbors':k,'method':name,'mse':float(np.mean((pred-y)**2))})
  print('finished',freq,k,flush=True)
(ROOT/'data'/'predict_4096.json').write_text(json.dumps(results,indent=1))
summary={}
for f in [1,2,5]:
 for k in [16,24]:
  x=[z for z in results if z['frequency']==f and z['neighbors']==k]
  summary[f'f{f}_k{k}']={name:float(np.mean([z['mse'] for z in x if z['method']==name])) for name in GEOM}
  summary[f'f{f}_k{k}']['cvt_mean']=float(np.mean([summary[f'f{f}_k{k}'][n] for n in GEOM if n.startswith('cvt_')]))
(ROOT/'data'/'predict_4096_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
