from laboratorio_ab4 import build, metrics, spectral, N,A,M
import numpy as np,json,time
from pathlib import Path
O=Path(__file__).resolve().parent/'ab4_data'
bands={
 'entrenada_k1':np.array([(x,y,z) for x in (-1,0,1) for y in (-1,0,1) for z in (-1,0,1) if (x,y,z)!=(0,0,0) and (x,y,z)>(0,0,0)],float),
 'no_entrenada_k2_3':np.array([(x,y,z) for x in range(-3,4) for y in range(-3,4) for z in range(-3,4) if 4 <= x*x+y*y+z*z <= 9 and (x,y,z)>(0,0,0)],float),
 'no_entrenada_k5_7':np.array([(x,y,z) for x in range(-7,8) for y in range(-7,8) for z in range(-7,8) if 25<= x*x+y*y+z*z <= 49 and (x,y,z)>(0,0,0)],float)
}

def calcbands(P,K):
 results=[]
 for a in range(A):
  U=P[a*M:(a+1)*M]
  v=np.exp(2j*np.pi*U@K.T).mean(axis=0)
  results.append(float(np.mean(np.abs(v)**2)))
 return float(np.mean(results))

rows=[]
for seed in range(701,713):
 for name,P in build(seed).items():
  z={'seed':seed,'method':name,**{b:calcbands(P,K) for b,K in bands.items()}}
  z.update({k:metrics(P,seed)[k] for k in ['cover_p95','drop_p95']})
  rows.append(z)
 print('seed',seed,flush=True)
(O/'bands.json').write_text(json.dumps(rows,indent=2))
for m in sorted(set(r['method'] for r in rows)):
 print(m, ' '.join(f'{b}={np.mean([r[b] for r in rows if r["method"]==m]):.5f}' for b in bands),flush=True)
