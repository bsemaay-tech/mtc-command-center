"""Hyperliquid broker adapter.

Unit tests mock the SDK clients. The P0 smoke script is written separately and
must not be run without explicit approval because it places testnet orders.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import re
from datetime import UTC, datetime
from decimal import Decimal, ROUND_DOWN

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


def round_hl_price(price: float, size_decimals: int) -> float:
    """Round positive prices down to Hyperliquid wire constraints."""
    value = Decimal(str(price))
    if value <= 0:
        raise ValueError("Hyperliquid price must be positive")
    if not 0 <= size_decimals <= 6:
        raise ValueError("Hyperliquid size_decimals must be between 0 and 6")
    if value == value.to_integral_value():
        return float(value)

    decimal_quantum = Decimal(1).scaleb(-(6 - size_decimals))
    significant_quantum = Decimal(1).scaleb(value.adjusted() - 4)
    # High-price decimals get one guard digit so 57542.4 becomes the requested
    # conservative integer tick 57540 rather than relying on integer exemption.
    if value >= 10_000:
        significant_quantum = significant_quantum.scaleb(1)
    quantum = max(decimal_quantum, significant_quantum)
    return float(value.quantize(quantum, rounding=ROUND_DOWN))


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
        self._owns_clients = info_client is None and exchange_client is None
        self.account_mode = "standard"
        self._order_specs: dict[str, dict] = {}
        self._bar_subscriptions: list[tuple[str, str, object, BarFinalizer]] = []
        self._user_callbacks: list[object] = []
        self._user_channels_subscribed = False
        self.rebuilding = False
        self.raw_event_hook = None  # optional diagnostic tap (B3/B6 probes)
        self._oid_to_cloid: dict[int, str] = {}
        self._size_decimals: dict[str, int] = {}
        self.last_bar_update: datetime | None = None

    async def connect(self) -> None:
        self._check_network_lock()
        # Invariant: Info REST methods including user_state remain usable on
        # the old client while only websocket subscriptions are dead;
        # BarFeed owns bar staleness detection.
        # B1 completion: a dead SDK websocket cannot be revived by
        # re-subscribing on the same Info object (observed live 2026-07-13:
        # exchange closed the socket with "Expired"; every resubscribe then
        # raised WebSocketConnectionClosedException). Rebuild the clients.
        old_info = None
        swapped = False
        try:
            needs_rebuild = self.info is None or self.exchange is None
            if self._owns_clients and self.info is not None:
                manager = getattr(self.info, "ws_manager", None)
                is_alive = getattr(manager, "is_alive", None)
                if manager is not None and callable(is_alive) and not is_alive():
                    old_info = self.info
                    self.rebuilding = True
                    needs_rebuild = True
            if needs_rebuild:
                new_info, new_exchange = await asyncio.to_thread(self._build_sdk_clients)
                # Subscribe every stored candle subscription on the new Info
                # BEFORE it is exposed via self.info.
                for coin, tf, receive, _finalizer in self._bar_subscriptions:
                    await asyncio.to_thread(
                        new_info.subscribe,
                        {"type": "candle", "coin": coin, "interval": tf},
                        receive,
                    )
                # One tuple assignment exposes the replacement pair together.
                self.info, self.exchange = new_info, new_exchange
                swapped = True
                self._user_channels_subscribed = False
            await self._detect_account_mode()
            await self._load_size_decimals()
            if hasattr(self.exchange, "update_leverage"):
                await asyncio.to_thread(self.exchange.update_leverage, self.leverage, self.coin, is_cross=False)
            if self._user_callbacks:
                self._subscribe_user_channels()
            self.connected = True
        finally:
            self.rebuilding = False
            # Best-effort disconnect of the old dead websocket only AFTER
            # the swap so there is never a window with no live Info.
            if swapped and old_info is not None:
                try:
                    await asyncio.to_thread(getattr(old_info, "disconnect_websocket", lambda: None))
                except Exception:  # noqa: BLE001 - old socket is already dead
                    pass

    async def disconnect(self) -> None:
        try:
            if self.info is not None and hasattr(self.info, "disconnect_websocket"):
                await asyncio.to_thread(self.info.disconnect_websocket)
        except RuntimeError as exc:
            logger.debug("Hyperliquid websocket disconnect skipped: %s", exc)
        finally:
            self.connected = False

    async def account(self) -> AccountSnapshot:
        if self.info is None:
            raise HyperliquidNotConfigured("Info client not configured")
        if self.account_mode == "unifiedAccount" and hasattr(self.info, "spot_user_state"):
            state = await asyncio.to_thread(self.info.spot_user_state, self.account_address)
            if not isinstance(state, dict):
                raise ValueError("Hyperliquid spot_user_state was not an object")
            balances = state.get("balances", [])
            usdc = next(
                (row for row in balances if isinstance(row, dict) and row.get("coin") == "USDC"),
                {},
            )
            equity = self._float(usdc.get("total"))
            held = self._float(usdc.get("hold"))
            available = max(equity - held, 0.0)
            return AccountSnapshot(
                equity=equity,
                available_margin=available,
                withdrawable=available,
            )
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
        """Register a typed-event callback; safe to call BEFORE connect().

        OrderManager subscribes at construction time, before the SDK clients
        exist. The callback is always retained; the actual channel
        subscription is flushed on connect()/resubscribe(). Channels are
        subscribed at most once regardless of callback count.
        """
        self._user_callbacks.append(on_event)
        if self.info is None or not hasattr(self.info, "subscribe"):
            return  # deferred — connect() flushes
        self._subscribe_user_channels()

    def _subscribe_user_channels(self) -> None:
        if self._user_channels_subscribed or self.info is None or not hasattr(self.info, "subscribe"):
            return
        self.info.subscribe(
            {"type": "userEvents", "user": self.account_address},
            self._receive_user_message,
        )
        self.info.subscribe(
            {"type": "orderUpdates", "user": self.account_address},
            self._receive_user_message,
        )
        self._user_channels_subscribed = True

    def finalize_due(self, now: datetime | None = None) -> None:
        for _, _, _, finalizer in self._bar_subscriptions:
            finalizer.finalize_due(now)

    def ws_alive(self) -> bool:
        """B1: report SDK websocket health for the BarFeed watchdog.

        The SDK's WebsocketManager is a Thread subclass; a dead thread means
        the socket dropped and every subscription with it. No manager (mock
        clients / skip_ws) means there is nothing to monitor — report alive.
        """
        if self.info is None:
            return False
        manager = getattr(self.info, "ws_manager", None)
        if manager is None:
            return True
        is_alive = getattr(manager, "is_alive", None)
        if callable(is_alive):
            try:
                return bool(is_alive())
            except Exception:  # noqa: BLE001 - health probe must never raise
                return False
        return True

    async def resubscribe(self) -> None:
        """Idempotent: connect() already re-registers everything when it
        rebuilds dead clients; the SDK raises NotImplementedError on
        duplicate userEvents/orderUpdates subscriptions (live incident
        2026-07-13 08:04-08:17Z: every reconnect retry died on this).
        Candle re-subscription is also skipped when the ws is alive —
        subscriptions only vanish when the socket (and thus Info) is
        replaced, which connect() now handles."""
        if self.info is None or not hasattr(self.info, "subscribe"):
            raise HyperliquidNotConfigured("Info client not configured")
        if self._user_callbacks and not self._user_channels_subscribed:
            await asyncio.to_thread(self._subscribe_user_channels)

    async def place_bracket(self, plan: OrderPlan, grouping: str = "normalTpsl") -> dict:
        """Place entry + SL + optional TP as a bulk group.

        Default ``grouping="normalTpsl"`` sends entry and trigger orders in a
        normal-TPSL group. Callers may pass ``grouping="na"`` to place each
        order independently, while retaining the SDK-required trigger ``tpsl``
        discriminator; this is the bounded smoke fallback when the exchange
        rejects a TPSL grouping type.

        ``reprotect_position`` continues to use ``positionTpsl`` because it
        protects an already-open position.
        """
        if self.exchange is None or not hasattr(self.exchange, "order"):
            raise HyperliquidNotConfigured("Exchange client not configured")
        is_entry_buy = plan.signal.direction == "LONG"
        is_exit_buy = not is_entry_buy
        entry_cloid = self._cloid(plan, "entry")
        sl_cloid = self._cloid(plan, "sl")
        entry_px = self._round_price(
            plan.signal.symbol,
            plan.limit_price if plan.entry_type == "LMT" else plan.signal.ref_price,
        )
        stop_px = self._round_price(plan.signal.symbol, plan.stop_loss)
        entry_type = {"limit": {"tif": "Gtc" if plan.entry_type == "LMT" else "Ioc"}}

        # The installed SDK's TriggerOrderType requires ``tpsl`` regardless
        # of grouping. With ``na`` it remains an independently submitted
        # trigger, rather than a normal-TPSL-linked child.
        sl_trigger = {"triggerPx": stop_px, "isMarket": True, "tpsl": "sl"}

        requests = [
            self._request(plan.signal.symbol, is_entry_buy, plan.qty, entry_px, entry_type, False, entry_cloid),
            self._request(
                plan.signal.symbol,
                is_exit_buy,
                plan.qty,
                stop_px,
                {"trigger": sl_trigger},
                True,
                sl_cloid,
            ),
        ]
        roles: list[tuple[str, Cloid, float | None]] = [("ENTRY", entry_cloid, None), ("SL", sl_cloid, stop_px)]
        if plan.take_profit is not None:
            tp_cloid = self._cloid(plan, "tp")
            take_profit_px = self._round_price(plan.signal.symbol, plan.take_profit)
            tp_trigger = {"triggerPx": take_profit_px, "isMarket": True, "tpsl": "tp"}
            requests.append(
                self._request(
                    plan.signal.symbol,
                    is_exit_buy,
                    plan.qty,
                    take_profit_px,
                    {"trigger": tp_trigger},
                    True,
                    tp_cloid,
                )
            )
            roles.append(("TP", tp_cloid, take_profit_px))

        raw = await asyncio.to_thread(self.exchange.bulk_orders, requests, grouping=grouping)
        return await self._verify_positioned_orders(
            raw, roles, requests, plan.qty, plan.signal.symbol
        )

    async def _verify_positioned_orders(
        self,
        raw: object,
        roles: list[tuple[str, Cloid, float | None]],
        requests: list[dict],
        qty: float,
        symbol: str,
    ) -> dict[str, dict]:
        """Verify bulk-placed orders via open_orders; authoritative verification.

        Every submitted cloid (including SL/TP triggers) MUST be visible in
        open_orders OR specifically confirmed filled by exchange status/position
        evidence.  Status cardinality is a hint only — never sufficient to claim
        resting.  Any unverified cloid raises HyperliquidOrderError with the full
        redacted raw response.
        """
        statuses = self._extract_statuses(raw)
        # Map statuses to roles by positional index; statuses may be fewer than
        # the number of requests in positionTpsl groups.
        role_to_status: dict[str, dict] = {}
        for idx, (role, _cloid, _tp) in enumerate(roles):
            if idx < len(statuses):
                role_to_status[role] = statuses[idx]
            else:
                # No individual status for this role — must be verified below
                role_to_status[role] = {}

        errors = [str(s.get("error")) for s in statuses if "error" in s]

        # Ground-truth query: every order we own that is live on the exchange
        open_orders = await self.open_orders()
        open_by_cloid: dict[str, BrokerOrder] = {o.cloid: o for o in open_orders if o.cloid}

        result: dict[str, dict] = {}
        for role, cloid, trigger_px in roles:
            cloid_str = str(cloid)
            status = role_to_status.get(role, {})

            if cloid_str in open_by_cloid:
                # Visible in open_orders — authoritative ground truth
                order = open_by_cloid[cloid_str]
                row = {
                    "cloid": cloid_str,
                    "oid": order.oid,
                    "role": role,
                    "status": order.status,
                    "qty": qty,
                    "symbol": symbol,
                }
                if trigger_px is not None:
                    row["trigger_px"] = trigger_px
                result[role.lower()] = row
            elif "filled" in status:
                # Filled status explains why the order is not in open_orders
                result[role.lower()] = self._order_result(role, cloid, status, qty, trigger_px=trigger_px)
                result[role.lower()]["symbol"] = symbol
            elif "pending_child" in status:
                # normalTpsl child trigger waiting for its parent to fill — not in
                # open_orders yet by design; the exchange cancels it automatically
                # if the parent is cancelled. Verified as a pending state.
                row = {
                    "cloid": cloid_str,
                    "oid": None,
                    "role": role,
                    "status": "WAITING_CHILD",
                    "qty": qty,
                    "symbol": symbol,
                    "pending_reason": status["pending_child"],
                }
                if trigger_px is not None:
                    row["trigger_px"] = trigger_px
                result[role.lower()] = row
            else:
                # Every cloid must be verified — no special exemptions for triggers
                raise HyperliquidOrderError(
                    f"cloid {cloid_str} ({role}) missing from open_orders and not explained; "
                    f"raw_response={self._raw_response_safe(raw)}"
                )

        # Update order_specs and oid_to_cloid from every row
        for idx, (role, cloid, _tp) in enumerate(roles):
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
            row = result.get(role.lower())
            if row and row.get("oid") is not None:
                self._oid_to_cloid[int(row["oid"])] = str(cloid)

        if errors:
            raise HyperliquidOrderError("; ".join(errors))

        return result

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        if self.exchange is None or not hasattr(self.exchange, "modify_order"):
            raise HyperliquidNotConfigured("Exchange client not configured")
        spec = self._order_specs.get(str(cloid))
        if spec is None:
            raise KeyError(f"unknown stop cloid: {cloid}")
        typed_cloid = Cloid.from_str(str(cloid))
        rounded_stop = self._round_price(spec["coin"], new_stop)
        order_type = {"trigger": {"triggerPx": rounded_stop, "isMarket": True, "tpsl": "sl"}}
        try:
            await asyncio.to_thread(
                self.exchange.modify_order,
                typed_cloid,
                spec["coin"],
                spec["is_buy"],
                spec["sz"],
                rounded_stop,
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
                rounded_stop,
                order_type,
                True,
                typed_cloid,
            )
            await asyncio.to_thread(self.exchange.bulk_orders, [replacement], grouping="positionTpsl")
        spec["limit_px"] = rounded_stop
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
        roles: list[tuple[str, Cloid, float | None]] = []
        for role, px, tpsl in (("SL", stop_loss, "sl"), ("TP", take_profit, "tp")):
            if px is None:
                continue
            rounded_px = self._round_price(position.symbol, px)
            cloid = self._raw_cloid(f"{decision_uid}:reprotect:{role.lower()}")
            request = self._request(
                position.symbol,
                is_exit_buy,
                abs(position.size),
                rounded_px,
                {"trigger": {"triggerPx": rounded_px, "isMarket": True, "tpsl": tpsl}},
                True,
                cloid,
            )
            requests.append(request)
            roles.append((role, cloid, rounded_px))
            self._order_specs[str(cloid)] = {**request, "role": role}
        if not requests:
            return None
        raw = await asyncio.to_thread(self.exchange.bulk_orders, requests, grouping="positionTpsl")
        return await self._verify_positioned_orders(
            raw, roles, requests, abs(position.size), position.symbol
        )

    def _check_network_lock(self) -> None:
        if self.network != "mainnet":
            return
        if not (self.enable_live and self.live_ack == LIVE_ACK and self.strategy_live_allowed):
            raise BrokerRefusedLive("mainnet requires CLI flag, HL_LIVE_ACK, and strategy live_allowed")

    def _build_sdk_clients(self) -> tuple[object, object]:
        if not self.account_address or not self.api_wallet_key:
            raise HyperliquidNotConfigured("HL_ACCOUNT_ADDRESS and HL_API_WALLET_KEY are required")
        from eth_account import Account
        from hyperliquid.exchange import Exchange
        from hyperliquid.info import Info
        from hyperliquid.utils import constants

        base_url = constants.TESTNET_API_URL if self.network == "testnet" else constants.MAINNET_API_URL
        wallet = Account.from_key(self.api_wallet_key)
        new_info = Info(base_url, skip_ws=False)
        new_exchange = Exchange(wallet, base_url, account_address=self.account_address)
        return new_info, new_exchange

    async def _detect_account_mode(self) -> None:
        if self.info is None or not hasattr(self.info, "query_user_abstraction_state"):
            self.account_mode = "standard"
            return
        raw_mode = await asyncio.to_thread(self.info.query_user_abstraction_state, self.account_address)
        if isinstance(raw_mode, str):
            self.account_mode = raw_mode
        elif isinstance(raw_mode, dict):
            self.account_mode = str(raw_mode.get("mode", raw_mode.get("abstraction", "standard")))
        else:
            self.account_mode = "standard"

    async def _load_size_decimals(self) -> None:
        if self.info is None or not hasattr(self.info, "meta"):
            return
        meta = await asyncio.to_thread(self.info.meta)
        universe = meta.get("universe", []) if isinstance(meta, dict) else []
        for row in universe:
            if isinstance(row, dict) and "name" in row and "szDecimals" in row:
                self._size_decimals[str(row["name"])] = int(row["szDecimals"])

    def _round_price(self, coin: str, price: float) -> float:
        return round_hl_price(price, self._size_decimals.get(coin, 5))

    def _cloid(self, plan: OrderPlan, role: str) -> Cloid:
        decision_uid = plan.decision_uid or f"{plan.signal.symbol}:{plan.signal.ts.isoformat()}:{plan.signal.direction}"
        raw = f"{decision_uid}:{role}"
        return self._raw_cloid(raw)

    @staticmethod
    def _raw_cloid(raw: str) -> Cloid:
        return Cloid.from_str("0x" + hashlib.blake2s(raw.encode("utf-8"), digest_size=16).hexdigest())

    @staticmethod
    def compute_cloids(decision_uid: str, roles: tuple[str, ...] = ("entry", "sl", "tp")) -> dict[str, str]:
        """Precompute deterministic cloids for a decision_uid (used by smoke cleanup)."""
        result: dict[str, str] = {}
        for role in roles:
            raw = f"{decision_uid}:{role}"
            result[role] = str(HyperliquidBroker._raw_cloid(raw))
        return result

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
            raise HyperliquidOrderError(
                f"Hyperliquid exchange response was not an object; "
                f"raw_response={HyperliquidBroker._raw_response_safe(raw)}"
            )
        response = raw.get("response")
        if isinstance(response, str):
            raise HyperliquidOrderError(
                f"{HyperliquidBroker._safe_exchange_message(response)}; "
                f"raw_response={HyperliquidBroker._raw_response_safe(raw)}"
            )
        if not isinstance(response, dict):
            raise HyperliquidOrderError(
                f"Hyperliquid exchange response payload was not an object; "
                f"raw_response={HyperliquidBroker._raw_response_safe(raw)}"
            )
        data = response.get("data")
        if isinstance(data, str):
            raise HyperliquidOrderError(
                f"{HyperliquidBroker._safe_exchange_message(data)}; "
                f"raw_response={HyperliquidBroker._raw_response_safe(raw)}"
            )
        if not isinstance(data, dict):
            raise HyperliquidOrderError(
                f"Hyperliquid exchange response data was not an object; "
                f"raw_response={HyperliquidBroker._raw_response_safe(raw)}"
            )
        statuses = data.get("statuses")
        if not isinstance(statuses, list):
            raise HyperliquidOrderError(
                f"Hyperliquid exchange response did not contain statuses; "
                f"raw_response={HyperliquidBroker._raw_response_safe(raw)}"
            )
        normalized: list[dict] = []
        for status in statuses:
            if isinstance(status, dict):
                normalized.append(status)
                continue
            # Real testnet (attempt 6): normalTpsl child triggers return the plain
            # string "waitingForFill" until the parent order fills. Treat known
            # pending-child strings as a first-class pending state; anything else
            # is still an error carrying the full redacted raw response.
            if isinstance(status, str) and status in {"waitingForFill", "waitingForTrigger"}:
                normalized.append({"pending_child": status})
                continue
            raise HyperliquidOrderError(
                f"{HyperliquidBroker._safe_exchange_message(str(status))}; "
                f"raw_response={HyperliquidBroker._raw_response_safe(raw)}"
            )
        return normalized

    @staticmethod
    def _safe_exchange_message(value: object, cap: int = 4000) -> str:
        message = str(value).strip() or "Hyperliquid exchange rejected the request"
        return re.sub(r"(?i)(?:0x)?[0-9a-f]{64,}", "[redacted]", message)[:cap]

    @staticmethod
    def _raw_response_safe(raw: object, cap: int = 4000) -> str:
        """Redact and cap a full exchange response for diagnostic logging."""
        import json as _json_mod
        try:
            serialized = _json_mod.dumps(raw, default=str)
        except Exception:
            serialized = str(raw)
        return HyperliquidBroker._safe_exchange_message(serialized, cap=cap)

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
        if self.raw_event_hook is not None:
            try:
                self.raw_event_hook(message)
            except Exception:  # noqa: BLE001 - diagnostics never break the path
                pass
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

    # ------------------------------------------------------------------
    # TS-P1-003 read-only recovery evidence (never mutates orders)
    # ------------------------------------------------------------------

    async def query_order_by_cloid(self, cloid: str) -> dict | None:
        """Read-only cloid lookup via SDK query_order_by_cloid.

        Normalizes and sanitizes the result; never persists raw exchange text.
        Returns None if the order is not found or the client is unavailable.
        """
        if self.info is None or not hasattr(self.info, "query_order_by_cloid"):
            return None
        try:
            raw = await asyncio.to_thread(
                self.info.query_order_by_cloid, self.account_address, Cloid.from_str(cloid)
            )
        except Exception:
            return None
        if raw is None:
            return None
        if not isinstance(raw, dict):
            return None
        order = raw.get("order", raw)
        if not isinstance(order, dict):
            return None
        return {
            "cloid": cloid,
            "oid": order.get("oid"),
            "status": str(order.get("status", "")).upper() or None,
            "coin": str(order.get("coin", self.coin)),
            "size": self._float(order.get("sz", order.get("size"))),
        }

    async def historical_orders(
        self, coin: str, lookback_hours: float = 24.0
    ) -> list[dict]:
        """Read-only recent order history via SDK historical_orders.

        Normalizes every returned row; never persists raw exchange text.
        Returns empty list when the client is unavailable or the call fails.
        """
        if self.info is None or not hasattr(self.info, "historical_orders"):
            return []
        try:
            raw = await asyncio.to_thread(
                self.info.historical_orders, self.account_address
            )
        except Exception:
            return []
        if not isinstance(raw, list):
            return []
        result: list[dict] = []
        for row in raw:
            if not isinstance(row, dict):
                continue
            result.append({
                "cloid": str(row.get("cloid", "")),
                "oid": row.get("oid"),
                "status": str(row.get("status", "")).upper() or None,
                "coin": str(row.get("coin", coin)),
                "size": self._float(row.get("sz", row.get("size"))),
            })
        return result

    async def user_fills(
        self, coin: str, lookback_hours: float = 24.0
    ) -> list[dict]:
        """Read-only recent fill history via SDK user_fills_by_time / user_fills.

        Normalizes every returned row; never persists raw exchange text.
        Returns empty list when the client is unavailable or the call fails.
        """
        if self.info is None:
            return []
        now_ms = int(datetime.now(UTC).timestamp() * 1000)
        start_ms = now_ms - int(lookback_hours * 3600 * 1000)
        try:
            if hasattr(self.info, "user_fills_by_time"):
                raw = await asyncio.to_thread(
                    self.info.user_fills_by_time, self.account_address, start_ms, now_ms
                )
            elif hasattr(self.info, "user_fills"):
                raw = await asyncio.to_thread(
                    self.info.user_fills, self.account_address
                )
            else:
                return []
        except Exception:
            return []
        if not isinstance(raw, list):
            return []
        result: list[dict] = []
        for row in raw:
            if not isinstance(row, dict):
                continue
            cloid = str(row.get("cloid", ""))
            raw_time = row.get("time", row.get("timestamp"))
            ts = datetime.fromtimestamp(float(raw_time) / 1000, tz=UTC).isoformat() if raw_time is not None else None
            result.append({
                "fill_id": str(row.get("tid", row.get("hash", ""))),
                "cloid": cloid,
                "coin": str(row.get("coin", coin)),
                "qty": self._float(row.get("sz", row.get("qty"))),
                "px": self._float(row.get("px")),
                "ts": ts,
            })
        return result

    def _dispatch_user_event(self, event: BrokerEvent) -> None:
        for callback in list(self._user_callbacks):
            callback(event)

    @staticmethod
    def _float(value: object, default: float = 0.0) -> float:
        if value in (None, ""):
            return default
        return float(value)
