# Registro acumulativo permanente — seis hallazgos N1 auditados (24/10/2026)

La **fuente canónica** es [LARP/FINDINGS_1_3/LEDGER.json](../../FINDINGS_1_3/LEDGER.json); copia completa y literal en [N1_REGISTRO_COMPLETO_AUDITADO.json](N1_REGISTRO_COMPLETO_AUDITADO.json), incluyendo evidencia, procedencia, limitaciones, hipótesis rivales, falsadores, literatura y vínculos.

**Seis entradas N1 auditas, cero N2 y N3, cero N1 nuevos en AB65. No son seis nuevos descubrimientos publicados; ninguna confirmación externa.** No contabilizar nuevamente por datos, seeds o ciclos.

| ID | Entrada | Resultado preciso y límite causal |
|---|---|---|
| LARP-1-001 | ALIAS-01 | At small integer label budgets, many nominally different continuous allocation mixtures map to identical three-stratum allocation vectors; 81-90% redundant across observed sources on the preselected grid. |
| LARP-1-002 | PROXY-GAP-02 | Exact optimal integer allocation on an imperfect auxiliary variance proxy can worsen true outcome variance relative to a less exact Hamilton approximation; five of six observed populations in one study. |
| LARP-1-003 | COST-PILOT-03 | In six observed finite populations, a six-label pilot can improve allocation relative to a raw noisy pilot after 70% auxiliary-variance shrinkage, yet fails to improve full-budget population risk variance again… |
| LARP-1-004 | TEMPO-COST-04 | When pilot labels are acquired before an induced change in the outcome, reusing them as if contemporaneous can increase bias, but paying to refresh them may worsen the mean squared error at fixed total label-ac… |
| LARP-1-005 | FIXED-SITE-MODALITY-CONTROL | At identical fixed spatial sensor locations and equal five-modality quotas, lowering finite-wavenumber modality structure power can improve same-type coverage and synthetic signal reconstruction compared with r… |
| LARP-1-006 | QB-MR-06 | En veinte programas defectuosos escritos para desafíos Quixey y elegidos deliberadamente de QuixBugs, tres pares de pruebas metamórficas manuales detectaron fallos en 13/20, frente a comprobaciones superficiale… |

## Procedencia y posibilidades de falsación
### LARP-1-001 — ALIAS-01

- Procedencia: `research/ab30-o4-integer-20261024` / `research/AB30_O4_INTEGER_20261024/reports/DICTAMEN_R1.md`; 6 identificadores de experimento, que no son N1 independientes.
- Evidencia: Post-exposure R1 repaired experiments, exact enumeration.
- Competidores/antecedentes: https://www.census.gov/library/working-papers/2014/adrm/rrs2014-07.html.
- Limitaciones y evidencias contrarias: discretization already known; grid/budget/strata-dependent; not external replication.
- Falsador: Alternative integer budgets and constraints with more distinct treatment vectors.
- Confirmación independiente: **NO**. Duplicado de: ninguno registrado.
- Relaciones: LARP-1-002.

### LARP-1-002 — PROXY-GAP-02

- Procedencia: `research/ab30-o4-integer-20261024` / `research/AB30_O4_INTEGER_20261024/reports/DICTAMEN_R1.md`; 6 identificadores de experimento, que no son N1 independientes.
- Evidencia: Post-exposure R1 repaired finite population design variance comparisons.
- Competidores/antecedentes: https://www.bls.gov/osmr/research-papers/2026/st260020.htm.
- Limitaciones y evidencias contrarias: Goodhart/proxy mismatch known; dataset reuse; proxy selection and scoring not field validated; no external replication.
- Falsador: Proxy calibrated strongly predicts within-stratum target variance, reversing outcome.
- Confirmación independiente: **NO**. Duplicado de: ninguno registrado.
- Relaciones: LARP-1-001.

### LARP-1-003 — COST-PILOT-03

- Procedencia: `research/ab30-composition-pilot-20261024` / `research/AB30_COMPOSITION_20261024/README.md`; 18 identificadores de experimento, que no son N1 independientes.
- Evidencia: Three prospectively specified six-source AB blocks plus a POSTSELECTED competent pilot-reuse audit with 500 finite-population random trials per source and budget; G larger budgets on same data, not independent replication..
- Competidores/antecedentes: https://www.bls.gov/osmr/research-papers/2026/st260020.htm ; https://www.jstatsoft.org/article/view/v114i10.
- Limitaciones y evidencias contrarias: original pilot method excludes pilot labels from final estimate, a weak design; post-run reuse test is exploratory, not new field data; only six reused public populations; strong Bayesian and multi-wave design literature exists; no independent external replication or publication-level novelty.
- Falsador: A budget-parity, fully efficient multi-wave field implementation beats competent one-wave controls in a preregistered independent dataset under measured label costs.
- Confirmación independiente: **NO**. Duplicado de: ninguno registrado.
- Relaciones: LARP-1-001, LARP-1-002.

### LARP-1-004 — TEMPO-COST-04

- Procedencia: `research/ab75-information-20261024` / `research/AB75_INFORMATION_20261024/DICTAMEN_R1.md`; 10 identificadores de experimento, que no son N1 independientes.
- Evidencia: B10 finite-population MC: stale-pilot HT greater absolute bias in 5/5 exploratory sources E and 4/5 G while lower MSE than stage2-only; B11 buying another six labels to refresh stale pilot led to worse MSE in 5/5 E and G. B=30 and 48, same historical data, outcome shifts constructed post-pilot. R1 no-leakage fixed transformation selected after observing earlier invalid results..
- Competidores/antecedentes: https://www.usgs.gov/publications/efficient-estimators-adaptive-stratified-sequential-sampling ; https://proceedings.mlr.press/v236/cook24a.html ; https://www3.stat.sinica.edu.tw/sstest/oldpdf/A24n119.pdf.
- Limitaciones y evidencias contrarias: All label changes are artificially constructed; no naturally observed temporal drift; Public historical datasets reused, no outside prospective deployment; R1 repair after exposure, not blind confirmation; Conditional unbiasedness and missing-label methods predate study; The cost tradeoff overlaps COST-PILOT-03, but temporal validity is a distinct operational failure mode; No field measurements of real labels and price; No claim of a new statistical theorem.
- Falsador: A preregistered real-time independent stream finds refreshed pilot labels improve net risk estimation enough to offset measured reacquisition cost, or there is no temporal bias in production outcome under detected drift..
- Confirmación independiente: **NO**. Duplicado de: ninguno registrado.
- Relaciones: LARP-1-001, LARP-1-002, LARP-1-003.

### LARP-1-005 — FIXED-SITE-MODALITY-CONTROL

- Procedencia: `research/ab30-fixed-site-multicolor-20261024` / `research/AB30_FIXED_SITE_20261024/reports/DICTAMEN.md`; 30 identificadores de experimento, que no son N1 independientes.
- Evidencia: Exact source and 30 A-D contracts frozen in GitHub before execution, 4 E+8 G synthetic layout seeds per task, five families including fixed type-specific modes, farthest-first stronger baseline and postselected public-image audit. All 30 raw per-seed JSON and 83k-character A-J report in archived ZIP..
- Competidores/antecedentes: https://www.liyiwei.org/papers/noise-sig10/ ; https://doi.org/10.1145/2487228.2487233 ; https://doi.org/10.1103/PhysRevE.89.022721.
- Limitaciones y evidencias contrarias: Blue noise for multiple classes and imaging sensors already published in SIGGRAPH 2010; Finite low-frequency S(k) not certificate of asymptotic multihyperuniformity; All 30 initial hypotheses use correlated artificial field/geometry generators; Strong farthest-first control wins most coverage, Fourier and OOD comparisons; Six public-image audit sources tested after seeing synthetic data, not preregistered independent validation; Four E and eight G seeds too few for general power, heavy overlapping tests; No cost parity/optimization effort control against published multicolor algorithms.
- Falsador: A prospective, independently acquired multisensor dataset with reliable measured modalities shows a consistent, predeclared A-vs-farthest reconstruction advantage, or failures of finite low-k reduction are shown to be a code artifact..
- Confirmación independiente: **NO**. Duplicado de: ninguno registrado.
- Relaciones: LARP-1-001, LARP-1-002, LARP-1-003, LARP-1-004.

### LARP-1-006 — QB-MR-06

- Procedencia: `research/ab20-quixbugs-20261024` / `research/AB20_QUIXBUGS_20261024/reports/DICTAMEN.md`; 20 identificadores de experimento, que no son N1 independientes.
- Evidencia: 20 preselected external human-crafted Quixey Challenge algorithms, E 3 seeds and G 5 seeds each drawn from a fixed hand-crafted pool of 12 cases per program. Program-level M>S difference +5/20, exact bilateral paired p=0.0625 (exploratory), corrected negative controls zero FP in 480 program-seed-method triples. Source R1 repair committed before replay after seeing invalid E results; 40 E/G JSONs reproduced byte-for-byte in same environment..
- Competidores/antecedentes: https://doi.org/10.1145/3656340 ; https://doi.org/10.1016/j.infsof.2024.107528 ; https://www.nist.gov/publications/metamorphic-testing-cybersecurity.
- Limitaciones y evidencias contrarias: QuixBugs are toy challenges with intentionally inserted defects, NOT production bugs; case inputs and metamorphic relations hand-built with knowledge of the algorithmic contract and likely defect type; not blind; baseline sanity checks shallow and not a competent Hypothesis/industry fuzzing suite; differential reference had unequal privileged access and additional queries; not equal total information budget; E and G reuse same twelve inputs/program, not external confirmation; first E had faulty sanity types in gcd/get_factors and invalid LCS relation; R1 repaired after E exposure and archived; paired two-sided exact 0.0625 on deliberately selected 20 programs, no population-level novelty inference; meta underdetects 7/20 detected by repaired reference; metamorphic testing and MR synthesis already widely published.
- Falsador: On truly blind defect cases from independent production repositories and equal total test cost versus strong contemporary property-testing baselines, program-specific metamorphic testing does not improve credible detection or exhibits unacceptable false-positive rates.
- Confirmación independiente: **NO**. Duplicado de: ninguno registrado.
- Relaciones: LARP-1-002, LARP-1-003, LARP-1-004.


## Histórico pendiente de reconciliación (no sumar aún)
Los dictámenes originales BR30, AB08, AB30 LIBRE y las distintas campañas AB45 describen resultados y algunos emplean «novedad 1/3». **El total histórico previo es NOT_AUDITED**, por lo que estos resultados son **candidatos por auditar**: se debe determinar fuente primaria, independencia, duplicado respecto a estas seis entradas, originalidad y tipo de réplica. No inferir un número total sin examinar las ramas y ZIP de origen. No sobrescribir entradas N1 existentes ni el ledger de priors al fusionar.

## Nuevos ensayos AB65
Veinte reanálisis de las trazas R2 (post-exposición), quince métodos × series ambientales, quince económicos y quince condiciones simuladas Wright–Fisher: **N1 campaña = 0, N2 = 0, N3 = 0**. El objetivo 2/3 continúa sin acreditar. Las tres disciplinas constituyen tres pivotes D4–D5, no 45 pivotes distintos.

**Regla O6:** Ante evidencia posterior, añadir un hallazgo solo si es distinto, con procedencia, falsador y limitaciones; registrar confirmaciones y refutaciones sin borrar versiones anteriores.
