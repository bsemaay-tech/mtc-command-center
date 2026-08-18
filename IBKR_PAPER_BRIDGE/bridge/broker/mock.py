"""Deterministic mock broker for tests and dry-run mode."""

from __future__ import annotations

import csv
import asyncio
import itertools
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from bridge.broker.base import RecoveryCycle, RecoveryEvidence, SubmissionResult
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
    streaming: bool = False
    stream_delay_s: float = 0.05
    _ids: itertools.count = field(default_factory=lambda: itertools.count(1))
    _user_callbacks: list[Callable[[BrokerEvent], None]] = field(default_factory=list)
    _bar_callbacks: list[Callable[[Bar], None]] = field(default_factory=list)
    resubscribe_count: int = 0
    place_count: int = 0

    # TS-P1-003 configurable outcomes
    pre_send_failure: bool = False
    post_send_timeout: bool = False
    definitive_rejection: bool = False
    mixed_response: bool = False  # accepted+rejected mix
    return_empty_response: bool = False
    return_malformed_response: bool = False
    wrong_cloids: bool = False
    extra_roles: bool = False
    missing_roles: bool = False
    crash_after_accept: bool = False  # accepts but then raises

    # Recovery evidence configuration
    recovery_evidence_map: dict[str, list[RecoveryEvidence]] = field(default_factory=dict)
    recovery_query_should_fail: bool = False
    recovery_open_orders_empty: bool = False
    recovery_delayed_visibility: bool = False  # orders appear after a delay
    _recovery_cycles_seen: int = 0

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
        if self.streaming:
            return []
        return self.bars[-lookback:]

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed: Callable[[Bar], None]) -> None:
        self._bar_callbacks.append(on_bar_closed)
        if not self.streaming:
            for bar in self.bars:
                on_bar_closed(bar)

    async def start_stream(self) -> None:
        for bar in self.bars:
            self.emit_bar(bar)
            await asyncio.sleep(self.stream_delay_s)

    def emit_bar(self, bar: Bar) -> None:
        self.process_bar(bar)
        for callback in list(self._bar_callbacks):
            callback(bar)

    async def resubscribe(self) -> None:
        self.resubscribe_count += 1

    def subscribe_user_events(self, on_event: Callable[[BrokerEvent], None]) -> None:
        self._user_callbacks.append(on_event)

    async def place_bracket(self, plan: OrderPlan) -> SubmissionResult:
        self.place_count += 1
        if not self.connected:
            raise RuntimeError("MockBroker is not connected")
        if self.pre_send_failure:
            return SubmissionResult(
                verdict="PRE_SEND_FAILURE",
                error_type="PreSendCheckFailed",
                safe_detail="mock pre-send failure",
            )
        if self.return_malformed_response:
            return SubmissionResult(
                verdict="OUTCOME_UNKNOWN",
                error_type="MalformedResponse",
                safe_detail="mock malformed response",
            )
        if self.crash_after_accept:
            # Simulate acceptance then raise
            self._create_mock_orders(plan)
            raise RuntimeError("mock crash after acceptance")

        if self.return_empty_response:
            return SubmissionResult(
                verdict="OUTCOME_UNKNOWN",
                error_type="EmptyResponse",
                safe_detail="mock empty response",
            )
        if len(self.bars) < 2:
            raise ValueError("MockBroker needs at least two bars for next-open fill")

        if self.definitive_rejection:
            return SubmissionResult(
                verdict="DEFINITIVE_REJECTION",
                rejection_reasons={"ENTRY": "mock rejection", "SL": "mock rejection"},
                safe_detail="all orders rejected",
            )

        orders = self._create_mock_orders(plan)

        if self.post_send_timeout:
            return SubmissionResult(
                verdict="OUTCOME_UNKNOWN",
                error_type="TimeoutError",
                safe_detail="mock post-send timeout",
            )

        if self.mixed_response:
            # Return verified success for entry but mark SL as rejected
            return SubmissionResult(
                verdict="OUTCOME_UNKNOWN",
                verified_orders={"entry": orders["entry"]},
                rejection_reasons={"SL": "mock partial rejection"},
                safe_detail="mixed accepted/rejected",
            )

        if self.wrong_cloids:
            wrong = dict(orders)
            wrong["entry"]["cloid"] = "wrong-cloid-xxx"
            return SubmissionResult(
                verdict="OUTCOME_UNKNOWN",
                verified_orders=wrong,
                safe_detail="wrong cloids",
            )

        if self.missing_roles:
            partial = {"entry": orders["entry"]}
            return SubmissionResult(
                verdict="OUTCOME_UNKNOWN",
                verified_orders=partial,
                safe_detail="missing sl role",
            )

        if self.extra_roles:
            extra = dict(orders)
            extra["EXTRA"] = {"cloid": "extra-cloid", "role": "EXTRA", "status": "OPEN", "qty": plan.qty}
            return SubmissionResult(
                verdict="OUTCOME_UNKNOWN",
                verified_orders=extra,
                safe_detail="extra role",
            )

        return SubmissionResult(
            verdict="VERIFIED_SUCCESS",
            verified_orders=orders,
        )

    def _create_mock_orders(self, plan: OrderPlan) -> dict[str, dict]:
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

    # --- TS-P1-003 recovery evidence ---

    async def query_order_by_cloid(self, cloid: str) -> dict[str, Any] | None:
        """Direct cloid lookup. Raises if recovery_query_should_fail is set."""
        if self.recovery_query_should_fail:
            raise RuntimeError("mock query failure")
        for order in self.orders:
            if order["cloid"] == cloid:
                return dict(order)
        return None

    async def historical_orders(self, coin: str, since_ts: str) -> list[dict[str, Any]]:
        """Historical orders. Raises if recovery_query_should_fail is set."""
        if self.recovery_query_should_fail:
            raise RuntimeError("mock historical query failure")
        return [dict(o) for o in self.orders
                if o.get("symbol", self.coin) == coin]

    async def user_fills(self, coin: str, since_ts: str) -> list[dict[str, Any]]:
        """User fills. Raises if recovery_query_should_fail is set."""
        if self.recovery_query_should_fail:
            raise RuntimeError("mock fills query failure")
        return [dict(f) for f in self.fills
                if f.get("role", "") != "UNKNOWN"]

    def get_planned_cloids(self, plan: OrderPlan) -> dict[str, str]:
        """Return deterministic role→cloid map without broker I/O."""
        decision_uid = plan.decision_uid or "mock-no-duid"
        roles = {"entry": f"{decision_uid}:ENTRY", "sl": f"{decision_uid}:SL"}
        if plan.take_profit is not None:
            roles["tp"] = f"{decision_uid}:TP"
        return roles

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
