# US-Equities 10m — Alpaca 6yr Multi-Strategy Sweep

**Date:** 2026-06-28
**Author:** Claude Opus 4.8
**Classification:** RESEARCH ONLY / NOT PROMOTABLE
**Data:** `03_QUANTLENS/data/native_us_equities_10m_alpaca_2026-06-28/` — 7 symbols (SPY, QQQ, AAPL, MSFT, NVDA, AMZN, TSLA), 10m, **~57,700 bars each (2020-07-27 → 2026-06-26, ~6yr)**, Alpaca IEX feed, split+dividend adjusted, RTH-only, **with volume**. Downloaded via `03_QUANTLENS/tools/alpaca_download_us_equities_10m.py`.

## Why this run

TradingView capped 10m history at ~20k bars (~2yr). On that thin data every strategy died. Barış provisioned an Alpaca key; we pulled ~3× the history (57.7k bars/symbol) for a 7-symbol universe and re-ran the full engine (honest walk-forward train-select + DSR multiple-testing deflation).

## Headline

**More data flipped the picture from "nothing" to "real candidates that beat buy&hold — but none clears the DSR robustness gate."**

| Metric | TradingView 2yr (3 sym) | Alpaca 6yr (7 sym) |
|---|---|---|
| Total cells | 9 (candidates) / 3 (8EMA) | 140 |
| PASS | 1 | **15** |
| DSR-robust | 0 | **0** |
| robust_final | 0 | **0** |

## PASS cells (15) — symbol coverage per strategy

| Strategy | PASS on (of 7) | Symbols |
|---|---|---|
| **GEN_DONCHIAN_BREAKOUT** | **5/7** | SPY, QQQ, AAPL, NVDA, TSLA |
| LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL | 3/7 | MSFT, AMZN, NVDA |
| GEN_GOLDEN_CROSS_PULLBACK | 2/7 | MSFT, TSLA |
| GEN_KELTNER_BREAKOUT | 2/7 | AAPL, NVDA |
| ANY_1H_RSI_CONFLUENCE_PLAYBOOK | 1/7 | NVDA |
| ANY_BOLLINGER_BANDS_20_2_TRI_SETUP | 1/7 | AMZN |
| GEN_MACD_BULL_CROSS | 1/7 | NVDA |

## Beat buy&hold (lockbox OOS) — the cells that actually add value

| Strategy | Symbol | Strategy OOS net% | Buy&hold OOS% |
|---|---|---|---|
| GEN_DONCHIAN_BREAKOUT | TSLA | **+37.1** | −9.8 |
| GEN_GOLDEN_CROSS_PULLBACK | TSLA | **+24.8** | −9.8 |
| ANY_BOLLINGER_BANDS_20_2 | AMZN | **+18.2** | +5.3 |
| GEN_DONCHIAN_BREAKOUT | AAPL | **+17.9** | +11.8 |
| GEN_GOLDEN_CROSS_PULLBACK | MSFT | **+6.3** | −11.9 |
| LIQUID_VWAP_PULLBACK | AMZN | **+5.9** | +5.3 |
| LIQUID_VWAP_PULLBACK | MSFT | **+3.1** | −11.9 |

Best DSR p-value across all 140 cells: **0.1375** (Keltner/AAPL) — still far above the ≤0.05 robustness threshold.

## Honest interpretation

- **GEN_DONCHIAN_BREAKOUT is the genuine lead.** Positive OOS on 5 of 7 symbols, beats buy&hold on AAPL and TSLA. Cross-symbol consistency is arguably stronger evidence than any single-cell DSR p-value — a spurious edge rarely repeats across 5 independent symbols.
- **But the formal gate is not met.** DSR deflates each cell's Sharpe for the number of configs tried; with 3 folds, no single cell reaches p ≤ 0.05. `robust_final = 0`. By the repo's own rules this is **NOT PROMOTABLE**.
- The strategies that beat buy&hold do so mostly where buy&hold was negative (TSLA, MSFT over this slice) — i.e. they add value as **risk-managed / lower-exposure** participation, not by out-returning a rising market.

## Recommendation for Barış

1. **Infra fully closed + upgraded.** Native US-equities 10m now has 6yr × 7 symbols, adjusted, with volume, discoverable via `03_QUANTLENS/data/README.md`.
2. **DONCHIAN breakout is worth real follow-up** — the only strategy with broad cross-symbol positive OOS. Productive next steps (each a separate, approval-gated decision):
   - Portfolio/cross-sectional evaluation of DONCHIAN across all 7 symbols (pooling trades raises DSR power vs per-cell).
   - More folds / longer history (Alpaca SIP paid → pre-2020) to strengthen DSR.
   - Volume-aware variants (we now have volume).
3. **Still do not promote / do not generate profile artifacts** — no cell is DSR-robust.

No `backtest_profile_result.json` / `top_results.json` generated. Engine unmodified. Generated run outputs left in the bundle's `full_sweep_2026-06-28/`.
