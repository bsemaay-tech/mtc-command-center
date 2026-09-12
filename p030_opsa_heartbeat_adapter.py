"""P030-owned adapter over the unchanged P026 heartbeat emitter."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path


OPSA_TOOLS = Path(__file__).resolve().parent / "MTC_COMMAND_CENTER" / "tools" / "opsa"
sys.path.insert(0, str(OPSA_TOOLS))

import heartbeat  # noqa: E402
from opsa_common import (  # noqa: E402
    atomic_write_json,
    HEARTBEAT_SCHEMA,
    parse_utc_iso,
    require_non_empty_string,
    resolve_confined_path,
)


_EMITTER_UTC_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _reject_nonfinite_json(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _state_directory(value: Path | str) -> Path:
    if isinstance(value, str) and not value.strip():
        raise ValueError("state_dir must not be empty or whitespace")
    try:
        return Path(value)
    except TypeError as exc:
        raise ValueError("state_dir must be a path") from exc


def emit_process_heartbeat(
    state_dir: Path, heartbeat_id: str, *, seq: int, note: str | None = None
) -> Path:
    """Emit only the exact P026 heartbeat payload."""

    state_dir = _state_directory(state_dir)
    heartbeat_id = require_non_empty_string(
        heartbeat_id, "id", "P026 heartbeat emitter"
    )
    if isinstance(seq, bool) or not isinstance(seq, int):
        raise ValueError("seq must be an integer")
    if note is not None and not isinstance(note, str):
        raise ValueError("note must be a string or null")
    return heartbeat.emit(state_dir, heartbeat_id, seq=seq, note=note)


def verify_process_heartbeat(state_dir: Path, heartbeat_id: str) -> dict:
    """Verify the exact P026 process-alive payload without applying a health policy."""

    state_dir = _state_directory(state_dir)
    heartbeat_id = require_non_empty_string(
        heartbeat_id, "id", "P026 heartbeat verifier"
    )
    path = resolve_confined_path(state_dir, f"{heartbeat_id}.hb.json")
    try:
        payload = json.loads(
            Path(path).read_text(encoding="utf-8"),
            parse_constant=_reject_nonfinite_json,
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("heartbeat is not readable JSON") from exc
    required = {"schema", "id", "seq", "emitted_at", "pid"}
    allowed = required | {"note"}
    if not isinstance(payload, dict) or not required <= set(payload) or not set(payload) <= allowed:
        raise ValueError("heartbeat fields do not match P026")
    if payload["schema"] != HEARTBEAT_SCHEMA or payload["id"] != heartbeat_id:
        raise ValueError("heartbeat identity does not match P026")
    if (
        isinstance(payload["seq"], bool)
        or not isinstance(payload["seq"], int)
        or isinstance(payload["pid"], bool)
        or not isinstance(payload["pid"], int)
    ):
        raise ValueError("heartbeat numeric fields do not match P026")
    if "note" in payload and (
        not isinstance(payload["note"], str) or not payload["note"]
    ):
        raise ValueError("heartbeat note does not match P026")
    emitted_at = payload["emitted_at"]
    if not isinstance(emitted_at, str) or not _EMITTER_UTC_Z.fullmatch(emitted_at):
        raise ValueError("heartbeat emitted_at must use exact emitter UTC-Z grammar")
    try:
        parse_utc_iso(emitted_at)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("heartbeat emitted_at does not match P026") from exc
    return payload


def _utc_z(value: str, field: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{field} must be a caller-supplied UTC Z timestamp")
    try:
        parsed = parse_utc_iso(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be a caller-supplied UTC Z timestamp") from exc
    if parsed.microsecond:
        raise ValueError(f"{field} must use whole seconds")
    return parsed


def write_health_sidecar(
    state_dir: Path,
    heartbeat_id: str,
    *,
    observed_at_utc: str,
    last_accepted_timestamp_utc: str | None,
    reconciliation_progress: None,
) -> Path:
    """Write P030 health signals separately from the P026 heartbeat payload."""

    state_dir = _state_directory(state_dir)
    heartbeat_id = require_non_empty_string(heartbeat_id, "id", "P030 health sidecar")
    observed_at = _utc_z(observed_at_utc, "observed_at_utc")
    if reconciliation_progress is not None:
        raise ValueError("reconciliation_progress must remain null in this slice")
    if last_accepted_timestamp_utc is None:
        market_freshness = {
            "availability": "unavailable",
            "last_accepted_timestamp_utc": None,
            "age_seconds": None,
        }
    else:
        last_accepted = _utc_z(
            last_accepted_timestamp_utc, "last_accepted_timestamp_utc"
        )
        age_seconds = int((observed_at - last_accepted).total_seconds())
        if age_seconds < 0:
            raise ValueError("last accepted timestamp cannot follow observed_at_utc")
        market_freshness = {
            "availability": "available",
            "last_accepted_timestamp_utc": last_accepted_timestamp_utc,
            "age_seconds": age_seconds,
        }
    path = resolve_confined_path(state_dir, f"{heartbeat_id}.health.json")
    atomic_write_json(
        path,
        {
            "schema": "p030.health_sidecar/v1",
            "id": heartbeat_id,
            "observed_at_utc": observed_at_utc,
            "market_freshness": market_freshness,
            "reconciliation_progress": reconciliation_progress,
        },
    )
    return path
