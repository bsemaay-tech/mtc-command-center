# Promotion Index — QuantLens Alpha Candidates

> These are alpha candidates from the overnight rigor audit. **None is an approved live trading system.** None is `APPROVED_FOR_MTC_V2_INTEGRATION`.
> All are LONG-only; engine logic verified; **fidelity to the original YouTube sources is NEEDS_SOURCE_CONFIRMATION**.
> Canonical evidence: `05_BACKTEST_RESULTS/MORNING_REPORT.md`, `MEGA_walk_forward_results.json`, `alpha_summary.json`, `multiwindow_summary.json`.

| Candidate ID | Family | Sym | TF | Status | Main reason | Next action |
|---|---|---|---|---|---|---|
| `QL_ALPHA_LINK_8EMA_1H` | 8EMA pullback + EMA8 trail exit | LINK | 1h | `PROMOTE_TO_FORWARD_PAPER_TRADE` + `PROMOTE_TO_PARITY_CANDIDATE` | +96.0 alpha, PF 2.04, 5/5 windows, 121 trades, stable | Python reference VERIFIED + Pine review wrapper ready → run TradingView parity (see PARITY_EXECUTION_CHECKLIST.md) |
| `QL_ALPHA_ADA_TWO_CANDLE_SR_1H` | S/R breakout + strong close | ADA | 1h | `PROMOTE_TO_FORWARD_PAPER_TRADE` + `PROMOTE_TO_PARITY_CANDIDATE` | +109.7 alpha, PF 1.72, 4/5 windows — but only 53 trades | Python reference VERIFIED + Pine review wrapper ready → forward paper-trade to grow sample, then TradingView parity |
| `QL_ALPHA_LTC_RSI_OVERSOLD_1H` | RSI(5) oversold→recovery (mean-rev) | LTC | 1h | `PROMOTE_TO_FORWARD_PAPER_TRADE` (parity deferred) | +116.7 alpha, 329 trades — but PF 1.23, folds 1/3, thin edge | Python reference VERIFIED → forward paper-trade + cost-sensitivity; Pine parity deferred |

## Parity preparation status (2026-05-30)
- Standalone Python reference producers generated and **VERIFIED** against recorded lockbox metrics for all 3 (`tools/reference_producer.py`).
- Per-candidate parity artifacts: `<id>_signals.csv`, `<id>_trades.csv`, `PARITY_REFERENCE_METRICS.md`.
- REVIEW_ONLY Pine v6 wrappers: `LINK_8EMA_REVIEW.pine`, `ADA_TWO_CANDLE_SR_REVIEW.pine` (LTC deferred).
- Execution procedure: `PARITY_EXECUTION_CHECKLIST.md`.
- **Live parity run (2026-05-30):** Pine v6 **server compile PASS** for LINK & ADA. **LINK loaded + ran live** on TradingView Desktop
  (MSIX install, relaunched with CDP): compiled, added to chart, long-only trades generated; PF ~1.65 on `LINKUSDT.P` futures
  (Jan2024–May2026), consistent with the Python reference edge. Details: `PARITY_RESULTS.md`.
- **LINK PineTS EXACT parity = PASS (2026-05-30):** producer run through PineTS on byte-identical Binance futures data vs the Python
  engine → **100.0% long-signal agreement** over 7485 bars (60/60), ema8 identical, atr14 within 1.6e-4. This is the definitive
  same-data parity gate (no feed mismatch). Artifacts in `QL_ALPHA_LINK_8EMA_1H/`: `pinets_link_parity.mjs`,
  `compare_link_pinets_parity.py`, `PINETS_PARITY_RESULT.json`. ADA: same harness ready, not yet run.
- **No production `MTC_V2.pine` modified. No live alerts/orders. None `APPROVED_FOR_MTC_V2_INTEGRATION`.**

## Cross-candidate caveats
- All **fail strict multiple-testing correction** (BH-FDR over full search space, Deflated Sharpe). Classified `STATISTICALLY_UNCONFIRMED` but practically interesting.
- "Alpha" = beat buy&hold over the locked OOS slice while the underlying fell. Strong evidence of beta-neutral behavior, NOT proof of a live edge.
- Folder paths:
  - `06_PROMOTED_TO_PARITY/QL_ALPHA_LINK_8EMA_1H/`
  - `06_PROMOTED_TO_PARITY/QL_ALPHA_ADA_TWO_CANDLE_SR_1H/`
  - `06_PROMOTED_TO_PARITY/QL_ALPHA_LTC_RSI_OVERSOLD_1H/`

Each folder: `PROMOTION_PACKET.md`, `producer_spec.json`, `FORWARD_PAPER_TRADE_PLAN.md`, `PINE_PARITY_PLAN.md`, `IMPLEMENTATION_NOTES.md`.
