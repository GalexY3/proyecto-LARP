# LARP AB30 Fixed-site Multicolor Sensing · 24-10-2026

**30 ciclos AB A–J ejecutados** y prerregistrados antes de calcular E/G: [ALL_30.json](prereg/ALL_30.json) commit `503d2c9`. [Código exacto](src/) congelado en tres partes b64+gzip, SHA256 `cae397a9e83a88a807ad5b77faeec1cc5a3ffdd8c682c6ee5822851fe8d2b156`. Original en Python y ZIP de conversación; tres Git blobs SHA comprobados. El README científico completo, ledger 83.825 bytes y 360 resultados brutos por semilla están en ZIP `LARP_AB30_FIXED_SITE_20261024.zip`, SHA256 `6851bc134613283d107de03e078bdeb81961d940fe25d0ae5f8aa8f8d5f49871`.

## Resultado: NO 2/3, NO 3/3
- B01 C01–C06: baja k finita por modalidad, frente a aleatorio 6/6 favorables G, contra greedy farthest-first 4/6.
- B02 C07–C12: cobertura de sensor superviviente, frente a aleatorio 6/6, contra farthest-first **2/6**.
- B03 C13–C18: IDW de campos periódicos, frente a aleatorio 6/6, contra farthest-first **3/6**.
- B04 C19–C24: Fourier ridge (último campo fuera de basis), contra farthest-first **2/6**.
- B05 C25–C30: campos aleatorios/transferencia a IID+jitter, contra farthest-first **2/6**.
- Auditoría posterior, NO ciclo 31: seis imágenes observadas skimage.data, unión de 20 sensores, IDW: farthest-first gana o empata en **3/6**, spectral favorecida en 3/6; sin transporte uniforme. [Prerregistro post-selection](prereg/POSTRUN_IMAGE_AUDIT.md).

**CT2 10→11→9→12→9→8→7/100** (último cambio por imágenes, no ciclo). Un 1/3 operacional nuevo LARP-1-005 registrado en [ledger canónico](../../FINDINGS_1_3/LEDGER.json), acumulado de entradas explícitas N1=5; N2=N3=0, total histórico pre-O4 sin auditar.

## Limitaciones
100 sitios simulados sobre toro periódico, cinco clases [40,24,16,12,8], los sitios **NO SE MUEVEN** en las comparaciones; solo se recolorean. Cuatro semillas E y ocho G del mismo simulador, reutilizadas entre familias: no replicación independiente ni treinta tests independientes. El objetivo minimiza `S(k)` a k finito: **NO certifica multihiperuniformidad**. El control farthest-first es fuerte en cobertura, pero NO iguala la publicación de Li-Yi Wei SIGGRAPH 2010, que ya resolvió multiclase blue-noise para sensores. Más: Jiao et al 2014 retina, Heck et al 2013 aliasing. La ventaja sobre un rival aleatorio no establece originalidad.

## Archivo
- [Resumen numérico de los 30](results/SUMMARY_30.csv).
- [Dictamen y límites](reports/DICTAMEN.md).
- Prerregistros GitHub anteriores a ejecución, fuente exacta en tres fragmentos.
- **ZIP íntegro** de conversación: 50 ficheros, 30 JSON ×12 semillas, 30 A–J individuales, seis imágenes × dos máscaras × dos estimadores, código editable, auditoría, gráficos. 30/30 JSON y resumen reproducidos byte a byte desde extracción limpia del ZIP en mismo entorno.
- Los brutos extensos/ledger completo todavía están en ZIP, no en GitHub; no reclamar O3 remoto completo ni clon Git independiente.

**AB-DECIDE:** cierre del bloque 30. Priorizar otra pregunta científica, o reproducir contra código publicado y modalidad observacional real antes de invertir más ciclos.
