# B02 Q07–Q12 — exact proxy allocation versus rounded Neyman (2026-10-24)
Precommit f38cbcc5. Δ = exact finite population variance on OBSERVED y for exact-proxy-optimum minus rounded proxy-Neyman; lower preferred.
| Cycle/source | E budgets 10/14/18 | G budgets 26/34 | Verdict |
|---|---:|---:|---|
| Q07 Diabetes | 0 | 0 | identical effective policy |
| Q08 Breast | +0.0044782 | +0.0023146 | exact proxy-optimal worse on actual y |
| Q09 Wine | 0 | 0 | identical |
| Q10 Digits | −0.0001411 | 0 | weak conditional improvement only |
| Q11 Nile | 0 | 0 | identical |
| Q12 Sunspots | 0 | 0 | identical |
A finite-pop true variance not proxy objective; B H1 exact-proxy optimum also optimizes y, nully false if proxy misaligned; C enumerate all integer triples with budget/caps; D exact optimizer by definition noninferior **on proxy objective** (verify code), raw source SHA locked; E six results; F strongest rival = post-hoc true-y oracle forbidden in actual policy and Census 2014 exact optimization prior art, so no novelty; G larger budgets same datasets, not independent; H refute naive belief proxy optimimization improves target; I valid conditional, classic proxy mismatch, 0/3 additional grade; J branch to randomized rounding rather than yet another static exact optimizer.
CT2 16→14/100; N1=1 (unchanged), N2=0, N3=0.
