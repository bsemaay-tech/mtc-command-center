from __future__ import annotations

from collections import deque
import math
from typing import Deque

from mtc_v2.core.indicators import IndicatorSnapshot, SupertrendIndicatorSnapshot
from mtc_v2.core.types import Bar, RawSignal


REASON_ST_WARMUP = "st_warmup"
REASON_ST_DIRECTION_INIT = "st_direction_init"
REASON_ST_HOLD_LONG = "st_hold_long"
REASON_ST_HOLD_SHORT = "st_hold_short"
REASON_ST_FLIP_LONG = "st_flip_long"
REASON_ST_FLIP_SHORT = "st_flip_short"
REASON_ST_INVALID_BAR = "st_invalid_bar"
REASON_ST_HA_NOT_SUPPORTED = "st_ha_not_supported"


class SupertrendSignal:
    """Parity-first Supertrend raw pulse producer with deterministic warmup."""

    def __init__(self, config: dict[str, object]) -> None:
        self.config = config
        self.atr_len = int(config.get("st_atr_len", 21))
        self.factor = float(config.get("st_factor", 4.0))
        self.use_wicks = bool(config.get("st_use_wicks", False))
        self.use_ha = bool(config.get("st_use_ha", False))

        if self.atr_len < 1:
            raise ValueError("st_atr_len must be >= 1")
        if self.factor <= 0.0:
            raise ValueError("st_factor must be > 0")

        self._trs: Deque[float] = deque(maxlen=self.atr_len)
        self._reset_runtime_state()

    @property
    def warmup_bars_required(self) -> int:
        # Warmup consumes atr_len TR values; bar 0 uses high-low when prev_close is absent.
        return self.atr_len

    def calculate(self, bar: Bar) -> RawSignal:
        if self.use_ha:
            self._reset_runtime_state()
            self._set_indicator_snapshot(valid_bar=False, warmup_ready=False)
            return self._signal(False, False, REASON_ST_HA_NOT_SUPPORTED)

        if not self._is_valid_bar(bar):
            self._set_indicator_snapshot(
                atr=self._prev_atr,
                upper_band=self._prev_upper_band,
                lower_band=self._prev_lower_band,
                line=self._last_line,
                direction=self._last_direction,
                valid_bar=False,
                warmup_ready=self._last_direction is not None,
            )
            return self._signal(False, False, REASON_ST_INVALID_BAR)

        tr = self._true_range(bar.high, bar.low)
        self._trs.append(tr)

        if len(self._trs) < self.atr_len:
            self._prev_close = bar.close
            self._set_indicator_snapshot(valid_bar=True, warmup_ready=False)
            return self._signal(False, False, REASON_ST_WARMUP)

        atr = self._next_atr(tr)
        basis = (bar.high + bar.low) / 2.0
        basic_upper = basis + (self.factor * atr)
        basic_lower = basis - (self.factor * atr)
        upper_band = self._next_upper_band(basic_upper)
        lower_band = self._next_lower_band(basic_lower)

        previous_direction = self._prev_direction
        high_eff = bar.high if self.use_wicks else bar.close
        low_eff = bar.low if self.use_wicks else bar.close

        if previous_direction is None:
            direction = 1
            long_raw = False
            short_raw = False
            reason = REASON_ST_DIRECTION_INIT
        elif previous_direction < 0 and self._prev_upper_band is not None and high_eff > self._prev_upper_band:
            direction = 1
            long_raw = True
            short_raw = False
            reason = REASON_ST_FLIP_LONG
        elif previous_direction > 0 and self._prev_lower_band is not None and low_eff < self._prev_lower_band:
            direction = -1
            long_raw = False
            short_raw = True
            reason = REASON_ST_FLIP_SHORT
        else:
            direction = previous_direction
            long_raw = False
            short_raw = False
            reason = REASON_ST_HOLD_LONG if direction > 0 else REASON_ST_HOLD_SHORT

        self._commit_state(
            atr=atr,
            upper_band=upper_band,
            lower_band=lower_band,
            direction=direction,
            close=bar.close,
        )
        self._set_indicator_snapshot(
            atr=atr,
            upper_band=upper_band,
            lower_band=lower_band,
            line=self._last_line,
            direction=self._last_direction,
            valid_bar=True,
            warmup_ready=True,
        )
        return self._signal(long_raw, short_raw, reason)

    def _true_range(self, high: float, low: float) -> float:
        if self._prev_close is None:
            # Pine-equivalent bootstrap: first TR falls back to the raw high-low range.
            return high - low
        return max(high - low, abs(high - self._prev_close), abs(low - self._prev_close))

    def _next_atr(self, tr: float) -> float:
        if self._prev_atr is None:
            return sum(self._trs) / float(self.atr_len)
        return ((self._prev_atr * float(self.atr_len - 1)) + tr) / float(self.atr_len)

    def _next_upper_band(self, basic_upper: float) -> float:
        if self._prev_upper_band is None or self._prev_close is None:
            return basic_upper
        if basic_upper < self._prev_upper_band or self._prev_close > self._prev_upper_band:
            return basic_upper
        return self._prev_upper_band

    def _next_lower_band(self, basic_lower: float) -> float:
        if self._prev_lower_band is None or self._prev_close is None:
            return basic_lower
        if basic_lower > self._prev_lower_band or self._prev_close < self._prev_lower_band:
            return basic_lower
        return self._prev_lower_band

    def _commit_state(
        self,
        *,
        atr: float,
        upper_band: float,
        lower_band: float,
        direction: int,
        close: float,
    ) -> None:
        self._last_line = lower_band if direction > 0 else upper_band
        self._last_direction = direction
        self._prev_atr = atr
        self._prev_upper_band = upper_band
        self._prev_lower_band = lower_band
        self._prev_direction = direction
        self._prev_close = close

    def _reset_runtime_state(self) -> None:
        self._trs.clear()
        self._prev_close: float | None = None
        self._prev_atr: float | None = None
        self._prev_upper_band: float | None = None
        self._prev_lower_band: float | None = None
        self._prev_direction: int | None = None
        self._last_line: float | None = None
        self._last_direction: int | None = None
        self._indicator_snapshot = IndicatorSnapshot()

    def _signal(self, long_raw: bool, short_raw: bool, reason: str) -> RawSignal:
        return RawSignal(
            long=long_raw,
            short=short_raw,
            reason=reason,
            direction=self._last_direction,
            line=self._last_line,
        )

    def indicator_snapshot(self) -> IndicatorSnapshot:
        return self._indicator_snapshot

    def _set_indicator_snapshot(
        self,
        *,
        atr: float | None = None,
        upper_band: float | None = None,
        lower_band: float | None = None,
        line: float | None = None,
        direction: int | None = None,
        valid_bar: bool,
        warmup_ready: bool,
    ) -> None:
        self._indicator_snapshot = IndicatorSnapshot(
            supertrend=SupertrendIndicatorSnapshot(
                atr=atr,
                upper_band=upper_band,
                lower_band=lower_band,
                line=line,
                direction=direction,
                valid_bar=valid_bar,
                warmup_ready=warmup_ready,
            )
        )

    @staticmethod
    def _is_valid_bar(bar: Bar) -> bool:
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
