"""Portable stdlib-only verifier for archived LARP research bundles.
Run: python research/AB_ARCHIVE_20261030/verify_repo_archives.py
No network, dataset download, CPU training, or write access needed.
Original mathematical results are not independently proved by this script.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parent
PACK=ROOT/'packages'
FILES={
 'formal':('LARP_MHU_FORMAL_18_CICLOS.zip','fc22523748d7e1c42b6d56be25c3c66cf0bfb5fe46032b2a9622deb34452baac'),
 'sisters':('LARP_MHU_HERMANAS_AB20_20261030.zip','6c234a97d8cd38a7c01442536bb0ea049ae5b9c1c5ebb89f9ed02aef5cfdc7fb'),
 'vision_c01':('LARP_VISION_AB_C01_20261029.zip','2594f2c073a32251d6cd98576304b03a241d8ee710ef5815063bef697eb95f06'),
 'vision_c02':('LARP_VISION_AB_C02_20261029.zip','ded310f787f22352200223642b1af0328715ddafe965b0ae8143747f3f3a6cbd'),
 'vision_c04':('LARP_VISION_C04_20261029.zip','dd6f72fc47a3f685b7b82e095660a852637fd2e1735c4e67cdf47a3b161be99b'),
}

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def verify():
 out={'status':'PASS','checks':[]}
 for kind,(name,expected) in FILES.items():
  p=PACK/name
  row={'kind':kind,'file':str(p.relative_to(ROOT)),'sha256_expected':expected}
  if not p.exists():raise FileNotFoundError(p)
  row['sha256_observed']=sha(p.read_bytes())
  if row['sha256_observed']!=expected:raise ValueError(f'{name}: SHA mismatch')
  with ZipFile(p) as z:
   if len(set(z.namelist()))!=len(z.namelist()):raise ValueError(f'{name}: duplicate member names')
   bad=z.testzip()
   if bad:raise ValueError(f'{name}: CRC mismatch {bad}')
   row['num_members']=len(z.namelist())
   if 'MANIFEST_SHA256.json' in z.namelist():
    m=json.loads(z.read('MANIFEST_SHA256.json'))
    for e in m['files']:
     member=e.get('file',e.get('path'))
     data=z.read(member)
     if sha(data)!=e['sha256'] or len(data)!=e.get('bytes',e.get('size')):
      raise ValueError(f'{name}: manifest mismatch for {member}')
    row['manifest_members_verified']=len(m['files'])
   else:
    row['manifest_members_verified']=None
   if kind=='vision_c01':
    a=json.loads(z.read('results_original.json'));b=json.loads(z.read('results_repaired.json'))
    if len(a['results'])!=1404 or len(b['results'])!=1404:raise ValueError('C01 incomplete')
    row['raw_records']=len(b['results']);row['repair']='POST_EXPOSURE'
   elif kind=='vision_c02':
    b=json.loads(z.read('results_c02.json'))
    if len(b['observations'])!=648:raise ValueError('C02 incomplete')
    row['raw_records']=648
   elif kind=='vision_c04':
    b=json.loads(z.read('c04_results.json'))
    if len(b['observations'])!=32400:raise ValueError('C04 incomplete')
    row['raw_records']=32400
   elif kind=='formal':
    if len(json.loads(z.read('LEDGER_M01_M18.json'))['cycles'])!=18:raise ValueError('M ledger incomplete')
   elif kind=='sisters':
    if len(json.loads(z.read('LEDGER_S01_S20.json'))['cycles'])!=20:raise ValueError('S ledger incomplete')
  out['checks'].append(row)
 out['note']='Artifact and manifest validity only; NOT training reproducibility, formal proof certification or scientific novelty.'
 return out

if __name__=='__main__':
 try:
  result=verify();print(json.dumps(result,ensure_ascii=False,indent=2));print('ARCHIVES VERIFIED',len(result['checks']),'of',len(FILES))
 except Exception as exc:
  print('ARCHIVE VERIFICATION FAILED:',str(exc),file=sys.stderr);raise SystemExit(1)
