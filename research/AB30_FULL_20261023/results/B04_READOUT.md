# B04 — Subgroup risk, observed results and repair
Preregit B04 commit 422dccc4da448029601720358d845da980830874, C20R prereg commit b5325993b22a2439f2aa17e779a42a947b863237. Predicted-class-0 subgroup chosen from model output **without true label access**. Four independent model splits, 96 repeated paired label selections per split. All CI exploratory.
| ID | Primary difference Δ=MSE(A)−MSE(B) | 95% descriptive interval | Status |
|--|--:|--|--|
| C16 group_SRS vs global_SRS, digits | -0.000719471 | [-0.003009147,+0.001570206] | INCONCLUSIVE |
| C17 subgroup strat vs subgroup SRS, digits | -0.00000214185 | [-0.000008958,+0.000004674] | INCONCLUSIVE |
| C18 group SRS vs unlabeled group proxy, wine | -0.00426623 | [-0.00903980,+0.000507346] | INCONCLUSIVE |
| C19 group strat vs global SRS, breast | -0.000761897 | [-0.00184885,+0.000325051] | INCONCLUSIVE |
| C20 subgroup SRS vs subgroup strat, iris | 0 EXACT | [0,0] | INVALID, NO VARIATION; NOT COUNTED |
| C20R PPS AIPW vs SRS under confident-label flip, iris | +0.0279784 | [+0.0199618,+0.0359950] | REFUTED WITHIN CONSTRUCTED LABEL SHIFT |
No causal fairness/generalization conclusion: subgroup defined by predicted class, not protected demographics. C20R uses a different estimand than C20; a new prereg was committed before execution. C20 original raw retained.
**AB-DECIDE DRIFT04:** sampling bias under targeted acquisitions becomes bottleneck, compare unbiased design-based correction with naive purposive inference and ratio/self-normalized alternatives. Results are not multiple independent studies across 4 seeds.
