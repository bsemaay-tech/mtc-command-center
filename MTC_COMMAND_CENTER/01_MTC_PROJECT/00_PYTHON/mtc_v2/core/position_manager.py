from __future__ import annotations

from mtc_v2.core.exits import STOP_OWNER_INITIAL
from mtc_v2.core.rounding import floor_qty_to_step
from mtc_v2.core.types import (
    Bar,
    CashEventKind,
    EconomicTransition,
    EconomicTransitionError,
    EntryDecision,
    EntryLeg,
    ExitEvent,
    FillDecision,
    PortfolioState,
    Position,
    RawSignal,
    REFUSED_INVALID_CASH_LEDGER_JOIN,
    WorkingExit,
)


POSITION_SIDE_LONG = "long"
POSITION_SIDE_SHORT = "short"
REASON_EXIT_OPP_SIGNAL = "opp_signal"


def merge_pyramid_stop(
    existing_stop: float | None,
    candidate_stop: float | None,
    *,
    is_long: bool,
) -> float | None:
    if existing_stop is None:
        return candidate_stop
    if candidate_stop is None:
        return existing_stop
    return max(existing_stop, candidate_stop) if is_long else min(existing_stop, candidate_stop)


def calc_avg_entry_price(entry_legs: list[EntryLeg]) -> float:
    active_legs = [leg for leg in entry_legs if leg.qty > 0.0]
    total_qty = sum(leg.qty for leg in active_legs)
    if total_qty <= 0.0:
        return 0.0
    weighted_cost = sum(leg.entry_price * leg.qty for leg in active_legs)
    return weighted_cost / total_qty


def _deplete_entry_legs(
    entry_legs: list[EntryLeg],
    *,
    exit_qty: float,
    qty_step: float,
) -> list[EntryLeg]:
    active_indices = [idx for idx, leg in enumerate(entry_legs) if leg.qty > 0.0]
    if not active_indices:
        return list(entry_legs)

    total_open_qty = sum(entry_legs[idx].qty for idx in active_indices)
    if exit_qty >= total_open_qty:
        return [EntryLeg(leg.entry_price, 0.0, leg.entry_bar) for leg in entry_legs]

    depleted_total = 0.0
    updates = {idx: entry_legs[idx].qty for idx in active_indices}
    last_active_idx = active_indices[-1]

    for idx in active_indices[:-1]:
        leg = entry_legs[idx]
        raw_deplete = exit_qty * leg.qty / total_open_qty
        leg_deplete = floor_qty_to_step(raw_deplete, qty_step)
        leg_deplete = min(leg.qty, leg_deplete)
        updates[idx] = max(0.0, leg.qty - leg_deplete)
        depleted_total += leg_deplete

    final_leg = entry_legs[last_active_idx]
    final_deplete = min(final_leg.qty, max(0.0, exit_qty - depleted_total))
    updates[last_active_idx] = max(0.0, final_leg.qty - final_deplete)

    result: list[EntryLeg] = []
    for idx, leg in enumerate(entry_legs):
        new_qty = updates.get(idx, leg.qty)
        result.append(EntryLeg(leg.entry_price, new_qty, leg.entry_bar))
    return result


def _first_active_tp_price(working_exits: list[WorkingExit]) -> float | None:
    for working_exit in working_exits:
        if working_exit.active and working_exit.target_price is not None:
            return float(working_exit.target_price)
    return None


class PositionManager:
    """Basket owner for entry lifecycle, partial exits and same-side adds."""

    def __init__(
        self,
        *,
        enable_long: bool,
        enable_short: bool,
        regime_lock: bool,
        max_entries: int,
        cooldown_bars: int,
        contract_multiplier: float,
        qty_step: float = 1.0,
    ) -> None:
        self.enable_long = bool(enable_long)
        self.enable_short = bool(enable_short)
        self.regime_lock = bool(regime_lock)
        self.max_entries = int(max_entries)
        self.cooldown_bars = int(cooldown_bars)
        self.contract_multiplier = float(contract_multiplier)
        self.qty_step = float(qty_step)

    @staticmethod
    def _transition_key(transition: EconomicTransition) -> tuple[object, ...]:
        return (
            transition.semantics_id,
            transition.instrument_record_digest,
            transition.cost_schedule_digest,
            transition.funding_schedule_digest,
            tuple(
                (
                    row.event_timestamp,
                    row.lifecycle_id,
                    row.cash_event_id,
                    row.kind.value,
                    row.signed_delta,
                )
                for row in transition.cash_events
            ),
            tuple(
                (row.event_timestamp, row.lifecycle_id, row.fill_id, row.event_class)
                for row in transition.fill_decisions
            ),
            tuple(
                (row.event_timestamp, row.lifecycle_id, row.sequence, row.decision)
                for row in transition.decision_events
            ),
        )

    @staticmethod
    def _cash_key(row: object) -> tuple[object, ...]:
        return (
            getattr(row, "event_timestamp"),
            getattr(row, "lifecycle_id"),
            getattr(row, "cash_event_id"),
        )

    @staticmethod
    def _position_after_exit(
        position: Position,
        fills: tuple[FillDecision, ...],
        *,
        next_quantity: float,
        qty_step: float,
    ) -> Position | None:
        exited = sum(row.quantity for row in fills)
        calculated_remainder = max(0.0, position.qty - exited)
        if abs(calculated_remainder - next_quantity) > 1e-12:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: next position quantity mismatch"
            )
        if next_quantity <= 1e-12:
            return None

        legs = list(position.entry_legs)
        completed = set(position.completed_exit_ids)
        working = list(position.working_exits)
        for fill in fills:
            legs = _deplete_entry_legs(legs, exit_qty=fill.quantity, qty_step=qty_step)
            if fill.exit_id is None:
                continue
            completed.add(fill.exit_id)
            working = [
                WorkingExit(
                    exit_id=row.exit_id,
                    kind=row.kind,
                    target_price=row.target_price,
                    stop_price=row.stop_price,
                    qty_fraction=row.qty_fraction,
                    book_version=row.book_version,
                    active=row.active and row.exit_id != fill.exit_id,
                )
                for row in working
            ]

        return Position(
            side=position.side,
            entry_price=position.entry_price,
            avg_entry_price=calc_avg_entry_price(legs),
            qty=next_quantity,
            entry_bar=position.entry_bar,
            initial_qty=position.initial_qty,
            active_stop_price=position.active_stop_price,
            active_tp_price=_first_active_tp_price(working),
            entry_legs=legs,
            lifecycle_id=position.lifecycle_id,
            working_exit_reference_qty=position.working_exit_reference_qty,
            working_exit_book_version=position.working_exit_book_version,
            active_stop_owner=position.active_stop_owner,
            working_exits=working,
            completed_exit_ids=completed,
            be_active=position.be_active,
            trail_active=position.trail_active,
            trail_price=position.trail_price,
            initial_risk_per_unit=position.initial_risk_per_unit,
        )

    def _position_after_open(
        self,
        state: PortfolioState,
        transition: EconomicTransition,
        *,
        bar: Bar,
        working_exits: list[WorkingExit] | None,
    ) -> Position:
        facts = transition.next_position_facts
        fills = transition.fill_decisions
        if len(fills) != 1 or facts.lifecycle_id is None or facts.side is None:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: invalid open transition shape"
            )
        fill = fills[0]
        side = facts.side.lower()
        exits = list(working_exits or [])
        if state.position is None:
            if abs(facts.quantity - fill.quantity) > 1e-12:
                raise EconomicTransitionError(
                    f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: open quantity mismatch"
                )
            return Position(
                side=side,
                entry_price=fill.final_fill_price,
                avg_entry_price=fill.final_fill_price,
                qty=facts.quantity,
                entry_bar=bar.bar_index,
                initial_qty=facts.quantity,
                active_stop_price=facts.active_stop_price,
                active_tp_price=_first_active_tp_price(exits),
                entry_legs=[EntryLeg(fill.final_fill_price, fill.quantity, bar.bar_index)],
                lifecycle_id=facts.lifecycle_id,
                working_exit_reference_qty=facts.quantity,
                working_exit_book_version=1,
                active_stop_owner=(
                    STOP_OWNER_INITIAL if facts.active_stop_price is not None else None
                ),
                working_exits=exits,
                initial_risk_per_unit=(
                    abs(fill.final_fill_price - facts.active_stop_price)
                    if facts.active_stop_price is not None
                    else None
                ),
            )

        current = state.position
        expected_quantity = current.qty + fill.quantity
        if (
            current.side != side
            or current.lifecycle_id != facts.lifecycle_id
            or abs(facts.quantity - expected_quantity) > 1e-12
        ):
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: add transition position mismatch"
            )
        legs = [*current.entry_legs, EntryLeg(fill.final_fill_price, fill.quantity, bar.bar_index)]
        merged_stop = merge_pyramid_stop(
            current.active_stop_price,
            facts.active_stop_price,
            is_long=side == POSITION_SIDE_LONG,
        )
        next_exits = exits if working_exits is not None else list(current.working_exits)
        return Position(
            side=current.side,
            entry_price=current.entry_price,
            avg_entry_price=calc_avg_entry_price(legs),
            qty=facts.quantity,
            entry_bar=current.entry_bar,
            initial_qty=current.initial_qty + fill.quantity,
            active_stop_price=merged_stop,
            active_tp_price=_first_active_tp_price(next_exits),
            entry_legs=legs,
            lifecycle_id=current.lifecycle_id,
            working_exit_reference_qty=facts.quantity,
            working_exit_book_version=current.working_exit_book_version + 1,
            active_stop_owner=current.active_stop_owner or STOP_OWNER_INITIAL,
            working_exits=next_exits,
            completed_exit_ids=set(current.completed_exit_ids),
            be_active=current.be_active,
            trail_active=current.trail_active,
            trail_price=current.trail_price,
            initial_risk_per_unit=current.initial_risk_per_unit,
        )

    def apply_transition(
        self,
        *,
        bar: Bar,
        state: PortfolioState,
        transition: EconomicTransition,
        reason: str | None = None,
        working_exits: list[WorkingExit] | None = None,
    ) -> None:
        """Commit one already-resolved corrected economic transition atomically.

        The manager applies only ``cash_events`` to equity. Fill prices, gross
        realization, fees, and funding are facts supplied by the transition and
        are never recalculated here.
        """

        if transition.semantics_id != "2.0.0":
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: corrected manager requires 2.0.0"
            )
        transition_key = self._transition_key(transition)
        if transition_key in state.applied_transition_keys:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: transition already applied"
            )
        cash_keys = {
            self._cash_key(row) for row in transition.cash_events
        }
        if cash_keys & state.applied_cash_event_keys:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: cash event already applied"
            )
        funding_ids = {row.funding_event_id for row in transition.funding_events}
        if funding_ids & state.applied_funding_event_ids:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: funding event already applied"
            )

        facts = transition.next_position_facts
        fills = transition.fill_decisions
        entry_fills = tuple(row for row in fills if row.event_class.endswith("ENTRY"))
        exit_fills = tuple(row for row in fills if not row.event_class.endswith("ENTRY"))
        if entry_fills and exit_fills:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: mixed entry and exit transition"
            )

        next_position = state.position
        exit_events: list[ExitEvent] = []
        if entry_fills:
            next_position = self._position_after_open(
                state, transition, bar=bar, working_exits=working_exits
            )
        elif exit_fills:
            if state.position is None:
                raise EconomicTransitionError(
                    f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: exit without position"
                )
            gross_by_fill = {
                row.fill_id: row.signed_delta
                for row in transition.cash_events
                if row.kind is CashEventKind.GROSS_REALIZATION and row.fill_id is not None
            }
            if set(gross_by_fill) != {row.fill_id for row in exit_fills}:
                raise EconomicTransitionError(
                    f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: exit gross-cash join mismatch"
                )
            next_position = self._position_after_exit(
                state.position,
                exit_fills,
                next_quantity=facts.quantity,
                qty_step=self.qty_step,
            )
            collision = any(
                dict(row.details).get("collision") == "True"
                for row in transition.decision_events
            )
            for fill in exit_fills:
                exit_events.append(
                    ExitEvent(
                        bar_index=bar.bar_index,
                        exit_price=fill.final_fill_price,
                        exit_qty=fill.quantity,
                        exit_reason=reason or fill.event_class,
                        realized_pnl=gross_by_fill[fill.fill_id],
                        exit_id=fill.exit_id,
                        was_pessimistic=(
                            collision and fill.event_class == "PROTECTIVE_STOP_EXIT"
                        ),
                        was_partial=next_position is not None,
                        fill_id=fill.fill_id,
                        event_class=fill.event_class,
                        fill_trigger=fill.fill_trigger,
                    )
                )
        elif state.position is not None:
            if (
                facts.lifecycle_id != state.position.lifecycle_id
                or facts.side is None
                or facts.side.lower() != state.position.side
                or abs(facts.quantity - state.position.qty) > 1e-12
            ):
                raise EconomicTransitionError(
                    f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: non-fill position mismatch"
                )

        funding_cash = sum(
            row.signed_delta
            for row in transition.cash_events
            if row.kind is CashEventKind.FUNDING
        )
        if transition.funding_events:
            expected_cumulative = state.cumulative_funding + funding_cash
            if abs(transition.funding_events[-1].cumulative_funding - expected_cumulative) > 1e-12:
                raise EconomicTransitionError(
                    f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: funding cumulative mismatch"
                )

        cash_delta = sum(row.signed_delta for row in transition.cash_events)
        guard_delta = sum(
            row.signed_delta
            for row in transition.cash_events
            if row.kind in (CashEventKind.GROSS_REALIZATION, CashEventKind.FEE)
        )
        gross_delta = sum(
            row.signed_delta
            for row in transition.cash_events
            if row.kind is CashEventKind.GROSS_REALIZATION
        )

        state.position = next_position
        state.realized_equity += cash_delta
        state.equity = state.initial_capital + state.realized_equity
        state.guard_realized_equity += guard_delta
        state.cumulative_fee += sum(row.fee_amount for row in transition.fee_events)
        state.cumulative_funding += funding_cash
        state.decision_events.extend(transition.decision_events)
        state.fill_events.extend(transition.fill_decisions)
        state.cash_events.extend(transition.cash_events)
        state.fee_events.extend(transition.fee_events)
        state.funding_events.extend(transition.funding_events)
        state.applied_transition_keys.add(transition_key)
        state.applied_cash_event_keys.update(cash_keys)
        state.applied_funding_event_ids.update(funding_ids)

        for row in transition.cash_events:
            if row.kind is CashEventKind.GROSS_REALIZATION:
                ledger = state.lifecycle_gross_pnl
            elif row.kind is CashEventKind.FEE:
                ledger = state.lifecycle_fee_cash
            else:
                ledger = state.lifecycle_funding_cash
            ledger[row.lifecycle_id] = ledger.get(row.lifecycle_id, 0.0) + row.signed_delta

        if entry_fills:
            state.total_entries += len(entry_fills)
            state.opened_this_bar_reason = reason
            state.last_entry_bar_index = bar.bar_index
            state.regime_lock_side = next_position.side if next_position is not None else None
            state.next_position_lifecycle_id = max(
                state.next_position_lifecycle_id, facts.lifecycle_id + 1
            )
        if exit_events:
            state.exit_events_this_bar.extend(exit_events)
            state.total_exits += len(exit_events)
            state.last_exit_bar_index = bar.bar_index
            state.closed_this_bar_reason = reason or exit_events[-1].exit_reason
            last = exit_events[-1]
            state.last_exit_price = last.exit_price
            state.last_exit_qty = sum(row.exit_qty for row in exit_events)
            state.last_exit_id = last.exit_id
            state.last_exit_was_pessimistic = last.was_pessimistic
            state.last_exit_was_partial = next_position is not None
            state.last_gross_realized_pnl = gross_delta
            if next_position is None:
                lifecycle_id = transition.cash_events[0].lifecycle_id
                lifecycle_gross = state.lifecycle_gross_pnl.get(lifecycle_id, 0.0)
                lifecycle_fees = state.lifecycle_fee_cash.get(lifecycle_id, 0.0)
                state.last_closed_guard_pnl = lifecycle_gross + lifecycle_fees
                state.last_realized_pnl = state.last_closed_guard_pnl
                state.unrealized_pnl = 0.0

    def can_open_raw_signal(
        self,
        *,
        raw: RawSignal,
        state: PortfolioState,
    ) -> EntryDecision:
        if state.block_new_entries_this_bar:
            return EntryDecision(False)

        if raw.long == raw.short:
            return EntryDecision(False)

        side = POSITION_SIDE_LONG if raw.long else POSITION_SIDE_SHORT
        if side == POSITION_SIDE_LONG and not self.enable_long:
            return EntryDecision(False)
        if side == POSITION_SIDE_SHORT and not self.enable_short:
            return EntryDecision(False)

        same_bar_reentry_allowed = state.closed_this_bar_reason == REASON_EXIT_OPP_SIGNAL
        if (
            not same_bar_reentry_allowed
            and self.cooldown_bars > 0
            and state.last_entry_bar_index is not None
            and (state.current_bar_index - state.last_entry_bar_index) < self.cooldown_bars
        ):
            return EntryDecision(False)

        if state.position is not None:
            if side != state.position.side:
                return EntryDecision(False)
            if len([leg for leg in state.position.entry_legs if leg.qty > 0.0]) >= self.max_entries:
                return EntryDecision(False)

        if self.regime_lock and state.regime_lock_side == side:
            return EntryDecision(False)

        return EntryDecision(
            True,
            side=side,
            reason=raw.reason,
            same_bar_reentry_allowed=same_bar_reentry_allowed,
        )

    def open_position(
        self,
        *,
        bar: Bar,
        side: str,
        qty: float,
        state: PortfolioState,
        reason: str | None,
        active_stop_price: float | None = None,
        active_tp_price: float | None = None,
        working_exits: list[WorkingExit] | None = None,
        fill_price: float | None = None,
    ) -> None:
        if qty <= 0.0:
            return

        working_exits = list(working_exits or [])
        entry_fill_price = float(fill_price) if fill_price is not None else float(bar.close)

        if state.position is None:
            entry_leg = EntryLeg(entry_price=entry_fill_price, qty=qty, entry_bar=bar.bar_index)
            state.position = Position(
                side=side,
                entry_price=entry_fill_price,
                avg_entry_price=entry_fill_price,
                qty=qty,
                entry_bar=bar.bar_index,
                initial_qty=qty,
                active_stop_price=active_stop_price,
                active_tp_price=active_tp_price if active_tp_price is not None else _first_active_tp_price(working_exits),
                entry_legs=[entry_leg],
                lifecycle_id=state.next_position_lifecycle_id,
                working_exit_reference_qty=qty,
                working_exit_book_version=1,
                active_stop_owner=STOP_OWNER_INITIAL if active_stop_price is not None else None,
                working_exits=working_exits,
                completed_exit_ids=set(),
                initial_risk_per_unit=abs(entry_fill_price - active_stop_price)
                if active_stop_price is not None
                else None,
            )
            state.next_position_lifecycle_id += 1
        else:
            position = state.position
            if position.side != side:
                return
            updated_entry_legs = [*position.entry_legs, EntryLeg(entry_fill_price, qty, bar.bar_index)]
            merged_qty = position.qty + qty
            merged_stop = merge_pyramid_stop(
                position.active_stop_price,
                active_stop_price,
                is_long=side == POSITION_SIDE_LONG,
            )
            next_book_version = position.working_exit_book_version + 1
            next_working_exits = list(working_exits) if working_exits else list(position.working_exits)
            next_owner = position.active_stop_owner
            if next_owner is None and merged_stop is not None:
                next_owner = STOP_OWNER_INITIAL
            state.position = Position(
                side=position.side,
                entry_price=position.entry_price,
                avg_entry_price=calc_avg_entry_price(updated_entry_legs),
                qty=merged_qty,
                entry_bar=position.entry_bar,
                initial_qty=position.initial_qty + qty,
                active_stop_price=merged_stop,
                active_tp_price=active_tp_price if active_tp_price is not None else _first_active_tp_price(next_working_exits),
                entry_legs=updated_entry_legs,
                lifecycle_id=position.lifecycle_id,
                working_exit_reference_qty=merged_qty,
                working_exit_book_version=next_book_version,
                active_stop_owner=next_owner,
                working_exits=next_working_exits,
                completed_exit_ids=set(position.completed_exit_ids),
                be_active=position.be_active,
                trail_active=position.trail_active,
                trail_price=position.trail_price,
                initial_risk_per_unit=position.initial_risk_per_unit,
            )

        state.total_entries += 1
        state.opened_this_bar_reason = reason
        state.regime_lock_side = side
        state.last_entry_bar_index = bar.bar_index

    def process_raw_signal(
        self,
        *,
        bar: Bar,
        raw: RawSignal,
        state: PortfolioState,
        qty: float,
        active_stop_price: float | None = None,
        active_tp_price: float | None = None,
        working_exits: list[WorkingExit] | None = None,
    ) -> None:
        decision = self.can_open_raw_signal(raw=raw, state=state)
        if not decision.can_open or decision.side is None:
            return
        self.open_position(
            bar=bar,
            side=decision.side,
            qty=qty,
            state=state,
            reason=decision.reason,
            active_stop_price=active_stop_price,
            active_tp_price=active_tp_price,
            working_exits=working_exits,
        )

    def close_position(
        self,
        *,
        bar: Bar,
        exit_price: float,
        reason: str,
        state: PortfolioState,
        exit_pct: float = 1.0,
        exit_id: str | None = None,
        is_pessimistic: bool = False,
    ) -> None:
        if state.position is None:
            return

        position = state.position
        reference_qty = position.working_exit_reference_qty if position.working_exit_reference_qty > 0.0 else position.qty
        exit_qty = position.qty if exit_pct >= 1.0 else min(position.qty, max(0.0, reference_qty * exit_pct))
        if exit_qty <= 0.0:
            return

        if position.side == POSITION_SIDE_LONG:
            realized_pnl = (exit_price - position.avg_entry_price) * exit_qty * self.contract_multiplier
        else:
            realized_pnl = (position.avg_entry_price - exit_price) * exit_qty * self.contract_multiplier

        remaining_qty = max(0.0, position.qty - exit_qty)
        is_full_close = remaining_qty <= 1e-12

        state.realized_equity += realized_pnl
        state.equity = state.initial_capital + state.realized_equity
        state.last_realized_pnl = realized_pnl
        state.last_exit_price = exit_price
        state.last_exit_qty = exit_qty
        state.last_exit_id = exit_id
        state.last_exit_was_pessimistic = is_pessimistic
        state.last_exit_was_partial = not is_full_close
        state.closed_this_bar_reason = reason
        state.last_exit_bar_index = bar.bar_index
        state.total_exits += 1
        state.exit_events_this_bar.append(
            ExitEvent(
                bar_index=bar.bar_index,
                exit_price=exit_price,
                exit_qty=exit_qty,
                exit_reason=reason,
                realized_pnl=realized_pnl,
                exit_id=exit_id,
                was_pessimistic=is_pessimistic,
                was_partial=not is_full_close,
            )
        )

        if is_full_close:
            state.position = None
            state.unrealized_pnl = 0.0
            return

        updated_legs = _deplete_entry_legs(
            position.entry_legs,
            exit_qty=exit_qty,
            qty_step=self.qty_step,
        )
        completed_exit_ids = set(position.completed_exit_ids)
        if exit_id:
            completed_exit_ids.add(exit_id)

        updated_working_exits: list[WorkingExit] = []
        for working_exit in position.working_exits:
            is_completed_exit = exit_id is not None and working_exit.exit_id == exit_id
            updated_working_exits.append(
                WorkingExit(
                    exit_id=working_exit.exit_id,
                    kind=working_exit.kind,
                    target_price=working_exit.target_price,
                    stop_price=working_exit.stop_price,
                    qty_fraction=working_exit.qty_fraction,
                    book_version=working_exit.book_version,
                    active=working_exit.active and not is_completed_exit,
                )
            )

        state.position = Position(
            side=position.side,
            entry_price=position.entry_price,
            avg_entry_price=calc_avg_entry_price(updated_legs),
            qty=remaining_qty,
            entry_bar=position.entry_bar,
            initial_qty=position.initial_qty,
            active_stop_price=position.active_stop_price,
            active_tp_price=_first_active_tp_price(updated_working_exits),
            entry_legs=updated_legs,
            lifecycle_id=position.lifecycle_id,
            working_exit_reference_qty=position.working_exit_reference_qty,
            working_exit_book_version=position.working_exit_book_version,
            active_stop_owner=position.active_stop_owner,
            working_exits=updated_working_exits,
            completed_exit_ids=completed_exit_ids,
            be_active=position.be_active,
            trail_active=position.trail_active,
            trail_price=position.trail_price,
            initial_risk_per_unit=position.initial_risk_per_unit,
        )
