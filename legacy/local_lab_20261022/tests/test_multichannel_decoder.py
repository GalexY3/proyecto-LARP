"""Technical tests only; synthetic fixtures are not LARP scientific results."""
import numpy as np
import pytest

from larp.multichannel_decoder import (channel_covariance, estimate_training_rho,
    fourier_features, lmmse_predict, local_sensor_ids, make_gaussian_bank,
    marked_observations)


MODES = np.array([[1, 0], [0, 1], [1, 1]], dtype=np.int64)


def test_gaussian_scale_cross_covariance_and_no_world_normalization():
    bank = make_gaussian_bank(MODES, 8.0, 6000, .8, np.random.default_rng(91011))
    samples = bank.coefficients.transpose(0, 2, 1).reshape(-1, 5)
    np.testing.assert_allclose(np.cov(samples, rowvar=False, bias=True), channel_covariance(.8)/3,
                               atol=.007, rtol=0)
    np.testing.assert_allclose(bank.analytic_variance.mean(axis=0), np.ones(5), atol=.025, rtol=0)
    assert bank.analytic_variance.std() > .2
    features = fourier_features(np.array([[.1, .4], [7.9, -.2]]), MODES, 8.0)
    np.testing.assert_allclose(bank.evaluate(np.array([[.1, .4], [7.9, -.2]])),
                               np.einsum("wcd,qd->wcq", bank.coefficients, features))


def test_marked_observations_do_not_read_unmarked_channels():
    bank = make_gaussian_bank(MODES, 8., 4, .8, np.random.default_rng(91012))
    points = np.array([[.2, .3], [1., 2.], [3., 4.]])
    labels = np.array([0, 4, 2])
    noise = np.arange(12).reshape(4, 3)/10
    expected = bank.evaluate(points)[:, labels, np.arange(3)]+.1*noise
    np.testing.assert_allclose(marked_observations(bank, points, labels, noise, .1), expected)


def test_independent_channels_and_local_missing_type_are_exactly_unaffected():
    points = np.array([[.1, 0.], [.2, 0.], [2., 2.], [3., 3.]])
    labels = np.array([0, 1, 2, 4])
    queries = np.array([[0., 0.]])
    y = np.array([[1., 2., 3., 4.]])
    kwargs = dict(points=points, labels=labels, queries=queries, modes=MODES, L=8.,
                  sigma=.1, model_rho=0., true_rho=0., scope="LOCAL", k=2)
    prediction, report = lmmse_predict(observations=y, **kwargs)
    changed = y.copy()
    changed[:, 1:] += 1000
    altered, _ = lmmse_predict(observations=changed, **kwargs)
    np.testing.assert_array_equal(prediction[:, 0], altered[:, 0])
    np.testing.assert_array_equal(prediction[:, 2:], np.zeros_like(prediction[:, 2:]))
    np.testing.assert_allclose(report["true_risk_by_channel_query"][2:], 1.)
    np.testing.assert_allclose(report["true_contrast_NMSE_by_query"], 1.)


@pytest.mark.parametrize("model_rho", [0., .8])
@pytest.mark.parametrize("scope,k", [("GLOBAL", 24), ("LOCAL", 4)])
def test_predictions_and_mismatch_risk_match_independent_covariance_formula(model_rho, scope, k):
    rng = np.random.default_rng(91013)
    points, queries = rng.uniform(0, 8, (40, 2)), rng.uniform(0, 8, (3, 2))
    labels = np.arange(40) % 5
    y = rng.normal(size=(3, 40))
    sigma, true_rho = .2, .35
    prediction, report = lmmse_predict(points, labels, queries, MODES, 8., y,
                                       sigma, model_rho, true_rho, scope, k)
    F, Fq = fourier_features(points, MODES, 8.), fourier_features(queries, MODES, 8.)
    Cmodel, Ctrue = channel_covariance(model_rho), channel_covariance(true_rho)
    for q in range(len(queries)):
        ids = np.arange(40) if scope == "GLOBAL" else report["local_sensor_ids"][q]
        Fs, cs = F[ids], labels[ids]
        kernel = Fs @ Fs.T/len(MODES)
        km = kernel*Cmodel[cs[:, None], cs[None, :]]+sigma**2*np.eye(len(ids))
        kt = kernel*Ctrue[cs[:, None], cs[None, :]]+sigma**2*np.eye(len(ids))
        spatial_cross = Fq[q] @ Fs.T/len(MODES)
        qm, qt = Cmodel[:, cs]*spatial_cross, Ctrue[:, cs]*spatial_cross
        weights = np.linalg.solve(km, qm.T).T
        np.testing.assert_allclose(prediction[:, :, q], y[:, ids] @ weights.T, atol=1e-10, rtol=1e-10)
        covariance = Ctrue-weights @ qt.T-qt @ weights.T+weights @ kt @ weights.T
        np.testing.assert_allclose(report["true_risk_by_channel_query"][:, q], np.diag(covariance), atol=1e-10)
        contrast = np.array([0., 0., 0., 1., -1.])/np.sqrt(2)
        np.testing.assert_allclose(report["true_contrast_MSE_by_query"][q], contrast @ covariance @ contrast, atol=1e-10)
    assert ("primal_Cholesky" if scope == "GLOBAL" else "dual_Cholesky") in report["solver_counts"]
    assert report["sensors_consulted_per_query"] == (40 if scope == "GLOBAL" else k)
    assert report["approx_MAC"] > 0


def test_local_ids_ignore_labels_and_break_ties_by_node_id_periodically():
    points = np.array([[1., 0.], [7., 0.], [0., 1.], [0., 7.], [4., 4.]])
    query = np.array([[0., 0.], [8., 8.]])
    np.testing.assert_array_equal(local_sensor_ids(points, query, 8., 3), [[0, 1, 2], [0, 1, 2]])


def test_OLS_training_rho_and_noise_covariance_on_full_grid():
    points = np.array([[a, b] for a in range(8) for b in range(8)], dtype=float)
    bank = make_gaussian_bank(MODES, 8., 1000, .8, np.random.default_rng(91014))
    rng = np.random.default_rng(91015)
    sigma = .1
    training = bank.evaluate(points)+sigma*rng.normal(size=(1000, 5, len(points)))
    result = estimate_training_rho(points, MODES, 8., training, sigma)
    np.testing.assert_allclose(result["rho_raw"], .8, atol=.04)
    expected = sigma**2*2/len(points)*np.eye(6)
    np.testing.assert_allclose(result["coefficient_noise_covariance"], expected, atol=1e-17)
    coefficient_error = result["coefficient_estimates"]-bank.coefficients
    empirical = np.cov(coefficient_error.reshape(-1, 6), rowvar=False, bias=True)
    np.testing.assert_allclose(empirical, expected, atol=3e-5, rtol=0)
    assert result["centering"] == result["covariance_normalization"] == "none"
    noiseless = estimate_training_rho(points, MODES, 8., bank.evaluate(points), 0.)
    np.testing.assert_allclose(noiseless["coefficient_estimates"], bank.coefficients, atol=2e-15)


def test_invalid_frequency_pairs_empty_training_and_singular_dictionary_are_rejected():
    with pytest.raises(ValueError, match="unique"):
        fourier_features(np.zeros((1, 2)), np.array([[1, 0], [-1, 0]]), 8.)
    with pytest.raises(ValueError, match="full Fourier column rank"):
        estimate_training_rho(np.zeros((8, 2)), MODES, 8., np.ones((3, 5, 8)), .1)
    with pytest.raises(ValueError, match="sigma"):
        lmmse_predict(np.ones((2, 2)), [0, 1], np.ones((1, 2)), MODES, 8.,
                       np.ones((1, 2)), 0., 0., 0., "GLOBAL")
