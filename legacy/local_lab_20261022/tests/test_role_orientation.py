import copy
import json
import time
from pathlib import Path

import numpy as np
import pytest
import torch

from larp.geometry import Geometry
from larp.learning_diagnostics import graph_context
from larp import role_orientation as phase4

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def prepared_parts():
    torch.set_num_threads(4)
    torch.use_deterministic_algorithms(True)
    cfg=json.loads((ROOT/phase4.CONFIG).read_text(encoding="utf-8"))
    parent=json.loads((ROOT/cfg["parent_manifest"]).read_text(encoding="utf-8"))
    context=graph_context(Geometry.load(ROOT/cfg["geometry_file"]))
    schedules=phase4.calendars(cfg,parent)
    panel,features=phase4.build_panels(context,cfg,parent,schedules)
    batches,contract=phase4.build_batches(context,panel)
    return cfg,parent,context,schedules,panel,features,batches,contract


def test_fixed_physical_slots_and_intentional_duplicate(prepared_parts):
    cfg,parent,context,schedules,panel,features,batches,contract=prepared_parts
    b,d=panel["panels"]["B"],panel["panels"]["D8"]
    assert b==parent["panel"]["panels"]["BALANCED"]
    assert [i for i,(x,y) in enumerate(zip(b,d)) if x!=y]==[11]
    assert d[10]==d[11]==[77,68,86]
    assert len(set(map(tuple,b)))==12 and len(set(map(tuple,d)))==11
    assert len(batches["B"]["cases"])==len(batches["D8"]["cases"])==48
    assert np.array_equal(batches["D8"]["cases"][40:44],batches["D8"]["cases"][44:48])
    assert panel["nominal_statistics"]["B"]["role_exposure_imbalance_squared"]==0
    assert panel["nominal_statistics"]["D8"]["role_exposure_imbalance_squared"]==8
    for metric in (panel["nominal_statistics"],*panel["weighted_statistics_by_seed"].values()):
        for key in ("physical_source_exposures","physical_query_exposures","ordered_motif_histogram","outdegree_histograms_by_role"):
            assert metric["B"][key]==metric["D8"][key]
    assert all([m[c]["role_exposure_imbalance_squared"] for c in ("B","D8")]==[4,3364]
               for m in panel["weighted_statistics_by_seed"].values())


def test_common_both_role_support_four_novel_pairs_and_u_holdout(prepared_parts):
    cfg,parent,context,schedules,panel,features,batches,contract=prepared_parts
    assert panel["common_both_role_sources"]==[4,8,13,19,35,39,46,49,57,69]
    assert len(set(map(tuple,panel["novel_unordered_SS_pairs"])))==4
    train_pairs={tuple(sorted(t[1:])) for ts in panel["panels"].values() for t in ts}
    assert not train_pairs.intersection(map(tuple,panel["novel_unordered_SS_pairs"]))
    for train in panel["panels"].values():
        assert not set(panel["reserved_U"]).intersection(site for t in train for site in t)
        assert not set(panel["reserved_queries"]).intersection(t[0] for t in train)
        for _,a,b in panel["SS"]:
            assert {a,b}<={t[1] for t in train}&{t[2] for t in train}
    assert 46 in {site for train in panel["panels"].values() for t in train for site in t[1:]}
    for ss,uu in zip(panel["SS"],panel["UU"]):
        assert ss[0]==uu[0]
        assert features["signature"][tuple(ss)][:2]==features["signature"][tuple(uu)][:2]==(2,2)


def test_physical_bit_matching_and_changed_physical_targets(prepared_parts):
    cfg,parent,context,schedules,panel,features,batches,contract=prepared_parts
    assert contract["physical_pattern_target_differences_by_slot"]==[0]*11+[2]
    assert contract["physical_bit_inputs_matched_with_role_marks_erased"]
    assert torch.equal(batches["B"]["inputs"][:44],batches["D8"]["inputs"][:44])
    assert not torch.equal(batches["B"]["inputs"][44:],batches["D8"]["inputs"][44:])
    for batch in batches.values():
        assert torch.count_nonzero(batch["inputs"][:,:,21:25])==0
        assert np.array_equal(batch["target"].numpy().ravel(),batch["cases"][:,3])
    assert cfg["calendar_seed_mapping"]=={"2103":2101,"2104":2102}
    for seed,old in cfg["calendar_seed_mapping"].items():
        assert np.array_equal(schedules[seed],parent["calendars"][str(old)])


def test_preparation_never_optimizes_or_forwards_and_refuses_overwrite(prepared_parts,tmp_path,monkeypatch):
    cfg=prepared_parts[0]
    def forbidden(*args,**kwargs):
        raise AssertionError("preparation must never optimize or forward")
    monkeypatch.setattr(torch.optim,"AdamW",forbidden)
    monkeypatch.setattr(phase4.GGNNLikeModel,"forward",forbidden)
    monkeypatch.setattr(phase4,"measure",forbidden)
    monkeypatch.setattr(phase4,"predictions",forbidden)
    destination=tmp_path/"prepared"
    manifest=phase4.prepare(cfg,destination,time.perf_counter())
    assert manifest["optimizers_created"]==manifest["forwards_performed"]==0
    assert set(manifest["initial_state_hashes"])=={"2103","2104"}
    assert manifest["initial_state_hashes"]["2103"]!=manifest["initial_state_hashes"]["2104"]
    assert cfg["scope_file"] in manifest["identity"]["files"]
    assert cfg["hypotheses_file"] in manifest["identity"]["files"]
    phase4.validate_prepared(cfg,manifest)
    with pytest.raises(FileExistsError):
        phase4.prepare(cfg,destination,time.perf_counter())


@pytest.mark.parametrize("field",["identity","panel","calendars","calendar_hashes","dataset_hashes","initial_state_hashes","geometry"])
def test_execution_preflight_rejects_tampered_preparation(prepared_parts,tmp_path,field):
    cfg=prepared_parts[0]
    manifest=phase4.prepare(cfg,tmp_path/"prepared",time.perf_counter())
    altered=copy.deepcopy(manifest)
    if field=="panel":
        altered[field]["panels"]["D8"].pop()
    elif field=="identity":
        altered[field]["hash"]="0"*64
    elif field=="calendars":
        altered[field]["2103"][0]=[0,1,2,3] if altered[field]["2103"][0]!=[0,1,2,3] else [4,5,6,7]
    elif field in ("initial_state_hashes","calendar_hashes"):
        altered[field]["2103"]="0"*64
    elif field=="dataset_hashes":
        altered[field]["D8"]["inputs"]="0"*64
    else:
        altered[field]["ports"]="0"*64
    with pytest.raises(ValueError,match="INVALID_EXPERIMENT"):
        phase4.validate_prepared(cfg,altered)


def _measurement(size,accuracy=1.):
    rows=[]
    wrong=round(size*(1-accuracy))
    for i in range(size):
        label=(i%4)//2
        prediction=1-label if i<wrong else label
        rows.append({"case":[61 if size==16 and i//4==2 else i//4,62,60,label,i%2],
            "target":label,"prediction":prediction,"logit":float(2*prediction-1),"source_gradients":[1.,0.],
            "source_flipped_logits":[float(1-2*prediction),float(2*prediction-1)],"source_flip_abs_logit_changes":[2.,0.],
            "source_flip_should_change_target":[True,False],"source_flip_correct_predictions":[True,True],
            "source_flip_class_changes":[True,False]})
    return {"accuracy":sum(r["prediction"]==r["target"] for r in rows)/size,"loss":.1,"finite":True,
        "cases":rows,"measure_checkpoint_update":250}


def _records():
    return [{"condition":c,"training_seed":s,"status":"COMPLETE","finite":True,"updates_completed":250,
        "score_checkpoint_update":250,"identity_verified":True,"data_verified":True,"checkpoint_sha256":"a"*64,
        "initial_state_hash":"b"*64,"final_state_hash":"c"*64,
        **{name:_measurement(size) for name,size in {**phase4.PRIMARY_SIZES,"AUX_OLD":16}.items()}}
        for c,s in [("D8",2103),("B",2103),("B",2104),("D8",2104)]]


def test_primary_gate_readiness_and_complete_aggregate_are_separate():
    records=_records()
    assert phase4.aggregate_status(records)=="COMPLETE"
    assert phase4.gate(records,"B") and phase4.gate(records,"B",require_aux=True)
    records[1]["AUX_OLD"]=_measurement(16,.75)
    assert phase4.gate(records,"B") and not phase4.gate(records,"B",require_aux=True)
    records[0]["status"]="NUMERICAL_FAILURE"
    assert phase4.aggregate_status(records)=="NUMERICAL_FAILURE"
    assert phase4.gate(records,"B") and not phase4.gate(records,"D8")
    records[0]["status"]="NOT_RUN"
    assert phase4.aggregate_status(records)=="INCOMPLETE"
    records[0]["status"]="RESOURCE_LIMIT"
    assert phase4.aggregate_status(records)=="RESOURCE_LIMIT"


@pytest.mark.parametrize("bad",["missing_run","duplicate_run","missing_panel","missing_case","missing_flip","nonfinite_flip","wrong_updates","wrong_score_state","missing_checkpoint"])
def test_no_false_complete_for_partial_or_malformed_individuals(bad):
    rows=_records()
    if bad=="missing_run":
        rows.pop()
    elif bad=="duplicate_run":
        rows[3]=copy.deepcopy(rows[0])
    elif bad=="missing_panel":
        rows[0].pop("SS")
    elif bad=="missing_case":
        rows[0]["train"]["cases"].pop()
    elif bad=="missing_flip":
        rows[0]["UU"]["cases"][0].pop("source_flipped_logits")
    elif bad=="nonfinite_flip":
        rows[0]["UU"]["cases"][0]["source_flipped_logits"][0]=float("nan")
    elif bad=="wrong_updates":
        rows[0]["updates_completed"]=249
    elif bad=="wrong_score_state":
        rows[0]["score_checkpoint_update"]=225
    else:
        rows[0].pop("checkpoint_sha256")
    assert phase4.aggregate_status(rows)=="INCOMPLETE"


def test_only_registered_h_r4_updates_and_uu_endpoint(prepared_parts):
    cfg=prepared_parts[0]
    hypotheses=json.loads((ROOT/cfg["hypotheses_file"]).read_text(encoding="utf-8"))
    rows=_records()
    ceiling=phase4.hypothesis_updates(rows,hypotheses)
    assert ceiling["updates"]["H-R4"]["direction"]=="weak_counterevidence"
    assert set(ceiling["updates"])=={"H-R4"}
    assert ceiling["H1_H6"]==ceiling["architecture_C"]==ceiling["H_R1_H_R3"]=="unchanged"
    for row in rows:
        if row["condition"]=="D8":
            row["UU"]=_measurement(16,.75)
    assert phase4.hypothesis_updates(rows,hypotheses)["updates"]["H-R4"]["direction"]=="weak_support"
    # SS advantage cannot replace the preregistered UU advantage.
    for row in rows:
        if row["condition"]=="D8":
            row["UU"]=_measurement(16)
            row["SS"]=_measurement(16,.75)
    assert phase4.hypothesis_updates(rows,hypotheses)["updates"]["H-R4"]["direction"]=="neutral_or_inconclusive"
    rows[0]["status"]="NOT_RUN"
    incomplete=phase4.hypothesis_updates(rows,hypotheses)
    assert not incomplete["eligible"] and incomplete["updates"]["H-R4"]["direction"]=="no_update_ineligible"


def test_worker_rejects_direct_execution_without_external_deadline(prepared_parts,tmp_path,monkeypatch):
    monkeypatch.delenv("LARP_ROLE_ORIENTATION_TOKEN",raising=False)
    with pytest.raises(ValueError,match="external hard supervisor required"):
        phase4.supervised_deadline(tmp_path,prepared_parts[0])


def test_protocol_rejects_extra_updates_or_altered_ss(prepared_parts):
    cfg=copy.deepcopy(prepared_parts[0])
    cfg["updates"]=251
    with pytest.raises(ValueError,match="changed fixed protocol fields"):
        phase4.check_config(cfg)
    cfg=copy.deepcopy(prepared_parts[0])
    cfg["SS"][0]=[58,68,57]
    with pytest.raises(ValueError,match="changed fixed protocol fields"):
        phase4.check_config(cfg)
