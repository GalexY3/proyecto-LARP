# Suplemento prospectivo de dos cadenas no iniciadas

9 de octubre de 2026. Decisión dentro de la autorización del investigador para continuar y desviarse justificadamente. La ejecución v1 se cierra como `BUG_INVALID` de infraestructura: diez cadenas completas, dos `NOT_RUN`. No se modifica ni reanuda su cápsula ni se reclasifica como ejecución original completa. La revisión independiente y el fallo se conservan, incluida la puerta que no detectó la carrera de archivos.

## Incidente y oportunidad de recuperación

Windows denegó `os.replace(active_trajectory.json)` cuando el supervisor leía ese archivo. Falló antes de llamar `run_chain` para g1103/seed1/cycle3. El estado anterior ya era inactivo; las diez trazas anteriores completaron190 propuestas. Ninguna propuesta ni RNG de cadena se inició para las dos filas restantes. La recuperación depende sólo del incidente de infraestructura; no se selecciona por rendimiento o aceptación. Se decidió antes de interpretar los endpoints.

Gasto: calibración2,4167939 s + preparación1,6772587 s + ejecución fallida87,9074383 s = **92,0014909 s**. Saldo del presupuesto original360 s: **267,9985091 s**. El suplemento reserva como máximo50 s de ese saldo, dos cadenas con harddeadline20 s y reserva final1 s. No hay otro presupuesto360, recalibración ni transferencia entre cadenas.

Allowlist y orden exactos: g1103/seed1/cycle3, después g1103/seed1/swap2. Conserva cap190, semillas originales `[20261009,9924,1103,1,1/0]`, sampler, evaluator, referencias, guardas, radii y recomputación completa. No repite las diez cadenas ejecutadas. Otro fallo cierra el suplemento sin retry; no se inicia una tercera intervención.

## Reparación y verificación

Un supervisor nuevo publica mensajes inmutables con marcadores de disponibilidad creados después de cerrar cada archivo. El lector sólo abre mensajes completos. No se reemplazan rutas compartidas entre lector y escritor; se evita la carrera observada. Verificar PID/PPID real y entorno mediante el mismo lanzamiento CPython base/venv. Probar el supervisor con workers stdlib sin importaciones científicas, tanto finalización como corte por tiempo. Congelar código y allowlist antes del suplemento.

## Interpretación

Auditar primero las diez cadenas como `PARTIAL_ONLY`; después las dos nuevas y la colección combinada. Esta última será **AMENDED_EXPLORATORY_OPERATOR_DIAGNOSTIC**, con procedencia de ambos lotes. Nunca sustituye al estado inválido de v1.

Aceptados y distancias por190 propuestas usan el mismo mecanismo científico. Los tiempos pueden cambiar por I/O y lote temporal: informar ambos lotes y considerar las razones por segundo descriptivas, sin atribuir limpiamente al operador el cruce de la puerta2×. Los umbrales de accesibilidad/viabilidad por aceptados y Hamming se mantienen como criterios de ingeniería. Sin p-values de propuestas dependientes, sin entrenamiento, sin actualización de H1–H6/C/H-R.
