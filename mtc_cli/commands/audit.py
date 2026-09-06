"""
mtc audit repo — read-only repo health snapshot.

Checks:
  - Required AI memory files present (router-era layout: current-state files
    only; see D002 / MAP97 and root AGENTS.md "Work and acceptance invariants")
  - Git index clean (no staged changes)
  - Overnight loop heartbeat age
  - Governance HANDOFF.md newest section carries NEXT ACTION / WAITING FOR OWNER
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

from mtc_cli.contract import Envelope

# Repo root = 2 levels up from this file (mtc_cli/commands/audit.py)
REPO_ROOT = Path(__file__).resolve().parents[2]
MCC       = REPO_ROOT / "MTC_COMMAND_CENTER"
AI_MEM    = MCC / "_AI_MEMORY"

# ---------------------------------------------------------------------------
# Required memory files — router-era layout (commit 552a41ec, 2026-08-25).
#
# GLOBAL_HANDOFF.md and NEXT_STEPS.md moved to `_AI_MEMORY/history/` (grep-on-
# demand archives) and are no longer current state. Current state now lives in
# the selected stage's capped HANDOFF.md, sticky decisions in root
# DECISIONS.md, and routing in root AGENTS.md / CONTEXT_MAP.md (D002, MAP97).
# Do not add the moved archive paths back here.
# ---------------------------------------------------------------------------
def _required_memory_files(root: Path) -> list[Path]:
    mcc = root / "MTC_COMMAND_CENTER"
    ai_mem = mcc / "_AI_MEMORY"
    return [
        root / "AGENTS.md",
        root / "CONTEXT_MAP.md",
        root / "DECISIONS.md",
        ai_mem / "START_HERE.md",
        ai_mem / "AI_RULES.md",
        ai_mem / "PROJECT_MEMORY.md",
        ai_mem / "ACTIVE_FILES.md",
        ai_mem / "SESSION_LOCK.md",
        mcc / "00_AGENT_PROTOCOLS" / "HANDOFF.md",
    ]


REQUIRED_MEMORY_FILES = _required_memory_files(REPO_ROOT)

HEARTBEAT_STALE_MINUTES = 30

# Governance stage handoff (MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md):
# newest-first sections separated by a top-level "## " heading. The newest
# section must carry a NEXT ACTION line and a WAITING FOR OWNER line — see
# root AGENTS.md "Keep truthful NEXT ACTION plus WAITING FOR OWNER/Nothing
# handoffs."
_SECTION_SPLIT_RE = re.compile(r"(?m)^## ")
_WAITING_NOTHING_RE = re.compile(r"^\s*nothing\b", re.IGNORECASE)


def _newest_section(handoff_text: str) -> str:
    parts = _SECTION_SPLIT_RE.split(handoff_text)
    # parts[0] is preamble before the first "## " heading (e.g. the H1 title).
    return parts[1] if len(parts) > 1 else handoff_text


def _handoff_next_action_count(section: str) -> int:
    return len(re.findall(r"NEXT ACTION", section))


def _handoff_waiting_for_owner_count(section: str) -> int:
    """Count WAITING FOR OWNER lines whose value is not 'Nothing ...'."""
    real = 0
    for line in section.splitlines():
        if "WAITING FOR OWNER" not in line:
            continue
        value = line.split("WAITING FOR OWNER", 1)[1]
        value = value.lstrip(":*").strip().rstrip(".").strip()
        if value and not _WAITING_NOTHING_RE.match(value):
            real += 1
    return real


def run(as_json: bool = False, repo_root: Path | str | None = None) -> Envelope:
    findings = []
    data: dict = {}

    root = Path(repo_root) if repo_root is not None else REPO_ROOT
    mcc = root / "MTC_COMMAND_CENTER"
    gov_handoff = mcc / "00_AGENT_PROTOCOLS" / "HANDOFF.md"
    heartbeat_path = mcc / "03_QUANTLENS" / "tools" / "overnight_runs" / "_heartbeat_night.json"

    # --- 1. Required memory files ---
    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(root))
        except ValueError:
            return str(p)

    # Use the patchable module-level list for the real repo root (existing
    # tests monkeypatch `audit_mod.REQUIRED_MEMORY_FILES`); recompute against
    # a fixture root explicitly so `repo_root=` callers get a rooted list.
    required_files = REQUIRED_MEMORY_FILES if repo_root is None else _required_memory_files(root)

    missing = [_rel(f) for f in required_files if not f.exists()]
    if missing:
        for m in missing:
            findings.append({"severity": "ERROR", "message": f"missing: {m}"})
    data["memory_files_ok"] = len(missing) == 0

    # --- 2. Git status (staged changes only — doesn't block but warns) ---
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=root, capture_output=True, text=True, timeout=10
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
    if heartbeat_path.exists():
        try:
            hb = json.loads(heartbeat_path.read_text(encoding="utf-8"))
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

    # --- 4. Governance HANDOFF.md next-action check ---
    # Replaces the pre-router "NEXT_STEPS stale in-progress" check, which
    # silently passed (next_steps_in_progress = None) once NEXT_STEPS.md moved
    # to history/. Current state now lives in the governance stage HANDOFF.md
    # (00_AGENT_PROTOCOLS/HANDOFF.md); a missing file or a newest section
    # missing NEXT ACTION / WAITING FOR OWNER is reported, never passed over.
    if not gov_handoff.exists():
        data["handoff_next_actions"] = None
        data["handoff_waiting_for_owner"] = None
        findings.append({
            "severity": "ERROR",
            "message": f"handoff check skipped: {_rel(gov_handoff)} not found",
        })
    else:
        section = _newest_section(gov_handoff.read_text(encoding="utf-8"))
        next_action_count = _handoff_next_action_count(section)
        waiting_count = _handoff_waiting_for_owner_count(section)
        data["handoff_next_actions"] = next_action_count
        data["handoff_waiting_for_owner"] = waiting_count
        if next_action_count == 0:
            findings.append({
                "severity": "ERROR",
                "message": f"{_rel(gov_handoff)} newest section is missing a NEXT ACTION line",
            })
        if "WAITING FOR OWNER" not in section:
            findings.append({
                "severity": "ERROR",
                "message": f"{_rel(gov_handoff)} newest section is missing a WAITING FOR OWNER line",
            })

    ok = not any(f["severity"] == "ERROR" for f in findings)
    return Envelope(
        ok=ok,
        command="audit repo",
        data=data,
        findings=findings,
    )
