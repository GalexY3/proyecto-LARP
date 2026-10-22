"""Synthetic scientific invariants; no historical patterns are evaluated."""
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "artifacts/next_exploration"))
spec = importlib.util.spec_from_file_location("native_worker_test", ROOT / "artifacts/native_neighborhood/worker.py")
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)


def test_oriented_cycles_have_one_rotation_and_two_directions():
    graph = np.ones((3, 3), bool)
    np.fill_diagonal(graph, False)
    swaps, cycles = worker.enumerate_moves(graph)
    assert swaps == [(0, 1), (0, 2), (1, 2)]
    assert cycles == [(0, 1, 2), (0, 2, 1)]
    one = np.zeros((3, 3), bool)
    one[0, 1] = one[1, 2] = one[2, 0] = True
    assert worker.enumerate_moves(one) == ([], [(0, 1, 2)])


def test_native_kernel_mass_uses_all_anchors_and_exact_mixture():
    labels = np.array([0, 1, 2])
    counts = np.ones(5, int) * 4
    nearest = {(i, c): set(range(3)) for i in range(3) for c in range(3) if labels[i] != c}
    swap = worker.mass((0, 1), labels, counts, nearest)
    assert swap["near"] == Fraction(2, 320)
    assert swap["global"] == Fraction(1, 160)
    cycle = worker.mass((0, 1, 2), labels, counts, nearest)
    assert cycle["near"] == Fraction(3, 3840)
    assert cycle["global"] == Fraction(1, 1280)
    assert cycle["mixture"] == Fraction(4, 5) * cycle["near"] + Fraction(1, 5) * cycle["global"]


def test_publication_is_exclusive_and_ready_follows_close(tmp_path):
    from bounded import publish, ready, read
    import pytest
    path = tmp_path / "record.json"
    assert not ready(path)
    publish(path, {"n": 130})
    assert ready(path) and read(path) == {"n": 130}
    with pytest.raises(FileExistsError):
        publish(path, {"n": 0})


def test_supervisor_terminates_owned_worker_before_global_deadline(tmp_path):
    # A synthetic worker holds after boot; no scientific imports or datasets.
    output = tmp_path / "run"
    output.mkdir()
    runner = ROOT / "artifacts/next_exploration/bounded.py"
    fake = tmp_path / "fake.py"
    fake.write_text("import sys,time\nfrom pathlib import Path\nsys.path.insert(0," + repr(str(runner.parent)) + ")\nfrom bounded import worker_boot\nworker_boot()\ntime.sleep(10)\n", encoding="utf-8")
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"output": str(output), "budget_seconds": .8}))
    (output / "prelaunch_seal.json").write_text(json.dumps({"historical": {}, "files": {}}))
    result = subprocess.run([sys.executable, "-B", str(runner), "--config", str(config), "--worker", str(fake)],
                            capture_output=True, text=True, timeout=8)
    supervision = json.loads((output / "supervision.json").read_text())
    assert result.returncode == 1 and supervision["status"] == "INVALID"
    assert "TimeoutError" in supervision["reason"]
    assert supervision["wall_seconds"] < 3
    assert json.loads((output / "boot.json").read_text())["pid"] == supervision["worker_pid"]
