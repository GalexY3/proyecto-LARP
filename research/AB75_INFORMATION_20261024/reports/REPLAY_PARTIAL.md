# Computational replay audit — AB75 R1, 2026-10-24

After packaging `LARP_AB75_20261024_COMPLETO.zip`, SHA256 `04ce6a444c07f2cf27f83c9a67a5b852330cf985190dfeb285b27b2db68e6d1b`, extracted its 426 files into a **fresh temporary directory** using Python ZipFile; no read from original working directory was used during replay.

Asserted exact SHA256 for the repaired R1 engines:
- v3 `949a9e4497fce1818633674fbc8d289cf6acb2622daa2a59afd9115683162f96`
- v4 `1f82bd3b43853e8b7484f543e2aad86d947d398b6fb00e71e370a90be76a20ab`

Executed five distinct cycle contracts **C05, C30, C56, C66, C75**, each with both E and G, using the source and prereg JSON **inside that extraction**. All **10 full per-draw JSON outputs matched the archived bytes exactly**, not merely their means or hashes. Audit instrument independently checked 312 pilot+stage2 integer label budgets and no-duplicate acquisition invariants, 30 counterfactual invariances to altering unobserved y while preserving pilot labels, and 8000 conditional-HT Monte Carlo draws on a separate small constructed population.

**Scope limitation:** partial reproducibility sample 10/150 R1 JSON outcomes; the other 140 have stored hashes/invariants but were NOT rerun from this separate extraction. Same host/env and installed dependencies; NO clean GitHub clone and NO new independent observational source, so NOT_EXTERNAL_REPLICATION and NOT CONFIRMATORY. The 150 invalid original pre-R1 outputs remain explicitly invalid.
