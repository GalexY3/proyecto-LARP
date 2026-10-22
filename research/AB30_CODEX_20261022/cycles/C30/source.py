from common import *
from scipy.spatial import cKDTree
from scipy.stats import qmc
import sys
sys.path.insert(0,str(ROOT))
from src.AB06_REALDATA_20261022.scale3d_geometry_v2 import generate
FOLDER=BASE/'cycles'/'C30'
NEW_SEEDS=[6023001,6023002]

def cvt_per_type(p,lab,seed):
    rng=np.random.default_rng(seed+9000);q=p.copy()
    for t in range(5):
        idx=np.where(lab==t)[0];centres=q[idx].copy()
        for _ in range(14):
            probes=rng.random((4000,3))
            assigned=cKDTree(centres,boxsize=1).query(probes,k=1)[1]
            for j in range(len(idx)):
                ps=probes[assigned==j]
                if len(ps):
                    dif=((ps-centres[j]+.5)%1-.5)
                    centres[j]=(centres[j]+dif.mean(axis=0))%1
        q[idx]=centres
    return q

def run():
 rows=[];construction=[];qx=finite_modes(2,1,2);q3=finite_modes(3,1,2)
 for seed in NEW_SEEDS:
  tic=time.perf_counter()
  a=generate(seed,128,device='cpu',iterations=600,spectral=False,chi=.12,local_weight=.15,grid_size=16,validate=False)
  b=generate(seed,128,device='cpu',iterations=600,spectral=True,chi=.12,local_weight=.15,grid_size=16,validate=False)
  labels=a['labels'].cpu().numpy()
  assert np.array_equal(labels,b['labels'].cpu().numpy())
  counts=np.bincount(labels);assert counts.tolist()==[52,27,22,16,11]
  r=np.random.default_rng(seed*19).random((128,3));sob=np.zeros_like(r)
  for t in range(5):
   ix=np.where(labels==t)[0];sob[ix]=qmc.Sobol(d=3,scramble=True,seed=seed+11*t).random_base2(int(np.ceil(np.log2(len(ix)))))[:len(ix)]
  geo={'local':a['coordinates'].cpu().numpy(),'mhu':b['coordinates'].cpu().numpy(),'random':r,'cvt':cvt_per_type(r,labels,seed),'sobol':sob}
  for p in geo.values():assert np.isfinite(p).all() and np.all((p>=0)&(p<1))
  path=FOLDER/f'geo_{seed}.npz';assert not path.exists()
  np.savez_compressed(path,labels=labels,**geo)
  record={'seed':seed,'counts':counts.tolist(),'file':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'local':a['construction'],'mhu':b['construction'],'local_history':a['history'],'mhu_history':b['history'],'total_construction_seconds':time.perf_counter()-tic,'no_spectral_filter_or_reseed':True}
  construction.append(record)
  for method,p in geo.items():
   p=np.asarray(p,dtype=float);balanced=np.ones(5)/5;weighted=counts/counts.sum()
   R0=node_covariance(p,labels,qx,0,0);R1=node_covariance(p,labels,qx,1,0)
   w0=mean_weights(labels,balanced);w1=mean_weights(labels,weighted)
   R3=node_covariance(p,labels,q3,0,.03);g=gls_weights(R3,labels,balanced)
   ranks=[]
   for c in range(5):
    t=2*np.pi*p[labels==c]@q3.T
    ranks.append(int(np.linalg.matrix_rank(np.column_stack([np.ones(counts[c]),np.cos(t),np.sin(t)]))))
   assert np.max(abs(np.eye(5)[labels].T@g-balanced))<1e-9
   rows.append({'seed':seed,'method':method,'S_xy_types_union':finite_spectrum(p[:,:2],labels,qx),'S_3d_types_union':finite_spectrum(p,labels,q3),'risk_xy_balanced_rho0_mean':float(w0@R0@w0),'risk_xy_counts_rho1_mean':float(w1@R1@w1),'risk_3d_balanced_rho0_gls_noise03':float(g@R3@g),'rank_3d_per_type':ranks,'rank_columns':1+2*len(q3)})
  print('new geometry completed',seed,flush=True)
 checks=[]
 for seed in NEW_SEEDS:
  d={r['method']:r for r in rows if r['seed']==seed};m=d['mhu'];c=d['cvt']
  checks.append({'seed':seed,'union_mhu_less_cvt':bool(m['S_xy_types_union'][-1]<c['S_xy_types_union'][-1]),'independent_balanced_mhu_worse_cvt':bool(m['risk_xy_balanced_rho0_mean']>c['risk_xy_balanced_rho0_mean']),'coherent_counts_mhu_better_cvt':bool(m['risk_xy_counts_rho1_mean']<c['risk_xy_counts_rho1_mean']),'native3d_gls_independent_mhu_worse_cvt':bool(m['risk_3d_balanced_rho0_gls_noise03']>c['risk_3d_balanced_rho0_gls_noise03'])})
 return {'construction':construction,'rows':rows,'prediction_checks':checks,'summary':{m:{key:float(np.mean([r[key] for r in rows if r['method']==m])) for key in ['risk_xy_balanced_rho0_mean','risk_xy_counts_rho1_mean','risk_3d_balanced_rho0_gls_noise03']} for m in METHODS},'scope':'Two unseen realizations of a historically selected generator. Within-generator replication only; all retained, no external dataset/architecture confirmation.'}
