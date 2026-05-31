"""
Convenience wrapper for TV vs Python trade comparison.

Example:
  python scripts/compare_tv_web_trades.py \
    --tv debug/BTCUSDT/15m/tv.csv \
    --py debug/BTCUSDT/15m/debug_python_trades.csv \
    --out debug/BTCUSDT/15m/parity_compare.csv \
    --dual-report \
    --summary-out debug/BTCUSDT/15m/parity_compare_summary.csv
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.parity.compare_tv_trades import build_report, clip_overlap, load_py_trades, load_tv_trades, summarize_report
from src.parity.dual_status import classify_parity_with_dual_view, compute_gap_days
from src.workflow.artifacts import (
    build_manifest,
    default_artifact_dir,
    render_simple_report,
    sha256_file,
    write_manifest,
    write_report,
    write_results,
)


def _parse_case_end_utc(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(str(raw))
    except ValueError:
        try:
            dt = datetime.strptime(str(raw), "%Y-%m-%d")
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt


def main() -> None:
    p = argparse.ArgumentParser(description="Compare TradingView trades with Python web/engine trades.")
    p.add_argument("--tv", required=True, help="Path to TradingView trade export CSV")
    p.add_argument("--py", required=True, help="Path to debug_python_trades CSV")
    p.add_argument("--out", required=True, help="Output parity report CSV path")
    p.add_argument("--tv-tz", default="Europe/London", help="TV timezone for naive timestamps")
    p.add_argument("--clip-overlap", action="store_true", help="Compare only overlapping time interval")
    p.add_argument("--dual-report", action="store_true", help="Compute both raw and clip-overlap summaries")
    p.add_argument("--summary-out", default="", help="Optional output CSV path for comparison summary row")
    p.add_argument("--case-end", default="", help="Optional case end datetime (UTC) for gap_days diagnostics")
    p.add_argument("--no-artifacts", action="store_true", help="Disable manifest/results/report output")
    p.add_argument("--artifacts-dir", default="", help="Custom output directory for run artifacts")
    p.add_argument("--run-id", default="", help="Optional run-id override")
    args = p.parse_args()

    tv_path = Path(args.tv).resolve()
    py_path = Path(args.py).resolve()

    tv_raw = load_tv_trades(tv_path, tv_tz=args.tv_tz)
    py_raw = load_py_trades(py_path)
    raw_report = build_report(tv_raw, py_raw)
    raw_summary = summarize_report(tv_raw, py_raw, raw_report)

    tv_clip, py_clip = clip_overlap(tv_raw, py_raw)
    clip_report = build_report(tv_clip, py_clip)
    clip_summary = summarize_report(tv_clip, py_clip, clip_report)

    if args.clip_overlap:
        report = clip_report
        summary = clip_summary
        mode = "clip"
    else:
        report = raw_report
        summary = raw_summary
        mode = "raw"

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(out, index=False)

    case_end_utc = _parse_case_end_utc(args.case_end)
    last_tv_exit_utc = None
    if len(tv_raw) > 0:
        try:
            last_tv_exit_utc = tv_raw["exit_time"].max().to_pydatetime()
        except Exception:
            last_tv_exit_utc = None
    gap_days = compute_gap_days(case_end_utc, last_tv_exit_utc)

    status, note, diag = classify_parity_with_dual_view(
        clip_summary=clip_summary,
        raw_summary=raw_summary,
        gap_days=gap_days,
    )

    print(f"Mode: {mode}")
    print(f"TV trades: {summary['tv_trades']}")
    print(f"PY trades: {summary['py_trades']}")
    if summary.get("raw_tv_trades") != summary["tv_trades"] or summary.get("raw_py_trades") != summary["py_trades"]:
        print(f"Raw TV trades: {summary['raw_tv_trades']}")
        print(f"Raw PY trades: {summary['raw_py_trades']}")
    print(f"Compared: {summary['compared']}")
    print(f"Extra TV trades: {summary['extra_tv_trades']}")
    print(f"Extra PY trades: {summary['extra_py_trades']}")
    print(f"Strict parity: {'PASS' if summary['strict_pass'] else 'FAIL'}")

    if args.dual_report:
        print("Dual summary:")
        print(
            f"  raw:  {'PASS' if raw_summary['strict_pass'] else 'FAIL'} "
            f"(tv={raw_summary['tv_trades']} py={raw_summary['py_trades']} "
            f"extra_tv={raw_summary['extra_tv_trades']} extra_py={raw_summary['extra_py_trades']})"
        )
        print(
            f"  clip: {'PASS' if clip_summary['strict_pass'] else 'FAIL'} "
            f"(tv={clip_summary['tv_trades']} py={clip_summary['py_trades']} "
            f"extra_tv={clip_summary['extra_tv_trades']} extra_py={clip_summary['extra_py_trades']})"
        )
        print(f"  classifier: {status} | {note}")

    if args.summary_out:
        summary_out = Path(args.summary_out)
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        with summary_out.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "tv_path",
                    "py_path",
                    "selected_mode",
                    "selected_strict_pass",
                    "raw_strict_pass",
                    "raw_tv_trades",
                    "raw_py_trades",
                    "raw_extra_tv",
                    "raw_extra_py",
                    "clip_strict_pass",
                    "clip_tv_trades",
                    "clip_py_trades",
                    "clip_extra_tv",
                    "clip_extra_py",
                    "dual_status",
                    "early_trade_end_candidate",
                    "gap_days",
                    "out_report",
                ]
            )
            w.writerow(
                [
                    str(tv_path),
                    str(py_path),
                    mode,
                    "PASS" if summary["strict_pass"] else "FAIL",
                    "PASS" if raw_summary["strict_pass"] else "FAIL",
                    raw_summary["tv_trades"],
                    raw_summary["py_trades"],
                    raw_summary["extra_tv_trades"],
                    raw_summary["extra_py_trades"],
                    "PASS" if clip_summary["strict_pass"] else "FAIL",
                    clip_summary["tv_trades"],
                    clip_summary["py_trades"],
                    clip_summary["extra_tv_trades"],
                    clip_summary["extra_py_trades"],
                    status,
                    diag.get("early_trade_end_candidate", ""),
                    diag.get("gap_days", ""),
                    str(out),
                ]
            )
        print(f"Summary: {summary_out}")

    if not args.no_artifacts:
        run_name = f"{tv_path.stem}_vs_{py_path.stem}"
        resolved_run_id = args.run_id or f"parity_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%SZ')}"
        outdir = Path(args.artifacts_dir).resolve() if args.artifacts_dir else default_artifact_dir(PROJECT_ROOT, "parity", run_name)

        manifest = build_manifest(
            project_root=PROJECT_ROOT,
            run_type="parity",
            run_id=resolved_run_id,
            case_file=None,
            dataset_file=None,
            start_date="",
            end_date=str(args.case_end or ""),
            extra={
                "tv_input": str(tv_path),
                "py_input": str(py_path),
                "tv_input_hash": "" if not tv_path.exists() else sha256_file(tv_path),
                "py_input_hash": "" if not py_path.exists() else sha256_file(py_path),
                "selected_mode": mode,
            },
        )

        payload = {
            "run_id": resolved_run_id,
            "run_type": "parity",
            "status": status,
            "selected_mode": mode,
            "raw_summary": raw_summary,
            "clip_summary": clip_summary,
            "classifier_note": note,
            "classifier_diag": diag,
            "artifacts": {},
        }

        manifest_path = write_manifest(outdir, manifest)
        results_path = write_results(outdir, payload)
        report_path = write_report(
            outdir,
            render_simple_report(
                title="TV vs Python Parity Report",
                run_id=resolved_run_id,
                status=status,
                key_values={
                    "tv_path": tv_path,
                    "py_path": py_path,
                    "raw_strict": "PASS" if raw_summary["strict_pass"] else "FAIL",
                    "clip_strict": "PASS" if clip_summary["strict_pass"] else "FAIL",
                    "raw_tv_trades": raw_summary.get("tv_trades", ""),
                    "raw_py_trades": raw_summary.get("py_trades", ""),
                    "gap_days": diag.get("gap_days", ""),
                    "early_trade_end_candidate": diag.get("early_trade_end_candidate", ""),
                    "note": note,
                },
                artifact_paths={
                    "manifest": str(manifest_path),
                    "results": str(results_path),
                    "parity_report_csv": str(out),
                },
            ),
        )
        payload["artifacts"] = {
            "manifest": str(manifest_path),
            "results": str(results_path),
            "report": str(report_path),
            "parity_report_csv": str(out),
        }
        write_results(outdir, payload)
        print(f"Artifacts: {outdir}")

    print(f"Output: {out}")


if __name__ == "__main__":
    main()
