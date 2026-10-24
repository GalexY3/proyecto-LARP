# Archive trigger — no new empirical cycles

Snapshot source runs: R0 40109096869 (invalid for scientific bug-detection outcomes); R1 40109855339 (first repaired tests); R2 40110153479 (wheel and pytest-cov repairs).

This workflow copies files from the immutable GitHub Actions artifacts into `results_uploaded/R0|R1|R2/`, saves per-file SHA256, and commits them on the research branch using the GitHub Actions token. No rerun, no new holdout, no change to the 20 authorized unique bug IDs. Any failures to download/upload are recorded as archival failures, not scientific results.

Final manual audit is written separately. The R2 automatic classifications have at least two false/under classifications (C09 false-positive due missing fixture; C16 true error not captured by assertion heuristic) and are NOT a scientific final dictamen.
