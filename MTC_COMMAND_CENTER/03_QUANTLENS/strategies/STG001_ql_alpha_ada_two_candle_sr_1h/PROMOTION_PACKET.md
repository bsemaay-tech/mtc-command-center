# Promotion Packet — QL_ALPHA_ADA_TWO_CANDLE_SR_1H

> **This is NOT an approved live trading system.** Alpha candidate for forward paper-trade and Pine parity preparation only.

## Summary (what matters)
- **Candidate ID:** `QL_ALPHA_ADA_TWO_CANDLE_SR_1H`
- **Engine strategy family:** `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR` (support/resistance breakout + strong-close confirmation)
- **Symbol / Timeframe:** ADAUSDT / 1h
- **Verified params:** `level_lookback=200, upper_third=0.6, break_buf_atr=0.0`
- **Direction:** LONG-only.
- **Promotion status:** `PROMOTE_TO_FORWARD_PAPER_TRADE` + `PROMOTE_TO_PARITY_CANDIDATE` (low-trade-count caveat)
- **Headline:** Strategy +79.2% vs buy&hold −30.5% → **+109.7% excess alpha**, while ADA fell.

## Backtest summary (locked OOS = last 25%)
| Metric | Value |
|---|---|
| Strategy compound return | +79.23% |
| Buy & hold (same window) | −30.47% |
| **Excess alpha** | **+109.70%** |
| Profit factor | 1.721 |
| Trades | 53 |
| Max drawdown | −14.16% |
| Win rate | 49.1% |
| Expectancy | 0.440 R |
| Scaled Sharpe | 1.70 |

## Producer interpretation (engine logic)
Breakout + sentiment confirmation: a bar that (a) closes in the **upper third of its range** (`pos>=0.6`), (b) closes **above the prior bar high**, and (c) closes **above the highest high of the last 200 bars** (resistance break, no ATR buffer). This is a **breakout-with-strong-close** reading of "two-candle SR", not a mean-reversion reading.

## Robustness / statistical status
- **Multi-window:** positive in **4/5** windows; parameter-neighborhood **stable**.
  - ⚠️ Q1 window shows +599% — an early-history small-sample distortion (large ADA moves); treat with caution. Q2 was −27.7%.
- **Walk-forward folds:** 2/3 positive.
- **Down-market alpha:** YES.
- **Bootstrap p (50k):** 0.014; **Deflated Sharpe p:** 0.015 — both **fail** strict BH-FDR / DSR thresholds.
- **Verdict:** `STATISTICALLY_UNCONFIRMED`; high alpha and high win rate but **only 53 lockbox trades** (above the 30 minimum but low confidence).

## Why this is a true-alpha candidate
+109.7 excess over a falling ADA, 49% win rate, expectancy 0.44R — strong per-trade economics. The breakout-with-strong-close logic is simple and deterministic.

## Known weaknesses
- **Low trade count (53)** → fragile statistics; the high alpha is partly carried by few large winners.
- Q1 +599% inflates multi-window optics; the durable evidence is Q3/Q4/H2.
- Engine logic is a **simplified interpretation**; **fidelity to the original "Two-Candle SR" video is NOT verified**.
- 200-bar resistance lookback makes signals rare; sensitive to lookback choice.

## Data coverage
- ADA 1h: 2020-01-31 → 2026-04-27, 54,680 bars (verified). Sufficient; lockbox/folds valid.

## Source files read
- `MEGA_walk_forward_results.json`, `alpha_summary.json`, `multiwindow_summary.json`, `MORNING_REPORT.md`, `CLAUDE_AUDIT_FINDINGS.md`, `tools/mega_walk_forward.py`.

## Recommendation
`PROMOTE_TO_FORWARD_PAPER_TRADE` (priority — gather more trades). Eligible for `PROMOTE_TO_PARITY_CANDIDATE` (logic+params verified) but parity work should wait until forward trades raise sample confidence. **Not** approved for live or MTC_v2 integration.
