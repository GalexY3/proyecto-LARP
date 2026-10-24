#!/usr/bin/env python3
"""LARP AB20 R2: check full upstream repo pairs with ORIGINAL BugsInPy test oracle.
Historical exact micro versions, full requirements and blind discovery are NOT claimed.
Python stdlib orchestration; every attempt, including failure, saved as a JSON document.
"""
import argparse, hashlib, json, os, re, shlex, shutil, subprocess, sys, time
from pathlib import Path

def run(command, cwd=None, env=None, timeout=100):
    t=time.monotonic()
    try:
        p=subprocess.run(command,cwd=str(cwd) if cwd else None,env=env,
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,
                         timeout=timeout)
        return {"state":"EXIT","code":p.returncode,"elapsed":round(time.monotonic()-t,3),
                "cmd":command,"stdout_tail":p.stdout[-12000:],"stderr_tail":p.stderr[-12000:]}
    except subprocess.TimeoutExpired as e:
        return {"state":"TIMEOUT","code":None,"elapsed":round(time.monotonic()-t,3),
                "cmd":command,"error":str(e)}
    except Exception as e:
        return {"state":"ERROR","code":None,"elapsed":round(time.monotonic()-t,3),
                "cmd":command,"error":repr(e)}

def sha(data): return hashlib.sha256(data).hexdigest()

def exact_test_commands(script):
    """Only execute recognized pytest/unittest commands; tox invocation is adapted to pytest."""
    out=[]
    for raw in script.splitlines():
        line=raw.strip()
        if not line or line.startswith("#"):continue
        try: args=shlex.split(line)
        except ValueError:out.append({"source":line,"unsupported":"TOKENIZATION"});continue
        if not args:continue
        if args[0]=="tox":
            out.append({"source":line,"argv":[sys.executable,"-m","pytest"]+args[1:],
                        "adaptation":"tox interpreted as pytest with same test selector; NOT identical tox env"})
        elif args[0] in ("pytest","py.test"):
            out.append({"source":line,"argv":[sys.executable,"-m","pytest"]+args[1:],
                        "adaptation":"pytest executable -> python -m pytest"})
        elif args[0] in ("python","python3") and args[1:3] in (["-m","pytest"],["-m","unittest"]):
            out.append({"source":line,"argv":[sys.executable]+args[1:],
                        "adaptation":"python shell name -> pinned interpreter"})
        else:
            out.append({"source":line,"unsupported":"UNRECOGNIZED_COMMAND"})
    return out

def has_environment_failure(x):
    s=(x.get("stdout_tail","")+"\n"+x.get("stderr_tail","")).lower()
    bad=["error collecting", "module not found", "modulenotfounderror", "importerror",
         "no module named", "not found:", "no tests ran", "collected 0 items",
         "failed to import", "nameerror: name 'aiohttptestcase'",
         "syntaxerror", "internalerror", "usage error","error during collection"]
    return any(y in s for y in bad)

def failure_is_assertion(x):
    s=(x.get("stdout_tail","")+"\n"+x.get("stderr_tail","")).lower()
    return ("assertionerror" in s or "assert " in s or "failed (failures=" in s or
            bool(re.search(r"\b\d+ failed",s))) and not has_environment_failure(x)

def source_case(c,repo,bench,base_out):
    case={"cycle_id":c["cycle_id"],"id":c["bug_id"],"project":c["project"],
          "buggy_sha":c["buggy_sha"],"fixed_sha":c["fixed_sha"],
          "documented_python":c["documented_python_version"],"actual_python":sys.version.split()[0],
          "full_repo":True,"full_bugsinpy_env":False,"retrospectively_exposed_fix":True,
          "status":"EXECUTION_ATTEMPT","versions":{},
          "A":"Can official targeted fixed-test find bug in original upstream full source?",
          "B":{"H1":"Fail on buggy and pass on fixed with relevant assertion",
               "H0":"No change in outcome","rival":"Dependency, test fixture or Python ABI mismatch"},
          "C":"Twenty fixed BugsInPy IDs, two revisions, fixed-test overlay exactly as BugsInPy checkout",
          "D":"Commit SHA verification, full repo source, test bytes hashes, exact test command",
          "F":"Post-exposure and selected benchmark; installation and failure-cause adverse audit",
          "G":"No independent external environment; GitHub hosted runner only",
          "H":"A failure during test collection is not evidence of bug detection",
          "I":{"grade":0,"CT2_before":8,"CT2_after":8},
          "J":"Continue/repair/stop depending on genuine test outcome"}
    root=Path(bench)/"projects"/c["project"]/"bugs"/str(c["bug_id"])
    tfile=root/"run_test.sh"
    if not tfile.exists():
        case["result"]="OFFICIAL_ORACLE_MISSING"
        return case
    script=tfile.read_text(encoding="utf8",errors="replace")
    commands=exact_test_commands(script)
    case["official_run_test_sha256"]=sha(tfile.read_bytes())
    case["official_commands"]=commands
    testpaths=[p for p in c["test_file"].split(";") if p]
    if any("unsupported" in p for p in commands) or not commands or not testpaths:
        case["result"]="OFFICIAL_COMMAND_UNSUPPORTED";return case
    # Copy the fixed revision's ORIGINAL test sources BEFORE changing into buggy revision.
    fix=run(["git","-c","advice.detachedHead=false","checkout","-f",c["fixed_sha"]],cwd=repo,timeout=65)
    if fix["code"]!=0:
        case["result"]="FIXED_CHECKOUT_BLOCKED";case["fixed_checkout"]=fix;return case
    if run(["git","rev-parse","HEAD"],cwd=repo)["stdout_tail"].strip()!=c["fixed_sha"]:
        case["result"]="FIXED_SHA_MISMATCH";return case
    overlay={}
    for path in testpaths:
        p=repo/path
        if not p.is_file():
            case["result"]="FIXED_TEST_SOURCE_ABSENT";case["absent"]=path;return case
        overlay[path]=p.read_bytes()
    case["overlaid_fixed_test_sha256"]={p:sha(v) for p,v in overlay.items()}
    for label,target in [("buggy",c["buggy_sha"]),("fixed",c["fixed_sha"])]:
        v={"sha_expected":target,"test_script_sha256":case["official_run_test_sha256"]}
        step=run(["git","-c","advice.detachedHead=false","checkout","-f",target],cwd=repo,timeout=65)
        v["checkout"]=step
        if step["code"]!=0:
            v["reason"]="CHECKOUT_FAILED";case["versions"][label]=v;continue
        head=run(["git","rev-parse","HEAD"],cwd=repo)
        v["sha_actual"]=head["stdout_tail"].strip()
        if v["sha_actual"]!=target:
            v["reason"]="SHA_MISMATCH";case["versions"][label]=v;continue
        # Like official BugsInPy checkout: carry tests added by fixed commit into buggy.
        if label=="buggy":
            for path,data in overlay.items():
                destination=repo/path
                destination.parent.mkdir(parents=True,exist_ok=True)
                destination.write_bytes(data)
            v["test_overlay_from_fixed"]=True
        else:v["test_overlay_from_fixed"]=False
        v["test_bytes"]={p:sha((repo/p).read_bytes()) for p in overlay}
        ins=run([sys.executable,"-m","pip","install","--disable-pip-version-check","-q",
                 "--no-build-isolation","-e",str(repo)],cwd=repo,timeout=125)
        v["editable_install"]=ins
        if ins["code"]!=0:
            v["reason"]="INSTALL_FAILED";case["versions"][label]=v;continue
        env=os.environ.copy()
        env["PYTHONPATH"]=str(repo)
        env["PYTHONDONTWRITEBYTECODE"]="1"
        v["tests"]=[]
        for cmd in commands:
            outcome=run(cmd["argv"],cwd=repo,env=env,timeout=55)
            outcome["source_command"]=cmd["source"]
            outcome["adaptation"]=cmd.get("adaptation")
            outcome["environment_error"]=has_environment_failure(outcome)
            outcome["assertion_failure"]=failure_is_assertion(outcome)
            v["tests"].append(outcome)
        case["versions"][label]=v
    a=case["versions"].get("buggy",{}).get("tests",[])
    b=case["versions"].get("fixed",{}).get("tests",[])
    if a and b and len(a)==len(b) and all(t["state"]=="EXIT" for t in a+b):
        envs=any(t["environment_error"] for t in a+b)
        fixed_ok=all(t["code"]==0 for t in b)
        buggy_assert=any(t["code"]!=0 and t["assertion_failure"] for t in a)
        if not envs and fixed_ok and buggy_assert:
            case["result"]="CANDIDATE_REPRODUCED_AUDIT_TRACE_REQUIRED"
        elif not envs and fixed_ok and all(t["code"]==0 for t in a):
            case["result"]="BOTH_PASS_NON_REPRODUCED"
        else:
            case["result"]="INCONCLUSIVE_ERRORS_OR_FIXED_FAILURE"
    else:case["result"]="INSTRUMENT_BLOCKED"
    case["E"]=case["versions"]
    return case

def main():
    p=argparse.ArgumentParser();p.add_argument("--project",required=True)
    p.add_argument("--manifest",default="research/AB20_FULLRUNTIME_20261024/PREREG_COHORT_20.json")
    p.add_argument("--out",default="research/AB20_FULLRUNTIME_20261024/results_r2")
    args=p.parse_args()
    m=json.load(open(args.manifest))
    cases=[x for x in m["cases"] if x["project"]==args.project]
    output=Path(args.out);output.mkdir(parents=True,exist_ok=True)
    work=Path("/tmp/larp_historical_r2");work.mkdir(exist_ok=True)
    print("R2 BEGIN",args.project,"n",len(cases),"python",sys.version,flush=True)
    benchmark=work/"BugsInPy"
    if not benchmark.exists():
        bn=run(["git","clone","--quiet","--depth","1",
                "https://github.com/soarsmu/BugsInPy.git",str(benchmark)],timeout=160)
    else:bn={"code":0,"state":"CACHE_LOCAL"}
    repo=work/("upstream_"+args.project)
    if repo.exists():shutil.rmtree(str(repo))
    co=run(["git","clone","--quiet","--no-checkout",cases[0]["upstream_url"]+".git",
            str(repo)],timeout=170)
    # Stable test harness for target Python; extra *test dependencies*, no claim of historical full requirements.
    dep=["pytest==5.4.3" if sys.version_info[:2]==(3,6) else "pytest==6.2.5",
         "pytest-mock==3.6.1","six","nose","mock","wheel==0.37.1"]
    if args.project=="PySnooper":dep+=["python_toolbox"]
    if args.project=="black":dep+=["aiohttp==3.6.3","aiohttp-cors==0.7.0","click==7.1.2"]
    if args.project=="cookiecutter":dep+=["click==7.1.2","pytest-cov==2.12.1"]
    setup=run([sys.executable,"-m","pip","install","--disable-pip-version-check","-q"]+dep,
              timeout=170)
    log={"project":args.project,"runner":sys.version,"bench_clone":bn,
         "repo_clone":co,"setup":setup,"installed_test_dependencies":dep,
         "deviations":["Python micro may differ from bug.info",
                       "Curated full requirements were not installed exactly",
                       "Fixed version's test files overlaid onto buggy per BugsInPy",
                       "tox test command translated to pytest when necessary"]}
    (output/(args.project+"_SETUP.json")).write_text(json.dumps(log,indent=2),encoding="utf8")
    for c in cases:
        if bn.get("code")!=0 or co["code"]!=0 or setup["code"]!=0:
            result={"cycle_id":c["cycle_id"],"project":args.project,"status":"NOT_EXECUTED",
                    "result":"ENVIRONMENT_BLOCKED",
                    "blockers":{"bench_clone":bn.get("code"),"upstream_clone":co.get("code"),"setup":setup.get("code")}}
        else:
            result=source_case(c,repo,benchmark,output)
        (output/(c["cycle_id"]+".json")).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf8")
        print(c["cycle_id"],result["result"],flush=True)
    print("R2 END",args.project,flush=True)

if __name__=="__main__":
    main()
