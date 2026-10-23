"""Adversarial audit & full A-J report, always after final test gate."""
from pathlib import Path
import sys, json, hashlib, math, csv, zipfile
import numpy as np
import pandas as pd
from scipy.stats import t as student_t
from statsmodels.stats.multitest import multipletests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from engine import load, forecast, split, ARMS, NAMES
names={'nile':'Caudal del Nilo','sunspots':'Manchas solares','co2':'CO₂ Mauna Loa','realgdp':'PIB real EE. UU. (log)','elnino':'Temperaturas El Niño','interest':'Tipo de interés'}
recs=[]; sign_matches=0; audit={}
for dataset in NAMES:
    y=load(dataset); windows=split(len(y)); early=windows['development']; cutoff=windows['validation'][1]
    sub,_=forecast(y[:cutoff],early); whole,choice=forecast(y,early)
    vv=np.arange(*windows['validation']);
    for arm in ['persistence','mean4','mean16','ewma03','trend8','adaptive','fixed']:
        assert np.allclose(sub[arm][vv],whole[arm][vv],rtol=0,atol=0,equal_nan=False), (dataset,arm,'test leak')
    for t0 in (max(34,int(.53*len(y))),int(.75*len(y))+3):
        if t0>=len(y):continue
        forged=y.copy();forged[t0:]+=23456
        alt,_=forecast(forged,early)
        for arm in whole:
            assert math.isclose(float(alt[arm][t0]),float(whole[arm][t0]),abs_tol=1e-11,rel_tol=1e-11), (dataset,arm,t0)
    audit[dataset]={'n':len(y),'sha256_series':hashlib.sha256(y.astype('<f8').tobytes()).hexdigest(),'validation_cutoff':cutoff,'final_start':windows['test'][0],'fixed_expert':choice,'zero_future_leak_check':'PASS','counterfactual_future_corruption':'PASS'}
    for idx,(a,b) in enumerate(ARMS):
        k=idx*6+NAMES.index(dataset)+1; cid=f'C{k:02d}'
        val=json.loads((ROOT/'results'/'validation'/f'{cid}.json').read_text())
        test=json.loads((ROOT/'results'/'test'/f'{cid}.json').read_text())
        inds=np.arange(*windows['test']); da=np.abs(y[inds]-whole[a][inds])-np.abs(y[inds]-whole[b][inds])
        assert np.isclose(da.mean(),test['raw_delta_mae'],atol=1e-12)
        assert test['data_sha256']==audit[dataset]['sha256_series']
        n=len(da)
        lag={'co2':52,'elnino':12,'sunspots':11,'realgdp':4,'interest':4,'nile':5}[dataset]
        lag=min(lag,n-2)
        center=da-da.mean()
        v=float(np.mean(center*center))
        for h in range(1,lag+1):
            v+=2*(1-h/(lag+1))*float(np.mean(center[h:]*center[:-h]))
        v=max(v,0.)
        se=np.sqrt(v/n)
        stat=float(da.mean()/se) if se>1e-14 else 0.
        p2=float(2*student_t.sf(abs(stat),df=max(n-1,1))) if se>1e-14 else 1.
        agree=np.sign(val['raw_delta_mae'])==np.sign(test['raw_delta_mae'])
        sign_matches+=agree
        r={**test,'val_delta':val['raw_delta_mae'],'val_normalized_delta':val['normalized_delta'],'same_direction_validation_test':bool(agree),'hac_lag':lag,'hac_se_delta':float(se),'hac_t':stat,'hac_two_sided_p_descriptive':p2,'mean_delta_loss':float(np.mean(da))}
        (ROOT/'results'/'test_enriched').mkdir(exist_ok=True,parents=True)
        (ROOT/'results'/'test_enriched'/f'{cid}.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
        (ROOT/'results'/'test_loss_vectors').mkdir(exist_ok=True,parents=True)
        (ROOT/'results'/'test_loss_vectors'/f'{cid}.json').write_text(json.dumps({'id':cid,'index':inds.tolist(),'actual':y[inds].tolist(),'arm_a':whole[a][inds].tolist(),'arm_b':whole[b][inds].tolist(),'absolute_loss_delta':da.tolist()},ensure_ascii=False)+'\n')
        recs.append(r)
pvals=[r['hac_two_sided_p_descriptive'] for r in recs]
reject,adj,_,_=multipletests(pvals,alpha=.05,method='holm')
for r,p,k in zip(recs,adj,reject):r['holm_p_descriptive']=float(p);r['holm_reject_descriptive']=bool(k)
report=ROOT/'reports';report.mkdir(exist_ok=True)
with open(report/'SUMMARY_30.csv','w',newline='') as f:
    fields=['id','dataset','n','a','b','val_delta','raw_delta_mae','normalized_delta','mae_a','mae_b','ci95','same_direction_validation_test','hac_lag','hac_se_delta','hac_two_sided_p_descriptive','holm_p_descriptive','holm_reject_descriptive','choice','data_sha256']
    w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(recs)
# Full A–J, truthful conditional G
lines=['# LARP AB30-TS — Treinta expedientes AB A–J','',
'Fecha: 23-10-2026. Preguntas congeladas por bloque ANTES de validación y test; código en GitHub antes de ejecución, anti-leak amendment antes de correr B01. Solo una apertura colectiva del test. A–J plenamente documentado no equivale a originalidad 2/3.','',
'**G significa aquí RECONTRASTE CRONOLÓGICO INTERNO**: un tramo posterior, nunca usado para escoger comparaciones; no una réplica externa de otro investigador, institución o instrumento. La misma serie aparece en cinco hipótesis y existe dependencia temporal; tests y multiplicidad son descriptivos.','']
for r in recs:
    cid=r['id'];i=int(cid[1:]);block=(i-1)//6; a,b=r['a'],r['b'];s=r['dataset']; d=r['raw_delta_mae']; ci=r['ci95'];v=r['val_delta'];sign='a favor de A' if d<0 else 'en contra de A'
    lines += [f'## {cid} — {names[s]}: {a} vs {b}','',
    f'**A. Verdad/estimando:** diferencia de MAE a un paso en la porción final cronológica de {names[s]}, unidades originales de serie transformada como en instrumento (PIB en log). n={r["n"]}. No estimación causal.',
    f'**B. Rivales:** H1 predice MAE({a}) inferior a MAE({b}); H0 delta≥0; H_otras tendencia, ciclo, persistencia, autocorrelación, outliers y cambios de régimen. Teoría de forecasting clásica antecedente.',
    f'**C. Contrato discriminante:** serie={s}, origen statsmodels datasets; desarrollo 35–50%, validación 50–75%, TEST cronológico 75–100%, un paso rodante con historia observada; todos los brazos sin coste extra de datos, aunque difieren en cómputo. 1499 remuestras circulares por bloques; falsador delta≥0; si IC incluye 0 es inconcluso.',
    f'**D. Instrumentación:** código Git SHA y registro de fuente bloqueado previo, antileak [validación truncada]; verifica causalidad por corrupción contrafactual del futuro, SHA256 de serie={r["data_sha256"]}; elección experta fija={r["choice"]}, datos faltantes CO₂ solo ffill. Mismo período para ambos brazos.',
    f'**E. Ejecución:** validación Δ={v:+.6g}; test Δ={d:+.6g}, MAE(A)={r["mae_a"]:.6g}, MAE(B)={r["mae_b"]:.6g}; efecto normalizado vs MAE persistencia={r["normalized_delta"]:+.3f}; IC95 bootstrap test=[{ci[0]:+.6g},{ci[1]:+.6g}]; {sign}. Resultados de pérdidas por instante en results/test_loss_vectors/{cid}.json.',
    f'**F. Auditoría adversarial:** dependencia temporal (HAC lag={r["hac_lag"]}), p bilateral HAC exploratorio={r["hac_two_sided_p_descriptive"]:.4g}, Holm descriptivo sobre 30 comparaciones={r["holm_p_descriptive"]:.4g}; aproximación asintótica, bajo tamaño efectivo/ciclo el p puede estar mal calibrado. Comparación sin tuning post-test; test no es estación independiente del mismo proceso.',
    f'**G. Recontraste:** la dirección val/test {"COINCIDE" if r["same_direction_validation_test"] else "CAMBIA"}. Estado G_INTERNAL_CHRONOLOGICAL_HOLDOUT; REPLICACIÓN EXTERNA NO REALIZADA. El test se abrió tras registrar los 30 diseños y validaciones.',
    f'**H. Actualización AB:** {"apoyo descriptivo condicionado" if d<0 else "contradicción de la superioridad esperada"}; el mecanismo no está identificado por esta diferencia. Contraevidencia: {"intervalo cruza cero, incertidumbre sustancial" if ci[0]<=0<=ci[1] else "señal más estable dentro de la serie, pero posible tendencia o periodo"}. Ni el resultado usado para generar una explicación ni estas variantes prueban esa explicación. Prior acumulativo se anota en PRIORS_DELTA.md.',
    '**I. Dictamen por dimensiones:** integridad del código y comparación temporal auditadas; validez causal N/A; transporte limitado a proceso/periodo; modelos clásicos sin novedad 2/3; relevancia operacional contextual; coste mínimo, datos históricos públicos, sin intervención sobre personas; no evidencia de método AB superior.',
    f'**J. AB-DECIDE:** {"REJECT_GENERAL_SUPERIORITY" if d>=0 else "RETAIN_DOMAIN_BOUND_CONTRAST"}; no tunear sobre holdout. Campaña CLOSE_30 al finalizar y PIVOT a predicción con datastream futuro verdaderamente externo solo si el valor de información lo justifica.','']
(report/'LEDGER_AJ_30.md').write_text('\n'.join(lines)+'\n')
# Priors
neg=sum(1 for r in recs if r['raw_delta_mae']<0); valneg=sum(1 for r in recs if r['val_delta']<0)
consistent=sum(r['same_direction_validation_test'] for r in recs)
byblock=[]
for j,(a,b) in enumerate(ARMS):
 rs=[r for r in recs if (int(r['id'][1:])-1)//6==j]
 byblock.append({'block':j+1,'a':a,'b':b,'test_A_improves_count':sum(r['raw_delta_mae']<0 for r in rs),'all_six':len(rs)})
assert all(k['all_six']==6 for k in byblock)
priors='''# Priors acumulativos nuevos — LARP AB30-TS (real, histórico, pronóstico)

Estos priors son incrementales y NO sustituyen los anteriores. No se asignan posteriors numéricas ficticias. Cada proposición especifica evidencia contraria, alcance y falsador.

**TS-P01 (diferenciación por proceso):** la historia reciente tiene valor desigual en procesos observados. B01 y B02 apoyan persistencia/ventana corta para CO2, log PIB e intereses, pero no establecen dominancia sobre ciclos. Contra: Nilo inconcluso, manchas solares y El Niño muestran heterogeneidad. Alcance: seis series históricas de statsmodels. Falsador: mismas predicciones en fuentes temporales externas y periodos posteriores.

**TS-P02 (periodicidad):** EWMA alpha=.3 mejora sobre media4 en Sunspots y El Niño, pero empeora CO2 y log PIB. Explicación por periodicidad NO identificada; faltan modelos estacionales ARIMA competentes y comparaciones con armónicos. Alcance: descriptivo. Falsador: controlar estacionalidad/ciclo y repetir con modelos competentes y cambios de periodo.

**TS-P03 (riesgo de extrapolación):** tendencia lineal sobre ocho instantes frecuentemente agrava error en procesos cíclicos (Sunspots, El Niño). Contra: log PIB y Nilo tienen puntos negativos/inconclusos; horizontes y escalas varían. Conocido en forecasting clásico. Falsador: diseño rolling multi-horizonte con tendencia calibrada antes de evaluar.

**TS-P04 (agregación de expertos):** ponderar por los últimos doce errores NO supera al experto fijo elegido solamente en desarrollo para estas fuentes y configuraciones. Contra: un ensemble adaptativo optimizado ex ante o con regularización adecuada puede mejorar; no generalizar. El baseline fijo es particularmente fuerte donde persiste buena predicción. Falsador: drift prospectivo de distribución frente a métodos Hedge/online aggregation bien calibrados.

**TS-P05 (validación y holdout):** comparar validación 50–75% con test cronológico 75–100% ofrece una comprobación interna más exigente que remuestrear semillas de un generador, pero los procesos siguen siendo los mismos y la inferencia HAC/moving-block es aproximada. Contra: series muy autocorreladas reducen N efectivo; no nuevo estudio independiente. Falsador: réplica temporal verdaderamente posterior al cierre o nuevos instrumentos.

**TS-P06 (metodología AB):** un flujo freeze–validate–branch–unseal-test obliga a preservar negativos y previene parte del peeking, pero NO demuestra que AB sea científicamente superior al diseño experimental convencional. Falsador: estudio de eficiencia AB vs expertos con misma información/recursos y resultados externos.
'''
(report/'PRIORS_DELTA.md').write_text(priors)
summary=dict(n_cycles=len(recs),validation_sign_favorable=valneg,test_sign_favorable=neg,same_sign_validation_test=consistent,descriptive_holm_count=sum(r['holm_reject_descriptive'] for r in recs),blocks=byblock,chronological_test_consumed=True,external_replications=0,originality_2_3=0,leakage_checks=audit,raw_test_losses_available=True)
(report/'AUDIT_SUMMARY.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
# Plot faceted as separate generated matplotlib figures
plt.figure(figsize=(12,7)); a=np.arange(1,31);vals=[r['normalized_delta'] for r in recs]
plt.axhline(0,linewidth=1)
plt.plot(a,vals,marker='o',linestyle='none');plt.xticks(a,rotation=90)
plt.xlabel('Ciclo AB');plt.ylabel('ΔMAE / MAE(persistencia) (menos = favorable al método A)')
plt.title('LARP AB30-TS · Test cronológico, 30 hipótesis congeladas')
plt.tight_layout();plt.savefig(ROOT/'figures'/'test_30_normalized.png',dpi=180);plt.close()
print(json.dumps({k:summary[k] for k in ('n_cycles','test_sign_favorable','validation_sign_favorable','same_sign_validation_test','descriptive_holm_count','blocks')},ensure_ascii=False,indent=2))