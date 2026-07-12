from __future__ import annotations

import asyncio
import threading
from datetime import UTC, datetime, timedelta
from unittest.mock import create_autospec

import pytest

from bridge.broker.hyperliquid import BarFinalizer, BrokerRefusedLive, HyperliquidBroker
from bridge.broker.mock import MockBroker
from bridge.engine.types import AccountSnapshot, Bar, BrokerOrder, OrderPlan, Position, Signal
from hyperliquid.exchange import Exchange
from hyperliquid.utils.types import Cloid


def test_hyperliquid_mainnet_refuses_without_triple_lock():
    broker = HyperliquidBroker(network="mainnet")

    with pytest.raises(BrokerRefusedLive):
        asyncio.run(broker.connect())


def test_hyperliquid_mainnet_allows_with_triple_lock_and_mock_clients():
    exchange = _exchange_mock()
    broker = HyperliquidBroker(
        network="mainnet",
        enable_live=True,
        live_ack="I_UNDERSTAND_THIS_IS_REAL_MONEY",
        strategy_live_allowed=True,
        info_client=object(),
        exchange_client=exchange,
    )

    asyncio.run(broker.connect())
    assert broker.connected is True
    exchange.update_leverage.assert_called_once_with(1, "BTC", is_cross=False)


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
    exchange = _exchange_mock()
    broker = HyperliquidBroker(info_client=object(), exchange_client=exchange)
    plan = _plan()

    ids = asyncio.run(broker.place_bracket(plan))

    assert set(ids) == {"entry", "sl", "tp"}
    requests = exchange.bulk_orders.call_args.args[0]
    assert exchange.bulk_orders.call_args.kwargs == {"grouping": "positionTpsl"}
    assert requests[0]["order_type"] == {"limit": {"tif": "Ioc"}}
    assert requests[1]["order_type"]["trigger"]["tpsl"] == "sl"
    assert "grouping" not in requests[1]["order_type"]
    assert requests[1]["reduce_only"] is True
    assert requests[2]["order_type"]["trigger"]["tpsl"] == "tp"
    assert all(isinstance(request["cloid"], Cloid) for request in requests)
    assert ids["sl"]["cloid"].startswith("0x")


def test_hl_modify_and_cancel_use_real_sdk_signatures():
    exchange = _exchange_mock()
    broker = HyperliquidBroker(info_client=object(), exchange_client=exchange)
    ids = asyncio.run(broker.place_bracket(_plan()))

    asyncio.run(broker.modify_stop(ids["sl"]["cloid"], 96.0))
    asyncio.run(broker.cancel(ids["sl"]["cloid"]))

    modify = exchange.modify_order.call_args
    assert isinstance(modify.args[0], Cloid)
    assert modify.args[1:6] == ("BTC", False, 0.1, 96.0, {"trigger": {"triggerPx": 96.0, "isMarket": True, "tpsl": "sl"}})
    assert modify.kwargs["reduce_only"] is True
    assert isinstance(modify.kwargs["cloid"], Cloid)
    cancel = exchange.cancel_by_cloid.call_args
    assert cancel.args[0] == "BTC"
    assert isinstance(cancel.args[1], Cloid)


def test_hl_flatten_reduce_only():
    info = FakeInfo(size="0.25")
    exchange = _exchange_mock()
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    asyncio.run(broker.flatten("BTC"))

    close = exchange.order.call_args
    assert close.args[:4] == ("BTC", False, 0.25, 0)
    assert close.kwargs["reduce_only"] is True
    assert isinstance(close.kwargs["cloid"], Cloid)


def test_broker_normalization_type_parity():
    info = FakeInfo(size="0.25", with_summary=True)
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=_exchange_mock())
    mock = MockBroker(bars=[], starting_equity=1000)

    account = asyncio.run(broker.account())
    positions = asyncio.run(broker.positions())
    orders = asyncio.run(broker.open_orders())
    mock_account = asyncio.run(mock.account())

    assert isinstance(account, AccountSnapshot)
    assert account.equity == 999.0
    assert account.available_margin == 989.0
    assert account.withdrawable == 980.0
    assert isinstance(positions[0], Position)
    assert positions[0].symbol == "BTC"
    assert positions[0].leverage == 1
    assert isinstance(orders[0], BrokerOrder)
    assert orders[0].role == "SL"
    assert isinstance(mock_account, AccountSnapshot)


def test_async_sdk_calls_are_offloaded_from_event_loop_thread():
    main_thread = threading.get_ident()
    info = ThreadRecordingInfo()
    exchange = _exchange_mock()
    exchange_threads: list[int] = []
    exchange.update_leverage.side_effect = lambda *args, **kwargs: exchange_threads.append(threading.get_ident())
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    async def exercise() -> None:
        await broker.connect()
        await broker.account()
        await broker.positions()
        await broker.open_orders()
        await broker.historical_bars("BTC", "1h", 1)
        await broker.place_bracket(_plan())

    asyncio.run(exercise())

    assert info.threads
    assert all(thread_id != main_thread for thread_id in info.threads)
    assert exchange_threads and exchange_threads[0] != main_thread


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


def _exchange_mock():
    exchange = create_autospec(Exchange, instance=True)
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [
                    {"resting": {"oid": 1}},
                    {"resting": {"oid": 2}},
                    {"resting": {"oid": 3}},
                ]
            }
        },
    }
    exchange.order.return_value = {"status": "ok", "response": {"data": {"statuses": [{"resting": {"oid": 4}}]}}}
    return exchange


class FakeInfo:
    def __init__(self, size: str, with_summary: bool = False) -> None:
        self.size = size
        self.with_summary = with_summary

    def user_state(self, address):
        state = {
            "assetPositions": [
                {
                    "position": {
                        "coin": "BTC",
                        "szi": self.size,
                        "entryPx": "100",
                        "unrealizedPnl": "2.5",
                        "leverage": {"type": "isolated", "value": 1},
                        "liquidationPx": None,
                        "marginUsed": "25",
                    }
                }
            ]
        }
        if self.with_summary:
            state.update(
                {
                    "marginSummary": {"accountValue": "999", "totalMarginUsed": "10"},
                    "withdrawable": "980",
                }
            )
        return state

    def open_orders(self, address):
        return [
            {
                "coin": "BTC",
                "side": "A",
                "sz": "0.25",
                "oid": 12,
                "cloid": "0x00000000000000000000000000000012",
                "orderType": "Stop Market",
                "triggerPx": "95",
                "reduceOnly": True,
            }
        ]


class ThreadRecordingInfo(FakeInfo):
    def __init__(self) -> None:
        super().__init__(size="0", with_summary=True)
        self.threads: list[int] = []

    def _record(self) -> None:
        self.threads.append(threading.get_ident())

    def user_state(self, address):
        self._record()
        return super().user_state(address)

    def open_orders(self, address):
        self._record()
        return []

    def candles_snapshot(self, coin, tf, start, end):
        self._record()
        return [_candle(datetime(2026, 7, 6, 0, tzinfo=UTC), 100)]
