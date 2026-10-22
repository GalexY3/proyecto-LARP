import numpy as np
import torch

from larp.model import LARPModel
from larp.transmission_probe import GainProbeModel, accuracy_gate, copy_gate, measure, target_batch


def test_factor_one_is_exact_original_forward_with_same_parameters():
    torch.set_num_threads(4)
    original, gain1, gain10 = LARPModel("G", 1, seed=2101), GainProbeModel(2101, 1), GainProbeModel(2101, 10)
    for key, value in original.state_dict().items():
        assert torch.equal(value, gain1.state_dict()[key])
        assert torch.equal(value, gain10.state_dict()[key])
    assert original.parameter_count == gain1.parameter_count == gain10.parameter_count == 12261
    x = torch.randn(4, 8, 25, generator=torch.Generator().manual_seed(73))
    edges = torch.tensor([[0, 1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 0]])
    dist, labels = torch.ones(8), torch.zeros(8, dtype=torch.long)
    assert torch.equal(original(x, edges, dist, labels, steps=16), gain1(x, edges, dist, labels, steps=16))
    assert not torch.equal(gain1(x, edges, dist, labels, steps=16), gain10(x, edges, dist, labels, steps=16))


def test_target_change_retains_same_input_tensor_and_second_bit():
    x = torch.tensor([[[0., 1.]], [[1., 0.]], [[1., 1.]], [[0., 0.]]])
    batch = {"inputs": x, "cases": np.array([[0, 1, 2, 0, 0], [0, 1, 2, 0, 1], [0, 1, 2, 1, 0], [0, 1, 2, 1, 1]]),
             "target": torch.tensor([[0.], [1.], [1.], [0.]])}
    copy = target_batch(batch, "b0")
    assert copy["inputs"] is batch["inputs"]
    assert torch.equal(copy["target"].ravel(), torch.tensor([0., 0., 1., 1.]))
    assert torch.equal(batch["target"].ravel(), torch.tensor([0., 1., 1., 0.]))


def test_common_gate_cannot_mix_favorable_gains_or_seeds():
    cfg = {"increment_gains": [1., 10.], "training_seeds": [2101, 2102], "gate_accuracy": .98}
    records = [{"geometry": kind, "training_seed": seed, "mode": "local", "target": "b0", "gain": gain,
                "status": "COMPLETE", "finite": True, "train": {"accuracy": 1.}, "validation": {"accuracy": 1.}}
               for kind, gain in (("grid", 1.), ("mhu", 10.)) for seed in cfg["training_seeds"]]
    assert copy_gate(records, cfg, ["grid"])
    assert not copy_gate(records, cfg, ["grid", "mhu"])
    assert not copy_gate(records[:1], cfg, ["grid"])
    records[0]["validation"]["accuracy"] = .5
    assert not copy_gate(records, cfg, ["grid"])


def test_accuracy_requires_train_and_validation_without_partial_endpoint():
    record = {"status": "COMPLETE", "finite": True, "train": {"accuracy": 1.}, "validation": {"accuracy": 1.}}
    assert accuracy_gate(record)
    assert not accuracy_gate({**record, "status": "RESOURCE_LIMIT"})
    assert not accuracy_gate({**record, "train": {"accuracy": .5}})


def test_b0_flip_scoring_requires_invariance_to_second_source():
    class ExactSelector(torch.nn.Module):
        def forward(self, inputs, edge_index, edge_dist, labels, steps=16):
            return (20 * (inputs[:, 1:2, 1:2] - .5)).expand(-1, 3, -1)
    inputs = torch.zeros(4, 3, 25)
    inputs[:, 1, 1] = torch.tensor([0., 0., 1., 1.])
    inputs[:, 2, 1] = torch.tensor([0., 1., 0., 1.])
    batch = {"inputs": inputs, "output": torch.zeros(4, dtype=torch.long),
             "sources": np.tile([1, 2], (4, 1)), "cases": np.array([[0, 1, 2, a, b] for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))]),
             "target": torch.tensor([[0.], [0.], [1.], [1.]])}
    context = {"edge_index": torch.tensor([[1, 2], [0, 0]]), "edge_dist": torch.ones(2),
               "labels": torch.zeros(3, dtype=torch.long), "hops": np.ones((3, 3))}
    result = measure(ExactSelector(), batch, context, {"steps": 16}, "b0")
    assert result["accuracy"] == 1
    assert result["source_flip_correct_fraction_by_role"] == [1., 1.]
    assert result["source_flip_class_change_fraction_by_role"] == [1., 0.]
