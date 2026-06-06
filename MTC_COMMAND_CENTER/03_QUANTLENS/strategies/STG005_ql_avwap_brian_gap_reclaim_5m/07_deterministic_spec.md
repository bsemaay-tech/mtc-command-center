# Deterministic Spec — Brian Shannon AVWAP Gap Reclaim 5m (QL_AVWAP_BRIAN_GAP_RECLAIM_5M)

> Source: Brian Shannon AVWAP methodology. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name and Shannon's framework.

## Universe
- US equities (liquid, large-cap preferred), 5m intraday bars.
- Requires 5m OHLCV with session timestamps and gap data.

## Concept
When a stock gaps up (or down) at the open, anchor a VWAP at the gap (prior close or
the opening print). Price reclaiming the gap AVWAP after initial selling is a long entry;
failure to reclaim is a short.

## Indicators
```
avwap_gap = VWAP anchored at the session open (or prior close)
           = cumulative(OHLC/4 × volume from first bar of day) / cumulative(volume from first bar)

prior_close = yesterday's closing price
gap_up      = open > prior_close × 1.005      # gaps more than 0.5%
```

## Signal definition (long entry — gap reclaim)
```
gap_condition    = gap_up AND (open > avwap_gap × 0.98)    # gapped above prior close
sold_off         = any(low <= prior_close) in first 30 min  # price sold back to fill range
reclaim_trigger  = close > avwap_gap                        # reclaim above AVWAP
volume_confirm   = volume > avg_5m_volume × 1.3             # elevated volume on reclaim

long_entry = gap_condition AND sold_off AND reclaim_trigger AND volume_confirm
```

## Stop
`stop = prior_close` — loss of gap-fill support level.

## Target
Next resistance level; or trail via session VWAP.

## Data requirements
- 5m OHLCV with session open identification
- Pre-market/prior close data for gap calculation
- Minimum: US equity with defined session open

## Known risks
- Gaps that fully fill and continue lower (gap-fill to downside) require different handling.
- Requires session-aware VWAP computation (resets each day).
- Cannot be tested on 24h crypto futures without session simulation.

## Disposition
Parity candidate (blocked by missing 5m intraday data in repo). Not approved for live trading.
