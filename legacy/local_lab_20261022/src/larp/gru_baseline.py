"""Isolated GGNN-like baseline; never substitutes the nominal LARP block.

The GRU input is [incoming mean message, persistent encoding], raw h is its
hidden state. Capacity is explicitly close but not exactly matched to G.
"""
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
from torch.nn import functional as F

from .artifacts import array_hash, digest, file_hash, utc_now, write_json
from .geometry import Geometry
from .learning_diagnostics import bind_cases, graph_context, make_cases, predictions, state_hash
from .model import LARPModel
from .transmission_probe import accuracy_gate, measure, target_batch

ROOT = Path(__file__).resolve().parents[2]


class GGNNLikeModel(nn.Module):
    """Shared GRU32, same initial encoder/message/readout; marks ignored."""
    def __init__(self, seed=2101):
        super().__init__()
        self.seed = int(seed)
        original = LARPModel("G", 1, seed=seed)
        for name in ("encoder", "normalization", "message", "readout1", "readout2"):
            setattr(self, name, getattr(original, name))
        self.distance_weight = original.distance_weight
        with torch.random.fork_rng(devices=[]):
            self.gru = nn.GRUCell(64, 32)
        for key, name in ((1, "weight_ih"), (2, "weight_hh")):
            value = int(np.random.SeedSequence([seed, 9921, key]).generate_state(1, dtype=np.uint64)[0])
            generator = torch.Generator(device="cpu").manual_seed(value % (2**63-1))
            nn.init.xavier_uniform_(getattr(self.gru, name), gain=1., generator=generator)
        nn.init.zeros_(self.gru.bias_ih)
        nn.init.zeros_(self.gru.bias_hh)

    @property
    def parameter_count(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(self, inputs, edge_index, edge_dist, labels=None, steps=16, return_states=False):
        if inputs.ndim != 3 or inputs.shape[-1] != 25 or steps < 0:
            raise ValueError("[B,N,25] and nonnegative horizon required")
        batch, n, _ = inputs.shape
        edges = torch.as_tensor(edge_index, dtype=torch.long, device=inputs.device)
        if edges.ndim != 2 or edges.shape[0] != 2:
            raise ValueError("edges must be [2,E]")
        if edges.numel() and (int(edges.min()) < 0 or int(edges.max()) >= n):
            raise ValueError("edge index outside node set")
        source, target = edges
        dist = torch.as_tensor(edge_dist, dtype=inputs.dtype, device=inputs.device).reshape(-1)
        if len(dist) != len(source):
            raise ValueError("one distance per directed arc required")
        count = inputs.new_zeros(n)
        count.index_add_(0, target, inputs.new_ones(len(target)))
        count = count.clamp_min(1).view(1, n, 1)
        encoded = self.encoder(inputs)
        h = encoded
        feature = torch.log1p(dist).view(1, -1, 1) * self.distance_weight.view(1, 1, 32)
        states = [h] if return_states else None
        for _ in range(steps):
            messages = torch.tanh(self.message(self.normalization(h))[:, source] + feature)
            mean = inputs.new_zeros(batch, n, 32)
            mean.index_add_(1, target, messages)
            mean = mean / count
            h = self.gru(torch.cat((mean, encoded), dim=-1).reshape(-1, 64), h.reshape(-1, 32)).reshape(batch, n, 32)
            if return_states:
                states.append(h)
        logits = self.readout2(F.silu(self.readout1(h)))
        return (logits, states) if return_states else logits


def explicit_identity():
    paths = ["src/larp/gru_baseline.py", "src/larp/transmission_probe.py", "src/larp/learning_diagnostics.py",
             "src/larp/model.py", "src/larp/data.py", "src/larp/graphs.py", "src/larp/geometry.py", "src/larp/artifacts.py",
             "configs/gru_baseline_v1.json"]
    files = {name: file_hash(ROOT/name) for name in paths}
    runtime = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "torch", "psutil")}
    runtime.update(python=platform.python_version(), platform=platform.platform(), threads=4, dtype="float32",
                   device="cpu", deterministic_algorithms=True)
    return {"files": files, "runtime": runtime, "hash": digest({"files": files, "runtime": runtime})}


def run_one(kind, mode, target, seed, base, context, schedule, cfg, directory, deadline):
    name = f"{mode}_{kind}_{target}_s{seed}"
    record = {"name": name, "geometry": kind, "mode": mode, "target": target, "training_seed": seed,
              "status": "NOT_RUN", "finite": False}
    if time.perf_counter() >= deadline:
        return {**record, "reason": "wall budget exhausted"}
    train, val = (target_batch(batch, target) for batch in base)
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
    for selected in schedule:
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
        record["train"] = measure(model, train, context, cfg, target)
        record["validation"] = measure(model, val, context, cfg, target)
        record["finite"] = bool(record["train"]["finite"] and record["validation"]["finite"]
                                  and all(torch.isfinite(p).all() for p in model.parameters()))
    if time.perf_counter() >= deadline:
        record["status"] = "RESOURCE_LIMIT"
    record.update(seconds_including_measurement=time.perf_counter()-begin,
                  RSS_peak_bytes_sampled=max(peak, process.memory_info().rss))
    out = directory/name
    out.mkdir(parents=True, exist_ok=False)
    torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(), "completed_updates": completed,
                "frozen_schedule": schedule}, out/"final_checkpoint.pt")
    record["checkpoint_sha256"] = file_hash(out/"final_checkpoint.pt")
    write_json(out/"results.json", record)
    print(name, record["status"], completed, "train", record.get("train", {}).get("accuracy"),
          "val", record.get("validation", {}).get("accuracy"), flush=True)
    return record


def main(argv=None):
    begin = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"artifacts/gru_baseline/v1")
    args = parser.parse_args(argv)
    cfg = json.loads((ROOT/"configs/gru_baseline_v1.json").read_text(encoding="utf-8"))
    torch.set_num_threads(cfg["cpu_threads"])
    torch.use_deterministic_algorithms(True)
    prior_path, calendar_path = ROOT/cfg["pool_file"], ROOT/cfg["calendar_file"]
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    calendar = json.loads(calendar_path.read_text(encoding="utf-8"))
    schedule = {seed: np.asarray(calendar["schedule"][str(seed)], dtype=np.int64) for seed in cfg["training_seeds"]}
    if any(value.shape != (250, 4) for value in schedule.values()):
        raise ValueError("frozen BALANCED calendar differs from 250/B4")
    contexts = {kind: graph_context(Geometry.load(ROOT/f"artifacts/geometry/{kind}_N400_g1101.npz")) for kind in cfg["geometries"]}
    for kind, c in contexts.items():
        original = prior["geometries"][kind]
        if (array_hash(c["geometry"].points) != original["coordinates_hash"] or c["edges_hash"] != original["edges_hash"]
                or c["ports"].digest != original["ports"]["digest"]):
            raise ValueError("frozen geometry, graph or ports changed")
    batches = {(kind, mode): tuple(bind_cases(c, make_cases(triples), mode) for triples in (
                    prior["pool"]["triples"][mode][:12], prior["pool"]["triples"][mode][12:]))
               for kind, c in contexts.items() for mode in ("local", "remote")}
    if array_hash(batches["grid", "local"][0]["inputs"].numpy()) != calendar["train_input_hash"]:
        raise ValueError("Grid local input bytes differ from BALANCED control")
    identity = explicit_identity()
    manifest = {"protocol": cfg, "protocol_hash": digest(cfg), "identity": identity, "frozen_UTC": utc_now(),
                "prior_pool_sha256": file_hash(prior_path), "prior_calendar_sha256": file_hash(calendar_path),
                "frozen_schedule": {str(seed): schedule[seed] for seed in cfg["training_seeds"]},
                "pool": prior["pool"], "geometries": prior["geometries"],
                "inputs": {f"{kind}_{mode}": {"train": array_hash(bs[0]["inputs"].numpy()),
                            "validation": array_hash(bs[1]["inputs"].numpy())} for (kind, mode), bs in batches.items()},
                "architecture_evidence": False, "test_opened": False, "priors_updated": False}
    args.output.mkdir(parents=True, exist_ok=False)
    write_json(args.output/"preregistration.json", manifest)
    (args.output/"protocol_frozen.md").write_text(
        "# Frozen GRU baseline diagnostic\n\n" +
        "GGNN-like GRU32 input[m32,u32], hiddenrawh32; no residual. Original encoder/LN/tanhmessage+distance/mean/readout kept " +
        "with byte-identical initial parameters. GRUW Xavier namespace9921, biases0. 12481P versus12261, notexactmatched. " +
        "Frozen same BALANCED calendar/inputs/roles/ports/triples; T16, B4, AdamW.003,250updates, seeds2101/2102. " +
        "Order Grid-localb0(2)→Grid-localXOR(2)→MHU-localb0/XOR(4)→remoteall(8). " +
        "Each gate requires bothseeds finite train+val>=.98 in every prior condition. Total240s CPU4, no retries/HPO/test/H1–H6/pilotoverride.\n\n" +
        f"Identity: {identity['hash']}\nProtocol: {manifest['protocol_hash']}\n", encoding="utf-8")
    deadline = begin+cfg["wall_budget_seconds"]
    records = []
    def block(kind, mode, targets, opened, reason):
        block_records = []
        for target in targets:
            for seed in cfg["training_seeds"]:
                r = (run_one(kind, mode, target, seed, batches[kind, mode], contexts[kind], schedule[seed], cfg, args.output, deadline) if opened else
                     {"name": f"{mode}_{kind}_{target}_s{seed}", "geometry": kind, "mode": mode, "target": target,
                      "training_seed": seed, "status": "NOT_RUN", "finite": False, "reason": reason})
                records.append(r)
                block_records.append(r)
        return opened and all(accuracy_gate(r, cfg["gate_accuracy"]) for r in block_records)
    grid_copy = block("grid", "local", ["b0"], True, "")
    grid_xor = block("grid", "local", ["xor"], grid_copy, "Grid local b0 gate failed or incomplete")
    common_local = block("mhu", "local", cfg["targets"], grid_xor, "Grid local XOR gate failed or incomplete")
    for kind in cfg["geometries"]:
        block(kind, "remote", cfg["targets"], common_local, "common local gates failed or incomplete")
    assert explicit_identity()["hash"] == identity["hash"], "frozen dependency changed"
    result = {"status": "COMPLETE" if all(r["status"] != "RESOURCE_LIMIT" for r in records) else "RESOURCE_LIMIT",
              "stage": "technical_gru_baseline", "identity": identity, "records": records,
              "grid_local_b0_gate": grid_copy, "grid_local_XOR_gate": grid_xor, "common_local_gate": common_local,
              "seconds_actual": time.perf_counter()-begin, "completed_UTC": utc_now(), "architecture_evidence": False,
              "test_opened": False, "priors_updated": False, "pilot_gate_unchanged": True}
    write_json(args.output/"results.json", result)
    print("grid_copy", grid_copy, "grid_XOR", grid_xor, "common_local", common_local, flush=True)
    return result


if __name__ == "__main__":
    main()
