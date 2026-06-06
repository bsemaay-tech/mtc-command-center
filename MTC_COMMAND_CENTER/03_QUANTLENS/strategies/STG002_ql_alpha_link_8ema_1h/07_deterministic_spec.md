# Deterministic Spec — LINK 8EMA Pullback + Trailing Exit (QL_ALPHA_LINK_8EMA_1H)

> Source: QL Alpha pipeline, promoted to parity. Verified parameters locked in
> `producer_spec.json`. No-repaint, no-lookahead confirmed.

## Universe
- LINKUSDT perpetual futures, 1h bars.
- Coverage verified: 2020-01-17 to 2026-04-27, 55 016 bars.

## Strategy family
8EMA pullback entry with EMA8 trailing exit.

## Indicators
```
ema8       = EMA(close, 8)
atr14      = ATR(14, Wilder/RMA)
slope      = ema8 - ema8[3]                         # 3-bar slope
dist_atr   = abs(close - ema8) / atr14              # proximity to EMA in ATR units
impulse_atr = abs(close - close[3]) / atr14         # prior bar's momentum in ATR units
```

## Signal definition
```
long_entry = (close > ema8)                          # price above EMA
           AND (slope > 0)                           # EMA rising
           AND (dist_atr <= 0.5)                     # close within 0.5 ATR of EMA (near-touch)
           AND (impulse_atr[1] >= 1.6)               # prior bar had strong impulse (pre-pullback move)
```
Short: none (long-only).

## Entry
Enter at **next bar open** after signal bar closes.

## Stop
`stop_price = lowest(low, 3)[1]` — lowest low of last 3 bars at signal bar.

## Exit
1. **Trailing EMA exit**: when `close < ema8`, exit at next bar open (no fixed target)
2. Hard stop: `low <= stop_price`
3. Force-exit after 96 bars (max_hold_bars)

## No-repaint / no-lookahead proof
- Signal evaluated on closed bar i, executed at open of bar i+1
- `impulse_atr[1]` uses prior bar — no forward reference
- Stop/exit checked intrabar on subsequent bars only

## Verified parameters (locked)
| Param | Value |
|---|---|
| pullback_atr | 0.5 |
| impulse_atr | 1.6 |
| slope_window | 3 |
| ema_len | 8 |
| atr_len | 14 |
| stop_lookback_bars | 3 |
| cost_bps_round_trip | 8.0 |
| max_hold_bars | 96 |

## Warmup
≥ 200 bars (EMA/ATR stability).

## Metrics (lockbox)
| Metric | Value |
|---|---|
| Return (compound) | +75.4% |
| Buy & Hold | -20.6% |
| Excess alpha | +96.0% |
| Profit factor | 2.038 |
| Trades | 121 |
| Max drawdown | -16.3% |
| Win rate | 35.5% |
| Expectancy | 0.34 R |
| Multi-window positive | 5/5 |

## Disposition
PROMOTED TO PARITY. Parity Pine: `LINK_8EMA_REVIEW.pine`. Not approved for live trading.
