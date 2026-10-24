# AB55 extraction/measurement contract — frozen before computing bulk outcomes

## Unit and estimand
Unit: one BugsInPy bug ID paired with its documented upstream fix commit. Outcomes are **repository change metadata**, not dynamic defect detection. Use only BugsInPy `projects/<project>/bugs/<id>/bug.info` and GitHub upstream `/repos/<owner>/<repo>/commits/<fixed_commit_id>`.

Normalize and record exact `buggy_commit_id, fixed_commit_id, python_version, test_file`, upstream fix message, `files[].filename, additions, deletions, changes`, and commit identities.

Define `test_cochange` = any changed path containing segments `test` or `tests` (or basename `test_...`), `source_cochange`=any changed Python implementation path not classified as test or doc; `code_change_lines` = sum of `changes` for `.py` implementation files excluding tests; `test_change_lines`=changes for `.py` tests. A fixed commit's test cochange is **not** proof that the corresponding test can be run under current Python, nor that a metamorphic relation is detectable.

For each case, the A–J ledger must separate: A unit/estimand; B source/test change hypothesis vs null; C independent fixed-commit metadata check; D instrumentation and upstream hash; E exact observed fields; F stronger rivals (historical environment, oracle exposure, selection); G not performed as external runtime replication; H prior; I originality 0–3 and CT2; J branch decision.

20 exposed source cases are discovery only; 30 subsequent IDs chosen before any `bug.info` or fix commit fetch in that cohort are held as a **locked descriptive source transfer set**. None constitutes independent execution.

## Named baseline and critique
Comparison to known bug/test metadata in BugsInPy is a strong **provenance baseline**. It is **not** a competent runtime differential or metamorphic testing baseline. Never report patch path change as “detected bug” or write a 20/20 bug-detection rate from successful metadata retrieval.

If GitHub returns a missing commit, access failure, partial truncated list, or unparseable file, write `NOT_VERIFIED`/null rather than filling values.

No one-sided significance claims; 20+30 cases not random from all bugs. Any association between fix size and presence of tests is descriptive under selection.

Next 5 AB intensive planning cycles will evaluate prospective matching environments, oracle-free test formulation, patch contamination controls, external replication, and novel cross-domain mechanism. Next 30 AB exploration cycles use metadata and software artifact provenance; if dynamic tests are unavailable, record them as documentary AB and **do not substitute** for runtime experiments.

**Novelty gate:** Existing BugsInPy papers and bug detection/fault localization methods are strong prior art. No 2/3 without executed independent evidence and specific novel discriminant.
