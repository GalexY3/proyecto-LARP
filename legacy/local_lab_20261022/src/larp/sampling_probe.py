"""Frozen spatial-observability probe; no learned network or architecture posterior.

Targets are common continuous Fourier fields independent of sensor marks. Each
sensor reads its marked channel. Five channel errors receive equal weight, so
the numerous A sensors cannot dominate the macro score. This experiment changes
observations when marks move and therefore is not a test of internal computation.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import csv
import importlib.metadata
import json
import platform
import time
import os
from contextlib import nullcontext

# The standalone module entry point reaches this before importing NumPy. These
# limits do not retroactively reconfigure BLAS in an already initialized process.
for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "4"
import numpy as np

from .artifacts import array_hash, digest, file_hash, utc_now, write_json
from .geometry import Geometry, generate_geometry, minimum_image

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs/sampling_probe_v1.json"
VERSION = "spatial_sampling_probe_v1"
_CONFIG_HASH = "8456858c73122c19db3cf846ab7913820e064388d4b04644d5fd58124df98de2"


def load_probe_config() -> dict:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if digest(config) != _CONFIG_HASH:
        raise ValueError("Frozen sampling v1 changed; create a new version instead")
    return config


def fourier_modes(lower: float, upper: float) -> np.ndarray:
    """One representative of each real Fourier +/- pair; no zero mode."""
    if not 0 < lower <= upper:
        raise ValueError("Expected a strictly positive ordered frequency band")
    stop = int(np.ceil(upper))
    modes = [(a, b) for a in range(stop+1) for b in range(-stop, stop+1)
             if (a > 0 or a == 0 and b > 0)
             and lower**2-1e-12 <= a*a+b*b <= upper**2+1e-12]
    modes.sort(key=lambda n: (n[0]*n[0]+n[1]*n[1], n[0], n[1]))
    if not modes:
        raise ValueError("Frequency band has no integer modes")
    return np.asarray(modes, dtype=np.int64)


@dataclass(frozen=True)
class FourierBank:
    modes: np.ndarray
    cosine: np.ndarray  # worlds, channels, modes
    sine: np.ndarray
    L: float

    @property
    def hashes(self) -> dict:
        return {"modes": array_hash(self.modes), "cosine": array_hash(self.cosine),
                "sine": array_hash(self.sine)}

    @property
    def analytic_variance(self) -> np.ndarray:
        return np.sum(self.cosine**2+self.sine**2, axis=-1)/2

    def evaluate(self, positions: np.ndarray) -> np.ndarray:
        """World x channel x point values, without geometry-dependent centering."""
        positions = np.asarray(positions, dtype=np.float64)
        if positions.ndim != 2 or positions.shape[1] != 2 or not np.isfinite(positions).all():
            raise ValueError("Positions must be finite (N,2)")
        phase = (2*np.pi/self.L)*(self.modes @ (positions % self.L).T)
        return np.einsum("wcm,mn->wcn", self.cosine, np.cos(phase), optimize=True) + np.einsum(
            "wcm,mn->wcn", self.sine, np.sin(phase), optimize=True)


def make_field_bank(band: str, config: dict | None = None) -> FourierBank:
    config = load_probe_config() if config is None else config
    bands = list(config["field_bands"])
    if band not in bands:
        raise ValueError("Unknown field band")
    modes = fourier_modes(*config["field_bands"][band])
    rng = np.random.default_rng(np.random.SeedSequence(
        [config["master_seed"], config["field_namespace"], bands.index(band)]))
    coefficients = rng.normal(size=(2, config["worlds_per_band"], config["channels"], len(modes)))
    normalization = np.sqrt(np.sum(coefficients**2, axis=(0, 3))/2)
    coefficients /= normalization[None, :, :, None]
    return FourierBank(modes, coefficients[0], coefficients[1], float(config["L"]))


def query_sites(config: dict | None = None) -> np.ndarray:
    config = load_probe_config() if config is None else config
    side, L = config["query_world_side"], config["L"]
    return np.asarray([(L*a/side+.5, L*b/side+.5) for a in range(side) for b in range(side)]) % L


def probe_labels(labels: np.ndarray, condition: str, geometry_seed: int,
                 config: dict | None = None) -> np.ndarray:
    config = load_probe_config() if config is None else config
    labels = np.array(labels, dtype=np.int64, copy=True)
    if condition == "native":
        return labels
    if condition != "shuffle":
        raise ValueError("Only native and fixed-count shuffle marks are preregistered")
    rng = np.random.default_rng(np.random.SeedSequence(
        [config["master_seed"], config["shuffle_namespace"], geometry_seed]))
    return rng.permutation(labels)


def common_sensor_noise(geometry_seed: int, config: dict | None = None) -> np.ndarray:
    """One standard normal noise per world and node ID, common to all conditions."""
    config = load_probe_config() if config is None else config
    rng = np.random.default_rng(np.random.SeedSequence(
        [config["master_seed"], config["noise_namespace"], geometry_seed]))
    return rng.normal(size=(config["worlds_per_band"], config["N"]))


def interpolation_weights(points: np.ndarray, labels: np.ndarray, queries: np.ndarray,
                          L: float, estimator: str, length_scale: float = 1.25,
                          cutoff_scales: float = 2.0) -> tuple[list[np.ndarray], dict]:
    """Per-channel Q x N weights; empty local support falls back to nearest."""
    points, queries = np.asarray(points, dtype=float), np.asarray(queries, dtype=float)
    labels = np.asarray(labels, dtype=np.int64)
    if labels.shape != (len(points),) or np.any(labels < 0) or np.any(labels >= 5):
        raise ValueError("Expected five-channel marks for every point")
    if estimator not in ("nearest_neighbor", "local_gaussian") or length_scale <= 0 or cutoff_scales <= 0:
        raise ValueError("Invalid fixed estimator")
    distances = np.linalg.norm(minimum_image(queries[:, None]-points[None], L), axis=-1)
    cutoff = length_scale*cutoff_scales
    weights, coverage = [], []
    for channel in range(5):
        indices = np.flatnonzero(labels == channel)
        if not len(indices):
            raise ValueError("Every channel must have at least one sensor")
        d = distances[:, indices]
        nearest = np.argmin(d, axis=1)  # sorted node IDs break exact ties
        nearest_d = d[np.arange(len(queries)), nearest]
        local = np.zeros_like(d)
        fallback = np.zeros(len(queries), dtype=bool)
        if estimator == "local_gaussian":
            local = np.exp(-.5*(d/length_scale)**2)*(d <= cutoff)
            fallback = local.sum(axis=1) == 0
            local[fallback, nearest[fallback]] = 1.0
            local /= local.sum(axis=1, keepdims=True)
        else:
            local[np.arange(len(queries)), nearest] = 1.0
        full = np.zeros((len(queries), len(points)))
        full[:, indices] = local
        weights.append(full)
        coverage.append({"channel": channel, "sensor_count": len(indices),
                         "nearest_distance_mean": float(nearest_d.mean()),
                         "nearest_distance_median": float(np.median(nearest_d)),
                         "nearest_distance_p90": float(np.quantile(nearest_d, .9)),
                         "nearest_distance_p95": float(np.quantile(nearest_d, .95)),
                         "nearest_distance_max": float(nearest_d.max()),
                         "query_void_fraction_at_cutoff": float(np.mean(nearest_d > cutoff)),
                         "kernel_fallback_fraction": float(fallback.mean())})
    report = {"channels": coverage, "cutoff": cutoff,
              "nearest_distance_mean_macro": float(np.mean([c["nearest_distance_mean"] for c in coverage])),
              "void_fraction_macro": float(np.mean([c["query_void_fraction_at_cutoff"] for c in coverage]))}
    return weights, report


def score_observations(observations: np.ndarray, weights: list[np.ndarray],
                       target: np.ndarray) -> dict:
    """MSE with equal channel weighting; fields' analytic variance is exactly 1."""
    observations, target = np.asarray(observations), np.asarray(target)
    if observations.ndim != 2 or target.ndim != 3 or target.shape[:2] != (len(observations), 5):
        raise ValueError("Expected observations (W,N) and targets (W,5,Q)")
    prediction = np.stack([observations @ w.T for w in weights], axis=1)
    if prediction.shape != target.shape or not np.isfinite(prediction).all():
        raise ValueError("Prediction shape mismatch or nonfinite prediction")
    world_channel_mse = np.mean((prediction-target)**2, axis=-1)
    return {"MSE_per_channel": world_channel_mse.mean(axis=0).tolist(),
            "MSE_macro": float(world_channel_mse.mean()),
            "world_macro_MSE": world_channel_mse.mean(axis=1).tolist(),
            "world_channel_MSE_hash": array_hash(world_channel_mse),
            "prediction_hash": array_hash(prediction), "score_is_neural_accuracy": False}


def probe_local_identity() -> dict:
    paths = [Path(__file__), CONFIG_PATH, ROOT/"src/larp/artifacts.py", ROOT/"src/larp/geometry.py",
             ROOT/"src/larp/avian.py", ROOT/"configs/avian_v1.json"]
    files = {str(path.relative_to(ROOT)).replace("\\", "/"): file_hash(path) for path in paths if path.exists()}
    runtime = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "matplotlib")}
    runtime["python"] = platform.python_version()
    runtime["thread_environment"] = {key: os.environ.get(key) for key in
                                   ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}
    return {"files": files, "runtime": runtime, "hash": digest({"files": files, "runtime": runtime})}


def _load_geometry(family: str, seed: int, output_dir: Path, config: dict) -> tuple[Geometry | None, Path]:
    if family == "nominal_mhu":
        path = ROOT / f"artifacts/geometry/mhu_N400_g{seed}.npz"
        if not path.exists():
            path = output_dir / f"geometries/mhu_N400_g{seed}.npz"
            if not path.exists() and config["generate_missing_nominal"]:
                generate_geometry(N=config["N"], seed=seed, kind="mhu").save(path)
    else:
        treatment = family.removeprefix("avian_")
        path = ROOT / f"artifacts/avian_v1/avian_{treatment}_N400_g{seed}.npz"
    return (Geometry.load(path) if path.exists() else None), path


def _summary(records: list[dict], config: dict) -> list[dict]:
    rows = []
    for family in config["families"]:
        for band in config["field_bands"]:
            for estimator in config["estimators"]:
                for sigma in config["noise_sigma"]:
                    cells = [r for r in records if r.get("status") == "COMPLETE" and
                             (r["family"], r["band"], r["estimator"], r["noise_sigma"]) ==
                             (family, band, estimator, sigma)]
                    native = {r["geometry_seed"]: r for r in cells if r["condition"] == "native"}
                    shuffle = {r["geometry_seed"]: r for r in cells if r["condition"] == "shuffle"}
                    seeds = [seed for seed in config["geometry_seeds"] if seed in native and seed in shuffle]
                    if not seeds:
                        continue
                    row = {"family": family, "band": band, "estimator": estimator,
                           "noise_sigma": sigma, "paired_geometry_count": len(seeds),
                           "complete_three_geometry_pairs": len(seeds) == len(config["geometry_seeds"])}
                    for condition, mapping in (("native", native), ("shuffle", shuffle)):
                        values = np.asarray([mapping[s]["score"]["MSE_macro"] for s in seeds])
                        row[f"{condition}_MSE_mean"] = float(values.mean())
                        row[f"{condition}_MSE_geometry_sd"] = float(values.std(ddof=1)) if len(values) > 1 else None
                    delta = np.asarray([native[s]["score"]["MSE_macro"]-shuffle[s]["score"]["MSE_macro"] for s in seeds])
                    row["native_minus_shuffle_MSE_per_geometry"] = delta.tolist()
                    row["native_minus_shuffle_MSE_mean"] = float(delta.mean())
                    row["native_minus_shuffle_MSE_geometry_sd"] = float(delta.std(ddof=1)) if len(delta) > 1 else None
                    row["inference"] = "descriptive_only; worlds_and_channels_are_not_architecture_replicates"
                    rows.append(row)
    return rows


def _plot_results(summary: list[dict], output_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 7), constrained_layout=True)
    colors = {"nominal_mhu": "#65758b", "avian_full_spectral": "#d96a32", "avian_local_only": "#2b8a80"}
    for row_index, band in enumerate(("smooth", "fine")):
        for col_index, estimator in enumerate(("nearest_neighbor", "local_gaussian")):
            ax = axes[row_index, col_index]
            cells = [r for r in summary if r["band"] == band and r["estimator"] == estimator and r["noise_sigma"] == .1]
            for family_index, row in enumerate(cells):
                for condition_index, condition in enumerate(("native", "shuffle")):
                    x = 2*family_index+condition_index
                    ax.errorbar(x, row[f"{condition}_MSE_mean"],
                                yerr=row[f"{condition}_MSE_geometry_sd"], marker="o",
                                color=colors[row["family"]], capsize=4)
            ax.set_xticks(np.arange(2*len(cells)), [f"{r['family'].replace('avian_', '')}\n{c}"
                          for r in cells for c in ("native", "shuffle")], rotation=20, fontsize=8)
            ax.set_title(f"{band} · {estimator}")
            ax.set_ylabel("MSE macro; media ± SD de 3 geometrías")
            ax.grid(axis="y", alpha=.2)
    fig.suptitle("Muestreo de cinco canales · ruido σ=.1 · sin red neuronal")
    fig.savefig(output_dir/"sampling_MSE.png", dpi=160)
    plt.close(fig)


def run_sampling_probe(output_dir: str | Path | None = None) -> dict:
    """Freeze first, then execute bounded complete matrix or record every omission."""
    config = load_probe_config()
    output_dir = Path(output_dir) if output_dir is not None else ROOT/"artifacts/sampling_probe/v1"
    output_dir.mkdir(parents=True, exist_ok=True)
    identity = probe_local_identity()
    prereg = {"version": VERSION, "created": utc_now(), "config": config, "config_hash": digest(config),
              "local_identity": identity, "no_hpo": True, "neural_training": False,
              "architecture_evidence": False, "beliefs_updated": False}
    prereg_path = output_dir/"preregistration.json"
    if prereg_path.exists():
        existing = json.loads(prereg_path.read_text(encoding="utf-8"))
        if existing["config_hash"] != prereg["config_hash"] or existing["local_identity"]["hash"] != identity["hash"]:
            raise FileExistsError("This probe series has different frozen provenance; use a new output directory")
        if (output_dir/"results.json").exists():
            prior = json.loads((output_dir/"results.json").read_text(encoding="utf-8"))
            if prior["status"] == "COMPLETE":
                return prior
            # Resume of a missing-geometry/budget series may complete the matrix,
            # but its previously observed failure/omission record is retained.
            history = output_dir/f"history/results_{digest(prior)}.json"
            if not history.exists():
                write_json(history, prior)
    else:
        write_json(prereg_path, prereg)  # before worlds/geometries/scores are observed
    start = time.perf_counter()
    records, geometries, missing = [], [], []
    queries = query_sites(config)
    banks = {band: make_field_bank(band, config) for band in config["field_bands"]}
    targets = {band: bank.evaluate(queries) for band, bank in banks.items()}
    bank_arrays = {f"{band}_{kind}": getattr(bank, kind) for band, bank in banks.items()
                   for kind in ("modes", "cosine", "sine")}
    np.savez_compressed(output_dir/"common_field_bank.npz", queries=queries, **bank_arrays)
    rng_manifest = {"query_hash": array_hash(queries), "field_hashes": {b: bank.hashes for b, bank in banks.items()},
                    "target_hashes": {b: array_hash(t) for b, t in targets.items()},
                    "analytic_variance": {b: [float(bank.analytic_variance.min()), float(bank.analytic_variance.max())]
                                          for b, bank in banks.items()}, "seed_keys": config["seed_keys"]}
    write_json(output_dir/"field_manifest.json", rng_manifest)
    timed_out = False
    import psutil
    process = psutil.Process()
    peak_rss = process.memory_info().rss
    # BLAS limits are configured before NumPy in the standalone invocation.
    with nullcontext():
        for family in config["families"]:
            for seed in config["geometry_seeds"]:
                if time.perf_counter()-start >= config["maximum_seconds"]:
                    timed_out = True
                    missing.append({"family": family, "geometry_seed": seed, "status": "RESOURCE_LIMIT_NOT_RUN"})
                    continue
                geometry, path = _load_geometry(family, seed, output_dir, config)
                if geometry is None:
                    missing.append({"family": family, "geometry_seed": seed, "status": "MISSING_GEOMETRY",
                                    "expected_path": str(path)})
                    continue
                if geometry.N != config["N"] or geometry.L != config["L"] or not np.array_equal(
                        np.bincount(geometry.labels, minlength=5), config["counts_A_to_E"]):
                    raise ValueError("Geometry dimensions/counts differ from the frozen sampling estimand")
                cert = geometry.metadata.get("certificate", {})
                admitted = bool(geometry.metadata.get("admitted", cert.get("scientific_admissible", False)))
                geometries.append({"family": family, "geometry_seed": seed, "path": str(path),
                                   "file_hash": file_hash(path), "hashes": geometry.hashes,
                                   "certificate_passed": bool(cert.get("passed", False)), "admitted": admitted,
                                   "local_only_deliberately_not_required_to_be_MHU": family == "avian_local_only",
                                   "generator_version": geometry.metadata.get("generator_version"),
                                   "generator_identity": geometry.metadata.get("local_identity_hash")})
                noise = common_sensor_noise(seed, config)
                all_values = {band: bank.evaluate(geometry.points) for band, bank in banks.items()}
                for condition in config["mark_conditions"]:
                    labels = probe_labels(geometry.labels, condition, seed, config)
                    for estimator in config["estimators"]:
                        weights, coverage = interpolation_weights(geometry.points, labels, queries, geometry.L,
                            estimator, config["kernel_length_scale"], config["kernel_cutoff_in_length_scales"])
                        for band in config["field_bands"]:
                            # f_c(x_i) for c=mark_i; no hidden access to other channels.
                            observations = all_values[band][:, labels, np.arange(geometry.N)]
                            for sigma in config["noise_sigma"]:
                                score = score_observations(observations+sigma*noise, weights, targets[band])
                                record = {"status": "COMPLETE", "family": family, "geometry_seed": seed,
                                          "condition": condition, "labels_hash": array_hash(labels),
                                          "coordinates_hash": geometry.hashes["points"], "band": band,
                                          "estimator": estimator, "noise_sigma": sigma, "noise_hash": array_hash(noise),
                                          "target_hash": rng_manifest["target_hashes"][band],
                                          "coverage": coverage, "score": score}
                                records.append(record)
                    peak_rss = max(peak_rss, process.memory_info().rss)
                write_json(output_dir/"partial_results.json", {"records": records, "geometries": geometries,
                    "missing_geometries": missing, "status": "RUNNING", "beliefs_updated": False})
    summaries = _summary(records, config)
    expected = len(config["families"])*len(config["geometry_seeds"])*len(config["mark_conditions"])*len(
        config["estimators"])*len(config["field_bands"])*len(config["noise_sigma"])
    primary_admitted = all(g["admitted"] for g in geometries if g["family"] != "avian_local_only")
    result = {"version": VERSION, "status": "COMPLETE" if not missing and len(records) == expected else
              ("RESOURCE_LIMIT" if timed_out else "INCOMPLETE_MATRIX"), "created": utc_now(),
              "local_identity_hash": identity["hash"], "config_hash": digest(config),
              "records": records, "expected_cells": expected, "completed_cells": len(records),
              "geometries": geometries, "missing_geometries": missing, "summary": summaries,
              "all_primary_geometries_admitted": primary_admitted,
              "positive_interpretation_eligible": not missing and len(records) == expected and primary_admitted,
              "field_manifest": rng_manifest, "seconds_before_plot": time.perf_counter()-start,
              "peak_RSS_bytes": peak_rss, "threads": config["threads"], "no_hpo": True,
              "architecture_evidence": False, "beliefs_updated": False, "neural_training": False,
              "replication_unit": "geometry; the 128 field worlds and 5 channels are within-geometry averages",
              "confounds": ["full_spectral/local_only also differ in optimized coordinates and local microstructure",
                            "noise paired by node ID, not by physical position across different geometries",
                            "fields span frozen bands; positive findings may not transfer to other spectra",
                            "native/shuffle changes acquired observations and does not isolate internal computation"]}
    _plot_results(summaries, output_dir)
    result["total_seconds_including_plot"] = time.perf_counter()-start
    result["budget_exceeded"] = result["total_seconds_including_plot"] > config["maximum_seconds"]
    write_json(output_dir/"results.json", result)
    if summaries:
        fields = list(summaries[0])
        with (output_dir/"summary.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for row in summaries:
                writer.writerow({key: json.dumps(value) if isinstance(value, list) else value for key, value in row.items()})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT/"artifacts/sampling_probe/v1")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps({"config": load_probe_config(), "local_identity": probe_local_identity(),
                          "will_train_neural_network": False}, indent=2))
        return 0
    result = run_sampling_probe(args.output_dir)
    print(json.dumps({key: result[key] for key in ("status", "completed_cells", "expected_cells",
          "total_seconds_including_plot", "peak_RSS_bytes", "beliefs_updated")}, indent=2))
    return 0 if result["status"] == "COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
