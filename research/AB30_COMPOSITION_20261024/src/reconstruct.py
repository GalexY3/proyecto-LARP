"""Rebuild original exact engine from four GitHub fragments and prospective R1."""
import base64,gzip,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
encoded=''.join((p/f'engine.py.gz.b64.{z}').read_text().strip() for z in ('part1','part2a','part2b','part3'))
raw=gzip.decompress(base64.b64decode(encoded))
sha=lambda a:hashlib.sha256(a).hexdigest()
assert sha(raw)=='af8548b2b5f11d91233ec51e9c155a15bee21b020b8d747a0a53414d2306e55c'
s=raw.decode()
needle="E=np.mean([z['delta_A_minus_B'] for z in records if z['phase']=='E']);G=np.mean([z['delta_A_minus_B'] for z in records if z['phase']=='G'])"
assert s.count(needle)==1
s=s.replace(needle,"E=np.mean([z['delta_A_minus_B'] for z in records if z['phase']=='E']);gmean=np.mean([z['delta_A_minus_B'] for z in records if z['phase']=='G'])")
s=s.replace("'G_mean_delta':float(G)","'G_mean_delta':float(gmean)")
s=s.replace("'A' if G<0 else 'B' if G>0","'A' if gmean<0 else 'B' if gmean>0")
fixed=s.encode()
assert sha(fixed)=='e2b2668649c415a57b79039d4e05bb8216f6740ceb4a2795547eea226ae42904'
(p/'engine_restored.py').write_bytes(fixed)
print('Engine v1 and R1 verified by SHA256')
