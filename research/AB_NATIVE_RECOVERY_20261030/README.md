# LARP — recuperación N400: puerta de identidad binaria (2026-10-30)

Estado: INSTRUMENT_READY, NATIVE_BYTES_NOT_READ, NO_SCIENTIFIC_CYCLE_CONSUMED.

Esta rama añade un verificador de solo lectura de seis NPZ nativos originales del repositorio y un exportador privado bit-exacto. El script es research/AB_NATIVE_RECOVERY_20261030/verify_and_export.py.

Se han fijado seis SHA de objeto Git del árbol original, comprobados contra los metadatos/certificados del repositorio. A diferencia del exportador anterior, el script **rechaza** un archivo reconstruido que preserve coordenadas pero cambie los bytes NPZ. Compara además los SHA256 de arrays, etiquetas, cuotas, dominio y metadatos, y rechaza sobrescrituras de exportaciones previas.

Ejecución local de prueba **sin originales**: `python verify_and_export.py --self-test`; PASS sobre una geometría sintética, test de sustitución de objeto Git, alteración de certificado, sobrescritura y recuperación float.hex bit-exacta. SHA256 del código `b1c0b1dbf44e1e5e7200595388084337f2bc16aa74ecfbb6c5bca0c8df6d4136`, blob Git `6a5cc2c3c7cd473c36c2b5c2705ff92303b51b9f`, commit `febf473e406c8e0854a210a7dd1eb4ad105d956c`.

## Uso para ejecutor autorizado con checkout privado

Después de posicionarse en la raíz de la rama y disponer de NumPy:

```bash
python research/AB_NATIVE_RECOVERY_20261030/verify_and_export.py --self-test
python research/AB_NATIVE_RECOVERY_20261030/verify_and_export.py --root .
```

Solo si el segundo comando confirma SIX_NATIVE_BLOBS_VERIFIED y count=6, ejecutar con `--write`. Los resultados privados se crean bajo research/AB_NATIVE_RECOVERY_20261030/private_exports, sin sobrescribir originales. No publicar datos fuera del repositorio ni habilitar CI. Si no hay acceso a los seis NPZ, informar bloqueo sin simular éxito.

## Puerta Wei y evaluación posterior

El comparador de Wei es el código **original** en 1iyiwei/noise, commit 0d1be2030518517199dff5c7e7514ee072037d59, target DartThrowing. Acceso al código C++ y CMake: confirmado. Compilación, prueba de humo y benchmarks: NO EJECUTADOS. Datos de cinco bandas ópticas auténticas: NO DESCARGADOS. No equiparar PoissonDisk con Wei. El siguiente estudio funcional requiere originales verificados, comparador competente, datos independientes y contrato AB A–J congelado antes de outcomes.

## Contabilidad rigurosa

Nuevo bloque autorizado: **10 AB-R, condicionado a desbloquear evidencia original**. Ejecutados científicos en este bloque: **0**. Test técnico de preparación: 1, no computa. Saldo: **10**. DRIFT hacia gate de instrumentación; STOP_LOCAL cuando no puede recuperarse la geometría. Las veinte verificaciones históricas N01–N20 no deben repetirse como ciclos nuevos.

No se ha modificado main. CLEAN_CLONE_NOT_VERIFIED. Informe original de contexto: research/AB_NATIVE_AUDIT_20261030/FINAL_RECEIPT.md.
