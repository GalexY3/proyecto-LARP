"""Posthoc oracle-band qualification of the frozen spatial sampling probe.

The estimator knows the generating Fourier band and noise variance, common to
all geometries. It is an oracle for this benchmark, not universal information
available to an arbitrary sensor or neural network. It performs no HPO, neural
training, architecture confirmation, or hypothesis-posterior update.
"""
from __future__ import annotations
import os
for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "4"

from pathlib import Path
import argparse
import csv
import importlib.metadata
import json
import platform
import time
import numpy as np

from .artifacts import array_hash, digest, file_hash, utc_now, write_json
from .geometry import Geometry
from .sampling_probe import FourierBank, load_probe_config, probe_labels, common_sensor_noise

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT/"configs/sampling_oracle_v1.json"
VERSION = "sampling_oracle_band_v1"
_CONFIG_HASH = "8f82daecac091c7f580cb5966680dcdbf9306ba43a6a40536d951f631ca1b038"


def load_oracle_config() -> dict:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if digest(config) != _CONFIG_HASH:
        raise ValueError("Frozen oracle config changed; create a new version")
    return config


def fourier_design(points: np.ndarray, modes: np.ndarray, L: float) -> np.ndarray:
    points = np.asarray(points, dtype=np.float64)
    modes = np.asarray(modes, dtype=np.int64)
    if points.ndim != 2 or points.shape[1] != 2 or modes.ndim != 2 or modes.shape[1] != 2:
        raise ValueError("points and modes must be two-dimensional coordinates")
    phase = 2*np.pi/L*((points % L) @ modes.T)
    return np.concatenate((np.cos(phase), np.sin(phase)), axis=-1)


def oracle_operator(design: np.ndarray, query_design: np.ndarray, *, sigma: float,
                    mode_pairs: int, rcond: float = 1e-10) -> tuple[np.ndarray, dict]:
    """Q x n_sensor observation-to-query map, from a single SVD.

    Sphere-normalized Fourier coefficients have covariance I/M. Ridge
    lambda=M*sigma^2 is consequently the LMMSE (optimal *linear*) rule for
    independent known Gaussian noise; it is not the exact sphere posterior.
    """
    design, query_design = np.asarray(design, dtype=np.float64), np.asarray(query_design, dtype=np.float64)
    if design.ndim != 2 or design.shape[1] != 2*mode_pairs or query_design.ndim != 2 or query_design.shape[1] != design.shape[1]:
        raise ValueError("design dimension must be D=2*M")
    if sigma < 0 or not np.isfinite(sigma) or not 0 < rcond < 1:
        raise ValueError("sigma must be nonnegative and rcond must lie in (0,1)")
    U, s, Vt = np.linalg.svd(design, full_matrices=False)
    cutoff = rcond*s[0]
    rank = int(np.sum(s > cutoff))
    ridge = mode_pairs*sigma**2
    if sigma == 0:
        inverse = np.divide(1, s, out=np.zeros_like(s), where=s > cutoff)
        estimator = "minimum_norm_SVD"
    else:
        inverse = s/(s*s+ridge)
        estimator = "LMMSE_ridge"
    coefficient_map = (Vt.T*inverse) @ U.T
    operator = query_design @ coefficient_map
    nullity = design.shape[1]-rank
    spectrum_condition = float(s[0]/s[-1]) if s[-1] > 0 else None
    full_condition = spectrum_condition if rank == design.shape[1] else None
    return operator, {"sensor_count": design.shape[0], "coefficient_dimension_D": design.shape[1],
                       "mode_pairs_M": mode_pairs, "rank": rank, "nullity": nullity,
                       "full_column_rank": rank == design.shape[1], "singular_values": s.tolist(),
                       "sigma_min_returned_spectrum": float(s[-1]),
                       "sigma_min_full_column_problem": float(s[-1]) if nullity == 0 else 0.0,
                       "condition_returned_spectrum": spectrum_condition,
                       "condition_full_column_problem": full_condition,
                       "condition_full_is_infinite_when_nullity_positive": nullity > 0,
                       "SVD_relative_cutoff": rcond, "SVD_absolute_cutoff": float(cutoff),
                       "ridge_lambda": ridge, "estimator": estimator,
                       "coefficient_covariance_diagonal": 1/mode_pairs,
                       "exact_nonlinear_posterior": False}


def load_frozen_inputs(config: dict) -> tuple[dict, dict, dict, np.ndarray]:
    """Read original fields and verify recorded bytes/array hashes; no remake."""
    source = ROOT/config["source_series"]
    names = {"results.json": "source_results_sha256", "common_field_bank.npz": "source_field_bank_sha256",
             "field_manifest.json": "source_field_manifest_sha256"}
    for filename, key in names.items():
        if file_hash(source/filename) != config[key]:
            raise ValueError(f"Frozen source input changed: {filename}")
    results = json.loads((source/"results.json").read_text(encoding="utf-8"))
    field_manifest = json.loads((source/"field_manifest.json").read_text(encoding="utf-8"))
    source_config = load_probe_config()
    with np.load(source/"common_field_bank.npz", allow_pickle=False) as arrays:
        banks = {band: FourierBank(arrays[f"{band}_modes"].copy(), arrays[f"{band}_cosine"].copy(),
                                  arrays[f"{band}_sine"].copy(), source_config["L"])
                 for band in config["bands"]}
        queries = arrays["queries"].copy()
    if array_hash(queries) != field_manifest["query_hash"]:
        raise ValueError("Original query hash changed")
    for band, bank in banks.items():
        if bank.hashes != field_manifest["field_hashes"][band] or not np.allclose(bank.analytic_variance, 1, atol=1e-12):
            raise ValueError("Original field hashes or analytic normalization changed")
        if array_hash(bank.evaluate(queries)) != field_manifest["target_hashes"][band]:
            raise ValueError("Original target values changed")
    if results["status"] != "COMPLETE" or results["completed_cells"] != 144:
        raise ValueError("Source v1 must have its complete frozen matrix")
    return results, source_config, banks, queries


def oracle_identity() -> dict:
    paths = [Path(__file__), CONFIG_PATH, ROOT/"src/larp/sampling_probe.py",
             ROOT/"src/larp/artifacts.py", ROOT/"src/larp/geometry.py", ROOT/"configs/sampling_probe_v1.json"]
    files = {str(p.relative_to(ROOT)).replace("\\", "/"): file_hash(p) for p in paths}
    runtime = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "matplotlib", "psutil")}
    runtime["python"] = platform.python_version()
    runtime["thread_environment"] = {key: os.environ[key] for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}
    return {"files": files, "runtime": runtime, "hash": digest({"files": files, "runtime": runtime})}


def summarize_oracle(records: list[dict]) -> list[dict]:
    keys = sorted(set((r["family"], r["band"], r["noise_sigma"]) for r in records if r["status"] == "COMPLETE"))
    rows = []
    for family, band, sigma in keys:
        native = {r["geometry_seed"]: r for r in records if r["status"] == "COMPLETE" and
                  (r["family"], r["band"], r["noise_sigma"], r["condition"]) == (family, band, sigma, "native")}
        shuffle = {r["geometry_seed"]: r for r in records if r["status"] == "COMPLETE" and
                   (r["family"], r["band"], r["noise_sigma"], r["condition"]) == (family, band, sigma, "shuffle")}
        seeds = sorted(set(native)&set(shuffle))
        if not seeds:
            continue
        a = np.asarray([native[s]["MSE_macro"] for s in seeds])
        b = np.asarray([shuffle[s]["MSE_macro"] for s in seeds])
        rows.append({"family": family, "band": band, "noise_sigma": sigma,
                     "paired_geometry_count": len(seeds), "native_MSE_mean": float(a.mean()),
                     "shuffle_MSE_mean": float(b.mean()), "native_MSE_geometry_SD": float(a.std(ddof=1)) if len(a)>1 else None,
                     "shuffle_MSE_geometry_SD": float(b.std(ddof=1)) if len(b)>1 else None,
                     "native_minus_shuffle_MSE_by_geometry": (a-b).tolist(),
                     "native_minus_shuffle_MSE_mean": float((a-b).mean()), "inference": "descriptive_posthoc_oracle"})
    return rows


def run_oracle(output_dir: str | Path = ROOT/"artifacts/sampling_oracle/v1") -> dict:
    config, identity = load_oracle_config(), oracle_identity()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    freeze = {"version": VERSION, "created": utc_now(), "config": config, "config_hash": digest(config),
              "local_identity": identity, "posthoc": True, "before_oracle_scores": True,
              "no_hpo": True, "MHU_confirmation": False, "architecture_evidence": False}
    freeze_path = output_dir/"preregistration.json"
    if freeze_path.exists():
        old = json.loads(freeze_path.read_text(encoding="utf-8"))
        if old["config_hash"] != freeze["config_hash"] or old["local_identity"]["hash"] != identity["hash"]:
            raise FileExistsError("Frozen oracle provenance changed; use another series directory")
        if (output_dir/"results.json").exists():
            previous = json.loads((output_dir/"results.json").read_text(encoding="utf-8"))
            if previous["status"] == "COMPLETE":
                return previous
    else:
        write_json(freeze_path, freeze)
    start = time.perf_counter()
    import psutil
    process = psutil.Process()
    peak_RSS = process.memory_info().rss
    source, source_config, banks, queries = load_frozen_inputs(config)
    targets = {b: bank.evaluate(queries) for b, bank in banks.items()}
    records, comparisons, geometry_provenance, omissions = [], [], [], []
    for g in source["geometries"]:
        family, seed = g["family"], g["geometry_seed"]
        path = Path(g["path"])
        if file_hash(path) != g["file_hash"]:
            raise ValueError("Source geometry byte hash changed")
        geometry = Geometry.load(path)
        if geometry.hashes != g["hashes"]:
            raise ValueError("Source geometry array hashes changed")
        geometry_provenance.append({**g, "original_byte_hash_verified": True, "original_array_hashes_verified": True})
        if time.perf_counter()-start >= config["maximum_seconds"]:
            omissions.append({"family": family, "geometry_seed": seed, "reason": "RESOURCE_LIMIT_NOT_RUN"})
            continue
        noise = common_sensor_noise(seed, source_config)
        all_values = {b: bank.evaluate(geometry.points) for b, bank in banks.items()}
        for condition in config["mark_conditions"]:
            labels = probe_labels(geometry.labels, condition, seed, source_config)
            for band, bank in banks.items():
                query_design = fourier_design(queries, bank.modes, geometry.L)
                for sigma in config["noise_sigma"]:
                    source_cells = [r for r in source["records"] if
                                    (r["family"], r["geometry_seed"], r["condition"], r["band"], r["noise_sigma"]) ==
                                    (family, seed, condition, band, sigma)]
                    if len(source_cells) != 2 or any(r["noise_hash"] != array_hash(noise) or
                        r["labels_hash"] != array_hash(labels) or r["target_hash"] != array_hash(targets[band]) for r in source_cells):
                        raise ValueError("Common noise, marks or targets differ from v1")
                    prediction = []
                    diagnostics = []
                    for c in range(5):
                        sensors = np.flatnonzero(labels == c)
                        design = fourier_design(geometry.points[sensors], bank.modes, geometry.L)
                        operator, report = oracle_operator(design, query_design, sigma=sigma,
                            mode_pairs=len(bank.modes), rcond=config["SVD_relative_cutoff"])
                        observation = all_values[band][:, c, sensors]+sigma*noise[:, sensors]
                        prediction.append(observation @ operator.T)
                        diagnostics.append({"channel": c, **report})
                    prediction = np.stack(prediction, axis=1)
                    if not np.isfinite(prediction).all():
                        raise ValueError("Nonfinite oracle prediction; no zero imputation")
                    world_channel_mse = np.mean((prediction-targets[band])**2, axis=-1)
                    mse = float(world_channel_mse.mean())
                    record = {"status": "COMPLETE", "family": family, "geometry_seed": seed, "condition": condition,
                              "band": band, "noise_sigma": sigma, "coordinates_hash": geometry.hashes["points"],
                              "labels_hash": array_hash(labels), "noise_hash": array_hash(noise),
                              "target_hash": array_hash(targets[band]), "prediction_hash": array_hash(prediction),
                              "MSE_macro": mse, "MSE_per_channel": world_channel_mse.mean(axis=0).tolist(),
                              "world_macro_MSE": world_channel_mse.mean(axis=1).tolist(),
                              "channel_design_diagnostics": diagnostics, "neural_accuracy": False}
                    records.append(record)
                    for comparator in source_cells:
                        original = comparator["score"]["MSE_macro"]
                        comparisons.append({"family": family, "geometry_seed": seed, "condition": condition,
                                            "band": band, "noise_sigma": sigma, "v1_estimator": comparator["estimator"],
                                            "v1_MSE_macro": original, "oracle_MSE_macro": mse,
                                            "oracle_minus_v1_MSE": mse-original,
                                            "new_independent_replication": False})
        peak_RSS = max(peak_RSS, process.memory_info().rss)
        write_json(output_dir/"partial_results.json", {"status": "RUNNING", "records": records,
                                                       "comparisons": comparisons, "posthoc": True})
    status = "COMPLETE" if not omissions and len(records) == config["expected_unique_oracle_cells"] else "INCOMPLETE_MATRIX"
    result = {"version": VERSION, "status": status, "config_hash": digest(config), "local_identity_hash": identity["hash"],
              "unique_oracle_cells": len(records), "expected_unique_oracle_cells": config["expected_unique_oracle_cells"],
              "v1_comparison_rows": len(comparisons), "comparison_rows_are_not_replicates": True,
              "records": records, "comparisons": comparisons, "summary": summarize_oracle(records),
              "geometry_provenance": geometry_provenance, "omissions": omissions,
              "seconds": time.perf_counter()-start, "peak_RSS_bytes": peak_RSS, "posthoc": True,
              "no_hpo": True, "oracle_information": config["oracle_information"], "neural_training": False,
              "architecture_evidence": False, "MHU_confirmation": False, "beliefs_updated": False}
    result["budget_exceeded"] = result["seconds"] > config["maximum_seconds"]
    write_json(output_dir/"results.json", result)
    if result["summary"]:
        with (output_dir/"summary.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(result["summary"][0]))
            writer.writeheader()
            writer.writerows({key: json.dumps(value) if isinstance(value, list) else value for key, value in row.items()}
                            for row in result["summary"])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT/"artifacts/sampling_oracle/v1")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps({"config": load_oracle_config(), "identity": oracle_identity(), "posthoc": True}, indent=2))
    else:
        r = run_oracle(args.output_dir)
        print(json.dumps({k: r[k] for k in ("status", "unique_oracle_cells", "v1_comparison_rows", "seconds", "peak_RSS_bytes", "beliefs_updated")}, indent=2))
