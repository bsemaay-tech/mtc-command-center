# DONCHIAN Cross-Sectional DSR — US-Equities 10m

**Date:** 2026-06-28
**Author:** Claude Opus 4.8
**Classification:** RESEARCH ONLY / NOT PROMOTABLE
**Data:** `native_us_equities_10m_alpaca_2026-06-28` (7 symbols, ~57.7k 10m bars each, ~6yr, adjusted, RTH)
**Strategy:** `GEN_DONCHIAN_BREAKOUT` (the lead from the 6yr sweep — positive OOS on 5/7 symbols)

## Question

The per-cell sweep showed DONCHIAN positive-OOS on 5/7 symbols but no single cell was DSR-robust (too few trades per cell for statistical power). Does **pooling OOS trades across all 7 symbols** — a much larger sample — confirm a real shared edge?

## Method (honest, engine code reused unmodified)

- Per symbol: train = first 75% bars, **lockbox/OOS = last 25%** (matches engine `LOCKBOX_FRACTION`).
- For each of the 60 DONCHIAN grid configs: apply to ALL 7 symbols, pool train R-series and pool OOS R-series.
- **Select ONE config** by best *pooled TRAIN* per-trade Sharpe (selection on train only — no OOS peeking).
- Evaluate that single shared config on the **pooled OOS** trades (all symbols combined).
- Deflate with the engine's own `deflated_sharpe_pvalue` (n_trials=60) + `bootstrap_p_positive`.

## Result

Selected config: `channel_len=150, atr_buf=0.1, stop_lookback=10` (best pooled train Sharpe).

**Pooled out-of-sample (all 7 symbols):**

| Metric | Value | Bar to clear |
|---|---|---|
| Trades | 488 | — |
| Mean R / trade | **+0.0298** | >0 |
| Win rate | 42.6% | — |
| Profit factor | **1.058** | — |
| Per-trade Sharpe | +0.0252 | — |
| Bootstrap p(mean ≤ 0) | **0.269** | < 0.05 |
| DSR confidence | **0.216** | ≥ 0.95 |
| DSR-robust? | **No** | — |

**Per-symbol OOS with the single shared config:**

| Symbol | Trades | Mean R | Win | PF |
|---|---|---|---|---|
| QQQ | 90 | **+0.188** | 0.478 | 1.39 |
| AAPL | 57 | **+0.188** | 0.491 | 1.45 |
| TSLA | 56 | +0.011 | 0.393 | 1.02 |
| NVDA | 71 | +0.005 | 0.394 | 1.01 |
| SPY | 87 | −0.001 | 0.402 | 1.00 |
| MSFT | 64 | **−0.109** | 0.406 | 0.80 |
| AMZN | 63 | **−0.111** | 0.413 | 0.79 |

## Verdict — the lead does NOT survive

Pooling 488 OOS trades did **not** rescue DONCHIAN:
- Edge is **positive but tiny** (PF 1.06, mean R +0.03).
- **Not statistically significant** (bootstrap p = 0.27; needs < 0.05).
- **Not DSR-robust** (0.22; needs ≥ 0.95).

The earlier "positive on 5/7 symbols" was an artifact of **each cell choosing its own best parameters** (per-symbol cherry-picking). Forced onto ONE shared config and tested honestly, only **2 of 7** symbols (QQQ, AAPL) are clearly positive while 2 (MSFT, AMZN) are clearly negative — no shared, tradeable edge. The 59/60 configs with "positive pooled OOS mean" are all micro-magnitude (PF≈1.0x), i.e. a consistent noise-level drift, not an edge.

**Possible narrow residual:** QQQ + AAPL alone show PF 1.39/1.45 with this config — a large-cap/index-and-mega-cap-tech niche. With only 2 names and the others negative, this is most likely noise, not a thesis. Not worth promotion work.

## Correction to prior reports

Earlier reports/handoffs this session described the DSR threshold as "p ≤ 0.05". That was the wrong direction: the engine's `deflated_sharpe_pvalue` returns a **confidence (higher better), robust at ≥ 0.95**. All "0 DSR-robust / NOT PROMOTABLE" conclusions are unchanged — only the threshold wording was inverted.

## Recommendation

- **Close the DONCHIAN lead.** No existing strategy — including the best cross-symbol candidate — has a robust, significant edge on native US-equities 10m.
- The infra (6yr × 7-symbol adjusted data with volume, discoverable bundle, downloader) stands and is reusable for any **future/new** strategy.
- No promotion, no profile/top_results artifact.
