"""Deterministic mock broker for tests and dry-run mode."""

from __future__ import annotations

import csv
import itertools
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

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


@dataclass
class MockBroker:
    bars: list[Bar]
    starting_equity: float = 10_000.0
    coin: str = "BTC"
    connected: bool = False
    orders: list[dict] = field(default_factory=list)
    fills: list[dict] = field(default_factory=list)
    position: Position | None = None
    _ids: itertools.count = field(default_factory=lambda: itertools.count(1))
    _user_callbacks: list[Callable[[BrokerEvent], None]] = field(default_factory=list)

    @classmethod
    def from_csv(cls, path: str | Path, starting_equity: float = 10_000.0) -> "MockBroker":
        rows: list[Bar] = []
        with Path(path).open("r", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                rows.append(
                    Bar(
                        ts=datetime.fromisoformat(row["ts"]),
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row["volume"]),
                    )
                )
        return cls(bars=rows, starting_equity=starting_equity)

    async def connect(self) -> None:
        self.connected = True

    async def account(self) -> AccountSnapshot:
        return AccountSnapshot(
            equity=self.starting_equity,
            available_margin=self.starting_equity,
            withdrawable=self.starting_equity,
        )

    async def positions(self) -> list[Position]:
        return [] if self.position is None else [self.position]

    async def open_orders(self) -> list[BrokerOrder]:
        rows: list[BrokerOrder] = []
        for order in self.orders:
            if order["status"] not in {"SUBMITTED", "OPEN"}:
                continue
            direction = order.get("direction", "LONG")
            is_entry = order["role"] == "ENTRY"
            is_buy = (direction == "LONG") if is_entry else (direction == "SHORT")
            rows.append(
                BrokerOrder(
                    cloid=order["cloid"],
                    oid=order["oid"],
                    coin=order.get("symbol", self.coin),
                    side="BUY" if is_buy else "SELL",
                    size=float(order["qty"]),
                    status=order["status"],
                    role=order["role"],
                    reduce_only=bool(order.get("reduce_only", False)),
                    trigger_px=order.get("trigger_px"),
                    order_type=order["role"],
                )
            )
        return rows

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list[Bar]:
        return self.bars[-lookback:]

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed: Callable[[Bar], None]) -> None:
        for bar in self.bars:
            on_bar_closed(bar)

    def subscribe_user_events(self, on_event: Callable[[BrokerEvent], None]) -> None:
        self._user_callbacks.append(on_event)

    async def place_bracket(self, plan: OrderPlan) -> dict:
        if not self.connected:
            raise RuntimeError("MockBroker is not connected")
        if len(self.bars) < 2:
            raise ValueError("MockBroker needs at least two bars for next-open fill")

        entry = self._order(
            "ENTRY",
            "OPEN",
            plan.qty,
            plan.signal.ref_price,
            reduce_only=False,
            signal_ts=plan.signal.ts,
            direction=plan.signal.direction,
            symbol=plan.signal.symbol,
            leverage=plan.leverage,
        )
        sl = self._order(
            "SL",
            "OPEN",
            plan.qty,
            plan.stop_loss,
            reduce_only=True,
            trigger_px=plan.stop_loss,
            direction=plan.signal.direction,
            symbol=plan.signal.symbol,
        )
        result = {"entry": entry, "sl": sl}
        if plan.take_profit is not None:
            result["tp"] = self._order(
                "TP",
                "OPEN",
                plan.qty,
                plan.take_profit,
                reduce_only=True,
                trigger_px=plan.take_profit,
                direction=plan.signal.direction,
                symbol=plan.signal.symbol,
            )
        return result

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        for order in self.orders:
            if order["cloid"] == cloid:
                order["trigger_px"] = new_stop
                order["avg_fill_px"] = new_stop
                return
        raise KeyError(cloid)

    async def cancel(self, cloid: str) -> None:
        for order in self.orders:
            if order["cloid"] == cloid and order["status"] in {"SUBMITTED", "OPEN"}:
                order["status"] = "CANCELLED_BY_ENGINE"
                self._emit_order_update(order)

    async def cancel_all(self) -> None:
        for order in self.orders:
            if order["status"] in {"SUBMITTED", "OPEN"}:
                order["status"] = "CANCELLED_BY_ENGINE"
                self._emit_order_update(order)

    async def flatten(self, coin: str) -> None:
        if self.position is not None and self.position.symbol == coin:
            qty = abs(self.position.size)
            px = self._last_price()
            close = self._order("CLOSE", "FILLED", qty, px, reduce_only=True, symbol=coin)
            self._record_fill(close, qty, px, datetime.now())
        self.position = None

    async def reprotect_position(
        self,
        position: Position,
        stop_loss: float,
        take_profit: float | None,
        decision_uid: str,
    ) -> dict[str, dict] | None:
        direction = "LONG" if position.size > 0 else "SHORT"
        sl = self._order(
            "SL",
            "OPEN",
            abs(position.size),
            stop_loss,
            reduce_only=True,
            trigger_px=stop_loss,
            direction=direction,
            symbol=position.symbol,
            cloid=f"mock-reprotect-{decision_uid}-sl",
        )
        return {"sl": sl}

    def process_bar(self, bar: Bar) -> None:
        for order in self.orders:
            if order["role"] != "ENTRY" or order["status"] != "OPEN":
                continue
            signal_ts = order.get("signal_ts")
            if isinstance(signal_ts, datetime) and bar.ts <= signal_ts:
                continue
            entry_px = bar.open
            order["status"] = "FILLED"
            order["avg_fill_px"] = entry_px
            direction = order.get("direction", "LONG")
            side = 1 if direction == "LONG" else -1
            self.position = Position(
                symbol=order.get("symbol", self.coin),
                size=float(order["qty"]) * side,
                entry_px=entry_px,
                unrealized=0.0,
                leverage=int(order.get("leverage", 1)),
                liquidation_px=None,
                margin_used=abs(float(order["qty"]) * entry_px) / max(int(order.get("leverage", 1)), 1),
            )
            self._record_fill(order, float(order["qty"]), entry_px, bar.ts)
            self._emit_order_update(order)

        if self.position is None:
            return

        is_long = self.position.size > 0
        trigger_orders = [order for order in self.orders if order["role"] in {"SL", "TP"} and order["status"] == "OPEN"]
        sl = next((order for order in trigger_orders if order["role"] == "SL"), None)
        tp = next((order for order in trigger_orders if order["role"] == "TP"), None)
        if sl is not None:
            sl_px = float(sl["trigger_px"])
            sl_hit = bar.low <= sl_px if is_long else bar.high >= sl_px
            if sl_hit:
                self._fill_exit(sl, sl_px, bar.ts)
                return
        if tp is not None:
            tp_px = float(tp["trigger_px"])
            tp_hit = bar.high >= tp_px if is_long else bar.low <= tp_px
            if tp_hit:
                self._fill_exit(tp, tp_px, bar.ts)

    def _next_bar_after(self, ts: datetime) -> Bar:
        for bar in self.bars:
            if bar.ts > ts:
                return bar
        return self.bars[-1]

    def _fill_exit(self, order: dict, px: float, ts: datetime) -> None:
        order["status"] = "FILLED"
        order["avg_fill_px"] = px
        self._record_fill(order, float(order["qty"]), px, ts)
        self._emit_order_update(order)
        self.position = None

    def _order(
        self,
        role: str,
        status: str,
        qty: float,
        avg_fill_px: float,
        reduce_only: bool = False,
        trigger_px: float | None = None,
        **extra,
    ) -> dict:
        oid = next(self._ids)
        requested_cloid = extra.pop("cloid", None)
        order = {
            "cloid": requested_cloid or f"mock-{oid}",
            "oid": oid,
            "role": role,
            "status": status,
            "qty": qty,
            "avg_fill_px": avg_fill_px,
            "reduce_only": reduce_only,
        }
        if trigger_px is not None:
            order["trigger_px"] = trigger_px
        order.update(extra)
        self.orders.append(order)
        return order

    def _record_fill(self, order: dict, qty: float, px: float, ts: datetime) -> None:
        fill = {
            "fill_id": f"{order['cloid']}:{len(self.fills) + 1}",
            "cloid": order["cloid"],
            "role": order["role"],
            "qty": qty,
            "px": px,
            "ts": ts,
        }
        self.fills.append(fill)
        event = FillEvent(
            fill_id=fill["fill_id"],
            cloid=fill["cloid"],
            coin=order.get("symbol", self.coin),
            qty=qty,
            px=px,
            ts=ts,
            role=order["role"],
        )
        for callback in list(self._user_callbacks):
            callback(event)

    def _emit_order_update(self, order: dict) -> None:
        event = OrderUpdateEvent(
            cloid=order["cloid"],
            status=order["status"],
            ts=datetime.now().astimezone(),
            filled_qty=float(order["qty"]) if order["status"] == "FILLED" else None,
            avg_fill_px=order.get("avg_fill_px"),
        )
        for callback in list(self._user_callbacks):
            callback(event)

    def _last_price(self) -> float:
        if self.bars:
            return self.bars[-1].close
        if self.position is not None:
            return self.position.entry_px
        return 0.0
