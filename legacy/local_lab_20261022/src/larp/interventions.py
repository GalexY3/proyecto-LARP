"""Invocable frozen-checkpoint diagnostics; no fitting and no automatic suite.

Only completed, preregistered pilot/confirmation runs whose test was already
opened can enter this module. Plans and per-condition records are resumable.
Technical-test overrides require an explicitly marked synthetic test bundle and
produce artifacts with scientific_evidence=False.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import torch
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

from .artifacts import array_hash, code_identity, digest, file_hash, utc_now, write_json
from .config import ROOT, load_profile
from .data import (TaskDataset, generate_task, register_ports, resource_ports,
                   minimum_image_displacements, fill_trivial_predictions, evaluate_task)
from .geometry import Geometry, MASTER_SEED
from .graphs import build_graph, validate_edge_index
from .robustness import (build_node_mask, build_batch_masks, build_edge_mask,
                         fixed_test_indices, normalized_damage_auc,
                         preregistered_centers, relocated_ports)
from .training import (evaluate, graph_tensors, initialize_runtime, load_trained_run,
                       model_hash)


KINDS = ("random", "lesion", "radius", "type", "edge", "relocation", "m1", "functions")


def _seed(*keys):
    return int(np.random.SeedSequence([MASTER_SEED, *map(int, keys)]).generate_state(1)[0])


def _load_bundle(run_dir, device="cpu", test_only=False):
    run_dir = Path(run_dir)
    model, cfg, manifest = load_trained_run(run_dir, device)
    result = json.loads((run_dir / "results.json").read_text(encoding="utf-8"))
    if cfg["stage"] not in {"pilot", "confirmation"} or not manifest.get("preregistered"):
        raise RuntimeError("Frozen interventions require preregistered pilot/confirmation")
    if cfg.get("condition") == "matched" and not test_only:
        raise RuntimeError("SCIENTIFIC_BLOCKER C3 matched pair population is unresolved")
    if result.get("status") != "COMPLETE" or not result.get("test_opened") or not manifest.get("test_opened"):
        raise RuntimeError("Frozen interventions require COMPLETE run with already-open test")
    if bool(cfg.get("technical_test_only", False)) != bool(test_only):
        raise RuntimeError("Technical overrides require a marked technical_test_only bundle")
    if cfg != manifest["config"] or manifest["code"]["source_hash"] != code_identity(ROOT)["source_hash"]:
        raise RuntimeError("Frozen run configuration/code identity differs from current implementation")
    saved = torch.load(run_dir / "checkpoints" / "last.pt", map_location=device, weights_only=False)
    if saved["completed_updates"] != cfg["updates"]:
        raise RuntimeError("Frozen checkpoint did not complete its preregistered budget")
    geometry = Geometry.load(run_dir / "geometry.npz")
    edges = np.load(run_dir / "edges.npy", allow_pickle=False)
    validate_edge_index(edges, geometry.N)
    dataset = TaskDataset.load(run_dir / "test_world.npz")
    ports = resource_ports(geometry.points, geometry.L) if cfg["task"] == "resource" else register_ports(
        geometry.points, geometry.L, cfg.get("world_side", 10))
    hashes = manifest["pair_hashes"]
    if (array_hash(geometry.points) != hashes["coordinates"] or array_hash(edges) != hashes["edges"]
            or ports.digest != hashes["ports"] or dataset.digest != hashes["data_test"]
            or array_hash(geometry.labels) != manifest["labels_hash"]):
        raise RuntimeError("Frozen X/E/ports/world/labels artifact hash mismatch")
    if not test_only and geometry.metadata.get("kind") in {"mhu", "hu"}:
        certificate = geometry.metadata.get("native_certificate") or geometry.metadata.get("certificate", {})
        if not certificate.get("scientific_admissible"):
            raise RuntimeError("SCIENTIFIC_BLOCKER frozen substrate has no admissible geometry certificate")
    initialize_runtime(device)
    snapshot = {"run_dir": str(run_dir.resolve()), "manifest_hash": file_hash(run_dir / "manifest.json"),
                "checkpoint_hash": file_hash(run_dir / "checkpoints" / "last.pt"),
                "model_hash": model_hash(model), "pair_hashes": hashes,
                "labels_hash": manifest["labels_hash"], "code": manifest["code"]}
    return model, cfg, manifest, geometry, edges, dataset, ports, snapshot


def _settings(test_only, limits):
    p = load_profile("robustness")
    limits = limits or {}
    if limits and not test_only:
        raise ValueError("Reduced intervention budgets require explicit technical test mode")
    if set(limits) - {"examples", "random_masks", "lesion_centers", "steps", "function_permutations"}:
        raise ValueError("unknown technical limit")
    effective = {"examples": p["test_examples"], "random_masks": p["random_masks"],
                 "lesion_centers": p["lesion_centers"], "steps": p["steps"],
                 "function_permutations": 20}
    effective.update(limits)
    if any(int(value) < 1 for value in effective.values()):
        raise ValueError("positive technical limits required")
    return p, effective


def _freeze(output, plan):
    output = Path(output)
    path = output / "preregistration.json"
    frozen = {"plan": plan, "plan_hash": digest(plan), "created_UTC": utc_now()}
    if path.exists():
        old = json.loads(path.read_text(encoding="utf-8"))
        if old["plan_hash"] != digest(old["plan"]) or old["plan_hash"] != frozen["plan_hash"]:
            raise RuntimeError("Intervention plan differs; create a new artifact series")
        return old
    write_json(path, frozen)
    return frozen


def _specifications(kind, p, effective, geometry, model):
    specs = []
    if kind in {"random", "lesion"}:
        repeat = effective["random_masks"] if kind == "random" else effective["lesion_centers"]
        for protection in (True, False):
            for level, q in enumerate(p["node_fractions"]):
                for rep in range(repeat):
                    specs.append({"id": f"{kind}_protect{int(protection)}_q{q:g}_r{rep}",
                                  "mode": kind, "q": q, "level": level, "rep": rep,
                                  "protect_ports": protection, "seed": _seed(8101, level, rep)})
    elif kind == "radius":
        for level, radius in enumerate(p["lesion_radii"]):
            for rep in range(effective["lesion_centers"]):
                specs.append({"id": f"radius_R{radius:g}_r{rep}", "mode": "radius", "radius": radius,
                              "rep": rep, "protect_ports": True, "seed": _seed(8102, level, rep)})
    elif kind == "type":
        multiplier = 4 if geometry.N == 1600 else 1
        for type_id in range(5):
            levels = [("absolute", int(n)*multiplier) for n in p["subtype_absolute"]]
            levels += [("fraction", value) for value in p["subtype_fractions"]]
            for level, (amount_kind, amount) in enumerate(levels):
                for rep in range(effective["random_masks"]):
                    for control in (False, True):
                        specs.append({"id": f"type{type_id}_{amount_kind}{amount:g}_r{rep}_control{int(control)}",
                                      "mode": "type", "type_id": type_id, "amount_kind": amount_kind,
                                      "amount": amount, "random_control": control, "rep": rep,
                                      "protect_ports": True, "seed": _seed(8103, type_id, level, rep)})
    elif kind == "edge":
        modes = ["independent_arcs"]
        specs = [{"id": f"edge_{mode}_q{q:g}_r{rep}", "mode": "edge", "edge_mode": mode,
                  "q": q, "rep": rep, "protect_ports": True, "seed": _seed(8104, level, rep)}
                 for mode in modes for level, q in enumerate(p["edge_fractions"])
                 for rep in range(effective["random_masks"])]
    elif kind == "relocation":
        specs = [{"id": f"relocation_{rep}", "mode": "relocation", "offset": offset,
                  "rep": rep, "protect_ports": True}
                 for rep, offset in enumerate([[0, 0], *p["relocations"]])]
    elif kind == "m1":
        if model.variant == "G":
            raise ValueError("M1 complete type-function collapse only applies to T/F")
        specs = [{"id": f"m1_lambda{value:g}", "mode": "m1", "collapse_lambda": value,
                  "protect_ports": True} for value in (0.0, 0.5, 1.0)]
    elif kind == "functions":
        if model.variant == "G":
            raise ValueError("Functional relocation only applies to T/F")
        specs = [{"id": "functions_native", "mode": "functions", "assignment": "native", "protect_ports": True},
                 {"id": "functions_global_rename", "mode": "functions", "assignment": "global_rename", "protect_ports": True}]
        specs.extend({"id": f"functions_permutation{rep}", "mode": "functions", "assignment": "permutation",
                      "rep": rep, "seed": _seed(geometry.metadata.get("geometry_seed", 0), 7201, rep),
                      "protect_ports": True} for rep in range(effective["function_permutations"]))
    else:
        raise ValueError(f"kind must be one of {KINDS}")
    return specs


def _diagnostics(geometry, edges, labels, masks, output_nodes, required_sources, steps,
                 edge_alive=None):
    """Actual damaged graphs; spatial windows at all original node coordinates.

    Hop coverage is measured at actual output nodes, with directed ancestors and
    duplicate-free BFS. SCC excludes removed isolated vertices. These diagnostics
    are averaged within the mask/example ensemble, never architecture replicates.
    """
    labels = np.asarray(labels, dtype=np.int64)
    masks = np.asarray(masks, dtype=bool)
    b, n = masks.shape
    displacement = minimum_image_displacements(geometry.points[:, None], geometry.points[None], geometry.L)
    distance = np.linalg.norm(displacement, axis=-1)
    spatial = {}
    for radius in (4, 5):
        neighborhood = (distance <= radius).astype(np.float32)
        empty, average = [], []
        for c in range(5):
            counts = (masks & (labels[None] == c)).astype(np.float32) @ neighborhood.T
            empty.append(float(np.mean(counts == 0)))
            average.append(float(np.mean(counts)))
        spatial[str(radius)] = {"empty_fraction_by_type": empty, "mean_count_by_type": average}
    hop_empty = {4: [], 8: []}
    hop_mean = {4: [], 8: []}
    scc_counts, accessibility, removed_counts = [], [], []
    topology_cache = {}
    arc_selection = np.ones(edges.shape[1], dtype=bool) if edge_alive is None else np.asarray(edge_alive, bool)
    for row in range(b):
        live = masks[row]
        arc_live = live[edges[0]] & live[edges[1]] & arc_selection
        key = array_hash(arc_live)
        if key not in topology_cache:
            adjacency = csr_matrix((np.ones(int(arc_live.sum()), dtype=bool),
                                    (edges[0, arc_live], edges[1, arc_live])), shape=(n, n))
            _, components = connected_components(adjacency, directed=True, connection="strong")
            topology_cache[key] = (adjacency, components)
        adjacency, components = topology_cache[key]
        scc_counts.append(len(np.unique(components[live])))
        destinations = output_nodes[row]
        reached = np.zeros((len(destinations), n), bool)
        reached[np.arange(len(destinations)), destinations] = live[destinations]
        frontier = reached.copy()
        for hop in range(1, max(8, steps) + 1):
            frontier = (frontier @ adjacency.T) & ~reached
            reached |= frontier
            if hop in hop_empty:
                counts = np.stack([reached[:, labels == c].sum(axis=1) for c in range(5)], axis=-1)
                output_live = live[destinations]
                hop_empty[hop].append((counts[output_live] == 0).mean(0) if output_live.any() else np.full(5, np.nan))
                hop_mean[hop].append(counts[output_live].mean(0) if output_live.any() else np.full(5, np.nan))
            if hop == steps:
                source_ids = required_sources[row] if required_sources is not None else []
                accessibility.append(float(reached[:, source_ids].mean()) if len(source_ids) else None)
        removed_counts.append(np.bincount(labels[~live], minlength=5))
    return {"spatial_window_center_definition": "all_original_substrate_nodes_including_removed_centers",
            "spatial_coverage_R4_R5": spatial,
            "hop_center_definition": "actual_surviving_output_nodes; directed_incoming_ancestors_including_self",
            "hop_coverage": {str(h): {"empty_fraction_by_type": np.nanmean(hop_empty[h], axis=0).tolist(),
                                      "mean_count_by_type": np.nanmean(hop_mean[h], axis=0).tolist()}
                             for h in (4, 8)},
            "SCC_count_alive_mean": float(np.mean(scc_counts)),
            "SCC_count_alive_min_max": [int(min(scc_counts)), int(max(scc_counts))],
            "required_source_output_pair_accessibility_fraction_at_T":
                float(np.mean([x for x in accessibility if x is not None])) if any(x is not None for x in accessibility) else None,
            "removed_by_type_mean": np.mean(removed_counts, axis=0).tolist(),
            "removed_count_min_max": [int((~masks).sum(1).min()), int((~masks).sum(1).max())],
            "examples_are_architecture_replicates": False}


def run_robustness(run_dir, output, kind="random", dry_run=True, *, device="cpu",
                   max_seconds=1800, test_only=False, test_limits=None, protect_ports=None):
    model, cfg, manifest, geometry, edges, dataset, ports, snapshot = _load_bundle(run_dir, device, test_only)
    if protect_ports not in {None, True, False}:
        raise ValueError("protect_ports must be None (both), True or False")
    if protect_ports is False and kind not in {"random", "lesion"}:
        raise ValueError("Unprotected repeat is preregistered only for random/localized node removal")
    if cfg["task"] == "resource" and (kind == "relocation" or
            (kind in {"random", "lesion"} and protect_ports is not True)):
        raise RuntimeError("SCIENTIFIC_BLOCKER resource end-to-end/relocation protocol not preregistered")
    p, effective = _settings(test_only, test_limits)
    indices = fixed_test_indices(len(dataset), int(effective["examples"]))
    specs = _specifications(kind, p, effective, geometry, model)
    if kind in {"random", "lesion"} and protect_ports is not None:
        specs = [item for item in specs if item["protect_ports"] == protect_ports]
    if kind == "edge":
        arcs = set(map(tuple, edges.T.tolist()))
        if all((target, source) in arcs for source, target in arcs):
            specs.extend(dict(item, id=item["id"].replace("independent_arcs", "paired_undirected_edges"),
                              edge_mode="paired_undirected_edges") for item in list(specs))
    centers = preregistered_centers(geometry.L, seed=_seed(8105), count=int(effective["lesion_centers"]))
    plan = {"kind": kind, "snapshot": snapshot, "settings": effective, "profile": p,
            "protection_selection": protect_ports,
            "test_indices": indices.tolist(), "centers": centers.tolist(), "conditions": specs,
            "scientific_evidence": not test_only, "priors_updated": False,
            "conditional_blocks": ["C3 matched", "partial_port_relocation", "resource_end_to_end"],
            "replication_unit": "geometry; examples/masks/centers are aggregated within geometry"}
    frozen = _freeze(output, plan)
    output = Path(output)
    if dry_run:
        status = {"status": "NOT_RUN", "plan_hash": frozen["plan_hash"], "conditions": len(specs),
                  "dry_run": True, "scientific_evidence": not test_only}
        write_json(output / "status.json", status)
        return status
    tensors = graph_tensors(geometry, edges, device)
    baseline_batch = dataset.batch(indices, geometry.points, ports, labels=geometry.labels)
    sources = (baseline_batch["selected_source_nodes"] if dataset.task == "copy" else baseline_batch.get("source_nodes"))
    source_array = None if sources is None else sources.numpy().reshape(len(indices), -1)
    active = baseline_batch["active_nodes"].numpy()
    output_nodes = baseline_batch["output_nodes"].numpy()
    start, records = time.perf_counter(), []
    evaluated_cache = {}
    for spec in specs:
        record_path = output / "records" / (spec["id"] + ".json")
        if record_path.exists():
            saved = json.loads(record_path.read_text(encoding="utf-8"))
            if saved["plan_hash"] != frozen["plan_hash"]:
                raise RuntimeError("Saved intervention record belongs to another plan")
            records.append(saved)
            continue
        if time.perf_counter() - start >= max_seconds:
            status = {"status": "RESOURCE_LIMIT", "completed_conditions": len(records), "conditions": len(specs),
                      "seconds_actual": time.perf_counter() - start, "resume": "repeat identical invocation"}
            write_json(output / "status.json", status)
            return status
        live = np.ones((len(indices), geometry.N), bool)
        arc_live, mask_metadata, evaluation_ports = None, [], ports
        local_tensors, local_model = tensors, model
        mode = spec["mode"]
        if mode in {"random", "lesion", "radius"}:
            args = {"mode": {"random": "random", "lesion": "localized", "radius": "disk"}[mode],
                    "q": spec.get("q", 0), "seed": spec["seed"], "L": geometry.L,
                    "labels": geometry.labels}
            if mode != "random":
                args["center"] = centers[spec["rep"]]
            if mode == "radius":
                args["radius"] = spec["radius"]
            live, mask_metadata = build_batch_masks(geometry.points, active,
                             protect_ports=spec["protect_ports"], **args)
        elif mode == "type":
            masks = []
            for row in range(len(indices)):
                args = {"mode": "type", "type_id": spec["type_id"], "labels": geometry.labels,
                        "seed": spec["seed"], "protected": active[row], "L": geometry.L}
                args["count" if spec["amount_kind"] == "absolute" else "fraction"] = spec["amount"]
                damaged = build_node_mask(geometry.points, **args)
                if spec["random_control"] and damaged.available:
                    damaged = build_node_mask(geometry.points, mode="random", count=damaged.metadata["requested_count"],
                                               seed=spec["seed"], protected=active[row], L=geometry.L,
                                               labels=geometry.labels)
                masks.append(damaged)
            live = np.stack([mask.alive for mask in masks])
            mask_metadata = [dict(mask.metadata, available=mask.available) for mask in masks]
        elif mode == "edge":
            damaged = build_edge_mask(edges, q=spec["q"], seed=spec["seed"], mode=spec["edge_mode"])
            arc_live = damaged.edge_alive
            mask_metadata = [dict(damaged.metadata, available=damaged.available)]
        elif mode == "relocation":
            evaluation_ports = relocated_ports(geometry.points, L=geometry.L, world_side=cfg.get("world_side", 10), offset=spec["offset"])
            batch = dataset.batch(indices, geometry.points, evaluation_ports)
            output_nodes = batch["output_nodes"].numpy()
            source = batch["selected_source_nodes"] if dataset.task == "copy" else batch.get("source_nodes")
            source_array = None if source is None else source.numpy().reshape(len(indices), -1)
        elif mode == "functions":
            assigned = geometry.labels.copy()
            if spec["assignment"] == "permutation":
                assigned = np.random.default_rng(spec["seed"]).permutation(assigned)
            elif spec["assignment"] == "global_rename":
                permutation = np.asarray([3, 0, 4, 1, 2])
                assigned = permutation[assigned]
                local_model = model.renamed_copy(permutation)
            if spec["assignment"] != "global_rename" and not np.array_equal(
                    np.bincount(assigned, minlength=5), np.bincount(geometry.labels, minlength=5)):
                raise RuntimeError("Function relocation did not conserve counts")
            local_tensors = (*tensors[:2], torch.as_tensor(assigned, device=device))
        available = all(item.get("available", True) for item in mask_metadata)
        mask_dir = output / "masks"
        mask_dir.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(mask_dir / (spec["id"] + ".npz"), alive=live,
                            edge_alive=np.ones(edges.shape[1], bool) if arc_live is None else arc_live,
                            function_labels=local_tensors[2].detach().cpu().numpy())
        key = digest({"live": array_hash(live), "arcs": None if arc_live is None else array_hash(arc_live),
                      "ports": evaluation_ports.digest, "labels": array_hash(local_tensors[2].cpu().numpy()),
                      "model": model_hash(local_model), "lambda": spec.get("collapse_lambda", 0)})
        metrics, diagnostics = None, None
        if available:
            if key in evaluated_cache:
                metrics, diagnostics = evaluated_cache[key]
            else:
                # geometry remains original: in resource/function interventions u
                # is unchanged even when the selected neural functions relocate.
                metrics = evaluate(local_model, dataset, geometry, evaluation_ports, local_tensors,
                                   cfg["batch_size"], device, indexes=indices,
                                   alive=live if mode in {"random", "lesion", "radius", "type"} else None,
                                   edge_alive=arc_live, steps=int(effective["steps"]),
                                   collapse_lambda=spec.get("collapse_lambda", 0),
                                   train_target_variance=manifest.get("train_target_variance_frozen"))
                function_labels = local_model.function_ids[local_tensors[2]].cpu().numpy()
                diagnostics = _diagnostics(geometry, edges, function_labels, live, output_nodes,
                                           source_array, int(effective["steps"]), arc_live)
                evaluated_cache[key] = (metrics, diagnostics)
        record = {"id": spec["id"], "plan_hash": frozen["plan_hash"], "condition": spec,
                  "status": "COMPLETE" if available else "UNAVAILABLE", "metrics": metrics,
                  "diagnostics": diagnostics, "mask_metadata": mask_metadata,
                  "ports": evaluation_ports.report(), "weights_frozen": True,
                  "scientific_evidence": not test_only, "priors_updated": False,
                  "completed_UTC": utc_now()}
        write_json(record_path, record)
        records.append(record)
        if model_hash(model) != snapshot["model_hash"]:
            raise RuntimeError("Frozen model changed during intervention")
    summary = {"status": "COMPLETE", "kind": kind, "conditions": len(records),
               "seconds_actual": time.perf_counter() - start, "scientific_evidence": not test_only,
               "priors_updated": False, "records": records}
    if kind in {"random", "lesion"}:
        summary["AUC"] = {}
        for protection in sorted({r["condition"]["protect_ports"] for r in records}):
            curve = []
            for q in p["node_fractions"]:
                selected = [r for r in records if r["condition"]["q"] == q
                            and r["condition"]["protect_ports"] == protection]
                curve.append(float(np.mean([r["metrics"]["score"] for r in selected]))
                             if all(r["status"] == "COMPLETE" for r in selected) else None)
            summary["AUC"]["protected" if protection else "end_to_end"] = (
                normalized_damage_auc(p["node_fractions"], curve) if all(x is not None for x in curve) else None)
    write_json(output / "results.json", summary)
    write_json(output / "status.json", {key: summary[key] for key in ("status", "conditions", "seconds_actual", "scientific_evidence")})
    return summary


def _scale_substrate(path, cfg, test_only):
    path = Path(path)
    geometry = Geometry.load(path / "geometry.npz" if path.is_dir() else path)
    if geometry.N != 1600 or not np.isclose(geometry.L, 40):
        raise ValueError("Scale evaluation requires N1600,L40 geometry archives")
    if not test_only and geometry.metadata.get("test_only"):
        raise ValueError("Test-only geometry cannot enter scientific scale evaluation")
    kind = geometry.metadata.get("kind")
    condition = cfg["condition"]
    expected_kind = {"native": "mhu", "shuffle": "mhu", "clustered": "mhu", "matched": "mhu",
                     "random_regular": "mhu", "small_world": "grid", "grid_balanced": "grid"}.get(condition, condition)
    if kind != expected_kind:
        raise ValueError("Provided scale geometry does not match trained substrate condition")
    expected_control = "shuffle" if condition == "random_regular" else condition
    if condition in {"shuffle", "clustered", "grid_balanced", "random_regular"} and geometry.metadata.get("mark_control") != expected_control:
        raise ValueError("Scale mark organization differs from trained condition")
    if condition == "matched":
        raise RuntimeError("SCIENTIFIC_BLOCKER C3 matched scale requires resolved pair population")
    if kind in {"mhu", "hu"} and not test_only:
        certificate = geometry.metadata.get("native_certificate") or geometry.metadata.get("certificate", {})
        if not certificate.get("scientific_admissible"):
            raise RuntimeError("SCIENTIFIC_BLOCKER scale geometry failed certificate")
    graph_kind = {"random_regular": "random_regular", "small_world": "small_world"}.get(condition, "knn")
    if cfg.get("regime", "causal") == "ecological" and graph_kind == "knn":
        graph_kind = "cardinal" if kind == "grid" else "delaunay"
    edges = build_graph(geometry, graph_kind, regime=cfg.get("regime", "causal"))
    if path.is_dir() and (path / "edges.npy").exists():
        given = np.load(path / "edges.npy", allow_pickle=False)
        if not np.array_equal(given, edges):
            raise ValueError("Provided scale edges differ from inherited frozen graph rule")
    return geometry, edges


def run_scale(run_dir, output, scale_geometry_paths=None, dry_run=True, *, device="cpu",
              max_seconds=1800, test_only=False, test_limits=None):
    """Evaluate N400 steps8/16/32/64 and three supplied N1600 steps16/32/64.

    No geometry is generated and no weights are fine-tuned. Omit scale archives
    to obtain an invocable plan with the missing-scale gate explicitly blocked.
    Primary labels remain copy/fill8. Fill16 is not silently substituted.
    """
    model, cfg, manifest, geometry, edges, dataset, ports, snapshot = _load_bundle(run_dir, device, test_only)
    if cfg["task"] not in {"copy", "fill"} or (geometry.N != 400 and not test_only):
        raise ValueError("Scale preregistration is for copy/fill trained at N400")
    _, effective = _settings(test_only, test_limits)
    paths = list(scale_geometry_paths or [])
    if paths and len(paths) != 3 and not test_only:
        raise ValueError("Scientific scale evaluation requires exactly three new geometries")
    substrates = [(geometry, edges, dataset, ports, step, "trained_N400") for step in (8, 16, 32, 64)]
    for path in paths:
        large, large_edges = _scale_substrate(path, cfg, test_only)
        if large.metadata.get("geometry_seed") == cfg["geometry_seed"]:
            raise ValueError("Scale geometry seed must be new")
        world = generate_task(cfg["task"], len(dataset), dataset.seed, world_side=20, L=40, split="test")
        large_ports = register_ports(large.points, 40, 20)
        substrates.extend((large, large_edges, world, large_ports, step, str(Path(path).resolve()))
                          for step in (16, 32, 64))
    if paths and not test_only and len({x[0].metadata.get("geometry_seed") for x in substrates[4:]}) != 3:
        raise ValueError("Scale geometries require three distinct new seeds")
    plan = {"kind": "scale", "snapshot": snapshot, "scientific_evidence": not test_only,
            "fine_tuning": False, "label_horizon_fill": 8, "priors_updated": False,
            "scale_gate": "READY" if paths else "MISSING_THREE_CERTIFIED_N1600_GEOMETRIES",
            "conditions": [{"N": g.N, "L": g.L, "steps": step, "source": source,
                            "points_hash": array_hash(g.points), "labels_hash": array_hash(g.labels),
                            "edges_hash": array_hash(e), "world_hash": d.digest, "ports_hash": port.digest}
                           for g, e, d, port, step, source in substrates],
            "examples": effective["examples"]}
    frozen = _freeze(output, plan)
    output = Path(output)
    if dry_run:
        result = {"status": "NOT_RUN", "conditions": len(substrates), "scale_gate": plan["scale_gate"],
                  "plan_hash": frozen["plan_hash"], "scientific_evidence": not test_only}
        write_json(output / "status.json", result)
        return result
    if not paths and not test_only:
        raise RuntimeError("Scale execution requires three certified new N1600 geometries; dry-run documents prerequisite")
    start, records = time.perf_counter(), []
    for index, (g, e, d, port, step, source) in enumerate(substrates):
        record_path = output / "records" / f"scale_{index}.json"
        if record_path.exists():
            old = json.loads(record_path.read_text(encoding="utf-8"))
            if old["plan_hash"] != frozen["plan_hash"]:
                raise RuntimeError("Scale record belongs to another plan")
            records.append(old)
            continue
        if time.perf_counter() - start >= max_seconds:
            status = {"status": "RESOURCE_LIMIT", "completed_conditions": len(records), "resume": "repeat identical invocation"}
            write_json(output / "status.json", status)
            return status
        indices = fixed_test_indices(len(d), int(effective["examples"]))
        metrics = evaluate(model, d, g, port, graph_tensors(g, e, device), cfg["batch_size"], device,
                           indexes=indices, steps=step)
        record = {"id": f"scale_{index}", "plan_hash": frozen["plan_hash"], "N": g.N,
                  "steps": step, "metrics": metrics, "source": source,
                  "fine_tuning": False, "scientific_evidence": not test_only, "priors_updated": False}
        write_json(record_path, record)
        records.append(record)
        if model_hash(model) != snapshot["model_hash"]:
            raise RuntimeError("Frozen model changed during scale evaluation")
    result = {"status": "COMPLETE", "records": records, "scientific_evidence": not test_only,
              "priors_updated": False, "seconds_actual": time.perf_counter() - start}
    write_json(output / "results.json", result)
    write_json(output / "status.json", {k: result[k] for k in ("status", "scientific_evidence", "seconds_actual")})
    return result
