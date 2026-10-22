"""Prevent redirector ownership failures from escaping the phase deadline."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import psutil
import pytest

SPEC = importlib.util.spec_from_file_location("information_supervisor", Path(__file__).resolve().parents[1]/"artifacts/sampling_information/run_supervised.py")
supervisor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(supervisor)


def test_real_cpython_child_owns_pid_and_timeout_leaves_no_descendants():
    # Only a synthetic sleeper; no research entry point is run.
    code = "import os,json,numpy,time; print(json.dumps({'pid':os.getpid(),'ppid':os.getppid(),'numpy':numpy.__version__}),flush=True); time.sleep(20)"
    command, env = supervisor.native_launch(["-c", code])
    process = subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
    try:
        line = process.stdout.readline()
        boot = json.loads(line)
        assert boot["pid"] == process.pid
        assert boot["ppid"] == __import__("os").getpid()
        children = psutil.Process(process.pid).children(recursive=True)
        # Windows may attach a hidden console host; it is not a Python worker.
        assert all(child.name().lower() == "conhost.exe" for child in children)
        with pytest.raises(subprocess.TimeoutExpired):
            process.communicate(timeout=.05)
    finally:
        process.kill()
        process.communicate()
    assert process.poll() is not None
    assert not psutil.pid_exists(process.pid)
    _, live = psutil.wait_procs(children, timeout=1)
    assert not live
