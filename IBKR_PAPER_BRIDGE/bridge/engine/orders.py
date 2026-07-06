"""OrderManager for bracket submission, reconciliation, and fill tracking."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from bridge.broker.mock import MockBroker
from bridge.engine.types import OrderPlan
from bridge.store.db import Store


class OrderManager:
    def __init__(self, store: Store, broker: MockBroker, run_id: str) -> None:
        self.store = store
        self.broker = broker
        self.run_id = run_id
        self._submitted: set[str] = set()

    async def submit_plan(self, decision_uid: str, plan: OrderPlan) -> dict[str, Any] | None:
        if decision_uid in self._submitted:
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
                order_json=order,
                decision_uid=decision_uid,
                trade_id=trade_id,
                role=order["role"],
                status=order["status"],
                qty=order["qty"],
                filled_qty=order["qty"] if order["status"] == "FILLED" else 0.0,
                avg_fill_px=order.get("avg_fill_px"),
            )

        exit_order = result.get("exit")
        if isinstance(exit_order, dict) and exit_order.get("status") == "FILLED":
            entry_px = float(result["entry"]["avg_fill_px"])
            exit_px = float(exit_order["avg_fill_px"])
            sign = 1 if plan.signal.direction == "LONG" else -1
            pnl = (exit_px - entry_px) * plan.qty * sign
            self.store.update_trade_exit(
                trade_id,
                exit_px=exit_px,
                exit_ts=datetime.now(UTC),
                exit_reason=str(exit_order["role"]),
                pnl=pnl,
            )
        return result
