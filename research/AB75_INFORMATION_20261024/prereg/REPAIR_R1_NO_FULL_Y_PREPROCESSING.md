# INSTRUMENT AUDIT/REPAIR R1 — **before** any corrected AB75 replay (24 Oct 2026)

## Error detected after all 75 original outcomes
The v1/v2 engine used FULL finite-population response quantiles, mean and standard deviation to winsorize and standardize y **before** showing its transformed pilot labels to the adaptive policy. Thus the pilot values contained unavailable aggregate response information, violating the no-unpurchased-outcome-leakage assumption, even though the policy function did not otherwise inspect unpurchased y. The first 75 per-draw results are preserved as `results_invalid_population_scaling/`, and **cannot be cited as evidence for an actually deployable label-acquisition policy**.

## Prospective fixed replay R1
Replace the following exact code block in *both* source versions (v1: e20d7220103548b03aca7cc04eb42ea8c953453360574ec7e6e61a9dd3c969da; v2: 4e776e1002d5f026062809e15e38db4564f46c9ad9dae180ff17e8923b26b397):
```python
    p=np.quantile(yy,[0.01,0.99]); yy=np.clip(yy,*p)
    yy=(yy-yy.mean())/max(yy.std(),1e-10)
    yy=np.clip(yy,-3,3)
```
with the **data-independent-at-execution** per-source constants
```python
    fixed={'engel':(550.,250.),'fair':(.5,2.),'anes96':(.5,.5),
           'randhie':(3.,5.),'grunfeld':(75.,80.),'macrodata':(6.,2.)}
    center,scale=fixed[key]
    yy=np.arcsinh((yy-center)/scale)
```
Constants were CHOSEN POST-EXPOSURE, not blinded. They do NOT compute or use response moments at runtime, but the redesign is exploratory and cannot become independent confirmation by rerunning the same sources. The transformed estimand also changes from winsorized-zmean to source-fixed asinh-mean; never mix scores across engines.

**Source hashes frozen HERE before repaired execution:**
- R1 v3 for C01–C55: SHA256 `949a9e4497fce1818633674fbc8d289cf6acb2622daa2a59afd9115683162f96`, 7804 bytes.
- R1 v4 for C56–C75: SHA256 `1f82bd3b43853e8b7484f543e2aad86d947d398b6fb00e71e370a90be76a20ab`, 7905 bytes, same paid-refresh patch as v2.
Full source files included in final ZIP; upload to GitHub may occur retrospectively, distinguish hash prereg from remote source bytes.

**All 75 source-specific A–J contracts and previous frozen nulls, competitors, budgets and labels remain unchanged except for the explicit transformed estimand and source.** All 75 rerun with exactly same RNG seeds, E/G simulation counts and source rows. External confirmation absent; 2/3 and 3/3 disallowed from repair alone. No results had been computed with repaired sources when this document was committed.
