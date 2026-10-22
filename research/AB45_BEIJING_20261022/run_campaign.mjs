// Reproducible sequential exploratory research on UCI Beijing weekly aggregated data.
// Run with Node.js 20+: node run_campaign.mjs
// Input weekly_observed.json generated from 12 original station CSVs using the
// extraction protocol recorded in README. No network needed for this stage.
import {readFileSync,writeFileSync} from 'node:fs';
const data=JSON.parse(readFileSync(new URL('./weekly_observed.json',import.meta.url),'utf8'));
function runCampaign(data) {
  const ns=data.station_names.length, nf=data.fields.length, T=data.weeks, D=ns*nf;
  const feats=Array.from({length:T},(_,t)=>Array.from({length:D},(_,j)=>data.weekly[Math.floor(j/nf)][t][j%nf]));
  const targets=["PM25_MEAN","NO2_MEAN","O3_MEAN","PM25_TOP3","PM25_PM10_GAP"];
  const targetValue=(row,tar)=>{
    const f=tar==="NO2_MEAN"?2:tar==="O3_MEAN"?3:0;
    const collect=k=>Array.from({length:ns},(_,s)=>row[s*nf+k]).filter(Number.isFinite);
    let v=collect(f);
    if(v.length<10)return null;
    if(tar==="PM25_TOP3"){return [...v].sort((a,b)=>b-a).slice(0,3).reduce((a,b)=>a+b,0)/3;}
    if(tar==="PM25_PM10_GAP"){const z=collect(1);if(z.length<10)return null;return z.reduce((a,b)=>a+b,0)/z.length-v.reduce((a,b)=>a+b,0)/v.length;}
    return v.reduce((a,b)=>a+b,0)/v.length;
  };
  const Y={};for(const tar of targets)Y[tar]=feats.map(row=>targetValue(row,tar));
  const sum=a=>a.reduce((p,v)=>p+v,0);
  const mean=a=>sum(a)/a.length;
  const rng=x=>{let t=x>>>0;return ()=>{t+=0x6D2B79F5;let x=t;x=Math.imul(x^(x>>>15),x|1);x^=x+Math.imul(x^(x>>>7),x|61);return ((x^(x>>>14))>>>0)/4294967296;}};
  function solve(a,b) {
    let n=b.length, A=a.map((r,i)=>[...r,b[i]]);
    for(let c=0;c<n;c++){
      let p=c;for(let k=c+1;k<n;k++)if(Math.abs(A[k][c])>Math.abs(A[p][c]))p=k;
      if(Math.abs(A[p][c])<1e-10)A[p][c]+=1e-7;
      [A[c],A[p]]=[A[p],A[c]];
      let v=A[c][c];if(Math.abs(v)<1e-12)throw Error("singular matrix");
      for(let q=c;q<=n;q++)A[c][q]/=v;
      for(let r=0;r<n;r++){if(r===c)continue;let t=A[r][c];for(let q=c;q<=n;q++)A[r][q]-=t*A[c][q];}
    }
    return A.map(r=>r[n]);
  }
  const normal=(Xraw,indices, yy)=> {
    let valid=indices.filter(i=>Number.isFinite(yy[i])), n=valid.length;
    if(n<8)throw Error("too few target weeks "+n);
    let mu=Array.from({length:D},(_,j)=>{
      const z=valid.map(i=>Xraw[i][j]).filter(Number.isFinite);return z.length?mean(z):0;
    });
    let sd=Array.from({length:D},(_,j)=>Math.sqrt(mean(valid.map(i=>Math.pow((Number.isFinite(Xraw[i][j])?Xraw[i][j]:mu[j])-mu[j],2))))||1);
    let ymu=mean(valid.map(i=>yy[i])), ysd=Math.sqrt(mean(valid.map(i=>(yy[i]-ymu)**2)))||1;
    const tf=i=>Xraw[i].map((v,j)=>(Number.isFinite(v)?v:mu[j])-mu[j]).map((v,j)=>v/sd[j]);
    return {tf,valid,ymu,ysd};
  };
  const methods=["GREEDY","SHRINK","COSI_PROXY","TYPE","MAXMIN","RANK","DOPT","RANDOM"];
  function trial(cfg, evalStart=130, evalEnd=170, forTest=false) {
    const yy=Y[cfg.target], tin=Array.from({length:cfg.nTrain},(_,i)=>Math.min(129,Math.floor((i+.5)*130/cfg.nTrain))).filter(i=>Number.isFinite(yy[i]));
    let tr=normal(feats,tin,yy);
    let XV=tr.valid.map(tr.tf), yv=tr.valid.map(i=>(yy[i]-tr.ymu)/tr.ysd);
    const va=Array.from({length:evalEnd-evalStart},(_,i)=>evalStart+i).filter(i=>Number.isFinite(yy[i]));
    let XE=va.map(tr.tf), yE=va.map(i=>yy[i]);
    let C=Array.from({length:D},()=>Array(D).fill(0)),cy=Array(D).fill(0);
    for(let i=0;i<XV.length;i++){let r=XV[i];for(let a=0;a<D;a++){cy[a]+=r[a]*yv[i];for(let b=0;b<=a;b++)C[a][b]+=r[a]*r[b];}}
    for(let a=0;a<D;a++){cy[a]/=XV.length;for(let b=0;b<=a;b++){C[a][b]/=XV.length;C[b][a]=C[a][b];}}
    const beta=(ss)=> {
      if(!ss.length)return [];
      return solve(ss.map(j=>ss.map(k=>C[j][k]+(j===k?cfg.alpha:0))),ss.map(j=>cy[j]));
    };
    const partial=(selected,j,shrink,objective)=> {
      if(!selected.length)return objective==="div"?1:cy[j]*cy[j]/(1+cfg.alpha);
      let Csh=(a,b)=>a===b?C[a][b]:(1-shrink)*C[a][b];
      const A=selected.map(s=>selected.map(t=>Csh(s,t)+(s===t?cfg.alpha:0)));
      const k=selected.map(s=>Csh(s,j));
      let vb=solve(A,selected.map(s=>cy[s]));
      let vk=solve(A,k);
      let vr=Math.max(.005,C[j][j]+cfg.alpha-sum(k.map((z,q)=>z*vk[q])));
      if(objective==="div")return vr;
      let residual=cy[j]-sum(k.map((z,q)=>z*vb[q]));
      return residual*residual/vr;
    };
    function select(method) {
      let selected=[],cand=Array.from({length:D},(_,i)=>i),rand=rng(1234+cfg.seed*719+methods.indexOf(method)*19);
      while(selected.length<cfg.budget){
        let best=-1e9,bj=-1;
        for(const j of cand){
          let score, role=j%nf, site=Math.floor(j/nf), roleNew=+(!selected.some(s=>s%nf===role)), siteNew=+(!selected.some(s=>Math.floor(s/nf)===site));
          const div=selected.length?1-Math.max(...selected.map(s=>Math.abs(C[j][s]))):1;
          if(method==="GREEDY")score=partial(selected,j,.04,"gain");
          else if(method==="SHRINK")score=partial(selected,j,.45,"gain");
          else if(method==="COSI_PROXY")score=.72*partial(selected,j,.45,"gain")+.13*roleNew+.15*div;
          else if(method==="TYPE")score=.74*partial(selected,j,.12,"gain")+.13*roleNew+.13*siteNew;
          else if(method==="MAXMIN")score=.45*Math.abs(cy[j])+.55*div;
          else if(method==="RANK")score=Math.abs(cy[j]);
          else if(method==="DOPT")score=partial(selected,j,.3,"div");
          else score=rand();
          score+=(D-j)*1e-12;
          if(score>best){best=score;bj=j;}
        }
        selected.push(bj);cand=cand.filter(j=>j!==bj);
      }
      return selected;
    }
    const rmse=(s)=> {
      let b=beta(s); let ee=0;
      for(let i=0;i<va.length;i++){let p=tr.ymu+tr.ysd*sum(s.map((j,k)=>b[k]*XE[i][j]));ee+=(p-yE[i])**2;}
      return Math.sqrt(ee/va.length);
    };
    const base=Math.sqrt(mean(yE.map(y=>(y-tr.ymu)**2)));
    const outs={};for(let m of methods){let ss=select(m);let val=rmse(ss);outs[m]={rmse:val,relative:val/base,selection:ss,types:ss.map(i=>data.fields[i%nf]),stations:ss.map(i=>data.station_names[Math.floor(i/nf)])};}
    return {cfg,samples:{train:tin.length,eval:va.length},mean_target:tr.ymu,naive_rmse:base,arms:outs};
  }
  const minKeys=new Set(),ledger=[],events=[];
  let cfg={target:"PM25_MEAN",nTrain:20,budget:6,alpha:.1,seed:5001,branch:"PILOT"};
  const altTargets=targets;
  const adapt=(r,cycle)=>{
    let a=Object.entries(r.arms).sort((x,y)=>x[1].rmse-y[1].rmse),winner=a[0][0],
        margin=(a[1][1].rmse-a[0][1].rmse)/a[1][1].rmse;
    let next={...r.cfg,seed:5001+cycle},why="";
    if(["COSI_PROXY","TYPE"].includes(winner)){
      if(margin>.04){next.branch="ROLE_FALSIFICATION";next.target=altTargets[(altTargets.indexOf(next.target)+3)%altTargets.length];why="Role-aware winner: test a different pollutant/target for mechanism transfer";}
      else {next.branch="DATA_SCARCITY";next.nTrain=Math.max(12,Math.round(next.nTrain*.65));why="Role-aware narrow win: reduce pilot size to challenge covariance regularizer";}
    } else if(["GREEDY","SHRINK"].includes(winner)){
      if(next.nTrain>=30 && margin>.04){next.branch="DATA_SCARCITY";next.nTrain=Math.max(12,Math.round(next.nTrain*.6));why="Supervised selector dominant: search low-data failure regime";}
      else {next.branch="TARGET_SHIFT";next.target=altTargets[(altTargets.indexOf(next.target)+1)%altTargets.length];why="Supervised selector wins: shift to nonlinear or different pollutant objective";}
    } else if(["MAXMIN","DOPT","RANDOM"].includes(winner)){
      next.branch="REGULARIZATION";next.alpha=next.alpha<.3?Math.round((next.alpha+.1)*100)/100:.03;next.budget=Math.max(3,next.budget-1);why="Task-agnostic method wins: stress model regularization with tighter budget";
    } else {
      next.branch="BUDGET_SHIFT";next.budget=next.budget>=10?3:next.budget+2;why="Marginal ranking wins: change reading budget to test diminishing returns";
    }
    if(cycle%6===0){next.target=altTargets[(altTargets.indexOf(next.target)+2)%altTargets.length];next.branch="DOMAIN_TRANSFER";why+="; periodic anti-stagnation changes target";}
    if(cycle%8===0){next.nTrain=[12,20,36,65,100,125][Math.floor(cycle/8)%6];next.branch="PILOT_COUNTEREXAMPLE";why+="; check independent pilot regime";}
    let key=z=>[z.target,z.nTrain,z.budget,z.alpha].join("|");
    for(let k=0;k<60&&minKeys.has(key(next));k++){
      if(k%3===0)next.target=altTargets[(altTargets.indexOf(next.target)+1)%altTargets.length];
      else if(k%3===1)next.budget=3+(next.budget+2)%10;
      else next.nTrain=[12,20,30,45,65,95,125][(k+cycle)%7];
    }
    return {next,why,winner,margin};
  };
  for(let c=1;c<=45;c++){
    const key=[cfg.target,cfg.nTrain,cfg.budget,cfg.alpha].join("|");
    if(minKeys.has(key))throw Error("Repeated condition: "+key);
    minKeys.add(key);
    const prospective={cycle:c,design_before_result:structuredClone(cfg),selection_justification:events.length?events[events.length-1].next_reason:"Initial diagnostic baseline",test_open:false};
    const res=trial(cfg);
    const chosen=Object.entries(res.arms).sort((a,b)=>a[1].rmse-b[1].rmse);
    const ad=adapt(res,c);
    prospective.result_winner=ad.winner;prospective.validation_rmse=chosen[0][1].rmse;prospective.second=chosen[1][0];prospective.margin=ad.margin;
    prospective.next_design=structuredClone(ad.next);prospective.next_reason=ad.why;
    events.push(prospective);ledger.push(res);cfg=ad.next;
  }
  // One-time final temporal evaluation; selection is fixed on validation for each target.
  let final=[];
  for(const target of ["PM25_MEAN","NO2_MEAN","O3_MEAN","PM25_TOP3","PM25_PM10_GAP"]){
    const cfg={target,nTrain:130,budget:6,alpha:.1,seed:777,branch:"FROZEN_FINAL"};
    const dev=trial(cfg,130,170), ranking=Object.entries(dev.arms).sort((a,b)=>a[1].rmse-b[1].rmse).map(([m])=>m);
    const test=trial(cfg,170,T,true);
    final.push({target,selected_method:ranking[0],val_rmse:dev.arms[ranking[0]].rmse,test_rmse:test.arms[ranking[0]].rmse,
      control_GREEDY:test.arms.GREEDY.rmse,control_SHRINK:test.arms.SHRINK.rmse,control_RANK:test.arms.RANK.rmse,
      control_COSI_PROXY:test.arms.COSI_PROXY.rmse,control_MAXMIN:test.arms.MAXMIN.rmse,
      baserate:test.naive_rmse,samples:test.samples,all_test:Object.fromEntries(methods.map(m=>[m,{rmse:test.arms[m].rmse,selection:test.arms[m].selection}]))});
  }
  const wins=Object.fromEntries(methods.map(m=>[m,0]));for(const e of events)wins[e.result_winner]++;
  return {meta:{dates:{train:"2013-03–2015-08 (weeks 0–129)",validation:"2015-08–2016-05 (130–169)",test:"2016-06–2017-02 (170–208)"},methods,source:data.source,notes:"45 adaptively chosen validation conditions; holdout test opened only once after cycle 45. COSI_PROXY not original Scale3D or published COSI; NO physical locations/communications simulated."},wins,events,ledger,final};
}
const results=runCampaign(data);
writeFileSync(new URL('./campaign_results.json',import.meta.url),JSON.stringify(results,null,2));
console.log(JSON.stringify({wins:results.wins,final:results.final.map(x=>({target:x.target,selected_method:x.selected_method,test_rmse:x.test_rmse,control_GREEDY:x.control_GREEDY}))},null,2));
