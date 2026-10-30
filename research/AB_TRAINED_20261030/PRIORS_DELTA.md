# Priors de LARP entrenado L01–L20 — 2026-10-30

- P-TR01 [observación computacional condicionada]: CVT por tipos 0,2211 NMSE frente a MHU proxy tipos 0,2873. Las 20 condiciones comparten generador; no trasladar al aviar original. Actualización: prior contra superioridad general de MHU se refuerza.
- P-TR02 [observación computacional condicionada]: rutas aprendidas por correlación de TRAIN tienen mayor longitud (~0,18) y peor media de NMSE que tipo o kNN en campos low/high/localized. Hipótesis explicativa de sobreajuste **NO demostrada causalmente**. Nueva prueba: router entrenado end-to-end con penalización por longitud e información, rival attention strong.
- P-TR03 [estructura]: CVT kNN obtiene cobertura media de 0,909 frente a MHU proxy kNN 0,752; distancias similares. Posible mediador, requiere ablación que iguale cobertura/longitud sin cambiar geometría.
- P-TR04 [bloqueo]: archivos nativos NPZ aviares de N400 disponibles en GitHub bajo ramas originales, pero conector no descarga binarios. No atribuir resultados proxy a ellos.
- P-TR05 [evidencia de integración]: 90 modelos MLP de 1009 parámetros, train/val/test por semillas disjuntas, 10 celdas repetidas localmente 100% coincidentes. Dado que datos son sintéticos, no confirma mejora real.
- N1 únicos nuevos: 0. N2=N3=0. CT2 rama matemática 24/100 histórico; rama trained proxy 18/100 (nuevo juicio ordinal, no probabilidad). R5 STOP_LOCAL.
