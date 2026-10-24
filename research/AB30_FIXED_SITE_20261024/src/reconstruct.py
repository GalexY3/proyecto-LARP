"""Recover the exact AB30 experiment engine frozen before execution."""
from pathlib import Path
import hashlib,base64,gzip
root=Path(__file__).resolve().parent
encoded=''.join((root/f'experiment.py.gz.b64.part{i}').read_text().strip() for i in (1,2,3))
source=gzip.decompress(base64.b64decode(encoded))
expected='cae397a9e83a88a807ad5b77faeec1cc5a3ffdd8c682c6ee5822851fe8d2b156'
actual=hashlib.sha256(source).hexdigest()
assert actual==expected,(actual,expected)
(root/'experiment.py').write_bytes(source)
print('Verified original experiment.py:',actual,len(source),'bytes')
