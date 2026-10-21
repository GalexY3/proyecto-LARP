"""AB 3.2.1 exploratory 30-cycle dynamic program. Sources original archived Scale3D geometries.
30 separate falsifiable questions; stages chosen based on evidence and registered next-decision.
No independence claimed across cycle questions. CPU / NumPy / SciPy; no external data.
"""
import os, math, json, hashlib, time
from pathlib import Path
from itertools import product
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import qmc
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data'; D.mkdir(exist_ok=True)
SEEDS=range(5201,5205); TYPES=5
COUNTS=np.array([1669,871,696,512,348]); TYPEIDX=[np.flatnonzero(np.repeat(np.arange(5),COUNTS)==i) for i in range(5)]
PATTERNS={}; LABS={}; SOURCES={}
for seed in SEEDS:
 z=np.load(D/f'orig_{seed}.npz'); labels=z['labels'].astype(int); assert sorted(np.bincount(labels).tolist())==sorted(COUNTS.tolist())
 LABS[seed]=labels; PATTERNS[seed]={k:z[k].astype(np.float64)%1 for k in ('initial','local','mhu')}
 zc=np.load(D/f'cvt_refined_4096_{1701+(seed-5201)%3}.npz'); l2=zc['labels']; cvt=np.empty((4096,3))
 for t in range(5):cvt[labels==t]=zc['points'][l2==t]
 PATTERNS[seed]['cvt']=cvt
 sob=np.empty((4096,3));lat=np.empty((4096,3));latin=np.empty((4096,3))
 for t in range(5):
  ids=np.where(labels==t)[0];n=len(ids)
  sob[ids]=qmc.Sobol(3,scramble=True,seed=seed*13+t).random_base2(math.ceil(math.log2(n)))[:n]
  # Periodic rank-1 lattice, one random torus shift per type. No jitter or exception for resonance.
  g=17+2*t;vec=np.array([1,g,g*g]);lat[ids]=((np.arange(n)[:,None]*vec[None,:])%n)/n+np.random.default_rng(seed*41+t).random(3)
  latin[ids]=qmc.LatinHypercube(3,scramble=True,seed=seed*31+t).random(n)
 PATTERNS[seed]['sobol']=sob%1;PATTERNS[seed]['lattice']=lat%1;PATTERNS[seed]['lhs']=latin%1
 assert all(p.shape==(4096,3) and np.isfinite(p).all() for p in PATTERNS[seed].values())
NAMES=list(PATTERNS[5201]); N=len(NAMES)
ALLMODES=np.array([p for p in product(range(-7,8),repeat=3) if p!=(0,0,0) and (p[0]>0 or (p[0]==0 and p[1]>0) or (p[0]==p[1]==0 and p[2]>0))],int)
NORM2=np.sum(ALLMODES**2,axis=1)
# Fixed BEFORE looking at results. Distinguish finite optimized band from nonoptimized frequency shells.
BANDS={'low':ALLMODES[NORM2<=6], 'medium':ALLMODES[(NORM2>6)&(NORM2<=24)], 'high':ALLMODES[(NORM2>24)&(NORM2<=80)]}
for k in ('medium','high'):
 rg=np.random.default_rng(11442 if k=='medium' else 11693)
 BANDS[k]=BANDS[k][rg.choice(len(BANDS[k]),min(48,len(BANDS[k])),replace=False)]
print('BANDS', {k:len(v) for k,v in BANDS.items()}, 'patterns',NAMES,flush=True)
# Returns exact complex sample means e^{i2pi k.x}, one per mode; squared magnitude = S(k)/n.
CACHE={}
def amps(seed,name,band,t=-1):
 key=(seed,name,band,t)
 if key in CACHE:return CACHE[key]
 pts=PATTERNS[seed][name];lab=LABS[seed]
 if t!=-1:pts=pts[lab==t]
 ph=2*np.pi*pts@BANDS[band].T
 out=np.exp(1j*ph).mean(axis=0)
 CACHE[key]=out
 return out

def power(seed,name,band,t=-1):return float(np.mean(abs(amps(seed,name,band,t))**2))

def paired_metric(fn,band='low'):
 return {name:float(np.mean([fn(seed,name,band) for seed in SEEDS])) for name in NAMES}

def coverage(seed,name,k=16,queries=800):
 p=PATTERNS[seed][name];lab=LABS[seed];q=np.random.default_rng(seed+88770).random((queries,3));dist,ix=cKDTree(p,boxsize=1).query(q,k=k)
 return float(np.mean(np.stack([(lab[ix]==t).any(1) for t in range(5)],axis=1).all(1)))

LOG=[]; TESTS={}
def cycle(number,title,hypothesis,rivals,measure,falsifier,next_rule,phase='experimental',notes=''):
 assert number==len(LOG)+1
 finite={str(k):v for k,v in measure.items()}
 def sanitize(v):
  if isinstance(v,(np.integer,np.floating)):return float(v)
  if isinstance(v,np.ndarray):return v.tolist()
  if isinstance(v,dict):return {str(k):sanitize(val) for k,val in v.items()}
  if isinstance(v,(list,tuple)):return [sanitize(u) for u in v]
  return v
 measure=sanitize(finite)
 entry={'id':f'C{number:02d}','phase':phase,'question':title,'hypothesis':hypothesis,'rivals':rivals,'observation':measure,'falsifier':falsifier,'AB_DECIDE':next_rule[0],'next_question_selected_after_observation':next_rule[1],'interpretation_limit':notes or 'Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.'}
 LOG.append(entry)
 (D/'cycles_running.json').write_text(json.dumps(LOG,indent=2,ensure_ascii=False,allow_nan=False))
 print(f'C{number:02d}',title, next_rule[0],json.dumps(measure,default=str)[:250],flush=True)
 return measure

def means_power(band,t=-1):return paired_metric(lambda s,n,b:power(s,n,b,t),band)

def wins(d,ref='mhu'):
 return sorted(d,key=lambda n:d[n])[0]

# C01 — independent source integrity and structural invariants
hashes={str(s):hashlib.sha256((D/f'orig_{s}.npz').read_bytes()).hexdigest() for s in SEEDS}
c1=cycle(1,'Procedencia y cuotas de las cuatro geometrías originales','No leakage por reetiquetado o fallo de distribución','Etiquetas erróneas, fuga de observaciones, fuentes duplicadas',{'sha256':hashes,'counts':COUNTS.tolist(),'unique_samples':len(set(hashes.values()))},'Identidad de archivos repetidos o cuotas inválidas',('CONTINUE','¿La penalización MHU reduce amplitudes bajas por tipo?'),'audit')
# C02 — low spectrum all types: separate objective vs performance
pall={n:np.mean([power(s,n,'low',-1) for s in SEEDS]) for n in NAMES}
c2=cycle(2,'Varianza espectral baja de población total','MHU suprime amplitud de modos bajos','CVT, Sobol, retícula, azar',{'mean_sq_complex':pall},'MHU no inferior a LOCAL',('CONTINUE','¿La supresión afecta a cada especie?'),notes='Exact Fourier sum, not claim asymptotic hyperuniformity.')
# C03 — per type suppression / worst rare type
per={n:{str(t):float(np.mean([power(s,n,'low',t) for s in SEEDS])) for t in range(5)} for n in NAMES}
c3=cycle(3,'Especies individuales y la peor clase','MHU suprime amplitud en las cinco especies','Supresión sólo en población global; tipo raro deteriorado',{'per_type_powers':per,'worst_per_type':{n:max(per[n].values()) for n in NAMES}},'MHU no mejora peor especie frente a LOCAL',('CONTINUE','¿La varianza de integración se deduce de estas amplitudes?'))
# C04 — exact Fourier identity trial
s=5201;n='mhu';k=BANDS['low'][0];p=PATTERNS[s][n][LABS[s]==4];z=np.exp(2j*np.pi*p@k).mean();phis=np.random.default_rng(550).uniform(0,2*np.pi,12000)
mean2=float(np.mean(np.real(z*np.exp(1j*phis))**2));exact=.5*abs(z)**2
c4=cycle(4,'Identidad exacta: error de un seno aleatorizado','E_phi error cuadrático=S(k)/(2n)','Efecto distinto a la optimización espectral',{'observed_MC':mean2,'analytic':exact,'relative_deviation':abs(mean2-exact)/max(exact,1e-20)},'Relación falla por fórmula o normalización',('CONTINUE','¿Cómo compite MHU con muestreadores QMC especializados?'),'analytic + numeric', 'La identidad es álgebra conocida, no novedad.')
# C05 — Sobol
q=means_power('low',t=4)
c5=cycle(5,'Comparador Sobol por especie menos abundante','MHU aventaja a Sobol aleatorizado en error medio Fourier','Sobol QMC gana sin hiperuniformidad construida',{'low_power_rare':q,'ratio_MHU_to_Sobol':q['mhu']/max(q['sobol'],1e-20)},'Sobol iguala/supera la supresión MHU',('CONTINUE','¿Una retícula de rango uno domina ambas?'))
# C06 — lattice
q=means_power('low')
c6=cycle(6,'Regla reticular trasladada como comparador fuerte','MHU sigue competitiva en integrales periódicas suaves','Regla de retícula anula modos no resonantes exactamente',{'low_total_power':q,'ratio_MHU_to_lattice':q['mhu']/max(q['lattice'],1e-30)},'Retícula mejora drásticamente modo de integración elegido',('PIVOT','¿Hay trade-off de cobertura de tipos entre retícula y MHU?' if q['lattice']<q['mhu'] else '¿Cómo cambia frecuencia sin resonancia?'),notes='Rank-1 lattice no equivale a Wei; baseline construido y declarado. Puede tener resonancias a frecuencias altas.')
# C07 — geometry v spectrum Pareto
q={n:float(np.mean([coverage(s,n) for s in SEEDS])) for n in NAMES}
c7=cycle(7,'Compromiso entre cobertura local y supresión espectral','Retícula óptima Fourier también cubre tipos localmente','Cobertura y S(k) no cooptimizan',{'coverage16':q,'low_spectral':pall},'Método domina en ambas sin coste',('CONTINUE','¿CVT ofrece un compromiso mejor que las dos?'))
# C08 — CVT Pareto non-dominance
d={n:{'coverage':q[n],'spectral_power':pall[n]} for n in NAMES}
pareto=[n for n in NAMES if not any((d[m]['coverage']>=d[n]['coverage'] and d[m]['spectral_power']<=d[n]['spectral_power'] and (d[m]['coverage']>d[n]['coverage'] or d[m]['spectral_power']<d[n]['spectral_power'])) for m in NAMES if m!=n)]
c8=cycle(8,'Frontera de Pareto para cobertura y cuadratura','MHU exhibe intercambio defendible frente a CVT/Lattice','Dominancia completa por un método clásico',{'pareto_methods':pareto,'comparators':d},'MHU dominada en las dos métricas',('CONTINUE','¿Se mantiene fuera de modos optimizados?'),notes='Pareto de dos métricas y métodos finitos, no teorema de optimalidad.')
# C09 — medium band
med=means_power('medium')
c9=cycle(9,'Generalización fuera de la banda Fourier baja','Ventaja espectral MHU persiste a frecuencias medias','Sobreajuste al espectro de la pérdida',{'medium_spectral':med,'ratio_MHU_to_LOCAL':med['mhu']/max(med['local'],1e-20)},'La supresión se pierde o invierte',('CONTINUE','¿Cuál es el riesgo en frecuencias altas?'))
# C10 — high band
high=means_power('high')
c10=cycle(10,'Riesgo de amplitudes altas y aliasing','Suprimir modos bajos no aumenta modos altos','Desplazamiento de energía espectral al exterior',{'high_spectral':high,'ratio_MHU_to_LOCAL':high['mhu']/max(high['local'],1e-20),'ratio_MHU_to_Sobol':high['mhu']/max(high['sobol'],1e-20)},'Potencia MHU supera claramente LOCAL/Sobol en banda alta',('CONTINUE','¿Existe orientación direccional privilegiada?'))
# End stage 1
print('STAGE_A_COMPLETE',len(LOG),flush=True)
# C11 — audit whether 'high' really held out; original spectral constraints cutoff
sys_path=__import__('sys');sys_path.path.insert(0,'/mnt/data')
from BR30_scale3d_geometry_original import reciprocal_modes
cutoffs={str(n):int(reciprocal_modes(int(n))[1]) for n in [4096]+COUNTS.tolist()}
frac_high_in_union=float(np.mean(np.sum(BANDS['high']**2,axis=1)<=cutoffs['4096']))
c11=cycle(11,'Auditoría de fuga: frecuencia alta realmente fuera del objetivo','La banda high verifica generalización espectral fuera de train','Corte union k²=78 y tipos menores, banda high parcialmente dentro',{'cutoff_k2':cutoffs,'high_inside_union_fraction':frac_high_in_union},'Toda o parte de high estaba entrenada',('REPAIR','Redefinir una banda estrictamente exterior y repetir diagnóstico'),phase='audit',notes='Corrección obligatoria: las anteriores medidas medium/high NO eran un holdout seguro del objetivo espectral de unión.')
# C12 — disjoint band outside all admitted original union constraint
rg=np.random.default_rng(2229)
out=ALLMODES[(NORM2>=100)&(NORM2<=140)]
BANDS['outside']=out[rg.choice(len(out),min(42,len(out)),replace=False)]
outpower=means_power('outside')
c12=cycle(12,'Extrapolación a modos fuera del corte spectral del conjunto','MHU reduce amplitudes también fuera de modos optimizados','S(k) se desplaza a modos vecinos; CVT/QMC mejora',{'outside_k2_range':[int(np.min(np.sum(BANDS['outside']**2,axis=1))),int(np.max(np.sum(BANDS['outside']**2,axis=1)))],'power':outpower,'ratio_mhu_local':outpower['mhu']/outpower['local']},'MHU pierde la supresión fuera de banda',('CONTINUE','Aislar si la especie escasa, cuya banda es menor, mantiene la ganancia'))
# C13 — single-species cutoff lower than population union
rarity={n:{'low':power(5201,n,'low',4),'medium':power(5201,n,'medium',4),'outside':power(5201,n,'outside',4)} for n in NAMES}
c13=cycle(13,'Cambio de banda por especie escasa','Especie rara retiene regularidad espectral aun superando su k²=13','Cae la protección fuera de su propia penalización',{'rare_type_cutoff_k2':cutoffs['348'],'powers_seed5201':rarity},'Fuera del corte raro MHU se comporta como CVT',('CONTINUE','Comprobar anisotropía direccional y coste de regularidad'))
# C14 — axis vs diagonal in low band, compare directional variation (not overinterpret)
axis=np.count_nonzero(BANDS['low'],axis=1)==1
ang={}
for n in NAMES:
 vals=[]
 for s in SEEDS:
  p=amps(s,n,'low',-1)
  vals.append((float(np.mean(abs(p[axis])**2)),float(np.mean(abs(p[~axis])**2))))
 ang[n]=[float(np.mean([v[i] for v in vals])) for i in (0,1)]
c14=cycle(14,'Isotropía del error espectral: ejes frente a diagonales','MHU mantiene baja potencia en múltiples orientaciones','FFT/CIC introduce artefactos de ejes',{'power_axis_vs_mixed':ang,'mhu_axis_to_mixed':ang['mhu'][0]/max(ang['mhu'][1],1e-30)},'MHU favorece sustancialmente ejes',('CONTINUE','Buscar fallo adversarial de la retícula, comparador dominante low'))
# C15 — exact alias of lattice for integer Fourier; search a deliberately resonant mode
# for type with smallest n, lattice generator [1,25,625] and k=(-25,1,0) -> dot=0. Could be high norm.
k=np.array([-25,1,0]);phis={}
for n in NAMES:
 ph=[]
 for s in SEEDS:
  mask=LABS[s]==4;z=np.exp(2j*np.pi*PATTERNS[s][n][mask]@k).mean();ph.append(abs(z)**2)
 phis[n]=float(np.mean(ph))
c15=cycle(15,'Modo resonante adversarial para retículas exactas','Retícula es óptima universalmente porque anula 40 modos bajos','Resonancias producen S(k) grande cuando k·g=0 mod n',{'adversarial_k':k.tolist(),'power':phis},'La retícula tiene error extremo en un modo permitido',('CONTINUE','Comparar riesgo máximo, no solo media espectral'))
# C16 — max vs mean low and outside risk (noise variance risk)
tail={}
for n in NAMES:
 tail[n]={b:float(np.mean([np.max(abs(amps(s,n,b))**2) for s in SEEDS])) for b in ('low','outside')}
c16=cycle(16,'Riesgo máximo de error por modo','MHU controla tanto la media como el peor modo','Un modo mal protegido domina bajo estímulo adversarial',{'max_mode_sq_mean':tail},'MHU peor que CVT en peor modo de interés',('CONTINUE','Auditar invariancia geométrica para descartar artefactos'))
# C17 — periodic translation invariance of power: deterministic identity
qseed=5201;pos=PATTERNS[qseed]['mhu'];shift=np.array([.227,.407,.689]);kset=BANDS['low'];nloc=len(pos)
f0=np.abs(np.exp(2j*np.pi*pos@kset.T).mean(0))**2
f1=np.abs(np.exp(2j*np.pi*((pos+shift)%1)@kset.T).mean(0))**2
reldiff=float(np.max(np.abs(f0-f1)));tol=3e-13
c17=cycle(17,'Invariancia de traslación del toro','Potencia S(k) es invariante bajo traslación periódica común','Error de implementación FFT, redondeo o máscara',{'max_abs_difference':reldiff,'passed':reldiff<tol},'El desplazamiento cambia S(k) fuera de tolerancia',('CONTINUE','Examinar perturbación de coordenadas a pequeña escala'),phase='audit',notes='Control exacto, no hallazgo científico de originalidad.')
# C18 — random coordinate jitter; effect on low spectral relative to normal spacing
jr={}
for n in ('local','mhu','cvt','sobol','lattice'):
 vals=[]
 for s in SEEDS:
  p=PATTERNS[s][n];rg=np.random.default_rng(s+119);pj=(p+rg.normal(0,.006,p.shape))%1
  a=np.exp(2j*np.pi*pj@BANDS['low'].T).mean(0)
  vals.append(float(np.mean(abs(a)**2)))
 jr[n]=float(np.mean(vals))
c18=cycle(18,'Estabilidad ante desplazamientos independientes de sensores','MHU conserva supresión bajo ruido de coordenadas','Penalización hipersensible a posiciones exactas',{'jitter_sigma_unit_box':.006,'new_low_power':jr,'before':{n:pall[n] for n in jr}},'Jitter anula ganancia MHU',('CONTINUE','Ensayar fallos de disponibilidad en vez de movimiento'))
# C19 — dropout iid20, same masks per geometric seed (not exact same spatial failures)
dr={};spe=['local','mhu','cvt','sobol','lattice']
for n in spe:
 vals=[]
 for s in SEEDS:
  p=PATTERNS[s][n];lab=LABS[s];ix=np.where(lab==4)[0];rg=np.random.default_rng(9192+s)
  for r in range(4):
   take=ix[rg.random(len(ix))>=.20]; z=np.exp(2j*np.pi*p[take]@BANDS['low'].T).mean(0);vals.append(float(np.mean(abs(z)**2)))
 dr[n]=float(np.mean(vals))
c19=cycle(19,'Pérdida aleatoria del 20 % de sensores raros','MHU conserva ventaja espectral relativa tras dropout','El muestreo Bernoulli destruye el cero espectral con piso ≈p/((1-p)n)',{'rare_type_low_power_after_dropout':dr,'before':{n:per[n]['4'] for n in spe}},'El dropout borra la relación de orden original',('CONTINUE','Probar agujero espacial, menos benigno que dropout'))
# C20 — hole spatial 1/5th sub-pop: radius 0.26 on unit torus; positions common center; need strong missing ratio
hr={}
for n in spe:
 vals=[];delrates=[]
 for s in SEEDS:
  p=PATTERNS[s][n];lab=LABS[s];cent=np.random.default_rng(s+889).random(3)
  delta=(p-cent+.5)%1-.5;keep=np.linalg.norm(delta,axis=1)>=.26;ix=np.flatnonzero((lab==4)&keep)
  z=np.exp(2j*np.pi*p[ix]@BANDS['low'].T).mean(0)
  vals.append(float(np.mean(abs(z)**2)));delrates.append(float(1-len(ix)/sum(lab==4)))
 hr[n]={'spectral_power':float(np.mean(vals)),'deleted_rare_fraction':float(np.mean(delrates))}
c20=cycle(20,'Fallos espaciales correlacionados de tipo raro','MHU conserva utilidad espectral cuando se vacía una región','Todos los diseños quedan dominados por el hueco y sesgo de cobertura',{'hole_radius':.26,'outcomes':hr},'Sin ventaja MHU frente a controles después del agujero',('CONTINUE','Usar inversión causal de etiquetas para aislar origen del espectro'))
print('STAGE_B_COMPLETE',len(LOG),flush=True)
# C21 — Relabel sensor-types while keeping union point positions identical
shuff={}
for n in ('initial','local','mhu','cvt','sobol','lattice'):
 vals=[]
 for s in SEEDS:
  p=PATTERNS[s][n];lab=LABS[s];rg=np.random.default_rng(s+90001);t=lab[rg.permutation(len(lab))]
  pp=p[t==4];z=np.exp(2j*np.pi*pp@BANDS['low'].T).mean(0);vals.append(float(np.mean(abs(z)**2)))
 shuff[n]=float(np.mean(vals))
c21=cycle(21,'Ablación causal: permutar marcas de tipo manteniendo todas las posiciones','MHU precisa asignación geométrica coordinada de clases','Supresión por sola unión de puntos o etiqueta sin efecto',{'rare_type_after_shuffle':shuff,'rare_type_before':{n:per[n]['4'] for n in shuff},'union_unchanged':True},'Barajar tipos no altera espectro por clase',('CONTINUE','Demostrar relación exacta entre espectro de subtipos y el de la unión'))
# C22 — strict algebraic bound finite and limit: any fixed mixture of hyperuniform species is HU
bound_results={}
for n in NAMES:
 ratios=[];above=[]
 for s in SEEDS:
  total=amps(s,n,'low',-1);components=[amps(s,n,'low',t) for t in range(5)];ns=np.bincount(LABS[s],minlength=5);weights=ns/ns.sum()
  exact=np.sum(np.stack(components)*weights[:,None],axis=0)
  bound=(np.sum(np.abs(np.stack(components))*weights[:,None],axis=0))**2
  err=float(np.max(np.abs(exact-total)));must=float(np.max(np.maximum(abs(total)**2-bound,0)))
  above.append((err,must));ratios.append(float(np.mean(abs(total)**2)/max(float(np.mean(bound)),1e-28)))
 bound_results[n]={'ratio_actual_to_bound':float(np.mean(ratios)),'max_residual_aliased':float(np.max(above))}
c22=cycle(22,'Teorema elemental: la unión de clases HU también es HU bajo fracciones estables','Es posible mantener S_i(k)→0 en todas las especies y S_total(k) distinto de cero','La desigualdad triangular obliga S_total(k)≤(Σ sqrt(f_i S_i(k)))²','identity_bound_computation' if False else {'bound_validation':bound_results,'derivation':'A_union=Σ f_i A_i; S_total=N|A_union|² ≤ (Σ sqrt(f_i S_i))²; para fracciones f_i estables y finitas, todos S_i→0 implica S_total→0.'},'La desigualdad algebraica falla o límites sin fracciones estables',('REPAIR','Estudiar papel real de correlaciones intertipo sin repetir la premisa falsa'),phase='analytic+numeric',notes='No es una demostración novedosa. Bajo hipótesis regulares cada especie asintóticamente HU implica unión HU; la afirmación de que mezclarlas destruye necesariamente HU es falsa.')
# C23 — force independent random shifts for every type and measure union cross-interference
shifted={}
for n in ('local','mhu','cvt','sobol','lattice'):
 old=[];new=[];expected=[]
 for s in SEEDS:
  f=np.bincount(LABS[s],minlength=5)/4096.;modes=BANDS['low'];A=np.stack([amps(s,n,'low',t) for t in range(5)])
  old.append(float(np.mean(abs(amps(s,n,'low'))**2)))
  expected.append(float(np.mean(np.sum(f[:,None]**2*abs(A)**2,axis=0))))
  for rep in range(12):
   sh=np.random.default_rng(11111+s+rep).random((5,3));phase=np.exp(2j*np.pi*sh@modes.T)
   amp=(f[:,None]*A*phase).sum(axis=0)
   new.append(float(np.mean(abs(amp)**2)))
 shifted[n]={'original_union':float(np.mean(old)),'independently_shifted_union':float(np.mean(new)),'expected_from_no_cross':float(np.mean(expected))}
c23=cycle(23,'Correlación cruzada: trasladar cada clase independientemente','Correlación entre tipos reduce S_total más que composición por tipo','La fase relativa puede aumentar o disminuir union S sin alterar S_i',{'union_spectral_by_shift':shifted},'Unión no cambia nunca tras traslaciones independientes',('CONTINUE','Comprobar integración conjunta ponderada de funciones distintas por tipo'),notes='Contraste de correlaciones de fase a N finito; no implica que suma de HU deje de ser HU.')
# C24 — weighted multi-sensor integrals with unknown Fourier coefficients per channel, true integral 0
wt=np.array([.2]*5)
err={}
for n in NAMES:
 mse=[]
 for s in SEEDS:
  AA=np.stack([amps(s,n,'low',t) for t in range(5)])
  rg=np.random.default_rng(4488+s);coeff=rg.normal(size=(1000,5,len(BANDS['low'])))+1j*rg.normal(size=(1000,5,len(BANDS['low'])))
  coefficient=(coeff*AA[None,:,:]).real.sum(axis=2)/np.sqrt(len(BANDS['low']))
  result=coefficient@wt;mse.append(np.mean(result**2))
 err[n]=float(np.mean(mse))
c24=cycle(24,'Cuadratura multi-canal: una función Fourier desconocida distinta por tipo','MHU reduce error de agregación de cinco especializaciones','Rank-one lattice puede integrar mejor señales periódicas compatibles',{'mse_1000_fourier_coeff_draws_per_geometry':err,'weight_per_type':wt.tolist()},'MHU no mejora a retícula o Sobol',('CONTINUE','¿La ventaja está limitada por ruido de medida independiente?'),notes='Estímulos sintéticos periódicos y regla de promedio conocida; no modelo neuronal ni test externo.')
# C25 — noise floor independent of spatial layout: no design can beat iid readout noise with fixed n
noise_var=.1**2
n=COUNTS;floor=float(noise_var*np.sum(wt**2/n));non_noise={n:err[n] for n in NAMES}
c25=cycle(25,'Límite por ruido independiente de sensor','Geometría espectral también suprime ruido blanco de lectura','La varianza iid del promedio queda fijada por n y pesos','noise_floor' if False else {'sigma_noise':.1,'variance_floor':floor,'noiseless_mse':non_noise},'Una geometría mejora el término blanco iid en igualdad de número de lecturas',('CONTINUE','¿Las clases raras dominan la pérdida aunque el conjunto esté muy regular?'),phase='analytic+numeric',notes='Var[Σ w_t mean(noise_t)] = σ²Σ w_t²/n_t si lecturas iid sin correlación; es un piso independiente de posición.')
# C26 — type imbalance: error contribution by type under equal vs population weights. Coefficients each real/imag N(0,1), so E(Re(c*z)^2)=|z|², NOT |z|²/2 (uniform phase has half factor).
for_weights={}
for label,w in [('equal',np.ones(5)/5),('population',COUNTS/4096),('rare_priority',np.array([.1,.1,.1,.1,.6]))]:
 score={}
 for name in NAMES:
  terms=[]
  for s in SEEDS:
   AA=np.stack([amps(s,name,'low',t) for t in range(5)])
   # expected MSE for independent channel Fourier fields, E coeff real and imag iid unit / sqrt(K)
   terms.append(float(np.sum(w**2*np.mean(abs(AA)**2,axis=1))))
  score[name]=float(np.mean(terms))
 for_weights[label]=score
c26=cycle(26,'Funciones asimétricas y el cuello de botella de la especie rara','El orden de algoritmos depende del peso de la clase minoritaria','El resultado es idéntico si todas las especies se comportan igual',{'expected_weighted_error':for_weights},'Todas las ponderaciones producen la misma jerarquía',('CONTINUE','¿La ventaja spectral resiste reducción global a mitad de sensores?'))
# C27 — resource budget half types; distinction from dropout-only rare at C19
half={}
for name in ('local','mhu','cvt','sobol','lattice'):
 vals=[]
 for s in SEEDS:
  lab=LABS[s];p=PATTERNS[s][name];rg=np.random.default_rng(9900+s)
  for rep in range(3):
   pp=[]
   for t in range(5):
    ix=np.flatnonzero(lab==t);sel=rg.choice(ix,size=int(len(ix)*.5),replace=False)
    pp.append(np.exp(2j*np.pi*p[sel]@BANDS['low'].T).mean(axis=0))
   aa=np.stack(pp);vals.append(float(np.sum(wt**2*np.mean(abs(aa)**2,axis=1))))
 half[name]=float(np.mean(vals))
c27=cycle(27,'Presupuesto de 50 % de sensores por especialidad','MHU mantiene ventaja relevante al reducir coste de muestreo','El submuestreo destruye orden y favorece diseños ya baratos',{'weighted_error_half_sample':half,'full_sample':for_weights['equal']},'La ventaja desaparece a media densidad',('CONTINUE','Buscar funciones no periódicas donde un diseño QMC tenga ventaja'),notes='Pérdida real por reconstrucción del patrón tras reducir n, no escalamiento optimizador a n/2 ni coste total de generación.')
# C28 — nonperiodic, smooth except toroidal boundary: x and x*y, compare known integrals 1/2 and 1/4
npf={n:{} for n in NAMES}
for n in NAMES:
 for tag in ('x','xy','bump'):
  v=[]
  for s in SEEDS:
   pp=PATTERNS[s][n];lab=LABS[s];# average of population weighted integration for every type
   vals=[]
   for t in range(5):
    xyz=pp[lab==t]
    if tag=='x': y=xyz[:,0];true=.5
    elif tag=='xy': y=xyz[:,0]*xyz[:,1];true=.25
    else:
     # fully analytic integral of product of 1D exp(-a(x-.5)^2), no periodic boundary
     from scipy.special import erf
     alpha=20.; y=np.exp(-alpha*((xyz-.5)**2).sum(axis=1));true=(np.sqrt(np.pi/alpha)*erf(np.sqrt(alpha)/2))**3
    vals.append((float(y.mean())-true)**2)
   v.append(np.mean(vals))
  npf[n][tag]=float(np.mean(v))
c28=cycle(28,'Transferencia a integración no periódica y función localizada','MHU mantiene ventaja en funciones suaves sin estructura Fourier toroidal','Sobol/retículas o CVT más apropiados para frontera real',{'nonperiodic_integral_mse_type_averaged':npf},'MHU deja de ser competitivo cuando cambia espacio funcional',('CONTINUE','Valorar si existe una ventaja de Pareto real y si es original'),notes='x,xy y bump gaussiana tienen integrales analíticas en [0,1]^3; los resultados describen estos tres integrandos, no una población universal.')
# C29 — combine several outcomes; identify nondominance vs novelty; multi-class prior art
metrics={n:{'coverage16':q[n],'low_power':pall[n],'outside_power':outpower[n],'nonperiodic_mse':float(np.mean(list(npf[n].values())))} for n in NAMES}
pareto_all=[]
for name in NAMES:
 def dominates(x,y):
  return (x['coverage16']>=y['coverage16'] and all(x[z]<=y[z] for z in ('low_power','outside_power','nonperiodic_mse')) and (x['coverage16']>y['coverage16'] or any(x[z]<y[z] for z in ('low_power','outside_power','nonperiodic_mse'))))
 if not any(dominates(metrics[other],metrics[name]) for other in NAMES if other!=name):pareto_all.append(name)
c29=cycle(29,'Frontera multivariable y prueba de originalidad frente a muestreo conocido','MHU aporta beneficio no reproducible por multi-class blue noise, QMC, retículas','Pareto en estos indicadores no acredita novedad ni utilidad neuronal',{'four_metrics':metrics,'non_dominated':pareto_all,'prior_art':'Wei multi-class blue noise 2010; randomized low discrepancy sampling; rank-1 lattice; variance error related to power spectrum'},'Alguna comparación fuerte elimina o explica la ventaja específica',('CONTINUE','Auditoría final de resultados e independencia: AB-DECIDE'),phase='synthesis+literature',notes='La frontera depende de pesos y métricas elegidos tras exploración; comparación con Wei original NO ejecutada.')
# C30 — last audit of 30 and decision; no additional experimental claim
planned=len(LOG)+1
checks={'previous_cycles':len(LOG),'sequential_ids':all(r['id']==f'C{i+1:02d}' for i,r in enumerate(LOG)),'original_geometry_seeds':list(SEEDS),'comparator_names':NAMES,'new_geometries_from_original_this_block':0,'all_numeric_exploratory':True,'strongest_spectral_mhu_low_ratio_to_local':pall['mhu']/pall['local'],'high_outside_mhu_ratio_to_local':outpower['mhu']/outpower['local'],'lattice_aliasing_peak':phis['lattice'],'MHU_in_4metric_pareto':('mhu' in pareto_all),'external_semantic_or_GPT_benchmark_done':False,'Wei_original_executed':False}
assert checks['previous_cycles']==29 and checks['sequential_ids']
c30=cycle(30,'Auditoría de cierre y decisión sobre extensión','Existe novedad arquitectónica 2/3 o 3/3 después de 30 ciclos','Propiedad geométrica conocida, sin generalización externa ni ventaja sobre baselines mejores',checks,'Hallazgos positivos exclusivos se sostienen bajo todos los controles fuertes',('STOP_NOVELTY_CLAIM','Solicitar 8 ciclos focalizados, condicionados a experimento comparador Wei original y datos/sistemas neuronales fuera de Fourier'),phase='audit+decision',notes='Treinta decisiones científicas correlacionadas, NO treinta ensayos independientes; ningún 2/3 o 3/3 acreditado. Recomendar máximo 8 nuevos ciclos solo si se obtienen controles externos y recursos suficientes.')
assert len(LOG)==30
(ROOT/'docs'/'AB_LEDGER_C01_C30.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2,allow_nan=False))
print('ALL_30_DONE',len(LOG),flush=True)
