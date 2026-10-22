from common import *
def run():
 rows=[]
 for g in GSEEDS:
  for method in METHODS:
   p,l=geometry(g,method);Q=finite_modes(2,4,9);alpha=np.ones(5)/5;R0=node_covariance(p,l,Q,0,.03);R1=node_covariance(p,l,Q,1,.03)
   wb=gls_weights(R0,l,alpha);wj=gls_weights(R1,l,alpha);by=[];ranks=[]
   for c in range(5):
    k=np.where(l==c)[0];b=wb[k];by.append(float(b@R0[np.ix_(k,k)]@b));t=2*np.pi*p[k,:2]@Q.T;ranks.append(int(np.linalg.matrix_rank(np.column_stack([np.ones(len(k)),np.cos(t),np.sin(t)]))))
   vb=float(wb@R1@wb);vj=float(wj@R1@wj);assert vj<=vb*(1+1e-6)+1e-12
   rows.append({'geometry':g,'method':method,'independent_risk_by_type':by,'design_ranks':ranks,'nuisance_columns':1+2*len(Q),'minority_fraction_rho0':sum(by[3:])/sum(by),'correlated_block_risk':vb,'correlated_joint_risk':vj,'joint_to_block':vj/vb})
 return {'rows':rows,'summary':{m:{'minority_fraction':float(np.mean([r['minority_fraction_rho0'] for r in rows if r['method']==m])),'joint_to_block':float(np.mean([r['joint_to_block'] for r in rows if r['method']==m])),'risk_by_type':np.mean([r['independent_risk_by_type'] for r in rows if r['method']==m],axis=0).tolist()} for m in METHODS}}
