"""C06 repair control: distinguish learned robustness from simple image smoothing/pooling.
Not an extra cycle; compare equal-parameter MLP preprocessed raw digits.
"""
from pathlib import Path
import numpy as np,json
from scipy.ndimage import rotate,gaussian_filter
from src.cycle6_robust import train_eval
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
def blur(im):return gaussian_filter(im,sigma=(0,.8,.8))
def pool(im):
    b=blur(im);pooled=b.reshape(len(b),4,2,4,2).mean(axis=(2,4)).reshape(len(b),16)
    return np.tile(pooled,(1,5))
if __name__=='__main__':
    z=np.load(D/'digits_split.npz');im=z['images'].astype(float);y=z['y'];itr=z['train'];iva=z['val'];ite=z['test']
    rng=np.random.default_rng(99128);orig=im[ite]
    corruption={'clean':orig,'gaussian_noise':np.clip(orig+rng.normal(0,.17,size=orig.shape),0,1),'block_occlusion':orig.copy(),'rotation_pm12':np.stack([rotate(a,float(rng.choice([-12,12])),reshape=False,order=1,mode='constant',cval=0) for a in orig])}
    for i in range(len(orig)):
        r=int(rng.integers(1,6));c=int(rng.integers(1,6));corruption['block_occlusion'][i,r:r+2,c:c+2]=0
    results={}
    for kind in ['blur64','blur_pool80']:
        f=(lambda arr: blur(arr).reshape(len(arr),64)) if kind=='blur64' else pool
        input=f(im).astype('float32');ext={k:f(v).astype('float32') for k,v in corruption.items()}
        out=[]
        for rs in [991,992,993,994]:
            ans=train_eval(input,y,itr,iva,ite,ext,seed=rs)
            out.append({'seed':rs,**ans})
        results[kind]=out
        print('C06 repair',kind,{k:float(np.mean([x['accuracy'][k] for x in out])) for k in ext},flush=True)
    (D/'C06_controls.json').write_text(json.dumps({'type':'repair of C06 baseline preprocessing confound; not a new cycle','conditions':results,'qualification':'A Gaussian blur and downsampling use all image pixels rather than exactly 128 sensor readings; these controls test representational inductive bias, not equal sensing cost.'},indent=2))
