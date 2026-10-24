# R1 execution authorization trigger, 24-10-2026

This commit triggers the R1 five-lane GitHub Actions workflow under O3. Upstream/source IDs and fixed test targets are immutable in `PREREG_COHORT_20.json`, commit `806095e`.
- Repair rationale frozen at commit `d4df992` in `REPAIR_R1_PRE_RUN.md`.
- Exact R1 runner frozen in GitHub commit `0e6eb231` at `run_full_runtime_r1.py`.
- Workflow amended at commit `5712433`; tests execute **after** all these commits.
- R0 in run 40109096869 remains archived as invalid detection evidence.
- R1 is post-exposure/repaired instrumentation, not independent replication or blind detection. Failures, timeouts and Python 3.6 Docker image issues must remain visible.
- Existing 20-cycle authorization applies; R1 replays and repairs do **not** increase the count of units beyond twenty.
