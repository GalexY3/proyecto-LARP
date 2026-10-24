# REPAIR R1 — GitHub redirection was interpreted as a zero-file commit
Original X07–X12 FastAPI metadata measurements (zero source changes; zero test cochanges) are INVALID.
The historic BugsInPy project.info points to tiangolo/fastapi. Current GitHub API responds at that URL with a Moved Permanently JSON and no files. The initial code wrongly accepted response.files || [] without requiring a real commit object.
The current canonical upstream path is fastapi/fastapi. One current canonical commit was previewed, so R1 is prospective for the remaining files but the overall repair is after some exposure.
Frozen repair protocol:
1. Use upstream fastapi/fastapi. Retain historic URL as provenance with REDIRECTED_REPO.
2. Require API result.sha to equal the exact BugsInPy fixed_commit_id and result.files to be an array; never interpret a redirect or error payload as an empty patch.
3. Preserve original result JSON unchanged as INVALID_AFTER_INSTRUMENTATION_DEFECT.
4. Save a separate X07_X12_FASTAPI_R1.json after this commit, with code/test metrics and status REPAIRED_AFTER_EXPOSURE.
5. Missing commits receive NOT_VERIFIED, never a numeric zero.
These are documentary audits only, not dynamic execution, independent confirmation or evidence of original 2/3. Source ID and cases unchanged.
