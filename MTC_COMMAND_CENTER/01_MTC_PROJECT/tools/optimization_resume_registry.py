from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REGISTRY_VERSION = "optimization_resume_registry_v1"

STATUS_PLANNED = "PLANNED"
STATUS_RUNNING = "RUNNING"
STATUS_COMPLETED = "COMPLETED"
STATUS_FAILED = "FAILED"
STATUS_SKIPPED_ALREADY_COMPLETED = "SKIPPED_ALREADY_COMPLETED"
STATUS_INVALIDATED_DATASET_HASH = "INVALIDATED_DATASET_HASH"
STATUS_INVALIDATED_CODE_VERSION = "INVALIDATED_CODE_VERSION"


@dataclass(frozen=True)
class EvaluationIdentity:
    profile_id: str
    dataset_id: str
    dataset_hash: str
    symbol: str
    timeframe: str
    window_id: str
    split_type: str
    params: dict[str, Any]
    runner_version: str
    optimizer_version: str
    parameter_mapper_version: str


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def evaluation_key(identity: EvaluationIdentity | dict[str, Any]) -> str:
    payload = asdict(identity) if isinstance(identity, EvaluationIdentity) else dict(identity)
    payload["params"] = json.loads(canonical_json(payload.get("params", {})))
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def metrics_hash(metrics: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(metrics).encode("utf-8")).hexdigest()


def row_result_hash(row: dict[str, Any]) -> str:
    ignored = {"worker_id", "traceback", "error_path"}
    return metrics_hash({key: value for key, value in row.items() if key not in ignored})


class ResumeRegistry:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS evaluations (
                    evaluation_key TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    result_path TEXT,
                    metrics_hash TEXT,
                    error TEXT,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conflicts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    evaluation_key TEXT NOT NULL,
                    first_hash TEXT NOT NULL,
                    conflicting_hash TEXT NOT NULL,
                    detail_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def _upsert(self, key: str, status: str, *, result_path: str | None = None, hash_value: str | None = None, error: str | None = None) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO evaluations(evaluation_key, status, result_path, metrics_hash, error, updated_at)
                VALUES(?, ?, ?, ?, ?, ?)
                ON CONFLICT(evaluation_key) DO UPDATE SET
                    status=excluded.status,
                    result_path=COALESCE(excluded.result_path, evaluations.result_path),
                    metrics_hash=COALESCE(excluded.metrics_hash, evaluations.metrics_hash),
                    error=excluded.error,
                    updated_at=excluded.updated_at
                """,
                (key, status, result_path, hash_value, error, now),
            )

    def register_planned(self, key: str) -> None:
        if not self._status(key):
            self._upsert(key, STATUS_PLANNED)

    def mark_running(self, key: str) -> None:
        self._upsert(key, STATUS_RUNNING)

    def mark_completed(self, key: str, result_path: str, metrics_hash: str) -> None:
        self._upsert(key, STATUS_COMPLETED, result_path=result_path, hash_value=metrics_hash)

    def mark_failed(self, key: str, error: str) -> None:
        self._upsert(key, STATUS_FAILED, error=error)

    def mark_skipped_already_completed(self, key: str) -> None:
        if self.is_completed(key):
            return
        self._upsert(key, STATUS_SKIPPED_ALREADY_COMPLETED)

    def _status(self, key: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute("SELECT status FROM evaluations WHERE evaluation_key = ?", (key,)).fetchone()
        return str(row[0]) if row else None

    def is_completed(self, key: str) -> bool:
        return self._status(key) == STATUS_COMPLETED

    def should_retry_failed(self, key: str, *, retry_failed: bool) -> bool:
        return retry_failed and self._status(key) == STATUS_FAILED

    def load_completed_keys(self) -> set[str]:
        with self._connect() as conn:
            return {str(row[0]) for row in conn.execute("SELECT evaluation_key FROM evaluations WHERE status = ?", (STATUS_COMPLETED,))}

    def dedupe_results(self, input_results: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        unique: dict[str, dict[str, Any]] = {}
        hashes: dict[str, str] = {}
        conflicts: list[dict[str, Any]] = []
        for row in input_results:
            key = str(row.get("evaluation_key") or "")
            if not key:
                key = metrics_hash(row)
                row = {**row, "evaluation_key": key}
            current_hash = row_result_hash(row)
            if key not in unique:
                unique[key] = row
                hashes[key] = current_hash
                continue
            if hashes[key] != current_hash:
                conflict = {
                    "evaluation_key": key,
                    "first_hash": hashes[key],
                    "conflicting_hash": current_hash,
                }
                conflicts.append(conflict)
                self._record_conflict(conflict)
        return list(unique.values()), conflicts

    def _record_conflict(self, conflict: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO conflicts(evaluation_key, first_hash, conflicting_hash, detail_json, created_at)
                VALUES(?, ?, ?, ?, ?)
                """,
                (
                    conflict["evaluation_key"],
                    conflict["first_hash"],
                    conflict["conflicting_hash"],
                    canonical_json(conflict),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

    def write_registry_report(self, path: Path) -> None:
        with self._connect() as conn:
            statuses = list(conn.execute("SELECT status, COUNT(*) FROM evaluations GROUP BY status ORDER BY status"))
            conflicts = list(conn.execute("SELECT evaluation_key, first_hash, conflicting_hash FROM conflicts ORDER BY id"))
        lines = [
            "# Resume / De-dup Registry Report",
            "",
            f"- Registry path: `{self.path}`",
            f"- Registry version: `{REGISTRY_VERSION}`",
            "",
            "## Status Counts",
            "",
        ]
        for status, count in statuses:
            lines.append(f"- {status}: {count}")
        lines.extend(["", "## Conflicts", ""])
        if conflicts:
            for key, first_hash, conflicting_hash in conflicts:
                lines.append(f"- `{key}`: `{first_hash}` vs `{conflicting_hash}`")
        else:
            lines.append("- None")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
