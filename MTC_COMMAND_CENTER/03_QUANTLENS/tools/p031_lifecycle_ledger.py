"""P0-31 Milestone 1 local append-only lifecycle ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sqlite3
import sys
import tempfile
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


CONTRACTS_DIR = Path(__file__).resolve().parents[2] / "contracts"
if str(CONTRACTS_DIR) not in sys.path:
    sys.path.insert(0, str(CONTRACTS_DIR))

from mtc_contracts.execution import LifecycleEvent, LifecycleWriterClass


SCHEMA_VERSION = "p031.lifecycle-ledger.v1"
ZERO_DIGEST = "0" * 64
SHA256 = re.compile(r"^[0-9a-f]{64}$")
CHECK_SET_PURPOSES = frozenset(
    {
        "worthiness",
        "shadow_eligibility",
        "paper_eligibility",
        "testnet_live_candidate_eligibility",
        "live_candidate_eligibility",
        "promotion",
        "supervisor",
    }
)

REGISTRAR_TRANSITIONS = frozenset(
    {
        (None, "CAPTURED", "CAPTURED"),
        ("CAPTURED", "TRIAGED", "TRIAGED"),
        ("CAPTURED", "DECLINED", "DECLINED"),
        ("TRIAGED", "CANDIDATE", "CANDIDATE"),
        ("CANDIDATE", "FROZEN", "FROZEN"),
        ("CANDIDATE", "PARKED", "PARKED"),
        ("DECLINED", "RE_ENTRY", "CANDIDATE"),
        ("PARKED", "RE_ENTRY", "CANDIDATE"),
        ("RETIRED", "RE_ENTRY", "CANDIDATE"),
    }
)
REENTRY_TRIGGERS = frozenset(
    {
        "NEW_DATA_REGIME",
        "NEW_KERNEL_VERSION",
        "NEW_SUBSTITUTE_CATALOGUE",
        "NEW_ENRICHMENT_MODULES",
        "OWNER_CURIOSITY",
    }
)
AUTHORITY_EVENTS = {
    LifecycleWriterClass.REGISTRAR: frozenset(
        {
            "CAPTURED",
            "TRIAGED",
            "DECLINED",
            "CANDIDATE",
            "FROZEN",
            "PARKED",
            "REJECTED",
            "RE_ENTRY",
        }
    ),
    LifecycleWriterClass.ENVIRONMENT_ADMISSION_AUTHORITY: frozenset(
        {
            "SHADOW_ELIGIBLE",
            "PAPER_ELIGIBLE",
            "TESTNET_ELIGIBLE",
            "ADMISSION_WITHHELD_CAPACITY",
            "LIVE_CANDIDATE",
        }
    ),
    LifecycleWriterClass.PROMOTION_AUTHORITY: frozenset({"PROMOTED", "RESUMED"}),
    LifecycleWriterClass.MULTI_WORKER_SUPERVISOR: frozenset(
        {"SUSPENDED", "RESUMED", "RETIRED"}
    ),
}
LADDER_TRANSITIONS = frozenset(
    {
        ("FROZEN", "SHADOW_ELIGIBLE", "SHADOW"),
        ("SHADOW", "PAPER_ELIGIBLE", "SHADOW"),
        ("SHADOW", "TESTNET_ELIGIBLE", "TESTNET"),
        ("TESTNET", "LIVE_CANDIDATE", "LIVE_CANDIDATE"),
        ("LIVE_CANDIDATE", "PROMOTED", "LIVE"),
        ("FROZEN", "ADMISSION_WITHHELD_CAPACITY", "FROZEN"),
        ("SHADOW", "SUSPENDED", "SUSPENDED"),
        ("TESTNET", "SUSPENDED", "SUSPENDED"),
        ("LIVE_CANDIDATE", "SUSPENDED", "SUSPENDED"),
        ("LIVE", "SUSPENDED", "SUSPENDED"),
        ("SUSPENDED", "RESUMED", "SHADOW"),
        ("SUSPENDED", "RESUMED", "TESTNET"),
        ("SUSPENDED", "RESUMED", "LIVE_CANDIDATE"),
        ("SUSPENDED", "RESUMED", "LIVE"),
        ("SHADOW", "RETIRED", "RETIRED"),
        ("TESTNET", "RETIRED", "RETIRED"),
        ("LIVE_CANDIDATE", "RETIRED", "RETIRED"),
        ("LIVE", "RETIRED", "RETIRED"),
        ("SUSPENDED", "RETIRED", "RETIRED"),
    }
)

IMMUTABLE_TRIGGER_SQL = {
    "lifecycle_events_no_update": """
        CREATE TRIGGER lifecycle_events_no_update
        BEFORE UPDATE ON lifecycle_events
        BEGIN SELECT RAISE(ABORT, 'IMMUTABLE_EVENT_HISTORY'); END
    """,
    "lifecycle_events_no_delete": """
        CREATE TRIGGER lifecycle_events_no_delete
        BEFORE DELETE ON lifecycle_events
        BEGIN SELECT RAISE(ABORT, 'IMMUTABLE_EVENT_HISTORY'); END
    """,
}
REQUIRED_TABLE_SQL = {
    "ledger_metadata": """
        CREATE TABLE ledger_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """,
    "lifecycle_events": """
        CREATE TABLE lifecycle_events (
            global_sequence INTEGER PRIMARY KEY,
            event_id TEXT NOT NULL UNIQUE,
            writer_class TEXT NOT NULL,
            writer_id TEXT NOT NULL,
            writer_sequence INTEGER NOT NULL,
            candidate_id TEXT NOT NULL,
            canonical_event BLOB NOT NULL,
            canonical_evidence BLOB NOT NULL,
            previous_digest TEXT NOT NULL,
            digest TEXT NOT NULL,
            UNIQUE (writer_class, writer_id, writer_sequence)
        )
    """,
    "lifecycle_current": """
        CREATE TABLE lifecycle_current (
            candidate_id TEXT PRIMARY KEY,
            current_state TEXT NOT NULL,
            package_hash TEXT,
            deployment_identity_hash TEXT,
            last_sequence INTEGER NOT NULL,
            source_kind TEXT NOT NULL CHECK (source_kind = 'FIXTURE'),
            authoritative INTEGER NOT NULL CHECK (authoritative = 0)
        )
    """,
}


@dataclass(frozen=True, slots=True)
class LifecycleRecord:
    """Public replay record carrying its local evidence provenance."""

    event: LifecycleEvent
    check_set_purpose: str | None
    check_set_version: str | None
    evaluation_run_hash: str | None
    failing_checks: tuple[dict[str, Any], ...]
    source_kind: str
    authoritative: bool = False

    def __getattr__(self, name: str) -> Any:
        return getattr(self.event, name)


def _canonical_event(event: LifecycleEvent) -> bytes:
    return json.dumps(
        event.model_dump(mode="json"),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _canonical_evidence(
    check_set_purpose: str | None,
    check_set_version: str | None,
    evaluation_run_hash: str | None,
    failing_checks: tuple[dict[str, Any], ...],
    source_kind: str,
) -> bytes:
    return json.dumps(
        {
            "check_set_purpose": check_set_purpose,
            "check_set_version": check_set_version,
            "evaluation_run_hash": evaluation_run_hash,
            "failing_checks": list(failing_checks),
            "source_kind": source_kind,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(previous: str, event_bytes: bytes, evidence_bytes: bytes) -> str:
    return hashlib.sha256(
        previous.encode("ascii") + b"\n" + event_bytes + b"\n" + evidence_bytes
    ).hexdigest()


def _validated_writer_pair(writer_pair: object, error: str) -> tuple[str, str]:
    if type(writer_pair) is not tuple or len(writer_pair) != 2:
        raise ValueError(error)
    writer_class, writer_id = writer_pair
    if type(writer_class) is LifecycleWriterClass:
        writer_class_value = writer_class.value
    elif type(writer_class) is str:
        writer_class_value = writer_class
    else:
        raise ValueError(error)
    if type(writer_id) is not str or not writer_class_value or not writer_id:
        raise ValueError(error)
    return writer_class_value, writer_id


def _normalize_schema_sql(sql: str | None) -> str:
    if sql is None:
        return ""
    normalized: list[str] = []
    quoted_until: str | None = None
    index = 0
    while index < len(sql):
        character = sql[index]
        if quoted_until is None:
            if character.isspace():
                index += 1
                continue
            normalized.append(character.casefold())
            if character in {"'", '"', "`"}:
                quoted_until = character
            elif character == "[":
                quoted_until = "]"
        else:
            normalized.append(character)
            if character == quoted_until:
                if index + 1 < len(sql) and sql[index + 1] == quoted_until:
                    normalized.append(sql[index + 1])
                    index += 1
                else:
                    quoted_until = None
        index += 1
    return "".join(normalized)


class LifecycleLedger:
    """A single-file SQLite ledger with one guarded append route."""

    def __init__(
        self,
        path: str | Path,
        writer_allowlist: Iterable[tuple[str | LifecycleWriterClass, str]] | None = None,
        active_check_sets: Mapping[str, Iterable[str]] | None = None,
    ) -> None:
        if writer_allowlist is None:
            raise ValueError("WRITER_ALLOWLIST_EMPTY")
        self.path = Path(path)
        self.writer_allowlist = frozenset(
            _validated_writer_pair(writer_pair, "WRITER_ALLOWLIST_INVALID")
            for writer_pair in writer_allowlist
        )
        if not self.writer_allowlist:
            raise ValueError("WRITER_ALLOWLIST_EMPTY")
        self.active_check_sets = self._normalize_active_check_sets(active_check_sets)
        existed = self.path.exists()
        if not existed:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = self._connect()
        try:
            if existed:
                self._validate_database(connection)
            else:
                self._create_schema(connection)
        finally:
            connection.close()

    def _connect(self, *, readonly: bool = False) -> sqlite3.Connection:
        if readonly:
            connection = sqlite3.connect(
                self.path.resolve().as_uri() + "?mode=ro", uri=True, timeout=10
            )
        else:
            connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        return connection

    @staticmethod
    def _normalize_active_check_sets(
        active_check_sets: Mapping[str, Iterable[str]] | None,
    ) -> dict[str, frozenset[str]]:
        if active_check_sets is None:
            return {}
        if not isinstance(active_check_sets, Mapping):
            raise ValueError("ACTIVE_CHECK_SETS_MAPPING_REQUIRED")
        normalized: dict[str, frozenset[str]] = {}
        for purpose, versions in active_check_sets.items():
            if type(purpose) is not str or purpose not in CHECK_SET_PURPOSES:
                raise ValueError("CHECK_SET_PURPOSE_UNKNOWN")
            if isinstance(versions, (str, bytes, bytearray)) or not isinstance(
                versions, Iterable
            ):
                raise ValueError("CHECK_SET_VERSIONS_INVALID")
            version_values = tuple(versions)
            if any(type(version) is not str for version in version_values):
                raise ValueError("CHECK_SET_VERSIONS_INVALID")
            normalized_versions = frozenset(version_values)
            if not normalized_versions or any(
                not version.strip() for version in normalized_versions
            ):
                raise ValueError("CHECK_SET_VERSIONS_INVALID")
            normalized[purpose] = normalized_versions
        return normalized

    @staticmethod
    def _create_schema(connection: sqlite3.Connection) -> None:
        connection.executescript(
            """
            CREATE TABLE ledger_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE lifecycle_events (
                global_sequence INTEGER PRIMARY KEY,
                event_id TEXT NOT NULL UNIQUE,
                writer_class TEXT NOT NULL,
                writer_id TEXT NOT NULL,
                writer_sequence INTEGER NOT NULL,
                candidate_id TEXT NOT NULL,
                canonical_event BLOB NOT NULL,
                canonical_evidence BLOB NOT NULL,
                previous_digest TEXT NOT NULL,
                digest TEXT NOT NULL,
                UNIQUE (writer_class, writer_id, writer_sequence)
            );
            CREATE TABLE lifecycle_current (
                candidate_id TEXT PRIMARY KEY,
                current_state TEXT NOT NULL,
                package_hash TEXT,
                deployment_identity_hash TEXT,
                last_sequence INTEGER NOT NULL,
                source_kind TEXT NOT NULL CHECK (source_kind = 'FIXTURE'),
                authoritative INTEGER NOT NULL CHECK (authoritative = 0)
            );
            CREATE TRIGGER lifecycle_events_no_update
            BEFORE UPDATE ON lifecycle_events
            BEGIN SELECT RAISE(ABORT, 'IMMUTABLE_EVENT_HISTORY'); END;
            CREATE TRIGGER lifecycle_events_no_delete
            BEFORE DELETE ON lifecycle_events
            BEGIN SELECT RAISE(ABORT, 'IMMUTABLE_EVENT_HISTORY'); END;
            """
        )
        connection.execute(
            "INSERT INTO ledger_metadata(key, value) VALUES ('schema_version', ?)",
            (SCHEMA_VERSION,),
        )
        connection.commit()

    @staticmethod
    def _validate_database(connection: sqlite3.Connection) -> None:
        result = connection.execute("PRAGMA quick_check").fetchone()
        if result is None or result[0] != "ok":
            raise ValueError("SQLITE_INTEGRITY_FAILURE")
        try:
            row = connection.execute(
                "SELECT value FROM ledger_metadata WHERE key = 'schema_version'"
            ).fetchone()
        except sqlite3.DatabaseError:
            raise
        if row is None or row[0] != SCHEMA_VERSION:
            raise ValueError("SCHEMA_VERSION_MISMATCH")
        object_rows = connection.execute(
            "SELECT type, name, tbl_name, sql FROM sqlite_master "
            "WHERE NOT (type = 'index' AND sql IS NULL "
            "AND name LIKE 'sqlite_autoindex_%')"
        ).fetchall()
        actual_objects = {
            (row[0], row[1]): (row[2], _normalize_schema_sql(row[3]))
            for row in object_rows
        }
        expected_objects = {
            **{
                ("table", name): (name, _normalize_schema_sql(sql))
                for name, sql in REQUIRED_TABLE_SQL.items()
            },
            **{
                ("trigger", name): (
                    "lifecycle_events",
                    _normalize_schema_sql(sql),
                )
                for name, sql in IMMUTABLE_TRIGGER_SQL.items()
            },
        }
        if actual_objects != expected_objects:
            raise ValueError("SCHEMA_OBJECT_SET_INVALID")

    @staticmethod
    def _validated_event(event: LifecycleEvent) -> tuple[LifecycleEvent, bytes]:
        if not isinstance(event, LifecycleEvent):
            raise TypeError("LIFECYCLE_EVENT_REQUIRED")
        validated = LifecycleEvent.model_validate(event.model_dump(mode="python"))
        if validated.timestamp.utcoffset() != timedelta(0):
            raise ValueError("TIMESTAMP_NOT_UTC")
        event_bytes = _canonical_event(validated)
        try:
            resolved = LifecycleEvent.model_validate_json(event_bytes)
        except Exception as exc:
            raise ValueError("INVALID_CANONICAL_PAYLOAD") from exc
        if _canonical_event(resolved) != event_bytes:
            raise ValueError("NONCANONICAL_PAYLOAD")
        if type(resolved.timestamp) is not datetime or resolved.timestamp.utcoffset() != timedelta(0):
            raise ValueError("TIMESTAMP_NOT_UTC")
        return resolved, event_bytes

    @staticmethod
    def _normalize_evidence(
        check_set_version: str | None,
        evaluation_run_hash: str | None,
        failing_checks: Sequence[Mapping[str, Any]],
        source_kind: str,
    ) -> tuple[str | None, str | None, tuple[dict[str, Any], ...], str]:
        if check_set_version is not None and (
            type(check_set_version) is not str or not check_set_version.strip()
        ):
            raise ValueError("CHECK_SET_VERSION_INVALID")
        if evaluation_run_hash is not None and (
            type(evaluation_run_hash) is not str
            or not SHA256.fullmatch(evaluation_run_hash)
        ):
            raise ValueError("EVALUATION_RUN_HASH_INVALID")
        if isinstance(failing_checks, (str, bytes, bytearray)) or not isinstance(
            failing_checks, Sequence
        ):
            raise ValueError("FAILING_CHECKS_INVALID")
        checks: list[dict[str, Any]] = []
        check_ids: set[str] = set()
        required = {"check_id", "observed_value", "threshold"}
        for value in failing_checks:
            if not isinstance(value, Mapping) or set(value) != required:
                raise ValueError("FAILING_CHECKS_INVALID")
            try:
                check_id = value["check_id"]
                observed = value["observed_value"]
                threshold = value["threshold"]
            except Exception as exc:
                raise ValueError("FAILING_CHECKS_INVALID") from exc
            if (
                type(check_id) is not str
                or not check_id.strip()
                or check_id in check_ids
                or not LifecycleLedger._is_json_scalar(observed)
                or not LifecycleLedger._is_json_scalar(threshold)
            ):
                raise ValueError("FAILING_CHECKS_INVALID")
            check_ids.add(check_id)
            checks.append(
                {
                    "check_id": check_id,
                    "observed_value": observed,
                    "threshold": threshold,
                }
            )
        if type(source_kind) is not str or source_kind != "FIXTURE":
            raise ValueError("SOURCE_KIND_NOT_FIXTURE")
        return check_set_version, evaluation_run_hash, tuple(checks), source_kind

    @staticmethod
    def _is_json_scalar(value: Any) -> bool:
        return value is not None and isinstance(value, (str, int, float, bool)) and not (
            isinstance(value, float) and not math.isfinite(value)
        )

    @staticmethod
    def _state_from_row(row: sqlite3.Row) -> dict[str, Any]:
        state = dict(row)
        state["authoritative"] = bool(state["authoritative"])
        return state

    @staticmethod
    def _check_set_purpose(event: LifecycleEvent) -> str | None:
        if event.event_type in {"TRIAGED", "DECLINED"}:
            return "worthiness"
        if event.event_type == "SHADOW_ELIGIBLE":
            return "shadow_eligibility"
        if event.event_type == "PAPER_ELIGIBLE":
            return "paper_eligibility"
        if event.event_type == "TESTNET_ELIGIBLE":
            return "testnet_live_candidate_eligibility"
        if event.event_type == "LIVE_CANDIDATE":
            return "live_candidate_eligibility"
        if event.event_type == "ADMISSION_WITHHELD_CAPACITY":
            return "shadow_eligibility" if event.previous_state == "FROZEN" else None
        if event.event_type == "PROMOTED" or (
            event.event_type == "RESUMED"
            and event.writer_class is LifecycleWriterClass.PROMOTION_AUTHORITY
        ):
            return "promotion"
        if event.event_type in {"SUSPENDED", "RETIRED"} or (
            event.event_type == "RESUMED"
            and event.writer_class is LifecycleWriterClass.MULTI_WORKER_SUPERVISOR
        ):
            return "supervisor"
        return None

    def _validate_transition(
        self,
        event: LifecycleEvent,
        current: Mapping[str, Any] | None,
        *,
        check_set_version: str | None,
        evaluation_run_hash: str | None,
        failing_checks: tuple[dict[str, Any], ...],
        prior_evaluations: set[str],
        current_evaluations: set[str],
        evaluation_owners: Mapping[str, str],
        last_timestamp: datetime | None,
        suspended_from_state: str | None,
        suspended_from: Mapping[str, str],
        states: Mapping[str, Mapping[str, Any]],
        deployment_owners: Mapping[str, str],
        retired_deployments: set[str],
        retired_packages: Mapping[str, set[str]],
        enforce_active: bool,
    ) -> tuple[str | None, str | None]:
        if not event.evidence_references:
            raise ValueError("EVIDENCE_REFERENCES_REQUIRED")
        writer_class = event.writer_class
        if event.event_type == "DEMOTED":
            raise ValueError("DEMOTION_TARGET_RUNG_MAPPING_UNRESOLVED")
        if event.event_type == "CHALLENGE":
            raise ValueError("CHALLENGE_INCUMBENT_DEPLOYMENT_IDENTITY_FIELD_MISSING")
        if event.event_type == "REJECTED":
            raise ValueError("REJECTED_PURPOSE_UNRESOLVED")
        if (
            event.event_type == "ADMISSION_WITHHELD_CAPACITY"
            and event.previous_state == "SHADOW"
        ):
            raise ValueError("ADMISSION_WITHHELD_TARGET_UNRESOLVED")
        actual_state = None if current is None else str(current["current_state"])
        if actual_state == "RETIRED" and event.event_type != "RE_ENTRY":
            raise ValueError("RETIRED_IDENTITY_TERMINAL")
        if event.event_type not in AUTHORITY_EVENTS[writer_class]:
            raise ValueError("WRITER_AUTHORITY_REFUSED")
        if event.previous_state != actual_state:
            raise ValueError("PREVIOUS_STATE_MISMATCH")
        if last_timestamp is not None and event.timestamp < last_timestamp:
            raise ValueError("TIMESTAMP_NOT_MONOTONIC")

        if (
            writer_class is not LifecycleWriterClass.REGISTRAR
            and actual_state
            in {"SHADOW", "TESTNET", "LIVE_CANDIDATE", "LIVE", "SUSPENDED"}
            and current is not None
            and event.package_hash == current.get("package_hash")
            and current.get("deployment_identity_hash") is not None
            and event.deployment_identity_hash is not None
            and event.deployment_identity_hash
            != current.get("deployment_identity_hash")
        ):
            raise ValueError("DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED")

        transition = (event.previous_state, event.event_type, event.next_state)
        if writer_class is LifecycleWriterClass.REGISTRAR:
            if transition not in REGISTRAR_TRANSITIONS:
                raise ValueError("ILLEGAL_TRANSITION")
        elif transition not in LADDER_TRANSITIONS:
            raise ValueError("ILLEGAL_TRANSITION")
        if event.event_type == "RESUMED":
            if suspended_from_state is None or event.next_state != suspended_from_state:
                raise ValueError("RESUME_TARGET_RUNG_MISMATCH")
            expected_writer = (
                LifecycleWriterClass.PROMOTION_AUTHORITY
                if suspended_from_state == "LIVE"
                else LifecycleWriterClass.MULTI_WORKER_SUPERVISOR
            )
            if writer_class is not expected_writer:
                raise ValueError("RESUME_WRITER_AUTHORITY_MISMATCH")
        if event.event_type == "PROMOTED" and any(
            candidate_id != event.candidate_id
            and (
                state["current_state"] == "LIVE"
                or (
                    state["current_state"] == "SUSPENDED"
                    and suspended_from.get(candidate_id) == "LIVE"
                )
            )
            for candidate_id, state in states.items()
        ):
            raise ValueError("SUCCESSION_ENVELOPE_UNRESOLVED")

        check_set_purpose = self._check_set_purpose(event)
        needs_check_set = check_set_purpose is not None
        if needs_check_set and check_set_version is None:
            raise ValueError("CHECK_SET_REQUIRED")
        if not needs_check_set and check_set_version is not None:
            raise ValueError("CHECK_SET_NOT_APPLICABLE")
        if enforce_active and needs_check_set:
            if check_set_version not in self.active_check_sets.get(
                check_set_purpose, ()
            ):
                raise ValueError("CHECK_SET_PURPOSE_MISMATCH")

        if event.event_type != "RE_ENTRY" and event.trigger is not None:
            raise ValueError("TRIGGER_NOT_APPLICABLE")
        if event.event_type == "RE_ENTRY":
            if event.trigger not in REENTRY_TRIGGERS:
                raise ValueError("REENTRY_TRIGGER_INVALID")
            if evaluation_run_hash is None or evaluation_run_hash in (
                prior_evaluations | current_evaluations
            ):
                raise ValueError("REENTRY_EVALUATION_NOT_FRESH")
            if failing_checks:
                raise ValueError("REENTRY_RECOUNTS_PRIOR_EVIDENCE")
        elif writer_class is not LifecycleWriterClass.REGISTRAR and evaluation_run_hash is None:
            raise ValueError("EVALUATION_RUN_HASH_REQUIRED")
        elif writer_class is LifecycleWriterClass.REGISTRAR and evaluation_run_hash is not None:
            raise ValueError("EVALUATION_RUN_HASH_NOT_APPLICABLE")
        elif failing_checks:
            raise ValueError("FAILING_CHECKS_NOT_APPLICABLE")
        evaluation_owner = (
            None
            if evaluation_run_hash is None
            else evaluation_owners.get(evaluation_run_hash)
        )
        if evaluation_owner is not None and evaluation_owner != event.candidate_id:
            raise ValueError("EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED")
        if (
            event.event_type != "RE_ENTRY"
            and evaluation_run_hash is not None
            and evaluation_run_hash in prior_evaluations
        ):
            raise ValueError("EVALUATION_RUN_HASH_REUSED")

        package_hash = event.package_hash
        deployment_hash = event.deployment_identity_hash
        if writer_class is LifecycleWriterClass.REGISTRAR:
            if event.event_type == "FROZEN":
                if package_hash is None:
                    raise ValueError("FROZEN_PACKAGE_HASH_REQUIRED")
                if deployment_hash is not None:
                    raise ValueError("FROZEN_DEPLOYMENT_IDENTITY_FORBIDDEN")
                if package_hash in retired_packages.get(event.candidate_id, set()):
                    raise ValueError("RETIRED_PACKAGE_IDENTITY")
            elif package_hash is not None or deployment_hash is not None:
                raise ValueError("PRE_FREEZE_IDENTITY_TOO_DEEP")
        else:
            if package_hash is None or deployment_hash is None:
                raise ValueError("LADDER_IDENTITY_INCOMPLETE")
            frozen_package = None if current is None else current.get("package_hash")
            current_deployment = None if current is None else current.get(
                "deployment_identity_hash"
            )
            if frozen_package is None or package_hash != frozen_package:
                raise ValueError("PACKAGE_IDENTITY_MISMATCH")
            if current_deployment is not None and deployment_hash != current_deployment:
                raise ValueError("DEPLOYMENT_IDENTITY_MISMATCH")
            if deployment_hash in retired_deployments:
                raise ValueError("DEPLOYMENT_IDENTITY_RETIRED")
            owner = deployment_owners.get(deployment_hash)
            if owner is not None and owner != event.candidate_id:
                raise ValueError("DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE")

        if event.event_type == "RE_ENTRY" and actual_state == "RETIRED":
            return None, None
        next_package = package_hash or (None if current is None else current.get("package_hash"))
        next_deployment = deployment_hash or (
            None if current is None else current.get("deployment_identity_hash")
        )
        return next_package, next_deployment

    def append(
        self,
        event: LifecycleEvent,
        *,
        check_set_version: str | None = None,
        evaluation_run_hash: str | None = None,
        failing_checks: Sequence[Mapping[str, Any]] = (),
        source_kind: str = "FIXTURE",
    ) -> LifecycleEvent:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            self._validate_database(connection)
            event, event_bytes = self._validated_event(event)
            (
                check_set_version,
                evaluation_run_hash,
                checks,
                source_kind,
            ) = self._normalize_evidence(
                check_set_version, evaluation_run_hash, failing_checks, source_kind
            )
            check_set_purpose = self._check_set_purpose(event)
            evidence_bytes = _canonical_evidence(
                check_set_purpose,
                check_set_version,
                evaluation_run_hash,
                checks,
                source_kind,
            )
            writer_pair = (event.writer_class.value, event.writer_id)
            if writer_pair not in self.writer_allowlist:
                raise ValueError("WRITER_NOT_ALLOWLISTED")
            (
                history,
                states,
                writer_sequences,
                suspended_from,
                deployment_owners,
                retired_deployments,
                retired_packages,
                prior_evaluations,
                current_evaluations,
                evaluation_owners,
                last_timestamps,
            ) = self._validated_history(connection)
            actual_view = {
                row["candidate_id"]: self._state_from_row(row)
                for row in connection.execute("SELECT * FROM lifecycle_current")
            }
            if actual_view != states:
                raise ValueError("DERIVED_VIEW_DRIFT")
            duplicate = connection.execute(
                "SELECT canonical_event, canonical_evidence FROM lifecycle_events "
                "WHERE event_id = ?",
                (event.event_id,),
            ).fetchone()
            if duplicate is not None:
                if (
                    bytes(duplicate[0]) == event_bytes
                    and bytes(duplicate[1]) == evidence_bytes
                ):
                    raise ValueError("DUPLICATE_EVENT")
                raise ValueError("CONFLICTING_EVENT")

            current = states.get(event.candidate_id)
            package_hash, deployment_hash = self._validate_transition(
                event,
                current,
                check_set_version=check_set_version,
                evaluation_run_hash=evaluation_run_hash,
                failing_checks=checks,
                prior_evaluations=prior_evaluations.setdefault(
                    event.candidate_id, set()
                ),
                current_evaluations=current_evaluations.setdefault(
                    event.candidate_id, set()
                ),
                evaluation_owners=evaluation_owners,
                last_timestamp=last_timestamps.get(event.candidate_id),
                suspended_from_state=suspended_from.get(event.candidate_id),
                suspended_from=suspended_from,
                states=states,
                deployment_owners=deployment_owners,
                retired_deployments=retired_deployments,
                retired_packages=retired_packages,
                enforce_active=True,
            )
            global_sequence = len(history) + 1
            writer_sequence = writer_sequences.get(writer_pair, 0) + 1
            previous_row = connection.execute(
                "SELECT digest FROM lifecycle_events ORDER BY global_sequence DESC LIMIT 1"
            ).fetchone()
            previous_digest = ZERO_DIGEST if previous_row is None else str(previous_row[0])
            digest = _digest(previous_digest, event_bytes, evidence_bytes)
            connection.execute(
                "INSERT INTO lifecycle_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    global_sequence,
                    event.event_id,
                    *writer_pair,
                    writer_sequence,
                    event.candidate_id,
                    event_bytes,
                    evidence_bytes,
                    previous_digest,
                    digest,
                ),
            )
            connection.execute(
                "INSERT INTO lifecycle_current VALUES (?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(candidate_id) DO UPDATE SET "
                "current_state=excluded.current_state, package_hash=excluded.package_hash, "
                "deployment_identity_hash=excluded.deployment_identity_hash, "
                "last_sequence=excluded.last_sequence, source_kind=excluded.source_kind, "
                "authoritative=excluded.authoritative",
                (
                    event.candidate_id,
                    event.next_state,
                    package_hash,
                    deployment_hash,
                    global_sequence,
                    source_kind,
                    False,
                ),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        return event

    def _validated_history(
        self, connection: sqlite3.Connection
    ) -> tuple[
        list[LifecycleRecord],
        dict[str, dict[str, Any]],
        dict[tuple[str, str], int],
        dict[str, str],
        dict[str, str],
        set[str],
        dict[str, set[str]],
        dict[str, set[str]],
        dict[str, set[str]],
        dict[str, str],
        dict[str, datetime],
    ]:
        events: list[LifecycleRecord] = []
        states: dict[str, dict[str, Any]] = {}
        writer_sequences: dict[tuple[str, str], int] = {}
        prior_evaluations: dict[str, set[str]] = {}
        current_evaluations: dict[str, set[str]] = {}
        evaluation_owners: dict[str, str] = {}
        last_timestamps: dict[str, datetime] = {}
        suspended_from: dict[str, str] = {}
        deployment_owners: dict[str, str] = {}
        retired_deployments: set[str] = set()
        retired_packages: dict[str, set[str]] = {}
        previous_digest = ZERO_DIGEST
        rows = connection.execute(
            "SELECT * FROM lifecycle_events ORDER BY global_sequence"
        ).fetchall()
        for expected_sequence, row in enumerate(rows, start=1):
            if row["global_sequence"] != expected_sequence:
                raise ValueError("GLOBAL_SEQUENCE_GAP")
            event_bytes = bytes(row["canonical_event"])
            evidence_bytes = bytes(row["canonical_evidence"])
            try:
                event = LifecycleEvent.model_validate_json(event_bytes)
                evidence = json.loads(evidence_bytes)
            except Exception as exc:
                raise ValueError("INVALID_CANONICAL_PAYLOAD") from exc
            event, normalized_event_bytes = self._validated_event(event)
            if not isinstance(evidence, dict) or "check_set_purpose" not in evidence:
                raise ValueError("CHECK_SET_PURPOSE_MISSING")
            if set(evidence) != {
                "check_set_purpose",
                "check_set_version",
                "evaluation_run_hash",
                "failing_checks",
                "source_kind",
            }:
                raise ValueError("INVALID_CANONICAL_PAYLOAD")
            check_set_purpose = self._check_set_purpose(event)
            if evidence["check_set_purpose"] != check_set_purpose:
                raise ValueError("CHECK_SET_PURPOSE_MISMATCH")
            try:
                normalized_evidence = self._normalize_evidence(
                    evidence["check_set_version"],
                    evidence["evaluation_run_hash"],
                    evidence["failing_checks"],
                    evidence["source_kind"],
                )
            except Exception as exc:
                raise ValueError("INVALID_CANONICAL_PAYLOAD") from exc
            if normalized_event_bytes != event_bytes or _canonical_evidence(
                check_set_purpose,
                *normalized_evidence,
            ) != evidence_bytes:
                raise ValueError("NONCANONICAL_PAYLOAD")
            if (
                row["event_id"] != event.event_id
                or row["writer_class"] != event.writer_class.value
                or row["writer_id"] != event.writer_id
                or row["candidate_id"] != event.candidate_id
            ):
                raise ValueError("INDEXED_EVENT_IDENTITY_MISMATCH")
            writer_pair = (event.writer_class.value, event.writer_id)
            next_writer_sequence = writer_sequences.get(writer_pair, 0) + 1
            if row["writer_sequence"] != next_writer_sequence:
                raise ValueError("WRITER_SEQUENCE_GAP")
            if row["previous_digest"] != previous_digest or row["digest"] != _digest(
                previous_digest, event_bytes, evidence_bytes
            ):
                raise ValueError("LEDGER_CHAIN_CHANGED")

            current = states.get(event.candidate_id)
            prior = prior_evaluations.setdefault(event.candidate_id, set())
            current_epoch = current_evaluations.setdefault(event.candidate_id, set())
            package_hash, deployment_hash = self._validate_transition(
                event,
                current,
                check_set_version=evidence["check_set_version"],
                evaluation_run_hash=evidence["evaluation_run_hash"],
                failing_checks=tuple(evidence["failing_checks"]),
                prior_evaluations=prior,
                current_evaluations=current_epoch,
                evaluation_owners=evaluation_owners,
                last_timestamp=last_timestamps.get(event.candidate_id),
                suspended_from_state=suspended_from.get(event.candidate_id),
                suspended_from=suspended_from,
                states=states,
                deployment_owners=deployment_owners,
                retired_deployments=retired_deployments,
                retired_packages=retired_packages,
                enforce_active=False,
            )
            if event.event_type == "RE_ENTRY":
                prior.update(current_epoch)
                current_epoch.clear()
            if evidence["evaluation_run_hash"] is not None:
                current_epoch.add(evidence["evaluation_run_hash"])
                evaluation_owners.setdefault(
                    evidence["evaluation_run_hash"], event.candidate_id
                )
            last_timestamps[event.candidate_id] = event.timestamp
            states[event.candidate_id] = {
                "candidate_id": event.candidate_id,
                "current_state": event.next_state,
                "package_hash": package_hash,
                "deployment_identity_hash": deployment_hash,
                "last_sequence": expected_sequence,
                "source_kind": evidence["source_kind"],
                "authoritative": False,
            }
            if deployment_hash is not None:
                deployment_owners.setdefault(deployment_hash, event.candidate_id)
            if event.event_type == "RETIRED" and deployment_hash is not None:
                retired_deployments.add(deployment_hash)
                if package_hash is not None:
                    retired_packages.setdefault(event.candidate_id, set()).add(
                        package_hash
                    )
            if event.event_type == "SUSPENDED":
                suspended_from[event.candidate_id] = event.previous_state
            elif event.event_type in {"RESUMED", "RETIRED"}:
                suspended_from.pop(event.candidate_id, None)
            writer_sequences[writer_pair] = next_writer_sequence
            previous_digest = row["digest"]
            events.append(
                LifecycleRecord(
                    event=event,
                    check_set_purpose=check_set_purpose,
                    check_set_version=evidence["check_set_version"],
                    evaluation_run_hash=evidence["evaluation_run_hash"],
                    failing_checks=tuple(evidence["failing_checks"]),
                    source_kind=evidence["source_kind"],
                )
            )
        return (
            events,
            states,
            writer_sequences,
            suspended_from,
            deployment_owners,
            retired_deployments,
            retired_packages,
            prior_evaluations,
            current_evaluations,
            evaluation_owners,
            last_timestamps,
        )

    def _verified_snapshot(
        self, connection: sqlite3.Connection
    ) -> tuple[
        list[LifecycleRecord],
        dict[str, dict[str, Any]],
        dict[tuple[str, str], int],
        dict[str, dict[str, Any]],
    ]:
        self._validate_database(connection)
        result = connection.execute("PRAGMA integrity_check").fetchone()
        if result is None or result[0] != "ok":
            raise ValueError("SQLITE_INTEGRITY_FAILURE")
        events, states, writer_sequences, _, _, _, _, _, _, _, _ = self._validated_history(
            connection
        )
        actual_view = {
            row["candidate_id"]: self._state_from_row(row)
            for row in connection.execute(
                "SELECT * FROM lifecycle_current ORDER BY candidate_id"
            )
        }
        if actual_view != states:
            raise ValueError("DERIVED_VIEW_DRIFT")
        return events, states, writer_sequences, actual_view

    def replay(self) -> list[LifecycleRecord]:
        connection = self._connect(readonly=True)
        try:
            self._validate_database(connection)
            return self._validated_history(connection)[0]
        finally:
            connection.close()

    def current_state(self, candidate_id: str) -> dict[str, Any] | None:
        if type(candidate_id) is not str or not candidate_id.strip():
            raise ValueError("CANDIDATE_ID_INVALID")
        connection = self._connect(readonly=True)
        try:
            connection.execute("BEGIN")
            _, _, _, actual_view = self._verified_snapshot(connection)
            return actual_view.get(candidate_id)
        finally:
            connection.close()

    def rebuild_current_view(self) -> None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            self._validate_database(connection)
            _, states, _, _, _, _, _, _, _, _, _ = self._validated_history(
                connection
            )
            connection.execute("DELETE FROM lifecycle_current")
            connection.executemany(
                "INSERT INTO lifecycle_current VALUES "
                "(:candidate_id, :current_state, :package_hash, "
                ":deployment_identity_hash, :last_sequence, :source_kind, "
                ":authoritative)",
                states.values(),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def verify_integrity(
        self,
        expected_event_ids: Iterable[str] = (),
        expected_writer_sequences: Mapping[tuple[str, str], int] | None = None,
    ) -> None:
        if isinstance(expected_event_ids, (str, bytes, bytearray)):
            raise ValueError("EXPECTED_EVENT_ID_INVALID")
        try:
            expected_ids = tuple(expected_event_ids)
        except TypeError:
            raise ValueError("EXPECTED_EVENT_ID_INVALID") from None
        if any(type(event_id) is not str or not event_id.strip() for event_id in expected_ids):
            raise ValueError("EXPECTED_EVENT_ID_INVALID")
        if expected_writer_sequences is None:
            checkpoints = ()
        elif not isinstance(expected_writer_sequences, Mapping):
            raise ValueError("WRITER_CHECKPOINT_INVALID")
        else:
            try:
                checkpoint_items = tuple(expected_writer_sequences.items())
            except Exception:
                raise ValueError("WRITER_CHECKPOINT_INVALID") from None
            checkpoints = []
            for item in checkpoint_items:
                try:
                    writer_pair, expected = item
                except Exception:
                    raise ValueError("WRITER_CHECKPOINT_INVALID") from None
                checkpoints.append((writer_pair, expected))
            checkpoints = tuple(checkpoints)
        connection = self._connect(readonly=True)
        try:
            connection.execute("BEGIN")
            events, _, writer_sequences, _ = self._verified_snapshot(connection)
            actual_ids = {event.event_id for event in events}
            missing = set(expected_ids) - actual_ids
            if missing:
                raise ValueError("EXPECTED_EVENT_MISSING: " + ",".join(sorted(missing)))
            for writer_pair, expected in checkpoints:
                if type(expected) is not int or expected < 0:
                    raise ValueError("WRITER_CHECKPOINT_INVALID")
                normalized = _validated_writer_pair(
                    writer_pair, "WRITER_CHECKPOINT_INVALID"
                )
                if writer_sequences.get(normalized, 0) < expected:
                    raise ValueError("WRITER_CHECKPOINT_GAP")
        finally:
            connection.close()

    def backup_to(self, destination: str | Path) -> Path:
        destination = Path(destination)
        if self.path.is_symlink():
            raise ValueError("BACKUP_SOURCE_SYMLINK")
        if destination.exists() or destination.is_symlink():
            raise FileExistsError("BACKUP_DESTINATION_EXISTS_OR_SYMLINK")
        source = self._connect(readonly=True)
        target: sqlite3.Connection | None = None
        temporary: Path | None = None
        try:
            source.execute("BEGIN")
            self._verified_snapshot(source)
            descriptor, temporary_name = tempfile.mkstemp(
                dir=destination.parent,
                prefix=f".{destination.name}.",
                suffix=".tmp",
            )
            os.close(descriptor)
            temporary = Path(temporary_name)
            target = sqlite3.connect(temporary)
            source.backup(target)
            target.close()
            target = None
            restored = LifecycleLedger(
                temporary, self.writer_allowlist, active_check_sets=self.active_check_sets
            )
            restored.verify_integrity()
            os.link(temporary, destination)
        finally:
            if target is not None:
                target.close()
            source.close()
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        return destination

    @classmethod
    def restore_from(
        cls,
        source: str | Path,
        destination: str | Path,
        writer_allowlist: Iterable[tuple[str | LifecycleWriterClass, str]] | None,
        active_check_sets: Mapping[str, Iterable[str]] | None = None,
    ) -> LifecycleLedger:
        source = Path(source)
        destination = Path(destination)
        if not source.is_file() or source.is_symlink():
            raise ValueError("RESTORE_SOURCE_INVALID")
        if destination.exists() or destination.is_symlink():
            raise FileExistsError("RESTORE_DESTINATION_EXISTS_OR_SYMLINK")
        source_ledger = cls(
            source, writer_allowlist, active_check_sets=active_check_sets
        )
        source_ledger.backup_to(destination)
        return cls(destination, writer_allowlist, active_check_sets=active_check_sets)

    def render_status_report(self) -> str:
        connection = self._connect(readonly=True)
        try:
            connection.execute("BEGIN")
            self._validate_database(connection)
            rows = connection.execute(
                "SELECT canonical_event, canonical_evidence FROM lifecycle_events "
                "ORDER BY candidate_id, global_sequence"
            ).fetchall()
            result = connection.execute("PRAGMA integrity_check").fetchone()
            if result is None or result[0] != "ok":
                raise ValueError("SQLITE_INTEGRITY_FAILURE")
            _, states, _, _, _, _, _, _, _, _, _ = self._validated_history(
                connection
            )
            actual_view = {
                row["candidate_id"]: self._state_from_row(row)
                for row in connection.execute(
                    "SELECT * FROM lifecycle_current ORDER BY candidate_id"
                )
            }
            if actual_view != states:
                raise ValueError("DERIVED_VIEW_DRIFT")
            derived_current_state = [states[key] for key in sorted(states)]
            return _render_status_report(rows, derived_current_state)
        finally:
            connection.close()


class Registrar:
    """Research-funnel writer constrained to the ledger's common append route."""

    def __init__(self, ledger: LifecycleLedger, writer_id: str) -> None:
        if type(writer_id) is not str or not writer_id.strip():
            raise ValueError("REGISTRAR_AUTHORITY_REFUSED")
        self.ledger = ledger
        self.writer_id = writer_id

    def append(self, event: LifecycleEvent, **evidence: Any) -> LifecycleEvent:
        if not isinstance(event, LifecycleEvent):
            raise TypeError("LIFECYCLE_EVENT_REQUIRED")
        ledger = self.ledger
        writer_id = self.writer_id
        if type(writer_id) is not str or not writer_id.strip():
            raise ValueError("REGISTRAR_AUTHORITY_REFUSED")
        event, _ = ledger._validated_event(event)
        event_writer_class = event.writer_class
        event_writer_id = event.writer_id
        if (
            type(event_writer_id) is not str
            or not event_writer_id.strip()
            or event_writer_class is not LifecycleWriterClass.REGISTRAR
            or event_writer_id != writer_id
        ):
            raise ValueError("REGISTRAR_AUTHORITY_REFUSED")
        return ledger.append(event, **evidence)


def _render_status_report(
    rows: Sequence[sqlite3.Row], derived_current_state: Sequence[Mapping[str, Any]]
) -> str:
    fixture_records = []
    for row in rows:
        event = json.loads(bytes(row["canonical_event"]))
        evidence = json.loads(bytes(row["canonical_evidence"]))
        fixture_records.append(
            {
                "event_id": event["event_id"],
                "event_type": event["event_type"],
                "candidate_id": event["candidate_id"],
                "source_kind": evidence["source_kind"],
                "writer_authority": event["writer_class"],
                "writer_id": event["writer_id"],
                "previous_state": event["previous_state"],
                "next_state": event["next_state"],
                "reason": event["reason"],
                "trigger": event["trigger"],
                "package_hash": event["package_hash"],
                "deployment_identity_hash": event["deployment_identity_hash"],
                "check_set_purpose": evidence["check_set_purpose"],
                "check_set_version": evidence["check_set_version"],
                "evaluation_run_hash": evidence["evaluation_run_hash"],
                "failing_checks": evidence["failing_checks"],
                "evidence_references": event["evidence_references"],
                "timestamp": event["timestamp"],
                "authoritative": False,
            }
        )
    report = {
        "scope": "FIXTURE LEDGER DATA",
        "actual_legacy_data": "ACTUAL/LEGACY DATA: NOT INCLUDED",
        "fixture_ledger_records": fixture_records,
        "derived_current_state": list(derived_current_state),
        "authoritative_ledger_records": [],
        "legacy_mapping": "UNKNOWN",
        "unresolved_dependencies": [
            "WP-P0-04 ACCEPTANCE: UNRESOLVED",
            "WP-P0-13 ACCEPTANCE: UNRESOLVED",
            "WORTHINESS CHECK-SET: INACTIVE",
        ],
        "assurance_limits": [
            "internal hashes do not independently prove omission-free history",
            "missing events require external expected-event/writer checkpoints",
        ],
        "unresolved_lifecycle_contracts": [
            "DEMOTED TARGET RUNG MAPPING: UNRESOLVED",
            "CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING",
            "ATOMIC SUCCESSION PROMOTED ACROSS TWO CANDIDATES: UNRESOLVED",
            "REJECTED FAILED-GATE PURPOSE: UNRESOLVED",
            "ADMISSION WITHHELD CAPACITY TARGET: UNRESOLVED",
            "DEPLOYMENT REFRESH ENVELOPE: UNRESOLVED",
            "EVALUATION RUN CANDIDATE SCOPE: UNRESOLVED",
        ],
    }
    return json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Read a P0-31 lifecycle ledger")
    subparsers = parser.add_subparsers(dest="command", required=True)
    report = subparsers.add_parser("report", help="render the read-only status report")
    report.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    if args.command == "report":
        connection = sqlite3.connect(args.path.resolve().as_uri() + "?mode=ro", uri=True)
        try:
            writer_allowlist = {
                (row[0], row[1])
                for row in connection.execute(
                    "SELECT DISTINCT writer_class, writer_id FROM lifecycle_events"
                )
            }
        finally:
            connection.close()
        if not writer_allowlist:
            writer_allowlist = {("REGISTRAR", "__read_only_report__")}
        ledger = LifecycleLedger(args.path, writer_allowlist)
        print(ledger.render_status_report())
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
