import numpy as np
import torch
from larp import scale3d_geometry as v1
from larp.scale3d_geometry_v2 import objective_data,generate,full_band_audit


def test_inverse_k2_changes_only_spectral_weights_and_preserves_component_normalization():
    counts=v1.hamilton_counts(1024)
    a=v1._objective_data(counts,32,.12,torch.device('cpu'),torch.float64)
    b=objective_data(counts,32,.12,torch.device('cpu'),torch.float64)
    torch.testing.assert_close(a['local_weights'],b['local_weights'])
    torch.testing.assert_close(a['correction'],b['correction'])
    torch.testing.assert_close(a['counts'],b['counts'])
    assert a['cutoffs']==b['cutoffs']
    torch.testing.assert_close(b['spectral_weights'].sum((-3,-2,-1)),torch.ones(6,dtype=torch.float64))
    assert torch.equal(a['spectral_weights']>0,b['spectral_weights']>0)
    # Same Hermitian multiplicity: k=(1,0,0) and (2,0,0) differ solely by 1/k².
    assert torch.isclose(b['spectral_weights'][0,1,0,0]/b['spectral_weights'][0,2,0,0],torch.tensor(4.,dtype=torch.float64))


def test_local_arm_matches_frozen_v1_without_neural_changes():
    a=v1.generate(77,64,iterations=3,spectral=False,grid_size=16,validate=False)
    b=generate(77,64,iterations=3,spectral=False,grid_size=16,validate=False)
    torch.testing.assert_close(a['coordinates'],b['coordinates'],rtol=0,atol=0)
    torch.testing.assert_close(a['labels'],b['labels'])


def test_audit_tests_every_mode_and_does_not_override_an_original_failure():
    rng=np.random.default_rng(78)
    p=torch.tensor(rng.random((64,3)),dtype=torch.float64)
    z=torch.tensor(np.repeat(np.arange(5),v1.hamilton_counts(64)))
    audit=v1.validate_geometry(p,z,chi=.12,sample_modes=3)
    audit['finite_low_k_pass']=False
    out=full_band_audit(p,z,audit,.12)
    assert out['original_sampled_gate_retained'] and out['full_band_audit_float64']
    assert out['finite_mean_threshold']==.20 and not out['finite_low_k_pass']
    for c,r in zip(range(-1,5),out['components']):
        x=p if c==-1 else p[z==c]
        modes,_=v1.reciprocal_modes(len(x),.12)
        phase=2*np.pi*x.numpy()@modes.T
        independent=np.abs(np.exp(1j*phase).sum(0))**2/len(x)
        np.testing.assert_allclose(r['exact_full_band_mean'],independent.mean(),atol=1e-13)
        assert r['exact_full_band_modes']==len(modes)
        assert sum(s['modes'] for s in r['shell_profile'])==len(modes)
