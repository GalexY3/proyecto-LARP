"""Create audit ledger and typed hypothesis graph; outcomes from the mathematical proofs in report."""
from pathlib import Path
import json,hashlib,datetime
root=Path(__file__).parent
cases=[
('M01','finite union HU','closure','Var(sum) ≤ (Σ√Var)² = o(V)','Cauchy bound','Torquato 2018','none'),
('M02','converse fails','counterexample','random marking of HU lattice gives color Var Θ(V)','random labels independent','Jiao 2014; Kim/Torquato 2018','none'),
('M03','independent vacancies','formula','Var Np = p²Var N + p(1-p) EN; S_p(0)=1-p','p∈(0,1),ρ>0','Kim/Torquato 2018','none'),
('M04','full species removal','corollary','any nonempty finite subset of HU classes HU','complete classes removed; surviving modes still functionally limited','Jiao 2014','M01'),
('M05','spectral PSD union','identity','S_all=v*Hv, 0≤S_all≤(Σ√f_i S_i)²','normalization and spectral cross terms','Torquato 2018','none'),
('M06','relative phase','constructive','fixed individual spectra, joint |A|² cos²(φ/2)','may violate sensor packing','Wei 2010; AB08 LARP','M05'),
('M07','Lipschitz minimax','theorem','radius 1/(2n) midpoint samples; minimax sup-error L/(2n)','1D bounded Lip, exact point measurements','classical covering','none'),
('M08','isotropic Gaussian tie','theorem','tr(Cov(X|AX))=d−n for any full-rank n×d A','noiseless, isotropic, linear','classical Gaussian conditioning','none'),
('M09','slope endpoint design','counterexample','n=4 endpoints Fisher 1 vs grid .3125, ratio 3.2','repeated x allowed, independent noise','classical design of experiments','none'),
('M10','smooth bump indistinguishability','constructive','polynomial φ(x)=Π(x−p_i)² vanishes at any finite P','unbounded smooth function class beyond amplitude [0,1]','classical approximation','none'),
('M11','random-phase Fourier risk','identity','E err² = 1/2 Σ b_k²|A_P(k)|²','random independent phases','classical spectral quadrature','none'),
('M12','multimodal covariance risk','identity','E|a*ξ|²=a*Ca; signs of correlations change risk 0/2/4','Cov PSD, fixed a','classical covariance matrices','M05'),
('M13','five RGB filter rank','exact rank','rank F=3, not five independent spectral dimensions','linear pointwise filters, spatial data remain useful','linear algebra','none'),
('M14','data processing Bayes','theorem','all decisions on T(X) are decisions on X; inf-risk_X≤inf-risk_T','same cost, unrestricted classifiers','data processing inequality','none'),
('M15','independent expert bases','counterexample','hidden x and −x both decode x, unaligned average hides x','naive hidden-state fusion; output-level not ruled out','representation gauge symmetry','none'),
('M16','inverse variance experts','optimum','w_i ∝ σ_i^−2, var=1/Σσ_i^−2; two sample risk .8','unbiased same target, independent errors','BLUE/generalized least squares','none'),
('M17','spectral crossing','constructive','P={0,1/2} beats Q={0,1/4} at k=1 and loses at k=2','finite point sets; neither certified MHU','classical aliasing','M11'),
('M18','adversarial covariance','minimax identity','sup_{C PSD,diag σ²} a*Ca=(Σσ_i|a_i|)²','adversarial correlations, same variances','Cauchy-Schwarz PSD','M12')]
pre='1c27c5d2679f876cbda60987b1152246a72a75c9'
rows=[]
for k,title,kind,proof,limits,prior,dep in cases:
    rows.append({'id':k,'title':title,'mode':'AB-R-FORMAL','status':'ANALYTIC_AB_COMPLETED','counted_authorization_slot':True,
        'type':kind,'parent':('M04' if False else 'VISION_C04'),
        'A':{'claim':title,'estimand':'mathematical functional/risk defined in proof','truth_contract':'deductive conditional mathematical claim'},
        'B':{'rivals':'negation of frozen hypothesis, alternate signal and cost models','falsifier':limits},
        'C':{'test':'formal derivation or exact counterexample under explicit assumptions','primary_evidence':proof},
        'D':{'frozen_contract_sha_or_commit':pre,'source_code_freeze_status':'not applicable as mathematical proof; audit script authored after prereg'},
        'E':{'observation':'proof argument completed; no human data or numerical inference','result':proof},
        'F':{'adversarial_limit':limits,'prior_art':prior,'dependency':dep},
        'G':{'verification':'written proof plus targeted SymPy/NumPy sanity check','external_replication':'NONE','reviewer_independence':'NOT_ATTESTED'},
        'H':{'prior_update':'No universal advantage MHU; see report for claim-specific inference','new_original_discovery':False},
        'I':{'mathematical_status':'proved conditional to assumptions, internally reviewed','novelty':'known or elementary derivation','grade':'0/3','N1_new':0,'N2':0,'N3':0},
        'J':{'decision':'PROVED / AUDITED; no novel 2/3; pivot to covariance-aware conditional visual design','cost':'one distinct mathematical question; no training/GPU'},
        'proof_source':'INFORME_MHU_FORMAL.md#'+k.lower(),'numerical_audit_key':k})
ledger={'date':'2026-10-29','branch':'research/ab-mhu-formal-20261029','method':'AB3.2.1 O1-O7','prereg_commit':pre,
 'base_grant':20,'prior_executed':2,'formal_budget':18,'formal_questions_addressed':len(rows),
 'mathematical_external_validation':'NONE','original_novel_theorems_verified':0,'N1_new':0,'N2':0,'N3':0,
 'overlapping_theorems':{'M04':'corollary_of_M01','M02':'same_thinning_logic_M03','M17':'application_of_M11'},
 'note':'18 mathematical contracts addressed, not 18 independent scientific discoveries. Symbolic checks not formal proof assistant certification.',
 'cycles':rows}
(root/'LEDGER_M01_M18.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False))
nodes=[{'id':'LARP-VISION-MATH','type':'research_goal','mode':'AB-R','status':'answered','name':'Are MHU distributions universally better?','source':'INFORME_MHU_FORMAL.md'},
 {'id':'LARP-MULTIMODAL-COVARIANCE','type':'research_goal','mode':'AB-R','status':'proposed','name':'Under which signal covariances/costs can MHU help?', 'source':'INFORME_MHU_FORMAL.md'}]
edges=[]
for x in rows:
 nodes.append({'id':x['id'],'type':'theorem_question','mode':'AB-R','status':'answered','name':x['title'],'source':'INFORME_MHU_FORMAL.md'})
 edges.append({'source':'LARP-VISION-MATH','target':x['id'],'relation':'branches_from'})
 if x['F']['dependency']!='none': edges.append({'source':x['F']['dependency'],'target':x['id'],'relation':'supports'})
for q in ['M11','M12','M16','M18']:
 edges.append({'source':q,'target':'LARP-MULTIMODAL-COVARIANCE','relation':'supports'})
(root/'GRAFO_O7.json').write_text(json.dumps({'nodes':nodes,'edges':edges,'version':'2026-10-29'},indent=2,ensure_ascii=False))
print('ledger',len(rows),'graph',len(nodes),len(edges),'sha',hashlib.sha256((root/'LEDGER_M01_M18.json').read_bytes()).hexdigest())
