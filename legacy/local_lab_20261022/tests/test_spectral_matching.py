"""Independent invariants for periodic mark matching, not neural benchmarks."""
import numpy as np
import pytest
from dataclasses import replace
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from larp.geometry import Geometry, integer_modes, structure_factors
from larp.spectral_matching import (
    SpectralMatchingCache, empirical_cdf_distance, integer_count_tolerance,
    compare_local_features, spectral_metrics, matching_energy,
    bounded_swap_search, admission, DEFAULT_TOLERANCES,
    exact_disc_window_variance, spectral_disc_variance_lower_bound,
)


def tiny_cache():
    # The A pair crosses the x boundary: periodic separation .5, not 19.5.
    # B is exactly at the final histogram edge 2.5. Each node has in-degree1.
    points = np.array([[.25, 0], [19.75, 0], [4, 4], [6.5, 4],
                       [8, 8], [9, 8], [12, 12], [13, 12], [16, 16], [17, 16]])
    labels = np.repeat(np.arange(5), 2)
    geometry = Geometry(points, labels, 20.)
    edges = np.array([np.arange(10), np.roll(np.arange(10), 1)])
    centers = np.array([[0., 0.], [4., 4.], [6.5, 4.], [19.9, 0.]])
    return SpectralMatchingCache(geometry, edges, centers=centers, incoming_degree=1)


def test_right_continuous_cdf_ties_and_exact_admission_boundary():
    assert empirical_cdf_distance([0, 0, 2], [0, 1, 1]) == pytest.approx(1 / 3)
    assert empirical_cdf_distance([0, 0], [0, 0]) == 0
    reference = np.zeros(10000, dtype=int)
    exactly = reference.copy()
    exactly[:200] = 1
    outside = reference.copy()
    outside[:201] = 1
    assert empirical_cdf_distance(reference, exactly) == .02
    assert empirical_cdf_distance(reference, exactly) <= DEFAULT_TOLERANCES["coverage_cdf"]
    assert empirical_cdf_distance(reference, outside) > DEFAULT_TOLERANCES["coverage_cdf"]
    with pytest.raises(ValueError, match="nonempty"):
        empirical_cdf_distance([], [1])


def test_periodic_coverage_homotypic_nearest_and_histogram_edges():
    cache = tiny_cache()
    a, b = cache.native_features.type_features[:2]
    assert np.allclose(a.homotypic_nearest, .5)
    assert a.coverage[0] == pytest.approx(.25)
    # np.histogram has [a,b) bins except last closed; no self-pairs, no doubling.
    assert a.physical_pair_histogram.tolist() == [0, 1, 0, 0, 0]
    assert b.physical_pair_histogram.tolist() == [0, 0, 0, 0, 1]
    assert int(a.physical_pair_histogram.sum()) == 1
    # Radius 2.5 includes the boundary B node, exactly.
    assert b.window_counts[1][1] == 2


def test_directed_type_matrix_has_source_rows_and_target_columns():
    cache = tiny_cache()
    expected = np.zeros((5, 5), dtype=int)
    for source, target in cache.edges.T:
        expected[cache.native_labels[source], cache.native_labels[target]] += 1
    counts = cache.directed_arc_counts(cache.native_labels)
    assert np.array_equal(counts, expected)
    assert not np.array_equal(counts, counts.T)
    assert counts.sum() == cache.edges.shape[1]
    for component in range(5):
        assert cache.native_features.type_features[component].outdegree_mean == pytest.approx(1)


def test_integer_tolerances_are_absolute_for_rare_empty_bins():
    assert integer_count_tolerance(0) == 2
    assert integer_count_tolerance(19) == 2
    assert integer_count_tolerance(20) == 2
    assert integer_count_tolerance(100) == 5
    assert integer_count_tolerance(101) == 6


def test_native_self_match_has_all_zero_residuals_and_labels_are_not_coerced():
    cache = tiny_cache()
    gate = compare_local_features(cache.native_features, cache.local_features(cache.native_labels), incoming_degree=1)
    assert gate["local_matching_passed"]
    assert gate["maximum_ratio"] == 0
    assert len(gate["residuals"]) == 120  # 19 per component plus 25 directed cells.
    assert all(residual["value"] == 0 for residual in gate["residuals"])
    with pytest.raises(ValueError, match="integer"):
        cache.local_features(cache.native_labels.astype(float))
    bad = cache.native_labels.copy()
    bad[0] = 1
    with pytest.raises(ValueError, match="preserve"):
        cache.local_features(bad)
    with pytest.raises(ValueError):
        cache.centers.setflags(write=True)


def test_incremental_swap_matches_full_metrics_and_does_not_change_union():
    cache = tiny_cache()
    labels = cache.native_labels.copy()
    amplitudes = cache.amplitudes(labels)
    features = cache.native_features
    rng = np.random.default_rng(50)
    for _ in range(40):
        first, second = rng.choice(cache.N, 2, replace=False)
        changed = (int(labels[first]), int(labels[second]))
        next_rho = cache.swapped_amplitudes(amplitudes, labels, int(first), int(second))
        candidate = labels.copy()
        candidate[first], candidate[second] = candidate[second], candidate[first]
        incremental = cache.local_features(candidate, previous=features, changed_types=changed)
        full = cache.local_features(candidate)
        assert compare_local_features(full, incremental, incoming_degree=1)["maximum_ratio"] == 0
        assert np.allclose(next_rho, cache.amplitudes(candidate), atol=2e-14, rtol=1e-14)
        assert np.allclose(next_rho.sum(axis=0), cache.union_amplitude, atol=2e-14, rtol=1e-14)
        labels, amplitudes, features = candidate, next_rho, incremental
    expected = structure_factors(cache.points, labels, cache.L)
    assert np.allclose(cache.structure_factors(amplitudes), expected[:5])
    assert np.array_equal(integer_modes(20), cache.modes)


def test_incremental_update_rejects_omitted_changed_type():
    cache = tiny_cache()
    labels = cache.native_labels.copy()
    labels[0], labels[2] = labels[2], labels[0]
    with pytest.raises(ValueError, match="omitted"):
        cache.local_features(labels, previous=cache.native_features, changed_types=(0,))


def test_concentration_sum_cross_hermitian_and_normalizations():
    cache = tiny_cache()
    rho = cache.amplitudes(cache.native_labels)
    metrics = spectral_metrics(rho, cache.union_amplitude, cache.counts, cache.modes)
    eta = np.array(metrics["concentration_eta_real"]) + 1j * np.array(metrics["concentration_eta_imag"])
    assert np.allclose(eta.sum(axis=0), 0, atol=1e-14)
    cross = np.array(metrics["component_cross_mode_mean_real"]) + 1j * np.array(metrics["component_cross_mode_mean_imag"])
    assert np.allclose(cross, cross.conj().T)
    assert np.linalg.eigvalsh(cross).min() >= -1e-12
    assert np.allclose(cross.diagonal().real, metrics["component_means"])
    expected_t = np.abs(eta)**2 / (cache.counts[:, None] * (1 - cache.counts[:, None] / cache.N))
    assert np.allclose(expected_t, metrics["concentration_structure_factors"])


def test_search_energy_uses_sums_and_every_constraint_still_gates():
    gate = {"residuals": [{"ratio": .5}, {"ratio": 2.}, {"ratio": 3.}],
            "component_means": [0, .25, .5, .75, 1.], "spectral_target": .5}
    assert matching_energy(gate, local_weight=100, spectral_weight=1) == pytest.approx(501.25)
    with pytest.raises(ValueError):
        matching_energy(gate, local_weight=-1)


def test_bounded_failure_is_not_admitted_or_mathematical_impossibility():
    cache = tiny_cache()
    result = bounded_swap_search(cache, seed_keys=(100, 101), starts=("native", "native"),
                                 proposals_per_start=2, maximum_seconds=10,
                                 initial_temperature=.1, final_temperature=.001,
                                 local_weight=100)
    assert result["status"] == "NOT_IDENTIFIED"
    assert result["total_proposals"] == 4
    assert result["admitted_labels"] is None
    assert result["search_failure_is_not_mathematical_impossibility"]
    assert not result["neural_or_field_scores_used"]
    for attempt in result["attempts"]:
        recovered = cache.native_labels.copy()
        for move in attempt["accepted_moves"]:
            i, j = move["first"], move["second"]
            recovered[i], recovered[j] = recovered[j], recovered[i]
        assert admission(cache, recovered)["component_means"] == attempt["last_gate"]["component_means"] or np.allclose(
            admission(cache, recovered)["component_means"], attempt["last_gate"]["component_means"])


def test_descriptive_windows_do_not_enter_matching_and_radii_follow_nodes():
    cache = tiny_cache()
    marks = cache.native_labels.copy()
    marks[0], marks[2] = marks[2], marks[0]
    radii = np.linspace(.1, .2, cache.N)
    with_radii = SpectralMatchingCache(cache.geometry, cache.edges, centers=cache.centers,
                                       incoming_degree=1, physical_radii=radii)
    first_hash = with_radii.identity()["physical_radii_by_original_node_hash"]
    measured = with_radii.measure(marks)
    assert first_hash == with_radii.identity()["physical_radii_by_original_node_hash"]
    assert [window["radius"] for window in measured["descriptive_long_windows"]] == [4., 5.]
    assert with_radii.local_radii == (1.25, 2.5)
    assert measured["union_amplitude_hash"] == with_radii.measure(with_radii.native_labels)["union_amplitude_hash"]


def test_exact_disc_variance_single_sensor_and_two_disjoint_sensor_supports():
    L, radius = 20., 2.
    p = np.pi * radius**2 / L**2
    single = exact_disc_window_variance(np.array([[1., 1.]]), L, radius)
    assert single["variance"] == pytest.approx(p * (1 - p))
    disjoint = exact_disc_window_variance(np.array([[1., 1.], [11., 11.]]), L, radius)
    assert disjoint["variance"] == pytest.approx(2 * p * (1 - 2 * p))
    # Periodically adjacent disks must include the overlap across the box edge.
    wrapped = exact_disc_window_variance(np.array([[.1, 1.], [19.9, 1.]]), L, radius)
    interior = exact_disc_window_variance(np.array([[10., 1.], [10.2, 1.]]), L, radius)
    assert wrapped["variance"] == pytest.approx(interior["variance"])
    assert wrapped["variance"] > disjoint["variance"]
    with pytest.raises(ValueError, match="L/4"):
        exact_disc_window_variance(np.array([[1., 1.]]), L, 5.01)


def test_parseval_disc_bound_allows_spectral_mass_at_minimum_weight():
    modes = integer_modes(20)
    result = spectral_disc_variance_lower_bound(163, 20., 2.5, modes, .5)
    weights = np.asarray(result["normalized_disc_fourier_weights"])
    coefficient = result["parseval_coefficient_per_halfspace_mode"]
    # The allowed mean floor is compatible with zero S in five of six modes.
    concentrated = np.zeros(len(modes))
    concentrated[np.argmin(weights)] = .5 * len(modes)
    assert coefficient * np.dot(weights, concentrated) == pytest.approx(result["variance_lower_bound"])
    assert coefficient * np.dot(weights, np.full(len(modes), .5)) >= result["variance_lower_bound"]
    with pytest.raises(ValueError, match="conjugate"):
        spectral_disc_variance_lower_bound(2, 20., 2., np.array([[1, 0], [-1, 0]]), .5)


def test_void_fraction_boundary_uses_integer_counts():
    cache = tiny_cache()
    baseline = np.repeat([0, 1], 5000)
    exactly = baseline.copy()
    exactly[:200] = 1
    outside = baseline.copy()
    outside[:201] = 1
    native_type = replace(cache.native_features.type_features[0], window_counts=(baseline, baseline))
    def compare(counts):
        control_type = replace(native_type, window_counts=(counts, counts))
        native = replace(cache.native_features, type_features=(native_type,) + cache.native_features.type_features[1:])
        candidate = replace(native, type_features=(control_type,) + native.type_features[1:])
        return compare_local_features(native, candidate, incoming_degree=1)
    boundary = [r for r in compare(exactly)["residuals"] if r["name"] == "window_void_fraction" and r["component"] == 0]
    assert all(r["value"] == .02 and r["passed"] for r in boundary)
    outside_gate = [r for r in compare(outside)["residuals"] if r["name"] == "window_void_fraction" and r["component"] == 0]
    assert all(not r["passed"] for r in outside_gate)


def test_optional_continuous_variance_guard_matches_disc_integral():
    cache = tiny_cache()
    for component, local in enumerate(cache.native_features.type_features):
        exact = tuple(exact_disc_window_variance(cache.points[cache.native_labels == component], cache.L, radius)["variance"]
                      for radius in cache.local_radii)
        assert local.exact_window_variances == pytest.approx(exact)
    native = cache.native_features
    gate = compare_local_features(native, native, incoming_degree=1, variance_guard_relative=.05)
    assert gate["local_matching_passed"] and len(gate["residuals"]) == 130
    original = native.type_features[0]
    changed = replace(original, exact_window_variances=(original.exact_window_variances[0] * 1.051,
                                                       original.exact_window_variances[1]))
    candidate = replace(native, type_features=(changed,) + native.type_features[1:])
    assert compare_local_features(native, candidate, incoming_degree=1)["local_matching_passed"]
    guarded = compare_local_features(native, candidate, incoming_degree=1, variance_guard_relative=.05)
    assert not guarded["local_matching_passed"]
    failed = [r for r in guarded["residuals"] if not r["passed"]]
    assert len(failed) == 1 and failed[0]["name"] == "exact_window_variance_relative_difference"


def test_explicit_trajectory_seeds_and_best_diagnostic_are_recoverable():
    cache = tiny_cache()
    events = []
    result = bounded_swap_search(cache, seed_keys=(7,), starts=("native", "native"),
        start_seed_keys=((20261009, 8843, 1101, 0), (20261009, 8843, 1101, 1)),
        proposals_per_start=3, maximum_seconds=10, maximum_seconds_per_start=5,
        initial_temperature=.1, final_temperature=.001, local_weight=100,
        variance_guard_relative=.05,
        trajectory_callback=lambda stage, row, labels: events.append((stage, row, labels.copy())))
    assert [row[0] for row in events] == ["START", "END", "START", "END"]
    for index, labels in enumerate(result["attempt_diagnostic_labels"]):
        gate = admission(cache, labels, variance_guard_relative=.05)
        assert matching_energy(gate, local_weight=100) == pytest.approx(result["attempts"][index]["best_diagnostic"]["energy"])
        assert result["attempts"][index]["seed_keys"][-1] == index


def test_expired_absolute_deadline_records_all_unstarted_trajectories():
    cache = tiny_cache()
    result = bounded_swap_search(cache, seed_keys=(7,), starts=("native", "native"),
        proposals_per_start=3, maximum_seconds=10, absolute_deadline_ns=time.perf_counter_ns() - 1,
        initial_temperature=.1, final_temperature=.001)
    assert result["total_proposals"] == 0
    assert result["stop_reason"] == "RESOURCE_LIMIT"
    assert all(attempt["status"] == "NOT_RUN_RESOURCE_LIMIT" for attempt in result["attempts"])


def test_direct_worker_pid_and_hard_kill_before_scientific_imports(tmp_path):
    runner_path = Path(__file__).resolve().parents[1] / "artifacts/spectral_matching/run_bounded.py"
    spec = importlib.util.spec_from_file_location("spectral_bounded_runner_test", runner_path)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    env = os.environ.copy()
    env.update(__PYVENV_LAUNCHER__=sys.executable, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    proc = subprocess.Popen([sys._base_executable, "-B", str(runner_path), "--worker", "--phase", "prepare",
        "--config", str(tmp_path / "unused.json"), "--output", str(tmp_path),
        "--expected-parent", str(os.getpid()), "--deadline-ns", str(time.perf_counter_ns() + 3_000_000_000)],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    try:
        end = time.perf_counter() + 2
        while not (tmp_path / "worker_boot.json").exists() and time.perf_counter() < end:
            time.sleep(.01)
        boot = json.loads((tmp_path / "worker_boot.json").read_text(encoding="utf-8"))
        assert boot["pid"] == proc.pid and boot["ppid"] == os.getpid()
        assert boot["sys_executable"] == sys.executable and boot["sys_prefix"] == sys.prefix
        assert proc.poll() is None  # Waiting for an unopened execution gate.
        runner.terminate_tree(proc)
        assert proc.poll() is not None
        assert not (tmp_path / "worker_completion.json").exists()
    finally:
        if proc.poll() is None:
            runner.terminate_tree(proc)
