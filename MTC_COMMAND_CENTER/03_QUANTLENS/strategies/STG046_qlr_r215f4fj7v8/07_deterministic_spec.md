# Deterministic Spec — QLR R215f4fj7V8 VWAP Multi-Setup System (STG046)

> Source: Pine review script `standalone_pine_strategy_REVIEW.pine`. Research-only visual review.
> No MTC production integration. Not optimized.

## Universe
- Any liquid intraday market with session-based VWAP (stocks, futures, crypto with session filter).
- Primary timeframe: intraday (5m, 15m, 30m). Session filter optional (09:30–16:00 ET for stocks).

## Two entry setups

### Setup A: Trend Continuation Long
```
session_vwap = VWAP anchored at session open

# VWAP trend
above_ratio = SMA(close > session_vwap ? 1 : 0, N)      # fraction of last N bars above VWAP
vwap_slope  = positive (VWAP trending up)
close_slope = positive (price trending up)

# Range breakout
range_high = highest(high[1], breakout_lookback)         # excludes current bar

trend_continuation_long = (close > session_vwap)
                        AND (vwap_slope >= 0)
                        AND (close_slope > 0)
                        AND (close > range_high)          # closes above N-bar high
```

### Setup B: Right-Side V Reversal Long
```
# Capitulation: wide range bar, high volume, far from VWAP
wide_range = (high - low) >= atr × 1.6
high_volume = volume >= SMA(volume, 20) × 2.0
dist_pct   = abs(close - session_vwap) / session_vwap × 100
downside_capitulation = (close < session_vwap) AND wide_range AND high_volume AND (dist_pct >= 1.5%)

# Track prior capitulation (sticky state)
prior_downside_capitulation = True once downside_capitulation fires (resets on long entry)

# V reversal entry: price stopped falling, then resumes
price_stopped_falling = (close > close[1]) AND (low >= low[1])
right_side_v_long = prior_downside_capitulation
                  AND price_stopped_falling
                  AND (high > high[1] OR close > high[1])
```

### Suppression filters (VWAP guard, no-man's land)
```
# Suppress long if price is steadily below VWAP (no capitulation occurred)
steadily_below_vwap = (below_ratio >= 0.80) AND (vwap_slope <= 0)
long_rejected_by_vwap = steadily_below_vwap AND NOT prior_downside_capitulation

# No-man's land: choppy zone — suppress all signals
bb_width_pct   = 4 × stdev(close, 24) / sma(close, 24) × 100
recent_range   = (highest(high, 24) - lowest(low, 24)) / close × 100
near_vwap_ratio = SMA(abs(close - vwap) <= atr×0.35 ? 1 : 0, 24)
vwap_flat       = vwap_slope_pct <= 0.04%
low_compression = bb_width_pct <= 2.0 OR recent_range <= 1.4
no_mans_land   = (near_vwap_ratio >= 0.45 AND vwap_flat) OR (low_compression AND vwap_flat)
```

### Cooldown
Signal blocked if last same-direction signal was within `signal_cooldown_bars` (default 20 bars),
UNLESS an opposite direction signal fired in between (which resets the cooldown).

## Final entry signal
```
final_entry = (trend_continuation_long OR right_side_v_long)
            AND NOT long_rejected_by_vwap
            AND NOT no_mans_land
            AND NOT conflict (long AND short both fire)
            AND cooldown_ok
            AND barstate.isconfirmed
            AND (strategy.position_size == 0)   # one position at a time
```

## Stop options
- `prior_bar`: `min(low, low[1])`
- `ATR`: `close - exit_atr × stop_atr_mult` (default: ATR(14) × 1.5)
- `percent`: `close × (1 - stop_percent/100)`

## Target options
- `R_multiple`: `close + risk × tp_r_multiple` (default: 2R)
- `ATR`: `close + exit_atr × tp_atr_mult`
- `none`: no target (hold until stop or time exit)

## Time exit
`close position after max_bars_in_trade bars` (default: off, 0 = disabled)

## Key parameters (defaults)
| Param | Default |
|---|---|
| signal_cooldown_bars | 20 |
| warmup_bars | 50 |
| vwap_guard_lookback | 10 |
| vwap_guard_ratio | 0.80 |
| breakout_lookback | 12 |
| compression_lookback | 24 |
| bb_width_threshold_pct | 2.0% |
| capitulation_volume_mult | 2.0× |
| capitulation_range_atr_mult | 1.6× |
| capitulation_vwap_distance_pct | 1.5% |
| stop_mode | prior_bar |
| tp_r_multiple | 2.0 |

## Classification
Research-only visual review. Not backtested with walk-forward or multi-window statistics.

## Disposition
Research-only. CANDIDATE for further development. Requires proper multi-asset, multi-session
backtest with correct session-anchored VWAP before promotion. Not approved for live trading.
