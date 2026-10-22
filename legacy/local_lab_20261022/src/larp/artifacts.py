"""Atomic, hash-backed records; no invented success states."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import os
import platform
import importlib.metadata
import subprocess
from collections.abc import Mapping
from datetime import datetime, timezone
import numpy as np


def json_safe(value):
    if isinstance(value, Mapping):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, np.ndarray):
        return json_safe(value.tolist())
    if isinstance(value, np.generic):
        return json_safe(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return {"nonfinite": "nan" if np.isnan(value) else "+inf" if value > 0 else "-inf"}
    if isinstance(value, Path):
        return str(value)
    return value


def canonical_json(value):
    return json.dumps(json_safe(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def array_hash(array):
    array = np.ascontiguousarray(array)
    h = hashlib.sha256()
    h.update(str(array.dtype).encode())
    h.update(str(array.shape).encode())
    h.update(array.tobytes())
    return h.hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(json_safe(value), ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    os.replace(temp, path)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def code_identity(root):
    root = Path(root)
    try:
        commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "UNCOMMITTED"
    paths = sorted((root / "src").rglob("*.py")) + sorted((root / "tests").glob("test_*.py")) + [root / "pyproject.toml",root / "requirements-lock.txt"]
    paths += sorted((root / "configs").glob("*.json"))
    paths += [root / "LARP_v0_1_RESEARCH_ARCHITECTURE_REVIEW.md"]
    files = {str(p.relative_to(root)).replace("\\", "/"): file_hash(p) for p in paths if p.exists()}
    versions = {name: importlib.metadata.version(name) for name in ["numpy","scipy","torch","matplotlib","networkx","psutil"]}
    versions["python"] = platform.python_version()
    return {"commit": commit, "source_hash": digest({"files":files,"runtime":versions}), "files": files,"runtime":versions}


def hardware():
    import psutil
    return {"platform": platform.platform(), "python": platform.python_version(),
            "cpu_count": psutil.cpu_count(), "RAM_bytes": psutil.virtual_memory().total}


def append_event(path, event):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(canonical_json({"time": utc_now(), **event}) + "\n")
