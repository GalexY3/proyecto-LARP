# ERRATA-E01 — GP periodic physical scale mismatch, after first outcome
Date 2026-10-30.

In frozen source `native_task_eval.js` (commit 8781b77d2068e45a5e792a63e67f453838e64210), the periodic kernel was `exp(-2*L²/ell² * [sin²(pi dx/L)+sin²(pi dy/L)])`. Small displacement d gives `exp(-2*pi²*d²/ell²)`, therefore its Euclidean near-zero correlation length is **ell/(2*pi)**, not ell. This is a semantic mismatch to prospective T01–T05, which refer to a physical lengthscale ell in native length units.

The source produced 156 rows, in commit 1d85324e68fead5739a6caf1a343a48388044f06. All results are immutable historical audit evidence. **T01–T05 from this first execution are INVALID for physical-lengthscale inference** (but not algebraically wrong for the old, much shorter kernel). T06–T10 unaffected. Replacing the kernel with `exp(-L²/(2*pi²*ell²) * [sin²(...)+sin²(...)])` gives `exp(-d²/(2*ell²))` locally. The corrected full source must be committed with a new hash BEFORE observing repaired outcomes; retain original and this errata, do not replace original result file or treat repaired result as blind independent replication.

No source N400 coordinates, quotas, controls, CVT optimization, routing, Fourier, sensors, evaluation sites, seeds or ell values change. Mark repaired T01–T05 POST_EXPOSURE_REPAIR. Do not elevate CT2 or grade originality. Count historical invalid analytical attempts separately in the ledger.
