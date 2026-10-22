from common import *
def run():
    im,y,tr,va,te=dataset();rows=[]
    for g in GSEEDS:
        for method in METHODS:
            p,l=geometry(g,method);M=encoder_matrix(g,method);s=np.linalg.svd(M,compute_uv=False);r=int(np.linalg.matrix_rank(M))
            direct=encode(im[:33],p,l);linear=im[:33].reshape(-1,64)@M
            rows.append({'geometry':g,'method':method,'rank':r,'smax':float(s[0]),'smin':float(s[-1]),'condition_nonzero':float(s[0]/s[r-1]),'noise_trace':float(np.sum(M*M)),'max_linearity_error':float(np.max(np.abs(direct-linear))),'singular_values':s.tolist()})
    return {'rows':rows,'summary':{'max_residual':max(r['max_linearity_error'] for r in rows),'full_rank_count':sum(r['rank']==64 for r in rows),'ranks':{m:[r['rank'] for r in rows if r['method']==m] for m in METHODS},'condition_by_method':{m:[round(r['condition_nonzero'],1) for r in rows if r['method']==m] for m in METHODS},'trace_range':[min(r['noise_trace'] for r in rows),max(r['noise_trace'] for r in rows)]}}

