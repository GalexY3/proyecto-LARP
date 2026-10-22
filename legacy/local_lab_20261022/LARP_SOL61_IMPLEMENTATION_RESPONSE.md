# Entrega de implementación LARP v0.1

**Repositorio implementado y probado en `C:\Programación\LARP`. El piloto copy se ha detenido conforme al contrato: XOR no aprende pese a acceso completo. No hay evidencia obtenida sobre utilidad funcional de MHU ni actualización de sus priors.**

## 1. Árbol y comandos

```text
configs/       contrato y siete presets inmutables con hashes
src/larp/      geometría/certificados, grafos, tareas/puertos, G/T/F,
               baselines, trainer/runner/CLI, intervenciones, AB/reportes
tests/         163 verificaciones unitarias e integraciones acotadas
docs/          SPEC_AUDIT, ADR, SCIENTIFIC_DEVIATIONS, AB_PRIORS,
               IMPLEMENTATION_STATUS y NEXT_EXPERIMENT
scripts/       install.ps1, entorno CPU con dependencias bloqueadas
runs/          manifests, mundos, curvas y checkpoints locales de ambas series
artifacts/     certificados, puertas, logs/JUnit, CSV/PNG, diagnósticos y AB
```

Desde la carpeta del repositorio, PowerShell:

```powershell
.\scripts\install.ps1
$p = '.\.venv\Scripts\python.exe'
& $p -m larp test
& $p -m larp validate-geometry --N 400 --seed 1101
& $p -m larp calibrate --execute --resume --directory runs/series_cli_exitfix/calibration
& $p -m larp smoke --execute --resume --directory runs/series_cli_exitfix/smoke
& $p -m larp pilot --task copy              # dry-run:12corridas, no training
& $p -m larp pilot --task copy --execute    # bloqueo correcto: puerta XOR fallida
& $p -m larp analyze --output artifacts/AB_initial.json
& $p -m larp resume --run runs/series_cli_exitfix/calibration/copy_native_T_g9001_s9002_u205_lr0.003_causal
& $p -m larp report --run-root runs/series_cli_exitfix --output artifacts/report_current
```

Los comandos de suite posterior y sus requisitos están en README. No se ejecutan confirmaciones automáticamente. Para una nueva serie usar otra carpeta, conservar los archivos previos y congelar hashes; `--resume` mantiene el seed/orden. En este estado, el piloto no debe forzarse editando una puerta.

## 2. Implementado, ejecutado, pendiente

Implementados y probados: generadores MHU/HU y certificados finitos por clase/unión; kNN dirigido/Delaunay/Grid/RR/SW/Poisson; marcas y Hamilton; Hungarian; oráculos XOR/copy/fill8/resources; G/T/F con parámetros/invariancias correctos; daño sin reconexión, colapso de funciones completas, relocalización de funciones y escala con pesos congelados; trainer exact-resume; preflight causal, planes inmutables, selección de baseline/HPO, análisis jerárquico y reportes reales.

Ejecutados: instalación CPU, suite global, originalN400/g1101, calibración200 y cuatro XOR. También diagnóstico frozen en validación y repetición técnica completa tras corregir el código de salida CLI. Comparación nativa–shuffle funcional, fill, screens/HPO/confirmación y evaluaciones científicas de robustez/escala **NOT_RUN**, bloqueadas por falta de aprendizaje. Las ramas ambiguas C3/puertos parciales y otras condicionales permanecen bloqueadas.

## 3. Tests y certificados reales

**163 PASS, cero fallos/errores/skips,8.12s pytest.** Respaldos `artifacts/tests/pytest.log` y `junit.xml`.

MHU originalN400/g1101: primer intento, counts163/85/68/50/34, certificadoPASS por los cinco componentes y unión, separación mínima.3000000037. Variance ratiosR4/R5=.255–.354, unión.3125. kNN6 tiene2400arcos y una SCC; gradiente y Delaunay/traslación verificados. `artifacts/geometry/` contiene certificados, métricas y tiempos. Certificar esta muestra finita no demuestra una ventaja neuronal.

## 4. Tiempo, memoria y presupuesto

Calibración actual5warmup+200medidos: mediana32.6ms/update, p9034.8ms;16.29s de entrenamiento con validaciones periódicas, finalvalidation3.14s separada;RSS430.7MB. La suma registrada de entrenamiento de la serie actual es67.24s; el picoRSS muestreado430.97MB. La extrapolación conservadora a12copy×1000 es≈18.4min, **no medida**. El presupuesto nominal cabe, pero cero de sus12000updates se ejecutaron porque XOR cerró la puerta.

## 5. Errores y ambigüedades

SPEC_AUDIT clasifica contradicciones/ambigüedades científicas, omisiones operativas y decisiones conservadas. C3 no define inequívocamente su población de parejas; reubicación parcial puede colisionar roles/coordenadas; D4 carece de una acción exacta si se activa anisotropía sistemática; el modeloAB continuo puede ser singular ante residuos idénticos. Otras ramas secundarias no definen retiro pareado impar ni penalizaciónNMSE de query perdida. No se fabricaron correcciones científicas.

Se corrigieron errores de implementación antes de cierre: RR comparte puntosMHU/marcas shuffle; screen comparte mundos focales; native/shuffle se comprueba antes de training/test; se conserva checkpoint500; HPO usa grupos con peso igual; las extensiones conservan paneles16; resume protege evidencia; el wrapper CLI propaga código2. Esta última corrección sólo cambió entrypoint/test, y sus repeticiones conservan exactamente pesos, pairing y score/loss en cinco corridas (`artifacts/reproducibility_cli_fix.json`).

## 6. Resultado completo y STOP

No se llegó al piloto funcional. El diagnóstico XOR G, g1101/250updates/T16:

| Condición | init2101 | init2102 | Accesibilidad val |
|---|---:|---:|---:|
| Grid-G |48.046875%|50%|100%|
| MHU-G |51.7578125%|50%|100%|

Train accesible51.0254%,50%,51.4160%,50%, respectivamente. Umbral98%. Todas las losses son finitas y todos los ejemplos tienen caminos≤16. El resultado detiene interpretación del bloque/interfaz bajo este entrenamiento; G no ve marcas y estas corridas no estiman utilidad multicomponente. Todas las semillas y curvas están conservadas, incluidas las negativas.

En veinte casos frozen por modelo, invertir un bit remoto no cambia ninguna clase y produce cambios de logit del orden1e−8; gradientes de fuente del orden1e−13 frente a≈1e−2 en el receptor. Es diagnóstico posthoc de señal atenuada, sin nuevo entrenamiento/test; no prueba causal exclusiva ni posterior contraMHU.

## 7. Historial AB

`artifacts/AB_initial.json` y `artifacts/report_current/AB_history.json`: H1–H6=.70,.35,.25,.75,.20,.30, C=.25, todos **UNUPDATED**. Son marginales, no exclusivos. No se calcularon posteriors de arquitectura con certificados/smoke/calibración/diagnóstico; la inferencia implementada exige confirmación preregistrada completa y sensibilidad.

## 8. Siguiente acción permitida

Diagnóstico técnico acotado centralizado/directo/local frente a remoto, con reglas y techo fijados en `docs/NEXT_EXPERIMENT.md`, aúnNOT_RUN. Primero determinar si el bloque aprende XOR local y si la señal se pierde al aumentarhops. T32 no arregla una inaccesibilidad ausente; GRU o cualquier ajuste científico exige nueva versión/preregistro y una única modificación discriminante. No relajar certificados ni reintentar semillas hasta conseguir una victoria.
