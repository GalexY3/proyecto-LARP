"""AB 3.2.1: adaptive sequential 30-decision exploration of low-pilot sparse sensing.

Images are real examples bundled with scikit-image. 4 train images; 2 development
images already exposed by previous project; a new untouched retina image is
accessed ONCE at C30. Native 2D proxies, not original 3D Scale3D.
Benchmarks are exploratory and non-independent at patch level.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import json,hashlib,time,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.stats import qmc
from sklearn.linear_model import Ridge
from skimage import data
P=Path(__file__).resolve().parent
SIDE=24; D=SIDE*SIDE; A=3
W0=np.array([.2126,.7152,.0722])
KK=np.array([(i,j) for i in range(-5,6) for j in range(-5,6) if 0 < i*i+j*j<=25 and (i>0 or (i==0 and j>0))],float)
XY=np.stack(np.meshgrid((np.arange(SIDE)+.5)/SIDE,(np.arange(SIDE)+.5)/SIDE),axis=-1).reshape(-1,2)

def image_patches(name,n,seed,retina=False):
    im=np.asarray(getattr(data,name)(),dtype=np.float32)/255
    if retina:im=im[300:1100,300:1100,:]
    rng=np.random.default_rng(seed)
    yy=rng.integers(0,im.shape[0]-SIDE+1,n);xx=rng.integers(0,im.shape[1]-SIDE+1,n)
    return np.stack([im[y:y+SIDE,x:x+SIDE,:].transpose(2,0,1) for x,y in zip(xx,yy)])

def load_data(with_heldout=False):
    names=['astronaut','coffee','chelsea','immunohistochemistry']
    train=np.concatenate([image_patches(s,450,100+i) for i,s in enumerate(names)])
    dev=np.concatenate([image_patches(s,240,300+i) for i,s in enumerate(['rocket','hubble_deep_field'])])
    if with_heldout:return train,dev,image_patches('retina',1100,97773,True)
    return train,dev

def target(arr,w):
    return np.einsum('c,nc->n',w,arr.mean(axis=(2,3)))

def unbiased_pred(arr,ids,w):
    x=arr.reshape(len(arr),3,D)
    return sum(w[a]*x[:,a,ids[a]].mean(axis=1) for a in range(A) if len(ids[a]))

def rmse(arr,ids,w):
    return float(np.mean((target(arr,w)-unbiased_pred(arr,ids,w))**2)**.5)

def learned_rmse(xtrain, xtest, ids,w,alpha=0.2):
    if len(xtrain)<4:return float('nan')
    zt=np.column_stack([xtrain.reshape(len(xtrain),3,D)[:,a,ids[a]] for a in range(3) if len(ids[a])]); zv=np.column_stack([xtest.reshape(len(xtest),3,D)[:,a,ids[a]] for a in range(3) if len(ids[a])]);
    m=Ridge(alpha=alpha).fit(zt,target(xtrain,w));return float(np.mean((target(xtest,w)-m.predict(zv))**2)**.5)

def fourier_cov(samples):
    ff=np.fft.fft2(samples-samples.mean(axis=(2,3),keepdims=True),axes=(2,3))/(D)
    z=np.stack([ff[:,:,int(i)%SIDE,int(j)%SIDE] for i,j in KK.astype(int)],axis=1)
    return np.einsum('nka,nkb->kab',z.conj(),z,optimize=True)/len(z)

def sobol_layout(q,seed):
    ans=[]
    for a,m in enumerate(q):
        if not m:ans.append(np.array([],dtype=int));continue
        unit=qmc.Sobol(2,scramble=True,seed=seed+37*a).random_base2(int(np.ceil(np.log2(m))))[:m]
        idx=np.clip((unit*SIDE).astype(int),0,SIDE-1)
        ids=idx[:,1]*SIDE+idx[:,0]
        used=set(); fixed=[]
        for idx in ids:
            idx=int(idx)
            if idx in used:
                cand=[i for i in range(D) if i not in used];idx=int(cand[np.argmin(np.sum((XY[cand]-XY[idx])**2,axis=1))])
            used.add(idx);fixed.append(idx)
        ans.append(np.array(fixed,dtype=int))
    return ans

def spectral_layout(samples,w,q,seed,variant='COSI_SHRINK',shrink=0.5,maxiter=68):
    C=fourier_cov(samples); B=len(KK)
    power=np.stack([np.diag(np.real(np.diag(c))) for c in C])
    if variant=='COSI_SHRINK':C=(1-shrink)*power+shrink*C
    elif variant=='POWER_DIAG':C=power
    elif variant=='ISOTROPIC':
        scale=float(np.real(np.trace(C,axis1=1,axis2=2)).mean())/(3)
        C=np.broadcast_to(np.eye(3)[None,:,:]*scale,(B,3,3)).copy()
    else:raise ValueError(variant)
    ids=sobol_layout(q,seed)
    if any(x==0 for x in q): return ids,0.0
    flat=np.concatenate([XY[ids[a]] for a in range(A)],axis=0)
    lengths=np.array(q); starts=np.r_[0,lengths.cumsum()]
    rng=np.random.default_rng(seed);x0=np.clip(flat+rng.normal(0,.016,flat.shape),.0001,.9999).reshape(-1)
    def loss(z):
        pts=z.reshape(sum(q),2)
        es=np.exp(2j*np.pi*(pts@KK.T))
        means=np.array([es[starts[a]:starts[a+1]].mean(axis=0)*w[a] for a in range(A)])
        u=np.einsum("kab,bk->ak",C,means,optimize=True)
        risk=float(np.real(np.vdot(means,u)))
        gr=np.zeros_like(pts)
        for a,m in enumerate(q):
            if not m:continue
            e=es[starts[a]:starts[a+1]]
            v=-(4*np.pi*w[a]/m)*np.einsum('jk,kd->jd',np.imag(np.conj(u[a])[None,:]*e),KK)
            gr[starts[a]:starts[a+1]]+=v
        # weak same-type repulsion, fixed strength across all variants
        lam=2e-5
        for a,m in enumerate(q):
            if m<2:continue
            ptsa=pts[starts[a]:starts[a+1]];delta=ptsa[:,None,:]-ptsa[None,:,:];delta-=np.rint(delta)
            rr=(delta**2).sum(axis=2); e=np.exp(-rr/.0225)*(1-np.eye(m))
            risk+=lam*e.sum();gr[starts[a]:starts[a+1]]+=lam*(-4/.0225)*np.einsum('ij,ijd->id',e,delta)
        return risk,gr.ravel()
    r=minimize(loss,x0,jac=True,bounds=[(.0001,.9999)]*len(x0),method='L-BFGS-B',options={'maxiter':maxiter,'ftol':1e-9})
    pp=r.x.reshape(-1,2);out=[]
    for a,m in enumerate(q):
        pts=pp[starts[a]:starts[a+1]];inds=np.clip((pts*SIDE).astype(int),0,SIDE-1);raw=inds[:,1]*SIDE+inds[:,0]
        used=set();new=[]
        for idx in raw:
            idx=int(idx)
            if idx in used:
                cands=np.array([i for i in range(D) if i not in used]);idx=int(cands[np.argmin(np.sum((XY[cands]-XY[idx])**2,axis=1))])
            used.add(idx);new.append(idx)
        out.append(np.array(new,dtype=int))
    return out,float(r.fun)

def direct_layout(samples,w,q,seed,passes=2):
    rng=np.random.default_rng(seed);ids=sobol_layout(q,seed);X=samples.reshape(len(samples),3,D)
    residual=unbiased_pred(samples,ids,w)-target(samples,w)
    for _ in range(passes):
        changes=0
        for a,j in rng.permutation([(a,j) for a in range(3) for j in range(q[a])]):
            a=int(a);j=int(j);old=ids[a][j]
            delta=(w[a]/q[a])*(X[:,a,:]-X[:,a,old,None]);scores=np.mean((residual[:,None]+delta)**2,axis=0)
            scores[ids[a][np.arange(q[a])!=j]]=np.inf
            new=int(np.argmin(scores))
            if new!=old:residual+=delta[:,new];ids[a][j]=new;changes+=1
        if not changes:break
    return ids,float(np.mean(residual**2)**.5)

def gp_greedy(samples,w,q,seed,shrink=.25,candidates=72):
    # Greedy Bayesian linear/GP-like conditional variance reduction, with a
    # shared candidate pool across methods; data-driven posterior of the target.
    rng=np.random.default_rng(seed)
    inds=[]; types=[]
    for a in range(3):
        c=qmc.Sobol(2,scramble=True,seed=seed+13*a).random_base2(7)[:candidates]
        xy=(np.clip((c*SIDE).astype(int),0,SIDE-1)); pos=np.unique(xy[:,1]*SIDE+xy[:,0]);
        inds.extend(pos.tolist());types.extend([a]*len(pos))
    inds=np.array(inds,dtype=int);types=np.array(types)
    x=samples.reshape(len(samples),3,D);features=np.stack([x[:,a,k] for a,k in zip(types,inds)],axis=1)
    feat=features-features.mean(axis=0); yy=target(samples,w); yy=yy-yy.mean()
    K=(feat.T@feat)/len(samples); ycov=(feat.T@yy)/len(samples)
    diag=np.diag(K).copy();K=(1-shrink)*K+shrink*np.diag(diag)+np.diag(diag*0.015+1e-5)
    Kcond=K.copy(); c=ycov.copy();remaining=np.array(q);selected=[]
    for j in range(sum(q)):
        allowed=(remaining[types]>0)
        if selected:allowed[selected]=False
        scores=c*c/(np.diag(Kcond)+1e-10);scores[~allowed]=-np.inf
        best=int(np.argmax(scores));selected.append(best);remaining[types[best]]-=1
        denom=Kcond[best,best]
        if denom>1e-9:
            cc=Kcond[:,best].copy();c-=cc*ycov[best]/denom if False else cc*(c[best]/denom)
            Kcond-=np.outer(cc,cc)/denom
            Kcond=(Kcond+Kcond.T)*.5
    res=[inds[[i for i in selected if types[i]==a]] for a in range(3)]
    return res,float(np.var(yy))

def eval_design(train,dev,method,params,seed):
    w=np.array(params['weights'],dtype=float);q=params['quota'];alpha=params.get('pilot',60)
    # Pilot selection uses only TRAIN scene samples; never the developmental environments.
    rng=np.random.default_rng(seed*19+19)
    samp=train[rng.choice(len(train),min(alpha,len(train)),replace=False)]
    t0=time.perf_counter()
    if method=='SOBOL':idx=sobol_layout(q,seed);loss=float('nan')
    elif method=='DIRECT':idx,loss=direct_layout(samp,w,q,seed)
    elif method=='GP':idx,loss=gp_greedy(samp,w,q,seed,shrink=params.get('gp_shrink',.35))
    else:idx,loss=spectral_layout(samp,w,q,seed,variant=method,shrink=params.get('shrink',.5))
    elapsed=time.perf_counter()-t0
    z={'method':method,'seed':seed,'pilot_n':len(samp),'q':q,'weights':w.tolist(),'loss':loss,'construction_s':elapsed,
       'development_fixed_RMSE':rmse(dev,idx,w),'train_fixed_RMSE':rmse(samp,idx,w),
       'development_ridge_RMSE':learned_rmse(samp,dev,idx,w,alpha=.25),
       'ids':[arr.tolist() for arr in idx]}
    return z

def compare(train,dev,param,seed,methods):
    results=[eval_design(train,dev,method,param,seed) for method in methods]
    return {'results':results,'rmses':{z['method']:z['development_fixed_RMSE'] for z in results},
            'ridges':{z['method']:z['development_ridge_RMSE'] for z in results},
            'seconds':{z['method']:z['construction_s'] for z in results}}

# Reactive decision policy: outcome of previous run selects next intervention.
# No outcome from new 3rd heldout scene is visible until cycle 30.
def next_design(i,history):
    pilot_values=[12,28,64,128,256,600,1200]
    budgets=[[2,4,2],[3,7,2],[4,10,2],[6,16,2],[9,23,4],[12,32,4]]
    weights=[[.2126,.7152,.0722],[1/3,1/3,1/3],[1,0,0],[0,1,0],[.5,0,-.5]]
    if not history:
        return {'branch':'BASELINE','pilot':64,'quota':[6,16,2],'weights':weights[0],'shrink':.5,'gp_shrink':.35}, 'Initial benchmark of strong direct, GP, diagonal and COSI controls'
    last=history[-1];errs=last['comparison']['rmses'];best=min(errs,key=errs.get);cosi=errs['COSI_SHRINK']
    if i<=7:
        # Invest whether spectral method wins due to low pilot, regardless of prior leader.
        j=i-2
        p=pilot_values[j]
        return {'branch':'LOW_PILOT_FOCUS' if best=='COSI_SHRINK' else 'LOW_PILOT_ADVERSARIAL','pilot':p,'quota':[6,16,2],'weights':weights[0],'shrink':.5,'gp_shrink':.35},f'Prior winner {best}; evaluate pilot n={p} on development'
    if i<=13:
        j=i-8;b=budgets[j]
        return {'branch':'SENSOR_BUDGET' if cosi<=errs['SOBOL'] else 'COVERAGE_PIVOT','pilot':64,'quota':b,'weights':weights[0],'shrink':.5,'gp_shrink':.35},f'Compare earlier COSI and Sobol; budget {sum(b)}'
    if i<=18:
        j=i-14;w=weights[j]
        # Aim for adversarial targets even if loses
        return {'branch':'ESTIMAND_SENSITIVITY' if cosi<=errs['DIRECT'] else 'ESTIMAND_PIVOT','pilot':64,'quota':[8,8,8],'weights':w,'shrink':.5,'gp_shrink':.35},'Target sensitivity after inspecting prior relative error'
    if i<=23:
        j=i-19;s=[0,.25,.5,.75,1][j]
        return {'branch':'CROSS_CHANNEL_ABLATION' if cosi<=errs['POWER_DIAG'] else 'DIAGONAL_NULL_FOCUS','pilot':64,'quota':[6,16,2],'weights':weights[0],'shrink':s,'gp_shrink':.35},'Cross-covariance shrinkage, compare POWER_DIAG'
    if i<=28:
        j=i-24;s=[0,.15,.35,.65,.9][j]
        return {'branch':'GP_ROBUSTNESS' if cosi<=errs['GP'] else 'GP_ADVANTAGE_PIVOT','pilot':64,'quota':[6,16,2],'weights':weights[0],'shrink':.5,'gp_shrink':s},'GP covariance shrink sensitivity'
    if i==29:
        return {'branch':'MODEL_SELECTION_LOCK','pilot':64,'quota':[6,16,2],'weights':weights[0],'shrink':.5,'gp_shrink':.35},'Freeze selected contender (selection uses only development data)'
    return {'branch':'FINAL_UNSEEN_SCENE','pilot':64,'quota':[6,16,2],'weights':weights[0],'shrink':.5,'gp_shrink':.35},'Evaluate exactly once on never-read retinal image'

def run():
    train,dev=load_data();methods=['SOBOL','DIRECT','GP','POWER_DIAG','COSI_SHRINK']
    start=time.time();ledger=[]
    for i in range(1,30):
        p,reason=next_design(i,ledger)
        comp=compare(train,dev,p,seed=7000+i,methods=methods)
        best=min(comp['rmses'],key=comp['rmses'].get)
        entry={'cycle':i,'date':'2026-10-22','decision_event':p['branch'],'reason_from_previous':reason,'params':p,'comparison':comp,
               'favored':best,'winner_suggested_only_dev':best,'status':'RUN_EXPLORATORY','holdout_retina_opened':False}
        ledger.append(entry)
        with (P/'ledger.jsonl').open('a') as f:f.write(json.dumps(entry,ensure_ascii=False)+'\n')
        print(f'C{i:02d} {p["branch"]} pilot={p["pilot"]} budget={sum(p["quota"])} shrink={p["shrink"]} -> {best} cosi={comp["rmses"]["COSI_SHRINK"]:.5f} GP={comp["rmses"]["GP"]:.5f}',flush=True)
    # Choose winner by mean relative development RMSE over cycles 1..29 for the fixed original estimand,
    # quota [6,16,2], pilot <=64; still contaminated by previous LARP searches.
    eligible=[r for r in ledger if r['params']['weights']==W0.tolist() and r['params']['quota']==[6,16,2] and r['params']['pilot']<=64]
    means={m:float(np.mean([r['comparison']['rmses'][m] for r in eligible])) for m in methods}
    champion=min(means,key=means.get)
    # Freeze selection *before* reading retina dataset. Persist freeze JSON and SHA.
    freeze={'champion':champion,'candidate_dev_means':means,'selection_records':[r['cycle'] for r in eligible],
      'all_methods':methods,'retina_test_seed':97773,'test_patches':1100,'retina_crop':[300,1100,300,1100],
      'protocol':'Same sample layout as C29, evaluate all methods (NOT multiple confirmatory claims) on retina once; no retuning.'}
    (P/'holdout_freeze.json').write_text(json.dumps(freeze,indent=2))
    freeze['sha256_pre_holdout']=hashlib.sha256((P/'holdout_freeze.json').read_bytes()).hexdigest()
    # Freeze exact C29 designs from previous run, no new fitting after opening retina
    c29=ledger[-1]; assert c29['cycle']==29
    _,_,retina=load_data(with_heldout=True)
    rows=[]
    for zz in c29['comparison']['results']:
        q=[np.array(x,dtype=int) for x in zz['ids']]
        rows.append({'method':zz['method'],'retina_fixed_RMSE':rmse(retina,q,W0),'development_fixed_RMSE':zz['development_fixed_RMSE'],
          'ratio_holdout_over_development':rmse(retina,q,W0)/zz['development_fixed_RMSE'],
          'ids':zz['ids']})
    final={'cycle':30,'date':'2026-10-22','decision_event':'FINAL_UNSEEN_SCENE','reason_from_previous':'Freeze C29 layouts; open retina ONCE',
           'freeze':freeze,'results':rows,'status':'RUN_SINGLE_NEW_SCENE_EXPLORATORY','holdout_retina_opened':True,
           'winner_retina_descriptive_only':min(rows,key=lambda z:z['retina_fixed_RMSE'])['method']}
    ledger.append(final)
    with (P/'ledger.jsonl').open('a') as f:f.write(json.dumps(final)+'\n')
    summary={'n_cycles':len(ledger),'c1_to_c29_dev_win_counts':{m:sum(e['favored']==m for e in ledger[:29]) for m in methods},
             'eligible_dev_means':means,'champion_selected_before_holdout':champion,'holdout_retina':rows,
             'runtime_sec':time.time()-start,'source_images':['astronaut','coffee','chelsea','immunohistochemistry','rocket','hubble_deep_field','retina'],
             'limits':['No independent 3D physical sensors','Only one new heldout scene','Patches within scenes dependent','Previous research already selected quota/target','No honest SOTA GP optimized implementation','Proxies not actual MHU/Local SI Scale3D']}
    (P/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    print('C30 holdout',json.dumps({x['method']:round(x['retina_fixed_RMSE'],6) for x in rows}),flush=True)
    print('Summary',json.dumps({k:v for k,v in summary.items() if k not in ['holdout_retina']},ensure_ascii=False),flush=True)
    return summary
if __name__=='__main__':run()
