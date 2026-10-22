# ERRATA PREVIA A EJECUCIÓN — B04 real datasets

El prerregistro B04 inicial (commit 6cf58d6638fbf7a088dd8e8e7c558f516ea2db52) refería el SHA256 984aceb47b6d8ad46378af37ec756f386a3b1f3a6a6a76ab58e04c973d4e9ceb. El motor abortó T19 con KeyError('dataset'), ANTES de calcular un único resultado: T19 INVALID; T20–T24 NO INTENTADOS bajo ese manifiesto.

Causa: en el generador local de prerregistros se asignó el campo 'dataset' solo al bloque 5, cuando B04 también utiliza una fuente real. La reparación cambia exclusivamente el esquema de los seis contratos B04 añadiendo dataset='diabetes' y k=3 o k=6; método, rivales, splits, código de análisis, semillas y endpoints permanecen iguales.

**Nuevo SHA256 del manifiesto JSON B04 CORREGIDO:** ff6d4d15cdf59814aea92eb42bc950625bc60bb8e82be32208a22365db558fd4. Este hash queda registrado ANTES del ensayo corregido; el hash anterior y el fallo se conservan íntegramente. Fuente experimental sin modificaciones: 867e75309dfa81c8568bb2360d4cb4909560a338d7f16a587d03bba877f1deb6.

Se ejecutarán T19–T24 bajo este nuevo compromiso. Este documento es una errata visible, NO demuestra el éxito ni la independencia científica.