from __future__ import annotations

import asyncio
from pathlib import Path
from datetime import UTC, datetime

from bridge.broker.mock import MockBroker
from bridge.engine.engine import BridgeEngine
from bridge.engine.orders import OrderManager
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.engine.types import Bar, Position, Signal
from bridge.store.db import Store


def test_dryrun_replay_creates_trade_and_decision_chain(tmp_path):
    asyncio.run(_run_dryrun_replay(tmp_path))


def test_engine_uses_broker_protocol_not_mockbroker_bars(tmp_path):
    asyncio.run(_run_protocol_broker_replay(tmp_path))


def test_strategy_drives_stop(tmp_path):
    asyncio.run(_run_strategy_stop(tmp_path))


def test_position_blocks_entry(tmp_path):
    asyncio.run(_run_position_blocks_entry(tmp_path))


def test_disarm_mid_await_no_submit(tmp_path):
    asyncio.run(_run_disarm_mid_await_no_submit(tmp_path))


def test_decision_chain_records_trade_closed(tmp_path):
    asyncio.run(_run_decision_chain_records_trade_closed(tmp_path))


async def _run_dryrun_replay(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    broker = MockBroker.from_csv("IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h.csv", starting_equity=100000)
    risk = RiskEngine(RiskConfig(max_position_notional_pct=0.5))
    engine = BridgeEngine(
        run_id="dryrun-test",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=risk,
        state="ARMED",
    )

    await engine.run_replay(max_bars=60)

    snapshot = store.get_snapshot()
    assert snapshot["trades"]
    chain = store.get_decision_chain(snapshot["trades"][0]["entry_decision_uid"])
    stages = [row["stage"] for row in chain]
    assert stages[:3] == ["SIGNAL", "RISK_PASS", "LLM_SKIPPED"]
    assert "SUBMITTED" in stages
    assert snapshot["orders"]


async def _run_protocol_broker_replay(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    broker = ProtocolOnlyBroker(
        bars=[
            Bar(
                ts=datetime(2026, 7, 6, 0, tzinfo=UTC),
                open=100,
                high=101,
                low=99,
                close=100,
                volume=1,
            )
        ]
    )
    engine = BridgeEngine(
        run_id="protocol-broker",
        broker=broker,
        store=store,
        strategy=NoSignalStrategy(),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )

    await engine.run_replay(max_bars=1)

    snapshot = store.get_snapshot()
    assert len(snapshot["bars"]) == 1
    assert broker.connected is True


async def _run_strategy_stop(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    bar = Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=102, low=99, close=100, volume=1)
    broker = RecordingBroker([bar])
    engine = BridgeEngine(
        run_id="strategy-stop",
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(stop_loss=90.0, take_profit=115.0),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )

    await engine.run_replay(max_bars=1)

    trade = store.get_snapshot()["trades"][0]
    assert trade["sl_initial"] == 90.0
    assert trade["tp_initial"] == 115.0


async def _run_position_blocks_entry(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    bar = Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=102, low=99, close=100, volume=1)
    broker = RecordingBroker(
        [bar],
        positions=[
            Position(
                symbol="BTC",
                size=0.5,
                entry_px=95.0,
                unrealized=1.0,
            )
        ],
    )
    engine = BridgeEngine(
        run_id="position-block",
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(stop_loss=90.0, take_profit=115.0),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )

    await engine.run_replay(max_bars=1)

    assert store.get_snapshot()["trades"] == []
    assert broker.submitted == []


async def _run_disarm_mid_await_no_submit(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    store.set_meta("app_state", "ARMED")
    bar = Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=102, low=99, close=100, volume=1)
    broker = RecordingBroker([bar])
    engine = BridgeEngine(
        run_id="mid-await-disarm",
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(stop_loss=90.0, take_profit=115.0),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        llm_gate=DisarmingGate(store),
        state="ARMED",
    )

    await engine.run_replay(max_bars=1)

    assert store.get_meta("app_state") == "DISARMED"
    assert broker.submitted == []
    assert store.get_snapshot()["trades"] == []


async def _run_decision_chain_records_trade_closed(tmp_path):
    bars = [
        Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=101, low=99, close=100, volume=1),
        Bar(ts=datetime(2026, 7, 6, 1, tzinfo=UTC), open=101, high=104, low=100, close=103, volume=1),
        Bar(ts=datetime(2026, 7, 6, 2, tzinfo=UTC), open=103, high=104, low=94, close=96, volume=1),
    ]
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    broker = MockBroker(bars=bars, starting_equity=100000)
    engine = BridgeEngine(
        run_id="closed-chain",
        broker=broker,
        store=store,
        strategy=FixedSignalStrategy(stop_loss=95.0, take_profit=None),
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )

    await engine.run_replay(max_bars=3)

    trade = store.get_snapshot()["trades"][0]
    stages = [row["stage"] for row in store.get_decision_chain(trade["entry_decision_uid"])]
    assert "TRADE_CLOSED" in stages
    assert trade["exit_reason"] == "SL"


def test_order_manager_duplicate_and_disarmed_guards(tmp_path):
    asyncio.run(_run_order_manager_guards(tmp_path))


async def _run_order_manager_guards(tmp_path):
    store = Store(tmp_path / "bridge.db")
    store.initialize()
    store.create_run("run", "dry_run", "testnet", {})
    broker = MockBroker.from_csv("IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h.csv", starting_equity=100000)
    await broker.connect()
    manager = OrderManager(store=store, broker=broker, run_id="run")

    engine = BridgeEngine(
        run_id="run",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        order_manager=manager,
        risk_engine=RiskEngine(RiskConfig(max_position_notional_pct=0.5)),
        state="ARMED",
    )
    await engine.run_replay(max_bars=25)
    first_order_count = len(store.get_snapshot()["orders"])
    await engine.run_replay(max_bars=25)
    assert len(store.get_snapshot()["orders"]) == first_order_count

    engine.disarm()
    await engine.run_replay(max_bars=60)
    assert engine.state == "DISARMED"


class NoSignalStrategy:
    id = "no_signal"
    warmup_bars = 0

    def on_bar(self, bars, position):
        return None

    def trail_level(self, bars, position):
        return None


class ProtocolOnlyBroker:
    coin = "BTC"

    def __init__(self, bars: list[Bar]) -> None:
        self._replay = bars
        self.connected = False

    async def connect(self) -> None:
        self.connected = True

    async def account(self) -> dict:
        return {"equity": 100000.0, "available_margin": 100000.0}

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
        raise AssertionError("no signal should be submitted")

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        raise AssertionError("no stop should be modified")

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

    def __init__(self, stop_loss: float, take_profit: float | None = None, direction: str = "LONG") -> None:
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.direction = direction

    def on_bar(self, bars, position):
        return Signal(
            ts=bars[-1].ts,
            symbol=self.symbol,
            direction=self.direction,
            reason="fixed",
            ref_price=bars[-1].close,
            stop_loss=self.stop_loss,
            take_profit=self.take_profit,
        )

    def trail_level(self, bars, position):
        return None


class RecordingBroker(ProtocolOnlyBroker):
    def __init__(self, bars: list[Bar], positions: list[Position] | None = None) -> None:
        super().__init__(bars)
        self._positions = positions or []
        self.submitted: list = []

    async def positions(self) -> list[Position]:
        return list(self._positions)

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


class DisarmingGate:
    def __init__(self, store: Store) -> None:
        self.store = store

    async def check(self, plan):
        self.store.set_meta("app_state", "DISARMED")

        class Result:
            reason = "test disarm"

        return Result()
