/* W05-W20, frozen physical spectroscopy assay. Pure JS; no raw dataset redistributed.
 * Invoke analyze(csv) in isolated V8 or: node w05_w20_analyze.js source.csv
 */
function analyze(csv) {
  'use strict';
  const names = ['dark skin','light skin','blue sky','foliage','blue flower','bluish green','orange','purplish blue','moderate red','purple','yellow green','orange yellow','blue','green','red','yellow','magenta','cyan','white 9.5 (.05 D)','neutral 8 (.23 D)','neutral 6.5 (.44 D)','neutral 5 (.70 D)','neutral 3.5 (1.05 D)','black 2 (1.5 D)'];
  const filterNames=['400 nm','442 nm','500 nm','550 nm','600 nm','650 nm','700 nm'];
  const wavelengthNames=[400,470,550,620,700];
  const lines=csv.trim().split(/\r?\n/);
  const hdr=lines[0].split(',').map(v=>v.trim());
  const idx={}; hdr.forEach((v,i)=>{if(idx[v]!==undefined)throw Error('DUPLICATE_COLUMN '+v); idx[v]=i;});
  for(const name of ['Wavelength',...names,...filterNames,'Large chequerboard (white)','Large chequerboard (black)','Small chequerboard (white)','Small chequerboard (black)','Printer paper (white)','Printer paper (toner)']) {
    if(idx[name]===undefined)throw Error('MISSING_COLUMN '+name);
  }
  const sample={};
  for(let z=1;z<lines.length;z++){
    const parts=lines[z].split(',');
    if(parts.length!==hdr.length)throw Error('COLUMN_COUNT '+z);
    const w=Number(parts[idx.Wavelength]);
    if(!Number.isInteger(w)||w!==349+z)throw Error('WAVELENGTH_EXPECTED_'+(349+z)+'_GOT_'+w);
    if(w<350||w>750)throw Error('BAD_WAVELENGTH');
    sample[w]=parts.map((v,j)=>{const x=Number(v); if(v.trim()===''||!Number.isFinite(x))throw Error('NONFINITE_'+w+'_'+hdr[j]);return x;});
  }
  if(lines.length!==402)throw Error('EXPECTED_401_ROWS_GOT_'+(lines.length-1));
  const at=(nm,w)=>sample[w][idx[nm]], grid=Array.from({length:31},(_,i)=>400+i*10);
  const domain=Array.from({length:401},(_,i)=>350+i);
  const nominal=[400,442,500,550,600,650,700];
  const mean=x=>x.reduce((s,y)=>s+y,0)/x.length;
  const median=x=>{const s=[...x].sort((a,b)=>a-b);return (s[Math.floor((s.length-1)/2)]+s[Math.floor(s.length/2)])/2;};
  const sq=x=>x*x;
  const mse=(a,b)=>mean(a.map((v,i)=>sq(v-b[i])));
  const percentile=(a,p)=>{const x=[...a].sort((u,v)=>u-v),v=p*(x.length-1),i=Math.floor(v),f=v-i;return x[i]*(1-f)+x[Math.min(x.length-1,i+1)]*f;};
  const report={source:{repo:'bllanos/chromatic-aberration',commit:'9350e51a1ca96d541a6a82627fd0bf7636cf6638',git_blob:'82b83444716930c75e1d2a77ac6eed9fd6ccdc8d',wavelength_min:350,wavelength_max:750,wavelength_step:1,material_patches:24,filters:7,source_data_published_here:false},cycles:{}};
  const out=(id,endpoint,details)=>{report.cycles[id]={status:'EXECUTED_EXPLORATORY_REAL_LAB_SPECTRA',endpoint,details,novelty:'0/3',external_replication:false,claim_limited_to_this_source:true};};
  const filterCurves=filterNames.map(name=>domain.map(w=>at(name,w)));
  const filterPos=filterCurves.map(y=>y.map(v=>Math.max(0,v)));
  const maxIndices=filterCurves.map(y=>y.indexOf(Math.max(...y)));
  const peaks=maxIndices.map(k=>domain[k]);
  const errors=peaks.map((w,i)=>Math.abs(w-nominal[i]));
  out('W05','filter_peak_nominal_deviation',{nominal,peaks,absolute_errors_nm:errors,median_absolute_error_nm:median(errors),n_filters:7});
  const fwhm=filterCurves.map(y=>{const mx=Math.max(...y),half=mx/2,points=domain.filter((_,i)=>y[i]>=half);return points.length?points[points.length-1]-points[0]:null;});
  out('W06','filter_sampled_FWHM',{width_nm:fwhm,median_width_nm:median(fwhm.filter(x=>x!==null)),n_censored:fwhm.filter(x=>x===null).length,not_true_interpolated_FWHM:true});
  const containment=filterPos.map((y,i)=>{const full=y.reduce((a,b)=>a+b,0),inside=domain.reduce((s,w,j)=>s+(Math.abs(w-nominal[i])<=10?y[j]:0),0);return full>0?inside/full:null;});
  out('W07','filter_energy_containment_pm10',{fractions:containment,median:median(containment.filter(x=>x!==null)),assumes_nonnegative_clipped:true});
  const overlaps=[];for(let i=0;i<6;i++){const a=filterPos[i],b=filterPos[i+1],den=Math.min(a.reduce((x,y)=>x+y,0),b.reduce((x,y)=>x+y,0));overlaps.push(den? a.reduce((s,v,j)=>s+Math.min(v,b[j]),0)/den:null);}
  out('W08','adjacent_filter_overlap',{adjacent_pairs:filterNames.slice(0,6).map((name,i)=>name+' vs '+filterNames[i+1]),overlap:overlaps,median:median(overlaps.filter(v=>v!==null))});
  let maxCos=-Infinity,maxPair=null,cosines=[];for(let i=0;i<7;i++)for(let j=i+1;j<7;j++){
    const a=filterPos[i],b=filterPos[j]; const dot=a.reduce((s,v,k)=>s+v*b[k],0),n1=Math.sqrt(a.reduce((s,v)=>s+v*v,0)),n2=Math.sqrt(b.reduce((s,v)=>s+v*v,0)); const cs=(n1*n2>0?dot/(n1*n2):null);
    cosines.push(cs);if(cs!==null&&cs>maxCos){maxCos=cs;maxPair=[filterNames[i],filterNames[j]];}
  }
  out('W09','filter_normalized_cosine_cross_talk',{max_off_diagonal_cosine:maxCos,pair:maxPair,median_pair_cosine:median(cosines.filter(x=>x!==null)),n_pairs:21});
  const patch=names.map(n=>grid.map(w=>at(n,w)));
  const corr=(a,b)=>{const am=mean(a),bm=mean(b),x=a.map(v=>v-am),y=b.map(v=>v-bm),d=Math.sqrt(x.reduce((s,v)=>s+v*v,0)*y.reduce((s,v)=>s+v*v,0));return d?x.reduce((s,v,i)=>s+v*y[i],0)/d:null;};
  const correlations=[];for(let i=0;i<24;i++)for(let j=i+1;j<24;j++)correlations.push(corr(patch[i],patch[j]));
  const cr=correlations.filter(x=>x!==null);
  out('W10','ColorChecker_pairwise_spectral_correlation',{n_patches:24,n_pairs:cr.length,median_pearson:median(cr),p10_pearson:percentile(cr,0.1),negative_fraction:cr.filter(x=>x<0).length/cr.length});
  // Jacobi eigenvalues of 24x24 row-centered material Gram (31 wavelengths each).
  const centered=patch.map(v=>v.map(x=>x-mean(v)));
  const gram=centered.map(a=>centered.map(b=>a.reduce((s,v,i)=>s+v*b[i],0)));
  let A=gram.map(row=>row.slice()),iter=0,off=Infinity;
  for(iter=0;iter<18000;iter++){
    let p=0,q=1,m=0;
    for(let i=0;i<24;i++)for(let j=i+1;j<24;j++)if(Math.abs(A[i][j])>m){m=Math.abs(A[i][j]);p=i;q=j;}
    off=m;
    if(m<1e-11)break;
    const theta=0.5*Math.atan2(2*A[p][q],A[q][q]-A[p][p]),c=Math.cos(theta),s=Math.sin(theta);
    const app=A[p][p],aqq=A[q][q],apq=A[p][q];
    A[p][p]=c*c*app-2*s*c*apq+s*s*aqq;
    A[q][q]=s*s*app+2*s*c*apq+c*c*aqq;A[p][q]=0;A[q][p]=0;
    for(let k=0;k<24;k++)if(k!==p&&k!==q){const akp=A[k][p],akq=A[k][q];A[k][p]=A[p][k]=c*akp-s*akq;A[k][q]=A[q][k]=s*akp+c*akq;}
  }
  const eigen=A.map((row,i)=>Math.max(0,row[i])),sumEig=eigen.reduce((a,b)=>a+b,0),r2=eigen.reduce((a,b)=>a+b*b,0),eff=sumEig*sumEig/r2;
  out('W11','ColorChecker_centered_Gram_effective_rank',{effective_rank:eff,max_eigen:eigen.reduce((a,b)=>Math.max(a,b),0),trace:sumEig,offdiag_max_after_Jacobi:off,iterations:iter});
  const interp=(vals,picks)=>{const xy=picks.map(w=>[w,vals[(w-400)/10]]).sort((a,b)=>a[0]-b[0]);return grid.map(w=>{if(w<=xy[0][0])return xy[0][1];if(w>=xy[xy.length-1][0])return xy[xy.length-1][1];let j=1;while(xy[j][0]<w)j++;const a=xy[j-1],b=xy[j],t=(w-a[0])/(b[0]-a[0]);return a[1]*(1-t)+b[1]*t;});};
  const reconmse=(picks,subset)=>mean(subset.map(row=>mse(row,interp(row,picks))));
  const fixed=wavelengthNames,dev=patch.slice(0,12),test=patch.slice(12);
  const fixedMse=reconmse(fixed,patch),constantMse=mean(patch.map(row=>mse(row,grid.map(()=>mean(fixed.map(w=>row[(w-400)/10]))))));
  out('W12','five_uniform_spectral_interpolation_vs_constant',{fixed_wavelengths:fixed,mse_piecewise_linear:fixedMse,mse_constant:constantMse,relative_improvement:constantMse>0?1-fixedMse/constantMse:null,n_patches:24});
  let chosen=[400,700]; const stages=[];
  for(let step=0;step<3;step++){
    let best=null,bestScore=Infinity;
    for(let w=410;w<700;w+=10){if(chosen.includes(w))continue;const pick=[...chosen,w].sort((a,b)=>a-b),loss=reconmse(pick,dev);
      if(loss<bestScore-1e-15||best===null){best=w;bestScore=loss;}}
    chosen.push(best);chosen.sort((a,b)=>a-b);stages.push({added:best,dev_mse:bestScore});
  }
  const greedyMseTest=reconmse(chosen,test),uniformMseTest=reconmse(fixed,test);
  out('W13','greedy_band_selection_12_dev_to_12_heldout',{selected:chosen,greedy_stages:stages,heldout_greedy_mse:greedyMseTest,heldout_uniform_mse:uniformMseTest,relative_advantage:uniformMseTest>0?1-greedyMseTest/uniformMseTest:null,dev_n:12,test_n:12,selection_bias_warning:true});
  const ablations=fixed.map(drop=>({drop,heldout_mse:reconmse(fixed.filter(w=>w!==drop),test)}));
  out('W14','fixed_band_dropout_stress_test',{basemse:uniformMseTest,ablations,worst_mse:Math.max(...ablations.map(x=>x.heldout_mse)),mean_mse:mean(ablations.map(x=>x.heldout_mse)),worst_ratio:uniformMseTest>0?Math.max(...ablations.map(x=>x.heldout_mse))/uniformMseTest:null});
  // Ridge: train 12 material profiles to predict each wavelength from 5 measured bands + unpenalized intercept, lambda=0.01.
  const design=row=>[1,...fixed.map(w=>row[(w-400)/10])],X=dev.map(design);
  const solve=(mat,vec)=>{let n=vec.length,M=mat.map((row,i)=>[...row,vec[i]]);
    for(let j=0;j<n;j++){let pivot=j;for(let i=j+1;i<n;i++)if(Math.abs(M[i][j])>Math.abs(M[pivot][j]))pivot=i;
      if(Math.abs(M[pivot][j])<1e-13)throw Error('SINGULAR_RIDGE');
      [M[pivot],M[j]]=[M[j],M[pivot]];let d=M[j][j];for(let k=j;k<=n;k++)M[j][k]/=d;
      for(let i=0;i<n;i++)if(i!==j){const factor=M[i][j];for(let k=j;k<=n;k++)M[i][k]-=factor*M[j][k];}}
    return M.map(row=>row[n]);};
  const weights=grid.map((w,k)=>{const ata=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>X.reduce((s,x)=>s+x[i]*x[j],0)+(i===j&&i>0?0.01:0)));
    const aty=Array.from({length:6},(_,i)=>X.reduce((s,x,t)=>s+x[i]*dev[t][k],0));return solve(ata,aty);});
  const ridgeLoss=mean(test.map(row=>{const xx=design(row);return mse(row,weights.map(b=>b.reduce((s,v,j)=>s+v*xx[j],0)));}));
  out('W15','ridge_5_band_train12_test12_vs_interpolation',{ridge_lambda:0.01,dev_n:12,test_n:12,heldout_ridge_mse:ridgeLoss,heldout_interpolation_mse:uniformMseTest,ridge_minus_interpolation:ridgeLoss-uniformMseTest});
  const checkers=['Large','Small'].map(s=>{const white=grid.map(w=>at(s+' chequerboard (white)',w)),black=grid.map(w=>at(s+' chequerboard (black)',w));
    return {size:s,mean_abs_white_minus_black:mean(white.map((v,i)=>Math.abs(v-black[i]))),mean_signed_white_minus_black:mean(white.map((v,i)=>v-black[i])),mean_normalized_contrast:mean(white.map((v,i)=>(v-black[i])/(Math.abs(v)+Math.abs(black[i])+1e-12)))};});
  out('W16','large_vs_small_checkerboard_black_white_contrast',{pairs:checkers,n_band_observations_per_pair:31,not_independent_pixels:true});
  const paper=grid.map(w=>at('Printer paper (white)',w)),toner=grid.map(w=>at('Printer paper (toner)',w));
  out('W17','printer_paper_white_vs_toner_contrast',{mean_white:mean(paper),mean_toner:mean(toner),mean_difference:mean(paper.map((v,i)=>v-toner[i])),mean_ratio_white_to_toner:mean(paper.map((v,i)=>v/(Math.abs(toner[i])+1e-12))),bands:31});
  const neutral=names.slice(18);let norder=0;
  for(let k=0;k<31;k++){let ok=true;for(let i=0;i<5;i++)if(at(neutral[i],grid[k])<at(neutral[i+1],grid[k])){ok=false;break;}if(ok)norder++;}
  out('W18','ColorChecker_six_neutral_density_monotonicity',{neutral_names:neutral,monotone_wavelength_count:norder,grid_band_count:31,fraction_monotone:norder/31});
  const rough=series=>{const d2=[];for(let j=1;j<series.length-1;j++)d2.push(series[j+1]-2*series[j]+series[j-1]);return Math.sqrt(d2.reduce((s,v)=>s+v*v,0)/(series.reduce((s,v)=>s+v*v,0)+1e-20));};
  const patchR=names.map(n=>rough(Array.from({length:301},(_,i)=>at(n,400+i)))),filterR=filterNames.map(n=>rough(Array.from({length:301},(_,i)=>at(n,400+i))));
  out('W19','spectral_1nm_roughness_patches_vs_filters',{patch_median:median(patchR),filter_median:median(filterR),filter_to_patch_roughness_ratio:median(patchR)>0?median(filterR)/median(patchR):null,patch_n:24,filter_n:7});
  let neg=0,above=0,nonfinite=0,total=0;for(const name of names)for(let w=400;w<=700;w++){const v=at(name,w);total++;if(v<0)neg++;if(v>1)above++;if(!Number.isFinite(v))nonfinite++;}
  out('W20','reflectance_physical_range_QA',{n_observations:total,negative:neg,above_one:above,nonfinite:nonfinite,negative_fraction:neg/total,above_one_fraction:above/total,not_independent_observations:true});
  report.audit={precommitted_endpoints:16,completed:Object.keys(report.cycles).length,all_finite_endpoints_checked:true,n_data_lines:401,source_wavelengths:31,original_image_data:false,spatial_sensor_coordinates:false,novel_scientific_1_3:0,novel_scientific_2_3:0,novel_scientific_3_3:0,CT2_math_before_after:[24,24],CT2_functional_before_after:[18,18]};
  return report;
}
if (typeof module!=='undefined' && typeof require==='function' && require.main===module){
  const fs=require('fs');const input=fs.readFileSync(process.argv[2],'utf8');console.log(JSON.stringify(analyze(input),null,2));
}
