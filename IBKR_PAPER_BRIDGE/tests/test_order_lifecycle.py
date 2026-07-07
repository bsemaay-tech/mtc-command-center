from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from bridge.broker.mock import MockBroker
from bridge.engine.orders import OrderManager
from bridge.engine.types import Bar, OrderPlan, Position, Signal
from bridge.store.db import Store


def test_sl_fills_on_later_bar():
    asyncio.run(_run_sl_fills_on_later_bar())


def test_trail_modifies_same_order():
    asyncio.run(_run_trail_modifies_same_order())


def test_reduce_only_close():
    asyncio.run(_run_reduce_only_close())


def test_naked_position_reprotects_then_flattens(tmp_path):
    asyncio.run(_run_naked_position_reprotects_then_flattens(tmp_path))


def test_duplicate_signal_persisted(tmp_path):
    asyncio.run(_run_duplicate_signal_persisted(tmp_path))


async def _run_sl_fills_on_later_bar() -> None:
    bars = [
        Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=101, low=99, close=100, volume=1),
        Bar(ts=datetime(2026, 7, 6, 1, tzinfo=UTC), open=101, high=104, low=100, close=103, volume=1),
        Bar(ts=datetime(2026, 7, 6, 2, tzinfo=UTC), open=103, high=104, low=94, close=96, volume=1),
    ]
    broker = MockBroker(bars=bars, starting_equity=1000)
    await broker.connect()

    ids = await broker.place_bracket(_plan(bars[0], stop_loss=95.0, take_profit=110.0))
    assert ids["entry"]["status"] == "OPEN"
    assert await broker.positions() == []

    broker.process_bar(bars[1])
    assert (await broker.positions())[0].entry_px == 101
    assert next(order for order in broker.orders if order["role"] == "SL")["status"] == "OPEN"

    broker.process_bar(bars[2])
    assert await broker.positions() == []
    assert next(order for order in broker.orders if order["role"] == "SL")["status"] == "FILLED"


async def _run_trail_modifies_same_order() -> None:
    bars = [
        Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=101, low=99, close=100, volume=1),
        Bar(ts=datetime(2026, 7, 6, 1, tzinfo=UTC), open=101, high=104, low=100, close=103, volume=1),
    ]
    broker = MockBroker(bars=bars, starting_equity=1000)
    await broker.connect()
    ids = await broker.place_bracket(_plan(bars[0], stop_loss=95.0, take_profit=None))
    sl_cloid = ids["sl"]["cloid"]

    await broker.modify_stop(sl_cloid, 99.0)

    sl = next(order for order in broker.orders if order["cloid"] == sl_cloid)
    assert sl["trigger_px"] == 99.0
    assert sl["cloid"] == sl_cloid


async def _run_reduce_only_close() -> None:
    bars = [
        Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=101, low=99, close=100, volume=1),
        Bar(ts=datetime(2026, 7, 6, 1, tzinfo=UTC), open=101, high=104, low=100, close=103, volume=1),
    ]
    broker = MockBroker(bars=bars, starting_equity=1000)
    await broker.connect()
    await broker.place_bracket(_plan(bars[0], stop_loss=95.0, take_profit=None))
    broker.process_bar(bars[1])

    await broker.flatten("BTC")

    close_order = broker.orders[-1]
    assert close_order["role"] == "CLOSE"
    assert close_order["reduce_only"] is True
    assert await broker.positions() == []


async def _run_naked_position_reprotects_then_flattens(tmp_path) -> None:
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    store.create_run("run", "dry_run", "testnet", {})
    broker = ReprotectFailsBroker()
    manager = OrderManager(store=store, broker=broker, run_id="run")

    await manager.reconcile()

    assert broker.reprotect_attempts == 1
    assert broker.flattened == ["BTC"]


async def _run_duplicate_signal_persisted(tmp_path) -> None:
    db_path = tmp_path / "bridge.db"
    store = Store(db_path)
    store.initialize()
    store.create_run("run", "dry_run", "testnet", {})
    bars = [
        Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=101, low=99, close=100, volume=1),
        Bar(ts=datetime(2026, 7, 6, 1, tzinfo=UTC), open=101, high=104, low=100, close=103, volume=1),
    ]
    broker = MockBroker(bars=bars, starting_equity=1000)
    await broker.connect()

    first = OrderManager(store=store, broker=broker, run_id="run")
    plan = _plan(bars[0], stop_loss=95.0, take_profit=None)
    assert await first.submit_plan("decision-1", plan) is not None
    store.close()

    reopened = Store(db_path)
    reopened.initialize()
    second = OrderManager(store=reopened, broker=broker, run_id="run")

    assert await second.submit_plan("decision-2", plan) is None


def _plan(bar: Bar, stop_loss: float, take_profit: float | None) -> OrderPlan:
    return OrderPlan(
        signal=Signal(
            ts=bar.ts,
            symbol="BTC",
            direction="LONG",
            reason="fixed",
            ref_price=bar.close,
            stop_loss=stop_loss,
            take_profit=take_profit,
        ),
        qty=0.1,
        entry_type="MKT",
        stop_loss=stop_loss,
        take_profit=take_profit,
        leverage=1,
        risk_dollars=0.5,
        risk_pct=0.001,
    )


class ReprotectFailsBroker:
    def __init__(self) -> None:
        self.reprotect_attempts = 0
        self.flattened: list[str] = []

    async def connect(self) -> None:
        return None

    async def account(self) -> dict[str, float]:
        return {"equity": 1000.0, "available_margin": 1000.0}

    async def positions(self) -> list[Position]:
        return [Position(symbol="BTC", size=0.1, entry_px=100.0)]

    async def open_orders(self) -> list[dict]:
        return []

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list[Bar]:
        return []

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed) -> None:
        return None

    async def place_bracket(self, plan: OrderPlan) -> dict:
        raise AssertionError("reconcile should not submit entries")

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        return None

    async def cancel(self, cloid: str) -> None:
        return None

    async def cancel_all(self) -> None:
        return None

    async def flatten(self, coin: str) -> None:
        self.flattened.append(coin)

    async def reprotect_position(self, position: Position) -> bool:
        self.reprotect_attempts += 1
        return False
