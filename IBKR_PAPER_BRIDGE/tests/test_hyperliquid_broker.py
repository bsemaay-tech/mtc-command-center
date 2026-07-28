from __future__ import annotations

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
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
from bridge.broker.base import BrokerPreSendFailure
from bridge.broker.mock import MockBroker
from bridge.engine.types import AccountSnapshot, Bar, BrokerOrder, FillEvent, OrderPlan, Position, Signal
from bridge.store.db import KillConflictError, Store
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


def test_hl_bracket_pre_send_veto_is_definitively_not_transmitted():
    exchange = _exchange_mock()
    broker = HyperliquidBroker(
        info_client=_verified_plan_info(), exchange_client=exchange
    )

    with pytest.raises(BrokerPreSendFailure) as exc_info:
        asyncio.run(
            broker.place_bracket(_plan(), pre_send_guard=lambda: False)
        )

    assert exc_info.value.reason_code == "HL_KILL_PRE_SEND_VETO"
    assert exc_info.value.write_may_have_started is False
    exchange.bulk_orders.assert_not_called()


def test_hl_bracket_executor_rechecks_kill_guard_after_queue_delay():
    async def scenario() -> None:
        exchange = _exchange_mock()
        broker = HyperliquidBroker(
            info_client=_verified_plan_info(), exchange_client=exchange
        )
        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        loop.set_default_executor(executor)
        blocker_started = threading.Event()
        release_blocker = threading.Event()
        guard_enabled = True
        guard_calls = 0

        def occupy_executor() -> None:
            blocker_started.set()
            release_blocker.wait(timeout=5)

        def guard() -> bool:
            nonlocal guard_calls
            guard_calls += 1
            return guard_enabled

        blocker = asyncio.create_task(asyncio.to_thread(occupy_executor))
        while not blocker_started.is_set():
            await asyncio.sleep(0)
        placement = asyncio.create_task(
            broker.place_bracket(_plan(), pre_send_guard=guard)
        )
        while guard_calls < 1:
            await asyncio.sleep(0)
        guard_enabled = False
        release_blocker.set()
        await blocker

        with pytest.raises(BrokerPreSendFailure) as exc_info:
            await placement
        assert exc_info.value.reason_code == "HL_KILL_PRE_SEND_VETO"
        assert exc_info.value.write_may_have_started is False
        assert guard_calls == 2
        exchange.bulk_orders.assert_not_called()
        executor.shutdown(wait=True)

    asyncio.run(scenario())


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


def test_hl_bracket_waiting_for_fill_child_is_verified_pending():
    """W1: real attempt-6 shape — resting entry + string waitingForFill child.

    Testnet returned: statuses = [{"resting": {oid, cloid}}, "waitingForFill"].
    Pending children are not in open_orders by design; they must verify as
    WAITING_CHILD instead of raising.
    """
    exchange = _exchange_mock()
    expected = HyperliquidBroker.compute_cloids("BTC:2026-07-06T00:00:00+00:00:LONG")
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "type": "order",
            "data": {
                "statuses": [
                    {"resting": {"oid": 56380800181, "cloid": expected["entry"]}},
                    "waitingForFill",
                    "waitingForTrigger",
                ]
            },
        },
    }
    broker = HyperliquidBroker(
        info_client=_c1_open_orders_info({"entry": {"oid": 56380800181, "status": "OPEN"}}),
        exchange_client=exchange,
    )

    ids = asyncio.run(broker.place_bracket(_plan()))

    assert ids["entry"]["oid"] == 56380800181
    assert ids["sl"]["status"] == "WAITING_CHILD"
    assert ids["sl"]["pending_reason"] == "waitingForFill"
    assert ids["sl"]["oid"] is None
    assert ids["sl"]["trigger_px"] == 95.0
    assert ids["tp"]["status"] == "WAITING_CHILD"
    assert ids["tp"]["pending_reason"] == "waitingForTrigger"


def test_hl_unknown_string_status_still_raises_with_raw_response():
    """W1: only known pending-child strings are accepted; others stay errors."""
    exchange = _exchange_mock()
    exchange.bulk_orders.return_value = {
        "status": "ok",
        "response": {
            "type": "order",
            "data": {"statuses": [{"resting": {"oid": 1}}, "somethingUnexpected"]},
        },
    }
    broker = HyperliquidBroker(
        info_client=_c1_open_orders_info({"entry": {"oid": 1, "status": "OPEN"}}),
        exchange_client=exchange,
    )

    with pytest.raises(HyperliquidOrderError) as err:
        asyncio.run(broker.place_bracket(_plan()))

    assert "somethingUnexpected" in str(err.value)
    assert "raw_response" in str(err.value)


def test_user_event_subscription_survives_pre_connect_registration():
    """B6 prereq: OrderManager subscribes BEFORE connect(); the callback must
    be retained and channels flushed at connect — and only once."""
    broker = HyperliquidBroker()  # no clients yet
    received: list[object] = []
    broker.subscribe_user_events(received.append)
    broker.subscribe_user_events(received.append)  # second callback pre-connect

    info = FakeInfo(size="0")
    exchange = _exchange_mock()
    broker.info = info
    broker.exchange = exchange
    asyncio.run(broker.connect())

    channels = [sub[0]["type"] for sub in info.subscriptions]
    assert channels.count("userEvents") == 1
    assert channels.count("orderUpdates") == 1
    # a later registration also must not duplicate channels
    broker.subscribe_user_events(received.append)
    channels = [sub[0]["type"] for sub in info.subscriptions]
    assert channels.count("userEvents") == 1


def test_real_captured_fill_payload_parses_to_typed_event():
    """B3: fixture is the REAL testnet fill payload captured during the B6
    fill smoke (docs/user_events_probe.json, 2026-07-13)."""
    broker = HyperliquidBroker(info_client=FakeInfo(size="0"), exchange_client=_exchange_mock())
    received: list[object] = []
    broker.subscribe_user_events(received.append)
    broker._oid_to_cloid[56382515366] = "0x700051b466fe62be49003f45c827bbd8"

    real_fill_message = {
        "channel": "user",
        "data": {
            "fills": [
                {
                    "coin": "BTC",
                    "px": "64110.0",
                    "sz": "0.00018",
                    "side": "B",
                    "time": 1783890260586,
                    "startPosition": "0.0",
                    "dir": "Open Long",
                    "closedPnl": "0.0",
                    "hash": "0xabc",
                    "oid": 56382515366,
                    "crossed": True,
                    "fee": "0.002",
                }
            ]
        },
    }
    broker._receive_user_message(real_fill_message)

    fills = [e for e in received if isinstance(e, FillEvent)]
    assert len(fills) == 1
    assert fills[0].cloid == "0x700051b466fe62be49003f45c827bbd8"
    assert fills[0].px == 64110.0
    assert fills[0].qty == 0.00018
    assert fills[0].fee == 0.002


def test_real_captured_order_update_payload_parses_to_typed_event():
    """B3: fixture is the REAL testnet orderUpdates payload from the B6 smoke."""
    from bridge.engine.types import OrderUpdateEvent

    broker = HyperliquidBroker(info_client=FakeInfo(size="0"), exchange_client=_exchange_mock())
    received: list[object] = []
    broker.subscribe_user_events(received.append)

    real_update_message = {
        "channel": "orderUpdates",
        "data": [
            {
                "order": {
                    "coin": "BTC",
                    "side": "A",
                    "limitPx": "62820.0",
                    "sz": "0.00018",
                    "oid": 56382516030,
                    "timestamp": 1783890261973,
                    "origSz": "0.00018",
                    "reduceOnly": True,
                    "cloid": "0x1b343338773b8dc13be656c31b0873e9",
                },
                "status": "open",
                "statusTimestamp": 1783890261975,
            }
        ],
    }
    broker._receive_user_message(real_update_message)

    updates = [e for e in received if isinstance(e, OrderUpdateEvent)]
    assert len(updates) == 1
    assert updates[0].cloid == "0x1b343338773b8dc13be656c31b0873e9"
    assert updates[0].status == "OPEN"


def test_connect_rebuilds_clients_when_owned_ws_is_dead():
    """B1 completion: live 'Expired' socket close (2026-07-13) proved a dead
    Info cannot be re-subscribed; connect() must rebuild owned clients.

    Updated for P2: _build_sdk_clients now returns a (new_info, new_exchange)
    tuple instead of mutating self.info / self.exchange directly.
    """
    broker = HyperliquidBroker()  # owns clients (none injected)
    dead_info = FakeInfo(size="0")
    dead_info.ws_manager = SimpleNamespace(is_alive=lambda: False)
    dead_info.disconnect_websocket = lambda: None
    broker.info = dead_info
    broker.exchange = _exchange_mock()
    broker._user_callbacks.append(lambda e: None)
    broker._user_channels_subscribed = True

    fresh_info = FakeInfo(size="0")
    fresh_exchange = _exchange_mock()
    rebuilds: list[bool] = []

    def fake_build():
        rebuilds.append(True)
        return fresh_info, fresh_exchange

    broker._build_sdk_clients = fake_build
    asyncio.run(broker.connect())

    assert rebuilds == [True]
    assert broker.info is fresh_info
    assert broker.exchange is fresh_exchange
    channels = [sub[0]["type"] for sub in fresh_info.subscriptions]
    assert "userEvents" in channels and "orderUpdates" in channels


def test_injected_clients_are_never_rebuilt():
    info = FakeInfo(size="0")
    info.ws_manager = SimpleNamespace(is_alive=lambda: False)  # dead, but injected
    broker = HyperliquidBroker(info_client=info, exchange_client=_exchange_mock())
    asyncio.run(broker.connect())
    assert broker.info is info  # test doubles stay untouched


def test_engine_default_notifier_is_disabled(tmp_path):
    """Telegram leak regression: engines built without an explicit notifier
    (i.e. every test) must never send real messages."""
    from bridge.broker.mock import MockBroker
    from bridge.engine.engine import BridgeEngine
    from bridge.engine.risk import RiskConfig, RiskEngine
    from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
    from bridge.store.db import Store

    store = Store(tmp_path / "notif.db")
    store.initialize()
    engine = BridgeEngine(
        run_id="notif",
        broker=MockBroker(bars=[], starting_equity=1000),
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
    )
    assert engine.notifier is not None and engine.notifier.enabled is False


# ── P2: race-fix rebuild / reconcile tests ─────────────────────────────


def test_positions_and_reconcile_use_old_client_during_blocking_rebuild(tmp_path):
    """P2: REST methods including positions() remain usable on the old Info
    client while _build_sdk_clients is blocking mid-rebuild, so the engine
    neither records RECONCILE_FAILED nor disarms."""
    from bridge.engine.engine import BridgeEngine
    from bridge.engine.risk import RiskConfig, RiskEngine
    from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
    from bridge.store.db import Store

    old_info = FakeInfo(size="0.5", with_summary=True)
    old_info.ws_manager = SimpleNamespace(is_alive=lambda: False)
    old_info.disconnect_websocket = lambda: None

    broker = HyperliquidBroker(account_address="0xabc")
    broker.info = old_info
    broker.exchange = _exchange_mock()
    broker._owns_clients = True

    build_started = threading.Event()
    build_may_finish = threading.Event()
    new_info = FakeInfo(size="0")
    new_exchange = _exchange_mock()

    def blocking_build():
        build_started.set()
        build_may_finish.wait()
        return new_info, new_exchange

    broker._build_sdk_clients = blocking_build

    store = Store(tmp_path / "blocked-rebuild.db")
    store.initialize()
    engine = BridgeEngine(
        run_id="blocked-rebuild",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
    )
    engine._set_state("ARMED")
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime(2026, 7, 13, 8, 0, tzinfo=UTC)

    async def run_test():
        connect_task = asyncio.create_task(broker.connect())
        await asyncio.to_thread(build_started.wait)
        # Mid-rebuild: old client still assigned, rebuilding flag is set
        assert broker.rebuilding is True
        assert broker.info is old_info
        positions = await broker.positions()
        assert len(positions) == 1
        assert positions[0].symbol == "BTC"
        assert await engine._run_reconcile_cycle() is True
        assert engine._app_state() == "ARMED"
        event_codes = [event["code"] for event in store.get_events()]
        assert "RECONCILE_FAILED" not in event_codes
        assert "RECONCILE_DEFERRED" not in event_codes
        # Release the builder
        build_may_finish.set()
        await connect_task
        assert broker.info is new_info
        assert broker.exchange is new_exchange
        assert broker.rebuilding is False

    asyncio.run(run_test())


def test_reconcile_during_rebuild_defers_not_disarms(tmp_path):
    """P2: when HyperliquidNotConfigured is raised during reconcile AND the
    broker is rebuilding, the cycle is deferred — no RECONCILE_FAILED event,
    no disarm, reconcile health fields preserved."""
    from bridge.engine.engine import BridgeEngine
    from bridge.engine.risk import RiskConfig, RiskEngine
    from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
    from bridge.store.db import Store

    store = Store(tmp_path / "defer.db")
    store.initialize()

    # Broker with no info → positions() raises HyperliquidNotConfigured
    broker = HyperliquidBroker(account_address="0xabc")
    broker.info = None
    broker.exchange = _exchange_mock()
    broker.rebuilding = True  # mid-rebuild

    engine = BridgeEngine(
        run_id="defer",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
    )
    # Manually set ARMED with fresh reconcile health
    engine._set_state("ARMED")
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime(2026, 7, 13, 8, 0, tzinfo=UTC)
    engine.reconcile_error = None

    result = asyncio.run(engine._run_reconcile_cycle())

    # Must return False (deferred, not failed)
    assert result is False
    # State preserved — NOT disarmed
    assert engine._app_state() == "ARMED"
    assert engine.reconcile_ready is True
    assert engine.last_reconcile_ts == datetime(2026, 7, 13, 8, 0, tzinfo=UTC)
    assert engine.reconcile_error is None
    assert engine._consecutive_reconcile_failures == 0

    # Verify RECONCILE_DEFERRED event was stored
    events = store.get_events()
    deferred = [e for e in events if e["code"] == "RECONCILE_DEFERRED"]
    assert len(deferred) == 1
    assert deferred[0]["severity"] == "WARN"
    assert deferred[0]["detail"] == "broker rebuilding"

    # Verify NO RECONCILE_FAILED event
    failed = [e for e in events if e["code"] == "RECONCILE_FAILED"]
    assert len(failed) == 0


def test_hyperliquid_not_configured_without_rebuild_counts_toward_threshold(tmp_path):
    """Only the rebuild case defers; genuine nonconfiguration consumes
    the same three-strike failure budget and then disarms."""
    from bridge.engine.engine import BridgeEngine
    from bridge.engine.risk import RiskConfig, RiskEngine
    from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
    from bridge.store.db import Store

    store = Store(tmp_path / "failclosed.db")
    store.initialize()

    broker = HyperliquidBroker(account_address="0xabc")
    broker.info = None  # will cause HyperliquidNotConfigured
    broker.exchange = _exchange_mock()
    broker.rebuilding = False  # NOT rebuilding

    engine = BridgeEngine(
        run_id="failclosed",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
    )
    engine._set_state("ARMED")
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime(2026, 7, 13, 8, 0, tzinfo=UTC)

    assert asyncio.run(engine._run_reconcile_cycle()) is False
    assert engine._app_state() == "ARMED"
    assert asyncio.run(engine._run_reconcile_cycle()) is False
    assert engine._app_state() == "ARMED"
    assert asyncio.run(engine._run_reconcile_cycle()) is False
    assert engine._app_state() == "DISARMED"
    assert engine.reconcile_ready is False
    assert engine.reconcile_error == "HyperliquidNotConfigured"

    events = store.get_events()
    failed = [e for e in events if e["code"] == "RECONCILE_FAILED"]
    assert len(failed) == 1
    tolerated = [e for e in events if e["code"] == "RECONCILE_FAILED_TOLERATED"]
    assert [e["detail"] for e in reversed(tolerated)] == [
        "consecutive=1/3; error=HyperliquidNotConfigured",
        "consecutive=2/3; error=HyperliquidNotConfigured",
    ]
    deferred = [e for e in events if e["code"] == "RECONCILE_DEFERRED"]
    assert len(deferred) == 0


def test_different_exception_during_rebuild_uses_failure_threshold(tmp_path):
    """P2: any exception other than HyperliquidNotConfigured, even while
    rebuilding, must follow the existing fail-closed path."""
    from bridge.engine.engine import BridgeEngine
    from bridge.engine.risk import RiskConfig, RiskEngine
    from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
    from bridge.store.db import Store

    store = Store(tmp_path / "other_exc.db")
    store.initialize()

    # Use a broker whose positions() raises ValueError (not HyperliquidNotConfigured)
    class _ValueErrorInfo:
        def user_state(self, address):
            raise ValueError("something else broke")

        def open_orders(self, address):
            return []

        def subscribe(self, *args, **kwargs):
            pass

    broker = HyperliquidBroker(account_address="0xabc")
    broker.info = _ValueErrorInfo()
    broker.exchange = _exchange_mock()
    broker.rebuilding = True  # rebuilding, but different exception

    engine = BridgeEngine(
        run_id="other_exc",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
    )
    engine._set_state("ARMED")
    engine.reconcile_ready = True
    engine.last_reconcile_ts = datetime(2026, 7, 13, 8, 0, tzinfo=UTC)

    for _ in range(2):
        assert asyncio.run(engine._run_reconcile_cycle()) is False
        assert engine._app_state() == "ARMED"
    result = asyncio.run(engine._run_reconcile_cycle())

    assert result is False
    # Must disarm — different exception is not deferred
    assert engine._app_state() == "DISARMED"
    assert engine.reconcile_ready is False

    events = store.get_events()
    failed = [e for e in events if e["code"] == "RECONCILE_FAILED"]
    assert len(failed) == 1
    deferred = [e for e in events if e["code"] == "RECONCILE_DEFERRED"]
    assert len(deferred) == 0


def test_rebuild_swap_integrity():
    """P2: during dead-owned-websocket rebuild, every stored candle
    subscription is registered on the new Info BEFORE it is exposed;
    userEvents/orderUpdates are each subscribed exactly once; and the
    old dead websocket is disconnected only AFTER the atomic swap."""
    old_info = FakeInfo(size="0")
    old_info.ws_manager = SimpleNamespace(is_alive=lambda: False)
    old_disconnect_after_swap: list[bool] = []

    def old_disconnect():
        old_disconnect_after_swap.append(broker.info is new_info)

    old_info.disconnect_websocket = old_disconnect

    new_info = FakeInfo(size="0")
    new_exchange = _exchange_mock()

    broker = HyperliquidBroker(account_address="0xabc")
    broker.info = old_info
    broker.exchange = _exchange_mock()
    broker._owns_clients = True
    broker._user_callbacks.append(lambda e: None)

    # Register a candle subscription before connect
    candle_received: list[object] = []

    def on_bar(bar):
        candle_received.append(bar)

    from bridge.engine.bars import BarFinalizer
    broker.subscribe_bars("ETH", "4h", on_bar)

    def tracking_build():
        return new_info, new_exchange

    broker._build_sdk_clients = tracking_build

    # Patch new_info.subscribe to capture when subscriptions happen
    original_new_subscribe = new_info.subscribe
    new_subscribe_calls: list[dict] = []

    def tracking_subscribe(subscription, callback):
        new_subscribe_calls.append({"sub": subscription, "exposed": broker.info is new_info})
        return original_new_subscribe(subscription, callback)

    new_info.subscribe = tracking_subscribe

    asyncio.run(broker.connect())

    # After connect, new_info is exposed
    assert broker.info is new_info
    assert broker.exchange is new_exchange

    # Every candle subscription must have been registered BEFORE exposure
    candle_subs = [c for c in new_subscribe_calls if c["sub"]["type"] == "candle"]
    assert len(candle_subs) >= 1  # our ETH candle sub
    assert all(not c["exposed"] for c in candle_subs), (
        "candle subscriptions must be registered BEFORE new_info is exposed"
    )

    # userEvents and orderUpdates each exactly once
    user_subs = [c for c in new_subscribe_calls if c["sub"]["type"] == "userEvents"]
    order_subs = [c for c in new_subscribe_calls if c["sub"]["type"] == "orderUpdates"]
    assert len(user_subs) == 1
    assert len(order_subs) == 1

    assert old_disconnect_after_swap == [True]


# ===========================================================================
# TS-P1-004 strict response -> outcome mapping and bounded snapshot evidence
# ===========================================================================

from bridge.engine.types import ActionOutcome, LotUnit, SymbolSnapshot  # noqa: E402

_OK_RESTING = {"status": "ok", "response": {"data": {"statuses": [{"resting": {"oid": 7}}]}}}
_OK_FILLED = {"status": "ok", "response": {"data": {"statuses": [{"filled": {"oid": 7}}]}}}
_OK_SUCCESS = {"status": "ok", "response": {"data": {"statuses": [{"success": True}]}}}


@pytest.mark.parametrize("raw", [_OK_RESTING, _OK_FILLED, _OK_SUCCESS])
def test_classify_applied_only_on_explicit_success(raw):
    outcome, _reason = HyperliquidBroker._classify_exchange_result(raw)
    assert outcome is ActionOutcome.APPLIED


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "boom",
        123,
        {},
        {"status": None},
        {"status": "weird"},
        {"status": "ok"},
        {"status": "ok", "response": "Failure"},
        {"status": "ok", "response": {"data": {}}},
        {"status": "ok", "response": {"data": {"statuses": []}}},
        {"status": "ok", "response": {"data": {"statuses": [{"mystery": 1}]}}},
        {"status": "err", "response": "internal error, please try again"},
        {"status": "ok", "response": {"data": {"statuses": [{"error": "rate limited"}]}}},
    ],
)
def test_classify_unknown_for_every_unusable_answer(raw):
    outcome, reason = HyperliquidBroker._classify_exchange_result(raw)
    assert outcome is ActionOutcome.UNKNOWN, reason


@pytest.mark.parametrize(
    "raw",
    [
        {"status": "err", "response": "Order was never placed, already canceled"},
        {"status": "err", "response": "order not found"},
        {
            "status": "ok",
            "response": {"data": {"statuses": [{"error": "Invalid order: reduce only"}]}},
        },
    ],
)
def test_classify_not_applied_only_on_authoritative_rejection(raw):
    outcome, _reason = HyperliquidBroker._classify_exchange_result(raw)
    assert outcome is ActionOutcome.NOT_APPLIED


def test_lot_unit_requires_exchange_metadata():
    broker = HyperliquidBroker(info_client=object(), exchange_client=object())
    assert broker.lot_unit("BTC") is None
    broker._size_decimals["BTC"] = 3
    assert broker.lot_unit("BTC") == LotUnit(3)
    broker._size_decimals["BTC"] = 99
    assert broker.lot_unit("BTC") is None


def test_symbol_snapshot_is_inexact_without_a_size_quantum():
    info = SimpleNamespace(
        user_state=lambda addr: {"assetPositions": []},
        open_orders=lambda addr: [],
    )
    broker = HyperliquidBroker(
        info_client=info, exchange_client=object(), account_address="0xabc"
    )
    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    assert isinstance(snapshot, SymbolSnapshot)
    assert snapshot.exact is False
    assert snapshot.evidence.reason_code == "HL_SIZE_QUANTUM_MISSING"


def test_symbol_snapshot_is_inexact_when_a_read_fails():
    def boom(addr):
        raise RuntimeError("transport down")

    broker = HyperliquidBroker(
        info_client=SimpleNamespace(user_state=boom, open_orders=lambda a: []),
        exchange_client=object(),
        account_address="0xabc",
    )
    broker._size_decimals["BTC"] = 3
    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    assert snapshot.exact is False
    assert snapshot.net_size is None
    assert snapshot.evidence.reason_code == "HL_POSITION_QUERY_FAILED"


def test_symbol_snapshot_is_exact_with_metadata_and_both_reads():
    info = SimpleNamespace(
        user_state=lambda addr: {
            "assetPositions": [{"position": {"coin": "BTC", "szi": "1.5"}}]
        },
        open_orders=lambda addr: [
            {"cloid": "0xabc", "oid": 7, "coin": "BTC", "side": "A", "sz": "1.5",
             "status": "OPEN", "orderType": "Stop Market", "triggerPx": "95.0",
             "reduceOnly": True}
        ],
    )
    broker = HyperliquidBroker(
        info_client=info, exchange_client=object(), account_address="0xabc"
    )
    broker._size_decimals["BTC"] = 3
    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    assert snapshot.exact is True
    assert snapshot.net_size == 1.5
    assert [o.role for o in snapshot.open_orders] == ["SL"]


def _sdk_recovery_open_order() -> dict:
    return {
        "coin": "BTC",
        "limitPx": "95.0",
        "oid": 7,
        "side": "A",
        "sz": "1.5",
        "timestamp": 1783890261975,
        "cloid": "0x" + "a" * 32,
        "reduceOnly": True,
        "origSz": "1.5",
        "orderType": "Stop Market",
        "triggerPx": "95.0",
    }


def _sdk_recovery_open_order_without(field: str) -> dict:
    row = _sdk_recovery_open_order()
    del row[field]
    return row


def test_sdk_open_orders_row_without_status_is_live_recovery_evidence():
    sdk_row = _sdk_recovery_open_order()
    cloid = sdk_row["cloid"]
    info = SimpleNamespace(
        user_state=lambda addr: {
            "assetPositions": [{"position": {"coin": "BTC", "szi": "1.5"}}]
        },
        open_orders=lambda addr: [sdk_row],
    )
    broker = HyperliquidBroker(
        info_client=info, exchange_client=object(), account_address="0xabc"
    )
    broker._size_decimals["BTC"] = 3

    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    result = asyncio.run(broker.query_order(cloid, "BTC"))

    assert snapshot.exact is True
    assert snapshot.net_size == 1.5
    assert len(snapshot.open_orders) == 1
    assert snapshot.open_orders[0].cloid == cloid
    assert snapshot.open_orders[0].status == "OPEN"
    assert snapshot.open_orders[0].role == "SL"
    assert snapshot.open_orders[0].reduce_only is True
    assert (result.known, result.found, result.terminal) == (True, True, False)
    assert result.raw_status == "OPEN"
    assert result.evidence.reason_code == "HL_ORDER_PRESENT"
    assert "status" not in sdk_row


@pytest.mark.parametrize(
    "raw_orders",
    [
        pytest.param({}, id="collection-is-not-a-list"),
        pytest.param([None], id="row-is-not-a-mapping"),
        pytest.param(
            [_sdk_recovery_open_order_without("cloid")], id="missing-cloid"
        ),
        pytest.param(
            [_sdk_recovery_open_order() | {"cloid": "  "}], id="empty-cloid"
        ),
        pytest.param(
            [_sdk_recovery_open_order_without("coin")], id="missing-coin"
        ),
        pytest.param(
            [_sdk_recovery_open_order() | {"side": "X"}], id="unknown-side"
        ),
        pytest.param(
            [_sdk_recovery_open_order_without("sz")], id="missing-size"
        ),
        pytest.param(
            [_sdk_recovery_open_order() | {"sz": "not-a-number"}],
            id="malformed-size",
        ),
        pytest.param(
            [_sdk_recovery_open_order() | {"sz": "nan"}], id="non-finite-size"
        ),
        pytest.param(
            [_sdk_recovery_open_order() | {"sz": "0"}], id="non-positive-size"
        ),
        pytest.param(
            [_sdk_recovery_open_order_without("reduceOnly")],
            id="missing-reduce-only",
        ),
        pytest.param(
            [_sdk_recovery_open_order() | {"reduceOnly": 1}],
            id="non-bool-reduce-only",
        ),
    ],
)
def test_malformed_recovery_open_order_evidence_fails_closed(raw_orders):
    info = SimpleNamespace(
        user_state=lambda addr: {
            "assetPositions": [{"position": {"coin": "BTC", "szi": "1.5"}}]
        },
        open_orders=lambda addr: raw_orders,
    )
    broker = HyperliquidBroker(
        info_client=info, exchange_client=object(), account_address="0xabc"
    )
    broker._size_decimals["BTC"] = 3

    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    result = asyncio.run(
        broker.query_order("0x" + "a" * 32, "BTC")
    )

    assert snapshot.exact is False
    assert snapshot.net_size is None
    assert snapshot.evidence.reason_code == "HL_ORDER_EVIDENCE_MALFORMED"
    assert result.known is False
    assert result.found is False
    assert result.terminal is False
    assert result.evidence.reason_code == "HL_ORDER_EVIDENCE_MALFORMED"


def test_symbol_snapshot_is_inexact_when_any_position_row_misses_coin():
    info = SimpleNamespace(
        user_state=lambda addr: {
            "assetPositions": [{"position": {"szi": "1.0"}}]
        },
        open_orders=lambda addr: [],
    )
    broker = HyperliquidBroker(
        info_client=info, exchange_client=object(), account_address="0xabc"
    )
    broker._size_decimals["BTC"] = 3

    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))

    assert snapshot.exact is False
    assert snapshot.net_size is None
    assert snapshot.evidence.reason_code == "HL_POSITION_EVIDENCE_MALFORMED"


def test_symbol_snapshot_is_inexact_when_stop_misses_reduce_only():
    info = SimpleNamespace(
        user_state=lambda addr: {
            "assetPositions": [{"position": {"coin": "BTC", "szi": "1.0"}}]
        },
        open_orders=lambda addr: [
            {
                "cloid": "0xabc",
                "coin": "BTC",
                "side": "A",
                "sz": "1.0",
                "status": "OPEN",
                "orderType": "Stop Market",
                "triggerPx": "95.0",
            }
        ],
    )
    broker = HyperliquidBroker(
        info_client=info, exchange_client=object(), account_address="0xabc"
    )
    broker._size_decimals["BTC"] = 3

    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))

    assert snapshot.exact is False
    assert snapshot.evidence.reason_code == "HL_ORDER_EVIDENCE_MALFORMED"


def test_symbol_snapshot_conflicting_positions_are_inexact():
    info = SimpleNamespace(
        user_state=lambda addr: {
            "assetPositions": [
                {"position": {"coin": "BTC", "szi": "1.0"}},
                {"position": {"coin": "BTC", "szi": "2.0"}},
            ]
        },
        open_orders=lambda addr: [],
    )
    broker = HyperliquidBroker(
        info_client=info, exchange_client=object(), account_address="0xabc"
    )
    broker._size_decimals["BTC"] = 3
    snapshot = asyncio.run(broker.symbol_snapshot("BTC"))
    assert snapshot.exact is False
    assert snapshot.evidence.reason_code == "HL_POSITION_CONFLICTING"


@pytest.mark.parametrize(
    ("raw", "known", "found", "terminal"),
    [
        ({"status": "unknownOid"}, False, False, False),
        (
            {"status": "order", "order": {"status": "open",
                                          "order": {"origSz": "2.0", "sz": "1.0"}}},
            True, True, False,
        ),
        ({"status": "order", "order": {"status": "canceled"}}, True, False, True),
        ({"status": "order", "order": {"status": "filled"}}, True, False, True),
        (
            {"status": "order", "order": {"status": "future_transient_status"}},
            False,
            False,
            False,
        ),
        ({"status": "order"}, False, False, False),
        ({"status": "order", "order": {}}, False, False, False),
        ({"status": "weird"}, False, False, False),
        ("garbage", False, False, False),
    ],
)
def test_parse_order_query_is_strict(raw, known, found, terminal):
    raw = deepcopy(raw)
    if isinstance(raw, dict) and raw.get("status") == "order":
        payload = raw.get("order")
        if isinstance(payload, dict) and isinstance(payload.get("status"), str):
            inner = payload.setdefault("order", {})
            if isinstance(inner, dict):
                inner.setdefault("cloid", "0xabc")
                inner.setdefault("coin", "BTC")
    result = HyperliquidBroker._parse_order_query(raw, "0xabc", "BTC")
    assert (result.known, result.found, result.terminal) == (known, found, terminal)


def test_parse_order_query_computes_filled_size():
    result = HyperliquidBroker._parse_order_query(
        {"status": "order",
         "order": {"status": "open", "order": {"cloid": "0xabc", "coin": "BTC", "origSz": "2.0", "sz": "0.5"}}},
        "0xabc", "BTC",
    )
    assert result.filled_size == 1.5


def test_kill_query_evidence_carries_exact_oid_and_terminal_fill_size():
    result = HyperliquidBroker._parse_order_query(
        {
            "status": "order",
            "order": {
                "status": "filled",
                "order": {"oid": 4242, "cloid": "0x" + "a" * 32, "coin": "BTC", "origSz": "1.25", "sz": "0"},
            },
        },
        "0x" + "a" * 32, "BTC",
    )
    assert result.known is True and result.terminal is True
    assert result.oid == 4242
    assert result.filled_size == 1.25


def test_kill_query_rejects_mismatched_returned_cloid_and_coin():
    result = HyperliquidBroker._parse_order_query(
        {
            "status": "order",
            "order": {
                "status": "filled",
                "order": {
                    "oid": 4242, "cloid": "0x" + "b" * 32,
                    "coin": "ETH", "origSz": "1.0", "sz": "0",
                },
            },
        },
        "0x" + "a" * 32,
        "BTC",
    )
    assert result.known is False
    assert result.evidence.reason_code == "HL_QUERY_IDENTITY_MISMATCH"


def test_query_order_open_order_absence_is_not_authoritative():
    broker = HyperliquidBroker(
        info_client=SimpleNamespace(open_orders=lambda addr: []),
        exchange_client=object(),
        account_address="0xabc",
    )
    result = asyncio.run(broker.query_order("0xabc", "BTC"))
    assert result.known is False
    assert result.evidence.reason_code == "HL_ORDER_ABSENCE_NOT_AUTHORITATIVE"


def test_query_order_open_order_fallback_rejects_malformed_rows():
    broker = HyperliquidBroker(
        info_client=SimpleNamespace(
            open_orders=lambda addr: [
                {
                    "cloid": "0xabc",
                    "coin": "BTC",
                    "side": "A",
                    "sz": "1.0",
                    "status": "OPEN",
                }
            ]
        ),
        exchange_client=object(),
        account_address="0xabc",
    )

    result = asyncio.run(broker.query_order("0xabc", "BTC"))

    assert result.known is False
    assert result.evidence.reason_code == "HL_ORDER_EVIDENCE_MALFORMED"


def test_typed_cancel_transport_failure_is_unknown():
    def boom(coin, cloid):
        raise TimeoutError("gateway timeout")

    broker = HyperliquidBroker(
        info_client=object(),
        exchange_client=SimpleNamespace(cancel_by_cloid=boom),
        account_address="0xabc",
    )
    result = asyncio.run(broker.cancel_order_by_cloid("0x" + "1" * 32, "BTC"))
    assert result.outcome is ActionOutcome.UNKNOWN
    assert result.evidence.reason_code == "HL_TRANSPORT_FAILED"


def test_typed_place_transport_failure_is_unknown():
    def boom(requests, grouping):
        raise TimeoutError("gateway timeout")

    broker = HyperliquidBroker(
        info_client=object(),
        exchange_client=SimpleNamespace(bulk_orders=boom),
        account_address="0xabc",
    )
    broker._size_decimals["BTC"] = 3
    result = asyncio.run(
        broker.place_protective_stop(
            symbol="BTC", cloid="0x" + "2" * 32, exit_side="SELL",
            size=1.0, trigger_px=95.0,
        )
    )
    assert result.outcome is ActionOutcome.UNKNOWN


def test_typed_flatten_transport_failure_is_unknown():
    def boom(*args, **kwargs):
        raise TimeoutError("gateway timeout")

    broker = HyperliquidBroker(
        info_client=object(),
        exchange_client=SimpleNamespace(_slippage_price=lambda *args: 100.0, order=boom),
        account_address="0xabc",
    )
    result = asyncio.run(
        broker.flatten_reduce_only(symbol="BTC", cloid="0x" + "3" * 32, size=1.0, exit_side="SELL")
    )
    assert result.outcome is ActionOutcome.UNKNOWN


def test_repair4_a5_epoch_rechecked_inside_hl_flatten_write_boundary(tmp_path):
    store = Store(tmp_path / "repair4-hl-epoch-boundary.db")
    store.initialize(target_schema_version=9)
    store.create_run("repair4-hl-boundary", "dry_run", "testnet", {})
    _request, epoch = store.open_kill_epoch(
        run_id="repair4-hl-boundary",
        symbol="BTC",
        flatten_requested=True,
        policy_version="policy-v1",
        process_uid="repair4-hl-old",
        opened_ts_monotonic=10.0,
    )
    writes: list[str] = []

    def slippage_price(*_args):
        store.open_kill_epoch(
            run_id="repair4-hl-boundary",
            symbol="BTC",
            flatten_requested=True,
            policy_version="policy-v1",
            process_uid="repair4-hl-new",
            opened_ts_monotonic=20.0,
        )
        return 100.0

    def order(*_args, **_kwargs):
        writes.append("order")
        return _OK_RESTING

    broker = HyperliquidBroker(
        info_client=object(),
        exchange_client=SimpleNamespace(
            _slippage_price=slippage_price,
            order=order,
        ),
        account_address="0xabc",
    )

    with pytest.raises(KillConflictError, match="KILL_EPOCH_STALE_WRITE"):
        asyncio.run(
            broker.kill_flatten_reduce_only(
                symbol="BTC",
                cloid="0x" + "3" * 32,
                size=1.0,
                exit_side="SELL",
                epoch=epoch,
                epoch_guard=store.assert_kill_epoch_active,
            )
        )

    assert writes == []
    assert "KILL_EPOCH_STALE_WRITE_REJECTED" in {
        str(row["code"]) for row in store.get_events()
    }


def test_kill_flatten_uses_frozen_side_even_if_wallet_position_would_flip():
    calls = []
    wallet_position = {"size": 1.25}

    def order(*args, **kwargs):
        calls.append((wallet_position["size"], args, kwargs))
        return _OK_RESTING

    def slippage_price(symbol, is_buy, slippage):
        wallet_position["size"] = -1.25
        return 99.0

    raw_cloid = "0x" + "6" * 32
    broker = HyperliquidBroker(
        info_client=object(),
        exchange_client=SimpleNamespace(
            _slippage_price=slippage_price,
            order=order,
        ),
        account_address="0xabc",
    )

    result = asyncio.run(
        broker.flatten_reduce_only(symbol="BTC", cloid=raw_cloid, size=1.25, exit_side="SELL")
    )

    assert result.outcome is ActionOutcome.APPLIED
    flipped_size, args, kwargs = calls[0]
    assert flipped_size == -1.25
    assert args == ("BTC", False, 1.25, 99.0)
    assert kwargs["order_type"] == {"limit": {"tif": "Ioc"}}
    assert kwargs["reduce_only"] is True
    assert isinstance(kwargs["cloid"], Cloid)
    assert kwargs["cloid"].to_raw() == raw_cloid


def test_typed_place_registers_spec_only_when_applied():
    calls: list[dict] = []

    def bulk_orders(requests, grouping):
        calls.append({"requests": requests, "grouping": grouping})
        return _OK_RESTING

    cloid = "0x" + "4" * 32
    broker = HyperliquidBroker(
        info_client=object(),
        exchange_client=SimpleNamespace(bulk_orders=bulk_orders),
        account_address="0xabc",
    )
    broker._size_decimals["BTC"] = 3
    result = asyncio.run(
        broker.place_protective_stop(
            symbol="BTC", cloid=cloid, exit_side="SELL", size=1.0, trigger_px=95.0
        )
    )
    assert result.outcome is ActionOutcome.APPLIED
    assert calls[0]["requests"][0]["reduce_only"] is True
    assert calls[0]["requests"][0]["is_buy"] is False
    assert broker._order_specs[cloid]["role"] == "SL"


def test_typed_surface_without_clients_is_not_applied_not_success():
    broker = HyperliquidBroker(info_client=None, exchange_client=None)
    cancel = asyncio.run(broker.cancel_order_by_cloid("0x" + "5" * 32, "BTC"))
    place = asyncio.run(
        broker.place_protective_stop(
            symbol="BTC", cloid="0x" + "5" * 32, exit_side="SELL",
            size=1.0, trigger_px=95.0,
        )
    )
    flat = asyncio.run(
        broker.flatten_reduce_only(symbol="BTC", cloid="0x" + "5" * 32, size=1.0, exit_side="SELL")
    )
    query = asyncio.run(broker.query_order("0x" + "5" * 32, "BTC"))
    assert cancel.outcome is ActionOutcome.NOT_APPLIED
    assert place.outcome is ActionOutcome.NOT_APPLIED
    assert flat.outcome is ActionOutcome.NOT_APPLIED
    assert query.known is False


def test_legacy_cancel_flatten_reprotect_signatures_are_preserved():
    import inspect

    broker = HyperliquidBroker(info_client=object(), exchange_client=object())
    assert list(inspect.signature(broker.cancel).parameters) == ["cloid"]
    assert list(inspect.signature(broker.flatten).parameters) == ["coin"]
    assert list(inspect.signature(broker.reprotect_position).parameters) == [
        "position", "stop_loss", "take_profit", "decision_uid"
    ]


# ---------------------------------------------------------------------------
# TS-P1-005 read-only full-reconciliation evidence
# ---------------------------------------------------------------------------

from bridge.engine.types import (  # noqa: E402 - grouped with the section it serves
    ReconcileComponentKind,
    ReconcileComponentStatus,
)


class ReconcileInfo:
    """Minimal Info double for the read-only reconciliation surface."""

    def __init__(
        self,
        *,
        state=None,
        orders=None,
        fill_pages=None,
        funding_pages=None,
        raise_on: str = "",
    ) -> None:
        self._state = state
        self._orders = orders if orders is not None else []
        self._fill_pages = list(fill_pages or [[]])
        self._funding_pages = list(funding_pages or [[]])
        self._raise_on = raise_on
        self.fill_calls: list[tuple[int, int]] = []
        self.funding_calls: list[tuple[int, int]] = []

    def user_state(self, address):
        if self._raise_on == "user_state":
            raise RuntimeError("boom")
        return self._state

    def open_orders(self, address):
        if self._raise_on == "open_orders":
            raise RuntimeError("boom")
        return self._orders

    def user_fills_by_time(self, address, start_time, end_time=None):
        self.fill_calls.append((start_time, end_time))
        return self._fill_pages[min(len(self.fill_calls) - 1, len(self._fill_pages) - 1)]

    def user_funding_history(self, address, start_time, end_time=None):
        self.funding_calls.append((start_time, end_time))
        return self._funding_pages[
            min(len(self.funding_calls) - 1, len(self._funding_pages) - 1)
        ]


def _reconcile_broker(info) -> HyperliquidBroker:
    broker = HyperliquidBroker(info_client=info, exchange_client=object())
    broker._size_decimals = {"BTC": 3}
    return broker


def _hl_state(*, equity="1000", margin_used="100", withdrawable="900", positions=None):
    return {
        "marginSummary": {"accountValue": equity, "totalMarginUsed": margin_used},
        "withdrawable": withdrawable,
        "assetPositions": positions if positions is not None else [],
    }


def test_portfolio_evidence_is_one_read_for_three_components():
    info = ReconcileInfo(
        state=_hl_state(
            positions=[{"position": {"coin": "BTC", "szi": "0.25"}}]
        )
    )
    broker = _reconcile_broker(info)
    portfolio = asyncio.run(broker.portfolio_evidence())

    assert portfolio.positions.rows == ({"symbol": "BTC", "size": 0.25},)
    assert portfolio.balances.rows == ({"equity": 1000.0, "withdrawable": 900.0},)
    assert portfolio.margin.rows == (
        {"margin_used": 100.0, "available_margin": 900.0},
    )
    # One REST call produces all three; balances/margin add nothing.
    assert portfolio.positions.call_count == 1
    assert portfolio.balances.call_count == 0
    assert portfolio.margin.call_count == 0
    # Identical source timestamp means zero intra-account skew by construction.
    assert portfolio.positions.observed_ts == portfolio.balances.observed_ts
    assert portfolio.margin.observed_ts == portfolio.balances.observed_ts


def test_v8_portfolio_evidence_retains_same_epoch_risk_fields():
    info = ReconcileInfo(
        state=_hl_state(
            positions=[{"position": {
                "coin": "BTC", "szi": "-0.25", "positionValue": "250",
                "liquidationPx": "1200", "leverage": {"type": "isolated", "value": 1},
            }}]
        )
    )
    broker = _reconcile_broker(info)
    broker.exposure_capture_enabled = True
    portfolio = asyncio.run(broker.portfolio_evidence())
    assert portfolio.positions.rows == ({
        "symbol": "BTC", "size": -0.25, "position_value": 250.0,
        "liquidation_px": 1200.0, "leverage": 1.0,
    },)
    assert portfolio.positions.observed_ts == portfolio.balances.observed_ts


def test_v8_missing_reported_leverage_is_malformed_not_synthesized():
    info = ReconcileInfo(
        state=_hl_state(
            positions=[{"position": {
                "coin": "BTC", "szi": "0.1", "positionValue": "100",
                "liquidationPx": "800",
            }}]
        )
    )
    broker = _reconcile_broker(info)
    broker.exposure_capture_enabled = True
    portfolio = asyncio.run(broker.portfolio_evidence())
    assert portfolio.positions.status is ReconcileComponentStatus.MALFORMED
    assert portfolio.positions.rows == ()


def test_v8_symbol_aliases_are_rejected_after_normalization():
    info = ReconcileInfo(
        state=_hl_state(
            positions=[
                {"position": {
                    "coin": "BTC", "szi": "0.1", "positionValue": "100",
                    "liquidationPx": "800",
                    "leverage": {"type": "isolated", "value": 0.5},
                }},
                {"position": {
                    "coin": " btc ", "szi": "0.1", "positionValue": "100",
                    "liquidationPx": "800",
                    "leverage": {"type": "isolated", "value": 0.5},
                }},
            ]
        )
    )
    broker = _reconcile_broker(info)
    broker.exposure_capture_enabled = True
    portfolio = asyncio.run(broker.portfolio_evidence())
    assert portfolio.positions.status is ReconcileComponentStatus.CONFLICTING


def test_portfolio_evidence_never_clamps_an_inconsistent_account():
    info = ReconcileInfo(state=_hl_state(equity="100", margin_used="500"))
    portfolio = asyncio.run(_reconcile_broker(info).portfolio_evidence())

    assert portfolio.balances.status is ReconcileComponentStatus.CONFLICTING
    assert portfolio.margin.status is ReconcileComponentStatus.CONFLICTING
    # The raw negative figure is retained, not repaired to zero.
    assert portfolio.margin.rows[0]["available_margin"] == -400.0
    assert portfolio.balances.accepted is False


def test_portfolio_evidence_fails_closed_on_transport_and_malformed_bodies():
    failed = asyncio.run(
        _reconcile_broker(ReconcileInfo(raise_on="user_state")).portfolio_evidence()
    )
    assert failed.positions.status is ReconcileComponentStatus.UNAVAILABLE
    assert failed.positions.rows == ()

    malformed = asyncio.run(
        _reconcile_broker(ReconcileInfo(state={"assetPositions": "nope"}))
        .portfolio_evidence()
    )
    assert malformed.positions.status is ReconcileComponentStatus.MALFORMED

    nan_position = asyncio.run(
        _reconcile_broker(
            ReconcileInfo(
                state=_hl_state(positions=[{"position": {"coin": "BTC", "szi": "nan"}}])
            )
        ).portfolio_evidence()
    )
    assert nan_position.positions.status is ReconcileComponentStatus.MALFORMED


def test_duplicate_position_rows_are_conflicting_not_summed():
    info = ReconcileInfo(
        state=_hl_state(
            positions=[
                {"position": {"coin": "BTC", "szi": "0.25"}},
                {"position": {"coin": "BTC", "szi": "0.50"}},
            ]
        )
    )
    portfolio = asyncio.run(_reconcile_broker(info).portfolio_evidence())
    assert portfolio.positions.status is ReconcileComponentStatus.CONFLICTING


def test_open_orders_evidence_sorts_and_fails_closed_on_bad_rows():
    info = ReconcileInfo(
        orders=[
            {"cloid": "0xb", "coin": "BTC", "side": "A", "sz": "0.1",
             "reduceOnly": True, "oid": 2},
            {"cloid": "0xa", "coin": "BTC", "side": "B", "sz": "0.1",
             "reduceOnly": False, "oid": 1},
        ]
    )
    evidence = asyncio.run(_reconcile_broker(info).open_orders_evidence())
    assert [row["cloid"] for row in evidence.rows] == ["0xa", "0xb"]
    assert evidence.accepted is True

    broken = ReconcileInfo(orders=[{"cloid": "0xa", "coin": "BTC"}])
    bad = asyncio.run(_reconcile_broker(broken).open_orders_evidence())
    assert bad.status is ReconcileComponentStatus.MALFORMED

    failed = asyncio.run(
        _reconcile_broker(ReconcileInfo(raise_on="open_orders")).open_orders_evidence()
    )
    assert failed.status is ReconcileComponentStatus.UNAVAILABLE


def _fill(hash_value: str, oid: int, time_ms: int) -> dict:
    return {
        "coin": "BTC",
        "side": "B",
        "px": "100.5",
        "sz": "0.1",
        "time": time_ms,
        "hash": hash_value,
        "oid": oid,
        "closedPnl": "0.0",
        "crossed": True,
        "dir": "Open Long",
        "startPosition": "0.0",
    }


def test_fills_evidence_identity_comes_from_documented_fields():
    info = ReconcileInfo(fill_pages=[[_fill("0xh", 7, 1_700)]])
    evidence = asyncio.run(
        _reconcile_broker(info).fills_evidence(start_ms=1_000, end_ms=2_000)
    )
    assert evidence.accepted is True
    assert evidence.rows[0]["event_id"] == "0xh:7:1700"
    assert evidence.rows[0]["effective_ts_ms"] == 1_700
    assert evidence.cursor_start_ms == 1_000
    assert evidence.cursor_end_ms == 2_000
    assert info.fill_calls == [(1_000, 2_000)]


def test_repair4_authoritative_kill_capture_binds_epoch_orders_and_fills():
    from bridge.engine import types as engine_types

    epoch_type = getattr(engine_types, "KillEvidenceEpoch", None)
    assert epoch_type is not None, "typed kill epoch is missing"
    info = ReconcileInfo(
        state=_hl_state(
            positions=[{"position": {"coin": "BTC", "szi": "0.1"}}]
        ),
        orders=[{
            "cloid": "0xowned",
            "coin": "BTC",
            "side": "A",
            "sz": "0.1",
            "reduceOnly": True,
            "oid": 8,
        }],
        fill_pages=[[_fill("0xowned-fill", 7, 1_700)]],
    )
    broker = _reconcile_broker(info)
    assert hasattr(
        broker, "capture_kill_evidence"
    ), "authoritative broker capture seam is missing"
    epoch = epoch_type(
        episode_id="kill-v1:" + "a" * 64,
        attempt_no=1,
        process_uid="repair4-hl",
        opened_ts_monotonic=10.0,
    )

    capture = asyncio.run(
        broker.capture_kill_evidence(
            epoch=epoch,
            symbol="BTC",
            start_ms=1_000,
            end_ms=2_000,
        )
    )

    assert capture.epoch == epoch
    assert capture.symbol == "BTC"
    assert capture.accepted is True
    assert capture.positions.rows == ({"symbol": "BTC", "size": 0.1},)
    assert capture.open_orders.rows[0]["oid"] == 8
    assert capture.fills.rows[0]["oid"] == 7
    assert info.fill_calls == [(1_000, 2_000)]


def test_live_and_historical_fill_use_the_same_fallback_identity_and_timestamp():
    row = {
        "coin": "BTC",
        "side": "B",
        "px": "100",
        "sz": "0.1",
        "time": 1_500,
        "hash": "0xfill",
        "oid": 7,
    }
    historical = HyperliquidBroker._parse_fill_evidence_row(row)
    broker = HyperliquidBroker(info_client=object(), exchange_client=object())
    broker._oid_to_cloid[7] = "0xowned"
    live = broker._parse_fill_event(dict(row))

    assert live is not None
    assert historical is not None
    assert live.fill_id == historical["event_id"] == "0xfill:7:1500"
    assert int(live.ts.timestamp() * 1000) == historical["effective_ts_ms"]


def test_full_open_order_evidence_rejects_missing_oid():
    info = ReconcileInfo(orders=[{
        "cloid": "0xforeign",
        "coin": "BTC",
        "side": "B",
        "sz": "0.1",
        "reduceOnly": False,
    }])
    evidence = asyncio.run(_reconcile_broker(info).open_orders_evidence())
    assert evidence.accepted is False
    assert evidence.status is ReconcileComponentStatus.MALFORMED


def test_fills_evidence_walks_pages_and_deduplicates_the_inclusive_boundary(
    monkeypatch,
):
    monkeypatch.setattr(HyperliquidBroker, "HL_FILLS_PAGE_LIMIT", 2)
    page_one = [_fill("0x1", 1, 1_100), _fill("0x2", 2, 1_200)]
    # The inclusive next-startTime replays the boundary row.
    page_two = [_fill("0x2", 2, 1_200), _fill("0x3", 3, 1_300)]
    info = ReconcileInfo(fill_pages=[page_one, page_two, []])
    evidence = asyncio.run(
        _reconcile_broker(info).fills_evidence(start_ms=1_000, end_ms=2_000)
    )

    assert evidence.accepted is True
    assert [row["event_id"] for row in evidence.rows] == [
        "0x1:1:1100", "0x2:2:1200", "0x3:3:1300",
    ]
    assert info.fill_calls[0] == (1_000, 2_000)
    assert info.fill_calls[1] == (1_200, 2_000)


def test_fills_evidence_fails_closed_when_the_cursor_stalls(monkeypatch):
    monkeypatch.setattr(HyperliquidBroker, "HL_FILLS_PAGE_LIMIT", 2)
    stalled = [_fill("0x1", 1, 1_000), _fill("0x2", 2, 1_000)]
    info = ReconcileInfo(fill_pages=[stalled])
    evidence = asyncio.run(
        _reconcile_broker(info).fills_evidence(start_ms=1_000, end_ms=2_000)
    )
    assert evidence.status is ReconcileComponentStatus.TRUNCATED
    assert evidence.reason_code == "HL_CURSOR_STALLED"
    assert evidence.accepted is False


def test_fills_evidence_fails_closed_at_the_documented_history_limit(monkeypatch):
    monkeypatch.setattr(HyperliquidBroker, "HL_FILLS_PAGE_LIMIT", 2)
    monkeypatch.setattr(HyperliquidBroker, "HL_FILLS_HISTORY_LIMIT", 2)
    info = ReconcileInfo(fill_pages=[[_fill("0x1", 1, 1_100), _fill("0x2", 2, 1_200)]])
    evidence = asyncio.run(
        _reconcile_broker(info).fills_evidence(start_ms=1_000, end_ms=2_000)
    )
    assert evidence.status is ReconcileComponentStatus.TRUNCATED
    assert evidence.reason_code == "HL_HISTORY_LIMIT_REACHED"


def test_fills_evidence_rejects_malformed_rows_and_inverted_windows():
    malformed = asyncio.run(
        _reconcile_broker(
            ReconcileInfo(fill_pages=[[{"coin": "BTC", "time": 1_100}]])
        ).fills_evidence(start_ms=1_000, end_ms=2_000)
    )
    assert malformed.status is ReconcileComponentStatus.MALFORMED

    inverted = asyncio.run(
        _reconcile_broker(ReconcileInfo()).fills_evidence(start_ms=2_000, end_ms=1_000)
    )
    assert inverted.status is ReconcileComponentStatus.STALE
    assert inverted.reason_code == "HL_WINDOW_INVERTED"


@pytest.mark.parametrize(
    "overrides",
    [
        {"side": "NOT_A_SIDE"},
        {"sz": "0"},
        {"sz": "-1"},
        {"px": "0"},
        {"px": "-100"},
        {"time": 999},
        {"time": 2_001},
    ],
)
def test_fills_evidence_rejects_invalid_semantics_and_out_of_window_rows(overrides):
    row = _fill("0xbad", 9, 1_500)
    row.update(overrides)
    evidence = asyncio.run(
        _reconcile_broker(ReconcileInfo(fill_pages=[[row]])).fills_evidence(
            start_ms=1_000, end_ms=2_000
        )
    )
    assert evidence.accepted is False
    assert evidence.status is ReconcileComponentStatus.MALFORMED


def _funding(hash_value: str, time_ms: int, usdc: str = "-1.25", **delta) -> dict:
    payload = {
        "coin": "BTC",
        "fundingRate": "0.0000125",
        "szi": "0.1",
        "type": "funding",
        "usdc": usdc,
        "nSamples": 1,
    }
    payload.update(delta)
    return {"delta": payload, "hash": hash_value, "time": time_ms}


def test_funding_evidence_uses_the_authoritative_event_hash():
    info = ReconcileInfo(funding_pages=[[_funding("0xfund", 1_400)]])
    evidence = asyncio.run(
        _reconcile_broker(info).funding_evidence(start_ms=1_000, end_ms=2_000)
    )
    row = evidence.rows[0]
    assert evidence.accepted is True
    assert row["event_id"] == "0xfund"          # authoritative hash, never synthesized
    assert row["symbol"] == "BTC"               # delta.coin
    assert row["amount_usdc"] == -1.25          # signed delta.usdc
    assert row["effective_ts_ms"] == 1_400      # record time
    assert row["funding_rate"] == 0.0000125
    assert row["n_samples"] == 1


@pytest.mark.parametrize(
    "row",
    [
        {"delta": {"coin": "BTC", "type": "funding", "usdc": "-1"}, "time": 1_400},
        {"delta": {"coin": "BTC", "type": "funding", "usdc": "-1"},
         "hash": "", "time": 1_400},
        {"delta": {"coin": "BTC", "type": "deposit", "usdc": "-1"},
         "hash": "0xf", "time": 1_400},
        {"delta": {"coin": "", "type": "funding", "usdc": "-1"},
         "hash": "0xf", "time": 1_400},
        {"delta": {"coin": "BTC", "type": "funding", "usdc": "nan"},
         "hash": "0xf", "time": 1_400},
        {"delta": {"coin": "BTC", "type": "funding", "usdc": "-1"},
         "hash": "0xf", "time": 0},
        {"delta": "not-a-mapping", "hash": "0xf", "time": 1_400},
    ],
    ids=[
        "missing-hash", "blank-hash", "wrong-delta-type", "blank-coin",
        "non-finite-usdc", "invalid-time", "malformed-delta",
    ],
)
def test_funding_evidence_fails_closed_on_unusable_records(row):
    info = ReconcileInfo(funding_pages=[[row]])
    evidence = asyncio.run(
        _reconcile_broker(info).funding_evidence(start_ms=1_000, end_ms=2_000)
    )
    assert evidence.status is ReconcileComponentStatus.MALFORMED
    assert evidence.rows == ()


def test_funding_evidence_pagination_progress_and_conflict(monkeypatch):
    monkeypatch.setattr(HyperliquidBroker, "HL_INFO_PAGE_LIMIT", 2)
    page_one = [_funding("0xf1", 1_100), _funding("0xf2", 1_200)]
    page_two = [_funding("0xf2", 1_200), _funding("0xf3", 1_300)]
    info = ReconcileInfo(funding_pages=[page_one, page_two, []])
    evidence = asyncio.run(
        _reconcile_broker(info).funding_evidence(start_ms=1_000, end_ms=2_000)
    )
    assert [row["event_id"] for row in evidence.rows] == ["0xf1", "0xf2", "0xf3"]
    assert info.funding_calls[1] == (1_200, 2_000)

    conflicting = ReconcileInfo(
        funding_pages=[[_funding("0xf1", 1_100), _funding("0xf1", 1_100, usdc="-9.0")]]
    )
    blocked = asyncio.run(
        _reconcile_broker(conflicting).funding_evidence(start_ms=1_000, end_ms=2_000)
    )
    assert blocked.status is ReconcileComponentStatus.CONFLICTING
    assert blocked.reason_code == "HL_FUNDING_IDENTITY_CONFLICT"


def test_reconciliation_reads_are_unavailable_without_an_info_client():
    broker = HyperliquidBroker(info_client=None, exchange_client=None)
    portfolio = asyncio.run(broker.portfolio_evidence())
    orders = asyncio.run(broker.open_orders_evidence())
    fills = asyncio.run(broker.fills_evidence(start_ms=0, end_ms=1))
    funding = asyncio.run(broker.funding_evidence(start_ms=0, end_ms=1))

    for component in (portfolio.positions, orders, fills, funding):
        assert component.status is ReconcileComponentStatus.UNAVAILABLE
        assert component.reason_code == "HL_NOT_CONFIGURED"
        assert component.accepted is False
    assert orders.kind is ReconcileComponentKind.OPEN_ORDERS
