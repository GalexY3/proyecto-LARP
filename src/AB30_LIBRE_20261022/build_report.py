from pathlib import Path
import json,hashlib,math,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';X=json.loads((ROOT/'docs'/'AB_LEDGER_C01_C30.json').read_text())
assert len(X)==30 and all(row['id']==f'C{i+1:02d}' for i,row in enumerate(X))
x=lambda i:X[i-1]['observation']
P=x(2)['mean_sq_complex'];C=x(7)['coverage16'];U=x(12)['power'];N=x(28)['nonperiodic_integral_mse_type_averaged'];Q=x(23)['union_spectral_by_shift'];E=x(24)['mse_1000_fourier_coeff_draws_per_geometry']
NAMES=['initial','local','mhu','cvt','sobol','lattice','lhs'];T={'initial':'RANDOM','local':'LOCAL','mhu':'MHU','cvt':'CVT','sobol':'Sobol','lattice':'Retícula','lhs':'LHS'}
for data,filename,title in [(P,'low_spectral.png','Banda optimizada — potencia espectral media'),(U,'out_spectral.png','Banda fuera del corte global — potencia espectral media')]:
 fig,ax=plt.subplots(figsize=(8.5,4.6))
 ax.bar([T[k] for k in NAMES],[data[k] for k in NAMES]);ax.set_yscale('log');ax.set_ylabel('Media |amplitud Fourier normalizada|² (log)');ax.set_title(title);ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(ROOT/'figures'/filename,dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.8))
for n in NAMES:
 ax.scatter(C[n]*100,P[n],s=75,label=T[n]);ax.annotate(T[n],(C[n]*100,P[n]),xytext=(5,5),textcoords='offset points',fontsize=8)
ax.set_yscale('log');ax.set_xlabel('Consultas con los cinco tipos en 16 vecinos (%)');ax.set_ylabel('Potencia espectral baja (menor mejor)');ax.set_title('Compromiso exploratorio: cobertura vs cuadratura');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(ROOT/'figures'/'frontier.png',dpi=160);plt.close(fig)
rows=[]
for c in X:
 rows.append(f"### {c['id']} · {c['question']}\n**Hipótesis:** {c['hypothesis']}. **Rival:** {c['rivals']}. **Falsador:** {c['falsifier']}. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada {c['id']} (observación completa). **Decisión:** {c['AB_DECIDE']}. **Siguiente pregunta:** {c['next_question_selected_after_observation']}.\n\n*Alcance:* {c['interpretation_limit']}\n")
ledger='# Ledger AB 3.2.1 — 30 ciclos de preguntas distintas (investigación libre)\n\n**Fecha:** 22 de octubre de 2026. **Registro en JSON:** `data/AB_LEDGER_C01_C30.json`. Exploración adaptativa y controles agrupados sobre 4 geometrías originales (n=4), sin confirmar independencia por 30 ciclos. No se comparó con GPT ni Wei original. Algunas preguntas estaban previstas en un mismo script: el branching fue parcialmente adaptativo, no 30 decisiones preregistradas separadamente antes de sus datos.\n\n'+'\n'.join(rows)
(ROOT/'docs'/'LEDGER_30_CICLOS.md').write_text(ledger)
report=f'''# LARP/MHU — Campaña libre AB 3.2.1 de 30 ciclos (22-10-2026)

## Dictamen
**30/30 preguntas y decisiones auditables ejecutadas; 0 confirmaciones independientes; 0 descubrimientos 2/3 o 3/3 acreditados.** Los ciclos C01–C30 son preguntas diferentes sobre las *mismas cuatro realizaciones originales de geometría* (5201–5204), combinadas con 7 métodos y funciones sintéticas. No son 30 estudios independientes. Fuentes originales ya versionadas y reevaluadas; este bloque no genera nuevas muestras Scale3D adicionales.

**Hallazgo 1 (conocimiento explícito recuperado):** MHU reduce el espectro de Fourier en la banda optimizada de 40 modos: potencia media **{P['mhu']:.5g}** versus LOCAL **{P['local']:.5g}**, CVT **{P['cvt']:.5g}** y RANDOM **{P['initial']:.5g}**. Pero una retícula trasladada (rango uno) consigue **{P['lattice']:.4g}** para la misma banda porque esos modos son no resonantes. Esto es teoría de cuadratura conocida, no arquitectura original. En la frecuencia resonante k=(-25,1,0), esa misma retícula presenta error de potencia **{x(15)['power']['lattice']:.4g}** —un aliasing extremo—: no existe dominador universal por estos tests.

**Hallazgo 2 (trade-off multicapa):** Con k=16 vecinos y cuatro seeds, disponibilidad de los cinco tipos: MHU **{C['mhu']*100:.2f}%**, LOCAL **{C['local']*100:.2f}%**, CVT **{C['cvt']*100:.2f}%** y retícula **{C['lattice']*100:.2f}%**. MHU combina acceso local razonable con amortiguación espectral superior a LOCAL/CVT en la banda elegida, aunque no domina simultáneamente las métricas ni supera todas las alternativas conocidas.

**Hallazgo 3 (fuera de banda verdadera):** auditoría C11 encontró que la antigua banda high era **100% interna a k²≤78**, donde ya se optimiza la unión MHU. Recalculamos fuera de la banda, modos k²={x(12)['outside_k2_range'][0]}–{x(12)['outside_k2_range'][1]}: MHU **{U['mhu']:.5g}**, LOCAL **{U['local']:.5g}**, CVT **{U['cvt']:.5g}**. Fuera del corte global, LOCAL supera a MHU: la ventaja de la penalización no se generaliza uniformemente.

**Hallazgo 4 (revisión conceptual):** si N_a/N→f_a estables y cada población tiene S_a(k)→0 al límite de baja frecuencia, entonces su unión también es HU: escribiendo A_a=(1/N_a)Σ_(i∈a)e^(ik·x_i), S_total=N|Σ f_a A_a|²≤(Σ√(f_a S_a))². Es la desigualdad triangular, NO un teorema nuevo. **La premisa 'combinar especies HU destruye la HU global y exige nuevo acoplamiento' es falsa sin hipótesis adicionales**. Lo que sí añade un acoplamiento de fases es menor S_total finito: al desplazar independiente y aleatoriamente los cinco tipos MHU, la potencia union creció de **{Q['mhu']['original_union']:.4g}** a **{Q['mhu']['independently_shifted_union']:.4g}**, unas **{Q['mhu']['independently_shifted_union']/Q['mhu']['original_union']:.1f} veces**. No se puede decir que las fases desplazadas rompan la HU de cada tipo.

**Hallazgo 5 (condiciones de utilidad):** en funciones periódicas Fourier desconocidas e independientes por especialidad, error de integración del promedio multicanal: MHU **{E['mhu']:.5g}**, LOCAL **{E['local']:.5g}**, CVT **{E['cvt']:.5g}**, retícula **{E['lattice']:.4g}** (1000 funciones aleatorias por geometría). Bajo un 50% de submuestreo en cada clase, los errores estimados de las opciones organizadas convergen: MHU **{x(27)['weighted_error_half_sample']['mhu']:.5g}**, CVT **{x(27)['weighted_error_half_sample']['cvt']:.5g}**. En funciones no periódicas, Sobol supera MHU para f(x)=x, con MSE Sobol **{N['sobol']['x']:.4g}** vs MHU **{N['mhu']['x']:.4g}**. El beneficio depende fuertemente de la clase de integrandos y presupuesto.

## Lo que no hemos demostrado
No se entrenaron nuevos modelos de lenguaje, Transformers, PointNet++ o GNN durante este bloque. No se ejecutó el código Multi-Class Blue Noise de Li-Yi Wei. No medimos hiperuniformidad asintótica ni rendimiento fuera de la muestra de datos espaciales sintéticos. Los comparadores Sobol, CVT y retícula no fueron emparejados por coste total de generación y optimización. En todo el bloque la unidad de independencia para comparar Scale3D original es **cuatro geometrías**. El script contenía una secuencia extensa de preguntas antes de evaluar los resultados; hubo reparación y pivot documentados C06, C11 y C22, pero no debe presentarse como 30 decisiones completamente replanificadas desde cero ni 30 falsaciones independientes.

## Riesgos, reparación realizada y calidad de los datos
- Se detectó y reparó un factor de 1/2 incorrecto en la derivación analítica de error con coeficientes real e imaginario gaussianos N(0,1): E[(Re(cz))²]=|z|² (no |z|²/2, que corresponde a fase uniforme). El código final y todos los resultados C26–C27 están recalculados; la primera ejecución errónea se conserva descriptivamente como errata técnica.
- La banda denominada high inicialmente era **in-band**; no se utiliza como validación OOD. La banda outside se eligió tras este descubrimiento, de manera exploratoria.
- Los modos reticulares resonantes fueron elegidos adversarialmente tras inspeccionar la regla; no medir su frecuencia por un único ejemplo ni comparar únicamente ese modo contra rivales.
- Las afirmaciones métricas se condicionan al modelo de entrada y al conjunto finito de funciones; no atribuimos ventajas a ontología neuronal o generalidad de inteligencia.

## Próxima investigación que podría justificar presupuesto adicional
**Solicitar 8 ciclos focalizados, no 30 automáticos**, condicionados a conseguir una implementación ejecutable del algoritmo original de Wei y a poder entrenar baselines neuronales con datos fuera del generador Fourier. Una línea plausible es aprovechar *interacciones entre funciones compartidas por diferentes tipos* para probar si el acoplamiento de fases que reduce S_union (sin alterar S_a) afecta a la transmisión de señales compartidas. Falsadores principales: control de cinco poblaciones independientemente desplazadas (mismas S_a), reglas QMC/Wei competentes y coste igualado. Sólo si ese mecanismo sobrevive, probarlo en modelo Scale3D entrenado con varias semillas y datos sensoriales externos.

## Referencias y prioridad
- Li-Yi Wei, *Multi-Class Blue Noise Sampling* (SIGGRAPH 2010): https://www.liyiwei.org/papers/noise-sig10/
- Morokoff & Caflisch, *Quasi-Random Sequences and Their Discrepancies* (SIAM, 1994): https://doi.org/10.1137/0915077
- Pilleboue et al., *Variance Analysis for Monte Carlo Integration* (2015): https://perso.liris.cnrs.fr/david.coeurjolly/publication/pilleboue-15-variance/
- Klatt, Lovrić et al., *Universal hidden order in amorphous cellular geometries* (2019): https://www.nature.com/articles/s41467-019-08360-5
- Investigación anterior y código original: https://github.com/GalexY3/proyecto-LARP (privado)
'''
(ROOT/'docs'/'INFORME_Y_SOLICITUD.md').write_text(report)
priors='''# Ledger acumulativo de priors de LARP — apéndice BR30 libre (no borrar entradas anteriores)

| ID | Hallazgo/Hipótesis | A favor | En contra o límite | Estado |
|---|---|---|---|---|
| BR30-F01 | MHU penaliza eficazmente fluctuación espectral finita de conjunto y cinco tipos | C02-C03, C21, fuente original | Estaba definido como objetivo; no novedad asintótica | VERIFICADO FINITO |
| BR30-F02 | MHU ofrece cuadratura superior a alternativas competentes | C24 frente LOCAL/CVT/Sobol | Retícula exacta en banda baja; Sobol mejor en varias funciones no periódicas | REFUTADA UNIVERSALIDAD |
| BR30-F03 | Una retícula sin aliasing domina MHU | C06 integrales no resonantes exactas | C15 encuentra resonancia con S=1 | REFUTADA UNIVERSALIDAD |
| BR30-F04 | Supresión MHU persiste fuera de banda | C09/C10 parecían favorables | C11 revela fuga, C12 encuentra LOCAL mejor fuera del corte | REPARADA: NO VALIDADO |
| BR30-F05 | Cada especie HU podría producir unión no HU bajo fracciones estables | Premisa histórica | C22 demuestra desigualdad triangular: imposible bajo sus hipótesis | RECHAZADA COMO PRINCIPIO |
| BR30-F06 | Coordinación de fases entre especies añade supresión finita de unión | C23: shifts independientes elevan S_total ~21x conservando S_i | Objetivo explícito del optimizador, no nueva teoría ni ventaja neural | OBSERVACIÓN SINTÉTICA |
| BR30-F07 | Multiespectral y disponibilidad local generan intercambio útil | C07-C08 y C29 frontera observada | CVT/QMC/lattice otras ventajas, se ignoran costes de construcción | HIPÓTESIS ABIERTA |
| BR30-F08 | Métrica de S(k) baja predice mejora en GPT | Ninguna | Experimentos Scale3D previos no concluyentes, ningún test de GPT aquí | NO VALIDADO |
| BR30-F09 | Reducción de sensores preserva gran ventaja MHU | C27 ligera ventaja a mitad densidad | Pérdida de casi toda supresión: MSE entre organizados converge | DEBILITADA |
| BR30-F10 | Beneficio de fases cruzadas podría mediar tareas de señal compartida | C23 y álgebra de amplitudes | No se ha entrenado ni ensayado tarea shared-channel | PRIORIZAR SI HAY 8 CICLOS MÁS |

**Procedencia:** `docs/AB_LEDGER_C01_C30.json`, fuente `src/ab30_live.py`. Estados exploratorios no son *Bayes factors* ni posteriores calibrados. Históricos BR12/BR30 anteriores permanecen en ledger maestro.
'''
(ROOT/'docs'/'PRIORS_APENDICE.md').write_text(priors)
files=[]
for p in ROOT.rglob('*'):
 if p.is_file() and p.name!='MANIFEST_SHA256.json': files.append((str(p.relative_to(ROOT)),hashlib.sha256(p.read_bytes()).hexdigest()))
(ROOT/'MANIFEST_SHA256.json').write_text(json.dumps(dict(files),indent=2))
print('report chars',len(report),'ledger chars',len(ledger),'files',len(files));print('C22 shift ratio',Q['mhu']['independently_shifted_union']/Q['mhu']['original_union'])
