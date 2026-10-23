"""LARP AB30-TS. Deterministic causal one-step forecasting; explicit chronological test gate."""
import argparse, json, hashlib
from pathlib import Path
import numpy as np
import statsmodels.api as sm
from scipy.stats import norm

NAMES=['nile','sunspots','co2','realgdp','elnino','interest']
ARMS=[('persistence','mean16'),('mean4','mean16'),('ewma03','mean4'),('trend8','persistence'),('adaptive','fixed')]

def load(name):
    if name=='nile': y=sm.datasets.nile.load_pandas().data['volume'].to_numpy()
    elif name=='sunspots': y=sm.datasets.sunspots.load_pandas().data['SUNACTIVITY'].to_numpy()
    elif name=='co2': y=sm.datasets.co2.load_pandas().data['co2'].ffill().to_numpy()
    elif name=='realgdp': y=np.log(sm.datasets.macrodata.load_pandas().data['realgdp'].to_numpy())
    elif name=='elnino': y=sm.datasets.elnino.load_pandas().data.iloc[:,1:13].to_numpy().reshape(-1)
    elif name=='interest': y=sm.datasets.interest_inflation.load_pandas().data['R'].to_numpy()
    else: raise ValueError(name)
    y=np.asarray(y,float)
    assert len(y)>=80 and np.isfinite(y).all()
    return y

def forecast(y,development_window=None):
    n=len(y); p={k:np.full(n,np.nan) for k in ['persistence','mean4','mean16','ewma03','trend8','adaptive','fixed']}
    ema=float(y[0]); errs={k:np.full(n,np.nan) for k in ['persistence','mean4','ewma03']}
    for t in range(1,n):
        if t>=20:
            p['persistence'][t]=y[t-1]
            p['mean4'][t]=np.mean(y[t-4:t])
            p['mean16'][t]=np.mean(y[t-16:t])
            a=np.arange(8,dtype=float); v=y[t-8:t]
            slope=np.sum((a-a.mean())*(v-v.mean()))/np.sum((a-a.mean())**2)
            p['trend8'][t]=v.mean()+slope*(8-a.mean())
            p['ewma03'][t]=ema
            if t>=33:
                candidates=['persistence','mean4','ewma03']
                scores=np.asarray([np.nanmean(errs[k][t-12:t]) for k in candidates])
                scale=max(float(np.median(scores)),1e-9)
                weights=np.exp(-scores/scale); weights/=weights.sum()
                p['adaptive'][t]=np.dot(weights,[p[k][t] for k in candidates])
            for k in errs: errs[k][t]=abs(y[t]-p[k][t])
        ema=.3*y[t]+.7*ema
    # fixed expert chosen ONLY on the early development segment (not the validation or test sets)
    lo,hi=development_window if development_window is not None else (max(33,int(.35*n)),int(.50*n))
    choice=min(errs,key=lambda k:np.nanmean(errs[k][lo:hi]))
    p['fixed']=p[choice].copy()
    return p,choice

def split(n):
    return {'development':[max(33,int(.35*n)),int(.50*n)],'validation':[int(.50*n),int(.75*n)],'test':[int(.75*n),n]}

def bootstrap_delta(delta,seed=0,b=1499):
    d=np.asarray(delta,float);n=len(d);block=max(2,int(n**(1/3)))
    rng=np.random.default_rng(seed)
    values=np.empty(b)
    for j in range(b):
        inds=[]
        while len(inds)<n:
            start=int(rng.integers(0,n));inds.extend(((start+np.arange(block))%n).tolist())
        values[j]=np.mean(d[np.asarray(inds[:n])])
    lo,hi=np.percentile(values,[2.5,97.5]);return [float(lo),float(hi)]

def run(spec,phase):
    name=spec['dataset']; full=load(name); partitions=split(len(full)); window=partitions[phase]
    y=full[:partitions['validation'][1]] if phase=='validation' else full
    pred,choice=forecast(y,partitions['development'])
    start,end=window; a,b=spec['a'],spec['b']; valid=np.arange(start,end)
    assert valid.min()>=33 and np.isfinite(pred[a][valid]).all() and np.isfinite(pred[b][valid]).all()
    d=np.abs(y[valid]-pred[a][valid])-np.abs(y[valid]-pred[b][valid])
    scale=np.mean(np.abs(y[valid]-pred['persistence'][valid]))
    return dict(id=spec['id'],dataset=name,phase=phase,a=a,b=b,choice=choice,n=int(len(valid)),n_series=int(len(full)),window=window,raw_delta_mae=float(np.mean(d)),normalized_delta=float(np.mean(d)/max(scale,1e-12)),mae_a=float(np.mean(np.abs(y[valid]-pred[a][valid]))),mae_b=float(np.mean(np.abs(y[valid]-pred[b][valid]))),ci95=bootstrap_delta(d,seed=int(spec['id'][1:])*111+(0 if phase=='validation' else 404)),pred_positive=bool(np.mean(d)<0),data_sha256=hashlib.sha256(y.astype('<f8').tobytes()).hexdigest(),direction='A_lower_MAE',scope='REAL_OBSERVED_HISTORICAL_SERIES',external_replication='NOT_CLAIMED')

def main():
    p=argparse.ArgumentParser();p.add_argument('spec');p.add_argument('--phase',choices=['validation','test'],default='validation');p.add_argument('--output',required=True);args=p.parse_args()
    spec=json.loads(Path(args.spec).read_text(encoding='utf8'))
    out=run(spec,args.phase);dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print(out['id'],out['phase'],out['normalized_delta'],out['ci95'])

if __name__=='__main__':main()
