from common import *
def run():
    im,y,tr,va,te=dataset();x=im.reshape(-1,64).astype('float32');std=x[tr].std(0)
    ex=corrupt(im[te]); rows=[]
    for mode in ['legacy','guard','fixed']:
        mu,sd=normalize_fit(x,tr,mode);base=(x[te]-mu)/sd
        for name,img in ex.items():
            z=(img.reshape(-1,64)-mu)/sd;en=np.mean((z-base)**2,0)
            rows.append({'mode':mode,'shift':name,'energy':float(en.sum()),'rare_positive_fraction':float(en[(std>1e-5)&(std<.05)].sum()/max(en.sum(),1e-30)),'zero_fraction':float(en[std<1e-5].sum()/max(en.sum(),1e-30)),'clip_fraction':float(np.mean(np.abs(z)>9))})
    return {'std_sorted':np.sort(std).tolist(),'rows':rows}

