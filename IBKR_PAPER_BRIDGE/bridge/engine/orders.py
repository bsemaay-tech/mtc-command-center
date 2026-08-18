"""OrderManager for bracket submission, reconciliation, and fill tracking.

TS-P1-003: submission-attempt lifecycle with SUBMITTING/UNKNOWN_SUBMISSION
quarantine, structured broker outcomes, and read-only recovery.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from bridge.broker.base import Broker, SubmissionOutcome
from bridge.engine.types import BrokerEvent, BrokerOrder, FillEvent, OrderPlan, OrderUpdateEvent, Position
from bridge.store.db import (
    IdentityCollisionError,
    OrderCollisionError,
    Store,
    compute_intent_identity,
    compute_request_identity,
)


class UnknownSubmissionError(Exception):
    """Raised when a submission outcome is OUTCOME_UNKNOWN."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


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

    # ------------------------------------------------------------------
    # TS-P1-002 identity-based submission
    # ------------------------------------------------------------------

    async def submit_plan(
        self, decision_uid: str, plan: OrderPlan, *, strategy_id: str = "keltner_trail_ema8"
    ) -> dict[str, Any] | None:
        """Submit an order plan with durable identity + submission-attempt lifecycle.

        TS-P1-003 additions:
        - Before broker I/O: obtain role→cloid plan from broker, persist SUBMITTING attempt
        - After broker I/O: handle structured outcomes (PRE_SEND_FAILURE,
          DEFINITIVE_REJECTION, VERIFIED_SUCCESS, OUTCOME_UNKNOWN)
        - Block all placements while any SUBMITTING, UNKNOWN_SUBMISSION, or
          CONFIRMED_PRESENT quarantine exists
        """

        # --- 0. Quarantine gate: block all new entries while active quarantine exists ---
        if hasattr(self.store, "has_active_quarantine") and self.store.has_active_quarantine():
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "WARN",
                "SUBMIT_BLOCKED_QUARANTINE",
                f"decision_uid={decision_uid}: active unknown-submission quarantine exists",
            )
            raise UnknownSubmissionError(
                "SUBMIT_BLOCKED_QUARANTINE",
                f"decision_uid={decision_uid}: active quarantine blocks new submissions",
            )

        if decision_uid in self._submitted:
            return None

        # --- 1. Compute dual identities ---
        intent_id, intent_preimage, intent_version = compute_intent_identity(
            strategy_id=strategy_id,
            symbol=plan.signal.symbol,
            direction=plan.signal.direction,
            signal_ts=plan.signal.ts,
        )
        request_id, request_preimage, request_version = compute_request_identity(
            intent_id=intent_id,
            symbol=plan.signal.symbol,
            direction=plan.signal.direction,
            ref_price=plan.signal.ref_price,
            qty=plan.qty,
            entry_type=plan.entry_type,
            limit_price=plan.limit_price,
            stop_loss=plan.stop_loss,
            take_profit=plan.take_profit,
            leverage=plan.leverage,
        )

        # --- 2. Obtain role→cloid plan from broker boundary (pure method) ---
        compute_cloids = getattr(self.broker, "compute_plan_cloids", None)
        if compute_cloids is not None:
            roles = ["entry", "sl"]
            if plan.take_profit is not None:
                roles.append("tp")
            planned_cloids = compute_cloids(request_id, tuple(roles))
        else:
            # Fallback: use request_id directly
            planned_cloids = {"ENTRY": f"{request_id}:ENTRY", "SL": f"{request_id}:SL"}
            if plan.take_profit is not None:
                planned_cloids["TP"] = f"{request_id}:TP"

        # --- 3. Durable reservation + submission attempt (single transaction) ---
        try:
            self.store.conn.execute("BEGIN IMMEDIATE")
        except Exception:
            raise

        try:
            result = self.store.reserve_identity(
                intent_id=intent_id,
                intent_preimage=intent_preimage,
                intent_version=intent_version,
                request_id=request_id,
                request_preimage=request_preimage,
                request_version=request_version,
                cloid_seed=request_id,
                origin_run_id=self.run_id,
                origin_decision_uid=decision_uid,
            )

            if result == "BLOCKED":
                self.store.conn.commit()
                return None  # idempotent replay, do not resubmit

            # Persist immutable submission attempt as SUBMITTING before broker I/O
            recovery_payload = {
                "intent_id": intent_id,
                "request_id": request_id,
                "decision_uid": decision_uid,
                "symbol": plan.signal.symbol,
                "direction": plan.signal.direction,
                "qty": plan.qty,
                "stop_loss": plan.stop_loss,
                "take_profit": plan.take_profit,
                "signal_ts": plan.signal.ts.isoformat(),
            }
            attempt_result = self.store.start_submission_attempt(
                request_id=request_id,
                intent_id=intent_id,
                planned_cloids=planned_cloids,
                recovery_payload=recovery_payload,
            )
            self.store.conn.commit()
        except IdentityCollisionError as exc:
            self.store.conn.rollback()
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                exc.code,
                f"intent_id={intent_id} request_id={request_id} decision_uid={decision_uid}",
            )
            raise
        except Exception:
            self.store.conn.rollback()
            raise

        # Reservation + SUBMITTING attempt now committed

        # --- 4. Set broker cloid seed and submit ---
        original_decision_uid = decision_uid
        plan.decision_uid = request_id
        broker_result = None
        outcome = None
        exc_info = None

        try:
            broker_result = await self.broker.place_bracket(plan)
        except Exception as exc:
            exc_info = exc
            exc_name = type(exc).__name__
            exc_msg = str(exc)[:500]

            # Determine outcome from exception
            if "PRE_SEND_FAILURE" in exc_msg:
                outcome = SubmissionOutcome.PRE_SEND_FAILURE
            elif "DEFINITIVE_REJECTION" in exc_msg:
                outcome = SubmissionOutcome.DEFINITIVE_REJECTION
            elif exc_name in {"TimeoutError", "ConnectionError"} or "OUTCOME_UNKNOWN" in exc_msg:
                outcome = SubmissionOutcome.OUTCOME_UNKNOWN
            else:
                # Any other exception after possible send → OUTCOME_UNKNOWN
                outcome = SubmissionOutcome.OUTCOME_UNKNOWN
        finally:
            plan.decision_uid = original_decision_uid

        # --- 5. Handle structured outcomes ---

        if outcome == SubmissionOutcome.PRE_SEND_FAILURE:
            # Adapter proved no exchange write started — safe to roll back
            self.store.transition_attempt_state(
                request_id, ["SUBMITTING"], "REJECTED", "PRE_SEND_FAILURE",
            )
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "PLACE_BRACKET_FAILED",
                f"decision_uid={original_decision_uid} intent_id={intent_id} "
                f"error_type={type(exc_info).__name__}",
            )
            raise exc_info

        if outcome == SubmissionOutcome.DEFINITIVE_REJECTION:
            self.store.transition_attempt_state(
                request_id, ["SUBMITTING"], "REJECTED", "DEFINITIVE_REJECTION",
            )
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "ORDER_DEFINITIVE_REJECTION",
                f"decision_uid={original_decision_uid} intent_id={intent_id}",
            )
            raise exc_info

        if outcome == SubmissionOutcome.OUTCOME_UNKNOWN or exc_info is not None:
            # Transition SUBMITTING → UNKNOWN_SUBMISSION atomically
            success = self.store.transition_attempt_state(
                request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION",
                f"OUTCOME_UNKNOWN:{type(exc_info).__name__}" if exc_info else "OUTCOME_UNKNOWN",
            )
            if not success:
                # SUBMITTING remains — still quarantined
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "UNKNOWN_TRANSITION_FAILED",
                    f"request_id={request_id}: SUBMITTING→UNKNOWN_SUBMISSION failed, "
                    f"quarantine preserved",
                )
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "OUTCOME_UNKNOWN",
                f"decision_uid={original_decision_uid} intent_id={intent_id} "
                f"request_id={request_id}",
            )
            raise UnknownSubmissionError(
                "OUTCOME_UNKNOWN",
                f"intent_id={intent_id}: submission outcome unknown, quarantined",
            )

        # --- 6. Validate broker_result ---
        verify_cloids = getattr(self.broker, "compute_plan_cloids", None) is not None
        if not isinstance(broker_result, dict) or not broker_result:
            if verify_cloids:
                self.store.transition_attempt_state(
                    request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "BROKER_RESULT_INVALID",
                )
                raise UnknownSubmissionError(
                    "BROKER_RESULT_INVALID",
                    f"intent_id={intent_id}: broker returned empty or non-mapping result",
                )
            else:
                self.store.insert_event(
                    self.run_id, datetime.now(UTC), "ERROR",
                    "BROKER_RESULT_INVALID",
                    f"decision_uid={original_decision_uid} intent_id={intent_id} "
                    f"type={type(broker_result).__name__}",
                )
                raise IdentityCollisionError(
                    "IDENTITY_BROKER_RESULT_INVALID",
                    f"intent_id={intent_id}: broker returned empty or non-mapping result",
                )

        # --- 7. Verify planned cloid/role coverage (only if broker supports it) ---
        roles_seen: set[str] = set()
        orders_data: list[dict[str, Any]] = []
        verify_cloids = getattr(self.broker, "compute_plan_cloids", None) is not None

        for role_key, order in broker_result.items():
            if not isinstance(order, dict):
                if verify_cloids:
                    self.store.transition_attempt_state(
                        request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "BROKER_ORDER_INVALID",
                    )
                    raise UnknownSubmissionError(
                        "BROKER_ORDER_INVALID",
                        f"intent_id={intent_id}: broker returned non-dict order for role={role_key}",
                    )
                else:
                    self.store.insert_event(
                        self.run_id, datetime.now(UTC), "ERROR",
                        "BROKER_ORDER_INVALID",
                        f"decision_uid={original_decision_uid} role={role_key} "
                        f"order_type={type(order).__name__}",
                    )
                    raise IdentityCollisionError(
                        "IDENTITY_BROKER_ORDER_INVALID",
                        f"intent_id={intent_id}: broker returned non-dict order for role={role_key}",
                    )

            missing = [k for k in ("cloid", "role", "status", "qty") if k not in order]
            if missing:
                if verify_cloids:
                    self.store.transition_attempt_state(
                        request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "BROKER_ORDER_MISSING_KEYS",
                    )
                    raise UnknownSubmissionError(
                        "BROKER_ORDER_MISSING_KEYS",
                        f"intent_id={intent_id}: order for role={role_key} missing keys: {','.join(missing)}",
                    )
                else:
                    self.store.insert_event(
                        self.run_id, datetime.now(UTC), "ERROR",
                        "BROKER_ORDER_MISSING_KEYS",
                        f"decision_uid={original_decision_uid} role={role_key} "
                        f"missing={','.join(missing)}",
                    )
                    raise IdentityCollisionError(
                        "IDENTITY_BROKER_ORDER_INVALID",
                        f"intent_id={intent_id}: broker order for role={role_key} "
                        f"missing keys: {','.join(missing)}",
                    )

            role = str(order["role"]).upper()
            cloid = str(order["cloid"])

            # Verify cloid matches planned (only when broker supports compute_plan_cloids)
            if verify_cloids and role in planned_cloids and cloid != planned_cloids[role]:
                self.store.transition_attempt_state(
                    request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "CLOID_MISMATCH",
                )
                raise UnknownSubmissionError(
                    "CLOID_MISMATCH",
                    f"intent_id={intent_id}: role={role} returned cloid={cloid} "
                    f"but planned={planned_cloids.get(role)}",
                )

            if verify_cloids and role in roles_seen:
                self.store.transition_attempt_state(
                    request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "DUPLICATE_ROLE",
                )
                raise UnknownSubmissionError(
                    "DUPLICATE_ROLE",
                    f"intent_id={intent_id}: duplicate role={role} in broker result",
                )
            roles_seen.add(role)

            orders_data.append({
                "cloid": cloid,
                "oid": order.get("oid"),
                "group_id": request_id,
                "order_ref": f"{request_id}:{role}",
                "order_json": self._jsonable_order(order),
                "decision_uid": original_decision_uid,
                "role": role,
                "status": order["status"],
                "qty": order["qty"],
                "filled_qty": order["qty"] if order["status"] == "FILLED" else 0.0,
                "avg_fill_px": order.get("avg_fill_px"),
            })

        # Check all planned roles are present (only when broker supports it)
        if verify_cloids:
            for planned_role in planned_cloids:
                if planned_role not in roles_seen:
                    self.store.transition_attempt_state(
                        request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "MISSING_ROLE",
                    )
                    raise UnknownSubmissionError(
                        "MISSING_ROLE",
                        f"intent_id={intent_id}: planned role={planned_role} not in broker result",
                    )

            # Check no extra roles
            for seen_role in roles_seen:
                if seen_role not in planned_cloids:
                    self.store.transition_attempt_state(
                        request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "EXTRA_ROLE",
                    )
                    raise UnknownSubmissionError(
                        "EXTRA_ROLE",
                        f"intent_id={intent_id}: unexpected role={seen_role} in broker result",
                    )

        if not orders_data:
            self.store.transition_attempt_state(
                request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "BROKER_ORDERS_EMPTY",
            )
            raise UnknownSubmissionError(
                "BROKER_ORDERS_EMPTY",
                f"intent_id={intent_id}: no valid orders in broker result",
            )

        # --- 8. Atomic finalization (VERIFIED_SUCCESS) ---
        try:
            trade_id = self.store.finalize_submission(
                intent_id=intent_id,
                request_id=request_id,
                run_id=self.run_id,
                coin=plan.signal.symbol,
                direction=plan.signal.direction,
                qty=plan.qty,
                entry_decision_uid=original_decision_uid,
                signal_ts=plan.signal.ts,
                decision_ts=datetime.now(UTC),
                expected_px=plan.signal.ref_price,
                risk_dollars=plan.risk_dollars,
                risk_pct=plan.risk_pct,
                leverage=plan.leverage,
                sl_initial=plan.stop_loss,
                tp_initial=plan.take_profit,
                llm_directive_id=None,
                orders_data=orders_data,
            )
        except (IdentityCollisionError, OrderCollisionError) as exc:
            # Finalization failed after broker success → UNKNOWN_SUBMISSION
            code = getattr(exc, 'code', 'FINALIZE_FAILED')
            self.store.transition_attempt_state(
                request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", code,
            )
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                code,
                f"intent_id={intent_id} decision_uid={original_decision_uid}",
            )
            raise UnknownSubmissionError(
                code,
                f"intent_id={intent_id}: finalization failed after broker, quarantined",
            )
        except Exception:
            self.store.transition_attempt_state(
                request_id, ["SUBMITTING"], "UNKNOWN_SUBMISSION", "FINALIZE_FAILED",
            )
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "IDENTITY_FINALIZE_FAILED",
                f"intent_id={intent_id} decision_uid={original_decision_uid}",
            )
            raise UnknownSubmissionError(
                "FINALIZE_FAILED",
                f"intent_id={intent_id}: finalization failed after broker, quarantined",
            )

        # Mark attempt FINALIZED
        self.store.transition_attempt_state(
            request_id, ["SUBMITTING"], "FINALIZED", "VERIFIED_SUCCESS",
        )

        self._submitted.add(original_decision_uid)
        await self.sync_broker_state()
        return broker_result

    # ------------------------------------------------------------------
    # Rest of OrderManager (TS-P1-001 behaviour preserved)
    # ------------------------------------------------------------------

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
        protected = {order.coin for order in open_orders if order.role == "SL" and self._match_order(order) is not None}
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
            try:
                recovered = await self.broker.reprotect_position(
                    position,
                    float(trade["sl_initial"]),
                    float(trade["tp_initial"]) if trade["tp_initial"] is not None else None,
                    str(trade["entry_decision_uid"]),
                )
            except Exception as exc:
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "REPROTECT_FAILED",
                    f"{position.symbol}: {type(exc).__name__}",
                )
                recovered = None
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
        try:
            realized_today = self.store.realized_pnl_today(self.run_id)
        except LookupError:
            realized_today = 0.0
        self.store.insert_equity(
            self.run_id,
            datetime.now(UTC),
            equity=account.equity,
            cash=account.available_margin,
            unrealized=sum(position.unrealized for position in positions),
            realized_today=realized_today,
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
                and self._match_order(order) is not None
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
            if self._match_order(order) is not None:
                await self.broker.cancel(order.cloid)
        await self.broker.flatten(position.symbol)
        await self.sync_broker_state()

    def _match_order(self, order: BrokerOrder) -> dict[str, Any] | None:
        """B2: match an exchange order to our DB (spec §6.5).

        Cascade: cloid → order_ref → conservative attributes
        (symbol+role+qty+trigger_px, live statuses only). An ambiguous
        attribute match emits RECON_AMBIGUOUS and returns None — the caller
        must not act on it.
        """
        if order.cloid:
            row = self.store.get_order(order.cloid)
            if row is not None:
                return row
        order_ref = getattr(order, "order_ref", None)
        if order_ref:
            row = self.store.get_order_by_ref(str(order_ref))
            if row is not None:
                return row
        role = getattr(order, "role", None)
        if role in {"SL", "TP", "ENTRY"}:
            candidates = self.store.find_live_orders_by_attributes(
                symbol=order.coin,
                role=str(role),
                qty=abs(order.size),
                trigger_px=getattr(order, "trigger_px", None),
            )
            if len(candidates) == 1:
                return candidates[0]
            if len(candidates) > 1:
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "WARN",
                    "RECON_AMBIGUOUS",
                    f"{order.coin}:{role}:{len(candidates)} candidates",
                )
        return None

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
        role = str(order["role"])
        if fill.role != "UNKNOWN" and fill.role != role:
            self._quarantine_fill(
                "FILL_ROLE_CONFLICT",
                fill,
                f"event_role={fill.role} stored_role={role} cloid={fill.cloid}",
            )
            self._synced_fills.add(fill.fill_id)
            return True

        trade_id = order["trade_id"]
        trade = self.store.get_trade(int(trade_id)) if trade_id is not None else None
        outcome = self.store.insert_fill(
            fill_id=fill.fill_id,
            cloid=fill.cloid,
            decision_uid=order["decision_uid"],
            fill_ts=fill.ts,
            qty=fill.qty,
            px=fill.px,
            fee=fill.fee,
            funding=fill.funding,
        )
        if outcome == "CONFLICT":
            self._quarantine_fill(
                "FILL_ID_CONFLICT",
                fill,
                f"immutable fill_id reused with different payload: {fill.fill_id}",
            )
            self._synced_fills.add(fill.fill_id)
            return True
        if trade is not None and trade["exit_ts"] is not None:
            if outcome == "EXACT_DUPLICATE":
                self._synced_fills.add(fill.fill_id)
                return True
            self._quarantine_fill(
                "POST_CLOSE_FILL",
                fill,
                f"trade_id={trade_id} role={role} canonical_exit_ts={trade['exit_ts']}",
            )
            self._synced_fills.add(fill.fill_id)
            return True

        # Cumulative order accounting: an order becomes FILLED only when its
        # persisted fills reach the ordered quantity; a partial fill keeps the
        # current status so pending/grace logic still sees a live order.
        order_filled_qty, order_vwap = self.store.order_fill_totals(fill.cloid)
        if order_filled_qty > float(order["qty"]) + 1e-9:
            self._quarantine_fill(
                "ORDER_OVERFILL",
                fill,
                f"cloid={fill.cloid} filled_qty={order_filled_qty} order_qty={order['qty']}",
            )
            self._synced_fills.add(fill.fill_id)
            return True
        order_complete = order_filled_qty >= float(order["qty"]) - 1e-9
        self.store.update_order_status(
            fill.cloid,
            "FILLED" if order_complete else str(order["status"]),
            filled_qty=order_filled_qty,
            avg_fill_px=order_vwap,
            ts_last=fill.ts,
        )
        if trade_id is not None and role == "ENTRY":
            totals = self.store.trade_fill_totals(int(trade_id))
            if totals["entry_qty"] > 0 and totals["entry_vwap"] is not None:
                self.store.update_trade_entry(
                    int(trade_id), float(totals["entry_vwap"]), str(totals["entry_first_ts"])
                )
        elif trade_id is not None and role in {"SL", "TP", "TRAIL", "CLOSE"}:
            trade = self.store.get_trade(int(trade_id))
            if trade is not None:
                totals = self.store.trade_fill_totals(int(trade_id))
                exit_qty = float(totals["exit_qty"])
                if totals["entry_qty"] > 0 and totals["entry_vwap"] is not None:
                    entry_qty = float(totals["entry_qty"])
                    entry_px = float(totals["entry_vwap"])
                else:
                    entry_qty = float(trade["qty"])
                    entry_px = float(trade["entry_px"] or trade["expected_px"])
                if exit_qty > entry_qty + 1e-9:
                    self._quarantine_fill(
                        "TRADE_OVERFILL",
                        fill,
                        f"trade_id={trade_id} exit_qty={exit_qty} entry_qty={entry_qty}",
                    )
                    self._synced_fills.add(fill.fill_id)
                    return True
                if exit_qty >= entry_qty - 1e-9:
                    if self.store.has_live_entry_remainder(int(trade_id)):
                        if outcome == "INSERTED":
                            self.store.insert_decision(
                                self.run_id,
                                order["decision_uid"],
                                fill.ts,
                                trade["coin"],
                                "TRADE_PARTIAL_EXIT",
                                {
                                    "exit_reason": role,
                                    "exit_qty": exit_qty,
                                    "entry_qty": entry_qty,
                                    "entry_remainder_live": True,
                                },
                                trade_id=int(trade_id),
                            )
                            self._quarantine_fill(
                                "ENTRY_REMAINDER_LIVE",
                                fill,
                                f"trade_id={trade_id} flat_qty={exit_qty} owned entry remainder can still fill",
                            )
                        self._synced_fills.add(fill.fill_id)
                        return True
                    exit_vwap = float(totals["exit_vwap"])
                    sign = 1 if trade["direction"] == "LONG" else -1
                    gross = (exit_vwap - entry_px) * entry_qty * sign
                    costs = self.store.trade_costs(str(order["decision_uid"]))
                    pnl = gross - costs
                    closed = self.store.close_trade_once_with_decision(
                        trade_id=int(trade_id),
                        run_id=self.run_id,
                        decision_uid=str(order["decision_uid"]),
                        coin=str(trade["coin"]),
                        exit_px=exit_vwap,
                        exit_ts=fill.ts,
                        exit_reason=role,
                        pnl=pnl,
                        payload={
                            "exit_reason": role,
                            "pnl": pnl,
                            "pnl_gross": gross,
                            "costs": costs,
                            "entry_basis_px": entry_px,
                            "exit_vwap": exit_vwap,
                            "qty": entry_qty,
                        },
                    )
                    if not closed:
                        self._quarantine_fill(
                            "TRADE_CLOSE_RACE",
                            fill,
                            f"trade_id={trade_id} was closed before atomic close",
                        )
                elif outcome == "INSERTED":
                    self.store.insert_decision(
                        self.run_id,
                        order["decision_uid"],
                        fill.ts,
                        trade["coin"],
                        "TRADE_PARTIAL_EXIT",
                        {"exit_reason": role, "exit_qty": exit_qty, "entry_qty": entry_qty},
                        trade_id=int(trade_id),
                    )
        self._synced_fills.add(fill.fill_id)
        return True

    def _quarantine_fill(self, code: str, fill: FillEvent, detail: str) -> None:
        """Persist an integrity fault and stop new entries without rewriting PnL."""
        self.store.set_meta("app_state", "DISARMED")
        self.store.insert_event(
            self.run_id,
            fill.ts,
            "ERROR",
            code,
            f"fill_id={fill.fill_id} {detail}",
        )

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
