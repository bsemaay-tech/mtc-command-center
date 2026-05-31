from __future__ import annotations

from mtc_v2.core.exits import STOP_OWNER_INITIAL
from mtc_v2.core.rounding import floor_qty_to_step
from mtc_v2.core.types import Bar, EntryDecision, EntryLeg, ExitEvent, PortfolioState, Position, RawSignal, WorkingExit


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
