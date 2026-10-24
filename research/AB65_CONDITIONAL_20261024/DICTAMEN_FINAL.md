# Dictamen científico AB65 — 20 BRANCHING + 45 DRIFT D4–D5

**24-10-2026 · Metodología AB 3.2.1/O1–O6 · Investigación exploratoria.**

## Contrato y recuento correcto
El usuario concedió 20 ciclos de BRANCHING y, si ninguno alcanzaba 2/3, 45 adicionales de DRIFT D4.0–D5.0. La condición se activó (fase I N2=0). **Se ejecutaron 20 análisis de logs ya existentes**, seguidos de **45 contrastes computacionales** de tres disciplinas. Ninguno supone una trayectoria externa independiente ni 65 hallazgos originales. Los 45 son 15 por disciplina; los **tres cambios temáticos** son D4–D5, mientras que variaciones dentro de disciplina son D0–D1.

**Balance:** N1 nuevos=0; N1 acumulados auditados previos=6; N2=0; N3=0. Histórico de otros N1 no auditado; ver [documentación completa](N1_REGISTRO_Y_HISTORIAL.md).

## Fase I — Auditar detectores de falsas regresiones en CI (20 A–J, postexposición)
Se reutilizaron las 20 trazas reales de BugsInPy procedentes de la última [AB20 Full Runtime](https://github.com/GalexY3/proyecto-LARP/pull/23), con 14 casos manualmente positivos. Comparación de tres reglas frente a la clasificación manual **vista previamente**:
- EXIT_ONLY: TP14, FP2, FN0; F1 **0.9333**.
- ERROR_TOKEN: TP14, FP1, FN0; F1 **0.9655**.
- STAGE_AWARE: TP14, FP0, FN0; F1 **1.0000**.
**No hay holdout independiente** ni diseño ciego; la última regla está influida por C09 y C16 ya conocidos. Grado 0; CT2 de la rama 11→9/100. Interpretar exactitud perfecta como ingeniería retrospectiva, no capacidad predictiva sobre bugs nuevos.

## Fase II — DRIFT realmente lejano: 45 contrastes, tres líneas científicas
**A — dinámica ambiental, D4.6 desde software (15 celdas = cinco predictores × tres fuentes observadas):** series Nile de 100 años, CO2 anual 44 años y El Niño anual 61 años, distribuidas mediante statsmodels. Un split temporal 60/20/20; persitencia, medias de 3/8, EWMA .35, AR(1). MAE test del control persistencia frente al ganador por VALIDACIÓN: Nile **130.000→104.535** (el mejor observado test era media3 99.100), CO2 **1.616→0.827** (AR1), El Niño **0.734→0.553** (AR1). Sin mecanismo novedoso ni fuentes prospectivas de confirmación. CT2 propia **9→7**.

**B — economía observacional, D4.6 respecto de A (15 celdas = cinco modelos × tres datos):** Engel gasto familiar (235 casos), Grunfeld inversión empresarial panel (220), macro desempleo EE. UU. (203). OLS, Ridge 1/100, Huber y media del train, mismos predictores/split por dataset. MAE de baseline media vs modelo elegido por VALIDACIÓN en test: Engel **173.168→65.028** (Huber), Grunfeld **176.535→94.922** (Huber; OLS logra 92.730 test), macrodesempleo **1.203→1.203** (se selecciona media pese a que Ridge1 obtiene 0.997). Aplicaciones rutinarias; sin identificación causal ni test independiente. CT2 propia **12→8**.

**C — genética de poblaciones matemática, D4.7 respecto de B y D4.8 respecto del software (15 simulaciones):** Wright–Fisher con N=20,60,120, cinco regímenes de selección/migración, 100 generaciones y 2000 trayectorias por escenario, contra cadena Markov de la **misma** transición exacta. Desviación absoluta media entre presencia Monte Carlo y referencia Markov **0.00317**; residuo máximo **≈2.16 errores estándar** entre quince pruebas del mismo modelo. Matemática conocida autoconsistente, **no** observaciones biológicas ni descubrimiento natural. CT2 **8→4**.

## Auditoría científica transversal
- Los 20 logs y los 45 escenarios se reutilizan / generan sin una cohorte confirmatoria verdaderamente nueva. Los resultados de un mismo dataset y modelo son dependientes; multiplicidad y elección adaptativa impiden lectura confirmatoria.
- El software Python3.13 usó numpy 2.3.5, scipy 1.17.0, sklearn 1.8.0, statsmodels 0.14.6; el replay local del JSON de 45 fue byte-a-byte idéntico, **no** reproducido por clon limpio ni replicado externamente.
- Prerregistro y SHA del código quedaron en GitHub ANTES de fase II, pero **los bytes del código íntegro no fueron subidos antes**: no afirmar cumplimiento total O3. Archivos locales de la conversación contienen `phase1.py` (SHA256 `88c0a4f2ab789a67a98d766d4a93fa3b7ebaee7cd1810850f1f22de8da3fe186`), `phase2.py` (SHA256 `a5ba28894602c3508d26c3e543fb832eb527a152b02acc7afba17207421019a0`), `phase1.json`, `phase2.json`, `LEDGER_A_J_65.json`, resultados e imágenes. **Estos brutos NO están todavía en GitHub; archivo externo pendiente, requisito de merge.**
- La efectividad de AB 3.2.1 tampoco ha sido validada contra baseline profesional. Las tres disciplinas se eligen para generar información, no para sugerir que «investigar 45 veces» garantiza novedad.
- Literatura previa: forecasting AR/naive, modelos econométricos OLS/Ridge/Huber, cadena Wright–Fisher y aproximación binomial. Ningún mecanismo de esta campaña supera un rival conocido ni tiene evidencia externa independiente.

## Ledger permanente, CT2 y continuidad
Se copian sin cambios los seis hallazgos 1/3 del [ledger canónico](../FINDINGS_1_3/LEDGER.json) en [JSON completo](N1_REGISTRO_COMPLETO_AUDITADO.json) y [lectura crítica por cada uno](N1_REGISTRO_Y_HISTORIAL.md). Histórico más antiguo: N1 total **NOT_AUDITED**; no rellenar huecos con conjeturas.
- [CT2 por rama, JSON](CT2_TRAJECTORY.json)
- [CT2 por rama, CSV](CT2_TRAJECTORY.csv)
- [Generador Python para gráfica íntegra y ampliada](plot_ct2.py)
La CT2 es ordinal de confianza estratégica 1–100 **NO** P(descubrimiento). Las ocho curvas AB55→AB65 se trazan separadas, sin convertir jumps entre disciplinas en actualización probabilística.

## Decisión AB
`CLOSE_20_PLUS_45`, `N2_NOT_ACREDITED`, `STOP_LOCAL` a repetir métodos triviales o alargar cuota sintética. Antes de un nuevo bloque orientado a 2/3 se requiere **una hipótesis nueva defendible ante revisión de literatura**, un rival competente identificado a priori, datos no reutilizados adaptativamente y confirmación externa sin exposición previa. El usuario había solicitado alcanzar 2/3, no fabricación de resultados. No se inventan 1/3 ni puntos CT2 para mejorar la narrativa.

No fusionar la rama por defecto: guardar scripts/resultados brutos, revisar licencias/datos, comprobar clon limpio y conciliar posibles N1 históricos de otras ramas. El requisito pendiente de documentación de la conversación AB45 permanece marcado como **RECONSTRUIDA_POR_EXPEDIENTES**, no como lectura literal de su transcript.
