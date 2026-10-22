"""Directed incoming graph contracts; no silent repair or symmetrization."""
from __future__ import annotations

from hashlib import sha256
import math
from typing import Any

import numpy as np
from scipy.spatial import Delaunay
from scipy.sparse import csr_matrix, diags
from scipy.sparse.csgraph import connected_components, shortest_path, laplacian
from scipy.sparse.linalg import eigsh

from .geometry import Geometry, MASTER_SEED, array_hash, minimum_image


def _id_ties(N: int) -> np.ndarray:
    """Stable SHA256 identity keys, independent of Python hash, marks and seed."""
    return np.asarray([int.from_bytes(sha256(f"larp-node-id:{i}".encode()).digest()[:8], "big")
                       for i in range(N)], dtype=np.uint64)


def validate_edge_index(edge_index: np.ndarray, N: int, *, k: int | None = None) -> np.ndarray:
    e = np.asarray(edge_index)
    if e.ndim != 2 or e.shape[0] != 2 or not np.issubdtype(e.dtype, np.integer):
        raise ValueError("edge_index must be integer (2,E), source then target.")
    if np.any(e < 0) or np.any(e >= N) or np.any(e[0] == e[1]):
        raise ValueError("Out-of-range nodes or self loops in edge_index.")
    if len(np.unique(e[0]*N+e[1])) != e.shape[1]:
        raise ValueError("Duplicate directed arcs in edge_index.")
    if k is not None and (e.shape[1] != k*N or not np.all(np.bincount(e[1], minlength=N) == k)):
        raise ValueError("Incoming-degree contract violated.")
    return e.astype(np.int64, copy=False)


def knn_graph(points: np.ndarray, L: float, k: int = 6) -> np.ndarray:
    """j -> i when j is one of i's k nearest periodic neighbors.

    Sorting uses distance and stable ID hash. No mark, target or class enters
    adjacency. Dense distances are intentional at N400/1600; rows are chunked
    at larger sizes to keep memory bounded.
    """
    points = np.asarray(points, dtype=np.float64)
    N = len(points)
    if k < 1 or k >= N:
        raise ValueError("Require 1 <= k < N.")
    ties = _id_ties(N)
    source = np.empty((N, k), dtype=np.int64)
    for start in range(0, N, 256):
        stop = min(N, start+256)
        displacement = minimum_image(points[None] - points[start:stop, None], L)
        squared = np.einsum("ijk,ijk->ij", displacement, displacement)
        squared[np.arange(stop-start), np.arange(start, stop)] = np.inf
        # Exact float64 squared distance is primary; ID hashes only break ties.
        for offset, row in enumerate(squared):
            source[start+offset] = np.lexsort((ties, row))[:k]
    target = np.repeat(np.arange(N), k)
    edge_index = np.vstack((source.ravel(), target))
    validate_edge_index(edge_index, N, k=k)
    return edge_index


def _circumcenters(triangles: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    a, b, c = triangles[:, 0], triangles[:, 1], triangles[:, 2]
    u, v = b-a, c-a
    determinant = 2*(u[:, 0]*v[:, 1]-u[:, 1]*v[:, 0])
    valid = np.abs(determinant) > 1e-14
    centers = np.full(a.shape, np.nan)
    uu, vv = np.sum(u*u, axis=1), np.sum(v*v, axis=1)
    relative = np.column_stack((v[:, 1]*uu-u[:, 1]*vv, u[:, 0]*vv-v[:, 0]*uu))
    centers[valid] = a[valid] + relative[valid]/determinant[valid, None]
    radius = np.linalg.norm(centers-a, axis=1)
    return centers, radius, valid


def _periodic_delaunay_edges(points: np.ndarray, L: float, copies: int) -> tuple[np.ndarray, dict]:
    N = len(points)
    half = copies//2
    offsets = [(a*L, b*L) for a in range(-half, half+1) for b in range(-half, half+1)]
    tiled = np.concatenate([points + offset for offset in offsets])
    ids = np.tile(np.arange(N), len(offsets))
    triangulation = Delaunay(tiled)
    centers, radius, valid = _circumcenters(tiled[triangulation.simplices])
    selected = valid & (centers[:, 0] >= 0) & (centers[:, 0] < L) & (centers[:, 1] >= 0) & (centers[:, 1] < L)
    triangles = ids[triangulation.simplices[selected]]
    if not len(triangles):
        raise ValueError("No periodic Delaunay triangles selected.")
    if np.any(np.apply_along_axis(lambda row: len(np.unique(row)), 1, triangles) < 3):
        raise ValueError("Delaunay repeats an original vertex within a periodic triangle.")
    undirected = np.sort(np.vstack((triangles[:, [0, 1]], triangles[:, [1, 2]], triangles[:, [0, 2]])), axis=1)
    undirected = np.unique(undirected, axis=0)
    edges = np.concatenate((undirected, undirected[:, ::-1])).T
    order = np.lexsort((edges[0], edges[1]))
    edges = edges[:, order]
    validate_edge_index(edges, N)
    return edges, {"copies": copies, "triangles": len(triangles), "undirected_edges": len(undirected),
                   "generic_torus_3N_edges": bool(len(undirected) == 3*N),
                   "maximum_circumradius": float(radius[selected].max()),
                   "large_circumradius": bool(np.any(radius[selected] >= L/2))}


def periodic_delaunay_graph(points: np.ndarray, L: float, *, verify_translation: bool = True,
                            return_diagnostics: bool = False) -> np.ndarray | tuple[np.ndarray, dict]:
    """3x3 tiling, circumcenter selection; 5x5 only when radius >= L/2."""
    points = np.asarray(points, dtype=np.float64)
    edges, diagnostics = _periodic_delaunay_edges(points, L, 3)
    if diagnostics["large_circumradius"]:
        larger, larger_diagnostics = _periodic_delaunay_edges(points, L, 5)
        if not np.array_equal(larger, edges):
            raise ValueError("3x3 and 5x5 periodic Delaunay disagree.")
        if larger_diagnostics["large_circumradius"]:
            raise ValueError("Delaunay circumradius ambiguity persists with 5x5 copies.")
        edges, diagnostics = larger, larger_diagnostics
    if verify_translation:
        translated = (points + np.asarray([0.137, 0.271])*L) % L
        comparison, _ = _periodic_delaunay_edges(translated, L, diagnostics["copies"])
        if not np.array_equal(edges, comparison):
            raise ValueError("Periodic Delaunay is not invariant to global translation (degenerate configuration).")
        diagnostics["translation_invariance"] = "PASS"
    else:
        diagnostics["translation_invariance"] = "NOT_RUN"
    diagnostics["edge_hash"] = array_hash(edges)
    return (edges, diagnostics) if return_diagnostics else edges


def grid_cardinal_graph(points: np.ndarray, L: float) -> np.ndarray:
    N = len(points)
    side = math.isqrt(N)
    if side*side != N or side < 3:
        raise ValueError("Cardinal graph needs a square grid with side >=3.")
    xy = np.floor(np.asarray(points)).astype(int)
    if len(np.unique(xy, axis=0)) != N or not np.isclose(L, side):
        raise ValueError("Expected one grid point per integer grid cell.")
    lookup = {tuple(position): index for index, position in enumerate(xy)}
    source, target = [], []
    for i, (a, b) in enumerate(xy):
        for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            source.append(lookup[((a+da) % side, (b+db) % side)])
            target.append(i)
    edges = np.asarray((source, target), dtype=np.int64)
    validate_edge_index(edges, N, k=4)
    return edges


def random_regular_graph(N: int, seed: int, degree: int = 6,
                         *, return_diagnostics: bool = False) -> np.ndarray | tuple[np.ndarray, dict]:
    import networkx as nx
    if degree >= N or N*degree % 2:
        raise ValueError("Invalid regular graph degree/N.")
    attempts = []
    children = np.random.SeedSequence([MASTER_SEED, seed, 201]).spawn(20)
    for attempt, child in enumerate(children):
        graph_seed = int(child.generate_state(1, dtype=np.uint32)[0])
        graph = nx.random_regular_graph(degree, N, seed=graph_seed)
        connected = nx.is_connected(graph)
        attempts.append({"attempt": attempt, "seed": graph_seed, "connected": connected})
        if connected:
            pairs = np.asarray(sorted(tuple(sorted(pair)) for pair in graph.edges()), dtype=np.int64)
            edges = np.vstack((pairs, pairs[:, ::-1])).T
            edges = edges[:, np.lexsort((edges[0], edges[1]))]
            validate_edge_index(edges, N, k=degree)
            if not np.all(np.bincount(edges[0], minlength=N) == degree):
                raise AssertionError("Random-regular outdegree mismatch.")
            diagnostics = {"attempts": attempts, "connected": True, "edge_hash": array_hash(edges)}
            return (edges, diagnostics) if return_diagnostics else edges
    raise ValueError("No connected random-regular graph in 20 attempts; seed failed.")


def small_world_graph(points: np.ndarray, L: float, seed: int, *, regime: str = "causal") -> np.ndarray:
    N = len(points)
    rng = np.random.default_rng(np.random.SeedSequence([MASTER_SEED, seed, 202]))
    if regime == "causal":
        edges = knn_graph(points, L, 6).copy()
        for target in range(N):
            slots = np.flatnonzero(edges[1] == target)
            for slot in slots:
                if rng.random() < .10:
                    current = set(int(x) for x in edges[0, slots])
                    # The existing source is eligible after its slot is freed.
                    # This is a uniformly chosen valid origin, not guaranteed
                    # long-range; the causal specification does not require it.
                    current.remove(int(edges[0, slot]))
                    eligible = np.asarray([i for i in range(N) if i != target and i not in current])
                    edges[0, slot] = rng.choice(eligible)
    elif regime == "ecological":
        cardinal = grid_cardinal_graph(points, L)
        source = []
        target = []
        for i in range(N):
            neighbors = list(cardinal[0, cardinal[1] == i])
            distances = np.linalg.norm(minimum_image(np.asarray(points)-points[i], L), axis=1)
            eligible = np.flatnonzero((distances >= L/4) & (np.arange(N) != i)
                                     & ~np.isin(np.arange(N), neighbors))
            if len(eligible) < 2:
                raise ValueError("Insufficient remote origins for ecological SW.")
            neighbors.extend(rng.choice(eligible, 2, replace=False).tolist())
            source.extend(neighbors)
            target.extend([i]*6)
        edges = np.asarray((source, target), dtype=np.int64)
    else:
        raise ValueError("SW regime must be causal or ecological.")
    validate_edge_index(edges, N, k=6)
    return edges


def directed_degree_preserving_swaps(edge_index: np.ndarray, N: int, seed: int,
                                     *, proposals: int | None = None, test_only: bool = False) -> np.ndarray:
    """Conditional control: 100E proposals, preserve each vertex's in/out count."""
    edges = validate_edge_index(edge_index, N).copy()
    E = edges.shape[1]
    count = 100*E if proposals is None else proposals
    if not test_only and count != 100*E:
        raise ValueError("Changing swap proposal budget requires test_only=True.")
    rng = np.random.default_rng(np.random.SeedSequence([MASTER_SEED, seed, 203]))
    present = set((int(a), int(b)) for a, b in edges.T)
    for _ in range(count):
        i, j = rng.choice(E, 2, replace=False)
        a, b = map(int, edges[:, i])
        c, d = map(int, edges[:, j])
        if a == c or b == d or a == d or c == b or (a, d) in present or (c, b) in present:
            continue
        present.remove((a, b)); present.remove((c, d))
        present.add((a, d)); present.add((c, b))
        edges[1, i], edges[1, j] = d, b
    validate_edge_index(edges, N)
    if not np.array_equal(np.bincount(edges[0], minlength=N), np.bincount(edge_index[0], minlength=N)) or not np.array_equal(
            np.bincount(edges[1], minlength=N), np.bincount(edge_index[1], minlength=N)):
        raise AssertionError("Degree-preserving swap changed degree.")
    return edges


def build_graph(geometry: Geometry, kind: str = "knn", *, regime: str = "causal",
                seed: int | None = None, k: int = 6) -> np.ndarray:
    seed = int(geometry.metadata.get("geometry_seed", 1101) if seed is None else seed)
    kind = {"knn6": "knn", "directed_incoming_knn": "knn", "periodic_delaunay": "delaunay",
            "rr": "random_regular", "sw": "small_world"}.get(kind, kind)
    if kind == "knn":
        return knn_graph(geometry.points, geometry.L, k)
    if kind == "delaunay":
        return periodic_delaunay_graph(geometry.points, geometry.L)
    if kind in ("cardinal", "grid"):
        return grid_cardinal_graph(geometry.points, geometry.L)
    if kind == "random_regular":
        return random_regular_graph(geometry.N, seed, degree=k)
    if kind == "small_world":
        return small_world_graph(geometry.points, geometry.L, seed, regime=regime)
    raise ValueError(f"Unknown graph kind {kind!r}.")


def directed_distances(edge_index: np.ndarray, N: int, sources: np.ndarray | None = None) -> np.ndarray:
    edges = validate_edge_index(edge_index, N)
    adjacency = csr_matrix((np.ones(edges.shape[1]), (edges[0], edges[1])), shape=(N, N))
    return shortest_path(adjacency, directed=True, unweighted=True, indices=sources)


def graph_metrics(edge_index: np.ndarray, N: int, points: np.ndarray | None = None,
                  L: float | None = None, *, spectral: bool = True) -> dict[str, Any]:
    edges = validate_edge_index(edge_index, N)
    source, target = edges
    adjacency = csr_matrix((np.ones(edges.shape[1]), (source, target)), shape=(N, N))
    in_degree, out_degree = np.bincount(target, minlength=N), np.bincount(source, minlength=N)
    arcs = set((int(a), int(b)) for a, b in edges.T)
    reciprocal = sum((b, a) in arcs for a, b in arcs)/len(arcs) if arcs else 0.0
    scc_count, scc_labels = connected_components(adjacency, directed=True, connection="strong")
    weak_count, weak_labels = connected_components(adjacency, directed=True, connection="weak")
    undirected = adjacency.maximum(adjacency.T)
    degree = np.asarray(undirected.sum(axis=1)).ravel()
    triangles_twice = np.asarray((undirected @ undirected).multiply(undirected).sum(axis=1)).ravel()
    clustering = np.divide(triangles_twice, degree*(degree-1), out=np.zeros(N), where=degree > 1)
    if N <= 400:
        origins = np.arange(N)
    else:
        origins = np.argsort(_id_ties(N))[:min(256, N)]
    distances = directed_distances(edges, N, origins)
    off_diagonal = np.ones(distances.shape, dtype=bool)
    off_diagonal[np.arange(len(origins)), origins] = False
    finite = distances[np.isfinite(distances) & off_diagonal]
    finite_hist = np.bincount(finite.astype(int)).tolist() if finite.size else []
    metrics = {"edge_hash": array_hash(edges), "N": N, "E": edges.shape[1],
               "in_degree": in_degree.tolist(), "out_degree": out_degree.tolist(),
               "in_degree_mean": float(in_degree.mean()), "in_degree_variance": float(in_degree.var()),
               "out_degree_mean": float(out_degree.mean()), "out_degree_variance": float(out_degree.var()),
               "reciprocity": reciprocal, "undirected_clustering_mean": float(clustering.mean()),
               "SCC_count": int(scc_count), "SCC_sizes": np.bincount(scc_labels).tolist(),
               "weak_component_count": int(weak_count), "weak_component_sizes": np.bincount(weak_labels).tolist(),
               "path_origin_ids": origins.tolist(), "path_all_pairs": bool(N <= 400),
               "finite_path_length_histogram": finite_hist,
               "inaccessible_fraction": float(np.isinf(distances[off_diagonal]).mean()),
               "finite_path_mean": float(finite.mean()) if finite.size else None,
               "finite_diameter": int(finite.max()) if finite.size else None,
               "algebraic_connectivity": {"status": "NOT_RUN"}}
    if points is not None:
        if L is None:
            raise ValueError("Edge-length metrics require L.")
        lengths = np.linalg.norm(minimum_image(np.asarray(points)[source]-np.asarray(points)[target], L), axis=1)
        metrics["edge_lengths"] = lengths.tolist()
        metrics["edge_length_mean"] = float(lengths.mean()) if len(lengths) else None
        metrics["edge_length_p50_p90_p95"] = np.quantile(lengths, [.5, .9, .95]).tolist() if len(lengths) else []
    if spectral and N > 2:
        if weak_count > 1:
            eigenvalue = 0.0
        else:
            matrix = laplacian(undirected, normed=False)
            if N <= 400:
                eigenvalue = float(np.linalg.eigvalsh(matrix.toarray())[1])
            else:
                eigenvalue = float(np.sort(eigsh(matrix.astype(float), k=2, which="SM", return_eigenvectors=False,
                                                  v0=np.sin(np.arange(N)+1.), tol=1e-6))[1])
        metrics["algebraic_connectivity"] = {"status": "COMPUTED", "value": eigenvalue,
                                             "definition": "unnormalized_laplacian_symmetrized_graph",
                                             "nonlinear_stability_certificate": False}
    return metrics


def hop_type_coverage(edge_index: np.ndarray, labels: np.ndarray, N: int,
                      hops: tuple[int, ...] = (1, 2, 4, 8)) -> dict:
    """Counts of types that can influence each node in <=h directed steps."""
    adjacency = csr_matrix((np.ones(edge_index.shape[1]), (edge_index[0], edge_index[1])), shape=(N, N))
    # Sources in row, targets in column: distance[source,target].
    distances = shortest_path(adjacency, directed=True, unweighted=True)
    report = {}
    for h in hops:
        accessible = distances <= h
        counts = np.asarray([(accessible & (labels[:, None] == c)).sum(axis=0) for c in range(5)]).T
        report[str(h)] = {"counts_by_node_and_type": counts.tolist(),
                          "type_empty_fraction": (counts == 0).mean(axis=0).tolist(),
                          "mean_counts_by_type": counts.mean(axis=0).tolist()}
    return report
