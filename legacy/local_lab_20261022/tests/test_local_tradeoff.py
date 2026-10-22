"""Differential cached objective checks using only a synthetic substrate."""
import importlib.util
from pathlib import Path
import sys
import numpy as np
from larp.geometry import Geometry
from larp.spectral_matching import SpectralMatchingCache

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("tradeoff_worker_test", ROOT / "artifacts/local_tradeoff/worker.py")
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)


def toy():
    rng = np.random.default_rng(56473)
    points, labels = rng.uniform(0, 20, (20, 2)), np.repeat(np.arange(5), 4)
    edges = np.array([(int((j - d) % 20), j) for j in range(20) for d in range(1, 7)]).T
    centers = rng.uniform(0, 20, (50, 2))
    return SpectralMatchingCache(Geometry(points, labels, 20.), edges, centers=centers,
                                 optimized_modes=np.array([[1, 0], [0, 1], [1, 1], [1, -1], [2, 0], [0, 2]]))


def test_cached_coverage_and_swap_fourier_equal_full_recomputation_after_walk():
    cache = toy()
    labels = cache.native_labels.copy()
    covers, amplitudes = worker.initial_state(cache, labels)
    rng = np.random.default_rng(673)
    for index in range(15):
        candidate, cc, aa, nodes = worker.proposal(cache, labels, covers, amplitudes, rng)
        full_covers, full_amplitudes = worker.initial_state(cache, candidate)
        assert np.array_equal(np.bincount(candidate, minlength=5), cache.counts)
        assert np.allclose(cc, full_covers, rtol=0, atol=1e-14)
        assert np.allclose(aa, full_amplitudes, rtol=0, atol=4e-14)
        for weight in (0., .5, 1.):
            assert np.allclose(worker.score(cc, aa, cache.counts, weight), worker.score(full_covers, full_amplitudes, cache.counts, weight), rtol=0, atol=1e-13)
        if index % 2:
            labels, covers, amplitudes = candidate, cc, aa


def test_zero_and_one_priorities_select_distinct_scientific_objectives():
    counts = np.ones(5, int) * 4
    covers = np.array([.7, .8, .9, .6, .5])
    amplitudes = np.ones((5, 6), complex) * 2
    assert worker.score(covers, amplitudes, counts, 0.) == (.9, .9, 1.)
    assert worker.score(covers, amplitudes, counts, 1.) == (1., .9, 1.)


def test_supervisor_checks_completed_phase_deadline_even_with_ready_end(tmp_path):
    import pytest
    from bounded_v2 import publish, validate_phases
    publish(tmp_path / "phase_start_0.json", {"deadline_ns": 1000})
    publish(tmp_path / "phase_end_0.json", {"completed_ns": 1000})
    with pytest.raises(TimeoutError):
        validate_phases(tmp_path)


def test_supervisor_requires_closed_phase_and_accepts_timely_close(tmp_path):
    import pytest
    from bounded_v2 import publish, validate_phases
    publish(tmp_path / "phase_start_0.json", {"deadline_ns": 1000})
    with pytest.raises(RuntimeError):
        validate_phases(tmp_path)
    publish(tmp_path / "phase_end_0.json", {"completed_ns": 999})
    assert validate_phases(tmp_path) == 1
