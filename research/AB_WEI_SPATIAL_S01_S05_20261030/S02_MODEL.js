/* S02 - seven-band site and satellite-id separated reconstruction.
 * Frozen code, independent of any user MHU geometry or training code.
 */
function auditS02(csv) {
  function parseCSV(line) {
    const out=[];let cur='',quoted=false;
    for(let i=0;i<line.length;i++){const c=line[i];
      if(c==='"'){if(quoted&&line[i+1]==='"'){cur+='"';i++;}else quoted=!quoted;}
      else if(c===','&&!quoted){out.push(cur);cur='';}
      else cur+=c;
    }
    if(quoted)throw Error('UNCLOSED_QUOTE');out.push(cur);return out;
  }
  const lines=csv.trim().split(/\r?\n/),header=parseCSV(lines[0]),cols=Object.fromEntries(header.map((h,i)=>[h,i]));
  const required=['Site_name','satellite_id','cloud_percent','time_diff_days','n_valid_pixels','n_total_pixels','acq_datetime','Latitude','Longitude','B1','B2','B3','B4','B5','B6','B7'];
  if(required.some(x=>cols[x]===undefined)||new Set(header).size!==header.length)throw Error('BAD_HEADER');
  const siteIdx=cols.Site_name,satIdx=cols.satellite_id;let quarantined=0;
  const rows=[];
  for(const line of lines.slice(1)){
    const f=parseCSV(line);if(f.length!==header.length)throw Error('BAD_CSV_SHAPE');
    const num=k=>Number(f[cols[k]]),vp=num('n_valid_pixels'),tp=num('n_total_pixels'),cloud=num('cloud_percent'),lag=num('time_diff_days'),coords=[num('Latitude'),num('Longitude')];
    const bands=Array.from({length:7},(_,i)=>num('B'+(i+1)));
    const ok=bands.every(Number.isFinite)&&coords.every(Number.isFinite)&&vp>=10&&tp>0&&vp<=tp&&cloud>=0&&cloud<=20&&lag>=0&&lag<=5&&Number.isFinite(Date.parse(f[cols.acq_datetime]));
    if(!ok){quarantined++;continue;}
    rows.push({site:f[siteIdx],sat:f[satIdx],x:[bands[0],bands[1],bands[2],bands[4],bands[6]],y:[bands[3],bands[5]],b:bands});
  }
  if(rows.length>500)throw Error('RESOURCES_OVER_500');
  const siteFreq=new Map();for(const r of rows)siteFreq.set(r.site,(siteFreq.get(r.site)||0)+1);
  function solve(A,b){
    const n=b.length,m=A.map((r,i)=>r.concat(b[i]));
    for(let i=0;i<n;i++){let p=i;for(let k=i+1;k<n;k++)if(Math.abs(m[k][i])>Math.abs(m[p][i]))p=k;
      if(Math.abs(m[p][i])<1e-14)throw Error('SINGULAR_RIDGE');
      [m[p],m[i]]=[m[i],m[p]];const d=m[i][i];
      for(let j=i;j<=n;j++)m[i][j]/=d;
      for(let k=0;k<n;k++){if(k===i)continue;const v=m[k][i];for(let j=i;j<=n;j++)m[k][j]-=v*m[i][j];}
    }
    return m.map(r=>r[n]);
  }
  function ridge(train){
    const n=train.length,means=Array.from({length:5},(_,j)=>train.reduce((s,r)=>s+r.x[j],0)/n);
    const sig=means.map((v,j)=>Math.sqrt(train.reduce((s,r)=>s+(r.x[j]-v)**2,0)/n)||1);
    const ys=[0,1].map(j=>train.reduce((s,r)=>s+r.y[j],0)/n);
    const ysig=ys.map((v,j)=>Math.sqrt(train.reduce((s,r)=>s+(r.y[j]-v)**2,0)/n)||1);
    const X=train.map(r=>[1,...r.x.map((v,j)=>(v-means[j])/sig[j])]);
    const mat=Array.from({length:6},()=>Array(6).fill(0));
    for(const x of X)for(let i=0;i<6;i++)for(let j=0;j<6;j++)mat[i][j]+=x[i]*x[j];
    for(let j=1;j<6;j++)mat[j][j]+=1.0;
    const bs=[0,1].map(q=>{const v=Array(6).fill(0);for(let k=0;k<X.length;k++)for(let j=0;j<6;j++)v[j]+=X[k][j]*((train[k].y[q]-ys[q])/ysig[q]);return solve(mat,v);});
    return row=>{const x=[1,...row.x.map((v,j)=>(v-means[j])/sig[j])];
      return [0,1].map(q=>ys[q]+ysig[q]*bs[q].reduce((s,v,j)=>s+v*x[j],0));};
  }
  const sites=[...siteFreq.keys()].sort(),folds=[];
  for(const site of sites){
    const test=rows.filter(r=>r.site===site);
    if(test.length<2)continue;
    const heldSat=new Set(test.map(r=>r.sat));
    const train=rows.filter(r=>r.site!==site&&!heldSat.has(r.sat));
    const trainSites=new Set(train.map(r=>r.site));
    if(train.length<30||trainSites.size<5)continue;
    if(train.some(x=>x.site===site||heldSat.has(x.sat)))throw Error('LEAKY_FOLD');
    const predict=ridge(train),meanTargets=[0,1].map(q=>train.reduce((s,r)=>s+r.y[q],0)/train.length);
    const stat={ridge:0,interpolation:0,train_mean:0};
    for(const r of test){
      const preds={ridge:predict(r),interpolation:[(r.b[2]+r.b[4])/2,(r.b[4]+r.b[6])/2],train_mean:meanTargets};
      for(const k of Object.keys(stat))stat[k]+=((preds[k][0]-r.y[0])**2+(preds[k][1]-r.y[1])**2)/2/test.length;
    }
    if(Object.values(stat).some(v=>!Number.isFinite(v)))throw Error('NONFINITE_MODEL');
    folds.push({site,train_rows:train.length,test_rows:test.length,train_sites:trainSites.size,held_satellite_products:heldSat.size,blocked_by_shared_products:rows.filter(r=>r.site!==site&&heldSat.has(r.sat)).length,mse:stat});
  }
  if(folds.length<15)throw Error('INSUFFICIENT_ELIGIBLE_FOLDS_'+folds.length);
  const avg=k=>folds.reduce((s,f)=>s+f.mse[k],0)/folds.length;
  const A={ridge:avg('ridge'),interpolation:avg('interpolation'),train_mean:avg('train_mean')};
  const med=k=>{const a=folds.map(f=>f.mse[k]).sort((a,b)=>a-b);return a[Math.floor(a.length/2)];};
  return {protocol:'S02_5_TO_7_FIELD_RECONSTRUCTION',source_commit:'26b8f243bdf3574ea2bb25eee927c720fa309dcb',source_blob:'4e6e5794d7c8f78b607fb7aa48b71edd918bd28a',qualified_rows:rows.length,quarantined_rows:quarantined,qualified_sites:sites.length,
    test_units_sites:folds.length,folds,mean_site_mse:A,median_site_mse:{ridge:med('ridge'),interpolation:med('interpolation'),train_mean:med('train_mean')},
    ridge_to_interpolation_ratio:A.ridge/A.interpolation,site_wins_ridge:folds.filter(f=>f.mse.ridge<f.mse.interpolation).length,
    shared_product_excluded_total_across_folds:folds.reduce((s,f)=>s+f.blocked_by_shared_products,0),
    primary_unit:'site_mean_not_satellite_row',scientific_grade:'0/3',
    caveats:['SITE_NAME_MAY_NOT_IDENTIFY_UNIQUE_WATERBODY','SEVEN_BANDS_ORDINAL_NOT_CALIBRATED_WAVELENGTH_INTERPOLATION','SOURCE_GLORIA_OVERLAP','NOT_FULL_2D_HYPERSPECTRAL_IMAGE','NO_MHU_GEOMETRY_OR_WEI_COMPARISON']};
}