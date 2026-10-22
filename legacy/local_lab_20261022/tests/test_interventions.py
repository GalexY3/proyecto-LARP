"""Tiny synthetic frozen bundles exercise orchestration, never MHU evidence."""
import json

import numpy as np
import pytest

import larp.interventions as interventions
import larp.training as training
from larp.geometry import Geometry
from larp.graphs import knn_graph


LIMITS = {"examples": 4, "random_masks": 1, "lesion_centers": 1,
          "steps": 2, "function_permutations": 2}


@pytest.fixture
def frozen_bundle(tmp_path, monkeypatch):
    identity = lambda _: {"source_hash": "synthetic_technical_fixture", "commit": "test_only"}
    monkeypatch.setattr(training, "code_identity", identity)
    monkeypatch.setattr(interventions, "code_identity", identity)
    a, b = np.meshgrid(np.arange(10), np.arange(10), indexing="ij")
    points = np.stack((a.ravel()+0.5, b.ravel()+0.5), axis=-1)
    geometry = Geometry(points, np.arange(100) % 5, 10,
                        {"kind": "grid", "geometry_seed": 123, "test_only": True})
    edges = knn_graph(points, 10)
    cfg = {"task": "copy", "stage": "pilot", "variant": "T", "condition": "grid",
           "geometry_seed": 123, "training_seed": 2101, "lr": 0.003,
           "updates": 1, "batch_size": 4, "steps": 2, "train_size": 12,
           "validation_size": 6, "test_size": 12, "world_side": 5, "L": 10,
           "regime": "causal", "technical_test_only": True}
    run_dir = tmp_path / "synthetic_run"
    result = training.train_run(cfg, geometry, edges, run_dir, preregistered=True,
                                open_test=True, validation_interval=1)
    assert result["status"] == "COMPLETE" and result["test_opened"]
    geometry.save(run_dir / "geometry.npz")
    np.save(run_dir / "edges.npy", edges)
    return run_dir


def test_dry_run_default_literal_and_closed_run_gate(frozen_bundle, tmp_path):
    output = tmp_path / "dry"
    result = interventions.run_robustness(frozen_bundle, output, kind="random",
                                         test_only=True, test_limits=LIMITS)
    assert result["status"] == "NOT_RUN" and result["conditions"] == 8
    assert result["scientific_evidence"] is False
    assert not (output / "records").exists()
    plan = json.loads((output / "preregistration.json").read_text(encoding="utf8"))["plan"]
    assert plan["priors_updated"] is False
    assert plan["profile"]["node_fractions"] == [0, 0.05, 0.1, 0.2]
    results_file = frozen_bundle / "results.json"
    saved = json.loads(results_file.read_text(encoding="utf8"))
    saved["status"] = "RESOURCE_LIMIT"
    results_file.write_text(json.dumps(saved), encoding="utf8")
    with pytest.raises(RuntimeError, match="COMPLETE"):
        interventions.run_robustness(frozen_bundle, tmp_path / "refused", test_only=True, test_limits=LIMITS)


def test_random_pipeline_protects_actual_ports_coverage_and_resume(frozen_bundle, tmp_path):
    output = tmp_path / "random"
    result = interventions.run_robustness(frozen_bundle, output, kind="random", dry_run=False,
                                         test_only=True, test_limits=LIMITS)
    assert result["status"] == "COMPLETE" and len(result["records"]) == 8
    assert set(result["AUC"]) == {"protected", "end_to_end"}
    for record in result["records"]:
        assert record["scientific_evidence"] is False and record["weights_frozen"]
        assert set(record["diagnostics"]["hop_coverage"]) == {"4", "8"}
        assert set(record["diagnostics"]["spatial_coverage_R4_R5"]) == {"4", "5"}
        if record["condition"]["protect_ports"]:
            assert record["metrics"]["processing_example_count"] == 4
    resumed = interventions.run_robustness(frozen_bundle, output, kind="random", dry_run=False,
                                          test_only=True, test_limits=LIMITS)
    assert resumed["records"] == result["records"]
    end_to_end = interventions.run_robustness(frozen_bundle, tmp_path / "unprotected", kind="random",
                   dry_run=False, protect_ports=False, test_only=True, test_limits=LIMITS)
    assert len(end_to_end["records"]) == 4
    assert set(end_to_end["AUC"]) == {"end_to_end"}


def test_full_function_collapse_relocation_and_rename_control(frozen_bundle, tmp_path):
    collapse = interventions.run_robustness(frozen_bundle, tmp_path / "m1", kind="m1", dry_run=False,
                                           test_only=True, test_limits=LIMITS)
    assert [r["condition"]["collapse_lambda"] for r in collapse["records"]] == [0, 0.5, 1]
    moved = interventions.run_robustness(frozen_bundle, tmp_path / "functions", kind="functions", dry_run=False,
                                        test_only=True, test_limits=LIMITS)
    assert len(moved["records"]) == 4
    native, renamed = moved["records"][:2]
    assert native["metrics"]["score"] == renamed["metrics"]["score"]
    assert native["metrics"]["loss"] == renamed["metrics"]["loss"]
    for path in (tmp_path / "functions" / "masks").glob("*.npz"):
        with np.load(path) as archive:
            assert np.bincount(archive["function_labels"], minlength=5).tolist() == [20]*5


def test_scale_dry_plan_and_small_extra_step_curve_no_fitting(frozen_bundle, tmp_path):
    plan = interventions.run_scale(frozen_bundle, tmp_path / "scale", test_only=True, test_limits=LIMITS)
    assert plan["status"] == "NOT_RUN" and plan["conditions"] == 4
    assert "MISSING" in plan["scale_gate"]
    result = interventions.run_scale(frozen_bundle, tmp_path / "scale", dry_run=False,
                                     test_only=True, test_limits=LIMITS)
    assert [r["steps"] for r in result["records"]] == [8, 16, 32, 64]
    assert all(not r["fine_tuning"] and not r["scientific_evidence"] for r in result["records"])
