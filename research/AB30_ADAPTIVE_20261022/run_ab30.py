"""Thirty feedback-selected computational contrasts on synthetic periodic 3D fields.
Not native LARP Scale3D; not neural training or external confirmation. AB3.2.1 exploratory.
"""
import json,hashlib
from pathlib import Path
import numpy as np
from scipy.stats import qmc
A,M=5,12; N=A*M; W=np.ones(A)/A
K=np.array([v for x in range(-2,3) for y in range(-2,3) for z in range(-2,3) if (v:=(x,y,z))>(0,0,0)],float); B=len(K); I=np.eye(A)
assert B==62
ROOT=Path(__file__).resolve().parent; LOG=ROOT/'ledger.jsonl'
SHA=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
def ph(p): return np.stack([np.exp(2j*np.pi*p[a*M:(a+1)*M]@K.T).mean(0) for a in range(A)])
def risk(p,c):
 z=ph(p)*W[:,None];return float(np.einsum('ak,kab,bk->',z.conj(),c,z).real/(2*B))
def grad(p,c):
 t=np.einsum('kab,bk->ak',c,ph(p)*W[:,None]);g=np.zeros_like(p)
 for a in range(A):
  sl=slice(a*M,(a+1)*M);z=np.exp(2j*np.pi*p[sl]@K.T)
  g[sl]=-(2*np.pi*W[a]/(M*B))*(np.imag(t[a].conj()[None,:]*z)@K)
 return g
def local(p,n=12):
 p=p.copy(); same=(np.arange(N)[:,None]//M)==(np.arange(N)[None,:]//M)
 for _ in range(n):
  d=p[:,None,:]-p[None,:,:];d-=np.round(d);r=np.linalg.norm(d,axis=-1)
  q=np.maximum(0,np.where(same,.28,.13)-r)*np.where(same,1,.2)/(r+1e-7)
  np.fill_diagonal(q,0);p=(p+.1*np.einsum('ij,ijk->ik',q,d))%1
 return p
def opt(p,c):
 p=p.copy()
 for i in range(35):
  p=(p-14*np.clip(grad(p,c),-.05,.05))%1
  if i%12==0:p=local(p,1)
 return p
def cvt(p,seed):
 p=p.copy();q=qmc.Sobol(3,scramble=True,seed=seed).random_base2(9)
 for _ in range(8):
  for a in range(A):
   sl=slice(a*M,(a+1)*M);x=p[sl];d=q[:,None,:]-x[None,:,:];d-=np.round(d)
   ix=np.argmin((d*d).sum(-1),axis=1);s=np.zeros_like(x)
   np.add.at(s,ix,d[np.arange(len(q)),ix]);p[sl]=(x+.6*s/np.maximum(1,np.bincount(ix,minlength=M))[:,None])%1
 return p
def cov(seed,coh=.6,het=.5):
 r=np.random.default_rng(seed);out=[]
 for k in K:
  u=r.normal(size=A);u/=np.linalg.norm(u)
  out.append((1+het*float(k@k>2))*((1-coh)*np.diag(1+het*r.lognormal(0,.5,A))+coh*np.outer(u,u)*A))
 return np.array(out)
def pilot(C,seed,n):
 r=np.random.default_rng(seed)
 return np.array([z.T@z/n for z in [r.multivariate_normal(np.zeros(A),c,size=n) for c in C]])
def shift(C,s):
 pi=np.array([1,2,4,0,3]);Q=C[np.roll(np.arange(B),13)][:,pi][:,:,pi]
 return (1-s)*C+s*Q
def outage(p,C,seed,rad):
 r=np.random.default_rng(seed);acc=[]
 for ctr in r.random((4,3)):
  z=[]
  for a in range(A):
   x=p[a*M:(a+1)*M];d=x-ctr;d-=np.round(d);x=x[np.sum(d*d,axis=1)>rad*rad]
   z.append(np.exp(2j*np.pi*x@K.T).mean(0) if len(x) else np.zeros(B,complex))
  q=np.array(z)*W[:,None];acc.append(float(np.einsum('ak,kab,bk->',q.conj(),C,q).real/(2*B)))
 return float(np.mean(acc))
def test_gradient():
 p=np.random.default_rng(123).random((N,3));C=cov(77);g=grad(p,C)
 for i,j in [(0,0),(21,1),(59,2)]:
  h=1e-6;q=p.copy();q[i,j]+=h;a=risk(q,C);q[i,j]-=2*h;b=risk(q,C)
  assert abs((a-b)/(2*h)-g[i,j])<1e-7
FAMS=['pilot_samples','role_correlation','spectral_shift','spatial_outage','role_heterogeneity','shrinkage']
def choose(rows):
 if not rows:return FAMS[0]
 counts={f:sum(z['branch']==f for z in rows) for f in FAMS}
 remaining=[f for f in FAMS if counts[f]==0]
 if remaining:
  if rows[-1]['regret']>.002 and 'spectral_shift' in remaining:return 'spectral_shift'
  return remaining[0]
 last=rows[-1];priority=(['spectral_shift','spatial_outage','pilot_samples'] if last['regret']>.001 else ['role_correlation','shrinkage','role_heterogeneity'] if last['regret']<-.001 else FAMS)
 return min(FAMS,key=lambda f:(counts[f]+(0 if f in priority else .4),priority.index(f) if f in priority else 9))
def run_one(t,branch):
 level=(t-1)//6%5; n=24;coh=.6;het=.5;s=.2;rad=.12;sh=.5
 if branch=='pilot_samples':n=[6,10,24,45,90][level]
 if branch=='role_correlation':coh=[0,.25,.5,.75,1][level]
 if branch=='spectral_shift':s=[0,.25,.5,.75,1][level]
 if branch=='spatial_outage':rad=[0,.08,.15,.22,.3][level]
 if branch=='role_heterogeneity':het=[0,.4,.8,1.2,1.8][level]
 if branch=='shrinkage':sh=[0,.25,.5,.75,1][level]
 C=cov(41000+t,coh,het);Chat=pilot(C,51000+t,n);eye=np.repeat(I[None,:,:],B,axis=0)
 trained=.9*Chat+.1*np.trace(Chat,axis1=1,axis2=2).mean()/A*eye
 shrunk=(1-sh)*trained+sh*np.trace(trained,axis1=1,axis2=2).mean()/A*eye
 raw=[]
 for rep in range(3):
  seed=81000+t*10+rep;r=np.random.default_rng(seed);p=r.random((N,3));loc=local(p,20)
  layouts={'IID':p,'Sobol':np.concatenate([qmc.Sobol(3,scramble=True,seed=seed+17*a).random_base2(4)[:M] for a in range(A)]),
    'LOCAL-proxy':loc,'CVT-proxy':cvt(loc,seed),'MHU-proxy':opt(loc,eye),'COSI-pilot':opt(loc,trained),'COSI-shrink':opt(loc,shrunk),
    'Oracle-known-covariance':opt(loc,C)}
  for name,x in layouts.items():
   raw.append({'seed':seed,'method':name,'source':risk(x,C)**.5,'shift':risk(x,shift(C,s))**.5,'outage':outage(x,C,seed+600,rad)**.5})
 methods={m:{k:float(np.mean([r[k] for r in raw if r['method']==m])) for k in ['source','shift','outage']} for m in sorted(set(x['method'] for x in raw))}
 mix=lambda m:np.mean(list(methods[m].values()))
 fair=[m for m in methods if m!='Oracle-known-covariance']
 winner=min(fair,key=mix)
 return {'parameters':{'pilot_n':n,'coherence':coh,'heterogeneity':het,'shift':s,'outage_radius':rad,'shrinkage':sh},
         'aggregate_RMSE':methods,'individual':raw,'winner':winner,'regret':float(mix('COSI-shrink')-mix('MHU-proxy'))}
def main():
 test_gradient()
 if LOG.exists():raise RuntimeError('Immutable ledger exists; refusing overwrite')
 rows=[]
 for t in range(1,31):
  branch=choose(rows); predecessor=rows[-1] if rows else None
  freeze={'cycle':t,'branch':branch,'parent':predecessor['cycle'] if predecessor else None,
    'reason_from_prior':{'previous_winner':predecessor['winner'],'previous_regret':predecessor['regret']} if predecessor else 'initial priority',
    'runner_sha256':SHA,'scope':'EXPLORATORY_SYNTHETIC_NOT_CONFIRMATORY',
    'rivals':'COSI-shrink vs MHU/LOCAL/CVT/Sobol and pilot+oracle kernels',
    'falsifier':'COSI advantage fails relative to equally informed comparator or shifts'}
  result=run_one(t,branch);row={**freeze,**result}
  with LOG.open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n')
  rows.append(row);print(f'C{t:02d} {branch}: best={row["winner"]}, COSI-MHU={row["regret"]:+.5f}',flush=True)
 result={'source_sha256':SHA,'cycles':30,'family_counts':{f:sum(z['branch']==f for z in rows) for f in FAMS},
   'winner_counts':{m:sum(z['winner']==m for z in rows) for m in sorted(set(z['winner'] for z in rows))},
   'cosi_better_count':sum(z['regret']<0 for z in rows),
   'mean_RMSE':{m:{key:float(np.mean([r['aggregate_RMSE'][m][key] for r in rows])) for key in ['source','shift','outage']} for m in rows[0]['aggregate_RMSE']},
   'limits':['Same synthetic generator across 30 feedback-selected conditions, not 30 independent domains',
     'Only 3 new synthetic geometry seeds per cycle; comparable sample size, not matched runtime',
     'Oracle receives true covariance and is NOT fair head-to-head baseline',
     'Not LARP Scale3D, no trained neural model or real 3D measurements',
     'All adaptive results exploratory; no fresh blinded confirmation or p-values']}
 (ROOT/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print('COMPLETE',flush=True)
if __name__=='__main__':main()
