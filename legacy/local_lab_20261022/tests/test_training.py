"""Bounded technical training/resume checks. These scores are not evidence."""
import json

import numpy as np
import pytest
import torch

import larp.training as training
from larp.data import register_ports
from larp.geometry import Geometry
from larp.graphs import knn_graph


def mini_geometry():
    a, b = np.meshgrid(np.arange(10), np.arange(10), indexing="ij")
    points = np.stack((a.ravel() + 0.5, b.ravel() + 0.5), axis=-1)
    return Geometry(points, np.arange(100) % 5, 10,
                    {"test_only": True, "geometry_seed": 123})


def mini_config(task="copy", stage="integration", updates=8):
    return {"task": task, "stage": stage, "variant": "T", "condition": "test_only",
            "geometry_seed": 123, "training_seed": 2101, "lr": 0.003,
            "updates": updates, "batch_size": 4, "steps": 2,
            "train_size": 30, "validation_size": 10, "test_size": 10,
            "world_side": 5, "L": 10}


@pytest.fixture
def stable_technical_identity(monkeypatch):
    # The team can edit unrelated sources concurrently. This isolates exact
    # resume mechanics; a separate test below checks the source mismatch gate.
    monkeypatch.setattr(training, "code_identity", lambda _: {
        "source_hash": "technical_fixture_source_hash", "commit": "test_only", "dirty": True})


def test_pause_resume_exact_weights_optimizer_order_counters_and_validation(tmp_path, stable_technical_identity):
    geometry = mini_geometry()
    edges = knn_graph(geometry.points, geometry.L)
    cfg = mini_config()
    complete_dir, resumed_dir = tmp_path / "continuous", tmp_path / "resumed"
    full = training.train_run(cfg, geometry, edges, complete_dir, validation_interval=4)
    partial = training.train_run(cfg, geometry, edges, resumed_dir,
                                 validation_interval=4, stop_after_update=4)
    assert partial["status"] == "PAUSED_AT_UPDATE_BOUNDARY"
    assert partial["updates_completed"] == 4 and partial["samples_seen"] == 16
    resumed = training.train_run(cfg, geometry, edges, resumed_dir,
                                 validation_interval=4, resume=True)
    assert full["status"] == resumed["status"] == "COMPLETE"
    assert full["updates_completed"] == resumed["updates_completed"] == 8
    # Last minibatch is two examples, not four: the first epoch has 30 samples.
    assert full["samples_seen"] == resumed["samples_seen"] == 30
    assert full["validation"]["score"] == resumed["validation"]["score"]
    assert full["validation"]["loss"] == resumed["validation"]["loss"]
    assert full["final_optimization_loss"] == resumed["final_optimization_loss"]
    full_model, _, _ = training.load_trained_run(complete_dir)
    resumed_model, _, _ = training.load_trained_run(resumed_dir)
    assert training.model_hash(full_model) == training.model_hash(resumed_model)
    left = torch.load(complete_dir / "checkpoints" / "last.pt", weights_only=False)
    right = torch.load(resumed_dir / "checkpoints" / "last.pt", weights_only=False)
    assert np.array_equal(left["order"], right["order"])
    assert left["cursor"] == right["cursor"] == 30
    assert left["rng"] == right["rng"]
    assert left["history"] == right["history"]
    for parameter_id, state in left["optimizer"]["state"].items():
        for key, value in state.items():
            assert torch.equal(value, right["optimizer"]["state"][parameter_id][key])
    # Reopening a completed closed-test run performs no new update, and must
    # retain the loss of the final completed optimizer step.
    unchanged = training.train_run(cfg, geometry, edges, complete_dir,
                                   validation_interval=4, resume=True)
    assert unchanged["final_optimization_loss"] == full["final_optimization_loss"]
    assert unchanged["samples_seen"] == 30


def test_resume_refuses_source_change(tmp_path, stable_technical_identity, monkeypatch):
    geometry = mini_geometry()
    edges = knn_graph(geometry.points, geometry.L)
    cfg = mini_config(updates=2)
    run_dir = tmp_path / "run"
    training.train_run(cfg, geometry, edges, run_dir, stop_after_update=1)
    monkeypatch.setattr(training, "code_identity", lambda _: {"source_hash": "changed"})
    with pytest.raises(ValueError, match="Existing run differs"):
        training.train_run(cfg, geometry, edges, run_dir, resume=True)


@pytest.mark.parametrize("stage,preregistered", [("integration", False), ("smoke", True), ("pilot", False)])
def test_test_open_guard_before_training(tmp_path, stage, preregistered):
    geometry = mini_geometry()
    edges = knn_graph(geometry.points, geometry.L)
    with pytest.raises(ValueError, match="Test opens only"):
        training.train_run(mini_config(stage=stage, updates=1), geometry, edges,
                           tmp_path / "forbidden", open_test=True, preregistered=preregistered)
    assert not (tmp_path / "forbidden").exists()


def test_test_remains_closed_after_final_validation_diverges(tmp_path, stable_technical_identity, monkeypatch):
    geometry = mini_geometry()
    edges = knn_graph(geometry.points, geometry.L)
    calls = []

    def fake_evaluate(model, dataset, *args, **kwargs):
        calls.append(dataset.split)
        # During update1 periodic validation finite, final validation divergent.
        return ({"score": 0.5, "loss": 1.0} if len(calls) == 1 else
                {"score": 0.0, "loss": float("inf"), "divergent": True})

    monkeypatch.setattr(training, "evaluate", fake_evaluate)
    result = training.train_run(mini_config(stage="pilot", updates=1), geometry, edges,
                                tmp_path / "failed", validation_interval=1,
                                open_test=True, preregistered=True)
    assert result["status"] == "NUMERICAL_FAILURE_UNVERIFIED"
    assert not result["test_opened"]
    assert calls == ["validation", "validation"]
    assert not (tmp_path / "failed" / "test_world.npz").exists()


def test_resource_uses_frozen_float64_train_variance(tmp_path, stable_technical_identity, monkeypatch):
    geometry = mini_geometry()
    edges = knn_graph(geometry.points, geometry.L)
    cfg = mini_config(task="resource", updates=1)
    expected = training.datasets_for(cfg)["train"].train_target_variance
    passed_variances = []
    original = training.evaluate

    def captured_evaluate(*args, **kwargs):
        passed_variances.append(kwargs["train_target_variance"])
        return original(*args, **kwargs)

    monkeypatch.setattr(training, "evaluate", captured_evaluate)
    training.train_run(cfg, geometry, edges, tmp_path / "resource", validation_interval=1)
    assert passed_variances and all(value == expected for value in passed_variances)
    manifest = json.loads((tmp_path / "resource" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["train_target_variance_frozen"] == expected


def test_evaluate_alive_selection_alignment_and_essential_input_condition():
    geometry = mini_geometry()
    dataset = training.datasets_for(mini_config())["validation"]
    ports = register_ports(geometry.points, 10, 5)
    edges = knn_graph(geometry.points, 10)
    tensors = training.graph_tensors(geometry, edges, "cpu")
    model = training.LARPModel("T", 8)
    indexes = np.array([7, 1, 9])
    batch = dataset.batch(indexes, geometry.points, ports)
    alive = np.ones((3, 100), dtype=bool)
    alive[0, int(batch["selected_source_nodes"][0])] = False
    alive[1, int(batch["output_nodes"][1, 0])] = False
    result = training.evaluate(model, dataset, geometry, ports, tensors, indexes=indexes,
                               alive=alive, batch_size=2, steps=2)
    assert result["processing_example_count"] == 1
    assert result["system_score_per_example"][:2] == [0, 0]
    assert result["system_failure_fraction"] == pytest.approx(2/3)
    with pytest.raises(ValueError, match="aligned with indexes"):
        training.evaluate(model, dataset, geometry, ports, tensors, indexes=indexes,
                           alive=np.ones((len(dataset), 100), bool), steps=2)
