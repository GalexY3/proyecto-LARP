#!/usr/bin/env python3
"""AB20 historical FULL repo checkout audit. NOT a mutation or patch-hunk simulator.
This script must be run from the campaign repository root with project and manifest args.
Exit 0 denotes successful archiving of attempts, never scientific success.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

def execute(cmd, cwd=None, timeout=70, env=None):
    started=time.monotonic()
    try:
        p=subprocess.run(cmd,cwd=str(cwd) if cwd else None,env=env,capture_output=True,text=True,
                         errors="replace",timeout=timeout)
        return dict(status="EXIT",code=p.returncode,seconds=round(time.monotonic()-started,3),
                    stdout=p.stdout[-14000:],stderr=p.stderr[-14000:],command=cmd)
    except subprocess.TimeoutExpired as e:
        return dict(status="TIMEOUT",code=None,seconds=round(time.monotonic()-started,3),
                    stdout=str(e.stdout)[-4000:],stderr=str(e.stderr)[-4000:],command=cmd)
    except Exception as e:
        return dict(status="ERROR",code=None,seconds=round(time.monotonic()-started,3),
                    error=repr(e),command=cmd)

def record_case(c,repo,python):
    z={"cycle_id":c["cycle_id"],"project":c["project"],"bug_id":c["bug_id"],
       "repo":c["upstream_url"],"expected_buggy":c["buggy_sha"],"expected_fixed":c["fixed_sha"],
       "documented_python":c["documented_python_version"],
       "actual_python":sys.version.split()[0],"case_source":"BugsInPy bug.info","test_file":c["test_file"],
       "status":"ATTEMPTED_FULL_CHECKOUT","versions":{},"retrospective_fix_exposure":True,
       "AB": {"A":"Whole historical package and test-file buggy/fixed parity",
              "B":"Repair should address a failing test; H0 no separable status; rival missing deps",
              "C":"Identical test selection and instrument in both upstream revisions",
              "D":"Workflow Python version approximation, git checkout and editable install",
              "F":"Known patch and developer's test file; unblinded, selected bugs",
              "G":"No external independent confirmation; same runner two revisions",
              "H":"Metadata and patch-level execution cannot establish historical full-package parity",
              "I":{"grade":0,"CT2_before":8,"CT2_after":8},
              "J":"Stop or repair instrumentation based on observed errors"}}
    for label,sha in [("buggy",c["buggy_sha"]),("fixed",c["fixed_sha"])]:
        v={"sha_requested":sha,"eligible":False}
        co=execute(["git","-c","advice.detachedHead=false","checkout","-f",sha],cwd=repo,timeout=55)
        v["checkout"]=co
        if co["code"] != 0:
            z["versions"][label]=v
            continue
        head=execute(["git","rev-parse","HEAD"],cwd=repo,timeout=15)
        v["sha_actual"]=head.get("stdout","").strip()
        if v["sha_actual"] != sha:
            v["error"]="COMMIT_MISMATCH"
            z["versions"][label]=v
            continue
        v["checkout_verified"]=True
        path=c["test_file"].split(";")[0]
        target=repo / path
        v["test_file_exists"]=target.is_file()
        if not target.is_file():
            v["error"]="TEST_FILE_ABSENT"
            z["versions"][label]=v
            continue
        # Reinstall package on each revision; avoid silently testing system installed packages.
        ins=execute([python,"-m","pip","install","--disable-pip-version-check","-q","-e",str(repo)],
                    cwd=repo,timeout=135)
        v["install"]=ins
        if ins["code"]!=0:
            v["error"]="INSTALL_FAILED"
            z["versions"][label]=v
            continue
        env=os.environ.copy()
        env["PYTHONPATH"]=str(repo)
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"]="1"
        tst=execute([python,"-m","pytest","-x","-q",path,"--disable-warnings"],
                    cwd=repo,timeout=65,env=env)
        v["test"]=tst
        v["eligible"]=tst["status"]=="EXIT"
        z["versions"][label]=v
    a=z["versions"].get("buggy",{}); b=z["versions"].get("fixed",{})
    ta=a.get("test",{});tb=b.get("test",{})
    if ta.get("code") not in [None,0] and tb.get("code")==0 and ta.get("status")==tb.get("status")=="EXIT":
        z["result"]="CANDIDATE_BUGGY_FAIL_FIXED_PASS_CHECK_FAILURE_CAUSE"
    elif ta.get("code")==0 and tb.get("code")==0:
        z["result"]="BOTH_PASS_BUG_NOT_REPRODUCED"
    elif a.get("checkout_verified") and b.get("checkout_verified") and ta.get("status")=="EXIT" and tb.get("status")=="EXIT":
        z["result"]="TEST_RUN_INCONCLUSIVE"
    else:
        z["result"]="INSTRUMENT_BLOCKED_OR_TIMEOUT"
    z["AB"]["E"]=z["versions"]
    z["AB"]["I"]["grade"]=0
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",required=True)
    ap.add_argument("--manifest",default="research/AB20_FULLRUNTIME_20261024/PREREG_COHORT_20.json")
    ap.add_argument("--out",default="research/AB20_FULLRUNTIME_20261024/results")
    args=ap.parse_args()
    manifest=json.load(open(args.manifest,encoding="utf8"))
    cases=[x for x in manifest["cases"] if x["project"]==args.project]
    if not cases: raise SystemExit("No cases for "+args.project)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    print("LARP AB20 AUDIT project",args.project,"cases",len(cases),"python",sys.version,flush=True)
    if "3.8" not in sys.version: print("WARNING Python may differ from original.",flush=True)
    work=Path("/tmp/larp_abhistorical")/args.project; work.parent.mkdir(exist_ok=True)
    if work.exists():shutil.rmtree(work)
    # Clone the FULL upstream repository, no reconstructed source snippets.
    clone=execute(["git","clone","--quiet","--no-checkout",cases[0]["upstream_url"]+".git",str(work)],timeout=190)
    if clone["code"] != 0:
        for c in cases:
            z={"cycle_id":c["cycle_id"],"project":args.project,
               "status":"NOT_EXECUTED","result":"FULL_CHECKOUT_FAILED","clone":clone,
               "AB_A_J_complete":False,"grade":0}
            (out/(c["cycle_id"]+".json")).write_text(json.dumps(z,indent=2,ensure_ascii=False))
        print("CHECKOUT FAILED",clone.get("stderr","")[-2000:],flush=True)
        return
    # pip/pytest may not be supported for all old projects in one current Python environment.
    version_setup=execute([sys.executable,"-m","pip","install","--disable-pip-version-check","-q",
                           "pytest==6.2.5","six","mock","nose","pytest-mock==3.6.1"],
                          timeout=145)
    (out/(args.project+"_SETUP.json")).write_text(json.dumps({"clone":clone,"pytest_setup":version_setup},indent=2))
    for c in cases:
        if version_setup["code"]!=0:
            z={"cycle_id":c["cycle_id"],"project":args.project,"result":"PYTEST_SETUP_FAILED",
               "status":"NOT_EXECUTED","setup":version_setup,"grade":0}
        else:
            z=record_case(c,work,sys.executable)
        (out/(c["cycle_id"]+".json")).write_text(json.dumps(z,indent=2,ensure_ascii=False))
        print(c["cycle_id"],z["result"],flush=True)
    print("CASE_JSON_COUNTS",len(cases),flush=True)

if __name__=="__main__":
    main()
