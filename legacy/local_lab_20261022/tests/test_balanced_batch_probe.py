import numpy as np
import pytest
import torch

from larp.artifacts import array_hash
from larp.balanced_batch_probe import balanced_schedule, control_compatible
from larp.learning_diagnostics import state_hash
from larp.transmission_probe import GainProbeModel


def test_schedule_preserves_quartets_and_each_complete_cycle_covers_every_triple():
    schedule = balanced_schedule(12, 250, 20261008, 2101, 9914)
    assert schedule.shape == (250, 4)
    assert np.array_equal(schedule % 4, np.tile(np.arange(4), (250, 1)))
    assert np.all(schedule//4 == schedule[:, :1]//4)
    for first in range(0, 240, 12):
        assert sorted((schedule[first:first+12, 0]//4).tolist()) == list(range(12))
    exposure = np.bincount(schedule.ravel(), minlength=48).reshape(12, 4)
    assert exposure.min() == 20 and exposure.max() == 21
    assert np.all(exposure == exposure[:, :1])
    assert np.array_equal(schedule, balanced_schedule(12, 250, 20261008, 2101, 9914))
    assert not np.array_equal(schedule, balanced_schedule(12, 250, 20261008, 2102, 9914))


def test_control_guard_rejects_changed_input_or_initialization():
    model = GainProbeModel(2101, 1)
    batch = {"inputs": torch.zeros(4, 8, 25), "target": torch.tensor([[0.], [0.], [1.], [1.]])}
    control = {"status": "COMPLETE", "target": "b0", "gain": 1., "geometry": "grid", "mode": "local",
               "training_seed": 2101, "updates_completed": 250, "initial_state_hash": state_hash(model),
               "train_input_hash": array_hash(batch["inputs"].numpy()), "validation_input_hash": array_hash(batch["inputs"].numpy()),
               "train_target_hash": array_hash(batch["target"].numpy()), "validation_target_hash": array_hash(batch["target"].numpy())}
    assert all(control_compatible(control, 2101, batch, batch, model).values())
    changed = {**batch, "inputs": batch["inputs"].clone()}
    changed["inputs"][0, 1, 1] = 1
    with pytest.raises(ValueError, match="RANDOM control differs"):
        control_compatible(control, 2101, changed, batch, model)
    with pytest.raises(ValueError, match="RANDOM control differs"):
        control_compatible(control, 2101, batch, batch, GainProbeModel(2102, 1))
