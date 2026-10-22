"""Preregistered bounded diagnostics; no mutation of LARP v0.1 or its gates.

Run as ``python -m larp.learning_diagnostics``. Freeze precedes all optimization.
The direct-local task deliberately places both bits at the receiver; it is not
the scientific remote XOR and its success cannot open the original pilot.
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

from .artifacts import array_hash, digest, file_hash, utc_now, write_json
from .data import coordinate_channels, minimum_image_displacements, register_ports, xor_oracle
from .geometry import Geometry
from .graphs import directed_distances, knn_graph
from .model import LARPModel

ROOT = Path(__file__).resolve().parents[2]
PATTERNS = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)


def explicit_identity(root=ROOT):
    """Only named dependencies, so concurrently authored modules cannot drift identity."""
    paths = ["src/larp/learning_diagnostics.py", "src/larp/model.py", "src/larp/data.py",
             "src/larp/graphs.py", "src/larp/geometry.py", "src/larp/artifacts.py",
             "configs/learning_diagnostics_v1.json"]
    files = {name: file_hash(root / name) for name in paths}
    runtime = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "torch", "psutil")}
    runtime.update(python=platform.python_version(), platform=platform.platform(),
                   device="cpu", threads=4, dtype="float32", deterministic_algorithms=True)
    return {"files": files, "runtime": runtime, "hash": digest({"files": files, "runtime": runtime})}


def state_hash(model):
    return digest({name: array_hash(tensor.detach().cpu().numpy())
                   for name, tensor in model.state_dict().items()})


def graph_context(geometry):
    edges = knn_graph(geometry.points, geometry.L, 6)
    delta = minimum_image_displacements(geometry.points[edges[0]], geometry.points[edges[1]], geometry.L)
    return {"geometry": geometry, "ports": register_ports(geometry.points, geometry.L),
            "edge_index": torch.tensor(edges, dtype=torch.long),
            "edge_dist": torch.tensor(np.linalg.norm(delta, axis=1), dtype=torch.float32),
            "labels": torch.tensor(np.array(geometry.labels), dtype=torch.long),
            "hops": directed_distances(edges, geometry.N), "edges_hash": array_hash(edges)}


def bind_cases(context, cases, mode):
    """Cases are [destination logical ID, source0 ID, source1 ID, bit0, bit1]."""
    geometry, ports = context["geometry"], context["ports"]
    cases = np.asarray(cases, dtype=np.int64)
    b = len(cases)
    x = np.zeros((b, geometry.N, 25), dtype=np.float32)
    x[:, :, 21:25] = coordinate_channels(geometry.points, geometry.L)
    x[:, ports.indices, 21:25] = coordinate_channels(ports.sites, geometry.L)
    output = ports.indices[cases[:, 0]]
    rows = np.arange(b)
    x[rows, output, 0] = 1
    if mode == "direct_local":
        x[rows, output, 1:3] = cases[:, 3:5]
        source_nodes = np.repeat(output[:, None], 2, axis=1)
        source_channels = np.broadcast_to(np.array([1, 2]), (b, 2)).copy()
    elif mode in {"local", "remote"}:
        source_nodes = ports.indices[cases[:, 1:3]]
        if np.any(source_nodes[:, 0] == source_nodes[:, 1]) or np.any(source_nodes == output[:, None]):
            raise ValueError("separate interfaces require three distinct sites")
        for role in range(2):
            x[rows, source_nodes[:, role], 0] = 1
            x[rows, source_nodes[:, role], 9 + role] = 1
            x[rows, source_nodes[:, role], 1] = cases[:, 3 + role]
        x[rows, output, 14:16] = 1
        source_channels = np.ones((b, 2), dtype=np.int64)
    else:
        raise ValueError("unknown binding mode")
    return {"inputs": torch.tensor(x), "output": torch.tensor(output),
            "target": torch.tensor(xor_oracle(cases[:, 3:5])[:, None]),
            "sources": source_nodes, "channels": source_channels, "cases": cases}


def make_cases(triples):
    return np.array([list(triple) + bits.tolist() for triple in triples for bits in PATTERNS], dtype=np.int64)


def select_common_pool(contexts, cfg):
    """Freeze logical triples only when strict local/remote conditions hold in both."""
    count = len(next(iter(contexts.values()))["ports"].indices)
    candidates = {}
    for destination in range(count):
        local, remote = [], []
        for source in range(count):
            if source == destination:
                continue
            hs, physical = [], []
            for c in contexts.values():
                p, g = c["ports"], c["geometry"]
                s, d = p.indices[source], p.indices[destination]
                hs.append(c["hops"][s, d])
                physical.append(np.linalg.norm(minimum_image_displacements(g.points[s], g.points[d], g.L)))
            if all(cfg["local_hops"][0] <= h <= cfg["local_hops"][1] for h in hs):
                local.append(source)
            if all(d >= cfg["remote_minimum_physical_distance"] for d in physical):
                remote.append(source)
        if len(local) >= 2 and len(remote) >= 2:
            candidates[destination] = {"local": local, "remote": remote}
    if len(candidates) < cfg["common_destinations"]:
        return {"status": "DIAGNOSTIC_UNAVAILABLE", "admissible_destination_count": len(candidates),
                "required": cfg["common_destinations"], "candidate_sources": candidates,
                "reason": "strict common 1-2 hop pool has fewer than 16 destinations"}
    rng = np.random.default_rng(np.random.SeedSequence([cfg["master_seed"], cfg["pool_selection_key"]]))
    selected = rng.choice(sorted(candidates), cfg["common_destinations"], replace=False).tolist()
    roles = np.random.default_rng(np.random.SeedSequence([cfg["master_seed"], cfg["role_selection_key"]]))
    triples = {mode: [[d, *roles.choice(candidates[d][mode], 2, replace=False).tolist()] for d in selected]
               for mode in ("local", "remote")}
    return {"status": "AVAILABLE", "admissible_destination_count": len(candidates),
            "candidate_sources": candidates, "selected_destinations": selected, "triples": triples,
            "train_triples": cfg["train_triples"], "validation_triples": cfg["validation_triples"]}


def finite_gate(record, threshold=.98):
    return (record.get("status") == "COMPLETE" and record.get("finite", False)
            and record.get("final", {}).get("accuracy", 0) >= threshold)


def predictions(model, batch, context=None, steps=16):
    if context is None:
        return model(batch["inputs"])
    logits = model(batch["inputs"], context["edge_index"], context["edge_dist"],
                   context["labels"], steps=steps)
    return logits[torch.arange(len(logits)), batch["output"]]


def final_diagnostics(model, batch, context, cfg):
    """Every enumerated pattern, both exact source flips and source gradients."""
    model.eval()
    records = []
    for start in range(0, len(batch["inputs"]), 4):
        stop = min(start + 4, len(batch["inputs"]))
        x = batch["inputs"][start:stop].clone().requires_grad_(True)
        part = {"inputs": x}
        if context is not None:
            part["output"] = batch["output"][start:stop]
        logits = predictions(model, part, context, cfg["steps"])
        grad = torch.autograd.grad(logits.sum(), x)[0]
        flips = []
        for role in range(2):
            flipped = x.detach().clone()
            rows = torch.arange(len(x))
            if context is None:
                flipped[:, role] = 1 - flipped[:, role]
            else:
                source = batch["sources"][start:stop, role]
                channel = batch["channels"][start:stop, role]
                flipped[rows, source, channel] = 1 - flipped[rows, source, channel]
            with torch.no_grad():
                counter = predictions(model, {**part, "inputs": flipped}, context, cfg["steps"])
            flips.append(counter.detach().numpy().reshape(-1))
        values = logits.detach().numpy().reshape(-1)
        for row in range(len(x)):
            index = start + row
            target = float(batch["target"][index, 0])
            if context is None:
                source_gradient = grad[row].detach().numpy().tolist()
                case, hops = PATTERNS[index].tolist(), [0, 0]
            else:
                source_gradient = [float(grad[row, batch["sources"][index, r], batch["channels"][index, r]]) for r in range(2)]
                case = batch["cases"][index].tolist()
                hops = [float(context["hops"][source, int(batch["output"][index])]) for source in batch["sources"][index]]
            records.append({"case": case, "target": target, "logit": float(values[row]),
                            "prediction": int(values[row] >= 0), "hops": hops,
                            "source_gradients": source_gradient,
                            "source_flipped_logits": [float(f[row]) for f in flips],
                            "source_flip_abs_logit_changes": [float(abs(f[row] - values[row])) for f in flips],
                            "source_flip_correct_predictions": [bool((f[row] >= 0) == (1 - target)) for f in flips],
                            "source_flip_class_changes": [bool((f[row] >= 0) != (values[row] >= 0)) for f in flips]})
    logits = torch.tensor([r["logit"] for r in records])[:, None]
    loss = float(nn.functional.binary_cross_entropy_with_logits(logits, batch["target"]))
    accuracy = float(np.mean([r["prediction"] == r["target"] for r in records]))
    gradients = np.array([r["source_gradients"] for r in records])
    finite = bool(np.isfinite(logits.numpy()).all() and np.isfinite(gradients).all() and np.isfinite(loss))
    return {"accuracy": accuracy, "loss": loss, "finite": finite,
            "source_gradient_abs_median": float(np.median(abs(gradients))),
            "flip_correct_prediction_fraction": float(np.mean([r["source_flip_correct_predictions"] for r in records])),
            "flip_class_change_fraction": float(np.mean([r["source_flip_class_changes"] for r in records])),
            "cases": records}


def run_one(name, seed, train_batch, validation_batch, cfg, directory, deadline, context=None):
    if time.perf_counter() >= deadline:
        return {"name": name, "training_seed": seed, "status": "NOT_RUN", "reason": "wall budget exhausted"}
    if context is None:
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed)
            model = nn.Sequential(nn.Linear(2, 32), nn.SiLU(), nn.Linear(32, 1))
    else:
        model = LARPModel("G", 1, seed=seed)
    initial = state_hash(model)
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg["lr"], betas=tuple(cfg["betas"]),
                                  eps=cfg["eps"], weight_decay=cfg["weight_decay"])
    criterion = nn.BCEWithLogitsLoss()
    rng = np.random.default_rng(np.random.SeedSequence([cfg["master_seed"], seed, cfg["minibatch_order_key"]]))
    order = rng.permutation(len(train_batch["inputs"]))
    cursor, completed, curves, elapsed_updates = 0, 0, [], []
    status = "COMPLETE"
    start = time.perf_counter()
    process = psutil.Process()
    peak = process.memory_info().rss
    for update in range(cfg["updates"]):
        if time.perf_counter() >= deadline:
            status = "RESOURCE_LIMIT"
            break
        if len(train_batch["inputs"]) == 4:
            chosen = np.arange(4)
        else:
            if cursor == len(order):
                order, cursor = rng.permutation(len(order)), 0
            chosen = order[cursor:cursor + cfg["batch_size"]]
            cursor += len(chosen)
        batch = {"inputs": train_batch["inputs"][chosen], "target": train_batch["target"][chosen]}
        if context is not None:
            batch["output"] = train_batch["output"][chosen]
        begin = time.perf_counter()
        optimizer.zero_grad(set_to_none=True)
        logits = predictions(model, batch, context, cfg["steps"])
        loss = criterion(logits, batch["target"])
        if not torch.isfinite(loss):
            status = "NUMERICAL_FAILURE_UNVERIFIED"
            break
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg["gradient_clip"])
        if not torch.isfinite(norm):
            status = "NUMERICAL_FAILURE_UNVERIFIED"
            break
        optimizer.step()
        elapsed_updates.append(time.perf_counter() - begin)
        peak = max(peak, process.memory_info().rss)
        completed += 1
        if completed % 25 == 0 or completed == 1:
            curves.append({"update": completed, "optimization_loss": float(loss.detach()),
                           "preclip_parameter_gradient_norm": float(norm)})
    # Reserve no hidden evaluation budget extension: these small diagnostics are
    # observed only if time remains; never finish an expired run under COMPLETE.
    result = {"name": name, "training_seed": seed, "status": status, "initial_state_hash": initial,
              "final_state_hash": state_hash(model), "updates_completed": completed,
              "seconds": time.perf_counter() - start, "RSS_peak_bytes_sampled": peak,
              "update_seconds_median": float(np.median(elapsed_updates)) if elapsed_updates else None,
              "optimization_curve": curves, "finite": False}
    if time.perf_counter() < deadline:
        result["train_final"] = final_diagnostics(model, train_batch, context, cfg)
        result["final"] = final_diagnostics(model, validation_batch, context, cfg)
        result["finite"] = bool(result["final"]["finite"] and result["train_final"]["finite"]
                                 and all(torch.isfinite(p).all() for p in model.parameters()))
        if time.perf_counter() >= deadline:
            result["status"] = "RESOURCE_LIMIT"
    else:
        result["status"] = "RESOURCE_LIMIT"
    result["seconds_including_final_diagnostics"] = time.perf_counter() - start
    result["RSS_peak_bytes_sampled"] = max(peak, process.memory_info().rss)
    target = directory / name
    target.mkdir(parents=True, exist_ok=False)
    torch.save(model.state_dict(), target / "final_state.pt")
    result["final_state_file_sha256"] = file_hash(target / "final_state.pt")
    write_json(target / "results.json", result)
    print(name, result["status"], completed, result.get("final", {}).get("accuracy"), flush=True)
    return result


def main(argv=None):
    series_begin = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "learning_diagnostics" / "v1")
    args = parser.parse_args(argv)
    cfg = json.loads((ROOT / "configs" / "learning_diagnostics_v1.json").read_text(encoding="utf-8"))
    torch.set_num_threads(cfg["cpu_threads"])
    torch.use_deterministic_algorithms(True)
    args.output.mkdir(parents=True, exist_ok=False)  # no result overwrites/retries
    contexts = {kind: graph_context(Geometry.load(ROOT / "artifacts" / "geometry" / f"{kind}_N400_g1101.npz"))
                for kind in cfg["geometries"]}
    if any(c["geometry"].N != cfg["N"] or c["geometry"].L != cfg["L"] for c in contexts.values()):
        raise ValueError("diagnostic geometry differs from frozen N/L")
    pool = select_common_pool(contexts, cfg)
    identity = explicit_identity()
    manifest = {"protocol": cfg, "protocol_hash": digest(cfg), "identity": identity,
                "frozen_UTC": utc_now(), "pool": pool,
                "geometries": {kind: {"coordinates_hash": array_hash(c["geometry"].points),
                                      "labels_hash": array_hash(c["geometry"].labels),
                                      "edges_hash": c["edges_hash"], "ports": c["ports"].report()}
                               for kind, c in contexts.items()},
                "stage": "technical_diagnostic", "architecture_evidence": False,
                "priors_updated": False, "test_opened": False}
    write_json(args.output / "preregistration.json", manifest)
    # Freeze the complete protocol and byte identity before any optimizer exists.
    (args.output / "protocol_frozen.md").write_text(
        "# Frozen technical diagnostic\n\n" +
        "Control order: centralized MLP → original G with both bits at receiver → local/remote interfaces. " +
        "Every seed and substrate must pass finite final accuracy ≥0.98 before the next gate. " +
        "Only final update250 counts; no LR sweep, retries, test, pilot override or architecture priors. " +
        "If fewer than16 common strict1–2 hop destinations exist, the distance diagnostic is unavailable. " +
        "The total optimization/measurement wall limit is300 seconds; an expired run is incomplete.\n\n" +
        f"Identity: {identity['hash']}\nProtocol: {manifest['protocol_hash']}\n", encoding="utf-8")
    deadline = series_begin + cfg["wall_budget_seconds"]
    records = []
    centralized = {"inputs": torch.tensor(PATTERNS), "target": torch.tensor(xor_oracle(PATTERNS)[:, None])}
    for seed in cfg["training_seeds"]:
        records.append(run_one(f"centralized_s{seed}", seed, centralized, centralized, cfg, args.output, deadline))
    central_pass = all(finite_gate(r, cfg["gate_accuracy"]) for r in records)
    direct_records = []
    for kind, context in contexts.items():
        cases = make_cases([[cfg["direct_local_destination"], -1, -1]])
        batch = bind_cases(context, cases, "direct_local")
        for seed in cfg["training_seeds"]:
            name = f"direct_local_{kind}_s{seed}"
            r = (run_one(name, seed, batch, batch, cfg, args.output, deadline, context) if central_pass else
                 {"name": name, "training_seed": seed, "status": "NOT_RUN", "reason": "centralized gate failed or incomplete"})
            records.append(r)
            direct_records.append(r)
    direct_pass = central_pass and all(finite_gate(r, cfg["gate_accuracy"]) for r in direct_records)
    for mode in ("local", "remote"):
        for kind, context in contexts.items():
            for seed in cfg["training_seeds"]:
                name = f"{mode}_{kind}_s{seed}"
                if not direct_pass:
                    r = {"name": name, "training_seed": seed, "status": "NOT_RUN", "reason": "direct-local gate failed or incomplete"}
                elif pool["status"] != "AVAILABLE":
                    r = {"name": name, "training_seed": seed, "status": "DIAGNOSTIC_UNAVAILABLE", "reason": pool["reason"]}
                else:
                    triples = pool["triples"][mode]
                    train = bind_cases(context, make_cases(triples[:cfg["train_triples"]]), mode)
                    val = bind_cases(context, make_cases(triples[cfg["train_triples"]:]), mode)
                    r = run_one(name, seed, train, val, cfg, args.output, deadline, context)
                records.append(r)
    assert explicit_identity()["hash"] == identity["hash"], "frozen dependencies changed during execution"
    report = {"status": "COMPLETE" if all(r["status"] != "RESOURCE_LIMIT" for r in records) else "RESOURCE_LIMIT",
              "stage": "technical_diagnostic", "architecture_evidence": False, "test_opened": False,
              "priors_updated": False, "pilot_gate_unchanged": True, "identity": identity,
              "centralized_gate": central_pass, "direct_local_gate": direct_pass,
              "strict_distance_pool_status": pool["status"], "records": records,
              "seconds_actual": time.perf_counter() - series_begin, "completed_UTC": utc_now()}
    write_json(args.output / "results.json", report)
    print("centralized_gate", central_pass, "direct_local_gate", direct_pass, "pool", pool["status"], flush=True)
    return report


if __name__ == "__main__":
    main()
