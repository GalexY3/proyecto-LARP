from common import *
def run():
    im,y,tr,va,te=dataset();x=im.reshape(-1,64).astype('float32')
    ext={k:v.reshape(-1,64).astype('float32') for k,v in corrupt(im[te]).items()}
    std=x[tr].std(0);tiny=np.where(std<1e-5)[0]
    out={'constant_or_tiny_features':tiny.tolist(),'train_size':len(tr),'val_size':len(va),'test_size':len(te),'models':{}}
    for mode in ['legacy','guard','fixed']:
        z=train(x,y,tr,va,te,ext,mode=mode);out['models'][mode]={k:v for k,v in z.items() if k not in ['predictions','val_curve']}
    return out
