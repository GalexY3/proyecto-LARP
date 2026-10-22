# LARP drift AB30: source identity and design commitment

Date 2026-10-23, AB3.2.1+O1+O2. The source code under local working directory `src/engine.py` was frozen **before execution** with SHA256 `867e75309dfa81c8568bb2360d4cb4909560a338d7f16a587d03bba877f1deb6`. Its full bytes must later be uploaded and match this hash, otherwise reject all associated run records. This is a prior source hash, not yet a source-code GitHub upload.

Research pivot: away from MHU geometry to *goal-aware observation/sensor portfolio selection under noise covariance uncertainty and distribution shift*. Latent Gaussian model with 9 possible observation vectors in 2 latent dimensions, budget 3 sensors, exhaustive enumeration of 84 feasible subsets. Competitors: nominal full covariance, diagonal-only, covariance shrinkage, robust max-case, CVaR-like tail, random and best-in-hindsight oracle; posterior decoder calibrated to NOMINAL noise, test evaluated under shifted noise. This separates selection from retuning the decoder.

Train scenario orientations are (1,3,5) with 65% of exposure perturbation; evaluation orientations (0,2,4) under full perturbation. Training scenarios and test outcomes share the synthetic covariance generator, so NOT independent external evaluation or real hidden-out test. Guard against comparing to oracle as attainable. Real dataset branch, if reached, uses sklearn's diabetes or breast cancer with train/validation-derived selection only; the same public datasets may already have been exposed adaptively in project history.

Strong prior art: Kim (2024) greedy selection with correlated noise https://link.springer.com/article/10.1186/s13634-024-01127-1 ; Uciński (2020) D-opt sensors with correlation https://doi.org/10.1016/j.measurement.2020.107873 ; Krause et al. (2008) robust submodular observation selection https://www.jmlr.org/papers/v9/krause08b.html ; Goldfarb/Iyengar (2003) robust portfolio optimization https://doi.org/10.1287/moor.28.1.1.14260 . None of these claims 2/3 new.

Mandatory: prereg spec before each block, results and decisions before next, accumulate priors and failure records, do not pretend to have an external replication or new algorithm if merely testing known robust optimization.

Assumptions: Python 3.13; NumPy 2.3.5, SciPy 1.17.0, scikit-learn 1.8.0; deterministic seeds. Status: `SOURCE_SHA_PRECOMMITTED_CONTENT_NOT_YET_UPLOADED`.