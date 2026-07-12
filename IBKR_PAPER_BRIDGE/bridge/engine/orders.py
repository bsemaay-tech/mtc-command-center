"""OrderManager for bracket submission, reconciliation, and fill tracking."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from bridge.broker.base import Broker
from bridge.engine.types import OrderPlan
from bridge.store.db import Store


class OrderManager:
    def __init__(self, store: Store, broker: Broker, run_id: str) -> None:
        self.store = store
        self.broker = broker
        self.run_id = run_id
        self._submitted: set[str] = set()
        self._synced_fills: set[str] = set()

    async def submit_plan(self, decision_uid: str, plan: OrderPlan) -> dict[str, Any] | None:
        if decision_uid in self._submitted:
            return None
        fingerprint = self._fingerprint(plan)
        if not self.store.claim_signal_fingerprint(self.run_id, fingerprint, decision_uid, plan.signal.ts):
            return None

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
        plan.decision_uid = decision_uid
        result = await self.broker.place_bracket(plan)
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
        broker_orders = getattr(self.broker, "orders", [])
        for order in broker_orders:
            stored = self.store.get_order(order["cloid"])
            if stored is None:
                continue
            self.store.update_order_status(
                order["cloid"],
                order["status"],
                filled_qty=order["qty"] if order["status"] == "FILLED" else None,
                avg_fill_px=order.get("avg_fill_px"),
            )

        broker_fills = getattr(self.broker, "fills", [])
        for fill in broker_fills:
            fill_id = str(fill.get("fill_id") or f"{fill['cloid']}:{fill.get('ts')}")
            if fill_id in self._synced_fills:
                continue
            order = self.store.get_order(fill["cloid"])
            if order is None:
                self._synced_fills.add(fill_id)
                continue
            self.store.insert_fill(
                fill_id=fill_id,
                cloid=fill["cloid"],
                decision_uid=order["decision_uid"],
                fill_ts=fill["ts"],
                qty=float(fill["qty"]),
                px=float(fill["px"]),
                fee=0.0,
                funding=0.0,
            )
            trade_id = order["trade_id"]
            if trade_id is not None and fill.get("role") == "ENTRY":
                self.store.update_trade_entry(int(trade_id), float(fill["px"]), fill["ts"])
            elif trade_id is not None and fill.get("role") in {"SL", "TP", "TRAIL", "CLOSE"}:
                trade = self.store.get_trade(int(trade_id))
                if trade is not None:
                    entry_px = float(trade["entry_px"] or trade["expected_px"])
                    direction = trade["direction"]
                    sign = 1 if direction == "LONG" else -1
                    pnl = (float(fill["px"]) - entry_px) * float(trade["qty"]) * sign
                    self.store.update_trade_exit(int(trade_id), float(fill["px"]), fill["ts"], str(fill["role"]), pnl)
                    self.store.insert_decision(
                        self.run_id,
                        order["decision_uid"],
                        fill["ts"],
                        trade["coin"],
                        "TRADE_CLOSED",
                        {"exit_reason": fill["role"], "pnl": pnl},
                        trade_id=int(trade_id),
                    )
            self._synced_fills.add(fill_id)

    async def reconcile(self) -> None:
        positions = await self.broker.positions()
        open_orders = await self.broker.open_orders()
        protected = {order.get("symbol") for order in open_orders if order.get("role") == "SL"}
        for position in positions:
            if position.symbol in protected:
                continue
            recovered = False
            reprotect = getattr(self.broker, "reprotect_position", None)
            if reprotect is not None:
                recovered = bool(await reprotect(position))
            if not recovered:
                await self.broker.flatten(position.symbol)
                self.store.insert_event(self.run_id, datetime.now(UTC), "WARN", "NAKED_POSITION_FLATTENED", position.symbol)

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
