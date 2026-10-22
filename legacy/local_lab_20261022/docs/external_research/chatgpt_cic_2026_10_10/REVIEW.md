# Revisión local del estudio CIC de ChatGPT

Fecha:2026-10-10. Encargo humano: revisar lo hecho por CGPT y redactar trabajo útil para el colaborador, comunicando resultados finales Scale3D. Las instrucciones recibidas se conservan como propuestas; no se adopta v3 ni se ejecuta generación nueva.

## Procedencia y comprobaciones

ZIP original: SHA256 `7440888d1ff370325b136ede2966d5ca9922d4f59b892012e8b34ceff2855aff`;129 archivos conservados en `received/`, más original ZIP y MD externo. Manifiesto128/128 válido; excluye su propio archivo.29 referencias de PROVENANCE coinciden. Ambos generadores recibidos son byte-idénticos a las fuentes locales congeladas; las seis nubes N32768 coinciden con los arrays del job v2.

Se ejecutaron los12 tests CPU revisados, PASS en4,79 s, con bytecode y caché pytest desactivados. No se reejecutó `run.py` ni auditores que sobrescriben recibos. Un cálculo separado desde los20 NPZ nuevos verificó el panel39 modos, fases de celda y NN global/homotípico; también primera shell N4096. Discrepancia máxima≈1,33e−14. Recibos nuevos en `artifacts/cic_review_20261010/{provenance.json,qa_review_receipt.json}`.

Hashes acreditan integridad y correspondencia de fuentes, no fecha independiente de la congelación. El material incluye investigación CPU externa, no nuevas réplicas del laboratorio local. Algunos registros de auditoría externos tomaban admisión y métricas homotípicas desde JSON; el recálculo local indicado amplía, sin confundir lectura con recomputación, el alcance verificado.

## Conclusiones y límites

La identidad `D=ΣS_c−S_union` y expectativas condicionadas por barajado son correctas bajo conteos fijos. La matriz espectral de UN modo es un producto exterior de rango≤1; sus autovalores no ofrecen automáticamente una colección de observables independientes. Separar espectro observado, media por shell/ensemble y espectro de la matriz esperada. El null de marcas no preserva packing/certificados ni sirve por sí mismo de control funcional.

La autoenergía CIC con pesos no negativos favorece centro de celda; eso no demuestra que explique toda la energía ni la trayectoria. Origen fresco usa un PRNG separado,600 muestras exógenas independientes, una por paso. Anula gradiente propio esperado condicionado a posiciones, pero no alias de pares ni actualización media de Adam. La intervención modifica objetivo efectivo y ruido/estado del optimizador simultáneamente.

N400 ya contiene12 construcciones, tres semillas y seis parejas; N4096 contiene8, dos semillas y cuatro parejas. Origen fresco mejora potencia axial, máximos del panel y separación en esas parejas. N4096 tiene6/8 admitidas: LOCAL fijo falla en ambas semillas; cuatro frescas admitidas. No son pares de patrones todos admitidos ni un control fresco sin supresión espectral. Ninguna red neuronal fue entrenada.

Fidelidad de auditoría: el runner recibido usa seed0 para banda muestreada; el generador local usa `seed+99871`. Primera shell y banda completa se conservan, pero para transferencia congelar la semilla exacta y no declarar igualdad completa de la puerta muestreada. `contrast_enrichment` regulariza el denominador con1e−15; si el esperado de D≈0, su ratio es indefinido/inestable, aunque no afecta al panel grande observado. No reparar archivos recibidos; proponer corrección prospectiva.

## Trabajo siguiente recomendado

No pedir otra batería CPU N400/N4096 por inercia. Derivar sustracción propia exacta mediante ocho momentos de los pesos, coste O(N), y objetivo promediado sobre orígenes con kernel de pares/aliases. Es el contraste más directo entre autofuerza y cambio global de potencial. Preparar fixtures y calificación CUDA nueva limitada; no medir timings locales en el contenedor por inferencia.

En paralelo, resolver el riesgo Bayes global/local de los productos actuales: la tarea difícil tiene1024 coeficientes reales por campo y su salto coincide con el cambio de conteos del tipo raro de348 a1393. Es una hipótesis post hoc de adquisición, no una explicación demostrada. El job neuronal v2 sí terminó8/8; sus datos son de origen fijo y se mantienen separados.

Valoración conservadora:2/3 de utilidad técnica interna y1/3 de novedad acreditada. H1–H6/C numéricos y protocolos originales permanecen intactos. El nuevo encargo externo pide cerrar mecanismos, controles y decisiones implementables, no promocionar MHU.
