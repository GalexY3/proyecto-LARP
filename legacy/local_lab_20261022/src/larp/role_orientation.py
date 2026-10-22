"""Phase4 fixed physical slots, prospective orientation contrast B versus D8.

Preparation never creates an optimizer or performs a forward. The execution
worker requires the external supervisor; all frozen historical code is reused
without mutation. Final states only, one attempt, no automatic XOR/MHU.
"""
from __future__ import annotations

import time
_IMPORT_ENTRY = time.perf_counter()

import argparse
import importlib.metadata
import json
import math
import os
import platform
from collections import Counter
from pathlib import Path

import numpy as np
import psutil
import torch
from torch.nn import functional as F

from .artifacts import array_hash, digest, file_hash, json_safe, utc_now, write_json
from .geometry import Geometry
from .gru_baseline import GGNNLikeModel
from .learning_diagnostics import predictions, state_hash, graph_context
from .role_coverage import auxiliary_support, batch_hashes, bind_panel, geometry_features
from .transmission_probe import measure

ROOT = Path(__file__).resolve().parents[2]
CONFIG = "configs/role_orientation_v1.json"
EXPECTED_PAIRS = {("B", 2103), ("B", 2104), ("D8", 2103), ("D8", 2104)}
B_SLOTS = [(18,19,8),(18,8,19),(40,49,39),(40,39,49),(3,4,13),(14,13,4),
           (36,35,46),(36,46,35),(68,57,69),(68,69,57),(77,68,86),(77,86,68)]
SS = [(24,13,35),(46,35,57),(47,46,57),(59,49,69)]
UU = [(24,23,25),(46,45,56),(47,37,48),(59,48,50)]
AUX_OLD = [(20,11,30),(26,16,25),(61,62,60),(21,11,22)]
PRIMARY_SIZES = {"train":48, "SS":16, "UU":16}


def check_config(cfg):
    """The version is one experiment, not a tuning entry point."""
    fixed = {"protocol":"role_orientation_v1", "primary_condition":"B", "conditions":["B","D8"],
        "run_order":[["D8",2103],["B",2103],["B",2104],["D8",2104]], "training_seeds":[2103,2104],
        "calendar_seed_mapping":{"2103":2101,"2104":2102}, "N":400, "L":20., "geometry":"grid",
        "geometry_seed":1101, "local_hops":[1,2], "expected_ordered_candidate_pool":2086,
        "training_slots_B":[list(t) for t in B_SLOTS],
        "intervention":{"condition":"D8","slot_index":11,"triple":[77,68,86],"deduplicate":False},
        "SS":[list(t) for t in SS], "UU":[list(t) for t in UU], "AUX_OLD":[list(t) for t in AUX_OLD],
        "parameters":12481, "target":"b0", "steps":16, "updates":250, "batch_size":4,
        "lr":.003, "betas":[.9,.999], "eps":1e-8, "weight_decay":1e-4, "gradient_clip":1.,
        "cpu_threads":4, "dtype":"float32", "wall_budget_seconds":120, "maximum_runs":4,
        "gate_accuracy":.98, "checkpoint_selection":"final update only",
        "automatic_XOR_MHU_remote_extension":False, "architecture_evidence":False, "test_opened":False,
        "priors_H1_H6_updated":False, "architecture_C_updated":False, "historical_H_R_updated":False}
    changed = [key for key, value in fixed.items() if cfg.get(key) != value]
    if changed:
        raise ValueError(f"INVALID_EXPERIMENT: changed fixed protocol fields {changed}")


def _json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def geometry_identity(context):
    return {"coordinates":array_hash(context["geometry"].points), "edges":context["edges_hash"],
            "ports":context["ports"].digest, "edge_distances":array_hash(context["edge_dist"].numpy()),
            "labels":array_hash(context["labels"].numpy())}


def explicit_identity(cfg):
    paths = ["src/larp/role_orientation.py", "src/larp/role_coverage.py", "src/larp/role_generalization.py",
        "src/larp/gru_baseline.py", "src/larp/transmission_probe.py", "src/larp/learning_diagnostics.py",
        "src/larp/model.py", "src/larp/data.py", "src/larp/graphs.py", "src/larp/geometry.py", "src/larp/artifacts.py",
        CONFIG, "tests/test_role_orientation.py", "docs/ROLE_ORIENTATION_PROTOCOL.md",
        "docs/projects/ROLE_ORIENTATION_PHASE4_DRAFT.md", "AGENTS.md",
        "docs/charter/LARP_RESEARCH_CHARTER_AB_2_1.md", cfg["hypotheses_file"], cfg["scope_file"],
        cfg["supervisor_file"], cfg["parent_manifest"], cfg["calendar_file"], cfg["auxiliary_old_panel_file"],
        cfg["geometry_file"], "requirements-lock.txt", "pyproject.toml"]
    files = {name:file_hash(ROOT/name) for name in paths}
    runtime = {name:importlib.metadata.version(name) for name in ("numpy","scipy","torch","psutil")}
    runtime.update(python=platform.python_version(), platform=platform.platform(), device="cpu",
        threads=torch.get_num_threads(), dtype=str(torch.get_default_dtype()).removeprefix("torch."),
        deterministic_algorithms=torch.are_deterministic_algorithms_enabled())
    if runtime["threads"] != 4 or runtime["dtype"] != "float32" or not runtime["deterministic_algorithms"]:
        raise ValueError("INVALID_EXPERIMENT: runtime settings differ")
    return {"files":files, "runtime":runtime, "hash":digest({"files":files,"runtime":runtime})}


def _hist(values, weights):
    result = Counter()
    for value, weight in zip(values, weights):
        result[tuple(value) if isinstance(value,(tuple,list)) else int(value)] += int(weight)
    return [{"value":key,"count":count} for key,count in sorted(result.items())]


def slot_statistics(triples, features, weights=None):
    weights = np.ones(len(triples), dtype=np.int64) if weights is None else np.asarray(weights,dtype=np.int64)
    counts = np.zeros((2,100),dtype=np.int64)
    queries, physical_sources = Counter(), Counter()
    for (q,a,b), weight in zip(triples,weights):
        counts[0,a] += weight
        counts[1,b] += weight
        queries[q] += int(weight)
        physical_sources[a] += int(weight)
        physical_sources[b] += int(weight)
    signatures = [features["signature"][tuple(t)] for t in triples]
    return json_safe({"slots":len(triples), "visits":int(weights.sum()),
        "unique_oriented_triples":len(set(triples)), "unique_marked_cases":4*len(set(triples)),
        "unique_physical_contexts":len({(q,*sorted((a,b))) for q,a,b in triples}),
        "unique_physical_pairs":len({tuple(sorted((a,b))) for _,a,b in triples}),
        "unique_queries":len(queries), "unique_sources":len(physical_sources),
        "source_exposures_by_role":counts, "physical_source_exposures":physical_sources,
        "physical_query_exposures":queries, "role_exposure_imbalance_squared":int(np.sum((counts[0]-counts[1])**2)),
        "sum_source_role_counts_squared":int(np.sum(counts**2)), "ordered_motif_histogram":_hist(signatures,weights),
        "outdegree_histograms_by_role":[_hist([features["outdegree"][t[role]] for t in triples],weights) for role in (1,2)],
        "signatures":signatures,
        "outdegrees_by_slot":[[int(features["outdegree"][a]),int(features["outdegree"][b])] for _,a,b in triples]})


def _physical(triples):
    return Counter((q,*sorted((a,b))) for q,a,b in triples)


def calendars(cfg, parent):
    historical = _json(ROOT/cfg["calendar_file"])["schedule"]
    result = {}
    for seed, historical_seed in cfg["calendar_seed_mapping"].items():
        schedule = np.asarray(historical[str(historical_seed)],dtype=np.int64)
        if not np.array_equal(schedule,np.asarray(parent["calendars"][str(historical_seed)],dtype=np.int64)):
            raise ValueError("INVALID_EXPERIMENT: historical calendars disagree")
        slots = schedule[:,0]//4
        if schedule.shape != (250,4) or not np.array_equal(schedule,4*slots[:,None]+np.arange(4)[None,:]):
            raise ValueError("INVALID_EXPERIMENT: calendar is not250 complete quartets")
        if np.any(slots<0) or np.any(slots>=12) or set(np.bincount(slots,minlength=12)) != {20,21}:
            raise ValueError("INVALID_EXPERIMENT: calendar slot exposure differs")
        result[seed] = schedule
    return result


def build_panels(context, cfg, parent, schedules):
    check_config(cfg)
    features = geometry_features(context,cfg)
    if len(features["pool"]) != 2086 or array_hash(np.asarray(features["pool"],dtype=np.int64)) != parent["panel"]["candidate_pool_hash"]:
        raise ValueError("INVALID_EXPERIMENT: historical candidate pool changed")
    current_geometry = geometry_identity(context)
    if any(current_geometry[key] != parent["geometry"][key] for key in ("coordinates","edges","ports")):
        raise ValueError("INVALID_EXPERIMENT: historical geometry/ports/arcs changed")
    if list(map(tuple,parent["panel"]["panels"]["BALANCED"])) != B_SLOTS:
        raise ValueError("INVALID_EXPERIMENT: B differs from historical BALANCED")
    old_panel = _json(ROOT/cfg["auxiliary_old_panel_file"])["pool"]["triples"]["local"][12:]
    if list(map(tuple,old_panel)) != AUX_OLD or parent["auxiliary_old_panel"]["triples"] != old_panel:
        raise ValueError("INVALID_EXPERIMENT: old challenge panel differs")
    b, d = list(B_SLOTS), list(B_SLOTS)
    d[11] = (77,68,86)
    panels = {"B":b,"D8":d}
    if _physical(b) != _physical(d) or [i for i,(x,y) in enumerate(zip(b,d)) if x!=y] != [11]:
        raise ValueError("INVALID_EXPERIMENT: physical slots or intervention differ")
    if len(set(b)) != 12 or len(set(d)) != 11:
        raise ValueError("INVALID_EXPERIMENT: intentional D8 duplicate was lost")
    all_triples = b+d+SS+UU+AUX_OLD
    if any(t not in features["signature"] for t in all_triples):
        raise ValueError("DIAGNOSTIC_UNAVAILABLE: inadmissible fixed triple")
    common = set(range(100))
    for triples in panels.values():
        common &= {t[1] for t in triples} & {t[2] for t in triples}
    if common != {4,8,13,19,35,39,46,49,57,69}:
        raise ValueError("INVALID_EXPERIMENT: common both-role support differs")
    ss_pairs = [tuple(sorted(t[1:])) for t in SS]
    train_pairs = {tuple(sorted(t[1:])) for t in b+d}
    if len(set(ss_pairs)) != 4 or set(ss_pairs)&train_pairs:
        raise ValueError("INVALID_EXPERIMENT: SS unordered pairs are not four novel pairs")
    if any(a not in common or c not in common for _,a,c in SS):
        raise ValueError("INVALID_EXPERIMENT: SS lacks common both-role support")
    query_set = {t[0] for t in SS}
    active = {site for t in b+d for site in t}
    reserved = {site for t in UU for site in t[1:]}
    if query_set != {24,46,47,59} or reserved != {23,25,37,45,48,50,56}:
        raise ValueError("INVALID_EXPERIMENT: validation identities differ")
    if query_set & {t[0] for t in b+d} or reserved & (active|query_set|{11}):
        raise ValueError("INVALID_EXPERIMENT: query holdout or U exclusions violated")
    if query_set & set(cfg["validation_excluded_query_sites"]) or any(11 in t[1:] for t in SS+UU):
        raise ValueError("INVALID_EXPERIMENT: old validation exclusions violated")
    if [t[0] for t in SS] != [t[0] for t in UU] or any(features["signature"][x][:2] != features["signature"][y][:2] for x,y in zip(SS,UU)):
        raise ValueError("INVALID_EXPERIMENT: SS-UU query/hop matching violated")
    nominal = {name:slot_statistics(triples,features) for name,triples in panels.items()}
    weighted = {seed:{name:slot_statistics(triples,features,np.bincount(s[:,0]//4,minlength=12))
                     for name,triples in panels.items()} for seed,s in schedules.items()}
    for metric in (nominal,*weighted.values()):
        for key in ("physical_source_exposures","physical_query_exposures","ordered_motif_histogram","outdegree_histograms_by_role"):
            if metric["B"][key] != metric["D8"][key]:
                raise ValueError(f"INVALID_EXPERIMENT: matching failed for {key}")
    if [nominal[c]["role_exposure_imbalance_squared"] for c in ("B","D8")] != [0,8]:
        raise ValueError("INVALID_EXPERIMENT: nominal I differs")
    if any([m[c]["role_exposure_imbalance_squared"] for c in ("B","D8")] != [4,3364] for m in weighted.values()):
        raise ValueError("INVALID_EXPERIMENT: weighted I differs")
    report = {"status":"AVAILABLE", "panels":panels, "SS":SS, "UU":UU, "common_both_role_sources":sorted(common),
        "novel_unordered_SS_pairs":ss_pairs, "reserved_U":sorted(reserved), "reserved_queries":sorted(query_set),
        "candidate_pool_count":len(features["pool"]), "candidate_pool_hash":array_hash(np.asarray(features["pool"],dtype=np.int64)),
        "physical_slots":[(q,*sorted((a,c))) for q,a,c in b], "nominal_statistics":nominal,
        "weighted_statistics_by_seed":weighted,
        "validation_statistics":{name:slot_statistics(triples,features) for name,triples in (("SS",SS),("UU",UU))},
        "all_invariants_passed":True, "D8_duplicate_intentional":True}
    return json_safe(report), features


def build_batches(context,panel):
    batches = {**{name:bind_panel(context,triples) for name,triples in panel["panels"].items()},
        "SS":bind_panel(context,panel["SS"]), "UU":bind_panel(context,panel["UU"]), "AUX_OLD":bind_panel(context,AUX_OLD)}
    for name,batch in batches.items():
        expected = 48 if name in ("B","D8") else 16
        if len(batch["cases"]) != expected or batch["inputs"].dtype != torch.float32 or torch.count_nonzero(batch["inputs"][:,:,21:25]):
            raise ValueError("INVALID_EXPERIMENT: case multiplicity, dtype or COORDS_OFF differs")
        if not np.array_equal(batch["target"].numpy().ravel(),batch["cases"][:,3]):
            raise ValueError("INVALID_EXPERIMENT: target differs from b0")
        for slot in range(expected//4):
            if not np.array_equal(batch["cases"][4*slot:4*slot+4,3:5],[[0,0],[0,1],[1,0],[1,1]]):
                raise ValueError("INVALID_EXPERIMENT: incomplete ordered quartet")
    # Erasing role marks leaves identical distributions of physical bit inputs.
    # At the reoriented slot, role-bit pattern01 corresponds to physical10.
    mismatch = []
    for slot in range(12):
        left = batches["B"]["inputs"][4*slot:4*slot+4].clone()
        right = batches["D8"]["inputs"][4*slot:4*slot+4].clone()
        left[:,:,9:11] = 0
        right[:,:,9:11] = 0
        mapping = [0,2,1,3] if slot==11 else [0,1,2,3]
        if not torch.equal(left,right[mapping]):
            raise ValueError("INVALID_EXPERIMENT: physical bit distribution changed")
        mismatch.append(int(torch.count_nonzero(batches["B"]["target"][4*slot:4*slot+4] != batches["D8"]["target"][4*slot+np.array(mapping)])))
    if mismatch != [0]*11+[2]:
        raise ValueError("INVALID_EXPERIMENT: reorientation label contract differs")
    return batches, {"physical_bit_inputs_matched_with_role_marks_erased":True,
        "physical_pattern_target_differences_by_slot":mismatch, "targets_balanced_per_slot":True,
        "matching_does_not_imply_casewise_marked_input_or_target_equality":True}


def prepare(cfg,directory,begin):
    check_config(cfg)
    if directory.exists():
        raise FileExistsError("preparation directory exists: no overwrite")
    identity = explicit_identity(cfg)
    parent = _json(ROOT/cfg["parent_manifest"])
    context = graph_context(Geometry.load(ROOT/cfg["geometry_file"]))
    schedules = calendars(cfg,parent)
    panel,_ = build_panels(context,cfg,parent,schedules)
    batches,contract = build_batches(context,panel)
    initial = {}
    for seed in cfg["training_seeds"]:
        model = GGNNLikeModel(seed)
        if model.parameter_count != cfg["parameters"] or any(p.dtype != torch.float32 or p.device.type != "cpu" for p in model.parameters()):
            raise ValueError("INVALID_EXPERIMENT: model capacity/device/dtype differs")
        initial[str(seed)] = state_hash(model)
    hypotheses = _json(ROOT/cfg["hypotheses_file"])
    if set(hypotheses["hypotheses"]) != {"H-R4"}:
        raise ValueError("INVALID_EXPERIMENT: phase4 must register only new H-R4")
    manifest = {"status":"PREPARED", "protocol":cfg, "protocol_hash":digest(cfg), "identity":identity,
        "frozen_UTC":utc_now(), "timezone":"Europe/Madrid", "panel":panel, "calendars":schedules,
        "calendar_hashes":{s:array_hash(c) for s,c in schedules.items()}, "initial_state_hashes":initial,
        "geometry":geometry_identity(context), "dataset_hashes":{name:batch_hashes(batch) for name,batch in batches.items()},
        "physical_input_label_contract":contract, "hypotheses":hypotheses,
        "auxiliary_old_panel":{"triples":AUX_OLD,"known_not_blind":True,"outside_primary_gate":True,
            "used_for_prospective_XOR_readiness":True,"training_support_by_condition":auxiliary_support(AUX_OLD,panel["panels"])},
        "preparation_seconds_no_training":time.perf_counter()-begin, "optimizers_created":0,"forwards_performed":0,
        "architecture_evidence":False,"test_opened":False,"H1_H6_updated":False,"architecture_C_updated":False,
        "historical_H_R_updated":False,"XOR_MHU_remote":{"status":"NOT_RUN"}}
    directory.mkdir(parents=True,exist_ok=False)
    write_json(directory/"preregistration.json",manifest)
    (directory/"protocol_frozen.md").write_text((ROOT/"docs/ROLE_ORIENTATION_PROTOCOL.md").read_text(encoding="utf-8")+
        f"\n\nFrozen identity: {identity['hash']}\nProtocol: {manifest['protocol_hash']}\n",encoding="utf-8")
    print("PREPARED B/D8, I=0/8, weightedI=4/3364; no optimizers or forwards",flush=True)
    return json_safe(manifest)


def measurement_valid(value,size):
    """Missing patterns/flips and nonfinite diagnostics cannot masquerade as COMPLETE."""
    if not isinstance(value,dict) or value.get("finite") is not True or len(value.get("cases",[])) != size:
        return False
    if not all(isinstance(value.get(k),(int,float)) and math.isfinite(value[k]) for k in ("accuracy","loss")):
        return False
    rows = value["cases"]
    for row in rows:
        if len(row.get("case",[])) != 5 or row.get("prediction") not in (0,1) or row.get("target") not in (0,1):
            return False
        scalars = [row.get("logit")]
        for key in ("source_gradients","source_flipped_logits","source_flip_abs_logit_changes"):
            if len(row.get(key,[])) != 2:
                return False
            scalars += row[key]
        if any(not isinstance(x,(int,float)) or not math.isfinite(x) for x in scalars):
            return False
        if row.get("source_flip_should_change_target") != [True,False]:
            return False
        for key in ("source_flip_correct_predictions","source_flip_class_changes"):
            if len(row.get(key,[])) != 2 or any(type(x) is not bool for x in row[key]):
                return False
    observed_accuracy = sum(row["prediction"]==row["target"] for row in rows)/size
    return math.isclose(value["accuracy"],observed_accuracy,abs_tol=1e-12)


def complete_record(record, require_aux=False):
    if (record.get("condition"),record.get("training_seed")) not in EXPECTED_PAIRS:
        return False
    if (record.get("status") != "COMPLETE" or record.get("finite") is not True or
        record.get("updates_completed") != 250 or record.get("score_checkpoint_update") != 250 or
        record.get("identity_verified") is not True or record.get("data_verified") is not True):
        return False
    if any(not isinstance(record.get(key),str) or len(record[key])!=64 for key in
           ("checkpoint_sha256","initial_state_hash","final_state_hash")):
        return False
    panels = {**PRIMARY_SIZES, **({"AUX_OLD":16} if require_aux else {})}
    return all(measurement_valid(record.get(split),size) and record[split].get("measure_checkpoint_update")==250
               for split,size in panels.items())


def gate(records,condition,threshold=.98,require_aux=False):
    selected = [row for row in records if row.get("condition")==condition]
    if len(selected)!=2 or {row.get("training_seed") for row in selected}!={2103,2104}:
        return False
    splits = (*PRIMARY_SIZES, *(("AUX_OLD",) if require_aux else ()))
    return all(complete_record(row,require_aux) and all(row[split]["accuracy"]>=threshold for split in splits)
               for row in selected)


def aggregate_status(records):
    if len(records)!=4 or {(r.get("condition"),r.get("training_seed")) for r in records}!=EXPECTED_PAIRS:
        return "INCOMPLETE"
    statuses = {row.get("status") for row in records}
    if "INVALID_EXPERIMENT" in statuses:
        return "INVALID_EXPERIMENT"
    if "RESOURCE_LIMIT" in statuses or any(r.get("status")=="NOT_RUN" and "budget" in r.get("reason","") for r in records):
        return "RESOURCE_LIMIT"
    if any(str(status).startswith("NUMERICAL_FAILURE") for status in statuses):
        return "NUMERICAL_FAILURE"
    return "COMPLETE" if all(complete_record(row) for row in records) else "INCOMPLETE"


def hypothesis_updates(records,hypotheses):
    eligible = aggregate_status(records)=="COMPLETE"
    h = hypotheses["hypotheses"]["H-R4"]
    out = {"eligible":eligible,"registered_hypotheses":hypotheses["version"],"numerical_posteriors":False,
        "Bayes_factors":False,"H1_H6":"unchanged","architecture_C":"unchanged","H_R1_H_R3":"unchanged","updates":{}}
    direction = "no_update_ineligible"
    if eligible:
        rows = {(r["condition"],r["training_seed"]):r for r in records}
        differences = {str(seed):rows["B",seed]["UU"]["accuracy"]-rows["D8",seed]["UU"]["accuracy"] for seed in (2103,2104)}
        out["UU_accuracy_differences_by_seed"] = differences
        threshold,effect = hypotheses["threshold"],hypotheses["effect_threshold_accuracy_points"]
        direction = ("weak_support" if gate(records,"B",threshold) and all(d>=effect for d in differences.values()) else
            "weak_counterevidence" if gate(records,"D8",threshold) and all(d<=0 for d in differences.values()) else
            "neutral_or_inconclusive")
    out["updates"]["H-R4"] = {"prior_ordinal":h["prior_ordinal"],"direction":direction,
        "limitation":h["limit"],"primary_effect_endpoint":"UU"}
    return out


def _measure_final(model,batch,context,cfg,completed):
    value = measure(model,batch,context,cfg,"b0")
    value["measure_checkpoint_update"] = completed
    value["slot_summaries"] = []
    for slot in range(len(batch["cases"])//4):
        rows = value["cases"][4*slot:4*slot+4]
        value["slot_summaries"].append({"slot_index":slot,"triple":batch["cases"][4*slot,:3].tolist(),
            "correct":sum(r["prediction"]==r["target"] for r in rows),"cases":4,
            "accuracy":sum(r["prediction"]==r["target"] for r in rows)/4})
    return value


def validate_prepared(cfg,manifest):
    """Full reconstruction before an optimizer, rather than trusting editable metadata."""
    check_config(cfg)
    if manifest.get("status")!="PREPARED" or manifest.get("protocol")!=cfg or manifest.get("protocol_hash")!=digest(cfg):
        raise ValueError("INVALID_EXPERIMENT: no identical prepared protocol")
    identity = explicit_identity(cfg)
    if identity != manifest["identity"]:
        raise ValueError("INVALID_EXPERIMENT: frozen source/config/document/runtime bytes changed")
    parent = _json(ROOT/cfg["parent_manifest"])
    context = graph_context(Geometry.load(ROOT/cfg["geometry_file"]))
    schedules = calendars(cfg,parent)
    panel,_ = build_panels(context,cfg,parent,schedules)
    if panel != manifest["panel"] or geometry_identity(context)!=manifest["geometry"]:
        raise ValueError("INVALID_EXPERIMENT: frozen panel/geometry/statistics changed")
    if json_safe(schedules)!=manifest["calendars"] or {s:array_hash(c) for s,c in schedules.items()}!=manifest["calendar_hashes"]:
        raise ValueError("INVALID_EXPERIMENT: frozen mapped calendars changed")
    batches,contract = build_batches(context,panel)
    if {name:batch_hashes(batch) for name,batch in batches.items()} != manifest["dataset_hashes"] or contract!=manifest["physical_input_label_contract"]:
        raise ValueError("INVALID_EXPERIMENT: frozen input/target/case bytes changed")
    if _json(ROOT/cfg["hypotheses_file"]) != manifest["hypotheses"]:
        raise ValueError("INVALID_EXPERIMENT: H-R4 changed")
    for seed in cfg["training_seeds"]:
        model = GGNNLikeModel(seed)
        if model.parameter_count!=cfg["parameters"] or state_hash(model)!=manifest["initial_state_hashes"][str(seed)]:
            raise ValueError("INVALID_EXPERIMENT: frozen initialization changed")
    return identity,context,batches,schedules


def _exclusive_json(path,value):
    with Path(path).open("x",encoding="utf-8") as stream:
        json.dump(json_safe(value),stream,ensure_ascii=False,indent=2,allow_nan=False)


def supervised_deadline(directory,cfg):
    """Reject accidental direct/unbounded worker invocation."""
    token = os.environ.get("LARP_ROLE_ORIENTATION_TOKEN")
    if not token:
        raise ValueError("external hard supervisor required; use artifacts/role_orientation/run_supervised.py")
    marker = _json(directory/"execution_started.json")
    parent_pid = int(os.environ["LARP_ROLE_ORIENTATION_SUPERVISOR_PID"])
    begin = float(os.environ["LARP_ROLE_ORIENTATION_BEGIN"])
    deadline = float(os.environ["LARP_ROLE_ORIENTATION_DEADLINE"])
    if (marker.get("token")!=token or marker.get("supervisor_pid")!=parent_pid or os.getppid()!=parent_pid or
        marker.get("command_entry_perf_counter")!=begin or marker.get("deadline_perf_counter")!=deadline or
        deadline-begin!=cfg["wall_budget_seconds"] or not psutil.pid_exists(parent_pid)):
        raise ValueError("INVALID_EXPERIMENT: supervisor/deadline identity differs")
    if marker["prepared_manifest_sha256"]!=file_hash(directory/"preregistration.json"):
        raise ValueError("INVALID_EXPERIMENT: prepared manifest changed after launch")
    _exclusive_json(directory/"worker_started.json",{"UTC":utc_now(),"pid":os.getpid(),"supervisor_pid":parent_pid,"token":token})
    return begin,deadline


def run_one(condition,seed,batches,context,calendar,manifest,cfg,directory,deadline):
    record = {"condition":condition,"training_seed":seed,"calendar_historical_seed":cfg["calendar_seed_mapping"][str(seed)],
        "status":"NOT_RUN","finite":False,"identity_verified":True,"data_verified":True,
        "updates_completed":0,"score_checkpoint_update":None}
    out = directory/f"{condition.lower()}_s{seed}"
    out.mkdir(parents=True,exist_ok=False)
    write_json(out/"progress.json",record)
    if time.perf_counter()>=deadline:
        record["reason"]="global wall budget exhausted"
        write_json(out/"results.json",record)
        return record
    model = GGNNLikeModel(seed)
    initial = state_hash(model)
    if initial!=manifest["initial_state_hashes"][str(seed)] or model.parameter_count!=cfg["parameters"]:
        raise ValueError("INVALID_EXPERIMENT: frozen initialization/model changed")
    record.update(initial_state_hash=initial,parameters=model.parameter_count,
        data_hashes={name:batch_hashes(batch) for name,batch in batches.items()},calendar_hash=array_hash(calendar))
    optimizer = torch.optim.AdamW(model.parameters(),lr=cfg["lr"],betas=tuple(cfg["betas"]),eps=cfg["eps"],weight_decay=cfg["weight_decay"])
    status,completed,curve,times = "COMPLETE",0,[],[]
    begin = time.perf_counter()
    process = psutil.Process()
    peak = process.memory_info().rss
    record["status"]="RUNNING"
    write_json(out/"progress.json",record)
    for selected in calendar:
        if time.perf_counter()>=deadline:
            status="RESOURCE_LIMIT"
            break
        model.train()
        optimizer.zero_grad(set_to_none=True)
        part={name:batches["train"][name][selected] for name in ("inputs","output","target")}
        tick=time.perf_counter()
        logits=predictions(model,part,context,cfg["steps"])
        loss=F.binary_cross_entropy_with_logits(logits,part["target"])
        if not torch.isfinite(loss):
            status="NUMERICAL_FAILURE"
            break
        loss.backward()
        norm=torch.nn.utils.clip_grad_norm_(model.parameters(),cfg["gradient_clip"])
        if not torch.isfinite(norm):
            status="NUMERICAL_FAILURE"
            break
        optimizer.step()
        completed+=1
        times.append(time.perf_counter()-tick)
        peak=max(peak,process.memory_info().rss)
        if completed==1 or completed%25==0:
            curve.append({"update":completed,"optimization_loss":float(loss.detach()),"preclip_gradient_norm":float(norm)})
            record.update(updates_completed=completed,optimization_curve=curve)
            write_json(out/"progress.json",record)
    record.update(status=status,updates_completed=completed,score_checkpoint_update=completed,
        optimization_curve=curve,final_state_hash=state_hash(model),
        exposure_count_by_case=np.bincount(calendar[:completed].ravel(),minlength=48),
        median_update_seconds=float(np.median(times)) if times else None)
    if not all(torch.isfinite(p).all() for p in model.parameters()):
        record["status"]="NUMERICAL_FAILURE"
    # Save the state that will be measured, before any final diagnostic.
    torch.save({"model":model.state_dict(),"optimizer":optimizer.state_dict(),"completed_updates":completed,
        "condition":condition,"training_seed":seed,"initial_state_hash":initial,"final_state_hash":record["final_state_hash"],
        "frozen_calendar":calendar,"protocol_hash":manifest["protocol_hash"],"identity_hash":manifest["identity"]["hash"]},out/"final_checkpoint.pt")
    record["checkpoint_sha256"]=file_hash(out/"final_checkpoint.pt")
    write_json(out/"progress.json",record)
    for name,batch in batches.items():
        if time.perf_counter()>=deadline:
            record[name]={"status":"AUX_NOT_MEASURED" if name=="AUX_OLD" else "NOT_MEASURED","reason":"global deadline"}
            record["status"]="RESOURCE_LIMIT"
            continue
        record[name]=_measure_final(model,batch,context,cfg,completed)
        if not measurement_valid(record[name],len(batch["cases"])):
            record["status"]="NUMERICAL_FAILURE"
        write_json(out/"progress.json",record)
    record["finite"]=bool(all(measurement_valid(record.get(name),size) for name,size in PRIMARY_SIZES.items())
        and all(torch.isfinite(p).all() for p in model.parameters()))
    if time.perf_counter()>=deadline:
        record["status"]="RESOURCE_LIMIT"
    elif record["status"]=="COMPLETE" and not complete_record(record):
        record["status"]="INCOMPLETE"
    record.update(seconds_including_measurement=time.perf_counter()-begin,RSS_peak_bytes_sampled=max(peak,process.memory_info().rss))
    write_json(out/"results.json",record)
    print(condition,seed,record["status"],completed,{name:record.get(name,{}).get("accuracy") for name in (*PRIMARY_SIZES,"AUX_OLD")},flush=True)
    return record


def execute(cfg,directory):
    begin,deadline=supervised_deadline(directory,cfg)
    forbidden=[directory/"results.json",directory/"H_R4_ordinal_updates.json"]
    forbidden += [directory/f"{c.lower()}_s{s}" for c,s in cfg["run_order"]]
    if any(path.exists() for path in forbidden):
        raise FileExistsError("existing execution evidence: no overwrite or retry")
    manifest=_json(directory/"preregistration.json")
    identity,context,batches,schedules=validate_prepared(cfg,manifest)
    records=[]
    for condition,seed in cfg["run_order"]:
        subsets={"train":batches[condition],"SS":batches["SS"],"UU":batches["UU"],"AUX_OLD":batches["AUX_OLD"]}
        records.append(run_one(condition,seed,subsets,context,schedules[str(seed)],manifest,cfg,directory,deadline))
    identity_unchanged=explicit_identity(cfg)==identity
    if not identity_unchanged:
        for record in records:
            record["identity_verified"]=False
            record["status"]="INVALID_EXPERIMENT"
    updates=hypothesis_updates(records,manifest["hypotheses"])
    result={"status":aggregate_status(records),"stage":cfg["stage"],"identity":identity,"identity_unchanged":identity_unchanged,
        "records":records,"primary_condition":"B","gates":{c:gate(records,c,cfg["gate_accuracy"]) for c in cfg["conditions"]},
        "XOR_readiness":gate(records,"B",cfg["gate_accuracy"],require_aux=True),
        "H_R4_ordinal_updates":updates,"seconds_actual_from_supervisor_entry":time.perf_counter()-begin,"completed_UTC":utc_now(),
        "paired_accuracy_differences":{str(seed):{split:next(r for r in records if r["condition"]=="B" and r["training_seed"]==seed).get(split,{}).get("accuracy",0)-
            next(r for r in records if r["condition"]=="D8" and r["training_seed"]==seed).get(split,{}).get("accuracy",0)
            for split in PRIMARY_SIZES if all(split in r and "accuracy" in r[split] for r in records if r["training_seed"]==seed)} for seed in (2103,2104)},
        "auxiliary_old_panel_comparability":manifest["auxiliary_old_panel"],
        "architecture_evidence":False,"test_opened":False,"H1_H6_updated":False,"architecture_C_updated":False,
        "historical_H_R_updated":False,"original_pilot_unchanged":True,
        "XOR_MHU_remote":{"status":"NOT_RUN","reason":"requires a separate prospective protocol and human decision"}}
    write_json(directory/"results.json",result)
    write_json(directory/"H_R4_ordinal_updates.json",updates)
    print("status",result["status"],"gates",result["gates"],"XOR_readiness",result["XOR_readiness"],flush=True)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare-only",action="store_true")
    group.add_argument("--execute-prepared",action="store_true")
    parser.add_argument("--output",type=Path,default=ROOT/"artifacts/role_orientation/v1")
    args=parser.parse_args(argv)
    cfg=_json(ROOT/CONFIG)
    torch.set_num_threads(cfg["cpu_threads"])
    torch.use_deterministic_algorithms(True)
    return prepare(cfg,args.output,_IMPORT_ENTRY) if args.prepare_only else execute(cfg,args.output)


if __name__=="__main__":
    main()
