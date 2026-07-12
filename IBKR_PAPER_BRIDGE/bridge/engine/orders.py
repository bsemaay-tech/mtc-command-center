"""OrderManager for bracket submission, reconciliation, and fill tracking."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from bridge.broker.base import Broker
from bridge.engine.types import BrokerEvent, FillEvent, OrderPlan, OrderUpdateEvent, Position
from bridge.store.db import Store


class OrderManager:
    def __init__(self, store: Store, broker: Broker, run_id: str, pending_grace_s: float = 120.0) -> None:
        self.store = store
        self.broker = broker
        self.run_id = run_id
        self._submitted: set[str] = set()
        self._synced_fills: set[str] = set()
        self._queued_events: list[BrokerEvent] = []
        self.pending_grace_s = pending_grace_s
        subscribe = getattr(self.broker, "subscribe_user_events", None)
        if subscribe is not None:
            subscribe(self._queue_event)

    async def submit_plan(self, decision_uid: str, plan: OrderPlan) -> dict[str, Any] | None:
        if decision_uid in self._submitted:
            return None
        fingerprint = self._fingerprint(plan)
        if not self.store.claim_signal_fingerprint(self.run_id, fingerprint, decision_uid, plan.signal.ts):
            return None

        plan.decision_uid = decision_uid
        result = await self.broker.place_bracket(plan)
        trade_id = self.store.create_trade(
            run_id=self.run_id,
            coin=plan.signal.symbol,
            direction=plan.signal.direction,
            qty=plan.qty,
            entry_decision_uid=decision_uid,
            signal_ts=plan.signal.ts,
            decision_ts=datetime.now(UTC),
            expected_px=plan.signal.ref_price,
            risk_dollars=plan.risk_dollars,
            risk_pct=plan.risk_pct,
            leverage=plan.leverage,
            sl_initial=plan.stop_loss,
            tp_initial=plan.take_profit,
            llm_directive_id=None,
        )
        self._submitted.add(decision_uid)

        for role, order in result.items():
            if not isinstance(order, dict):
                continue
            self.store.insert_order(
                cloid=order["cloid"],
                oid=order["oid"],
                group_id=decision_uid,
                order_ref=f"{decision_uid}:{role.upper()}",
                order_json=self._jsonable_order(order),
                decision_uid=decision_uid,
                trade_id=trade_id,
                role=order["role"],
                status=order["status"],
                qty=order["qty"],
                filled_qty=order["qty"] if order["status"] == "FILLED" else 0.0,
                avg_fill_px=order.get("avg_fill_px"),
            )

        await self.sync_broker_state()
        return result

    async def sync_broker_state(self) -> None:
        pending: list[BrokerEvent] = []
        for event in self._queued_events:
            if not self._ingest_event(event):
                pending.append(event)
        self._queued_events = pending

        broker_orders = await self.broker.open_orders()
        for order in broker_orders:
            stored = self.store.get_order(order.cloid)
            if stored is None:
                continue
            self.store.update_order_status(
                order.cloid,
                order.status,
            )

    async def reconcile(self) -> None:
        positions = await self.broker.positions()
        open_orders = await self.broker.open_orders()
        protected = {order.coin for order in open_orders if order.role == "SL" and self.store.get_order(order.cloid)}
        for position in positions:
            if position.symbol in protected:
                continue
            trade = self.store.get_open_trade_for_coin(self.run_id, position.symbol)
            if trade is None:
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "WARN",
                    "FOREIGN_POSITION_IGNORED",
                    position.symbol,
                )
                continue
            if self._within_pending_grace(int(trade["trade_id"])):
                continue
            recovered = await self.broker.reprotect_position(
                position,
                float(trade["sl_initial"]),
                float(trade["tp_initial"]) if trade["tp_initial"] is not None else None,
                str(trade["entry_decision_uid"]),
            )
            if recovered:
                self._persist_reprotected(recovered, trade)
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "WARN",
                    "NAKED_POSITION_REPROTECTED",
                    position.symbol,
                )
            else:
                await self.broker.flatten(position.symbol)
                self.store.insert_event(self.run_id, datetime.now(UTC), "WARN", "NAKED_POSITION_FLATTENED", position.symbol)
        account = await self.broker.account()
        self.store.insert_equity(
            self.run_id,
            datetime.now(UTC),
            equity=account.equity,
            cash=account.available_margin,
            unrealized=sum(position.unrealized for position in positions),
            realized_today=0.0,
        )

    async def trail_position(self, position: Position, new_stop: float) -> bool:
        trade = self.store.get_open_trade_for_coin(self.run_id, position.symbol)
        if trade is None:
            return False
        orders = await self.broker.open_orders()
        stop = next(
            (
                order
                for order in orders
                if order.coin == position.symbol
                and order.role == "SL"
                and self.store.get_order(order.cloid) is not None
            ),
            None,
        )
        if stop is None:
            return False
        if stop.trigger_px is not None:
            if position.size > 0 and new_stop <= stop.trigger_px:
                return False
            if position.size < 0 and new_stop >= stop.trigger_px:
                return False
        await self.broker.modify_stop(stop.cloid, new_stop)
        self.store.insert_event(
            self.run_id,
            datetime.now(UTC),
            "INFO",
            "TRAIL_MODIFIED",
            f"{position.symbol}:{new_stop}",
        )
        return True

    async def close_position(self, position: Position) -> None:
        for order in await self.broker.open_orders():
            if order.coin != position.symbol or order.role not in {"SL", "TP"}:
                continue
            if self.store.get_order(order.cloid) is not None:
                await self.broker.cancel(order.cloid)
        await self.broker.flatten(position.symbol)
        await self.sync_broker_state()

    def _queue_event(self, event: BrokerEvent) -> None:
        self._queued_events.append(event)

    def _ingest_event(self, event: BrokerEvent) -> bool:
        if isinstance(event, OrderUpdateEvent):
            if self.store.get_order(event.cloid) is None:
                return False
            self.store.update_order_status(
                event.cloid,
                event.status,
                filled_qty=event.filled_qty,
                avg_fill_px=event.avg_fill_px,
                ts_last=event.ts,
            )
            return True
        if isinstance(event, FillEvent):
            return self._ingest_fill(event)
        return True

    def _ingest_fill(self, fill: FillEvent) -> bool:
        if fill.fill_id in self._synced_fills:
            return True
        order = self.store.get_order(fill.cloid)
        if order is None:
            return False
        role = fill.role if fill.role != "UNKNOWN" else order["role"]
        self.store.insert_fill(
            fill_id=fill.fill_id,
            cloid=fill.cloid,
            decision_uid=order["decision_uid"],
            fill_ts=fill.ts,
            qty=fill.qty,
            px=fill.px,
            fee=fill.fee,
            funding=fill.funding,
        )
        self.store.update_order_status(
            fill.cloid,
            "FILLED",
            filled_qty=fill.qty,
            avg_fill_px=fill.px,
            ts_last=fill.ts,
        )
        trade_id = order["trade_id"]
        if trade_id is not None and role == "ENTRY":
            self.store.update_trade_entry(int(trade_id), fill.px, fill.ts)
        elif trade_id is not None and role in {"SL", "TP", "TRAIL", "CLOSE"}:
            trade = self.store.get_trade(int(trade_id))
            if trade is not None:
                entry_px = float(trade["entry_px"] or trade["expected_px"])
                sign = 1 if trade["direction"] == "LONG" else -1
                pnl = (fill.px - entry_px) * float(trade["qty"]) * sign
                self.store.update_trade_exit(int(trade_id), fill.px, fill.ts, role, pnl)
                self.store.insert_decision(
                    self.run_id,
                    order["decision_uid"],
                    fill.ts,
                    trade["coin"],
                    "TRADE_CLOSED",
                    {"exit_reason": role, "pnl": pnl},
                    trade_id=int(trade_id),
                )
        self._synced_fills.add(fill.fill_id)
        return True

    def _within_pending_grace(self, trade_id: int) -> bool:
        now = datetime.now(UTC)
        for order in reversed(self.store.get_orders_for_trade(trade_id)):
            if order["role"] != "SL" or order["status"] not in {"SUBMITTED", "OPEN"}:
                continue
            submitted = datetime.fromisoformat(order["ts_submit"])
            if submitted.tzinfo is None:
                submitted = submitted.replace(tzinfo=UTC)
            return (now - submitted).total_seconds() < self.pending_grace_s
        return False

    def _persist_reprotected(self, recovered: dict[str, Any], trade: dict[str, Any]) -> None:
        for role, order in recovered.items():
            if not isinstance(order, dict):
                continue
            self.store.insert_order(
                cloid=order["cloid"],
                oid=order.get("oid"),
                group_id=str(trade["entry_decision_uid"]),
                order_ref=f"{trade['entry_decision_uid']}:{role.upper()}:REPROTECT",
                order_json=self._jsonable_order(order),
                decision_uid=str(trade["entry_decision_uid"]),
                trade_id=int(trade["trade_id"]),
                role=order["role"],
                status=order["status"],
                qty=float(order["qty"]),
            )

    @staticmethod
    def _fingerprint(plan: OrderPlan) -> str:
        return f"{plan.signal.symbol}:{plan.signal.direction}:{plan.signal.ts.isoformat()}"

    @staticmethod
    def _jsonable_order(order: dict[str, Any]) -> dict[str, Any]:
        clean: dict[str, Any] = {}
        for key, value in order.items():
            if isinstance(value, datetime):
                clean[key] = value.isoformat()
            else:
                clean[key] = value
        return clean
