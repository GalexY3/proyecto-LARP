# Eight cumulative priors — LARP AB30 FULL, 23 October 2026

These are appended to, not substitutes for, historical LARP priors. All evidence is exploratory, no numerical Bayesian posterior is invented, no original 2/3 discovery is declared.

**FULL30-P01: Sampling to learn versus sampling to estimate are distinct.** C01, C21, C29 show deterministic uncertainty-tail labeling biases unweighted population risk estimates. Counterevidence/limit: no retraining experiment was run, so no claim about learning superiority. Classic survey inference and Imberg et al. 2020 already discuss this.

**FULL30-P02: Proportional stratification does not guarantee general improvement.** C02 showed ΔMSE -0.000134; C26 new-split recheck showed +0.0000101 with CI across zero, C03R inconclusive. Falsifier: independent new-domain preregistration with enough cluster units. Status: NOT_GENERALIZED.

**FULL30-P03: AIPW depends for efficiency, not design unbiasedness, on proxy quality.** C08 artificially inverted proxy caused MSE ~0.01018 versus ~0.000123 for constant proxy. C12 and C28 show failure under constructed high-confidence label shifts. Counterpoint: with correct inclusion probabilities, AIPW remains unbiased conditional on fixed full losses even if q is wrong; severe increase is predominantly finite-sample variance. Status: KNOWN_THEORY_PLUS_CONDITIONAL_RESULT.

**FULL30-P04: Aggressive PPS may outperform mild targeting when the proxy remains informative.** C09 and its C27 internal recheck favor high focus in Wine; C10 HT comparison inconclusive; C12/C28 show limitations under shifted errors. Next: prospective stream, observed label costs. Status: TASK_CONDITIONAL.

**FULL30-P05: HT and population poststratification are strong survey baseline controls.** C21/C29 demonstrate correction over naive means, C22 over unweighted strata and C24/C30 over Hajek under these distributions. Cannot claim HT universally minimum-MSE. Status: CLASSIC_SURVEY_PRINCIPLE.

**FULL30-P06: Predicted-class subgroup audits require variation in target losses.** C16–C19 inconclusive and C20 all-zero loss invalid; C20R reverses augmentation ranking under a constructed shift. Predicted classes are not demographic protected groups. Status: NOT_VALIDATED.

**FULL30-P07: Audit repairs do not prove AB better than conventional science.** C03 equivalent allocation invalid; C20 null outcome invalid; B04 local TSV schema malformed but rereplay produced five identical raw-output SHA256s after matching GitHub original. Operational instrument success, no end-to-end superiority claim.

**FULL30-P08: New splits of an exposed dataset are not independent external replication.** Five selected rechecks C26–C30: four directions persist, C26 not; Holm p-values descriptive under overlapping split dependence. Falsifier: untouched time-ordered external data and professional PPRM/sequential baselines. Status: INTERNAL_CONSISTENCY_ONLY.

Refs: https://proceedings.mlr.press/v108/imberg20a.html ; https://proceedings.mlr.press/v306/zhang26g.html
