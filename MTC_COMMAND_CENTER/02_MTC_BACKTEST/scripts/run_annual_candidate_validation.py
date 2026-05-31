from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _stage_name(case_path: Path) -> str:
    stem = case_path.stem
    if stem.endswith("_full"):
        stem = stem[:-5]
    return stem


def _build_case(base_case: Path, dataset_name: str, year: int, out_path: Path) -> Path:
    payload = _read_json(base_case)
    payload["dataset"] = dataset_name
    payload["start_date"] = f"{year}-01-01T00:00:00"
    payload["end_date"] = f"{year + 1}-01-01T00:00:00"
    payload.setdefault("_annual_validation", {})
    payload["_annual_validation"]["source_case"] = str(base_case.resolve())
    payload["_annual_validation"]["year"] = year
    _write_json(out_path, payload)
    return out_path


def _run_case(case_path: Path, artifacts_dir: Path) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "run_case.py"),
        str(case_path),
        "--artifacts-dir",
        str(artifacts_dir),
    ]
    proc = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"run_case failed for {case_path.name} ({proc.returncode})\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return _read_json(artifacts_dir / "results.json")


def main() -> int:
    ap = argparse.ArgumentParser(description="Run annual validation backtests for selected candidate cases.")
    ap.add_argument("--case", action="append", required=True, help="Candidate case JSON path; repeat per case")
    ap.add_argument("--years", default="2024,2023,2022", help="Comma-separated years")
    ap.add_argument("--dataset", required=True, help="Dataset name under mtc_backtest/data")
    ap.add_argument("--outdir", required=True, help="Output directory")
    args = ap.parse_args()

    years = [int(x.strip()) for x in args.years.split(",") if x.strip()]
    case_paths = [Path(p).resolve() if Path(p).is_absolute() else (PROJECT_ROOT / p).resolve() for p in args.case]
    outdir = Path(args.outdir).resolve()
    cases_dir = outdir / "cases"
    eval_dir = outdir / "evaluations"
    cases_dir.mkdir(parents=True, exist_ok=True)
    eval_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for case_path in case_paths:
        stage = _stage_name(case_path)
        for year in years:
            annual_case = _build_case(
                case_path,
                args.dataset,
                year,
                cases_dir / f"{stage}_{year}.json",
            )
            results = _run_case(annual_case, eval_dir / f"{stage}_{year}")
            metrics = results.get("metrics", {})
            rows.append(
                {
                    "stage": stage,
                    "year": year,
                    "case_path": str(annual_case),
                    "net_profit": metrics.get("net_profit"),
                    "net_profit_pct": metrics.get("net_profit_pct"),
                    "max_drawdown": metrics.get("max_drawdown"),
                    "profit_factor": metrics.get("profit_factor"),
                    "win_rate": metrics.get("win_rate"),
                    "total_trades": metrics.get("total_trades"),
                }
            )

    summary = {
        "dataset": args.dataset,
        "years": years,
        "cases": [str(p) for p in case_paths],
        "results": rows,
    }
    _write_json(outdir / "summary.json", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
