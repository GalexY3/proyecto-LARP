# C02 · Dictamen AB con resultados verificados — 2026-10-29

**Autorización:** 20 ciclos branching posteriores al C01 de esta rama. **Contabilidad:** 1 experimento nuevo ejecutado C02 (prerregistro hash; limitación O3 descrita abajo), 0 nuevos N1 no duplicados, N2/N3 0; saldo recomendado 19. CT2 VISIÓN 22 (inicio C01) → 17 (fin C01) → 13 (C02), ordinal, no probabilidad. **R5 STOP_LOCAL** sobre RGB 48×48, pivot condicionado a cubos espectrales originales y método Wei ejecutable. No merge a main ni CI.

## Prerregistro, límites y hashes
- Preregistrado A–J en commit `4ea4fbe98eebd562536e4f7bf937da45291bdceb` antes de outcomes.
- SHA256 del código `vision_ab_c02.py` anunciado previamente: `42b7bcef08ed0b02909ec4b95bbd3bbb46a338762ed011f1e8a64735b1e60729`; hash verificado tras la ejecución. Depende de `vision_ab_c01.py` SHA256 `5e47f6e63e98dd14655f8eeec0e8d826d97eb750fd24c099ea4b6aa3e50ea993`.
- SHA256 resultados originales C02 `aaf9b227855ea05fff1351c0bf5d5fd91faf15e8c4622f4d7d9a6669dac3006e`.
- **Limitación de gobernanza:** solo el HASH del código estaba congelado en GitHub, no los bytes de la fuente; por tanto no cumple literalmente el control más fuerte O3 de fuente depositada previamente. Fuente íntegra, resultados y scripts de auditoría disponibles en ZIP de conversación; **CLEAN_CLONE_NOT_VERIFIED**. No hacer afirmación de freeze-run GitHub completamente verificado.

## A–D: pregunta, diseño, controles
Cinco filtros virtuales lineales de una fotografía RGB: R, G, B, (R+G)/2, (G+B)/2. 160 lecturas escalares, 32 por tipo; cuatro seeds [2029,2039,2053,2063]; imágenes DEV astronaut/coffee/chelsea/rocket, TEST retina/stereo_motorcycle/hubble_deep_field/immunohistochemistry y stress sintético colorwheel. **Solo retina y stereo_motorcycle son nuevas a C01**. Interpolación/regresión común sobre 64 bases gaussianas espaciales por tres canales RGB, ridge `lambda=.012`, anchura `sigma=.17`. Comparadores: cuadrícula equilibrada, PoissonDisk fill_space+farthest/etiquetas maximin (proxy **NO Wei auténtico**), Sobol con etiquetas maximin, variante espectral por subtipos, variante espectral conjunta, y joint con fase de cada tipo rota aleatoriamente. Condiciones clean, pérdida 20%, ruido .03. 648 observaciones.

## E: MSE TEST 4 imágenes (menor mejor)
| Método | Clean | drop20 | ruido .03 |
|---|---:|---:|---:|
| Poisson+maximin (NO Wei) | **.014835** | **.016495** | **.015077** |
| Sobol equilibrado | .015074 | .016608 | .015246 |
| Cuadrícula equilibrada | .015167 | .017322 | .015369 |
| Espectral SUB | .015454 | .016749 | .015705 |
| Espectral JOINT | .015477 | .016890 | .015777 |
| JOINT fases rotas | .015351 | .017131 | .015729 |

Para clean JOINT empeora vs Poisson 4.33% y vs SUB 0.145%. Beneficia vs Poisson solo en 1/4 imágenes; las dos imágenes no observadas en C01 dan JOINT 3.52% peor que Poisson. Retina favorece joint; stereo_motorcycle la contradice. Sin evidencia de generalidad. Ablación: traslación de subtipos mantiene potencia espectral individual con precisión ~1e-20, pero **no** emerge ventaja funcional de la coordinación. No es una certificación asintótica MHU.

## F–G: adversariales y confirmación
- Filtrado virtual 5 tipos sobre **3** canales RGB (rango espectral máximo 3): no son 5 bandas ópticas verdaderas ni retina aviar.
- Mismo número de lecturas/decodificador; costo de diseño geométrico distinto; no se miden inferencia neuronal/FLOPs hardware, solo MSE de reconstrucción.
- Corpus pequeño y contaminación por C01 en dos TEST: sin p-valores confirmatorios ni replicación externa.
- Wei 2010 (*Multi-Class Blue Noise Sampling*) está localizado pero aún NO compilado/ejecutado ni sustituido por este proxy; WACV 2023 aprende conjuntamente selección de banda, CFA y reconstrucción.
- Source de GitHub pre-outcome en forma de hash, no bytes; aplicar errata metodológica de portabilidad.

## H–I: priors, contribución y novedad
P-VIS06: no hay ganancia media del acoplamiento espectral multiclase sobre rivales fuertes en RGB filtrado. P-VIS07: fases relativas por subtipo conservan espectro individual, pero romperlas no perjudica generalmente resultado. P-VIS08: la heterogeneidad de escenas no valida un nicho favorable. P-VIS09: Wei 2010 y WACV 2023 son antecedentes decisivos, novelty gate abierto. **N1 adicional 0; N2/N3=0**.

## J: decisión
**STOP_LOCAL** para barridos adicionales con este dataset/preprocesado. **PIVOT/BRANCHING libre** a sensores de 5 bandas genuinas (CAVE 32×31), diseño de filtros multiespectral auténtico (Wei SIGGRAPH 2010 como control), modelos de reconstrucción aprendidos y evaluación real con paridad de presupuesto/coste. Si fuente/derechos/acceso inaccesibles, usar plazas para auditoría legal/documental/metodológica; no gastar ciclos ficticios. Sin datos independientes no subir 2/3.

Fuentes: https://www.liyiwei.org/papers/noise-sig10/ ; https://openaccess.thecvf.com/content/WACV2023/html/Li_Jointly_Learning_Band_Selection_and_Filter_Array_Design_for_Hyperspectral_WACV_2023_paper.html ; https://cave.cs.columbia.edu/repository/Multispectral ; https://www.epfl.ch/labs/ivrl/research/downloads/rgb-nir-scene-dataset/
