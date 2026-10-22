"""Explicitly authorized, bounded CUDA scaling job. No historical runs altered."""
from __future__ import annotations
import argparse, copy, hashlib, json, math, os, sys, time, traceback
from pathlib import Path
import numpy as np
import torch
from torch import nn
from scipy.spatial import cKDTree
from .scale3d_geometry import generate
from .scale3d_report import write_report

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def publish(path, value, *, exclusive=False):
    path = Path(path)
    text = json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False)+"\n"
    if exclusive:
        with path.open("x", encoding="utf-8") as f: f.write(text)
    else:
        temporary = path.with_suffix(path.suffix+".next")
        temporary.write_text(text, encoding="utf-8")
        temporary.replace(path)


def periodic_features(x):
    return torch.cat((torch.sin(2*math.pi*x), torch.cos(2*math.pi*x)), -1)


class Block(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.norm = nn.LayerNorm(width)
        self.message = nn.Linear(width, width, bias=False)
        self.film = nn.Embedding(5, 2*width)
        self.mlp = nn.Sequential(nn.Linear(width, 4*width), nn.GELU(), nn.Linear(4*width, width))
        nn.init.zeros_(self.film.weight)

    def forward(self, h, adjacency, labels):
        B, N, D = h.shape
        pooled = torch.sparse.mm(adjacency, h.permute(1,0,2).reshape(N,B*D)).reshape(N,B,D).permute(1,0,2)
        gamma, beta = self.film(labels).chunk(2,-1)
        z = (self.norm(h)+self.message(pooled))*(1+.1*torch.tanh(gamma))+.1*beta
        return h+self.mlp(z)/math.sqrt(8)


class SpatialNetwork(nn.Module):
    def __init__(self, width=256, layers=8):
        super().__init__()
        self.input = nn.Linear(15,width)
        self.blocks = nn.ModuleList([Block(width) for _ in range(layers)])
        self.head = nn.Sequential(nn.LayerNorm(width+9),nn.Linear(width+9,width),nn.GELU(),nn.Linear(width,5))

    def forward(self, observations, geometry, queries, task):
        B,N = observations.shape
        labels = geometry["labels"]
        types = nn.functional.one_hot(labels,5).float()
        condition = nn.functional.one_hot(torch.tensor(task,device=observations.device),3).float()
        fixed = torch.cat((types,periodic_features(geometry["points"]),condition.expand(N,3)), -1)
        h = self.input(torch.cat((observations[...,None],fixed.expand(B,N,14)), -1))
        for block in self.blocks: h=block(h,geometry["adjacency"],labels)
        ids,weights = geometry["query_ids"],geometry["query_weights"]
        pooled=(h[:,ids,:]*weights[None,:,:,None]).sum(2)
        qfixed=torch.cat((periodic_features(queries),condition.expand(len(queries),3)),-1)
        return self.head(torch.cat((pooled,qfixed.expand(B,len(queries),9)),-1))


def graph_data(points, labels, queries, degree, device):
    x=points.detach().cpu().numpy().astype(np.float64)%1
    q=queries.detach().cpu().numpy()
    tree=cKDTree(x,boxsize=1)
    distances,ids=tree.query(x,k=degree+1,workers=1)
    # Remove by ID rather than assuming self is first when nodes coincide.
    mask=ids!=np.arange(len(x))[:,None]
    ids=np.array([row[m][:degree] for row,m in zip(ids,mask)])
    distances=np.array([row[m][:degree] for row,m in zip(distances,mask)])
    scale=max(float(np.median(distances)),1e-8)
    weights=np.exp(-.5*(distances/scale)**2);weights/=weights.sum(1,keepdims=True)
    rows=np.repeat(np.arange(len(x)),degree)
    adj=torch.sparse_coo_tensor(torch.tensor(np.stack((rows,ids.ravel())),device=device),
          torch.tensor(weights.ravel(),dtype=torch.float32,device=device),(len(x),len(x)),check_invariants=True).coalesce()
    qd,qi=tree.query(q,k=degree,workers=1)
    qw=np.exp(-.5*(qd/scale)**2);qw/=qw.sum(1,keepdims=True)
    result={"points":points.to(device),"labels":labels.to(device),"adjacency":adj,
            "query_ids":torch.tensor(qi,device=device),"query_weights":torch.tensor(qw,dtype=torch.float32,device=device)}
    report={"nodes":len(x),"edges":int(adj._nnz()),"degree":degree,
        "neighbor_radius_mean":float(distances[:,-1].mean()),"neighbor_radius_p95":float(np.quantile(distances[:,-1],.95)),
        "query_radius_mean":float(qd[:,-1].mean()),
        "query_missing_type_fraction":[float(np.mean(~np.any(labels.cpu().numpy()[qi]==c,axis=1))) for c in range(5)]}
    return result,report


def task_modes(config, device):
    rng=np.random.default_rng(config["mode_seed"])
    result=[]
    for lower,upper in config["bands"]:
        a=np.array([(i,j,k) for i in range(-upper,upper+1) for j in range(-upper,upper+1)
          for k in range(-upper,upper+1) if lower**2<=i*i+j*j+k*k<=upper**2 and
          (i>0 or i==0 and j>0 or i==j==0 and k>0)],dtype=np.int64)
        take=min(config["modes_per_task"],len(a))
        result.append(torch.tensor(a[rng.choice(len(a),take,replace=False)],device=device,dtype=torch.float32))
    return result


def targets(fields, task):
    if task<2:return fields
    return torch.stack((fields[...,0]*fields[...,1],fields[...,1]*fields[...,2],
       fields[...,2]*fields[...,3],fields[...,3]*fields[...,4],fields[...,0]*fields[...,2]*fields[...,4]),-1)


def features_at(points,modes):
    phase=2*math.pi*(points@modes.T)
    return torch.cat((phase.cos(),phase.sin()),-1)


def world(seed, B, M, device):
    rng=torch.Generator(device=device).manual_seed(seed)
    return torch.randn((B,5,2*M),generator=rng,device=device)/math.sqrt(M)


def observations(coefficients, phi, labels):
    values=torch.einsum("bcd,nd->bnc",coefficients,phi)
    return values.gather(2,labels[None,:,None].expand(len(coefficients),-1,1)).squeeze(-1)


@torch.no_grad()
def evaluate(models,geometries,phis,qphis,queries,modes,config,seed):
    scores={name:[] for name in models}
    for model in models.values():model.eval()
    for task in range(3):
        errors={name:[] for name in models}
        for start in range(0,config["evaluation_worlds"],config["batch"]):
            B=min(config["batch"],config["evaluation_worlds"]-start)
            coeff=world(seed+task*100000+start,B,len(modes[task]),queries.device)
            y=targets(torch.einsum("bcd,qd->bqc",coeff,qphis[task]),task)
            for name,model in models.items():
                obs=observations(coeff,phis[name][task],geometries[name]["labels"])
                pred=model(obs,geometries[name],queries,task)
                errors[name].extend(((pred-y)**2).mean((1,2)).cpu().tolist())
        for name in models:scores[name].append({"task":task,"MSE":float(np.mean(errors[name])),"world_MSE":errors[name]})
    return scores


def run(config_path,output):
    config=json.loads(config_path.read_text(encoding="utf-8"))
    output.mkdir(parents=True,exist_ok=True)
    device=torch.device("cuda")
    if not torch.cuda.is_available():raise RuntimeError("CUDA required: do not substitute a CPU run")
    torch.set_num_threads(8)
    torch.cuda.set_per_process_memory_fraction(config["VRAM_fraction"])
    torch.backends.cuda.matmul.allow_tf32=True
    torch.manual_seed(config["master_seed"])
    source_paths=[Path(__file__),ROOT/"src/larp/scale3d_geometry.py",ROOT/"src/larp/scale3d_runner.py",
                  ROOT/"src/larp/scale3d_report.py",ROOT/"docs/experiments/SCALE3D_V1_PROTOCOL.md",config_path]
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
