"""Restore frozen Python engine from three compressed GitHub blobs; audit exact SHA."""
from pathlib import Path
import base64,gzip,hashlib
r=Path(__file__).resolve().parent
orig='41a7ffe9b64a6eb4694969f6bd08bc5fcd401f3d79372990c67725cb0e310ee7'
patched='20e0c44f5bf813be9e6516fd2b3de00501c6034e028f7b8bfbc126eb912516fc'
parts=''.join((r/f'engine.py.gz.b64.part{i}').read_text().strip() for i in (1,2,3))
code=gzip.decompress(base64.b64decode(parts))
assert hashlib.sha256(code).hexdigest()==orig
a=b"            a=label_survey(rngA,data,spec['a'],**cfg)\n            b=label_survey(rngB,data,spec['b'],**cfg)"
b=b"            cfg_a={**cfg,'proxy':spec.get('proxy_a',cfg['proxy'])}\n            cfg_b={**cfg,'proxy':spec.get('proxy_b',cfg['proxy'])}\n            a=label_survey(rngA,data,spec['a'],**cfg_a)\n            b=label_survey(rngB,data,spec['b'],**cfg_b)"
assert code.count(a)==1
v2=code.replace(a,b)
assert hashlib.sha256(v2).hexdigest()==patched
(r/'engine_B01_original.py').write_bytes(code)
(r/'engine_B02_onwards.py').write_bytes(v2)
print('Source v1/v2 verified')
