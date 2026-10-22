"""Pure components for a new multichannel, information-by-reach pilot.

This module neither generates geometry nor writes results. Gaussian Fourier
coefficients have covariance C_rho/M and are never normalized per realization.
Each physical sensor reads its marked channel only. Both scopes use the same
LMMSE rule, with independent signal-model knowledge and observation reach.
Expected risks are algebraic diagnostics; reproducing them does not confirm MHU.
"""
from __future__ import annotations

from dataclasses import dataclass
import time

import numpy as np
from scipy.linalg import cho_factor, cho_solve


CHANNELS = 5


def channel_covariance(rho: float) -> np.ndarray:
    """Unit diagonal equicorrelation; the declared pilot uses rho=0 or .8."""
    if not np.isfinite(rho) or not 0 <= rho < 1:
        raise ValueError("rho must be finite and in [0,1)")
    return (1.0-rho)*np.eye(CHANNELS)+rho*np.ones((CHANNELS, CHANNELS))


def fourier_features(points: np.ndarray, modes: np.ndarray, L: float) -> np.ndarray:
    """Columns are all cosine modes followed by all sine modes."""
    points = np.asarray(points, dtype=np.float64)
    supplied_modes = np.asarray(modes)
    if points.ndim != 2 or points.shape[1] != 2 or not np.isfinite(points).all():
        raise ValueError("points must be finite (n,2)")
    if supplied_modes.ndim != 2 or supplied_modes.shape[1] != 2 or len(supplied_modes) == 0:
        raise ValueError("modes must be a nonempty (M,2) integer array")
    if not np.isfinite(supplied_modes).all() or not np.equal(supplied_modes, np.round(supplied_modes)).all():
        raise ValueError("modes must be finite integers")
    integer_modes = supplied_modes.astype(np.int64)
    if any(np.array_equal(m, [0, 0]) for m in integer_modes):
        raise ValueError("the bank excludes the zero Fourier mode")
    # Duplicate or opposite representatives invalidate unit-variance bookkeeping.
    mode_set = {tuple(m) for m in integer_modes.tolist()}
    if len(mode_set) != len(integer_modes) or any((-a, -b) in mode_set for a, b in mode_set):
        raise ValueError("modes must contain one unique representative of each +/- pair")
    if not np.isfinite(L) or L <= 0:
        raise ValueError("L must be finite and positive")
    phase = 2*np.pi/L*((points % L) @ integer_modes.T)
    return np.concatenate((np.cos(phase), np.sin(phase)), axis=1)


@dataclass(frozen=True)
class GaussianFieldBank:
    modes: np.ndarray
    coefficients: np.ndarray  # (world,channel,D), D=2*M
    L: float
    rho: float

    @property
    def analytic_variance(self) -> np.ndarray:
        """Spatial variance per world/channel, variable rather than forced to one."""
        return np.sum(self.coefficients**2, axis=-1)/2

    def evaluate(self, points: np.ndarray) -> np.ndarray:
        features = fourier_features(points, self.modes, self.L)
        return np.einsum("wcd,qd->wcq", self.coefficients, features, optimize=True)


def make_gaussian_bank(modes: np.ndarray, L: float, worlds: int, rho: float,
                       rng: np.random.Generator) -> GaussianFieldBank:
    """Caller supplies every RNG; independent modes/cos/sin, correlated channels."""
    fourier_features(np.empty((0, 2)), modes, L)
    if not isinstance(worlds, (int, np.integer)) or worlds <= 0:
        raise ValueError("worlds must be a positive integer")
    M = len(modes)
    chol = np.linalg.cholesky(channel_covariance(rho))
    normal = rng.normal(size=(worlds, 2*M, CHANNELS))
    coefficients = (normal @ chol.T).transpose(0, 2, 1)/np.sqrt(M)
    return GaussianFieldBank(np.array(modes, dtype=np.int64, copy=True), coefficients, float(L), float(rho))


def _labels(labels: np.ndarray, count: int) -> np.ndarray:
    given = np.asarray(labels)
    if given.shape != (count,) or not np.isfinite(given).all() or not np.equal(given, np.round(given)).all():
        raise ValueError("labels must be an integer vector with one mark per sensor")
    result = given.astype(np.int64)
    if np.any(result < 0) or np.any(result >= CHANNELS):
        raise ValueError("labels must be in [0,4]")
    return result


def _sigma(sigma: float, *, positive: bool = False) -> None:
    if not np.isfinite(sigma) or sigma < 0 or (positive and sigma == 0):
        raise ValueError("sigma must be finite and positive" if positive else "sigma must be finite and nonnegative")


def marked_observations(bank: GaussianFieldBank, points: np.ndarray, labels: np.ndarray,
                        noise: np.ndarray, sigma: float) -> np.ndarray:
    _sigma(sigma)
    labels = _labels(labels, len(points))
    noise = np.asarray(noise, dtype=np.float64)
    expected_shape = (len(bank.coefficients), len(points))
    if noise.shape != expected_shape or not np.isfinite(noise).all():
        raise ValueError("noise must be finite (world,sensor)")
    values = bank.evaluate(points)
    return values[:, labels, np.arange(len(points))]+sigma*noise


def estimate_training_rho(points: np.ndarray, modes: np.ndarray, L: float,
                          observations: np.ndarray, sigma: float) -> dict:
    """OLS on independent, fully observed training maps only; never center test.

    Cross-channel products have no expected contribution from independent
    channel noise. Cov(OLS noise) = sigma^2 (F.T F)^-1 per channel. The caller
    retains the raw estimate and clips the decoder parameter to [0,.95].
    """
    _sigma(sigma)
    F = fourier_features(points, modes, L)
    observations = np.asarray(observations, dtype=np.float64)
    if observations.ndim != 3 or observations.shape[1:] != (CHANNELS, len(points)) or observations.shape[0] == 0:
        raise ValueError("training observations must be (world,5,gridpoint)")
    if not np.isfinite(observations).all():
        raise ValueError("training observations must be finite")
    if np.linalg.matrix_rank(F, tol=1e-10*np.linalg.norm(F, 2)) != F.shape[1]:
        raise ValueError("training grid must have full Fourier column rank")
    gram = F.T @ F
    chol = cho_factor(gram, lower=True, check_finite=False)
    ols_map = cho_solve(chol, F.T, check_finite=False)
    estimates = observations @ ols_map.T
    channel_products = np.einsum("wcd,wed->wce", estimates, estimates, optimize=True)/F.shape[1]
    offdiag = ~np.eye(CHANNELS, dtype=bool)
    world_rho = len(modes)*channel_products[:, offdiag].mean(axis=1)
    raw = float(world_rho.mean())
    return {"rho_hat": float(np.clip(raw, 0.0, 0.95)), "rho_raw": raw,
            "rho_clipped": not 0 <= raw <= 0.95, "world_rho_estimates": world_rho,
            "coefficient_estimates": estimates,
            "coefficient_noise_covariance": sigma**2*cho_solve(chol, np.eye(F.shape[1]), check_finite=False),
            "training_worlds": len(observations), "training_gridpoints": len(points),
            "OLS_rank": F.shape[1], "coefficient_dimension_D": F.shape[1],
            "centering": "none", "covariance_normalization": "none",
            "noise_cross_channel_expectation": 0.0,
            "rho_formula": "M*mean(theta_hat_c*theta_hat_d), pooled worlds, Fourier columns, c!=d"}


def local_sensor_ids(points: np.ndarray, queries: np.ndarray, L: float, k: int = 24) -> np.ndarray:
    """K nearest physical node IDs, marks/values blind; exact ties use node ID."""
    points, queries = np.asarray(points, dtype=np.float64), np.asarray(queries, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 2 or queries.ndim != 2 or queries.shape[1] != 2:
        raise ValueError("points and queries must have shape (n,2)")
    if not np.isfinite(points).all() or not np.isfinite(queries).all() or not np.isfinite(L) or L <= 0:
        raise ValueError("coordinates and L must be finite, L positive")
    if not isinstance(k, (int, np.integer)) or k <= 0 or k > len(points):
        raise ValueError("k must be an integer in [1,sensor_count]")
    displacement = queries[:, None, :]-points[None, :, :]
    displacement -= L*np.round(displacement/L)
    distance_squared = np.sum(displacement**2, axis=-1)
    return np.argsort(distance_squared, axis=1, kind="stable")[:, :k]


def _observation_features(F: np.ndarray, labels: np.ndarray, rho: float) -> np.ndarray:
    chol = np.linalg.cholesky(channel_covariance(rho))
    return (chol[labels, :, None]*F[:, None, :]).reshape(len(F), CHANNELS*F.shape[1])/np.sqrt(F.shape[1]/2)


def _query_features(F: np.ndarray, rho: float) -> np.ndarray:
    chol = np.linalg.cholesky(channel_covariance(rho))
    return np.einsum("ca,qd->cqad", chol, F).reshape(CHANNELS*len(F), CHANNELS*F.shape[1])/np.sqrt(F.shape[1]/2)


def _weights(B: np.ndarray, T: np.ndarray, sigma: float) -> tuple[np.ndarray, str, int]:
    n, p = B.shape
    if p < n:
        chol = cho_factor(B.T @ B+sigma**2*np.eye(p), lower=True, check_finite=False)
        solved = cho_solve(chol, B.T, check_finite=False)
        weights = T @ solved
        # Approximate MAC for Gram, triangular solves and mapping; not FLOPs.
        mac = n*p*p + p**3//3 + p*p*n + len(T)*p*n
        return weights, "primal_Cholesky", mac
    chol = cho_factor(B @ B.T+sigma**2*np.eye(n), lower=True, check_finite=False)
    cross = T @ B.T
    weights = cho_solve(chol, cross.T, check_finite=False).T
    mac = n*n*p + n**3//3 + len(T)*p*n + n*n*len(T)
    return weights, "dual_Cholesky", mac


def _true_risks(weights: np.ndarray, B: np.ndarray, T: np.ndarray,
                sigma: float) -> np.ndarray:
    # Stable, nonnegative mismatch identity: ||T-WB||^2+sigma^2||W||^2.
    error_map = T-weights @ B
    return np.sum(error_map**2, axis=1)+sigma**2*np.sum(weights**2, axis=1)


def lmmse_predict(points: np.ndarray, labels: np.ndarray, queries: np.ndarray,
                  modes: np.ndarray, L: float, observations: np.ndarray, sigma: float,
                  model_rho: float, true_rho: float, scope: str,
                  k: int = 24) -> tuple[np.ndarray, dict]:
    """Return prediction (W,5,Q) and expected true/model risks, not a score.

    scope is LOCAL or GLOBAL (LOCAL_K24 also accepted with k=24). Model and
    true rho are deliberately separate. Costs omit no observations in the
    kernel solve: LOCAL consults K total nodes for all outputs, never K/type.
    GLOBAL batches all queries and switches to a latent-space solve when useful.
    """
    start = time.perf_counter()
    _sigma(sigma, positive=True)
    labels = _labels(labels, len(points))
    observations = np.asarray(observations, dtype=np.float64)
    if observations.ndim != 2 or observations.shape[1] != len(points) or observations.shape[0] == 0:
        raise ValueError("observations must be (world,sensor)")
    if not np.isfinite(observations).all() or len(points) == 0 or len(queries) == 0:
        raise ValueError("nonempty finite observations, points and queries required")
    if scope not in ("LOCAL", "LOCAL_K24", "GLOBAL") or (scope == "LOCAL_K24" and k != 24):
        raise ValueError("scope must be LOCAL, LOCAL_K24 with k=24, or GLOBAL")
    F, Fq = fourier_features(points, modes, L), fourier_features(queries, modes, L)
    Bmodel, Tmodel = _observation_features(F, labels, model_rho), _query_features(Fq, model_rho)
    Btrue, Ttrue = _observation_features(F, labels, true_rho), _query_features(Fq, true_rho)
    worlds, Q = len(observations), len(queries)
    selection_start = time.perf_counter()
    ids = None if scope == "GLOBAL" else local_sensor_ids(points, queries, L, k)
    selection_seconds = time.perf_counter()-selection_start
    prepare_seconds = selection_start-start
    prediction = np.empty((worlds, CHANNELS, Q))
    true_risk = np.empty((CHANNELS, Q))
    assumed_risk = np.empty_like(true_risk)
    contrast_risk = np.empty(Q)
    fit_seconds = prediction_seconds = risk_seconds = 0.0
    approx_mac = 0
    solvers: dict[str, int] = {}
    if scope == "GLOBAL":
        fit_start = time.perf_counter()
        weights, solver, mac = _weights(Bmodel, Tmodel, sigma)
        fit_seconds = time.perf_counter()-fit_start
        solvers[solver] = 1
        prediction_start = time.perf_counter()
        prediction = (observations @ weights.T).reshape(worlds, CHANNELS, Q)
        prediction_seconds = time.perf_counter()-prediction_start
        risk_start = time.perf_counter()
        true_risk = _true_risks(weights, Btrue, Ttrue, sigma).reshape(CHANNELS, Q)
        assumed_risk = _true_risks(weights, Bmodel, Tmodel, sigma).reshape(CHANNELS, Q)
        contrast_weights = (weights[3*Q:4*Q]-weights[4*Q:5*Q])/np.sqrt(2)
        contrast_target = (Ttrue[3*Q:4*Q]-Ttrue[4*Q:5*Q])/np.sqrt(2)
        contrast_risk = _true_risks(contrast_weights, Btrue, contrast_target, sigma)
        risk_seconds = time.perf_counter()-risk_start
        approx_mac = mac+worlds*len(points)*CHANNELS*Q+(2*CHANNELS+1)*Q*len(points)*Bmodel.shape[1]
    else:
        for q in range(Q):
            subset = ids[q]
            rows = np.arange(CHANNELS)*Q+q
            Bm, Bt = Bmodel[subset], Btrue[subset]
            Tm, Tt = Tmodel[rows], Ttrue[rows]
            fit_start = time.perf_counter()
            weights, solver, mac = _weights(Bm, Tm, sigma)
            fit_seconds += time.perf_counter()-fit_start
            solvers[solver] = solvers.get(solver, 0)+1
            prediction_start = time.perf_counter()
            prediction[:, :, q] = observations[:, subset] @ weights.T
            prediction_seconds += time.perf_counter()-prediction_start
            risk_start = time.perf_counter()
            true_risk[:, q] = _true_risks(weights, Bt, Tt, sigma)
            assumed_risk[:, q] = _true_risks(weights, Bm, Tm, sigma)
            contrast_risk[q] = _true_risks((weights[3]-weights[4])[None, :]/np.sqrt(2), Bt,
                                           (Tt[3]-Tt[4])[None, :]/np.sqrt(2), sigma)[0]
            risk_seconds += time.perf_counter()-risk_start
            approx_mac += mac+worlds*k*CHANNELS+(2*CHANNELS+1)*k*Bm.shape[1]
    contrast_variance = 1.0-true_rho
    diagnostics = {"scope": scope, "model_rho": float(model_rho), "true_rho": float(true_rho),
                   "sigma": float(sigma), "sensors_consulted_per_query": len(points) if scope == "GLOBAL" else k,
                   "channel_count": CHANNELS, "coefficient_dimension_per_channel": F.shape[1],
                   "latent_dimension": Bmodel.shape[1], "solver_counts": solvers,
                   "true_risk_by_channel_query": true_risk,
                   "assumed_model_risk_by_channel_query": assumed_risk,
                   "true_risk_per_channel": true_risk.mean(axis=1), "true_risk_macro": float(true_risk.mean()),
                   "true_contrast_MSE_by_query": contrast_risk,
                   "contrast_target": "(f_D-f_E)/sqrt(2)", "contrast_variance_denominator": contrast_variance,
                   "true_contrast_NMSE_by_query": contrast_risk/contrast_variance,
                   "model_fit_seconds": fit_seconds, "prediction_seconds": prediction_seconds,
                   "risk_seconds": risk_seconds, "prepare_seconds": prepare_seconds,
                   "selection_seconds": selection_seconds, "total_seconds": time.perf_counter()-start,
                   "approx_MAC": int(approx_mac), "approx_MAC_scope": "solve, weights, prediction, risk; excludes feature/trig preparation",
                   "worlds_are_not_geometry_replicates": True, "MHU_confirmation": False}
    if ids is not None:
        diagnostics["local_sensor_ids"] = ids
    return prediction, diagnostics
