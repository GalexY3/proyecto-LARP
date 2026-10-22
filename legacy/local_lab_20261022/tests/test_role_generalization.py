import numpy as np
import pytest
import torch

from larp.artifacts import array_hash
from larp.gru_baseline import GGNNLikeModel
from larp.learning_diagnostics import state_hash
from larp.role_generalization import coordinates_off, preflight_control


def test_coordinate_ablation_copies_and_zeroes_all_nodes_without_other_changes():
    x = torch.randn(4, 8, 25, generator=torch.Generator().manual_seed(371))
    original = x.clone()
    target = torch.tensor([[0.], [0.], [1.], [1.]])
    batch = {"inputs": x, "target": target, "cases": np.arange(20).reshape(4, 5)}
    changed = coordinates_off(batch)
    assert changed["inputs"] is not x
    assert torch.equal(x, original)
    assert torch.equal(changed["inputs"][:, :, :21], original[:, :, :21])
    assert torch.count_nonzero(changed["inputs"][:, :, 21:25]) == 0
    assert changed["target"] is target and changed["cases"] is batch["cases"]


def test_control_preflight_rejects_target_or_initial_weight_drift():
    model = GGNNLikeModel(2101)
    batch = {"inputs": torch.zeros(4, 8, 25), "target": torch.tensor([[0.], [0.], [1.], [1.]])}
    record = {"status": "COMPLETE", "training_seed": 2101, "geometry": "grid", "target": "b0", "mode": "local",
              "parameters": 12481, "updates_completed": 250, "initial_state_hash": state_hash(model),
              "train_input_hash": array_hash(batch["inputs"].numpy()), "validation_input_hash": array_hash(batch["inputs"].numpy()),
              "train_target_hash": array_hash(batch["target"].numpy()), "validation_target_hash": array_hash(batch["target"].numpy())}
    assert all(preflight_control(record, model, 2101, batch, batch).values())
    changed = {**batch, "target": 1-batch["target"]}
    with pytest.raises(ValueError, match="reused control differs"):
        preflight_control(record, model, 2101, changed, batch)
    with pytest.raises(ValueError, match="reused control differs"):
        preflight_control(record, GGNNLikeModel(2102), 2101, batch, batch)
