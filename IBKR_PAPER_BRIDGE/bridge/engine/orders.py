"""OrderManager for bracket submission, reconciliation, and fill tracking."""

from __future__ import annotations

import asyncio
import inspect
import json
import time
from collections.abc import Mapping, Sequence
from contextlib import asynccontextmanager
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
    KILL_VERIFY_DEADLINE_S,
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
    KillActionKind,
    KillEvidenceCapture,
    KillEvidenceEpoch,
    KillTerminalState,
    OrderPlan,
    OrderQueryResult,
    OrderState,
    OrderUpdateEvent,
    OrderView,
    PartialActionKind,
    PartialProtectionState,
    Position,
    Provenance,
    ReconcileComponentStatus,
    SymbolSnapshot,
    canonical_order_state,
    lots_to_size,
    quantize_lots,
)
from bridge.store.db import (
    IdentityCollisionError,
    KillConflictError,
    OrderCollisionError,
    PartialRecoveryConflictError,
    Store,
    compute_intent_identity,
    compute_kill_action_cloid,
    compute_kill_action_id,
    compute_partial_action_cloid,
    compute_partial_action_id,
    compute_partial_recovery_id,
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

_KILL_RECOVERY_METHODS = (
    "lot_unit",
    "capture_kill_evidence",
    "symbol_snapshot",
    "query_order",
    "kill_cancel_order_by_cloid",
    "kill_flatten_reduce_only",
)

_LIVE_ORDER_STATUSES = frozenset({
    "OPEN",
    "SUBMITTED",
    "PENDING",
    "RESTING",
    "PARTIALLY_FILLED",
    "PENDING_CANCEL",
})


class SymbolLockNotHeld(RuntimeError):
    """Programming error: an owned mutation was attempted outside the lock."""

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.reason_code = "SYMBOL_LOCK_NOT_HELD"
        super().__init__(f"{self.reason_code}: {symbol}")


class _KillEvidenceFault(RuntimeError):
    """Secret-safe local validation failure for one kill observation."""

    def __init__(self, state: KillTerminalState, reason_code: str) -> None:
        self.state = state
        self.reason_code = reason_code
        super().__init__(reason_code)


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


@asynccontextmanager
async def _kill_full_writer_scope(store: Store, *, already_held: bool):
    """Reuse the caller-owned full writer; otherwise acquire it exactly once."""
    if already_held:
        yield
        return
    from bridge.engine.reconcile import full_writer_guard

    async with full_writer_guard(store):
        yield


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
        self._kill_mono_deadlines: dict[str, float] = {}
        self._active_kill_epoch: KillEvidenceEpoch | None = None
        # Set before any KILL persistence or broker await. The final submit
        # boundary consults this in-memory latch even if SQLite is unavailable.
        self.kill_latched = False
        self.symbol_locks = SymbolLockRegistry()
        self._legacy_partial_scan_done = False
        subscribe = getattr(self.broker, "subscribe_user_events", None)
        if subscribe is not None:
            subscribe(self._queue_event)

    # ------------------------------------------------------------------
    # TS-P1-009 durable, owned-only kill coordinator
    # ------------------------------------------------------------------

    @staticmethod
    def _kill_reason(value: object, fallback: str = "KILL_EVIDENCE_INVALID") -> str:
        text = "".join(
            char if char.isalnum() or char in {"_", "-", ":"} else "_"
            for char in str(value or fallback).upper()
        )
        return (text or fallback)[:96]

    def _kill_now(self) -> datetime:
        value = self.store._clock()  # trusted local clock used by the ledger
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    @staticmethod
    def _kill_evidence_payload(value: Any) -> dict[str, Any]:
        evidence = getattr(value, "evidence", value)
        if isinstance(evidence, Evidence):
            payload = evidence.as_payload()
        else:
            payload = {"source": "LOCAL", "reason_code": "EVIDENCE_UNAVAILABLE"}
        if isinstance(value, OrderQueryResult):
            payload["query"] = {
                "known": bool(value.known),
                "found": bool(value.found),
                "terminal": bool(value.terminal),
                "raw_status": value.raw_status,
                "filled_size": value.filled_size,
                "oid": value.oid,
                "cloid": value.cloid,
                "symbol": value.symbol,
            }
        return payload

    def _kill_broker_available(self) -> bool:
        return all(callable(getattr(self.broker, name, None)) for name in _KILL_RECOVERY_METHODS)

    def _kill_epoch(self) -> KillEvidenceEpoch:
        if self._active_kill_epoch is None:
            raise _KillEvidenceFault(
                KillTerminalState.UNKNOWN, "KILL_EPOCH_INACTIVE"
            )
        return self._active_kill_epoch

    def _assert_kill_epoch_active(self) -> None:
        self.store.assert_kill_epoch_active(self._kill_epoch())

    def _kill_epoch_guard(self) -> Callable[[KillEvidenceEpoch], None]:
        def guard(epoch: KillEvidenceEpoch) -> None:
            self.store.assert_kill_epoch_active_for_mutation(epoch)

        return guard

    def _require_kill_capture(
        self, capture: Any, *, symbol: str
    ) -> KillEvidenceCapture:
        if not isinstance(capture, KillEvidenceCapture):
            raise _KillEvidenceFault(
                KillTerminalState.UNKNOWN, "KILL_CAPTURE_UNAVAILABLE"
            )
        if capture.epoch != self._kill_epoch() or capture.symbol != symbol:
            raise _KillEvidenceFault(
                KillTerminalState.UNKNOWN, "KILL_CAPTURE_EPOCH_MISMATCH"
            )
        if not capture.accepted:
            invalid = next(
                component
                for component in (
                    capture.positions,
                    capture.open_orders,
                    capture.fills,
                )
                if not component.accepted
            )
            ambiguous = invalid.status in {
                ReconcileComponentStatus.MALFORMED,
                ReconcileComponentStatus.CONFLICTING,
            } or any(
                marker in str(invalid.reason_code).upper()
                for marker in ("MALFORMED", "CONFLICT")
            )
            raise _KillEvidenceFault(
                (
                    KillTerminalState.AMBIGUOUS
                    if ambiguous
                    else KillTerminalState.UNKNOWN
                ),
                invalid.reason_code if ambiguous else capture.reason_code,
            )
        return capture

    async def _kill_snapshot(self, symbol: str) -> SymbolSnapshot:
        try:
            snapshot = await asyncio.wait_for(
                self.broker.symbol_snapshot(symbol),
                timeout=KILL_VERIFY_DEADLINE_S,
            )
        except asyncio.TimeoutError as exc:
            raise _KillEvidenceFault(
                KillTerminalState.UNKNOWN, "SYMBOL_SNAPSHOT_TIMEOUT"
            ) from exc
        except Exception as exc:
            raise _KillEvidenceFault(
                KillTerminalState.UNKNOWN,
                f"SYMBOL_SNAPSHOT_FAILED_{type(exc).__name__}",
            ) from exc
        if (
            not isinstance(snapshot, SymbolSnapshot)
            or snapshot.symbol != symbol
            or not snapshot.exact
            or snapshot.lot is None
            or snapshot.net_size is None
            or snapshot.observed_ts is None
        ):
            raise _KillEvidenceFault(
                KillTerminalState.UNRESOLVED, "SYMBOL_SNAPSHOT_NOT_EXACT"
            )
        return snapshot

    def _kill_model(
        self,
        snapshot: SymbolSnapshot,
        *,
        symbol: str,
        capture: KillEvidenceCapture,
    ) -> dict[str, Any]:
        """Validate the complete observation before authorizing any mutation."""
        lot = snapshot.lot
        if lot is None:
            raise _KillEvidenceFault(
                KillTerminalState.UNRESOLVED, "SIZE_QUANTUM_UNAVAILABLE"
            )
        try:
            observed_lots = quantize_lots(abs(float(snapshot.net_size)), lot)
        except (LotQuantizationError, TypeError, ValueError) as exc:
            reason = getattr(exc, "reason_code", "POSITION_QUANTITY_INVALID")
            raise _KillEvidenceFault(KillTerminalState.AMBIGUOUS, reason) from exc
        observed_signed = observed_lots if float(snapshot.net_size) >= 0 else -observed_lots

        exchange_by_alias: dict[str, OrderView] = {}
        for order in snapshot.open_orders:
            cloid = str(order.cloid).strip()
            alias = cloid.casefold()
            if (
                not cloid
                or alias in exchange_by_alias
                or str(order.coin) != symbol
                or str(order.side).upper() not in {"BUY", "SELL"}
                or str(order.status).upper() not in _LIVE_ORDER_STATUSES
            ):
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "ORDER_IDENTITY_AMBIGUOUS"
                )
            try:
                size_lots = quantize_lots(abs(float(order.size)), lot)
            except (LotQuantizationError, TypeError, ValueError) as exc:
                reason = getattr(exc, "reason_code", "ORDER_QUANTITY_INVALID")
                raise _KillEvidenceFault(KillTerminalState.AMBIGUOUS, reason) from exc
            if size_lots <= 0:
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "ORDER_QUANTITY_NON_POSITIVE"
                )
            exchange_by_alias[alias] = order

        unknown = [
            row
            for row in self.store.local_orders_with_unknown_status()
            if str(row.get("symbol") or "") == symbol
        ]
        if unknown:
            raise _KillEvidenceFault(
                KillTerminalState.UNRESOLVED, "LOCAL_ORDER_STATUS_UNKNOWN"
            )

        local_live = [
            row
            for row in self.store.live_local_orders()
            if str(row.get("symbol") or "") == symbol
        ]
        local_aliases: set[str] = set()
        risk_orders: list[tuple[dict[str, Any], OrderView | None]] = []
        protection_orders: list[tuple[dict[str, Any], OrderView]] = []
        owned_cloids: set[str] = set()
        for row in local_live:
            cloid = str(row.get("cloid") or "").strip()
            alias = cloid.casefold()
            if not cloid or alias in local_aliases:
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "LOCAL_ORDER_IDENTITY_AMBIGUOUS"
                )
            local_aliases.add(alias)
            owned_cloids.add(cloid)
            try:
                local_lots = quantize_lots(abs(float(row["qty"])), lot)
            except (KeyError, LotQuantizationError, TypeError, ValueError) as exc:
                reason = getattr(exc, "reason_code", "LOCAL_ORDER_QUANTITY_INVALID")
                raise _KillEvidenceFault(KillTerminalState.AMBIGUOUS, reason) from exc
            if local_lots <= 0:
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "LOCAL_ORDER_QUANTITY_NON_POSITIVE"
                )
            observed = exchange_by_alias.get(alias)
            role = str(row.get("role") or "").upper()
            if observed is not None:
                try:
                    exchange_lots = quantize_lots(abs(float(observed.size)), lot)
                except (LotQuantizationError, TypeError, ValueError) as exc:
                    reason = getattr(exc, "reason_code", "ORDER_QUANTITY_INVALID")
                    raise _KillEvidenceFault(
                        KillTerminalState.AMBIGUOUS, reason
                    ) from exc
                if (
                    str(observed.cloid) != cloid
                    or exchange_lots != local_lots
                    or str(observed.role).upper() not in {role, "UNKNOWN"}
                ):
                    raise _KillEvidenceFault(
                        KillTerminalState.AMBIGUOUS, "OWNED_ORDER_EVIDENCE_CONFLICT"
                    )
            if role == "ENTRY":
                if observed is not None and bool(observed.reduce_only):
                    raise _KillEvidenceFault(
                        KillTerminalState.AMBIGUOUS, "ENTRY_REDUCE_ONLY_CONFLICT"
                    )
                risk_orders.append((row, observed))
            else:
                if observed is not None:
                    if not bool(observed.reduce_only):
                        raise _KillEvidenceFault(
                            KillTerminalState.AMBIGUOUS,
                            "PROTECTION_NOT_REDUCE_ONLY",
                        )
                    protection_orders.append((row, observed))

        expected_signed = 0
        trade_nets: dict[int, int] = {}
        trade_directions: dict[int, str] = {}
        trade_decisions: dict[int, str] = {}
        durable_capture_identities: set[tuple[str, int]] = set()
        durable_capture_lots_by_oid: dict[int, int] = {}
        owned_position_rows = self.store.kill_owned_position_rows(symbol)
        for row in owned_position_rows:
            lineage_run_id = str(row.get("trade_run_id") or "")
            if lineage_run_id and lineage_run_id != self.run_id:
                # Valid historical fills from another run are not evidence of
                # ownership for this run. They are ignored, not reclassified
                # as corrupt current-run lineage.
                continue
            if (
                not lineage_run_id
                or str(row.get("trade_coin") or "") != symbol
            ):
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "POSITION_LINEAGE_INCOMPLETE"
                )
            trade_id = row.get("trade_id")
            direction = str(row.get("trade_direction") or "").upper()
            role = str(row.get("role") or "").upper()
            if (
                trade_id is None
                or direction not in {"LONG", "SHORT"}
                or not str(row.get("decision_uid") or "")
                or str(row.get("decision_uid") or "")
                != str(row.get("trade_entry_decision_uid") or "")
            ):
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "POSITION_LINEAGE_INCOMPLETE"
                )
            if role != "ENTRY" and role not in {
                "SL",
                "TP",
                "TRAIL",
                "CLOSE",
                "KILL_FLATTEN",
            }:
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "OWNED_FILL_ROLE_AMBIGUOUS"
                )
            try:
                order_payload = json.loads(str(row.get("order_json") or "{}"))
            except (TypeError, ValueError, json.JSONDecodeError) as exc:
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "POSITION_LINEAGE_INCOMPLETE"
                ) from exc
            if (
                not isinstance(order_payload, Mapping)
                or str(order_payload.get("role") or "").upper() != role
            ):
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "OWNED_FILL_ROLE_CONFLICT"
                )
            try:
                reported_lots = quantize_lots(row["filled_qty"], lot)
                ledger_lots = quantize_lots(row["durable_fill_qty"], lot)
                ordered_lots = quantize_lots(row["qty"], lot)
            except (KeyError, LotQuantizationError, TypeError, ValueError) as exc:
                reason = getattr(exc, "reason_code", "FILLED_QUANTITY_INVALID")
                raise _KillEvidenceFault(KillTerminalState.AMBIGUOUS, reason) from exc
            if reported_lots <= 0 or ledger_lots < 0 or ordered_lots <= 0:
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS,
                    "OWNED_FILL_LINEAGE_CONFLICT",
                )
            fill_uids = {
                value for value in str(
                    row.get("durable_fill_decision_uids") or ""
                ).split(",") if value
            }
            direct_kill_fill = bool(row.get("kill_direct_fill_proven"))
            if direct_kill_fill:
                if (
                    role != "KILL_FLATTEN"
                    or int(row.get("kill_action_qty_lots") or 0) != ordered_lots
                    or int(row.get("durable_fill_count") or 0) <= 0
                    or ledger_lots != reported_lots
                    or fill_uids != {str(row["decision_uid"])}
                    or int(row.get("durable_fill_identity_conflicts") or 0) != 0
                ):
                    raise _KillEvidenceFault(
                        KillTerminalState.AMBIGUOUS,
                        "OWNED_FILL_LINEAGE_CONFLICT",
                    )
                durable_lots = reported_lots
            else:
                durable_lots = ledger_lots
                if (
                    int(row.get("durable_fill_count") or 0) <= 0
                    or durable_lots != reported_lots
                    or fill_uids != {str(row["decision_uid"])}
                    or int(row.get("durable_fill_identity_conflicts") or 0) != 0
                ):
                    raise _KillEvidenceFault(
                        KillTerminalState.AMBIGUOUS,
                        "OWNED_FILL_LINEAGE_CONFLICT",
                    )
            if role != "ENTRY":
                raw_side = str(order_payload.get("side") or "").upper()
                if not raw_side and str(order_payload.get("direction") or "").upper() in {
                    "LONG",
                    "SHORT",
                }:
                    payload_direction = str(order_payload["direction"]).upper()
                    raw_side = "SELL" if payload_direction == "LONG" else "BUY"
                side = (
                    "BUY"
                    if raw_side in {"B", "BUY"}
                    else "SELL"
                    if raw_side in {"A", "SELL"}
                    else ""
                )
                expected_exit_side = "SELL" if direction == "LONG" else "BUY"
                if (
                    side != expected_exit_side
                    or order_payload.get("reduce_only") is not True
                    or (
                        role == "KILL_FLATTEN"
                        and (
                            not direct_kill_fill
                            or str(row.get("kill_action_exit_side") or "")
                            != expected_exit_side
                        )
                    )
                ):
                    raise _KillEvidenceFault(
                        KillTerminalState.AMBIGUOUS,
                        "OWNED_FILL_REDUCTION_CONFLICT",
                    )
            filled_lots = durable_lots
            try:
                durable_oid = int(row["oid"])
            except (KeyError, TypeError, ValueError, OverflowError) as exc:
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS,
                    "OWNED_FILL_LINEAGE_CONFLICT",
                ) from exc
            durable_fill_ids = {
                value
                for value in str(row.get("durable_fill_ids") or "").split(",")
                if value
            }
            if (
                isinstance(row.get("oid"), bool)
                or len(durable_fill_ids)
                != int(row.get("durable_fill_count") or 0)
                or any(
                    (fill_id, durable_oid) in durable_capture_identities
                    for fill_id in durable_fill_ids
                )
            ):
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS,
                    "OWNED_FILL_LINEAGE_CONFLICT",
                )
            durable_capture_identities.update(
                (fill_id, durable_oid) for fill_id in durable_fill_ids
            )
            durable_capture_lots_by_oid[durable_oid] = (
                durable_capture_lots_by_oid.get(durable_oid, 0) + filled_lots
            )
            sign = 1 if direction == "LONG" else -1
            contribution = sign * filled_lots
            if role != "ENTRY":
                contribution *= -1
            expected_signed += contribution
            trade_key = int(trade_id)
            trade_nets[trade_key] = trade_nets.get(trade_key, 0) + contribution
            trade_directions[trade_key] = direction
            trade_decisions.setdefault(
                trade_key, str(row.get("decision_uid") or "")
            )

        ownership_reason: str | None = None
        if any(
            (direction == "LONG" and trade_nets[trade_id] < 0)
            or (direction == "SHORT" and trade_nets[trade_id] > 0)
            for trade_id, direction in trade_directions.items()
        ):
            ownership_reason = "OWNERSHIP_AMBIGUOUS"
        contributing_trades = {
            trade_id for trade_id, net_lots in trade_nets.items() if net_lots != 0
        }
        if expected_signed != observed_signed:
            ownership_reason = "OWNERSHIP_AMBIGUOUS"
        if expected_signed != 0 and len(contributing_trades) != 1:
            ownership_reason = "OWNERSHIP_AMBIGUOUS"
        if (
            capture.epoch != self._kill_epoch()
            or capture.symbol != symbol
            or not capture.accepted
        ):
            raise _KillEvidenceFault(
                KillTerminalState.UNKNOWN, capture.reason_code
            )
        try:
            position_rows = [
                dict(row)
                for row in capture.positions.canonical_rows()
                if str(row.get("symbol") or "") == symbol
            ]
            if len(position_rows) > 1:
                raise ValueError
            captured_size = (
                0.0
                if not position_rows
                else float(position_rows[0]["size"])
            )
            captured_lots = quantize_lots(abs(captured_size), lot)
            captured_signed = (
                captured_lots if captured_size >= 0 else -captured_lots
            )
            if captured_signed != observed_signed:
                raise ValueError

            capture_orders: dict[str, Mapping[str, Any]] = {}
            for raw in capture.open_orders.canonical_rows():
                if str(raw.get("coin") or "") != symbol:
                    continue
                alias = str(raw.get("cloid") or "").casefold()
                if not alias or alias in capture_orders:
                    raise ValueError
                capture_orders[alias] = raw
            if set(capture_orders) != set(exchange_by_alias):
                raise ValueError
            for alias, raw in capture_orders.items():
                observed = exchange_by_alias[alias]
                raw_side = str(raw.get("side") or "").upper()
                side = {"A": "SELL", "B": "BUY"}.get(
                    raw_side, raw_side
                )
                raw_size = raw.get("size", raw.get("sz"))
                if (
                    side != str(observed.side).upper()
                    or quantize_lots(raw_size, lot)
                    != quantize_lots(observed.size, lot)
                    or bool(raw.get("reduce_only", False))
                    != bool(observed.reduce_only)
                ):
                    raise ValueError

            captured_identities: set[tuple[str, int]] = set()
            captured_lots_by_oid: dict[int, int] = {}
            for raw in capture.fills.canonical_rows():
                if str(raw.get("coin") or "") != symbol:
                    continue
                event_id = str(raw.get("event_id") or "").strip()
                oid = int(raw["oid"])
                identity = (event_id, oid)
                fill_lots = quantize_lots(raw["size"], lot)
                if (
                    not event_id
                    or isinstance(raw.get("oid"), bool)
                    or fill_lots <= 0
                    or identity in captured_identities
                ):
                    raise ValueError
                captured_identities.add(identity)
                captured_lots_by_oid[oid] = (
                    captured_lots_by_oid.get(oid, 0) + fill_lots
                )
            if (
                captured_identities != durable_capture_identities
                or captured_lots_by_oid != durable_capture_lots_by_oid
            ):
                ownership_reason = "OWNERSHIP_AMBIGUOUS"
        except (
            KeyError,
            LotQuantizationError,
            TypeError,
            ValueError,
            OverflowError,
        ):
            ownership_reason = "OWNERSHIP_AMBIGUOUS"
        return {
            "snapshot": snapshot,
            "lot": lot,
            "observed_lots": observed_signed,
            "expected_lots": expected_signed,
            "risk_orders": risk_orders,
            "protection_orders": protection_orders,
            "owned_cloids": owned_cloids,
            "trade_id": (
                next(iter(contributing_trades))
                if len(contributing_trades) == 1
                else None
            ),
            "decision_uid": (
                trade_decisions[next(iter(contributing_trades))]
                if len(contributing_trades) == 1
                and trade_decisions.get(next(iter(contributing_trades)), "")
                else None
            ),
            "ownership_reason": ownership_reason,
        }

    def _kill_remaining(self, action: Mapping[str, Any]) -> float:
        action_id = str(action.get("action_id") or "")
        try:
            reserved = datetime.fromisoformat(str(action["reserved_ts"]))
            deadline = datetime.fromisoformat(str(action["deadline_ts"]))
            if reserved.tzinfo is None:
                reserved = reserved.replace(tzinfo=UTC)
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=UTC)
            reserved = reserved.astimezone(UTC)
            deadline = deadline.astimezone(UTC)
        except (KeyError, TypeError, ValueError):
            return 0.0
        now = self._kill_now()
        if (
            not action_id
            or deadline <= reserved
            or (deadline - reserved).total_seconds() > KILL_VERIFY_DEADLINE_S + 0.001
            or now < reserved
        ):
            return 0.0
        try:
            if not self.store.observe_kill_action_clock(
                epoch=self._kill_epoch(),
                action_id=action_id,
                observed_ts=now,
            ):
                return 0.0
        except Exception:
            return 0.0
        wall_remaining = (deadline - now).total_seconds()
        mono_deadline = self._kill_mono_deadlines.get(action_id)
        if mono_deadline is None:
            # A process that did not reserve the action has no write-capable
            # monotonic continuity. It may query, but it may never reconstruct
            # a resend budget from wall time.
            return 0.0
        return max(
            0.0,
            min(wall_remaining, mono_deadline - self._monotonic()),
        )

    def _track_new_kill_action(self, action: Mapping[str, Any]) -> None:
        action_id = str(action.get("action_id") or "")
        try:
            reserved = datetime.fromisoformat(str(action["reserved_ts"]))
            deadline = datetime.fromisoformat(str(action["deadline_ts"]))
            if reserved.tzinfo is None:
                reserved = reserved.replace(tzinfo=UTC)
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=UTC)
            budget = (deadline.astimezone(UTC) - reserved.astimezone(UTC)).total_seconds()
        except (KeyError, TypeError, ValueError):
            return
        if action_id and 0 < budget <= KILL_VERIFY_DEADLINE_S + 0.001:
            self._kill_mono_deadlines[action_id] = self._monotonic() + budget

    @staticmethod
    def _kill_query_identity_matches(
        query: Any, *, cloid: str, symbol: str
    ) -> bool:
        return (
            bool(getattr(query, "known", False))
            and str(getattr(query, "cloid", "") or "") == str(cloid)
            and str(getattr(query, "symbol", "") or "") == str(symbol)
        )

    async def _kill_await(self, action: Mapping[str, Any], awaitable: Any) -> Any:
        remaining = self._kill_remaining(action)
        if remaining <= 0:
            if hasattr(awaitable, "close"):
                awaitable.close()
            raise asyncio.TimeoutError
        return await asyncio.wait_for(awaitable, timeout=remaining)

    @staticmethod
    async def _kill_query_await(awaitable: Any) -> Any:
        return await asyncio.wait_for(awaitable, timeout=KILL_VERIFY_DEADLINE_S)

    def _kill_record(
        self,
        action_id: str,
        status: str,
        reason_code: str,
        value: Any = None,
        *,
        local_order_terminal_status: str | None = None,
        flatten_order: Mapping[str, Any] | None = None,
        flatten_fills: Sequence[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return self.store.record_kill_action_event(
            epoch=self._kill_epoch(),
            action_id=action_id,
            status=status,
            reason_code=self._kill_reason(reason_code),
            evidence_source=str(
                getattr(getattr(value, "evidence", None), "source", "LOCAL")
            ),
            evidence=self._kill_evidence_payload(value),
            observed_ts=self._kill_now(),
            local_order_terminal_status=local_order_terminal_status,
            flatten_order=flatten_order,
            flatten_fills=flatten_fills,
        )

    async def _kill_query_cancel(
        self, action: Mapping[str, Any], *, symbol: str, target: str
    ) -> bool:
        try:
            query = await self._kill_query_await(
                self.broker.query_order(target, symbol)
            )
        except asyncio.TimeoutError:
            self._kill_record(
                str(action["action_id"]), "UNKNOWN", "CANCEL_VERIFY_DEADLINE"
            )
            return False
        except Exception as exc:
            self._kill_record(
                str(action["action_id"]),
                "UNKNOWN",
                f"CANCEL_QUERY_FAILED_{type(exc).__name__}",
            )
            return False
        if not self._kill_query_identity_matches(query, cloid=target, symbol=symbol):
            self._kill_record(
                str(action["action_id"]),
                "UNKNOWN",
                getattr(query.evidence, "reason_code", "CANCEL_QUERY_UNKNOWN"),
                query,
            )
            return False
        if query.terminal or not query.found:
            self._kill_record(
                str(action["action_id"]),
                "APPLIED",
                "CANCEL_TERMINAL_QUERY",
                query,
                local_order_terminal_status="CANCELLED_BY_ENGINE",
            )
            return True
        self._kill_record(
            str(action["action_id"]),
            "NOT_APPLIED",
            "CANCEL_ORDER_STILL_LIVE",
            query,
        )
        return False

    async def _kill_cancel(
        self,
        *,
        episode_id: str,
        symbol: str,
        row: Mapping[str, Any],
        observed: OrderView | None,
    ) -> bool:
        target = str(row["cloid"])
        action_id = compute_kill_action_id(
            episode_id=episode_id,
            kind=KillActionKind.CANCEL.value,
            target=target,
            qty_lots=None,
        )
        reserved_ts = self._kill_now()
        replay, action = self.store.reserve_kill_action(
            epoch=self._kill_epoch(),
            episode_id=episode_id,
            kind=KillActionKind.CANCEL.value,
            target=target,
            qty_lots=None,
            cloid=target,
            deadline_ts=reserved_ts + timedelta(seconds=KILL_VERIFY_DEADLINE_S),
            action_id=action_id,
            reserved_ts=reserved_ts,
        )
        if not replay and observed is None:
            self._kill_record(
                action_id,
                "APPLIED",
                "CANCEL_SNAPSHOT_ABSENT",
                local_order_terminal_status="CANCELLED_BY_ENGINE",
            )
            return True
        if not replay:
            self._track_new_kill_action(action)
        if replay and str(action["current_outcome"]) != ActionOutcome.NOT_APPLIED.value:
            return await self._kill_query_cancel(
                action, symbol=symbol, target=target
            )
        if replay and self._kill_remaining(action) <= 0:
            return await self._kill_query_cancel(
                action, symbol=symbol, target=target
            )
        if replay:
            # A prior direct query proved NOT_APPLIED. It authorizes this one
            # same-identity resend; this call never queries and resends in one
            # replay step.
            pass
        self._kill_record(action_id, "SENT", "CANCEL_SEND_STARTED")
        self._assert_kill_epoch_active()
        try:
            result = await self._kill_await(
                action,
                self.broker.kill_cancel_order_by_cloid(
                    target,
                    symbol,
                    epoch=self._kill_epoch(),
                    epoch_guard=self._kill_epoch_guard(),
                    worker_epoch_guard=(
                        self.store.assert_kill_epoch_owned_in_memory
                    ),
                ),
            )
        except asyncio.TimeoutError:
            self._kill_record(action_id, "UNKNOWN", "CANCEL_TRANSPORT_TIMEOUT")
            return False
        except KillConflictError as exc:
            if exc.reason_code == "KILL_EPOCH_STALE_WRITE":
                self.store.record_kill_epoch_stale_write_rejection(
                    self._kill_epoch(), "CANCEL_MUTATION_BOUNDARY"
                )
            raise
        except Exception as exc:
            self._kill_record(
                action_id,
                "UNKNOWN",
                f"CANCEL_TRANSPORT_FAILED_{type(exc).__name__}",
            )
            return False
        # A write response is transport evidence only. Even a typed
        # NOT_APPLIED response cannot authorize resend until direct query
        # independently proves that outcome.
        status = (
            "UNKNOWN"
            if result.outcome is ActionOutcome.UNKNOWN
            else "EVIDENCE"
        )
        self._kill_record(
            action_id,
            status,
            getattr(result.evidence, "reason_code", "CANCEL_RESULT"),
            result,
        )
        if result.outcome is ActionOutcome.UNKNOWN:
            return await self._kill_query_cancel(
                self.store.get_kill_action(action_id) or action,
                symbol=symbol,
                target=target,
            )
        return await self._kill_query_cancel(
            self.store.get_kill_action(action_id) or action,
            symbol=symbol,
            target=target,
        )

    async def _kill_query_flatten(
        self,
        action: Mapping[str, Any],
        *,
        symbol: str,
        qty_lots: int,
        lot: LotUnit,
        trade_id: int,
    ) -> str:
        action_id = str(action["action_id"])
        cloid = str(action["cloid"])
        try:
            query = await self._kill_query_await(
                self.broker.query_order(cloid, symbol)
            )
        except asyncio.TimeoutError:
            self._kill_record(action_id, "UNKNOWN", "FLATTEN_VERIFY_DEADLINE")
            return "UNKNOWN"
        except Exception as exc:
            self._kill_record(
                action_id,
                "UNKNOWN",
                f"FLATTEN_QUERY_FAILED_{type(exc).__name__}",
            )
            return "UNKNOWN"
        if not self._kill_query_identity_matches(query, cloid=cloid, symbol=symbol):
            self._kill_record(
                action_id,
                "UNKNOWN",
                getattr(query.evidence, "reason_code", "FLATTEN_QUERY_UNKNOWN"),
                query,
            )
            return "UNKNOWN"
        if query.filled_size is None:
            self._kill_record(
                action_id, "UNKNOWN", "FLATTEN_FILLED_QUANTITY_MISSING", query
            )
            return "UNKNOWN"
        try:
            filled_lots = quantize_lots(query.filled_size, lot)
        except (LotQuantizationError, TypeError, ValueError):
            self._kill_record(
                action_id, "UNKNOWN", "FLATTEN_FILLED_QUANTITY_INVALID", query
            )
            return "UNKNOWN"
        if filled_lots < 0 or filled_lots > qty_lots:
            self._kill_record(
                action_id, "UNKNOWN", "FLATTEN_FILLED_QUANTITY_INVALID", query
            )
            return "UNKNOWN"
        if query.terminal and query.oid is not None and filled_lots > 0:
            flatten_fills = await self._kill_exact_flatten_fills(
                action,
                query=query,
                symbol=symbol,
                filled_lots=filled_lots,
                lot=lot,
            )
            if flatten_fills is None:
                self._kill_record(
                    action_id,
                    "UNKNOWN",
                    "FLATTEN_FILL_EVIDENCE_MISSING",
                    query,
                )
                return "UNKNOWN"
            self._kill_record(
                action_id,
                "APPLIED",
                (
                    "FLATTEN_TERMINAL_QUERY"
                    if filled_lots == qty_lots
                    else "FLATTEN_PARTIAL"
                ),
                query,
                flatten_order={
                    "oid": int(query.oid),
                    "symbol": symbol,
                    "trade_id": trade_id,
                    "qty": lots_to_size(qty_lots, lot),
                    "filled_qty": lots_to_size(filled_lots, lot),
                    "decision_uid": str(
                        (self.store.get_trade(int(trade_id)) or {}).get(
                            "entry_decision_uid", ""
                        )
                    ),
                },
                flatten_fills=flatten_fills,
            )
            self._drain_queued_events_locked(symbol)
            return "APPLIED" if filled_lots == qty_lots else "PARTIAL"
        if query.terminal and filled_lots == 0:
            self._kill_record(
                action_id, "NOT_APPLIED", "FLATTEN_DIRECT_NOT_APPLIED", query
            )
            return "NOT_APPLIED"
        self._kill_record(
            action_id, "UNKNOWN", "FLATTEN_TERMINAL_PROOF_MISSING", query
        )
        return "UNKNOWN"

    async def _kill_exact_flatten_fills(
        self,
        action: Mapping[str, Any],
        *,
        query: OrderQueryResult,
        symbol: str,
        filled_lots: int,
        lot: LotUnit,
    ) -> list[dict[str, Any]] | None:
        """Fetch exact immutable fill identities for a query-proven KILL IOC."""
        fetch = getattr(self.broker, "fills_evidence", None)
        if not callable(fetch) or query.oid is None:
            return None
        try:
            reserved = datetime.fromisoformat(str(action["reserved_ts"]))
            deadline = datetime.fromisoformat(str(action["deadline_ts"]))
            if reserved.tzinfo is None:
                reserved = reserved.replace(tzinfo=UTC)
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=UTC)
            # The full-reconcile contract already permits bounded component
            # clock skew. Widen by the same five-second action bound, then bind
            # by exact oid/symbol/side/lot total so unrelated fills cannot match.
            skew_ms = int(KILL_VERIFY_DEADLINE_S * 1000)
            start_ms = (
                int(reserved.astimezone(UTC).timestamp() * 1000) - skew_ms
            )
            end_ms = (
                int(deadline.astimezone(UTC).timestamp() * 1000) + skew_ms
            )
            evidence = await self._kill_query_await(
                fetch(start_ms=start_ms, end_ms=end_ms)
            )
        except (asyncio.TimeoutError, TypeError, ValueError, OverflowError):
            return None
        except Exception:
            return None
        if not bool(getattr(evidence, "accepted", False)):
            return None
        expected_side = str(action.get("exit_side") or "")
        rows: list[dict[str, Any]] = []
        seen: set[str] = set()
        total_lots = 0
        try:
            canonical_rows = evidence.canonical_rows()
        except Exception:
            return None
        for raw in canonical_rows:
            if raw.get("oid") != query.oid:
                continue
            event_id = str(raw.get("event_id") or "").strip()
            side = str(raw.get("side") or "").upper()
            side = {"A": "SELL", "B": "BUY"}.get(side, side)
            try:
                qty_lots = quantize_lots(raw["size"], lot)
                px = float(raw["px"])
                effective_ts_ms = int(raw["effective_ts_ms"])
            except (
                KeyError,
                LotQuantizationError,
                TypeError,
                ValueError,
                OverflowError,
            ):
                return None
            if (
                not event_id
                or event_id in seen
                or str(raw.get("coin") or "") != symbol
                or side != expected_side
                or qty_lots <= 0
                or not math.isfinite(px)
                or px <= 0
                or effective_ts_ms < start_ms
                or effective_ts_ms > end_ms
            ):
                return None
            seen.add(event_id)
            total_lots += qty_lots
            rows.append(
                {
                    "fill_id": event_id,
                    "fill_ts": datetime.fromtimestamp(
                        effective_ts_ms / 1000, tz=UTC
                    ),
                    "qty": lots_to_size(qty_lots, lot),
                    "px": px,
                    "fee": 0.0,
                    "funding": 0.0,
                }
            )
        if not rows or total_lots != filled_lots:
            return None
        return rows

    async def _kill_flatten(
        self,
        *,
        episode_id: str,
        symbol: str,
        qty_lots: int,
        lot: LotUnit,
        trade_id: int,
        exit_side: str,
    ) -> str:
        existing = self.store.kill_actions_for_episode(
            episode_id, kind=KillActionKind.FLATTEN.value
        )
        if existing:
            if len(existing) != 1:
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "FLATTEN_ACTION_AMBIGUOUS"
                )
            action = existing[0]
            if str(action.get("exit_side") or "") not in {"BUY", "SELL"}:
                raise _KillEvidenceFault(
                    KillTerminalState.AMBIGUOUS, "FLATTEN_EXIT_SIDE_MISSING"
                )
            if str(action["current_outcome"]) == ActionOutcome.NOT_APPLIED.value:
                sent_count = sum(
                    1 for event in self.store.kill_action_events(str(action["action_id"]))
                    if str(event["status"]) == "SENT"
                )
                if sent_count < 2 and self._kill_remaining(action) > 0:
                    return await self._kill_send_flatten(
                        action, symbol=symbol, lot=lot, trade_id=trade_id
                    )
            return await self._kill_query_flatten(
                action,
                symbol=symbol,
                qty_lots=int(action["qty_lots"]),
                lot=lot,
                trade_id=trade_id,
            )
        action_id = compute_kill_action_id(
            episode_id=episode_id,
            kind=KillActionKind.FLATTEN.value,
            target=symbol,
            qty_lots=qty_lots,
        )
        cloid = compute_kill_action_cloid(action_id)
        reserved_ts = self._kill_now()
        replay, action = self.store.reserve_kill_action(
            epoch=self._kill_epoch(),
            episode_id=episode_id,
            kind=KillActionKind.FLATTEN.value,
            target=symbol,
            qty_lots=qty_lots,
            cloid=cloid,
            deadline_ts=reserved_ts + timedelta(seconds=KILL_VERIFY_DEADLINE_S),
            action_id=action_id,
            reserved_ts=reserved_ts,
            exit_side=exit_side,
        )
        if not replay:
            self._track_new_kill_action(action)
        if replay and str(action["current_outcome"]) != ActionOutcome.NOT_APPLIED.value:
            return await self._kill_query_flatten(
                action,
                symbol=symbol,
                qty_lots=qty_lots,
                lot=lot,
                trade_id=trade_id,
            )
        return await self._kill_send_flatten(
            action, symbol=symbol, lot=lot, trade_id=trade_id
        )

    async def _kill_send_flatten(
        self, action: Mapping[str, Any], *, symbol: str, lot: LotUnit, trade_id: int
    ) -> str:
        action_id = str(action["action_id"])
        cloid = str(action["cloid"])
        qty_lots = int(action["qty_lots"])
        exit_side = str(action.get("exit_side") or "")
        if self._kill_remaining(action) <= 0:
            return await self._kill_query_flatten(
                action, symbol=symbol, qty_lots=qty_lots, lot=lot, trade_id=trade_id
            )
        self._kill_record(action_id, "SENT", "FLATTEN_SEND_STARTED")
        self._assert_kill_epoch_active()
        try:
            result = await self._kill_await(
                action,
                self.broker.kill_flatten_reduce_only(
                    symbol=symbol,
                    cloid=cloid,
                    size=lots_to_size(qty_lots, lot),
                    exit_side=exit_side,
                    epoch=self._kill_epoch(),
                    epoch_guard=self._kill_epoch_guard(),
                    worker_epoch_guard=(
                        self.store.assert_kill_epoch_owned_in_memory
                    ),
                ),
            )
        except asyncio.TimeoutError:
            self._kill_record(action_id, "UNKNOWN", "FLATTEN_TRANSPORT_TIMEOUT")
            return "UNKNOWN"
        except KillConflictError as exc:
            if exc.reason_code == "KILL_EPOCH_STALE_WRITE":
                self.store.record_kill_epoch_stale_write_rejection(
                    self._kill_epoch(), "FLATTEN_MUTATION_BOUNDARY"
                )
            raise
        except Exception as exc:
            self._kill_record(
                action_id,
                "UNKNOWN",
                f"FLATTEN_TRANSPORT_FAILED_{type(exc).__name__}",
            )
            return "UNKNOWN"
        status = (
            "UNKNOWN"
            if result.outcome is ActionOutcome.UNKNOWN
            else "EVIDENCE"
        )
        self._kill_record(
            action_id,
            status,
            getattr(result.evidence, "reason_code", "FLATTEN_RESULT"),
            result,
        )
        if result.outcome is ActionOutcome.UNKNOWN:
            return await self._kill_query_flatten(
                self.store.get_kill_action(action_id) or action,
                symbol=symbol,
                qty_lots=qty_lots,
                lot=lot,
                trade_id=trade_id,
            )
        return await self._kill_query_flatten(
            self.store.get_kill_action(action_id) or action,
            symbol=symbol,
            qty_lots=qty_lots,
            lot=lot,
            trade_id=trade_id,
        )

    async def run_kill_episode(
        self,
        request: Mapping[str, Any],
        *,
        epoch: KillEvidenceEpoch,
        capture_evidence: Callable[[], Any],
        full_writer_already_held: bool = False,
    ) -> dict[str, Any]:
        """Resolve one reserved episode under full-writer -> symbol ordering."""
        episode_id = str(request["episode_id"])
        symbol = str(request["symbol"])
        flatten_requested = bool(request["flatten_requested"])
        self._active_kill_epoch = epoch
        if epoch.episode_id != episode_id:
            return {
                "state": KillTerminalState.UNKNOWN.value,
                "reason": "KILL_EPOCH_EPISODE_MISMATCH",
            }
        if not self._kill_broker_available():
            return {
                "state": KillTerminalState.UNRESOLVED.value,
                "reason": "KILL_BROKER_API_UNAVAILABLE",
            }
        if self.symbol_locks.is_held(symbol):
            return {
                "state": KillTerminalState.UNRESOLVED.value,
                "reason": "KILL_LOCK_ORDER_DEFERRED",
            }
        async with _kill_full_writer_scope(
            self.store, already_held=full_writer_already_held
        ):
            async with self.symbol_locks.hold(symbol):
                if self.store.has_submission_quarantine():
                    return {
                        "state": KillTerminalState.UNRESOLVED.value,
                        "reason": "SUBMISSION_QUARANTINE_ACTIVE",
                    }
                if self._partial_recovery_owns(symbol):
                    return {
                        "state": KillTerminalState.UNRESOLVED.value,
                        "reason": "PARTIAL_RECOVERY_ACTIVE",
                    }
                try:
                    capture = self._require_kill_capture(
                        await capture_evidence(), symbol=symbol
                    )
                    self._assert_kill_epoch_active()
                    snapshot = await self._kill_snapshot(symbol)
                    model = self._kill_model(
                        snapshot, symbol=symbol, capture=capture
                    )
                except _KillEvidenceFault as fault:
                    return {
                        "state": fault.state.value,
                        "reason": fault.reason_code,
                    }

                if model["ownership_reason"] is not None:
                    return {
                        "state": KillTerminalState.AMBIGUOUS.value,
                        "reason": model["ownership_reason"],
                    }

                for row, observed in model["risk_orders"]:
                    if not await self._kill_cancel(
                        episode_id=episode_id,
                        symbol=symbol,
                        row=row,
                        observed=observed,
                    ):
                        return {
                            "state": KillTerminalState.UNKNOWN.value,
                            "reason": "CANCEL_TERMINAL_PROOF_MISSING",
                        }

                try:
                    capture = self._require_kill_capture(
                        await capture_evidence(), symbol=symbol
                    )
                    self._assert_kill_epoch_active()
                    snapshot = await self._kill_snapshot(symbol)
                    model = self._kill_model(
                        snapshot, symbol=symbol, capture=capture
                    )
                except _KillEvidenceFault as fault:
                    return {
                        "state": fault.state.value,
                        "reason": fault.reason_code,
                    }
                if model["ownership_reason"] is not None:
                    return {
                        "state": KillTerminalState.AMBIGUOUS.value,
                        "reason": model["ownership_reason"],
                    }

                position_lots = abs(int(model["observed_lots"]))
                if position_lots == 0:
                    for row, observed in model["protection_orders"]:
                        if not await self._kill_cancel(
                            episode_id=episode_id,
                            symbol=symbol,
                            row=row,
                            observed=observed,
                        ):
                            return {
                                "state": KillTerminalState.UNKNOWN.value,
                                "reason": "RESIDUAL_PROTECTION_CANCEL_UNKNOWN",
                            }
                    return {
                        "state": KillTerminalState.SAFE_FLAT.value,
                        "reason": "DIRECT_SAFE_FLAT_PROOF",
                        "proof": {
                            "symbol": symbol,
                            "position_lots": 0,
                            "snapshot": snapshot.evidence.as_payload(),
                        },
                    }

                if not flatten_requested:
                    protection = self.qualifying_protection(
                        snapshot,
                        position_lots=position_lots,
                        exit_side=exit_side_for(float(snapshot.net_size)),
                        owned_cloids=set(model["owned_cloids"]),
                    )
                    if protection is None:
                        return {
                            "state": KillTerminalState.UNRESOLVED.value,
                            "reason": "EXACT_OWNED_PROTECTION_MISSING",
                        }
                    return {
                        "state": KillTerminalState.SAFE_RETAINED.value,
                        "reason": "DIRECT_SAFE_RETAINED_PROOF",
                        "proof": {
                            "symbol": symbol,
                            "position_lots": int(model["observed_lots"]),
                            "protection_cloid": str(protection.cloid),
                            "snapshot": snapshot.evidence.as_payload(),
                        },
                    }

                trade_id = model["trade_id"]
                if trade_id is None:
                    return {
                        "state": KillTerminalState.AMBIGUOUS.value,
                        "reason": "OWNERSHIP_AMBIGUOUS",
                    }
                flattened = await self._kill_flatten(
                    episode_id=episode_id,
                    symbol=symbol,
                    qty_lots=position_lots,
                    lot=model["lot"],
                    trade_id=int(trade_id),
                    exit_side=exit_side_for(float(snapshot.net_size)),
                )
                if flattened == "PARTIAL":
                    return {
                        "state": KillTerminalState.UNKNOWN.value,
                        "reason": "FLATTEN_PARTIAL",
                    }
                if flattened != "APPLIED":
                    return {
                        "state": KillTerminalState.UNKNOWN.value,
                        "reason": "FLATTEN_TERMINAL_PROOF_MISSING",
                    }
                try:
                    capture = self._require_kill_capture(
                        await capture_evidence(), symbol=symbol
                    )
                    self._assert_kill_epoch_active()
                    snapshot = await self._kill_snapshot(symbol)
                    model = self._kill_model(
                        snapshot, symbol=symbol, capture=capture
                    )
                except _KillEvidenceFault as fault:
                    return {
                        "state": fault.state.value,
                        "reason": fault.reason_code,
                    }
                if model["ownership_reason"] is not None or int(
                    model["observed_lots"]
                ) != 0:
                    return {
                        "state": KillTerminalState.UNKNOWN.value,
                        "reason": "FLATTEN_POSITION_NOT_FLAT",
                    }
                for row, observed in model["protection_orders"]:
                    if not await self._kill_cancel(
                        episode_id=episode_id,
                        symbol=symbol,
                        row=row,
                        observed=observed,
                    ):
                        return {
                            "state": KillTerminalState.UNKNOWN.value,
                            "reason": "RESIDUAL_PROTECTION_CANCEL_UNKNOWN",
                        }
                return {
                    "state": KillTerminalState.SAFE_FLAT.value,
                    "reason": "DIRECT_SAFE_FLAT_PROOF",
                    "proof": {
                        "symbol": symbol,
                        "position_lots": 0,
                        "snapshot": snapshot.evidence.as_payload(),
                    },
                }

    # ------------------------------------------------------------------
    # TS-P1-002 identity-based submission
    # ------------------------------------------------------------------

    async def submit_plan(
        self, decision_uid: str, plan: OrderPlan, *, strategy_id: str = "keltner_trail_ema8"
    ) -> dict[str, Any] | None:
        """Serialize the final new-risk boundary with partial recovery.

        The engine performs earlier advisory checks, but only this boundary owns
        reservation/send sequencing.  The final ARM and recovery checks therefore
        run after acquiring the same per-symbol writer lock used by fill
        ingestion and recovery.
        """
        symbol = str(plan.signal.symbol)
        async with self.symbol_locks.hold(symbol):
            state = self.store.get_meta("app_state")
            if (
                self.kill_latched
                or (state is not None and state != "ARMED")
                or self._partial_recovery_owns(symbol)
            ):
                return None
            return await self._submit_plan_locked(
                decision_uid, plan, strategy_id=strategy_id
            )

    def _new_risk_pre_send_allowed(
        self, symbol: str, *, attempt_id: str
    ) -> bool:
        """Synchronous last-wire veto used by adapters at their write boundary."""
        state = self.store.get_meta("app_state")
        attempt = self.store.get_submission_attempt(attempt_id)
        other_quarantine = any(
            str(row.get("attempt_id") or "") != attempt_id
            for row in self.store.get_quarantined_submission_attempts()
        )
        return not (
            self.kill_latched
            or (state is not None and state != "ARMED")
            or attempt is None
            or str(attempt.get("state") or "") != "SUBMITTING"
            or other_quarantine
            or self._partial_recovery_owns(symbol)
        )

    async def _place_bracket_with_guard(
        self,
        plan: OrderPlan,
        *,
        symbol: str,
        attempt_id: str,
    ) -> Any:
        """Use the adapter boundary guard, retaining legacy fake compatibility."""
        place_bracket = self.broker.place_bracket
        def guard() -> bool:
            return self._new_risk_pre_send_allowed(
                symbol, attempt_id=attempt_id
            )

        # Production adapters may call this worker-safe projection inside an
        # executor. SQLite-backed checks stay in the event-loop preflight.
        guard.in_memory_only = lambda: not self.kill_latched  # type: ignore[attr-defined]
        try:
            parameters = inspect.signature(place_bracket).parameters.values()
        except (TypeError, ValueError) as exc:
            raise BrokerPreSendFailure(
                "BROKER_PRE_SEND_GUARD_UNAVAILABLE"
            ) from exc
        accepts_guard = any(
            parameter.name == "pre_send_guard"
            or parameter.kind is inspect.Parameter.VAR_KEYWORD
            for parameter in parameters
        )
        if accepts_guard:
            return await place_bracket(plan, pre_send_guard=guard)
        # Legacy in-process fakes predate the protocol extension. Production
        # adapters implement the guarded branch above; this preserves their
        # older unit-test contract with the last synchronous manager veto.
        if not guard():
            raise BrokerPreSendFailure("KILL_PRE_SEND_VETO")
        return await place_bracket(plan)

    async def _submit_plan_locked(
        self, decision_uid: str, plan: OrderPlan, *, strategy_id: str
    ) -> dict[str, Any] | None:
        """Reserve, submit, verify, and finalize while holding the symbol lock."""
        symbol = str(plan.signal.symbol)
        self.symbol_locks.require(symbol)
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
        # This authorizes durable reservation only. The adapter receives a
        # separate synchronous guard and must re-check it at the write boundary.
        state = self.store.get_meta("app_state")
        if (
            self.kill_latched
            or (state is not None and state != "ARMED")
            or self.store.has_submission_quarantine()
            or self._partial_recovery_owns(symbol)
        ):
            return None
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
                broker_result = await self._place_bracket_with_guard(
                    plan,
                    symbol=symbol,
                    attempt_id=attempt_id,
                )
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
        if self.kill_latched:
            self._quarantine_unknown(attempt_id, "KILL_LATCHED_DURING_TRANSMISSION")
            raise UnknownSubmissionError(
                "KILL_LATCHED_DURING_TRANSMISSION", request_id, attempt_id
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

    def _event_symbol(self, event: BrokerEvent) -> str | None:
        if isinstance(event, FillEvent):
            return str(event.coin)
        if isinstance(event, OrderUpdateEvent):
            order = self.store.get_order(event.cloid)
            if order is None or order.get("trade_id") is None:
                return None
            trade = self.store.get_trade(int(order["trade_id"]))
            return None if trade is None else str(trade["coin"])
        return None

    def _drain_queued_events_locked(self, symbol: str) -> None:
        """Ingest same-symbol callbacks emitted during broker I/O."""
        self.symbol_locks.require(symbol)
        pending: list[BrokerEvent] = []
        for event in self._queued_events:
            if self._event_symbol(event) != symbol or not self._ingest_event(event):
                pending.append(event)
        self._queued_events = pending

    def _canonical_status(
        self,
        *,
        order: Mapping[str, Any],
        raw_status: object,
        filled_qty: float | None,
        symbol: str,
    ) -> str:
        """Quantity/action-derived durable status; malformed evidence fails closed."""
        durable_filled = (
            float(filled_qty)
            if filled_qty is not None
            else float(order.get("filled_qty") or 0.0)
        )
        lot = self._broker_lot_unit(symbol)
        if lot is None:
            raise LotQuantizationError("SIZE_QUANTUM_UNAVAILABLE")
        try:
            return canonical_order_state(
                raw_status=raw_status,
                ordered_qty=float(order["qty"]),
                filled_qty=durable_filled,
                lot=lot,
                cancel_reserved=self.store.partial_cancel_reserved_for_cloid(
                    str(order["cloid"])
                ),
            ).value
        except LotQuantizationError:
            raise
        except Exception:
            # Existing unrelated brokers may expose legacy raw spellings that
            # are outside the TS-P1-001 alias inventory. Preserve their
            # established spelling only after exact quantity normalization has
            # succeeded. Quantization failures never reach this fallback.
            return str(raw_status)

    async def drain_queued_events(self) -> int:
        """Ingest queued broker callbacks under the per-symbol writer locks.

        Purely local: no broker I/O happens here. TS-P1-005 calls it once,
        after acquiring the global full-reconcile writer guard and before any
        evidence is collected, so a full capture always observes one coherent
        local epoch rather than a half-applied event queue.

        Returns the number of events consumed.
        """
        before = len(self._queued_events)
        pending: list[BrokerEvent] = []
        for event in self._queued_events:
            symbol = self._event_symbol(event)
            if symbol is None:
                if not self._ingest_event(event):
                    pending.append(event)
                continue
            async with self.symbol_locks.hold(symbol):
                if not self._ingest_event(event):
                    pending.append(event)
        self._queued_events = pending
        return before - len(pending)

    async def sync_broker_state(self) -> None:
        await self.drain_queued_events()

        broker_orders = await self.broker.open_orders()
        for order in broker_orders:
            async with self.symbol_locks.hold(str(order.coin)):
                stored = self.store.get_order(order.cloid)
                if stored is None:
                    continue
                try:
                    status = self._canonical_status(
                        order=stored,
                        raw_status=order.status,
                        filled_qty=stored.get("filled_qty"),
                        symbol=str(order.coin),
                    )
                except LotQuantizationError as exc:
                    self._quantity_integrity_fault(
                        symbol=str(order.coin),
                        observed_ts=datetime.now(UTC),
                        detail=f"cloid={order.cloid} reason={exc.reason_code}",
                    )
                    continue
                self.store.update_order_status(
                    order.cloid,
                    status,
                )

    async def reconcile(self, *, _full_guard_held: bool = False) -> None:
        if not _full_guard_held:
            # Import lazily to avoid a module cycle. Light and full reconciliation
            # share this database-scoped epoch guard for their entire broker/local
            # observation window; neither can construct a mixed-state snapshot.
            from bridge.engine.reconcile import full_writer_guard

            async with full_writer_guard(self.store):
                await self.reconcile(_full_guard_held=True)
            return
        await self.recover_unknown_submissions()
        if self.store.has_submission_quarantine():
            # TS-P1-003 quarantine dominates: TS-P1-004 defers completely.
            return
        # Broker callbacks are queued synchronously. Consume them under the
        # symbol writer lock before either recovery or ordinary reconcile can
        # classify the same exposure from an older local view.
        await self.sync_broker_state()
        if self.store.has_submission_quarantine():
            return
        await self.run_partial_recoveries()
        positions = await self.broker.positions()
        for observed in positions:
            symbol = str(observed.symbol)
            async with self.symbol_locks.hold(symbol):
                # Re-read every decision input after acquiring the symbol
                # writer lock. The pre-lock list is only an iteration seed.
                if self.store.has_submission_quarantine():
                    continue
                if self._partial_recovery_owns(symbol):
                    continue
                current_positions = await self.broker.positions()
                position = next(
                    (
                        item
                        for item in current_positions
                        if item.symbol == symbol and item.size != 0
                    ),
                    None,
                )
                if position is None:
                    continue
                if await self._claim_post_safe_flat_exposure(position):
                    continue
                open_orders = await self.broker.open_orders()
                if self._position_is_protected(position, open_orders):
                    continue
                trade = self.store.get_open_trade_for_coin(self.run_id, symbol)
                if trade is None:
                    self.store.insert_event(
                        self.run_id,
                        datetime.now(UTC),
                        "WARN",
                        "FOREIGN_POSITION_IGNORED",
                        symbol,
                    )
                    continue
                if self._within_pending_grace(int(trade["trade_id"])):
                    continue
                try:
                    recovered = await self.broker.reprotect_position(
                        position,
                        float(trade["sl_initial"]),
                        (
                            float(trade["tp_initial"])
                            if trade["tp_initial"] is not None
                            else None
                        ),
                        str(trade["entry_decision_uid"]),
                    )
                except Exception as exc:
                    self.store.insert_event(
                        self.run_id,
                        datetime.now(UTC),
                        "ERROR",
                        "REPROTECT_FAILED",
                        f"{symbol}: {type(exc).__name__}",
                    )
                    recovered = None
                if recovered:
                    self._persist_reprotected(recovered, trade)
                    self.store.insert_event(
                        self.run_id,
                        datetime.now(UTC),
                        "WARN",
                        "NAKED_POSITION_REPROTECTED",
                        symbol,
                    )
                else:
                    await self.broker.flatten(symbol)
                    self.store.insert_event(
                        self.run_id,
                        datetime.now(UTC),
                        "WARN",
                        "NAKED_POSITION_FLATTENED",
                        symbol,
                    )
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
            order = self.store.get_order(event.cloid)
            if order is None:
                return False
            symbol = self._event_symbol(event) or ""
            try:
                status = self._canonical_status(
                    order=order,
                    raw_status=event.status,
                    filled_qty=event.filled_qty,
                    symbol=symbol,
                )
            except LotQuantizationError as exc:
                self._quantity_integrity_fault(
                    symbol=symbol,
                    observed_ts=event.ts,
                    detail=f"cloid={event.cloid} reason={exc.reason_code}",
                )
                return True
            self.store.update_order_status(
                event.cloid,
                status,
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
        kill_close_alias = (
            role == "KILL_FLATTEN"
            and str(fill.role).upper() in {"CLOSE", "KILL_FLATTEN"}
        )
        if fill.role != "UNKNOWN" and fill.role != role and not kill_close_alias:
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
        lot = self._broker_lot_unit(str(fill.coin))
        if lot is None:
            self._quantity_integrity_fault(
                symbol=str(fill.coin),
                observed_ts=fill.ts,
                detail=f"fill_id={fill.fill_id} cloid={fill.cloid} "
                "reason=SIZE_QUANTUM_UNAVAILABLE",
            )
            self._synced_fills.add(fill.fill_id)
            return True
        try:
            event_lots = quantize_lots(fill.qty, lot)
            ordered_lots = quantize_lots(float(order["qty"]), lot)
            filled_lots = quantize_lots(order_filled_qty, lot)
            if event_lots <= 0:
                raise LotQuantizationError("NON_POSITIVE_FILL_QUANTITY")
            if ordered_lots <= 0:
                raise LotQuantizationError("NON_POSITIVE_ORDER_QUANTITY")
        except LotQuantizationError as exc:
            self._quantity_integrity_fault(
                symbol=str(fill.coin),
                observed_ts=fill.ts,
                detail=f"fill_id={fill.fill_id} cloid={fill.cloid} "
                f"reason={exc.reason_code}",
            )
            self._synced_fills.add(fill.fill_id)
            return True
        if filled_lots > ordered_lots:
            self._quarantine_fill(
                "ORDER_OVERFILL",
                fill,
                f"cloid={fill.cloid} filled_lots={filled_lots} "
                f"ordered_lots={ordered_lots}",
            )
            self._synced_fills.add(fill.fill_id)
            return True
        status = self._canonical_status(
            order=order,
            raw_status=str(order["status"]),
            filled_qty=order_filled_qty,
            symbol=str(fill.coin),
        )
        self.store.update_order_status(
            fill.cloid,
            status,
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
                try:
                    entry_lots = quantize_lots(entry_qty, lot)
                    exit_lots = quantize_lots(exit_qty, lot)
                except LotQuantizationError as exc:
                    self._quantity_integrity_fault(
                        symbol=str(fill.coin),
                        observed_ts=fill.ts,
                        detail=f"fill_id={fill.fill_id} trade_id={trade_id} "
                        f"reason={exc.reason_code}",
                    )
                    self._synced_fills.add(fill.fill_id)
                    return True
                if exit_lots > entry_lots:
                    self._quarantine_fill(
                        "TRADE_OVERFILL",
                        fill,
                        f"trade_id={trade_id} exit_lots={exit_lots} "
                        f"entry_lots={entry_lots}",
                    )
                    self._synced_fills.add(fill.fill_id)
                    return True
                if exit_lots == entry_lots:
                    try:
                        live_entry_remainder = self._has_live_entry_remainder_exact(
                            int(trade_id), lot
                        )
                    except LotQuantizationError as exc:
                        self._quantity_integrity_fault(
                            symbol=str(fill.coin),
                            observed_ts=fill.ts,
                            detail=f"fill_id={fill.fill_id} trade_id={trade_id} "
                            f"reason={exc.reason_code}",
                        )
                        self._synced_fills.add(fill.fill_id)
                        return True
                    if live_entry_remainder:
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

    def _has_live_entry_remainder_exact(
        self, trade_id: int, lot: LotUnit
    ) -> bool:
        for order in self.store.get_orders_for_trade(trade_id):
            if order["role"] != "ENTRY" or order["status"] not in {
                "OPEN",
                "SUBMITTED",
                "PENDING",
                "PARTIALLY_FILLED",
                "PENDING_CANCEL",
            }:
                continue
            filled_qty, _ = self.store.order_fill_totals(str(order["cloid"]))
            filled_lots = quantize_lots(filled_qty, lot)
            ordered_lots = quantize_lots(float(order["qty"]), lot)
            if filled_lots < ordered_lots:
                return True
        return False

    def _quantity_integrity_fault(
        self, *, symbol: str, observed_ts: datetime, detail: str
    ) -> None:
        """Persist malformed lot evidence and stop new risk without mutation."""
        self.store.set_meta("app_state", "DISARMED")
        self.store.insert_event(
            self.run_id,
            observed_ts,
            "ERROR",
            "FILL_QUANTITY_INTEGRITY",
            f"{symbol} {detail}".strip(),
        )

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
            if order["role"] != "SL" or order["status"] not in {
                "SUBMITTED", "OPEN", "PARTIALLY_FILLED", "PENDING_CANCEL",
            }:
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
        if self.store.partial_recovery_abort_active(symbol):
            return True
        latest = self.store.latest_partial_recovery_for_symbol(symbol)
        return bool(
            latest is not None
            and str(latest["state"])
            == PartialProtectionState.PROTECTED_PARTIAL.value
            and str(latest["reason_code"]) != "REARM_ARCHIVED"
        )

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
        if self.store.has_submission_quarantine():
            # TS-P1-003 owns the safety decision. Do not create a competing
            # recovery row or latch; the conservative legacy scan will inspect
            # the durable fill only after that quarantine resolves.
            return
        trade_id = order.get("trade_id")
        if trade_id is None:
            return
        try:
            ordered = float(order["qty"])
        except (TypeError, ValueError):
            return
        trade = self.store.get_trade(int(trade_id))
        if trade is None or trade["exit_ts"] is not None:
            return
        symbol = str(trade["coin"])
        lot = self._broker_lot_unit(symbol)
        if lot is None:
            self._quantity_integrity_fault(
                symbol=symbol,
                observed_ts=self.store.now(),
                detail=f"cloid={order['cloid']} reason=SIZE_QUANTUM_UNAVAILABLE",
            )
            return
        try:
            ordered_lots = quantize_lots(ordered, lot)
            filled_lots = quantize_lots(float(filled_qty), lot)
        except LotQuantizationError as exc:
            self._quantity_integrity_fault(
                symbol=symbol,
                observed_ts=self.store.now(),
                detail=f"cloid={order['cloid']} reason={exc.reason_code}",
            )
            return
        existing = self.store.active_partial_recovery_for_symbol(symbol)
        if existing is not None:
            # A live generation already owns this symbol; quantities are
            # recomputed by the runner. The deadline is never rewritten.
            return
        latest = self.store.latest_partial_recovery_for_symbol(symbol)
        same_lineage = bool(
            latest is not None
            and int(latest["trade_id"]) == int(trade_id)
            and str(latest["entry_cloid"]) == str(order["cloid"])
        )
        if same_lineage and str(latest["state"]) == (
            PartialProtectionState.UNPROTECTED_ABORT.value
        ):
            # Sticky fail-closed: new evidence may be inspected by a human,
            # but an aborted generation never restarts automatic mutation.
            return
        if same_lineage and str(latest["state"]) == (
            PartialProtectionState.PROTECTED_PARTIAL.value
        ):
            if int(latest["filled_lots"] or -1) == filled_lots:
                return
            # A late fill invalidates the accepted quantity proof while
            # retaining the original, non-resetting 10-second deadline.
            self.store.open_partial_generation(
                recovery_id=str(latest["recovery_id"]),
                reason_code="LATE_FILL_REQUANTIFY",
                filled_lots=filled_lots,
            )
            self._disarm_for_partial(
                "PARTIAL_LATE_FILL_REOPENED", symbol, str(order["cloid"])
            )
            return
        reopening_safe_flat = bool(
            same_lineage
            and str(latest["state"]) == PartialProtectionState.SAFE_FLAT.value
            and int(latest["filled_lots"] or -1) != filled_lots
        )
        if not (0 < filled_lots < ordered_lots) and not reopening_safe_flat:
            # A normal exact fill has no recovery work. Exact/full fills only
            # reopen an already accepted lineage when the quantity changed.
            return
        if (
            reopening_safe_flat
        ):
            # SAFE_FLAT is terminal only for that generation. A late exposure
            # gets a new identity, never a fresh safety budget.
            first_observed = self._parse_utc(latest["first_observed_ts"])
            deadline = self._parse_utc(latest["protect_deadline_ts"])
            if first_observed is None:
                first_observed = datetime(1970, 1, 1, tzinfo=UTC)
            if deadline is None:
                deadline = first_observed
        else:
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
                generation=(
                    int(latest["generation"]) + 1
                    if same_lineage
                    and str(latest["state"])
                    == PartialProtectionState.SAFE_FLAT.value
                    else 0
                ),
                size_decimals=(None if lot is None else lot.size_decimals),
                ordered_lots=ordered_lots,
                filled_lots=filled_lots,
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

    async def _claim_post_safe_flat_exposure(self, position: Position) -> bool:
        """Claim same-trade exposure that invalidates a prior SAFE_FLAT proof.

        The caller holds the per-symbol writer lock. Exact owned evidence opens
        a new recovery generation. Inexact, mixed, foreign, or contradictory
        evidence opens that generation directly into the sticky abort state.
        No broker mutation is performed here.
        """
        symbol = str(position.symbol)
        self.symbol_locks.require(symbol)
        latest = self.store.latest_partial_recovery_for_symbol(symbol)
        if (
            latest is None
            or str(latest["state"]) != PartialProtectionState.SAFE_FLAT.value
        ):
            return False
        trade = self.store.get_open_trade_for_coin(self.run_id, symbol)
        if trade is None or int(trade["trade_id"]) != int(latest["trade_id"]):
            # A later trade has its own lineage; the old SAFE_FLAT row cannot
            # claim it merely because both use the same symbol.
            return False
        if self.store.has_submission_quarantine():
            return True

        broker = self._partial_broker()
        snapshot: SymbolSnapshot | None = None
        provenance = Provenance.UNVERIFIED
        position_lots: int | None = None
        current_filled_lots: int | None = None
        reason = "RECOVERY_API_UNAVAILABLE"
        if broker is not None:
            snapshot = await self._snapshot(broker, latest)
            if self.store.has_submission_quarantine():
                return True
            if snapshot.exact and snapshot.lot is not None:
                try:
                    filled_qty, _ = self.store.order_fill_totals(
                        str(latest["entry_cloid"])
                    )
                    current_filled_lots = quantize_lots(filled_qty, snapshot.lot)
                    baseline_filled_lots = int(latest["filled_lots"])
                except (LotQuantizationError, TypeError, ValueError):
                    reason = "POST_SAFE_FLAT_FILL_EVIDENCE_INVALID"
                else:
                    if current_filled_lots > baseline_filled_lots:
                        provenance, position_lots, reason = self._classify(
                            latest, snapshot
                        )
                    elif current_filled_lots == baseline_filled_lots:
                        try:
                            position_lots = quantize_lots(
                                abs(float(snapshot.net_size or 0.0)), snapshot.lot
                            )
                        except LotQuantizationError:
                            position_lots = None
                        provenance = Provenance.AMBIGUOUS
                        reason = "POST_SAFE_FLAT_NO_FRESH_OWNED_EVIDENCE"
                    else:
                        provenance = Provenance.AMBIGUOUS
                        reason = "POST_SAFE_FLAT_FILL_EVIDENCE_REGRESSED"
            else:
                reason = "SNAPSHOT_INEXACT"

        first_observed = self._parse_utc(latest["first_observed_ts"])
        deadline = self._parse_utc(latest["protect_deadline_ts"])
        if first_observed is None:
            first_observed = datetime(1970, 1, 1, tzinfo=UTC)
        if deadline is None:
            deadline = first_observed
        generation = int(latest["generation"]) + 1
        try:
            opened = self.store.open_partial_recovery(
                run_id=self.run_id,
                symbol=symbol,
                trade_id=int(latest["trade_id"]),
                entry_cloid=str(latest["entry_cloid"]),
                entry_decision_uid=str(latest["entry_decision_uid"]),
                entry_request_id=str(latest["entry_request_id"]),
                first_observed_ts=first_observed,
                protect_deadline_ts=deadline,
                generation=generation,
                size_decimals=(
                    latest["size_decimals"]
                    if snapshot is None or snapshot.lot is None
                    else snapshot.lot.size_decimals
                ),
                ordered_lots=latest["ordered_lots"],
                filled_lots=(
                    latest["filled_lots"]
                    if current_filled_lots is None
                    else current_filled_lots
                ),
                reason_code="POST_SAFE_FLAT_EXPOSURE",
            )
        except PartialRecoveryConflictError as exc:
            self._disarm_for_partial(
                "PARTIAL_RECOVERY_OPEN_FAILED", symbol, exc.code
            )
            return True

        if provenance is Provenance.OWNED and position_lots not in (None, 0):
            self.store.transition_partial_recovery(
                str(opened["recovery_id"]),
                expected=PartialProtectionState.PARTIAL_DETECTED.value,
                target=PartialProtectionState.PARTIAL_DETECTED.value,
                reason_code="POST_SAFE_FLAT_OWNED",
                provenance=provenance.value,
                position_lots=position_lots,
            )
            self._arm_monotonic_deadline(opened, "protect", PROTECT_DEADLINE_S)
            self._disarm_for_partial(
                "PARTIAL_POST_SAFE_FLAT_REOPENED", symbol, str(generation)
            )
            return True

        self.store.transition_partial_recovery(
            str(opened["recovery_id"]),
            expected=PartialProtectionState.PARTIAL_DETECTED.value,
            target=PartialProtectionState.UNPROTECTED_ABORT.value,
            reason_code=reason,
            provenance=provenance.value,
            position_lots=position_lots,
        )
        self._disarm_for_partial("UNPROTECTED_ABORT", symbol, reason)
        return True

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
            for row in self.store.partial_actions_for_lineage(
                int(recovery["trade_id"]), str(recovery["entry_cloid"])
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
                return Provenance.MIXED, None, "OTHER_TRADE_ORDER_PRESENT"
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
            owned_net_lots = quantize_lots(
                float(totals["entry_qty"]), lot
            ) - quantize_lots(float(totals["exit_qty"]), lot)
            owned_net_lots -= self.store.applied_partial_flatten_lots(
                int(recovery["trade_id"]), str(recovery["entry_cloid"])
            )
        except LotQuantizationError as exc:
            return Provenance.UNVERIFIED, None, exc.reason_code
        if owned_net_lots < 0:
            return Provenance.AMBIGUOUS, None, "LOCAL_EXIT_EXCEEDS_ENTRY"
        if position_lots > owned_net_lots:
            # Authoritative exposure exceeds the net quantity proved by this
            # trade's durable fills: some contribution is manual/foreign.
            return Provenance.MIXED, position_lots, "MIXED_PROVENANCE"
        if position_lots < owned_net_lots:
            # A missing exit, stale position, or other contradictory evidence
            # cannot authorize mutation either.
            return Provenance.AMBIGUOUS, position_lots, "OWNED_QUANTITY_CONFLICT"
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

        Safety requires exactly one live owned SL for the symbol, and that one
        stop must be opposite-side, reduce-only, and exactly sized in lot
        units.  A second live owned SL is stale/duplicate protection, even when
        it is under/over-sized, and therefore fails closed until the dedicated
        post-replacement cancellation proof removes it.
        """
        if snapshot.lot is None:
            return None
        owned_stops = self._live_owned_stops(snapshot, owned_cloids)
        if len(owned_stops) != 1:
            return None
        order = owned_stops[0]
        return (
            order
            if self._stop_exactly_covers(
                order,
                symbol=snapshot.symbol,
                position_lots=position_lots,
                exit_side=exit_side,
                lot=snapshot.lot,
            )
            else None
        )

    @staticmethod
    def _live_owned_stops(
        snapshot: SymbolSnapshot, owned_cloids: set[str]
    ) -> tuple[OrderView, ...]:
        """All live same-symbol SLs whose cloids are durably lineage-owned."""
        return tuple(
            order
            for order in snapshot.open_orders
            if str(order.coin) == snapshot.symbol
            and str(order.status).upper() in _LIVE_ORDER_STATUSES
            and str(order.role).upper() == "SL"
            and str(order.cloid) in owned_cloids
        )

    @staticmethod
    def _stop_exactly_covers(
        order: Any,
        *,
        symbol: str,
        position_lots: int,
        exit_side: str,
        lot: LotUnit,
    ) -> bool:
        """Shared exact stop shape/quantity predicate."""
        if str(getattr(order, "coin", "")) != symbol:
            return False
        if str(getattr(order, "status", "")).upper() not in _LIVE_ORDER_STATUSES:
            return False
        if str(getattr(order, "role", "")).upper() != "SL":
            return False
        if not bool(getattr(order, "reduce_only", False)):
            return False
        if str(getattr(order, "side", "")).upper() != str(exit_side).upper():
            return False
        try:
            return (
                quantize_lots(abs(float(getattr(order, "size"))), lot)
                == int(position_lots)
            )
        except (LotQuantizationError, TypeError, ValueError):
            return False

    def _replacement_protection(
        self,
        recovery: Mapping[str, Any],
        snapshot: SymbolSnapshot,
        *,
        position_lots: int,
        exit_side: str,
        owned_cloids: set[str],
    ) -> OrderView | None:
        """Return the one verified current-generation replacement stop.

        This narrower predicate is used only as the safety anchor while stale
        siblings are being removed.  It never by itself qualifies the position
        as protected: the public shared predicate still requires exactly one
        live owned SL.
        """
        if snapshot.lot is None:
            return None
        action_id = compute_partial_action_id(
            kind=PartialActionKind.INSTALL_STOP.value,
            trade_id=int(recovery["trade_id"]),
            entry_cloid=str(recovery["entry_cloid"]),
            entry_request_id=str(recovery["entry_request_id"]),
            generation=int(recovery["generation"]),
            qty_lots=int(position_lots),
        )
        replacement_cloid = compute_partial_action_cloid(action_id)
        action = self.store.get_partial_action(action_id)
        if (
            action is None
            or str(action["kind"]) != PartialActionKind.INSTALL_STOP.value
            or str(action["target_cloid"]) != replacement_cloid
        ):
            return None
        candidates = [
            order
            for order in self._live_owned_stops(snapshot, owned_cloids)
            if str(order.cloid) == replacement_cloid
        ]
        if len(candidates) != 1:
            return None
        replacement = candidates[0]
        return (
            replacement
            if self._stop_exactly_covers(
                replacement,
                symbol=snapshot.symbol,
                position_lots=position_lots,
                exit_side=exit_side,
                lot=snapshot.lot,
            )
            else None
        )

    async def _stale_protection_cleanup(
        self,
        recovery: Mapping[str, Any],
        broker: Any,
        snapshot: SymbolSnapshot,
        *,
        anchor: OrderView,
        owned_cloids: set[str],
    ) -> tuple[bool, bool]:
        """Cancel only stale lineage-owned SLs after an exact anchor is live.

        Returns ``(cleared, progressed)``.  Every stale target is reserved
        under its deterministic ``CANCEL_PROTECTION`` identity before I/O and
        is then queried directly.  A stale order present in the input snapshot
        always requires a fresh snapshot before ``cleared`` can become true.
        UNKNOWN remains query-only; a resend is delegated to ``_cancel_orphan``
        only after durable NOT_APPLIED evidence under the same identity.
        """
        symbol = str(recovery["symbol"])
        self.symbol_locks.require(symbol)
        live_owned = self._live_owned_stops(snapshot, owned_cloids)
        if anchor not in live_owned:
            return False, False
        stale = [
            order for order in live_owned if str(order.cloid) != str(anchor.cloid)
        ]
        actions = [
            row
            for row in self.store.partial_actions_for_lineage(
                int(recovery["trade_id"]), str(recovery["entry_cloid"])
            )
            if str(row["kind"]) == PartialActionKind.CANCEL_PROTECTION.value
        ]
        progressed = False

        # A prior cancel aimed at today's anchor must be proved NOT_APPLIED.
        # It is never resent while that exact stop is the safety anchor.
        for action in actions:
            if str(action["target_cloid"]) != str(anchor.cloid):
                continue
            outcome = self.store.resolve_partial_action(str(action["action_id"]))
            if outcome != ActionOutcome.NOT_APPLIED.value:
                queried = await self._query_action(
                    broker,
                    recovery,
                    str(action["action_id"]),
                    str(anchor.cloid),
                    "ANCHOR_CANCEL",
                    effect_is_absence=True,
                )
                progressed = progressed or queried is not None
            if (
                self.store.resolve_partial_action(str(action["action_id"]))
                != ActionOutcome.NOT_APPLIED.value
            ):
                return False, progressed

        for order in stale:
            action_id = compute_partial_action_id(
                kind=PartialActionKind.CANCEL_PROTECTION.value,
                trade_id=int(recovery["trade_id"]),
                entry_cloid=str(recovery["entry_cloid"]),
                entry_request_id=str(recovery["entry_request_id"]),
                target_cloid=str(order.cloid),
            )
            before = self.store.resolve_partial_action(action_id)
            await self._cancel_orphan(recovery, broker, order)
            queried = await self._query_action(
                broker,
                recovery,
                action_id,
                str(order.cloid),
                "STALE_PROTECTION",
                effect_is_absence=True,
            )
            progressed = progressed or (
                before in (None, ActionOutcome.NOT_APPLIED.value)
                or queried is not None
            )
            if (
                queried != ActionRecordStatus.APPLIED.value
                or self.store.resolve_partial_action(action_id)
                != ActionOutcome.APPLIED.value
            ):
                return False, progressed

        if stale:
            # The cancellation queries are authoritative for each target, but
            # acceptance also requires a new complete symbol snapshot.
            return False, True

        # Prove every earlier stale-stop cancellation terminal/absent directly;
        # broker transport success alone is never accepting evidence.
        for action in actions:
            target = str(action["target_cloid"])
            if target == str(anchor.cloid):
                continue
            queried = await self._query_action(
                broker,
                recovery,
                str(action["action_id"]),
                target,
                "STALE_PROTECTION",
                effect_is_absence=True,
            )
            progressed = progressed or queried is not None
            if (
                queried != ActionRecordStatus.APPLIED.value
                or self.store.resolve_partial_action(str(action["action_id"]))
                != ActionOutcome.APPLIED.value
            ):
                return False, progressed
        return True, progressed

    def _stale_cancel_unknown(self, recovery: Mapping[str, Any]) -> bool:
        """Whether any lineage stale-stop cancellation is still unresolved."""
        return any(
            str(row["kind"]) == PartialActionKind.CANCEL_PROTECTION.value
            and self.store.resolve_partial_action(str(row["action_id"]))
            in (None, ActionOutcome.UNKNOWN.value)
            for row in self.store.partial_actions_for_lineage(
                int(recovery["trade_id"]), str(recovery["entry_cloid"])
            )
        )

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
        if lot is None:
            return False
        try:
            position_lots = quantize_lots(abs(float(position.size)), lot)
        except LotQuantizationError:
            return False
        owned_stops = [
            order
            for order in open_orders
            if getattr(order, "coin", None) == position.symbol
            and str(getattr(order, "role", "")).upper() == "SL"
            and str(getattr(order, "status", "OPEN")).upper()
            in _LIVE_ORDER_STATUSES
            and self._match_order(order) is not None
        ]
        if len(owned_stops) != 1:
            return False
        return self._stop_exactly_covers(
            owned_stops[0],
            symbol=position.symbol,
            position_lots=position_lots,
            exit_side=exit_side_for(position.size),
            lot=lot,
        )

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
        if self.store.has_submission_quarantine():
            # Re-check after every awaited evidence call. A quarantine that
            # appeared mid-cycle dominates before any later reservation/I/O.
            self._partial_event(
                "WARN",
                "PARTIAL_RECOVERY_DEFERRED_QUARANTINE",
                str(recovery["symbol"]),
            )
            return False
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
        if self.store.has_submission_quarantine():
            return False
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
            self._drain_queued_events_locked(symbol)
            self._record_outcome(
                action_id, ActionOutcome.UNKNOWN, "PLACE_RAISED", type(exc).__name__
            )
            return
        self._drain_queued_events_locked(symbol)
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
        if self.store.has_submission_quarantine():
            return False
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
            provenance, _classified_lots, reason = self._classify(recovery, snapshot)
            if provenance is not Provenance.OWNED:
                if provenance is Provenance.UNVERIFIED and not expired:
                    self._partial_event(
                        "WARN",
                        "PARTIAL_EVIDENCE_INCOMPLETE",
                        str(recovery["symbol"]),
                        reason,
                    )
                    return False
                self._abort(recovery, reason)
                return True
            owned = self._owned_cloids(recovery)
            protection = self.qualifying_protection(
                snapshot,
                position_lots=int(position_lots),
                exit_side=exit_side_for(float(snapshot.net_size)),
                owned_cloids=owned,
            )
            anchor = protection or self._replacement_protection(
                recovery,
                snapshot,
                position_lots=int(position_lots),
                exit_side=exit_side_for(float(snapshot.net_size)),
                owned_cloids=owned,
            )
            if anchor is not None:
                cleared, progressed = await self._stale_protection_cleanup(
                    recovery,
                    broker,
                    snapshot,
                    anchor=anchor,
                    owned_cloids=owned,
                )
                if not cleared:
                    if expired:
                        if self._stale_cancel_unknown(recovery):
                            self._abort(recovery, "STALE_PROTECTION_CANCEL_UNKNOWN")
                            return True
                        return self._enter_flatten(
                            recovery, "STALE_PROTECTION_LIVE", int(position_lots)
                        )
                    return progressed
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
        *,
        effect_is_absence: bool = False,
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
        identity_matches = (
            str(getattr(result, "cloid", "") or "") == str(cloid)
            and str(getattr(result, "symbol", "") or "") == symbol
        )
        if not known or not identity_matches:
            self.store.record_partial_action_event(
                action_id=action_id, status=ActionRecordStatus.UNKNOWN.value,
                reason_code=(
                    f"{label}_QUERY_UNKNOWN" if not known
                    else f"{label}_QUERY_IDENTITY_MISMATCH"
                ),
                evidence_source="BROKER",
                evidence={},
            )
            return None
        found = bool(getattr(result, "found", False))
        terminal = bool(getattr(result, "terminal", False))
        raw_status = getattr(result, "raw_status", None)
        # `found` means *live*. For a placement, live or terminal presence
        # proves application. For a cancel, a live target proves NOT_APPLIED
        # while terminal/absent evidence proves the intended absence. Keeping
        # these opposite effects explicit prevents a cancel replay from being
        # authorized by the wrong evidence polarity.
        applied = (
            (not found or terminal)
            if effect_is_absence
            else (found or raw_status is not None)
        )
        status = ActionRecordStatus.APPLIED if applied else ActionRecordStatus.NOT_APPLIED
        self.store.record_partial_action_event(
            action_id=action_id, status=status.value,
            reason_code=f"{label}_QUERY_RESOLVED", evidence_source="BROKER",
            evidence={
                "found": found,
                "terminal": terminal,
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
        prior = self.store.get_partial_action(action_id)
        if prior is not None:
            if (
                str(prior["kind"]) != PartialActionKind.CANCEL_ENTRY.value
                or str(prior["target_cloid"]) != str(recovery["entry_cloid"])
            ):
                raise PartialRecoveryConflictError(
                    "PARTIAL_ACTION_IDENTITY_CONFLICT", f"action_id={action_id}"
                )
            # CANCEL_ENTRY is deliberately generation-independent. A new
            # recovery generation reuses the immutable reservation and its
            # evidence instead of attempting to attach the same identity to a
            # second recovery row.
            self.store.transition_partial_recovery(
                str(recovery["recovery_id"]),
                expected=str(recovery["state"]),
                target=PartialProtectionState.CANCEL_PENDING.value,
                reason_code="CANCEL_ENTRY_RESERVATION_REUSED",
                **dict(fields),
            )
            return True
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
            self._drain_queued_events_locked(symbol)
            self._record_outcome(
                action_id, ActionOutcome.UNKNOWN, "CANCEL_RAISED", type(exc).__name__
            )
            return
        self._drain_queued_events_locked(symbol)
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
        if self.store.has_submission_quarantine():
            return False
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
            if outcome != ActionOutcome.APPLIED.value:
                self._record_outcome(
                    action_id,
                    ActionOutcome.APPLIED,
                    "CANCEL_ENTRY_TERMINAL_OBSERVED",
                )
            self._persist_entry_terminal(recovery, query)
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

    def _persist_entry_terminal(
        self, recovery: Mapping[str, Any], query: Any
    ) -> None:
        """Persist only a terminal state supported by authoritative evidence."""
        raw = str(getattr(query, "raw_status", "") or "").strip().upper()
        aliases = {
            "FILLED": OrderState.FILLED.value,
            "CANCELED": OrderState.CANCELED.value,
            "CANCELLED": OrderState.CANCELED.value,
            "CANCELLED_BY_ENGINE": OrderState.CANCELED.value,
            "REJECTED": OrderState.REJECTED.value,
            "EXPIRED": OrderState.EXPIRED.value,
        }
        status = aliases.get(raw)
        if status is None and bool(getattr(query, "known", False)):
            order = self.store.get_order(str(recovery["entry_cloid"]))
            if order is not None:
                filled, _ = self.store.order_fill_totals(
                    str(recovery["entry_cloid"])
                )
                try:
                    lot = LotUnit(recovery["size_decimals"])
                    filled_lots = quantize_lots(filled, lot)
                    ordered_lots = quantize_lots(float(order["qty"]), lot)
                except (LotQuantizationError, TypeError, ValueError):
                    return
                status = (
                    OrderState.FILLED.value
                    if filled_lots >= ordered_lots
                    else OrderState.CANCELED.value
                )
        if status is not None:
            self.store.update_order_status(
                str(recovery["entry_cloid"]), status
            )

    async def _resolve_after_entry_terminal(
        self, recovery: Mapping[str, Any], broker: Any
    ) -> bool:
        snapshot = await self._snapshot(broker, recovery)
        if self.store.has_submission_quarantine():
            return False
        if (
            snapshot.exact
            and snapshot.lot is not None
            and snapshot.net_size is not None
            and quantize_lots(abs(float(snapshot.net_size)), snapshot.lot) == 0
            and str(recovery["provenance"]) == Provenance.OWNED.value
        ):
            return await self._verify_safe_flat(recovery, broker, snapshot)
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
        owned = self._owned_cloids(recovery)
        protection = self.qualifying_protection(
            snapshot,
            position_lots=position_lots,
            exit_side=exit_side_for(float(snapshot.net_size or 0.0)),
            owned_cloids=owned,
        )
        anchor = protection or self._replacement_protection(
            recovery,
            snapshot,
            position_lots=position_lots,
            exit_side=exit_side_for(float(snapshot.net_size or 0.0)),
            owned_cloids=owned,
        )
        if anchor is not None:
            cleared, progressed = await self._stale_protection_cleanup(
                recovery,
                broker,
                snapshot,
                anchor=anchor,
                owned_cloids=owned,
            )
            if not cleared:
                if self._deadline_expired(recovery, "protect"):
                    if self._stale_cancel_unknown(recovery):
                        self._abort(recovery, "STALE_PROTECTION_CANCEL_UNKNOWN")
                        return True
                    return self._enter_flatten(
                        recovery, "STALE_PROTECTION_LIVE", position_lots
                    )
                return progressed
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
        if self.store.has_submission_quarantine():
            return False
        expired = self._deadline_expired(recovery, "flatten")
        if not snapshot.exact or snapshot.lot is None or snapshot.net_size is None:
            self._abort(recovery, "FLATTEN_EVIDENCE_INCOMPLETE")
            return True
        try:
            live_lots = quantize_lots(abs(float(snapshot.net_size)), snapshot.lot)
        except LotQuantizationError as exc:
            self._abort(recovery, exc.reason_code)
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
            action = attempts[0]
            action_id = str(action["action_id"])
            outcome = self.store.resolve_partial_action(action_id)
            if outcome in (None, ActionOutcome.UNKNOWN.value):
                await self._query_action(
                    broker,
                    recovery,
                    action_id,
                    str(action["target_cloid"]),
                    "FLATTEN",
                )
                outcome = self.store.resolve_partial_action(action_id)
            if outcome in (None, ActionOutcome.UNKNOWN.value):
                # UNKNOWN permits queries only. The attempt sequence and broker
                # mutation count remain frozen until the same cloid resolves.
                if expired:
                    self._abort(recovery, "FLATTEN_DEADLINE_EXPIRED")
                    return True
                if (
                    str(recovery["state"])
                    != PartialProtectionState.FLATTEN_UNKNOWN.value
                ):
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
            if live_lots == 0:
                return await self._verify_safe_flat(recovery, broker, snapshot)
            provenance, classified_lots, reason = self._classify(recovery, snapshot)
            if provenance is not Provenance.OWNED or classified_lots != live_lots:
                self._abort(recovery, reason)
                return True
            if expired:
                self._abort(recovery, "FLATTEN_DEADLINE_EXPIRED")
                return True
            # Definitive outcome plus authoritative proof of a nonzero
            # remainder: only now may the sequence advance.
            self.store.bump_partial_flatten_seq(str(recovery["recovery_id"]), seq)
            return True

        if live_lots == 0:
            return await self._verify_safe_flat(recovery, broker, snapshot)
        provenance, classified_lots, reason = self._classify(recovery, snapshot)
        if provenance is not Provenance.OWNED or classified_lots != live_lots:
            self._abort(recovery, reason)
            return True
        if expired:
            self._abort(recovery, "FLATTEN_DEADLINE_EXPIRED")
            return True

        # Re-snapshot immediately before reservation. A manual/foreign change
        # that lands after the phase-entry snapshot therefore cannot influence
        # either the durable target quantity or broker I/O.
        reservation_snapshot = await self._snapshot(broker, recovery)
        if self.store.has_submission_quarantine():
            return False
        reservation_provenance, reservation_lots, reservation_reason = self._classify(
            recovery, reservation_snapshot
        )
        if (
            reservation_provenance is not Provenance.OWNED
            or reservation_lots is None
            or reservation_snapshot.lot is None
        ):
            self._abort(recovery, reservation_reason)
            return True
        if reservation_lots == 0:
            return await self._verify_safe_flat(
                recovery, broker, reservation_snapshot
            )
        if self._deadline_expired(recovery, "flatten"):
            self._abort(recovery, "FLATTEN_DEADLINE_EXPIRED")
            return True

        action_id = compute_partial_action_id(
            kind=PartialActionKind.FLATTEN.value,
            trade_id=int(recovery["trade_id"]),
            entry_cloid=str(recovery["entry_cloid"]),
            entry_request_id=str(recovery["entry_request_id"]),
            generation=int(recovery["generation"]),
            flatten_seq=seq,
            qty_lots=reservation_lots,
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
            qty_lots=reservation_lots,
            position_lots=reservation_lots,
        )
        if not is_replay:
            await self._send_flatten(
                recovery,
                broker,
                action_id,
                cloid,
                reservation_lots,
                reservation_snapshot.lot,
                exit_side_for(float(reservation_snapshot.net_size)),
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
        exit_side: str,
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
                symbol=symbol, cloid=cloid, size=lots_to_size(live_lots, lot),
                exit_side=exit_side,
            )
        except Exception as exc:  # noqa: BLE001
            self._drain_queued_events_locked(symbol)
            self._record_outcome(
                action_id, ActionOutcome.UNKNOWN, "FLATTEN_RAISED", type(exc).__name__
            )
            return
        self._drain_queued_events_locked(symbol)
        self._record_typed_outcome(action_id, result, "FLATTEN")

    async def _verify_safe_flat(
        self, recovery: Mapping[str, Any], broker: Any, snapshot: SymbolSnapshot
    ) -> bool:
        """SAFE_FLAT requires fresh exact evidence on every owned artefact."""
        symbol = str(recovery["symbol"])
        if (
            not snapshot.exact
            or snapshot.lot is None
            or snapshot.net_size is None
        ):
            self._abort(recovery, "SAFE_FLAT_EVIDENCE_INCOMPLETE")
            return True
        try:
            if quantize_lots(abs(float(snapshot.net_size)), snapshot.lot) != 0:
                self._abort(recovery, "SAFE_FLAT_POSITION_NONZERO")
                return True
        except LotQuantizationError as exc:
            self._abort(recovery, exc.reason_code)
            return True

        # A flatten transport result never proves safety. If a flatten identity
        # exists, require a fresh direct query of that exact cloid before any
        # further mutation (including entry/orphan cancellation).
        flatten_actions = self.store.partial_actions_for_recovery(
            str(recovery["recovery_id"]), PartialActionKind.FLATTEN.value
        )
        if flatten_actions:
            latest_flatten = max(
                flatten_actions,
                key=lambda row: (
                    int(row["flatten_seq"] or 0),
                    str(row["reserved_ts"]),
                    str(row["action_id"]),
                ),
            )
            queried = await self._query_action(
                broker,
                recovery,
                str(latest_flatten["action_id"]),
                str(latest_flatten["target_cloid"]),
                "FLATTEN",
            )
            flatten_outcome = self.store.resolve_partial_action(
                str(latest_flatten["action_id"])
            )
            if (
                queried != ActionRecordStatus.APPLIED.value
                or flatten_outcome != ActionOutcome.APPLIED.value
            ):
                if self._deadline_expired(recovery, "flatten"):
                    self._abort(recovery, "FLATTEN_DEADLINE_EXPIRED")
                    return True
                if (
                    flatten_outcome in (None, ActionOutcome.UNKNOWN.value)
                    and str(recovery["state"])
                    != PartialProtectionState.FLATTEN_UNKNOWN.value
                ):
                    self.store.transition_partial_recovery(
                        str(recovery["recovery_id"]),
                        expected=str(recovery["state"]),
                        target=PartialProtectionState.FLATTEN_UNKNOWN.value,
                        reason_code="FLATTEN_OUTCOME_UNKNOWN",
                    )
                    return True
                return False

        provenance, flat_lots, flat_reason = self._classify(recovery, snapshot)
        if provenance is not Provenance.OWNED or flat_lots != 0:
            self._abort(recovery, flat_reason)
            return True

        entry_cloid = str(recovery["entry_cloid"])
        owned = self._owned_cloids(recovery)
        try:
            entry_query = await broker.query_order(entry_cloid, symbol)
        except Exception:  # noqa: BLE001
            entry_query = None
        if self.store.has_submission_quarantine():
            return False
        entry_terminal = bool(
            entry_query is not None
            and getattr(entry_query, "known", False)
            and getattr(entry_query, "terminal", False)
        )
        if entry_terminal:
            self._persist_entry_terminal(recovery, entry_query)
            cancel_action_id = compute_partial_action_id(
                kind=PartialActionKind.CANCEL_ENTRY.value,
                trade_id=int(recovery["trade_id"]),
                entry_cloid=entry_cloid,
                entry_request_id=str(recovery["entry_request_id"]),
            )
            if (
                self.store.get_partial_action(cancel_action_id) is not None
                and self.store.resolve_partial_action(cancel_action_id)
                != ActionOutcome.APPLIED.value
            ):
                self._record_outcome(
                    cancel_action_id,
                    ActionOutcome.APPLIED,
                    "CANCEL_ENTRY_TERMINAL_OBSERVED",
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

        # No accepting state may coexist with an unresolved lineage action.
        # Query each exact target with the correct evidence polarity; never
        # reserve or resend while any result remains UNKNOWN.
        for action in self.store.partial_actions_for_lineage(
            int(recovery["trade_id"]), entry_cloid
        ):
            action_id = str(action["action_id"])
            if self.store.resolve_partial_action(action_id) not in (
                None,
                ActionOutcome.UNKNOWN.value,
            ):
                continue
            kind = PartialActionKind(str(action["kind"]))
            await self._query_action(
                broker,
                recovery,
                action_id,
                str(action["target_cloid"]),
                kind.value,
                effect_is_absence=kind
                in {
                    PartialActionKind.CANCEL_ENTRY,
                    PartialActionKind.CANCEL_PROTECTION,
                },
            )
        unresolved = [
            action
            for action in self.store.partial_actions_for_lineage(
                int(recovery["trade_id"]), entry_cloid
            )
            if self.store.resolve_partial_action(str(action["action_id"]))
            in (None, ActionOutcome.UNKNOWN.value)
        ]
        if unresolved:
            if in_flatten and self._deadline_expired(recovery, "flatten"):
                self._abort(recovery, "LINEAGE_ACTION_UNRESOLVED")
                return True
            return False

        try:
            filled_qty, _ = self.store.order_fill_totals(entry_cloid)
            safe_flat_filled_lots = quantize_lots(filled_qty, snapshot.lot)
        except LotQuantizationError as exc:
            self._abort(recovery, exc.reason_code)
            return True
        self.store.transition_partial_recovery(
            str(recovery["recovery_id"]),
            expected=str(recovery["state"]),
            target=PartialProtectionState.SAFE_FLAT.value,
            reason_code="SAFE_FLAT",
            position_lots=0,
            filled_lots=safe_flat_filled_lots,
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
        prior = self.store.get_partial_action(action_id)
        if prior is None:
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
        if (
            str(prior["kind"]) != PartialActionKind.CANCEL_ENTRY.value
            or str(prior["target_cloid"]) != str(recovery["entry_cloid"])
        ):
            raise PartialRecoveryConflictError(
                "PARTIAL_ACTION_IDENTITY_CONFLICT", f"action_id={action_id}"
            )
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
        prior = self.store.get_partial_action(action_id)
        is_replay = prior is not None
        if prior is None:
            self.store.reserve_partial_action(
                recovery_id=str(recovery["recovery_id"]),
                action_id=action_id,
                kind=PartialActionKind.CANCEL_PROTECTION.value,
                target_cloid=str(order.cloid),
                expected_state=str(recovery["state"]),
                next_state=str(recovery["state"]),
                reason_code="CANCEL_PROTECTION_RESERVED",
            )
        elif (
            str(prior["kind"]) != PartialActionKind.CANCEL_PROTECTION.value
            or str(prior["target_cloid"]) != str(order.cloid)
        ):
            raise PartialRecoveryConflictError(
                "PARTIAL_ACTION_IDENTITY_CONFLICT", f"action_id={action_id}"
            )
        outcome = self.store.resolve_partial_action(action_id)
        if is_replay and outcome != ActionOutcome.NOT_APPLIED.value:
            await self._query_action(
                broker,
                recovery,
                action_id,
                str(order.cloid),
                "ORPHAN",
                effect_is_absence=True,
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
            self._drain_queued_events_locked(symbol)
            self._record_outcome(
                action_id, ActionOutcome.UNKNOWN, "CANCEL_RAISED", type(exc).__name__
            )
            return
        self._drain_queued_events_locked(symbol)
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
                request_id = str(
                    candidate["group_id"]
                    or candidate["order_ref"]
                    or candidate["decision_uid"]
                )
                latest = self.store.latest_partial_recovery_for_symbol(symbol)
                same_lineage = bool(
                    latest is not None
                    and int(latest["trade_id"]) == int(candidate["trade_id"])
                    and str(latest["entry_cloid"]) == str(candidate["cloid"])
                )
                if (
                    same_lineage
                    and str(latest["state"])
                    == PartialProtectionState.PROTECTED_PARTIAL.value
                ):
                    # Whether pending human proof or already archived, this
                    # accepting generation is not a legacy orphan.
                    continue
                post_safe_flat = bool(
                    same_lineage
                    and str(latest["state"])
                    == PartialProtectionState.SAFE_FLAT.value
                )
                generation = (
                    int(latest["generation"]) + 1 if post_safe_flat else 0
                )
                abort_reason: str | None = None
                snapshot: SymbolSnapshot | None = None
                position_lots: int | None = None
                if first_fill is None:
                    # No trustworthy observation time means already expired,
                    # and weak evidence may not authorize even a snapshot-led
                    # broker mutation.
                    first_fill = datetime(1970, 1, 1, tzinfo=UTC)
                    abort_reason = "LEGACY_FIRST_OBSERVATION_MISSING"
                elif broker is None:
                    abort_reason = "RECOVERY_API_UNAVAILABLE"
                else:
                    synthetic = {
                        "recovery_id": compute_partial_recovery_id(
                            trade_id=int(candidate["trade_id"]),
                            entry_cloid=str(candidate["cloid"]),
                            generation=generation,
                        ),
                        "symbol": symbol,
                        "trade_id": int(candidate["trade_id"]),
                        "entry_cloid": str(candidate["cloid"]),
                    }
                    snapshot = await self._snapshot(broker, synthetic)
                    if self.store.has_submission_quarantine():
                        # A quarantine that appeared during the read-only
                        # snapshot wins. Retry the scan only after it resolves.
                        self._legacy_partial_scan_done = False
                        return
                    no_fresh_post_flat_evidence = False
                    if (
                        post_safe_flat
                        and snapshot.exact
                        and snapshot.lot is not None
                        and snapshot.net_size is not None
                    ):
                        try:
                            candidate_filled_lots = quantize_lots(
                                float(candidate["filled_qty"]), snapshot.lot
                            )
                            baseline_filled_lots = int(latest["filled_lots"])
                            position_lots = quantize_lots(
                                abs(float(snapshot.net_size)), snapshot.lot
                            )
                            no_fresh_post_flat_evidence = (
                                position_lots > 0
                                and candidate_filled_lots
                                <= baseline_filled_lots
                            )
                        except (LotQuantizationError, TypeError, ValueError):
                            no_fresh_post_flat_evidence = True
                    if no_fresh_post_flat_evidence:
                        provenance = Provenance.AMBIGUOUS
                        abort_reason = (
                            "POST_SAFE_FLAT_NO_FRESH_OWNED_EVIDENCE"
                        )
                    else:
                        provenance, position_lots, abort_reason = self._classify(
                            synthetic, snapshot
                        )
                    if provenance is Provenance.OWNED and position_lots:
                        abort_reason = None
                    elif (
                        post_safe_flat
                        and provenance is Provenance.OWNED
                        and position_lots == 0
                    ):
                        # A fresh exact locked snapshot still proves the prior
                        # accepting flat result. There is nothing to reopen.
                        continue
                    elif abort_reason == "OWNED":
                        abort_reason = "LEGACY_ZERO_POSITION_CONFLICT"

                # Conservative seeding: the budget is measured from the
                # earliest durable fill; missing evidence uses the Unix epoch,
                # never a fresh 10-second window.
                deadline = first_fill + timedelta(seconds=PROTECT_DEADLINE_S)
                lot = None if snapshot is None else snapshot.lot
                ordered_lots: int | None = None
                filled_lots: int | None = None
                if lot is not None:
                    try:
                        ordered_lots = quantize_lots(
                            float(candidate["ordered_qty"]), lot
                        )
                        filled_lots = quantize_lots(
                            float(candidate["filled_qty"]), lot
                        )
                    except LotQuantizationError as exc:
                        abort_reason = exc.reason_code
                try:
                    opened = self.store.open_partial_recovery(
                        run_id=self.run_id,
                        symbol=symbol,
                        trade_id=int(candidate["trade_id"]),
                        entry_cloid=str(candidate["cloid"]),
                        entry_decision_uid=str(candidate["decision_uid"]),
                        entry_request_id=request_id,
                        first_observed_ts=first_fill,
                        protect_deadline_ts=deadline,
                        generation=generation,
                        size_decimals=(
                            None if lot is None else lot.size_decimals
                        ),
                        ordered_lots=ordered_lots,
                        filled_lots=filled_lots,
                        reason_code="PARTIAL_LEGACY_RECOVERED",
                    )
                except PartialRecoveryConflictError as exc:
                    self._disarm_for_partial(
                        "PARTIAL_RECOVERY_OPEN_FAILED", symbol, exc.code
                    )
                    continue
                if abort_reason is not None:
                    self.store.transition_partial_recovery(
                        str(opened["recovery_id"]),
                        expected=PartialProtectionState.PARTIAL_DETECTED.value,
                        target=PartialProtectionState.UNPROTECTED_ABORT.value,
                        reason_code=abort_reason,
                    )
                    self._disarm_for_partial(
                        "UNPROTECTED_ABORT", symbol, abort_reason
                    )
                    continue
                self._disarm_for_partial(
                    "PARTIAL_LEGACY_DETECTED", symbol,
                    (
                        f"cloid={candidate['cloid']} "
                        f"filled={candidate['filled_qty']} lots={position_lots}"
                    ),
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
