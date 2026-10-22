from pathlib import Path
import json,hashlib,datetime,zipfile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.scale3d_geometry import reciprocal_modes
R=Path(__file__).resolve().parents[1];D=R/'data';DOUT=R/'docs';FG=R/'figures';FG.mkdir(exist_ok=True)
read=lambda f: json.loads((D/f).read_text());c2=read('C02.json');c3=read('C03.json');c4=read('C04.json');c5=read('C05.json');c6=read('C06.json');control=read('C06_controls.json')
name_order=['local','mhu','cvt','sobol','random','pixel_mlp'];display={'local':'LOCAL','mhu':'MHU','cvt':'CVT','sobol':'Sobol','random':'Aleatoria','pixel_mlp':'MLP píxeles','blur64':'MLP píxeles suavizados','blur_pool80':'MLP promedio 4×4'}
clean={n:np.array([a['result']['test_acc'] for a in c4['outcomes'] if a['name']==n]) for n in name_order}
rob={n:{k:float(np.mean([a['accuracy'][k] for a in c6['measures'] if a['method']==n])) for k in ['clean','gaussian_noise','block_occlusion','rotation_pm12']} for n in name_order}
rob.update({n:{k:float(np.mean([a['accuracy'][k] for a in v])) for k in ['clean','gaussian_noise','block_occlusion','rotation_pm12']} for n,v in control['conditions'].items()})
geom={n:float(np.mean([r['coverage'][n]['2d'] for r in c2])) for n in name_order if n!='pixel_mlp'}
mode,_=reciprocal_modes(128)
spec={n:[] for n in geom}
for seed in [8101,8102,8103,8104]:
 z=np.load(D/f'geo_{seed}.npz')
 for n in geom:
  p=z[n];spec[n].append(float(np.mean(abs(np.exp(2j*np.pi*p@mode.T).mean(0))**2)))
summary={'design':{'N':128,'geometry_seeds':[8101,8102,8103,8104],'geometry_dimensions':3,'image_dimensions':2,'original_geometry_steps':600,'UCI_digits_samples':1797,'external_to_geometry_optimization':True,'Wei_original_executed':False,'neural_MLP_parameters':5834,'baseline_MLP_parameters':5860,'test_size':450,'holdout':True},'finite_spectrum_3d':{n:{'mean':float(np.mean(s)),'seeds':s} for n,s in spec.items()},'coverage_2d_five_types_k8':geom,'clean_specialized_test_accuracy':{n:{'mean':float(clean[n].mean()),'sd':float(clean[n].std(ddof=1)),'seeds':clean[n].tolist()} for n in clean},'functional_role_delta':c5['mean_delta'],'robustness_test_accuracy_intensity_only':rob,'comparison_note':'Small n=4 geometry seeds, same test images and exact Image transforms; test examples not independent geometry replicates.'}
(D/'SUMMARY_AB06.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
plt.figure(figsize=(9,5))
for i,n in enumerate(name_order):plt.bar(i,clean[n].mean()*100,yerr=clean[n].std(ddof=1)*100,capsize=4)
plt.xticks(range(len(name_order)),[display[x] for x in name_order],rotation=15);plt.ylabel('Exactitud en test (%)');plt.ylim(88,100);plt.title('C04 — Dígitos UCI: cinco tipos y MLP convencional');plt.grid(axis='y',alpha=.2);plt.tight_layout();plt.savefig(FG/'C04_accuracy.png',dpi=180);plt.close()
plt.figure(figsize=(9,5))
for i,n in enumerate(name_order):plt.bar(i,c5['mean_delta'].get(n,0)*100)
plt.xticks(range(len(name_order)),[display[x] for x in name_order],rotation=15);plt.ylabel('Especializados − todos intensidad (puntos %)');plt.title('C05 — Ablación de especialización sensorial');plt.grid(axis='y',alpha=.2);plt.tight_layout();plt.savefig(FG/'C05_roles.png',dpi=180);plt.close()
labels=['LOCAL','MHU','CVT','Sobol','Aleatoria','MLP píxeles','MLP suavizado','MLP 4×4'];keys=name_order+['blur64','blur_pool80']
plt.figure(figsize=(10,5.5));x=np.arange(len(keys));w=.29
for i,(task,desc) in enumerate([('rotation_pm12','Rotación ±12°'),('gaussian_noise','Ruido σ=0,17'),('block_occlusion','Oclusión 2×2')]):
 plt.bar(x+(i-1)*w,[rob[n][task]*100 for n in keys],w,label=desc)
plt.xticks(x,labels,rotation=30,ha='right');plt.ylabel('Exactitud en test perturbado (%)');plt.ylim(0,100);plt.title('C06 — Transferencia a perturbaciones no entrenadas');plt.legend();plt.grid(axis='y',alpha=.2);plt.tight_layout();plt.savefig(FG/'C06_robustness.png',dpi=180);plt.close()

ledger='''# Ledger AB 3.2.1 — 6 ciclos focalizados LARP, 22-10-2026

**Evidencia exploratoria:** todas las comparaciones neuronales son pruebas sobre un dataset real de 1797 imágenes, pero las cuatro geometrías son réplicas de construcción, no cuatro datasets. Los controles C06 adicionales son REPAIR dentro de C06, no C07. Cada próximo paso se seleccionó después de inspeccionar el anterior; los scripts para ciclos posteriores fueron escritos progresivamente.

'''
entries=[
('C01','¿Existe un comparador Wei original ejecutable aquí?','El repositorio público original 1iyiwei/noise/RainbowNoise contiene fuentes y CMake, README indica VS .NET 2003; el acceso disponible permite inspeccionar código pero no ha proporcionado un ejecutable validado para Linux/3D/5 tipos/N comparable.','Implementación propia o CVT podrían hacerse pasar por Wei.','BARRERA_DE_EJECUCIÓN_WEI / PIVOT','Probar transferencia a datos reales, manteniendo Wei como comparador pendiente.','Auditoría fuente: https://github.com/1iyiwei/noise/tree/master/RainbowNoise/src ; no afirmar que Wei sea imposible en general; únicamente no ejecutado ni validado en esta sesión.'),
('C02','¿Podemos generar realizaciones independientes sin reutilizar las cuatro antiguas?','Cuatro semillas nuevas 8101–8104, N128, 600 iteraciones auténticas por LOCAL/MHU, init/labels pareadas y verificadas con modo 0 iteraciones. Bajo proyectar a plano, la cobertura de cinco tipos k=8 varía y CVT/Sobol a menudo mejoran MHU. Auditoría Fourier de 40 modos 3D sí comprueba supresión en MHU.','El hallazgo Fourier procede solo del objetivo; proyectar 3D a 2D puede destruirlo.','CONTINUE_CON_LIMITACION','Fijar benchmark no Fourier sobre estas geometrías independientes.','N reducido frente a N4096 histórico; optimizador v2 original archivado, validate=False, espectro exacto añadido ex post; CVT construido y declarado no equivale a Wei.'),
('C03','¿Produce la distribución MHU un muestreo espacial útil sobre imágenes reales?','UCI Digits 1797 imágenes 8×8; 5 roles intensidad/blur/dx/dy/Laplaciano suavizado, lectura en coordenadas geométricas y RBF a grid 4×4. Reconstrucción de gris N128 sin ganador sistemático MHU.','Quizá la red aprende diferencia que MSE de reconstrucción no capta.','CONTINUE','Entrenar MLP equiparados con píxeles y validar convergencia.','No se entrenó geometría usando etiquetas ni imágenes; imputación por RBF e interpolación son decisiones comunes, pero no CVT/Wei igualados en coste.'),
('C04','¿Supera LARP a redes convencionales en clasificación real con parámetros semejantes?','20 MLP sobre geometrías y cuatro MLP pixel baseline. Mejora MHU no demostrada: MHU 94.94% vs LOCAL 95.06%, Sobol 96.11%, píxeles 96.78%.','Diferencias de operator de los roles, no solo geometría.','PIVOT_TO_ROLE_ABLATION','Mantener mismas nubes y sustituir roles diferentes por intensidad común.','~5834 parámetros geométricos vs ~5860 píxel (0.45% diferencia); 240 pasos máximos y early stopping val; algunas carreras seleccionan último paso, por lo que no afirmar convergencia completa; solo 4 geometrías.'),
('C05','¿Aporta ventaja la especialización funcional de tipos frente a roles redundantes?','Cada muestra preserva las mismas posiciones, etiquetas, canales y parámetros; reemplazar funciones diferentes por intensidad en los cinco tipos mejora MHU en 1.56 puntos de media y LOCAL en 1.11; para Sobol diferencias pequeñas.','El conjunto de transformaciones no necesariamente aporta información discriminante independiente.','PIVOT_TO_ROBUSTNESS','Probar intensidad común y comparadores de preprocesado bajo corrupción nueva.','Ablación altera simultáneamente la información disponible y la semántica de roles; no prueba que la especialización sea inútil para otras tareas.'),
('C06','¿Sobreviven diferencias de aprendizaje a desplazamientos de distribución y baselines de preprocesado?','Con intensidad y modelos congelados, LOCAL 73.17% vs MHU 71.39% en rotación ±12°, LOCAL 91.00% vs MHU 90.39% con ruido. Pixel MLP raw 33.33% rotación, pero blur64 controla parte de diferencia (48.72%); rol de representación vs geometría no identificado completamente.','Los filtros y el pooling, no la hiperuniformidad, podrían explicar toda la robustez.','CLOSE_NO_NOVELTY_REQUEST_CONDITIONAL','Exigir 2D nativo, Wei ejecutable y un problema con múltiples canales realmente informativos antes de ampliar.','Dataset test original y perturbaciones no son datasets independientes; tamaño e inductive bias no totalmente pareados; comparador blur usa todos los píxeles, no igual presupuesto sensores. No prueba 2/3 ni 3/3.')]
for cid,q,o,r,d,n,l in entries:
 ledger+=f'### {cid} — {q}\n**Observación:** {o}\n\n**Rival/falsador:** {r}\n\n**Decisión AB:** {d}. **Siguiente pregunta:** {n}\n\n**Límites:** {l}\n\n'
(DOUT/'01_LEDGER_AB06.md').write_text(ledger)
md='''# LARP/MHU — seis ciclos con datos reales y falsación de ventaja neuronal

**Fecha:** 22-10-2026. **Estado:** C01-C06 cerrados, exploratorios. **2/3:** no acreditado. **3/3:** no acreditado. **Evaluación nativa de Li-Yi Wei:** no realizada (BARRERA_DE_EJECUCIÓN).

## 1. Qué cambió

Se abandonaron los campos Fourier sintéticos: UCI Optical Recognition of Handwritten Digits (copia sklearn; 1797 imágenes de 8×8, 10 dígitos). Se generaron cuatro semillas **nuevas** de n=128, con funciones originales Scale3D LOCAL y MHU v2 durante 600 iteraciones; también CVT por tipo, Sobol por tipo y azar. Las geometrías 3D se proyectaron al espacio 2D de imagen. Ésta es deliberadamente una prueba de transferencia fuera del dominio geométrico de construcción, no un benchmark de point clouds 3D.

Una clase sensorial mide intensidad, otra suavizado, otra gradiente horizontal, otra gradiente vertical y otra Laplaciano suavizado. Se proyectan 128 lecturas por imagen en 80 características (5 tipos × 4×4 celdas por RBF). Un MLP con 5834 parámetros aprende la clase de dígito. Baseline: MLP directamente sobre 64 píxeles, 5860 parámetros. Mismos índices train/val/test estratificados, hasta 240 actualizaciones AdamW de lote completo; checkpoint escogido por val loss y test solamente evaluado después. Sin GPU y sin datos de entrenamiento derivados de Fourier.

## 2. Resultados observados

### Filtro espectral sigue funcionando sin predecir rendimiento neuronal

'''
for n in ['mhu','local','sobol','cvt','random']:
 md+=f'- {display[n]}: potencia normalizada Fourier 3D media {summary["finite_spectrum_3d"][n]["mean"]:.6g}; cobertura proyectada de cinco tipos entre 8 vecinos {geom[n]*100:.1f}%.\n'
md+='\n### Clasificación clean (test; media de cuatro geometrías, para pixel cuatro inicializaciones)\n\n| Método | Exactitud media | Desviación estándar entre geometrías / inicializaciones |\n|---|---:|---:|\n'
for n in name_order:md+=f'| {display[n]} | {clean[n].mean()*100:.2f}% | {clean[n].std(ddof=1)*100:.2f} puntos |\n'
md+='\n**MHU frente a LOCAL:** diferencias pareadas por geometría '
md+=', '.join(f'{(a-b)*100:+.2f} pp' for a,b in zip(clean['mhu'],clean['local']))+'. n=4 pequeño; sin ventaja robusta ni equivalencia estadística acreditada. **Sobol** y los píxeles originales superan MHU en la media. Algunos modelos lograron mejor checkpoint en el paso 240: el presupuesto no garantiza convergencia final. No se igualaron el coste de generación ni los FLOPs de codificación sensorial.\n\n'
md+='### Ablación de roles: cinco operadores frente a cinco copias de intensidad\n\n'
for n in ['mhu','local','cvt','sobol','random']:md+=f'- {display[n]}: especializados menos homogéneos = {c5["mean_delta"][n]*100:+.2f} puntos porcentuales.\n'
md+='\nLa heterogeneidad funcional no genera una ventaja automática; el filtro puede eliminar señales discriminantes de la imagen.\n\n'
md+='### Robustez (solo intensidad, protocolo de entrenamiento cerrado)\n\n| Método | Clean | Ruido gaussiano σ=0,17 | Oclusión 2×2 | Rotación ±12° |\n|---|---:|---:|---:|---:|\n'
for n in name_order+['blur64','blur_pool80']:
 a=rob[n];md+=f'| {display[n]} | {a["clean"]*100:.2f}% | {a["gaussian_noise"]*100:.2f}% | {a["block_occlusion"]*100:.2f}% | {a["rotation_pm12"]*100:.2f}% |\n'
md+='''
**Interpretación:** algunos codificadores basados en sensores tienen más tolerancia a ruido y rotación que el MLP de píxeles directos. Pero LOCAL suele superar MHU en esos shifts, Sobol cambia su posición y un MLP con píxeles suavizados recupera parte de la resistencia. No atribuir estas diferencias a MHU, porque los codificadores espaciales incluyen filtrado/RBF y el comparador suavizado utiliza píxeles completos. Son pruebas de *pipeline* con representación distinta, no una igualdad exhaustiva de FLOPs, información y lecturas.

## 3. Comparador clásico Wei y límites

El código original de **Li-Yi Wei, Multi-Class Blue Noise Sampling (SIGGRAPH 2010)** está público en https://github.com/1iyiwei/noise/tree/master/RainbowNoise/src; su README indica compilación histórica con Visual Studio .NET 2003 y ejemplo de DartThrowing. Se auditaron sus fuentes, pero **NO se obtuvo ni ejecutó una implementación Wei validada en 3D N=128 ni se compararon runtimes**. CVT/Sobol son comparadores clásicos ejecutados, pero no sustitutos etiquetables como Wei. Se conserva BARRERA_DE_EJECUCIÓN_WEI en el registro metodológico.

El benchmark de dígitos procede de observaciones reales, pero sigue siendo un único dataset pequeño; la lectura geométrica proyectada 3D→2D es inadecuada para inferir utilidad en 3D, y las 4 geometrías no bastan para inferir generalidad. Baselines de CPU con parámetros cercanos ≠ presupuesto total computacional exactamente igual. Los intentos de buscar ventaja de novedad 2/3/3/3 **fallan**.

## 4. Decisión y solicitud

**AB-DECIDE: STOP a la hipótesis de superioridad directa de la disposición MHU original en aprendizaje de dígitos y a seguir reciclando pruebas Fourier.** Conservar la propiedad de coordinación espectral intertipo como característica geométrica útil y conocida; de este bloque rescatar la utilidad potencial del *pipeline sensorial robusto*, que aparece en distintas geometrías y por tanto NO identifica una contribución específica de MHU.

**SOLICITO PIVOT 4 CICLOS**, condicionados a disponer de: (a) datos espaciales 3D reales o un benchmark point-cloud estable que no sea proyección 8×8; (b) entrenamiento convergido de al menos una red sobre esos datos; (c) implementación real de Wei o baseline equivalente **claramente etiquetado** y (d) igualación de sensores, información y FLOPs, no solo parámetros. El primer ciclo tendría que resolver disponibilidad técnica; si no, registrar STOP y no fabricar evidencia ni gastar ciclos vacíos.

## Trazabilidad

- C01: auditoría de fuentes públicas Wei y ejecutabilidad.
- C02: `src/cycle2_geometry.py`, `data/geo_8101..8104.npz` y `data/C02.json`.
- C03: `src/cycle3_digits.py`, dataset `digits_split.npz`, `digits_features_*`, `data/C03.json`.
- C04: `src/cycle4_train.py`, `data/C04.json`, test accuracy y curvas val completas.
- C05: `src/cycle5_roles.py`, `data/C05.json`.
- C06: `src/cycle6_robust.py`, `src/cycle6_controls.py`, `data/C06.json`, `data/C06_controls.json`; la segunda ejecución fue un REPAIR de confusión por preprocesado, no un séptimo ciclo.

- Fuente sobre dataset: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html
- Prior art: https://www.liyiwei.org/papers/noise-sig10/ y https://github.com/1iyiwei/noise
'''
(DOUT/'02_DICTAMEN_AB06.md').write_text(md)
pri='''# Priors acumulativos BR06-R (no sustituyen al ledger maestro)

| ID | Proposición | Evidencia a favor | Evidencia adversa | Grado/alcance |
|---|---|---|---|---|
| BR06-R01 | Generador auténtico Scale3D produce MHU finita también en N128 | C02: cuatro nuevas semillas y Fourier 3D mucho menor que LOCAL | Objetivo explícito; validate=False y tarea 2D; no demuestra HU asintótica | Observación finita verificada |
| BR06-R02 | La geometría MHU otorga mejor clasificación real | Ninguna victoria general | C04 MHU 94,94%, Sobol 96,11%, MLP píxel 96,78%; n=4 | Debilitada, no general |
| BR06-R03 | Cinco funciones sensoriales heterogéneas mejoran el aprendizaje | Hipótesis de complementariedad | C05 roles distintos empeoran MHU ≈1,56 pp respecto a mismas cinco funciones de intensidad | Refutada para este operador/dataset |
| BR06-R04 | La representación sensorial espacial puede incrementar robustez a rotación y ruido | C06 supera al MLP directo pixel en varios shifts | Baselines suavizados reducen la brecha; no está aislado efecto MHU | Abierta para otro dominio, confusión reconocida |
| BR06-R05 | MHU tiene robustez específica frente a LOCAL | C06 en alguna semilla | Medias LOCAL superiores MHU en rotación y ruido; semillas heterogéneas | No validada |
| BR06-R06 | Wei original disponible y ejecutado como baseline | Repositorio público confirmado | README VS2003, no binario ejecutado ni comparabilidad con N128 | BARRERA_DE_EJECUCIÓN, fuente localizada |
| BR06-R07 | MHU en 3D transferida por proyección 2D preserva todas sus ventajas | Fourier 3D finito fuerte | Reconstrucción y clasificación en 2D sin dominio MHU | Hipótesis debilitada para proyección |

Procedencia: `docs/01_LEDGER_AB06.md`, scripts `src/cycle*`, datos `data/C0*.json`; todos resultados exploratorios, NO Bayes factors. Conservar las entradas BR08-X01..X06 y BR30-F01..F10 previas.
'''
(DOUT/'03_PRIORS_AB06.md').write_text(pri)
method='''# Observaciones para Metodología AB — 22-10-2026

**Fuente:** LARP AB06 seis ciclos, dataset UCI Digits y repo privado `GalexY3/proyecto-LARP`; no cambiar la versión de AB automáticamente.

**AB-M020 — GATE de dimensionalidad y observabilidad.** Un patrón 3D con regularidad espectral confirmada no tiene garantizada la misma propiedad cuando se proyecta a imágenes 2D. Solicitar documento que identifique la dimensión y simetrías de la tarea, geometría original, proyección/embedding y observabilidad de cada rasgo. Falsador: en casos donde la proyección sí preserve la métrica relevante el gate debe permitirlo sin penalidad. Estado: propuesta.

**AB-M021 — GATE de información sensorial vs igualdad de parámetros.** Modelos de ≈5800 parámetros pueden recibir distinta cantidad y transformación de información: intensidad, derivadas, interpolación RBF y suavizado por tipo. Antes de inferir ventaja de arquitectura, equiparar contenido, costo de lectura, preprocesado y FLOPs; agregar baselines de identidad y preprocess+MLP. Reparación detectada en C06: MLP píxel suavizado mejora robustez. Estado: propuesta.

**AB-B011 — Conservar negativos de roles especialistas sin forzar complementariedad.** La hipótesis intuitiva de roles tipados tuvo una refutación clara en datos externos a Fourier: las cinco transformaciones fueron peores que cinco lecturas de intensidad en la mayoría de semillas. Beneficio metodológico de ablación controlada de semántica y geometría por separado. Límite: no invalida roles en todos los dominios. Estado: práctica prometedora.

**AB-M022 — Auditoría de comparador fuente ≠ ejecutable.** Localizar repo original no es ejecutar ni validar a igual coste. Registrar `SOURCE_LOCATED`, `BUILD_SUCCESS`, `SMOKE_PASS`, `DATA_COMPARABLE`, `RUNTIME_BUDGET_MATCHED` como gates separados. C01 fuente Wei 2010 localizada pero no compilación validada. Estado: propuesta.
'''
(DOUT/'04_NOTA_AB.md').write_text(method)
(R/'README.md').write_text('''# LARP / AB 3.2.1 — seis ciclos con UCI Digits (22-10-2026)

Investigación exploratoria. **No confirma 2/3 ni 3/3**. No equipara a Wei, Transformer ni GPT.

Ejecutar desde directorio raíz:

```bash
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle2_geometry
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle3_digits
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle4_train
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle5_roles
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle6_robust
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle6_controls
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.build_dossier
```

Deps: numpy scipy scikit-learn torch matplotlib. GPU no requerida. Fuente `src/scale3d_geometry.py` y v2 recuperada de archivo LARP anterior; se conserva intacta. Dataset UCI Digits se puede redistribuir aquí desde sklearn; labels por muestra, splits y features cacheadas. 4 geometrías originales independientes y 4 semillas de modelo en baseline. Estadística de geometría n=4, no 1797.

Ver `docs/02_DICTAMEN_AB06.md` para interpretación, `docs/01_LEDGER_AB06.md` decisiones, `docs/03_PRIORS_AB06.md` priors.
''')
manifest={}
for p in R.rglob('*'):
 if p.is_file() and not ('__pycache__' in str(p)) and p.name!='MANIFEST_SHA256.json':manifest[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2))
print('Wrote',len(manifest),'files, clean', {n:round(float(v.mean()),4) for n,v in clean.items()})
