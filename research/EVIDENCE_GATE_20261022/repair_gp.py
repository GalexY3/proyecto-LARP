"""Post-test adversarial GP candidate-pool repair; NEVER count as new holdout."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import json,sys,time
import numpy as np
from pathlib import Path
from sklearn.linear_model import Ridge
sys.path.insert(0,str(Path(__file__).resolve().parent))
from bench import get,load,W,TRAIN,DEV,TEST,N_PER_SCENE,QUOTA,target,metrics,predict_ridge,unbiased_pred
P=Path(__file__).resolve().parent

def full_gp(pilot,shrink=.45,epsilon=1e-5):
    N=len(pilot)
    X=pilot.reshape(N,3,-1).reshape(N,-1).astype(float)
    xx=X-X.mean(axis=0)
    yy=target(pilot,W);yc=yy-yy.mean()
    K=xx.T@xx/N
    ycova=xx.T@yc/N
    diag=K.diagonal().copy()
    K*=1-shrink
    K[np.diag_indices_from(K)]+=shrink*diag+.015*diag+epsilon
    np.fill_diagonal(K,np.diag(K).clip(min=epsilon))
    c=ycova.copy()
    # Remaining quota is counted per role, not per candidate.
    remain=np.array(QUOTA)
    selected=[]
    for _ in range(sum(QUOTA)):
        allowed=remain[np.arange(1728)//576]>0
        if selected:allowed[selected]=False
        scores=c*c/np.maximum(K.diagonal(),1e-9)
        scores[~allowed]=-np.inf
        i=int(np.argmax(scores));selected.append(i)
        remain[i//576]-=1
        denom=float(K[i,i]);k=K[:,i].copy()
        c-=k*(c[i]/denom)
        K-=np.outer(k,k)/denom
        K=(K+K.T)*.5
    return [np.array([j%576 for j in selected if j//576==a],dtype=int) for a in range(3)]

def run():
    train,dev=get();tests={x:load(x,N_PER_SCENE,120+j) for j,x in enumerate(TEST)}
    records=[]
    for seed,n in [(4001,16),(4002,16),(4003,32),(4004,32),(4005,96),(4006,96)]:
        rng=np.random.default_rng(seed); pilot=train[rng.choice(len(train),n,replace=False)]
        t0=time.monotonic();ids=full_gp(pilot)
        val={'pilot':n,'seed':seed,'duration_seconds':time.monotonic()-t0,
             'positions':[v.tolist() for v in ids],
             'development':{'fixed':metrics(dev,unbiased_pred(dev,ids,W))['rmse'],
                            'ridge':metrics(dev,predict_ridge(pilot,dev,ids))['rmse']},
             'test_posthoc':{}}
        for name,a in tests.items():
            val['test_posthoc'][name]={'fixed':metrics(a,unbiased_pred(a,ids,W))['rmse'],
              'ridge':metrics(a,predict_ridge(pilot,a,ids))['rmse']}
        records.append(val)
        print('GP_ALL',seed,n,'dev',val['development'],'seconds',round(val['duration_seconds'],1),flush=True)
    overall={k:float(np.mean([v['test_posthoc'][x][k] for v in records for x in TEST])) for k in ('fixed','ridge')}
    (P/'GP_ALL_POSTHOC.json').write_text(json.dumps({'status':'POST_HOC_AFTER_HOLDOUT','estimator_alignment':'candidate geometry expanded, same target and readout',
           'full_candidates_per_role':576,'records':records,'macro_rmse':overall},indent=2))
    print('MACRO',overall,flush=True)
if __name__=='__main__':run()
