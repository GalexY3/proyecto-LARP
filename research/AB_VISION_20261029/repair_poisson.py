"""LARP VISION C01 POST-EXPOSURE REPAIR. Only poisson_disk arm.
Original randomized PoissonDisk.random(N) samples a partial occupied region;
this post-hoc replacement uses fill_space + density-aware thinning.
Not a prospective confirmatory correction and not a second AB cycle.
"""
import hashlib,json
from pathlib import Path
import numpy as np
from scipy.stats import qmc
from scipy.spatial import cKDTree
import vision_ab_c01 as main

def poisson_repaired(seed):
    pts=qmc.PoissonDisk(d=2,radius=.062,seed=seed,ncandidates=50).fill_space()
    if len(pts)<main.N: raise RuntimeError('Insufficient candidates')
    p=pts.copy()
    while len(p)>main.N:
        dist2=np.sum((p[:,None,:]-p[None,:,:])**2,axis=-1)
        density=np.exp(-dist2/(.09**2)).sum(axis=1)
        p=np.delete(p,int(np.argmax(density)),axis=0)
    return p

def run():
    root=Path(__file__).resolve().parent
    original=(root/'results_original.json').read_bytes()
    rec=json.loads(original)
    rec['repair']={'arm':'poisson_disk','status':'POST_EXPOSURE_REPAIR','original_sha256':hashlib.sha256(original).hexdigest(),
                   'original_error':'PoissonDisk.random(N) clustered in first explored portion of 2D domain; erroneous coverage',
                   'procedure':'PoissonDisk(radius=.062).fill_space(), remove highest Gaussian point density until N=160',
                   'interpretation':'Exploratory, not prospective confirmation, original output intact'}
    rec['results']=[r for r in rec['results'] if r['method']!='poisson_disk']
    rec['geometry']=[r for r in rec['geometry'] if r['method']!='poisson_disk']
    for seed in main.SEEDS:
        p=poisson_repaired(seed)
        labels=np.tile(np.arange(main.TYPES),main.N//main.TYPES);np.random.default_rng(seed).shuffle(labels)
        rec['geometry'].append({'seed':seed,'method':'poisson_disk',**main.geom_diagnostics(p,labels)})
        operator=main.sampler(p)
        for name in main.IMAGES:
            im=main.to_gray(name)
            vals=main.sampling_values(im,p)
            tests=[('clean',main.reconstruct(vals,operator)),('drop30',main.dropout_reconstruct(vals,p,seed+700)),
                   ('noise08',main.reconstruct(np.clip(vals+np.random.default_rng(seed+9100+main.IMAGES.index(name)).normal(0,.08,size=main.N),0,1),operator))]
            for cond,pred in tests:
                diff=pred-im
                rec['results'].append({'seed':seed,'method':'poisson_disk','image':name,
                                       'split':'DEV' if name in main.DEV else 'TEST','condition':cond,
                                       'mse':float(np.mean(diff*diff)),'mae':float(np.mean(np.abs(diff)))})
    (root/'results_repaired.json').write_text(json.dumps(rec,indent=2))
    print('REPAIR written; source original',rec['repair']['original_sha256'])
if __name__=='__main__': run()
