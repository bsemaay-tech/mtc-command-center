from __future__ import annotations

from dataclasses import dataclass, field


INDICATOR_SUPERTREND = "supertrend"


@dataclass(slots=True, frozen=True)
class SupertrendIndicatorSnapshot:
    atr: float | None = None
    upper_band: float | None = None
    lower_band: float | None = None
    line: float | None = None
    direction: int | None = None
    valid_bar: bool = False
    warmup_ready: bool = False


@dataclass(slots=True, frozen=True)
class AtrStopIndicatorSnapshot:
    atr: float | None = None
    valid_bar: bool = False
    warmup_ready: bool = False


@dataclass(slots=True, frozen=True)
class AtrTakeProfitIndicatorSnapshot:
    atr: float | None = None
    valid_bar: bool = False
    warmup_ready: bool = False


@dataclass(slots=True, frozen=True)
class IndicatorSnapshot:
    supertrend: SupertrendIndicatorSnapshot = field(default_factory=SupertrendIndicatorSnapshot)
    atr_stop: AtrStopIndicatorSnapshot = field(default_factory=AtrStopIndicatorSnapshot)
    atr_tp: AtrTakeProfitIndicatorSnapshot = field(default_factory=AtrTakeProfitIndicatorSnapshot)
