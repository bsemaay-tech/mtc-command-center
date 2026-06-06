# Deterministic Spec — Highest Volume Edge ProSwing 1D (QL_HIGHEST_VOLUME_EDGE_PROSWING_1D)

> Source: ProSwing / highest volume edge intake. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name.

## Universe
- US equities (liquid growth stocks), 1D bars.
- ProSwing framework: swing trade entries in institutional-quality trending stocks.

## Concept
Identify the "highest volume" days in a stock's recent history — these represent institutional
accumulation or distribution events. Buy on pullbacks to the price range of the highest-volume
accumulation days in an uptrend.

## Indicators
```
volume_ma20   = SMA(volume, 20)
volume_ma50   = SMA(volume, 50)
highest_vol_n = highest(volume, 50)                          # 50-bar highest volume
hv_day_close  = close where volume == highest_vol_n          # close on highest-vol day
hv_day_low    = low where volume == highest_vol_n            # low on highest-vol day
```

## Signal definition (long only)
```
# Trend filter: stock in uptrend
uptrend = (close > SMA(close, 50)) AND (SMA(close, 50) > SMA(close, 200))

# Support zone: near the highest-volume day's low (institutional support)
hv_support  = low >= hv_day_low × 0.98          # within 2% of HV day low
approaching = low <= (hv_day_close + hv_day_low) / 2   # midpoint support

# Pullback on lighter volume (no distribution)
vol_dry     = volume < volume_ma20

long_entry  = uptrend AND approaching[1] AND (close > hv_day_low) AND vol_dry[1]
```

## Stop
`stop = hv_day_low × 0.97` — 3% below the institutional anchor day low.

## Target
Prior high or 2× stop distance.

## Data requirements
- 1D OHLCV with volume
- Minimum 50 bars (highest volume lookback)

## Known risks
- Highest volume within 50 bars can shift rapidly; the "anchor" level moves.
- Single-day volume events can be outliers (index rebalancing, etc.) — not always institutional.
- Long-only, bull-market dependent.

## Disposition
Parity candidate. Not approved for live trading. Strong conceptually; needs robust
highest-volume detection that filters outliers.
