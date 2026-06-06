# Deterministic Spec — ADA Two-Candle S/R Breakout (QL_ALPHA_ADA_TWO_CANDLE_SR_1H)

> Source: QL Alpha pipeline, promoted to parity. Verified parameters locked in
> `producer_spec.json`. No-repaint, no-lookahead confirmed.

## Universe
- ADAUSDT perpetual futures, 1h bars.
- Coverage verified: 2020-01-31 to 2026-04-27, 54 680 bars.

## Strategy family
Support/resistance breakout with strong close.

## Indicators
- `high_break = highest(high, 200)[1]` — rolling 200-bar high, shifted 1 (no lookahead)
- `atr14 = ATR(14)` — Wilder (RMA)
- `close_position = (close - low) / (high - low)` — close location within bar

## Signal definition
```
long_entry = (close_position >= 0.6)                   # close in upper third
           AND (close > high[1])                        # close above prior bar high
           AND (close > high_break + 0.0 * atr14)      # close above 200-bar breakout level
```
Short: none (long-only).

## Entry
Enter at **next bar open** after signal bar closes (bar_close_only = true).

## Stop
`stop_price = lowest(low, 2)[1]` — lowest low of last 2 bars at signal bar close.

## Exit
1. Fixed 2R target: `entry + 2 × (entry − stop_price)`
2. Hard stop: `low <= stop_price`
3. Force-exit after 96 bars (max_hold_bars)

## No-repaint / no-lookahead proof
- `high_break` shifted by 1 → excludes current bar
- `close_position` uses only current bar OHLC (closed)
- Signal on bar i, executed at bar i+1 open

## Verified parameters (locked)
| Param | Value |
|---|---|
| level_lookback | 200 |
| upper_third | 0.6 |
| break_buf_atr | 0.0 |
| atr_len | 14 |
| stop_lookback_bars | 2 |
| target_R | 2.0 |
| cost_bps_round_trip | 8.0 |
| max_hold_bars | 96 |

## Warmup
≥ 210 bars (200-bar lookback + ATR warmup).

## Metrics (lockbox)
| Metric | Value |
|---|---|
| Return (compound) | +79.2% |
| Buy & Hold | -30.5% |
| Excess alpha | +109.7% |
| Profit factor | 1.721 |
| Trades | 53 |
| Max drawdown | -14.2% |
| Win rate | 49.1% |
| Expectancy | 0.44 R |
| Multi-window positive | 4/5 |

Caveat: 53 trades is a thin sample; Q1 window +599% is a small-sample distortion.

## Backtesting risks
- Low trade count — do not over-optimize.
- BH-FDR survivor: false (did not survive BH correction).

## Disposition
PROMOTED TO PARITY. Parity Pine: `ADA_TWO_CANDLE_SR_REVIEW.pine`. Not approved for live trading.
