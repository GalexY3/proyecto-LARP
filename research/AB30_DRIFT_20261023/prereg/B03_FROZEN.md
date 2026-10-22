# Preregistro AB30 Drift B03: T13–T18
Fecha: 2026-10-23. PRE-EJECUCIÓN. AB 3.2.1/O1/O2.
SHA256 del manifiesto JSON local congelado: cfdcad9e86df8c4274f0aecab7151dba6a1d8d61a9847f294ab5e52df9ba1a46
SHA256 de motor Python precommitted: 867e75309dfa81c8568bb2360d4cb4909560a338d7f16a587d03bba877f1deb6
Todas las comparaciones usan semillas 1200..1223 inclusive, 9 posibles sensores, subconjuntos de 3, estimador calibrado con covarianza nominal, evaluación MSE pareada. Un intervalo que cruce cero es inconcluso. No es réplica externa.
- T13 nominal vs diagonal; group, rho=.95, shift=0, test=0: conocer correlación extrema supera aproximación diagonal.
- T14 shrink vs nominal; random, rho=.95, shift=.5, test=2: shrinkage ayuda con factores cambiantes.
- T15 cvar vs nominal; random, rho=.9, shift=.7, test=1: tail risk ayuda con shift fuerte.
- T16 robust vs cvar; signed, rho=.7, shift=.6, test=2: minimax supera CVaR bajo cambios de signo.
- T17 diagonal vs nominal; global, rho=.95, shift=0, test=0: simplificación diagonal evita sobreajuste en factor global.
- T18 nominal vs random; signed, rho=.9, shift=.4, test=2: la selección informada supera elección aleatoria en shift.
Estos contrastes se predefinen antes de ejecutarse como diagnóstico final de la familia sintética. Si fracasan, AB-DECIDE PIVOT a datos reales sin llenar más cupos con el mismo generador. Se registrarán también condiciones adversas.