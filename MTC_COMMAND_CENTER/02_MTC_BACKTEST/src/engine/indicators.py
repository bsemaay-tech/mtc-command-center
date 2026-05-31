"""
Technical Indicators Module.

All indicators match TradingView's ta.* functions for parity.
Uses pandas for vectorized calculations.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional


def sma(src: pd.Series, length: int) -> pd.Series:
    """
    Simple Moving Average.
    
    Matches TradingView: ta.sma(src, length)
    """
    return src.rolling(window=length, min_periods=length).mean()


def ema(src: pd.Series, length: int) -> pd.Series:
    """
    Exponential Moving Average.
    
    Matches TradingView: ta.ema(src, length)
    Uses the same alpha = 2/(length+1) formula.
    """
    return src.ewm(span=length, adjust=False).mean()


def rma(src: pd.Series, length: int) -> pd.Series:
    """
    Wilder's Moving Average (RMA).
    
    Matches TradingView: ta.rma(src, length)
    Pine-equivalent seed behavior:
    - First defined value is SMA(src, length)
    - Then recursive: alpha*src + (1-alpha)*prev, alpha=1/length
    """
    alpha = 1.0 / float(length)
    out = pd.Series(index=src.index, dtype=float)
    if length <= 0 or len(src) == 0:
        return out

    sma_seed = src.rolling(window=length, min_periods=length).mean()
    start_idx = sma_seed.first_valid_index()
    if start_idx is None:
        return out

    start_pos = src.index.get_loc(start_idx)

    # Use numpy arrays for the recursive loop (avoids pandas iloc overhead)
    vals = src.values
    result = out.values.copy()
    result[start_pos] = sma_seed.iloc[start_pos]

    for i in range(start_pos + 1, len(vals)):
        result[i] = alpha * vals[i] + (1.0 - alpha) * result[i - 1]

    return pd.Series(result, index=src.index)


def wma(src: pd.Series, length: int) -> pd.Series:
    """
    Weighted Moving Average.
    
    Matches TradingView: ta.wma(src, length)
    """
    weights = np.arange(1, length + 1)
    return src.rolling(window=length).apply(
        lambda x: np.dot(x, weights) / weights.sum(),
        raw=True
    )


def hma(src: pd.Series, length: int) -> pd.Series:
    """
    Hull Moving Average.
    
    Matches TradingView: ta.hma(src, length)
    HMA = WMA(2*WMA(src, length/2) - WMA(src, length), sqrt(length))
    """
    half_len = max(1, length // 2)
    sqrt_len = max(1, int(np.sqrt(length)))
    
    wma_half = wma(src, half_len)
    wma_full = wma(src, length)
    
    raw_hma = 2 * wma_half - wma_full
    return wma(raw_hma, sqrt_len)


def tr(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """
    True Range.
    
    Matches TradingView: ta.tr
    """
    prev_close = close.shift(1)
    
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    
    return pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)


def atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int) -> pd.Series:
    """
    Average True Range.
    
    Matches TradingView: ta.atr(length)
    Uses Wilder's smoothing (RMA).
    """
    true_range = tr(high, low, close)
    return rma(true_range, length)


def supertrend(
    open_: pd.Series,
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    atr_length: int = 21,
    factor: float = 4.0,
    use_wicks: bool = True
) -> Tuple[pd.Series, pd.Series]:
    """
    Supertrend Indicator (MTC parity implementation).
    
    Matches `LIB_Signal_Supertrend_Fix.f_supertrend_signal_src` logic used by
    MASTER_TEMPLATE_CORE. This is intentionally not a generic ta.supertrend clone:
    it includes doji handling and prior-bar wick-based band locking rules.
    
    Args:
        open_: Open prices (or HA open when HA mode is active)
        high: High prices
        low: Low prices
        close: Close prices
        atr_length: ATR period
        factor: ATR multiplier
        use_wicks: If True use high/low touches; else use close touches
        
    Returns:
        (supertrend_line, direction)
        direction: 1 for bullish (below price), -1 for bearish (above price)
    """
    atr_val = atr(high, low, close, atr_length)
    src = (high + low) / 2.0
    atr_scaled = factor * atr_val

    h_eff = high if use_wicks else close
    l_eff = low if use_wicks else close
    is_doji = (open_ == close) & (open_ == low) & (open_ == high)

    long_stop_raw = src - atr_scaled
    short_stop_raw = src + atr_scaled

    long_stop = pd.Series(index=close.index, dtype=float)
    short_stop = pd.Series(index=close.index, dtype=float)
    direction = pd.Series(index=close.index, dtype=int)
    supertrend_line = pd.Series(index=close.index, dtype=float)

    for i in range(len(close)):
        curr_long = long_stop_raw.iloc[i]
        prev_long = long_stop.iloc[i - 1] if i > 0 and not pd.isna(long_stop.iloc[i - 1]) else curr_long

        if curr_long > 0:
            if bool(is_doji.iloc[i]):
                long_stop.iloc[i] = prev_long
            else:
                prev_l_eff = l_eff.iloc[i - 1] if i > 0 else np.nan
                long_stop.iloc[i] = max(curr_long, prev_long) if (not pd.isna(prev_l_eff) and prev_l_eff > prev_long) else curr_long
        else:
            long_stop.iloc[i] = prev_long

        curr_short = short_stop_raw.iloc[i]
        prev_short = short_stop.iloc[i - 1] if i > 0 and not pd.isna(short_stop.iloc[i - 1]) else curr_short

        if curr_short > 0:
            if bool(is_doji.iloc[i]):
                short_stop.iloc[i] = prev_short
            else:
                prev_h_eff = h_eff.iloc[i - 1] if i > 0 else np.nan
                short_stop.iloc[i] = min(curr_short, prev_short) if (not pd.isna(prev_h_eff) and prev_h_eff < prev_short) else curr_short
        else:
            short_stop.iloc[i] = prev_short

    prev_dir = 1
    for i in range(len(close)):
        long_prev = long_stop.iloc[i - 1] if i > 0 and not pd.isna(long_stop.iloc[i - 1]) else long_stop.iloc[i]
        short_prev = short_stop.iloc[i - 1] if i > 0 and not pd.isna(short_stop.iloc[i - 1]) else short_stop.iloc[i]

        if prev_dir == -1 and h_eff.iloc[i] > short_prev:
            curr_dir = 1
        elif prev_dir == 1 and l_eff.iloc[i] < long_prev:
            curr_dir = -1
        else:
            curr_dir = prev_dir

        direction.iloc[i] = curr_dir
        supertrend_line.iloc[i] = long_stop.iloc[i] if curr_dir == 1 else short_stop.iloc[i]
        prev_dir = curr_dir

    return supertrend_line, direction


def adx(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14) -> pd.Series:
    """
    Average Directional Index.
    
    Matches TradingView: ta.adx(high, low, close, length)
    """
    # Calculate +DM and -DM
    up_move = high.diff()
    down_move = -low.diff()
    
    plus_dm = pd.Series(np.where(
        (up_move > down_move) & (up_move > 0),
        up_move,
        0
    ), index=high.index)
    
    minus_dm = pd.Series(np.where(
        (down_move > up_move) & (down_move > 0),
        down_move,
        0
    ), index=high.index)
    
    # Calculate smoothed +DM, -DM and TR
    tr_val = tr(high, low, close)
    
    smoothed_tr = rma(tr_val, length)
    smoothed_plus_dm = rma(plus_dm, length)
    smoothed_minus_dm = rma(minus_dm, length)
    
    # Calculate +DI and -DI
    plus_di = 100 * smoothed_plus_dm / smoothed_tr
    minus_di = 100 * smoothed_minus_dm / smoothed_tr
    
    # Calculate DX
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    
    # Calculate ADX (smoothed DX)
    adx_val = rma(dx, length)
    
    return adx_val


def choppiness(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14) -> pd.Series:
    """
    Choppiness Index.
    
    Measures market trendiness (low = trending, high = ranging).
    Values typically between 0-100, with 38.2 and 61.8 as key levels.
    """
    # Sum of ATR
    atr_sum = tr(high, low, close).rolling(window=length).sum()
    
    # Highest high and lowest low over period
    highest = high.rolling(window=length).max()
    lowest = low.rolling(window=length).min()
    
    # Choppiness formula
    chop = 100 * np.log10(atr_sum / (highest - lowest)) / np.log10(length)
    
    return chop


def rsi(src: pd.Series, length: int = 14) -> pd.Series:
    """
    Relative Strength Index.
    
    Matches TradingView: ta.rsi(src, length)
    """
    delta = src.diff()
    
    gains = delta.where(delta > 0, 0)
    losses = (-delta).where(delta < 0, 0)
    
    avg_gain = rma(gains, length)
    avg_loss = rma(losses, length)
    
    rs = avg_gain / avg_loss
    rsi_val = 100 - (100 / (1 + rs))
    
    return rsi_val


def bollinger_bands(
    src: pd.Series,
    length: int = 20,
    mult: float = 2.0
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Bollinger Bands.
    
    Matches TradingView: ta.bb(src, length, mult)
    
    Returns:
        (upper_band, middle_band, lower_band)
    """
    middle = sma(src, length)
    std = src.rolling(window=length).std()
    
    upper = middle + (mult * std)
    lower = middle - (mult * std)
    
    return upper, middle, lower


def heikin_ashi(
    open_: pd.Series,
    high: pd.Series,
    low: pd.Series,
    close: pd.Series
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Heikin Ashi candles.
    
    Matches TradingView: request.security(ticker.heikinashi(...))
    
    Returns:
        (ha_open, ha_high, ha_low, ha_close)
    """
    # HA Close
    ha_close = (open_ + high + low + close) / 4
    
    # HA Open (needs previous HA values)
    ha_open = pd.Series(index=open_.index, dtype=float)
    ha_open.iloc[0] = (open_.iloc[0] + close.iloc[0]) / 2
    
    for i in range(1, len(open_)):
        ha_open.iloc[i] = (ha_open.iloc[i-1] + ha_close.iloc[i-1]) / 2
    
    # HA High and Low
    ha_high = pd.concat([high, ha_open, ha_close], axis=1).max(axis=1)
    ha_low = pd.concat([low, ha_open, ha_close], axis=1).min(axis=1)
    
    return ha_open, ha_high, ha_low, ha_close


def ma(src: pd.Series, length: int, ma_type: str = "EMA") -> pd.Series:
    """
    Generic moving average selector.
    
    Args:
        src: Source series
        length: MA period
        ma_type: Type of MA (SMA, EMA, RMA, WMA, HMA, DEMA, TEMA, VWMA, KAMA)
        
    Returns:
        Moving average series
    """
    ma_type = ma_type.upper()
    
    if ma_type == "SMA":
        return sma(src, length)
    elif ma_type == "EMA":
        return ema(src, length)
    elif ma_type == "RMA":
        return rma(src, length)
    elif ma_type == "WMA":
        return wma(src, length)
    elif ma_type == "HMA":
        return hma(src, length)
    elif ma_type == "DEMA":
        e1 = ema(src, length)
        e2 = ema(e1, length)
        return 2.0 * e1 - e2
    elif ma_type == "TEMA":
        e1 = ema(src, length)
        e2 = ema(e1, length)
        e3 = ema(e2, length)
        return 3.0 * (e1 - e2) + e3
    elif ma_type == "VWMA":
        # Volume-aware VWMA is implemented at call sites where volume is available.
        # Fallback to SMA keeps this helper deterministic.
        return sma(src, length)
    elif ma_type == "KAMA":
        change = (src - src.shift(length)).abs()
        volatility = (src - src.shift(1)).abs().rolling(length, min_periods=length).sum()
        er = (change / volatility.replace(0, np.nan)).fillna(0.0)
        fast = 2.0 / (2 + 1)
        slow = 2.0 / (30 + 1)
        sc = (er * (fast - slow) + slow) ** 2
        out = pd.Series(index=src.index, dtype=float)
        if len(src) > 0:
            out.iloc[0] = src.iloc[0]
        for i in range(1, len(src)):
            prev = out.iloc[i - 1]
            out.iloc[i] = prev + sc.iloc[i] * (src.iloc[i] - prev)
        return out
    else:
        raise ValueError(f"Unknown MA type: {ma_type}")


def mcginley_dynamic(
    src: pd.Series,
    length: int = 20,
    k: float = 0.6,
    mintick: float = 1e-12,
) -> pd.Series:
    """
    McGinley Dynamic.

    Pine parity implementation for `LIB_MATH.f_mcginley()`:
    - seed with current source when previous value is undefined
    - floor denominator at 1.0
    - floor ratio at 0.001

    `k` is intentionally retained for backward-compatible call sites but is
    not used by the Pine implementation.
    """
    out = pd.Series(index=src.index, dtype=float)
    if len(src) == 0 or length <= 0:
        return out
    first_idx = src.first_valid_index()
    if first_idx is None:
        return out
    start = src.index.get_loc(first_idx)
    vals = src.values
    res = out.values.copy()
    res[start] = float(vals[start])
    tick = max(float(mintick), 1e-12)
    for i in range(start + 1, len(vals)):
        prev = float(res[i - 1])
        price = float(vals[i])
        mg_prev = price if np.isnan(prev) else prev
        ratio = max(price / max(mg_prev, tick), 0.001)
        denom = float(length) * (ratio ** 4)
        res[i] = mg_prev + ((price - mg_prev) / max(denom, 1.0))
    return pd.Series(res, index=src.index)


def volume_sma(volume: pd.Series, length: int) -> pd.Series:
    """Simple moving average of volume."""
    return sma(volume, length)


def atr_ratio(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    atr_length: int = 14,
    baseline_length: int = 100
) -> pd.Series:
    """
    ATR Ratio (current ATR / baseline ATR).
    
    Used for volatility floor filter.
    """
    current_atr = atr(high, low, close, atr_length)
    baseline_atr = sma(current_atr, baseline_length)
    
    return current_atr / baseline_atr
