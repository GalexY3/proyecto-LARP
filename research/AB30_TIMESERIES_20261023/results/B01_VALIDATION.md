# B01 VALIDATION A–J (test still sealed)
Codes C01–C06. Chronological development [35%,50%], validation [50%,75%], FINAL TEST [75%,100%] not accessed. Each compares persistence with lag-16 mean, lower MAE preferred. Inference: 1499 circular-block bootstrap draws, approximate CI, not FWER corrected.
| C | series | val n | delta MAE | 95% interval | audit |
|---|---|---:|---:|---|---|
| 01 | Nile | 25 | +22.12750 | [-8.590,+47.073] | inconclusive, mean reversion possible |
| 02 | Sunspots | 77 | -11.07346 | [-15.300,-7.566] | persistence wins locally |
| 03 | CO2 | 571 | -1.47356 | [-1.609,-1.341] | mean16 fails rising trend |
| 04 | RealGDP log | 51 | -0.06050 | [-0.06960,-0.05147] | persistent level wins over long mean |
| 05 | ElNino flattened monthly | 183 | -0.90600 | [-1.141,-0.713] | long mean erases seasonality |
| 06 | Interest R | 27 | -0.01031 | [-0.01439,-0.00632] | persistence wins locally |
**A:** estimand paired one-step MAE across chronologically subsequent forecasts for separate real datasets. **B:** H1 persistence beats long, rivals rising trend, nonlinear reversals and seasonal cycle. **C:** fixed per-series time splits, baseline and bootstrap prereg. **D:** input anti-leak amendment prior to run; each predictor strictly past-only, data hashes recorded in JSON. **E:** validation above, raw per-cycle results in ZIP final. **F:** CO2 values ffill only, original Nile/sunspots tiny independent effective sample, no correction for multiple; macro log scale; ElNino flattened months. **G:** final independent chronology remains unopened; not yet claim confirmation. **H:** long mean often uncompetitive because lag makes it stale; this is known and confounded with trend. **I:** no novel theory, modest transport; compute straightforward. **J:** CONTINUE into lag-4 versus lag-16 to distinguish window effect from mere persistence.
