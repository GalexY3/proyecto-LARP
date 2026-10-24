# Instrument version v2, pre-B11 repair/extension (BEFORE B11–B14)

**v1 engine.py** SHA256 e20d7220103548b03aca7cc04eb42ea8c953453360574ec7e6e61a9dd3c969da, immutable for C01–C55. **v2 engine2.py** SHA256 4e776e1002d5f026062809e15e38db4564f46c9ad9dae180ff17e8923b26b397, 7,746 bytes. v2 will only be used for C56–C75.

Exact text substitutions on unchanged v1:
1. `nr=policy(py,gs,x,y,kind,B-3*n1)` → `nr=policy(py,gs,x,y,kind,B-3*n1*(2 if estimator=="refresh" else 1))`.
2. `est=evaluate(yc,y,gs,p1,s2,estimator,missing,rng,x)` → `est=evaluate(yc,yc if estimator=="refresh" else y,gs,p1,s2,"ht" if estimator=="refresh" else estimator,missing,rng,x)`.

The second phase labels are contemporaneous. First-stage labels are measured at time 0; only REFRESH pays another 3*n1 queries after the artificial shift and uses current y for pilot stratum values. This leaves fewer unique stage2 labels at fixed TOTAL label-action budget B. Source hash was locally calculated and frozen here **before** any v2 experiment, not afterwards. No B01–B10 results are changed or retroactively repaired; no post-hoc replacement of a failed comparator.

The MNAR propensity `P(response=1|ycurrent)` is defined by simulator and is inaccessible without y; calling it "oracle IPW" is compulsory. MAR response propensity depends on observable x and can be known to the simulator. Both are synthetic missingness, NOT natural response collection. The full editable v2 code will be included in ZIP and added to GitHub after runs, explicitly not claiming pre-run full source bytes.
