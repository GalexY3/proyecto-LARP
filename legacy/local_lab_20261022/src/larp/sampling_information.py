"""Finite-query information/risk diagnostic on frozen sampling observations.

This evaluates ensemble expectations for existing linear estimators. Historical
fields are reused as comparators, not independent confirmation. No generators,
optimizer, training, or architectural belief update is invoked.
"""
from __future__ import annotations

import os
for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "4"

import argparse
import json
from pathlib import Path
import platform
import time
import numpy as np

from .artifacts import array_hash, digest, file_hash, utc_now
from .geometry import Geometry
from .sampling_oracle import fourier_design, load_frozen_inputs, load_oracle_config
from .sampling_probe import interpolation_weights, probe_labels

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs/sampling_information_v1.json"
CONFIG_HASH = "2cadcaccb58c764458bf6970ec5188d44da1bcf76cbe4fc8c30f3a3c462e18e2"


def write_exclusive(path: Path, data: dict) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=True, allow_nan=False, indent=2)
        stream.write("\n")


def load_config() -> dict:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if digest(config) != CONFIG_HASH:
        raise ValueError("Frozen information config changed; create another version")
    return config


def gram_from_density(points: np.ndarray, modes: np.ndarray, L: float) -> tuple[np.ndarray, dict]:
    """Real cosine/sine Gram from density amplitudes at mode sums/differences."""
    points, modes = np.asarray(points, dtype=float), np.asarray(modes, dtype=int)
    differences = modes[None, :, :] - modes[:, None, :]
    sums = modes[:, None, :] + modes[None, :, :]
    all_modes = np.concatenate((differences.reshape(-1, 2), sums.reshape(-1, 2)))
    unique, inverse = np.unique(all_modes, axis=0, return_inverse=True)
    rho = np.exp(2j*np.pi/L*((points % L) @ unique.T)).sum(axis=0)
    M = len(modes)
    difference = rho[inverse[:M*M]].reshape(M, M)
    total = rho[inverse[M*M:]].reshape(M, M)
    cc = (difference.real + total.real)/2
    ss = (difference.real - total.real)/2
    cs = (difference.imag + total.imag)/2
    gram = np.block([[cc, cs], [cs.T, ss]])
    return gram, {"density_mode_count_including_zero_and_signs": len(unique),
                  "maximum_density_mode_norm": float(np.linalg.norm(unique, axis=1).max()),
                  "required_density_modes": unique.tolist()}


def design_diagnostic(A: np.ndarray, Q: np.ndarray, *, M: int,
                      rcond: float) -> tuple[dict, dict]:
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    cutoff = rcond*s[0]
    retained = s > cutoff
    V = Vt[retained].T
    observed = V @ V.T
    null = np.eye(A.shape[1]) - observed
    null_floor = float(np.sum((Q @ null)**2)/(M*len(Q)))
    report = {"sensor_count": len(A), "dimension": A.shape[1],
              "rank": int(retained.sum()), "numerical_nullity": A.shape[1]-int(retained.sum()),
              "minimum_nullity_from_count": max(0, A.shape[1]-len(A)),
              "relative_cutoff": rcond, "absolute_cutoff": float(cutoff),
              "singular_values": s.tolist(),
              "query_weighted_noiseless_null_floor": null_floor,
              "uniform_continuous_torus_null_floor": (A.shape[1]-int(retained.sum()))/(2*M),
              "null_floor_is_numerical_rank_dependent": True}
    return report, {"U": U, "s": s, "Vt": Vt, "observed": observed, "null": null}


def linear_risk(A: np.ndarray, Q: np.ndarray, H: np.ndarray, *, M: int,
                sigma: float, observed: np.ndarray, null: np.ndarray) -> dict:
    """True ensemble MSE of H y; H may be mismatched to the field model."""
    if M <= 0 or sigma < 0 or not np.isfinite(sigma):
        raise ValueError("Invalid covariance or noise")
    if A.ndim != 2 or Q.ndim != 2 or H.shape != (len(Q), len(A)) or A.shape[1] != Q.shape[1]:
        raise ValueError("Incompatible observation, target or estimator dimensions")
    if not all(np.isfinite(x).all() for x in (A, Q, H, observed, null)):
        raise ValueError("Nonfinite matrix")
    bias = H @ A - Q
    unresolved = float(np.sum((bias @ null)**2)/(M*len(Q)))
    resolved = float(np.sum((bias @ observed)**2)/(M*len(Q)))
    noise = float(sigma**2*np.sum(H**2)/len(Q))
    direct = float(np.sum(bias**2)/(M*len(Q)) + noise)
    return {"expected_MSE": direct, "nullspace_bias_component": unresolved,
            "observed_subspace_bias_component": resolved, "noise_component": noise,
            "decomposition_error": abs(direct-unresolved-resolved-noise)}


def oracle_maps(Q: np.ndarray, svd: dict, *, M: int, sigma: float,
                rcond: float) -> tuple[np.ndarray, np.ndarray]:
    s = svd["s"]
    if sigma == 0:
        inverse = np.divide(1, s, out=np.zeros_like(s), where=s > rcond*s[0])
    else:
        inverse = s/(s*s+M*sigma**2)
    K = (svd["Vt"].T * inverse) @ svd["U"].T
    return Q @ K, K


def uniform_oracle_risk(A: np.ndarray, K: np.ndarray, *, M: int,
                        sigma: float, observed: np.ndarray, null: np.ndarray) -> dict:
    # Continuous uniform queries have E[phi(q)phi(q)^T]=I/2; no new queries drawn.
    residual = K @ A - np.eye(A.shape[1])
    unresolved = float(np.sum((residual @ null)**2)/(2*M))
    resolved = float(np.sum((residual @ observed)**2)/(2*M))
    noise = float(sigma**2*np.sum(K**2)/2)
    return {"expected_MSE": unresolved+resolved+noise,
            "nullspace_bias_component": unresolved,
            "observed_subspace_bias_component": resolved, "noise_component": noise}


def summarize(records: list[dict]) -> list[dict]:
    rows = []
    keys = sorted({(r["family"], r["condition"], r["band"], r["noise_sigma"], r["estimator"]) for r in records})
    for key in keys:
        cells = [r for r in records if (r["family"], r["condition"], r["band"], r["noise_sigma"], r["estimator"]) == key]
        row = dict(zip(("family", "condition", "band", "noise_sigma", "estimator"), key))
        row["geometry_count"] = len(cells)
        for metric in ("expected_MSE", "nullspace_bias_component", "observed_subspace_bias_component", "noise_component", "historical_empirical_MSE"):
            values = [c[metric] for c in cells]
            row[metric+"_mean"] = float(np.mean(values))
            row[metric+"_by_geometry"] = values
        if key[-1] == "oracle_band":
            row["uniform_continuous_expected_MSE_mean"] = float(np.mean([c["uniform_continuous_risk"]["expected_MSE"] for c in cells]))
        rows.append(row)
    return rows


def run(output: Path) -> dict:
    config = load_config()
    if output.exists() and any((output / name).exists() for name in ("protocol_freeze.json", "results.json")):
        raise FileExistsError("Use a fresh output directory; immutable evidence is never overwritten")
    output.mkdir(parents=True, exist_ok=True)
    source_oracle = ROOT / config["source_oracle_results"]
    if file_hash(source_oracle) != config["source_oracle_sha256"]:
        raise ValueError("Historical oracle changed")
    oracle = json.loads(source_oracle.read_text(encoding="utf-8"))
    source, probe_config, banks, queries = load_frozen_inputs(load_oracle_config())
    inputs = {str(source_oracle.relative_to(ROOT)): file_hash(source_oracle)}
    for filename in ("results.json", "common_field_bank.npz", "field_manifest.json"):
        path = ROOT / "artifacts/sampling_probe/v1" / filename
        inputs[str(path.relative_to(ROOT)).replace("\\", "/")] = file_hash(path)
    for g in source["geometries"]:
        path = Path(g["path"])
        if file_hash(path) != g["file_hash"]:
            raise ValueError("Historical geometry changed")
        inputs[str(path.relative_to(ROOT)).replace("\\", "/")] = file_hash(path)
    dependencies = [Path(__file__), CONFIG_PATH, ROOT/"src/larp/sampling_probe.py",
                    ROOT/"src/larp/sampling_oracle.py", ROOT/"src/larp/geometry.py", ROOT/"src/larp/artifacts.py",
                    ROOT/"configs/sampling_probe_v1.json", ROOT/"configs/sampling_oracle_v1.json"]
    identity = {str(p.relative_to(ROOT)).replace("\\", "/"): file_hash(p) for p in dependencies}
    write_exclusive(output/"protocol_freeze.json", {"config": config, "config_hash": digest(config),
        "created": utc_now(), "inputs": inputs, "identity": identity,
        "runtime": {"python": platform.python_version(), "numpy": np.__version__,
                    "pid": os.getpid(), "ppid": os.getppid(), "threads": config["threads"]},
        "before_new_diagnostic_scores": True, "historical_results_already_observed": True,
        "stage": "posthoc_algebraic_diagnostic", "new_fields_or_geometries": False})
    start = time.perf_counter()
    records, designs, query_reports = [], [], []
    max_identity_error = 0.0
    max_decomposition_error = 0.0
    for band, bank in banks.items():
        Q = fourier_design(queries, bank.modes, probe_config["L"])
        eig = np.linalg.eigvalsh(Q.T @ Q / len(Q))
        query_reports.append({"band": band, "query_count": len(Q), "dimension": Q.shape[1],
            "rank": int(np.linalg.matrix_rank(Q, tol=config["SVD_relative_cutoff"]*np.linalg.norm(Q, 2))),
            "query_second_moment_eigenvalues": eig.tolist(),
            "max_departure_from_uniform_torus_second_moment": float(np.max(np.abs(eig-.5))),
            "query_hash": array_hash(queries), "coefficient_variance": 1/len(bank.modes)})
    omissions = []
    for g in source["geometries"]:
        if time.perf_counter()-start > config["maximum_numeric_seconds"]:
            omissions.append({"family": g["family"], "seed": g["geometry_seed"], "status": "RESOURCE_LIMIT_NOT_RUN"})
            continue
        geometry = Geometry.load(g["path"])
        if geometry.hashes != g["hashes"]:
            raise ValueError("Historical geometry arrays changed")
        for condition in config["conditions"]:
            labels = probe_labels(geometry.labels, condition, g["geometry_seed"], probe_config)
            local_weights = {name: interpolation_weights(geometry.points, labels, queries, geometry.L, name,
                probe_config["kernel_length_scale"], probe_config["kernel_cutoff_in_length_scales"])[0]
                for name in ("nearest_neighbor", "local_gaussian")}
            for band, bank in banks.items():
                M = len(bank.modes)
                Q = fourier_design(queries, bank.modes, geometry.L)
                channel_diagnostics, risks = [], {(sigma, est): [] for sigma in config["noise_sigma"] for est in config["estimators"]}
                uniform_risks = {sigma: [] for sigma in config["noise_sigma"]}
                for c in range(5):
                    if time.perf_counter()-start >= config["maximum_numeric_seconds"]:
                        raise TimeoutError("Numerical deadline reached; this frozen series cannot be rerun")
                    ids = np.flatnonzero(labels == c)
                    points = geometry.points[ids]
                    A = fourier_design(points, bank.modes, geometry.L)
                    diag, svd = design_diagnostic(A, Q, M=M, rcond=config["SVD_relative_cutoff"])
                    density_gram, density_report = gram_from_density(points, bank.modes, geometry.L)
                    gram_error = float(np.max(np.abs(density_gram - A.T @ A)))
                    max_identity_error = max(max_identity_error, gram_error)
                    certificate_modes = np.asarray(config["density_modes_halfspace"])
                    rho = np.exp(2j*np.pi/geometry.L*(points @ certificate_modes.T)).sum(axis=0)
                    diag.update({"family": g["family"], "geometry_seed": g["geometry_seed"], "condition": condition,
                        "band": band, "channel": c, "density_gram_identity_max_error": gram_error,
                        "density_modes": density_report, "six_mode_S_mean": float(np.mean(np.abs(rho)**2/len(ids))),
                        "coordinates_hash": geometry.hashes["points"], "labels_hash": array_hash(labels)})
                    designs.append(diag)
                    channel_diagnostics.append(diag)
                    for sigma in config["noise_sigma"]:
                        H, K = oracle_maps(Q, svd, M=M, sigma=sigma, rcond=config["SVD_relative_cutoff"])
                        uniform_risks[sigma].append(uniform_oracle_risk(A, K, M=M, sigma=sigma,
                            observed=svd["observed"], null=svd["null"]))
                        for est in config["estimators"]:
                            rule = H if est == "oracle_band" else local_weights[est][c][:, ids]
                            risk = linear_risk(A, Q, rule, M=M, sigma=sigma, observed=svd["observed"], null=svd["null"])
                            max_decomposition_error = max(max_decomposition_error, risk["decomposition_error"])
                            risks[sigma, est].append({"channel": c, **risk})
                for (sigma, est), per_channel in risks.items():
                    key = (g["family"], g["geometry_seed"], condition, band, sigma)
                    if est == "oracle_band":
                        old = [r for r in oracle["records"] if (r["family"], r["geometry_seed"], r["condition"], r["band"], r["noise_sigma"]) == key]
                        empirical = old[0]["MSE_macro"] if len(old) == 1 else None
                    else:
                        old = [r for r in source["records"] if (r["family"], r["geometry_seed"], r["condition"], r["band"], r["noise_sigma"]) == key and r["estimator"] == est]
                        empirical = old[0]["score"]["MSE_macro"] if len(old) == 1 else None
                    if empirical is None:
                        raise ValueError("Historical cell must resolve exactly once")
                    if old[0]["labels_hash"] != array_hash(labels):
                        raise ValueError("Historical cell marks do not match reconstructed marks")
                    if "coordinates_hash" in old[0] and old[0]["coordinates_hash"] != geometry.hashes["points"]:
                        raise ValueError("Historical cell coordinates do not match geometry")
                    record = dict(zip(("family", "geometry_seed", "condition", "band", "noise_sigma"), key))
                    record.update({"estimator": est, "channel_risks": per_channel, "historical_empirical_MSE": empirical})
                    for metric in ("expected_MSE", "nullspace_bias_component", "observed_subspace_bias_component", "noise_component"):
                        record[metric] = float(np.mean([r[metric] for r in per_channel]))
                    if est == "oracle_band":
                        record["uniform_continuous_risk"] = {metric: float(np.mean([r[metric] for r in uniform_risks[sigma]]))
                            for metric in uniform_risks[sigma][0]}
                    records.append(record)
    numeric_seconds = time.perf_counter()-start
    checks = {"nine_geometries": len(source["geometries"]) == config["expected_geometry_count"],
              "all_designs": len(designs) == config["expected_designs"],
              "all_cells": len(records) == config["expected_cells"], "no_omissions": not omissions,
              "within_numeric_budget": numeric_seconds <= config["maximum_numeric_seconds"],
              "density_gram_identity": max_identity_error <= config["identity_absolute_tolerance"],
              "risk_decomposition": max_decomposition_error <= config["risk_decomposition_absolute_tolerance"]}
    result = {"version": config["version"], "status": "COMPLETE" if all(checks.values()) else "INCOMPLETE_OR_INVALID",
              "checks": checks, "numeric_seconds": numeric_seconds, "query_reports": query_reports,
              "designs": designs, "records": records, "summary": summarize(records), "omissions": omissions,
              "max_density_gram_identity_error": max_identity_error, "max_risk_decomposition_error": max_decomposition_error,
              "new_fields": 0, "new_geometries": 0, "neural_training": False, "architecture_evidence": False,
              "historical_beliefs_updated": False, "confirmatory": False,
              "interpretation": "Known covariance algebra and posthoc diagnosis; not new independent evidence"}
    write_exclusive(output/"results.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT/"artifacts/sampling_information/v1")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps(load_config(), indent=2))
    else:
        result = run(args.output_dir)
        print(json.dumps({k: result[k] for k in ("status", "checks", "numeric_seconds", "max_density_gram_identity_error", "max_risk_decomposition_error")}))
