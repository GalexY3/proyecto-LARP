"""Topological countercheck, not neural training or asymptotic HU.
All graphs are undirected symmetrized Euclidean periodic kNN.
Graph Laplacian spectral gap is only a proxy for global message-mixing.
"""
from pathlib import Path
import sys,json,time
import numpy as np
from scipy.spatial import cKDTree
from scipy import sparse
from scipy.sparse.csgraph import connected_components,laplacian
from scipy.sparse.linalg import eigsh,ArpackNoConvergence
from evaluate_orig import load
R=Path(__file__).resolve().parent; D=R/'data'

def measure(seed, k=12):
 pts,labs=load(seed);rows=[]
 for name,p in pts.items():
  t0=time.perf_counter()
  idx=cKDTree(p,boxsize=1).query(p,k=k+1)[1][:,1:]
  n=len(p);r=np.repeat(np.arange(n),k);c=idx.ravel()
  A=sparse.coo_matrix((np.ones(len(r)),(r,c)),shape=(n,n)).tocsr()
  A=A.maximum(A.T).tocsr();A.data[:]=1
  ncomp,comp=connected_components(A,directed=False)
  g={'seed':seed,'name':name,'k':k,'components':int(ncomp), 'largest_fraction':float(np.bincount(comp).max()/n),'cross_type_edges':float(np.mean(labs[sparse.triu(A,k=1).nonzero()[0]]!=labs[sparse.triu(A,k=1).nonzero()[1]]))}
  if ncomp==1:
   L=laplacian(A,normed=True)
   try:
    vals=eigsh(L,k=3,which='SM',return_eigenvectors=False,tol=1e-4,maxiter=1500)
    g['spectral_gap']=float(sorted(vals)[1])
   except (ArpackNoConvergence,ValueError) as e:g['spectral_gap']=None;g['solver_error']=str(e)
  else:g['spectral_gap']=0.
  g['seconds']=time.perf_counter()-t0
  rows.append(g)
  print('TOPO',seed,name,'components',g['components'],'gap',g['spectral_gap'],'seconds',round(g['seconds'],2),flush=True)
 return rows
if __name__=='__main__':
 rows=[]
 for s in [int(i) for i in sys.argv[1:]]:rows+=measure(s)
 (D/'topology_summary.json').write_text(json.dumps(rows,indent=2))
