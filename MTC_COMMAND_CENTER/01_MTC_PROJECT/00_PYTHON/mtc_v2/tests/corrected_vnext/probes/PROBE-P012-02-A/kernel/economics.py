"""Version-selected execution economics for one atomic state transition.

The public seam is :meth:`ExecutionEconomics.resolve`.  It is deliberately
pure: callers provide immutable facts and receive an immutable
``EconomicTransition``.  Only the caller may apply the returned cash ledger or
position facts.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
import math
from pathlib import Path
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


def _fee_rows(
    *,
    records: EconomicRecords,
    event_timestamp: datetime,
    lifecycle_id: int,
    fill_id: str,
    fill_sequence: int,
    event_class: str,
    fill_price: float,
    quantity: float,
    contract_multiplier: float,
    cash_sequence: int,
    fee_sequence: int,
) -> tuple[CashEvent, FeeEvent]:
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
    return cash, fee


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
        candidate_quantity = _size_quantity(
            corrected=True,
            entry=final_fill,
            stop=resolved_stop,
            equity=state.sizing_equity,
            risk_pct=intent.risk_pct,
            fallback_size_pct=intent.fallback_size_pct,
            max_leverage_cap=intent.max_leverage_cap,
            instrument=replace(instrument, min_notional=0.0),
        )
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
        fee_cash, fee = _fee_rows(
            records=records,
            event_timestamp=market.timestamp,
            lifecycle_id=lifecycle_id,
            fill_id=fill.fill_id,
            fill_sequence=fill_sequence,
            event_class=event_class,
            fill_price=final_fill,
            quantity=quantity,
            contract_multiplier=instrument.contract_multiplier,
            cash_sequence=state.next_cash_sequence,
            fee_sequence=state.next_fee_sequence,
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
            fee_cash, fee = _fee_rows(
                records=records,
                event_timestamp=market.timestamp,
                lifecycle_id=state.lifecycle_id,
                fill_id=fill_id,
                fill_sequence=fill_sequence,
                event_class=event_class,
                fill_price=final_fill,
                quantity=quantity,
                contract_multiplier=instrument.contract_multiplier,
                cash_sequence=state.next_cash_sequence + len(cash),
                fee_sequence=state.next_fee_sequence + len(fees),
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
        fee_cash, fee = _fee_rows(
            records=records,
            event_timestamp=market.timestamp,
            lifecycle_id=int(state.lifecycle_id),
            fill_id=fill.fill_id,
            fill_sequence=fill_sequence,
            event_class=event_class,
            fill_price=final_fill,
            quantity=quantity,
            contract_multiplier=instrument.contract_multiplier,
            cash_sequence=state.next_cash_sequence,
            fee_sequence=state.next_fee_sequence,
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
            decision_events=prefix,
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
