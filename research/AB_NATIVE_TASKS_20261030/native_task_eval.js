/* LARP AB-R T01–T10 source, frozen before outcomes.
Analytic, task-conditioned comparisons on original 400-node coordinates from six private verified exact IEEE-754 exports.
No stochastic outcomes or GNN training. Not a validation of empirical biology or neural performance. */
function evaluateNativeTask(inputs) {
  'use strict';
  const L=20, N=400, counts=[163,85,68,50,34], seeds=[1101,1102,1103];
  const kinds=['full_spectral','local_only','cvt_proxy','halton'];
  const expected={
    avian_full_spectral_N400_g1101:'71cbbb405105e03663fbdc40cdfbe471bce29675',
    avian_full_spectral_N400_g1102:'60d849256e624efbad46dd2127c4c1bcce8d6d55',
    avian_full_spectral_N400_g1103:'8bad8683ef9cfa3489c6d8792f8e1c387783b9bf',
    avian_local_only_N400_g1101:'4a77364209bb3c1cbcf1ee0f2c746490389825ea',
    avian_local_only_N400_g1102:'0938f6eadfc95fb7d60fa3b5f5331c9bf70dc27a',
    avian_local_only_N400_g1103:'595024b0fb801e586d264d81cf95b789aa91a29b'
  };
  function hx(s){
    const m=/^(-?)0x([0-9a-f]+)\.([0-9a-f]+)p([+-]?\d+)$/i.exec(s);
    if(!m)throw Error('Invalid exact float hex: '+s);
    const frac=m[3].length, mantissa=parseInt(m[2]+m[3],16);
    return (m[1]?-1:1)*mantissa*Math.pow(2,+m[4]-4*frac);
  }
  function mod(x){return (x%L+L)%L}
  function delta(x,y){let d=Math.abs(x-y);return Math.min(d,L-d)}
  function d2(a,b){let dx=delta(a[0],b[0]),dy=delta(a[1],b[1]);return dx*dx+dy*dy}
  function half(a,b){let d=a-b;return d-L*Math.round(d/L)}
  function avg(a){return a.reduce((s,x)=>s+x,0)/a.length}
  function halton(k,b){let a=0,f=1;for(let i=k;i>0;i=Math.floor(i/b)){f/=b;a+=f*(i%b)}return a}
  function checkNative(obj,stem){
    if(obj.stem!==stem||obj.npz_git_blob!==expected[stem])throw Error('Pinned source mismatch '+stem);
    const p=obj.points_float64_hex,labels=obj.labels_int64;
    if(!Array.isArray(p)||p.length!==400||!Array.isArray(labels)||labels.length!==400)throw Error('Bad native shapes '+stem);
    if(hx(obj.L_hex)!==L)throw Error('Wrong domain '+stem);
    const bins=[0,0,0,0,0],coords=p.map((row,i)=>{
      const z=row.map(hx);if(row.length!==2||z.some(x=>!Number.isFinite(x)||x<0||x>=L))throw Error('Invalid coordinates '+stem);
      const k=labels[i];if(!Number.isInteger(k)||k<0||k>4)throw Error('Bad labels '+stem);bins[k]++;return z;
    });
    if(bins.some((x,i)=>x!==counts[i]))throw Error('Wrong original quotas '+stem);
    if(!obj.geometry_hashes?.points||!obj.geometry_hashes?.labels||!obj.geometry_hashes?.geometry)throw Error('Missing hashes '+stem);
    return{p:coords,labels:[...labels],kind:stem.includes('full_spectral')?'full_spectral':'local_only'};
  }
  function makeHalton(labels,seed){
    const pos=new Array(N);const counter=[0,0,0,0,0];
    for(let i=0;i<N;i++){let c=labels[i],j=counter[c]++,k=1+(seed-1100)*37+c*59+j;
      pos[i]=[halton(k,2)*L,halton(k,3)*L];
    }
    return pos;
  }
  function makeCVT(source,labels){
    const p=source.map(a=>a.slice()), grid=[];
    for(let x=0;x<24;x++)for(let y=0;y<24;y++)grid.push([(x+.5)*L/24,(y+.5)*L/24]);
    for(let it=0;it<25;it++){
      const sumX=new Float64Array(N),sumY=new Float64Array(N),num=new Uint32Array(N);
      for(let c=0;c<5;c++){
        const ids=[];for(let i=0;i<N;i++)if(labels[i]===c)ids.push(i);
        for(const z of grid){
          let best=-1,bd=Infinity;
          for(const i of ids){const d=d2(z,p[i]);if(d<bd){bd=d;best=i}}
          sumX[best]+=half(z[0],p[best][0]);sumY[best]+=half(z[1],p[best][1]);num[best]++;
        }
      }
      for(let i=0;i<N;i++)if(num[i]){p[i][0]=mod(p[i][0]+0.8*sumX[i]/num[i]);p[i][1]=mod(p[i][1]+0.8*sumY[i]/num[i])}
    }
    return p;
  }
  function kfun(a,b,ell){
    const x=Math.sin(Math.PI*(a[0]-b[0])/L),y=Math.sin(Math.PI*(a[1]-b[1])/L);
    return Math.exp((-2*L*L/(ell*ell))*(x*x+y*y));
  }
  function chol(K,n){
    const lower=new Float64Array(n*n);
    for(let i=0;i<n;i++)for(let j=0;j<=i;j++){
      let s=K[i*n+j];
      for(let k=0;k<j;k++)s-=lower[i*n+k]*lower[j*n+k];
      if(i===j){if(s<=1e-12)throw Error('Kernel not positive definite '+i+' '+s);lower[i*n+j]=Math.sqrt(s)}
      else lower[i*n+j]=s/lower[j*n+j];
    }
    return lower;
  }
  const query=[];for(let x=0;x<8;x++)for(let y=0;y<8;y++)query.push([(x+.5)*L/8,(y+.5)*L/8]);
  function gpRisk(p,labels,ell){
    let byType=[];
    for(let c=0;c<5;c++){
      const sites=[];for(let i=0;i<N;i++)if(labels[i]===c)sites.push(p[i]);
      let n=sites.length, K=new Float64Array(n*n);
      for(let i=0;i<n;i++)for(let j=0;j<=i;j++){const x=kfun(sites[i],sites[j],ell)+(i===j?.01:0);K[i*n+j]=x;K[j*n+i]=x}
      const A=chol(K,n);let risk=0,z=new Float64Array(n);
      for(const q of query){
        for(let i=0;i<n;i++){let v=kfun(q,sites[i],ell);for(let j=0;j<i;j++)v-=A[i*n+j]*z[j];z[i]=v/A[i*n+i]}
        let v=1;for(let i=0;i<n;i++)v-=z[i]*z[i];risk+=Math.max(0,v);
      }
      byType.push(risk/query.length);
    }
    return{equal_type:avg(byType),population_weighted:byType.reduce((s,v,i)=>s+v*counts[i],0)/N,by_type:byType};
  }
  function chooseNeighbors(p,labels,rule){
    const adj=new Array(N),edgeD=[];
    for(let i=0;i<N;i++){
      const sort=[];for(let j=0;j<N;j++)if(j!==i)sort.push([d2(p[i],p[j]),j]);
      sort.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
      let chosen;
      if(rule==='knn') chosen=sort.slice(0,6).map(t=>t[1]);
      else{
        chosen=[];for(let c=0;c<5;c++){
          const first=sort.find(t=>labels[t[1]]===c&&!chosen.includes(t[1]));
          if(!first)throw Error('Missing modal donor '+c);
          chosen.push(first[1]);
        }
        for(const t of sort)if(chosen.length<6&&!chosen.includes(t[1]))chosen.push(t[1]);
      }
      if(chosen.length!==6||new Set(chosen).size!==6)throw Error('Degree !=6');
      adj[i]=chosen;for(const j of chosen)edgeD.push(Math.sqrt(d2(p[i],p[j])));
    }
    return{adj,edge_mean:avg(edgeD)};
  }
  function hopRisk(p,labels,graph,hops){
    const {adj,edge_mean}=graph;let total=0,covered=0,typesTotal=0,byType=Array(5).fill(0);
    for(let i=0;i<N;i++){
      const seen=new Uint8Array(N);seen[i]=1;let frontier=[i];
      for(let h=0;h<hops;h++){
        const next=[];
        for(const u of frontier)for(const v of adj[u])if(!seen[v]){seen[v]=1;next.push(v)}
        frontier=next;
      }
      const best=[200,200,200,200,200], found=[false,false,false,false,false];
      for(let j=0;j<N;j++)if(seen[j]){const c=labels[j],v=d2(p[i],p[j]);if(v<best[c])best[c]=v;found[c]=true}
      for(let c=0;c<5;c++){const loss=best[c]/200;total+=loss;byType[c]+=loss;if(found[c])covered++;typesTotal++}
    }
    return{mean_normalized_square:total/typesTotal,available_type_fraction:covered/typesTotal,mean_edge_length:edge_mean,by_type:byType.map(x=>x/N)};
  }
  const originals=new Map(),all=[];
  for(const seed of seeds){
    const source={};for(const t of ['full_spectral','local_only']){
      const stem='avian_'+t+'_N400_g'+seed, obj=inputs[stem];
      if(!obj)throw Error('Missing private original '+stem);
      source[t]=checkNative(obj,stem);
    }
    if(source.full_spectral.labels.some((c,i)=>c!==source.local_only.labels[i]))throw Error('Original labels mismatch seed '+seed);
    const labels=source.full_spectral.labels;
    const hal=makeHalton(labels,seed),cvt=makeCVT(hal,labels);
    for(const [kind,p] of [['full_spectral',source.full_spectral.p],['local_only',source.local_only.p],['cvt_proxy',cvt],['halton',hal]])all.push({seed,kind,p,labels});
  }
  const rows=[],ells=[.5,.8,1.25,2,3.5];
  for(const original of all){
    for(let i=0;i<ells.length;i++){
      const risk=gpRisk(original.p,original.labels,ells[i]);
      rows.push({task:'T'+String(i+1).padStart(2,'0'),seed:original.seed,model:original.kind,metric:'GP_analytic_risk',parameter:ells[i],...risk});
    }
    const knn=chooseNeighbors(original.p,original.labels,'knn');
    const typed=chooseNeighbors(original.p,original.labels,'type');
    for(let hops=1;hops<=3;hops++){
      for(const [name,graph] of [['knn',knn],['typed',typed]]){
        const risk=hopRisk(original.p,original.labels,graph,hops);
        rows.push({task:'T'+String(hops+5).padStart(2,'0'),seed:original.seed,model:original.kind+'_'+name,metric:'graph_reachable_modality_error',parameter:hops,...risk});
      }
    }
    const optimized=[[1,0],[0,1],[1,1],[1,-1],[2,0],[0,2]];
    const blocked=new Set(optimized.flatMap(([x,y])=>[x+','+y,(-x)+','+(-y)]));
    for(const task of ['T09','T10']){
      const ks=[];for(let kx=0;kx<=9;kx++)for(let ky=-9;ky<=9;ky++){
        const norm=kx*kx+ky*ky;
        if(kx===0&&ky<=0)continue;
        if(task==='T09'&&norm>0&&norm<=16&&!blocked.has(kx+','+ky))ks.push([kx,ky]);
        if(task==='T10'&&norm>16&&norm<=81)ks.push([kx,ky]);
      }
      const means=[],groups=[0,1,2,3,4,-1];
      for(const c of groups){
        let ids=[];for(let i=0;i<N;i++)if(c<0||original.labels[i]===c)ids.push(i);
        let risk=0;
        for(const [kx,ky] of ks){let re=0,im=0;for(const i of ids){const a=2*Math.PI*(kx*original.p[i][0]+ky*original.p[i][1])/L;re+=Math.cos(a);im+=Math.sin(a)}risk+=(re*re+im*im)/ids.length}
        means.push(risk/ks.length);
      }
      rows.push({task,seed:original.seed,model:original.kind,metric:'Fourier_S_k_mean',modes:ks.length,by_type:means.slice(0,5),union:means[5],equal_type:avg(means.slice(0,5)),population_weighted:means.slice(0,5).reduce((s,v,i)=>s+v*counts[i],0)/N});
    }
  }
  if(rows.length!==3*4*(5+6+2))throw Error('Unexpected factorial row count: '+rows.length);
  // Averages per unique task and method, preserving all paired original seed records.
  const summary=[];
  for(let t=1;t<=10;t++){
    const task='T'+String(t).padStart(2,'0');
    for(const model of [...kinds,...kinds.flatMap(k=>[k+'_knn',k+'_typed'])]){
      const rr=rows.filter(r=>r.task===task&&r.model===model);
      if(rr.length===0)continue;if(rr.length!==3)throw Error('Not 3 paired models '+task+'/'+model);
      let key=t<=5?'equal_type':t<=8?'mean_normalized_square':'equal_type';
      summary.push({task,model,metric:key,mean:avg(rr.map(r=>r[key])),individual_seeds:rr.map(r=>({seed:r.seed,value:r[key]}))});
    }
  }
  return {schema:'AB_NATIVE_TASKS_T01_T10',date:'2026-10-30',source_kind:'Genuine original N400 IEEE754 exact coordinate exports',source_ref:'research/ab-r-native-export-20261030-053103',units:'3 paired native seeds only; 8x8 integration grid and 400 nodes are NOT independent replicas',parameters:{box:L,nodes:N,type_counts:counts,GP_ell:ells,GP_sensor_noise_variance:.01,GP_queries:64,graph_outdegree:6,graph_hops:[1,2,3],CVT_grid:'24x24',CVT_steps:25,CVT_relaxation:.8},rows,summary,claims:'Mathematical task-conditioned analytic posterior and reachability risks, not empirical or neural results'};
}
