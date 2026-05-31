from __future__ import annotations

import json
import os
import shutil
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

from .paths import canonicalize, default_mcc_root
from .schema import validate_json_schema


TASK_RESOURCE = "02_TASKS/TASK_QUEUE.json"
TASK_LOCK = "02_TASKS/.locks/task_queue.lock"
TASK_HISTORY = "02_TASKS/TASK_HISTORY.json"
STATUS_EVENTS = "03_STATUS/status_events.jsonl"
VALID_TASK_STATES = {
    "TODO",
    "READY",
    "IN_PROGRESS",
    "WAITING_FOR_USER",
    "WAITING_FOR_AI_REVIEW",
    "STALE",
    "FAILED",
    "DONE",
    "ARCHIVED",
}


class WriterError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def process_inbox(
    mcc_root: str | Path | None = None,
    owner_ai: str = "codex-local",
    task_id: str = "MCC-BOOT-010",
) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    inbox = root / "02_TASKS" / "inbox"
    outbox = root / "02_TASKS" / "outbox"
    outbox.mkdir(parents=True, exist_ok=True)

    proposal_paths = sorted(path for path in inbox.glob("*.json") if path.is_file())
    results = []
    for proposal_path in proposal_paths:
        results.append(process_proposal(root, proposal_path, owner_ai=owner_ai, writer_task_id=task_id))

    return {
        "schema_version": "1.0",
        "mode": "controlled_write",
        "processed": len(results),
        "accepted": sum(1 for item in results if item["status"] == "accepted"),
        "rejected": sum(1 for item in results if item["status"] == "rejected"),
        "skipped": sum(1 for item in results if item["status"] == "skipped"),
        "results": results,
    }


def process_proposal(
    mcc_root: str | Path,
    proposal_path: Path,
    owner_ai: str = "codex-local",
    writer_task_id: str = "MCC-BOOT-010",
) -> dict[str, Any]:
    root = canonicalize(mcc_root)
    outbox = root / "02_TASKS" / "outbox"
    outbox.mkdir(parents=True, exist_ok=True)

    parsed, parse_errors = _read_proposal(proposal_path)
    proposal_id = str((parsed or {}).get("proposal_id") or proposal_path.stem)
    action = str((parsed or {}).get("action") or "unknown")

    if _receipt_exists(outbox, proposal_id):
        return {
            "proposal_id": proposal_id,
            "status": "skipped",
            "action": action,
            "receipt_path": None,
            "errors": ["receipt already exists"],
        }

    errors = parse_errors or _validate_task_proposal(parsed)

    try:
        with _task_lock(root, owner_ai=owner_ai, task_id=writer_task_id):
            if errors:
                receipt = _build_receipt(proposal_id, action, "rejected", proposal_path, errors=errors)
                _write_receipt(outbox, receipt)
                _append_status_event(
                    root,
                    event_type="TASK_PROPOSAL_REJECTED",
                    task_id=writer_task_id,
                    action="reject_task_proposal",
                    result="rejected",
                    error_code="ERR-TASK-PROPOSAL",
                )
                return _result_from_receipt(receipt)

            task = dict(parsed["task"])
            queue = _load_json(root / TASK_RESOURCE)
            if any(existing.get("id") == task["id"] for existing in queue.get("tasks", [])):
                receipt = _build_receipt(
                    proposal_id,
                    action,
                    "rejected",
                    proposal_path,
                    applied_task_id=task["id"],
                    errors=[f"task already exists: {task['id']}"],
                )
                _write_receipt(outbox, receipt)
                _append_status_event(
                    root,
                    event_type="TASK_PROPOSAL_REJECTED",
                    task_id=task["id"],
                    action="reject_task_proposal",
                    result="rejected",
                    error_code="ERR-TASK-DUPLICATE",
                )
                return _result_from_receipt(receipt)

            queue.setdefault("tasks", []).append(task)
            queue["generated_at"] = _now_iso()
            _write_validated_json(root, root / TASK_RESOURCE, queue, root / "06_SCHEMAS" / "task_queue.schema.json")

            history = _load_json(root / TASK_HISTORY)
            history.setdefault("events", []).append(
                {
                    "event_id": _history_event_id(),
                    "task_id": task["id"],
                    "event_type": "CREATED",
                    "created_at": _now_iso(),
                    "created_by": owner_ai,
                    "summary": f"Task created from proposal {proposal_id}.",
                    "report_path": None,
                }
            )
            _write_validated_json(root, root / TASK_HISTORY, history, root / "06_SCHEMAS" / "task_history.schema.json")

            receipt = _build_receipt(
                proposal_id,
                action,
                "accepted",
                proposal_path,
                applied_task_id=task["id"],
                errors=[],
            )
            _write_receipt(outbox, receipt)
            _append_status_event(
                root,
                event_type="TASK_PROPOSAL_ACCEPTED",
                task_id=task["id"],
                action="accept_task_proposal",
                result="accepted",
                error_code=None,
            )
            return _result_from_receipt(receipt)
    except WriterError as exc:
        receipt = _build_receipt(proposal_id, action, "rejected", proposal_path, errors=[f"{exc.code}: {exc.message}"])
        _write_receipt(outbox, receipt)
        return _result_from_receipt(receipt)


def _read_proposal(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except UnicodeDecodeError as exc:
        return None, [f"utf-8 decode error: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"json parse error: {exc}"]
    except OSError as exc:
        return None, [f"read error: {exc}"]


def _validate_task_proposal(proposal: dict[str, Any] | None) -> list[str]:
    if not isinstance(proposal, dict):
        return ["proposal must be an object"]
    errors = []
    for key in ("schema_version", "proposal_id", "action", "task"):
        if key not in proposal:
            errors.append(f"missing required field: {key}")
    if proposal.get("action") != "create_task":
        errors.append("only create_task proposals are supported")
    task = proposal.get("task")
    if not isinstance(task, dict):
        errors.append("task must be an object")
        return errors
    for key in ("id", "title", "status", "assigned_ai", "phase", "requires_user_input"):
        if key not in task:
            errors.append(f"task missing required field: {key}")
    if task.get("status") not in VALID_TASK_STATES:
        errors.append(f"invalid task status: {task.get('status')}")
    if not isinstance(task.get("requires_user_input"), bool):
        errors.append("task requires_user_input must be boolean")
    return errors


@contextmanager
def _task_lock(root: Path, owner_ai: str, task_id: str) -> Iterator[None]:
    lock_path = root / TASK_LOCK
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    _recover_stale_or_corrupt_lock(lock_path)
    lock = {
        "resource": TASK_RESOURCE,
        "owner_ai": owner_ai,
        "task_id": task_id,
        "acquired_at": _now_iso(),
        "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat(),
    }
    try:
        with lock_path.open("x", encoding="utf-8") as handle:
            json.dump(lock, handle, ensure_ascii=False, separators=(",", ":"))
    except FileExistsError as exc:
        raise WriterError("ERR-TASK-LOCKED", str(exc)) from exc
    try:
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def _recover_stale_or_corrupt_lock(lock_path: Path) -> None:
    if not lock_path.exists():
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        expires_at = datetime.fromisoformat(str(lock["expires_at"]))
    except Exception:
        lock_path.rename(lock_path.with_name(f"{lock_path.name}.corrupt.{stamp}"))
        return
    if expires_at <= datetime.now(timezone.utc):
        lock_path.rename(lock_path.with_name(f"{lock_path.name}.stale.{stamp}"))


def _write_validated_json(root: Path, target: Path, payload: dict[str, Any], schema_path: Path) -> None:
    schema = _load_json(schema_path)
    issues = validate_json_schema(payload, schema)
    if issues:
        raise WriterError("ERR-JSON-SCHEMA", "; ".join(f"{issue.path}: {issue.message}" for issue in issues))

    backup_dir = _backup_dir_for(root, target)
    backup_dir.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.copy2(target, backup_dir / f"{target.name}.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.bak")
        _trim_backups(backup_dir, target.name)

    temp_path = target.with_name(f"{target.name}.tmp.{os.getpid()}")
    raw = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    with temp_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())

    temp_payload = _load_json(temp_path)
    issues = validate_json_schema(temp_payload, schema)
    if issues:
        temp_path.unlink(missing_ok=True)
        raise WriterError("ERR-JSON-SCHEMA", "; ".join(f"{issue.path}: {issue.message}" for issue in issues))
    os.replace(temp_path, target)


def _backup_dir_for(root: Path, target: Path) -> Path:
    rel_parent = target.parent.relative_to(root)
    return root / "03_STATUS" / ".backups" / str(rel_parent).replace("\\", "_").replace("/", "_")


def _trim_backups(backup_dir: Path, file_name: str, keep: int = 15) -> None:
    backups = sorted(backup_dir.glob(f"{file_name}.*.bak"), key=lambda item: item.stat().st_mtime, reverse=True)
    for old in backups[keep:]:
        old.unlink(missing_ok=True)


def _append_status_event(
    root: Path,
    event_type: str,
    task_id: str,
    action: str,
    result: str,
    error_code: str | None,
) -> None:
    event = {
        "schema_version": "1.0",
        "event_id": _status_event_id(),
        "event_type": event_type,
        "created_at": _now_iso(),
        "task_id": task_id,
        "agent_id": "mcc-writer",
        "model": None,
        "session_id": None,
        "target_file": TASK_RESOURCE,
        "action": action,
        "hash_before_sha256": None,
        "hash_after_sha256": None,
        "result": result,
        "error_code": error_code,
        "report_path": None,
    }
    schema = _load_json(root / "06_SCHEMAS" / "status_event.schema.json")
    issues = validate_json_schema(event, schema)
    if issues:
        raise WriterError("ERR-JSON-SCHEMA", "; ".join(f"{issue.path}: {issue.message}" for issue in issues))
    status_path = root / STATUS_EVENTS
    with status_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")


def _build_receipt(
    proposal_id: str,
    action: str,
    status: str,
    proposal_path: Path,
    applied_task_id: str | None = None,
    errors: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "proposal_id": proposal_id,
        "status": status,
        "action": action,
        "created_at": _now_iso(),
        "source_path": str(proposal_path),
        "applied_task_id": applied_task_id,
        "errors": errors or [],
    }


def _write_receipt(outbox: Path, receipt: dict[str, Any]) -> Path:
    schema_path = outbox.parents[1] / "06_SCHEMAS" / "task_proposal_receipt.schema.json"
    if schema_path.exists():
        issues = validate_json_schema(receipt, _load_json(schema_path))
        if issues:
            raise WriterError("ERR-JSON-SCHEMA", "; ".join(f"{issue.path}: {issue.message}" for issue in issues))
    target = outbox / f"{receipt['proposal_id']}.{receipt['status']}.json"
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def _receipt_exists(outbox: Path, proposal_id: str) -> bool:
    return any(outbox.glob(f"{proposal_id}.*.json"))


def _result_from_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": receipt["proposal_id"],
        "status": receipt["status"],
        "action": receipt["action"],
        "applied_task_id": receipt["applied_task_id"],
        "errors": receipt["errors"],
    }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _history_event_id() -> str:
    return "HIST-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _status_event_id() -> str:
    return "EVT-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")

