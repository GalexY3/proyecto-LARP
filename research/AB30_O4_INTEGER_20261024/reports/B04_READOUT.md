**AVISO DE INVALIDACIÓN:** Este informe histórico procede del motor v1 MAL ETIQUETADO Hamilton. Sus números han sido sustituidos por los 30 resultados R1 en [DICTAMEN_R1](DICTAMEN_R1.md) y [RESULTS_R1_30_ROUNDED.json](../results/RESULTS_R1_30_ROUNDED.json). Conservar solo para auditoría del error de instrumentación.

# B04 Q19–Q24 — guarded allocation under constructed stress
Prereg 295a2c1 before running. Four scoring conditions per source: original observed y plus each of three *synthetic, mean-centered, Gaussian within-stratum* volatility shocks (σ=2 standardized y), with policies seeing ONLY x proxy. Δ=max Var_A(guard)-max Var_B(exact proxy) across those four worlds; lower=guard better.
| ID source | E budgets10/14/18 | G budgets26/34 |
|---|---:|---:|
| Q19 Diabetes | −0.1379436 | −0.0543699 |
| Q20 Breast | −0.1808912 | −0.1005221 |
| Q21 Wine | 0 | +0.0002071 |
| Q22 Digits | −0.0044126 | −0.0098461 |
| Q23 Nile | −0.0184477 | −0.0164397 |
| Q24 Sunspots | +0.0116127 | +0.0060961 |
A worst-case finite-pop variance, not average observational loss; B rivals artificial generator making guard favorable, strong minimax optimizer untested; C paired same proxy/info/budgets, four scoring worlds pre-fixed; D target leakage prohibited; E four favorable two non; F ablation original y included but artificial shifts designed for audit, not observed natural changes; G larger budgets same six sources, strong sign persistence but not external; H guarded allocation may hedge proxy misspecification; I **1/3 portfolio candidate GUIDED-GUARD-02**, same local mechanism across sources counted once, well known robust/stratified principles and no 2/3; J move to robust minimax allocation, strongest direct rival. 
CT2 for line **12→19/100**; campaign N1=2 provisional, N2=N3=0.