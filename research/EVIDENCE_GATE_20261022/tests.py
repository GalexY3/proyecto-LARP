import unittest, sys, json,hashlib
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P));from bench import load,get,metrics,unbiased_pred,target,W,SIDE,QUOTA
from repair_gp import full_gp
class TestEvidenceGate(unittest.TestCase):
 def test_sources_shapes(self):
  for name in ['camera','moon','gravel','brick','cell','microaneurysms']:
   x=load(name,2,53)
   self.assertEqual(x.shape,(2,3,SIDE,SIDE));self.assertTrue(np.all(np.isfinite(x)))
 def test_estimator_exact_for_full_grid(self):
  x=load('camera',5,12)
  pred=unbiased_pred(x,[np.arange(SIDE**2) for a in range(3)],W)
  self.assertLess(float(np.max(abs(pred-target(x,W)))),2e-6)
 def test_full_gp_quota_and_bounds(self):
  x=load('moon',18,20)
  ids=full_gp(x)
  self.assertEqual([len(i) for i in ids],QUOTA)
  for arr in ids:
   self.assertEqual(len(arr),len(np.unique(arr)))
   self.assertGreaterEqual(min(arr),0);self.assertLess(max(arr),SIDE**2)
 def test_holdout_freeze_link(self):
  b=(P/'HOLDOUT_FREEZE.json').read_bytes();r=json.loads((P/'TEST_RESULTS.json').read_text());
  self.assertEqual(hashlib.sha256(b).hexdigest(),r['freeze_sha256'])
  self.assertEqual(len(r['results']),6*5*4*2)
 def test_no_source_overwriting(self):
  d=json.loads((P/'HOLDOUT_FREEZE.json').read_text())
  self.assertFalse(set(d['train_sources'])&set(d['test_sources']))
  self.assertNotIn(d['dev_sources'],d['test_sources'])
 def test_deterministic_patches(self):
  self.assertTrue(np.array_equal(load('gravel',3,100),load('gravel',3,100)))
if __name__=='__main__':unittest.main(verbosity=2)
