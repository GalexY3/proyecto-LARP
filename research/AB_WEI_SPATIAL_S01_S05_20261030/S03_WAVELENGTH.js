/* S03 source-frozen native wavelength interpolation adversary, same S02 folds. */
function auditS03(csv,priorS02){
  const source=priorS02.results || priorS02;
  if(source.protocol!=='S02_5_TO_7_FIELD_RECONSTRUCTION'||source.source_blob!=='4e6e5794d7c8f78b607fb7aa48b71edd918bd28a')throw Error('WRONG_S02_PRIOR');
  const parse=s=>{let fields=[],b='',q=false;for(let i=0;i<s.length;i++){const c=s[i];if(c==='"'){if(q&&s[i+1]==='"'){b+='"';i++;}else q=!q;}else if(c===','&&!q){fields.push(b);b='';}else b+=c;}if(q)throw Error('BAD_QUOTE');fields.push(b);return fields;};
  const lines=csv.trim().split(/\r?\n/),cols=Object.fromEntries(parse(lines[0]).map((x,i)=>[x,i])),sites=new Map(),known=new Set(['S2A','S2B']);
  const ws={S2A:[443,490,560,665,705,740,783],S2B:[442,492,559,665,704,739,780]};
  let qualified=0;
  for(let i=1;i<lines.length;i++){
    const x=parse(lines[i]),n=k=>Number(x[cols[k]]),site=x[cols.Site_name],sensor=x[cols.sensor];
    const bands=Array.from({length:7},(_,j)=>n('B'+(j+1)));
    const vp=n('n_valid_pixels'),tp=n('n_total_pixels'),cloud=n('cloud_percent'),lag=n('time_diff_days');
    const coords=[n('Latitude'),n('Longitude')];
    const eligible=bands.every(Number.isFinite)&&coords.every(Number.isFinite)&&vp>=10&&tp>0&&vp<=tp&&cloud>=0&&cloud<=20&&lag>=0&&lag<=5&&Number.isFinite(Date.parse(x[cols.acq_datetime]));
    if(!eligible)continue;qualified++;
    if(!known.has(sensor))throw Error('UNKNOWN_SENSOR_'+sensor);
    const w=ws[sensor],pred=[
       bands[2]+(bands[4]-bands[2])*(w[3]-w[2])/(w[4]-w[2]),
       bands[4]+(bands[6]-bands[4])*(w[5]-w[4])/(w[6]-w[4])
    ];
    const y=[bands[3],bands[5]];
    const loss=((pred[0]-y[0])**2+(pred[1]-y[1])**2)/2;
    if(!sites.has(site))sites.set(site,[]);
    sites.get(site).push(loss);
  }
  if(qualified!==source.qualified_rows)throw Error('QUALITY_FILTER_DISAGREEMENT');
  const folds=source.folds.map(f=>{
    const errors=sites.get(f.site);
    if(!errors||errors.length!==f.test_rows)throw Error('FOLD_PARITY_FAILED_'+f.site);
    return {site:f.site,n:f.test_rows,wavelength_mse:errors.reduce((a,b)=>a+b,0)/errors.length,
      ridge_mse:f.mse.ridge,ordinal_interpolation_mse:f.mse.interpolation};
  });
  const avg=k=>folds.reduce((s,f)=>s+f[k],0)/folds.length;
  const A={physical_wavelength:avg('wavelength_mse'),ordinal_band_index:avg('ordinal_interpolation_mse'),ridge:avg('ridge_mse')};
  if(Math.abs(A.ridge-source.mean_site_mse.ridge)>1e-14||Math.abs(A.ordinal_band_index-source.mean_site_mse.interpolation)>1e-14)throw Error('SOURCE_COMPARATOR_PARITY_FAILED');
  return {
    protocol:'S03_PHYSICAL_WAVELENGTH_ADVERSARY',source_commit:'26b8f243bdf3574ea2bb25eee927c720fa309dcb',
    fold_count:folds.length,qualified_records:qualified,
    folds,mean_site_mse:A,
    ridge_to_physical_ratio:A.ridge/A.physical_wavelength,
    physical_to_ordinal_ratio:A.physical_wavelength/A.ordinal_band_index,
    ridge_site_wins:folds.filter(f=>f.ridge_mse<f.wavelength_mse).length,
    physical_site_wins_over_ordinal:folds.filter(f=>f.wavelength_mse<f.ordinal_interpolation_mse).length,
    wavelengths_nm:ws,grade:'0/3',
    caveats:['POST_S02_EXPLORATORY','CENTRAL_WAVELENGTH_NOT_FULL_SRF','S2B_SRF_PLACEHOLDER_IN_SOURCE_REPO','SAME_34_SITE_FOLDS_NOT_EXTERNAL_REPLICATION','NO_MHU_GEOMETRY','NO_WEI_BINARY']
  };
}