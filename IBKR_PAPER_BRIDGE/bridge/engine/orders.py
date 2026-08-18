"""OrderManager for bracket submission, reconciliation, and fill tracking."""

from __future__ import annotations

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
    # TS-P1-003 unknown-submission safe count
    # ------------------------------------------------------------------

    @property
    def active_unknown_count(self) -> int:
        """Number of unresolved UNKNOWN_SUBMISSION attempts."""
        return self.store.get_active_unknown_count()

    # ------------------------------------------------------------------
    # TS-P1-002 identity-based submission + TS-P1-003 unknown handling
    # ------------------------------------------------------------------

    async def submit_plan(
        self, decision_uid: str, plan: OrderPlan, *, strategy_id: str = "keltner_trail_ema8"
    ) -> dict[str, Any] | None:
        """Submit an order plan with durable identity reservation and unknown-submission safety.

        The canonical intent_id and request_id are computed and persisted
        before broker I/O.  Duplicate delivery or replay is blocked.
        Materially different requests for the same intent cause a fail-closed
        collision error.

        Before broker I/O: exact planned cloids + canonical safe recovery payload
        + state SUBMITTING are committed. Replay/concurrency sees active attempt
        and performs zero broker writes. Any stale SUBMITTING discovered after
        crash is treated as unknown.
        """
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

        # --- 2. Pre-compute planned cloids (same derivation as broker adapter) ---
        planned_cloids = self._compute_planned_cloids(request_id, plan)

        # --- 3. Durable reservation + SUBMITTING attempt (single transaction) ---
        try:
            self.store.conn.execute("BEGIN IMMEDIATE")
        except Exception:
            raise

        attempt_id: int | None = None
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
            if result == "RESERVED":
                # Create SUBMITTING attempt BEFORE broker I/O
                attempt_id = self.store.create_submission_attempt(
                    intent_id=intent_id,
                    request_id=request_id,
                    run_id=self.run_id,
                    decision_uid=decision_uid,
                    planned_cloids=planned_cloids,
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

        if result == "BLOCKED":
            # Identity already exists — idempotent replay, do not resubmit
            return None

        # Reservation + SUBMITTING attempt are now committed

        # --- 4. Set broker cloid seed and submit ---
        original_decision_uid = decision_uid
        plan.decision_uid = request_id
        broker_result: dict[str, Any] | None = None
        pre_send_failure = False
        try:
            broker_result = await self.broker.place_bracket(plan)
        except Exception as exc:
            # PRE_SEND_FAILURE: error before send confirmed
            pre_send_failure = True
            self._record_pre_send_failure(
                attempt_id, intent_id, original_decision_uid, type(exc).__name__
            )
            if hasattr(self.store, "insert_event"):
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "PLACE_BRACKET_FAILED",
                    f"decision_uid={original_decision_uid} intent_id={intent_id} "
                    f"error_type={type(exc).__name__}",
                )
            raise
        finally:
            plan.decision_uid = original_decision_uid

        if pre_send_failure:
            # Already handled in except block
            raise RuntimeError("UNREACHABLE")

        # --- 5. Classify outcome ---
        outcome, orders_data = self._classify_broker_result(
            broker_result, request_id, original_decision_uid, intent_id
        )

        if outcome == SubmissionOutcome.DEFINITIVE_REJECTION:
            self._record_definitive_rejection(
                attempt_id, intent_id, original_decision_uid
            )
            raise IdentityCollisionError(
                "IDENTITY_DEFINITIVE_REJECTION",
                f"intent_id={intent_id}: exchange rejected the submission",
            )

        if outcome == SubmissionOutcome.OUTCOME_UNKNOWN:
            self._record_unknown_submission(
                attempt_id, intent_id, original_decision_uid
            )
            raise IdentityCollisionError(
                "IDENTITY_OUTCOME_UNKNOWN",
                f"intent_id={intent_id}: submission outcome ambiguous",
            )

        # --- 6. VERIFIED_SUCCESS: atomic finalization ---
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
            # Finalization failed after verified broker success → UNKNOWN
            self._record_unknown_submission(
                attempt_id, intent_id, original_decision_uid,
                note=f"finalize_failed:{type(exc).__name__}"
            )
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                getattr(exc, "code", "IDENTITY_FINALIZE_FAILED"),
                f"intent_id={intent_id} decision_uid={original_decision_uid}",
            )
            raise
        except Exception:
            self._record_unknown_submission(
                attempt_id, intent_id, original_decision_uid,
                note="finalize_failed:generic"
            )
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "IDENTITY_FINALIZE_FAILED",
                f"intent_id={intent_id} decision_uid={original_decision_uid}",
            )
            raise

        # --- 7. Resolve attempt as VERIFIED_SUCCESS ---
        self._resolve_attempt(attempt_id, "VERIFIED_SUCCESS", "VERIFIED_SUCCESS")

        self._submitted.add(original_decision_uid)

        await self.sync_broker_state()
        return broker_result

    # ------------------------------------------------------------------
    # TS-P1-003 submission helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_planned_cloids(request_id: str, plan: OrderPlan) -> list[str]:
        """Pre-compute planned cloids using the same derivation as broker adapter.

        Uses blake2s hash of decision_uid:role, same as HyperliquidBroker._cloid.
        """
        import hashlib
        roles = ["entry", "sl"]
        if plan.take_profit is not None:
            roles.append("tp")
        result: list[str] = []
        for role in roles:
            raw = f"{request_id}:{role}"
            cloid = "0x" + hashlib.blake2s(raw.encode("utf-8"), digest_size=16).hexdigest()
            result.append(cloid)
        return result

    def _classify_broker_result(
        self,
        broker_result: Any,
        request_id: str,
        decision_uid: str,
        intent_id: str,
    ) -> tuple[SubmissionOutcome, list[dict[str, Any]]]:
        """Classify the broker result into a structured outcome.

        Returns (outcome, orders_data). orders_data is non-empty only for
        VERIFIED_SUCCESS.
        """
        # Invalid/empty/partial/mixed response → OUTCOME_UNKNOWN
        if not isinstance(broker_result, dict) or not broker_result:
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "BROKER_RESULT_INVALID",
                f"decision_uid={decision_uid} intent_id={intent_id} "
                f"type={type(broker_result).__name__}",
            )
            return SubmissionOutcome.OUTCOME_UNKNOWN, []

        orders_data: list[dict[str, Any]] = []
        has_rejection = False
        for role, order in broker_result.items():
            if not isinstance(order, dict):
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "BROKER_ORDER_INVALID",
                    f"decision_uid={decision_uid} role={role} "
                    f"order_type={type(order).__name__}",
                )
                return SubmissionOutcome.OUTCOME_UNKNOWN, []

            missing = [k for k in ("cloid", "role", "status", "qty") if k not in order]
            if missing:
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "BROKER_ORDER_MISSING_KEYS",
                    f"decision_uid={decision_uid} role={role} "
                    f"missing={','.join(missing)}",
                )
                return SubmissionOutcome.OUTCOME_UNKNOWN, []

            status = str(order.get("status", "")).upper()
            if status in ("REJECTED", "CANCELLED", "EXPIRED"):
                has_rejection = True

            orders_data.append({
                "cloid": order["cloid"],
                "oid": order.get("oid"),
                "group_id": request_id,
                "order_ref": f"{request_id}:{role.upper()}",
                "order_json": self._jsonable_order(order),
                "decision_uid": decision_uid,
                "role": order["role"],
                "status": order["status"],
                "qty": order["qty"],
                "filled_qty": order["qty"] if order["status"] == "FILLED" else 0.0,
                "avg_fill_px": order.get("avg_fill_px"),
            })

        if not orders_data:
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "BROKER_ORDERS_EMPTY",
                f"decision_uid={decision_uid} intent_id={intent_id}",
            )
            return SubmissionOutcome.OUTCOME_UNKNOWN, []

        if has_rejection:
            return SubmissionOutcome.DEFINITIVE_REJECTION, orders_data

        return SubmissionOutcome.VERIFIED_SUCCESS, orders_data

    def _record_pre_send_failure(
        self, attempt_id: int | None, intent_id: str,
        decision_uid: str, error_type: str
    ) -> None:
        """Record PRE_SEND_FAILURE — attempt stays SUBMITTING or resolves if possible."""
        if attempt_id is None:
            return
        try:
            self.store.conn.execute("BEGIN IMMEDIATE")
            ok = self.store.resolve_submission_attempt(
                attempt_id, "DEFINITIVE_REJECTION", "PRE_SEND_FAILURE"
            )
            self.store.conn.commit()
            if not ok:
                # Could not resolve — attempt may already be handled
                pass
        except Exception:
            try:
                self.store.conn.rollback()
            except Exception:
                pass

    def _record_definitive_rejection(
        self, attempt_id: int | None, intent_id: str, decision_uid: str
    ) -> None:
        """Record DEFINITIVE_REJECTION — atomically resolve attempt."""
        if attempt_id is None:
            return
        try:
            self.store.conn.execute("BEGIN IMMEDIATE")
            self.store.resolve_submission_attempt(
                attempt_id, "DEFINITIVE_REJECTION", "DEFINITIVE_REJECTION"
            )
            self.store.conn.commit()
        except Exception:
            try:
                self.store.conn.rollback()
            except Exception:
                pass

    def _record_unknown_submission(
        self, attempt_id: int | None, intent_id: str,
        decision_uid: str, note: str = ""
    ) -> None:
        """Record OUTCOME_UNKNOWN — atomically resolve attempt as UNKNOWN_SUBMISSION.

        If the update itself fails, durable SUBMITTING remains non-replayable
        and is treated as unknown on restart.
        """
        if attempt_id is None:
            return
        try:
            self.store.conn.execute("BEGIN IMMEDIATE")
            ok = self.store.resolve_submission_attempt(
                attempt_id, "UNKNOWN_SUBMISSION", "OUTCOME_UNKNOWN"
            )
            self.store.conn.commit()
            if not ok:
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "UNKNOWN_RESOLVE_FAILED",
                    f"attempt_id={attempt_id} intent_id={intent_id} "
                    f"decision_uid={decision_uid} note={note}",
                )
        except Exception:
            try:
                self.store.conn.rollback()
            except Exception:
                pass
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "UNKNOWN_RESOLVE_FAILED",
                f"attempt_id={attempt_id} intent_id={intent_id} "
                f"decision_uid={decision_uid} note={note}",
            )

    def _resolve_attempt(
        self, attempt_id: int | None, state: str, outcome: str
    ) -> None:
        """Resolve attempt atomically."""
        if attempt_id is None:
            return
        try:
            self.store.conn.execute("BEGIN IMMEDIATE")
            self.store.resolve_submission_attempt(attempt_id, state, outcome)
            self.store.conn.commit()
        except Exception:
            try:
                self.store.conn.rollback()
            except Exception:
                pass

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
