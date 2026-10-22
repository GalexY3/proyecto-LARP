import hashlib
import json
import os
import subprocess
import sys

import pytest

from larp import scale3d_runner as runner


def test_native_worker_argv_and_environment_retain_selected_venv(tmp_path):
    base = tmp_path / "native-python.exe"
    venv = tmp_path / "venv" / "Scripts" / "python.exe"
    command = runner.worker_command(tmp_path / "config.json", tmp_path / "run", base_python=base)
    assert command[0] == str(base.resolve())
    assert command[1:4] == ["-B", "-m", "larp.scale3d_train"]
    assert command[-1] == "--execute"
    environment = runner.runtime_environment(venv, inherited={"CUSTOM": "kept", "PYTHONPATH": "other"}, root=tmp_path)
    assert environment["__PYVENV_LAUNCHER__"] == str(venv.resolve())
    assert environment["PYTHONPATH"].startswith(str(tmp_path / "src"))
    assert environment["PYTHONPATH"].endswith("other")
    assert environment["CUSTOM"] == "kept"


@pytest.mark.skipif(os.name != "nt", reason="Windows CPython virtual-environment launcher contract")
def test_native_python_short_process_really_uses_selected_venv():
    completed = subprocess.run(
        [sys._base_executable, "-B", "-c", "import json,sys; print(json.dumps({'prefix':sys.prefix,'base_prefix':sys.base_prefix,'executable':sys.executable}))"],
        env=runner.runtime_environment(sys.executable), capture_output=True, text=True,
        timeout=10, creationflags=runner.hidden_flags(), check=True,
    )
    state = json.loads(completed.stdout)
    assert os.path.normcase(state["prefix"]) == os.path.normcase(sys.prefix)
    assert os.path.normcase(state["base_prefix"]) == os.path.normcase(sys.base_prefix)
    assert os.path.normcase(state["executable"]) == os.path.normcase(sys.executable)


class OwnedProcess:
    def __init__(self, timeout):
        self.timeout = timeout
        self.kills = 0
        self.waits = []

    def wait(self, timeout):
        self.waits.append(timeout)
        if self.timeout and self.kills == 0:
            raise subprocess.TimeoutExpired("owned-process", timeout)
        return 7 if self.kills else 0

    def kill(self):
        self.kills += 1


def test_timeout_only_kills_the_owned_process_and_reaps_it():
    owned, other = OwnedProcess(True), OwnedProcess(False)
    assert runner.wait_owned_process(owned, .1) == {"status": "HARD_TIMEOUT", "returncode": 7}
    assert owned.kills == 1 and owned.waits == [.1, 30]
    assert other.kills == 0 and other.waits == []


def test_normal_exit_is_never_killed():
    owned = OwnedProcess(False)
    assert runner.wait_owned_process(owned, 2) == {"status": "FINISHED", "returncode": 0}
    assert owned.kills == 0


def test_launch_refuses_existing_run_before_spawning(tmp_path, monkeypatch):
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"maximum_job_seconds": 1}), encoding="utf-8")
    output = tmp_path / "run"
    output.mkdir()
    original = output / "protocol.json"
    original.write_text("preserve", encoding="utf-8")
    monkeypatch.setattr(runner.subprocess, "Popen", lambda *a, **k: pytest.fail("must not spawn"))
    with pytest.raises(FileExistsError):
        runner.launch(config, output)
    assert original.read_text(encoding="utf-8") == "preserve"


def test_launch_lock_and_receipt_are_exclusive_and_preserve_budget(tmp_path, monkeypatch):
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"maximum_job_seconds": 600}), encoding="utf-8")
    output = tmp_path / "run"
    seen = {}

    def fake_popen(command, **kwargs):
        seen.update(command=command, **kwargs)
        return type("Process", (), {"pid": 7123})()

    monkeypatch.setattr(runner.subprocess, "Popen", fake_popen)
    receipt = runner.launch(config, output, venv_python=tmp_path / "venv-python.exe")
    assert receipt["guardian_pid"] == 7123
    assert receipt["maximum_job_seconds"] == 600
    assert "--guard" in seen["command"]
    assert seen["stdin"] == subprocess.DEVNULL
    lock = json.loads((output / "launch.lock").read_text(encoding="utf-8"))
    assert lock["config"] == str(config.resolve())
    assert lock["token"] in seen["command"]
    assert json.loads((output / "launch.json").read_text(encoding="utf-8"))["guardian_pid"] == 7123
    with pytest.raises(FileExistsError):
        runner.launch(config, output)


@pytest.mark.parametrize("budget", [0, -1, 21601, float("inf"), float("nan")])
def test_invalid_or_unbounded_budget_rejected(budget):
    with pytest.raises(ValueError):
        runner.job_budget({"maximum_job_seconds": budget})


@pytest.mark.parametrize("protocol_pid, expected", [(4312, "FINISHED"), (99, "PROTOCOL_PID_MISMATCH")])
def test_guard_records_native_worker_ownership_and_terminal_receipt(tmp_path, monkeypatch, protocol_pid, expected):
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"maximum_job_seconds": 600}), encoding="utf-8")
    output = tmp_path / "run"
    output.mkdir()
    runner.publish(output / "launch.lock", {"token": "owned", "config": str(config.resolve()),
                   "output": str(output.resolve()),
                   "config_sha256": hashlib.sha256(config.read_bytes()).hexdigest()}, exclusive=True)

    def fake_popen(*args, **kwargs):
        runner.publish(output / "protocol.json", {"pid": protocol_pid}, exclusive=True)
        process = OwnedProcess(False)
        process.pid = 4312
        return process

    monkeypatch.setattr(runner.subprocess, "Popen", fake_popen)
    result = runner.guard(config, output, tmp_path / "venv-python.exe", "owned")
    assert result["status"] == expected
    assert result["worker_pid"] == 4312
    assert result["protocol_pid_matches_worker"] == (protocol_pid == 4312)
    assert json.loads((output / "runner.json").read_text(encoding="utf-8"))["status"] == expected


def test_guard_rejects_foreign_launch_before_spawning(tmp_path, monkeypatch):
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"maximum_job_seconds": 600}), encoding="utf-8")
    output = tmp_path / "run"
    output.mkdir()
    runner.publish(output / "launch.lock", {"token": "owned", "config": str(config.resolve()),
                   "output": str(output.resolve())}, exclusive=True)
    monkeypatch.setattr(runner.subprocess, "Popen", lambda *a, **k: pytest.fail("must not spawn"))
    with pytest.raises(ValueError, match="does not own"):
        runner.guard(config, output, tmp_path / "venv-python.exe", "foreign")
