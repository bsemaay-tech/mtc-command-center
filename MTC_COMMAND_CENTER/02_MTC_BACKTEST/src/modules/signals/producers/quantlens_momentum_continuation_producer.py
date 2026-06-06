"""QuantLens momentum-continuation manual producer adapter."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.modules.signals.base import SignalPlugin


class QuantLensMomentumContinuationProducerAdapter(SignalPlugin):
    """Raw long producer for the QuantLens momentum-continuation family.

    Mirrors the entry side of ``QL_FAM_MOMENTUM_CONTINUATION`` from the
    QuantLens family-template runner. Stops and trade lifecycle decisions are
    intentionally excluded so the existing MTC risk engine owns them.
    """

    def __init__(
        self,
        mom_lb: int = 10,
        trend_ema: int = 50,
        breakout_lb: int = 10,
    ) -> None:
        super().__init__(
            name="producer_ql_fam_momentum_continuation",
            mom_lb=int(mom_lb),
            trend_ema=int(trend_ema),
            breakout_lb=int(breakout_lb),
        )
        ok, message = self.validate_params()
        if not ok:
            raise ValueError(message)

    @property
    def mom_lb(self) -> int:
        return int(self.params["mom_lb"])

    @property
    def trend_ema(self) -> int:
        return int(self.params["trend_ema"])

    @property
    def breakout_lb(self) -> int:
        return int(self.params["breakout_lb"])

    def generate(self, df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
        debug = self.get_debug_series(df)
        long_raw = debug["long_raw"].fillna(False).astype(bool)
        short_raw = pd.Series(False, index=df.index, dtype=bool)
        return long_raw, short_raw

    def get_debug_series(self, df: pd.DataFrame) -> dict[str, pd.Series]:
        missing = {"close", "high"} - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        close = pd.to_numeric(df["close"], errors="coerce")
        high = pd.to_numeric(df["high"], errors="coerce")

        trend_ema = close.ewm(span=self.trend_ema, adjust=False).mean()
        roc = close.pct_change(self.mom_lb)
        trend = close > trend_ema
        mom_ok = roc.shift(1) > 0
        chan_hi = high.rolling(self.breakout_lb, min_periods=2).max().shift(1)
        breakout = close > chan_hi
        long_raw = (trend & mom_ok & breakout).fillna(False).astype(bool)

        return {
            "trend_ema": trend_ema,
            "roc": roc,
            "chan_hi": chan_hi,
            "trend": trend.astype(bool),
            "mom_ok": mom_ok.fillna(False).astype(bool),
            "breakout": breakout.fillna(False).astype(bool),
            "long_raw": long_raw,
        }

    def validate_params(self) -> tuple[bool, str | None]:
        for key in ("mom_lb", "trend_ema", "breakout_lb"):
            value: Any = self.params.get(key)
            if not isinstance(value, int) or value <= 0:
                return False, f"{key} must be a positive integer"
        return True, None

