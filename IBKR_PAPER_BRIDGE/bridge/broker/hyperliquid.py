"""Hyperliquid broker adapter.

Unit tests mock the SDK clients. The P0 smoke script is written separately and
must not be run without explicit approval because it places testnet orders.
"""

from __future__ import annotations

import asyncio
import os
import hashlib
import logging
from datetime import UTC, datetime

from bridge.engine.types import (
    AccountSnapshot,
    Bar,
    BrokerEvent,
    BrokerOrder,
    FillEvent,
    OrderPlan,
    OrderUpdateEvent,
    Position,
)
from bridge.engine.bars import BarFinalizer, timeframe_delta
from hyperliquid.utils.types import Cloid

LIVE_ACK = "I_UNDERSTAND_THIS_IS_REAL_MONEY"
logger = logging.getLogger(__name__)


class BrokerRefusedLive(RuntimeError):
    pass


class HyperliquidNotConfigured(RuntimeError):
    pass


class HyperliquidOrderError(RuntimeError):
    pass


class HyperliquidBroker:
    def __init__(
        self,
        network: str = "testnet",
        enable_live: bool = False,
        live_ack: str = "",
        strategy_live_allowed: bool = False,
        account_address: str | None = None,
        api_wallet_key: str | None = None,
        info_client: object | None = None,
        exchange_client: object | None = None,
        coin: str = "BTC",
        leverage: int = 1,
    ) -> None:
        self.network = network
        self.enable_live = enable_live
        self.live_ack = live_ack
        self.strategy_live_allowed = strategy_live_allowed
        self.account_address = account_address or os.environ.get("HL_ACCOUNT_ADDRESS", "")
        self.api_wallet_key = api_wallet_key or os.environ.get("HL_API_WALLET_KEY", "")
        self.info = info_client
        self.exchange = exchange_client
        self.coin = coin
        self.leverage = leverage
        self.connected = False
        self._order_specs: dict[str, dict] = {}
        self._bar_subscriptions: list[tuple[str, str, object, BarFinalizer]] = []
        self._user_callbacks: list[object] = []
        self._oid_to_cloid: dict[int, str] = {}
        self.last_bar_update: datetime | None = None

    async def connect(self) -> None:
        self._check_network_lock()
        if self.info is None or self.exchange is None:
            await asyncio.to_thread(self._build_sdk_clients)
        if hasattr(self.exchange, "update_leverage"):
            await asyncio.to_thread(self.exchange.update_leverage, self.leverage, self.coin, is_cross=False)
        self.connected = True

    async def account(self) -> AccountSnapshot:
        if self.info is None:
            raise HyperliquidNotConfigured("Info client not configured")
        if hasattr(self.info, "user_state"):
            state = await asyncio.to_thread(self.info.user_state, self.account_address)
            if not isinstance(state, dict):
                raise ValueError("Hyperliquid user_state was not an object")
            summary = state.get("marginSummary", {})
            equity = self._float(summary.get("accountValue"))
            margin_used = self._float(summary.get("totalMarginUsed"))
            withdrawable = self._float(state.get("withdrawable"))
            return AccountSnapshot(
                equity=equity,
                available_margin=max(equity - margin_used, 0.0),
                withdrawable=withdrawable,
            )
        raise HyperliquidNotConfigured("Info client has no user_state")

    async def positions(self) -> list[Position]:
        if self.info is None or not hasattr(self.info, "user_state"):
            raise HyperliquidNotConfigured("Info client not configured")
        state = await asyncio.to_thread(self.info.user_state, self.account_address)
        rows = state.get("assetPositions", []) if isinstance(state, dict) else []
        positions: list[Position] = []
        for row in rows:
            parsed = self._parse_position(row)
            if parsed is not None and parsed.size != 0:
                positions.append(parsed)
        return positions

    async def open_orders(self) -> list[BrokerOrder]:
        if self.info is None or not hasattr(self.info, "open_orders"):
            return []
        rows = await asyncio.to_thread(self.info.open_orders, self.account_address)
        return [self._parse_order(row) for row in rows if isinstance(row, dict)]

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list[Bar]:
        if self.info is None or not hasattr(self.info, "candles_snapshot"):
            return []
        end_ms = int(datetime.now(UTC).timestamp() * 1000)
        window_ms = int(timeframe_delta(tf).total_seconds() * 1000)
        start_ms = end_ms - window_ms * max(lookback * 2, 2)
        candles = (await asyncio.to_thread(self.info.candles_snapshot, coin, tf, start_ms, end_ms))[-lookback:]
        return [
            Bar(
                ts=datetime.fromtimestamp(int(c["t"]) / 1000, tz=UTC),
                open=float(c["o"]),
                high=float(c["h"]),
                low=float(c["l"]),
                close=float(c["c"]),
                volume=float(c["v"]),
            )
            for c in candles
        ]

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed) -> None:
        if self.info is None or not hasattr(self.info, "subscribe"):
            return
        subscription = {"type": "candle", "coin": coin, "interval": tf}

        def receive(message: dict) -> None:
            self.last_bar_update = datetime.now(UTC)
            finalizer.on_candle(message)

        finalizer = BarFinalizer(on_bar_closed=on_bar_closed, timeframe=tf)
        self._bar_subscriptions.append((coin, tf, receive, finalizer))
        self.info.subscribe(subscription, receive)

    def subscribe_user_events(self, on_event) -> None:
        if self.info is None or not hasattr(self.info, "subscribe"):
            return
        self._user_callbacks.append(on_event)
        self.info.subscribe(
            {"type": "userEvents", "user": self.account_address},
            self._receive_user_message,
        )
        self.info.subscribe(
            {"type": "orderUpdates", "user": self.account_address},
            self._receive_user_message,
        )

    def finalize_due(self, now: datetime | None = None) -> None:
        for _, _, _, finalizer in self._bar_subscriptions:
            finalizer.finalize_due(now)

    async def resubscribe(self) -> None:
        if self.info is None or not hasattr(self.info, "subscribe"):
            raise HyperliquidNotConfigured("Info client not configured")
        for coin, tf, receive, _ in self._bar_subscriptions:
            await asyncio.to_thread(
                self.info.subscribe,
                {"type": "candle", "coin": coin, "interval": tf},
                receive,
            )
        if self._user_callbacks:
            await asyncio.to_thread(
                self.info.subscribe,
                {"type": "userEvents", "user": self.account_address},
                self._receive_user_message,
            )
            await asyncio.to_thread(
                self.info.subscribe,
                {"type": "orderUpdates", "user": self.account_address},
                self._receive_user_message,
            )

    async def place_bracket(self, plan: OrderPlan) -> dict:
        if self.exchange is None or not hasattr(self.exchange, "order"):
            raise HyperliquidNotConfigured("Exchange client not configured")
        is_entry_buy = plan.signal.direction == "LONG"
        is_exit_buy = not is_entry_buy
        entry_cloid = self._cloid(plan, "entry")
        sl_cloid = self._cloid(plan, "sl")
        entry_px = plan.limit_price if plan.entry_type == "LMT" else plan.signal.ref_price
        entry_type = {"limit": {"tif": "Gtc" if plan.entry_type == "LMT" else "Ioc"}}
        requests = [
            self._request(plan.signal.symbol, is_entry_buy, plan.qty, entry_px, entry_type, False, entry_cloid),
            self._request(
                plan.signal.symbol,
                is_exit_buy,
                plan.qty,
                plan.stop_loss,
                {"trigger": {"triggerPx": plan.stop_loss, "isMarket": True, "tpsl": "sl"}},
                True,
                sl_cloid,
            ),
        ]
        roles: list[tuple[str, Cloid, float | None]] = [("ENTRY", entry_cloid, None), ("SL", sl_cloid, plan.stop_loss)]
        if plan.take_profit is not None:
            tp_cloid = self._cloid(plan, "tp")
            requests.append(
                self._request(
                    plan.signal.symbol,
                    is_exit_buy,
                    plan.qty,
                    plan.take_profit,
                    {"trigger": {"triggerPx": plan.take_profit, "isMarket": True, "tpsl": "tp"}},
                    True,
                    tp_cloid,
                )
            )
            roles.append(("TP", tp_cloid, plan.take_profit))

        raw = await asyncio.to_thread(self.exchange.bulk_orders, requests, grouping="positionTpsl")
        statuses = self._extract_statuses(raw)
        if len(statuses) != len(requests):
            raise HyperliquidOrderError("bulk order response did not contain every status")
        errors = [str(status.get("error")) for status in statuses if "error" in status]
        if errors:
            raise HyperliquidOrderError("; ".join(errors))
        result: dict[str, dict] = {}
        for idx, (role, cloid, trigger_px) in enumerate(roles):
            status = statuses[idx] if idx < len(statuses) else {}
            result[role.lower()] = self._order_result(role, cloid, status, plan.qty, trigger_px=trigger_px)
            result[role.lower()]["symbol"] = plan.signal.symbol
            request = requests[idx]
            self._order_specs[str(cloid)] = {
                "coin": request["coin"],
                "is_buy": request["is_buy"],
                "sz": request["sz"],
                "limit_px": request["limit_px"],
                "order_type": request["order_type"],
                "reduce_only": request["reduce_only"],
                "cloid": cloid,
                "role": role,
            }
            oid = result[role.lower()].get("oid")
            if oid is not None:
                self._oid_to_cloid[int(oid)] = str(cloid)
        return result

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        if self.exchange is None or not hasattr(self.exchange, "modify_order"):
            raise HyperliquidNotConfigured("Exchange client not configured")
        spec = self._order_specs.get(str(cloid))
        if spec is None:
            raise KeyError(f"unknown stop cloid: {cloid}")
        typed_cloid = Cloid.from_str(str(cloid))
        order_type = {"trigger": {"triggerPx": new_stop, "isMarket": True, "tpsl": "sl"}}
        try:
            await asyncio.to_thread(
                self.exchange.modify_order,
                typed_cloid,
                spec["coin"],
                spec["is_buy"],
                spec["sz"],
                new_stop,
                order_type,
                reduce_only=True,
                cloid=typed_cloid,
            )
        except Exception:
            logger.warning("stop modify failed; cancelling and replacing cloid=%s", cloid)
            await asyncio.to_thread(self.exchange.cancel_by_cloid, spec["coin"], typed_cloid)
            replacement = self._request(
                spec["coin"],
                spec["is_buy"],
                spec["sz"],
                new_stop,
                order_type,
                True,
                typed_cloid,
            )
            await asyncio.to_thread(self.exchange.bulk_orders, [replacement], grouping="positionTpsl")
        spec["limit_px"] = new_stop
        spec["order_type"] = order_type

    async def cancel(self, cloid: str) -> None:
        if self.exchange is not None and hasattr(self.exchange, "cancel_by_cloid"):
            spec = self._order_specs.get(str(cloid), {})
            coin = str(spec.get("coin", self.coin))
            await asyncio.to_thread(self.exchange.cancel_by_cloid, coin, Cloid.from_str(str(cloid)))

    async def cancel_all(self) -> None:
        for order in await self.open_orders():
            if order.cloid:
                await self.cancel(order.cloid)

    async def flatten(self, coin: str) -> None:
        if self.exchange is None or not hasattr(self.exchange, "market_close"):
            raise HyperliquidNotConfigured("Exchange client not configured")
        size = 0.0
        for position in await self.positions():
            if position.symbol != coin:
                continue
            size = position.size
            break
        if size == 0:
            return None
        await asyncio.to_thread(
            self.exchange.market_close,
            coin,
            sz=abs(size),
            slippage=0.05,
            cloid=self._raw_cloid(f"{coin}:flatten:{datetime.now(UTC).isoformat()}"),
        )
        return None

    async def reprotect_position(
        self,
        position: Position,
        stop_loss: float,
        take_profit: float | None,
        decision_uid: str,
    ) -> dict[str, dict] | None:
        if self.exchange is None or not hasattr(self.exchange, "bulk_orders"):
            return None
        is_exit_buy = position.size < 0
        requests: list[dict] = []
        for role, px, tpsl in (("SL", stop_loss, "sl"), ("TP", take_profit, "tp")):
            if px is None:
                continue
            cloid = self._raw_cloid(f"{decision_uid}:reprotect:{role.lower()}")
            request = self._request(
                position.symbol,
                is_exit_buy,
                abs(position.size),
                px,
                {"trigger": {"triggerPx": px, "isMarket": True, "tpsl": tpsl}},
                True,
                cloid,
            )
            requests.append(request)
            self._order_specs[str(cloid)] = {**request, "role": role}
        if not requests:
            return None
        raw = await asyncio.to_thread(self.exchange.bulk_orders, requests, grouping="positionTpsl")
        statuses = self._extract_statuses(raw)
        if len(statuses) != len(requests) or any("error" in status for status in statuses):
            return None
        result: dict[str, dict] = {}
        for request, status in zip(requests, statuses):
            cloid = request["cloid"]
            spec = self._order_specs[str(cloid)]
            role = spec["role"]
            row = self._order_result(role, cloid, status, request["sz"], request["limit_px"])
            row["symbol"] = position.symbol
            result[role.lower()] = row
            if row.get("oid") is not None:
                self._oid_to_cloid[int(row["oid"])] = str(cloid)
        return result

    def _check_network_lock(self) -> None:
        if self.network != "mainnet":
            return
        if not (self.enable_live and self.live_ack == LIVE_ACK and self.strategy_live_allowed):
            raise BrokerRefusedLive("mainnet requires CLI flag, HL_LIVE_ACK, and strategy live_allowed")

    def _build_sdk_clients(self) -> None:
        if not self.account_address or not self.api_wallet_key:
            raise HyperliquidNotConfigured("HL_ACCOUNT_ADDRESS and HL_API_WALLET_KEY are required")
        from eth_account import Account
        from hyperliquid.exchange import Exchange
        from hyperliquid.info import Info
        from hyperliquid.utils import constants

        base_url = constants.TESTNET_API_URL if self.network == "testnet" else constants.MAINNET_API_URL
        wallet = Account.from_key(self.api_wallet_key)
        self.info = Info(base_url, skip_ws=False)
        self.exchange = Exchange(wallet, base_url, account_address=self.account_address)

    def _cloid(self, plan: OrderPlan, role: str) -> Cloid:
        decision_uid = plan.decision_uid or f"{plan.signal.symbol}:{plan.signal.ts.isoformat()}:{plan.signal.direction}"
        raw = f"{decision_uid}:{role}"
        return self._raw_cloid(raw)

    @staticmethod
    def _raw_cloid(raw: str) -> Cloid:
        return Cloid.from_str("0x" + hashlib.blake2s(raw.encode("utf-8"), digest_size=16).hexdigest())

    @staticmethod
    def _order_result(role: str, cloid: Cloid, raw: object, qty: float, trigger_px: float | None = None) -> dict:
        result = {"cloid": str(cloid), "oid": None, "role": role, "status": "OPEN", "qty": qty}
        oid = HyperliquidBroker._extract_oid(raw)
        if oid is not None:
            result["oid"] = oid
        if trigger_px is not None:
            result["trigger_px"] = trigger_px
        return result

    @staticmethod
    def _extract_oid(raw: object) -> int | None:
        if not isinstance(raw, dict):
            return None
        status = raw
        if "response" in raw:
            statuses = raw.get("response", {}).get("data", {}).get("statuses", [])
            if not statuses:
                return None
            status = statuses[0]
        if "resting" in status:
            return status["resting"].get("oid")
        if "filled" in status:
            return status["filled"].get("oid")
        return None

    @staticmethod
    def _extract_statuses(raw: object) -> list[dict]:
        if not isinstance(raw, dict):
            return []
        statuses = raw.get("response", {}).get("data", {}).get("statuses", [])
        return [status for status in statuses if isinstance(status, dict)]

    @staticmethod
    def _request(
        coin: str,
        is_buy: bool,
        size: float,
        limit_px: float,
        order_type: dict,
        reduce_only: bool,
        cloid: Cloid,
    ) -> dict:
        return {
            "coin": coin,
            "is_buy": is_buy,
            "sz": size,
            "limit_px": limit_px,
            "order_type": order_type,
            "reduce_only": reduce_only,
            "cloid": cloid,
        }

    @staticmethod
    def _parse_position(position: object) -> Position | None:
        if not isinstance(position, dict):
            return None
        payload = position.get("position", position)
        if not isinstance(payload, dict) or "coin" not in payload:
            return None
        raw_size = payload.get("szi", payload.get("size", 0))
        leverage_raw = payload.get("leverage", 1)
        leverage = leverage_raw.get("value", 1) if isinstance(leverage_raw, dict) else leverage_raw
        liquidation = payload.get("liquidationPx")
        return Position(
            symbol=str(payload["coin"]),
            size=HyperliquidBroker._float(raw_size),
            entry_px=HyperliquidBroker._float(payload.get("entryPx")),
            unrealized=HyperliquidBroker._float(payload.get("unrealizedPnl")),
            leverage=int(HyperliquidBroker._float(leverage, 1.0)),
            liquidation_px=None if liquidation in (None, "") else HyperliquidBroker._float(liquidation),
            margin_used=HyperliquidBroker._float(payload.get("marginUsed")),
        )

    def _parse_order(self, row: dict) -> BrokerOrder:
        side_raw = str(row.get("side", "B")).upper()
        order_type = str(row.get("orderType", row.get("order_type", ""))) or None
        trigger_raw = row.get("triggerPx", row.get("trigger_px"))
        trigger_px = None if trigger_raw in (None, "", "0", 0) else HyperliquidBroker._float(trigger_raw)
        spec = self._order_specs.get(str(row.get("cloid", "")), {})
        role = str(spec.get("role", "UNKNOWN"))
        lowered = (order_type or "").lower()
        if role == "UNKNOWN" and ("stop" in lowered or "sl" in lowered):
            role = "SL"
        elif role == "UNKNOWN" and ("take" in lowered or "tp" in lowered):
            role = "TP"
        return BrokerOrder(
            cloid=str(row.get("cloid", "")),
            oid=int(row["oid"]) if row.get("oid") is not None else None,
            coin=str(row.get("coin", "")),
            side="BUY" if side_raw in {"B", "BUY"} else "SELL",
            size=self._float(row.get("sz", row.get("size"))),
            status=str(row.get("status", "OPEN")),
            role=role,
            reduce_only=bool(row.get("reduceOnly", row.get("reduce_only", role in {"SL", "TP"}))),
            trigger_px=trigger_px,
            order_type=order_type,
            order_ref=row.get("orderRef", row.get("order_ref")),
        )

    def _receive_user_message(self, message: dict) -> None:
        channel = str(message.get("channel", ""))
        data = message.get("data", message)
        if channel == "user" or "fills" in data:
            fills = data.get("fills", []) if isinstance(data, dict) else []
            for fill in fills:
                event = self._parse_fill_event(fill)
                if event is not None:
                    self._dispatch_user_event(event)
        if channel == "orderUpdates" or isinstance(data, list):
            updates = data if isinstance(data, list) else data.get("orderUpdates", [])
            for update in updates:
                event = self._parse_order_update(update)
                if event is not None:
                    self._dispatch_user_event(event)

    def _parse_fill_event(self, fill: object) -> FillEvent | None:
        if not isinstance(fill, dict):
            return None
        oid = fill.get("oid")
        cloid_value = fill.get("cloid")
        if not cloid_value and oid is not None:
            cloid_value = self._oid_to_cloid.get(int(oid))
        cloid = str(cloid_value or "")
        if not cloid:
            return None
        spec = self._order_specs.get(cloid, {})
        raw_time = fill.get("time", fill.get("timestamp"))
        ts = datetime.fromtimestamp(float(raw_time) / 1000, tz=UTC) if raw_time is not None else datetime.now(UTC)
        return FillEvent(
            fill_id=str(fill.get("tid", fill.get("hash", f"{cloid}:{raw_time}"))),
            cloid=cloid,
            coin=str(fill.get("coin", spec.get("coin", self.coin))),
            qty=self._float(fill.get("sz", fill.get("qty"))),
            px=self._float(fill.get("px")),
            ts=ts,
            fee=self._float(fill.get("fee")),
            role=spec.get("role", "UNKNOWN"),
        )

    def _parse_order_update(self, update: object) -> OrderUpdateEvent | None:
        if not isinstance(update, dict):
            return None
        order = update.get("order", update)
        if not isinstance(order, dict):
            return None
        oid = order.get("oid")
        cloid_value = order.get("cloid")
        if not cloid_value and oid is not None:
            cloid_value = self._oid_to_cloid.get(int(oid))
        cloid = str(cloid_value or "")
        if not cloid:
            return None
        raw_time = update.get("statusTimestamp", update.get("time"))
        ts = datetime.fromtimestamp(float(raw_time) / 1000, tz=UTC) if raw_time is not None else datetime.now(UTC)
        return OrderUpdateEvent(
            cloid=cloid,
            status=str(update.get("status", order.get("status", "OPEN"))).upper(),
            ts=ts,
            filled_qty=self._float(order.get("filledSz")) if order.get("filledSz") is not None else None,
            avg_fill_px=self._float(order.get("avgPx")) if order.get("avgPx") is not None else None,
        )

    def _dispatch_user_event(self, event: BrokerEvent) -> None:
        for callback in list(self._user_callbacks):
            callback(event)

    @staticmethod
    def _float(value: object, default: float = 0.0) -> float:
        if value in (None, ""):
            return default
        return float(value)
