/* W21 original averaged versus raw replicate consistency, source-only. */
function audit21(rawText,averageText) {
  const splitCSV=s=>{let out=[],buf='',quoted=false;for(let i=0;i<s.length;i++){const c=s[i];if(c==='"'){if(quoted&&s[i+1]==='"'){buf+='"';i++;}else quoted=!quoted;}else if(c===','&&!quoted){out.push(buf.trim());buf='';}else buf+=c;}if(quoted)throw Error('UNCLOSED_QUOTE');out.push(buf.trim());return out;};
  const parse=src=>{const lines=src.trim().split(/\r?\n/),head=splitCSV(lines[0]),columns=new Map(head.map((x,i)=>[x,i]));if(new Set(head).size!==head.length)throw Error('DUPLICATE_COLUMNS');
    const rows=new Map();for(let j=1;j<lines.length;j++){const p=splitCSV(lines[j]);if(p.length!==head.length)throw Error('BAD_ROW_FIELDS_'+j);
      const w=Number(p[0]);if(w!==349+j)throw Error('BAD_WAVELENGTH_'+w);const n=p.map(x=>Number(x));
      if(p.some(x=>x.length===0)||n.some(x=>!Number.isFinite(x)))throw Error('NONFINITE_'+w);rows.set(w,n);}if(rows.size!==401)throw Error('NOT_401_WAVELENGTHS');return {rows,columns};};
  const raw=parse(rawText),avg=parse(averageText);
  const at=(tab,col,w)=>{const index=tab.columns.get(col);if(index===undefined)throw Error('MISSING '+col);return tab.rows.get(w)[index];};
  const pairGroups=[
    ['550 nm',['550 nm','550 nm (2)']],
    ['Large chequerboard (white)',['Large chequerboard (white1)','Large chequerboard (white2)']],
    ['Large chequerboard (black)',['Large chequerboard (black1)','Large chequerboard (black2)']],
    ['Small chequerboard (white)',['Small chequerboard (white1)','Small chequerboard (white2)']],
    ['Small chequerboard (black)',['Small chequerboard (black1)','Small chequerboard (black2)']]
  ];
  const directNames=['400 nm','442 nm','500 nm','600 nm','650 nm','700 nm','Printer paper (white)','Printer paper (toner)','dark skin','light skin','blue sky','foliage','blue flower','bluish green','orange','purplish blue','moderate red','purple','yellow green','orange yellow','blue','green','red','yellow','magenta','cyan','white 9.5 (.05 D)','neutral 8 (.23 D)','neutral 6.5 (.44 D)','neutral 5 (.70 D)','neutral 3.5 (1.05 D)','black 2 (1.5 D)'];
  let globalMax=0,nTotal=0;
  const pairResults=pairGroups.map(([name,[a,b]])=>{let max=0,sumsq=0,repSumsq=0;
    for(let w=350;w<=750;w++){const v=(at(raw,a,w)+at(raw,b,w))/2,observed=at(avg,name,w),err=Math.abs(v-observed),dr=at(raw,a,w)-at(raw,b,w);
      max=Math.max(max,err);globalMax=Math.max(globalMax,err);sumsq+=err*err;repSumsq+=dr*dr;nTotal++;}
    return {name,maximum_absolute_averaging_discrepancy:max,rmse_averaging:Math.sqrt(sumsq/401),replicate_pair_rms_difference:Math.sqrt(repSumsq/401)};});
  let maxDirect=0;for(const name of directNames)for(let w=350;w<=750;w++)maxDirect=Math.max(maxDirect,Math.abs(at(raw,name,w)-at(avg,name,w)));
  const tol=0.00001;
  return {id:'W21',status:globalMax<=tol&&maxDirect<=tol?'CONSISTENT_WITH_SIMPLE_PAIR_AVERAGING':'INCONSISTENT_WITH_SIMPLE_PAIR_AVERAGING',
    source_named_git_blob:'ab00192d9b537d4b7942357ee7f2ed30ee623b12',source_averaged_git_blob:'82b83444716930c75e1d2a77ac6eed9fd6ccdc8d',
    pairResults,global_max_average_error:globalMax,max_direct_column_error:maxDirect,comparison_tolerance:tol,
    pair_positions_checked:nTotal,direct_positions_checked:directNames.length*401,
    laboratory_replicate_sets:5,source_independent_labs:1,grade:'0/3',warnings:['WAVELENGTH_SAMPLES_NOT_INDEPENDENT','DOES_NOT_PROVE_RAW_INSTRUMENT_CALIBRATION','ONE_SOURCE_ONLY']};
}
