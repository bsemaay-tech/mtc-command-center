from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from bridge.broker.mock import MockBroker
from bridge.engine.orders import OrderManager
from bridge.engine.types import AccountSnapshot, Bar, OrderPlan, Position, Signal
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


def test_foreign_position_is_warned_and_never_flattened(tmp_path):
    asyncio.run(_run_foreign_position_is_warned_and_never_flattened(tmp_path))


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
    now = datetime(2026, 7, 6, 0, tzinfo=UTC)
    store.create_trade(
        run_id="run",
        coin="BTC",
        direction="LONG",
        qty=0.1,
        entry_decision_uid="owned-decision",
        signal_ts=now,
        decision_ts=now,
        expected_px=100.0,
        risk_dollars=1.0,
        risk_pct=0.001,
        leverage=1,
        sl_initial=95.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    broker = ReprotectFailsBroker()
    manager = OrderManager(store=store, broker=broker, run_id="run", pending_grace_s=0)

    await manager.reconcile()

    assert broker.reprotect_attempts == 1
    assert broker.flattened == ["BTC"]


async def _run_foreign_position_is_warned_and_never_flattened(tmp_path) -> None:
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    store.create_run("run", "dry_run", "testnet", {})
    broker = ReprotectFailsBroker()
    manager = OrderManager(store=store, broker=broker, run_id="run", pending_grace_s=0)

    await manager.reconcile()

    assert broker.reprotect_attempts == 0
    assert broker.flattened == []
    assert store.get_snapshot()["events"][-1]["code"] == "FOREIGN_POSITION_IGNORED"


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

    async def account(self) -> AccountSnapshot:
        return AccountSnapshot(equity=1000.0, available_margin=1000.0)

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

    async def reprotect_position(self, position: Position, stop_loss, take_profit, decision_uid):
        self.reprotect_attempts += 1
        return None


def test_match_order_cascade_cloid_then_ref_then_attributes(tmp_path):
    """B2: reconciler matching falls back cloid -> order_ref -> attributes."""
    from bridge.engine.types import BrokerOrder

    store = Store(tmp_path / "b2.db")
    store.initialize()
    store.create_run("b2", "dry_run", "testnet", {})
    manager = OrderManager(store, MockBroker(bars=[], starting_equity=1000), "b2")
    store.insert_order(
        cloid="0xaa", oid=1, group_id="d1", order_ref="d1:SL",
        order_json={"symbol": "BTC", "trigger_px": 95.0},
        decision_uid="d1", trade_id=None, role="SL",
        status="OPEN", qty=0.5, filled_qty=0.0, avg_fill_px=None,
    )

    base = dict(coin="BTC", side="SELL", size=0.5, status="OPEN", role="SL",
                reduce_only=True, trigger_px=95.0, order_type="Stop Market")
    # 1) cloid hit
    assert manager._match_order(BrokerOrder(cloid="0xaa", oid=1, **base))["cloid"] == "0xaa"
    # 2) unknown cloid, order_ref hit
    assert manager._match_order(
        BrokerOrder(cloid="0xdead", oid=2, order_ref="d1:SL", **base)
    )["cloid"] == "0xaa"
    # 3) unknown cloid+ref, single attribute match
    assert manager._match_order(BrokerOrder(cloid="0xdead", oid=2, **base))["cloid"] == "0xaa"
    # 3b) attribute mismatch (different trigger) -> no match
    miss = dict(base, trigger_px=90.0)
    assert manager._match_order(BrokerOrder(cloid="0xdead", oid=2, **miss)) is None


def test_match_order_ambiguous_attributes_warns_and_returns_none(tmp_path):
    from bridge.engine.types import BrokerOrder

    store = Store(tmp_path / "b2b.db")
    store.initialize()
    store.create_run("b2b", "dry_run", "testnet", {})
    manager = OrderManager(store, MockBroker(bars=[], starting_equity=1000), "b2b")
    for idx in ("0x01", "0x02"):
        store.insert_order(
            cloid=idx, oid=None, group_id="d", order_ref=f"d:{idx}",
            order_json={"symbol": "BTC", "trigger_px": 95.0},
            decision_uid="d", trade_id=None, role="SL",
            status="OPEN", qty=0.5, filled_qty=0.0, avg_fill_px=None,
        )

    order = BrokerOrder(cloid="0xdead", oid=9, coin="BTC", side="SELL", size=0.5,
                        status="OPEN", role="SL", reduce_only=True,
                        trigger_px=95.0, order_type="Stop Market")
    assert manager._match_order(order) is None
    events = store.get_events()
    assert any(e["code"] == "RECON_AMBIGUOUS" for e in events)
