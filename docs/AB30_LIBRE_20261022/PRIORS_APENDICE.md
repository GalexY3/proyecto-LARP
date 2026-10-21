# Ledger acumulativo de priors de LARP — apéndice BR30 libre (no borrar entradas anteriores)

| ID | Hallazgo/Hipótesis | A favor | En contra o límite | Estado |
|---|---|---|---|---|
| BR30-F01 | MHU penaliza eficazmente fluctuación espectral finita de conjunto y cinco tipos | C02-C03, C21, fuente original | Estaba definido como objetivo; no novedad asintótica | VERIFICADO FINITO |
| BR30-F02 | MHU ofrece cuadratura superior a alternativas competentes | C24 frente LOCAL/CVT/Sobol | Retícula exacta en banda baja; Sobol mejor en varias funciones no periódicas | REFUTADA UNIVERSALIDAD |
| BR30-F03 | Una retícula sin aliasing domina MHU | C06 integrales no resonantes exactas | C15 encuentra resonancia con S=1 | REFUTADA UNIVERSALIDAD |
| BR30-F04 | Supresión MHU persiste fuera de banda | C09/C10 parecían favorables | C11 revela fuga, C12 encuentra LOCAL mejor fuera del corte | REPARADA: NO VALIDADO |
| BR30-F05 | Cada especie HU podría producir unión no HU bajo fracciones estables | Premisa histórica | C22 demuestra desigualdad triangular: imposible bajo sus hipótesis | RECHAZADA COMO PRINCIPIO |
| BR30-F06 | Coordinación de fases entre especies añade supresión finita de unión | C23: shifts independientes elevan S_total ~21x conservando S_i | Objetivo explícito del optimizador, no nueva teoría ni ventaja neural | OBSERVACIÓN SINTÉTICA |
| BR30-F07 | Multiespectral y disponibilidad local generan intercambio útil | C07-C08 y C29 frontera observada | CVT/QMC/lattice otras ventajas, se ignoran costes de construcción | HIPÓTESIS ABIERTA |
| BR30-F08 | Métrica de S(k) baja predice mejora en GPT | Ninguna | Experimentos Scale3D previos no concluyentes, ningún test de GPT aquí | NO VALIDADO |
| BR30-F09 | Reducción de sensores preserva gran ventaja MHU | C27 ligera ventaja a mitad densidad | Pérdida de casi toda supresión: MSE entre organizados converge | DEBILITADA |
| BR30-F10 | Beneficio de fases cruzadas podría mediar tareas de señal compartida | C23 y álgebra de amplitudes | No se ha entrenado ni ensayado tarea shared-channel | PRIORIZAR SI HAY 8 CICLOS MÁS |

**Procedencia:** `docs/AB_LEDGER_C01_C30.json`, fuente `src/ab30_live.py`. Estados exploratorios no son *Bayes factors* ni posteriores calibrados. Históricos BR12/BR30 anteriores permanecen en ledger maestro.
