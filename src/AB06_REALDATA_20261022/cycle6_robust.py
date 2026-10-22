"""C06: clean and held-out covariate shift on real digits, using C05-preferred intensity-only operator.
Never tune on distorted test images, checkpoint selected on clean validation.
"""
from pathlib import Path
import json
import numpy as np
from scipy.ndimage import rotate
from src.cycle3_digits import sample,basis,centres
from src.cycle4_train import torch,nn
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
SEEDS=[8101,8102,8103,8104];NAMES=['local','mhu','cvt','sobol','random']

def enc_gray(images,p,lab):
    out=[]
    for t in range(5):
        pts=p[lab==t,:2];r=sample(images,pts);out.append(r@basis(pts,centres))
    return np.concatenate(out,axis=1).astype('float32')

def train_eval(X,y,itr,iva,ite,ext,seed=991,steps=240,hidden=None):
    torch.manual_seed(seed);torch.set_num_threads(2)
    mu=X[itr].mean(0);sd=np.maximum(X[itr].std(0),1e-5);sd=np.where(sd<1e-5,1,sd)
    tr=torch.from_numpy(np.clip((X-mu)/sd,-9,9).astype('float32'));ty=torch.from_numpy(y)
    test={key:torch.from_numpy(np.clip((v-mu)/sd,-9,9).astype('float32')) for key,v in ext.items()}
    n=X.shape[1];h=hidden or (64 if n==80 else 78)
    net=nn.Sequential(nn.Linear(n,h),nn.ReLU(),nn.Linear(h,10));optimizer=torch.optim.AdamW(net.parameters(),lr=.012,weight_decay=.001)
    loss=nn.CrossEntropyLoss();best=np.inf;st=None;bad=0
    for ep in range(steps):
        net.train();optimizer.zero_grad();L=loss(net(tr[itr]),ty[itr]);L.backward();optimizer.step()
        net.eval()
        with torch.no_grad():vl=float(loss(net(tr[iva]),ty[iva]).item())
        if vl<best-1e-5:best=vl;bad=0;st={k:v.clone() for k,v in net.state_dict().items()};bestep=ep+1
        else:bad+=1
        if bad>=45:break
    net.load_state_dict(st);net.eval()
    with torch.no_grad():
        res={key:float((net(v).argmax(1)==ty[ite]).float().mean().item()) for key,v in test.items()}
    return {'accuracy':res,'best_step':bestep,'params':sum(a.numel() for a in net.parameters())}

if __name__=='__main__':
    z=np.load(D/'digits_split.npz');Y=z['y'];im=z['images'].astype(float);itr=z['train'];iva=z['val'];ite=z['test']
    rng=np.random.default_rng(99128);orig=im[ite]
    corruption={
        'clean':orig,
        'gaussian_noise':np.clip(orig+rng.normal(0,.17,size=orig.shape),0,1),
        'block_occlusion':orig.copy(),
        'rotation_pm12':np.stack([rotate(a,float(rng.choice([-12,12])),reshape=False,order=1,mode='constant',cval=0) for a in orig])
    }
    for i in range(len(orig)):
        r=int(rng.integers(1,6));c=int(rng.integers(1,6));corruption['block_occlusion'][i,r:r+2,c:c+2]=0
    measures=[]
    for seed in SEEDS:
        zz=np.load(D/f'geo_{seed}.npz');lab=zz['labels']
        for name in NAMES:
            X=np.load(D/f'digits_features_{seed}_{name}.npz')['homogeneous']
            ext={key:enc_gray(val,zz[name],lab) for key,val in corruption.items()}
            res=train_eval(X,Y,itr,iva,ite,ext)
            measures.append({'geometry_seed':seed,'method':name,**res})
            print('C06',seed,name,'clean',round(res['accuracy']['clean'],3),'rot',round(res['accuracy']['rotation_pm12'],3),'noise',round(res['accuracy']['gaussian_noise'],3),flush=True)
    for rs in [991,992,993,994]:
        X=im.reshape(-1,64).astype('float32');ext={key:val.reshape(len(val),64).astype('float32') for key,val in corruption.items()}
        res=train_eval(X,Y,itr,iva,ite,ext,seed=rs)
        measures.append({'geometry_seed':None,'method':'pixel_mlp','model_seed':rs,**res})
        print('C06 baseline',rs,res['accuracy'],flush=True)
    (D/'C06.json').write_text(json.dumps({'corruptions':['noise sigma .17','2x2 occlusion random position','rotate +/-12deg'],'choice_after_C05':'intensity-only functional ablation chosen because it improved clean benchmark','paired_test_images':True,'not_independent_digits':'all corruption variants generated from the same held-out images; geometry replicates n=4, model seeds n=4','measures':measures},indent=2))
