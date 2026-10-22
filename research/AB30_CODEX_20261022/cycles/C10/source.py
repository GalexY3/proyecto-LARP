from common import *
def run():
    im,y,tr,va,te=dataset();X=im.reshape(-1,64);cor={k:v.reshape(-1,64) for k,v in corrupt(im[te]).items()}
    result,net,mup,sp=train(X,y,tr,va,te,cor,mode='global',return_model=True);net=net.double()
    W=net[0].weight.detach().numpy();b=net[0].bias.detach().numpy();rows=[]
    refs={k:net(torch.from_numpy(((x-mup)/sp).astype('float64'))).detach().numpy() for k,x in cor.items()}
    for g in GSEEDS:
        for method in ['mhu','cvt']:
            M=encoder_matrix(g,method);F=X@M;muf,sf=normalize_fit(F,tr,'global')
            Wf=(sf[0]/sp[0])*(W@np.linalg.pinv(M).T);bf=b-W@mup/sp[0]+Wf@muf/sf[0]
            for precision in ['float64','float32']:
                mapped=nn.Sequential(nn.Linear(80,78),nn.ReLU(),nn.Linear(78,10)).double()
                with torch.no_grad():
                    mapped[0].weight.copy_(torch.from_numpy(Wf));mapped[0].bias.copy_(torch.from_numpy(bf));mapped[2].load_state_dict(net[2].state_dict())
                if precision=='float32':mapped=mapped.float()
                errs=[];agreements=[]
                for k,x in cor.items():
                    z=torch.from_numpy(((x@M-muf)/sf).astype(precision));v=mapped(z).detach().numpy()
                    errs.append(float(np.max(np.abs(v-refs[k]))));agreements.append(float(np.mean(v.argmax(1)==refs[k].argmax(1))))
                rows.append({'geometry':g,'method':method,'precision':precision,'max_logit_error':max(errs),'minimum_prediction_agreement':min(agreements),'weight_norm':float(np.linalg.norm(Wf))})
    return {'pixel_accuracy':result['accuracy'],'rows':rows,'summary':{p:{'max_error':max(r['max_logit_error'] for r in rows if r['precision']==p),'min_agreement':min(r['minimum_prediction_agreement'] for r in rows if r['precision']==p)} for p in ['float64','float32']}}

