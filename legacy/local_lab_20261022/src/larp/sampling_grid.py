"""Budget-gated Grid baseline and query-phase supplement; previous v1 intact."""
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
from . import geometry as geom
from .artifacts import array_hash, digest, file_hash, utc_now, write_json
from .sampling_probe import (probe_labels, common_sensor_noise, interpolation_weights, score_observations)
from .sampling_oracle import (load_oracle_config, load_frozen_inputs, fourier_design, oracle_operator)

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT/"configs/sampling_grid_v1.json"
VERSION = "sampling_grid_supplement_v1"
_CONFIG_HASH = "8aabee3c054b9b3325e8a7390388888df98ea1546f0a2918bce7ca7a810419cb"


def load_config() -> dict:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if digest(config) != _CONFIG_HASH:
        raise ValueError("Frozen Grid supplement changed; create another version")
    return config


def local_identity() -> dict:
    paths = [Path(__file__), CONFIG_PATH, ROOT/"src/larp/geometry.py", ROOT/"src/larp/artifacts.py",
             ROOT/"src/larp/sampling_probe.py", ROOT/"src/larp/sampling_oracle.py",
             ROOT/"configs/sampling_probe_v1.json", ROOT/"configs/sampling_oracle_v1.json"]
    files = {str(p.relative_to(ROOT)).replace("\\", "/"): file_hash(p) for p in paths}
    runtime = {p: importlib.metadata.version(p) for p in ("numpy", "scipy", "psutil")}
    runtime["python"] = platform.python_version()
    runtime["threads"] = {k: os.environ[k] for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}
    return {"files": files, "runtime": runtime, "hash": digest({"files": files, "runtime": runtime})}


def continuous_queries(config: dict) -> np.ndarray:
    return np.random.default_rng(np.random.SeedSequence(config["continuous_queries"]["seed_keys"])).uniform(
        0, config["construction"]["L"], (config["continuous_queries"]["count"], 2))


def time_relabel(grid: geom.Geometry, seed: int, *, proposals: int, restarts: int,
                 test_only: bool) -> tuple[geom.Geometry, dict]:
    """Time certificates separately without modifying the frozen implementation."""
    original = geom.certify_geometry
    timings = []

    def timed_certificate(*args, **kwargs):
        before = time.perf_counter()
        value = original(*args, **kwargs)
        timings.append(time.perf_counter()-before)
        return value

    geom.certify_geometry = timed_certificate
    start = time.perf_counter()
    try:
        result = geom.relabel_geometry(grid, "grid_balanced", seed, proposals=proposals,
                                       restarts=restarts, test_only=test_only)
    finally:
        elapsed = time.perf_counter()-start
        geom.certify_geometry = original
    actual_proposals = sum(int(a["proposals"]) for a in result.metadata["annealing"]["attempts"])
    return result, {"total_seconds": elapsed, "noncertificate_seconds": elapsed-sum(timings),
                    "certificate_seconds": timings, "actual_proposals": actual_proposals,
                    "seconds_per_proposal_conservative_includes_wrapper": (elapsed-sum(timings))/actual_proposals,
                    "test_only": test_only}


def conservative_construction_estimate(calibrations: list[dict], grid_create_seconds: float,
                                      config: dict) -> dict:
    rules = config["construction"]
    sec_per_proposal = max(r["seconds_per_proposal_conservative_includes_wrapper"] for r in calibrations)
    cert_seconds = max(t for r in calibrations for t in r["certificate_seconds"])
    factor = rules["conservative_runtime_multiplier"]
    estimate = factor*(rules["maximum_total_proposals"]*sec_per_proposal+
                       rules["maximum_total_certificates"]*cert_seconds+3*grid_create_seconds)
    return {"seconds_per_proposal_max_measured": sec_per_proposal,
            "certificate_seconds_max_measured": cert_seconds, "grid_create_seconds_measured": grid_create_seconds,
            "runtime_multiplier": factor, "worst_case_proposals": rules["maximum_total_proposals"],
            "worst_case_certificates": rules["maximum_total_certificates"],
            "estimated_conservative_construction_seconds": estimate,
            "budget_seconds": rules["maximum_seconds"], "eligible": estimate <= rules["maximum_seconds"],
            "can_interrupt_mid_attempt": False}


def calibrate(config: dict, output_dir: Path) -> dict:
    calibration = config["calibration"]
    before = time.perf_counter()
    grid = geom.generate_geometry(400, calibration["seed"], "grid", detailed_certificate=False)
    grid_seconds = time.perf_counter()-before
    measurements = []
    for proposals in (calibration["first_proposals"], calibration["extended_proposals"]):
        if measurements and measurements[0]["seconds_per_proposal_conservative_includes_wrapper"]*proposals >= calibration["extended_optimization_ceiling_seconds"]:
            break
        candidate, timing = time_relabel(grid, calibration["seed"], proposals=proposals, restarts=1, test_only=True)
        candidate.save(output_dir/f"calibration/Grid9005_proposals{proposals}_TEST_ONLY.npz")
        timing["proposals"] = proposals
        timing["hashes"] = candidate.hashes
        timing["annealing"] = candidate.to_dict()["metadata"]["annealing"]
        timing["no_field_MSE"] = True
        measurements.append(timing)
    result = {"measurements": measurements, "grid_create_seconds": grid_seconds,
              "decision": conservative_construction_estimate(measurements, grid_seconds, config),
              "no_field_MSE": True, "architecture_evidence": False}
    write_json(output_dir/"calibration.json", result)
    return result


def construct_grids(config: dict, output_dir: Path, calibration: dict) -> tuple[list, dict]:
    if not calibration["decision"]["eligible"]:
        return [], {"status": "NOT_RUN", "reason": "conservative_estimate_exceeds_180_seconds",
                    "decision": calibration["decision"], "no_field_MSE": True}
    started = time.perf_counter()
    rows, candidates = [], []
    rules = config["construction"]
    for seed in config["geometry_seeds"]:
        if time.perf_counter()-started >= rules["maximum_seconds"]:
            break
        grid = geom.generate_geometry(rules["N"], seed, "grid", detailed_certificate=False)
        candidate, timing = time_relabel(grid, seed, proposals=rules["proposals"],
                                        restarts=rules["restarts"], test_only=False)
        candidate.save(output_dir/f"geometries/grid_balanced_N400_g{seed}.npz")
        row = {"family": "grid_balanced", "geometry_seed": seed, "hashes": candidate.hashes,
               "path": str(output_dir/f"geometries/grid_balanced_N400_g{seed}.npz"),
               "annealing": candidate.to_dict()["metadata"]["annealing"], "timing": timing,
               "coordinate_replication": "same_grid_coordinates_different_mark_assignments"}
        rows.append(row)
        candidates.append(("grid_balanced", seed, candidate))
        write_json(output_dir/"construction_partial.json", {"records": rows, "seconds": time.perf_counter()-started})
    complete = len(candidates) == len(config["geometry_seeds"])
    return candidates, {"status": "COMPLETE" if complete else "RESOURCE_LIMIT", "records": rows, "seconds": time.perf_counter()-started,
                        "budget_exceeded": time.perf_counter()-started > rules["maximum_seconds"],
                        "original_budget_unchanged": True, "no_field_MSE": True,
                        "spatial_coordinate_realizations": 1, "mark_realizations": 3}


def score_oracle(bank, points, labels, queries, noise, sigma) -> tuple[dict, list]:
    values = bank.evaluate(points)
    target = bank.evaluate(queries)
    Q = fourier_design(queries, bank.modes, bank.L)
    predictions, reports = [], []
    for c in range(5):
        sensor = np.flatnonzero(labels == c)
        operator, diagnostics = oracle_operator(fourier_design(points[sensor], bank.modes, bank.L), Q,
                                                 sigma=sigma, mode_pairs=len(bank.modes), rcond=1e-10)
        predictions.append((values[:, c, sensor]+sigma*noise[:, sensor]) @ operator.T)
        reports.append({"channel": c, **diagnostics})
    prediction = np.stack(predictions, axis=1)
    mse = np.mean((prediction-target)**2, axis=-1)
    return {"MSE_macro": float(mse.mean()), "MSE_per_channel": mse.mean(axis=0).tolist(),
            "world_macro_MSE": mse.mean(axis=1).tolist(), "prediction_hash": array_hash(prediction)}, reports


def original_cell(source: dict, oracle_source: dict, family, seed, mark, band, sigma, estimator) -> dict:
    cells = oracle_source["records"] if estimator == "oracle_band" else source["records"]
    matching = [r for r in cells if (r["family"],r["geometry_seed"],r["condition"],r["band"],r["noise_sigma"]) ==
                (family,seed,mark,band,sigma) and (estimator == "oracle_band" or r["estimator"] == estimator)]
    if len(matching) != 1:
        raise ValueError("Original aligned cell missing or duplicated")
    return matching[0]


def summarize(records: list[dict]) -> list[dict]:
    groups = sorted(set((r["family"],r["query_stratum"],r["estimator"],r["band"],r["noise_sigma"]) for r in records))
    rows = []
    for key in groups:
        selected = [r for r in records if (r["family"],r["query_stratum"],r["estimator"],r["band"],r["noise_sigma"]) == key]
        a = {r["geometry_seed"]: r["score"]["MSE_macro"] for r in selected if r["condition"] == "native"}
        b = {r["geometry_seed"]: r["score"]["MSE_macro"] for r in selected if r["condition"] == "shuffle"}
        seeds = sorted(set(a)&set(b))
        x,y = np.array([a[s] for s in seeds]), np.array([b[s] for s in seeds])
        rows.append({"family":key[0],"query_stratum":key[1],"estimator":key[2],"band":key[3],"noise_sigma":key[4],
                     "realizations":len(seeds),"native_MSE_mean":float(x.mean()),"shuffle_MSE_mean":float(y.mean()),
                     "native_MSE_SD":float(x.std(ddof=1)),"shuffle_MSE_SD":float(y.std(ddof=1)),
                     "native_minus_shuffle_by_realization":(x-y).tolist(),
                     "grid_replicates_are_labels_on_same_coordinates":key[0]=="grid_balanced"})
    return rows


def evaluate(config: dict, grids: list, output_dir: Path) -> dict:
    source, source_config, banks, aligned = load_frozen_inputs(load_oracle_config())
    oracle_path = ROOT/config["source_oracle_series"]/"results.json"
    if file_hash(oracle_path) != config["source_oracle_results_sha256"]:
        raise ValueError("Original oracle series changed")
    oracle_source = json.loads(oracle_path.read_text(encoding="utf-8"))
    all_geometries = []
    for row in source["geometries"]:
        path = Path(row["path"])
        if file_hash(path) != row["file_hash"]:
            raise ValueError("Original geometry bytes changed")
        all_geometries.append((row["family"],row["geometry_seed"],geom.Geometry.load(path)))
    all_geometries += grids
    queries = {"aligned":aligned, "continuous":continuous_queries(config)}
    write_json(output_dir/"queries.json", {k:{"hash":array_hash(v),"points":v.tolist()} for k,v in queries.items()})
    records, reused, omissions = [], 0, []
    started = time.perf_counter()
    import psutil
    process = psutil.Process()
    peak_RSS = process.memory_info().rss
    for family,seed,geometry in all_geometries:
        if time.perf_counter()-started >= config["evaluation"]["maximum_seconds"]:
            omissions.append({"family":family,"seed":seed,"reason":"RESOURCE_LIMIT_NOT_RUN"})
            continue
        noise = common_sensor_noise(seed, source_config)
        values = {b:bank.evaluate(geometry.points) for b,bank in banks.items()}
        for mark in config["marks"]:
            labels = probe_labels(geometry.labels,mark,seed,source_config)
            for stratum,sites in queries.items():
                for estimator in config["estimators"]:
                    coverage = None
                    if estimator != "oracle_band":
                        weights,coverage = interpolation_weights(geometry.points,labels,sites,geometry.L,estimator,
                            config["evaluation"]["kernel_length_scale"],config["evaluation"]["kernel_cutoff_scales"])
                    for band,bank in banks.items():
                        target = bank.evaluate(sites)
                        for sigma in config["noise_sigma"]:
                            diagnostics = None
                            if estimator == "oracle_band":
                                score,diagnostics = score_oracle(bank,geometry.points,labels,sites,noise,sigma)
                            else:
                                observations = values[band][:,labels,np.arange(geometry.N)]+sigma*noise
                                score = score_observations(observations,weights,target)
                            reuses = family != "grid_balanced" and stratum == "aligned"
                            if reuses:
                                old = original_cell(source,oracle_source,family,seed,mark,band,sigma,estimator)
                                old_score = old if estimator == "oracle_band" else old["score"]
                                if score["prediction_hash"] != old_score["prediction_hash"] or score["MSE_macro"] != old_score["MSE_macro"]:
                                    raise ValueError("Aligned replay does not reproduce original predictions/scores")
                                reused += 1
                            records.append({"family":family,"geometry_seed":seed,"condition":mark,"query_stratum":stratum,
                                "estimator":estimator,"band":band,"noise_sigma":sigma,"score":score,
                                "coordinates_hash":geometry.hashes["points"],"labels_hash":array_hash(labels),
                                "query_hash":array_hash(sites),"target_hash":array_hash(target),"noise_hash":array_hash(noise),
                                "coverage":coverage,"oracle_diagnostics":diagnostics,"reused_previous_aligned_cell":reuses,
                                "new_independent_replication":False})
        peak_RSS=max(peak_RSS,process.memory_info().rss)
        write_json(output_dir/"evaluation_partial.json", {"records":records,"reused":reused,"omissions":omissions})
    elapsed=time.perf_counter()-started
    result={"status":"COMPLETE" if len(records)==config["evaluation"]["expected_cells"] and not omissions else "INCOMPLETE_MATRIX",
            "records":records,"summary":summarize(records),"omissions":omissions,"completed_cells":len(records),
            "expected_cells":config["evaluation"]["expected_cells"],"reused_aligned_cells":reused,
            "new_cells":len(records)-reused,"seconds":elapsed,"budget_exceeded":elapsed>config["evaluation"]["maximum_seconds"],
            "peak_RSS_bytes":peak_RSS,"posthoc_supplement":True,"architecture_evidence":False,"beliefs_updated":False,
            "replication_grid":"three_labels_one_coordinate_grid","no_hpo":True}
    write_json(output_dir/"evaluation.json",result)
    if result["summary"]:
        with (output_dir/"summary.csv").open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(result["summary"][0]));writer.writeheader()
            writer.writerows({k:json.dumps(v) if isinstance(v,list) else v for k,v in r.items()} for r in result["summary"])
    return result


def run(output_dir: str|Path = ROOT/"artifacts/sampling_grid/v1") -> dict:
    config,identity=load_config(),local_identity()
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    freeze={"version":VERSION,"config":config,"config_hash":digest(config),"local_identity":identity,
            "created":utc_now(),"before_calibration_construction_scores":True,"neural_training":False,
            "architecture_evidence":False,"beliefs_updated":False}
    freeze_path=output_dir/"preregistration.json"
    if freeze_path.exists():
        old=json.loads(freeze_path.read_text(encoding="utf-8"))
        if old["config_hash"]!=freeze["config_hash"] or old["local_identity"]["hash"]!=identity["hash"]:
            raise FileExistsError("Different frozen Grid supplement provenance; use another series")
        if (output_dir/"results.json").exists():
            return json.loads((output_dir/"results.json").read_text(encoding="utf-8"))
    else:
        write_json(freeze_path,freeze)
    started=time.perf_counter()
    calibration=calibrate(config,output_dir)
    grids,construction=construct_grids(config,output_dir,calibration)
    write_json(output_dir/"construction.json",construction)
    if not grids or construction["status"] != "COMPLETE" or construction.get("budget_exceeded", False):
        result={"version":VERSION,"status":"GRID_NOT_RUN","calibration":calibration,
                "construction":construction,"evaluation":{"status":"NOT_RUN","reason":"construction_budget_gate"},
                "no_field_MSE":True,"architecture_evidence":False,"beliefs_updated":False}
    else:
        evaluation=evaluate(config,grids,output_dir)
        result={"version":VERSION,"status":evaluation["status"],"calibration":calibration,
                "construction":construction,"evaluation_path":str(output_dir/"evaluation.json"),
                "completed_cells":evaluation["completed_cells"],"reused_aligned_cells":evaluation["reused_aligned_cells"],
                "new_cells":evaluation["new_cells"],"architecture_evidence":False,"beliefs_updated":False}
    result["total_seconds"]=time.perf_counter()-started
    result["local_identity_hash"]=identity["hash"]
    write_json(output_dir/"results.json",result)
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=ROOT/"artifacts/sampling_grid/v1")
    parser.add_argument("--dry-run",action="store_true")
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps({"config":load_config(),"identity":local_identity(),"will_train_neural_network":False},indent=2))
    else:
        r=run(args.output_dir)
        print(json.dumps({k:v for k,v in r.items() if k not in ("calibration","construction")},indent=2))
