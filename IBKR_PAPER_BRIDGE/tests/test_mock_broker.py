from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from bridge.broker.mock import MockBroker
from bridge.engine.types import Bar, OrderPlan, Signal


def test_mock_broker_market_fill_and_sl_priority(tmp_path):
    asyncio.run(_run_market_fill_and_sl_priority())


async def _run_market_fill_and_sl_priority():
    bars = [
        Bar(ts=datetime(2026, 7, 6, 0, tzinfo=UTC), open=100, high=101, low=99, close=100, volume=1),
        Bar(ts=datetime(2026, 7, 6, 1, tzinfo=UTC), open=101, high=110, low=94, close=105, volume=1),
    ]
    broker = MockBroker(bars=bars, starting_equity=1000)
    await broker.connect()

    signal = Signal(
        ts=bars[0].ts,
        symbol="BTC",
        direction="LONG",
        reason="test",
        ref_price=100,
    )
    plan = OrderPlan(
        signal=signal,
        qty=0.1,
        entry_type="MKT",
        stop_loss=95,
        take_profit=108,
        leverage=1,
        risk_dollars=0.5,
        risk_pct=0.001,
    )

    ids = await broker.place_bracket(plan)
    assert ids["entry"]["avg_fill_px"] == 101
    assert ids["exit"]["status"] == "FILLED"
    assert ids["exit"]["role"] == "SL"
    assert ids["exit"]["avg_fill_px"] == 95
    assert await broker.positions() == []


def test_mock_broker_loads_fixture():
    broker = MockBroker.from_csv("IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h.csv")

    assert len(broker.bars) >= 2000
    assert broker.coin == "BTC"
