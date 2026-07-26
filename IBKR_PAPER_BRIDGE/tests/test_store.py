from __future__ import annotations

from datetime import UTC, datetime, timedelta

from bridge.store.db import Store


def test_store_roundtrip_decision_chain_and_schema_version(tmp_path):
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()

    assert store.get_meta("schema_version") == "4"

    run_id = "run-test"
    decision_uid = "decision-001"
    now = datetime(2026, 7, 6, 12, 0, tzinfo=UTC)

    store.create_run(run_id, mode="dry_run", network="testnet", config={"coin": "BTC"})
    store.insert_bar("BTC", "1h", now, 100.0, 105.0, 99.0, 104.0, 123.0)
    store.insert_decision(run_id, decision_uid, now, "BTC", "SIGNAL", {"direction": "LONG"})
    store.insert_decision(run_id, decision_uid, now, "BTC", "RISK_PASS", {"qty": 0.1})

    trade_id = store.create_trade(
        run_id=run_id,
        coin="BTC",
        direction="LONG",
        qty=0.1,
        entry_decision_uid=decision_uid,
        signal_ts=now,
        decision_ts=now,
        expected_px=104.0,
        risk_dollars=10.0,
        risk_pct=0.005,
        leverage=1,
        sl_initial=100.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    store.insert_order(
        cloid="0xentry",
        oid=101,
        group_id="g1",
        order_ref=f"{decision_uid}:ENTRY",
        order_json={"type": "market"},
        decision_uid=decision_uid,
        trade_id=trade_id,
        role="ENTRY",
        status="SUBMITTED",
        qty=0.1,
    )
    store.update_order_status("0xentry", "FILLED", filled_qty=0.1, avg_fill_px=104.5, ts_last=now)
    store.insert_fill("fill-1", "0xentry", decision_uid, now, 0.1, 104.5, fee=0.01, funding=0.0)
    store.update_trade_exit(trade_id, exit_px=108.0, exit_ts=now, exit_reason="TP", pnl=0.35)
    store.insert_equity(run_id, now, equity=1000.0, cash=999.0, unrealized=1.0, realized_today=0.35)
    store.upsert_risk_day("2026-07-06", 1000.0, 0.35, 0.35, 0.01, 1, 0)
    store.insert_event(run_id, now, "INFO", "TEST_EVENT", "ok")

    chain = store.get_decision_chain(decision_uid)
    assert [row["stage"] for row in chain] == ["SIGNAL", "RISK_PASS"]
    assert chain[0]["payload"]["direction"] == "LONG"

    snapshot = store.get_snapshot()
    assert snapshot["runs"][0]["run_id"] == run_id
    assert snapshot["trades"][0]["trade_id"] == trade_id
    assert snapshot["orders"][0]["status"] == "FILLED"
    assert snapshot["fills"][0]["fill_id"] == "fill-1"
    assert snapshot["events"][0]["code"] == "TEST_EVENT"
    assert snapshot["bars"][0]["close"] == 104.0


# ===========================================================================
# TS-P1-004 — schema v5 partial-fill recovery ledger
# ===========================================================================

import sqlite3

import pytest

from bridge.store.db import (
    MigrationError,
    PartialRecoveryConflictError,
    compute_partial_action_cloid,
    compute_partial_action_id,
    compute_partial_recovery_id,
)

_REQUEST_ID = "request-v1:" + "c" * 64


def _v4_with_trade(tmp_path, *, target=4):
    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=target)
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store.create_run("run", mode="dry_run", network="testnet", config={})
    trade_id = store.create_trade(
        run_id="run", coin="BTC", direction="LONG", qty=2.0,
        entry_decision_uid="d1", signal_ts=now, decision_ts=now,
        expected_px=100.0, risk_dollars=1.0, risk_pct=0.001, leverage=1,
        sl_initial=95.0, tp_initial=None, llm_directive_id=None,
    )
    store.insert_order(
        cloid="entry-1", oid=1, group_id=_REQUEST_ID,
        order_ref=f"{_REQUEST_ID}:ENTRY", order_json={"symbol": "BTC"},
        decision_uid="d1", trade_id=trade_id, role="ENTRY", status="OPEN", qty=2.0,
    )
    return store, int(trade_id), now


def test_default_initialize_stays_on_schema_v4(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    assert store.get_meta("schema_version") == "4"
    assert store.partial_protection_enabled() is False
    residue = store.conn.execute(
        "SELECT name FROM sqlite_master WHERE name LIKE 'partial_fill_%'"
    ).fetchall()
    assert residue == []


def test_opt_in_v5_migration_is_additive_and_preserves_v4_rows(tmp_path):
    store, trade_id, _now = _v4_with_trade(tmp_path)
    orders = store.conn.execute("SELECT * FROM orders").fetchall()
    trades = store.conn.execute("SELECT * FROM trades").fetchall()
    store.close()

    upgraded = Store(tmp_path / "bridge.db")
    upgraded.initialize(target_schema_version=5)

    assert upgraded.get_meta("schema_version") == "5"
    assert upgraded.partial_protection_enabled() is True
    assert [dict(r) for r in upgraded.conn.execute("SELECT * FROM orders")] == [
        dict(r) for r in orders
    ]
    assert [dict(r) for r in upgraded.conn.execute("SELECT * FROM trades")] == [
        dict(r) for r in trades
    ]
    # no speculative backfill
    assert upgraded.list_partial_recoveries() == []


def test_v5_migration_rolls_back_completely_on_failure(tmp_path):
    class FailingStore(Store):
        def _validate_partial_fill_schema_v5(self):
            raise MigrationError("injected")

    store, _trade_id, _now = _v4_with_trade(tmp_path)
    store.close()

    failing = FailingStore(tmp_path / "bridge.db")
    with pytest.raises(MigrationError):
        failing.initialize(target_schema_version=5)

    assert failing.get_meta("schema_version") == "4"
    assert failing.conn.execute(
        "SELECT name FROM sqlite_master WHERE name LIKE 'partial_fill_%'"
    ).fetchall() == []
    assert failing.conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 1
    assert failing.conn.execute("SELECT COUNT(*) FROM trades").fetchone()[0] == 1


def test_v5_reopen_is_idempotent(tmp_path):
    store, _trade_id, _now = _v4_with_trade(tmp_path, target=5)
    store.close()
    for _ in range(3):
        reopened = Store(tmp_path / "bridge.db")
        reopened.initialize(target_schema_version=5)
        assert reopened.get_meta("schema_version") == "5"
        reopened.close()


def test_partial_recovery_and_action_identities_are_deterministic():
    first = compute_partial_recovery_id(trade_id=1, entry_cloid="e", generation=0)
    assert first == compute_partial_recovery_id(
        trade_id=1, entry_cloid="e", generation=0
    )
    assert first != compute_partial_recovery_id(
        trade_id=1, entry_cloid="e", generation=1
    )
    cancel = compute_partial_action_id(
        kind="CANCEL_ENTRY", trade_id=1, entry_cloid="e", entry_request_id=_REQUEST_ID
    )
    assert cancel.startswith("pfa-v1:")
    assert compute_partial_action_cloid(cancel).startswith("0x")
    assert len(compute_partial_action_cloid(cancel)) == 34


def test_reservation_transition_and_append_only_evidence(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    assert recovery["state"] == "PARTIAL_DETECTED"

    # idempotent open: the deadline is never rewritten
    again = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now + timedelta(seconds=99),
        protect_deadline_ts=now + timedelta(seconds=999),
    )
    assert again["protect_deadline_ts"] == recovery["protect_deadline_ts"]

    action_id = compute_partial_action_id(
        kind="INSTALL_STOP", trade_id=trade_id, entry_cloid="entry-1",
        entry_request_id=_REQUEST_ID, generation=0, qty_lots=1000,
    )
    is_replay, row = store.reserve_partial_action(
        recovery_id=str(recovery["recovery_id"]), action_id=action_id,
        kind="INSTALL_STOP", target_cloid=compute_partial_action_cloid(action_id),
        expected_state="PARTIAL_DETECTED", next_state="PROTECTION_PENDING",
        reason_code="PROTECTION_RESERVED", generation=0, qty_lots=1000,
    )
    assert is_replay is False and row["qty_lots"] == 1000
    # the state transition is committed in the same transaction as the reservation
    assert store.get_partial_recovery(str(recovery["recovery_id"]))["state"] == (
        "PROTECTION_PENDING"
    )
    assert [e["status"] for e in store.partial_action_events(action_id)] == ["RESERVED"]

    store.record_partial_action_event(
        action_id=action_id, status="SENT", reason_code="PROTECTION_SENT"
    )
    store.record_partial_action_event(
        action_id=action_id, status="APPLIED", reason_code="MOCK_OK"
    )
    assert [e["seq"] for e in store.partial_action_events(action_id)] == [1, 2, 3]
    assert store.resolve_partial_action(action_id) == "APPLIED"

    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            "UPDATE partial_fill_action_events SET status='NOT_APPLIED'"
        )
    store.conn.rollback()


def test_reservation_identity_conflict_is_refused(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    action_id = compute_partial_action_id(
        kind="INSTALL_STOP", trade_id=trade_id, entry_cloid="entry-1",
        entry_request_id=_REQUEST_ID, generation=0, qty_lots=1000,
    )
    common = dict(
        recovery_id=str(recovery["recovery_id"]), action_id=action_id,
        kind="INSTALL_STOP", target_cloid=compute_partial_action_cloid(action_id),
        expected_state="PARTIAL_DETECTED", next_state="PROTECTION_PENDING",
        reason_code="PROTECTION_RESERVED", generation=0,
    )
    store.reserve_partial_action(qty_lots=1000, **common)
    common["expected_state"] = "PROTECTION_PENDING"
    with pytest.raises(PartialRecoveryConflictError) as exc:
        store.reserve_partial_action(qty_lots=1500, **common)
    assert exc.value.code == "PARTIAL_ACTION_IDENTITY_CONFLICT"


def test_generation_bump_preserves_deadline_and_first_observation(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PARTIAL_DETECTED",
        target="PROTECTION_PENDING", reason_code="X",
    )
    bumped = store.open_partial_generation(
        recovery_id=str(recovery["recovery_id"]), reason_code="LATE_FILL_REQUANTIFY",
        position_lots=1500,
    )
    assert bumped["generation"] == 1
    assert bumped["state"] == "PARTIAL_DETECTED"
    assert bumped["protect_deadline_ts"] == recovery["protect_deadline_ts"]
    assert bumped["first_observed_ts"] == recovery["first_observed_ts"]
    assert bumped["position_lots"] == 1500


def test_legacy_partial_entry_candidates_is_a_pure_local_query(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    assert store.legacy_partial_entry_candidates() == []

    store.insert_fill("f1", "entry-1", "d1", now, 1.0, 100.0, fee=0.0, funding=0.0)
    candidates = store.legacy_partial_entry_candidates()
    assert [c["cloid"] for c in candidates] == ["entry-1"]
    assert candidates[0]["ordered_qty"] == 2.0
    assert candidates[0]["filled_qty"] == 1.0

    # a fully filled entry is not a partial
    store.insert_fill("f2", "entry-1", "d1", now, 1.0, 100.0, fee=0.0, funding=0.0)
    assert store.legacy_partial_entry_candidates() == []


def test_blocking_and_rearm_queries(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    assert store.partial_recovery_blocks_new_risk() is False

    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    assert store.partial_recovery_blocks_new_risk() is True

    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PARTIAL_DETECTED",
        target="PROTECTION_PENDING", reason_code="X",
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PROTECTION_PENDING",
        target="PROTECTION_VERIFIED", reason_code="X",
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PROTECTION_VERIFIED",
        target="CANCEL_PENDING", reason_code="X",
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="CANCEL_PENDING",
        target="PROTECTED_PARTIAL", reason_code="PROTECTED_PARTIAL",
    )
    assert store.partial_recovery_blocks_new_risk() is False
    assert [r["recovery_id"] for r in store.partial_recoveries_awaiting_rearm()] == [
        recovery["recovery_id"]
    ]

    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PROTECTED_PARTIAL",
        target="PROTECTED_PARTIAL", reason_code="REARM_ARCHIVED",
    )
    assert store.partial_recoveries_awaiting_rearm() == []


def test_unprotected_abort_is_a_sticky_latch(tmp_path):
    store, trade_id, now = _v4_with_trade(tmp_path, target=5)
    recovery = store.open_partial_recovery(
        run_id="run", symbol="BTC", trade_id=trade_id, entry_cloid="entry-1",
        entry_decision_uid="d1", entry_request_id=_REQUEST_ID,
        first_observed_ts=now, protect_deadline_ts=now + timedelta(seconds=10),
    )
    store.transition_partial_recovery(
        str(recovery["recovery_id"]), expected="PARTIAL_DETECTED",
        target="UNPROTECTED_ABORT", reason_code="MIXED_PROVENANCE",
    )
    assert store.partial_recovery_abort_active("BTC") is True
    assert store.partial_recovery_blocks_new_risk() is True
    assert store.active_partial_recovery_for_symbol("BTC") is None


# ---------------------------------------------------------------------------
# TS-P1-005 schema v6 (opt-in; default target stays v4)
# ---------------------------------------------------------------------------

_V6_OBJECTS = (
    "reconcile_attempts",
    "reconcile_components",
    "reconcile_diffs",
    "reconcile_checkpoints",
    "funding_events",
)


def _existing_objects(store) -> set[str]:
    rows = store.conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    return {str(row["name"]) for row in rows}


def test_v6_capable_build_opened_with_default_target_stays_v4(tmp_path):
    """The operational baseline is untouched by TS-P1-005."""
    from bridge.store.db import SCHEMA_VERSION_FULL_RECONCILE, Store

    assert SCHEMA_VERSION_FULL_RECONCILE == 6
    store = Store(tmp_path / "bridge.db")
    store.initialize()

    assert store.get_meta("schema_version") == "4"
    assert store.full_reconcile_enabled() is False
    assert not (_existing_objects(store) & set(_V6_OBJECTS))
    assert store.latest_accepted_reconcile_checkpoint() is None
    store.close()


def test_v4_chain_can_reach_v6_and_keeps_v5_ledger(tmp_path):
    from bridge.store.db import Store

    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=6)

    assert store.get_meta("schema_version") == "6"
    assert set(_V6_OBJECTS) <= _existing_objects(store)
    # v6 is strictly additive: the v5 recovery ledger is still present and
    # still authoritative, so partial-fill gating cannot silently switch off.
    assert {"partial_fill_recoveries", "partial_fill_actions"} <= _existing_objects(store)
    assert store.partial_protection_enabled() is True
    assert store.full_reconcile_enabled() is True
    store.close()


def test_v6_database_reopened_with_default_target_is_never_downgraded(tmp_path):
    from bridge.store.db import Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.close()

    reopened = Store(path)
    reopened.initialize()
    assert reopened.get_meta("schema_version") == "6"
    assert reopened.full_reconcile_enabled() is True
    reopened.close()


def test_v6_migration_aborts_on_a_preexisting_object_and_rolls_back(tmp_path):
    from bridge.store.db import MigrationError, Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=5)
    # Non-canonical residue squatting on a v6 name.
    store.conn.execute("CREATE TABLE funding_events (bogus TEXT)")
    store.conn.commit()

    with pytest.raises(MigrationError):
        store._migrate_v5_to_v6()

    assert store.get_meta("schema_version") == "5"
    remaining = _existing_objects(store)
    assert "reconcile_attempts" not in remaining
    assert "reconcile_checkpoints" not in remaining
    store.close()


def test_schema_version_claiming_v6_without_v6_objects_fails_closed(tmp_path):
    """A meta row alone is not proof of a version."""
    from bridge.store.db import Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize()
    store.conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '6')"
    )
    store.conn.commit()
    store.close()

    reopened = Store(path)
    with pytest.raises(RuntimeError, match="Unsupported schema_version"):
        reopened.initialize(target_schema_version=6)
    reopened.close()


def test_v6_reopen_rejects_a_tampered_topology(tmp_path):
    from bridge.store.db import MigrationError, Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.conn.execute("DROP TABLE funding_events")
    store.conn.commit()
    store.close()

    reopened = Store(path)
    with pytest.raises(MigrationError):
        reopened.initialize(target_schema_version=6)
    reopened.close()


def test_v6_checkpoint_pointer_must_resolve_on_reopen(tmp_path):
    from bridge.store.db import (
        RECONCILE_CHECKPOINT_POINTER_KEY,
        MigrationError,
        Store,
    )

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.set_meta(RECONCILE_CHECKPOINT_POINTER_KEY, "ckpt-v1:" + "0" * 64)
    store.close()

    reopened = Store(path)
    with pytest.raises(MigrationError):
        reopened.initialize(target_schema_version=6)
    reopened.close()


def test_reconcile_attempt_cannot_be_accepted_without_a_complete_state(tmp_path):
    from bridge.engine.types import ReconcileAttemptState
    from bridge.store.db import ReconcileConflictError, Store

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=6)
    attempt_id = store.reserve_reconcile_attempt(
        run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )

    with pytest.raises(ReconcileConflictError):
        store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=ReconcileAttemptState.INCOMPLETE,
            ended_ts=now,
            duration_ms=1,
            canonical_hash="a" * 64,
            reason_code="BOGUS",
            accepted=True,
            fresh=True,
        )
    # The attempt is still open and no checkpoint exists.
    assert store.get_reconcile_attempt(attempt_id)["state"] == "COLLECTING"
    assert store.count_accepted_reconcile_checkpoints() == 0

    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.INCOMPLETE,
        ended_ts=now,
        duration_ms=1,
        canonical_hash=None,
        reason_code="TESTED",
        accepted=False,
        fresh=False,
    )
    with pytest.raises(ReconcileConflictError):
        store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=ReconcileAttemptState.COMPLETE,
            ended_ts=now,
            duration_ms=1,
            canonical_hash="b" * 64,
            reason_code="RETRY",
            accepted=True,
            fresh=True,
        )
    store.close()


def test_reconcile_ledger_methods_refuse_a_v4_store(tmp_path):
    from bridge.store.db import ReconcileConflictError, Store

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(tmp_path / "bridge.db")
    store.initialize()

    with pytest.raises(ReconcileConflictError):
        store.reserve_reconcile_attempt(
            run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
        )
    assert store.latest_accepted_reconcile_checkpoint() is None
    assert store.count_accepted_reconcile_checkpoints() == 0
    assert store.list_funding_events() == []
    assert store.full_reconcile_ready(now=now, max_age_s=900.0) is False
    store.close()


def test_funding_event_identity_conflict_is_refused(tmp_path):
    from bridge.engine.types import (
        FundingAttribution,
        FundingEventRecord,
        ReconcileAttemptState,
    )
    from bridge.store.db import ReconcileConflictError, Store

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(tmp_path / "bridge.db")
    store.initialize(target_schema_version=6)

    def record(amount: float) -> FundingEventRecord:
        return FundingEventRecord(
            event_id="0xhash",
            symbol="BTC",
            amount_usdc=amount,
            effective_ts=now,
            attribution=FundingAttribution.ATTRIBUTED,
        )

    def finalize(events):
        attempt_id = store.reserve_reconcile_attempt(
            run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
        )
        store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=ReconcileAttemptState.INCOMPLETE,
            ended_ts=now,
            duration_ms=1,
            canonical_hash=None,
            reason_code="TESTED",
            funding_events=events,
            accepted=False,
            fresh=False,
        )
        return attempt_id

    finalize([record(-1.0)])
    assert len(store.list_funding_events()) == 1
    # Exact replay is idempotent.
    finalize([record(-1.0)])
    assert len(store.list_funding_events()) == 1
    # A conflicting redefinition of the same identity is refused.
    with pytest.raises(ReconcileConflictError):
        finalize([record(-9.0)])
    assert len(store.list_funding_events()) == 1
    assert store.funding_total(symbol="BTC") == -1.0
    store.close()


# ---------------------------------------------------------------------------
# TS-P1-005 R1 — the live durable status set is derived, never hand-listed
# ---------------------------------------------------------------------------

_LIVE_STATUS_CASES = (
    "OPEN",
    "RESTING",
    "WAITING_CHILD",
    "SUBMITTED",
    "PARTIALLY_FILLED",
    "PENDING_CANCEL",
)

_TERMINAL_STATUS_CASES = ("FILLED", "CANCELED", "CANCELLED", "REJECTED", "EXPIRED")


def _seed_status_order(store, *, cloid: str, status: str, symbol: str = "BTC") -> None:
    store.insert_order(
        cloid=cloid,
        oid=1,
        group_id="g",
        order_ref=f"ref-{cloid}",
        order_json={"symbol": symbol},
        decision_uid=f"decision-{cloid}",
        trade_id=1,
        role="ENTRY",
        status=status,
        qty=0.1,
    )


@pytest.mark.parametrize("status", _LIVE_STATUS_CASES)
def test_live_local_orders_include_every_derived_live_status(tmp_path, status):
    """Present: a durable row in any live spelling is visible to reconciliation."""
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    _seed_status_order(store, cloid="0xlive", status=status)

    assert [row["cloid"] for row in store.live_local_orders()] == ["0xlive"]
    # A live status is a *known* status, so it never doubles as unknown state.
    assert store.local_orders_with_unknown_status() == []
    store.close()


@pytest.mark.parametrize("status", _TERMINAL_STATUS_CASES)
def test_live_local_orders_exclude_every_terminal_status(tmp_path, status):
    """Absent: a provably finished order is neither live nor unknown."""
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    _seed_status_order(store, cloid="0xdone", status=status)

    assert store.live_local_orders() == []
    assert store.local_orders_with_unknown_status() == []
    store.close()


def test_unknown_durable_status_is_never_silently_dropped(tmp_path):
    """A status outside the closed space is surfaced, not filtered away."""
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    _seed_status_order(store, cloid="0xweird", status="TRIGGER_PENDING")

    assert store.live_local_orders() == []
    unknown = store.local_orders_with_unknown_status()
    assert [row["cloid"] for row in unknown] == ["0xweird"]
    assert unknown[0]["status"] == "TRIGGER_PENDING"
    assert unknown[0]["symbol"] == "BTC"
    store.close()


def test_durable_status_space_is_derived_from_the_order_state_contract():
    """The set follows OrderState/aliases; it cannot silently fall behind."""
    from bridge.engine.types import (
        KNOWN_DURABLE_ORDER_STATUSES,
        LEGACY_LIVE_ORDER_STATUS_SPELLINGS,
        LIVE_DURABLE_ORDER_STATUSES,
        RAW_ORDER_STATUS_ALIASES,
        TERMINAL_DURABLE_ORDER_STATUSES,
        TERMINAL_ORDER_STATES,
        OrderState,
    )

    for state in OrderState:
        target = (
            TERMINAL_DURABLE_ORDER_STATUSES
            if state in TERMINAL_ORDER_STATES
            else LIVE_DURABLE_ORDER_STATUSES
        )
        assert state.value in target, state
    for raw, state in RAW_ORDER_STATUS_ALIASES.items():
        target = (
            TERMINAL_DURABLE_ORDER_STATUSES
            if state in TERMINAL_ORDER_STATES
            else LIVE_DURABLE_ORDER_STATUSES
        )
        assert raw in target, raw
    assert {"RESTING", "WAITING_CHILD"} <= LEGACY_LIVE_ORDER_STATUS_SPELLINGS
    assert LEGACY_LIVE_ORDER_STATUS_SPELLINGS <= LIVE_DURABLE_ORDER_STATUSES
    assert not (LIVE_DURABLE_ORDER_STATUSES & TERMINAL_DURABLE_ORDER_STATUSES)
    assert KNOWN_DURABLE_ORDER_STATUSES == (
        LIVE_DURABLE_ORDER_STATUSES | TERMINAL_DURABLE_ORDER_STATUSES
    )
    # The predecessor hand-written list is a strict subset of the derived one.
    assert {
        "OPEN", "SUBMITTED", "PENDING", "PENDING_NEW", "ACCEPTED",
        "PARTIALLY_FILLED", "PENDING_CANCEL",
    } <= LIVE_DURABLE_ORDER_STATUSES


# ---------------------------------------------------------------------------
# TS-P1-005 R2 / R5 — readiness recency and durable coverage continuity
# ---------------------------------------------------------------------------


def _v6_store(tmp_path, name: str = "bridge.db"):
    store = Store(tmp_path / name)
    store.initialize(target_schema_version=6)
    return store


def _ms(value):
    return int(value.timestamp() * 1000)


def _accept(
    store,
    *,
    now,
    coverage_ms: int,
    seq_hash: str = "a",
    diffs=(),
    duration_ms: int = 1,
    observed_ts=None,
    coverage_start_ms: int = 0,
    funding_rows=(),
    funding_events=(),
):
    from bridge.engine.types import (
        REQUIRED_RECONCILE_COMPONENTS,
        ComponentEvidence,
        ReconcileAttemptState,
        ReconcileComponentStatus,
        reconcile_digest,
    )

    attempt_id = store.reserve_reconcile_attempt(
        run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )
    components = tuple(
        ComponentEvidence(
            kind=kind,
            source="TEST",
            status=ReconcileComponentStatus.COMPLETE,
            observed_ts=observed_ts or now,
            rows=tuple(funding_rows) if kind.value == "FUNDING" else (),
            exact=True,
            complete=True,
            reason_code="TEST_COMPLETE",
            cursor_start_ms=coverage_start_ms if kind.value in {"FILLS", "FUNDING"} else None,
            cursor_end_ms=coverage_ms if kind.value in {"FILLS", "FUNDING"} else None,
        )
        for kind in REQUIRED_RECONCILE_COMPONENTS
    )
    payload = {
        "version": "test",
        "components": {
            component.kind.value: {
                "digest": component.digest,
                "cursor_start_ms": component.cursor_start_ms,
                "cursor_end_ms": component.cursor_end_ms,
            }
            for component in components
        },
        "diffs": [diff.canonical() for diff in diffs],
        "funding_event_ids": sorted(event.event_id for event in funding_events),
        "funding_event_digests": {
            event.event_id: event.digest for event in funding_events
        },
    }
    canonical_hash = reconcile_digest({
        "version": payload["version"],
        "components": {
            component.kind.value: component.digest for component in components
        },
        "diffs": [diff.canonical() for diff in diffs],
    })
    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.COMPLETE,
        ended_ts=now,
        duration_ms=duration_ms,
        canonical_hash=canonical_hash,
        reason_code="ACCEPTED",
        diffs=diffs,
        accepted=True,
        fresh=True,
        components=components,
        funding_events=funding_events,
        snapshot_payload=payload,
        coverage_upper_bound_ms=coverage_ms,
    )
    return attempt_id


def _fail_attempt(store, *, now, reason: str = "TESTED"):
    from bridge.engine.types import ReconcileAttemptState

    attempt_id = store.reserve_reconcile_attempt(
        run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )
    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.INCOMPLETE,
        ended_ts=now,
        duration_ms=1,
        canonical_hash=None,
        reason_code=reason,
        accepted=False,
        fresh=False,
    )
    return attempt_id


def test_a_later_failed_attempt_makes_a_young_checkpoint_not_ready(tmp_path):
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    accepted = _accept(store, now=now, coverage_ms=_ms(now))

    assert store.latest_resolved_reconcile_attempt_id() == accepted
    assert store.full_reconcile_ready(now=now, max_age_s=900.0) is True

    _fail_attempt(store, now=now + timedelta(seconds=30))
    # The checkpoint is still young and still the accepted pointer - and it is
    # no longer the most recent word on the account, so it is not ready.
    assert store.latest_accepted_reconcile_checkpoint()["attempt_id"] == accepted
    assert (
        store.full_reconcile_ready(now=now + timedelta(seconds=31), max_age_s=900.0)
        is False
    )

    # Only a fresh accept restores readiness.
    later = now + timedelta(seconds=60)
    _accept(store, now=later, coverage_ms=_ms(later), seq_hash="b")
    assert (
        store.full_reconcile_ready(now=now + timedelta(seconds=61), max_age_s=900.0)
        is True
    )
    store.close()


def test_a_restart_interrupted_attempt_makes_readiness_false(tmp_path):
    path = tmp_path / "bridge.db"
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(path)
    store.initialize(target_schema_version=6)
    _accept(store, now=now, coverage_ms=_ms(now))
    # A capture that never resolved (crash/kill).
    store.reserve_reconcile_attempt(
        run_id="run",
        started_ts=now + timedelta(seconds=30),
        deadline_s=5.0,
        max_skew_s=5.0,
    )
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=6)
    assert reopened.full_reconcile_ready(now=now, max_age_s=900.0) is True
    assert (
        reopened.resolve_interrupted_reconcile_attempts(
            observed_ts=now + timedelta(seconds=40)
        )
        == 1
    )
    assert (
        reopened.full_reconcile_ready(now=now + timedelta(seconds=41), max_age_s=900.0)
        is False
    )
    reopened.close()


def test_interrupted_attempt_order_is_wall_clock_rollback_proof(tmp_path):
    path = tmp_path / "bridge.db"
    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = Store(path)
    store.initialize(target_schema_version=6)
    accepted = _accept(store, now=now, coverage_ms=_ms(now))
    interrupted = store.reserve_reconcile_attempt(
        run_id="run",
        started_ts=now + timedelta(seconds=30),
        deadline_s=5.0,
        max_skew_s=5.0,
    )
    store.close()

    reopened = Store(path)
    reopened.initialize(target_schema_version=6)
    reopened.resolve_interrupted_reconcile_attempts(
        observed_ts=now - timedelta(minutes=5)
    )
    assert reopened.latest_resolved_reconcile_attempt_id() == interrupted
    assert reopened.latest_resolved_reconcile_attempt_id() != accepted
    assert reopened.full_reconcile_ready(now=now, max_age_s=900.0) is False
    reopened.close()


def test_store_cannot_publish_incomplete_or_nonfresh_checkpoint(tmp_path):
    from bridge.engine.types import ReconcileAttemptState
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    for fresh in (False, True):
        attempt_id = store.reserve_reconcile_attempt(
            run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
        )
        with pytest.raises(ReconcileConflictError):
            store.finalize_reconcile_attempt(
                attempt_id=attempt_id,
                state=ReconcileAttemptState.COMPLETE,
                ended_ts=now,
                duration_ms=1,
                canonical_hash="a" * 64,
                reason_code="ACCEPTED",
                components=(),
                accepted=True,
                fresh=fresh,
                snapshot_payload={"version": "test", "components": {}, "diffs": []},
                coverage_upper_bound_ms=1_000,
            )
    assert store.count_accepted_reconcile_checkpoints() == 0
    assert store.full_reconcile_ready(now=now, max_age_s=900.0) is False
    store.close()


def test_store_rejects_blocking_diff_and_over_deadline_acceptance(tmp_path):
    from bridge.engine.types import (
        ReconcileDiffKind,
        ReconcileDiffRecord,
        ReconcileOwnership,
    )
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    blocking = ReconcileDiffRecord(
        kind=ReconcileDiffKind.ORDER,
        subject="probe",
        reason_code="PROBE_BLOCK",
        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
        blocking=True,
    )
    with pytest.raises(ReconcileConflictError, match="RECONCILE_ACCEPT_BLOCKING_DIFF"):
        _accept(store, now=now, coverage_ms=_ms(now), diffs=(blocking,))
    with pytest.raises(ReconcileConflictError, match="RECONCILE_ACCEPT_ENVELOPE_INVALID"):
        _accept(
            store,
            now=now + timedelta(seconds=1),
            coverage_ms=_ms(now + timedelta(seconds=1)),
            duration_ms=5_001,
        )
    stale_now = now + timedelta(seconds=2)
    with pytest.raises(ReconcileConflictError, match="RECONCILE_ACCEPT_COMPONENT_STALE"):
        _accept(
            store,
            now=stale_now,
            coverage_ms=_ms(stale_now),
            observed_ts=stale_now - timedelta(seconds=6),
        )
    assert store.count_accepted_reconcile_checkpoints() == 0
    store.close()


def test_accepted_attempt_requires_and_derives_immutable_coverage(tmp_path):
    from bridge.engine.types import ReconcileAttemptState
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    assert store.reconcile_coverage_upper_bound_ms() is None

    attempt_id = store.reserve_reconcile_attempt(
        run_id="run", started_ts=now, deadline_s=5.0, max_skew_s=5.0
    )
    with pytest.raises(ReconcileConflictError):
        store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=ReconcileAttemptState.COMPLETE,
            ended_ts=now,
            duration_ms=1,
            canonical_hash="a" * 64,
            reason_code="ACCEPTED",
            accepted=True,
            fresh=True,
            snapshot_payload={"version": "test"},
        )
    assert store.get_reconcile_attempt(attempt_id)["state"] == "COLLECTING"
    assert store.reconcile_coverage_upper_bound_ms() is None

    # A fully proven checkpoint derives coverage from its immutable components.
    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.INCOMPLETE,
        ended_ts=now,
        duration_ms=1,
        canonical_hash=None,
        reason_code="TESTED",
        accepted=False,
        fresh=False,
    )
    first_accept = now + timedelta(seconds=1)
    first_bound = _ms(first_accept)
    _accept(store, now=first_accept, coverage_ms=first_bound)
    assert store.reconcile_coverage_upper_bound_ms() == first_bound
    assert store.get_meta("reconcile_coverage_upper_bound_ms") is None

    # A failed attempt never moves coverage.
    _fail_attempt(store, now=now + timedelta(seconds=10))
    assert store.reconcile_coverage_upper_bound_ms() == first_bound

    # Coverage is monotonic: a backwards bound is refused and rolls back whole.
    with pytest.raises(ReconcileConflictError):
        rollback = now - timedelta(seconds=20)
        _accept(store, now=rollback, coverage_ms=_ms(rollback))
    assert store.reconcile_coverage_upper_bound_ms() == first_bound
    assert store.count_accepted_reconcile_checkpoints() == 1
    store.close()


def test_store_rejects_discontinuous_accepted_coverage(tmp_path):
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    _accept(store, now=now, coverage_ms=_ms(now))
    later = now + timedelta(seconds=10)
    with pytest.raises(ReconcileConflictError, match="RECONCILE_ACCEPT_COVERAGE_GAP"):
        _accept(
            store,
            now=later,
            coverage_start_ms=_ms(now) + 1,
            coverage_ms=_ms(later),
        )


def test_store_rejects_funding_component_without_ledger_event(tmp_path):
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    funding_row = {
        "event_id": "0xfund",
        "symbol": "BTC",
        "amount_usdc": -1.0,
        "effective_ts_ms": _ms(now),
        "source": "TEST",
    }
    with pytest.raises(
        ReconcileConflictError, match="RECONCILE_ACCEPT_FUNDING_LEDGER_MISMATCH"
    ):
        _accept(
            store,
            now=now,
            coverage_ms=_ms(now),
            funding_rows=(funding_row,),
            funding_events=(),
        )
    store.close()


def test_store_rejects_semantically_different_funding_record(tmp_path):
    from bridge.engine.types import FundingEventRecord
    from bridge.store.db import ReconcileConflictError

    now = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)
    store = _v6_store(tmp_path)
    component_row = {
        "event_id": "0xfund-semantic",
        "symbol": "BTC",
        "amount_usdc": -1.0,
        "effective_ts_ms": _ms(now),
        "source": "TEST",
        "funding_rate": None,
        "position_szi": None,
        "n_samples": None,
    }
    different = FundingEventRecord(
        event_id="0xfund-semantic",
        symbol="BTC",
        amount_usdc=-9.0,
        effective_ts=now,
        source="TEST",
    )
    with pytest.raises(
        ReconcileConflictError, match="RECONCILE_ACCEPT_FUNDING_LEDGER_MISMATCH"
    ):
        _accept(
            store,
            now=now,
            coverage_ms=_ms(now),
            funding_rows=(component_row,),
            funding_events=(different,),
        )
    assert store.count_accepted_reconcile_checkpoints() == 0
    store.close()


def test_unauthorized_coverage_pointer_fails_closed_on_reopen(tmp_path):
    from bridge.store.db import MigrationError, Store

    path = tmp_path / "bridge.db"
    store = Store(path)
    store.initialize(target_schema_version=6)
    store.set_meta("reconcile_coverage_upper_bound_ms", "1234")
    store.close()

    reopened = Store(path)
    with pytest.raises(MigrationError):
        reopened.initialize(target_schema_version=6)
    reopened.close()
