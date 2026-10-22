# Erratas de instrumentación (no ciclos extra)

- El primer intento de ejecución falló por asignar `DEV=['grass']` como lista en lugar de la cadena `'grass'` antes de poder cargar escenas de test. No produjo datos científicos. Se reparó antes de la corrida conservada.
- Antes de la corrida válida se detectó que `get()` cargaba todos los conjuntos antes de escribir el archivo de congelación. Se reparó para cargar explícitamente las imágenes de prueba **después de escribir `HOLDOUT_FREEZE.json`**, antes de la única corrida conservada. No se reclamó preregistro externo de este freeze local.
- El test de reconstrucción usando los 576 píxeles presentó un máximo de diferencia aproximado 1.08e-6 atribuible a acumulación float32, y se reparó la tolerancia a 2e-6 sin alterar código de inferencia ni resultados. 6/6 tests tras corrección.
- La comparación GP original disponía de un pool efectivo más pequeño que el nominal. Se conservó y se añadió GP_ALL con 576 candidatos por rol; todos los resultados GP_ALL son posteriores al holdout y no deben utilizarse como confirmación nueva.
