from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

import pytest

from bridge.broker.hyperliquid import BarFinalizer, BrokerRefusedLive, HyperliquidBroker
from bridge.engine.types import Bar, OrderPlan, Signal


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


def test_hl_bracket_places_native_triggers():
    exchange = FakeExchange()
    broker = HyperliquidBroker(info_client=object(), exchange_client=exchange)
    plan = _plan()

    ids = asyncio.run(broker.place_bracket(plan))

    assert set(ids) == {"entry", "sl", "tp"}
    assert exchange.orders[0]["order_type"] == {"limit": {"tif": "Ioc"}}
    assert exchange.orders[1]["order_type"]["trigger"]["tpsl"] == "sl"
    assert exchange.orders[1]["order_type"]["grouping"] == "positionTpsl"
    assert exchange.orders[1]["reduce_only"] is True
    assert exchange.orders[2]["order_type"]["trigger"]["tpsl"] == "tp"
    assert ids["sl"]["cloid"].startswith("0x")


def test_hl_flatten_reduce_only():
    info = FakeInfo(size="0.25")
    exchange = FakeExchange()
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    asyncio.run(broker.flatten("BTC"))

    close = exchange.orders[-1]
    assert close["coin"] == "BTC"
    assert close["is_buy"] is False
    assert close["sz"] == 0.25
    assert close["reduce_only"] is True


def _candle(ts: datetime, close: float) -> dict:
    return {
        "t": int(ts.timestamp() * 1000),
        "o": "100",
        "h": str(close + 1),
        "l": str(close - 1),
        "c": str(close),
        "v": "10",
    }


def _plan() -> OrderPlan:
    ts = datetime(2026, 7, 6, 0, tzinfo=UTC)
    return OrderPlan(
        signal=Signal(
            ts=ts,
            symbol="BTC",
            direction="LONG",
            reason="test",
            ref_price=100.0,
            stop_loss=95.0,
            take_profit=110.0,
        ),
        qty=0.1,
        entry_type="MKT",
        stop_loss=95.0,
        take_profit=110.0,
    )


class FakeExchange:
    def __init__(self) -> None:
        self.orders: list[dict] = []
        self.modified: list[dict] = []

    def order(self, coin, is_buy, sz, limit_px, order_type, reduce_only=False, cloid=None):
        call = {
            "coin": coin,
            "is_buy": is_buy,
            "sz": sz,
            "limit_px": limit_px,
            "order_type": order_type,
            "reduce_only": reduce_only,
            "cloid": cloid,
        }
        self.orders.append(call)
        return {"status": "ok", "response": {"data": {"statuses": [{"resting": {"oid": len(self.orders)}}]}}}

    def modify_order(self, cloid, order):
        self.modified.append({"cloid": cloid, "order": order})


class FakeInfo:
    def __init__(self, size: str) -> None:
        self.size = size

    def user_state(self, address):
        return {"assetPositions": [{"position": {"coin": "BTC", "szi": self.size}}]}
