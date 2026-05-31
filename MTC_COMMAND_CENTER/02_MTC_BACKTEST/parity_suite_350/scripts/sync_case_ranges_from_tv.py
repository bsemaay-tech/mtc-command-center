#!/usr/bin/env python3
"""
Sync case JSON start/end dates from downloaded TV XLSX Trading range.

Only updates cases that already have an XLSX in `tv_manual_inputs/<run_order>_<case_id>/`.
Trading range is treated as authoritative because parity runs should follow the
actual TV export window, not a stale manifest default.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple
import zoneinfo

import openpyxl


def read_tv_properties(xlsx_path: Path) -> dict[str, str]:
    props: dict[str, str] = {}
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    try:
        ws = wb["Properties"]
        for row in ws.iter_rows(values_only=True):
            if row[0] and row[1] is not None:
                props[str(row[0]).strip()] = str(row[1]).strip()
    finally:
        wb.close()
    return props


def parse_tv_range(raw: str, tv_tz: str) -> Tuple[Optional[datetime], Optional[datetime]]:
    if not raw:
        return None, None
    normalized = raw.replace("—", "?").replace("–", "?").replace("???", "?")
    if "?" not in normalized:
        return None, None
    start_raw, end_raw = [part.strip() for part in normalized.split("?", 1)]
    tz = zoneinfo.ZoneInfo(tv_tz)
    try:
        start_dt = datetime.strptime(start_raw, "%b %d, %Y, %H:%M").replace(tzinfo=tz).astimezone(timezone.utc)
        end_dt = datetime.strptime(end_raw, "%b %d, %Y, %H:%M").replace(tzinfo=tz).astimezone(timezone.utc)
    except ValueError:
        return None, None
    return start_dt, end_dt


def fmt_case_dt(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def main() -> None:
    suite_root = Path(__file__).resolve().parent.parent
    cases_dir = suite_root / "cases"
    tv_inputs_dir = suite_root / "tv_manual_inputs"

    updated = 0
    skipped = 0

    for case_json in sorted(cases_dir.glob("*.json")):
        case_id = case_json.stem
        matches = list(tv_inputs_dir.glob(f"*_{case_id}"))
        if not matches:
            skipped += 1
            continue
        xlsx_files = list(matches[0].glob("*.xlsx"))
        if not xlsx_files:
            skipped += 1
            continue

        case = json.loads(case_json.read_text(encoding="utf-8"))
        tv_tz = case.get("tv_tz", "UTC")
        props = read_tv_properties(xlsx_files[0])
        trading_range = props.get("Trading range", "")
        start_dt, end_dt = parse_tv_range(trading_range, tv_tz)
        if start_dt is None or end_dt is None:
            skipped += 1
            continue

        new_start = fmt_case_dt(start_dt)
        new_end = fmt_case_dt(end_dt)
        old_start = case.get("start_date")
        old_end = case.get("end_date")
        if old_start == new_start and old_end == new_end:
            continue

        case["start_date"] = new_start
        case["end_date"] = new_end
        case_json.write_text(json.dumps(case, indent=2), encoding="utf-8")
        updated += 1
        print(f"UPDATED {case_id}: {old_start}..{old_end} -> {new_start}..{new_end}")

    print(f"\nDone. updated={updated} skipped={skipped}")


if __name__ == "__main__":
    main()
