# US-Equities 10m — Multi-Strategy Native Sweep

**Date:** 2026-06-28
**Author:** Claude Opus 4.8
**Classification:** RESEARCH ONLY / NOT PROMOTABLE
**Data:** `03_QUANTLENS/data/native_us_equities_10m_us3_tradingview_2026-06-28/` (SPY/QQQ/AAPL, 20,094 native TradingView 10m RTH bars each, 2024-06-03 → 2026-06-26)

## Scope

After the 8EMA-pullback strategy died on SPY/QQQ/AAPL (`SPY_QQQ_AAPL_10M_8EMA_PARAM_SWEEP_2026-06-28.md`), Barış approved testing **every other distinct strategy** in the engine on the same native bundle.

- 15 distinct strategies swept (the 3 `US_EQUITIES_INTRADAY_*` strategies are byte-identical signal+grid aliases of 8EMA → skipped; `SWING_1H_DUAL_RSI` needs a daily-RSI map / 1D bundle we don't have → skipped).
- Two-stage method, deliberately:
  1. **Stage A — exploratory best-of-grid sweep** (full-period + lockbox-OOS, hand-rolled): which strategies *look* like they have signal.
  2. **Stage B — honest engine walk-forward** (`mega_walk_forward.py`: select config on **train fold only**, evaluate on locked OOS, then **Deflated Sharpe Ratio** deflation for multiple testing): which strategies *actually* survive.

## Stage A — exploratory sweep (optimistic, cherry-picked)

Top by surviving configs (full net>0 AND lockbox net>0 AND ≥30 trades):

| Strategy | Survivors | Best lockbox-OOS config |
|---|---|---|
| GEN_DONCHIAN_BREAKOUT | 88 | QQQ +12.4% / 51 tr / PF 1.57 |
| VWAP_PULLBACK_REVERSAL | 39 | AAPL +13.7% / 20 tr / PF 2.43 |
| GEN_GOLDEN_CROSS_PULLBACK | 17 | AAPL +10.0% / 54 tr / PF 1.49 |
| ANY_BOLLINGER_BANDS_20_2 | 22 | QQQ +7.6% / 23 tr / PF 1.96 |
| GEN_MACD_BULL_CROSS | 10 | QQQ +5.3% / 46 tr / PF 1.35 |
| (others) | 0–9 | weak |

This looked promising — unlike 8EMA (1 noise survivor), several strategies showed lots of positive-OOS configs.

## Stage B — honest engine walk-forward (the real test)

Ran the actual DSR-gated engine on the top 3 (DONCHIAN, VWAP, GOLDEN_CROSS) × SPY/QQQ/AAPL — 9 cells, 207 configs, output contained in `candidate_sweep_2026-06-28/`, engine unmodified.

| Strategy | Symbol | Class | OOS trades | OOS net% | PF | DSR p | robust_final |
|---|---|---|---|---|---|---|---|
| GEN_DONCHIAN_BREAKOUT | AAPL | **PASS** | 69 | +2.18 | 1.07 | 0.215 | **false** |
| GEN_DONCHIAN_BREAKOUT | QQQ | FAIL | 76 | −1.30 | 0.99 | 0.128 | false |
| GEN_DONCHIAN_BREAKOUT | SPY | FAIL | 44 | −1.13 | 0.93 | 0.156 | false |
| GOLDEN_CROSS_PULLBACK | AAPL | FAIL | 59 | −0.21 | 1.00 | 0.308 | false |
| GOLDEN_CROSS_PULLBACK | QQQ | FAIL | 49 | −2.11 | 0.86 | 0.178 | false |
| GOLDEN_CROSS_PULLBACK | SPY | FAIL | 53 | −4.91 | 0.62 | 0.025 | false |
| VWAP_PULLBACK_REVERSAL | AAPL | FAIL | 35 | −5.40 | 0.72 | 0.062 | false |
| VWAP_PULLBACK_REVERSAL | QQQ | INSUFFICIENT | 27 | −2.26 | 0.82 | 0.144 | false |
| VWAP_PULLBACK_REVERSAL | SPY | INSUFFICIENT | 12 | −3.71 | 0.29 | 0.016 | false |

**1 of 9 cells PASS (DONCHIAN/AAPL), 0 DSR-robust, 0 robust_final.**

## Verdict

**No promotable strategy on SPY/QQQ/AAPL 10m in this window.** The gap between Stage A and Stage B is the whole story:

- Stage A's "88 survivors" for DONCHIAN were **multiple-testing noise** — picking the best lockbox config peeks at the OOS data.
- Stage B selects each config on the **train fold only**, then tests honestly on locked OOS, then deflates the Sharpe for the number of configs tried. The apparent edge collapses: DONCHIAN/AAPL is the only positive-OOS PASS and its DSR p-value (0.215) is far from significant (need ≤ 0.05); buy&hold (+47% AAPL) dwarfs its +2.18%.

This is the same conclusion the crypto-proxy soak reached for these strategies: real signal does not survive honest out-of-sample + multiple-testing control.

## Recommendation for Barış

1. **Pipeline is fully proven** on native US-equities 10m — data ingest, bundle, engine, walk-forward, DSR, regime breakdown all run correctly on real SPY/QQQ/AAPL bars. The infra blocker is closed.
2. **None of the 15 existing strategies has a robust edge here.** Do not promote, do not run a full multi-iteration soak expecting a winner.
3. If you want to pursue US-equities 10m seriously, the productive paths are **new strategy logic** (not in the current grid) and/or **more symbols + longer history** — the current strategy library is crypto-era and does not transfer.
4. Adjustment policy + equity-session gating remain unconfigured — **moot** until a strategy with a real edge exists.

No `backtest_profile_result.json` / `top_results.json` generated (nothing qualifies).
