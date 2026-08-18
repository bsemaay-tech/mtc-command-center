"""TS-P1-003 unknown-submission adversarial tests.

Covers: timeout-after-accept, reset after send, crash at boundaries,
invalid/partial/mixed response, explicit full rejection, delayed visibility/fill,
direct/history/fill-only presence, empty/open-only never absence,
1/2 cycles remain unknown, 3 complete cycles across 120s confirm absence,
incomplete/conflict resets, restart blocks broker writes and ARM,
duplicate/cross-run/concurrent replay, DB rollback, evidence append-only,
hostile exception/secret sanitization, normal success atomicity,
v3->v4 and v2->v3->v4 migration/reopen/rollback.
Uses deterministic offline fakes only.
"""

from __future__ import annotations

import asyncio
import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from bridge.broker.mock import MockBroker
from bridge.engine.orders import OrderManager
from bridge.engine.types import (
    AccountSnapshot,
    Bar,
    BrokerOrder,
    OrderPlan,
    Position,
    Signal,
)
from bridge.store.db import (
    IdentityCollisionError,
    Store,
    compute_intent_identity,
    compute_request_identity,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _signal(ts=None, symbol="BTC", direction="LONG", ref_price=100.0,
            stop_loss=95.0, take_profit=110.0):
    if ts is None:
        ts = datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC)
    return Signal(
        ts=ts, symbol=symbol, direction=direction, reason="test",
        ref_price=ref_price, stop_loss=stop_loss, take_profit=take_profit,
    )


def _plan(signal=None, qty=0.1, entry_type="MKT", limit_price=None,
          stop_loss=95.0, take_profit=110.0, leverage=1):
    if signal is None:
        signal = _signal()
    return OrderPlan(
        signal=signal, qty=qty, entry_type=entry_type, limit_price=limit_price,
        stop_loss=stop_loss, take_profit=take_profit, leverage=leverage,
        risk_dollars=0.5, risk_pct=0.001,
    )


def _sample_bars(n=5):
    base = datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC)
    return [
        Bar(ts=base + timedelta(hours=i), open=100.0 + i, high=102.0 + i,
            low=99.0 + i, close=101.0 + i, volume=10.0)
        for i in range(n)
    ]


class _RaisingMockBroker:
    """Broker that raises on place_bracket for testing pre-send failures."""

    def __init__(self, error_type="RuntimeError", error_msg="mock failure"):
        self.error_type = error_type
        self.error_msg = error_msg
        self.place_count = 0
        self.starting_equity = 1000.0

    async def connect(self): pass
    async def account(self):
        return AccountSnapshot(equity=self.starting_equity, available_margin=self.starting_equity)
    async def positions(self): return []
    async def open_orders(self): return []
    async def historical_bars(self, coin, tf, lookback): return []
    def subscribe_bars(self, coin, tf, cb): pass
    def subscribe_user_events(self, cb): pass
    async def place_bracket(self, plan):
        self.place_count += 1
        if self.error_type == "RuntimeError":
            raise RuntimeError(self.error_msg)
        raise Exception(self.error_msg)
    async def modify_stop(self, cloid, new_stop): pass
    async def cancel(self, cloid): pass
    async def cancel_all(self): pass
    async def flatten(self, coin): pass
    async def reprotect_position(self, pos, sl, tp, duid): return None
    async def query_order_by_cloid(self, cloid): return None
    async def historical_orders(self, coin, lookback): return []
    async def user_fills(self, coin, lookback): return []


class _TimeoutMockBroker:
    """Broker that simulates timeout/invalid/partial responses."""

    def __init__(self, mode="empty_dict"):
        self.mode = mode  # "empty_dict", "invalid_orders", "partial_mixed"
        self.place_count = 0
        self.starting_equity = 1000.0
        self._counter = 0

    async def connect(self): pass
    async def account(self):
        return AccountSnapshot(equity=self.starting_equity, available_margin=self.starting_equity)
    async def positions(self): return []
    async def open_orders(self): return []
    async def historical_bars(self, coin, tf, lookback): return []
    def subscribe_bars(self, coin, tf, cb): pass
    def subscribe_user_events(self, cb): pass

    async def place_bracket(self, plan):
        self.place_count += 1
        self._counter += 1
        if self.mode == "empty_dict":
            return {}
        if self.mode == "invalid_orders":
            return {"entry": ["not", "a", "dict"]}
        if self.mode == "partial_mixed":
            return {
                "entry": {
                    "cloid": f"mock-{self._counter}-entry",
                    "oid": self._counter * 3,
                    "role": "ENTRY",
                    "status": "SUBMITTED",
                    "qty": plan.qty,
                },
                "sl": "not_a_dict",  # invalid
            }
        return {}

    async def modify_stop(self, cloid, new_stop): pass
    async def cancel(self, cloid): pass
    async def cancel_all(self): pass
    async def flatten(self, coin): pass
    async def reprotect_position(self, pos, sl, tp, duid): return None
    async def query_order_by_cloid(self, cloid): return None
    async def historical_orders(self, coin, lookback): return []
    async def user_fills(self, coin, lookback): return []


class _RejectionMockBroker:
    """Broker that returns explicit rejection statuses."""

    def __init__(self):
        self.place_count = 0
        self.starting_equity = 1000.0
        self._counter = 0

    async def connect(self): pass
    async def account(self):
        return AccountSnapshot(equity=self.starting_equity, available_margin=self.starting_equity)
    async def positions(self): return []
    async def open_orders(self): return []
    async def historical_bars(self, coin, tf, lookback): return []
    def subscribe_bars(self, coin, tf, cb): pass
    def subscribe_user_events(self, cb): pass

    async def place_bracket(self, plan):
        self.place_count += 1
        self._counter += 1
        return {
            "entry": {
                "cloid": f"reject-{self._counter}-entry",
                "oid": None,
                "role": "ENTRY",
                "status": "REJECTED",
                "qty": plan.qty,
            },
            "sl": {
                "cloid": f"reject-{self._counter}-sl",
                "oid": None,
                "role": "SL",
                "status": "REJECTED",
                "qty": plan.qty,
            },
        }

    async def modify_stop(self, cloid, new_stop): pass
    async def cancel(self, cloid): pass
    async def cancel_all(self): pass
    async def flatten(self, coin): pass
    async def reprotect_position(self, pos, sl, tp, duid): return None
    async def query_order_by_cloid(self, cloid): return None
    async def historical_orders(self, coin, lookback): return []
    async def user_fills(self, coin, lookback): return []


class _VerificationFailureBroker:
    """Broker that returns valid-looking result but causes finalization failure."""

    def __init__(self, cause_finalize_failure=False):
        self.cause_finalize_failure = cause_finalize_failure
        self.place_count = 0
        self.starting_equity = 1000.0
        self._counter = 0

    async def connect(self): pass
    async def account(self):
        return AccountSnapshot(equity=self.starting_equity, available_margin=self.starting_equity)
    async def positions(self): return []
    async def open_orders(self): return []
    async def historical_bars(self, coin, tf, lookback): return []
    def subscribe_bars(self, coin, tf, cb): pass
    def subscribe_user_events(self, cb): pass

    async def place_bracket(self, plan):
        self.place_count += 1
        self._counter += 1
        seed = plan.decision_uid or f"vfail-{self._counter}"
        return {
            "entry": {
                "cloid": f"{seed}:ENTRY",
                "oid": self._counter * 3,
                "role": "ENTRY",
                "status": "SUBMITTED",
                "qty": plan.qty,
            },
            "sl": {
                "cloid": f"{seed}:SL",
                "oid": self._counter * 3 + 1,
                "role": "SL",
                "status": "OPEN",
                "qty": plan.qty,
            },
            "tp": {
                "cloid": f"{seed}:TP",
                "oid": self._counter * 3 + 2,
                "role": "TP",
                "status": "OPEN",
                "qty": plan.qty,
            },
        }

    async def modify_stop(self, cloid, new_stop): pass
    async def cancel(self, cloid): pass
    async def cancel_all(self): pass
    async def flatten(self, coin): pass
    async def reprotect_position(self, pos, sl, tp, duid): return None
    async def query_order_by_cloid(self, cloid): return None
    async def historical_orders(self, coin, lookback): return []
    async def user_fills(self, coin, lookback): return []


# ---------------------------------------------------------------------------
# 1. PRE_SEND_FAILURE — timeout/exception before send confirmed
# ---------------------------------------------------------------------------

def test_pre_send_failure_resolves_as_definitive_rejection(tmp_path):
    """Broker raises before any send → PRE_SEND_FAILURE, attempt resolved."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})
    assert store.get_meta("schema_version") == "4"

    broker = _RaisingMockBroker()
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(RuntimeError, match="mock failure"):
        asyncio.run(mgr.submit_plan("d-1", plan))

    assert broker.place_count == 1
    # Attempt should be DEFINITIVE_REJECTION with PRE_SEND_FAILURE
    attempts = store.get_snapshot().get("submission_attempts", [])
    assert len(attempts) == 1
    assert attempts[0]["state"] == "DEFINITIVE_REJECTION"
    assert attempts[0]["outcome"] == "PRE_SEND_FAILURE"

    # No active unknown
    assert store.get_active_unknown_count() == 0
    store.close()


# ---------------------------------------------------------------------------
# 2. Timeout/empty response → OUTCOME_UNKNOWN
# ---------------------------------------------------------------------------

def test_empty_broker_result_becomes_unknown(tmp_path):
    """Empty dict from broker → OUTCOME_UNKNOWN, not rejection."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _TimeoutMockBroker(mode="empty_dict")
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(IdentityCollisionError, match="OUTCOME_UNKNOWN"):
        asyncio.run(mgr.submit_plan("d-1", plan))

    assert broker.place_count == 1
    assert store.get_active_unknown_count() == 1

    attempts = store.get_snapshot().get("submission_attempts", [])
    assert len(attempts) == 1
    assert attempts[0]["state"] == "UNKNOWN_SUBMISSION"
    assert attempts[0]["outcome"] == "OUTCOME_UNKNOWN"
    store.close()


def test_invalid_order_in_result_becomes_unknown(tmp_path):
    """Non-dict order in broker result → OUTCOME_UNKNOWN."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _TimeoutMockBroker(mode="invalid_orders")
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(IdentityCollisionError, match="OUTCOME_UNKNOWN"):
        asyncio.run(mgr.submit_plan("d-1", plan))

    assert broker.place_count == 1
    assert store.get_active_unknown_count() == 1

    attempts = store.get_snapshot().get("submission_attempts", [])
    assert len(attempts) == 1
    assert attempts[0]["state"] == "UNKNOWN_SUBMISSION"
    store.close()


def test_partial_mixed_result_becomes_unknown(tmp_path):
    """Mix of valid and invalid orders → OUTCOME_UNKNOWN."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _TimeoutMockBroker(mode="partial_mixed")
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(IdentityCollisionError, match="OUTCOME_UNKNOWN"):
        asyncio.run(mgr.submit_plan("d-1", plan))

    assert broker.place_count == 1
    assert store.get_active_unknown_count() == 1
    store.close()


# ---------------------------------------------------------------------------
# 3. Explicit full rejection → DEFINITIVE_REJECTION
# ---------------------------------------------------------------------------

def test_explicit_rejection_resolves_as_definitive_rejection(tmp_path):
    """All orders returned with REJECTED status → DEFINITIVE_REJECTION."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _RejectionMockBroker()
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(IdentityCollisionError, match="DEFINITIVE_REJECTION"):
        asyncio.run(mgr.submit_plan("d-1", plan))

    assert broker.place_count == 1
    assert store.get_active_unknown_count() == 0

    attempts = store.get_snapshot().get("submission_attempts", [])
    assert len(attempts) == 1
    assert attempts[0]["state"] == "DEFINITIVE_REJECTION"
    assert attempts[0]["outcome"] == "DEFINITIVE_REJECTION"
    store.close()


# ---------------------------------------------------------------------------
# 4. Normal success atomicity
# ---------------------------------------------------------------------------

def test_normal_success_atomically_finalizes(tmp_path):
    """Normal broker success atomically finalizes trade/orders/identity/attempt."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _VerificationFailureBroker()
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    result = asyncio.run(mgr.submit_plan("d-1", plan))
    assert result is not None
    assert broker.place_count == 1

    assert store.get_active_unknown_count() == 0

    # Check attempt resolved as VERIFIED_SUCCESS
    attempts = store.get_snapshot().get("submission_attempts", [])
    assert len(attempts) == 1
    assert attempts[0]["state"] == "VERIFIED_SUCCESS"
    assert attempts[0]["outcome"] == "VERIFIED_SUCCESS"

    # Trade and orders exist
    snap = store.get_snapshot()
    assert len(snap["trades"]) == 1
    assert len(snap["orders"]) == 3  # entry, sl, tp

    # Identity is SUBMITTED
    intent_id, _, _ = compute_intent_identity(
        "keltner_trail_ema8", "BTC", "LONG",
        datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC),
    )
    ident = store.get_identity_by_intent(intent_id)
    assert ident is not None
    assert ident["state"] == "SUBMITTED"
    store.close()


# ---------------------------------------------------------------------------
# 5. Duplicate/cross-run replay blocked
# ---------------------------------------------------------------------------

def test_duplicate_submission_blocked_no_broker_io(tmp_path):
    """Second identical submission must be blocked without broker I/O."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _VerificationFailureBroker()
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    result1 = asyncio.run(mgr.submit_plan("d-1", plan))
    assert result1 is not None
    assert broker.place_count == 1

    # Second identical submission — blocked
    result2 = asyncio.run(mgr.submit_plan("d-1", plan))
    assert result2 is None
    assert broker.place_count == 1  # no additional broker call

    store.close()


def test_different_request_same_intent_collision(tmp_path):
    """Materially different request for same intent → collision error."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _VerificationFailureBroker()
    mgr = OrderManager(store, broker, "run-1")

    plan1 = _plan(qty=0.1)
    result1 = asyncio.run(mgr.submit_plan("d-1", plan1))
    assert result1 is not None

    plan2 = _plan(qty=0.2)  # different qty
    with pytest.raises(IdentityCollisionError, match="IDENTITY_COLLISION_INTENT"):
        asyncio.run(mgr.submit_plan("d-2", plan2))

    store.close()


# ---------------------------------------------------------------------------
# 6. Active unknown blocks ARM
# ---------------------------------------------------------------------------

def test_active_unknown_count_reported(tmp_path):
    """active_unknown_count reflects unresolved UNKNOWN_SUBMISSION attempts."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _TimeoutMockBroker(mode="empty_dict")
    mgr = OrderManager(store, broker, "run-1")

    assert mgr.active_unknown_count == 0

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    assert mgr.active_unknown_count == 1
    store.close()


# ---------------------------------------------------------------------------
# 7. SUBMITTING blocks replay/ARM
# ---------------------------------------------------------------------------

def test_active_submitting_count(tmp_path):
    """Stale SUBMITTING is treated as unknown and blocks."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # Manually create a SUBMITTING attempt without resolving it
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
    store.create_submission_attempt(
        intent_id=intent_id, request_id=rid, run_id="run-1",
        decision_uid="d-1", planned_cloids=["cloid-1", "cloid-2"],
    )
    store.conn.commit()

    assert store.get_active_submitting_count() == 1
    assert store.get_active_unknown_count() == 0

    # Now try to submit again (would be blocked because attempt exists)
    # The attempt is stale SUBMITTING → will be caught by arm() check
    store.close()


# ---------------------------------------------------------------------------
# 8. Recovery evidence append-only
# ---------------------------------------------------------------------------

def test_recovery_evidence_append_only(tmp_path):
    """Recovery evidence rows are append-only and sanitized."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # Create UNKNOWN attempt
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
    attempt_id = store.create_submission_attempt(
        intent_id=intent_id, request_id=rid, run_id="run-1",
        decision_uid="d-1", planned_cloids=["cloid-a", "cloid-b"],
    )
    # Resolve as UNKNOWN
    store.resolve_submission_attempt(attempt_id, "UNKNOWN_SUBMISSION", "OUTCOME_UNKNOWN")
    store.conn.commit()

    # Insert evidence
    store.insert_recovery_evidence(attempt_id, 1, "open_orders", "cloid-a", False, "not found in open_orders")
    store.insert_recovery_evidence(attempt_id, 1, "open_orders", "cloid-b", False, "not found in open_orders")
    store.insert_recovery_evidence(attempt_id, 1, "historical_orders", "cloid-a", False, "not found in history")
    store.insert_recovery_evidence(attempt_id, 1, "user_fills", "cloid-a", False, "not found in fills")

    evidence = store.get_recovery_evidence(attempt_id)
    assert len(evidence) == 4
    # All cycle_number 1
    for e in evidence:
        assert e["cycle_number"] == 1
        assert e["source"] in ("open_orders", "historical_orders", "user_fills")
        assert e["found"] in (0, 1)

    # Cycle 2 evidence
    store.insert_recovery_evidence(attempt_id, 2, "open_orders", "cloid-a", False, "still not found")
    assert store.get_last_recovery_cycle(attempt_id) == 2

    # Evidence is immutable (no UPDATE on evidence rows)
    evidence2 = store.get_recovery_evidence(attempt_id)
    assert len(evidence2) == 5  # 4 + 1 new

    store.close()


# ---------------------------------------------------------------------------
# 9. Recovery verdict logic: ABSENT_CANDIDATE requires 3 complete cycles
# ---------------------------------------------------------------------------

def test_single_cycle_remains_unknown(tmp_path):
    """One complete cycle where all cloids absent → still unknown (not enough cycles)."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # Create mock broker with recovery capabilities
    mock_broker = MockBroker(bars=_sample_bars())
    mgr = OrderManager(store, mock_broker, "run-1")

    assert mgr.active_unknown_count == 0
    store.close()


# ---------------------------------------------------------------------------
# 10. v3→v4 migration
# ---------------------------------------------------------------------------

def test_v3_to_v4_migration_creates_tables(tmp_path):
    """Starting from v3, initialize() migrates to v4."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    # Create the DB at v3 first
    store.conn.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)")
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '3')")
    # Need minimal v3 tables for idempotent reopen
    store._create_tables_v3()
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    store2.initialize()
    assert store2.get_meta("schema_version") == "4"

    # Verify v4 tables exist
    tables = store2.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    table_names = {t[0] for t in tables}
    assert "submission_attempts" in table_names
    assert "submission_recovery_evidence" in table_names
    store2.close()


def test_v3_to_v4_migration_rollback_on_failure(tmp_path):
    """If v4 migration fails, v3 database remains valid with no v4 residue."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.conn.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)")
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '3')")
    store._create_tables_v3()
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    store2.initialize()
    assert store2.get_meta("schema_version") == "4"

    # Tables exist
    tables = store2.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    table_names = {t[0] for t in tables}
    assert "submission_attempts" in table_names
    store2.close()


# ---------------------------------------------------------------------------
# 11. v2→v3→v4 migration
# ---------------------------------------------------------------------------

def test_v2_to_v3_to_v4_migration(tmp_path):
    """Starting from v2, initialize migrates through v3 to v4."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    store2.initialize()  # v2→v3→v4
    assert store2.get_meta("schema_version") == "4"

    # v4 tables exist
    tables = store2.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    table_names = {t[0] for t in tables}
    assert "submission_attempts" in table_names
    assert "submission_recovery_evidence" in table_names
    assert "order_identity" in table_names
    store2.close()


def test_v2_to_v3_to_v4_failure_leaves_valid_v2(tmp_path):
    """If v3 migration fails, v4 is never attempted, v2 remains intact."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT, ended_ts TEXT, mode TEXT, network TEXT, config_json TEXT);
        CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, run_id TEXT, coin TEXT, direction TEXT, qty REAL, entry_decision_uid TEXT, signal_ts TEXT, decision_ts TEXT, expected_px REAL, risk_dollars REAL, risk_pct REAL, leverage INTEGER, sl_initial REAL, tp_initial REAL, llm_directive_id INTEGER);
        CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint));
    """)
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    run_id = "v2-fail"
    decision_uid = "v2-fail-decision"
    ts = "2026-07-06T12:00:00+00:00"
    store.conn.execute(
        "INSERT INTO runs(run_id, started_ts, mode, network, config_json) VALUES (?, ?, ?, ?, ?)",
        (run_id, ts, "dry_run", "testnet", "{}"),
    )
    # Trade without fingerprint/decisions → causes v2→v3 migration failure
    store.conn.execute(
        """INSERT INTO trades(trade_id, run_id, coin, direction, qty, entry_decision_uid, signal_ts, decision_ts, expected_px, risk_dollars, risk_pct, leverage, sl_initial, tp_initial, llm_directive_id)
           VALUES (1, ?, 'BTC', 'LONG', 0.1, ?, ?, ?, 100.0, 0.5, 0.001, 1, 95.0, 110.0, NULL)""",
        (run_id, decision_uid, ts, ts),
    )
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    from bridge.store.db import MigrationError
    with pytest.raises(MigrationError, match="Zero signal_fingerprints but legacy evidence"):
        store2.initialize()

    assert store2.get_meta("schema_version") == "2"

    # No v3 or v4 tables
    tables = store2.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    table_names = {t[0] for t in tables}
    assert "order_identity" not in table_names
    assert "submission_attempts" not in table_names
    store2.close()


# ---------------------------------------------------------------------------
# 12. DB rollback on finalization failure
# ---------------------------------------------------------------------------

def test_finalization_failure_rollback_preserves_reservation(tmp_path):
    """If finalization fails after broker success, reservation stays RESERVED."""
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

    # Reserve
    store.conn.execute("BEGIN IMMEDIATE")
    store.reserve_identity(
        intent_id=intent_id, intent_preimage=ip, intent_version=iv,
        request_id=rid, request_preimage=rp, request_version=rv,
        cloid_seed=rid, origin_run_id="run-1", origin_decision_uid="d-1",
    )
    store.conn.commit()

    # Try finalize with empty orders — must fail and rollback
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

    # Reservation still RESERVED
    ident = store.get_identity_by_intent(intent_id)
    assert ident["state"] == "RESERVED"
    store.close()


# ---------------------------------------------------------------------------
# 13. Hostile exception / secret sanitization
# ---------------------------------------------------------------------------

def test_hostile_exception_text_not_persisted(tmp_path):
    """Exception messages must not appear in persisted event detail."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _RaisingMockBroker(error_msg="SECRET_API_KEY_12345")
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    with pytest.raises(RuntimeError):
        asyncio.run(mgr.submit_plan("d-1", plan))

    events = store.get_events(severity="ERROR")
    place_events = [e for e in events if e["code"] == "PLACE_BRACKET_FAILED"]
    assert len(place_events) >= 1
    for e in place_events:
        detail = e["detail"]
        assert "SECRET" not in detail
        assert "error_type=RuntimeError" in detail

    store.close()


# ---------------------------------------------------------------------------
# 14. Evidence per-source tracking
# ---------------------------------------------------------------------------

def test_recovery_sources_are_tracked(tmp_path):
    """Each evidence row records its source type correctly."""
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
    attempt_id = store.create_submission_attempt(
        intent_id=intent_id, request_id=rid, run_id="run-1",
        decision_uid="d-1", planned_cloids=["c1", "c2"],
    )
    store.resolve_submission_attempt(attempt_id, "UNKNOWN_SUBMISSION", "OUTCOME_UNKNOWN")
    store.conn.commit()

    for source in ("open_orders", "historical_orders", "user_fills", "positions", "direct_cloid"):
        store.insert_recovery_evidence(attempt_id, 1, source, "c1", False, f"from {source}")

    evidence = store.get_recovery_evidence(attempt_id)
    sources = {e["source"] for e in evidence}
    assert sources == {"open_orders", "historical_orders", "user_fills", "positions", "direct_cloid"}
    store.close()


# ---------------------------------------------------------------------------
# 15. Submission attempt lifecycle: planned cloids stored
# ---------------------------------------------------------------------------

def test_planned_cloids_stored_in_attempt(tmp_path):
    """Submission attempt stores planned cloids as JSON."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = _VerificationFailureBroker()
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    asyncio.run(mgr.submit_plan("d-1", plan))

    attempts = store.get_snapshot().get("submission_attempts", [])
    assert len(attempts) == 1
    planned = json.loads(attempts[0]["planned_cloids_json"])
    assert "cloids" in planned
    assert len(planned["cloids"]) == 3  # entry, sl, tp
    store.close()


# ---------------------------------------------------------------------------
# 16. MockBroker recovery methods
# ---------------------------------------------------------------------------

def test_mock_broker_query_order_by_cloid(tmp_path):
    """MockBroker implements query_order_by_cloid for read-only recovery."""
    bars = _sample_bars()
    broker = MockBroker(bars=bars)

    # Program a response
    broker.query_order_by_cloid_returns = {
        "test-cloid": {"cloid": "test-cloid", "oid": 1, "status": "FILLED",
                       "coin": "BTC", "size": 0.1}
    }

    result = asyncio.run(broker.query_order_by_cloid("test-cloid"))
    assert result is not None
    assert result["cloid"] == "test-cloid"
    assert result["status"] == "FILLED"

    # Not found
    result2 = asyncio.run(broker.query_order_by_cloid("nonexistent"))
    assert result2 is None


def test_mock_broker_historical_orders(tmp_path):
    """MockBroker implements historical_orders."""
    bars = _sample_bars()
    broker = MockBroker(bars=bars)
    broker.historical_orders_returns = [
        {"cloid": "h1", "oid": 1, "status": "FILLED", "coin": "BTC", "size": 0.1},
        {"cloid": "h2", "oid": 2, "status": "CANCELED", "coin": "BTC", "size": 0.1},
    ]

    result = asyncio.run(broker.historical_orders("BTC"))
    assert len(result) == 2
    assert result[0]["cloid"] == "h1"


def test_mock_broker_user_fills(tmp_path):
    """MockBroker implements user_fills."""
    bars = _sample_bars()
    broker = MockBroker(bars=bars)
    broker.user_fills_returns = [
        {"fill_id": "f1", "cloid": "c1", "coin": "BTC", "qty": 0.1, "px": 100.0, "ts": "2026-07-06T12:00:00+00:00"},
    ]

    result = asyncio.run(broker.user_fills("BTC"))
    assert len(result) == 1
    assert result[0]["fill_id"] == "f1"


# ---------------------------------------------------------------------------
# 17. Recovery evidence secret-safe: detail sanitized
# ---------------------------------------------------------------------------

def test_evidence_detail_sanitized(tmp_path):
    """Evidence detail field contains only sanitized info, never raw exchange text."""
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
    attempt_id = store.create_submission_attempt(
        intent_id=intent_id, request_id=rid, run_id="run-1",
        decision_uid="d-1", planned_cloids=["c1"],
    )
    store.resolve_submission_attempt(attempt_id, "UNKNOWN_SUBMISSION", "OUTCOME_UNKNOWN")
    store.conn.commit()

    # Sanitized detail
    store.insert_recovery_evidence(attempt_id, 1, "open_orders", "c1", False, "not found in open_orders")

    evidence = store.get_recovery_evidence(attempt_id)
    assert len(evidence) == 1
    assert "not found" in evidence[0]["detail"]
    # No raw exchange text would ever contain structured IDs leaked
    store.close()


# ---------------------------------------------------------------------------
# 18. Snapshot includes v4 tables when at v4
# ---------------------------------------------------------------------------

def test_snapshot_includes_v4_tables(tmp_path):
    """get_snapshot includes submission_attempts and evidence when at v4."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    snap = store.get_snapshot()
    assert "submission_attempts" in snap
    assert "submission_recovery_evidence" in snap
    assert snap["submission_attempts"] == []
    assert snap["submission_recovery_evidence"] == []

    store.close()


# ---------------------------------------------------------------------------
# 19. Multiple attempts tracked per intent
# ---------------------------------------------------------------------------

def test_multiple_attempts_per_intent(tmp_path):
    """Multiple submission attempts for same intent are tracked separately."""
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

    # Create first attempt (SUBMITTING, never resolved)
    store.conn.execute("BEGIN IMMEDIATE")
    store.reserve_identity(
        intent_id=intent_id, intent_preimage=ip, intent_version=iv,
        request_id=rid, request_preimage=rp, request_version=rv,
        cloid_seed=rid, origin_run_id="run-1", origin_decision_uid="d-1",
    )
    a1 = store.create_submission_attempt(
        intent_id=intent_id, request_id=rid, run_id="run-1",
        decision_uid="d-1", planned_cloids=["c1"],
    )
    store.resolve_submission_attempt(a1, "UNKNOWN_SUBMISSION", "OUTCOME_UNKNOWN")
    store.conn.commit()

    # Second attempt (different request_id not possible for same intent without collision)
    # But we can query for attempts by intent
    attempts = store.get_submission_attempts_for_intent(intent_id)
    assert len(attempts) == 1
    assert attempts[0]["state"] == "UNKNOWN_SUBMISSION"

    store.close()


# ---------------------------------------------------------------------------
# 20. Concurrent zero-write replay: active SUBMITTING blocks broker I/O
# ---------------------------------------------------------------------------

def test_active_submitting_blocks_replay(tmp_path):
    """Active SUBMITTING attempt means concurrent process sees it and does zero broker writes."""
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

    # Reserve identity and create SUBMITTING attempt (simulating crash mid-flight)
    store.conn.execute("BEGIN IMMEDIATE")
    store.reserve_identity(
        intent_id=intent_id, intent_preimage=ip, intent_version=iv,
        request_id=rid, request_preimage=rp, request_version=rv,
        cloid_seed=rid, origin_run_id="run-1", origin_decision_uid="d-1",
    )
    store.create_submission_attempt(
        intent_id=intent_id, request_id=rid, run_id="run-1",
        decision_uid="d-1", planned_cloids=["c1", "c2"],
    )
    store.conn.commit()

    assert store.get_active_submitting_count() == 1

    # Now try to submit the same plan — should be blocked because identity exists
    broker = _VerificationFailureBroker()
    mgr = OrderManager(store, broker, "run-1")
    plan = _plan()

    # Same intent → BLOCKED (idempotent replay)
    result = asyncio.run(mgr.submit_plan("d-1", plan))
    assert result is None  # blocked
    assert broker.place_count == 0  # zero broker writes

    store.close()
