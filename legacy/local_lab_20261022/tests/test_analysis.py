"""Statistical checks use synthetic data, never architecture evidence."""

import copy

import numpy as np
import pytest
from scipy.linalg import block_diag
from scipy.special import logsumexp, ndtr
from scipy.stats import multivariate_normal

from larp.analysis import (
    H_MARGINAL_PRIORS, PAIR_HASH_KEYS, analyze_paired_effect, analyze_records,
    bootstrap_geometry, infer_paired_effect, initial_beliefs, paired_differences,
    subjective_hypothesis_update,
)


def synthetic_effects(effect=0.0):
    # Paired initializations are centered within each geometry; independent
    # geometry effects remain the principal replication unit.
    geometry_effects = np.array([-0.010, -0.007, -0.004, -0.001, 0.001, 0.004, 0.007, 0.010])
    residuals = np.array([-0.004, 0.004])
    return effect + geometry_effects[:, None] + residuals[None, :]


def test_analytic_marginalization_matches_dense_gaussian_reference():
    deltas = np.array([[0.018, 0.028], [-0.010, -0.020]])
    posterior = infer_paired_effect(deltas, quadrature_nodes=8)
    means, variances, log_reference = [], [], []
    nodes, weights = np.polynomial.legendre.leggauss(8)
    lower, upper = posterior.sigma_bounds
    sigma = lower + (nodes + 1) * (upper - lower) / 2
    integration_weights = weights * (upper - lower) / 2
    normalization = 2 * (ndtr(upper / 0.05) - ndtr(lower / 0.05))
    halfnormal = np.sqrt(2 / np.pi) / 0.05 * np.exp(-0.5 * (sigma / 0.05) ** 2) / normalization
    ones, y = np.ones(deltas.size), deltas.ravel()
    for gi, sigma_g in enumerate(sigma):
        for si, sigma_s in enumerate(sigma):
            group_covariance = sigma_s ** 2 * np.eye(2) + sigma_g ** 2 * np.ones((2, 2))
            conditional_covariance = block_diag(group_covariance, group_covariance)
            inverse = np.linalg.inv(conditional_covariance)
            variance = 1 / (1 / 0.05 ** 2 + ones @ inverse @ ones)
            means.append(variance * (ones @ inverse @ y))
            variances.append(variance)
            marginal_covariance = conditional_covariance + 0.05 ** 2 * np.ones((4, 4))
            density = multivariate_normal.logpdf(y, mean=np.zeros(4), cov=marginal_covariance)
            log_reference.append(density + np.log(halfnormal[gi] * halfnormal[si])
                                 + np.log(integration_weights[gi] * integration_weights[si]))
    np.testing.assert_allclose(posterior.component_means, means, rtol=1e-9, atol=1e-12)
    np.testing.assert_allclose(posterior.component_variances, variances, rtol=1e-9, atol=1e-12)
    normalization_reference = logsumexp(log_reference)
    np.testing.assert_allclose(posterior.weights, np.exp(log_reference - normalization_reference), rtol=1e-9)
    assert posterior.log_evidence == pytest.approx(normalization_reference, abs=1e-10)


@pytest.mark.parametrize("effect,expected", [(0.0, "null"), (0.075, "positive"), (-0.075, "negative")])
def test_null_positive_negative_and_quadrature_sensitivity(effect, expected):
    values = synthetic_effects(effect)
    summary = infer_paired_effect(values).summary()
    fine = infer_paired_effect(values, quadrature_nodes=192).summary()
    assert summary["mean"] == pytest.approx(fine["mean"], abs=1e-7)
    assert summary["credible_interval_95"] == pytest.approx(fine["credible_interval_95"], abs=1e-6)
    for name in ("probability_positive", "probability_negative", "probability_rope"):
        assert summary[name] == pytest.approx(fine[name], abs=1e-6)
    assert sum(summary[name] for name in ("probability_positive", "probability_negative", "probability_rope")) == pytest.approx(1)
    assert summary["geometries"] == 8
    assert summary["initializations_per_geometry"] == 2
    if expected == "null":
        assert summary["probability_rope"] > 0.90
        assert abs(summary["mean"]) < 1e-12
    elif expected == "positive":
        assert summary["probability_positive"] > 0.95
    else:
        assert summary["probability_negative"] > 0.95


def test_sign_symmetry_including_intervals():
    positive = infer_paired_effect(synthetic_effects(0.05)).summary()
    negative = infer_paired_effect(-synthetic_effects(0.05)).summary()
    assert positive["mean"] == pytest.approx(-negative["mean"], abs=1e-12)
    assert positive["probability_positive"] == pytest.approx(negative["probability_negative"], abs=1e-12)
    assert positive["credible_interval_95"] == pytest.approx([-x for x in reversed(negative["credible_interval_95"])], abs=1e-10)


def test_geometry_not_initialization_is_bootstrap_unit():
    values = synthetic_effects()
    result = bootstrap_geometry(values, seed=73, samples=1000)
    rng = np.random.default_rng(73)
    group_means = values.mean(axis=1)
    reference = group_means[rng.integers(0, 8, (1000, 8))].mean(axis=1)
    assert result["percentile_interval_95"] == pytest.approx(np.quantile(reference, [0.025, 0.975]))
    repeated = bootstrap_geometry(np.repeat(values, 4, axis=1), seed=73, samples=1000)
    assert result["percentile_interval_95"] == pytest.approx(repeated["percentile_interval_95"])
    assert result["replication_unit"] == "geometry"
    assert result["not_a_bayesian_posterior"] is True


@pytest.mark.parametrize("invalid", [np.zeros((1, 2)), np.zeros((8, 1)), np.zeros(16), [[np.nan, 0], [0, 0]], [[2, 0], [0, 0]]])
def test_invalid_panels_rejected(invalid):
    with pytest.raises(ValueError):
        infer_paired_effect(invalid)


def test_exact_tied_repeats_raise_boundary_warning_not_false_precision():
    posterior = infer_paired_effect(np.zeros((8, 2)))
    assert posterior.exact_within_geometry_ties is True
    assert posterior.summary()["probability_rope"] > 0.99


def test_synthetic_analysis_reports_sensitivity_without_updating_architecture():
    result = analyze_paired_effect(synthetic_effects(0.075), bootstrap_samples=500)
    assert result["quadrature_converged"] is True
    assert result["tail_negligible"] is True
    assert set(result["mu_prior_sensitivity"]) == {"0.02", "0.1"}
    assert result["architecture_decision_eligible"] is False
    assert result["architecture_beliefs_updated"] is False
    assert result["H_marginal_priors"] == H_MARGINAL_PRIORS


@pytest.mark.parametrize("stage", ["smoke", "calibration", "integration", "unit_test", "pilot", "screen"])
def test_technical_and_selected_pilot_scores_cannot_update_architecture(stage):
    with pytest.raises(ValueError):
        analyze_paired_effect(synthetic_effects(), evidence_stage=stage)
    with pytest.raises(ValueError):
        subjective_hypothesis_update("H3", "strong_for", evidence_stage=stage, evidence_id="synthetic")


def test_marginal_priors_are_not_a_normalized_partition_and_h5_stays_locked():
    beliefs = initial_beliefs()
    assert sum(H_MARGINAL_PRIORS.values()) > 1
    assert beliefs["mutually_exclusive"] is False
    assert all(value["prior"] == value["posterior"] and value["status"] == "UNUPDATED"
               for value in beliefs["hypotheses"].values())
    with pytest.raises(ValueError, match="H5"):
        subjective_hypothesis_update("H5", "strong_for", evidence_stage="confirmation", evidence_id="confirm")
    update = subjective_hypothesis_update("H3", "weak_for", evidence_stage="confirmation", evidence_id="confirm")
    assert update["posterior_illustrative"] == pytest.approx(0.4)
    assert update["is_estimated_Bayes_factor"] is False
    assert update["posterior_sensitivity"] < update["posterior_illustrative"]


def manifest_records():
    rows = []
    deltas = synthetic_effects(0.075)
    for gi in range(8):
        for si in range(2):
            for condition in ("native", "shuffle"):
                rows.append({
                    "experiment_id": f"g{gi}-s{si}-{condition}", "stage": "confirmation",
                    "preregistered": True, "task": "copy", "variant": "T",
                    "geometry_seed": 3101 + gi, "training_seed": 4101 + si,
                    "condition": condition, "status": "COMPLETE",
                    "score_split": "test", "test_opened": True,
                    "score": 0.65 + (float(deltas[gi, si]) if condition == "native" else 0),
                    "pair_hashes": {key: f"hash-{key}" for key in PAIR_HASH_KEYS},
                    "labels_hash": "hash-" + condition,
                })
    return rows


def test_paired_records_audit_complete_panel_and_explicit_estimand():
    rows = manifest_records()
    # All checks before invoking numerical inference, so these invalid cases are cheap.
    invalid = copy.deepcopy(rows)
    invalid[0]["pair_hashes"]["edges"] = "different"
    with pytest.raises(ValueError, match="pairing"):
        analyze_records(invalid)
    with pytest.raises(ValueError, match="Incomplete"):
        analyze_records(rows[:-1])
    with pytest.raises(ValueError, match="Duplicate"):
        analyze_records(rows + rows[:1])
    invalid = copy.deepcopy(rows)
    invalid[0]["preregistered"] = False
    with pytest.raises(ValueError, match="preregistration"):
        analyze_records(invalid)
    invalid = copy.deepcopy(rows)
    invalid[0]["status"] = "INFRASTRUCTURE_FAILURE"
    with pytest.raises(ValueError, match="infrastructure"):
        analyze_records(invalid)
    invalid = copy.deepcopy(rows)
    invalid[0]["stage"] = "smoke"
    with pytest.raises(ValueError, match="phase"):
        analyze_records(invalid)
    invalid = copy.deepcopy(rows)
    invalid[0]["score_split"] = "validation"
    with pytest.raises(ValueError, match="test endpoint"):
        analyze_records(invalid)
    invalid = copy.deepcopy(rows)
    invalid[0]["test_opened"] = False
    with pytest.raises(ValueError, match="test endpoint"):
        analyze_records(invalid)


def test_reproducible_divergence_is_zero_while_architecture_estimand_is_explicit(monkeypatch):
    captured = {}
    def capture(deltas, **kwargs):
        captured["deltas"] = deltas
        return {"architecture_beliefs_updated": False, "numerically_decision_eligible": True}
    monkeypatch.setattr("larp.analysis.analyze_paired_effect", capture)
    rows = manifest_records()
    rows[0]["status"] = "TRAINING_DIVERGENCE"
    rows[0]["score"] = float("nan")  # Logged run score may be missing, system score cannot be.
    with pytest.raises(ValueError, match="reproducibly verified"):
        analyze_records(rows)
    rows[0].update(divergence_verified=True, infrastructure_excluded=True)
    result = analyze_records(rows)
    assert result["native_scores"][0][0] == 0
    assert captured["deltas"][0][0] == pytest.approx(-0.65)
    assert result["divergence_count"] == 1
    assert result["system_failure_rate"] == pytest.approx(1 / 32)
    assert result["architecture_decision_eligible"] is False
    rows = manifest_records()
    for row in rows:
        if row["condition"] == "shuffle":
            row["condition"] = "grid"
            for key in ("coordinates", "edges", "ports"):
                row["pair_hashes"][key] = "different-baseline-" + key
    with pytest.raises(ValueError, match="pairing"):
        analyze_records(rows, control_condition="grid")
    result = analyze_records(rows, control_condition="grid", estimand="architecture")
    assert result["estimand"] == "architecture"
    assert "coordinates" not in result["pair_hash_fields_checked"]
    assert "data_test" in result["pair_hash_fields_checked"]


def test_robustness_completed_scores_must_use_test_data(monkeypatch):
    monkeypatch.setattr("larp.analysis.analyze_paired_effect", lambda *args, **kwargs: {})
    rows = manifest_records()
    for row in rows:
        row["stage"] = "robustness"
    assert analyze_records(rows)["task"] == "copy"
    rows[0]["score_split"] = "validation"
    with pytest.raises(ValueError, match="test endpoint"):
        analyze_records(rows)


def test_frozen_expected_seed_manifest_is_required_and_must_be_complete(monkeypatch):
    monkeypatch.setattr("larp.analysis.analyze_paired_effect", lambda *args, **kwargs: {
        "numerically_decision_eligible": True, "architecture_beliefs_updated": False,
    })
    rows = manifest_records()
    expected_g, expected_s = list(range(3101, 3109)), [4101, 4102]
    descriptive = analyze_records(rows)
    assert descriptive["replication_manifest_complete"] is False
    assert descriptive["architecture_decision_eligible"] is False
    complete = analyze_records(rows, expected_geometry_seeds=expected_g, expected_training_seeds=expected_s)
    assert complete["replication_manifest_complete"] is True
    assert complete["confirmation_design_conforms"] is True
    assert complete["architecture_decision_eligible"] is True
    with pytest.raises(ValueError, match="geometry seed panel"):
        analyze_records(rows[:-4], expected_geometry_seeds=expected_g, expected_training_seeds=expected_s)
    with pytest.raises(ValueError, match="training seed panel"):
        analyze_records([row for row in rows if row["training_seed"] == 4101],
                        expected_geometry_seeds=expected_g, expected_training_seeds=expected_s)
    with pytest.raises(ValueError, match="Duplicate seed"):
        analyze_records(rows, expected_geometry_seeds=expected_g + [3101], expected_training_seeds=expected_s)
    for row in rows:
        row.update(expected_geometry_seeds=expected_g, expected_training_seeds=expected_s)
    assert analyze_records(rows)["architecture_decision_eligible"] is True
    contradictory = copy.deepcopy(rows)
    contradictory[0]["expected_geometry_seeds"] = [1, 2]
    with pytest.raises(ValueError, match="Conflicting"):
        analyze_records(contradictory)
    missing = copy.deepcopy(rows)
    del missing[0]["expected_training_seeds"]
    with pytest.raises(ValueError, match="missing"):
        analyze_records(missing)
    with pytest.raises(ValueError, match="disagree"):
        analyze_records(rows, expected_geometry_seeds=[7, 8])


def test_small_complete_panel_is_descriptive_and_cannot_override_confirmation_design(monkeypatch):
    monkeypatch.setattr("larp.analysis.analyze_paired_effect", lambda *args, **kwargs: {
        "numerically_decision_eligible": True,
    })
    rows = [row for row in manifest_records() if row["geometry_seed"] < 3104]
    result = analyze_records(rows, expected_geometry_seeds=[3101, 3102, 3103],
                             expected_training_seeds=[4101, 4102])
    assert result["replication_manifest_complete"] is True
    assert result["confirmation_design_conforms"] is False
    assert result["architecture_decision_eligible"] is False


def test_paired_differences_never_silently_reorders_or_imputes_scores():
    expected = synthetic_effects(0.075)
    np.testing.assert_allclose(paired_differences(0.5 + expected, np.full((8, 2), 0.5)), expected)
    with pytest.raises(ValueError, match="shape"):
        paired_differences(np.zeros((8, 2)), np.zeros((8, 3)))
    with pytest.raises(ValueError, match="finite"):
        paired_differences(np.full((8, 2), np.nan), np.zeros((8, 2)))
