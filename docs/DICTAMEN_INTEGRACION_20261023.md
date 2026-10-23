# Dictamen de saneamiento e integración LARP — 23-10-2026

**Objetivo:** conservar resultados útiles, evitar merges que reescriben genealogías de evidencia, identificar el nivel de prueba y hacer navegable `main`. Decisiones realizadas directamente en los repositorios privados vinculados. **Un merge no equivale a validación científica**.

## Fusiones confirmadas

| Repositorio | Origen | PR | Commit de merge | Selección |
|---|---|---|---|---|
| LARP | research/ab30-intensive-20261022 | #6 | `95bf0b1969dd676440c336aa2f3a7ec04db81dc9` | Archivo exploratorio de 30 contrastes; no MHU certificada |
| LARP | research/ab30-novelty-20261022 | #7 | `94efc458d88099942d9608b4e7ffb21209bd9bd1` | Falsación y comparación con optimización por tipos; 2/3 no acreditado |
| LARP | integration/curated-evidence-20261023 | #10 | `6ece73bb3b4a950f6fa867486a8234c888a6a8ed` | Trasplante de nueve archivos de Beijing + índice/política/README, SIN rama histórica divergente |
| Metodologia-AB | integration/ab-observatory-20261023 | #7 | `17cfb1478ededffe8b827066e6d85aeef996bab4` | Observatorio M027–M035 con propuestas; README distingue norma de propuesta |
| Metodologia-AB | O3 adoptado por commit en main | — | `bf4beaf6ab23a5b5f9425407abd12b17e2aad269` | Anexo normativo de bucles DRIFT (adopción ≠ eficacia validada) |

## Auditoría de integridad de trasplante

Los nueve blobs en `research/AB45_BEIJING_20261022/` coinciden con los Git SHA originales de la rama `research/ab45-beijing-real-20261022`. Comprobados explícitamente: `campaign_results.json` (`07a314a2c7c4f348e0b4c9d86f2b9f0b2e8d7542`) y `weekly_observed.json` (`47d9cd98122cb264bb2012a2580a9213f3369c68`). No se reescriben series, instrumentos ni cifras. No se ha reproducido computacionalmente de cero la campaña.

En `Metodologia-AB`, el observatorio de la rama antigua contenía **exactamente** el texto original de `main` como prefijo y agregaba las propuestas posteriores: la actualización no borró observaciones precedentes. Documento incorporado git blob `005d1b195223f2847320e6e14f37a9d9524ea66d`. Las propuestas M031, M032–M033, M034 y M035 permanecen etiquetadas como propuestas, no nueva versión central de AB.

## PR cerrados sin pérdida de ramas

- LARP #5: **SUPERSEDED**, sus nueve archivos fueron trasladados íntegramente por PR #10.
- LARP #1–#4: **CLOSED UNMERGED / ARCHIVED IN BRANCH**. No se eliminaron las ramas ni sus códigos, que aún contienen material experimental no integrado. Se evitaron los diffs acumulativos contra un `main` ya divergente.
- Metodologia-AB #1–#5: **SUPERSEDED**, sus contenidos de observatorio/documentos M027–M035 ya están conservados en `main` por PR #7. Se cerraron sin segunda fusión.

## Trabajo pendiente, no declarar solucionado

**LARP #8**, AB30 DRIFT: documentos, CSV y código comprimido presentes, pero raw por semilla fuera de GitHub. Falta incorporar sin falsear fechas, chequear hashes y replay limpio. B04 conserva una reparación de manifiesto.

**LARP #9**, AB45 DRIFT: 45 ensayos reportados, solo B01 con congelación GitHub previa. B02–B09 tuvieron congelación local, infracción O3 no reparable retrospectivamente. JSON brutos y ledger íntegro permanecen en ZIP fuera de `main`. No se ha ejecutado un clon limpio.

**LARP #6/#7 ya fusionados:** tienen algunos resultados resumidos y código, pero siguen pendientes de incorporar brutos por semilla y comprobar un clon limpio. Mantener estado ARCHIVED_EXPLORATORY incluso en `main`.

**Beijing:** observaciones semanales derivadas incluidas, CSV horarios originales externos referenciados por hashes, no vendorizados. Un único test cronológico consumido y no repetible como holdout limpio tras la selección. No equivale a despliegue real ni certifica COSI/MHU.

## Hoja de ruta técnica

1. Congelar `research/INDEX.md` y `research/CAMPAIGNS.json` como inventario canónico; actualizarlos tras cada decisión.
2. Recuperar desde artefactos originales los JSON por semilla ausentes en GitHub, con manifiesto de hashes y procedencia retrospectiva EXPLÍCITA.
3. Añadir una prueba de clon limpio reproducible para campañas seleccionadas; reportar qué dependencias y datasets externos faltan.
4. Para nuevas investigaciones aplicar AB3.2.1/O1/O2/O3 y no abrir validación externa sobre datasets consumidos. Ningún hallazgo es 2/3 por integración.
5. No abrir otra batería sintética antes de identificar información nueva o un control profesional no ejecutado.

El informe es **auditoría de gobernanza/documentación**, no un resultado experimental nuevo.
