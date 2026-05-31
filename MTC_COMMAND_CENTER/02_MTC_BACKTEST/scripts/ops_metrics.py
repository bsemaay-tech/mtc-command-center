from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def compute_run_duration_seconds(run_dir: Path) -> float:
    if not run_dir.exists():
        return 0.0
    files = [p for p in run_dir.rglob("*") if p.is_file()]
    if not files:
        return 0.0
    mtimes = [p.stat().st_mtime for p in files]
    return max(0.0, float(max(mtimes) - min(mtimes)))


def parity_drift_count(parity_report_csv: Path) -> int:
    if not parity_report_csv.exists():
        return 0
    df = pd.read_csv(parity_report_csv)
    if "all_core_match" not in df.columns:
        return 0
    return int((~df["all_core_match"].astype(bool)).sum())


def walkforward_pass_fail(summary_json: Path) -> bool:
    if not summary_json.exists():
        return False
    payload = json.loads(summary_json.read_text(encoding="utf-8"))
    return payload.get("status") == "OK" and int(payload.get("ok_candidates", 0)) > 0


def build_metrics(run_dir: Path | None, walkforward_summary: Path | None, parity_report: Path | None) -> dict:
    duration = compute_run_duration_seconds(run_dir) if run_dir else 0.0
    wf_ok = walkforward_pass_fail(walkforward_summary) if walkforward_summary else True
    drift = parity_drift_count(parity_report) if parity_report else 0
    return {
        "run_duration_seconds": duration,
        "walkforward_pass": wf_ok,
        "parity_drift_count": drift,
        "overall_pass": bool(wf_ok and drift == 0),
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Operational metrics for run duration/pass-fail/parity drift.")
    p.add_argument("--run-dir", required=False)
    p.add_argument("--walkforward-summary", required=False)
    p.add_argument("--parity-report", required=False)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    metrics = build_metrics(
        Path(args.run_dir) if args.run_dir else None,
        Path(args.walkforward_summary) if args.walkforward_summary else None,
        Path(args.parity_report) if args.parity_report else None,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Metrics written: {out}")


if __name__ == "__main__":
    main()
