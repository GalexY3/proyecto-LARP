from common import *
def run():
    rows=[];residual=[]
    for g in GSEEDS:
        for method in METHODS:
            p,l=geometry(g,method); rec={'geometry':g,'method':method}
            for d in [2,3]:
                rec[f'low{d}']=finite_spectrum(p[:,:d],l,finite_modes(d,1,2))
                rec[f'mid{d}']=finite_spectrum(p[:,:d],l,finite_modes(d,4,9))
            q=finite_modes(2,1,9);a,u=amplitudes(p[:,:2],l,q);b,v=amplitudes(p,l,np.column_stack([q,np.zeros(len(q))]))
            residual.append(float(max(np.max(abs(a-b)),np.max(abs(u-v)))))
            rows.append(rec)
    return {'rows':rows,'summary':{'mean_low2':{m:np.mean([r['low2'] for r in rows if r['method']==m],axis=0).tolist() for m in METHODS},'mean_low3':{m:np.mean([r['low3'] for r in rows if r['method']==m],axis=0).tolist() for m in METHODS},'projection_amplitude_residual':max(residual)},'meaning':'Finite-mode descriptive signature; not asymptotic HU certification or causal utility.'}
