"""Deterministic mock broker for tests and dry-run mode.

TS-P1-003: configurable outcome injection, recovery evidence, and cloid plan.
"""

from __future__ import annotations

import csv
import asyncio
import itertools
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, UTC
from pathlib import Path
from typing import Callable

from bridge.broker.base import EvidenceVerdict, RecoveryEvidence, SubmissionOutcome
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

    # TS-P1-003 outcome injection
    _inject_pre_send_failure: bool = False
    _inject_timeout_after_accept: bool = False
    _inject_malformed_response: bool = False
    _inject_partial_response: bool = False
    _inject_wrong_cloid: bool = False
    _inject_extra_role: bool = False
    _inject_duplicate_role: bool = False
    _inject_mixed_accept_reject: bool = False
    _inject_definitive_rejection: bool = False
    _inject_crash_after_accept: bool = False  # signals "crash before local finalization"

    # TS-P1-003 recovery evidence injection
    _recovery_evidence: RecoveryEvidence | None = None
    _recovery_cycles_until_present: int = 0  # cycles until evidence flips to PRESENT
    _recovery_cycles_until_absent: int = 0  # cycles until evidence flips to ABSENT
    _recovery_cycle_count: int = field(default=0, init=False)
    _historical_cloids: dict[str, dict] = field(default_factory=dict)
    _fill_cloids: dict[str, list[dict]] = field(default_factory=dict)
    _query_failure: bool = False
    _truncated_coverage: bool = False
    _stale_coverage: bool = False

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

    # ------------------------------------------------------------------
    # TS-P1-003: cloid plan (pure broker-boundary method)
    # ------------------------------------------------------------------

    def compute_plan_cloids(self, decision_uid: str, roles: tuple[str, ...] = ("entry", "sl", "tp")) -> dict[str, str]:
        """Deterministic role→cloid map using blake2s (matches Hyperliquid adapter)."""
        result: dict[str, str] = {}
        for role in roles:
            raw = f"{decision_uid}:{role}"
            cloid = "0x" + hashlib.blake2s(raw.encode("utf-8"), digest_size=16).hexdigest()
            result[role.upper()] = cloid
        return result

    # ------------------------------------------------------------------
    # TS-P1-003: recovery evidence
    # ------------------------------------------------------------------

    async def recovery_evidence(
        self,
        planned_cloids: dict[str, str],
        attempt_start_ts: str | None,
    ) -> RecoveryEvidence:
        """Return typed recovery evidence (injectable for tests)."""
        self._recovery_cycle_count += 1

        # Always perform actual lookups first
        found_cloids: list[str] = []
        sources_checked: list[str] = ["direct_lookup", "open_orders", "historical", "fills"]
        sources_complete: list[str] = []
        reason_codes: list[str] = []
        ts_end = datetime.now(UTC).isoformat()

        for role, cloid in planned_cloids.items():
            if not cloid:
                continue
            try:
                result = await self.query_order_by_cloid(cloid, self.coin)
                if result is not None:
                    found_cloids.append(cloid)
            except Exception:
                reason_codes.append("DIRECT_LOOKUP_FAILED")
        sources_complete.append("direct_lookup")

        # Open orders
        try:
            open_orders = await self.open_orders()
            open_cloids = {o.cloid for o in open_orders if o.cloid}
            sources_complete.append("open_orders")
            for cloid in planned_cloids.values():
                if cloid in open_cloids and cloid not in found_cloids:
                    found_cloids.append(cloid)
        except Exception:
            reason_codes.append("OPEN_ORDERS_FAILED")

        sources_complete.append("historical")
        sources_complete.append("fills")

        # Override with injection flags
        if self._recovery_evidence is not None:
            return self._recovery_evidence

        if self._query_failure:
            return RecoveryEvidence(
                verdict=EvidenceVerdict.INCOMPLETE,
                planned_cloids=planned_cloids,
                sources_checked=sources_checked,
                sources_complete=[],
                reason_codes=["QUERY_FAILED"],
                ts_start=attempt_start_ts,
                ts_end=ts_end,
                attempt_window_covered=False,
            )

        if self._truncated_coverage:
            return RecoveryEvidence(
                verdict=EvidenceVerdict.INCOMPLETE,
                planned_cloids=planned_cloids,
                sources_checked=["direct_lookup", "open_orders"],
                sources_complete=["direct_lookup"],
                reason_codes=["COVERAGE_TRUNCATED"],
                ts_start=attempt_start_ts,
                ts_end=ts_end,
                attempt_window_covered=False,
            )

        if self._stale_coverage:
            return RecoveryEvidence(
                verdict=EvidenceVerdict.INCOMPLETE,
                planned_cloids=planned_cloids,
                sources_checked=sources_checked,
                sources_complete=sources_complete,
                reason_codes=["STALE_COVERAGE"],
                ts_start=attempt_start_ts,
                ts_end=ts_end,
                attempt_window_covered=False,
            )

        if self._recovery_cycles_until_present > 0:
            if self._recovery_cycle_count >= self._recovery_cycles_until_present:
                return RecoveryEvidence(
                    verdict=EvidenceVerdict.PRESENT,
                    planned_cloids=planned_cloids,
                    found_cloids=found_cloids or list(planned_cloids.values())[:1],
                    sources_checked=sources_checked,
                    sources_complete=sources_complete,
                    reason_codes=["DIRECT_LOOKUP_FOUND"],
                    ts_start=attempt_start_ts,
                    ts_end=ts_end,
                    attempt_window_covered=True,
                )
            return RecoveryEvidence(
                verdict=EvidenceVerdict.ABSENT_CANDIDATE,
                planned_cloids=planned_cloids,
                sources_checked=sources_checked,
                sources_complete=sources_complete,
                reason_codes=[],
                ts_start=attempt_start_ts,
                ts_end=ts_end,
                attempt_window_covered=True,
            )

        if self._recovery_cycles_until_absent > 0:
            if self._recovery_cycle_count >= self._recovery_cycles_until_absent:
                return RecoveryEvidence(
                    verdict=EvidenceVerdict.ABSENT_CANDIDATE,
                    planned_cloids=planned_cloids,
                    sources_checked=sources_checked,
                    sources_complete=sources_complete,
                    reason_codes=[],
                    ts_start=attempt_start_ts,
                    ts_end=ts_end,
                    attempt_window_covered=True,
                )
            return RecoveryEvidence(
                verdict=EvidenceVerdict.INCOMPLETE,
                planned_cloids=planned_cloids,
                sources_checked=["direct_lookup", "open_orders"],
                sources_complete=["direct_lookup"],
                reason_codes=["WAITING_FOR_VISIBILITY"],
                ts_start=attempt_start_ts,
                ts_end=ts_end,
                attempt_window_covered=False,
            )

        # Determine verdict from actual lookups
        if found_cloids:
            verdict = EvidenceVerdict.PRESENT
        elif len(sources_complete) < len(sources_checked):
            verdict = EvidenceVerdict.INCOMPLETE
        elif reason_codes:
            verdict = EvidenceVerdict.INCOMPLETE
        else:
            verdict = EvidenceVerdict.ABSENT_CANDIDATE

        return RecoveryEvidence(
            verdict=verdict,
            planned_cloids=planned_cloids,
            found_cloids=found_cloids,
            sources_checked=sources_checked,
            sources_complete=sources_complete,
            reason_codes=reason_codes,
            ts_start=attempt_start_ts,
            ts_end=ts_end,
            attempt_window_covered=len(sources_complete) == len(sources_checked),
        )

    async def query_order_by_cloid(self, cloid: str, coin: str) -> dict | None:
        """Direct cloid lookup against stored mock orders."""
        for order in self.orders:
            if order.get("cloid") == cloid:
                return dict(order)
        if cloid in self._historical_cloids:
            return dict(self._historical_cloids[cloid])
        return None

    async def historical_orders(self, coin: str, since_ts: str | None) -> list[dict]:
        """Historical order snapshot from stored mock orders."""
        result: list[dict] = []
        for order in self.orders:
            if order.get("symbol", self.coin) == coin:
                result.append(dict(order))
        for cloid, order in self._historical_cloids.items():
            result.append(dict(order))
        return result

    async def user_fills_by_time(self, coin: str, since_ts: str | None) -> list[dict]:
        """Fill history covering the attempt window."""
        result: list[dict] = []
        for fill in self.fills:
            result.append(dict(fill))
        for fills_list in self._fill_cloids.values():
            for fill in fills_list:
                result.append(dict(fill))
        return result

    # ------------------------------------------------------------------
    # place_bracket with outcome injection
    # ------------------------------------------------------------------

    async def place_bracket(self, plan: OrderPlan) -> dict:
        if not self.connected:
            raise RuntimeError("MockBroker is not connected")
        if len(self.bars) < 2:
            raise ValueError("MockBroker needs at least two bars for next-open fill")

        if self._inject_pre_send_failure:
            raise RuntimeError("PRE_SEND_FAILURE: validation before send")

        if self._inject_definitive_rejection:
            raise RuntimeError("DEFINITIVE_REJECTION: all orders rejected by exchange")

        # Use planned cloids from broker boundary
        duid = plan.decision_uid or f"mock-{next(self._ids)}"
        planned_cloids = self.compute_plan_cloids(duid)

        entry_cloid = planned_cloids.get("ENTRY", f"mock-entry-{next(self._ids)}")
        sl_cloid = planned_cloids.get("SL", f"mock-sl-{next(self._ids)}")
        tp_cloid = planned_cloids.get("TP", f"mock-tp-{next(self._ids)}")

        entry = self._order(
            "ENTRY", "OPEN", plan.qty, plan.signal.ref_price,
            reduce_only=False, signal_ts=plan.signal.ts,
            direction=plan.signal.direction, symbol=plan.signal.symbol,
            leverage=plan.leverage, cloid=entry_cloid,
        )
        sl = self._order(
            "SL", "OPEN", plan.qty, plan.stop_loss,
            reduce_only=True, trigger_px=plan.stop_loss,
            direction=plan.signal.direction, symbol=plan.signal.symbol,
            cloid=sl_cloid,
        )
        result = {"entry": entry, "sl": sl}
        if plan.take_profit is not None:
            result["tp"] = self._order(
                "TP", "OPEN", plan.qty, plan.take_profit,
                reduce_only=True, trigger_px=plan.take_profit,
                direction=plan.signal.direction, symbol=plan.signal.symbol,
                cloid=tp_cloid,
            )

        if self._inject_timeout_after_accept:
            raise TimeoutError("OUTCOME_UNKNOWN: timeout after exchange acceptance")

        if self._inject_malformed_response:
            return {"unexpected": object()}

        if self._inject_partial_response:
            return {"entry": entry}

        if self._inject_wrong_cloid:
            wrong_entry = dict(entry)
            wrong_entry["cloid"] = "0xWRONGCLOID000000000000000000000"
            return {"entry": wrong_entry, "sl": sl}

        if self._inject_extra_role:
            extra = self._order("EXTRA", "OPEN", plan.qty, plan.signal.ref_price,
                                reduce_only=False, direction=plan.signal.direction,
                                symbol=plan.signal.symbol)
            result["extra"] = extra
            return result

        if self._inject_duplicate_role:
            result["entry2"] = dict(entry)
            return result

        if self._inject_mixed_accept_reject:
            sl["status"] = "REJECTED"
            return result

        if self._inject_crash_after_accept:
            raise RuntimeError("OUTCOME_UNKNOWN: crash after exchange acceptance")

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
