#!/usr/bin/env python3
"""W02 source-frozen minimal CMake policy gate. No Wei binary, no network, no LARP data."""
import hashlib
import json
import pathlib
import platform
import subprocess
import sys
import tempfile

def cmd(args, cwd=None):
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=15)
        return {"argv": args, "returncode": r.returncode, "stdout": r.stdout, "stderr": r.stderr}
    except subprocess.TimeoutExpired as e:
        return {"argv": args, "returncode": None, "timeout": True, "stdout": str(e.stdout), "stderr": str(e.stderr)}

SOURCE = """# W02 synthetic source, NOT Wei
#include <iostream>
int main() { std::cout << "W02_OK"; return 0; }
"""
ARMS = (
    ("legacy_2_6_no_flag", "2.6", []),
    ("legacy_2_6_policy_min_3_5", "2.6", ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5"]),
    ("modern_3_5_no_flag", "3.5", []),
)

def run():
    out = {"protocol": "W02", "scientific_cycle": False,
           "host": platform.platform(), "python": sys.version,
           "script_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
           "cmake": cmd(["cmake", "--version"]),
           "cxx": cmd(["g++", "--version"]), "arms": []}
    with tempfile.TemporaryDirectory(prefix="larp_w02_") as d:
        root = pathlib.Path(d)
        for label, version, flags in ARMS:
            directory = root / label
            directory.mkdir()
            (directory / "main.cpp").write_text(SOURCE, encoding="utf-8")
            cmakelists = "cmake_minimum_required(VERSION " + version + ")\nproject(LegacyMinimal LANGUAGES CXX)\nadd_executable(legacy_min main.cpp)\n"
            (directory / "CMakeLists.txt").write_text(cmakelists, encoding="utf-8")
            build = directory / "build"
            configure = cmd(["cmake", "-S", str(directory), "-B", str(build), *flags])
            compilation = cmd(["cmake", "--build", str(build), "--target", "legacy_min"]) if configure["returncode"] == 0 else None
            exe = build / "legacy_min"
            execution = cmd([str(exe)]) if exe.exists() and compilation and compilation["returncode"] == 0 else None
            out["arms"].append({
                "id": label, "min_version": version, "flags": flags,
                "source_sha256": hashlib.sha256((cmakelists + SOURCE).encode("utf-8")).hexdigest(),
                "configure": configure, "build": compilation, "run": execution,
                "build_success": bool(execution and execution["returncode"] == 0 and execution["stdout"] == "W02_OK")
            })
    return out

if __name__ == "__main__":
    p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("w02_results.json")
    p.write_text(json.dumps(run(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("W02 results saved at", p)
