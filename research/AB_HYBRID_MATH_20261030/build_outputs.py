from pathlib import Path
import json,hashlib
p=Path('/mnt/data/LARP_AB_HYBRID_20261030')
r=json.loads((p/'CHECKS_H01_H05.json').read_text())
notes=[
('H01','CVT versus spectral aliasing','quantization versus Fourier resonance on alternating even-n torus','Regular grid minimizes quantization; hybrid with spectral term can leave grid','n=8 ε=0,1/128,1/32; exact gap-power identities','Q=1/(12n²)+ε²; S_n=cos²(2πnε); λ<4π²n² w destabilizes grid','Known convex quantization and Fourier aliasing, only a conditional extension of S08/S09','Maintain task-specific spectral/coverage tradeoff','Investigate 2D band priorities after strong controls'),
('H02','fixed-quota concentration covariance','randomly relabel fixed coordinates with n_c quotas','Independent colors versus hypergeometric negative correlations','N=4 quotas 2,1,1; 12 colorings','C_cd=N/(N−1)(n_c δ_cd−n_c n_d/N)(1−|Z|²/N²)','Bhatia-Thornton/partial spectral structure; extension of S17','Need full concentration cross spectrum as null','Test label effect holding X and physical radii fixed'),
('H03','robust Fourier minimax','two samples, unknown mix of Fourier k=1 or k=2','v2-like inverse-square prior versus minimax spectral risk','symbolic minimax x∈[0,1]','Min max(S1,S2)=1/4 at Δ=1/3; v2 weight optimum Δ=1/2 worst-case1','Only two points, two modes, not a trained v2 network; S13 antecedent','Unknown frequency spectrum requires robust family of priors','Optimize risk under credible uncertainty set and test real spectra'),
('H04','local modality coverage','fixed quota five types, random 6-neighbor sample without replacement','high heterotypic edge fraction does not imply complete five-type availability','exact inclusion-exclusion vs 6=2+1+1+1+1 hypergeometric composition','P(all five types)=0.05773846225940983 weighted by focal class','Random labels not actual geometric kNN/learned router; general hypergeometric identity','Degree-6 random routing is a weak baseline for specialist cooperation','Compare label-aware routing to random/expander at same edge/FLOPs budget'),
('H05','coset incompatibility','1D N12 grid union, class quotas 6,4,2','each n_c|N insufficient for simultaneous subgrid optimality','enumerate 2x3 possible residues','q6=2 and q4=3 coprime ⇒ every pair overlaps on 2 sites','Circle-specific CRT and regular sublattices; extends S07','Test coset intersection constraints before requesting exact species optima','Quantify best feasible relaxed multi-class coverage for unequal quotas')]
checks={x['id']:x for x in r['checks']}
cycles=[]
for v in notes:
 id,title,estimand,rival,design,observed,limits,prior,next_=v
 cycles.append({
 'id':id,'mode':'AB-R','state':'RUN_VALID_DEDUCTIVE','grade_0_3':0,
 'A':{'question':title,'estimand':estimand,'unit':'finite geometric configuration under stated mathematical assumptions','external_population':'none'},
 'B':{'rival':rival,'null':'no claimed universal superiority of MHU; negation/counterexamples in frozen contract'},
 'C':{'discriminant':design,'registered_hypothesis':'research/AB_HYBRID_MATH_20261030/PREREG_H01_H05.md'},
 'D':{'prereg_commit':'12083759d28527968d75e7879568315793c44fad','frozen_code_commit':'3738712ff153307fa0683a3e6322fcec69c2065c','code_git_blob':'4e42be1b22095ea88767e0fb00abfb865b85ceb9','code_sha256':'5e6487a901111d346a7859633afbfac1d7ac5c5d3868d4d3337f744e1f7e2086','frozen_before_outcomes':True},
 'E':{'executed':True,'result':observed,'test_evidence':checks[id]['evidence'],'test_passed':checks[id]['pass']},
 'F':{'adversarial_limits':limits},
 'G':{'local_independent_process_replay':'exact_byte_match','external_independent_replication':False,'mechanized_proof':False},
 'H':{'prior_revision':prior,'n1_new_unique':False,'n2_new':False,'n3_new':False},
 'I':{'validity':'conditional mathematical derivation plus finite/symbolic checks','original_scientific_discovery':False,'ct2_change':0},
 'J':{'decision':'CLOSE_FORMAL','next_evidence':next_,'r5':'do not repeat numerical checks as independent confirmation'}
 })
out={'schema':'AB_3_2_1_O1_O7','campaign':'LARP-AB-R-HYBRID-20261030','grant':30,'formal_valid':5,'experimental_valid':0,'invalid':0,'planning':0,'remaining':25,
 'preregistered_commit':'12083759d28527968d75e7879568315793c44fad',
 'code_frozen_commit':'3738712ff153307fa0683a3e6322fcec69c2065c',
 'checks_json_sha256':hashlib.sha256((p/'CHECKS_H01_H05.json').read_bytes()).hexdigest(),
 'N1_new_unique':0,'N2_new':0,'N3_new':0,'scope':'five mathematical questions and five diagnostic tests, not five scientific discoveries','cycles':cycles}
(p/'LEDGER_H01_H05.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(p/'PRIORS_DELTA_H01_H05.md').write_text('''# Priors actualizados — H01–H05 (append-only, 2026-10-30)

- **P-HYBRID-01 / CVT vs alias:** en una familia 1D exacta, eliminar resonancia exige sacrificar cuantización; garantía condicional, no efecto neuronal. Extiende S08–S09 sin duplicar N1.
- **P-HYBRID-02 / especies condicionadas:** una matriz de concentración bajo cuotas fijas tiene correlaciones negativas intrínsecas. No usar cinco tests espectrales como réplicas independientes ni asumir independencia de marcas. Extiende S17; falsador: matriz empírica bajo permutación con cuotas y X fijos que viole el nulo.
- **P-HYBRID-03 / MHU-v2 robusto:** un prior de señal 1/k² puede diferir fuertemente de riesgo minimax. No declarar la distribución v2 superior si no se conoce banda/covarianza. Extiende S13; falsador: pérdidas reales alineadas con espectro con ratio prior correctamente especificado.
- **P-HYBRID-04 / grafo multiespecialista:** seis vecinos de composición aleatoria cubren las cinco clases con probabilidad 5,773846%. La mezcla media no garantiza acceso completo. No adjudicar la distribución kNN real a este control nulo. Extiende S16.
- **P-HYBRID-05 / subredes intercaladas:** que cada cuota divida el total no es suficiente para compatibilidad conjunta. Las intersecciones forzosas de cosets impiden exactitud simultánea en N12 cuotas 6+4+2. Extiende S07.

**Nivel:** 0/3 original en los cinco casos; 0 N1 únicos nuevos, 0 N2, 0 N3. Ninguna elevación CT2 por resultados construidos. Mantener CT2 rama matemática condicional (referencia histórica 24/100, ordinal), sin comparación numérica nueva con Wei o datos. R5: no repetir pruebas de estas identidades; gastar futuros ciclos solo en nuevos mecanismos distinguibles.
''')
(p/'CURRENT.md').write_text('''# CURRENT · LARP AB-R Hybrids (2026-10-30)

Granted **30** free AB-R cycles, H01–H05 now **5 formal cycles completed** with explicit A–J, 0 invalid, 0 planning counted, **25 still authorized**. New N1 0, N2 0, N3 0. Stop re-testing identities by extra seeds; pivot when evidence improves. Current branch `research/ab-r-mhu-hybrids-20261030`; parent `research/ab-archive-audit-20261030` HEAD `5c1f00dab72a4c744b32a2a64efd298f9b24c8a9`. No merge into main, no CI.

Frozen prereg commit **12083759d28527968d75e7879568315793c44fad**, full source frozen commit **3738712ff153307fa0683a3e6322fcec69c2065c**, source Git blob **4e42be1b22095ea88767e0fb00abfb865b85ceb9**, SHA256 **5e6487a901111d346a7859633afbfac1d7ac5c5d3868d4d3337f744e1f7e2086**. 5/5 verified, exact local independent-process replay byte-identical JSON SHA256 **57a86c7774be32ef3ad732721eb75f3ac7d6f803abd549352dea1142cde35f7a**. CLEAN_CLONE_NOT_VERIFIED, no external proof assistant or external scientific replication.

5 exact conditioned mathematical insights: H01 CVT-vs-alias Pareto boundary; H02 cross-class null covariance fixed quotas; H03 mismatch MHU-v2 weighted spectral criterion vs minimax; H04 exact six-edge all-five-specialist availability 5.773846%; H05 gcd/coset obstruction beyond divisibility. All are based on known mathematics and project-specific derivations, no proven novel 2/3. Historical CT2 24/100 for conditioned mathematical branch not adjusted for quantity.

Next direction may branch freely within the **25 already authorized**; no need to re-request permission. Prior art: Wei 2010, Krause JMLR 2008, Bhatia–Thornton partial factors and LARP S01–S20. The real test of computational value requires functional/independent data and strong matching.
''')
(p/'SOURCES.json').write_text(json.dumps({'sources':[
 {'id':'SRC-H01','kind':'internal_original','url':'https://github.com/GalexY3/proyecto-LARP/blob/research/ab-archive-audit-20261030/research/AB_MHU_SISTERS_20261030/INFORME_S01_S20.md','relevance':'S07-S17 prior derived geometry and Fourier cases'},
 {'id':'SRC-H02','kind':'published_prior_art','url':'https://journals.iucr.org/j/issues/2021/01/00/gj5253/index.html','relevance':'Bhatia-Thornton and partial concentration structure factors, not novel claim'},
 {'id':'SRC-H03','kind':'published_prior_art','url':'https://www.liyiwei.org/papers/noise-sig10/','relevance':'2010 multi-class blue-noise competitor and independent prior art'},
 {'id':'SRC-H04','kind':'published_prior_art','url':'https://jmlr.org/papers/v9/krause08a.html','relevance':'strong submodular/data-aware sensor placement comparator'},
 {'id':'SRC-H05','kind':'original_repository','url':'https://github.com/GalexY3/proyecto-LARP','relevance':'LARP original 400 nodes count quotas and geometry models'}
 ],'new_original_human_data':False,'license_acceptance':False},ensure_ascii=False,indent=2)+'\n')
print('files generated',[(x.name,x.stat().st_size) for x in p.glob('*') if x.is_file()])
