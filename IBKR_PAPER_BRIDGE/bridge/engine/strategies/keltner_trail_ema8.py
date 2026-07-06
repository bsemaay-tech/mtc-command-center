"""Keltner channel breakout x EMA(8) trailing-stop strategy."""

from __future__ import annotations

from typing import Sequence

from bridge.engine.types import Bar, Position, Signal


class KeltnerTrailEma8:
    """Plumbing test subject only, not a promotion claim."""

    id: str = "keltner_trail_ema8"
    warmup_bars: int = 20

    def on_bar(
        self, bars: Sequence[Bar], position: Position | None
    ) -> Signal | None:
        """Return a signal or None. Placeholder always returns None."""
        return None

    def trail_level(
        self, bars: Sequence[Bar], position: Position
    ) -> float | None:
        """Return updated trailing stop level or None."""
        return None
