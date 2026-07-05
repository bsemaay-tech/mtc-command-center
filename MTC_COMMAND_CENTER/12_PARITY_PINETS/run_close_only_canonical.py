from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/close_only_canonical_manifest.json"
PARITY_COMPARE = REPO_ROOT / "parity_compare.py"


def _load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _selected_cases(manifest: dict, wave: str | None) -> list[dict]:
    cases = manifest["cases"]
    if not wave:
        return cases
    return [case for case in cases if case.get("wave") == wave]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--wave", default="", help="Optional wave name from the manifest.")
    parser.add_argument("--start", default="2025-01-01")
    parser.add_argument("--end", default="2025-12-31")
    parser.add_argument("--retries", type=int, default=2, help="Extra retries per case on nonzero exit / mismatch.")
    parser.add_argument("--retry-delay-seconds", type=float, default=5.0)
    parser.add_argument("--summary-json", default="reports/close_only_canonical_rerun_summary.json")
    parser.add_argument("--summary-csv", default="reports/close_only_canonical_rerun_summary.csv")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest = _load_manifest(manifest_path)
    wave = args.wave or None
    cases = _selected_cases(manifest, wave)
    if not cases:
        print(f"No cases selected from manifest: {manifest_path}")
        return 1

    summary_rows: list[dict[str, object]] = []
    overall_ok = True
    started_at = datetime.now(timezone.utc).isoformat()

    for case in cases:
        case_id = str(case["id"])
        expected_trades = int(case["expected_trades"])
        print(f"=== {case_id} ===")
        report_path = REPO_ROOT / f"reports/tracker_cases/{case_id}/parity_compare.json"
        verdict = "ERROR"
        trade_count = None
        result_returncode = 1
        attempts = 0
        ok = False

        while attempts <= args.retries and not ok:
            attempts += 1
            cmd = [
                sys.executable,
                str(PARITY_COMPARE),
                "--fetch-fresh",
                "--start",
                args.start,
                "--end",
                args.end,
                "--tracker-case",
                case_id,
            ]
            attempt_started = datetime.now(timezone.utc).timestamp()
            result = subprocess.run(cmd, cwd=REPO_ROOT)
            result_returncode = result.returncode
            verdict = "ERROR"
            trade_count = None
            if report_path.exists() and report_path.stat().st_mtime >= attempt_started - 1.0:
                report = json.loads(report_path.read_text(encoding="utf-8"))
                verdict = str(report.get("verdict", "ERROR"))
                for metric in report.get("metrics", []):
                    if metric.get("key") == "total_trades":
                        trade_count = int(metric.get("pine", 0))
                        break
            ok = result_returncode == 0 and verdict == "PASS" and trade_count == expected_trades
            if not ok and attempts <= args.retries:
                print(f"Retrying {case_id} in {args.retry_delay_seconds:.1f}s (attempt {attempts}/{args.retries + 1})")
                time.sleep(args.retry_delay_seconds)

        overall_ok = overall_ok and ok
        summary_rows.append(
            {
                "case_id": case_id,
                "wave": case.get("wave", ""),
                "expected_trades": expected_trades,
                "actual_trades": trade_count if trade_count is not None else "",
                "verdict": verdict,
                "returncode": result_returncode,
                "attempts": attempts,
                "status": "PASS" if ok else "FAIL",
            }
        )

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "started_at": started_at,
        "manifest": str(manifest_path),
        "wave": wave or "all",
        "profile": manifest.get("profile", ""),
        "status": "PASS" if overall_ok else "FAIL",
        "cases": summary_rows,
    }

    summary_json_path = REPO_ROOT / args.summary_json
    summary_csv_path = REPO_ROOT / args.summary_csv
    summary_json_path.parent.mkdir(parents=True, exist_ok=True)
    summary_csv_path.parent.mkdir(parents=True, exist_ok=True)
    summary_json_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    with summary_csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["case_id", "wave", "expected_trades", "actual_trades", "verdict", "returncode", "attempts", "status"],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Saved summary: {summary_json_path}")
    print(f"Saved summary CSV: {summary_csv_path}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
