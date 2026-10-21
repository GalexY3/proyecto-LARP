from pathlib import Path
import json,hashlib,zipfile,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
A=lambda name:json.loads((R/'data'/name).read_text())
coverage=json.loads((R/'logs'/'coverage.json').read_text());q512={k:coverage[k]['mean'] for k in coverage if k.endswith("'cover')")}
orig=A('fast_4096.json');pred=A('predict_4096_summary.json');bw=A('bandwidth_heldout_summary.json');learn=A('learned_specialists.json');drop=A('dropout_4096.json');spec=A('spectrum_finite.json');access=A('access_comparison.json')
# 12 substantive questions ordered by evidence and documented in local chronology.
cycles=[
('01','Prior art','¿Es nueva la disponibilidad local de múltiples clases y qué baseline es genuino?',
 'Wei 2010 ya define sampling multiclase en dimensiones arbitrarias, con código original; avian-patterns-lab es 2D y pequeño. No se ejecuta el código original Wei aquí.',
 'H_nueva: propiedad única de LOCAL; H_W: multi-class blue noise preexistente. Evidencia fuerte a favor de H_W.',
 'PIVOT','Inspeccionar realizaciones independientes y evitar usar nombre Wei para un control propio.'),
('02','Replicación geométrica','¿Podemos generar patrones independientes y no depender de una sola geometría?',
 '12 semillas independientes × cuatro procedimientos con N=512 y cinco tipos, cuotas [209,109,87,64,43]. LOCAL_derived sólo implementa una repulsión local inspirada, no el optimizador original de Scale3D.',
 'H: se pueden generar geometrías comparables; H_alt: extrapolación entre implementaciones. Limitación: reconstrucción no es réplica algorítmica.',
 'REPAIR','Medir cobertura con CVT por tipo y no adjudicarle resultados al LOCAL original.'),
('03','Cobertura independiente','¿LOCAL derivado conserva la ventaja ante un baseline espacial robusto?',
 'Con 16 vecinos y 12 geometrías nuevas: IID 61.43%, stratified 77.41%, LOCAL_derived 69.17%, CVT per-type 97.31%. CVT domina en esta implementación.',
 'H_LOCAL, H_CVT, H_null. Conclusión dependiente de versión LOCAL_derived y N512; no refuta Scale3D original.',
 'PIVOT','Revisar N4096 con coordenadas auténticas, no extender conclusión al original.'),
('04','Escala original 4096','¿CVT puede rivalizar con las coordenadas LOCAL originales al mismo N y cuotas?',
 'N4096: ORIGINAL_LOCAL cobertura k16=96.08%, MHU=95.28%; seis CVT con 8 iter. cobertura k16 entre 94.72% y 96.52%. Solo una LOCAL original.',
 'H_cobertura_L > CVT; H_CVT≈L; H_seeds. Requiere convergencia del comparador antes de discriminar.',
 'REPAIR','Aumentar iteraciones CVT; no interpretar una línea base suboptimizada como victoria.'),
('05','Convergencia de baseline','¿Optimizar CVT altera la comparación?',
 'Con 15 iteraciones adicionales en tres CVT independientes: cobertura k16=97.64%, 97.68%, 97.56% > LOCAL original 96.08% (consulta común; no inferencia entre generadores LOCAL).',
 'H_LOCAL persistentemente mejor; H_competidor subentrenado. Se debilita H_LOCAL. Sin Wei todavía.',
 'PIVOT','Examinar efecto en MSE real, no solo cobertura kNN.'),
('06','Reconstrucción con kernel fijo','¿La ventaja inicial LOCAL sobre CVT persiste en una tarea multicanal?',
 'f1,k24,bandwidth=.11: LOCAL original MSE=.14040; CVT seis geometrías no refinadas media=.15424; RANDOM .39909; MHU=.15709. Ventaja descriptiva LOCAL sobre CVT suboptimizado (~9%).',
 'H_LOCAL funcional; H_parametrización kernel; H_CVT por optimizar. El estimador conoce los tipos y la fórmula objetivo.',
 'CONTINUE','Variar la suavidad antes de atribuir un mecanismo universal.'),
('07','Escala de señal','¿La ventaja se extiende a señales espaciales de frecuencia media o alta?',
 'Con kernel fijo y f5,k16: CVT seis geoms media 2.4708 < LOCAL 2.5151; f2,k24 CVT media .9692 vs LOCAL .9658 prácticamente empate. Los MSE altos indican error considerable en frecuencia 5.',
 'H_suavidad condiciona ventaja vs H_geometría universal. La diferencia cambia con frecuencia. Diseño exploratorio.',
 'PIVOT','Optimizar bandwidth con desarrollo y aplicar a mundos retenidos por método.'),
('08','Control de estimador','¿La pequeña ventaja LOCAL sobre CVT era artefacto de bandwidth?',
 'Bandwidth elegido individualmente por mínima MSE en ocho mundos dev; doce mundos heldout: f1 LOCAL=.1074, CVT refinados .0893–.0922, MHU=.1181; f2 LOCAL=.7274, CVT refinados .6945–.7167. Un MSE condicionado al generador, no generalización externa.',
 'H_LOCAL mejor a estimador comparable; H_CVT mejor con tuning justo; H_nula. La ventaja LOCAL NO sobrevive este control.',
 'STOP (superioridad geométrica)','Comprobar si acceso semánticamente tipado proporciona una vía independiente de la geometría.'),
('09','Acceso por tipo','¿Elegir vecinos expresamente por tipo mejora la tarea con presupuesto de señales reducido?',
 'Con f1: acceso global k16 LOCAL MSE=.1142; oráculo 1 por tipo (5 lecturas) LOCAL=.3160; CVT refinados global ~.095–.100, oráculo ~.306–.318. Buscar 5 árboles no equivale a coste global; ventaja de asegurar tipos no compensa pérdida de redundancia al interpolar.',
 'H_estratificar siempre es mejor; H_varianza por 1 muestra/tipo; resultados niegan H_estratificar en esta configuración.',
 'STOP (oráculo de 1 por tipo)','Si cobertura no basta, probar composición aprendida en vez de fórmula incorporada.'),
('10','Composición aprendida','¿Cinco especialistas aprendidos cambian ranking de geometrías?',
 'MLP 5→48→48→1 (3 inicializaciones) entrenado en mundos distintos: MSE test LOCAL=.1478; CVT refinados .1249–.1319; MHU=.1608; RANDOM=.5298. Interpolación con composición analítica sobre mismos campos supera al MLP.',
 'H_LOCAL neural; H_CVT + representación 5 canales; H_sesgo. Modelo no es Scale3D GNN ni Transformer; datos Fourier sintéticos.',
 'STOP (claim LARP > CVT)','Comprobar perturbaciones por pérdida de sensores; beneficio puede depender de densidad.'),
('11','Tolerancia a fallos','¿CVT/LOCAL muestran ventajas robustas con dropout de sensores?',
 'f1,k16,band=.05,12 mundos: al 0% LOCAL=.1294, CVT refinados .0993–.1059; al 60% LOCAL=.5311, MHU=.4742 y CVT refinados ~.498; todas empeoran. Ningún vencedor uniforme al borrar 60%.',
 'H_CVT uniforme; H_beneficio condicionado por disponibilidad. Comparación condicionada a una LOCAL y tres CVT; dropout igualado por índices no exactamente espacial.',
 'PIVOT','Verificar si el rasgo espectral definitorio MHU conserva valor diferenciado, sin confundirlo con reducción de MSE.'),
('12','Auditoría espectral y cierre','¿La supresión espectral MHU es el factor necesario para la ventaja funcional?',
 'Sobre 80 vectores Fourier discretos de norma <=2.5: S_all medio MHU=4.35e-6, LOCAL=.00294, CVT refinado .051–.090, RANDOM=1.16. MHU suprime mucho más; CVT refinado predice mejor las señales suaves. No hay demostración asintótica de HU.',
 'H_espectro global necesario para predicción suave; H_cobertura y precisión local son suficientes en esta tarea. Se debilita necesidad de la penalización espectral.',
 'STOP (línea concreta); sin extensión automática','Cerrar 12/12; +12 autorizados NO activados por falta de nuevo comparador genuino Wei, nuevas LOCAL originales y validación externa.')]

HEADER='''# LARP — AB 3.2.1 | BR12 dinámico (12 decisiones documentadas)

**Fecha:** 21-10-2026. **Autorización:** 12 ciclos y hasta 12 más condicionados a necesidad. **Estado:** 12 preguntas sustantivas evaluadas, 12 decisiones; las ampliaciones no utilizadas. Un ciclo aquí es pregunta + contraste/auditoría + decisión que orienta el siguiente, NO una semilla/valor de k. Se conservan errores y desviaciones del plan. **Todos los ensayos numéricos nuevos son exploratorios**, aunque algunos usan mundos nuevos después de ajustar en desarrollo; no hay registro confirmatorio previo específico que permita reclamar confirmación externa.

**Ojo:** la cronología corresponde a sucesivas decisiones durante esta sesión; los scripts de C04–C12 se añadieron tras observar pruebas previas. Sólo el código inicial `src/dynamic_research.py` fue subido a GitHub *antes* de la primera comparación nueva. No hay continuidad de optimizador entre LOCAL_derived (N512) y LOCAL_original (N4096). Se conserva explícitamente el código de cada brazo en el paquete.

## Convención A-J
A = pregunta/unidad, B = hipótesis rivales, C = protocolo/predecisión, D = instrumentación, E = medida, F = falsadores, G = confirmación, H = actualización cualitativa, I = dictamen/alcance, J = decisión y siguiente pregunta. No se han abierto 12 holdouts independientes. Parar si no existe ganancia informativa.
'''
lines=[HEADER]
for i,(id,branch,q,evidence,rivals,dec,nxt) in enumerate(cycles):
 lines.extend([f'## C{id} | {branch}',f'**A — Pregunta:** {q}', '**B — Rivales / D — Instrumentación:** '+rivals,
 '**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).',
 f'**E — Observación:** {evidence}',
 '**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.',
 '**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.',
 f'**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.',
 f'**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.',
 f'**J — AB-DECIDE:** **{dec}**. **Siguiente ciclo decidido a partir de esta evidencia:** {nxt}',''])
lines+=['## Dictamen acumulativo',
 'LOCAL y MHU muestran cobertura funcional alta frente a iid y estratificado simple. Un CVT per-type convencional, cuando se refina y optimiza el interpolador con datos de desarrollo separados, iguala o supera en tareas suaves al LOCAL original fijo en los casos medidos. Esto **NO prueba** que el optimizador LOCAL original sea inferior a CVT: solo hay una realización original; el estimando entre generadores está sin identificar. La supresión espectral de MHU sobre modos finitos está observada, pero no es necesaria para la ventaja predictiva en este simulador.',
 'Originalidad 2/3 y 3/3: **NO**; no existe validez externa y no se ha ejecutado genuinamente Wei 2010. No hay comparación neuronal Scale3D completa ni con Transformer en este bloque.',
 'Desglose presupuesto: 12/12 iniciales consumidos como decisiones sustantivas; los 12 adicionales quedan disponibles en la autorización del usuario, pero no se activan por ausencia de nueva clase de evidencia o comparador sin implementar. Escalar sólo con el código original repetible LOCAL y baseline Wei correcto, un nuevo dataset externo o GPU para entrenamiento controlado.',
 '## Fuentes y código','- Wei 2010 https://www.liyiwei.org/papers/noise-sig10/ ; código https://github.com/1iyiwei/noise/tree/master/RainbowNoise','- Precedente LARP BR30: https://github.com/GalexY3/proyecto-LARP/blob/main/docs/00_DICTAMEN.md',
 '- Prerregistro dinámico: https://github.com/GalexY3/proyecto-LARP/blob/main/prereg/BR12_DYNAMIC_20261021.md',
 '- El paquete `src/` incluye el código completo, las semillas y el generador derivado; `data/` los cálculos tabulados y las coordenadas de nuevos patrones. Las tres geometrías originales están en el repo previo y se copian al paquete de reproducción.','']
(R/'docs'/'01_LEDGER_AB_C01_C12.md').write_text('\n'.join(lines),encoding='utf-8')
# priors new, without overwriting old ledger.
priors='''# Priors nuevos LARP · BR12 dinámico (anexar al ledger maestro)

| ID | Proposición y procedencia | Evidencia favorable | Contraevidencia / incertidumbre | Falsador | Estado |
|---|---|---|---|---|---|
| BR12-L09 | CVT por tipo logra cobertura próxima de las cinco clases; 12 geometrías N512 y N4096. | CVT512 97.31% k16; CVT refinados 4096 ~97.6%. | CVT no es Wei; no existe réplica independiente del original LOCAL a N4096. | Original LOCAL nuevas geometrías supera CVT genuino y barato de forma replicada. | SINTÉTICO exploratorio |
| BR12-L10 | La ventaja LOCAL f1 sobre CVT puede explicarse parcialmente por iteraciones de optimización y bandwidth del estimador. | CVT inicial MSE f1 k24 .1542 > LOCAL .1404; refinado+tuning f1 CVT .0893–.0922 < LOCAL .1074. | Efectos de CVT refinamiento y tuning no se aislaron factorialmente con igualdad total de coste. | Diseño independiente y igualado de geometrías/costo invierte el ranking. | SINTÉTICO exploratorio |
| BR12-L11 | Función aprendida multiclase sobre posiciones favorece necesariamente LOCAL. | No confirmada. | MLP cinco canales: CVT .1249–.1319, LOCAL .1478 y MHU .1608; estimador analítico mejora todos. | GNN original Scale3D con múltiples patrones independientes y nuevos datos supera CVT/PointNet++ a igual coste. | NO_VALIDADO |
| BR12-L12 | La supresión espectral MHU de modos bajos es condición necesaria para predecir campos suaves. | MHU S_all finito ~4.35e-6. | CVT tiene S_all muy superior (.05–.09) y menor MSE. Metrica S calculada en 80 modos y geometrías fijas. | Tareas nuevas de largo alcance muestran ventaja replicable espectral neta. | REFUTADO EN ESTE MODELO, universal NO_VALIDADO |
| BR12-L13 | El acceso oracular de un punto por tipo es más eficiente para composición que los 16 vecinos globales. | Garantiza cinco tipos con solo 5 lecturas de sensores. | LOCAL MSE .316 vs .114 con 16 vecinos; ruido de interpolación mayor; búsqueda de 5 árboles tiene coste extra. | Otras funciones/tareas y costes totales muestran superioridad reproducible. | NO_VALIDADO |
| BR12-L14 | CVT mantiene ventaja bajo perturbaciones por sensores perdidos. | A 0% CVT ~.10 vs LOCAL .129. | A 60% MHU .474 < CVT ~.499 y LOCAL .531, todo muy degradado. | Ensayos independientes con fallos correlacionados/ruido real. | SINTÉTICO condicionado |
| BR12-L15 | La diferencia original Scale3D/N4096 puede inferirse a partir de LOCAL_derived/N512. | Ninguna. | El derivado N512 tiene peor cobertura que estratificado; no comparte optimizador/escala. | Reimplementación matemáticamente equivalente con tests de gradiente e inicialización. | RECHAZADO como equivalencia |
'''
(R/'docs'/'02_PRIORS_NUEVOS_BR12.md').write_text(priors,encoding='utf-8')
summary='''# Dictamen final LARP · BR12 dinámico

**12 ciclos sustantivos / 12 autorizados, +12 no utilizados.** Rama geométrica detenida por falta de ventaja única; no existe 2/3 o 3/3.

1. Nuevas 12 geometrías por brazo a N=512: CVT por tipo 97,31% cobertura k16; LOCAL_derived 69,17%; iid 61,43%. **LOCAL_derived no es el original**.
2. Coordenadas originales N=4096: LOCAL 96,08% cobertura k16; CVT a 8 iteraciones 94,72%–96,52%; con 15 más, tres CVT llegan a 97,56%–97,68%.
3. Primera comparación de reconstrucción fija: MSE f1,k24, bandwidth .11 LOCAL=.1404, CVT no refinado media=.1542. **Parecía** favorecer LOCAL. El siguiente ciclo impuso calibración individual del estimador y refinó CVT: dev 8 mundos → test 12 mundos. MSE LOCAL=.1074, CVT refinado=.0893–.0922. **El ranking se invirtió**. Esta calibración no fue un confirmatorio pre-registrado, sino nueva exploración con datos apartados del ajuste.
4. MLP neuronal de cinco canales, tres inicializaciones: CVT refinado .1249–.1319; LOCAL .1478; MHU .1608. No es GNN original ni Transformer, así que no generalizar.
5. Al eliminar 60% de sensores, MHU logra MSE .474 frente a CVT ~.499 y LOCAL .531; es un efecto exploratorio no una superioridad universal. En f5 las mejoras se reducen.
6. Factor espectral finito promedio sobre 80 modos: MHU S_all=4.35e-6; LOCAL=.00294, CVT .051–.090, IID=1.16. Una reducción S(k) notable no implica mejor predicción en esta tarea. Ninguna de estas mediciones prueba hiperuniformidad asintótica.

## Gobernanza
La unidad independiente de generación geométrica es la geometría, no los mundos o consultas. Una única geometría LOCAL/MHU original implica ausencia de inferencia causal/general entre algoritmos originales. *CVT per-type* es una implementación de Lloyd del presente bloque, no el algoritmo auténtico de Wei (2010). Comparar ambas bajo el mismo nombre invalidaría la auditoría.

## AB-DECIDE
**STOP a investigar «LOCAL superior» con nuevos mundos Fourier y parámetros similares**. La hipótesis de cobertura funcional no está refutada como mecanismo útil, pero es terreno conocido: Wei 2010 y CVT por tipo. **REPAIR** sólo con código del generador original repetible en N4096, implementación Wei usable a 3D/4096, o datos sensoriales externos / entrenamiento GNN completo con baseline PointNet++. No activar +12 sin esas novedades. Se conserva facultad del usuario de continuar desde nueva evidencia, no una promesa de ejecución posterior.
'''
(R/'docs'/'00_DICTAMEN_BR12.md').write_text(summary,encoding='utf-8')
# graphics
plt.rcParams.update({'font.size':10})
fig,ax=plt.subplots(figsize=(9,4.8))
methods=['IID','Estratificada','LOCAL derivado','CVT por tipo']
vals=[q512.get(f"('{n}', 'global', 'cover')")*100 for n in ('iid','stratified','local_derived','cvt_type')]
ax.bar(methods,vals);ax.set_ylim(0,105);ax.set_ylabel('Cobertura de los cinco tipos (%)');ax.set_title('N=512: 12 geometrías independientes por método, k=16')
for i,x in enumerate(vals):ax.annotate(f'{x:.1f}%',(i,x),ha='center',xytext=(0,5),textcoords='offset points')
fig.tight_layout();fig.savefig(R/'figures'/'cobertura_n512.png',dpi=155);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.8))
labels=['LOCAL original','CVT poco refinado','LOCAL calibrado','CVT refinado calibrado']
values=[pred['f1_k24']['local'],pred['f1_k24']['cvt_mean'],next(x['heldout_mse'] for x in bw if x['freq']==1 and x['name']=='local'),np.mean([x['heldout_mse'] for x in bw if x['freq']==1 and x['name'].startswith('cvt_refined')])]
ax.bar(labels,values);ax.set_ylabel('MSE, menor es mejor');ax.set_title('Cómo cambia el ranking al refinar CVT y calibrar el kernel')
ax.tick_params(axis='x',labelrotation=13)
for i,x in enumerate(values):ax.annotate(f'{x:.3f}',(i,x),ha='center',xytext=(0,5),textcoords='offset points')
fig.tight_layout();fig.savefig(R/'figures'/'comparacion_estimador.png',dpi=155);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.8))
names=list(spec['metrics'].keys());vals=[spec['metrics'][x]['all'] for x in names]
ax.bar(names,vals);ax.set_yscale('log');ax.set_ylabel('S(k) media en 80 modos, eje log');ax.set_title('MHU suprime modos finitos; CVT predice mejor en la tarea suave')
ax.tick_params(axis='x',labelrotation=15)
fig.tight_layout();fig.savefig(R/'figures'/'comparacion_spectral.png',dpi=155);plt.close(fig)
# manifest hash all artifacts except itself, zip
manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(R.rglob('*')) if p.is_file() and p.name!='MANIFEST_SHA256.json' and not p.suffix=='.zip' }
(R/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
zip_path=R.parent/'LARP_BR12_DINAMICO_AB321_20261021.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(R.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(R))
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None
print('12 cycles; ZIP',zip_path,'bytes',zip_path.stat().st_size,'files',len(manifest))
