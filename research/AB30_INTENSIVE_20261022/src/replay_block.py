"""Reproduce a frozen AB block from its GitHub-stored manifest. Exploratory only."""
import argparse,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('block',choices=[f'B{i:02}' for i in range(1,6)]);a=p.parse_args()
manifest=json.loads((ROOT/'prereg'/f'{a.block}.json').read_text(encoding='utf-8'))
(ROOT/'results').mkdir(exist_ok=True)
for s in manifest['specs']:
 spec=ROOT/'prereg'/f'{s["id"]}.json'
 spec.write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 subprocess.run([sys.executable,str(ROOT/'src'/'engine.py'),str(spec)],check=True)
