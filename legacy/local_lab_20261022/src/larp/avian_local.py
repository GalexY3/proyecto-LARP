"""First-packed local-only controls, without selecting for a positive MHU test.

Uses the frozen avian objective with its spectral term exactly removed. Kept
separate to preserve the exact source provenance of the previously run full
candidate. This is not a relaxation of MHU admission criteria.
"""
from __future__ import annotations
from pathlib import Path
import math
import time
import json
import numpy as np
from scipy.optimize import minimize

from .avian import (ROOT, VERSION, load_avian_config, avian_objective, avian_local_identity,
                    packing_diagnostics, check_avian_gradient, plot_avian_validation)
from .geometry import Geometry, array_hash, certify_geometry, common_window_centers
from .artifacts import digest, file_hash, write_json, utc_now


def local_control_identity() -> dict:
    identity = avian_local_identity()
    identity["files"]["src/larp/avian_local.py"] = file_hash(Path(__file__))
    identity["hash"] = digest({"files": identity["files"], "runtime": identity["runtime"]})
    return identity


class _Limit(RuntimeError):
    pass


def generate_local_control(seed: int = 1101, *, output_dir: str | Path = ROOT/"artifacts/avian_v1") -> Geometry:
    """First complete packed candidate, irrespective of finite MHU certificate.

    Label/coordinate initialization, radius growth, optimization and caps are
    identical to avian v1 full_spectral. MHU failure is measured, never used to
    replace a packed control by another seed or attempt. No neural training.
    """
    config, identity = load_avian_config(), local_control_identity()
    if seed not in config["geometry_seeds"]:
        raise ValueError("frozen control seeds are 1101,1102,1103")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"avian_local_only_N400_g{seed}"
    if (output_dir/f"{prefix}.npz").exists():
        previous = Geometry.load(output_dir/f"{prefix}.npz")
        if previous.metadata["local_identity_hash"] != identity["hash"]:
            raise FileExistsError("local control belongs to different source provenance")
        return previous
    opt = config["optimizer"]
    start = time.perf_counter()
    deadline = start+config["maximum_generation_seconds_per_seed"]
    attempts = []
    import psutil
    process = psutil.Process()
    peak_RSS = process.memory_info().rss
    for attempt in range(config["max_attempts"]):
        rng = np.random.default_rng(np.random.SeedSequence([config["master_seed"], seed, attempt]))
        labels = rng.permutation(np.repeat(np.arange(5), config["counts_A_to_E"]))
        points = rng.uniform(0, config["L"], (config["N"], 2))
        initial_hash = array_hash(points)
        first, second = np.zeros_like(points), np.zeros_like(points)
        steps, iterations, evaluations, trace = 0, 0, 0, []
        status, message = "COMPLETE", None
        before = time.perf_counter()
        try:
            for step in range(1, opt["Adam_steps"]+1):
                if time.perf_counter() >= deadline:
                    raise _Limit()
                growth = opt["growth_start"]+(1-opt["growth_start"])*min(step/opt["growth_end_step"], 1.0)
                energy, gradient, parts = avian_objective(points, labels, growth=growth,
                                                        treatment="local_only", config=config, details=True)
                first = opt["beta1"]*first+(1-opt["beta1"])*gradient
                second = opt["beta2"]*second+(1-opt["beta2"])*gradient**2
                rate = opt["lr_end"]+(opt["lr_start"]-opt["lr_end"])*(1+math.cos(math.pi*step/opt["Adam_steps"]))/2
                points = (points-rate*(first/(1-opt["beta1"]**step))/
                          (np.sqrt(second/(1-opt["beta2"]**step))+opt["epsilon"])) % config["L"]
                steps = step
                if step % 500 == 0:
                    peak_RSS = max(peak_RSS, process.memory_info().rss)
                    trace.append({"optimizer": "Adam", "step": step, "energy": energy, "lr": rate, **parts})
            accepted = points.copy()

            def objective(flat):
                nonlocal evaluations
                if time.perf_counter() >= deadline:
                    raise _Limit()
                evaluations += 1
                value, gradient = avian_objective(flat.reshape(-1, 2), labels, treatment="local_only", config=config)
                return value, gradient.ravel()

            def callback(flat):
                nonlocal accepted, iterations
                accepted = flat.reshape(-1, 2).copy() % config["L"]
                iterations += 1

            try:
                optimized = minimize(objective, points.ravel(), jac=True, method="L-BFGS-B",
                                     callback=callback, options={"maxiter": opt["LBFGSB_maxiter"],
                                     "maxfun": opt["LBFGSB_maxfun"], "maxcor": opt["LBFGSB_maxcor"],
                                     "gtol": opt["LBFGSB_gtol"], "ftol": opt["LBFGSB_ftol"]})
                accepted = optimized.x.reshape(-1, 2) % config["L"]
                message = str(optimized.message)
            finally:
                points = accepted
        except _Limit:
            status, message = "RESOURCE_LIMIT", "Final accepted iterate retained at fixed seed cap"
        except (ValueError, FloatingPointError) as exc:
            status, message = "NUMERICAL_FAILURE_UNVERIFIED", f"{type(exc).__name__}: {exc}"
        base = {"generator_version": VERSION, "control_selection_version": "first_packed_not_MHU_selected_v1",
                "kind": "avian_hybrid", "treatment": "local_only", "geometry_seed": seed,
                "attempt": attempt, "test_only": False, "architecture_preregistered": False,
                "config_hash": digest(config), "local_identity_hash": identity["hash"],
                "local_identity": identity, "differs_from_preregistered_v0_1": True,
                "empirical_retina_replication": False, "neural_training": False,
                "seed_keys": [config["master_seed"], seed, attempt]}
        candidate = Geometry(points, labels, config["L"], base)
        cert_start = time.perf_counter()
        cert = certify_geometry(candidate, scope="mhu", centers=common_window_centers(config["L"]), detailed=True)
        cert_seconds = time.perf_counter()-cert_start
        packing = packing_diagnostics(candidate, config)
        energy, _, parts = avian_objective(points, labels, treatment="local_only", config=config, details=True)
        control_admitted = status == "COMPLETE" and packing["packing_admitted"]
        mhu_admitted = control_admitted and cert["scientific_admissible"]
        record = {"attempt": attempt, "status": status, "message": message, "initial_points_hash": initial_hash,
                  "hashes": candidate.hashes, "adam_steps": steps, "lbfgsb_iterations": iterations,
                  "lbfgsb_evaluations": evaluations, "optimization_seconds": cert_start-before,
                  "certificate_seconds": cert_seconds, "final_energy": energy, **parts,
                  "packing": packing, "certificate": cert, "control_admitted": bool(control_admitted),
                  "mhu_admitted": bool(mhu_admitted), "trace": trace}
        attempts.append(record)
        candidate = Geometry(points, labels, config["L"], {**base, "status": "PACKED_LOCAL_CONTROL" if control_admitted else "CONTROL_FAILURE",
                    "admitted": bool(mhu_admitted), "mhu_admitted": bool(mhu_admitted),
                    "control_admitted": bool(control_admitted), "certificate": cert, "packing": packing,
                    "optimizer": {"name": "float64_Adam_then_SciPy_LBFGSB", "status": status,
                                  "adam_steps": steps, "lbfgsb_iterations": iterations},
                    "attempts": attempts, "runtime_seconds": time.perf_counter()-start,
                    "peak_RSS_bytes": peak_RSS, "config": config,
                    "MHU_certificate_was_selection_criterion": False,
                    "finite_certificate_is_not_asymptotic_proof": True})
        candidate.save(output_dir/f"{prefix}_attempt{attempt}.npz")
        write_json(output_dir/f"{prefix}_attempt{attempt}_record.json", record)
        if control_admitted or status != "COMPLETE" or time.perf_counter() >= deadline:
            break
    candidate.save(output_dir/f"{prefix}.npz")
    write_json(output_dir/f"{prefix}_manifest.json", {"created": utc_now(), **candidate.to_dict()})
    write_json(output_dir/f"{prefix}_certificate.json", cert)
    return candidate


def validate_local_suite(output_dir: str | Path = ROOT/"artifacts/avian_v1") -> dict:
    from .graphs import knn_graph, graph_metrics, hop_type_coverage
    from .data import register_ports
    output_dir = Path(output_dir)
    rows = []
    for seed in load_avian_config()["geometry_seeds"]:
        geometry = generate_local_control(seed, output_dir=output_dir)
        prefix = f"avian_local_only_N400_g{seed}"
        edges = knn_graph(geometry.points, geometry.L, 6)
        graph = graph_metrics(edges, geometry.N, geometry.points, geometry.L)
        graph["type_coverage"] = hop_type_coverage(edges, geometry.labels, geometry.N)
        ports = register_ports(geometry.points, geometry.L)
        gradient = check_avian_gradient(geometry.points, geometry.labels, seed=seed, treatment="local_only")
        write_json(output_dir/f"{prefix}_graph_metrics.json", graph)
        write_json(output_dir/f"{prefix}_ports.json", {**ports.report(), "indices": ports.indices.tolist(), "sites": ports.sites.tolist()})
        write_json(output_dir/f"{prefix}_gradient.json", gradient)
        rows.append({"seed": seed, "admitted": geometry.metadata["mhu_admitted"],
                     "control_admitted": geometry.metadata["control_admitted"],
                     "status": geometry.metadata["status"], "attempt": geometry.metadata["attempt"],
                     "hashes": geometry.hashes, "runtime_seconds": geometry.metadata["runtime_seconds"],
                     "peak_RSS_bytes": geometry.metadata["peak_RSS_bytes"],
                     "certificate_passed": geometry.metadata["certificate"]["passed"],
                     "packing_maximum_overlap": geometry.metadata["packing"]["maximum_relative_overlap"],
                     "gradient_passed": gradient["passed"], "SCC_count": graph["SCC_count"], "port_digest": ports.digest})
    summary = {"version": VERSION, "control_selection_version": "first_packed_not_MHU_selected_v1",
               "treatment": "local_only", "local_identity": local_control_identity(), "records": rows,
               "packed_control_count": sum(r["control_admitted"] for r in rows),
               "finite_MHU_admitted_count": sum(r["admitted"] for r in rows),
               "architecture_evidence": False, "beliefs_updated": False,
               "MHU_certificate_was_selection_criterion": False}
    write_json(output_dir/"summary_local_only.json", summary)
    plot_avian_validation(summary, output_dir)
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT/"artifacts/avian_v1")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps({"config": load_avian_config(), "identity": local_control_identity(),
                          "MHU_certificate_was_selection_criterion": False, "neural_training": False}, indent=2))
    else:
        print(json.dumps(validate_local_suite(args.output_dir), indent=2))
