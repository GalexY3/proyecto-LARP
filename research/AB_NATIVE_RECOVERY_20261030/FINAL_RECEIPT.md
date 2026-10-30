# Recibo técnico de recuperación N400 — 2026-10-30

**HEAD previo:** cb27582f30ffa11c383a51bd143591eb04691bd5. `main` no ha sido alterada por esta campaña.

## Resultados efectivos
- Inspección directa de árbol privado GitHub: 6/6 blobs NPZ N400 presentes, tamaños entre 91.236 y 91.646 bytes, sus SHA Git fijados en verify_and_export.py.
- Obtención de bytes NPZ mediante los métodos disponibles del conector GitHub: **FALLIDA** (el contenido binario no es UTF-8); no se ha accedido a las coordenadas, ni verificado directamente sus hashes a partir de bytes locales en esta sesión.
- Descarga de código original de Wei: el repositorio, rama/commit y estructura C++ son legibles a través de GitHub; la descarga directa en el contenedor carece de conectividad DNS. **WEI_NOT_BUILT, WEI_NOT_RUN**.
- Verificador nuevo `verify_and_export.py`: SHA256 `b1c0b1dbf44e1e5e7200595388084337f2bc16aa74ecfbb6c5bca0c8df6d4136`, Git blob verificado idéntico `6a5cc2c3c7cd473c36c2b5c2705ff92303b51b9f`, commit `febf473e406c8e0854a210a7dd1eb4ad105d956c`.
- **SELF-TEST LOCAL PASS**: geometría sintética con 400 puntos, cuotas y bits float64; verificadas coincidencia de objeto Git, hash de arrays, metadatos, ida/vuelta IEEE-754, rechazo de objeto alterado, certificado alterado y sobrescritura. No es una prueba original N400.
- En el contenedor de ChatGPT la ejecución contra directorio `/mnt/data` termina con **FileNotFoundError** por ausencia de los seis NPZ. El error se conserva como evidencia de bloqueo, no se sustituye por fixtures sintéticos.

## Evaluación científica y presupuesto
El usuario concedió diez ciclos AB-R **condicionados prioritariamente al acceso a geometrías nativas, Wei auténtico y datos multibanda independientes**. **Ciclos científicos efectivamente consumidos: 0; bloqueados sin gasto: 10.** Una inspección técnica y un self-test son trabajo instrumental y no cuentan como experimentos A–J. No se han abierto outcomes ni se ha actualizado CT2, N1, N2 o N3.

**R5 / STOP_LOCAL:** no repetir contrastes proxy L01–L20 ni revisiones documentales N01–N20 solo para agotar presupuesto. El proyecto queda en `NEEDS_EXTERNAL_EXECUTOR` hasta que un equipo con acceso legítimo ejecute el verificador sobre los NPZ y entregue datos exportados y hashes originales. La tarea técnica para Windows está descrita en README.md y en el archivo de conversación EXECUTOR_TASK.md.

La exportación privada con `--write` solo se permite después de que todas las seis coincidencias de objeto Git y SHA de geometría pasen, y no permite sobrescribir un directorio no vacío. Se exige una nueva congelación AB A–J antes de evaluar rendimiento funcional. Código fuente de Wei https://github.com/1iyiwei/noise, commit `0d1be2030518517199dff5c7e7514ee072037d59`.
