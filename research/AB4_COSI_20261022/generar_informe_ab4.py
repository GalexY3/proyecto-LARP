import json,hashlib,zipfile
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
base=Path(__file__).resolve().parent
out=base/'ab4_data'
bands=json.loads((out/'bands.json').read_text())
rob=json.loads((out/'robustness.json').read_text())

def mean(name,key,data):
 return float(np.mean([z[key] for z in data if z['method']==name]))

# graph 1: actual numbers for simulated 3D performance (not neural)
names=['MHU-proxy','HYBRID-proxy','FPS','SOBOL','LOCAL-proxy']
X=['entrenada_k1','no_entrenada_k2_3','no_entrenada_k5_7']
Y=np.array([[mean(name,k,bands) for k in X] for name in names])
fig,ax=plt.subplots(figsize=(9,5.4))
for i,name in enumerate(names):
 ax.plot(np.arange(3),Y[i],marker='o',label=name)
ax.set_xticks(np.arange(3),['Band k1\noptimizada','Band k2–3\nno optimizada','Band k5–7\nno optimizada'])
ax.set_ylabel('Potencia residual media por tipo (menor es mejor)')
ax.set_title('Bandas de frecuencia — 12 configuraciones sintéticas 3D')
ax.grid(alpha=.25);ax.legend(frameon=False,ncol=2,fontsize=9)
fig.tight_layout();fig.savefig(base/'AB4_bandas.png',dpi=180);plt.close(fig)

# graph 2: compare actual out-of-sample risk and covariate shift
methods=['MHU-wide-proxy','COSI-pilot-proxy','COSI-shrink50-proxy','FPS','LOCAL-proxy']
keys=['test_risk','shift_risk','drop_risk']
fig,ax=plt.subplots(figsize=(9,5.5))
for name in methods:
 values=[np.mean([np.sqrt(z[k]) for z in rob if z['method']==name]) for k in keys]
 ax.plot(range(3),values,marker='o',label=name)
ax.set_xticks(range(3),['Covarianza conocida\nprueba independiente','Cambio de covarianza\nfuera de entrenamiento','Fallo espacial\nagrupado'])
ax.set_ylabel('RMSE esperado para campos Fourier sintéticos')
ax.set_title('Compromiso adaptación–robustez — 8 semillas nuevas (801–808)')
ax.grid(alpha=.25);ax.legend(frameon=False,ncol=2,fontsize=9)
fig.tight_layout();fig.savefig(base/'AB4_robustez.png',dpi=180);plt.close(fig)

sel={name:{k:np.mean([np.sqrt(z[k]) for z in rob if z['method']==name]) for k in keys} for name in methods}
lines=[]
for n,v in sel.items():lines.append(f'| {n} | {v["test_risk"]:.5f} | {v["shift_risk"]:.5f} | {v["drop_risk"]:.5f} |')
report=f'''# LARP — AB 3.2.1: cuatro ciclos de exploración sobre MHU, LOCAL-SI y una arquitectura alternativa

**Fecha:** 22 de octubre de 2026  
**Naturaleza:** cuatro ciclos exploratorios suplementarios; no sustituyen los criterios de entrada para un experimento confirmatorio 2/3 ni validan el Scale3D original.  
**Estado:** sin datos 3D reales accesibles en la sesión; sin ejecución nativa del benchmark Wei; sin nuevas redes neuronales entrenadas. **Originalidad verificada: 1/3 (no se ha demostrado mejora 2/3/3/3).**

## Contexto recuperado
El informe previo `AB06_docs_02_DICTAMEN_AB06.md` de Google Drive (22-10-2026) registró rendimiento de MHU 94,94%, LOCAL 95,06%, CVT 95,17%, Sobol 96,11%, MLP píxeles 96,78% sobre los dígitos de UCI/sklearn (1797 imágenes 8×8), cuatro semillas geométricas; MHU supera LOCAL en ciertos casos, pero no hay una ventaja neuronal robusta. En robutez para intensidad única, LOCAL superó MHU en ruido y rotación; efectos de representación/preprocesamiento no están aislados.

## C01 — Auditoría de originalidad y de condiciones de validez
**Hipótesis:** una distribución multiclase equilibrada podría ser novedosa. **Refutador:** Wei (SIGGRAPH 2010) ya construye multi-class blue noise donde clases y sus uniones presentan regularidad; extensión a dimensiones arbitrarias, muestreo adaptativo y diseños de sensores. Los diseños de sensores por información mutua y cuadratura con kernels son precedentes adicionales. **Decisión:** no reclamar novedad de multiclase, de cobertura, de optimización por covarianza, ni de robustez por sí solas.

**Fuente primaria Wei:** https://www.liyiwei.org/papers/noise-sig10/  
**Guestrin et al. (2005):** https://mlanthology.org/icml/2005/guestrin2005icml-near/  
**Huszár & Duvenaud (2012):** https://proceedings.mlr.press/r10/huszar12a.html  
**Khanna et al. (2021):** https://proceedings.mlr.press/v161/khanna21a.html  
**Zeng et al. (2026):** https://www.mdpi.com/2075-5309/16/5/1024  
**Adaptación en reconstrucción de campos acústicos (2026):** https://pubmed.ncbi.nlm.nih.gov/41563273/

**Restricciones instrumentales:** `skimage.data.cells3d` contiene volumen fluorescente 3D de membranas/núcleos de células y fue localizado documentalmente, pero falló su descarga por red. No se reemplazó con imágenes 2D proyectadas, y el algoritmo original de Wei tampoco fue compilado. La demostración se mantiene sintética. No confundir 3D sintético con datos 3D observados.

## C02 — Concentración espectral frente a cobertura y transferencia
**Estimando:** potencia espectral media por tipo sobre bandas de ondas periódicas 3D, menor es mejor. Universo: cubo periódico [0,1)^3 con 160 nodos (cinco roles, 32 por tipo); seeds 701–712, 12 realizaciones independientes. Generadores: uniforme IID, Sobol multiclase, FPS multiclase, repulsión local (`LOCAL-proxy`), penalización Fourier + repulsión (`MHU-proxy`) e híbrido Fourier + CVT (`HYBRID-proxy`). Todos con mismo número de nodos y roles; **no equiparados por tiempo de generación**. Las proxies son implementaciones experimentales autónomas, no el auténtico Scale3D.

| Método | Banda entrenada k1 | Banda no entrenada k2–3 | Banda no entrenada k5–7 |
|---|---:|---:|---:|
'''
for n in ['IID','SOBOL','FPS','LOCAL-proxy','MHU-proxy','HYBRID-proxy']:
 vals=[mean(n,k,bands) for k in X]
 report+=f'| {n} | '+ ' | '.join(f'{v:.5f}' for v in vals)+' |\n'
report+='''
**Observación:** MHU-proxy casi anula las frecuencias explícitamente objetivo, pero en k2–3 FPS es mejor: MHU 0,02311, híbrido 0,01454, FPS 0,01206. El híbrido mejora la generalización de MHU respecto a esa banda, pero NO supera FPS. La potencia aquí no certifica hiperuniformidad asintótica ni calidad de aprendizaje neuronal.

## C03 — Pivote hacia un objetivo espectral dependiente de la tarea (COSI)
**Mecanismo:** en vez de minimizar el espectro de cada población indiscriminadamente, optimizamos una forma cuadrática definida por matrices de covarianza positiva semidefinida `C(k)`, estimadas con 60 muestras piloto sintéticas independientes por frecuencia y semilla:

L_C = (1/(2|K|)) sum_k (W A(k))* C_hat(k) (W A(k)); W_a=1/5.

En la distribución de señales utilizada, cinco roles registran observaciones de campos Fourier tridimensionales parcialmente correlacionados. Optimizar por covarianza es legítimo como **adaptación a la tarea**, pero ofrece información adicional respecto a un generador geométrico no informado, por lo que NO acredita una ganancia exclusivamente geométrica.

**Corrección técnica:** la primera implementación del gradiente de `COSI` tenía signo invertido. Detectado por diferencias finitas (errores relativos ~2), corregido antes de conservar las corridas. Tras corregir, discrepancia relativa numérico/analítico ~1e−9–2e−8. Para un campo Fourier sintético independiente, RMSE analítico 0,03859 y RMSE Monte Carlo de 1500 campos nuevos 0,03911 (diferencia ≈1,35%).

En semillas 701–708, MHU-wide-proxy obtuvo 0,01841 de RMSE y COSI piloto 0,01382 en la distribución fuente (~25% menos). Frente a un cambio de covarianza, empeoró: 0,02545 de MHU-wide vs 0,03191 de COSI. No es superioridad general.

**Identidad teórica adversarial:** el objetivo COSI es una discrepancia de kernel matricial en un conjunto finito de frecuencias, con `K_ab(x,y)=sum_k C_ab(k) exp(2πik·(x-y))`. Como cada C(k) es PSD, la conexión con cuadratura y embeddings de media de kernels es directa. Tal equivalencia niega la novedad del principio abstracto. COSI es un nombre interno del prototipo, no familia nueva acreditada.

## C04 — Regularización para resistir desplazamientos de covarianza y fallos espaciales
**Hipótesis de mejora:** reducir especialización mezclando la covarianza piloto y una penalización espectral isotrópica general. `C_shrink(k)=0,5*C_pilot(k)+0,5*traza_media(C_pilot)/(5)*I` (mezcla fija, no elegida después de ver semillas 801–808).

**Unidad:** ocho nuevas realizaciones 801–808; se compararon MHU-wide, COSI piloto, COSI-shrink50, FPS, Sobol, LOCAL e IID. Los fallos espaciales retiran sensores dentro de bolas de radio 0,18 en el toro 3D; 18 centros aleatorios de falla por realización, compartidos entre métodos. La etiqueta *cambio de covarianza* usa una permutación de bandas y relaciones entre roles simulada y no observada. Todos los métodos se evalúan con mismo número de sensores iniciales, funciones y datos de test.

| Método | RMSE distribución fuente | RMSE covarianza desplazada | RMSE fallos espaciales |
|---|---:|---:|---:|
'''
report+='\n'.join(lines)+'\n'
report+='''
**Lectura:** COSI-shrink50 mejora la distribución fuente y la resistencia a fallos frente a MHU-wide-proxy, pero es peor con el cambio de covarianza (~0,02615 frente a 0,02500). Por tanto, NO domina a todos los rivales bajo todos los criterios.

**Comparaciones pareadas exploratorias, COSI-shrink50 menos MHU-wide (8 semillas):** fuente −0,00505, IC bootstrap percentil 95% [−0,00538,−0,00472]; fallos −0,00429 [−0,00462,−0,00395]; shift +0,00115 [+0,00059,+0,00173]. Los intervalos describen solo variación entre estas ocho semillas sintéticas, no incertidumbre en dominios reales ni corrección por selección sucesiva.

## Síntesis epistemológica
- **Conservamos MHU:** como inductor espectral fuertemente orientado a señales suaves de frecuencia conocida y finita. Nunca decir HU asintótica probada.
- **Conservamos LOCAL SI:** como regularizador de cobertura/repulsión local, sin pretensión de familia matemática nueva.
- **Descartamos superioridad universal MHU:** FPS fue claramente competitivo/mejor fuera de banda y en cobertura; Sobol ya fue superior en la clasificación real previa.
- **Mejora de diseño:** COSI-shrink es candidato a sucesor **para sensores multiclase con covarianzas aproximadamente estables** y fallos locales, no un nuevo SOTA neuronal.
- **Originalidad:** la función objetivo equivale a métodos conocidos de muestreo por kernels; la posible novedad requeriría mostrar que una regla recurrente multihiperuniforme + condicionamiento dinámico supera diseño por GP/MI, blue noise multiclase, kernel herding, FPS, CVT, Sobol, Local SI y redes estándar, con una predicción transferible pre-registrada en datos reales 3D y convergencia del entrenamiento.
- **Gating AB06:** el requerimiento de datos espaciales 3D reales, Wei original/competidor equivalente etiquetado y FLOPs/sensores pareados **NO se ha satisfecho**. Por consiguiente, estos son cuatro ciclos **exploratorios** con valor de criba, no ciclos confirmatorios 2/3.

## Priors LARP nuevos — añadir al ledger maestro sin borrar anteriores
| Prior | Antecedente | Evidencia favorable | Evidencia adversa | Grado |
|---|---|---|---|---|
| LARP-AB4-P01 | MHU domina fuera de banda | Espectro objetivo k1 suprimido | FPS mejora k2–3 (0,01206 vs MHU-proxy 0,02311) | Debilitado |
| LARP-AB4-P02 | Local-SI + cobertura puede complementar la supresión espectral | Híbrido baja error k2–3 MHU→0,01454 | FPS 0,01206 aún mejor | Exploratorio |
| LARP-AB4-P03 | Covarianza de roles es señal útil para distribución espacial | COSI en fuente 0,01382 vs 0,01841 de MHU-wide | Pierde con cambio de covarianza | Apoyo condicionado |
| LARP-AB4-P04 | Contracción isotrópica reduce sobreajuste a covariance pilot | COSI-shrink50 en fuente y caída de nodos mejora sobre COSI | Shift empeora frente MHU-wide 0,02615 vs 0,02500 | Apoyo condicionado |
| LARP-AB4-P05 | COSI es principio matemático nuevo | Ninguna evidencia | Equivale a discrepancia kernel matricial / cuadratura conocida | No acreditado |
| LARP-AB4-P06 | Ya hay transferencia a 3D neuronal real | Ninguna | Datos reales inaccesibles; no se entrenó modelo neuronal 3D | Pendiente: barrera |

**Regla de cierre AB:** sin elevar a resultados confirmatorios los valores sintéticos; detener nuevas iteraciones Fourier sin comparación competente y base empírica 3D; pivotar hacia benchmark 3D real con adquisición correlacionada y fallo por regiones, más kernel quadrature/GP y red neuronal recurrente como rivales.

## Reproducción local
```
pip install numpy scipy matplotlib
python laboratorio_ab4.py --quick
python evaluar_bandas_ab4.py
python covarianza_ab4.py
python robustez_ab4.py
```
Los scripts crean `ab4_data/metrics.json`, `bands.json`, `covariance.json` y `robustness.json`. Las figuras incluidas son `AB4_bandas.png`, `AB4_robustez.png`, representadas con matplotlib y datos medidos, no generadas con DALL-E. Las semillas y reglas de test están explícitas. El método no usa la implementación MHU Scale3D original, cuyos resultados no deben recalificarse usando estas cifras.
'''
(base/'LARP_AB4_DICTAMEN_20261022.md').write_text(report,encoding='utf-8')
# Add provenance manifest and package
sources=['laboratorio_ab4.py','evaluar_bandas_ab4.py','covarianza_ab4.py','robustez_ab4.py','generar_informe_ab4.py',
 'AB4_bandas.png','AB4_robustez.png','LARP_AB4_DICTAMEN_20261022.md']
sources+=['ab4_data/'+x for x in ['metrics.json','summary.json','bands.json','covariance.json','robustness.json']]
manifest={s:hashlib.sha256((base/s).read_bytes()).hexdigest() for s in sources}
(base/'AB4_SHA256.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(base/'LARP_AB4_paquete_reproducible.zip','w',zipfile.ZIP_DEFLATED,compresslevel=8) as zz:
 for s in sources+['AB4_SHA256.json']:
  zz.write(base/s,arcname=s)
print('created',[str(base/p) for p in ['LARP_AB4_DICTAMEN_20261022.md','LARP_AB4_paquete_reproducible.zip','AB4_bandas.png','AB4_robustez.png']])
