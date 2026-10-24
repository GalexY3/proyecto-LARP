# LARP AB20 — QuixBugs y calidad de relaciones metamórficas

**Estado:** 20 ciclos AB A–J ejecutados, 20 algoritmos de retos Quixey con defecto externo, *no* incidencias reales de producción. Resultados E (3 selecciones de casos) y G (5 selecciones del mismo pool) tras reparación R1: chequeos superficiales **8/20**, metamórficos **13/20**, oráculo de referencia **20/20**. Controles negativos tras reparar E v1: 0 falsas alarmas en 480 ensayos programa/semilla/método.

## Navegación
- [Prerregistro de 20 contratos antes de experimentar](prereg/ALL_20.json)
- [Reparación de contratos erróneos, congelada antes del replay](prereg/REPAIR_R1_NEGATIVE_CONTROLS.md)
- [Dictamen detallado y grados](reports/DICTAMEN.md)
- [Los veinte registros A–J resumidos](reports/LEDGER_AJ_20_GITHUB.md)
- [Resultados E/G por programa](results/SUMMARY_20.csv)
- [Licencia del código QuixBugs](UPSTREAM_LICENSE)
- Registro de 1/3 permanente: `research/FINDINGS_1_3/LEDGER.json` de `main`, entrada `LARP-1-006`.

**Fuente externa:** [jkoppel/QuixBugs](https://github.com/jkoppel/QuixBugs/tree/4257f44b0ff1181dedaedee6a447e133219fcebf), commit `4257f44b0ff1181dedaedee6a447e133219fcebf`. Programas copiados semánticamente en Python con formato condensado; no idénticos byte a byte, conserva aviso de procedencia MIT. Motor original v1 SHA256 `7999be6213a8223ecd904ee39cee5816a215589275ca735a6c3b4f91cc3a608a`, motor reparado R1 SHA256 `db5dc62aa1c5fe2f08b3ac233582493808d75c95793ed87f6fdcbb05a70f8a57`.

**Deuda O3:** el código completo **solo tenía su hash comprometido** antes de ejecutar, no los bytes en GitHub; los archivos brutos E/G, E inválida y el ledger extenso se preservan en ZIP de conversación `LARP_AB20_QUIXBUGS_20261024.zip`, SHA256 `9c86fb7283d9a29006296ea0b4bf1c45fa91c18969d59404bae8d779b310e603` (80 miembros). 40 JSON de E/G se reprodujeron byte a byte bajo **el mismo entorno** tras extracción independiente; no hubo clon limpio remoto ni replicación independiente. Mantener PR en borrador hasta backfill remoto y verificación de paridad. CT2 final 11/100 ordinal, N1 acumulados seis explícitos, N2=N3 cero.
