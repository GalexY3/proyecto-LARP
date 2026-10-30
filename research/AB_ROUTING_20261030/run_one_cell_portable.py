"""POST-OUTCOME PORTABILITY REPAIR of previously frozen checkpoint wrapper for frozen learned_followup.
All geometry, routing, training, splits and metrics imported UNCHANGED from frozen source.
Each command executes one geometry seed x field context; no result-based tuning.
"""
import json,sys,time,hashlib,platform
from pathlib import Path
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import learned_followup as F

def main(geometry_seed,context,outdir):
 assert geometry_seed in F.GSEEDS and context in F.CONTEXTS
 start=time.perf_counter();out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 torch.set_num_threads(1)
 lab=F.prev.labels_for_seed(geometry_seed)
 xx,yy=np.meshgrid((np.arange(20)+.5)/20,(np.arange(20)+.5)/20)
 pts={'grid':np.column_stack([xx.ravel(),yy.ravel()]),
      'cvt':F.prev.cvt_geometry(geometry_seed,lab),
      'mhu':F.prev.optimize_mhu(geometry_seed,lab)}
 graphs={}
 for geom,p in pts.items():
    for policy in ('knn','type'):
        graphs[f'{geom}_{policy}']=F.prev.make_edges(p,lab,policy,geometry_seed)
 train_fields={geom:[F.prev.field(p,context,fs) for fs in F.TRAIN_SEEDS] for geom,p in pts.items()}
 for geom,p in pts.items():graphs[f'{geom}_learned']=F.graph_learned(p,lab,context,train_fields[geom])
 records=[];model_checks=[];geom_checks=[]
 for method in F.METHODS:
    geom=method.split('_')[0];p=pts[geom];edges=graphs[method]
    assert edges.shape==(F.N,F.DEG) and all(len(set(row))==F.DEG for row in edges)
    assert np.all(edges!=np.arange(F.N)[:,None])
    d=np.sqrt(F.prev.distance(p,p)[np.arange(F.N)[:,None],edges])
    geom_checks.append(dict(geom_seed=geometry_seed,context=context,method=method,mean_edge_length=float(d.mean()),mean_type_coverage=float(np.mean([(len(set(lab[[i]+list(edges[i])]))/5) for i in range(F.N)]))))
    train_data=F.create_data(p,lab,edges,context,F.TRAIN_SEEDS,'clean')
    val_data=F.create_data(p,lab,edges,context,F.VAL_SEEDS,'clean')
    net,epoch,valloss=F.train_net(train_data,val_data,seed=geometry_seed*101+F.CONTEXTS.index(context)*100+F.METHODS.index(method))
    model_checks.append(dict(geom_seed=geometry_seed,context=context,method=method,val_mse=valloss,best_epoch=epoch,parameters=sum(q.numel() for q in net.parameters())))
    for shift in F.SHIFTS:
        test_data=F.create_data(p,lab,edges,context,F.TEST_SEEDS,shift)
        nmse=F.eval_net(net,test_data)
        for fs,val in zip(F.TEST_SEEDS,nmse):
            records.append(dict(cycle=f'L{(F.CONTEXTS.index(context)*4+F.SHIFTS.index(shift)+1):02d}',geometry_seed=geometry_seed,field_seed=fs,context=context,shift=shift,method=method,nmse=float(val)))
 data={'geometry_seed':geometry_seed,'context':context,'records':records,'geometry_diagnostics':geom_checks,'training_diagnostics':model_checks,
      'parent_code_sha256':F.hashfile(F.prev.__file__),'frozen_code_sha256':F.hashfile(F.__file__),
      'wrapper_code_sha256':F.hashfile(__file__),'elapsed_sec':time.perf_counter()-start,'versions':{'python':platform.python_version(),'torch':torch.__version__,'numpy':np.__version__}}
 path=out/f'cell_{geometry_seed}_{context}.json';path.write_text(json.dumps(data,sort_keys=True,separators=(',',':')))
 print('CELL_FINISHED',geometry_seed,context,'rows',len(records),'seconds',round(data['elapsed_sec'],2),'sha',F.hashfile(path),flush=True)
if __name__=='__main__':
 main(int(sys.argv[1]),sys.argv[2],sys.argv[3])
