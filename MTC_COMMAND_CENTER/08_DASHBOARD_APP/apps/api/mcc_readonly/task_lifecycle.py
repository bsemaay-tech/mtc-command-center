from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def build_task_lifecycle(task_queue: dict[str, Any] | None, now: datetime | None = None) -> dict[str, Any]:
    current_time = now or datetime.now(timezone.utc)
    tasks = (task_queue or {}).get("tasks", [])
    by_status: dict[str, int] = {}
    waiting_for_user = []
    stale_candidates = []
    task_flags: dict[str, list[str]] = {}

    for task in tasks:
        status = str(task.get("status") or "UNKNOWN")
        task_id = str(task.get("id") or "")
        by_status[status] = by_status.get(status, 0) + 1

        flags: list[str] = []
        if status == "WAITING_FOR_USER" or task.get("requires_user_input") is True:
            flags.append("WAITING_FOR_USER")
            waiting_for_user.append(_task_ref(task))

        if _is_stale_candidate(task, current_time):
            flags.append("STALE_CANDIDATE")
            stale_candidates.append(_task_ref(task))

        if task_id:
            task_flags[task_id] = flags

    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "summary": {
            "total": len(tasks),
            "by_status": by_status,
            "waiting_for_user": len(waiting_for_user),
            "stale_candidates": len(stale_candidates),
        },
        "waiting_for_user": waiting_for_user,
        "stale_candidates": stale_candidates,
        "task_flags": task_flags,
    }


def _is_stale_candidate(task: dict[str, Any], now: datetime) -> bool:
    if task.get("status") != "IN_PROGRESS":
        return False
    timeout_seconds = task.get("timeout_seconds")
    if not isinstance(timeout_seconds, int) or timeout_seconds <= 0:
        return False
    timestamp = _parse_task_time(task.get("updated_at") or task.get("created_at"))
    if timestamp is None:
        return False
    return (now - timestamp).total_seconds() > timeout_seconds


def _parse_task_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _task_ref(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": task.get("id"),
        "title": task.get("title"),
        "status": task.get("status"),
        "phase": task.get("phase"),
        "updated_at": task.get("updated_at"),
        "timeout_seconds": task.get("timeout_seconds"),
    }

