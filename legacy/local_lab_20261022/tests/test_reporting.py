"""Reporter verification uses explicitly synthetic temporary fixtures."""

import csv
import json
from pathlib import Path

from larp.analysis import H_MARGINAL_PRIORS
from larp.reporting import summarize


def test_empty_report_has_no_invented_results_and_preserves_ab_history(tmp_path):
    summary = summarize(tmp_path / "no_runs", tmp_path / "report")
    assert summary["result_records_loaded"] == 0
    assert summary["figures"] == []
    assert summary["architecture_beliefs_updated_by_reporting"] is False
    history = tmp_path / "report" / "AB_history.json"
    before = history.read_bytes()
    beliefs = json.loads(before)
    assert beliefs["status"] == "UNUPDATED"
    assert all(beliefs["hypotheses"][name]["posterior"] == prior for name, prior in H_MARGINAL_PRIORS.items())
    summarize(tmp_path / "no_runs", tmp_path / "report")
    assert history.read_bytes() == before


def test_csv_and_png_use_logged_records_keep_failures_and_nonfinite_values(tmp_path):
    run = tmp_path / "runs" / "synthetic_reporter_fixture"
    run.mkdir(parents=True)
    result = {
        "experiment_id": "synthetic_reporter_fixture", "stage": "integration",
        "task": "copy", "variant": "T", "condition": "native",
        "geometry_seed": 101, "training_seed": 201,
        "status": "NUMERICAL_FAILURE_UNVERIFIED", "score_split": "validation",
        "score": 0.0, "loss": {"nonfinite": "+inf"}, "updates_completed": 20,
        "updates_budget": 30, "samples_seen": 80, "test_opened": False,
        "preregistered": False, "validation": {"score": 0.0, "loss": {"nonfinite": "+inf"}},
    }
    (run / "results.json").write_text(json.dumps(result), encoding="utf-8")
    events = [
        {"update": 10, "optimization_loss": 0.72, "validation_score": .49, "validation_loss": .70},
        {"update": 20, "optimization_loss": {"nonfinite": "nan"}, "validation_score": .50, "validation_loss": .69},
    ]
    (run / "curve.jsonl").write_text("\n".join(json.dumps(event) for event in events) + "\ninvalid-json", encoding="utf-8")
    output = tmp_path / "report"
    summary = summarize(tmp_path / "runs", output)
    assert summary["result_records_loaded"] == 1
    assert summary["status_counts"] == {"NUMERICAL_FAILURE_UNVERIFIED": 1}
    assert summary["curve_events_loaded"] == 2
    assert summary["warnings"][0]["status"] == "INVALID_CURVE_EVENT"
    assert summary["architecture_beliefs_updated_by_reporting"] is False
    assert len(summary["figures"]) == 2
    assert all(figure["inference"] == "none" for figure in summary["figures"])
    assert all(Path(figure["path"]).exists() for figure in summary["figures"])
    with (output / "results.csv").open(encoding="utf-8", newline="") as stream:
        row = next(csv.DictReader(stream))
    assert row["status"] == result["status"]
    assert row["score"] == "0.0"
    assert row["loss"] == "+inf"
    assert row["test_score"] == ""
    assert row["source_sha256"]


def test_corrupt_result_is_reported_as_invalid_and_never_counted_as_pass(tmp_path):
    run = tmp_path / "runs" / "broken"
    run.mkdir(parents=True)
    (run / "results.json").write_text("not-json", encoding="utf-8")
    summary = summarize(tmp_path / "runs", tmp_path / "report")
    assert summary["result_files_found"] == 1
    assert summary["result_records_loaded"] == 0
    assert summary["status_counts"] == {}
    assert summary["warnings"][0]["status"] == "INVALID_RECORD"
    assert summary["figures"] == []


def test_suite_aggregate_is_provenance_index_and_cannot_duplicate_run_counts(tmp_path, monkeypatch):
    monkeypatch.setattr("larp.reporting._figures", lambda *args: [])
    runroot = tmp_path / "runs"
    run = runroot / "synthetic_fixture"
    run.mkdir(parents=True)
    record = {"experiment_id": "synthetic_fixture", "stage": "integration",
              "status": "COMPLETE", "score": .5, "score_split": "validation"}
    (run / "results.json").write_text(json.dumps(record), encoding="utf-8")
    (runroot / "results.json").write_text(json.dumps([record]), encoding="utf-8")
    summary = summarize(runroot, tmp_path / "report")
    assert summary["result_files_found"] == 2
    assert summary["result_records_loaded"] == 1
    assert summary["status_counts"] == {"COMPLETE": 1}
    assert summary["warnings"] == []
    assert len(summary["source_results"]) == len(summary["aggregate_indexes"]) == 1
    assert summary["aggregate_indexes"][0]["role"] == "suite_index_only"
    assert summary["aggregate_indexes"][0]["entries"] == 1
