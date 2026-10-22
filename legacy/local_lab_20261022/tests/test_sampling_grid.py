"""Budget safety, query registration and aligned reuse accounting."""
import numpy as np
import pytest
import larp.sampling_grid as supplement
from larp.sampling_grid import load_config,continuous_queries,conservative_construction_estimate,original_cell
from larp.geometry import generate_geometry


def test_supplement_denominators_do_not_promote_reused_cells():
    cfg=load_config()
    assert cfg["evaluation"]["expected_cells"]==576
    assert cfg["evaluation"]["reused_aligned_cells"]==216
    assert cfg["evaluation"]["new_cells"]==360
    assert cfg["construction"]["proposals"]==100000
    assert cfg["construction"]["restarts"]==10


def test_continuous_queries_fixed_rng_and_distinct_from_grid_sites():
    cfg=load_config();sites=continuous_queries(cfg)
    assert sites.shape==(100,2) and np.all((sites>=0)&(sites<20))
    np.testing.assert_array_equal(sites,continuous_queries(cfg))
    assert not np.any(np.all(np.isclose((sites-.5)%1,0,atol=1e-12),axis=1))


def test_conservative_estimate_blocks_long_annealing_before_scores():
    cfg=load_config()
    cal=[{"seconds_per_proposal_conservative_includes_wrapper":.0001,"certificate_seconds":[.2]}]
    estimate=conservative_construction_estimate(cal,.2,cfg)
    assert estimate["estimated_conservative_construction_seconds"]>600
    assert not estimate["eligible"] and not estimate["can_interrupt_mid_attempt"]


def test_safety_uses_slower_calibration_instead_of_fastest_seed():
    cfg=load_config()
    a={"seconds_per_proposal_conservative_includes_wrapper":1e-5,"certificate_seconds":[.2]}
    b={"seconds_per_proposal_conservative_includes_wrapper":2e-5,"certificate_seconds":[.3]}
    r=conservative_construction_estimate([a,b],.2,cfg)
    assert r["seconds_per_proposal_max_measured"]==2e-5
    assert r["certificate_seconds_max_measured"]==.3


def test_grid_aligned_queries_coincide_but_counts_are_nominal():
    grid=generate_geometry(400,9005,"grid",detailed_certificate=False)
    q=np.asarray([(2*a+.5,2*b+.5) for a in range(10) for b in range(10)])
    assert np.all(np.any(np.all(q[:,None,:]==grid.points[None,:,:],axis=-1),axis=1))
    np.testing.assert_array_equal(np.bincount(grid.labels,minlength=5),[163,85,68,50,34])


def test_original_cell_matches_specific_estimator_without_duplicates():
    row={"family":"nominal_mhu","geometry_seed":1101,"condition":"native","band":"smooth","noise_sigma":.1}
    a={**row,"estimator":"nearest_neighbor"};b={**row,"estimator":"local_gaussian"}
    assert original_cell({"records":[a,b]},{"records":[row]},"nominal_mhu",1101,"native","smooth",.1,"oracle_band")==row
    assert original_cell({"records":[a,b]},{"records":[row]},"nominal_mhu",1101,"native","smooth",.1,"local_gaussian")==b


def test_budget_rejection_stops_before_any_field_score(monkeypatch,tmp_path):
    monkeypatch.setattr(supplement,"calibrate",lambda *args:{"decision":{"eligible":False}})
    monkeypatch.setattr(supplement,"evaluate",lambda *args:pytest.fail("Budget-rejected construction cannot evaluate fields"))
    result=supplement.run(tmp_path)
    assert result["status"]=="GRID_NOT_RUN" and result["no_field_MSE"]
    assert (tmp_path/"preregistration.json").exists()
    assert not result["beliefs_updated"]
