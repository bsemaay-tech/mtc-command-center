"""
mtc audit repo — read-only repo health snapshot.

Checks:
  - Required AI memory files present (router-era layout: current-state files
    only; see D002 / MAP97 and root AGENTS.md "Work and acceptance invariants")
  - Git index clean (no staged changes)
  - Overnight loop heartbeat age
  - Governance HANDOFF.md newest section carries NEXT ACTION / WAITING FOR OWNER

The governance HANDOFF.md (MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md) is
written newest-first: each lane/session appends its "## " section above the
older ones, so the current state is always the section nearest the top. This
check reads only that first "## " section (see `_newest_section`) — an older
section further down is out of scope for the NEXT ACTION / WAITING FOR OWNER
presence checks below.
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

# A WAITING FOR OWNER value that means "no ask" — matched after stripping the
# leading "WAITING FOR OWNER" label, ":"/"*" markers, and a trailing ".".
#
# "nothing" keeps its pre-existing, prefix-tolerant behavior: it may be
# followed by trailing prose, e.g. "Nothing for this lane" (this is the
# established convention this change must not break). The newly added
# tokens (none/n/a/-/—/empty) are matched as the *entire* value instead —
# each is a placeholder in its own right, not a prefix, so "none of the
# below needs a decision" is still a real, countable ask.
_WAITING_NOTHING_PREFIX_RE = re.compile(r"^\s*nothing\b", re.IGNORECASE)
_WAITING_NOTHING_WHOLE_VALUE_TOKENS = {"nothing", "none", "n/a", "na", "-", "—"}

# Kept for backward compatibility / external callers that reference the old
# name directly; prefer `_is_no_owner_ask` for new checks.
_WAITING_NOTHING_RE = _WAITING_NOTHING_PREFIX_RE


def _is_no_owner_ask(value: str) -> bool:
    """True when a WAITING FOR OWNER value carries no real ask.

    Covers an empty value, a bare "-"/"—" placeholder, an optionally
    parenthesized "none"/"n/a" token (case-insensitive, matched as the whole
    value), and "nothing" (case-insensitive), which — as before this change
    — may also be followed by trailing prose (e.g. "Nothing for this
    lane"). Anything else, including a token embedded as a prefix of a
    longer real ask (e.g. "none of the below needs a decision"), is a real,
    countable item.
    """
    stripped = value.strip()
    if not stripped:
        return True
    if _WAITING_NOTHING_PREFIX_RE.match(stripped):
        return True
    unwrapped = stripped
    if unwrapped.startswith("(") and unwrapped.endswith(")") and len(unwrapped) > 1:
        unwrapped = unwrapped[1:-1].strip()
        if not unwrapped:
            return True
    normalized = unwrapped.rstrip(".").strip().lower()
    return normalized in _WAITING_NOTHING_WHOLE_VALUE_TOKENS


def _newest_section(handoff_text: str) -> str:
    parts = _SECTION_SPLIT_RE.split(handoff_text)
    # parts[0] is preamble before the first "## " heading (e.g. the H1 title).
    return parts[1] if len(parts) > 1 else handoff_text


# A NEXT ACTION *label* line: NEXT ACTION either bolded ("**NEXT ACTION**")
# or colon-terminated ("NEXT ACTION:", with or without surrounding "**"). A
# bare mention of the phrase inside prose that carries neither form does not
# count, even though the substring "NEXT ACTION" is present on that line; a
# labelled occurrence embedded inside a longer prose line (e.g. "... the
# NEXT ACTION: ship it.") still counts — the label form is what
# disambiguates a committed action item from incidental prose.
_NEXT_ACTION_LABEL_RE = re.compile(
    r"^.*(?:\*\*NEXT ACTION\*\*|NEXT ACTION\s*:).*$",
    re.MULTILINE,
)


def _handoff_next_action_count(section: str) -> int:
    """Count lines carrying a NEXT ACTION label (line-anchored, not a bare
    substring count — see `_NEXT_ACTION_LABEL_RE`)."""
    return len(_NEXT_ACTION_LABEL_RE.findall(section))


def _handoff_waiting_for_owner_count(section: str) -> int:
    """Count WAITING FOR OWNER lines whose value is not a "no ask" token."""
    real = 0
    for line in section.splitlines():
        if "WAITING FOR OWNER" not in line:
            continue
        value = line.split("WAITING FOR OWNER", 1)[1]
        value = value.lstrip(":*").strip().rstrip(".").strip()
        if not _is_no_owner_ask(value):
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
