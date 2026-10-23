# B05 — Resultados y decisión
Prereg commit f1160a52a26d76a01944feb0efa08cea13362844. Outcome MSE of finite population 0-1 risk; Δ=A−B (negative preferred). Datasets sklearn previously seen; nested 96 survey replicates within each of four split seeds. Numerical CI descriptive.
| ID | Mechanism | Delta | CI95 |
|---|---|---|---|
| C21 | PPS Horvitz-Thompson vs unweighted high-uncertainty sampling | -0.0301206 | [-0.0455192,-0.0147221] |
| C22 | Weighted population strata vs unweighted oversampling | -0.000273799 | [-0.000410007,-0.000137592] |
| C23 | AIPW vs unweighted mild PPS | -0.00172485 | [-0.00663927,+0.00318957] |
| C24 | HT vs Hajek under aggressive PPS | -0.000291269 | [-0.000493972,-0.0000885664] |
| C25 | Weighted high-risk allocation vs proportional allocation | -0.0000484238 | [-0.000171218,+0.0000743702] |
These are well known survey-sampling correction mechanisms, not original methodology. HT/AIPW means share same queried labels where policies and RNG coincide; when policies differ acquisitions are not identical, but budgets fixed. One outcome per seed (many nested draws) for descriptive interval. Multiple testing unadjusted; **no 2/3**.
**AB-DECIDE:** Do not add a sixth exploratory design variant family. Select five sufficiently discriminating claims from B01–B05 for a prospective new-seed recheck on previously seen datasets. This is an internal stability audit not external validation and must not be called a clean holdout.
