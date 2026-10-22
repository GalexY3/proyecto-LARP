import numpy as np
import pytest

from larp.robustness import (build_batch_masks, build_edge_mask, build_node_mask,
                             evaluate_damaged_predictions, fixed_test_indices, normalized_damage_auc,
                             output_preservation, preregistered_centers,
                             relocated_ports)


def points(n=100):
    return np.random.default_rng(82).uniform(0, 20, (n, 2))


def test_exact_count_ports_protected_and_preregistered_randomness():
    x = points()
    protected = np.zeros(100, bool)
    protected[:10] = True
    mask = build_node_mask(x, q=0.20, seed=7, protected=protected)
    assert mask.available and len(mask.removed) == 20
    assert mask.alive[:10].all()
    assert mask.digest == build_node_mask(x, q=0.20, seed=7, protected=protected).digest
    assert mask.digest != build_node_mask(x, q=0.20, seed=8, protected=protected).digest
    assert mask.metadata["reconnect"] is False


def test_localized_periodic_nearest_and_fixed_radius_counts():
    x = np.array([[0.1, 0], [19.9, 0], [10, 10], [1, 0], [2, 0]])
    mask = build_node_mask(x, mode="localized", count=2, center=[0, 0], L=20)
    assert set(mask.removed.tolist()) == {0, 1}
    assert mask.metadata["result_radius"] == pytest.approx(0.1)
    disk = build_node_mask(x, mode="disk", radius=1.1, center=[0, 0], L=20, protected=[0])
    assert set(disk.removed.tolist()) == {1, 3}
    assert disk.metadata["removed_count"] == 2


def test_type_absolute_fraction_and_unavailable_not_replace():
    x = points(20)
    labels = np.arange(20) % 5
    mask = build_node_mask(x, mode="type", type_id=3, labels=labels, count=4)
    assert mask.available and len(mask.removed) == 4
    assert np.all(labels[mask.removed] == 3)
    absent = build_node_mask(x, mode="type", type_id=3, labels=labels, count=4, protected=[3])
    assert not absent.available and absent.alive.all()
    assert absent.metadata["reason"] == "insufficient_eligible_nodes"
    fraction = build_node_mask(x, mode="type", type_id=3, labels=labels, fraction=0.5)
    assert len(fraction.removed) == 2


def test_batch_example_specific_protection_and_end_to_end_flags():
    x = points(20)
    active = np.zeros((2, 20), bool)
    active[0, [0, 1]] = True
    active[1, [2, 3]] = True
    alive, records = build_batch_masks(x, active, q=0.20, seed=5)
    assert np.all(alive[active]) and np.all((~alive).sum(1) == 4)
    unprotected, _ = build_batch_masks(x, active, protect_ports=False, q=1, seed=5)
    flags = output_preservation(unprotected, np.array([[0], [2]]), np.array([[1], [3]]))
    assert not flags["processing_eligible"].any()
    assert len(records) == 2


def test_edge_arc_and_pair_modes_no_topology_mutation():
    edges = np.array([[0, 1, 1, 2, 2, 3, 3, 0], [1, 0, 2, 1, 3, 2, 0, 3]])
    original = edges.copy()
    independent = build_edge_mask(edges, q=0.5, seed=2)
    paired = build_edge_mask(edges, q=0.5, seed=2, mode="paired_undirected_edges")
    assert np.count_nonzero(~independent.edge_alive) == np.count_nonzero(~paired.edge_alive) == 4
    for arc in range(0, 8, 2):
        assert paired.edge_alive[arc] == paired.edge_alive[arc+1]
    assert np.array_equal(edges, original)
    odd = build_edge_mask(edges, q=0.125, mode="paired_undirected_edges")
    assert not odd.available and "SCIENTIFIC_BLOCKER" in odd.metadata["reason"]


def test_preregistered_hash_indices_centers_auc_and_relocation():
    indices = fixed_test_indices(1000)
    assert len(indices) == len(np.unique(indices)) == 512
    assert np.array_equal(indices, fixed_test_indices(1000))
    assert np.array_equal(preregistered_centers(seed=9), preregistered_centers(seed=9))
    assert normalized_damage_auc([0, 0.05, 0.10, 0.20], [0.8]*4) == pytest.approx(0.8)
    assert normalized_damage_auc([0, 0.10, 0.20], [1, 0.5, 0]) == pytest.approx(0.5)
    with pytest.raises(ValueError):
        normalized_damage_auc([0, 0.10], [1, 0.5])
    ports = relocated_ports(points(400), offset=(0.5, 0), world_side=10)
    assert len(np.unique(ports.indices)) == 100
    assert ports.sites[0].tolist() == [1.0, 0.5]


def test_end_to_end_copy_lost_essential_input_is_failure_not_processing():
    alive = np.ones((3, 5), bool)
    alive[0, 1] = False  # selected source lost despite intact output
    alive[1, 4] = False  # output lost: placeholder logit must be ignored
    logits = np.array([[[4, 4]], [[np.nan, np.nan]], [[4, -4]]])
    target = np.array([[[1, 1]], [[1, 1]], [[1, 0]]], dtype=float)
    metrics = evaluate_damaged_predictions("copy", logits, target, alive,
                                          np.array([[4], [4], [4]]), np.array([1, 1, 1]))
    assert metrics["score"] == pytest.approx(1/3)
    assert metrics["processing_score"] == 1
    assert metrics["processing_example_count"] == 1
    assert metrics["system_failure_fraction"] == pytest.approx(2/3)
    assert metrics["processing_metrics"]["loss"] < 0.1


def test_end_to_end_fill_macro_per_p_zero_missing_outputs_without_fabrication():
    alive = np.ones((4, 4), bool)
    alive[1, 3] = False
    logits = np.array([[[2], [-2]], [[np.nan], [np.nan]], [[-2], [2]], [[2], [-2]]])
    target = np.array([[[1], [0]], [[1], [0]], [[1], [0]], [[1], [0]]], dtype=float)
    output_nodes = np.array([[2, 3]] * 4)
    metrics = evaluate_damaged_predictions("fill", logits, target, alive, output_nodes,
                                          np.zeros((4, 1), dtype=int),
                                          free=np.ones((4, 2), bool), p=[0.45, 0.45, 0.55, 0.65])
    assert metrics["system_score_per_example"] == [1, 0, 0, 1]
    assert metrics["system_BA_by_p"] == {"0.45": 0.5, "0.55": 0, "0.65": 1}
    assert metrics["score"] == pytest.approx(0.5)
    assert metrics["processing_score"] == pytest.approx(2/3)
    assert np.isfinite(metrics["processing_metrics"]["BCE"])
