# LARP — AB30 Drift, 23 octubre 2026

**30 contrastes completados (T01–T30)** en cinco bloques adaptativos y una auditoría prospectiva adicional AUD01 no contada. **Originalidad 2/3 NO acreditada**; no se ha confirmado la superioridad de AB ni un efecto MHU. La investigación se desvía de geometría MHU a **selección de información, error correlacionado, coste de características y drift relevante para la tarea**.

## Índice
- [Dictamen consolidado](REPORT.md)
- [Ledger por ensayo A–J, índice GitHub](LEDGER_30_INDEX.md). El ledger íntegro A–J y raw JSON por semilla están en el ZIP entregado en la conversación.
- [Tabla de 30 resultados](results/AB30_SUMMARY.csv) y [resultados de cada bloque](results)
- [Priors acumulativos nuevos](PRIORS_APPEND.md) (no reemplazar priors LARP anteriores).
- [Auditoría archivística y prueba de proyección](ARCHIVE_AUDIT.md)
- [Freeze fuente original y referencias](SOURCE_LOCK.md)
- Prereg B01/B02, gzip+base64; B03 en texto con hash; B04 inicial invalidado y nuevo freeze B04_REPAIR; B05 en texto con hash. Revisar historia de commits, no reescribir retrospectivamente.

## Recuperar motor
En este repositorio hay cinco partes consecutivas de `src/engine.py.gz.b64.part1` a `part5`. Concatenarlas **sin separadores**, añadir el relleno terminal de dos caracteres iguales, decodificar Base64 y descomprimir gzip. Resultado exacto: `src/engine.py` SHA256 `867e75309dfa81c8568bb2360d4cb4909560a338d7f16a587d03bba877f1deb6`, congelado en GitHub antes de los ensayos bajo commit `0be4f7c`. Las partes del fuente se incorporaron posteriormente con verificación de identidad, NO como código publicado íntegro antes de ejecutar.

Entorno local: Python 3.13; NumPy 2.3.5, SciPy 1.17.0, scikit-learn 1.8.0. En el ZIP están los JSON exactos con semillas para reproducir `python src/engine.py prereg/B01.json results` y demás B02..B05. **CLEAN_CLONE_NOT_VERIFIED**. Los resultados completos JSON por semilla no están aún alojados en GitHub; conservar SHA256 del ZIP de conversación `b24a2adc36588589cc9dd783785907ff2e4f9cc53c51d4638a671282917059ab`.

## Lectura científica
- Tres bloques sintéticos comparten generador Gaussian-linear: no permiten inferir superioridad universal de selección robusta.
- Dos datasets reales públicos Diabetes y Breast Cancer Wisconsin con particiones repetidas: no son validación externa independiente.
- AUD01 muestra que igual cambio global de covarianza puede tener daño diferente dependiendo de proyección por predictor, una **identidad lineal conocida** y no 2/3.
- Derivación prospectiva: investigación de alertas de distribución orientadas al costo de decisión, con etiquetas tardías, ante controles robustos de change detection y datos externos.

Estado de gobernanza: rama privada y PR draft sin merge; source/ledger parcial accesible en GitHub y expediente completo ZIP. No declarar que GitHub contiene raw completo ni reproducción limpia comprobada.
