import numpy as np
import torch

from larp.balanced_batch_probe import balanced_schedule
from larp.gru_baseline import GGNNLikeModel
from larp.model import LARPModel


def test_parameter_count_same_initial_cores_and_external_rng_unchanged():
    torch.manual_seed(713)
    before = torch.random.get_rng_state().clone()
    model = GGNNLikeModel(2101)
    assert torch.equal(before, torch.random.get_rng_state())
    assert model.parameter_count == 12481
    original = LARPModel("G", 1, seed=2101)
    for name in ("encoder", "normalization", "message", "readout1", "readout2"):
        a, b = getattr(model, name).state_dict(), getattr(original, name).state_dict()
        assert all(torch.equal(a[key], b[key]) for key in a)
    assert torch.equal(model.distance_weight, original.distance_weight)
    assert torch.count_nonzero(model.gru.bias_ih) == torch.count_nonzero(model.gru.bias_hh) == 0


def test_labels_invisible_and_batches_isolated():
    torch.set_num_threads(4)
    model = GGNNLikeModel(2101)
    x = torch.randn(2, 8, 25, generator=torch.Generator().manual_seed(1))
    edges = torch.tensor([[0, 1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7]])
    a = model(x, edges, torch.ones(7), torch.zeros(8), steps=4)
    b = model(x, edges, torch.ones(7), torch.arange(8)%5, steps=4)
    assert torch.equal(a, b)
    changed = x.clone()
    changed[1, 0, 1] += 3
    c = model(changed, edges, torch.ones(7), None, steps=4)
    assert torch.equal(a[0], c[0])


def test_causal_support_cannot_cross_more_than_T_directed_edges():
    model = GGNNLikeModel(2101)
    x = torch.randn(1, 8, 25, generator=torch.Generator().manual_seed(62))
    changed = x.clone()
    changed[0, 0, 1] += 1
    edges = torch.tensor([[0, 1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7]])
    first = model(x, edges, torch.ones(7), None, steps=2)
    second = model(changed, edges, torch.ones(7), None, steps=2)
    assert torch.equal(first[:, 3:], second[:, 3:])
    assert not torch.equal(first[:, 2], second[:, 2])


def test_reused_balanced_calendar_keeps_all_four_patterns():
    from pathlib import Path
    import json
    root = Path(__file__).resolve().parents[1]
    frozen = json.loads((root/"artifacts/balanced_batch_probe/v1/preregistration.json").read_text(encoding="utf-8"))
    for seed in (2101, 2102):
        calendar = np.array(frozen["schedule"][str(seed)])
        assert np.array_equal(calendar, balanced_schedule(12, 250, 20261008, seed, 9914))
        assert np.array_equal(calendar%4, np.tile(np.arange(4), (250, 1)))
