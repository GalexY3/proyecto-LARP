# CURRENT — LARP archival AB-P, 2026-10-30

- New grant: maximum 20 cycles, purpose archive/save in GitHub and audit integrity of LARP/MHU and derivatives. Completed: **20 AB-P provenance/integrity gates (A01–A20) after one documented repair**; 0 new AB-R scientific cycles, 0 new N1, N2 or N3. No quotas remaining from this 20-gate block, no implied further grant.
- First audit execution: 19/20 PASS, A17 invalid because auditor expected a flat JSON; historical M01-M18 check records live under `tests`. Errata `ERRATA_A17.md`. Fixed script committed before second run and second execution 20/20 PASS.
- Preserved: five exact original ZIP blobs, original complete ledgers M01-M18 and S01-S20, inspectable source/CSV/JSON of C01/C02/C04, reports, priors, per-asset hashes and portable archive verifier.
- Code freeze integrity: first source `b4d9c09`, first post-outcome errata `0f25294`, corrected source `bb5ab5b`, first failure results `2623061`.
- Confirmed local exact hash agreement of full Git reports and three restored raw vision JSONs; binary ZIP objects agreed with local Git blob hashes before being committed.
- External scientific confirmations: 0. CLEAN_CLONE_NOT_VERIFIED; only local clone-like portable script execution was performed. No MHU science CT2 changes. No changes to `main` or expensive CI. Scientific R5: stop interpreting archival successes as physical/AI validation.
