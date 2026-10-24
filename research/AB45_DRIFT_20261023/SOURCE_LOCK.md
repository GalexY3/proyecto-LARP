# Pre-run engine commitment AB45
Date 2026-10-23. AB3.2.1 + O1 + O2 + O3 (DRIFT).
Exact SHA256 of runnable local source src/engine.py: f00acd99470bc7d17554bcc778f7cbc1fbacc8626e4eac1c4c8caa7b6b809df8.
Environment Python 3.13, numpy 2.3.5, scipy 1.17.0, sklearn 1.8.0.
Code execution and specs MUST match this hash. If engine changes, freeze a new commit before executing; preserve old logs. This is a hash commitment only; full source content is not yet in GitHub and must be archived after execution without claiming otherwise.
Data: local scikit-learn breast/wine/iris/digits samples; reused datasets from prior work, not external validation. Train normalization only train, logistic fixed C=0.5, holdout 40% stratified by seed. Target perturbations and label-only concept shifts constructed from the same holdout, never independent data.
Designed signals: input norm, model-weight projected input mean, output mean, uncertainty mean, subsample MMD; labels acquired under fixed equal budgets random/uncertainty/confident/stratified/mixed. Results measure rank/ROC/top4 alert, sampling estimator MSE/bias/variance/coverage, information-theoretic label-only impossibility.
All 45 tests exploratory; no 2/3 without new, independent real prospective stream and strong benchmarks WATCH / conditional conformal martingales / prediction-powered risk monitoring.
