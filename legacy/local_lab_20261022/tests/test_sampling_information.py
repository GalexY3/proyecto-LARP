"""Independent covariance checks for the information diagnostic."""
import numpy as np
import pytest

from larp.sampling_information import design_diagnostic, gram_from_density, linear_risk, oracle_maps, uniform_oracle_risk
from larp.sampling_oracle import fourier_design


def test_real_gram_uses_both_density_sums_and_differences():
    points = np.random.default_rng(14).uniform(0, 20, (17, 2))
    modes = np.array([[1, 0], [0, 1], [3, -2]])
    A = fourier_design(points, modes, 20)
    reconstructed, report = gram_from_density(points, modes, 20)
    np.testing.assert_allclose(reconstructed, A.T @ A, atol=3e-14)
    assert [6, -4] in report["required_density_modes"]


@pytest.mark.parametrize("sigma", [0.0, 0.1])
def test_decomposition_matches_independent_covariance_matrix(sigma):
    rng = np.random.default_rng(42)
    A, Q, H = rng.normal(size=(3, 8)), rng.normal(size=(7, 8)), rng.normal(size=(7, 3))
    diag, svd = design_diagnostic(A, Q, M=4, rcond=1e-10)
    result = linear_risk(A, Q, H, M=4, sigma=sigma, observed=svd["observed"], null=svd["null"])
    Cyy = A @ A.T/4 + sigma**2*np.eye(3)
    Cyq = A @ Q.T/4
    Cqq = Q @ Q.T/4
    covariance = Cqq - H @ Cyq - Cyq.T @ H.T + H @ Cyy @ H.T
    assert result["expected_MSE"] == pytest.approx(np.trace(covariance)/7, abs=2e-14)
    assert result["decomposition_error"] < 2e-14
    assert diag["numerical_nullity"] == 5


def test_nullity_is_not_a_fixed_query_error_floor():
    A = np.array([[1., 0., 0., 0.], [0., 1., 0., 0.]])
    Q = A.copy()  # Queries deliberately ignore both unobserved coefficients.
    diag, svd = design_diagnostic(A, Q, M=2, rcond=1e-10)
    H, K = oracle_maps(Q, svd, M=2, sigma=0, rcond=1e-10)
    assert diag["numerical_nullity"] == 2
    assert diag["query_weighted_noiseless_null_floor"] == 0
    assert diag["uniform_continuous_torus_null_floor"] == .5
    assert linear_risk(A, Q, H, M=2, sigma=0, observed=svd["observed"], null=svd["null"])["expected_MSE"] == 0
    assert uniform_oracle_risk(A, K, M=2, sigma=0, observed=svd["observed"], null=svd["null"])["expected_MSE"] == .5


def test_gaussian_oracle_risk_equals_conditional_covariance():
    rng = np.random.default_rng(51)
    A, Q = rng.normal(size=(11, 8)), rng.normal(size=(6, 8))
    _, svd = design_diagnostic(A, Q, M=4, rcond=1e-10)
    H, _ = oracle_maps(Q, svd, M=4, sigma=.1, rcond=1e-10)
    risk = linear_risk(A, Q, H, M=4, sigma=.1, observed=svd["observed"], null=svd["null"])
    Cpost = np.linalg.inv(4*np.eye(8) + A.T @ A/.01)
    assert risk["expected_MSE"] == pytest.approx(np.trace(Q @ Cpost @ Q.T)/len(Q), abs=1e-15)


def test_historical_nyquist_queries_are_not_uniform_continuous_covariance():
    queries = np.array([(2*a+.5, 2*b+.5) for a in range(10) for b in range(10)])
    modes = np.array([[5, 0], [0, 5]])
    Q = fourier_design(queries, modes, 20)
    assert np.linalg.matrix_rank(Q, tol=1e-10) == 2
    assert np.max(np.abs(Q.T @ Q/len(Q) - .5*np.eye(4))) > .49


def test_nonfinite_risk_inputs_fail_instead_of_imputing():
    A, Q, H = np.ones((2, 4)), np.ones((3, 4)), np.ones((3, 2))
    H[0, 0] = np.nan
    with pytest.raises(ValueError, match="Nonfinite"):
        linear_risk(A, Q, H, M=2, sigma=.1, observed=np.eye(4), null=np.zeros((4, 4)))


@pytest.mark.parametrize("sigma, expected", [(0., 3/8), (.2, 79/204)])
def test_independently_derived_singular_weighted_query_risk(sigma, expected):
    A = np.sqrt(2)*np.array([[1.,0.,0.,0.], [0.,1.,0.,0.], [1.,0.,0.,0.], [0.,1.,0.,0.]])
    Q = np.array([[np.sqrt(1.5),0.,np.sqrt(.5),0.], [0.,1.,0.,1.]])
    _, svd = design_diagnostic(A, Q, M=2, rcond=1e-10)
    H, _ = oracle_maps(Q, svd, M=2, sigma=sigma, rcond=1e-10)
    risk = linear_risk(A, Q, H, M=2, sigma=sigma, observed=svd["observed"], null=svd["null"])
    assert risk["expected_MSE"] == pytest.approx(expected, abs=1e-15)


def test_positive_ridge_keeps_small_singular_values_below_rank_cutoff():
    A = np.array([[1.,0.,0.,0.], [0.,1e-12,0.,0.]])
    Q = np.eye(4)
    report, svd = design_diagnostic(A, Q, M=2, rcond=1e-10)
    _, K = oracle_maps(Q, svd, M=2, sigma=.1, rcond=1e-10)
    assert report["rank"] == 1
    assert K[1,1] == pytest.approx(1e-12/(1e-24+.02), abs=1e-25)
    assert K[1,1] > 0
