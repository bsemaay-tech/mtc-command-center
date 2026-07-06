from __future__ import annotations

import asyncio
from pathlib import Path

from bridge.broker.mock import MockBroker
from bridge.engine.engine import BridgeEngine
from bridge.engine.orders import OrderManager
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.store.db import Store


def test_dryrun_replay_creates_trade_and_decision_chain(tmp_path):
    asyncio.run(_run_dryrun_replay(tmp_path))


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
    )

    await engine.run_replay(max_bars=60)

    snapshot = store.get_snapshot()
    assert snapshot["trades"]
    chain = store.get_decision_chain(snapshot["trades"][0]["entry_decision_uid"])
    assert [row["stage"] for row in chain] == ["SIGNAL", "RISK_PASS", "LLM_SKIPPED", "SUBMITTED"]
    assert snapshot["orders"][0]["status"] == "FILLED"


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
    )
    await engine.run_replay(max_bars=25)
    first_order_count = len(store.get_snapshot()["orders"])
    await engine.run_replay(max_bars=25)
    assert len(store.get_snapshot()["orders"]) == first_order_count

    engine.disarm()
    await engine.run_replay(max_bars=60)
    assert engine.state == "DISARMED"
