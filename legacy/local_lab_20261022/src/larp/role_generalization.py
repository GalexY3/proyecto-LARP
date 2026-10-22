"""One preregistered input ablation, reusing the existing GRU control exactly."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import numpy as np
import psutil
import torch
from torch.nn import functional as F

from .artifacts import array_hash, digest, file_hash, utc_now, write_json
from .geometry import Geometry
from .gru_baseline import GGNNLikeModel
from .learning_diagnostics import bind_cases, graph_context, make_cases, predictions, state_hash
from .transmission_probe import accuracy_gate, measure, target_batch

ROOT = Path(__file__).resolve().parents[2]


def coordinates_off(batch):
    """A copied input tensor only; noncoordinate channels and metadata preserved."""
    result = dict(batch)
    result["inputs"] = batch["inputs"].clone()
    result["inputs"][:, :, 21:25] = 0
    return result


def explicit_identity():
    paths = ["src/larp/role_generalization.py", "src/larp/gru_baseline.py", "src/larp/transmission_probe.py",
             "src/larp/learning_diagnostics.py", "src/larp/model.py", "src/larp/data.py", "src/larp/graphs.py",
             "src/larp/geometry.py", "src/larp/artifacts.py", "configs/role_generalization_v1.json"]
    files = {name: file_hash(ROOT/name) for name in paths}
    runtime = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "torch", "psutil")}
    runtime.update(python=platform.python_version(), platform=platform.platform(), device="cpu", threads=4,
                   dtype="float32", deterministic_algorithms=True)
    return {"files": files, "runtime": runtime, "hash": digest({"files": files, "runtime": runtime})}


def preflight_control(record, model, seed, train_on, validation_on):
    checks = {"status": record["status"] == "COMPLETE", "seed": record["training_seed"] == seed,
              "geometry": record["geometry"] == "grid", "target": record["target"] == "b0",
              "mode": record["mode"] == "local", "parameters": record["parameters"] == model.parameter_count == 12481,
              "budget": record["updates_completed"] == 250,
              "initialization": record["initial_state_hash"] == state_hash(model),
              "train_input": record["train_input_hash"] == array_hash(train_on["inputs"].numpy()),
              "validation_input": record["validation_input_hash"] == array_hash(validation_on["inputs"].numpy()),
              "train_target": record["train_target_hash"] == array_hash(train_on["target"].numpy()),
              "validation_target": record["validation_target_hash"] == array_hash(validation_on["target"].numpy())}
    if not all(checks.values()):
        raise ValueError(f"COORDS_ON reused control differs: {checks}")
    return checks


def run_one(seed, batches, context, calendar, checks, cfg, directory, deadline):
    record = {"training_seed": seed, "condition": "COORDS_OFF", "status": "NOT_RUN", "finite": False,
              "control_reused_not_independent": True, "preflight": checks}
    if time.perf_counter() >= deadline:
        return {**record, "reason": "wall budget exhausted"}
    train, val = batches
    model = GGNNLikeModel(seed)
    assert model.parameter_count == cfg["parameters"]
    record.update(initial_state_hash=state_hash(model), parameters=model.parameter_count,
                  train_input_hash=array_hash(train["inputs"].numpy()), validation_input_hash=array_hash(val["inputs"].numpy()),
                  train_target_hash=array_hash(train["target"].numpy()), validation_target_hash=array_hash(val["target"].numpy()))
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg["lr"], betas=tuple(cfg["betas"]),
                                  eps=cfg["eps"], weight_decay=cfg["weight_decay"])
    status, completed, curve, times = "COMPLETE", 0, [], []
    begin = time.perf_counter()
    process = psutil.Process()
    peak = process.memory_info().rss
    for selected in calendar:
        if time.perf_counter() >= deadline:
            status = "RESOURCE_LIMIT"
            break
        optimizer.zero_grad(set_to_none=True)
        part = {name: train[name][selected] for name in ("inputs", "output", "target")}
        tick = time.perf_counter()
        logits = predictions(model, part, context, cfg["steps"])
        loss = F.binary_cross_entropy_with_logits(logits, part["target"])
        if not torch.isfinite(loss):
            status = "NUMERICAL_FAILURE_UNVERIFIED"
            break
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg["gradient_clip"])
        if not torch.isfinite(norm):
            status = "NUMERICAL_FAILURE_UNVERIFIED"
            break
        optimizer.step()
        times.append(time.perf_counter()-tick)
        completed += 1
        peak = max(peak, process.memory_info().rss)
        if completed == 1 or completed % 25 == 0:
            curve.append({"update": completed, "optimization_loss": float(loss.detach()), "preclip_gradient_norm": float(norm)})
    record.update(status=status, updates_completed=completed, optimization_curve=curve,
                  final_state_hash=state_hash(model), median_update_seconds=float(np.median(times)) if times else None)
    if time.perf_counter() < deadline:
        record["train"] = measure(model, train, context, cfg, "b0")
        record["validation"] = measure(model, val, context, cfg, "b0")
        record["finite"] = bool(record["train"]["finite"] and record["validation"]["finite"]
                                  and all(torch.isfinite(p).all() for p in model.parameters()))
    if time.perf_counter() >= deadline:
        record["status"] = "RESOURCE_LIMIT"
    record.update(seconds_including_measurement=time.perf_counter()-begin,
                  RSS_peak_bytes_sampled=max(peak, process.memory_info().rss))
    out = directory/f"coords_off_s{seed}"
    out.mkdir(parents=True, exist_ok=False)
    torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(), "completed_updates": completed,
                "frozen_calendar": calendar}, out/"final_checkpoint.pt")
    record["checkpoint_sha256"] = file_hash(out/"final_checkpoint.pt")
    write_json(out/"results.json", record)
    print("COORDS_OFF", seed, record["status"], completed, "train", record.get("train", {}).get("accuracy"),
          "val", record.get("validation", {}).get("accuracy"), flush=True)
    return record


def main(argv=None):
    begin = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"artifacts/role_generalization/v1")
    args = parser.parse_args(argv)
    cfg_path = ROOT/"configs/role_generalization_v1.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    torch.set_num_threads(cfg["cpu_threads"])
    torch.use_deterministic_algorithms(True)
    pool_path, calendar_path, control_prereg_path = (ROOT/cfg[name] for name in ("pool_file", "calendar_file", "control_preregistration"))
    prior = json.loads(pool_path.read_text(encoding="utf-8"))
    calendar_record = json.loads(calendar_path.read_text(encoding="utf-8"))
    control_prereg = json.loads(control_prereg_path.read_text(encoding="utf-8"))
    matched_settings = ["N", "L", "parameters", "training_seeds", "steps", "updates", "batch_size", "lr", "betas", "eps",
                        "weight_decay", "gradient_clip", "cpu_threads", "dtype"]
    if any(cfg[name] != control_prereg["protocol"][name] for name in matched_settings):
        raise ValueError("COORDS_ON model/optimizer/budget differs")
    frozen_gru_hash = control_prereg["identity"]["files"]["src/larp/gru_baseline.py"]
    if file_hash(ROOT/"src/larp/gru_baseline.py") != frozen_gru_hash:
        raise ValueError("published GGNNLikeModel source changed")
    context = graph_context(Geometry.load(ROOT/"artifacts/geometry/grid_N400_g1101.npz"))
    original = prior["geometries"]["grid"]
    if (array_hash(context["geometry"].points) != original["coordinates_hash"] or context["edges_hash"] != original["edges_hash"]
            or context["ports"].digest != original["ports"]["digest"]):
        raise ValueError("frozen graph/ports changed")
    triples = prior["pool"]["triples"]["local"]
    on = tuple(target_batch(bind_cases(context, make_cases(subset), "local"), "b0") for subset in (triples[:12], triples[12:]))
    off = tuple(coordinates_off(batch) for batch in on)
    controls, calendars, checks = {}, {}, {}
    for seed in cfg["training_seeds"]:
        controls[seed] = json.loads((ROOT/cfg["control_results"].format(seed=seed)).read_text(encoding="utf-8"))
        calendars[seed] = np.asarray(calendar_record["schedule"][str(seed)], dtype=np.int64)
        if not np.array_equal(calendars[seed], np.asarray(control_prereg["frozen_schedule"][str(seed)])):
            raise ValueError("BALANCED calendar differs from COORDS_ON")
        checks[seed] = preflight_control(controls[seed], GGNNLikeModel(seed), seed, *on)
    identity = explicit_identity()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {"protocol": cfg, "protocol_hash": digest(cfg), "identity": identity, "frozen_UTC": utc_now(),
                "pool_file_sha256": file_hash(pool_path), "calendar_file_sha256": file_hash(calendar_path),
                "control_preregistration_sha256": file_hash(control_prereg_path),
                "matched_model_optimizer_budget_settings": {name: cfg[name] for name in matched_settings},
                "preflight": {str(seed): checks[seed] for seed in cfg["training_seeds"]},
                "initial_shared_hashes": {str(seed): controls[seed]["initial_state_hash"] for seed in cfg["training_seeds"]},
                "calendars": {str(seed): calendars[seed] for seed in cfg["training_seeds"]},
                "inputs": {split: {"COORDS_ON": array_hash(a["inputs"].numpy()), "COORDS_OFF": array_hash(b["inputs"].numpy()),
                    "target": array_hash(a["target"].numpy()), "cases": a["cases"]} for split, a, b in zip(("train", "validation"), on, off)},
                "controls_reused_not_independent": {str(seed): {"path": cfg["control_results"].format(seed=seed),
                    "sha256": file_hash(ROOT/cfg["control_results"].format(seed=seed)),
                    "checkpoint_sha256": controls[seed]["checkpoint_sha256"]} for seed in cfg["training_seeds"]},
                "architecture_evidence": False, "test_opened": False, "priors_updated": False}
    write_json(args.output/"preregistration.json", manifest)
    (args.output/"protocol_frozen.md").write_text(
        "# Frozen coordinate input ablation\n\n" +
        "Original GGNNLikeModel,12481P,T16,B4,250updates,.003AdamW; Gridg1101,targetb0,seeds2101/2102. " +
        "Only change zeroes every slot21:25 at every node in copied train/val/measurement inputs. " +
        "COORDS_ON reused, same byte initialization/input noncoordinate channels/targets/calendars/graph/edge distances. " +
        "120s CPU4; final state only; both finite train+val>=.98 gate. No automatic XOR/MHU/remote, retries,test,AB or scientific gate override.\n\n" +
        f"Identity: {identity['hash']}\nProtocol: {manifest['protocol_hash']}\n", encoding="utf-8")
    deadline = begin+cfg["wall_budget_seconds"]
    records = [run_one(seed, off, context, calendars[seed], checks[seed], cfg, args.output, deadline) for seed in cfg["training_seeds"]]
    assert explicit_identity()["hash"] == identity["hash"], "frozen dependency changed"
    result = {"status": "COMPLETE" if all(r["status"] != "RESOURCE_LIMIT" for r in records) else "RESOURCE_LIMIT",
              "stage": "technical_role_generalization", "identity": identity, "records": records,
              "coords_off_gate": all(accuracy_gate(r, cfg["gate_accuracy"]) for r in records),
              "COORDS_ON_reused_controls": [{"training_seed": seed, "reused_not_independent": True,
                  "source": cfg["control_results"].format(seed=seed), "train": controls[seed]["train"],
                  "validation": controls[seed]["validation"]} for seed in cfg["training_seeds"]],
              "XOR_MHU_remote": {"status": "NOT_RUN", "reason": "outside this frozen two-run input ablation"},
              "seconds_actual": time.perf_counter()-begin, "completed_UTC": utc_now(), "architecture_evidence": False,
              "test_opened": False, "priors_updated": False, "pilot_gate_unchanged": True}
    write_json(args.output/"results.json", result)
    print("coords_off_gate", result["coords_off_gate"], flush=True)
    return result


if __name__ == "__main__":
    main()
