#!/usr/bin/env python3
"""W04 frozen parse-only parity gate for Wei DartThrowing ASCII stdout.

No upstream Wei source is executed and validation does not prove sampling quality.
"""
from __future__ import annotations
import hashlib
import json
import math
import re
import sys

QUOTAS = (163, 85, 68, 50, 34)
SIDE = 20.0
N = sum(QUOTAS)


class GateError(ValueError):
    def __init__(self, code: str, detail: str):
        self.code = code
        super().__init__(f"{code}: {detail}")


def validate(text: str) -> dict:
    if not isinstance(text, str):
        raise GateError("TYPE", "Expected decoded UTF-8 sample text")
    lines = text.splitlines()
    if len(lines) != N:
        raise GateError("N", f"Expected exactly {N} lines, got {len(lines)}")
    counts = [0] * len(QUOTAS)
    for lineno, line in enumerate(lines, 1):
        fields = line.split()
        if len(fields) != 3:
            raise GateError("FORMAT", f"Line {lineno}: expected class x y")
        if not re.fullmatch(r"[+-]?\d+", fields[0]):
            raise GateError("CLASS", f"Line {lineno}: invalid class token")
        label = int(fields[0])
        if not 0 <= label < len(QUOTAS):
            raise GateError("CLASS", f"Line {lineno}: class {label}")
        try:
            x, y = float(fields[1]), float(fields[2])
        except ValueError:
            raise GateError("FORMAT", f"Line {lineno}: invalid coordinate")
        if not math.isfinite(x) or not math.isfinite(y):
            raise GateError("NONFINITE", f"Line {lineno}: NaN/Inf")
        if not (0 <= x < SIDE and 0 <= y < SIDE):
            raise GateError("BOUNDS", f"Line {lineno}: outside [0,{SIDE})²")
        counts[label] += 1
    if tuple(counts) != QUOTAS:
        raise GateError("QUOTA", f"Expected {QUOTAS}, got {tuple(counts)}")
    return {
        "status": "PASS_FORMAT_AND_QUOTAS_ONLY",
        "n": N, "quotas": list(counts), "side": SIDE,
        "stdout_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "limitations": ["NO_PROOF_OF_WEI_ORIGIN", "NO_DISTANCE_OR_SPECTRAL_PARITY", "NO_SEED_REPLAY"]
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python w04_quota_gate.py samples_ascii.txt")
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            result = validate(f.read())
        print(json.dumps(result, sort_keys=True, indent=2))
    except (OSError, UnicodeError, GateError) as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc)}, ensure_ascii=False))
        sys.exit(1)
