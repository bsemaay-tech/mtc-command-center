"""Tests for the honest monitoring-window state (TS-P0-003).

Core acceptance: a DOWN bridge can NEVER present as an active soak window.
The window state is derived from persisted evidence (store meta) plus a
liveness staleness rule, so a consumer reading stale evidence sees DOWN,
not the last persisted ARMED state.
"""

from __future__ import annotations

import asyncio
import itertools
from datetime import UTC, datetime, timedelta

import pytest

from bridge.broker.mock import MockBroker
from bridge.engine import window as w
from bridge.engine.engine import BridgeEngine
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.store.db import Store

T0 = datetime(2026, 7, 19, 12, 0, tzinfo=UTC)
STALE_S = 300.0


def fresh(now=T0, delta_s=0.0):
    return now - timedelta(seconds=delta_s)


# ---------------------------------------------------------------------------
# pure decision function: every transition
# ---------------------------------------------------------------------------


def compute(**kw):
    defaults = dict(
        app_state="ARMED",
        started_ts=fresh(delta_s=3600),
        last_alive_ts=fresh(delta_s=10),
        interrupted_ts=None,
        reset_ts=None,
        now=T0,
        stale_after_s=STALE_S,
    )
    defaults.update(kw)
    return w.compute_window_state(**defaults)


def test_running_requires_armed_fresh_uninterrupted():
    assert compute() == w.WINDOW_RUNNING


def test_no_window_started_is_down():
    assert compute(started_ts=None) == w.WINDOW_DOWN


def test_stale_liveness_is_down_even_if_armed():
    assert compute(last_alive_ts=fresh(delta_s=STALE_S + 1)) == w.WINDOW_DOWN


def test_missing_liveness_is_down():
    assert compute(last_alive_ts=None) == w.WINDOW_DOWN


def test_stale_age_boundary_exact_is_alive():
    assert compute(last_alive_ts=fresh(delta_s=STALE_S)) == w.WINDOW_RUNNING
    assert compute(last_alive_ts=fresh(delta_s=STALE_S + 0.001)) == w.WINDOW_DOWN


def test_interrupted_flag_wins_over_armed():
    assert (
        compute(interrupted_ts=fresh(delta_s=60)) == w.WINDOW_INTERRUPTED
    )


def test_disarmed_alive_is_interrupted():
    assert compute(app_state="DISARMED") == w.WINDOW_INTERRUPTED


def test_killed_alive_is_interrupted():
    assert compute(app_state="KILLED") == w.WINDOW_INTERRUPTED


def test_reset_pending_is_reset():
    assert (
        compute(started_ts=None, reset_ts=fresh(delta_s=5)) == w.WINDOW_RESET
    )


def test_down_bridge_never_presents_active_exhaustive():
    """Property sweep: no combination with stale/missing liveness or a
    non-ARMED state may ever yield RUNNING."""
    app_states = ["ARMED", "DISARMED", "KILLED"]
    started = [None, fresh(delta_s=3600)]
    alive = [None, fresh(delta_s=10), fresh(delta_s=STALE_S + 60)]
    interrupted = [None, fresh(delta_s=60)]
    reset = [None, fresh(delta_s=5)]
    for a, s, al, i, r in itertools.product(
        app_states, started, alive, interrupted, reset
    ):
        state = compute(
            app_state=a,
            started_ts=s,
            last_alive_ts=al,
            interrupted_ts=i,
            reset_ts=r,
        )
        if state == w.WINDOW_RUNNING:
            assert a == "ARMED"
            assert s is not None
            assert al is not None and (T0 - al).total_seconds() <= STALE_S
            assert i is None
        stale = al is None or (T0 - al).total_seconds() > STALE_S
        if stale:
            assert state != w.WINDOW_RUNNING


# ---------------------------------------------------------------------------
# store-backed read model + transition helpers
# ---------------------------------------------------------------------------


@pytest.fixture()
def store(tmp_path):
    s = Store(tmp_path / "window.db")
    s.initialize()
    return s


def status_at(store, now, app_state="ARMED"):
    return w.window_status(
        store, app_state=app_state, now=now, stale_after_s=STALE_S
    )


def test_fresh_store_is_down(store):
    block = status_at(store, T0)
    assert block["state"] == w.WINDOW_DOWN
    assert block["started_ts"] is None


def test_start_and_liveness_running(store):
    w.record_window_start(store, T0)
    w.record_liveness(store, T0 + timedelta(seconds=60))
    block = status_at(store, T0 + timedelta(seconds=90))
    assert block["state"] == w.WINDOW_RUNNING
    assert block["started_ts"] == T0.isoformat()


def test_stale_liveness_down_despite_armed_meta(store):
    """THE acceptance case: bridge died while ARMED; a later reader must see
    DOWN, not an active window."""
    w.record_window_start(store, T0)
    w.record_liveness(store, T0 + timedelta(seconds=60))
    later = T0 + timedelta(hours=6)
    block = status_at(store, later, app_state="ARMED")
    assert block["state"] == w.WINDOW_DOWN


def test_restart_after_gap_stamps_interrupted(store):
    w.record_window_start(store, T0)
    w.record_liveness(store, T0 + timedelta(seconds=60))
    restart = T0 + timedelta(hours=6)
    stamped = w.detect_interruption(store, restart, stale_after_s=STALE_S)
    assert stamped is True
    w.record_liveness(store, restart)  # bridge alive again
    block = status_at(store, restart + timedelta(seconds=5))
    assert block["state"] == w.WINDOW_INTERRUPTED


def test_rearm_after_interruption_stays_interrupted(store):
    w.record_window_start(store, T0)
    w.record_liveness(store, T0 + timedelta(seconds=60))
    restart = T0 + timedelta(hours=6)
    w.detect_interruption(store, restart, stale_after_s=STALE_S)
    # operator re-arms WITHOUT resetting the window
    w.record_window_start(store, restart)
    w.record_liveness(store, restart)
    block = status_at(store, restart + timedelta(seconds=5))
    assert block["state"] == w.WINDOW_INTERRUPTED  # sticky until explicit reset


def test_short_gap_does_not_stamp_interrupted(store):
    w.record_window_start(store, T0)
    w.record_liveness(store, T0 + timedelta(seconds=60))
    restart = T0 + timedelta(seconds=60 + STALE_S / 2)
    stamped = w.detect_interruption(store, restart, stale_after_s=STALE_S)
    assert stamped is False
    w.record_liveness(store, restart)
    block = status_at(store, restart)
    assert block["state"] == w.WINDOW_RUNNING


def test_reset_then_new_window_runs_clean(store):
    w.record_window_start(store, T0)
    w.record_liveness(store, T0 + timedelta(seconds=60))
    w.detect_interruption(store, T0 + timedelta(hours=6), stale_after_s=STALE_S)
    reset_at = T0 + timedelta(hours=7)
    w.reset_window(store, reset_at)
    block = status_at(store, reset_at + timedelta(seconds=1))
    assert block["state"] == w.WINDOW_RESET
    start2 = reset_at + timedelta(minutes=5)
    w.record_window_start(store, start2)
    w.record_liveness(store, start2)
    block = status_at(store, start2 + timedelta(seconds=10))
    assert block["state"] == w.WINDOW_RUNNING
    assert block["interrupted_ts"] is None
    assert block["started_ts"] == start2.isoformat()


def test_window_status_survives_store_failure(store):
    """Evidence unreadable -> DOWN, never a fabricated active window."""

    class BrokenStore:
        def get_meta(self, key):
            raise RuntimeError("db gone")

    block = w.window_status(
        BrokenStore(), app_state="ARMED", now=T0, stale_after_s=STALE_S
    )
    assert block["state"] == w.WINDOW_DOWN
    assert block["error"] == "store_unreadable"


# ---------------------------------------------------------------------------
# engine integration: status() exposes the window; arm starts it;
# reconcile success records liveness
# ---------------------------------------------------------------------------


def _engine(store):
    return BridgeEngine(
        run_id="window-test",
        broker=MockBroker([], starting_equity=1000),
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
    )


def test_engine_status_contains_window_block(store):
    engine = _engine(store)
    status = engine.status()
    assert "window" in status
    assert status["window"]["state"] == w.WINDOW_DOWN  # nothing started, no liveness


def test_engine_arm_starts_window_and_reconcile_keeps_it_alive(store):
    async def scenario():
        engine = _engine(store)
        await engine.broker.connect()
        await engine.order_manager.reconcile()
        engine.reconcile_ready = True
        engine.last_reconcile_ts = datetime.now(UTC)
        await engine.arm()
        assert await engine._run_reconcile_cycle() is True
        return engine.status()

    status = asyncio.run(scenario())
    assert status["state"] == "ARMED"
    assert status["window"]["state"] == w.WINDOW_RUNNING


def test_engine_status_window_down_after_staleness(store, monkeypatch):
    async def scenario():
        engine = _engine(store)
        await engine.broker.connect()
        await engine.order_manager.reconcile()
        engine.reconcile_ready = True
        engine.last_reconcile_ts = datetime.now(UTC)
        await engine.arm()
        assert await engine._run_reconcile_cycle() is True
        return engine

    engine = asyncio.run(scenario())
    # simulate a reader far in the future: liveness stamp is now stale
    future = datetime.now(UTC) + timedelta(hours=2)
    block = w.window_status(
        store, app_state="ARMED", now=future, stale_after_s=STALE_S
    )
    assert block["state"] == w.WINDOW_DOWN
