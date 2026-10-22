import json
from pathlib import Path
import numpy as np
import pytest

from larp.geometry import generate_geometry
from larp.learning_diagnostics import graph_context
from larp.role_coverage import build_panels, gate, greedy_extras, hypothesis_updates, objective

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def panels():
    cfg=json.loads((ROOT/"configs/role_coverage_v1.json").read_text(encoding="utf-8"))
    context=graph_context(generate_geometry(N=400,seed=1101,kind="grid"))
    report,features=build_panels(context,cfg)
    return cfg,report,features


def test_common_validation_support_and_reserved_active_port_holdout(panels):
    cfg,panel,features=panels
    assert panel["status"]=="AVAILABLE" and panel["candidate_pool_count"]==2086
    assert len(panel["SS"])==len(panel["UU"])==4
    assert [t[0] for t in panel["SS"]]==[t[0] for t in panel["UU"]]
    assert len(set(panel["reserved_queries"]))==4
    for condition,triples in panel["panels"].items():
        assert len(triples)==len(set(triples))==12
        assert triples[:4]==panel["anchors"]
        assert triples[4:]==sorted(triples[4:])
        active={site for t in triples for site in t}
        assert not active.intersection(panel["reserved_U"])
        assert not {t[0] for t in triples}.intersection(panel["reserved_queries"])
        for _,a,b in panel["SS"]:
            assert a in {t[1] for t in triples} and b in {t[2] for t in triples}
            assert a in {t[2] for t in triples} and b in {t[1] for t in triples}
    for ss,uu in zip(panel["SS"],panel["UU"]):
        assert ss[0] not in cfg["validation_excluded_query_sites"]
        assert 11 not in ss[1:] and 11 not in uu[1:]
        assert (features["hops"][ss[1],ss[0]],features["hops"][ss[2],ss[0]]) == (features["hops"][uu[1],uu[0]],features["hops"][uu[2],uu[0]])


def test_reproducible_first_eligibility_and_fixed_swapped_anchors(panels):
    cfg,panel,features=panels
    # Seed9941 first geometrically eligible candidate, not a score-selected panel.
    assert panel["attempts"][-1]["status"]=="ACCEPTED"
    assert all(a["status"]=="REJECTED" for a in panel["attempts"][:-1])
    a,b,c,d=panel["anchors"]
    assert b==(a[0],a[2],a[1]) and d==(c[0],c[2],c[1])
    assert len({a[1],a[2],c[1],c[2]})==4
    assert set(panel["hop_profiles"])=={(2,2)}


def test_greedy_lexicographic_objective_matches_exhaustive_first_step(panels):
    cfg,panel,features=panels
    pool=features["pool"]
    reserved=set(panel["reserved_U"])
    eligible=[i for i,t in enumerate(pool) if t not in panel["anchors"] and t[0] not in panel["reserved_queries"] and not(set(t)&reserved)]
    priority=panel["balanced_tie_priority"]
    expected=min(eligible,key=lambda i:objective(panel["anchors"]+[pool[i]],features["signature"])+(int(priority[i]),))
    result,trace=greedy_extras(panel["anchors"],eligible,features,priority,1)
    assert trace[0]["candidate_pool_index"]==expected
    assert result==[pool[expected]]


def fake_records(ss=.99,uu=.99):
    return [{"condition":c,"training_seed":s,"status":"COMPLETE","finite":True,"updates_completed":250,
             "train":{"accuracy":1.},"SS":{"accuracy":ss},"UU":{"accuracy":uu}}
            for c in ("UNIFORM","BALANCED") for s in (2101,2102)]


def test_gate_requires_both_seeds_both_strata_and_no_partial():
    rows=fake_records()
    assert gate(rows,"BALANCED")
    rows[-1]["UU"]["accuracy"] = .9375
    assert not gate(rows,"BALANCED")
    rows[-1]["UU"]["accuracy"] = 1
    rows[-1]["status"]="RESOURCE_LIMIT"
    assert not gate(rows,"BALANCED")


def test_registered_ordinal_rules_never_update_architecture_or_incomplete():
    hypotheses=json.loads((ROOT/"configs/role_coverage_hypotheses_v1.json").read_text(encoding="utf-8"))
    rows=fake_records(ss=1.,uu=1.)
    for row in rows:
        if row["condition"]=="UNIFORM":
            row["UU"]["accuracy"]=.75
    updated=hypothesis_updates(rows,hypotheses)
    assert updated["updates"]["H-R1"]["direction"]=="weak_support"
    assert updated["updates"]["H-R2"]["direction"]=="weak_counterevidence"
    assert updated["updates"]["H-R3"]["direction"]=="weak_counterevidence"
    assert updated["H1_H6"]==updated["architecture_C"]=="unchanged"
    supported_only=fake_records(ss=1.,uu=.75)
    partial=hypothesis_updates(supported_only,hypotheses)
    assert partial["updates"]["H-R2"]["direction"]=="weak_support"
    assert partial["updates"]["H-R3"]["direction"]=="weak_counterevidence"
    rows[0]["status"]="NOT_RUN"
    incomplete=hypothesis_updates(rows,hypotheses)
    assert not incomplete["eligible"]
    assert all(h["direction"]=="no_update_ineligible" for h in incomplete["updates"].values())
