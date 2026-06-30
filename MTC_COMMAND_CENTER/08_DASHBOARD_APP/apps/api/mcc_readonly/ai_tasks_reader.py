"""Read-only reader for the AI Task prompt library (`05_REGISTRY/AI_TASKS.json`).

Surfaces copy-ready prompt templates for the dashboard's AI Tasks tab. Never writes,
never executes; tolerates an absent/invalid file with a structured empty state.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root

REGISTRY_REL_PATH = Path("05_REGISTRY") / "AI_TASKS.json"


def _empty(reason: str) -> dict[str, Any]:
    return {"available": False, "reason": reason, "intro": "", "tasks": [], "count": 0}


def build_ai_tasks(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    path = root / REGISTRY_REL_PATH
    if not path.exists():
        return _empty("registry_not_found")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # malformed JSON must not break the snapshot
        return _empty(f"json_error: {exc}")

    tasks_in = raw.get("tasks") if isinstance(raw, dict) else None
    tasks: list[dict[str, Any]] = []
    if isinstance(tasks_in, list):
        for t in tasks_in:
            if not isinstance(t, dict):
                continue
            tid = str(t.get("id") or "").strip()
            prompt = str(t.get("prompt") or "").strip()
            if not tid or not prompt:
                continue
            tasks.append(
                {
                    "id": tid,
                    "title": str(t.get("title") or tid),
                    "summary": str(t.get("summary") or ""),
                    "read": [str(x) for x in t.get("read", []) if isinstance(t.get("read"), list)],
                    "knobs": [str(x) for x in t.get("knobs", []) if isinstance(t.get("knobs"), list)],
                    "prompt": prompt,
                }
            )

    return {
        "available": True,
        "source": REGISTRY_REL_PATH.as_posix(),
        "updated": (raw.get("updated") if isinstance(raw, dict) else None),
        "intro": (str(raw.get("intro")) if isinstance(raw, dict) and raw.get("intro") else ""),
        "tasks": tasks,
        "count": len(tasks),
    }
