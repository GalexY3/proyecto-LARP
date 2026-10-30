/* IP01-IP15. Real AVIRIS Indian Pines 2D spatial 220-band data.
 Original native N400 six exported float64 hexadecimal geometry snapshots, 3 paired seeds.
 ONLY derived aggregate outputs. No raw spectra or coordinates in result.
 Native Wei original not run. CVT is a deterministic Lloyd proxy (not Wei).
*/
function analyzeIP15(csv, geometries) {
  "use strict";
  const W=145,N=21025,C=5,QUOTAS=[163,85,68,50,34],QUOTA200=[81,43,34,25,17],QUOTA100=[41,21,17,13,8],BANDS=[20,60,90,130,190],SEEDS=[1101,1102,1103];
  const sourceSHA="0ed4500533a7c27e479944ce01996e676cabff1d";
  const geometrySHA={
    MHU:["18f4567d4c72aa7bdd9e2de6cb4f7f5a007df8ad","5642a47b34d1ac3ae840c06a989855db2b5dc6d9","5e2d9ba161bba318ed219c5116e383d443656453"],
    LOCAL:["de57ad4d700303aabb495affa08ecd986371a5f1","05febd925bb0e61a94d4a5d9230d34e0dd3af24b","931c4f73495121fc7034ae6ebdf6b2218ecdcccc"]
  };
  function rng(seed){let a=seed>>>0;return ()=>{a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return ((t^(t>>>14))>>>0)/4294967296;};}
  function permuteInPlace(a,r){for(let i=a.length-1;i>0;i--){const j=Math.floor(r()*(i+1));const t=a[i];a[i]=a[j];a[j]=t;}return a;}
  function parseFloatHex(h){
    const m=/^([+-]?)0x([0-9a-f]+)(?:\.([0-9a-f]+))?p([+-]?\d+)$/i.exec(h);
    if(!m)throw Error("INVALID_HEXFLOAT");
    const fract=m[3]||"",mant=Number.parseInt(m[2],16)+(fract?Number.parseInt(fract,16)/Math.pow(16,fract.length):0);
    return (m[1]==="-"?-1:1)*mant*Math.pow(2,Number(m[4]));
  }
  function parseImage(text){
    const ls=text.trim().split(/\r?\n/);
    if(ls.length!==N+4)throw Error("PIXEL_ROW_COUNT_"+ls.length);
    if(ls[0].trim()!=="21025,222")throw Error("INDIAN_PINES_ORIGINAL_METADATA");
    const classes=ls[1].split(",");
    if(classes.length!==17)throw Error("LABEL_NAME_COUNT");
    const header=ls[3].split(",");
    if(header.length!==222||header[0]!=="column#"||header[1]!=="line#"||header.slice(2).some((x,i)=>x!=="#"+i))throw Error("BAND_HEADER");
    const field=new Float64Array(N*C),labels=new Uint8Array(N),labelCount=Array(17).fill(0);
    let allFinite=0,zeroCount=0,negativeCount=0,maxMagnitude=0,missing=0;
    for(let i=0;i<N;i++){
      const f=ls[i+4].split(",");
      if(f.length!==223)throw Error("BAD_DATA_FIELD_COUNT_IDX_"+i);
      const x=Number(f[0]),y=Number(f[1]),label=Number(f[222]);
      if(!Number.isInteger(x)||!Number.isInteger(y)||x!==Math.floor(i/W)||y!==i%W)throw Error("PIXEL_GRID_ORDER_IDX_"+i);
      if(!Number.isInteger(label)||label<0||label>16)throw Error("INVALID_LABEL");
      labels[i]=label;labelCount[label]++;
      for(let j=0;j<220;j++){
        const v=Number(f[2+j]);
        if(!Number.isFinite(v))throw Error("NONFINITE_AVIRIS_"+i+"_"+j);
        if(v===0)zeroCount++;
        if(v<0)negativeCount++;
        maxMagnitude=Math.max(maxMagnitude,Math.abs(v));allFinite++;
        for(let c=0;c<C;c++)if(j===BANDS[c])field[i*C+c]=v;
      }
    }
    return {field,labels,integrity:{rows:N,columns:223,spectral_bands:220,finite_band_cells:allFinite,zero_band_cells:zeroCount,negative_band_cells:negativeCount,max_abs_band_value:maxMagnitude,label_counts:labelCount,physical_scene:"INDIAN_PINES_AVIRIS_1992_145X145",row_major:"X_OUTER_Y_INNER",raw_source_git_blob:sourceSHA}};
  }
  function snap(raw,alreadyUnit145){
    const occupied=new Set(),nodes=[],meta={initial_collisions:0,total_shift_pixels:0,max_shift_pixels:0,moved_points:0,quota_actual:Array(C).fill(0)};
    for(let i=0;i<raw.length;i++){
      const p=raw[i],tx=alreadyUnit145?p.x:p.x*W/20,ty=alreadyUnit145?p.y:p.y*W/20,label=p.c;
      if(!Number.isFinite(tx)||!Number.isFinite(ty)||tx<0||ty<0||tx>=W||ty>=W||!Number.isInteger(label)||label<0||label>=C)throw Error("INVALID_SAMPLE_COORDINATE");
      const bx=Math.floor(tx),by=Math.floor(ty);if(occupied.has(bx*W+by))meta.initial_collisions++;
      let found=null;
      for(let rad=0;rad<=6&&!found;rad++){
        let bestScore=Infinity;
        for(let dx=-rad;dx<=rad;dx++)for(let dy=-rad;dy<=rad;dy++){
          if(rad>0&&Math.abs(dx)!==rad&&Math.abs(dy)!==rad)continue;
          const x=bx+dx,y=by+dy;
          if(x<0||y<0||x>=W||y>=W||occupied.has(x*W+y))continue;
          const cost=(x+0.5-tx)**2+(y+0.5-ty)**2;
          if(cost<bestScore-1e-10||(Math.abs(cost-bestScore)<=1e-10&&found&&(x<found.x||(x===found.x&&y<found.y)))){
            bestScore=cost;found={x,y};
          }
        }
      }
      if(!found)throw Error("SNAPPING_RADIUS_OVER_6");
      occupied.add(found.x*W+found.y);
      const shift=Math.hypot(found.x-bx,found.y-by);
      meta.total_shift_pixels+=shift;meta.max_shift_pixels=Math.max(meta.max_shift_pixels,shift);if(shift>0)meta.moved_points++;
      nodes.push({x:found.x,y:found.y,idx:found.x*W+found.y,c:label});
      meta.quota_actual[label]++;
    }
    if(nodes.length!==400||QUOTAS.some((v,i)=>meta.quota_actual[i]!==v)||occupied.size!==400)throw Error("SAMPLE_BUDGET_OR_QUOTA");
    meta.average_shift_pixels=meta.total_shift_pixels/nodes.length;
    return {nodes,meta};
  }
  function cvt(seed,shuffleLabels){
    const rand=rng(seed^0xC037),sites=[];
    for(let ix=0;ix<20;ix++)for(let iy=0;iy<20;iy++){
      sites.push({x:Math.min(W-0.01,Math.max(0.01,(ix+0.5)*W/20+(rand()-.5)*3)),
                  y:Math.min(W-0.01,Math.max(0.01,(iy+0.5)*W/20+(rand()-.5)*3))});
    }
    const iters=8;
    for(let iter=0;iter<iters;iter++){
      const accum=Array.from({length:400},()=>[0,0,0]);
      for(let x=0;x<W;x++)for(let y=0;y<W;y++){
        let best=0,d=Infinity;for(let p=0;p<400;p++){
          const dx=x+0.5-sites[p].x,dy=y+0.5-sites[p].y,t=dx*dx+dy*dy;
          if(t<d){d=t;best=p;}
        }
        accum[best][0]+=x+0.5;accum[best][1]+=y+0.5;accum[best][2]++;
      }
      for(let p=0;p<400;p++)if(accum[p][2]){sites[p].x=accum[p][0]/accum[p][2];sites[p].y=accum[p][1]/accum[p][2];}
    }
    return snap(sites.map((p,i)=>({x:p.x,y:p.y,c:shuffleLabels[i]})),true);
  }
  function getNodes(G,seed,method,sharedBaselineLabels){
    if(method==="RANDOM"){
      const r=rng(seed^0xBADC0DE),order=Array.from({length:N},(_,i)=>i);
      // Partial Fisher-Yates without replacement.
      const raw=[];for(let i=0;i<400;i++){
        const j=i+Math.floor(r()*(N-i));[order[i],order[j]]=[order[j],order[i]];
        const idx=order[i];raw.push({x:Math.floor(idx/W)+0.5,y:idx%W+0.5,c:sharedBaselineLabels[i]});
      }
      return snap(raw,true);
    }
    if(method==="CVT")return cvt(seed,sharedBaselineLabels);
    const k=method+seed;const item=G[k];
    if(!item||!item.obj||item.sha!==geometrySHA[method][SEEDS.indexOf(seed)])throw Error("NATIVE_GIT_BLOB_MISMATCH_"+k);
    const j=item.obj;
    if(j.points_float64_hex.length!==400||j.labels_int64.length!==400||j.L_hex!=="0x1.4000000000000p+4")throw Error("NATIVE_N400_METADATA");
    const raw=j.points_float64_hex.map((xy,i)=>({x:parseFloatHex(xy[0]),y:parseFloatHex(xy[1]),c:j.labels_int64[i]}));
    return snap(raw,false);
  }
  function selectBudgets(nodes,seed,m){
    const lists=Array.from({length:C},()=>[]);
    for(const node of nodes)lists[node.c].push({...node,active200:false,active100:false});
    const salt={MHU:101,LOCAL:202,RANDOM:303,CVT:404}[m];
    for(let c=0;c<C;c++){
      if(lists[c].length!==QUOTAS[c])throw Error("INPUT_LABEL_COUNT");
      const shuffled=Array.from({length:lists[c].length},(_,i)=>i),r=rng((seed*1439+salt*83+c*499)>>>0);
      permuteInPlace(shuffled,r);
      for(let i=0;i<QUOTA200[c];i++)lists[c][shuffled[i]].active200=true;
      for(let i=0;i<QUOTA100[c];i++)lists[c][shuffled[i]].active100=true;
    }
    return lists;
  }
  const image=parseImage(csv),field=image.field,GT=image.labels;
  const commonLabels=[];for(let c=0;c<C;c++)for(let i=0;i<QUOTAS[c];i++)commonLabels.push(c);
  const layouts=[],geometric=[];
  const methods=["MHU","LOCAL","RANDOM","CVT"];
  for(const seed of SEEDS){
    const shuf=permuteInPlace(commonLabels.slice(),rng(seed^0xA558));
    for(const m of methods){
      const g=getNodes(geometries,seed,m,shuf);
      layouts.push({seed,method:m,nodes:g.nodes,byClass:selectBudgets(g.nodes,seed,m)});
      geometric.push({seed,method:m,...g.meta});
    }
  }
  // Fair, common, source-independent checkerboard test positions, without any sampled pixels.
  const excluded=new Set(layouts.flatMap(g=>g.nodes.map(p=>p.idx))),test=[];
  for(let x=0;x<W;x+=2)for(let y=0;y<W;y+=2){const idx=x*W+y;if(!excluded.has(idx))test.push({x,y,idx,label:GT[idx]});}
  if(test.length<2500)throw Error("COMMON_TEST_TOO_SMALL_"+test.length);
  const norm=Array(C).fill(0),pNorm=Array(C).fill(0);
  const placeboIndex=i=>(97*i+1337)%N;
  for(const p of test)for(let c=0;c<C;c++){
    const v=field[p.idx*C+c],q=field[placeboIndex(p.idx)*C+c];
    norm[c]+=v*v/test.length;pNorm[c]+=q*q/test.length;
  }
  if(norm.some(x=>x<=0)||pNorm.some(x=>x<=0))throw Error("ZERO_CHANNEL_REFERENCE");
  const grad=test.map(p=>{
    let total=0;
    for(let c=0;c<C;c++){
      const x1=Math.max(0,p.x-1),x2=Math.min(W-1,p.x+1),y1=Math.max(0,p.y-1),y2=Math.min(W-1,p.y+1);
      const dx=(field[(x2*W+p.y)*C+c]-field[(x1*W+p.y)*C+c])/(x2-x1||1);
      const dy=(field[(p.x*W+y2)*C+c]-field[(p.x*W+y1)*C+c])/(y2-y1||1);
      total+=(dx*dx+dy*dy)/norm[c];
    }return total/C;
  }),gs=grad.slice().sort((a,b)=>a-b),threshold=gs[Math.floor(gs.length/2)];
  for(let i=0;i<test.length;i++)test[i].highGradient=grad[i]>threshold;
  const run=[];
  function estimate(near,k,valueOf){let sw=0,s=0;for(let i=0;i<Math.min(k,near.length);i++){const a=near[i],w=1/(a.d2+1e-9);sw+=w;s+=w*valueOf(a.node);}return s/sw;}
  function nearestInsert(list,node,d2){let j=list.length;while(j>0&&list[j-1].d2>d2)j--;if(j>=8)return;list.splice(j,0,{node,d2});if(list.length>8)list.pop();}
  for(const g of layouts){
    const sums={},metricNames=["NN1","IDW4","IDW8","GAUSS","BUDGET200","BUDGET100","PLACEBO"];
    for(const name of metricNames)sums[name]={normalized:0,raw:0,n:0,perType:Array(C).fill(0)};
    const mask={high:{e:0,n:0},low:{e:0,n:0},background:{e:0,n:0},labeled:{e:0,n:0}};
    const cover=Array.from({length:17},()=>({e:0,n:0}));
    for(const p of test){
      for(let c=0;c<C;c++){
        const selected=g.byClass[c],near=[],near200=[],near100=[];
        let gaussianSW=0,gaussianSV=0;
        for(const node of selected){
          const dx=node.x-p.x,dy=node.y-p.y,d2=dx*dx+dy*dy;
          nearestInsert(near,node,d2);
          if(node.active200)nearestInsert(near200,node,d2);
          if(node.active100)nearestInsert(near100,node,d2);
          const w=Math.exp(-d2/(2*18*18));
          gaussianSW+=w;gaussianSV+=w*field[node.idx*C+c];
        }
        if(!near.length||!near200.length||!near100.length||!(gaussianSW>0))throw Error("INVALID_NEIGHBOR_SET");
        const val=node=>field[node.idx*C+c],pval=node=>field[placeboIndex(node.idx)*C+c];
        const preds={
          NN1:val(near[0].node),
          IDW4:estimate(near,4,val),
          IDW8:estimate(near,8,val),
          GAUSS:gaussianSV/gaussianSW,
          BUDGET200:estimate(near200,4,val),
          BUDGET100:estimate(near100,4,val),
          PLACEBO:estimate(near,4,pval)
        };
        const truth=field[p.idx*C+c],placeboTruth=field[placeboIndex(p.idx)*C+c];
        for(const name of metricNames){
          const e=(preds[name]-(name==="PLACEBO"?placeboTruth:truth))**2;
          if(!Number.isFinite(e))throw Error("NONFINITE_PREDICTION");
          const en=e/(name==="PLACEBO"?pNorm[c]:norm[c]);
          const r=sums[name];r.normalized+=en;r.raw+=e;r.n++;r.perType[c]+=en;
          if(name==="IDW4"){
            const a=p.highGradient?mask.high:mask.low;a.e+=en;a.n++;
            const b=p.label===0?mask.background:mask.labeled;b.e+=en;b.n++;
            cover[p.label].e+=en;cover[p.label].n++;
          }
        }
      }
    }
    for(const name of metricNames){const m=sums[name];m.normalized/=m.n;m.raw/=m.n;m.perType=m.perType.map(v=>v/test.length);}
    for(const v of Object.values(mask))v.mse=v.e/v.n;
    const perCover=cover.map((r,label)=>({label,test_pixel_count:r.n/C,normalized_mse:r.n?r.e/r.n:null}));
    run.push({seed:g.seed,method:g.method,metric:sums,segments:{
      highGradient:{mse:mask.high.mse,test_pixels:mask.high.n/C},
      lowGradient:{mse:mask.low.mse,test_pixels:mask.low.n/C},
      background:{mse:mask.background.mse,test_pixels:mask.background.n/C},
      labeled:{mse:mask.labeled.mse,test_pixels:mask.labeled.n/C},
      perCover},sampling_count:400});
  }
  const avg=(arr)=>arr.reduce((s,x)=>s+x,0)/arr.length;
  const rankings={};for(const name of ["NN1","IDW4","IDW8","GAUSS","BUDGET200","BUDGET100","PLACEBO"]){
    rankings[name]=Object.fromEntries(methods.map(m=>[m,avg(run.filter(z=>z.method===m).map(z=>z.metric[name].normalized))]));
  }
  const paired={};for(const name of Object.keys(rankings))paired[name]=SEEDS.map(seed=>{
    const m=run.find(x=>x.method==="MHU"&&x.seed===seed),l=run.find(x=>x.method==="LOCAL"&&x.seed===seed);
    return {seed,ratio_MHU_to_LOCAL:m.metric[name].normalized/l.metric[name].normalized,
      difference_MHU_minus_LOCAL:m.metric[name].normalized-l.metric[name].normalized};
  });
  const summarizeSegment=seg=>Object.fromEntries(methods.map(m=>[m,avg(run.filter(x=>x.method===m).map(x=>x.segments[seg].mse))]));
  const perType=Object.fromEntries(methods.map(m=>[m,Array.from({length:C},(_,c)=>avg(run.filter(x=>x.method===m).map(x=>x.metric.IDW4.perType[c])))]));
  const qualifyCover=[];
  for(let cls=0;cls<17;cls++){
    const n=run[0].segments.perCover[cls].test_pixel_count;
    if(n>=100)qualifyCover.push({class_id:cls,heldout_pixels:n,by_method:Object.fromEntries(methods.map(m=>[m,avg(run.filter(x=>x.method===m).map(x=>x.segments.perCover[cls].normalized_mse))]))});
  }
  const mhuVsLocal=(k)=>({mh:u=>rankings[k].MHU,local:rankings[k].LOCAL,ratio:rankings[k].MHU/rankings[k].LOCAL});
  const placeboLoss=rankings.PLACEBO;
  const tasks={
    IP01:{endpoint:"source_integrity",outcome:image.integrity,status:"DONE"},
    IP02:{endpoint:"pixel_mapping_400_quota",outcome:geometric,status:"DONE"},
    IP03:{endpoint:"Cvt_vs_random_discrete_density",outcome:{
      mean_snap_shift_CVT:avg(geometric.filter(x=>x.method==="CVT").map(x=>x.average_shift_pixels)),
      mean_snap_shift_RANDOM:avg(geometric.filter(x=>x.method==="RANDOM").map(x=>x.average_shift_pixels)),
      common_test_pixels:test.length,selected_band_ids:BANDS},status:"DONE"},
    IP04:{endpoint:"real_2D_IDW_k4",outcome:{method_mean_normalized_mse:rankings.IDW4,paired:paired.IDW4},status:"DONE"},
    IP05:{endpoint:"real_2D_nearest1",outcome:{method_mean_normalized_mse:rankings.NN1,paired:paired.NN1},status:"DONE"},
    IP06:{endpoint:"real_2D_IDW_k8",outcome:{method_mean_normalized_mse:rankings.IDW8,paired:paired.IDW8},status:"DONE"},
    IP07:{endpoint:"real_2D_gaussian_h18",outcome:{method_mean_normalized_mse:rankings.GAUSS,paired:paired.GAUSS},status:"DONE"},
    IP08:{endpoint:"high_gradient_IDW4",outcome:{source_gradient_median:threshold,mean_mse_by_method:summarizeSegment("highGradient"),n:test.filter(x=>x.highGradient).length},status:"DONE"},
    IP09:{endpoint:"low_gradient_IDW4",outcome:{source_gradient_median:threshold,mean_mse_by_method:summarizeSegment("lowGradient"),n:test.filter(x=>!x.highGradient).length},status:"DONE"},
    IP10:{endpoint:"GT_coverage_macro_class_IDW4",outcome:{per_cover_eligible:qualifyCover,eligible_class_count:qualifyCover.length},status:"DONE"},
    IP11:{endpoint:"GT_unlabeled_background_vs_labeled_IDW4",outcome:{background:summarizeSegment("background"),labeled:summarizeSegment("labeled")},status:"DONE"},
    IP12:{endpoint:"5_channel_type_loss_IDW4",outcome:{per_type_normalized_mse:perType,bands:BANDS,quotas:QUOTAS},status:"DONE"},
    IP13:{endpoint:"200_budget_IDW4",outcome:{method_mean_normalized_mse:rankings.BUDGET200,paired:paired.BUDGET200,quotas:QUOTA200},status:"DONE"},
    IP14:{endpoint:"100_budget_IDW4",outcome:{method_mean_normalized_mse:rankings.BUDGET100,paired:paired.BUDGET100,quotas:QUOTA100},status:"DONE"},
    IP15:{endpoint:"placebo_spatial_permutation",outcome:{method_mean_normalized_mse:placeboLoss,paired:paired.PLACEBO,field_permutation:"(97*idx+1337)%21025",rankings_on_real:rankings.IDW4},status:"DONE"}
  };
  if(Object.keys(tasks).length!==15||Object.values(tasks).some(x=>x.status!=="DONE"))throw Error("BAD_CYCLE_COUNT");
  const judge={};
  for(const name of Object.keys(rankings)){
    const v=rankings[name];judge[name]={ranked_methods:methods.slice().sort((a,b)=>v[a]-v[b]),MHU_vs_LOCAL_mean:v.MHU/v.LOCAL,paired_MHU_win_count:paired[name].filter(x=>x.difference_MHU_minus_LOCAL<0).length};
  }
  return {schema:"AB_IP15_REAL_2D_HSI_V1",source_manifest:"SOURCE_MANIFEST_PRE_OUTCOME.json",scene:"AVIRIS_IndianPines_145x145x220",
    prior_claims:"ONE_REAL_SCENE_15_DEPENDENT_ESTIMANDS_NOT_15_INDEPENDENT_REPLICATIONS",
    source_metadata:{pixels:N,spectral_bands:220,channels_tested:BANDS,sample_quota:QUOTAS,test_pixels_common:test.length,gt_test_categories:qualifyCover.length,grid_map:"X_OUTER_Y_INNER",source_git_blob:sourceSHA},
    input_integrity:image.integrity,geometric_mapping:geometric,judge,run,
    tasks,
    critical_limitations:["SOURCE_1992_AVIRIS_2D_NOT_RETINAL_5_PHOTORECEPTOR_EXPERIMENT","SOURCE_SAME_IMAGE_FOR_ALL_15_TASKS","SOURCE_LICENSE_NOT_VERIFIED_NO_REDISTRIBUTION","NO_WEI_ORIGINAL_COMPILED_OR_RUN","CVT_DETERMINISTIC_LLOYD_PROXY_NOT_AUTHENTIC_AUTHOR_SOLVER","NATIVE_GEOMETRY_FROM_VERIFIED_EXPORT_JSON_NOT_INDEPENDENT_NPZ_REOPEN","PIXEL_SNAP_NEAREST_FREE_MODIFIES_ORIGINAL_CONTINUOUS_PATTERN","TEST_PIXELS_CHECKERBOARD_COMMON_EXCLUDED_ALL_SAMPLERS","ORIGINAL_N400_NEURAL_BENCHMARK_NOT_EXECUTED","NO_CAUSAL_OR_BIOLOGICAL_EFFICACY_CLAIM"],
    grade:"0/3",new_N1:0,new_N2:0,new_N3:0,CT2_math_before_after:[24,24],CT2_functional_before_after:[18,18]};
}
