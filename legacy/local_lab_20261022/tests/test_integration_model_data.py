"""Small CPU pipeline integration, never evidence for an MHU advantage."""
import numpy as np
import pytest
import torch

from larp.data import generate_task, register_ports
from larp.geometry import Geometry, minimum_image
from larp.graphs import knn_graph
from larp.model import LARPModel
from larp.training import graph_tensors, select_ports


def setup_fixture():
    # 36 density-one substrate nodes, nine independent external ports. Includes
    # all five types without running/certifying a scientific MHU generator.
    a, b = np.meshgrid(np.arange(6), np.arange(6), indexing="ij")
    points = np.stack((a.ravel() + 0.5, b.ravel() + 0.5), axis=-1)
    labels = np.arange(36) % 5
    return Geometry(points, labels, 6, {"test_only": True, "geometry_seed": 17})


@pytest.mark.parametrize("task", ["xor", "copy", "fill"])
@pytest.mark.parametrize("variant", ["G", "T", "F"])
def test_small_world_graph_model_loss_backward(task, variant):
    geometry = setup_fixture()
    edges = knn_graph(geometry.points, geometry.L, 6)
    assert edges.shape == (2, 6*geometry.N)
    ports = register_ports(geometry.points, L=6, world_side=3)
    dataset = generate_task(task, 12, 5001, world_side=3, L=6)
    batch = dataset.batch([0, 1, 2, 3], geometry.points, ports)
    model = LARPModel(variant, 8 if task == "copy" else 1)
    tensors = graph_tensors(geometry, edges, "cpu")
    logits = model(batch["inputs"], *tensors[:2], tensors[2], steps=2)
    selected = select_ports(logits, batch["output_nodes"])
    assert selected.shape == batch["target"].shape
    loss = torch.nn.functional.binary_cross_entropy_with_logits(selected, batch["target"])
    loss.backward()
    assert torch.isfinite(loss)
    for parameter in model.parameters():
        assert parameter.grad is not None and torch.isfinite(parameter.grad).all()
    # No model shape or graph adjacency depends on the oracle's obstacles.
    if task == "fill":
        assert len(ports.indices) == 9
        assert edges.shape[1] == 216


def test_native_shuffle_pair_preserves_world_ports_coordinates_edges_and_base_weights():
    native = setup_fixture()
    shuffled = Geometry(native.points, np.random.default_rng(7101).permutation(native.labels),
                        native.L, {"test_only": True})
    assert np.array_equal(np.bincount(native.labels, minlength=5), np.bincount(shuffled.labels, minlength=5))
    edges_a, edges_b = knn_graph(native.points, 6), knn_graph(shuffled.points, 6)
    ports_a, ports_b = register_ports(native.points, 6, 3), register_ports(shuffled.points, 6, 3)
    assert ports_a.digest == ports_b.digest
    assert np.array_equal(edges_a, edges_b)
    dataset = generate_task("copy", 10, 5001, world_side=3, L=6)
    first, second = dataset.batch([0, 1], native.points, ports_a), dataset.batch([0, 1], shuffled.points, ports_b)
    assert torch.equal(first["inputs"], second["inputs"])
    assert torch.equal(first["target"], second["target"])
    model_a, model_b = LARPModel("T", seed=2101), LARPModel("T", seed=2101)
    assert all(torch.equal(left, right) for left, right in zip(model_a.parameters(), model_b.parameters()))
    before = dataset.digest
    distances = np.linalg.norm(minimum_image(native.points[edges_a[0]] - native.points[edges_a[1]], 6), axis=-1)
    model_a(first["inputs"], torch.tensor(edges_a), torch.tensor(distances, dtype=torch.float32), torch.tensor(native.labels), steps=2)
    model_b(second["inputs"], torch.tensor(edges_b), torch.tensor(distances, dtype=torch.float32), torch.tensor(shuffled.labels), steps=2)
    assert before == dataset.digest
