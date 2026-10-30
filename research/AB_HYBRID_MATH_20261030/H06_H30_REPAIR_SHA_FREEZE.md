# Pre-reexecution source identity freeze H06–H30
2026-10-30. Original source prereg had 1 instrument error in H18; errata commit `2c264eec47b6dd75197ee571b0beaf150e559117`, documented before any repair execution.

Only change: `(1+ks**2)**-2` → `(1+ks.astype(float)**2)**-2` to permit floating reciprocal powers. No outcome data, theory, thresholds, checks, seeds or tests changed.

**Repaired exact source SHA256: `27ff861886fadaa03718b9ac8b0037cf84edcfa06100be5282b6d8d2c09f81b6`**, bytes as subsequently verified. NO second run executed at the time of this commit. Source-body GitHub deposition remains pending due container transfer bridge expiry and must be reported as weaker O3 than full source freeze. Do not count the failed run as an extra cycle.
