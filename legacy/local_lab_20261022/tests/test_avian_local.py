"""Control selection must not condition on having passed the MHU test."""
import copy
import numpy as np
import pytest
import larp.avian_local as local
from larp.avian import load_avian_config


def test_first_packed_control_retained_when_certificate_fails(monkeypatch, tmp_path):
    config = copy.deepcopy(load_avian_config())
    config["optimizer"]["Adam_steps"] = 2
    config["optimizer"]["LBFGSB_maxiter"] = 1
    monkeypatch.setattr(local, "load_avian_config", lambda: config)
    calls = []

    def failed_certificate(*args, **kwargs):
        calls.append(1)
        return {"passed": False, "scientific_admissible": False, "mocked_in_unit_test": True}

    monkeypatch.setattr(local, "certify_geometry", failed_certificate)
    monkeypatch.setattr(local, "packing_diagnostics", lambda *args: {
        "packing_admitted": True, "maximum_relative_overlap": 0.0, "mocked_in_unit_test": True})
    geometry = local.generate_local_control(1101, output_dir=tmp_path)
    assert len(calls) == 1
    assert geometry.metadata["attempt"] == 0
    assert geometry.metadata["control_admitted"]
    assert not geometry.metadata["admitted"]
    assert not geometry.metadata["mhu_admitted"]
    assert not geometry.metadata["MHU_certificate_was_selection_criterion"]
    assert not geometry.metadata["certificate"]["passed"]
    assert not geometry.metadata["neural_training"]
    assert geometry.metadata["attempts"][0]["spectral_energy"] == 0


def test_local_control_keeps_exact_initial_seed_namespace(monkeypatch, tmp_path):
    config = copy.deepcopy(load_avian_config())
    config["optimizer"]["Adam_steps"] = 0
    config["optimizer"]["LBFGSB_maxiter"] = 1
    monkeypatch.setattr(local, "load_avian_config", lambda: config)
    monkeypatch.setattr(local, "certify_geometry", lambda *args, **kwargs: {
        "passed": False, "scientific_admissible": False, "mocked_in_unit_test": True})
    monkeypatch.setattr(local, "packing_diagnostics", lambda *args: {
        "packing_admitted": True, "maximum_relative_overlap": 0.0, "mocked_in_unit_test": True})
    geometry = local.generate_local_control(1102, output_dir=tmp_path)
    rng = np.random.default_rng(np.random.SeedSequence([20261008, 1102, 0]))
    labels = rng.permutation(np.repeat(np.arange(5), [163, 85, 68, 50, 34]))
    points = rng.uniform(0, 20, (400, 2))
    assert np.array_equal(labels, geometry.labels)
    assert geometry.metadata["attempts"][0]["initial_points_hash"] == local.array_hash(points)


def test_local_seed_replacement_is_not_authorized(tmp_path):
    with pytest.raises(ValueError, match="frozen control seeds"):
        local.generate_local_control(9001, output_dir=tmp_path)
