#!/usr/bin/env python
"""
Deterministic staged optimization runner.

Consumes a staged space definition (JSON or YAML), runs optimizer_v0 per stage,
and emits standardized artifacts per stage and at workflow root.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.workflow.artifacts import (
    build_manifest,
    config_hash,
    ensure_dir,
    render_simple_report,
    sha256_file,
    write_manifest,
    write_report,
    write_results,
)


def _load_stage_def(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Stages file not found: {path}")

    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except Exception as exc:
            raise RuntimeError("YAML stages file requested but PyYAML is not installed.") from exc
        return yaml.safe_load(path.read_text(encoding="utf-8-sig"))

    return json.loads(path.read_text(encoding="utf-8-sig"))


def _run_checked(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def _stage_run(
    *,
    stage: dict[str, Any],
    case_path: Path,
    outdir: Path,
    base_seed: int,
    workers: int,
    reuse_cache: bool,
) -> dict[str, Any]:
    name = str(stage.get("name", "stage"))
    mode = str(stage.get("mode", "random")).lower()
    iters = int(stage.get("iters", 50))
    top_k = int(stage.get("top_k", 10))
    seed = int(stage.get("seed", base_seed))
    seed_offset = int(stage.get("seed_offset", 0))
    stage_seed = seed + seed_offset

    stage_dir = ensure_dir(outdir / name)
    stage_results = stage_dir / "results.json"

    stage_fingerprint = config_hash(
        {
            "stage": stage,
            "case": str(case_path),
            "case_hash": sha256_file(case_path),
            "seed": stage_seed,
            "workers": workers,
        }
    )

    if reuse_cache and stage_results.exists():
        try:
            cached = json.loads(stage_results.read_text(encoding="utf-8"))
            if cached.get("stage_fingerprint") == stage_fingerprint and cached.get("status") == "PASS":
                cached["cache_used"] = True
                return cached
        except Exception:
            pass

    db = stage_dir / "results.db"
    trials = stage_dir / "trials.csv"
    pareto = stage_dir / "pareto.json"
    candidates_dir = ensure_dir(stage_dir / "candidates")

    run_cmd = [
        sys.executable,
        "-m",
        "src.optimizer_v0",
        "run",
        "--case",
        str(case_path),
        "--mode",
        mode,
        "--seed",
        str(stage_seed),
        "--workers",
        str(workers),
        "--db",
        str(db),
        "--out",
        str(trials),
        "--pareto-out",
        str(pareto),
    ]
    if mode in {"random", "bayes"}:
        run_cmd.extend(["--iters", str(iters)])
    if stage.get("space_file"):
        run_cmd.extend(["--space-file", str(stage["space_file"])])
    if stage.get("objectives"):
        run_cmd.extend(["--objectives", str(stage["objectives"])])

    rc, out, err = _run_checked(run_cmd, PROJECT_ROOT)
    if rc != 0:
        payload = {
            "stage": name,
            "status": "FAIL",
            "reason": "optimizer_run_failed",
            "return_code": rc,
            "stdout": out,
            "stderr": err,
            "stage_fingerprint": stage_fingerprint,
            "cache_used": False,
        }
        write_results(stage_dir, payload)
        return payload

    export_cmd = [
        sys.executable,
        "-m",
        "src.optimizer_v0",
        "export-candidates",
        "--pareto",
        str(pareto),
        "--outdir",
        str(candidates_dir),
        "--top-k",
        str(top_k),
        "--overwrite",
    ]
    rc2, out2, err2 = _run_checked(export_cmd, PROJECT_ROOT)
    if rc2 != 0:
        payload = {
            "stage": name,
            "status": "FAIL",
            "reason": "candidate_export_failed",
            "return_code": rc2,
            "stdout": out2,
            "stderr": err2,
            "stage_fingerprint": stage_fingerprint,
            "cache_used": False,
        }
        write_results(stage_dir, payload)
        return payload

    pareto_count = 0
    try:
        pj = json.loads(pareto.read_text(encoding="utf-8"))
        pareto_count = len(pj.get("items", []))
    except Exception:
        pareto_count = 0

    payload = {
        "stage": name,
        "status": "PASS",
        "mode": mode,
        "iters": iters,
        "seed": stage_seed,
        "workers": workers,
        "top_k": top_k,
        "space_file": str(stage.get("space_file", "")),
        "stage_fingerprint": stage_fingerprint,
        "pareto_count": pareto_count,
        "cache_used": False,
        "artifacts": {
            "db": str(db),
            "trials_csv": str(trials),
            "pareto_json": str(pareto),
            "candidates_dir": str(candidates_dir),
        },
    }

    manifest = build_manifest(
        project_root=PROJECT_ROOT,
        run_type="optimization_stage",
        run_id=f"stage_{name}",
        case_file=case_path,
        dataset_file=None,
        start_date="",
        end_date="",
        config_obj={"stage": stage, "seed": stage_seed, "workers": workers},
        seed=stage_seed,
        workers=workers,
        extra={
            "stage_name": name,
            "stage_mode": mode,
            "space_file": str(stage.get("space_file", "")),
            "pareto_count": pareto_count,
        },
    )
    mpath = write_manifest(stage_dir, manifest)
    rpath = write_results(stage_dir, payload)
    repath = write_report(
        stage_dir,
        render_simple_report(
            title=f"Staged Optimization - {name}",
            run_id=f"stage_{name}",
            status="PASS",
            key_values={
                "mode": mode,
                "iters": iters,
                "seed": stage_seed,
                "top_k": top_k,
                "pareto_count": pareto_count,
                "space_file": stage.get("space_file", ""),
            },
            artifact_paths={
                "manifest": str(mpath),
                "results": str(rpath),
                "trials_csv": str(trials),
                "pareto_json": str(pareto),
            },
        ),
    )
    payload["artifacts"]["manifest"] = str(mpath)
    payload["artifacts"]["results"] = str(rpath)
    payload["artifacts"]["report"] = str(repath)
    write_results(stage_dir, payload)
    return payload


def main() -> int:
    ap = argparse.ArgumentParser(description="Run staged deterministic optimization workflow.")
    ap.add_argument("--case", required=True, help="Base case JSON path")
    ap.add_argument("--stages-file", required=True, help="Stages JSON/YAML path")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--seed", type=int, default=42, help="Base seed")
    ap.add_argument("--workers", type=int, default=1, help="Worker count")
    ap.add_argument("--reuse-cache", action="store_true", help="Reuse finished stage outputs if fingerprint matches")
    args = ap.parse_args()

    case_path = (PROJECT_ROOT / args.case).resolve() if not Path(args.case).is_absolute() else Path(args.case).resolve()
    stages_file = (PROJECT_ROOT / args.stages_file).resolve() if not Path(args.stages_file).is_absolute() else Path(args.stages_file).resolve()
    outdir = Path(args.outdir).resolve()
    ensure_dir(outdir)

    if not case_path.exists():
        raise FileNotFoundError(f"Case file not found: {case_path}")

    cfg = _load_stage_def(stages_file)
    stages = cfg.get("stages", [])
    if not isinstance(stages, list) or not stages:
        raise ValueError("Stages file must contain non-empty 'stages' list")

    stage_results: list[dict[str, Any]] = []
    for stage in stages:
        result = _stage_run(
            stage=stage,
            case_path=case_path,
            outdir=outdir,
            base_seed=args.seed,
            workers=args.workers,
            reuse_cache=args.reuse_cache,
        )
        stage_results.append(result)
        if result.get("status") != "PASS":
            break

    workflow_status = "PASS" if all(r.get("status") == "PASS" for r in stage_results) else "FAIL"
    run_id = f"staged_opt_{Path(case_path).stem}"

    manifest = build_manifest(
        project_root=PROJECT_ROOT,
        run_type="staged_optimization",
        run_id=run_id,
        case_file=case_path,
        dataset_file=None,
        start_date="",
        end_date="",
        config_obj={"stages_file": str(stages_file), "seed": args.seed, "workers": args.workers},
        seed=args.seed,
        workers=args.workers,
        extra={
            "stages_file": str(stages_file),
            "stages_count": len(stages),
            "stages_completed": sum(1 for r in stage_results if r.get("status") == "PASS"),
        },
    )
    mpath = write_manifest(outdir, manifest)

    payload = {
        "run_id": run_id,
        "run_type": "staged_optimization",
        "status": workflow_status,
        "case": str(case_path),
        "stages_file": str(stages_file),
        "seed": args.seed,
        "workers": args.workers,
        "stages": stage_results,
        "artifacts": {
            "manifest": str(mpath),
        },
    }
    rpath = write_results(outdir, payload)
    repath = write_report(
        outdir,
        render_simple_report(
            title="Staged Optimization Workflow",
            run_id=run_id,
            status=workflow_status,
            key_values={
                "case": case_path,
                "stages_file": stages_file,
                "stages_total": len(stages),
                "stages_pass": sum(1 for r in stage_results if r.get("status") == "PASS"),
                "seed": args.seed,
                "workers": args.workers,
            },
            artifact_paths={
                "manifest": str(mpath),
                "results": str(rpath),
            },
        ),
    )
    payload["artifacts"]["results"] = str(rpath)
    payload["artifacts"]["report"] = str(repath)
    write_results(outdir, payload)

    print(f"staged_optimization_status={workflow_status}")
    print(f"outdir={outdir}")
    return 0 if workflow_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
