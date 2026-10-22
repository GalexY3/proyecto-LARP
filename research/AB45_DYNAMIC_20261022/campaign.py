"""LARP: transparent adaptive 45-decision (max) real-data branch exploration.
This is *not* native MHU, original COSI, nor a new neural architecture.
A cycle is one pre-recorded question/condition + all matched arms on a fixed VALIDATION set.
Test not accessed in cycle evaluation; exactly one final test readout after decisions frozen.
"""
from pathlib import Path
import numpy as np, json, time, hashlib, platform, math, sys
from sklearn.datasets import load_digits,load_wine,load_breast_cancer,load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from scipy.spatial.distance import cdist
from scipy.linalg import solve

ROOT=Path(__file__).resolve().parent
DATASETS={"digits":load_digits,"wine":load_wine,"breast":load_breast_cancer,"diabetes":load_diabetes}
DS={}
for i,(name,loader) in enumerate(DATASETS.items()):
 ds=loader(); x=np.asarray(ds.data,float); y=np.asarray(ds.target)
 classif=name!='diabetes'
 idx=np.arange(len(y));trainval,test=train_test_split(idx,test_size=.22,random_state=7100+i,stratify=y if classif else None)
 tr,val=train_test_split(trainval,test_size=.28,random_state=8100+i,stratify=y[trainval] if classif else None)
 if classif:
  klass=np.unique(y)
  oy=np.zeros((len(y),len(klass)))
  for j,k in enumerate(klass):oy[:,j]=(y==k).astype(float)
 else:
  mu=y[tr].mean();sd=y[tr].std();oy=((y-mu)/sd)[:,None]
 DS[name]=dict(x=x,y=oy,labels=y,train=tr,val=val,test=test,classif=classif,d=x.shape[1],n=len(y),nclass=oy.shape[1]);

def transforms(rawtr,raw_eval,noise=.0,dropout=0.,seed=1):
 mu=rawtr.mean(0); sd=np.maximum(rawtr.std(0),1e-5)
 x=np.clip((rawtr-mu)/sd,-10,10);te=np.clip((raw_eval-mu)/sd,-10,10)
 rng=np.random.default_rng(seed)
 if noise:te=te+rng.normal(0,noise,te.shape)
 if dropout:te=te*(rng.random(te.shape)>dropout)
 return x,te

def cov_select(C,Q,k):
 """Greedy linear Bayes risk reduction, PSD cov and vector target cross-cov."""
 d=C.shape[0]; chosen=[];mask=np.ones(d,bool)
 for _ in range(k):
  if chosen:
   sub=C[np.ix_(chosen,chosen)]
   rq=Q-C[:,chosen]@solve(sub,Q[chosen],assume_a='pos',check_finite=False)
   inv=solve(sub,C[chosen,:],assume_a='pos',check_finite=False)
   rv=np.diag(C)-np.sum(C[:,chosen]*inv.T,axis=1)
  else:rq=Q;rv=np.diag(C).copy()
  gain=np.sum(rq*rq,axis=1)/np.maximum(rv,1e-8)
  gain[~mask]=-np.inf
  j=int(gain.argmax()); chosen.append(j);mask[j]=False
 return chosen

def fps_select(name,z,k,seed):
 d=z.shape[1]
 if name=='digits':
  a=np.array([(i//8,i%8) for i in range(64)],float)
  # Start near grid centre then greedily maximize min distance (geometry-only).
  first=int(np.argmin(np.sum((a-3.5)**2,axis=1)))
  dist=cdist(a,a)
 else:
  # Nonspatial: feature correlation dissimilarity, not physical distance.
  corr=np.corrcoef(z.T); corr=np.nan_to_num(corr)
  dist=1-np.abs(corr)
  first=int(np.argmin(np.sum(np.abs(corr),axis=1)))
 sel=[first];used=np.zeros(d,bool);used[first]=True
 for _ in range(k-1):
  score=np.min(dist[:,sel],axis=1);score[used]=-np.inf
  j=int(np.argmax(score));sel.append(j);used[j]=True
 return sel

def methods(x,y,ds,k,seed):
 n,d=x.shape; q=(x-x.mean(0)).T@(y-y.mean(0))/n
 z=x-x.mean(0); S=(z.T@z)/n
 C=S+.17*np.eye(d)
 # standard linear Gaussian guided selection with estimated covariance
 targets=cov_select(C,q,k)
 # shrink covariance of predictor noise; same q and train as TARGET
 diagonal=np.diag(np.diag(S)); shrink=cov_select(.35*S+.65*diagonal+.17*np.eye(d),q,k)
 # rank supervised signal per individual feature = simple strong known baseline
 rank=np.sum(q*q,axis=1)/(np.diag(S)+.17)
 ranktop=np.argsort(-rank)[:k].tolist()
 # Hybrid spatial target covariance with spectrum prior for image pixel grid (proxy, not genuine MHU/COSI)
 if ds=='digits':
  pos=np.indices((8,8)).reshape(2,-1).T
  sp=np.exp(-cdist(pos,pos)**2/(2*2.4**2))
  empirical_diag=np.sqrt(np.diag(S))
  sp=sp*empirical_diag[:,None]*empirical_diag[None,:]
  hybrid=cov_select(.65*S+.35*sp+.17*np.eye(d),q,k)
 else:
  hybrid=shrink.copy() # NO meaningful spatial analogue outside images; excluded from comparative win count
 random=np.random.default_rng(seed).choice(d,k,replace=False).tolist()
 fps=fps_select(ds,x,k,seed)
 return {'TARGET':targets,'SHRINK':shrink,'RANK':ranktop,'FPS':fps,'RANDOM':random,'SPATIAL_HYBRID':hybrid}

def fit_eval(x,y,xe,ye,sel,noise,drop,seed,alpha):
 # Training and evaluation were already standardized together from the pilot.
 # NEVER scale evaluation a second time; noise/dropout apply in standardized units.
 rng=np.random.default_rng(seed)
 te=xe.copy()
 if noise:te=te+rng.normal(0,noise,size=te.shape)
 if drop:te=te*(rng.random(te.shape)>drop)
 model=Ridge(alpha=alpha).fit(x[:,sel],y)
 yh=model.predict(te[:,sel]);err=float(np.sqrt(np.mean((yh-ye)**2)))
 return err,model

def evaluate(config,seed=9200,include_test=False):
 d=DS[config['dataset']];idx=np.random.default_rng(seed).permutation(d['train'])[:min(config['pilot'],len(d['train']))]
 trainx=d['x'][idx]; trainy=d['y'][idx]
 ev_idx=d['test'] if include_test else d['val']
 evalx=d['x'][ev_idx]; evaly=d['y'][ev_idx]
 X,Xe=transforms(trainx,evalx)
 nfeat=min(config['budget'],d['d']-1)
 t=time.perf_counter();sels=methods(X,trainy,config['dataset'],nfeat,seed);selection_elapsed=time.perf_counter()-t
 arms={}
 for arm,ids in sels.items():
  # All arms use same supervised readout and train data (no differences in information).
  rmse,_=fit_eval(X,trainy,Xe,evaly,ids,config['noise'],config['dropout'],seed+19,config['alpha'])
  arms[arm]={'rmse':rmse,'ids':ids}
 if config['dataset']!='digits':arms.pop('SPATIAL_HYBRID')
 return {'scores':arms,'elapsed_selection_all_s':round(selection_elapsed,6),'ntrain':len(idx),'neval':len(ev_idx)}

FAMILIES=['BASE','FEWSHOT','BUDGET','NOISE','DROPOUT','RIDGE_ALPHA','TRANSFER_DOMAIN']
def propose(history,counts,cycle):
 """Causally reactive proposal. The branch and config are computed from PREVIOUS results.
 Not from a prelisted set of 45 conditions. Decision written before execution.
 Domains alternate to prevent a single dataset from monopolizing the evidence.
 """
 if not history:
  return {'dataset':'digits','family':'BASE','pilot':160,'budget':8,'noise':0.,'dropout':0.,'alpha':1.,'motivation':'First real image dataset, fixed honest train/validation/test split'}
 last=history[-1];win=last['winner'];margin=last['relative_margin'];prior=last['condition']
 domain_counts={n:sum(h['condition']['dataset']==n for h in history) for n in DS}
 # Branching: do not take duplicate setting, privilege fresh domains if poor winner or narrow gap.
 if margin<.015 or win in ('TARGET','RANK'):
  focus='TRANSFER_DOMAIN'; ds=min(domain_counts,key=lambda n:(domain_counts[n],n))
 elif win in ('SHRINK','SPATIAL_HYBRID'):
  focus='FEWSHOT' if counts['FEWSHOT']<counts['NOISE']+2 else 'NOISE';ds=prior['dataset']
 elif win=='FPS':
  focus='BUDGET';ds=prior['dataset']
 else:
  focus='DROPOUT' if counts['DROPOUT']<=counts['RIDGE_ALPHA'] else 'RIDGE_ALPHA';ds=prior['dataset']
 # Diversity escape: every 4 cycles force least tested FAMILY on least tested dataset.
 if cycle%4==1:
  focus=min(FAMILIES,key=lambda f:(counts[f],f));ds=min(domain_counts,key=lambda n:(domain_counts[n],n))
 n=DS[ds]['d'];maxpilot=len(DS[ds]['train'])
 budget={'digits':[4,8,12,20],'wine':[3,5,7,9],'breast':[4,8,12,16],'diabetes':[2,3,5,7]}[ds][(cycle+counts[focus])%4]
 pilot0=min(maxpilot,{'digits':320,'wine':90,'breast':200,'diabetes':180}[ds])
 pilot={'BASE':pilot0,'FEWSHOT':max(16,int(pilot0/(2+(cycle%3)*2))), 'BUDGET':pilot0,
        'NOISE':pilot0,'DROPOUT':pilot0,'RIDGE_ALPHA':pilot0,'TRANSFER_DOMAIN':pilot0}[focus]
 noise=(0.15+(cycle%3)*.2) if focus=='NOISE' else 0.
 drop=(0.10+(cycle%3)*.15) if focus=='DROPOUT' else 0.
 alpha=([.02,.2,2.0][cycle%3] if focus=='RIDGE_ALPHA' else 1.)
 return {'dataset':ds,'family':focus,'pilot':pilot,'budget':budget,'noise':noise,'dropout':drop,'alpha':alpha,
         'motivation':f"Post-cycle {cycle-1}: {win} won validation with {margin:.2%} relative gap; {'seek weak-signal alternative' if margin<.015 else 'attempt discriminating ablation'}; family selected adaptively."}

def main(ncycles=45):
 for p in ['decision_events.jsonl','cycles.jsonl']:(ROOT/p).write_text('')
 counts={x:0 for x in FAMILIES};history=[];seen=set()
 for cycle in range(1,ncycles+1):
  config=propose(history,counts,cycle)
  # Repair duplicates by opening a different budget and pilot conditional on prior outcomes.
  while True:
   sig=tuple((k,config[k]) for k in ['dataset','family','pilot','budget','noise','dropout','alpha'])
   if sig not in seen:break
   config['budget']=2+(config['budget']%(DS[config['dataset']]['d']-2))
   config['pilot']=min(len(DS[config['dataset']]['train']),config['pilot']+cycle%11+1)
  seen.add(sig);counts[config['family']]+=1
  decision={'cycle':cycle,'condition':config,'previous_cycle':cycle-1 if cycle>1 else None,
    'previous_winner':history[-1]['winner'] if history else None,
    'prior_result_margin':history[-1]['relative_margin'] if history else None,
    'time_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
    'frozen_before_val_execution':True,'decision_basis':'PREVIOUS VALIDATION SCORES ONLY, NEVER HELDOUT TEST',
    'rivals':['TARGET','SHRINK','RANK','FPS','RANDOM']+(['SPATIAL_HYBRID'] if config['dataset']=='digits' else []),
    'hypothesis':'Shrinkage or spatial geometry may add value in small-pilot or corruption regimes; may fail vs supervised selection.'}
  with (ROOT/'decision_events.jsonl').open('a') as f:f.write(json.dumps(decision,ensure_ascii=False)+'\n');f.flush()
  r=evaluate(config,9200+cycle*77)
  ranks=sorted(r['scores'],key=lambda x:r['scores'][x]['rmse'])
  best=r['scores'][ranks[0]]['rmse']; second=r['scores'][ranks[1]]['rmse']
  result={'cycle':cycle,'condition':config,'winner':ranks[0],'runner':ranks[1],
          'relative_margin':float((second-best)/max(second,1e-7)),
          'scores':r['scores'],'ntrain':r['ntrain'],'neval':r['neval'],
          'status':'REAL_OBSERVATIONAL_DATA_EXPLORATORY_REUSED_VALIDATION',
          'strict_not_original_MHU':True,'decision':'BRANCH_NEXT' if cycle<ncycles else 'CLOSE_AND_TEST_ONCE'}
  with (ROOT/'cycles.jsonl').open('a') as f:f.write(json.dumps(result,ensure_ascii=False)+'\n');f.flush()
  history.append(result)
  print(f"C{cycle:02} {config['dataset']:8} {config['family']:15} pilot={r['ntrain']:3} k={config['budget']:2} {ranks[0]:14} RMSE={best:.4f} vs {ranks[1]} {second:.4f}",flush=True)
 # IMPORTANT test consulted only ONCE after development for a SINGLE preregistered
 # selection rule: for each domain choose method with lowest mean validation RMSE over its
 # five most recent configurations. Final test on one frozen, unperturbed fixed config per dataset.
 domain_receipts={}
 for domain in DS:
  recent=[z for z in history if z['condition']['dataset']==domain][-5:]
  method_names=list(recent[0]['scores']);avg_val={m:float(np.mean([r['scores'][m]['rmse'] for r in recent])) for m in method_names}
  champion=min(avg_val,key=avg_val.get)
  # Baseline always TARGET, both evaluated once on same final heldout setting.
  cfg={'dataset':domain,'family':'FINAL_CLEAN','pilot':min(len(DS[domain]['train']),{'digits':320,'wine':90,'breast':200,'diabetes':180}[domain]),
       'budget':{'digits':8,'wine':5,'breast':8,'diabetes':3}[domain], 'noise':0.,'dropout':0.,'alpha':1.}
  te=evaluate(cfg,seed=123000+list(DS).index(domain)*99,include_test=True)
  domain_receipts[domain]={'chosen_method':champion,'selection_validation_score':avg_val,'frozen_final_config':cfg,
                           'test_once':{m:d['rmse'] for m,d in te['scores'].items()},
                           'holdout_size':te['neval'],'note':'fixed final condition differs from adaptively explored conditions; this is a transfer test, not confirmatory victory of chosen method'}
 out={'ncycles':len(history),'families':counts,'dataset_counts':{a:sum(h['condition']['dataset']==a for h in history) for a in DS},
      'wins':{m:sum(h['winner']==m for h in history) for m in ['TARGET','SHRINK','RANK','FPS','RANDOM','SPATIAL_HYBRID']},
      'final_test':domain_receipts,'evaluation_warning':'same validation reused 45x; adaptive decisions not 45 independent studies; one fixed heldout per domain used only at end',
      'science_warning':'feature selection, not original hyperuniform geometry nor truly costed adaptive per-instance acquisition',
      'source':'sklearn builtin datasets; no external network',
      'versions':{'python':platform.python_version(),'sklearn':__import__('sklearn').__version__,'numpy':np.__version__}}
 (ROOT/'SUMMARY.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
 return out

if __name__=='__main__':
 m=int(sys.argv[1]) if len(sys.argv)>1 else 45;main(m)
