"""AB8 exploratory: cross-class Fourier coherence in five marked point sets.

Sources: archived authentic 4096-node Scale3D patterns, four paired seeds,
CVT references from prior campaigns. Compare the *same per-type point clouds*
under global and independent translations. This is not a novel neural model.
"""
import os,sys,json,math,time
from pathlib import Path
from itertools import product
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from scipy.stats import qmc

ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data';OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
SEEDS=list(range(5201,5205)); TYPES=5
COUNTS=np.array([1669,871,696,512,348]);f=COUNTS/4096
names=['initial','local','mhu','cvt','sobol','lattice','lhs']
low=np.array([k for k in product(range(-3,4),repeat=3) if k!=(0,0,0) and (k[0]>0 or k[0]==0 and k[1]>0 or k[0]==0 and k[1]==0 and k[2]>0) and sum(a*a for a in k)<=6],dtype=np.int64)
assert len(low)==40
rr=np.random.default_rng(2229)
allm=np.array([k for k in product(range(-12,13),repeat=3) if k!=(0,0,0) and (k[0]>0 or k[0]==0 and k[1]>0 or k[0]==0 and k[1]==0 and k[2]>0) and 101<=sum(a*a for a in k)<=140],dtype=np.int64)
outside=allm[rr.choice(len(allm),42,replace=False)]
BANDS={'low':low,'outside':outside}

PAT={};LAB={};COMP={};AMPS={}
for seed in SEEDS:
    with np.load(D/f'orig_{seed}.npz') as z:
        LAB[seed]=z['labels'].astype('int64'); PAT[seed]={k:z[k].astype(float)%1 for k in ('initial','local','mhu')}
    with np.load(D/f'cvt_refined_4096_{1701+(seed-5201)%3}.npz') as z:
        cvt=np.empty((4096,3),float)
        for j in range(5):cvt[LAB[seed]==j]=z['points'][z['labels']==j]
        PAT[seed]['cvt']=cvt%1
    sob=np.empty((4096,3));lat=sob.copy();lhs=sob.copy()
    for j in range(5):
        idx=np.where(LAB[seed]==j)[0];n=len(idx)
        sob[idx]=qmc.Sobol(3,scramble=True,seed=seed*13+j).random_base2(math.ceil(math.log2(n)))[:n]
        gen=17+2*j;v=np.array([1,gen,gen*gen]);lat[idx]=((np.arange(n)[:,None]*v[None,:])%n)/n+np.random.default_rng(seed*41+j).random(3)
        lhs[idx]=qmc.LatinHypercube(3,scramble=True,seed=seed*31+j).random(n)
    PAT[seed].update(sobol=sob%1,lattice=lat%1,lhs=lhs%1)
    assert np.array_equal(np.bincount(LAB[seed],minlength=5),COUNTS)
    for name in names:
        for band,ks in BANDS.items():
            A=np.stack([np.exp(2j*np.pi*(PAT[seed][name][LAB[seed]==j] @ ks.T)).mean(axis=0) for j in range(5)])
            AMPS[(seed,name,band)]=A

def spectral(A,w=f):return float(np.mean(np.abs(w@A)**2))
def independent(A,w=f):return float(np.mean(np.sum((w[:,None]**2)*(abs(A)**2),axis=0)))
def components(A,w=f):
    selfpart=independent(A,w);full=spectral(A,w)
    return {'union':full,'diag':selfpart,'cross':full-selfpart,'cross_fraction':(full-selfpart)/selfpart if selfpart>1e-26 else None}
def save(idx,question,observe,decision,nextq,qualifications):
    record={'cycle':idx,'question':question,'observations':observe,'AB_DECIDE':decision,'next_selected':nextq,'limits':qualifications,'classification':'EXPLORATORY_ADAPTIVE_FOUR_GEOMETRIES'}
    p=OUT/f'C{idx:02d}.json';p.write_text(json.dumps(record,indent=2,ensure_ascii=False,allow_nan=False));print(f'C{idx:02d} {decision}: {question}',flush=True)
    return record

def cov(seed,name,points=None,k=16):
    p=PAT[seed][name] if points is None else points; rng=np.random.default_rng(seed+88770)
    q=rng.random((800,3));ix=cKDTree(p%1,boxsize=1).query(q,k=k)[1]
    return float(np.mean(np.stack([(LAB[seed][ix]==j).any(axis=1) for j in range(5)]).all(axis=0)))

def translated(A,modes,shift):return A*np.exp(2j*np.pi*(shift@modes.T))

def matched_shift(seed,name,band,rep=100):
    A=AMPS[(seed,name,band)];ks=BANDS[band];rg=np.random.default_rng(seed*109+len(name)+len(band))
    vals=[]
    for _ in range(rep):vals.append(spectral(translated(A,ks,rg.random((5,3)))))
    return float(np.mean(vals)),float(np.std(vals,ddof=1)),float(np.quantile(vals,.05)),float(np.quantile(vals,.95))

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='c1':
        res={}
        for name in names:
            per=[]
            for seed in SEEDS:
                A=AMPS[(seed,name,'low')];c=components(A);B=(f@A)
                assert max(abs(B-(np.exp(2j*np.pi*PAT[seed][name]@low.T).mean(axis=0))))<1e-12
                per.append(c)
            res[name]={x:float(np.mean([v[x] for v in per if v[x] is not None])) for x in ['union','diag','cross']}
            res[name]['seeds']=per
        save(1,'¿Qué parte de la supresión de unión proviene de los términos cruzados entre tipos?',res,'CONTINUE','Desplazar clases sin alterar sus autospectros y medir efecto', 'Atribución algebraica de Fourier; misma banda optimizada y cuatro semillas, no ventaja neural.')
    elif cmd=='c2':
        res={}
        for name in names:
            raw=[];sh=[];per=[]
            for seed in SEEDS:
                r=spectral(AMPS[(seed,name,'low')]);z=matched_shift(seed,name,'low',rep=96)
                raw.append(r);sh.append(z[0]);per.append({'seed':seed,'before':r,'shift_mean':z[0],'q05':z[2],'q95':z[3]})
            res[name]={'original':float(np.mean(raw)),'random_relative_translation_mean':float(np.mean(sh)),'ratio':float(np.mean(sh))/max(float(np.mean(raw)),1e-29),'per_seed':per}
        save(2,'¿La coordinación intertipo aporta algo más allá de los autospectros S_a?',res,'CONTINUE','Examinar señales compartidas frente a independientes', 'Traslaciones mantienen cada S_a exactamente, modifican S_union y cobertura; correlación espectral cruzada es mecanismo clásico.')
    elif cmd=='c3':
        r={};weights={'population':f,'equal':np.ones(5)/5, 'rare_priority':np.array([.1,.1,.1,.1,.6])}
        for wname,w in weights.items():
            r[wname]={}
            for name in names:
                seeds=[]
                for seed in SEEDS:
                    A=AMPS[(seed,name,'low')];diag=independent(A,w);s=spectral(A,w)
                    # Covariance of Gaussian common field and independent type fields
                    pred={str(rho):float(rho*s+(1-rho)*diag) for rho in (0.,.25,.5,.75,1.)}
                    seeds.append(pred)
                r[wname][name]={k:float(np.mean([v[k] for v in seeds])) for k in seeds[0]}
        # Monte Carlo independent verification for MHU/LOCAL, shared rho=0.75 and equal weights
        monte={};rho=.75;w=weights['equal'];rg=np.random.default_rng(94040)
        for n in ('local','mhu','cvt'):
            A=AMPS[(5201,n,'low')]; K=A.shape[1];batch=7000
            shared=(rg.normal(size=(batch,K))+1j*rg.normal(size=(batch,K)))/np.sqrt(K)
            separate=(rg.normal(size=(batch,5,K))+1j*rg.normal(size=(batch,5,K)))/np.sqrt(K)
            e=(np.sqrt(rho)*shared[:,None,:]+np.sqrt(1-rho)*separate)
            xs=(np.real((e*A[None,:,:]).sum(axis=2))@w)
            monte[n]={'observed':float(np.mean(xs**2)),'analytic':float(rho*spectral(A,w)+(1-rho)*independent(A,w))}
        res={'expected_risk':r,'monte_carlo':monte,'coefficient_normalization':'independent real and imaginary standard Gaussian / sqrt(K); no 1/2 factor'}
        save(3,'¿Cambia la utilidad de las fases cruzadas al variar correlación funcional y pesos por tipo?',res,'CONTINUE','Repetir fuera de banda para descartar función fabricada a favor', 'Estimación de DC con campos gaussianos toroidales conocidos; fórmula matemática valida MC, no generalización neuronal.')
    elif cmd=='c4':
        res={}
        for band in ('low','outside'):
            x={}
            for name in names:
                original=[];s=[];diag=[]
                for seed in SEEDS:
                    A=AMPS[(seed,name,band)];original.append(spectral(A));diag.append(independent(A));s.append(matched_shift(seed,name,band,rep=32)[0])
                x[name]={'original':float(np.mean(original)),'after_relative_shifts':float(np.mean(s)),'independent_baseline':float(np.mean(diag))}
            res[band]=x
        save(4,'¿Persiste la ventaja por fase cruzada en frecuencias realmente no optimizadas?',res,'CONTINUE','Intentar construir el mismo efecto con un comparador de bajo coste mediante traslaciones optimizadas', 'La banda fuera de corte es pos-seleccionada y el conjunto de modos finite; no holdout confirmatorio.')
    elif cmd=='c5':
        rng=np.random.default_rng(6161);train=low[:20];hold=low[20:]
        records={}
        for name in ('local','mhu','cvt','sobol'):
            outputs=[]
            for seed in SEEDS:
                A=AMPS[(seed,name,'low')]
                def fun(x):
                    sh=np.vstack([np.zeros(3),x.reshape(4,3)]);Z=translated(A[:,:20],train,sh)
                    return spectral(Z)
                x0=np.zeros(12); opt=minimize(fun,x0,method='L-BFGS-B',bounds=[(-1,1)]*12,options={'maxiter':220,'ftol':1e-15,'gtol':1e-12,'eps':5e-4})
                sh=np.vstack([np.zeros(3),opt.x.reshape(4,3)])
                old=spectral(A);new=spectral(translated(A,low,sh));tr0=spectral(A[:,:20]);tr1=spectral(translated(A[:,:20],train,sh));h0=spectral(A[:,20:]);h1=spectral(translated(A[:,20:],hold,sh))
                p=PAT[seed][name].copy()
                for t in range(5):p[LAB[seed]==t]=(p[LAB[seed]==t]+sh[t])%1
                outputs.append({'seed':seed,'initial_all':old,'optimized_all':new,'train_initial':tr0,'train_optimized':tr1,'heldout_initial':h0,'heldout_optimized':h1,'cover16_before':cov(seed,name),'cover16_after':cov(seed,name,points=p),'optimizer_success':bool(opt.success),'func_evals':opt.nfev})
            records[name]={'by_seed':outputs,'mean_heldout_ratio':float(np.mean([z['heldout_optimized']/max(z['heldout_initial'],1e-30) for z in outputs])),'mean_coverage_change':float(np.mean([z['cover16_after']-z['cover16_before'] for z in outputs]))}
        save(5,'¿Puede recuperarse acoplamiento mediante traslaciones convencionales manteniendo los S_a?',records,'CONTINUE','Probar la sensibilidad al ruido y presupuestos de sensores', 'Optimizamos 12 grados de traslación en bandas in-sample; prueba hold-out low no es independiente de entrenamiento original MHU. Tiempo de generación no equiparado.')
    elif cmd=='c6':
        res={}
        for name in names:
            t=[]
            for seed in SEEDS:
                p=PAT[seed][name];lab=LAB[seed];w=f
                modes=low
                rg=np.random.default_rng(seed+8713)
                pairs=[]
                for frac in (0.,.1,.25,.5):
                    vals=[]
                    for rep in range(24):
                        aa=[]
                        for j in range(5):
                            ix=np.where(lab==j)[0];keep=ix[rg.random(len(ix))>=frac]
                            if len(keep)==0:continue
                            aa.append(np.exp(2j*np.pi*p[keep]@modes.T).mean(axis=0))
                        if len(aa)!=5:continue
                        vals.append(spectral(np.stack(aa),w))
                    pairs.append({'drop':frac,'mse':float(np.mean(vals))})
                t.append(pairs)
            res[name]={str(frac):float(np.mean([seq[i]['mse'] for seq in t])) for i,frac in enumerate((0.,.1,.25,.5))}
        save(6,'¿La ventaja de fases cruzadas resiste el coste de pérdidas de sensores?',res,'CONTINUE','Entrenar una lectura aprendida con target variable y comprobar si diferencia es útil', 'Se renormaliza media por tipo tras dropout; no simula costes de red; mismos mundos matemáticos, distinto ratio de sensores.')
    elif cmd=='c7':
        # Holdout worlds for learning five offsets from noisy sensor-class averages.
        # Zero predictor is nontrivial comparator because DC offset has non-zero variance.
        from sklearn.linear_model import Ridge
        w=f
        r={};rng=np.random.default_rng(7700)
        NTR=250;NTE=2000;K=len(low)
        mu_train=rng.normal(0,.07,size=(NTR,5));mu_test=rng.normal(0,.07,size=(NTE,5))
        shtr=(rng.normal(size=(NTR,K))+1j*rng.normal(size=(NTR,K)))/np.sqrt(K)
        shte=(rng.normal(size=(NTE,K))+1j*rng.normal(size=(NTE,K)))/np.sqrt(K)
        targettr=mu_train@w;targette=mu_test@w
        for name in names:
            per=[]
            for seed in SEEDS:
                A=AMPS[(seed,name,'low')]
                # Shared latent perturbation identical in all five channels; DC offsets independent per type
                Xtr=mu_train+np.real(shtr@A.T)
                Xte=mu_test+np.real(shte@A.T)
                lin=Ridge(alpha=1e-4,fit_intercept=True)
                lin.fit(Xtr,targettr)
                predicted=lin.predict(Xte)
                direct=Xte@w
                per.append({'seed':seed,'learned_mse':float(np.mean((predicted-targette)**2)),'direct_mse':float(np.mean((direct-targette)**2)),'zero_mse':float(np.mean(targette**2)),'effective_weights':lin.coef_.tolist()})
            r[name]={'per_seed':per,'learned_mse_mean':float(np.mean([x['learned_mse'] for x in per])),'direct_mse_mean':float(np.mean([x['direct_mse'] for x in per]))}
        save(7,'¿Persiste el efecto en una lectura aprendida con objetivo no trivial, sin fórmula fija?',{'scores':r,'training_samples':NTR,'test_samples':NTE,'estimator':'ridge 5 features with same regularization; test worlds held out','target': 'weighted average of 5 independent DC offsets; common low Fourier perturbation'},'CONTINUE','Auditar si el mejor rendimiento es también nuevo y suficiente para redes reales', 'Ridge no es Transformer/GNN; las distribuciones de entrenamiento y prueba comparten generador y banda baja optimizada; geometrías n=4.')
    elif cmd=='c8':
        # OOD task: a model learned on the low Fourier modes must process independent
        # test worlds with modes strictly outside Scale3D spectral objective.
        from sklearn.linear_model import Ridge
        w=f; K=len(low);L=len(outside)
        rg=np.random.default_rng(7700); NTR=250;NTE=2000
        mut=rg.normal(0,.07,size=(NTR,5));mue=rg.normal(0,.07,size=(NTE,5))
        tr=(rg.normal(size=(NTR,K))+1j*rg.normal(size=(NTR,K)))/np.sqrt(K)
        te_low=(rg.normal(size=(NTE,K))+1j*rg.normal(size=(NTE,K)))/np.sqrt(K)
        te_out=(rg.normal(size=(NTE,L))+1j*rg.normal(size=(NTE,L)))/np.sqrt(L)
        res={}
        for name in names:
            per=[]
            for seed in SEEDS:
                A=AMPS[(seed,name,'low')];B=AMPS[(seed,name,'outside')]
                train=mut+np.real(tr@A.T)
                model=Ridge(alpha=1e-4).fit(train,mut@w)
                xlo=mue+np.real(te_low@A.T);xout=mue+np.real(te_out@B.T)
                true=mue@w
                low_mse=float(np.mean((model.predict(xlo)-true)**2))
                out_mse=float(np.mean((model.predict(xout)-true)**2))
                out_direct=float(np.mean((xout@w-true)**2))
                per.append({'seed':seed,'low_test_mse':low_mse,'outside_transfer_mse':out_mse,'outside_direct_mse':out_direct})
            res[name]={'low_test_mean':float(np.mean([p['low_test_mse'] for p in per])), 'outside_transfer_mean':float(np.mean([p['outside_transfer_mse'] for p in per])), 'outside_direct_mean':float(np.mean([p['outside_direct_mse'] for p in per])),'per_seed':per}
        save(8,'¿Generaliza una lectura entrenada con señales compartidas bajas a frecuencias nuevas?',{'scores':res,'train_worlds':NTR,'test_worlds':NTE,'low_modes':int(K),'outside_modes':int(L),'outside_range_k2':[int((outside*outside).sum(axis=1).min()),int((outside*outside).sum(axis=1).max())],'benchmark':'Ridge same parameter budget and same draws; four geometries original per Scale3D'},'CLOSE_BLOCK_REQUEST_DECISION','Evaluación del bloque, novedades, solicitud de ciclos posteriores por valor de información','OOD relativo al objetivo espectral de Scale3D; reusar familia espacial Fourier y no disponer de Wei auténtico limitan novedad 2/3. El readout no prueba arquitectura de lenguaje.')
    else:raise SystemExit(f'unknown cmd {cmd}')
