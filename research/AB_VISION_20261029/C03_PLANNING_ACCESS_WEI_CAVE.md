# VISION C03 — PIVOT instrumental / planificación A–J, NO ciclo experimental
Fecha: 2026-10-29; estado `PLANNING_AB_ONLY`. No consumir plaza AB ni alegar ejecución Wei, CAVE o entrenamiento de ViT.

**A Pregunta:** ¿qué fuente original y rival publicado pueden permitir un contraste 2/3 de MHU como mosaico multisensor? Unidad: escena multiespectral original, replicación independiente por escena/dataset, no patches ni seeds.

**B Hipótesis de viabilidad:** H0 no hay acceso reproducible al cubo ni rival en este entorno; H1 existen fuentes oficiales públicas de escenas con bandas y código Wei auténtico, pero requiere descarga/portabilidad; H2 el mayor rival real son mosaicos espectrales aprendidos optimizados con decodificador (Li et al. WACV 2023), que puede dominar topologías fijas.

**C Datos y comparadores declarados:** CAVE Columbia, 32 escenas originales 512×512×31 bandas (400–700nm en pasos de 10nm); exacto original https://cave.cs.columbia.edu/repository/Multispectral ; espejo HF license metadata 'unknown' https://huggingface.co/datasets/danaroth/cave (NO presumir permiso de redistribución). Segundo dataset ICVL 202 escenas×31 bands (archivos enormes), https://huggingface.co/datasets/ICVL-BGU/ICVL_HS_2016 ; EPFL RGB-NIR 477 escenas 4 modalidades aproximadas https://www.epfl.ch/labs/ivrl/research/downloads/rgb-nir-scene-dataset/ . Rival Li-Yi Wei SIGGRAPH 2010 https://www.liyiwei.org/papers/noise-sig10/ y código https://github.com/1iyiwei/noise/tree/master/RainbowNoise. Código fuente real consultado con GitHub: RainbowNoise/CMakeLists.txt, src/Main/CMakeLists.txt, src/Main/DartThrowing.cpp, src/Library/CMakeLists.txt; incluye ejecutable DartThrowing con argumentos para `dimension num_classes priority r_values k_number domain_size`. CMake declara compatibilidad mínima 2.6 y mensaje sobre funciones Windows; compilación Linux es hipótesis, NO comprobada. Rival adicional: Li, Dai, Van Gool WACV 2023 https://openaccess.thecvf.com/content/WACV2023/html/Li_Jointly_Learning_Band_Selection_and_Filter_Array_Design_for_Hyperspectral_WACV_2023_paper.html ; Bian et al. IEEE TIP 2021 DOI 10.1109/TIP.2021.3108913.

**D Auditoría de instrumentos:** Se inspeccionaron README, archivo raíz CMake, CMake de ejecutables y código DartThrowing; no se clonó ni compiló ni ejecutó. CAVE oficial responde metadatos web pero este entorno no pudo descargar ZIP originales (red del contenedor no resuelve host; URL binaria no quedó accesible mediante herramienta). Los metadatos 32×31 NO equivalen a observaciones en mano. En GitHub no redistribuir datos hasta verificar términos de origen.

**E Resultado de la investigación documental:** fuente primaria y código fuente original identificados; **ningún benchmark MHU-WEI fue ejecutado**. Nuevas vías son técnicamente específicas y pertinentes, pero siguen bloqueadas por adquisición y compilación.

**F Auditoría adversarial:** prior art de multicolor blue noise precede LARP; la comparación con Poisson+maximin NO es Wei; learned MSFA CFA y reconstructor joint 2023 pueden explicar ventajas no geométricas; investigación en 5 filtros RGB virtuales no es 5 espectros ópticos.

**G Confirmación:** NO ejecutada; no confundir enlaces a GitHub con pipeline reproducida. Futuro test ciego preferiblemente imagen-level, train/val/test por escena completa; prior art check y derechos antes de download.

**H Priors:** P-VIS09 ampliado: antecedente 2023 de diseño conjunto banda/mosaico/reconstrucción sube exigencia de control. Fuente nueva para metodología pero NO sube CT2 de ventaja MHU.

**I Dictamen:** Originalidad 2/3 NO acreditada; la incertidumbre predominante ahora es instrumental, no número de semillas. Calidad de documentación primaria alta para existencia, calidad de ejecución nula.

**J AB-DECIDE:** PIVOT condicionado a acceso de cubos 31 bandas y compilación validada de RainbowNoise. No repetir mismas simulaciones RGB. **PLANNING_AB_ONLY**, no consume las 19 plazas restantes.

## Tarea reproducible para ejecutor compatible
1. Descargar legalmente 3 escenas CAVE de tres categorías diferentes con sus 31 PNG 16-bit (sin aceptar términos nuevos por el usuario). Guardar URL exacta, licencia/permiso y SHA256 de origen; no exponer/redistribuir bytes originales del dataset en repo.
2. Clonar https://github.com/1iyiwei/noise en commit fijo; identificar target `DartThrowing`/mejor soft-disk, entorno, patches necesarios, seed/aleatoriedad, y producir imagen simple de 5 clases N=160; medir cuotas, espectros conjuntos e individuales, coste de generación; portar solo si es legal y comparable. Si falla compilación, conservar log y STOP en esa puerta.
3. Solo tras superar los pasos anteriores crear prereg A–J con código íntegro y SHA en GitHub **antes** de outcomes para evaluar CAVE: grilla, Sobol, Wei auténtico, MHU individual/joint, patrones con fases rotas; medir MSE/PSNR multibanda, robustez, n muestras y tiempo/FLOPs de decoder, pérdidas 20%.
4. No iniciar ViT/CNN costosa o 20 loops por inercia. R5 detener si el control publicado domina y no existe intervención nueva que discrimine mecanismos.
