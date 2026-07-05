#!/usr/bin/env python3
"""Derive 03_STATUS/CURRENT_STATUS.json from the live memory files.

Barış decision 2026-07-05 (audit MCC_APP_AUDIT_2026-07-05.md): CURRENT_STATUS.json
was a hand-curated artifact that silently went stale (frozen 2026-05-30 while the
dashboard Home read it as current). This tool regenerates it from the two files that
ARE kept current every session:

  * GLOBAL_HANDOFF.md  — newest section (first "## " header) -> phase + summary
  * NEXT_STEPS.md      — first actionable bullet             -> next_recommended_action

Static/safety fields (product, mode=read_only, live_trading_enabled=false, root) are
preserved from the existing file or defaulted safely. It never enables live trading and
never invents evidence — it only relays what the memory files already say.

Usage:
  python derive_current_status.py            # dry-run: print derived JSON, write nothing
  python derive_current_status.py --apply     # write 03_STATUS/CURRENT_STATUS.json
  python derive_current_status.py --check      # exit 1 if on-disk file differs from derived
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

MCC_ROOT = Path(__file__).resolve().parents[2]
MEMORY = MCC_ROOT / "_AI_MEMORY"
STATUS_FILE = MCC_ROOT / "03_STATUS" / "CURRENT_STATUS.json"

DEFAULTS = {
    "schema_version": "1.0",
    "product": "MTC Command Center",
    "short_name": "MCC",
    "root": str(MCC_ROOT).replace("\\", "/"),
    "mode": "read_only",
    "dry_run": True,
    "live_trading_enabled": False,
    "active_writer": None,
}
BASE_WARNINGS = ["No live trading allowed", "MTC_v2 core files remain protected"]


def _newest_handoff_section(text: str) -> tuple[str, str]:
    """Return (topic, first_paragraph) of the newest '## ' section."""
    lines = text.splitlines()
    header = None
    body: list[str] = []
    for line in lines:
        if line.startswith("## "):
            header = line[3:].strip()
            continue
        if header is not None:
            if line.startswith("## "):
                break
            body.append(line)
            # stop at first blank line AFTER we captured some prose
            if body and body[-1].strip() == "" and any(b.strip() for b in body[:-1]):
                break
    if header is None:
        return ("Unknown", "")
    # topic = text after the last em-dash in the header (e.g. "... — Topic")
    topic = header.split("—")[-1].strip() if "—" in header else header
    paragraph = " ".join(b.strip() for b in body if b.strip())
    paragraph = re.sub(r"\s+", " ", paragraph).strip()
    return (topic, paragraph)


def _first_action(text: str) -> str | None:
    """First not-yet-done actionable bullet in NEXT_STEPS (skips ~~struck~~ / DONE)."""
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("-"):
            continue
        body = s.lstrip("-").strip()
        if body.startswith("~~") or "DONE" in body[:40].upper():
            continue
        if "[AI:" in body or body:
            cleaned = re.sub(r"\*+", "", body)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            if cleaned:
                return cleaned[:500]
    return None


def derive() -> dict:
    existing = {}
    if STATUS_FILE.exists():
        try:
            existing = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    handoff = (MEMORY / "GLOBAL_HANDOFF.md").read_text(encoding="utf-8")
    next_steps = (MEMORY / "NEXT_STEPS.md").read_text(encoding="utf-8")

    topic, summary = _newest_handoff_section(handoff)
    action = _first_action(next_steps)

    status = dict(DEFAULTS)
    # preserve a hand-set root/product if present and sane
    for k in ("product", "short_name", "root"):
        if existing.get(k):
            status[k] = existing[k]
    status["phase"] = topic or existing.get("phase") or "Unknown"
    status["last_updated"] = date.today().isoformat() + "T00:00:00+03:00"
    status["summary"] = (
        summary or existing.get("summary") or "Derived from GLOBAL_HANDOFF.md."
    )[:1200]
    status["critical_warnings"] = BASE_WARNINGS
    status["next_recommended_action"] = action
    return status


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="write CURRENT_STATUS.json")
    ap.add_argument("--check", action="store_true", help="exit 1 if on-disk differs")
    args = ap.parse_args()

    derived = derive()
    rendered = json.dumps(derived, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        current = STATUS_FILE.read_text(encoding="utf-8") if STATUS_FILE.exists() else ""
        # compare everything except last_updated (timestamp always changes)
        def _norm(s: str) -> dict:
            try:
                d = json.loads(s)
            except Exception:
                return {"__invalid__": True}
            d.pop("last_updated", None)
            return d
        if _norm(current) == _norm(rendered):
            print("CURRENT_STATUS.json is in sync with memory files.")
            return 0
        print("DRIFT: CURRENT_STATUS.json differs from derived. Run with --apply.")
        return 1

    if args.apply:
        STATUS_FILE.write_text(rendered, encoding="utf-8")
        print(f"wrote {STATUS_FILE}")
        return 0

    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
