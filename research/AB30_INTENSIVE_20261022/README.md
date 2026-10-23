# LARP — Investigación AB30 intensiva (22-10-2026)

**30 contrastes exploratorios N01–N30 + tres auditorías adversariales AUD01–AUD03, no contadas en el cupo.** Protocolo AB 3.2.1 + O1 + O2. **No hay MHU certificada ni descubrimiento 2/3 acreditado.**

## Cronología inmutable

- Código congelado para B01–B03: commit 626b456891a11cf5228a75786afb1b577becf64c
- B01 geometría prerregistrado: 0a3b10d; resultados: c6e0ebe
- B02 integración prerregistrado: c4fcb09; resultados: b5921a6
- B03 reconstrucción prerregistrado: 9ef84ea; resultados: b13d87c
- Baseline de 64 píxeles añadido antes de B04: 47312001f898fecdc82365732160bf8a47ce486d
- B04 Digits prerregistrado: 64e6a7c; resultados: fa73974
- B05 grafo prerregistrado: 56b129e; resultados: 7e38734
- Auditoría externa AL CUPO, no externa al generador: prereg d9494f3; resultados 9f7f155

## Reproducibilidad

En Python 3.13 ejecutar desde esta carpeta:

```bash
python -m pip install -r requirements.txt
python src/replay_block.py B01
python src/replay_block.py B02
python src/replay_block.py B03
python src/replay_block.py B04
python src/replay_block.py B05
python src/build_ledger.py
```

El motor usa semillas en los manifests preregistrados B01–B05, genera archivos JSON por semilla y puede reconstruir el ledger A–J desde el CSV versionado. **No se ha verificado un clon limpio**.

## Archivos

- src/engine.py: motor congelado antes de cada etapa; src/replay_block.py: reproducir manifests.
- prereg/B01.json…B05.json: contratos con A/B/C y falsadores.
- results/B0x_summary.json: resultados versionados por bloque.
- results/RESULTS_30.csv: 30 comparaciones, medias, deltas e intervalos.
- reports/DICTAMEN.md: interpretación adversarial y limitaciones.
- reports/PRIORS_DELTA.md: priors acumulativos, sin borrar los históricos.
- src/build_ledger.py: produce reports/LEDGER_FROM_GITHUB.md con A–J.

## Límite archivístico

El conjunto completo de resultados individuales por semilla y el ledger extenso fueron empaquetados en la conversación como ZIP. Sus JSON íntegros **todavía no se han incorporado en esta rama**; para conservar el expediente completo hay que añadirlos, verificar hashes y ensayar un clon limpio. La rama es un registro primario versionado **parcial**, no debe presentarse como archivo íntegro ni como confirmación independiente. El SHA-256 del ZIP distribuido en la conversación figura en ARCHIVE_RECEIPT.md.

Los resultados se obtuvieron con layouts CVT y controles; sin Wei 2010 original, sin GNN aprendida, sin MHU asintótica, sin test ciego externo. Los seis tests dentro de cada bloque fueron prerregistrados conjuntamente; solo hubo branching entre bloques.
