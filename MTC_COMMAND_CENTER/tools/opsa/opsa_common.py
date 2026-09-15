"""Shared helpers for the OPS-A survivability tooling (WP-P0-26, local half).

Design invariants for every tool in this package (audit against these):

1. **No delete code path at all.** No ``os.remove``, ``os.unlink``, ``Path.unlink``,
   ``os.rmdir``, ``Path.rmdir``, ``shutil.rmtree``, ``shutil.move``, ``os.truncate``
   or any other destructive call exists anywhere under ``tools/opsa``. The tools may
   create and overwrite files only. Protected evidence classes can therefore never be
   deleted by this tooling — not by design intent, but by construction.
   (``os.replace`` overwrites a destination atomically; it is a write, not a delete.
   A failed atomic write may leave a ``*.tmp`` file behind; we deliberately do NOT
   clean that up, because a cleanup path would be a delete path.)
2. **UTC only** (repo time discipline, plan #45): every persisted timestamp is an
   ISO-8601 UTC string ending in ``Z``. Local time is never written.
3. **Inability to evaluate is its own outcome** (DESIGN_DEFECT_PATTERNS pattern 1):
   tools never report OK when they could not actually check something; they report a
   distinct check-failure outcome instead of silently passing or masking it.
4. **Standard library only** — no third-party dependencies, per the lane contract.

Harvested patterns (see LANE_REPORT.md reuse record):
- ``_atomic_write_json`` / UTC-Z stamps from ``03_QUANTLENS/tools/progress_emitter.py``
- exit-code convention (0 ok / non-zero alert) from
  ``02_MTC_BACKTEST/scripts/health_alerts.py``; the three-way extension to
  0 ok / 2 alert / 3 check-failure is THIS package's own addition, not
  health_alerts.py's (it knows no rc-3 could-not-evaluate class).
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath
from urllib.parse import unquote

MANIFEST_SCHEMA = "mtc.opsa_manifest/v1"
HEARTBEAT_SCHEMA = "mtc.opsa_heartbeat/v1"
WATCHDOG_EVENT_SCHEMA = "mtc.opsa_watchdog_event/v1"
CONFIG_SCHEMA = "mtc.opsa_backup_config/v1"
#: Per-run completion evidence (WP-P0-26 completion-marker repair, owner packet 2026-09-07 sections 4-5):
#: every SUCCESSFUL backup run leaves an immutable per-run manifest plus a completion marker inside
#: its run directory; a partial or interrupted run leaves neither, and restore refuses such a run.
RUN_MANIFEST_SCHEMA = "mtc.opsa_run_manifest/v1"
RUN_COMPLETE_SCHEMA = "mtc.opsa_run_complete/v1"
RUN_MANIFEST_NAME = "RUN_MANIFEST.jsonl"
COMPLETE_MARKER_NAME = "COMPLETE.json"

#: Exit codes: 0 ok / 2 alert harvested from health_alerts.py's convention;
#: 3 could-not-evaluate is this package's extension (honest-wording fix, audit R1 nit 5).
RC_OK = 0
RC_ALERT = 2
RC_CHECK_FAILED = 3


class RequiredFieldError(ValueError):
    """A required external-input field is absent, non-string, or empty."""

    def __init__(self, field: str, context: str):
        self.field = field
        self.context = context
        super().__init__(f"{context} field {field!r} must be a non-empty string")


def require_non_empty_string(value: object, field: str, context: str) -> str:
    """Return a required string field or raise before it reaches path handling."""
    if not isinstance(value, str) or not value:
        raise RequiredFieldError(field, context)
    return value


def require_non_empty_string_field(record: object, field: str, context: str) -> str:
    """Validate one required field from an external mapping without coercing it."""
    if not isinstance(record, dict):
        raise RequiredFieldError(field, context)
    return require_non_empty_string(record.get(field), field, context)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    return utc_now().isoformat(timespec="seconds").replace("+00:00", "Z")


def run_id_for(dt: datetime) -> str:
    """Sortable, effectively collision-free run id (millisecond precision).

    Same-second runs would otherwise merge into one run directory and one manifest
    run_id — ms precision keeps lexicographic ordering AND uniqueness for any realistic
    cadence (a run always takes longer than 1 ms of hashing).
    """
    return f"opsa-{dt.strftime('%Y%m%dT%H%M%S')}.{dt.microsecond // 1000:03d}Z"


def parse_utc_iso(value: str) -> datetime:
    """Parse an ISO-8601 string (``...Z`` or offset form) into an aware UTC datetime.

    Raises ValueError on anything unparseable — callers must treat that as a
    check-failure, never as freshness.
    """
    ts = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise ValueError(f"naive timestamp (no offset): {value!r}")
    return ts.astimezone(timezone.utc)


def atomic_write_bytes(path: Path, data: bytes) -> None:
    """Write bytes via tmp file + os.replace so readers never see a torn file.

    On failure the tmp file is left on disk (no cleanup — see module docstring;
    a cleanup path would be a delete path, so failure simply propagates).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)
    os.replace(tmp_name, path)


def atomic_write_json(path: Path, payload: dict) -> None:
    atomic_write_bytes(Path(path), json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                              indent=2).encode("utf-8") + b"\n")


def sha256_file(path: Path) -> str:
    """Streaming SHA-256 of a file's raw bytes."""
    digest = hashlib.sha256()
    with open(Path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_jsonl(path: Path, record: dict) -> None:
    """Append one JSON record to an append-only JSONL file (manifest / event log).

    Opened in ``"a"`` mode only: the file is never rewritten, truncated or read back
    by the writer. One ``write`` of one line + newline per call, then flush + fsync so
    an interrupted run leaves every completed record durable.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())


def write_once_bytes(path: Path, data: bytes) -> None:
    """Create ``path`` exclusively and write ``data`` in one call, then flush + fsync.

    ``O_EXCL`` semantics: an existing file is never rewritten or truncated (immutability of
    the per-run manifest and completion marker). ``FileExistsError`` propagates to the caller.
    No tmp file, no rename, no delete path.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def write_once_json(path: Path, payload: dict) -> None:
    write_once_bytes(Path(path), json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                            indent=2).encode("utf-8") + b"\n")


class RunNotComplete(ValueError):
    """The run directory carries no valid completion evidence (marker or per-run manifest)."""


def run_manifest_path(run_dir: Path) -> Path:
    return Path(run_dir) / RUN_MANIFEST_NAME


def complete_marker_path(run_dir: Path) -> Path:
    return Path(run_dir) / COMPLETE_MARKER_NAME


def load_complete_marker(run_dir: Path, run_id: str) -> dict:
    """Return the completion marker of ``run_dir`` after verifying it belongs to ``run_id`` and
    that the per-run manifest it names still hashes to the recorded digest.

    Refuses (``RunNotComplete``) when the marker or the per-run manifest is absent, unreadable,
    not a JSON object, of another schema/run, or when the manifest bytes no longer match the
    marker's ``run_manifest_sha256``. Never repairs, never writes.
    """
    run_dir = Path(run_dir)
    marker = complete_marker_path(run_dir)
    manifest = run_manifest_path(run_dir)
    if not marker.is_file():
        raise RunNotComplete(f"run {run_id}: no completion marker ({COMPLETE_MARKER_NAME} absent)")
    if not manifest.is_file():
        raise RunNotComplete(f"run {run_id}: no per-run manifest ({RUN_MANIFEST_NAME} absent)")
    try:
        payload = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RunNotComplete(f"run {run_id}: completion marker unreadable: {exc}") from exc
    if not isinstance(payload, dict):
        raise RunNotComplete(f"run {run_id}: completion marker is not a JSON object")
    if payload.get("schema") != RUN_COMPLETE_SCHEMA:
        raise RunNotComplete(f"run {run_id}: completion marker schema mismatch: {payload.get('schema')!r}")
    if payload.get("run_id") != run_id:
        raise RunNotComplete(f"run {run_id}: completion marker names run {payload.get('run_id')!r}")
    recorded = payload.get("run_manifest_sha256")
    actual = sha256_file(manifest)
    if not isinstance(recorded, str) or recorded != actual:
        raise RunNotComplete(f"run {run_id}: per-run manifest hash mismatch "
                             f"(marker={str(recorded)[:16]}… actual={actual[:16]}…)")
    return payload


def read_jsonl(path: Path) -> list[dict]:
    """Read a JSONL file into a list of records (for restore / audit reads).

    A malformed line is returned as ``{"record": "_malformed", "line_number": ...}``
    so the caller can report it as a check-failure instead of silently skipping it.
    """
    records: list[dict] = []
    with open(Path(path), "r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                records.append({"record": "_malformed", "line_number": lineno})
    return records


def to_posix_rel(path: Path, base: Path) -> str:
    """Relative path with forward slashes (portable manifest form)."""
    return Path(path).resolve().relative_to(Path(base).resolve()).as_posix()


def resolve_confined_path(root: Path, *parts: str | Path) -> Path:
    """Resolve a destination that must remain strictly below ``root``.

    User- or manifest-controlled path parts are rejected when they are absolute,
    carry a Windows drive/UNC prefix, contain a parent component, or encode such a
    component with URL-style escapes.  Both the literal and repeatedly-decoded forms
    are checked so an id such as ``..%2Foutside`` cannot bypass the same rule that
    rejects ``../outside``.  The returned path is canonical and strictly inside the
    canonical root; equality with the root itself is not sufficient.
    """
    root_resolved = Path(root).expanduser().resolve()
    literal_candidate = root_resolved
    decoded_candidate = root_resolved

    if not parts:
        raise ValueError("confined path requires at least one child component")

    for part in parts:
        if isinstance(part, Path):
            raw = str(part)
        elif isinstance(part, str):
            raw = part
        else:
            raise ValueError(
                f"path component must be a non-empty string or Path, got {type(part).__name__}")
        if not raw or "\x00" in raw:
            raise ValueError(f"unsafe empty/NUL path component: {raw!r}")

        decoded = raw
        for _ in range(5):
            next_value = unquote(decoded)
            if next_value == decoded:
                break
            decoded = next_value

        for value in (raw, decoded):
            windows = PureWindowsPath(value)
            normalized_parts = value.replace("\\", "/").split("/")
            if (Path(value).is_absolute() or windows.drive or windows.root
                    or ".." in normalized_parts):
                raise ValueError(f"path escapes configured root: {raw!r}")

        literal_candidate = literal_candidate / raw
        decoded_candidate = decoded_candidate / decoded

    for candidate in (literal_candidate, decoded_candidate):
        resolved = candidate.resolve()
        try:
            resolved.relative_to(root_resolved)
        except ValueError as exc:
            raise ValueError(f"path escapes configured root: {candidate}") from exc
        if resolved == root_resolved:
            raise ValueError(f"path must be strictly inside configured root: {candidate}")

    return literal_candidate.resolve()


def load_backup_config(config_path: Path) -> dict:
    """Load and validate a backup config; raises with a clear message on schema drift."""
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config.get("schema") != CONFIG_SCHEMA:
        raise ValueError(f"config schema must be {CONFIG_SCHEMA}, got {config.get('schema')!r}")
    require_non_empty_string_field(config, "backup_root", "backup config")
    stores = config.get("stores")
    if not isinstance(stores, list) or not stores:
        raise ValueError("config must set a non-empty stores list")
    seen_ids: set[str] = set()
    for index, store in enumerate(stores):
        for field in ("id", "path", "class"):
            require_non_empty_string_field(store, field, f"backup config store[{index}]")
        if store["id"] in seen_ids:
            raise ValueError(f"duplicate store id: {store['id']!r}")
        resolve_confined_path(Path(config["backup_root"]), "runs", "_config_check",
                              store["id"])
        seen_ids.add(store["id"])
    return config
