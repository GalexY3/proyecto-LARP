# Observaciones para Metodología AB — 22-10-2026

**Fuente:** LARP AB06 seis ciclos, dataset UCI Digits y repo privado `GalexY3/proyecto-LARP`; no cambiar la versión de AB automáticamente.

**AB-M020 — GATE de dimensionalidad y observabilidad.** Un patrón 3D con regularidad espectral confirmada no tiene garantizada la misma propiedad cuando se proyecta a imágenes 2D. Solicitar documento que identifique la dimensión y simetrías de la tarea, geometría original, proyección/embedding y observabilidad de cada rasgo. Falsador: en casos donde la proyección sí preserve la métrica relevante el gate debe permitirlo sin penalidad. Estado: propuesta.

**AB-M021 — GATE de información sensorial vs igualdad de parámetros.** Modelos de ≈5800 parámetros pueden recibir distinta cantidad y transformación de información: intensidad, derivadas, interpolación RBF y suavizado por tipo. Antes de inferir ventaja de arquitectura, equiparar contenido, costo de lectura, preprocesado y FLOPs; agregar baselines de identidad y preprocess+MLP. Reparación detectada en C06: MLP píxel suavizado mejora robustez. Estado: propuesta.

**AB-B011 — Conservar negativos de roles especialistas sin forzar complementariedad.** La hipótesis intuitiva de roles tipados tuvo una refutación clara en datos externos a Fourier: las cinco transformaciones fueron peores que cinco lecturas de intensidad en la mayoría de semillas. Beneficio metodológico de ablación controlada de semántica y geometría por separado. Límite: no invalida roles en todos los dominios. Estado: práctica prometedora.

**AB-M022 — Auditoría de comparador fuente ≠ ejecutable.** Localizar repo original no es ejecutar ni validar a igual coste. Registrar `SOURCE_LOCATED`, `BUILD_SUCCESS`, `SMOKE_PASS`, `DATA_COMPARABLE`, `RUNTIME_BUDGET_MATCHED` como gates separados. C01 fuente Wei 2010 localizada pero no compilación validada. Estado: propuesta.
