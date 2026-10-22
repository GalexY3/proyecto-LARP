"""Frozen plans, current-code gates and sequential execution. No long autorun."""
from pathlib import Path
import json
import time
import numpy as np
from .config import ROOT, load_profile
from .artifacts import write_json, digest, code_identity, utc_now, array_hash
from .geometry import Geometry, certify_geometry
from .graphs import graph_metrics, directed_distances
from .baselines import make_substrate, choose_baseline
from .data import register_ports
from .training import train_run, load_trained_run, datasets_for, evaluate, graph_tensors, data_hashes, model_hash

GATES = ROOT / "artifacts" / "gates"


def gate_path(name):
    return GATES / (name + ".json")


def record_gate(name, passed, **payload):
    value = {"gate": name, "passed": bool(passed), "created_UTC": utc_now(),
             "code": code_identity(ROOT), **payload}
    write_json(gate_path(name), value)
    return value


def require_gates(*names):
    identity = code_identity(ROOT)["source_hash"]
    for name in names:
        path = gate_path(name)
        if not path.exists():
            raise RuntimeError(f"GATE_NOT_RUN {name}")
        value = json.loads(path.read_text(encoding="utf-8"))
        if not value["passed"]:
            raise RuntimeError(f"GATE_FAILED {name}; no automatic scientific revision")
        if value["code"]["source_hash"] != identity:
            raise RuntimeError(f"STALE_GATE {name}: rerun after code change")


def validate_geometry(N=400, seed=1101):
    begin = time.perf_counter()
    geometry, edges = make_substrate("native", N, seed, cache=ROOT / "artifacts" / "geometry")
    output = ROOT / "artifacts" / "geometry" / f"mhu_N{N}_g{seed}"
    certificate = certify_geometry(geometry, scope="mhu")
    write_json(str(output)+"_certificate.json", certificate)
    metrics = graph_metrics(edges, N, geometry.points, geometry.L)
    write_json(str(output)+"_graph_metrics.json", metrics)
    return record_gate("geometry", certificate["scientific_admissible"], N=N, seed=seed,
                       geometry_hashes=geometry.hashes, certificate=str(output)+"_certificate.json",
                       graph_metrics=str(output)+"_graph_metrics.json", seconds=time.perf_counter()-begin)


def freeze_plan(path, plan):
    """Results are never written into the immutable plan itself."""
    path = Path(path)
    value = {"plan": plan, "plan_hash": digest(plan), "code": code_identity(ROOT),
             "created_UTC": utc_now(), "results": None}
    if path.exists():
        old = json.loads(path.read_text(encoding="utf-8"))
        if digest(old["plan"]) != old["plan_hash"] or old["plan_hash"] != value["plan_hash"] or old["code"]["source_hash"] != value["code"]["source_hash"]:
            raise RuntimeError("Frozen plan differs: create a new series, never rewrite a preregistration")
        return old
    write_json(path, value)
    return value


def run_config(profile, task, condition, geometry_seed, training_seed, *, updates=None, variant=None, lr=None, regime="causal"):
    N = 100 if condition == "nca" else profile["N"]
    return {"stage": profile["stage"], "task": task, "condition": condition,
            "N": N, "L": 20.0 if condition == "nca" else float(np.sqrt(N)), "world_side": 10,
            "variant": variant or profile["variant"], "geometry_seed": geometry_seed,
            "training_seed": training_seed, "updates": updates or profile["updates"],
            "batch_size": profile["batch_size"], "steps": profile["steps"],
            "train_size": profile["train_size"], "validation_size": profile["validation_size"],
            "test_size": profile["test_size"], "lr": lr if lr is not None else profile.get("lr", .003),
            "regime": regime}


def run_id(cfg):
    return f"{cfg['task']}_{cfg['condition']}_{cfg['variant']}_g{cfg['geometry_seed']}_s{cfg['training_seed']}_u{cfg['updates']}_lr{cfg['lr']:g}_{cfg['regime']}"


def pairing_preflight(configs):
    """Verify every focal pair before training or opening any endpoint."""
    from .model import LARPModel
    from .config import optimizer_settings
    checked = []
    keys = lambda c: (c["task"], c["variant"], c["geometry_seed"], c["training_seed"], c["lr"], c["updates"], c["regime"])
    identities = [(keys(c),c["condition"]) for c in configs]
    if len(identities) != len(set(identities)):
        raise ValueError("Duplicate run in preregistered panel")
    native = {keys(c): c for c in configs if c["condition"] == "native"}
    shuffled = {keys(c): c for c in configs if c["condition"] == "shuffle"}
    for key in shuffled:
        if key not in native:
            raise ValueError("Shuffle without a preregistered native pair")
        hashes, label_hashes = [], []
        for cfg in (native[key], shuffled[key]):
            g, e = make_substrate(cfg["condition"], cfg["N"], cfg["geometry_seed"], regime=cfg["regime"], cache=ROOT / "artifacts" / "geometry")
            from .data import resource_ports
            ports = resource_ports(g.points,g.L) if cfg["task"]=="resource" else register_ports(g.points, g.L, cfg.get("world_side",10))
            model = LARPModel(cfg["variant"], 8 if cfg["task"]=="copy" else 1, 29 if cfg["task"]=="resource" else 25, cfg["training_seed"])
            hashes.append({"coordinates": array_hash(g.points), "edges": array_hash(e), "ports": ports.digest,
                           **data_hashes(cfg), "optimizer": digest(optimizer_settings(cfg["lr"])),
                           "budget": digest({"updates":cfg["updates"],"steps":cfg["steps"],"batch_size":cfg["batch_size"]}),
                           "shared_initialization": model_hash(model)})
            label_hashes.append(array_hash(g.labels))
        if hashes[0] != hashes[1] or label_hashes[0] == label_hashes[1]:
            raise RuntimeError("SCIENTIFIC_BLOCKER causal pairing failed before training")
        checked.append({"pair": list(key), "hashes": hashes[0], "labels": label_hashes})
    return checked


def execute_configs(configs, directory, *, open_test=False, resume=False, maximum_hours=8):
    directory = Path(directory)
    freeze_plan(directory / "preregistration.json", {"configs": configs, "open_test": open_test,
                "endpoints": "copy bit accuracy; fill macro BA; xor accessible validation accuracy",
                "priors_updated": False, "maximum_hours": maximum_hours})
    write_json(directory / "pairing_preflight.json", pairing_preflight(configs))
    started = time.perf_counter()
    records = []
    for cfg in configs:
        if time.perf_counter()-started > maximum_hours*3600:
            write_json(directory / "status.json", {"status": "RESOURCE_LIMIT_SUITE", "records": records})
            return records
        geometry, edges = make_substrate(cfg["condition"], cfg["N"], cfg["geometry_seed"],
                                         regime=cfg["regime"], cache=ROOT / "artifacts" / "geometry")
        run_dir = directory / run_id(cfg)
        if (run_dir / "geometry.npz").exists():
            if Geometry.load(run_dir / "geometry.npz").hashes != geometry.hashes or not np.array_equal(np.load(run_dir / "edges.npy"), edges):
                raise RuntimeError("Existing run substrate differs; evidence cannot be overwritten")
        else:
            geometry.save(run_dir / "geometry.npz")
            np.save(run_dir / "edges.npy", edges)
        record = train_run(cfg, geometry, edges, run_dir, resume=resume and (run_dir / "manifest.json").exists(),
                           open_test=open_test, preregistered=True)
        records.append(record)
        write_json(directory / "results.json", records)
        if record["status"] != "COMPLETE":
            write_json(directory / "status.json", {"status": "STOPPED", "reason": record["status"], "run": run_id(cfg)})
            return records
    write_json(directory / "status.json", {"status": "COMPLETE", "count": len(records)})
    return records


def calibration(directory=None, *, resume=False):
    require_gates("scientific_tests", "geometry")
    directory = Path(directory or ROOT / "runs" / "calibration")
    profile = load_profile("pilot_focal")
    cfg = run_config(profile, "copy", "native", 9001, 9002, updates=205)
    cfg["stage"] = "calibration"
    records = execute_configs([cfg], directory, resume=resume)
    record = records[0]
    import torch
    saved = torch.load(directory / run_id(cfg) / "checkpoints" / "last.pt", weights_only=False)
    seconds = np.asarray(saved["tracking"]["times"])[5:205]
    measured = {"status": record["status"], "warmup_updates": 5, "measured_updates": len(seconds),
                "median_step_seconds": float(np.median(seconds)), "p90_step_seconds": float(np.percentile(seconds, 90)),
                "train_seconds_actual": record["training_seconds_including_periodic_validation"],
                "validation_seconds_actual": record["validation"]["evaluation_seconds"],
                "RSS_peak_bytes_sampled": record["RSS_peak_bytes_sampled"],
                "measure_scope": "data binding excluded from individual step timer; included in whole training wall time",
                "architecture_evidence": False}
    # Estimates carry a label; final full-val/test time uses measured inference.
    measured["estimated_seconds_per_1000update_run"] = measured["p90_step_seconds"]*1000 + record["validation"]["evaluation_seconds"]*15
    # Use the slower of per-step and total wall estimates: data binding and
    # measured intermediate validation must not disappear from budget planning.
    measured["whole_wall_seconds_per_update_with_validation"] = record["training_seconds_including_periodic_validation"]/205
    measured["estimated_seconds_per_1000update_run"] = max(measured["estimated_seconds_per_1000update_run"],
        measured["whole_wall_seconds_per_update_with_validation"]*1000 + record["validation"]["evaluation_seconds"]*4)
    measured["estimated_seconds_12run_pilot"] = measured["estimated_seconds_per_1000update_run"]*12
    measured["recommended_pilot_updates"] = 500 if measured["estimated_seconds_12run_pilot"] > 8*3600 or measured["estimated_seconds_per_1000update_run"] > 1800 else 1000
    measured["reduced_pilot_estimated_seconds"] = (measured["p90_step_seconds"]*500 + record["validation"]["evaluation_seconds"]*10)*12
    write_json(directory / "calibration.json", measured)
    return record_gate("calibration", record["status"] == "COMPLETE" and len(seconds) == 200, **measured)


def accessibility(dataset, geometry, edges, ports, steps):
    distances = directed_distances(edges, geometry.N)
    source = ports.indices[dataset.arrays["source_sites"]]
    destination = ports.indices[dataset.arrays["destination"]]
    hops = distances[source, destination[:, None]]
    required = hops if dataset.task == "xor" else hops[np.arange(len(dataset)), dataset.arrays["query"]][:, None]
    accessible = np.all(required <= steps, axis=1)
    return accessible, {"fraction": float(accessible.mean()), "inaccessible_examples": int((~accessible).sum()),
                        "required_hops_median_finite": float(np.median(required[np.isfinite(required)]))}


def smoke(directory=None, *, resume=False):
    require_gates("scientific_tests", "geometry", "calibration")
    directory = Path(directory or ROOT / "runs" / "smoke")
    profile = load_profile("smoke")
    configs = [run_config(profile, "xor", c, 1101, s) for c in profile["geometries"] for s in profile["training_seeds"]]
    records = execute_configs(configs, directory, resume=resume)
    diagnostics = []
    for cfg, record in zip(configs, records):
        run_dir = directory / run_id(cfg)
        geometry = Geometry.load(run_dir / "geometry.npz")
        edges = np.load(run_dir / "edges.npy")
        model, _, _ = load_trained_run(run_dir)
        ports = register_ports(geometry.points, geometry.L)
        tensors = graph_tensors(geometry, edges, "cpu")
        split_results = {}
        for split, dataset in datasets_for(cfg).items():
            mask, description = accessibility(dataset, geometry, edges, ports, cfg["steps"])
            score = evaluate(model, dataset, geometry, ports, tensors, indexes=np.flatnonzero(mask)) if mask.any() else None
            split_results[split] = {"accessibility": description, "accessible_score": score}
        diagnostics.append({"run": run_id(cfg), "status": record["status"], "all_validation": record["validation"], **split_results})
    passed = len(records) == len(configs) and all(r["status"] == "COMPLETE" and
        r["validation"]["accessible_score"] is not None and
        not r["validation"]["accessible_score"].get("divergent", False) and
        r["validation"]["accessible_score"]["score"] >= profile["gate_accessible_accuracy"] for r in diagnostics)
    write_json(directory / "diagnostics.json", diagnostics)
    return record_gate("smoke", passed, diagnostics=diagnostics, test_opened=False,
                       next_action="pilot permitted" if passed else "STOP copy/fill; diagnose block/interface, version any scientific revision")


def plan_stage(stage, task="copy", *, ecological=False):
    if stage in {"pilot", "fill"}:
        profile = load_profile("pilot_focal")
        budget = json.loads(gate_path("calibration").read_text(encoding="utf-8"))["recommended_pilot_updates"] if gate_path("calibration").exists() else 1000
        configs = [run_config(profile, "fill" if stage == "fill" else task, c, g, s, updates=budget)
                   for g in profile["geometry_seeds"] for s in profile["training_seeds"] for c in profile["conditions"]]
    elif stage == "screen":
        profile = load_profile("baseline_screen")
        conditions = [(c, "T") for c in profile["geometries"]]+[("native", "G"), ("hu", "G")]
        if ecological:
            if task != "fill":
                raise ValueError("Ecological screen preregistered only for fill")
            conditions = [("grid_balanced", "T"), ("hu", "T"), ("native", "T"), ("small_world", "T"), ("nca", "G")]
        configs = [run_config(profile, task, c, 1101, s, variant=v, regime="ecological" if ecological else "causal")
                   for c, v in conditions for s in profile["training_seeds"]]
    else:
        raise ValueError(stage)
    return {"stage": stage, "task": task, "configs": configs, "count": len(configs),
            "open_test": stage in {"pilot", "fill"}, "architecture_posterior": False,
            "requires": ["scientific_tests", "geometry", "calibration", "smoke"],
            "automatic": False}


def execute_stage(stage, task="copy", directory=None, *, resume=False, ecological=False):
    require_gates("scientific_tests", "geometry", "calibration", "smoke")
    if stage in {"fill", "screen"}:
        require_gates("pilot_copy")
    if stage == "screen" and task == "fill":
        require_gates("fill_fill")
    plan = plan_stage(stage, task, ecological=ecological)
    directory = Path(directory or ROOT / "runs" / (stage+"_"+task+("_ecological" if ecological else "")))
    records = execute_configs(plan["configs"], directory, open_test=plan["open_test"], resume=resume)
    if len(records) == plan["count"] and all(r["status"] == "COMPLETE" for r in records):
        record_gate(stage+"_"+task, True, results=str(directory / "results.json"), count=len(records))
        if stage == "screen" and not ecological:
            write_json(directory / "baseline_selection.json", choose_baseline(records))
    return records


def confirmation_plan(task, baseline, lr=.003, *, extension=False, hpo=False):
    p = load_profile("confirmation")
    seeds = p["extension_seeds"] if extension else p["geometry_seeds"]
    training = p["hpo_training_seeds"] if hpo else p["training_seeds"]
    conditions = ["native", "shuffle", baseline]
    configs = [run_config(p, task, c, g, s, updates=p["hpo_updates"] if hpo else p["updates"], lr=rate)
               for g in ([p["hpo_geometry_seed"]] if hpo else seeds) for s in training
               for c in conditions for rate in (p["lr_candidates"] if hpo else [lr])]
    if hpo:
        for cfg in configs:
            cfg["stage"] = "calibration"  # always validation, no architecture evidence
    return {"task": task, "configs": configs, "count": len(configs), "open_test": not hpo,
            "expected_geometry_seeds": seeds, "expected_training_seeds": p["training_seeds"],
            "conditions": conditions, "lr": lr, "extension": extension, "HPO": hpo,
            "automatic": False, "conditional_branches_blocked": ["C3 matched", "partial port relocation", "D4 if needed"]}


def freeze_confirmation(task, *, directory=None, resume=False):
    require_gates("scientific_tests", "geometry", "calibration", "smoke", "pilot_copy", "screen_"+task)
    if task == "fill":
        require_gates("fill_fill")
    screen_gate = json.loads(gate_path("screen_"+task).read_text(encoding="utf-8"))
    screen = Path(screen_gate["results"]).parent
    selection = json.loads((screen / "baseline_selection.json").read_text(encoding="utf-8"))
    directory = Path(directory or ROOT / "runs" / ("confirmation_"+task))
    hpo = confirmation_plan(task, selection["condition"], hpo=True)
    records = execute_configs(hpo["configs"], directory / "hpo", open_test=False, resume=resume, maximum_hours=48)
    if len(records) != hpo["count"] or any(r["status"] != "COMPLETE" for r in records):
        raise RuntimeError("HPO incomplete; no frozen confirmation")
    values = {}
    for lr in load_profile("confirmation")["lr_candidates"]:
        group = [r for r in records if r["code"] and abs(json.loads((directory / "hpo" / r["experiment_id"] / "manifest.json").read_text(encoding="utf-8"))["config"]["lr"]-lr)<1e-12]
        mhu = np.mean([r["score"] for r in group if r["condition"] in {"native", "shuffle"}])
        rival = np.mean([r["score"] for r in group if r["condition"] == selection["condition"]])
        values[str(lr)] = float((mhu+rival)/2)
    best = min(load_profile("confirmation")["lr_candidates"], key=lambda lr: (-values[str(lr)], lr))
    plan = confirmation_plan(task, selection["condition"], best)
    plan["HPO_validation_scores"] = values
    return freeze_plan(directory / "frozen_confirmation.json", plan)


def confirm(task, *, directory=None, resume=False, extension=False):
    require_gates("scientific_tests", "geometry", "calibration", "smoke", "pilot_copy", "screen_"+task)
    if task == "fill":
        require_gates("fill_fill")
    directory = Path(directory or ROOT / "runs" / ("confirmation_"+task))
    frozen = json.loads((directory / "frozen_confirmation.json").read_text(encoding="utf-8"))
    if frozen["code"]["source_hash"] != code_identity(ROOT)["source_hash"]:
        raise RuntimeError("Frozen scientific plan belongs to different code")
    plan = frozen["plan"]
    if plan["task"] != task or digest(plan) != frozen["plan_hash"]:
        raise RuntimeError("Frozen confirmation task/payload differs")
    if extension:
        analysis = json.loads((directory / "analysis.json").read_text(encoding="utf-8"))
        if analysis.get("effect_classification") != "inconclusive":
            raise RuntimeError("Single extension only if initial eight geometries inconclusive")
        plan = confirmation_plan(task, plan["conditions"][2], plan["lr"], extension=True)
        freeze_plan(directory / "extension" / "frozen_confirmation.json",plan)
    records = execute_configs(plan["configs"], directory / ("extension" if extension else "main"), open_test=True,
                              resume=resume, maximum_hours=48)
    for record in records:
        record["expected_geometry_seeds"] = plan["expected_geometry_seeds"]
        record["expected_training_seeds"] = plan["expected_training_seeds"]
    write_json(directory / ("extension_results.json" if extension else "results.json"), records)
    if extension:
        originals = json.loads((directory / "results.json").read_text(encoding="utf-8"))
        all_seeds = load_profile("confirmation")["geometry_seeds"] + load_profile("confirmation")["extension_seeds"]
        combined = [{**r,"expected_geometry_seeds":all_seeds} for r in originals+records]
        write_json(directory / "combined16_results.json",combined)
    return records
