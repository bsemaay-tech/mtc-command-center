from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math
from typing import Deque, Iterable

from mtc_v2.core.config import (
    EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
    SL_BASIS_CLOSE,
    TP_MODE_ATR,
    TP_MODE_MULTI,
    TP_MODE_PERCENT,
    TP_MODE_R,
)
from mtc_v2.core.indicators import AtrStopIndicatorSnapshot, AtrTakeProfitIndicatorSnapshot
from mtc_v2.core.rounding import ceil_to_grid, floor_to_grid, round_half_up_to_grid
from mtc_v2.core.types import Bar, Position, WorkingExit


REASON_EXIT_SL_ATR = "sl_atr_hit"
REASON_EXIT_SL_PERCENT = "sl_percent_hit"
REASON_EXIT_SL_SWING_ATR = "sl_swing_atr_hit"
REASON_EXIT_TP_ATR = "tp_atr_hit"
REASON_EXIT_TP_PERCENT = "tp_percent_hit"
REASON_EXIT_TP_R = "tp_r_hit"
REASON_EXIT_TP1 = "tp1_hit"
REASON_EXIT_TP2 = "tp2_hit"
REASON_EXIT_BE = "be_hit"
REASON_EXIT_TRAIL = "trail_hit"

POSITION_SIDE_LONG = "long"
POSITION_SIDE_SHORT = "short"

STOP_OWNER_INITIAL = "INITIAL_SL"
STOP_OWNER_BE = "BE"
STOP_OWNER_TRAIL = "TRAIL"


@dataclass(slots=True, frozen=True)
class PriceExitHit:
    hit: bool = False
    fill_price: float | None = None
    reason: str | None = None
    is_pessimistic: bool = False
    exit_pct: float = 1.0
    exit_id: str | None = None
    continue_evaluation_this_bar: bool = False
    cancel_remaining_targets_after_fill: bool = False


class AtrTracker:
    def __init__(self, *, length: int, enabled: bool, snapshot_kind: str) -> None:
        self.length = int(length)
        self.enabled = bool(enabled)
        self.snapshot_kind = snapshot_kind
        if self.length < 1:
            raise ValueError("ATR length must be >= 1")
        self._trs: Deque[float] = deque(maxlen=self.length)
        self._prev_close: float | None = None
        self._prev_atr: float | None = None
        self._valid_bar = True

    @property
    def warmup_bars_required(self) -> int:
        return self.length if self.enabled else 0

    @property
    def atr(self) -> float | None:
        return self._prev_atr

    @property
    def valid_bar(self) -> bool:
        return self._valid_bar

    @property
    def warmup_ready(self) -> bool:
        return (not self.enabled) or self._prev_atr is not None

    def update(self, bar: Bar):
        if not self.enabled:
            self._valid_bar = True
            return self.snapshot()

        if not is_valid_bar(bar):
            self._valid_bar = False
            return self.snapshot()

        self._valid_bar = True
        tr = self._true_range(bar)
        self._trs.append(tr)

        if len(self._trs) < self.length:
            self._prev_close = bar.close
            return self.snapshot()

        if self._prev_atr is None:
            self._prev_atr = sum(self._trs) / float(self.length)
        else:
            self._prev_atr = ((self._prev_atr * float(self.length - 1)) + tr) / float(self.length)
        self._prev_close = bar.close
        return self.snapshot()

    def snapshot(self):
        if self.snapshot_kind == "tp":
            return AtrTakeProfitIndicatorSnapshot(
                atr=self._prev_atr,
                valid_bar=self._valid_bar,
                warmup_ready=self.warmup_ready,
            )
        return AtrStopIndicatorSnapshot(
            atr=self._prev_atr,
            valid_bar=self._valid_bar,
            warmup_ready=self.warmup_ready,
        )

    def _true_range(self, bar: Bar) -> float:
        if self._prev_close is None:
            return bar.high - bar.low
        return max(bar.high - bar.low, abs(bar.high - self._prev_close), abs(bar.low - self._prev_close))


def is_valid_bar(bar: Bar) -> bool:
    prices = (bar.open, bar.high, bar.low, bar.close)
    if not all(math.isfinite(price) for price in prices):
        return False
    if bar.high < bar.low:
        return False
    if bar.open < bar.low or bar.open > bar.high:
        return False
    if bar.close < bar.low or bar.close > bar.high:
        return False
    return True


def sync_working_exit_stops(position: Position) -> None:
    for working_exit in position.working_exits:
        if working_exit.active:
            working_exit.stop_price = position.active_stop_price


def find_swing_reference(
    history: Iterable[Bar],
    *,
    is_long: bool,
    lookback: int,
    basis: str,
) -> float | None:
    bars = list(history)
    if not bars:
        return None

    window = bars[-int(lookback) :]
    if not window:
        return None

    if basis == SL_BASIS_CLOSE:
        values = [bar.close for bar in window]
    else:
        values = [bar.low for bar in window] if is_long else [bar.high for bar in window]

    if not values:
        return None
    return min(values) if is_long else max(values)


def align_stop_price(price: float, *, side: str, price_tick: float) -> float:
    if side == POSITION_SIDE_LONG:
        return floor_to_grid(price, price_tick)
    if side == POSITION_SIDE_SHORT:
        return ceil_to_grid(price, price_tick)
    raise ValueError(f"Unsupported side: {side}")


def calc_sl(
    config: dict[str, object],
    *,
    bar: Bar,
    entry_price: float,
    is_long: bool,
    price_tick: float,
    atr_value: float | None = None,
    swing_reference: float | None = None,
    swing_atr_value: float | None = None,
) -> float | None:
    if not bool(config["use_sl"]):
        return None

    side = POSITION_SIDE_LONG if is_long else POSITION_SIDE_SHORT

    if bool(config["use_sl_atr"]):
        if atr_value is None:
            return None
        distance = float(config["sl_atr_mult"]) * float(atr_value)
        raw = entry_price - distance if is_long else entry_price + distance
        return align_stop_price(raw, side=side, price_tick=price_tick)

    if bool(config["use_sl_percent"]):
        distance_ratio = float(config["sl_percent"]) / 100.0
        raw = entry_price * (1.0 - distance_ratio) if is_long else entry_price * (1.0 + distance_ratio)
        return align_stop_price(raw, side=side, price_tick=price_tick)

    if bool(config["use_sl_swing_atr"]):
        if swing_reference is None or swing_atr_value is None:
            return None
        distance = float(config["sl_swing_atr_mult"]) * float(swing_atr_value)
        raw = swing_reference - distance if is_long else swing_reference + distance
        return align_stop_price(raw, side=side, price_tick=price_tick)

    return None


def build_working_exit_book(
    config: dict[str, object],
    *,
    entry_price: float,
    is_long: bool,
    price_tick: float,
    atr_value: float | None = None,
    initial_risk_per_unit: float | None = None,
    book_version: int,
    completed_exit_ids: set[str] | None = None,
) -> tuple[float | None, list[WorkingExit]]:
    completed = set(completed_exit_ids or set())
    tp_mode = str(config["tp_mode"])
    direction = 1.0 if is_long else -1.0

    def _tp_price(distance: float) -> float:
        raw = entry_price + (direction * float(distance))
        return round_half_up_to_grid(raw, price_tick)

    if tp_mode == "None":
        return None, []

    if tp_mode == TP_MODE_ATR:
        if atr_value is None:
            return None, []
        target = _tp_price(float(config["tp_atr_mult"]) * float(atr_value))
        return target, [WorkingExit("TP", "TP", target, None, 1.0, book_version=book_version)]

    if tp_mode == TP_MODE_PERCENT:
        ratio = float(config["tp_percent"]) / 100.0
        raw = entry_price * (1.0 + ratio) if is_long else entry_price * (1.0 - ratio)
        target = round_half_up_to_grid(raw, price_tick)
        return target, [WorkingExit("TP", "TP", target, None, 1.0, book_version=book_version)]

    if tp_mode == TP_MODE_R:
        if initial_risk_per_unit is None or initial_risk_per_unit <= 0.0:
            return None, []
        target = _tp_price(initial_risk_per_unit * float(config["tp_r_multiple"]))
        return target, [WorkingExit("TP", "TP", target, None, 1.0, book_version=book_version)]

    if tp_mode == TP_MODE_MULTI:
        if initial_risk_per_unit is None or initial_risk_per_unit <= 0.0:
            return None, []
        exits: list[WorkingExit] = []
        if "TP1" not in completed:
            tp1_target = _tp_price(initial_risk_per_unit * float(config["tp1_r_multiple"]))
            exits.append(
                WorkingExit(
                    "TP1",
                    "TP1",
                    tp1_target,
                    None,
                    float(config["tp1_close_pct"]) / 100.0,
                    book_version=book_version,
                )
            )
        if "TP2" not in completed:
            tp2_target = _tp_price(initial_risk_per_unit * float(config["tp2_r_multiple"]))
            exits.append(WorkingExit("TP2", "TP2", tp2_target, None, 1.0, book_version=book_version))
        first_target = exits[0].target_price if exits else None
        return first_target, exits

    return None, []


def update_protective_stop_owner(
    config: dict[str, object],
    *,
    position: Position,
    bar: Bar,
    prev_bar: Bar | None = None,
    price_tick: float,
    trail_atr: float | None = None,
) -> None:
    if position.active_stop_price is None or position.initial_risk_per_unit is None:
        sync_working_exit_stops(position)
        return

    is_long = position.side == POSITION_SIDE_LONG
    initial_risk = float(position.initial_risk_per_unit)
    close_only_execution = _is_close_only_execution(config)
    tw_research_mode = str(config.get("tw_audit_semantics_mode", "off")) == "research"
    tw_trailing_mode = str(config.get("tw_trailing_semantics_mode", "local"))
    tw_be_mode = str(config.get("tw_be_semantics_mode", "local"))
    trail_source_bar = prev_bar if (tw_research_mode and tw_trailing_mode == "next_bar_confirmed") else bar
    be_source_bar = prev_bar if (tw_research_mode and tw_be_mode == "next_bar_confirmed") else bar

    if bool(config["use_trailing"]) and trail_atr is not None and trail_atr > 0.0:
        trigger_price = position.avg_entry_price + (initial_risk * float(config["trail_start_r"])) * (1.0 if is_long else -1.0)
        use_close_trigger = close_only_execution or (tw_research_mode and tw_trailing_mode == "tradingview")
        if trail_source_bar is None:
            trigger_probe = None
        else:
            trigger_probe = trail_source_bar.close if use_close_trigger else (trail_source_bar.high if is_long else trail_source_bar.low)
        if trigger_probe is None:
            trail_triggered = False
        else:
            trail_triggered = (trigger_probe >= trigger_price) if is_long else (trigger_probe <= trigger_price)
        if position.trail_active or trail_triggered:
            position.trail_active = True
            position.active_stop_owner = STOP_OWNER_TRAIL
            if trail_source_bar is None:
                sync_working_exit_stops(position)
                return
            anchor = trail_source_bar.close if use_close_trigger else (trail_source_bar.high if is_long else trail_source_bar.low)
            if position.trail_price is None:
                position.trail_price = anchor
            else:
                position.trail_price = max(position.trail_price, anchor) if is_long else min(position.trail_price, anchor)
            distance = float(config["trail_distance_atr_mult"]) * float(trail_atr)
            candidate_stop = position.trail_price - distance if is_long else position.trail_price + distance
            aligned_stop = align_stop_price(candidate_stop, side=position.side, price_tick=price_tick)
            if is_long:
                position.active_stop_price = max(position.active_stop_price, aligned_stop)
            else:
                position.active_stop_price = min(position.active_stop_price, aligned_stop)
            sync_working_exit_stops(position)
            return

    if bool(config["use_break_even"]) and position.active_stop_owner != STOP_OWNER_TRAIL:
        trigger_price = position.avg_entry_price + (initial_risk * float(config["be_trigger_r"])) * (1.0 if is_long else -1.0)
        use_close_trigger = close_only_execution or (tw_research_mode and tw_be_mode == "tradingview")
        if be_source_bar is None:
            trigger_probe = None
        else:
            trigger_probe = be_source_bar.close if use_close_trigger else (be_source_bar.high if is_long else be_source_bar.low)
        be_triggered = False if trigger_probe is None else ((trigger_probe >= trigger_price) if is_long else (trigger_probe <= trigger_price))
        if position.be_active or be_triggered:
            position.be_active = True
            position.active_stop_owner = STOP_OWNER_BE
            target_stop = position.entry_price + (initial_risk * float(config["be_buffer_r"])) * (1.0 if is_long else -1.0)
            aligned_stop = align_stop_price(target_stop, side=position.side, price_tick=price_tick)
            if is_long:
                position.active_stop_price = max(position.active_stop_price, aligned_stop)
            else:
                position.active_stop_price = min(position.active_stop_price, aligned_stop)

    sync_working_exit_stops(position)


def evaluate_price_exit(
    config: dict[str, object],
    *,
    bar: Bar,
    position: Position,
) -> PriceExitHit:
    if _is_close_only_execution(config):
        return _evaluate_close_only_price_exit(config, bar=bar, position=position)

    stop_hit = _evaluate_stop_hit(config, bar=bar, position=position)
    target_hit = _evaluate_target_hit(config, bar=bar, position=position)

    if stop_hit.hit and target_hit.hit:
        return PriceExitHit(
            hit=True,
            fill_price=stop_hit.fill_price,
            reason=stop_hit.reason,
            is_pessimistic=True,
            exit_pct=1.0,
            exit_id=stop_hit.exit_id,
            continue_evaluation_this_bar=False,
        )
    if stop_hit.hit:
        return stop_hit
    if target_hit.hit:
        return target_hit
    return PriceExitHit()


def _evaluate_close_only_price_exit(
    config: dict[str, object],
    *,
    bar: Bar,
    position: Position,
) -> PriceExitHit:
    stop_hit = _evaluate_close_only_stop_hit(config, bar=bar, position=position)
    if stop_hit.hit:
        return stop_hit

    return _evaluate_close_only_target_hit(config, bar=bar, position=position)


def _evaluate_stop_hit(config: dict[str, object], *, bar: Bar, position: Position) -> PriceExitHit:
    stop_price = position.active_stop_price
    if stop_price is None or not is_valid_bar(bar):
        return PriceExitHit()

    if position.side == POSITION_SIDE_LONG:
        if bar.open <= stop_price:
            fill_price = bar.open
        elif bar.low <= stop_price:
            fill_price = stop_price
        else:
            return PriceExitHit()
    else:
        if bar.open >= stop_price:
            fill_price = bar.open
        elif bar.high >= stop_price:
            fill_price = stop_price
        else:
            return PriceExitHit()

    return PriceExitHit(
        hit=True,
        fill_price=fill_price,
        reason=_stop_reason(config, position),
        exit_pct=1.0,
        exit_id=str(position.active_stop_owner or STOP_OWNER_INITIAL),
    )


def _evaluate_close_only_stop_hit(
    config: dict[str, object],
    *,
    bar: Bar,
    position: Position,
) -> PriceExitHit:
    stop_price = position.active_stop_price
    if stop_price is None or not is_valid_bar(bar):
        return PriceExitHit()

    if position.side == POSITION_SIDE_LONG:
        if bar.close > stop_price:
            return PriceExitHit()
    else:
        if bar.close < stop_price:
            return PriceExitHit()

    return PriceExitHit(
        hit=True,
        fill_price=bar.close,
        reason=_stop_reason(config, position),
        exit_pct=1.0,
        exit_id=str(position.active_stop_owner or STOP_OWNER_INITIAL),
    )


def _evaluate_target_hit(config: dict[str, object], *, bar: Bar, position: Position) -> PriceExitHit:
    active_exits = [working_exit for working_exit in position.working_exits if working_exit.active and working_exit.target_price is not None]
    if not active_exits or not is_valid_bar(bar):
        return PriceExitHit()

    is_long = position.side == POSITION_SIDE_LONG
    ordered = sorted(
        active_exits,
        key=lambda working_exit: float(working_exit.target_price),
        reverse=not is_long,
    )

    for working_exit in ordered:
        target = float(working_exit.target_price)
        if is_long:
            if bar.open >= target:
                fill_price = bar.open
            elif bar.high >= target:
                fill_price = target
            else:
                continue
        else:
            if bar.open <= target:
                fill_price = bar.open
            elif bar.low <= target:
                fill_price = target
            else:
                continue

        continue_eval = working_exit.kind == "TP1"
        exit_pct = float(working_exit.qty_fraction)
        if working_exit.kind == "TP2":
            exit_pct = 1.0

        return PriceExitHit(
            hit=True,
            fill_price=fill_price,
            reason=_target_reason(config, working_exit),
            exit_pct=exit_pct,
            exit_id=working_exit.exit_id,
            continue_evaluation_this_bar=continue_eval,
        )

    return PriceExitHit()


def _evaluate_close_only_target_hit(
    config: dict[str, object],
    *,
    bar: Bar,
    position: Position,
) -> PriceExitHit:
    active_exits = [working_exit for working_exit in position.working_exits if working_exit.active and working_exit.target_price is not None]
    if not active_exits or not is_valid_bar(bar):
        return PriceExitHit()

    is_long = position.side == POSITION_SIDE_LONG
    ordered = sorted(
        active_exits,
        key=lambda working_exit: float(working_exit.target_price),
        reverse=not is_long,
    )

    for working_exit in ordered:
        target = float(working_exit.target_price)
        if is_long:
            if bar.close < target:
                continue
        else:
            if bar.close > target:
                continue

        continue_eval = False
        exit_pct = float(working_exit.qty_fraction)
        if working_exit.kind == "TP2":
            exit_pct = 1.0
        cancel_remaining_targets = False
        if working_exit.kind == "TP1":
            sibling_targets = [
                float(sibling.target_price)
                for sibling in ordered
                if sibling.exit_id != working_exit.exit_id and sibling.active and sibling.target_price is not None
            ]
            if sibling_targets:
                next_target = sibling_targets[0]
                if is_long:
                    cancel_remaining_targets = bar.close >= next_target
                else:
                    cancel_remaining_targets = bar.close <= next_target

        return PriceExitHit(
            hit=True,
            fill_price=bar.close,
            reason=_target_reason(config, working_exit),
            exit_pct=exit_pct,
            exit_id=working_exit.exit_id,
            continue_evaluation_this_bar=continue_eval,
            cancel_remaining_targets_after_fill=cancel_remaining_targets,
        )

    return PriceExitHit()


def disable_active_target_exits(position: Position) -> None:
    position.active_tp_price = None
    for working_exit in position.working_exits:
        if working_exit.active and working_exit.target_price is not None:
            working_exit.active = False


def _is_close_only_execution(config: dict[str, object]) -> bool:
    return str(config.get("execution_profile_id", "")) == EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC


def _stop_reason(config: dict[str, object], position: Position) -> str:
    owner = str(position.active_stop_owner or STOP_OWNER_INITIAL)
    if owner == STOP_OWNER_TRAIL:
        return REASON_EXIT_TRAIL
    if owner == STOP_OWNER_BE:
        return REASON_EXIT_BE
    if bool(config["use_sl_percent"]):
        return REASON_EXIT_SL_PERCENT
    if bool(config["use_sl_swing_atr"]):
        return REASON_EXIT_SL_SWING_ATR
    return REASON_EXIT_SL_ATR


def _target_reason(config: dict[str, object], working_exit: WorkingExit) -> str:
    if working_exit.kind == "TP1":
        return REASON_EXIT_TP1
    if working_exit.kind == "TP2":
        return REASON_EXIT_TP2
    tp_mode = str(config["tp_mode"])
    if tp_mode == TP_MODE_PERCENT:
        return REASON_EXIT_TP_PERCENT
    if tp_mode == TP_MODE_R:
        return REASON_EXIT_TP_R
    return REASON_EXIT_TP_ATR
