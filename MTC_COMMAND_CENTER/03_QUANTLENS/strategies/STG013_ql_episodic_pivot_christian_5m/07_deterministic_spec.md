# Deterministic Spec — Christian Flanders Episodic Pivot 5m (QL_EPISODIC_PIVOT_CHRISTIAN_5M)

> Source: Christian Flanders episodic pivot intake. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name and Christian's method.

## Universe
- US equities (individual stocks), 5m intraday bars.
- "Episodic pivot" = stocks that gap significantly on a positive catalyst (earnings beat, guidance raise, etc.).

## Concept
Christian Flanders' episodic pivot setup: when a stock gaps up 10%+ on earnings or a major
catalyst, buy the first 5m pullback to the session VWAP (or the gap support level) after the
initial open. The gap is the "pivot" event; the pullback is the entry.

## Indicators
```
session_vwap = VWAP anchored at 09:30 ET
or_low       = lowest(low, first 6 × 5m bars)     # 30-min opening range low
gap_pct      = (open - prior_close) / prior_close × 100
```

## Signal definition (long only)
```
# Pre-filter: must be an episodic event
episodic = gap_pct >= 10.0                          # 10%+ gap on catalyst

# Entry: first pullback to session VWAP / OR low after the gap
near_vwap = (low <= session_vwap × 1.01)            # touches session VWAP
reclaims  = close > session_vwap                    # closes back above VWAP
vol_ok    = volume > SMA(volume_5m, 20)            # above-average 5m volume

long_entry = episodic AND near_vwap[1] AND reclaims AND vol_ok
           AND (bar_index >= 6)                      # after opening range formation
```
Short: none.

## Stop
`stop = session_vwap × 0.99` or `or_low`.

## Target
Gap high + 0.5× gap size; or 2× stop distance. Exit EOD if not hit.

## Data requirements
- 5m OHLCV with 09:30 ET session identification and VWAP calculation
- Prior-day close for gap calculation
- Catalyst/earnings calendar (optional filter)

## Known risks
- Opening VWAP pulls up fast on a gap day — may not be touched at all.
- Aggressive episodic pivots can reverse on sell-the-news; size conservatively.
- Not testable in repo (no 5m intraday data with session anchor).

## Disposition
Parity candidate (blocked by missing 5m data). Not approved for live trading.
