# LARP AB30 O4 — Dictamen R1 y métricas de novedad (24-10-2026)

**30 ciclos AB A–J reparados Q01–Q30**, ejecutados en cinco bloques de seis fuentes. **CT2 final 15/100**, frente a 18/100 inicial; es juicio ordinal de trayectoria, no probabilidad. Hallazgos no duplicados de la campaña: **N1=2**, N2=0, N3=0. El recuento 1/3 histórico de otras campañas no fue auditado y no se inventa.

**REPAIR relevante, preservar historial:** una ejecución piloto B01 (6 salidas, no prerregistrada) precedió a los freezes y no se contabiliza. Después los 30 primeros experimentos B01–B05 con motor v1 SHA `f800f562...` estuvieron mal etiquetados Hamilton, pues redistribuían restos de forma iterativa. **Todos los 30 outputs v1 son inválidos para esa definición científica**; su código y resultados se conservan en el ZIP. Antes del replay R1 se comprometió la reparación exacta [REPAIR_R1_SOURCE](../prereg/REPAIR_R1_SOURCE.md) GitHub commit `52f811d` y motor v2 SHA256 `ad330115b84f9e47b8d0372c8d3b6222ae5c34b916b0d364d9a34b82c7449b14`, recuperable con [reconstruct.py](../src/reconstruct.py). Los 30 R1 son **exploratorios post-exposición**, no confirmación ciega.

Poblaciones observadas: sklearn Diabetes 442, Breast Cancer 569, Wine 178, Digits 1797, statsmodels Nile 100 y Sunspots 309. Estratificación 20/30/50% con covariable observable x. El verdadero y se usa SOLO para calcular la varianza del estimador, nunca para asignar etiquetas. E presupuestos 10/14/18 y G 26/34 **en las mismas poblaciones**. G no es confirmación externa. B04/B05 incluyen shocks de volatilidad artificiales, no drift natural. Resultado objetivo para media estratificada: Σ W_h²(1−n_h/N_h) S_y,h²/n_h.

| Ciclos | Pregunta | Hallazgo R1 |
|---|---|---|
| Q01–Q06 | ¿Cuántos parámetros de mezcla producen tratamientos enteros idénticos? | Aproximadamente 81–90% de 21 λ redundantes en presupuestos E. **1/3 ALIAS-01**, resultado operativo conocido matemáticamente. |
| Q07–Q12 | ¿La solución entera óptima para el proxy mejora el resultado verdadero frente a Hamilton? | Empeora en 5 de 6 fuentes; mejora solo en Wine. **1/3 PROXY-GAP-02**, desajuste de proxy ya comprendido teóricamente. |
| Q13–Q18 | ¿Redondeo dependiente aleatorio supera Hamilton determinista? | Pierde en seis fuentes E; algunos signos cambian con G. No generalidad. |
| Q19–Q24 | ¿Reserva 50/50 proporcional reduce el peor riesgo bajo shocks construidos frente a optimización proxy? | Favorece Diabetes, Breast y Nile; perjudica Wine, Digits, Sunspots en E. Efecto condicional y **no cuenta un tercer 1/3** por solapamiento con PROXY-GAP-02. |
| Q25–Q30 | ¿Minimax entero basado en incertidumbre del proxy supera guard 50/50 en el riesgo verdadero? | **Pierde en las seis fuentes** tanto E como G. Optimizar robustez del proxy no garantiza robustez del target. |

**Calibración/auditoría:** 630 comprobaciones sumas, cuotas y fronteras de muestra; 30 verificaciones de optimalidad del proxy exacto frente al redondeo; Monte Carlo de 7.000 muestras para Nile, varianza teórica 0,049304 vs empírica 0,048844 (0,93% relativo); 25.000 redondeos aleatorios preservan expectativas fraccionales aproximadamente. Los cinco bloques R1 se reprodujeron byte a byte tras extraer el archivo en otro directorio bajo **el mismo entorno instalado**. `CLEAN_GITHUB_CLONE_NOT_VERIFIED`, `EXTERNAL_REPLICATION_ABSENT`.

**Prior art:** Census Bureau 2014 documenta asignación estratificada entera óptima, incluida la insuficiencia de redondear; Neyman y costes ya están en bibliografía de muestreo. https://www.census.gov/library/working-papers/2014/adrm/rrs2014-07.html . No atribuir nivel 2/3/3/3 a los hallazgos actuales.

**Archivos:** los valores R1 redondeados por los treinta ciclos están en [RESULTS_R1_30_ROUNDED.json](../results/RESULTS_R1_30_ROUNDED.json). El ledger A–J de 30 ciclos (92.710 bytes), cinco JSON R1 por presupuesto, seis JSON v1 inválidos, priors, auditorías, código editable y todos sus SHA256 están en el ZIP de conversación `LARP_AB30_O4_20261024.zip` (27 miembros), SHA256 `25f1918c9d5991f2684bce4ac9601d2b489b0382c15d84ebc8cc44a8a844259f`. Los JSON completos aún no están en GitHub, solo el resumen y códigos/compromentisos; no fingir cumplimiento total O3 de archivo bruto remoto.

**AB-DECIDE:** 30 reparados completados sin STOP, cuatro transiciones BRANCH/DRIFT internas. Mejor siguiente clase de evidencia: costos reales y proxies medidos en una corriente externa con un baseline entero profesional, no más semillas de estos seis datos.
