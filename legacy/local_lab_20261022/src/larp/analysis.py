"""Preregistered paired inference, with geometry as the replication unit.

Implements review L, lines 389--403.  ``sigma_initialization`` is the
within-geometry residual variance in that equation; it is not a crossed seed
random effect.  No architecture belief is inferred from smoke/unit tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import brentq
from scipy.special import logsumexp, ndtr
from scipy.stats import norm


H_MARGINAL_PRIORS = {
    "H1": 0.70, "H2": 0.35, "H3": 0.25,
    "H4": 0.75, "H5": 0.20, "H6": 0.30,
}
GRADES = ("strong_against", "weak_against", "neutral", "weak_for", "strong_for")
SUBJECTIVE_LR = dict(zip(GRADES, (0.2, 0.5, 1.0, 2.0, 5.0)))
SUBJECTIVE_LR_SENSITIVITY = dict(zip(GRADES, (1 / 3, 2 / 3, 1.0, 1.5, 3.0)))
PAIR_HASH_KEYS = (
    "coordinates", "edges", "ports", "data_train", "data_validation", "data_test",
    "optimizer", "budget", "shared_initialization",
)
_EVIDENCE_STAGES = frozenset(("confirmation", "robustness"))


def _effects(deltas: ArrayLike) -> NDArray[np.float64]:
    values = np.asarray(deltas, dtype=np.float64)
    if values.ndim != 2 or values.shape[0] < 2 or values.shape[1] < 2:
        raise ValueError("Expected at least two geometries and two paired initializations, G x S.")
    if not np.all(np.isfinite(values)):
        raise ValueError("Effects must be finite; reproducible divergence needs system score zero.")
    if np.any(np.abs(values) > 1):
        raise ValueError("Primary score differences must be within [-1, 1].")
    return values


def paired_differences(native: ArrayLike, control: ArrayLike) -> NDArray[np.float64]:
    """Difference of scores already aggregated within geometry/init, never bits."""
    native_array = np.asarray(native, dtype=np.float64)
    control_array = np.asarray(control, dtype=np.float64)
    if native_array.shape != control_array.shape:
        raise ValueError("Native and control scores must have identical paired shapes.")
    for scores in (native_array, control_array):
        if not np.all(np.isfinite(scores)) or np.any((scores < 0) | (scores > 1)):
            raise ValueError("Primary system scores must be finite and in [0, 1].")
    return _effects(native_array - control_array)


@dataclass(frozen=True)
class EffectPosterior:
    """Gaussian-mixture posterior of mu after integrating both random effects."""

    weights: NDArray[np.float64]
    component_means: NDArray[np.float64]
    component_variances: NDArray[np.float64]
    sigma_geometry: NDArray[np.float64]
    sigma_initialization: NDArray[np.float64]
    log_evidence: float
    mu_prior_std: float
    sigma_prior_std: float
    sigma_bounds: tuple[float, float]
    quadrature_nodes: int
    geometries: int
    initializations_per_geometry: int
    exact_within_geometry_ties: bool

    def cdf(self, value: float) -> float:
        scales = np.sqrt(self.component_variances)
        return float(np.dot(self.weights, ndtr((value - self.component_means) / scales)))

    def quantile(self, probability: float) -> float:
        if not 0 < probability < 1:
            raise ValueError("Quantile probability must be strictly between zero and one.")
        scales = np.sqrt(self.component_variances)
        # A mixture quantile lies between the smallest/largest component quantile.
        candidates = self.component_means + norm.ppf(probability) * scales
        lower, upper = float(np.min(candidates)), float(np.max(candidates))
        if lower == upper:
            return lower
        return float(brentq(lambda value: self.cdf(value) - probability, lower, upper, xtol=1e-12))

    def probability_above(self, value: float) -> float:
        return float(np.dot(self.weights, ndtr(
            (self.component_means - value) / np.sqrt(self.component_variances))))

    def summary(self, rope: float = 0.02) -> dict[str, Any]:
        if not np.isfinite(rope) or rope <= 0:
            raise ValueError("ROPE half-width must be positive and finite.")
        mean = float(np.dot(self.weights, self.component_means))
        variance = float(np.dot(
            self.weights, self.component_variances + (self.component_means - mean) ** 2))
        p_positive = self.probability_above(rope)
        p_negative = self.cdf(-rope)
        p_rope = float(np.clip(1.0 - p_positive - p_negative, 0.0, 1.0))
        return {
            "mean": mean, "median": self.quantile(0.5), "std": float(np.sqrt(variance)),
            "credible_interval_95": [self.quantile(0.025), self.quantile(0.975)],
            "probability_positive": p_positive, "probability_rope": p_rope,
            "probability_negative": p_negative,
            "probability_noninferior": self.probability_above(-rope), "rope": [-rope, rope],
            "sigma_geometry_mean": float(np.dot(self.weights, self.sigma_geometry)),
            "sigma_initialization_mean": float(np.dot(self.weights, self.sigma_initialization)),
            "log_evidence": self.log_evidence,
            "mu_prior_std": self.mu_prior_std, "sigma_prior_std": self.sigma_prior_std,
            "sigma_bounds": list(self.sigma_bounds), "quadrature_nodes": self.quadrature_nodes,
            "geometries": self.geometries,
            "initializations_per_geometry": self.initializations_per_geometry,
            "replication_unit": "geometry",
            "model": "delta[g,s] = mu + b[g] + epsilon[g,s]",
            "sigma_prior_integrated": "HalfNormal normalized on stated numerical interval",
            "exact_within_geometry_ties": self.exact_within_geometry_ties,
        }


def infer_paired_effect(
    deltas: ArrayLike, *, mu_prior_std: float = 0.05, sigma_prior_std: float = 0.05,
    sigma_bounds: tuple[float, float] = (1e-6, 0.25), quadrature_nodes: int = 96,
) -> EffectPosterior:
    """Integrate mu and geometry effects analytically, sigmas by Gauss-Legendre.

    Given sigmas, each group has covariance sigma_s**2 I + sigma_g**2 11'.
    Its mean variance is sigma_g**2 + sigma_s**2 / S.  The normal prior of mu
    is integrated exactly, including its determinant factor.  Quadrature
    density uses the half-normal prior normalized on the declared interval;
    comparison with the extended interval is required before a decision.
    """
    values = _effects(deltas)
    if not np.isfinite(mu_prior_std) or mu_prior_std <= 0:
        raise ValueError("mu_prior_std must be positive and finite.")
    if not np.isfinite(sigma_prior_std) or sigma_prior_std <= 0:
        raise ValueError("sigma_prior_std must be positive and finite.")
    lower, upper = map(float, sigma_bounds)
    if not 0 < lower < upper or not np.isfinite(upper):
        raise ValueError("Expected positive, ordered finite sigma integration bounds.")
    if isinstance(quadrature_nodes, bool) or int(quadrature_nodes) != quadrature_nodes or quadrature_nodes < 8:
        raise ValueError("quadrature_nodes must be an integer of at least eight.")
    geometries, initializations = values.shape
    group_means = values.mean(axis=1)
    within_sum_squares = float(np.sum((values - group_means[:, None]) ** 2))
    nodes, weights = np.polynomial.legendre.leggauss(int(quadrature_nodes))
    sigma = lower + (nodes + 1) * (upper - lower) / 2
    integration_weights = weights * (upper - lower) / 2
    sigma_geometry, sigma_initialization = np.meshgrid(sigma, sigma, indexing="ij")
    sigma_g2, sigma_s2 = sigma_geometry ** 2, sigma_initialization ** 2
    group_variance = sigma_g2 + sigma_s2 / initializations
    precision = 1 / mu_prior_std ** 2 + geometries / group_variance
    variance_mu = 1 / precision
    linear = float(np.sum(group_means)) / group_variance
    mean_mu = linear * variance_mu
    # Determinant for G groups of S correlated observations.
    log_determinant = geometries * (
        (initializations - 1) * np.log(sigma_s2)
        + np.log(sigma_s2 + initializations * sigma_g2))
    quadratic = within_sum_squares / sigma_s2 + float(np.sum(group_means ** 2)) / group_variance
    log_marginal = -0.5 * (values.size * np.log(2 * np.pi) + log_determinant + quadratic)
    log_marginal += 0.5 * np.log(variance_mu / mu_prior_std ** 2) + 0.5 * linear ** 2 * variance_mu
    prior_mass = 2 * (ndtr(upper / sigma_prior_std) - ndtr(lower / sigma_prior_std))
    if prior_mass <= 0:
        raise ValueError("Sigma bounds have zero numerical prior mass.")
    log_halfnormal = (np.log(np.sqrt(2 / np.pi) / sigma_prior_std) - np.log(prior_mass)
                      - 0.5 * (sigma / sigma_prior_std) ** 2)
    log_weights = (log_marginal + log_halfnormal[:, None] + log_halfnormal[None, :]
                   + np.log(integration_weights)[:, None] + np.log(integration_weights)[None, :])
    log_evidence = float(logsumexp(log_weights))
    normalized = np.exp(log_weights - log_evidence)
    normalized /= normalized.sum()
    return EffectPosterior(
        normalized.ravel(), mean_mu.ravel(), variance_mu.ravel(),
        sigma_geometry.ravel(), sigma_initialization.ravel(), log_evidence,
        mu_prior_std, sigma_prior_std, (lower, upper), int(quadrature_nodes),
        geometries, initializations, within_sum_squares == 0,
    )


def bootstrap_geometry(
    deltas: ArrayLike, *, seed: int = 20261008, samples: int = 10000,
) -> dict[str, Any]:
    """Percentile sensitivity check: resample complete geometry clusters."""
    values = _effects(deltas)
    if isinstance(samples, bool) or int(samples) != samples or samples < 100:
        raise ValueError("At least 100 integer bootstrap samples are required.")
    means = values.mean(axis=1)
    rng = np.random.default_rng(seed)
    resampled = rng.integers(0, len(means), size=(int(samples), len(means)))
    bootstrap_means = means[resampled].mean(axis=1)
    return {
        "mean": float(means.mean()),
        "percentile_interval_95": np.quantile(bootstrap_means, [0.025, 0.975]).tolist(),
        "std": float(np.std(bootstrap_means, ddof=1)), "seed": int(seed),
        "samples": int(samples), "replication_unit": "geometry",
        "geometries": len(means), "not_a_bayesian_posterior": True,
    }


def _decision(summary: Mapping[str, Any]) -> str:
    if summary["probability_positive"] >= 0.95:
        return "positive_practical_effect"
    if summary["probability_negative"] >= 0.95:
        return "negative_practical_effect"
    if summary["probability_rope"] >= 0.90:
        return "within_rope"
    return "inconclusive"


def analyze_paired_effect(
    deltas: ArrayLike, *, evidence_stage: str = "synthetic", bootstrap_seed: int = 20261008,
    bootstrap_samples: int = 10000,
) -> dict[str, Any]:
    """Return numerical diagnostics; never updates H1--H6 automatically.

    ``synthetic`` is allowed solely to test inference.  Only confirmed paired
    data may be architecture evidence.  The record-level wrapper additionally
    checks the pairing manifest and preregistration.
    """
    if evidence_stage not in _EVIDENCE_STAGES | {"synthetic"}:
        raise ValueError("Unit tests, calibration, smoke, pilot selection and screen are not architecture evidence.")
    values = _effects(deltas)
    base = infer_paired_effect(values)
    validated = infer_paired_effect(values, quadrature_nodes=192)
    summary, validation_summary = base.summary(), validated.summary()
    sensitivity = {
        str(std): infer_paired_effect(values, mu_prior_std=std, quadrature_nodes=192).summary()
        for std in (0.02, 0.10)
    }
    # Twice as many nodes preserves local node spacing when doubling the upper bound.
    extended = infer_paired_effect(values, sigma_bounds=(1e-6, 0.50), quadrature_nodes=384)
    extended_summary = extended.summary()
    tail_mass = float(np.sum(extended.weights[
        (extended.sigma_geometry > 0.25) | (extended.sigma_initialization > 0.25)]))
    diagnostic_keys = ("mean", "std", "probability_positive", "probability_rope", "probability_negative")
    quadrature_difference = max(abs(summary[key] - validation_summary[key]) for key in diagnostic_keys)
    interval_difference = max(abs(a - b) for a, b in zip(
        summary["credible_interval_95"], validation_summary["credible_interval_95"]))
    log_evidence_difference = abs(base.log_evidence - validated.log_evidence)
    # These numerical tolerances are engineering error controls, not new effect thresholds.
    numerical_ok = quadrature_difference <= 0.001 and interval_difference <= 0.0001 and log_evidence_difference <= 0.01
    tail_ok = tail_mass <= 0.0001
    prior_decisions = {_decision(validation_summary)} | {_decision(value) for value in sensitivity.values()}
    bootstrap = bootstrap_geometry(values, seed=bootstrap_seed, samples=bootstrap_samples)
    bootstrap_low, bootstrap_high = bootstrap["percentile_interval_95"]
    posterior_decision = _decision(validation_summary)
    bootstrap_disagreement = (
        (posterior_decision == "positive_practical_effect" and bootstrap_low <= 0.02)
        or (posterior_decision == "negative_practical_effect" and bootstrap_high >= -0.02)
        or (posterior_decision == "within_rope" and (bootstrap_low < -0.02 or bootstrap_high > 0.02))
    )
    sensitivity_ok = len(prior_decisions) == 1 and not bootstrap_disagreement
    # Exact tied repeats can put the continuous residual model at a singular boundary.
    boundary_ok = not base.exact_within_geometry_ties
    numerical_decision_eligible = evidence_stage in _EVIDENCE_STAGES and numerical_ok and tail_ok and sensitivity_ok and boundary_ok
    return {
        "evidence_stage": evidence_stage, "posterior": summary,
        "quadrature_192": validation_summary, "mu_prior_sensitivity": sensitivity,
        "extended_sigma_interval": extended_summary, "posterior_tail_mass_above_0_25": tail_mass,
        "quadrature_max_summary_difference": quadrature_difference,
        "quadrature_max_interval_difference": interval_difference,
        "quadrature_log_evidence_difference": log_evidence_difference,
        "quadrature_converged": numerical_ok, "tail_negligible": tail_ok,
        "bootstrap": bootstrap, "bootstrap_disagreement": bootstrap_disagreement,
        "prior_decision_sensitive": len(prior_decisions) != 1,
        "continuous_model_boundary_sensitive": not boundary_ok,
        "effect_classification": posterior_decision,
        "numerically_decision_eligible": numerical_decision_eligible,
        # Raw matrices carry no seed identities or frozen expected replication
        # manifest. Only analyze_records can attest a completed preregistration.
        "architecture_decision_eligible": False,
        "architecture_beliefs_updated": False, "H_marginal_priors": dict(H_MARGINAL_PRIORS),
        "scope_warning": "One task effect is not the multi-task stop/pivot/continue decision.",
    }


def initial_beliefs() -> dict[str, Any]:
    """Persistable AB initialization. Priors are marginal, not normalized."""
    return {
        "status": "UNUPDATED", "architecture_evidence": [], "mutually_exclusive": False,
        "hypotheses": {name: {"prior": prior, "posterior": prior, "status": "UNUPDATED"}
                       for name, prior in H_MARGINAL_PRIORS.items()},
        "architecture_effect_prior": {"distribution": "Normal", "mean": 0.0, "std": 0.05},
        "sigma_priors": {"distribution": "HalfNormal", "std": 0.05},
        "mechanism_prior": 0.25, "rope": [-0.02, 0.02],
        "note": "Technical tests, certificates, calibration and smoke do not update architecture beliefs.",
    }


def subjective_hypothesis_update(
    hypothesis: str, grade: str, *, evidence_stage: str, evidence_id: str,
    prior: float | None = None,
) -> dict[str, Any]:
    """Explicit illustrative odds update, labeled subjective rather than a Bayes factor."""
    if hypothesis not in H_MARGINAL_PRIORS or grade not in GRADES:
        raise ValueError("Unknown hypothesis or qualitative grade.")
    if evidence_stage not in _EVIDENCE_STAGES | {"plasticity"} or not evidence_id:
        raise ValueError("A confirmed, identified evidence package is required.")
    if hypothesis == "H5" and evidence_stage != "plasticity":
        raise ValueError("H5 remains unupdated until plasticity and warm-start evidence.")
    probability = H_MARGINAL_PRIORS[hypothesis] if prior is None else float(prior)
    if not 0 < probability < 1:
        raise ValueError("Prior probability must be strictly between zero and one.")
    def apply(likelihood_ratio: float) -> float:
        return probability * likelihood_ratio / (1 - probability + probability * likelihood_ratio)
    return {
        "hypothesis": hypothesis, "prior": probability, "grade": grade,
        "evidence_stage": evidence_stage, "evidence_id": evidence_id,
        "subjective_LR": SUBJECTIVE_LR[grade], "posterior_illustrative": apply(SUBJECTIVE_LR[grade]),
        "sensitivity_LR": SUBJECTIVE_LR_SENSITIVITY[grade],
        "posterior_sensitivity": apply(SUBJECTIVE_LR_SENSITIVITY[grade]),
        "is_estimated_Bayes_factor": False,
        "warning": "Elicited subjective odds update; correlated diagnostics form one evidence package.",
    }


def analyze_records(
    records: Iterable[Mapping[str, Any]], *, native_condition: str = "native",
    control_condition: str = "shuffle", bootstrap_seed: int = 20261008,
    estimand: str = "marks",
    expected_geometry_seeds: Iterable[int] | None = None,
    expected_training_seeds: Iterable[int] | None = None,
) -> dict[str, Any]:
    """Guarded analysis of complete, paired confirmation/robustness manifests.

    One record per condition, geometry and training seed is required. All hash
    fields listed in PAIR_HASH_KEYS must match within each pair. Dataset and
    architecture identifiers must be constant across the analysis. A manifest
    attests that selection and preregistration were frozen before its test.
    Missing/infrastructure/invalid runs stop analysis. Completed scores must be
    test endpoints (confirmation additionally attests ``test_opened=True``).
    Divergence contributes score 0 only after explicit reproducibility and
    infrastructure-exclusion verification, as required by review L.
    Expected seed lists may be supplied as arguments or identically embedded
    in every record. A complete frozen replication manifest is required for
    architecture-decision eligibility. Without it, numerical inference is
    explicitly descriptive and cannot treat a partial panel as completion.
    """
    if estimand not in ("marks", "architecture"):
        raise ValueError("Choose the marks or complete-architecture estimand explicitly.")
    rows = list(records)
    if not rows:
        raise ValueError("No records supplied.")
    stages = {row.get("stage") for row in rows}
    if len(stages) != 1 or not stages <= _EVIDENCE_STAGES:
        raise ValueError("Only a single confirmation or robustness phase may provide architecture evidence.")
    if any(row.get("preregistered") is not True for row in rows):
        raise ValueError("Frozen preregistration is required before test analysis.")
    keyed: dict[tuple[int, int, str], Mapping[str, Any]] = {}
    for row in rows:
        condition = str(row.get("condition"))
        if condition not in (native_condition, control_condition):
            raise ValueError("Do not silently select a comparison from unrelated conditions.")
        key = (int(row["geometry_seed"]), int(row["training_seed"]), condition)
        if key in keyed:
            raise ValueError("Duplicate run: maps/masks/repeated evaluations are not architecture replicates.")
        keyed[key] = row
    geometries = sorted({key[0] for key in keyed})
    training_seeds = sorted({key[1] for key in keyed})
    def expected_seeds(field: str, supplied: Iterable[int] | None) -> list[int] | None:
        def canonical(seeds: Iterable[int]) -> list[int]:
            entries = list(seeds)
            if not entries or any(isinstance(seed, (bool, np.bool_)) or int(seed) != seed for seed in entries):
                raise ValueError(f"{field} must be a nonempty sequence of integer seed identities.")
            if len(set(entries)) != len(entries):
                raise ValueError(f"Duplicate seed in {field} preregistration.")
            return sorted(int(seed) for seed in entries)
        explicit = canonical(supplied) if supplied is not None else None
        embedded = [row.get(field) for row in rows]
        if any(value is not None for value in embedded):
            if any(value is None for value in embedded):
                raise ValueError(f"Expected replication manifest missing {field} in some records.")
            canonical_embedded = [canonical(value) for value in embedded]
            if any(value != canonical_embedded[0] for value in canonical_embedded[1:]):
                raise ValueError(f"Conflicting frozen replication manifests: {field}.")
            if explicit is not None and explicit != canonical_embedded[0]:
                raise ValueError(f"Supplied and embedded replication manifests disagree: {field}.")
            return canonical_embedded[0]
        return explicit
    expected_geometries = expected_seeds("expected_geometry_seeds", expected_geometry_seeds)
    expected_initializations = expected_seeds("expected_training_seeds", expected_training_seeds)
    if expected_geometries is not None and geometries != expected_geometries:
        raise ValueError("Incomplete or unexpected geometry seed panel relative to frozen preregistration.")
    if expected_initializations is not None and training_seeds != expected_initializations:
        raise ValueError("Incomplete or unexpected training seed panel relative to frozen preregistration.")
    replication_manifest_complete = expected_geometries is not None and expected_initializations is not None
    confirmation_design_conforms = (
        next(iter(stages)) != "confirmation"
        or (len(geometries) in (8, 16) and len(training_seeds) == 2)
    )
    native_scores = np.empty((len(geometries), len(training_seeds)), dtype=np.float64)
    control_scores = np.empty_like(native_scores)
    divergence_count = 0
    for gi, geometry in enumerate(geometries):
        for si, training_seed in enumerate(training_seeds):
            try:
                pair = [keyed[(geometry, training_seed, condition)]
                        for condition in (native_condition, control_condition)]
            except KeyError as error:
                raise ValueError("Incomplete paired geometry/init panel; resume the same seed.") from error
            checked_hash_keys = PAIR_HASH_KEYS if estimand == "marks" else PAIR_HASH_KEYS[3:]
            for field in checked_hash_keys:
                pair_hashes = [row.get("pair_hashes", {}) for row in pair]
                if not pair_hashes[0].get(field) or pair_hashes[0].get(field) != pair_hashes[1].get(field):
                    raise ValueError(f"Causal pairing mismatch or missing manifest field: {field}.")
            if estimand == "marks" and (
                pair[0].get("labels_hash") == pair[1].get("labels_hash")
                or any(not row.get("labels_hash") for row in pair)
            ):
                raise ValueError("Native and shuffle must have independently audited mark assignments.")
            for ci, row in enumerate(pair):
                status = row.get("status")
                if status == "TRAINING_DIVERGENCE":
                    if row.get("divergence_verified") is not True or row.get("infrastructure_excluded") is not True:
                        raise ValueError("Scientific divergence must be reproducibly verified with infrastructure excluded.")
                    score = 0.0
                    divergence_count += 1
                elif status == "COMPLETE":
                    if row.get("score_split") != "test" or (
                        row.get("stage") == "confirmation" and row.get("test_opened") is not True
                    ):
                        raise ValueError("Completed architecture evidence requires the frozen test endpoint, not validation.")
                    score = float(row["score"])
                else:
                    raise ValueError("Unfinished, infrastructure or invalid runs must not become architecture evidence.")
                (native_scores if ci == 0 else control_scores)[gi, si] = score
    for field in ("task", "variant", "data_train", "data_validation", "data_test", "budget", "optimizer"):
        identifiers = {
            row.get(field) if field in ("task", "variant") else row.get("pair_hashes", {}).get(field)
            for row in rows
        }
        if len(identifiers) != 1 or None in identifiers:
            raise ValueError(f"Analyze a single fixed task, model and budget; inconsistent {field}.")
    analysis = analyze_paired_effect(
        paired_differences(native_scores, control_scores),
        evidence_stage=next(iter(stages)), bootstrap_seed=bootstrap_seed)
    analysis.update({
        "geometry_seeds": geometries, "training_seeds": training_seeds,
        "native_scores": native_scores.tolist(), "control_scores": control_scores.tolist(),
        "divergence_count": divergence_count, "system_failure_rate": divergence_count / len(rows),
        "condition_native": native_condition, "condition_control": control_condition,
        "task": rows[0]["task"], "variant": rows[0]["variant"], "estimand": estimand,
        "pair_hash_fields_checked": list(checked_hash_keys),
        "expected_geometry_seeds": expected_geometries,
        "expected_training_seeds": expected_initializations,
        "replication_manifest_complete": replication_manifest_complete,
        "confirmation_design_conforms": confirmation_design_conforms,
        "architecture_decision_eligible": bool(
            analysis.get("numerically_decision_eligible", False)
            and replication_manifest_complete and confirmation_design_conforms
        ),
    })
    return analysis
