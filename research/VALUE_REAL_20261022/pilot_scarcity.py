"""Secondary exploratory experiment: sample complexity & transfer, no heldout-driven selection.
Depends on real_rgb_sensors.py. New methods compare cross-role spectrum vs per-role spectrum vs direct data fit.
"""
import json, time
import numpy as np
from pathlib import Path
import real_rgb_sensors as m
R=Path(__file__).resolve().parent

def experiment():
    train, _, ext=m.get_data()
    result=[]
    for n in [12,30,90,300,1800]:
        for pilot_seed in range(5):
            rng=np.random.default_rng(8800+pilot_seed)
            selected=np.concatenate([rng.choice(np.arange(i*450,(i+1)*450),n//4,replace=False) for i in range(4)]) if n<1800 else np.arange(1800)
            tr=train[selected]
            C=m.covariance_train(tr)
            diag=np.stack([np.diag(np.real(np.diag(c))) for c in C])
            methods={'POWER-DIAG':diag,'COSI-FULL':C,'COSI-SHRINK':.5*C+.5*diag}
            for method in ['POWER-DIAG','COSI-FULL','COSI-SHRINK','DIRECT-EMPIRICAL']:
                for layout_seed in range(3):
                    seed=9600+layout_seed
                    if method=='DIRECT-EMPIRICAL':ids,_=m.greedy_direct(tr,seed,passes=3)
                    else:ids,_=m.spectral_layout(methods[method],seed)
                    result.append({'pilot':len(tr),'pilot_seed':pilot_seed,'layout_seed':layout_seed,'method':method,
                        'rocket':m.evaluate(ids,ext['rocket'])[0],'hubble':m.evaluate(ids,ext['hubble_deep_field'])[0]})
        print('done pilots',n,flush=True)
    aggregate={}
    for n in [12,28,88,300,1800]:
        aggregate[str(n)]={}
        for method in ['POWER-DIAG','COSI-FULL','COSI-SHRINK','DIRECT-EMPIRICAL']:
            r=[z for z in result if z['pilot']==n and z['method']==method]
            aggregate[str(n)][method]={'rocket':float(np.mean([z['rocket'] for z in r])),'hubble':float(np.mean([z['hubble'] for z in r])),
                'mean_two_scenes':float(np.mean([(z['rocket']+z['hubble'])/2 for z in r]))}
    (R/'pilot_scarcity_results.json').write_text(json.dumps({'notice':'Exploratory; independent pilot seeds/layout seeds but only two external scenes','all':result,'summary':aggregate},indent=2))
    print(json.dumps(aggregate,indent=2),flush=True)
if __name__=='__main__':experiment()
