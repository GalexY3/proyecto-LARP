"""Frozen-checkpoint lesions (contract K): explicit masks, never reconnection.

Protection is example-specific. Every quantity removed is measured relative to
the original N/E, unless an explicit per-type fraction is requested. Unavailable
levels are reported rather than supplemented with another resource class.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

from .data import (FILL_PROBABILITIES, canonical_task, evaluate_task,
                   minimum_image_displacements, register_ports)


NODE_FRACTIONS = (0.0, 0.05, 0.10, 0.20)
EDGE_FRACTIONS = (0.0, 0.05, 0.10, 0.20, 0.40)
RADII = (1.0, 2.0, 3.0, 4.0)
TYPE_ABSOLUTE_COUNTS_400 = (4, 8, 16)
TYPE_FRACTIONS = (0.25, 0.50, 0.75)
RELOCATION_OFFSETS = ((0.5, 0.0), (0.0, 0.5), (0.5, 0.5))


@dataclass(frozen=True)
class NodeMask:
    alive: np.ndarray
    removed: np.ndarray
    available: bool
    metadata: dict

    @property
    def digest(self) -> str:
        return hashlib.sha256(np.ascontiguousarray(self.alive).tobytes()).hexdigest()


@dataclass(frozen=True)
class EdgeMask:
    edge_alive: np.ndarray
    available: bool
    metadata: dict


def _protected_array(protected, n: int) -> np.ndarray:
    mask = np.zeros(n, dtype=bool)
    if protected is not None:
        values = np.asarray(protected)
        if values.dtype == bool:
            if values.shape != (n,):
                raise ValueError("Boolean protected mask must be [N]")
            mask = values.copy()
        else:
            mask[np.asarray(values, dtype=np.int64)] = True
    return mask


def build_node_mask(positions: np.ndarray, *, mode: str = "random", q: float = 0.0,
                    L: float = 20.0, seed: int = 0, protected=None,
                    center=None, radius: float | None = None, labels=None,
                    type_id: int | None = None, count: int | None = None,
                    fraction: float | None = None) -> NodeMask:
    """Build a single mask; active ports are protected only when passed explicitly.

    Modes: random, localized (exact count nearest center), disk (fixed radius),
    type (absolute count or eligible-type fraction). ``q*N`` always uses original N.
    """
    positions = np.asarray(positions, dtype=np.float64)
    n = len(positions)
    if positions.shape != (n, 2) or not 0 <= q <= 1:
        raise ValueError("2D positions and q in [0,1] required")
    protection = _protected_array(protected, n)
    eligible = np.flatnonzero(~protection)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 801]))
    distances = None
    requested = int(round(q * n)) if count is None else int(count)
    if requested < 0:
        raise ValueError("negative removal count")
    if mode in {"localized", "disk"}:
        if center is None:
            raise ValueError("localized lesions require a preregistered physical center")
        distances = np.linalg.norm(minimum_image_displacements(np.asarray(center), positions, L), axis=1)
    if mode == "type":
        labels = np.asarray(labels)
        if labels.shape != (n,) or type_id not in range(5):
            raise ValueError("type lesion requires labels[N] and a type_id 0..4")
        eligible = eligible[labels[eligible] == type_id]
        if fraction is not None:
            if not 0 <= fraction <= 1:
                raise ValueError("type fraction in [0,1] required")
            requested = int(round(fraction * len(eligible)))
        elif count is None:
            raise ValueError("absolute type lesion requires count")
    elif mode == "disk":
        if radius is None or radius < 0:
            raise ValueError("fixed-radius lesion requires a nonnegative radius")
        eligible_in_disk = eligible[distances[eligible] <= radius]
        requested = len(eligible_in_disk)
    elif mode not in {"random", "localized"}:
        raise ValueError("unknown node-removal mode")
    metadata = {"mode": mode, "seed": int(seed), "N": n, "q": float(q),
                "requested_count": requested, "eligible_count": len(eligible),
                "protected_count": int(protection.sum()), "type_id": type_id,
                "center": np.asarray(center).tolist() if center is not None else None,
                "fixed_radius": radius, "per_type_fraction": fraction,
                "reconnect": False}
    if requested > len(eligible):
        metadata.update(reason="insufficient_eligible_nodes", removed_count=0)
        return NodeMask(np.ones(n, dtype=bool), np.empty(0, dtype=np.int64), False, metadata)
    if mode == "localized":
        order = np.lexsort((eligible, distances[eligible]))
        removed = eligible[order[:requested]]
    elif mode == "disk":
        removed = eligible_in_disk
    else:
        # Common rank per node, then filter protected/class nodes. Thus the random
        # mask stream is shared across examples and native/shuffle where eligible.
        rank = rng.permutation(n)
        selected_eligible = np.zeros(n, dtype=bool)
        selected_eligible[eligible] = True
        removed = rank[selected_eligible[rank]][:requested]
    alive = np.ones(n, dtype=bool)
    alive[removed] = False
    metadata.update(removed_count=len(removed), removed_fraction=len(removed) / n,
                    result_radius=float(distances[removed].max()) if distances is not None and len(removed) else 0.0)
    if labels is not None:
        labels = np.asarray(labels, dtype=np.int64)
        metadata["removed_by_type"] = np.bincount(labels[removed], minlength=5).tolist()
    return NodeMask(alive, np.asarray(removed, dtype=np.int64), True, metadata)


def build_batch_masks(positions: np.ndarray, active_nodes: np.ndarray, *,
                      protect_ports: bool = True, **kwargs) -> tuple[np.ndarray, list[dict]]:
    active_nodes = np.asarray(active_nodes, dtype=bool)
    if active_nodes.ndim != 2 or active_nodes.shape[1] != len(positions):
        raise ValueError("active_nodes must be [B,N]")
    masks = [build_node_mask(positions, protected=row if protect_ports else None, **kwargs)
             for row in active_nodes]
    return np.stack([mask.alive for mask in masks]), [dict(mask.metadata, available=mask.available) for mask in masks]


def build_edge_mask(edge_index: np.ndarray, *, q: float, seed: int = 0,
                    mode: str = "independent_arcs") -> EdgeMask:
    edges = np.asarray(edge_index, dtype=np.int64)
    if edges.ndim != 2 or edges.shape[0] != 2 or not 0 <= q <= 1:
        raise ValueError("edge_index[2,E] and q in [0,1] required")
    e = edges.shape[1]
    requested = int(round(q * e))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 802]))
    alive = np.ones(e, dtype=bool)
    metadata = {"q": float(q), "E": e, "requested_arcs": requested,
                "seed": int(seed), "mode": mode, "reconnect": False}
    if mode == "independent_arcs":
        removed = rng.permutation(e)[:requested]
    elif mode == "paired_undirected_edges":
        if len(set(zip(edges[0].tolist(), edges[1].tolist()))) != e:
            raise ValueError("paired edge lesion requires distinct directed arcs")
        index = {tuple(pair): slot for slot, pair in enumerate(edges.T.tolist())}
        pairs = []
        for (source, target), slot in index.items():
            if source == target or (target, source) not in index:
                raise ValueError("paired lesion requires simple bidirectional graph")
            if source < target:
                pairs.append((slot, index[(target, source)]))
        if requested % 2:
            metadata.update(reason="SCIENTIFIC_BLOCKER_exact_arc_count_is_odd_for_pair_removal", removed_arcs=0)
            return EdgeMask(alive, False, metadata)
        pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
        removed = pairs[rng.permutation(len(pairs))[:requested // 2]].ravel()
    else:
        raise ValueError("unknown arc-removal mode")
    alive[removed] = False
    metadata["removed_arcs"] = int(np.count_nonzero(~alive))
    return EdgeMask(alive, True, metadata)


def preregistered_centers(L: float = 20, seed: int = 0, count: int = 20) -> np.ndarray:
    return np.random.default_rng(np.random.SeedSequence([int(seed), 803])).uniform(0, L, (count, 2))


def fixed_test_indices(dataset_size: int, count: int = 512, key: int = 804) -> np.ndarray:
    """Choose by deterministic hash before predictions; no score-dependent choice."""
    if count > dataset_size:
        raise ValueError("cannot select more examples than exist")
    order = sorted(range(dataset_size), key=lambda i: hashlib.sha256(f"{key}:{i}".encode()).digest())
    return np.asarray(order[:count], dtype=np.int64)


def normalized_damage_auc(q, scores) -> float:
    q, scores = np.asarray(q, dtype=np.float64), np.asarray(scores, dtype=np.float64)
    if q.shape != scores.shape or q.ndim != 1 or len(q) < 2 or np.any(np.diff(q) <= 0):
        raise ValueError("strictly increasing q and one score per q required")
    if not np.isclose(q[0], 0) or not np.isclose(q[-1], 0.20):
        raise ValueError("primary damage AUC is restricted to q=0..0.20")
    return float(np.trapezoid(scores, q) / 0.20)


def output_preservation(alive: np.ndarray, output_nodes: np.ndarray,
                        essential_source_nodes: np.ndarray | None = None) -> dict:
    """Masks for K7 system failure vs processing conditional on intact I/O."""
    alive = np.asarray(alive, dtype=bool)
    output_nodes = np.asarray(output_nodes, dtype=np.int64)
    if alive.ndim == 1:
        alive = np.broadcast_to(alive, (output_nodes.shape[0], len(alive)))
    rows = np.arange(len(alive))[:, None]
    output_intact = alive[rows, output_nodes]
    essential_intact = np.ones(len(alive), dtype=bool)
    if essential_source_nodes is not None:
        nodes = np.asarray(essential_source_nodes, dtype=np.int64).reshape(len(alive), -1)
        essential_intact = alive[rows, nodes].all(axis=1)
    return {"output_node_intact": output_intact,
            "all_outputs_intact": output_intact.all(axis=1),
            "essential_inputs_intact": essential_intact,
            "processing_eligible": output_intact.all(axis=1) & essential_intact}


def relocated_ports(positions, *, L: float = 20, world_side: int = 10,
                    offset=(0.5, 0.0)):
    """Whole-system K6 relocation; task worlds and targets are unchanged."""
    return register_ports(positions, L, world_side, offset)


def _numpy(value):
    return value.detach().cpu().numpy() if hasattr(value, "detach") else np.asarray(value)


def evaluate_damaged_predictions(task, logits, target, alive, output_nodes,
                                 required_source_nodes, free=None, p=None) -> dict:
    """Separate K7 system failures and processing conditional on intact I/O.

    All required outputs and essential inputs must survive for an example's
    system contribution to be its task score; otherwise its contribution is 0.
    Removed-output placeholders never enter a prediction/loss computation.
    Fill performs the preregistered per-map → per-p → equal-p aggregation.
    For copy pass only selected_source_nodes, XOR both source_nodes, fill seed.
    Masks [B,N] must be aligned with the predictions' selected example order.
    """
    task = canonical_task(task)
    if task == "resource":
        raise ValueError("SCIENTIFIC_BLOCKER_resource_end_to_end_failure_score_not_preregistered")
    logits, target = _numpy(logits), _numpy(target)
    alive, nodes = _numpy(alive).astype(bool), _numpy(output_nodes).astype(np.int64)
    if logits.shape != target.shape or logits.shape[:2] != nodes.shape:
        raise ValueError("logits/targets[B,P,o] and output_nodes[B,P] required")
    if alive.ndim == 2 and alive.shape[0] != len(logits):
        raise ValueError("alive[B,N] must align with selected examples")
    source = None if required_source_nodes is None else _numpy(required_source_nodes)
    flags = output_preservation(alive, nodes, source)
    eligible = flags["processing_eligible"]
    free_array = None if free is None else _numpy(free)
    probability = None if p is None else _numpy(p).reshape(-1)
    processing = None
    per_example = np.zeros(len(logits), dtype=np.float64)
    exact_per_example = np.zeros(len(logits), dtype=np.float64)
    if eligible.any():
        processing = evaluate_task(task, logits[eligible], target[eligible],
                                   free=None if free_array is None else free_array[eligible],
                                   p=None if probability is None else probability[eligible])
        if not processing.get("divergent", False):
            if task == "fill":
                per_example[eligible] = processing["BA_per_map"]
            else:
                correct = (logits[eligible] >= 0) == target[eligible].astype(bool)
                per_example[eligible] = correct.mean(axis=tuple(range(1, correct.ndim)))
                exact_per_example[eligible] = correct.all(axis=tuple(range(1, correct.ndim)))
    if task == "fill":
        if free_array is None or probability is None:
            raise ValueError("fill damage evaluation requires free masks and p")
        by_factor = {f"{factor:.2f}": float(per_example[np.isclose(probability, factor, rtol=0, atol=1e-12)].mean())
                     for factor in FILL_PROBABILITIES
                     if np.isclose(probability, factor, rtol=0, atol=1e-12).any()}
        if not by_factor:
            raise ValueError("no known fill probability factors")
        system_score = float(np.mean(list(by_factor.values())))
    else:
        by_factor = None
        system_score = float(per_example.mean())
    result = {"score": system_score, "system_score": system_score,
              "system_score_per_example": per_example.tolist(),
              "system_failure_fraction": float(np.mean(~eligible)),
              "processing_metrics": processing,
              "processing_score": None if processing is None else processing["score"],
              "loss": None if processing is None else processing["loss"],
              "processing_example_count": int(eligible.sum()),
              "output_present_fraction": float(flags["output_node_intact"].mean()),
              "output_complete_fraction": float(flags["all_outputs_intact"].mean()),
              "essential_inputs_complete_fraction": float(flags["essential_inputs_intact"].mean()),
              "processing_condition": "all_essential_inputs_and_all_outputs_alive"}
    if by_factor is not None:
        result["system_BA_by_p"] = by_factor
    else:
        result["system_exact_accuracy"] = float(exact_per_example.mean())
    return result
