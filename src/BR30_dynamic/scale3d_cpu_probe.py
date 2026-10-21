"""AB exploratory scaled-down CPU probe using archived original SpatialNetwork/Block.
No claim of equivalence to GPU Scale3D v2 original size. Frozen before training if committed.
All arms equal network (width48, layers4), fixed training/val/test worlds and query sets,
with geometry-specific inputs and adjacency. Single geometry seed 5201.
"""
import argparse,math,time,json,hashlib
from pathlib import Path
import numpy as np,torch
from larp.scale3d_train import SpatialNetwork,graph_data,features_at,observations,targets,world
from evaluate_orig import load
ROOT=Path(__file__).resolve().parent; D=ROOT/'data';D.mkdir(exist_ok=True)
MODES=np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,-1,0],[0,1,-1],[1,0,-1]],dtype=float)

def run(name,geom_seed=5201,init_seed=444,steps=220):
 torch.set_num_threads(2); torch.manual_seed(init_seed)
 g,labels=load(geom_seed)
 p=torch.tensor(g[name],dtype=torch.float32);lab=torch.tensor(labels,dtype=torch.long)
 rng=np.random.default_rng(27771)
 trq=torch.tensor(rng.random((80,3)),dtype=torch.float32)
 vaq=torch.tensor(rng.random((80,3)),dtype=torch.float32)
 teq=torch.tensor(rng.random((80,3)),dtype=torch.float32)
 trgraph,_=graph_data(p,lab,trq,degree=12,device=torch.device('cpu'))
 valgraph,_=graph_data(p,lab,vaq,degree=12,device=torch.device('cpu'))
 testgraph,_=graph_data(p,lab,teq,degree=12,device=torch.device('cpu'))
 modes=torch.tensor(MODES,dtype=torch.float32)
 nodephi=features_at(p,modes)
 trainphi=features_at(trq,modes)
 valphi=features_at(vaq,modes)
 testphi=features_at(teq,modes)
 model=SpatialNetwork(width=48,layers=4)
 param_count=sum(p.numel() for p in model.parameters());optimizer=torch.optim.AdamW(model.parameters(),lr=0.0007,weight_decay=0.0001)

 def dataset(lo,hi,graph,q,phi):
  xs=[];ys=[]
  for seed in range(lo,hi):
   coeff=world(seed,1,len(MODES),torch.device('cpu'))
   x=observations(coeff,nodephi,lab)
   targ=targets(torch.einsum('bcd,qd->bqc',coeff,phi),2)
   xs.append(x);ys.append(targ)
  return torch.cat(xs),torch.cat(ys)
 train_x,train_y=dataset(120001,120097,trgraph,trq,trainphi)
 valid_x,valid_y=dataset(220001,220017,valgraph,vaq,valphi)
 test_x,test_y=dataset(320001,320025,testgraph,teq,testphi)

 def evaluate(x,y,graph,q):
  model.eval();total=0
  with torch.no_grad():
   for start in range(0,len(x),2):
    yh=model(x[start:start+2],graph,q,2)
    total+=float(((yh-y[start:start+2])**2).sum())
  return total/y.numel()

 start=time.perf_counter();best=float('inf');snapshot=None;history=[]
 gen=torch.Generator().manual_seed(125556)
 for i in range(steps):
  model.train();idx=torch.randint(len(train_x),(2,),generator=gen)
  pred=model(train_x[idx],trgraph,trq,2)
  loss=((pred-train_y[idx])**2).mean()
  optimizer.zero_grad(set_to_none=True);loss.backward();optimizer.step()
  if (i+1)%20==0 or i==0 or i==steps-1:
   val=evaluate(valid_x,valid_y,valgraph,vaq)
   if val<best:
    best=val;snapshot={k:v.detach().clone() for k,v in model.state_dict().items()}
   history.append({'update':i+1,'train_loss':float(loss),'validation_mse':val})
   print(name,'update',i+1,'train',round(float(loss),3),'val',round(val,3),flush=True)
 model.load_state_dict(snapshot)
 test=evaluate(test_x,test_y,testgraph,teq)
 result={'name':name,'geom_seed':geom_seed,'seed_model':init_seed,'parameters':param_count,'layers':4,'width':48,'k':12,'steps':steps,'train_worlds':96,'validation_worlds':16,'test_worlds':24,'training_queries':80,'test_queries':80,'best_validation_mse':best,'test_mse':test,'runtime_sec':time.perf_counter()-start,'history':history, 'classification':'EXPLORATORY_CPU_SCALED_NETWORK_NOT_EXACT_GPU_SCALE3D'}
 (D/f'probe_{geom_seed}_{name}_{init_seed}.json').write_text(json.dumps(result,indent=2))
 print('FINAL',name,'TEST_MSE',test,'SECS',result['runtime_sec'],flush=True)
 return result

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--name',choices=['initial','local','mhu','cvt_refined_1701'],required=True);a.add_argument('--geom-seed',type=int,default=5201);a.add_argument('--model-seed',type=int,default=444);a.add_argument('--steps',type=int,default=220);p=a.parse_args()
 run(p.name,p.geom_seed,p.model_seed,p.steps)
