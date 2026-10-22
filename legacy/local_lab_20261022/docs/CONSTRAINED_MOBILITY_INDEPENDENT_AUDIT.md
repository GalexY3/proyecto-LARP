# Auditoría independiente de Constrained Mobility v1

El auditor nuevo `artifacts/constrained_mobility/independent_trace_audit.py`
lee los artefactos terminados y escribe exclusivamente un archivo JSON nuevo.
No importa `larp`, no ejecuta cadenas ni optimizadores y no calcula rendimiento
neuronal o de adquisición. Reutiliza las fórmulas numpy independientes de
`artifacts/spectral_matching/independent_metrics_check.py`; conserva ese archivo.

Comprueba todas las propuestas por replay: hashes exactos, recuentos conservados,
dos/tres sitios y tipos distintos, ciclo permitido, prefijo RNG documentado,
130 identidades/tolerancias/ratios/booleanos, decisión por conjunción de las
130 desigualdades, familias de rechazo y distancias Hamming. Los conteos por
familia son cofallos de propuestas y no evidencias independientes.

La muestra de recálculo se fija antes de observar las cadenas: índices desde
cero `{0, n//2, n-1, primer aceptado, primer rechazado}`, deduplicados.
Recalcula las 130 desigualdades en cada candidato elegido y en los estados
nativo y final. Las decisiones deben coincidir exactamente; una tolerancia
numérica pequeña sirve sólo para comparar valores de dos implementaciones,
sin relajar la guarda experimental del 5% ni sus umbrales.

Los valores de métricas en propuestas fuera de esa muestra sólo reciben
comprobaciones de consistencia interna. El replay RNG certifica el prefijo
registrado; no reproduce velocidad ni truncamiento por reloj. El muestreo
condicionado por etiquetas y vecinos próximos no demuestra distribución
uniforme, mezcla o conectividad del conjunto factible. La independencia es
respecto del evaluador prospectivo, con fórmulas y runtime numpy compartidos
con la auditoría histórica; no constituye una réplica científica independiente.

Uso después de terminar la ejecución:

```text
python artifacts/constrained_mobility/independent_trace_audit.py --config CONFIG_FROZEN.json --prepared prepared.json --results results.json --output AUDIT_NUEVO.json
```

El modo `--self-test --output ARCHIVO_NUEVO.json` sólo prueba la herramienta,
el muestreo prefijado y casos artificiales de corrupción/guarda de varianza.

## Incidente de ejecución y procedencia de la colección

La ejecución v1 terminó `BUG_INVALID` por una carrera de archivos en Windows
después de diez cadenas completas. La auditoría nueva de ese subconjunto
conserva `PARTIAL_ONLY`, identifica las dos cadenas no iniciadas y no imputa
sus resultados. El auditor original y su sello previo permanecen inalterados.

Un suplemento sellado por separado ejecutó únicamente esas dos identidades
predeterminadas, con código científico, semillas, cap y guardas iguales.
El auditor original verifica la colección combinada de doce cadenas; su
`PASS` certifica integridad y coincidencia de las métricas comprobadas.
La procedencia científica es `AMENDED_EXPLORATORY_OPERATOR_DIAGNOSTIC` y
nunca convierte la cápsula original en una ejecución válida completa.
El coste total incluye ambos lotes; las comparaciones de coste entre lotes
siguen siendo descriptivas por el cambio de I/O y el momento de ejecución.
