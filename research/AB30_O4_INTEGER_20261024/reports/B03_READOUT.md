# B03 Q13–Q18 — dependent stochastic rounding versus Hamilton integer allocation
Precommit 809504bc. Actual finite population variance A(randomized round expectation over 200 allocations)−B(deterministic rounding), fixed continuous 50/50 proxy/proportional target, same integer label budget.
| Dataset cycle | E10/14/18 | G26/34 |
|---|---:|---:|
| Diabetes Q13 | +0.0000854 | −0.0004679 |
| Breast Q14 | +0.0010641 | +0.0002676 |
| Wine Q15 | +0.0044995 | +0.0004466 |
| Digits Q16 | −0.0030194 | −0.0007640 |
| Nile Q17 | −0.0090726 | −0.0008807 |
| Sunspots Q18 | −0.0010674 | +0.0000897 |
A estimate exact mean finite-pop variance of randomized allocation; B H1 stochastic rounding best, H0 >=0 and strong deterministic control; C independent RNG draws of exact-budget allocation (dependent rounding unbiased on fractional target), true y only scoring; D allocations integer, n>0, sum budget; E mixed results; F no data shift here, rounding method already classical and 200 draws not independent worlds; G budget transfer same finite population yields sign flips; H no universal benefit; I 0/3 new grade, no 2/3; J DRIFT from rounding mechanism to robustness of fixed integer policies under unforeseen noise.
CT2 **14→12/100**; campaign N1=1, N2=N3=0.