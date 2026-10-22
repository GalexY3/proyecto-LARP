"""Meaningful checks for the independent avian candidate, without full runs."""
from pathlib import Path
import json
import numpy as np
import pytest

from larp.avian import (load_avian_config, cell_radii, homotypic_distances,
                        avian_objective, check_avian_gradient, generate_avian,
                        packing_diagnostics, avian_local_identity)
from larp.geometry import Geometry


def initial(seed=987):
    config = load_avian_config()
    rng = np.random.default_rng(seed)
    labels = rng.permutation(np.repeat(np.arange(5), config["counts_A_to_E"]))
    return rng.uniform(0, 20, (400, 2)), labels


def test_frozen_counts_physical_radii_and_homotypic_distance():
    config = load_avian_config()
    assert config["counts_A_to_E"] == [163, 85, 68, 50, 34]
    assert config["geometry_seeds"] == [1101, 1102, 1103]
    assert np.isclose(np.pi*np.dot(config["counts_A_to_E"], cell_radii()**2)/400, .58)
    assert np.allclose(cell_radii()/cell_radii()[-1], [1.5, 1.13, 1.06, 1.19, 1])
    assert np.allclose(homotypic_distances()**2*np.array(config["counts_A_to_E"])/400, 2/np.sqrt(3))


@pytest.mark.parametrize("treatment", ["full_spectral", "local_only"])
@pytest.mark.parametrize("growth", [.25, 1.0])
def test_analytic_gradient_random_active_pairs(treatment, growth):
    points, labels = initial()
    result = check_avian_gradient(points, labels, treatment=treatment, growth=growth,
                                 coordinates=28, epsilon=2e-6)
    assert result["passed"], result
    assert result["maximum_scaled_error"] < 2e-6


@pytest.mark.parametrize("treatment", ["full_spectral", "local_only"])
def test_translation_and_permutation_equivariance(treatment):
    points, labels = initial()
    value, gradient = avian_objective(points, labels, treatment=treatment)
    shifted, shifted_gradient = avian_objective((points+[11.3, -7.9]) % 20, labels, treatment=treatment)
    assert np.isclose(value, shifted, atol=1e-10, rtol=1e-12)
    assert np.allclose(gradient, shifted_gradient, atol=1e-10, rtol=1e-11)
    permutation = np.random.default_rng(1).permutation(400)
    permuted, permuted_gradient = avian_objective(points[permutation], labels[permutation], treatment=treatment)
    assert np.isclose(value, permuted, rtol=1e-12)
    assert np.allclose(gradient[permutation], permuted_gradient, atol=1e-10)
    assert np.linalg.norm(gradient.sum(axis=0)) < 1e-9


def test_local_only_removes_exactly_the_spectral_component():
    points, labels = initial()
    full, gf, full_parts = avian_objective(points, labels, details=True)
    local, gl, local_parts = avian_objective(points, labels, treatment="local_only", details=True)
    assert local_parts["spectral_energy"] == 0
    assert np.isclose(full-local, full_parts["spectral_energy"])
    assert full_parts["packing_energy"] == local_parts["packing_energy"]
    assert full_parts["homotypic_energy"] == local_parts["homotypic_energy"]
    assert not np.allclose(gf, gl)


def test_invalid_collisions_counts_and_growth_rejected():
    points, labels = initial()
    points[1] = points[0]
    with pytest.raises(ValueError, match="collision"):
        avian_objective(points, labels)
    points, labels = initial()
    labels[0] = (labels[0]+1) % 5
    with pytest.raises(ValueError, match="counts"):
        avian_objective(points, labels)
    with pytest.raises(ValueError, match="growth"):
        avian_objective(points, initial()[1], growth=0)


def test_original_scientific_profile_is_not_silently_relaxed():
    with pytest.raises(ValueError, match="Budget overrides"):
        generate_avian(1101, adam_steps=1)
    with pytest.raises(ValueError, match="seeds"):
        generate_avian(1104)
    with pytest.raises(ValueError, match="10000 common"):
        generate_avian(1101, centers=np.zeros((10000, 2)))


def test_reduced_generation_reproducible_and_never_admitted(tmp_path):
    centers = np.random.default_rng(1).uniform(0, 20, (20, 2))
    args = dict(test_only=True, adam_steps=3, lbfgs_iterations=0, max_attempts=1,
                maximum_seconds=20, centers=centers)
    a = generate_avian(1101, output_dir=tmp_path, **args)
    b = generate_avian(1101, **args)
    assert a.hashes == b.hashes
    assert a.metadata["test_only"]
    assert not a.metadata["admitted"]
    assert not a.metadata["certificate"]["scientific_admissible"]
    assert Geometry.load(tmp_path/"avian_full_spectral_N400_g1101.npz").hashes == a.hashes
    assert a.metadata["attempts"][0]["adam_steps"] == 3


def test_timeout_is_retained_as_failure_not_certificate_promotion(tmp_path):
    centers = np.random.default_rng(1).uniform(0, 20, (10, 2))
    geometry = generate_avian(1101, test_only=True, maximum_seconds=1e-12,
                              adam_steps=20, lbfgs_iterations=0, max_attempts=4,
                              centers=centers, output_dir=tmp_path)
    assert geometry.metadata["optimizer"]["status"] == "RESOURCE_LIMIT"
    assert len(geometry.metadata["attempts"]) == 1
    assert not geometry.metadata["admitted"]
    assert geometry.metadata["attempts"][0]["adam_steps"] == 0


def test_packing_reports_soft_penalty_and_real_overlap():
    points, labels = initial()
    result = packing_diagnostics(Geometry(points, labels, 20))
    assert result["maximum_relative_overlap"] > .002
    assert not result["packing_admitted"]
    assert result["nominal_disk_area_fraction"] == pytest.approx(.58)
    assert "soft_penalty" in result["hard_core_enforcement"]


def test_local_manifest_does_not_hash_unrelated_parallel_modules():
    identity = avian_local_identity()
    assert "src/larp/model.py" not in identity["files"]
    assert "src/larp/avian.py" in identity["files"]
    assert "configs/avian_v1.json" in identity["files"]
