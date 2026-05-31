from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean


@dataclass(frozen=True)
class SignalConfig:
    warmup_bars: int = 50
    vwap_guard_lookback: int = 8
    vwap_guard_ratio: float = 0.75
    slope_lookback: int = 12
    range_lookback: int = 20
    breakout_lookback: int = 10
    atr_lookback: int = 14
    volume_lookback: int = 20
    capitulation_volume_mult: float = 2.0
    capitulation_range_atr_mult: float = 1.5
    capitulation_vwap_distance_pct: float = 1.5
    compression_lookback: int = 20
    compression_width_pct: float = 1.2
    enable_long: bool = True
    enable_short: bool = True


REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def load_ohlcv_csv(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for column in REQUIRED_COLUMNS:
            if column not in row:
                raise ValueError(f"missing required column: {column}")
        for column in ["open", "high", "low", "close", "volume"]:
            row[column] = float(row[column])
    return rows


def write_csv(path: str | Path, rows: list[dict], fields: list[str]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _date_key(timestamp: str) -> str:
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return timestamp[:10]


def _slope(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return (values[-1] - values[0]) / max(1, len(values) - 1)


def _sma(values: list[float], index: int, lookback: int) -> float | None:
    if index + 1 < lookback:
        return None
    return mean(values[index - lookback + 1 : index + 1])


def _true_range(rows: list[dict], index: int) -> float:
    high = rows[index]["high"]
    low = rows[index]["low"]
    if index == 0:
        return high - low
    prev_close = rows[index - 1]["close"]
    return max(high - low, abs(high - prev_close), abs(low - prev_close))


def compute_signals(rows: list[dict], config: SignalConfig | None = None) -> list[dict]:
    cfg = config or SignalConfig()
    closes = [float(r["close"]) for r in rows]
    highs = [float(r["high"]) for r in rows]
    lows = [float(r["low"]) for r in rows]
    volumes = [float(r["volume"]) for r in rows]
    true_ranges = [_true_range(rows, i) for i in range(len(rows))]
    output: list[dict] = []
    current_session = None
    cumulative_pv = 0.0
    cumulative_volume = 0.0
    vwap_values: list[float] = []
    recent_down_capitulation = False
    recent_up_capitulation = False

    for i, row in enumerate(rows):
        session = _date_key(str(row["timestamp"]))
        if session != current_session:
            current_session = session
            cumulative_pv = 0.0
            cumulative_volume = 0.0
        typical = (row["high"] + row["low"] + row["close"]) / 3.0
        cumulative_pv += typical * row["volume"]
        cumulative_volume += row["volume"]
        vwap = cumulative_pv / cumulative_volume if cumulative_volume else row["close"]
        vwap_values.append(vwap)

        atr = _sma(true_ranges, i, cfg.atr_lookback)
        volume_ma = _sma(volumes, i, cfg.volume_lookback)
        close_slope = _slope(closes[max(0, i - cfg.slope_lookback + 1) : i + 1])
        vwap_slope = _slope(vwap_values[max(0, i - cfg.slope_lookback + 1) : i + 1])
        below_ratio = 0.0
        above_ratio = 0.0
        if i + 1 >= cfg.vwap_guard_lookback:
            vw = vwap_values[i - cfg.vwap_guard_lookback + 1 : i + 1]
            cs = closes[i - cfg.vwap_guard_lookback + 1 : i + 1]
            below_ratio = sum(1 for c, v in zip(cs, vw) if c < v) / cfg.vwap_guard_lookback
            above_ratio = sum(1 for c, v in zip(cs, vw) if c > v) / cfg.vwap_guard_lookback
        steadily_below_vwap = below_ratio >= cfg.vwap_guard_ratio and vwap_slope <= 0
        steadily_above_vwap = above_ratio >= cfg.vwap_guard_ratio and vwap_slope >= 0
        range_width_pct = 999.0
        if i + 1 >= cfg.compression_lookback:
            recent_high = max(highs[i - cfg.compression_lookback + 1 : i + 1])
            recent_low = min(lows[i - cfg.compression_lookback + 1 : i + 1])
            range_width_pct = (recent_high - recent_low) / closes[i] * 100.0 if closes[i] else 999.0
        range_bound = range_width_pct <= cfg.compression_width_pct

        downside_capitulation = False
        upside_capitulation = False
        if atr and volume_ma and i > 0:
            dist_pct = abs(closes[i] - vwap) / vwap * 100.0 if vwap else 0.0
            wide_range = true_ranges[i] >= atr * cfg.capitulation_range_atr_mult
            high_volume = volumes[i] >= volume_ma * cfg.capitulation_volume_mult
            downside_capitulation = closes[i] < vwap and wide_range and high_volume and dist_pct >= cfg.capitulation_vwap_distance_pct
            upside_capitulation = closes[i] > vwap and wide_range and high_volume and dist_pct >= cfg.capitulation_vwap_distance_pct
        if downside_capitulation:
            recent_down_capitulation = True
        if upside_capitulation:
            recent_up_capitulation = True

        range_high = max(highs[max(0, i - cfg.breakout_lookback) : i]) if i > 0 else highs[i]
        range_low = min(lows[max(0, i - cfg.breakout_lookback) : i]) if i > 0 else lows[i]
        trend_continuation_long = closes[i] > vwap and vwap_slope >= 0 and close_slope > 0 and closes[i] > range_high and not range_bound
        trend_continuation_short = closes[i] < vwap and vwap_slope <= 0 and close_slope < 0 and closes[i] < range_low and not range_bound
        right_side_v_long = i > 0 and recent_down_capitulation and highs[i] > highs[i - 1] and closes[i] > highs[i - 1]
        right_side_v_short = i > 0 and recent_up_capitulation and lows[i] < lows[i - 1] and closes[i] < lows[i - 1]

        long_rejected_by_vwap = steadily_below_vwap and not downside_capitulation and not recent_down_capitulation
        short_rejected_by_vwap = steadily_above_vwap and not upside_capitulation and not recent_up_capitulation
        long_pulse = bool(cfg.enable_long and i >= cfg.warmup_bars and not long_rejected_by_vwap and (trend_continuation_long or right_side_v_long))
        short_pulse = bool(cfg.enable_short and i >= cfg.warmup_bars and not short_rejected_by_vwap and (trend_continuation_short or right_side_v_short))
        if long_pulse:
            recent_down_capitulation = False
        if short_pulse:
            recent_up_capitulation = False

        output.append(
            {
                "timestamp": row["timestamp"],
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": row["volume"],
                "session_vwap": round(vwap, 6),
                "close_slope": round(close_slope, 6),
                "vwap_slope": round(vwap_slope, 6),
                "below_vwap_ratio": round(below_ratio, 4),
                "above_vwap_ratio": round(above_ratio, 4),
                "range_width_pct": round(range_width_pct, 6),
                "range_bound": range_bound,
                "downside_capitulation": downside_capitulation,
                "upside_capitulation": upside_capitulation,
                "trend_continuation_long": trend_continuation_long,
                "trend_continuation_short": trend_continuation_short,
                "right_side_v_long": right_side_v_long,
                "right_side_v_short": right_side_v_short,
                "long_rejected_by_vwap": long_rejected_by_vwap,
                "short_rejected_by_vwap": short_rejected_by_vwap,
                "raw_long_pulse": long_pulse,
                "raw_short_pulse": short_pulse,
                "initial_stop_long": min(lows[i], lows[i - 1]) if long_pulse and i > 0 else "",
                "initial_stop_short": max(highs[i], highs[i - 1]) if short_pulse and i > 0 else "",
            }
        )
    return output


SIGNAL_FIELDS = [
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "session_vwap",
    "close_slope",
    "vwap_slope",
    "below_vwap_ratio",
    "above_vwap_ratio",
    "range_width_pct",
    "range_bound",
    "downside_capitulation",
    "upside_capitulation",
    "trend_continuation_long",
    "trend_continuation_short",
    "right_side_v_long",
    "right_side_v_short",
    "long_rejected_by_vwap",
    "short_rejected_by_vwap",
    "raw_long_pulse",
    "raw_short_pulse",
    "initial_stop_long",
    "initial_stop_short",
]
