#!/usr/bin/env python3
"""Read (without changing) the six genuine native N400 NPZ files and verify exact hashes.

Requires local checkout of private GalexY3/proyecto-LARP and NumPy.
The JSON export preserves exact float64 bytes using float.hex() and is PRIVATE.
This tool was authored AFTER previous historical N400 outcomes and has NOT been
run against native files in the ChatGPT container (binary GitHub access blocked).
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np

SUB = Path("legacy/local_lab_20261022/artifacts/avian_v1")
OUT = Path("research/AB_NATIVE_AUDIT_20261030/native_exports")
SEEDS = (1101, 1102, 1103)
KINDS = ("full_spectral", "local_only")
COUNTS = [163, 85, 68, 50, 34]

def array_hash(arr):
    arr = np.ascontiguousarray(arr)
    h = hashlib.sha256()
    h.update(arr.dtype.str.encode("ascii"))
    h.update(json.dumps(arr.shape).encode("ascii"))
    h.update(arr.tobytes())
    return h.hexdigest()

def geometry_hash(points, labels, box):
    a, b = array_hash(points), array_hash(labels)
    return {"points": a, "labels": b,
            "geometry": hashlib.sha256((a+b+float(box).hex()).encode()).hexdigest()}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."),
                        help="Root of the private LARP working tree")
    parser.add_argument("--write", action="store_true",
                        help="Create private exact-bit JSON exports only after hash checks pass")
    args = parser.parse_args()
    root = args.root.resolve()
    outdir = root / OUT
    digest_records = []
    for kind in KINDS:
        for seed in SEEDS:
            stem = f"avian_{kind}_N400_g{seed}"
            npz_path = root / SUB / (stem + ".npz")
            cert_path = root / SUB / (stem + "_certificate.json")
            if not npz_path.is_file() or not cert_path.is_file():
                raise FileNotFoundError(f"Missing original pair {npz_path}, {cert_path}")
            cert = json.loads(cert_path.read_text(encoding="utf-8"))
            with np.load(npz_path, allow_pickle=False) as archive:
                points = np.array(archive["points"], copy=True)
                labels = np.array(archive["labels"], copy=True)
                box = float(archive["L"].item())
                meta = json.loads(str(archive["metadata_json"].item()))
            assert points.shape == (400, 2), (stem, points.shape)
            assert labels.shape == (400,), (stem, labels.shape)
            assert points.dtype == np.dtype("float64"), (stem, points.dtype)
            assert labels.dtype == np.dtype("int64"), (stem, labels.dtype)
            assert np.isfinite(points).all() and np.isfinite(box)
            assert np.all(points >= 0) and np.all(points < box)
            assert np.bincount(labels, minlength=5).tolist() == COUNTS
            hashes = geometry_hash(points, labels, box)
            assert hashes == cert["geometry_hashes"], (stem, "certificate hash")
            assert hashes == meta["hashes"], (stem, "metadata hash")
            # For user audit: Git object contents must match the local checkout.
            try:
                git_blob = subprocess.check_output(["git", "-C", str(root), "hash-object",
                                                    str(npz_path)], text=True).strip()
            except Exception:
                git_blob = None
            rec = {"stem": stem, "native_npz": str(npz_path.relative_to(root)),
                   "native_git_blob": git_blob, "hashes": hashes,
                   "sha256_npz": hashlib.sha256(npz_path.read_bytes()).hexdigest(),
                   "source_certificate": str(cert_path.relative_to(root)),
                   "box_hex": box.hex(), "n": 400}
            digest_records.append(rec)
            if args.write:
                outdir.mkdir(parents=True, exist_ok=True)
                payload = {**rec, "points_float64_hex":
                           [[float(x).hex() for x in row] for row in points],
                           "labels_int64": labels.astype(int).tolist()}
                dest = outdir / (stem + ".json")
                if dest.exists():
                    raise FileExistsError(f"Refusing overwrite: {dest}")
                dest.write_text(json.dumps(payload, ensure_ascii=False,
                                           separators=(",", ":"))+"\n", encoding="utf-8")
                # Decode and validate bit-for-bit against source
                check = json.loads(dest.read_text(encoding="utf-8"))
                pp = np.asarray([[float.fromhex(x) for x in row]
                                 for row in check["points_float64_hex"]], dtype=np.float64)
                ll = np.asarray(check["labels_int64"], dtype=np.int64)
                assert np.array_equal(pp.view("uint64"), points.view("uint64"))
                assert np.array_equal(ll, labels)
                assert geometry_hash(pp, ll, float.fromhex(check["box_hex"])) == hashes
    print(json.dumps({"status": "PASS_LOCAL_NATIVE_CHECKOUT",
                      "files_verified": len(digest_records), "exports_written": args.write,
                      "records": digest_records}, indent=2))

if __name__ == "__main__":
    main()
