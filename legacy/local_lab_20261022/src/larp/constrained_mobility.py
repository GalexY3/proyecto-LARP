"""Neutral, locally constrained functional-mark mobility on a fixed substrate.

Both move operators use full local-feature and Fourier recomputation. Fourier
statistics are diagnostics only; acceptance checks every local inequality.
Three-cycles conserve global component counts but do not guarantee local
compensation, uniform sampling of the feasible set, or mixing.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path
import json
import time

import numpy as np

from .artifacts import file_hash
from .geometry import array_hash
from .spectral_matching import (
    DEFAULT_TOLERANCES, SpectralMatchingCache, compare_local_features,
)

VERSION = "fixed_substrate_constrained_mobility_v1"
SCHEMA_FIELDS = ("name", "component", "radius_index", "radius", "bin_index",
                 "bin_lower", "bin_upper", "target_component", "quantile")


def _validate_proposal_rule(operator: str, near_probability: float,
                            nearest_count: int) -> int:
    if operator not in ("swap2", "cycle3"):
        raise ValueError("Operator must be swap2 or cycle3")
    if not np.isfinite(near_probability) or not 0 <= near_probability <= 1:
        raise ValueError("Near probability must be between zero and one")
    if not isinstance(nearest_count, (int, np.integer)) or nearest_count < 1:
        raise ValueError("Nearest count must be a positive integer")
    return 2 if operator == "swap2" else 3


def propose_candidate(cache: SpectralMatchingCache, labels: np.ndarray,
                      rng: np.random.Generator, operator: str, *,
                      near_probability: float = .8,
                      nearest_count: int = 4) -> tuple[np.ndarray, dict]:
    """Draw distinct types uniformly, then nodes from the same anchor rule.

The near/global Bernoulli is drawn once per proposal. All non-anchor nodes
are selected independently within their distinct types, and all distances
are periodic distances to the anchor. Distance ties use original node IDs.
"""
    size = _validate_proposal_rule(operator, near_probability, nearest_count)
    labels = cache.validate_labels(labels)
    subsets = tuple(combinations(range(5), size))
    subset = subsets[int(rng.integers(len(subsets)))]
    components = rng.permutation(subset)
    anchor = int(rng.choice(np.flatnonzero(labels == components[0])))
    near = bool(rng.random() < near_probability)
    nodes = [anchor]
    for component in components[1:]:
        eligible = np.flatnonzero(labels == component)
        if near:
            order = np.lexsort((eligible, cache.point_distances[anchor, eligible]))
            eligible = eligible[order[:nearest_count]]
        nodes.append(int(rng.choice(eligible)))
    orientation = int(rng.choice((-1, 1))) if size == 3 else 1
    node_ids = np.asarray(nodes, dtype=np.int64)
    old = labels[node_ids].copy()
    new = np.roll(old, orientation)
    candidate = labels.copy()
    candidate[node_ids] = new
    # A positive roll sends the old mark at index i to index i+1.
    destinations = np.roll(node_ids, -orientation)
    transport = cache.point_distances[node_ids, destinations]
    return candidate, {
        "operator": operator, "selected_components": components.tolist(),
        "node_ids": nodes, "old_marks": old.tolist(), "new_marks": new.tolist(),
        "anchor_node": anchor, "near": near, "orientation": orientation,
        "changed_sites": int(np.count_nonzero(candidate != labels)),
        "mark_transport_distances": transport.tolist(),
        "mark_transport_distance_sum": float(transport.sum()),
        "mark_transport_distance_rms": float(np.sqrt(np.mean(transport**2))),
    }


def _constraint_id(residual: dict) -> str:
    dimensions = ("component", "radius_index", "bin_index", "target_component", "quantile")
    return residual["name"] + "|" + "|".join(
        f"{key}={residual[key]}" for key in dimensions if key in residual)


def evaluate_candidate(cache: SpectralMatchingCache, candidate: np.ndarray,
                       tolerances: dict | None = None, *,
                       variance_guard_relative: float = .05) -> dict:
    """Fully recompute the local gate, retaining every residual and spectrum.

The frozen two radii/five pair bins produce 130 local inequalities when the
exact variance guard is active. No spectrum, objective or task score gates.
"""
    if not np.isfinite(variance_guard_relative) or variance_guard_relative <= 0:
        raise ValueError("The exact variance relative guard must be positive")
    candidate = cache.validate_labels(candidate)
    features = cache.local_features(candidate)
    local = compare_local_features(
        cache.native_features, features,
        tolerances=dict(DEFAULT_TOLERANCES if tolerances is None else tolerances),
        incoming_degree=cache.incoming_degree,
        variance_guard_relative=variance_guard_relative)
    for residual in local["residuals"]:
        residual["id"] = _constraint_id(residual)
        if "radius_index" in residual:
            residual["radius"] = float(cache.local_radii[residual["radius_index"]])
        if "bin_index" in residual:
            index = residual["bin_index"]
            residual["bin_lower"] = float(cache.pair_bins[index])
            residual["bin_upper"] = float(cache.pair_bins[index + 1])
    structure = cache.structure_factors(cache.amplitudes(candidate))
    if not np.isfinite(structure).all():
        raise ValueError("Spectral diagnostics must be finite")
    return {
        **local, "labels_hash": features.labels_hash,
        "variance_guard_relative": float(variance_guard_relative),
        "constraint_count": len(local["residuals"]),
        "component_means": structure.mean(axis=1).tolist(),
        "component_maxima": structure.max(axis=1).tolist(),
        "accepted_by_local_gate": bool(local["local_matching_passed"]),
        "spectral_diagnostics_only": True,
        "full_local_recomputation": True, "full_amplitude_recomputation": True,
    }


def constraint_schema(gate: dict) -> list[dict]:
    """Return ordered identities whose fields never depend on candidate values."""
    schema = [{"id": residual.get("id", _constraint_id(residual)),
               **{key: residual.get(key) for key in SCHEMA_FIELDS},
               "tolerance": residual["tolerance"]}
              for residual in gate["residuals"]]
    if len({entry["id"] for entry in schema}) != len(schema):
        raise ValueError("Constraint identifiers must be unique")
    return schema


def run_chain(cache: SpectralMatchingCache, *, operator: str,
              seed_keys: tuple[int, ...], proposals: int,
              deadline_ns: int, output_file: str | Path,
              tolerances: dict | None = None,
              variance_guard_relative: float = .05,
              near_probability: float = .8, nearest_count: int = 4) -> dict:
    """Start at native marks and accept iff all exact local inequalities pass.

The trace records each candidate, including hard rejections. Family counts
count proposals failing at least one inequality in that family, rather than
adding correlated co-failures. No stationary distribution is claimed.
Per-record proposal timings stop before writing that record; total proposal
cost includes serialization, writing and flushing, and the deadline is checked
again after those operations. The caller also enforces an external deadline.
"""
    _validate_proposal_rule(operator, near_probability, nearest_count)
    if not isinstance(proposals, (int, np.integer)) or proposals < 0:
        raise ValueError("Proposals must be a nonnegative integer")
    if not isinstance(deadline_ns, (int, np.integer)):
        raise ValueError("Deadline must be an absolute perf_counter_ns integer")
    started_ns = time.perf_counter_ns()
    rng = np.random.default_rng(np.random.SeedSequence(seed_keys))
    labels = np.array(cache.native_labels, dtype=np.int64, copy=True)
    native_hash = array_hash(labels)
    current_gate = evaluate_candidate(cache, labels, tolerances,
                                      variance_guard_relative=variance_guard_relative)
    if not current_gate["local_matching_passed"]:
        raise RuntimeError("Native marks must pass their own local gate")
    native_gate = current_gate
    schema = constraint_schema(current_gate)
    by_constraint = {entry["id"]: 0 for entry in schema}
    by_family = {entry["name"]: 0 for entry in schema}
    initial_means = current_gate["component_means"]
    visited = {native_hash}
    performed = 0
    accepted_count = total_proposal_ns = maximum_hamming = maximum_proposed_hamming = 0
    stop_reason = "PROPOSAL_LIMIT"
    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        for proposal_index in range(1, proposals + 1):
            proposal_started_ns = time.perf_counter_ns()
            if proposal_started_ns >= deadline_ns:
                stop_reason = "DEADLINE"
                break
            before_hash = array_hash(labels)
            candidate, move = propose_candidate(
                cache, labels, rng, operator, near_probability=near_probability,
                nearest_count=nearest_count)
            gate = evaluate_candidate(cache, candidate, tolerances,
                                      variance_guard_relative=variance_guard_relative)
            if constraint_schema(gate) != schema:
                raise RuntimeError("Local constraint schema changed during the chain")
            accepted = bool(gate["local_matching_passed"])
            failed = [residual for residual in gate["residuals"] if not residual["passed"]]
            for residual in failed:
                by_constraint[residual["id"]] += 1
            failed_families = sorted({residual["name"] for residual in failed})
            for family in failed_families:
                by_family[family] += 1
            candidate_hamming = int(np.count_nonzero(candidate != cache.native_labels))
            maximum_proposed_hamming = max(maximum_proposed_hamming, candidate_hamming)
            if accepted:
                labels = candidate
                current_gate = gate
                accepted_count += 1
                visited.add(gate["labels_hash"])
            hamming = int(np.count_nonzero(labels != cache.native_labels))
            maximum_hamming = max(maximum_hamming, hamming)
            measured_ns = time.perf_counter_ns()
            record = {
                "proposal": proposal_index, "proposal_metadata": move,
                "accepted": accepted, "before_labels_hash": before_hash,
                "candidate_labels_hash": gate["labels_hash"],
                "after_labels_hash": array_hash(labels),
                "candidate_component_means": gate["component_means"],
                "accepted_current_component_means": current_gate["component_means"],
                "residuals": gate["residuals"],
                "failed_constraint_ids": [residual["id"] for residual in failed],
                "failed_families": failed_families,
                "local_matching_passed": accepted,
                "maximum_constraint_ratio": gate["maximum_ratio"],
                "changed_sites": move["changed_sites"],
                "candidate_hamming_from_native": candidate_hamming,
                "hamming_from_native": hamming,
                "elapsed_ns": measured_ns - started_ns,
                "proposal_elapsed_ns": measured_ns - proposal_started_ns,
            }
            stream.write(json.dumps(record, allow_nan=False, separators=(",", ":")) + "\n")
            stream.flush()
            completed_ns = time.perf_counter_ns()
            total_proposal_ns += completed_ns - proposal_started_ns
            performed += 1
            if completed_ns >= deadline_ns:
                stop_reason = "DEADLINE"
                break
    trace_hash = file_hash(output)
    ended_ns = time.perf_counter_ns()
    if ended_ns >= deadline_ns:
        stop_reason = "DEADLINE"
    return {
        "version": VERSION, "operator": operator, "seed_keys": list(seed_keys),
        "requested_proposals": int(proposals), "proposals": performed,
        "stop_reason": stop_reason, "accepted_moves": accepted_count,
        "rejected_moves": performed - accepted_count,
        "initial_labels_hash": native_hash, "final_labels_hash": array_hash(labels),
        "final_labels": labels.tolist(), "initial_component_means": initial_means,
        "final_component_means": current_gate["component_means"],
        "maximum_hamming_from_native": maximum_hamming,
        "maximum_proposed_hamming_from_native": maximum_proposed_hamming,
        "final_hamming_from_native": int(np.count_nonzero(labels != cache.native_labels)),
        "unique_visited_accepted_hashes": sorted(visited),
        "unique_visited_accepted_state_count": len(visited),
        "total_proposal_ns": total_proposal_ns,
        "elapsed_ns": ended_ns - started_ns, "deadline_ns": int(deadline_ns),
        "constraint_schema": schema, "rejection_counts_by_constraint": by_constraint,
        "rejection_counts_by_family": by_family,
        "native_gate": native_gate, "final_gate": current_gate,
        "trace_path": str(output.resolve()), "trace_hash": trace_hash,
        "output_file": str(output.resolve()), "spectral_diagnostics_only": True,
        "neural_or_field_scores_used": False,
        "full_recomputation_for_both_operators": True,
        "variance_guard_relative": float(variance_guard_relative),
        "near_probability": float(near_probability), "nearest_count": int(nearest_count),
        "uniform_feasible_sampling_or_mixing_claimed": False,
        "family_counts_are_cofailure_diagnostics_not_independent_evidence": True,
        "total_proposal_cost_includes_jsonl_write": True,
    }
