# Priors acumulativos BR06-R (no sustituyen al ledger maestro)

| ID | Proposición | Evidencia a favor | Evidencia adversa | Grado/alcance |
|---|---|---|---|---|
| BR06-R01 | Generador auténtico Scale3D produce MHU finita también en N128 | C02: cuatro nuevas semillas y Fourier 3D mucho menor que LOCAL | Objetivo explícito; validate=False y tarea 2D; no demuestra HU asintótica | Observación finita verificada |
| BR06-R02 | La geometría MHU otorga mejor clasificación real | Ninguna victoria general | C04 MHU 94,94%, Sobol 96,11%, MLP píxel 96,78%; n=4 | Debilitada, no general |
| BR06-R03 | Cinco funciones sensoriales heterogéneas mejoran el aprendizaje | Hipótesis de complementariedad | C05 roles distintos empeoran MHU ≈1,56 pp respecto a mismas cinco funciones de intensidad | Refutada para este operador/dataset |
| BR06-R04 | La representación sensorial espacial puede incrementar robustez a rotación y ruido | C06 supera al MLP directo pixel en varios shifts | Baselines suavizados reducen la brecha; no está aislado efecto MHU | Abierta para otro dominio, confusión reconocida |
| BR06-R05 | MHU tiene robustez específica frente a LOCAL | C06 en alguna semilla | Medias LOCAL superiores MHU en rotación y ruido; semillas heterogéneas | No validada |
| BR06-R06 | Wei original disponible y ejecutado como baseline | Repositorio público confirmado | README VS2003, no binario ejecutado ni comparabilidad con N128 | BARRERA_DE_EJECUCIÓN, fuente localizada |
| BR06-R07 | MHU en 3D transferida por proyección 2D preserva todas sus ventajas | Fourier 3D finito fuerte | Reconstrucción y clasificación en 2D sin dominio MHU | Hipótesis debilitada para proyección |

Procedencia: `docs/01_LEDGER_AB06.md`, scripts `src/cycle*`, datos `data/C0*.json`; todos resultados exploratorios, NO Bayes factors. Conservar las entradas BR08-X01..X06 y BR30-F01..F10 previas.
