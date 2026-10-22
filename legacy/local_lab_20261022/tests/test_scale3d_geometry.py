"""Small invariant checks, not scientific geometry-quality experiments."""
import math

import numpy as np
import pytest
import torch

from larp.scale3d_geometry import (cic_density, exact_structure_factor, generate,
                                  hamilton_counts, reciprocal_modes, validate_geometry)


def test_hamilton_preserves_original_ratios_counts_and_ties():
    np.testing.assert_array_equal(hamilton_counts(400), [163,85,68,50,34])
    for N in [1024,4096,16384,32768]:
        counts = hamilton_counts(N)
        assert counts.sum() == N and counts.min() >= 2
        assert np.abs(counts - N*np.array([163,85,68,50,34])/400).max() < 1


def test_cic_conserves_each_component_mass_and_periodicity():
    points = torch.tensor([[.13,.27,.34],[.93,.96,.99],[1.01,-.2,.4]], dtype=torch.float64)
    labels = torch.tensor([0,1,0])
    density = cic_density(points, labels, 8, 2)
    torch.testing.assert_close(density.sum((1,2,3)), torch.tensor([2.,1.], dtype=torch.float64))
    torch.testing.assert_close(density, cic_density(points+torch.tensor([2.,-3.,1.]), labels, 8, 2))


def test_cic_gradient_matches_independent_trilinear_vertex_derivative():
    # Within a cell, d(x*y*z)/dx is independently known.
    points = torch.tensor([[.17,.29,.42]], dtype=torch.float64, requires_grad=True)
    density = cic_density(points, torch.tensor([0]), 8, 1)
    density[0,2,3,4].backward()
    frac = points.detach()[0]*8 - torch.floor(points.detach()[0]*8)
    expected = 8*torch.tensor([frac[1]*frac[2],frac[0]*frac[2],frac[0]*frac[1]])
    torch.testing.assert_close(points.grad[0], expected)


def test_exact_fourier_sum_and_derivative_are_not_fft_proxy():
    points = torch.tensor([[.07,.13,.19],[.43,.31,.73]], dtype=torch.float64, requires_grad=True)
    modes = torch.tensor([[1,0,0],[1,-1,2]])
    observed = exact_structure_factor(points, modes, chunk_size=1)
    phase = 2*math.pi*points.detach().numpy() @ modes.numpy().T
    expected = abs(np.exp(1j*phase).sum(0))**2/2
    np.testing.assert_allclose(observed.detach(), expected, atol=1e-14)
    torch.autograd.gradcheck(lambda x: exact_structure_factor(x,modes), (points,), eps=1e-6, atol=1e-7)


def test_modes_use_complete_shells_and_exclude_zero_and_conjugate_duplicates():
    modes, cutoff2 = reciprocal_modes(1024, .12)
    assert len(modes) <= 3*1023*.12
    assert np.all(np.sum(modes*modes, axis=1) <= cutoff2)
    assert not np.any(np.all(modes == 0, axis=1))
    tuples = set(map(tuple,modes.tolist()))
    assert all(tuple(-m) not in tuples for m in modes)
    # Complete isotropic first shell includes each coordinate axis.
    assert {(1,0,0),(0,1,0),(0,0,1)} <= tuples


def test_generate_zero_iteration_arms_share_coordinates_labels_without_retry():
    a = generate(24, 64, iterations=0, spectral=True, grid_size=16, validate=False)
    b = generate(24, 64, iterations=0, spectral=False, grid_size=16, validate=False)
    torch.testing.assert_close(a["coordinates"],b["coordinates"])
    torch.testing.assert_close(a["labels"],b["labels"])
    assert a["coordinates"].shape == (64,3)
    assert a["box_length"] == pytest.approx(4)
    assert a["coordinates"].min() >= 0 and a["coordinates"].max() < 1


def test_exact_finite_validation_does_not_claim_asymptotic_hu():
    rng = np.random.default_rng(49)
    points = torch.tensor(rng.random((64,3)),dtype=torch.float64)
    labels = torch.tensor(np.repeat(np.arange(5),hamilton_counts(64)))
    result = validate_geometry(points, labels, sample_modes=4)
    assert len(result["components"]) == 6
    assert result["exact_audit_float64"] and not result["asymptotic_HU_established"]
    assert result["subsampled_bands"]
    assert not result["finite_low_k_pass"]


def test_validation_rejects_missing_and_extra_types_and_nonfinite_coordinates():
    points = torch.zeros((64,3),dtype=torch.float64)
    labels = torch.tensor(np.repeat(np.arange(5),hamilton_counts(64)))
    bad = labels.clone()
    bad[0] = 5
    with pytest.raises(ValueError,match="five-component"):
        validate_geometry(points,bad)
    points[0,0] = float("nan")
    with pytest.raises(ValueError,match="coordinates"):
        validate_geometry(points,labels)


@pytest.mark.parametrize("N", [0,9,10,10.5,True])
def test_invalid_counts_do_not_silently_drop_components(N):
    with pytest.raises(ValueError):
        hamilton_counts(N)
