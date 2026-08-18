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
