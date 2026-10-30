# ERRATA-02 — three CSV Git blob mismatches in transfer

Fecha 2026-10-30. Auditoría de identidad **GitHub vs archivos locales originales** tras el commit `56f4c78df64098135f4de40a37ef0f4639e8a75b`.

35/38 paths matched the original Git blob bytes. Three CSV derived from original ZIPs **did not**. The ZIP files themselves are byte-identical and remain the archival authority; no scientific data has been changed.

| Path | Original expected Git blob | Initially stored blob |
|---|---|---|
| `research/AB_VISION_20261029/CONTRASTS_CLUSTER_BOOTSTRAP.csv` | `efbd9c333292154033ec98beb755c7f103c310bc` | `025921c3611465ff5665fe223634be2068f14d51` |
| `research/AB_VISION_20261029/MSE_TEST_TABLE.csv` | `bd4233d3fe8fd73df6123219313dc56360e46e4e` | `c0d5f9de3b27bc58baf5ddb4941aac1191fcbca9` |
| `research/AB_VISION_20261029/C02_MEANS.csv` | `fb5e7b307cb3276c6161213cfa156bf6d5bc52f8` | `3181fac9d9cae9cdaaa083f0dcf6e1520d7e06c0` |

Probable causa: transferencia de archivos CSV usando un lector interpretativo, que no garantiza preservar todos los bytes. **No usar comparación de valores para declarar igualdad binaria.**

REPAIR autorizado para mover SOLO estos tres paths a blobs nuevos creados mediante base64 original, manteniendo el resto del árbol y las evidencias. Comprobar Git SHA y SHA256 contra ZIP antes de cerrar. No reescribir la versión errónea del historial; dejar ambos commits trazables. Fallo de portabilidad, no de validez de los resultados C01/C02.
