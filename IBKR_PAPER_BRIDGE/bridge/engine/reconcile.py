"""TS-P1-005 bounded, immutable full reconciliation capture.

One cycle obtains authoritative read-only broker evidence for orders, fills,
positions, balances, margin and funding, reads the durable local intent and
pending-action state, compares them deterministically, and commits exactly one
outcome: an accepted checkpoint, or a reason-coded failed attempt that leaves
the previous accepted checkpoint untouched.

Nothing in this module mutates exchange state. Every path that cannot *prove*
completeness, exactness and freshness is non-accepting.
"""

from __future__ import annotations

import asyncio
import json
import math
import time
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from bridge.engine.types import (
    DIFF_ACCOUNT_INCONSISTENT,
    DIFF_EXCHANGE_IDENTITY_CONFLICT,
    DIFF_FOREIGN_ORDER_OBSERVED,
    DIFF_FUNDING_UNATTRIBUTED,
    DIFF_LOCAL_ORDER_STATUS_UNKNOWN,
    DIFF_ORPHAN_OWNED_CLOID,
    DIFF_OWNED_ORDER_MISSING,
    DIFF_OWNED_ORDER_QTY_MISMATCH,
    DIFF_OWNED_ORDER_STATUS_MISMATCH,
    DIFF_OWNED_ORDER_UNKNOWN_QUANTUM,
    DIFF_PENDING_ACTION_DIVERGENCE,
    DIFF_POSITION_QTY_MISMATCH,
    DIFF_POSITION_UNKNOWN_QUANTUM,
    DIFF_UNKNOWN_OWNERSHIP_ORDER,
    DIFF_UNKNOWN_OWNERSHIP_POSITION,
    FULL_RECONCILE_COVERAGE_GAP,
    FULL_RECONCILE_COVERAGE_UNPROVABLE,
    FULL_RECONCILE_DEADLINE_S,
    FULL_RECONCILE_MAX_SKEW_S,
    REQUIRED_RECONCILE_COMPONENTS,
    TERMINAL_ORDER_STATES,
    ComponentEvidence,
    FullReconcileResult,
    FundingAttribution,
    FundingEventRecord,
    LotQuantizationError,
    ReconcileAttemptState,
    ReconcileComponentKind,
    ReconcileComponentStatus,
    ReconcileDiffKind,
    ReconcileDiffRecord,
    ReconcileOwnership,
    normalize_raw_order_status,
    quantize_lots,
    reconcile_digest,
)

SNAPSHOT_VERSION = "ts-p1-005-snapshot-v1"

# Absolute float residue tolerated when re-checking the account identity
# ``available_margin == equity - margin_used``. It is deliberately far below
# any economically meaningful amount: this is a float-representation guard,
# never a permissive band, and it is never applied to quantities (those are
# compared in exact integer lots).
ACCOUNT_IDENTITY_ABS_TOL = 1e-6

_FULL_WRITER_GUARDS: dict[str, asyncio.Lock] = {}


def _guard_key(store: Any) -> str:
    try:
        return str(Path(store.db_path).resolve())
    except (OSError, TypeError, ValueError):  # pragma: no cover - exotic paths
        return str(getattr(store, "db_path", id(store)))


def full_writer_guard(store: Any) -> asyncio.Lock:
    """The one global full-reconcile writer guard for a given database."""
    key = _guard_key(store)
    guard = _FULL_WRITER_GUARDS.get(key)
    if guard is None:
        guard = asyncio.Lock()
        _FULL_WRITER_GUARDS[key] = guard
    return guard


def _sign(direction: str) -> int:
    return 1 if str(direction).upper() == "LONG" else -1


def _finite(value: object) -> float | None:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


class FullReconciler:
    """One bounded full-portfolio capture per :meth:`run_cycle` call."""

    def __init__(
        self,
        *,
        store: Any,
        broker: Any,
        run_id: str,
        order_manager: Any | None = None,
        clock: Callable[[], datetime] | None = None,
        monotonic: Callable[[], float] | None = None,
        deadline_s: float = FULL_RECONCILE_DEADLINE_S,
        max_skew_s: float = FULL_RECONCILE_MAX_SKEW_S,
    ) -> None:
        self.store = store
        self.broker = broker
        self.run_id = run_id
        self.order_manager = order_manager
        self._clock: Callable[[], datetime] = clock or (lambda: datetime.now(UTC))
        self._monotonic: Callable[[], float] = monotonic or time.monotonic
        self.deadline_s = float(deadline_s)
        self.max_skew_s = float(max_skew_s)
        # Generation identity of the client the capture started with. A broker
        # rebuild mid-collection therefore invalidates the whole attempt.
        self._client_generation: tuple[int, int] | None = None
        # Set when a collection step ran out of the wall-clock budget. The
        # post-hoc monotonic check below stays, but it can only fire *after*
        # an unbounded await has already returned; this flag is what makes a
        # hung broker call fail closed in bounded wall time.
        self._deadline_hit = False

    # ------------------------------------------------------------------
    # public entry point
    # ------------------------------------------------------------------

    async def run_cycle(self) -> FullReconcileResult:
        """Collect, validate, diff and atomically persist exactly one attempt.

        Ordinary adapter and validation failures are recorded as a durable
        failed attempt and returned. ``BaseException`` (a real kill) is
        deliberately *not* caught: the reserved attempt then stays
        ``COLLECTING`` on disk and is resolved as INCOMPLETE on reopen.
        """
        guard = full_writer_guard(self.store)
        self._deadline_hit = False
        started_ts = self._now()
        mono_start = self._monotonic()
        overlapped = guard.locked()
        attempt_id = self.store.reserve_reconcile_attempt(
            run_id=self.run_id,
            started_ts=started_ts,
            deadline_s=self.deadline_s,
            max_skew_s=self.max_skew_s,
        )
        if overlapped:
            # No broker I/O at all: an overlapping full attempt is refused, not
            # queued, so two captures can never interleave into one epoch.
            return self._fail(
                attempt_id=attempt_id,
                started_ts=started_ts,
                mono_start=mono_start,
                state=ReconcileAttemptState.INCOMPLETE,
                reason_code="FULL_RECONCILE_OVERLAP",
                components=(),
            )
        await guard.acquire()
        try:
            return await self._run_locked(attempt_id, started_ts, mono_start)
        except Exception as exc:  # noqa: BLE001 - any handled failure is evidence
            return self._fail(
                attempt_id=attempt_id,
                started_ts=started_ts,
                mono_start=mono_start,
                state=ReconcileAttemptState.INCOMPLETE,
                reason_code=self._safe_reason("FULL_RECONCILE_FAILED", exc),
                components=(),
            )
        finally:
            guard.release()

    # ------------------------------------------------------------------
    # collection
    # ------------------------------------------------------------------

    async def _run_locked(
        self, attempt_id: str, started_ts: datetime, mono_start: float
    ) -> FullReconcileResult:
        missing = self._missing_surface()
        if missing:
            return self._fail(
                attempt_id=attempt_id,
                started_ts=started_ts,
                mono_start=mono_start,
                state=ReconcileAttemptState.INCOMPLETE,
                reason_code="FULL_RECONCILE_API_UNAVAILABLE",
                components=(),
            )
        self._client_generation = self._generation()

        # Drain queued broker callbacks under the existing per-symbol writer
        # locks first, so the capture observes one coherent local epoch.
        if self.order_manager is not None:
            drain = getattr(self.order_manager, "drain_queued_events", None)
            if drain is not None:
                await drain()

        bounds = self._coverage_bounds(started_ts)
        if isinstance(bounds, str):
            return self._fail(
                attempt_id=attempt_id,
                started_ts=started_ts,
                mono_start=mono_start,
                state=ReconcileAttemptState.INCOMPLETE,
                reason_code=bounds,
                components=(),
            )
        start_ms, end_ms = bounds

        components: dict[ReconcileComponentKind, ComponentEvidence] = {}
        components[ReconcileComponentKind.PENDING_ACTIONS] = (
            self._pending_actions_evidence()
        )

        portfolio = await self._guarded(
            ReconcileComponentKind.POSITIONS,
            lambda: self.broker.portfolio_evidence(),
            budget=self._budget(mono_start),
        )
        if isinstance(portfolio, ComponentEvidence):
            # A failed account read invalidates all three derived components.
            for kind in (
                ReconcileComponentKind.POSITIONS,
                ReconcileComponentKind.BALANCES,
                ReconcileComponentKind.MARGIN,
            ):
                components[kind] = ComponentEvidence(
                    kind=kind,
                    source=portfolio.source,
                    status=portfolio.status,
                    observed_ts=portfolio.observed_ts,
                    reason_code=portfolio.reason_code,
                )
        else:
            components[ReconcileComponentKind.POSITIONS] = portfolio.positions
            components[ReconcileComponentKind.BALANCES] = portfolio.balances
            components[ReconcileComponentKind.MARGIN] = portfolio.margin

        components[ReconcileComponentKind.OPEN_ORDERS] = self._as_component(
            ReconcileComponentKind.OPEN_ORDERS,
            await self._guarded(
                ReconcileComponentKind.OPEN_ORDERS,
                lambda: self.broker.open_orders_evidence(),
                budget=self._budget(mono_start),
            ),
        )
        components[ReconcileComponentKind.FILLS] = self._as_component(
            ReconcileComponentKind.FILLS,
            await self._guarded(
                ReconcileComponentKind.FILLS,
                lambda: self.broker.fills_evidence(
                    start_ms=start_ms, end_ms=end_ms
                ),
                budget=self._budget(mono_start),
            ),
        )
        components[ReconcileComponentKind.FUNDING] = self._as_component(
            ReconcileComponentKind.FUNDING,
            await self._guarded(
                ReconcileComponentKind.FUNDING,
                lambda: self.broker.funding_evidence(
                    start_ms=start_ms, end_ms=end_ms
                ),
                budget=self._budget(mono_start),
            ),
        )

        ended_ts = self._now()
        elapsed = self._monotonic() - mono_start
        ordered = tuple(components[kind] for kind in REQUIRED_RECONCILE_COMPONENTS)

        if self._deadline_hit:
            # A collection step was cut off by the wall-clock budget itself.
            return self._fail(
                attempt_id=attempt_id,
                started_ts=started_ts,
                mono_start=mono_start,
                state=ReconcileAttemptState.STALE,
                reason_code="FULL_RECONCILE_DEADLINE_EXCEEDED",
                components=ordered,
                ended_ts=ended_ts,
            )

        envelope_reason = self._envelope_failure(
            started_ts=started_ts,
            ended_ts=ended_ts,
            elapsed=elapsed,
            components=ordered,
        )
        if envelope_reason is not None:
            return self._fail(
                attempt_id=attempt_id,
                started_ts=started_ts,
                mono_start=mono_start,
                state=ReconcileAttemptState.STALE,
                reason_code=envelope_reason,
                components=ordered,
                ended_ts=ended_ts,
            )

        state, reason = self._collection_verdict(ordered)
        if state is not ReconcileAttemptState.COMPLETE:
            return self._fail(
                attempt_id=attempt_id,
                started_ts=started_ts,
                mono_start=mono_start,
                state=state,
                reason_code=reason,
                components=ordered,
                ended_ts=ended_ts,
            )

        coverage_reason = self._coverage_failure(
            components, start_ms=start_ms, end_ms=end_ms
        )
        if coverage_reason is not None:
            # The evidence is internally healthy but does not *prove* the
            # required continuous interval; accepting it would advance the
            # coverage pointer over an interval nobody observed.
            return self._fail(
                attempt_id=attempt_id,
                started_ts=started_ts,
                mono_start=mono_start,
                state=ReconcileAttemptState.INCOMPLETE,
                reason_code=coverage_reason,
                components=ordered,
                ended_ts=ended_ts,
            )

        diffs, funding_events = self._build_diff(components)
        canonical_hash = self._canonical_hash(ordered, diffs)
        blocking = tuple(diff for diff in diffs if diff.blocking)
        accepted = not blocking
        final_state = (
            ReconcileAttemptState.COMPLETE
            if accepted
            else ReconcileAttemptState.CONFLICTING
        )
        reason_code = "ACCEPTED" if accepted else blocking[0].reason_code
        duration_ms = max(int(round(elapsed * 1000)), 0)

        self.store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=final_state,
            ended_ts=ended_ts,
            duration_ms=duration_ms,
            canonical_hash=canonical_hash,
            reason_code=reason_code,
            components=ordered,
            diffs=diffs,
            funding_events=funding_events,
            accepted=accepted,
            fresh=True,
            snapshot_payload=self._snapshot_payload(ordered, diffs, funding_events),
            # Only an accepted attempt advances coverage, and it advances to
            # exactly the interval this capture proved.
            coverage_upper_bound_ms=end_ms if accepted else None,
        )
        return FullReconcileResult(
            attempt_id=attempt_id,
            run_id=self.run_id,
            state=final_state,
            started_ts=started_ts,
            ended_ts=ended_ts,
            duration_ms=duration_ms,
            components=ordered,
            diffs=diffs,
            funding_events=funding_events,
            canonical_hash=canonical_hash,
            reason_code=reason_code,
            accepted=accepted,
        )

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    def _now(self) -> datetime:
        value = self._clock()
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    def _missing_surface(self) -> tuple[str, ...]:
        required = (
            "lot_unit",
            "portfolio_evidence",
            "open_orders_evidence",
            "fills_evidence",
            "funding_evidence",
        )
        return tuple(name for name in required if getattr(self.broker, name, None) is None)

    def _generation(self) -> tuple[int, int]:
        """Identity of the adapter's live client pair.

        A reconnect that rebuilds the SDK clients changes these ids, so
        evidence collected across a rebuild can be detected and refused
        instead of silently mixed into one snapshot.
        """
        return (
            id(getattr(self.broker, "info", None)),
            id(getattr(self.broker, "exchange", None)),
        )

    @staticmethod
    def _safe_reason(prefix: str, exc: BaseException) -> str:
        """Secret-safe reason code: type name only, never a payload."""
        name = type(exc).__name__.upper()
        cleaned = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name)
        return f"{prefix}:{cleaned}"[:96]

    def _budget(self, mono_start: float) -> float:
        """Wall-clock budget still available to the next collection step."""
        return self.deadline_s - (self._monotonic() - mono_start)

    def _deadline_evidence(self, kind: ReconcileComponentKind) -> ComponentEvidence:
        return ComponentEvidence(
            kind=kind,
            source="BROKER",
            status=ReconcileComponentStatus.STALE,
            observed_ts=None,
            reason_code=f"{kind.value}_DEADLINE_EXCEEDED",
        )

    async def _guarded(
        self,
        kind: ReconcileComponentKind,
        factory: Callable[[], Any],
        *,
        budget: float,
    ) -> Any:
        """Await one adapter call under the *remaining* capture deadline.

        ``asyncio.timeout`` cancels the current task rather than wrapping the
        call in a child task, so an outer ``CancelledError`` and a real
        ``BaseException`` kill both keep propagating exactly as before. A hung
        adapter await is bounded here, not only detected afterwards.

        The awaitable is built by ``factory`` so that an exhausted budget never
        creates a coroutine that is then abandoned unawaited.
        """
        if budget <= 0:
            self._deadline_hit = True
            return self._deadline_evidence(kind)
        try:
            async with asyncio.timeout(budget) as scope:
                return await factory()
        except TimeoutError:
            if scope.expired():
                self._deadline_hit = True
                return self._deadline_evidence(kind)
            return ComponentEvidence(
                kind=kind,
                source="BROKER",
                status=ReconcileComponentStatus.UNAVAILABLE,
                observed_ts=None,
                reason_code=f"{kind.value}_QUERY_FAILED:TIMEOUTERROR",
            )
        except Exception as exc:  # noqa: BLE001 - a failed read is inexact evidence
            return ComponentEvidence(
                kind=kind,
                source="BROKER",
                status=ReconcileComponentStatus.UNAVAILABLE,
                observed_ts=None,
                reason_code=self._safe_reason(f"{kind.value}_QUERY_FAILED", exc),
            )

    # ------------------------------------------------------------------
    # durable fills/funding coverage continuity
    # ------------------------------------------------------------------

    def _coverage_bounds(self, started_ts: datetime) -> tuple[int, int] | str:
        """Lower/upper epoch-ms bounds this capture must cover continuously.

        There is no fixed lookback. Every capture after the first acceptance
        starts at the upper bound the last *accepted* checkpoint proved, so a
        failed attempt or a downtime widens the next window instead of silently
        skipping the interval nobody observed.

        Before the first acceptance there is no pointer, and the current run's
        durable ``started_ts`` alone is *not* a safe floor: a run that never
        accepted anything and was then restarted would hand the new run a lower
        bound after the old run's observation window, silently dropping it. The
        floor is therefore the earlier of the current run's start and the
        earliest start in the append-only attempt ledger (which already
        includes this attempt's own durable reservation).

        Returns a reason code string when no provable lower bound exists.
        """
        end_ms = int(started_ts.timestamp() * 1000)
        pointer = self.store.reconcile_coverage_upper_bound_ms()
        if pointer is None:
            run_started = self.store.run_started_ts(self.run_id)
            if run_started is None:
                # No accepted coverage and no durable run lineage: any lower
                # bound would be invented.
                return FULL_RECONCILE_COVERAGE_UNPROVABLE
            floor = run_started
            earliest_attempt = self.store.earliest_reconcile_attempt_started_ts()
            if earliest_attempt is not None and earliest_attempt < floor:
                floor = earliest_attempt
            start_ms = int(floor.timestamp() * 1000)
        else:
            start_ms = int(pointer)
        if start_ms > end_ms:
            # The required interval ends before it starts (clock rollback or a
            # pointer from the future): nothing here can be proven.
            return FULL_RECONCILE_COVERAGE_UNPROVABLE
        return start_ms, end_ms

    @staticmethod
    def _coverage_failure(
        components: Mapping[ReconcileComponentKind, ComponentEvidence],
        *,
        start_ms: int,
        end_ms: int,
    ) -> str | None:
        """Refuse acceptance unless the evidence covers the whole interval.

        The adapter reports the cursor bounds it actually walked. A component
        whose bounds do not contain ``[start_ms, end_ms]`` — because retention,
        the page budget or the deadline stopped it short — leaves a hole, so
        the attempt fails closed rather than advancing the coverage pointer
        over unobserved time.
        """
        for kind in (ReconcileComponentKind.FILLS, ReconcileComponentKind.FUNDING):
            component = components.get(kind)
            if component is None:
                return FULL_RECONCILE_COVERAGE_GAP
            if component.cursor_start_ms is None or component.cursor_end_ms is None:
                return FULL_RECONCILE_COVERAGE_GAP
            if component.cursor_start_ms > start_ms or component.cursor_end_ms < end_ms:
                return FULL_RECONCILE_COVERAGE_GAP
        return None

    def _as_component(
        self, kind: ReconcileComponentKind, value: Any
    ) -> ComponentEvidence:
        if isinstance(value, ComponentEvidence) and value.kind is kind:
            return value
        if isinstance(value, ComponentEvidence):
            return ComponentEvidence(
                kind=kind,
                source=value.source,
                status=value.status,
                observed_ts=value.observed_ts,
                reason_code=value.reason_code,
            )
        return ComponentEvidence(
            kind=kind,
            source="BROKER",
            status=ReconcileComponentStatus.MALFORMED,
            observed_ts=None,
            reason_code=f"{kind.value}_EVIDENCE_MALFORMED",
        )

    def _pending_actions_evidence(self) -> ComponentEvidence:
        rows = tuple(
            {
                "kind": str(row["kind"]),
                "id": str(row["id"]),
                "state": str(row["state"]),
                "symbol": str(row.get("symbol") or ""),
            }
            for row in self.store.pending_reconcile_actions()
        )
        return ComponentEvidence(
            kind=ReconcileComponentKind.PENDING_ACTIONS,
            source="LOCAL",
            status=ReconcileComponentStatus.COMPLETE,
            observed_ts=self._now(),
            rows=rows,
            exact=True,
            complete=True,
            reason_code="LOCAL_PENDING_ACTIONS",
        )

    def _envelope_failure(
        self,
        *,
        started_ts: datetime,
        ended_ts: datetime,
        elapsed: float,
        components: Sequence[ComponentEvidence],
    ) -> str | None:
        """D2=A envelope: deadline, skew, clock rollback and future evidence."""
        if elapsed > self.deadline_s:
            return "FULL_RECONCILE_DEADLINE_EXCEEDED"
        if ended_ts < started_ts:
            return "FULL_RECONCILE_CLOCK_ROLLBACK"
        if self._client_generation is not None and (
            self._generation() != self._client_generation
        ):
            return "FULL_RECONCILE_CLIENT_REBUILT"
        stamps = [
            component.observed_ts
            for component in components
            if component.observed_ts is not None
        ]
        if not stamps:
            return None
        normalized = [stamp.astimezone(UTC) for stamp in stamps]
        if (max(normalized) - min(normalized)).total_seconds() > self.max_skew_s:
            return "FULL_RECONCILE_SOURCE_SKEW"
        if (max(normalized) - ended_ts).total_seconds() > self.max_skew_s:
            return "FULL_RECONCILE_SOURCE_IN_FUTURE"
        if (started_ts - min(normalized)).total_seconds() > self.max_skew_s:
            return "FULL_RECONCILE_SOURCE_STALE"
        return None

    @staticmethod
    def _collection_verdict(
        components: Sequence[ComponentEvidence],
    ) -> tuple[ReconcileAttemptState, str]:
        present = {component.kind for component in components}
        for kind in REQUIRED_RECONCILE_COMPONENTS:
            if kind not in present:
                return (
                    ReconcileAttemptState.INCOMPLETE,
                    f"{kind.value}_COMPONENT_MISSING",
                )
        conflicting = [
            component
            for component in components
            if component.status is ReconcileComponentStatus.CONFLICTING
        ]
        if conflicting:
            return (
                ReconcileAttemptState.CONFLICTING,
                f"{conflicting[0].kind.value}_CONFLICTING",
            )
        stale = [
            component
            for component in components
            if component.status is ReconcileComponentStatus.STALE
        ]
        if stale:
            return ReconcileAttemptState.STALE, f"{stale[0].kind.value}_STALE"
        rejected = [component for component in components if not component.accepted]
        if rejected:
            return (
                ReconcileAttemptState.INCOMPLETE,
                f"{rejected[0].kind.value}_{rejected[0].status.value}",
            )
        return ReconcileAttemptState.COMPLETE, "COMPLETE"

    @staticmethod
    def _canonical_hash(
        components: Sequence[ComponentEvidence],
        diffs: Sequence[ReconcileDiffRecord],
    ) -> str:
        """Deterministic over evidence content and diff only.

        Attempt ids, wall-clock bounds and wire row order are deliberately
        excluded, so identical evidence and identical durable state always
        produce the same hash.
        """
        return reconcile_digest({
            "version": SNAPSHOT_VERSION,
            "components": {
                component.kind.value: component.digest
                for component in sorted(components, key=lambda item: item.kind.value)
            },
            "diffs": [diff.canonical() for diff in diffs],
        })

    def _snapshot_payload(
        self,
        components: Sequence[ComponentEvidence],
        diffs: Sequence[ReconcileDiffRecord],
        funding_events: Sequence[FundingEventRecord],
    ) -> dict[str, Any]:
        return {
            "version": SNAPSHOT_VERSION,
            "run_id": self.run_id,
            "components": {
                component.kind.value: {
                    "source": component.source,
                    "status": component.status.value,
                    "observed_ts": (
                        component.observed_ts.astimezone(UTC).isoformat()
                        if component.observed_ts is not None
                        else None
                    ),
                    "row_count": len(component.rows),
                    "page_count": component.page_count,
                    "call_count": component.call_count,
                    "cursor_start_ms": component.cursor_start_ms,
                    "cursor_end_ms": component.cursor_end_ms,
                    "digest": component.digest,
                }
                for component in sorted(components, key=lambda item: item.kind.value)
            },
            "diffs": [diff.canonical() for diff in diffs],
            "funding_event_ids": sorted(
                event.event_id for event in funding_events
            ),
            "funding_event_digests": {
                event.event_id: event.digest
                for event in sorted(funding_events, key=lambda item: item.event_id)
            },
        }

    def _fail(
        self,
        *,
        attempt_id: str,
        started_ts: datetime,
        mono_start: float,
        state: ReconcileAttemptState,
        reason_code: str,
        components: Sequence[ComponentEvidence],
        ended_ts: datetime | None = None,
    ) -> FullReconcileResult:
        """Record a non-accepting attempt; the prior pointer is never touched."""
        resolved_end = ended_ts or self._now()
        duration_ms = max(int(round((self._monotonic() - mono_start) * 1000)), 0)
        ordered = tuple(components)
        # Funding evidence that itself validated is retained even when the
        # composite attempt fails: the ledger is append-only evidence, not a
        # by-product of acceptance.
        funding_events, funding_diffs = self._funding_records_if_valid(ordered)
        evidence_diffs = self._conflict_evidence_diffs(ordered) + funding_diffs
        try:
            self.store.finalize_reconcile_attempt(
                attempt_id=attempt_id,
                state=state,
                ended_ts=resolved_end,
                duration_ms=duration_ms,
                canonical_hash=None,
                reason_code=reason_code,
                components=ordered,
                diffs=evidence_diffs,
                funding_events=funding_events,
                accepted=False,
                fresh=False,
                snapshot_payload=None,
            )
        except Exception:  # noqa: BLE001 - evidence write failure must not mask
            self.store.finalize_reconcile_attempt(
                attempt_id=attempt_id,
                state=state,
                ended_ts=resolved_end,
                duration_ms=duration_ms,
                canonical_hash=None,
                reason_code="FULL_RECONCILE_EVIDENCE_WRITE_FAILED",
                components=(),
                diffs=(),
                funding_events=(),
                accepted=False,
                fresh=False,
                snapshot_payload=None,
            )
        return FullReconcileResult(
            attempt_id=attempt_id,
            run_id=self.run_id,
            state=state,
            started_ts=started_ts,
            ended_ts=resolved_end,
            duration_ms=duration_ms,
            components=ordered,
            diffs=evidence_diffs,
            funding_events=funding_events,
            canonical_hash="",
            reason_code=reason_code,
            accepted=False,
        )

    @staticmethod
    def _conflict_evidence_diffs(
        components: Sequence[ComponentEvidence],
    ) -> tuple[ReconcileDiffRecord, ...]:
        """Persist both normalized observations for any broker identity conflict."""
        records: list[ReconcileDiffRecord] = []
        for component in components:
            if component.status is not ReconcileComponentStatus.CONFLICTING:
                continue
            kind = (
                ReconcileDiffKind.FUNDING
                if component.kind is ReconcileComponentKind.FUNDING
                else ReconcileDiffKind.ORDER
            )
            records.append(
                ReconcileDiffRecord(
                    kind=kind,
                    subject=component.kind.value,
                    reason_code=DIFF_EXCHANGE_IDENTITY_CONFLICT,
                    ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                    blocking=True,
                    exchange={
                        "observations": component.canonical_rows(),
                        "observation_digests": [
                            reconcile_digest(dict(row))
                            for row in component.canonical_rows()
                        ],
                    },
                )
            )
        return tuple(records)

    def _funding_records_if_valid(
        self, components: Sequence[ComponentEvidence]
    ) -> tuple[
        tuple[FundingEventRecord, ...], tuple[ReconcileDiffRecord, ...]
    ]:
        for component in components:
            if component.kind is ReconcileComponentKind.FUNDING and component.accepted:
                records, diffs = self._funding_records(component)
                return records, tuple(diffs)
        return (), ()

    # ------------------------------------------------------------------
    # deterministic diff
    # ------------------------------------------------------------------

    def _build_diff(
        self, components: Mapping[ReconcileComponentKind, ComponentEvidence]
    ) -> tuple[tuple[ReconcileDiffRecord, ...], tuple[FundingEventRecord, ...]]:
        diffs: list[ReconcileDiffRecord] = []
        local_orders = {
            str(row["cloid"]): row for row in self.store.live_local_orders()
        }
        diffs.extend(
            self._order_diffs(
                components[ReconcileComponentKind.OPEN_ORDERS], local_orders
            )
        )
        diffs.extend(self._fill_diffs(components[ReconcileComponentKind.FILLS]))
        diffs.extend(
            self._position_diffs(components[ReconcileComponentKind.POSITIONS])
        )
        diffs.extend(
            self._account_diffs(
                components[ReconcileComponentKind.BALANCES],
                components[ReconcileComponentKind.MARGIN],
            )
        )
        funding_records, funding_diffs = self._funding_records(
            components[ReconcileComponentKind.FUNDING]
        )
        diffs.extend(funding_diffs)
        diffs.extend(
            self._pending_action_diffs(
                components[ReconcileComponentKind.PENDING_ACTIONS]
            )
        )
        diffs.extend(self._unknown_local_status_diffs())
        ordered = tuple(
            sorted(
                diffs,
                key=lambda diff: (
                    diff.kind.value,
                    diff.subject,
                    diff.reason_code,
                    diff.ownership.value,
                ),
            )
        )
        return ordered, funding_records

    def _fill_diffs(
        self, component: ComponentEvidence
    ) -> list[ReconcileDiffRecord]:
        """Bind every fill to one durable broker order identity, fail closed otherwise."""
        diffs: list[ReconcileDiffRecord] = []
        cumulative_by_oid: dict[int, float] = {}
        observed_fill_ids: set[str] = set()
        for index, raw in enumerate(component.canonical_rows()):
            oid = raw.get("oid")
            subject = str(raw.get("event_id") or raw.get("fill_id") or f"row:{index}")
            if isinstance(oid, bool) or not isinstance(oid, int):
                order = None
            else:
                order = self.store.get_order_by_oid(oid)
            if order is None:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=subject,
                        reason_code=DIFF_UNKNOWN_OWNERSHIP_ORDER,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        exchange=raw,
                    )
                )
                continue
            observed_fill_ids.add(subject)
            try:
                fill_size = float(raw["size"])
                ordered_size = float(order["qty"])
            except (KeyError, TypeError, ValueError):
                fill_size = -1.0
                ordered_size = 0.0
            cumulative_by_oid[oid] = cumulative_by_oid.get(oid, 0.0) + fill_size
            try:
                order_payload = json.loads(str(order.get("order_json") or "{}"))
            except (TypeError, ValueError, json.JSONDecodeError):
                order_payload = {}
            expected_symbol = str(order_payload.get("symbol") or "")
            observed_symbol = str(raw.get("coin") or "")
            observed_side = str(raw.get("side") or "").upper()
            observed_side = {"A": "SELL", "B": "BUY"}.get(
                observed_side, observed_side
            )
            trade = (
                self.store.get_trade(int(order["trade_id"]))
                if order.get("trade_id") is not None
                else None
            )
            direction = str((trade or {}).get("direction") or "").upper()
            role = str(order.get("role") or "").upper()
            expected_side = None
            if direction in {"LONG", "SHORT"}:
                is_entry = role == "ENTRY"
                expected_side = (
                    "BUY"
                    if (direction == "LONG") == is_entry
                    else "SELL"
                )
            lot = self.broker.lot_unit(observed_symbol) if observed_symbol else None
            try:
                if lot is not None:
                    quantize_lots(fill_size, lot)
                    quantize_lots(ordered_size, lot)
            except LotQuantizationError:
                lot_valid = False
            else:
                lot_valid = lot is not None
            if (
                fill_size <= 0
                or ordered_size <= 0
                or cumulative_by_oid[oid] > ordered_size
                or not expected_symbol
                or observed_symbol != expected_symbol
                or expected_side is None
                or observed_side != expected_side
                or not lot_valid
            ):
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=subject,
                        reason_code=DIFF_EXCHANGE_IDENTITY_CONFLICT,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local={
                            "oid": oid,
                            "qty": ordered_size,
                            "symbol": expected_symbol,
                            "side": expected_side,
                        },
                        exchange=raw,
                    )
                )
                continue
            local_fills = {
                str(item["fill_id"]): item
                for item in self.store.list_fills_for_order(str(order["cloid"]))
            }
            local_fill = local_fills.get(subject)
            try:
                local_ts = (
                    datetime.fromisoformat(str(local_fill["fill_ts"]))
                    if local_fill is not None
                    else None
                )
                if local_ts is not None and local_ts.tzinfo is None:
                    local_ts = local_ts.replace(tzinfo=UTC)
                local_ts_ms = (
                    int(local_ts.astimezone(UTC).timestamp() * 1000)
                    if local_ts is not None
                    else None
                )
                local_matches = (
                    local_fill is not None
                    and float(local_fill["qty"]) == fill_size
                    and float(local_fill["px"]) == float(raw["px"])
                    and local_ts_ms == int(raw["effective_ts_ms"])
                )
            except (KeyError, TypeError, ValueError, OverflowError):
                local_matches = False
            if not local_matches:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=subject,
                        reason_code=DIFF_EXCHANGE_IDENTITY_CONFLICT,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local=local_fill,
                        exchange=raw,
                    )
                )
        if component.cursor_start_ms is not None and component.cursor_end_ms is not None:
            for local_fill in self.store.list_all_fills():
                try:
                    fill_ts = datetime.fromisoformat(str(local_fill["fill_ts"]))
                    if fill_ts.tzinfo is None:
                        fill_ts = fill_ts.replace(tzinfo=UTC)
                    fill_ts_ms = int(fill_ts.astimezone(UTC).timestamp() * 1000)
                except (TypeError, ValueError, OverflowError):
                    fill_ts_ms = component.cursor_start_ms
                fill_id = str(local_fill["fill_id"])
                if (
                    component.cursor_start_ms <= fill_ts_ms <= component.cursor_end_ms
                    and fill_id not in observed_fill_ids
                ):
                    diffs.append(
                        ReconcileDiffRecord(
                            kind=ReconcileDiffKind.ORDER,
                            subject=fill_id,
                            reason_code=DIFF_EXCHANGE_IDENTITY_CONFLICT,
                            ownership=ReconcileOwnership.OWNED,
                            blocking=True,
                            local=local_fill,
                        )
                    )
        return diffs

    def _order_diffs(
        self,
        component: ComponentEvidence,
        local_orders: Mapping[str, Mapping[str, Any]],
    ) -> list[ReconcileDiffRecord]:
        diffs: list[ReconcileDiffRecord] = []
        exchange: dict[str, dict[str, Any]] = {}
        for index, raw in enumerate(component.canonical_rows()):
            cloid = raw.get("cloid")
            if not isinstance(cloid, str) or not cloid.strip():
                # No complete identity → not provably foreign (D1=B).
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=f"row:{index}",
                        reason_code=DIFF_UNKNOWN_OWNERSHIP_ORDER,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        exchange=raw,
                    )
                )
                continue
            previous = exchange.get(cloid)
            if previous is not None and previous != raw:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_EXCHANGE_IDENTITY_CONFLICT,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        local=previous,
                        exchange=raw,
                    )
                )
                continue
            exchange[cloid] = raw

        for cloid in sorted(local_orders):
            local = local_orders[cloid]
            observed = exchange.get(cloid)
            symbol = str(local.get("symbol") or "")
            if local.get("trade_id") is None or not symbol:
                # A durable owned cloid without usable lineage cannot be
                # classified against exchange evidence at all.
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_ORPHAN_OWNED_CLOID,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local=self._local_order_payload(local),
                        exchange=observed,
                    )
                )
                continue
            if observed is None:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_OWNED_ORDER_MISSING,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local=self._local_order_payload(local),
                    )
                )
                continue
            trade = (
                self.store.get_trade(int(local["trade_id"]))
                if local.get("trade_id") is not None
                else None
            )
            direction = str((trade or {}).get("direction") or "").upper()
            role = str(local.get("role") or "").upper()
            expected_side = None
            if direction in {"LONG", "SHORT"}:
                expected_side = (
                    "BUY"
                    if (direction == "LONG") == (role == "ENTRY")
                    else "SELL"
                )
            observed_side = {"A": "SELL", "B": "BUY"}.get(
                str(observed.get("side") or "").upper(),
                str(observed.get("side") or "").upper(),
            )
            expected_reduce_only = role != "ENTRY"
            identity_mismatch = (
                str(observed.get("coin") or "") != symbol
                or observed.get("oid") != local.get("oid")
                or str(observed.get("role") or "").upper() not in {role, "UNKNOWN"}
                or observed_side != expected_side
                or observed.get("reduce_only") is not expected_reduce_only
            )
            if identity_mismatch:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_EXCHANGE_IDENTITY_CONFLICT,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local={
                            **self._local_order_payload(local),
                            "oid": local.get("oid"),
                            "side": expected_side,
                            "reduce_only": expected_reduce_only,
                        },
                        exchange=observed,
                    )
                )
                continue
            lot = self.broker.lot_unit(symbol) if symbol else None
            if lot is None:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_OWNED_ORDER_UNKNOWN_QUANTUM,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local=self._local_order_payload(local),
                        exchange=observed,
                    )
                )
                continue
            try:
                local_lots = quantize_lots(abs(float(local["qty"])), lot)
                exchange_lots = quantize_lots(abs(float(observed.get("size", 0))), lot)
            except (LotQuantizationError, KeyError, TypeError, ValueError):
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_OWNED_ORDER_UNKNOWN_QUANTUM,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local=self._local_order_payload(local),
                        exchange=observed,
                    )
                )
                continue
            if local_lots != exchange_lots:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_OWNED_ORDER_QTY_MISMATCH,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local={"lots": local_lots},
                        exchange={"lots": exchange_lots},
                    )
                )
                continue
            if self._status_conflict(local, observed):
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_OWNED_ORDER_STATUS_MISMATCH,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local={"status": str(local.get("status"))},
                        exchange={"status": str(observed.get("status"))},
                    )
                )

        for cloid in sorted(set(exchange) - set(local_orders)):
            observed = exchange[cloid]
            if self.store.get_order(cloid) is not None:
                # Live on the exchange but terminal in durable local intent.
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_OWNED_ORDER_STATUS_MISMATCH,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local={"status": "TERMINAL_OR_ABSENT"},
                        exchange=observed,
                    )
                )
                continue
            foreign_complete = (
                isinstance(observed.get("oid"), int)
                and not isinstance(observed.get("oid"), bool)
                and isinstance(observed.get("coin"), str)
                and bool(str(observed.get("coin")).strip())
                and str(observed.get("side") or "").upper()
                in {"A", "B", "BUY", "SELL"}
                and _finite(observed.get("size")) is not None
                and float(observed.get("size")) > 0
                and isinstance(observed.get("reduce_only"), bool)
            )
            if not foreign_complete:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.ORDER,
                        subject=cloid,
                        reason_code=DIFF_UNKNOWN_OWNERSHIP_ORDER,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        exchange=observed,
                    )
                )
                continue
            # D1=B: a complete, non-owned order identity is observe-only.
            diffs.append(
                ReconcileDiffRecord(
                    kind=ReconcileDiffKind.ORDER,
                    subject=cloid,
                    reason_code=DIFF_FOREIGN_ORDER_OBSERVED,
                    ownership=ReconcileOwnership.FOREIGN_IDENTIFIED,
                    blocking=False,
                    exchange=observed,
                )
            )
        return diffs

    def _unknown_local_status_diffs(self) -> list[ReconcileDiffRecord]:
        """A durable order status outside the closed space is never dropped.

        ``live_local_orders()`` answers "provably still live"; such a row is
        neither provably live nor provably terminal, so it cannot be silently
        excluded from the comparison — it blocks until the status vocabulary
        or the row is reconciled by an owner.
        """
        return [
            ReconcileDiffRecord(
                kind=ReconcileDiffKind.ORDER,
                subject=str(row.get("cloid") or "unknown"),
                reason_code=DIFF_LOCAL_ORDER_STATUS_UNKNOWN,
                ownership=ReconcileOwnership.OWNED,
                blocking=True,
                local=self._local_order_payload(row),
            )
            for row in self.store.local_orders_with_unknown_status()
        ]

    @staticmethod
    def _local_order_payload(local: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "status": str(local.get("status")),
            "qty": _finite(local.get("qty")),
            "filled_qty": _finite(local.get("filled_qty")),
            "symbol": str(local.get("symbol") or ""),
            "role": str(local.get("role") or ""),
        }

    @staticmethod
    def _status_conflict(
        local: Mapping[str, Any], observed: Mapping[str, Any]
    ) -> bool:
        try:
            exchange_state = normalize_raw_order_status(observed.get("status"))
        except Exception:  # noqa: BLE001 - unknown spelling is itself a conflict
            return True
        return exchange_state in TERMINAL_ORDER_STATES

    def _position_diffs(
        self, component: ComponentEvidence
    ) -> list[ReconcileDiffRecord]:
        diffs: list[ReconcileDiffRecord] = []
        expected = self._expected_position_lots()
        observed: dict[str, float] = {}
        for row in component.canonical_rows():
            symbol = str(row.get("symbol") or "")
            size = _finite(row.get("size"))
            if not symbol or size is None:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.POSITION,
                        subject=symbol or "unknown",
                        reason_code=DIFF_UNKNOWN_OWNERSHIP_POSITION,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        exchange=row,
                    )
                )
                continue
            observed[symbol] = observed.get(symbol, 0.0) + size

        for symbol in sorted(set(observed) | set(expected)):
            size = observed.get(symbol, 0.0)
            lot = self.broker.lot_unit(symbol)
            if lot is None:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.POSITION,
                        subject=symbol,
                        reason_code=DIFF_POSITION_UNKNOWN_QUANTUM,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        exchange={"size": size},
                    )
                )
                continue
            try:
                observed_lots = quantize_lots(abs(size), lot)
                observed_lots = observed_lots if size >= 0 else -observed_lots
                expected_lots = expected.get(symbol)
                expected_lots = (
                    None
                    if expected_lots is None
                    else self._signed_lots(expected_lots, lot)
                )
            except LotQuantizationError:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.POSITION,
                        subject=symbol,
                        reason_code=DIFF_POSITION_UNKNOWN_QUANTUM,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        exchange={"size": size},
                    )
                )
                continue
            if expected_lots is None:
                if observed_lots != 0:
                    # An exchange position with no owned-order lineage has
                    # UNKNOWN ownership — never "safely foreign" (D1=B).
                    diffs.append(
                        ReconcileDiffRecord(
                            kind=ReconcileDiffKind.POSITION,
                            subject=symbol,
                            reason_code=DIFF_UNKNOWN_OWNERSHIP_POSITION,
                            ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                            blocking=True,
                            exchange={"lots": observed_lots},
                        )
                    )
                continue
            if observed_lots != expected_lots:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.POSITION,
                        subject=symbol,
                        reason_code=DIFF_POSITION_QTY_MISMATCH,
                        ownership=ReconcileOwnership.OWNED,
                        blocking=True,
                        local={"lots": expected_lots},
                        exchange={"lots": observed_lots},
                    )
                )
        return diffs

    @staticmethod
    def _signed_lots(value: float, lot: Any) -> int:
        lots = quantize_lots(abs(value), lot)
        return lots if value >= 0 else -lots

    def _expected_position_lots(self) -> dict[str, float]:
        """Net signed exposure implied by durable local fills, per symbol.

        Entries add in the trade's direction; protective/close roles reduce it.
        A symbol appears here only when owned-order lineage exists, which is
        exactly the attribution D1=B requires before a position can be
        classified at all.
        """
        expected: dict[str, float] = {}
        for row in self.store.live_local_orders() + self._terminal_filled_orders():
            symbol = str(row.get("symbol") or "")
            filled = _finite(row.get("filled_qty")) or 0.0
            if not symbol:
                continue
            expected.setdefault(symbol, 0.0)
            if filled == 0.0:
                continue
            trade_id = row.get("trade_id")
            if trade_id is None:
                continue
            trade = self.store.get_trade(int(trade_id))
            if trade is None:
                continue
            sign = _sign(str(trade.get("direction") or "LONG"))
            role = str(row.get("role") or "").upper()
            if role == "ENTRY":
                expected[symbol] += sign * filled
            else:
                expected[symbol] -= sign * filled
        return expected

    def _terminal_filled_orders(self) -> list[dict[str, Any]]:
        rows = self.store._rows(
            "SELECT * FROM orders WHERE filled_qty > 0 ORDER BY cloid"
        )
        live = {str(row["cloid"]) for row in self.store.live_local_orders()}
        resolved: list[dict[str, Any]] = []
        for row in rows:
            if str(row["cloid"]) in live:
                continue
            try:
                row["symbol"] = str(json.loads(row["order_json"]).get("symbol") or "")
            except (TypeError, ValueError):
                row["symbol"] = ""
            resolved.append(row)
        return resolved

    def _account_diffs(
        self, balances: ComponentEvidence, margin: ComponentEvidence
    ) -> list[ReconcileDiffRecord]:
        payload: dict[str, Any] = {}
        for component in (balances, margin):
            for row in component.canonical_rows():
                payload.update(row)
        equity = _finite(payload.get("equity"))
        withdrawable = _finite(payload.get("withdrawable"))
        margin_used = _finite(payload.get("margin_used"))
        available = _finite(payload.get("available_margin"))
        problems: list[str] = []
        if None in (equity, withdrawable, margin_used, available):
            problems.append("NON_FINITE")
        else:
            if min(equity, withdrawable, margin_used, available) < 0:
                problems.append("NEGATIVE")
            if withdrawable > equity or margin_used > equity:
                problems.append("EXCEEDS_EQUITY")
            if not math.isclose(
                available, equity - margin_used, rel_tol=0.0,
                abs_tol=ACCOUNT_IDENTITY_ABS_TOL,
            ):
                problems.append("IDENTITY")
        if not problems:
            return []
        return [
            ReconcileDiffRecord(
                kind=ReconcileDiffKind.ACCOUNT,
                subject="ACCOUNT",
                reason_code=DIFF_ACCOUNT_INCONSISTENT,
                ownership=ReconcileOwnership.OWNED,
                blocking=True,
                exchange={
                    "equity": equity,
                    "withdrawable": withdrawable,
                    "margin_used": margin_used,
                    "available_margin": available,
                    "problems": sorted(problems),
                },
            )
        ]

    def _funding_records(
        self, component: ComponentEvidence
    ) -> tuple[tuple[FundingEventRecord, ...], list[ReconcileDiffRecord]]:
        """Signed funding ledger with D3=A attribution; identities never made up."""
        known_symbols = self._owned_symbols()
        records: list[FundingEventRecord] = []
        diffs: list[ReconcileDiffRecord] = []
        for row in component.canonical_rows():
            event_id = row.get("event_id")
            symbol = str(row.get("symbol") or "")
            amount = _finite(row.get("amount_usdc"))
            ts_ms = row.get("effective_ts_ms")
            if (
                not isinstance(event_id, str)
                or not event_id.strip()
                or not symbol
                or amount is None
                or not isinstance(ts_ms, int)
                or isinstance(ts_ms, bool)
            ):
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.FUNDING,
                        subject=str(event_id or "unknown"),
                        reason_code=DIFF_FUNDING_UNATTRIBUTED,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        exchange=row,
                    )
                )
                continue
            attribution = (
                FundingAttribution.ATTRIBUTED
                if symbol in known_symbols
                else FundingAttribution.UNATTRIBUTED
            )
            record = FundingEventRecord(
                event_id=event_id,
                symbol=symbol,
                amount_usdc=amount,
                effective_ts=datetime.fromtimestamp(ts_ms / 1000, tz=UTC),
                source=str(row.get("source") or "HL_USER_FUNDING"),
                attribution=attribution,
                funding_rate=_finite(row.get("funding_rate")),
                position_szi=_finite(row.get("position_szi")),
                n_samples=(
                    int(row["n_samples"])
                    if isinstance(row.get("n_samples"), int)
                    and not isinstance(row.get("n_samples"), bool)
                    else None
                ),
            )
            existing = self.store.get_funding_event(event_id)
            if existing is not None and str(existing["payload_digest"]) != record.digest:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.FUNDING,
                        subject=event_id,
                        reason_code=DIFF_EXCHANGE_IDENTITY_CONFLICT,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        local={
                            "event_id": existing["event_id"],
                            "symbol": existing["symbol"],
                            "amount_usdc": existing["amount_usdc"],
                            "effective_ts": existing["effective_ts"],
                            "source": existing["source"],
                            "payload_digest": existing["payload_digest"],
                        },
                        exchange={
                            **record.authoritative(),
                            "payload_digest": record.digest,
                        },
                    )
                )
                continue
            records.append(record)
            if attribution is FundingAttribution.UNATTRIBUTED:
                diffs.append(
                    ReconcileDiffRecord(
                        kind=ReconcileDiffKind.FUNDING,
                        subject=event_id,
                        reason_code=DIFF_FUNDING_UNATTRIBUTED,
                        ownership=ReconcileOwnership.UNKNOWN_OWNERSHIP,
                        blocking=True,
                        exchange={"symbol": symbol, "amount_usdc": amount},
                    )
                )
        return tuple(records), diffs

    def _owned_symbols(self) -> set[str]:
        symbols = {
            str(row.get("symbol") or "") for row in self.store.live_local_orders()
        }
        symbols |= {
            str(row.get("symbol") or "") for row in self._terminal_filled_orders()
        }
        symbols.discard("")
        return symbols

    def _pending_action_diffs(
        self, component: ComponentEvidence
    ) -> list[ReconcileDiffRecord]:
        diffs: list[ReconcileDiffRecord] = []
        for row in component.canonical_rows():
            # TS-P1-003 quarantine and TS-P1-004 recovery keep their own
            # authority: reconciliation only observes and blocks on them.
            diffs.append(
                ReconcileDiffRecord(
                    kind=ReconcileDiffKind.PENDING_ACTION,
                    subject=str(row.get("id") or "unknown"),
                    reason_code=DIFF_PENDING_ACTION_DIVERGENCE,
                    ownership=ReconcileOwnership.OWNED,
                    blocking=True,
                    local=row,
                )
            )
        return diffs
