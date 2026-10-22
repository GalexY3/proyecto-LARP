"""Reusable instruments, not a prewritten sequence of experiments.

Encoder formulas adapted explicitly from historical AB06 cycle3_digits.py.
No legacy module imports: those scripts have relocated paths and import side effects.
"""
from pathlib import Path
import os, sys, json, hashlib, time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.deps'))
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','2')
import numpy as np
import scipy
from scipy.ndimage import map_coordinates, rotate, gaussian_filter, sobel, laplace
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import torch
from torch import nn
torch.set_num_threads(2)
BASE=Path(__file__).resolve().parent
GEODIR=ROOT/'data/AB06_REALDATA_20261022'
METHODS=['local','mhu','cvt','sobol','random']
GSEEDS=[8101,8102,8103,8104]
CENTRES=np.array([[(a+.5)/4,(b+.5)/4] for a in range(4) for b in range(4)],float)

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dataset(split=(811,812)):
    d=load_digits(); images=d.images.astype(np.float64)/16; y=d.target.astype(np.int64)
    idx=np.arange(len(y)); tr,te=train_test_split(idx,test_size=.25,stratify=y,random_state=split[0])
    tr,va=train_test_split(tr,test_size=.19,stratify=y[tr],random_state=split[1])
    return images,y,tr,va,te
def corrupt(images,seed=99128):
    rng=np.random.default_rng(seed)
    out={'clean':images.copy(),'noise':np.clip(images+rng.normal(0,.17,images.shape),0,1),'occlusion':images.copy(),
         'rotation':np.stack([rotate(x,float(rng.choice([-12,12])),reshape=False,order=1,mode='constant',cval=0) for x in images])}
    for i in range(len(images)):
        a=int(rng.integers(1,6)); b=int(rng.integers(1,6)); out['occlusion'][i,a:a+2,b:b+2]=0
    return out
def sample(images,pts):
    n=len(images); m=len(pts)
    coords=np.array([np.repeat(np.arange(n),m),np.tile(pts[:,0]*7,n),np.tile(pts[:,1]*7,n)])
    return map_coordinates(images,coords,order=1,mode='nearest').reshape(n,m)
def basis(pts,targets=CENTRES,sigma=.16):
    d2=np.sum((pts[:,None,:]-targets[None,:,:])**2,axis=2)
    b=np.exp(-.5*d2/sigma**2)
    return b/(b.sum(0,keepdims=True)+1e-9)
def encode(images,p,lab,roles=False,sigma=.16):
    mods=[images]*5 if not roles else [images,gaussian_filter(images,(0,.85,.85)),sobel(images,axis=2)/8,sobel(images,axis=1)/8,-laplace(gaussian_filter(images,(0,.75,.75)))/5]
    return np.concatenate([sample(mods[t],p[lab==t,:2])@basis(p[lab==t,:2],sigma=sigma) for t in range(5)],1)
def geometry(seed,method):
    with np.load(GEODIR/f'geo_{seed}.npz') as z: return z[method].copy(),z['labels'].copy()
def encoder_matrix(seed,method,roles=False,sigma=.16):
    p,l=geometry(seed,method)
    return encode(np.eye(64).reshape(64,8,8),p,l,roles=roles,sigma=sigma)
def normalize_fit(X,tr,mode='guard'):
    mu=X[tr].mean(0); sd=X[tr].std(0)
    if mode=='legacy': sd=np.maximum(sd,1e-5);sd=np.where(sd<1e-5,1,sd)
    elif mode=='guard': sd=np.where(sd<1e-5,1,sd)
    elif mode=='fixed': mu=np.zeros(X.shape[1]);sd=np.ones(X.shape[1])
    elif mode=='global': sd=np.repeat(max(float(X[tr].std()),1e-5),X.shape[1])
    else: raise ValueError(mode)
    return mu,sd
def train(X,y,tr,va,te,ext=None,seed=991,steps=240,mode='guard',hidden=None,clip=9.,decay=.001,lr=.012,patience=45,return_model=False):
    torch.manual_seed(seed)
    X=np.asarray(X,dtype=np.float32);ext=ext or {'clean':X[te]}
    mu,sd=normalize_fit(X,tr,mode)
    def transform(a):
        z=(np.asarray(a,dtype=np.float32)-mu)/sd
        if clip is not None:z=np.clip(z,-clip,clip)
        return torch.from_numpy(z.astype('float32'))
    tx=transform(X); ty=torch.from_numpy(y)
    h=hidden or (64 if X.shape[1]==80 else 78)
    net=nn.Sequential(nn.Linear(X.shape[1],h),nn.ReLU(),nn.Linear(h,10))
    opt=torch.optim.AdamW(net.parameters(),lr=lr,weight_decay=decay)
    criterion=nn.CrossEntropyLoss(); best=np.inf; bad=0; history=[]
    start=time.perf_counter()
    for ep in range(steps):
        net.train();opt.zero_grad();loss=criterion(net(tx[tr]),ty[tr]);loss.backward();opt.step()
        net.eval()
        with torch.no_grad(): vl=float(criterion(net(tx[va]),ty[va]))
        if not np.isfinite(float(loss.detach())) or not np.isfinite(vl):
            raise FloatingPointError('Nonfinite train/validation loss; no score is valid.')
        history.append(vl)
        if vl<best-1e-5:best=vl;bad=0;state={k:v.detach().clone() for k,v in net.state_dict().items()};bestep=ep+1
        else:bad+=1
        if patience is not None and bad>=patience:break
    if not np.isfinite(best): raise RuntimeError('No finite validation checkpoint.')
    net.load_state_dict(state); net.eval()
    scores={};pred={}
    with torch.no_grad():
        for name,a in ext.items():
            pr=net(transform(a)).argmax(1).numpy();pred[name]=pr.tolist();scores[name]=float(np.mean(pr==y[te]))
    result={'accuracy':scores,'predictions':pred,'best_step':bestep,'steps':ep+1,'val_loss':best,'val_curve':history,
            'params':sum(a.numel() for a in net.parameters()),'elapsed':time.perf_counter()-start}
    return (result,net,mu,sd) if return_model else result
def version_info():
    import sklearn
    return {'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'torch':torch.__version__,'sklearn':sklearn.__version__,'threads':torch.get_num_threads()}

def finite_modes(dim,lo=1,hi=2):
    """One vector per conjugate pair; unit-torus angular wavevectors are 2*pi*q."""
    from itertools import product
    cap=int(np.ceil(np.sqrt(hi)))
    return np.array([q for q in product(range(-cap,cap+1),repeat=dim)
        if lo<=sum(x*x for x in q)<=hi and next((x for x in q if x),0)>0],float)

def amplitudes(p,labels,q):
    p=np.asarray(p,dtype=float);q=np.asarray(q,dtype=float)
    phase=np.exp(-2j*np.pi*p@q.T)
    a=np.array([phase[labels==c].sum(0)/np.sqrt(np.sum(labels==c)) for c in range(5)])
    union=phase.sum(0)/np.sqrt(len(p))
    return a,union

def finite_spectrum(p,labels,q):
    a,u=amplitudes(p,labels,q)
    return np.concatenate([np.mean(abs(a)**2,axis=1),[np.mean(abs(u)**2)]]).tolist()
