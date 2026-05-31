#!/usr/bin/env python
"""
Build a reproducible workbook-variant parity case from an existing case JSON.

Narrow scope by design:
- clones an existing case
- stamps replay-specific metadata/overrides for workbook forensics
- does not parse XLSX or alter engine logic
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PROJECT_ROOT.parent


def _abs(path_like: str) -> Path:
    p = Path(path_like)
    return p if p.is_absolute() else (REPO_ROOT / p).resolve()


def _to_runner_path(path_like: str) -> str:
    """Normalize paths for run_case.py path resolution.

    Prefer project-root-relative paths for files under mtc_backtest so generated
    cases remain portable. Fall back to absolute paths for assets outside the
    project tree (for example 110_/data mirrors).
    """
    p = _abs(path_like)
    try:
        return p.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(p.as_posix())


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid JSON payload: {path}")
    return payload


def _parse_bool(text: str) -> bool:
    value = text.strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value: {text}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build workbook-variant replay case JSON.")
    ap.add_argument("--base-case", required=True, help="Existing case JSON path")
    ap.add_argument("--out", required=True, help="Output case JSON path")
    ap.add_argument("--dataset", help="Override dataset path")
    ap.add_argument("--start-date", help="Override evaluation start date (UTC ISO)")
    ap.add_argument("--end-date", help="Override evaluation end date (UTC ISO)")
    ap.add_argument("--tv-csv", help="Override TV CSV path")
    ap.add_argument("--tv-tz", help="Override TV timezone")
    ap.add_argument("--workbook", help="Source workbook path for metadata only")
    ap.add_argument("--effective-history-start-utc", help="Metadata only; replay history start")
    ap.add_argument("--dataset-available-end-utc", help="Metadata only; local dataset max timestamp")
    ap.add_argument("--debug-dir", help="Override config.parity.debug_dir")
    ap.add_argument(
        "--force-terminal-manual-close",
        default="true",
        help="Set config.parity.force_terminal_manual_close (true/false). Default: true",
    )
    ap.add_argument("--comment", help="Override top-level _comment")
    args = ap.parse_args()

    base_case_path = _abs(args.base_case)
    out_path = _abs(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    case = _load_json(base_case_path)

    if args.dataset:
        case["dataset"] = _to_runner_path(args.dataset)
    if args.start_date:
        case["start_date"] = args.start_date
    if args.end_date:
        case["end_date"] = args.end_date
    if args.tv_csv:
        case["tv_csv"] = _to_runner_path(args.tv_csv)
    if args.tv_tz:
        case["tv_tz"] = args.tv_tz
    if args.comment:
        case["_comment"] = args.comment

    cfg = case.setdefault("config", {})
    parity = cfg.setdefault("parity", {})
    parity["force_terminal_manual_close"] = _parse_bool(args.force_terminal_manual_close)
    if args.debug_dir:
        parity["debug_dir"] = _to_runner_path(args.debug_dir)

    replay = case.setdefault("_workbook_replay", {})
    replay["built_at_utc"] = datetime.now(timezone.utc).isoformat()
    replay["built_from_case"] = _to_runner_path(str(base_case_path))
    if args.workbook:
        replay["source_workbook"] = _to_runner_path(args.workbook)
    if args.effective_history_start_utc:
        replay["effective_history_start_utc"] = args.effective_history_start_utc
    if args.dataset_available_end_utc:
        replay["dataset_available_end_utc"] = args.dataset_available_end_utc

    out_path.write_text(json.dumps(case, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"built_case={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
