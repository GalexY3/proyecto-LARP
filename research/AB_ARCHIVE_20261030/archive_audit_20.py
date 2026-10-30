"""AB-P archive integrity audit: 20 preregistered post-exposure checks.

This script verifies prior artefact consistency; it does not infer MHU superiority,
prove new mathematics, or perform external scientific replication.
Only stdlib + numpy + pandas; original ZIPs are treated as read-only sources.
"""
from __future__ import annotations

import collections
import hashlib
import json
import math
import subprocess
import sys
import traceback
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd

BASE = Path('/mnt/data')
ROOT = Path(__file__).resolve().parent
ZIP = {
 'M':BASE/'LARP_MHU_FORMAL_20261029/LARP_MHU_FORMAL_18_CICLOS.zip',
 'S':BASE/'LARP_MHU_SISTERS_20261030/LARP_MHU_HERMANAS_AB20_20261030.zip',
 'C01':BASE/'LARP_VISION_AB_20261029/LARP_VISION_AB_C01_20261029.zip',
 'C02':BASE/'LARP_VISION_AB_20261029/LARP_VISION_AB_C02_20261029.zip',
 'C04':BASE/'LARP_VISION_AB_20261029/C04/LARP_VISION_C04_20261029.zip',
}
SHA = {x:hashlib.sha256(p.read_bytes()).hexdigest() for x,p in ZIP.items()}
EXPECTED_ZIP = {
 'M':'fc22523748d7e1c42b6d56be25c3c66cf0bfb5fe46032b2a9622deb34452baac',
 'S':'6c234a97d8cd38a7c01442536bb0ea049ae5b9c1c5ebb89f9ed02aef5cfdc7fb',
 'C01':'2594f2c073a32251d6cd98576304b03a241d8ee710ef5815063bef697eb95f06',
 'C02':'ded310f787f22352200223642b1af0328715ddafe965b0ae8143747f3f3a6cbd',
 'C04':'dd6f72fc47a3f685b7b82e095660a852637fd2e1735c4e67cdf47a3b161be99b',
}
results = []

def check(id, claim, fn):
 try:
  ev=fn()
  results.append({'id':id,'claim':claim,'status':'PASS','evidence':ev})
 except Exception as e:
  results.append({'id':id,'claim':claim,'status':'FAIL','error':str(e),'traceback':traceback.format_exc(limit=3)})

def read(key,name):
 with ZipFile(ZIP[key]) as z:return z.read(name)

def get(key,name):return json.loads(read(key,name))

def assert_true(x,msg='assertion failed'):
 if not x:raise AssertionError(msg)

def same_csv(a,b,numerics):
 x=pd.read_csv(pd.io.common.BytesIO(a)).sort_values(numerics[0]).reset_index(drop=True)
 y=pd.read_csv(pd.io.common.BytesIO(b)).sort_values(numerics[0]).reset_index(drop=True)
 assert_true(x.shape==y.shape and list(x.columns)==list(y.columns),'shape/columns')
 for col in x.columns:
  if pd.api.types.is_numeric_dtype(x[col]):assert_true(np.allclose(x[col],y[col],rtol=1e-11,atol=1e-13,equal_nan=True),f'number difference {col}')
  else: assert_true(x[col].tolist()==y[col].tolist(),f'text difference {col}')
 return {'rows':len(x),'columns':list(x.columns)}

check('A01','All 5 ZIP containers are readable and have unique entry names',lambda:{k:{'num_entries':len(ZipFile(p).namelist()),'bad_crc_member':ZipFile(p).testzip()} for k,p in ZIP.items()} if all(len(z.namelist())==len(set(z.namelist())) and z.testzip() is None for z in [ZipFile(x) for x in ZIP.values()]) else (_ for _ in ()).throw(AssertionError('bad archive')))
check('A02','Five ZIP SHA256 digests equal the historical immutable bundle digests',lambda: (assert_true(SHA==EXPECTED_ZIP,{'observed':SHA}),SHA)[1])

def manifest_check(key):
 m=get(key,'MANIFEST_SHA256.json');count=0;bad=[]
 with ZipFile(ZIP[key]) as z:
  for f in m['files']:
   name=f.get('path',f.get('file'))
   data=z.read(name);hash_=hashlib.sha256(data).hexdigest()
   if hash_ != f['sha256'] or len(data)!=f.get('size',f.get('bytes')):bad.append({'file':name,'sha':hash_})
   count+=1
 assert_true(not bad, bad)
 return {'files_verified':count,'manifest_fields':list(m)}
check('A03','Embedded formal 18-file SHA manifest matches ZIP bytes',lambda:manifest_check('M'))
check('A04','Embedded sisters 20-file SHA manifest matches ZIP bytes',lambda:manifest_check('S'))

check('A05','C01 frozen original and repair code SHA identities',lambda:(assert_true(hashlib.sha256(read('C01','vision_ab_c01.py')).hexdigest()=='5e47f6e63e98dd14655f8eeec0e8d826d97eb750fd24c099ea4b6aa3e50ea993'),assert_true(hashlib.sha256(read('C01','repair_poisson.py')).hexdigest()=='85438d783f220761e1b5b8d2c678e2a77ee2787a2c7e5cbefac3b8d6d13c9570'),{'original_source_SHA256':'5e47f6e6…','repair_SHA256':'85438d78…'})[-1])

def repair_scope():
 a=get('C01','results_original.json');b=get('C01','results_repaired.json')
 assert_true(set(a)==set(b)-{'repair'} and all(a[k]==b[k] for k in a if k not in ('results','geometry')),'unexpected top-level changes')
 def compare(kind):
  aa={ (v['seed'],v['method'],v.get('image'),v.get('condition')):v for v in a[kind]}
  bb={ (v['seed'],v['method'],v.get('image'),v.get('condition')):v for v in b[kind]}
  assert_true(aa.keys()==bb.keys(),kind+' key changes')
  changed=[k for k in aa if aa[k]!=bb[k]]
  assert_true(all(k[1]=='poisson_disk' for k in changed),kind+' changes another method')
  return {'changed':len(changed),'total':len(aa),'examples':changed[:2]}
 return {'results':compare('results'),'geometry':compare('geometry'),'repair_status':b['repair']['status']}
check('A06','C01 post-outcome Poisson repair touched no other method',repair_scope)

def factorial_c01():
 r=get('C01','results_repaired.json');a=pd.DataFrame(r['results'])
 assert_true(len(a)==6*6*13*3 and len(r['geometry'])==36,'factorial counts')
 assert_true(np.isfinite(a[['mse','mae']].to_numpy()).all(),'nonfinite')
 assert_true(a.groupby(['seed','method','image','condition']).size().eq(1).all(),'duplicate factorial cell')
 return {'records':len(a),'seeds':len(r['seeds']),'images':len(r['images']),'methods':len(r['methods']),'conditions':sorted(a.condition.unique())}
check('A07','C01 exact 6×6×13×3 and finite metric rows',factorial_c01)

def aggregate_c01():
 df=pd.DataFrame(get('C01','results_repaired.json')['results']);tab=df[df.split=='TEST'].groupby(['condition','method'])['mse'].mean().unstack()
 from io import StringIO
 x=pd.read_csv(StringIO(read('C01','MSE_TEST_TABLE.csv').decode()),index_col=0)
 assert_true(tab.index.equals(x.index) and tab.columns.equals(x.columns),'index label mismatch')
 assert_true(np.allclose(tab.to_numpy(),x.to_numpy(),rtol=1e-11,atol=1e-13),'MSE mismatch')
 return {'cells':int(tab.size),'clean_joint':float(tab.loc['clean','mhu_joint'])}
check('A08','C01 TEST MSE table reproduces from raw records',aggregate_c01)

def source_c02():
 sha=hashlib.sha256(read('C02','vision_ab_c02.py')).hexdigest();assert_true(sha=='42b7bcef08ed0b02909ec4b95bbd3bbb46a338762ed011f1e8a64735b1e60729')
 f=np.array(get('C02','results_c02.json')['filters']);assert_true(f.shape==(5,3))
 return {'source_sha256':sha,'filters':f.tolist()}
check('A09','C02 code SHA frozen and sensor matrix shape verified',source_c02)

def factorial_c02():
 r=get('C02','results_c02.json');a=pd.DataFrame(r['observations'])
 assert_true(len(a)==4*6*9*3 and len(r['geometry'])==4*6,'C02 counts')
 assert_true(a.groupby(['seed','method','image','condition']).size().eq(1).all(),'duplicate C02 row')
 assert_true(np.isfinite(a[['mse','mae']].to_numpy()).all(),'nonfinite')
 return {'n':len(a),'methods':sorted(a.method.unique()),'splits':a.split.value_counts().to_dict()}
check('A10','C02 full factorial and finite observations',factorial_c02)

def aggregate_c02():
 r=get('C02','results_c02.json');df=pd.DataFrame(r['observations']);actual=df.groupby(['split','method','condition']).agg(mse=('mse','mean'),mae=('mae','mean'),n=('mse','size')).reset_index()
 published=pd.read_csv(pd.io.common.BytesIO(read('C02','C02_MEANS.csv')))
 actual=actual.sort_values(['split','method','condition']).reset_index(drop=True)
 published=published.sort_values(['split','method','condition']).reset_index(drop=True)
 assert_true(actual[['split','method','condition']].equals(published[['split','method','condition']]))
 assert_true(np.allclose(actual[['mse','mae','n']],published[['mse','mae','n']],rtol=1e-11,atol=1e-13))
 return {'groups':len(actual),'test_joint_clean':float(actual.query("split=='TEST' and method=='spectral_joint' and condition=='clean'").mse.iloc[0])}
check('A11','C02 means CSV reproduces from all raw records',aggregate_c02)
check('A12','C02 five virtual filters span only a three-dimensional RGB subspace',lambda:(assert_true(np.linalg.matrix_rank(np.array(get('C02','results_c02.json')['filters']))==3),{'rank':3,'filters':5,'physical_bands':False})[-1])

def source_c04():
 r=get('C04','c04_results.json');src=hashlib.sha256(read('C04','vision_c04.py')).hexdigest();assert_true(src=='d57d21ce76d4513419fbf38df9ec62b771872a4d50f1856a3a16133b268b31ae')
 assert_true(len(r['observations'])==32400 and len(r['methods'])==9)
 return {'code_sha256':src,'observations':len(r['observations']),'seed_count':len(r['seeds'])}
check('A13','C04 frozen code SHA and observation dimensions',source_c04)

def c04_repeats():
 r=get('C04','c04_results.json');a=pd.DataFrame(r['observations'])
 counts=a.groupby(['method','condition','image_id']).size()
 assert_true(len(set(a.image_id))==200 and counts.eq(6).all(),'cluster replication')
 assert_true(len(a)==32400 and len(counts)==9*3*200,'count mismatch')
 return {'independent_images_upper_bound':200,'repeats_per_image_method_condition':6,'total_predictions':len(a)}
check('A14','C04 images are repeated; 32,400 predictions are NOT 32,400 independent images',c04_repeats)

def c04_means():
 r=get('C04','c04_results.json');a=pd.DataFrame(r['observations']);published=pd.DataFrame(get('C04','c04_means.json'))
 computed=a.groupby(['method','condition']).correct.agg(['mean','size']).reset_index().rename(columns={'mean':'accuracy','size':'num_predictions'})
 x=published.sort_values(['method','condition']).reset_index(drop=True)
 y=computed.sort_values(['method','condition']).reset_index(drop=True)
 assert_true(x[['method','condition']].equals(y[['method','condition']]));assert_true(np.allclose(x[['accuracy','num_predictions']],y[['accuracy','num_predictions']]))
 return {'methods':len(r['methods']),'groups':len(x),'joint_clean':float(x.query("method=='spectral_joint' and condition=='clean'").accuracy.iloc[0])}
check('A15','C04 27 published means reproduce from 32,400 predictions',c04_means)

def c04_audit():
 d=get('C04','c04_audit.json');a=get('C04','c04_results.json')['observations']
 assert_true(d['n_independent_images_upper_bound']==200 and d['observations']==32400,'audit counts')
 assert_true(len(d['contrasts'])==3*8,'contrast count')
 assert_true(all('bootstrap_95_pp' in x and len(x['bootstrap_95_pp'])==2 for x in d['contrasts']))
 return {'contrasts':len(d['contrasts']),'bootstrap_resamples':d['bootstrap_reps'],'scope':'descriptive posthoc clustered by image'}
check('A16','C04 cluster bootstrap was reported as descriptive and has complete contrasts',c04_audit)

def formal_math():
 r=get('M','AUDITORIA_M01_M18.json')['tests'];assert_true(isinstance(r,dict) and len(r)==18 and all(v['verified'] for v in r.values()))
 return {'recorded_checks':len(r),'all_true':True,'source_verifier_sha256':hashlib.sha256(read('M','auditoria_formal.py')).hexdigest()}
check('A17','Formal M01–M18 recorded mathematical checker is 18/18 true',formal_math)

def sister_math():
 r=get('S','checks_20.json');assert_true(len(r['checks'])==20 and all(x['pass_check'] for x in r['checks']))
 assert_true(hashlib.sha256(read('S','checks_20.json')).hexdigest()=='87a9e4d1fe9b3964aa13156376e3f47e9b0ef81c16c7a959392c1a4caa5e689e')
 return {'recorded_checks':20,'all_true':True,'source_verifier_sha256':hashlib.sha256(read('S','audit_20.py')).hexdigest()}
check('A18','S01–S20 recorded mathematical checker matches frozen digest',sister_math)

def ledgers():
 a=get('M','LEDGER_M01_M18.json');b=get('S','LEDGER_S01_S20.json')
 ida=[x.get('id',x.get('cycle_id')) for x in a['cycles']];idb=[x.get('id',x.get('cycle_id')) for x in b['cycles']]
 assert_true(len(ida)==18 and len(set(ida))==18,'M ledger unique')
 assert_true(len(idb)==20 and len(set(idb))==20,'S ledger unique')
 assert_true(a['N1_new']==0 and b['n1_new_unique']==0 and a['N2']==0 and b['n2']==0)
 return {'M_ids':ida,'S_ids':idb,'scientific_original_discoveries':0}
check('A19','Original A–J ledgers identify 18+20 questions but zero original N1/N2/N3',ledgers)

def portability():
 # Presence of raw data bundle and clean-clone limitations are verifiable; cannot certify other-host execution.
 for k,z in ZIP.items():
  assert_true(z.is_file(),'missing '+k)
 for k,n in [('M','auditoria_formal.py'),('S','audit_20.py'),('C01','vision_ab_c01.py'),('C02','vision_ab_c02.py'),('C04','vision_c04.py')]:
  assert_true(bool(read(k,n)),f'missing {n}')
 return {'archive_containers':len(ZIP),'raw_data_in_zips':{'C01':len(get('C01','results_repaired.json')['results']),'C02':len(get('C02','results_c02.json')['observations']),'C04':len(get('C04','c04_results.json')['observations'])},'clean_clone_verified':False,'new_original_science':False}
check('A20','Scientific source and outputs recoverable; external clean clone remains unverified',portability)

out={'schema':'AB_P_ARCHIVE_20261030','date':'2026-10-30','grant':20,'declared_scope':'post-exposure reproducibility/archival, not prospective causal confirmation','original_zip_sha256':SHA,'total':len(results),'passed':sum(x['status']=='PASS' for x in results),'failed':sum(x['status']=='FAIL' for x in results),'checks':results}
file=ROOT/'AB_ARCHIVE_AUDIT_RESULTS.json';file.write_text(json.dumps(out,indent=2,ensure_ascii=False,default=str)+'\n')
print('AB ARCHIVE AUDIT',out['passed'],'/',out['total'],'pass; fails',out['failed'])
for x in results:print(x['id'],x['status'],x['claim'],x.get('error',''))
if out['failed']:
 sys.exit(2)
