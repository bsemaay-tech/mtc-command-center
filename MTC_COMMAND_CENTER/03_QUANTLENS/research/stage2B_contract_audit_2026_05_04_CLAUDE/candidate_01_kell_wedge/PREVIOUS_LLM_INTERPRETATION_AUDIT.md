# PREVIOUS_LLM_INTERPRETATION_AUDIT — Kell Wedge Pop

## What Codex/previous LLM actually coded
File: `06_QUANTLENS_LAB/research/strategy_batch_2026_05_03/run_batch.py` → `signal_kell()`.

```
trend         = close > EMA20
mini_base     = (high.rolling(5).max() - low.rolling(5).min()) / close*100 <= 8
long_entry    = trend & mini_base.shift(1) & (close > high.rolling(5).max().shift(1))
exit_long     = close < EMA20
stop          = ATR_2 default; or rolling-5 low
target        = close + 3*(close-stop)
```

Variants: `wedge_pop`, `ema_crossback`, `basin_break`, default.

## Comparison to source idea

| Source requirement | Coded? | Notes |
|---|---|---|
| Pre-flush / reversal extension | NO | Completely missing. Strategy fires on any uptrend + tight 5-bar range + Donchian-5 break. |
| Snapback to 10/20EMA after flush | NO | Not modelled. |
| Higher-low pivot confirmed | NO | No swing-low logic at all. |
| Contraction defined as ATR percentile drop | PARTIAL | Approximated as `range/close <= 8%`, only one bar lookback, no percentile context. |
| Mini-base duration ≥ 3 bars (ideally with at least one inside-day) | PARTIAL | Implicit via 5-bar window only. |
| Multi-TF: weekly+daily+intraday confirmation | NO | Single timeframe only. |
| Equity-leader / theme universe | NO | Tested on BTC/ETH/SOL/BNB/XRP only. |
| MA-ride exit logic with adaptive 10vs20 selection | NO | Simple `close < EMA20`. |

## Identified errors

- **Over-simplification (severe):** the cycle preconditions (flush → snapback → higher-low → contraction) are entirely dropped. What's left is "uptrend + Donchian-5 break".
- **Wrong market:** crypto majors substituted for equity leaders. Kell's edge is *stock selection plus cycle*, not "EMA breakout works on any liquid asset".
- **Missing filter:** no theme / leadership / RS-vs-benchmark filter.
- **Missing context:** no pre-flush requirement → buys breakouts in already-extended trends, exactly what Kell warns against.
- **Discretionary component falsely mechanized:** "tight mini base" became `range/close <= 8%`, with no parameter from Kell's framework justifying 8.
- **Strategy degraded into simple breakout:** the resulting backtest is essentially a 5-bar Donchian with EMA20 trend gate. Stage2 metrics for this likely measure the breakout baseline, not Kell's edge.

## Classification
**MATERIAL_MISINTERPRETATION** (borderline NOT_THE_SAME_STRATEGY for the `wedge_pop` variant on crypto).

Was the previous backtest fair? **NO.** Crypto-majors backtest of a degraded breakout proxy says nothing about Kell's actual equity edge. Stage 2 weak/loss results should not be used to reject Kell.
