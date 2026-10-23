"""Post-test exploratory, not confirmatory: stronger causal forecast baselines."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'src'))
from engine import NAMES,load,forecast,split
allres=[]
for name in NAMES:
 y=load(name);n=len(y);part=split(n);lo,hi=part['development']
 pred,old_choice=forecast(y,part['development'])
 ar=np.full(n,np.nan);season=np.full(n,np.nan)
 for t in range(35,n):
  x=y[t-33:t-1]; target=y[t-32:t]
  xm=np.mean(x);ym=np.mean(target);var=np.sum((x-xm)**2)
  beta=np.dot(x-xm,target-ym)/(var+1e-8)
  beta=np.clip(beta,-2,2)
  ar[t]=ym+beta*(y[t-1]-xm)
 lag={'co2':52,'elnino':12}.get(name)
 if lag is not None: season[lag:]=y[:-lag]
 can=['persistence','mean4','ewma03','ar32']
 pred['ar32']=ar
 if lag is not None:
  pred['seasonal']=season;can.append('seasonal')
 devmae={k:float(np.nanmean(abs(y[lo:hi]-pred[k][lo:hi]))) for k in can}
 choice=min(can,key=lambda k:devmae[k]);v=np.arange(*part['test'])
 res={'dataset':name,'n_test':len(v),'best_dev_candidate':choice,'development_errors':devmae,'final_mae_strong':float(np.mean(abs(y[v]-pred[choice][v]))),'final_mae_fixed_3way':float(np.mean(abs(y[v]-pred['fixed'][v]))),'final_mae_adaptive':float(np.mean(abs(y[v]-pred['adaptive'][v]))),'final_mae_ar32':float(np.mean(abs(y[v]-ar[v]))),'final_mae_seasonal':float(np.mean(abs(y[v]-season[v]))) if lag else None,'scope':'POST_TEST_ADVERSARIAL_EXPLORATION','G':'NO_NEW_HOLDOUT'}
 assert np.isfinite(res['final_mae_strong'])
 allres.append(res);print(name,choice,res['final_mae_strong'],res['final_mae_fixed_3way'],res['final_mae_adaptive'])
 (P/'results'/'post_test_adversarial').mkdir(exist_ok=True,parents=True)
 (P/'results'/'post_test_adversarial'/f'{name}.json').write_text(json.dumps(res,indent=2)+'\n')
(P/'reports'/'POST_TEST_ADVERSARIAL.json').write_text(json.dumps(allres,indent=2)+'\n')