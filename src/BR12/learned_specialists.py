import json,sys,time
from pathlib import Path
import numpy as np,torch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import br30_previous as br
base=Path(__file__).resolve().parents[1]
torch.set_num_threads(2)
G={g:(np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{g}_geometry.npz'))['points'],np.load(str(Path(__file__).resolve().parents[1]/'data/geometrias'/f'{g}_geometry.npz'))['labels']) for g in ('local','mhu','random')}
for s in [1701,1702,1703]:
 d=np.load(base/'data'/f'cvt_refined_4096_{s}.npz');G[f'cvt_{s}']=(d['points'],d['labels'])

def dataset(geo,first,last,freq=1):
 p,t=geo;xx=[];yy=[]
 for seed in range(first,last+1):
  q,a,m,y=br.ds(seed,240,freq)
  _,ch,_,_=br.infer(p,t,q,a,m,k=16,band=.05 if freq==1 else .035,return_f=True)
  xx.append(ch);yy.append(y)
 return torch.tensor(np.concatenate(xx),dtype=torch.float32),torch.tensor(np.concatenate(yy)[:,None],dtype=torch.float32)

out=[]
for name,geo in G.items():
 trX,trY=dataset(geo,8101,8120);vaX,vaY=dataset(geo,8201,8205);teX,teY=dataset(geo,8301,8310)
 # ground-truth formula applied to interpolated channels is the non-learned control
 def calc(x):return x[:,0]*x[:,1]+x[:,2]*x[:,3]+.4*x[:,0]*x[:,2]*x[:,4]
 heuristic=float(((calc(teX)[:,None]-teY)**2).mean())
 for init in [2,17,41]:
  torch.manual_seed(init)
  model=torch.nn.Sequential(torch.nn.Linear(5,48),torch.nn.SiLU(),torch.nn.Linear(48,48),torch.nn.SiLU(),torch.nn.Linear(48,1))
  opt=torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=.001)
  best=float('inf');bestw=None
  for step in range(360):
   idx=torch.randint(len(trX),(192,))
   pred=model(trX[idx]);loss=torch.mean((pred-trY[idx])**2)
   opt.zero_grad();loss.backward();opt.step()
   if step%30==0 or step==359:
    with torch.no_grad():val=float(torch.mean((model(vaX)-vaY)**2))
    if val<best:best=val;bestw={k:v.detach().clone() for k,v in model.state_dict().items()}
  model.load_state_dict(bestw)
  with torch.no_grad():test=float(torch.mean((model(teX)-teY)**2))
  out.append({'method':name,'init':init,'mse_test':test,'mse_formula_control':heuristic,'val_best':best,'parameters':sum(p.numel() for p in model.parameters())})
 print(name,'trained MSE',round(float(np.mean([q['mse_test'] for q in out if q['method']==name])),5),'formula',round(heuristic,5),flush=True)
(base/'data'/'learned_specialists.json').write_text(json.dumps(out,indent=2))
