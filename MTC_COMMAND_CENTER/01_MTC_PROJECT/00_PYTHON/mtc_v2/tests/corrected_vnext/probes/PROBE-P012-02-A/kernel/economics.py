"""Version-selected execution economics for one atomic state transition.

The public seam is :meth:`ExecutionEconomics.resolve`.  It is deliberately
pure: callers provide immutable facts and receive an immutable
``EconomicTransition``.  Only the caller may apply the returned cash ledger or
position facts.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import base64
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any, Mapping

from mtc_v2.core.instrument import (
    InstrumentMetadata,
    InstrumentRecord,
    load_verified_instrument_record,
    load_verified_json_record,
)
from mtc_v2.core.semantics import resolve_semantics_id
from mtc_v2.core.types import (
    CashEvent,
    CashEventKind,
    DecisionEvent,
    EconomicTransition,
    FeeEvent,
    FillDecision,
    FundingEvent,
    FundingEventKey,
    PositionFacts,
)


REFUSED_ECONOMIC_INPUT = "REFUSED_ECONOMIC_INPUT"
REFUSED_MISSING_COST_SCHEDULE = "REFUSED_MISSING_COST_SCHEDULE"
REFUSED_MISSING_FUNDING_EVENT = "REFUSED_MISSING_FUNDING_EVENT"
REFUSED_UNSUPPORTED_COLLISION_POLICY = "REFUSED_UNSUPPORTED_COLLISION_POLICY"
REFUSED_AMBIGUOUS_SAME_BAR = "REFUSED_AMBIGUOUS_SAME_BAR"
REFUSED_DUPLICATE_FUNDING_EVENT = "REFUSED_DUPLICATE_FUNDING_EVENT"
REFUSED_UNMAPPED_FILL_EVENT_CLASS = "REFUSED_UNMAPPED_FILL_EVENT_CLASS"
REFUSED_MISSING_ADMITTED_FEE = "REFUSED_MISSING_ADMITTED_FEE"
REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE = "REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE"
REFUSED_UNSPECIFIED_ADMITTED_INTERVAL_START = (
    "REFUSED_UNSPECIFIED_ADMITTED_INTERVAL_START"
)
REFUSED_BEFORE_ADMITTED_INTERVAL_START = "REFUSED_BEFORE_ADMITTED_INTERVAL_START"
REFUSED_UNSPECIFIED_ADMITTED_ACCOUNT_PRODUCT = (
    "REFUSED_UNSPECIFIED_ADMITTED_ACCOUNT_PRODUCT"
)
REFUSED_UNAUTHENTICATED_REPORTED_FEE = "REFUSED_UNAUTHENTICATED_REPORTED_FEE"
REFUSED_UNSUPPORTED_REPORTED_FEE_REPRESENTATION = (
    "REFUSED_UNSUPPORTED_REPORTED_FEE_REPRESENTATION"
)

# --- OD-20260912-P012-PATHD-1 decision B (fees) ---------------------------
# B1=C: the venue's own reported per-fill fee is the admitted cash amount; the
# pinned schedule survives only as a guarded pre-trade estimator.
ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1 = "HL_FEE_REPORTED_PER_FILL_V1"
ADMITTED_COST_SOURCES = (ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1,)
GUARDED_ESTIMATOR_SCHEDULE_ID = "HL_FEE_SCHEDULE_ESTIMATOR_GUARDED_V1"
# B2=C, owner-signed: 5% of the estimate, relative only.  The `max(5%, 1e-6
# USDC)` variant offered by the packet was NOT adopted: it strictly weakens
# detection near zero (estimate 1e-6, reported 1.9e-6 deviates by 90% of the
# estimate yet 9e-7 <= 1e-6, so the floor form would admit it silently), and the
# owner decision allows the floor only on a showing that it never weakens
# detection.  See test_pathd_fees.py::test_absolute_tolerance_floor_would_weaken_detection.
ESTIMATOR_TOLERANCE_RELATIVE = 0.05
ESTIMATOR_TOLERANCE_FORM = "RELATIVE_FRACTION_OF_ESTIMATE_V1"
FEE_ESTIMATOR_SUSPENDED = "FEE_ESTIMATOR_SUSPENDED"
FEE_ESTIMATOR_AGREED = "FEE_ESTIMATOR_AGREED"
ADMITTED_COST_APPLIED = "ADMITTED_COST_APPLIED"
ESTIMATOR_DEVIATION_SIGNED_RISK_ID = "PATHD-RISK-FEE-ESTIMATOR-DEVIATION-V1"
REPORTED_FEE_CHARGE = "CHARGE"
REPORTED_FEE_REBATE = "REBATE"
# The fixed component's evidence is unresolved: it is one of the cost record's
# ``refused_missing_fields``, and the admitted amount is read from the venue
# rather than computed, so no fixed component is applied and none is invented.
# The admitted path therefore carries *no* fixed-component value and says so
# with this explicit marker instead of a number a consumer could read as a
# fact.  ``0.0`` would be exactly such an invented fact.
FIXED_COMPONENT_UNRESOLVED = "UNRESOLVED_NOT_APPLIED"
_LOWER_SHA256_HEX = re.compile(r"\A[0-9a-f]{64}\Z")


class EconomicsRefusal(ValueError):
    """Closed refusal raised before an invalid transition can be returned."""

    def __init__(self, refusal_code: str, detail: str) -> None:
        self.refusal_code = refusal_code
        self.detail = detail
        super().__init__(f"{refusal_code}: {detail}")


class IntentKind(str, Enum):
    OPEN = "OPEN"
    PROTECTIVE_STOP = "PROTECTIVE_STOP"
    TARGET = "TARGET"
    MARKET_EXIT = "MARKET_EXIT"
    FUNDING_TICK = "FUNDING_TICK"


@dataclass(frozen=True, slots=True)
class ExitCandidate:
    exit_id: str
    kind: IntentKind
    price: float
    quantity_fraction: float = 1.0


@dataclass(frozen=True, slots=True)
class ReportedFillFee:
    """One claimed venue-reported fee with local consistency evidence.

    This is the *only* admitted cost input under
    :data:`ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1`.  On admission,
    ``reported_amount`` is the exact captured fee string in ``fee_token``.  It
    is read, never recomputed, never rounded and never replaced by an estimate.
    There is no default: a fill with no reported fee is refused, never treated
    as zero.

    ``closed_pnl`` is an optional exact-string assertion.  A captured value is
    carried beside the fee and never merged into the fee amount; an absent
    captured value remains explicitly unknown and is never defaulted to zero.

    The remaining fields are required local consistency inputs for admission.
    They are rechecked on every admitted runtime path; there is no
    caller-forgeable verified shortcut:

    ``source_class``
        must be exactly :data:`ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1`.  A
        number carrying any other class, or none, is not an admitted cost.
    ``account_scope`` / ``product``
        caller-declared account and product associations.  They must equal the
        cost record's declarations; neither is claimed to be a native capture
        field or proof of account ownership.
    ``capture_sha256``
        lower-case SHA-256 over ``capture_bytes`` exactly as supplied.
    ``capture_bytes``
        immutable original bytes for one JSON fill object.  The bounded local
        parser interprets only already-known fields and retains every byte;
        extra native members are not rejected or silently reconstructed.
    ``native_fill_id`` / ``native_instrument``
        caller-declared associations checked against identity and coin derived
        from the capture.  ``fill_id`` remains the separate internal MTC fill
        association.

    They all default to ``None`` on purpose: a bare object still constructs, so
    the refusal a caller gets is the typed
    :data:`REFUSED_UNAUTHENTICATED_REPORTED_FEE`, not a ``TypeError``.

    Limitation, stated rather than hidden: byte/content consistency does not
    authenticate venue origin, account ownership, completeness, or production
    permission.  A caller can forge an internally consistent object.  The
    independent external authentication and admission gate remains required.
    """

    fill_id: str
    reported_amount: str
    fee_token: str
    fee_class: str = REPORTED_FEE_CHARGE
    closed_pnl: str | None = None
    source_class: str | None = None
    account_scope: str | None = None
    product: str | None = None
    capture_sha256: str | None = None
    capture_bytes: bytes | None = None
    native_fill_id: str | None = None
    native_instrument: str | None = None


@dataclass(frozen=True, slots=True)
class _CapturedReportedFee:
    amount: float
    amount_raw: str
    closed_pnl: float | None
    closed_pnl_raw: str | None
    native_fill_id: str
    native_instrument: str
    native_time_ms: int
    native_hash: str | None
    native_oid: int | None
    native_tid: int | None
    capture_bytes_base64: str


@dataclass(frozen=True, slots=True)
class EconomicIntent:
    kind: IntentKind
    action_side: str | None = None
    position_side: str | None = None
    reference_price: float | None = None
    requested_quantity: float | None = None
    stop_price: float | None = None
    stop_percent: float | None = None
    stop_distance: float | None = None
    risk_pct: float = 0.0
    fallback_size_pct: float = 0.0
    max_leverage_cap: float = 1.0
    event_class: str | None = None
    reason: str | None = None
    exit_id: str | None = None
    exit_candidates: tuple[ExitCandidate, ...] = ()
    same_bar_collision_policy_id: str | None = "STOP_FIRST"
    funding_event_id: str | None = None
    funding_event_in_window: bool = True
    # Venue-reported fees keyed by the fill they belong to.  Consumed only by
    # the admitted-cost path; ignored by records without an admitted cost
    # source, whose behaviour is unchanged.
    reported_fill_fees: tuple[ReportedFillFee, ...] = ()


@dataclass(frozen=True, slots=True)
class MarketEvent:
    timestamp: datetime
    bar_index: int
    open: float
    high: float
    low: float
    close: float
    execution_profile_id: str = "close_only_deterministic_v2"


@dataclass(frozen=True, slots=True)
class EconomicState:
    lifecycle_id: int | None = None
    position_side: str | None = None
    quantity: float = 0.0
    entry_fill_price: float | None = None
    sizing_equity: float = 0.0
    equity: float = 0.0
    cumulative_funding: float = 0.0
    applied_funding_event_keys: frozenset[FundingEventKey] = frozenset()
    next_lifecycle_id: int = 1
    next_decision_sequence: int = 0
    next_fill_sequence: int = 0
    next_cash_sequence: int = 0
    next_fee_sequence: int = 0
    next_funding_sequence: int = 0


@dataclass(frozen=True, slots=True)
class EconomicRecords:
    instrument: InstrumentRecord
    cost: Mapping[str, Any] | None
    cost_digest: str | None
    funding: Mapping[str, Any]
    funding_digest: str
    runtime_instrument_config: Mapping[str, object] | None = None

    @classmethod
    def from_record_paths(
        cls,
        *,
        instrument_path: str | Path,
        funding_path: str | Path,
        cost_path: str | Path | None = None,
        runtime_instrument_config: Mapping[str, object] | None = None,
    ) -> "EconomicRecords":
        instrument = load_verified_instrument_record(instrument_path)
        funding = load_verified_json_record(funding_path)
        cost = load_verified_json_record(cost_path) if cost_path is not None else None
        return cls(
            instrument=instrument,
            cost=None if cost is None else cost.data,
            cost_digest=None if cost is None else cost.digest,
            funding=funding.data,
            funding_digest=funding.digest,
            runtime_instrument_config=runtime_instrument_config,
        )

    @property
    def cost_schedule_id(self) -> str | None:
        if self.cost is None:
            return None
        return str(self.cost["schedule_id"])

    @property
    def funding_schedule_id(self) -> str:
        return str(self.funding["schedule_id"])


class ExecutionEconomics(ABC):
    """Pure version-specific resolver for economic intents."""

    semantics_id: str

    @abstractmethod
    def resolve(
        self,
        state: EconomicState,
        intent: EconomicIntent,
        market_event: MarketEvent,
        records: EconomicRecords,
    ) -> EconomicTransition:
        """Resolve one intent without mutating any argument."""


def _details(**values: object) -> tuple[tuple[str, object], ...]:
    return tuple(values.items())


def _position_facts(
    *,
    lifecycle_id: int | None,
    side: str | None,
    quantity: float,
    entry_fill_price: float | None,
    active_stop_price: float | None = None,
) -> PositionFacts:
    return PositionFacts(
        lifecycle_id=lifecycle_id,
        side=side,
        quantity=quantity,
        entry_fill_price=entry_fill_price,
        active_stop_price=active_stop_price,
    )


def _empty_transition(
    *,
    semantics_id: str,
    state: EconomicState,
    records: EconomicRecords,
    decisions: tuple[DecisionEvent, ...] = (),
) -> EconomicTransition:
    return EconomicTransition(
        semantics_id=semantics_id,
        instrument_record_id=records.instrument.record_id,
        instrument_record_digest=records.instrument.digest,
        cost_schedule_id=records.cost_schedule_id,
        cost_schedule_digest=records.cost_digest,
        funding_schedule_id=records.funding_schedule_id,
        funding_schedule_digest=records.funding_digest,
        next_position_facts=_position_facts(
            lifecycle_id=state.lifecycle_id,
            side=state.position_side,
            quantity=state.quantity,
            entry_fill_price=state.entry_fill_price,
        ),
        decision_events=decisions,
    )


def _size_quantity(
    *,
    corrected: bool,
    entry: float,
    stop: float | None,
    equity: float,
    risk_pct: float,
    fallback_size_pct: float,
    max_leverage_cap: float,
    instrument: InstrumentMetadata,
) -> float:
    if not math.isfinite(entry) or entry <= 0.0:
        return 0.0
    if not math.isfinite(equity) or equity <= 0.0:
        return 0.0
    multiplier = instrument.contract_multiplier if corrected else 1.0
    if stop is not None and math.isfinite(stop):
        distance = abs(entry - stop)
        if distance <= 0.0:
            return 0.0
        raw = equity * (risk_pct / 100.0) / (distance * multiplier)
    else:
        raw = equity * (fallback_size_pct / 100.0) / (entry * multiplier)
    leverage_cap = equity * max_leverage_cap / (entry * instrument.contract_multiplier)
    raw = min(raw, leverage_cap)
    if not math.isfinite(raw) or raw <= 0.0:
        return 0.0
    quantity = instrument.floor_qty(raw)
    if quantity < instrument.min_qty:
        return 0.0
    if quantity * entry * instrument.contract_multiplier < instrument.min_notional:
        return 0.0
    return quantity


def _fill_price(
    *,
    reference: float,
    action_side: str,
    instrument: InstrumentMetadata,
    cost: Mapping[str, Any],
) -> tuple[float, float, float, str]:
    model = cost.get("slippage_model_id")
    if model != "BPS_OF_REFERENCE_V1":
        raise EconomicsRefusal(REFUSED_ECONOMIC_INPUT, f"unsupported slippage model {model!r}")
    bps = float(cost.get("slippage_parameters", {}).get("slippage_bps"))
    if not math.isfinite(bps) or bps < 0.0:
        raise EconomicsRefusal(REFUSED_ECONOMIC_INPUT, "slippage_bps must be finite and non-negative")
    impact = abs(reference) * bps / 10_000.0
    if action_side == "BUY":
        return instrument.ceil_price(reference + impact), bps, impact, "CEIL"
    if action_side == "SELL":
        return instrument.floor_price(reference - impact), bps, impact, "FLOOR"
    raise EconomicsRefusal(REFUSED_ECONOMIC_INPUT, f"unknown action side {action_side!r}")


@dataclass(frozen=True, slots=True)
class _PendingDecision:
    """A decision the fee path produced before its sequence number is known."""

    decision: str
    details: tuple[tuple[str, object], ...]
    refusal_code: str | None = None


def _parse_z_timestamp(value: object, field_name: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise EconomicsRefusal(
            REFUSED_ECONOMIC_INPUT, f"{field_name} must be an explicit Z timestamp"
        )
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise EconomicsRefusal(
            REFUSED_ECONOMIC_INPUT, f"{field_name} is not an ISO-8601 timestamp"
        ) from exc
    return parsed.astimezone(timezone.utc)


def _guard_admitted_event_class(cost: Mapping[str, Any] | None, event_class: str) -> None:
    """Refuse an unmapped/refused fill class *before* any row is built.

    Applies only to records declaring an admitted cost source, so the frozen
    schedule path keeps its exact behaviour.  ``MARGIN_CALL_LIQUIDATION`` stays
    refused with the record's own ``CANNOT_MAP...`` disposition: admitting a
    reported fee never turns the liquidation class into a mapped one.
    """
    if cost is None or cost.get("admitted_cost_source") is None:
        return
    refused = cost.get("refused_event_classes")
    if isinstance(refused, Mapping) and event_class in refused:
        raise EconomicsRefusal(
            REFUSED_UNMAPPED_FILL_EVENT_CLASS,
            f"{event_class} is refused by this schedule: {refused[event_class]}",
        )
    roles = cost.get("liquidity_roles")
    if not isinstance(roles, Mapping) or event_class not in roles:
        raise EconomicsRefusal(REFUSED_UNMAPPED_FILL_EVENT_CLASS, event_class)


def _declared_account_and_product(cost: Mapping[str, Any]) -> tuple[str, str]:
    """The record's declared own account and product, or a typed refusal.

    OD-20260912-P012-PATHD-1 leaves the account and product UNSPECIFIED until
    authenticated evidence exists.  A record that declares neither — by
    omitting the keys or by carrying an explicit ``null`` — cannot bind a
    reported fee to anything, so every admitted-cost computation under it
    refuses.  Nothing is defaulted, inferred or carried over from another
    record.
    """
    declared: list[str] = []
    for key in ("admitted_account", "admitted_product"):
        value = cost.get(key)
        if not isinstance(value, str) or not value.strip():
            raise EconomicsRefusal(
                REFUSED_UNSPECIFIED_ADMITTED_ACCOUNT_PRODUCT,
                f"{key} is UNSPECIFIED on this cost record; the admitted-cost "
                "path cannot bind a venue-reported fee to an own account and "
                "product until both are declared explicitly",
            )
        declared.append(value)
    return declared[0], declared[1]


def _fee_evidence_refusal(
    event_class: str,
    fill_id: str,
    detail: str,
) -> EconomicsRefusal:
    return EconomicsRefusal(
        REFUSED_UNAUTHENTICATED_REPORTED_FEE,
        f"{event_class}: reported fee for fill {fill_id} {detail}",
    )


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _reject_nonfinite_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant {value!r}")


def _captured_decimal_float(
    raw: object,
    *,
    label: str,
    event_class: str,
    fill_id: str,
) -> tuple[Decimal, float]:
    if not isinstance(raw, str) or not raw:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"has captured {label} that is not a non-empty raw string",
        )
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"has captured {label} {raw!r} that is not a decimal",
        ) from exc
    if not value.is_finite():
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"has captured {label} {raw!r} that is not finite",
        )
    projected = float(value)
    if not math.isfinite(projected) or Decimal(str(projected)) != value:
        raise EconomicsRefusal(
            REFUSED_UNSUPPORTED_REPORTED_FEE_REPRESENTATION,
            f"{event_class}: captured {label} raw value {raw!r} for fill "
            f"{fill_id} does not survive the existing float's canonical "
            "decimal round-trip; the raw value is retained and no rounded "
            "value or estimator substitute is admitted",
        )
    return value, projected


def _require_fee_evidence_consistency(
    *,
    reported: ReportedFillFee,
    cost: Mapping[str, Any],
    fill_id: str,
    event_class: str,
    declared_account: str,
    declared_product: str,
    settlement_currency: str,
    event_timestamp: datetime,
    evaluated_symbol: str,
    verified_venue: str | None,
    verified_product_type: str | None,
) -> _CapturedReportedFee:
    """Recheck exact local capture consistency on every admitted fee path.

    The bytes are one original JSON fill object.  This bounded local
    interpretation is not a claim about a complete venue envelope and does not
    authenticate origin: an internally consistent object can still be forged.
    """
    if reported.source_class != ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            "carries "
            f"source_class {reported.source_class!r}, not the admitted "
            f"{ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1!r}; an unclassed "
            "number is not supported local fill evidence",
        )
    if reported.account_scope != declared_account:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            "is scoped by the caller to "
            f"account {reported.account_scope!r}, not the declared "
            f"{declared_account!r}",
        )
    if reported.product != declared_product:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            "is scoped by the caller to "
            f"product {reported.product!r}, not the declared "
            f"{declared_product!r}",
        )

    capture = reported.capture_bytes
    if not isinstance(capture, bytes):
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"has no immutable capture bytes (got {type(capture).__name__})",
        )
    digest = reported.capture_sha256
    if not isinstance(digest, str) or _LOWER_SHA256_HEX.fullmatch(digest) is None:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            "carries "
            f"capture_sha256 {digest!r}; a lower-case SHA-256 hex digest of "
            "the exact capture bytes is required",
        )
    actual_digest = hashlib.sha256(capture).hexdigest()
    if actual_digest != digest:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"capture bytes do not hash to capture_sha256 {digest!r}",
        )

    try:
        capture_text = capture.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise _fee_evidence_refusal(
            event_class, fill_id, "capture bytes are not strict UTF-8"
        ) from exc
    try:
        native = json.loads(
            capture_text,
            object_pairs_hook=_reject_duplicate_json_keys,
            parse_constant=_reject_nonfinite_json_constant,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"capture bytes are not unambiguous JSON: {exc}",
        ) from exc
    if not isinstance(native, dict):
        raise _fee_evidence_refusal(
            event_class, fill_id, "capture JSON is not one single-fill object"
        )

    raw_time = native.get("time")
    if isinstance(raw_time, bool) or not isinstance(raw_time, int) or raw_time <= 0:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"capture time {raw_time!r} is not a positive integer millisecond value",
        )
    coin = native.get("coin")
    if not isinstance(coin, str) or not coin.strip():
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"capture native instrument coin {coin!r} is not a non-empty string",
        )

    raw_tid = native.get("tid")
    native_hash: str | None = None
    native_oid: int | None = None
    native_tid: int | None = None
    if "tid" in native:
        if isinstance(raw_tid, bool) or not isinstance(raw_tid, int):
            raise _fee_evidence_refusal(
                event_class,
                fill_id,
                f"capture tid {raw_tid!r} is not a non-boolean integer identity",
            )
        native_tid = raw_tid
        derived_native_fill_id = str(raw_tid)
    else:
        raw_hash = native.get("hash")
        raw_oid = native.get("oid")
        if (
            not isinstance(raw_hash, str)
            or not raw_hash.strip()
            or isinstance(raw_oid, bool)
            or not isinstance(raw_oid, int)
        ):
            raise _fee_evidence_refusal(
                event_class,
                fill_id,
                "capture has no usable native fill identity; require an integer "
                "tid or non-empty hash plus integer oid and time",
            )
        native_hash = raw_hash
        native_oid = raw_oid
        derived_native_fill_id = f"{raw_hash}:{raw_oid}:{raw_time}"

    if reported.native_fill_id != derived_native_fill_id:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"declares native fill {reported.native_fill_id!r}, not captured "
            f"native fill {derived_native_fill_id!r}",
        )
    if reported.native_instrument != coin:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"declares native instrument {reported.native_instrument!r}, not "
            f"captured coin {coin!r}; no symbol alias is inferred",
        )

    if event_timestamp.tzinfo is None:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            "cannot bind capture time to a timezone-naive runtime event",
        )
    utc_event = event_timestamp.astimezone(timezone.utc)
    if utc_event.microsecond % 1000:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            "runtime event time has sub-millisecond precision and cannot equal "
            "the captured integer millisecond time without rounding",
        )
    epoch_delta = utc_event - datetime(1970, 1, 1, tzinfo=timezone.utc)
    event_time_ms = (
        (epoch_delta.days * 86400 + epoch_delta.seconds) * 1000
        + epoch_delta.microseconds // 1000
    )
    if raw_time != event_time_ms:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"capture time {raw_time} does not equal runtime event time "
            f"{event_time_ms} milliseconds",
        )

    raw_fee = native.get("fee")
    amount_decimal, amount = _captured_decimal_float(
        raw_fee,
        label="fee",
        event_class=event_class,
        fill_id=fill_id,
    )
    if not isinstance(reported.reported_amount, str):
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            "has a reported_amount assertion that is not the exact source string",
        )
    if reported.reported_amount != raw_fee:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"asserts fee source text {reported.reported_amount!r}, which does "
            f"not match captured fee source text {raw_fee!r}",
        )
    captured_token = native.get("feeToken")
    if not isinstance(captured_token, str) or not captured_token:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"has captured feeToken {captured_token!r}, not a non-empty string",
        )
    if captured_token != reported.fee_token or captured_token != settlement_currency:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"has captured feeToken {captured_token!r}, caller token "
            f"{reported.fee_token!r}, and settlement currency "
            f"{settlement_currency!r}; all must match exactly",
        )

    if reported.fee_class == REPORTED_FEE_CHARGE and amount_decimal < 0:
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: reported fee for fill {fill_id} is negative but is "
            "not declared a rebate",
        )
    if reported.fee_class == REPORTED_FEE_REBATE and amount_decimal > 0:
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: reported fee for fill {fill_id} is declared a "
            "rebate but is positive",
        )

    if "closedPnl" not in native:
        raw_closed_pnl = None
        if reported.closed_pnl is not None:
            raise _fee_evidence_refusal(
                event_class,
                fill_id,
                f"asserts closedPnl {reported.closed_pnl!r}, but the capture "
                "does not contain closedPnl",
            )
        closed_pnl = None
    else:
        raw_closed_pnl = native["closedPnl"]
        if reported.closed_pnl is not None and (
            not isinstance(reported.closed_pnl, str)
            or reported.closed_pnl != raw_closed_pnl
        ):
            raise _fee_evidence_refusal(
                event_class,
                fill_id,
                f"asserts closedPnl source text {reported.closed_pnl!r}, which "
                f"does not match captured source text {raw_closed_pnl!r}",
            )
        _, closed_pnl = _captured_decimal_float(
            raw_closed_pnl,
            label="closedPnl",
            event_class=event_class,
            fill_id=fill_id,
        )

    if coin != evaluated_symbol:
        raise _fee_evidence_refusal(
            event_class,
            fill_id,
            f"declares native instrument {reported.native_instrument!r} and "
            f"captured coin {coin!r}, not evaluated runtime symbol "
            f"{evaluated_symbol!r}; no symbol alias is inferred",
        )
    for scope_key, verified_value in (
        ("symbol_scope", evaluated_symbol),
        ("venue_scope", verified_venue),
        ("product_type_scope", verified_product_type),
    ):
        if scope_key in cost and cost[scope_key] != verified_value:
            raise _fee_evidence_refusal(
                event_class,
                fill_id,
                f"cost {scope_key} {cost[scope_key]!r} does not match verified "
                f"instrument value {verified_value!r}",
            )

    return _CapturedReportedFee(
        amount=amount,
        amount_raw=raw_fee,
        closed_pnl=closed_pnl,
        closed_pnl_raw=raw_closed_pnl,
        native_fill_id=derived_native_fill_id,
        native_instrument=coin,
        native_time_ms=raw_time,
        native_hash=native_hash,
        native_oid=native_oid,
        native_tid=native_tid,
        capture_bytes_base64=base64.b64encode(capture).decode("ascii"),
    )


def _admitted_reported_fee(
    *,
    cost: Mapping[str, Any],
    fill_id: str,
    event_class: str,
    reported_fees: tuple[ReportedFillFee, ...],
) -> ReportedFillFee:
    """Select one typed row while retaining legacy refusal ordering.

    Missing, ``None``, non-finite, wrong-token, duplicated or sign-inconsistent
    inputs all refuse.  Nothing here ever falls back to zero, to the schedule or
    to another fill's number.

    Exact source-text and capture checks happen in
    :func:`_require_fee_evidence_consistency`.  Finite legacy numeric objects
    still reach that check, where absent proof gets a typed refusal rather than
    a constructor ``TypeError``.
    """
    for row in reported_fees:
        if row is not None and not isinstance(row, ReportedFillFee):
            raise EconomicsRefusal(
                REFUSED_MISSING_ADMITTED_FEE,
                f"{event_class}: reported fee row is not a typed ReportedFillFee",
            )
    matching = [row for row in reported_fees if row is not None and row.fill_id == fill_id]
    if not matching:
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: no venue-reported fee for fill {fill_id}; an "
            "admitted cost is never defaulted, estimated or zeroed",
        )
    if len(matching) != 1:
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: {len(matching)} venue-reported fees for fill {fill_id}",
        )
    reported = matching[0]
    amount = reported.reported_amount
    if amount is None or isinstance(amount, bool) or not isinstance(
        amount, (str, int, float)
    ):
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: reported fee for fill {fill_id} is not a number",
        )
    if isinstance(amount, (int, float)) and not math.isfinite(float(amount)):
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: reported fee for fill {fill_id} is not finite",
        )
    settlement_currency = str(cost["settlement_currency"])
    if reported.fee_token != settlement_currency:
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: reported fee for fill {fill_id} is denominated in "
            f"{reported.fee_token!r}, not the settlement currency "
            f"{settlement_currency!r}",
        )
    if reported.fee_class not in (REPORTED_FEE_CHARGE, REPORTED_FEE_REBATE):
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: reported fee for fill {fill_id} carries unknown "
            f"fee_class {reported.fee_class!r}",
        )
    if (
        isinstance(amount, (int, float))
        and reported.fee_class == REPORTED_FEE_CHARGE
        and float(amount) < 0.0
    ):
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: reported fee for fill {fill_id} is negative but is "
            "not declared a rebate",
        )
    if (
        isinstance(amount, (int, float))
        and reported.fee_class == REPORTED_FEE_REBATE
        and float(amount) > 0.0
    ):
        raise EconomicsRefusal(
            REFUSED_MISSING_ADMITTED_FEE,
            f"{event_class}: reported fee for fill {fill_id} is declared a "
            "rebate but is positive",
        )
    if reported.closed_pnl is not None and not isinstance(reported.closed_pnl, str):
        if isinstance(reported.closed_pnl, bool) or not isinstance(
            reported.closed_pnl, (int, float)
        ):
            raise EconomicsRefusal(
                REFUSED_MISSING_ADMITTED_FEE,
                f"{event_class}: closed_pnl for fill {fill_id} is not a number",
            )
        if not math.isfinite(float(reported.closed_pnl)):
            raise EconomicsRefusal(
                REFUSED_MISSING_ADMITTED_FEE,
                f"{event_class}: closed_pnl for fill {fill_id} is not finite",
            )
    return reported


def _estimator_parameters(cost: Mapping[str, Any]) -> float:
    """The owner-signed guarded-estimator parameters, or a refusal."""
    if cost.get("estimator_schedule_id") != GUARDED_ESTIMATOR_SCHEDULE_ID:
        raise EconomicsRefusal(
            REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE,
            "the admitted-cost path requires estimator_schedule_id "
            f"{GUARDED_ESTIMATOR_SCHEDULE_ID!r}, got "
            f"{cost.get('estimator_schedule_id')!r}",
        )
    estimator = cost.get("estimator")
    if not isinstance(estimator, Mapping):
        raise EconomicsRefusal(
            REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE,
            "the admitted-cost path requires an estimator object",
        )
    if estimator.get("tolerance_form") != ESTIMATOR_TOLERANCE_FORM:
        raise EconomicsRefusal(
            REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE,
            f"estimator.tolerance_form must be {ESTIMATOR_TOLERANCE_FORM!r}",
        )
    tolerance = estimator.get("tolerance_relative")
    if (
        isinstance(tolerance, bool)
        or not isinstance(tolerance, (int, float))
        or float(tolerance) != ESTIMATOR_TOLERANCE_RELATIVE
    ):
        # A record may not widen (or narrow) the owner-signed B2=C tolerance.
        raise EconomicsRefusal(
            REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE,
            "estimator.tolerance_relative must be the owner-signed "
            f"{ESTIMATOR_TOLERANCE_RELATIVE}, got {tolerance!r}",
        )
    return float(tolerance)


def _admitted_fee_rows(
    *,
    records: EconomicRecords,
    cost: Mapping[str, Any],
    event_timestamp: datetime,
    lifecycle_id: int,
    fill_id: str,
    fill_sequence: int,
    event_class: str,
    evaluated_symbol: str,
    role: str,
    rate: float,
    fill_price: float,
    quantity: float,
    contract_multiplier: float,
    cash_sequence: int,
    fee_sequence: int,
    reported_fees: tuple[ReportedFillFee, ...],
) -> tuple[CashEvent, FeeEvent, tuple[_PendingDecision, ...]]:
    """The ``HL_FEE_REPORTED_PER_FILL_V1`` admitted-cost path.

    The admitted cash amount is the captured fee source string projected into
    the existing float bookkeeping only after a lossless canonical-decimal
    round-trip guard.  Exact bytes, digest, selected native fields and caller
    declarations are rechecked here.  This proves local consistency only, not
    venue origin, account ownership or production permission.

    The schedule is evaluated *alongside* it purely as a guarded estimator: a
    deviation beyond the owner-signed tolerance suspends the estimator for
    pre-trade sizing and raises a signed-risk marker, and never changes the
    admitted amount.

    The two arms stay separable end to end.  On the emitted ``FeeEvent``,
    ``rate`` and ``fee_notional`` are estimator inputs while ``fee_amount`` and
    ``fee_cash_delta`` are the venue's own number; in the decision details the
    ``estimator_*``/``tolerance_*`` members and the ``reported_*``/``fee_*``
    members are named apart for the same reason.  ``fixed_component`` belongs
    to neither: no fixed component is applied here and none is invented, so it
    is absent rather than zero.
    """
    refused = cost.get("refused_event_classes")
    if isinstance(refused, Mapping) and event_class in refused:
        raise EconomicsRefusal(
            REFUSED_UNMAPPED_FILL_EVENT_CLASS,
            f"{event_class} is refused by this schedule: {refused[event_class]}",
        )
    if "admitted_interval_start" not in cost:
        raise EconomicsRefusal(
            REFUSED_UNSPECIFIED_ADMITTED_INTERVAL_START,
            "the admitted-cost path requires an explicit admitted_interval_start field",
        )
    raw_start = cost["admitted_interval_start"]
    if raw_start is None:
        raise EconomicsRefusal(
            REFUSED_UNSPECIFIED_ADMITTED_INTERVAL_START,
            "admitted_interval_start is UNSPECIFIED (the first authenticated "
            "own-account fill is not established); no admitted cost can be "
            "computed before it",
        )
    start = _parse_z_timestamp(raw_start, "admitted_interval_start")
    if event_timestamp.tzinfo is None:
        raise EconomicsRefusal(
            REFUSED_ECONOMIC_INPUT, "admitted cost requires a timezone-aware event timestamp"
        )
    if event_timestamp.astimezone(timezone.utc) < start:
        raise EconomicsRefusal(
            REFUSED_BEFORE_ADMITTED_INTERVAL_START,
            f"{event_class} at {event_timestamp.isoformat()} precedes the "
            f"admitted interval start {raw_start}",
        )

    tolerance_relative = _estimator_parameters(cost)
    reported = _admitted_reported_fee(
        cost=cost,
        fill_id=fill_id,
        event_class=event_class,
        reported_fees=reported_fees,
    )
    # There is exactly one typed row for this internal fill.  Every use then
    # re-hashes and re-parses its supplied proof; there is no trusted flag.
    declared_account, declared_product = _declared_account_and_product(cost)
    settlement_currency = str(cost["settlement_currency"])
    evidence = _require_fee_evidence_consistency(
        reported=reported,
        cost=cost,
        fill_id=fill_id,
        event_class=event_class,
        declared_account=declared_account,
        declared_product=declared_product,
        settlement_currency=settlement_currency,
        event_timestamp=event_timestamp,
        evaluated_symbol=evaluated_symbol,
        verified_venue=records.instrument.venue,
        verified_product_type=records.instrument.product_type,
    )
    amount = evidence.amount
    notional = abs(fill_price * quantity * contract_multiplier)
    estimate = notional * rate
    deviation = abs(amount - estimate)
    tolerance = tolerance_relative * abs(estimate)
    suspended = deviation > tolerance
    # The admitted amount is the venue's charge; the estimator never overrides it.
    signed = 0.0 if amount == 0.0 else -amount
    # Two arms, never one.  Everything prefixed ``reported_``/``fee_`` is the
    # captured charged number and its local evidence binding; everything
    # prefixed ``estimator_``/``tolerance_`` is the pinned schedule's guarded
    # pre-trade estimate.  The admitted cash is the first arm only: the second
    # never produced, corrected or replaced it.
    shared_details: dict[str, object] = {
        "admitted_cost_source": ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1,
        "estimator_schedule_id": GUARDED_ESTIMATOR_SCHEDULE_ID,
        "event_class": event_class,
        "fill_id": fill_id,
        "liquidity_role": role,
        "reported_amount": amount,
        "reported_amount_raw": evidence.amount_raw,
        "fee_token": reported.fee_token,
        "fee_class": reported.fee_class,
        "closed_pnl": evidence.closed_pnl,
        "closed_pnl_raw": evidence.closed_pnl_raw,
        "closed_pnl_status": (
            "CAPTURED_RAW_STRING"
            if evidence.closed_pnl_raw is not None
            else "NOT_PRESENT_UNKNOWN"
        ),
        "fee_source_class": reported.source_class,
        "fee_account_scope": reported.account_scope,
        "fee_product": reported.product,
        "fee_capture_sha256": reported.capture_sha256,
        "fee_capture_bytes_base64": evidence.capture_bytes_base64,
        "fee_native_fill_id": evidence.native_fill_id,
        "fee_native_fill_id_declared": reported.native_fill_id,
        "fee_native_instrument": evidence.native_instrument,
        "fee_native_instrument_declared": reported.native_instrument,
        "fee_native_time_ms": evidence.native_time_ms,
        "fee_native_hash": evidence.native_hash,
        "fee_native_oid": evidence.native_oid,
        "fee_native_tid": evidence.native_tid,
        "fee_declared_context_class": "CALLER_DECLARED_NOT_NATIVE_FIELDS",
        "fee_evidence_limit": (
            "INTERNALLY_CONSISTENT_CAPTURE_MAY_BE_FORGED_ORIGIN_NOT_ESTABLISHED"
        ),
        "fixed_component_status": FIXED_COMPONENT_UNRESOLVED,
        "estimator_rate": rate,
        "estimator_notional": notional,
        "estimator_amount": estimate,
        "absolute_deviation": deviation,
        "tolerance_form": ESTIMATOR_TOLERANCE_FORM,
        "tolerance_relative": tolerance_relative,
        "tolerance_absolute": tolerance,
    }
    pending = [
        _PendingDecision(
            decision=ADMITTED_COST_APPLIED,
            details=_details(**shared_details),
        )
    ]
    if suspended:
        pending.append(
            _PendingDecision(
                decision=FEE_ESTIMATOR_SUSPENDED,
                details=_details(
                    estimator_suspended_for="PRE_TRADE_SIZING",
                    signed_risk_id=ESTIMATOR_DEVIATION_SIGNED_RISK_ID,
                    admitted_amount_overridden=False,
                    **shared_details,
                ),
            )
        )
    else:
        pending.append(
            _PendingDecision(
                decision=FEE_ESTIMATOR_AGREED,
                details=_details(**shared_details),
            )
        )
    cash_event_id = f"CE-FEE-{fill_sequence}"
    cash = CashEvent(
        sequence=cash_sequence,
        cash_event_id=cash_event_id,
        event_timestamp=event_timestamp,
        lifecycle_id=lifecycle_id,
        kind=CashEventKind.FEE,
        signed_delta=signed,
        settlement_currency=settlement_currency,
        fill_id=fill_id,
    )
    fee = FeeEvent(
        sequence=fee_sequence,
        event_timestamp=event_timestamp,
        lifecycle_id=lifecycle_id,
        fill_id=fill_id,
        event_class=event_class,
        liquidity_role=role,
        schedule_id=str(cost["schedule_id"]),
        schedule_digest=records.cost_digest,
        # Estimator arm: ``rate`` and ``fee_notional`` are the pinned
        # schedule's guarded pre-trade inputs and nothing else.  They did not
        # produce ``fee_amount``.
        rate=rate,
        # No fixed component exists on this path.  Its evidence is unresolved
        # and none was applied, so the value is absent — ``None``, never the
        # invented number ``0.0`` — and its terminal disposition travels as
        # ``fixed_component_status`` in the decision details above.
        fixed_component=None,
        fee_notional=notional,
        # Captured-reported arm: locally consistent, not origin-authenticated.
        fee_amount=amount,
        fee_cash_delta=signed,
        settlement_currency=settlement_currency,
        cash_event_id=cash_event_id,
    )
    return cash, fee, tuple(pending)


def _fee_rows(
    *,
    records: EconomicRecords,
    event_timestamp: datetime,
    lifecycle_id: int,
    fill_id: str,
    fill_sequence: int,
    event_class: str,
    evaluated_symbol: str,
    fill_price: float,
    quantity: float,
    contract_multiplier: float,
    cash_sequence: int,
    fee_sequence: int,
    reported_fees: tuple[ReportedFillFee, ...] = (),
) -> tuple[CashEvent, FeeEvent, tuple[_PendingDecision, ...]]:
    if records.cost is None or records.cost_digest is None:
        raise EconomicsRefusal(REFUSED_MISSING_COST_SCHEDULE, event_class)
    roles = records.cost.get("liquidity_roles")
    if not isinstance(roles, Mapping) or event_class not in roles:
        raise EconomicsRefusal(REFUSED_UNMAPPED_FILL_EVENT_CLASS, event_class)
    role = str(roles[event_class])
    rate_key = "maker_rate" if role == "MAKER" else "taker_rate" if role == "TAKER" else None
    if rate_key is None:
        raise EconomicsRefusal(REFUSED_ECONOMIC_INPUT, f"unknown liquidity role {role!r}")
    rate = float(records.cost[rate_key])
    admitted_source = records.cost.get("admitted_cost_source")
    if admitted_source is not None:
        if admitted_source not in ADMITTED_COST_SOURCES:
            raise EconomicsRefusal(
                REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE,
                f"unknown admitted cost source {admitted_source!r}",
            )
        return _admitted_fee_rows(
            records=records,
            cost=records.cost,
            event_timestamp=event_timestamp,
            lifecycle_id=lifecycle_id,
            fill_id=fill_id,
            fill_sequence=fill_sequence,
            event_class=event_class,
            evaluated_symbol=evaluated_symbol,
            role=role,
            rate=rate,
            fill_price=fill_price,
            quantity=quantity,
            contract_multiplier=contract_multiplier,
            cash_sequence=cash_sequence,
            fee_sequence=fee_sequence,
            reported_fees=reported_fees,
        )
    fixed = float(records.cost.get("fixed_component", 0.0))
    minimum = float(records.cost.get("minimum_fee", 0.0))
    if records.cost.get("fee_rounding_rule") != "EXACT_IDENTITY_V1":
        raise EconomicsRefusal(REFUSED_ECONOMIC_INPUT, "fee rounding rule is not executable")
    notional = abs(fill_price * quantity * contract_multiplier)
    amount = max(notional * rate + fixed, minimum)
    signed = 0.0 if amount == 0.0 else -amount
    cash_event_id = f"CE-FEE-{fill_sequence}"
    cash = CashEvent(
        sequence=cash_sequence,
        cash_event_id=cash_event_id,
        event_timestamp=event_timestamp,
        lifecycle_id=lifecycle_id,
        kind=CashEventKind.FEE,
        signed_delta=signed,
        settlement_currency=str(records.cost["settlement_currency"]),
        fill_id=fill_id,
    )
    fee = FeeEvent(
        sequence=fee_sequence,
        event_timestamp=event_timestamp,
        lifecycle_id=lifecycle_id,
        fill_id=fill_id,
        event_class=event_class,
        liquidity_role=role,
        schedule_id=str(records.cost["schedule_id"]),
        schedule_digest=records.cost_digest,
        rate=rate,
        fixed_component=fixed,
        fee_notional=notional,
        fee_amount=amount,
        fee_cash_delta=signed,
        settlement_currency=str(records.cost["settlement_currency"]),
        cash_event_id=cash_event_id,
    )
    return cash, fee, ()


def _appended_decisions(
    *,
    decisions: list[DecisionEvent],
    pending: tuple[_PendingDecision, ...],
    base_sequence: int,
    event_timestamp: datetime,
) -> None:
    for item in pending:
        decisions.append(
            DecisionEvent(
                sequence=base_sequence + len(decisions),
                event_timestamp=event_timestamp,
                decision=item.decision,
                refusal_code=item.refusal_code,
                details=item.details,
            )
        )


class LegacyEconomicsAdapter(ExecutionEconomics):
    """The frozen ``1.0.0`` economic behavior at the new seam."""

    semantics_id = "1.0.0"

    def resolve(
        self,
        state: EconomicState,
        intent: EconomicIntent,
        market_event: MarketEvent,
        records: EconomicRecords,
    ) -> EconomicTransition:
        resolve_semantics_id(self.semantics_id)
        instrument = self._instrument(records, market_event)
        if intent.kind is IntentKind.FUNDING_TICK:
            return _empty_transition(
                semantics_id=self.semantics_id, state=state, records=records
            )
        if intent.kind is IntentKind.OPEN:
            reference = market_event.close if intent.reference_price is None else float(intent.reference_price)
            resolved_stop = _entry_stop(intent, reference, instrument)
            quantity = (
                float(intent.requested_quantity)
                if intent.requested_quantity is not None
                else _size_quantity(
                    corrected=False,
                    entry=reference,
                    stop=resolved_stop,
                    equity=state.sizing_equity,
                    risk_pct=intent.risk_pct,
                    fallback_size_pct=intent.fallback_size_pct,
                    max_leverage_cap=intent.max_leverage_cap,
                    instrument=instrument,
                )
            )
            if quantity <= 0.0:
                return _empty_transition(
                    semantics_id=self.semantics_id, state=state, records=records
                )
            lifecycle_id = state.lifecycle_id or 1
            fill = FillDecision(
                sequence=0,
                event_timestamp=market_event.timestamp,
                lifecycle_id=lifecycle_id,
                fill_id="F0",
                event_class="ENTRY",
                side=intent.action_side or "BUY",
                reference_price=reference,
                slippage_model_id="LEGACY_NONE",
                slippage_bps=0.0,
                slippage_impact=0.0,
                slippage_application_count=0,
                final_fill_price=reference,
                quantity=quantity,
                liquidity_role="LEGACY_UNSPECIFIED",
            )
            return EconomicTransition(
                semantics_id=self.semantics_id,
                instrument_record_id=records.instrument.record_id,
                instrument_record_digest=records.instrument.digest,
                cost_schedule_id=None,
                cost_schedule_digest=None,
                funding_schedule_id=records.funding_schedule_id,
                funding_schedule_digest=records.funding_digest,
                next_position_facts=_position_facts(
                    lifecycle_id=lifecycle_id,
                    side=intent.position_side,
                    quantity=quantity,
                    entry_fill_price=reference,
                    active_stop_price=resolved_stop,
                ),
                fill_decisions=(fill,),
            )
        return self._resolve_exit(state, intent, market_event, records, instrument)

    @staticmethod
    def _instrument(
        records: EconomicRecords, market_event: MarketEvent
    ) -> InstrumentMetadata:
        runtime = records.runtime_instrument_config
        if runtime:
            return InstrumentMetadata.from_config(dict(runtime))
        return records.instrument.for_evaluation(market_event.timestamp, {})

    def _resolve_exit(
        self,
        state: EconomicState,
        intent: EconomicIntent,
        market_event: MarketEvent,
        records: EconomicRecords,
        instrument: InstrumentMetadata,
    ) -> EconomicTransition:
        del instrument
        if state.lifecycle_id is None or state.quantity <= 0.0:
            return _empty_transition(semantics_id=self.semantics_id, state=state, records=records)
        candidates = _legacy_touched_candidates(state, intent, market_event)
        stop = next((item for item in candidates if item[0].kind is IntentKind.PROTECTIVE_STOP), None)
        chosen = stop or (candidates[0] if candidates else None)
        if chosen is None:
            return _empty_transition(semantics_id=self.semantics_id, state=state, records=records)
        candidate, reference = chosen
        fill_id = "F0"
        action_side = "SELL" if state.position_side == "LONG" else "BUY"
        fill = FillDecision(
            sequence=0,
            event_timestamp=market_event.timestamp,
            lifecycle_id=state.lifecycle_id,
            fill_id=fill_id,
            event_class="PROTECTIVE_STOP_EXIT" if candidate.kind is IntentKind.PROTECTIVE_STOP else "TARGET_EXIT",
            side=action_side,
            reference_price=reference,
            slippage_model_id="LEGACY_NONE",
            slippage_bps=0.0,
            slippage_impact=0.0,
            slippage_application_count=0,
            final_fill_price=reference,
            quantity=state.quantity,
            liquidity_role="LEGACY_UNSPECIFIED",
        )
        gross = _gross_delta(state, reference, state.quantity, records.instrument.contract_multiplier)
        cash = CashEvent(
            sequence=0,
            cash_event_id="CE-GROSS-0",
            event_timestamp=market_event.timestamp,
            lifecycle_id=state.lifecycle_id,
            kind=CashEventKind.GROSS_REALIZATION,
            signed_delta=gross,
            settlement_currency=str(records.instrument.settlement_currency),
            fill_id=fill_id,
        )
        return EconomicTransition(
            semantics_id=self.semantics_id,
            instrument_record_id=records.instrument.record_id,
            instrument_record_digest=records.instrument.digest,
            funding_schedule_id=records.funding_schedule_id,
            funding_schedule_digest=records.funding_digest,
            next_position_facts=_position_facts(
                lifecycle_id=None, side=None, quantity=0.0, entry_fill_price=None
            ),
            fill_decisions=(fill,),
            cash_events=(cash,),
        )


def _gross_delta(
    state: EconomicState,
    fill_price: float,
    quantity: float,
    multiplier: float | int | None,
) -> float:
    if state.entry_fill_price is None or multiplier is None:
        raise EconomicsRefusal(REFUSED_ECONOMIC_INPUT, "exit requires entry and multiplier")
    if state.position_side == "LONG":
        return (fill_price - state.entry_fill_price) * quantity * float(multiplier)
    if state.position_side == "SHORT":
        return (state.entry_fill_price - fill_price) * quantity * float(multiplier)
    raise EconomicsRefusal(REFUSED_ECONOMIC_INPUT, "exit requires a position side")


def _entry_stop(
    intent: EconomicIntent,
    entry_fill: float,
    instrument: InstrumentMetadata,
) -> float | None:
    if intent.stop_price is not None:
        return intent.stop_price
    if intent.stop_distance is not None:
        distance = float(intent.stop_distance)
        if not math.isfinite(distance) or distance <= 0.0:
            raise EconomicsRefusal(
                REFUSED_ECONOMIC_INPUT,
                "stop_distance must be positive and finite",
            )
        if intent.position_side == "LONG":
            return instrument.floor_price(entry_fill - distance)
        if intent.position_side == "SHORT":
            return instrument.ceil_price(entry_fill + distance)
        raise EconomicsRefusal(
            REFUSED_ECONOMIC_INPUT, "entry stop requires position side"
        )
    if intent.stop_percent is None:
        return None
    percent = float(intent.stop_percent)
    if not math.isfinite(percent) or percent <= 0.0:
        raise EconomicsRefusal(REFUSED_ECONOMIC_INPUT, "stop_percent must be positive and finite")
    if intent.position_side == "LONG":
        return instrument.floor_price(entry_fill * (1.0 - percent / 100.0))
    if intent.position_side == "SHORT":
        return instrument.ceil_price(entry_fill * (1.0 + percent / 100.0))
    raise EconomicsRefusal(REFUSED_ECONOMIC_INPUT, "entry stop requires position side")


def _touched_candidates(
    state: EconomicState,
    intent: EconomicIntent,
    market: MarketEvent,
) -> list[tuple[ExitCandidate, float]]:
    touched: list[tuple[ExitCandidate, float]] = []
    for candidate in intent.exit_candidates:
        if candidate.kind is IntentKind.PROTECTIVE_STOP:
            if state.position_side == "LONG":
                if market.open <= candidate.price:
                    touched.append((candidate, market.open))
                elif market.low <= candidate.price:
                    touched.append((candidate, candidate.price))
            elif state.position_side == "SHORT":
                if market.open >= candidate.price:
                    touched.append((candidate, market.open))
                elif market.high >= candidate.price:
                    touched.append((candidate, candidate.price))
        elif candidate.kind is IntentKind.TARGET:
            if state.position_side == "LONG" and market.high >= candidate.price:
                touched.append((candidate, candidate.price))
            elif state.position_side == "SHORT" and market.low <= candidate.price:
                touched.append((candidate, candidate.price))
    return touched


def _legacy_touched_candidates(
    state: EconomicState,
    intent: EconomicIntent,
    market: MarketEvent,
) -> list[tuple[ExitCandidate, float]]:
    if market.execution_profile_id != "close_only_deterministic_v2":
        return _touched_candidates(state, intent, market)
    touched: list[tuple[ExitCandidate, float]] = []
    for candidate in intent.exit_candidates:
        if candidate.kind is IntentKind.PROTECTIVE_STOP:
            if state.position_side == "LONG" and market.close <= candidate.price:
                touched.append((candidate, market.close))
            elif state.position_side == "SHORT" and market.close >= candidate.price:
                touched.append((candidate, market.close))
        elif candidate.kind is IntentKind.TARGET:
            if state.position_side == "LONG" and market.close >= candidate.price:
                touched.append((candidate, market.close))
            elif state.position_side == "SHORT" and market.close <= candidate.price:
                touched.append((candidate, market.close))
    return touched


class CorrectedEconomicsAdapter(ExecutionEconomics):
    """The ``2.0.0`` implementation of the design's ordered economics."""

    semantics_id = "2.0.0"

    def resolve(
        self,
        state: EconomicState,
        intent: EconomicIntent,
        market_event: MarketEvent,
        records: EconomicRecords,
    ) -> EconomicTransition:
        resolve_semantics_id(self.semantics_id)
        instrument = records.instrument.for_evaluation(
            market_event.timestamp, records.runtime_instrument_config or {}
        )
        prefix = ()
        if state.next_decision_sequence == 0:
            prefix = (
                DecisionEvent(
                    sequence=0,
                    event_timestamp=market_event.timestamp,
                    decision="SEMANTICS_VALIDATED",
                ),
            )
        if intent.kind is IntentKind.FUNDING_TICK:
            return self._resolve_funding(state, intent, market_event, records, prefix)
        if intent.kind is IntentKind.OPEN:
            return self._resolve_open(state, intent, market_event, records, instrument, prefix)
        return self._resolve_exit(state, intent, market_event, records, instrument, prefix)

    def _resolve_open(
        self,
        state: EconomicState,
        intent: EconomicIntent,
        market: MarketEvent,
        records: EconomicRecords,
        instrument: InstrumentMetadata,
        prefix: tuple[DecisionEvent, ...],
    ) -> EconomicTransition:
        if records.cost is None:
            raise EconomicsRefusal(REFUSED_MISSING_COST_SCHEDULE, "OPEN")
        reference = market.close if intent.reference_price is None else float(intent.reference_price)
        action_side = intent.action_side or "BUY"
        final_fill, bps, impact, alignment = _fill_price(
            reference=reference,
            action_side=action_side,
            instrument=instrument,
            cost=records.cost,
        )
        resolved_stop = _entry_stop(intent, final_fill, instrument)
        # C3=A: floor to the quantity step first, then refuse below the
        # minimum quantity, then refuse below the minimum notional.  With the
        # historical ``min_qty == 0`` records the floored size is admitted
        # exactly as before, so no existing decision stream changes.
        floored_quantity = _size_quantity(
            corrected=True,
            entry=final_fill,
            stop=resolved_stop,
            equity=state.sizing_equity,
            risk_pct=intent.risk_pct,
            fallback_size_pct=intent.fallback_size_pct,
            max_leverage_cap=intent.max_leverage_cap,
            instrument=replace(instrument, min_notional=0.0, min_qty=0.0),
        )
        refused_min_quantity = floored_quantity < instrument.min_qty
        candidate_quantity = 0.0 if refused_min_quantity else floored_quantity
        order_notional = (
            candidate_quantity * final_fill * instrument.contract_multiplier
        )
        refused_min_notional = order_notional <= instrument.min_notional
        quantity = 0.0 if refused_min_notional else candidate_quantity
        selector = "FALLBACK" if resolved_stop is None or not math.isfinite(resolved_stop) else "RISK"
        decisions = list(prefix)
        next_sequence = state.next_decision_sequence + len(decisions)
        decisions.append(
            DecisionEvent(
                sequence=next_sequence,
                event_timestamp=market.timestamp,
                decision="SIZING_COMPUTED",
                details=_details(
                    selector=selector,
                    contract_multiplier=instrument.contract_multiplier,
                    order_notional=order_notional,
                ),
            )
        )
        next_sequence += 1
        if instrument.min_qty > 0.0:
            # Only a positive owner-guard floor produces this pair; the
            # historical zero-floor records keep their exact decision stream.
            decisions.append(
                DecisionEvent(
                    sequence=next_sequence,
                    event_timestamp=market.timestamp,
                    decision=(
                        "REFUSED_MINIMUM_QUANTITY"
                        if refused_min_quantity
                        else "MINIMUM_QUANTITY_ADMITTED"
                    ),
                    refusal_code=(
                        "REFUSED_MINIMUM_QUANTITY" if refused_min_quantity else None
                    ),
                    details=_details(
                        floored_quantity=floored_quantity,
                        quantity_step=instrument.qty_step,
                        required_minimum_quantity=instrument.min_qty,
                        minimum_quantity_provenance=instrument.min_qty_provenance,
                        minimum_quantity_is_owner_guard=instrument.min_qty_is_owner_guard,
                    ),
                )
            )
            next_sequence += 1
            if refused_min_quantity:
                return _empty_transition(
                    semantics_id=self.semantics_id,
                    state=state,
                    records=records,
                    decisions=tuple(decisions),
                )
        decisions.append(
            DecisionEvent(
                sequence=next_sequence,
                event_timestamp=market.timestamp,
                decision=(
                    "REFUSED_MIN_NOTIONAL"
                    if refused_min_notional
                    else "MIN_NOTIONAL_ADMITTED"
                ),
                refusal_code=(
                    "REFUSED_MIN_NOTIONAL" if refused_min_notional else None
                ),
                details=_details(
                    order_notional=order_notional,
                    required_min_notional=instrument.min_notional,
                ),
            )
        )
        if refused_min_notional:
            return _empty_transition(
                semantics_id=self.semantics_id,
                state=state,
                records=records,
                decisions=tuple(decisions),
            )
        lifecycle_id = state.lifecycle_id or state.next_lifecycle_id
        event_class = intent.event_class or "ENTRY"
        _guard_admitted_event_class(records.cost, event_class)
        fill_sequence = state.next_fill_sequence
        fill = FillDecision(
            sequence=fill_sequence,
            event_timestamp=market.timestamp,
            lifecycle_id=lifecycle_id,
            fill_id=f"F{fill_sequence}",
            event_class=event_class,
            side=action_side,
            reference_price=reference,
            slippage_model_id=str(records.cost["slippage_model_id"]),
            slippage_bps=bps,
            slippage_impact=impact,
            slippage_application_count=1,
            final_fill_price=final_fill,
            quantity=quantity,
            liquidity_role=str(records.cost["liquidity_roles"][event_class]),
            price_tick_alignment=alignment,
            unrounded_fill_price=(
                reference + impact if action_side == "BUY" else reference - impact
            ),
        )
        fee_cash, fee, pending = _fee_rows(
            records=records,
            event_timestamp=market.timestamp,
            lifecycle_id=lifecycle_id,
            fill_id=fill.fill_id,
            fill_sequence=fill_sequence,
            event_class=event_class,
            evaluated_symbol=instrument.symbol,
            fill_price=final_fill,
            quantity=quantity,
            contract_multiplier=instrument.contract_multiplier,
            cash_sequence=state.next_cash_sequence,
            fee_sequence=state.next_fee_sequence,
            reported_fees=intent.reported_fill_fees,
        )
        _appended_decisions(
            decisions=decisions,
            pending=pending,
            base_sequence=state.next_decision_sequence,
            event_timestamp=market.timestamp,
        )
        return EconomicTransition(
            semantics_id=self.semantics_id,
            instrument_record_id=records.instrument.record_id,
            instrument_record_digest=records.instrument.digest,
            cost_schedule_id=records.cost_schedule_id,
            cost_schedule_digest=records.cost_digest,
            funding_schedule_id=records.funding_schedule_id,
            funding_schedule_digest=records.funding_digest,
            next_position_facts=_position_facts(
                lifecycle_id=lifecycle_id,
                side=intent.position_side,
                quantity=quantity,
                entry_fill_price=final_fill,
                active_stop_price=resolved_stop,
            ),
            decision_events=tuple(decisions),
            fill_decisions=(fill,),
            cash_events=(fee_cash,),
            fee_events=(fee,),
        )

    def _resolve_exit(
        self,
        state: EconomicState,
        intent: EconomicIntent,
        market: MarketEvent,
        records: EconomicRecords,
        instrument: InstrumentMetadata,
        prefix: tuple[DecisionEvent, ...],
    ) -> EconomicTransition:
        if state.lifecycle_id is None or state.quantity <= 0.0:
            return _empty_transition(
                semantics_id=self.semantics_id,
                state=state,
                records=records,
                decisions=prefix,
            )
        if intent.kind is IntentKind.MARKET_EXIT:
            return self._resolve_market_exit(
                state, intent, market, records, instrument, prefix
            )
        policy = intent.same_bar_collision_policy_id
        if policy not in {"STOP_FIRST", "TARGET_FIRST", "SUBBAR_UNKNOWN"}:
            raise EconomicsRefusal(REFUSED_UNSUPPORTED_COLLISION_POLICY, str(policy))
        touched = _touched_candidates(state, intent, market)
        stops = [item for item in touched if item[0].kind is IntentKind.PROTECTIVE_STOP]
        targets = [item for item in touched if item[0].kind is IntentKind.TARGET]
        stop_candidate = next(
            (
                candidate
                for candidate in intent.exit_candidates
                if candidate.kind is IntentKind.PROTECTIVE_STOP
            ),
            None,
        )
        collision = bool(stops and targets)
        if collision and policy == "SUBBAR_UNKNOWN":
            raise EconomicsRefusal(REFUSED_AMBIGUOUS_SAME_BAR, "stop and target touched")
        if collision and policy == "STOP_FIRST":
            chosen = [(stops[0][0], stops[0][1], state.quantity)]
        else:
            if state.position_side == "LONG":
                targets.sort(
                    key=lambda item: (item[0].price, item[0].exit_id.encode("utf-8"))
                )
            else:
                targets.sort(
                    key=lambda item: (-item[0].price, item[0].exit_id.encode("utf-8"))
                )
            chosen: list[tuple[ExitCandidate, float, float]] = []
            remainder = state.quantity
            for candidate, reference in targets:
                quantity = min(remainder, state.quantity * candidate.quantity_fraction)
                if quantity > 0.0:
                    chosen.append((candidate, reference, quantity))
                    remainder -= quantity
            if stops and remainder > 0.0:
                chosen.append((stops[0][0], stops[0][1], remainder))
            if not targets and stops:
                chosen = [(stops[0][0], stops[0][1], state.quantity)]
        decisions = list(prefix)
        next_sequence = state.next_decision_sequence + len(decisions)
        if stop_candidate is not None:
            if state.position_side == "LONG":
                open_beyond_stop = market.open <= stop_candidate.price
                intrabar_touch = market.low <= stop_candidate.price
                touch_predicate = "LOW_TOUCH"
            else:
                open_beyond_stop = market.open >= stop_candidate.price
                intrabar_touch = market.high >= stop_candidate.price
                touch_predicate = "HIGH_TOUCH"
            if open_beyond_stop:
                predicate = "OPEN_BEYOND_STOP"
                reference_source = "BAR_OPEN"
                reference_price = market.open
            elif intrabar_touch:
                predicate = touch_predicate
                reference_source = "STOP_LEVEL"
                reference_price = stop_candidate.price
            else:
                predicate = "NO_TOUCH"
                reference_source = None
                reference_price = None
            selected_stop = next(
                (
                    (candidate, reference, quantity)
                    for candidate, reference, quantity in chosen
                    if candidate.kind is IntentKind.PROTECTIVE_STOP
                ),
                None,
            )
            stop_details: dict[str, object] = {
                "position_side": state.position_side,
                "stop_price": stop_candidate.price,
                "predicate": predicate,
            }
            if selected_stop is not None:
                stop_details.update(
                    reference_source=reference_source,
                    reference_price=reference_price,
                )
            decisions.append(
                DecisionEvent(
                    sequence=next_sequence,
                    event_timestamp=market.timestamp,
                    decision="PROTECTIVE_STOP_EVALUATED",
                    details=_details(**stop_details),
                )
            )
            next_sequence += 1
        if not chosen:
            return _empty_transition(
                semantics_id=self.semantics_id,
                state=state,
                records=records,
                decisions=tuple(decisions),
            )
        if any(
            candidate.kind is IntentKind.TARGET
            for candidate in intent.exit_candidates
        ):
            touched_target_prices = [candidate.price for candidate, _reference in targets]
            equal_price_tie = len(touched_target_prices) != len(set(touched_target_prices))
            collision_details: dict[str, object] = {
                "collision": collision,
                "same_bar_collision_policy_id": policy,
                "touched_exit_ids": [
                    candidate.exit_id
                    for candidate, _reference in touched
                    if candidate.kind is IntentKind.PROTECTIVE_STOP
                ]
                + [
                    candidate.exit_id
                    for candidate, _reference in touched
                    if candidate.kind is IntentKind.TARGET
                ],
                "ordered_chosen_exit_ids": [candidate.exit_id for candidate, _reference, _quantity in chosen],
                "reference_quantity": state.quantity,
                "stop_remainder_quantity": sum(
                    quantity
                    for candidate, _reference, quantity in chosen
                    if candidate.kind is IntentKind.PROTECTIVE_STOP
                ),
            }
            if targets:
                ordering_rule = (
                    "LONG_ASCENDING_TARGET_PRICE"
                    if state.position_side == "LONG"
                    else "SHORT_DESCENDING_TARGET_PRICE"
                )
                collision_details["target_ordering_rule"] = ordering_rule + (
                    "_THEN_EXIT_ID_UTF8_BYTE_ORDER" if equal_price_tie else ""
                )
            if equal_price_tie:
                collision_details["tie_break_applied"] = True
            decisions.append(
                DecisionEvent(
                    sequence=next_sequence,
                    event_timestamp=market.timestamp,
                    decision="COLLISION_RESOLVED",
                    details=_details(**collision_details),
                )
            )
        fills: list[FillDecision] = []
        cash: list[CashEvent] = []
        fees: list[FeeEvent] = []
        remaining = state.quantity
        for index, (candidate, reference, quantity) in enumerate(chosen):
            event_class = (
                "PROTECTIVE_STOP_EXIT"
                if candidate.kind is IntentKind.PROTECTIVE_STOP
                else "TARGET_EXIT"
            )
            action_side = "SELL" if state.position_side == "LONG" else "BUY"
            if records.cost is None:
                raise EconomicsRefusal(REFUSED_MISSING_COST_SCHEDULE, event_class)
            _guard_admitted_event_class(records.cost, event_class)
            final_fill, bps, impact, alignment = _fill_price(
                reference=reference,
                action_side=action_side,
                instrument=instrument,
                cost=records.cost,
            )
            fill_sequence = state.next_fill_sequence + index
            fill_id = f"F{fill_sequence}"
            fills.append(
                FillDecision(
                    sequence=fill_sequence,
                    event_timestamp=market.timestamp,
                    lifecycle_id=state.lifecycle_id,
                    fill_id=fill_id,
                    event_class=event_class,
                    side=action_side,
                    reference_price=reference,
                    slippage_model_id=str(records.cost["slippage_model_id"]),
                    slippage_bps=bps,
                    slippage_impact=impact,
                    slippage_application_count=1,
                    final_fill_price=final_fill,
                    quantity=quantity,
                    liquidity_role=str(records.cost["liquidity_roles"][event_class]),
                    exit_id=candidate.exit_id,
                    price_tick_alignment=alignment,
                    unrounded_fill_price=(
                        reference + impact if action_side == "BUY" else reference - impact
                    ),
                )
            )
            fee_cash, fee, pending = _fee_rows(
                records=records,
                event_timestamp=market.timestamp,
                lifecycle_id=state.lifecycle_id,
                fill_id=fill_id,
                fill_sequence=fill_sequence,
                event_class=event_class,
                evaluated_symbol=instrument.symbol,
                fill_price=final_fill,
                quantity=quantity,
                contract_multiplier=instrument.contract_multiplier,
                cash_sequence=state.next_cash_sequence + len(cash),
                fee_sequence=state.next_fee_sequence + len(fees),
                reported_fees=intent.reported_fill_fees,
            )
            _appended_decisions(
                decisions=decisions,
                pending=pending,
                base_sequence=state.next_decision_sequence,
                event_timestamp=market.timestamp,
            )
            cash.append(fee_cash)
            fees.append(fee)
            gross = _gross_delta(state, final_fill, quantity, instrument.contract_multiplier)
            cash.append(
                CashEvent(
                    sequence=state.next_cash_sequence + len(cash),
                    cash_event_id=f"CE-GROSS-{fill_sequence}",
                    event_timestamp=market.timestamp,
                    lifecycle_id=state.lifecycle_id,
                    kind=CashEventKind.GROSS_REALIZATION,
                    signed_delta=gross,
                    settlement_currency=str(records.instrument.settlement_currency),
                    fill_id=fill_id,
                )
            )
            remaining -= quantity
        next_facts = (
            _position_facts(lifecycle_id=None, side=None, quantity=0.0, entry_fill_price=None)
            if remaining <= 0.0
            else _position_facts(
                lifecycle_id=state.lifecycle_id,
                side=state.position_side,
                quantity=remaining,
                entry_fill_price=state.entry_fill_price,
            )
        )
        return EconomicTransition(
            semantics_id=self.semantics_id,
            instrument_record_id=records.instrument.record_id,
            instrument_record_digest=records.instrument.digest,
            cost_schedule_id=records.cost_schedule_id,
            cost_schedule_digest=records.cost_digest,
            funding_schedule_id=records.funding_schedule_id,
            funding_schedule_digest=records.funding_digest,
            next_position_facts=next_facts,
            decision_events=tuple(decisions),
            fill_decisions=tuple(fills),
            cash_events=tuple(cash),
            fee_events=tuple(fees),
        )

    def _resolve_market_exit(
        self,
        state: EconomicState,
        intent: EconomicIntent,
        market: MarketEvent,
        records: EconomicRecords,
        instrument: InstrumentMetadata,
        prefix: tuple[DecisionEvent, ...],
    ) -> EconomicTransition:
        if records.cost is None:
            raise EconomicsRefusal(REFUSED_MISSING_COST_SCHEDULE, "MARKET_EXIT")
        requested = state.quantity if intent.requested_quantity is None else float(
            intent.requested_quantity
        )
        quantity = min(state.quantity, max(0.0, requested))
        if quantity <= 0.0:
            return _empty_transition(
                semantics_id=self.semantics_id,
                state=state,
                records=records,
                decisions=prefix,
            )
        reference = market.close if intent.reference_price is None else float(
            intent.reference_price
        )
        action_side = "SELL" if state.position_side == "LONG" else "BUY"
        final_fill, bps, impact, alignment = _fill_price(
            reference=reference,
            action_side=action_side,
            instrument=instrument,
            cost=records.cost,
        )
        event_class = intent.event_class or "MARKET_EXIT"
        _guard_admitted_event_class(records.cost, event_class)
        fill_sequence = state.next_fill_sequence
        fill = FillDecision(
            sequence=fill_sequence,
            event_timestamp=market.timestamp,
            lifecycle_id=int(state.lifecycle_id),
            fill_id=f"F{fill_sequence}",
            event_class=event_class,
            side=action_side,
            reference_price=reference,
            slippage_model_id=str(records.cost["slippage_model_id"]),
            slippage_bps=bps,
            slippage_impact=impact,
            slippage_application_count=1,
            final_fill_price=final_fill,
            quantity=quantity,
            liquidity_role=str(records.cost["liquidity_roles"][event_class]),
            exit_id=intent.exit_id,
            price_tick_alignment=alignment,
            unrounded_fill_price=(
                reference + impact if action_side == "BUY" else reference - impact
            ),
        )
        fee_cash, fee, pending = _fee_rows(
            records=records,
            event_timestamp=market.timestamp,
            lifecycle_id=int(state.lifecycle_id),
            fill_id=fill.fill_id,
            fill_sequence=fill_sequence,
            event_class=event_class,
            evaluated_symbol=instrument.symbol,
            fill_price=final_fill,
            quantity=quantity,
            contract_multiplier=instrument.contract_multiplier,
            cash_sequence=state.next_cash_sequence,
            fee_sequence=state.next_fee_sequence,
            reported_fees=intent.reported_fill_fees,
        )
        market_exit_decisions = list(prefix)
        _appended_decisions(
            decisions=market_exit_decisions,
            pending=pending,
            base_sequence=state.next_decision_sequence,
            event_timestamp=market.timestamp,
        )
        gross = CashEvent(
            sequence=state.next_cash_sequence + 1,
            cash_event_id=f"CE-GROSS-{fill_sequence}",
            event_timestamp=market.timestamp,
            lifecycle_id=int(state.lifecycle_id),
            kind=CashEventKind.GROSS_REALIZATION,
            signed_delta=_gross_delta(
                state, final_fill, quantity, instrument.contract_multiplier
            ),
            settlement_currency=str(records.instrument.settlement_currency),
            fill_id=fill.fill_id,
        )
        remainder = state.quantity - quantity
        next_facts = (
            _position_facts(
                lifecycle_id=None,
                side=None,
                quantity=0.0,
                entry_fill_price=None,
            )
            if remainder <= 0.0
            else _position_facts(
                lifecycle_id=state.lifecycle_id,
                side=state.position_side,
                quantity=remainder,
                entry_fill_price=state.entry_fill_price,
            )
        )
        return EconomicTransition(
            semantics_id=self.semantics_id,
            instrument_record_id=records.instrument.record_id,
            instrument_record_digest=records.instrument.digest,
            cost_schedule_id=records.cost_schedule_id,
            cost_schedule_digest=records.cost_digest,
            funding_schedule_id=records.funding_schedule_id,
            funding_schedule_digest=records.funding_digest,
            next_position_facts=next_facts,
            decision_events=tuple(market_exit_decisions),
            fill_decisions=(fill,),
            cash_events=(fee_cash, gross),
            fee_events=(fee,),
        )

    def _resolve_funding(
        self,
        state: EconomicState,
        intent: EconomicIntent,
        market: MarketEvent,
        records: EconomicRecords,
        prefix: tuple[DecisionEvent, ...],
    ) -> EconomicTransition:
        event_id = intent.funding_event_id
        events = records.funding.get("events")
        if not isinstance(events, tuple) and not isinstance(events, list):
            raise EconomicsRefusal(REFUSED_MISSING_FUNDING_EVENT, str(event_id))
        matching = [event for event in events if event.get("funding_event_id") == event_id]
        if len(matching) != 1:
            raise EconomicsRefusal(REFUSED_MISSING_FUNDING_EVENT, str(event_id))
        event = matching[0]
        payer = event.get("positive_rate_payer")
        if not isinstance(payer, str) or payer not in {"LONG", "SHORT"}:
            raise EconomicsRefusal(
                REFUSED_ECONOMIC_INPUT,
                f"positive_rate_payer must be LONG or SHORT, got {payer!r}",
            )
        eligible = (
            intent.funding_event_in_window
            and state.lifecycle_id is not None
            and state.quantity > 0.0
        )
        if (
            state.lifecycle_id is not None
            and (str(event_id), int(state.lifecycle_id)) in state.applied_funding_event_keys
        ):
            raise EconomicsRefusal(REFUSED_DUPLICATE_FUNDING_EVENT, str(event_id))
        decision = DecisionEvent(
            sequence=state.next_decision_sequence + len(prefix),
            event_timestamp=market.timestamp,
            decision="FUNDING_ELIGIBILITY",
            details=_details(
                funding_event_id=event_id,
                eligible=eligible,
                position_snapshot_rule=records.funding.get("position_snapshot_rule"),
            ),
        )
        if not eligible:
            return _empty_transition(
                semantics_id=self.semantics_id,
                state=state,
                records=records,
                decisions=(*prefix, decision),
            )
        multiplier = float(records.instrument.contract_multiplier)
        oracle_price = float(event["oracle_price"])
        raw_rate = float(event["raw_rate"])
        long_rate = -raw_rate if payer == "LONG" else raw_rate
        side_factor = 1.0 if state.position_side == "LONG" else -1.0
        notional = abs(oracle_price * state.quantity * multiplier)
        signed = notional * long_rate * side_factor
        cumulative = state.cumulative_funding + signed
        funding_sequence = state.next_funding_sequence
        cash_event_id = f"CE-FUND-{funding_sequence}"
        cash = CashEvent(
            sequence=state.next_cash_sequence,
            cash_event_id=cash_event_id,
            event_timestamp=market.timestamp,
            lifecycle_id=int(state.lifecycle_id),
            kind=CashEventKind.FUNDING,
            signed_delta=signed,
            settlement_currency=str(records.funding["settlement_currency"]),
            funding_event_id=str(event_id),
        )
        funding = FundingEvent(
            sequence=funding_sequence,
            funding_event_id=str(event_id),
            event_timestamp=market.timestamp,
            lifecycle_id=int(state.lifecycle_id),
            position_side=str(state.position_side),
            open_qty=state.quantity,
            contract_multiplier=multiplier,
            oracle_price=oracle_price,
            raw_rate=raw_rate,
            positive_rate_payer=payer,
            long_cashflow_rate=long_rate,
            notional=notional,
            funding_cash_delta=signed,
            cumulative_funding=cumulative,
            schedule_id=records.funding_schedule_id,
            schedule_digest=records.funding_digest,
            source_event_digest=str(event["source_event_digest"]),
            cash_event_id=cash_event_id,
        )
        return EconomicTransition(
            semantics_id=self.semantics_id,
            instrument_record_id=records.instrument.record_id,
            instrument_record_digest=records.instrument.digest,
            cost_schedule_id=records.cost_schedule_id,
            cost_schedule_digest=records.cost_digest,
            funding_schedule_id=records.funding_schedule_id,
            funding_schedule_digest=records.funding_digest,
            next_position_facts=_position_facts(
                lifecycle_id=state.lifecycle_id,
                side=state.position_side,
                quantity=state.quantity,
                entry_fill_price=state.entry_fill_price,
            ),
            decision_events=(*prefix, decision),
            cash_events=(cash,),
            funding_events=(funding,),
        )
