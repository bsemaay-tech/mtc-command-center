"""Hyperliquid broker adapter.

Unit tests mock the SDK clients. The P0 smoke script is written separately and
must not be run without explicit approval because it places testnet orders.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import math
import os
import re
from datetime import UTC, datetime
from decimal import Decimal, ROUND_DOWN

from bridge.broker.base import (
    BrokerOutcomeUnknown,
    BrokerPreSendFailure,
    EvidenceStatus,
    RecoveryQueryEvidence,
    SubmissionDisposition,
    SubmissionOutcome,
    SubmissionRecoveryEvidence,
    SubmissionRecoveryRequest,
)
from bridge.engine.types import (
    AccountSnapshot,
    ActionOutcome,
    Bar,
    BrokerEvent,
    BrokerOrder,
    CancelResult,
    Evidence,
    FillEvent,
    FlattenResult,
    LotQuantizationError,
    LotUnit,
    OrderPlan,
    OrderQueryResult,
    OrderUpdateEvent,
    OrderView,
    PlaceResult,
    Position,
    SymbolSnapshot,
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


class BrokerRefusedLive(BrokerPreSendFailure):
    def __init__(self, message: str) -> None:
        self.reason_code = "HL_LIVE_LOCK_REFUSED"
        self.disposition = SubmissionDisposition.DEFINITIVE_REJECTION
        self.write_may_have_started = False
        RuntimeError.__init__(self, message)


class HyperliquidNotConfigured(BrokerPreSendFailure):
    def __init__(self, message: str) -> None:
        self.reason_code = "HL_NOT_CONFIGURED"
        self.disposition = SubmissionDisposition.DEFINITIVE_REJECTION
        self.write_may_have_started = False
        RuntimeError.__init__(self, message)


class HyperliquidOrderError(BrokerOutcomeUnknown):
    def __init__(self, message: str, reason_code: str = "HL_OUTCOME_UNKNOWN") -> None:
        self.reason_code = reason_code
        self.disposition = SubmissionDisposition.OUTCOME_UNKNOWN
        self.write_may_have_started = True
        RuntimeError.__init__(self, message)


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

    def planned_cloids(self, plan: OrderPlan) -> dict[str, str]:
        decision_uid = plan.decision_uid or (
            f"{plan.signal.symbol}:{plan.signal.ts.isoformat()}:{plan.signal.direction}"
        )
        roles = ("entry", "sl", "tp") if plan.take_profit is not None else ("entry", "sl")
        return {
            role.upper(): cloid
            for role, cloid in self.compute_cloids(decision_uid, roles).items()
        }

    async def place_bracket(
        self, plan: OrderPlan, grouping: str = "normalTpsl"
    ) -> SubmissionOutcome:
        """Place entry + SL + optional TP as a bulk group.

        Default ``grouping="normalTpsl"`` sends entry and trigger orders in a
        normal-TPSL group. Callers may pass ``grouping="na"`` to place each
        order independently, while retaining the SDK-required trigger ``tpsl``
        discriminator; this is the bounded smoke fallback when the exchange
        rejects a TPSL grouping type.

        ``reprotect_position`` continues to use ``positionTpsl`` because it
        protects an already-open position.
        """
        if self.exchange is None or not hasattr(self.exchange, "bulk_orders"):
            raise HyperliquidNotConfigured("Exchange client not configured")
        try:
            planned = self.planned_cloids(plan)
            is_entry_buy = plan.signal.direction == "LONG"
            is_exit_buy = not is_entry_buy
            entry_cloid = Cloid.from_str(planned["ENTRY"])
            sl_cloid = Cloid.from_str(planned["SL"])
            entry_px = self._round_price(
                plan.signal.symbol,
                plan.limit_price if plan.entry_type == "LMT" else plan.signal.ref_price,
            )
            stop_px = self._round_price(plan.signal.symbol, plan.stop_loss)
            entry_type = {"limit": {"tif": "Gtc" if plan.entry_type == "LMT" else "Ioc"}}
            # TriggerOrderType requires ``tpsl`` even with grouping="na".
            sl_trigger = {"triggerPx": stop_px, "isMarket": True, "tpsl": "sl"}
            requests = [
                self._request(
                    plan.signal.symbol,
                    is_entry_buy,
                    plan.qty,
                    entry_px,
                    entry_type,
                    False,
                    entry_cloid,
                ),
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
            roles: list[tuple[str, Cloid, float | None]] = [
                ("ENTRY", entry_cloid, None),
                ("SL", sl_cloid, stop_px),
            ]
            if plan.take_profit is not None:
                tp_cloid = Cloid.from_str(planned["TP"])
                take_profit_px = self._round_price(
                    plan.signal.symbol, plan.take_profit
                )
                tp_trigger = {
                    "triggerPx": take_profit_px,
                    "isMarket": True,
                    "tpsl": "tp",
                }
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
        except Exception as exc:
            raise BrokerPreSendFailure("HL_REQUEST_BUILD_FAILED") from exc

        try:
            raw = await asyncio.to_thread(
                self.exchange.bulk_orders, requests, grouping=grouping
            )
        except HyperliquidOrderError:
            raise
        except Exception as exc:
            raise HyperliquidOrderError(
                "Hyperliquid write outcome unknown", "HL_BULK_WRITE_EXCEPTION"
            ) from exc
        try:
            return await self._verify_positioned_orders(
                raw, roles, requests, plan.qty, plan.signal.symbol
            )
        except HyperliquidOrderError:
            raise
        except Exception as exc:
            raise HyperliquidOrderError(
                "Hyperliquid post-write verification failed",
                "HL_POST_SEND_VERIFICATION_FAILED",
            ) from exc

    async def _verify_positioned_orders(
        self,
        raw: object,
        roles: list[tuple[str, Cloid, float | None]],
        requests: list[dict],
        qty: float,
        symbol: str,
    ) -> SubmissionOutcome:
        """Verify bulk-placed orders via open_orders; authoritative verification.

        Every submitted cloid (including SL/TP triggers) MUST be visible in
        open_orders OR specifically confirmed filled by exchange status/position
        evidence.  Status cardinality is a hint only — never sufficient to claim
        resting.  Any unverified cloid raises HyperliquidOrderError with the full
        redacted raw response.
        """
        statuses = self._extract_statuses(raw)
        if len(statuses) > len(roles):
            raise HyperliquidOrderError(
                "cloid result missing from open_orders or result cardinality mismatched",
                "HL_RESULT_CARDINALITY_MISMATCH",
            )
        role_to_status: dict[str, dict] = {}
        for idx, (role, _cloid, _tp) in enumerate(roles):
            role_to_status[role] = statuses[idx] if idx < len(statuses) else {}

        errors = [str(s.get("error")) for s in statuses if "error" in s]
        conclusive_rejections = (
            len(statuses) == len(roles)
            and all(
                "error" in status
                and not any(
                    key in status for key in ("resting", "filled", "pending_child")
                )
                for status in statuses
            )
        )
        if conclusive_rejections:
            return SubmissionOutcome(
                SubmissionDisposition.DEFINITIVE_REJECTION,
                {},
                "HL_ALL_ORDERS_REJECTED",
            )
        if errors:
            raise HyperliquidOrderError(
                "; ".join(self._safe_exchange_message(error) for error in errors),
                "HL_MIXED_BULK_RESULT",
            )
        for status in statuses:
            compatible = sum(
                key in status for key in ("resting", "filled", "pending_child")
            )
            if compatible != 1:
                raise HyperliquidOrderError(
                    "Hyperliquid status was malformed",
                    "HL_STATUS_MALFORMED",
                )

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

        return SubmissionOutcome(
            (
                SubmissionDisposition.VERIFIED_SUCCESS
                if len(statuses) == len(roles)
                else SubmissionDisposition.OUTCOME_UNKNOWN
            ),
            result,
            (
                "HL_VERIFIED_SUCCESS"
                if len(statuses) == len(roles)
                else "HL_RESULT_CARDINALITY_MISMATCH"
            ),
        )

    async def submission_recovery_evidence(
        self, request: SubmissionRecoveryRequest
    ) -> SubmissionRecoveryEvidence:
        """Collect conservative, request-specific evidence without write calls."""
        planned = set(map(str, request.planned_cloids.values()))
        direct: dict[str, RecoveryQueryEvidence] = {}
        lookup = (
            getattr(self.info, "query_order_by_cloid", None)
            if self.info is not None
            else None
        )
        for cloid in sorted(planned):
            if not callable(lookup):
                direct[cloid] = RecoveryQueryEvidence(
                    EvidenceStatus.UNAVAILABLE, (), "HL_DIRECT_LOOKUP_UNAVAILABLE"
                )
                continue
            try:
                raw = await asyncio.to_thread(
                    lookup, self.account_address, Cloid.from_str(cloid)
                )
            except Exception:
                direct[cloid] = RecoveryQueryEvidence(
                    EvidenceStatus.QUERY_FAILED, (), "HL_DIRECT_LOOKUP_FAILED"
                )
                continue
            found = self._collect_cloids(raw) & planned
            if cloid in found:
                direct[cloid] = RecoveryQueryEvidence(
                    EvidenceStatus.FOUND, (cloid,), "HL_DIRECT_FOUND"
                )
            elif self._is_authoritative_not_found(raw):
                direct[cloid] = RecoveryQueryEvidence(
                    EvidenceStatus.NOT_FOUND, (), "HL_DIRECT_NOT_FOUND"
                )
            else:
                direct[cloid] = RecoveryQueryEvidence(
                    EvidenceStatus.CONFLICTING, tuple(sorted(found)),
                    "HL_DIRECT_MALFORMED",
                )

        open_evidence = await self._collection_recovery_evidence(
            ("open_orders",),
            planned,
            (self.account_address,),
            "HL_OPEN_ORDERS",
        )
        history_evidence = await self._collection_recovery_evidence(
            ("historical_orders",),
            planned,
            (self.account_address,),
            "HL_HISTORY",
        )

        start_ms = int(datetime.fromisoformat(request.window_start).timestamp() * 1000)
        end_ms = int(datetime.now(UTC).timestamp() * 1000)
        fills_method = (
            getattr(self.info, "user_fills_by_time", None)
            if self.info is not None
            else None
        )
        if callable(fills_method):
            fills_evidence = await self._collection_recovery_evidence(
                ("user_fills_by_time",),
                planned,
                (self.account_address, start_ms, end_ms),
                "HL_FILLS",
            )
        else:
            unbounded_fills = (
                getattr(self.info, "user_fills", None)
                if self.info is not None
                else None
            )
            if not callable(unbounded_fills):
                fills_evidence = RecoveryQueryEvidence(
                    EvidenceStatus.UNAVAILABLE, (), "HL_FILLS_UNAVAILABLE"
                )
            else:
                try:
                    raw_fills = await asyncio.to_thread(
                        unbounded_fills, self.account_address
                    )
                    found_fills = self._collect_cloids(raw_fills) & planned
                    fills_evidence = RecoveryQueryEvidence(
                        EvidenceStatus.FOUND
                        if found_fills
                        else EvidenceStatus.TRUNCATED,
                        tuple(sorted(found_fills)),
                        "HL_FILLS_FOUND"
                        if found_fills
                        else "HL_FILLS_WINDOW_UNPROVEN",
                    )
                except Exception:
                    fills_evidence = RecoveryQueryEvidence(
                        EvidenceStatus.QUERY_FAILED, (), "HL_FILLS_FAILED"
                    )

        position_evidence = await self._position_recovery_evidence(request.symbol)
        return SubmissionRecoveryEvidence(
            request_id=request.request_id,
            planned_cloids=dict(request.planned_cloids),
            direct_lookup=direct,
            open_orders=open_evidence,
            historical_orders=history_evidence,
            fills=fills_evidence,
            position=position_evidence,
        )

    async def _collection_recovery_evidence(
        self,
        method_names: tuple[str, ...],
        planned: set[str],
        args: tuple[object, ...],
        code_prefix: str,
    ) -> RecoveryQueryEvidence:
        method = None
        if self.info is not None:
            method = next(
                (
                    getattr(self.info, name)
                    for name in method_names
                    if callable(getattr(self.info, name, None))
                ),
                None,
            )
        if method is None:
            return RecoveryQueryEvidence(
                EvidenceStatus.UNAVAILABLE, (), f"{code_prefix}_UNAVAILABLE"
            )
        try:
            raw = await asyncio.to_thread(method, *args)
        except Exception:
            return RecoveryQueryEvidence(
                EvidenceStatus.QUERY_FAILED, (), f"{code_prefix}_FAILED"
            )
        if isinstance(raw, dict) and any(
            bool(raw.get(flag)) for flag in ("truncated", "hasMore", "has_more")
        ):
            found = self._collect_cloids(raw) & planned
            return RecoveryQueryEvidence(
                EvidenceStatus.FOUND if found else EvidenceStatus.TRUNCATED,
                tuple(sorted(found)),
                f"{code_prefix}_FOUND"
                if found
                else f"{code_prefix}_TRUNCATED",
            )
        rows: object = raw
        if isinstance(raw, dict):
            rows = raw.get("data", raw.get("orders", raw.get("fills")))
        if not isinstance(rows, list):
            return RecoveryQueryEvidence(
                EvidenceStatus.CONFLICTING, (), f"{code_prefix}_MALFORMED"
            )
        found = self._collect_cloids(rows) & planned
        return RecoveryQueryEvidence(
            EvidenceStatus.FOUND if found else EvidenceStatus.NOT_FOUND,
            tuple(sorted(found)),
            f"{code_prefix}_FOUND" if found else f"{code_prefix}_NOT_FOUND",
        )

    async def _position_recovery_evidence(
        self, symbol: str
    ) -> RecoveryQueryEvidence:
        method = (
            getattr(self.info, "user_state", None)
            if self.info is not None
            else None
        )
        if not callable(method):
            return RecoveryQueryEvidence(
                EvidenceStatus.UNAVAILABLE, (), "HL_POSITION_UNAVAILABLE"
            )
        try:
            raw = await asyncio.to_thread(method, self.account_address)
        except Exception:
            return RecoveryQueryEvidence(
                EvidenceStatus.QUERY_FAILED, (), "HL_POSITION_FAILED"
            )
        if not isinstance(raw, dict) or not isinstance(
            raw.get("assetPositions", []), list
        ):
            return RecoveryQueryEvidence(
                EvidenceStatus.CONFLICTING, (), "HL_POSITION_MALFORMED"
            )
        for row in raw.get("assetPositions", []):
            position = self._parse_position(row)
            if position is not None and position.symbol == symbol and position.size != 0:
                return RecoveryQueryEvidence(
                    EvidenceStatus.FOUND, (), "HL_POSITION_EXPOSURE"
                )
        return RecoveryQueryEvidence(
            EvidenceStatus.NOT_FOUND, (), "HL_POSITION_FLAT"
        )

    @classmethod
    def _collect_cloids(cls, value: object) -> set[str]:
        found: set[str] = set()
        if isinstance(value, dict):
            for key, child in value.items():
                if str(key).lower() in {
                    "cloid",
                    "clientorderid",
                    "client_order_id",
                } and child is not None:
                    found.add(str(child))
                else:
                    found.update(cls._collect_cloids(child))
        elif isinstance(value, (list, tuple)):
            for child in value:
                found.update(cls._collect_cloids(child))
        return found

    @staticmethod
    def _is_authoritative_not_found(raw: object) -> bool:
        if not isinstance(raw, dict):
            return False
        status = str(raw.get("status", raw.get("error", ""))).lower()
        return status in {
            "unknownoid",
            "unknown_oid",
            "notfound",
            "not_found",
            "order not found",
        }

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

    # ------------------------------------------------------------------
    # TS-P1-004 typed, bounded partial-recovery surface
    #
    # Strict response mapping only. `status=ok` plus a resting/filled/success
    # status is APPLIED; an *authoritative* not-found/already-canceled/
    # validation rejection is NOT_APPLIED; everything else — timeout, transport
    # error, unparseable body, missing status, unexpected shape — is UNKNOWN.
    # There is no optimistic branch anywhere in this section.
    # ------------------------------------------------------------------

    _LIVE_ORDER_STATUSES = frozenset({"OPEN", "SUBMITTED", "PENDING", "RESTING"})
    _TERMINAL_ORDER_STATUSES = frozenset(
        {"FILLED", "CANCELED", "CANCELLED", "REJECTED", "EXPIRED"}
    )

    def lot_unit(self, symbol: str) -> LotUnit | None:
        """Symbol size quantum from exchange metadata; None when unknown."""
        decimals = self._size_decimals.get(str(symbol))
        if decimals is None:
            return None
        try:
            return LotUnit(int(decimals))
        except (LotQuantizationError, TypeError, ValueError):
            return None

    def _parse_recovery_open_orders(self, raw_orders: object) -> list[BrokerOrder]:
        """Fail-closed parser for open-order evidence used by recovery."""
        if not isinstance(raw_orders, list):
            raise ValueError("order collection")
        orders: list[BrokerOrder] = []
        for row in raw_orders:
            if not isinstance(row, dict):
                raise ValueError("order row")
            required = (
                isinstance(row.get("cloid"), str)
                and bool(str(row["cloid"]).strip())
                and isinstance(row.get("coin"), str)
                and bool(str(row["coin"]).strip())
                and str(row.get("side", "")).upper()
                in {"A", "B", "BUY", "SELL"}
                and ("sz" in row or "size" in row)
                and isinstance(row.get("status"), str)
                and bool(str(row["status"]).strip())
                and ("reduceOnly" in row or "reduce_only" in row)
            )
            reduce_only_raw = row.get("reduceOnly", row.get("reduce_only"))
            size = float(row.get("sz", row.get("size")))
            status = str(row["status"]).strip().upper()
            if (
                not required
                or not isinstance(reduce_only_raw, bool)
                or not math.isfinite(size)
                or size <= 0
                or status not in self._LIVE_ORDER_STATUSES
            ):
                raise ValueError("order fields")
            orders.append(self._parse_order(row))
        return orders

    async def symbol_snapshot(self, symbol: str) -> SymbolSnapshot:
        """Bounded position + open-order evidence for exactly one symbol."""
        lot = self.lot_unit(symbol)
        if self.info is None or not hasattr(self.info, "user_state"):
            return SymbolSnapshot(
                symbol=symbol,
                exact=False,
                net_size=None,
                open_orders=(),
                lot=lot,
                evidence=Evidence("SNAPSHOT", "HL_POSITION_QUERY_FAILED"),
            )
        try:
            state = await asyncio.to_thread(
                self.info.user_state, self.account_address
            )
        except Exception as exc:  # noqa: BLE001 - any failure is inexact evidence
            return SymbolSnapshot(
                symbol=symbol, exact=False, net_size=None, open_orders=(), lot=lot,
                evidence=Evidence(
                    "SNAPSHOT", "HL_POSITION_QUERY_FAILED", detail=type(exc).__name__
                ),
            )
        if not isinstance(state, dict) or not isinstance(
            state.get("assetPositions"), list
        ):
            return SymbolSnapshot(
                symbol=symbol,
                exact=False,
                net_size=None,
                open_orders=(),
                lot=lot,
                evidence=Evidence("SNAPSHOT", "HL_POSITION_EVIDENCE_MALFORMED"),
            )
        positions: list[Position] = []
        try:
            for row in state["assetPositions"]:
                if not isinstance(row, dict):
                    raise ValueError("position row")
                payload = row.get("position", row)
                if (
                    not isinstance(payload, dict)
                    or not isinstance(payload.get("coin"), str)
                    or not str(payload["coin"]).strip()
                    or ("szi" not in payload and "size" not in payload)
                ):
                    raise ValueError("position fields")
                raw_size = payload.get("szi", payload.get("size"))
                parsed_size = float(raw_size)
                if not math.isfinite(parsed_size):
                    raise ValueError("position size")
                parsed = self._parse_position(row)
                if parsed is None:
                    raise ValueError("position parse")
                if parsed.size != 0:
                    positions.append(parsed)
        except (TypeError, ValueError, OverflowError):
            return SymbolSnapshot(
                symbol=symbol,
                exact=False,
                net_size=None,
                open_orders=(),
                lot=lot,
                evidence=Evidence("SNAPSHOT", "HL_POSITION_EVIDENCE_MALFORMED"),
            )
        if not hasattr(self.info, "open_orders"):
            return SymbolSnapshot(
                symbol=symbol,
                exact=False,
                net_size=None,
                open_orders=(),
                lot=lot,
                evidence=Evidence("SNAPSHOT", "HL_OPEN_ORDER_QUERY_FAILED"),
            )
        try:
            raw_orders = await asyncio.to_thread(
                self.info.open_orders, self.account_address
            )
        except Exception as exc:  # noqa: BLE001
            return SymbolSnapshot(
                symbol=symbol, exact=False, net_size=None, open_orders=(), lot=lot,
                evidence=Evidence(
                    "SNAPSHOT", "HL_OPEN_ORDER_QUERY_FAILED", detail=type(exc).__name__
                ),
            )
        try:
            orders = self._parse_recovery_open_orders(raw_orders)
        except (TypeError, ValueError, OverflowError):
            return SymbolSnapshot(
                symbol=symbol,
                exact=False,
                net_size=None,
                open_orders=(),
                lot=lot,
                evidence=Evidence("SNAPSHOT", "HL_ORDER_EVIDENCE_MALFORMED"),
            )
        matching = [p for p in positions if p.symbol == symbol]
        if len(matching) > 1:
            return SymbolSnapshot(
                symbol=symbol, exact=False, net_size=None, open_orders=(), lot=lot,
                evidence=Evidence("SNAPSHOT", "HL_POSITION_CONFLICTING"),
            )
        net = float(matching[0].size) if matching else 0.0
        views = tuple(
            OrderView(
                cloid=order.cloid,
                coin=order.coin,
                side=order.side,
                size=float(order.size),
                role=str(order.role),
                reduce_only=bool(order.reduce_only),
                trigger_px=order.trigger_px,
                status=str(order.status),
                order_ref=order.order_ref,
            )
            for order in orders
            if order.coin == symbol
        )
        return SymbolSnapshot(
            symbol=symbol,
            exact=lot is not None,
            net_size=net,
            open_orders=views,
            lot=lot,
            evidence=Evidence(
                "SNAPSHOT",
                "HL_SNAPSHOT_COMPLETE" if lot is not None else "HL_SIZE_QUANTUM_MISSING",
            ),
            observed_ts=datetime.now(UTC),
        )

    async def query_order(self, cloid: str, symbol: str) -> OrderQueryResult:
        """Direct single-order lookup; an unusable answer stays UNKNOWN."""
        if self.info is None:
            return OrderQueryResult(
                known=False, evidence=Evidence("QUERY_ORDER", "HL_NOT_CONFIGURED")
            )
        lookup = getattr(self.info, "query_order_by_cloid", None)
        if callable(lookup):
            try:
                raw = await asyncio.to_thread(lookup, self.account_address, Cloid.from_str(str(cloid)))
            except Exception as exc:  # noqa: BLE001
                return OrderQueryResult(
                    known=False,
                    evidence=Evidence(
                        "QUERY_ORDER", "HL_QUERY_FAILED", detail=type(exc).__name__
                    ),
                )
            return self._parse_order_query(raw, cloid)
        # Fall back to the raw open-order collection: it can only prove presence,
        # and any malformed row makes the entire recovery answer inexact.
        if not hasattr(self.info, "open_orders"):
            return OrderQueryResult(
                known=False,
                evidence=Evidence("OPEN_ORDERS", "HL_OPEN_ORDER_QUERY_FAILED"),
            )
        try:
            raw_orders = await asyncio.to_thread(
                self.info.open_orders, self.account_address
            )
            orders = self._parse_recovery_open_orders(raw_orders)
        except Exception as exc:  # noqa: BLE001
            return OrderQueryResult(
                known=False,
                evidence=Evidence(
                    "OPEN_ORDERS", "HL_ORDER_EVIDENCE_MALFORMED",
                    detail=type(exc).__name__,
                ),
            )
        for order in orders:
            if order.cloid == str(cloid):
                return OrderQueryResult(
                    known=True, found=True, terminal=False,
                    raw_status=str(order.status),
                    evidence=Evidence("OPEN_ORDERS", "HL_ORDER_PRESENT"),
                )
        # Absence from the open-order page alone is not proof of terminality.
        return OrderQueryResult(
            known=False,
            evidence=Evidence("OPEN_ORDERS", "HL_ORDER_ABSENCE_NOT_AUTHORITATIVE"),
        )

    @classmethod
    def _parse_order_query(cls, raw: object, cloid: str) -> OrderQueryResult:
        if not isinstance(raw, dict):
            return OrderQueryResult(
                known=False, evidence=Evidence("QUERY_ORDER", "HL_QUERY_UNPARSEABLE")
            )
        status = raw.get("status")
        if isinstance(status, str) and status.lower() in {"unknownoid", "unknown_oid"}:
            return OrderQueryResult(
                known=True, found=False, terminal=True,
                evidence=Evidence("QUERY_ORDER", "HL_ORDER_UNKNOWN_OID"),
            )
        if not isinstance(status, str) or status.lower() != "order":
            return OrderQueryResult(
                known=False, evidence=Evidence("QUERY_ORDER", "HL_QUERY_UNEXPECTED")
            )
        payload = raw.get("order")
        if not isinstance(payload, dict):
            return OrderQueryResult(
                known=False, evidence=Evidence("QUERY_ORDER", "HL_QUERY_UNPARSEABLE")
            )
        order_status = payload.get("status")
        if not isinstance(order_status, str) or not order_status.strip():
            return OrderQueryResult(
                known=False, evidence=Evidence("QUERY_ORDER", "HL_QUERY_STATUS_MISSING")
            )
        normalized = order_status.strip().upper()
        if normalized not in (
            cls._LIVE_ORDER_STATUSES | cls._TERMINAL_ORDER_STATUSES
        ):
            return OrderQueryResult(
                known=False,
                evidence=Evidence("QUERY_ORDER", "HL_QUERY_STATUS_UNKNOWN"),
            )
        inner = payload.get("order")
        filled: float | None = None
        if isinstance(inner, dict):
            original = inner.get("origSz")
            remaining = inner.get("sz")
            if original is not None and remaining is not None:
                try:
                    filled = float(original) - float(remaining)
                except (TypeError, ValueError):
                    filled = None
        live = normalized in cls._LIVE_ORDER_STATUSES
        return OrderQueryResult(
            known=True,
            found=live,
            terminal=not live,
            raw_status=normalized,
            filled_size=filled,
            evidence=Evidence("QUERY_ORDER", "HL_QUERY_COMPLETE"),
        )

    _NOT_APPLIED_MARKERS = (
        "order was never placed",
        "never placed",
        "order not found",
        "was not found",
        "already canceled",
        "already cancelled",
        "cannot be canceled",
        "invalid order",
        "reduce only",
        "insufficient",
    )

    @classmethod
    def _classify_exchange_result(cls, raw: object) -> tuple[ActionOutcome, str]:
        """Strict response -> outcome mapping. Anything unexpected is UNKNOWN."""
        if not isinstance(raw, dict):
            return ActionOutcome.UNKNOWN, "HL_RESPONSE_NOT_OBJECT"
        status = raw.get("status")
        if not isinstance(status, str):
            return ActionOutcome.UNKNOWN, "HL_STATUS_MISSING"
        if status.lower() == "err":
            message = cls._safe_exchange_message(raw.get("response"), cap=256).lower()
            if any(marker in message for marker in cls._NOT_APPLIED_MARKERS):
                return ActionOutcome.NOT_APPLIED, "HL_DEFINITIVE_REJECTION"
            return ActionOutcome.UNKNOWN, "HL_ERROR_NOT_AUTHORITATIVE"
        if status.lower() != "ok":
            return ActionOutcome.UNKNOWN, "HL_STATUS_UNEXPECTED"
        try:
            statuses = cls._extract_statuses(raw)
        except Exception:  # noqa: BLE001 - unparseable body is never a success
            return ActionOutcome.UNKNOWN, "HL_RESPONSE_UNPARSEABLE"
        if not statuses:
            return ActionOutcome.UNKNOWN, "HL_STATUSES_EMPTY"
        for entry in statuses:
            if "error" in entry:
                message = cls._safe_exchange_message(entry.get("error"), cap=256).lower()
                if any(marker in message for marker in cls._NOT_APPLIED_MARKERS):
                    return ActionOutcome.NOT_APPLIED, "HL_DEFINITIVE_REJECTION"
                return ActionOutcome.UNKNOWN, "HL_ERROR_NOT_AUTHORITATIVE"
            if not ({"resting", "filled", "success", "pending_child"} & set(entry)):
                return ActionOutcome.UNKNOWN, "HL_STATUS_UNRECOGNIZED"
        return ActionOutcome.APPLIED, "HL_APPLIED"

    async def cancel_order_by_cloid(self, cloid: str, symbol: str) -> CancelResult:
        if self.exchange is None or not hasattr(self.exchange, "cancel_by_cloid"):
            return CancelResult(
                ActionOutcome.NOT_APPLIED, str(cloid),
                Evidence("CANCEL", "HL_NOT_CONFIGURED"),
            )
        spec = self._order_specs.get(str(cloid), {})
        coin = str(spec.get("coin", symbol or self.coin))
        try:
            raw = await asyncio.to_thread(
                self.exchange.cancel_by_cloid, coin, Cloid.from_str(str(cloid))
            )
        except Exception as exc:  # noqa: BLE001 - transport failure is UNKNOWN
            return CancelResult(
                ActionOutcome.UNKNOWN, str(cloid),
                Evidence("CANCEL", "HL_TRANSPORT_FAILED", detail=type(exc).__name__),
            )
        outcome, reason = self._classify_exchange_result(raw)
        return CancelResult(outcome, str(cloid), Evidence("CANCEL", reason))

    async def place_protective_stop(
        self,
        *,
        symbol: str,
        cloid: str,
        exit_side: str,
        size: float,
        trigger_px: float,
    ) -> PlaceResult:
        if self.exchange is None or not hasattr(self.exchange, "bulk_orders"):
            return PlaceResult(
                ActionOutcome.NOT_APPLIED, str(cloid), None,
                Evidence("PLACE", "HL_NOT_CONFIGURED"),
            )
        is_buy = str(exit_side).upper() == "BUY"
        try:
            rounded = self._round_price(symbol, trigger_px)
        except Exception as exc:  # noqa: BLE001 - never send an unrounded price
            return PlaceResult(
                ActionOutcome.NOT_APPLIED, str(cloid), None,
                Evidence("PLACE", "HL_PRICE_INVALID", detail=type(exc).__name__),
            )
        typed_cloid = Cloid.from_str(str(cloid))
        request = self._request(
            symbol,
            is_buy,
            float(size),
            rounded,
            {"trigger": {"triggerPx": rounded, "isMarket": True, "tpsl": "sl"}},
            True,
            typed_cloid,
        )
        try:
            raw = await asyncio.to_thread(
                self.exchange.bulk_orders, [request], grouping="positionTpsl"
            )
        except Exception as exc:  # noqa: BLE001
            return PlaceResult(
                ActionOutcome.UNKNOWN, str(cloid), None,
                Evidence("PLACE", "HL_TRANSPORT_FAILED", detail=type(exc).__name__),
            )
        outcome, reason = self._classify_exchange_result(raw)
        if outcome is ActionOutcome.APPLIED:
            self._order_specs[str(cloid)] = {**request, "role": "SL"}
        return PlaceResult(
            outcome, str(cloid), self._extract_oid(raw), Evidence("PLACE", reason)
        )

    async def flatten_reduce_only(
        self, *, symbol: str, cloid: str, size: float
    ) -> FlattenResult:
        if self.exchange is None or not hasattr(self.exchange, "market_close"):
            return FlattenResult(
                ActionOutcome.NOT_APPLIED, str(cloid),
                Evidence("FLATTEN", "HL_NOT_CONFIGURED"),
            )
        try:
            raw = await asyncio.to_thread(
                self.exchange.market_close,
                symbol,
                sz=abs(float(size)),
                slippage=0.05,
                cloid=Cloid.from_str(str(cloid)),
            )
        except Exception as exc:  # noqa: BLE001
            return FlattenResult(
                ActionOutcome.UNKNOWN, str(cloid),
                Evidence("FLATTEN", "HL_TRANSPORT_FAILED", detail=type(exc).__name__),
            )
        outcome, reason = self._classify_exchange_result(raw)
        return FlattenResult(outcome, str(cloid), Evidence("FLATTEN", reason))

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
        status = "FILLED" if isinstance(raw, dict) and "filled" in raw else "OPEN"
        result = {"cloid": str(cloid), "oid": None, "role": role, "status": status, "qty": qty}
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
            reduce_only=bool(row.get("reduceOnly", row.get("reduce_only", False))),
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

    def _dispatch_user_event(self, event: BrokerEvent) -> None:
        for callback in list(self._user_callbacks):
            callback(event)

    @staticmethod
    def _float(value: object, default: float = 0.0) -> float:
        if value in (None, ""):
            return default
        return float(value)
