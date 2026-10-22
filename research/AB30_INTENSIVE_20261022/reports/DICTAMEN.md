# LARP — 30 ciclos AB intensivos: dictamen consolidado

Fecha 22-10-2026. Protocolo AB 3.2.1 + O1 + O2; rama privada research/ab30-intensive-20261022. Estado: 30 preguntas/contrastes computacionales ejecutados, distribuidos en cinco bloques de seis, con congelaciones GitHub previas a cada bloque. Tres auditorías posteriores de retícula NO cuentan dentro de los 30. NO HAY descubrimiento 2/3 ni 3/3 acreditado.

## Procedencia y alcance
Motor inicial congelado en 626b456891a11cf5228a75786afb1b577becf64c, previa reparación de fase compartida; añadido baseline convencional de 64 píxeles de forma prospectiva en 47312001f898fecdc82365732160bf8a47ce486d. Prereg B01 0a3b10d, B02 c4fcb09, B03 9ef84ea, B04 64e6a7c, B05 56b129e; AUD posterior d9494f3. Los 6 contrastes de un mismo bloque se congelaron conjuntamente: branching entre bloques, no planificación individual postresultado.

Los mundos geométricos son cuadrados periódicos 2D con 100 posiciones (20 por cada uno de cinco tipos) bajo CVT por tipo/global, Sobol por tipo/global, iid, retícula y traslaciones. NINGÚN generador está certificado como MHU y no se ejecutó el algoritmo multiclass blue noise de Li-Yi Wei. n=12 semillas geométricas pareadas por ciclo salvo Digits, n=8. Múltiples tareas y el mismo dataset Digits ya expuesto: los IC95 t pareados son DESCRIPTIVOS, sin corrección para todas las afirmaciones ni replicación externa.

## B01: cobertura y espectro, N01–N06
CVT por tipo frente a IID reduce p95 de la distancia al tipo más alejado: delta A-B = -0.10734. Frente a Sobol por tipo mejora distancia media -0.02322. Una retícula por tipo mejora ese p95 frente a CVT (-0.00427 a favor retícula). CVT disminuye potencia espectral baja de unión frente a Sobol global, pero trasladar subtipos independientemente N06 no cambia potencia global en dirección clara (IC cruza cero). Ninguno de esos resultados identifica MHU asintótica.

## B02: cuadratura, N07–N12
Fracaso funcional de la presunta ventaja: con sinusoides periódicos compartidos f=1 el MSE de CVT es 0.000494149 vs Sobol global 0.0000431151; f=6, 0.00797060 vs 0.00039601. Una retícula por tipo integra frecuencias no resonantes con MSE ~1e-32. Consecuencia: espectro promedio y cobertura no son sustitutos de error condicionado a frecuencia objetivo. No hay prueba de superioridad general de la retícula porque su aliasing fuera de banda sigue siendo una limitación.

## B03: reconstrucción, N13–N18
Seis contrastes favorables a CVT por tipo para MSE de reconstrucción espacial con kernel gaussiano de ancho fijo 0.095. N15 independiente suave CVT=0.0310704 vs Sobol global=0.1016446; bajo pérdida 30% N17 CVT=0.1108879 vs Sobol por tipo 0.1289769. Bajo ruido observacional 0.2, N18 CVT=0.0493865 vs Sobol 0.0784374. Esa ventaja es compatible con el sesgo geométrico de buena cobertura, no con causalidad específica de MHU.

## B04: clasificación real Digits, N19–N24
Las cinco vistas se obtienen deterministamente de los 64 píxeles originales, no de sensores independientes. N19 CVT BA=0.92878 vs Sobol global 0.92704, IC de diferencia cruza 0. N20 baseline de 64 píxeles BA=0.93842 > CVT 0.92878. N22 rotación 15° favorece píxeles 0.71282 frente CVT 0.69561, con incertidumbre cruzando cero. N24 desplazamiento favorece CVT 0.47398 vs píxeles 0.43909; no es un efecto causal aislado de geometría: cambia el procesamiento funcional. Dataset reutilizado, sin holdout externo.

## B05: transporte por grafos, N25–N30
CVT mejora gap de adyacencia normalizada frente a IID, 0.08026 vs 0.05032, pero Sobol global obtiene 0.09001 y supera a CVT N26. El momento espectral 12 y CV de grado tampoco favorecen CVT frente a Sobol. Número efectivo de aristas NO exactamente emparejado al simetrizar kNN; ningún entrenamiento de GNN en esta rama.

## Auditoría posterior (no contada como ciclos)
Prereg independiente de la auditoría d9494f3, ejecutada después de observar B03. AUD01–03: CVT supera una retícula por tipo en reconstrucción: f=1 compartida MSE CVT 0.0304975 vs retícula 0.0330764, f=1 independiente 0.0304778 vs 0.0330622, f=3 compartida 0.679723 vs 0.920413. Compatible con sesgo del interpolador; no replicación fuera del modelo ni identificación MHU.

## Auditoría A–J y gobernanza
Los 30 contrastes tienen predicción, falsador, rivales, código, semillas, registros numéricos y decisión. La fase G registra AUSENCIA de confirmación independiente, nunca un éxito ficticio. El generador de ledger A–J está versionado en src/build_ledger.py y usa prereg/B01..B05 y results/RESULTS_30.csv. El raw completo por semilla está en el paquete de conversación pero no íntegramente trasladado aún a GitHub, por lo que no declarar GitHub como archivo completo de evidencia. CLEAN_CLONE_NOT_VERIFIED. Las credenciales de originalidad no derivan de commits o de repetir semillas.

AB-H: siete priors nuevos en reports/PRIORS_DELTA.md; originales históricos intactos. AB-DECIDE: CLOSE_QUOTA, no STOP científico. El camino a 2/3 requiere un mecanismo predictivo exclusivo frente a Wei, muestras MHU certificadas, tareas no diseñadas para CVT, igualdad de información/coste y replicación externa independiente.

Referencias: Jiao et al., Phys. Rev. E 89, 022721 (2014), doi:10.1103/PhysRevE.89.022721; Li-Yi Wei, Multi-Class Blue Noise Sampling, SIGGRAPH 2010, https://www.liyiwei.org/papers/noise-sig10/ .
