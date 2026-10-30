# LARP trained routing L01–L20: reproduction and provenance

Original frozen research files in branch: `research/AB_ROUTING_20261030/learned_followup.py`, `research/AB_ROUTING_20261030/run_one_cell.py` and upstream `ab30_functional.py`; protocol in `research/AB_TRAINED_20261030/PREREG_L01_L20.md`. Resource-cap errata `ERRATA_RESOURCE_CAP.md` precedes full execution.

To replay on a machine with Python3.11+, NumPy, SciPy, PyTorch CPU, in a checked out copy of this branch, modify only output path; do not alter frozen source. The originally preregistered `run_one_cell.py` has a nonportable import path. Use the **post-outcome portable adapter** in the same directory as `learned_followup.py` and `ab30_functional.py`: `python research/AB_ROUTING_20261030/run_one_cell_portable.py 3011 low /tmp/run`. It changed only the import-path resolution and reproduces one complete local cell; it was **not** prospectively frozen, and no clean clone on another machine has been verified.

Results archive contains 10 original per-cell JSON, 10 exact replays with only `elapsed_sec` varying, predeclared protocol, audit, CSV summary, 20 A–J ledgers, reports, plots. All synthetic and no original NPZ native geometries. Source model parent `ab30_functional.py` is part of repo. Field seeds are divided into disjoint train/validation/test sets. 400 nodes x 6 edges all methods.
