# LARP — Índice canónico de investigaciones
**Actualizado:** 2026-10-23. Este archivo distingue material fusionado, ramas pendientes y grado de evidencia. **Entrar en `main` significa conservación versionada, no confirmación científica.**

## Evidencia integrada y accesible en main

| Campaña | Material | Evidencia y límites | Estado documental |
|---|---|---|---|
| BR30 y BR12 históricos | [Dictamen](../docs/00_DICTAMEN.md), [priors acumulativos](../docs/02_PRIORS_LARP.md) | Reconstrucción espacial sintética con límites de generadores y controles | ARCHIVADA_EXPLORATORIA |
| AB30 CODEX | [Informe](AB30_CODEX_20261022/REPORT.md) | 10 de 30 ciclos de un bloque anterior; resultados condicionados; no asumir 30 completados aquí | ARCHIVADA_EXPLORATORIA |
| AB30 INTENSIVE | [Informe](AB30_INTENSIVE_20261022/reports/DICTAMEN.md), [CSV](AB30_INTENSIVE_20261022/results/RESULTS_30.csv) | 30 contrastes y 3 auditorías de CVT; no MHU certificada; archivo bruto completo fuera del repositorio | ARCHIVADA_EXPLORATORIA, PR #6 fusionado |
| AB30 DISCOVERY | [Informe](AB30_DISCOVERY_20261022/reports/DICTAMEN.md), [ledger](AB30_DISCOVERY_20261022/reports/LEDGER_D01_D30.md) | 30 contrastes y 6 auditorías; la optimización de subtipos basta como rival fuerte; sin 2/3; bruto en ZIP externo | ARCHIVADA_EXPLORATORIA, PR #7 fusionado |
| AB45 BEIJING | [Dictamen](AB45_BEIJING_20261022/DICTAMEN.md), [script](AB45_BEIJING_20261022/run_campaign.mjs), [observaciones semanales](AB45_BEIJING_20261022/weekly_observed.json) | 12 estaciones físicas y 209 semanas, 45 condiciones adaptativas de validación y un solo test cronológico de 39 semanas; `COSI_PROXY` NO equivale a COSI ni a MHU; test consumido | OBSERVACIONAL_EXPLORATORIA. Trasplante selectivo del antiguo PR #5, sin sobrescribir `README` ni priors históricos |

## Ramas abiertas, NO integradas

| PR | Motivo de mantener pendiente |
|---|---|
| [#8 — AB30 DRIFT](https://github.com/GalexY3/proyecto-LARP/pull/8) | Código y CSV resumen presentes; incorporar raw por semilla, cotejar SHA y probar clon limpio |
| [#9 — AB45 DRIFT](https://github.com/GalexY3/proyecto-LARP/pull/9) | En B02–B09 el freeze fue local, no previo en GitHub. No corregir retrospectivamente esa carencia; incluir raw íntegro y prueba limpia |
| [#1–#4, y #5 antiguos](https://github.com/GalexY3/proyecto-LARP/pulls) | Dependencias entre ramas, cambios de README y ledgers, conflictos con `main`; rescatar solo aportaciones no duplicadas en nuevos commits selectivos |

## Línea de investigación actual
No se ha acreditado superioridad computacional de MHU ni descubrimiento interno 2/3. El **DRIFT exploratorio** plantea selección de información según función de pérdida, monitorización de daño con etiquetas tardías y distinción entre etiquetar para estimar riesgo o para aprender. Estos problemas tienen trabajos previos competentes y **todavía no han sido validados externamente**.

## Reglas de mantenimiento
- [Política de integración y reproducibilidad](../docs/INTEGRACION_Y_REPRODUCIBILIDAD.md).
- [Metodología AB 3.2.1/O1/O2/O3](https://github.com/GalexY3/Metodologia-AB).
- Preservar priors negativos, reparaciones y commit SHA. Nunca reetiquetar exploración como confirmación por el merge.
- Ningún ZIP de conversación se presupone accesible desde un clon del repositorio. Los resultados brutos no depositados se indican como **pendiente de archivado**.
