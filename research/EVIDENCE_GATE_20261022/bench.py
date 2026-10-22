"""LARP proof-of-utility gate: physical grayscale-image operator streams.

Not an environmental/multisite sensor experiment. Three channels are derived
from each original grayscale image, so they do not constitute independent
physical modalities. All methods use the same pilot data and same two readouts.
Target is a *known* weighted average of the three operator means; an additional
Ridge readout is fit on exactly the same pilot for each design.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import sys, json, hashlib, time
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter, sobel
from scipy.stats import qmc
from sklearn.linear_model import Ridge
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'reference'))
from value30_spectral import sobol_layout, spectral_layout, direct_layout, gp_greedy, target, unbiased_pred, SIDE
from skimage import data
W=np.array([.5,.2,.3])
QUOTA=[4,8,4]
N_PER_SCENE=160
TRAIN=['camera','moon']; DEV='grass'; TEST=['gravel','brick','cell','microaneurysms']

def load(name,n,seed):
    im=np.asarray(getattr(data,name)(),dtype=np.float32)/255
    assert im.ndim==2, (name,im.shape)
    blur=gaussian_filter(im,1.3)
    grad=np.sqrt(sobel(im,axis=0)**2+sobel(im,axis=1)**2)/4
    # Reference intensity, blurred intensity and gradient magnitude are computed
    # on the entire *same* physical grayscale image. The target is their weighted mean.
    images=np.stack([im,blur,grad])
    rng=np.random.default_rng(seed)
    iy=rng.integers(0,im.shape[0]-SIDE+1,n)
    ix=rng.integers(0,im.shape[1]-SIDE+1,n)
    return np.stack([images[:,y:y+SIDE,x:x+SIDE] for y,x in zip(iy,ix)]).astype(np.float32)

def get():
    t=np.concatenate([load(x,N_PER_SCENE,50+j) for j,x in enumerate(TRAIN)])
    d=load(DEV,N_PER_SCENE,70)
    return t,d

def predict_ridge(pilot,arr,ids,alpha=.02):
    def fea(a):
        x=a.reshape(len(a),3,-1)
        return np.column_stack([x[:,r,ids[r]] for r in range(3) if len(ids[r])])
    mdl=Ridge(alpha=alpha).fit(fea(pilot),target(pilot,W))
    return mdl.predict(fea(arr))

def layout(pilot,method,seed):
    if method=='SOBOL':return sobol_layout(QUOTA,seed)
    if method=='DIRECT':return direct_layout(pilot,W,QUOTA,seed,passes=2)[0]
    if method=='GP':return gp_greedy(pilot,W,QUOTA,seed,shrink=.45,candidates=144)[0]
    if method=='POWER_DIAG':return spectral_layout(pilot,W,QUOTA,seed,variant='POWER_DIAG',maxiter=65)[0]
    if method=='COSI':return spectral_layout(pilot,W,QUOTA,seed,variant='COSI_SHRINK',shrink=.5,maxiter=65)[0]
    raise ValueError(method)

def metrics(a,y):
    return dict(rmse=float(np.mean((np.asarray(y)-target(a,W))**2)**.5),
                mae=float(np.mean(np.abs(np.asarray(y)-target(a,W)))))

def run():
    train,dev=get(); methods=['SOBOL','DIRECT','GP','POWER_DIAG','COSI']
    # Phase A, not a new independent holdout. Six arms fixed *before* opening tests.
    conditions=[(16,4001),(16,4002),(32,4003),(32,4004),(96,4005),(96,4006)]
    records=[]; freezes=[]
    for cycle,(pilot_n,seed) in enumerate(conditions,1):
        t0=time.monotonic(); rng=np.random.default_rng(seed)
        pilot=train[rng.choice(len(train),pilot_n,replace=False)]
        design=[]
        for method in methods:
            ix=layout(pilot,method,seed)
            vf=metrics(dev,unbiased_pred(dev,ix,W))['rmse']
            vr=metrics(dev,predict_ridge(pilot,dev,ix))['rmse']
            design.append({'method':method,'ids':[p.tolist() for p in ix],'dev_fixed_rmse':vf,'dev_ridge_rmse':vr})
        entry={'cycle':cycle,'pilot_n':pilot_n,'seed':seed,'method_risks':design,'duration_s':time.monotonic()-t0,
               'decision':'FOCUS' if cycle<5 else 'GATE_TO_TEST', 'test_consumed':False}
        records.append(entry)
        print('A%02d'%cycle,pilot_n, ' '.join(f'{r["method"]}:{r["dev_fixed_rmse"]:.4f}/{r["dev_ridge_rmse"]:.4f}' for r in design),flush=True)
    (ROOT/'dev_ledger.json').write_text(json.dumps(records,indent=2))
    # One preregistered comparison of methods on four as-yet unopened images.
    # ALL methods evaluated: no cherry-picked single winner; summary is descriptive.
    freeze={'readouts':['fixed_mean','ridge_alpha_.02'],'quota':QUOTA,'weights':W.tolist(),
            'test_sources':TEST,'train_sources':TRAIN,'dev_sources':DEV,'conditions':conditions,
            'designs':[{ 'pilot_n':r['pilot_n'],'seed':r['seed'],'methods':[{'name':z['method'],'ids':z['ids']} for z in r['method_risks']]} for r in records],
            'single_test_opening':True,'limitations':'Derived channels; one fixed estimator targeted by COSI; scanner texture not spatial environmental field.'}
    b=json.dumps(freeze,sort_keys=True,indent=2).encode();(ROOT/'HOLDOUT_FREEZE.json').write_bytes(b)
    freeze_hash=hashlib.sha256(b).hexdigest();print('FREEZE',freeze_hash,flush=True)
    # Only now score each preselected layout for all four new sources.
    tests={x:load(x,N_PER_SCENE,120+j) for j,x in enumerate(TEST)}
    rows=[]
    for r in records:
        rng=np.random.default_rng(r['seed']);pilot=train[rng.choice(len(train),r['pilot_n'],replace=False)]
        for z in r['method_risks']:
            ix=[np.array(v,dtype=int) for v in z['ids']]
            for name,arr in tests.items():
                for estimator in ['fixed','ridge']:
                    y=unbiased_pred(arr,ix,W) if estimator=='fixed' else predict_ridge(pilot,arr,ix)
                    row={'pilot_n':r['pilot_n'],'seed':r['seed'],'method':z['method'],'test_scene':name,
                         'estimator':estimator,**metrics(arr,y)}
                    rows.append(row)
    (ROOT/'TEST_RESULTS.json').write_text(json.dumps({'freeze_sha256':freeze_hash,'results':rows},indent=2))
    # Equal scene weights. Same train/test and deterministic input for all methods.
    d={}
    for est in ['fixed','ridge']:
        d[est]={}
        for m in methods:
            rs=[x for x in rows if x['method']==m and x['estimator']==est]
            per={s:float(np.mean([x['rmse'] for x in rs if x['test_scene']==s])) for s in TEST}
            d[est][m]={'unweighted_scene_macro_rmse':float(np.mean(list(per.values()))),'by_scene':per}
    (ROOT/'SUMMARY.json').write_text(json.dumps({'methods':methods,'summary':d,'condition_count':len(conditions),
          'scene_count':len(TEST),'frozen_test_sha256':freeze_hash,'data_provenance':'scikit-image built-in physical grayscale images; three operator-derived channels (not native multisensor sites).'},indent=2))
    print('SUMMARY',json.dumps(d,indent=2),flush=True)

if __name__=='__main__':run()
