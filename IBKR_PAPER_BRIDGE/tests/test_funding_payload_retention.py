"""P0-12 retained funding payload (schema v10) — offline persistence suite.

Every fixture here is explicitly synthetic: the event hashes, symbols, amounts
and normalized values are invented for the test and are not venue evidence, not
a capture, and not a claim about Hyperliquid. Each test builds its own
throwaway database under pytest's ``tmp_path``; no real database is opened and
no broker, host or network is contacted.

The property under test is narrow: the normalized ``FundingEventRecord``
fields the Bridge *already* observes (``funding_rate``, ``position_szi``,
``n_samples``) must survive a restart instead of being lost to a
non-invertible digest — and retained bytes that stop proving themselves against
the immutable ledger digest must be refused rather than returned.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime

import pytest

from bridge.engine.types import (
    FundingAttribution,
    FundingEventRecord,
    ReconcileAttemptState,
)
from bridge.store.db import (
    SCHEMA_VERSION_BASELINE,
    SCHEMA_VERSION_FUNDING_PAYLOAD,
    SCHEMA_VERSION_KILL_EVIDENCE,
    MigrationError,
    ReconcileConflictError,
    Store,
)

NOW = datetime(2026, 9, 11, 12, 0, tzinfo=UTC)


def synthetic_event(
    *,
    event_id: str = "0xsynthetic0001",
    amount_usdc: float = -1.25,
    funding_rate: float | None = 0.0000125,
    position_szi: float | None = 0.1,
    n_samples: int | None = 1,
    attribution: FundingAttribution = FundingAttribution.ATTRIBUTED,
) -> FundingEventRecord:
    """One invented funding event with the normalized fields under test."""
    return FundingEventRecord(
        event_id=event_id,
        symbol="BTC",
        amount_usdc=amount_usdc,
        effective_ts=NOW,
        source="HL_USER_FUNDING",
        attribution=attribution,
        funding_rate=funding_rate,
        position_szi=position_szi,
        n_samples=n_samples,
    )


def open_at(path, version: int) -> Store:
    store = Store(path)
    store.initialize(target_schema_version=version)
    return store


def record(store: Store, *events: FundingEventRecord) -> str:
    """Drive the real acceptance write path for the given funding events."""
    attempt_id = store.reserve_reconcile_attempt(
        run_id="run-retention", started_ts=NOW, deadline_s=5.0, max_skew_s=5.0
    )
    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.INCOMPLETE,
        ended_ts=NOW,
        duration_ms=1,
        canonical_hash=None,
        reason_code="TESTED",
        funding_events=events,
        accepted=False,
        fresh=False,
    )
    return attempt_id


def payload_rows(store: Store) -> list[dict]:
    return store._rows(
        "SELECT * FROM funding_event_payloads ORDER BY event_id"
    )


# ---------------------------------------------------------------------------
# Retention across a restart
# ---------------------------------------------------------------------------


def test_new_event_retains_normalized_payload_across_restart(tmp_path):
    db_path = tmp_path / "retention.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    ledger_before = store.get_funding_event(event.event_id)
    store.close()

    reopened = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    # The ledger row itself is untouched by retention.
    assert reopened.get_funding_event(event.event_id) == ledger_before
    assert ledger_before["payload_digest"] == event.digest

    recovered = reopened.get_funding_event_payload(event.event_id)
    # Exactly the existing authoritative domain, value for value.
    assert recovered == event.authoritative()
    assert recovered["funding_rate"] == 0.0000125
    assert recovered["position_szi"] == 0.1
    assert recovered["n_samples"] == 1
    # The retained bytes reproduce the ledger's own immutable digest.
    assert (
        FundingEventRecord(
            event_id=recovered["event_id"],
            symbol=recovered["symbol"],
            amount_usdc=recovered["amount_usdc"],
            effective_ts=datetime.fromisoformat(recovered["effective_ts"]),
            source=recovered["source"],
            funding_rate=recovered["funding_rate"],
            position_szi=recovered["position_szi"],
            n_samples=recovered["n_samples"],
        ).digest
        == ledger_before["payload_digest"]
    )
    reopened.close()


def test_optional_nulls_are_retained_as_null_not_zero(tmp_path):
    db_path = tmp_path / "nulls.db"
    event = synthetic_event(
        event_id="0xsynthetic-null",
        funding_rate=None,
        position_szi=None,
        n_samples=None,
    )
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    store.close()

    reopened = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    recovered = reopened.get_funding_event_payload(event.event_id)
    assert recovered["funding_rate"] is None
    assert recovered["position_szi"] is None
    assert recovered["n_samples"] is None
    # An absent observation is never a zero observation.
    assert recovered["funding_rate"] != 0
    assert recovered["n_samples"] != 0
    reopened.close()


def test_duplicate_delivery_keeps_one_event_and_one_payload(tmp_path):
    db_path = tmp_path / "duplicate.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event, event)
    record(store, event)
    assert len(store.list_funding_events()) == 1
    assert len(payload_rows(store)) == 1
    total = store.funding_total(symbol="BTC")
    store.close()

    reopened = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(reopened, event)
    assert len(reopened.list_funding_events()) == 1
    assert len(payload_rows(reopened)) == 1
    assert reopened.funding_total(symbol="BTC") == total
    assert reopened.get_funding_event_payload(event.event_id) == (
        event.authoritative()
    )
    reopened.close()


def test_conflicting_identity_refuses_and_writes_neither_row(tmp_path):
    db_path = tmp_path / "conflict.db"
    first = synthetic_event(amount_usdc=-1.0)
    drifted = synthetic_event(amount_usdc=-9.0)
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, first)
    ledger_before = store.get_funding_event(first.event_id)
    payload_before = payload_rows(store)

    with pytest.raises(ReconcileConflictError) as excinfo:
        record(store, drifted)
    assert excinfo.value.code == "FUNDING_EVENT_IDENTITY_CONFLICT"

    assert store.get_funding_event(first.event_id) == ledger_before
    assert payload_rows(store) == payload_before
    assert store.get_funding_event_payload(first.event_id) == (
        first.authoritative()
    )
    store.close()


def test_payload_write_failure_rolls_back_the_whole_attempt(tmp_path, monkeypatch):
    db_path = tmp_path / "rollback.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)

    def boom(self, **kwargs):
        raise RuntimeError("synthetic payload write failure")

    monkeypatch.setattr(Store, "_append_funding_payload_locked", boom)
    with pytest.raises(RuntimeError):
        attempt_id = record(store, event)
    monkeypatch.undo()

    # Neither half of the acceptance transaction survived.
    assert store.list_funding_events() == []
    assert payload_rows(store) == []
    unresolved = store._rows(
        "SELECT state FROM reconcile_attempts ORDER BY seq"
    )
    assert [row["state"] for row in unresolved] == ["COLLECTING"]
    store.close()

    reopened = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    assert reopened.list_funding_events() == []
    assert payload_rows(reopened) == []
    reopened.close()


# ---------------------------------------------------------------------------
# Historical rows: explicitly unavailable, never fabricated
# ---------------------------------------------------------------------------


def test_historical_event_is_unavailable_and_replay_does_not_backfill(tmp_path):
    db_path = tmp_path / "historical.db"
    event = synthetic_event(event_id="0xsynthetic-historical")
    store = open_at(db_path, SCHEMA_VERSION_KILL_EVIDENCE)
    record(store, event)
    ledger_before = store.get_funding_event(event.event_id)
    store.close()

    upgraded = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    assert upgraded.get_meta("schema_version") == str(
        SCHEMA_VERSION_FUNDING_PAYLOAD
    )
    # The historical ledger row keeps its exact bytes and digest.
    assert upgraded.get_funding_event(event.event_id) == ledger_before
    # The missing payload is explicitly unavailable, not reconstructed.
    assert upgraded.get_funding_event_payload(event.event_id) is None
    assert payload_rows(upgraded) == []

    # An ordinary replay of the same event must not silently manufacture the
    # evidence the migration refused to invent.
    record(upgraded, event)
    assert upgraded.get_funding_event_payload(event.event_id) is None
    assert payload_rows(upgraded) == []
    assert len(upgraded.list_funding_events()) == 1
    upgraded.close()


def test_unknown_event_is_refused_rather_than_reported_unavailable(tmp_path):
    store = open_at(tmp_path / "unknown.db", SCHEMA_VERSION_FUNDING_PAYLOAD)
    with pytest.raises(ReconcileConflictError) as excinfo:
        store.get_funding_event_payload("0xnever-recorded")
    assert excinfo.value.code == "FUNDING_PAYLOAD_EVENT_UNKNOWN"
    store.close()


# ---------------------------------------------------------------------------
# Damaged retained bytes are refused
# ---------------------------------------------------------------------------


def tamper(db_path, event_id: str, payload_json: str) -> None:
    """Overwrite retained bytes out-of-band, as disk damage would."""
    raw = sqlite3.connect(db_path)
    try:
        raw.execute("DROP TRIGGER trg_funding_payload_no_update")
        raw.execute(
            "UPDATE funding_event_payloads SET payload_json = ? "
            "WHERE event_id = ?",
            (payload_json, event_id),
        )
        raw.commit()
    finally:
        raw.close()


def test_tampered_payload_is_refused_even_when_parseable(tmp_path):
    db_path = tmp_path / "tampered.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    store.close()

    forged = dict(event.authoritative())
    forged["funding_rate"] = 0.5  # still valid JSON, still the right domain
    tamper(db_path, event.event_id, json.dumps(forged, sort_keys=True,
                                               separators=(",", ":")))

    store = Store(db_path)
    with pytest.raises(ReconcileConflictError) as excinfo:
        store.get_funding_event_payload(event.event_id)
    assert excinfo.value.code == "FUNDING_PAYLOAD_DIGEST_MISMATCH"
    store.close()


def test_malformed_payload_is_refused(tmp_path):
    db_path = tmp_path / "malformed.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    store.close()

    tamper(db_path, event.event_id, "{not json")

    store = Store(db_path)
    with pytest.raises(ReconcileConflictError) as excinfo:
        store.get_funding_event_payload(event.event_id)
    assert excinfo.value.code == "FUNDING_PAYLOAD_MALFORMED"
    store.close()


def test_domain_drift_in_retained_bytes_is_refused(tmp_path):
    db_path = tmp_path / "domain.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    store.close()

    narrowed = dict(event.authoritative())
    narrowed.pop("n_samples")
    tamper(db_path, event.event_id, json.dumps(narrowed, sort_keys=True,
                                               separators=(",", ":")))

    store = Store(db_path)
    with pytest.raises(ReconcileConflictError) as excinfo:
        store.get_funding_event_payload(event.event_id)
    assert excinfo.value.code == "FUNDING_PAYLOAD_DOMAIN_MISMATCH"
    store.close()


def test_noncanonical_but_valid_payload_json_is_refused(tmp_path):
    db_path = tmp_path / "noncanonical.db"
    event = synthetic_event(event_id="0xnoncanonical")
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    canonical = payload_rows(store)[0]["payload_json"]
    store.close()

    noncanonical = json.dumps(json.loads(canonical), sort_keys=True, indent=1)
    assert json.loads(noncanonical) == event.authoritative()
    assert noncanonical != canonical
    tamper(db_path, event.event_id, noncanonical)

    damaged = Store(db_path)
    with pytest.raises(ReconcileConflictError) as excinfo:
        damaged.get_funding_event_payload(event.event_id)
    assert excinfo.value.code == "FUNDING_PAYLOAD_MALFORMED"
    damaged.close()


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_nonfinite_json_tokens_receive_stable_integrity_refusal(tmp_path, token):
    db_path = tmp_path / f"nonfinite-{token}.db"
    event = synthetic_event(event_id=f"0xnonfinite-{token}")
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    canonical = payload_rows(store)[0]["payload_json"]
    store.close()

    marker = '"funding_rate":1.25e-05'
    assert marker in canonical
    tamper(
        db_path,
        event.event_id,
        canonical.replace(marker, f'"funding_rate":{token}'),
    )

    damaged = Store(db_path)
    with pytest.raises(ReconcileConflictError) as excinfo:
        damaged.get_funding_event_payload(event.event_id)
    assert excinfo.value.code == "FUNDING_PAYLOAD_MALFORMED"
    damaged.close()


def test_a_damaged_store_fails_closed_on_reopen(tmp_path):
    db_path = tmp_path / "damaged-reopen.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    store.close()

    tamper(db_path, event.event_id, "{not json")

    with pytest.raises(MigrationError):
        open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)


def test_retained_payload_is_append_only(tmp_path):
    db_path = tmp_path / "append-only.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    with pytest.raises(sqlite3.DatabaseError):
        store.conn.execute(
            "UPDATE funding_event_payloads SET payload_json = '{}'"
        )
    with pytest.raises(sqlite3.DatabaseError):
        store.conn.execute("DELETE FROM funding_event_payloads")
    assert store.get_funding_event_payload(event.event_id) == (
        event.authoritative()
    )
    store.close()


# ---------------------------------------------------------------------------
# Opt-in capability and migration
# ---------------------------------------------------------------------------


def test_default_target_stays_v4_without_retention(tmp_path):
    store = Store(tmp_path / "default.db")
    store.initialize()
    assert store.get_meta("schema_version") == str(SCHEMA_VERSION_BASELINE)
    assert store.funding_payload_retention_enabled() is False
    assert store._has_any_funding_payload_object() is False
    store.close()


def test_v9_store_keeps_its_behavior_and_refuses_payload_reads(tmp_path):
    db_path = tmp_path / "v9.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_KILL_EVIDENCE)
    record(store, event)
    assert store.funding_payload_retention_enabled() is False
    assert store._has_any_funding_payload_object() is False
    assert store.kill_evidence_enabled() is True
    with pytest.raises(ReconcileConflictError) as excinfo:
        store.get_funding_event_payload(event.event_id)
    assert excinfo.value.code == "FUNDING_PAYLOAD_SCHEMA_INACTIVE"
    store.close()

    # Reopening a v9 store at the default target never upgrades it.
    reopened = Store(db_path)
    reopened.initialize()
    assert reopened.get_meta("schema_version") == str(
        SCHEMA_VERSION_KILL_EVIDENCE
    )
    assert reopened.funding_payload_retention_enabled() is False
    reopened.close()


def test_v10_reopen_is_idempotent_and_never_downgrades(tmp_path):
    db_path = tmp_path / "idempotent.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    store.close()

    for target in (
        SCHEMA_VERSION_BASELINE,
        SCHEMA_VERSION_KILL_EVIDENCE,
        SCHEMA_VERSION_FUNDING_PAYLOAD,
    ):
        reopened = Store(db_path)
        reopened.initialize(target_schema_version=target)
        assert reopened.get_meta("schema_version") == str(
            SCHEMA_VERSION_FUNDING_PAYLOAD
        )
        assert reopened.funding_payload_retention_enabled() is True
        assert reopened.get_funding_event_payload(event.event_id) == (
            event.authoritative()
        )
        assert len(payload_rows(reopened)) == 1
        reopened.close()


def test_v10_meta_row_without_its_table_fails_closed(tmp_path):
    db_path = tmp_path / "claimed-v10.db"
    store = open_at(db_path, SCHEMA_VERSION_KILL_EVIDENCE)
    store.conn.execute(
        "UPDATE meta SET value = ? WHERE key = 'schema_version'",
        (str(SCHEMA_VERSION_FUNDING_PAYLOAD),),
    )
    store.conn.commit()
    store.close()

    with pytest.raises(RuntimeError):
        open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)


def test_migration_refuses_a_preexisting_payload_object(tmp_path):
    db_path = tmp_path / "preexisting.db"
    store = open_at(db_path, SCHEMA_VERSION_KILL_EVIDENCE)
    store.conn.execute(
        "CREATE TABLE funding_event_payloads (event_id TEXT PRIMARY KEY)"
    )
    store.conn.commit()
    store.close()

    reopened = Store(db_path)
    with pytest.raises(MigrationError):
        reopened.initialize(target_schema_version=SCHEMA_VERSION_FUNDING_PAYLOAD)
    # The failed migration left a reopenable v9 database and a secret-safe mark.
    assert reopened.get_meta("schema_version") == str(
        SCHEMA_VERSION_KILL_EVIDENCE
    )
    assert reopened.get_meta("funding_payload_migration_failure") == (
        "FUNDING_PAYLOAD_MIGRATION_FAILED:MigrationError"
    )
    reopened.close()


# ---------------------------------------------------------------------------
# Independently specified cases (missing-case report, 2026-09-11)
# ---------------------------------------------------------------------------

# Pinned *before* the writer exists, so changing the writer and the canonical
# helper together cannot make the round-trip pass tautologically. Synthetic.
FROZEN_EVENT = FundingEventRecord(
    event_id="0xfund-retain",
    symbol="BTC",
    amount_usdc=-1.25,
    effective_ts=datetime(2026, 7, 26, 12, 0, tzinfo=UTC),
    source="TEST",
    funding_rate=1.25e-05,
    position_szi=0.1,
    n_samples=1,
)
FROZEN_CANONICAL_JSON = (
    '{"amount_usdc":-1.25,"effective_ts":"2026-07-26T12:00:00+00:00",'
    '"event_id":"0xfund-retain","funding_rate":1.25e-05,"n_samples":1,'
    '"position_szi":0.1,"source":"TEST","symbol":"BTC"}'
)
FROZEN_DIGEST = (
    "77fb9ccfc5d2dddf90d53b7e2c924b5b240e849cb934dc1633734c3a62bd4a73"
)


def test_retained_bytes_match_a_frozen_canonical_fixture(tmp_path):
    db_path = tmp_path / "frozen.db"
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, FROZEN_EVENT)
    store.close()

    reopened = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    row = reopened._rows(
        "SELECT * FROM funding_event_payloads WHERE event_id = ?",
        (FROZEN_EVENT.event_id,),
    )[0]
    # Exact stored text and digest, pinned independently of the writer.
    assert row["payload_json"] == FROZEN_CANONICAL_JSON
    assert row["payload_digest"] == FROZEN_DIGEST
    # The pre-change ledger digest is unmoved by retention.
    assert reopened.get_funding_event(FROZEN_EVENT.event_id)[
        "payload_digest"
    ] == FROZEN_DIGEST
    assert reopened.get_funding_event_payload(FROZEN_EVENT.event_id) == (
        json.loads(FROZEN_CANONICAL_JSON)
    )
    reopened.close()


def test_retained_payload_excludes_locally_derived_attribution(tmp_path):
    db_path = tmp_path / "no-attribution.db"
    event = synthetic_event(attribution=FundingAttribution.UNATTRIBUTED)
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, event)
    store.close()

    reopened = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    recovered = reopened.get_funding_event_payload(event.event_id)
    # attribution is locally derived, so it is not exchange-authoritative and
    # must stay out of the retained payload exactly as it stays out of the
    # identity digest.
    assert "attribution" not in recovered
    assert tuple(sorted(recovered)) == Store._FUNDING_PAYLOAD_FIELDS
    # It is still recorded on the ledger row, unchanged.
    assert reopened.get_funding_event(event.event_id)["attribution"] == (
        FundingAttribution.UNATTRIBUTED.value
    )
    reopened.close()


@pytest.mark.parametrize(
    "field,value",
    [
        ("funding_rate", 0.0000999),
        ("position_szi", 0.9),
        ("n_samples", 3),
        ("amount_usdc", -9.0),
    ],
)
def test_each_authoritative_field_drift_is_refused(tmp_path, field, value):
    db_path = tmp_path / f"drift-{field}.db"
    original = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, original)
    ledger_before = store.get_funding_event(original.event_id)
    payload_before = payload_rows(store)

    drifted = synthetic_event(**{field: value})
    assert drifted.digest != original.digest
    with pytest.raises(ReconcileConflictError) as excinfo:
        record(store, drifted)
    assert excinfo.value.code == "FUNDING_EVENT_IDENTITY_CONFLICT"
    store.close()

    reopened = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    assert reopened.get_funding_event(original.event_id) == ledger_before
    assert payload_rows(reopened) == payload_before
    assert reopened.get_funding_event_payload(original.event_id) == (
        original.authoritative()
    )
    reopened.close()


def test_changed_replay_of_a_historical_event_still_conflicts(tmp_path):
    db_path = tmp_path / "historical-conflict.db"
    event = synthetic_event(event_id="0xsynthetic-legacy")
    store = open_at(db_path, SCHEMA_VERSION_KILL_EVIDENCE)
    record(store, event)
    ledger_before = store.get_funding_event(event.event_id)
    store.close()

    upgraded = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    with pytest.raises(ReconcileConflictError) as excinfo:
        record(upgraded, synthetic_event(
            event_id="0xsynthetic-legacy", funding_rate=0.5
        ))
    # The refusal comes from the legacy ledger digest, which is all a
    # pre-upgrade row has — and it is enough.
    assert excinfo.value.code == "FUNDING_EVENT_IDENTITY_CONFLICT"
    assert upgraded.get_funding_event(event.event_id) == ledger_before
    assert payload_rows(upgraded) == []
    upgraded.close()


@pytest.mark.parametrize("target", [4, 5, 6, 7, 8, 9])
def test_explicit_v4_to_v9_targets_gain_no_payload_capability(tmp_path, target):
    store = Store(tmp_path / f"v{target}.db")
    store.initialize(target_schema_version=target)
    assert store.get_meta("schema_version") == str(target)
    assert store.funding_payload_retention_enabled() is False
    assert store._has_any_funding_payload_object() is False
    with pytest.raises(ReconcileConflictError) as excinfo:
        store.get_funding_event_payload("0xsynthetic-never-present")
    assert excinfo.value.code == "FUNDING_PAYLOAD_SCHEMA_INACTIVE"
    store.close()


def test_v9_to_v10_ddl_fault_rolls_back_and_keeps_v9_reopenable(
    tmp_path, monkeypatch
):
    db_path = tmp_path / "ddl-fault.db"
    event = synthetic_event()
    store = open_at(db_path, SCHEMA_VERSION_KILL_EVIDENCE)
    record(store, event)
    ledger_before = store.get_funding_event(event.event_id)
    objects_before = {
        str(row["name"])
        for row in store.conn.execute(
            "SELECT name FROM sqlite_master"
        ).fetchall()
    }
    store.close()

    original = Store._create_funding_payload_tables_v10

    def fail_after_ddl(self):
        original(self)
        raise RuntimeError("secret injected migration detail")

    monkeypatch.setattr(Store, "_create_funding_payload_tables_v10", fail_after_ddl)
    faulted = Store(db_path)
    with pytest.raises(RuntimeError):
        faulted.initialize(target_schema_version=SCHEMA_VERSION_FUNDING_PAYLOAD)
    faulted.close()
    monkeypatch.undo()

    reopened = Store(db_path)
    reopened.initialize(target_schema_version=SCHEMA_VERSION_KILL_EVIDENCE)
    assert reopened.get_meta("schema_version") == str(SCHEMA_VERSION_KILL_EVIDENCE)
    # No partial v10 object survived, and the legacy row is untouched.
    assert {
        str(row["name"])
        for row in reopened.conn.execute("SELECT name FROM sqlite_master").fetchall()
    } == objects_before
    assert reopened.get_funding_event(event.event_id) == ledger_before
    marker = reopened.get_meta("funding_payload_migration_failure")
    # Secret-safe: the exception type only, never the injected message.
    assert marker == "FUNDING_PAYLOAD_MIGRATION_FAILED:RuntimeError"
    assert "secret" not in marker
    reopened.close()


def test_v9_to_v10_schema_meta_update_failure_rolls_back_everything(
    tmp_path, monkeypatch
):
    db_path = tmp_path / "meta-failure.db"
    event = synthetic_event(event_id="0xmeta-failure")
    store = open_at(db_path, SCHEMA_VERSION_KILL_EVIDENCE)
    record(store, event)
    ledger_before = store.get_funding_event(event.event_id)
    store.close()

    real_connect = sqlite3.connect

    class FailV10MetaUpdate(sqlite3.Connection):
        def execute(self, sql, parameters=(), /):
            statement = " ".join(sql.lower().split())
            if (
                statement.startswith(
                    "update meta set value=? where key='schema_version'"
                )
                and parameters
                and str(parameters[0]) == str(SCHEMA_VERSION_FUNDING_PAYLOAD)
            ):
                raise sqlite3.OperationalError(
                    "synthetic schema-meta update failure"
                )
            return super().execute(sql, parameters)

    def failing_connect(*args, **kwargs):
        return real_connect(*args, factory=FailV10MetaUpdate, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", failing_connect)
        failing = Store(db_path)
        with pytest.raises(sqlite3.OperationalError, match="schema-meta update"):
            failing.initialize(
                target_schema_version=SCHEMA_VERSION_FUNDING_PAYLOAD
            )

    assert failing.get_meta("schema_version") == str(
        SCHEMA_VERSION_KILL_EVIDENCE
    )
    assert failing.get_funding_event(event.event_id) == ledger_before
    assert failing._has_any_funding_payload_object() is False
    assert failing.get_meta("funding_payload_migration_failure") == (
        "FUNDING_PAYLOAD_MIGRATION_FAILED:OperationalError"
    )
    failing.close()

    reopened = open_at(db_path, SCHEMA_VERSION_KILL_EVIDENCE)
    assert reopened.get_funding_event(event.event_id) == ledger_before
    assert reopened._has_any_funding_payload_object() is False
    reopened.close()


def test_v10_store_missing_its_immutability_trigger_fails_closed(tmp_path):
    db_path = tmp_path / "missing-trigger.db"
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, synthetic_event())
    store.close()

    raw = sqlite3.connect(db_path)
    try:
        raw.execute("DROP TRIGGER trg_funding_payload_no_delete")
        raw.commit()
    finally:
        raw.close()

    with pytest.raises(MigrationError):
        open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)


def test_v10_store_missing_its_table_fails_closed(tmp_path):
    db_path = tmp_path / "missing-table.db"
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    store.close()

    raw = sqlite3.connect(db_path)
    try:
        raw.execute("DROP TABLE funding_event_payloads")
        raw.commit()
    finally:
        raw.close()

    with pytest.raises(RuntimeError):
        open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)


def test_an_orphaned_retained_payload_fails_closed(tmp_path):
    """A payload whose ledger row is absent is damage, not evidence."""
    db_path = tmp_path / "orphan.db"
    store = open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
    record(store, synthetic_event())
    store.close()

    raw = sqlite3.connect(db_path)
    try:
        raw.execute("PRAGMA foreign_keys=OFF")
        raw.execute("DROP TRIGGER trg_funding_payload_no_update")
        raw.execute(
            "UPDATE funding_event_payloads SET event_id = '0xorphan'"
        )
        raw.commit()
    finally:
        raw.close()

    with pytest.raises(MigrationError):
        open_at(db_path, SCHEMA_VERSION_FUNDING_PAYLOAD)
