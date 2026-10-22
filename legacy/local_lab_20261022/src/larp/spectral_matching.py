"""Fixed-substrate mark controls: exact local matching and spectral diagnostics.

This prospective module never changes coordinates, graph arcs or physical
radii. Marks denote functional channels. Scientific execution requires an
externally frozen protocol; the low-level search has no neural/field scores.
Historical generators and certificates are deliberately not imported as
mutable scientific machinery.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
import math
import time

import numpy as np
from scipy.special import j1

from .artifacts import digest, file_hash
from .geometry import Geometry, array_hash, integer_modes, periodic_distances
from .graphs import validate_edge_index

ROOT = Path(__file__).resolve().parents[2]
VERSION = "fixed_X_functional_marks_spectral_matching_v1"
COUNTS = (163, 85, 68, 50, 34)
CENTER_SEED_KEYS = (20261008, 8841)
PAIR_BINS = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5)
LOCAL_RADII = (1.25, 2.5)
DEFAULT_TOLERANCES = {
    "coverage_cdf": 0.02,
    "coverage_quantile_over_a": 0.03,
    "window_cdf": 0.02,
    "window_void": 0.02,
    "homotypic_cdf_floor": 0.05,
    "homotypic_cdf_count_numerator": 2.0,
    "homotypic_quantile_over_a": 0.05,
    "homotypic_minimum_slack_over_a": 0.05,
    "integer_count_absolute_floor": 2,
    "integer_count_relative": 0.05,
    "integer_count_relative_minimum": 20,
    "outdegree_difference_over_incoming_degree": 0.02,
}


def empirical_cdf_distance(first: np.ndarray, second: np.ndarray) -> float:
    """Exact two-sample CDF sup distance, including ties/right continuity."""
    first, second = np.sort(np.asarray(first)), np.sort(np.asarray(second))
    if not len(first) or not len(second):
        raise ValueError("CDF matching requires two nonempty samples")
    support = np.unique(np.concatenate((first, second)))
    first_counts = np.searchsorted(first, support, side="right").astype(np.int64)
    second_counts = np.searchsorted(second, support, side="right").astype(np.int64)
    # Integer cross-products before division keep the 200/10000=.02 boundary
    # exact; subtracting two floating CDFs can incorrectly reject that boundary.
    numerator = np.max(np.abs(first_counts * len(second) - second_counts * len(first)))
    return float(numerator / (len(first) * len(second)))


def integer_count_tolerance(native_count: int, tolerances: dict | None = None) -> int:
    tolerance = DEFAULT_TOLERANCES if tolerances is None else tolerances
    floor = int(tolerance["integer_count_absolute_floor"])
    if native_count < tolerance["integer_count_relative_minimum"]:
        return floor
    return max(floor, math.ceil(float(tolerance["integer_count_relative"]) * native_count))


def exact_disc_window_variance(points: np.ndarray, L: float, radius: float) -> dict:
    """Uniform-center torus variance from pair-disc intersections, without MC.

    For R<=L/4 the closest periodic image is the only possible positive-area
    intersection. Larger windows require additional images and are rejected.
    This diagnostic is not an extra admission inequality.
    """
    points = np.asarray(points, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 2 or not len(points):
        raise ValueError("A nonempty (n,2) point array is required")
    if not np.isfinite(points).all() or not np.isfinite(L) or L <= 0 or not 0 < radius <= L / 4:
        raise ValueError("Exact closest-image disc formula requires 0<R<=L/4")
    if np.any(points < 0) or np.any(points >= L):
        raise ValueError("Points must lie in the periodic box")
    distances = periodic_distances(points, points, L)[np.triu_indices(len(points), k=1)]
    active = distances[distances < 2 * radius]
    scaled = np.clip(active / (2 * radius), 0, 1)
    overlaps = 2 * radius**2 * np.arccos(scaled) - .5 * active * np.sqrt(
        np.maximum(4 * radius**2 - active**2, 0))
    area = np.pi * radius**2
    mean = len(points) * area / L**2
    second = (len(points) * area + 2 * overlaps.sum()) / L**2
    return {"radius": float(radius), "count": len(points), "mean": float(mean),
            "second_moment": float(second), "variance": float(second - mean**2),
            "method": "exact_uniform_torus_centers_pair_disc_intersections_R_le_L_over_4",
            "monte_carlo_centers_used": False, "admission_criterion": False}


def spectral_disc_variance_lower_bound(count: int, L: float, radius: float,
                                       modes: np.ndarray, mean_structure_floor: float) -> dict:
    """Necessary variance bound given a mean S floor over nonredundant modes.

    Parseval contributions are nonnegative. For M half-space modes the smallest
    disk Fourier weight times M*mean(S) is a conservative bound, allowing S to
    concentrate in the mode whose disk weight is smallest. This is not a bound
    that assumes each individual mode reaches the mean floor.
    """
    modes = np.asarray(modes)
    if not isinstance(count, (int, np.integer)) or count < 1 or L <= 0 or not 0 < radius <= L / 2:
        raise ValueError("Positive count and ordinary disc 0<R<=L/2 required")
    if modes.ndim != 2 or modes.shape[1] != 2 or len(modes) == 0 or not np.issubdtype(modes.dtype, np.integer):
        raise ValueError("Nonempty integer modes required")
    if np.any(np.all(modes == 0, axis=1)) or mean_structure_floor < 0:
        raise ValueError("Nonzero modes and nonnegative mean structure floor required")
    canonical = [tuple(mode) for mode in modes]
    if len(set(canonical)) != len(canonical) or any(tuple(-mode) in set(canonical) for mode in modes):
        raise ValueError("Modes must be unique and exclude conjugate duplicates")
    z = 2 * np.pi * radius / L * np.linalg.norm(modes, axis=1)
    normalized_weights = (2 * j1(z) / z)**2
    area = np.pi * radius**2
    coefficient = 2 * count * area**2 / L**4
    bound = coefficient * len(modes) * mean_structure_floor * normalized_weights.min()
    return {"radius": float(radius), "count": int(count), "modes": modes.tolist(),
            "mean_structure_floor": float(mean_structure_floor),
            "normalized_disc_fourier_weights": normalized_weights.tolist(),
            "minimum_weight": float(normalized_weights.min()),
            "variance_lower_bound": float(bound),
            "parseval_coefficient_per_halfspace_mode": float(coefficient),
            "necessary_not_sufficient": True,
            "floor_is_mean_over_modes_not_each_mode": True,
            "inferential_scope": "deterministic_substrate_uniform_periodic_centers"}


def _readonly(array: np.ndarray) -> np.ndarray:
    result = np.ascontiguousarray(array)
    return np.frombuffer(result.tobytes(), dtype=result.dtype).reshape(result.shape)


@dataclass(frozen=True)
class TypeFeatures:
    count: int
    scale_a: float
    coverage: np.ndarray
    coverage_quantiles: np.ndarray
    window_counts: tuple[np.ndarray, ...]
    homotypic_nearest: np.ndarray
    homotypic_quantiles: np.ndarray
    homotypic_minimum: float
    physical_pair_histogram: np.ndarray
    outdegree_mean: float
    exact_window_variances: tuple[float, ...]


@dataclass(frozen=True)
class LocalFeatures:
    labels_hash: str
    labels: np.ndarray
    type_features: tuple[TypeFeatures, ...]
    directed_type_arcs: np.ndarray


class SpectralMatchingCache:
    """Geometry-only float64 cache; metric values are never task dependent."""

    def __init__(self, geometry: Geometry, edge_index: np.ndarray, *,
                 center_count: int = 10000,
                 center_seed_keys: tuple[int, ...] = CENTER_SEED_KEYS,
                 centers: np.ndarray | None = None,
                 optimized_modes: np.ndarray | None = None,
                 pair_bins: tuple[float, ...] = PAIR_BINS,
                 local_radii: tuple[float, ...] = LOCAL_RADII,
                 incoming_degree: int = 6,
                 physical_radii: np.ndarray | None = None):
        self.geometry = geometry
        self.points, self.native_labels, self.L = geometry.points, geometry.labels, geometry.L
        self.N = geometry.N
        self.counts = np.bincount(geometry.labels, minlength=5)
        if np.any(self.counts < 2):
            raise ValueError("Each component needs at least two homotypic samples")
        self.edges = _readonly(validate_edge_index(edge_index, self.N))
        if not isinstance(incoming_degree, int) or incoming_degree <= 0:
            raise ValueError("Incoming-degree normalization must be positive")
        if not np.all(np.bincount(self.edges[1], minlength=self.N) == incoming_degree):
            raise ValueError("Frozen incoming-degree normalization must match every node")
        self.incoming_degree = incoming_degree
        if physical_radii is None:
            self.physical_radii = None
        else:
            radii = np.asarray(physical_radii, dtype=np.float64)
            if radii.shape != (self.N,) or not np.isfinite(radii).all() or np.any(radii <= 0):
                raise ValueError("Physical radii must be positive finite values for every original node")
            self.physical_radii = _readonly(radii)
        self.pair_bins, self.local_radii = tuple(pair_bins), tuple(local_radii)
        if len(self.pair_bins) < 2 or not np.all(np.diff(self.pair_bins) > 0):
            raise ValueError("Pair histogram bins must be strictly increasing")
        if not self.local_radii or not np.all(np.asarray(self.local_radii) > 0):
            raise ValueError("Window radii must be positive")
        if centers is None:
            if not isinstance(center_count, int) or center_count < 1:
                raise ValueError("Center count must be a positive integer")
            rng = np.random.default_rng(np.random.SeedSequence(center_seed_keys))
            centers = rng.uniform(0, self.L, (center_count, 2))
        centers = np.asarray(centers, dtype=np.float64)
        if centers.ndim != 2 or centers.shape[1] != 2 or not len(centers) or not np.isfinite(centers).all():
            raise ValueError("Centers must be a nonempty finite (M,2) array")
        if np.any(centers < 0) or np.any(centers >= self.L):
            raise ValueError("Centers must lie in the same periodic box")
        self.centers = _readonly(centers)
        self.center_seed_keys = tuple(center_seed_keys)
        self.center_distances = _readonly(periodic_distances(self.centers, self.points, self.L))
        self.point_distances = _readonly(periodic_distances(self.points, self.points, self.L))
        self.window_membership = tuple(_readonly(self.center_distances <= radius)
                                       for radius in self.local_radii)
        self.outdegree = _readonly(np.bincount(self.edges[0], minlength=self.N))
        modes = integer_modes(self.L) if optimized_modes is None else np.asarray(optimized_modes)
        if modes.ndim != 2 or modes.shape[1] != 2 or not len(modes) or not np.issubdtype(modes.dtype, np.integer):
            raise ValueError("At least one integer reciprocal-lattice mode is required")
        self.modes = _readonly(modes.astype(np.int64))
        self.phase = _readonly(np.exp(2j * np.pi / self.L * (self.points @ self.modes.T)))
        self.union_amplitude = _readonly(self.phase.sum(axis=0))
        self.native_features = self.local_features(self.native_labels)
        self.native_amplitudes = self.amplitudes(self.native_labels)

    @classmethod
    def from_geometry(cls, geometry: Geometry, edge_index: np.ndarray, **kwargs):
        return cls(geometry, edge_index, **kwargs)

    def validate_labels(self, labels: np.ndarray) -> np.ndarray:
        labels = np.asarray(labels)
        if labels.shape != (self.N,) or not np.issubdtype(labels.dtype, np.integer):
            raise ValueError("Marks must have integer shape (N,)")
        if np.any(labels < 0) or np.any(labels >= 5):
            raise ValueError("Marks must be five component IDs 0..4")
        if not np.array_equal(np.bincount(labels, minlength=5), self.counts):
            raise ValueError("Functional mark controls must preserve all five counts")
        return labels.astype(np.int64, copy=False)

    def _type_features(self, labels: np.ndarray, component: int) -> TypeFeatures:
        selected = np.flatnonzero(labels == component)
        count = len(selected)
        scale = self.L / math.sqrt(count)
        coverage = self.center_distances[:, selected].min(axis=1)
        windows = tuple(membership[:, selected].sum(axis=1, dtype=np.int64)
                        for membership in self.window_membership)
        distances = self.point_distances[np.ix_(selected, selected)].copy()
        upper = distances[np.triu_indices(count, k=1)]
        histogram = np.histogram(upper, bins=self.pair_bins)[0]
        np.fill_diagonal(distances, np.inf)
        nearest = distances.min(axis=1)
        variances = []
        for radius in self.local_radii:
            if radius > self.L / 4:
                raise ValueError("Exact local variance requires R<=L/4")
            active = upper[upper < 2 * radius]
            overlap = 2 * radius**2 * np.arccos(np.clip(active / (2 * radius), 0, 1)) - .5 * active * np.sqrt(
                np.maximum(4 * radius**2 - active**2, 0))
            mean = count * np.pi * radius**2 / self.L**2
            variances.append(float(mean + 2 * overlap.sum() / self.L**2 - mean**2))
        return TypeFeatures(count, scale, _readonly(coverage),
                            _readonly(np.quantile(coverage, [.5, .9, .95], method="linear")),
                            tuple(_readonly(window) for window in windows),
                            _readonly(nearest),
                            _readonly(np.quantile(nearest, [.1, .5, .9], method="linear")),
                            float(nearest.min()), _readonly(histogram),
                            float(self.outdegree[selected].mean()), tuple(variances))

    def directed_arc_counts(self, labels: np.ndarray) -> np.ndarray:
        labels = self.validate_labels(labels)
        # Row=source component, column=target component. No symmetrization.
        index = 5 * labels[self.edges[0]] + labels[self.edges[1]]
        return np.bincount(index, minlength=25).reshape(5, 5)

    def local_features(self, labels: np.ndarray, *, previous: LocalFeatures | None = None,
                       changed_types: tuple[int, ...] | None = None) -> LocalFeatures:
        labels = self.validate_labels(labels)
        if previous is not None and changed_types is None:
            raise ValueError("Incremental features require explicit changed component IDs")
        changed = set(range(5)) if previous is None else set(changed_types)
        if any(component not in range(5) for component in changed):
            raise ValueError("Unknown changed component")
        if previous is not None:
            changed_nodes = np.flatnonzero(labels != previous.labels)
            actual_changed = set(labels[changed_nodes]) | set(previous.labels[changed_nodes])
            if not actual_changed.issubset(changed):
                raise ValueError("Incremental update omitted a changed component")
        types = tuple(self._type_features(labels, component) if component in changed
                      else previous.type_features[component] for component in range(5))
        return LocalFeatures(array_hash(labels), _readonly(labels), types, _readonly(self.directed_arc_counts(labels)))

    def amplitudes(self, labels: np.ndarray) -> np.ndarray:
        labels = self.validate_labels(labels)
        return np.asarray([self.phase[labels == component].sum(axis=0) for component in range(5)])

    def swapped_amplitudes(self, amplitudes: np.ndarray, labels: np.ndarray,
                           first: int, second: int) -> np.ndarray:
        """Exact two-component swap delta; caller retains unchanged old marks."""
        labels = self.validate_labels(labels)
        if first == second or not 0 <= first < self.N or not 0 <= second < self.N:
            raise ValueError("Swap requires two distinct node IDs in range")
        if np.asarray(amplitudes).shape != (5, len(self.modes)):
            raise ValueError("Amplitude array shape mismatch")
        result = np.array(amplitudes, dtype=np.complex128, copy=True)
        a, b = labels[first], labels[second]
        if a != b:
            delta = self.phase[second] - self.phase[first]
            result[a] += delta
            result[b] -= delta
        return result

    def structure_factors(self, amplitudes: np.ndarray) -> np.ndarray:
        return np.abs(amplitudes)**2 / self.counts[:, None]

    def identity(self) -> dict:
        return {"version": VERSION, "N": self.N, "L": self.L,
                "geometry_hashes": self.geometry.hashes,
                "edge_hash": array_hash(self.edges),
                "center_hash": array_hash(self.centers),
                "center_count": len(self.centers), "center_seed_keys": list(self.center_seed_keys),
                "point_distances_hash": array_hash(self.point_distances),
                "center_distances_hash": array_hash(self.center_distances),
                "mode_hash": array_hash(self.modes), "modes": self.modes.tolist(),
                "counts": self.counts.tolist(), "pair_bins": list(self.pair_bins),
                "local_radii": list(self.local_radii), "incoming_degree": self.incoming_degree,
                "physical_radii_by_original_node_hash": (array_hash(self.physical_radii)
                                                         if self.physical_radii is not None else None),
                "physical_radii_follow_original_nodes": True,
                "marks_mean_functional_channels": True,
                "neural_or_field_scores_used": False}

    def measure(self, labels: np.ndarray, *, features: LocalFeatures | None = None,
                amplitudes: np.ndarray | None = None, descriptive: bool = True) -> dict:
        labels = self.validate_labels(labels)
        features = self.local_features(labels) if features is None else features
        if features.labels_hash != array_hash(labels):
            raise ValueError("Cached features belong to different marks")
        amplitudes = self.amplitudes(labels) if amplitudes is None else amplitudes
        types = []
        for component, local in enumerate(features.type_features):
            windows = []
            for radius, counts in zip(self.local_radii, local.window_counts):
                histogram = np.bincount(counts)
                windows.append({"radius": radius, "count_histogram": histogram.tolist(),
                                "count_mean": float(counts.mean()),
                                "count_variance_population_empirical_centers": float(counts.var(ddof=0)),
                                "void_fraction": float(np.mean(counts == 0)),
                                "occupied_fraction": float(np.mean(counts > 0)),
                                "window_counts_hash": array_hash(counts)})
            types.append({"component": component, "count": local.count, "scale_a": local.scale_a,
                          "coverage_quantiles_p50_p90_p95": local.coverage_quantiles.tolist(),
                          "coverage_distances_hash": array_hash(local.coverage),
                          "local_windows": windows,
                          "homotypic_nearest_distances": local.homotypic_nearest.tolist(),
                          "homotypic_quantiles_p10_p50_p90": local.homotypic_quantiles.tolist(),
                          "homotypic_minimum": local.homotypic_minimum,
                          "all_unordered_physical_pair_histogram": local.physical_pair_histogram.tolist(),
                          "outdegree_mean": local.outdegree_mean,
                          "exact_local_window_variance": [exact_disc_window_variance(
                              self.points[labels == component], self.L, radius)
                              for radius in self.local_radii if radius <= self.L / 4]})
        result = {"labels_hash": array_hash(labels), "types": types,
                  "directed_type_arc_counts_source_target": features.directed_type_arcs.tolist(),
                  "spectral": spectral_metrics(amplitudes, self.union_amplitude, self.counts, self.modes),
                  "union_amplitude_hash": array_hash(self.union_amplitude),
                  "field_or_neural_scores_used": False}
        if descriptive:
            # These measurements never participate in local matching/admission.
            result["descriptive_long_windows"] = [
                {"radius": radius,
                 "types": [{"component": component,
                            "mean": float(counts.mean()), "variance": float(counts.var(ddof=0)),
                            "void_fraction": float(np.mean(counts == 0))}
                           for component in range(5)
                           for counts in [(self.center_distances[:, labels == component] <= radius).sum(axis=1)]]}
                for radius in (4.0, 5.0)]
            outside = integer_modes(self.L, max_wave_number=2 * np.pi * 6 / self.L,
                                    exclude_optimized=True)
            phase = np.exp(2j * np.pi / self.L * (self.points @ outside.T))
            rho = np.asarray([phase[labels == c].sum(axis=0) for c in range(5)])
            result["descriptive_outside_band"] = spectral_metrics(rho, phase.sum(axis=0), self.counts, outside)
        return result


def spectral_metrics(amplitudes: np.ndarray, union_amplitude: np.ndarray,
                     counts: np.ndarray, modes: np.ndarray) -> dict:
    """Per-mode spectra and mode-averaged cross matrix, not independent replicas."""
    rho = np.asarray(amplitudes, dtype=np.complex128)
    counts = np.asarray(counts, dtype=np.int64)
    union = np.asarray(union_amplitude, dtype=np.complex128)
    if counts.shape != (5,) or np.any(counts <= 0) or rho.shape != (5, len(union)) or len(union) == 0:
        raise ValueError("Five nonempty components and nonempty common modes required")
    if not np.isfinite(rho).all() or not np.isfinite(union).all():
        raise ValueError("Spectral amplitudes must be finite")
    N = int(counts.sum())
    structure = np.abs(rho)**2 / counts[:, None]
    union_structure = np.abs(union)**2 / N
    fractions = counts / N
    eta = rho - fractions[:, None] * union
    concentration = np.abs(eta)**2 / (counts * (1 - fractions))[:, None]
    normalized = rho / np.sqrt(counts[:, None])
    normalized_eta = eta / np.sqrt((counts * (1 - fractions))[:, None])
    cross = normalized @ normalized.conj().T / rho.shape[1]
    concentration_cross = normalized_eta @ normalized_eta.conj().T / rho.shape[1]
    return {"modes": np.asarray(modes, dtype=np.int64).tolist(),
            "component_structure_factors": structure.tolist(),
            "component_means": structure.mean(axis=1).tolist(),
            "component_maxima": structure.max(axis=1).tolist(),
            "union_structure_factors": union_structure.tolist(),
            "union_mean": float(union_structure.mean()), "union_maximum": float(union_structure.max()),
            "rho_real": rho.real.tolist(), "rho_imag": rho.imag.tolist(),
            "concentration_eta_real": eta.real.tolist(), "concentration_eta_imag": eta.imag.tolist(),
            "concentration_structure_factors": concentration.tolist(),
            "concentration_means": concentration.mean(axis=1).tolist(),
            "component_cross_mode_mean_real": cross.real.tolist(),
            "component_cross_mode_mean_imag": cross.imag.tolist(),
            "concentration_cross_mode_mean_real": concentration_cross.real.tolist(),
            "concentration_cross_mode_mean_imag": concentration_cross.imag.tolist(),
            "concentration_sum_maximum_absolute": float(np.abs(eta.sum(axis=0)).max()),
            "cross_covariance_definition": "mean_modes(rho_c*conj(rho_d))/sqrt(n_c*n_d)",
            "concentration_cross_definition": "mean_modes(eta_c*conj(eta_d))/sqrt(n_c*(1-f_c)*n_d*(1-f_d))",
            "modes_are_not_independent_geometry_replicates": True,
            "finite_certificate_is_not_asymptotic_proof": True}


def compare_local_features(reference: LocalFeatures, candidate: LocalFeatures, *,
                           tolerances: dict | None = None, incoming_degree: int = 6,
                           variance_guard_relative: float | None = None) -> dict:
    """Every inequality is recorded; no averaging can hide a failed component."""
    tolerances = dict(DEFAULT_TOLERANCES if tolerances is None else tolerances)
    if set(tolerances) != set(DEFAULT_TOLERANCES):
        raise ValueError("Local tolerance keys must be explicit and complete")
    if variance_guard_relative is not None and (not np.isfinite(variance_guard_relative) or variance_guard_relative <= 0):
        raise ValueError("Optional exact variance relative tolerance must be positive")
    residuals: list[dict] = []

    def record(name: str, value: float, bound: float, component: int | None, **details):
        if not np.isfinite(value) or bound <= 0:
            raise ValueError("Residuals require finite values and positive thresholds")
        residuals.append({"name": name, "component": component, "value": float(value),
                          "tolerance": float(bound), "ratio": float(value / bound),
                          "passed": bool(value <= bound), **details})

    for component, (native, control) in enumerate(zip(reference.type_features, candidate.type_features)):
        if native.count != control.count or native.scale_a != control.scale_a:
            raise ValueError("The conditioned component counts/scales changed")
        record("coverage_cdf", empirical_cdf_distance(native.coverage, control.coverage),
               tolerances["coverage_cdf"], component)
        for index, quantile in enumerate((.5, .9, .95)):
            record("coverage_quantile", abs(native.coverage_quantiles[index] - control.coverage_quantiles[index]) / native.scale_a,
                   tolerances["coverage_quantile_over_a"], component, quantile=quantile)
        if len(native.window_counts) != len(control.window_counts):
            raise ValueError("Window radii changed")
        for index, (native_counts, control_counts) in enumerate(zip(native.window_counts, control.window_counts)):
            record("window_count_cdf", empirical_cdf_distance(native_counts, control_counts),
                   tolerances["window_cdf"], component, radius_index=index)
            if len(native_counts) != len(control_counts):
                raise ValueError("Window counts must share the frozen centers")
            void_difference = abs(int(np.count_nonzero(native_counts == 0)) - int(np.count_nonzero(control_counts == 0))) / len(native_counts)
            record("window_void_fraction", void_difference,
                   tolerances["window_void"], component, radius_index=index)
            if variance_guard_relative is not None:
                native_variance = native.exact_window_variances[index]
                candidate_variance = control.exact_window_variances[index]
                if native_variance <= 0:
                    raise ValueError("Relative variance guard requires a positive native variance")
                record("exact_window_variance_relative_difference", abs(candidate_variance - native_variance) / native_variance,
                       variance_guard_relative, component, radius_index=index,
                       reference_variance=native_variance, candidate_variance=candidate_variance)
        homo_bound = max(tolerances["homotypic_cdf_floor"], tolerances["homotypic_cdf_count_numerator"] / native.count)
        record("homotypic_nearest_cdf", empirical_cdf_distance(native.homotypic_nearest, control.homotypic_nearest),
               homo_bound, component)
        for index, quantile in enumerate((.1, .5, .9)):
            record("homotypic_quantile", abs(native.homotypic_quantiles[index] - control.homotypic_quantiles[index]) / native.scale_a,
                   tolerances["homotypic_quantile_over_a"], component, quantile=quantile)
        record("homotypic_minimum_deficit", max(0.0, native.homotypic_minimum - control.homotypic_minimum) / native.scale_a,
               tolerances["homotypic_minimum_slack_over_a"], component)
        for bin_index, (native_count, control_count) in enumerate(zip(native.physical_pair_histogram, control.physical_pair_histogram)):
            record("homotypic_unordered_pair_bin", abs(int(native_count) - int(control_count)),
                   integer_count_tolerance(int(native_count), tolerances), component,
                   bin_index=bin_index, reference_count=int(native_count), candidate_count=int(control_count))
        record("outdegree_mean_difference", abs(native.outdegree_mean - control.outdegree_mean) / incoming_degree,
               tolerances["outdegree_difference_over_incoming_degree"], component)
    for source in range(5):
        for target in range(5):
            native_count = int(reference.directed_type_arcs[source, target])
            control_count = int(candidate.directed_type_arcs[source, target])
            record("directed_type_arc_count", abs(native_count - control_count),
                   integer_count_tolerance(native_count, tolerances), source,
                   target_component=target, reference_count=native_count, candidate_count=control_count)
    ratios = np.asarray([residual["ratio"] for residual in residuals])
    return {"local_matching_passed": all(residual["passed"] for residual in residuals),
            "residuals": residuals, "failed_constraint_count": int(np.sum(ratios > 1)),
            "maximum_ratio": float(ratios.max()),
            "unweighted_mean_squared_excess": float(np.mean(np.maximum(ratios - 1, 0)**2)),
            "local_matching_does_not_equal_complete_microstructure": True}


def admission(cache: SpectralMatchingCache, labels: np.ndarray, *,
              tolerances: dict | None = None, spectral_target: float = 0.5,
              features: LocalFeatures | None = None, amplitudes: np.ndarray | None = None,
              variance_guard_relative: float | None = None) -> dict:
    labels = cache.validate_labels(labels)
    features = cache.local_features(labels) if features is None else features
    if features.labels_hash != array_hash(labels):
        raise ValueError("Feature/mark mismatch")
    amplitudes = cache.amplitudes(labels) if amplitudes is None else amplitudes
    means = cache.structure_factors(amplitudes).mean(axis=1)
    if not np.isfinite(means).all() or spectral_target <= 0:
        raise ValueError("Spectral gate requires finite means and a positive target")
    local = compare_local_features(cache.native_features, features, tolerances=tolerances,
                                   incoming_degree=cache.incoming_degree,
                                   variance_guard_relative=variance_guard_relative)
    native = cache.structure_factors(cache.native_amplitudes)
    native_union = np.abs(cache.union_amplitude)**2 / cache.N
    native_valid = bool(np.all(native.mean(axis=1) <= .05) and np.all(native.max(axis=1) <= .10)
                        and native_union.mean() <= .05 and native_union.max() <= .10)
    spectral_valid = bool(np.all(means >= spectral_target))
    return {**local, "spectral_target": spectral_target, "component_means": means.tolist(),
            "component_maxima": cache.structure_factors(amplitudes).max(axis=1).tolist(),
            "spectral_manipulation_passed": spectral_valid,
            "native_component_and_union_certificate_passed": native_valid,
            "variance_guard_relative": variance_guard_relative,
            "admitted": bool(native_valid and local["local_matching_passed"] and spectral_valid),
            "conditioned_union_is_unchanged": True,
            "union_amplitude_hash": array_hash(cache.union_amplitude)}


def matching_energy(gate: dict, *, local_weight: float = 1.0,
                    spectral_weight: float = 1.0) -> float:
    """Sum normalized violations; admission always checks every exact gate."""
    if local_weight < 0 or spectral_weight < 0 or local_weight + spectral_weight == 0:
        raise ValueError("At least one nonnegative search weight must be positive")
    deficits = np.maximum(1 - np.asarray(gate["component_means"]) / gate["spectral_target"], 0)
    ratios = np.asarray([residual["ratio"] for residual in gate["residuals"]])
    return float(local_weight * np.sum(np.maximum(ratios - 1, 0)**2)
                 + spectral_weight * np.sum(deficits**2))


def bounded_swap_search(cache: SpectralMatchingCache, *, seed_keys: tuple[int, ...],
                        starts: tuple[str, ...], proposals_per_start: int,
                        maximum_seconds: float, initial_temperature: float,
                        final_temperature: float, local_weight: float = 1.0,
                        spectral_weight: float = 1.0, tolerances: dict | None = None,
                        spectral_target: float = 0.5,
                        near_probability: float = 0.8, nearest_destination_count: int = 4,
                        history_stride: int = 50,
                        maximum_seconds_per_start: float | None = None,
                        checkpoint: Callable[[dict, np.ndarray], None] | None = None,
                        variance_guard_relative: float | None = None,
                        absolute_deadline_ns: int | None = None,
                        start_seed_keys: tuple[tuple[int, ...], ...] | None = None,
                        trajectory_callback: Callable[[str, dict, np.ndarray], None] | None = None) -> dict:
    """Frozen starts, count-preserving swaps, and first fully admitted control.

    A failed bounded search is NOT_IDENTIFIED, never evidence that the
    underlying control is mathematically impossible. Best diagnostics do not
    become admitted controls. Deadline is additionally enforced by a parent
    process in scientific execution.
    """
    if not starts or any(start not in ("native", "fixed_count_shuffle") for start in starts):
        raise ValueError("Starts must be an explicit sequence of native/shuffle")
    if proposals_per_start < 0 or maximum_seconds <= 0:
        raise ValueError("Invalid explicit search budget")
    if initial_temperature <= 0 or final_temperature <= 0:
        raise ValueError("Annealing temperatures must be positive")
    if not 0 <= near_probability <= 1 or nearest_destination_count < 1 or history_stride < 1:
        raise ValueError("Invalid fixed proposal/history rule")
    if maximum_seconds_per_start is not None and maximum_seconds_per_start <= 0:
        raise ValueError("Per-start cap must be positive")
    started = time.perf_counter()
    deadline_ns = time.perf_counter_ns() + int(maximum_seconds * 1_000_000_000)
    if absolute_deadline_ns is not None:
        deadline_ns = min(deadline_ns, absolute_deadline_ns)
    if start_seed_keys is not None:
        if len(start_seed_keys) != len(starts):
            raise ValueError("Every trajectory requires its explicit seed keys")
        streams = [np.random.SeedSequence(keys) for keys in start_seed_keys]
    else:
        streams = np.random.SeedSequence(seed_keys).spawn(len(starts))
    attempts, best, admitted_labels, best_labels = [], None, None, None
    attempt_diagnostic_labels = []
    stop = "PROPOSAL_LIMIT"
    total_proposals = 0
    labels = np.array(cache.native_labels, copy=True)
    type_pairs = [(first, second) for first in range(5) for second in range(first + 1, 5)]
    for start_index, (start_kind, stream) in enumerate(zip(starts, streams)):
        if time.perf_counter_ns() >= deadline_ns:
            stop = "RESOURCE_LIMIT"
            break
        rng = np.random.default_rng(stream)
        start_deadline_ns = min(deadline_ns, time.perf_counter_ns() + int((maximum_seconds_per_start
                            if maximum_seconds_per_start is not None else maximum_seconds) * 1_000_000_000))
        if trajectory_callback is not None:
            trajectory_callback("START", {"start_index": start_index, "deadline_ns": start_deadline_ns,
                "started_ns": time.perf_counter_ns()}, cache.native_labels)
        attempt_stop = "PROPOSAL_LIMIT"
        labels = np.array(cache.native_labels, copy=True)
        if start_kind == "fixed_count_shuffle":
            labels = rng.permutation(labels)
        features, amplitudes = cache.local_features(labels), cache.amplitudes(labels)
        initial_labels_hash = array_hash(labels)
        gate = admission(cache, labels, tolerances=tolerances, spectral_target=spectral_target,
                         features=features, amplitudes=amplitudes, variance_guard_relative=variance_guard_relative)
        energy = matching_energy(gate, local_weight=local_weight, spectral_weight=spectral_weight)
        initial_gate = gate
        attempt_best = {"energy": energy, "gate": gate, "labels_hash": array_hash(labels), "proposal": 0}
        attempt_best_labels = labels.copy()
        accepted, performed = 0, 0
        accepted_moves, history = [], []
        for proposal in range(proposals_per_start + 1):
            # This checks the initial start too; no admitted start is discarded.
            record = {"start_index": start_index, "start_kind": start_kind,
                      "proposals": performed, "energy": energy, "gate": gate,
                      "labels_hash": array_hash(labels)}
            if best is None or energy < best["energy"]:
                best = record
                best_labels = labels.copy()
            if performed % history_stride == 0 or performed == proposals_per_start or gate["admitted"]:
                history.append(record)
            if gate["admitted"]:
                verified_gate = admission(cache, labels, tolerances=tolerances, spectral_target=spectral_target,
                                          variance_guard_relative=variance_guard_relative)
                if not verified_gate["admitted"]:
                    raise RuntimeError("Incremental admission did not survive full recomputation")
                gate = verified_gate
                admitted_labels = labels.copy()
                stop = "FIRST_ADMITTED"
                attempt_stop = stop
                break
            if proposal == proposals_per_start:
                break
            if time.perf_counter_ns() >= start_deadline_ns:
                attempt_stop = "START_RESOURCE_LIMIT"
                if time.perf_counter_ns() >= deadline_ns:
                    stop = "RESOURCE_LIMIT"
                break
            source_type, destination_type = type_pairs[int(rng.integers(len(type_pairs)))]
            # Reverse direction randomly: the sorted pair ordering is not a bias.
            if rng.random() < .5:
                source_type, destination_type = destination_type, source_type
            first = int(rng.choice(np.flatnonzero(labels == source_type)))
            eligible = np.flatnonzero(labels == destination_type)
            if rng.random() < near_probability:
                order = np.lexsort((eligible, cache.point_distances[first, eligible]))
                eligible = eligible[order[:nearest_destination_count]]
            second = int(rng.choice(eligible))
            a, b = int(labels[first]), int(labels[second])
            candidate = labels.copy()
            candidate[first], candidate[second] = candidate[second], candidate[first]
            candidate_amplitudes = cache.swapped_amplitudes(amplitudes, labels, first, second)
            candidate_features = cache.local_features(candidate, previous=features, changed_types=(a, b))
            candidate_gate = admission(cache, candidate, tolerances=tolerances, spectral_target=spectral_target,
                                       features=candidate_features, amplitudes=candidate_amplitudes,
                                       variance_guard_relative=variance_guard_relative)
            candidate_energy = matching_energy(candidate_gate, local_weight=local_weight,
                                               spectral_weight=spectral_weight)
            if candidate_energy < attempt_best["energy"]:
                attempt_best = {"energy": candidate_energy, "gate": candidate_gate,
                                "labels_hash": array_hash(candidate), "proposal": performed + 1}
                attempt_best_labels = candidate.copy()
            fraction = proposal / max(1, proposals_per_start - 1)
            temperature = initial_temperature * (final_temperature / initial_temperature)**fraction
            accept = candidate_energy <= energy or rng.random() < math.exp(min(0.0, (energy - candidate_energy) / temperature))
            total_proposals += 1
            performed += 1
            if best is None or candidate_energy < best["energy"]:
                best = {"start_index": start_index, "start_kind": start_kind, "proposals": performed,
                        "energy": candidate_energy, "gate": candidate_gate, "labels_hash": array_hash(candidate)}
                best_labels = candidate.copy()
            # Admission wins immediately even if a numerical energy is higher.
            if accept or candidate_gate["admitted"]:
                labels, amplitudes, features, gate, energy = (candidate, candidate_amplitudes,
                                                              candidate_features, candidate_gate, candidate_energy)
                accepted += 1
                accepted_moves.append({"proposal": performed, "first": first, "second": second,
                                       "source_type": a, "destination_type": b,
                                       "energy": energy, "labels_hash": array_hash(labels)})
            if checkpoint is not None and performed % history_stride == 0:
                checkpoint({"status": "SEARCHING", "total_proposals": total_proposals,
                            "start_index": start_index, "last_gate": gate,
                            "best": best, "wall_seconds": time.perf_counter() - started}, labels)
        attempt = {"start_index": start_index, "start_kind": start_kind,
                   "seed_keys": list(start_seed_keys[start_index]) if start_seed_keys is not None else list(seed_keys),
                   "seed_spawn_key": list(stream.spawn_key), "initial_labels_hash": initial_labels_hash,
                   "initial_gate": initial_gate, "proposals": performed, "accepted_swaps": accepted,
                   "stop_reason": attempt_stop,
                   "last_labels_hash": array_hash(labels), "last_energy": energy, "last_gate": gate,
                   "best_diagnostic": attempt_best,
                   "accepted_moves": accepted_moves, "history": history}
        attempt_diagnostic_labels.append(attempt_best_labels)
        if trajectory_callback is not None:
            trajectory_callback("END", attempt, admitted_labels if admitted_labels is not None else attempt_best_labels)
        attempts.append(attempt)
        if admitted_labels is not None or stop == "RESOURCE_LIMIT":
            break
    if admitted_labels is not None:
        # Direct admission uses rho summation and all local metrics,
        # discarding the incremental search cache as authority.
        verified = admission(cache, admitted_labels, tolerances=tolerances, spectral_target=spectral_target,
                             variance_guard_relative=variance_guard_relative)
        if not verified["admitted"]:
            raise RuntimeError("Incremental admission did not survive full recomputation")
        for skipped in range(len(attempts), len(starts)):
            attempts.append({"start_index": skipped, "start_kind": starts[skipped],
                             "status": "NOT_RUN_ALREADY_ADMITTED", "proposals": 0})
    if admitted_labels is None:
        for skipped in range(len(attempts), len(starts)):
            attempts.append({"start_index": skipped, "start_kind": starts[skipped],
                             "status": "NOT_RUN_RESOURCE_LIMIT", "proposals": 0})
    final = {"version": VERSION,
             "status": "ADMITTED" if admitted_labels is not None else "NOT_IDENTIFIED",
             "stop_reason": stop, "attempts": attempts, "total_proposals": total_proposals,
             "best_diagnostic": best, "wall_seconds": time.perf_counter() - started,
             "best_diagnostic_labels": best_labels,
             "attempt_diagnostic_labels": attempt_diagnostic_labels,
             "admitted_labels": admitted_labels, "admitted_labels_hash": (
                 array_hash(admitted_labels) if admitted_labels is not None else None),
             "neural_or_field_scores_used": False,
             "search_failure_is_not_mathematical_impossibility": True}
    if checkpoint is not None:
        checkpoint({key: value for key, value in final.items() if key not in ("admitted_labels", "best_diagnostic_labels", "attempt_diagnostic_labels")},
                   admitted_labels if admitted_labels is not None else labels)
    return final


def source_identity() -> dict:
    files = {"src/larp/spectral_matching.py": file_hash(Path(__file__)),
             "src/larp/geometry.py": file_hash(ROOT / "src/larp/geometry.py"),
             "src/larp/graphs.py": file_hash(ROOT / "src/larp/graphs.py"),
             "src/larp/artifacts.py": file_hash(ROOT / "src/larp/artifacts.py")}
    return {"files": files, "hash": digest(files)}
