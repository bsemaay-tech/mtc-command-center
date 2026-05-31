#!/usr/bin/env python3
"""
Setup Check for Core-2 Cases (all cases beyond Core-1).

Dynamically discovers all case JSONs and validates TV XLSX setup.
"""

import json
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple, Optional, List
import openpyxl

def read_tv_properties(xlsx_path: Path) -> Dict[str, str]:
    """Read Properties sheet from TV XLSX."""
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
    if value in ("on", "yes", "true", "enabled"):
        return "On"
    if value in ("off", "no", "false", "disabled"):
        return "Off"
    return value.strip()

def compare_values(tv_value: str, expected_value: str) -> bool:
    """Compare TV value with expected value."""
    tv_norm = normalize_value(tv_value)
    exp_norm = normalize_value(expected_value)

    if tv_norm == exp_norm:
        return True

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
        print(f"  ERROR loading {case_json_path}: {e}")
        return None

def find_tv_xlsx(run_order: int, case_id: str, tv_inputs_base: Path) -> Optional[Path]:
    """Find TV XLSX file in case folder."""
    case_folder = tv_inputs_base / f"{run_order:03d}_{case_id}"
    if not case_folder.exists():
        return None
    xlsx_files = list(case_folder.glob("*.xlsx"))
    return xlsx_files[0] if xlsx_files else None

def check_case(run_order: int, case_id: str, cases_base: Path, tv_inputs_base: Path) -> Tuple[str, str, str]:
    """Check a single case. Returns (status, primary_check_detail, notes)."""
    tv_xlsx_path = find_tv_xlsx(run_order, case_id, tv_inputs_base)
    if not tv_xlsx_path:
        return "NO_FILE", "", f"No XLSX file found in {run_order:03d}_{case_id}/"

    case_json_path = cases_base / f"{case_id}.json"
    case_data = load_case_json(case_json_path)
    if not case_data:
        return "NO_FILE", "", f"Cannot load case JSON: {case_json_path}"

    tv_props = read_tv_properties(tv_xlsx_path)
    if not tv_props:
        return "FAIL", "", f"Cannot read Properties from {tv_xlsx_path.name}"

    # Extract expected settings
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
        primary_status = f"FAIL ('{primary_input_name}' not found)"
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
            parent_failures.append(f"{parent_name}: not found")

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

def discover_cases(cases_base: Path) -> List[Tuple[int, str]]:
    """Discover all cases from case JSON files."""
    cases = []
    for case_json in sorted(cases_base.glob("*.json")):
        case_id = case_json.stem
        # Try to extract run_order from TV folder naming
        tv_inputs_base = cases_base.parent / "tv_manual_inputs"
        for tv_folder in tv_inputs_base.glob("*_*"):
            folder_name = tv_folder.name
            parts = folder_name.split("_", 1)
            if len(parts) == 2 and parts[1] == case_id:
                try:
                    run_order = int(parts[0])
                    cases.append((run_order, case_id))
                    break
                except ValueError:
                    pass
    return sorted(cases)

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

    # Discover all cases
    all_cases = discover_cases(cases_base)
    print(f"Discovered {len(all_cases)} total cases")
    print()

    results = []
    pass_count = 0
    fail_count = 0
    no_file_count = 0

    for run_order, case_id in all_cases:
        print(f"[{run_order:03d}] {case_id}...", end=" ", flush=True)
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
    csv_path = compare_runs_base / "all_setup_check.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run_order", "case_id", "status", "primary_detail", "notes"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Results written to: {csv_path}")

    # Summary by status
    pass_cases = [r for r in results if r["status"] == "PASS"]
    fail_cases = [r for r in results if r["status"] == "FAIL"]

    if pass_cases:
        print(f"\n{len(pass_cases)} PASS cases (ready for backtest)")
        if len(pass_cases) <= 50:
            for r in pass_cases:
                print(f"  {r['run_order']:03d} {r['case_id']}")
        else:
            for r in pass_cases[:10]:
                print(f"  {r['run_order']:03d} {r['case_id']}")
            print(f"  ... ({len(pass_cases) - 20} more)")
            for r in pass_cases[-10:]:
                print(f"  {r['run_order']:03d} {r['case_id']}")

    if fail_cases:
        print(f"\n{len(fail_cases)} FAIL cases (setup issues):")
        for r in fail_cases[:20]:
            print(f"  {r['run_order']:03d} {r['case_id']}")
            if r["notes"]:
                print(f"       {r['notes']}")
        if len(fail_cases) > 20:
            print(f"  ... ({len(fail_cases) - 20} more)")

if __name__ == "__main__":
    main()
