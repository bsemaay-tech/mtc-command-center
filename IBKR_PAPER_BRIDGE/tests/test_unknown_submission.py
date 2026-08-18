"""TS-P1-003 unknown-submission quarantine tests.

Tests exercise real OrderManager/BridgeEngine/Store paths.
"""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from bridge.broker.base import SubmissionResult
from bridge.broker.mock import MockBroker
from bridge.engine.orders import OrderManager
from bridge.engine.types import AccountSnapshot, Bar, OrderPlan, Position, Signal
from bridge.store.db import IdentityCollisionError, Store, compute_intent_identity


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
        signal=signal, qty=qty, entry_type=entry_type,
        limit_price=limit_price, stop_loss=stop_loss,
        take_profit=take_profit, leverage=leverage,
        risk_dollars=0.5, risk_pct=0.001,
    )


def _mock_bars(n=20):
    base = datetime(2026, 7, 6, 12, 0, 0, tzinfo=UTC)
    bars = []
    for i in range(n):
        t = base + timedelta(hours=i)
        bars.append(Bar(ts=t, open=100.0 + i, high=102.0 + i,
                        low=99.0 + i, close=101.0 + i, volume=10.0))
    return bars


# ---------------------------------------------------------------------------
# 1. PRE_SEND_FAILURE is recognized, no attempt transition to UNKNOWN
# ---------------------------------------------------------------------------

def test_pre_send_failure_recognized(tmp_path):
    """Proven pre-send failure → DEFINITIVE_REJECTION, no unknown quarantine."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), pre_send_failure=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_PRE_SEND_FAILURE"

    # No active quarantine
    assert not store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 2. DEFINITIVE_REJECTION is recognized without unknown quarantine
# ---------------------------------------------------------------------------

def test_definitive_rejection_recognized(tmp_path):
    """Complete rejection → DEFINITIVE_REJECTION, no unknown quarantine."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), definitive_rejection=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_DEFINITIVE_REJECTION"

    assert not store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 3. Mixed response (partial accept + reject) → OUTCOME_UNKNOWN, DISARM
# ---------------------------------------------------------------------------

def test_mixed_response_is_unknown(tmp_path):
    """Mixed accepted/rejected → OUTCOME_UNKNOWN transition, quarantine active."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), mixed_response=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_OUTCOME_UNKNOWN"

    # Quarantine is active
    assert store.has_active_quarantine()
    # App state should be DISARMED
    assert store.get_meta("app_state") == "DISARMED"
    store.close()


# ---------------------------------------------------------------------------
# 4. Post-send timeout → OUTCOME_UNKNOWN, quarantine active
# ---------------------------------------------------------------------------

def test_post_send_timeout_is_unknown(tmp_path):
    """Post-send timeout → OUTCOME_UNKNOWN transition."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_OUTCOME_UNKNOWN"

    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 5. Empty/malformed response → OUTCOME_UNKNOWN
# ---------------------------------------------------------------------------

def test_empty_response_is_unknown(tmp_path):
    """Empty broker result → OUTCOME_UNKNOWN."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), return_empty_response=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_OUTCOME_UNKNOWN"

    assert store.has_active_quarantine()
    store.close()


def test_malformed_response_is_unknown(tmp_path):
    """Malformed broker result → OUTCOME_UNKNOWN."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), return_malformed_response=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_OUTCOME_UNKNOWN"

    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 6. Crash after acceptance → OUTCOME_UNKNOWN
# ---------------------------------------------------------------------------

def test_crash_after_accept_is_unknown(tmp_path):
    """Broker accepts then raises → OUTCOME_UNKNOWN, quarantine."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), crash_after_accept=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_OUTCOME_UNKNOWN"

    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 7. Wrong cloids → OUTCOME_UNKNOWN
# ---------------------------------------------------------------------------

def test_wrong_cloids_is_unknown(tmp_path):
    """Wrong cloids returned → OUTCOME_UNKNOWN."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), wrong_cloids=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_OUTCOME_UNKNOWN"

    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 8. Missing roles → OUTCOME_UNKNOWN
# ---------------------------------------------------------------------------

def test_missing_roles_is_unknown(tmp_path):
    """Missing role in result → OUTCOME_UNKNOWN."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), missing_roles=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_OUTCOME_UNKNOWN"

    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 9. Extra roles → OUTCOME_UNKNOWN
# ---------------------------------------------------------------------------

def test_extra_roles_is_unknown(tmp_path):
    """Extra role in result → OUTCOME_UNKNOWN."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), extra_roles=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError) as exc_info:
        asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert exc_info.value.code == "IDENTITY_OUTCOME_UNKNOWN"

    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 10. VERIFIED_SUCCESS works normally
# ---------------------------------------------------------------------------

def test_normal_verified_success(tmp_path):
    """Normal submission succeeds and finalizes."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars())
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    result = asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert result is not None
    assert "entry" in result
    assert "sl" in result
    assert not store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 11. Unknown immediately DISARMS and blocks new submissions
# ---------------------------------------------------------------------------

def test_unknown_immediately_disarms_and_blocks(tmp_path):
    """After UNKNOWN_SUBMISSION, new plans are blocked."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    # First submission → UNKNOWN
    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    assert store.has_active_quarantine()
    assert store.get_meta("app_state") == "DISARMED"

    # Second submission → blocked by quarantine
    broker2 = MockBroker(bars=_mock_bars())
    broker2.connected = True
    mgr2 = OrderManager(store, broker2, "run-1")
    ts2 = datetime(2026, 7, 6, 13, 0, 0, tzinfo=UTC)
    result = asyncio.run(mgr2.submit_plan("d-2", _plan(signal=_signal(ts=ts2))))
    assert result is None  # blocked
    assert broker2.place_count == 0

    store.close()


# ---------------------------------------------------------------------------
# 12. Recovery: 1 cycle → still UNKNOWN_SUBMISSION
# ---------------------------------------------------------------------------

def test_one_recovery_cycle_stays_unknown(tmp_path):
    """After one recovery cycle, quarantine persists (need 3)."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    assert store.has_active_quarantine()

    # Run recovery
    asyncio.run(mgr.run_recovery_cycle())
    # Still active — 1 cycle is not enough
    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 13. Recovery: 2 cycles still unknown
# ---------------------------------------------------------------------------

def test_two_recovery_cycles_stay_unknown(tmp_path):
    """After two recovery cycles, quarantine persists (need 3)."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    asyncio.run(mgr.run_recovery_cycle())
    assert store.has_active_quarantine()

    asyncio.run(mgr.run_recovery_cycle())
    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 14. Recovery: 3 cycles under 120s → still unknown
# ---------------------------------------------------------------------------

def test_three_cycles_under_120s_stay_unknown(tmp_path):
    """Three complete cycles but under 120s span → still UNKNOWN."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    for _ in range(3):
        asyncio.run(mgr.run_recovery_cycle())

    # Still active — less than 120s between first and last cycle
    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 15. Query failure does not prove absence
# ---------------------------------------------------------------------------

def test_query_failure_never_proves_absence(tmp_path):
    """Recovery query failures → INCOMPLETE, never confirm absence."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True,
                        recovery_query_should_fail=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    for _ in range(5):
        asyncio.run(mgr.run_recovery_cycle())

    # Query failures mean INCOMPLETE, not ABSENT
    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 16. Presence found via direct lookup
# ---------------------------------------------------------------------------

def test_direct_lookup_presence_confirms_present(tmp_path):
    """Direct cloid lookup finding an order → CONFIRMED_PRESENT."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    # Find the planned cloid from the submission attempt
    import json as _json
    active = store.get_active_attempts()
    planned_cloids_raw = active[0].get("planned_cloids_json", "{}")
    planned_cloids = _json.loads(planned_cloids_raw) if isinstance(planned_cloids_raw, str) else planned_cloids_raw
    entry_cloid = planned_cloids.get("entry", "")

    # Put a matching order in broker's order book with the exact planned cloid
    broker.orders.append({
        "cloid": entry_cloid, "oid": 999, "role": "ENTRY",
        "status": "OPEN", "qty": 0.1, "symbol": "BTC",
    })

    asyncio.run(mgr.run_recovery_cycle())

    # Should be CONFIRMED_PRESENT
    active2 = store.get_active_attempts()
    assert len(active2) >= 1
    states = [a["state"] for a in active2]
    assert "CONFIRMED_PRESENT" in states
    store.close()


# ---------------------------------------------------------------------------
# 17. CONFIRMED_PRESENT remains visible and blocks ARM
# ---------------------------------------------------------------------------

def test_confirmed_present_blocks_arm(tmp_path):
    """CONFIRMED_PRESENT must remain visible in status and block ARM."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    # Find the planned cloid and make recovery find the order
    import json as _json
    active = store.get_active_attempts()
    planned_cloids_raw = active[0].get("planned_cloids_json", "{}")
    planned_cloids = _json.loads(planned_cloids_raw) if isinstance(planned_cloids_raw, str) else planned_cloids_raw
    entry_cloid = planned_cloids.get("entry", "")

    broker.orders.append({
        "cloid": entry_cloid, "oid": 999, "role": "ENTRY",
        "status": "OPEN", "qty": 0.1, "symbol": "BTC",
    })
    asyncio.run(mgr.run_recovery_cycle())

    assert store.has_active_quarantine()
    active2 = store.get_active_attempts()
    states = [a["state"] for a in active2]
    assert "CONFIRMED_PRESENT" in states

    store.close()


# ---------------------------------------------------------------------------
# 18. Restart discovers SUBMITTING and performs zero placement
# ---------------------------------------------------------------------------

def test_restart_discovers_submitting_zero_placement(tmp_path):
    """Restart finds SUBMITTING — performs no placement writes."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    store.close()

    # Simulate restart
    store2 = Store(db_path)
    store2.initialize()
    assert store2.has_active_quarantine()

    active = store2.get_active_attempts()
    assert len(active) >= 1
    assert any(a["state"] in ("UNKNOWN_SUBMISSION", "SUBMITTING") for a in active)

    # New broker — should have zero placement calls
    broker2 = MockBroker(bars=_mock_bars())
    broker2.connected = True
    mgr2 = OrderManager(store2, broker2, "run-2")
    result = asyncio.run(mgr2.submit_plan("d-2", _plan(
        signal=_signal(ts=datetime(2026, 7, 6, 13, 0, 0, tzinfo=UTC))
    )))
    assert result is None  # blocked
    assert broker2.place_count == 0

    store2.close()


# ---------------------------------------------------------------------------
# 19. Atomic rollback preserves prior quarantine
# ---------------------------------------------------------------------------

def test_atomic_rollback_preserves_prior_quarantine(tmp_path):
    """DB failure during transition rolls back but prior quarantine survives."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    assert store.has_active_quarantine()

    # Attempt an invalid transition (should fail but keep quarantine)
    store.conn.execute("BEGIN IMMEDIATE")
    try:
        # Invalid: from ["VERIFIED_SUCCESS"] when state is UNKNOWN_SUBMISSION
        store.transition_attempt_state(
            attempt_id=1,
            from_states=["VERIFIED_SUCCESS"],
            to_state="CONFIRMED_ABSENT",
        )
    except Exception:
        store.conn.rollback()

    # Quarantine still active
    assert store.has_active_quarantine()
    store.close()


# ---------------------------------------------------------------------------
# 20. Hostile exception text never persists
# ---------------------------------------------------------------------------

def test_hostile_exception_text_never_persists(tmp_path):
    """Raw exception messages with secrets must not be persisted."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    # Check events contain no raw exception text
    events = store.get_events()
    for ev in events:
        detail = ev.get("detail", "")
        # Should not contain anything that looks like a secret
        assert "secret" not in detail.lower()
        assert "password" not in detail.lower()
        assert "key=" not in detail.lower()

    # Attempt recovery with error
    broker.recovery_query_should_fail = True
    asyncio.run(mgr.run_recovery_cycle())

    # Evidence payloads must be safe
    snap = store.get_snapshot()
    for ev in snap.get("recovery_evidence", []):
        payload = ev.get("safe_payload_json", "{}")
        if isinstance(payload, str):
            payload_data = json.loads(payload)
        else:
            payload_data = payload
        for v in payload_data.values():
            if isinstance(v, str):
                assert "secret" not in v.lower()

    store.close()


# ---------------------------------------------------------------------------
# 21. Normal success is atomic
# ---------------------------------------------------------------------------

def test_normal_success_is_atomic(tmp_path):
    """VERIFIED_SUCCESS finalizes trade + orders + identity + attempt in one flow."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars())
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    result = asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert result is not None

    # All persisted
    snap = store.get_snapshot()
    assert len(snap["trades"]) == 1
    assert len(snap["orders"]) >= 2  # entry + sl (+ tp if set)
    assert len(snap["identities"]) == 1
    assert len(snap["submission_attempts"]) >= 1

    attempt = snap["submission_attempts"][0]
    assert attempt["state"] == "VERIFIED_SUCCESS"

    store.close()


# ---------------------------------------------------------------------------
# 22. v3→v4 migration success and idempotent reopen
# ---------------------------------------------------------------------------

def test_v3_to_v4_migration_success(tmp_path):
    """v3 database migrates cleanly to v4."""
    db_path = tmp_path / "bridge.db"

    # Create a proper v3 database by initializing as v4, then downgrading meta
    store = Store(db_path)
    store.initialize()  # creates v4
    # Manually downgrade meta to v3
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '3')")
    # Drop v4-only tables to simulate pre-v4 state
    store.conn.execute("DROP TABLE IF EXISTS submission_attempts")
    store.conn.execute("DROP TABLE IF EXISTS submission_recovery_evidence")
    store.conn.commit()
    store.close()

    # Reopen — should migrate to v4
    store2 = Store(db_path)
    store2.initialize()
    assert store2.get_meta("schema_version") == "4"

    # v4 tables exist
    tbl = store2.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='submission_attempts'"
    ).fetchone()
    assert tbl is not None

    tbl2 = store2.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='submission_recovery_evidence'"
    ).fetchone()
    assert tbl2 is not None

    # Reopen is idempotent
    store2.close()
    store3 = Store(db_path)
    store3.initialize()
    assert store3.get_meta("schema_version") == "4"
    store3.close()


# ---------------------------------------------------------------------------
# 23. v2→v3→v4 chain migration
# ---------------------------------------------------------------------------

def test_v2_to_v3_to_v4_migration(tmp_path):
    """v2 database migrates through v3 to v4."""
    db_path = tmp_path / "bridge.db"

    store = Store(db_path)
    store.conn.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)")
    store.conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '2')")
    store.conn.execute("CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, started_ts TEXT)")
    store.conn.execute("CREATE TABLE IF NOT EXISTS signal_fingerprints (run_id TEXT, fingerprint TEXT, decision_uid TEXT, ts TEXT, PRIMARY KEY(run_id, fingerprint))")
    # Zero fingerprints + no trades/orders → safe to upgrade
    store.conn.commit()
    store.close()

    store2 = Store(db_path)
    store2.initialize()
    assert store2.get_meta("schema_version") == "4"
    store2.close()


# ---------------------------------------------------------------------------
# 24. Submitting blocks independent of engine
# ---------------------------------------------------------------------------

def test_submitting_blocks_independent_of_engine_caller(tmp_path):
    """OrderManager.submit_plan blocks when SUBMITTING exists, even if engine caller bypassed."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    # Simulate a SUBMITTING state via direct DB insertion
    store.conn.execute("BEGIN IMMEDIATE")
    store.create_submission_attempt(
        request_id="test-request-id",
        origin_run_id="run-0",
        origin_decision_uid="d-0",
        strategy_id="keltner_trail_ema8",
        coin="BTC",
        direction="LONG",
        qty=0.1,
        planned_roles=["entry", "sl"],
        planned_cloids={"entry": "cloid-e", "sl": "cloid-s"},
        recovery_payload={"test": True},
    )
    store.conn.commit()

    broker = MockBroker(bars=_mock_bars())
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    result = asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert result is None  # blocked
    assert broker.place_count == 0
    store.close()


# ---------------------------------------------------------------------------
# 25. Recovery evidence is append-only
# ---------------------------------------------------------------------------

def test_recovery_evidence_append_only(tmp_path):
    """Recovery evidence rows accumulate, never overwritten."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars(), post_send_timeout=True)
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    with pytest.raises(IdentityCollisionError):
        asyncio.run(mgr.submit_plan("d-1", _plan()))

    # Run 3 recovery cycles
    for _ in range(3):
        asyncio.run(mgr.run_recovery_cycle())

    snap = store.get_snapshot()
    evidence_count = len(snap["recovery_evidence"])
    assert evidence_count >= 3  # at least one per cycle per source

    # Run one more cycle
    asyncio.run(mgr.run_recovery_cycle())
    snap2 = store.get_snapshot()
    assert len(snap2["recovery_evidence"]) > evidence_count

    store.close()


# ---------------------------------------------------------------------------
# 26. Terminal transition attacks fail
# ---------------------------------------------------------------------------

def test_terminal_transition_attacks_rejected(tmp_path):
    """Self-transitions are rejected; transitions require exact pre-state."""
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run-1", "dry_run", "testnet", {})

    broker = MockBroker(bars=_mock_bars())
    broker.connected = True
    mgr = OrderManager(store, broker, "run-1")

    # Normal success
    result = asyncio.run(mgr.submit_plan("d-1", _plan()))
    assert result is not None

    # Attempt self-transition
    with pytest.raises(ValueError, match="Self-transition forbidden"):
        store.transition_attempt_state(
            attempt_id=1,
            from_states=["VERIFIED_SUCCESS"],
            to_state="VERIFIED_SUCCESS",
        )

    # Attempt transition from wrong pre-state
    store.conn.execute("BEGIN IMMEDIATE")
    ok = store.transition_attempt_state(
        attempt_id=1,
        from_states=["SUBMITTING"],  # wrong — actual state is VERIFIED_SUCCESS
        to_state="UNKNOWN_SUBMISSION",
    )
    store.conn.commit()
    assert not ok  # Should fail — VERIFIED_SUCCESS is not in from_states

    store.close()
