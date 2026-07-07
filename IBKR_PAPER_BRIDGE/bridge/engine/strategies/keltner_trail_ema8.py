"""Keltner channel breakout x EMA(8) trailing-stop strategy."""

from __future__ import annotations

from statistics import mean
from typing import Sequence

from bridge.engine.types import Bar, Position, Signal


class KeltnerTrailEma8:
    """Plumbing test subject only, not a promotion claim."""

    id: str = "keltner_trail_ema8"
    warmup_bars: int = 20
    kc_length: int = 20
    kc_mult: float = 2.0
    atr_length: int = 20
    trail_ema: int = 8

    def __init__(self, symbol: str = "BTC") -> None:
        self.symbol = symbol
        self._last_signal_direction: str | None = None

    def on_bar(
        self, bars: Sequence[Bar], position: Position | None
    ) -> Signal | None:
        if position is not None or len(bars) <= max(self.kc_length, self.atr_length):
            return None

        idx = len(bars) - 1
        prior = bars[idx - self.kc_length : idx]
        prior_tr = [
            self._true_range(bars[i], bars[i - 1].close if i > 0 else None)
            for i in range(idx - self.atr_length, idx)
        ]
        mid = mean(bar.close for bar in prior)
        atr = mean(prior_tr)
        upper = mid + self.kc_mult * atr
        lower = mid - self.kc_mult * atr
        current = bars[-1]

        direction: str | None = None
        if current.close > upper:
            direction = "LONG"
        elif current.close < lower:
            direction = "SHORT"

        if direction is None or direction == self._last_signal_direction:
            return None

        self._last_signal_direction = direction
        return Signal(
            ts=current.ts,
            symbol=self.symbol,
            direction=direction,
            reason=f"close {'above' if direction == 'LONG' else 'below'} keltner",
            ref_price=current.close,
            stop_loss=lower if direction == "LONG" else upper,
            take_profit=None,
        )

    def trail_level(
        self, bars: Sequence[Bar], position: Position
    ) -> float | None:
        """Return updated trailing stop level or None."""
        if len(bars) < self.trail_ema:
            return None
        closes = [bar.close for bar in bars[-self.trail_ema :]]
        return mean(closes)

    @staticmethod
    def _true_range(bar: Bar, prev_close: float | None) -> float:
        if prev_close is None:
            return bar.high - bar.low
        return max(bar.high - bar.low, abs(bar.high - prev_close), abs(bar.low - prev_close))
