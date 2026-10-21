# LARP · AB 3.2.1 · branching dinámico de 12 ciclos (21-10-2026)

## Qué puede y qué no puede demostrar

12 decisiones científicas sucesivas, 12 clases de evidencia relacionadas (no 12 estudios independientes). **Todos los cálculos nuevos se clasifican como exploratorios**, incluidos los mundos de test apartados de los del ajuste. No se ha probado ni reconstruido exactamente el algoritmo Scale3D original mediante múltiples semillas. El generador `local_derived` es una **aproximación NUEVA**, inferior al CVT en el ejemplo N=512; no atribuir su comportamiento al original. El control `cvt_type` es Lloyd por tipo, **NO es el algoritmo original Multi-Class Blue Noise de Li-Yi Wei**. Su código histórico no se ejecutó.

Se preservan tres coordenadas auténticas, una por RANDOM/LOCAL/MHU a N=4096, y seis CVT sintéticos N=4096 (tres refinados). Se comparan por cobertura, muestreo de campos Fourier, un MLP pequeño con cinco canales, sensibilidad a perturbaciones y espectro finito. El conjunto de mundo/queries no sustituye geometrías originales independientes; no existe inferencia entre generadores originales ni validez externa. La supresión de S(k) en 80 modos no prueba hiperuniformidad asintótica.

## Documentos

- `docs/00_DICTAMEN_BR12.md`: conclusión conservadora y límites.
- `docs/01_LEDGER_AB_C01_C12.md`: preguntas, rivales, hallazgos y AB-DECIDE secuenciales.
- `docs/02_PRIORS_NUEVOS_BR12.md`: entradas BR12-L09–L15 para el ledger acumulativo.
- `docs/03_EXECUTION_PROVENANCE.json`: SHA de los scripts ejecutados antes de las adaptaciones de rutas.
- `MANIFEST_SHA256.json`: hashes de contenidos; regenerado en cada paquete.
- `logs/`: salida de ejecución, incluida prueba lenta que agotó tiempo de CPU y no constituyó evidencia completa.

## Reproducibilidad

Requiere Python 3.10+, NumPy, SciPy, Matplotlib y PyTorch (MLP). Se preserva `src/br30_previous.py` como algoritmo del simulador sintético BR30 y las tres geometrías originales como NPZ. Utilizar `OPENBLAS_NUM_THREADS=1` para evitar problemas de rendimiento. Ejecución en orden:

```bash
python src/dynamic_research.py construct --first 1201 --last 1212
python src/dynamic_research.py coverage --first 1201 --last 1212
python src/fast_4096.py
python src/refine_cvt.py
python src/compare_4096.py
python src/bandwidth_budget.py
python src/access_controls.py
python src/learned_specialists.py
python src/dropout_4096.py
python src/spectrum_control.py
python src/build_dossier.py
```

**Importante:** `src/build_dossier.py` lee también `logs/coverage.json`, que se preserva en el paquete; el comando de `coverage` imprime el resumen y puede redirigirse allí. No borre `logs/coverage.json` antes de reconstruir el informe. Los NPZ nuevos originales no son datos biológicos, sino patrones construidos computacionalmente.

## Gobernanza y procedencia

- LARP: https://github.com/GalexY3/proyecto-LARP (privado)
- AB: https://github.com/GalexY3/Metodologia-AB (privado)
- Prior art: Li-Yi Wei, *Multi-Class Blue Noise Sampling*, SIGGRAPH 2010 — https://www.liyiwei.org/papers/noise-sig10/ ; código original: https://github.com/1iyiwei/noise/tree/master/RainbowNoise
- Código del generador derivado (antes de los primeros contrastes nuevos; compilación/dos muestras piloto anteriores): commit `56b38d13ae6b9e3c02b03021961a922772128b50`.
- Prerregistro metodológico dinámico anterior a la nueva batería: commit `aff298281e3b9efab361964cf068a95c8c0b1163`.

**AB-DECIDE**: consumidos los 12 primeros ciclos. No activamos los 12 adicionales, puesto que no han aparecido ventajas originales frente al baseline refinado que justifiquen una ampliación. Falta la implementación fiel de Wei y nuevas realizaciones del optimizador Scale3D original.
