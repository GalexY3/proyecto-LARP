from common import *
def run():
    im,y,tr,va,te=dataset();x=im.reshape(-1,64).astype('float32');ext={k:v.reshape(-1,64).astype('float32') for k,v in corrupt(im[te]).items()};rows=[]
    for mode in ['guard','fixed','global']:
        z=train(x,y,tr,va,te,ext,mode=mode);rows.append({'mode':mode,**{k:v for k,v in z.items() if k not in ['predictions','val_curve']}})
    for floor in [.05,.1,.2]:
        mu=x[tr].mean(0);sd=np.maximum(x[tr].std(0),floor)
        z=train((x-mu)/sd,y,tr,va,te,{k:(v-mu)/sd for k,v in ext.items()},mode='fixed')
        rows.append({'mode':'floor_'+str(floor),**{k:v for k,v in z.items() if k not in ['predictions','val_curve']}})
    return {'rows':rows,'summary':rows}

