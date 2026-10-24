# LARP AB75 — source identity and governance, 24 October 2026

User authorization: 30 AB cycles; if none credibly reaches 2/3, another 45. Branching/pivot/drift permitted. The 75 slots are a ceiling conditional on 2/3, but the 30+45 cycles are granted. Full A–J per cycle, no false 2/3.

**Pre-execution Python source SHA256** `e20d7220103548b03aca7cc04eb42ea8c953453360574ec7e6e61a9dd3c969da`, 7,645 bytes, file `src/engine.py` in downloadable evidence archive. Remote GitHub holds hash before all executions; the full script may be archived later, and doing so does not imply pre-run remote bytes. Version immutability: reject changed digest for any cycle.

Data: six **previously collected** statsmodels datasets (engel, fair, anes96, randhie, grunfeld, macrodata); RandHIE deterministic n=3500 subsample seed 818; response y winsorized 1%-99%, standardized to zero mean/unit SD, clipped [-3,3], all decisions only use x and legally acquired pilot labels. Three x strata by rank roughly [20%,30%,50%]. Estimand is their finite-population mean under documented transformation, not original untrimmed mean.

Design: 2 pilot labels per stratum, SRS without replacement from each stratum. Second-stage integer allocation is based on stage-one outcomes only (or cheap x); every arm uses total B=30 or B=48 labels, n_2≥1 per stratum. Second stage samples SRS uniformly from remaining units. B phase is **a budget sensitivity on the same observational source**, not an outside replication. Per-cycle fresh Monte Carlo acquisition draws, repeated within the same finite source, not independent studies.

Core estimators:
- Naive pooled stratum sample means (possibly biased when n2 is driven by pilot outcomes).
- Stage-conditional design estimator `(sum(y_pilot) + (N_h-n1)*mean(y_second))/N_h`, which is design-unbiased for fixed finite y under uniform stage-two sampling conditional on pilot, provided n2≥1 and y_pilot remains current.
- Stage-two-only estimator to probe pilot label staleness.
- Known-propensity IPW response correction for observed x-based MAR; propensity under outcome-dependent MNAR is an **inaccessible oracle** and is never claimed deployable.

Endpoints: MSE of estimates (primary); empirical signed bias (secondary); 95% bootstrap interval **of simulation draws** quantifies Monte Carlo uncertainty conditional on the fixed data and assumptions, **not** uncertainty across independent populations.
No fresh external source, deployment or independent replication.

Strong prior art pre-gate:
USGS Salehi et al. 2010 https://www.usgs.gov/publications/efficient-estimators-adaptive-stratified-sequential-sampling
Cook/Mishler/Ramdas 2024 https://proceedings.mlr.press/v236/cook24a.html
Survey missing-data and doubly robust literature https://www3.stat.sinica.edu.tw/sstest/oldpdf/A24n119.pdf
HT known design weights https://online.stat.psu.edu/stat506/Lesson03

Novelty grades: 0/3, 1/3 only for nonduplicated conditional operational finding, 2/3 only with novel discriminant and stronger baselines on independent data, 3/3 more. No grade inflation for reproducing a mathematical identity. Permanent registry `research/FINDINGS_1_3/LEDGER.json` in main currently contains 3 explicit audited findings (global historical pre-O4 total NOT_AUDITED).
CT2 initial 12/100 from prior campaign; CT2 is an ordinal informed confidence about a **specific line**, not a calibrated probability. Each experiment stores before/after/reason and pivot identity. Show final chronological CT2 plot.

**Important:** Source code bytes were frozen locally and hashed here before outcomes, but are not yet fully in GitHub. This is a known remote O3 archiving gap; the final report MUST distinguish source hash freeze from pre-run complete remote source. All block/spec contract records will be committed before runs. No retrospective claim to independent G.
