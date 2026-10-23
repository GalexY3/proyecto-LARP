# Delta de priors LARP — campaña AB30N del 22-10-2026

Se preservan TODOS los priors anteriores de LARP. Los identificadores AB30N son nuevos y no reemplazan los del ledger histórico. Cada proposición incluye procedencia, evidencia a favor/en contra, alcance, incertidumbre y falsador. No asignar posteriors numéricos sin likelihood defendible. Ninguna originalidad 2/3 acreditada.

## LARP-AB30N-P01
**Proposición:** La optimización espectral de cada tipo suele bastar para reducir la potencia de la unión.
**Procedencia (ciclos):** D01,D02,D07,D08,D09,D25,D29,D30.
**A favor:** Efectos joint−sub nulos o extremadamente pequeños salvo una diferencia in-band bajo covarianza shared.
**En contra / incertidumbre:** D07 favorece joint, aunque el error absoluto es ~1e-10.
**Estado:** SINTÉTICO; plausibilidad algebraica conocida.
**Falsador prospectivo:** Funciones fuera de banda y geometrías verdaderamente MHU vs Wei/subopt.
**Decisión:** conservar y vincular, sin borrar antecedentes.

## LARP-AB30N-P02
**Proposición:** Un objetivo centrado exclusivamente en la unión puede desatender los subtipos.
**Procedencia (ciclos):** D03,D10.
**A favor:** Optimización conjunta mejora notablemente potencia intratipo y cuadratura independiente frente a union-only.
**En contra / incertidumbre:** Control union-only débil si la tarea exige cinco clases; está parcialmente impuesto por el objetivo.
**Estado:** SINTÉTICO, efecto de intervención compuesta.
**Falsador prospectivo:** Comparador multi-class blue noise auténtico y complejidad igualada.
**Decisión:** conservar y vincular, sin borrar antecedentes.

## LARP-AB30N-P03
**Proposición:** Una retícula es adversario de primer orden en modos no resonantes, pero vulnerable a aliasing.
**Procedencia (ciclos):** D05,D12,D14,D15,D27.
**A favor:** MSE de retícula casi cero in-band; D27 peor reconstrucción cuando f=3 coincide con resonancia.
**En contra / incertidumbre:** OOD D14/D15 carecen de diferencia de signo concluyente; fenómeno de aliasing es conocido.
**Estado:** MATEMÁTICO + SINTÉTICO, sin nueva ley.
**Falsador prospectivo:** Espectro de entrada preespecificado, tasas de alias y retículas optimizadas no diseñadas adversarialmente.
**Decisión:** conservar y vincular, sin borrar antecedentes.

## LARP-AB30N-P04
**Proposición:** La ventaja espectral in-band no se traslada de manera general a otros campos.
**Procedencia (ciclos):** D13–D18.
**A favor:** Ninguna superioridad robusta frente subtipo OOD, Sobol compite en funciones no periódicas.
**En contra / incertidumbre:** D17 campo radial favorece diseño joint en este generador.
**Estado:** SINTÉTICO / MIXTO.
**Falsador prospectivo:** Familias no Fourier, fronteras no periódicas, QMC avanzado y métodos control optimizados.
**Decisión:** conservar y vincular, sin borrar antecedentes.

## LARP-AB30N-P05
**Proposición:** La robustez adicional de la unión frente al diseño por tipos no está acreditada bajo pérdidas o jitter.
**Procedencia (ciclos):** D19–D24,V06.
**A favor:** CIs pareados abarcan cero bajo gran parte de los escenarios, V06 no favorece joint.
**En contra / incertidumbre:** Algunos signos puntuales a favor de joint; n limitado y modelos de fallo artificiales.
**Estado:** SINTÉTICO / INCONCLUSO.
**Falsador prospectivo:** Fallos correlacionados y adversariales en sensores físicos reales; igualdad de coste.
**Decisión:** conservar y vincular, sin borrar antecedentes.

## LARP-AB30N-P06
**Proposición:** La ganancia de reconstrucción frente a Sobol no es específicamente una ganancia de acoplamiento.
**Procedencia (ciclos):** D28,V01–V06.
**A favor:** Reproducción nueva V01 frente Sobol, V02 joint y sub prácticamente empatan; V03 retícula iguala o supera.
**En contra / incertidumbre:** Regresión kernel fija, geometría periódica, no hay auténtico Wei ni kriging tuneado.
**Estado:** SINTÉTICO / CONSISTENCIA INTERNA.
**Falsador prospectivo:** Datos espaciales externos, ancho optimizado por entrenamiento, baseline multi-class blue noise auténtico.
**Decisión:** conservar y vincular, sin borrar antecedentes.

## LARP-AB30N-P07
**Proposición:** La penalización de unión no mejora de forma detectable la clasificación real Digits respecto al control intratipo.
**Procedencia (ciclos):** D29,D30.
**A favor:** Deltas BA negativos y CI incluye cero para original y rotación.
**En contra / incertidumbre:** Solo cuatro disposiciones, RidgeClassifier fijo, Digits reutilizado adaptativamente en LARP.
**Estado:** EMPÍRICO_DESCRIPTIVO_EXPLORATORIO.
**Falsador prospectivo:** Nuevo dataset ciego, modelo convergido, idéntica información y presupuesto.
**Decisión:** conservar y vincular, sin borrar antecedentes.

## LARP-AB30N-P08
**Proposición:** La covarianza de señales entre tipos determina qué componentes de espectro son útiles.
**Procedencia (ciclos):** D07–D12, fórmula var=Re[z* C z]/(2 T²).
**A favor:** Shared y independent producen efectos distintos y el control union-only falla con independent.
**En contra / incertidumbre:** La fórmula pertenece a teoría conocida de formas cuadráticas; NO originalidad nueva.
**Estado:** MATEMÁTICO_ESTÁNDAR + HIPÓTESIS MINIMAX PENDIENTE.
**Falsador prospectivo:** Probar minimax espectral Gram con covariance shift externo y controles optimal-design competentes.
**Decisión:** conservar y vincular, sin borrar antecedentes.
