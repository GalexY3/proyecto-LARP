"""Substrates share the recurrent core; ecological comparisons are explicit."""
from pathlib import Path
import numpy as np
from .geometry import Geometry, generate_geometry, relabel_geometry
from .graphs import build_graph


def make_substrate(condition, N=400, seed=1101, *, regime="causal", cache=None):
    if condition == "nca":
        from .data import world_sites
        from .geometry import hamilton_counts
        from .graphs import grid_cardinal_graph
        geometry = Geometry(world_sites(10, 20), np.repeat(np.arange(5), hamilton_counts(100)), 20,
                            {"kind": "nca", "geometry_seed": seed, "test_only": False,
                             "claim": "ecological grid100 at exact world sites, G core"})
        unit_grid = generate_geometry(100, seed, "grid")
        return geometry, grid_cardinal_graph(unit_grid.points, unit_grid.L)
    kind = {"native": "mhu", "shuffle": "mhu", "clustered": "mhu", "matched": "mhu",
            "grid_balanced": "grid", "random_regular": "mhu", "small_world": "grid",
            "nca": "grid"}.get(condition, condition)
    if cache is not None:
        path = Path(cache) / f"{kind}_N{N}_g{seed}.npz"
        if path.exists():
            geometry = Geometry.load(path)
            if geometry.N != N or geometry.metadata["geometry_seed"] != seed or geometry.metadata["kind"] != kind:
                raise ValueError("Cached geometry identity mismatch")
        else:
            geometry = generate_geometry(N, seed, kind)
            geometry.save(path)
    else:
        geometry = generate_geometry(N, seed, kind)
    if kind in {"mhu", "hu"} and not geometry.metadata["certificate"].get("scientific_admissible"):
        raise RuntimeError("SCIENTIFIC_BLOCKER failed geometry certificate; seed is retained")
    graph_kind = {"random_regular": "random_regular", "small_world": "small_world", "nca": "cardinal"}.get(condition, "knn")
    if regime == "ecological" and graph_kind == "knn":
        graph_kind = "cardinal" if kind == "grid" else "delaunay"
    edges = build_graph(geometry, graph_kind, regime=regime, seed=seed)
    if condition in {"shuffle", "clustered", "matched", "grid_balanced", "random_regular"}:
        geometry = relabel_geometry(geometry, "shuffle" if condition=="random_regular" else condition, seed, edge_index=edges)
    return geometry, edges


def choose_baseline(records, tolerance=.005):
    """Only nominal T causal rivals, validation, identical completed budget."""
    order = ["grid_balanced", "hu", "small_world", "random_regular", "poisson"]
    candidates = {}
    for condition in order:
        rows = [r for r in records if r["condition"] == condition and r["variant"] == "T"]
        if len(rows) != 2 or any(r["status"] != "COMPLETE" or r["score_split"] != "validation" or r["stage"] != "screen" or
                                 r["updates_completed"] != 500 for r in rows):
            raise ValueError("Baseline screen incomplete; do not choose an easier rival")
        if len({r["training_seed"] for r in rows}) != 2 or len({r["geometry_seed"] for r in rows}) != 1 or len({r["task"] for r in rows}) != 1:
            raise ValueError("Screen requires two distinct initializations and one task/geometry")
        candidates[condition] = {"score": float(np.mean([r["score"] for r in rows])),
                                 "active_edges": rows[0]["active_edges"], "parameters": rows[0]["parameters"]}
    if len({r["task"] for r in records}) != 1 or len({r["geometry_seed"] for r in records}) != 1:
        raise ValueError("Mixed task/geometry screen cannot select a rival")
    best = max(v["score"] for v in candidates.values())
    tied = [c for c in order if best-candidates[c]["score"] <= tolerance]
    # Shared core/shape: lower edge count is the only varying active MAC term.
    chosen = min(tied, key=lambda c: (candidates[c]["active_edges"], order.index(c)))
    return {"condition": chosen, "candidates": candidates, "criterion": "validation_mean; <=.005 MAC then fixed order"}
