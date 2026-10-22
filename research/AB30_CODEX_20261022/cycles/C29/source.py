from common import *
def run():
 rows=[];alpha=np.ones(5)/5;Q=finite_modes(3,1,2)
 for g in GSEEDS:
  for method in METHODS:
   p,l=geometry(g,method);R=node_covariance(p,l,Q,1,.03);H=np.eye(5)[l]
   for rmu in [0,.5,1]:
    P=(1-rmu)*np.eye(5)+rmu*np.ones((5,5));fullV=H@P@H.T+R;fullc=H@P@alpha;vf=float(alpha@P@alpha-fullc@np.linalg.solve(fullV,fullc))
    for missing in [0,4]:
     keep=np.where(l!=missing)[0];O=H[keep];V=O@P@O.T+R[np.ix_(keep,keep)];c=O@P@alpha;risk=float(alpha@P@alpha-c@np.linalg.solve(V,c));other=[i for i in range(5) if i!=missing];cond=float(P[missing,missing]-P[missing,other]@np.linalg.pinv(P[np.ix_(other,other)])@P[other,missing]);bound=alpha[missing]**2*max(cond,0.)
     assert risk>=bound-1e-10 and risk>=vf-1e-10
     rows.append({'geometry':g,'method':method,'offset_correlation':rmu,'missing_type':missing,'remaining_nodes':len(keep),'full_risk':vf,'missing_risk':risk,'information_lower_bound':bound})
 return {'rows':rows,'summary':{f'offsetrho{rmu}':{m:{'missing_risk':float(np.mean([r['missing_risk'] for r in rows if r['method']==m and r['offset_correlation']==rmu])),'full_risk':float(np.mean([r['full_risk'] for r in rows if r['method']==m and r['offset_correlation']==rmu])),'bound':float(np.mean([r['information_lower_bound'] for r in rows if r['method']==m and r['offset_correlation']==rmu]))} for m in ['local','mhu','cvt','random']} for rmu in [0,.5,1]}}
