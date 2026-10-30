/* W22, CIE 1931 2 degree 1nm source table: synthetic equal-energy tristimulus loss. */
function audit22(measuredCSV, cieCSV) {
  const names=['dark skin','light skin','blue sky','foliage','blue flower','bluish green','orange','purplish blue','moderate red','purple','yellow green','orange yellow','blue','green','red','yellow','magenta','cyan','white 9.5 (.05 D)','neutral 8 (.23 D)','neutral 6.5 (.44 D)','neutral 5 (.70 D)','neutral 3.5 (1.05 D)','black 2 (1.5 D)'];
  const data=measuredCSV.trim().split(/\r?\n/),heads=data[0].split(','),cols=new Map(heads.map((x,i)=>[x,i]));
  const wavelengths=Array.from({length:31},(_,i)=>400+10*i),rowmap=new Map();
  for(const line of data.slice(1)){const v=line.split(',').map(Number);if(v.some(x=>!Number.isFinite(x)))throw Error('MEASURED_BAD_NONFINITE');rowmap.set(v[0],v);}
  if(rowmap.size!==401)throw Error('EXPECTED_LAB_401');
  const cie=new Map();for(const line of cieCSV.trim().split(/\r?\n/)){const v=line.split(',').map(Number);if(v.length!==4||v.some(x=>!Number.isFinite(x)))throw Error('BAD_CIE_LINE');if(cie.has(v[0]))throw Error('DUP_CIE');cie.set(v[0],v.slice(1));}
  for(const w of wavelengths)if(!cie.has(w))throw Error('MISSING_CIE_'+w);
  const cieYsum=wavelengths.reduce((s,w)=>s+cie.get(w)[1],0);
  const fixed=[400,470,550,620,700],greedy=[400,470,530,610,700];
  function interp(full,picks){const x=picks.map(w=>[w,full[(w-400)/10]]).sort((a,b)=>a[0]-b[0]);return wavelengths.map(w=>{
    if(w<=x[0][0])return x[0][1];if(w>=x[x.length-1][0])return x[x.length-1][1];
    let j=1;while(x[j][0]<w)j++;const a=x[j-1],b=x[j],q=(w-a[0])/(b[0]-a[0]);return a[1]*(1-q)+b[1]*q;});}
  const XYZ=v=>[0,1,2].map(c=>wavelengths.reduce((s,w,i)=>s+v[i]*cie.get(w)[c],0)/cieYsum);
  const sqerr=(a,b)=>a.reduce((s,x,i)=>s+(x-b[i])**2,0)/3;
  const results=names.slice(12).map(name=>{if(!cols.has(name))throw Error('MISSING_PATCH_'+name);const original=wavelengths.map(w=>rowmap.get(w)[cols.get(name)]);
    const goal=XYZ(original),errF=sqerr(goal,XYZ(interp(original,fixed))),errG=sqerr(goal,XYZ(interp(original,greedy)));
    return {name,xyz_error_fixed:errF,xyz_error_greedy:errG,greedy_better:errG<errF};});
  const mean=v=>v.reduce((a,b)=>a+b,0)/v.length;
  const fixedMean=mean(results.map(r=>r.xyz_error_fixed)),greedyMean=mean(results.map(r=>r.xyz_error_greedy));
  return {id:'W22',status:'COMPUTED_HYPOTHETICAL_EQUAL_ENERGY_CIE_XYZ_LOSS',cie_source_repo:'sblisesivdin/spectrum-to-rgb',cie_source_git_blob:'9b4e3f73b4bb412a762a6d03cb8060bfea652a6e',cie_official_doi:'10.25039/CIE.DS.xvudnb9b',measured_git_blob:'82b83444716930c75e1d2a77ac6eed9fd6ccdc8d',
    cie_row_count:cie.size,reflectance_wavelength_range:'400-700nm 10nm steps',hypothetical_illuminant:'E_equal_energy_not_actual_illumination',
    fixed_picks:fixed,greedy_picks:greedy,heldout_n:12,heldout_per_patch:results,
    mean_xyz_squared_error_fixed:fixedMean,mean_xyz_squared_error_greedy:greedyMean,
    greedy_relative_advantage:fixedMean>0?1-greedyMean/fixedMean:null,greedy_better_patches:results.filter(r=>r.greedy_better).length,
    grade:'0/3',independent_standard_not_independent_lab:true,warnings:['NOT_MEASURED_COLOR_APPEARANCE','NOT_CALIBRATED_ILLUMINANT','SAME_12_PATCHES_W13_HOLDOUT_EXPOSED','NO_SPATIAL_MHU_OUTCOME']};
}
