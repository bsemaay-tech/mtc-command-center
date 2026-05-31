#!/usr/bin/env python3
"""
Check Setup for Core-1 Cases (Seq 059-080 boundary cases)

Validates that TV XLSX Properties match expected case JSON configurations.
Outputs: core1_setup_check.csv with PASS/FAIL/NO_FILE status per case.
"""

import json
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple, Optional, List
import openpyxl

# Core-1 cases to check (20 total)
CORE1_CASES = [
    (135, "parity_core_059_tp_mode_single_tp_v01"),
    (136, "parity_bnd_059_tp_mode_single_tp_v02"),
    (137, "parity_bnd_059_tp_mode_single_tp_v03"),
    (138, "parity_core_060_tp_distance_v01"),
    (139, "parity_bnd_060_tp_distance_v02"),
    (140, "parity_bnd_060_tp_distance_v03"),
    (141, "parity_core_061_tp_r_multiple_single_tp_v01"),
    (142, "parity_bnd_061_tp_r_multiple_single_tp_v02"),
    (143, "parity_bnd_061_tp_r_multiple_single_tp_v03"),
    (153, "parity_bnd_066_tp2_at_r_multiple_v02"),
    (154, "parity_bnd_066_tp2_at_r_multiple_v03"),
    (174, "parity_bnd_073_be_trigger_r_multiple_v02"),
    (175, "parity_bnd_073_be_trigger_r_multiple_v03"),
    (177, "parity_bnd_074_be_buffer_r_multiple_v02"),
    (183, "parity_bnd_076_tp1_close_of_position_v02"),
    (184, "parity_bnd_076_tp1_close_of_position_v03"),
    (191, "parity_bnd_079_start_after_r_multiple_v02"),
    (192, "parity_bnd_079_start_after_r_multiple_v03"),
    (194, "parity_bnd_080_trail_distance_r_multiple_v02"),
    (195, "parity_bnd_080_trail_distance_r_multiple_v03"),
]

def read_tv_properties(xlsx_path: Path) -> Dict[str, str]:
    """Read Properties sheet from TV XLSX. Returns {name: value} dict."""
    props = {}
    try:
        wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
        ws = wb["Properties"]
        for row in ws.iter_rows(values_only=True):
            if row[0] and row[1] is not None:
                name = str(row[0]).strip()
                value = str(row[1]).strip()
                props[name] = value
        wb.close()
    except Exception as e:
        print(f"  ERROR reading {xlsx_path}: {e}")
        return {}
    return props

def normalize_value(value: str) -> str:
    """Normalize TV property value for comparison."""
    if not value:
        return ""
    value = value.strip().lower()
    # "On" / "Off" normalization
    if value in ("on", "yes", "true", "enabled"):
        return "On"
    if value in ("off", "no", "false", "disabled"):
        return "Off"
    # Keep numeric values as-is
    return value.strip()

def compare_values(tv_value: str, expected_value: str) -> bool:
    """Compare TV value with expected value (case-insensitive, numeric with epsilon)."""
    tv_norm = normalize_value(tv_value)
    exp_norm = normalize_value(expected_value)

    if tv_norm == exp_norm:
        return True

    # Try float comparison with epsilon
    try:
        tv_float = float(tv_value)
        exp_float = float(expected_value)
        return abs(tv_float - exp_float) < 0.001
    except (ValueError, TypeError):
        return False

def parse_case_datetime(raw: str) -> Optional[datetime]:
    """Parse case JSON datetime as UTC."""
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def parse_tv_range(raw: str, tv_tz: str) -> Tuple[Optional[datetime], Optional[datetime]]:
    """Parse TV 'Trading range' string into UTC datetimes."""
    if not raw or "—" not in raw:
        return None, None
    import zoneinfo
    tz = zoneinfo.ZoneInfo(tv_tz)
    start_raw, end_raw = [part.strip() for part in raw.split("—", 1)]
    try:
        start_dt = datetime.strptime(start_raw, "%b %d, %Y, %H:%M").replace(tzinfo=tz).astimezone(timezone.utc)
        end_dt = datetime.strptime(end_raw, "%b %d, %Y, %H:%M").replace(tzinfo=tz).astimezone(timezone.utc)
    except ValueError:
        return None, None
    return start_dt, end_dt

def load_case_json(case_json_path: Path) -> Optional[Dict]:
    """Load case JSON file."""
    try:
        with open(case_json_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"  ERROR loading case JSON {case_json_path}: {e}")
        return None

def find_tv_xlsx(run_order: int, case_id: str, tv_inputs_base: Path) -> Optional[Path]:
    """Find TV XLSX file in the case's folder."""
    case_folder = tv_inputs_base / f"{run_order:03d}_{case_id}"
    if not case_folder.exists():
        return None

    # Look for .xlsx file in the folder
    xlsx_files = list(case_folder.glob("*.xlsx"))
    if xlsx_files:
        return xlsx_files[0]
    return None

def check_case(run_order: int, case_id: str, cases_base: Path, tv_inputs_base: Path) -> Tuple[str, str, str]:
    """
    Check a single case. Returns (status, primary_check_detail, notes).
    Status: PASS, FAIL, NO_FILE
    """
    # Find TV XLSX
    tv_xlsx_path = find_tv_xlsx(run_order, case_id, tv_inputs_base)
    if not tv_xlsx_path:
        return "NO_FILE", "", f"No XLSX file found in {run_order:03d}_{case_id}/"

    # Load case JSON
    case_json_path = cases_base / f"{case_id}.json"
    case_data = load_case_json(case_json_path)
    if not case_data:
        return "NO_FILE", "", f"Cannot load case JSON: {case_json_path}"

    # Read TV properties
    tv_props = read_tv_properties(tv_xlsx_path)
    if not tv_props:
        return "FAIL", "", f"Cannot read Properties from {tv_xlsx_path.name}"

    # Extract expected settings from case JSON
    generated = case_data.get("_generated", {})
    primary_input_name = generated.get("source_input_name", "")
    primary_target_value = generated.get("source_target_value", "")

    tv_case = case_data.get("_tv_case", {})
    parents = tv_case.get("parents", [])
    tv_tz = case_data.get("tv_tz", "UTC")

    # Check primary setting
    primary_status = "FAIL"
    if primary_input_name and primary_input_name in tv_props:
        tv_value = tv_props[primary_input_name]
        if compare_values(tv_value, primary_target_value):
            primary_status = "PASS"
        else:
            primary_status = f"FAIL (expected '{primary_target_value}', got '{tv_value}')"
    elif primary_input_name:
        primary_status = f"FAIL ('{primary_input_name}' not found in Properties)"
    else:
        primary_status = "UNKNOWN"

    # Check parent conditions
    parent_failures = []
    for parent in parents:
        parent_name = parent.get("name", "")
        parent_value = parent.get("value", "")
        if parent_name in tv_props:
            tv_value = tv_props[parent_name]
            if not compare_values(tv_value, parent_value):
                parent_failures.append(f"{parent_name}: expected '{parent_value}', got '{tv_value}'")
        else:
            parent_failures.append(f"{parent_name}: not found in Properties")

    range_failures = []
    trading_range = tv_props.get("Trading range", "")
    tv_start_dt, tv_end_dt = parse_tv_range(trading_range, tv_tz)
    case_start_dt = parse_case_datetime(case_data.get("start_date", ""))
    case_end_dt = parse_case_datetime(case_data.get("end_date", ""))
    if trading_range:
        if tv_start_dt is None or tv_end_dt is None:
            range_failures.append(f"Trading range parse failed: '{trading_range}'")
        else:
            if case_start_dt is not None and tv_start_dt != case_start_dt:
                range_failures.append(
                    f"Trading range start mismatch: case {case_start_dt.isoformat()} vs TV {tv_start_dt.isoformat()}"
                )
            if case_end_dt is not None and tv_end_dt != case_end_dt:
                range_failures.append(
                    f"Trading range end mismatch: case {case_end_dt.isoformat()} vs TV {tv_end_dt.isoformat()}"
                )

    # Overall status
    overall_status = "PASS"
    notes = ""

    if "FAIL" in str(primary_status):
        overall_status = "FAIL"
        notes = f"Primary: {primary_status}"

    if parent_failures:
        overall_status = "FAIL"
        if notes:
            notes += "; "
        notes += f"Parents: {'; '.join(parent_failures)}"

    if range_failures:
        overall_status = "FAIL"
        if notes:
            notes += "; "
        notes += f"Range: {'; '.join(range_failures)}"

    return overall_status, primary_status, notes

def main():
    base_path = Path(__file__).parent.parent
    cases_base = base_path / "cases"
    tv_inputs_base = base_path / "tv_manual_inputs"
    compare_runs_base = base_path / "compare_runs"

    if not cases_base.exists():
        print(f"ERROR: cases directory not found: {cases_base}")
        return

    if not tv_inputs_base.exists():
        print(f"ERROR: tv_manual_inputs directory not found: {tv_inputs_base}")
        return

    compare_runs_base.mkdir(exist_ok=True)

    print(f"Checking {len(CORE1_CASES)} Core-1 cases...")
    print(f"Cases base: {cases_base}")
    print(f"TV inputs base: {tv_inputs_base}")
    print()

    results = []
    pass_count = 0
    fail_count = 0
    no_file_count = 0

    for run_order, case_id in CORE1_CASES:
        print(f"[{run_order:03d}] {case_id}...", end=" ")
        status, primary_detail, notes = check_case(run_order, case_id, cases_base, tv_inputs_base)

        if status == "PASS":
            print("[PASS]")
            pass_count += 1
        elif status == "NO_FILE":
            print("[NO_FILE]")
            no_file_count += 1
        else:
            print("[FAIL]")
            fail_count += 1

        results.append({
            "run_order": run_order,
            "case_id": case_id,
            "status": status,
            "primary_detail": primary_detail,
            "notes": notes,
        })

    print()
    print(f"Summary: {pass_count} PASS, {fail_count} FAIL, {no_file_count} NO_FILE")
    print()

    # Write CSV
    csv_path = compare_runs_base / "core1_setup_check.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run_order", "case_id", "status", "primary_detail", "notes"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Results written to: {csv_path}")

    # Summary by status
    print()
    print("PASS cases:")
    for r in results:
        if r["status"] == "PASS":
            print(f"  {r['run_order']:03d} {r['case_id']}")

    print("\nFAIL cases:")
    for r in results:
        if r["status"] == "FAIL":
            print(f"  {r['run_order']:03d} {r['case_id']}")
            if r["notes"]:
                print(f"       {r['notes']}")

    print("\nNO_FILE cases:")
    for r in results:
        if r["status"] == "NO_FILE":
            print(f"  {r['run_order']:03d} {r['case_id']}")

if __name__ == "__main__":
    main()
