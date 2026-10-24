"""Reconstruct source v1 and repaired R1 engine from GitHub archived parts."""
import base64,gzip,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
z=''.join((p/f'experiment.py.gz.b64.part{i}').read_text().strip() for i in (1,2,3))
b=gzip.decompress(base64.b64decode(z))
assert hashlib.sha256(b).hexdigest()=='f800f562eb72d0e5d4784bb8d0ffe35f9f60d5d45e87d49631c4eb452265d47a'
start=b.index(b'def apportion(');stop=b.index(b'\ndef candidates(',start)
replacement='''def apportion(target,counts,B):
    """Bounded Hamilton largest remainders after reserving one label per stratum."""
    weights=np.maximum(np.asarray(target,float),0)
    counts=np.asarray(counts,int)
    assert len(weights)==len(counts)==3 and 3<=B<=sum(counts)
    if weights.sum()<=0:weights=np.ones(3)
    weights=weights/weights.sum()
    ideal=1+(B-3)*weights
    v=np.minimum(np.floor(ideal).astype(int),counts)
    v=np.maximum(v,1)
    # Assign remaining seats by the largest underallocation to the ideal
    while v.sum()<B:
        room=np.where(v<counts)[0]
        assert len(room)>0
        i=room[int(np.argmax(ideal[room]-v[room]))]
        v[i]+=1
    # When a stratum saturated (not seen in the current sources), repair overflows
    while v.sum()>B:
        excess=np.where(v>1)[0]
        i=excess[int(np.argmin(ideal[excess]-v[excess]))]
        v[i]-=1
    assert sum(v)==B and (v>=1).all() and (v<=counts).all()
    return tuple(map(int,v))
'''.encode()
patched=b[:start]+replacement+b[stop:]
assert hashlib.sha256(patched).hexdigest()=='ad330115b84f9e47b8d0372c8d3b6222ae5c34b916b0d364d9a34b82c7449b14'
(p/'experiment_v1_INVALID.py').write_bytes(b)
(p/'experiment_R1.py').write_bytes(patched)
print('Both sources recovered and their exact SHA256 values verified.')
