# Reparación de portabilidad posterior a los resultados — NO ciclo adicional

El envoltorio `run_one_cell.py` congelado antes de resultados funciona en el directorio local original, pero importa el archivo principal desde una ruta relativa al layout del contenedor (`parents[1]/LARP_ROUTING_AB30_20261030`). Esto **impide su ejecución directa desde un checkout limpio de GitHub**. Es una deficiencia O2 del paquete, no un error en la simulación o una alteración del resultado.

**Reparación posterior a la apertura del test:** `run_one_cell_portable.py` cambia únicamente esa resolución de importación por `Path(__file__).resolve().parent`, permitiendo colocar el envoltorio en la misma carpeta GitHub que `learned_followup.py` y `ab30_functional.py`. No se cambian funciones de medición, pesos, seeds, modelos, benchmarks, umbrales ni procesado de outcomes. Esta corrección NO era parte del freeze preregistrado y se marca POST_OUTCOME_PORTABILITY_FIX.

Se ejecutó la celda `3011 low` con el envoltorio portable en el entorno local; coincidieron exactamente todas las salidas no temporales y no relacionadas con la huella del propio envoltorio (`elapsed_sec`, `wrapper_code_sha256`). El resto de las nueve celdas tiene doble ejecución exacta bajo el envoltorio original, descontando `elapsed_sec`. **CLEAN_CLONE_NOT_VERIFIED**; tampoco demuestra independencia científica.
