# AB50 DRIFT lejano — 24/10/2026

**Estado comprobado:** **20 experimentos computacionales AB (P01–P20) + 10 ciclos especiales AB solo de PLANIFICACIÓN (D01–D10) + 20 experimentos computacionales AB (S01–S20)**. En total **50 ciclos A–J**, no 60 experimentos. En la fase final se eligió utilizar el **mínimo autorizado de 20** porque todavía no apareció una nueva fuente de evidencia independiente.

## Resultado
- **2/3: ninguno; 3/3: ninguno. Hallazgos 1/3 NUEVOS: 0.** Los cinco 1/3 anteriores conservan su ledger canónico en `main/research/FINDINGS_1_3/LEDGER.json`; histórico anterior a O4 no auditado.
- Primera rama D1,2, cobertura de sensores raros ante fallos. Zonal supera random 19/20 E y 20/20 G, pero farthest-first 12/20 E y 13/20 G. CT2 geométrica **7→5/100**. Misma geometría N=64, cuotas [32,20,12] por pareja; G son semillas del mismo simulador, no replicación externa.
- Ten special D3,3–D5,0: diez expedientes de alternativas, **solo planificación y literatura**. Oportunidad elegida D01, pruebas metamórficas de software científico D4,5, CT2 prospectiva 19/100. D10 verificación formal obtuvo 17/100, química computacional D08 6/100 pese a D5,0.
- Segunda rama D4,5, 20 variantes artificiales (5 funciones ×4 defectos). En las 48 entradas G por mutante, sanidad detecta 35,6%, metamórficas 64,9%, oráculo diferencial 97,9%. Referencias sanas cumplen 100% de relaciones en E y G. CT2 de software **19→13/100** después del control fuerte. **El salto 5→19 es reinicio de línea, no confirmación empírica.**

## Código, prerregistro y trazabilidad
- Script exacto `sensors.py`: SHA256 `4c2224a09052bae02dd907abed6bf28954c26456a11e8e6ca02098294ab7582d`, hash y contratos en SOURCE_LOCK/prereg ANTES de ejecutar.
- Script `metamorphic.py`: SHA256 `874fa5ca3518d1afcb6b8396b885f5b4c5fdb872e114f0a40e4aebe2f188ebb3`, hash y contratos antes de ejecutar. Las fuentes COMPLETAS se incluyen en el ZIP de conversación, pero los bytes de ambas **no fueron subidos enteramente a GitHub antes de las pruebas**, así que no fingir cumplimiento O3 completo.
- `prereg/PHASE_I_20.json`, `prereg/SPECIAL_D01_D10.json`, `prereg/PHASE_III_20.json`; resúmenes parciales `results/SUMMARY_40_ROUNDED.csv`.
- Archivo original descargable del usuario: `LARP_AB50_DRIFT_20261024_COMPLETO.zip`, SHA256 `39a4629b4ef157b477af0e0b2f4208bbbbf67aff1261123ce5e411cd2f489838`, 20 entradas. Incluye raw JSON por semilla, 50 expedientes A–J, diez contratos de oportunidades extensos, source, gráfica CT2 y manifiesto por SHA.
- **Reproducción verificada:** fuente y resultados regenerados **byte a byte** desde ZIP extraído en otro directorio, en el mismo entorno Python; sin clon limpio GitHub ni replicación científica externa. Los 10 especiales se verificaron estructuralmente, no pueden «reproducirse» como experimentos no ejecutados.
- **Deuda GitHub:** JSON individual completo y 130 KB de A–J siguen solo en ZIP; no fusionar automáticamente a main antes del backfill, revisión de procedencia y reejecución desde clon limpio.

**AB-DECIDE:** cerrar las 50 posiciones autorizadas sin hallazgo 2/3. Antes de otra campaña metamórfica se requiere software de terceros con fallos independientes, tests de referencia más competentes y paridad de presupuesto. Próxima autorización mínima 20, máxima 45 ciclos AB.

**Normativa nueva:** [AB 3.2.1-O5 D0–D5](https://github.com/GalexY3/Metodologia-AB/blob/main/docs/AB_3_2_1_O5_DISTANCIA_DRIFT.md), ya en `main`; CT2 se puntúa por rama, no comparar cambios de hipótesis como evidencia positiva.
