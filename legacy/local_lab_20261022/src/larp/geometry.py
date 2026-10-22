"""Frozen finite collective-coordinate geometries and auditable mark controls.

The avian preview is not this preregistered generator. No tissue sizes or
homotypic repulsion are added here. All admission thresholds are specification
constants; test-only budgets can never yield an admissible scientific artifact.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping
import json
import math
import time

import numpy as np
from scipy.optimize import line_search
from scipy.spatial import cKDTree, Voronoi

MASTER_SEED = 20261008
TYPE_NAMES = ("A", "B", "C", "D", "E")
TYPE_WEIGHTS = (407, 211, 171, 126, 85)
WINDOW_RADII = (0.5, 1.0, 2.0, 3.0, 4.0, 5.0)
GENERATOR_VERSION = "collective_coordinate_v0.1"


def array_hash(array: np.ndarray) -> str:
    a = np.ascontiguousarray(array)
    h = sha256()
    h.update(a.dtype.str.encode("ascii"))
    h.update(json.dumps(a.shape).encode("ascii"))
    h.update(a.tobytes())
    return h.hexdigest()


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(k): _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    if isinstance(value, np.generic):
        return value.item()
    return value


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


@dataclass(frozen=True)
class Geometry:
    points: np.ndarray
    labels: np.ndarray
    L: float
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        p = np.array(self.points, dtype=np.float64, order="C", copy=True)
        c = np.array(self.labels, dtype=np.int64, order="C", copy=True)
        if p.ndim != 2 or p.shape[1] != 2 or c.shape != (len(p),):
            raise ValueError("Expected points (N,2) and labels (N,).")
        if not np.isfinite(p).all() or not np.isfinite(self.L) or self.L <= 0:
            raise ValueError("Coordinates and positive domain length must be finite.")
        if np.any(p < 0) or np.any(p >= self.L):
            raise ValueError("Geometry coordinates must already lie in [0,L).")
        if np.any(c < 0) or np.any(c >= 5):
            raise ValueError("Five class IDs are 0..4.")
        # Bytes-backed arrays cannot be made writable again by setflags.
        p = np.frombuffer(p.tobytes(), dtype=np.float64).reshape(p.shape)
        c = np.frombuffer(c.tobytes(), dtype=np.int64).reshape(c.shape)
        object.__setattr__(self, "points", p)
        object.__setattr__(self, "labels", c)
        object.__setattr__(self, "L", float(self.L))
        object.__setattr__(self, "metadata", _freeze(dict(self.metadata)))

    @property
    def N(self) -> int:
        return len(self.points)

    @property
    def hashes(self) -> dict[str, str]:
        xhash = array_hash(self.points)
        lhash = array_hash(self.labels)
        total = sha256((xhash + lhash + float(self.L).hex()).encode()).hexdigest()
        return {"points": xhash, "labels": lhash, "geometry": total}

    def save(self, path: str | Path) -> None:
        save_geometry(self, path)

    def to_dict(self, *, include_arrays: bool = False) -> dict:
        result = {"N": self.N, "L": self.L, "hashes": self.hashes,
                  "metadata": _plain(self.metadata)}
        if include_arrays:
            result.update({"points": self.points.tolist(), "labels": self.labels.tolist()})
        return result

    @classmethod
    def load(cls, path: str | Path) -> "Geometry":
        return load_geometry(path)


def save_geometry(geometry: Geometry, path: str | Path) -> None:
    """Write immutable numeric arrays and JSON metadata without pickled objects."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        previous = load_geometry(target)
        if previous.hashes != geometry.hashes:
            raise FileExistsError("Refusing to replace a geometry with different hashes.")
        return
    metadata = _plain(geometry.metadata)
    metadata["hashes"] = geometry.hashes
    temp = target.with_name(target.name + ".tmp")
    with temp.open("wb") as f:
        np.savez_compressed(f, points=geometry.points, labels=geometry.labels,
                            L=np.asarray(geometry.L), metadata_json=np.asarray(
                                json.dumps(metadata, sort_keys=True, allow_nan=False)))
    temp.replace(target)


def load_geometry(path: str | Path) -> Geometry:
    with np.load(path, allow_pickle=False) as f:
        metadata = json.loads(str(f["metadata_json"].item()))
        geometry = Geometry(f["points"], f["labels"], float(f["L"].item()), metadata)
    if metadata.get("hashes") != geometry.hashes:
        raise ValueError("Geometry hash mismatch: artifact was changed or corrupted.")
    return geometry


def hamilton_counts(N: int, equal: bool = False) -> np.ndarray:
    if not isinstance(N, (int, np.integer)) or N < 5:
        raise ValueError("At least five nodes are needed for five nonempty types.")
    weights = np.ones(5, dtype=np.int64) if equal else np.asarray(TYPE_WEIGHTS)
    denominator = int(weights.sum())
    numerators = int(N) * weights
    result = numerators // denominator
    remainders = numerators % denominator
    order = np.lexsort((np.arange(5), -remainders))
    result[order[:int(N - result.sum())]] += 1
    if np.any(result == 0):
        raise ValueError("This N leaves at least one biological component empty.")
    return result.astype(np.int64)


def minimum_image(delta: np.ndarray, L: float) -> np.ndarray:
    delta = np.asarray(delta, dtype=np.float64)
    return delta - L * np.round(delta / L)


def periodic_distances(a: np.ndarray, b: np.ndarray, L: float) -> np.ndarray:
    return np.linalg.norm(minimum_image(np.asarray(a)[:, None] - np.asarray(b)[None], L), axis=-1)


def integer_modes(L: float, *, max_wave_number: float | None = None,
                  exclude_optimized: bool = False) -> np.ndarray:
    cutoff = L / 10 if max_wave_number is None else max_wave_number * L / (2 * np.pi)
    radius = int(math.ceil(cutoff))
    modes = [(x, y) for x in range(radius + 1) for y in range(-radius, radius + 1)
             if (x > 0 or x == 0 and y > 0) and x*x+y*y <= cutoff*cutoff + 1e-12
             and (not exclude_optimized or x*x+y*y > (L/10)**2 + 1e-12)]
    modes.sort(key=lambda n: (n[0]*n[0]+n[1]*n[1], -n[0], -n[1]))
    return np.asarray(modes, dtype=np.int64).reshape(-1, 2)


def spectral_amplitudes(points: np.ndarray, labels: np.ndarray, L: float,
                        modes: np.ndarray | None = None) -> np.ndarray:
    """Returns A_A,...,A_E,A_union for each nonredundant integer mode."""
    modes = integer_modes(L) if modes is None else np.asarray(modes)
    phase = np.exp(2j * np.pi / L * (np.asarray(points) @ modes.T))
    components = np.asarray([phase[np.asarray(labels) == c].sum(axis=0) for c in range(5)])
    return np.vstack((components, phase.sum(axis=0)))


def structure_factors(points: np.ndarray, labels: np.ndarray, L: float,
                      modes: np.ndarray | None = None, chunk_size: int = 64) -> np.ndarray:
    modes = integer_modes(L) if modes is None else np.asarray(modes)
    counts = np.r_[np.bincount(labels, minlength=5), len(points)].astype(float)
    if np.any(counts == 0):
        raise ValueError("Structure factors require nonempty components.")
    blocks = [np.abs(spectral_amplitudes(points, labels, L, modes[start:start+chunk_size]))**2
              / counts[:, None] for start in range(0, len(modes), chunk_size)]
    return np.concatenate(blocks, axis=1) if blocks else np.empty((6, 0))


def geometry_objective(points: np.ndarray, labels: np.ndarray, L: float, *,
                       kind: str = "mhu", modes: np.ndarray | None = None,
                       details: bool = False) -> tuple[float, np.ndarray] | tuple[float, np.ndarray, dict]:
    """Analytic periodic collective-coordinate energy and its gradient.

    cKDTree pairs are rebuilt at *every* evaluation. Coordinates at an exact
    collision are nondifferentiable; no numerical tie direction is invented.
    """
    points = np.asarray(points, dtype=np.float64) % L
    labels = np.asarray(labels, dtype=np.int64)
    modes = integer_modes(L) if modes is None else np.asarray(modes, dtype=np.int64)
    if kind not in ("mhu", "hu") or len(modes) == 0:
        raise ValueError("MHU/HU objective needs at least one optimized mode (L>=10).")
    k = 2 * np.pi / L * modes
    phases = np.exp(1j * points @ k.T)
    gradient = np.zeros_like(points)
    amplitude = phases.sum(axis=0)
    N, M = len(points), len(modes)
    union_energy = float(np.mean(np.abs(amplitude)**2 / N))
    gradient += -2 / (N*M) * np.imag(phases * amplitude.conj()) @ k
    component_energy = 0.0
    if kind == "mhu":
        for c in range(5):
            mask = labels == c
            n = int(mask.sum())
            if n == 0:
                raise ValueError("MHU objective has an empty component.")
            a = phases[mask].sum(axis=0)
            component_energy += float(np.mean(np.abs(a)**2/n) / 5)
            gradient[mask] += -2 / (5*n*M) * np.imag(phases[mask] * a.conj()) @ k
    pairs = cKDTree(points, boxsize=L).query_pairs(0.30, output_type="ndarray")
    repulsion_energy = 0.0
    if len(pairs):
        i, j = pairs.T
        displacement = minimum_image(points[i] - points[j], L)
        r = np.linalg.norm(displacement, axis=1)
        if np.any(r == 0):
            raise ValueError("Exact coincident points make the repulsion gradient undefined.")
        residual = 1 - r / 0.30
        repulsion_energy = float(10 / N * residual @ residual)
        pair_grad = -20 / (N * 0.30) * (residual/r)[:, None] * displacement
        np.add.at(gradient, i, pair_grad)
        np.add.at(gradient, j, -pair_grad)
    total = union_energy + component_energy + repulsion_energy
    if details:
        return total, gradient, {"union_energy": union_energy, "component_energy": component_energy,
                                 "repulsion_energy": repulsion_energy, "active_pairs": len(pairs),
                                 "gradient_norm": float(np.linalg.norm(gradient))}
    return total, gradient


def finite_difference_gradient_check(points: np.ndarray, labels: np.ndarray, L: float,
                                     *, coordinates: int = 20, seed: int = 6101,
                                     epsilon: float = 1e-6, kind: str = "mhu") -> dict:
    energy, analytic = geometry_objective(points, labels, L, kind=kind)
    rng = np.random.default_rng(np.random.SeedSequence([MASTER_SEED, seed, 104]))
    selected = rng.choice(np.asarray(points).size, min(coordinates, np.asarray(points).size), replace=False)
    numeric, expected = [], []
    for index in selected:
        upper, lower = np.array(points, copy=True), np.array(points, copy=True)
        upper.flat[index] += epsilon
        lower.flat[index] -= epsilon
        numeric.append((geometry_objective(upper, labels, L, kind=kind)[0]
                        - geometry_objective(lower, labels, L, kind=kind)[0])/(2*epsilon))
        expected.append(analytic.flat[index])
    error = np.abs(np.asarray(numeric)-expected)
    return {"energy": energy, "coordinates": selected.tolist(),
            "analytic": expected, "finite_difference": numeric,
            "maximum_absolute_error": float(error.max()),
            "maximum_scaled_error": float(np.max(error / (1 + np.abs(expected)))),
            "passed": bool(np.allclose(numeric, expected, atol=2e-6, rtol=2e-5))}


class _EvaluationLimit(RuntimeError):
    pass


def _optimize(points: np.ndarray, labels: np.ndarray, L: float, kind: str,
              adam_steps: int, lbfgs_iterations: int, lbfgs_evaluations: int) -> tuple[np.ndarray, dict]:
    x = points.copy()
    momentum, variance = np.zeros_like(x), np.zeros_like(x)
    trace = []
    started = time.perf_counter()
    for step in range(adam_steps):
        value, gradient, diagnostics = geometry_objective(x, labels, L, kind=kind, details=True)
        fraction = step / max(1, adam_steps-1)
        lr = 0.0001 + 0.5*(0.025-0.0001)*(1+math.cos(math.pi*fraction))
        momentum = 0.9*momentum + 0.1*gradient
        variance = 0.999*variance + 0.001*gradient**2
        corrected_m = momentum/(1-0.9**(step+1))
        corrected_v = variance/(1-0.999**(step+1))
        x = (x - lr*corrected_m/(np.sqrt(corrected_v)+1e-8)) % L
        if step % 100 == 0 or step == adam_steps-1:
            trace.append({"optimizer": "Adam", "step": step+1, "energy": value, "lr": lr, **diagnostics})
    # Explicit L-BFGS, no bounds: scipy.line_search enforces strong Wolfe.
    # Keep unwrapped iterates here; objective wraps coordinates on evaluation.
    flat = x.ravel().copy()
    history: list[tuple[np.ndarray, np.ndarray, float]] = []
    evaluation_count = 0
    cached_x = cached_value = cached_gradient = None
    last_evaluated = flat.copy()

    def evaluate(z: np.ndarray) -> tuple[float, np.ndarray]:
        nonlocal evaluation_count, cached_x, cached_value, cached_gradient, last_evaluated
        if cached_x is not None and np.array_equal(z, cached_x):
            return cached_value, cached_gradient
        if evaluation_count >= lbfgs_evaluations:
            raise _EvaluationLimit()
        f, g = geometry_objective(z.reshape(-1, 2), labels, L, kind=kind)
        evaluation_count += 1
        cached_x, cached_value, cached_gradient = z.copy(), f, g.ravel()
        last_evaluated = z.copy()
        return f, g.ravel()

    stop = "iteration_limit"
    iterations = 0
    try:
        if lbfgs_iterations and lbfgs_evaluations:
            value, gradient = evaluate(flat)
            for iteration in range(lbfgs_iterations):
                if np.max(np.abs(gradient)) <= 1e-8:
                    stop = "gradient_tolerance"
                    break
                direction = gradient.copy()
                alphas = []
                for s, y, rho in reversed(history):
                    alpha = rho*(s @ direction)
                    alphas.append(alpha)
                    direction -= alpha*y
                if history:
                    s, y, _ = history[-1]
                    direction *= (s @ y)/(y @ y)
                for (s, y, rho), alpha in zip(history, reversed(alphas)):
                    direction += s*(alpha-rho*(y @ direction))
                direction = -direction
                if gradient @ direction >= 0:
                    direction = -gradient
                    history.clear()
                alpha = line_search(lambda z: evaluate(z)[0], lambda z: evaluate(z)[1],
                                    flat, direction, gfk=gradient, old_fval=value,
                                    maxiter=20)[0]
                if alpha is None:
                    stop = "strong_wolfe_line_search_failed"
                    break
                following = flat + alpha*direction
                next_value, next_gradient = evaluate(following)
                s, y = following-flat, next_gradient-gradient
                curvature = float(s @ y)
                if curvature > 1e-14:
                    history.append((s, y, 1/curvature))
                    history = history[-20:]
                iterations += 1
                trace.append({"optimizer": "L-BFGS", "step": iterations, "energy": next_value,
                              "gradient_norm": float(np.linalg.norm(next_gradient))})
                changed = abs(next_value-value) <= 1e-12 or np.max(np.abs(s)) <= 1e-12
                flat, value, gradient = following, next_value, next_gradient
                if changed:
                    stop = "change_tolerance"
                    break
    except _EvaluationLimit:
        stop = "evaluation_limit"
        # Keep the last accepted iterate, never an unaccepted line-search point.
    final = flat.reshape(-1, 2) % L
    energy, gradient, diagnostics = geometry_objective(final, labels, L, kind=kind, details=True)
    return final, {"wall_seconds": time.perf_counter()-started, "adam_steps": adam_steps,
                   "lbfgs_iterations": iterations, "lbfgs_evaluations": evaluation_count,
                   "lbfgs_stop": stop, "final_energy": energy, **diagnostics, "trace": trace}


def generate_geometry(N: int = 400, seed: int = 1101, kind: str = "mhu", equal: bool = False,
                      *, test_only: bool = False, adam_steps: int | None = None,
                      lbfgs_iterations: int | None = None, max_restarts: int | None = None,
                      window_centers: np.ndarray | None = None,
                      detailed_certificate: bool = True) -> Geometry:
    """Generate the first admitted attempt; failed seeds remain failed artifacts.

    Reduced numerical budgets are explicitly test-only, not scientific variants.
    The full certificate still runs by default and a failure does not relax it.
    """
    kind = {"hu_union": "hu", "HU": "hu", "MHU": "mhu"}.get(kind, kind)
    if kind not in ("mhu", "hu", "grid", "poisson"):
        raise ValueError(f"Unknown geometry {kind!r}.")
    budgets = (6000 if adam_steps is None else adam_steps,
               250 if lbfgs_iterations is None else lbfgs_iterations,
               4 if max_restarts is None else max_restarts)
    if not test_only and budgets != (6000, 250, 4):
        raise ValueError("Changing preregistered geometry budgets requires test_only=True.")
    if any(value < 0 for value in budgets) or budgets[2] < 1:
        raise ValueError("Invalid optimizer budget.")
    L = math.sqrt(N)
    counts = hamilton_counts(N, equal)
    children = np.random.SeedSequence([MASTER_SEED, int(seed), 101]).spawn(budgets[2])
    attempts = []
    for attempt, child in enumerate(children):
        streams = child.spawn(2)
        p_rng, c_rng = (np.random.default_rng(stream) for stream in streams)
        initial = p_rng.uniform(0, L, size=(N, 2))
        labels = c_rng.permutation(np.repeat(np.arange(5), counts))
        optimizer = {"status": "NOT_APPLICABLE"}
        if kind == "grid":
            side = math.isqrt(N)
            if side*side != N:
                raise ValueError("A square grid needs square N.")
            initial = np.column_stack(np.unravel_index(np.arange(N), (side, side))).astype(float)+0.5
        if kind in ("mhu", "hu"):
            initial, optimizer = _optimize(initial, labels, L, kind, budgets[0], budgets[1],
                                           1000 if not test_only else max(1, budgets[1]*8))
        metadata = {"generator_version": GENERATOR_VERSION, "kind": kind, "N": N,
                    "density": N/L**2, "geometry_seed": int(seed), "attempt": attempt,
                    "counts": counts.tolist(), "equal_proportions": equal, "test_only": test_only,
                    "seed_keys": [MASTER_SEED, int(seed), 101], "attempt_spawn_key": list(child.spawn_key),
                    "adam_steps": budgets[0], "lbfgs_max_iterations": budgets[1],
                    "modes": integer_modes(L).tolist(), "optimizer": optimizer}
        geometry = Geometry(initial, labels, L, metadata)
        if kind in ("mhu", "hu"):
            certificate = certify_geometry(geometry, scope="union" if kind == "hu" else "mhu",
                                           centers=window_centers, detailed=detailed_certificate)
        else:
            certificate = {"status": "BASELINE_UNCERTIFIED", "passed": False,
                           "scientific_admissible": False, "claim": "baseline_not_MHU"}
        attempts.append({"attempt": attempt, "hashes": geometry.hashes, "optimizer": optimizer,
                         "certificate": certificate})
        metadata.update({"attempts": attempts.copy(), "certificate": certificate,
                         "failed_seed": kind in ("mhu", "hu") and not certificate["passed"]})
        geometry = Geometry(initial, labels, L, metadata)
        if certificate["passed"] or kind in ("poisson", "grid") or test_only:
            return geometry
    return geometry


def common_window_centers(L: float, count: int = 10000, seed: int = 6101) -> np.ndarray:
    """Common across geometries/conditions at equal L; never keyed by geometry."""
    return np.random.default_rng(np.random.SeedSequence([MASTER_SEED, seed, 103])).uniform(0, L, (count, 2))


def window_statistics(geometry: Geometry, centers: np.ndarray,
                      radii: tuple[float, ...] = WINDOW_RADII) -> dict:
    if any(r > geometry.L/2 for r in radii):
        raise ValueError("Specified circular window formula requires R <= L/2.")
    centers = np.asarray(centers, dtype=np.float64) % geometry.L
    result = {}
    for c, name in enumerate((*TYPE_NAMES, "union")):
        points = geometry.points if c == 5 else geometry.points[geometry.labels == c]
        tree = cKDTree(points, boxsize=geometry.L)
        counts = np.asarray([tree.query_ball_point(centers, r, return_length=True) for r in radii])
        p = np.pi*np.asarray(radii)**2/geometry.L**2
        variance = counts.var(axis=1, ddof=0)
        reference = len(points)*p*(1-p)
        result[name] = {"radii": list(radii), "mean_counts": counts.mean(axis=1).tolist(),
                        "variance": variance.tolist(), "binomial_reference": reference.tolist(),
                        "variance_ratio": (variance/reference).tolist(),
                        "empty_fraction": (counts == 0).mean(axis=1).tolist(),
                        "count_p05": np.quantile(counts, 0.05, axis=1).tolist(),
                        "count_p50": np.quantile(counts, 0.50, axis=1).tolist()}
    return result


def _anisotropy(spectra: np.ndarray, modes: np.ndarray) -> list[dict]:
    angles = np.arctan2(modes[:, 1], modes[:, 0])
    harmonic = np.exp(2j*angles)
    reports = []
    for spectrum in spectra:
        z = (spectrum @ harmonic)/max(float(spectrum.sum()), np.finfo(float).tiny)
        reports.append({"quadrupole_magnitude": float(abs(z)), "quadrupole_real": float(z.real),
                        "quadrupole_imag": float(z.imag), "orientation_radians": float(np.angle(z)/2),
                        "flag": bool(abs(z) > 0.30), "flag_is_exclusion": False})
    return reports


def radial_spectra(geometry: Geometry, modes: np.ndarray, spectra: np.ndarray) -> dict:
    """Fixed physical k bins enable comparisons at fixed density across sizes."""
    wave_numbers = 2*np.pi/geometry.L*np.linalg.norm(modes,axis=1)
    boundaries = np.linspace(0,np.pi,41)
    result = {"bin_edges_physical_k":boundaries.tolist(),"bin_count":[],"mean_S":{}}
    selected_bins = np.minimum(np.searchsorted(boundaries,wave_numbers,side="right")-1,39)
    result["bin_count"] = np.bincount(selected_bins,minlength=40).tolist()
    for c,name in enumerate((*TYPE_NAMES,"union")):
        result["mean_S"][name] = [float(spectra[c,selected_bins==i].mean()) if np.any(selected_bins==i) else None for i in range(40)]
    return result


def certify_geometry(geometry: Geometry, *, scope: str = "mhu", centers: np.ndarray | None = None,
                      detailed: bool = True, center_seed: int = 6101,
                      random_anisotropy_controls: int = 0) -> dict:
    """Apply the frozen finite criteria; never infer asymptotic HU from a pass."""
    if scope not in ("mhu", "union"):
        raise ValueError("Certificate scope is mhu or union.")
    modes = integer_modes(geometry.L)
    if len(modes) == 0 or geometry.L < 10:
        return {"status": "NOT_APPLICABLE_TEST_SCALE", "passed": False,
                "scientific_admissible": False, "reason": "Full certificate needs L>=10."}
    centers = common_window_centers(geometry.L, seed=center_seed) if centers is None else np.asarray(centers)
    low = structure_factors(geometry.points, geometry.labels, geometry.L, modes)
    high_modes = integer_modes(geometry.L, max_wave_number=np.pi, exclude_optimized=True)
    high = structure_factors(geometry.points, geometry.labels, geometry.L, high_modes)
    counts = np.r_[np.bincount(geometry.labels, minlength=5), geometry.N]
    windows = window_statistics(geometry, centers)
    nearest = cKDTree(geometry.points, boxsize=geometry.L).query(geometry.points, k=2)[0][:, 1]
    min_distance = float(nearest.min())
    component_reports = {}
    anisotropy = _anisotropy(high, high_modes)
    selected = range(6) if scope == "mhu" else (5,)
    for c, name in enumerate((*TYPE_NAMES, "union")):
        window_ratio = float(np.mean(np.asarray(windows[name]["variance_ratio"])[[4, 5]]))
        mean_s, max_s = float(low[c].mean()), float(low[c].max())
        max_bragg = float(high[c].max()/counts[c])
        passed = mean_s <= 0.05 and max_s <= 0.10 and window_ratio <= 0.65 and max_bragg < 0.50
        component_reports[name] = {"restricted_S": low[c].tolist(), "restricted_mean_S": mean_s,
                                   "restricted_max_S": max_s, "mean_variance_ratio_R4_R5": window_ratio,
                                   "maximum_nonoptimized_S_over_N": max_bragg,
                                   "passed": bool(passed), "required": c in selected,
                                   "anisotropy": anisotropy[c]}
    passed = min_distance >= 0.299 and all(component_reports[(*TYPE_NAMES, "union")[c]]["passed"] for c in selected)
    full_centers = len(centers) == 10000
    scientific = passed and full_centers and not geometry.metadata.get("test_only", False)
    report = {"version": "finite_certificate_v0.1", "scope": scope, "status": "PASS" if passed else "FAIL",
              "passed": bool(passed), "scientific_admissible": bool(scientific),
              "test_only": bool(geometry.metadata.get("test_only", False)),
              "full_window_budget": full_centers, "centers_count": len(centers), "centers_hash": array_hash(centers),
              "center_seed": center_seed, "geometry_hashes": geometry.hashes, "counts": counts.tolist(),
              "density": geometry.N/geometry.L**2, "minimum_union_distance": min_distance,
              "minimum_distance_passed": min_distance >= 0.299,
              "optimized_integer_modes": modes.tolist(), "nonoptimized_integer_modes": high_modes.tolist(),
              "components": component_reports, "window_statistics": windows,
              "nonoptimized_S": high.tolist(), "asymptotic_proof": False,
              "anisotropy_controls": {"status": "NOT_RUN", "required_ensemble_controls": 200}}
    all_modes = np.vstack((modes,high_modes))
    all_spectrum = np.concatenate((low,high),axis=1)
    report["radial_spectra"] = radial_spectra(geometry,all_modes,all_spectrum)
    high_k = 2*np.pi/geometry.L*np.linalg.norm(high_modes,axis=1)
    rebound = high_k <= 1.5*np.pi/5 + 1e-12
    report["rebound_after_cutoff"] = {"physical_k_interval":[np.pi/5,1.5*np.pi/5],
        "modes":high_modes[rebound].tolist(),
        "mean_S":{name:float(high[c,rebound].mean()) if np.any(rebound) else None
                  for c,name in enumerate((*TYPE_NAMES,"union"))},
        "is_admission_criterion":False}
    if detailed:
        report["descriptive"] = geometry_diagnostics(geometry, centers)
    if random_anisotropy_controls:
        if random_anisotropy_controls != 200:
            raise ValueError("Preregistered anisotropy ensemble uses exactly 200 random controls.")
        report["anisotropy_controls"] = anisotropy_reference(geometry, controls=200)
    return report


def toroidal_voronoi_areas(points: np.ndarray, L: float) -> np.ndarray:
    N = len(points)
    offsets = np.asarray([(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)])*L
    tiled = np.concatenate([points + offset for offset in offsets])
    diagram = Voronoi(tiled)
    central = 4*N + np.arange(N)
    areas = []
    for vertex in central:
        region = diagram.regions[diagram.point_region[vertex]]
        if -1 in region or len(region) < 3:
            raise ValueError("Periodic Voronoi has an unbounded central region.")
        polygon = diagram.vertices[region]
        areas.append(abs(np.sum(polygon[:, 0]*np.roll(polygon[:, 1], -1)
                                - polygon[:, 1]*np.roll(polygon[:, 0], -1)))/2)
    areas = np.asarray(areas)
    if not np.isclose(areas.sum(), L*L, atol=1e-7, rtol=1e-7):
        raise ValueError("Toroidal Voronoi area does not sum to domain area.")
    return areas


def geometry_diagnostics(geometry: Geometry, centers: np.ndarray | None = None) -> dict:
    centers = common_window_centers(geometry.L) if centers is None else np.asarray(centers)
    p, labels, L, N = geometry.points, geometry.labels, geometry.L, geometry.N
    tree = cKDTree(p, boxsize=L)
    distances, indices = tree.query(p, k=min(N, 7))
    nearest = distances[:, 1]
    delta = minimum_image(p[indices[:, 1:]]-p[:, None], L)
    theta = np.arctan2(delta[..., 1], delta[..., 0])
    orders = {}
    for q in (4, 6):
        local = np.mean(np.exp(1j*q*theta), axis=1)
        orders[f"q{q}"] = {"local_abs_mean": float(np.abs(local).mean()),
                              "global_abs": float(abs(local.mean())),
                              "global_real": float(local.mean().real), "global_imag": float(local.mean().imag)}
    nearest_type = {}
    for c, name in enumerate(TYPE_NAMES):
        type_tree = cKDTree(p[labels == c], boxsize=L)
        d = type_tree.query(centers, k=1)[0]
        self_dist = type_tree.query(p[labels == c], k=2)[0][:, 1]
        nearest_type[name] = {"distance_to_type_p50_p90_p95": np.quantile(d, [.5, .9, .95]).tolist(),
                              "within_type_nearest_CDF_sorted": np.sort(self_dist).tolist()}
    radius = min(5.0, L/2)
    bins = np.linspace(0, radius, 41)
    pairs = tree.query_pairs(radius, output_type="ndarray")
    r = np.linalg.norm(minimum_image(p[pairs[:, 0]]-p[pairs[:, 1]], L), axis=1)
    area = np.pi*(bins[1:]**2-bins[:-1]**2)/(L*L)
    g2 = {"bin_edges": bins.tolist()}
    union_hist = np.histogram(r, bins)[0]
    g2["union"] = (union_hist/(N*(N-1)/2*area)).tolist()
    for a in range(5):
        for b in range(a, 5):
            if a == b:
                mask = (labels[pairs[:, 0]] == a) & (labels[pairs[:, 1]] == a)
                n = int(np.sum(labels == a))
                expected_pairs = n*(n-1)/2
            else:
                mask = ((labels[pairs[:, 0]] == a) & (labels[pairs[:, 1]] == b)) | ((labels[pairs[:, 0]] == b) & (labels[pairs[:, 1]] == a))
                expected_pairs = int(np.sum(labels == a))*int(np.sum(labels == b))
            g2[f"{TYPE_NAMES[a]}_{TYPE_NAMES[b]}"] = (np.histogram(r[mask], bins)[0]/(expected_pairs*area)).tolist()
    try:
        areas = toroidal_voronoi_areas(p, L)
        voronoi = {"status": "COMPUTED", "areas": areas.tolist(), "mean": float(areas.mean()), "variance": float(areas.var())}
    except Exception as exc:
        voronoi = {"status": "FAILED", "error": str(exc)}
    return {"nearest_neighbor_CDF_sorted": np.sort(nearest).tolist(), "nearest_type": nearest_type,
            "g2": g2, "voronoi": voronoi, "orientational_order": orders}


def anisotropy_reference(geometry: Geometry, controls: int = 200, seed: int = 6101) -> dict:
    modes = integer_modes(geometry.L, max_wave_number=np.pi, exclude_optimized=True)
    rng = np.random.default_rng(np.random.SeedSequence([MASTER_SEED, seed, 105]))
    references = []
    for _ in range(controls):
        points = rng.uniform(0, geometry.L, geometry.points.shape)
        spectra = structure_factors(points, geometry.labels, geometry.L, modes)
        references.append([v["quadrupole_magnitude"] for v in _anisotropy(spectra, modes)])
    values = np.asarray(references)
    return {"status": "COMPUTED", "count": controls, "seed_keys": [MASTER_SEED, seed, 105],
            "quadrupole_by_control": values.tolist(), "p50_p90_p95_by_component": np.quantile(values, [.5, .9, .95], axis=0).tolist(),
            "ensemble_systematic_anisotropy_assessment": "NOT_RUN_requires_multiple_MHU_geometries"}


def shuffle_labels(labels: np.ndarray, seed: int) -> np.ndarray:
    return np.random.default_rng(np.random.SeedSequence([MASTER_SEED, seed, 7101])).permutation(labels)


def clustered_labels(geometry: Geometry, seed: int) -> np.ndarray:
    rng = np.random.default_rng(np.random.SeedSequence([MASTER_SEED, seed, 7101, 2]))
    shifted_x = (geometry.points[:, 0] + rng.uniform(0, geometry.L)) % geometry.L
    order = np.lexsort((np.arange(geometry.N), shifted_x))
    labels = np.empty(geometry.N, dtype=np.int64)
    labels[order] = np.repeat(np.arange(5), np.bincount(geometry.labels, minlength=5))
    return labels


def _metropolis(energy, labels: np.ndarray, rng: np.random.Generator, proposals: int) -> tuple[np.ndarray, float, dict]:
    labels = labels.copy()
    current = float(energy(labels))
    best, best_energy = labels.copy(), current
    accepted = 0
    for step in range(proposals):
        i = int(rng.integers(len(labels)))
        j = int(rng.integers(len(labels)))
        while labels[j] == labels[i]:
            i, j = map(int, rng.integers(len(labels), size=2))
        labels[i], labels[j] = labels[j], labels[i]
        following = float(energy(labels))
        temperature = 0.1 * (0.0001/0.1)**(step/max(1, proposals-1))
        delta = following-current
        if delta <= 0 or rng.random() < math.exp(-delta/temperature):
            current = following
            accepted += 1
            if current < best_energy:
                best, best_energy = labels.copy(), current
        else:
            labels[i], labels[j] = labels[j], labels[i]
    return best, best_energy, {"proposals": proposals, "accepted": accepted, "minimum_energy": best_energy}


class _MarkAnnealingState:
    """Exact cached sufficient statistics; swaps leave the target energy intact."""

    def __init__(self, geometry: Geometry, labels: np.ndarray, control: str,
                 edge_index: np.ndarray | None, reference: Mapping | None):
        self.geometry, self.labels = geometry, labels.copy()
        self.control, self.reference = control, reference
        self.phase = np.exp(2j*np.pi/geometry.L*(geometry.points @ integer_modes(geometry.L).T))
        self.counts = np.bincount(labels, minlength=5)
        self.amplitudes = np.asarray([self.phase[labels == c].sum(axis=0) for c in range(5)])
        if control == "matched":
            self.edges = np.asarray(edge_index)
            source, target = self.edges
            self.directed_pairs = np.bincount(labels[source]*5+labels[target], minlength=25).reshape(5,5)
            self.outdegree = np.bincount(source, minlength=geometry.N)
            self.degree_sum = np.bincount(labels, weights=self.outdegree, minlength=5)
            self.edge_incidence = [np.flatnonzero((source == i) | (target == i)) for i in range(geometry.N)]
            self.pairs = cKDTree(geometry.points, boxsize=geometry.L).query_pairs(3.0, output_type="ndarray")
            r = np.linalg.norm(minimum_image(geometry.points[self.pairs[:,0]]-geometry.points[self.pairs[:,1]], geometry.L),axis=1)
            self.bins = np.minimum(np.searchsorted([0,.5,1,2,3],r,side="right")-1,3)
            self.pair_incidence = [np.flatnonzero(np.any(self.pairs == i,axis=1)) for i in range(geometry.N)]
            self.homotypic = np.zeros((5,4),dtype=np.int64)
            same = labels[self.pairs[:,0]] == labels[self.pairs[:,1]]
            np.add.at(self.homotypic,(labels[self.pairs[same,0]],self.bins[same]),1)

    def energy(self) -> float:
        spectrum = np.mean(np.abs(self.amplitudes)**2/self.counts[:,None],axis=1)
        if self.control == "grid_balanced":
            return float(spectrum.mean())
        feature = {"directed_type_edge_matrix": self.directed_pairs,
                   "homotypic_pair_bins": self.homotypic,
                   "class_mean_outdegree": self.degree_sum/self.counts,
                   "component_mean_low_k_S": spectrum}
        return matched_energy(feature,self.reference)

    def swap(self, i: int, j: int) -> None:
        a,b = int(self.labels[i]),int(self.labels[j])
        difference = self.phase[j]-self.phase[i]
        self.amplitudes[a] += difference
        self.amplitudes[b] -= difference
        if self.control == "matched":
            affected_e = np.union1d(self.edge_incidence[i],self.edge_incidence[j])
            source,target = self.edges[:,affected_e]
            np.add.at(self.directed_pairs,(self.labels[source],self.labels[target]),-1)
            affected_p = np.union1d(self.pair_incidence[i],self.pair_incidence[j])
            u,v = self.pairs[affected_p].T
            old_same = self.labels[u] == self.labels[v]
            np.add.at(self.homotypic,(self.labels[u[old_same]],self.bins[affected_p[old_same]]),-1)
            degree_difference = self.outdegree[j]-self.outdegree[i]
            self.degree_sum[a] += degree_difference
            self.degree_sum[b] -= degree_difference
        self.labels[i],self.labels[j] = b,a
        if self.control == "matched":
            np.add.at(self.directed_pairs,(self.labels[source],self.labels[target]),1)
            new_same = self.labels[u] == self.labels[v]
            np.add.at(self.homotypic,(self.labels[u[new_same]],self.bins[affected_p[new_same]]),1)

    def rebuild(self) -> None:
        """Eliminate floating accumulation every 1000 proposals, before admission."""
        self.amplitudes = np.asarray([self.phase[self.labels == c].sum(axis=0) for c in range(5)])


def _anneal_marks(geometry: Geometry, labels: np.ndarray, control: str,
                  edge_index: np.ndarray | None, reference: Mapping | None,
                  rng: np.random.Generator, proposals: int) -> tuple[np.ndarray,float,dict]:
    state = _MarkAnnealingState(geometry,labels,control,edge_index,reference)
    current = state.energy()
    best,best_energy = state.labels.copy(),current
    accepted = 0
    for step in range(proposals):
        i,j = map(int,rng.integers(geometry.N,size=2))
        while state.labels[i] == state.labels[j]:
            i,j = map(int,rng.integers(geometry.N,size=2))
        state.swap(i,j)
        following = state.energy()
        temperature = 0.1*(0.0001/0.1)**(step/max(1,proposals-1))
        delta = following-current
        if delta <= 0 or rng.random() < math.exp(-delta/temperature):
            current = following
            accepted += 1
            if current < best_energy:
                best,best_energy = state.labels.copy(),current
        else:
            state.swap(i,j)
        if (step+1)%1000 == 0:
            state.rebuild()
            current = state.energy()
    final = _MarkAnnealingState(geometry,best,control,edge_index,reference).energy()
    return best,final,{"proposals":proposals,"accepted":accepted,"minimum_energy":final,
                       "implementation":"cached_exact_statistics_incremental_swaps"}


def mark_features(geometry: Geometry, labels: np.ndarray, edge_index: np.ndarray) -> dict:
    labels = np.asarray(labels)
    source, target = np.asarray(edge_index)
    directed_pairs = np.bincount(labels[source]*5+labels[target], minlength=25).reshape(5, 5)
    outdegree = np.bincount(source, minlength=geometry.N)
    means = np.asarray([outdegree[labels == c].mean() for c in range(5)])
    pairs = cKDTree(geometry.points, boxsize=geometry.L).query_pairs(3.0, output_type="ndarray")
    r = np.linalg.norm(minimum_image(geometry.points[pairs[:, 0]]-geometry.points[pairs[:, 1]], geometry.L), axis=1)
    histograms = np.asarray([np.histogram(r[(labels[pairs[:, 0]] == c) & (labels[pairs[:, 1]] == c)], [0, .5, 1, 2, 3])[0] for c in range(5)])
    low = structure_factors(geometry.points, labels, geometry.L)[:5].mean(axis=1)
    return {"directed_type_edge_matrix": directed_pairs, "homotypic_pair_bins": histograms,
            "class_mean_outdegree": means, "component_mean_low_k_S": low}


def matched_energy(features: Mapping, reference: Mapping) -> float:
    total = 0.0
    for key in ("directed_type_edge_matrix", "homotypic_pair_bins"):
        expected = np.asarray(reference[key])
        tolerance = np.where(expected >= 20, 0.05*expected, 2.0)
        residual = np.maximum(0, np.abs(np.asarray(features[key])-expected)-tolerance)/tolerance
        total += float(np.sum(residual**2))
    deviation = np.abs(np.asarray(features["class_mean_outdegree"])-reference["class_mean_outdegree"])
    total += float(np.sum((np.maximum(0, deviation-0.10)/0.10)**2))
    total += float(np.sum((np.maximum(0, 0.50-np.asarray(features["component_mean_low_k_S"]))/0.50)**2))
    return total


def relabel_geometry(geometry: Geometry, control: str = "shuffle", seed: int | None = None,
                     *, edge_index: np.ndarray | None = None, test_only: bool = False,
                     proposals: int = 100000, restarts: int = 10,
                     centers: np.ndarray | None = None) -> Geometry:
    seed = int(geometry.metadata.get("geometry_seed", 1101) if seed is None else seed)
    control = {"gridbalanced": "grid_balanced", "matched_local_statistics": "matched"}.get(control, control)
    if control == "matched" and not test_only:
        raise RuntimeError("SCIENTIFIC_BLOCKER B_MATCHED-PAIR-POPULATION: population of homotypic "
                           "pairs must be resolved and preregistered before scientific C3 execution; "
                           "test_only=True permits technical verification only.")
    if not test_only and (proposals != 100000 or restarts != 10):
        raise ValueError("Reduced mark annealing budgets require test_only=True.")
    metadata = _plain(geometry.metadata)
    metadata.update({"mark_control": control, "parent_hashes": geometry.hashes, "control_seed": seed,
                     "test_only": bool(test_only or metadata.get("test_only", False))})
    if control == "native":
        return geometry
    if control == "shuffle":
        labels = shuffle_labels(geometry.labels, seed)
    elif control == "clustered":
        labels = clustered_labels(geometry, seed)
    elif control in ("grid_balanced", "matched"):
        if control == "matched" and edge_index is None:
            raise ValueError("Matched control requires the unchanged directed graph.")
        if control == "grid_balanced" and geometry.metadata.get("kind") != "grid":
            raise ValueError("Grid-balanced controls require a grid geometry.")
        equal = np.all(np.bincount(geometry.labels, minlength=5) == geometry.N/5)
        records = []
        if control == "grid_balanced" and equal:
            xy = np.floor(geometry.points).astype(int)
            labels = (xy[:, 0]+2*xy[:, 1]) % 5
            metadata["annealing"] = {"status": "EXACT_EQUAL_SUBLATTICE", "proposals": 0}
        else:
            reference = None if control == "grid_balanced" else mark_features(geometry, geometry.labels, edge_index)
            children = np.random.SeedSequence([MASTER_SEED, seed, 7101, 3 if control == "grid_balanced" else 4]).spawn(restarts)
            best, minimum, admitted = geometry.labels.copy(), math.inf, False
            for attempt, child in enumerate(children):
                rng = np.random.default_rng(child)
                initial = rng.permutation(geometry.labels)
                candidate, candidate_energy, record = _anneal_marks(geometry, initial, control, edge_index, reference, rng, proposals)
                record["attempt"] = attempt
                if candidate_energy < minimum:
                    best, minimum = candidate, candidate_energy
                if control == "matched":
                    passed = candidate_energy <= 1e-10
                    record["features"] = _plain(mark_features(geometry, candidate, edge_index))
                else:
                    trial = Geometry(geometry.points, candidate, geometry.L, metadata)
                    certificate = certify_geometry(trial, centers=centers, detailed=False)
                    # A crystalline union is deliberate for Grid. Only the
                    # component spectral/window criteria select balanced marks.
                    passed = all(v["restricted_mean_S"] <= .05 and v["restricted_max_S"] <= .10
                                 and v["mean_variance_ratio_R4_R5"] <= .65
                                 for name, v in certificate["components"].items() if name != "union")
                    record["component_certificate"] = certificate["components"]
                record["admitted"] = bool(passed)
                records.append(record)
                if passed:
                    best, minimum, admitted = candidate, candidate_energy, True
                    break
            labels = best
            metadata["annealing"] = {"status": "ADMITTED" if admitted else "FAILED", "attempts": records,
                                     "minimum_energy": minimum, "admitted": admitted,
                                     "name": control if admitted else ("Grid balanceada aproximada" if control == "grid_balanced" else "matched_failed"),
                                     "long_wave_mechanism_identifiable": False,
                                     "scientific_blocker": "B_MATCHED-PAIR-POPULATION" if control == "matched" else None,
                                     "homotypic_population": "all_unordered_physical_pairs_within_distance_3_not_graph_arcs"}
    else:
        raise ValueError(f"Unknown mark control {control!r}.")
    result = Geometry(geometry.points, labels, geometry.L, metadata)
    if not np.array_equal(result.points, geometry.points) or not np.array_equal(
            np.bincount(result.labels, minlength=5), np.bincount(geometry.labels, minlength=5)):
        raise AssertionError("Mark controls must conserve coordinates and exact counts.")
    # Original certificate describes original marks only; never inherit it as
    # though shuffled or clustered marks also met MHU admission.
    metadata["native_certificate"] = metadata.pop("certificate", None)
    metadata["certificate"] = {"status": "MARK_CONTROL_NOT_NATIVE_MHU", "passed": False,
                               "scientific_admissible": False, "parent_geometry_hash": geometry.hashes["geometry"]}
    return Geometry(result.points, result.labels, result.L, metadata)
