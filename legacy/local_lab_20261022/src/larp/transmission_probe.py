"""One frozen 2x2 target/gain diagnostic; original model and evidence stay intact."""
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
from torch import nn

from .artifacts import array_hash, digest, file_hash, utc_now, write_json
from .geometry import Geometry
from .learning_diagnostics import bind_cases, graph_context, make_cases, predictions, state_hash
from .model import LARPModel

ROOT = Path(__file__).resolve().parents[2]


class GainProbeModel(LARPModel):
    """Scalar factor of the complete increment, no added capacity or graph change."""
    def __init__(self, seed=2101, increment_gain=1.0):
        super().__init__("G", 1, seed=seed)
        if increment_gain not in {1.0, 10.0}:
            raise ValueError("only preregistered factors 1 and 10 are supported")
        self.increment_gain = float(increment_gain)

    def increment(self, z, message, encoded, labels):
        result = super().increment(z, message, encoded, labels)
        # Returning the same tensor at gain1 avoids even a needless multiply;
        # that branch must reproduce the original forward bit for bit.
        return result if self.increment_gain == 1 else result * self.increment_gain


def target_batch(batch, target):
    """The only task change is its labels: all inputs and interfaces are shared."""
    result = dict(batch)
    if target == "b0":
        result["target"] = torch.tensor(batch["cases"][:, 3:4], dtype=torch.float32)
    elif target != "xor":
        raise ValueError("unknown target")
    return result


def explicit_identity():
    paths = ["src/larp/transmission_probe.py", "src/larp/learning_diagnostics.py", "src/larp/model.py",
             "src/larp/data.py", "src/larp/graphs.py", "src/larp/geometry.py", "src/larp/artifacts.py",
             "configs/transmission_probe_v1.json"]
    files = {name: file_hash(ROOT / name) for name in paths}
    runtime = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "torch", "psutil")}
    runtime.update(python=platform.python_version(), platform=platform.platform(), device="cpu", threads=4,
                   dtype="float32", deterministic_algorithms=True)
    return {"files": files, "runtime": runtime, "hash": digest({"files": files, "runtime": runtime})}


def accuracy_gate(record, threshold=.98):
    return (record.get("status") == "COMPLETE" and record.get("finite", False)
            and record.get("train", {}).get("accuracy", 0) >= threshold
            and record.get("validation", {}).get("accuracy", 0) >= threshold)


def copy_gate(records, cfg, geometries):
    """Require one common fixed factor, all expected seeds, both splits, finite."""
    for gain in cfg["increment_gains"]:
        chosen = [r for r in records if r["mode"] == "local" and r["target"] == "b0"
                  and r["gain"] == gain and r["geometry"] in geometries]
        expected = {(geometry, seed) for geometry in geometries for seed in cfg["training_seeds"]}
        if {(r["geometry"], r["training_seed"]) for r in chosen} == expected and all(
                accuracy_gate(r, cfg["gate_accuracy"]) for r in chosen):
            return True
    return False


def measure(model, batch, context, cfg, target):
    """Report every pattern and correct flip label for the selected target."""
    model.eval()
    observed = []
    for start in range(0, len(batch["inputs"]), 4):
        stop = min(start + 4, len(batch["inputs"]))
        x = batch["inputs"][start:stop].clone().requires_grad_(True)
        output = batch["output"][start:stop]
        logits = predictions(model, {"inputs": x, "output": output}, context, cfg["steps"])
        gradient = torch.autograd.grad(logits.sum(), x)[0]
        flipped_logits = []
        for role in range(2):
            counter_x = x.detach().clone()
            source = batch["sources"][start:stop, role]
            counter_x[torch.arange(len(x)), source, 1] = 1 - counter_x[torch.arange(len(x)), source, 1]
            with torch.no_grad():
                counter = predictions(model, {"inputs": counter_x, "output": output}, context, cfg["steps"])
            flipped_logits.append(counter.numpy().ravel())
        values = logits.detach().numpy().ravel()
        for row, value in enumerate(values):
            index = start + row
            label = float(batch["target"][index, 0])
            flips_label = [True, target == "xor"]
            expected_labels = [1-label if flip else label for flip in flips_label]
            observed.append({"case": batch["cases"][index].tolist(), "target": label,
                "logit": float(value), "prediction": int(value >= 0),
                "hops": [float(context["hops"][source, int(output[row])]) for source in batch["sources"][index]],
                "source_gradients": [float(gradient[row, source, 1]) for source in batch["sources"][index]],
                "source_flipped_logits": [float(c[row]) for c in flipped_logits],
                "source_flip_abs_logit_changes": [float(abs(c[row]-value)) for c in flipped_logits],
                "source_flip_should_change_target": flips_label,
                "source_flip_correct_predictions": [bool((c[row] >= 0) == label_after) for c, label_after in zip(flipped_logits, expected_labels)],
                "source_flip_class_changes": [bool((c[row] >= 0) != (value >= 0)) for c in flipped_logits]})
    values = torch.tensor([r["logit"] for r in observed])[:, None]
    gradients = np.array([r["source_gradients"] for r in observed])
    loss = float(nn.functional.binary_cross_entropy_with_logits(values, batch["target"]))
    return {"accuracy": float(np.mean([r["prediction"] == r["target"] for r in observed])), "loss": loss,
            "source_gradient_abs_median_by_role": np.median(abs(gradients), axis=0).tolist(),
            "source_flip_correct_fraction_by_role": np.mean([r["source_flip_correct_predictions"] for r in observed], axis=0).tolist(),
            "source_flip_class_change_fraction_by_role": np.mean([r["source_flip_class_changes"] for r in observed], axis=0).tolist(),
            "finite": bool(np.isfinite(values.numpy()).all() and np.isfinite(gradients).all() and np.isfinite(loss)),
            "cases": observed}


def run_one(kind, mode, target, gain, seed, base_batches, context, cfg, directory, deadline):
    name = f"{mode}_{kind}_{target}_gain{gain:g}_s{seed}"
    record = {"name": name, "geometry": kind, "mode": mode, "target": target,
              "gain": gain, "training_seed": seed, "status": "NOT_RUN", "finite": False}
    if time.perf_counter() >= deadline:
        return {**record, "reason": "wall budget exhausted"}
    train, val = (target_batch(batch, target) for batch in base_batches)
    model = GainProbeModel(seed, gain)
    record.update(initial_state_hash=state_hash(model), parameter_count=model.parameter_count,
        train_input_hash=array_hash(train["inputs"].numpy()), validation_input_hash=array_hash(val["inputs"].numpy()),
        train_target_hash=array_hash(train["target"].numpy()), validation_target_hash=array_hash(val["target"].numpy()))
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg["lr"], betas=tuple(cfg["betas"]),
                                  eps=cfg["eps"], weight_decay=cfg["weight_decay"])
    rng = np.random.default_rng(np.random.SeedSequence([cfg["master_seed"], seed, cfg["minibatch_order_key"]]))
    order, cursor, completed = rng.permutation(len(train["inputs"])), 0, 0
    curve, times = [], []
    status = "COMPLETE"
    process = psutil.Process()
    peak = process.memory_info().rss
    begin = time.perf_counter()
    for _ in range(cfg["updates"]):
        if time.perf_counter() >= deadline:
            status = "RESOURCE_LIMIT"
            break
        if cursor == len(order):
            order, cursor = rng.permutation(len(order)), 0
        selected = order[cursor:cursor+cfg["batch_size"]]
        cursor += len(selected)
        batch = {name: train[name][selected] for name in ("inputs", "output", "target")}
        tick = time.perf_counter()
        optimizer.zero_grad(set_to_none=True)
        logits = predictions(model, batch, context, cfg["steps"])
        loss = nn.functional.binary_cross_entropy_with_logits(logits, batch["target"])
        if not torch.isfinite(loss):
            status = "NUMERICAL_FAILURE_UNVERIFIED"
            break
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg["gradient_clip"])
        if not torch.isfinite(norm):
            status = "NUMERICAL_FAILURE_UNVERIFIED"
            break
        optimizer.step()
        completed += 1
        times.append(time.perf_counter() - tick)
        peak = max(peak, process.memory_info().rss)
        if completed == 1 or completed % 25 == 0:
            curve.append({"update": completed, "optimization_loss": float(loss.detach()),
                          "preclip_gradient_norm": float(norm)})
    record.update(status=status, updates_completed=completed, optimization_curve=curve,
                  update_seconds_median=float(np.median(times)) if times else None,
                  final_state_hash=state_hash(model))
    if time.perf_counter() < deadline:
        record["train"] = measure(model, train, context, cfg, target)
        record["validation"] = measure(model, val, context, cfg, target)
        record["finite"] = bool(record["train"]["finite"] and record["validation"]["finite"]
                                  and all(torch.isfinite(p).all() for p in model.parameters()))
    if time.perf_counter() >= deadline:
        record["status"] = "RESOURCE_LIMIT"
    record.update(seconds_including_final_measurement=time.perf_counter()-begin,
                  RSS_peak_bytes_sampled=max(peak, process.memory_info().rss))
    original = ROOT / "artifacts" / "learning_diagnostics" / "v1" / f"{mode}_{kind}_s{seed}" / "results.json"
    if gain == 1 and target == "xor" and original.exists() and record["status"] == "COMPLETE":
        original_record = json.loads(original.read_text(encoding="utf-8"))
        record["gain1_XOR_reproduces_previous_final_state"] = record["final_state_hash"] == original_record["final_state_hash"]
    out = directory / name
    out.mkdir(parents=True, exist_ok=False)
    torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(), "completed_updates": completed,
                "order": order, "cursor": cursor, "rng": rng.bit_generator.state}, out / "final_checkpoint.pt")
    record["checkpoint_sha256"] = file_hash(out / "final_checkpoint.pt")
    write_json(out / "results.json", record)
    print(name, record["status"], completed, "train", record.get("train", {}).get("accuracy"),
          "val", record.get("validation", {}).get("accuracy"), flush=True)
    return record


def main(argv=None):
    begin = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "transmission_probe" / "v1")
    parser.add_argument("--freeze-only", action="store_true", help="inspect identity/protocol without creating evidence")
    args = parser.parse_args(argv)
    cfg = json.loads((ROOT / "configs" / "transmission_probe_v1.json").read_text(encoding="utf-8"))
    torch.set_num_threads(cfg["cpu_threads"])
    torch.use_deterministic_algorithms(True)
    prior_path = ROOT / cfg["pool_file"]
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    if prior["pool"]["status"] != "AVAILABLE":
        raise ValueError("DIAGNOSTIC_UNAVAILABLE: previous strict pool absent")
    contexts = {kind: graph_context(Geometry.load(ROOT / "artifacts" / "geometry" / f"{kind}_N400_g1101.npz")) for kind in cfg["geometries"]}
    for kind, c in contexts.items():
        original = prior["geometries"][kind]
        if (array_hash(c["geometry"].points) != original["coordinates_hash"] or c["edges_hash"] != original["edges_hash"]
                or c["ports"].digest != original["ports"]["digest"]):
            raise ValueError("previously frozen geometry/graph/ports changed")
    batches = {(kind, mode): tuple(bind_cases(c, make_cases(triples), mode) for triples in (
                    prior["pool"]["triples"][mode][:prior["pool"]["train_triples"]],
                    prior["pool"]["triples"][mode][prior["pool"]["train_triples"]:]))
               for kind, c in contexts.items() for mode in ("local", "remote")}
    identity = explicit_identity()
    manifest = {"protocol": cfg, "protocol_hash": digest(cfg), "identity": identity,
                "frozen_UTC": utc_now(), "prior_pool_file_hash": file_hash(prior_path),
                "prior_diagnostic_identity": prior["identity"]["hash"], "pool": prior["pool"],
                "inputs": {f"{kind}_{mode}": {"train": array_hash(bs[0]["inputs"].numpy()),
                            "validation": array_hash(bs[1]["inputs"].numpy()), "cases_train": bs[0]["cases"],
                            "cases_validation": bs[1]["cases"]} for (kind, mode), bs in batches.items()},
                "geometries": prior["geometries"], "architecture_evidence": False,
                "test_opened": False, "priors_updated": False}
    if args.freeze_only:
        print(json.dumps({"identity": identity, "protocol_hash": manifest["protocol_hash"], "status": "NOT_RUN"}, indent=2))
        return manifest
    args.output.mkdir(parents=True, exist_ok=False)
    write_json(args.output / "preregistration.json", manifest)
    (args.output / "protocol_frozen.md").write_text(
        "# Frozen transmission diagnostic\n\n" +
        "Targets b0/XOR cross gains1/10 inside the original complete increment; original .1 residual multiplier stays unchanged. " +
        "Exact inputs, roles, triples, initialization, T16, optimizer,250updates. CPU4; total ceiling360s. " +
        "First Grid-local8runs; MHU-local8 only if one fixed gain obtains finite b0 train+val>=.98 in both Grid seeds. " +
        "Remote16 only if one common fixed gain obtains that gate in both geometries/seeds. " +
        "All factors run when opened; no gain winner selected, retries, test, architecture evidence or scientific gate override.\n\n" +
        f"Identity: {identity['hash']}\nProtocol hash: {manifest['protocol_hash']}\n", encoding="utf-8")
    deadline = begin + cfg["wall_budget_seconds"]
    records = []
    def block(kind, mode, opened, reason):
        for target in cfg["targets"]:
            for gain in cfg["increment_gains"]:
                for seed in cfg["training_seeds"]:
                    record = (run_one(kind, mode, target, gain, seed, batches[kind, mode], contexts[kind], cfg, args.output, deadline) if opened else
                              {"name": f"{mode}_{kind}_{target}_gain{gain:g}_s{seed}", "geometry": kind, "mode": mode,
                               "target": target, "gain": gain, "training_seed": seed, "status": "NOT_RUN", "reason": reason, "finite": False})
                    records.append(record)
    block("grid", "local", True, "")
    grid_gate = copy_gate(records, cfg, ["grid"])
    block("mhu", "local", grid_gate, "Grid local-copy gate failed or incomplete")
    remote_gate = copy_gate(records, cfg, cfg["geometries"])
    for kind in cfg["geometries"]:
        block(kind, "remote", remote_gate, "common local-copy gate failed or incomplete")
    assert explicit_identity()["hash"] == identity["hash"], "frozen dependency changed during execution"
    result = {"status": "COMPLETE" if all(r["status"] != "RESOURCE_LIMIT" for r in records) else "RESOURCE_LIMIT",
              "stage": "technical_transmission_probe", "architecture_evidence": False,
              "test_opened": False, "priors_updated": False, "pilot_gate_unchanged": True,
              "identity": identity, "grid_local_copy_gate": grid_gate, "common_local_copy_gate": remote_gate,
              "seconds_actual": time.perf_counter()-begin, "completed_UTC": utc_now(), "records": records}
    write_json(args.output / "results.json", result)
    print("grid_copy_gate", grid_gate, "common_copy_gate", remote_gate, flush=True)
    return result


if __name__ == "__main__":
    main()
