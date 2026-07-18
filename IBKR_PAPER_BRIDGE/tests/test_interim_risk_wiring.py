"""Interim TS-P1-007: engine-path proof that DAILY_LOSS and CONSECUTIVE_LOSS
gates receive real persisted values.

Every risk assertion here drives ``BridgeEngine.on_bar`` through
``run_replay`` — no test passes ``realized_today``/``consecutive_losses``
directly into ``RiskEngine.evaluate``.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

from bridge.broker.mock import MockBroker
from bridge.engine.engine import BridgeEngine
from bridge.engine.orders import OrderManager
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.types import Bar, Signal
from bridge.store.db import Store

EQUITY = 100000.0
DAILY_LIMIT = EQUITY * RiskConfig().max_daily_loss_pct


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


def _bar() -> Bar:
    return Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=102, low=99, close=100, volume=1)


def _today_base() -> datetime:
    now = datetime.now(UTC)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return max(day_start, now - timedelta(minutes=5))


def _seed_closed_trade(store: Store, pnl: float, exit_ts: datetime, tag: str) -> int:
    trade_id = store.create_trade(
        run_id="seed-run",
        coin="BTC",
        direction="LONG",
        qty=1.0,
        entry_decision_uid=f"seed-run:BTC:{tag}",
        signal_ts=exit_ts - timedelta(hours=1),
        decision_ts=exit_ts - timedelta(hours=1),
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


def _engine(store: Store, broker: ProtocolBroker, run_id: str) -> BridgeEngine:
    return BridgeEngine(
        run_id=run_id,
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )


def _rejections(store: Store, reason: str) -> list[dict]:
    return [
        row
        for row in store.get_snapshot()["decisions"]
        if row["stage"] == "RISK_REJECT" and reason in str(row["payload_json"])
    ]


def test_daily_loss_gate_triggers_through_engine_path(tmp_path):
    asyncio.run(_daily_loss_trigger(tmp_path))


async def _daily_loss_trigger(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    _seed_closed_trade(store, -DAILY_LIMIT, _today_base(), "boundary")
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
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    _seed_closed_trade(store, -(DAILY_LIMIT - 1.0), _today_base(), "inside")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "daily-loss-inside")

    await engine.run_replay(max_bars=1)

    assert len(broker.submitted) == 1
    assert store.get_meta("app_state") == "ARMED"
    assert not _rejections(store, "DAILY_LOSS_LIMIT")


def test_yesterday_loss_does_not_count_toward_daily_gate(tmp_path):
    asyncio.run(_yesterday_loss(tmp_path))


async def _yesterday_loss(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    _seed_closed_trade(store, -(DAILY_LIMIT * 2), datetime.now(UTC) - timedelta(days=1), "yesterday")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "daily-loss-yesterday")

    await engine.run_replay(max_bars=1)

    assert len(broker.submitted) == 1
    assert store.get_meta("app_state") == "ARMED"


def test_consecutive_loss_gate_triggers_through_engine_path(tmp_path):
    asyncio.run(_consecutive_trigger(tmp_path))


async def _consecutive_trigger(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    base = _today_base()
    for i in range(RiskConfig().max_consecutive_losses):
        _seed_closed_trade(store, -1.0, base + timedelta(seconds=i), f"streak{i}")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "consecutive-trigger")

    await engine.run_replay(max_bars=1)

    assert broker.submitted == []
    assert store.get_meta("app_state") == "DISARMED"
    assert _rejections(store, "CONSECUTIVE_LOSS_LIMIT")


def test_win_resets_consecutive_loss_streak(tmp_path):
    asyncio.run(_win_resets_streak(tmp_path))


async def _win_resets_streak(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    base = _today_base()
    for i, pnl in enumerate((-1.0, -1.0, 1.0, -1.0)):
        _seed_closed_trade(store, pnl, base + timedelta(seconds=i), f"mix{i}")
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "streak-reset")

    await engine.run_replay(max_bars=1)

    assert len(broker.submitted) == 1
    assert store.get_meta("app_state") == "ARMED"
    assert not _rejections(store, "CONSECUTIVE_LOSS_LIMIT")


def test_gates_persist_across_restart(tmp_path):
    asyncio.run(_restart_persistence(tmp_path))


async def _restart_persistence(tmp_path):
    db_path = tmp_path / "bridge.db"
    first = Store(db_path)
    first.initialize()
    _seed_closed_trade(first, -DAILY_LIMIT, _today_base(), "restart")

    # Fresh Store + fresh engine on the same file simulates a process restart:
    # the gate must trigger from SQLite state alone.
    store = Store(db_path)
    store.initialize()
    broker = ProtocolBroker([_bar()])
    engine = _engine(store, broker, "restart-run")

    await engine.run_replay(max_bars=1)

    assert broker.submitted == []
    assert store.get_meta("app_state") == "DISARMED"
    assert _rejections(store, "DAILY_LOSS_LIMIT")


def test_reconcile_equity_row_carries_realized_today(tmp_path):
    asyncio.run(_equity_row_realized(tmp_path))


async def _equity_row_realized(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    store.create_run("equity-run", "dry_run", "testnet", {})
    _seed_closed_trade(store, -123.45, _today_base(), "equity")
    broker = MockBroker([], starting_equity=1000)
    manager = OrderManager(store=store, broker=broker, run_id="equity-run")

    await manager.reconcile()

    rows = store.get_equity()
    assert rows
    assert rows[0]["realized_today"] == -123.45


def test_store_helpers_empty_and_open_trades(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    assert store.realized_pnl_today() == 0.0
    assert store.consecutive_closed_losses() == 0

    # An open trade (no exit, NULL pnl) must not affect either helper.
    store.create_trade(
        run_id="open-run",
        coin="BTC",
        direction="LONG",
        qty=1.0,
        entry_decision_uid="open-run:BTC:open",
        signal_ts=datetime.now(UTC),
        decision_ts=datetime.now(UTC),
        expected_px=100.0,
        risk_dollars=1.0,
        risk_pct=0.005,
        leverage=1,
        sl_initial=90.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    _seed_closed_trade(store, 5.0, _today_base(), "win")
    assert store.realized_pnl_today() == 5.0
    assert store.consecutive_closed_losses() == 0
