# LARP AB75 — campaña AB con 30 + 45 ciclos

**Resultado:** 75 expedientes A–J, 14 bloques con DRIFT y BRANCHING, 150 ejecuciones E/G corregidas, 150 versiones previas archivadas como inválidas por filtración de preprocesado. **CT2 12→10/100; N1 nuevo 1 (provisional), N2=N3 0.** La primera tanda 30 no obtuvo 2/3, por eso se utilizó la autorización adicional de 45.

Abrir primero [Dictamen](reports/DICTAMEN.md), [A–J de cada ciclo](ledger/LEDGER_AJ_75.md), [resumen CSV](reports/SUMMARY_75.csv), [lectura por bloque](reports/BLOCK_READOUTS.md), [CT2](reports/CT2_TRAJECTORY.json) y [auditoría](reports/AUDIT.json). Los resultados individuales E/G están en `results/C##_E.json` y `results/C##_G.json`, con una trayectoria de muestras por resultado. `results_invalid_population_scaling/` guarda los 150 anteriores que NO deben usarse para reivindicar hipótesis sin filtración.

La fuente fuente v1/v2 `src/engine.py`/`src/engine2.py` era defectuosa, los motores R1 `src/engine3.py`/`src/engine4.py` usan centros/escalas fijos. Código reproducible: `src/design.py`, `src/run_block.py` y `src/finalize.py`. Ejecutar en Python con numpy, scipy, statsmodels, matplotlib (versiones en requirements). E/G usan las mismas poblaciones históricas, y las intervenciones de drift/MNAR son simuladas.

Los 75 contratos se almacenan en `prereg/`. Antes de cada bloque el contrato se había comprometido en GitHub y el SHA de fuente corregida se congeló antes de R1, pero los scripts fuente y los datos brutos completos pueden haber sido copiados al remoto retrospectivamente; **no** afirmar cumplimiento O3 de bytes pre-run íntegros ni replicación externa. El ZIP local tiene `MANIFEST.json` de todos los hashes.

**Pendiente:** prueba desde clon GitHub limpio y benchmark serio con datos prospectivos que no contengan el objetivo completo accesible en la simulación. No hay originalidad 2/3 acreditada. Para siguiente bloque **SOLICITO BRANCHING 30 CICLOS**.