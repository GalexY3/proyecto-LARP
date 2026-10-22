"""C04: matched-parameter MLP on real UCI Digits; preselected val early stopping, same update cap."""
from pathlib import Path
import time,json,hashlib
import numpy as np
import torch
from torch import nn
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
torch.set_num_threads(2)
NAMES=['local','mhu','cvt','sobol','random'];SEEDS=[8101,8102,8103,8104]

def evaluate(X,y,itr,iva,ite,trainseed=991,cap=240,hidden=None):
    torch.manual_seed(trainseed)
    # training set preprocessing only
    mu=X[itr].mean(0);sd=X[itr].std(0);sd=np.where(sd<1e-5,1,sd)
    X=((X-mu)/sd).clip(-9,9).astype('float32')
    tx=torch.from_numpy(X);ty=torch.from_numpy(y)
    in_dim=X.shape[1];hidden=hidden or (64 if in_dim==80 else 78)
    model=nn.Sequential(nn.Linear(in_dim,hidden),nn.ReLU(),nn.Linear(hidden,10))
    params=sum(a.numel() for a in model.parameters())
    optimizer=torch.optim.AdamW(model.parameters(),lr=.012,weight_decay=.001)
    loss=nn.CrossEntropyLoss()
    history=[];best=-1;checkpoint=None;bad=0;patience=45
    for epoch in range(cap):
        model.train();optimizer.zero_grad(set_to_none=True)
        logits=model(tx[itr]);L=loss(logits,ty[itr]);L.backward();optimizer.step()
        model.eval()
        with torch.no_grad():
            vp=model(tx[iva]);vacc=float((vp.argmax(1)==ty[iva]).float().mean());vl=float(loss(vp,ty[iva]));tracc=float((model(tx[itr]).argmax(1)==ty[itr]).float().mean())
        history.append({'step':epoch+1,'train_loss':float(L),'train_acc':tracc,'val_acc':vacc,'val_loss':vl})
        # Choose checkpoint on val loss; never use test before checkpoint selected
        if best<0 or vl<best-1e-5:
            best=vl;bad=0;checkpoint={k:v.clone() for k,v in model.state_dict().items()};selected_epoch=epoch+1
        else:bad+=1
        if bad>=patience:break
    model.load_state_dict(checkpoint);model.eval()
    with torch.no_grad():
        test=model(tx[ite]);test_acc=float((test.argmax(1)==ty[ite]).float().mean());test_loss=float(loss(test,ty[ite]));
        predicted=test.argmax(1).numpy()
    return {'test_acc':test_acc,'test_loss':test_loss,'best_val_loss':best,'selected_step':selected_epoch,'steps_executed':len(history),'last_val_loss':history[-1]['val_loss'],'params':params,'history':history,'test_pred':predicted.tolist()}

if __name__=='__main__':
    z=np.load(D/'digits_split.npz');y=z['y'];itr=z['train'];iva=z['val'];ite=z['test'];I=z['images']
    out=[]
    for seed in SEEDS:
        for name in NAMES:
            X=np.load(D/f'digits_features_{seed}_{name}.npz')['features']
            result=evaluate(X,y,itr,iva,ite,trainseed=991)
            out.append({'geometry_seed':seed,'name':name,'role':'five_different','result':result})
            print('C04',seed,name,'test_acc',round(result['test_acc'],3),'step',result['selected_step'],'params',result['params'],flush=True)
    for modelseed in [991,992,993,994]:
        baseline=evaluate(I.reshape(-1,64),y,itr,iva,ite,trainseed=modelseed)
        out.append({'geometry_seed':None,'name':'pixel_mlp','role':'raw_pixels','model_seed':modelseed,'result':baseline})
        print('C04 baseline',modelseed,'test',round(baseline['test_acc'],3),flush=True)
    (D/'C04.json').write_text(json.dumps({'outcomes':out,'condition':'single_full_batch_step_per_epoch; AdamW .012 wd .001; val patience45; caps 240, locked stratified split; test read after checkpoint selection; same training samples and update cap, ~matched param counts; preprocessing cost not equal'},indent=2))
