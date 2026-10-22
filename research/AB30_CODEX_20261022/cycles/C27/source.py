from common import *
def run():
 im,y,tr,va,te=dataset();X=im.reshape(-1,64);mu,sd=normalize_fit(X,tr,'global');Z=(X-mu)/sd;C=Z[tr].T@Z[tr]/len(tr);ev,V=np.linalg.eigh(C);Cs=(V*np.sqrt(np.maximum(ev,0)))@V.T;floor=.01*np.trace(C)/64
 metrics=[('identity',np.eye(64)),('data_diagonal',np.diag(1/(np.diag(C)+floor))),('data_covariance',np.linalg.inv(C+floor*np.eye(64)))]
 for g in GSEEDS:
  for m in ['mhu','cvt']:
   M=encoder_matrix(g,m);metrics.append((f'{m}_{g}',M@M.T))
 tx=torch.from_numpy(Z[tr].astype('float64'));vx=torch.from_numpy(Z[va].astype('float64'));ty=torch.from_numpy(y[tr]);vy=torch.from_numpy(y[va]);rows=[]
 for name,K in metrics:
  scale=float(np.linalg.eigvalsh(Cs@K@Cs)[-1]);Kt=torch.from_numpy((K/scale).astype('float64'))
  for seed in [991,992]:
   torch.manual_seed(seed);net=nn.Sequential(nn.Linear(64,64),nn.ReLU(),nn.Linear(64,10)).double();hist=[];vh=[];tic=time.perf_counter()
   for step in range(240):
    net.zero_grad();loss=nn.functional.cross_entropy(net(tx),ty);loss.backward()
    with torch.no_grad():
     net[0].weight-=.1*(net[0].weight.grad@Kt)
     for p in [net[0].bias,net[2].weight,net[2].bias]:p-=.1*p.grad
     vl=float(nn.functional.cross_entropy(net(vx),vy));tl=float(loss.detach());assert np.isfinite(tl+vl)
    hist.append(tl);vh.append(vl)
   rows.append({'metric':name,'seed':seed,'scale':scale,'train_auc':float(np.mean(hist)),'final_train_loss':hist[-1],'best_val_loss':min(vh),'final_val_loss':vh[-1],'train_curve':hist,'val_curve':vh,'elapsed_seconds':time.perf_counter()-tic,'params':sum(p.numel() for p in net.parameters())})
 fam=lambda name:name.split('_')[0] if name.startswith(('mhu_','cvt_')) else name
 return {'rows':rows,'summary':{f:{k:float(np.mean([r[k] for r in rows if fam(r['metric'])==f])) for k in ['train_auc','final_train_loss','best_val_loss','final_val_loss']} for f in ['identity','data_diagonal','data_covariance','mhu','cvt']},'scope':'SGD mechanism, exposed Digits train/validation; no test scores or convergence claim.'}
