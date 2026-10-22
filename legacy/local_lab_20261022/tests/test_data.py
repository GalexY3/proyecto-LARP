"""Independent external oracles, role/coordinate encoding and aggregate metrics."""
import inspect

import numpy as np
import pytest
import torch

from larp.data import (TaskDataset, assign_ports, coordinate_channels, copy_oracle,
                       evaluate_resource_fields, evaluate_task, fill_trivial_predictions,
                       flood_fill_oracle, generate_task, register_ports, resource_ports,
                       resource_sites, world_sites, xor_oracle)


def grid_points(side=20):
    a, b = np.meshgrid(np.arange(side), np.arange(side), indexing="ij")
    return np.stack((a.ravel() + 0.5, b.ravel() + 0.5), axis=-1)


def test_manual_XOR_and_copy_oracles():
    assert xor_oracle(np.array([[0, 0], [0, 1], [1, 0], [1, 1]])).tolist() == [0, 1, 1, 0]
    payload = np.arange(2 * 5 * 8).reshape(2, 5, 8)
    result = copy_oracle(payload, np.array([4, 1]))
    assert np.array_equal(result[0], payload[0, 4])
    assert np.array_equal(result[1], payload[1, 1])


def test_100_XOR_and_copy_cases_against_direct_external_labels():
    rng = np.random.default_rng(518)
    bits = rng.integers(2, size=(100, 2))
    expected_xor = np.array([(int(a) + int(b)) % 2 for a, b in bits], dtype=np.float32)
    assert np.array_equal(xor_oracle(bits), expected_xor)
    payload = rng.integers(2, size=(100, 5, 8))
    queries = rng.integers(5, size=100)
    expected_copy = np.stack([row[int(query)] for row, query in zip(payload, queries)])
    assert np.array_equal(copy_oracle(payload, queries), expected_copy)


def test_BFS_manual_torus_and_horizon():
    free = np.ones((10, 10), dtype=bool)
    target, distance = flood_fill_oracle(free, 0, 8, True)
    assert distance[9, 0] == 1 and distance[0, 9] == 1
    assert distance[5, 5] == 10 and target[5, 5] == 0
    assert target[4, 4] == 1
    free[:] = False
    free[0, 0] = free[9, 0] = True
    assert flood_fill_oracle(free, 0).sum() == 2


def test_100_BFS_cases_against_independent_iterated_cardinal_oracle():
    rng = np.random.default_rng(184)
    for _ in range(100):
        free = rng.random((10, 10)) < rng.choice([0.45, 0.55, 0.65])
        seed = int(rng.integers(100))
        free.ravel()[seed] = True
        reached = np.zeros_like(free)
        reached.ravel()[seed] = True
        for _ in range(8):
            reached |= free & (np.roll(reached, 1, 0) | np.roll(reached, -1, 0)
                               | np.roll(reached, 1, 1) | np.roll(reached, -1, 1))
        assert np.array_equal(reached, flood_fill_oracle(free, seed, 8))


def test_ports_are_injective_exact_deterministic_and_periodic():
    points = grid_points()
    first, second = register_ports(points), register_ports(points)
    assert len(np.unique(first.indices)) == 100
    assert np.array_equal(first.indices, second.indices)
    assert first.digest == second.digest
    assert first.maximum_displacement == 0
    shifted = assign_ports((points + 20) % 20, first.sites, 20)
    assert np.array_equal(shifted.indices, first.indices)
    with pytest.raises(ValueError):
        register_ports(points[:99])


@pytest.mark.parametrize("task", ["xor", "copy", "fill"])
def test_datasets_reproducible_graph_independent_splits_and_archive(task, tmp_path):
    assert not any(name in inspect.signature(generate_task).parameters for name in ("edges", "edge_index", "labels", "positions"))
    train = generate_task(task, 31, 5001)
    assert train.digest == generate_task(task, 31, 5001).digest
    val = generate_task(task, 31, 5002, split="validation")
    test = generate_task(task, 31, 5003, split="test")
    assert len({train.digest, val.digest, test.digest}) == 3
    assert not np.array_equal(train.target, val.target)
    path = tmp_path / "dataset.npz"
    train.save(path)
    restored = TaskDataset.load(path)
    assert restored.digest == train.digest
    points = grid_points()
    digest = train.digest
    batch = train.batch([0, 1], points, register_ports(points))
    assert batch["inputs"].shape == (2, 400, 25)
    assert train.digest == digest
    with pytest.raises(ValueError):
        train.arrays["target"][0] = 0


def test_copy_roles_queries_payload_and_no_remote_leakage():
    dataset = generate_task("copy", 1024, 5001)
    counts = np.bincount(dataset.arrays["query"], minlength=5)
    assert counts.max() - counts.min() <= 1
    source = world_sites()[dataset.arrays["source_sites"]]
    destination = world_sites()[dataset.arrays["destination"]]
    delta = source - destination[:, None]
    delta -= 20 * np.round(delta / 20)
    assert np.all(np.linalg.norm(delta, axis=-1) >= 5)
    assert all(len(set(row)) == 5 and dest not in row for row, dest in zip(dataset.arrays["source_sites"], dataset.arrays["destination"]))
    points = grid_points()
    ports = register_ports(points)
    batch = dataset.batch(np.arange(4), points, ports)
    inputs = batch["inputs"].numpy()
    for row in range(4):
        sources = batch["source_nodes"][row].numpy()
        output = int(batch["output_nodes"][row, 0])
        assert np.count_nonzero(inputs[row, :, 0]) == 6
        assert np.count_nonzero(inputs[row, output, 1:9]) == 0
        assert np.count_nonzero(inputs[row, output, 14:19]) == 1
        assert np.array_equal(inputs[row, sources, 1:9], dataset.arrays["payload"][row])
        non_sources = np.ones(400, dtype=bool)
        non_sources[sources] = False
        assert np.count_nonzero(inputs[row, non_sources, 1:14]) == 0
        query = int(dataset.arrays["query"][row])
        assert np.array_equal(batch["target"][row, 0].numpy(), inputs[row, sources[query], 1:9])
    assert np.count_nonzero(inputs[:, :, 19:21]) == 0
    assert np.allclose(inputs[:, ports.indices, 21:25], coordinate_channels(ports.sites, 20))


def test_XOR_four_combinations_balanced_and_encoding():
    data = generate_task("xor", 32, 5001)
    bits = data.arrays["payload"][:, :, 0].astype(int)
    assert np.bincount(2 * bits[:, 0] + bits[:, 1]).tolist() == [8, 8, 8, 8]
    points = grid_points()
    batch = data.batch([0, 1], points, register_ports(points))
    for i in range(2):
        out = batch["output_nodes"][i, 0]
        assert batch["inputs"][i, out, 14:19].tolist() == [1, 1, 0, 0, 0]


def test_fill_train_weight_is_frozen_and_all_100_ports_used():
    data = generate_task("fill", 40, 5001)
    positive = data.target.sum()
    assert data.positive_weight == np.clip((data.target.size - positive) / positive, 1, 5)
    assert generate_task("fill", 10, 5002, split="validation").positive_weight is None
    assert generate_task("fill", 10, 5003, split="test").positive_weight is None
    points = grid_points()
    batch = data.batch([0, 1], points, register_ports(points))
    assert batch["output_nodes"].shape == (2, 100)
    assert batch["active_nodes"].sum().item() == 200
    assert batch["inputs"][:, :, 19].sum().item() == 2
    assert torch.count_nonzero(batch["inputs"][:, :, 1:19]) == 0


def test_fill_BA_map_macro_and_degenerate_accuracy():
    # Factor 0.45 has two maps, others one. Per-map then per-p weighting matters.
    target = np.array([[[1], [0], [0]], [[1], [0], [0]], [[1], [0], [0]], [[1], [1], [1]]], dtype=float)
    pred = np.array([[[1], [0], [0]], [[1], [1], [1]], [[0], [1], [1]], [[1], [0], [0]]], dtype=bool)
    logits = np.where(pred, 2.0, -2.0)
    metrics = evaluate_task("fill", logits, target, np.ones((4, 3), dtype=bool), np.array([0.45, 0.45, 0.55, 0.65]))
    assert metrics["BA_per_map"] == [1, 0.5, 0, 1/3]
    assert metrics["degenerate_map_frequency"] == 0.25
    assert metrics["score"] == pytest.approx((0.75 + 0 + 1/3) / 3)
    assert evaluate_task("xor", np.zeros((2, 1, 1)), np.ones((2, 1, 1)))["score"] == 1


def test_trivial_fill_controls_and_resource_normalization_encoding():
    fill = generate_task("fill", 4, 5001)
    controls = fill_trivial_predictions(fill)
    assert np.all(controls["seed_only"].sum(axis=1) == 1)
    assert np.array_equal(controls["all_free"], fill.arrays["free"])
    resource = generate_task("resource", 3, 5001)
    coefficients = resource.arrays["coefficients"]
    assert resource.train_target_variance == np.var(resource.target, dtype=np.float64)
    assert np.allclose(np.sum(coefficients**2, axis=(2, 3)) / 2, 1)
    # Dense quadrature on a periodic grid verifies spatial zero mean/unit variance.
    axis = np.arange(80) * 20 / 80
    a, b = np.meshgrid(axis, axis, indexing="ij")
    values = evaluate_resource_fields(coefficients, np.stack((a.ravel(), b.ravel()), axis=1), 20)
    assert np.allclose(values.mean(-1), 0, atol=1e-12)
    assert np.allclose(values.var(-1), 1, atol=1e-12)
    points = grid_points()
    ports = resource_ports(points)
    labels = np.arange(400) % 5
    batch = resource.batch([0, 1], points, ports, labels=labels)
    inputs = batch["inputs"].numpy()
    assert inputs.shape == (2, 400, 29)
    assert np.count_nonzero(inputs[:, :, 9:21]) == 0
    assert np.allclose(inputs[:, :, 21:25], coordinate_channels(points, 20))
    physical = evaluate_resource_fields(coefficients[:2], points, 20)
    for c in range(5):
        sites = labels == c
        assert np.allclose(inputs[:, sites, 1+c], physical[:, c, sites])
        other_slots = [i for i in range(1, 9) if i != 1+c]
        assert np.count_nonzero(inputs[:, sites][:, :, other_slots]) == 0
    assert np.allclose(batch["target"].numpy()[..., 0],
                       evaluate_resource_fields(coefficients[:2], resource_sites(), 20).mean(1))
