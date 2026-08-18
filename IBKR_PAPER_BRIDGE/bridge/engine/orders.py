"""OrderManager for bracket submission, reconciliation, and fill tracking."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
import math
from typing import Any, Callable

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
from bridge.engine.types import (
    FLATTEN_VERIFY_DEADLINE_S,
    PARTIAL_TERMINAL_STATES,
    PROTECT_DEADLINE_S,
    ActionOutcome,
    ActionRecordStatus,
    BrokerEvent,
    BrokerOrder,
    Evidence,
    FillEvent,
    LotQuantizationError,
    LotUnit,
    OrderPlan,
    OrderUpdateEvent,
    OrderView,
    PartialActionKind,
    PartialProtectionState,
    Position,
    Provenance,
    SymbolSnapshot,
    lots_to_size,
    quantize_lots,
)
from bridge.store.db import (
    IdentityCollisionError,
    OrderCollisionError,
    PartialRecoveryConflictError,
    Store,
    compute_intent_identity,
    compute_partial_action_cloid,
    compute_partial_action_id,
    compute_request_identity,
)

_PARTIAL_RECOVERY_METHODS = (
    "lot_unit",
    "symbol_snapshot",
    "query_order",
    "cancel_order_by_cloid",
    "place_protective_stop",
    "flatten_reduce_only",
)

_LIVE_ORDER_STATUSES = frozenset({"OPEN", "SUBMITTED", "PENDING", "RESTING"})


class SymbolLockNotHeld(RuntimeError):
    """Programming error: an owned mutation was attempted outside the lock."""

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.reason_code = "SYMBOL_LOCK_NOT_HELD"
        super().__init__(f"{self.reason_code}: {symbol}")


class SymbolLockRegistry:
    """One writer per symbol.

    Fill ingestion, order updates, periodic reconcile, restart recovery,
    disarm/kill, ordinary trail/close/flip and the whole partial-recovery run
    serialize through the same per-symbol lock. It is reentrant for the owning
    asyncio task so a recovery run can call helpers that assert the lock.
    """

    def __init__(self) -> None:
        self._locks: dict[str, asyncio.Lock] = {}
        self._depth: dict[str, int] = {}
        self._owner: dict[str, object] = {}

    def _lock_for(self, symbol: str) -> asyncio.Lock:
        lock = self._locks.get(symbol)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[symbol] = lock
        return lock

    @staticmethod
    def _current_task() -> object:
        try:
            return asyncio.current_task()
        except RuntimeError:  # pragma: no cover - no running loop
            return None

    def is_held(self, symbol: str) -> bool:
        return self._owner.get(symbol) is self._current_task() and bool(
            self._depth.get(symbol)
        )

    def require(self, symbol: str) -> None:
        if not self.is_held(symbol):
            raise SymbolLockNotHeld(symbol)

    def hold(self, symbol: str) -> "_SymbolLockHold":
        return _SymbolLockHold(self, symbol)


class _SymbolLockHold:
    def __init__(self, registry: SymbolLockRegistry, symbol: str) -> None:
        self._registry = registry
        self._symbol = symbol
        self._reentrant = False

    async def __aenter__(self) -> "_SymbolLockHold":
        registry, symbol = self._registry, self._symbol
        if registry.is_held(symbol):
            self._reentrant = True
            registry._depth[symbol] += 1
            return self
        await registry._lock_for(symbol).acquire()
        registry._owner[symbol] = registry._current_task()
        registry._depth[symbol] = 1
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        registry, symbol = self._registry, self._symbol
        registry._depth[symbol] -= 1
        if registry._depth[symbol] == 0:
            registry._owner.pop(symbol, None)
            registry._lock_for(symbol).release()
        return None


def exact_size_equal(left: float, right: float, lot: LotUnit | None) -> bool:
    """Exact quantity comparison — integer lots when a quantum is known.

    Falls back to exact decimal spelling (never a magic epsilon) when the
    caller has no size quantum, so a legacy fake broker without exchange
    metadata still gets an exact comparison rather than a permissive one.
    """
    try:
        if lot is not None:
            return quantize_lots(abs(left), lot) == quantize_lots(abs(right), lot)
        return Decimal(str(abs(left))) == Decimal(str(abs(right)))
    except (LotQuantizationError, InvalidOperation, ValueError, TypeError):
        return False


def exit_side_for(size: float) -> str:
    """The side that reduces a position of the given signed size."""
    return "SELL" if size > 0 else "BUY"


def _local_evidence(reason_code: str, detail: str = "") -> Evidence:
    return Evidence("LOCAL", reason_code, detail=detail)


class OrderManager:
    def __init__(
        self,
        store: Store,
        broker: Broker,
        run_id: str,
        pending_grace_s: float = 120.0,
        *,
        monotonic: Callable[[], float] | None = None,
    ) -> None:
        self.store = store
        self.broker = broker
        self.run_id = run_id
        self._submitted: set[str] = set()
        self._synced_fills: set[str] = set()
        self._queued_events: list[BrokerEvent] = []
        self.pending_grace_s = pending_grace_s
        # Injected monotonic runtime clock. Its values are process-local and
        # are deliberately never persisted; a restart falls back to the durable
        # UTC deadline alone (see _deadline_expired).
        self._monotonic: Callable[[], float] = monotonic or time.monotonic
        self._mono_deadlines: dict[str, float] = {}
        self.symbol_locks = SymbolLockRegistry()
        self._legacy_partial_scan_done = False
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
            # TS-P1-003 quarantine dominates: TS-P1-004 defers completely.
            return
        await self.run_partial_recoveries()
        positions = await self.broker.positions()
        open_orders = await self.broker.open_orders()
        protected = {
            position.symbol
            for position in positions
            if self._position_is_protected(position, open_orders)
        }
        for position in positions:
            if position.symbol in protected:
                continue
            if self._partial_recovery_owns(position.symbol):
                # The recovery state machine is the only writer for this
                # symbol; ordinary repair must not compete with it.
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
        async with self.symbol_locks.hold(position.symbol):
            # Re-check under the lock: a partial recovery may have claimed the
            # symbol between the caller's decision and this acquisition.
            if self._partial_recovery_owns(position.symbol):
                self._partial_event(
                    "WARN", "TRAIL_SUPPRESSED_PARTIAL_RECOVERY", position.symbol
                )
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
        async with self.symbol_locks.hold(position.symbol):
            if self._partial_recovery_owns(position.symbol):
                self._partial_event(
                    "WARN", "CLOSE_SUPPRESSED_PARTIAL_RECOVERY", position.symbol
                )
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
            self._observe_entry_fill(order, order_filled_qty)
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

    # ==================================================================
    # TS-P1-004 — partial-fill protect-or-flatten
    # ==================================================================

    def _partial_broker(self) -> Any | None:
        """The bounded recovery surface, or None when the adapter lacks it."""
        broker = self.broker
        if all(callable(getattr(broker, name, None)) for name in _PARTIAL_RECOVERY_METHODS):
            return broker
        return None

    def _partial_event(
        self, severity: str, code: str, symbol: str, detail: str = ""
    ) -> None:
        try:
            self.store.insert_event(
                self.run_id,
                datetime.now(UTC),
                severity,
                code,
                f"{symbol} {detail}".strip(),
            )
        except Exception:  # pragma: no cover - never let audit break safety
            pass

    def _partial_recovery_owns(self, symbol: str) -> bool:
        """True while the recovery machine (or its abort latch) owns a symbol."""
        if not self.store.partial_protection_enabled():
            return False
        if self.store.active_partial_recovery_for_symbol(symbol) is not None:
            return True
        return self.store.partial_recovery_abort_active(symbol)

    def _disarm_for_partial(self, code: str, symbol: str, detail: str = "") -> None:
        try:
            self.store.set_meta("app_state", "DISARMED")
        except Exception:  # pragma: no cover - defensive
            pass
        self._partial_event("ERROR", code, symbol, detail)

    # ---------------- detection ----------------

    def _observe_entry_fill(self, order: Mapping[str, Any], filled_qty: float) -> None:
        """Persist the first partial observation before any broker mutation.

        Called from fill ingestion. This method never performs broker I/O: it
        only writes the durable recovery row (with its fixed deadline) and
        latches the application DISARMED so no new risk can be opened while an
        owned entry is partially filled.
        """
        if not self.store.partial_protection_enabled():
            return
        trade_id = order.get("trade_id")
        if trade_id is None:
            return
        try:
            ordered = float(order["qty"])
        except (TypeError, ValueError):
            return
        if not (0.0 < float(filled_qty) < ordered):
            return
        trade = self.store.get_trade(int(trade_id))
        if trade is None or trade["exit_ts"] is not None:
            return
        symbol = str(trade["coin"])
        existing = self.store.active_partial_recovery_for_symbol(symbol)
        if existing is not None:
            # A live generation already owns this symbol; quantities are
            # recomputed by the runner. The deadline is never rewritten.
            return
        first_observed = self.store.now()
        deadline = first_observed + timedelta(seconds=PROTECT_DEADLINE_S)
        request_id = str(
            order.get("group_id") or order.get("order_ref") or order["decision_uid"]
        )
        try:
            row = self.store.open_partial_recovery(
                run_id=self.run_id,
                symbol=symbol,
                trade_id=int(trade_id),
                entry_cloid=str(order["cloid"]),
                entry_decision_uid=str(order["decision_uid"]),
                entry_request_id=request_id,
                first_observed_ts=first_observed,
                protect_deadline_ts=deadline,
                reason_code="PARTIAL_ENTRY_FILL",
            )
            # Arm the runtime monotonic domain at the moment of detection, not
            # at the first recovery pass, so a stalled scheduler cannot buy time.
            self._arm_monotonic_deadline(row, "protect", PROTECT_DEADLINE_S)
        except PartialRecoveryConflictError as exc:
            self._disarm_for_partial(
                "PARTIAL_RECOVERY_OPEN_FAILED", symbol, exc.code
            )
            return
        self._disarm_for_partial(
            "PARTIAL_FILL_DETECTED",
            symbol,
            f"trade_id={trade_id} filled={filled_qty} ordered={ordered}",
        )

    # ---------------- deadlines ----------------

    @staticmethod
    def _parse_utc(value: object) -> datetime | None:
        if value in (None, ""):
            return None
        try:
            parsed = datetime.fromisoformat(str(value))
        except (TypeError, ValueError):
            return None
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)

    def _arm_monotonic_deadline(
        self, recovery: Mapping[str, Any], kind: str, budget_s: float
    ) -> None:
        """Bind the persisted UTC deadline to this process's monotonic clock.

        The remaining UTC budget — never a fresh full budget — is what gets
        armed, so a restart cannot buy extra time.
        """
        key = f"{recovery['recovery_id']}:{kind}"
        if key in self._mono_deadlines:
            return
        deadline = self._parse_utc(
            recovery["protect_deadline_ts" if kind == "protect" else "flatten_deadline_ts"]
        )
        if deadline is None:
            return
        remaining = (deadline - self.store.now()).total_seconds()
        self._mono_deadlines[key] = self._monotonic() + max(0.0, min(budget_s, remaining))

    def _deadline_expired(self, recovery: Mapping[str, Any], kind: str) -> bool:
        """Conservative expiry: either clock domain may expire a deadline."""
        field = "protect_deadline_ts" if kind == "protect" else "flatten_deadline_ts"
        raw = recovery[field]
        if raw in (None, ""):
            return False  # budget not started yet
        deadline = self._parse_utc(raw)
        first_observed = self._parse_utc(recovery["first_observed_ts"])
        if deadline is None or first_observed is None:
            return True  # unparseable durable evidence is treated as expired
        now = self.store.now()
        if now < first_observed:
            return True  # wall-clock rollback / conflicting domains
        utc_expired = now >= deadline
        mono_deadline = self._mono_deadlines.get(f"{recovery['recovery_id']}:{kind}")
        mono_expired = (
            mono_deadline is not None and self._monotonic() >= mono_deadline
        )
        return utc_expired or mono_expired

    # ---------------- evidence / provenance ----------------

    def _owned_cloids(self, recovery: Mapping[str, Any]) -> set[str]:
        owned = {
            str(row["cloid"])
            for row in self.store.get_orders_for_trade(int(recovery["trade_id"]))
        }
        owned |= {
            str(row["target_cloid"])
            for row in self.store.partial_actions_for_recovery(
                str(recovery["recovery_id"])
            )
        }
        return owned

    async def _snapshot(
        self, broker: Any, recovery: Mapping[str, Any]
    ) -> SymbolSnapshot:
        symbol = str(recovery["symbol"])
        self.symbol_locks.require(symbol)
        try:
            snapshot = await broker.symbol_snapshot(symbol)
        except Exception as exc:  # noqa: BLE001 - any failure is inexact evidence
            return SymbolSnapshot(
                symbol=symbol, exact=False, net_size=None, open_orders=(), lot=None,
                evidence=_local_evidence("SNAPSHOT_FAILED", type(exc).__name__),
            )
        if not isinstance(snapshot, SymbolSnapshot):
            return SymbolSnapshot(
                symbol=symbol, exact=False, net_size=None, open_orders=(), lot=None,
                evidence=_local_evidence("SNAPSHOT_UNTYPED"),
            )
        return snapshot

    def _classify(
        self, recovery: Mapping[str, Any], snapshot: SymbolSnapshot
    ) -> tuple[Provenance, int | None, str]:
        """Owned / mixed / foreign / ambiguous verdict for the bounded snapshot."""
        if not snapshot.exact or snapshot.lot is None or snapshot.net_size is None:
            return Provenance.UNVERIFIED, None, "SNAPSHOT_INEXACT"
        lot = snapshot.lot
        owned_cloids = self._owned_cloids(recovery)
        for order in snapshot.open_orders:
            if str(order.status).upper() not in _LIVE_ORDER_STATUSES:
                continue
            if str(order.cloid) in owned_cloids:
                continue
            if self.store.get_order(str(order.cloid)) is not None:
                continue
            return Provenance.FOREIGN, None, "FOREIGN_ORDER_PRESENT"
        trade = self.store.get_trade(int(recovery["trade_id"]))
        if trade is None:
            return Provenance.AMBIGUOUS, None, "TRADE_MISSING"
        net = float(snapshot.net_size)
        direction = str(trade["direction"]).upper()
        if (direction == "LONG" and net < 0) or (direction == "SHORT" and net > 0):
            return Provenance.AMBIGUOUS, None, "POSITION_SIDE_CONFLICT"
        try:
            position_lots = quantize_lots(abs(net), lot)
            totals = self.store.trade_fill_totals(int(recovery["trade_id"]))
            entry_order = self.store.get_order(str(recovery["entry_cloid"]))
            if entry_order is None:
                return Provenance.AMBIGUOUS, None, "ENTRY_ORDER_MISSING"
            owned_ceiling = quantize_lots(
                float(entry_order["qty"]), lot
            ) - quantize_lots(float(totals["exit_qty"]), lot)
        except LotQuantizationError as exc:
            return Provenance.UNVERIFIED, None, exc.reason_code
        if owned_ceiling < 0:
            return Provenance.AMBIGUOUS, None, "LOCAL_EXIT_EXCEEDS_ENTRY"
        if position_lots > owned_ceiling:
            # More live size than this trade could ever account for.
            return Provenance.MIXED, position_lots, "MIXED_PROVENANCE"
        return Provenance.OWNED, position_lots, "OWNED"

    def qualifying_protection(
        self,
        snapshot: SymbolSnapshot,
        *,
        position_lots: int,
        exit_side: str,
        owned_cloids: set[str],
    ) -> OrderView | None:
        """The single shared protection predicate (placement AND reconcile).

        A stop qualifies only when it is: this symbol, the opposite exit side,
        role ``SL``, reduce-only, owned by this lineage, live, and sized to
        exactly ``position_lots``. Take-profit never substitutes.
        """
        if snapshot.lot is None:
            return None
        for order in snapshot.open_orders:
            if str(order.coin) != snapshot.symbol:
                continue
            if str(order.status).upper() not in _LIVE_ORDER_STATUSES:
                continue
            if str(order.role).upper() != "SL":
                continue
            if not order.reduce_only:
                continue
            if str(order.side).upper() != str(exit_side).upper():
                continue
            if str(order.cloid) not in owned_cloids:
                continue
            try:
                if quantize_lots(abs(float(order.size)), snapshot.lot) != position_lots:
                    continue
            except LotQuantizationError:
                continue
            return order
        return None

    def _position_is_protected(
        self, position: Position, open_orders: list[BrokerOrder]
    ) -> bool:
        """Quantity-aware repair of the previously quantity-blind reconcile.

        The old rule accepted *any* matched SL order as protection for a
        symbol, so an undersized, oversized, wrong-side or non-reduce-only stop
        was silently reported as safe. The same exact-quantity predicate now
        governs both placement verification and reconciliation.
        """
        lot = self._broker_lot_unit(position.symbol)
        wanted_side = exit_side_for(position.size)
        for order in open_orders:
            if getattr(order, "coin", None) != position.symbol:
                continue
            if str(getattr(order, "role", "")) != "SL":
                continue
            if not bool(getattr(order, "reduce_only", False)):
                continue
            if str(getattr(order, "side", "")).upper() != wanted_side:
                continue
            if str(getattr(order, "status", "OPEN")).upper() not in _LIVE_ORDER_STATUSES:
                continue
            if not exact_size_equal(float(order.size), float(position.size), lot):
                continue
            if self._match_order(order) is None:
                continue
            return True
        return False

    def _broker_lot_unit(self, symbol: str) -> LotUnit | None:
        getter = getattr(self.broker, "lot_unit", None)
        if not callable(getter):
            return None
        try:
            lot = getter(symbol)
        except Exception:  # noqa: BLE001 - a broken quantum is "unknown"
            return None
        return lot if isinstance(lot, LotUnit) else None

    # ---------------- runner ----------------

    async def run_partial_recoveries(self) -> None:
        """Drive every active recovery generation; safe to call repeatedly."""
        if not self.store.partial_protection_enabled():
            return
        if self.store.has_submission_quarantine():
            return
        await self._legacy_partial_scan()
        for recovery in self.store.list_partial_recoveries():
            if str(recovery["state"]) in {
                state.value for state in PARTIAL_TERMINAL_STATES
            }:
                continue
            await self.run_partial_recovery(str(recovery["symbol"]))

    async def run_partial_recovery(
        self, symbol: str, *, max_cycles: int = 16
    ) -> str | None:
        """Run one bounded protect-or-flatten sequence for ``symbol``."""
        if not self.store.partial_protection_enabled():
            return None
        async with self.symbol_locks.hold(symbol):
            recovery = self.store.active_partial_recovery_for_symbol(symbol)
            if recovery is None:
                return None
            if self.store.has_submission_quarantine():
                # Dominant TS-P1-003 quarantine: defer, do not abort, do not
                # reserve, do not mutate.
                self._partial_event(
                    "WARN", "PARTIAL_RECOVERY_DEFERRED_QUARANTINE", symbol
                )
                return str(recovery["state"])
            broker = self._partial_broker()
            if broker is None:
                self._abort(recovery, "RECOVERY_API_UNAVAILABLE")
                return PartialProtectionState.UNPROTECTED_ABORT.value
            self._arm_monotonic_deadline(recovery, "protect", PROTECT_DEADLINE_S)
            for _ in range(max_cycles):
                current = self.store.get_partial_recovery(
                    str(recovery["recovery_id"])
                )
                if current is None:  # pragma: no cover - defensive
                    return None
                if str(current["state"]) in {
                    state.value for state in PARTIAL_TERMINAL_STATES
                }:
                    return str(current["state"])
                if not await self._partial_cycle(current, broker):
                    return str(current["state"])
            final = self.store.get_partial_recovery(str(recovery["recovery_id"]))
            return None if final is None else str(final["state"])

    async def _partial_cycle(
        self, recovery: Mapping[str, Any], broker: Any
    ) -> bool:
        state = PartialProtectionState(str(recovery["state"]))
        if state is PartialProtectionState.PARTIAL_DETECTED:
            return await self._cycle_detected(recovery, broker)
        if state is PartialProtectionState.PROTECTION_PENDING:
            return await self._cycle_protection_pending(recovery, broker)
        if state is PartialProtectionState.PROTECTION_VERIFIED:
            return await self._cycle_protection_verified(recovery, broker)
        if state in {
            PartialProtectionState.CANCEL_PENDING,
            PartialProtectionState.CANCEL_UNKNOWN,
        }:
            return await self._cycle_cancel(recovery, broker)
        if state in {
            PartialProtectionState.FLATTEN_PENDING,
            PartialProtectionState.FLATTEN_UNKNOWN,
        }:
            return await self._cycle_flatten(recovery, broker)
        return False

    def _abort(self, recovery: Mapping[str, Any], reason: str) -> None:
        """Durable fail-closed end state. Never called after a pending mutation."""
        symbol = str(recovery["symbol"])
        try:
            self.store.transition_partial_recovery(
                str(recovery["recovery_id"]),
                expected=str(recovery["state"]),
                target=PartialProtectionState.UNPROTECTED_ABORT.value,
                reason_code=reason,
            )
        except PartialRecoveryConflictError:
            pass
        self._disarm_for_partial("UNPROTECTED_ABORT", symbol, reason)

    async def _cycle_detected(
        self, recovery: Mapping[str, Any], broker: Any
    ) -> bool:
        snapshot = await self._snapshot(broker, recovery)
        provenance, position_lots, reason = self._classify(recovery, snapshot)
        if provenance is not Provenance.OWNED:
            if provenance is Provenance.UNVERIFIED and not self._deadline_expired(
                recovery, "protect"
            ):
                self._partial_event(
                    "WARN", "PARTIAL_EVIDENCE_INCOMPLETE", str(recovery["symbol"]), reason
                )
                return False
            self._abort(recovery, reason)
            return True
        if position_lots is None or snapshot.lot is None:  # pragma: no cover
            self._abort(recovery, "QUANTITY_UNRESOLVED")
            return True
        trade = self.store.get_trade(int(recovery["trade_id"]))
        if trade is None or trade["sl_initial"] is None:
            self._abort(recovery, "PROTECTION_PRICE_UNAVAILABLE")
            return True
        if position_lots == 0:
            # Nothing live to protect: prove the entry terminal, then prove flat.
            return await self._begin_cancel(
                recovery, broker, position_lots=0,
                fields={
                    "provenance": provenance.value,
                    "size_decimals": snapshot.lot.size_decimals,
                    "position_lots": 0,
                },
            )
        if self._deadline_expired(recovery, "protect"):
            return self._enter_flatten(recovery, "PROTECT_DEADLINE_EXPIRED", position_lots)
        exit_side = exit_side_for(float(snapshot.net_size or 0.0))
        action_id = compute_partial_action_id(
            kind=PartialActionKind.INSTALL_STOP.value,
            trade_id=int(recovery["trade_id"]),
            entry_cloid=str(recovery["entry_cloid"]),
            entry_request_id=str(recovery["entry_request_id"]),
            generation=int(recovery["generation"]),
            qty_lots=position_lots,
        )
        cloid = compute_partial_action_cloid(action_id)
        is_replay, _ = self.store.reserve_partial_action(
            recovery_id=str(recovery["recovery_id"]),
            action_id=action_id,
            kind=PartialActionKind.INSTALL_STOP.value,
            target_cloid=cloid,
            expected_state=PartialProtectionState.PARTIAL_DETECTED.value,
            next_state=PartialProtectionState.PROTECTION_PENDING.value,
            reason_code="PROTECTION_RESERVED",
            generation=int(recovery["generation"]),
            qty_lots=position_lots,
            provenance=provenance.value,
            size_decimals=snapshot.lot.size_decimals,
            position_lots=position_lots,
        )
        if not is_replay:
            await self._send_stop(
                recovery, broker, action_id, cloid, position_lots,
                snapshot.lot, exit_side, float(trade["sl_initial"]),
            )
        return True

    async def _send_stop(
        self,
        recovery: Mapping[str, Any],
        broker: Any,
        action_id: str,
        cloid: str,
        position_lots: int,
        lot: LotUnit,
        exit_side: str,
        trigger_px: float,
    ) -> None:
        symbol = str(recovery["symbol"])
        self.symbol_locks.require(symbol)
        self.store.record_partial_action_event(
            action_id=action_id, status=ActionRecordStatus.SENT.value,
            reason_code="PROTECTION_SENT", evidence_source="LOCAL",
            evidence={"qty_lots": position_lots, "exit_side": exit_side},
        )
        try:
            result = await broker.place_protective_stop(
                symbol=symbol, cloid=cloid, exit_side=exit_side,
                size=lots_to_size(position_lots, lot), trigger_px=trigger_px,
            )
        except Exception as exc:  # noqa: BLE001 - a raised adapter is UNKNOWN
            self._record_outcome(
                action_id, ActionOutcome.UNKNOWN, "PLACE_RAISED", type(exc).__name__
            )
            return
        self._record_typed_outcome(action_id, result, "PLACE")

    def _record_outcome(
        self, action_id: str, outcome: ActionOutcome, reason: str, detail: str = ""
    ) -> None:
        self.store.record_partial_action_event(
            action_id=action_id,
            status=ActionRecordStatus(outcome.value).value,
            reason_code=reason,
            evidence_source="BROKER",
            evidence={"detail": detail[:256]},
        )

    def _record_typed_outcome(self, action_id: str, result: Any, source: str) -> None:
        outcome = getattr(result, "outcome", None)
        if not isinstance(outcome, ActionOutcome):
            self._record_outcome(
                action_id, ActionOutcome.UNKNOWN, f"{source}_UNTYPED_RESULT"
            )
            return
        evidence = getattr(result, "evidence", None)
        reason = getattr(evidence, "reason_code", f"{source}_RESULT")
        self.store.record_partial_action_event(
            action_id=action_id,
            status=ActionRecordStatus(outcome.value).value,
            reason_code=str(reason),
            evidence_source=str(getattr(evidence, "source", source)),
            evidence=evidence.as_payload() if evidence is not None else {},
        )

    async def _cycle_protection_pending(
        self, recovery: Mapping[str, Any], broker: Any
    ) -> bool:
        snapshot = await self._snapshot(broker, recovery)
        position_lots = recovery["position_lots"]
        if position_lots is None:  # pragma: no cover - defensive
            self._abort(recovery, "QUANTITY_UNRESOLVED")
            return True
        action_id = compute_partial_action_id(
            kind=PartialActionKind.INSTALL_STOP.value,
            trade_id=int(recovery["trade_id"]),
            entry_cloid=str(recovery["entry_cloid"]),
            entry_request_id=str(recovery["entry_request_id"]),
            generation=int(recovery["generation"]),
            qty_lots=int(position_lots),
        )
        cloid = compute_partial_action_cloid(action_id)
        outcome = self.store.resolve_partial_action(action_id)
        expired = self._deadline_expired(recovery, "protect")

        if snapshot.exact and snapshot.lot is not None and snapshot.net_size is not None:
            try:
                live_lots = quantize_lots(abs(float(snapshot.net_size)), snapshot.lot)
            except LotQuantizationError:
                live_lots = None
            if live_lots is not None and live_lots != int(position_lots):
                # A newly observed fill invalidates the prior quantity proof.
                self.store.open_partial_generation(
                    recovery_id=str(recovery["recovery_id"]),
                    reason_code="LATE_FILL_REQUANTIFY",
                    position_lots=live_lots,
                )
                return True
            owned = self._owned_cloids(recovery)
            protection = self.qualifying_protection(
                snapshot,
                position_lots=int(position_lots),
                exit_side=exit_side_for(float(snapshot.net_size)),
                owned_cloids=owned,
            )
            if protection is not None:
                if outcome != ActionOutcome.APPLIED.value:
                    self._record_outcome(
                        action_id, ActionOutcome.APPLIED, "PROTECTION_OBSERVED_LIVE"
                    )
                self.store.transition_partial_recovery(
                    str(recovery["recovery_id"]),
                    expected=PartialProtectionState.PROTECTION_PENDING.value,
                    target=PartialProtectionState.PROTECTION_VERIFIED.value,
                    reason_code="PROTECTION_VERIFIED",
                )
                return True

        if expired:
            return self._enter_flatten(
                recovery, "PROTECT_DEADLINE_EXPIRED", int(position_lots)
            )
        if outcome == ActionOutcome.NOT_APPLIED.value:
            # Proven not applied: the *same* identity and cloid may be re-sent.
            trade = self.store.get_trade(int(recovery["trade_id"]))
            if trade is None or trade["sl_initial"] is None or snapshot.lot is None:
                self._abort(recovery, "PROTECTION_PRICE_UNAVAILABLE")
                return True
            await self._send_stop(
                recovery, broker, action_id, cloid, int(position_lots), snapshot.lot,
                exit_side_for(float(snapshot.net_size or 0.0)), float(trade["sl_initial"]),
            )
            return True
        # UNKNOWN or not yet acknowledged: evidence queries only, never a
        # second placement and never a new identity.
        await self._query_action(broker, recovery, action_id, cloid, "PROTECTION")
        return False

    async def _query_action(
        self,
        broker: Any,
        recovery: Mapping[str, Any],
        action_id: str,
        cloid: str,
        label: str,
    ) -> str | None:
        """Resolve an UNKNOWN action by direct evidence only."""
        symbol = str(recovery["symbol"])
        self.symbol_locks.require(symbol)
        try:
            result = await broker.query_order(cloid, symbol)
        except Exception as exc:  # noqa: BLE001
            self.store.record_partial_action_event(
                action_id=action_id, status=ActionRecordStatus.UNKNOWN.value,
                reason_code=f"{label}_QUERY_FAILED", evidence_source="BROKER",
                evidence={"detail": type(exc).__name__},
            )
            return None
        known = bool(getattr(result, "known", False))
        if not known:
            self.store.record_partial_action_event(
                action_id=action_id, status=ActionRecordStatus.UNKNOWN.value,
                reason_code=f"{label}_QUERY_UNKNOWN", evidence_source="BROKER",
                evidence={},
            )
            return None
        found = bool(getattr(result, "found", False))
        raw_status = getattr(result, "raw_status", None)
        # `found` means *live*. An order that exists but is already terminal
        # still proves the write landed, so it must never be folded to
        # NOT_APPLIED — that would authorize a re-issue of an applied action.
        # Only an authoritative absence (known, no order, no status) is
        # proof of non-application.
        applied = found or raw_status is not None
        status = ActionRecordStatus.APPLIED if applied else ActionRecordStatus.NOT_APPLIED
        self.store.record_partial_action_event(
            action_id=action_id, status=status.value,
            reason_code=f"{label}_QUERY_RESOLVED", evidence_source="BROKER",
            evidence={
                "found": found,
                "terminal": bool(getattr(result, "terminal", False)),
                "raw_status": str(raw_status) if raw_status is not None else None,
            },
        )
        return status.value

    async def _cycle_protection_verified(
        self, recovery: Mapping[str, Any], broker: Any
    ) -> bool:
        return await self._begin_cancel(
            recovery, broker, position_lots=int(recovery["position_lots"] or 0),
            fields={},
        )

    async def _begin_cancel(
        self,
        recovery: Mapping[str, Any],
        broker: Any,
        *,
        position_lots: int,
        fields: Mapping[str, Any],
    ) -> bool:
        action_id = compute_partial_action_id(
            kind=PartialActionKind.CANCEL_ENTRY.value,
            trade_id=int(recovery["trade_id"]),
            entry_cloid=str(recovery["entry_cloid"]),
            entry_request_id=str(recovery["entry_request_id"]),
        )
        is_replay, _ = self.store.reserve_partial_action(
            recovery_id=str(recovery["recovery_id"]),
            action_id=action_id,
            kind=PartialActionKind.CANCEL_ENTRY.value,
            target_cloid=str(recovery["entry_cloid"]),
            expected_state=str(recovery["state"]),
            next_state=PartialProtectionState.CANCEL_PENDING.value,
            reason_code="CANCEL_ENTRY_RESERVED",
            **dict(fields),
        )
        if not is_replay:
            await self._send_cancel(recovery, broker, action_id)
        return True

    async def _send_cancel(
        self, recovery: Mapping[str, Any], broker: Any, action_id: str
    ) -> None:
        symbol = str(recovery["symbol"])
        self.symbol_locks.require(symbol)
        cloid = str(recovery["entry_cloid"])
        self.store.record_partial_action_event(
            action_id=action_id, status=ActionRecordStatus.SENT.value,
            reason_code="CANCEL_ENTRY_SENT", evidence_source="LOCAL",
            evidence={"cloid": cloid},
        )
        try:
            result = await broker.cancel_order_by_cloid(cloid, symbol)
        except Exception as exc:  # noqa: BLE001
            self._record_outcome(
                action_id, ActionOutcome.UNKNOWN, "CANCEL_RAISED", type(exc).__name__
            )
            return
        self._record_typed_outcome(action_id, result, "CANCEL")

    async def _cycle_cancel(
        self, recovery: Mapping[str, Any], broker: Any
    ) -> bool:
        symbol = str(recovery["symbol"])
        entry_cloid = str(recovery["entry_cloid"])
        action_id = compute_partial_action_id(
            kind=PartialActionKind.CANCEL_ENTRY.value,
            trade_id=int(recovery["trade_id"]),
            entry_cloid=entry_cloid,
            entry_request_id=str(recovery["entry_request_id"]),
        )
        outcome = self.store.resolve_partial_action(action_id)
        try:
            query = await broker.query_order(entry_cloid, symbol)
        except Exception as exc:  # noqa: BLE001
            query = None
            self.store.record_partial_action_event(
                action_id=action_id, status=ActionRecordStatus.UNKNOWN.value,
                reason_code="ENTRY_QUERY_FAILED", evidence_source="BROKER",
                evidence={"detail": type(exc).__name__},
            )
        entry_terminal = bool(
            query is not None
            and getattr(query, "known", False)
            and getattr(query, "terminal", False)
        )
        entry_live = bool(
            query is not None
            and getattr(query, "known", False)
            and getattr(query, "found", False)
        )
        expired = self._deadline_expired(recovery, "protect")

        if entry_terminal:
            return await self._resolve_after_entry_terminal(recovery, broker)
        if expired:
            return self._enter_flatten(
                recovery, "PROTECT_DEADLINE_EXPIRED",
                int(recovery["position_lots"] or 0),
            )
        if entry_live and outcome == ActionOutcome.NOT_APPLIED.value:
            # Proven not applied and still live: same identity may be re-sent.
            await self._send_cancel(recovery, broker, action_id)
            return True
        if str(recovery["state"]) != PartialProtectionState.CANCEL_UNKNOWN.value and (
            outcome == ActionOutcome.UNKNOWN.value or query is None
            or not getattr(query, "known", False)
        ):
            self.store.transition_partial_recovery(
                str(recovery["recovery_id"]),
                expected=str(recovery["state"]),
                target=PartialProtectionState.CANCEL_UNKNOWN.value,
                reason_code="CANCEL_OUTCOME_UNKNOWN",
            )
            return True
        return False

    async def _resolve_after_entry_terminal(
        self, recovery: Mapping[str, Any], broker: Any
    ) -> bool:
        snapshot = await self._snapshot(broker, recovery)
        provenance, position_lots, reason = self._classify(recovery, snapshot)
        if provenance is not Provenance.OWNED:
            if provenance is Provenance.UNVERIFIED and not self._deadline_expired(
                recovery, "protect"
            ):
                return False
            self._abort(recovery, reason)
            return True
        if position_lots is None or snapshot.lot is None:  # pragma: no cover
            self._abort(recovery, "QUANTITY_UNRESOLVED")
            return True
        if position_lots != int(recovery["position_lots"] or 0):
            self.store.open_partial_generation(
                recovery_id=str(recovery["recovery_id"]),
                reason_code="LATE_FILL_REQUANTIFY",
                position_lots=position_lots,
            )
            return True
        if position_lots == 0:
            return await self._verify_safe_flat(recovery, broker, snapshot)
        protection = self.qualifying_protection(
            snapshot,
            position_lots=position_lots,
            exit_side=exit_side_for(float(snapshot.net_size or 0.0)),
            owned_cloids=self._owned_cloids(recovery),
        )
        if protection is None:
            if self._deadline_expired(recovery, "protect"):
                return self._enter_flatten(
                    recovery, "PROTECTION_LOST", position_lots
                )
            return False
        self.store.transition_partial_recovery(
            str(recovery["recovery_id"]),
            expected=str(recovery["state"]),
            target=PartialProtectionState.PROTECTED_PARTIAL.value,
            reason_code="PROTECTED_PARTIAL",
            position_lots=position_lots,
        )
        self._partial_event(
            "WARN", "PARTIAL_PROTECTED", str(recovery["symbol"]),
            f"lots={position_lots} generation={recovery['generation']}",
        )
        return True

    def _enter_flatten(
        self, recovery: Mapping[str, Any], reason: str, position_lots: int
    ) -> bool:
        """Start the separately bounded flatten phase (5s, non-resetting)."""
        flatten_deadline = recovery["flatten_deadline_ts"] or (
            self.store.now() + timedelta(seconds=FLATTEN_VERIFY_DEADLINE_S)
        )
        updated = self.store.transition_partial_recovery(
            str(recovery["recovery_id"]),
            expected=str(recovery["state"]),
            target=PartialProtectionState.FLATTEN_PENDING.value,
            reason_code=reason,
            flatten_deadline_ts=flatten_deadline,
            position_lots=position_lots,
        )
        self._arm_monotonic_deadline(updated, "flatten", FLATTEN_VERIFY_DEADLINE_S)
        self._partial_event(
            "WARN", "PARTIAL_FLATTEN_STARTED", str(recovery["symbol"]), reason
        )
        return True

    async def _cycle_flatten(
        self, recovery: Mapping[str, Any], broker: Any
    ) -> bool:
        self._arm_monotonic_deadline(recovery, "flatten", FLATTEN_VERIFY_DEADLINE_S)
        symbol = str(recovery["symbol"])
        snapshot = await self._snapshot(broker, recovery)
        expired = self._deadline_expired(recovery, "flatten")
        if not snapshot.exact or snapshot.lot is None or snapshot.net_size is None:
            if expired:
                self._abort(recovery, "FLATTEN_EVIDENCE_INCOMPLETE")
                return True
            self._partial_event("WARN", "PARTIAL_EVIDENCE_INCOMPLETE", symbol)
            return False
        try:
            live_lots = quantize_lots(abs(float(snapshot.net_size)), snapshot.lot)
        except LotQuantizationError as exc:
            self._abort(recovery, exc.reason_code)
            return True

        if live_lots == 0:
            return await self._verify_safe_flat(recovery, broker, snapshot)
        if expired:
            self._abort(recovery, "FLATTEN_DEADLINE_EXPIRED")
            return True

        seq = int(recovery["flatten_seq"])
        attempts = [
            row
            for row in self.store.partial_actions_for_recovery(
                str(recovery["recovery_id"]), PartialActionKind.FLATTEN.value
            )
            if int(row["flatten_seq"] or 0) == seq
        ]
        if attempts:
            outcome = self.store.resolve_partial_action(str(attempts[0]["action_id"]))
            if outcome in (None, ActionOutcome.UNKNOWN.value):
                # Position evidence is the only authority here and it still
                # shows a remainder. The attempt sequence stays frozen: an
                # unknown flatten never mints a second market close.
                if str(recovery["state"]) != PartialProtectionState.FLATTEN_UNKNOWN.value:
                    self.store.transition_partial_recovery(
                        str(recovery["recovery_id"]),
                        expected=str(recovery["state"]),
                        target=PartialProtectionState.FLATTEN_UNKNOWN.value,
                        reason_code="FLATTEN_OUTCOME_UNKNOWN",
                    )
                    return True
                self._partial_event(
                    "WARN", "PARTIAL_FLATTEN_UNRESOLVED", symbol, f"seq={seq}"
                )
                return False
            # Definitive outcome plus authoritative proof of a nonzero
            # remainder: only now may the sequence advance.
            self.store.bump_partial_flatten_seq(str(recovery["recovery_id"]), seq)
            return True
        action_id = compute_partial_action_id(
            kind=PartialActionKind.FLATTEN.value,
            trade_id=int(recovery["trade_id"]),
            entry_cloid=str(recovery["entry_cloid"]),
            entry_request_id=str(recovery["entry_request_id"]),
            generation=int(recovery["generation"]),
            flatten_seq=seq,
            qty_lots=live_lots,
        )
        cloid = compute_partial_action_cloid(action_id)
        is_replay, _ = self.store.reserve_partial_action(
            recovery_id=str(recovery["recovery_id"]),
            action_id=action_id,
            kind=PartialActionKind.FLATTEN.value,
            target_cloid=cloid,
            expected_state=str(recovery["state"]),
            next_state=PartialProtectionState.FLATTEN_PENDING.value,
            reason_code="FLATTEN_RESERVED",
            generation=int(recovery["generation"]),
            flatten_seq=seq,
            qty_lots=live_lots,
            position_lots=live_lots,
        )
        if not is_replay:
            await self._send_flatten(
                recovery, broker, action_id, cloid, live_lots, snapshot.lot
            )
        return True

    async def _send_flatten(
        self,
        recovery: Mapping[str, Any],
        broker: Any,
        action_id: str,
        cloid: str,
        live_lots: int,
        lot: LotUnit,
    ) -> None:
        symbol = str(recovery["symbol"])
        self.symbol_locks.require(symbol)
        self.store.record_partial_action_event(
            action_id=action_id, status=ActionRecordStatus.SENT.value,
            reason_code="FLATTEN_SENT", evidence_source="LOCAL",
            evidence={"qty_lots": live_lots},
        )
        try:
            result = await broker.flatten_reduce_only(
                symbol=symbol, cloid=cloid, size=lots_to_size(live_lots, lot)
            )
        except Exception as exc:  # noqa: BLE001
            self._record_outcome(
                action_id, ActionOutcome.UNKNOWN, "FLATTEN_RAISED", type(exc).__name__
            )
            return
        self._record_typed_outcome(action_id, result, "FLATTEN")

    async def _verify_safe_flat(
        self, recovery: Mapping[str, Any], broker: Any, snapshot: SymbolSnapshot
    ) -> bool:
        """SAFE_FLAT requires fresh exact evidence on every owned artefact."""
        symbol = str(recovery["symbol"])
        entry_cloid = str(recovery["entry_cloid"])
        owned = self._owned_cloids(recovery)
        try:
            entry_query = await broker.query_order(entry_cloid, symbol)
        except Exception:  # noqa: BLE001
            entry_query = None
        entry_terminal = bool(
            entry_query is not None
            and getattr(entry_query, "known", False)
            and getattr(entry_query, "terminal", False)
        )
        in_flatten = str(recovery["state"]) in {
            PartialProtectionState.FLATTEN_PENDING.value,
            PartialProtectionState.FLATTEN_UNKNOWN.value,
        }
        if not entry_terminal:
            if not in_flatten:
                if self._deadline_expired(recovery, "protect"):
                    return self._enter_flatten(recovery, "ENTRY_NOT_TERMINAL", 0)
                return False
            if self._deadline_expired(recovery, "flatten"):
                # Bounded budget spent with a proven-live owned entry remainder.
                self._abort(recovery, "ENTRY_LIVE_AT_FLATTEN")
                return True
            # Position is flat but the owned entry remainder can still fill:
            # drive the stable CANCEL_ENTRY identity to a terminal answer.
            return await self._ensure_entry_cancelled(recovery, broker, entry_query)
        orphans = [
            order
            for order in snapshot.open_orders
            if str(order.coin) == symbol
            and str(order.status).upper() in _LIVE_ORDER_STATUSES
            and str(order.cloid) in owned
        ]
        if orphans:
            if not in_flatten:
                return self._enter_flatten(recovery, "ORPHAN_PROTECTION_LIVE", 0)
            if self._deadline_expired(recovery, "flatten"):
                self._abort(recovery, "ORPHAN_PROTECTION_LIVE")
                return True
            await self._cancel_orphan(recovery, broker, orphans[0])
            return True
        self.store.transition_partial_recovery(
            str(recovery["recovery_id"]),
            expected=str(recovery["state"]),
            target=PartialProtectionState.SAFE_FLAT.value,
            reason_code="SAFE_FLAT",
            position_lots=0,
        )
        self._partial_event("WARN", "PARTIAL_SAFE_FLAT", symbol)
        return True

    async def _ensure_entry_cancelled(
        self, recovery: Mapping[str, Any], broker: Any, entry_query: Any
    ) -> bool:
        """Drive the stable CANCEL_ENTRY identity without changing state.

        Used from the flatten phase, where the position may already be flat but
        the owned entry remainder can still fill. The identity is the same one
        the ordinary path uses, so a replay never mints a second cancel and an
        UNKNOWN outcome stays query-only.
        """
        action_id = compute_partial_action_id(
            kind=PartialActionKind.CANCEL_ENTRY.value,
            trade_id=int(recovery["trade_id"]),
            entry_cloid=str(recovery["entry_cloid"]),
            entry_request_id=str(recovery["entry_request_id"]),
        )
        reserved = {
            str(row["action_id"])
            for row in self.store.partial_actions_for_recovery(
                str(recovery["recovery_id"]), PartialActionKind.CANCEL_ENTRY.value
            )
        }
        if action_id not in reserved:
            self.store.reserve_partial_action(
                recovery_id=str(recovery["recovery_id"]),
                action_id=action_id,
                kind=PartialActionKind.CANCEL_ENTRY.value,
                target_cloid=str(recovery["entry_cloid"]),
                expected_state=str(recovery["state"]),
                next_state=str(recovery["state"]),
                reason_code="CANCEL_ENTRY_RESERVED",
            )
            await self._send_cancel(recovery, broker, action_id)
            return True
        outcome = self.store.resolve_partial_action(action_id)
        entry_live = bool(
            entry_query is not None
            and getattr(entry_query, "known", False)
            and getattr(entry_query, "found", False)
        )
        if outcome == ActionOutcome.NOT_APPLIED.value and entry_live:
            await self._send_cancel(recovery, broker, action_id)
            return True
        self._partial_event(
            "WARN", "PARTIAL_ENTRY_CANCEL_UNRESOLVED", str(recovery["symbol"])
        )
        return False

    async def _cancel_orphan(
        self, recovery: Mapping[str, Any], broker: Any, order: OrderView
    ) -> None:
        """Remove an owned protective order left behind by a completed flatten."""
        symbol = str(recovery["symbol"])
        self.symbol_locks.require(symbol)
        action_id = compute_partial_action_id(
            kind=PartialActionKind.CANCEL_PROTECTION.value,
            trade_id=int(recovery["trade_id"]),
            entry_cloid=str(recovery["entry_cloid"]),
            entry_request_id=str(recovery["entry_request_id"]),
            target_cloid=str(order.cloid),
        )
        is_replay, _ = self.store.reserve_partial_action(
            recovery_id=str(recovery["recovery_id"]),
            action_id=action_id,
            kind=PartialActionKind.CANCEL_PROTECTION.value,
            target_cloid=str(order.cloid),
            expected_state=str(recovery["state"]),
            next_state=str(recovery["state"]),
            reason_code="CANCEL_PROTECTION_RESERVED",
        )
        outcome = self.store.resolve_partial_action(action_id)
        if is_replay and outcome == ActionOutcome.UNKNOWN.value:
            await self._query_action(
                broker, recovery, action_id, str(order.cloid), "ORPHAN"
            )
            return
        self.store.record_partial_action_event(
            action_id=action_id, status=ActionRecordStatus.SENT.value,
            reason_code="CANCEL_PROTECTION_SENT", evidence_source="LOCAL",
            evidence={"cloid": str(order.cloid)},
        )
        try:
            result = await broker.cancel_order_by_cloid(str(order.cloid), symbol)
        except Exception as exc:  # noqa: BLE001
            self._record_outcome(
                action_id, ActionOutcome.UNKNOWN, "CANCEL_RAISED", type(exc).__name__
            )
            return
        self._record_typed_outcome(action_id, result, "CANCEL")

    # ---------------- startup / legacy ----------------

    async def _legacy_partial_scan(self) -> None:
        """One startup pass over pre-existing owned partial entries.

        Runs after the atomic schema migration and entirely inside
        ``OrderManager``: ``store/db.py`` performs no broker I/O. Strong
        evidence (durable identity + local fills + an exact locked snapshot
        that agrees) opens a recovery generation whose deadline is seeded
        conservatively from the earliest durable fill — never a fresh 10s
        window. Weak, incomplete or mixed evidence opens nothing and mutates
        nothing.
        """
        if self._legacy_partial_scan_done:
            return
        self._legacy_partial_scan_done = True
        if not self.store.partial_protection_enabled():
            return
        broker = self._partial_broker()
        for candidate in self.store.legacy_partial_entry_candidates():
            symbol = str(candidate["coin"])
            if self.store.active_partial_recovery_for_symbol(symbol) is not None:
                continue
            async with self.symbol_locks.hold(symbol):
                first_fill = self._parse_utc(candidate["first_fill_ts"])
                if first_fill is None:
                    self._disarm_for_partial(
                        "PARTIAL_LEGACY_EVIDENCE_WEAK", symbol,
                        f"cloid={candidate['cloid']} no first-fill evidence",
                    )
                    continue
                if broker is None:
                    self._disarm_for_partial(
                        "PARTIAL_LEGACY_EVIDENCE_WEAK", symbol,
                        "recovery API unavailable",
                    )
                    continue
                # Conservative seeding: the budget is measured from the earliest
                # durable fill, so an old partial starts already expired.
                deadline = first_fill + timedelta(seconds=PROTECT_DEADLINE_S)
                request_id = str(
                    candidate["group_id"]
                    or candidate["order_ref"]
                    or candidate["decision_uid"]
                )
                try:
                    self.store.open_partial_recovery(
                        run_id=self.run_id,
                        symbol=symbol,
                        trade_id=int(candidate["trade_id"]),
                        entry_cloid=str(candidate["cloid"]),
                        entry_decision_uid=str(candidate["decision_uid"]),
                        entry_request_id=request_id,
                        first_observed_ts=first_fill,
                        protect_deadline_ts=deadline,
                        reason_code="PARTIAL_LEGACY_RECOVERED",
                    )
                except PartialRecoveryConflictError as exc:
                    self._disarm_for_partial(
                        "PARTIAL_RECOVERY_OPEN_FAILED", symbol, exc.code
                    )
                    continue
                self._disarm_for_partial(
                    "PARTIAL_LEGACY_DETECTED", symbol,
                    f"cloid={candidate['cloid']} filled={candidate['filled_qty']}",
                )

    # ---------------- human re-ARM gate ----------------

    async def confirm_partial_rearm(self, recovery_id: str) -> bool:
        """Human re-ARM proof for a PROTECTED_PARTIAL generation.

        Requires a *fresh* exact snapshot under the same per-symbol lock that
        still shows exact protection for the live quantity. Only then is the
        generation archived and the position handed back to ordinary
        trail/close management.
        """
        recovery = self.store.get_partial_recovery(recovery_id)
        if recovery is None:
            return False
        if str(recovery["state"]) != PartialProtectionState.PROTECTED_PARTIAL.value:
            return False
        broker = self._partial_broker()
        if broker is None:
            return False
        symbol = str(recovery["symbol"])
        async with self.symbol_locks.hold(symbol):
            snapshot = await self._snapshot(broker, recovery)
            provenance, position_lots, _ = self._classify(recovery, snapshot)
            if provenance is not Provenance.OWNED or position_lots is None:
                return False
            if position_lots == 0:
                return False
            protection = self.qualifying_protection(
                snapshot,
                position_lots=position_lots,
                exit_side=exit_side_for(float(snapshot.net_size or 0.0)),
                owned_cloids=self._owned_cloids(recovery),
            )
            if protection is None:
                return False
            self.store.transition_partial_recovery(
                recovery_id,
                expected=PartialProtectionState.PROTECTED_PARTIAL.value,
                target=PartialProtectionState.PROTECTED_PARTIAL.value,
                reason_code="REARM_ARCHIVED",
                position_lots=position_lots,
            )
            self._partial_event("INFO", "PARTIAL_RECOVERY_ARCHIVED", symbol)
            return True

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
