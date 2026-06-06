# Deterministic Spec — Deepak Singhania Snapback to 50SMA Intraday (QL_DEEPAK_SNAPBACK_50SMA_INTRADAY)

> Source: Deepak Singhania snapback method. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name and Deepak's method.

## Universe
- US equities (growth stocks), intraday (15m or 30m bars).
- Best on stocks trending well above their 50 SMA.

## Concept
A trending stock pulls back sharply intraday to touch its 50-period SMA on the 15m/30m chart.
This snapback to key support in a strong uptrend is a tactical long entry with tight stop.

## Indicators
```
sma50_intraday = SMA(close, 50)      # on 15m or 30m bars
atr = ATR(14)
```

## Signal definition (long only)
```
# Daily-level trend filter (must confirm on daily first)
daily_trend = close_1d > SMA_1d(close, 200)      # daily: above 200 SMA

# Intraday: snapback to 50 SMA
touching_50 = (low <= sma50_intraday × 1.005)     # touched within 0.5%
reclaiming  = close > sma50_intraday              # bar closes above 50 SMA
volume_dry  = volume < SMA(volume, 20) × 0.7     # light volume on pullback (preferred)

long_entry = daily_trend AND touching_50[1] AND reclaiming AND volume_dry[1]
```

## Stop
`stop = lowest(low, 3)[1]` or `sma50_intraday × 0.995`.

## Target
Return to prior intraday high; or trail with 8-period EMA.

## Data requirements
- Intraday 15m or 30m OHLCV with session timestamps
- Daily OHLCV for trend filter
- Multi-timeframe data access

## Known risks
- 50 SMA on 15m can lag significantly for fast-moving stocks.
- Intraday pullbacks can accelerate below 50 SMA before reversing — "snap" is sharp.
- Not available in repo (no intraday data with session anchor).

## Disposition
Parity candidate (blocked by missing intraday data). Not approved for live trading.
