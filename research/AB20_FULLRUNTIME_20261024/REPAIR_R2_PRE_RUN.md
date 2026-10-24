# R2 prospective REPAIR before further executions; 24-10-2026

R0 initial Github run 40109096869 INVALID for bug detection. R1 run **40109855339** completed (GitHub Actions status success means all results uploaded, NOT that twenty defects reproduced). R1 source `0e6eb231` archived before its launch, 20 official commands from BugsInPy and fixed-test overlay run on full upstream revisions. Local artifact inspection yielded:
- `tqdm` C01–C05: five `CANDIDATE_REPRODUCED_AUDIT_TRACE_REQUIRED`, buggy assertion/TypeError and fixed test passes on full repository in Python 3.6.15 Docker.
- Cookiecutter C12: one analogous candidate.
- Cookiecutter C09–C11: `pytest` test invocation failed with unrecognized `--cov` arguments specified by its historical `setup.cfg`, same both versions. Need install `pytest-cov`.
- PySnooper C06–C08, youtube-dl C13–C16 and black C17–C20: editable install fails on generation of metadata with `error: invalid command 'bdist_wheel'`. Need `wheel`, no skipping install and no claim of reproduction.
- 20 units total: six candidates, eleven install-blocked, three pytest-config blocked. The user authorized 20 units, not twenty successes. Repairs do NOT create new independent observations or second grant.

R2 is a **post-exposure instrumental repair** only:
1. Same frozen case list in `PREREG_COHORT_20.json` commit 806095e, same upstream SHA, same `run_test.sh` and fixed-test overlay algorithm.
2. Install `wheel==0.37.1` in per-project setup to permit editable installs. For cookiecutter install `pytest-cov==2.12.1` for inherited pytest ini options. No algorithmic tuning, outcome threshold changes, dataset selection, or test rewrites.
3. Code exact R2 must be committed to GitHub BEFORE triggering `R2_START.md`; retained R0+R1 raw archives unchanged. If errors persist log them. R2 is not new independent confirmation.
4. Scientifically defensible 'candidate' requires a real assertion/exception during the selected test in buggy + pass in fixed. No installation, no import, no collection counts. Audit trace to rule out environmental causes. All versions still depend on imperfect compatibility (3.6.15 instead of 3.6.9, Python3.8.18 vs 3.8.1/3.8.3, shared project toolchain, curated rather than independent sample).
5. CT2 stays 8/100 until independent novelty/replication; no N1/N2/N3 by mere regression reproduction.

Next project constraint: source code repo full, not hunk snippets; fixed's own test overlaid onto buggy per official BugsInPy. Dependency pins from corpus `requirements.txt` not exactly restored; this is an explicit reproducibility limit.
