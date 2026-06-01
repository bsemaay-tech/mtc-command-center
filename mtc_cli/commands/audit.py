"""
mtc audit repo — read-only repo health snapshot.

Checks:
  - Required AI memory files present
  - Git index clean (no staged changes)
  - Overnight loop heartbeat age
  - NEXT_STEPS has no stale in-progress tasks
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

from mtc_cli.contract import Envelope

# Repo root = 2 levels up from this file (mtc_cli/commands/audit.py)
REPO_ROOT = Path(__file__).resolve().parents[2]
MCC       = REPO_ROOT / "MTC_COMMAND_CENTER"
AI_MEM    = MCC / "_AI_MEMORY"

REQUIRED_MEMORY_FILES = [
    AI_MEM / "START_HERE.md",
    AI_MEM / "AI_RULES.md",
    AI_MEM / "GLOBAL_HANDOFF.md",
    AI_MEM / "NEXT_STEPS.md",
    AI_MEM / "PROJECT_MEMORY.md",
    AI_MEM / "ACTIVE_FILES.md",
]

HEARTBEAT_PATH = MCC / "03_QUANTLENS" / "tools" / "overnight_runs" / "_heartbeat_night.json"
HEARTBEAT_STALE_MINUTES = 30


def run(as_json: bool = False) -> Envelope:
    findings = []
    data: dict = {}

    # --- 1. Required memory files ---
    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(REPO_ROOT))
        except ValueError:
            return str(p)

    missing = [_rel(f) for f in REQUIRED_MEMORY_FILES if not f.exists()]
    if missing:
        for m in missing:
            findings.append({"severity": "ERROR", "message": f"missing: {m}"})
    data["memory_files_ok"] = len(missing) == 0

    # --- 2. Git status (staged changes only — doesn't block but warns) ---
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=10
        )
        staged = [l for l in result.stdout.splitlines() if l.strip()]
        data["git_staged_count"] = len(staged)
        if staged:
            findings.append({
                "severity": "WARN",
                "message": f"{len(staged)} staged files not yet committed",
                "files": staged[:10],
            })
    except Exception as exc:
        findings.append({"severity": "WARN", "message": f"git check failed: {exc}"})
        data["git_staged_count"] = None

    # --- 3. Overnight loop heartbeat ---
    if HEARTBEAT_PATH.exists():
        try:
            hb = json.loads(HEARTBEAT_PATH.read_text(encoding="utf-8"))
            ts_str = hb.get("ts", "")
            if ts_str:
                from datetime import datetime, timezone
                ts = datetime.fromisoformat(ts_str)
                age_min = (datetime.now(timezone.utc) - ts).total_seconds() / 60
                data["heartbeat_age_minutes"] = round(age_min, 1)
                data["heartbeat_iter"] = hb.get("iter")
                data["heartbeat_passes"] = hb.get("passes")
                if age_min > HEARTBEAT_STALE_MINUTES:
                    findings.append({
                        "severity": "WARN",
                        "message": f"overnight loop heartbeat stale ({age_min:.0f} min old)",
                    })
            else:
                data["heartbeat_age_minutes"] = None
        except Exception as exc:
            data["heartbeat_error"] = str(exc)
    else:
        data["heartbeat_age_minutes"] = None

    # --- 4. NEXT_STEPS stale in-progress check ---
    next_steps = AI_MEM / "NEXT_STEPS.md"
    if next_steps.exists():
        content = next_steps.read_text(encoding="utf-8")
        in_progress_lines = [
            l.strip() for l in content.splitlines()
            if "| IN_PROGRESS |" in l or "IN_PROGRESS" in l
        ]
        data["next_steps_in_progress"] = len(in_progress_lines)
    else:
        data["next_steps_in_progress"] = None

    ok = not any(f["severity"] == "ERROR" for f in findings)
    return Envelope(
        ok=ok,
        command="audit repo",
        data=data,
        findings=findings,
    )
