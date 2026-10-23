# G HOLDOUT UNSEAL CONTRACT — committed prior to ANY final-period execution
**Prerequisite complete:** source engine committed and Git SHA matched local; B01 initial + prospective no-lookahead amendment, B02–B05 preregs committed BEFORE their validation runs. ALL 30 validation results reported in B01..B05_READOUT files. No final-period (last 25%) score, graph or model choice has been observed or used for selection. This is the first and ONLY opening of final test.

The exact 30 hypotheses are fixed (6 independent historic observed data sources × 5 forecast mechanisms):
B01 persistence vs mean16 (C01–C06);
B02 mean4 vs mean16 (C07–C12);
B03 EWMA alpha=.3 vs mean4 (C13–C18);
B04 trend last8 vs persistence (C19–C24);
B05 adaptive weights last12 errors vs development-best fixed expert (C25–C30).
Same engine source Git blob 756d9e5568571c6985298719938c3ca5b717b793; SHA256 cfc0a2d1097df213a09d33188bce6a265a2bf68b7876bcca5ef4140c829daa23.

**G protocol:** Evaluate every fixed cycle on last 25% chrono window ONCE, using rolling one-step predictions and labels known only from strictly earlier dates. Save JSON for all 30 including negatives; no tuning, no repeated test-driven selection. Report unadjusted moving-block-bootstrap CI95 per cycle and descriptive sensitivity to multiplicity across the THIRTY comparisons; do not declare 30 independent hypotheses. Distinguish final chronological within-source consistency from independent outside-source confirmation; datasets are real but historically available. If results contradict validation, preserve contradiction. Source files unchanged from prereg. J final CLOSE or documented PIVOT after all G are audited.

**Epistemic label:** G_INTERNAL_CHRONOLOGICAL_HOLDOUT, not EXTERNALLY_CONFIRMED; novelty 2/3 not anticipated from standard forecasting baselines.
