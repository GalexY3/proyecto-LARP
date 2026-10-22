"""Phase3: frozen geometry-only curricula and a common SS/UU validation panel.

Preparation creates no optimizer. Execution requires that exact preparation,
including unchanged code/config/hypotheses, and uses one global wall deadline.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import time
from collections import Counter
from itertools import permutations
from pathlib import Path

import numpy as np
import psutil
import torch
from scipy.sparse import csr_matrix
from torch.nn import functional as F

from .artifacts import array_hash, digest, file_hash, utc_now, write_json
from .data import minimum_image_displacements
from .geometry import Geometry
from .gru_baseline import GGNNLikeModel
from .learning_diagnostics import bind_cases, graph_context, make_cases, predictions, state_hash
from .role_generalization import coordinates_off
from .transmission_probe import measure, target_batch

ROOT = Path(__file__).resolve().parents[2]


def geometry_features(context, cfg):
    ports, geometry = context["ports"].indices, context["geometry"]
    edges = context["edge_index"].numpy()
    hops = context["hops"][np.ix_(ports, ports)]
    adjacency = csr_matrix((np.ones(edges.shape[1], dtype=np.int64), (edges[0], edges[1])), shape=(geometry.N, geometry.N))
    paths2 = (adjacency@adjacency)[ports][:, ports].toarray()
    r2 = np.sum(minimum_image_displacements(geometry.points[ports, None], geometry.points[ports][None], geometry.L)**2, axis=2)
    near = {q: np.flatnonzero((hops[:,q]>=cfg["local_hops"][0]) & (hops[:,q]<=cfg["local_hops"][1])).tolist() for q in range(len(ports))}
    pool = [(q,a,b) for q in range(len(ports)) for a,b in permutations(near[q],2)]
    signature = {t: (int(hops[t[1],t[0]]), int(hops[t[2],t[0]]), int(paths2[t[1],t[0]]), int(paths2[t[2],t[0]]),
                     round(float(r2[t[1],t[0]]),8), round(float(r2[t[2],t[0]]),8)) for t in pool}
    return {"pool": pool, "near": near, "hops": hops, "paths2": paths2, "r2": r2, "signature": signature,
            "outdegree": np.bincount(edges[0], minlength=geometry.N)[ports]}


def objective(triples, signatures, site_count=100):
    count = np.zeros((2,site_count), dtype=np.int64)
    for _,a,b in triples:
        count[0,a] += 1
        count[1,b] += 1
    histogram = Counter(signatures[tuple(t)] for t in triples)
    return (int(np.sum(count**2)), int(np.sum((count[0]-count[1])**2)), sum(v*v for v in histogram.values()))


def greedy_extras(anchors, eligible_ids, features, priority, count_to_add=8):
    pool, signature = features["pool"], features["signature"]
    selected = list(map(tuple, anchors))
    available = set(map(int, eligible_ids))
    trace = []
    for step in range(count_to_add):
        counts = np.zeros((2,100), dtype=np.int64)
        for _,a,b in selected:
            counts[0,a] += 1
            counts[1,b] += 1
        histogram = Counter(signature[t] for t in selected)
        difference = counts[0]-counts[1]
        def increment(index):
            t = pool[index]
            _,a,b = t
            return (int(2*counts[0,a]+2*counts[1,b]+2), int(2*difference[a]-2*difference[b]+2),
                    int(2*histogram[signature[t]]+1), int(priority[index]))
        best = min(available, key=increment)
        trace.append({"step":step, "candidate_pool_index":best, "triple":pool[best],
                      "objective_increment":increment(best)[:3], "tie_priority":int(priority[best]),
                      "objective_after":objective(selected+[pool[best]],signature)})
        selected.append(pool[best])
        available.remove(best)
    return sorted(selected[len(anchors):]), trace


def panel_metrics(triples, features):
    counts = np.zeros((2,100), dtype=np.int64)
    for _,a,b in triples:
        counts[0,a] += 1
        counts[1,b] += 1
    return {"triple_count":len(triples), "unique_queries":len({t[0] for t in triples}),
            "unique_sources_by_role":[int(np.count_nonzero(c)) for c in counts],
            "source_exposures_in_triples_by_role":counts,
            "role_exposure_imbalance_squared":int(np.sum((counts[0]-counts[1])**2)),
            "objective":objective(triples, features["signature"]),
            "source_outdegrees_by_role":[[int(features["outdegree"][t[r]]) for t in triples] for r in (1,2)],
            "signatures":[features["signature"][tuple(t)] for t in triples]}


def build_panels(context, cfg):
    features = geometry_features(context,cfg)
    pool = features["pool"]
    if len(pool) != cfg["expected_ordered_candidate_pool"]:
        raise ValueError("candidate pool differs from the frozen Grid specification")
    rng = np.random.default_rng(np.random.SeedSequence([cfg["master_seed"],cfg["namespaces"]["anchors"]]))
    validation_rng = np.random.default_rng(np.random.SeedSequence([cfg["master_seed"],cfg["namespaces"]["validation"]]))
    excluded_queries = set(cfg["validation_excluded_query_sites"])
    excluded_sources = set(cfg["validation_excluded_source_sites"])
    attempts = []
    accepted = None
    for attempt in range(cfg["maximum_anchor_attempts"]):
        sampled_ids = rng.choice(len(pool),2,replace=False).tolist()
        base = [pool[i] for i in sampled_ids]
        training_queries = {t[0] for t in base}
        seen = {site for t in base for site in t[1:]}
        info = {"attempt":attempt, "base_candidate_ids":sampled_ids, "base_triples":base}
        if len(training_queries)!=2 or len(seen)!=4:
            attempts.append({**info,"status":"REJECTED","reason":"need two different queries and four distinct source sites"})
            continue
        query_matches = {}
        for q in range(100):
            if q in training_queries|excluded_queries:
                continue
            near = features["near"][q]
            ss = [(a,b) for a,b in permutations(near,2) if a in seen and b in seen and a not in excluded_sources and b not in excluded_sources]
            # Reserved U cannot overlap any active anchor port. These exclusions
            # apply to validation source selection, never globally purge training.
            uu = [(a,b) for a,b in permutations(near,2) if a not in seen|training_queries|excluded_sources and b not in seen|training_queries|excluded_sources]
            matches = [(a,b,c,d) for a,b in ss for c,d in uu
                       if (features["hops"][a,q],features["hops"][b,q]) == (features["hops"][c,q],features["hops"][d,q])]
            if matches:
                query_matches[q] = matches
        if len(query_matches)<cfg["validation_queries"]:
            attempts.append({**info,"status":"REJECTED","reason":"fewer than four common SS/UU query candidates", "query_candidates":list(query_matches)})
            continue
        queries = validation_rng.choice(sorted(query_matches),cfg["validation_queries"],replace=False).tolist()
        ss, uu = [], []
        for q in queries:
            a,b,c,d = query_matches[q][int(validation_rng.integers(len(query_matches[q])))]
            ss.append((q,a,b))
            uu.append((q,c,d))
        reserved_u = {site for t in uu for site in t[1:]}
        anchors = [base[0],(base[0][0],base[0][2],base[0][1]),base[1],(base[1][0],base[1][2],base[1][1])]
        query_set = set(queries)
        eligible_ids = [i for i,t in enumerate(pool) if t not in anchors and t[0] not in query_set and not(set(t)&reserved_u)]
        if len(eligible_ids)<cfg["extras"]:
            attempts.append({**info,"status":"REJECTED","reason":"reserved validation leaves fewer than eight extras",
                             "reserved_queries":queries,"reserved_U":sorted(reserved_u)})
            continue
        attempts.append({**info,"status":"ACCEPTED","query_candidates":list(query_matches),
                         "reserved_queries":queries,"reserved_U":sorted(reserved_u),"eligible_extras":len(eligible_ids)})
        accepted = (anchors,ss,uu,eligible_ids,reserved_u,queries)
        break
    if accepted is None:
        return {"status":"DIAGNOSTIC_UNAVAILABLE","reason":"no geometry-only eligible panel within 1000 attempts","attempts":attempts,
                "candidate_pool_count":len(pool)},features
    anchors,ss,uu,eligible_ids,reserved_u,queries = accepted
    uniform_rng = np.random.default_rng(np.random.SeedSequence([cfg["master_seed"],cfg["namespaces"]["uniform"]]))
    uniform_ids = uniform_rng.choice(eligible_ids,cfg["extras"],replace=False).tolist()
    uniform_extras = sorted(pool[i] for i in uniform_ids)
    ties = np.random.default_rng(np.random.SeedSequence([cfg["master_seed"],cfg["namespaces"]["balanced_ties"]])).permutation(len(pool))
    priority = np.empty(len(pool),dtype=np.int64)
    priority[ties] = np.arange(len(pool))
    balanced, greedy_trace = greedy_extras(anchors,eligible_ids,features,priority,cfg["extras"])
    panels = {"UNIFORM":anchors+uniform_extras,"BALANCED":anchors+balanced}
    report = {"status":"AVAILABLE","candidate_pool_count":len(pool), "candidate_pool_hash":array_hash(np.array(pool,dtype=np.int64)),
              "hop_profiles":sorted(set((s[0],s[1]) for s in features["signature"].values())),
              "signature_bins":sorted(set(features["signature"].values())), "attempts":attempts,
              "anchors":anchors,"panels":panels,"SS":ss,"UU":uu,"reserved_U":sorted(reserved_u),"reserved_queries":queries,
              "eligible_extra_count":len(eligible_ids),"uniform_sampled_pool_ids_before_sort":uniform_ids,
              "balanced_tie_priority":priority,"balanced_greedy_trace":greedy_trace,
              "panel_metrics":{name:panel_metrics(triples,features) for name,triples in panels.items()},
              "validation_metrics":{name:panel_metrics(triples,features) for name,triples in (("SS",ss),("UU",uu))},
              "limitations":["conditional Uniform, four fixed anchors plus eight random extras; not twelve IID",
                  "seen validation sources come from four shared anchors, not every source exposure",
                  "hop matching is coarse; all actual hops equal two",
                  "motif proxy omits direction, source-query mixing, longer walks and neighborhood states",
                  "the diversity intervention is a curriculum-construction package, not an isolated count mediator"]}
    return report,features


def bind_panel(context,triples):
    return coordinates_off(target_batch(bind_cases(context,make_cases(triples),"local"),"b0"))


def gate(records,condition,threshold=.98):
    selected = [r for r in records if r["condition"]==condition]
    return (len(selected)==2 and {r["training_seed"] for r in selected}=={2101,2102}
            and all(r["status"]=="COMPLETE" and r.get("finite",False) and r.get("updates_completed")==250
                    and all(r.get(split,{}).get("accuracy",0)>=threshold for split in ("train","SS","UU")) for r in selected))


def hypothesis_updates(records,hypotheses):
    expected = {(c,s) for c in ("UNIFORM","BALANCED") for s in (2101,2102)}
    eligible = ({(r["condition"],r["training_seed"]) for r in records}==expected and len(records)==4
                and all(r["status"]=="COMPLETE" and r.get("finite",False) and r.get("updates_completed")==250 for r in records))
    out = {"eligible":eligible,"registered_hypotheses":hypotheses["version"],"numerical_posteriors":False,
           "Bayes_factors":False,"H1_H6":"unchanged","architecture_C":"unchanged","updates":{}}
    if not eligible:
        for name,h in hypotheses["hypotheses"].items():
            out["updates"][name] = {"prior_ordinal":h["prior_ordinal"],"direction":"no_update_ineligible",
                                    "limitation":h["limit"]}
        return out
    rows = {(r["condition"],r["training_seed"]):r for r in records}
    threshold,effect = hypotheses["threshold"],hypotheses["effect_threshold_accuracy_points"]
    b = [rows["BALANCED",s] for s in (2101,2102)]
    u = [rows["UNIFORM",s] for s in (2101,2102)]
    diff = [x["UU"]["accuracy"]-y["UU"]["accuracy"] for x,y in zip(b,u)]
    b_train_ss = all(r["train"]["accuracy"]>=threshold and r["SS"]["accuracy"]>=threshold for r in b)
    u_train_ss = all(r["train"]["accuracy"]>=threshold and r["SS"]["accuracy"]>=threshold for r in u)
    b_all = gate(records,"BALANCED",threshold)
    directions = {
        "H-R1":"weak_support" if b_train_ss and all(d>=effect for d in diff) else "weak_counterevidence" if u_train_ss and all(d<=-effect for d in diff) else "neutral_or_inconclusive",
        "H-R2":"weak_support" if b_train_ss and all(r["UU"]["accuracy"]<threshold for r in b) else "weak_counterevidence" if b_all else "neutral_or_inconclusive",
        "H-R3":"weak_support" if any(r["SS"]["accuracy"]<threshold for r in b) else "weak_counterevidence" if b_train_ss else "neutral_or_inconclusive"}
    out["UU_accuracy_differences_by_seed"] = {str(s):d for s,d in zip((2101,2102),diff)}
    for name,h in hypotheses["hypotheses"].items():
        out["updates"][name] = {"prior_ordinal":h["prior_ordinal"],"direction":directions[name],
            "ordinal_assessment":"moderately_plausible_with_weak_support" if directions[name]=="weak_support" else
                "moderately_plausible_with_weak_counterevidence" if directions[name]=="weak_counterevidence" else "moderately_plausible_unresolved",
            "limitation":h["limit"]}
    ss_failures = sum(r["SS"]["accuracy"]<threshold for r in b)
    out["updates"]["H-R3"]["failure_pattern"] = "two_seed_transfer_failure" if ss_failures==2 else "one_seed_initialization_instability" if ss_failures==1 else "no_SS_failure"
    return out


def explicit_identity(cfg):
    paths = ["src/larp/role_coverage.py","src/larp/role_generalization.py","src/larp/gru_baseline.py","src/larp/transmission_probe.py",
             "src/larp/learning_diagnostics.py","src/larp/model.py","src/larp/data.py","src/larp/graphs.py","src/larp/geometry.py",
             "src/larp/artifacts.py","configs/role_coverage_v1.json",cfg["hypotheses_file"],cfg["scope_file"],
             "tests/test_role_coverage.py",cfg["calendar_file"],"artifacts/geometry/grid_N400_g1101.npz"]
    paths.append(cfg["auxiliary_old_panel_file"])
    files = {name:file_hash(ROOT/name) for name in paths}
    runtime = {name:importlib.metadata.version(name) for name in ("numpy","scipy","torch","psutil")}
    runtime.update(python=platform.python_version(),platform=platform.platform(),threads=4,device="cpu",dtype="float32",deterministic_algorithms=True)
    return {"files":files,"runtime":runtime,"hash":digest({"files":files,"runtime":runtime})}


def batch_hashes(batch):
    return {name:array_hash(np.asarray(value)) for name,value in (("inputs",batch["inputs"].numpy()),("target",batch["target"].numpy()),
            ("output",batch["output"].numpy()),("cases",batch["cases"]))}


def auxiliary_support(known_triples,panels):
    """Pre-score disclosure of how new training changes old-panel comparability."""
    return {condition:[{"triple":t,"exact_triple_in_training":tuple(t) in set(map(tuple,train)),
                "query_seen_as_query":t[0] in {x[0] for x in train},
                "source0_seen_as_role0":t[1] in {x[1] for x in train},
                "source0_seen_as_role1":t[1] in {x[2] for x in train},
                "source1_seen_as_role0":t[2] in {x[1] for x in train},
                "source1_seen_as_role1":t[2] in {x[2] for x in train},
                "active_port_exposed_any_training_role":{str(site):site in {s for x in train for s in x} for site in t}}
                for t in known_triples] for condition,train in panels.items()}


def prepare(cfg,directory,begin):
    context = graph_context(Geometry.load(ROOT/"artifacts/geometry/grid_N400_g1101.npz"))
    panel,features = build_panels(context,cfg)
    calendar = json.loads((ROOT/cfg["calendar_file"]).read_text(encoding="utf-8"))
    schedules = {str(seed):calendar["schedule"][str(seed)] for seed in cfg["training_seeds"]}
    if any(np.asarray(s).shape!=(250,4) for s in schedules.values()):
        raise ValueError("published balanced calendar differs")
    hypotheses = json.loads((ROOT/cfg["hypotheses_file"]).read_text(encoding="utf-8"))
    identity = explicit_identity(cfg)
    directory.mkdir(parents=True,exist_ok=False)
    manifest = {"status":"PREPARED" if panel["status"]=="AVAILABLE" else "DIAGNOSTIC_UNAVAILABLE",
        "protocol":cfg,"protocol_hash":digest(cfg),"identity":identity,"frozen_UTC":utc_now(),"panel":panel,"calendars":schedules,
        "hypotheses":hypotheses,"initial_state_hashes":{str(seed):state_hash(GGNNLikeModel(seed)) for seed in cfg["training_seeds"]},
        "geometry":{"coordinates":array_hash(context["geometry"].points),"edges":context["edges_hash"],"ports":context["ports"].digest},
        "preparation_seconds_no_training":time.perf_counter()-begin,"architecture_evidence":False,"test_opened":False,
        "H1_H6_updated":False,"architecture_C_updated":False}
    if panel["status"]=="AVAILABLE":
        old_panel=json.loads((ROOT/cfg["auxiliary_old_panel_file"]).read_text(encoding="utf-8"))["pool"]["triples"]["local"][12:]
        batches = {**{name:bind_panel(context,triples) for name,triples in panel["panels"].items()},
                   "SS":bind_panel(context,panel["SS"]),"UU":bind_panel(context,panel["UU"]),"AUX_OLD":bind_panel(context,old_panel)}
        manifest["dataset_hashes"] = {name:batch_hashes(batch) for name,batch in batches.items()}
        manifest["auxiliary_old_panel"]={"triples":old_panel,"known_not_blind":True,"outside_gate_and_H_R_update":True,
                                         "training_support_by_condition":auxiliary_support(old_panel,panel["panels"])}
    write_json(directory/"preregistration.json",manifest)
    (directory/"protocol_frozen.md").write_text(
        "# Phase3 frozen before optimizers\n\nFour common anchors plus8extras perpanel; uniform conditional vslexicographic geometry-only coverage. " +
        "SS/UU common4queries×4patterns, hops matched; U held fromeveryactive trainingrole. GGNN unchanged/COORDS_OFF, " +
        "B4/T16/.003AdamW/250updates, seeds2101/2102; old balanced calendars reused. ABBA fixed, global120s. " +
        "BALANCED primary; bothseeds train/SS/UU>=.98 finite. H-R ordinal registered, no numericAB/H1–H6/C/test/pilotoverride. " +
        "Allfour oldvaltriples measured AUX atfinal state outsidegates, withsupport disclosure; neverfeedback. " +
        "No retries, winners, extra runs or automatic XOR/MHU/remote.\n\n" +f"Identity: {identity['hash']}\n",encoding="utf-8")
    print("PREPARED",panel["status"],"anchors",panel.get("anchors"),"queries",panel.get("reserved_queries"),flush=True)
    return manifest


def run_one(condition,seed,batches,context,calendar,manifest,cfg,directory,deadline):
    record = {"condition":condition,"training_seed":seed,"status":"NOT_RUN","finite":False}
    if time.perf_counter()>=deadline:
        return {**record,"reason":"global wall budget exhausted"}
    model = GGNNLikeModel(seed)
    if state_hash(model)!=manifest["initial_state_hashes"][str(seed)]:
        raise ValueError("frozen initialization changed")
    assert model.parameter_count==cfg["parameters"]
    record.update(initial_state_hash=state_hash(model),parameters=model.parameter_count,
                  data_hashes={name:batch_hashes(batch) for name,batch in batches.items()})
    optimizer = torch.optim.AdamW(model.parameters(),lr=cfg["lr"],betas=tuple(cfg["betas"]),eps=cfg["eps"],weight_decay=cfg["weight_decay"])
    status,completed,curve,times = "COMPLETE",0,[],[]
    begin = time.perf_counter()
    process = psutil.Process()
    peak = process.memory_info().rss
    for selected in calendar:
        if time.perf_counter()>=deadline:
            status="RESOURCE_LIMIT"
            break
        optimizer.zero_grad(set_to_none=True)
        part={name:batches["train"][name][selected] for name in ("inputs","output","target")}
        tick=time.perf_counter()
        logits=predictions(model,part,context,cfg["steps"])
        loss=F.binary_cross_entropy_with_logits(logits,part["target"])
        if not torch.isfinite(loss):
            status="NUMERICAL_FAILURE_UNVERIFIED"
            break
        loss.backward()
        norm=torch.nn.utils.clip_grad_norm_(model.parameters(),cfg["gradient_clip"])
        if not torch.isfinite(norm):
            status="NUMERICAL_FAILURE_UNVERIFIED"
            break
        optimizer.step()
        times.append(time.perf_counter()-tick)
        completed+=1
        peak=max(peak,process.memory_info().rss)
        if completed==1 or completed%25==0:
            curve.append({"update":completed,"optimization_loss":float(loss.detach()),"preclip_gradient_norm":float(norm)})
    record.update(status=status,updates_completed=completed,optimization_curve=curve,final_state_hash=state_hash(model),
                  median_update_seconds=float(np.median(times)) if times else None)
    if time.perf_counter()<deadline:
        for name,batch in batches.items():
            if time.perf_counter()>=deadline:
                if name=="AUX_OLD":
                    record[name]={"status":"AUX_NOT_MEASURED","reason":"global deadline prevents auxiliary measurement"}
                break
            record[name]=measure(model,batch,context,cfg,"b0")
        record["finite"]=bool(all(name in record and record[name]["finite"] for name in ("train","SS","UU"))
                              and all(torch.isfinite(p).all() for p in model.parameters()))
    if time.perf_counter()>=deadline:
        record["status"]="RESOURCE_LIMIT"
    if "AUX_OLD" not in record:
        record["AUX_OLD"]={"status":"AUX_NOT_MEASURED","reason":"global deadline or incomplete final measurement"}
    record.update(seconds_including_measurement=time.perf_counter()-begin,RSS_peak_bytes_sampled=max(peak,process.memory_info().rss))
    out=directory/f"{condition.lower()}_s{seed}"
    out.mkdir(parents=True,exist_ok=False)
    torch.save({"model":model.state_dict(),"optimizer":optimizer.state_dict(),"completed_updates":completed,"frozen_calendar":calendar},out/"final_checkpoint.pt")
    record["checkpoint_sha256"]=file_hash(out/"final_checkpoint.pt")
    write_json(out/"results.json",record)
    print(condition,seed,record["status"],completed,"scores",{name:record.get(name,{}).get("accuracy") for name in ("train","SS","UU")},flush=True)
    return record


def execute(cfg,directory,begin):
    manifest_path=directory/"preregistration.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["status"]!="PREPARED":
        raise ValueError("DIAGNOSTIC_UNAVAILABLE: no eligible frozen preparation")
    identity=explicit_identity(cfg)
    if identity["hash"]!=manifest["identity"]["hash"] or digest(cfg)!=manifest["protocol_hash"]:
        raise ValueError("frozen preparation source/config/runtime changed; never execute silently")
    if (directory/"execution_started.json").exists():
        raise FileExistsError("execution already started: no retries or overwritten evidence")
    context=graph_context(Geometry.load(ROOT/"artifacts/geometry/grid_N400_g1101.npz"))
    current={"coordinates":array_hash(context["geometry"].points),"edges":context["edges_hash"],"ports":context["ports"].digest}
    if current!=manifest["geometry"]:
        raise ValueError("frozen substrate changed")
    panel=manifest["panel"]
    batches={**{name:bind_panel(context,triples) for name,triples in panel["panels"].items()},"SS":bind_panel(context,panel["SS"]),"UU":bind_panel(context,panel["UU"]),
             "AUX_OLD":bind_panel(context,manifest["auxiliary_old_panel"]["triples"])}
    if {name:batch_hashes(batch) for name,batch in batches.items()}!=manifest["dataset_hashes"]:
        raise ValueError("frozen input/target/cases bytes changed")
    write_json(directory/"execution_started.json",{"UTC":utc_now(),"identity":identity["hash"],"deadline_seconds":cfg["wall_budget_seconds"],
                                               "prepared_manifest_sha256":file_hash(manifest_path)})
    deadline=begin+cfg["wall_budget_seconds"]
    records=[]
    for condition,seed in cfg["run_order"]:
        subsets={"train":batches[condition],"SS":batches["SS"],"UU":batches["UU"],"AUX_OLD":batches["AUX_OLD"]}
        records.append(run_one(condition,seed,subsets,context,np.asarray(manifest["calendars"][str(seed)],dtype=np.int64),manifest,cfg,directory,deadline))
    assert explicit_identity(cfg)["hash"]==identity["hash"],"frozen dependency changed during execution"
    updates=hypothesis_updates(records,manifest["hypotheses"])
    result={"status":"COMPLETE" if all(r["status"]!="RESOURCE_LIMIT" for r in records) else "RESOURCE_LIMIT",
            "stage":cfg["stage"],"identity":identity,"records":records,"primary_condition":"BALANCED",
            "gates":{condition:gate(records,condition,cfg["gate_accuracy"]) for condition in cfg["conditions"]},
            "H_R_ordinal_updates":updates,"seconds_actual":time.perf_counter()-begin,"completed_UTC":utc_now(),
            "architecture_evidence":False,"test_opened":False,"H1_H6_updated":False,"architecture_C_updated":False,
            "original_pilot_unchanged":True,"XOR_MHU_remote":{"status":"NOT_RUN","reason":"outside this frozen four-run experiment"}}
    result["auxiliary_old_panel_comparability"]=manifest["auxiliary_old_panel"]
    write_json(directory/"results.json",result)
    write_json(directory/"H_R_ordinal_updates.json",updates)
    print("gates",result["gates"],"H-R",{name:value["direction"] for name,value in updates["updates"].items()},flush=True)
    return result


def main(argv=None):
    begin=time.perf_counter()
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare-only",action="store_true")
    group.add_argument("--execute-prepared",action="store_true")
    parser.add_argument("--output",type=Path,default=ROOT/"artifacts/role_coverage/v1")
    args=parser.parse_args(argv)
    cfg=json.loads((ROOT/"configs/role_coverage_v1.json").read_text(encoding="utf-8"))
    if not (ROOT/cfg["hypotheses_file"]).exists():
        raise FileNotFoundError("hypotheses must be registered before preparation")
    torch.set_num_threads(cfg["cpu_threads"])
    torch.use_deterministic_algorithms(True)
    return prepare(cfg,args.output,begin) if args.prepare_only else execute(cfg,args.output,begin)


if __name__=="__main__":
    main()
