# Promotion Packet — QL_ALPHA_LINK_8EMA_1H

> **This is NOT an approved live trading system.** It is an alpha candidate for forward paper-trade and Pine parity preparation only.

## Summary (what matters)
- **Candidate ID:** `QL_ALPHA_LINK_8EMA_1H`
- **Engine strategy family:** `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` (8EMA pullback entry + 8EMA trailing exit)
- **Symbol / Timeframe:** LINKUSDT / 1h
- **Verified params:** `pullback_atr=0.5, impulse_atr=1.6, slope_window=3`
- **Direction:** LONG-only (engine simulates long signals only; all performance is from longs)
- **Promotion status:** `PROMOTE_TO_FORWARD_PAPER_TRADE` + `PROMOTE_TO_PARITY_CANDIDATE`
- **Headline:** Strategy +75.4% vs buy&hold −20.6% over the locked OOS slice → **+96.0% excess alpha**, while LINK fell.

## Backtest summary (locked OOS = last 25% of history)
| Metric | Value |
|---|---|
| Strategy compound return | +75.37% |
| Buy & hold (same window) | −20.64% |
| **Excess alpha** | **+96.01%** |
| Profit factor | 2.038 |
| Trades | 121 |
| Max drawdown | −16.31% |
| Win rate | 35.5% |
| Expectancy | 0.338 R |
| Scaled Sharpe (t-stat-like) | 1.64 |

## Robustness / statistical status
- **Multi-window (Q1..Q4 + H2):** positive in **5/5** windows; parameter-neighborhood **stable**. Strongest of the three alpha candidates.
- **Walk-forward folds:** positive in 2/3 forward folds.
- **Down-market alpha:** YES (profited while LINK declined).
- **Bootstrap p (50k resamples):** 0.027 (significant alone, but **does NOT survive Benjamini-Hochberg FDR** over the full search space).
- **Deflated Sharpe p:** 0.068 (**fails** p≥0.95 threshold).
- **Verdict:** `STATISTICALLY_UNCONFIRMED` under strict multiple-testing correction, but **practically the strongest** candidate (best PF, 5/5 regime, decent trade count).

## Why this is a true-alpha candidate
Beat buy & hold by ~+96 points and made money while the underlying fell — this is beta-neutral behavior, not trend capture. PF 2.04 with 121 trades and stable parameter neighborhood is the cleanest practical profile in the overnight set.

## Known weaknesses
- Fails strict multiple-testing correction (BH-FDR, DSR) — treat as candidate, not proven edge.
- `8EMA_EXIT_TRAIL` mixes a producer (entry) with an exit rule (close<EMA8 trail) — must be separated for MTC_v2 (see IMPLEMENTATION_NOTES).
- Engine logic is a **simplified interpretation**; **fidelity to the original YouTube "8EMA" producer is NOT verified** (the source intake spec was not confirmed bar-for-bar).
- Win rate 35.5% depends on the 2R-equivalent trailing exit capturing large winners; sensitive to exit fidelity.

## Data coverage
- LINK 1h: 2020-01-17 → 2026-04-27, 55,016 bars (verified from disk). Sufficient history; lockbox and folds valid.

## Source files read
- `05_BACKTEST_RESULTS/MEGA_walk_forward_results.json` (verified params + metrics)
- `05_BACKTEST_RESULTS/alpha_summary.json` (buy&hold / excess alpha)
- `05_BACKTEST_RESULTS/multiwindow_summary.json` (regime + stability)
- `05_BACKTEST_RESULTS/MORNING_REPORT.md`, `CLAUDE_AUDIT_FINDINGS.md`
- `tools/mega_walk_forward.py` (signal definition: `build_signals`, `simulate_slice`)

## Recommendation
`PROMOTE_TO_FORWARD_PAPER_TRADE` now; eligible for `PROMOTE_TO_PARITY_CANDIDATE` because engine logic + params are verified. **Not** approved for live or MTC_v2 core integration.
