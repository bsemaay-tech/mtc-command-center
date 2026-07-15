"""Strategy protocol (abstract interface)."""

from __future__ import annotations

from typing import Protocol, Sequence

from bridge.engine.types import Bar, Position, Signal


class Strategy(Protocol):
    id: str
    warmup_bars: int

    def on_bar(
        self, bars: Sequence[Bar], position: Position | None
    ) -> Signal | None:
        ...

    def trail_level(
        self, bars: Sequence[Bar], position: Position
    ) -> float | None:
        ...
