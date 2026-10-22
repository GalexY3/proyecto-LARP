"""Algorithmic controls for neutral constrained mobility; no scientific run."""
import json
import time

import numpy as np
import pytest

from larp.geometry import Geometry, array_hash
from larp.spectral_matching import DEFAULT_TOLERANCES, SpectralMatchingCache
import larp.constrained_mobility as mobility


def tiny_cache():
    points = np.array([[.25, 0], [19.75, 0], [4, 4], [6.5, 4],
                       [8, 8], [9, 8], [12, 12], [13, 12], [16, 16], [17, 16]])
    geometry = Geometry(points, np.repeat(np.arange(5), 2), 20.)
    edges = np.array([np.arange(10), np.roll(np.arange(10), 1)])
    centers = np.array([[0., 0.], [4., 4.], [6.5, 4.], [19.9, 0.]])
    return SpectralMatchingCache(geometry, edges, centers=centers, incoming_degree=1,
                                 physical_radii=np.linspace(.1, .2, 10))


@pytest.mark.parametrize("operator,size", [("swap2", 2), ("cycle3", 3)])
def test_move_conservation_inverse_transport_and_frozen_substrate(operator, size):
    cache = tiny_cache()
    labels = cache.native_labels.copy()
    original_hashes = [array_hash(a) for a in (cache.points, cache.edges, cache.physical_radii)]
    rng = np.random.default_rng(321)
    orientations = set()
    for _ in range(30):
        candidate, move = mobility.propose_candidate(cache, labels, rng, operator)
        nodes = np.array(move["node_ids"])
        orientation = move["orientation"]
        orientations.add(orientation)
        assert len(set(labels[nodes])) == size
        assert np.array_equal(np.bincount(candidate, minlength=5), cache.counts)
        assert np.count_nonzero(labels != candidate) == size == move["changed_sites"]
        assert candidate[nodes].tolist() == move["new_marks"]
        assert labels[nodes].tolist() == move["old_marks"]
        recovered = candidate.copy()
        recovered[nodes] = np.roll(candidate[nodes], -orientation)
        assert np.array_equal(recovered, labels)
        expected = cache.point_distances[nodes, np.roll(nodes, -orientation)]
        assert move["mark_transport_distances"] == expected.tolist()
        assert move["mark_transport_distance_sum"] == pytest.approx(expected.sum())
        assert move["mark_transport_distance_rms"] == pytest.approx(np.sqrt(np.mean(expected**2)))
        assert np.allclose(cache.amplitudes(candidate).sum(axis=0), cache.union_amplitude,
                           atol=2e-14, rtol=1e-14)
        assert [array_hash(a) for a in (cache.points, cache.edges, cache.physical_radii)] == original_hashes
        labels = candidate
    if operator == "cycle3":
        assert orientations == {-1, 1}


@pytest.mark.parametrize("operator", ["swap2", "cycle3"])
def test_seed_reproducibility_and_nearest_anchor_rule(operator):
    cache = tiny_cache()
    first_rng, second_rng = np.random.default_rng(998), np.random.default_rng(998)
    for _ in range(20):
        candidate, move = mobility.propose_candidate(cache, cache.native_labels, first_rng,
                                                     operator, near_probability=1, nearest_count=1)
        other, other_move = mobility.propose_candidate(cache, cache.native_labels, second_rng,
                                                       operator, near_probability=1, nearest_count=1)
        assert np.array_equal(candidate, other)
        assert move == other_move
        assert move["near"]
        anchor = move["node_ids"][0]
        for node in move["node_ids"][1:]:
            eligible = np.flatnonzero(cache.native_labels == cache.native_labels[node])
            order = np.lexsort((eligible, cache.point_distances[anchor, eligible]))
            assert node == eligible[order[0]]


def test_complete_stable_schema_and_full_evaluator(monkeypatch):
    cache = tiny_cache()
    calls = []
    original = cache.local_features
    def full_only(labels, **kwargs):
        calls.append(kwargs)
        return original(labels, **kwargs)
    monkeypatch.setattr(cache, "local_features", full_only)
    native = mobility.evaluate_candidate(cache, cache.native_labels)
    candidate, _ = mobility.propose_candidate(cache, cache.native_labels,
                                             np.random.default_rng(30), "cycle3")
    changed = mobility.evaluate_candidate(cache, candidate)
    assert calls == [{}, {}]
    assert native["constraint_count"] == 130
    assert len(native["residuals"]) == 130
    assert all(item["ratio"] == 0 for item in native["residuals"])
    assert len(set(item["id"] for item in native["residuals"])) == 130
    assert mobility.constraint_schema(native) == mobility.constraint_schema(changed)
    assert sum(item["name"] == "exact_window_variance_relative_difference"
               for item in native["residuals"]) == 10


def test_complete_chain_reproducibility_and_replay(tmp_path):
    cache = tiny_cache()
    tolerances = {key: 10**6 for key in DEFAULT_TOLERANCES}
    results, logs = [], []
    for index in range(2):
        output = tmp_path / f"repro_{index}.jsonl"
        results.append(mobility.run_chain(
            cache, operator="cycle3", seed_keys=(19, 21), proposals=8,
            deadline_ns=time.perf_counter_ns() + 10**10, output_file=output,
            tolerances=tolerances, variance_guard_relative=10**6))
        logs.append([json.loads(line) for line in output.read_text().splitlines()])
    assert results[0]["final_labels"] == results[1]["final_labels"]
    assert results[0]["final_labels_hash"] == results[1]["final_labels_hash"]
    assert results[0]["rejection_counts_by_constraint"] == results[1]["rejection_counts_by_constraint"]
    for first, second in zip(*logs):
        assert {k: v for k, v in first.items() if not k.endswith("_ns")} == {
            k: v for k, v in second.items() if not k.endswith("_ns")}
    recovered = cache.native_labels.copy()
    maximum_hamming = 0
    for record in logs[0]:
        assert array_hash(recovered) == record["before_labels_hash"]
        move = record["proposal_metadata"]
        nodes = np.array(move["node_ids"])
        assert recovered[nodes].tolist() == move["old_marks"]
        candidate = recovered.copy()
        candidate[nodes] = move["new_marks"]
        assert array_hash(candidate) == record["candidate_labels_hash"]
        if record["accepted"]:
            recovered = candidate
        assert array_hash(recovered) == record["after_labels_hash"]
        maximum_hamming = max(maximum_hamming, np.count_nonzero(recovered != cache.native_labels))
    assert recovered.tolist() == results[0]["final_labels"]
    assert maximum_hamming == results[0]["maximum_hamming_from_native"]
    assert len(results[0]["native_gate"]["residuals"]) == len(results[0]["final_gate"]["residuals"]) == 130


def test_hard_rejection_preserves_state_and_records_exact_failures(tmp_path):
    cache = tiny_cache()
    result = mobility.run_chain(cache, operator="cycle3", seed_keys=(5, 9), proposals=5,
                                deadline_ns=time.perf_counter_ns() + 10**10,
                                output_file=tmp_path / "rejected.jsonl")
    records = [json.loads(line) for line in (tmp_path / "rejected.jsonl").read_text().splitlines()]
    assert result["trace_path"] == str((tmp_path / "rejected.jsonl").resolve())
    assert len(result["trace_hash"]) == 64
    assert len(records) == 5
    assert result["accepted_moves"] == 0
    assert result["final_labels_hash"] == array_hash(cache.native_labels)
    assert result["final_labels"] == cache.native_labels.tolist()
    assert result["final_hamming_from_native"] == result["maximum_hamming_from_native"] == 0
    for record in records:
        assert len(record["residuals"]) == 130
        assert not record["accepted"]
        assert record["before_labels_hash"] == record["after_labels_hash"] == result["initial_labels_hash"]
        assert record["candidate_labels_hash"] != record["after_labels_hash"]
        assert record["failed_constraint_ids"] == [r["id"] for r in record["residuals"] if not r["passed"]]
    expected_constraints = {item["id"]: sum(item["id"] in r["failed_constraint_ids"] for r in records)
                            for item in result["constraint_schema"]}
    expected_families = {family: sum(any(r["name"] == family and not r["passed"]
                                        for r in record["residuals"]) for record in records)
                         for family in result["rejection_counts_by_family"]}
    assert result["rejection_counts_by_constraint"] == expected_constraints
    assert result["rejection_counts_by_family"] == expected_families
    assert result["total_proposal_ns"] >= sum(r["proposal_elapsed_ns"] for r in records)
    json.dumps(result, allow_nan=False)


def test_neutral_acceptance_does_not_gate_spectral_diagnostic(tmp_path, monkeypatch):
    cache = tiny_cache()
    # Relax local guards only in this software test so all distinct-type moves
    # pass; inject alternating spectra to test both upward/downward acceptance.
    tolerances = {key: 10**6 for key in DEFAULT_TOLERANCES}
    original = cache.structure_factors
    calls = []
    def alternating(amplitudes):
        calls.append(1)
        return np.full_like(original(amplitudes), 10. if len(calls) % 2 else 0.)
    monkeypatch.setattr(cache, "structure_factors", alternating)
    result = mobility.run_chain(cache, operator="swap2", seed_keys=(13,), proposals=4,
                                deadline_ns=time.perf_counter_ns() + 10**10,
                                output_file=tmp_path / "neutral.jsonl", tolerances=tolerances,
                                variance_guard_relative=10**6)
    records = [json.loads(line) for line in (tmp_path / "neutral.jsonl").read_text().splitlines()]
    assert result["accepted_moves"] == 4
    assert [r["candidate_component_means"][0] for r in records] == [0., 10., 0., 10.]
    assert all(r["accepted"] and not r["failed_constraint_ids"] for r in records)
    for previous, current in zip(records, records[1:]):
        assert previous["after_labels_hash"] == current["before_labels_hash"]
    assert result["uniform_feasible_sampling_or_mixing_claimed"] is False


def test_deadline_before_draw_and_after_write(tmp_path, monkeypatch):
    cache = tiny_cache()
    result = mobility.run_chain(cache, operator="cycle3", seed_keys=(0,), proposals=3,
                                deadline_ns=time.perf_counter_ns() - 1,
                                output_file=tmp_path / "expired.jsonl")
    assert result["stop_reason"] == "DEADLINE"
    assert result["proposals"] == 0
    assert (tmp_path / "expired.jsonl").read_text() == ""
    # First draw starts at 2; evaluation completes at 3; write completes at
    # 5 >= deadline. The next draw must never occur.
    moments = iter([1, 2, 3, 5, 6])
    monkeypatch.setattr(mobility.time, "perf_counter_ns", lambda: next(moments))
    result = mobility.run_chain(cache, operator="swap2", seed_keys=(2,), proposals=3,
                                deadline_ns=4, output_file=tmp_path / "write_deadline.jsonl")
    assert result["stop_reason"] == "DEADLINE"
    assert result["proposals"] == 1
    assert len((tmp_path / "write_deadline.jsonl").read_text().splitlines()) == 1


def test_output_is_never_overwritten_and_invalid_rule_rejected(tmp_path):
    output = tmp_path / "existing.jsonl"
    output.write_text("original\n")
    cache = tiny_cache()
    with pytest.raises(FileExistsError):
        mobility.run_chain(cache, operator="swap2", seed_keys=(1,), proposals=0,
                           deadline_ns=time.perf_counter_ns() + 10**10, output_file=output)
    assert output.read_text() == "original\n"
    with pytest.raises(ValueError, match="positive"):
        mobility.evaluate_candidate(cache, cache.native_labels, variance_guard_relative=0)
    with pytest.raises(ValueError, match="Operator"):
        mobility.propose_candidate(cache, cache.native_labels, np.random.default_rng(0), "bad")
