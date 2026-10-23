import json,sys
from pathlib import Path
from engine import NAMES,ARMS,run
root=Path(__file__).resolve().parents[1]
block=int(sys.argv[1]); phase=sys.argv[2]
for i,dataset in enumerate(NAMES):
    n=(block-1)*6+i+1
    a,b=ARMS[block-1]
    spec=dict(id=f'C{n:02d}',block=f'B{block:02d}',dataset=dataset,a=a,b=b,claim=f'On {dataset}, the {a} predictor gives lower one-step MAE than {b} on the chronological evaluation window',null='E[|Y-A|-|Y-B|]>=0',alternative='E[|Y-A|-|Y-B|]<0',falsifier='point delta >=0 or CI overlaps 0',source='statsmodels.datasets',exposure='public historical observed data, never previously evaluated in this LARP branch',budget='same observations and one-step horizon',holdout_status='final 25 percent locked until all thirty validation records exist',selection='BXX hypothesis fixed prevalidation')
    p=root/'prereg'/f'C{n:02d}.json';p.write_text(json.dumps(spec,indent=2)+'\n')
    out=run(spec,phase)
    q=root/'results'/phase/f'C{n:02d}.json';q.parent.mkdir(exist_ok=True,parents=True);q.write_text(json.dumps(out,indent=2)+'\n')
    print(f'{n:02} {dataset:12} n={out["n"]:4} dnorm={out["normalized_delta"]:+.3f} d={out["raw_delta_mae"]:+.5f} ci=[{out["ci95"][0]:+.5f},{out["ci95"][1]:+.5f}] static={out["choice"]}',flush=True)