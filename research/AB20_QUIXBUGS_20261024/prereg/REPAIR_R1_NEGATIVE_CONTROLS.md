# REPAIR R1 — Pre-rerun prospective commitment after inspecting exploratory E
At exploratory E (seeds 101,103,107), an audit of **corrected-reference negative controls** revealed instrument false positives: shallow sanity mistakenly required gcd to return a list and get_factors to return an integer; an invalid metamorphic law claimed that prefixing a common unique character increased the longest common *substring* length by exactly one. This is NOT necessarily true. Earlier E v1 results are INVALID for those strategies and preserved as raw artifact.
Source v1 SHA256 7999be6213a8223ecd904ee39cee5816a215589275ca735a6c3b4f91cc3a608a.
Source R1 SHA256 **db5dc62aa1c5fe2f08b3ac233582493808d75c95793ed87f6fdcbb05a70f8a57**, 16,524 bytes, frozen **BEFORE** re-executing any repaired E/G:
- remove get_factors from scalar-int sanity and include gcd, as dictated by corrected program return types.
- add get_factors list-of-integers sanity contract.
- replace false law LCS("#"+s,"#"+t) = LCS(s,t)+1 with valid reverse-invariance LCS(reverse(s),reverse(t)) = LCS(s,t) for longest common contiguous substring.
No changes to upstream defect implementations, exact reference one-line patches, names, sample cases, budgets, seeds, safe tracing or other 19 MR tests.
**Epistemic penalty:** E exploratory results were observed; R1 corrections were adaptively motivated, so rerun E is exploratory/post-exposure. The five G seeds were NOT opened before this lock, but they sample the same handwritten cases and benchmark; no independent external confirmation. **Do not conflate corrected-reference false positives with true defect detections.** All 20 programs rerun under R1 for comparability; source v1 and raw E_invalid_v1 remain in ZIP. Original prereg hypotheses endure unless falsified, no 2/3 claim.
