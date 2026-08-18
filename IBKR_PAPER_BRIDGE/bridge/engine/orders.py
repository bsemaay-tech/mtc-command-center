"""OrderManager for bracket submission, reconciliation, and fill tracking."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
import math
from typing import Any

from bridge.broker.base import (
    Broker,
    BrokerOutcomeUnknown,
    BrokerPreSendFailure,
    EvidenceStatus,
    RecoveryQueryEvidence,
    SubmissionDisposition,
    SubmissionOutcome,
    SubmissionRecoveryEvidence,
    SubmissionRecoveryRequest,
    SubmissionRejectedError,
    UnknownSubmissionError,
)
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
    # TS-P1-002 identity-based submission
    # ------------------------------------------------------------------

    async def submit_plan(
        self, decision_uid: str, plan: OrderPlan, *, strategy_id: str = "keltner_trail_ema8"
    ) -> dict[str, Any] | None:
        """Reserve, submit, verify, and finalize without an ambiguous retry path."""
        if decision_uid in self._submitted:
            return None

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

        quarantined = self.store.get_quarantined_submission_attempts()
        if quarantined:
            active = quarantined[0]
            raise UnknownSubmissionError(
                "SUBMISSION_QUARANTINE_ACTIVE",
                str(active["request_id"]),
                str(active["attempt_id"]),
            )

        original_decision_uid = decision_uid
        plan.decision_uid = request_id
        try:
            planner = getattr(self.broker, "planned_cloids", None)
            if not callable(planner):
                if self._legacy_dry_run_boundary_allowed():
                    plan.decision_uid = original_decision_uid
                    return await self._submit_legacy_dry_run(
                        decision_uid=decision_uid,
                        plan=plan,
                        intent_id=intent_id,
                        intent_preimage=intent_preimage,
                        intent_version=intent_version,
                        request_id=request_id,
                        request_preimage=request_preimage,
                        request_version=request_version,
                    )
                raise BrokerPreSendFailure("BROKER_IDENTITY_BOUNDARY_UNAVAILABLE")
            planned_cloids = {
                str(role).upper(): str(cloid)
                for role, cloid in planner(plan).items()
            }
        finally:
            plan.decision_uid = original_decision_uid

        recovery_payload = {
            "version": "ts-p1-003-recovery-v1",
            "symbol": plan.signal.symbol.upper(),
            "direction": plan.signal.direction.upper(),
            "signal_ts": plan.signal.ts.astimezone(UTC).isoformat(),
            "ref_price_hex": float(plan.signal.ref_price).hex(),
            "qty_hex": float(plan.qty).hex(),
            "entry_type": plan.entry_type,
            "limit_price_hex": (
                float(plan.limit_price).hex() if plan.limit_price is not None else None
            ),
            "stop_loss_hex": float(plan.stop_loss).hex(),
            "take_profit_hex": (
                float(plan.take_profit).hex() if plan.take_profit is not None else None
            ),
            "leverage": plan.leverage,
        }
        try:
            result, attempt_id = self.store.reserve_submission(
                intent_id=intent_id,
                intent_preimage=intent_preimage,
                intent_version=intent_version,
                request_id=request_id,
                request_preimage=request_preimage,
                request_version=request_version,
                cloid_seed=request_id,
                origin_run_id=self.run_id,
                origin_decision_uid=decision_uid,
                recovery_payload=recovery_payload,
                planned_cloids=planned_cloids,
            )
        except IdentityCollisionError as exc:
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                exc.code,
                f"intent_id={intent_id} request_id={request_id} decision_uid={decision_uid}",
            )
            raise

        if result == "BLOCKED":
            return None

        plan.decision_uid = request_id
        try:
            try:
                broker_result = await self.broker.place_bracket(plan)
            except BrokerPreSendFailure as exc:
                reason_code = self._safe_broker_reason_code(
                    exc.reason_code, "PRE_SEND_FAILURE"
                )
                try:
                    self.store.transition_submission_attempt(
                        attempt_id, "PRE_SEND_FAILURE", reason_code
                    )
                except Exception:
                    raise UnknownSubmissionError(
                        "PRE_SEND_FINALIZATION_FAILED", request_id, attempt_id
                    ) from exc
                raise SubmissionRejectedError(
                    "PRE_SEND_FAILURE", request_id, attempt_id
                ) from exc
            except BrokerOutcomeUnknown as exc:
                reason_code = self._safe_broker_reason_code(
                    exc.reason_code, "OUTCOME_UNKNOWN"
                )
                self._quarantine_unknown(attempt_id, reason_code)
                raise UnknownSubmissionError(
                    reason_code, request_id, attempt_id
                ) from exc
            except Exception as exc:
                self._quarantine_unknown(attempt_id, "UNTYPED_BROKER_EXCEPTION")
                raise UnknownSubmissionError(
                    "UNTYPED_BROKER_EXCEPTION", request_id, attempt_id
                ) from exc
        finally:
            plan.decision_uid = original_decision_uid

        if not isinstance(broker_result, SubmissionOutcome):
            self._quarantine_unknown(attempt_id, "UNTYPED_BROKER_RESULT")
            raise UnknownSubmissionError(
                "UNTYPED_BROKER_RESULT", request_id, attempt_id
            )
        if broker_result.disposition is SubmissionDisposition.DEFINITIVE_REJECTION:
            if broker_result.orders:
                self._quarantine_unknown(attempt_id, "REJECTION_WITH_ORDER_ROWS")
                raise UnknownSubmissionError(
                    "REJECTION_WITH_ORDER_ROWS", request_id, attempt_id
                )
            try:
                reason_code = self._safe_broker_reason_code(
                    broker_result.reason_code, "DEFINITIVE_REJECTION"
                )
                self.store.transition_submission_attempt(
                    attempt_id,
                    "DEFINITIVE_REJECTION",
                    reason_code,
                )
            except Exception as exc:
                raise UnknownSubmissionError(
                    "DEFINITIVE_REJECTION_FINALIZATION_FAILED",
                    request_id,
                    attempt_id,
                ) from exc
            raise SubmissionRejectedError(
                "DEFINITIVE_REJECTION", request_id, attempt_id
            )
        if broker_result.disposition is SubmissionDisposition.OUTCOME_UNKNOWN:
            reason_code = self._safe_broker_reason_code(
                broker_result.reason_code, "OUTCOME_UNKNOWN"
            )
            self._quarantine_unknown(attempt_id, reason_code)
            raise UnknownSubmissionError(
                reason_code,
                request_id,
                attempt_id,
            )
        if broker_result.disposition is not SubmissionDisposition.VERIFIED_SUCCESS:
            self._quarantine_unknown(attempt_id, "INVALID_SUBMISSION_DISPOSITION")
            raise UnknownSubmissionError(
                "INVALID_SUBMISSION_DISPOSITION", request_id, attempt_id
            )

        try:
            orders_data = self._validated_orders(
                broker_result.orders,
                planned_cloids,
                plan,
                request_id,
                original_decision_uid,
            )
        except Exception as exc:
            self._quarantine_unknown(attempt_id, "BROKER_RESULT_COVERAGE_INVALID")
            raise UnknownSubmissionError(
                "BROKER_RESULT_COVERAGE_INVALID", request_id, attempt_id
            ) from exc

        try:
            self.store.finalize_submission(
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
                attempt_id=attempt_id,
            )
        except Exception as exc:
            self._quarantine_unknown(attempt_id, "LOCAL_FINALIZATION_FAILED")
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "ERROR",
                "LOCAL_FINALIZATION_FAILED",
                f"intent_id={intent_id} request_id={request_id} attempt_id={attempt_id}",
            )
            raise UnknownSubmissionError(
                "LOCAL_FINALIZATION_FAILED", request_id, attempt_id
            ) from exc

        self._submitted.add(original_decision_uid)
        try:
            await self.sync_broker_state()
        except Exception:
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                "WARN",
                "POST_FINALIZE_SYNC_DEFERRED",
                f"request_id={request_id} attempt_id={attempt_id}",
            )
        return {
            str(row["role"]).lower(): dict(row["order_json"])
            for row in orders_data
        }

    def _legacy_dry_run_boundary_allowed(self) -> bool:
        """Compatibility only for old in-process dry-run recording fakes."""
        run = self.store.get_run(self.run_id)
        return (
            run is not None
            and run.get("mode") == "dry_run"
            and isinstance(getattr(self.broker, "submitted", None), list)
        )

    async def _submit_legacy_dry_run(
        self,
        *,
        decision_uid: str,
        plan: OrderPlan,
        intent_id: str,
        intent_preimage: str,
        intent_version: str,
        request_id: str,
        request_preimage: str,
        request_version: str,
    ) -> dict[str, Any] | None:
        """Preserve accepted offline protocol-only tests; never used by adapters."""
        self.store.conn.execute("BEGIN IMMEDIATE")
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
            self.store.conn.commit()
        except Exception:
            self.store.conn.rollback()
            raise
        if result == "BLOCKED":
            return None

        original = plan.decision_uid
        plan.decision_uid = request_id
        try:
            raw = await self.broker.place_bracket(plan)
        finally:
            plan.decision_uid = original
        if not isinstance(raw, dict) or not raw:
            raise RuntimeError("LEGACY_DRY_RUN_RESULT_INVALID")
        orders_data: list[dict[str, Any]] = []
        for raw_role, order in raw.items():
            if not isinstance(order, dict) or any(
                key not in order for key in ("cloid", "role", "status", "qty")
            ):
                raise RuntimeError("LEGACY_DRY_RUN_RESULT_INVALID")
            role = str(raw_role).upper()
            qty = float(order["qty"])
            orders_data.append({
                "cloid": str(order["cloid"]),
                "oid": order.get("oid"),
                "group_id": request_id,
                "order_ref": f"{request_id}:{role}",
                "order_json": self._jsonable_order(order),
                "decision_uid": decision_uid,
                "role": str(order["role"]).upper(),
                "status": str(order["status"]).upper(),
                "qty": qty,
                "filled_qty": (
                    qty if str(order["status"]).upper() == "FILLED" else 0.0
                ),
                "avg_fill_px": order.get("avg_fill_px"),
            })
        self.store.finalize_submission(
            intent_id=intent_id,
            request_id=request_id,
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
            orders_data=orders_data,
        )
        self._submitted.add(decision_uid)
        return {
            str(role): self._jsonable_order(order)
            for role, order in raw.items()
        }

    def _quarantine_unknown(self, attempt_id: str, reason_code: str) -> None:
        """Best-effort UNKNOWN transition; failed writes leave SUBMITTING durable."""
        try:
            self.store.mark_submission_unknown(attempt_id, reason_code)
        except Exception:
            try:
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "UNKNOWN_TRANSITION_FAILED",
                    f"attempt_id={attempt_id}",
                )
            except Exception:
                pass

    @staticmethod
    def _safe_broker_reason_code(value: object, fallback: str) -> str:
        """Accept only short structured adapter codes; never forward raw text."""
        code = str(value).strip().upper()
        if (
            code
            and len(code) <= 96
            and all(
                ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_:-."
                for ch in code
            )
        ):
            return code
        return fallback

    def _validated_orders(
        self,
        orders: Mapping[str, dict[str, Any]],
        planned_cloids: Mapping[str, str],
        plan: OrderPlan,
        request_id: str,
        original_decision_uid: str,
    ) -> list[dict[str, Any]]:
        """Require exact role/cloid coverage and success-compatible statuses."""
        if not isinstance(orders, Mapping) or not orders:
            raise ValueError("orders must be a non-empty mapping")
        normalized: dict[str, dict[str, Any]] = {}
        for raw_role, order in orders.items():
            role = str(raw_role).upper()
            if role in normalized or role not in {"ENTRY", "SL", "TP"}:
                raise ValueError("duplicate or invalid result role")
            if not isinstance(order, dict):
                raise ValueError("order result must be a mapping")
            normalized[role] = order
        expected = {str(role).upper(): str(cloid) for role, cloid in planned_cloids.items()}
        if set(normalized) != set(expected):
            raise ValueError("result role coverage mismatch")

        success_statuses = {
            "ACCEPTED",
            "SUBMITTED",
            "OPEN",
            "RESTING",
            "PENDING",
            "WAITING_CHILD",
            "FILLED",
        }
        seen_cloids: set[str] = set()
        rows: list[dict[str, Any]] = []
        for role in sorted(expected):
            order = normalized[role]
            if any(key not in order for key in ("cloid", "role", "status", "qty")):
                raise ValueError("order result is missing required fields")
            cloid = str(order["cloid"])
            status = str(order["status"]).upper()
            qty = float(order["qty"])
            if str(order["role"]).upper() != role:
                raise ValueError("order role mismatch")
            if cloid != expected[role] or cloid in seen_cloids:
                raise ValueError("order cloid coverage mismatch")
            if status not in success_statuses:
                raise ValueError("order status is not success-compatible")
            if not math.isfinite(qty) or qty != float(plan.qty):
                raise ValueError("order quantity mismatch")
            seen_cloids.add(cloid)
            rows.append({
                "cloid": cloid,
                "oid": order.get("oid"),
                "group_id": request_id,
                "order_ref": f"{request_id}:{role}",
                "order_json": self._jsonable_order(order),
                "decision_uid": original_decision_uid,
                "role": role,
                "status": status,
                "qty": qty,
                "filled_qty": qty if status == "FILLED" else 0.0,
                "avg_fill_px": order.get("avg_fill_px"),
            })
        return rows

    async def recover_unknown_submissions(self) -> None:
        """Run one conservative evidence cycle for every active attempt."""
        for attempt in self.store.get_active_submission_attempts():
            request = SubmissionRecoveryRequest(
                attempt_id=str(attempt["attempt_id"]),
                request_id=str(attempt["request_id"]),
                planned_cloids=dict(attempt["planned_cloids"]),
                symbol=str(attempt["recovery_payload"]["symbol"]),
                window_start=str(attempt["created_ts"]),
            )
            evidence_method = getattr(
                self.broker, "submission_recovery_evidence", None
            )
            if not callable(evidence_method):
                evidence = self._unavailable_evidence(
                    request, EvidenceStatus.UNAVAILABLE, "RECOVERY_API_UNAVAILABLE"
                )
            else:
                try:
                    evidence = await evidence_method(request)
                except Exception:
                    evidence = self._unavailable_evidence(
                        request, EvidenceStatus.QUERY_FAILED, "RECOVERY_QUERY_FAILED"
                    )
            if not isinstance(evidence, SubmissionRecoveryEvidence):
                evidence = self._unavailable_evidence(
                    request, EvidenceStatus.CONFLICTING, "RECOVERY_EVIDENCE_UNTYPED"
                )
            expected_map = {
                str(role).upper(): str(cloid)
                for role, cloid in request.planned_cloids.items()
            }
            evidence_map = {
                str(role).upper(): str(cloid)
                for role, cloid in evidence.planned_cloids.items()
            }
            if (
                evidence.request_id != request.request_id
                or evidence_map != expected_map
                or set(evidence.direct_lookup) != set(expected_map.values())
            ):
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "ERROR",
                    "RECOVERY_EVIDENCE_LINKAGE_REJECTED",
                    f"attempt_id={request.attempt_id} request_id={request.request_id}",
                )
                continue
            verdict = self._recovery_verdict(evidence, set(expected_map.values()))
            payload = self._recovery_payload(evidence)
            state = self.store.record_recovery_cycle(
                attempt_id=request.attempt_id,
                request_id=request.request_id,
                planned_cloids=expected_map,
                observed_ts=self.store.now(),
                verdict=verdict,
                evidence_payload=payload,
            )
            if state in {"CONFIRMED_PRESENT", "CONFIRMED_ABSENT"}:
                self.store.insert_event(
                    self.run_id,
                    datetime.now(UTC),
                    "WARN",
                    state,
                    f"attempt_id={request.attempt_id} request_id={request.request_id}",
                )

    @staticmethod
    def _unavailable_evidence(
        request: SubmissionRecoveryRequest,
        status: EvidenceStatus,
        reason_code: str,
    ) -> SubmissionRecoveryEvidence:
        query = RecoveryQueryEvidence(status=status, reason_code=reason_code)
        return SubmissionRecoveryEvidence(
            request_id=request.request_id,
            planned_cloids=dict(request.planned_cloids),
            direct_lookup={
                str(cloid): query for cloid in request.planned_cloids.values()
            },
            open_orders=query,
            historical_orders=query,
            fills=query,
            position=query,
        )

    @staticmethod
    def _recovery_verdict(
        evidence: SubmissionRecoveryEvidence, planned: set[str]
    ) -> str:
        required = [
            *evidence.direct_lookup.values(),
            evidence.open_orders,
            evidence.historical_orders,
            evidence.fills,
        ]
        all_queries = [*required, evidence.position]
        for query in all_queries:
            found = tuple(map(str, query.found_cloids))
            if len(set(found)) != len(found):
                return "CONFLICTING"
            if query.status is EvidenceStatus.FOUND and not found:
                return "CONFLICTING"
            if query.status is not EvidenceStatus.FOUND and found:
                return "CONFLICTING"
            if set(found) - planned:
                return "CONFLICTING"
        for queried_cloid, query in evidence.direct_lookup.items():
            if (
                query.status is EvidenceStatus.FOUND
                and str(queried_cloid) not in set(map(str, query.found_cloids))
            ):
                return "CONFLICTING"

        attributable = {
            cloid
            for query in required
            for cloid in map(str, query.found_cloids)
            if cloid in planned
        }
        if attributable:
            return "PRESENT"
        if evidence.position.status in {
            EvidenceStatus.FOUND,
            EvidenceStatus.CONFLICTING,
        }:
            return "CONFLICTING"
        if any(query.status is EvidenceStatus.CONFLICTING for query in required):
            return "CONFLICTING"
        if (
            all(
                query.status is EvidenceStatus.NOT_FOUND
                for query in evidence.direct_lookup.values()
            )
            and evidence.open_orders.status is EvidenceStatus.NOT_FOUND
            and evidence.historical_orders.status is EvidenceStatus.NOT_FOUND
            and evidence.fills.status is EvidenceStatus.NOT_FOUND
        ):
            return "ABSENT_COMPLETE"
        return "INCOMPLETE"

    @staticmethod
    def _query_payload(query: RecoveryQueryEvidence) -> dict[str, Any]:
        return {
            "status": query.status.value,
            "found_cloids": list(map(str, query.found_cloids)),
            "reason_code": query.reason_code,
        }

    @classmethod
    def _recovery_payload(
        cls, evidence: SubmissionRecoveryEvidence
    ) -> dict[str, Any]:
        return {
            "request_id": evidence.request_id,
            "planned_cloids": {
                str(role).upper(): str(cloid)
                for role, cloid in evidence.planned_cloids.items()
            },
            "direct_lookup": {
                str(cloid): cls._query_payload(query)
                for cloid, query in evidence.direct_lookup.items()
            },
            "open_orders": cls._query_payload(evidence.open_orders),
            "historical_orders": cls._query_payload(evidence.historical_orders),
            "fills": cls._query_payload(evidence.fills),
            "position": cls._query_payload(evidence.position),
        }

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
        await self.recover_unknown_submissions()
        if self.store.has_submission_quarantine():
            return
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
        if self.store.has_submission_quarantine():
            return False
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
        if self.store.has_submission_quarantine():
            return
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
        allowed = {
            "cloid",
            "oid",
            "role",
            "status",
            "qty",
            "filled_qty",
            "symbol",
            "trigger_px",
            "avg_fill_px",
            "reduce_only",
            "side",
            "order_type",
            "price",
            "limit_px",
            "direction",
            "leverage",
            "signal_ts",
        }
        clean: dict[str, Any] = {}
        for key, value in order.items():
            if key not in allowed:
                continue
            if isinstance(value, datetime):
                clean[key] = value.isoformat()
            else:
                clean[key] = value
        return clean
