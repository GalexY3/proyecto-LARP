"""Build an A-J reading dossier from the GitHub block preregistrations and results CSV."""
import csv,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest={s['id']:s for b in range(1,6) for s in json.loads((root/'prereg'/f'B{b:02}.json').read_text())['specs']}
with open(root/'results'/'RESULTS_30.csv') as f: rows=list(csv.DictReader(f))
assert len(rows)==30 and len(manifest)==30
out=['# LARP: ledger reproducible A–J (versión derivada del GitHub CSV)','', 'Los IC95 son descriptivos, no confirmaciones. No hay datos externos independientes, ni MHU certificada, ni código original Wei. La unidad independiente es la semilla de geometría dentro de cada generador; Digits reusa el mismo dataset.','']
for x in rows:
 s=manifest[x['id']]; lo=float(x['ci95_lower']); hi=float(x['ci95_upper']); d=float(x['delta_a_minus_b']); expected=(d>0 if s['direction']=='higher' else d<0)
 out.extend([f'## {x["id"]} · {s["kind"]}: {s["a"]} vs {s["b"]}', '', f'**A.** Pregunta/estimando: {s["claim"]}. Unidad: semilla; endpoint: {s.get("primary_endpoint",s["kind"])}.', f'**B.** Hipótesis alternativa frente a nula de delta 0; rivales: {s.get("rivals",[])}; H_otras abiertas.', f'**C.** Prueba congelada por bloque: {len(s["seeds"])} semillas; dirección {s["direction"]}; falsador: {s.get("falsification_rule","delta en dirección opuesta")}.', f'**D.** Instrumentación: versión del motor {s["source_code_commit"]}; mismos ejemplos y semillas dentro de cada par; algoritmo reproducible, pero costes no siempre emparejados.', f'**E.** A={x["mean_a"]}; B={x["mean_b"]}; A−B={d:.10g}; IC95=[{lo:.10g},{hi:.10g}]; dirección preferida={expected}.', '**F.** Auditoría: selección exploratoria y datos repetidos; comprobar exposición de holdout, multiplicidad, objetivo favorecido por la construcción y controles insuficientes (Wei no ejecutado).', '**G.** Confirmación externa: NO REALIZADA; semillas del mismo generador no constituyen replicación externa.', f'**H.** Actualización cualitativa: {"apoyo limitado dentro del modelo" if expected else "contradicción o límite dentro del modelo"}; nueva hipótesis discriminante requiere otros datos y controles. No asignar probabilidad previa inventada.', '**I.** Validez: condicionada al generador; causalidad MHU: no identificada; transportabilidad baja; originalidad 2/3 NO; ética sin datos personales; clon limpio no verificado.', f'**J.** {"PIVOT entre bloques" if int(x["id"][1:]) in (6,12,18,24) else "CIERRE DE CUPO" if x["id"]=="N30" else "CONTINUE"}.', ''])
(root/'reports').mkdir(exist_ok=True)
(root/'reports'/'LEDGER_FROM_GITHUB.md').write_text('\n'.join(out)+'\n')
print('Created',len(rows),'cycle ledgers')
