# Auditoría independiente del matching espectral

Estado inicial: **AUDITOR PREPARADO; implementación y búsqueda pendientes de auditoría**. Se aplica AB 2.1 prospectivamente. No se generaron controles, entrenaron redes ni calcularon scores de adquisición. Esta nota no autoriza ejecuciones.

## Definiciones que deben congelarse

El auditor `artifacts/spectral_matching/independent_metrics_check.py` usa sólo NumPy y biblioteca estándar; no importa funciones de `larp`. Reconstruye distancias con una implementación propia de imagen mínima, matrices dirigidas y los seis modos originales. Lee NPZ sin pickle, conserva el orden de nodos y exige X float64, etiquetas int64, N400, L20 y conteos `[163,85,68,50,34]`.

1. Los centros son exactamente 10.000 muestras uniformes mediante `default_rng(SeedSequence([20261008,8841]))`. No reutilizar los centros del certificado histórico, cuya semilla es distinta. Cobertura significa distancia desde cada centro al punto más próximo del tipo correspondiente.
2. La distancia entre CDF empíricas se evalúa en la unión de **todos** los valores observados, incluyendo multiplicidad y usando CDF derecha. Un histograma aproximado puede ocultar su máximo. Para evitar un rechazo espurio en el umbral 0,02, se restan productos cruzados de conteos enteros antes de dividir; no se restan dos probabilidades flotantes redondeadas.
3. Cuantiles mediante `np.quantile(..., method="linear")`. El normalizador por tipo es `a_c=L/sqrt(n_c)`, común a referencia y candidato. Ninguna normalización usa el espaciado observado del candidato.
4. Ventanas: discos periódicos, inclusión `d <= R`, radios físicos 1,25 y 2,5. El soporte de conteos y fracción vacía se publica por tipo. La comparación de fracción vacía no se sustituye por igualdad de medias.
5. Vecino homotípico: excluir únicamente el mismo **índice** de nodo. Un vecino distinto en una coordenada idéntica tiene distancia cero; no puede descartarse. Comparar CDF, los tres cuantiles y el mínimo con los criterios fijados conjuntamente.
6. Histogramas homotípicos: todas las parejas físicas no ordenadas `i<j`. Bins `[0,.5,1,1.5,2,2.5]`, convención `[a,b)` salvo último bin inclusivo en 2,5. No son arcos del grafo ni histogramas de nearest-neighbour.
7. Matriz de arcos: filas tipo de **origen**, columnas tipo de **destino**; `E[0]` es source y `E[1]` target. No simetrizar ni colapsar recíprocos. Se comprueba cada una de las 25 celdas con tolerancia entera derivada de su conteo de referencia. El outdegree medio es arcos salientes del tipo divididos por su población y su diferencia se divide por seis.
8. Toda condición se aplica a A–E simultáneamente. La admisión exige matching local y de arcos, referencia con medias ≤0,05 y máximos ≤0,10, candidato con medias ≥0,50 **para los cinco componentes**, unión idéntica y concentraciones válidas. No es admisión cumplir un coste surrogate bajo o alterar sólo un tipo.

## Espectros y falsas réplicas

Modos no redundantes en orden fijo: `(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2)`. Se usa `rho_c=sum exp(2πi X·n/L)` y `S_c=|rho_c|²/n_c`. La unión se suma directamente en orden de nodos, idéntico en ambos casos; sumar amplitudes por clases introduce otra secuencia de redondeo y puede violar igualdad de hashes a pesar de la invariancia matemática.

Las concentraciones son `eta_c=rho_c-(n_c/N)rho_union`; su suma debe ser cero salvo error de redondeo. Para que la diagonal del espectro cruzado de concentración coincida con `T_c`, normalizar amplitudes por `sqrt(n_c*(1-n_c/N))`. La matriz de componente ordinaria usa `rho_c/sqrt(n_c)` y su diagonal coincide con la media de `S_c`. Las matrices se promedian sobre los seis modos; el outer product de un solo modo tiene rango uno por construcción. Ni los cinco tipos ni los seis modos constituyen réplicas independientes de geometría.

Las tres referencias históricas reconstruidas cumplen holgadamente los límites espectrales. Sus máximos de `S_c` entre tipos/modos son aproximadamente 0,007581 (1101), 0,011364 (1102) y 0,017198 (1103). El residuo máximo de `sum eta_c` es menor que `2e-14`. Los valores completos se conservan en `native_independent_g1101_v1.json` a `native_independent_g1103_v1.json`; se calcularon exclusivamente sobre entradas históricas, sin construir candidatos. Esos recibos conservan el hash de la versión de auditor que los produjo; el posterior ajuste del CDF se registra por un nuevo self-test, sin sobrescribirlos.

## Límites científicos y de ejecución

El matching de estas estadísticas no iguala cada vecindario ni toda la microestructura. Una ventaja pequeña comparable a residuales locales no identifica causalidad exclusiva de ondas largas. No incorporar R4/R5 al matching: son descripciones posteriores del mecanismo intervenido. Las etiquetas son funciones de adquisición con radios físicos fijos por nodo; hacer viajar el radio con la etiqueta cambiaría el estimando y puede romper el empaquetamiento.

Las propuestas de búsqueda pueden usar estadísticas geométricas, pero nunca targets, MSE, gradientes de redes o scores de campos para seleccionar. Antes del primer intento, congelar código, semillas, propuestas, máximo de intentos/reinicios y techo externo. Seleccionar el primer control admitido; ningún control admisible dentro del presupuesto implica `NOT_IDENTIFIED`, no refutación de MHU. Calibrar exclusivamente infraestructura/métricas de referencias, sin candidatos ni scores, y contabilizar esa calibración aparte.

En Windows, el supervisor de un techo duro debe controlar el proceso que realmente calcula, no únicamente el redirector `venv/Scripts/python.exe`: usar CPython base con `__PYVENV_LAUNCHER__` apuntando al ejecutable del venv cuando proceda, o comprobar terminación del árbol completo. Un supervisor que mata un proceso intermediario y deja vivo el worker viola el presupuesto. La auditoría de infraestructura debe usar procesos dummy y preservar sus recibos; no usar una corrida científica como test del kill.

El self-test v2 contiene diez comprobaciones y se conserva sin cambios. El recibo v3 añade el límite exacto 0,02 de fracción vacía mediante conteos enteros: **11/11 PASS**. El recibo v4 verifica además la varianza continua para un punto Bernoulli y dos puntos coincidentes: **13/13 PASS**. Esto prueba el auditor; no equivale todavía a auditar una implementación o una búsqueda.

## Extensión prospectiva de 9 de octubre: varianza y suelo espectral

Se preparó el auditor para aceptar un `--spectral-floor` explícito y una puerta opcional `--variance-guard-relative`; el valor por defecto 0,50 y la ausencia de puerta conservan la definición histórica. La puerta nueva compara la **varianza continua exacta** del conteo en disco con la nativa, para ambos radios y cada tipo, y admite diferencia relativa absoluta ≤0,05. No compara la varianza empírica sobre los 10.000 centros. Los recibos `native_independent_g1101_v2.json` a `native_independent_g1103_v2.json` fijan todas las métricas, centros, arcos reconstruidos y radios físicos originales; no contienen controles ni scores.

El NPZ de un candidato debe conservar un array `physical_radii` float64 de 400 nodos. Los radios originales se recuperan una vez de `metadata_json.packing.cell_radii_A_to_E` y las etiquetas **nativas**. Permutar etiquetas funcionales no permite recalcular radios usando la nueva etiqueta.

La recomputación independiente `window_spectral_bound_check.py`, recibida en `window_spectral_bound_independent.json`, verifica por integración numérica los coeficientes del disco y por una suma de Fourier positiva hasta nmax64 la normalización de la varianza exacta. Con suelo q, la condición necesaria es `Var ≥ 12*n_c*q*min_6|w_R|²`. Para q=0,50, en A/R2,5 la cota 1,227426 supera las tres varianzas nativas 0,830803/0,875142/0,850924 incluso con el margen continuo de 5%. **q=0,50 más esa puerta continua es imposible en estas tres referencias.** Esto no prueba imposibilidad del protocolo histórico de CDF empírica ≤0,02, que carecía de esta puerta.

q=0,25 más la puerta continua de 5% queda **sin obstrucción por esta cota necesaria**; no demuestra que exista un etiquetado admitido. Los máximos q necesarios que permite la cota conjunta son 0,355354/0,374319/0,363961 para g1101/g1102/g1103. No son máximos alcanzables certificados.

La descomposición adicional se conserva en `independent_window_budget.json`, con script y entradas identificados por hash. Al llamar B a la varianza aportada por los seis modos y sus conjugados, y U a todo el resto, `ΔU ≤ .05*Var_native - [LB(q)-B_native]`. En q=0,25/R2,5/A esto exige reducir U al menos 0,567746/0,559863/0,569106, aproximadamente 68,7%/64,7%/67,0% del resto nativo. Es una redistribución espectral necesaria al condicionar la varianza, no una intervención que modifica sólo los seis modos. No aporta una conclusión sobre utilidad MHU ni rendimiento de adquisición.

El worker, configuración, supervisión y búsqueda siguen pendientes de auditoría prelaunch con firma y hashes finales. Ningún resultado matemático de esta sección autoriza ejecutar una búsqueda ni evaluar campos.
