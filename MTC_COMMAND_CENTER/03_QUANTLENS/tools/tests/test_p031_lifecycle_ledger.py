"""Public-seam tests for the P0-31 Milestone 1 lifecycle ledger."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import pickle
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta, timezone, tzinfo
from pathlib import Path
from threading import Event, Thread
from typing import Any, Mapping
from unittest.mock import patch


TOOLS_DIR = Path(__file__).resolve().parents[1]
CONTRACTS_DIR = Path(__file__).resolve().parents[3] / "contracts"
MODULE_PATH = TOOLS_DIR / "p031_lifecycle_ledger.py"
for search_path in (TOOLS_DIR, CONTRACTS_DIR):
    if str(search_path) not in sys.path:
        sys.path.insert(0, str(search_path))

from mtc_contracts.execution import LifecycleEvent, LifecycleWriterClass
from p031_lifecycle_ledger import LifecycleLedger, LifecycleRecord, Registrar


SCHEMA_VERSION = "p031.lifecycle-ledger.v1"
CANDIDATE_A = "QLC-20260912-a1b2c3d4"
CANDIDATE_B = "QLC-20260912-b2c3d4e5"
PACKAGE_A = "1" * 64
PACKAGE_B = "2" * 64
DEPLOYMENT_A = "3" * 64
DEPLOYMENT_B = "4" * 64
EVALUATION_A = "5" * 64
EVALUATION_B = "6" * 64
BASE_TIME = datetime(2026, 9, 12, 8, 30, tzinfo=UTC)
FAILING_CHECKS = (
    {"check_id": "DSR", "observed_value": 0.42, "threshold": ">=0.95"},
    {"check_id": "BH_FDR", "observed_value": 0.18, "threshold": "<=0.05"},
)
REENTRY_TRIGGERS = (
    "NEW_DATA_REGIME",
    "NEW_KERNEL_VERSION",
    "NEW_SUBSTITUTE_CATALOGUE",
    "NEW_ENRICHMENT_MODULES",
    "OWNER_CURIOSITY",
)
ALLOWLIST = frozenset(
    {
        ("REGISTRAR", "registrar-1"),
        ("REGISTRAR", "registrar-2"),
        ("ENVIRONMENT_ADMISSION_AUTHORITY", "admission-1"),
        ("PROMOTION_AUTHORITY", "promotion-1"),
        ("MULTI_WORKER_SUPERVISOR", "supervisor-1"),
    }
)
ACTIVE_CHECK_SETS = {
    "worthiness": ("worthiness.v1",),
    "shadow_eligibility": ("shadow-eligibility.v1",),
    "paper_eligibility": ("paper-eligibility.v1",),
    "testnet_live_candidate_eligibility": ("testnet-eligibility.v1",),
    "live_candidate_eligibility": ("live-candidate-eligibility.v1",),
    "promotion": ("promotion.v1",),
    "supervisor": ("supervisor.v1",),
}


def event(**overrides: Any) -> LifecycleEvent:
    """Build a valid fixed fixture; expected values are specification literals."""

    values: dict[str, Any] = {
        "event_id": "event-captured-a",
        "event_type": "CAPTURED",
        "writer_id": "registrar-1",
        "writer_class": "REGISTRAR",
        "previous_state": None,
        "next_state": "CAPTURED",
        "candidate_id": CANDIDATE_A,
        "package_hash": None,
        "deployment_identity_hash": None,
        "reason": "initial fixture capture",
        "trigger": None,
        "evidence_references": ("fixture://capture/a",),
        "timestamp": BASE_TIME,
    }
    values.update(overrides)
    return LifecycleEvent(**values)


def observed_state(value: Any) -> str:
    """Read the state exposed by a public return value without fixing its container."""

    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        for name in ("current_state", "next_state", "state"):
            if name in value:
                return str(value[name])
        if "event" in value:
            return observed_state(value["event"])
    for name in ("current_state", "next_state", "state"):
        if hasattr(value, name):
            return str(getattr(value, name))
    if hasattr(value, "event"):
        return observed_state(value.event)
    raise AssertionError(f"public state result has no state field: {value!r}")


def public_field(value: Any, name: str) -> Any:
    """Read an explicit public field from a record or its event envelope."""

    if isinstance(value, Mapping):
        if name in value:
            return value[name]
        if "event" in value:
            return public_field(value["event"], name)
    if hasattr(value, name):
        return getattr(value, name)
    if hasattr(value, "event"):
        return public_field(value.event, name)
    raise AssertionError(f"public record has no {name!r} field: {value!r}")


def sqlite_relation_with_columns(path: Path, required: set[str]) -> str:
    """Locate a persisted relation for an external storage-boundary attack test."""

    connection = sqlite3.connect(path)
    try:
        rows = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        for (name,) in rows:
            quoted = name.replace('"', '""')
            columns = {
                row[1]
                for row in connection.execute(f'PRAGMA table_info("{quoted}")')
            }
            if required <= columns:
                return name
    finally:
        connection.close()
    raise AssertionError(f"no SQLite relation exposes required columns {required!r}")


class LifecycleLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = Path(self.temp_dir.name) / "lifecycle.sqlite"
        self.ledger = LifecycleLedger(
            self.db_path,
            ALLOWLIST,
            active_check_sets=ACTIVE_CHECK_SETS,
        )
        self.registrar = Registrar(self.ledger, "registrar-1")

    def append_capture(
        self,
        *,
        candidate_id: str = CANDIDATE_A,
        event_id: str = "event-captured-a",
        writer_id: str = "registrar-1",
        timestamp: datetime = BASE_TIME,
    ) -> LifecycleEvent:
        captured = event(
            event_id=event_id,
            writer_id=writer_id,
            candidate_id=candidate_id,
            timestamp=timestamp,
            evidence_references=(f"fixture://capture/{candidate_id}",),
        )
        Registrar(self.ledger, writer_id).append(captured)
        return captured

    def append_to_candidate(self, candidate_id: str = CANDIDATE_A) -> None:
        self.append_capture(candidate_id=candidate_id)
        self.registrar.append(
            event(
                event_id=f"event-triaged-{candidate_id}",
                event_type="TRIAGED",
                previous_state="CAPTURED",
                next_state="TRIAGED",
                candidate_id=candidate_id,
                reason="ratified worthiness checks passed",
                evidence_references=("fixture://worthiness/a",),
                timestamp=BASE_TIME + timedelta(seconds=1),
            ),
            check_set_version="worthiness.v1",
        )
        self.registrar.append(
            event(
                event_id=f"event-candidate-{candidate_id}",
                event_type="CANDIDATE",
                previous_state="TRIAGED",
                next_state="CANDIDATE",
                candidate_id=candidate_id,
                reason="rules extracted into a candidate",
                evidence_references=("fixture://candidate/a",),
                timestamp=BASE_TIME + timedelta(seconds=2),
            )
        )

    def append_to_frozen(self, candidate_id: str = CANDIDATE_A) -> None:
        self.append_to_candidate(candidate_id)
        self.registrar.append(
            event(
                event_id=f"event-frozen-{candidate_id}",
                event_type="FROZEN",
                previous_state="CANDIDATE",
                next_state="FROZEN",
                candidate_id=candidate_id,
                package_hash=PACKAGE_A,
                reason="fixture package frozen",
                evidence_references=("fixture://package/1",),
                timestamp=BASE_TIME + timedelta(seconds=3),
            )
        )

    def new_ledger(
        self,
        name: str,
        *,
        accepted_evaluation_catalog: tuple[str, ...] | None = None,
    ) -> LifecycleLedger:
        return LifecycleLedger(
            Path(self.temp_dir.name) / f"{name}.sqlite",
            ALLOWLIST,
            active_check_sets=ACTIVE_CHECK_SETS,
            accepted_evaluation_catalog=accepted_evaluation_catalog,
        )

    def append_candidate_fixture(
        self, ledger: LifecycleLedger, candidate_id: str, prefix: str
    ) -> None:
        registrar = Registrar(ledger, "registrar-1")
        registrar.append(
            event(
                event_id=f"{prefix}-captured",
                candidate_id=candidate_id,
                evidence_references=(f"fixture://{prefix}/capture",),
            )
        )
        registrar.append(
            event(
                event_id=f"{prefix}-triaged",
                event_type="TRIAGED",
                previous_state="CAPTURED",
                next_state="TRIAGED",
                candidate_id=candidate_id,
                evidence_references=(f"fixture://{prefix}/triage",),
                timestamp=BASE_TIME + timedelta(seconds=1),
            ),
            check_set_version="worthiness.v1",
        )
        registrar.append(
            event(
                event_id=f"{prefix}-candidate",
                event_type="CANDIDATE",
                previous_state="TRIAGED",
                next_state="CANDIDATE",
                candidate_id=candidate_id,
                evidence_references=(f"fixture://{prefix}/candidate",),
                timestamp=BASE_TIME + timedelta(seconds=2),
            )
        )

    def append_frozen_fixture(
        self,
        ledger: LifecycleLedger,
        candidate_id: str,
        prefix: str,
        *,
        package_hash: str = PACKAGE_A,
    ) -> None:
        self.append_candidate_fixture(ledger, candidate_id, prefix)
        registrar = Registrar(ledger, "registrar-1")
        registrar.append(
            event(
                event_id=f"{prefix}-frozen",
                event_type="FROZEN",
                previous_state="CANDIDATE",
                next_state="FROZEN",
                candidate_id=candidate_id,
                package_hash=package_hash,
                evidence_references=(f"fixture://{prefix}/frozen",),
                timestamp=BASE_TIME + timedelta(seconds=3),
            )
        )

    def append_authority_event(
        self,
        ledger: LifecycleLedger,
        *,
        candidate_id: str,
        event_id: str,
        event_type: str,
        previous_state: str,
        next_state: str,
        writer_class: str,
        writer_id: str,
        check_set_version: str,
        package_hash: str = PACKAGE_A,
        deployment_identity_hash: str = DEPLOYMENT_A,
        offset: int = 4,
        evaluation_run_hash: str | None = None,
        failing_checks: tuple[dict[str, Any], ...] = (),
        check_set_purpose: str | None = None,
        catalog_backed: bool = False,
    ) -> None:
        ledger.append(
            event(
                event_id=event_id,
                event_type=event_type,
                writer_id=writer_id,
                writer_class=writer_class,
                previous_state=previous_state,
                next_state=next_state,
                candidate_id=candidate_id,
                package_hash=package_hash,
                deployment_identity_hash=deployment_identity_hash,
                reason=f"fixed {event_type.lower()} matrix fixture",
                evidence_references=(f"fixture://matrix/{event_id}",),
                timestamp=BASE_TIME + timedelta(seconds=offset),
            ),
            check_set_version=check_set_version,
            evaluation_run_hash=evaluation_run_hash
            or hashlib.sha256(event_id.encode()).hexdigest(),
            failing_checks=failing_checks,
            check_set_purpose=check_set_purpose,
            catalog_backed=catalog_backed,
        )

    def build_to_rung(
        self,
        ledger: LifecycleLedger,
        candidate_id: str,
        prefix: str,
        rung: str,
        *,
        include_paper: bool = False,
        package_hash: str = PACKAGE_A,
        deployment_identity_hash: str = DEPLOYMENT_A,
    ) -> None:
        self.append_frozen_fixture(
            ledger, candidate_id, prefix, package_hash=package_hash
        )
        current = "FROZEN"
        ordered = [("SHADOW_ELIGIBLE", "SHADOW")]
        if include_paper or rung == "PAPER_ELIGIBLE":
            ordered.append(("PAPER_ELIGIBLE", "SHADOW"))
        if rung in {"TESTNET_ELIGIBLE", "LIVE_CANDIDATE", "PROMOTED"}:
            ordered.append(("TESTNET_ELIGIBLE", "TESTNET"))
        if rung in {"LIVE_CANDIDATE", "PROMOTED"}:
            ordered.append(("LIVE_CANDIDATE", "LIVE_CANDIDATE"))
        if rung == "PROMOTED":
            ordered.append(("PROMOTED", "LIVE"))
        for offset, (event_type, next_state) in enumerate(ordered, start=4):
            if event_type == "PROMOTED":
                writer_class = "PROMOTION_AUTHORITY"
                writer_id = "promotion-1"
                check_set = "promotion.v1"
            else:
                writer_class = "ENVIRONMENT_ADMISSION_AUTHORITY"
                writer_id = "admission-1"
                check_set = {
                    "SHADOW_ELIGIBLE": "shadow-eligibility.v1",
                    "PAPER_ELIGIBLE": "paper-eligibility.v1",
                    "TESTNET_ELIGIBLE": "testnet-eligibility.v1",
                    "LIVE_CANDIDATE": "live-candidate-eligibility.v1",
                }[event_type]
            self.append_authority_event(
                ledger,
                candidate_id=candidate_id,
                event_id=f"{prefix}-{event_type.lower()}",
                event_type=event_type,
                previous_state=current,
                next_state=next_state,
                writer_class=writer_class,
                writer_id=writer_id,
                check_set_version=check_set,
                package_hash=package_hash,
                deployment_identity_hash=deployment_identity_hash,
                offset=offset,
            )
            current = next_state

    def inject_live_candidate_history(
        self,
        ledger: LifecycleLedger,
        candidate_id: str,
        event_id: str,
        *,
        include_purpose: bool,
        purpose: str = "testnet_live_candidate_eligibility",
        package_hash: str = PACKAGE_A,
        deployment_identity_hash: str = DEPLOYMENT_A,
    ) -> None:
        historic_event = event(
            event_id=event_id,
            event_type="LIVE_CANDIDATE",
            writer_id="admission-1",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            previous_state="TESTNET",
            next_state="LIVE_CANDIDATE",
            candidate_id=candidate_id,
            package_hash=package_hash,
            deployment_identity_hash=deployment_identity_hash,
            timestamp=BASE_TIME + timedelta(seconds=6),
        )
        event_bytes = json.dumps(
            historic_event.model_dump(mode="json"),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        evidence = {
            "check_set_version": "testnet-eligibility.v1",
            "evaluation_run_hash": EVALUATION_A,
            "failing_checks": [],
            "catalog_backed": False,
            "source_kind": "FIXTURE",
        }
        if include_purpose:
            evidence["check_set_purpose"] = purpose
        evidence_bytes = json.dumps(
            evidence,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

        connection = sqlite3.connect(ledger.path)
        try:
            sequence = connection.execute(
                "SELECT COALESCE(MAX(global_sequence), 0) + 1 FROM lifecycle_events"
            ).fetchone()[0]
            writer_sequence = connection.execute(
                "SELECT COALESCE(MAX(writer_sequence), 0) + 1 FROM lifecycle_events "
                "WHERE writer_class = ? AND writer_id = ?",
                ("ENVIRONMENT_ADMISSION_AUTHORITY", "admission-1"),
            ).fetchone()[0]
            previous_digest = connection.execute(
                "SELECT digest FROM lifecycle_events "
                "ORDER BY global_sequence DESC LIMIT 1"
            ).fetchone()[0]
            digest = hashlib.sha256(
                previous_digest.encode("ascii")
                + b"\n"
                + event_bytes
                + b"\n"
                + evidence_bytes
            ).hexdigest()
            connection.execute(
                "INSERT INTO lifecycle_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    sequence,
                    historic_event.event_id,
                    historic_event.writer_class.value,
                    historic_event.writer_id,
                    writer_sequence,
                    historic_event.candidate_id,
                    event_bytes,
                    evidence_bytes,
                    previous_digest,
                    digest,
                ),
            )
            connection.execute(
                "UPDATE lifecycle_current SET current_state = ?, last_sequence = ? "
                "WHERE candidate_id = ?",
                (historic_event.next_state, sequence, candidate_id),
            )
            connection.commit()
        finally:
            connection.close()

    def test_default_and_empty_writer_allowlists_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            default_path = Path(temp_dir) / "default.sqlite"
            empty_path = Path(temp_dir) / "empty.sqlite"
            with self.assertRaises(ValueError):
                LifecycleLedger(default_path)
            with self.assertRaises(ValueError):
                LifecycleLedger(empty_path, ())

    def test_initial_capture_is_replayable_and_current(self) -> None:
        self.append_capture()

        replayed = self.ledger.replay()

        self.assertEqual(len(replayed), 1)
        self.assertEqual(observed_state(replayed[0]), "CAPTURED")
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "CAPTURED")
        self.assertEqual(self.ledger.replay(), replayed)

    def test_unknown_candidate_has_no_derived_state(self) -> None:
        self.assertIsNone(self.ledger.current_state("QLC-20260912-never-seen"))

    def test_exact_writer_pair_must_be_allowlisted(self) -> None:
        unauthorized = event(writer_id="registrar-impostor")

        with self.assertRaises(ValueError):
            self.ledger.append(unauthorized)

        self.assertEqual(self.ledger.replay(), [])

    def test_early_build_refuses_every_non_fixture_source_kind(self) -> None:
        for source_kind in ("ACTUAL", "LEGACY", "AUTHORITATIVE", "fixture"):
            with self.subTest(source_kind=source_kind):
                with self.assertRaises(ValueError):
                    self.ledger.append(event(), source_kind=source_kind)

        self.assertEqual(self.ledger.replay(), [])

    def test_append_refuses_empty_evidence_references(self) -> None:
        without_provenance = event(evidence_references=())

        with self.assertRaises(ValueError):
            self.ledger.append(without_provenance)

        self.assertEqual(self.ledger.replay(), [])

    def test_registrar_rejects_non_registrar_event(self) -> None:
        wrong_authority = event(
            writer_id="admission-1",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            event_type="SHADOW_ELIGIBLE",
            next_state="SHADOW_ELIGIBLE",
            package_hash=PACKAGE_A,
            deployment_identity_hash=DEPLOYMENT_A,
        )

        with self.assertRaises(ValueError):
            self.registrar.append(wrong_authority)

        self.assertEqual(self.ledger.replay(), [])

    def test_captured_to_triaged_requires_an_active_exact_check_set(self) -> None:
        self.append_capture()
        triaged = event(
            event_id="event-triaged-a",
            event_type="TRIAGED",
            previous_state="CAPTURED",
            next_state="TRIAGED",
            reason="worthiness checks passed",
            timestamp=BASE_TIME + timedelta(seconds=1),
        )

        with self.assertRaises(ValueError):
            self.registrar.append(triaged)
        with self.assertRaises(ValueError):
            self.registrar.append(triaged, check_set_version="worthiness.v0.1-draft")

        self.registrar.append(triaged, check_set_version="worthiness.v1")
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "TRIAGED")

    def test_each_permitted_funnel_terminal_is_replayable(self) -> None:
        terminal_cases = (
            ("FROZEN", PACKAGE_A),
            ("PARKED", None),
        )
        for index, (state, package_hash) in enumerate(
            terminal_cases, start=1
        ):
            with self.subTest(state=state):
                candidate_id = f"QLC-20260912-terminal-{index}"
                capture_time = BASE_TIME + timedelta(minutes=index)
                self.append_capture(
                    candidate_id=candidate_id,
                    event_id=f"event-captured-terminal-{index}",
                    timestamp=capture_time,
                )
                registrar = Registrar(self.ledger, "registrar-1")
                registrar.append(
                    event(
                        event_id=f"event-triaged-terminal-{index}",
                        event_type="TRIAGED",
                        previous_state="CAPTURED",
                        next_state="TRIAGED",
                        candidate_id=candidate_id,
                        timestamp=capture_time + timedelta(seconds=1),
                    ),
                    check_set_version="worthiness.v1",
                )
                registrar.append(
                    event(
                        event_id=f"event-candidate-terminal-{index}",
                        event_type="CANDIDATE",
                        previous_state="TRIAGED",
                        next_state="CANDIDATE",
                        candidate_id=candidate_id,
                        timestamp=capture_time + timedelta(seconds=2),
                    )
                )
                registrar.append(
                    event(
                        event_id=f"event-{state.lower()}-{index}",
                        event_type=state,
                        previous_state="CANDIDATE",
                        next_state=state,
                        candidate_id=candidate_id,
                        package_hash=package_hash,
                        timestamp=capture_time + timedelta(seconds=3),
                    ),
                )
                self.assertEqual(
                    observed_state(self.ledger.current_state(candidate_id)), state
                )

    def test_triage_may_end_declined(self) -> None:
        self.append_capture()
        self.registrar.append(
            event(
                event_id="event-declined-a",
                event_type="DECLINED",
                previous_state="CAPTURED",
                next_state="DECLINED",
                reason="mechanism absent from fixture",
                timestamp=BASE_TIME + timedelta(seconds=1),
            ),
            check_set_version="worthiness.v1",
        )
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "DECLINED")

    def test_illegal_transition_does_not_change_current_state(self) -> None:
        self.append_capture()
        illegal = event(
            event_id="event-illegal-a",
            event_type="FROZEN",
            previous_state="CAPTURED",
            next_state="FROZEN",
            package_hash=PACKAGE_A,
            timestamp=BASE_TIME + timedelta(seconds=1),
        )

        with self.assertRaises(ValueError):
            self.registrar.append(illegal)

        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "CAPTURED")
        self.assertEqual(len(self.ledger.replay()), 1)

    def test_previous_state_must_match_derived_current_state(self) -> None:
        self.append_capture()
        stale = event(
            event_id="event-stale-a",
            event_type="CANDIDATE",
            previous_state="TRIAGED",
            next_state="CANDIDATE",
            timestamp=BASE_TIME + timedelta(seconds=1),
        )

        with self.assertRaises(ValueError):
            self.registrar.append(stale)

        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "CAPTURED")

    def test_duplicate_and_conflicting_event_ids_have_distinct_refusals(self) -> None:
        original = self.append_capture()

        with self.assertRaisesRegex(ValueError, "DUPLICATE_EVENT"):
            self.registrar.append(original)
        with self.assertRaisesRegex(ValueError, "CONFLICTING_EVENT"):
            self.registrar.append(
                event(reason="same id but different canonical event bytes")
            )

        self.assertEqual(len(self.ledger.replay()), 1)

    def test_rejected_requires_purpose_hash_and_failing_checks(self) -> None:
        self.append_to_candidate()
        rejected = event(
            event_id="event-rejected-a",
            event_type="REJECTED",
            previous_state="CANDIDATE",
            next_state="REJECTED",
            timestamp=BASE_TIME + timedelta(seconds=3),
        )

        refusal_shapes = (
            {
                "error": "CHECK_SET_PURPOSE_REQUIRED",
                "check_set_version": None,
                "evaluation_run_hash": EVALUATION_A,
                "failing_checks": FAILING_CHECKS,
            },
            {
                "error": "EVALUATION_RUN_HASH_REQUIRED",
                "check_set_version": "worthiness.v1",
                "evaluation_run_hash": None,
                "failing_checks": FAILING_CHECKS,
                "check_set_purpose": "worthiness",
            },
            {
                "error": "FAILING_CHECKS_REQUIRED",
                "check_set_version": "worthiness.v1",
                "evaluation_run_hash": EVALUATION_A,
                "failing_checks": (),
                "check_set_purpose": "worthiness",
            },
        )
        for evidence in refusal_shapes:
            error = evidence.pop("error")
            with self.subTest(evidence=evidence):
                with self.assertRaisesRegex(ValueError, error):
                    self.registrar.append(rejected, **evidence)

        with self.assertRaisesRegex(ValueError, "CHECK_SET_PURPOSE_MISMATCH"):
            self.registrar.append(
                rejected,
                check_set_version="promotion.v1",
                evaluation_run_hash=EVALUATION_A,
                failing_checks=FAILING_CHECKS,
                check_set_purpose="promotion",
            )

        self.registrar.append(
            rejected,
            check_set_version="worthiness.v1",
            evaluation_run_hash=EVALUATION_A,
            failing_checks=FAILING_CHECKS,
            check_set_purpose="worthiness",
        )
        replayed = self.ledger.replay()[-1]
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "REJECTED")
        self.assertEqual(replayed.check_set_purpose, "worthiness")
        self.assertEqual(replayed.evaluation_run_hash, EVALUATION_A)
        self.assertEqual(replayed.failing_checks, FAILING_CHECKS)

    def test_rejected_reentry_returns_to_same_candidate(self) -> None:
        self.append_to_candidate()
        self.registrar.append(
            event(
                event_id="event-rejected-for-reentry",
                event_type="REJECTED",
                previous_state="CANDIDATE",
                next_state="REJECTED",
                timestamp=BASE_TIME + timedelta(seconds=3),
            ),
            check_set_version="worthiness.v1",
            evaluation_run_hash=EVALUATION_A,
            failing_checks=FAILING_CHECKS,
            check_set_purpose="worthiness",
        )
        self.registrar.append(
            event(
                event_id="event-rejected-reentry",
                event_type="RE_ENTRY",
                previous_state="REJECTED",
                next_state="CANDIDATE",
                trigger="NEW_DATA_REGIME",
                timestamp=BASE_TIME + timedelta(seconds=4),
            ),
            evaluation_run_hash=EVALUATION_B,
        )
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "CANDIDATE")

    def test_every_ratified_reentry_trigger_returns_to_same_candidate(self) -> None:
        for index, trigger in enumerate(REENTRY_TRIGGERS, start=1):
            with self.subTest(trigger=trigger):
                path = Path(self.temp_dir.name) / f"reentry-{index}.sqlite"
                ledger = LifecycleLedger(path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS)
                registrar = Registrar(ledger, "registrar-1")
                candidate_id = f"QLC-20260912-reentry-{index}"
                registrar.append(
                    event(
                        event_id=f"event-capture-reentry-{index}",
                        candidate_id=candidate_id,
                    )
                )
                registrar.append(
                    event(
                        event_id=f"event-declined-reentry-{index}",
                        event_type="DECLINED",
                        previous_state="CAPTURED",
                        next_state="DECLINED",
                        candidate_id=candidate_id,
                        timestamp=BASE_TIME + timedelta(seconds=1),
                    ),
                    check_set_version="worthiness.v1",
                )
                registrar.append(
                    event(
                        event_id=f"event-reentry-{index}",
                        event_type="RE_ENTRY",
                        previous_state="DECLINED",
                        next_state="CANDIDATE",
                        candidate_id=candidate_id,
                        trigger=trigger,
                        evidence_references=(f"fixture://reentry/{index}/fresh",),
                        timestamp=BASE_TIME + timedelta(seconds=2),
                    ),
                    evaluation_run_hash=EVALUATION_B,
                )
                self.assertEqual(observed_state(ledger.current_state(candidate_id)), "CANDIDATE")

    def test_reentry_rejects_unknown_trigger_and_reused_evaluation(self) -> None:
        self.append_to_candidate()
        parked = event(
            event_id="event-parked-a",
            event_type="PARKED",
            previous_state="CANDIDATE",
            next_state="PARKED",
            timestamp=BASE_TIME + timedelta(seconds=3),
        )
        self.registrar.append(parked)
        with self.assertRaisesRegex(ValueError, "REENTRY_TRIGGER_INVALID"):
            self.registrar.append(
                event(
                    event_id="event-reentry-unknown",
                    event_type="RE_ENTRY",
                    previous_state="PARKED",
                    next_state="CANDIDATE",
                    trigger="CALENDAR_ELAPSED",
                    timestamp=BASE_TIME + timedelta(seconds=4),
                ),
                evaluation_run_hash=EVALUATION_B,
            )
        self.registrar.append(
            event(
                event_id="event-reentry-valid",
                event_type="RE_ENTRY",
                previous_state="PARKED",
                next_state="CANDIDATE",
                trigger="NEW_DATA_REGIME",
                timestamp=BASE_TIME + timedelta(seconds=4),
            ),
            evaluation_run_hash=EVALUATION_A,
        )
        self.registrar.append(
            event(
                event_id="event-parked-again",
                event_type="PARKED",
                previous_state="CANDIDATE",
                next_state="PARKED",
                timestamp=BASE_TIME + timedelta(seconds=5),
            )
        )
        with self.assertRaisesRegex(ValueError, "REENTRY_EVALUATION_NOT_FRESH"):
            self.registrar.append(
                event(
                    event_id="event-reentry-reused",
                    event_type="RE_ENTRY",
                    previous_state="PARKED",
                    next_state="CANDIDATE",
                    trigger="NEW_DATA_REGIME",
                    timestamp=BASE_TIME + timedelta(seconds=6),
                ),
                evaluation_run_hash=EVALUATION_A,
            )
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "PARKED")

        with self.assertRaises(ValueError):
            self.registrar.append(
                event(
                    event_id="event-reentry-recounted",
                    event_type="RE_ENTRY",
                    previous_state="PARKED",
                    next_state="CANDIDATE",
                    trigger="NEW_DATA_REGIME",
                    evidence_references=("fixture://reentry/fresh",),
                    timestamp=BASE_TIME + timedelta(seconds=6),
                ),
                evaluation_run_hash=EVALUATION_B,
                failing_checks=FAILING_CHECKS,
            )

    def test_other_writer_classes_have_distinct_authority_and_deep_identity(self) -> None:
        self.append_to_frozen()
        ladder_events = (
            (
                "event-shadow-a",
                "SHADOW_ELIGIBLE",
                "admission-1",
                "ENVIRONMENT_ADMISSION_AUTHORITY",
                "FROZEN",
                "SHADOW",
                "shadow-eligibility.v1",
            ),
            (
                "event-testnet-a",
                "TESTNET_ELIGIBLE",
                "admission-1",
                "ENVIRONMENT_ADMISSION_AUTHORITY",
                "SHADOW",
                "TESTNET",
                "testnet-eligibility.v1",
            ),
            (
                "event-live-candidate-a",
                "LIVE_CANDIDATE",
                "admission-1",
                "ENVIRONMENT_ADMISSION_AUTHORITY",
                "TESTNET",
                "LIVE_CANDIDATE",
                "live-candidate-eligibility.v1",
            ),
            (
                "event-promoted-a",
                "PROMOTED",
                "promotion-1",
                "PROMOTION_AUTHORITY",
                "LIVE_CANDIDATE",
                "LIVE",
                "promotion.v1",
            ),
            (
                "event-suspended-a",
                "SUSPENDED",
                "supervisor-1",
                "MULTI_WORKER_SUPERVISOR",
                "LIVE",
                "SUSPENDED",
                "supervisor.v1",
            ),
        )
        for offset, row in enumerate(ladder_events, start=4):
            event_id, event_type, writer_id, writer_class, previous, next_state, check_set = row
            self.ledger.append(
                event(
                    event_id=event_id,
                    event_type=event_type,
                    writer_id=writer_id,
                    writer_class=writer_class,
                    previous_state=previous,
                    next_state=next_state,
                    package_hash=PACKAGE_A,
                    deployment_identity_hash=DEPLOYMENT_A,
                    reason=f"fixed {event_type.lower()} fixture evidence",
                    timestamp=BASE_TIME + timedelta(seconds=offset),
                ),
                check_set_version=check_set,
                evaluation_run_hash=hashlib.sha256(event_id.encode()).hexdigest(),
            )
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "SUSPENDED")

    def test_authority_cannot_issue_another_writer_class_event(self) -> None:
        self.append_to_frozen()
        registrar_ladder = event(
            event_id="event-registrar-shadow-a",
            event_type="SHADOW_ELIGIBLE",
            previous_state="FROZEN",
            next_state="SHADOW_ELIGIBLE",
            package_hash=PACKAGE_A,
            deployment_identity_hash=DEPLOYMENT_A,
            timestamp=BASE_TIME + timedelta(seconds=4),
        )
        admission_promotion = event(
            event_id="event-admission-promoted-a",
            event_type="PROMOTED",
            writer_id="admission-1",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            previous_state="FROZEN",
            next_state="PROMOTED",
            package_hash=PACKAGE_A,
            deployment_identity_hash=DEPLOYMENT_A,
            timestamp=BASE_TIME + timedelta(seconds=4),
        )

        with self.assertRaises(ValueError):
            self.registrar.append(registrar_ladder)
        with self.assertRaises(ValueError):
            self.ledger.append(
                admission_promotion,
                check_set_version="promotion.v1",
                evaluation_run_hash=EVALUATION_A,
            )
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "FROZEN")

    def test_ladder_identity_must_be_complete_and_match_frozen_package(self) -> None:
        self.append_to_frozen()
        for event_id, package_hash, deployment_hash in (
            ("event-shadow-no-package", None, DEPLOYMENT_A),
            ("event-shadow-no-deployment", PACKAGE_A, None),
            ("event-shadow-wrong-package", PACKAGE_B, DEPLOYMENT_A),
        ):
            with self.subTest(event_id=event_id):
                with self.assertRaises(ValueError):
                    self.ledger.append(
                        event(
                            event_id=event_id,
                            event_type="SHADOW_ELIGIBLE",
                            writer_id="admission-1",
                            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                            previous_state="FROZEN",
                            next_state="SHADOW",
                            package_hash=package_hash,
                            deployment_identity_hash=deployment_hash,
                            timestamp=BASE_TIME + timedelta(seconds=4),
                        ),
                        check_set_version="shadow-eligibility.v1",
                        evaluation_run_hash=EVALUATION_A,
                    )
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "FROZEN")

    def test_append_revalidates_malformed_and_naive_time_contract_objects(self) -> None:
        with self.assertRaises((TypeError, ValueError)):
            self.ledger.append({"event_id": "not-a-contract"})  # type: ignore[arg-type]

        naive_event = LifecycleEvent.model_construct(
            **event().model_dump(exclude={"timestamp"}),
            timestamp=datetime(2026, 9, 12, 8, 30),
        )
        with self.assertRaises(ValueError):
            self.ledger.append(naive_event)

        self.assertEqual(self.ledger.replay(), [])

    def test_restart_preserves_history_and_current_view(self) -> None:
        self.append_to_candidate()
        first_replay = self.ledger.replay()

        reopened = LifecycleLedger(
            self.db_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
        )

        self.assertEqual(reopened.replay(), first_replay)
        self.assertEqual(observed_state(reopened.current_state(CANDIDATE_A)), "CANDIDATE")

    def test_two_concurrent_writers_commit_complete_independent_events(self) -> None:
        candidate_ids = (CANDIDATE_A, CANDIDATE_B)

        def append_in_own_connection(index: int) -> None:
            ledger = LifecycleLedger(
                self.db_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
            )
            writer_id = f"registrar-{index + 1}"
            Registrar(ledger, writer_id).append(
                event(
                    event_id=f"event-concurrent-{index + 1}",
                    writer_id=writer_id,
                    candidate_id=candidate_ids[index],
                    timestamp=BASE_TIME + timedelta(seconds=index),
                )
            )

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(append_in_own_connection, index) for index in range(2)]
            for future in futures:
                future.result(timeout=10)

        self.assertEqual(len(self.ledger.replay()), 2)
        self.assertEqual(
            {observed_state(self.ledger.current_state(value)) for value in candidate_ids},
            {"CAPTURED"},
        )
        self.ledger.verify_integrity(
            expected_writer_sequences={
                ("REGISTRAR", "registrar-1"): 1,
                ("REGISTRAR", "registrar-2"): 1,
            }
        )

    def test_interrupted_uncommitted_view_change_is_discarded_on_restart(self) -> None:
        self.append_capture()
        view_table = sqlite_relation_with_columns(
            self.db_path, {"candidate_id", "current_state"}
        )
        quoted = view_table.replace('"', '""')
        connection = sqlite3.connect(self.db_path)
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            f'UPDATE "{quoted}" SET current_state = ? WHERE candidate_id = ?',
            ("INTERRUPTED_APPEND", CANDIDATE_A),
        )
        connection.close()

        reopened = LifecycleLedger(
            self.db_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
        )
        self.assertEqual(observed_state(reopened.current_state(CANDIDATE_A)), "CAPTURED")
        self.assertEqual(len(reopened.replay()), 1)
        reopened.verify_integrity()

    def test_rebuild_current_view_is_lossless_and_deterministic(self) -> None:
        self.append_to_frozen()
        before_replay = self.ledger.replay()
        before_state = observed_state(self.ledger.current_state(CANDIDATE_A))

        self.ledger.rebuild_current_view()
        first_rebuild = self.ledger.replay()
        self.ledger.rebuild_current_view()

        self.assertEqual(first_rebuild, before_replay)
        self.assertEqual(self.ledger.replay(), before_replay)
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), before_state)

    def test_event_history_refuses_external_update_and_delete(self) -> None:
        self.append_capture()
        event_table = sqlite_relation_with_columns(
            self.db_path, {"event_id", "canonical_event", "digest"}
        )
        quoted = event_table.replace('"', '""')

        for statement in (
            f'UPDATE "{quoted}" SET canonical_event = canonical_event WHERE event_id = ?',
            f'DELETE FROM "{quoted}" WHERE event_id = ?',
        ):
            with self.subTest(statement=statement.split()[0]):
                connection = sqlite3.connect(self.db_path)
                try:
                    with self.assertRaises(sqlite3.DatabaseError):
                        connection.execute(statement, ("event-captured-a",))
                finally:
                    connection.close()

        self.assertEqual(len(self.ledger.replay()), 1)
        self.ledger.verify_integrity()

    def test_history_has_no_public_edit_or_delete_route(self) -> None:
        self.assertFalse(hasattr(self.ledger, "update"))
        self.assertFalse(hasattr(self.ledger, "delete"))
        self.assertFalse(hasattr(self.ledger, "remove"))

    def test_integrity_detects_missing_expected_event_and_writer_checkpoint_gap(self) -> None:
        self.append_capture()
        self.ledger.verify_integrity(
            expected_event_ids=("event-captured-a",),
            expected_writer_sequences={("REGISTRAR", "registrar-1"): 1},
        )

        with self.assertRaises(ValueError):
            self.ledger.verify_integrity(expected_event_ids=("event-never-appended",))
        with self.assertRaises(ValueError):
            self.ledger.verify_integrity(
                expected_writer_sequences={("REGISTRAR", "registrar-1"): 2}
            )

    def test_integrity_detects_equal_length_edit_to_canonical_chain_bytes(self) -> None:
        self.append_capture()
        attacked_path = Path(self.temp_dir.name) / "edited-chain.sqlite"
        self.ledger.backup_to(attacked_path)
        original = b"initial fixture capture"
        replacement = b"tampered fixture captur"
        self.assertEqual(len(original), len(replacement))
        content = attacked_path.read_bytes()
        self.assertIn(original, content)
        attacked_path.write_bytes(content.replace(original, replacement, 1))

        with self.assertRaises((ValueError, sqlite3.DatabaseError)):
            attacked = LifecycleLedger(
                attacked_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
            )
            attacked.verify_integrity()

    def test_reads_fail_closed_after_equal_length_chain_edit(self) -> None:
        self.append_capture()
        attacked_path = Path(self.temp_dir.name) / "read-attacked-chain.sqlite"
        self.ledger.backup_to(attacked_path)
        original = b"initial fixture capture"
        replacement = b"tampered fixture captur"
        content = attacked_path.read_bytes()
        self.assertEqual(len(original), len(replacement))
        self.assertIn(original, content)
        attacked_path.write_bytes(content.replace(original, replacement, 1))
        attacked = LifecycleLedger(
            attacked_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
        )

        for seam, read in (
            ("current_state", lambda: attacked.current_state(CANDIDATE_A)),
            ("status_report", attacked.render_status_report),
        ):
            with self.subTest(seam=seam):
                with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                    read()

    def test_schema_version_is_fixed_and_mismatch_is_refused(self) -> None:
        self.append_capture()
        wrong_version_path = Path(self.temp_dir.name) / "wrong-version.sqlite"
        self.ledger.backup_to(wrong_version_path)
        content = wrong_version_path.read_bytes()
        expected = SCHEMA_VERSION.encode("ascii")
        wrong = b"p031.lifecycle-ledger.v0"
        self.assertEqual(len(expected), len(wrong))
        self.assertIn(expected, content)
        wrong_version_path.write_bytes(content.replace(expected, wrong, 1))

        with self.assertRaises((ValueError, sqlite3.DatabaseError)):
            LifecycleLedger(
                wrong_version_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
            )

    def test_reopen_refuses_weakened_event_uniqueness_with_valid_version_and_guards(
        self,
    ) -> None:
        self.append_capture()
        weakened_path = Path(self.temp_dir.name) / "weakened-event-uniqueness.sqlite"
        self.ledger.backup_to(weakened_path)

        connection = sqlite3.connect(weakened_path)
        try:
            connection.executescript(
                """
                DROP TRIGGER lifecycle_events_no_update;
                DROP TRIGGER lifecycle_events_no_delete;
                ALTER TABLE lifecycle_events RENAME TO lifecycle_events_original;
                CREATE TABLE lifecycle_events (
                    global_sequence INTEGER PRIMARY KEY,
                    event_id TEXT NOT NULL,
                    writer_class TEXT NOT NULL,
                    writer_id TEXT NOT NULL,
                    writer_sequence INTEGER NOT NULL,
                    candidate_id TEXT NOT NULL,
                    canonical_event BLOB NOT NULL,
                    canonical_evidence BLOB NOT NULL,
                    previous_digest TEXT NOT NULL,
                    digest TEXT NOT NULL
                );
                INSERT INTO lifecycle_events
                SELECT * FROM lifecycle_events_original;
                DROP TABLE lifecycle_events_original;
                CREATE TRIGGER lifecycle_events_no_update
                BEFORE UPDATE ON lifecycle_events
                BEGIN SELECT RAISE(ABORT, 'IMMUTABLE_EVENT_HISTORY'); END;
                CREATE TRIGGER lifecycle_events_no_delete
                BEFORE DELETE ON lifecycle_events
                BEGIN SELECT RAISE(ABORT, 'IMMUTABLE_EVENT_HISTORY'); END;
                """
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaisesRegex(ValueError, "SCHEMA|GUARD"):
            LifecycleLedger(
                weakened_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
            )

    def test_backup_restores_complete_history_and_refuses_overwrite(self) -> None:
        self.append_to_candidate()
        backup_path = Path(self.temp_dir.name) / "backup.sqlite"

        self.ledger.backup_to(backup_path)
        restored = LifecycleLedger(
            backup_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
        )

        self.assertEqual(restored.replay(), self.ledger.replay())
        self.assertEqual(observed_state(restored.current_state(CANDIDATE_A)), "CANDIDATE")
        restored.verify_integrity(expected_event_ids=(f"event-candidate-{CANDIDATE_A}",))
        with self.assertRaises((FileExistsError, ValueError)):
            self.ledger.backup_to(backup_path)

    def test_restore_from_round_trip_refuses_overwrite_and_corrupt_source(self) -> None:
        self.append_to_candidate()
        backup_path = Path(self.temp_dir.name) / "restore-source.sqlite"
        restored_path = Path(self.temp_dir.name) / "restored-new-destination.sqlite"
        self.ledger.backup_to(backup_path)

        LifecycleLedger.restore_from(
            backup_path,
            restored_path,
            ALLOWLIST,
            active_check_sets=ACTIVE_CHECK_SETS,
        )
        restored = LifecycleLedger(
            restored_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
        )

        self.assertEqual(restored.replay(), self.ledger.replay())
        restored.verify_integrity()
        with self.assertRaises((FileExistsError, ValueError)):
            LifecycleLedger.restore_from(
                backup_path,
                restored_path,
                ALLOWLIST,
                active_check_sets=ACTIVE_CHECK_SETS,
            )

        corrupt_source = Path(self.temp_dir.name) / "corrupt-restore-source.sqlite"
        corrupt_destination = Path(self.temp_dir.name) / "corrupt-restore-output.sqlite"
        content = backup_path.read_bytes()
        corrupt_source.write_bytes(b"not-a-sqlite-ledger" + content[19:])
        with self.assertRaises((ValueError, sqlite3.DatabaseError)):
            LifecycleLedger.restore_from(
                corrupt_source,
                corrupt_destination,
                ALLOWLIST,
                active_check_sets=ACTIVE_CHECK_SETS,
            )
        self.assertFalse(corrupt_destination.exists())

    def test_corrupted_backup_is_refused(self) -> None:
        self.append_capture()
        corrupt_path = Path(self.temp_dir.name) / "corrupt.sqlite"
        self.ledger.backup_to(corrupt_path)
        content = corrupt_path.read_bytes()
        corrupt_path.write_bytes(b"not-a-sqlite-ledger" + content[19:])

        with self.assertRaises((ValueError, sqlite3.DatabaseError)):
            LifecycleLedger(corrupt_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS)

    def test_backup_refuses_symlink_source_and_destination_ambiguity(self) -> None:
        self.append_capture()
        target = Path(self.temp_dir.name) / "symlink-target.sqlite"
        link = Path(self.temp_dir.name) / "symlink-destination.sqlite"
        source_link = Path(self.temp_dir.name) / "symlink-source.sqlite"
        target.write_bytes(b"sentinel")
        try:
            link.symlink_to(target)
            source_link.symlink_to(self.db_path)
        except OSError as exc:
            self.skipTest(f"file symlinks unavailable on this host: {exc}")

        with self.assertRaises((FileExistsError, ValueError)):
            self.ledger.backup_to(link)
        self.assertEqual(target.read_bytes(), b"sentinel")
        linked = LifecycleLedger(
            source_link, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
        )
        with self.assertRaises(ValueError):
            linked.backup_to(Path(self.temp_dir.name) / "symlink-source-copy.sqlite")

    def test_status_report_is_read_only_deterministic_and_provenance_first(self) -> None:
        self.append_to_frozen()
        before = self.db_path.read_bytes()

        first = self.ledger.render_status_report()
        second = self.ledger.render_status_report()

        self.assertEqual(first, second)
        self.assertEqual(self.db_path.read_bytes(), before)
        for literal in (
            CANDIDATE_A,
            "FIXTURE",
            "REGISTRAR",
            "CANDIDATE",
            "FROZEN",
            "fixture package frozen",
            PACKAGE_A,
            "fixture://package/1",
            "2026-09-12",
            "unresolved",
        ):
            with self.subTest(literal=literal):
                self.assertIn(literal, first)
        self.assertNotIn("eligible because tests passed", first.lower())
        self.assertNotIn("admitted because tests passed", first.lower())
        self.assertNotIn("live because tests passed", first.lower())

    def test_status_report_separates_fixture_scope_and_names_open_dependencies(self) -> None:
        self.append_capture()

        report = self.ledger.render_status_report()
        decoded = json.loads(report)
        upper_report = report.upper()

        for literal in (
            "FIXTURE LEDGER DATA",
            "ACTUAL/LEGACY DATA: NOT INCLUDED",
            "WP-P0-04 ACCEPTANCE: UNRESOLVED",
            "WP-P0-13 ACCEPTANCE: UNRESOLVED",
            "WORTHINESS CHECK-SET: INACTIVE",
        ):
            with self.subTest(literal=literal):
                self.assertIn(literal, upper_report)
        self.assertEqual(decoded["authoritative_ledger_records"], [])
        self.assertTrue(
            all(
                record["source_kind"] == "FIXTURE"
                for record in decoded["fixture_ledger_records"]
            )
        )
        reported_states = {
            record[field]
            for record in decoded["fixture_ledger_records"]
            for field in ("previous_state", "next_state")
        }
        self.assertTrue(
            all(
                record["writer_authority"] != "PROMOTION_AUTHORITY"
                for record in decoded["fixture_ledger_records"]
            )
        )
        for forbidden_inference in (
            "eligibility",
            "admission",
            "promotion",
            "accepted",
        ):
            with self.subTest(forbidden_inference=forbidden_inference):
                self.assertNotIn(forbidden_inference, decoded)
        self.assertIn(
            "ATOMIC SUCCESSION INTERIM REFUSAL: RATIFIED BY OD-4",
            decoded["ratified_lifecycle_contracts"],
        )
        for forbidden_record_state in (
            "SHADOW_ELIGIBLE",
            "PAPER_ELIGIBLE",
            "TESTNET_ELIGIBLE",
            "LIVE_CANDIDATE",
            "PROMOTED",
            "ADMITTED",
        ):
            with self.subTest(forbidden_record_state=forbidden_record_state):
                self.assertNotIn(forbidden_record_state, reported_states)

    def test_report_cli_is_read_only_and_matches_public_renderer(self) -> None:
        self.append_capture()
        before = self.db_path.read_bytes()

        completed = subprocess.run(
            [sys.executable, str(MODULE_PATH), "report", str(self.db_path)],
            cwd=TOOLS_DIR,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), self.ledger.render_status_report().strip())
        self.assertEqual(self.db_path.read_bytes(), before)

    def test_report_cli_emits_utf8_for_non_ansi_candidate_text(self) -> None:
        candidate_id = "QLC-20260913-\u4e2d"
        self.append_capture(
            candidate_id=candidate_id,
            event_id="report-cli-unicode-captured",
        )
        before = self.db_path.read_bytes()
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "0"
        environment["PYTHONIOENCODING"] = "cp1254:strict"

        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                "-X",
                "utf8=0",
                str(MODULE_PATH),
                "report",
                str(self.db_path),
            ],
            cwd=TOOLS_DIR,
            check=False,
            capture_output=True,
            env=environment,
        )

        self.assertEqual(
            completed.returncode,
            0,
            completed.stderr.decode("cp1254", errors="replace"),
        )
        report = json.loads(completed.stdout.decode("utf-8"))
        self.assertIn(
            candidate_id,
            [row["candidate_id"] for row in report["fixture_ledger_records"]],
        )
        self.assertEqual(self.ledger.replay()[0].candidate_id, candidate_id)
        self.ledger.verify_integrity(
            expected_event_ids=("report-cli-unicode-captured",)
        )
        self.assertEqual(self.db_path.read_bytes(), before)

    def test_append_uses_replayed_history_not_committed_current_view_drift(self) -> None:
        for mutation in ("UPDATE", "DELETE"):
            with self.subTest(mutation=mutation):
                ledger = self.new_ledger(f"current-drift-{mutation.lower()}")
                candidate_id = f"QLC-20260912-current-drift-{mutation.lower()}"
                Registrar(ledger, "registrar-1").append(
                    event(
                        event_id=f"drift-{mutation.lower()}-captured",
                        candidate_id=candidate_id,
                    )
                )
                connection = sqlite3.connect(ledger.path)
                try:
                    if mutation == "UPDATE":
                        connection.execute(
                            "UPDATE lifecycle_current SET current_state = 'TRIAGED' "
                            "WHERE candidate_id = ?",
                            (candidate_id,),
                        )
                    else:
                        connection.execute(
                            "DELETE FROM lifecycle_current WHERE candidate_id = ?",
                            (candidate_id,),
                        )
                    connection.commit()
                finally:
                    connection.close()

                with self.assertRaisesRegex(ValueError, "DERIVED_VIEW_DRIFT"):
                    Registrar(ledger, "registrar-1").append(
                        event(
                            event_id=f"drift-{mutation.lower()}-declined",
                            event_type="DECLINED",
                            previous_state="CAPTURED",
                            next_state="DECLINED",
                            candidate_id=candidate_id,
                            timestamp=BASE_TIME + timedelta(seconds=1),
                        ),
                        check_set_version="worthiness.v1",
                    )
                ledger.rebuild_current_view()
                Registrar(ledger, "registrar-1").append(
                    event(
                        event_id=f"drift-{mutation.lower()}-declined",
                        event_type="DECLINED",
                        previous_state="CAPTURED",
                        next_state="DECLINED",
                        candidate_id=candidate_id,
                        timestamp=BASE_TIME + timedelta(seconds=1),
                    ),
                    check_set_version="worthiness.v1",
                )
                self.assertEqual(observed_state(ledger.current_state(candidate_id)), "DECLINED")
                ledger.verify_integrity()

    def test_identity_depth_is_exact_before_freeze_and_through_tail(self) -> None:
        for label, package_hash, deployment_hash in (
            ("captured-package", PACKAGE_A, None),
            ("captured-deployment", None, DEPLOYMENT_A),
        ):
            with self.subTest(label=label):
                ledger = self.new_ledger(label)
                with self.assertRaises(ValueError):
                    ledger.append(
                        event(
                            event_id=label,
                            candidate_id=f"QLC-20260912-{label}",
                            package_hash=package_hash,
                            deployment_identity_hash=deployment_hash,
                        )
                    )

        frozen_ledger = self.new_ledger("frozen-deployment-refused")
        candidate_id = "QLC-20260912-frozen-deployment"
        registrar = Registrar(frozen_ledger, "registrar-1")
        registrar.append(event(event_id="freeze-depth-captured", candidate_id=candidate_id))
        registrar.append(
            event(
                event_id="freeze-depth-triaged",
                event_type="TRIAGED",
                previous_state="CAPTURED",
                next_state="TRIAGED",
                candidate_id=candidate_id,
                timestamp=BASE_TIME + timedelta(seconds=1),
            ),
            check_set_version="worthiness.v1",
        )
        registrar.append(
            event(
                event_id="freeze-depth-candidate",
                event_type="CANDIDATE",
                previous_state="TRIAGED",
                next_state="CANDIDATE",
                candidate_id=candidate_id,
                timestamp=BASE_TIME + timedelta(seconds=2),
            )
        )
        with self.assertRaises(ValueError):
            registrar.append(
                event(
                    event_id="freeze-depth-frozen",
                    event_type="FROZEN",
                    previous_state="CANDIDATE",
                    next_state="FROZEN",
                    candidate_id=candidate_id,
                    package_hash=PACKAGE_A,
                    deployment_identity_hash=DEPLOYMENT_A,
                    timestamp=BASE_TIME + timedelta(seconds=3),
                )
            )

        tail_ledger = self.new_ledger("tail-identity")
        tail_candidate = "QLC-20260912-tail-identity"
        self.build_to_rung(tail_ledger, tail_candidate, "tail-identity", "PROMOTED")
        self.append_authority_event(
            tail_ledger,
            candidate_id=tail_candidate,
            event_id="tail-identity-suspended",
            event_type="SUSPENDED",
            previous_state="LIVE",
            next_state="SUSPENDED",
            writer_class="MULTI_WORKER_SUPERVISOR",
            writer_id="supervisor-1",
            check_set_version="supervisor.v1",
            offset=9,
        )
        state = tail_ledger.current_state(tail_candidate)
        self.assertEqual(state["package_hash"], PACKAGE_A)
        self.assertEqual(state["deployment_identity_hash"], DEPLOYMENT_A)
        with self.assertRaises(ValueError):
            self.append_authority_event(
                tail_ledger,
                candidate_id=tail_candidate,
            event_id="tail-identity-mismatch",
            event_type="RESUMED",
            previous_state="SUSPENDED",
            next_state="LIVE",
                writer_class="PROMOTION_AUTHORITY",
                writer_id="promotion-1",
                check_set_version="promotion.v1",
                deployment_identity_hash=DEPLOYMENT_B,
                offset=10,
            )

    def test_duplicate_identity_includes_canonical_evidence_envelope(self) -> None:
        self.append_capture()
        triaged = event(
            event_id="envelope-triaged",
            event_type="TRIAGED",
            previous_state="CAPTURED",
            next_state="TRIAGED",
            timestamp=BASE_TIME + timedelta(seconds=1),
        )
        self.registrar.append(triaged, check_set_version="worthiness.v1")

        with self.assertRaisesRegex(ValueError, "DUPLICATE_EVENT"):
            self.registrar.append(triaged, check_set_version="worthiness.v1")
        with self.assertRaisesRegex(ValueError, "CONFLICTING_EVENT"):
            self.registrar.append(
                triaged, check_set_version="shadow-eligibility.v1"
            )

    def test_missing_or_altered_history_guard_fails_every_public_seam_closed(self) -> None:
        self.append_capture()
        mutations = {
            "missing": (
                "DROP TRIGGER lifecycle_events_no_update",
            ),
            "altered": (
                "DROP TRIGGER lifecycle_events_no_delete",
                "CREATE TRIGGER lifecycle_events_no_delete BEFORE DELETE ON "
                "lifecycle_events BEGIN SELECT 1; END",
            ),
        }
        for mutation, statements in mutations.items():
            for seam in ("reopen", "append", "verify", "backup", "report"):
                with self.subTest(mutation=mutation, seam=seam):
                    attacked_path = (
                        Path(self.temp_dir.name) / f"guard-{mutation}-{seam}.sqlite"
                    )
                    self.ledger.backup_to(attacked_path)
                    attacked = LifecycleLedger(
                        attacked_path,
                        ALLOWLIST,
                        active_check_sets=ACTIVE_CHECK_SETS,
                    )
                    connection = sqlite3.connect(attacked_path)
                    try:
                        for statement in statements:
                            connection.execute(statement)
                        connection.commit()
                    finally:
                        connection.close()

                    if seam == "reopen":
                        read = lambda: LifecycleLedger(
                            attacked_path,
                            ALLOWLIST,
                            active_check_sets=ACTIVE_CHECK_SETS,
                        )
                    elif seam == "append":
                        read = lambda: attacked.append(
                            event(
                                event_id=f"guard-{mutation}-append",
                                candidate_id=f"QLC-20260912-guard-{mutation}",
                            )
                        )
                    elif seam == "verify":
                        read = attacked.verify_integrity
                    elif seam == "backup":
                        destination = (
                            Path(self.temp_dir.name)
                            / f"guard-{mutation}-{seam}-copy.sqlite"
                        )
                        read = lambda: attacked.backup_to(destination)
                    else:
                        read = attacked.render_status_report
                    with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                        read()

    def test_unexpected_ignore_insert_trigger_fails_closed_before_state_mutation(
        self,
    ) -> None:
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                "CREATE TRIGGER unexpected_ignore_insert "
                "BEFORE INSERT ON lifecycle_events "
                "BEGIN SELECT RAISE(IGNORE); END"
            )
            connection.commit()
        finally:
            connection.close()

        append_refused = False
        try:
            self.registrar.append(event(event_id="unexpected-trigger-captured"))
        except (ValueError, sqlite3.DatabaseError):
            append_refused = True

        connection = sqlite3.connect(self.db_path)
        try:
            counts = (
                connection.execute("SELECT COUNT(*) FROM lifecycle_events").fetchone()[0],
                connection.execute("SELECT COUNT(*) FROM lifecycle_current").fetchone()[0],
            )
        finally:
            connection.close()
        reopen_refused = False
        try:
            LifecycleLedger(
                self.db_path,
                ALLOWLIST,
                active_check_sets=ACTIVE_CHECK_SETS,
            )
        except (ValueError, sqlite3.DatabaseError):
            reopen_refused = True

        self.assertEqual(
            (append_refused, counts, reopen_refused),
            (True, (0, 0), True),
        )

    def test_unexpected_unique_index_fails_every_schema_seam_before_mutation(
        self,
    ) -> None:
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                "CREATE UNIQUE INDEX unexpected_event_digest "
                "ON lifecycle_events(digest)"
            )
            connection.commit()
        finally:
            connection.close()

        def refused(operation: Any) -> bool:
            try:
                operation()
            except (ValueError, sqlite3.DatabaseError):
                return True
            return False

        reopen_refused = refused(
            lambda: LifecycleLedger(
                self.db_path,
                ALLOWLIST,
                active_check_sets=ACTIVE_CHECK_SETS,
            )
        )
        verify_refused = refused(self.ledger.verify_integrity)
        append_refused = refused(
            lambda: self.registrar.append(event(event_id="unexpected-index-captured"))
        )
        connection = sqlite3.connect(self.db_path)
        try:
            counts = (
                connection.execute("SELECT COUNT(*) FROM lifecycle_events").fetchone()[0],
                connection.execute("SELECT COUNT(*) FROM lifecycle_current").fetchone()[0],
            )
        finally:
            connection.close()

        self.assertEqual(
            (reopen_refused, verify_refused, append_refused, counts),
            (True, True, True, (0, 0)),
        )

    def test_lowercase_fixture_check_literal_is_not_the_v1_schema(self) -> None:
        connection = sqlite3.connect(self.db_path)
        try:
            connection.executescript(
                """
                ALTER TABLE lifecycle_current RENAME TO lifecycle_current_original;
                CREATE TABLE lifecycle_current (
                    candidate_id TEXT PRIMARY KEY,
                    current_state TEXT NOT NULL,
                    package_hash TEXT,
                    deployment_identity_hash TEXT,
                    last_sequence INTEGER NOT NULL,
                    source_kind TEXT NOT NULL CHECK (source_kind = 'fixture'),
                    authoritative INTEGER NOT NULL CHECK (authoritative = 0)
                );
                DROP TABLE lifecycle_current_original;
                """
            )
            connection.commit()
            schema_sql = connection.execute(
                "SELECT sql FROM sqlite_master "
                "WHERE type = 'table' AND name = 'lifecycle_current'"
            ).fetchone()[0]
            quick_check = connection.execute("PRAGMA quick_check").fetchone()[0]
        finally:
            connection.close()

        self.assertIn("source_kind = 'fixture'", schema_sql)
        self.assertEqual(quick_check, "ok")
        with self.assertRaisesRegex(ValueError, "SCHEMA"):
            LifecycleLedger(
                self.db_path,
                ALLOWLIST,
                active_check_sets=ACTIVE_CHECK_SETS,
            )

    def test_non_utc_aware_timestamp_is_refused_without_mutation(self) -> None:
        non_utc = event(
            event_id="non-utc-captured",
            candidate_id="QLC-20260913-non-utc",
            timestamp=datetime.fromisoformat("2026-09-12T11:30:00+03:00"),
        )
        refused = False
        try:
            self.registrar.append(non_utc)
        except ValueError:
            refused = True

        connection = sqlite3.connect(self.db_path)
        try:
            counts_after_non_utc = (
                connection.execute("SELECT COUNT(*) FROM lifecycle_events").fetchone()[0],
                connection.execute("SELECT COUNT(*) FROM lifecycle_current").fetchone()[0],
            )
        finally:
            connection.close()

        utc_candidate = "QLC-20260913-utc-still-valid"
        self.registrar.append(
            event(
                event_id="utc-still-valid-captured",
                candidate_id=utc_candidate,
                timestamp=BASE_TIME,
            )
        )
        self.assertEqual(
            (
                refused,
                counts_after_non_utc,
                observed_state(self.ledger.current_state(utc_candidate)),
            ),
            (True, (0, 0), "CAPTURED"),
        )

    def test_historic_non_utc_event_fails_every_read_and_backup_seam(self) -> None:
        self.append_capture()
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute("DROP TRIGGER lifecycle_events_no_update")
            connection.execute("DROP TRIGGER lifecycle_events_no_delete")
            row = connection.execute(
                "SELECT canonical_event, canonical_evidence, previous_digest "
                "FROM lifecycle_events WHERE global_sequence = 1"
            ).fetchone()
            payload = json.loads(bytes(row[0]))
            payload["timestamp"] = "2026-09-12T11:30:00+03:00"
            event_bytes = json.dumps(
                payload,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            evidence_bytes = bytes(row[1])
            digest = hashlib.sha256(
                str(row[2]).encode("ascii")
                + b"\n"
                + event_bytes
                + b"\n"
                + evidence_bytes
            ).hexdigest()
            connection.execute(
                "UPDATE lifecycle_events SET canonical_event = ?, digest = ? "
                "WHERE global_sequence = 1",
                (event_bytes, digest),
            )
            connection.execute(
                "CREATE TRIGGER lifecycle_events_no_update "
                "BEFORE UPDATE ON lifecycle_events "
                "BEGIN SELECT RAISE(ABORT, 'IMMUTABLE_EVENT_HISTORY'); END"
            )
            connection.execute(
                "CREATE TRIGGER lifecycle_events_no_delete "
                "BEFORE DELETE ON lifecycle_events "
                "BEGIN SELECT RAISE(ABORT, 'IMMUTABLE_EVENT_HISTORY'); END"
            )
            connection.commit()
        finally:
            connection.close()

        backup_path = Path(self.temp_dir.name) / "non-utc-history-backup.sqlite"
        operations = {
            "replay": self.ledger.replay,
            "integrity": self.ledger.verify_integrity,
            "current": lambda: self.ledger.current_state(CANDIDATE_A),
            "report": self.ledger.render_status_report,
            "backup": lambda: self.ledger.backup_to(backup_path),
        }
        for seam, operation in operations.items():
            with self.subTest(seam=seam):
                with self.assertRaisesRegex(ValueError, "TIMESTAMP_NOT_UTC"):
                    operation()

    def test_admission_record_types_materialize_only_canonical_states(self) -> None:
        self.append_to_frozen()

        def append_decision(
            event_id: str,
            event_type: str,
            previous_state: str,
            next_state: str,
            writer_class: str,
            writer_id: str,
            check_set_version: str,
            offset: int,
        ) -> None:
            self.ledger.append(
                event(
                    event_id=event_id,
                    event_type=event_type,
                    previous_state=previous_state,
                    next_state=next_state,
                    writer_class=writer_class,
                    writer_id=writer_id,
                    package_hash=PACKAGE_A,
                    deployment_identity_hash=DEPLOYMENT_A,
                    timestamp=BASE_TIME + timedelta(seconds=offset),
                ),
                check_set_version=check_set_version,
                evaluation_run_hash=hashlib.sha256(event_id.encode()).hexdigest(),
            )

        decisions = (
            ("canonical-shadow", "SHADOW_ELIGIBLE", "FROZEN", "SHADOW", "shadow-eligibility.v1"),
            ("canonical-paper", "PAPER_ELIGIBLE", "SHADOW", "SHADOW", "paper-eligibility.v1"),
            ("canonical-testnet", "TESTNET_ELIGIBLE", "SHADOW", "TESTNET", "testnet-eligibility.v1"),
            ("canonical-live-candidate", "LIVE_CANDIDATE", "TESTNET", "LIVE_CANDIDATE", "live-candidate-eligibility.v1"),
            ("canonical-live", "PROMOTED", "LIVE_CANDIDATE", "LIVE", "promotion.v1"),
        )
        for offset, (event_id, event_type, previous, next_state, check_set) in enumerate(
            decisions, start=4
        ):
            append_decision(
                event_id,
                event_type,
                previous,
                next_state,
                "PROMOTION_AUTHORITY" if event_type == "PROMOTED" else "ENVIRONMENT_ADMISSION_AUTHORITY",
                "promotion-1" if event_type == "PROMOTED" else "admission-1",
                check_set,
                offset,
            )
            self.assertEqual(
                observed_state(self.ledger.current_state(CANDIDATE_A)), next_state
            )

        capacity = self.new_ledger("canonical-capacity")
        capacity_candidate = "QLC-20260913-canonical-capacity"
        self.append_frozen_fixture(
            capacity, capacity_candidate, "canonical-capacity"
        )
        self.append_authority_event(
            capacity,
            candidate_id=capacity_candidate,
            event_id="canonical-capacity-withheld",
            event_type="ADMISSION_WITHHELD_CAPACITY",
            previous_state="FROZEN",
            next_state="FROZEN",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="shadow-eligibility.v1",
        )
        self.assertEqual(observed_state(capacity.current_state(capacity_candidate)), "FROZEN")

        shadow = self.new_ledger("ambiguous-shadow-capacity")
        shadow_candidate = "QLC-20260913-ambiguous-shadow-capacity"
        self.build_to_rung(
            shadow, shadow_candidate, "ambiguous-shadow-capacity", "SHADOW_ELIGIBLE"
        )
        self.append_authority_event(
            shadow,
            candidate_id=shadow_candidate,
            event_id="shadow-capacity-withheld",
            event_type="ADMISSION_WITHHELD_CAPACITY",
            previous_state="SHADOW",
            next_state="SHADOW",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="paper-eligibility.v1",
            offset=5,
        )
        self.assertEqual(observed_state(shadow.current_state(shadow_candidate)), "SHADOW")

        wrong_capacity = self.new_ledger("wrong-shadow-capacity")
        wrong_capacity_candidate = "QLC-20260913-wrong-shadow-capacity"
        self.build_to_rung(
            wrong_capacity,
            wrong_capacity_candidate,
            "wrong-shadow-capacity",
            "SHADOW_ELIGIBLE",
        )
        with self.assertRaisesRegex(ValueError, "ADMISSION_WITHHELD_TARGET_UNRESOLVED"):
            self.append_authority_event(
                wrong_capacity,
                candidate_id=wrong_capacity_candidate,
                event_id="wrong-shadow-capacity-withheld",
                event_type="ADMISSION_WITHHELD_CAPACITY",
                previous_state="SHADOW",
                next_state="SHADOW",
                writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                writer_id="admission-1",
                check_set_version="promotion.v1",
                offset=5,
            )

    def test_rejected_purpose_and_stale_evaluation_fail_closed(self) -> None:
        def inject_history(
            ledger: LifecycleLedger,
            historic_event: LifecycleEvent,
            *,
            check_set_version: str,
            evaluation_run_hash: str,
            failing_checks: tuple[dict[str, Any], ...] = (),
        ) -> None:
            event_bytes = json.dumps(
                historic_event.model_dump(mode="json"),
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            evidence_bytes = json.dumps(
                {
                    "check_set_purpose": (
                        "shadow_eligibility"
                        if historic_event.event_type == "SHADOW_ELIGIBLE"
                        else None
                    ),
                    "check_set_version": check_set_version,
                    "evaluation_run_hash": evaluation_run_hash,
                    "failing_checks": list(failing_checks),
                    "catalog_backed": False,
                    "source_kind": "FIXTURE",
                },
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            connection = sqlite3.connect(ledger.path)
            try:
                sequence = connection.execute(
                    "SELECT COALESCE(MAX(global_sequence), 0) + 1 FROM lifecycle_events"
                ).fetchone()[0]
                writer_sequence = connection.execute(
                    "SELECT COUNT(*) + 1 FROM lifecycle_events "
                    "WHERE writer_class = ? AND writer_id = ?",
                    (historic_event.writer_class.value, historic_event.writer_id),
                ).fetchone()[0]
                previous_digest = connection.execute(
                    "SELECT digest FROM lifecycle_events "
                    "ORDER BY global_sequence DESC LIMIT 1"
                ).fetchone()[0]
                digest = hashlib.sha256(
                    previous_digest.encode("ascii")
                    + b"\n"
                    + event_bytes
                    + b"\n"
                    + evidence_bytes
                ).hexdigest()
                prior_identity = connection.execute(
                    "SELECT package_hash, deployment_identity_hash "
                    "FROM lifecycle_current WHERE candidate_id = ?",
                    (historic_event.candidate_id,),
                ).fetchone()
                package_hash = historic_event.package_hash or prior_identity[0]
                deployment_hash = (
                    historic_event.deployment_identity_hash or prior_identity[1]
                )
                connection.execute(
                    "INSERT INTO lifecycle_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        sequence,
                        historic_event.event_id,
                        historic_event.writer_class.value,
                        historic_event.writer_id,
                        writer_sequence,
                        historic_event.candidate_id,
                        event_bytes,
                        evidence_bytes,
                        previous_digest,
                        digest,
                    ),
                )
                connection.execute(
                    "UPDATE lifecycle_current SET current_state = ?, package_hash = ?, "
                    "deployment_identity_hash = ?, last_sequence = ? "
                    "WHERE candidate_id = ?",
                    (
                        historic_event.next_state,
                        package_hash,
                        deployment_hash,
                        sequence,
                        historic_event.candidate_id,
                    ),
                )
                connection.commit()
            finally:
                connection.close()

        rejected = self.new_ledger("rejected-purpose-required")
        rejected_candidate = "QLC-20260913-rejected-purpose-required"
        self.append_candidate_fixture(
            rejected, rejected_candidate, "rejected-purpose-required"
        )
        rejected_refused = False
        try:
            Registrar(rejected, "registrar-1").append(
                event(
                    event_id="rejected-purpose-record",
                    event_type="REJECTED",
                    previous_state="CANDIDATE",
                    next_state="REJECTED",
                    candidate_id=rejected_candidate,
                    timestamp=BASE_TIME + timedelta(seconds=3),
                ),
                check_set_version="worthiness.v1",
                evaluation_run_hash=EVALUATION_A,
                failing_checks=FAILING_CHECKS,
            )
        except ValueError as exc:
            rejected_refused = str(exc) == "CHECK_SET_PURPOSE_REQUIRED"
        inject_history(
            rejected,
            event(
                event_id="historic-rejected-purpose-record",
                event_type="REJECTED",
                previous_state="CANDIDATE",
                next_state="REJECTED",
                candidate_id=rejected_candidate,
                timestamp=BASE_TIME + timedelta(seconds=3),
            ),
            check_set_version="worthiness.v1",
            evaluation_run_hash=EVALUATION_A,
            failing_checks=FAILING_CHECKS,
        )
        with self.assertRaisesRegex(ValueError, "CHECK_SET_PURPOSE_REQUIRED"):
            rejected.replay()

        stale = self.new_ledger("stale-evaluation-epoch")
        stale_candidate = "QLC-20260913-stale-evaluation-epoch"
        self.build_to_rung(
            stale, stale_candidate, "stale-evaluation-epoch", "SHADOW_ELIGIBLE"
        )
        prior_state = observed_state(stale.current_state(stale_candidate))
        self.append_authority_event(
            stale,
            candidate_id=stale_candidate,
            event_id="stale-evaluation-retired",
            event_type="RETIRED",
            previous_state=prior_state,
            next_state="RETIRED",
            writer_class="MULTI_WORKER_SUPERVISOR",
            writer_id="supervisor-1",
            check_set_version="supervisor.v1",
            offset=5,
        )
        Registrar(stale, "registrar-1").append(
            event(
                event_id="stale-evaluation-reentry",
                event_type="RE_ENTRY",
                previous_state="RETIRED",
                next_state="CANDIDATE",
                candidate_id=stale_candidate,
                reason="Exchange rules materially changed.",
                trigger="OWNER_EXTERNAL_CHANGE",
                timestamp=BASE_TIME + timedelta(seconds=6),
            ),
            evaluation_run_hash=EVALUATION_B,
        )
        Registrar(stale, "registrar-1").append(
            event(
                event_id="stale-evaluation-refrozen",
                event_type="FROZEN",
                previous_state="CANDIDATE",
                next_state="FROZEN",
                candidate_id=stale_candidate,
                package_hash=PACKAGE_B,
                timestamp=BASE_TIME + timedelta(seconds=7),
            )
        )
        stale_event = event(
            event_id="stale-evaluation-reused",
            event_type="SHADOW_ELIGIBLE",
            writer_id="admission-1",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            previous_state="FROZEN",
            next_state="SHADOW",
            candidate_id=stale_candidate,
            package_hash=PACKAGE_B,
            deployment_identity_hash=DEPLOYMENT_B,
            timestamp=BASE_TIME + timedelta(seconds=8),
        )
        prior_evaluation = hashlib.sha256(
            b"stale-evaluation-epoch-shadow_eligible"
        ).hexdigest()
        stale_refused = False
        try:
            stale.append(
                stale_event,
                check_set_version="shadow-eligibility.v1",
                evaluation_run_hash=prior_evaluation,
            )
        except ValueError as exc:
            stale_refused = str(exc) == "EVALUATION_RUN_HASH_REUSED"
        inject_history(
            stale,
            stale_event,
            check_set_version="shadow-eligibility.v1",
            evaluation_run_hash=prior_evaluation,
        )
        with self.assertRaisesRegex(ValueError, "EVALUATION_RUN_HASH_REUSED"):
            stale.verify_integrity()

        self.assertEqual((rejected_refused, stale_refused), (True, True))

    def test_backup_copies_the_same_source_handle_it_verified(self) -> None:
        source_candidate = "QLC-20260913-backup-source-a"
        self.append_capture(candidate_id=source_candidate, event_id="backup-source-a")
        replacement = self.new_ledger("backup-source-b")
        replacement_candidate = "QLC-20260913-backup-source-b"
        Registrar(replacement, "registrar-1").append(
            event(event_id="backup-source-b", candidate_id=replacement_candidate)
        )
        backup_path = Path(self.temp_dir.name) / "stable-source-backup.sqlite"
        original_path = self.ledger.path
        original_snapshot = self.ledger._verified_snapshot
        swapped = False

        def verify_then_swap(connection: sqlite3.Connection) -> Any:
            nonlocal swapped
            result = original_snapshot(connection)
            self.ledger.path = replacement.path
            swapped = True
            return result

        try:
            with patch.object(
                self.ledger, "_verified_snapshot", side_effect=verify_then_swap
            ):
                self.ledger.backup_to(backup_path)
        finally:
            self.ledger.path = original_path

        copied = LifecycleLedger(
            backup_path, ALLOWLIST, active_check_sets=ACTIVE_CHECK_SETS
        )
        copied_candidates = {record.candidate_id for record in copied.replay()}
        self.assertEqual((swapped, copied_candidates), (True, {source_candidate}))

    def test_empty_generator_writer_allowlist_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            LifecycleLedger(
                Path(self.temp_dir.name) / "empty-generator.sqlite",
                (writer for writer in ()),
            )

    def test_report_states_hash_and_external_checkpoint_assurance_limits(self) -> None:
        report = json.loads(self.ledger.render_status_report())

        self.assertEqual(
            set(report["assurance_limits"]),
            {
                "internal hashes do not independently prove omission-free history",
                "missing events require external expected-event/writer checkpoints",
            },
        )

    def test_current_epoch_evaluation_may_support_multiple_decisions(self) -> None:
        capacity = self.new_ledger("current-epoch-capacity")
        capacity_candidate = "QLC-20260913-current-epoch-capacity"
        self.append_frozen_fixture(
            capacity, capacity_candidate, "current-epoch-capacity"
        )
        for event_id, event_type, previous_state, next_state in (
            (
                "current-epoch-capacity-withheld",
                "ADMISSION_WITHHELD_CAPACITY",
                "FROZEN",
                "FROZEN",
            ),
            (
                "current-epoch-capacity-shadow",
                "SHADOW_ELIGIBLE",
                "FROZEN",
                "SHADOW",
            ),
        ):
            self.append_authority_event(
                capacity,
                candidate_id=capacity_candidate,
                event_id=event_id,
                event_type=event_type,
                previous_state=previous_state,
                next_state=next_state,
                writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                writer_id="admission-1",
                check_set_version="shadow-eligibility.v1",
                evaluation_run_hash=EVALUATION_A,
            )

        paper = self.new_ledger("current-epoch-paper")
        paper_candidate = "QLC-20260913-current-epoch-paper"
        self.build_to_rung(
            paper, paper_candidate, "current-epoch-paper", "SHADOW_ELIGIBLE"
        )
        self.append_authority_event(
            paper,
            candidate_id=paper_candidate,
            event_id="current-epoch-paper-eligible",
            event_type="PAPER_ELIGIBLE",
            previous_state="SHADOW",
            next_state="SHADOW",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="paper-eligibility.v1",
            evaluation_run_hash=EVALUATION_A,
        )
        self.append_authority_event(
            paper,
            candidate_id=paper_candidate,
            event_id="current-epoch-testnet-eligible",
            event_type="TESTNET_ELIGIBLE",
            previous_state="SHADOW",
            next_state="TESTNET",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="testnet-eligibility.v1",
            evaluation_run_hash=EVALUATION_A,
        )

        live = self.new_ledger("current-epoch-live")
        live_candidate = "QLC-20260913-current-epoch-live"
        self.build_to_rung(
            live, live_candidate, "current-epoch-live", "TESTNET_ELIGIBLE"
        )
        self.append_authority_event(
            live,
            candidate_id=live_candidate,
            event_id="current-epoch-live-decision",
            event_type="LIVE_CANDIDATE",
            previous_state="TESTNET",
            next_state="LIVE_CANDIDATE",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="live-candidate-eligibility.v1",
            evaluation_run_hash=EVALUATION_A,
            offset=6,
        )
        self.append_authority_event(
            live,
            candidate_id=live_candidate,
            event_id="current-epoch-promotion-decision",
            event_type="PROMOTED",
            previous_state="LIVE_CANDIDATE",
            next_state="LIVE",
            writer_class="PROMOTION_AUTHORITY",
            writer_id="promotion-1",
            check_set_version="promotion.v1",
            evaluation_run_hash=EVALUATION_A,
            offset=6,
        )

        for ledger in (capacity, paper, live):
            ledger.verify_integrity()
        self.assertEqual(
            [
                (
                    record.event_type,
                    record.check_set_purpose,
                    record.check_set_version,
                    record.evaluation_run_hash,
                )
                for record in capacity.replay()[-2:]
            ],
            [
                (
                    "ADMISSION_WITHHELD_CAPACITY",
                    "shadow_eligibility",
                    "shadow-eligibility.v1",
                    EVALUATION_A,
                ),
                (
                    "SHADOW_ELIGIBLE",
                    "shadow_eligibility",
                    "shadow-eligibility.v1",
                    EVALUATION_A,
                ),
            ],
        )
        self.assertEqual(observed_state(capacity.current_state(capacity_candidate)), "SHADOW")
        self.assertEqual(
            [
                (
                    record.event_type,
                    record.check_set_purpose,
                    record.check_set_version,
                    record.evaluation_run_hash,
                )
                for record in paper.replay()[-2:]
            ],
            [
                ("PAPER_ELIGIBLE", "paper_eligibility", "paper-eligibility.v1", EVALUATION_A),
                (
                    "TESTNET_ELIGIBLE",
                    "testnet_live_candidate_eligibility",
                    "testnet-eligibility.v1",
                    EVALUATION_A,
                ),
            ],
        )
        self.assertEqual(observed_state(paper.current_state(paper_candidate)), "TESTNET")
        self.assertEqual(
            [
                (
                    record.event_type,
                    record.check_set_purpose,
                    record.check_set_version,
                    record.evaluation_run_hash,
                )
                for record in live.replay()[-2:]
            ],
            [
                (
                    "LIVE_CANDIDATE",
                    "live_candidate_eligibility",
                    "live-candidate-eligibility.v1",
                    EVALUATION_A,
                ),
                ("PROMOTED", "promotion", "promotion.v1", EVALUATION_A),
            ],
        )
        self.assertEqual(observed_state(live.current_state(live_candidate)), "LIVE")

    def test_live_candidate_uses_a_distinct_check_set_purpose(self) -> None:
        self.build_to_rung(
            self.ledger, CANDIDATE_A, "live-purpose", "TESTNET_ELIGIBLE"
        )
        with self.assertRaisesRegex(ValueError, "CHECK_SET_PURPOSE_MISMATCH"):
            self.append_authority_event(
                self.ledger,
                candidate_id=CANDIDATE_A,
                event_id="live-purpose-testnet-version-refused",
                event_type="LIVE_CANDIDATE",
                previous_state="TESTNET",
                next_state="LIVE_CANDIDATE",
                writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                writer_id="admission-1",
                check_set_version="testnet-eligibility.v1",
                offset=6,
            )

        configured = LifecycleLedger(
            Path(self.temp_dir.name) / "live-purpose-configured.sqlite",
            ALLOWLIST,
            active_check_sets=ACTIVE_CHECK_SETS,
        )
        candidate_id = "QLC-20260913-live-purpose-configured"
        self.build_to_rung(
            configured, candidate_id, "live-purpose-configured", "TESTNET_ELIGIBLE"
        )
        self.append_authority_event(
            configured,
            candidate_id=candidate_id,
            event_id="live-purpose-distinct-version",
            event_type="LIVE_CANDIDATE",
            previous_state="TESTNET",
            next_state="LIVE_CANDIDATE",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="live-candidate-eligibility.v1",
            offset=6,
        )

    def test_demoted_requires_strict_descent_and_keeps_deployment_identity(self) -> None:
        candidate_id = "QLC-20260913-demoted"
        self.build_to_rung(self.ledger, candidate_id, "demoted", "PROMOTED")
        self.append_authority_event(
            self.ledger,
            candidate_id=candidate_id,
            event_id="demoted-to-live-candidate",
            event_type="DEMOTED",
            previous_state="LIVE",
            next_state="LIVE_CANDIDATE",
            writer_class="MULTI_WORKER_SUPERVISOR",
            writer_id="supervisor-1",
            check_set_version="supervisor.v1",
            offset=8,
        )
        state = self.ledger.current_state(candidate_id)
        self.assertEqual(observed_state(state), "LIVE_CANDIDATE")
        self.assertEqual(state["deployment_identity_hash"], DEPLOYMENT_A)

        with self.assertRaisesRegex(ValueError, "DEMOTION_TARGET_RUNG_NOT_BELOW_CURRENT"):
            self.append_authority_event(
                self.ledger,
                candidate_id=candidate_id,
                event_id="demoted-sideways-refused",
                event_type="DEMOTED",
                previous_state="LIVE_CANDIDATE",
                next_state="LIVE_CANDIDATE",
                writer_class="MULTI_WORKER_SUPERVISOR",
                writer_id="supervisor-1",
                check_set_version="supervisor.v1",
                offset=9,
            )

    def test_deployment_refresh_returns_to_frozen_under_new_composite(self) -> None:
        candidate_id = "QLC-20260913-deployment-refresh"
        self.build_to_rung(
            self.ledger, candidate_id, "deployment-refresh", "SHADOW_ELIGIBLE"
        )
        with self.assertRaisesRegex(
            ValueError, "DEPLOYMENT_REFRESH_IDENTITY_INVALID"
        ):
            self.registrar.append(
                event(
                    event_id="deployment-refresh-same-identity-refused",
                    event_type="FROZEN",
                    previous_state="SHADOW",
                    next_state="FROZEN",
                    candidate_id=candidate_id,
                    package_hash=PACKAGE_A,
                    deployment_identity_hash=DEPLOYMENT_A,
                    evidence_references=("fixture://deployment-refresh/same-composite",),
                    timestamp=BASE_TIME + timedelta(seconds=5),
                )
            )
        with self.assertRaisesRegex(
            ValueError, "DEPLOYMENT_REFRESH_IDENTITY_INVALID"
        ):
            self.registrar.append(
                event(
                    event_id="deployment-refresh-missing-identity-refused",
                    event_type="FROZEN",
                    previous_state="SHADOW",
                    next_state="FROZEN",
                    candidate_id=candidate_id,
                    package_hash=PACKAGE_A,
                    deployment_identity_hash=None,
                    evidence_references=("fixture://deployment-refresh/missing-identity",),
                    timestamp=BASE_TIME + timedelta(seconds=5),
                )
            )
        with self.assertRaisesRegex(
            ValueError, "DEPLOYMENT_REFRESH_IDENTITY_INVALID"
        ):
            self.registrar.append(
                event(
                    event_id="deployment-refresh-package-drift-refused",
                    event_type="FROZEN",
                    previous_state="SHADOW",
                    next_state="FROZEN",
                    candidate_id=candidate_id,
                    package_hash=PACKAGE_B,
                    deployment_identity_hash=DEPLOYMENT_B,
                    evidence_references=("fixture://deployment-refresh/package-drift",),
                    timestamp=BASE_TIME + timedelta(seconds=5),
                )
            )
        self.registrar.append(
            event(
                event_id="deployment-refresh-record",
                event_type="FROZEN",
                previous_state="SHADOW",
                next_state="FROZEN",
                candidate_id=candidate_id,
                package_hash=PACKAGE_A,
                deployment_identity_hash=DEPLOYMENT_B,
                evidence_references=("fixture://deployment-refresh/new-composite",),
                timestamp=BASE_TIME + timedelta(seconds=6),
            )
        )
        state = self.ledger.current_state(candidate_id)
        self.assertEqual(observed_state(state), "FROZEN")
        self.assertEqual(state["package_hash"], PACKAGE_A)
        self.assertEqual(state["deployment_identity_hash"], DEPLOYMENT_B)

    def test_status_report_identifies_events_and_all_contract_blockers(self) -> None:
        self.append_capture()
        report = json.loads(self.ledger.render_status_report())

        row = report["fixture_ledger_records"][0]
        self.assertEqual(
            (row["event_id"], row["event_type"]),
            ("event-captured-a", "CAPTURED"),
        )
        self.assertEqual(
            set(report["unresolved_lifecycle_contracts"]),
            {
                "CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING",
            },
        )
        self.assertEqual(
            set(report["ratified_lifecycle_contracts"]),
            {
                "DEMOTED TARGET RUNG MAPPING: RESOLVED BY OD-2",
                "ATOMIC SUCCESSION INTERIM REFUSAL: RATIFIED BY OD-4",
                "REJECTED FAILED-GATE PURPOSE: RESOLVED BY OD-5",
                "ADMISSION WITHHELD CAPACITY TARGET: RESOLVED BY OD-6",
                "DEPLOYMENT REFRESH ENVELOPE: RESOLVED BY OD-7",
                "EVALUATION RUN CANDIDATE SCOPE: RATIFIED BY OD-8",
                "SAME-EPOCH EVALUATION REUSE: RATIFIED BY OD-10",
            },
        )

    def test_pre_purpose_history_fails_every_read_and_backup_seam(self) -> None:
        candidate_id = "QLC-20260913-purpose-missing"
        self.build_to_rung(
            self.ledger, candidate_id, "purpose-missing", "TESTNET_ELIGIBLE"
        )
        self.inject_live_candidate_history(
            self.ledger,
            candidate_id,
            "purpose-missing-live-candidate",
            include_purpose=False,
        )
        backup_path = Path(self.temp_dir.name) / "purpose-missing-backup.sqlite"
        operations = {
            "replay": self.ledger.replay,
            "integrity": self.ledger.verify_integrity,
            "current": lambda: self.ledger.current_state(candidate_id),
            "report": self.ledger.render_status_report,
            "backup": lambda: self.ledger.backup_to(backup_path),
        }
        for seam, operation in operations.items():
            with self.subTest(seam=seam):
                with self.assertRaisesRegex(
                    ValueError, "CHECK_SET_PURPOSE_MISSING"
                ):
                    operation()

    def test_wrong_historic_purpose_fails_every_read_and_backup_seam(self) -> None:
        candidate_id = "QLC-20260913-purpose-mismatch"
        self.build_to_rung(
            self.ledger, candidate_id, "purpose-mismatch", "TESTNET_ELIGIBLE"
        )
        self.inject_live_candidate_history(
            self.ledger,
            candidate_id,
            "purpose-mismatch-live-candidate",
            include_purpose=True,
        )
        backup_path = Path(self.temp_dir.name) / "purpose-mismatch-backup.sqlite"
        operations = {
            "replay": self.ledger.replay,
            "integrity": self.ledger.verify_integrity,
            "current": lambda: self.ledger.current_state(candidate_id),
            "report": self.ledger.render_status_report,
            "backup": lambda: self.ledger.backup_to(backup_path),
        }
        for seam, operation in operations.items():
            with self.subTest(seam=seam):
                with self.assertRaisesRegex(
                    ValueError, "CHECK_SET_PURPOSE_MISMATCH"
                ):
                    operation()

    def test_new_history_exposes_derived_check_set_purpose(self) -> None:
        self.build_to_rung(
            self.ledger, CANDIDATE_A, "purpose-provenance", "LIVE_CANDIDATE"
        )

        replay = self.ledger.replay()
        self.assertIsNone(replay[0].check_set_purpose)
        self.assertEqual(
            replay[-1].check_set_purpose, "live_candidate_eligibility"
        )
        connection = sqlite3.connect(self.db_path)
        try:
            evidence = [
                json.loads(bytes(row[0]))
                for row in connection.execute(
                    "SELECT canonical_evidence FROM lifecycle_events "
                    "ORDER BY global_sequence"
                )
            ]
        finally:
            connection.close()
        self.assertTrue(
            all(
                set(item)
                == {
                    "check_set_purpose",
                    "check_set_version",
                    "evaluation_run_hash",
                    "failing_checks",
                    "catalog_backed",
                    "source_kind",
                }
                for item in evidence
            )
        )
        self.assertIsNone(evidence[0]["check_set_purpose"])
        self.assertEqual(
            evidence[-1]["check_set_purpose"], "live_candidate_eligibility"
        )
        report = json.loads(self.ledger.render_status_report())
        self.assertIsNone(report["fixture_ledger_records"][0]["check_set_purpose"])
        self.assertEqual(
            report["fixture_ledger_records"][-1]["check_set_purpose"],
            "live_candidate_eligibility",
        )
        self.ledger.verify_integrity()
        self.assertEqual(
            observed_state(self.ledger.current_state(CANDIDATE_A)), "LIVE_CANDIDATE"
        )
        self.ledger.backup_to(
            Path(self.temp_dir.name) / "purpose-provenance-backup.sqlite"
        )

    def test_evaluation_hash_cannot_cross_candidate_scope(self) -> None:
        first_candidate = "QLC-20260913-evaluation-scope-first"
        second_candidate = "QLC-20260913-evaluation-scope-second"
        self.append_frozen_fixture(
            self.ledger, first_candidate, "evaluation-scope-first"
        )
        self.append_frozen_fixture(
            self.ledger,
            second_candidate,
            "evaluation-scope-second",
            package_hash=PACKAGE_B,
        )
        self.append_authority_event(
            self.ledger,
            candidate_id=first_candidate,
            event_id="evaluation-scope-first-shadow",
            event_type="SHADOW_ELIGIBLE",
            previous_state="FROZEN",
            next_state="SHADOW",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="shadow-eligibility.v1",
            evaluation_run_hash=EVALUATION_A,
        )
        with self.subTest(seam="append"):
            with self.assertRaisesRegex(
                ValueError, "EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED"
            ):
                self.append_authority_event(
                    self.ledger,
                    candidate_id=second_candidate,
                    event_id="evaluation-scope-second-shadow",
                    event_type="SHADOW_ELIGIBLE",
                    previous_state="FROZEN",
                    next_state="SHADOW",
                    writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                    writer_id="admission-1",
                    check_set_version="shadow-eligibility.v1",
                    package_hash=PACKAGE_B,
                    deployment_identity_hash=DEPLOYMENT_B,
                    evaluation_run_hash=EVALUATION_A,
                )

        replay = self.new_ledger("evaluation-scope-replay")
        self.build_to_rung(
            replay,
            first_candidate,
            "evaluation-scope-replay-first",
            "TESTNET_ELIGIBLE",
        )
        self.append_authority_event(
            replay,
            candidate_id=first_candidate,
            event_id="evaluation-scope-replay-first-live",
            event_type="LIVE_CANDIDATE",
            previous_state="TESTNET",
            next_state="LIVE_CANDIDATE",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="live-candidate-eligibility.v1",
            evaluation_run_hash=EVALUATION_A,
            offset=6,
        )
        self.build_to_rung(
            replay,
            second_candidate,
            "evaluation-scope-replay-second",
            "TESTNET_ELIGIBLE",
            package_hash=PACKAGE_B,
            deployment_identity_hash=DEPLOYMENT_B,
        )
        self.inject_live_candidate_history(
            replay,
            second_candidate,
            "evaluation-scope-replay-second-live",
            include_purpose=True,
            purpose="live_candidate_eligibility",
            package_hash=PACKAGE_B,
            deployment_identity_hash=DEPLOYMENT_B,
        )
        with self.subTest(seam="replay"):
            with self.assertRaisesRegex(
                ValueError, "EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED"
            ):
                replay.replay()

    def test_catalog_backed_claim_fails_closed_without_catalog(self) -> None:
        candidate_id = "QLC-20260913-catalog-backed"
        self.append_frozen_fixture(self.ledger, candidate_id, "catalog-backed")
        with self.assertRaisesRegex(
            ValueError, "CATALOG_BACKED_EVIDENCE_WITHOUT_ACCEPTED_CATALOG"
        ):
            self.append_authority_event(
                self.ledger,
                candidate_id=candidate_id,
                event_id="catalog-backed-without-catalog",
                event_type="SHADOW_ELIGIBLE",
                previous_state="FROZEN",
                next_state="SHADOW",
                writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                writer_id="admission-1",
                check_set_version="shadow-eligibility.v1",
                evaluation_run_hash=EVALUATION_A,
                catalog_backed=True,
            )

    def test_accepted_evaluation_catalog_rejects_invalid_shapes(self) -> None:
        for label, catalog in (
            ("string", EVALUATION_A),
            ("bytes", EVALUATION_A.encode("ascii")),
            ("bytearray", bytearray(EVALUATION_A.encode("ascii"))),
            ("uppercase-hash", ("A" * 64,)),
            ("short-hash", ("abc",)),
            ("non-string-hash", (1,)),
        ):
            with self.subTest(label=label):
                with self.assertRaisesRegex(
                    ValueError, "ACCEPTED_EVALUATION_CATALOG_INVALID"
                ):
                    LifecycleLedger(
                        Path(self.temp_dir.name) / f"invalid-catalog-{label}.sqlite",
                        ALLOWLIST,
                        active_check_sets=ACTIVE_CHECK_SETS,
                        accepted_evaluation_catalog=catalog,
                    )

    def test_accepted_evaluation_catalog_accepts_valid_hash_tuple(self) -> None:
        ledger = self.new_ledger(
            "valid-catalog-tuple",
            accepted_evaluation_catalog=(EVALUATION_A, EVALUATION_B),
        )

        self.assertEqual(
            ledger.accepted_evaluation_catalog,
            frozenset((EVALUATION_A, EVALUATION_B)),
        )

    def test_catalog_backed_argument_must_be_bool(self) -> None:
        for label, catalog_backed in (
            ("integer", 1),
            ("string", "true"),
            ("float", 1.0),
            ("none", None),
        ):
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, "CATALOG_BACKED_INVALID"):
                    self.registrar.append(
                        event(event_id=f"catalog-backed-invalid-{label}"),
                        catalog_backed=catalog_backed,
                    )

    def test_configured_catalog_refuses_absent_hash_and_accepts_present_hash(self) -> None:
        ledger = self.new_ledger(
            "configured-catalog",
            accepted_evaluation_catalog=(EVALUATION_A,),
        )
        accepted_candidate = "QLC-20260913-catalog-accepted"
        self.append_frozen_fixture(ledger, accepted_candidate, "catalog-accepted")
        self.append_authority_event(
            ledger,
            candidate_id=accepted_candidate,
            event_id="catalog-present-shadow",
            event_type="SHADOW_ELIGIBLE",
            previous_state="FROZEN",
            next_state="SHADOW",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="shadow-eligibility.v1",
            evaluation_run_hash=EVALUATION_A,
            catalog_backed=True,
        )
        self.assertEqual(observed_state(ledger.current_state(accepted_candidate)), "SHADOW")

        refused_candidate = "QLC-20260913-catalog-refused"
        self.append_frozen_fixture(
            ledger,
            refused_candidate,
            "catalog-refused",
            package_hash=PACKAGE_B,
        )
        with self.assertRaisesRegex(
            ValueError, "EVALUATION_RUN_HASH_NOT_IN_ACCEPTED_CATALOG"
        ):
            self.append_authority_event(
                ledger,
                candidate_id=refused_candidate,
                event_id="catalog-absent-shadow",
                event_type="SHADOW_ELIGIBLE",
                previous_state="FROZEN",
                next_state="SHADOW",
                writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                writer_id="admission-1",
                check_set_version="shadow-eligibility.v1",
                package_hash=PACKAGE_B,
                deployment_identity_hash=DEPLOYMENT_B,
                evaluation_run_hash=EVALUATION_B,
            )

        missing_hash_candidate = "QLC-20260913-catalog-missing-hash"
        self.append_frozen_fixture(
            ledger,
            missing_hash_candidate,
            "catalog-missing-hash",
            package_hash="7" * 64,
        )
        with self.assertRaisesRegex(
            ValueError, "CATALOG_BACKED_WITHOUT_EVALUATION_HASH"
        ):
            ledger.append(
                event(
                    event_id="catalog-backed-without-evaluation-hash",
                    event_type="SHADOW_ELIGIBLE",
                    writer_id="admission-1",
                    writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                    previous_state="FROZEN",
                    next_state="SHADOW",
                    candidate_id=missing_hash_candidate,
                    package_hash="7" * 64,
                    deployment_identity_hash="8" * 64,
                    timestamp=BASE_TIME + timedelta(seconds=4),
                ),
                check_set_version="shadow-eligibility.v1",
                catalog_backed=True,
            )

    def test_deployment_refresh_registrar_path_is_available_at_every_deep_state(
        self,
    ) -> None:
        cases = (
            (
                "TESTNET_ELIGIBLE",
                "TESTNET",
                "LIVE_CANDIDATE",
                "LIVE_CANDIDATE",
                "ENVIRONMENT_ADMISSION_AUTHORITY",
                "admission-1",
                "live-candidate-eligibility.v1",
            ),
            (
                "LIVE_CANDIDATE",
                "LIVE_CANDIDATE",
                "PROMOTED",
                "LIVE",
                "PROMOTION_AUTHORITY",
                "promotion-1",
                "promotion.v1",
            ),
            (
                "PROMOTED",
                "LIVE",
                "SUSPENDED",
                "SUSPENDED",
                "MULTI_WORKER_SUPERVISOR",
                "supervisor-1",
                "supervisor.v1",
            ),
        )
        for build_target, state, event_type, next_state, writer_class, writer_id, check_set in cases:
            with self.subTest(state=state):
                ledger = self.new_ledger(f"deployment-refresh-{state.lower()}")
                candidate_id = f"QLC-20260913-refresh-{state.lower()}"
                self.build_to_rung(
                    ledger, candidate_id, f"refresh-{state.lower()}", build_target
                )
                with self.assertRaisesRegex(
                    ValueError, "DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED"
                ):
                    self.append_authority_event(
                        ledger,
                        candidate_id=candidate_id,
                        event_id=f"refresh-{state.lower()}-authority-attempt",
                        event_type=event_type,
                        previous_state=state,
                        next_state=next_state,
                        writer_class=writer_class,
                        writer_id=writer_id,
                        check_set_version=check_set,
                        deployment_identity_hash=DEPLOYMENT_B,
                        offset=9,
                    )
                with self.assertRaisesRegex(ValueError, "DEPLOYMENT_REFRESH_IDENTITY_INVALID"):
                    Registrar(ledger, "registrar-1").append(
                        event(
                            event_id=f"refresh-{state.lower()}-same-identity",
                            event_type="FROZEN",
                            previous_state=state,
                            next_state="FROZEN",
                            candidate_id=candidate_id,
                            package_hash=PACKAGE_A,
                            deployment_identity_hash=DEPLOYMENT_A,
                            evidence_references=(f"fixture://refresh/{state.lower()}/same",),
                            timestamp=BASE_TIME + timedelta(seconds=10),
                        )
                    )
                Registrar(ledger, "registrar-1").append(
                    event(
                        event_id=f"refresh-{state.lower()}-record",
                        event_type="FROZEN",
                        previous_state=state,
                        next_state="FROZEN",
                        candidate_id=candidate_id,
                        package_hash=PACKAGE_A,
                        deployment_identity_hash=DEPLOYMENT_B,
                        evidence_references=(f"fixture://refresh/{state.lower()}",),
                        timestamp=BASE_TIME + timedelta(seconds=11),
                    )
                )
                refreshed = ledger.current_state(candidate_id)
                self.assertEqual(observed_state(refreshed), "FROZEN")
                self.assertEqual(refreshed["deployment_identity_hash"], DEPLOYMENT_B)

        suspended = self.new_ledger("deployment-refresh-suspended")
        suspended_candidate = "QLC-20260913-refresh-suspended"
        self.build_to_rung(
            suspended,
            suspended_candidate,
            "refresh-suspended",
            "SHADOW_ELIGIBLE",
        )
        self.append_authority_event(
            suspended,
            candidate_id=suspended_candidate,
            event_id="refresh-suspended-record",
            event_type="SUSPENDED",
            previous_state="SHADOW",
            next_state="SUSPENDED",
            writer_class="MULTI_WORKER_SUPERVISOR",
            writer_id="supervisor-1",
            check_set_version="supervisor.v1",
            offset=5,
        )
        with self.subTest(state="SUSPENDED"):
            with self.assertRaisesRegex(ValueError, "DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED"):
                self.append_authority_event(
                    suspended,
                    candidate_id=suspended_candidate,
                    event_id="refresh-suspended-authority-attempt",
                    event_type="RESUMED",
                    previous_state="SUSPENDED",
                    next_state="SHADOW",
                    writer_class="MULTI_WORKER_SUPERVISOR",
                    writer_id="supervisor-1",
                    check_set_version="supervisor.v1",
                    deployment_identity_hash=DEPLOYMENT_B,
                    offset=6,
                )
            Registrar(suspended, "registrar-1").append(
                event(
                    event_id="refresh-suspended-recorded",
                    event_type="FROZEN",
                    previous_state="SUSPENDED",
                    next_state="FROZEN",
                    candidate_id=suspended_candidate,
                    package_hash=PACKAGE_A,
                    deployment_identity_hash=DEPLOYMENT_B,
                    evidence_references=("fixture://refresh/suspended",),
                    timestamp=BASE_TIME + timedelta(seconds=7),
                )
            )
            self.assertEqual(
                observed_state(suspended.current_state(suspended_candidate)), "FROZEN"
            )
            with self.assertRaisesRegex(
                ValueError, "RESUME_TARGET_RUNG_MISMATCH|PREVIOUS_STATE_MISMATCH"
            ):
                self.append_authority_event(
                    suspended,
                    candidate_id=suspended_candidate,
                    event_id="refresh-suspended-attempt",
                    event_type="RESUMED",
                    previous_state="SUSPENDED",
                    next_state="SHADOW",
                    writer_class="MULTI_WORKER_SUPERVISOR",
                    writer_id="supervisor-1",
                    check_set_version="supervisor.v1",
                    deployment_identity_hash=DEPLOYMENT_B,
                    offset=6,
                )

    def test_candidate_timestamp_must_be_monotonic_on_append_and_reads(self) -> None:
        append_candidate = "QLC-20260913-timestamp-append"
        self.append_capture(candidate_id=append_candidate, event_id="timestamp-append-capture")
        with self.subTest(seam="append"):
            with self.assertRaisesRegex(ValueError, "TIMESTAMP_NOT_MONOTONIC"):
                Registrar(self.ledger, "registrar-1").append(
                    event(
                        event_id="timestamp-append-triaged",
                        event_type="TRIAGED",
                        previous_state="CAPTURED",
                        next_state="TRIAGED",
                        candidate_id=append_candidate,
                        timestamp=BASE_TIME - timedelta(days=365),
                    ),
                    check_set_version="worthiness.v1",
                )

        historic = self.new_ledger("timestamp-history")
        historic_candidate = "QLC-20260913-timestamp-history"
        Registrar(historic, "registrar-1").append(
            event(event_id="timestamp-history-capture", candidate_id=historic_candidate)
        )
        historic_event = event(
            event_id="timestamp-history-triaged",
            event_type="TRIAGED",
            previous_state="CAPTURED",
            next_state="TRIAGED",
            candidate_id=historic_candidate,
            timestamp=BASE_TIME - timedelta(days=365),
        )
        event_bytes = json.dumps(
            historic_event.model_dump(mode="json"),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        evidence_bytes = json.dumps(
            {
                "check_set_purpose": "worthiness",
                "check_set_version": "worthiness.v1",
                "evaluation_run_hash": None,
                "failing_checks": [],
                "catalog_backed": False,
                "source_kind": "FIXTURE",
            },
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        connection = sqlite3.connect(historic.path)
        try:
            previous_digest = connection.execute(
                "SELECT digest FROM lifecycle_events WHERE global_sequence = 1"
            ).fetchone()[0]
            digest = hashlib.sha256(
                previous_digest.encode("ascii")
                + b"\n"
                + event_bytes
                + b"\n"
                + evidence_bytes
            ).hexdigest()
            connection.execute(
                "INSERT INTO lifecycle_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    2,
                    historic_event.event_id,
                    historic_event.writer_class.value,
                    historic_event.writer_id,
                    2,
                    historic_event.candidate_id,
                    event_bytes,
                    evidence_bytes,
                    previous_digest,
                    digest,
                ),
            )
            connection.execute(
                "UPDATE lifecycle_current SET current_state = 'TRIAGED', last_sequence = 2 "
                "WHERE candidate_id = ?",
                (historic_candidate,),
            )
            connection.commit()
        finally:
            connection.close()
        backup_path = Path(self.temp_dir.name) / "timestamp-history-backup.sqlite"
        operations = {
            "replay": historic.replay,
            "integrity": historic.verify_integrity,
            "current": lambda: historic.current_state(historic_candidate),
            "report": historic.render_status_report,
            "backup": lambda: historic.backup_to(backup_path),
        }
        for seam, operation in operations.items():
            with self.subTest(seam=seam):
                with self.assertRaisesRegex(ValueError, "TIMESTAMP_NOT_MONOTONIC"):
                    operation()

        equal = self.new_ledger("timestamp-equal")
        equal_candidate = "QLC-20260913-timestamp-equal"
        Registrar(equal, "registrar-1").append(
            event(event_id="timestamp-equal-capture", candidate_id=equal_candidate)
        )
        Registrar(equal, "registrar-1").append(
            event(
                event_id="timestamp-equal-triaged",
                event_type="TRIAGED",
                previous_state="CAPTURED",
                next_state="TRIAGED",
                candidate_id=equal_candidate,
                timestamp=BASE_TIME,
            ),
            check_set_version="worthiness.v1",
        )

    def test_external_writer_checkpoint_is_a_minimum(self) -> None:
        self.append_capture()
        self.registrar.append(
            event(
                event_id="checkpoint-triaged",
                event_type="TRIAGED",
                previous_state="CAPTURED",
                next_state="TRIAGED",
                timestamp=BASE_TIME + timedelta(seconds=1),
            ),
            check_set_version="worthiness.v1",
        )

        self.ledger.verify_integrity(
            expected_writer_sequences={("REGISTRAR", "registrar-1"): 1}
        )
        self.ledger.verify_integrity(
            expected_writer_sequences={("REGISTRAR", "registrar-1"): 2}
        )
        with self.assertRaisesRegex(ValueError, "WRITER_CHECKPOINT_GAP"):
            self.ledger.verify_integrity(
                expected_writer_sequences={("REGISTRAR", "registrar-1"): 3}
            )

    def test_external_writer_checkpoint_requires_non_negative_plain_integer(self) -> None:
        self.append_capture()
        invalid_checkpoints = (
            ("nan", float("nan")),
            ("fractional", 1.5),
            ("negative", -1),
            ("boolean", True),
            ("string", "1"),
        )
        for label, expected in invalid_checkpoints:
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, "WRITER_CHECKPOINT_INVALID"):
                    self.ledger.verify_integrity(
                        expected_writer_sequences={
                            ("REGISTRAR", "registrar-1"): expected
                        }
                    )

        self.ledger.verify_integrity(
            expected_writer_sequences={("REGISTRAR", "registrar-1"): 0}
        )
        self.ledger.verify_integrity(
            expected_writer_sequences={("REGISTRAR", "registrar-1"): 1}
        )
        with self.assertRaisesRegex(ValueError, "WRITER_CHECKPOINT_GAP"):
            self.ledger.verify_integrity(
                expected_writer_sequences={("REGISTRAR", "registrar-1"): 2}
            )

    def test_external_writer_checkpoints_are_snapshotted_once(self) -> None:
        self.append_capture()
        writer_pair = ("REGISTRAR", "registrar-1")

        class ChangingCheckpoints(dict[tuple[str, str], Any]):
            def __init__(self) -> None:
                super().__init__({writer_pair: 1})
                self.view_count = 0

            def _next_expected(self) -> Any:
                self.view_count += 1
                expected = self[writer_pair]
                self[writer_pair] = float("nan")
                return expected

            def values(self) -> tuple[Any]:
                return (self._next_expected(),)

            def items(self) -> tuple[tuple[tuple[str, str], Any]]:
                return ((writer_pair, self._next_expected()),)

        checkpoints = ChangingCheckpoints()
        self.ledger.verify_integrity(expected_writer_sequences=checkpoints)

        self.assertEqual(checkpoints.view_count, 1)

    def test_external_writer_checkpoint_rejects_arbitrary_int_subclass(self) -> None:
        self.append_capture()

        class FalseGreenInt(int):
            def __lt__(self, other: object) -> bool:
                return False

            def __gt__(self, other: object) -> bool:
                return False

        with self.assertRaisesRegex(ValueError, "WRITER_CHECKPOINT_INVALID"):
            self.ledger.verify_integrity(
                expected_writer_sequences={
                    ("REGISTRAR", "registrar-1"): FalseGreenInt(2)
                }
            )

    def test_writer_allowlist_rejects_malformed_and_subclass_identifiers(self) -> None:
        class RegistrarString(str):
            def __str__(self) -> str:
                return "REGISTRAR"

        class WriterIdString(str):
            def __str__(self) -> str:
                return "registrar-1"

        class WriterPairTuple(tuple):
            pass

        invalid_entries = (
            (RegistrarString("ATTACKER"), "registrar-1"),
            ("REGISTRAR", WriterIdString("attacker")),
            ["REGISTRAR", "registrar-1"],
            WriterPairTuple(("REGISTRAR", "registrar-1")),
            ("REGISTRAR", "registrar-1", "ignored"),
            ("", "registrar-1"),
            ("REGISTRAR", ""),
        )
        for index, entry in enumerate(invalid_entries):
            with self.subTest(index=index):
                with self.assertRaisesRegex(ValueError, "WRITER_ALLOWLIST_INVALID"):
                    LifecycleLedger(
                        Path(self.temp_dir.name) / f"invalid-writer-{index}.sqlite",
                        (entry,),
                        active_check_sets=ACTIVE_CHECK_SETS,
                    )

        LifecycleLedger(
            Path(self.temp_dir.name) / "enum-writer.sqlite",
            ((LifecycleWriterClass.REGISTRAR, "registrar-1"),),
            active_check_sets=ACTIVE_CHECK_SETS,
        )

    def test_active_check_sets_reject_str_subclass_identifiers(self) -> None:
        class PurposeString(str):
            def __str__(self) -> str:
                return "shadow_eligibility"

        class VersionString(str):
            pass

        invalid_registries = (
            (
                "purpose",
                {PurposeString("worthiness"): ("worthiness.v1",)},
                "CHECK_SET_PURPOSE_UNKNOWN",
            ),
            (
                "version",
                {"worthiness": (VersionString("worthiness.v1"),)},
                "CHECK_SET_VERSIONS_INVALID",
            ),
        )
        for label, registry, error in invalid_registries:
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, error):
                    LifecycleLedger(
                        Path(self.temp_dir.name) / f"invalid-check-set-{label}.sqlite",
                        ALLOWLIST,
                        active_check_sets=registry,
                    )

    def test_external_writer_checkpoint_rejects_malformed_keys(self) -> None:
        self.append_capture()

        class RegistrarString(str):
            def __str__(self) -> str:
                return "REGISTRAR"

        class WriterIdString(str):
            def __str__(self) -> str:
                return "registrar-1"

        class WriterPairTuple(tuple):
            pass

        invalid_keys = (
            ("REGISTRAR", "registrar-1", "ignored"),
            WriterPairTuple(("REGISTRAR", "registrar-1")),
            (RegistrarString("ATTACKER"), "registrar-1"),
            ("REGISTRAR", WriterIdString("attacker")),
            ("", "registrar-1"),
            ("REGISTRAR", ""),
        )
        for index, writer_pair in enumerate(invalid_keys):
            with self.subTest(index=index):
                with self.assertRaisesRegex(ValueError, "WRITER_CHECKPOINT_INVALID"):
                    self.ledger.verify_integrity(
                        expected_writer_sequences={writer_pair: 0}
                    )

        self.ledger.verify_integrity(
            expected_writer_sequences={
                (LifecycleWriterClass.REGISTRAR, "registrar-1"): 1
            }
        )

    def test_append_rejects_check_set_version_str_subclass_before_mutation(
        self,
    ) -> None:
        class CheckSetAlias(str):
            def __eq__(self, other: object) -> bool:
                return other == "worthiness.v1"

        self.append_capture()
        before = self.ledger.replay()
        with self.assertRaisesRegex(ValueError, "CHECK_SET_VERSION_INVALID"):
            self.registrar.append(
                event(
                    event_id="r17-check-set-version",
                    event_type="TRIAGED",
                    previous_state="CAPTURED",
                    next_state="TRIAGED",
                    timestamp=BASE_TIME + timedelta(seconds=1),
                ),
                check_set_version=CheckSetAlias("attacker-version"),
            )

        self.assertEqual(self.ledger.replay(), before)
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "CAPTURED")
        self.ledger.verify_integrity(expected_event_ids=("event-captured-a",))

    def test_append_rejects_evaluation_hash_str_subclass_before_mutation(
        self,
    ) -> None:
        class EvaluationHashString(str):
            pass

        self.append_to_frozen()
        before = self.ledger.replay()
        self.assertEqual(len(before), 4)
        with self.assertRaisesRegex(ValueError, "EVALUATION_RUN_HASH_INVALID"):
            self.append_authority_event(
                self.ledger,
                candidate_id=CANDIDATE_A,
                event_id="r17-evaluation-hash",
                event_type="SHADOW_ELIGIBLE",
                previous_state="FROZEN",
                next_state="SHADOW",
                writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                writer_id="admission-1",
                check_set_version="shadow-eligibility.v1",
                evaluation_run_hash=EvaluationHashString(EVALUATION_A),
            )

        self.assertEqual(self.ledger.replay(), before)
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "FROZEN")
        self.ledger.verify_integrity(
            expected_event_ids=(f"event-frozen-{CANDIDATE_A}",)
        )

    def test_append_rejects_source_kind_str_subclass_before_mutation(self) -> None:
        class SourceKindString(str):
            pass

        with self.assertRaisesRegex(ValueError, "SOURCE_KIND_NOT_FIXTURE"):
            self.registrar.append(
                event(event_id="r17-source-kind"),
                source_kind=SourceKindString("FIXTURE"),
            )

        self.assertEqual(self.ledger.replay(), [])
        self.ledger.verify_integrity()

    def test_append_rejects_failing_check_id_str_subclass_before_mutation(
        self,
    ) -> None:
        class CheckIdString(str):
            pass

        with self.assertRaisesRegex(ValueError, "FAILING_CHECKS_INVALID"):
            self.registrar.append(
                event(event_id="r17-check-id"),
                failing_checks=(
                    {
                        "check_id": CheckIdString("DSR"),
                        "observed_value": 0.42,
                        "threshold": ">=0.95",
                    },
                ),
            )

        self.assertEqual(self.ledger.replay(), [])
        self.ledger.verify_integrity()

    def test_expected_event_ids_are_snapshotted_and_exactly_validated(self) -> None:
        class EventIdString(str):
            pass

        class ChangingExpectedIds:
            def __init__(self) -> None:
                self.iterations = 0

            def __iter__(self) -> Any:
                self.iterations += 1
                if self.iterations == 1:
                    return iter((EventIdString("event-captured-a"),))
                return iter(("event-never-appended",))

        self.append_capture()
        changing = ChangingExpectedIds()
        with self.assertRaisesRegex(ValueError, "EXPECTED_EVENT_ID_INVALID"):
            self.ledger.verify_integrity(expected_event_ids=changing)
        self.assertEqual(changing.iterations, 1)

        invalid_inputs = (
            "event-captured-a",
            b"event-captured-a",
            bytearray(b"event-captured-a"),
            1,
            ("",),
        )
        for invalid in invalid_inputs:
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "EXPECTED_EVENT_ID_INVALID"):
                    self.ledger.verify_integrity(expected_event_ids=invalid)

        self.ledger.verify_integrity(expected_event_ids=("event-captured-a",))
        self.assertEqual(len(self.ledger.replay()), 1)

    def test_current_state_rejects_candidate_id_str_subclass_before_lookup(
        self,
    ) -> None:
        class CandidateIdString(str):
            pass

        self.append_capture()
        for invalid in (CandidateIdString(CANDIDATE_A), "", 1):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "CANDIDATE_ID_INVALID"):
                    self.ledger.current_state(invalid)

        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "CAPTURED")
        self.ledger.verify_integrity(expected_event_ids=("event-captured-a",))

    def test_registrar_rejects_writer_id_str_subclass_before_mutation(self) -> None:
        class WriterIdString(str):
            pass

        class EqualityAlias(str):
            def __eq__(self, other: object) -> bool:
                return other == "registrar-1"

            def __ne__(self, other: object) -> bool:
                return not self == other

        invalid_writer_ids = (
            WriterIdString("registrar-1"),
            EqualityAlias("attacker"),
            "",
            1,
        )
        for index, writer_id in enumerate(invalid_writer_ids):
            with self.subTest(index=index):
                ledger = self.new_ledger(f"r17-registrar-{index}")
                with self.assertRaisesRegex(ValueError, "REGISTRAR_AUTHORITY_REFUSED"):
                    Registrar(ledger, writer_id)
                self.assertEqual(ledger.replay(), [])
                ledger.verify_integrity()

        mutated = self.new_ledger("r17-registrar-mutated")
        registrar = Registrar(mutated, "registrar-1")
        registrar.writer_id = EqualityAlias("attacker")
        with self.assertRaisesRegex(ValueError, "REGISTRAR_AUTHORITY_REFUSED"):
            registrar.append(event(event_id="r17-registrar-mutated"))
        self.assertEqual(mutated.replay(), [])
        mutated.verify_integrity()

        valid = self.new_ledger("r17-registrar-valid")
        Registrar(valid, "registrar-1").append(event(event_id="r17-registrar-valid"))
        self.assertEqual(len(valid.replay()), 1)
        valid.verify_integrity(expected_event_ids=("r17-registrar-valid",))

    def test_datetime_utcoffset_override_is_refused_before_mutation(self) -> None:
        class SneakyDatetime(datetime):
            def utcoffset(self) -> timedelta:
                return timedelta(0)

        ledger = self.new_ledger("r18-datetime-utcoffset")
        candidate_id = "QLC-20260913-r18-datetime-utcoffset"
        sneaky = SneakyDatetime(
            2026,
            9,
            13,
            8,
            30,
            tzinfo=timezone(timedelta(hours=5)),
        )
        with self.assertRaisesRegex(ValueError, "TIMESTAMP_NOT_UTC"):
            Registrar(ledger, "registrar-1").append(
                event(
                    event_id="r18-datetime-utcoffset",
                    candidate_id=candidate_id,
                    timestamp=sneaky,
                )
            )
        self.assertEqual(ledger.replay(), [])
        self.assertIsNone(ledger.current_state(candidate_id))
        ledger.verify_integrity()

        plain = self.new_ledger("r18-plain-non-utc")
        with self.assertRaisesRegex(ValueError, "TIMESTAMP_NOT_UTC"):
            Registrar(plain, "registrar-1").append(
                event(
                    event_id="r18-plain-non-utc",
                    candidate_id="QLC-20260913-r18-plain-non-utc",
                    timestamp=datetime(
                        2026,
                        9,
                        13,
                        8,
                        30,
                        tzinfo=timezone(timedelta(hours=5)),
                    ),
                )
            )
        self.assertEqual(plain.replay(), [])
        plain.verify_integrity()

        valid = self.new_ledger("r18-valid-utc")
        Registrar(valid, "registrar-1").append(
            event(
                event_id="r18-valid-utc",
                candidate_id="QLC-20260913-r18-valid-utc",
                timestamp=BASE_TIME,
            )
        )
        self.assertEqual(len(valid.replay()), 1)
        valid.verify_integrity(expected_event_ids=("r18-valid-utc",))

    def test_stateful_plain_timezone_is_refused_before_mutation(self) -> None:
        class StatefulTimezone(tzinfo):
            def __init__(self) -> None:
                self.calls = 0

            def utcoffset(self, value: datetime | None) -> timedelta:
                del value
                self.calls += 1
                return timedelta(0) if self.calls <= 3 else timedelta(hours=7)

            def dst(self, value: datetime | None) -> timedelta:
                del value
                return timedelta(0)

        ledger = self.new_ledger("r18-stateful-timezone")
        candidate_id = "QLC-20260913-r18-stateful-timezone"
        stateful = StatefulTimezone()
        timestamp = datetime(2026, 9, 13, 8, 30, tzinfo=stateful)
        with self.assertRaisesRegex(ValueError, "TIMESTAMP_NOT_UTC"):
            Registrar(ledger, "registrar-1").append(
                event(
                    event_id="r18-stateful-timezone",
                    candidate_id=candidate_id,
                    timestamp=timestamp,
                )
            )
        self.assertEqual(stateful.calls, 4)
        self.assertEqual(ledger.replay(), [])
        self.assertIsNone(ledger.current_state(candidate_id))
        ledger.verify_integrity()

    def test_datetime_lt_override_is_refused_before_mutation(self) -> None:
        class NeverEarlier(datetime):
            def __lt__(self, other: object) -> bool:
                del other
                return False

        candidate_id = "QLC-20260913-r18-datetime-lt"
        ledger = self.new_ledger("r18-datetime-lt")
        registrar = Registrar(ledger, "registrar-1")
        registrar.append(
            event(
                event_id="r18-datetime-lt-captured",
                candidate_id=candidate_id,
                timestamp=BASE_TIME,
            )
        )
        before = ledger.replay()
        with self.assertRaisesRegex(ValueError, "TIMESTAMP_NOT_MONOTONIC"):
            registrar.append(
                event(
                    event_id="r18-datetime-lt-triaged",
                    event_type="TRIAGED",
                    previous_state="CAPTURED",
                    next_state="TRIAGED",
                    candidate_id=candidate_id,
                    timestamp=NeverEarlier(2026, 9, 12, 7, 30, tzinfo=UTC),
                ),
                check_set_version="worthiness.v1",
            )
        self.assertEqual(ledger.replay(), before)
        self.assertEqual(observed_state(ledger.current_state(candidate_id)), "CAPTURED")
        ledger.verify_integrity(expected_event_ids=("r18-datetime-lt-captured",))

        control = self.new_ledger("r18-plain-backdated")
        control_registrar = Registrar(control, "registrar-1")
        control_registrar.append(
            event(
                event_id="r18-plain-backdated-captured",
                candidate_id=candidate_id,
                timestamp=BASE_TIME,
            )
        )
        with self.assertRaisesRegex(ValueError, "TIMESTAMP_NOT_MONOTONIC"):
            control_registrar.append(
                event(
                    event_id="r18-plain-backdated-triaged",
                    event_type="TRIAGED",
                    previous_state="CAPTURED",
                    next_state="TRIAGED",
                    candidate_id=candidate_id,
                    timestamp=BASE_TIME - timedelta(hours=1),
                ),
                check_set_version="worthiness.v1",
            )
        self.assertEqual(len(control.replay()), 1)
        control.verify_integrity(
            expected_event_ids=("r18-plain-backdated-captured",)
        )

    def test_registrar_normalizes_event_writer_id_before_comparison(self) -> None:
        class WriterEqualityAlias(str):
            def __eq__(self, other: object) -> bool:
                del other
                return True

            def __ne__(self, other: object) -> bool:
                del other
                return False

        for route in ("object-setattr", "model-construct"):
            with self.subTest(route=route):
                ledger = self.new_ledger(f"r18-event-writer-{route}")
                malicious = event(event_id=f"r18-event-writer-{route}")
                alias = WriterEqualityAlias("registrar-2")
                if route == "object-setattr":
                    object.__setattr__(malicious, "writer_id", alias)
                else:
                    values = malicious.model_dump(mode="python")
                    values["writer_id"] = alias
                    malicious = LifecycleEvent.model_construct(**values)
                with self.assertRaisesRegex(
                    ValueError, "REGISTRAR_AUTHORITY_REFUSED"
                ):
                    Registrar(ledger, "registrar-1").append(malicious)
                self.assertEqual(ledger.replay(), [])
                ledger.verify_integrity()

        valid = self.new_ledger("r18-event-writer-valid")
        Registrar(valid, "registrar-1").append(
            event(event_id="r18-event-writer-valid")
        )
        records = valid.replay()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].event.writer_id, "registrar-1")
        valid.verify_integrity(
            expected_writer_sequences={("REGISTRAR", "registrar-1"): 1}
        )

    def test_non_mapping_writer_checkpoints_have_stable_refusal(self) -> None:
        self.append_capture()
        with self.assertRaisesRegex(ValueError, "WRITER_CHECKPOINT_INVALID"):
            self.ledger.verify_integrity(
                expected_writer_sequences=(("REGISTRAR", "registrar-1"), 1)
            )
        self.ledger.verify_integrity(expected_event_ids=("event-captured-a",))
        self.assertEqual(len(self.ledger.replay()), 1)

    def test_malformed_writer_checkpoint_items_have_stable_refusal(self) -> None:
        writer_pair = ("REGISTRAR", "registrar-1")

        class RaisingItems(Mapping[tuple[str, str], int]):
            def __iter__(self) -> Any:
                return iter((writer_pair,))

            def __len__(self) -> int:
                return 1

            def __getitem__(self, key: tuple[str, str]) -> int:
                return 1

            def items(self) -> Any:
                raise KeyError(writer_pair)

        class NonPairItems(Mapping[tuple[str, str], int]):
            def __iter__(self) -> Any:
                return iter((writer_pair,))

            def __len__(self) -> int:
                return 1

            def __getitem__(self, key: tuple[str, str]) -> int:
                return 1

            def items(self) -> Any:
                return ((writer_pair, 1, "unexpected"),)

        self.append_capture()
        for label, checkpoints in (
            ("items-exception", RaisingItems()),
            ("non-pair-item", NonPairItems()),
        ):
            with self.subTest(label=label):
                with self.assertRaisesRegex(
                    ValueError, "WRITER_CHECKPOINT_INVALID"
                ):
                    self.ledger.verify_integrity(
                        expected_writer_sequences=checkpoints
                    )

        self.ledger.verify_integrity(expected_event_ids=("event-captured-a",))
        self.assertEqual(len(self.ledger.replay()), 1)

    def test_inconsistent_failing_check_mapping_has_stable_refusal(self) -> None:
        class InconsistentCheck(Mapping[str, Any]):
            def __iter__(self) -> Any:
                return iter(("check_id", "observed_value", "threshold"))

            def __len__(self) -> int:
                return 3

            def __getitem__(self, key: str) -> Any:
                if key == "check_id":
                    raise KeyError(key)
                return 0.42 if key == "observed_value" else ">=0.95"

        with self.assertRaisesRegex(ValueError, "FAILING_CHECKS_INVALID"):
            self.registrar.append(
                event(event_id="r18-inconsistent-check"),
                failing_checks=(InconsistentCheck(),),
            )
        self.assertEqual(self.ledger.replay(), [])
        self.ledger.verify_integrity()

    def test_append_refuses_derived_view_drift_until_explicit_rebuild(self) -> None:
        self.append_capture()
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                "UPDATE lifecycle_current SET current_state = 'TRIAGED' "
                "WHERE candidate_id = ?",
                (CANDIDATE_A,),
            )
            connection.commit()
        finally:
            connection.close()
        triaged = event(
            event_id="derived-drift-triaged",
            event_type="TRIAGED",
            previous_state="CAPTURED",
            next_state="TRIAGED",
            timestamp=BASE_TIME + timedelta(seconds=1),
        )

        with self.assertRaisesRegex(ValueError, "DERIVED_VIEW_DRIFT"):
            self.registrar.append(triaged, check_set_version="worthiness.v1")
        self.assertEqual(len(self.ledger.replay()), 1)
        connection = sqlite3.connect(self.db_path)
        try:
            drifted_state = connection.execute(
                "SELECT current_state FROM lifecycle_current WHERE candidate_id = ?",
                (CANDIDATE_A,),
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(drifted_state, "TRIAGED")

        self.ledger.rebuild_current_view()
        self.registrar.append(triaged, check_set_version="worthiness.v1")
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_A)), "TRIAGED")

    def test_accepted_lifecycle_matrix_is_explicit_and_identity_preserving(self) -> None:
        paper_ledger = self.new_ledger("paper-matrix")
        paper_candidate = "QLC-20260912-paper-matrix"
        self.build_to_rung(
            paper_ledger,
            paper_candidate,
            "paper-matrix",
            "PAPER_ELIGIBLE",
            include_paper=True,
        )
        self.append_authority_event(
            paper_ledger,
            candidate_id=paper_candidate,
            event_id="paper-matrix-testnet",
            event_type="TESTNET_ELIGIBLE",
            previous_state="SHADOW",
            next_state="TESTNET",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="testnet-eligibility.v1",
            offset=6,
        )
        self.assertEqual(
            observed_state(paper_ledger.current_state(paper_candidate)),
            "TESTNET",
        )

        direct_ledger = self.new_ledger("direct-testnet-matrix")
        direct_candidate = "QLC-20260912-direct-testnet"
        self.build_to_rung(
            direct_ledger,
            direct_candidate,
            "direct-testnet",
            "TESTNET_ELIGIBLE",
        )
        self.assertEqual(
            observed_state(direct_ledger.current_state(direct_candidate)),
            "TESTNET",
        )

        capacity_ledger = self.new_ledger("withheld-before-admission")
        capacity_candidate = "QLC-20260912-withheld-before-admission"
        self.append_frozen_fixture(
            capacity_ledger,
            capacity_candidate,
            "withheld-before-admission",
        )
        self.append_authority_event(
            capacity_ledger,
            candidate_id=capacity_candidate,
            event_id="withheld-before-admission-record",
            event_type="ADMISSION_WITHHELD_CAPACITY",
            previous_state="FROZEN",
            next_state="FROZEN",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="shadow-eligibility.v1",
            offset=4,
        )
        self.assertEqual(
            observed_state(capacity_ledger.current_state(capacity_candidate)), "FROZEN"
        )
        self.assertEqual(
            capacity_ledger.replay()[-1].event_type,
            "ADMISSION_WITHHELD_CAPACITY",
        )

        for build_target, rung in (
            ("SHADOW_ELIGIBLE", "SHADOW"),
            ("TESTNET_ELIGIBLE", "TESTNET"),
            ("LIVE_CANDIDATE", "LIVE_CANDIDATE"),
            ("PROMOTED", "LIVE"),
        ):
            with self.subTest(suspend_resume_rung=rung):
                ledger = self.new_ledger(f"resume-{rung.lower()}")
                candidate_id = f"QLC-20260912-resume-{rung.lower()}"
                self.build_to_rung(
                    ledger,
                    candidate_id,
                    f"resume-{rung.lower()}",
                    build_target,
                )
                self.append_authority_event(
                    ledger,
                    candidate_id=candidate_id,
                    event_id=f"resume-{rung.lower()}-suspended",
                    event_type="SUSPENDED",
                    previous_state=rung,
                    next_state="SUSPENDED",
                    writer_class="MULTI_WORKER_SUPERVISOR",
                    writer_id="supervisor-1",
                    check_set_version="supervisor.v1",
                    offset=9,
                )
                live_resume = rung == "LIVE"
                self.append_authority_event(
                    ledger,
                    candidate_id=candidate_id,
                    event_id=f"resume-{rung.lower()}-resumed",
                    event_type="RESUMED",
                    previous_state="SUSPENDED",
                    next_state=rung,
                    writer_class=(
                        "PROMOTION_AUTHORITY"
                        if live_resume
                        else "MULTI_WORKER_SUPERVISOR"
                    ),
                    writer_id="promotion-1" if live_resume else "supervisor-1",
                    check_set_version="promotion.v1" if live_resume else "supervisor.v1",
                    offset=10,
                )
                state = ledger.current_state(candidate_id)
                self.assertEqual(observed_state(state), rung)
                self.assertEqual(state["package_hash"], PACKAGE_A)
                self.assertEqual(state["deployment_identity_hash"], DEPLOYMENT_A)

        retired_ledger = self.new_ledger("retired-terminal")
        retired_candidate = "QLC-20260912-retired-terminal"
        self.build_to_rung(
            retired_ledger,
            retired_candidate,
            "retired-terminal",
            "SHADOW_ELIGIBLE",
        )
        self.append_authority_event(
            retired_ledger,
            candidate_id=retired_candidate,
            event_id="retired-terminal-record",
            event_type="RETIRED",
            previous_state="SHADOW",
            next_state="RETIRED",
            writer_class="MULTI_WORKER_SUPERVISOR",
            writer_id="supervisor-1",
            check_set_version="supervisor.v1",
            offset=6,
        )
        with self.assertRaisesRegex(ValueError, "RETIRED_IDENTITY_TERMINAL"):
            self.append_authority_event(
                retired_ledger,
                candidate_id=retired_candidate,
                event_id="retired-terminal-reopen",
                event_type="SHADOW_ELIGIBLE",
                previous_state="RETIRED",
                next_state="SHADOW",
                writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                writer_id="admission-1",
                check_set_version="shadow-eligibility.v1",
                offset=7,
            )

    def test_deployment_identity_is_globally_bound_and_retired_identity_stays_terminal(
        self,
    ) -> None:
        for retired in (False, True):
            with self.subTest(retired=retired):
                ledger = self.new_ledger(f"deployment-binding-{retired}")
                first_candidate = f"QLC-20260912-deployment-owner-{retired}"
                second_candidate = f"QLC-20260912-deployment-reuser-{retired}"
                self.build_to_rung(
                    ledger,
                    first_candidate,
                    f"deployment-owner-{retired}",
                    "SHADOW_ELIGIBLE",
                )
                if retired:
                    self.append_authority_event(
                        ledger,
                        candidate_id=first_candidate,
                        event_id="deployment-owner-retired",
                        event_type="RETIRED",
                        previous_state="SHADOW",
                        next_state="RETIRED",
                        writer_class="MULTI_WORKER_SUPERVISOR",
                        writer_id="supervisor-1",
                        check_set_version="supervisor.v1",
                        offset=5,
                    )
                self.append_frozen_fixture(
                    ledger,
                    second_candidate,
                    f"deployment-reuser-{retired}",
                    package_hash=PACKAGE_B,
                )
                with self.assertRaisesRegex(
                    ValueError, "DEPLOYMENT.*(?:BOUND|RETIRED)"
                ):
                    self.append_authority_event(
                        ledger,
                        candidate_id=second_candidate,
                        event_id=f"deployment-reuse-{retired}",
                        event_type="SHADOW_ELIGIBLE",
                        previous_state="FROZEN",
                        next_state="SHADOW",
                        writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                        writer_id="admission-1",
                        check_set_version="shadow-eligibility.v1",
                        package_hash=PACKAGE_B,
                        deployment_identity_hash=DEPLOYMENT_A,
                        offset=6,
                    )

    def test_retired_candidate_reenters_with_new_package_but_not_retired_deployment(
        self,
    ) -> None:
        ledger = self.new_ledger("retired-candidate-reentry")
        candidate_id = "QLC-20260912-retired-candidate-reentry"
        self.build_to_rung(
            ledger, candidate_id, "retired-candidate-reentry", "SHADOW_ELIGIBLE"
        )
        self.append_authority_event(
            ledger,
            candidate_id=candidate_id,
            event_id="retired-candidate-record",
            event_type="RETIRED",
            previous_state="SHADOW",
            next_state="RETIRED",
            writer_class="MULTI_WORKER_SUPERVISOR",
            writer_id="supervisor-1",
            check_set_version="supervisor.v1",
            offset=5,
        )

        registrar = Registrar(ledger, "registrar-1")
        registrar.append(
            event(
                event_id="retired-candidate-reentry-record",
                event_type="RE_ENTRY",
                previous_state="RETIRED",
                next_state="CANDIDATE",
                candidate_id=candidate_id,
                reason="Exchange rules materially changed.",
                trigger="OWNER_EXTERNAL_CHANGE",
                evidence_references=("fixture://retired/reentry/fresh",),
                timestamp=BASE_TIME + timedelta(seconds=6),
            ),
            evaluation_run_hash=EVALUATION_B,
        )
        reentered = ledger.current_state(candidate_id)
        self.assertEqual(observed_state(reentered), "CANDIDATE")
        self.assertIsNone(reentered["package_hash"])
        self.assertIsNone(reentered["deployment_identity_hash"])

        registrar.append(
            event(
                event_id="retired-candidate-refrozen",
                event_type="FROZEN",
                previous_state="CANDIDATE",
                next_state="FROZEN",
                candidate_id=candidate_id,
                package_hash=PACKAGE_B,
                evidence_references=("fixture://retired/refrozen/new-package",),
                timestamp=BASE_TIME + timedelta(seconds=7),
            )
        )
        with self.assertRaisesRegex(ValueError, "DEPLOYMENT.*RETIRED"):
            self.append_authority_event(
                ledger,
                candidate_id=candidate_id,
                event_id="retired-deployment-refused",
                event_type="SHADOW_ELIGIBLE",
                previous_state="FROZEN",
                next_state="SHADOW",
                writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
                writer_id="admission-1",
                check_set_version="shadow-eligibility.v1",
                package_hash=PACKAGE_B,
                deployment_identity_hash=DEPLOYMENT_A,
                offset=8,
            )
        self.append_authority_event(
            ledger,
            candidate_id=candidate_id,
            event_id="new-deployment-accepted",
            event_type="SHADOW_ELIGIBLE",
            previous_state="FROZEN",
            next_state="SHADOW",
            writer_class="ENVIRONMENT_ADMISSION_AUTHORITY",
            writer_id="admission-1",
            check_set_version="shadow-eligibility.v1",
            package_hash=PACKAGE_B,
            deployment_identity_hash=DEPLOYMENT_B,
            offset=9,
        )
        state = ledger.current_state(candidate_id)
        self.assertEqual(state["package_hash"], PACKAGE_B)
        self.assertEqual(state["deployment_identity_hash"], DEPLOYMENT_B)

    def test_retired_reentry_requires_owner_external_change_reason(self) -> None:
        ledger = self.new_ledger("retired-reentry-trigger")
        candidate_id = "QLC-20260913-retired-trigger"
        self.build_to_rung(ledger, candidate_id, "retired-trigger", "SHADOW_ELIGIBLE")
        self.append_authority_event(
            ledger,
            candidate_id=candidate_id,
            event_id="retired-trigger-record",
            event_type="RETIRED",
            previous_state="SHADOW",
            next_state="RETIRED",
            writer_class="MULTI_WORKER_SUPERVISOR",
            writer_id="supervisor-1",
            check_set_version="supervisor.v1",
            offset=5,
        )
        registrar = Registrar(ledger, "registrar-1")
        for label, trigger, reason in (
            ("ordinary-trigger", "NEW_DATA_REGIME", "New data exists."),
            ("not-one-sentence", "OWNER_EXTERNAL_CHANGE", "One. Two."),
        ):
            with self.subTest(label=label):
                with self.assertRaisesRegex(
                    ValueError, "RETIRED_REENTRY_EXTERNAL_CHANGE_REASON_REQUIRED"
                ):
                    registrar.append(
                        event(
                            event_id=f"retired-reentry-{label}",
                            event_type="RE_ENTRY",
                            previous_state="RETIRED",
                            next_state="CANDIDATE",
                            candidate_id=candidate_id,
                            reason=reason,
                            trigger=trigger,
                            evidence_references=(f"fixture://retired/{label}",),
                            timestamp=BASE_TIME + timedelta(seconds=6),
                        ),
                        evaluation_run_hash=hashlib.sha256(label.encode()).hexdigest(),
                    )

        parked = self.new_ledger("owner-external-nonretired")
        parked_candidate = "QLC-20260913-owner-external-nonretired"
        self.append_candidate_fixture(
            parked, parked_candidate, "owner-external-nonretired"
        )
        Registrar(parked, "registrar-1").append(
            event(
                event_id="owner-external-nonretired-parked",
                event_type="PARKED",
                previous_state="CANDIDATE",
                next_state="PARKED",
                candidate_id=parked_candidate,
                timestamp=BASE_TIME + timedelta(seconds=3),
            )
        )
        with self.assertRaisesRegex(ValueError, "REENTRY_TRIGGER_INVALID"):
            Registrar(parked, "registrar-1").append(
                event(
                    event_id="owner-external-nonretired-reentry",
                    event_type="RE_ENTRY",
                    previous_state="PARKED",
                    next_state="CANDIDATE",
                    candidate_id=parked_candidate,
                    reason="External rule changed.",
                    trigger="OWNER_EXTERNAL_CHANGE",
                    evidence_references=("fixture://owner-external/nonretired",),
                    timestamp=BASE_TIME + timedelta(seconds=4),
                ),
                evaluation_run_hash=EVALUATION_B,
            )

    def test_second_promoted_candidate_requires_atomic_succession_envelope(self) -> None:
        ledger = self.new_ledger("second-promotion")
        self.build_to_rung(
            ledger,
            CANDIDATE_A,
            "first-promoted-candidate",
            "PROMOTED",
        )
        self.build_to_rung(
            ledger,
            CANDIDATE_B,
            "second-live-candidate",
            "LIVE_CANDIDATE",
            package_hash=PACKAGE_B,
            deployment_identity_hash=DEPLOYMENT_B,
        )
        with self.assertRaisesRegex(
            ValueError, "SUCCESSION_ENVELOPE_UNRESOLVED"
        ):
            self.append_authority_event(
                ledger,
                candidate_id=CANDIDATE_B,
                event_id="second-candidate-promoted",
                event_type="PROMOTED",
                previous_state="LIVE_CANDIDATE",
                next_state="LIVE",
                writer_class="PROMOTION_AUTHORITY",
                writer_id="promotion-1",
                check_set_version="promotion.v1",
                package_hash=PACKAGE_B,
                deployment_identity_hash=DEPLOYMENT_B,
                offset=8,
            )

        self.append_authority_event(
            ledger,
            candidate_id=CANDIDATE_A,
            event_id="first-promoted-candidate-suspended",
            event_type="SUSPENDED",
            previous_state="LIVE",
            next_state="SUSPENDED",
            writer_class="MULTI_WORKER_SUPERVISOR",
            writer_id="supervisor-1",
            check_set_version="supervisor.v1",
            offset=9,
        )
        with self.assertRaisesRegex(
            ValueError, "SUCCESSION_ENVELOPE_UNRESOLVED"
        ):
            self.append_authority_event(
                ledger,
                candidate_id=CANDIDATE_B,
                event_id="second-candidate-promoted-while-first-suspended",
                event_type="PROMOTED",
                previous_state="LIVE_CANDIDATE",
                next_state="LIVE",
                writer_class="PROMOTION_AUTHORITY",
                writer_id="promotion-1",
                check_set_version="promotion.v1",
                package_hash=PACKAGE_B,
                deployment_identity_hash=DEPLOYMENT_B,
                offset=10,
            )

    def test_backup_and_restore_destination_races_preserve_foreign_owner(self) -> None:
        self.append_capture()
        restore_source = Path(self.temp_dir.name) / "race-restore-source.sqlite"
        self.ledger.backup_to(restore_source)
        original_verify = LifecycleLedger.verify_integrity

        for operation in ("backup", "restore"):
            with self.subTest(operation=operation):
                destination = Path(self.temp_dir.name) / f"race-{operation}.sqlite"
                foreign_created = False

                def verify_after_foreign_create(
                    ledger: LifecycleLedger, *args: Any, **kwargs: Any
                ) -> None:
                    nonlocal foreign_created
                    if not foreign_created:
                        foreign = sqlite3.connect(destination)
                        try:
                            foreign.execute(
                                "CREATE TABLE foreign_owner(marker TEXT NOT NULL)"
                            )
                            foreign.execute(
                                "INSERT INTO foreign_owner VALUES ('foreign-owner')"
                            )
                            foreign.commit()
                        finally:
                            foreign.close()
                        foreign_created = True
                    original_verify(ledger, *args, **kwargs)

                refusal: Exception | None = None
                with patch.object(
                    LifecycleLedger,
                    "verify_integrity",
                    new=verify_after_foreign_create,
                ):
                    try:
                        if operation == "backup":
                            self.ledger.backup_to(destination)
                        else:
                            LifecycleLedger.restore_from(
                                restore_source,
                                destination,
                                ALLOWLIST,
                                active_check_sets=ACTIVE_CHECK_SETS,
                            )
                    except (FileExistsError, ValueError) as exc:
                        refusal = exc

                marker = None
                foreign = sqlite3.connect(destination)
                try:
                    row = foreign.execute(
                        "SELECT marker FROM foreign_owner"
                    ).fetchone()
                    marker = None if row is None else row[0]
                except sqlite3.DatabaseError:
                    pass
                finally:
                    foreign.close()
                self.assertEqual(
                    (isinstance(refusal, (FileExistsError, ValueError)), marker),
                    (True, "foreign-owner"),
                )

    def test_replay_and_current_state_expose_fixture_non_authoritative_provenance(
        self,
    ) -> None:
        ledger = self.new_ledger("public-provenance")
        candidate_id = "QLC-20260912-public-provenance"
        self.build_to_rung(
            ledger, candidate_id, "public-provenance", "PROMOTED"
        )

        replayed = ledger.replay()
        promoted = [
            record
            for record in replayed
            if public_field(record, "event_type") == "PROMOTED"
        ]
        self.assertEqual(len(promoted), 1)
        for record in replayed:
            self.assertEqual(public_field(record, "source_kind"), "FIXTURE")
            self.assertIs(public_field(record, "authoritative"), False)

        state = ledger.current_state(candidate_id)
        self.assertEqual(observed_state(state), "LIVE")
        self.assertEqual(public_field(state, "source_kind"), "FIXTURE")
        self.assertIs(public_field(state, "authoritative"), False)

    def test_replay_record_copy_and_protocol_serialization_preserve_provenance(
        self,
    ) -> None:
        self.append_capture()
        record = self.ledger.replay()[0]

        copied = copy.deepcopy(record)
        self.assertIs(type(copied), LifecycleRecord)
        self.assertEqual(copied.event_id, record.event_id)
        self.assertEqual(copied.check_set_purpose, record.check_set_purpose)
        self.assertEqual(copied.check_set_version, record.check_set_version)
        self.assertEqual(copied.evaluation_run_hash, record.evaluation_run_hash)
        self.assertEqual(copied.failing_checks, record.failing_checks)
        self.assertEqual(copied.source_kind, "FIXTURE")
        self.assertIs(copied.authoritative, False)

        restored = pickle.loads(pickle.dumps(copied))
        self.assertIs(type(restored), LifecycleRecord)
        self.assertEqual(restored, record)
        self.assertEqual(
            restored.event.model_dump(mode="json"),
            record.event.model_dump(mode="json"),
        )
        self.assertEqual(restored.source_kind, "FIXTURE")
        self.assertIs(restored.authoritative, False)

    def test_failing_checks_require_canonical_complete_ordered_unique_records(
        self,
    ) -> None:
        malformed = {
            "bare-string": "DSR:observed=0.42;threshold=>=0.95",
            "unordered-set": {
                '{"check_id":"DSR","observed_value":0.42,"threshold":">=0.95"}',
                '{"check_id":"BH_FDR","observed_value":0.18,"threshold":"<=0.05"}',
            },
            "missing-check-id": (
                {"observed_value": 0.42, "threshold": ">=0.95"},
            ),
            "missing-observed": (
                {"check_id": "DSR", "threshold": ">=0.95"},
            ),
            "missing-threshold": (
                {"check_id": "DSR", "observed_value": 0.42},
            ),
            "empty-check-id": (
                {"check_id": "", "observed_value": 0.42, "threshold": ">=0.95"},
            ),
            "null-observed": (
                {"check_id": "DSR", "observed_value": None, "threshold": ">=0.95"},
            ),
            "null-threshold": (
                {"check_id": "DSR", "observed_value": 0.42, "threshold": None},
            ),
            "nonscalar-observed": (
                {"check_id": "DSR", "observed_value": [0.42], "threshold": ">=0.95"},
            ),
            "nonscalar-threshold": (
                {"check_id": "DSR", "observed_value": 0.42, "threshold": {"gte": 0.95}},
            ),
            "duplicate-check-id": (FAILING_CHECKS[0], dict(FAILING_CHECKS[0])),
        }
        for label, failing_checks in malformed.items():
            with self.subTest(label=label):
                ledger = self.new_ledger(f"malformed-check-{label}")
                candidate_id = f"QLC-20260912-malformed-{label}"
                self.append_candidate_fixture(
                    ledger, candidate_id, f"malformed-{label}"
                )
                with self.assertRaisesRegex(
                    ValueError, "FAILING_CHECKS"
                ):
                    Registrar(ledger, "registrar-1").append(
                        event(
                            event_id=f"malformed-{label}-rejected",
                            event_type="REJECTED",
                            previous_state="CANDIDATE",
                            next_state="REJECTED",
                            candidate_id=candidate_id,
                            timestamp=BASE_TIME + timedelta(seconds=3),
                        ),
                        check_set_version="worthiness.v1",
                        evaluation_run_hash=EVALUATION_A,
                        failing_checks=failing_checks,
                        check_set_purpose="worthiness",
                    )

        accepted = self.new_ledger("canonical-failing-checks")
        accepted_candidate = "QLC-20260912-canonical-failing-checks"
        self.append_candidate_fixture(
            accepted, accepted_candidate, "canonical-failing-checks"
        )
        Registrar(accepted, "registrar-1").append(
            event(
                event_id="canonical-failing-checks-rejected",
                event_type="REJECTED",
                previous_state="CANDIDATE",
                next_state="REJECTED",
                candidate_id=accepted_candidate,
                timestamp=BASE_TIME + timedelta(seconds=3),
            ),
            check_set_version="worthiness.v1",
            evaluation_run_hash=EVALUATION_A,
            failing_checks=FAILING_CHECKS,
            check_set_purpose="worthiness",
        )
        self.assertEqual(
            observed_state(accepted.current_state(accepted_candidate)), "REJECTED"
        )

    def test_report_uses_event_next_state_and_true_derived_current_state(self) -> None:
        self.append_to_frozen()
        decoded = json.loads(self.ledger.render_status_report())

        records = decoded["fixture_ledger_records"]
        self.assertEqual(
            [record["next_state"] for record in records],
            ["CAPTURED", "TRIAGED", "CANDIDATE", "FROZEN"],
        )
        self.assertTrue(all("current_state" not in record for record in records))

        derived_section = decoded["derived_current_state"]
        if isinstance(derived_section, list):
            matches = [
                record
                for record in derived_section
                if record.get("candidate_id") == CANDIDATE_A
            ]
            self.assertEqual(len(matches), 1)
            derived = matches[0]
        elif CANDIDATE_A in derived_section:
            derived = dict(derived_section[CANDIDATE_A])
            derived.setdefault("candidate_id", CANDIDATE_A)
        else:
            derived = derived_section

        materialized = self.ledger.current_state(CANDIDATE_A)
        for field in (
            "candidate_id",
            "current_state",
            "package_hash",
            "deployment_identity_hash",
            "last_sequence",
            "source_kind",
            "authoritative",
        ):
            with self.subTest(field=field):
                self.assertEqual(derived[field], materialized[field])
        self.assertEqual(derived["source_kind"], "FIXTURE")
        self.assertIs(derived["authoritative"], False)

    def test_check_set_version_is_bound_to_transition_purpose(self) -> None:
        wrong_path = Path(self.temp_dir.name) / "wrong-check-purpose.sqlite"
        wrong = LifecycleLedger(
            wrong_path,
            ALLOWLIST,
            active_check_sets={"promotion": ("promotion.v1",)},
        )
        wrong_registrar = Registrar(wrong, "registrar-1")
        wrong_registrar.append(
            event(
                event_id="wrong-purpose-captured",
                candidate_id="QLC-20260913-wrong-purpose",
            )
        )
        with self.assertRaises(ValueError):
            wrong_registrar.append(
                event(
                    event_id="wrong-purpose-triaged",
                    event_type="TRIAGED",
                    previous_state="CAPTURED",
                    next_state="TRIAGED",
                    candidate_id="QLC-20260913-wrong-purpose",
                    timestamp=BASE_TIME + timedelta(seconds=1),
                ),
                check_set_version="promotion.v1",
            )
        self.assertEqual(
            observed_state(wrong.current_state("QLC-20260913-wrong-purpose")),
            "CAPTURED",
        )

        correct_path = Path(self.temp_dir.name) / "correct-check-purpose.sqlite"
        correct = LifecycleLedger(
            correct_path,
            ALLOWLIST,
            active_check_sets={"worthiness": ("worthiness.v1",)},
        )
        correct_registrar = Registrar(correct, "registrar-1")
        correct_registrar.append(
            event(
                event_id="correct-purpose-captured",
                candidate_id="QLC-20260913-correct-purpose",
            )
        )
        correct_registrar.append(
            event(
                event_id="correct-purpose-triaged",
                event_type="TRIAGED",
                previous_state="CAPTURED",
                next_state="TRIAGED",
                candidate_id="QLC-20260913-correct-purpose",
                timestamp=BASE_TIME + timedelta(seconds=1),
            ),
            check_set_version="worthiness.v1",
        )
        self.assertEqual(
            observed_state(correct.current_state("QLC-20260913-correct-purpose")),
            "TRIAGED",
        )

    def test_retired_package_cannot_be_refrozen_after_reentry(self) -> None:
        def retired_then_reentered(name: str) -> tuple[LifecycleLedger, str, Registrar]:
            ledger = self.new_ledger(name)
            candidate_id = f"QLC-20260913-{name}"
            self.build_to_rung(ledger, candidate_id, name, "SHADOW_ELIGIBLE")
            self.append_authority_event(
                ledger,
                candidate_id=candidate_id,
                event_id=f"{name}-retired",
                event_type="RETIRED",
                previous_state="SHADOW",
                next_state="RETIRED",
                writer_class="MULTI_WORKER_SUPERVISOR",
                writer_id="supervisor-1",
                check_set_version="supervisor.v1",
                offset=5,
            )
            registrar = Registrar(ledger, "registrar-1")
            registrar.append(
                event(
                    event_id=f"{name}-reentry",
                    event_type="RE_ENTRY",
                    previous_state="RETIRED",
                    next_state="CANDIDATE",
                    candidate_id=candidate_id,
                    reason="Exchange rules materially changed.",
                    trigger="OWNER_EXTERNAL_CHANGE",
                    evidence_references=(f"fixture://{name}/fresh-evaluation",),
                    timestamp=BASE_TIME + timedelta(seconds=6),
                ),
                evaluation_run_hash=EVALUATION_B,
            )
            return ledger, candidate_id, registrar

        refused, refused_candidate, refused_registrar = retired_then_reentered(
            "retired-package-refused"
        )
        with self.assertRaisesRegex(ValueError, "RETIRED_PACKAGE"):
            refused_registrar.append(
                event(
                    event_id="retired-package-reused",
                    event_type="FROZEN",
                    previous_state="CANDIDATE",
                    next_state="FROZEN",
                    candidate_id=refused_candidate,
                    package_hash=PACKAGE_A,
                    timestamp=BASE_TIME + timedelta(seconds=7),
                )
            )

        accepted, accepted_candidate, accepted_registrar = retired_then_reentered(
            "new-package-accepted"
        )
        accepted_registrar.append(
            event(
                event_id="new-package-refrozen",
                event_type="FROZEN",
                previous_state="CANDIDATE",
                next_state="FROZEN",
                candidate_id=accepted_candidate,
                package_hash=PACKAGE_B,
                timestamp=BASE_TIME + timedelta(seconds=7),
            )
        )
        state = accepted.current_state(accepted_candidate)
        self.assertEqual(observed_state(state), "FROZEN")
        self.assertEqual(state["package_hash"], PACKAGE_B)

    def test_status_report_uses_one_snapshot_during_concurrent_append(self) -> None:
        self.append_capture()
        wal = sqlite3.connect(self.db_path)
        try:
            self.assertEqual(wal.execute("PRAGMA journal_mode=WAL").fetchone()[0], "wal")
        finally:
            wal.close()

        history_read = Event()
        append_committed = Event()
        real_connect = sqlite3.connect

        class HistoryCursor:
            def __init__(self, cursor: sqlite3.Cursor) -> None:
                self.cursor = cursor

            def fetchall(self) -> list[sqlite3.Row]:
                rows = self.cursor.fetchall()
                history_read.set()
                if not append_committed.wait(timeout=5):
                    raise AssertionError("concurrent append did not commit")
                return rows

            def __getattr__(self, name: str) -> Any:
                return getattr(self.cursor, name)

        class ReportConnection:
            def __init__(self, connection: sqlite3.Connection) -> None:
                object.__setattr__(self, "connection", connection)

            def __getattr__(self, name: str) -> Any:
                return getattr(self.connection, name)

            def __setattr__(self, name: str, value: Any) -> None:
                setattr(self.connection, name, value)

            def execute(self, statement: str, *args: Any) -> Any:
                cursor = self.connection.execute(statement, *args)
                if "SELECT canonical_event, canonical_evidence" in statement:
                    return HistoryCursor(cursor)
                return cursor

        def instrumented_connect(database: Any, *args: Any, **kwargs: Any) -> Any:
            connection = real_connect(database, *args, **kwargs)
            if kwargs.get("uri"):
                return ReportConnection(connection)
            return connection

        report_result: list[str] = []
        report_errors: list[BaseException] = []

        def render_report() -> None:
            try:
                report_result.append(self.ledger.render_status_report())
            except BaseException as exc:
                report_errors.append(exc)

        reporter = Thread(target=render_report, name="p031-r5-report", daemon=True)
        with patch(
            "p031_lifecycle_ledger.sqlite3.connect", side_effect=instrumented_connect
        ):
            reporter.start()
            try:
                self.assertTrue(history_read.wait(timeout=5))
                Registrar(self.ledger, "registrar-2").append(
                    event(
                        event_id="report-race-later-append",
                        writer_id="registrar-2",
                        candidate_id=CANDIDATE_B,
                        timestamp=BASE_TIME + timedelta(seconds=1),
                    )
                )
            finally:
                append_committed.set()
                reporter.join(timeout=5)

        self.assertFalse(reporter.is_alive())
        self.assertEqual(report_errors, [])
        self.assertEqual(len(report_result), 1)
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_B)), "CAPTURED")
        self.ledger.verify_integrity()

        report = json.loads(report_result[0])
        event_candidates = {
            record["candidate_id"] for record in report["fixture_ledger_records"]
        }
        state_candidates = {
            record["candidate_id"] for record in report["derived_current_state"]
        }
        self.assertEqual(event_candidates, {CANDIDATE_A})
        self.assertEqual(state_candidates, event_candidates)

    def test_current_state_does_not_return_an_unverified_second_snapshot(self) -> None:
        self.append_capture()
        wal = sqlite3.connect(self.db_path)
        try:
            self.assertEqual(wal.execute("PRAGMA journal_mode=WAL").fetchone()[0], "wal")
        finally:
            wal.close()

        mutation_committed = Event()
        real_connect = sqlite3.connect

        def tamper() -> None:
            if mutation_committed.is_set():
                return
            attacker = real_connect(self.db_path)
            try:
                attacker.execute(
                    "UPDATE lifecycle_current SET current_state = 'TRIAGED' "
                    "WHERE candidate_id = ?",
                    (CANDIDATE_A,),
                )
                attacker.commit()
            finally:
                attacker.close()
            mutation_committed.set()

        class CurrentViewCursor:
            def __init__(self, cursor: sqlite3.Cursor) -> None:
                self.cursor = cursor

            def fetchall(self) -> list[sqlite3.Row]:
                rows = self.cursor.fetchall()
                tamper()
                return rows

            def __iter__(self) -> Any:
                rows = list(self.cursor)
                tamper()
                return iter(rows)

            def __getattr__(self, name: str) -> Any:
                return getattr(self.cursor, name)

        class CurrentStateConnection:
            def __init__(self, connection: sqlite3.Connection) -> None:
                object.__setattr__(self, "connection", connection)

            def __getattr__(self, name: str) -> Any:
                return getattr(self.connection, name)

            def __setattr__(self, name: str, value: Any) -> None:
                setattr(self.connection, name, value)

            def execute(self, statement: str, *args: Any) -> Any:
                if (
                    "SELECT * FROM lifecycle_current WHERE candidate_id" in statement
                    and not mutation_committed.is_set()
                ):
                    tamper()
                cursor = self.connection.execute(statement, *args)
                if "SELECT * FROM lifecycle_current ORDER BY candidate_id" in statement:
                    return CurrentViewCursor(cursor)
                return cursor

        def instrumented_connect(database: Any, *args: Any, **kwargs: Any) -> Any:
            connection = real_connect(database, *args, **kwargs)
            if kwargs.get("uri"):
                return CurrentStateConnection(connection)
            return connection

        with patch(
            "p031_lifecycle_ledger.sqlite3.connect", side_effect=instrumented_connect
        ):
            state = self.ledger.current_state(CANDIDATE_A)

        self.assertTrue(mutation_committed.is_set())
        self.assertEqual(observed_state(state), "CAPTURED")

    def test_verify_integrity_uses_one_snapshot_during_concurrent_append(self) -> None:
        self.append_capture()
        wal = sqlite3.connect(self.db_path)
        try:
            self.assertEqual(wal.execute("PRAGMA journal_mode=WAL").fetchone()[0], "wal")
        finally:
            wal.close()

        history_read = Event()
        append_committed = Event()
        real_connect = sqlite3.connect

        class HistoryCursor:
            def __init__(self, cursor: sqlite3.Cursor) -> None:
                self.cursor = cursor

            def fetchall(self) -> list[sqlite3.Row]:
                rows = self.cursor.fetchall()
                history_read.set()
                if not append_committed.wait(timeout=5):
                    raise AssertionError("concurrent append did not commit")
                return rows

            def __getattr__(self, name: str) -> Any:
                return getattr(self.cursor, name)

        class VerifyConnection:
            def __init__(self, connection: sqlite3.Connection) -> None:
                object.__setattr__(self, "connection", connection)

            def __getattr__(self, name: str) -> Any:
                return getattr(self.connection, name)

            def __setattr__(self, name: str, value: Any) -> None:
                setattr(self.connection, name, value)

            def execute(self, statement: str, *args: Any) -> Any:
                cursor = self.connection.execute(statement, *args)
                if "SELECT * FROM lifecycle_events ORDER BY global_sequence" in statement:
                    return HistoryCursor(cursor)
                return cursor

        def instrumented_connect(database: Any, *args: Any, **kwargs: Any) -> Any:
            connection = real_connect(database, *args, **kwargs)
            if kwargs.get("uri"):
                return VerifyConnection(connection)
            return connection

        verify_errors: list[BaseException] = []

        def verify() -> None:
            try:
                self.ledger.verify_integrity()
            except BaseException as exc:
                verify_errors.append(exc)

        verifier = Thread(target=verify, name="p031-r6-verify", daemon=True)
        with patch(
            "p031_lifecycle_ledger.sqlite3.connect", side_effect=instrumented_connect
        ):
            verifier.start()
            try:
                self.assertTrue(history_read.wait(timeout=5))
                Registrar(self.ledger, "registrar-2").append(
                    event(
                        event_id="verify-race-later-append",
                        writer_id="registrar-2",
                        candidate_id=CANDIDATE_B,
                        timestamp=BASE_TIME + timedelta(seconds=1),
                    )
                )
            finally:
                append_committed.set()
                verifier.join(timeout=5)

        self.assertFalse(verifier.is_alive())
        self.assertEqual(verify_errors, [])
        self.assertEqual(observed_state(self.ledger.current_state(CANDIDATE_B)), "CAPTURED")
        self.ledger.verify_integrity()

    def test_purposeless_registrar_events_refuse_irrelevant_evidence(self) -> None:
        evidence_cases = (
            ("check-set", {"check_set_version": "promotion.v1"}, {}),
            ("evaluation", {"evaluation_run_hash": EVALUATION_A}, {}),
            ("trigger", {}, {"trigger": "NEW_DATA_REGIME"}),
        )
        for event_type in ("CAPTURED", "CANDIDATE"):
            for label, append_kwargs, event_kwargs in evidence_cases:
                with self.subTest(event_type=event_type, evidence=label):
                    ledger = self.new_ledger(f"irrelevant-{event_type}-{label}")
                    registrar = Registrar(ledger, "registrar-1")
                    candidate_id = f"QLC-20260913-{event_type.lower()}-{label}"
                    if event_type == "CANDIDATE":
                        registrar.append(
                            event(
                                event_id=f"irrelevant-{event_type}-{label}-captured",
                                candidate_id=candidate_id,
                            )
                        )
                        registrar.append(
                            event(
                                event_id=f"irrelevant-{event_type}-{label}-triaged",
                                event_type="TRIAGED",
                                previous_state="CAPTURED",
                                next_state="TRIAGED",
                                candidate_id=candidate_id,
                                timestamp=BASE_TIME + timedelta(seconds=1),
                            ),
                            check_set_version="worthiness.v1",
                        )
                    with self.assertRaises(ValueError):
                        registrar.append(
                            event(
                                event_id=f"irrelevant-{event_type}-{label}",
                                event_type=event_type,
                                previous_state=None if event_type == "CAPTURED" else "TRIAGED",
                                next_state=event_type,
                                candidate_id=candidate_id,
                                timestamp=BASE_TIME + timedelta(seconds=2),
                                **event_kwargs,
                            ),
                            **append_kwargs,
                        )

    def test_unresolved_challenge_contract_fails_closed_and_stays_visible(self) -> None:
        challenge_ledger = self.new_ledger("challenge-missing-identity")
        challenge_candidate = "QLC-20260912-challenge-missing-identity"
        self.append_frozen_fixture(
            challenge_ledger, challenge_candidate, "challenge-missing-identity"
        )
        with self.assertRaisesRegex(
            ValueError, "CHALLENGE_INCUMBENT_DEPLOYMENT_IDENTITY_FIELD_MISSING"
        ):
            self.append_authority_event(
                challenge_ledger,
                candidate_id=challenge_candidate,
                event_id="challenge-missing-identity-record",
                event_type="CHALLENGE",
                previous_state="FROZEN",
                next_state="FROZEN",
                writer_class="PROMOTION_AUTHORITY",
                writer_id="promotion-1",
                check_set_version="promotion.v1",
                offset=5,
            )

        report = json.loads(self.ledger.render_status_report())
        self.assertEqual(
            set(report["unresolved_lifecycle_contracts"]),
            {
                "CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING",
            },
        )
        self.assertEqual(
            set(report["ratified_lifecycle_contracts"]),
            {
                "DEMOTED TARGET RUNG MAPPING: RESOLVED BY OD-2",
                "ATOMIC SUCCESSION INTERIM REFUSAL: RATIFIED BY OD-4",
                "REJECTED FAILED-GATE PURPOSE: RESOLVED BY OD-5",
                "ADMISSION WITHHELD CAPACITY TARGET: RESOLVED BY OD-6",
                "DEPLOYMENT REFRESH ENVELOPE: RESOLVED BY OD-7",
                "EVALUATION RUN CANDIDATE SCOPE: RATIFIED BY OD-8",
                "SAME-EPOCH EVALUATION REUSE: RATIFIED BY OD-10",
            },
        )


if __name__ == "__main__":
    unittest.main()
