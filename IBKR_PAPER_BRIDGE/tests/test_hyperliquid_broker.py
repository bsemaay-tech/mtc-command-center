from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

import pytest

from bridge.broker.hyperliquid import BarFinalizer, BrokerRefusedLive, HyperliquidBroker
from bridge.engine.types import Bar


def test_hyperliquid_mainnet_refuses_without_triple_lock():
    broker = HyperliquidBroker(network="mainnet")

    with pytest.raises(BrokerRefusedLive):
        asyncio.run(broker.connect())


def test_hyperliquid_mainnet_allows_with_triple_lock_and_mock_clients():
    broker = HyperliquidBroker(
        network="mainnet",
        enable_live=True,
        live_ack="I_UNDERSTAND_THIS_IS_REAL_MONEY",
        strategy_live_allowed=True,
        info_client=object(),
        exchange_client=object(),
    )

    asyncio.run(broker.connect())
    assert broker.connected is True


def test_bar_finalizer_emits_once_and_dedupes_reconnect_duplicate():
    emitted: list[Bar] = []
    finalizer = BarFinalizer(on_bar_closed=emitted.append)
    base = datetime(2026, 7, 6, 0, tzinfo=UTC)

    finalizer.on_candle(_candle(base, 100))
    finalizer.on_candle(_candle(base + timedelta(hours=1), 101))
    finalizer.on_candle(_candle(base + timedelta(hours=1), 101))
    finalizer.on_candle(_candle(base + timedelta(hours=2), 102))

    assert [bar.ts for bar in emitted] == [base, base + timedelta(hours=1)]


def _candle(ts: datetime, close: float) -> dict:
    return {
        "t": int(ts.timestamp() * 1000),
        "o": "100",
        "h": str(close + 1),
        "l": str(close - 1),
        "c": str(close),
        "v": "10",
    }
