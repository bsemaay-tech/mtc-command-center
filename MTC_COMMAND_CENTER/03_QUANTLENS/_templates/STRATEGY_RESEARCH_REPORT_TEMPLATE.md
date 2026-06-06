# Strategy Research Report — `<research_run_id>`

> Final report for one research run. Save under
> `03_QUANTLENS/research/<research_run_id>/report.md` and register the run in
> `05_REGISTRY/RESEARCH_RUN_REGISTRY.json` (`research_runs[]`) so it appears in
> **Strategy Research Lab → Research Runs**.

## 1. Executive summary
2–5 sentences: what was tried, what was found, the final call.

## 2. Research objective
The hypothesis and what "success" would look like.

## 3. Asset universe
Symbols and why they were chosen.

## 4. Data range
Start..end, source, bar count, any gaps.

## 5. Strategy components used
Component_ids and indicator_ids from the registries.

## 6. Architecture families tested
One or more of: regime_switching_strategy, signal_scoring_ensemble,
specialist_strategy_portfolio, breakout_pullback_hybrid.

## 7. Backtest assumptions
Per `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`:
starting capital, commission, slippage, position sizing, execution timing
(next-bar open), long-only vs long/short, 24/7 handling.

## 8. Variant summary
Table of every variant (link each to its variant log). Include rejected ones.

| variant_id | architecture | net % | maxDD % | PF | win % | decision |
|---|---|---|---|---|---|---|

## 9. Winning strategy, if any
Full description, parameters, and why it won. State explicitly if none won.

## 10. Full asset-by-asset results
One row per asset for the leading variant(s).

## 11. Portfolio-level results
Aggregate equity, drawdown, correlation/diversification notes.

## 12. Robustness analysis
Multi-window, walk-forward, parameter sensitivity, B&H alpha.

## 13. Overfitting risk analysis
DSR, BH-FDR survivorship, trade count, in/out-of-sample gap.

## 14. Code safety review
Result of STRATEGY_CODE_REVIEW_CHECKLIST.md (PASS/FAIL + notes).

## 15. TradingView compatibility notes
Repaint/lookahead parity, Pine⇄Python conversion risks.

## 16. UI tracking record path
Paths to the RESEARCH_RUN_REGISTRY / VARIANT_LOG_REGISTRY entries and this report.

## 17. Final recommendation
One of (verbatim label):
- **Recommended for further paper testing**
- **Needs more research**
- **Not recommended**
- **No robust strategy found**

## 18. Next steps
Concrete follow-up actions (tag with [AI: ...] for NEXT_STEPS.md).
