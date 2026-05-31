# Master Overnight QuantLens Report

## 1. Executive Verdict
No candidate is Pine/MTC producer-ready tonight. The strongest practical continuation candidates remain Stage-2/Stage-3 research items, not integration items. The research package is Python-only and preserves the previous audited lesson that weak first-pass results must not be promoted.

## 2-6. Inventory and Extraction
- Input inventory count: 74
- Duplicate count: 1
- Valid intake count: 73
- Raw transcript mistaken count: 0
- Strategy candidates extracted: 14

## 7-11. Candidate Status
|candidate_id|title|tier|classification|testability|mtc_relevance|pf|net_return_pct|trade_count|
|---|---|---|---|---|---|---|---|---|
|CANDIDATE_001|Kell Wedge Pop / EMA Crossback|A|WEAK_CANDIDATE|TEST_NOW_LOCAL_DATA|PRODUCER_CANDIDATE|1.7481|331.7517|111|
|CANDIDATE_002|Martin Luke Pullback AVWAP|B|WEAK_CANDIDATE|TEST_WITH_1D_CRYPTO_PROXY|PRODUCER_CANDIDATE|1.4435|17034.8144|584|
|CANDIDATE_003|Slingshot EMA(high,4) Pullback|A|WEAK_CANDIDATE|TEST_NOW_LOCAL_DATA|PRODUCER_CANDIDATE|1.4581|292669.9798|1388|
|CANDIDATE_004|Crabel Range Expansion|A|WEAK_CANDIDATE|TEST_NOW_LOCAL_DATA|PRODUCER_CANDIDATE|1.251|7179649232.748|8105|
|CANDIDATE_005|BigBeluga RSI Divergence + CHoCH + ATR|A|WEAK_CANDIDATE|TEST_NOW_LOCAL_DATA|PRODUCER_CANDIDATE|1.4516|3955.225|465|
|CANDIDATE_006|CANSLIM Shakeout +3|C|DATA_BLOCKED|NEEDS_US_EQUITY_DATA|PRODUCER_CANDIDATE|0.0|0.0|0|
|CANDIDATE_007|Linda 5SMA RS Pullback|A|WEAK_CANDIDATE|TEST_NOW_LOCAL_DATA|PRODUCER_CANDIDATE|1.3096|1206.3069|687|
|CANDIDATE_008|8AM ET Opening Range Breakout|B|REJECT_CRYPTO_PROXY|TEST_WITH_5M_CRYPTO_PROXY|PRODUCER_CANDIDATE|0.5383|-99.4805|4259|
|CANDIDATE_009|HighBeta Opening-Bar Gap-and-Go|B|WEAK_CANDIDATE_CRYPTO_PROXY|TEST_WITH_5M_CRYPTO_PROXY|PRODUCER_CANDIDATE|1.0861|3.0885|151|
|CANDIDATE_010|Ty Rajnus Microcap Liquidity Reversion Short|C|DATA_BLOCKED|NEEDS_US_MICROCAP_DATA|DATA_BLOCKED|0.0|0.0|0|
|CANDIDATE_011|Daily Extension Anti-Chase Filter|A|REJECT|TEST_NOW_LOCAL_DATA|FILTER_CANDIDATE|0.5201|-96.8928|111|
|CANDIDATE_012|EMA20/50 Two-Retest Baseline|A|BASELINE_ONLY|TEST_NOW_LOCAL_DATA|BASELINE_ONLY|1.8741|738.7124|135|
|CANDIDATE_013|Weinstein / Long-Base Stage Analysis|B|UNTESTED_OR_BLOCKED|TEST_WITH_1D_CRYPTO_PROXY|PRODUCER_CANDIDATE||||
|CANDIDATE_014|Wyckoff / Process Framework|C|UNTESTED_OR_BLOCKED|REJECT_NOT_TESTABLE|PROCESS_ONLY||||

## 12. Top 5 Day-Trade Candidates
|candidate_id|title|classification|pf|net_return_pct|testability|
|---|---|---|---|---|---|
|CANDIDATE_008|8AM ET Opening Range Breakout|REJECT_CRYPTO_PROXY|0.5383|-99.4805|TEST_WITH_5M_CRYPTO_PROXY|
|CANDIDATE_009|HighBeta Opening-Bar Gap-and-Go|WEAK_CANDIDATE_CRYPTO_PROXY|1.0861|3.0885|TEST_WITH_5M_CRYPTO_PROXY|

## 13. Top 5 Swing-Trade Candidates
|candidate_id|title|classification|pf|net_return_pct|max_dd_pct|
|---|---|---|---|---|---|
|CANDIDATE_001|Kell Wedge Pop / EMA Crossback|WEAK_CANDIDATE|1.7481|331.7517|-46.3269|
|CANDIDATE_002|Martin Luke Pullback AVWAP|WEAK_CANDIDATE|1.4435|17034.8144|-91.7686|
|CANDIDATE_003|Slingshot EMA(high,4) Pullback|WEAK_CANDIDATE|1.4581|292669.9798|-86.417|
|CANDIDATE_004|Crabel Range Expansion|WEAK_CANDIDATE|1.251|7179649232.748|-98.442|
|CANDIDATE_005|BigBeluga RSI Divergence + CHoCH + ATR|WEAK_CANDIDATE|1.4516|3955.225|-79.8493|

## 14. Top 5 Position-Trading Candidates
|candidate_id|title|classification|testability|score|
|---|---|---|---|---|
|CANDIDATE_006|CANSLIM Shakeout +3|DATA_BLOCKED|NEEDS_US_EQUITY_DATA|8|
|CANDIDATE_013|Weinstein / Long-Base Stage Analysis|UNTESTED_OR_BLOCKED|TEST_WITH_1D_CRYPTO_PROXY|17|
|CANDIDATE_014|Wyckoff / Process Framework|UNTESTED_OR_BLOCKED|REJECT_NOT_TESTABLE|5|

## 15. Candidates Suitable for Stage 2 Robustness
|candidate_id|title|classification|pf|net_return_pct|max_dd_pct|
|---|---|---|---|---|---|
|CANDIDATE_001|Kell Wedge Pop / EMA Crossback|WEAK_CANDIDATE|1.7481|331.7517|-46.3269|
|CANDIDATE_003|Slingshot EMA(high,4) Pullback|WEAK_CANDIDATE|1.4581|292669.9798|-86.417|
|CANDIDATE_004|Crabel Range Expansion|WEAK_CANDIDATE|1.251|7179649232.748|-98.442|
|CANDIDATE_005|BigBeluga RSI Divergence + CHoCH + ATR|WEAK_CANDIDATE|1.4516|3955.225|-79.8493|
|CANDIDATE_007|Linda 5SMA RS Pullback|WEAK_CANDIDATE|1.3096|1206.3069|-85.9357|

## 16. MTC Filters/Gates Only
- CANDIDATE_011 Daily Extension Anti-Chase Filter should remain filter research only unless applied to a producer trade set and shown to reduce drawdown.

## 17. Exit/SL/TP/Trailing/Sizing Modules
- No standalone exit/sizing module is promoted tonight. ATR/time exits remain reusable research components only.

## 18. Needs Real US Equity Data
- CANDIDATE_006 CANSLIM Shakeout +3.
- CANDIDATE_013 Weinstein / Long-Base Stage Analysis, if treated as equity-native rather than crypto proxy.

## 19. Needs US Microcap/Borrow/Locate/Halt Data
- CANDIDATE_010 Ty Rajnus Microcap Short remains DATA_BLOCKED.

## 20. Needs 1m/5m Session-Aware Data
- CANDIDATE_009 HighBeta needs real US equity gap/session data.
- CANDIDATE_008 has crypto 5m proxy data but was rejected in prior and current proxy context.

## 21. Top Data Acquisition Tasks for Tomorrow
1. US equities daily OHLCV plus benchmark relative strength for CANSLIM/Weinstein.
2. US high-beta equity 5m with regular-session gaps for HighBeta.
3. US microcap 1m with premarket/borrow/locate/dilution/halt metadata for Ty Rajnus.

## 22. Exact Files Created
See `FILES_CREATED.txt`.

## 23. Exact Commands Run
See `COMMAND_LOG.txt` and `RUN_LOG.md`.

## 24. Validation Results
See `VALIDATION_REPORT.md` and `METRIC_RECOMPUTE_CHECK.csv`.

## 25. Known Limitations
- Candidate extraction is deterministic keyword/formalization over finalized intake reports, not an LLM rewrite of full transcripts.
- Some strategy prototypes are conservative proxies because source reports contain discretionary details.
- Crypto proxy does not prove equity-native/session-native edge.
- Fee stress is checked on the same generated trade set and must be monotonic.

## 26. Next Recommended Codex Prompt for Tomorrow
Audit `overnight_intake_batch_2026_05_03`, verify candidate extraction against selected intake reports, then choose either US equity data acquisition or Stage 2 robustness for the top weak swing candidates. Do not move to Pine until robustness gates pass.
