# AB 3.2.1 — LARP PIVOT / L01–L20 — trained functional comparison

Date: 2026-10-30. Authorized: 20 AB-R cycles, user grants unconditional BRANCH/PIVOT without intermediate confirmation. Parent branch `research/ab-r-functional-routing-20261030` @ `0138a3070f0d152e556333fe8027d56f7ba0226f`. New branch `research/ab-r-native-trained-20261030`. State at creation: **BEFORE OUTCOMES**.

## Native retrieval gate and validity
Attempted to fetch six original binary LARP avian N400 geometries from `legacy/local_lab_20261022/artifacts/avian_v1/*.npz` through the connected GitHub API. Tree and file SHAs are visible; binary fetch returns `GitHub Fetch only accepts UTF-8 text`. HTTPS from the execution container cannot resolve github.com and no mounted copies of the native `.npz` have been found. **NATIVE_400_BENCHMARK_BLOCKED**. The original generator source `legacy/local_lab_20261022/src/larp/avian.py` is readable, but rerunning its nonconvex process would not establish exact historical identity. No native result may be claimed. This investigation therefore branches to **controlled functional proxies**; if full native inputs become available, test independently. R5 forbids calling these original avian geometries.

## Frozen instruments
Full prospective script: `research/AB_ROUTING_20261030/learned_followup.py` SHA256 `320bab4445e5e381b9378b681940ada89fe6df74086c4c0f9a1b8e51b2d7b031`. Its prior geometry dependency `research/AB_ROUTING_20261030/ab30_functional.py` SHA256 `cf187e6a367239dd46e2e25351158f5c1d8020423750987c4b8dc3fdcd9118d2`, already versioned in GitHub. Do not execute prior to the GitHub commit of this source **and** this protocol.

## A–J common research contract
A: finite 400-sensor torus, exact counts [163,85,68,50,34], directed 6-edge graph. Outcome: normalized mean square error predicting five-modal synthetic target at the nodes under specified perturbation. Independent statistical unit: **field realization**, with two conditional geometry seeds 3011,3023 as sensitivity analyses; 16 heldout field seeds. No external real imagery nor causal neural validation.
B: H1: task-supervised learned sparse graph routing (`*_learned`) outperforms locality-only and type-aware fixed routing under shift; null: gain fails to persist out of train distribution, or strong CVT/grid wins. H2: MHU finite spectral proxy does not dominate competent CVT or grid when both learn same decoder and get same information. Rivals: `grid_knn,cvt_knn,mhu_knn,grid_type,cvt_type,mhu_type,grid_learned,cvt_learned,mhu_learned`, all six outgoing edges and identical decoder architecture.
C: **20 factorial conditions** five spatial signal families × four test perturbations. These share data and are NOT twenty independent external replications. Train with 24 prechosen clean field seeds 50101–50124; validation 6 seeds 51101–51106; holdout test 16 seeds 52101–52116. NEVER tune on holdout. Geometry seeds 3011 and 3023 fixed. Prespecified primary pairings within each condition: (i) `mhu_learned` minus `cvt_learned`, (ii) `mhu_type` minus `cvt_type`, (iii) `mhu_learned` minus `mhu_type`, (iv) `mhu_type` minus `mhu_knn`, all on NMSE (negative=good). Provide worst rival, all methods, independent-field pooled mean, signs. No p-values confirmatory for shared synthetic world.
D: fixed neural MLP feature (15 inputs: five sensed intensities, five distances, five availability masks) with 24 hidden GELU units in two layers, Adam LR .006 weight decay .005 for 12 epochs, 8 batches each epoch, best checkpoint by VAL. Same network, 1+6 messages and same training sample budget for all methods. The learned router uses **target labels only from TRAIN to learn 6 neighbors** (correlation and class redundancy penalty), whereas the geometric routing has no supervised routing training. This is **unequal design computation**, explicitly measured and not hidden. Test fields and shifts are not used to learn routing.
E: one prospective execution and one clean-process repeat, keeping every row and negative outcome. Planned 2 geometry seeds × 5 contexts × 4 shifts × 9 methods × 16 heldout seeds = **5760** rows; 90 separately trained neural decoders. Contexts `low,high,correlated,anticorrelated,localized` (same synthetic generator family as previous AB30); shifts `clean,drop20,rare_drop40,noise15` at TEST only. No claim new source independent from earlier AB30.
F: adversarial audit common dependence on same generator, train/val/test field seeds distinct but not external data; fixed no recovery after dropout, finite spectral MHU proxy cannot claim original avian, CVT proxy not true native LOCAL, learned routing has privileged train targets and extra design cost, bilinear/FFT not involved, no learned attention over candidate edges with state updates. Any gain may be simply matching task covariance built into generator; disclose selection bias, overfit to geometry and budget.
G: two fresh-process runs **with same seeds** establish local software determinism only; external replication = NOT_DONE; no proof of asymptotic MHU. Clean cloned repo = NOT_VERIFIED. Compare all rows/weights summary and versions.
H: prior P-VIS graph type coverage can help, but previous AB30 CVT type outperformed MHU type in all 30 cells. Preserve negative prior and do not elevate 2/3 based on win over a weak comparator. Update only qualitatively; CT2 24/100 inherited conditional branch (ordinal not probability) unless independently justified.
I: score internal, external, information parity, design training cost, novelty, failure modes, accuracy and uncertainty independently. Scientific N1 only if new unique functional diagnostic not inherited; N2/N3 requires independent evidence, genuine published competitor, external replication.
J: STOP_LOCAL if no MHU-specific win vs strongest matched comparator, while using the remaining **already-authorized** cycles for nonrepetitive pivots. Do NOT spend cycles on cherry-picked additional seeds. If native geometry cannot be obtained, explicitly finish with non-native scope and unresolved gate. Do not merge main, trigger CI, or misstate results.

## Frozen 20 contrasts

| Cycle | Context | Perturbation | Estimand |
|---|---|---|---|
| L01 | low | clean | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L02 | low | drop20 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L03 | low | rare_drop40 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L04 | low | noise15 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L05 | high | clean | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L06 | high | drop20 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L07 | high | rare_drop40 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L08 | high | noise15 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L09 | correlated | clean | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L10 | correlated | drop20 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L11 | correlated | rare_drop40 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L12 | correlated | noise15 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L13 | anticorrelated | clean | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L14 | anticorrelated | drop20 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L15 | anticorrelated | rare_drop40 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L16 | anticorrelated | noise15 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L17 | localized | clean | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L18 | localized | drop20 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L19 | localized | rare_drop40 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
| L20 | localized | noise15 | Matched paired test NMSE of all 9 trained graph/geometry strategies, main comparisons preregistered above |
