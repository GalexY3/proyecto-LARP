#!/usr/bin/env python3
"""Build truthful AB3.2.1 ledger and dossier from BR30 pilot + one-claim confirmation."""
from pathlib import Path
import pandas as pd, numpy as np,json,hashlib,zipfile,math
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
BASE=Path(__file__).resolve().parents[1];out=BASE/'docs';out.mkdir(exist_ok=True)
pdopt=lambda x: str(round(float(x),6))
d=pd.read_csv(BASE/'data/pilot_summary.csv');cf=json.loads((BASE/'data/confirm_focus_summary.json').read_text())
TITLE={
 'A':'Probabilidad de disponer de los cinco tipos entre los vecinos más próximos',
 'B':'Radio necesario para alcanzar los cinco tipos funcionales',
 'C':'Error de reconstrucción composicional frente a frecuencia espacial',
 'D':'Resistencia de la reconstrucción ante pérdida aleatoria de sensores',
 'E':'Sensibilidad al ancho de banda del estimador espacial',
 'F':'Ablación causal de posiciones, etiquetas y correspondencia señal–posición'
}
COND={
'A':[f'k={k}' for k in [8,12,16,24,32]],
'B':[f'q={q:.2f}' for q in [.5,.75,.9,.95,.99]],
'C':[f'freq={x}' for x in [1,2,3,4,6]],
'D':[f'drop={x}' for x in [0,.1,.25,.4,.6]],
'E':[f'bw_k24={x}' for x in [.3,.6,1,2,4]],
'F':['labels_shuffled','positions_shuffled_per_type','only_dominant','signals_scrambled_per_type','positions_labels_permuted']
}
RIVALS={
'A':'Efecto trivial del número de vecinos y las cuotas; estratificación de rejilla; cobertura no equivale a hiperuniformidad.',
'B':'Una configuración estratificada competente podría conseguir los mismos radios; sólo se audita una geometría fija por algoritmo.',
'C':'La superioridad puede ser explicada por continuidad impuesta de campos Fourier y por información de posición/tipo conocida por el interpolador.',
'D':'El decaimiento puede obedecer únicamente a menor densidad, no a un mecanismo robusto de reparación neuronal.',
'E':'La variación se explica por sesgo-varianza del kernel gaussiano; la anchura no está optimizada por validación independiente.',
'F':'La pérdida de ventaja puede depender del deterioro trivial de la información; los controles algebraicamente nulos deben permanecer invariantes.'
}
FALSIFY={
'A':'LOCAL no eleva cobertura respecto al control estratificado ni a RANDOM para este k, o el orden se invierte.',
'B':'LOCAL no reduce el radio de cuantiles respecto a RANDOM/control estratificado.',
'C':'LOCAL no supera un estratificado por tipo con el mismo interpolador; la diferencia desaparece con frecuencias mayores.',
'D':'La ventaja de LOCAL se anula o invierte bajo la tasa de dropout fijada.',
'E':'La ventaja relativa de LOCAL depende críticamente de elegir retrospectivamente el bandwidth.',
'F':'Ablación no cambia nada cuando debería, o cambia mucho un control que debería ser invariante; posible bug o inferencia espuria.'
}
lines=['# LARP · AB 3.2.1 · BRANCHING 30 — Ledger auditable','',
'**2026-10-21**. Bloque autorizado expresamente por el investigador para LARP (no reutiliza autorizaciones de AB general).',
'**Alcance:** 30 decisiones *condición-específicas* agrupadas en seis familias, **no** 30 descubrimientos independientes. Todas A–F son exploratorias excepto la única reivindicación C11 confirmada en mundos nuevos tras prerregistro de selección. Una única geometría por construcción: no replicación biológica externa.',
'**Nota de integridad:** toda condición exploratoria comparte simulador, geometrías, mundos, etiquetas y algunos controles. No interpretar los 880 registros del piloto como 880 experimentos independientes.','',
'## Contrato compartido A–J',
'A. Unidad: geometría 3D toroidal fija de 4096 nodos y/o mundo Fourier generado. Estimando geométrico: cobertura/radio para un punto uniformemente consultado; estimando predictivo: media MSE por mundo. Acceso a tipos y posiciones es idéntico entre brazos. B. Hipótesis rivales: LOCAL favorecida, nula de igualdad, MHU/STRATIFIED/RANDOM competentes y H_otras no modelada. C. Métricas, semillas y presupuesto en prerregistro. D. Invariantes de cuotas/permutación y no fuga en inferencia. E. Control apareado. F. Auditoría adversarial y mecanismos impuestos. G. Piloto seeds 11–20; selección única C11 confirmada con seeds 901–920. H. Actualización cualitativa de priors, sin probabilidades numéricas inventadas. I. Dictamen multidimensional. J. AB-DECIDE.','']
alldec=[]
for i in range(1,31):
    b='ABCDEF'[(i-1)//5];param=COND[b][(i-1)%5]
    cur=d[(d.cycle==i)&(d.endpoint.isin(['full_coverage','radius_5_types','MSE']))]
    vals={g:float(cur[cur.geometry==g]['mean'].iloc[0]) for g in ('local','mhu','random','stratified')}
    if b in 'BCDEF':
        effect=vals['local']-vals['stratified']
        margin=f'MSE' if b!='B' else 'radio'
        if b=='B':favor=effect<0
        elif b=='F' and param in ('positions_shuffled_per_type','positions_labels_permuted'):favor=abs(effect)<1 # not claim
        else:favor=effect<0
    else:
        effect=vals['local']-vals['stratified'];margin='cobertura';favor=effect>0
    if b=='F' and param in ('positions_shuffled_per_type','positions_labels_permuted'):
        dec='REPAIR (control de identidad, no intervención sustantiva)'
    elif b=='C' and i==11:
        dec='CONTINUE → prueba confirmatoria única preregistrada (realizada después de seleccionar C11)'
    elif b=='C' and i>=14:
        dec='STOP para altas frecuencias: ventaja decrece y error absoluto aumenta'
    elif b=='D' and i==20:
        dec='STOP por degradación notable a dropout=.60'
    elif b=='F':
        dec='STOP en esta ablación: mecanismo conocido, no original'
    elif favor:dec='CONTINUE sólo con control externo/no simulado'
    else:dec='STOP: no ventaja robusta sobre control espacial competente'
    alldec.append({'cycle':i,'branch':b,'condition':param,'decision':dec,'local':vals['local'],'stratified':vals['stratified'],'delta_local_minus_stratified':effect})
    lines += [f'## Ciclo LARP-BR30-{i:02d} — {TITLE[b]} · {param}',
    f'**Pregunta y estimando (A).** {TITLE[b]}. Condición congelada `{param}`; estimando medido: `{margin}` en una consulta/mundo de la población sintética especificada.',
    f'**Rivales (B).** H_L: geometría LOCAL beneficia la medida bajo el presupuesto; H0: no mejora sobre control competente; H_M: MHU puede superar LOCAL; H_ALT: {RIVALS[b]} H_otras: otras leyes de diseño espacial no evaluadas.',
    '**Prerregistro (C).** Véase `prereg/BR30_20261021.md` (commit previo a ejecutar). Presupuesto de inferencia fijo por ejemplo; consulta y mundos pareados; no se elige esta condición por su resultado.',
    '**Instrumentación (D).** Cuotas fijas [1669,871,696,512,348]; puntos en [0,1)^3; distancia toroidal `cKDTree(boxsize=1)`; test de permutación de filas exacto; señales generadas por Fourier con etiquetas ocultas sólo cuando la ablación las cambia.',
    '**Ejecución (E).** Una geometría fija para cada brazo y condiciones apareadas en simulador; medias exploratorias por mundo o valor finito por población geométrica:',
    '| LOCAL | MHU | STRATIFIED | RANDOM | LOCAL−STRATIFIED |', '|---:|---:|---:|---:|---:|',
    '| '+ ' | '.join(pdopt(vals[g]) for g in ('local','mhu','stratified','random'))+' | '+pdopt(effect)+' |',
    f'**Auditor adversarial (F).** {RIVALS[b]} **Falsador:** {FALSIFY[b]}',
    '**Confirmación (G).** '+ ('Mundos 901–920 confirmaron la comparación LOCAL−STRATIFIED en C11; NO nuevos patrones físicos/geométricos; ver documento principal.' if i==11 else 'NO confirmación independiente de esta condición; sólo diagnóstico exploratorio.'),
    f'**Actualización AB (H).** La diferencia observada respecto a control espacial competente es {effect:+.6f}, valor condicionado al DGP. No se asigna posterior numérico por falta de verosimilitud representativa de aplicaciones reales.',
    '**Dictamen (I).** Validez interna: parcial al DGP/algoritmo; identificación causal: solo intervención sintética de geometría/etiquetas bajo reglas impuestas; replicación externa: ausente; transferibilidad a modelos de lenguaje: NO estudiada; originalidad: NO acreditada. Un conjunto finito no demuestra hiperuniformidad asintótica.',
    f'**AB-DECIDE (J).** **{dec}**','']

lines += ['## Auditoría transversal del branching',
'- Resultados C:E con mundos sintéticos independientes de distinto coeficiente, pero **geometría compartida fija**. No bootstrap sobre queries como si fueran geometrías.',
'- Las muestras de A/B son Monte Carlo sobre la misma geometría, por tanto IC entre queries solo mediría error de integración espacial, no efecto generalizable sobre generadores.',
'- F28 elimina cuatro tipos y pierde casi todo rendimiento por construcción: no atribuir causalidad emergente.',
'- F27 y F30 son **controles de identidad algebraica**, no ablaciones de disposición espacial. Comprobar que no cambian la predicción; su existencia evita pseudohallazgos.',
'- El diseño no enfrenta LARP neuronal, MoE o Transformer, sino **geometrías + interpolador clásico**. NO afirmar superioridad arquitectónica.',
'- Las 30 decisiones comparten seis preguntas-familia: nadie debe presentarlas como treinta ensayos científicos independientes.',
'']
(out/'01_LEDGER_30_CICLOS.md').write_text('\n'.join(lines))

priors='''# Ledger acumulativo de priors LARP — actualización BR30 (21-10-2026)

Se conserva la procedencia histórica documentada; **no se inventa un ledger histórico exhaustivo que aquí no se ha importado**. IDs locales nuevos BR30-L01 etc, sujetos a reconciliación con el ledger principal cuando esté disponible. Un prior no es un hecho universal.

| ID | Proposición | Procedencia | Alcance y clase | Evidencia favorable | Evidencia contraria / incertidumbre | Falsador | Decisión |
|---|---|---|---|---|---|---|---|
| BR30-L01 | La cobertura multiclase local reduce distancias al quinto tipo frente a puntos iid bajo cuotas fijas | Geometrías originales + nuevos A/B | SINTÉTICO geométrico; una geometría por algoritmo | Cobertura k16 LOCAL 96.20%, RANDOM 62.32%, estratificado 80.88% | Depende de constructor y distribución fija; los antecedentes multi-class blue noise ya persiguen esto | Control multi-class blue noise optimizado iguala o supera con mismo coste | CONTINUE condicionado |
| BR30-L02 | LOCAL mejora reconstrucción composicional de campos suaves frente a muestreo estratificado simple | Piloto C11 y confirmación nueva en mundos sintéticos | SINTÉTICO, condicionado a DGP Fourier y kernel gaussiano | Delta confirmación −0.0750 IC95 [−0.0912,−0.0589] por mundo | Una geometría fija y una familia Fourier; control estratificado simple no es SOTA | Replicación con nuevas geometrías y baselines multiclase blue noise elimina ventaja | CONTINUE limitado |
| BR30-L03 | La ventaja espacial se reduce conforme crece la frecuencia del campo | Piloto C11–C15 | SINTÉTICO exploratorio | LOCAL 0.134 vs 2.106 al pasar f1→f6; delta frente estratificado cae | En f6 MSE elevado para todos; escalas y amplitudes fijas | Una nueva familia de señales altas frecuencias preserva ventaja | PIVOT a suavidad/cobertura |
| BR30-L04 | El beneficio espacial depende de correspondencia correcta entre etiquetas y sensores | F26, F28, F29 | SINTÉTICO exploratorio | Permutar etiquetas/descorrelacionar señales degrada casi a nulo | Consecuencia parcialmente incorporada al DGP que define cinco campos | Alternativas sin tipos conservan misma ventaja | CONTINUE con ablaciones fuertes |
| BR30-L05 | MHU supera a LOCAL por la penalización espectral en este benchmark | Piloto C11–C15 y confirmación C11 | NO_VALIDADO; contraste H3 | MHU f2 ligeramente menos MSE (0.807 vs .812) | LOCAL mejor f1 (0.134 vs 0.140), confirmación .1258 vs .1323; sin control estadístico de H3 | Series independientes grandes, tareas long-range y medidor asintótico | STOP afirmación fuerte |
| BR30-L06 | La geometría LOCAL por sí sola supera modelos de lenguaje y Transformers | Contexto previo LARP vs GPT | NO_VALIDADO | Ventaja en tareas espaciales bajo prototipo inicial | GPT pequeño gana bytes-per-byte, interpolación clásica supera redes en tarea espacial; ninguna comparación actual con GPT | Comparación GPU con paridad FLOPs y benchmarks externos | STOP reivindicación |
| BR30-L07 | Hay novedad científica al promover cobertura heterotípica local | Estado del arte revisado en BR30 | NO_VALIDADO | Interesante hipótesis funcional | Multi-Class Blue Noise Sampling (Wei, SIGGRAPH 2010) y heterocoordinación retinal (Lomba et al., 2020) anticipan idea | Mecanismo que supera métodos competentes con predicciones nuevas y replicación externa | NO 2/3 |
| BR30-L08 | Una red de especialistas semánticos (lenguaje/código/matemáticas) mejora gracias a geometría LOCAL | Propuesta del usuario; todavía no probada aquí | HIPÓTESIS NO_VALIDADA | Cobertura geométrica de cinco tipos y éxito espacial como motivación | No equivalen sensores Fourier a expertos semánticos; MoE ya existe | Factorial geometría × especialización sobre corpus externo; mejores baselines | REPAIR antes de afirmar |
'''
(out/'02_PRIORS_LARP.md').write_text(priors)

brief=f'''# Dictamen científico del branching 30 — LARP / AB 3.2.1

**Fecha:** 21-10-2026. **Autorización:** 30 ciclos con branching; ejecutados 30 contrastes condición-específicos bajo seis ramas, con registro A–J (no 30 estudios independientes). **Conclusión:** evidencia *intra-modelo* de una ventaja para cobertura funcional de campos suaves, no descubrimiento 2/3.

## Hallazgo confirmado de forma limitada
Una única afirmación elegida tras piloto y preregistrada *antes* de los nuevos mundos sintéticos: MSE de interpolación multicanal en f=1, LOCAL frente STRATIFIED, mismos 24 vecinos, mismo kernel y mismas consultas y coeficientes por mundo, 20 mundos × 512 queries. Resultados: {cf['means']}; diferencia (LOCAL−STRATIFIED) **{cf['diff_mean']:.6f}**; IC95 pareado por mundo **[{cf['ci_95_two_sided_t'][0]:.6f}, {cf['ci_95_two_sided_t'][1]:.6f}]**, t19={cf['t_statistic']:.3f}, p bilateral={cf['p_two_sided']:.3g}. 20 mundos independientes de señales **sobre las mismas geometrías fijas**, no 20 replicaciones de un generador espacial.

## Qué sí explica la ventaja
LOCAL y MHU, optimizados para separación dentro de cada uno de los cinco grupos, elevan disponibilidad cercana de canales complementarios. En nuestro control de 8.192 consultas uniformes sobre los originales, k=16: LOCAL 96.20%, MHU 94.91%, STRATIFIED 80.88%, RANDOM 62.32%. Esto es un beneficio de **muestreo funcional/espacial** bajo cargas conocidas, no una propiedad neuronal universal.

## Qué la limita
* C11 f1: LOCAL MSE≈0.134 vs STRATIFIED≈0.208; C15 f6: LOCAL≈2.106 vs STRATIFIED≈2.149. La ventaja pierde relevancia al subir la frecuencia (todos empeoran).
* Permutar etiquetas degrada; eliminar cuatro tipos hace la tarea irresoluble por el interpolador: resultado parcialmente impuesto por mecanismo del simulador.
* MHU y LOCAL empatan aproximadamente en esta tarea. Penalización espectral no aporta una mejora inequívoca.
* Bandwidth 0.3×distancia k24 da mucho menos error que el bandwidth base (pilot LOCAL f2 MSE .608 vs .813), lo que indica sensibilidad al estimador; optimización de bandwidth sólo exploratoria (no retune del confirmatorio).
* El algoritmo predictor es **un interpolador gaussiano clásico por tipo**, NO un nuevo entrenamiento de LARP neuronal. No resolver código/matemáticas/lenguaje.
* F27/F30 son invariantes algebraicas de renombrado/reordenación y no intervenciones geométricas; confundirlas con ablación invalida argumento.
* Comparator STRATIFIED está basado en una rejilla perturbada por tipo, **no** es el mejor algoritmo de multi-class blue noise; no es correcto afirmar SOTA.

## Auditoría de originalidad
Antecedentes verificables: Wei (2010), *Multi-Class Blue Noise Sampling*, https://www.liyiwei.org/papers/noise-sig10/; Jiao et al. (2014), https://doi.org/10.1103/PhysRevE.89.022721; Lomba et al. (2020), https://doi.org/10.1103/PhysRevE.102.012134. Tienen mecanismos de muestreo espacial multiclase, heterocoordinación y supresión de fluctuaciones. LOCAL no constituye por sí sola una clase matemática novedosa. Una extensión a equipos de expertos semánticos sigue sin probar.

## Procedencia y auditabilidad
Prerregistro github: c6a6e3fcedb717e3e2faee5f8f5fd38d7be463f4. Bloqueo SHA del script antes de ejecutar: eea8e364efe6d8c9b5d49d2d83493d3c2292d01e. Selección confirmatoria: 76b332002d0a6c047976359ccf124b7dd3eafeac. Fuente local congelada SHA256 6ba3d7347c087bdf71c7de800312866c4f10dbf0f9da5ba26b499a33957284c5. El intento inicial de ejecutar `--phase confirm` con 30 condiciones agotó el tiempo y no generó CSV completo; se ejecutó **exclusivamente** la afirmación congelada con `src/confirm_focus.py`. No presentar experimentos no ejecutados como ejecutados.

## AB-DECIDE
**PIVOT condicional hacia muestreo de sensores multiclase y especialización funcional**, sólo si se accede a nuevos generadores de geometrías, simulaciones físicas o expertos ML con comparadores competentes Multi-Class Blue Noise / PointNet++ / Set Transformer. **STOP** en repetir el mismo Fourier sintético: no aumenta evidencia de novedad. **Ninguna contribución de nivel 2/3 ni 3/3 acreditada.**
'''
(out/'00_DICTAMEN.md').write_text(brief)

README='''# LARP — branching AB 3.2.1, 30 condiciones de contraste (2026-10-21)

## Lectura
- `docs/00_DICTAMEN.md`: principal; `docs/01_LEDGER_30_CICLOS.md`: auditoría A–J por condición; `docs/02_PRIORS_LARP.md`: priors nuevos y estado.
- `data/pilot_raw.csv` (880 filas); `data/pilot_summary.csv`; `data/confirm_focus_raw.csv` (80 filas); `data/confirm_focus_summary.json`.
- `src/run_br30.py` código del piloto (source lock en GitHub antes de experimentos); `src/confirm_focus.py` script confirmatorio; `data/geometrias/*.npz` entradas originales.

## Reproducción (Python 3.10+, numpy, scipy, pandas, matplotlib)
`OPENBLAS_NUM_THREADS=1 python src/run_br30.py --phase pilot --out data`
`OPENBLAS_NUM_THREADS=1 python src/confirm_focus.py`
`python src/build_report.py`

## Límites
Se usa un solo patrón geométrico original por algoritmo y nuevos mundos sintéticos Fourier. NO réplica biológica, NO inferencia sobre lenguaje, NO LLM, NO nueva arquitectura neuronal probada en este estudio. Tras la selección confirmatoria no se han abierto múltiples afirmaciones confirmatorias. Tres controles clásicos/espaciales (RANDOM, STRATIFIED, kernel por tipo) incluidos, pero falta Multi-Class Blue Noise optimizado, PNT++ y Set Transformer.

AB: https://github.com/GalexY3/Metodologia-AB
LARP privado: https://github.com/GalexY3/proyecto-LARP
'''
(BASE/'README.md').write_text(README)

# figures separate matplotlib (not invented data)
fig=BASE/'figures';fig.mkdir(exist_ok=True)
allg=['random','stratified','local','mhu'];labels=['RANDOM','STRATIFIED','LOCAL','MHU']
for cyc,key,ylbl,name in [(3,'full_coverage','Fracción de consultas con cinco tipos','cobertura_k16'),(11,'MSE','MSE (menor = mejor)','mse_frecuencia_1')]:
    st=d[(d.cycle==cyc)&(d.endpoint==key)]
    yy=[float(st[st.geometry==g]['mean'].iloc[0]) for g in allg]
    figg,ax=plt.subplots(figsize=(9,4.2));rect=ax.bar(labels,yy,color=['#858c9b','#b6a595','#16a1a0','#7f67c1'])
    ax.set_title('LARP BR30: '+name.replace('_',' '));ax.set_ylabel(ylbl);ax.grid(axis='y',alpha=.17)
    for a,v in zip(rect,yy):ax.text(a.get_x()+a.get_width()/2,a.get_height(),f'{v:.3f}',ha='center',va='bottom',fontsize=9)
    figg.tight_layout();figg.savefig(fig/(name+'.png'),dpi=165);plt.close(figg)
# Key per cycle machine-readable decisions
(BASE/'data/cycle_decisions.json').write_text(json.dumps(alldec,indent=2,ensure_ascii=False))
manifest={}
for f in sorted(BASE.rglob('*')):
    if f.is_file() and f.name!='MANIFEST_SHA256.json' and '.pyc' not in f.suffix:
        manifest[str(f.relative_to(BASE))]=hashlib.sha256(f.read_bytes()).hexdigest()
(BASE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2))
zip_path=BASE.parent/'LARP_BR30_AB_321_20261021.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for f in sorted(BASE.rglob('*')):
        if f.is_file() and '__pycache__' not in str(f):z.write(f,arcname='LARP_BR30_20261021/'+str(f.relative_to(BASE)))
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None
print(json.dumps({'cycles':len(alldec),'zip':str(zip_path),'bytes':zip_path.stat().st_size,'files':len(manifest),'ledger_words':len((out/'01_LEDGER_30_CICLOS.md').read_text().split())},indent=2))
