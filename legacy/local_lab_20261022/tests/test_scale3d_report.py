import csv
from copy import deepcopy

import pytest

from larp.scale3d_report import SEEDS, SIZES, write_report


def record(N, seed, step=300):
    factor = 1 if seed == 3101 else 2
    scores = {arm: [{"task": task, "MSE": factor * value, "world_MSE": [factor * value]}
                   for task in range(3)]
              for arm, value in (("mhu", 2.), ("local", 4.), ("random", 8.))}
    return {"N": N, "seed": seed, "status": "BUDGET_LIMIT_MATCHED_STEPS",
            "training_updates": step, "evaluations": [{"step": step, "scores": scores}]}


def test_complete_coverage_checks_endpoint_and_paired_ratios(tmp_path):
    final = {"status": "INCOMPLETE_OR_INVALID", "common_scale_endpoint": 300,
             "records": [record(N, seed) for N in SIZES for seed in SEEDS]}
    original = deepcopy(final)
    outcome = write_report(final, tmp_path)
    assert outcome == {"global_scale_eligible": True, "global_checkpoint": 300, "comparison_rows": 12}
    assert final == original
    with (tmp_path / "comparison.csv").open(encoding="utf-8") as stream:
        row = next(csv.DictReader(stream))
    assert float(row["MSE_mhu_mean"]) == 3
    assert float(row["MSE_mhu_min"]) == 2
    assert float(row["MSE_mhu_max"]) == 4
    assert float(row["ratio_MHU_LOCAL_mean"]) == .5
    assert float(row["ratio_MHU_RANDOM_mean"]) == .25


def test_omitted_size_rejects_global_endpoint_but_keeps_local_pairs(tmp_path):
    final = {"common_scale_endpoint": 300,
             "records": [record(N, seed) for N in SIZES[:-1] for seed in SEEDS]}
    outcome = write_report(final, tmp_path)
    assert not outcome["global_scale_eligible"]
    assert outcome["global_checkpoint"] is None and outcome["comparison_rows"] == 9
    assert "ESCALA INCONCLUYENTE" in (tmp_path / "SUMMARY.md").read_text(encoding="utf-8")
    assert not (tmp_path / "comparison.png").exists()


def test_all_invalid_has_header_only_without_invented_measurements(tmp_path):
    final = {"common_scale_endpoint": None, "records": [
        {"N": N, "seed": seed, "status": "INVALID_MHU_CLAIM", "training_updates": 0}
        for N in SIZES for seed in SEEDS]}
    outcome = write_report(final, tmp_path)
    assert outcome["comparison_rows"] == 0
    assert len((tmp_path / "comparison.csv").read_text().splitlines()) == 1
    assert "no se imputan resultados" in (tmp_path / "SUMMARY.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("failure", ["duplicate", "different_step", "nan", "missing_arm", "zero_denominator"])
def test_bad_pair_or_undefined_ratio_is_not_fabricated(tmp_path, failure):
    a, b = record(1024, 3101), record(1024, 3102)
    if failure == "duplicate":
        records = [a, b, deepcopy(b)]
    else:
        records = [a, b]
        if failure == "different_step":
            b["evaluations"][0]["step"] = 600
            b["training_updates"] = 600
        elif failure == "nan":
            b["evaluations"][0]["scores"]["mhu"][0]["MSE"] = float("nan")
        elif failure == "missing_arm":
            del b["evaluations"][0]["scores"]["random"]
        else:
            b["evaluations"][0]["scores"]["local"][0]["MSE"] = 0
    result = write_report({"common_scale_endpoint": None, "records": records}, tmp_path)
    assert not result["global_scale_eligible"]
    if failure == "zero_denominator":
        with (tmp_path / "comparison.csv").open(encoding="utf-8") as stream:
            assert next(csv.DictReader(stream))["ratio_MHU_LOCAL_mean"] == ""
    else:
        assert result["comparison_rows"] == 0
