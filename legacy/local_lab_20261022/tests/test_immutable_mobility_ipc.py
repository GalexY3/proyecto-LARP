"""Real-process IPC checks without importing scientific worker machinery."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/"artifacts/constrained_mobility/run_io_supplement.py"


def run_dummy(folder, *, stall=False):
    command=[sys.executable,"-B",str(RUNNER),"--dummy","--config",
             str(ROOT/"configs/constrained_mobility_v1.json"),"--output",str(folder)]
    if stall:command.append("--stall")
    return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=10)


def test_immutable_messages_and_direct_worker_identity(tmp_path):
    folder=tmp_path/"complete"
    process=run_dummy(folder)
    assert process.returncode==0,process.stderr
    assert json.loads((folder/"supervision.json").read_bytes())["status"]=="COMPLETE"
    assert json.loads((folder/"gate.json").read_bytes())["PID_PPID_verified"]
    for index in (0,1):
        assert (folder/f"start_{index}.json.ready").exists()
        assert (folder/f"end_{index}.json.ready").exists()
    assert json.loads((folder/"completion.json").read_bytes())["scientific_calls"]==0
    assert not list(folder.glob("*.tmp"))


def test_supervisor_enforces_immutable_message_deadline(tmp_path):
    folder=tmp_path/"limit"
    process=run_dummy(folder,stall=True)
    assert process.returncode!=0
    report=json.loads((folder/"supervision.json").read_bytes())
    assert report["status"]=="RESOURCE_LIMIT"
    assert report["returncode"] is not None
    assert (folder/"start_0.json.ready").exists()
    assert not (folder/"end_0.json.ready").exists()
    assert not (folder/"completion.json").exists()
