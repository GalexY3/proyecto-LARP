"""Post-hoc adversarial repair of optimizer; NOT an extra AB branching cycle."""
import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import run_ab30 as x
OUT=Path(__file__).resolve().parent

def monotonic(p,C,steps=90):
    p=p.copy(); history=[x.risk(p,C)]
    for _ in range(steps):
        g=x.grad(p,C); current=history[-1]; eta=16.
        success=False
        for _ in range(22):
            q=(p-eta*g)%1;loss=x.risk(q,C)
            if loss<=current-1e-12:
                p=q;history.append(loss); success=True;break
            eta*=.5
        if not success: break
    assert np.max(np.diff(history))<=1e-10
    return p,history

def examine(t):
    original=json.loads((OUT/'ledger.jsonl').read_text().splitlines()[t-1]);v=original['parameters']
    C=x.cov(41000+t,v['coherence'],v['heterogeneity']);chat=x.pilot(C,51000+t,v['pilot_n']);eye=np.repeat(x.I[None,:,:],x.B,axis=0)
    trained=.9*chat+.1*np.trace(chat,axis1=1,axis2=2).mean()/x.A*eye
    shrunk=(1-v['shrinkage'])*trained+v['shrinkage']*np.trace(trained,axis1=1,axis2=2).mean()/x.A*eye
    row=[]
    for rep in range(3):
        seed=81000+t*10+rep;init=np.random.default_rng(seed).random((x.N,3));loc=x.local(init,20)
        variants={'MHU-monotone':eye,'COSI-monotone':trained,'COSI-shrink-monotone':shrunk,'Oracle-monotone':C}
        for name,Z in variants.items():
            geom,h=monotonic(loc,Z,90)
            row.append({'seed':seed,'method':name,'target_start':h[0],'target_end':h[-1],
              'source_RMSE':x.risk(geom,C)**.5,'shift_RMSE':x.risk(geom,x.shift(C,v['shift']))**.5,
              'outage_RMSE':x.outage(geom,C,seed+600,v['outage_radius'])**.5,
              'steps_accepted':len(h)-1})
    agg={k:{m:float(np.mean([z[m] for z in row if z['method']==k])) for m in ['source_RMSE','shift_RMSE','outage_RMSE','steps_accepted']} for k in variants}
    return {'cycle_repaired':t,'previous_regret':original['regret'],'aggregate':agg,'rows':row}
if __name__=='__main__':
    result=[examine(i) for i in range(1,31)]
    (OUT/'repair_optim.json').write_text(json.dumps({'method':'posthoc monotone linesearch, 90 steps; original data unchanged','comparisons':result},indent=2))
    for r in result:
      print('C%02d'%r['cycle_repaired'],{m:round(z['source_RMSE'],5) for m,z in r['aggregate'].items()})
