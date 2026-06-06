# Deterministic Spec — LTC RSI(5) Oversold Recovery (QL_ALPHA_LTC_RSI_OVERSOLD_1H)

> Source: QL Alpha pipeline. Verified parameters locked in `producer_spec.json`.
> No-repaint, no-lookahead confirmed.

## Universe
- LTCUSDT perpetual futures, 1h bars.
- Coverage verified: 2020-01-09 to 2026-04-27, 55 208 bars.

## Strategy family
RSI oversold recovery — mean reversion.

## Indicators
```
rsi5 = RSI(close, 5)    # Wilder method (EWM alpha = 1/5, min_periods = 5)
```

## Signal definition
```
long_entry = (rsi5[1] < 35)     # prior bar RSI was oversold
           AND (rsi5 >= 45)     # current bar RSI recovered above threshold
```
Short: none (long-only). No trend filter (pure mean reversion).

## Entry
Enter at **next bar open** after signal bar closes.

## Stop
`stop_price = lowest(low, 5)[1]` — lowest low of last 5 bars at signal bar.

## Exit
1. Fixed 2R target: `entry + 2 × (entry − stop_price)`
2. Hard stop: `low <= stop_price`
3. Force-exit after 96 bars (max_hold_bars)

## No-repaint / no-lookahead proof
- RSI computed on closed bars; `rsi5[1]` is prior bar value
- Signal on bar i, executed at open of bar i+1
- No intrabar dependencies

## Verified parameters (locked)
| Param | Value |
|---|---|
| rsi_len | 5 |
| oversold | 35 |
| recovery | 45 |
| stop_lookback_bars | 5 |
| target_R | 2.0 |
| cost_bps_round_trip | 8.0 |
| max_hold_bars | 96 |

## Warmup
≥ 50 bars (RSI(5) stability).

## Metrics (lockbox)
| Metric | Value |
|---|---|
| Return (compound) | +95.8% |
| Buy & Hold | -20.8% |
| Excess alpha | +116.7% |
| Profit factor | 1.23 |
| Trades | 329 |
| Max drawdown | -22.0% |
| Win rate | 38.0% |
| Expectancy | 0.11 R |
| Multi-window positive | 4/5 |
| WF folds positive | 1/3 |

Caveats: thin PF 1.23, low expectancy 0.11R, fold consistency only 1/3.

## Backtesting risks
- Low expectancy — very sensitive to slippage/fees.
- Walk-forward fold consistency only 1/3 — regime-dependent.
- BH-FDR survivor: false.

## Disposition
PROMOTE_TO_FORWARD_PAPER_TRADE (deferred parity; revisit after forward paper-trade).
Not approved for live trading.
