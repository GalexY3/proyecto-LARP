from common import *
from copy import deepcopy
def run():
 im,y,tr,va,te=dataset();X=im.reshape(-1,64);Q=np.linalg.qr(np.random.default_rng(60226).normal(size=(80,80)))[0];qt=torch.from_numpy(Q);rows=[]
 for g in GSEEDS:
  for method in ['mhu','cvt']:
   M=encoder_matrix(g,method);F=X@M;mu,sd=normalize_fit(F,tr,'global');Z=torch.from_numpy(((F[tr]-mu)/sd).astype('float64'));ZR=Z@qt;ty=torch.from_numpy(y[tr]);N=M/sd[0];kr=float(np.max(abs(N@N.T-(N@Q)@(N@Q).T)))
   for optname in ['SGD','AdamW']:
    torch.manual_seed(991);a=nn.Sequential(nn.Linear(80,64),nn.ReLU(),nn.Linear(64,10)).double();b=deepcopy(a)
    with torch.no_grad():b[0].weight.copy_(a[0].weight@qt)
    Opt=torch.optim.SGD if optname=='SGD' else torch.optim.AdamW;lr=.05 if optname=='SGD' else .012;oa=Opt(a.parameters(),lr=lr,weight_decay=.001);ob=Opt(b.parameters(),lr=lr,weight_decay=.001);trace=[]
    for step in range(61):
     aa=a(Z);bb=b(ZR);err=float(torch.max(abs(aa-bb)).detach())
     if step in [0,1,10,60]:trace.append({'step':step,'max_logit_delta':err,'loss_original':float(nn.functional.cross_entropy(aa,ty).detach()),'loss_rotated':float(nn.functional.cross_entropy(bb,ty).detach())})
     if step==0:assert err<1e-10
     if optname=='SGD':assert err<1e-8
     if step<60:
      oa.zero_grad();ob.zero_grad();nn.functional.cross_entropy(aa,ty).backward();nn.functional.cross_entropy(bb,ty).backward();oa.step();ob.step()
    rows.append({'geometry':g,'method':method,'optimizer':optname,'K_residual':kr,'trace':trace})
 return {'rows':rows,'summary':{opt:{'max_final_delta':max(r['trace'][-1]['max_logit_delta'] for r in rows if r['optimizer']==opt),'max_step1_delta':max(r['trace'][1]['max_logit_delta'] for r in rows if r['optimizer']==opt)} for opt in ['SGD','AdamW']},'evaluation':'Training trajectory only; validation/test not scored.'}
