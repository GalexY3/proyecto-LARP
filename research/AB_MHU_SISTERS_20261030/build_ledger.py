from pathlib import Path
import re, json, hashlib, datetime
p=Path(__file__).resolve().parent
s=(p/'INFORME_S01_S20.md').read_text()
raw=json.loads((p/'checks_20.json').read_text())
checks={r['id']:r for r in raw['checks']}
titles=re.findall(r'^### (S\d\d)\. (.+)$',s,flags=re.M)
assert len(titles)==20 and len(checks)==20
parts=re.split(r'^### (S\d\d)\. (.+)$',s,flags=re.M)
proofs={parts[i]:parts[i+2].strip() for i in range(1,len(parts),3)}
branches={f'S{i:02d}':('B01_PHASING' if i<=5 else 'B02_COVERAGE' if i<=10 else 'B03_SAMPLING' if i<=15 else 'B04_LABELS') for i in range(1,21)}
parents={'S03':'S02','S05':'S02','S07':'S06','S09':'S08','S12':'S11','S13':'S11','S14':'S11','S17':'S02','S18':'S01','S19':'S01','S20':'S14'}
priors={
'B01_PHASING':{'before':24,'after':24,'reason':'Phase cancellation and weights are rigorously characterized but existing AB08 and Wei overlap heavily; no new independent functionality.'},
'B02_COVERAGE':{'before':17,'after':17,'reason':'1D coverage/quantization establishes useful exact adversarial cases but is classical and does not resolve 3D sensors.'},
'B03_SAMPLING':{'before':15,'after':15,'reason':'Exact Fourier/noise/graph results clarify failure modes but are well known and lack a novel algorithmic advance.'},
'B04_LABELS':{'before':21,'after':21,'reason':'Exact biological-count reference and fairness of objectives clarify mechanism but no verified superior optimizer.'},
}
cycles=[]
for ident,title in titles:
  branch=branches[ident]; chk=checks[ident];assert chk['pass_check']
  cycles.append({
    'id':ident,'kind':'DEDUCTIVE_AB','campaign':'MHU_SISTERS_20261030','branch':branch,
    'status':'RUN_VALID_MATHEMATICAL_ANALYSIS','pre_commit':'f2c86270196df6eda87533953cc0169df81ec5a0',
    'code_commit':'e4a3605e0fad53418d7ca08f187c4d3ce1c440ce',
    'code_git_blob_sha':'56ec9c33fbb92f09fafac46270c48c1d6a6e7b7d',
    'code_sha256':'78751d1064d5dffcdff06669748be641e9f2a7a70df0410e460a3241ee1c6296',
    'A':{'question':title,'unit':'mathematical model/point pattern under stated conditional assumptions','truth_contract':'algebraic identity, exact counterexample, source-code derivation; not causal/real data'},
    'B':{'preferred':f'claim S{ident[1:]} of the frozen preregistration','null':'claim false or dependent on unacknowledged assumptions','rivals':'strong lattice/CVT/LOCAL, phase disorder, IID or structural counterexample as appropriate'},
    'C':{'discriminating_design':'direct analytic derivation plus model-specific finite exact/symbolic check, as written in complete report','proof_or_counterexample':proofs[ident]},
    'D':{'freeze_order':'prospective full prereg and COMPLETE code in GitHub BEFORE first audit execution','code_status':'frozen and blob identity checked before run','check_is_not_proof':True},
    'E':{'execution':'derivation documented and fixed verification program run once','check_result':chk['evidence'],'passed':chk['pass_check']},
    'F':{'adversarial':'domain restrictions and rival explanations documented in cycle proof; finite code check cannot certify generality','prior_art':'Jiao 2014, Wei 2010, Lomba 2020, Du et al CVT, Torquato HU and elementary Fourier/combinatorial identities'},
    'G':{'internal_symbolic_or_numeric_verification':True,'independent_peer_review':False,'external_replication':False,'formal_proof_assistant':False},
    'H':{'prior_update':'conditional model mechanism clarified; no update supporting universal MHU superiority','duplicate_or_dependency':parents.get(ident),'ct2_before':priors[branch]['before'],'ct2_after':priors[branch]['after'],'ct2_reason':priors[branch]['reason']},
    'I':{'internal_grade':'0/3 known/elementary mathematical identity or source-specific analytic corollary','new_n1':False,'new_n2':False,'new_n3':False,'novelty_audited':'not certified beyond prior-art review','validity':'mathematical conditional only'},
    'J':{'decision':'CLOSE_FORMAL_QUESTION','next':'advance only to matched-cost physically grounded modalities or constrained multiobjective theorem with genuinely new prediction','no_main_merge':True}
  })
ledger={'schema':'LARP_AB321_SISTERS20_V1','date':'2026-10-30','grant':20,'valid_formal_questions':len(cycles),'invalid':0,'planning':0,'n1_new_unique':0,'n2':0,'n3':0,'baseline':'The prior 18 formal cycles are historical and not counted in this grant.','mathematical_independence':'Many results share elementary Fourier, packing or combinatorial ancestry; 20 cycles do NOT mean 20 independent original findings.','data':'Original source-code analysis; no new independent observational data','frozen_code_sha256':cycles[0]['code_sha256'],'raw_checks_sha256':hashlib.sha256((p/'checks_20.json').read_bytes()).hexdigest(),'CT2_by_branch':priors,'cycles':cycles}
(p/'LEDGER_S01_S20.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
source=[{'url':'https://doi.org/10.1103/PhysRevE.89.022721','claim':'avian multi-hyperuniformity prior art'},{'url':'https://doi.org/10.1103/PhysRevE.102.012134','claim':'heterocoordination prior art'},{'url':'https://www.liyiwei.org/papers/noise-sig10/','claim':'multiclass blue noise strong competitor'},{'url':'https://doi.org/10.1137/S0036144599352836','claim':'CVT quantization prior art'},{'url':'https://doi.org/10.1103/PhysRevE.94.022122','claim':'hyperuniformity general theory'},{'url':'https://doi.org/10.1051/epjam/2024003','claim':'multihyperuniform antenna applications'}]
(p/'SOURCES.json').write_text(json.dumps(source,ensure_ascii=False,indent=2))
(p/'PRIORS_DELTA.md').write_text('''# LARP MHU Sisters: apéndice de priors 2026-10-30\n\nConservar priors históricos y no deducir originalidad de pruebas algebraicas.\n\nP-SIST01 [MATEMATICO_CONOCIDO] LOCAL, MHUv1 y MHUv2 optimizan objetivos DISTINTOS; v2 cambia pesos baja-k a 1/k², no garantiza mejor downstream (S01,S13).\nP-SIST02 [MATEMATICO_CONOCIDO] Fases intertipo pueden cancelar una frecuencia a magnitudes fijas, pero una familia de uniones de pares no puede cancelar todo simultáneamente sin restricciones (S02,S03,S04,S05).\nP-SIST03 [MATEMATICO_CONOCIDO] Cobertura minimax y cuantización CVT de 1D pueden alcanzarse simultáneamente con cantidades iguales, y cuotas desiguales pueden impedir retícula multiclase exacta (S06,S07,S08).\nP-SIST04 [MATEMATICO_CONOCIDO] El espectro stealth de banda finita no fuerza radio de cobertura óptimo (S09); IID tiene un riesgo explícito de zonas sin clase (S10).\nP-SIST05 [MATEMATICO_CONOCIDO] IID S=1 esperado, retícula exacta resuena, jitter añade piso de ruido; la distribución de frecuencia de las señales decide eficiencia (S11,S12,S13,S14).\nP-SIST06 [MATEMATICO_CONOCIDO] El grafo no se identifica mediante la geometría de puntos sola; tener más Fiedler no demuestra mejor aprendizaje (S15).\nP-SIST07 [MATEMATICO_CONOCIDO] La mezcla de etiquetas sin orden produce alta heterotipia nula con las propias cuotas (73.89%) y piso espectral positivo por subtipo aunque unión sea stealth (S16,S17).\nP-SIST08 [MATEMATICO_CONOCIDO] El óptimo GLOBAL de suma local+espectral sacrifica necesariamente algo de mínimo local a cambio de S; los algoritmos prácticos pueden no alcanzar ningún óptimo (S18).\nP-SIST09 [ARQUITECTURA_ESPECIFICA] El promedio tipo uniforme sobreproporciona el efecto de una especie escasa respecto a un promedio ponderado por cuota, factor 163/34=4.794 entre extremos (S19).\nP-SIST10 [MATEMATICO_CONOCIDO] La banda de baja frecuencia es relativamente estable ante pequeños desplazamientos por cota 2π|k|δ; no garantiza transferencia a alta frecuencia (S20).\n\nCT2 sin subir: B01 24→24; B02 17→17; B03 15→15; B04 21→21. No son probabilidades; comparación entre ramas no es una mejora. Nuevos N1 0, N2 0, N3 0.\n''')
# Typed O7 graph: 4 thematic branches and 20 results.
nodes=[{'id':'LARP_SISTERS','type':'research_goal','state':'closed','mode':'AB-R','source':'INFORME_S01_S20.md'}];edges=[]
for b in priors:
 nodes.append({'id':b,'type':'branch','state':'answered','mode':'AB-R','source':'INFORME_S01_S20.md'});edges.append({'source':'LARP_SISTERS','target':b,'relation':'branches_from'})
for c in cycles:
 nodes.append({'id':c['id'],'type':'mathematical_proposition','state':'answered','mode':'AB-R','source':'INFORME_S01_S20.md','grade':'0/3','external_replication':False});edges.append({'source':c['branch'],'target':c['id'],'relation':'tests'})
 if c['H']['duplicate_or_dependency']:edges.append({'source':c['H']['duplicate_or_dependency'],'target':c['id'],'relation':'related_to'})
(p/'GRAFO_O7.json').write_text(json.dumps({'schema':'AB_O7_TYPED_GRAPH','nodes':nodes,'edges':edges,'warning':'Answered does not imply independently novel theorem or successful replication'},ensure_ascii=False,indent=2))
(p/'CT2.json').write_text(json.dumps({'schema':'CT2_ORDINAL_NOT_PROBABILITY','by_branch':priors,'prior_vision_state':11,'no_aggregate_score':True},ensure_ascii=False,indent=2))
print('ledger',len(cycles),'valid',sum(c['E']['passed'] for c in cycles),'size', (p/'LEDGER_S01_S20.json').stat().st_size)
