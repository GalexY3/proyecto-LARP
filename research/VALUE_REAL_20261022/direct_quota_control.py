"""Adversarial direct empirical selection at SAME 24 measurements and role quota.
Uses only training patches; disjoint test scenes read only after design.
"""
import json,time
import numpy as np
from pathlib import Path
import real_rgb_sensors as m
import quota_ablations as qa
OUT=Path(__file__).resolve().parent

def direct(tr,q,seed,passes=5):
 rng=np.random.default_rng(seed);X=tr.reshape(len(tr),3,m.PIX).astype(np.float32)
 tgt=(X.mean(2)*m.WT).sum(1)
 ids=qa.init_ids(q,seed)
 pred=sum(m.WT[a]*X[:,a,ids[a]].mean(1) for a in range(3))
 res=pred-tgt
 for epoch in range(passes):
  changed=0
  pairs=[(a,j) for a in range(3) for j in range(q[a])]
  rng.shuffle(pairs)
  for a,j in pairs:
   prev=int(ids[a][j]);delta=(m.WT[a]/q[a])*(X[:,a,:]-X[:,a,prev,None])
   losses=np.mean((res[:,None]+delta)**2,axis=0)
   for id0 in ids[a]:
    if id0!=prev:losses[int(id0)]=np.inf
   best=int(np.argmin(losses))
   if best!=prev:
    ids[a][j]=best;res+=delta[:,best];changed+=1
  if not changed:break
 return ids

def main():
 train,_,ext=m.get_data();rows=[]
 for q in [[8,8,8],[6,16,2],[4,16,4],[4,18,2]]:
  st=time.time()
  for s in range(7):
   loc=direct(train,q,5500+s,passes=5)
   rows.append({'q':q,'seed':s,'train':qa.eval(train,loc),'rocket':qa.eval(ext['rocket'],loc),'hubble':qa.eval(ext['hubble_deep_field'],loc)})
  z=[a for a in rows if a['q']==q]
  print(q,'mean train/rocket/hubble',*[round(float(np.mean([a[k] for a in z])),5) for k in ['train','rocket','hubble']],'s/layout',round((time.time()-st)/7,2),flush=True)
 (OUT/'direct_quota_results.json').write_text(json.dumps({'notes':'Explorer, direct layout trained on exact target; not paired in CPU cost with spectral proxy','rows':rows},indent=2))
if __name__=='__main__':main()
