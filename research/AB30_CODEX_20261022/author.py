"""Record a human/agent-selected branch; contains no experiment sequence or selector."""
from pathlib import Path
import json
BASE=Path(__file__).resolve().parent
def dump(p,obj):
    with p.open('x',encoding='utf-8') as f: json.dump(obj,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
def cycle(cid,name,question,rivals,intervention,prediction,falsifier,source,budget=120,seeds=None,refs=None):
    folder=BASE/'cycles'/cid;folder.mkdir(exist_ok=False)
    prev=f'C{int(cid[1:])-1:02}'
    protocol={'id':cid,'parent_id':prev,'short_name':name,'date':'2026-10-22',
      'authorization':'User explicitly resumed and requested remaining twenty cycles with ChatRelay available.',
      'A':question,'B':rivals,'C':intervention,
      'D':'Frozen source, inputs and supervisor. Full finite-array results retained. Seeds/conditions are not additional cycles.',
      'estimand':question,'null':rivals[-1], 'predicted_discriminant':prediction,'falsification_rule':falsifier,
      'budget':{'wall_seconds':budget,'threads':2},'rng_seeds':seeds or [8101,8102,8103,8104],
      'source_refs':refs or ['research/AB30_CODEX_20261022/common.py'],
      'holdout_status':'Historical geometries exposed; generated random worlds are within-model evidence, not external confirmation.',
      'selection_exposure':'Question chosen after preceding result/decision; exploratory. No untouched holdout is claimed.'}
    dump(folder/'protocol.json',protocol)
    (folder/'source.py').write_text(source,encoding='utf-8')
def decision(cid,E,F,H,J,next_id,options=None,I=None):
    dump(BASE/'cycles'/cid/'decision.json',{'id':cid,'E':E,'F':F,
      'G':'No external confirmation; historical geometries and/or within-model simulations. No confirmatory p-value claimed.',
      'H':H,'I':I or 'Separate validity, identification, transportability and cost; inference conditional on four geometric realizations.',
      'J':J,'options_rejected':options or [],'recorded_after_result':True,'next_cycle':next_id})
