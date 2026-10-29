"""LARP-VISION C04: true downstream classification; AB3.2.1 preregister BEFORE outcomes.
NO certified MHU / authentic Wei / independent replication.
200 skimage LFW subset face-vs-background crops; 160 scalar image readings.
"""
import json, hashlib, platform, sys, time
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import qmc
from scipy.ndimage import map_coordinates
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.feature_selection import f_classif
from sklearn.metrics import balanced_accuracy_score
from skimage import data
import torch

N=160; K=5; SEEDS=[4101,4109,4127]; FOLDS=[13,29]; STEPS=70
METHODS=['grid','sobol','poisson_disk','spectral_joint','spectral_sub','joint_phase_broken','random','supervised_kbest','full_pixels']
LOW_K=np.array([(i,j) for i in range(-3,4) for j in range(-3,4) if 0<i*i+j*j<=10 and (i>0 or (i==0 and j>0))],float)

def optimize(seed,labels,joint):
    base=qmc.Sobol(d=2,scramble=True,seed=seed+3100).random_base2(8)[:N]
    torch.manual_seed(seed)
    p=torch.tensor(base,dtype=torch.float64,requires_grad=True)
    k=torch.tensor(LOW_K,dtype=torch.float64)
    lab=torch.tensor(labels)
    opt=torch.optim.Adam([p],lr=.014)
    for _ in range(STEPS):
        opt.zero_grad()
        z=torch.exp(2j*np.pi*(p@k.T))
        c=torch.stack([(z[lab==i].mean(0).abs()**2).mean() for i in range(K)]).mean()
        u=(z.mean(0).abs()**2).mean()
        d=p[:,None,:]-p[None,:,:]
        d=d-torch.round(d.detach())
        rep=(torch.exp(-(d*d).sum(-1)/.0009).sum()-N)/(N*N)
        loss=c+(u if joint else 0)+.15*rep
        loss.backward();opt.step()
        with torch.no_grad():p.remainder_(1.)
    return p.detach().numpy()

def geometries(seed):
    y,x=np.mgrid[:10,:16]
    grid=np.stack(((x.ravel()+.5)/16,(y.ravel()+.5)/10),1)
    sob=qmc.Sobol(d=2,scramble=True,seed=seed).random_base2(8)[:N]
    rng=np.random.default_rng(seed);labels=np.repeat(np.arange(5),32);rng.shuffle(labels)
    allpts=qmc.PoissonDisk(d=2,radius=.061,ncandidates=50,seed=seed+300).fill_space()
    if len(allpts)<N:raise RuntimeError('Poisson underfilled')
    sel=[int(np.random.default_rng(seed+10).integers(len(allpts)))]
    dist=np.sum((allpts-allpts[sel[0]])**2,1)
    for _ in range(N-1):
        dist[sel[-1]]=-1
        j=int(np.argmax(dist));sel.append(j)
        dist=np.minimum(dist,np.sum((allpts-allpts[j])**2,1))
    poisson=allpts[sel]
    joint=optimize(seed,labels,True)
    sub=optimize(seed,labels,False)
    phases=np.random.default_rng(seed+901).random((K,2))
    broken=joint.copy()
    for t in range(K):broken[labels==t]=(broken[labels==t]+phases[t])%1
    return {'grid':grid,'sobol':sob,'poisson_disk':poisson,'spectral_joint':joint,'spectral_sub':sub,'joint_phase_broken':broken,'random':rng.random((N,2))},labels

def reads(images,p):
    # independent scalar bilinear readings; no access to labels
    pos=p*25-.5
    return np.vstack([map_coordinates(im,[pos[:,1],pos[:,0]],order=1,mode='nearest') for im in images])

def spectral(p,l):
    z=np.exp(2j*np.pi*(p@LOW_K.T))
    return {'union':float(np.mean(np.abs(z.mean(0))**2)),
            'individual':float(np.mean([np.mean(np.abs(z[l==i].mean(0))**2) for i in range(K)]))}

def main(outdir):
    t0=time.perf_counter()
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    images=np.asarray(data.lfw_subset(),dtype=np.float64)
    assert images.shape==(200,25,25) and images.min()>=0 and images.max()<=1
    y=np.r_[np.ones(100,dtype=int),np.zeros(100,dtype=int)]
    clean=images
    rng=np.random.default_rng(240301)
    noise=np.clip(images+rng.normal(0,.13,size=images.shape),0,1)
    occluded=images.copy()
    for i in range(len(images)):
        iy=int(rng.integers(0,20));ix=int(rng.integers(0,20))
        occluded[i,iy:iy+6,ix:ix+6]=0
    cond={'clean':clean,'noise13':noise,'occlusion6':occluded}
    raw=[];geom=[];sourcehash=hashlib.sha256(images.tobytes()).hexdigest()
    for seed in SEEDS:
        gs,lab=geometries(seed)
        for m,p in gs.items():
            assert p.shape==(N,2) and np.isfinite(p).all() and np.all((p>=0)&(p<1))
            geom.append(dict(seed=seed,method=m,**spectral(p,lab)))
        cache={condition:{m:reads(img,p) for m,p in gs.items()} for condition,img in cond.items()}
        for fold_seed in FOLDS:
            cv=StratifiedKFold(5,shuffle=True,random_state=fold_seed)
            for fold,(tr,te) in enumerate(cv.split(images,y)):
                # Learned sensor locations; only labels in TRAIN available for selecting coordinates.
                f,_=f_classif(images[tr].reshape(len(tr),625),y[tr]);f=np.nan_to_num(f,nan=-1,posinf=1e15)
                idx=np.sort(np.argsort(f,kind='stable')[-N:])
                for m in METHODS:
                    if m=='supervised_kbest':
                        Xtr=clean[tr].reshape(len(tr),625)[:,idx]
                        Xtests={name:img[te].reshape(len(te),625)[:,idx] for name,img in cond.items()}
                    elif m=='full_pixels':
                        Xtr=clean[tr].reshape(len(tr),625)
                        Xtests={name:img[te].reshape(len(te),625) for name,img in cond.items()}
                    else:
                        Xtr=cache['clean'][m][tr]
                        Xtests={name:cache[name][m][te] for name in cond}
                    clf=SVC(kernel='rbf',C=2.0,gamma='scale',class_weight='balanced')
                    clf.fit(Xtr,y[tr])
                    for condition,Xte in Xtests.items():
                        pred=clf.predict(Xte)
                        for k,ix in enumerate(te):
                            raw.append(dict(seed=seed,fold_seed=fold_seed,fold=fold,method=m,condition=condition,
                                            image_id=int(ix),label=int(y[ix]),correct=int(pred[k]==y[ix])))
        print('COMPLETED',seed,'records',len(raw),flush=True)
    outdict={'id':'LARP-VISION-C04','code_sha_note':'verify committed source SHA','source_image_sha256':sourcehash,
             'methods':METHODS,'seeds':SEEDS,'fold_random_states':FOLDS,'steps':STEPS,'N':N,
             'observations':raw,'geometry':geom,'versions':{'python':platform.python_version(),
                 'numpy':np.__version__,'scipy':scipy.__version__,'sklearn':__import__('sklearn').__version__,
                 'torch':torch.__version__},'elapsed_sec':time.perf_counter()-t0}
    f=out/'c04_results.json';f.write_text(json.dumps(outdict,indent=2))
    summary=[]
    for m in METHODS:
        for condition in cond:
            a=[r['correct'] for r in raw if r['method']==m and r['condition']==condition]
            summary.append({'method':m,'condition':condition,'accuracy':float(np.mean(a)),'num_predictions':len(a)})
    (out/'c04_means.json').write_text(json.dumps(summary,indent=2))
    print('WROTE',f,'SHA256',hashlib.sha256(f.read_bytes()).hexdigest(),'ELAPSED',round(time.perf_counter()-t0,1),flush=True)
if __name__=='__main__':
    torch.set_num_threads(2)
    main(sys.argv[1] if len(sys.argv)>1 else '.')
