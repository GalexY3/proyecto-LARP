"""Run exact archived Scale3D v2 code, without modifying the optimizer.
Exploratory runs. Seeds predetermined in prereg/BR30_DYNAMIC_20261021.md.
CVT comparison separately using BR12-refined independent geometries.
"""
from pathlib import Path
import sys, json, time
import numpy as np
import torch
from scale3d import scale3d_geometry_v2 as g
from scale3d import scale3d_geometry as v1
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'data';OUT.mkdir(exist_ok=True)
N=4096

def generate(seed,iterations=600):
    rng=np.random.default_rng(seed)
    initial=rng.random((N,3))
    labels=rng.permutation(np.repeat(np.arange(5),v1.hamilton_counts(N)))
    p=OUT/f'orig_{seed}.npz'
    record={'seed':seed,'N':N,'iterations':iterations,'generator_sha_v1':'220096b284fa928a8090cb73abb1fafb71c40a753614491feb5a3b26f0e98cf2','generator_sha_v2':'5f2bec63ae2e6b05e528af89173ca1975fd82d3422b15773cbade82636822d7c'}
    arrays={'initial':initial,'labels':labels}
    for name,sp in [('local',False),('mhu',True)]:
        result=g.generate(seed,N,iterations=iterations,spectral=sp,validate=False)
        pts=result['coordinates'].detach().cpu().numpy()
        assert np.array_equal(result['labels'].cpu().numpy(),labels)
        assert np.isfinite(pts).all() and np.all((pts>=0)&(pts<1))
        arrays[name]=pts
        record[name]={'construction':result['construction'],'history':result['history']}
        print('COMPLETE',seed,name,'secs',result['construction']['elapsed_seconds_including_exact_validation'],flush=True)
    np.savez_compressed(p,**arrays)
    (OUT/f'orig_{seed}.json').write_text(json.dumps(record,indent=2))
    print('SAVED',seed,p,flush=True)
if __name__=='__main__':
    torch.set_num_threads(2)
    for x in [int(z) for z in sys.argv[1:]]:generate(x)
