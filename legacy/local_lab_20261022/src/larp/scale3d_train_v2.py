"""Fresh v2 scaling run; retain the frozen v1 network and task implementation."""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
from pathlib import Path
import time
import traceback

import numpy as np
import torch

from .scale3d_train import (
    SpatialNetwork, evaluate, features_at, graph_data, observations,
    publish, sha, targets, task_modes, world,
)
from .scale3d_geometry_v2 import generate
from .scale3d_report_v2 import write_report

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_SOURCE_PATHS = (
    "src/larp/scale3d_train.py",
    "src/larp/scale3d_geometry.py",
    "src/larp/scale3d_report.py",
    "src/larp/scale3d_train_v2.py",
    "src/larp/scale3d_geometry_v2.py",
    "src/larp/scale3d_runner_v2.py",
    "src/larp/scale3d_report_v2.py",
    "docs/experiments/SCALE3D_V2_PROTOCOL.md",
)


def validate_config(config):
    if config.get("version") != "scale3d_v2":
        raise ValueError("This trainer requires version scale3d_v2; v1 is frozen")
    if config.get("require_finite_MHU_pass") is not True:
        raise ValueError("The finite MHU gate must remain enabled")
    if config.get("full_band_exact_audit") is not True:
        raise ValueError("The full exact low-band audit must remain enabled")


def verify_generator_qualification(config):
    path=(ROOT/config["generator_qualification"]).resolve()
    if not path.is_relative_to(ROOT.resolve()):raise ValueError("Qualification must stay inside project")
    result=json.loads(path.read_text(encoding="utf-8"))
    records=[r for r in result["records"] if r["version"]=="v2"]
    expected={(N,seed) for N in (16384,32768) for seed in (9107,9108)}
    if result["status"]!="PASS" or len(records)!=4 or {(r["N"],r["seed"]) for r in records}!=expected or not all(r["pass"] for r in records):
        raise ValueError("Complete large-geometry qualification required before training")
    protocol=json.loads((path.parent/"protocol.json").read_text(encoding="utf-8"))
    for name,digest in protocol["source_sha256"].items():
        if sha(ROOT/name)!=digest:raise ValueError("Generator changed after qualification")


def frozen_source_paths(config, config_path):
    declared = config.get("source_paths", list(REQUIRED_SOURCE_PATHS))
    if not isinstance(declared, list) or not all(isinstance(p, str) for p in declared):
        raise ValueError("source_paths must be a list of relative paths")
    if not set(REQUIRED_SOURCE_PATHS).issubset(declared):
        raise ValueError("source_paths omits a required dependency")
    paths = []
    for name in declared:
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT.resolve()):
            raise ValueError("source_paths must stay inside the project")
        if not path.is_file():
            raise FileNotFoundError(path)
        if path not in paths:
            paths.append(path)
    config_path = Path(config_path).resolve()
    if not config_path.is_relative_to(ROOT.resolve()):
        raise ValueError("The configuration must stay inside the project")
    if config_path not in paths:
        paths.append(config_path)
    return paths


def run(config_path,output):
    config=json.loads(config_path.read_text(encoding="utf-8"))
    validate_config(config)
    verify_generator_qualification(config)
    output.mkdir(parents=True,exist_ok=True)
    device=torch.device("cuda")
    if not torch.cuda.is_available():raise RuntimeError("CUDA required: do not substitute a CPU run")
    torch.set_num_threads(8)
    torch.cuda.set_per_process_memory_fraction(config["VRAM_fraction"])
    torch.backends.cuda.matmul.allow_tf32=True
    torch.manual_seed(config["master_seed"])
    source_paths=frozen_source_paths(config,config_path)
    protocol={"config":config,"files":{str(p.relative_to(ROOT)):sha(p) for p in source_paths},
        "torch":torch.__version__,"cuda_runtime":torch.version.cuda,"GPU":torch.cuda.get_device_name(),
        "pid":os.getpid(),"ppid":os.getppid(),"precision":"FP32 with TF32 permitted; geometry audit FP64",
        "status":"FROZEN_BEFORE_GENERATION_AND_TRAINING","historical_priors_updated":False}
    publish(output/"protocol.json",protocol,exclusive=True)
    started=time.monotonic();deadline=started+config["maximum_job_seconds"]
    query_rng=np.random.default_rng(config["query_seed"])
    queries=torch.tensor(query_rng.random((config["queries"],3)),dtype=torch.float32,device=device)
    test_query_rng=np.random.default_rng(config["test_query_seed"])
    test_queries=torch.tensor(test_query_rng.random((config["queries"],3)),dtype=torch.float32,device=device)
    modes=task_modes(config,device)
    qphis=[features_at(queries,m) for m in modes]
    test_qphis=[features_at(test_queries,m) for m in modes]
    results=[]
    for N in config["sizes"]:
      for seed in config["geometry_seeds"]:
        if time.monotonic()>=deadline:break
        pair=output/f"N{N}_g{seed}";pair.mkdir(exist_ok=False)
        pair_deadline=min(deadline,time.monotonic()+config["maximum_triplet_seconds"])
        publish(output/"progress.json",{"status":"GENERATING_3D","N":N,"seed":seed,"pid":os.getpid()})
        geometries,eval_geometries,georeports={},{},{}
        for name in config["arms"]:
            candidate=generate(seed,N,device,iterations=0 if name=="random" else config["geometry_iterations"],
                spectral=name=="mhu",chi=config["chi"],local_weight=config["local_weight"])
            p=candidate["coordinates"];z=candidate["labels"]
            np.savez_compressed(pair/f"{name}_geometry.npz",points=p.cpu().numpy(),labels=z.cpu().numpy())
            publish(pair/f"{name}_geometry.json",{k:v for k,v in candidate.items() if k not in ("coordinates","labels")},exclusive=True)
            geometries[name],georeports[name]=graph_data(p,z,queries,config["degree"],device)
            eval_ports,_=graph_data(p,z,test_queries,config["degree"],device)
            eval_geometries[name]={**geometries[name],"query_ids":eval_ports["query_ids"],"query_weights":eval_ports["query_weights"]}
            del eval_ports
            if name=="mhu" and not candidate["validation"]["finite_low_k_pass"]:
                break
        if len(geometries)!=len(config["arms"]):
            record={"N":N,"seed":seed,"status":"INVALID_MHU_CLAIM","training_updates":0}
            results.append(record);publish(pair/"result.json",record,exclusive=True)
            del geometries,eval_geometries,candidate,p,z
            torch.cuda.empty_cache()
            continue
        torch.manual_seed(config["master_seed"]+seed)
        template=SpatialNetwork(config["width"],config["layers"]).to(device)
        models={name:copy.deepcopy(template) for name in config["arms"]};del template
        optimizers={name:torch.optim.AdamW(model.parameters(),lr=config["learning_rate"],weight_decay=1e-4) for name,model in models.items()}
        phis={name:[features_at(g["points"],m) for m in modes] for name,g in geometries.items()}
        publish(pair/"matching.json",{"parameter_counts":{name:sum(p.numel() for p in m.parameters()) for name,m in models.items()},
            "common_initialization":True,"graph":georeports,"batch":config["batch"],
            "evaluation_uses_new_worlds_and_queries":True,"train_query_seed":config["query_seed"],
            "test_query_seed":config["test_query_seed"]},exclusive=True)
        last_step=0;checks=[]
        order=config["arms"] if seed%2 else list(reversed(config["arms"]))
        training_seconds={name:0. for name in models}
        torch.cuda.reset_peak_memory_stats()
        for step in range(1,config["updates"]+1):
            if time.monotonic()>=pair_deadline:break
            rng=np.random.default_rng(config["master_seed"]+step)
            task=0 if step<=300 else int(rng.choice(2,p=[.2,.8])) if step<=600 else int(rng.choice(3,p=[.1,.2,.7]))
            coeff=world(config["master_seed"]*100000+seed*10000+step,config["batch"],len(modes[task]),device)
            y=targets(torch.einsum("bcd,qd->bqc",coeff,qphis[task]),task)
            loss_values={}
            for name in order:
                model=models[name];model.train();optimizers[name].zero_grad(set_to_none=True)
                obs=observations(coeff,phis[name][task],geometries[name]["labels"])
                before=time.perf_counter()
                pred=model(obs,geometries[name],queries,task)
                loss=(pred-y).square().mean()
                if not torch.isfinite(loss):raise RuntimeError("Nonfinite training loss; preserve failure")
                loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.);optimizers[name].step()
                torch.cuda.synchronize();training_seconds[name]+=time.perf_counter()-before
                loss_values[name]=float(loss.detach())
            last_step=step
            if step%20==0:
                publish(output/"progress.json",{"status":"TRAINING","N":N,"seed":seed,"paired_step":step,
                    "curriculum_task":task,"loss":loss_values,"pid":os.getpid(),
                    "allocated_VRAM_GiB":torch.cuda.max_memory_allocated()/2**30,"elapsed_seconds":time.monotonic()-started})
            if step in config["checkpoints"]:
                scores=evaluate(models,eval_geometries,phis,test_qphis,test_queries,modes,config,config["evaluation_seed"])
                evaluation={"step":step,"scores":scores};checks.append(evaluation)
                publish(pair/f"evaluation_u{step}.json",evaluation,exclusive=True)
                with (pair/f"checkpoint_u{step}.pt").open("xb") as f:
                    torch.save({"step":step,"models":{name:m.state_dict() for name,m in models.items()},
                        "optimizers":{name:o.state_dict() for name,o in optimizers.items()},"config":config,
                        "torch_rng":torch.get_rng_state(),"cuda_rng":torch.cuda.get_rng_state()},f)
        status="COMPLETE" if last_step==config["updates"] else "BUDGET_LIMIT_MATCHED_STEPS"
        record={"N":N,"seed":seed,"status":status,"training_updates":last_step,"evaluations":checks,
                "training_seconds":training_seconds,"peak_VRAM_GiB":torch.cuda.max_memory_allocated()/2**30}
        publish(pair/"result.json",record,exclusive=True);results.append(record)
        del models,optimizers,geometries,eval_geometries,phis,candidate,p,z
        torch.cuda.empty_cache()
        publish(output/"partial_results.json",{"records":results,"status":"RUNNING"})
    common=set(config["checkpoints"])
    for r in results:common &= {e["step"] for e in r.get("evaluations",[])}
    expected={(N,seed) for N in config["sizes"] for seed in config["geometry_seeds"]}
    if {(r["N"],r["seed"]) for r in results}!=expected:common=set()
    complete=len(results)==len(config["sizes"])*len(config["geometry_seeds"]) and all(r["status"]=="COMPLETE" for r in results)
    final={"status":"COMPLETE" if complete else "INCOMPLETE_OR_INVALID","records":results,
       "config":config,
       "common_scale_endpoint":max(common) if common else None,"seconds":time.monotonic()-started,
       "interpretation":"Exploratory end-to-end sensor-density scaling; not pure neural-computation causality or asymptotic MHU proof",
       "historical_priors_updated":False}
    publish(output/"results.json",final,exclusive=True)
    write_report(final,output)
    publish(output/"progress.json",{"status":final["status"],"pid":os.getpid(),"seconds":final["seconds"]})


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    p.add_argument("--execute",action="store_true");a=p.parse_args()
    if not a.execute:print(a.config.read_text(encoding="utf-8"))
    else:
        try:run(a.config.resolve(),a.output.resolve())
        except BaseException as error:
            a.output.mkdir(parents=True,exist_ok=True)
            publish(a.output/"failure.json",{"status":"FAILED","error":repr(error),"traceback":traceback.format_exc(),"pid":os.getpid()})
            publish(a.output/"progress.json",{"status":"FAILED","error":repr(error),"pid":os.getpid()})
            raise
