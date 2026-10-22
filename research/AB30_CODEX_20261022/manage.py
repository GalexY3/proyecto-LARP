"""Freeze/run one cycle with immutable receipts, source locks and worker timeout."""
from pathlib import Path
from datetime import datetime,timezone
import sys,subprocess,json,hashlib,runpy,time,os,re,traceback,contextlib,math
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[1]
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write_new(p,obj):
    text=json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    with p.open('x',encoding='utf-8') as f:f.write(text)
def sources(folder):return [folder/'source.py',folder/'protocol.json',BASE/'common.py',BASE/'manage.py']
def geohashes():return {p.relative_to(ROOT).as_posix():digest(p) for p in sorted((ROOT/'data/AB06_REALDATA_20261022').glob('geo_*.npz'))}
def verify(folder):
    lock=json.loads((folder/'freeze.json').read_text(encoding='utf-8'))
    for p in sources(folder):
        rel=p.relative_to(ROOT).as_posix()
        if digest(p)!=lock['source_sha256'][rel]:raise RuntimeError(f'Changed source: {rel}')
        blob=subprocess.check_output(['git','show',f'{lock["freeze_commit"]}:{rel}'],cwd=ROOT)
        if blob.replace(b'\r\n',b'\n')!=p.read_bytes().replace(b'\r\n',b'\n'):raise RuntimeError(f'Not frozen: {rel}')
    if geohashes()!=lock['geometry_sha256']:raise RuntimeError('Changed geometry inputs')
    parent=lock.get('parent_decision')
    if parent and digest(ROOT/parent['path'])!=parent['sha256']:raise RuntimeError('Changed parent decision')
    return lock
def worker(folder):
    out={'status':'FAILED','result':{},'inputs':{},'environment':{}}
    try:
        verify(folder)
        with contextlib.redirect_stdout(sys.stderr):
            import common
            out['environment']=common.version_info();out['inputs']={'geometry_sha256':geohashes(),'datasets':[]}
            original=common.dataset
            def tracked(*args,**kwargs):
                arrays=original(*args,**kwargs)
                out['inputs']['datasets'].append({'args':repr(args),'kwargs':repr(kwargs),'arrays':{n:{'shape':list(a.shape),'dtype':str(a.dtype),'sha256':hashlib.sha256(common.np.ascontiguousarray(a).tobytes()).hexdigest()} for n,a in zip(['images','labels','train','validation','test'],arrays)}})
                return arrays
            common.dataset=tracked;tracked()
            result=runpy.run_path(str(folder/'source.py'))['run']()
            if not isinstance(result,dict):raise TypeError('run() must return dict')
            out.update(result=result,status='COMPLETED')
    except BaseException:out['error']=traceback.format_exc()
    print(json.dumps(out,ensure_ascii=False,allow_nan=False));return int(out['status']!='COMPLETED')
def stop(process):
    if process.poll() is None:
        if os.name=='nt':subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True)
        if process.poll() is None:process.kill()
        process.communicate(timeout=10)
def execute(folder,protocol):
    if (folder/'result.json').exists():raise RuntimeError('Immutable result exists; use repair cycle')
    tic=time.perf_counter();process=None
    out={'id':protocol['id'],'started_utc':datetime.now(timezone.utc).isoformat(),'status':'FAILED','inference':'exploratory','result':{}}
    try:
        lock=verify(folder);out.update(freeze_commit=lock['freeze_commit'],parent_decision=lock.get('parent_decision'),protocol_sha256=digest(folder/'protocol.json'),source_sha256=digest(folder/'source.py'),common_sha256=digest(BASE/'common.py'))
        seconds=float(protocol['budget']['wall_seconds'])
        if not math.isfinite(seconds) or seconds<=0:raise ValueError('Invalid wall budget')
        options={'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {}
        process=subprocess.Popen([sys.executable,str(BASE/'manage.py'),'--worker',protocol['id']],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',env={**os.environ,'PYTHONUTF8':'1'},**options)
        output,errors=process.communicate(timeout=max(.001,seconds-(time.perf_counter()-tic)))
        out.update(json.loads(output));out['worker_returncode']=process.returncode
        if errors:out['worker_stderr_tail']=errors[-12000:]
        if process.returncode and out['status']=='COMPLETED':out.update(status='FAILED',error='Nonzero worker exit')
    except subprocess.TimeoutExpired:
        stop(process);out.update(status='BUDGET_EXCEEDED',error='Worker tree stopped at wall budget')
    except KeyboardInterrupt:
        if process is not None:stop(process)
        out.update(status='INTERRUPTED',error='Interrupted by caller')
    except BaseException:
        if process is not None:stop(process)
        out['error']=traceback.format_exc()
    finally:
        out.update(elapsed_seconds=time.perf_counter()-tic,finished_utc=datetime.now(timezone.utc).isoformat());write_new(folder/'result.json',out)
    result=out['result'];print(json.dumps({'id':out['id'],'status':out['status'],'elapsed':out['elapsed_seconds'],'result':result.get('summary',{'keys':list(result)}),'error':out.get('error')},ensure_ascii=False))
    return int(out['status']!='COMPLETED')
def main():
    if len(sys.argv)!=3 or sys.argv[1] not in ['freeze','run','--worker'] or not re.fullmatch(r'C\d{2}',sys.argv[2]):raise SystemExit('Usage: manage.py freeze|run Cnn')
    action,cid=sys.argv[1:];folder=BASE/'cycles'/cid;protocol=json.loads((folder/'protocol.json').read_text(encoding='utf-8'))
    if protocol['id']!=cid:raise ValueError('Protocol ID mismatch')
    if action=='--worker':return worker(folder)
    if action=='run':return execute(folder,protocol)
    if (folder/'freeze.json').exists() or (folder/'result.json').exists():raise RuntimeError('Already frozen/executed')
    parent=None
    if int(cid[1:])>1:
        prev=BASE/'cycles'/f'C{int(cid[1:])-1:02}'/'decision.json'
        if not prev.exists():raise RuntimeError('Previous decision required')
        parent={'path':prev.relative_to(ROOT).as_posix(),'sha256':digest(prev)}
    paths=[*sources(folder),ROOT/'.gitignore',BASE/'README.md',BASE/'requirements-extra.txt']
    if parent:paths += [p for p in prev.parent.iterdir() if p.is_file()]
    paths=[p.relative_to(ROOT).as_posix() for p in paths if p.exists()]
    if set(git('diff','--cached','--name-only').splitlines())-set(paths):raise RuntimeError('Unrelated files staged')
    subprocess.run(['git','-c','core.safecrlf=false','add','--',*paths],cwd=ROOT,check=True,capture_output=True)
    subprocess.run(['git','commit','-m',f'research({cid}): freeze {protocol["short_name"]} after prior evidence'],cwd=ROOT,check=True,capture_output=True)
    lock={'id':cid,'freeze_commit':git('rev-parse','HEAD'),'parent_decision':parent,'source_sha256':{p.relative_to(ROOT).as_posix():digest(p) for p in sources(folder)},'geometry_sha256':geohashes()}
    subprocess.run(['git','push','-u','origin','HEAD'],cwd=ROOT,check=True,capture_output=True)
    lock['pushed_utc']=datetime.now(timezone.utc).isoformat();write_new(folder/'freeze.json',lock)
    print(json.dumps({'id':cid,'freeze_commit':lock['freeze_commit']}));return 0
if __name__=='__main__':raise SystemExit(main())
