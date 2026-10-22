"""CLI: explicit execution flags, readable gates and no long default jobs."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from .config import ROOT, load_profile
from .artifacts import write_json, json_safe, code_identity
from . import runner


def parser():
    p = argparse.ArgumentParser(description="LARP v0.1: gated, paired, CPU research experiment")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("test", help="Run all bounded tests, log JUnit and refresh code-specific gate")
    g = sub.add_parser("validate-geometry")
    g.add_argument("--N", type=int, default=400, choices=[400,1600,6400])
    g.add_argument("--seed", type=int, default=1101)
    for name in ["calibrate", "smoke", "pilot", "fill", "screen"]:
        s = sub.add_parser(name)
        s.add_argument("--execute", action="store_true", help="Otherwise show dry-run plan only")
        s.add_argument("--resume", action="store_true")
        s.add_argument("--directory", type=Path)
        if name in {"pilot", "screen"}:
            s.add_argument("--task", choices=["copy","fill"], default="copy")
        if name == "screen":
            s.add_argument("--ecological", action="store_true")
    for name in ["freeze-confirmation", "confirm"]:
        c = sub.add_parser(name)
        c.add_argument("--task", choices=["copy","fill"], required=True)
        c.add_argument("--baseline", default="grid_balanced", choices=["grid_balanced","hu","small_world","random_regular","poisson"], help="Dry-run placeholder; executed plan uses frozen screen selection")
        c.add_argument("--execute", action="store_true")
        c.add_argument("--resume", action="store_true")
        c.add_argument("--directory", type=Path)
        if name == "confirm":
            c.add_argument("--extension", action="store_true")
    for name in ["robustness", "scale"]:
        r = sub.add_parser(name)
        r.add_argument("--run", type=Path, required=True)
        r.add_argument("--output", type=Path, required=True)
        r.add_argument("--execute", action="store_true")
        if name == "robustness":
            r.add_argument("--kind", choices=["random","lesion","radius","type","edge","relocation","m1","functions"], default="random")
            r.add_argument("--unprotected", action="store_true")
        else:
            r.add_argument("--geometries", type=Path, nargs=3, help="Three already-certified new N1600 substrate archives")
    a = sub.add_parser("analyze")
    a.add_argument("--records", type=Path)
    a.add_argument("--output", type=Path, default=ROOT / "artifacts" / "analysis.json")
    a.add_argument("--control", default="shuffle")
    a.add_argument("--estimand", choices=["marks","architecture"], default="marks")
    report = sub.add_parser("report")
    report.add_argument("--run-root", type=Path, default=ROOT / "runs")
    report.add_argument("--output", type=Path, default=ROOT / "artifacts" / "report")
    resume = sub.add_parser("resume")
    resume.add_argument("--run", type=Path, required=True)
    failure = sub.add_parser("verify-failure")
    failure.add_argument("--run", type=Path, required=True)
    failure.add_argument("--execute", action="store_true")
    return p


def run_tests():
    log_dir = ROOT / "artifacts" / "tests"
    log_dir.mkdir(parents=True, exist_ok=True)
    begin = time.perf_counter()
    result = subprocess.run([sys.executable,"-m","pytest","-q","--junitxml",str(log_dir / "junit.xml")],
                            cwd=ROOT, capture_output=True, text=True)
    (log_dir / "pytest.log").write_text(result.stdout+result.stderr, encoding="utf-8")
    print(result.stdout, end="")
    tree = ET.parse(log_dir / "junit.xml")
    suites = list(tree.getroot().iter("testsuite"))
    totals = {key: sum(int(s.attrib.get(key,0)) for s in suites) for key in ["tests","failures","errors","skipped"]}
    gate = runner.record_gate("scientific_tests", result.returncode==0 and totals["tests"]>0 and totals["skipped"]==0,
                             counts=totals, seconds=time.perf_counter()-begin, log=str(log_dir / "pytest.log"))
    if result.returncode:
        raise RuntimeError("Tests failed; later scientific gates closed")
    return gate


def resume_run(path):
    import numpy as np
    from .geometry import Geometry
    from .training import train_run
    manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
    runner.require_gates("scientific_tests", "geometry")
    result_path = path / "results.json"
    if result_path.exists():
        status = json.loads(result_path.read_text(encoding="utf-8"))["status"]
        if status == "NUMERICAL_FAILURE_UNVERIFIED":
            raise RuntimeError("Use verify-failure from original initialization, not resume past nonfinite episode")
        if status == "TRAINING_DIVERGENCE":
            raise RuntimeError("Verified divergence is immutable evidence; never resume to replace it")
    cfg = manifest["config"]
    if cfg["stage"] in {"smoke", "pilot", "confirmation"}:
        runner.require_gates("calibration")
    if cfg["stage"] in {"pilot", "confirmation"}:
        runner.require_gates("smoke")
    if cfg["task"] == "fill" and cfg["stage"] in {"pilot", "confirmation"}:
        runner.require_gates("pilot_copy")
    if cfg["stage"] == "confirmation":
        runner.require_gates("pilot_copy", "screen_"+cfg["task"])
        if cfg["task"] == "fill": runner.require_gates("fill_fill")
        candidates = [ancestor / "frozen_confirmation.json" for ancestor in path.parents]
        frozen_path = next((p for p in candidates if p.exists()),None)
        if frozen_path is None:
            raise RuntimeError("Confirmation resume requires frozen HPO selection")
        frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
        from .artifacts import digest
        if digest(frozen["plan"]) != frozen["plan_hash"] or frozen["code"]["source_hash"] != code_identity(ROOT)["source_hash"]:
            raise RuntimeError("Frozen confirmation identity mismatch")
        if cfg not in frozen["plan"]["configs"]:
            raise RuntimeError("This run is absent from the frozen initial confirmation panel")
    return train_run(cfg, Geometry.load(path / "geometry.npz"), np.load(path / "edges.npy"), path,
                     resume=True, preregistered=manifest["preregistered"],
                     open_test=cfg["stage"] in {"pilot","confirmation"})


def verify_failure(path):
    import numpy as np
    from .geometry import Geometry
    from .training import train_run
    runner.require_gates("scientific_tests", "geometry")
    original = json.loads((path / "results.json").read_text(encoding="utf-8"))
    manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
    if original["status"] != "NUMERICAL_FAILURE_UNVERIFIED":
        raise ValueError("Not an unverified numerical failure")
    if manifest["code"]["source_hash"] != code_identity(ROOT)["source_hash"]:
        raise ValueError("Same code required to verify reproducible failure")
    replay = train_run(manifest["config"], Geometry.load(path / "geometry.npz"), np.load(path / "edges.npy"),
                       path / "failure_replay", preregistered=manifest["preregistered"])
    verified = replay["status"] == original["status"] and replay["updates_completed"] == original["updates_completed"]
    evidence = {"reproduction_verified": verified, "replay": replay["experiment_id"],
                "reason": "Same code/init/data/order, finite health tests, same first failing update",
                "infrastructure_excluded": verified}
    write_json(path / "failure_verification.json", evidence)
    if verified:
        original.update(status="TRAINING_DIVERGENCE", divergence_verified=True, infrastructure_excluded=True, score=0.0,
                        score_split="test" if manifest["config"]["stage"]=="confirmation" else "validation")
        write_json(path / "results.json", original)
    return evidence


def dispatch(args):
    command = args.command
    if command == "test": return run_tests()
    if command == "validate-geometry": return runner.validate_geometry(args.N,args.seed)
    if command == "calibrate":
        return runner.calibration(args.directory,resume=args.resume) if args.execute else {"stage":"calibration","measured_updates":200,"warmup_updates":5,"requires":["scientific_tests","geometry"],"test_opened":False}
    if command == "smoke":
        return runner.smoke(args.directory,resume=args.resume) if args.execute else load_profile("smoke")
    if command in {"pilot","fill","screen"}:
        task = getattr(args,"task","fill" if command=="fill" else "copy")
        kwargs = {"ecological":getattr(args,"ecological",False)}
        return runner.execute_stage(command,task,args.directory,resume=args.resume,**kwargs) if args.execute else runner.plan_stage(command,task,**kwargs)
    if command in {"confirm","freeze-confirmation"}:
        if not args.execute:
            return runner.confirmation_plan(args.task,args.baseline,hpo=command=="freeze-confirmation",extension=getattr(args,"extension",False))
        return runner.freeze_confirmation(args.task,directory=args.directory,resume=args.resume) if command=="freeze-confirmation" else runner.confirm(args.task,directory=args.directory,resume=args.resume,extension=args.extension)
    if command == "analyze":
        from .analysis import initial_beliefs, analyze_records
        if not args.records:
            result = initial_beliefs()
        else:
            records = json.loads(args.records.read_text(encoding="utf-8"))
            if any(r["stage"] not in {"confirmation","robustness"} for r in records):
                result = {"status":"DESCRIPTIVE_ONLY","architecture_beliefs_updated":False,"record_count":len(records),
                          "reason":"Technical/smoke/pilot evidence cannot update architectural priors","priors":initial_beliefs()}
            else:
                if any(r.get("preregistered") is not True for r in records):
                    raise ValueError("A frozen preregistration is required for every supplied record")
                contrast = [r for r in records if r.get("condition") in {"native",args.control}]
                excluded = sorted({r.get("condition") for r in records if r.get("condition") not in {"native",args.control}})
                result = analyze_records(contrast,control_condition=args.control,estimand=args.estimand)
                result["excluded_conditions_from_selected_contrast"] = excluded
        write_json(args.output,result)
        return result
    if command == "report":
        from .reporting import summarize
        return summarize(args.run_root,args.output)
    if command == "resume": return resume_run(args.run)
    if command == "verify-failure":
        return verify_failure(args.run) if args.execute else {"stage":"failure_reproduction","run":str(args.run),"automatic":False}
    if command in {"robustness","scale"}:
        from .interventions import run_robustness, run_scale
        runner.require_gates("scientific_tests","geometry","smoke") if args.execute else None
        if command == "robustness":
            return run_robustness(args.run,args.output,kind=args.kind,dry_run=not args.execute,protect_ports=False if args.unprotected else None)
        return run_scale(args.run,args.output,scale_geometry_paths=args.geometries,dry_run=not args.execute)
    raise ValueError(command)


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        result = dispatch(args)
        # Full evidence remains in artifacts; concise CLI records reference paths.
        if isinstance(result,list):
            result = {"count":len(result),"statuses":[r.get("status") for r in result]}
        print(json.dumps(json_safe(result),ensure_ascii=False,indent=2,allow_nan=False))
        return 0
    except (ValueError,RuntimeError,FileNotFoundError,FileExistsError) as error:
        print(f"BLOCKED: {error}",file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
