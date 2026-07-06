"""Deterministic mock broker for tests and dry-run mode."""

from __future__ import annotations

import csv
import itertools
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

from bridge.engine.types import Bar, OrderPlan, Position


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

    async def account(self) -> dict:
        return {"equity": self.starting_equity, "available_margin": self.starting_equity}

    async def positions(self) -> list[Position]:
        return [] if self.position is None else [self.position]

    async def open_orders(self) -> list[dict]:
        return [order for order in self.orders if order["status"] in {"SUBMITTED", "OPEN"}]

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list[Bar]:
        return self.bars[-lookback:]

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed: Callable[[Bar], None]) -> None:
        for bar in self.bars:
            on_bar_closed(bar)

    async def place_bracket(self, plan: OrderPlan) -> dict:
        if not self.connected:
            raise RuntimeError("MockBroker is not connected")
        if len(self.bars) < 2:
            raise ValueError("MockBroker needs at least two bars for next-open fill")

        fill_bar = self._next_bar_after(plan.signal.ts)
        side = 1 if plan.signal.direction == "LONG" else -1
        entry_px = fill_bar.open if plan.entry_type == "MKT" else plan.limit_price
        if entry_px is None:
            raise ValueError("limit_price is required for LMT orders")

        entry = self._order("ENTRY", "FILLED", plan.qty, entry_px)
        self.fills.append({"role": "ENTRY", "qty": plan.qty, "px": entry_px})
        self.position = Position(
            symbol=plan.signal.symbol,
            size=plan.qty * side,
            entry_px=entry_px,
            unrealized=0.0,
            leverage=plan.leverage,
            liquidation_px=None,
            margin_used=abs(plan.qty * entry_px) / max(plan.leverage, 1),
        )

        exit_order = self._simulate_exit(plan, start_bar=fill_bar)
        return {"entry": entry, "exit": exit_order}

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        for order in self.orders:
            if order["cloid"] == cloid:
                order["trigger_px"] = new_stop
                return
        raise KeyError(cloid)

    async def cancel(self, cloid: str) -> None:
        for order in self.orders:
            if order["cloid"] == cloid and order["status"] in {"SUBMITTED", "OPEN"}:
                order["status"] = "CANCELLED_BY_ENGINE"

    async def cancel_all(self) -> None:
        for order in self.orders:
            if order["status"] in {"SUBMITTED", "OPEN"}:
                order["status"] = "CANCELLED_BY_ENGINE"

    async def flatten(self, coin: str) -> None:
        self.position = None

    def _next_bar_after(self, ts: datetime) -> Bar:
        for bar in self.bars:
            if bar.ts > ts:
                return bar
        return self.bars[-1]

    def _simulate_exit(self, plan: OrderPlan, start_bar: Bar) -> dict:
        is_long = plan.signal.direction == "LONG"
        for bar in self.bars[self.bars.index(start_bar) :]:
            sl_hit = bar.low <= plan.stop_loss if is_long else bar.high >= plan.stop_loss
            tp_hit = False
            if plan.take_profit is not None:
                tp_hit = bar.high >= plan.take_profit if is_long else bar.low <= plan.take_profit

            if sl_hit:
                return self._close("SL", plan.qty, plan.stop_loss)
            if tp_hit and plan.take_profit is not None:
                return self._close("TP", plan.qty, plan.take_profit)

        return self._order("SL", "OPEN", plan.qty, plan.stop_loss)

    def _close(self, role: str, qty: float, px: float) -> dict:
        order = self._order(role, "FILLED", qty, px)
        self.fills.append({"role": role, "qty": qty, "px": px})
        self.position = None
        return order

    def _order(self, role: str, status: str, qty: float, avg_fill_px: float) -> dict:
        oid = next(self._ids)
        order = {
            "cloid": f"mock-{oid}",
            "oid": oid,
            "role": role,
            "status": status,
            "qty": qty,
            "avg_fill_px": avg_fill_px,
        }
        self.orders.append(order)
        return order
