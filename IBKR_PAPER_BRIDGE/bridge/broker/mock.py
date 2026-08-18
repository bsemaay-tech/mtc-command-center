"""Deterministic mock broker for tests and dry-run mode."""

from __future__ import annotations

import csv
import asyncio
import itertools
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

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

_LIVE_STATUSES = frozenset({"SUBMITTED", "OPEN", "PENDING"})


@dataclass
class ScriptedOutcome:
    """One forced broker verdict, with the exchange effect stated separately.

    ``outcome`` is what the adapter *reports*; ``applied`` is what actually
    happened on the exchange. The two are deliberately independent so tests can
    build the dangerous cases — reported UNKNOWN but really applied, reported
    UNKNOWN and really not applied — that a real transport failure produces.
    """

    outcome: ActionOutcome
    applied: bool = True
    reason_code: str = "MOCK_SCRIPTED"


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

    # --- TS-P1-004 partial-recovery surface (defaults = healthy exchange) ---
    partial_size_decimals: int | None = 3
    partial_snapshot_exact: bool = True
    partial_snapshot_available: bool = True
    partial_query_available: bool = True
    partial_foreign_orders: list[dict] = field(default_factory=list)
    partial_extra_position: float = 0.0
    scripted_place: list[ScriptedOutcome] = field(default_factory=list)
    scripted_cancel: list[ScriptedOutcome] = field(default_factory=list)
    scripted_flatten: list[ScriptedOutcome] = field(default_factory=list)
    late_entry_fill_on_cancel: float = 0.0
    partial_calls: list[tuple[str, str]] = field(default_factory=list)

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

    def planned_cloids(self, plan: OrderPlan) -> dict[str, str]:
        seed = plan.decision_uid or (
            f"{plan.signal.symbol}:{plan.signal.ts.isoformat()}:{plan.signal.direction}"
        )
        roles = ["ENTRY", "SL"]
        if plan.take_profit is not None:
            roles.append("TP")
        return {role: f"{seed}:{role}" for role in roles}

    async def place_bracket(self, plan: OrderPlan) -> SubmissionOutcome:
        if not self.connected:
            raise BrokerPreSendFailure("MOCK_NOT_CONNECTED")
        if len(self.bars) < 2:
            raise BrokerPreSendFailure("MOCK_BARS_UNAVAILABLE")

        cloids = self.planned_cloids(plan)
        write_started = False
        try:
            write_started = True
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
                cloid=cloids["ENTRY"],
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
                cloid=cloids["SL"],
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
                    cloid=cloids["TP"],
                )
        except Exception as exc:
            if write_started:
                raise BrokerOutcomeUnknown("MOCK_POST_WRITE_FAILURE") from exc
            raise BrokerPreSendFailure("MOCK_PRE_SEND_FAILURE") from exc
        return SubmissionOutcome(
            SubmissionDisposition.VERIFIED_SUCCESS,
            result,
            "MOCK_VERIFIED_SUCCESS",
        )

    async def submission_recovery_evidence(
        self, request: SubmissionRecoveryRequest
    ) -> SubmissionRecoveryEvidence:
        planned = set(map(str, request.planned_cloids.values()))
        order_cloids = {
            str(order.get("cloid")) for order in self.orders if order.get("cloid")
        }
        open_cloids = {
            str(order.get("cloid"))
            for order in self.orders
            if order.get("cloid")
            and order.get("status") in {"SUBMITTED", "OPEN"}
        }
        fill_cloids = {
            str(fill.get("cloid")) for fill in self.fills if fill.get("cloid")
        }

        def query(found: set[str]) -> RecoveryQueryEvidence:
            owned = tuple(sorted(found & planned))
            return RecoveryQueryEvidence(
                EvidenceStatus.FOUND if owned else EvidenceStatus.NOT_FOUND,
                owned,
                "MOCK_COMPLETE",
            )

        direct = {
            cloid: query({cloid} if cloid in order_cloids or cloid in fill_cloids else set())
            for cloid in sorted(planned)
        }
        position = RecoveryQueryEvidence(
            EvidenceStatus.FOUND
            if self.position is not None
            and self.position.symbol == request.symbol
            and self.position.size != 0
            else EvidenceStatus.NOT_FOUND,
            (),
            "MOCK_POSITION_COMPLETE",
        )
        return SubmissionRecoveryEvidence(
            request_id=request.request_id,
            planned_cloids=dict(request.planned_cloids),
            direct_lookup=direct,
            open_orders=query(open_cloids),
            historical_orders=query(order_cloids),
            fills=query(fill_cloids),
            position=position,
        )

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

    # ------------------------------------------------------------------
    # TS-P1-004 typed, bounded partial-recovery surface
    # ------------------------------------------------------------------

    def lot_unit(self, symbol: str) -> LotUnit | None:
        if self.partial_size_decimals is None:
            return None
        try:
            return LotUnit(int(self.partial_size_decimals))
        except LotQuantizationError:
            return None

    @property
    def broker_mutations(self) -> list[tuple[str, str]]:
        """Only the calls that can change exchange state."""
        return [
            call
            for call in self.partial_calls
            if call[0] in {"cancel_order_by_cloid", "place_protective_stop", "flatten_reduce_only"}
        ]

    async def symbol_snapshot(self, symbol: str) -> SymbolSnapshot:
        self.partial_calls.append(("symbol_snapshot", symbol))
        lot = self.lot_unit(symbol)
        if not self.partial_snapshot_available:
            return SymbolSnapshot(
                symbol=symbol,
                exact=False,
                net_size=None,
                open_orders=(),
                lot=lot,
                evidence=Evidence("SNAPSHOT", "MOCK_SNAPSHOT_UNAVAILABLE"),
            )
        net = 0.0
        if self.position is not None and self.position.symbol == symbol:
            net = float(self.position.size)
        net += float(self.partial_extra_position)
        views: list[OrderView] = []
        for order in self.orders:
            if str(order.get("status")) not in _LIVE_STATUSES:
                continue
            if str(order.get("symbol", self.coin)) != symbol:
                continue
            views.append(self._order_view(order))
        for foreign in self.partial_foreign_orders:
            if str(foreign.get("symbol", self.coin)) != symbol:
                continue
            views.append(self._order_view(foreign))
        return SymbolSnapshot(
            symbol=symbol,
            exact=bool(self.partial_snapshot_exact and lot is not None),
            net_size=net,
            open_orders=tuple(views),
            lot=lot,
            evidence=Evidence("SNAPSHOT", "MOCK_SNAPSHOT_COMPLETE"),
            observed_ts=datetime.now(),
        )

    def _order_view(self, order: dict) -> OrderView:
        direction = str(order.get("direction", "LONG"))
        role = str(order.get("role", "UNKNOWN"))
        is_entry = role == "ENTRY"
        is_buy = (direction == "LONG") if is_entry else (direction == "SHORT")
        return OrderView(
            cloid=str(order.get("cloid", "")),
            coin=str(order.get("symbol", self.coin)),
            side="BUY" if is_buy else "SELL",
            size=float(order.get("qty", 0.0)),
            role=role,
            reduce_only=bool(order.get("reduce_only", False)),
            trigger_px=order.get("trigger_px"),
            status=str(order.get("status", "OPEN")),
            order_ref=order.get("order_ref"),
        )

    def _find_order(self, cloid: str) -> dict | None:
        for order in self.orders:
            if str(order.get("cloid")) == str(cloid):
                return order
        for order in self.partial_foreign_orders:
            if str(order.get("cloid")) == str(cloid):
                return order
        return None

    async def query_order(self, cloid: str, symbol: str) -> OrderQueryResult:
        self.partial_calls.append(("query_order", str(cloid)))
        if not self.partial_query_available:
            return OrderQueryResult(
                known=False,
                evidence=Evidence("QUERY_ORDER", "MOCK_QUERY_UNAVAILABLE"),
            )
        order = self._find_order(cloid)
        if order is None:
            return OrderQueryResult(
                known=True,
                found=False,
                terminal=True,
                evidence=Evidence("QUERY_ORDER", "MOCK_ORDER_ABSENT"),
            )
        status = str(order.get("status", "OPEN"))
        filled = sum(
            float(fill["qty"]) for fill in self.fills if str(fill["cloid"]) == str(cloid)
        )
        return OrderQueryResult(
            known=True,
            found=status in _LIVE_STATUSES,
            terminal=status not in _LIVE_STATUSES,
            raw_status=status,
            filled_size=filled,
            evidence=Evidence("QUERY_ORDER", "MOCK_ORDER_FOUND"),
        )

    @staticmethod
    def _next_script(script: list[ScriptedOutcome]) -> ScriptedOutcome | None:
        return script.pop(0) if script else None

    async def cancel_order_by_cloid(self, cloid: str, symbol: str) -> CancelResult:
        self.partial_calls.append(("cancel_order_by_cloid", str(cloid)))
        if self.late_entry_fill_on_cancel:
            self._apply_late_entry_fill(str(cloid))
        script = self._next_script(self.scripted_cancel)
        order = self._find_order(cloid)
        if script is not None:
            if script.applied and order is not None and str(order.get("status")) in _LIVE_STATUSES:
                order["status"] = "CANCELLED_BY_ENGINE"
                self._emit_order_update(order)
            return CancelResult(
                script.outcome, str(cloid), Evidence("CANCEL", script.reason_code)
            )
        if order is None:
            return CancelResult(
                ActionOutcome.NOT_APPLIED, str(cloid),
                Evidence("CANCEL", "MOCK_ORDER_ABSENT"),
            )
        if str(order.get("status")) not in _LIVE_STATUSES:
            return CancelResult(
                ActionOutcome.NOT_APPLIED, str(cloid),
                Evidence("CANCEL", "MOCK_ORDER_ALREADY_TERMINAL"),
            )
        order["status"] = "CANCELLED_BY_ENGINE"
        self._emit_order_update(order)
        return CancelResult(
            ActionOutcome.APPLIED, str(cloid), Evidence("CANCEL", "MOCK_CANCEL_OK")
        )

    def _apply_late_entry_fill(self, cancel_cloid: str) -> None:
        """Simulate a fill that lands between the cancel request and its ack."""
        qty = float(self.late_entry_fill_on_cancel)
        self.late_entry_fill_on_cancel = 0.0
        order = self._find_order(cancel_cloid)
        if order is None or str(order.get("role")) != "ENTRY":
            return
        px = self._last_price()
        direction = str(order.get("direction", "LONG"))
        side = 1 if direction == "LONG" else -1
        symbol = str(order.get("symbol", self.coin))
        if self.position is None:
            self.position = Position(
                symbol=symbol, size=qty * side, entry_px=px, unrealized=0.0
            )
        else:
            self.position = self.position.model_copy(
                update={"size": self.position.size + qty * side}
            )
        self._record_fill(order, qty, px, datetime.now())

    async def place_protective_stop(
        self,
        *,
        symbol: str,
        cloid: str,
        exit_side: str,
        size: float,
        trigger_px: float,
    ) -> PlaceResult:
        self.partial_calls.append(("place_protective_stop", str(cloid)))
        script = self._next_script(self.scripted_place)
        direction = "LONG" if str(exit_side).upper() == "SELL" else "SHORT"
        if script is not None:
            if script.applied:
                self._install_stop(symbol, cloid, direction, size, trigger_px)
            return PlaceResult(
                script.outcome, str(cloid), None, Evidence("PLACE", script.reason_code)
            )
        order = self._install_stop(symbol, cloid, direction, size, trigger_px)
        return PlaceResult(
            ActionOutcome.APPLIED,
            str(cloid),
            int(order["oid"]),
            Evidence("PLACE", "MOCK_PLACE_OK"),
        )

    def _install_stop(
        self, symbol: str, cloid: str, direction: str, size: float, trigger_px: float
    ) -> dict:
        existing = self._find_order(cloid)
        if existing is not None:
            existing["status"] = "OPEN"
            existing["qty"] = float(size)
            existing["trigger_px"] = float(trigger_px)
            return existing
        return self._order(
            "SL",
            "OPEN",
            float(size),
            float(trigger_px),
            reduce_only=True,
            trigger_px=float(trigger_px),
            direction=direction,
            symbol=symbol,
            cloid=str(cloid),
        )

    async def flatten_reduce_only(
        self, *, symbol: str, cloid: str, size: float
    ) -> FlattenResult:
        self.partial_calls.append(("flatten_reduce_only", str(cloid)))
        script = self._next_script(self.scripted_flatten)
        if script is not None:
            if script.applied:
                self._reduce_position(symbol, size, cloid)
            return FlattenResult(
                script.outcome, str(cloid), Evidence("FLATTEN", script.reason_code)
            )
        self._reduce_position(symbol, size, cloid)
        return FlattenResult(
            ActionOutcome.APPLIED, str(cloid), Evidence("FLATTEN", "MOCK_FLATTEN_OK")
        )

    def _reduce_position(self, symbol: str, size: float, cloid: str) -> None:
        if self.position is None or self.position.symbol != symbol:
            return
        px = self._last_price()
        current = float(self.position.size)
        reduce_by = min(abs(current), abs(float(size)))
        close = self._order(
            "CLOSE", "FILLED", reduce_by, px, reduce_only=True, symbol=symbol,
            cloid=str(cloid),
        )
        self._record_fill(close, reduce_by, px, datetime.now())
        remaining = current - reduce_by if current > 0 else current + reduce_by
        self.position = (
            None
            if remaining == 0
            else self.position.model_copy(update={"size": remaining})
        )

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
