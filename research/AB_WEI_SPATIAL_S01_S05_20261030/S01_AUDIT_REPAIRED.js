function parseRFC4180Line(line) {
  const fields=[];let cur='',quoted=false;
  for(let i=0;i<line.length;i++){
    const c=line[i];
    if(c==='"'){if(quoted&&line[i+1]==='"'){cur+='"';i++;}else{quoted=!quoted;}}
    else if(c===','&&!quoted){fields.push(cur);cur='';}
    else{cur+=c;}
  }
  if(quoted)throw Error('UNTERMINATED_CSV_QUOTE');
  fields.push(cur);return fields;
}

/* S01 frozen audit of genuine Sentinel-2 match-ups, no machine learning.
 * Does not re-publish any coordinates or raw data.
 */
function auditS01(csv) {
  const lines=csv.trim().split(/\r?\n/),columns=parseRFC4180Line(lines[0]);
  const required=['satellite_id','Site_name','Latitude','Longitude','acq_datetime','GLORIA_ID','B1','B2','B3','B4','B5','B6','B7','n_valid_pixels','n_total_pixels','cloud_percent','time_diff_days'];
  if(new Set(columns).size!==columns.length||required.some(x=>!columns.includes(x)))throw Error('MISSING_OR_DUPLICATE_REQUIRED_COLUMN');
  const col=Object.fromEntries(columns.map((x,i)=>[x,i]));
  const entries=[];const errs={bad_shape:0,bad_coordinates:0,bad_spectral_nonfinite:0,bad_pixel_counts:0,zero_valid_pixel:0,bad_cloud_range:0,bad_time_difference:0,bad_iso_date:0};
  let duplicates=0;const seen=new Set();const dupIDs=new Map();const instrumentSet=new Set();const labelCounts=new Map();
  const count=(m,k)=>(m.set(k,(m.get(k)||0)+1));
  for(let i=1;i<lines.length;i++){
    const row=parseRFC4180Line(lines[i]);
    if(row.length!==columns.length){errs.bad_shape++;continue;}
    const get=k=>row[col[k]],val=k=>Number(get(k)),site=get('Site_name'),id=get('GLORIA_ID');
    const bands=Array.from({length:7},(_,j)=>val('B'+(j+1)));
    const coords=[val('Latitude'),val('Longitude')],vp=val('n_valid_pixels'),tp=val('n_total_pixels'),cloud=val('cloud_percent'),lag=val('time_diff_days');
    if(!coords.every(Number.isFinite)||coords[0]<-90||coords[0]>90||coords[1]<-180||coords[1]>180)errs.bad_coordinates++;
    if(!bands.every(Number.isFinite))errs.bad_spectral_nonfinite++;
    if(!Number.isInteger(vp)||!Number.isInteger(tp)||vp<0||tp<=0||vp>tp)errs.bad_pixel_counts++;
    if(vp===0)errs.zero_valid_pixel++;
    if(!Number.isFinite(cloud)||cloud<0||cloud>100)errs.bad_cloud_range++;
    if(!Number.isFinite(lag)||lag<0)errs.bad_time_difference++;
    if(!Number.isFinite(Date.parse(get('acq_datetime'))))errs.bad_iso_date++;
    const key=[id,get('satellite_id'),get('Latitude'),get('Longitude')].join('|');
    if(seen.has(key))duplicates++;else seen.add(key);
    count(dupIDs,id);count(labelCounts,site);instrumentSet.add(get('sensor'));
    const basic=bands.every(Number.isFinite)&&coords.every(Number.isFinite)&&vp>=0&&tp>0&&vp<=tp&&cloud>=0&&cloud<=100&&lag>=0&&Number.isFinite(Date.parse(get('acq_datetime')));
    entries.push({site,id,satellite:get('satellite_id'),vp,tp,cloud,lag,qualityA:basic,qualityB:basic&&vp>=10,qualityC:basic&&vp>=10&&cloud<=20&&lag<=5});
  }
  const summarize=flag=>{
    const x=entries.filter(x=>x[flag]),sites=new Map();
    for(const y of x)count(sites,y.site);
    return {rows:x.length,unique_sites:sites.size,sites_with_at_least_2_rows:[...sites.values()].filter(n=>n>=2).length,unique_in_situ_ids:new Set(x.map(z=>z.id)).size,unique_satellite_products:new Set(x.map(z=>z.satellite)).size,median_valid_pixel_fraction:x.length?([...x].map(x=>x.vp/x.tp).sort((a,b)=>a-b)[Math.floor(x.length/2)]):null};
  };
  const A=summarize('qualityA'),B=summarize('qualityB'),C=summarize('qualityC');
  return {protocol:'S01_7_BAND_FIELD_QC',source:'chuishun-kong/id-dbo@26b8f243bdf3574ea2bb25eee927c720fa309dcb',source_git_blob:'4e6e5794d7c8f78b607fb7aa48b71edd918bd28a',csv_lines:lines.length,parsed_records:entries.length,
    issues:errs,exact_duplicates:duplicates,duplicated_in_situ_ids:[...dupIDs.values()].filter(n=>n>1).length,
    instrument_types:[...instrumentSet].sort(),site_count_all:labelCounts.size,
    filters:{A,B,C},eligible_S02:C.rows>=30&&C.unique_sites>=6&&C.sites_with_at_least_2_rows>=4,
    unit:'satellite_in_situ_matchup_not_imagery_pixel',scientific_novelty:'0/3',
    caveats:['SOURCE_OWNERS_WARN_INSITU_DEVELOPMENT_OVERLAP','SITE_AND_SATELLITE_ID_DEPENDENCE','NO_2D_FULL_MULTIBAND_CUBE','NO_WEI_BINARY','DATA_LICENSE_NOT_VERIFIED']};
}