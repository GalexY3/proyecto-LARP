"""LARP AB-R L01-L20: supervised learned routing and neural decoding; finite proxy geometry only.
Parent geometry generator: ab30_functional.py frozen in repository, NOT original native avian NPZ.
Use same 400 sensor counts, 6 outgoing edges; independent training/validation/test FIELD seeds.
A learned graph uses target-field information ONLY from train; other graphs unsupervised.
No actual retinal data, no Wei competitor, no claim of thermodynamic MHU or clinical perception.
"""
from __future__ import annotations
import sys, os, json, hashlib, platform, time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from scipy.spatial import cKDTree
import ab30_functional as prev

N=400; DEG=6
GSEEDS=[3011,3023]
TRAIN_SEEDS=list(range(50101,50125))
VAL_SEEDS=list(range(51101,51107))
TEST_SEEDS=list(range(52101,52117))
CONTEXTS=['low','high','correlated','anticorrelated','localized']
SHIFTS=['clean','drop20','rare_drop40','noise15']
METHODS=['grid_knn','cvt_knn','mhu_knn','grid_type','cvt_type','mhu_type','grid_learned','cvt_learned','mhu_learned']
EPOCHS=12; LR=.006; L2=.005; HIDDEN=24

def hashfile(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def graph_learned(p,lab,context,train):
    # Fit directed edges on TRAIN targets using same physical sensing: each node has one modality.
    # Scores are abs correlation and modest distance penalty. Freeze before VAL/TEST.
    measured=np.stack([f[np.arange(N),lab] for f,w,t,v in train])
    targets=np.stack([target for f,w,target,v in train])
    X=measured-measured.mean(0);Y=targets-targets.mean(0)
    cross=Y.T@X/(len(train)-1)
    cov=abs(cross)/(np.maximum(Y.std(0)[:,None]*X.std(0)[None,:],1e-8))
    d=np.sqrt(prev.distance(p,p));scores=cov-0.04*d
    np.fill_diagonal(scores,-np.inf)
    # OMP-lite greedy residual score with type redundancy penalty; cheap supervised routing control.
    out=np.empty((N,DEG),dtype=int)
    for i in range(N):
        s=scores[i].copy();picked=[]
        for q in range(DEG):
            j=int(np.argmax(s));picked.append(j)
            s[j]=-np.inf
            s[lab==lab[j]]-=0.04
        out[i]=picked
    return out

def feature(field,p,lab,edges,shift,seed):
    rng=np.random.default_rng(seed)
    observed=field[np.arange(N),lab].copy()
    retained=np.ones(N,dtype=bool)
    if shift=='drop20':retained=rng.random(N)>.20
    elif shift=='rare_drop40':retained[lab==4]=rng.random(np.sum(lab==4))>.40
    elif shift=='noise15':observed+=rng.normal(0,.15,N)
    d=prev.distance(p,p)
    # own measurement plus 6 graph edges; use nearest selected source for each type
    cand=np.column_stack([np.arange(N),edges])
    feats=np.zeros((N,15),dtype=np.float32)
    for c in range(5):
        avail=(lab[cand]==c)&retained[cand]
        dist=np.where(avail,d[np.arange(N)[:,None],cand],np.inf)
        ix=np.argmin(dist,axis=1)
        rows=np.arange(N);chosen=cand[rows,ix]
        good=np.isfinite(dist[rows,ix])
        feats[:,c]=np.where(good,observed[chosen],0.)
        feats[:,5+c]=np.where(good,np.sqrt(dist[rows,ix]),.71)
        feats[:,10+c]=good.astype(np.float32)
    return feats

class Decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(15,HIDDEN),nn.GELU(),nn.Linear(HIDDEN,HIDDEN),nn.GELU(),nn.Linear(HIDDEN,1))
    def forward(self,x):return self.net(x).squeeze(-1)

def create_data(p,lab,edges,context,seeds,shift):
    xx=[];yy=[];variance=[]
    for seed in seeds:
        field,w,target,var=prev.field(p,context,seed)
        x=feature(field,p,lab,edges,shift, seed*101+17+SHIFTS.index(shift))
        xx.append(x);yy.append(target.astype(np.float32));variance.append(var)
    return np.stack(xx),np.stack(yy),np.array(variance)

def train_net(train_data,val_data,seed):
    X,Y,V=train_data;A,B,C=val_data
    torch.manual_seed(seed); net=Decoder(); opt=torch.optim.Adam(net.parameters(),lr=LR,weight_decay=L2)
    tx=torch.from_numpy(X.reshape(-1,15));ty=torch.from_numpy(Y.reshape(-1))
    va=torch.from_numpy(A.reshape(-1,15)); vb=torch.from_numpy(B.reshape(-1))
    best=float('inf'); state=None;best_epoch=-1
    rng=np.random.default_rng(seed+73)
    for epoch in range(EPOCHS):
        net.train();idx=rng.permutation(len(tx))
        for chunk in np.array_split(idx,8):
            pred=net(tx[chunk]);loss=(pred-ty[chunk]).square().mean()
            opt.zero_grad();loss.backward();opt.step()
        net.eval()
        with torch.no_grad(): val_loss=float((net(va)-vb).square().mean())
        if val_loss < best:
            best=val_loss;best_epoch=epoch
            state={k:v.clone() for k,v in net.state_dict().items()}
    net.load_state_dict(state)
    return net,best_epoch,best

def eval_net(net,data):
    X,Y,V=data
    with torch.no_grad():
        pred=net(torch.from_numpy(X.reshape(-1,15))).reshape(len(X),N).numpy()
    return ((pred-Y)**2).mean(axis=1)/(V+1e-12)

def main(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter()
    torch.set_num_threads(1)
    records=[];model_checks=[];geom_checks=[]
    for gseed in GSEEDS:
        lab=prev.labels_for_seed(gseed)
        xx,yy=np.meshgrid((np.arange(20)+.5)/20,(np.arange(20)+.5)/20)
        pts={'grid':np.column_stack([xx.ravel(),yy.ravel()]),'cvt':prev.cvt_geometry(gseed,lab),'mhu':prev.optimize_mhu(gseed,lab)}
        graphs={}
        for geom,p in pts.items():
            for policy in ('knn','type'):
                graphs[f'{geom}_{policy}']=prev.make_edges(p,lab,policy,gseed)
        for context in CONTEXTS:
            train_fields={geom:[prev.field(p,context,fs) for fs in TRAIN_SEEDS] for geom,p in pts.items()}
            for geom,p in pts.items():graphs[f'{geom}_learned']=graph_learned(p,lab,context,train_fields[geom])
            for method in METHODS:
                geom=method.split('_')[0];p=pts[geom];edges=graphs[method]
                assert edges.shape==(N,DEG) and all(len(set(row))==DEG for row in edges)
                assert np.all(edges!=np.arange(N)[:,None])
                d=np.sqrt(prev.distance(p,p)[np.arange(N)[:,None],edges])
                geom_checks.append(dict(geom_seed=gseed,context=context,method=method,mean_edge_length=float(d.mean()),mean_type_coverage=float(np.mean([(len(set(lab[[i]+list(edges[i])]))/5) for i in range(N)]))))
                train_data=create_data(p,lab,edges,context,TRAIN_SEEDS,'clean')
                val_data=create_data(p,lab,edges,context,VAL_SEEDS,'clean')
                net,epoch,valloss=train_net(train_data,val_data,seed=gseed*101+CONTEXTS.index(context)*100+METHODS.index(method))
                model_checks.append(dict(geom_seed=gseed,context=context,method=method,val_mse=valloss,best_epoch=epoch,parameters=sum(q.numel() for q in net.parameters())))
                for shift in SHIFTS:
                    test_data=create_data(p,lab,edges,context,TEST_SEEDS,shift)
                    nmse=eval_net(net,test_data)
                    for fs,val in zip(TEST_SEEDS,nmse):
                        records.append(dict(cycle=f'L{(CONTEXTS.index(context)*4+SHIFTS.index(shift)+1):02d}',geometry_seed=gseed,field_seed=fs,context=context,shift=shift,method=method,nmse=float(val)))
            print('DONE',gseed,context,'records',len(records),'elapsed',round(time.perf_counter()-start,1),flush=True)
    obj={'status':'SYNTHETIC_PROXY_ONLY','parent_code_sha256':hashfile(prev.__file__),'code_sha256':hashfile(__file__),
        'contexts':CONTEXTS,'shifts':SHIFTS,'methods':METHODS,'geometry_seeds':GSEEDS,'train_seeds':TRAIN_SEEDS,'val_seeds':VAL_SEEDS,'test_seeds':TEST_SEEDS,
        'degrees':DEG,'parameters_per_model':sum(q.numel() for q in Decoder().parameters()),'records':records,'geometry_diagnostics':geom_checks,'training_diagnostics':model_checks,
        'versions':{'python':platform.python_version(),'torch':torch.__version__,'numpy':np.__version__},'elapsed_sec':time.perf_counter()-start}
    path=out/'results.json';path.write_text(json.dumps(obj,sort_keys=True,separators=(',',':')))
    print('RESULT SHA256',hashfile(path),'RECORDS',len(records),'elapsed',round(time.perf_counter()-start,1),flush=True)
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else '.')
