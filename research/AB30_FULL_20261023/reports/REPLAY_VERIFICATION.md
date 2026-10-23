# Independent archive-extraction replay verification — 23-10-2026
The distributed `LARP_AB30_FULL_20261023.zip` (119 members, SHA256 e1617868cbae2c7cea4337ec2c776cc1372d51f43eb6b1b92487daa0405c5338) was extracted into a separate fresh directory **without reusing the original campaign working directory**.

- Archive integrity: `ZipFile.testzip() == None`.
- Source: `source/reconstruct_engine.py` recovered both historical engine versions with exact declared SHA256; reconstructed v2 was bit-identical to the distributed `engine.py`.
- Execution C03R from archived `prereg/B01_REPAIR.json` regenerated the original `results/C03R.json` with **exact identical SHA256**.
- Execution C26–C30 from archived `prereg/B06.json` on twelve 2026 campaign split seeds regenerated **all five original per-draw raw JSON files with identical SHA256**.
- Environment: same host installation of Python 3.13/sklearn 1.8.0/scipy 1.17.0/numpy 2.3.5, `OPENBLAS_NUM_THREADS=1`. Dependencies were **not installed from scratch** and no GitHub clean clone was executed. State `CLEAN_ARCHIVE_EXTRACTION_REPLAY_PARTIAL_VERIFIED`, **not** `CLEAN_CLONE_VERIFIED` and **not** replication using new independent observational data.

This is a reproducibility gate and integrity audit, not external confirmation or discovery 2/3.
