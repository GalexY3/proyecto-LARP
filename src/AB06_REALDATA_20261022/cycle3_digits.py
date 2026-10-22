"""C03: external-to-Fourier UCI Digits 8x8, five role-specific sensor modalities.
3D point clouds projected into (x,y) image domain: explicit domain mismatch.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.ndimage import gaussian_filter, sobel, laplace, map_coordinates
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';
SEEDS=[8101,8102,8103,8104]; NAMES=['local','mhu','cvt','sobol','random']
digits=load_digits();im=digits.images.astype(np.float64)/16;Y=digits.target.astype(int)
idx=np.arange(len(Y));itr,ite=train_test_split(idx,test_size=.25,stratify=Y,random_state=811);itr,iva=train_test_split(itr,test_size=.19,stratify=Y[itr],random_state=812)
np.savez_compressed(D/'digits_split.npz',train=itr,val=iva,test=ite,images=im.astype('float32'),y=Y)
modalities=np.stack([im,gaussian_filter(im,(0,.85,.85)),sobel(im,axis=2)/8,sobel(im,axis=1)/8,-laplace(gaussian_filter(im,(0,.75,.75)))/5],axis=1)
centres=np.array([[(a+.5)/4,(b+.5)/4] for a in range(4) for b in range(4)],dtype=float)
trg=np.array([[(a+.5)/8,(b+.5)/8] for a in range(8) for b in range(8)],float)

# 8x8 images, always sample nearest valid edge (not periodic image data)
def sample(arr,positions):
    n=len(arr);m=len(positions)
    coords=np.array([np.repeat(np.arange(n),m),np.tile(positions[:,0]*7,n),np.tile(positions[:,1]*7,n)])
    return map_coordinates(arr,coords,order=1,mode='nearest').reshape(n,m)

def basis(positions,targets,sigma=.16):
    d2=np.sum((positions[:,None,:]-targets[None,:,:])**2,axis=2)
    B=np.exp(-.5*d2/sigma**2)
    return B/(B.sum(axis=0,keepdims=True)+1e-9)

def make_features(geo,role=True):
    p=geo['points']; lab=geo['labels'];Z=[]
    for t in range(5):
        ix=np.where(lab==t)[0]; pts=p[ix,:2]
        modality=t if role else 0
        X=sample(modalities[:,modality],pts)
        Z.append(X@basis(pts,centres))
    return np.concatenate(Z,axis=1).astype('float32')

if __name__=='__main__':
    entries=[]
    for seed in SEEDS:
        z=np.load(D/f'geo_{seed}.npz');lab=z['labels'];
        for name in NAMES:
            pp=z[name];g={'points':pp,'labels':lab}
            F=make_features(g,role=True)
            Fsame=make_features(g,role=False)
            np.savez_compressed(D/f'digits_features_{seed}_{name}.npz',features=F,homogeneous=Fsame)
            rare=(lab==4);pts=pp[rare,:2]
            # Observational mean nearest type-4 distance in image (not a model fit)
            from scipy.spatial import cKDTree
            d,_=cKDTree(pts).query(trg,k=1)
            # Intensity class (type0): reconstruct digit image by RBF readings at original sensor positions
            ip=pp[lab==0,:2]; read=sample(im,ip)
            recon=read@basis(ip,trg,sigma=.11)
            mse=float(np.mean((recon.reshape(-1,8,8)-im)**2))
            entries.append({'seed':seed,'geometry':name,'mean_distance_rare_type':float(np.mean(d)),'gray_reconstruction_mse':mse,'features_sha256':hashlib.sha256((D/f'digits_features_{seed}_{name}.npz').read_bytes()).hexdigest()})
        print('C03',seed,{r['geometry']:round(r['gray_reconstruction_mse'],4) for r in entries[-5:]},flush=True)
    (D/'C03.json').write_text(json.dumps({'benchmark':'UCI Optical Digits as distributed by sklearn, 1797 8x8 images, non-Fourier and never used in geometry optimization','train':len(itr),'val':len(iva),'test':len(ite),'modality_roles':['intensity','blur','horizontal derivative','vertical derivative','negative LoG'],'feature_shape':[len(im),80],'projection_warning':'3D Scale3D geometries projected into 2D; not an architecture tuned for digit data','records':entries},indent=2))
