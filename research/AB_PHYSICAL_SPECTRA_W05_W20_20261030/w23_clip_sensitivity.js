/* W23 physically motivated exploratory sensitivity, reuses frozen W22 without modifying it. */
function audit23(measuredCSV, cieCSV, frozenW22) {
  if(typeof frozenW22!=='function')throw Error('NEED_ORIGINAL_FROZEN_W22');
  const names=['dark skin','light skin','blue sky','foliage','blue flower','bluish green','orange','purplish blue','moderate red','purple','yellow green','orange yellow','blue','green','red','yellow','magenta','cyan','white 9.5 (.05 D)','neutral 8 (.23 D)','neutral 6.5 (.44 D)','neutral 5 (.70 D)','neutral 3.5 (1.05 D)','black 2 (1.5 D)'];
  const lines=measuredCSV.trim().split(/\r?\n/),headers=lines[0].split(','),ix=names.map(n=>headers.indexOf(n));
  if(ix.some(i=>i<0))throw Error('MISSING_PATCH');
  let changedAll=0,changedHeldoutGrid=0,nonfinite=0;
  const revised=[lines[0]];
  for(const line of lines.slice(1)){
    const row=line.split(','),w=Number(row[0]);
    for(let k=0;k<ix.length;k++){const i=ix[k],v=Number(row[i]);if(!Number.isFinite(v)){nonfinite++;throw Error('NONFINITE');}
      const clipped=Math.max(0,Math.min(1,v));
      if(clipped!==v){changedAll++;if(k>=12&&w>=400&&w<=700&&(w-400)%10===0)changedHeldoutGrid++;row[i]=String(clipped);}
    }revised.push(row.join(','));
  }
  const original=frozenW22(measuredCSV,cieCSV);
  const clipped=frozenW22(revised.join('\n')+'\n',cieCSV);
  const ranking=(r)=>Math.sign(r.mean_xyz_squared_error_greedy-r.mean_xyz_squared_error_fixed);
  return {
    id:'W23',status:'COMPUTED_POST_HOC_MOTIVATED_EXPLORATORY',
    original_fixed_xyz_mse:original.mean_xyz_squared_error_fixed,original_greedy_xyz_mse:original.mean_xyz_squared_error_greedy,
    clipped_fixed_xyz_mse:clipped.mean_xyz_squared_error_fixed,clipped_greedy_xyz_mse:clipped.mean_xyz_squared_error_greedy,
    original_relative_greedy_advantage:original.greedy_relative_advantage,
    clipped_relative_greedy_advantage:clipped.greedy_relative_advantage,
    original_greedy_better_patches:original.greedy_better_patches,
    clipped_greedy_better_patches:clipped.greedy_better_patches,
    mean_ranking_reversed:ranking(original)!==ranking(clipped),
    changed_entries_all_24x401:changedAll,changed_entries_heldout12x31:changedHeldoutGrid,
    nonfinite_source_values:nonfinite,
    source_git_blobs:{lab:'82b83444716930c75e1d2a77ac6eed9fd6ccdc8d',CIE:'9b4e3f73b4bb412a762a6d03cb8060bfea652a6e',original_W22_code:'c6daf40fa5a0ce72e22c00412ea995243e81d1ca'},
    grade:'0/3',selection_exposure:'W20_ABOVE_ONE_ALREADY_SEEN',scientific_replication:false,
    caution:['CLIPPING_IS_NOT_A_CALIBRATION_CORRECTION','EQUAL_ENERGY_CIE_NOT_MEASURED_APPEARANCE','SAME_12_HELDOUT_PATCHES_AS_W13_W22','NO_MHU_NEURAL_EVIDENCE']
  };
}
