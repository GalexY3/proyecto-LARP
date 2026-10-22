"""Oracle algebra and strong-estimator limits, without expanding the suite."""
import numpy as np
import pytest
from larp.sampling_oracle import fourier_design, oracle_operator, load_oracle_config
from larp.sampling_probe import make_field_bank


def test_frozen_oracle_is_posthoc_and_does_not_duplicate_cells():
    cfg = load_oracle_config()
    assert cfg["expected_unique_oracle_cells"] == 72
    assert cfg["expected_comparisons_to_v1_estimators"] == 144
    assert cfg["no_hpo"] and not cfg["architecture_evidence"]
    assert cfg["ridge_lambda_rule"] == "number_real_mode_pairs * noise_sigma^2"


def test_noiseless_full_rank_fourier_exact_recovery():
    rng = np.random.default_rng(9)
    modes = np.array([[1, 0], [0, 1], [1, 1]])
    points, queries = rng.uniform(0, 20, (16, 2)), rng.uniform(0, 20, (11, 2))
    A, Q = fourier_design(points, modes, 20), fourier_design(queries, modes, 20)
    operator, report = oracle_operator(A, Q, sigma=0, mode_pairs=3)
    beta = rng.normal(size=(8, 6))
    np.testing.assert_allclose((beta@A.T)@operator.T, beta@Q.T, atol=2e-14)
    assert report["rank"] == 6 and report["nullity"] == 0


def test_ridge_exactly_matches_known_linear_covariance_rule():
    rng = np.random.default_rng(5)
    A, Q = rng.normal(size=(9, 8)), rng.normal(size=(6, 8))
    sigma, M = .1, 4
    operator, report = oracle_operator(A, Q, sigma=sigma, mode_pairs=M)
    expected = Q@np.linalg.solve(A.T@A+M*sigma**2*np.eye(8), A.T)
    np.testing.assert_allclose(operator, expected, atol=2e-14)
    assert report["ridge_lambda"] == pytest.approx(.04)
    assert not report["exact_nonlinear_posterior"]


def test_underdetermined_problem_reports_nullity_and_uses_minimum_norm():
    rng = np.random.default_rng(4)
    A, Q = rng.normal(size=(3, 8)), np.eye(8)
    operator, report = oracle_operator(A, Q, sigma=0, mode_pairs=4)
    np.testing.assert_allclose(operator, np.linalg.pinv(A, rcond=1e-10), atol=1e-14)
    assert report["rank"] == 3 and report["nullity"] == 5
    assert report["sigma_min_full_column_problem"] == 0
    assert report["condition_full_column_problem"] is None
    assert report["condition_full_is_infinite_when_nullity_positive"]


def test_zero_singular_values_are_not_inverted_or_silently_full_rank():
    A = np.ones((10, 4))
    operator, report = oracle_operator(A, np.eye(4), sigma=0, mode_pairs=2)
    assert report["rank"] == 1 and report["nullity"] == 3
    assert np.isfinite(operator).all()
    np.testing.assert_allclose(operator, np.linalg.pinv(A, rcond=1e-10), atol=1e-15)


def test_periodic_design_and_covariance_dimensions():
    points = np.array([[.3, 1.5], [15., 19.]])
    modes = np.array([[1, 0], [0, 2], [2, -1]])
    np.testing.assert_allclose(fourier_design(points, modes, 20), fourier_design(points+[20, -20], modes, 20), atol=5e-15)
    with pytest.raises(ValueError, match="D=2"):
        oracle_operator(np.ones((3, 5)), np.ones((2, 5)), sigma=0, mode_pairs=3)


@pytest.mark.parametrize("band", ["smooth", "fine"])
def test_actual_sphere_normalization_matches_ridge_prior_covariance_scale(band):
    bank = make_field_bank(band)
    coefficients = np.concatenate((bank.cosine, bank.sine), axis=-1)
    M = len(bank.modes)
    # Norm^2=2 on a rotationally invariant D=2M sphere implies Cov=I/M.
    # This catches a changed field scale even if the ridge algebra itself passes.
    np.testing.assert_allclose(np.sum(coefficients**2, axis=-1), 2, atol=2e-15)
    assert np.mean(coefficients**2) == pytest.approx(1/M, abs=2e-16)


def test_other_channel_values_cannot_enter_a_channel_oracle_operator():
    rng = np.random.default_rng(71)
    points, queries = rng.uniform(0, 20, (30, 2)), rng.uniform(0, 20, (6, 2))
    labels = np.repeat(np.arange(5), 6)
    modes = np.array([[1, 0], [0, 1]])
    Aall, Q = fourier_design(points, modes, 20), fourier_design(queries, modes, 20)
    coefficients = rng.normal(size=(8, 5, 4))
    values = np.einsum("wcd,nd->wcn", coefficients, Aall)
    c = 2
    sensors = np.flatnonzero(labels == c)
    operator, _ = oracle_operator(Aall[sensors], Q, sigma=0, mode_pairs=2)
    baseline = values[:, c, sensors]@operator.T
    # Counterfactual changes of the four inaccessible channels leave c unchanged.
    other = values.copy()
    other[:, np.arange(5) != c, :] += rng.normal(size=(8, 4, 30))*10000
    np.testing.assert_array_equal(other[:, c, sensors]@operator.T, baseline)
    np.testing.assert_allclose(baseline, coefficients[:, c]@Q.T, atol=2e-14)
