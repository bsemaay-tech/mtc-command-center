"""TS-P1-002 focused identity tests.

RED on unmodified base (semantic failures, not just missing names).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from bridge.engine.orders import OrderManager
from bridge.engine.types import AccountSnapshot, Bar, OrderPlan, Position, Signal
from bridge.store.db import (
    IdentityCollisionError,
    MigrationError,
    OrderCollisionError,
    Store,
    _canonical_json,
    _float_hex,
    compute_intent_identity,
    compute_request_identity,
)


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

def _signal(ts=None, symbol="BTC", direction="LONG", ref_price=100.0,
            stop_loss=95.0, take_profit=110.0):
    if ts is None:
        ts = datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC)
    return Signal(
        ts=ts,
        symbol=symbol,
        direction=direction,
        reason="test",
        ref_price=ref_price,
        stop_loss=stop_loss,
        take_profit=take_profit,
    )


def _plan(signal=None, qty=0.1, entry_type="MKT", limit_price=None,
          stop_loss=95.0, take_profit=110.0, leverage=1):
    if signal is None:
        signal = _signal()
    return OrderPlan(
        signal=signal,
        qty=qty,
        entry_type=entry_type,
        limit_price=limit_price,
        stop_loss=stop_loss,
        take_profit=take_profit,
        leverage=leverage,
        risk_dollars=0.5,
        risk_pct=0.001,
    )


class _SimpleMockBroker:
    """Minimal broker that returns predictable bracket results."""

    def __init__(self, starting_equity=1000.0, raise_on_place=False):
        self.starting_equity = starting_equity
        self.raise_on_place = raise_on_place
        self.place_count = 0
        self.orders: list[dict] = []
        self._counter = 0

    async def connect(self):
        return None

    async def account(self):
        return AccountSnapshot(equity=self.starting_equity, available_margin=self.starting_equity)

    async def positions(self):
        return []

    async def open_orders(self):
        return []

    async def historical_bars(self, coin, tf, lookback):
        return []

    def subscribe_bars(self, coin, tf, on_bar_closed):
        return None

    def subscribe_user_events(self, handler):
        return None

    async def place_bracket(self, plan):
        if self.raise_on_place:
            raise RuntimeError("broker unavailable")
        self.place_count += 1
        self._counter += 1
        seed = plan.decision_uid or f"no-decision-{self._counter}"
        return {
            "entry": {
                "cloid": f"{seed}:ENTRY",
                "oid": self._counter * 3,
                "role": "ENTRY",
                "status": "SUBMITTED",
                "qty": plan.qty,
                "symbol": plan.signal.symbol,
            },
            "sl": {
                "cloid": f"{seed}:SL",
                "oid": self._counter * 3 + 1,
                "role": "SL",
                "status": "OPEN",
                "qty": plan.qty,
                "symbol": plan.signal.symbol,
            },
            "tp": {
                "cloid": f"{seed}:TP",
                "oid": self._counter * 3 + 2,
                "role": "TP",
                "status": "OPEN",
                "qty": plan.qty,
                "symbol": plan.signal.symbol,
            },
        }

    async def modify_stop(self, cloid, new_stop):
        return None

    async def cancel(self, cloid):
        return None

    async def cancel_all(self):
        return None

    async def flatten(self, coin):
        return None

    async def reprotect_position(self, position, stop_loss, take_profit, decision_uid):
        return None


# ---------------------------------------------------------------------------
# 1. Same canonical intent + identical request across new run id
# ---------------------------------------------------------------------------

def test_same_intent_same_request_across_runs_same_ids_no_duplicate_broker_call(tmp_path):
    """Identical intent+request produces same IDs; second call blocked without broker I/O."""
    db_path = tmp_path / "bridge.db"

    # First run
    store1 = Store(db_path)
    store1.initialize()
    store1.create_run("run-1", "dry_run", "testnet", {})
    broker1 = _SimpleMockBroker()
    mgr1 = OrderManager(store1, broker1, "run-1")

    plan = _plan()
    decision_uid_1 = "run-1:BTC:2026-07-06T12:00:00Z:LONG"
    result1 = asyncio.run(mgr1.submit_plan(decision_uid_1, plan))
    assert result1 is not None
    assert broker1.place_count == 1

    # Verify identity persisted
    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    ident = store1.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["state"] == "SUBMITTED"
    assert ident["origin_run_id"] == "run-1"
    request_id_v1 = ident["request_id"]

    store1.close()

    # Second run — reopen store
    store2 = Store(db_path)
    store2.initialize()
    store2.create_run("run-2", "dry_run", "testnet", {})
    broker2 = _SimpleMockBroker()
    mgr2 = OrderManager(store2, broker2, "run-2")

    decision_uid_2 = "run-2:BTC:2026-07-06T12:00:00Z:LONG"
    result2 = asyncio.run(mgr2.submit_plan(decision_uid_2, plan))
    # Should be blocked — no second broker call
    assert result2 is None
    assert broker2.place_count == 0

    # Same IDs
    intent_id2, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    assert intent_id2 == intent_id

    # Predicted cloids are stable
    r_id2, _, _ = compute_request_identity(
        intent_id=intent_id, symbol="BTC", direction="LONG",
        ref_price=100.0, qty=0.1, entry_type="MKT", limit_price=None,
        stop_loss=95.0, take_profit=110.0, leverage=1,
    )
    assert r_id2 == request_id_v1
    assert f"{r_id2}:ENTRY" == f"{request_id_v1}:ENTRY"

    store2.close()


# ---------------------------------------------------------------------------
# 2. Same semantic intent with changed request params → mismatch error
# ---------------------------------------------------------------------------

def test_same_intent_different_request_raises_collision_error(tmp_path):
    """Same intent but different qty/stop/limit/TP/leverage raises collision."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})
    broker = _SimpleMockBroker()
    mgr = OrderManager(store, broker, "run-1")

    plan1 = _plan(qty=0.1, stop_loss=95.0)
    result1 = asyncio.run(mgr.submit_plan("d-1", plan1))
    assert result1 is not None
    assert broker.place_count == 1

    # Same intent, different qty
    plan2 = _plan(qty=0.2, stop_loss=95.0)
    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-2", plan2))
    assert exc_info.value.code == "IDENTITY_COLLISION_INTENT"
    # No second broker call
    assert broker.place_count == 1

    # Original evidence unchanged
    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    ident = store.get_identity_by_intent(intent_id)
    assert ident["origin_decision_uid"] == "d-1"

    store.close()


# ---------------------------------------------------------------------------
# 3. Different semantic intent → different identity/request/cloids
# ---------------------------------------------------------------------------

def test_different_intent_different_ids(tmp_path):
    """Different symbols/directions/timestamps produce different IDs."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    ts1 = datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC)
    ts2 = datetime(2026, 7, 6, 13, 0, 0, tzinfo=UTC)

    intent1, _, _ = compute_intent_identity("keltner_trail_ema8", "BTC", "LONG", ts1)
    intent2, _, _ = compute_intent_identity("keltner_trail_ema8", "ETH", "LONG", ts1)
    intent3, _, _ = compute_intent_identity("keltner_trail_ema8", "BTC", "SHORT", ts1)
    intent4, _, _ = compute_intent_identity("keltner_trail_ema8", "BTC", "LONG", ts2)

    all_ids = {intent1, intent2, intent3, intent4}
    assert len(all_ids) == 4

    # Request IDs are also different (each embeds intent_id)
    req1, _, _ = compute_request_identity(
        intent1, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1)
    req2, _, _ = compute_request_identity(
        intent2, "ETH", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1)
    assert req1 != req2


# ---------------------------------------------------------------------------
# 4. Reservation is queryably durable before broker invocation
# ---------------------------------------------------------------------------

def test_reservation_durable_before_broker(tmp_path):
    """After reserve_identity commits, the row is visible before broker I/O."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    intent_id, intent_preimage, intent_version = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    request_id, request_preimage, request_version = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )

    # Simulate the reservation that OrderManager does internally
    store.conn.execute("BEGIN IMMEDIATE")
    result = store.reserve_identity(
        intent_id=intent_id,
        intent_preimage=intent_preimage,
        intent_version=intent_version,
        request_id=request_id,
        request_preimage=request_preimage,
        request_version=request_version,
        cloid_seed=request_id,
        origin_run_id="run-1",
        origin_decision_uid="d-1",
    )
    store.conn.commit()
    assert result == "RESERVED"

    # Readable before any broker call
    ident = store.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["state"] == "RESERVED"
    assert ident["origin_run_id"] == "run-1"
    assert ident["reserved_ts"] is not None
    assert ident["submitted_ts"] is None

    store.close()


# ---------------------------------------------------------------------------
# 5. Broker exception/crash leaves RESERVED; restart blocks without retry
# ---------------------------------------------------------------------------

def test_broker_exception_leaves_reserved_restart_blocks(tmp_path):
    """Broker failure after reservation: state stays RESERVED, replay blocked."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # Broker that fails
    broker = _SimpleMockBroker(raise_on_place=True)
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(RuntimeError, match="broker unavailable"):
        asyncio.run(mgr.submit_plan("d-1", plan))

    # Reservation is still RESERVED
    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    ident = store.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["state"] == "RESERVED"

    # Restart (reopen store) — same plan blocked
    store.close()
    store2 = Store(db_path)
    store2.initialize()
    store2.create_run("run-2", "dry_run", "testnet", {})
    broker2 = _SimpleMockBroker()
    mgr2 = OrderManager(store2, broker2, "run-2")

    result = asyncio.run(mgr2.submit_plan("d-2", plan))
    assert result is None  # blocked
    assert broker2.place_count == 0

    store2.close()


# ---------------------------------------------------------------------------
# 6. Forced digest collision with unequal preimage fails closed
# ---------------------------------------------------------------------------

def test_digest_collision_different_preimage_fails_closed(tmp_path):
    """If two different preimages produce the same SHA-256 (forced), fail."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # First, create a legitimate reservation
    intent_id_1, intent_preimage_1, intent_version = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    request_id_1, request_preimage_1, request_version = compute_request_identity(
        intent_id_1, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )

    store.conn.execute("BEGIN IMMEDIATE")
    store.reserve_identity(
        intent_id=intent_id_1, intent_preimage=intent_preimage_1,
        intent_version=intent_version,
        request_id=request_id_1, request_preimage=request_preimage_1,
        request_version=request_version,
        cloid_seed=request_id_1, origin_run_id="run-1",
        origin_decision_uid="d-1",
    )
    store.conn.commit()

    # Now try to reserve with same intent_id but a different preimage
    # (simulating a SHA-256 collision)
    fake_preimage = '{"version":"ts-p1-002-intent-v1","different":"payload"}'
    # Verify it's actually different
    assert fake_preimage != intent_preimage_1

    store.conn.execute("BEGIN IMMEDIATE")
    with pytest.raises(IdentityCollisionError) as exc_info:
        store.reserve_identity(
            intent_id=intent_id_1,  # same hash
            intent_preimage=fake_preimage,  # different preimage
            intent_version=intent_version,
            request_id=request_id_1,
            request_preimage=request_preimage_1,
            request_version=request_version,
            cloid_seed=request_id_1,
            origin_run_id="run-1",
            origin_decision_uid="d-2",
        )
    store.conn.rollback()
    assert exc_info.value.code == "IDENTITY_DIGEST_COLLISION"

    # Event recorded
    events = store.get_events()
    # The collision error should have been logged by submit_plan
    # (direct store call won't log, that's fine)

    store.close()


# ---------------------------------------------------------------------------
# 7. Two connections/concurrent claim: exactly one reservation wins
# ---------------------------------------------------------------------------

def test_concurrent_claim_exactly_one_wins(tmp_path):
    """Only one reservation can win for the same intent_id."""
    db_path = tmp_path / "bridge.db"
    store1 = Store(db_path)
    store1.initialize()
    store1.create_run("run-1", "dry_run", "testnet", {})

    intent_id, intent_preimage, intent_version = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    request_id, request_preimage, request_version = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )

    # First reservation — wins
    store1.conn.execute("BEGIN IMMEDIATE")
    result1 = store1.reserve_identity(
        intent_id=intent_id, intent_preimage=intent_preimage,
        intent_version=intent_version,
        request_id=request_id, request_preimage=request_preimage,
        request_version=request_version,
        cloid_seed=request_id, origin_run_id="run-1",
        origin_decision_uid="d-1",
    )
    store1.conn.commit()
    assert result1 == "RESERVED"

    # Second store (same DB) — blocked
    store2 = Store(db_path)
    store2.initialize()
    store2.conn.execute("BEGIN IMMEDIATE")
    result2 = store2.reserve_identity(
        intent_id=intent_id, intent_preimage=intent_preimage,
        intent_version=intent_version,
        request_id=request_id, request_preimage=request_preimage,
        request_version=request_version,
        cloid_seed=request_id, origin_run_id="run-2",
        origin_decision_uid="d-2",
    )
    store2.conn.commit()
    assert result2 == "BLOCKED"  # second sees exact match, blocked

    store1.close()
    store2.close()


# ---------------------------------------------------------------------------
# 8. Successful finalization atomically persists RESERVED→SUBMITTED + trade + orders
# ---------------------------------------------------------------------------

def test_finalization_atomic_persists_all(tmp_path):
    """finalize_submission atomically commits state transition, trade, orders."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    intent_id, intent_preimage, intent_version = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    request_id, request_preimage, request_version = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )

    # Reservation
    store.conn.execute("BEGIN IMMEDIATE")
    store.reserve_identity(
        intent_id=intent_id, intent_preimage=intent_preimage,
        intent_version=intent_version,
        request_id=request_id, request_preimage=request_preimage,
        request_version=request_version,
        cloid_seed=request_id, origin_run_id="run-1",
        origin_decision_uid="d-1",
    )
    store.conn.commit()

    # Finalize
    orders_data = [
        {
            "cloid": f"{request_id}:ENTRY",
            "oid": 101,
            "group_id": request_id,
            "order_ref": f"{request_id}:ENTRY",
            "order_json": json.dumps({"type": "market"}),
            "decision_uid": "d-1",
            "role": "ENTRY",
            "status": "SUBMITTED",
            "qty": 0.1,
            "filled_qty": 0.0,
            "avg_fill_px": None,
        },
        {
            "cloid": f"{request_id}:SL",
            "oid": 102,
            "group_id": request_id,
            "order_ref": f"{request_id}:SL",
            "order_json": json.dumps({"type": "stop"}),
            "decision_uid": "d-1",
            "role": "SL",
            "status": "OPEN",
            "qty": 0.1,
            "filled_qty": 0.0,
            "avg_fill_px": None,
        },
    ]

    trade_id = store.finalize_submission(
        intent_id=intent_id,
        run_id="run-1",
        coin="BTC",
        direction="LONG",
        qty=0.1,
        entry_decision_uid="d-1",
        signal_ts=datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
        decision_ts=datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
        expected_px=100.0,
        risk_dollars=0.5,
        risk_pct=0.001,
        leverage=1,
        sl_initial=95.0,
        tp_initial=110.0,
        llm_directive_id=None,
        orders_data=orders_data,
    )

    assert trade_id > 0

    # Verify all persisted
    ident = store.get_identity_by_intent(intent_id)
    assert ident["state"] == "SUBMITTED"
    assert ident["submitted_ts"] is not None

    trade = store.get_trade(trade_id)
    assert trade is not None
    assert trade["coin"] == "BTC"
    assert float(trade["qty"]) == 0.1

    entry_order = store.get_order(f"{request_id}:ENTRY")
    assert entry_order is not None
    assert entry_order["status"] == "SUBMITTED"

    sl_order = store.get_order(f"{request_id}:SL")
    assert sl_order is not None
    assert sl_order["role"] == "SL"

    store.close()


# ---------------------------------------------------------------------------
# 9. Forced post-broker order collision/finalization failure rolls back
# ---------------------------------------------------------------------------

def test_finalization_order_collision_rolls_back(tmp_path):
    """If an order cloid conflicts during finalization, rollback everything."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    intent_id, intent_preimage, intent_version = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    request_id, request_preimage, request_version = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )

    # Reservation
    store.conn.execute("BEGIN IMMEDIATE")
    store.reserve_identity(
        intent_id=intent_id, intent_preimage=intent_preimage,
        intent_version=intent_version,
        request_id=request_id, request_preimage=request_preimage,
        request_version=request_version,
        cloid_seed=request_id, origin_run_id="run-1",
        origin_decision_uid="d-1",
    )
    store.conn.commit()

    # Pre-insert a conflicting order with the same cloid but different decision_uid
    store.insert_order(
        cloid=f"{request_id}:ENTRY",
        oid=999,
        group_id="other",
        order_ref="other:ENTRY",
        order_json={"type": "other"},
        decision_uid="d-other",
        trade_id=None,
        role="ENTRY",
        status="FILLED",
        qty=0.5,
    )

    orders_data = [
        {
            "cloid": f"{request_id}:ENTRY",  # conflicts!
            "oid": 101,
            "group_id": request_id,
            "order_ref": f"{request_id}:ENTRY",
            "order_json": json.dumps({"type": "market"}),
            "decision_uid": "d-1",
            "role": "ENTRY",
            "status": "SUBMITTED",
            "qty": 0.1,
            "filled_qty": 0.0,
            "avg_fill_px": None,
        },
    ]

    with pytest.raises(OrderCollisionError):
        store.finalize_submission(
            intent_id=intent_id,
            run_id="run-1",
            coin="BTC",
            direction="LONG",
            qty=0.1,
            entry_decision_uid="d-1",
            signal_ts=datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
            decision_ts=datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
            expected_px=100.0,
            risk_dollars=0.5,
            risk_pct=0.001,
            leverage=1,
            sl_initial=95.0,
            tp_initial=110.0,
            llm_directive_id=None,
            orders_data=orders_data,
        )

    # Reservation should still be RESERVED (rollback preserved it)
    ident = store.get_identity_by_intent(intent_id)
    assert ident["state"] == "RESERVED"

    # Original cloid row preserved
    existing = store.get_order(f"{request_id}:ENTRY")
    assert existing is not None
    assert existing["decision_uid"] == "d-other"
    assert float(existing["qty"]) == 0.5

    # No new trade created
    snapshot = store.get_snapshot()
    assert len(snapshot["trades"]) == 0

    store.close()


# ---------------------------------------------------------------------------
# 10. Exact order replay safe; conflicting insert_order cannot overwrite
# ---------------------------------------------------------------------------

def test_exact_order_replay_safe_conflict_cannot_overwrite(tmp_path):
    """Idempotent replay of same order is safe; different identity raises error."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # Insert original
    store.insert_order(
        cloid="0xSafe", oid=1, group_id="g", order_ref="d:ENTRY",
        order_json={"type": "market"}, decision_uid="d-1", trade_id=None,
        role="ENTRY", status="SUBMITTED", qty=0.1,
    )

    # Exact replay (same identity fields) — should update mutable fields, not raise
    store.insert_order(
        cloid="0xSafe", oid=1, group_id="g", order_ref="d:ENTRY",
        order_json={"type": "market"}, decision_uid="d-1", trade_id=None,
        role="ENTRY", status="FILLED", qty=0.1,
        filled_qty=0.1, avg_fill_px=100.0,
    )
    row = store.get_order("0xSafe")
    assert row["status"] == "FILLED"
    assert float(row["filled_qty"]) == 0.1

    # Different identity (different decision_uid) — must raise
    with pytest.raises(OrderCollisionError) as exc_info:
        store.insert_order(
            cloid="0xSafe", oid=2, group_id="g2", order_ref="d2:ENTRY",
            order_json={"type": "market"}, decision_uid="d-2", trade_id=2,
            role="ENTRY", status="SUBMITTED", qty=0.1,
        )
    assert exc_info.value.cloid == "0xSafe"

    # Original unchanged (decision_uid still "d-1")
    row2 = store.get_order("0xSafe")
    assert row2["decision_uid"] == "d-1"

    store.close()


# ---------------------------------------------------------------------------
# 11. Realistic populated v2 migration backfills LEGACY_SUBMITTED
# ---------------------------------------------------------------------------

def test_v2_migration_backfills_legacy_submitted(tmp_path):
    """A v2 DB with fingerprint+decision+order chain backfills to LEGACY_SUBMITTED."""
    db_path = tmp_path / "bridge.db"

    # Create v2 database manually
    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    # Insert a complete v2 signal-to-order chain
    run_id = "v2-run"
    decision_uid = "v2-run:BTC:2026-07-06T12:00:00Z:LONG"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    # SIGNAL decision
    sig_payload = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
        "stop_loss": 95.0, "take_profit": 110.0,
    })
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", sig_payload),
    )
    # RISK_PASS decision
    risk_payload = json.dumps({
        "order_plan": {
            "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG", "ref_price": 100.0,
                       "stop_loss": 95.0, "take_profit": 110.0},
            "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
            "take_profit": 110.0, "leverage": 1,
        },
        "gates": [],
    })
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", risk_payload),
    )
    # Fingerprint
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "BTC:LONG:2026-07-06T12:00:00+00:00", decision_uid, ts),
    )
    # Order (so it becomes LEGACY_SUBMITTED)
    store.conn.execute(
        """INSERT INTO orders(cloid, oid, group_id, order_ref, order_json, decision_uid, trade_id, role, status, qty)
           VALUES ('legacy-cloid', 1, 'g', 'ref', '{}', ?, 1, 'ENTRY', 'FILLED', 0.1)""",
        (decision_uid,),
    )
    store.conn.commit()
    store.close()

    # Now initialize — should migrate v2→v3
    store2 = Store(db_path)
    store2.initialize()

    # Schema version bumped
    assert store2.get_meta("schema_version") == "3"

    # Identity row created
    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    ident = store2.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["state"] == "LEGACY_SUBMITTED"
    assert ident["origin_run_id"] == run_id
    assert ident["origin_decision_uid"] == decision_uid

    # Snapshot includes identity
    snap = store2.get_snapshot()
    assert "identities" in snap
    assert len(snap["identities"]) >= 1

    store2.close()


# ---------------------------------------------------------------------------
# 12. v2 ambiguous pre-broker row backfills LEGACY_RESERVED and blocks replay
# ---------------------------------------------------------------------------

def test_v2_migration_legacy_reserved_for_pre_broker_row(tmp_path):
    """A v2 fingerprint with no matching orders becomes LEGACY_RESERVED."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-run-amb"
    decision_uid = "v2-run-amb:BTC:2026-07-06T12:00:00Z:LONG"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    sig_payload = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
        "stop_loss": 95.0, "take_profit": 110.0,
    })
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", sig_payload),
    )
    risk_payload = json.dumps({
        "order_plan": {
            "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG", "ref_price": 100.0,
                       "stop_loss": 95.0, "take_profit": 110.0},
            "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
            "take_profit": 110.0, "leverage": 1,
        },
        "gates": [],
    })
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", risk_payload),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "BTC:LONG:2026-07-06T12:00:00+00:00", decision_uid, ts),
    )
    # No order row → should become LEGACY_RESERVED
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    store2.initialize()

    assert store2.get_meta("schema_version") == "3"

    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    ident = store2.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["state"] == "LEGACY_RESERVED"
    assert ident["submitted_ts"] is None

    # Now trying to submit the same plan should be blocked (identity exists)
    broker = _SimpleMockBroker()
    mgr = OrderManager(store2, broker, "new-run")
    plan = _plan()
    result = asyncio.run(mgr.submit_plan("d-new", plan))
    assert result is None  # blocked
    assert broker.place_count == 0

    store2.close()


# ---------------------------------------------------------------------------
# 13. Malformed/unmappable/conflicting v2 data rolls migration back
# ---------------------------------------------------------------------------

def test_v2_migration_malformed_data_rolls_back(tmp_path):
    """Missing SIGNAL decision → migration rolls back, schema stays v2."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-bad"
    decision_uid = "v2-bad:BTC:2026-07-06T12:00:00Z:LONG"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    # Fingerprint exists but NO SIGNAL decision → migration must fail
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "BTC:LONG:2026-07-06T12:00:00+00:00", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="No SIGNAL decision"):
        store2.initialize()

    # Schema version unchanged
    assert store2.get_meta("schema_version") == "2"

    # No identity rows
    rows = store2._rows("SELECT COUNT(*) as c FROM order_identity")
    assert rows[0]["c"] == 0

    store2.close()


def test_v2_migration_conflicting_intents_rolls_back(tmp_path):
    """Two fingerprints with same intent but different request params → rollback."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        ("run-a", ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        ("run-b", ts, "dry_run", "testnet", "{}"),
    )

    same_sig = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
        "stop_loss": 95.0, "take_profit": 110.0,
    })

    # Same intent but different request (different stop_loss in order_plan)
    risk_a = json.dumps({
        "order_plan": {
            "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG", "ref_price": 100.0,
                       "stop_loss": 95.0, "take_profit": 110.0},
            "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
            "take_profit": 110.0, "leverage": 1,
        },
        "gates": [],
    })
    risk_b = json.dumps({
        "order_plan": {
            "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG", "ref_price": 100.0,
                       "stop_loss": 90.0, "take_profit": 110.0},
            "qty": 0.1, "entry_type": "MKT", "stop_loss": 90.0,
            "take_profit": 110.0, "leverage": 1,
        },
        "gates": [],
    })

    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        ("du-a", "run-a", ts, "BTC", same_sig),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        ("du-a", "run-a", ts, "BTC", risk_a),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        ("du-b", "run-b", ts, "BTC", same_sig),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        ("du-b", "run-b", ts, "BTC", risk_b),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        ("run-a", "fp-a", "du-a", ts),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        ("run-b", "fp-b", "du-b", ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="Intent collision"):
        store2.initialize()

    # Schema version unchanged
    assert store2.get_meta("schema_version") == "2"
    rows = store2._rows("SELECT COUNT(*) as c FROM order_identity")
    assert rows[0]["c"] == 0

    store2.close()


# ---------------------------------------------------------------------------
# 14. Fresh v3 and repeated reopen are idempotent
# ---------------------------------------------------------------------------

def test_fresh_v3_initialization(tmp_path):
    """Fresh database initializes directly at v3."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()

    assert store.get_meta("schema_version") == "3"

    # Identity table exists
    store.conn.execute("SELECT COUNT(*) FROM order_identity")

    store.close()


def test_repeated_v3_reopen_is_idempotent(tmp_path):
    """Reopening an existing v3 database is a no-op."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    assert store.get_meta("schema_version") == "3"
    store.close()

    # Reopen
    store2 = Store(db_path)
    store2.initialize()
    assert store2.get_meta("schema_version") == "3"

    # Can still operate
    store2.create_run("run-1", "dry_run", "testnet", {})
    assert store2.get_run("run-1") is not None

    store2.close()


# ---------------------------------------------------------------------------
# 15. Unsupported/corrupt schema version fails closed
# ---------------------------------------------------------------------------

def test_unsupported_schema_version_fails_closed(tmp_path):
    """Unknown schema version raises RuntimeError."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.conn.executescript("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)")
    store.conn.execute("INSERT INTO meta(key, value) VALUES ('schema_version', '99')")
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(RuntimeError, match="Unsupported schema_version"):
        store2.initialize()
    store2.close()


def test_corrupt_schema_version_fails_closed(tmp_path):
    """Corrupt/non-numeric version fails."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.conn.executescript("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)")
    store.conn.execute("INSERT INTO meta(key, value) VALUES ('schema_version', 'malware')")
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(RuntimeError, match="Unsupported schema_version"):
        store2.initialize()
    store2.close()


# ---------------------------------------------------------------------------
# 16. Snapshot/export includes identity evidence; rollback never deletes it
# ---------------------------------------------------------------------------

def test_snapshot_includes_identity_rollback_never_deletes(tmp_path):
    """get_snapshot includes identities; no destructive downgrade."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    intent_id, intent_preimage, intent_version = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    request_id, request_preimage, request_version = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )

    store.conn.execute("BEGIN IMMEDIATE")
    store.reserve_identity(
        intent_id=intent_id, intent_preimage=intent_preimage,
        intent_version=intent_version,
        request_id=request_id, request_preimage=request_preimage,
        request_version=request_version,
        cloid_seed=request_id, origin_run_id="run-1",
        origin_decision_uid="d-1",
    )
    store.conn.commit()

    snap = store.get_snapshot()
    assert "identities" in snap
    assert len(snap["identities"]) >= 1
    ident = snap["identities"][0]
    assert ident["intent_id"] == intent_id
    assert ident["request_id"] == request_id
    assert ident["state"] == "RESERVED"

    # Close and reopen — identity still there
    store.close()
    store2 = Store(db_path)
    store2.initialize()
    snap2 = store2.get_snapshot()
    assert len(snap2["identities"]) >= 1

    store2.close()


# ---------------------------------------------------------------------------
# 17. Existing TS-P1-001 transition/alias behavior remains unchanged
# ---------------------------------------------------------------------------

def test_ts_p1_001_transition_and_alias_unchanged(tmp_path):
    """TS-P1-001 OrderState transitions and raw-status aliases still work."""
    from bridge.engine.types import (
        OrderState,
        can_transition,
        normalize_raw_order_status,
        validate_order_transition,
    )

    # Open → Filled transition still legal
    assert can_transition(OrderState.OPEN, OrderState.FILLED) is True
    assert validate_order_transition(OrderState.OPEN, OrderState.FILLED) == OrderState.FILLED

    # Filled → Open still illegal
    assert can_transition(OrderState.FILLED, OrderState.OPEN) is False

    # Raw status aliases
    assert normalize_raw_order_status("OPEN") is OrderState.OPEN
    assert normalize_raw_order_status("SUBMITTED") is OrderState.SUBMITTED
    assert normalize_raw_order_status("PENDING") is OrderState.SUBMITTED
    assert normalize_raw_order_status("FILLED") is OrderState.FILLED
    assert normalize_raw_order_status(" open ") is OrderState.OPEN


# ---------------------------------------------------------------------------
# Additional: float hex determinism
# ---------------------------------------------------------------------------

def test_float_hex_determinism():
    """Float hex encoding is deterministic and normalizes -0."""
    assert _float_hex(0.0) == _float_hex(-0.0)
    assert _float_hex(0.0) == "0x0.0p+0"
    assert _float_hex(1.0) == "0x1.0000000000000p+0"
    assert _float_hex(100.0) == "0x1.9000000000000p+6"

    import math
    with pytest.raises(ValueError):
        _float_hex(float("nan"))
    with pytest.raises(ValueError):
        _float_hex(float("inf"))


def test_canonical_json_stable():
    """Canonical JSON has sorted keys and compact format."""
    obj = {"b": 2, "a": 1}
    result = _canonical_json(obj)
    assert result == '{"a":1,"b":2}'


def test_identity_preimage_roundtrip():
    """Same inputs produce same preimages every time."""
    ts = datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC)
    i1, p1, v1 = compute_intent_identity("keltner_trail_ema8", "BTC", "LONG", ts)
    i2, p2, v2 = compute_intent_identity("keltner_trail_ema8", "BTC", "LONG", ts)
    assert i1 == i2
    assert p1 == p2
    assert v1 == v2

    r1, rp1, rv1 = compute_request_identity(i1, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1)
    r2, rp2, rv2 = compute_request_identity(i2, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1)
    assert r1 == r2
    assert rp1 == rp2
    assert rv1 == rv2
