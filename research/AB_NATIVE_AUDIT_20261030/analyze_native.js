
/* LARP native N400 audit: PURE JS, no network or files.
Input is six immutable original certificates, two original summary records, one prior provenance audit.
Registration: Post-exposure calculations, NOT confirmatory inference, NOT raw NPZ verification.
*/
function analyzeNative(certs,summaries,prov){
const names=["A","B","C","D","E","union"], seeds=[1101,1102,1103], rad=[0.5,2,4,5];
const get=(seed,t)=>certs[String(seed)][t];
const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
const round=x=>Number.isFinite(x)?+x.toPrecision(10):null;
const paired=(metric)=>{
 const rows=seeds.map(seed=>{let full=metric(get(seed,"full_spectral")),local=metric(get(seed,"local_only"));return{seed,full:round(full),local:round(local),difference:round(full-local),ratio:round(local!==0?full/local:NaN)}})
 return{rows,means:{full:round(mean(rows.map(x=>x.full))),local:round(mean(rows.map(x=>x.local))),difference:round(mean(rows.map(x=>x.difference))),ratio_of_means:round(mean(rows.map(x=>x.full))/mean(rows.map(x=>x.local)))},paired_wins:rows.filter(x=>x.difference<0).length};
};
const checks=[];
function add(id,title,question,evidence,expected=""){
 checks.push({id,title,question,outcome:evidence,status:"COMPLETED_DOCUMENTARY_AB_R",expected,falsifier:"A source-level contradiction, missing value or opposite paired sign invalidates the claimed scoped direction",caveats:"Three pre-existing matched geometry seeds; same code family; post-exposure archive; no independent geometric measurements, no blind holdout, no original NPZ verification",originality:"KNOWN_OR_DESCRIPTIVE_0_OF_3",independent_replication:false});
}
const provOK=prov.comparison?.shared_hashes_all_equal===true && prov.comparison?.runtime_equal===true;
const hashCheck=seeds.map(seed=>({seed,centers:Array.from(new Set(["full_spectral","local_only"].map(t=>get(seed,t).centers_hash))),counts:Array.from(new Set(["full_spectral","local_only"].map(t=>JSON.stringify(get(seed,t).counts))))}));
add("N01","Centro y configuración de conteos","¿Coinciden ventana de muestreo y vector de conteos por cada pareja?",{provenance_shared_code:provOK,paired_hashes:hashCheck}, "Centros/counts compartidos");
add("N02","Identidad inicial","¿Coinciden inicialización y etiquetas?",{pairs:prov.individual_manifests.map(x=>({seed:x.seed,initial_equal:x.initial_points_hash_equal,labels_equal:x.labels_hash_equal,attempt_zero:x.same_attempt_zero}))},"Tres pares emparejados por inicialización");
add("N03","Puertas de admisión","¿La selección full vs LOCAL usa criterio de exclusión distinto?",{per_seed:seeds.map(seed=>({seed,full_cert:get(seed,"full_spectral").scientific_admissible,local_cert:get(seed,"local_only").scientific_admissible})),summary_counts:{full:summaries.full_spectral.admitted_count,local_packed:summaries.local_only.packed_control_count,local_mhu:summaries.local_only.finite_MHU_admitted_count}},"Full certificado, LOCAL empaquetado");
add("N04","No asintótico","¿Los originales acreditan hiperuniformidad termodinámica?",{all_explicitly_not_asymptotic:seeds.every(seed=>["full_spectral","local_only"].every(t=>get(seed,t).asymptotic_proof===false)),anisotropy_audits:seeds.map(seed=>["full_spectral","local_only"].map(t=>({seed,t,status:get(seed,t).anisotropy_controls?.status})))}, "No extrapolar certificado finito");
for(const [id,type] of [["N05","union"],["N06","A"],["N07","B"],["N08","C"],["N09","D"],["N10","E"]]){
 add(id,type==="union"?"Baja frecuencia del conjunto":`Baja frecuencia de especie ${type}`,`Comparación del S medio en los seis modos optimizados para ${type}`,paired(o=>o.components[type].restricted_mean_S),"S reducido full por diseño");
}
add("N11","Modos no optimizados","¿Hay deterioro de potencia fuera de los seis modos optimizados?",{per_component:Object.fromEntries(names.map(type=>[type,paired(o=>o.components[type].maximum_nonoptimized_S_over_N)]))},"Signo no prefijado; conservar rebound");
add("N12","Rebote post-corte","¿Mejora el espectro justo fuera de la banda restringida?",{per_component:Object.fromEntries(names.map(type=>[type,paired(o=>o.rebound_after_cutoff.mean_S[type])])),criterion_used:seeds.every(s=>!get(s,"full_spectral").rebound_after_cutoff.is_admission_criterion)},"No optimizado, por tanto sin adjudicación favorable");
for(let j=0;j<rad.length;j++){
 const id=`N${String(13+j).padStart(2,"0")}`,r=rad[j];
 add(id,`Ventana conteo R=${r}`,`Varianza espacial en ventana circular de radio ${r}`,{by_type:Object.fromEntries(names.map(type=>[type,paired(o=>{const w=o.window_statistics[type];const i=w.radii.findIndex(x=>Math.abs(x-r)<1e-9);if(i<0)throw Error("missing radius");return w.variance[i]})]))},radius:r},"Comparación emparejada, centros de ventana correlacionados");
}
add("N17","Vecinos de tipo próximo","¿Afectó el término espectral a la distancia p95 al tipo más cercano?",{by_type:Object.fromEntries(names.slice(0,5).map(type=>[type,paired(o=>o.descriptive.nearest_type[type].distance_to_type_p50_p90_p95[2])]))},"No asumir signo favorable");
add("N18","Voronoi y orden angular","¿Qué impacto local se observa en dispersión de áreas y orden hexagonal?",{voronoi:paired(o=>o.descriptive.voronoi.variance),q6_local:paired(o=>o.descriptive.orientational_order.q6.local_abs_mean),q6_global:paired(o=>o.descriptive.orientational_order.q6.global_abs)},"No equivale a CVT en riesgo funcional");
add("N19","Grafo nativo documental","¿Se cumple conectividad en las redes originales?",{records:seeds.map(seed=>({seed,full:summaries.full_spectral.records.find(x=>x.seed===seed),local:summaries.local_only.records.find(x=>x.seed===seed)})).map(x=>({seed:x.seed,full_scc:x.full.SCC_count,local_scc:x.local.SCC_count,same_port_digest:x.full.port_digest===x.local.port_digest,full_port:x.full.port_digest,local_port:x.local.port_digest}))},"Certificado no es entrenamiento ni transmisión funcional medida");
add("N20","Puerta de evidencia independiente","¿Existen bytes nativos accesibles y ejecución genuina Wei / datos ópticos en el entorno?",{read_access:"GitHub connector rejects binary NPZ with UnicodeDecodeError; local container cannot resolve GitHub host DNS; original original native coordinate reconstruction NOT performed",licensed_original_wei:"Original Wei code visible but not built or run; Poisson proxy is NOT Wei",real_bands:"CAVE and other multispectral sources documented but not downloaded",next_action:"Windows executor with GitHub access must export native six NPZ and hashes, compile authentic Wei on frozen commit, choose independent true 5+ band source; freeze A–J+code BEFORE new outcomes",gate:"STOP_NATIVE_FUNCTIONAL_NO_RAW_BYTES"},"No upgraded validity from existing certificate");
return{schema:"AB_3_2_1_NATIVE_AUDIT",date:"2026-10-30",count:checks.length,units:"3 geometries x 2 treatments, not 6 external datasets",checks,scope:"post-exposure documentary analytic, no causal / asymptotic / functional claims",methods:"paired differences and ratios exactly derived from original six certificate JSONs",source:"GalexY3/proyecto-LARP/legacy/local_lab_20261022/artifacts/avian_v1/"};
}
