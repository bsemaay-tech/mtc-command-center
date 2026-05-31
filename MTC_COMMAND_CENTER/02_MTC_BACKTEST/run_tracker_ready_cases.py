from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
TRACKER_CSV = REPO_ROOT / "MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/MTC_V2_PARITY_CASES.csv"


def load_ready_cases() -> list[dict[str, str]]:
    with TRACKER_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ready = [row for row in rows if str(row.get("status", "")).strip() == "READY_FOR_AUTO"]
    ready.sort(key=lambda row: int(float(str(row.get("run_order") or "999999"))))
    return ready


def main() -> int:
    ready_cases = load_ready_cases()
    if not ready_cases:
        print("No READY_FOR_AUTO tracker cases found.")
        return 0

    print(f"Running {len(ready_cases)} READY_FOR_AUTO tracker cases...")
    failures: list[str] = []

    for index, row in enumerate(ready_cases, start=1):
        case_id = str(row["case_id"]).strip()
        print(f"\n[{index}/{len(ready_cases)}] {case_id} :: {row.get('primary_change', '')}")
        cmd = [
            sys.executable,
            "parity_compare.py",
            "--fetch-fresh",
            "--tracker-case",
            case_id,
            "--tracker-agent",
            "Codex",
        ]
        result = subprocess.run(cmd, cwd=SCRIPT_DIR)
        if result.returncode != 0:
            failures.append(case_id)

    print("\n=== Tracker Ready Case Run Summary ===")
    print(f"Total   : {len(ready_cases)}")
    print(f"Failed  : {len(failures)}")
    if failures:
        print("Cases   : " + ", ".join(failures))
        return 1

    print("All READY_FOR_AUTO cases completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
