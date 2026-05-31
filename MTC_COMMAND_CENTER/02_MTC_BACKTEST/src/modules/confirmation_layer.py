from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from ..config.defaults import ConfirmationConfig
from ..engine.indicators import atr


def _pivot_confirmed(src: pd.Series, left: int, right: int, find_high: bool) -> pd.Series:
    """Return Pine-like pivot values on the confirmation bar."""
    vals = src.astype(float).to_numpy()
    out = np.full(len(vals), np.nan, dtype=float)
    if left <= 0 or right <= 0:
        return pd.Series(out, index=src.index, dtype=float)

    for i in range(left + right, len(vals)):
        pivot_idx = i - right
        start = pivot_idx - left
        end = pivot_idx + right + 1
        window = vals[start:end]
        pivot_val = vals[pivot_idx]
        if np.isnan(pivot_val) or np.isnan(window).any():
            continue
        if find_high:
            if pivot_val == np.max(window):
                out[i] = pivot_val
        else:
            if pivot_val == np.min(window):
                out[i] = pivot_val
    return pd.Series(out, index=src.index, dtype=float)


def _swing_ok_long(level: Optional[float], close: float, max_pct: float) -> bool:
    if max_pct <= 0.0:
        return True
    if level is None or np.isnan(level) or close <= 0:
        return False
    if level <= close:
        return True
    return (100.0 * (level - close) / close) <= max_pct


def _swing_ok_short(level: Optional[float], close: float, max_pct: float) -> bool:
    if max_pct <= 0.0:
        return True
    if level is None or np.isnan(level) or close <= 0:
        return False
    if level >= close:
        return True
    return (100.0 * (close - level) / close) <= max_pct


def _in_session(ts: Optional[pd.Timestamp], session: str) -> bool:
    if ts is None or not session or "-" not in session:
        return True
    start_txt, end_txt = session.split("-", 1)
    if len(start_txt) != 4 or len(end_txt) != 4:
        return True
    try:
        start_minutes = int(start_txt[:2]) * 60 + int(start_txt[2:])
        end_minutes = int(end_txt[:2]) * 60 + int(end_txt[2:])
    except ValueError:
        return True

    local = ts if ts.tzinfo is not None else ts.tz_localize("UTC")
    cur_minutes = local.hour * 60 + local.minute
    if start_minutes <= end_minutes:
        return start_minutes <= cur_minutes <= end_minutes
    return cur_minutes >= start_minutes or cur_minutes <= end_minutes


@dataclass
class ConfirmationStepResult:
    long_confirmed: bool
    short_confirmed: bool
    waiting_long: bool
    waiting_short: bool
    long_level: Optional[float] = None
    short_level: Optional[float] = None
    wait_long_start_bar: Optional[int] = None
    wait_short_start_bar: Optional[int] = None
    last_swing_high: Optional[float] = None
    last_swing_low: Optional[float] = None


class ConfirmationLayer:
    """Stateful Pine-style confirmation layer with one-bar confirmed pulses."""

    def __init__(self, df: pd.DataFrame, config: ConfirmationConfig, mintick: float):
        self.c = config
        self.mintick = max(float(mintick), 1e-10)
        self.open_ = df["open"].astype(float).reset_index(drop=True)
        self.high = df["high"].astype(float).reset_index(drop=True)
        self.low = df["low"].astype(float).reset_index(drop=True)
        self.close = df["close"].astype(float).reset_index(drop=True)
        self.timestamps = (
            pd.to_datetime(df["timestamp"], utc=True).reset_index(drop=True)
            if "timestamp" in df.columns else None
        )
        self._pivot_high = _pivot_confirmed(self.high, self.c.p_left, self.c.p_right, True)
        self._pivot_low = _pivot_confirmed(self.low, self.c.p_left, self.c.p_right, False)
        self._atr = atr(self.high, self.low, self.close, self.c.atr_len)
        self._roc1 = ((self.close - self.close.shift(1)) / self.close.shift(1).replace(0.0, np.nan)) * 100.0

        self.last_swing_high: Optional[float] = None
        self.last_swing_low: Optional[float] = None
        self.last_swing_high_bar: Optional[int] = None
        self.last_swing_low_bar: Optional[int] = None
        self.wait_long = False
        self.wait_short = False
        self.long_level: Optional[float] = None
        self.short_level: Optional[float] = None
        self.wait_long_start_bar: Optional[int] = None
        self.wait_short_start_bar: Optional[int] = None
        self.wait_long_started = False
        self.wait_short_started = False
        self.last_long_confirm_bar: Optional[int] = None
        self.last_short_confirm_bar: Optional[int] = None
        self.prev_long_raw = False
        self.prev_short_raw = False
        self.prev_enabled = bool(self.c.enabled)
        self._deferred_flat_long_event = False
        self._deferred_flat_short_event = False
        self._deferred_flat_long_from_bar: Optional[int] = None
        self._deferred_flat_short_from_bar: Optional[int] = None

    def defer_flat_event(
        self,
        *,
        long_event: bool = False,
        short_event: bool = False,
        source_bar: Optional[int] = None,
    ) -> None:
        if long_event:
            self._deferred_flat_long_event = True
            self._deferred_flat_long_from_bar = source_bar
        if short_event:
            self._deferred_flat_short_event = True
            self._deferred_flat_short_from_bar = source_bar

    def align_wait_state_on_eval_start(self, i: int, long_raw: bool, short_raw: bool) -> None:
        """
        Narrow parity hook for eval-start in warmup_only mode.

        During preroll we intentionally advance confirmation state so pivots are
        warmed up. On the first tradable bar, Pine can behave as if the active
        wait uses the freshest confirmed swing level rather than a stale level
        carried from deeper preroll history. We only realign the active wait
        level; we do not reset pivots or wait age.
        """
        if not self.c.enabled:
            return

        ph = self._pivot_high.iloc[i]
        pl = self._pivot_low.iloc[i]
        if not pd.isna(ph):
            self.last_swing_high = float(ph)
            self.last_swing_high_bar = i
        if not pd.isna(pl):
            self.last_swing_low = float(pl)
            self.last_swing_low_bar = i

        close = float(self.close.iloc[i])
        if self.wait_long and bool(long_raw):
            if _swing_ok_long(self.last_swing_high, close, self.c.max_swing_distance_pct):
                self.long_level = self.last_swing_high
        if self.wait_short and bool(short_raw):
            if _swing_ok_short(self.last_swing_low, close, self.c.max_swing_distance_pct):
                self.short_level = self.last_swing_low

    def step(self, i: int, pos_size: float, long_raw: bool, short_raw: bool) -> ConfirmationStepResult:
        if not self.c.enabled:
            self._reset_waits()
            self.prev_long_raw = bool(long_raw)
            self.prev_short_raw = bool(short_raw)
            self.prev_enabled = False
            return ConfirmationStepResult(
                bool(long_raw),
                bool(short_raw),
                False,
                False,
                None,
                None,
                None,
                None,
                self.last_swing_high,
                self.last_swing_low,
            )

        close = float(self.close.iloc[i])
        open_ = float(self.open_.iloc[i])
        high = float(self.high.iloc[i])
        low = float(self.low.iloc[i])
        ts = self.timestamps.iloc[i] if self.timestamps is not None else None

        conf_in_session = (not self.c.use_session_filter) or _in_session(ts, self.c.session)
        conf_should_confirm = conf_in_session and (not self.c.gate_only_when_flat or pos_size == 0)
        conf_use_just_turned_on = self.c.enabled and not self.prev_enabled

        ph = self._pivot_high.iloc[i]
        pl = self._pivot_low.iloc[i]
        if not pd.isna(ph):
            self.last_swing_high = float(ph)
            self.last_swing_high_bar = i
        if not pd.isna(pl):
            self.last_swing_low = float(pl)
            self.last_swing_low_bar = i

        pivot_age_ok_high = (
            self.last_swing_high is not None
            and (
                self.c.max_pivot_age_bars <= 0
                or (self.last_swing_high_bar is not None and (i - self.last_swing_high_bar <= self.c.max_pivot_age_bars))
            )
        )
        pivot_age_ok_low = (
            self.last_swing_low is not None
            and (
                self.c.max_pivot_age_bars <= 0
                or (self.last_swing_low_bar is not None and (i - self.last_swing_low_bar <= self.c.max_pivot_age_bars))
            )
        )

        long_raw_event_edge = conf_should_confirm and bool(long_raw) and not self.prev_long_raw
        short_raw_event_edge = conf_should_confirm and bool(short_raw) and not self.prev_short_raw
        long_raw_event_level = conf_should_confirm and bool(long_raw)
        short_raw_event_level = conf_should_confirm and bool(short_raw)

        if self.c.raw_event_mode == "LEVEL":
            long_raw_event = long_raw_event_level
            short_raw_event = short_raw_event_level
        else:
            long_raw_event = long_raw_event_edge
            short_raw_event = short_raw_event_edge

        if conf_use_just_turned_on and conf_should_confirm:
            long_raw_event = long_raw_event or bool(long_raw)
            short_raw_event = short_raw_event or bool(short_raw)
        deferred_long_from_bar = None
        deferred_short_from_bar = None
        if conf_should_confirm and pos_size == 0:
            if self._deferred_flat_long_event and bool(long_raw):
                long_raw_event = True
                deferred_long_from_bar = self._deferred_flat_long_from_bar
            if self._deferred_flat_short_event and bool(short_raw):
                short_raw_event = True
                deferred_short_from_bar = self._deferred_flat_short_from_bar
        if not bool(long_raw):
            self._deferred_flat_long_event = False
            self._deferred_flat_long_from_bar = None
        if not bool(short_raw):
            self._deferred_flat_short_event = False
            self._deferred_flat_short_from_bar = None
        if long_raw_event:
            self._deferred_flat_long_event = False
            self._deferred_flat_long_from_bar = None
        if short_raw_event:
            self._deferred_flat_short_event = False
            self._deferred_flat_short_from_bar = None

        take_long_event = long_raw_event
        take_short_event = short_raw_event
        if take_long_event and take_short_event:
            if self.c.same_bar_tie_rule == "LONG_WINS":
                take_short_event = False
            elif self.c.same_bar_tie_rule == "SHORT_WINS":
                take_long_event = False
            else:
                take_long_event = False
                take_short_event = False

        if take_long_event and pivot_age_ok_high:
            if self.c.raw_event_mode == "LEVEL":
                allow_start = (not self.wait_long) or (self.c.refresh_on_new_raw_signal and not self.wait_long_started)
            else:
                allow_start = (not self.wait_long) or self.c.refresh_on_new_raw_signal
            if allow_start and _swing_ok_long(self.last_swing_high, close, self.c.max_swing_distance_pct):
                self.wait_long = True
                self.wait_short = False
                self.long_level = self.last_swing_high
                self.short_level = None
                self.wait_long_start_bar = deferred_long_from_bar if deferred_long_from_bar is not None else i
                self.wait_short_start_bar = None
                self.wait_long_started = True
                self.wait_short_started = False
        if take_short_event and pivot_age_ok_low:
            if self.c.raw_event_mode == "LEVEL":
                allow_start = (not self.wait_short) or (self.c.refresh_on_new_raw_signal and not self.wait_short_started)
            else:
                allow_start = (not self.wait_short) or self.c.refresh_on_new_raw_signal
            if allow_start and _swing_ok_short(self.last_swing_low, close, self.c.max_swing_distance_pct):
                self.wait_short = True
                self.wait_long = False
                self.short_level = self.last_swing_low
                self.long_level = None
                self.wait_short_start_bar = deferred_short_from_bar if deferred_short_from_bar is not None else i
                self.wait_long_start_bar = None
                self.wait_short_started = True
                self.wait_long_started = False

        if not self.wait_long:
            self.wait_long_started = False
        if not self.wait_short:
            self.wait_short_started = False

        long_level_updated = False
        short_level_updated = False
        if conf_should_confirm and self.c.dynamic_level_while_waiting:
            if self.wait_long and self.last_swing_high is not None and self.last_swing_high != self.long_level:
                self.long_level = (
                    self.last_swing_high
                    if self.c.dyn_update_mode == "ANY" or self.long_level is None
                    else max(self.long_level, self.last_swing_high)
                )
                long_level_updated = True
            if self.wait_short and self.last_swing_low is not None and self.last_swing_low != self.short_level:
                self.short_level = (
                    self.last_swing_low
                    if self.c.dyn_update_mode == "ANY" or self.short_level is None
                    else min(self.short_level, self.last_swing_low)
                )
                short_level_updated = True
            if self.wait_long and long_level_updated and not _swing_ok_long(self.long_level, close, self.c.max_swing_distance_pct):
                self.wait_long = False
                self.long_level = None
                self.wait_long_start_bar = None
                self.wait_long_started = False
            if self.wait_short and short_level_updated and not _swing_ok_short(self.short_level, close, self.c.max_swing_distance_pct):
                self.wait_short = False
                self.short_level = None
                self.wait_short_start_bar = None
                self.wait_short_started = False

        if conf_should_confirm:
            if self.wait_long and self.wait_long_start_bar is not None and (i - self.wait_long_start_bar >= self.c.confirm_timeout_bars):
                self.wait_long = False
                self.long_level = None
                self.wait_long_start_bar = None
                self.wait_long_started = False
            if self.wait_short and self.wait_short_start_bar is not None and (i - self.wait_short_start_bar >= self.c.confirm_timeout_bars):
                self.wait_short = False
                self.short_level = None
                self.wait_short_start_bar = None
                self.wait_short_started = False

        long_break_level = None if self.long_level is None else self.long_level + self.mintick * self.c.break_buffer_ticks
        short_break_level = None if self.short_level is None else self.short_level - self.mintick * self.c.break_buffer_ticks
        long_age_ok = self.wait_long and self.wait_long_start_bar is not None and i > self.wait_long_start_bar and (i - self.wait_long_start_bar >= self.c.min_wait_bars)
        short_age_ok = self.wait_short and self.wait_short_start_bar is not None and i > self.wait_short_start_bar and (i - self.wait_short_start_bar >= self.c.min_wait_bars)

        long_break_raw = bool(long_break_level is not None and ((close > long_break_level) if self.c.require_close_beyond else (high > long_break_level)))
        short_break_raw = bool(short_break_level is not None and ((close < short_break_level) if self.c.require_close_beyond else (low < short_break_level)))
        allow_break_long = (not self.c.defer_break_on_level_update) or (not long_level_updated) or long_break_raw
        allow_break_short = (not self.c.defer_break_on_level_update) or (not short_level_updated) or short_break_raw

        break_long = conf_should_confirm and long_age_ok and (self.long_level is not None) and allow_break_long and long_break_raw
        break_short = conf_should_confirm and short_age_ok and (self.short_level is not None) and allow_break_short and short_break_raw

        if self.c.use_momentum:
            if self.c.momentum_mode == "ROC_1":
                roc1 = self._roc1.iloc[i]
                mom_long_ok = not pd.isna(roc1) and float(roc1) >= self.c.roc_min_pct
                mom_short_ok = not pd.isna(roc1) and float(roc1) <= (-self.c.roc_min_pct)
            else:
                atr_val = self._atr.iloc[i]
                body_ok = not pd.isna(atr_val) and abs(close - open_) >= float(atr_val) * self.c.mom_atr_mult
                mom_long_ok = body_ok and close > open_
                mom_short_ok = body_ok and close < open_
        else:
            mom_long_ok = True
            mom_short_ok = True

        long_confirmed = (break_long and mom_long_ok) if conf_should_confirm else bool(long_raw)
        short_confirmed = (break_short and mom_short_ok) if conf_should_confirm else bool(short_raw)

        if self.c.require_raw_still_true:
            long_confirmed = long_confirmed and bool(long_raw)
            short_confirmed = short_confirmed and bool(short_raw)

        long_pulse = long_confirmed and self.last_long_confirm_bar != i
        short_pulse = short_confirmed and self.last_short_confirm_bar != i
        if long_pulse:
            self.last_long_confirm_bar = i
        if short_pulse:
            self.last_short_confirm_bar = i

        if conf_should_confirm and long_pulse:
            self._reset_waits()
        if conf_should_confirm and short_pulse:
            self._reset_waits()

        self.prev_long_raw = bool(long_raw)
        self.prev_short_raw = bool(short_raw)
        self.prev_enabled = bool(self.c.enabled)
        return ConfirmationStepResult(
            bool(long_pulse),
            bool(short_pulse),
            self.wait_long,
            self.wait_short,
            self.long_level,
            self.short_level,
            self.wait_long_start_bar,
            self.wait_short_start_bar,
            self.last_swing_high,
            self.last_swing_low,
        )

    def _reset_waits(self) -> None:
        self.wait_long = False
        self.wait_short = False
        self.long_level = None
        self.short_level = None
        self.wait_long_start_bar = None
        self.wait_short_start_bar = None
        self.wait_long_started = False
        self.wait_short_started = False
