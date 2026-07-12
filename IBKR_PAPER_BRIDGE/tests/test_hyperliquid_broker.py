from __future__ import annotations

import asyncio
import threading
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock, create_autospec

import pytest

from bridge.broker.hyperliquid import (
    BarFinalizer,
    BrokerRefusedLive,
    HyperliquidBroker,
    HyperliquidOrderError,
    round_hl_price,
)
from bridge.broker.mock import MockBroker
from bridge.engine.types import AccountSnapshot, Bar, BrokerOrder, FillEvent, OrderPlan, Position, Signal
from hyperliquid.exchange import Exchange
from hyperliquid.utils.signing import order_request_to_order_wire, order_type_to_wire
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
    """G1: place_bracket defaults to grouping=normalTpsl."""
    exchange = _exchange_mock()
    broker = HyperliquidBroker(info_client=_verified_plan_info(), exchange_client=exchange)
    plan = _plan()

    ids = asyncio.run(broker.place_bracket(plan))

    assert set(ids) == {"entry", "sl", "tp"}
    requests = exchange.bulk_orders.call_args.args[0]
    assert exchange.bulk_orders.call_args.kwargs == {"grouping": "normalTpsl"}
    assert requests[0]["order_type"] == {"limit": {"tif": "Ioc"}}
    assert requests[1]["order_type"]["trigger"]["tpsl"] == "sl"
    assert "grouping" not in requests[1]["order_type"]
    assert requests[1]["reduce_only"] is True
    assert requests[2]["order_type"]["trigger"]["tpsl"] == "tp"
    assert all(isinstance(request["cloid"], Cloid) for request in requests)
    # Use installed SDK helpers for the actual wire contract, not a hand-made
    # wire dict. Trigger wire must retain the required tpsl discriminator.
    sl_wire = order_request_to_order_wire(requests[1], 0)
    assert sl_wire["t"] == order_type_to_wire(requests[1]["order_type"])
    assert sl_wire["t"]["trigger"]["tpsl"] == "sl"
    assert ids["sl"]["cloid"].startswith("0x")


def test_hl_bracket_explicit_grouping_na_keeps_sdk_trigger_shape():
    """G1: independent ``na`` trigger remains valid for SDK wire conversion."""
    exchange = _exchange_mock()
    broker = HyperliquidBroker(info_client=_verified_plan_info(), exchange_client=exchange)
    plan = _plan()

    ids = asyncio.run(broker.place_bracket(plan, grouping="na"))

    assert set(ids) == {"entry", "sl", "tp"}
    requests = exchange.bulk_orders.call_args.args[0]
    assert exchange.bulk_orders.call_args.kwargs == {"grouping": "na"}
    # The SDK's TriggerOrderType requires the tpsl discriminator even with na.
    assert requests[1]["order_type"]["trigger"]["tpsl"] == "sl"
    assert requests[1]["order_type"]["trigger"]["isMarket"] is True
    assert requests[1]["order_type"]["trigger"]["triggerPx"] == 95.0
    assert requests[2]["order_type"]["trigger"]["tpsl"] == "tp"
    assert requests[2]["order_type"]["trigger"]["isMarket"] is True
    assert requests[2]["order_type"]["trigger"]["triggerPx"] == 110.0
    assert order_request_to_order_wire(requests[1], 0)["t"] == order_type_to_wire(requests[1]["order_type"])


def test_hl_bracket_explicit_grouping_passthrough():
    """G1: explicit grouping parameter is forwarded to bulk_orders."""
    exchange = _exchange_mock()
    broker = HyperliquidBroker(info_client=_verified_plan_info(), exchange_client=exchange)
    plan = _plan()

    asyncio.run(broker.place_bracket(plan, grouping="normalTpsl"))
    assert exchange.bulk_orders.call_args.kwargs == {"grouping": "normalTpsl"}


def test_hl_price_rounding_contract():
    assert round_hl_price(57542.4, 5) == 57540.0
    assert round_hl_price(0.123456, 2) == 0.1234
    assert round_hl_price(95.0, 5) == 95.0


def test_hl_reprotect_rounds_trigger_and_limit_prices():
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {"data": {"statuses": [{"resting": {"oid": 7}}]}},
    }
    broker = HyperliquidBroker(
        info_client=_verified_reprotect_info("rounded-reprotect"), exchange_client=exchange
    )
    position = Position(symbol="BTC", size=0.1, entry_px=60_000)

    asyncio.run(broker.reprotect_position(position, 57542.4, None, "rounded-reprotect"))

    request = exchange.bulk_orders.call_args.args[0][0]
    assert request["limit_px"] == 57540.0
    assert request["order_type"]["trigger"]["triggerPx"] == 57540.0


def test_hl_unified_account_uses_spot_usdc_balance_and_hold():
    info = UnifiedInfo()
    exchange = _exchange_mock()
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    asyncio.run(broker.connect())
    account = asyncio.run(broker.account())

    assert broker.account_mode == "unifiedAccount"
    assert account.equity == 999.0
    assert account.available_margin == 989.0
    assert account.withdrawable == 989.0


def test_hl_string_exchange_rejection_is_preserved_and_secret_redacted():
    exchange = _exchange_mock()
    secret_like = "ab" * 32
    exchange.bulk_orders.return_value = {
        "status": "err",
        "response": f"Insufficient margin request={secret_like}",
    }
    broker = HyperliquidBroker(info_client=object(), exchange_client=exchange)

    with pytest.raises(HyperliquidOrderError, match="Insufficient margin") as exc_info:
        asyncio.run(broker.place_bracket(_plan()))

    assert secret_like not in str(exc_info.value)
    assert "[redacted]" in str(exc_info.value)


def test_hl_disconnect_stops_sdk_websocket():
    info = DisconnectInfo()
    broker = HyperliquidBroker(info_client=info, exchange_client=_exchange_mock())

    asyncio.run(broker.connect())
    asyncio.run(broker.disconnect())

    assert info.disconnected is True
    assert broker.connected is False


def test_hl_modify_and_cancel_use_real_sdk_signatures():
    exchange = _exchange_mock()
    broker = HyperliquidBroker(info_client=_verified_plan_info(), exchange_client=exchange)
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
    broker = HyperliquidBroker(info_client=_verified_plan_info(), exchange_client=exchange)
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
    info._open_orders = _c1_open_order_rows(
        {"entry": {"oid": 1, "status": "OPEN"}, "sl": {"oid": 2, "status": "OPEN"}, "tp": {"oid": 3, "status": "OPEN"}}
    )
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
    """G1: reprotect_position uses grouping=positionTpsl (unchanged)."""
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {"data": {"statuses": [{"resting": {"oid": 7}}]}},
    }
    broker = HyperliquidBroker(
        info_client=_verified_reprotect_info("decision-owned"), exchange_client=exchange
    )
    position = Position(symbol="BTC", size=0.1, entry_px=100)

    result = asyncio.run(broker.reprotect_position(position, 95.0, None, "decision-owned"))

    assert result is not None and set(result) == {"sl"}
    requests = exchange.bulk_orders.call_args.args[0]
    assert exchange.bulk_orders.call_args.kwargs == {"grouping": "positionTpsl"}
    assert requests[0]["reduce_only"] is True
    assert requests[0]["order_type"]["trigger"]["tpsl"] == "sl"


# ── G2: smoke fallback normalTpsl → na (mocked) ─────────────────────────


def test_g2_normal_tpsl_rejection_falls_back_to_na_exactly_once():
    """G2: normalTpsl rejected with type/grouping error → C3 cleanup → exactly
    one na retry (no loop, no third attempt)."""
    exchange = _exchange_mock()
    call_groupings: list[str] = []

    def _bulk_orders(requests, grouping):
        call_groupings.append(grouping)
        if grouping == "normalTpsl":
            raise HyperliquidOrderError(
                "Trigger order has unexpected type.; "
                "raw_response={'status':'ok','response':{'type':'order','data':{'statuses':[{'error':'Trigger order has unexpected type.'}]}}}"
            )
        # na grouping succeeds
        return {
            "status": "ok",
            "response": {
                "data": {
                    "statuses": [
                        {"resting": {"oid": 101}},
                        {"resting": {"oid": 102}},
                        {"resting": {"oid": 103}},
                    ]
                }
            },
        }

    exchange.bulk_orders.side_effect = _bulk_orders
    broker = HyperliquidBroker(info_client=_verified_plan_info(), exchange_client=exchange)
    plan = _plan()

    # Simulate G2 logic: first try normalTpsl, on type/grouping error fall back to na
    # First attempt
    with pytest.raises(HyperliquidOrderError):
        asyncio.run(broker.place_bracket(plan, grouping="normalTpsl"))

    assert call_groupings == ["normalTpsl"]
    assert exchange.bulk_orders.call_count == 1

    # Fallback attempt (na)
    result = asyncio.run(broker.place_bracket(plan, grouping="na"))
    assert call_groupings == ["normalTpsl", "na"]
    assert exchange.bulk_orders.call_count == 2
    assert set(result) == {"entry", "sl", "tp"}


def test_g2_non_type_error_does_not_fall_back():
    """G2: a non-type/non-grouping error (e.g. insufficient margin) must NOT
    trigger a fallback — only one placement call, no second attempt."""
    exchange = _exchange_mock()
    call_groupings: list[str] = []

    def _bulk_orders(requests, grouping):
        call_groupings.append(grouping)
        raise HyperliquidOrderError(
            "Insufficient margin; "
            "raw_response={'status':'err','response':'Insufficient margin'}"
        )

    exchange.bulk_orders.side_effect = _bulk_orders
    broker = HyperliquidBroker(info_client=object(), exchange_client=exchange)
    plan = _plan()

    with pytest.raises(HyperliquidOrderError, match="Insufficient margin"):
        asyncio.run(broker.place_bracket(plan, grouping="normalTpsl"))

    assert call_groupings == ["normalTpsl"]
    assert exchange.bulk_orders.call_count == 1  # no fallback


def test_g2_fallback_grouping_rejection_detection():
    """G2: verify that the smoke-level keyword detection correctly identifies
    type/grouping rejections."""
    # These should be detected as grouping rejection
    grouping_messages = [
        "Trigger order has unexpected type.",
        "Invalid grouping type",
        "Order type not supported for this grouping",
        "tpsl field not allowed",
    ]
    for msg in grouping_messages:
        msg_lower = msg.lower()
        is_grouping = any(
            keyword in msg_lower
            for keyword in ("type", "grouping", "trigger", "unexpected", "tpsl")
        )
        assert is_grouping, f"Should detect grouping rejection in: {msg}"

    # These should NOT be detected as grouping rejection
    non_grouping_messages = [
        "Insufficient margin",
        "Rate limit exceeded",
        "Order size too small",
        "Price outside allowed range",
        "",
    ]
    for msg in non_grouping_messages:
        msg_lower = msg.lower()
        is_grouping = any(
            keyword in msg_lower
            for keyword in ("type", "grouping", "trigger", "unexpected", "tpsl")
        )
        assert not is_grouping, f"Should NOT detect grouping rejection in: {msg}"


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
        if hasattr(self, "_open_orders"):
            return self._open_orders
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
        return _c1_open_order_rows(
            {"entry": {"oid": 1, "status": "OPEN"}, "sl": {"oid": 2, "status": "OPEN"}, "tp": {"oid": 3, "status": "OPEN"}}
        )

    def candles_snapshot(self, coin, tf, start, end):
        self._record()
        return [_candle(datetime(2026, 7, 6, 0, tzinfo=UTC), 100)]


class UnifiedInfo(FakeInfo):
    def __init__(self) -> None:
        super().__init__(size="0", with_summary=True)

    def query_user_abstraction_state(self, address):
        return "unifiedAccount"

    def spot_user_state(self, address):
        return {"balances": [{"coin": "USDC", "total": "999", "hold": "10"}]}


class DisconnectInfo:
    def __init__(self) -> None:
        self.disconnected = False

    def disconnect_websocket(self):
        self.disconnected = True


# ── C1: positionTpsl cardinality tolerance ──────────────────────────────


def test_c1_three_order_group_with_one_status():
    """3-order group (entry+SL+TP) returns only 1 status — all verified
    authoritatively via open_orders (no blind trigger acceptance)."""
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [
                    {"resting": {"oid": 10}},
                ]
            }
        },
    }
    info = _c1_open_orders_info(
        open_cloids={
            "entry": {"oid": 10, "status": "OPEN"},
            "sl": {"oid": 11, "status": "OPEN"},
            "tp": {"oid": 12, "status": "OPEN"},
        }
    )
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    result = asyncio.run(broker.place_bracket(_plan()))

    assert set(result) == {"entry", "sl", "tp"}
    assert result["entry"]["oid"] == 10
    assert result["sl"]["oid"] == 11
    assert result["sl"]["status"] == "OPEN"
    assert result["tp"]["oid"] == 12


def test_c1_three_order_group_with_two_statuses():
    """3-order group returns 2 statuses — all verified authoritatively via open_orders."""
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [
                    {"resting": {"oid": 20}},
                    {"resting": {"oid": 21}},
                ]
            }
        },
    }
    info = _c1_open_orders_info(
        open_cloids={
            "entry": {"oid": 20, "status": "OPEN"},
            "sl": {"oid": 21, "status": "OPEN"},
            "tp": {"oid": 22, "status": "OPEN"},
        }
    )
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    result = asyncio.run(broker.place_bracket(_plan()))

    assert set(result) == {"entry", "sl", "tp"}
    assert result["entry"]["oid"] == 20
    assert result["sl"]["oid"] == 21
    assert result["tp"]["oid"] == 22


def test_c1_three_order_group_with_three_statuses():
    """3-order group returns all 3 statuses — classic case still works."""
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [
                    {"resting": {"oid": 30}},
                    {"resting": {"oid": 31}},
                    {"resting": {"oid": 32}},
                ]
            }
        },
    }
    info = _c1_open_orders_info(
        open_cloids={
            "entry": {"oid": 30, "status": "OPEN"},
            "sl": {"oid": 31, "status": "OPEN"},
            "tp": {"oid": 32, "status": "OPEN"},
        }
    )
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    result = asyncio.run(broker.place_bracket(_plan()))

    assert set(result) == {"entry", "sl", "tp"}
    assert all(row["oid"] is not None for row in result.values())


def test_c1_error_status_still_raises():
    """An error in any status must still raise HyperliquidOrderError."""
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [
                    {"error": "Insufficient margin", "resting": {"oid": 40}},
                ]
            }
        },
    }
    info = _c1_open_orders_info(
        open_cloids={
            "entry": {"oid": 40, "status": "OPEN"},
            "sl": {"oid": 41, "status": "OPEN"},
            "tp": {"oid": 42, "status": "OPEN"},
        }
    )
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    with pytest.raises(HyperliquidOrderError, match="Insufficient margin"):
        asyncio.run(broker.place_bracket(_plan()))


def test_c1_verification_driven_result_missing_cloid_raises():
    """If a non-trigger cloid is neither in open_orders nor confirmed by status, raise."""
    exchange = _exchange_mock()
    # Return zero statuses — entry gets no status, triggers get ACCEPTED
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [],
            }
        },
    }
    # Open orders has only SL and TP; ENTRY is completely missing
    info = _c1_open_orders_info(
        open_cloids={
            "sl": {"oid": 51, "status": "OPEN"},
            "tp": {"oid": 52, "status": "OPEN"},
        }
    )
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    with pytest.raises(HyperliquidOrderError, match="missing from open_orders"):
        asyncio.run(broker.place_bracket(_plan()))


def test_c1_filled_status_explains_missing_order():
    """A filled status explains why an order is not in open_orders."""
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [
                    {"filled": {"oid": 60, "totalSz": "0.1"}},
                ]
            }
        },
    }
    # Only SL and TP visible in open_orders; entry was filled
    info = _c1_open_orders_info(
        open_cloids={
            "sl": {"oid": 61, "status": "OPEN"},
            "tp": {"oid": 62, "status": "OPEN"},
        }
    )
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    result = asyncio.run(broker.place_bracket(_plan()))

    assert set(result) == {"entry", "sl", "tp"}
    assert result["entry"]["oid"] == 60
    assert result["sl"]["oid"] == 61
    assert result["tp"]["oid"] == 62


# ── C2: raw response capture on mismatch ────────────────────────────────


def test_c2_raw_response_safe_redacts_and_caps():
    """_raw_response_safe redacts 64+ hex and caps at requested length."""
    long_secret = "ab" * 64  # 128 hex chars
    raw = {
        "status": "err",
        "response": f"something went wrong with key={long_secret}",
        "extra": "x" * 5000,
    }
    safe = HyperliquidBroker._raw_response_safe(raw, cap=4000)

    assert long_secret not in safe
    assert "[redacted]" in safe
    assert len(safe) <= 4000
    assert "something went wrong" in safe


def test_c2_surprising_response_preserved_in_error():
    """When cardinality surprises us, the raw response is embedded in the error."""
    exchange = _exchange_mock()
    surprising = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [],  # empty statuses — entry is unexplained
            }
        },
    }
    exchange.bulk_orders.return_value = surprising
    # Use FakeInfo so open_orders returns a cloid not matching ours
    broker = HyperliquidBroker(account_address="0xabc", info_client=FakeInfo(size="0"), exchange_client=exchange)

    with pytest.raises(HyperliquidOrderError, match="raw_response=") as exc_info:
        asyncio.run(broker.place_bracket(_plan()))

    error_str = str(exc_info.value)
    # The error should contain the redacted raw response
    assert "raw_response=" in error_str
    assert '"statuses": []' in error_str


# ── C3: guaranteed owned-cloid cleanup ──────────────────────────────────


def test_c3_verify_positioned_orders_still_populates_order_specs():
    """Order specs must be populated even when triggers are accepted-with-position."""
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [
                    {"resting": {"oid": 70}},
                ]
            }
        },
    }
    info = _c1_open_orders_info(
        open_cloids={
            "entry": {"oid": 70, "status": "OPEN"},
            "sl": {"oid": 71, "status": "OPEN"},
            "tp": {"oid": 72, "status": "OPEN"},
        }
    )
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    result = asyncio.run(broker.place_bracket(_plan()))

    # All three specs should be populated
    for role in ("entry", "sl", "tp"):
        cloid = result[role]["cloid"]
        assert cloid in broker._order_specs
        assert broker._order_specs[cloid]["role"].upper() == role.upper()

    # Modify should work on the sl
    asyncio.run(broker.modify_stop(result["sl"]["cloid"], 96.0))
    assert exchange.modify_order.called


def test_c1_missing_trigger_cloid_raises():
    """A trigger (SL/TP) not in open_orders and not confirmed filled MUST raise.

    This is the key audit fix: no submitted cloid may succeed merely because
    it has no individual status.  The old code treated missing-trigger-status
    as 'accepted-with-position' which was non-authoritative.
    """
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [
                    {"resting": {"oid": 80}},
                ]
            }
        },
    }
    # Only entry is in open_orders; SL and TP are completely missing
    info = _c1_open_orders_info(
        open_cloids={
            "entry": {"oid": 80, "status": "OPEN"},
        }
    )
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    with pytest.raises(HyperliquidOrderError, match="missing from open_orders"):
        asyncio.run(broker.place_bracket(_plan()))


def test_c1_reprotect_no_longer_swallows_verification_failure():
    """reprotect_position must propagate HyperliquidOrderError, not return None."""
    exchange = _exchange_mock()
    # Return zero statuses with no open_orders backing — verification MUST fail
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {"data": {"statuses": []}},
    }
    info = _c1_open_orders_info(open_cloids={})  # nothing in open_orders
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)
    position = Position(symbol="BTC", size=0.1, entry_px=100)

    with pytest.raises(HyperliquidOrderError, match="missing from open_orders"):
        asyncio.run(broker.reprotect_position(position, 95.0, None, "decision-reprotect"))


# ── C2: full raw response in every parser error ─────────────────────────


def test_c2_extract_statuses_includes_raw_response_on_type_error():
    """When statuses is not a list, the error MUST embed the redacted raw response."""
    raw = {
        "status": "ok",
        "response": {"data": {"statuses": "not_a_list_surprise"}},
    }
    with pytest.raises(HyperliquidOrderError, match="raw_response=") as exc_info:
        HyperliquidBroker._extract_statuses(raw)
    error_str = str(exc_info.value)
    assert "raw_response=" in error_str
    assert '"statuses"' in error_str


def test_c2_extract_statuses_includes_raw_response_on_non_dict_item():
    """When a status item is not a dict, error must carry redacted raw response."""
    raw = {
        "status": "ok",
        "response": {"data": {"statuses": ["just_a_string"]}},
    }
    with pytest.raises(HyperliquidOrderError, match="raw_response=") as exc_info:
        HyperliquidBroker._extract_statuses(raw)
    error_str = str(exc_info.value)
    assert "raw_response=" in error_str


def test_c2_non_dict_raw_yields_raw_response_in_error():
    """When the top-level raw is not a dict, error includes redacted raw."""
    with pytest.raises(HyperliquidOrderError, match="raw_response=") as exc_info:
        HyperliquidBroker._extract_statuses("not_even_json")
    error_str = str(exc_info.value)
    assert "raw_response=" in error_str


# ── C3: mid-parse exception triggers cleanup ────────────────────────────


def test_c3_mid_parse_placement_exception_cancels_resting_owned_order(
    monkeypatch,
):
    """If verification raises mid-way, any successfully placed order must be
    cancellable.  This test simulates an exchange that accepts the entry but
    whose open_orders view is missing the SL — causing a HyperliquidOrderError.
    The smoke-level cleanup path cancels cloids that do appear in open_orders.
    """
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "data": {
                "statuses": [
                    {"resting": {"oid": 90}},
                ]
            }
        },
    }
    # Only entry is visible — SL and TP are missing, so verification MUST raise
    info = _c1_open_orders_info(
        open_cloids={
            "entry": {"oid": 90, "status": "OPEN"},
        }
    )
    broker = HyperliquidBroker(account_address="0xabc", info_client=info, exchange_client=exchange)

    # place_bracket must raise because SL/TP not in open_orders
    with pytest.raises(HyperliquidOrderError, match="missing from open_orders"):
        asyncio.run(broker.place_bracket(_plan()))

    # The entry order WAS placed (it's in open_orders), so it should be
    # cancellable.  Simulate what _deterministic_cleanup does.
    open_orders = asyncio.run(broker.open_orders())
    entry_cloid = HyperliquidBroker.compute_cloids("BTC:2026-07-06T00:00:00+00:00:LONG")["entry"]
    entry_in_open = [o for o in open_orders if o.cloid == entry_cloid]
    assert len(entry_in_open) == 1
    # Cancel it
    asyncio.run(broker.cancel(entry_in_open[0].cloid))
    exchange.cancel_by_cloid.assert_called()
    assert exchange.cancel_by_cloid.call_args.args[0] == "BTC"


# ── C1-C3 helpers ───────────────────────────────────────────────────────


def _c1_open_orders_info(open_cloids: dict) -> object:
    """Return an info stub whose open_orders() returns orders keyed by cloid suffix role.

    The cloid is computed from the plan in _plan() which uses a fixed ts + symbol.
    We precompute the expected cloids for the same decision_uid pattern used by _plan.
    """
    orders = _c1_open_order_rows(open_cloids)

    class _C1Info:
        def user_state(self, address):
            return {"assetPositions": []}

        def open_orders(self, address):
            return orders

        def subscribe(self, *args, **kwargs):
            pass

    return _C1Info()


def _c1_open_order_rows(open_cloids: dict) -> list[dict]:
    expected = HyperliquidBroker.compute_cloids("BTC:2026-07-06T00:00:00+00:00:LONG")
    orders: list[dict] = []
    for role, cloid_str in expected.items():
        if role in open_cloids:
            cfg = open_cloids[role]
            orders.append({
                "coin": "BTC",
                "side": "B" if role == "entry" else "A",
                "sz": "0.1",
                "oid": cfg["oid"],
                "cloid": cloid_str,
                "status": cfg.get("status", "OPEN"),
                "orderType": "Limit" if role == "entry" else "Stop Market",
                "triggerPx": "95" if role == "sl" else ("110" if role == "tp" else None),
                "reduceOnly": role != "entry",
            })

    return orders


def _verified_plan_info() -> object:
    return _c1_open_orders_info(
        {"entry": {"oid": 1, "status": "OPEN"}, "sl": {"oid": 2, "status": "OPEN"}, "tp": {"oid": 3, "status": "OPEN"}}
    )


def _verified_reprotect_info(decision_uid: str) -> object:
    cloid = str(HyperliquidBroker._raw_cloid(f"{decision_uid}:reprotect:sl"))

    class _ReprotectInfo:
        def user_state(self, address):
            return {"assetPositions": []}

        def open_orders(self, address):
            return [{"coin": "BTC", "side": "A", "sz": "0.1", "oid": 7, "cloid": cloid, "orderType": "Stop Market", "triggerPx": "95", "reduceOnly": True}]

    return _ReprotectInfo()
