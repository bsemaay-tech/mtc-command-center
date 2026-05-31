from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from dataclasses import asdict
import csv
from pathlib import Path

from build_case_queue import QUEUE_PATH, STATE_PATH, build_queue
from compare_case import compare_case
from read_tracker import read_tracker
from run_python_parity import run_case as run_python_case
from tw_apply_case import apply_case
from tw_collect_result import collect_case
from write_report import write_report


REPO_ROOT = Path(__file__).resolve().parents[4]
BACKTEST_ROOT = Path(__file__).resolve().parents[2]
V2_PARITY = REPO_ROOT / "MTC_COMMAND_CENTER" / "01_MTC_PROJECT" / "05_PARITY"
OUTPUT_DIR = V2_PARITY / "_nightly"
LOG_DIR = OUTPUT_DIR / "logs"
CASE_DIR = OUTPUT_DIR / "cases"
TRACKER_CSV = V2_PARITY / "MTC_V2_PARITY_CASES.csv"
TRACKER_SOURCE_CSV = V2_PARITY / "MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv"


def _load_plan(case_no: str) -> dict:
    folder = V2_PARITY / "TW_EXPORT_CASES_V2" / case_no
    return json.loads((folder / "case_plan.json").read_text(encoding="utf-8"))


def _save_case_log(case_no: str, payload: dict) -> None:
    (CASE_DIR / case_no).mkdir(parents=True, exist_ok=True)
    (CASE_DIR / case_no / "case_result.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _materialize_tracker_csv() -> None:
    if not TRACKER_SOURCE_CSV.exists():
        return
    with TRACKER_SOURCE_CSV.open(encoding="utf-8", newline="") as src:
        reader = csv.DictReader(src)
        rows = list(reader)
    if not rows:
        return
    fieldnames = ["case_id", "symbol", "timeframe", "bars", *[name for name in reader.fieldnames or [] if name != "case_no"]]
    with TRACKER_CSV.open("w", encoding="utf-8", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["case_id"] = str(row.get("case_no") or row.get("\ufeffcase_no") or "").strip()
            out.setdefault("symbol", "BTCUSDT.P")
            out.setdefault("timeframe", "60")
            out.setdefault("bars", "1000")
            writer.writerow({k: out.get(k, "") for k in fieldnames})


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    CASE_DIR.mkdir(parents=True, exist_ok=True)
    _materialize_tracker_csv()
    queue = build_queue(read_tracker(), resume=True)
    QUEUE_PATH.write_text(json.dumps([asdict(q) for q in queue], ensure_ascii=False, indent=2), encoding="utf-8")

    results: list[dict] = []
    completed = []
    for item in queue:
        case_plan = _load_plan(item.case_no)
        started = datetime.utcnow().isoformat() + "Z"
        try:
            tv_result = apply_case(case_plan)
            tv_collect = collect_case(case_plan)
            py_result = run_python_case(case_plan)
            cmp = compare_case(tv_collect, py_result)
            status = cmp.status
            payload = {
                "case_no": item.case_no,
                "status": status,
                "started_at": started,
                "tv_apply": tv_result,
                "tv_collect": tv_collect,
                "python": py_result,
                "compare": asdict(cmp),
            }
        except Exception as exc:
            status = "ERROR"
            payload = {
                "case_no": item.case_no,
                "status": status,
                "started_at": started,
                "error": str(exc),
            }
        results.append(payload)
        completed.append(item.case_no)
        _save_case_log(item.case_no, payload)
        STATE_PATH.write_text(json.dumps({"completed_cases": completed}, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "total_planned": len(queue),
        "processed": len(results),
        "pass": sum(1 for r in results if r.get("status") == "PASS"),
        "fail": sum(1 for r in results if r.get("status") == "FAIL"),
        "partial": sum(1 for r in results if r.get("status") == "PARTIAL"),
        "error": sum(1 for r in results if r.get("status") == "ERROR"),
        "skipped": sum(1 for r in results if r.get("status") == "SKIPPED"),
        "manual_review": [r["case_no"] for r in results if r.get("status") != "PASS"],
    }
    write_report(OUTPUT_DIR, results, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
