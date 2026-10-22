# Suplemento Grid y queries: resultado de la ejecución

Fecha 2026-10-08. `sampling_grid_supplement_v1` completado sin alterar geometría.py ni las series previas. Es una extensión post hoc, congelada antes de calibración, construcción o nuevos scores; no una confirmación independiente de MHU. Código nuevo `src/larp/sampling_grid.py`, configuración `configs/sampling_grid_v1.json`, SHA-256 canónico `8aabee3c054b9b3325e8a7390388888df98ea1546f0a2918bce7ca7a810419cb`.

**576/576 celdas completas:** cuatro familias × tres realizaciones × dos marcas × tres estimadores × dos bandas × dos niveles de ruido × dos estratos de queries. **216 celdas aligned** de las tres familias previas se reprodujeron con hashes de predicción y MSE idénticos a sus registros v1. Las **360 celdas adicionales** incluyen Grid y queries continuas; reutilizan el banco de 128 campos por banda y no constituyen 360 nuevas réplicas independientes. Grid aporta tres asignaciones de marcas sobre **una misma rejilla de coordenadas**.

## Construcción y presupuesto medidos

La calibración utilizó Grid9005, conteos 163/85/68/50/34 y el `relabel_geometry` existente, con test_only, un reinicio y sin evaluar MSE de campos. Se midieron primero 1.000 propuestas y, puesto que la extrapolación de 10.000 era inferior a cinco segundos, 10.000 propuestas. El coste sin certificado fue 0,01781/0,16813 s, equivalente a 17,81/16,81 μs por propuesta; los certificados separados tardaron 0,20513/0,20567 s.

La regla congelada utiliza el ritmo **más lento** observado, tres millones de propuestas y treinta certificados, más creación de tres rejillas, con factor de seguridad dos para todos esos costes. Estimación conservadora **119,21 s <180 s**, por lo que se autorizó la construcción fuerte. No se escogió presupuesto mediante calidad de interpolación ni se incorporó la coloración técnica de calibración como baseline.

Se invocó el presupuesto original de 100.000 propuestas por intento y hasta diez reinicios para cada semilla 1101–1103, sin modificaciones de objetivo, RNG, programación térmica o criterios. Las tres coloraciones pasan su admisión de componentes en el intento cero, después de **100.000 propuestas completas cada una**. Se conservan sus candidatos/records y los resultados de calibración separados. Los tiempos por coloración fueron 1,851/1,821/1,833 s, incluida certificación. Tiempo de construcción total **5,518 s**; evaluación **3,362 s**, inferior a su techo separado de 30 s; ejecución total **9,770 s**, incluyendo calibración y escrituras. RSS máximo muestreado de evaluación: **100.175.872 bytes**. La figura se renderiza después como operación de presentación separada y su tiempo queda en `plot_manifest.json`.

La admisión Grid corresponde a los criterios originales de balance de componentes, no a una afirmación de mosaico aviar ni de unión desordenada: el sustrato de coordenadas es deliberadamente cristalino. No se cambiaron conteos a 80/80/80/80/80 ni se aplicó una subrejilla exacta reservada para ese caso distinto.

## Resultado adversarial

La candidata aviar conserva su ventaja frente a este Grid balanceado para los decoders locales y estos campos, también con queries continuas. **El oracle-band cambia el ranking en fine:** Grid supera las dos familias aviares y MHU nominal. Las candidatas full y local siguen próximas; esta tanda tampoco identifica una ventaja específica de MHU.

La tabla muestra MSE macro **native, queries continuas, σ=0,1**; menor es mejor. El CSV y JSON incluyen todas las bandas/ruidos/queries/estimadores y los signos adversos, sin seleccionar semillas ni borrar condiciones.

| Familia | NN smooth | Kernel smooth | Oracle smooth | NN fine | Kernel fine | Oracle fine |
|---|---:|---:|---:|---:|---:|---:|
| MHU nominal | 0,205379 | 0,154805 | 0,002405 | 1,024080 | 0,953827 | 0,131039 |
| Aviar full | 0,135922 | 0,046185 | 0,001987 | 0,772821 | 0,608785 | 0,138230 |
| Aviar local | 0,132412 | 0,047933 | 0,001987 | 0,752017 | 0,607375 | 0,136474 |
| Grid balanceado | 0,188337 | 0,130278 | 0,002230 | 0,972975 | 0,886270 | 0,128437 |

Grid native kernel smooth cambia de 0,121335 aligned a 0,130278 continuous; en fine cambia de 0,869012 a 0,886270. La interfaz importa y ambos estratos se conservan. La ventaja local aviar frente a Grid aparece en ambos, de modo que esta ganancia local no se explica exclusivamente por la coincidencia exacta de queries y nodos Grid. No basta para adjudicarla a ondas largas: el objetivo de balance Grid sólo controla pocos modos espectrales y no reproduce la separación homotípica aviar.

Para oracle fine con σ=0,1 y queries continuas, full native 0,138230 frente a shuffle 0,129292, local native 0,136474 frente a shuffle 0,128947 y Grid native 0,128437 frente a shuffle 0,130875. Se mantiene el contraejemplo de que marcas nativas aviares pueden perjudicar un decoder global competente bajo otra banda/ruido. El conocimiento exacto de banda y ruido está disponible para todas las familias del oracle y constituye información privilegiada del benchmark, no una capacidad neuronal universal ni comunicaciones igualadas con los decoders locales.

## Alcance y siguiente decisión

El baseline fuerte de Grid bajo su objetivo congelado sí se ejecutó; no queda un rival omitido por coste. La rejilla no necesita optimizar posiciones y ese ahorro es parte de su coste real. Esto no acredita que esta coloración sea la mejor asignación posible de los cinco canales sobre Grid: un objetivo que iguale exclusión/distancias/vacíos sería un contraste distinto y debe fijarse en otra versión.

Las diferencias de asignaciones sobre Grid no son tres realizaciones independientes de X, y los mundos/queries/bandas siguen compartidos. Las medias/SD de tres realizaciones son descriptivas, sin p-values ni posterior de arquitectura. No se entrenó ninguna red, no se abrió XOR ni se actualizaron H1–H6.

La próxima decisión de investigación debe distinguir: conveniencia de un decoder local y cobertura de sensores, espectro de los campos, condicionamiento/aliasing del decoder global, y eventual procesamiento recurrente. Un rival que iguale las estadísticas locales de canales continúa siendo necesario antes de reclamar causalidad de multihiperuniformidad. Este resultado acota la utilidad aviar a determinadas condiciones, en vez de validarla como ventaja universal.

## Artefactos y comandos

`artifacts/sampling_grid/v1/` contiene preregistración, calibración TEST_ONLY, tres geometrías balanceadas, construcción/records, queries/hash, `evaluation.json` con 576 celdas, `summary.csv`, `results.json` y registro de pruebas. Las coordenadas de queries continuas se fijaron con SeedSequence `[20261008,7814]` antes de sus scores.

![Todas las familias y marcas con ruido .1, ambos estratos de queries y tres decoders](C:/Programación/LARP/artifacts/sampling_grid/v1/sampling_grid_MSE.png)

La figura se inspeccionó visualmente; muestra medias/SD de realizaciones, no intervalos inferenciales de geometrías independientes para Grid. Su script `render_results.py` y manifest registran hashes de entrada/salida y no calculan nuevos scores.

```powershell
.\.venv\Scripts\python.exe -m larp.sampling_grid --dry-run
.\.venv\Scripts\python.exe -m larp.sampling_grid
.\.venv\Scripts\python.exe -m pytest tests/test_sampling_grid.py -q
```

**Siete pruebas pasan**, JUnit `test_sampling_grid.xml`: denominadores/reutilización, RNG de queries continuas, coincidencia Grid/aligned con conteos reales, estimación conservadora que utiliza el ritmo lento y que impide MSE ante rechazo de presupuesto, y selección inequívoca de celdas originales por estimador. Las series anteriores y el código científico existente permanecen intactos.
