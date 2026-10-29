# LARP-VISION C04 — Dictamen AB 3.2.1, 2026-10-29

**RUN + POST-HOC AUDIT, 1 nuevo ciclo ejecutado.** Bloque de 20 autorizado por investigador: C02 + C04 ejecutados=2; C03 PLANNING_AB_ONLY=0; saldo **18**. N1 no duplicados nuevos 0, N2 0, N3 0. CT2 Vision 22→17 C01→13 C02→11 C04, juicio ordinal no probabilidad. **R5 STOP_LOCAL** sobre pequeño benchmark LFW, **BRANCH** hacia imágenes con cinco canales físicos verdaderos; no merge a main ni CI.

## A–D Contrato y freeze previo a outcomes
- Pregunta: ¿mejora una distribución espectral MHU finita de 160 lecturas la **clasificación real** rostro/no rostro, comparada con rivales competentes y con la ablación de coordinación de 5 tipos?
- Dataset skimage `lfw_subset`: 100 recortes de caras + 100 de fondos de 25×25, no 200 personas independientes confirmadas. 5 tipos × 32 lecturas del **mismo canal de intensidad gris**, no 5 bandas ópticas. Cada muestra bilineal combina hasta 4 píxeles, por lo que tampoco equivale estrictamente a 160 fotodiodos independientes. Unidad = imagen original.
- Comparadores: grid, Sobol, PoissonDisk con cobertura/fill_space, MHU_PROXY_JOINT, MHU_PROXY_SUB, fases relativas intertipo rotas, azar; `supervised_kbest` 160 pixels seleccionados usando solo etiquetas TRAIN mediante ANOVA (no TokenLearner ni rival aprendido fuerte) y `full_pixels` 625 pixeles no matched. Todas las opciones usan un SVC RBF C=2 gamma=scale class_weight=balanced.
- Seeds geométricos [4101,4109,4127], dos validaciones cruzadas estratificadas 5 folds con estados [13,29]; entrenamiento clean, tests clean, ruido gaussiano sigma 0.13, oclusión negra 6×6. 70 pasos Adam para joint/sub bajo costo geométrico no igualado.
- **PREREG completo antes de outcomes** en commit `cb110f2b81f1f767d1c2de8483dad1241958380a`. **Código FUENTE completo congelado** antes de outcomes en commit `4e4f4e1742015756b1216e7a0cd84f77c4a017ef`, blob git `979e61cdaacd2b30ca08a0968eb2e0f8d2dbebbf` coincide con `git hash-object` del código local ejecutado. SHA256 del código `d57d21ce76d4513419fbf38df9ec62b771872a4d50f1856a3a16133b268b31ae`.
- Datos imágenes SHA256 `ce1ab433bd0a896d88a87e40efdf37d9e1ce98bbd3317b498da9f0a7b8e125d5`.

## E Resultados (aciertos %, 200 imágenes con 6 exposiciones correlacionadas cada una)
| Método | Clean | Ruido .13 | Occlusion 6×6 |
|---|---:|---:|---:|
| Grid | 97.25 | 97.00 | 96.00 |
| PoissonDisk | 97.25 | 96.75 | 96.33 |
| Sobol | 97.17 | 97.00 | 95.83 |
| MHU finite-JOINT | 97.17 | 97.17 | 95.67 |
| MHU finite-SUB | 97.17 | 97.17 | 95.83 |
| JOINT fase rota | 97.00 | 96.58 | 95.75 |
| Azar | 97.25 | 97.17 | 96.00 |
| ANOVA top-160 pixel | 93.50 | 93.25 | 89.75 |
| Full 625 pixel | 97.25 | 97.25 | 95.75 |

Total `32,400` predicciones individuales: 3 geometrías × 2 CV × 200 fotografías × 9 métodos × 3 condiciones. No equivale a 32.400 observaciones externas. SHA256 JSON bruto `ec917d39129004f56066836a1637c7d263099bc28c6f8880082303ee03474456`. Raw disponible en ZIP de conversación, **NO versionado aquí**. CLEAN_CLONE_NOT_VERIFIED.

## F–G Auditoría adversarial y confirmación
- Bootstrap descriptivo, cluster a 200 imágenes, 8.000 remuestreos, no corrección multiplicidad: JOINT−grid clean = −0.083 puntos porcentuales (IC95 descriptivo −0.25, 0.0); JOINT−Poisson igual. JOINT−SUB clean = 0 (−0.25,+0.25). Oclusión: JOINT−Poisson = −0.667 pp (−1.333,−0.167), sin validez inferencial externa. Reutilización de imágenes dentro del mismo corpus, posible dependencia.
- **Techo de clasificación** 96–97 % incluso con geometría aleatoria y 160 lecturas, por lo que el outcome no discrimina adecuadamente el mecanismo geométrico; stop.
- MHU-JOINT low-k unión 4.60e−07, SUB 1.49e−06, retícula ~0. Reducción del proxy espectral no genera ventaja funcional; replica intuición previa de otros ciclos, **no N1 nuevo**.
- Los 5 tipos son etiquetas geométricas, no 5 modalidades reales; no se estudian Vision Transformers, Wei original, precisión de imágenes complejas ni coste energético real. La selección supervisada ANOVA no representa el mejor rival de selección aprendida. Semillas/folds no son réplica independiente.

## H–I Priors / grado
P-VIS10: benchmark LFW próximo a techo y falta sensibilidad. P-VIS11: separación espectral no identifica mejor clasificación. P-VIS12: 160 muestras bilineales no equivalen a 160 sensores físicos/igual consumo; P-VIS13: ANOVA univariante no es rival aprendido moderno. CT2 Vision 13→11 por saturación y falta de superioridad, **no probabilidad**. N1 nuevos 0, N2/N3 0. Validez local condicional, transporte insuficiente, originalidad no acreditada.

## J AB-DECIDE
**STOP_LOCAL**: no repetir entrenamiento de la misma clasificación con nuevas semillas. Continuar solo cuando haya acceso a imágenes multiespectrales de al menos 5 bandas originales y comparador competente (Wei 2010, muestreo fijo optimizado, y/o reconstrucción/lectura visual aprendida). Entre fuentes consideradas: CAVE 32×31 bandas (licencia de redistribución no verificada); dataset agrícola/multiespectral Bürgewald MicaSense CC0 (seis bandas, 735 capturas, archivos grandes). **18 plazas restantes** del bloque ya autorizado; no solicitar otro bloque.

ZIP de conversación `LARP_VISION_C04_20261029.zip` contiene script congelado, salida 6MB JSON, 3 figuras, auditoría, priors y hash del ZIP `fd2ec58d4338df0279eaee345f25aa239aec5f560d882196ff1449de8df6b89e`. No afirmar archivado GitHub de raw.
