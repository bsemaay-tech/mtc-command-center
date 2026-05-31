from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_DIR = REPO_ROOT / "MTC_COMMAND_CENTER" / "01_MTC_PROJECT" / "05_PARITY" / "_nightly"


def apply_case(case: dict, dry_run: bool = False) -> dict:
    # Thin browser layer only. Case-specific TradingView UI input application is
    # intentionally kept narrow and resumable.
    result = {
        "case_no": case["case_no"],
        "status": "SKIPPED",
        "note": "TradingView input application is intentionally thin; current run assumes chart/code are already loaded.",
        "applied": {},
    }
    if dry_run:
        result["status"] = "DRY_RUN"
    return result


def main() -> int:
    raise SystemExit("Use run_planned_cases.py to orchestrate cases.")


if __name__ == "__main__":
    raise SystemExit(main())
