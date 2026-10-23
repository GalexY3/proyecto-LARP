# AB30-TS — recibo verificable de archivo y estado final
Fecha: 23-10-2026.

**ZIP completo de la conversación:** `LARP_AB30_TIMESERIES_20261023.zip`, SHA256 `8f689d3a84158d2d24994a086b75eb03962131b839e236a447666cf9d0ca9492`, tamaño 390065 bytes, 183 miembros, comprobación `zipfile.testzip() == None`. Incluye 30 specs, 30 JSON de validación, 30 JSON de test, 30 auditorías enriquecidas, 30 vectores temporales observación/pronóstico/pérdida, 30 expedientes A–J, instrumentación, código, seis priors, figura y errores. El ZIP NO pertenece a este repo, pero **los cinco paquetes `results/raw/B01..B05_RAW.json.gz.b64` depositan retrospectivamente exactamente las observaciones por ciclo en el repositorio**.

Git blob SHA de paquetes, cotejados explícitamente con la codificación Base64 del archivo local:
- B01 `ccb059c7e8b0e9ca45ec5850693315f74208bcc8`
- B02 `ec5fca0187d43a9a41c1b6d85ebf9af215b5be91`
- B03 `9e7abe3c2822c72b8eb10588468c877480657b60`
- B04 `1d08a8c66a7b19c77ddcfafa8f5f2e0b7b378044`
- B05 `3ffb6448c153cf96a4b6a7d1fae1f6aa3edfaa04`

Reconstruct `python src/unpack_results.py`, then process `python src/stage.py 1 validation` etc; **no test holdout remains unconsumed**. Full per-cycle A–J in `reports/ledger/B01_AJ.md` ... `B05_AJ.md`, all present and not excerpts. Numeric summaries in `reports/SUMMARY_30.csv`, machine readable `reports/AUDIT_SUMMARY.json`. Original engine frozen before execution at Git blob `756d9e5568571c6985298719938c3ca5b717b793`, SHA256 `cfc0a2d1097df213a09d33188bce6a265a2bf68b7876bcca5ef4140c829daa23`.

**REPRODUCED_COMPUTATIONALLY_IN_ISOLATED_DIRECTORY:** all 60 validation/test JSON exactly reproducible SHA256 after fixing a directory creation bug of the retrospective `stage.py`; source engine and all original numeric results unchanged. **NOT CLEAN GIT CLONE INDEPENDENT MACHINE; NOT EXTERNAL EMPIRICAL REPLICATION.** Do not upgrade AB scientific level 2/3 from this audit.

Governance: five block preregs plus B01 prospective anti-leak amendment and explicit G holdout unseal were committed before validation/test phases. Separate posttest professional-baseline audit is descriptively postselected; no confirmatory reuse of exposed test.
