# LARP · AB 3.2.1 · BRANCHING 30 — Ledger auditable

**2026-10-21**. Bloque autorizado expresamente por el investigador para LARP (no reutiliza autorizaciones de AB general).
**Alcance:** 30 decisiones *condición-específicas* agrupadas en seis familias, **no** 30 descubrimientos independientes. Todas A–F son exploratorias excepto la única reivindicación C11 confirmada en mundos nuevos tras prerregistro de selección. Una única geometría por construcción: no replicación biológica externa.
**Nota de integridad:** toda condición exploratoria comparte simulador, geometrías, mundos, etiquetas y algunos controles. No interpretar los 880 registros del piloto como 880 experimentos independientes.

## Contrato compartido A–J
A. Unidad: geometría 3D toroidal fija de 4096 nodos y/o mundo Fourier generado. Estimando geométrico: cobertura/radio para un punto uniformemente consultado; estimando predictivo: media MSE por mundo. Acceso a tipos y posiciones es idéntico entre brazos. B. Hipótesis rivales: LOCAL favorecida, nula de igualdad, MHU/STRATIFIED/RANDOM competentes y H_otras no modelada. C. Métricas, semillas y presupuesto en prerregistro. D. Invariantes de cuotas/permutación y no fuga en inferencia. E. Control apareado. F. Auditoría adversarial y mecanismos impuestos. G. Piloto seeds 11–20; selección única C11 confirmada con seeds 901–920. H. Actualización cualitativa de priors, sin probabilidades numéricas inventadas. I. Dictamen multidimensional. J. AB-DECIDE.

## Ciclo LARP-BR30-01 — Probabilidad de disponer de los cinco tipos entre los vecinos más próximos · k=8
**Pregunta y estimando (A).** Probabilidad de disponer de los cinco tipos entre los vecinos más próximos. Condición congelada `k=8`; estimando medido: `cobertura` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.505737 | 0.466431 | 0.297363 | 0.181152 | 0.208374 |
**Auditor adversarial (F).** Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. **Falsador:** LOCAL no eleva cobertura respecto al control estratificado ni a RANDOM para este k, o el orden se invierte.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es +0.208374, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-02 — Probabilidad de disponer de los cinco tipos entre los vecinos más próximos · k=12
**Pregunta y estimando (A).** Probabilidad de disponer de los cinco tipos entre los vecinos más próximos. Condición congelada `k=12`; estimando medido: `cobertura` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.848145 | 0.816284 | 0.623657 | 0.426636 | 0.224487 |
**Auditor adversarial (F).** Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. **Falsador:** LOCAL no eleva cobertura respecto al control estratificado ni a RANDOM para este k, o el orden se invierte.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es +0.224487, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-03 — Probabilidad de disponer de los cinco tipos entre los vecinos más próximos · k=16
**Pregunta y estimando (A).** Probabilidad de disponer de los cinco tipos entre los vecinos más próximos. Condición congelada `k=16`; estimando medido: `cobertura` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.962036 | 0.949097 | 0.808838 | 0.623169 | 0.153198 |
**Auditor adversarial (F).** Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. **Falsador:** LOCAL no eleva cobertura respecto al control estratificado ni a RANDOM para este k, o el orden se invierte.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es +0.153198, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-04 — Probabilidad de disponer de los cinco tipos entre los vecinos más próximos · k=24
**Pregunta y estimando (A).** Probabilidad de disponer de los cinco tipos entre los vecinos más próximos. Condición congelada `k=24`; estimando medido: `cobertura` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.998291 | 0.997681 | 0.94751 | 0.85144 | 0.050781 |
**Auditor adversarial (F).** Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. **Falsador:** LOCAL no eleva cobertura respecto al control estratificado ni a RANDOM para este k, o el orden se invierte.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es +0.050781, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-05 — Probabilidad de disponer de los cinco tipos entre los vecinos más próximos · k=32
**Pregunta y estimando (A).** Probabilidad de disponer de los cinco tipos entre los vecinos más próximos. Condición congelada `k=32`; estimando medido: `cobertura` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 1.0 | 1.0 | 0.983521 | 0.941895 | 0.016479 |
**Auditor adversarial (F).** Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad. **Falsador:** LOCAL no eleva cobertura respecto al control estratificado ni a RANDOM para este k, o el orden se invierte.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es +0.016479, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-06 — Radio necesario para alcanzar los cinco tipos funcionales · q=0.50
**Pregunta y estimando (A).** Radio necesario para alcanzar los cinco tipos funcionales. Condición congelada `q=0.50`; estimando medido: `radio` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.077424 | 0.078636 | 0.084897 | 0.092627 | -0.007473 |
**Auditor adversarial (F).** Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. **Falsador:** LOCAL no reduce el radio de cuantiles respecto a RANDOM/control estratificado.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.007473, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-07 — Radio necesario para alcanzar los cinco tipos funcionales · q=0.75
**Pregunta y estimando (A).** Radio necesario para alcanzar los cinco tipos funcionales. Condición congelada `q=0.75`; estimando medido: `radio` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.084944 | 0.08626 | 0.095843 | 0.105935 | -0.0109 |
**Auditor adversarial (F).** Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. **Falsador:** LOCAL no reduce el radio de cuantiles respecto a RANDOM/control estratificado.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.010900, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-08 — Radio necesario para alcanzar los cinco tipos funcionales · q=0.90
**Pregunta y estimando (A).** Radio necesario para alcanzar los cinco tipos funcionales. Condición congelada `q=0.90`; estimando medido: `radio` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.092051 | 0.093809 | 0.106639 | 0.119117 | -0.014589 |
**Auditor adversarial (F).** Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. **Falsador:** LOCAL no reduce el radio de cuantiles respecto a RANDOM/control estratificado.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.014589, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-09 — Radio necesario para alcanzar los cinco tipos funcionales · q=0.95
**Pregunta y estimando (A).** Radio necesario para alcanzar los cinco tipos funcionales. Condición congelada `q=0.95`; estimando medido: `radio` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.096463 | 0.098276 | 0.113983 | 0.127818 | -0.01752 |
**Auditor adversarial (F).** Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. **Falsador:** LOCAL no reduce el radio de cuantiles respecto a RANDOM/control estratificado.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.017520, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-10 — Radio necesario para alcanzar los cinco tipos funcionales · q=0.99
**Pregunta y estimando (A).** Radio necesario para alcanzar los cinco tipos funcionales. Condición congelada `q=0.99`; estimando medido: `radio` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.105178 | 0.106785 | 0.130533 | 0.146064 | -0.025356 |
**Auditor adversarial (F).** Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo. **Falsador:** LOCAL no reduce el radio de cuantiles respecto a RANDOM/control estratificado.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.025356, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-11 — Error de reconstrucción composicional frente a frecuencia espacial · freq=1
**Pregunta y estimando (A).** Error de reconstrucción composicional frente a frecuencia espacial. Condición congelada `freq=1`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.133975 | 0.140211 | 0.207771 | 0.355091 | -0.073796 |
**Auditor adversarial (F).** La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. **Falsador:** LOCAL no supera un estratificado por tipo con el mismo interpolador; la diferencia desaparece con frecuencias mayores.
**Confirmación (G).** Mundos 901–920 confirmaron la comparación LOCAL−STRATIFIED en C11; NO nuevos patrones físicos/geométricos; ver documento principal.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.073796, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE → prueba confirmatoria única preregistrada (realizada después de seleccionar C11)**

## Ciclo LARP-BR30-12 — Error de reconstrucción composicional frente a frecuencia espacial · freq=2
**Pregunta y estimando (A).** Error de reconstrucción composicional frente a frecuencia espacial. Condición congelada `freq=2`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.811611 | 0.807418 | 0.909168 | 1.107649 | -0.097556 |
**Auditor adversarial (F).** La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. **Falsador:** LOCAL no supera un estratificado por tipo con el mismo interpolador; la diferencia desaparece con frecuencias mayores.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.097556, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-13 — Error de reconstrucción composicional frente a frecuencia espacial · freq=3
**Pregunta y estimando (A).** Error de reconstrucción composicional frente a frecuencia espacial. Condición congelada `freq=3`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 1.590264 | 1.596647 | 1.710608 | 1.835722 | -0.120344 |
**Auditor adversarial (F).** La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. **Falsador:** LOCAL no supera un estratificado por tipo con el mismo interpolador; la diferencia desaparece con frecuencias mayores.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.120344, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-14 — Error de reconstrucción composicional frente a frecuencia espacial · freq=4
**Pregunta y estimando (A).** Error de reconstrucción composicional frente a frecuencia espacial. Condición congelada `freq=4`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 1.98237 | 1.999319 | 2.074392 | 2.102328 | -0.092023 |
**Auditor adversarial (F).** La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. **Falsador:** LOCAL no supera un estratificado por tipo con el mismo interpolador; la diferencia desaparece con frecuencias mayores.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.092023, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **STOP para altas frecuencias: ventaja decrece y error absoluto aumenta**

## Ciclo LARP-BR30-15 — Error de reconstrucción composicional frente a frecuencia espacial · freq=6
**Pregunta y estimando (A).** Error de reconstrucción composicional frente a frecuencia espacial. Condición congelada `freq=6`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 2.105872 | 2.131938 | 2.148912 | 2.156024 | -0.04304 |
**Auditor adversarial (F).** La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador. **Falsador:** LOCAL no supera un estratificado por tipo con el mismo interpolador; la diferencia desaparece con frecuencias mayores.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.043040, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **STOP para altas frecuencias: ventaja decrece y error absoluto aumenta**

## Ciclo LARP-BR30-16 — Resistencia de la reconstrucción ante pérdida aleatoria de sensores · drop=0
**Pregunta y estimando (A).** Resistencia de la reconstrucción ante pérdida aleatoria de sensores. Condición congelada `drop=0`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.811611 | 0.807418 | 0.909168 | 1.107649 | -0.097556 |
**Auditor adversarial (F).** El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. **Falsador:** La ventaja de LOCAL se anula o invierte bajo la tasa de dropout fijada.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.097556, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-17 — Resistencia de la reconstrucción ante pérdida aleatoria de sensores · drop=0.1
**Pregunta y estimando (A).** Resistencia de la reconstrucción ante pérdida aleatoria de sensores. Condición congelada `drop=0.1`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.893906 | 0.906231 | 0.978446 | 1.128251 | -0.08454 |
**Auditor adversarial (F).** El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. **Falsador:** La ventaja de LOCAL se anula o invierte bajo la tasa de dropout fijada.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.084540, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-18 — Resistencia de la reconstrucción ante pérdida aleatoria de sensores · drop=0.25
**Pregunta y estimando (A).** Resistencia de la reconstrucción ante pérdida aleatoria de sensores. Condición congelada `drop=0.25`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 1.053774 | 1.038863 | 1.120196 | 1.260602 | -0.066423 |
**Auditor adversarial (F).** El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. **Falsador:** La ventaja de LOCAL se anula o invierte bajo la tasa de dropout fijada.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.066423, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-19 — Resistencia de la reconstrucción ante pérdida aleatoria de sensores · drop=0.4
**Pregunta y estimando (A).** Resistencia de la reconstrucción ante pérdida aleatoria de sensores. Condición congelada `drop=0.4`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 1.217849 | 1.228537 | 1.334883 | 1.405661 | -0.117034 |
**Auditor adversarial (F).** El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. **Falsador:** La ventaja de LOCAL se anula o invierte bajo la tasa de dropout fijada.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.117034, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-20 — Resistencia de la reconstrucción ante pérdida aleatoria de sensores · drop=0.6
**Pregunta y estimando (A).** Resistencia de la reconstrucción ante pérdida aleatoria de sensores. Condición congelada `drop=0.6`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 1.53634 | 1.543966 | 1.524374 | 1.613459 | 0.011966 |
**Auditor adversarial (F).** El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal. **Falsador:** La ventaja de LOCAL se anula o invierte bajo la tasa de dropout fijada.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es +0.011966, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **STOP por degradación notable a dropout=.60**

## Ciclo LARP-BR30-21 — Sensibilidad al ancho de banda del estimador espacial · bw_k24=0.3
**Pregunta y estimando (A).** Sensibilidad al ancho de banda del estimador espacial. Condición congelada `bw_k24=0.3`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.607915 | 0.606138 | 0.761811 | 1.016821 | -0.153896 |
**Auditor adversarial (F).** La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. **Falsador:** La ventaja relativa de LOCAL depende críticamente de elegir retrospectivamente el bandwidth.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.153896, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-22 — Sensibilidad al ancho de banda del estimador espacial · bw_k24=0.6
**Pregunta y estimando (A).** Sensibilidad al ancho de banda del estimador espacial. Condición congelada `bw_k24=0.6`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.709573 | 0.708134 | 0.827054 | 1.044115 | -0.11748 |
**Auditor adversarial (F).** La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. **Falsador:** La ventaja relativa de LOCAL depende críticamente de elegir retrospectivamente el bandwidth.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.117480, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-23 — Sensibilidad al ancho de banda del estimador espacial · bw_k24=1
**Pregunta y estimando (A).** Sensibilidad al ancho de banda del estimador espacial. Condición congelada `bw_k24=1`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.8129 | 0.808641 | 0.910255 | 1.10871 | -0.097355 |
**Auditor adversarial (F).** La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. **Falsador:** La ventaja relativa de LOCAL depende críticamente de elegir retrospectivamente el bandwidth.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.097355, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-24 — Sensibilidad al ancho de banda del estimador espacial · bw_k24=2
**Pregunta y estimando (A).** Sensibilidad al ancho de banda del estimador espacial. Condición congelada `bw_k24=2`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.863344 | 0.857425 | 0.951981 | 1.142025 | -0.088637 |
**Auditor adversarial (F).** La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. **Falsador:** La ventaja relativa de LOCAL depende críticamente de elegir retrospectivamente el bandwidth.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.088637, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-25 — Sensibilidad al ancho de banda del estimador espacial · bw_k24=4
**Pregunta y estimando (A).** Sensibilidad al ancho de banda del estimador espacial. Condición congelada `bw_k24=4`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.876396 | 0.870028 | 0.962887 | 1.150814 | -0.086491 |
**Auditor adversarial (F).** La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente. **Falsador:** La ventaja relativa de LOCAL depende críticamente de elegir retrospectivamente el bandwidth.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.086491, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **CONTINUE sólo con control externo/no simulado**

## Ciclo LARP-BR30-26 — Ablación causal de posiciones, etiquetas y correspondencia señal–posición · labels_shuffled
**Pregunta y estimando (A).** Ablación causal de posiciones, etiquetas y correspondencia señal–posición. Condición congelada `labels_shuffled`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 1.104115 | 1.101002 | 1.067733 | 1.16832 | 0.036383 |
**Auditor adversarial (F).** La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. **Falsador:** Ablación no cambia nada cuando debería, o cambia mucho un control que debería ser invariante; posible bug o inferencia espuria.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es +0.036383, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **STOP en esta ablación: mecanismo conocido, no original**

## Ciclo LARP-BR30-27 — Ablación causal de posiciones, etiquetas y correspondencia señal–posición · positions_shuffled_per_type
**Pregunta y estimando (A).** Ablación causal de posiciones, etiquetas y correspondencia señal–posición. Condición congelada `positions_shuffled_per_type`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.811611 | 0.807418 | 0.909168 | 1.107649 | -0.097556 |
**Auditor adversarial (F).** La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. **Falsador:** Ablación no cambia nada cuando debería, o cambia mucho un control que debería ser invariante; posible bug o inferencia espuria.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.097556, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **REPAIR (control de identidad, no intervención sustantiva)**

## Ciclo LARP-BR30-28 — Ablación causal de posiciones, etiquetas y correspondencia señal–posición · only_dominant
**Pregunta y estimando (A).** Ablación causal de posiciones, etiquetas y correspondencia señal–posición. Condición congelada `only_dominant`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 2.036359 | 2.036359 | 2.036359 | 2.036359 | 0.0 |
**Auditor adversarial (F).** La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. **Falsador:** Ablación no cambia nada cuando debería, o cambia mucho un control que debería ser invariante; posible bug o inferencia espuria.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es +0.000000, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **STOP en esta ablación: mecanismo conocido, no original**

## Ciclo LARP-BR30-29 — Ablación causal de posiciones, etiquetas y correspondencia señal–posición · signals_scrambled_per_type
**Pregunta y estimando (A).** Ablación causal de posiciones, etiquetas y correspondencia señal–posición. Condición congelada `signals_scrambled_per_type`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 2.162113 | 2.15219 | 2.132754 | 2.202591 | 0.029359 |
**Auditor adversarial (F).** La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. **Falsador:** Ablación no cambia nada cuando debería, o cambia mucho un control que debería ser invariante; posible bug o inferencia espuria.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es +0.029359, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **STOP en esta ablación: mecanismo conocido, no original**

## Ciclo LARP-BR30-30 — Ablación causal de posiciones, etiquetas y correspondencia señal–posición · positions_labels_permuted
**Pregunta y estimando (A).** Ablación causal de posiciones, etiquetas y correspondencia señal–posición. Condición congelada `positions_labels_permuted`; estimando medido: `MSE` en una consulta/mundo de la población sintética especificada.
**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. H_otras: otras leyes de diseño espacial no evaluadas.
**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.
**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.
**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:
| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |
|---:|---:|---:|---:|---:|
| 0.811611 | 0.807418 | 0.909168 | 1.107649 | -0.097556 |
**Auditor adversarial (F).** La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes. **Falsador:** Ablación no cambia nada cuando debería, o cambia mucho un control que debería ser invariante; posible bug o inferencia espuria.
**Confirmación (G).** NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.
**Actualización AB (H).** La diferencia observada respecto a control espacial competente es -0.097556, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.
**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.
**AB-DECIDE (J).** **REPAIR (control de identidad, no intervención sustantiva)**

## Auditoría transversal del branching
- Resultados C:E con mundos sintéticos independientes de distinto coeficiente, pero **geometría compartida fija**. No bootstrap sobre queries como si fueran geometrías.
- Las muestras de A/B son Monte Carlo sobre la misma geometría, por tanto IC entre queries solo mediría error de integración espacial, no efecto generalizable sobre generadores.
- F28 elimina cuatro tipos y pierde casi todo rendimiento por construcción: no atribuir causalidad emergente.
- F27 y F30 son **controles de identidad algebraica**, no ablaciones de disposición espacial. Comprobar que no cambian la predicción; su existencia evita pseudohallazgos.
- El diseño no enfrenta LARP neuronal, MoE o Transformer, sino **geometrías + interpolador clásico**. NO afirmar superioridad arquitectónica.
- Las 30 decisiones comparten seis preguntas-familia: nadie debe presentarlas como treinta ensayos científicos independientes.
