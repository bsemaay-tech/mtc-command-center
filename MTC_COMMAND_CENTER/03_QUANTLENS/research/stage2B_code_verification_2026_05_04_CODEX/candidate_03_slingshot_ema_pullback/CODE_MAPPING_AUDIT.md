# Code Mapping Audit

|rule|classification|evidence|
|---|---|---|
|lookahead bias|AMBIGUOUS|Most rolling indicators are past-only, but Stage-2 code was not originally backed by per-contract golden tests.|
|future candles|IMPLEMENTED_EXACTLY|No direct future indicator references found in the inspected Stage-2 functions.|
|same-bar entry/exit ambiguity|POSSIBLE_EXECUTION_BUG|Stop/target logic can evaluate full OHLC of the entry bar; this is deterministic but not market-sequence-realistic.|
|exit-before-entry ordering|IMPLEMENTED_DIFFERENTLY|Previous code generally advances index after exit, but no shared invariant test existed.|
|gap fill realism|POSSIBLE_EXECUTION_BUG|Prior code does not consistently distinguish stop trigger price from next open gap fills.|
|trigger price vs next open fill|IMPLEMENTED_DIFFERENTLY|Most candidates enter next open; Crabel enters trigger price on same bar.|
|intrabar high/low ordering|POSSIBLE_EXECUTION_BUG|Stop-first rule is conservative but not proven against real intrabar sequence.|
|warmup|AMBIGUOUS|Fixed index warmups exist but are not mechanically tied to every indicator dependency.|
|NaN handling|AMBIGUOUS|Pandas comparisons suppress many NaNs but no explicit fail-fast gate existed.|
|missing candles|AMBIGUOUS|Data quality reports exist; candidate code does not uniformly enforce missing-bar policy.|
|asset silently skipped|IMPLEMENTED_DIFFERENTLY|Previous harness logs some asset failures but continues.|
|short/long fee sign|IMPLEMENTED_EXACTLY|Return recompute here confirms cost subtracts from gross returns.|
|slippage sign|IMPLEMENTED_EXACTLY|Cost stress is monotonic in the repaired recompute.|
|gross vs net confusion|POSSIBLE_EXECUTION_BUG|Previous reports emphasized compounded net return values that became numerically misleading.|
|PF calculation|IMPLEMENTED_EXACTLY|PF recomputed from trade_trace net returns.|
|drawdown calculation|IMPLEMENTED_DIFFERENTLY|Compounded drawdown is sensitive to extreme compounding; non-compounded return is included here.|
|compounding overflow|POSSIBLE_EXECUTION_BUG|Compounding status: OVERFLOW_RISK_CAPPED.|
|over-optimization|AMBIGUOUS|Stage-2 selected best parameter sets from grids; Stage-2B does not promote them as production defaults.|
|wrong timeframe|AMBIGUOUS|Native/proxy timeframe used here: 1D.|
|crypto proxy caveat|IMPLEMENTED_EXACTLY|Marked as US_equity_style_crypto_proxy.|

## Recomputed Metric Snapshot
- trade_count: 856
- PF: 1.749484
- OOS rows: 3
- fee monotonic PF: 1.749484 >= 1.720543 >= 1.692191 >= 1.637186
