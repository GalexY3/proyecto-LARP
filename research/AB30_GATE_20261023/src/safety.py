"""AB30-GATE: causal expert switching; no test reads before a preregistered unseal."""
import argparse, json, hashlib
from pathlib import Path
import numpy as np
from scipy.special import expit
from legacy_engine import load as load_legacy, forecast, split, bootstrap_delta
import statsmodels.api as sm

DATASETS=("nile","sunspots","co2","elnino","unemployment","inflation")
EXPERTS=("persistence","mean4","ewma03")

def observations(name):
    if name=="unemployment":
        y=sm.datasets.macrodata.load_pandas().data["unemp"].to_numpy(float)
    elif name=="inflation":
        y=sm.datasets.macrodata.load_pandas().data["infl"].to_numpy(float)
    else:
        y=load_legacy(name)
    assert np.isfinite(y).all() and len(y)>=100
    return np.asarray(y, float)

def ar1(past):
    x=past[:-1]; z=past[1:]
    vx=np.mean((x-x.mean())**2)
    beta=np.mean((x-x.mean())*(z-z.mean()))/max(vx,1e-12)
    beta=float(np.clip(beta,-1.15,1.15))
    return float(z.mean()+beta*(past[-1]-x.mean()))

def methods(y,dev):
    n=len(y)
    baseline,fixedchoice=forecast(y,dev)
    p={k:np.full(n,np.nan) for k in ["fixed","winner","gate","hedge","equal","shrink","ar32","softgate"]}
    p["fixed"]=baseline["fixed"].copy()
    scale=max(float(np.nanmedian(np.abs(np.diff(y[:max(dev[1],40)])))),1e-9)
    for t in range(max(40,dev[0]),n):
        vals=np.array([baseline[k][t] for k in EXPERTS])
        if not np.all(np.isfinite(vals)):
            continue
        lo=max(20,t-24)
        history=np.arange(lo,t)
        # only realized past outcomes are used; no scoring on the current target
        error=np.vstack([y[history]-baseline[k][history] for k in EXPERTS]).T
        losses=np.abs(error)
        if not np.isfinite(losses).all():
            continue
        score=losses.mean(axis=0)
        winner=int(np.argmin(score))
        p["winner"][t]=vals[winner]
        p["equal"][t]=float(vals.mean())
        w=np.exp(-score/max(np.median(score),scale*0.05,1e-9))
        w/=w.sum()
        p["hedge"][t]=float(w@vals)
        # Error-second-moment shrinkage, simplex-constrained by clipping
        gram=(error.T@error)/len(history)
        ridge=max(float(np.trace(gram))/3,1e-8)*1.0
        try:
            ww=np.linalg.solve(gram+ridge*np.eye(3),np.ones(3))
        except np.linalg.LinAlgError:
            ww=np.ones(3)
        ww=np.maximum(ww,0)
        ww=ww/max(ww.sum(),1e-12)
        p["shrink"][t]=float(ww@vals)
        # evaluate a switch vs the development-only fixed expert
        f_idx=EXPERTS.index(fixedchoice)
        gap=losses[:,winner]-losses[:,f_idx]
        effect=float(gap.mean())
        # Newey-West lag3 estimate of SE of the recent difference
        gc=gap-gap.mean()
        var=float(gc@gc)/len(gc)
        for j in range(1,min(3,len(gc)-1)+1):
            var+=2*(1-j/4)*float(gc[j:]@gc[:-j])/len(gc)
        se=float(np.sqrt(max(var,0)/len(gc)))
        allow=effect < -1.645*se and winner != f_idx
        p["gate"][t]=float(vals[winner] if allow else vals[f_idx])
        blend=float(expit(-effect/max(se,scale*.05,1e-9)))
        p["softgate"][t]=float(blend*vals[winner]+(1-blend)*vals[f_idx])
        p["ar32"][t]=ar1(y[t-32:t])
    return p,fixedchoice

def run(spec,phase):
    name=spec["dataset"]
    full=observations(name)
    sp=split(len(full))
    end=sp["validation"][1] if phase=="validation" else len(full)
    y=full[:end]
    pred,fixedchoice=methods(y,sp["development"])
    start,stop=sp[phase]
    pos=np.arange(start,stop)
    a,b=spec["a"],spec["b"]
    assert len(pos)>=20 and np.isfinite(pred[a][pos]).all() and np.isfinite(pred[b][pos]).all()
    la=np.abs(y[pos]-pred[a][pos]);lb=np.abs(y[pos]-pred[b][pos])
    delta=la-lb
    pscale=max(float(np.mean(np.abs(y[pos]-pred["fixed"][pos]))),1e-9)
    return {
        "id":spec["id"],"phase":phase,"dataset":name,"a":a,"b":b,
        "n":len(pos),"time_indices":[int(start),int(stop)],"fixed_expert":fixedchoice,
        "mae_a":float(la.mean()),"mae_b":float(lb.mean()),
        "delta_mae":float(delta.mean()),"normalized_delta":float(delta.mean()/pscale),
        "ci95_block":bootstrap_delta(delta,int(spec["id"][1:])*191+(0 if phase=="validation" else 811),b=599),
        "source_dataset_sha256":hashlib.sha256(full.astype("<f8").tobytes()).hexdigest(),
        "raw_loss_delta":delta.tolist(),"not_external_confirmation":True
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--phase",choices=("validation","test"),default="validation")
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    spec=json.loads(Path(args.spec).read_text())
    result=run(spec,args.phase)
    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(result["id"],result["phase"],round(result["delta_mae"],6),result["ci95_block"])

if __name__=="__main__":
    main()
