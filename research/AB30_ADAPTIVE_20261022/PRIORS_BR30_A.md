# LARP BR30-A — adenda de priors, 22-10-2026

**Tipo:** priors sustantivos LARP. Son cualitativos; no sustituyen el ledger previo BR06/BR08/BR30 ni pasan a los A01–A21 metodológicos. **Origen:** 30 condiciones sintéticas adaptativas, más reparación post hoc.

| ID | Proposición y alcance | Evidencia favorable | Contraevidencia/límite | Falsador | Estado |
|---|---|---|---|---|---|
| BR30-A01 | Covarianza piloto puede mejorar cuadratura de campos 3D correlacionados | COSI-shrink-monotone RMSE .06042 frente MHU .07345 en 30 condiciones | Igualada tarea sintética; misma familia DGP; no se controló coste total ni kernel competente | Una cuadratura por kernels con mismo piloto iguala/supera el efecto | SINTETICO_EXPLORATORIO |
| BR30-A02 | Contracción isotrópica sirve contra especialización piloto | Mejora agregada media frente COSI-monotone (.06042 vs .06104 fuente; .06561 vs .06835 shift) | Selección de parámetros exploratoria; heterogeneidad y shift pueden invertir efectos | Comparador con shrink óptimo y holdout externo | CONDICIONAL |
| BR30-A03 | Rankings con fixed-step pueden invertirse por inestabilidad | C27 oráculo peor antes, mejor en solver monótono (.08820 vs MHU .10695 fuente) | Repair modifica pasos y update; no establece óptimo global | Reproducción con L-BFGS, gradiente y mismas condiciones | REPAIR_DETECTADO |
| BR30-A04 | Ledger parent+resultado permite verificar branching limitado | 30 entradas con reason_from_prior | Scheduler predefine familias y balancea aproximadamente 5 por familia; no 30 proyectos independientes | Testear decisiones de scheduler contrafactuales | METODOLOGICO_OBSERVACIONAL_LOCAL |
| BR30-A05 | COSI representa principio geométrico nuevo de orden neuronal | Ninguna | Kernel discrepancy matricial es antecedente, no se entrenó red | Superar rivales kernel y Wei y red baseline pareados en 3D real | NO_VALIDADO |
