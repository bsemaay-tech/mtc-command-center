# Promotion Packet — QL_ALPHA_LTC_RSI_OVERSOLD_1H

> **This is NOT an approved live trading system.** Alpha candidate for forward paper-trade preparation only.

## Summary (what matters)
- **Candidate ID:** `QL_ALPHA_LTC_RSI_OVERSOLD_1H`
- **Engine strategy family:** `GEN_RSI_OVERSOLD_REVERSAL` (RSI oversold → recovery cross, mean-reversion)
- **Symbol / Timeframe:** LTCUSDT / 1h
- **Verified params:** `rsi_len=5, oversold=35, recovery=45`
- **Direction:** LONG-only. **No trend filter** — pure mean reversion.
- **Promotion status:** `PROMOTE_TO_FORWARD_PAPER_TRADE` (parity deferred — weak fold consistency)
- **Headline:** Strategy +95.8% vs buy&hold −20.8% → **+116.7% excess alpha**, while LTC fell. Highest alpha of the three, weakest robustness profile.

## Backtest summary (locked OOS = last 25%)
| Metric | Value |
|---|---|
| Strategy compound return | +95.81% |
| Buy & hold (same window) | −20.84% |
| **Excess alpha** | **+116.65%** |
| Profit factor | 1.230 |
| Trades | 329 (highest sample of the three) |
| Max drawdown | −21.98% |
| Win rate | 38.0% |
| Expectancy | 0.107 R |
| Scaled Sharpe | 1.51 |

## Producer interpretation (engine logic)
`rsi5 = RSI(close,5)`. Long when `rsi5[1] < 35` (was oversold) AND `rsi5 >= 45` (recovered). No trend filter, no regime gate — a fast-RSI dip-recovery mean-reversion entry. Exit = 2R target / stop (5-bar low) / 96-bar limit.

## Robustness / statistical status
- **Multi-window:** positive in **4/5** windows; parameter-neighborhood **stable**.
  - ⚠️ Q3 window = **−26.4%** (one clearly negative regime).
- **Walk-forward folds:** **only 1/3 positive** — the weakest fold consistency of the three candidates.
- **Down-market alpha:** YES.
- **Bootstrap p (50k):** 0.085 (NOT significant); **Deflated Sharpe p:** 0.0 (fails). **Not** a BH-FDR survivor.
- **Verdict:** `STATISTICALLY_UNCONFIRMED`. Large 329-trade sample and high alpha, but **low PF (1.23)**, thin expectancy (0.107R), and 1/3 fold consistency → the edge is shallow and regime-sensitive.

## Why this is a true-alpha candidate
+116.7 excess over a falling LTC across 329 trades is the largest, most-traded alpha signal in the set; the high sample makes the average behavior meaningful even if per-trade edge is thin.

## Known weaknesses
- **Thin edge:** PF 1.23, expectancy 0.107R — small per-trade margin; sensitive to cost/slippage assumptions.
- **Fold inconsistency (1/3)** and a negative Q3 window → regime-dependent.
- **No trend filter** → vulnerable in sustained downtrends (mean reversion buying dips).
- Engine logic verified, but **fidelity to the original "RSI Oversold" video is NOT verified**; RSI(5) with oversold 35 / recovery 45 is the grid's best, not a confirmed source rule.

## Data coverage
- LTC 1h: 2020-01-09 → 2026-04-27, 55,208 bars (verified). Sufficient; lockbox/folds valid.

## Source files read
- `MEGA_walk_forward_results.json`, `alpha_summary.json`, `multiwindow_summary.json`, `MORNING_REPORT.md`, `CLAUDE_AUDIT_FINDINGS.md`, `tools/mega_walk_forward.py`.

## Recommendation
`PROMOTE_TO_FORWARD_PAPER_TRADE` only. **Parity work deferred** until forward results improve fold/PF profile (the 1/3 fold consistency and thin PF are not yet parity-grade). **Not** approved for live or MTC_v2 integration.
