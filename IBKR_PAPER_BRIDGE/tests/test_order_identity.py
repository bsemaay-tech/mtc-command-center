"""TS-P1-002 focused identity tests.

RED on unmodified base (semantic failures, not just missing names).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import math
import sqlite3
from datetime import UTC, datetime
import datetime as _dt
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
    _finite_float,
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

    def __init__(self, starting_equity=1000.0, raise_on_place=False,
                 return_invalid=False, return_empty=False):
        self.starting_equity = starting_equity
        self.raise_on_place = raise_on_place
        self.return_invalid = return_invalid
        self.return_empty = return_empty
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

        if self.return_empty:
            return {}

        seed = plan.decision_uid or f"no-decision-{self._counter}"

        if self.return_invalid:
            return {"entry": ["not", "a", "dict"]}

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
        request_id=request_id,
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

    # Pre-insert a conflicting order with the same cloid but different identity
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
            request_id=request_id,
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
# 10b. Changed oid/group_id/order_ref each fail without modifying original
# ---------------------------------------------------------------------------

def test_changed_oid_fails_preserves_original(tmp_path):
    """Changed oid on same cloid raises OrderCollisionError without modifying original."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    store.insert_order(
        cloid="0xOidTest", oid=100, group_id="g", order_ref="ref:ENTRY",
        order_json={"type": "market"}, decision_uid="d-1", trade_id=1,
        role="ENTRY", status="SUBMITTED", qty=0.1,
    )

    with pytest.raises(OrderCollisionError):
        store.insert_order(
            cloid="0xOidTest", oid=999, group_id="g", order_ref="ref:ENTRY",
            order_json={"type": "market"}, decision_uid="d-1", trade_id=1,
            role="ENTRY", status="SUBMITTED", qty=0.1,
        )

    row = store.get_order("0xOidTest")
    assert row["oid"] == 100  # unchanged
    assert row["status"] == "SUBMITTED"  # not overwritten

    store.close()


def test_changed_group_id_fails_preserves_original(tmp_path):
    """Changed group_id on same cloid raises OrderCollisionError without modifying original."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    store.insert_order(
        cloid="0xGidTest", oid=1, group_id="original-group", order_ref="ref:ENTRY",
        order_json={"type": "market"}, decision_uid="d-1", trade_id=1,
        role="ENTRY", status="SUBMITTED", qty=0.1,
    )

    with pytest.raises(OrderCollisionError):
        store.insert_order(
            cloid="0xGidTest", oid=1, group_id="different-group", order_ref="ref:ENTRY",
            order_json={"type": "market"}, decision_uid="d-1", trade_id=1,
            role="ENTRY", status="SUBMITTED", qty=0.1,
        )

    row = store.get_order("0xGidTest")
    assert row["group_id"] == "original-group"

    store.close()


def test_changed_order_ref_fails_preserves_original(tmp_path):
    """Changed order_ref on same cloid raises OrderCollisionError without modifying original."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    store.insert_order(
        cloid="0xRefTest", oid=1, group_id="g", order_ref="orig:ENTRY",
        order_json={"type": "market"}, decision_uid="d-1", trade_id=1,
        role="ENTRY", status="SUBMITTED", qty=0.1,
    )

    with pytest.raises(OrderCollisionError):
        store.insert_order(
            cloid="0xRefTest", oid=1, group_id="g", order_ref="changed:ENTRY",
            order_json={"type": "market"}, decision_uid="d-1", trade_id=1,
            role="ENTRY", status="SUBMITTED", qty=0.1,
        )

    row = store.get_order("0xRefTest")
    assert row["order_ref"] == "orig:ENTRY"

    store.close()


# ---------------------------------------------------------------------------
# 10c. Naive timestamps are rejected by compute_intent_identity
# ---------------------------------------------------------------------------

def test_naive_timestamp_rejected(tmp_path):
    """compute_intent_identity rejects naive (no tzinfo) datetimes."""
    naive_ts = datetime(2026, 7, 6, 12, 0, 0)
    assert naive_ts.tzinfo is None

    with pytest.raises(ValueError, match="timezone-aware"):
        compute_intent_identity("keltner_trail_ema8", "BTC", "LONG", naive_ts)

    # But timezone-aware works fine
    aware_ts = datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC)
    i, p, v = compute_intent_identity("keltner_trail_ema8", "BTC", "LONG", aware_ts)
    assert i.startswith("intent-v1:")


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
        CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, run_id TEXT, coin TEXT, direction TEXT, qty REAL, entry_decision_uid TEXT, signal_ts TEXT, decision_ts TEXT, expected_px REAL, risk_dollars REAL, risk_pct REAL, leverage INTEGER, sl_initial REAL, tp_initial REAL, llm_directive_id INTEGER);
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
    # RISK_PASS decision with signal stop_loss/take_profit matching order_plan
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
    # Trade (so order-trade mapping is consistent)
    store.conn.execute(
        """INSERT INTO trades(run_id, coin, direction, qty, entry_decision_uid, signal_ts, decision_ts, expected_px, risk_dollars, risk_pct, leverage, sl_initial, tp_initial, llm_directive_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (run_id, "BTC", "LONG", 0.1, decision_uid, ts, ts, 100.0, 0.5, 0.001, 1, 95.0, 110.0, None),
    )
    # Order (so it becomes LEGACY_SUBMITTED with consistent trade mapping)
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
        CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, run_id TEXT, coin TEXT, direction TEXT, qty REAL, entry_decision_uid TEXT, signal_ts TEXT, decision_ts TEXT, expected_px REAL, risk_dollars REAL, risk_pct REAL, leverage INTEGER, sl_initial REAL, tp_initial REAL, llm_directive_id INTEGER);
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

    # No order_identity table residue in sqlite_master
    tbl = store2.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='order_identity'"
    ).fetchone()
    assert tbl is None

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

    # No order_identity table residue in sqlite_master
    tbl = store2.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='order_identity'"
    ).fetchone()
    assert tbl is None

    store2.close()


# ---------------------------------------------------------------------------
# 13b. Duplicate decision_uid in another run cannot contaminate exact-run backfill
# ---------------------------------------------------------------------------

def test_duplicate_decision_uid_other_run_does_not_contaminate(tmp_path):
    """A decision_uid appearing in a different run must not be picked up."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, run_id TEXT, coin TEXT, direction TEXT, qty REAL, entry_decision_uid TEXT, signal_ts TEXT, decision_ts TEXT, expected_px REAL, risk_dollars REAL, risk_pct REAL, leverage INTEGER, sl_initial REAL, tp_initial REAL, llm_directive_id INTEGER);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    ts = "2026-07-06T12:00:00+00:00"
    run_a = "run-a"
    run_b = "run-b"
    shared_decision_uid = "shared-decision-uid"

    # Run A: complete valid chain
    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_a, ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_b, ts, "dry_run", "testnet", "{}"),
    )

    sig_payload = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
        "stop_loss": 95.0, "take_profit": 110.0,
    })
    risk_payload = json.dumps({
        "order_plan": {
            "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG", "ref_price": 100.0,
                       "stop_loss": 95.0, "take_profit": 110.0},
            "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
            "take_profit": 110.0, "leverage": 1,
        },
        "gates": [],
    })

    # Run A: insert SIGNAL and RISK_PASS for shared_decision_uid
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (shared_decision_uid, run_a, ts, "BTC", sig_payload),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (shared_decision_uid, run_a, ts, "BTC", risk_payload),
    )

    # Run B: also insert SIGNAL but with a different RISK_PASS (should NOT be picked up)
    risk_b = json.dumps({
        "order_plan": {
            "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG", "ref_price": 100.0,
                       "stop_loss": 80.0, "take_profit": 110.0},
            "qty": 0.1, "entry_type": "MKT", "stop_loss": 80.0,
            "take_profit": 110.0, "leverage": 1,
        },
        "gates": [],
    })
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (shared_decision_uid, run_b, ts, "BTC", sig_payload),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (shared_decision_uid, run_b, ts, "BTC", risk_b),
    )

    # Fingerprint only for run_a with this decision_uid
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_a, "fp-a", shared_decision_uid, ts),
    )

    store.conn.commit()
    store.close()

    # Migration should succeed: only run_a's SIGNAL+RISK_PASS is used
    store2 = Store(db_path)
    store2.initialize()

    assert store2.get_meta("schema_version") == "3"

    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    ident = store2.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["origin_run_id"] == run_a

    store2.close()


# ---------------------------------------------------------------------------
# 13c. Duplicate SIGNAL or RISK_PASS for same run_id+decision_uid fails
# ---------------------------------------------------------------------------

def test_duplicate_signal_fails_migration(tmp_path):
    """Multiple SIGNAL decisions for same run_id+decision_uid → migration fails."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-dup"
    decision_uid = "v2-dup:BTC:2026-07-06T12:00:00Z:LONG"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    sig_payload = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
    })
    # Two SIGNAL rows
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", sig_payload),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", sig_payload),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="Multiple SIGNAL"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"

    store2.close()


def test_duplicate_risk_pass_fails_migration(tmp_path):
    """Multiple RISK_PASS decisions for same run_id+decision_uid → migration fails."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-dupr"
    decision_uid = "v2-dupr:BTC:2026-07-06T12:00:00Z:LONG"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    sig_payload = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
    })
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
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", sig_payload),
    )
    # Two RISK_PASS rows
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", risk_payload),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", risk_payload),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="Multiple RISK_PASS"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"

    store2.close()


# ---------------------------------------------------------------------------
# 13d. Orphan/cross-run order/trade mapping fails migration
# ---------------------------------------------------------------------------

def test_orphan_trade_reference_fails_migration(tmp_path):
    """Order with non-existent trade_id fails migration."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, run_id TEXT, coin TEXT, direction TEXT, qty REAL, entry_decision_uid TEXT, signal_ts TEXT, decision_ts TEXT, expected_px REAL, risk_dollars REAL, risk_pct REAL, leverage INTEGER, sl_initial REAL, tp_initial REAL, llm_directive_id INTEGER);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-orphan"
    decision_uid = "v2-orphan:BTC:2026-07-06T12:00:00Z:LONG"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    sig_payload = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
    })
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
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", sig_payload),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", risk_payload),
    )
    # Order referencing non-existent trade_id=999
    store.conn.execute(
        """INSERT INTO orders(cloid, oid, group_id, order_ref, order_json, decision_uid, trade_id, role, status, qty)
           VALUES ('orphan-cloid', 1, 'g', 'ref', '{}', ?, 999, 'ENTRY', 'FILLED', 0.1)""",
        (decision_uid,),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="non-existent trade"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"

    store2.close()


def test_cross_run_trade_mapping_fails_migration(tmp_path):
    """Order's trade entry_decision_uid doesn't match → fail migration."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, run_id TEXT, coin TEXT, direction TEXT, qty REAL, entry_decision_uid TEXT, signal_ts TEXT, decision_ts TEXT, expected_px REAL, risk_dollars REAL, risk_pct REAL, leverage INTEGER, sl_initial REAL, tp_initial REAL, llm_directive_id INTEGER);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-crossrun"
    decision_uid = "v2-crossrun:BTC:2026-07-06T12:00:00Z:LONG"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    sig_payload = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
    })
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
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", sig_payload),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", risk_payload),
    )
    # Trade exists but entry_decision_uid differs
    store.conn.execute(
        """INSERT INTO trades(trade_id, run_id, coin, direction, qty, entry_decision_uid, signal_ts, decision_ts, expected_px, risk_dollars, risk_pct, leverage, sl_initial, tp_initial, llm_directive_id)
           VALUES (1, ?, 'BTC', 'LONG', 0.1, 'different-decision', ?, ?, 100.0, 0.5, 0.001, 1, 95.0, 110.0, NULL)""",
        (run_id, ts, ts),
    )
    # Order references the trade
    store.conn.execute(
        """INSERT INTO orders(cloid, oid, group_id, order_ref, order_json, decision_uid, trade_id, role, status, qty)
           VALUES ('crossrun-cloid', 1, 'g', 'ref', '{}', ?, 1, 'ENTRY', 'FILLED', 0.1)""",
        (decision_uid,),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="cross-run"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"

    store2.close()


# ---------------------------------------------------------------------------
# 14. Fresh v3 and reopen idempotent
# ---------------------------------------------------------------------------

def test_fresh_v3_initialization(tmp_path):
    """Fresh database initializes directly at v3."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    assert store.get_meta("schema_version") == "3"
    store.close()


def test_v3_reopen_idempotent(tmp_path):
    """Reopening a v3 database is safe and idempotent."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.close()

    store2 = Store(db_path)
    store2.initialize()  # should not raise
    assert store2.get_meta("schema_version") == "3"
    store2.close()


# ---------------------------------------------------------------------------
# 15. Unsupported/corrupt schema version fails closed
# ---------------------------------------------------------------------------

def test_unsupported_schema_version_fails(tmp_path):
    """An unsupported schema_version raises an error, not a silent downgrade."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.conn.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)")
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '99')")
    store.conn.commit()

    with pytest.raises(RuntimeError, match="Unsupported schema_version='99'"):
        store.initialize()
    store.close()


def test_corrupt_schema_version_string_fails(tmp_path):
    """A non-integer schema_version fails closed."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.conn.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)")
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', 'garbage')")
    store.conn.commit()

    with pytest.raises(RuntimeError, match="Unsupported schema_version='garbage'"):
        store.initialize()
    store.close()


# ---------------------------------------------------------------------------
# 16. Snapshot/export includes identity evidence
# ---------------------------------------------------------------------------

def test_snapshot_includes_identity(tmp_path):
    """get_snapshot includes identities key."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    intent_id, ip, iv = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    rid, rp, rv = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )
    store.conn.execute("BEGIN IMMEDIATE")
    store.reserve_identity(
        intent_id=intent_id, intent_preimage=ip, intent_version=iv,
        request_id=rid, request_preimage=rp, request_version=rv,
        cloid_seed=rid, origin_run_id="run-1", origin_decision_uid="d-1",
    )
    store.conn.commit()

    snap = store.get_snapshot()
    assert "identities" in snap
    assert len(snap["identities"]) == 1

    store.close()


# ---------------------------------------------------------------------------
# 17. TS-P1-001 transition/alias behavior unchanged
# ---------------------------------------------------------------------------

def test_p1_001_behavior_unchanged(tmp_path):
    """Store methods independent of identity work normally after v3 init."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # Basic operations
    store.set_meta("test_key", "test_value")
    assert store.get_meta("test_key") == "test_value"

    store.insert_bar("BTC", "1h", datetime(2026, 7, 6, 12, 0, tzinfo=UTC),
                     100.0, 105.0, 99.0, 102.0, 10.0)

    bars = store.get_bars()
    assert len(bars) == 1
    assert bars[0]["coin"] == "BTC"

    # Events still work
    store.insert_event("run-1", datetime.now(UTC), "INFO", "TEST", "test detail")
    events = store.get_events()
    assert any(e["code"] == "TEST" for e in events)

    store.close()


# ---------------------------------------------------------------------------
# 18. Float hex and canonical JSON determinism
# ---------------------------------------------------------------------------

def test_float_hex_normalization():
    assert _float_hex(0.0) == _float_hex(-0.0)
    assert _float_hex(0.0) == "0x0.0p+0"
    with pytest.raises(ValueError):
        _float_hex(float("nan"))
    with pytest.raises(ValueError):
        _float_hex(float("inf"))


def test_canonical_json_determinism():
    a = _canonical_json({"b": 2, "a": 1})
    b = _canonical_json({"a": 1, "b": 2})
    assert a == b


# ---------------------------------------------------------------------------
# 19. Identity preimage roundtrip
# ---------------------------------------------------------------------------

def test_identity_preimage_roundtrip():
    intent_id, preimage, version = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    obj = json.loads(preimage)
    assert obj["version"] == version
    assert obj["strategy_id"] == "keltner_trail_ema8"
    assert obj["symbol"] == "BTC"
    assert obj["direction"] == "LONG"
    assert intent_id.startswith("intent-v1:")

    request_id, req_preimage, req_version = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )
    req_obj = json.loads(req_preimage)
    assert req_obj["version"] == req_version
    assert req_obj["intent_id"] == intent_id
    assert request_id.startswith("request-v1:")


# ---------------------------------------------------------------------------
# 20. Finalization rejects empty orders
# ---------------------------------------------------------------------------

def test_finalization_rejects_empty_orders(tmp_path):
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    intent_id, ip, iv = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    rid, rp, rv = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )
    store.conn.execute("BEGIN IMMEDIATE")
    store.reserve_identity(
        intent_id=intent_id, intent_preimage=ip, intent_version=iv,
        request_id=rid, request_preimage=rp, request_version=rv,
        cloid_seed=rid, origin_run_id="run-1", origin_decision_uid="d-1",
    )
    store.conn.commit()

    with pytest.raises(IdentityCollisionError, match="empty orders_data"):
        store.finalize_submission(
            intent_id=intent_id, request_id=rid, run_id="run-1",
            coin="BTC", direction="LONG", qty=0.1,
            entry_decision_uid="d-1",
            signal_ts=datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
            decision_ts=datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
            expected_px=100.0, risk_dollars=0.5, risk_pct=0.001,
            leverage=1, sl_initial=95.0, tp_initial=110.0,
            llm_directive_id=None, orders_data=[],
        )

    ident = store.get_identity_by_intent(intent_id)
    assert ident["state"] == "RESERVED"
    store.close()


# ---------------------------------------------------------------------------
# 21. plan.decision_uid restored after broker
# ---------------------------------------------------------------------------

def test_plan_decision_uid_restored_after_broker(tmp_path):
    """plan.decision_uid is restored to the original value after broker I/O."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _SimpleMockBroker()
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()
    original_duid = "run-1:BTC:2026-07-06T12:00:00Z:LONG"

    result = asyncio.run(mgr.submit_plan(original_duid, plan))
    assert result is not None

    # plan.decision_uid must have been restored
    assert plan.decision_uid == original_duid
    store.close()


# ===========================================================================
# REPAIR-2 TARGETED RED/GREEN TESTS
# ===========================================================================


# ---------------------------------------------------------------------------
# Repair 2-1: LEGACY_SUBMITTED cross-run trade detection
# ---------------------------------------------------------------------------

def test_repair2_1_cross_run_trade_run_id_mismatch_fails_migration(tmp_path):
    """Order's trade has same decision_uid but different run_id → fail."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, run_id TEXT, coin TEXT, direction TEXT, qty REAL, entry_decision_uid TEXT, signal_ts TEXT, decision_ts TEXT, expected_px REAL, risk_dollars REAL, risk_pct REAL, leverage INTEGER, sl_initial REAL, tp_initial REAL, llm_directive_id INTEGER);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_a = "run-a"
    run_b = "run-b"
    decision_uid = "target-decision"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_a, ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_b, ts, "dry_run", "testnet", "{}"),
    )
    sig_payload = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
        "stop_loss": 95.0, "take_profit": 110.0,
    })
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
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_a, ts, "BTC", sig_payload),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_a, ts, "BTC", risk_payload),
    )
    # Trade is in run_b, but fingerprint is from run_a
    store.conn.execute(
        """INSERT INTO trades(trade_id, run_id, coin, direction, qty, entry_decision_uid, signal_ts, decision_ts, expected_px, risk_dollars, risk_pct, leverage, sl_initial, tp_initial, llm_directive_id)
           VALUES (1, ?, 'BTC', 'LONG', 0.1, ?, ?, ?, 100.0, 0.5, 0.001, 1, 95.0, 110.0, NULL)""",
        (run_b, decision_uid, ts, ts),
    )
    store.conn.execute(
        """INSERT INTO orders(cloid, oid, group_id, order_ref, order_json, decision_uid, trade_id, role, status, qty)
           VALUES ('cross-cloid', 1, 'g', 'ref', '{}', ?, 1, 'ENTRY', 'FILLED', 0.1)""",
        (decision_uid,),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_a, "fp-a", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="cross-run trade"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


# ---------------------------------------------------------------------------
# Repair 2-2: NULL trade_id rejected as LEGACY_SUBMITTED
# ---------------------------------------------------------------------------

def test_repair2_2_null_trade_id_fails_migration(tmp_path):
    """Order with NULL trade_id must fail migration as incompatible."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, run_id TEXT, coin TEXT, direction TEXT, qty REAL, entry_decision_uid TEXT, signal_ts TEXT, decision_ts TEXT, expected_px REAL, risk_dollars REAL, risk_pct REAL, leverage INTEGER, sl_initial REAL, tp_initial REAL, llm_directive_id INTEGER);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-null"
    decision_uid = "v2-null-decision"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    sig_payload = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
    })
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
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", sig_payload),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", risk_payload),
    )
    # Order with NULL trade_id
    store.conn.execute(
        """INSERT INTO orders(cloid, oid, group_id, order_ref, order_json, decision_uid, trade_id, role, status, qty)
           VALUES ('null-trade-cloid', 1, 'g', 'ref', '{}', ?, NULL, 'ENTRY', 'SUBMITTED', 0.1)""",
        (decision_uid,),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="NULL trade_id"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


# ---------------------------------------------------------------------------
# Repair 2-3: Duplicate fingerprint origins comparison
# ---------------------------------------------------------------------------

def test_repair2_3_duplicate_intent_incompatible_origin_fails_migration(tmp_path):
    """Two fingerprints same intent/request but different origin_run_id → fail."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (cloid TEXT PRIMARY KEY, oid INTEGER, group_id TEXT, order_ref TEXT, order_json TEXT, decision_uid TEXT, trade_id INTEGER, role TEXT, status TEXT, qty REAL, filled_qty REAL, avg_fill_px REAL, ts_submit TEXT, ts_last TEXT);
        CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, run_id TEXT, coin TEXT, direction TEXT, qty REAL, entry_decision_uid TEXT, signal_ts TEXT, decision_ts TEXT, expected_px REAL, risk_dollars REAL, risk_pct REAL, leverage INTEGER, sl_initial REAL, tp_initial REAL, llm_directive_id INTEGER);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    ts = "2026-07-06T12:00:00+00:00"
    sig = json.dumps({
        "ts": ts, "symbol": "BTC", "direction": "LONG",
        "reason": "test", "ref_price": 100.0,
    })
    risk = json.dumps({
        "order_plan": {
            "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG", "ref_price": 100.0,
                       "stop_loss": 95.0, "take_profit": 110.0},
            "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
            "take_profit": 110.0, "leverage": 1,
        },
        "gates": [],
    })

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        ("run-x", ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        ("run-y", ts, "dry_run", "testnet", "{}"),
    )
    # Same signal, same risk → same intent + request, but different origin_run_id
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        ("du-x", "run-x", ts, "BTC", sig),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        ("du-x", "run-x", ts, "BTC", risk),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        ("du-y", "run-y", ts, "BTC", sig),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        ("du-y", "run-y", ts, "BTC", risk),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        ("run-x", "fp-x", "du-x", ts),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        ("run-y", "fp-y", "du-y", ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="incompatible origin_run_id"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


# ---------------------------------------------------------------------------
# Repair 2-4: DDL CHECK constraints prevent invalid data
# ---------------------------------------------------------------------------

def test_repair2_4_empty_intent_preimage_rejected(tmp_path):
    """Empty intent_preimage must be rejected by CHECK constraint."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            """INSERT INTO order_identity(
                 intent_id, intent_preimage, intent_version,
                 request_id, request_preimage, request_version,
                 cloid_seed, origin_run_id, origin_decision_uid,
                 state, reserved_ts, submitted_ts
               ) VALUES ('intent-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '', 'ts-p1-002-intent-v1',
                 'request-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"x":"y"}', 'ts-p1-002-request-v1',
                 'seed', 'run-1', 'd-1',
                 'RESERVED', '2026-07-06T12:00:00+00:00', NULL)"""
        )
    store.close()


def test_repair2_4_invalid_intent_version_rejected(tmp_path):
    """Wrong intent_version must be rejected by CHECK constraint."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            """INSERT INTO order_identity(
                 intent_id, intent_preimage, intent_version,
                 request_id, request_preimage, request_version,
                 cloid_seed, origin_run_id, origin_decision_uid,
                 state, reserved_ts, submitted_ts
               ) VALUES ('intent-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"v":"1"}', 'wrong-version',
                 'request-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"x":"y"}', 'ts-p1-002-request-v1',
                 'seed', 'run-1', 'd-1',
                 'RESERVED', '2026-07-06T12:00:00+00:00', NULL)"""
        )
    store.close()


def test_repair2_4_state_timestamp_inconsistency_reserved_with_submitted_ts_rejected(tmp_path):
    """RESERVED with submitted_ts non-null must be rejected."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            """INSERT INTO order_identity(
                 intent_id, intent_preimage, intent_version,
                 request_id, request_preimage, request_version,
                 cloid_seed, origin_run_id, origin_decision_uid,
                 state, reserved_ts, submitted_ts
               ) VALUES ('intent-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"v":"1"}', 'ts-p1-002-intent-v1',
                 'request-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"x":"y"}', 'ts-p1-002-request-v1',
                 'seed', 'run-1', 'd-1',
                 'RESERVED', '2026-07-06T12:00:00+00:00', '2026-07-06T12:00:00+00:00')"""
        )
    store.close()


def test_repair2_4_state_timestamp_consistency_submitted_with_null_submitted_ts_rejected(tmp_path):
    """SUBMITTED with submitted_ts NULL must be rejected."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            """INSERT INTO order_identity(
                 intent_id, intent_preimage, intent_version,
                 request_id, request_preimage, request_version,
                 cloid_seed, origin_run_id, origin_decision_uid,
                 state, reserved_ts, submitted_ts
               ) VALUES ('intent-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"v":"1"}', 'ts-p1-002-intent-v1',
                 'request-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"x":"y"}', 'ts-p1-002-request-v1',
                 'seed', 'run-1', 'd-1',
                 'SUBMITTED', '2026-07-06T12:00:00+00:00', NULL)"""
        )
    store.close()


# ---------------------------------------------------------------------------
# Repair 2-5: Exception text sanitization in events
# ---------------------------------------------------------------------------

def test_repair2_5_broker_exception_event_contains_no_raw_exc_text(tmp_path):
    """PLACE_BRACKET_FAILED event detail must contain no raw str(exc)."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _SimpleMockBroker(raise_on_place=True)
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(RuntimeError, match="broker unavailable"):
        asyncio.run(mgr.submit_plan("d-1", plan))

    # Check event detail contains no raw exception text
    events = store.get_events(severity="ERROR")
    place_events = [e for e in events if e["code"] == "PLACE_BRACKET_FAILED"]
    assert len(place_events) >= 1
    for e in place_events:
        detail = e["detail"]
        assert "broker unavailable" not in detail
        assert "decision_uid=d-1" in detail
        assert "error_type=RuntimeError" in detail
    store.close()


def test_repair2_5_collision_event_uses_exc_code(tmp_path):
    """IdentityCollisionError event must use exc.code, not hardcoded string."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _SimpleMockBroker()
    mgr = OrderManager(store, broker, "run-1")
    plan1 = _plan(qty=0.1)
    result1 = asyncio.run(mgr.submit_plan("d-1", plan1))
    assert result1 is not None

    # Causes IDENTITY_COLLISION_INTENT
    plan2 = _plan(qty=0.2)
    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-2", plan2))
    assert exc_info.value.code == "IDENTITY_COLLISION_INTENT"

    events = store.get_events(severity="ERROR")
    collision_events = [e for e in events if e["code"] == "IDENTITY_COLLISION_INTENT"]
    assert len(collision_events) >= 1
    store.close()


# ---------------------------------------------------------------------------
# Repair 2-6: compute_intent_identity rejects tzinfo with utcoffset()=None
# ---------------------------------------------------------------------------

def test_repair2_6_tzinfo_with_null_utcoffset_rejected(tmp_path):
    """tzinfo objects whose utcoffset(signal_ts) is None must be rejected."""
    FakeTZ = type('FakeTZ', (_dt.tzinfo,), {
        'utcoffset': lambda self, dt: None,
        'dst': lambda self, dt: None,
        'tzname': lambda self, dt: 'FAKE',
    })
    tz = FakeTZ()
    ts = datetime(2026, 7, 6, 12, 0, 0, tzinfo=tz)
    assert ts.tzinfo is not None
    assert ts.utcoffset() is None

    with pytest.raises(ValueError, match="concrete UTC offset"):
        compute_intent_identity("keltner_trail_ema8", "BTC", "LONG", ts)


# ---------------------------------------------------------------------------
# Repair 2-7: SIGNAL/order_plan full semantic agreement
# ---------------------------------------------------------------------------

def test_repair2_7_signal_plan_timestamp_mismatch_fails_migration(tmp_path):
    """Mismatched ts between SIGNAL and order_plan.signal must fail."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-tsmismatch"
    decision_uid = "v2-tsmismatch-decision"
    ts1 = "2026-07-06T12:00:00+00:00"
    ts2 = "2026-07-06T13:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts1, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts1, "BTC", json.dumps({
            "ts": ts1, "symbol": "BTC", "direction": "LONG",
            "reason": "test", "ref_price": 100.0,
        })),
    )
    # RISK_PASS with different ts in order_plan.signal
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts1, "BTC", json.dumps({
            "order_plan": {
                "signal": {"ts": ts2, "symbol": "BTC", "direction": "LONG",
                           "ref_price": 100.0},
                "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
                "take_profit": 110.0, "leverage": 1,
            },
            "gates": [],
        })),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts1),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="timestamp mismatch"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


def test_repair2_7_signal_plan_ref_price_mismatch_fails_migration(tmp_path):
    """Mismatched ref_price between SIGNAL and order_plan.signal must fail."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-rpmismatch"
    decision_uid = "v2-rpmismatch-decision"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "ts": ts, "symbol": "BTC", "direction": "LONG",
            "reason": "test", "ref_price": 100.0,
        })),
    )
    # RISK_PASS with different ref_price in order_plan.signal
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "order_plan": {
                "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG",
                           "ref_price": 200.0},
                "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
                "take_profit": 110.0, "leverage": 1,
            },
            "gates": [],
        })),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="ref_price mismatch"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


# ---------------------------------------------------------------------------
# Repair 2-8: broker_result validation
# ---------------------------------------------------------------------------

def test_repair2_8_empty_broker_result_leaves_reserved(tmp_path):
    """Empty broker_result must leave RESERVED and raise."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _SimpleMockBroker(return_empty=True)
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(IdentityCollisionError, match="empty or non-mapping"):
        asyncio.run(mgr.submit_plan("d-1", plan))

    assert broker.place_count == 1  # broker was called
    # Reservation should still be RESERVED
    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    ident = store.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["state"] == "RESERVED"

    # No trade or orders created
    snapshot = store.get_snapshot()
    assert len(snapshot["trades"]) == 0
    assert len(snapshot["orders"]) == 0
    store.close()


def test_repair2_8_invalid_broker_order_rejected(tmp_path):
    """Non-dict order in broker_result must be rejected."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _SimpleMockBroker(return_invalid=True)
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(IdentityCollisionError, match="non-dict order"):
        asyncio.run(mgr.submit_plan("d-1", plan))

    assert broker.place_count == 1
    # Reservation stays RESERVED
    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    ident = store.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["state"] == "RESERVED"
    store.close()


# ===========================================================================
# REPAIR-3 TARGETED RED/GREEN TESTS
# ===========================================================================


# ---------------------------------------------------------------------------
# Repair 3-1: Malformed hash rejection at DB boundary
# ---------------------------------------------------------------------------

def test_repair3_1_intent_id_too_short_rejected(tmp_path):
    """intent_id shorter than 74 chars must be rejected by CHECK."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # 73 chars (one short)
    short_id = "intent-v1:" + "a" * 63
    assert len(short_id) == 73
    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            """INSERT INTO order_identity(
                 intent_id, intent_preimage, intent_version,
                 request_id, request_preimage, request_version,
                 cloid_seed, origin_run_id, origin_decision_uid,
                 state, reserved_ts, submitted_ts
               ) VALUES (?, '{"v":"1"}', 'ts-p1-002-intent-v1',
                 'request-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"x":"y"}', 'ts-p1-002-request-v1',
                 'seed', 'run-1', 'd-1',
                 'RESERVED', '2026-07-06T12:00:00+00:00', NULL)""",
            (short_id,),
        )
    store.close()


def test_repair3_1_intent_id_uppercase_hex_rejected(tmp_path):
    """intent_id with uppercase hex chars must be rejected by CHECK."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # 74 chars but with uppercase A-F
    uc_id = "intent-v1:" + "A" * 64
    assert len(uc_id) == 74
    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            """INSERT INTO order_identity(
                 intent_id, intent_preimage, intent_version,
                 request_id, request_preimage, request_version,
                 cloid_seed, origin_run_id, origin_decision_uid,
                 state, reserved_ts, submitted_ts
               ) VALUES (?, '{"v":"1"}', 'ts-p1-002-intent-v1',
                 'request-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"x":"y"}', 'ts-p1-002-request-v1',
                 'seed', 'run-1', 'd-1',
                 'RESERVED', '2026-07-06T12:00:00+00:00', NULL)""",
            (uc_id,),
        )
    store.close()


def test_repair3_1_intent_id_non_hex_rejected(tmp_path):
    """intent_id with non-hex chars (g) must be rejected by CHECK."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # 74 chars but with 'g' in hex suffix
    bad_id = "intent-v1:" + "a" * 63 + "g"
    assert len(bad_id) == 74
    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            """INSERT INTO order_identity(
                 intent_id, intent_preimage, intent_version,
                 request_id, request_preimage, request_version,
                 cloid_seed, origin_run_id, origin_decision_uid,
                 state, reserved_ts, submitted_ts
               ) VALUES (?, '{"v":"1"}', 'ts-p1-002-intent-v1',
                 'request-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"x":"y"}', 'ts-p1-002-request-v1',
                 'seed', 'run-1', 'd-1',
                 'RESERVED', '2026-07-06T12:00:00+00:00', NULL)""",
            (bad_id,),
        )
    store.close()


def test_repair3_1_request_id_too_short_rejected(tmp_path):
    """request_id shorter than 75 chars must be rejected by CHECK."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # 74 chars (one short)
    short_id = "request-v1:" + "a" * 63
    assert len(short_id) == 74
    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute(
            """INSERT INTO order_identity(
                 intent_id, intent_preimage, intent_version,
                 request_id, request_preimage, request_version,
                 cloid_seed, origin_run_id, origin_decision_uid,
                 state, reserved_ts, submitted_ts
               ) VALUES ('intent-v1:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
                 '{"v":"1"}', 'ts-p1-002-intent-v1',
                 ?, '{"x":"y"}', 'ts-p1-002-request-v1',
                 'seed', 'run-1', 'd-1',
                 'RESERVED', '2026-07-06T12:00:00+00:00', NULL)""",
            (short_id,),
        )
    store.close()


def test_repair3_1_valid_generated_ids_pass_check(tmp_path):
    """Generated intent_id and request_id must pass CHECK and be insertable."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    intent_id, ip, iv = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    rid, rp, rv = compute_request_identity(
        intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 1,
    )

    # Verify exact lengths
    assert len(intent_id) == 74
    assert len(rid) == 75

    # Verify successful insert (no IntegrityError)
    store.conn.execute("BEGIN IMMEDIATE")
    result = store.reserve_identity(
        intent_id=intent_id, intent_preimage=ip, intent_version=iv,
        request_id=rid, request_preimage=rp, request_version=rv,
        cloid_seed=rid, origin_run_id="run-1", origin_decision_uid="d-1",
    )
    store.conn.commit()
    assert result == "RESERVED"

    ident = store.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["state"] == "RESERVED"

    store.close()


# ---------------------------------------------------------------------------
# Repair 3-2: Migration signal stop_loss/take_profit vs order_plan comparison
# ---------------------------------------------------------------------------

def test_repair3_2_signal_plan_stop_loss_mismatch_fails_migration(tmp_path):
    """Different stop_loss between plan_signal and order_plan must fail."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-slmismatch"
    decision_uid = "v2-slmismatch-decision"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "ts": ts, "symbol": "BTC", "direction": "LONG",
            "reason": "test", "ref_price": 100.0,
            "stop_loss": 95.0, "take_profit": 110.0,
        })),
    )
    # RISK_PASS: signal.stop_loss=95.0 but order_plan.stop_loss=90.0
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "order_plan": {
                "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG",
                           "ref_price": 100.0, "stop_loss": 95.0,
                           "take_profit": 110.0},
                "qty": 0.1, "entry_type": "MKT", "stop_loss": 90.0,
                "take_profit": 110.0, "leverage": 1,
            },
            "gates": [],
        })),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="stop_loss mismatch"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


def test_repair3_2_signal_plan_take_profit_mismatch_fails_migration(tmp_path):
    """Different take_profit between plan_signal and order_plan must fail."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-tpmismatch"
    decision_uid = "v2-tpmismatch-decision"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "ts": ts, "symbol": "BTC", "direction": "LONG",
            "reason": "test", "ref_price": 100.0,
            "stop_loss": 95.0, "take_profit": 110.0,
        })),
    )
    # RISK_PASS: signal.take_profit=110.0 but order_plan.take_profit=120.0
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "order_plan": {
                "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG",
                           "ref_price": 100.0, "stop_loss": 95.0,
                           "take_profit": 110.0},
                "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
                "take_profit": 120.0, "leverage": 1,
            },
            "gates": [],
        })),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="take_profit mismatch"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


def test_repair3_2_signal_plan_take_profit_none_mismatch_fails_migration(tmp_path):
    """Signal take_profit=None but order_plan has a value must fail."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-tpnone"
    decision_uid = "v2-tpnone-decision"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "ts": ts, "symbol": "BTC", "direction": "LONG",
            "reason": "test", "ref_price": 100.0,
            "stop_loss": 95.0, "take_profit": 110.0,
        })),
    )
    # RISK_PASS: signal has no take_profit but order_plan does
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "order_plan": {
                "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG",
                           "ref_price": 100.0, "stop_loss": 95.0},
                "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
                "take_profit": 110.0, "leverage": 1,
            },
            "gates": [],
        })),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="take_profit None mismatch"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


# ---------------------------------------------------------------------------
# Repair 3-3: Exact adjacent-float ref_price mismatch rejects migration
# ---------------------------------------------------------------------------

def test_repair3_3_exact_adjacent_float_ref_mismatch_fails_migration(tmp_path):
    """Ref price differing by 1 ULP must fail (no epsilon tolerance)."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-adjfloat"
    decision_uid = "v2-adjfloat-decision"
    ts = "2026-07-06T12:00:00+00:00"
    import math as _math
    # Two floats that are adjacent in IEEE-754 representation
    ref_a = 100.0
    ref_b = _math.nextafter(100.0, 200.0)  # next representable float after 100.0
    assert ref_b != ref_a
    assert abs(ref_a - ref_b) < 1e-12  # would pass epsilon check

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "ts": ts, "symbol": "BTC", "direction": "LONG",
            "reason": "test", "ref_price": ref_a,
        })),
    )
    # RISK_PASS with ref_b (adjacent float, would pass epsilon but fail exact hex)
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "order_plan": {
                "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG",
                           "ref_price": ref_b, "stop_loss": 95.0,
                           "take_profit": 110.0},
                "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
                "take_profit": 110.0, "leverage": 1,
            },
            "gates": [],
        })),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="ref_price mismatch"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


# ---------------------------------------------------------------------------
# Repair 3-4: Equivalent timestamp spellings accepted
# ---------------------------------------------------------------------------

def test_repair3_4_equivalent_timestamp_spellings_accepted(tmp_path):
    """Z vs +00:00 timestamp spellings representing same instant must be accepted."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-eqts"
    decision_uid = "v2-eqts-decision"
    ts_z = "2026-07-06T12:00:00Z"
    ts_offset = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts_z, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts_z, "BTC", json.dumps({
            "ts": ts_z, "symbol": "BTC", "direction": "LONG",
            "reason": "test", "ref_price": 100.0,
            "stop_loss": 95.0, "take_profit": 110.0,
        })),
    )
    # RISK_PASS uses +00:00 spelling (same instant as Z)
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts_z, "BTC", json.dumps({
            "order_plan": {
                "signal": {"ts": ts_offset, "symbol": "BTC", "direction": "LONG",
                           "ref_price": 100.0, "stop_loss": 95.0,
                           "take_profit": 110.0},
                "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
                "take_profit": 110.0, "leverage": 1,
            },
            "gates": [],
        })),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts_z),
    )
    store.conn.commit()
    store.close()

    # Migration should succeed — equivalent spellings are the same instant
    store2 = Store(db_path)
    store2.initialize()
    assert store2.get_meta("schema_version") == "3"
    store2.close()


# ---------------------------------------------------------------------------
# Repair 3-5: Non-integral leverage rejected
# ---------------------------------------------------------------------------

def test_repair3_5_non_integral_leverage_rejected_by_compute_request_identity():
    """compute_request_identity must reject non-integral leverage."""
    intent_id = "intent-v1:" + "a" * 64
    with pytest.raises(ValueError, match="leverage must be a true int"):
        compute_request_identity(
            intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 2.5,
        )

    # Bool rejected (isinstance(True, int) is True in Python)
    with pytest.raises(ValueError, match="leverage must be a true int"):
        compute_request_identity(
            intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, True,
        )

    # Zero/negative rejected
    with pytest.raises(ValueError, match="leverage must be positive"):
        compute_request_identity(
            intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, 110.0, 0,
        )


def test_repair3_5_non_integral_leverage_fails_migration(tmp_path):
    """v2 migration with non-integral leverage must fail."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, decision_uid TEXT NOT NULL, run_id TEXT, ts TEXT, coin TEXT, stage TEXT, trade_id INTEGER, payload_json TEXT, payload_version INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()

    run_id = "v2-leverage"
    decision_uid = "v2-leverage-decision"
    ts = "2026-07-06T12:00:00+00:00"

    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'SIGNAL', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "ts": ts, "symbol": "BTC", "direction": "LONG",
            "reason": "test", "ref_price": 100.0,
            "stop_loss": 95.0, "take_profit": 110.0,
        })),
    )
    # Non-integral leverage 2.5
    store.conn.execute(
        "INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, payload_json) VALUES (?, ?, ?, ?, 'RISK_PASS', ?)",
        (decision_uid, run_id, ts, "BTC", json.dumps({
            "order_plan": {
                "signal": {"ts": ts, "symbol": "BTC", "direction": "LONG",
                           "ref_price": 100.0, "stop_loss": 95.0,
                           "take_profit": 110.0},
                "qty": 0.1, "entry_type": "MKT", "stop_loss": 95.0,
                "take_profit": 110.0, "leverage": 2.5,
            },
            "gates": [],
        })),
    )
    store.conn.execute(
        "INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts) VALUES (?, ?, ?, ?)",
        (run_id, "fp", decision_uid, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    with pytest.raises(MigrationError, match="Non-integral leverage"):
        store2.initialize()
    assert store2.get_meta("schema_version") == "2"
    store2.close()


# ---------------------------------------------------------------------------
# Repair 3-6: Non-finite float rejection in compute_request_identity
# ---------------------------------------------------------------------------

def test_repair3_6_nan_ref_price_rejected():
    """NaN ref_price must be rejected."""
    intent_id = "intent-v1:" + "a" * 64
    with pytest.raises(ValueError, match="ref_price must be finite"):
        compute_request_identity(
            intent_id, "BTC", "LONG", float("nan"), 0.1, "MKT", None, 95.0, 110.0, 1,
        )


def test_repair3_6_inf_qty_rejected():
    """Infinity qty must be rejected."""
    intent_id = "intent-v1:" + "a" * 64
    with pytest.raises(ValueError, match="qty must be finite"):
        compute_request_identity(
            intent_id, "BTC", "LONG", 100.0, float("inf"), "MKT", None, 95.0, 110.0, 1,
        )


def test_repair3_6_nan_take_profit_rejected():
    """NaN take_profit must be rejected."""
    intent_id = "intent-v1:" + "a" * 64
    with pytest.raises(ValueError, match="take_profit must be finite"):
        compute_request_identity(
            intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, 95.0, float("nan"), 1,
        )


def test_repair3_6_nan_limit_price_rejected():
    """NaN limit_price must be rejected."""
    intent_id = "intent-v1:" + "a" * 64
    with pytest.raises(ValueError, match="limit_price must be finite"):
        compute_request_identity(
            intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", float("nan"), 95.0, 110.0, 1,
        )


def test_repair3_6_nan_stop_loss_rejected():
    """NaN stop_loss must be rejected."""
    intent_id = "intent-v1:" + "a" * 64
    with pytest.raises(ValueError, match="stop_loss must be finite"):
        compute_request_identity(
            intent_id, "BTC", "LONG", 100.0, 0.1, "MKT", None, float("nan"), 110.0, 1,
        )
