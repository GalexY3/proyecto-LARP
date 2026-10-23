# B03 — Resultados y decisión AB
Fuente precongelada: B03.tsv commit f284a327c6a5a77bf2ae93c37ab4723abb13460c; motor v2 hash 20e0c44... y parche PREVIO a B02. Intervention `flip_all`, `flip_confident`, `flip_uncertain`, `rare_error` applied to EVALUATION LABELS ONLY, not observed real-world changes; frozen X, model, q and queries.
| Ciclo | Comparación | Delta MSE A−B | Intervalo descriptivo por 4 seeds |
|--|--|--:|--|
| C11 | SRS vs proxy without labels, all labels reversed | -0.884382 | [-0.900598,-0.868166] |
| C12 | AIPW PPS vs SRS, shift confident | +0.0403528 | [+0.0186972,+0.0620084] |
| C13 | AIPW PPS vs SRS, shift uncertain | -0.00150707 | [-0.00283042,-0.000183724] |
| C14 | Strata risk proxy vs SRS, shift confident | -0.00327412 | [-0.00500136,-0.00154688] |
| C15 | Neyman from q vs proportional strat, rare errors | +0.000661271 | [+0.000268325,+0.00105422] |
C11 known non-identifiability, not a new principle. C12 loses: risk predictions trained on nominal validation are invalid in confident-label shift. C13 and C14 favor targeting and cover under selected generator; C15 contradicts Neyman assumption. All contrasts exploratory with tests deliberately defined using frozen model confidence, no outside causal effect.
**DRIFT 03 / AB-DECIDE:** move to estimation of preobservable subpopulation risk and equal-budget allocation. Neither auto-target uncertainty nor auto-target majority qualifies universally. More seeds of same shift generator will not establish external generality.
