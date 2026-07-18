"""Interim TS-P1-007: engine-path proof that DAILY_LOSS and CONSECUTIVE_LOSS
gates receive real persisted values.

Risk assertions drive ``BridgeEngine.on_bar`` through ``run_replay`` — no test
passes ``realized_today``/``consecutive_losses`` directly into
``RiskEngine.evaluate``. Net-PnL assertions drive the real
``OrderManager._ingest_fill`` path. A frozen Store clock makes every UTC-day
boundary deterministic (audit F-06).
"""

from __future__ import annotations

import asyncio
import sqlite3
from datetime import UTC, datetime, timedelta

import pytest

from bridge.broker.mock import MockBroker
from bridge.engine.engine import BridgeEngine
from bridge.engine.orders import OrderManager
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.types import Bar, FillEvent, Signal
from bridge.store.db import Store

EQUITY = 100000.0
DAILY_LIMIT = EQUITY * RiskConfig().max_daily_loss_pct
FROZEN = datetime(2026, 7, 6, 12, 0, tzinfo=UTC)
SEED_RUN = "seed-run"


class ProtocolBroker:
    coin = "BTC"

    def __init__(self, bars: list[Bar]) -> None:
        self._replay = bars
        self.connected = False
        self.submitted: list = []

    async def connect(self) -> None:
        self.connected = True

    async def account(self) -> dict:
        return {"equity": EQUITY, "available_margin": EQUITY}

    async def positions(self) -> list:
        return []

    async def open_orders(self) -> list:
        return []

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list[Bar]:
        return self._replay[-lookback:]

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed) -> None:
        for bar in self._replay:
            on_bar_closed(bar)

    async def place_bracket(self, plan) -> dict:
        self.submitted.append(plan)
        return {
            "entry": {
                "cloid": f"{plan.signal.ts.timestamp()}:entry",
                "oid": 1,
                "role": "ENTRY",
                "status": "FILLED",
                "qty": plan.qty,
                "avg_fill_px": plan.signal.ref_price,
            }
        }

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        return None

    async def cancel(self, cloid: str) -> None:
        return None

    async def cancel_all(self) -> None:
        return None

    async def flatten(self, coin: str) -> None:
        return None


class FixedSignalStrategy:
    id = "fixed_signal"
    warmup_bars = 0
    symbol = "BTC"

    def __init__(self, stop_loss: float = 90.0) -> None:
        self.stop_loss = stop_loss

    def on_bar(self, bars, position):
        return Signal(
            ts=bars[-1].ts,
            symbol=self.symbol,
            direction="LONG",
            reason="fixed",
            ref_price=bars[-1].close,
            stop_loss=self.stop_loss,
            take_profit=None,
        )

    def trail_level(self, bars, position):
        return None


class BrokenRiskReadStore(Store):
    """Risk-input reads fail; everything else works (transient read fault)."""

    def realized_pnl_today(self, run_id: str, now=None) -> float:
        raise sqlite3.DatabaseError("disk I/O error")


class DeadWriteStore(Store):
    """Risk-input reads fail AND the matching state/event writes fail, while
    meta reads still return the stale persisted value (worst observable case:
    the DISARMED verdict cannot be persisted)."""

    dead: bool = False

    def realized_pnl_today(self, run_id: str, now=None) -> float:
        if self.dead:
            raise sqlite3.DatabaseError("disk I/O error")
        return super().realized_pnl_today(run_id, now)

    def set_meta(self, key: str, value: str) -> None:
        if self.dead and key == "app_state":
            raise sqlite3.DatabaseError("disk I/O error")
        super().set_meta(key, value)

    def insert_event(self, *args, **kwargs):
        if self.dead:
            raise sqlite3.DatabaseError("disk I/O error")
        return super().insert_event(*args, **kwargs)


def _bar() -> Bar:
    return Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=102, low=99, close=100, volume=1)


def _store(tmp_path, cls=Store, name: str = "bridge.db"):
    store = cls(tmp_path / name, clock=lambda: FROZEN)
    store.initialize()
    store.create_run(SEED_RUN, "dry_run", "testnet", {})
    return store


def _seed_closed_trade(store: Store, pnl: float, exit_ts, tag: str, run_id: str = SEED_RUN) -> int:
    entry_ts = FROZEN - timedelta(hours=2)
    trade_id = store.create_trade(
        run_id=run_id,
        coin="BTC",
        direction="LONG",
        qty=1.0,
        entry_decision_uid=f"{run_id}:BTC:{tag}",
        signal_ts=entry_ts,
        decision_ts=entry_ts,
        expected_px=100.0,
        risk_dollars=1.0,
        risk_pct=0.005,
        leverage=1,
        sl_initial=90.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    store.update_trade_exit(trade_id, exit_px=100.0 + pnl, exit_ts=exit_ts, exit_reason="SL", pnl=pnl)
    return trade_id


def _ingest_closed_trade(
    store: Store,
    manager: OrderManager,
    tag: str,
    entry_px: float,
    exit_px: float,
    entry_fee: float,
    exit_fee: float,
    funding: float = 0.0,
    exit_ts: datetime | None = None,
    run_id: str = SEED_RUN,
) -> int:
    exit_ts = exit_ts or FROZEN
    duid = f"{run_id}:BTC:{tag}"
    trade_id = store.create_trade(
        run_id=run_id,
        coin="BTC",
        direction="LONG",
        qty=1.0,
        entry_decision_uid=duid,
        signal_ts=exit_ts - timedelta(hours=1),
        decision_ts=exit_ts - timedelta(hours=1),
        expected_px=entry_px,
        risk_dollars=1.0,
        risk_pct=0.005,
        leverage=1,
        sl_initial=entry_px * 0.9,
        tp_initial=None,
        llm_directive_id=None,
    )
    store.insert_order(
        cloid=f"{tag}-e", oid=None, group_id=None, order_ref=f"{tag}-e", order_json={},
        decision_uid=duid, trade_id=trade_id, role="ENTRY", status="SUBMITTED", qty=1.0,
    )
    store.insert_order(
        cloid=f"{tag}-s", oid=None, group_id=None, order_ref=f"{tag}-s", order_json={},
        decision_uid=duid, trade_id=trade_id, role="SL", status="OPEN", qty=1.0,
    )
    manager._ingest_fill(FillEvent(
        fill_id=f"{tag}-f1", cloid=f"{tag}-e", coin="BTC", qty=1.0, px=entry_px,
        ts=exit_ts - timedelta(minutes=30), fee=entry_fee, role="ENTRY",
    ))
    manager._ingest_fill(FillEvent(
        fill_id=f"{tag}-f2", cloid=f"{tag}-s", coin="BTC", qty=1.0, px=exit_px,
        ts=exit_ts, fee=exit_fee, funding=funding, role="SL",
    ))
    return trade_id


def _engine(store: Store, broker: ProtocolBroker, run_id: str) -> BridgeEngine:
    return BridgeEngine(
        run_id=run_id,
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )


def _manager(store: Store) -> OrderManager:
    return OrderManager(store=store, broker=MockBroker([], starting_equity=1000), run_id=SEED_RUN)


def _rejections(store: Store, reason: str) -> list[dict]:
    return [
        row
        for row in store.get_snapshot()["decisions"]
        if row["stage"] == "RISK_REJECT" and reason in str(row["payload_json"])
    ]


# --- Gate triggers through the engine path -------------------------------


def test_daily_loss_gate_triggers_through_engine_path(tmp_path):
    asyncio.run(_daily_loss_trigger(tmp_path))


async def _daily_loss_trigger(tmp_path):
    store = _store(tmp_path)
    _seed_closed_trade(store, -DAILY_LIMIT, FROZEN - timedelta(minutes=5), "boundary")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "daily-loss-trigger")

    await engine.run_replay(max_bars=1)

    assert broker.submitted == []
    assert store.get_meta("app_state") == "DISARMED"
    assert _rejections(store, "DAILY_LOSS_LIMIT")
    assert any(row["code"] == "RISK_AUTO_DISARM" for row in store.get_events())


def test_daily_loss_one_dollar_inside_boundary_passes(tmp_path):
    asyncio.run(_daily_loss_inside(tmp_path))


async def _daily_loss_inside(tmp_path):
    store = _store(tmp_path)
    _seed_closed_trade(store, -(DAILY_LIMIT - 1.0), FROZEN - timedelta(minutes=5), "inside")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "daily-loss-inside")

    await engine.run_replay(max_bars=1)

    assert len(broker.submitted) == 1
    assert store.get_meta("app_state") == "ARMED"
    assert not _rejections(store, "DAILY_LOSS_LIMIT")


def test_yesterday_loss_does_not_count_toward_daily_gate(tmp_path):
    asyncio.run(_yesterday_loss(tmp_path))


async def _yesterday_loss(tmp_path):
    store = _store(tmp_path)
    _seed_closed_trade(store, -(DAILY_LIMIT * 2), FROZEN - timedelta(days=1), "yesterday")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "daily-loss-yesterday")

    await engine.run_replay(max_bars=1)

    assert len(broker.submitted) == 1
    assert store.get_meta("app_state") == "ARMED"


def test_consecutive_loss_gate_triggers_through_engine_path(tmp_path):
    asyncio.run(_consecutive_trigger(tmp_path))


async def _consecutive_trigger(tmp_path):
    store = _store(tmp_path)
    for i in range(RiskConfig().max_consecutive_losses):
        _seed_closed_trade(store, -1.0, FROZEN - timedelta(minutes=5) + timedelta(seconds=i), f"streak{i}")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "consecutive-trigger")

    await engine.run_replay(max_bars=1)

    assert broker.submitted == []
    assert store.get_meta("app_state") == "DISARMED"
    assert _rejections(store, "CONSECUTIVE_LOSS_LIMIT")


def test_win_resets_consecutive_loss_streak(tmp_path):
    asyncio.run(_win_resets_streak(tmp_path))


async def _win_resets_streak(tmp_path):
    store = _store(tmp_path)
    for i, pnl in enumerate((-1.0, -1.0, 1.0, -1.0)):
        _seed_closed_trade(store, pnl, FROZEN - timedelta(minutes=5) + timedelta(seconds=i), f"mix{i}")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "streak-reset")

    await engine.run_replay(max_bars=1)

    assert len(broker.submitted) == 1
    assert store.get_meta("app_state") == "ARMED"
    assert not _rejections(store, "CONSECUTIVE_LOSS_LIMIT")


def test_gates_persist_across_restart(tmp_path):
    asyncio.run(_restart_persistence(tmp_path))


async def _restart_persistence(tmp_path):
    first = _store(tmp_path)
    _seed_closed_trade(first, -DAILY_LIMIT, FROZEN - timedelta(minutes=5), "restart")
    first.close()

    # Fresh Store + fresh engine on the same file simulates a process restart:
    # the gate must trigger from SQLite state alone.
    store = Store(tmp_path / "bridge.db", clock=lambda: FROZEN)
    store.initialize()
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "restart-run")

    await engine.run_replay(max_bars=1)

    assert broker.submitted == []
    assert store.get_meta("app_state") == "DISARMED"
    assert _rejections(store, "DAILY_LOSS_LIMIT")


# --- Environment isolation (audit F-01) ----------------------------------


def test_other_mode_trades_never_reach_the_gates(tmp_path):
    asyncio.run(_mode_isolation_engine_path(tmp_path))


async def _mode_isolation_engine_path(tmp_path):
    store = _store(tmp_path)
    store.create_run("paper-run", "paper", "testnet", {})
    # Catastrophic paper losses in the shared DB file must not trip a dry-run
    # engine's gates (and vice versa).
    for i in range(5):
        _seed_closed_trade(store, -DAILY_LIMIT, FROZEN - timedelta(minutes=5) + timedelta(seconds=i),
                           f"paper{i}", run_id="paper-run")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "mode-isolation")

    await engine.run_replay(max_bars=1)

    assert len(broker.submitted) == 1
    assert store.get_meta("app_state") == "ARMED"


def test_store_helpers_scope_by_mode_and_win_cannot_reset_foreign_streak(tmp_path):
    store = _store(tmp_path)
    store.create_run("paper-run", "paper", "testnet", {})
    base = FROZEN - timedelta(minutes=5)
    _seed_closed_trade(store, -100.0, base, "dr-loss1")
    _seed_closed_trade(store, -100.0, base + timedelta(seconds=1), "dr-loss2")
    # A later dry-run win must not reset the paper streak, and paper losses
    # must not appear in dry-run sums.
    _seed_closed_trade(store, -500.0, base + timedelta(seconds=2), "p-loss", run_id="paper-run")
    _seed_closed_trade(store, 50.0, base + timedelta(seconds=3), "dr-win")

    assert store.realized_pnl_today(SEED_RUN) == pytest.approx(-150.0)
    assert store.consecutive_closed_losses(SEED_RUN) == 0  # dry-run win is latest dry-run close
    assert store.realized_pnl_today("paper-run") == pytest.approx(-500.0)
    assert store.consecutive_closed_losses("paper-run") == 1  # dry-run win did not reset it


def test_unknown_run_id_fails_closed(tmp_path):
    store = _store(tmp_path)
    with pytest.raises(LookupError):
        store.realized_pnl_today("never-created")
    with pytest.raises(LookupError):
        store.consecutive_closed_losses("never-created")


# --- Net PnL through the real fill path (audit F-02) ----------------------


def test_fee_only_loss_is_a_net_loss(tmp_path):
    store = _store(tmp_path)
    manager = _manager(store)
    trade_id = _ingest_closed_trade(store, manager, "feeonly", 100.0, 100.0, entry_fee=10.0, exit_fee=15.0)

    trade = store.get_trade(trade_id)
    assert trade["pnl"] == pytest.approx(-25.0)
    assert store.realized_pnl_today(SEED_RUN) == pytest.approx(-25.0)
    assert store.consecutive_closed_losses(SEED_RUN) == 1


def test_gross_win_net_loss_and_funding_debit(tmp_path):
    store = _store(tmp_path)
    manager = _manager(store)
    trade_id = _ingest_closed_trade(
        store, manager, "grosswin", 100.0, 100.02, entry_fee=5.0, exit_fee=2.0, funding=3.0
    )

    trade = store.get_trade(trade_id)
    assert trade["pnl"] == pytest.approx(100.02 - 100.0 - 10.0)
    assert trade["pnl"] < 0
    # Funding credit (negative = rebate) reduces the cost.
    credit_id = _ingest_closed_trade(
        store, manager, "credit", 100.0, 100.0, entry_fee=1.0, exit_fee=1.0, funding=-5.0,
        exit_ts=FROZEN + timedelta(minutes=1),
    )
    assert store.get_trade(credit_id)["pnl"] == pytest.approx(3.0)


def test_net_fee_losses_trip_consecutive_gate_through_engine_path(tmp_path):
    asyncio.run(_net_loss_streak_engine_path(tmp_path))


async def _net_loss_streak_engine_path(tmp_path):
    store = _store(tmp_path)
    manager = _manager(store)
    # Three gross-flat trades that are net losers only because of fees.
    for i in range(RiskConfig().max_consecutive_losses):
        _ingest_closed_trade(
            store, manager, f"netloss{i}", 100.0, 100.0, entry_fee=2.0, exit_fee=2.0,
            exit_ts=FROZEN - timedelta(minutes=5) + timedelta(seconds=i),
        )
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "net-loss-streak")

    await engine.run_replay(max_bars=1)

    assert broker.submitted == []
    assert store.get_meta("app_state") == "DISARMED"
    assert _rejections(store, "CONSECUTIVE_LOSS_LIMIT")


# --- Fail-closed on risk-input read failure (audit F-03) ------------------


def test_risk_input_read_failure_fails_closed_and_is_observable(tmp_path):
    asyncio.run(_risk_input_failure(tmp_path))


async def _risk_input_failure(tmp_path):
    store = _store(tmp_path, cls=BrokenRiskReadStore)
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "risk-input-fail")

    await engine.run_replay(max_bars=1)

    assert broker.submitted == []
    assert engine.state == "DISARMED"
    assert store.get_meta("app_state") == "DISARMED"
    assert any(row["code"] == "RISK_INPUT_FAILED" for row in store.get_events())
    status = engine.status()
    assert status["state"] == "DISARMED"
    assert "DatabaseError" in str(status["risk_input_error"])


def test_risk_input_failure_stays_disarmed_even_when_writes_also_fail(tmp_path):
    asyncio.run(_risk_input_failure_dead_writes(tmp_path))


async def _risk_input_failure_dead_writes(tmp_path):
    store = _store(tmp_path, cls=DeadWriteStore)
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "risk-input-dead")
    store.dead = True

    await engine.run_replay(max_bars=1)

    assert broker.submitted == []
    # Persisted meta still says ARMED (the disarm write failed), but the
    # sticky in-memory latch must dominate every observable surface.
    assert engine.state == "DISARMED"
    status = engine.status()
    assert status["state"] == "DISARMED"
    assert "DatabaseError" in str(status["risk_input_error"])
    assert engine._app_state() == "DISARMED"


# --- Timestamp canonicalization and day bounds (audit F-04) ---------------


def test_timestamp_forms_are_canonicalized_and_day_is_bounded(tmp_path):
    store = _store(tmp_path)
    base = FROZEN - timedelta(minutes=5)
    # Offset form: 2026-07-05T23:30-02:00 == 2026-07-06T01:30 UTC -> counted.
    _seed_closed_trade(store, -10.0, "2026-07-05T23:30:00-02:00", "offset")
    # Space-separated naive string -> UTC -> counted.
    _seed_closed_trade(store, -10.0, "2026-07-06 01:00:00", "space")
    # Zulu suffix -> counted.
    _seed_closed_trade(store, -10.0, "2026-07-06T22:00:00Z", "zulu")
    # Naive datetime object -> UTC -> counted.
    _seed_closed_trade(store, -10.0, datetime(2026, 7, 6, 2, 0), "naive")
    # Yesterday UTC (23:30-02:00 == 07-06 01:30, so use a real prior day) -> excluded.
    _seed_closed_trade(store, -100.0, "2026-07-05T10:00:00+00:00", "prior")
    # Future day -> excluded from today's bounded interval.
    _seed_closed_trade(store, -100.0, "2026-07-07T01:00:00+00:00", "future")
    _ = base

    assert store.realized_pnl_today(SEED_RUN) == pytest.approx(-40.0)

    # Naive `now` injection is treated as UTC, matching storage semantics.
    assert store.realized_pnl_today(SEED_RUN, now=datetime(2026, 7, 6, 3, 0)) == pytest.approx(-40.0)


def test_invalid_timestamp_string_is_rejected(tmp_path):
    store = _store(tmp_path)
    trade_id = _seed_closed_trade(store, -1.0, FROZEN, "valid")
    with pytest.raises(ValueError):
        store.update_trade_exit(trade_id, exit_px=99.0, exit_ts="not-a-timestamp", exit_reason="SL", pnl=-1.0)


# --- Store helper edges ----------------------------------------------------


def test_store_helpers_empty_open_and_zero_pnl(tmp_path):
    store = _store(tmp_path)
    assert store.realized_pnl_today(SEED_RUN) == 0.0
    assert store.consecutive_closed_losses(SEED_RUN) == 0

    # An open trade (no exit, NULL pnl) must not affect either helper.
    store.create_trade(
        run_id=SEED_RUN,
        coin="BTC",
        direction="LONG",
        qty=1.0,
        entry_decision_uid=f"{SEED_RUN}:BTC:open",
        signal_ts=FROZEN,
        decision_ts=FROZEN,
        expected_px=100.0,
        risk_dollars=1.0,
        risk_pct=0.005,
        leverage=1,
        sl_initial=90.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    _seed_closed_trade(store, -2.0, FROZEN - timedelta(seconds=2), "loss")
    # Zero-PnL close counts in the daily sum and breaks the loss streak.
    _seed_closed_trade(store, 0.0, FROZEN - timedelta(seconds=1), "flat")
    assert store.realized_pnl_today(SEED_RUN) == pytest.approx(-2.0)
    assert store.consecutive_closed_losses(SEED_RUN) == 0


def test_reconcile_equity_row_carries_realized_today(tmp_path):
    asyncio.run(_equity_row_realized(tmp_path))


async def _equity_row_realized(tmp_path):
    store = _store(tmp_path)
    _seed_closed_trade(store, -123.45, FROZEN - timedelta(minutes=5), "equity")
    manager = _manager(store)

    await manager.reconcile()

    rows = store.get_equity()
    assert rows
    assert rows[0]["realized_today"] == pytest.approx(-123.45)
