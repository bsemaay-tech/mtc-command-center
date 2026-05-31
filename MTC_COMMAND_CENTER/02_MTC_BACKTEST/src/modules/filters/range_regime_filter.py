"""
Range Regime Filter (ADX + Chop + hold bars).
"""

from typing import Dict, Tuple

import pandas as pd

from .base import FilterPlugin
from ...engine.indicators import adx, choppiness


class RangeRegimeFilter(FilterPlugin):
    """Allow trades when trend regime is active, with hold-bar smoothing."""

    def __init__(
        self,
        enabled: bool = False,
        adx_on: float = 25.0,
        adx_off: float = 20.0,
        chop_on: float = 50.0,
        chop_off: float = 62.0,
        hold_bars: int = 8,
        agg_mode: str = "AND",
        min_pass: int = 2,
        adx_min: float | None = None,
        chop_max: float | None = None,
        adx_len: int = 14,
        chop_len: int = 14,
    ):
        if adx_min is not None:
            adx_off = float(adx_min)
            if adx_on == 25.0:
                adx_on = max(25.0, adx_off)
        if chop_max is not None:
            chop_off = float(chop_max)
            if chop_on == 50.0:
                chop_on = min(50.0, chop_off)

        super().__init__(
            name="Range_Regime_Filter",
            enabled=enabled,
            adx_on=adx_on,
            adx_off=adx_off,
            chop_on=chop_on,
            chop_off=chop_off,
            hold_bars=hold_bars,
            agg_mode=agg_mode,
            min_pass=min_pass,
            adx_len=adx_len,
            chop_len=chop_len,
        )
        self.adx_on = adx_on
        self.adx_off = adx_off
        self.chop_on = chop_on
        self.chop_off = chop_off
        self.hold_bars = max(0, int(hold_bars))
        self.agg_mode = str(agg_mode).upper()
        self.min_pass = max(1, int(min_pass))
        self.adx_len = max(1, int(adx_len))
        self.chop_len = max(1, int(chop_len))
        self._debug: Dict[str, pd.Series] = {}

    def apply(self, df: pd.DataFrame, **context) -> Tuple[pd.Series, pd.Series]:
        if not self.enabled:
            allow = pd.Series(True, index=df.index)
            return allow, allow

        adx_v = adx(df["high"], df["low"], df["close"], length=self.adx_len)
        chop_v = choppiness(df["high"], df["low"], df["close"], length=self.chop_len)
        adx_on_eff = max(float(self.adx_on), float(self.adx_off))
        adx_off_eff = min(float(self.adx_on), float(self.adx_off))
        chop_off_eff = max(float(self.chop_off), float(self.chop_on))
        chop_on_eff = min(float(self.chop_off), float(self.chop_on))

        # Pine parity state machine:
        # - Hysteresis on ADX/CHOP pass flags
        # - Hold bars are applied to BLOCKED regime, not pass regime
        adx_pass = True
        chop_pass = True
        range_blocked = False
        range_hold = 0

        idx = df.index
        allow_vals = pd.Series(True, index=idx, dtype=bool)
        raw_regime_ok_vals = pd.Series(True, index=idx, dtype=bool)
        held_regime_ok_vals = pd.Series(True, index=idx, dtype=bool)
        blocked_vals = pd.Series(False, index=idx, dtype=bool)
        pass_count_vals = pd.Series(2, index=idx, dtype=int)

        for i in range(len(df)):
            a = adx_v.iloc[i]
            c = chop_v.iloc[i]
            inds_ok = pd.notna(a) and pd.notna(c)

            if inds_ok:
                if a > adx_on_eff:
                    adx_pass = True
                elif a < adx_off_eff:
                    adx_pass = False

                if c < chop_on_eff:
                    chop_pass = True
                elif c > chop_off_eff:
                    chop_pass = False

                pass_count = (1 if adx_pass else 0) + (1 if chop_pass else 0)
                active_count = 2
                # Pine parity: minPassEff = min(min_pass, max(1, activeCount))
                min_pass_eff = min(self.min_pass, max(1, active_count))
                if self.agg_mode == "COUNT":
                    trend_allowed = pass_count >= min_pass_eff
                else:
                    trend_allowed = pass_count == active_count
                raw_regime_ok_vals.iloc[i] = trend_allowed

                if not trend_allowed:
                    range_blocked = True
                    range_hold = self.hold_bars
                elif range_blocked:
                    if range_hold > 0:
                        range_hold -= 1
                        range_blocked = True
                    else:
                        range_blocked = False
            else:
                pass_count = (1 if adx_pass else 0) + (1 if chop_pass else 0)
                active_count = 2
                min_pass_eff = min(self.min_pass, max(1, active_count))
                if self.agg_mode == "COUNT":
                    raw_regime_ok_vals.iloc[i] = pass_count >= min_pass_eff
                else:
                    raw_regime_ok_vals.iloc[i] = pass_count == active_count

            blocked_vals.iloc[i] = range_blocked
            held_regime_ok_vals.iloc[i] = not range_blocked
            allow_vals.iloc[i] = not range_blocked
            pass_count_vals.iloc[i] = pass_count

        allow = allow_vals.fillna(True)
        self._debug = {
            "adx": adx_v,
            "chop": chop_v,
            "raw_regime_ok": raw_regime_ok_vals.astype(bool),
            "held_regime_ok": held_regime_ok_vals.astype(bool),
            "range_blocked": blocked_vals.astype(bool),
            "pass_count": pass_count_vals,
        }
        return allow, allow

    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        if not self._debug:
            self.apply(df)
        return self._debug.copy()
