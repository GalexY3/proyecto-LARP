from common import *
def run():
 rng=np.random.default_rng(60221);Q=finite_modes(3,1,2);rows=[]
 for g in GSEEDS:
  for method in METHODS:
   p,l=geometry(g,method);n=np.bincount(l);m=n//2;a,u=amplitudes(p,l,Q);C=(a@a.conj().T/len(Q)).real;fr=m/n;D=np.sqrt(fr);Cp=D[:,None]*C*D[None,:];diag=1+(m-1)/(n-1)*(np.diag(C)-1);np.fill_diagonal(Cp,diag);w=np.sqrt(m/m.sum());pred=np.r_[diag,w@Cp@w];vals=[]
   for rep in range(200):
    keep=np.concatenate([rng.choice(np.where(l==c)[0],m[c],replace=False) for c in range(5)]);vals.append(finite_spectrum(p[keep],l[keep],Q))
   mc=np.mean(vals,axis=0);rows.append({'geometry':g,'method':method,'counts_before':n.tolist(),'counts_after':m.tolist(),'predicted':pred.tolist(),'observed':mc.tolist(),'full_union':float(np.mean(abs(u)**2)),'max_relative_mc_error':float(np.max(abs(mc/pred-1)))})
 return {'rows':rows,'summary':{m:{'full_union':float(np.mean([r['full_union'] for r in rows if r['method']==m])),'retained_union':float(np.mean([r['observed'][-1] for r in rows if r['method']==m])),'retained_components':np.mean([r['observed'][:5] for r in rows if r['method']==m],axis=0).tolist()} for m in METHODS},'max_relative_mc_error':max(r['max_relative_mc_error'] for r in rows)}
