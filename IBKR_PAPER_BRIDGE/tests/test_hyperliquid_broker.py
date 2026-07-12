from __future__ import annotations

import asyncio
import threading
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock, create_autospec

import pytest

from bridge.broker.hyperliquid import BarFinalizer, BrokerRefusedLive, HyperliquidBroker
from bridge.broker.mock import MockBroker
from bridge.engine.types import AccountSnapshot, Bar, BrokerOrder, FillEvent, OrderPlan, Position, Signal
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


def test_hl_modify_stop_fallback_replaces_with_clean_order_request():
    exchange = _exchange_mock()
    broker = HyperliquidBroker(info_client=object(), exchange_client=exchange)
    ids = asyncio.run(broker.place_bracket(_plan()))
    exchange.modify_order.side_effect = RuntimeError("forced modify failure")

    asyncio.run(broker.modify_stop(ids["sl"]["cloid"], 96.0))

    replacement = exchange.bulk_orders.call_args_list[-1].args[0][0]
    assert set(replacement) == {
        "coin",
        "is_buy",
        "sz",
        "limit_px",
        "order_type",
        "reduce_only",
        "cloid",
    }
    assert replacement["limit_px"] == 96.0
    assert replacement["reduce_only"] is True
    assert replacement["order_type"] == {
        "trigger": {"triggerPx": 96.0, "isMarket": True, "tpsl": "sl"}
    }


@pytest.mark.parametrize("position_size", ["0.25", "-0.25"])
def test_hl_flatten_uses_market_close_for_long_and_short(position_size):
    info = FakeInfo(size=position_size)
    exchange = _exchange_mock()
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    asyncio.run(broker.flatten("BTC"))

    close = exchange.market_close.call_args
    assert close.args == ("BTC",)
    assert close.kwargs["sz"] == 0.25
    assert close.kwargs["slippage"] == 0.05
    assert isinstance(close.kwargs["cloid"], Cloid)


def test_hl_flatten_zero_position_does_not_submit_close():
    exchange = _exchange_mock()
    broker = HyperliquidBroker(
        account_address="0xabc",
        info_client=FakeInfo(size="0"),
        exchange_client=exchange,
    )

    asyncio.run(broker.flatten("BTC"))

    exchange.market_close.assert_not_called()
    exchange.order.assert_not_called()


@pytest.mark.parametrize(
    ("position_size", "crossing_px", "expected_is_buy"),
    [("0.25", 95.0, False), ("-0.25", 105.0, True)],
)
def test_installed_sdk_market_close_builds_crossing_reduce_only_ioc(
    position_size,
    crossing_px,
    expected_is_buy,
):
    exchange = create_autospec(Exchange, instance=True)
    exchange.wallet = SimpleNamespace(address="0xabc")
    exchange.account_address = "0xabc"
    exchange.vault_address = None
    exchange.info = SimpleNamespace(
        user_state=Mock(
            return_value={
                "assetPositions": [{"position": {"coin": "BTC", "szi": position_size}}]
            }
        )
    )
    exchange._slippage_price.return_value = crossing_px
    cloid = Cloid.from_int(1)

    Exchange.market_close(exchange, "BTC", sz=0.25, slippage=0.05, cloid=cloid)

    order = exchange.order.call_args
    assert order.args[:4] == ("BTC", expected_is_buy, 0.25, crossing_px)
    assert crossing_px > 0
    assert order.kwargs["order_type"] == {"limit": {"tif": "Ioc"}}
    assert order.kwargs["reduce_only"] is True
    assert order.kwargs["cloid"] is cloid


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


def test_hl_user_fill_event_is_typed_and_mapped_by_oid():
    info = FakeInfo(size="0", with_summary=True)
    exchange = _exchange_mock()
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)
    asyncio.run(broker.place_bracket(_plan()))
    events = []
    broker.subscribe_user_events(events.append)

    broker._receive_user_message(
        {
            "channel": "user",
            "data": {
                "fills": [
                    {"oid": 1, "coin": "BTC", "sz": "0.1", "px": "100", "time": 1783814400000, "tid": 99}
                ]
            },
        }
    )

    assert isinstance(events[0], FillEvent)
    assert events[0].role == "ENTRY"
    assert events[0].cloid.startswith("0x")
    assert {sub["type"] for sub, _ in info.subscriptions} == {"userEvents", "orderUpdates"}


def test_hl_reprotects_position_with_native_trigger_group():
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {"data": {"statuses": [{"resting": {"oid": 7}}]}},
    }
    broker = HyperliquidBroker(info_client=object(), exchange_client=exchange)
    position = Position(symbol="BTC", size=0.1, entry_px=100)

    result = asyncio.run(broker.reprotect_position(position, 95.0, None, "decision-owned"))

    assert result is not None and set(result) == {"sl"}
    requests = exchange.bulk_orders.call_args.args[0]
    assert exchange.bulk_orders.call_args.kwargs == {"grouping": "positionTpsl"}
    assert requests[0]["reduce_only"] is True
    assert requests[0]["order_type"]["trigger"]["tpsl"] == "sl"


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
        self.subscriptions: list[tuple[dict, object]] = []

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

    def subscribe(self, subscription, callback):
        self.subscriptions.append((subscription, callback))
        return len(self.subscriptions)


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
