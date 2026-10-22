# AB30 novelty source lock (pre-execution)

Date: 2026-10-22. AB 3.2.1 + O1 + O2. GitHub pre-execution hash commitment.
Source file `src/experiment.py` (currently produced locally; to be incorporated intact in later commit).
SHA256 of exact source bytes: `df7e95fa9bb96c8d65b9634b5188dc9ea587d364f6257dcaa8ba8d7d6a42e443`.
Environment: Python 3.13.5; NumPy 2.3.5, SciPy 1.17.0, scikit-learn 1.8.0.
Main methods: 5 species x 12 points; periodic 2-D unit square; mode Ktrain = (1,0),(0,1),(1,1),(1,-1),(2,0),(0,2); modes Kout=(2,1),(1,2),(2,-1),(1,-2),(3,0),(0,3),(2,2),(2,-2),(3,1),(1,3). Different geometries: joint weighted Fourier optimization, subtype-only, union-only, same-type soft repulsion, typewise Sobol, typewise 3x4 periodic lattice, iid. Spectral optimizers use L-BFGS-B, max 65 iterations, identical initial Sobol points, class quotas. These are FINITE MODE spectral optimizers: cannot claim an asymptotic MHU certificate.
Important distinction: the committed hash freezes local code byte identity before experiments, but the SOURCE BYTES are not yet in GitHub. The subsequent GitHub source upload MUST match the above hash; cloning this commit alone is insufficient to reproduce. Avoid describing this as full code freeze before upload.

Scientific aim: contrast transferable functional gains under unknown cross-channel covariance, task shift, dropout and external tasks. A pattern designed to suppress a particular Fourier band does not show generality on that band. Every block will be frozen before running and deviations/repairs recorded with an explicit invalid attempt.
References: Jiao et al. Phys Rev E 89 022721 (2014); Li-Yi Wei Multi-Class Blue Noise Sampling (SIGGRAPH 2010). Wei's authentic C++ implementation has NOT been run; a soft repulsion substitute is not an equivalent baseline.
