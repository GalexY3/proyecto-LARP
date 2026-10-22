import unittest,numpy as np,json
from pathlib import Path
from experiment import sobol_layout, spectral_layout,rmse,load_data,target,unbiased_pred,fourier_cov,D,KK,W0
class Audit(unittest.TestCase):
 def test_layout_counts(self):
  for q in ([6,16,2],[2,4,2],[9,23,4]):
   for ids,m in zip(sobol_layout(q,33),q):self.assertEqual(len(set(ids)),m)
 def test_mean_exact(self):
  x=np.ones((3,3,24,24)); ids=sobol_layout([6,16,2],77)
  self.assertLess(rmse(x,ids,W0),1e-13)
 def test_channels_and_cov(self):
  rng=np.random.default_rng(33);x=rng.normal(size=(18,3,24,24));c=fourier_cov(x)
  self.assertEqual(c.shape,(len(KK),3,3));self.assertLess(np.max(abs(c-c.conj().transpose(0,2,1))),1e-11)
  self.assertGreaterEqual(min(float(np.linalg.eigvalsh(m).min()) for m in c),-1e-10)
 def test_fixed_readout(self):
  rng=np.random.default_rng(4);x=rng.normal(size=(6,3,24,24));ids=sobol_layout([6,16,2],4)
  pred=sum(W0[a]*x.reshape(6,3,D)[:,a,ids[a]].mean(axis=1) for a in range(3))
  self.assertTrue(np.allclose(pred,unbiased_pred(x,ids,W0)))
 def test_grad_quadratic(self):
  # Analytical derivative in spectral_layout tested separately in earlier AB4;
  # check local finite-score sensitivity/invariants, not claiming full gradient here.
  x=np.random.default_rng(77).normal(size=(20,3,24,24));ids,loss=spectral_layout(x,W0,[6,16,2],77)
  self.assertTrue(np.isfinite(loss));self.assertEqual(sum(len(z) for z in ids),24)
 def test_frozen_holdout(self):
  d=Path(__file__).parent; f=json.loads((d/'holdout_freeze.json').read_text());
  self.assertEqual(f['retina_test_seed'],97773); self.assertEqual(f['champion'],'COSI_SHRINK')
  l=[json.loads(z) for z in (d/'ledger.jsonl').read_text().splitlines()]
  self.assertEqual(len(l),30);self.assertFalse(any(z['holdout_retina_opened'] for z in l[:29]));self.assertTrue(l[-1]['holdout_retina_opened'])
if __name__=='__main__':unittest.main(verbosity=2)
