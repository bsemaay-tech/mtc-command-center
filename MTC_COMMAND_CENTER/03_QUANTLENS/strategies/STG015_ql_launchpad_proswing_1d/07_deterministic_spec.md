# Deterministic Spec — Launchpad ProSwing 1D (QL_LAUNCHPAD_PROSWING_1D)

> Source: ProSwing launchpad intake. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name.

## Universe
- US equities (liquid growth stocks), 1D bars.
- ProSwing framework: early-stage breakout after multi-week base compression.

## Concept
The "launchpad" is a compact base (tight price range, drying volume) that forms after a prior
uptrend before the next leg up. Buy the initial breakout from the launchpad base — before
full VCP or breakout criteria are met — for earlier exposure with tight risk.

## Indicators
```
atr = ATR(14)
volume_ma20 = SMA(volume, 20)

# Base compression: N-bar range is tight relative to ATR
base_range_pct = (highest(high, 20) - lowest(low, 20)) / close × 100
compact = base_range_pct <= 15.0              # price range < 15% over 20 bars

# Volume drying
vol_drying = volume < volume_ma20 × 0.7      # volume 30% below average

# Breakout: close above the base high
base_high = highest(high, 20)[1]
breakout  = close > base_high
```

## Signal definition (long only)
```
uptrend = close > SMA(close, 200)            # price above 200 SMA (in larger uptrend)

long_entry = uptrend
           AND compact                        # price was compressed
           AND vol_drying[1]                  # volume was drying
           AND breakout                       # closed above the base high
           AND volume > volume_ma20 × 1.3    # breakout on above-average volume
```
Short: none.

## Stop
`stop = lowest(low, 5)[1]` — lowest low of the 5-bar base exit period.

## Target
No fixed target. Trail with 10-bar EMA.

## Data requirements
- 1D OHLCV with volume
- Minimum 200 bars warmup

## Known risks
- Compact base can be forming in a downtrend — 200 SMA filter is essential.
- False breakouts on launchpad bases are common; volume confirmation reduces (but doesn't eliminate) them.
- 15% range threshold is heuristic; may need symbol-specific calibration.

## Disposition
Parity candidate. Not approved for live trading.
