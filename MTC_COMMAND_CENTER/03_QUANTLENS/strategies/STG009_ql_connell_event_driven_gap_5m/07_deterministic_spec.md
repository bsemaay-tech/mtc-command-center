# Deterministic Spec — Andrew Connell Event-Driven Gap 5m (QL_CONNELL_EVENT_DRIVEN_GAP_5M)

> Source: Andrew Connell event-driven gap intake (5m variant). Promoted to parity candidate
> in prior system. No active producer_spec.json. Spec reconstructed from strategy name.

## Universe
- US equities (individual stocks), 5m intraday bars.
- Same event-driven concept as STG008 but on intraday 5m for precise entry timing.

## Concept
After identifying a qualifying event-driven gap (STG008 criteria), refine entry timing on 5m:
wait for the first 30-60 minute opening range to form, then buy a breakout or pullback-to-support
entry with tighter stop.

## Signal definition (5m, reconstructed)
```
# Daily-level pre-filter (must already meet 1D gap criteria)
qualifying_gap = gap_pct >= 5 AND vol_ratio >= 2.0 AND holds_gain (from 1D bar)

# 5m intraday logic: Opening Range setup
or_high_5m = highest(high, first 6 × 5m bars)     # 30-min opening range high
or_low_5m  = lowest(low, first 6 × 5m bars)       # 30-min opening range low
session_avwap = VWAP(09:30 ET anchor)

# Entry: buy the 5m breakout above the opening range (confirmed hold of gap)
long_entry  = qualifying_gap
            AND (bar_index >= 6)                    # after OR formation
            AND (close > or_high_5m)               # breakout above OR
            AND (close > session_avwap)            # above AVWAP (gap holding)

# Alternative: buy first 5m pullback to session_avwap after gap
```

## Stop
`stop = or_low_5m` or `session_avwap × 0.99`.

## Target
Target = prior resistance level or 2×–3× stop distance.

## Data requirements
- 5m OHLCV with 09:30 ET session identification
- Prior-day close for gap calculation
- Qualifying gap flag from 1D analysis (pre-filter)

## Known risks
- Same as STG008 but faster execution risk.
- Opening range breakouts on gap days often fail without volume confirmation.
- Intraday execution requires direct-access platform.

## Disposition
Parity candidate (blocked by missing 5m data). Not approved for live trading. Refines
the 1D gap signal (STG008) with 5m timing.
