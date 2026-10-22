"""Training/evaluation with auditable pairing and resumable exact data order."""
from __future__ import annotations
from pathlib import Path
import os
import time
import numpy as np
import psutil
import torch
from torch import nn
from .model import LARPModel
from .data import generate_task, evaluate_task, register_ports, resource_ports
from .geometry import Geometry, minimum_image
from .config import ROOT, dataset_seed, optimizer_settings
from .artifacts import array_hash, digest, write_json, append_event, code_identity, utc_now, hardware
from .robustness import evaluate_damaged_predictions


def initialize_runtime(device="cpu"):
    torch.set_num_threads(4)
    torch.use_deterministic_algorithms(True)
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise ValueError("CUDA requested but unavailable; CPU remains supported")


def model_hash(model):
    return digest({name: array_hash(value.detach().cpu().numpy()) for name, value in model.state_dict().items()})


def edge_distances(points, edge_index, L):
    return np.linalg.norm(minimum_image(points[edge_index[0]] - points[edge_index[1]], L), axis=1)


def datasets_for(config, include_test=False):
    task, stage = config["task"], config["stage"]
    result = {}
    for split in ("train", "validation", "test"):
        if split == "test" and not include_test:
            continue
        size = config["validation_size" if split == "validation" else split + "_size"]
        result[split] = generate_task(task, size, dataset_seed(task, stage, split),
                                      world_side=config.get("world_side", 10),
                                      L=config.get("L", 20.0), split=split,
                                      fill_iterations=config.get("fill_iterations", 8))
    return result


def data_hashes(config):
    # A manifest may hash test world bytes before use; no model sees its labels.
    # This separate reproducible generator never returns scores to HPO.
    return {"data_" + split: dataset.digest for split, dataset in datasets_for(config, True).items()}


def select_ports(logits, nodes):
    rows = torch.arange(logits.shape[0], device=logits.device).unsqueeze(1)
    return logits[rows, nodes]


def graph_tensors(geometry, edge_index, device):
    return (torch.as_tensor(np.array(edge_index, copy=True), dtype=torch.long, device=device),
            torch.as_tensor(edge_distances(geometry.points, edge_index, geometry.L), dtype=torch.float32, device=device),
            torch.as_tensor(np.array(geometry.labels, copy=True), dtype=torch.long, device=device))


@torch.no_grad()
def evaluate(model, dataset, geometry, ports, tensors, batch_size=4, device="cpu",
             indexes=None, alive=None, edge_alive=None, collapse_lambda=0.0,
             steps=16, train_target_variance=None, input_ports=None, output_ports=None):
    model.eval()
    indices = np.arange(len(dataset)) if indexes is None else np.asarray(indexes, dtype=np.int64).reshape(-1)
    if not len(indices) or batch_size < 1:
        raise ValueError("evaluation requires a nonempty selection and positive batch size")
    # Two-dimensional masks are aligned with the selected example order, never
    # guessed as full-dataset masks. This remains explicit when indexes is sparse.
    def aligned_masks(value, width, name):
        if value is None:
            return None
        array = value.detach().cpu().numpy() if isinstance(value, torch.Tensor) else np.asarray(value)
        if array.ndim == 1 and array.shape == (width,):
            return array.astype(bool, copy=False)
        if array.ndim == 2 and array.shape == (len(indices), width):
            return array.astype(bool, copy=False)
        raise ValueError(f"{name} must be [{width}] or [selected_examples,{width}], aligned with indexes")
    alive_array = aligned_masks(alive, geometry.N, "alive")
    arcs_array = aligned_masks(edge_alive, tensors[0].shape[1], "edge_alive")
    outputs, targets, free, probability = [], [], [], []
    masks, output_nodes, required_sources = [], [], []
    start = time.perf_counter()
    for first in range(0, len(indices), batch_size):
        selected = indices[first:first + batch_size]
        batch = dataset.batch(selected, geometry.points, ports, device=device,
                              labels=geometry.labels, input_ports=input_ports, output_ports=output_ports)
        mask = None if alive_array is None else torch.as_tensor(alive_array[first:first + len(selected)] if alive_array.ndim == 2 else alive_array, device=device)
        arcs = None if arcs_array is None else torch.as_tensor(arcs_array[first:first + len(selected)] if arcs_array.ndim == 2 else arcs_array, device=device)
        logits = model(batch["inputs"], *tensors[:2], tensors[2], steps=steps,
                       alive=mask, edge_alive=arcs, collapse_lambda=collapse_lambda)
        values = select_ports(logits, batch["output_nodes"])
        outputs.append(values.cpu().numpy())
        targets.append(batch["target"].cpu().numpy())
        if mask is not None:
            mask = mask.expand(len(selected), geometry.N)
            masks.append(mask.cpu().numpy())
            output_nodes.append(batch["output_nodes"].cpu().numpy())
            if dataset.task in {"xor", "copy", "fill"}:
                essential = batch["selected_source_nodes"] if dataset.task == "copy" else batch["source_nodes"]
                required_sources.append(essential.reshape(len(selected), -1).cpu().numpy())
        if dataset.task == "fill":
            free.append(batch["free"].cpu().numpy())
            probability.append(batch["p"].cpu().numpy())
    prediction = np.concatenate(outputs)
    truth = np.concatenate(targets)
    free_array = np.concatenate(free) if free else None
    p_array = np.concatenate(probability) if probability else None
    if masks and dataset.task != "resource":
        result = evaluate_damaged_predictions(dataset.task, prediction, truth,
                    np.concatenate(masks), np.concatenate(output_nodes),
                    np.concatenate(required_sources), free=free_array, p=p_array)
    else:
        # Protected resource queries retain a well-defined NMSE. The protocol has
        # no missing-query NMSE penalty; do not manufacture one by assigning zero.
        if masks:
            all_masks, all_nodes = np.concatenate(masks), np.concatenate(output_nodes)
            if not np.all(all_masks[np.arange(len(indices))[:, None], all_nodes]):
                raise ValueError("SCIENTIFIC_BLOCKER_resource_end_to_end_failure_score_not_preregistered")
        result = evaluate_task(dataset.task, prediction, truth, free=free_array,
                               p=p_array, train_target_variance=train_target_variance)
    result["evaluation_seconds"] = time.perf_counter() - start
    return result


def _save_checkpoint(path, model, optimizer, order, cursor, rng, completed, config, history, elapsed, tracking):
    state = {"model": model.state_dict(), "optimizer": optimizer.state_dict(),
             "order": order, "cursor": cursor, "rng": rng.bit_generator.state,
             "completed_updates": completed, "config": config, "history": history,
             "elapsed_training_seconds": elapsed, "tracking": tracking}
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    torch.save(state, temporary)
    os.replace(temporary, path)


def train_run(config, geometry: Geometry, edge_index, run_dir, *, device="cpu",
              resume=False, open_test=False, validation_interval=100,
              max_seconds=1800.0, preregistered=False, stop_after_update=None):
    config = dict(config)
    if open_test and (config["stage"] not in {"pilot", "confirmation"} or not preregistered):
        raise ValueError("Test opens only after frozen pilot/confirmation, not HPO/smoke")
    initialize_runtime(device)
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    task, variant = config["task"], config["variant"]
    output_dim = 8 if task == "copy" else 1
    model = LARPModel(variant, output_dim, 29 if task == "resource" else 25,
                      config["training_seed"]).to(device)
    assert model.parameter_count == model.expected_parameter_count
    initial_hash = model_hash(model)
    settings = optimizer_settings(config["lr"])
    optimizer = torch.optim.AdamW(model.parameters(), lr=settings["lr"],
                                  betas=tuple(settings["betas"]), eps=settings["eps"],
                                  weight_decay=settings["weight_decay"])
    sets = datasets_for(config)
    ports = resource_ports(geometry.points, geometry.L) if task == "resource" else register_ports(geometry.points, geometry.L, config.get("world_side", 10))
    tensors = graph_tensors(geometry, edge_index, device)
    pos_weight = sets["train"].positive_weight
    criterion = nn.MSELoss() if task == "resource" else nn.BCEWithLogitsLoss(
        pos_weight=None if pos_weight is None else torch.tensor([pos_weight], device=device))
    target_variance = sets["train"].train_target_variance if task == "resource" else None
    pair_hashes = {"coordinates": array_hash(geometry.points), "edges": array_hash(edge_index),
                   "ports": ports.digest, **data_hashes(config), "optimizer": digest(settings),
                   "budget": digest({"updates": config["updates"], "batch_size": config["batch_size"],
                                      "steps": config["steps"]}), "shared_initialization": initial_hash}
    identity = code_identity(ROOT)
    manifest = {"experiment_id": run_dir.name, "created_UTC": utc_now(),
                "config": config, "config_hash": digest(config), "pair_hashes": pair_hashes,
                "labels_hash": array_hash(geometry.labels), "code": identity,
                "ports": ports.report(), "hardware": hardware(), "device": device,
                "parameters": model.parameter_count, "active_edges": int(edge_index.shape[1]),
                "adapter_MAC_per_node": model.adapter_mac_per_node,
                "train_target_variance_frozen": target_variance,
                "preregistered": bool(preregistered), "test_opened": False}
    manifest_path = run_dir / "manifest.json"
    if manifest_path.exists():
        import json
        old = json.loads(manifest_path.read_text(encoding="utf-8"))
        if old["config_hash"] != manifest["config_hash"] or old["pair_hashes"] != pair_hashes or old["code"]["source_hash"] != identity["source_hash"]:
            raise ValueError("Existing run differs; use a new code/protocol series, never overwrite evidence")
        if not resume:
            raise FileExistsError("Run already exists; resume its checkpoint explicitly")
        manifest = old
        result_path = run_dir / "results.json"
        if result_path.exists():
            prior_result = json.loads(result_path.read_text(encoding="utf-8"))
            if prior_result["status"] == "COMPLETE" and prior_result.get("test_opened"):
                return prior_result  # An opened-test endpoint is immutable/idempotent.
    else:
        write_json(manifest_path, manifest)
    sets["train"].save(run_dir / "train_world.npz")
    sets["validation"].save(run_dir / "validation_world.npz")
    rng = np.random.default_rng(np.random.SeedSequence([20261008, config["training_seed"], 8021]))
    order = rng.permutation(len(sets["train"]))
    cursor, completed, elapsed_before, history = 0, 0, 0.0, []
    tracking = {"samples_seen": 0, "times": [], "threshold_at": None, "final_loss": None,
                "peak_RSS": psutil.Process().memory_info().rss}
    checkpoint = run_dir / "checkpoints" / "last.pt"
    if resume:
        if not checkpoint.exists():
            raise FileNotFoundError("No checkpoint to resume")
        # This command accepts only locally-created checkpoints, not untrusted downloads.
        saved = torch.load(checkpoint, map_location=device, weights_only=False)
        if saved["config"] != config:
            raise ValueError("Checkpoint configuration mismatch")
        model.load_state_dict(saved["model"])
        optimizer.load_state_dict(saved["optimizer"])
        order, cursor, completed = saved["order"], saved["cursor"], saved["completed_updates"]
        rng.bit_generator.state = saved["rng"]
        history, elapsed_before = saved["history"], saved["elapsed_training_seconds"]
        tracking = saved["tracking"]
    process = psutil.Process()
    peak_RSS = max(tracking["peak_RSS"], process.memory_info().rss)
    if device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats(device)
    begin = time.perf_counter()
    status, final_loss = "COMPLETE", tracking.get("final_loss")
    times = tracking["times"]
    threshold_at = tracking["threshold_at"]
    if not checkpoint.exists():
        _save_checkpoint(checkpoint, model, optimizer, order, cursor, rng, completed,
                         config, history, elapsed_before, tracking)
    try:
        while completed < config["updates"]:
            if elapsed_before + time.perf_counter() - begin > max_seconds:
                status = "RESOURCE_LIMIT"
                break
            model.train()
            if cursor == len(order):
                order, cursor = rng.permutation(len(order)), 0
            # A final short minibatch is legal and never samples with replacement.
            selected = order[cursor:cursor + config["batch_size"]]
            cursor += len(selected)
            batch = sets["train"].batch(selected, geometry.points, ports, device=device, labels=geometry.labels)
            start = time.perf_counter()
            optimizer.zero_grad(set_to_none=True)
            logits = model(batch["inputs"], *tensors[:2], tensors[2], steps=config["steps"])
            loss = criterion(select_ports(logits, batch["output_nodes"]), batch["target"])
            if not torch.isfinite(loss):
                status, final_loss = "NUMERICAL_FAILURE_UNVERIFIED", float("inf")
                break
            loss.backward()
            gradient_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            if not torch.isfinite(gradient_norm):
                status, final_loss = "NUMERICAL_FAILURE_UNVERIFIED", float("inf")
                break
            optimizer.step()
            if device.startswith("cuda"):
                torch.cuda.synchronize(device)
            times.append(time.perf_counter() - start)
            completed += 1
            tracking["samples_seen"] += len(selected)
            final_loss = float(loss.detach().cpu())
            tracking["final_loss"] = final_loss
            peak_RSS = max(peak_RSS, process.memory_info().rss)
            if completed % validation_interval == 0 or completed == config["updates"]:
                metrics = evaluate(model, sets["validation"], geometry, ports, tensors,
                                    config["batch_size"], device, steps=config["steps"],
                                    train_target_variance=target_variance)
                point = {"update": completed, "optimization_loss": final_loss,
                         "validation_score": metrics["score"], "validation_loss": metrics["loss"]}
                history.append(point)
                append_event(run_dir / "curve.jsonl", point)
                threshold = .98 if task == "xor" else .95
                if metrics["score"] >= threshold and threshold_at is None:
                    threshold_at = completed
                if metrics.get("divergent"):
                    status, final_loss = "NUMERICAL_FAILURE_UNVERIFIED", float("inf")
                tracking.update(times=times, threshold_at=threshold_at, peak_RSS=peak_RSS)
                _save_checkpoint(checkpoint, model, optimizer, order, cursor, rng, completed,
                                 config, history, elapsed_before + time.perf_counter() - begin, tracking)
                if completed == 500 and config["updates"] > 500:
                    import shutil
                    snapshot = checkpoint.with_name("snapshot_500.pt")
                    if not snapshot.exists():
                        shutil.copy2(checkpoint, snapshot)
                        write_json(run_dir / "checkpoint_500_metrics.json", {
                            "stage":"pilot_checkpoint", "task":task, "variant":variant,
                            "condition":config["condition"], "geometry_seed":config["geometry_seed"],
                            "training_seed":config["training_seed"], "updates_completed":500,
                            "score_split":"validation", "validation":metrics,
                            "pair_hashes":{**pair_hashes,"budget":digest({"updates":500,"batch_size":config["batch_size"],"steps":config["steps"]})},
                            "labels_hash":manifest["labels_hash"],"code":identity,"test_opened":False})
                if status != "COMPLETE":
                    break
            if stop_after_update is not None and completed >= stop_after_update:
                status = "PAUSED_AT_UPDATE_BOUNDARY"
                break
    except KeyboardInterrupt:
        status = "INFRASTRUCTURE_INTERRUPTION"
        # Never save a partially-updated model/optimizer. Restore the last valid
        # boundary so the same episodes are replayed with the same RNG on resume.
        saved = torch.load(checkpoint, map_location=device, weights_only=False)
        model.load_state_dict(saved["model"])
        optimizer.load_state_dict(saved["optimizer"])
        order, cursor, completed = saved["order"], saved["cursor"], saved["completed_updates"]
        rng.bit_generator.state = saved["rng"]
        history, tracking = saved["history"], saved["tracking"]
        times, threshold_at = tracking["times"], tracking["threshold_at"]
        final_loss = tracking.get("final_loss")
    elapsed = elapsed_before + time.perf_counter() - begin
    tracking.update(times=times, threshold_at=threshold_at, peak_RSS=peak_RSS)
    _save_checkpoint(checkpoint, model, optimizer, order, cursor, rng, completed, config, history, elapsed, tracking)
    validation = ({"score": 0.0, "loss": float("inf")} if status == "NUMERICAL_FAILURE_UNVERIFIED" else
                  evaluate(model, sets["validation"], geometry, ports, tensors, config["batch_size"], device,
                           steps=config["steps"], train_target_variance=target_variance))
    result = {"experiment_id": run_dir.name, "stage": config["stage"], "task": task,
              "variant": variant, "condition": config["condition"], "geometry_seed": config["geometry_seed"],
              "training_seed": config["training_seed"], "status": status,
              "preregistered": bool(preregistered), "pair_hashes": pair_hashes,
              "labels_hash": manifest["labels_hash"], "parameters": model.parameter_count,
              "adapter_MAC_per_node": model.adapter_mac_per_node,
              "active_edges": int(edge_index.shape[1]), "updates_completed": completed,
              "updates_budget": config["updates"], "samples_seen": tracking["samples_seen"],
              "training_seconds_including_periodic_validation": elapsed,
              "optimizer_step_seconds_median": float(np.median(times)) if times else None,
              "optimizer_step_seconds_p90": float(np.percentile(times, 90)) if times else None,
              "RSS_peak_bytes_sampled": peak_RSS,
              "device_peak_bytes": torch.cuda.max_memory_allocated(device) if device.startswith("cuda") else 0,
              "steps_to_validation_threshold": threshold_at, "threshold_check_resolution": validation_interval,
              "final_optimization_loss": final_loss, "validation": validation,
              "score": validation["score"], "loss": validation["loss"], "score_split": "validation",
              "test_opened": False, "code": identity, "completed_UTC": utc_now()}
    if validation.get("divergent"):
        result.update(status="NUMERICAL_FAILURE_UNVERIFIED", score=0.0, loss=float("inf"))
    if open_test and result["status"] == "COMPLETE":
        test = datasets_for(config, True)["test"]
        test.save(run_dir / "test_world.npz")
        metrics = evaluate(model, test, geometry, ports, tensors, config["batch_size"], device,
                           steps=config["steps"], train_target_variance=target_variance)
        result.update(test=metrics, score=metrics["score"], loss=metrics["loss"], score_split="test", test_opened=True)
        if metrics.get("divergent"):
            result.update(status="NUMERICAL_FAILURE_UNVERIFIED", score=0.0, loss=float("inf"))
        manifest["test_opened"] = True
        write_json(manifest_path, manifest)
    write_json(run_dir / "results.json", result)
    return result


def load_trained_run(run_dir, device="cpu", checkpoint_name="last.pt"):
    import json
    run_dir = Path(run_dir)
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    saved = torch.load(run_dir / "checkpoints" / checkpoint_name, map_location=device, weights_only=False)
    cfg = saved["config"]
    model = LARPModel(cfg["variant"], 8 if cfg["task"] == "copy" else 1,
                      29 if cfg["task"] == "resource" else 25, cfg["training_seed"]).to(device)
    model.load_state_dict(saved["model"])
    return model, cfg, manifest
