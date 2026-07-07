"""Hyperliquid broker adapter.

Unit tests mock the SDK clients. The P0 smoke script is written separately and
must not be run without explicit approval because it places testnet orders.
"""

from __future__ import annotations

import os
import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Callable

from bridge.engine.types import Bar, OrderPlan

LIVE_ACK = "I_UNDERSTAND_THIS_IS_REAL_MONEY"


class BrokerRefusedLive(RuntimeError):
    pass


class HyperliquidNotConfigured(RuntimeError):
    pass


@dataclass
class BarFinalizer:
    on_bar_closed: Callable[[Bar], None]
    last_open_ts: datetime | None = None
    current: Bar | None = None
    emitted: set[datetime] | None = None

    def __post_init__(self) -> None:
        if self.emitted is None:
            self.emitted = set()

    def on_candle(self, candle: dict) -> None:
        opened = datetime.fromtimestamp(int(candle["t"]) / 1000, tz=UTC)
        bar = Bar(
            ts=opened,
            open=float(candle["o"]),
            high=float(candle["h"]),
            low=float(candle["l"]),
            close=float(candle["c"]),
            volume=float(candle["v"]),
        )
        if self.current is not None and opened > self.current.ts:
            self._emit(self.current)
        self.current = bar
        self.last_open_ts = opened

    def _emit(self, bar: Bar) -> None:
        assert self.emitted is not None
        if bar.ts in self.emitted:
            return
        self.emitted.add(bar.ts)
        self.on_bar_closed(bar)


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
    ) -> None:
        self.network = network
        self.enable_live = enable_live
        self.live_ack = live_ack
        self.strategy_live_allowed = strategy_live_allowed
        self.account_address = account_address or os.environ.get("HL_ACCOUNT_ADDRESS", "")
        self.api_wallet_key = api_wallet_key or os.environ.get("HL_API_WALLET_KEY", "")
        self.info = info_client
        self.exchange = exchange_client
        self.connected = False

    async def connect(self) -> None:
        self._check_network_lock()
        if self.info is None or self.exchange is None:
            self._build_sdk_clients()
        self.connected = True

    async def account(self) -> dict:
        if self.info is None:
            raise HyperliquidNotConfigured("Info client not configured")
        if hasattr(self.info, "user_state"):
            return self.info.user_state(self.account_address)  # type: ignore[no-any-return]
        return {}

    async def positions(self) -> list:
        state = await self.account()
        return state.get("assetPositions", []) if isinstance(state, dict) else []

    async def open_orders(self) -> list:
        if self.info is None or not hasattr(self.info, "open_orders"):
            return []
        return self.info.open_orders(self.account_address)  # type: ignore[no-any-return]

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list[Bar]:
        if self.info is None or not hasattr(self.info, "candles_snapshot"):
            return []
        candles = self.info.candles_snapshot(coin, tf, 0, 0)[-lookback:]
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
        finalizer = BarFinalizer(on_bar_closed=on_bar_closed)
        self.info.subscribe({"type": "candle", "coin": coin, "interval": tf}, finalizer.on_candle)

    async def place_bracket(self, plan: OrderPlan) -> dict:
        if self.exchange is None or not hasattr(self.exchange, "order"):
            raise HyperliquidNotConfigured("Exchange client not configured")
        is_entry_buy = plan.signal.direction == "LONG"
        is_exit_buy = not is_entry_buy
        entry_cloid = self._cloid(plan, "entry")
        sl_cloid = self._cloid(plan, "sl")
        entry_raw = self.exchange.order(
            plan.signal.symbol,
            is_entry_buy,
            plan.qty,
            0,
            {"limit": {"tif": "Ioc"}},
            reduce_only=False,
            cloid=entry_cloid,
        )
        sl_raw = self.exchange.order(
            plan.signal.symbol,
            is_exit_buy,
            plan.qty,
            0,
            {
                "trigger": {"triggerPx": plan.stop_loss, "isMarket": True, "tpsl": "sl"},
                "grouping": "positionTpsl",
            },
            reduce_only=True,
            cloid=sl_cloid,
        )
        result = {
            "entry": self._order_result("ENTRY", entry_cloid, entry_raw, plan.qty),
            "sl": self._order_result("SL", sl_cloid, sl_raw, plan.qty, trigger_px=plan.stop_loss),
        }
        if plan.take_profit is not None:
            tp_cloid = self._cloid(plan, "tp")
            tp_raw = self.exchange.order(
                plan.signal.symbol,
                is_exit_buy,
                plan.qty,
                0,
                {
                    "trigger": {"triggerPx": plan.take_profit, "isMarket": True, "tpsl": "tp"},
                    "grouping": "positionTpsl",
                },
                reduce_only=True,
                cloid=tp_cloid,
            )
            result["tp"] = self._order_result("TP", tp_cloid, tp_raw, plan.qty, trigger_px=plan.take_profit)
        return result

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        if self.exchange is not None and hasattr(self.exchange, "modify_order"):
            self.exchange.modify_order(
                cloid,
                {"trigger": {"triggerPx": new_stop, "isMarket": True, "tpsl": "sl"}, "grouping": "positionTpsl"},
            )

    async def cancel(self, cloid: str) -> None:
        if self.exchange is not None and hasattr(self.exchange, "cancel_by_cloid"):
            self.exchange.cancel_by_cloid(cloid)

    async def cancel_all(self) -> None:
        for order in await self.open_orders():
            cloid = order.get("cloid") if isinstance(order, dict) else None
            if cloid:
                await self.cancel(cloid)

    async def flatten(self, coin: str) -> None:
        if self.exchange is None or not hasattr(self.exchange, "order"):
            raise HyperliquidNotConfigured("Exchange client not configured")
        size = 0.0
        for position in await self.positions():
            parsed = self._parse_position(position)
            if parsed is None or parsed["coin"] != coin:
                continue
            size = float(parsed["size"])
            break
        if size == 0:
            return None
        self.exchange.order(
            coin,
            size < 0,
            abs(size),
            0,
            {"limit": {"tif": "Ioc"}},
            reduce_only=True,
            cloid=self._raw_cloid(f"{coin}:flatten:{datetime.now(UTC).isoformat()}"),
        )
        return None

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

    def _cloid(self, plan: OrderPlan, role: str) -> str:
        raw = f"{plan.signal.symbol}:{plan.signal.ts.isoformat()}:{plan.signal.direction}:{role}"
        return self._raw_cloid(raw)

    @staticmethod
    def _raw_cloid(raw: str) -> str:
        return "0x" + hashlib.blake2s(raw.encode("utf-8"), digest_size=16).hexdigest()

    @staticmethod
    def _order_result(role: str, cloid: str, raw: object, qty: float, trigger_px: float | None = None) -> dict:
        result = {"cloid": cloid, "oid": None, "role": role, "status": "OPEN", "qty": qty}
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
    def _parse_position(position: object) -> dict[str, object] | None:
        if not isinstance(position, dict):
            return None
        payload = position.get("position", position)
        if not isinstance(payload, dict) or "coin" not in payload:
            return None
        raw_size = payload.get("szi", payload.get("size", 0))
        return {"coin": payload["coin"], "size": float(raw_size)}
