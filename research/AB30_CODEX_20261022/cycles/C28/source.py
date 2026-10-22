from common import *
def run():
 Q=finite_modes(2,1,2);rows=[];maxerr=0.
 def metrics(p,l):
  a,u=amplitudes(p[:,:2],l,Q);C=(a@a.conj().T/len(Q)).real;n=np.bincount(l);out={}
  for name,alpha,rho in [('common_counts',n/n.sum(),1),('independent_balanced',np.ones(5)/5,0),('common_balanced',np.ones(5)/5,1)]:
   w=alpha/np.sqrt(n);out[name]=float(w@(C*((1-rho)*np.eye(5)+rho*np.ones((5,5))))@w)
  out['component_trace']=float(np.trace(C));return out
 for g in GSEEDS:
  for method in ['local','mhu','cvt']:
   p,l=geometry(g,method);native=metrics(p,l);rng=np.random.default_rng(60228+g);perms=[]
   for rep in range(64):
    ll=rng.permutation(l);v=metrics(p,ll);maxerr=max(maxerr,abs(v['common_counts']/native['common_counts']-1));perms.append(v)
   rows.append({'geometry':g,'method':method,'native':native,'permuted':{k:float(np.mean([r[k] for r in perms])) for k in native},'permutation_metrics':perms})
 assert maxerr<1e-9
 return {'rows':rows,'summary':{m:{name:{k:float(np.mean([r[name][k] for r in rows if r['method']==m])) for k in ['common_counts','independent_balanced','common_balanced','component_trace']} for name in ['native','permuted']} for m in ['local','mhu','cvt']},'max_common_counts_relative_residual':maxerr}
