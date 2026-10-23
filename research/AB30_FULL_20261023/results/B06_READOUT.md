# B06 — Five prospectively locked internal rechecks (C26–C30)
**Design frozen BEFORE computation:** GitHub commit `db0c0277c7ca17993f18a5bafc560915404aa866`; twelve new split seeds `107,109,113,127,131,137,139,149,151,157,163,167`, 120 paired label selections per split; comparisons and expected signs fixed in prereg/B06_FROZEN.md.

| ID | Claim from exploratory blocks | Δ=MSE(A)−MSE(B) | Cluster t CI95 | Result |
|---|---|---:|---|---|
| C26 | C02: proportional risk stratification improves SRS | +0.0000100603 | [-0.0000636518,+0.0000837725] | **NO SUPPORT**; direction not reproduced |
| C27 | C09: aggressive PPS improves AIPW vs mild PPS | -0.000244666 | [-0.000347061,-0.000142271] | Direction persists |
| C28 | C12: AIPW calibrated proxy FAILS against SRS when high-confidence labels change | +0.037096 | [+0.0319291,+0.0422629] | Expected **negative result persists** |
| C29 | C21: HT corrects biased purposive sampling vs naive | -0.0321985 | [-0.0402001,-0.0241968] | Direction persists |
| C30 | C24: HT beats self-normalized Hajek under targeted PPS | -0.000258583 | [-0.000429845,-0.0000873213] | Direction persists |

**Multiplicity:** five comparisons selected after B01–B05, ALL FIVE reported. Illustrative Holm-adjusted split-level p-values: C26 0.76948, C27 0.000806, C28 3.29×10^-8, C29 9.81×10^-6, C30 0.01359. This is NOT a familywise-confirmatory guarantee because train/test splits overlap across seeds and the datasets are previously exposed. Random survey repetitions within each split are nested, not independent populations.

**A–J:** A fixed finite population 0–1 risk; B selected rivals and null zero Δ; C frozen comparisons/seeds; D original engine + B02 patch, randomized sampling; E full per-draw results in downloadable ZIP; F bias/adaptive-selection/multiplicity audit; G **internal new-split recheck only, external replication ABSENT**; H retain C26 contradiction and conditional support for 4 others; I novelty 2/3 NO; J CLOSE 30 valid cycles, do not burn more seed quota to simulate replication.

**Limitations:** last block has 12 distinct *partitions*, not 12 independent datasets. Raw JSON per seed/draw archived locally and in user ZIP, not yet committed as raw files to GitHub. `CLEAN_CLONE_NOT_VERIFIED`.
