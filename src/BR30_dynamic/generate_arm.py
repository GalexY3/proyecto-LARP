"""Resumable Scale3D v2 calls, one treatment per process; original optimizer unmodified."""
import sys,time,json
from pathlib import Path
import numpy as np, torch
from scale3d import scale3d_geometry_v2 as v2
from scale3d import scale3d_geometry as v1
D=Path(__file__).resolve().parent/'data';D.mkdir(exist_ok=True)
seed=int(sys.argv[1]); treatment=sys.argv[2];iterations=int(sys.argv[3]) if len(sys.argv)>3 else 600
if treatment not in ('local','mhu'):raise SystemExit('invalid treatment')
torch.set_num_threads(2)
r=np.random.default_rng(seed);p0=r.random((4096,3));labels=r.permutation(np.repeat(np.arange(5),v1.hamilton_counts(4096)))
z=v2.generate(seed,4096,iterations=iterations,spectral=(treatment=='mhu'),validate=False)
assert np.array_equal(z['labels'].cpu().numpy(),labels)
out=z['coordinates'].detach().cpu().numpy()
np.savez_compressed(D/f'arm_{seed}_{treatment}.npz',points=out,labels=labels,initial=p0)
(D/f'arm_{seed}_{treatment}.json').write_text(json.dumps({'sha_v2':'5f2bec63ae2e6b05e528af89173ca1975fd82d3422b15773cbade82636822d7c','construction':z['construction'],'final':z['history'][-1]},indent=2))
print(seed,treatment,z['construction']['elapsed_seconds_including_exact_validation'],flush=True)
