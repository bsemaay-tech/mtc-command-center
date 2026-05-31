from __future__ import annotations

import math
from typing import Any

from mtc_v2.core.types import Bar, RawSignal


REASON_RF_INIT = "rf_init"
REASON_RF_HOLD = "rf_hold"
REASON_RF_FLIP_LONG = "rf_flip_long"
REASON_RF_FLIP_SHORT = "rf_flip_short"
REASON_RF_INVALID_BAR = "rf_invalid_bar"


class RangeFilterSignal:
    """Isolated Range Filter POC signal producer for feature parity only."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.range_size = float(config.get("rf_range", 1000.0))
        if self.range_size <= 0.0:
            raise ValueError("rf_range must be > 0")
        self._line: float | None = None
        self._direction = 0
        self._snapshot: dict[str, Any] = {}

    @property
    def warmup_bars_required(self) -> int:
        return 0

    def calculate(self, bar: Bar) -> RawSignal:
        if not self._is_valid_bar(bar):
            self._set_snapshot(bar.close if math.isfinite(bar.close) else None)
            return RawSignal(False, False, REASON_RF_INVALID_BAR, self._direction, self._line)

        if self._line is None:
            self._line = bar.close
            self._direction = 0
            self._set_snapshot(bar.close)
            return RawSignal(False, False, REASON_RF_INIT, self._direction, self._line)

        previous_direction = self._direction
        upper_band = self._line + self.range_size
        lower_band = self._line - self.range_size
        long_raw = False
        short_raw = False
        reason = REASON_RF_HOLD

        if previous_direction < 0 and bar.close > self._line:
            self._line = bar.close - self.range_size
            self._direction = 1
            long_raw = True
            reason = REASON_RF_FLIP_LONG
        elif previous_direction <= 0 and bar.close > upper_band:
            self._line = bar.close - self.range_size
            self._direction = 1
            long_raw = previous_direction != 1
            reason = REASON_RF_FLIP_LONG if long_raw else REASON_RF_HOLD
        elif previous_direction >= 0 and bar.close < self._line:
            self._line = bar.close + self.range_size
            self._direction = -1
            short_raw = previous_direction != -1
            reason = REASON_RF_FLIP_SHORT if short_raw else REASON_RF_HOLD
        elif previous_direction > 0 and bar.close > upper_band:
            self._line = bar.close - self.range_size
        elif previous_direction < 0 and bar.close < lower_band:
            self._line = bar.close + self.range_size

        self._set_snapshot(bar.close)
        return RawSignal(long_raw, short_raw, reason, self._direction, self._line)

    def indicator_snapshot(self) -> dict[str, Any]:
        return self._snapshot

    def _set_snapshot(self, source_price: float | None) -> None:
        self._snapshot = {
            "source_price": source_price,
            "filter_line": self._line,
            "upper_band": None if self._line is None else self._line + self.range_size,
            "lower_band": None if self._line is None else self._line - self.range_size,
            "direction": self._direction,
        }

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


def evaluate_range_filter(*args: Any, **kwargs: Any) -> None:
    raise NotImplementedError("Use RangeFilterSignal directly for isolated feature parity POC.")
