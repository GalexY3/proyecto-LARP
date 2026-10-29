# LARP / AB VISION C01 — Dictamen y gobernanza (2026-10-29)

**Experimento original:** PRE-REGISTERED_GITHUB + RUN, un ciclo AB A–J; un brazo INVALID reparado de forma POST_EXPOSURE. **N1 nuevos=0 (relación sustancial con LARP-1-005 y AB08); N2=N3=0; CT2_VISION 22→17** juicio ordinal, no probabilidad. **STOP_LOCAL** sobre el mismo benchmark, PIVOT condicional a nueva fuente.

## Registro inmutable de secuencia
- PREREG commit, anterior a outcomes: `e50994d130af34207dfe4ceb14682f8253ceed93`, archivo `PREREG_C01.md`.
- SHA256 del código que ejecutó la primera prueba: `5e47f6e63e98dd14655f8eeec0e8d826d97eb750fd24c099ea4b6aa3e50ea993` (`vision_ab_c01.py`). Fuente completa adjunta como artefacto descargable en la conversación, todavía no copiada a GitHub ni verificada en clon limpio.
- SHA256 resultados íntegros originales: `71cc4ca2b18360f83de5c61aaf2286fe25e6c19e76d14a30044bee6ca2cd9c18`.
- Tras VER el test se descubrió que `qmc.PoissonDisk(...).random(N)` concentraba lecturas en parte de la imagen. **Todos los resultados Poisson originales INVALIDOS**.
- ERRATA commit `728c8b86e0ba3d814ef51abfaff3b75495ed0042`, anterior únicamente a la REPARACIÓN, no a los outcomes.
- Código reparación SHA256 `85438d783f220761e1b5b8d2c678e2a77ee2787a2c7e5cbefac3b8d6d13c9570`; reparado con radius=.062, fill_space y eliminación del punto de mayor densidad hasta 160.
- SHA256 resultados reparados `45c502b20277839476576c5868d348a66567193d2d012a778217734a15fbd5b8`. Poisson reparado = EXPLORATORY_POSTEXPOSURE, NO confirmatorio.
- Raw JSON completo, scripts y figuras en ZIP de conversación, NO en GitHub. CLEAN_CLONE_NOT_VERIFIED.

## Experimento
13 imágenes skimage.data, nueve TEST reservadas para este script, cuatro DEV. No confirmar que sean completamente nuevas respecto al historial LARP. Seis semillas [1103,1109,1117,1123,1129,1151]. N=160 lecturas, 5 tipos iguales, 128x128, gris, mismos interpolador triangular/fallback, tres condiciones (clean, dropout30, ruido 0.08).

Brazos: grid, Sobol, PoissonDisk reparado, CVT por subtipo, MHU_PROXY_JOINT (potencia baja-k subtipo y unión), MHU_PROXY_SUB_ONLY (sin penalizar unión). Ni Wei auténtico ni ViT ejecutados. No es MHU asintótica certificada y las cinco etiquetas tienen la misma función gris. Unidad de independencia admisible: imagen original; seeds correlacionadas por imagen.

## Resultados MSE TEST (menor mejor)
| Método | Clean | 30% dropout | Ruido 0.08 |
|---|---:|---:|---:|
| grid | .013028 | **.014919** | .016479 |
| poisson_disk (reparado posthoc) | **.013014** | .015174 | **.016160** |
| mhu_joint | .013214 | .015340 | .016408 |
| mhu_subtypes | .013226 | .014929 | .016532 |
| sobol | .013484 | .015447 | .016870 |
| cvt_subtypes | .015904 | .017546 | .019722 |

Joint low-k union 6.2367e-08 versus subtypes-only 2.0382e-07; geometría mejor respecto a su objetivo, pero efecto MSE joint-subtypes: clean -0.000012, dropout +0.000411 (**peor**), ruido -0.000124. Joint no vence de modo sostenido grid/Poisson. Comparación con Wei y token aprendidos no instrumentada. El bootstrap por 9 imágenes es descriptivo, sin pretensiones confirmatorias. Error/noise/semillas por imágenes no son muestras externas.

## Interpretación A–J / R5
**A** Unidad fotografía y fidelidad de reconstrucción, NO capacidad de reconocer imágenes. **B** H1 coordinación conjunta contra nula/rivales grid, Poisson, Sobol, CVT. **C** N=160 y tres perturbaciones predefinidas. **D** SHA prereg y reparación explícita del brazo inválido. **E** corrida completa 6 semillas × 13 imágenes × 3 condiciones × 6 métodos. **F** sin Wei auténtico, no igualar generación, canales del mismo tipo, imagen no periódica, dataset restringido, error Poisson registrado. **G** no replicación externa. **H** prior de utilidad automática MHU en visual monomodal se debilita, prior de funcionalidad multimodal permanece sin probar. **I** no novedad 2/3, ninguna red visual entrenada. **J** STOP_LOCAL + PIVOT condicionado a observaciones nuevas y métodos competentes.

## Fuentes
- Jiao et al. 2014 retina aviar https://doi.org/10.1103/PhysRevE.89.022721
- Wei 2010 multicolor blue noise https://www.liyiwei.org/papers/noise-sig10/
- TokenLearner https://arxiv.org/abs/2106.11297
- DynamicViT https://proceedings.neurips.cc/paper/2021/hash/747d3443e319a22747fbb873e8b2f9-Abstract.html
- ToMe https://arxiv.org/abs/2210.09461
- Evidencia previa LARP `docs/AB06_REALDATA_20261022/DICTAMEN_AB06.md`, `docs/AB08_CROSSPHASE_20261022/DICTAMEN_AB08.md`, `research/AB30_DISCOVERY_20261022/reports/DICTAMEN.md`, `research/FINDINGS_1_3/LEDGER.json`.

## Siguiente dirección
No seguir gastando simulaciones iguales. Distinguir desplazamiento de fase conjunto (conservar espectros por subtipo) en **imágenes/canales funcionalmente distintos**, auténtico Wei 2010 y un ViT preentrenado bajo igual cómputo, benchmark independiente con miles de imágenes; medir exactitud, calibración, robustez, FLOPs y energía real. Solo entonces 20 ciclos branching podrían justificarse. **SOLICITO BRANCHING 20 CICLOS CONDICIONADOS A NUEVA EVIDENCIA.**
