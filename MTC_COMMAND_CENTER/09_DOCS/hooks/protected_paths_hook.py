#!/usr/bin/env python
"""Pre-commit guard for MCC protected paths."""

import json
import re
import subprocess
import sys
from pathlib import Path

MCC_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = MCC_ROOT.parent
POLICY = MCC_ROOT / "09_DOCS" / "PROTECTED_PATHS_POLICY.md"
TASK_HISTORY = MCC_ROOT / "02_TASKS" / "TASK_HISTORY.json"
HARDCODED_PATH_AUDIT = MCC_ROOT / "03_QUANTLENS" / "tools" / "audit_hardcoded_paths.py"


def staged_paths() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def protected_patterns() -> list[str]:
    defaults = [
        "MTC_V2.pine",
        "01_MASTER TEMPLATE_V2/01_PINE/",
        "01_MASTER TEMPLATE_V2/00_PYTHON/",
        "01_MASTER TEMPLATE_V2/05_PARITY/",
        "MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md",
    ]
    if not POLICY.exists():
        return defaults
    text = POLICY.read_text(encoding="utf-8")
    return defaults + [line.strip() for line in text.splitlines() if line.strip().startswith("01_MASTER")]


def touches_protected(path: str, patterns: list[str]) -> bool:
    return any(pattern in path for pattern in patterns)


def approved_task_exists(task_id: str) -> bool:
    if not TASK_HISTORY.exists():
        return False
    history = json.loads(TASK_HISTORY.read_text(encoding="utf-8"))
    for event in history.get("events", []):
        if event.get("task_id") == task_id and event.get("event_type") in {"APPROVED", "COMPLETED"}:
            return True
    return False


def commit_message() -> str:
    msg_file = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if msg_file and msg_file.exists():
        return msg_file.read_text(encoding="utf-8", errors="replace")
    return ""


def main() -> int:
    if HARDCODED_PATH_AUDIT.exists():
        audit = subprocess.run(
            [sys.executable, str(HARDCODED_PATH_AUDIT), "--staged"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if audit.returncode != 0:
            print(audit.stdout.strip())
            if audit.stderr.strip():
                print(audit.stderr.strip())
            return audit.returncode

    protected = [p for p in staged_paths() if touches_protected(p, protected_patterns())]
    if not protected:
        return 0

    token = re.search(r"APPROVED-PATCH-PLAN:\s*([A-Za-z0-9_.-]+)", commit_message())
    if token and approved_task_exists(token.group(1)):
        return 0

    print("Protected path commit blocked. Required token: APPROVED-PATCH-PLAN: <task_id>")
    for path in protected:
        print(f" - {path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
