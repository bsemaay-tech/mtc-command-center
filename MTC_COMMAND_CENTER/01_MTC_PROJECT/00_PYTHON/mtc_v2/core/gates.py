from __future__ import annotations

import math
from datetime import time as _time
from typing import TYPE_CHECKING

from mtc_v2.core.types import GateResult

if TYPE_CHECKING:
    from mtc_v2.core.ma import HtfMovingAverageTracker
    from mtc_v2.core.types import HtfSnapshot


GATE_MA_FILTER = "ma_filter"
GATE_MA_SLOPE_FILTER = "ma_slope_filter"
GATE_MCGINLEY_FILTER = "mcginley_filter"
GATE_VOLUME_FILTER = "volume_filter"
GATE_ADX_FILTER = "adx_filter"
GATE_CHOP_FILTER = "chop_filter"
GATE_ATR_VOL_FLOOR = "atr_vol_floor"
GATE_MACD_REGIME = "macd_regime"
GATE_MACD_CROSS = "macd_cross"
GATE_MACD_HIST = "macd_hist"
GATE_MACD_ZERO_DIST = "macd_zero_dist"


def evaluate_ma_filter(
    config: dict[str, object],
    *,
    close: float,
    ma_line: float | None,
) -> GateResult:
    if not bool(config.get("use_ma_filter", False)) or ma_line is None:
        return GateResult(gate_name=GATE_MA_FILTER, long_ok=True, short_ok=True, value=ma_line)
    return GateResult(
        gate_name=GATE_MA_FILTER,
        long_ok=float(close) > float(ma_line),
        short_ok=float(close) < float(ma_line),
        value=float(ma_line),
    )


def evaluate_ma_slope_filter(
    config: dict[str, object],
    *,
    ma_line: float | None,
    prev_ma_line: float | None,
) -> GateResult:
    if (
        not bool(config.get("use_ma_slope_filter", False))
        or ma_line is None
        or prev_ma_line is None
        or abs(float(prev_ma_line)) <= 1e-12
    ):
        return GateResult(gate_name=GATE_MA_SLOPE_FILTER, long_ok=True, short_ok=True, value=None)

    slope_ratio = (float(ma_line) - float(prev_ma_line)) / float(prev_ma_line)
    min_pct = float(config.get("ma_slope_min_pct", 0.0))
    return GateResult(
        gate_name=GATE_MA_SLOPE_FILTER,
        long_ok=slope_ratio > min_pct,
        short_ok=slope_ratio < -min_pct,
        value=slope_ratio,
    )


def evaluate_mcginley_filter(
    config: dict[str, object],
    *,
    close: float,
    mcginley_line: float | None,
) -> GateResult:
    """Gate: close > mcginley \u2192 long OK; close < mcginley \u2192 short OK."""
    if not bool(config.get("use_mcginley_filter", False)) or mcginley_line is None:
        return GateResult(
            gate_name=GATE_MCGINLEY_FILTER,
            long_ok=True,
            short_ok=True,
            value=mcginley_line,
        )
    return GateResult(
        gate_name=GATE_MCGINLEY_FILTER,
        long_ok=float(close) > float(mcginley_line),
        short_ok=float(close) < float(mcginley_line),
        value=float(mcginley_line),
    )


def evaluate_volume_filter(
    config: dict[str, object],
    *,
    volume: float,
    vol_sma: float | None,
) -> GateResult:
    """Gate: volume >= vol_sma * vol_mult \u2192 both directions OK."""
    if not bool(config.get("use_volume_filter", False)) or vol_sma is None:
        return GateResult(gate_name=GATE_VOLUME_FILTER, long_ok=True, short_ok=True, value=vol_sma)

    mult = float(config.get("vol_sma_mult", 1.0))
    threshold = float(vol_sma) * mult
    passes = float(volume) >= threshold
    return GateResult(
        gate_name=GATE_VOLUME_FILTER,
        long_ok=passes,
        short_ok=passes,
        value=float(volume) / float(vol_sma) if float(vol_sma) > 0 else None,
    )


def evaluate_adx_filter(
    config: dict[str, object],
    *,
    adx: float | None,
) -> GateResult:
    """Gate: ADX >= threshold \u2192 trend is strong enough for both directions."""
    if not bool(config.get("use_adx_filter", False)) or adx is None:
        return GateResult(gate_name=GATE_ADX_FILTER, long_ok=True, short_ok=True, value=adx)

    threshold = float(config.get("adx_threshold", 25.0))
    passes = float(adx) >= threshold
    return GateResult(
        gate_name=GATE_ADX_FILTER,
        long_ok=passes,
        short_ok=passes,
        value=float(adx),
    )


def evaluate_chop_filter(
    config: dict[str, object],
    *,
    chop: float | None,
) -> GateResult:
    """Gate: Choppiness Index < threshold \u2192 market is trending.

    Low choppiness = trending. High choppiness = ranging.
    Blocks both directions when market is too choppy.
    """
    if not bool(config.get("use_chop_filter", False)) or chop is None:
        return GateResult(gate_name=GATE_CHOP_FILTER, long_ok=True, short_ok=True, value=chop)

    threshold = float(config.get("chop_threshold", 61.8))
    passes = float(chop) < threshold
    return GateResult(
        gate_name=GATE_CHOP_FILTER,
        long_ok=passes,
        short_ok=passes,
        value=float(chop),
    )


def evaluate_atr_vol_floor(
    config: dict[str, object],
    *,
    atr: float | None,
    baseline_atr: float | None,
) -> GateResult:
    """Gate: ATR >= baseline_ATR * mult \u2192 volatility is sufficient.

    Blocks both directions when volatility is too low (compression zones).
    baseline_atr is a slow SMA of ATR used as the reference level.
    """
    if not bool(config.get("use_atr_vol_floor", False)) or atr is None or baseline_atr is None:
        return GateResult(gate_name=GATE_ATR_VOL_FLOOR, long_ok=True, short_ok=True, value=atr)

    mult = float(config.get("atr_vol_floor_mult", 0.5))
    threshold = float(baseline_atr) * mult
    passes = float(atr) >= threshold
    return GateResult(
        gate_name=GATE_ATR_VOL_FLOOR,
        long_ok=passes,
        short_ok=passes,
        value=float(atr) / float(baseline_atr) if float(baseline_atr) > 0 else None,
    )


def evaluate_macd_regime(
    config: dict[str, object],
    *,
    macd_line: float | None,
) -> GateResult:
    if not bool(config.get("use_macd_regime_filter", False)) or macd_line is None:
        return GateResult(gate_name=GATE_MACD_REGIME, long_ok=True, short_ok=True, value=macd_line)
    return GateResult(
        gate_name=GATE_MACD_REGIME,
        long_ok=float(macd_line) > 0.0,
        short_ok=float(macd_line) < 0.0,
        value=float(macd_line),
    )

def evaluate_macd_cross(
    config: dict[str, object],
    *,
    macd_line: float | None,
    macd_signal: float | None,
) -> GateResult:
    if not bool(config.get("use_macd_cross_filter", False)) or macd_line is None or macd_signal is None:
        return GateResult(gate_name=GATE_MACD_CROSS, long_ok=True, short_ok=True, value=macd_line)
    return GateResult(
        gate_name=GATE_MACD_CROSS,
        long_ok=float(macd_line) > float(macd_signal),
        short_ok=float(macd_line) < float(macd_signal),
        value=float(macd_line) - float(macd_signal),
    )

def evaluate_macd_hist(
    config: dict[str, object],
    *,
    macd_hist: float | None,
    prev_macd_hist: float | None,
) -> GateResult:
    if not bool(config.get("use_macd_hist_filter", False)) or macd_hist is None:
        return GateResult(gate_name=GATE_MACD_HIST, long_ok=True, short_ok=True, value=macd_hist)
    
    mode = str(config.get("macd_hist_mode", "POSITIVE"))
    h = float(macd_hist)
    ph = float(prev_macd_hist) if prev_macd_hist is not None else 0.0
    
    long_ok = True
    short_ok = True
    
    if mode == "POSITIVE":
        long_ok = h > 0.0
        short_ok = h < 0.0
    elif mode == "RISING":
        long_ok = h > ph
        short_ok = h < ph
    elif mode == "RISING_POSITIVE":
        long_ok = (h > 0.0) and (h > ph)
        short_ok = (h < 0.0) and (h < ph)
        
    return GateResult(
        gate_name=GATE_MACD_HIST,
        long_ok=long_ok,
        short_ok=short_ok,
        value=h,
    )

def evaluate_macd_zero_dist(
    config: dict[str, object],
    *,
    macd_line: float | None,
) -> GateResult:
    if not bool(config.get("use_macd_zero_dist_filter", False)) or macd_line is None:
        return GateResult(gate_name=GATE_MACD_ZERO_DIST, long_ok=True, short_ok=True, value=macd_line)

    dist = abs(float(macd_line))
    min_dist = float(config.get("macd_zero_dist_min", 0.0))
    passes = dist >= min_dist
    return GateResult(
        gate_name=GATE_MACD_ZERO_DIST,
        long_ok=passes,
        short_ok=passes,
        value=dist,
    )


GATE_CANDLE_PATTERN = "candle_pattern_gate"
GATE_LEVEL_PROXIMITY = "level_proximity_gate"


def _candle_pattern_single(
    bar_open: float,
    bar_high: float,
    bar_low: float,
    bar_close: float,
    prev_open: float,
    prev_close: float,
) -> tuple[bool, bool]:
    """Return (bullish, bearish) pattern booleans for a single bar pair."""
    curr_body = abs(bar_close - bar_open)
    curr_upper_wick = bar_high - max(bar_open, bar_close)
    curr_lower_wick = min(bar_open, bar_close) - bar_low

    bullish_engulf = (
        bar_open < prev_close
        and bar_close > prev_open
        and prev_close < prev_open
        and bar_close > bar_open
    )
    hammer = (
        curr_body > 0
        and curr_lower_wick > 2.0 * curr_body
        and curr_upper_wick < 0.5 * curr_body
        and bar_close > bar_open
    )
    bearish_engulf = (
        bar_open > prev_close
        and bar_close < prev_open
        and prev_close > prev_open
        and bar_close < bar_open
    )
    shooting_star = (
        curr_body > 0
        and curr_upper_wick > 2.0 * curr_body
        and curr_lower_wick < 0.5 * curr_body
        and bar_close < bar_open
    )
    return (bullish_engulf or hammer, bearish_engulf or shooting_star)


def evaluate_candle_pattern_gate(
    config: dict[str, object],
    *,
    recent_bars: "list",
) -> GateResult:
    if not bool(config.get("use_candle_pattern_gate", False)):
        return GateResult(gate_name=GATE_CANDLE_PATTERN, long_ok=True, short_ok=True)
    if len(recent_bars) < 2:
        return GateResult(gate_name=GATE_CANDLE_PATTERN, long_ok=True, short_ok=True)

    long_ok = False
    short_ok = False
    for i in range(1, len(recent_bars)):
        b = recent_bars[i]
        p = recent_bars[i - 1]
        bull, bear = _candle_pattern_single(
            float(b.open), float(b.high), float(b.low), float(b.close),
            float(p.open), float(p.close),
        )
        if bull:
            long_ok = True
        if bear:
            short_ok = True
        if long_ok and short_ok:
            break

    return GateResult(gate_name=GATE_CANDLE_PATTERN, long_ok=long_ok, short_ok=short_ok)


def evaluate_level_proximity_gate(
    config: dict[str, object],
    *,
    close: float,
    recent_highs: list[float],
    recent_lows: list[float],
) -> GateResult:
    if not bool(config.get("use_level_proximity_gate", False)):
        return GateResult(gate_name=GATE_LEVEL_PROXIMITY, long_ok=True, short_ok=True)
    if not recent_highs or not recent_lows:
        return GateResult(gate_name=GATE_LEVEL_PROXIMITY, long_ok=True, short_ok=True)

    threshold = float(config.get("level_proximity_threshold_pct", 0.5))
    swing_high = max(recent_highs)
    swing_low  = min(recent_lows)

    def near(level: float) -> bool:
        if level <= 0.0:
            return False
        return abs(close - level) / level * 100.0 <= threshold

    long_ok  = near(swing_low)
    short_ok = near(swing_high)
    return GateResult(gate_name=GATE_LEVEL_PROXIMITY, long_ok=long_ok, short_ok=short_ok)


# ---------------------------------------------------------------------------
# L12 — HTF Trend Filter
# ---------------------------------------------------------------------------

GATE_HTF_TREND = "htf_trend_filter"


def evaluate_htf_trend_filter(
    close: float,
    htf_snap: "HtfSnapshot",
    ma_type: str,
    ma_len: int,
    buffer_pct: float,
    _tracker: "HtfMovingAverageTracker | None" = None,
) -> GateResult:
    """HTF MA trend filter gate.

    Logic
    -----
    - If HTF snapshot is not ready (warmup): pass-through (both OK).
    - Determine MA value:
      * If ``_tracker`` is provided and ready, use ``_tracker.line``.
      * Otherwise fall back to ``htf_snap.close`` directly (covers unit tests
        and len-1 / no-warmup scenarios).
    - Long OK when  ``close > ma_val * (1 - buffer_pct/100)``
    - Short OK when ``close < ma_val * (1 + buffer_pct/100)``

    Mirrors Pine::

        htf_close_raw = request.security(..., close[1], barmerge.lookahead_off)
        close > htf_trend_line_state * (1 - htf_trend_buffer_pct/100)
    """
    _PASS = GateResult(gate_name=GATE_HTF_TREND, long_ok=True, short_ok=True,
                       value=None, category="filter")

    if not htf_snap.is_ready:
        return _PASS

    # Resolve MA value from tracker (stateful) or fall back to raw HTF close
    if _tracker is not None and _tracker.ready:
        ma_val = _tracker.line
    else:
        ma_val = htf_snap.close  # use raw HTF close (warmup / test convenience)

    if ma_val is None:
        return _PASS

    buf = buffer_pct / 100.0
    long_ok  = float(close) > float(ma_val) * (1.0 - buf)
    short_ok = float(close) < float(ma_val) * (1.0 + buf)
    return GateResult(
        gate_name=GATE_HTF_TREND,
        long_ok=bool(long_ok),
        short_ok=bool(short_ok),
        value=float(ma_val),
        category="filter",
    )


# ---------------------------------------------------------------------------
# L12 — MACD HTF Bias gate
# ---------------------------------------------------------------------------

GATE_MACD_HTF_BIAS = "macd_htf_bias"
GATE_MOMENTUM_FILTER = "momentum_filter"


def evaluate_macd_htf_bias(
    *,
    use_macd_htf_bias: bool,
    macd_htf_line: "float | None",
) -> "GateResult":
    """HTF MACD bias gate.

    When enabled, requires the HTF MACD line to be > 0 for long entries and
    < 0 for short entries.  Pass-through when disabled or HTF MACD not ready.

    Pine equivalent::
        bool l12_macd_htf_bias_long_ok  = not use_macd_htf_bias or na(macd_htf_line_state) or macd_htf_line_state > 0.0
        bool l12_macd_htf_bias_short_ok = not use_macd_htf_bias or na(macd_htf_line_state) or macd_htf_line_state < 0.0
    """
    _PASS = GateResult(gate_name=GATE_MACD_HTF_BIAS, long_ok=True, short_ok=True,
                       value=None, category="filter")
    if not use_macd_htf_bias or macd_htf_line is None:
        return _PASS
    return GateResult(
        gate_name=GATE_MACD_HTF_BIAS,
        long_ok=float(macd_htf_line) > 0.0,
        short_ok=float(macd_htf_line) < 0.0,
        value=float(macd_htf_line),
        category="filter",
    )


# ---------------------------------------------------------------------------
# L12 — Momentum Filter
# ---------------------------------------------------------------------------


def evaluate_momentum_filter(
    config: dict[str, object],
    *,
    bar_close: float,
    bar_open: float,
    prev_close: "float | None",
    momentum_atr: "float | None",
) -> "GateResult":
    """Gate: momentum filter — direction-agnostic.

    ATR_BODY mode: |close - open| >= atr * momentum_atr_mult
    ROC mode:      |close - prev_close| / prev_close * 100 >= momentum_roc_min_pct

    Pass-through when disabled or the required indicator is not yet ready.

    Pine equivalent::
        bool l12_momentum_ok =
            not use_momentum_filter or (
                momentum_mode == "ATR_BODY"
                    ? (na(momentum_atr_state) or math.abs(close - open) >= momentum_atr_state * momentum_atr_mult)
                    : (na(close[1]) or close[1] <= 0 or math.abs(close - close[1]) / close[1] * 100 >= momentum_roc_min_pct)
            )
    """
    _PASS = GateResult(gate_name=GATE_MOMENTUM_FILTER, long_ok=True, short_ok=True,
                       value=None, category="filter")
    if not bool(config.get("use_momentum_filter", False)):
        return _PASS

    mode = str(config.get("momentum_mode", "ATR_BODY"))

    if mode == "ATR_BODY":
        if momentum_atr is None:
            return _PASS
        body = abs(float(bar_close) - float(bar_open))
        mult = float(config.get("momentum_atr_mult", 0.30))
        passes = body >= float(momentum_atr) * mult
        value: float = body
    else:  # ROC
        if prev_close is None or abs(float(prev_close)) < 1e-12:
            return _PASS
        roc = abs(float(bar_close) - float(prev_close)) / abs(float(prev_close)) * 100.0
        min_pct = float(config.get("momentum_roc_min_pct", 0.15))
        passes = roc >= min_pct
        value = roc

    return GateResult(
        gate_name=GATE_MOMENTUM_FILTER,
        long_ok=passes,
        short_ok=passes,
        value=value,
        category="filter",
    )


# ---------------------------------------------------------------------------
# L12 — Session Filter
# ---------------------------------------------------------------------------

SESSION_DEFS: dict[str, dict[str, str]] = {
    "New York": {"start": "09:30", "end": "16:00", "tz": "America/New_York"},
    "London":   {"start": "08:00", "end": "16:30", "tz": "Europe/London"},
    "Asia":     {"start": "09:00", "end": "15:00", "tz": "Asia/Tokyo"},
    "Sydney":   {"start": "10:00", "end": "16:00", "tz": "Australia/Sydney"},
}

GATE_SESSION = "session_filter"


def _time_in_session(ts_utc: "datetime", start_str: str, end_str: str, tz_name: str) -> bool:
    """Return True if ``ts_utc`` falls within [start_str, end_str) in ``tz_name``."""
    import zoneinfo
    from datetime import timezone as _tz
    # Ensure the timestamp is timezone-aware UTC
    if ts_utc.tzinfo is None:
        import datetime as _dt
        ts_utc = ts_utc.replace(tzinfo=_tz.utc)
    from datetime import datetime as _datetime
    # Convert to target timezone
    zi = zoneinfo.ZoneInfo(tz_name)
    local_ts = ts_utc.astimezone(zi)
    t = local_ts.time().replace(tzinfo=None)
    h_s, m_s = int(start_str.split(":")[0]), int(start_str.split(":")[1])
    h_e, m_e = int(end_str.split(":")[0]), int(end_str.split(":")[1])
    s = _time(h_s, m_s)
    e = _time(h_e, m_e)
    if s <= e:
        return s <= t < e
    else:  # overnight crossing midnight
        return t >= s or t < e


def _parse_session_string(session_str: str) -> tuple[str, str, str]:
    """Parse a Pine-style session string 'HHMM-HHMM:Timezone' into (start, end, tz).

    Returns 24h clock strings like '09:30' and the timezone identifier.
    Falls back to 'UTC' if no timezone specified.
    """
    tz_name = "UTC"
    if ":" in session_str:
        parts = session_str.rsplit(":", 1)
        time_part = parts[0]
        tz_name = parts[1]
    else:
        time_part = session_str
    start_raw, end_raw = time_part.split("-")
    start = f"{start_raw[:2]}:{start_raw[2:]}"
    end = f"{end_raw[:2]}:{end_raw[2:]}"
    return start, end, tz_name


def evaluate_session_filter(
    config: dict[str, object],
    *,
    bar_timestamp: "datetime | None",
) -> "GateResult":
    """Gate: entry only allowed during configured trading session.

    Direction-agnostic — blocks both long and short outside the session.

    Pine equivalent::
        bool l12_session_ok = not use_session_filter
        if use_session_filter
            string _sess_str = (lookup or custom)
            l12_session_ok := not na(time(_sess_str))
    """
    _PASS = GateResult(gate_name=GATE_SESSION, long_ok=True, short_ok=True,
                       value=None, category="filter")
    if not bool(config.get("use_session_filter", False)):
        return _PASS
    if bar_timestamp is None:
        return _PASS

    session_name = str(config.get("session_name", "New York"))
    if session_name == "Custom":
        raw = str(config.get("session_custom_string", "0930-1600:UTC"))
        start, end, tz = _parse_session_string(raw)
    else:
        if session_name not in SESSION_DEFS:
            return _PASS  # unknown session → pass through
        defn = SESSION_DEFS[session_name]
        start, end, tz = defn["start"], defn["end"], defn["tz"]

    ok = _time_in_session(bar_timestamp, start, end, tz)
    return GateResult(
        gate_name=GATE_SESSION,
        long_ok=bool(ok),
        short_ok=bool(ok),
        value=1.0 if ok else 0.0,
        category="filter",
    )
