# LARP — 30 ciclos AB completos, 23-10-2026

**30 ciclos contables C01,C02,C03R,C04–C19,C20R,C21–C30; 2 INVALID preservados (C03,C20).** Seis bloques adaptativos con drift/branching real: diseño de muestreo → proxies → label-shift construido → riesgo de subpoblaciones → corrección del muestreo → cinco recontrastes internos. Protocolo AB 3.2.1/O1/O2/O3. **No descubrimiento 2/3, no confirmación externa.**

## Empezar aquí
- [Dictamen completo y limitaciones](reports/DICTAMEN.md).
- [Los treinta deltas de MSE redondeados](results/SUMMARY_30_ROUNDED.csv), más lectura individual de [B01](results/B01_READOUT.md), [B02](results/B02_READOUT.md), [B03](results/B03_READOUT.md), [B04](results/B04_READOUT.md), [B05](results/B05_READOUT.md), [B06](results/B06_READOUT.md).
- [Priors acumulativos nuevos](reports/PRIORS_DELTA.md), conservando todos los del repositorio.
- [Incidencias y erratas](errors/), incluidas C03/C20 invalids y reproducción B04 con cinco hashes idénticos.
- [Fuente y restauración](source/reconstruct_engine.py) + SHA256 [SOURCE_LOCK.json](SOURCE_LOCK.json). La fuente v1 comprimida en tres fragmentos se registró ANTES de ejecutar y el patch B02 se versionó antes de ese bloque.

## Comprobación de fuente
Desde una copia/clon con Python 3:
```bash
cd research/AB30_FULL_20261023/source
python reconstruct_engine.py
# source/engine_B01_original.py: SHA256 41a7ffe9...
# source/engine_B02_onwards.py: SHA256 20e0c44f...
```
Las dependencias están en [requirements.txt](requirements.txt). Los CSV de hipótesis originales están en `prereg/B01.tsv`...; B06 fue congelado como `prereg/B06_FROZEN.md` antes de ejecutar (seeds y signos); el TSV legible por máquina está en el ZIP.

## Estado archivístico transparente
**GitHub aún NO contiene los 32 JSON brutos por extracción/seed ni los 32 A–J detallados**. Permanecen dentro del archivo ZIP completo de la conversación `LARP_AB30_FULL_20261023.zip` con **119 entradas** y SHA256 **`e1617868cbae2c7cea4337ec2c776cc1372d51f43eb6b1b92487daa0405c5338`**. Incluye fuente editable, todos los manifests, datos por consulta, ledger de 32 A–J (30 válidos), gráficos, reparaciones, priors y hashes individuales. GitHub contiene summaries y las especificaciones originales antes de ejecutar. Este déficit O3 debe repararse con importación posterior explícitamente retrospectiva, no fingir resultados brutos GitHub previos.

B04 tuvo TSV local mal formado y se corrigió contra prereg GitHub previo; cinco resultados SHA idénticos. C03 y C20 INVALID no cuentan. Datos observacionales públicos empaquetados en sklearn previamente expuestos en LARP; label flips artificiales; doce nuevos splits de B06 solapan observaciones, no son un test externo independiente. **CLEAN_CLONE_NOT_VERIFIED.** No fusionar la rama antes de revisar archivo, fuente y reproducibilidad.

**Próxima evidencia que importa:** flujo externo con etiquetas realmente demoradas y métodos profesionales PPRM/active sampling, igualando presupuesto y coste. Otra tanda de Digits/Wine no prueba novedad.
