from pathlib import Path
import numpy as np,json,time
from scipy.spatial import cKDTree
base=Path(__file__).resolve().parents[1];labels=np.load(Path(__file__).resolve().parents[1]/'data/geometrias/local_geometry.npz')['labels']
q=np.random.default_rng(880888).random((2500,3))
res={}
for s in [1701,1702,1703]:
 p=np.load(base/'data'/f'cvt_4096_{s}.npz')['points']
 rng=np.random.default_rng(s+95000)
 start=time.time()
 for it in range(15):
  qq=rng.random((24000,3))
  for tt in range(5):
   ix=np.where(labels==tt)[0];sub=p[ix];_,nearest=cKDTree(sub,boxsize=1).query(qq)
   dis=(qq-sub[nearest]+.5)%1-.5
   delta=np.zeros_like(sub);np.add.at(delta,nearest,dis)
   cnt=np.bincount(nearest,minlength=len(ix))
   p[ix]=(sub+.72*delta/np.maximum(cnt[:,None],1))%1
 dd,idx=cKDTree(p,boxsize=1).query(q,k=24)
 t=labels[idx];cov=float(np.stack([(t[:,:16]==x).any(1) for x in range(5)],axis=1).all(1).mean())
 np.savez_compressed(base/'data'/f'cvt_refined_4096_{s}.npz',points=p,labels=labels)
 res[str(s)]={'coverage16':cov,'elapsed':time.time()-start}
 print(s,cov,'seconds',round(res[str(s)]['elapsed'],1),flush=True)
(base/'data'/'cvt_refined_metrics.json').write_text(json.dumps(res,indent=2))
