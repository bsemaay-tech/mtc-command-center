"""Local-only, append-only research disclosure tracker for WP-P0-22.

This is deliberately a reduced local slice.  It records declared experiment
identity and disclosure events; it does not establish independent access
history, clean windows, or promotion eligibility.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import unicodedata
from typing import Any, Callable


ROLES = frozenset({"strategy", "configuration", "dataset", "report"})
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
DOS_DEVICE_NAMES = frozenset({"CON", "PRN", "AUX", "NUL", "CLOCK$", "CONIN$", "CONOUT$"})
DOS_PORT_RE = re.compile(r"^(?:COM|LPT)[1-9¹²³]$")


class TrackerError(ValueError):
    """A user-facing validation or tracker operation error."""


def _text(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or not value.strip()
        or any(
            ord(character) < 32
            or ord(character) == 127
            or unicodedata.category(character).startswith("C")
            for character in value
        )
    ):
        raise TrackerError(f"{name} must be a non-empty string")
    return value


def _utc(value: Any, name: str) -> str:
    value = _text(value, name)
    if not UTC_RE.fullmatch(value):
        raise TrackerError(f"{name} must be a normalized UTC timestamp ending in Z")
    try:
        parsed = _dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise TrackerError(f"{name} is not a valid UTC timestamp") from exc
    if parsed.tzinfo is not None:
        raise TrackerError(f"{name} must be UTC")
    return value


def _sha(value: Any, name: str) -> str:
    value = _text(value, name)
    if not SHA256_RE.fullmatch(value):
        raise TrackerError(f"{name} must be lowercase hexadecimal SHA-256")
    return value


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _now_utc() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _safe_path(
    value: str | os.PathLike[str], name: str, *, require_absolute: bool
) -> Path:
    try:
        raw = os.fspath(value)
    except TypeError as exc:
        raise TrackerError(f"{name} must be a path string") from exc
    raw = _text(raw, name)
    normalized = raw.replace("/", "\\").lower()
    if raw.startswith(("\\\\", "//")) or normalized.startswith(
        (
            "\\\\",
            "\\\\?",
            "\\\\.",
            "\\??",
            "\\device",
            "\\dosdevices",
            "\\globalroot",
            "\\global??",
            "\\pipe",
        )
    ):
        raise TrackerError(f"{name} must be a local non-device path")
    for component in normalized.split("\\"):
        for candidate in component.split(":"):
            candidate = candidate.rstrip(" .")
            stem = candidate.split(".", 1)[0].rstrip(" .").upper()
            if stem in DOS_DEVICE_NAMES or DOS_PORT_RE.fullmatch(stem):
                raise TrackerError(f"{name} must not use a reserved DOS device alias")
    path = Path(raw)
    if require_absolute and not path.is_absolute():
        raise TrackerError(f"{name} must be absolute")
    return path


def _db_path(value: str | os.PathLike[str]) -> Path:
    path = _safe_path(value, "db path", require_absolute=False)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def _md(value: Any, name: str = "markdown value") -> str:
    """Render dynamic values as inert, single-line Markdown text."""
    if value is None:
        text = "unknown"
    elif isinstance(value, (dict, list, tuple)):
        text = _canonical(value)
    else:
        text = str(value)
    _text(text, name)
    escaped = text.replace("&", "&amp;").replace("`", "&#96;")
    return f"`{escaped}`"


def _hash_file(path: Path) -> str:
    path = _safe_path(path, "referenced file path", require_absolute=True)
    try:
        with path.open("rb") as handle:
            return hashlib.sha256(handle.read()).hexdigest()
    except (OSError, ValueError) as exc:
        raise TrackerError(f"referenced file is missing or unreadable: {path}") from exc


def _validate_spec(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise TrackerError("spec must be a JSON object")
    allowed = {
        "record_version",
        "local_experiment_id",
        "period_start_utc",
        "period_end_utc",
        "references",
        "family_reference",
        "parent_experiment_ids",
        "related_experiment_ids",
    }
    unknown = sorted(set(raw) - allowed)
    if unknown:
        raise TrackerError(f"unknown spec field(s): {', '.join(unknown)}")
    if type(raw.get("record_version")) is not int or raw["record_version"] != 1:
        raise TrackerError("record_version must be 1")
    experiment_id = _text(raw.get("local_experiment_id"), "local_experiment_id")
    start = _utc(raw.get("period_start_utc"), "period_start_utc")
    end = _utc(raw.get("period_end_utc"), "period_end_utc")
    if start >= end:
        raise TrackerError("period_start_utc must be earlier than period_end_utc")

    references = raw.get("references")
    if not isinstance(references, list) or not references:
        raise TrackerError("references must be a non-empty array")
    clean_references: list[dict[str, str]] = []
    seen: set[str] = set()
    roles: set[str] = set()
    for index, reference in enumerate(references):
        if not isinstance(reference, dict) or set(reference) != {"reference_id", "role", "path", "sha256"}:
            raise TrackerError(f"references[{index}] must contain exactly reference_id, role, path, sha256")
        reference_id = _text(reference["reference_id"], f"references[{index}].reference_id")
        if reference_id in seen:
            raise TrackerError(f"duplicate reference_id: {reference_id}")
        seen.add(reference_id)
        role = _text(reference["role"], f"references[{index}].role")
        if role not in ROLES:
            raise TrackerError(f"unsupported reference role: {role}")
        path = _safe_path(
            reference["path"], f"references[{index}].path", require_absolute=True
        )
        digest = _sha(reference["sha256"], f"references[{index}].sha256")
        clean_references.append(
            {"reference_id": reference_id, "role": role, "path": str(path), "sha256": digest}
        )
        roles.add(role)
    missing_roles = sorted(ROLES - roles)
    if missing_roles:
        raise TrackerError(f"missing required reference role(s): {', '.join(missing_roles)}")

    clean: dict[str, Any] = {
        "record_version": 1,
        "local_experiment_id": experiment_id,
        "period_start_utc": start,
        "period_end_utc": end,
        "references": clean_references,
    }
    if "family_reference" in raw:
        clean["family_reference"] = _text(raw["family_reference"], "family_reference")
    for field in ("parent_experiment_ids", "related_experiment_ids"):
        if field in raw:
            values = raw[field]
            if not isinstance(values, list):
                raise TrackerError(f"{field} must be an array when supplied")
            clean_values = [_text(value, f"{field}[]") for value in values]
            if len(set(clean_values)) != len(clean_values):
                raise TrackerError(f"{field} must not contain duplicates")
            clean[field] = clean_values
    return clean


SCHEMA = """
CREATE TABLE IF NOT EXISTS experiment_revisions (
    id INTEGER PRIMARY KEY,
    local_experiment_id TEXT NOT NULL,
    revision INTEGER NOT NULL,
    manifest_json TEXT NOT NULL,
    local_manifest_sha256 TEXT NOT NULL,
    period_start_utc TEXT NOT NULL,
    period_end_utc TEXT NOT NULL,
    family_reference TEXT,
    parent_experiment_ids_json TEXT,
    related_experiment_ids_json TEXT,
    created_at_utc TEXT NOT NULL,
    UNIQUE(local_experiment_id, revision),
    UNIQUE(local_experiment_id, manifest_json)
);
CREATE TABLE IF NOT EXISTS "references" (
    id INTEGER PRIMARY KEY,
    revision_id INTEGER NOT NULL REFERENCES experiment_revisions(id),
    reference_id TEXT NOT NULL,
    role TEXT NOT NULL,
    path TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    UNIQUE(revision_id, reference_id)
);
CREATE TABLE IF NOT EXISTS disclosure_attempts (
    id INTEGER PRIMARY KEY,
    revision_id INTEGER NOT NULL REFERENCES experiment_revisions(id),
    experiment_id TEXT NOT NULL,
    revision INTEGER NOT NULL,
    report_id TEXT NOT NULL,
    attempted_at_utc TEXT NOT NULL,
    report_sha256 TEXT NOT NULL,
    report_bytes INTEGER NOT NULL,
    period_start_utc TEXT NOT NULL,
    period_end_utc TEXT NOT NULL
);
"""


def _connect(path: Path, *, read_only: bool = False) -> sqlite3.Connection:
    path = _safe_path(path, "db path", require_absolute=False)
    if read_only:
        if not path.exists():
            raise TrackerError(f"database does not exist: {path}")
        uri = f"{path.resolve().as_uri()}?mode=ro"
        connection = sqlite3.connect(uri, uri=True)
    else:
        connection = sqlite3.connect(str(path))
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _ensure_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA)


def register(db_path: str | os.PathLike[str], spec_path: str | os.PathLike[str]) -> dict[str, Any]:
    """Validate and register a manifest, returning its local revision summary."""
    database = _db_path(db_path)
    spec_file = _safe_path(spec_path, "spec path", require_absolute=False)
    try:
        with spec_file.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except (OSError, ValueError, UnicodeError) as exc:
        raise TrackerError(f"cannot read spec: {spec_file}") from exc
    spec = _validate_spec(raw)
    manifest_json = _canonical(spec)
    manifest_sha = hashlib.sha256(manifest_json.encode("utf-8")).hexdigest()

    # ponytail: hash all trust-boundary inputs before any database write.
    for reference in spec["references"]:
        actual = _hash_file(Path(reference["path"]))
        if actual != reference["sha256"]:
            raise TrackerError(f"sha256 mismatch for reference: {reference['reference_id']}")

    connection: sqlite3.Connection | None = None
    try:
        connection = _connect(database)
        _ensure_schema(connection)
        connection.execute("BEGIN IMMEDIATE")
        existing = connection.execute(
            "SELECT local_experiment_id, revision, local_manifest_sha256 "
            "FROM experiment_revisions WHERE local_experiment_id=? AND manifest_json=?",
            (spec["local_experiment_id"], manifest_json),
        ).fetchone()
        if existing is not None:
            connection.commit()
            return {
                "local_experiment_id": existing[0],
                "revision": existing[1],
                "local_manifest_sha256": existing[2],
                "idempotent": True,
            }
        latest = connection.execute(
            "SELECT COALESCE(MAX(revision), 0) FROM experiment_revisions WHERE local_experiment_id=?",
            (spec["local_experiment_id"],),
        ).fetchone()[0]
        revision = int(latest) + 1
        cursor = connection.execute(
            "INSERT INTO experiment_revisions (local_experiment_id, revision, manifest_json, "
            "local_manifest_sha256, period_start_utc, period_end_utc, family_reference, "
            "parent_experiment_ids_json, related_experiment_ids_json, created_at_utc) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                spec["local_experiment_id"],
                revision,
                manifest_json,
                manifest_sha,
                spec["period_start_utc"],
                spec["period_end_utc"],
                spec.get("family_reference"),
                _canonical(spec["parent_experiment_ids"]) if "parent_experiment_ids" in spec else None,
                _canonical(spec["related_experiment_ids"]) if "related_experiment_ids" in spec else None,
                _now_utc(),
            ),
        )
        revision_id = cursor.lastrowid
        connection.executemany(
            "INSERT INTO \"references\" (revision_id, reference_id, role, path, sha256) VALUES (?, ?, ?, ?, ?)",
            [
                (revision_id, r["reference_id"], r["role"], r["path"], r["sha256"])
                for r in spec["references"]
            ],
        )
        connection.commit()
        return {
            "local_experiment_id": spec["local_experiment_id"],
            "revision": revision,
            "local_manifest_sha256": manifest_sha,
            "idempotent": False,
        }
    except (sqlite3.Error, OSError) as exc:
        if connection is not None:
            connection.rollback()
        raise TrackerError(f"registration failed: {exc}") from exc
    finally:
        if connection is not None:
            connection.close()


def disclose_report(
    db_path: str | os.PathLike[str],
    experiment_id: str,
    revision: int,
    report_id: str,
    emit_bytes: Callable[[bytes], Any],
) -> dict[str, Any]:
    """Record one valid report disclosure, then emit its exact bytes once."""
    database = _db_path(db_path)
    experiment_id = _text(experiment_id, "experiment_id")
    report_id = _text(report_id, "report_id")
    if type(revision) is not int or revision < 1:
        raise TrackerError("revision must be a positive integer")
    if not callable(emit_bytes):
        raise TrackerError("emit_bytes must be callable")
    connection: sqlite3.Connection | None = None
    try:
        connection = _connect(database, read_only=True)
        row = connection.execute(
            "SELECT r.id, r.path, r.sha256, e.period_start_utc, e.period_end_utc "
        "FROM \"references\" r JOIN experiment_revisions e ON e.id=r.revision_id "
            "WHERE e.local_experiment_id=? AND e.revision=? AND r.reference_id=? AND r.role='report'",
            (experiment_id, revision, report_id),
        ).fetchone()
    except (sqlite3.Error, OSError) as exc:
        if connection is not None:
            connection.close()
        raise TrackerError(f"disclosure lookup failed: {exc}") from exc
    if row is None:
        connection.close()
        raise TrackerError("registered report reference not found")
    reference_row_id, path_value, expected_sha, period_start, period_end = row
    del reference_row_id
    try:
        report_path = _safe_path(path_value, "stored report path", require_absolute=True)
    except TrackerError:
        connection.close()
        raise
    if not SHA256_RE.fullmatch(expected_sha):
        connection.close()
        raise TrackerError("stored report reference is invalid")
    try:
        # Exactly one read into exactly one buffer; this buffer is the one emitted.
        with report_path.open("rb") as handle:
            report_bytes = handle.read()
    except OSError as exc:
        connection.close()
        raise TrackerError(f"report is missing or unreadable: {report_path}") from exc
    report_sha = hashlib.sha256(report_bytes).hexdigest()
    if report_sha != expected_sha:
        connection.close()
        raise TrackerError("report sha256 mismatch; disclosure refused")

    try:
        connection.close()
        connection = _connect(database)
        _ensure_schema(connection)
        connection.execute("BEGIN IMMEDIATE")
        revision_row = connection.execute(
            "SELECT id, period_start_utc, period_end_utc FROM experiment_revisions "
            "WHERE local_experiment_id=? AND revision=?",
            (experiment_id, revision),
        ).fetchone()
        if revision_row is None:
            raise TrackerError("registered experiment revision disappeared")
        connection.execute(
            "INSERT INTO disclosure_attempts (revision_id, experiment_id, revision, report_id, attempted_at_utc, "
            "report_sha256, report_bytes, period_start_utc, period_end_utc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                revision_row[0],
                experiment_id,
                revision,
                report_id,
                _now_utc(),
                report_sha,
                len(report_bytes),
                period_start,
                period_end,
            ),
        )
        connection.commit()
    except (sqlite3.Error, OSError) as exc:
        if connection is not None:
            connection.rollback()
        raise TrackerError(f"disclosure logging failed: {exc}") from exc
    finally:
        if connection is not None:
            connection.close()

    # Commit has completed before this single invocation; emitter failure leaves the event.
    emit_bytes(report_bytes)
    return {
        "local_experiment_id": experiment_id,
        "revision": revision,
        "report_id": report_id,
        "report_sha256": report_sha,
        "report_bytes": len(report_bytes),
    }


def _load_rows(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    revisions: list[dict[str, Any]] = []
    rows = connection.execute(
        "SELECT id, local_experiment_id, revision, manifest_json, local_manifest_sha256, "
        "period_start_utc, period_end_utc, family_reference, parent_experiment_ids_json, "
        "related_experiment_ids_json, created_at_utc FROM experiment_revisions "
        "ORDER BY local_experiment_id, revision"
    ).fetchall()
    for row in rows:
        revision_id, experiment_id, revision, manifest_json, manifest_sha, start, end, family, parents, related, created = row
        experiment_id = _text(experiment_id, "stored experiment id")
        manifest_json = _text(manifest_json, "stored manifest")
        manifest_sha = _sha(manifest_sha, "stored manifest sha256")
        start = _utc(start, "stored period_start_utc")
        end = _utc(end, "stored period_end_utc")
        if start >= end:
            raise TrackerError("stored period_start_utc must be earlier than period_end_utc")
        if family is not None:
            family = _text(family, "stored family_reference")
        references: list[dict[str, Any]] = []
        for ref in connection.execute(
            "SELECT reference_id, role, path, sha256 FROM \"references\" WHERE revision_id=? ORDER BY id",
            (revision_id,),
        ):
            reference_id, role, path_value, expected_sha = ref
            reference_id = _text(reference_id, "stored reference id")
            role = _text(role, "stored reference role")
            expected_sha = _sha(expected_sha, "stored reference sha256")
            path = _safe_path(path_value, "stored reference path", require_absolute=False)
            if not path.is_absolute() or not path.exists() or not path.is_file():
                state = "MISSING"
            else:
                try:
                    actual_sha = _hash_file(path)
                except TrackerError:
                    actual_sha = None
                state = "MATCH" if actual_sha == expected_sha else "MISMATCH"
            references.append(
                {
                    "reference_id": reference_id,
                    "role": role,
                    "path": path_value,
                    "sha256": expected_sha,
                    "state": state,
                }
            )
        disclosures = [
            {
                "attempt_id": attempt[0],
                "report_id": _text(attempt[1], "stored report id"),
                "attempted_at_utc": _utc(attempt[2], "stored attempted_at_utc"),
                "report_sha256": _sha(attempt[3], "stored report sha256"),
                "report_bytes": attempt[4],
                "period_start_utc": _utc(attempt[5], "stored disclosure period_start_utc"),
                "period_end_utc": _utc(attempt[6], "stored disclosure period_end_utc"),
            }
            for attempt in connection.execute(
                "SELECT id, report_id, attempted_at_utc, report_sha256, report_bytes, "
                "period_start_utc, period_end_utc FROM disclosure_attempts WHERE revision_id=? ORDER BY id",
                (revision_id,),
            )
        ]
        revisions.append(
            {
                "local_experiment_id": experiment_id,
                "revision": revision,
                "local_manifest_sha256": manifest_sha,
                "manifest": json.loads(manifest_json),
                "period_start_utc": start,
                "period_end_utc": end,
                "family_reference": family,
                "parent_experiment_ids": json.loads(parents) if parents is not None else None,
                "related_experiment_ids": json.loads(related) if related is not None else None,
                "created_at_utc": created,
                "references": references,
                "disclosures": disclosures,
                "whole_period_local_exposure": bool(disclosures),
            }
        )
    return revisions


def _status_payload(db_path: str | os.PathLike[str]) -> dict[str, Any]:
    database = _db_path(db_path)
    connection: sqlite3.Connection | None = None
    try:
        connection = _connect(database, read_only=True)
        revisions = _load_rows(connection)
    except (sqlite3.Error, OSError) as exc:
        raise TrackerError(f"status failed: {exc}") from exc
    finally:
        if connection is not None:
            connection.close()

    all_disclosures = [
        {**disclosure, "local_experiment_id": revision["local_experiment_id"], "revision": revision["revision"]}
        for revision in revisions
        for disclosure in revision["disclosures"]
    ]
    overlaps: list[dict[str, Any]] = []
    for index, left in enumerate(revisions):
        left_start = left["period_start_utc"]
        left_end = left["period_end_utc"]
        for right in revisions[index + 1 :]:
            start = max(left_start, right["period_start_utc"])
            end = min(left_end, right["period_end_utc"])
            if start < end:
                overlaps.append(
                    {
                        "left": {"local_experiment_id": left["local_experiment_id"], "revision": left["revision"]},
                        "right": {"local_experiment_id": right["local_experiment_id"], "revision": right["revision"]},
                        "overlap_start_utc": start,
                        "overlap_end_utc": end,
                    }
                )

    lineage_conflicts: list[dict[str, Any]] = []
    by_experiment: dict[str, list[dict[str, Any]]] = {}
    for revision in revisions:
        by_experiment.setdefault(revision["local_experiment_id"], []).append(revision)
    for experiment_id, group in by_experiment.items():
        if len(group) < 2:
            continue
        fields = ("family_reference", "parent_experiment_ids", "related_experiment_ids")
        for field in fields:
            values = {_canonical(revision[field]) for revision in group}
            if len(values) > 1:
                lineage_conflicts.append(
                    {
                        "local_experiment_id": experiment_id,
                        "field": field,
                        "revisions": [revision["revision"] for revision in group],
                        "values": [revision[field] for revision in group],
                    }
                )

    lineage_warnings = [
        f"{revision['local_experiment_id']} revision {revision['revision']} has unknown family_reference"
        for revision in revisions
        if revision["family_reference"] is None
    ]
    lineage_warnings.extend(
        f"{revision['local_experiment_id']} revision {revision['revision']} reuses known family_reference "
        f"{revision['family_reference']}; reuse is not evidence of independence"
        for revision in revisions
        if revision["family_reference"] is not None
    )
    lineage_warnings.extend(
        f"{revision['local_experiment_id']} revision {revision['revision']} has unknown parent_experiment_ids"
        for revision in revisions
        if revision["parent_experiment_ids"] is None
    )
    lineage_warnings.extend(
        f"{revision['local_experiment_id']} revision {revision['revision']} has unknown related_experiment_ids"
        for revision in revisions
        if revision["related_experiment_ids"] is None
    )
    lineage_warnings.extend(
        f"{revision['local_experiment_id']} revision {revision['revision']} declares known parent_experiment_ids "
        f"{revision['parent_experiment_ids']}; lineage is not independently verified"
        for revision in revisions
        if revision["parent_experiment_ids"]
    )
    lineage_warnings.extend(
        f"{revision['local_experiment_id']} revision {revision['revision']} declares known related_experiment_ids "
        f"{revision['related_experiment_ids']}; related reuse is not independently verified"
        for revision in revisions
        if revision["related_experiment_ids"]
    )
    access_warnings = [
        "Notebook, AI, file-browser, export, raw-file, copied-file, and other reader paths are unmonitored.",
        "This local application history is not tamper-proof and is not an independent clock or observer.",
        "Unlogged prior reads and copies cannot be repaired retroactively; records remain development data.",
        "An empty disclosure log, a new name, or a new local ID is not evidence of independence.",
    ]
    return {
        "classification": "LOCAL_LOG_ONLY",
        "access_completeness": "ACCESS_COMPLETENESS_UNVERIFIED",
        "revisions": revisions,
        "disclosure_attempts": all_disclosures,
        "whole_period_local_exposure": [
            {
                "local_experiment_id": revision["local_experiment_id"],
                "revision": revision["revision"],
                "period_start_utc": revision["period_start_utc"],
                "period_end_utc": revision["period_end_utc"],
                "exposed": revision["whole_period_local_exposure"],
            }
            for revision in revisions
        ],
        "overlapping_declared_periods": overlaps,
        "known_lineage_links": [
            {
                "local_experiment_id": revision["local_experiment_id"],
                "revision": revision["revision"],
                "family_reference": revision["family_reference"],
                "parent_experiment_ids": revision["parent_experiment_ids"],
                "related_experiment_ids": revision["related_experiment_ids"],
            }
            for revision in revisions
        ],
        "lineage_conflicts_across_revisions": lineage_conflicts,
        "unresolved_lineage_warnings": lineage_warnings,
        "unresolved_access_history_warnings": access_warnings,
        "limitations": [
            "No untouched duration is produced; clean-window status is unavailable.",
            "No P0-22 acceptance/admission receipt or promotion eligibility is produced.",
            "Canonical family resolution, complete reader-path instrumentation, independent protected access/clock history, and full-window binding remain future work.",
        ],
    }


def status(db_path: str | os.PathLike[str], output_format: str = "json") -> str:
    if output_format not in {"json", "markdown"}:
        raise TrackerError("format must be json or markdown")
    payload = _status_payload(db_path)
    if output_format == "json":
        return _canonical(payload)
    lines = [
        "# P0-22 Local Research Tracker",
        "",
        f"- Classification: {_md(payload['classification'])}",
        f"- Access completeness: {_md(payload['access_completeness'])}",
        f"- Revisions: {_md(len(payload['revisions']))}",
        f"- Disclosure attempts: {_md(len(payload['disclosure_attempts']))}",
        f"- Overlapping declared periods: {_md(len(payload['overlapping_declared_periods']))}",
        "",
        "## Revisions",
        "",
    ]
    for revision in payload["revisions"]:
        lines.append(
            f"- {_md(revision['local_experiment_id'])} revision {_md(revision['revision'])}: "
            f"{_md(revision['period_start_utc'])} to {_md(revision['period_end_utc'])}; "
            f"whole-period local exposure = {_md(revision['whole_period_local_exposure'])}"
        )
        for reference in revision["references"]:
            lines.append(
                f"  - {_md(reference['reference_id'])} ({_md(reference['role'])}): "
                f"{_md(reference['state'])}"
            )
    lines.extend(["", "## Warnings and limitations", ""])
    for warning in payload["unresolved_lineage_warnings"] + payload["unresolved_access_history_warnings"] + payload["limitations"]:
        lines.append(f"- {_md(warning)}")
    lines.extend(["", "## Disclosure attempts", ""])
    for attempt in payload["disclosure_attempts"]:
        lines.append(
            f"- attempt {_md(attempt['attempt_id'])}: {_md(attempt['local_experiment_id'])} revision "
            f"{_md(attempt['revision'])}, report {_md(attempt['report_id'])}, "
            f"period {_md(attempt['period_start_utc'])} to {_md(attempt['period_end_utc'])}"
        )
    lines.extend(["", "## Declared period overlaps", ""])
    for overlap in payload["overlapping_declared_periods"]:
        left = overlap["left"]
        right = overlap["right"]
        lines.append(
            f"- {_md(left['local_experiment_id'])} revision {_md(left['revision'])} overlaps "
            f"{_md(right['local_experiment_id'])} revision {_md(right['revision'])} "
            f"from {_md(overlap['overlap_start_utc'])} to {_md(overlap['overlap_end_utc'])}"
        )
    lines.extend(["", "## Known lineage links", ""])
    for link in payload["known_lineage_links"]:
        lines.append(
            f"- {_md(link['local_experiment_id'])} revision {_md(link['revision'])}: "
            f"family={_md(link['family_reference'])}, parents={_md(link['parent_experiment_ids'])}, "
            f"related={_md(link['related_experiment_ids'])}"
        )
    lines.extend(["", "## Lineage conflicts", ""])
    for conflict in payload["lineage_conflicts_across_revisions"]:
        lines.append(
            f"- {_md(conflict['local_experiment_id'])} field {_md(conflict['field'])} "
            f"differs across revisions {_md(conflict['revisions'])}: {_md(conflict['values'])}"
        )
    return "\n".join(lines) + "\n"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track local research manifests and report disclosures.")
    commands = parser.add_subparsers(dest="command", required=True)
    register_parser = commands.add_parser("register", help="register a validated local experiment manifest")
    register_parser.add_argument("--db", required=True, help="SQLite database path")
    register_parser.add_argument("--spec", required=True, help="version-1 manifest JSON path")
    disclose_parser = commands.add_parser("disclose", help="record and emit one registered report")
    disclose_parser.add_argument("--db", required=True, help="SQLite database path")
    disclose_parser.add_argument("--experiment-id", required=True)
    disclose_parser.add_argument("--revision", required=True, type=int)
    disclose_parser.add_argument("--report-id", required=True)
    status_parser = commands.add_parser("status", help="show local tracker status")
    status_parser.add_argument("--db", required=True, help="SQLite database path")
    status_parser.add_argument("--format", choices=("json", "markdown"), required=True)
    return parser


def _stdout_text(value: str) -> None:
    """Write protocol text as UTF-8 regardless of the Windows console locale."""
    sys.stdout.buffer.write(value.encode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        if args.command == "register":
            _stdout_text(_canonical(register(args.db, args.spec)) + "\n")
        elif args.command == "disclose":
            disclose_report(args.db, args.experiment_id, args.revision, args.report_id, sys.stdout.buffer.write)
        else:
            _stdout_text(status(args.db, args.format))
        return 0
    except (TrackerError, OSError, sqlite3.Error, BrokenPipeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
