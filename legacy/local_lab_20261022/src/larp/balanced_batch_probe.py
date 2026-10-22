"""One fixed batch-coupling intervention; reuses RANDOM evidence explicitly."""
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

from .artifacts import array_hash, digest, file_hash, utc_now, write_json
from .geometry import Geometry
from .learning_diagnostics import bind_cases, graph_context, make_cases, predictions, state_hash
from .transmission_probe import GainProbeModel, accuracy_gate, measure, target_batch

ROOT = Path(__file__).resolve().parents[2]


def balanced_schedule(triple_count, updates, master_seed, training_seed, order_key):
    """Every update uses all patterns of one triple; cycles cover each triple once."""
    if triple_count < 1 or updates < 0:
        raise ValueError("positive triple count and nonnegative updates required")
    rng = np.random.default_rng(np.random.SeedSequence([master_seed, training_seed, order_key]))
    selected = []
    while len(selected) < updates:
        selected.extend(rng.permutation(triple_count).tolist())
    return np.array([[4*triple + pattern for pattern in range(4)] for triple in selected[:updates]], dtype=np.int64).reshape(-1, 4)


def explicit_identity():
    paths = ["src/larp/balanced_batch_probe.py", "src/larp/transmission_probe.py", "src/larp/learning_diagnostics.py",
             "src/larp/model.py", "src/larp/data.py", "src/larp/graphs.py", "src/larp/geometry.py", "src/larp/artifacts.py",
             "configs/balanced_batch_probe_v1.json"]
    files = {name: file_hash(ROOT / name) for name in paths}
    runtime = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "torch", "psutil")}
    runtime.update(python=platform.python_version(), platform=platform.platform(), threads=4,
                   device="cpu", dtype="float32", deterministic_algorithms=True)
    return {"files": files, "runtime": runtime, "hash": digest({"files": files, "runtime": runtime})}


def control_compatible(control, seed, train, val, model):
    """Byte identity of the factors held fixed; reused evidence is never a new seed."""
    checks = {
        "status_complete": control["status"] == "COMPLETE",
        "target": control["target"] == "b0", "gain": control["gain"] == 1,
        "geometry": control["geometry"] == "grid", "mode": control["mode"] == "local",
        "seed": control["training_seed"] == seed, "budget": control["updates_completed"] == 250,
        "initialization": control["initial_state_hash"] == state_hash(model),
        "train_inputs": control["train_input_hash"] == array_hash(train["inputs"].numpy()),
        "validation_inputs": control["validation_input_hash"] == array_hash(val["inputs"].numpy()),
        "train_targets": control["train_target_hash"] == array_hash(train["target"].numpy()),
        "validation_targets": control["validation_target_hash"] == array_hash(val["target"].numpy()),
    }
    if not all(checks.values()):
        raise ValueError(f"reused RANDOM control differs: {checks}")
    return checks


def run_one(seed, train, val, context, schedule, control, cfg, directory, deadline):
    if time.perf_counter() >= deadline:
        return {"training_seed": seed, "status": "NOT_RUN", "reason": "wall budget exhausted"}
    model = GainProbeModel(seed, cfg["increment_gain"])
    checks = control_compatible(control, seed, train, val, model)
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg["lr"], betas=tuple(cfg["betas"]),
                                  eps=cfg["eps"], weight_decay=cfg["weight_decay"])
    begin = time.perf_counter()
    record = {"training_seed": seed, "condition": "BALANCED", "status": "COMPLETE", "finite": False,
              "initial_state_hash": state_hash(model), "control_compatibility": checks,
              "random_control_reused_not_independent": True, "random_control_initial_state_hash": control["initial_state_hash"]}
    trace, gradient_curve, times, completed = [], [], [], 0
    process = psutil.Process()
    peak = process.memory_info().rss
    def trace_point(update):
        nonlocal peak
        trace.append({"update": update, "train": measure(model, train, context, cfg, "b0"),
                      "validation": measure(model, val, context, cfg, "b0")})
        peak = max(peak, process.memory_info().rss)
    trace_point(0)
    for selected in schedule:
        if time.perf_counter() >= deadline:
            record["status"] = "RESOURCE_LIMIT"
            break
        model.train()
        optimizer.zero_grad(set_to_none=True)
        part = {name: train[name][selected] for name in ("inputs", "output", "target")}
        tick = time.perf_counter()
        logits = predictions(model, part, context, cfg["steps"])
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, part["target"])
        if not torch.isfinite(loss):
            record["status"] = "NUMERICAL_FAILURE_UNVERIFIED"
            break
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg["gradient_clip"])
        if not torch.isfinite(norm):
            record["status"] = "NUMERICAL_FAILURE_UNVERIFIED"
            break
        optimizer.step()
        times.append(time.perf_counter()-tick)
        completed += 1
        gradient_curve.append({"update": completed, "triple_train_index": int(selected[0]//4),
                               "optimization_loss": float(loss.detach()), "preclip_parameter_gradient_norm": float(norm)})
        peak = max(peak, process.memory_info().rss)
        if completed in cfg["trace_updates"]:
            trace_point(completed)
    if trace[-1]["update"] != completed and time.perf_counter() < deadline:
        trace_point(completed)
    if time.perf_counter() >= deadline:
        record["status"] = "RESOURCE_LIMIT"
    record.update(updates_completed=completed, final_state_hash=state_hash(model), trace=trace,
                  optimization_gradient_curve=gradient_curve, train=trace[-1]["train"], validation=trace[-1]["validation"],
                  score_checkpoint_update=trace[-1]["update"],
                  exposure_count_by_case=np.bincount(schedule[:completed].ravel(), minlength=len(train["inputs"])),
                  median_update_seconds=float(np.median(times)) if times else None,
                  seconds_including_trace=time.perf_counter()-begin, RSS_peak_bytes_sampled=peak)
    record["finite"] = bool(record["train"]["finite"] and record["validation"]["finite"]
                              and all(torch.isfinite(p).all() for p in model.parameters()))
    out = directory / f"balanced_s{seed}"
    out.mkdir(parents=True, exist_ok=False)
    torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(), "completed_updates": completed,
                "frozen_schedule": schedule}, out / "final_checkpoint.pt")
    record["checkpoint_sha256"] = file_hash(out / "final_checkpoint.pt")
    write_json(out / "results.json", record)
    print("BALANCED", seed, record["status"], completed, "train", record["train"]["accuracy"],
          "validation", record["validation"]["accuracy"], flush=True)
    return record


def main(argv=None):
    begin = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "balanced_batch_probe" / "v1")
    args = parser.parse_args(argv)
    cfg = json.loads((ROOT / "configs/balanced_batch_probe_v1.json").read_text(encoding="utf-8"))
    torch.set_num_threads(cfg["cpu_threads"])
    torch.use_deterministic_algorithms(True)
    prior_path = ROOT / cfg["pool_file"]
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    control_protocol_path = ROOT / "artifacts/transmission_probe/v1/preregistration.json"
    control_protocol = json.loads(control_protocol_path.read_text(encoding="utf-8"))["protocol"]
    same_settings = ["N", "L", "variant", "steps", "updates", "batch_size", "lr", "betas", "eps",
                     "weight_decay", "gradient_clip", "cpu_threads", "dtype", "minibatch_order_key"]
    if any(cfg[name] != control_protocol[name] for name in same_settings):
        raise ValueError("RANDOM control model/optimizer/budget differs")
    context = graph_context(Geometry.load(ROOT / "artifacts/geometry/grid_N400_g1101.npz"))
    original = prior["geometries"]["grid"]
    if (array_hash(context["geometry"].points) != original["coordinates_hash"] or context["edges_hash"] != original["edges_hash"]
            or context["ports"].digest != original["ports"]["digest"]):
        raise ValueError("previously frozen Grid graph/ports changed")
    triples = prior["pool"]["triples"]["local"]
    train = target_batch(bind_cases(context, make_cases(triples[:12]), "local"), "b0")
    val = target_batch(bind_cases(context, make_cases(triples[12:]), "local"), "b0")
    controls, schedules = {}, {}
    for seed in cfg["training_seeds"]:
        control_path = ROOT / cfg["random_control_results"].format(seed=seed)
        controls[seed] = json.loads(control_path.read_text(encoding="utf-8"))
        schedules[seed] = balanced_schedule(12, cfg["updates"], cfg["master_seed"], seed, cfg["minibatch_order_key"])
    identity = explicit_identity()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {"protocol": cfg, "protocol_hash": digest(cfg), "identity": identity, "frozen_UTC": utc_now(),
                "prior_pool_file_hash": file_hash(prior_path), "random_controls_reused_not_independent": True,
                "random_control_protocol_sha256": file_hash(control_protocol_path),
                "matched_model_optimizer_budget_settings": {name: cfg[name] for name in same_settings},
                "random_control_files": {str(seed): {"path": cfg["random_control_results"].format(seed=seed),
                    "file_sha256": file_hash(ROOT/cfg["random_control_results"].format(seed=seed)),
                    "checkpoint_sha256": controls[seed]["checkpoint_sha256"]} for seed in cfg["training_seeds"]},
                "schedule": {str(seed): schedules[seed] for seed in cfg["training_seeds"]},
                "train_cases": train["cases"], "validation_cases": val["cases"],
                "train_input_hash": array_hash(train["inputs"].numpy()), "validation_input_hash": array_hash(val["inputs"].numpy()),
                "train_target_hash": array_hash(train["target"].numpy()), "validation_target_hash": array_hash(val["target"].numpy()),
                "architecture_evidence": False, "test_opened": False, "priors_updated": False}
    write_json(args.output / "preregistration.json", manifest)
    (args.output / "protocol_frozen.md").write_text(
        "# Frozen batch-coupling diagnostic\n\n" +
        "BALANCED versus previously observed RANDOM, explicitly reused control. Only minibatch coupling changes: " +
        "all4patterns of one triple perB4. Triple cycles randomized without replacement. Same48train/16validation, " +
        "bits/roles/ports/graph, initialization, b0 target, gain1, T16, AdamW.003,250updates. " +
        "Two seeds2101/2102; CPU4; total120s. All patterns/source gradients recorded at0,1,25…250. " +
        "Finite final train+val>=.98 in both seeds defines a technical success; no pilot override, test, H1–H6, retries, fullbatch48.\n\n" +
        f"Identity: {identity['hash']}\nProtocol hash: {manifest['protocol_hash']}\n", encoding="utf-8")
    deadline = begin + cfg["wall_budget_seconds"]
    records = [run_one(seed, train, val, context, schedules[seed], controls[seed], cfg, args.output, deadline)
               for seed in cfg["training_seeds"]]
    assert explicit_identity()["hash"] == identity["hash"], "frozen dependency changed"
    result = {"status": "COMPLETE" if all(r["status"] != "RESOURCE_LIMIT" for r in records) else "RESOURCE_LIMIT",
              "stage": "technical_batch_probe", "identity": identity, "records": records,
              "random_controls": [{"training_seed": seed, "reused_not_independent": True,
                  "source": cfg["random_control_results"].format(seed=seed), "train": controls[seed]["train"],
                  "validation": controls[seed]["validation"]} for seed in cfg["training_seeds"]],
              "balanced_gate": all(accuracy_gate(r, cfg["gate_accuracy"]) for r in records),
              "full_batch_48": {"status": "NOT_RUN", "reason": "outside this frozen single-factor diagnostic"},
              "seconds_actual": time.perf_counter()-begin, "completed_UTC": utc_now(),
              "architecture_evidence": False, "test_opened": False, "priors_updated": False, "pilot_gate_unchanged": True}
    write_json(args.output / "results.json", result)
    print("balanced_gate", result["balanced_gate"], flush=True)
    return result


if __name__ == "__main__":
    main()
