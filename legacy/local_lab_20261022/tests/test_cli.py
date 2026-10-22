"""CLI dry-run/analysis gates, using mocked execution and tiny metadata."""

import json
import subprocess
import sys

import pytest

from larp import cli, runner


def test_python_module_propagates_a_caught_blocker_exit_status(tmp_path):
    result = subprocess.run([sys.executable,"-m","larp","resume","--run",str(tmp_path / "absent_run")],
                            capture_output=True,text=True)
    assert result.returncode == 2
    assert "BLOCKED:" in result.stderr


@pytest.mark.parametrize("arguments", [
    ["calibrate"], ["smoke"], ["pilot"], ["fill"], ["screen"],
    ["screen", "--task", "fill", "--ecological"],
    ["freeze-confirmation", "--task", "copy"], ["confirm", "--task", "copy"],
    ["verify-failure", "--run", "unused_fixture_path"],
])
def test_default_planning_never_generates_geometry_trains_or_opens_test(arguments, monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        pytest.fail("A dry-run attempted execution")
    monkeypatch.setattr(runner, "GATES", tmp_path / "no_gates")
    for name in ("calibration", "smoke", "execute_stage", "freeze_confirmation", "confirm",
                 "execute_configs", "train_run", "make_substrate", "require_gates"):
        monkeypatch.setattr(runner, name, forbidden)
    monkeypatch.setattr(cli, "verify_failure", forbidden)
    result = cli.dispatch(cli.parser().parse_args(arguments))
    assert isinstance(result, dict)
    assert not list(tmp_path.rglob("results.json"))


@pytest.mark.parametrize("stage", ["pilot", "smoke", "calibration", "integration", "screen"])
def test_cli_selected_pilot_or_technical_records_are_descriptive_without_posterior(stage, monkeypatch, tmp_path):
    import larp.analysis as analysis
    def forbidden(*args, **kwargs):
        pytest.fail("Selected/technical evidence reached confirmatory inference")
    monkeypatch.setattr(analysis, "analyze_records", forbidden)
    records, output = tmp_path / "records.json", tmp_path / "analysis.json"
    records.write_text(json.dumps([{"stage": stage}]), encoding="utf-8")
    args = cli.parser().parse_args(["analyze", "--records", str(records), "--output", str(output)])
    result = cli.dispatch(args)
    assert result["status"] == "DESCRIPTIVE_ONLY"
    assert result["architecture_beliefs_updated"] is False
    assert result["priors"]["status"] == "UNUPDATED"
    assert json.loads(output.read_text(encoding="utf-8")) == result


def test_analyze_without_evidence_only_writes_initial_priors(tmp_path):
    output = tmp_path / "initial_priors.json"
    result = cli.dispatch(cli.parser().parse_args(["analyze", "--output", str(output)]))
    assert result["status"] == "UNUPDATED"
    assert result["architecture_evidence"] == []
    assert all(row["prior"] == row["posterior"] for row in result["hypotheses"].values())


def test_explicit_execute_requires_valid_gates_before_any_training(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(runner, "GATES", tmp_path / "missing_gates")
    def forbidden(*args, **kwargs):
        pytest.fail("Training reached before gates")
    monkeypatch.setattr(runner, "execute_configs", forbidden)
    code = cli.main(["pilot", "--execute", "--directory", str(tmp_path / "not_created")])
    assert code == 2
    assert "GATE_NOT_RUN" in capsys.readouterr().err
    assert not (tmp_path / "not_created").exists()


def test_invalid_confirmatory_metadata_returns_blocked_without_analysis_artifact(tmp_path, capsys):
    records, output = tmp_path / "records.json", tmp_path / "analysis.json"
    records.write_text(json.dumps([{"stage": "confirmation", "condition": "native", "preregistered": False}]), encoding="utf-8")
    assert cli.main(["analyze", "--records", str(records), "--output", str(output)]) == 2
    assert "preregistration" in capsys.readouterr().err
    assert not output.exists()


@pytest.mark.parametrize("control,estimand", [("shuffle", "marks"), ("grid_balanced", "architecture")])
def test_cli_analyze_selects_only_the_explicit_contrast_from_confirmation_suite(control, estimand, tmp_path, monkeypatch):
    import larp.analysis as analysis
    captured = {}
    def capture(records, **kwargs):
        captured["records"] = records
        captured["kwargs"] = kwargs
        return {"architecture_beliefs_updated": False, "synthetic_routing_test": True}
    monkeypatch.setattr(analysis, "analyze_records", capture)
    records = [{"stage": "confirmation", "condition": condition, "preregistered": True,
                "experiment_id": f"fixture-{condition}"}
               for condition in ("native", "shuffle", "grid_balanced")]
    path, output = tmp_path / "confirmation_results.json", tmp_path / "analysis.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    cli.dispatch(cli.parser().parse_args(["analyze", "--records", str(path), "--control", control,
                                         "--estimand", estimand, "--output", str(output)]))
    assert {row["condition"] for row in captured["records"]} == {"native", control}
    assert captured["kwargs"]["control_condition"] == control
    assert captured["kwargs"]["estimand"] == estimand
