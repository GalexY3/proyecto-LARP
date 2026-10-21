from pathlib import Path
import sys,json,time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import br30_previous as br
from scipy.spatial import cKDTree
root=Path(__file__).resolve().parents[1];labels=np.load(Path(__file__).resolve().parents[1]/'data/geometrias/local_geometry.npz')['labels']
geos={x:np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{x}_geometry.npz'))['points'] for x in ('local','mhu','random')}
for ss in [1701,1702,1703]:geos[f'cvt_refined_{ss}']=np.load(root/'data'/f'cvt_refined_4096_{ss}.npz')['points']
for ss in [1704,1705,1706]:geos[f'cvt_base_{ss}']=np.load(root/'data'/f'cvt_4096_{ss}.npz')['points']
BANDS=[.035,.05,.075,.11,.16]
rec=[]
for split,seeds in [('dev',range(5101,5109)),('heldout',range(6101,6113))]:
 for freq in [1,2,5]:
  for seed in seeds:
   q,a,m,y=br.ds(seed,384,freq)
   # compute values once per geometry
   for name,p in geos.items():
    dd,ix=cKDTree(p,boxsize=1).query(q,k=24)
    t=labels[ix];sensor=br.np.cos(2*br.np.pi*p[ix]@m.T)@a[:,:,0].T+br.np.sin(2*br.np.pi*p[ix]@m.T)@a[:,:,1].T
    obs=br.np.take_along_axis(sensor,t[...,None],axis=-1)[...,0]
    for bandwidth in BANDS:
     weights=np.exp(-.5*(dd/bandwidth)**2);ch=np.zeros((len(q),5))
     for tt in range(5):
      w=weights*(t==tt);ch[:,tt]=(w*obs).sum(1)/np.maximum(w.sum(1),1e-12)
     yp=ch[:,0]*ch[:,1]+ch[:,2]*ch[:,3]+.4*ch[:,0]*ch[:,2]*ch[:,4]
     rec.append(dict(split=split,freq=freq,seed=seed,name=name,band=bandwidth,mse=float(np.mean((yp-y)**2))))
   print('phase',split,'freq',freq,'seed',seed,flush=True)
(root/'data'/'bandwidth_all.json').write_text(json.dumps(rec,indent=1))
# optimize kernel bandwidth on dev for each (freq,geometry) and eval on heldout, NOT further tuning
chosen={};reports=[]
for f in [1,2,5]:
 for name in geos:
  d=[x for x in rec if x['split']=='dev' and x['freq']==f and x['name']==name]
  by={bw:float(np.mean([x['mse'] for x in d if x['band']==bw])) for bw in BANDS}
  bw=min(by,key=by.get);chosen[f'{f}|{name}']=bw
  t=[x for x in rec if x['split']=='heldout' and x['freq']==f and x['name']==name and x['band']==bw]
  reports.append({'freq':f,'name':name,'chosen_band_dev':bw,'dev_mse':by[bw],'heldout_mse':float(np.mean([x['mse'] for x in t]))})
(root/'data'/'bandwidth_heldout_summary.json').write_text(json.dumps(reports,indent=2))
for f in [1,2,5]:
 print('FREQ',f,[(r['name'],round(r['heldout_mse'],4),r['chosen_band_dev']) for r in reports if r['freq']==f])
