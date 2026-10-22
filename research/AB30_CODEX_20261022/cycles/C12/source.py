from common import *
def run():
 rows=[]
 for g in GSEEDS:
  for method in METHODS:
   p,l=geometry(g,method);a,u=amplitudes(p[:,:2],l,finite_modes(2,1,2));C=(a@a.conj().T/len(u)).real
   w=np.sqrt(np.bincount(l)/len(l));ev,V=np.linalg.eigh(C);us=float(w@C@w)
   assert abs(us-float(np.mean(abs(u)**2)))<1e-10
   rows.append({'geometry':g,'method':method,'matrix':C.tolist(),'eigenvalues':ev.tolist(),'trace':float(np.trace(C)),'worst':float(ev[-1]),'union':us,'union_to_worst':us/max(float(ev[-1]),1e-15),'common_overlap_smallest':float((w@V[:,0])**2)})
 return {'rows':rows,'summary':{m:{k:float(np.mean([r[k] for r in rows if r['method']==m])) for k in ['trace','worst','union','union_to_worst','common_overlap_smallest']} for m in METHODS}}
