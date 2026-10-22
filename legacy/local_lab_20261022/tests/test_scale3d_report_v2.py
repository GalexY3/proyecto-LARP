import json
from larp.scale3d_report_v2 import write_report,SIZES,SEEDS


def test_v2_report_uses_fresh_seeds_and_marks_scope(tmp_path):
    records=[]
    for N in SIZES:
        for seed in SEEDS:
            scores={arm:[{'task':t,'MSE':value} for t in range(3)]
                    for arm,value in [('mhu',.2),('local',.3),('random',.4)]}
            records.append({'N':N,'seed':seed,'status':'COMPLETE','training_updates':1800,
                'evaluations':[{'step':1800,'scores':scores}]})
    result=write_report({'status':'COMPLETE','common_scale_endpoint':1800,'records':records},tmp_path)
    assert SEEDS==(3201,3202) and result['global_scale_eligible']
    text=(tmp_path/'SUMMARY.md').read_text(encoding='utf-8')
    assert 'v2' in text and 'CIC puede inducir orden de rejilla' in text


def test_old_seeds_cannot_supply_v2_scale_coverage(tmp_path):
    result=write_report({'common_scale_endpoint':1800,'records':[
        {'N':N,'seed':seed,'status':'COMPLETE','training_updates':1800} for N in SIZES for seed in (3101,3102)]},tmp_path)
    assert not result['global_scale_eligible'] and result['comparison_rows']==0
