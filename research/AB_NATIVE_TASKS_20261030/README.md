# Reproducibility — genuine N400 task-conditioned contrast

The user-operated Windows recovery created the private source branch `research/ab-r-native-export-20261030-053103` with six exact-hex JSONs and a `TRANSFER_MANIFEST.json`. Current research branch is based upon that branch, so all native files are inherited without being modified.

## Execute

From the root of a private checkout of `research/ab-r-native-functional-20261030` with **Node.js 18+**:

```powershell
node research/AB_NATIVE_TASKS_20261030/replay_node.js
```

The runner reads the six checked-in original native exports, re-evaluates `native_task_eval_v2.js` with no external dependencies, and requires strict JSON identity of all **156 individual records** and **52 aggregate cells** against `RESULTS_T01_T10_REPAIRED.json`. Also verifies that the 96 communication/Fourier records are identical to `RESULTS_T01_T10.json`. It does not silently repair any data or write files. Performance depends on Node runtime. **CLEAN_CLONE_NOT_VERIFIED** in this ChatGPT environment; exact replay has been independently performed twice in JS isolates via the connected source.

Files: `PREREG_T01_T10.md` (before first run), `native_task_eval.js` (original source), `RESULTS_T01_T10.json` (original), `ERRATA_E01_GP_LENGTHSCALE.md` (GP physical-scale repair), `native_task_eval_v2.js` (repaired source frozen before rerun), `RESULTS_T01_T10_REPAIRED.json` (156 outcomes), `AUDIT_T01_T10.json` (25 checks), `LEDGER_T01_T10_AJ.json`, `DICTAMEN_T01_T10.md`, `PRIORS_DELTA.md`, `CURRENT.md`, `GRAFO_O7.json`.

The Gaussian posterior risk is an **analytic model expectation** under chosen periodic spatial covariance and noise, not an empirical image reconstruction or GNN training. For the correction in ell and why these 5 tasks are post-exposure exploratory, read the errata. Three fixed geometry seeds are the only paired units.

Original Wei 2010 build on the user's Windows reported `BUILD_FAILED_LOG_SAVED`; inspect the local `wei-build.log` from the earlier recovery session for the exact diagnosis. Do not silently substitute PoissonDisk for Wei.
