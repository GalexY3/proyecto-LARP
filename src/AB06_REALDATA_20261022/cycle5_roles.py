"""C05: isolate functional heterogeneity by changing ONLY the role-to-signal map."""
from pathlib import Path
import json,numpy as np
from src.cycle4_train import evaluate
D=Path(__file__).resolve().parents[1]/'data'
SEEDS=[8101,8102,8103,8104]; NAMES=['local','mhu','cvt','sobol','random']
if __name__=='__main__':
    zz=np.load(D/'digits_split.npz');y=zz['y'];itr=zz['train'];iva=zz['val'];ite=zz['test']
    old=json.loads((D/'C04.json').read_text())['outcomes']
    records=[]
    for seed in SEEDS:
        for name in NAMES:
            X=np.load(D/f'digits_features_{seed}_{name}.npz')['homogeneous']
            out=evaluate(X,y,itr,iva,ite,trainseed=991,cap=240)
            orig=next(o for o in old if o['name']==name and o['geometry_seed']==seed)['result']['test_acc']
            records.append({'seed':seed,'geometry':name,'all_five_roles_intensity':out['test_acc'],'functional_roles':orig,'functional_minus_homogeneous':orig-out['test_acc'],'homogeneous_selected_step':out['selected_step'],'train_params':out['params']})
            print('C05',seed,name,'roles',round(orig,3),'homog',round(out['test_acc'],3),'delta',round(orig-out['test_acc'],3),flush=True)
    sums={name:float(np.mean([r['functional_minus_homogeneous'] for r in records if r['geometry']==name])) for name in NAMES}
    (D/'C05.json').write_text(json.dumps({'records':records,'mean_delta':sums,'causal_intervention':'same coordinates and labels, same 80 input dimensionality and MLP optimization; only replace type-specific image operators with identical intensity operator','warning':'Different transforms can change signal content, not just ontology; performance gain/loss is task-dependent, 4 independent geometries'},indent=2))
