"""Bounded plan/gate checks; no scientific training or geometry generation."""

import copy
import json
from types import SimpleNamespace

import numpy as np
import pytest

from larp import config, runner
from larp.artifacts import file_hash
from larp.baselines import choose_baseline
from larp.training import datasets_for
from larp.geometry import Geometry


def screen_records():
    conditions = ("grid_balanced", "hu", "small_world", "random_regular", "poisson")
    scores = (.60, .61, .72, .66, .57)
    return [
        {"experiment_id": f"synthetic-screen-{condition}-{seed}", "stage": "screen",
         "task": "copy", "condition": condition, "variant": "T", "regime": "causal",
         "geometry_seed": 1101, "training_seed": seed, "score_split": "validation",
         "status": "COMPLETE", "score": score + offset, "updates_completed": 500,
         "updates_budget": 500, "active_edges": 2400, "parameters": 12508}
        for condition, score in zip(conditions, scores)
        for seed, offset in ((2101, -.01), (2102, .01))
    ]


def test_strongest_baseline_uses_two_initializations_final_equal_budget_validation():
    rows = screen_records()
    # Irrelevant G control cannot replace the strongest nominal T opponent.
    rows.append({**rows[0], "variant": "G", "score": 1.0})
    result = choose_baseline(rows)
    assert result["condition"] == "small_world"
    assert result["candidates"]["small_world"]["score"] == pytest.approx(.72)
    assert len(result["candidates"]) == 5


@pytest.mark.parametrize("field,value", [
    ("status", "RESOURCE_LIMIT"), ("score_split", "test"), ("updates_completed", 1000),
    ("training_seed", 2101), ("geometry_seed", 1102), ("task", "fill"), ("stage", "confirmation"),
])
def test_baseline_selection_rejects_incomplete_unpaired_or_wrong_stage_screen(field, value):
    rows = screen_records()
    rows[1][field] = value
    with pytest.raises(ValueError):
        choose_baseline(rows)


def test_baseline_selection_rejects_missing_rival_and_resolves_preregistered_ties():
    rows = screen_records()
    with pytest.raises(ValueError):
        choose_baseline(rows[:-1])
    for row in rows:
        row["score"] = .70
    assert choose_baseline(rows)["condition"] == "grid_balanced"
    for row in rows:
        if row["condition"] == "hu":
            row["active_edges"] = 2000
    assert choose_baseline(rows)["condition"] == "hu"


def test_presets_immutable_and_contract_hash_checked(tmp_path, monkeypatch):
    profiles = tmp_path / "configs"
    profiles.mkdir()
    preset = profiles / "pilot_focal.json"
    preset.write_text(json.dumps({"updates": 1000}), encoding="utf-8")
    contract_path = profiles / "scientific_contract.json"
    contract_path.write_text(json.dumps({"larp_v0_1_decisions": {"N_train": 400}}), encoding="utf-8")
    index = {path.name: file_hash(path) for path in (preset, contract_path)}
    (profiles / "preset_hashes.json").write_text(json.dumps(index), encoding="utf-8")
    monkeypatch.setattr(config, "ROOT", tmp_path)
    loaded = config.load_profile("pilot_focal")
    loaded["updates"] = 3
    assert config.load_profile("pilot_focal")["updates"] == 1000
    preset.write_text(json.dumps({"updates": 500}), encoding="utf-8")
    with pytest.raises(ValueError, match="Immutable"):
        config.load_profile("pilot_focal")
    assert config.contract()["N_train"] == 400
    contract_path.write_text(json.dumps({"larp_v0_1_decisions": {"N_train": 100}}), encoding="utf-8")
    with pytest.raises(ValueError, match="Immutable"):
        config.contract()


def test_pilot_screen_same_data_confirmation_independent_without_heavy_generation():
    base = {"task": "copy", "train_size": 12, "validation_size": 6, "test_size": 9,
            "world_side": 5, "L": 10}
    pilot = datasets_for({**base, "stage": "pilot"}, include_test=True)
    screen = datasets_for({**base, "stage": "screen"}, include_test=True)
    confirmation = datasets_for({**base, "stage": "confirmation"}, include_test=True)
    assert {split: dataset.digest for split, dataset in pilot.items()} == {
        split: dataset.digest for split, dataset in screen.items()}
    assert all(pilot[split].digest != confirmation[split].digest for split in pilot)
    assert len({dataset.digest for dataset in pilot.values()}) == 3


def test_accessibility_follows_source_to_destination_direction_and_copy_selected_source():
    geometry = SimpleNamespace(N=4)
    edges = np.array([[0, 1, 2], [1, 2, 3]], dtype=np.int64)
    ports = SimpleNamespace(indices=np.arange(4))
    arrays = {"source_sites": np.array([[0, 2], [3, 1], [3, 0]]),
              "destination": np.array([3, 0, 2]), "query": np.array([0, 0, 1])}
    class Dataset:
        task = "copy"
        def __init__(self):
            self.arrays = arrays
        def __len__(self):
            return 3
    dataset = Dataset()
    accessible, description = runner.accessibility(dataset, geometry, edges, ports, 3)
    np.testing.assert_array_equal(accessible, [True, False, True])
    assert description["fraction"] == pytest.approx(2 / 3)
    dataset.task = "xor"
    accessible, _ = runner.accessibility(dataset, geometry, edges, ports, 3)
    np.testing.assert_array_equal(accessible, [True, False, False])


def test_frozen_plan_idempotent_rejects_changes_and_payload_tampering(tmp_path, monkeypatch):
    identity = {"source_hash": "unchanged_test_source", "commit": "synthetic"}
    monkeypatch.setattr(runner, "code_identity", lambda _: identity)
    path = tmp_path / "preregistration.json"
    plan = {"configs": [{"updates": 1000}], "results": None}
    frozen = runner.freeze_plan(path, plan)
    before = path.read_bytes()
    assert runner.freeze_plan(path, copy.deepcopy(plan)) == frozen
    assert path.read_bytes() == before
    with pytest.raises(RuntimeError, match="Frozen"):
        runner.freeze_plan(path, {"configs": [{"updates": 500}]})
    tampered = json.loads(path.read_text(encoding="utf-8"))
    tampered["plan"]["configs"][0]["updates"] = 999
    path.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(RuntimeError, match="Frozen|corrupt|hash|tamper"):
        runner.freeze_plan(path, plan)


def test_gates_missing_failed_and_stale_never_authorize_execution(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "GATES", tmp_path / "gates")
    monkeypatch.setattr(runner, "code_identity", lambda _: {"source_hash": "current"})
    with pytest.raises(RuntimeError, match="GATE_NOT_RUN"):
        runner.require_gates("scientific_tests")
    runner.record_gate("scientific_tests", False)
    with pytest.raises(RuntimeError, match="GATE_FAILED"):
        runner.require_gates("scientific_tests")
    gate = runner.record_gate("scientific_tests", True)
    runner.require_gates("scientific_tests")
    gate["code"]["source_hash"] = "old"
    runner.gate_path("scientific_tests").write_text(json.dumps(gate), encoding="utf-8")
    with pytest.raises(RuntimeError, match="STALE_GATE"):
        runner.require_gates("scientific_tests")


def test_stage_plans_have_exact_budgets_seed_counts_and_hpo_closed_test(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "GATES", tmp_path / "no_gates")
    pilot = runner.plan_stage("pilot", "copy")
    assert pilot["count"] == 12
    assert {cfg["updates"] for cfg in pilot["configs"]} == {1000}
    screen = runner.plan_stage("screen", "copy")
    assert screen["count"] == 14 and screen["open_test"] is False
    assert {cfg["updates"] for cfg in screen["configs"]} == {500}
    confirmation = runner.confirmation_plan("copy", "grid_balanced")
    assert confirmation["count"] == 48
    assert len(confirmation["expected_geometry_seeds"]) == 8
    assert {cfg["updates"] for cfg in confirmation["configs"]} == {3000}
    hpo = runner.confirmation_plan("copy", "grid_balanced", hpo=True)
    assert hpo["count"] == 18 and hpo["open_test"] is False
    assert {cfg["stage"] for cfg in hpo["configs"]} == {"calibration"}
    assert {cfg["updates"] for cfg in hpo["configs"]} == {300}
    assert len({cfg["geometry_seed"] for cfg in hpo["configs"]}) == 1
    assert len({cfg["training_seed"] for cfg in hpo["configs"]}) == 2


def _mock_preflight(monkeypatch, mismatch=None):
    import larp.model as model_module
    monkeypatch.setattr(model_module, "LARPModel", lambda *args: SimpleNamespace())
    monkeypatch.setattr(runner, "model_hash", lambda _: "same_initial_weights")
    monkeypatch.setattr(runner, "register_ports", lambda *args: SimpleNamespace(digest="same_ports"))
    monkeypatch.setattr(runner, "data_hashes", lambda cfg: {"data_train": str(cfg["train_size"]),
                                                          "data_validation": str(cfg["validation_size"]),
                                                          "data_test": str(cfg["test_size"])})
    def substrate(condition, N, seed, **kwargs):
        points = np.stack((np.arange(5), np.arange(5)), axis=1).astype(float)
        labels = np.arange(5) if condition == "native" else np.roll(np.arange(5), 1)
        edges = np.array([[0, 1, 2, 3], [1, 2, 3, 4]], dtype=np.int64)
        if condition == "shuffle":
            if mismatch == "coordinates":
                points[0, 0] += .01
            elif mismatch == "edges":
                edges[0, 0] = 4
            elif mismatch == "labels":
                labels = np.arange(5)
        return Geometry(points, labels, 20, {"test_only": True}), edges
    monkeypatch.setattr(runner, "make_substrate", substrate)
    return [{"stage": "pilot", "task": "copy", "variant": "T", "condition": condition,
             "geometry_seed": 1101, "training_seed": 2101, "lr": .003, "updates": 1000,
             "regime": "causal", "N": 400, "world_side": 10, "steps": 16, "batch_size": 4,
             "train_size": 8192, "validation_size": 1024, "test_size": 4096}
            for condition in ("native", "shuffle")]


@pytest.mark.parametrize("mismatch", ["coordinates", "edges", "labels", "budget", "data"])
def test_pairing_preflight_rejects_factor_changes_before_training(mismatch, monkeypatch):
    configs = _mock_preflight(monkeypatch, mismatch)
    if mismatch == "budget":
        configs[1]["batch_size"] = 8
    elif mismatch == "data":
        configs[1]["train_size"] = 12
    with pytest.raises(RuntimeError, match="pairing"):
        runner.pairing_preflight(configs)


def test_pairing_preflight_accepts_only_marks_changed_and_rejects_unpaired_or_duplicate(monkeypatch):
    configs = _mock_preflight(monkeypatch)
    result = runner.pairing_preflight(configs)
    assert len(result) == 1
    assert result[0]["labels"][0] != result[0]["labels"][1]
    with pytest.raises(ValueError, match="native pair"):
        runner.pairing_preflight(configs[1:])
    with pytest.raises(ValueError, match="uplicate"):
        runner.pairing_preflight(configs + configs[1:])


def test_execution_aborts_on_preflight_mismatch_before_any_model_training(tmp_path, monkeypatch):
    configs = _mock_preflight(monkeypatch, "coordinates")
    monkeypatch.setattr(runner, "code_identity", lambda _: {"source_hash": "stable_fixture"})
    def forbidden(*args, **kwargs):
        pytest.fail("A test endpoint/training call reached before causal preflight passed")
    monkeypatch.setattr(runner, "train_run", forbidden)
    with pytest.raises(RuntimeError, match="pairing"):
        runner.execute_configs(configs, tmp_path / "pair", open_test=True)
    assert not list((tmp_path / "pair").rglob("test_world.npz"))


def test_confirmation_task_mismatch_fails_before_execute(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "require_gates", lambda *args: None)
    monkeypatch.setattr(runner, "code_identity", lambda _: {"source_hash": "stable_fixture"})
    def forbidden(*args, **kwargs):
        pytest.fail("Mismatched task reached execution")
    monkeypatch.setattr(runner, "execute_configs", forbidden)
    plan = runner.confirmation_plan("copy", "grid_balanced")
    runner.freeze_plan(tmp_path / "frozen_confirmation.json", plan)
    with pytest.raises(RuntimeError, match="task"):
        runner.confirm("fill", directory=tmp_path)


def test_freeze_confirmation_uses_custom_screen_gate_location_and_common_hpo_weight(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "GATES", tmp_path / "gates")
    monkeypatch.setattr(runner, "require_gates", lambda *args: None)
    monkeypatch.setattr(runner, "code_identity", lambda _: {"source_hash": "stable_fixture"})
    screen = tmp_path / "custom_screen"
    screen.mkdir()
    (screen / "baseline_selection.json").write_text(json.dumps({"condition": "small_world"}), encoding="utf-8")
    runner.GATES.mkdir()
    runner.gate_path("screen_copy").write_text(json.dumps({"results": str(screen / "results.json")}), encoding="utf-8")
    captured = []
    def fake_hpo(configs, directory, **kwargs):
        assert kwargs["open_test"] is False
        rows = []
        for index, cfg in enumerate(configs):
            captured.append(cfg)
            run = directory / f"hpo-{index}"
            run.mkdir(parents=True)
            (run / "manifest.json").write_text(json.dumps({"config": cfg}), encoding="utf-8")
            # Candidate .003 beats .001 when geometric groups, not conditions,
            # receive equal weight; .01 is deliberately poor.
            score = (1.0 if cfg["condition"] in ("native", "shuffle") else 0.0) if cfg["lr"] == .001 else (
                .60 if cfg["lr"] == .003 else .10)
            rows.append({"experiment_id": run.name, "code": {"source_hash": "stable_fixture"},
                         "condition": cfg["condition"], "score": score, "status": "COMPLETE"})
        return rows
    monkeypatch.setattr(runner, "execute_configs", fake_hpo)
    frozen = runner.freeze_confirmation("copy", directory=tmp_path / "confirm")
    assert {cfg["condition"] for cfg in captured} == {"native", "shuffle", "small_world"}
    assert frozen["plan"]["lr"] == .003
    assert frozen["plan"]["conditions"][-1] == "small_world"
