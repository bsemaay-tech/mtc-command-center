#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent          # mtc_backtest
REPO_ROOT = PROJECT_ROOT.parent           # repo root
sys.path.insert(0, str(PROJECT_ROOT))

from src.workflow.artifacts import (  # noqa: E402
    build_manifest,
    default_artifact_dir,
    render_simple_report,
    sha256_file,
    write_manifest,
    write_report,
    write_results,
)


@dataclass
class StepResult:
    name: str
    status: str
    command: str = ""
    output: str = ""
    error: str = ""
    skip_reason: str = ""


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [_json_safe(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    # datetime/date like objects from YAML
    if hasattr(value, "isoformat") and callable(getattr(value, "isoformat")):
        try:
            return value.isoformat()
        except Exception:
            return str(value)
    return value


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _to_abs(path_like: str) -> Path:
    p = Path(path_like)
    if p.is_absolute():
        return p
    return (REPO_ROOT / p).resolve()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be mapping: {path}")
    return data


def _run(cmd: list[str], *, cwd: Path, step: str) -> StepResult:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return StepResult(
        name=step,
        status="PASS" if p.returncode == 0 else "FAIL",
        command=" ".join(cmd),
        output=p.stdout[-5000:],
        error=p.stderr[-5000:],
    )


def _skip(step: str, reason: str) -> StepResult:
    return StepResult(name=step, status="SKIP", skip_reason=reason)


def _step_enabled(autorun: dict[str, Any], key: str, default: bool = True) -> bool:
    steps = autorun.get("steps", {})
    if not isinstance(steps, dict):
        return default
    entry = steps.get(key, default)
    if isinstance(entry, dict):
        return bool(entry.get("enabled", default))
    return bool(entry)


def _resolve_dataset_from_catalog(data_ref: str, catalog_path: Path) -> Path:
    if ":" not in data_ref:
        return _to_abs(data_ref)

    symbol, tf = [x.strip() for x in data_ref.split(":", 1)]
    if not catalog_path.exists():
        raise FileNotFoundError(f"Catalog not found for data_ref resolution: {catalog_path}")

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    entry = catalog.get(symbol, {}).get(tf, {})
    abs_path = str(entry.get("abs_path", "")).strip()
    rel_path = str(entry.get("path", "")).strip()

    if abs_path:
        p = Path(abs_path)
        if p.exists():
            return p.resolve()

    if rel_path:
        cand1 = (REPO_ROOT / rel_path).resolve()
        cand2 = (REPO_ROOT / "110_" / rel_path).resolve()
        if cand1.exists():
            return cand1
        if cand2.exists():
            return cand2

    raise FileNotFoundError(f"Could not resolve data_ref='{data_ref}' from catalog")


def _catalog_has_symbol_tfs(catalog_path: Path, symbol: str, timeframes: list[str]) -> bool:
    if not catalog_path.exists():
        return False
    try:
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
        symbol_entry = payload.get(symbol, {})
        for tf in timeframes:
            entry = symbol_entry.get(tf, {})
            abs_path = str(entry.get("abs_path", "")).strip()
            rel_path = str(entry.get("path", "")).strip()
            ok = False
            if abs_path and Path(abs_path).exists():
                ok = True
            elif rel_path:
                if (REPO_ROOT / rel_path).exists() or (REPO_ROOT / "110_" / rel_path).exists():
                    ok = True
            if not ok:
                return False
        return True
    except Exception:
        return False


def _load_case(case_path: Path) -> dict[str, Any]:
    payload = json.loads(case_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid case file: {case_path}")
    return payload


def _find_latest_py_debug_csv(case_path: Path) -> Path:
    case = _load_case(case_path)
    debug_dir = str(case.get("config", {}).get("parity", {}).get("debug_dir", "")).strip()
    if not debug_dir:
        raise ValueError(f"Case has no config.parity.debug_dir: {case_path}")
    debug_path = _to_abs(f"mtc_backtest/{debug_dir}")
    if not debug_path.exists():
        raise FileNotFoundError(f"Debug dir not found: {debug_path}")

    files = sorted(debug_path.glob("debug_python_trades*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No debug_python_trades*.csv found in {debug_path}")
    return files[0]


def _build_stage_spaces(
    *,
    param_space: dict[str, Any],
    autorun: dict[str, Any],
    run_dir: Path,
) -> tuple[Path, list[Path]]:
    registry = param_space.get("module_registry", {})
    stages = param_space.get("stages", [])
    if not isinstance(stages, list) or not stages:
        raise ValueError("param_space.yaml must include non-empty stages list")

    # Flatten module id -> params
    module_map: dict[str, list[dict[str, Any]]] = {}
    for group_name, group_items in registry.items():
        if not isinstance(group_items, dict):
            continue
        for module_id, module_def in group_items.items():
            full_id = f"{group_name}.{module_id}"
            params = module_def.get("params", []) if isinstance(module_def, dict) else []
            module_map[full_id] = list(params)

    space_dir = run_dir / "spaces"
    space_dir.mkdir(parents=True, exist_ok=True)

    default_opt = autorun.get("optimization", {})
    default_mode = str(default_opt.get("mode", "random"))
    default_iters = int(default_opt.get("iters", 20))
    default_top_k = int(default_opt.get("top_k", 8))

    stage_entries: list[dict[str, Any]] = []
    created_spaces: list[Path] = []

    for stage in stages:
        sid = str(stage.get("id", "stage"))
        include_modules = stage.get("module_ids", [])
        if not isinstance(include_modules, list):
            include_modules = []

        grid: dict[str, Any] = {}
        random_space: dict[str, Any] = {}

        for mid in include_modules:
            for p in module_map.get(str(mid), []):
                key = str(p.get("key", "")).strip()
                if not key:
                    continue
                if isinstance(p.get("grid"), dict):
                    grid[key] = p["grid"]
                if isinstance(p.get("random"), dict):
                    random_space[key] = p["random"]

        for p in stage.get("extra_params", []) if isinstance(stage.get("extra_params"), list) else []:
            key = str(p.get("key", "")).strip()
            if not key:
                continue
            if isinstance(p.get("grid"), dict):
                grid[key] = p["grid"]
            if isinstance(p.get("random"), dict):
                random_space[key] = p["random"]

        space_payload = {"grid": grid, "random": random_space}
        space_file = (space_dir / f"{sid}.json").resolve()
        space_file.write_text(json.dumps(space_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        created_spaces.append(space_file)

        stage_entries.append(
            {
                "name": sid,
                "mode": str(stage.get("mode", default_mode)),
                "iters": int(stage.get("iters", default_iters)),
                "top_k": int(stage.get("top_k", default_top_k)),
                "space_file": str(space_file),
            }
        )

    stages_file = (run_dir / "stages_autogen.json").resolve()
    stages_file.write_text(json.dumps({"stages": stage_entries}, indent=2, ensure_ascii=False), encoding="utf-8")
    return stages_file, created_spaces


def _write_run_index(
    *,
    autorun: dict[str, Any],
    run_id: str,
    run_dir: Path,
    results: list[StepResult],
    payload: dict[str, Any],
) -> Path:
    runtime = autorun.get("runtime", {})
    root = runtime.get("run_index_root", "mtc_backtest/backtest_assets/runs")
    index_dir = _to_abs(str(root)) / run_id
    index_dir.mkdir(parents=True, exist_ok=True)

    index_json = index_dir / "index.json"
    index_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        f"# Autopilot Run Index - {run_id}",
        "",
        f"- run_dir: `{run_dir}`",
        f"- manifest: `{payload.get('artifacts', {}).get('manifest', '')}`",
        f"- results: `{payload.get('artifacts', {}).get('results', '')}`",
        f"- report: `{payload.get('artifacts', {}).get('report', '')}`",
        "",
        "## Step Status",
        "",
        "| Step | Status | Skip Reason |",
        "|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r.name} | {r.status} | {r.skip_reason} |")

    lines += [
        "",
        "## Artifact Roots",
        "",
        "- Backtest runs: `mtc_backtest/results/backtest_runs/`",
        "- Parity runs: `mtc_backtest/results/parity_runs/`",
        "- Autopilot runs: `mtc_backtest/results/autopilot_runs/`",
        "- Staged optimization: `mtc_backtest/results/autopilot/staged_opt/`",
        "- Walk-forward: `mtc_backtest/results/autopilot/walkforward/`",
        "- Robustness: `mtc_backtest/results/autopilot/robustness/`",
        "",
        f"- index_json: `{index_json}`",
        "",
    ]

    index_md = index_dir / "INDEX.md"
    index_md.write_text("\n".join(lines), encoding="utf-8")
    return index_md


def main() -> int:
    ap = argparse.ArgumentParser(description="Autopilot runner for data/parity/backtest/optimization/robustness")
    ap.add_argument("--autorun", default="mtc_backtest/backtest_assets/autorun.yaml", help="Path to autorun YAML")
    ap.add_argument("--param-space", default="mtc_backtest/backtest_assets/param_space.yaml", help="Path to staged param-space YAML")
    ap.add_argument("--stop-on-fail", action="store_true", help="Stop pipeline when a step fails")
    args = ap.parse_args()

    autorun_path = _to_abs(args.autorun)
    param_space_path = _to_abs(args.param_space)

    autorun = _load_yaml(autorun_path)
    param_space = _load_yaml(param_space_path)

    run_name = f"autopilot_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%SZ')}"
    run_dir = default_artifact_dir(PROJECT_ROOT, "autopilot", run_name)
    run_tag = run_name

    py = sys.executable
    results: list[StepResult] = []

    # Step 1: build datasets + validate (wrapper)
    data_cfg = autorun.get("data", {})
    catalog_path = _to_abs(str(data_cfg.get("catalog", "mtc_backtest/backtest_assets/data_catalog.json")))
    if _step_enabled(autorun, "data_pipeline", True):
        results.append(
            _run(
                [
                    py,
                    "mtc_backtest/scripts/download_datasets_autopilot.py",
                    "--autorun",
                    str(autorun_path),
                ],
                cwd=REPO_ROOT,
                step="data_pipeline",
            )
        )
    else:
        results.append(_skip("data_pipeline", "DISABLED_IN_AUTORUN"))

    # Step 2: regime calendar (wrapper)
    if _step_enabled(autorun, "data_pipeline", True):
        results.append(
            _run(
                [
                    py,
                    "mtc_backtest/scripts/generate_regime_calendar_4h.py",
                    "--autorun",
                    str(autorun_path),
                    "--override-yaml",
                    str(_to_abs(str(autorun.get("regime", {}).get("override_yaml", "mtc_backtest/backtest_assets/regime_override.yaml")))),
                ],
                cwd=REPO_ROOT,
                step="regime_calendar_generate",
            )
        )
    else:
        results.append(_skip("regime_calendar_generate", "DISABLED_IN_AUTORUN"))

    # Step 3: parity smoke (raw + clip)
    parity_cfg = autorun.get("parity", {})
    parity_case = _to_abs(str(parity_cfg.get("case_for_py_generation", "mtc_backtest/configs/cases/full_jul2025_jan2026_parity.json")))
    tv_csv = _to_abs(str(parity_cfg.get("tv_csv", "mtc_backtest/debug/BTCUSDT/15m/MT_CORE2_BINANCE_BTCUSDT.P_2026-02-13_6e3fc.csv")))
    py_csv_cfg = str(parity_cfg.get("py_csv", "")).strip()
    py_csv = _to_abs(py_csv_cfg) if py_csv_cfg else None

    if not _step_enabled(autorun, "parity_smoke", True):
        results.append(_skip("parity_py_csv_generate", "DISABLED_IN_AUTORUN"))
        results.append(_skip("parity_smoke_raw", "DISABLED_IN_AUTORUN"))
        results.append(_skip("parity_smoke_clip", "DISABLED_IN_AUTORUN"))
    elif not tv_csv.exists():
        results.append(_skip("parity_py_csv_generate", "TV_EXPORT_MISSING"))
        results.append(_skip("parity_smoke_raw", "TV_EXPORT_MISSING"))
        results.append(_skip("parity_smoke_clip", "TV_EXPORT_MISSING"))
    else:
        if py_csv is None or not py_csv.exists():
            # generate fresh PY debug csv from parity case
            results.append(
                _run(
                    [py, "mtc_backtest/scripts/run_case.py", str(parity_case)],
                    cwd=REPO_ROOT,
                    step="parity_py_csv_generate",
                )
            )
            try:
                py_csv = _find_latest_py_debug_csv(parity_case)
            except Exception as exc:
                results.append(StepResult(name="parity_py_csv_resolve", status="FAIL", error=str(exc)))
                py_csv = None

        parity_out_raw = _to_abs(str(parity_cfg.get("out_raw_csv", "mtc_backtest/results/parity_smoke_raw.csv")))
        parity_out_clip = _to_abs(str(parity_cfg.get("out_clip_csv", "mtc_backtest/results/parity_smoke_clip.csv")))
        summary_raw = _to_abs(str(parity_cfg.get("summary_raw_csv", "mtc_backtest/results/parity_smoke_raw_summary.csv")))
        summary_clip = _to_abs(str(parity_cfg.get("summary_clip_csv", "mtc_backtest/results/parity_smoke_clip_summary.csv")))

        case_end = str(parity_cfg.get("case_end", ""))
        tv_tz = str(parity_cfg.get("tv_tz", "Europe/London"))

        if py_csv is None:
            results.append(_skip("parity_smoke_raw", "PY_DEBUG_CSV_MISSING"))
            results.append(_skip("parity_smoke_clip", "PY_DEBUG_CSV_MISSING"))
        else:
            results.append(
                _run(
                    [
                        py,
                        "mtc_backtest/scripts/compare_tv_web_trades.py",
                        "--tv", str(tv_csv),
                        "--py", str(py_csv),
                        "--out", str(parity_out_raw),
                        "--tv-tz", tv_tz,
                        "--dual-report",
                        "--summary-out", str(summary_raw),
                        "--case-end", case_end,
                    ],
                    cwd=REPO_ROOT,
                    step="parity_smoke_raw",
                )
            )
            results.append(
                _run(
                    [
                        py,
                        "mtc_backtest/scripts/compare_tv_web_trades.py",
                        "--tv", str(tv_csv),
                        "--py", str(py_csv),
                        "--out", str(parity_out_clip),
                        "--tv-tz", tv_tz,
                        "--dual-report",
                        "--clip-overlap",
                        "--summary-out", str(summary_clip),
                        "--case-end", case_end,
                    ],
                    cwd=REPO_ROOT,
                    step="parity_smoke_clip",
                )
            )

    # Step 4: baseline backtest
    bt_cfg = autorun.get("baseline_backtest", {})
    baseline_case = _to_abs(str(bt_cfg.get("case", "mtc_backtest/configs/cases/sep2025_parity.json")))
    baseline_regime = str(bt_cfg.get("regime", "all"))
    if not _step_enabled(autorun, "baseline_backtest", True):
        results.append(_skip("baseline_backtest", "DISABLED_IN_AUTORUN"))
    elif not baseline_case.exists():
        results.append(_skip("baseline_backtest", "BASE_CASE_MISSING"))
    else:
        results.append(
            _run(
                [
                    py,
                    "mtc_backtest/scripts/run_case.py",
                    str(baseline_case),
                    "--regime",
                    baseline_regime,
                ],
                cwd=REPO_ROOT,
                step="baseline_backtest",
            )
        )

    # Step 5: tiny optimization (optimizer_v0)
    tiny_cfg = autorun.get("tiny_optimization", {})
    tiny_case = _to_abs(str(tiny_cfg.get("case", str(baseline_case))))
    if not _step_enabled(autorun, "tiny_optimization", True):
        results.append(_skip("tiny_optimization", "DISABLED_IN_AUTORUN"))
    elif not tiny_case.exists():
        results.append(_skip("tiny_optimization", "TINY_CASE_MISSING"))
    else:
        tiny_db_base = _to_abs(str(tiny_cfg.get("db", "mtc_backtest/results/optimizer_smoke.db")))
        tiny_out_base = _to_abs(str(tiny_cfg.get("out_csv", "mtc_backtest/results/optimizer_smoke_trials.csv")))
        tiny_pareto_base = _to_abs(str(tiny_cfg.get("pareto_out", "mtc_backtest/results/optimizer_smoke_pareto.json")))

        tiny_db = tiny_db_base.with_name(f"{tiny_db_base.stem}_{run_tag}{tiny_db_base.suffix or '.db'}")
        tiny_out = tiny_out_base.with_name(f"{tiny_out_base.stem}_{run_tag}{tiny_out_base.suffix or '.csv'}")
        tiny_pareto = tiny_pareto_base.with_name(f"{tiny_pareto_base.stem}_{run_tag}{tiny_pareto_base.suffix or '.json'}")
        tiny_db.parent.mkdir(parents=True, exist_ok=True)
        tiny_out.parent.mkdir(parents=True, exist_ok=True)
        tiny_pareto.parent.mkdir(parents=True, exist_ok=True)

        tiny_cmd = [
            py,
            "-m",
            "src.optimizer_v0",
            "run",
            "--case",
            str(tiny_case),
            "--mode",
            str(tiny_cfg.get("mode", "random")),
            "--iters",
            str(int(tiny_cfg.get("iters", 30))),
            "--seed",
            str(int(autorun.get("seed", 42))),
            "--workers",
            str(int(tiny_cfg.get("workers", 1))),
            "--db",
            str(tiny_db),
            "--out",
            str(tiny_out),
            "--pareto-out",
            str(tiny_pareto),
            "--objectives",
            str(tiny_cfg.get("objectives", "net_profit,max_dd_pct,profit_factor,win_rate,total_trades")),
        ]
        results.append(_run(tiny_cmd, cwd=PROJECT_ROOT, step="tiny_optimization"))

    # Step 6: staged optimization
    stages_file, space_files = _build_stage_spaces(param_space=param_space, autorun=autorun, run_dir=run_dir)
    opt_cfg = autorun.get("optimization", {})
    opt_case = _to_abs(str(opt_cfg.get("case", str(baseline_case))))
    opt_outdir_base = _to_abs(str(opt_cfg.get("outdir", "mtc_backtest/results/autopilot/staged_opt")))
    opt_outdir = (opt_outdir_base / run_tag).resolve()
    if not _step_enabled(autorun, "staged_optimization", True):
        results.append(_skip("staged_optimization", "DISABLED_IN_AUTORUN"))
    elif not opt_case.exists():
        results.append(_skip("staged_optimization", "STAGED_CASE_MISSING"))
    else:
        results.append(
            _run(
                [
                    py,
                    "mtc_backtest/scripts/staged_optimize.py",
                    "--case", str(opt_case),
                    "--stages-file", str(stages_file),
                    "--outdir", str(opt_outdir),
                    "--seed", str(int(autorun.get("seed", 42))),
                    "--workers", str(int(opt_cfg.get("workers", 1))),
                ],
                cwd=REPO_ROOT,
                step="staged_optimization",
            )
        )

    # Step 7: walk-forward robustness
    rb_cfg = autorun.get("robustness", {})
    train_case = _to_abs(str(rb_cfg.get("train_case", "mtc_backtest/configs/cases/full_jul2025_jan2026_parity.json")))
    target_case_1 = _to_abs(str(rb_cfg.get("target_case_1", "mtc_backtest/configs/cases/target_sep2025_dec2025.json")))
    target_case_2 = _to_abs(str(rb_cfg.get("target_case_2", "mtc_backtest/configs/cases/target_jan2026.json")))

    wf_outdir_base = _to_abs(str(rb_cfg.get("walkforward_outdir", "mtc_backtest/results/autopilot/walkforward")))
    wf_outdir = (wf_outdir_base / run_tag).resolve()
    if not _step_enabled(autorun, "walkforward", True):
        results.append(_skip("walkforward_validate", "DISABLED_IN_AUTORUN"))
    elif not (train_case.exists() and target_case_1.exists() and target_case_2.exists()):
        results.append(_skip("walkforward_validate", "WALKFORWARD_CASE_MISSING"))
    else:
        results.append(
            _run(
                [
                    py,
                    "mtc_backtest/scripts/walk_forward_validate.py",
                    "--train-case", str(train_case),
                    "--target-case-1", str(target_case_1),
                    "--target-case-2", str(target_case_2),
                    "--iters", str(int(rb_cfg.get("iters", 10))),
                    "--seed", str(int(autorun.get("seed", 42))),
                    "--workers", str(int(rb_cfg.get("workers", 1))),
                    "--outdir", str(wf_outdir),
                ],
                cwd=REPO_ROOT,
                step="walkforward_validate",
            )
        )

    candidate_file = None
    cand_dirs = [
        opt_outdir / "stage_signal" / "candidates",
        opt_outdir / "candidates",
        wf_outdir / "candidates",
    ]
    for cdir in cand_dirs:
        if cdir.exists():
            files = sorted(cdir.glob("candidate_*.json"))
            if files:
                candidate_file = files[0]
                break

    manual_candidate = str(rb_cfg.get("candidate_json", "")).strip()
    if manual_candidate:
        c = _to_abs(manual_candidate)
        if c.exists():
            candidate_file = c

    if not _step_enabled(autorun, "robustness", True):
        results.append(_skip("robustness_runner", "DISABLED_IN_AUTORUN"))
    elif candidate_file is not None:
        robustness_outdir_base = _to_abs(str(rb_cfg.get("robustness_outdir", "mtc_backtest/results/autopilot/robustness")))
        robustness_outdir = (robustness_outdir_base / run_tag).resolve()
        results.append(
            _run(
                [
                    py,
                    "mtc_backtest/scripts/robustness_runner.py",
                    "--case", str(opt_case),
                    "--candidate", str(candidate_file),
                    "--outdir", str(robustness_outdir),
                    "--seed", str(int(autorun.get("seed", 42))),
                    "--workers", str(int(rb_cfg.get("workers", 1))),
                ],
                cwd=REPO_ROOT,
                step="robustness_runner",
            )
        )
    else:
        results.append(_skip("robustness_runner", "CANDIDATE_MISSING"))

    overall_status = "FAIL" if any(r.status == "FAIL" for r in results) else "PASS"
    run_id = f"autopilot_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%SZ')}"

    manifest = build_manifest(
        project_root=PROJECT_ROOT,
        run_type="autopilot",
        run_id=run_id,
        case_file=None,
        dataset_file=None,
        seed=int(autorun.get("seed", 42)),
        workers=1,
        config_obj={
            "autorun": _json_safe(autorun),
            "param_space_file": str(param_space_path),
            "timezone": str(autorun.get("timezone", "UTC")),
        },
        extra={
            "autorun_file": str(autorun_path),
            "autorun_hash": sha256_file(autorun_path),
            "param_space_file": str(param_space_path),
            "param_space_hash": sha256_file(param_space_path),
            "commands_source": str(autorun.get("commands_source", "100_PROJECT_MEMORY_FİLE/20_BACKTEST_WORKFLOW/01_CURRENT_STATE.md")),
            "generated_at": _now_utc(),
            "spaces_generated": [str(p) for p in space_files],
        },
    )
    manifest_path = write_manifest(run_dir, manifest)

    payload = {
        "run_id": run_id,
        "run_type": "autopilot",
        "status": overall_status,
        "autorun_file": str(autorun_path),
        "param_space_file": str(param_space_path),
        "steps": [r.__dict__ for r in results],
        "artifacts": {
            "manifest": str(manifest_path),
        },
    }
    results_path = write_results(run_dir, payload)

    report_lines = [
        "# Autopilot Run Report",
        "",
        f"- run_id: `{run_id}`",
        f"- status: `{overall_status}`",
        f"- autorun: `{autorun_path}`",
        f"- param_space: `{param_space_path}`",
        "",
        "## Step Status",
        "",
        "| Step | Status | Skip Reason |",
        "|------|--------|-------------|",
    ]
    for r in results:
        report_lines.append(f"| {r.name} | {r.status} | {r.skip_reason} |")

    report_path = write_report(run_dir, "\n".join(report_lines) + "\n")
    payload["artifacts"].update({"results": str(results_path), "report": str(report_path)})
    write_results(run_dir, payload)

    run_index_path = _write_run_index(
        autorun=autorun,
        run_id=run_id,
        run_dir=run_dir,
        results=results,
        payload=payload,
    )
    payload["artifacts"]["run_index"] = str(run_index_path)
    write_results(run_dir, payload)

    print(f"autopilot_status={overall_status}")
    print(f"artifacts_dir={run_dir}")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
