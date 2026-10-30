# ERRATA ARCHIVE A17 — 2026-10-30

Primer auditor completo depositado ANTES de outcomes (reparación de ingesta de archivo erróneo incluida): commit `b4d9c09e154a0139d1157107f32466a4141fc583`, blob Git `6814cf134417f9792cefa26bdd81d03dadb7eeef`, SHA256 local inicial `cde86a8d56a3c2754d1d4933f4743ccf3e1db8228528e7766ea0db5f17de5264`.

Primera corrida del auditor: **19 PASS / 1 FAIL**. A17 se marcó FAIL por bug del propio instrumento: la salida histórica `AUDITORIA_M01_M18.json` tiene raíz `{date,type,python,tests}`; el código esperaba 18 claves directamente en la raíz, aunque hay **18 registros dentro de tests**. Los otros 19 tests no fallaron. No afecta a los bytes históricos ni invalida los 18 controles anteriores. 
Se conserva el primer resultado fallido en el ZIP de cierre. Reparación exclusivamente en la línea de A17, cambiando `get(...)` por `get(...)['tests']`. Nuevo archivo local SHA256 `0ee43ff7e8b07ea925e1b2e5c4e3d83d6065d5ce7fd91afac52f37fc727dc6b3`. **Registrar nuevo commit y verificar Git blob antes de la repetición**, sin cambiar preguntas A01–A20, umbrales ni datos originales.
Estado: ERRATA POST-FIRST-RUN; reejecución aún pendiente de guardar nuevo código. No contar como otra prueba independiente.
