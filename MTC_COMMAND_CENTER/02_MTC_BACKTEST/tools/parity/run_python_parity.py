from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "01_MASTER TEMPLATE_V2" / "05_PARITY" / "_nightly"


def run_case(case: dict) -> dict:
    case_dir = REPO_ROOT / case["folder"] if case.get("folder") else None
    case_plan = {}
    if case_dir and (case_dir / "case_plan.json").exists():
        case_plan = json.loads((case_dir / "case_plan.json").read_text(encoding="utf-8"))
    raw_case_no = str(case.get("case_no", "")).strip()
    tracker_case = raw_case_no if raw_case_no.startswith("case_") else f"case_{int(raw_case_no):03d}"
    case_overrides = case_plan.get("planned_overrides", {})
    overrides_path = OUTPUT_DIR / "case_overrides" / f"{tracker_case}.json"
    overrides_path.parent.mkdir(parents=True, exist_ok=True)
    overrides_path.write_text(json.dumps(case_overrides, ensure_ascii=False, indent=2), encoding="utf-8")
    cmd = [
        sys.executable,
        str(REPO_ROOT / "parity_compare.py"),
        "--fetch-fresh",
        "--case",
        str(overrides_path),
        "--tracker-case",
        tracker_case,
        "--tracker-agent",
        "Codex",
    ]
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    compare_path = REPO_ROOT / "reports" / "tracker_cases" / tracker_case / "parity_compare.json"
    structured = {}
    if compare_path.exists():
        try:
            structured = json.loads(compare_path.read_text(encoding="utf-8"))
        except Exception:
            structured = {}
    return {
        "case_no": case["case_no"],
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "status": "OK" if proc.returncode == 0 else "ERROR",
        "report": structured,
    }


def main() -> int:
    raise SystemExit("Use run_planned_cases.py to orchestrate cases.")


if __name__ == "__main__":
    raise SystemExit(main())
