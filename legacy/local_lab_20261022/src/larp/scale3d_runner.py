"""Launch one authorized CUDA job and bound its own worker without a service."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback
import uuid

ROOT = Path(__file__).resolve().parents[2]
HARD_LIMIT_SECONDS = 21600


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def publish(path, value, *, exclusive=False):
    path = Path(path)
    content = json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
    if exclusive:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(content)
    else:
        temporary = path.with_suffix(path.suffix + ".next")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)


def runtime_environment(venv_python, *, inherited=None, root=ROOT):
    environment = dict(os.environ if inherited is None else inherited)
    # Launch native CPython directly, retaining the selected virtual environment.
    environment["__PYVENV_LAUNCHER__"] = str(Path(venv_python).resolve())
    previous_path = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = str(Path(root) / "src") + (
        os.pathsep + previous_path if previous_path else ""
    )
    environment["PYTHONUNBUFFERED"] = "1"
    environment.setdefault("OMP_NUM_THREADS", "8")
    environment.setdefault("MKL_NUM_THREADS", "8")
    return environment


def worker_command(config, output, *, base_python=None):
    native_python = Path(base_python or sys._base_executable).resolve()
    return [str(native_python), "-B", "-m", "larp.scale3d_train", "--config",
            str(Path(config).resolve()), "--output", str(Path(output).resolve()), "--execute"]


def hidden_flags():
    if os.name == "nt":
        return subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
    return 0


def job_budget(config):
    value = float(config["maximum_job_seconds"])
    if not math.isfinite(value) or not 0 < value <= HARD_LIMIT_SECONDS:
        raise ValueError("maximum_job_seconds must be positive and at most 21600")
    return value


def wait_owned_process(process, seconds):
    """Only the Popen instance created here may be terminated on a timeout."""
    try:
        return {"status": "FINISHED", "returncode": process.wait(timeout=seconds)}
    except subprocess.TimeoutExpired:
        process.kill()
        returncode = process.wait(timeout=30)
        return {"status": "HARD_TIMEOUT", "returncode": returncode}


def launch(config_path, output, *, venv_python=None):
    config_path, output = Path(config_path).resolve(), Path(output).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    budget = job_budget(config)
    venv_python = Path(venv_python or sys.executable).resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise FileExistsError(f"Refusing to reuse a nonempty run directory: {output}")
    token = uuid.uuid4().hex
    lock = {"token": token, "config": str(config_path), "output": str(output),
            "requested_UTC": utc_now(), "launcher_pid": os.getpid(),
            "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
            "maximum_job_seconds": budget}
    # This permanent exclusive record also prevents concurrent duplicate launches.
    publish(output / "launch.lock", lock, exclusive=True)
    command = [str(Path(sys._base_executable).resolve()), "-B", "-m",
               "larp.scale3d_runner", "--guard", "--config", str(config_path),
               "--output", str(output), "--venv-python", str(venv_python),
               "--token", token]
    try:
        with (output / "guardian.log").open("x", encoding="utf-8") as log:
            process = subprocess.Popen(
                command, cwd=str(ROOT), env=runtime_environment(venv_python),
                stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                creationflags=hidden_flags(), close_fds=True,
            )
        receipt = {"status": "GUARDIAN_LAUNCHED", "guardian_pid": process.pid,
                   "launcher_pid": os.getpid(), "launched_UTC": utc_now(),
                   "command": command, "venv_python": str(venv_python),
                   "maximum_job_seconds": budget, "config": str(config_path),
                   "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
                   "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   "output": str(output), "guardian_log": str(output / "guardian.log"),
                   "worker_log": str(output / "worker.log")}
        publish(output / "launch.json", receipt, exclusive=True)
        return receipt
    except BaseException as error:
        publish(output / "launch_failure.json", {"status": "LAUNCH_FAILED",
                "error": repr(error), "UTC": utc_now()}, exclusive=True)
        raise


def guard(config_path, output, venv_python, token):
    config_path, output = Path(config_path).resolve(), Path(output).resolve()
    lock = json.loads((output / "launch.lock").read_text(encoding="utf-8"))
    if (not token or lock.get("token") != token or lock.get("config") != str(config_path)
            or lock.get("output") != str(output)):
        raise ValueError("Guardian does not own the requested launch lock")
    if lock.get("config_sha256") != hashlib.sha256(config_path.read_bytes()).hexdigest():
        raise ValueError("Configuration changed after launch")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    budget = job_budget(config)
    command = worker_command(config_path, output)
    started = time.monotonic()
    receipt = {"status": "STARTING", "guardian_pid": os.getpid(),
               "started_UTC": utc_now(), "command": command,
               "config_sha256": lock["config_sha256"],
               "venv_python": str(Path(venv_python).resolve()),
               "maximum_job_seconds": budget, "output": str(output)}
    publish(output / "runner.json", receipt, exclusive=True)
    process = None
    try:
        with (output / "worker.log").open("x", encoding="utf-8") as log:
            process = subprocess.Popen(
                command, cwd=str(ROOT), env=runtime_environment(venv_python),
                stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                creationflags=hidden_flags(), close_fds=True,
            )
            receipt.update(status="RUNNING", worker_pid=process.pid)
            publish(output / "runner.json", receipt)
            receipt.update(wait_owned_process(process, max(.001, budget - (time.monotonic() - started))))
        protocol = output / "protocol.json"
        if protocol.exists():
            protocol_pid = json.loads(protocol.read_text(encoding="utf-8")).get("pid")
            receipt["protocol_pid"] = protocol_pid
            receipt["protocol_pid_matches_worker"] = protocol_pid == process.pid
            if protocol_pid != process.pid:
                receipt["status"] = "PROTOCOL_PID_MISMATCH"
        if receipt["status"] == "FINISHED":
            receipt["status"] = "FINISHED" if receipt["returncode"] == 0 else "WORKER_FAILED"
        if receipt["status"] == "HARD_TIMEOUT":
            progress_path = output / "progress.json"
            previous = json.loads(progress_path.read_text(encoding="utf-8")) if progress_path.exists() else None
            publish(progress_path, {"status": "HARD_TIMEOUT", "pid": process.pid,
                    "guardian_pid": os.getpid(), "last_worker_progress": previous})
    except BaseException as error:
        # Exceptions here must not leave this runner's GPU worker running.
        if process is not None and process.poll() is None:
            process.kill()
            process.wait(timeout=30)
        receipt.update(status="GUARDIAN_FAILED", error=repr(error), traceback=traceback.format_exc())
    receipt.update(finished_UTC=utc_now(), elapsed_seconds=time.monotonic() - started)
    publish(output / "runner.json", receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--launch", action="store_true")
    parser.add_argument("--guard", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--venv-python", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--token", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.guard:
        if args.launch or not args.venv_python or not args.token:
            parser.error("Internal guardian requires a virtual environment and launch token")
        result = guard(args.config, args.output, args.venv_python, args.token)
    elif args.launch:
        result = launch(args.config, args.output, venv_python=args.venv_python)
    else:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        result = {"status": "DRY_RUN", "command": worker_command(args.config, args.output),
                  "maximum_job_seconds": job_budget(config)}
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
