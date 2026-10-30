#!/usr/bin/env python3
"""Verify six immutable LARP N400 NPZ blobs, preserving exact IEEE-754 bits.

This instrument does not produce scientific outcomes. Default = strict read-only.
Original repository: GalexY3/proyecto-LARP. Requires numpy, Python >=3.10.
Run only in an authorized private clone; exports remain private.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Mapping
import numpy as np

SOURCE = Path('legacy/local_lab_20261022/artifacts/avian_v1')
DEFAULT_EXPORT = Path('research/AB_NATIVE_RECOVERY_20261030/private_exports')
EXPECTED_GIT_BLOBS = {
    'avian_full_spectral_N400_g1101': '71cbbb405105e03663fbdc40cdfbe471bce29675',
    'avian_full_spectral_N400_g1102': '60d849256e624efbad46dd2127c4c1bcce8d6d55',
    'avian_full_spectral_N400_g1103': '8bad8683ef9cfa3489c6d8792f8e1c387783b9bf',
    'avian_local_only_N400_g1101': '4a77364209bb3c1cbcf1ee0f2c746490389825ea',
    'avian_local_only_N400_g1102': '0938f6eadfc95fb7d60fa3b5f5331c9bf70dc27a',
    'avian_local_only_N400_g1103': '595024b0fb801e586d264d81cf95b789aa91a29b',
}
COUNTS = (163, 85, 68, 50, 34)


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def array_hash(array: np.ndarray) -> str:
    """Matches legacy/local_lab_20261022/src/larp/geometry.py:29-35."""
    arr = np.ascontiguousarray(array)
    h = hashlib.sha256()
    h.update(arr.dtype.str.encode('ascii'))
    h.update(json.dumps(arr.shape).encode('ascii'))
    h.update(arr.tobytes())
    return h.hexdigest()


def geometry_hashes(points: np.ndarray, labels: np.ndarray, box: float) -> dict[str, str]:
    a, b = array_hash(points), array_hash(labels)
    c = hashlib.sha256((a + b + float(box).hex()).encode()).hexdigest()
    return {'points': a, 'labels': b, 'geometry': c}


def verify_one(npz_file: Path, cert_file: Path, expected_blob_sha: str) -> dict:
    raw = npz_file.read_bytes()
    actual_blob = git_blob_sha(raw)
    if actual_blob != expected_blob_sha:
        raise ValueError(f'{npz_file.name}: Git blob mismatch {actual_blob}, expected {expected_blob_sha}')
    cert = json.loads(cert_file.read_text(encoding='utf-8'))
    with np.load(npz_file, allow_pickle=False) as archive:
        if set(archive.files) != {'points', 'labels', 'L', 'metadata_json'}:
            raise ValueError(f'{npz_file.name}: unexpected NPZ member keys: {archive.files}')
        points = np.asarray(archive['points'])
        labels = np.asarray(archive['labels'])
        box = float(archive['L'].item())
        metadata = json.loads(str(archive['metadata_json'].item()))
    if points.shape != (400, 2) or points.dtype != np.dtype('<f8'):
        raise ValueError('points must be float64 400x2')
    if labels.shape != (400,) or labels.dtype != np.dtype('<i8'):
        raise ValueError('labels must be int64 length 400')
    if not np.isfinite(points).all() or not np.isfinite(box) or box <= 0:
        raise ValueError('nonfinite or nonpositive box')
    if (points < 0).any() or (points >= box).any():
        raise ValueError('points are outside [0,L)')
    if not np.array_equal(np.bincount(labels, minlength=5), COUNTS):
        raise ValueError('type quotas mismatch')
    hashes = geometry_hashes(points, labels, box)
    if hashes != cert.get('geometry_hashes') or hashes != metadata.get('hashes'):
        raise ValueError(f'{npz_file.name}: geometry/certificate/metadata SHA256 mismatch')
    return {'stem': npz_file.stem, 'npz_git_blob': actual_blob,
            'npz_sha256': hashlib.sha256(raw).hexdigest(), 'geometry_hashes': hashes,
            'L_hex': box.hex(), 'points': points, 'labels': labels}


def verify_all(root: Path, expected: Mapping[str, str] = EXPECTED_GIT_BLOBS) -> list[dict]:
    records = []
    for stem, sha in expected.items():
        records.append(verify_one(root / SOURCE / (stem + '.npz'),
                                  root / SOURCE / (stem + '_certificate.json'), sha))
    if len(records) != 6:
        raise AssertionError('Exactly six original N400 inputs required')
    for seed in (1101, 1102, 1103):
        m = {k: next(r for r in records if r['stem'] == f'avian_{k}_N400_g{seed}')
             for k in ('full_spectral', 'local_only')}
        if m['full_spectral']['geometry_hashes']['labels'] != m['local_only']['geometry_hashes']['labels']:
            raise ValueError(f'Labels unequal for paired seed {seed}')
        if m['full_spectral']['L_hex'] != m['local_only']['L_hex']:
            raise ValueError(f'Box unequal for paired seed {seed}')
    return records


def export_verified(records: list[dict], destination: Path) -> list[str]:
    """Exports only after ALL six original files verify; never overwrite."""
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f'Export directory must be empty: {destination}')
    destination.mkdir(parents=True, exist_ok=True)
    exported = []
    for r in records:
        payload = {k: r[k] for k in ('stem', 'npz_git_blob', 'npz_sha256', 'geometry_hashes', 'L_hex')}
        payload['points_float64_hex'] = [[float(x).hex() for x in pair] for pair in r['points']]
        payload['labels_int64'] = r['labels'].astype(int).tolist()
        file = destination / (r['stem'] + '.json')
        file.write_text(json.dumps(payload, separators=(',', ':')) + '\n', encoding='utf-8')
        obj = json.loads(file.read_text(encoding='utf-8'))
        points2 = np.array([[float.fromhex(x) for x in row] for row in obj['points_float64_hex']],dtype=np.float64)
        labels2 = np.array(obj['labels_int64'], dtype=np.int64)
        if not (np.array_equal(points2.view('uint64'), r['points'].view('uint64'))
                and np.array_equal(labels2.view('uint64'), r['labels'].view('uint64'))
                and geometry_hashes(points2,labels2,float.fromhex(obj['L_hex'])) == r['geometry_hashes']):
            raise AssertionError(f'Non-bit-exact exported data: {file}')
        exported.append(str(file))
    return exported


def self_test() -> dict:
    """No production bytes: synthetic fixture tests hash acceptance, tampering and exact export."""
    with tempfile.TemporaryDirectory(prefix='larp-native-smoke-') as tmp:
        root = Path(tmp)
        src = root / SOURCE
        src.mkdir(parents=True)
        rng = np.random.default_rng(7361)
        points = rng.random((400,2), dtype=np.float64) * 20
        labels = np.repeat(np.arange(5,dtype=np.int64),COUNTS)
        rng.shuffle(labels)
        shas = geometry_hashes(points,labels,20.0)
        p = src / 'synthetic_N400.npz'
        cert = src / 'synthetic_N400_certificate.json'
        with p.open('wb') as f:
            np.savez_compressed(f,points=points,labels=labels,L=np.asarray(20.0),
                metadata_json=np.asarray(json.dumps({'hashes':shas})))
        cert.write_text(json.dumps({'geometry_hashes':shas}),encoding='utf-8')
        expected_sha = git_blob_sha(p.read_bytes())
        rec = verify_one(p,cert,expected_sha)
        exact = export_verified([rec],root/'export')
        try:
            verify_one(p,cert,'0'*40)
            raise AssertionError('Tampered pinned blob should fail')
        except ValueError as e:
            assert 'Git blob mismatch' in str(e)
        try:
            export_verified([rec],root/'export')
            raise AssertionError('Overwriting an export should fail')
        except FileExistsError:
            pass
        cert.write_text(json.dumps({'geometry_hashes':{**shas,'points':'0'*64}}),encoding='utf-8')
        try:
            verify_one(p,cert,expected_sha)
            raise AssertionError('Tampered certificate should fail')
        except ValueError as e:
            assert 'mismatch' in str(e)
        return {'fixture':'SYNTHETIC_NOT_NATIVE', 'verified_fixture':True,
                'altered_npz_rejected':True, 'certificate_mismatch_rejected':True,
                'overwriting_rejected':True, 'IEEE754_float_exact_roundtrip':True,
                'exports':len(exact)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path('.'))
    ap.add_argument('--write',action='store_true',help='Export private exact JSONs; requires all six verified')
    ap.add_argument('--output',type=Path,default=DEFAULT_EXPORT)
    ap.add_argument('--self-test',action='store_true',help='Run synthetic-only unit tests; no N400 originals')
    args=ap.parse_args()
    if args.self_test:
        print(json.dumps({'status':'SELF_TEST_ONLY',**self_test()},indent=2))
        return
    records=verify_all(args.root.resolve())
    paths=[]
    if args.write:
        paths=export_verified(records,args.root.resolve()/args.output)
    print(json.dumps({'status':'SIX_NATIVE_BLOBS_VERIFIED','count':len(records),
                      'exported':paths, 'records':[
                          {k:r[k] for k in ('stem','npz_git_blob','npz_sha256','geometry_hashes','L_hex')}
                          for r in records]},indent=2))

if __name__=='__main__':
    main()
