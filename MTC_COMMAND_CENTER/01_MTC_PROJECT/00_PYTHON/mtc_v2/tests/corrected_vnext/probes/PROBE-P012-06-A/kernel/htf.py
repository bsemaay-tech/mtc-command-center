"""
HTF (Higher Time Frame) resampling and alignment utilities.

Architecture contract
---------------------
- LTF bars are resampled to HTF using pandas ``resample()``.
- Each LTF bar receives the **prior-closed** HTF bar's OHLCV values.
  This mirrors Pine's ``request.security(..., expr[1], barmerge.lookahead_off)``
  pattern: the ``[1]`` gives the prior-confirmed bar so there is no repaint.
- ``build_htf_lookup()`` pre-computes a dict: ltf_timestamp → htf_dict | None.
  ``None`` means the first HTF bar is still incomplete (warmup).
"""
from __future__ import annotations

import pandas as pd

# Maps Pine input.string timeframe values → pandas resample offset aliases
RESAMPLE_RULES: dict[str, str] = {
    "30":  "30min",
    "60":  "1h",
    "120": "2h",
    "240": "4h",
    "D":   "1D",
    "W":   "1W",
}

TF_DURATIONS: dict[str, pd.Timedelta] = {
    "30": pd.Timedelta(minutes=30),
    "60": pd.Timedelta(hours=1),
    "120": pd.Timedelta(hours=2),
    "240": pd.Timedelta(hours=4),
    "D": pd.Timedelta(days=1),
    "W": pd.Timedelta(weeks=1),
}


def _tf_to_pandas_rule(tf: str) -> str:
    if tf in RESAMPLE_RULES:
        return RESAMPLE_RULES[tf]
    raise ValueError(
        f"Unsupported HTF timeframe: {tf!r}. Supported: {sorted(RESAMPLE_RULES)}"
    )


def resample_ohlcv(df_ltf: pd.DataFrame, tf: str, chart_timezone: str | None = None) -> pd.DataFrame:
    """Resample LTF OHLCV DataFrame to the given HTF.

    Parameters
    ----------
    df_ltf : pd.DataFrame
        LTF bars with a UTC ``DatetimeIndex`` and columns
        ``open``, ``high``, ``low``, ``close``, ``volume``.
    tf : str
        Pine-style timeframe string (e.g. ``"240"`` for 4 h).

    Returns
    -------
    pd.DataFrame
        HTF bars; the bar timestamp is the open of the first LTF bar
        in the window (``label="left"``).  Incomplete trailing bars are
        dropped via ``dropna()``.
    """
    rule = _tf_to_pandas_rule(tf)
    agg = {
        "open":   "first",
        "high":   "max",
        "low":    "min",
        "close":  "last",
        "volume": "sum",
    }
    # Timezone-aware daily/weekly resampling: TradingView daily/weekly bars are anchored to chart timezone.
    if tf in {"D", "W"} and chart_timezone:
        from datetime import timezone as _tz, timedelta as _td
        tzlabel = str(chart_timezone).strip()
        def _parse_tz(label: str):
            up = label.upper()
            if up.startswith("UTC"):
                sign = 1
                rest = up[3:]
                if rest.startswith("+"): sign = 1; rest = rest[1:]
                elif rest.startswith("-"): sign = -1; rest = rest[1:]
                if ":" in rest:
                    hh, mm = rest.split(":", 1)
                    return _tz(_td(hours=sign*int(hh), minutes=sign*int(mm)))
                if rest:
                    return _tz(_td(hours=sign*int(rest)))
                return _tz.utc
            if up.startswith("+") or up.startswith("-"):
                sign = 1 if up[0]=="+" else -1
                rest = up[1:]
                if ":" in rest:
                    hh, mm = rest.split(":", 1)
                    return _tz(_td(hours=sign*int(hh), minutes=sign*int(mm)))
                return _tz(_td(hours=sign*int(rest)))
            return _tz.utc
        _target_tz = _parse_tz(tzlabel)
        _df_local = df_ltf.copy()
        if _df_local.index.tz is None:
            _df_local.index = _df_local.index.tz_localize("UTC")
        _df_local = _df_local.tz_convert(_target_tz)
        _df_htf_local = _df_local.resample(rule, label="left", closed="left").agg(agg).dropna()
        return _df_htf_local.tz_convert("UTC")
    return df_ltf.resample(rule, label="left", closed="left").agg(agg).dropna()


def align_htf_to_ltf(df_ltf: pd.DataFrame, df_htf: pd.DataFrame) -> pd.DataFrame:
    """For each LTF bar return the **prior-closed** HTF bar values.

    Implementation
    --------------
    1. Shift the HTF index forward by exactly one HTF period so that HTF bar
       *N*'s values first appear on the **first** LTF bar of the following HTF
       period. This mirrors Pine's
       ``request.security(..., close[1], barmerge.lookahead_off)`` timing,
       where the prior-confirmed HTF close becomes visible as soon as the new
       HTF bar starts.

       Example — 4 h HTF, 1 h LTF:
       shift = 4 h
       HTF bar [00:00–04:00) (label 00:00) → shifted label 04:00.
       merge_asof assigns its close to LTF bars 04:00 – 07:00, matching the
       prior-closed ``close[1]`` contract.

    2. ``merge_asof(direction='backward')`` assigns to each LTF bar the most
       recent shifted HTF label that is ≤ the LTF bar's timestamp.
    3. LTF bars before the first shifted label have no prior bar → ``NaN``.

    Columns returned
    ----------------
    ``htf_open``, ``htf_high``, ``htf_low``, ``htf_close``, ``htf_volume``
    (NaN where no prior HTF bar is complete).
    """
    if len(df_htf) < 2:
        # Not enough HTF bars to determine a period → all NaN
        empty_cols = {
            "htf_open": float("nan"),
            "htf_high": float("nan"),
            "htf_low":  float("nan"),
            "htf_close": float("nan"),
            "htf_volume": float("nan"),
        }
        return pd.DataFrame(empty_cols, index=df_ltf.index)

    htf_period = df_htf.index[1] - df_htf.index[0]

    df_htf_shifted = df_htf.copy()
    # For request.security(..., expr[1], lookahead_off), prior-closed HTF
    # values become available at the first LTF bar of the next HTF window.
    df_htf_shifted.index = df_htf_shifted.index + htf_period
    df_htf_shifted.columns = [f"htf_{c}" for c in df_htf_shifted.columns]

    ltf_times = df_ltf.index.to_frame(name="timestamp").reset_index(drop=True)
    htf_times = df_htf_shifted.reset_index(names="htf_ts")

    merged = pd.merge_asof(
        ltf_times,
        htf_times,
        left_on="timestamp",
        right_on="htf_ts",
        direction="backward",
    ).drop(columns=["htf_ts"])
    merged.index = df_ltf.index
    return merged.drop(columns=["timestamp"])


def build_htf_lookup(df_ltf: pd.DataFrame, tf: str, chart_timezone: str | None = None) -> dict[pd.Timestamp, dict | None]:
    """Pre-compute prior-closed HTF values for every LTF bar.

    Returns
    -------
    dict
        ``ltf_timestamp`` → ``{"open", "high", "low", "close", "volume"}``
        or ``None`` during the warmup period (first HTF bar not yet closed).
    """
    if len(df_ltf.index) >= 2:
        ltf_period = df_ltf.index[1] - df_ltf.index[0]
        requested_period = TF_DURATIONS[tf]
        if requested_period < ltf_period:
            return {ts: None for ts in df_ltf.index}

    df_htf = resample_ohlcv(df_ltf, tf, chart_timezone=chart_timezone)
    aligned = align_htf_to_ltf(df_ltf, df_htf)

    result: dict[pd.Timestamp, dict | None] = {}
    for ts, row in aligned.iterrows():
        htf_close = row.get("htf_close")
        if htf_close is None or (hasattr(htf_close, "__float__") and pd.isna(htf_close)):
            result[ts] = None
        else:
            result[ts] = {
                "open":   float(row["htf_open"]),
                "high":   float(row["htf_high"]),
                "low":    float(row["htf_low"]),
                "close":  float(htf_close),
                "volume": float(row["htf_volume"]),
            }
    return result
