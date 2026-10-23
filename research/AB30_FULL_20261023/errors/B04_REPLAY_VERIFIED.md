# B04 REPLAY verification — completed after errata
The corrected local B04.tsv now has exact Git blob SHA `4748f1513fa7c6564d450b70adbf2c2d309096b0`, identical to the ORIGINAL GitHub preregistration committed BEFORE the first execution.
Rebuilt B04.json now has `group=true` and nonnull `claim` in all C16–C20. Replayed every cycle on unchanged engine SHA256 `20e0c44f5bf813be9e6516fd2b3de00501c6034e028f7b8bfbc126eb912516fc`, identical seeds and draw counts.
**BIT-FOR-BIT raw JSON SHA256 identical for all five experiments**, including C20, to hashes recorded in `B04_LOCAL_SCHEMA_ERRATA.md`.
The fault was metadata parsing, not computation. C20 remains excluded due zero outcome variance, replaced prospectively by C20R. No contradictory result was hidden. Repaired manifest and original malformed TSV retained in local archival ZIP; remote source prereg was correct throughout.
