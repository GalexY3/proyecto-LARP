"""Meaningful checks of independent targets, toroidal sensing and macro scores."""
from copy import deepcopy
import json

import numpy as np
import pytest

from larp.geometry import Geometry
from larp import sampling_probe as probe


def small_config():
    config = deepcopy(probe.load_probe_config())
    config.update(N=10, L=4.0, worlds_per_band=8, geometry_seeds=[1],
                  counts_A_to_E=[2]*5, families=["nominal_mhu"], query_world_side=2)
    return config


def points_and_labels():
    return np.asarray([(0.2+a*.3, .1+b*2) for a in range(5) for b in range(2)]), np.repeat(np.arange(5), 2)


def test_frozen_config_accepts_exactly_v1():
    config = probe.load_probe_config()
    assert config["neural_training"] is False and config["beliefs_updated"] is False
    assert config["geometry_seeds"] == [1101, 1102, 1103]
    assert config["worlds_per_band"] == 128


def test_zero_mode_excluded_and_unique_real_modes():
    modes = probe.fourier_modes(1, 2)
    assert len(modes) == 6
    assert not any((m == 0).all() for m in modes)
    mode_set = set(map(tuple, modes))
    assert not any(tuple(-m) in mode_set for m in modes)
    with pytest.raises(ValueError):
        probe.fourier_modes(0, 1)


@pytest.mark.parametrize("band", ["smooth", "fine"])
def test_analytic_unit_variance_and_continuous_mean_without_sensor_normalization(band):
    config = small_config()
    bank = probe.make_field_bank(band, config)
    np.testing.assert_allclose(bank.analytic_variance, 1, atol=5e-16)
    # A torus quadrature resolving every integer mode verifies the algebra.
    axis = np.arange(16)*config["L"]/16
    grid = np.asarray([(a, b) for a in axis for b in axis])
    values = bank.evaluate(grid)
    np.testing.assert_allclose(values.mean(axis=-1), 0, atol=1e-15)
    np.testing.assert_allclose(np.mean(values**2, axis=-1), 1, atol=2e-15)


def test_common_fields_reproduce_and_are_periodic():
    config = small_config()
    a, b = probe.make_field_bank("smooth", config), probe.make_field_bank("smooth", config)
    assert a.hashes == b.hashes
    points, _ = points_and_labels()
    np.testing.assert_allclose(a.evaluate(points), a.evaluate(points+[config["L"], -config["L"]]), atol=3e-15)
    assert a.hashes != probe.make_field_bank("fine", config).hashes


def test_shuffle_preserves_counts_and_common_targets_ignore_marks():
    config = probe.load_probe_config()
    labels = np.repeat(np.arange(5), config["counts_A_to_E"])
    shuffled = probe.probe_labels(labels, "shuffle", 1101, config)
    assert not np.array_equal(shuffled, labels)
    np.testing.assert_array_equal(np.bincount(shuffled), np.bincount(labels))
    np.testing.assert_array_equal(shuffled, probe.probe_labels(labels, "shuffle", 1101, config))
    target_before = probe.make_field_bank("smooth", config).evaluate(probe.query_sites(config))
    probe.probe_labels(labels, "shuffle", 1102, config)
    np.testing.assert_array_equal(target_before, probe.make_field_bank("smooth", config).evaluate(probe.query_sites(config)))


@pytest.mark.parametrize("estimator", ["nearest_neighbor", "local_gaussian"])
def test_weights_only_observe_their_channel_and_reproduce_constants(estimator):
    points, labels = points_and_labels()
    queries = np.asarray([[0, 0], [3.8, 3.9], [2, 2]])
    weights, report = probe.interpolation_weights(points, labels, queries, 4, estimator)
    observations = np.broadcast_to(labels+2, (8, len(labels)))
    targets = np.broadcast_to((np.arange(5)+2)[None, :, None], (8, 5, len(queries)))
    for c, w in enumerate(weights):
        np.testing.assert_allclose(w.sum(axis=1), 1)
        assert (w[:, labels != c] == 0).all()
    assert probe.score_observations(observations, weights, targets)["MSE_macro"] < 1e-29
    assert len(report["channels"]) == 5


def test_periodic_nearest_and_empty_local_fallback_are_exact():
    points, labels = points_and_labels()
    points[0] = [3.99, 0]
    queries = np.asarray([[.01, 0], [2.5, 3.3]])
    nearest, _ = probe.interpolation_weights(points, labels, queries, 4, "nearest_neighbor")
    kernel, report = probe.interpolation_weights(points, labels, queries, 4, "local_gaussian", .0001, 2)
    assert nearest[0][0, 0] == 1
    for a, b in zip(nearest, kernel):
        np.testing.assert_array_equal(a, b)
    assert report["channels"][0]["kernel_fallback_fraction"] == 1


def test_macro_score_does_not_weight_by_sensor_count():
    labels = np.asarray([0]*5+[1]*2+[2, 3, 4])
    points, _ = points_and_labels()
    queries = np.asarray([[1, 1]])
    weights, _ = probe.interpolation_weights(points, labels, queries, 4, "nearest_neighbor")
    observations = np.zeros((8, 10))
    targets = np.broadcast_to(np.arange(5)[None, :, None], (8, 5, 1))
    score = probe.score_observations(observations, weights, targets)
    assert score["MSE_macro"] == np.mean(np.arange(5)**2) == 6.0


def test_noise_common_by_node_id_not_condition_or_band():
    config = small_config()
    np.testing.assert_array_equal(probe.common_sensor_noise(1, config), probe.common_sensor_noise(1, config))
    assert not np.array_equal(probe.common_sensor_noise(1, config), probe.common_sensor_noise(2, config))


def test_run_freezes_before_score_and_is_idempotent_without_reopening(monkeypatch, tmp_path):
    config = small_config()
    points, labels = points_and_labels()
    geometry = Geometry(points, labels, config["L"], {"certificate": {"passed": True, "scientific_admissible": True}})
    path = tmp_path/"source.npz"
    geometry.save(path)
    monkeypatch.setattr(probe, "load_probe_config", lambda: config)
    monkeypatch.setattr(probe, "_load_geometry", lambda *a: (geometry, path))
    monkeypatch.setattr(probe, "_plot_results", lambda *a: None)
    score_original = probe.score_observations

    def guarded_score(*args):
        assert (tmp_path/"out/preregistration.json").exists()
        assert json.loads((tmp_path/"out/preregistration.json").read_text())["beliefs_updated"] is False
        return score_original(*args)

    monkeypatch.setattr(probe, "score_observations", guarded_score)
    result = probe.run_sampling_probe(tmp_path/"out")
    assert result["completed_cells"] == result["expected_cells"] == 16
    assert result["status"] == "COMPLETE" and result["beliefs_updated"] is False
    monkeypatch.setattr(probe, "_load_geometry", lambda *a: pytest.fail("Completed run was reopened"))
    assert probe.run_sampling_probe(tmp_path/"out") == result


def test_missing_geometries_retained_and_cannot_claim_complete(monkeypatch, tmp_path):
    config = small_config()
    monkeypatch.setattr(probe, "load_probe_config", lambda: config)
    monkeypatch.setattr(probe, "_load_geometry", lambda *a: (None, tmp_path/"missing.npz"))
    monkeypatch.setattr(probe, "_plot_results", lambda *a: None)
    result = probe.run_sampling_probe(tmp_path)
    assert result["status"] == "INCOMPLETE_MATRIX"
    assert result["positive_interpretation_eligible"] is False
    assert result["missing_geometries"][0]["geometry_seed"] == 1


def test_failed_local_control_is_kept_but_not_promoted_to_mhu(monkeypatch, tmp_path):
    config = small_config()
    config["families"] = ["avian_local_only"]
    points, labels = points_and_labels()
    geometry = Geometry(points, labels, config["L"], {"admitted": False, "certificate": {"passed": False}})
    path = tmp_path/"control.npz"
    geometry.save(path)
    monkeypatch.setattr(probe, "load_probe_config", lambda: config)
    monkeypatch.setattr(probe, "_load_geometry", lambda *a: (geometry, path))
    monkeypatch.setattr(probe, "_plot_results", lambda *a: None)
    result = probe.run_sampling_probe(tmp_path/"out")
    assert result["status"] == "COMPLETE" and result["geometries"][0]["admitted"] is False
    assert result["geometries"][0]["local_only_deliberately_not_required_to_be_MHU"] is True
