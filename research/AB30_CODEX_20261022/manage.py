"""Freeze or execute ONE human-selected cycle; no automatic next-cycle scheduler."""
from pathlib import Path
import sys, subprocess, json, hashlib, runpy, time
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[1]
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    action,cid=sys.argv[1:]; folder=BASE/'cycles'/cid
    protocol=json.loads((folder/'protocol.json').read_text(encoding='utf-8'))
    if action=='freeze':
        assert protocol['id']==cid
        if int(cid[1:])>1:
            prev=BASE/'cycles'/f'C{int(cid[1:])-1:02}'/'decision.json'
            assert prev.exists(),'Previous decision must exist before next freeze.'
        subprocess.run(['git','add','--','.gitignore','research/AB30_CODEX_20261022'],cwd=ROOT,check=True)
        subprocess.run(['git','commit','-m',f'research({cid}): freeze {protocol["short_name"]} after prior evidence'],cwd=ROOT,check=True)
        subprocess.run(['git','push','-u','origin','HEAD'],cwd=ROOT,check=True)
        print(json.dumps({'id':cid,'freeze_commit':git('rev-parse','HEAD')}))
    elif action=='run':
        assert not (folder/'result.json').exists(),'Results are immutable; use an explicit repair cycle.'
        # Neither the selected source nor its common instruments may change after freeze.
        for p in [folder/'source.py',folder/'protocol.json',BASE/'common.py',BASE/'manage.py']:
            rel=p.relative_to(ROOT).as_posix()
            assert git('hash-object',str(p))==git('rev-parse',f'HEAD:{rel}'),f'Unfrozen source: {p}'
        start=datetime.now(timezone.utc).isoformat();tic=time.perf_counter()
        ns=runpy.run_path(str(folder/'source.py'))
        result=ns['run']()
        import common
        out={'id':cid,'started_utc':start,'elapsed_seconds':time.perf_counter()-tic,'freeze_commit':git('rev-parse','HEAD'),
             'protocol_sha256':digest(folder/'protocol.json'),'source_sha256':digest(folder/'source.py'),'common_sha256':digest(BASE/'common.py'),
             'environment':common.version_info(),'result':result,'status':'RUN','inference':'exploratory'}
        (folder/'result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        print(json.dumps({'id':cid,'elapsed':out['elapsed_seconds'],'result':result},ensure_ascii=False))
    else:raise ValueError(action)
if __name__=='__main__':main()
