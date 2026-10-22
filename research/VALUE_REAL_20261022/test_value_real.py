"""Reproduction guards for 2026-10-22 real RGB exploratory study."""
import json
from pathlib import Path
import numpy as np
import real_rgb_sensors as m
import quota_ablations as q
ROOT=Path(__file__).resolve().parent

def test_gradient():
 rng=np.random.default_rng(111)
 C=m.covariance_train(rng.random((40,3,m.SIDE,m.SIDE),dtype=np.float32))
 p=rng.uniform(.1,.9,m.A*m.M*2)
 _,analytic=m.spectral_score(p,C,derivative=True)
 diffs=[]
 for i in [0,1,7,18,31,47]:
  v=np.eye(1,len(p),i).ravel()*1e-6
  fd=(m.spectral_score(p+v,C)-m.spectral_score(p-v,C))/(2e-6)
  diffs.append(abs(fd-analytic[i]))
 assert max(diffs)<1e-8, max(diffs)
 return max(diffs)

def test_results():
 base=json.loads((ROOT/'real_rgb_results.json').read_text())
 assert len(base['results'])==63
 for arm in base['summary']:
  rows=[r for r in base['results'] if r['method']==arm]
  assert len(rows)==7
  for k in ['rocket_RMSE','hubble_RMSE']:
   assert abs(np.mean([r[k] for r in rows])-base['summary'][arm][k])<1e-10
  for r in rows:
   ids=np.asarray(r['ids'])
   assert ids.shape==(3,8) and all(len(set(ids[a]))==8 for a in range(3))
 qb=json.loads((ROOT/'quota_ablations_results.json').read_text())
 assert len(qb['summary'])==24
 for s in qb['summary']:
  rows=[r for r in qb['rows'] if r['quotas']==s['quotas'] and r['method']==s['method']]
  assert len(rows)==7 and sum(s['quotas'])==24
  assert abs(s['rocket']-np.mean([r['rocket'] for r in rows]))<1e-10
 scarce=json.loads((ROOT/'pilot_quota_results.json').read_text())
 assert sorted(map(int,scarce['summary'].keys()))==[12,28,88,300,1800]
 for n in [12,28,88]:
  z=scarce['summary'][str(n)]
  assert np.mean([z['COSI-SHRINK'][k] for k in ['rocket','hubble']]) < np.mean([z['DIRECT-EMPIRICAL'][k] for k in ['rocket','hubble']])
 return True

if __name__=='__main__':
 print('Max absolute FD error:',test_gradient())
 print('Result aggregation, quotas and main negative checked:',test_results())
 print('PASS')
