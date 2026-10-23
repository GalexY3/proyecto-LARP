"""Expand five post-execution GitHub archives into per-cycle JSON without changing provenance."""
from pathlib import Path
import argparse,base64,gzip,json,hashlib
base=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('--output',default='unpacked_raw')
args=p.parse_args()
dest=(base/args.output).resolve()
count=0
for b in range(1,6):
    src=base/'results'/'raw'/f'B{b:02d}_RAW.json.gz.b64'
    raw=gzip.decompress(base64.b64decode(src.read_text().strip()))
    data=json.loads(raw)
    assert data['block']==f'B{b:02d}'
    assert data['release_status']=='POST_EXECUTION_RAW_ARCHIVAL_NOT_PREREG'
    ids=list(data['six_cycles'])
    assert ids==[f'C{i:02d}' for i in range((b-1)*6+1,b*6+1)]
    for cycle,payload in data['six_cycles'].items():
        for kind in ('spec','validation','test','audit','loss_vectors'):
            d=dest/kind
            d.mkdir(parents=True,exist_ok=True)
            (d/f'{cycle}.json').write_text(json.dumps(payload[kind],indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        count+=1
print(f'Expanded {count} cycles from versioned post-execution archives; raw JSON values recovered')
