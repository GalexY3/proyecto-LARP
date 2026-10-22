import json
from pathlib import Path
import subprocess

import pytest

from larp import scale3d_runner_v2 as runner


def test_v2_native_worker_and_guardian_are_isolated(tmp_path, monkeypatch):
    command = runner.worker_command(tmp_path / "config.json", tmp_path / "run",
                                    base_python=tmp_path / "native-python.exe")
    assert command[1:4] == ["-B", "-m", "larp.scale3d_train_v2"]
    assert command[-1] == "--execute"
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"version": "scale3d_v2", "maximum_job_seconds": 600}),
                      encoding="utf-8")
    seen = {}

    def fake_popen(argv, **kwargs):
        seen.update(argv=argv, **kwargs)
        return type("Process", (), {"pid": 4567})()

    monkeypatch.setattr(runner.subprocess, "Popen", fake_popen)
    output = tmp_path / "new-run"
    receipt = runner.launch(config, output, venv_python=tmp_path / "selected-python.exe")
    assert "larp.scale3d_runner_v2" in seen["argv"]
    assert seen["stdin"] == subprocess.DEVNULL
    assert seen["env"]["__PYVENV_LAUNCHER__"] == str((tmp_path / "selected-python.exe").resolve())
    assert receipt["guardian_pid"] == 4567
    assert receipt["maximum_job_seconds"] == 600
    with pytest.raises(FileExistsError):
        runner.launch(config, output)


@pytest.mark.parametrize("version", [None, "scale3d_v1", "scale3d_v3"])
def test_runner_rejects_other_versions_before_creating_a_run(tmp_path, version, monkeypatch):
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"version": version, "maximum_job_seconds": 600}),
                      encoding="utf-8")
    output = tmp_path / "untouched"
    monkeypatch.setattr(runner.subprocess, "Popen", lambda *a, **k: pytest.fail("must not spawn"))
    with pytest.raises(ValueError, match="scale3d_v2"):
        runner.launch(config, output)
    assert not output.exists()


def test_v2_reuses_the_exact_frozen_network_tasks_and_evaluator():
    from larp import scale3d_train as old, scale3d_train_v2 as new
    for name in ("SpatialNetwork", "evaluate", "features_at", "graph_data", "observations",
                 "targets", "task_modes", "world"):
        assert getattr(new, name) is getattr(old, name)
    assert new.generate.__module__ == "larp.scale3d_geometry_v2"
    assert new.write_report.__module__ == "larp.scale3d_report_v2"


def test_trainer_rejects_v1_before_cuda_or_output_creation(tmp_path):
    from larp import scale3d_train_v2 as trainer
    config = tmp_path / "config.json"
    config.write_text('{"version": "scale3d_v1"}', encoding="utf-8")
    output = tmp_path / "untouched"
    with pytest.raises(ValueError, match="scale3d_v2"):
        trainer.run(config, output)
    assert not output.exists()


def test_provenance_covers_old_dependencies_and_all_new_modules(tmp_path, monkeypatch):
    from larp import scale3d_train_v2 as trainer
    monkeypatch.setattr(trainer, "ROOT", tmp_path)
    for name in trainer.REQUIRED_SOURCE_PATHS:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("fixture", encoding="utf-8")
    config = tmp_path / "configs" / "scale3d_v2.json"
    config.parent.mkdir()
    config.write_text("{}", encoding="utf-8")
    result = trainer.frozen_source_paths({}, config)
    assert set(result) == {tmp_path / p for p in trainer.REQUIRED_SOURCE_PATHS} | {config}
    omitted = list(trainer.REQUIRED_SOURCE_PATHS)[1:]
    with pytest.raises(ValueError, match="omits"):
        trainer.frozen_source_paths({"source_paths": omitted}, config)
    with pytest.raises(ValueError, match="inside"):
        trainer.frozen_source_paths({"source_paths": list(trainer.REQUIRED_SOURCE_PATHS) + ["../foreign.py"]}, config)


def test_required_mhu_gate_cannot_be_disabled():
    from larp import scale3d_train_v2 as trainer
    with pytest.raises(ValueError, match="finite MHU gate"):
        trainer.validate_config({"version": "scale3d_v2", "require_finite_MHU_pass": False})


def test_full_band_gate_cannot_be_disabled():
    from larp import scale3d_train_v2 as trainer
    with pytest.raises(ValueError, match="full exact"):
        trainer.validate_config({"version":"scale3d_v2","require_finite_MHU_pass":True,
                                 "full_band_exact_audit":False})


def test_qualification_requires_complete_panel_and_unchanged_source(tmp_path,monkeypatch):
    from larp import scale3d_train_v2 as trainer
    monkeypatch.setattr(trainer,'ROOT',tmp_path)
    folder=tmp_path/'qualification';folder.mkdir()
    source=tmp_path/'source.py';source.write_text('frozen',encoding='utf-8')
    protocol={'source_sha256':{'source.py':trainer.sha(source)}}
    (folder/'protocol.json').write_text(json.dumps(protocol),encoding='utf-8')
    records=[{'version':'v2','N':N,'seed':seed,'pass':True} for N in (16384,32768) for seed in (9107,9108)]
    result={'status':'PASS','records':records}
    path=folder/'result.json';path.write_text(json.dumps(result),encoding='utf-8')
    config={'generator_qualification':'qualification/result.json'}
    trainer.verify_generator_qualification(config)
    path.write_text(json.dumps({**result,'records':records[:-1]}),encoding='utf-8')
    with pytest.raises(ValueError,match='Complete large'):trainer.verify_generator_qualification(config)
    path.write_text(json.dumps(result),encoding='utf-8');source.write_text('changed',encoding='utf-8')
    with pytest.raises(ValueError,match='changed after'):trainer.verify_generator_qualification(config)
