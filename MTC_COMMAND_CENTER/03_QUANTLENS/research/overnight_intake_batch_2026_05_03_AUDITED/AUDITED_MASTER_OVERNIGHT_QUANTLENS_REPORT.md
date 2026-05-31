# Audited Master Overnight QuantLens Report

## 1. Executive Verdict
- Pine-ready strategies: none.
- MTC producer-ready strategies: none.
- Stage 2 candidates: CANDIDATE_003, CANDIDATE_001, CANDIDATE_004, CANDIDATE_007, CANDIDATE_005, CANDIDATE_002.
- Day-trade candidates: HighBeta remains data-needing weak proxy; 8AM ORB is rejected.
- Swing candidates: several weak candidates merit robustness only.
- Position candidates: blocked by real equity data.
- Rejected: 8AM ORB crypto proxy, process-only Wyckoff, standalone anti-chase as producer.

## 2. First-Run Reliability Verdict
Partially reliable. First-run clean trade exports recompute consistently, but reporting/classification was not reliable enough because huge compounded returns and high drawdowns were not framed conservatively enough.

## 3. Input Coverage
- Intake directory: `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs`
- Total .md files: 74
- Valid intakes: 51
- Raw transcripts: 0
- Duplicates: 23
- Around-66 expectation: actual count differs because this intake directory currently contains 74 markdown files and audited duplicate/raw classification is path-content based.

## 4. Candidate Extraction Summary
- First-run candidates audited: 14
- Audited candidates: 14
- Reclassified or downgraded: anti-chase, EMA20/50, HighBeta, ORB, data-blocked equity/microcap items.

## 5. Data Audit Summary
- Crypto daily bundle used for swing proxies.
- 5m research data used for intraday crypto proxies.
- US equity/microcap data unavailable.
- Proxy warnings apply to HighBeta, CANSLIM, Weinstein, microcap, and session strategies.

## 6. Backtest Audit Summary
- Tested candidates: 10
- Rerun candidates: none; audited recomputation used same exported trade sets to avoid mixed-trade fee errors.
- Invalidated tests: no trade export invalidated, but promotion claims downgraded.

## 7. Metric Audit Summary
|candidate_id|first_trade_count|audited_trade_count|first_pf|audited_pf|mismatch_status|
|---|---|---|---|---|---|
|CANDIDATE_001|111|111|1.7481|1.7481|MATCH|
|CANDIDATE_002|584|584|1.4435|1.4435|MATCH|
|CANDIDATE_003|1388|1388|1.4581|1.4581|MATCH|
|CANDIDATE_004|8105|8105|1.251|1.251|MATCH|
|CANDIDATE_005|465|465|1.4516|1.4516|MATCH|
|CANDIDATE_006|0|0|0.0|0.0|MATCH|
|CANDIDATE_007|687|687|1.3096|1.3096|MATCH|
|CANDIDATE_008|4259|4259|0.5383|0.5383|MATCH|
|CANDIDATE_009|151|151|1.0861|1.0861|MATCH|
|CANDIDATE_010|0|0|0.0|0.0|MATCH|
|CANDIDATE_011|111|111|0.5201|0.5201|MATCH|
|CANDIDATE_012|135|135|1.8741|1.8741|MATCH|
|CANDIDATE_013|0|0|0.0|0.0|MATCH|
|CANDIDATE_014|0|0|0.0|0.0|MATCH|

## 8. Corrected Strategy Ranking
|audited_rank|candidate_id|horizon|data_type|assets_tested|trades|PF_base|PF_fee_2x|max_DD|final_classification|next_action|
|---|---|---|---|---|---|---|---|---|---|---|
|1|CANDIDATE_003|SWING|CRYPTO_PROXY|10|1388|1.4581|1.3872|-86.417|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|2|CANDIDATE_001|SWING|CRYPTO_PROXY|10|111|1.7481|1.6786|-46.3269|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|3|CANDIDATE_004|SWING|CRYPTO_PROXY|10|8105|1.251|1.1866|-98.442|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|4|CANDIDATE_012|SWING|CRYPTO_PROXY|10|135|1.8741|1.8376|-82.1442|BASELINE_ONLY|Keep for benchmark comparisons|
|5|CANDIDATE_009|DAY_TRADE|5M_PROXY|5|151|1.0861|0.716|-7.1457|NEEDS_INTRADAY_SESSION_DATA|Acquire US high-beta 5m gap/session data|
|6|CANDIDATE_007|SWING|CRYPTO_PROXY|10|687|1.3096|1.2609|-85.9357|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|7|CANDIDATE_005|SWING|CRYPTO_PROXY|10|465|1.4516|1.4236|-79.8493|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|8|CANDIDATE_002|SWING|CRYPTO_PROXY|10|584|1.4435|1.4078|-91.7686|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|9|CANDIDATE_008|DAY_TRADE|5M_PROXY|5|4259|0.5383|0.3067|-99.4799|REJECT_NO_EDGE|Do not pursue|
|10|CANDIDATE_006|POSITION|DATA_BLOCKED|0|0|0.0|0.0|0.0|NEEDS_REAL_EQUITY_DATA|Acquire US equity daily/RS data|
|11|CANDIDATE_010|SWING|DATA_BLOCKED|0|0|0.0|0.0|0.0|NEEDS_REAL_MICROCAP_DATA|Acquire microcap 1m/borrow/locate/halt/dilution data|
|12|CANDIDATE_013|POSITION|DATA_BLOCKED|0|0|0.0|0.0|0.0|NEEDS_REAL_EQUITY_DATA|Acquire US equity daily/RS data|
|13|CANDIDATE_014|PROCESS|REAL_NATIVE|0|0|0.0|0.0|0.0|PROCESS_ONLY|Do not pursue|
|14|CANDIDATE_011|FILTER|CRYPTO_PROXY|10|111|0.5201|0.5031|-98.614|FILTER_ONLY|Test as gate on existing producer trade sets|

## 9. Corrected Day-Trade Candidates
|candidate_id|PF_base|PF_fee_2x|max_DD|final_classification|next_action|
|---|---|---|---|---|---|
|CANDIDATE_009|1.0861|0.716|-7.1457|NEEDS_INTRADAY_SESSION_DATA|Acquire US high-beta 5m gap/session data|
|CANDIDATE_008|0.5383|0.3067|-99.4799|REJECT_NO_EDGE|Do not pursue|

## 10. Corrected Swing-Trade Candidates
|candidate_id|PF_base|PF_fee_2x|max_DD|final_classification|next_action|
|---|---|---|---|---|---|
|CANDIDATE_003|1.4581|1.3872|-86.417|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|CANDIDATE_001|1.7481|1.6786|-46.3269|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|CANDIDATE_004|1.251|1.1866|-98.442|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|CANDIDATE_012|1.8741|1.8376|-82.1442|BASELINE_ONLY|Keep for benchmark comparisons|
|CANDIDATE_007|1.3096|1.2609|-85.9357|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|CANDIDATE_005|1.4516|1.4236|-79.8493|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|CANDIDATE_002|1.4435|1.4078|-91.7686|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|CANDIDATE_010|0.0|0.0|0.0|NEEDS_REAL_MICROCAP_DATA|Acquire microcap 1m/borrow/locate/halt/dilution data|

## 11. Corrected Position-Trading Candidates
|candidate_id|data_type|final_classification|next_action|
|---|---|---|---|
|CANDIDATE_006|DATA_BLOCKED|NEEDS_REAL_EQUITY_DATA|Acquire US equity daily/RS data|
|CANDIDATE_013|DATA_BLOCKED|NEEDS_REAL_EQUITY_DATA|Acquire US equity daily/RS data|

## 12. Filter / Exit / Sizing Modules Worth Keeping
- Daily Extension Anti-Chase: keep only as gate/filter research, not standalone producer.
- ATR/time exits remain reusable audit components only.

## 13. Rejected / Blocked Ideas
|candidate_id|final_classification|next_action|
|---|---|---|
|CANDIDATE_009|NEEDS_INTRADAY_SESSION_DATA|Acquire US high-beta 5m gap/session data|
|CANDIDATE_006|NEEDS_REAL_EQUITY_DATA|Acquire US equity daily/RS data|
|CANDIDATE_010|NEEDS_REAL_MICROCAP_DATA|Acquire microcap 1m/borrow/locate/halt/dilution data|
|CANDIDATE_013|NEEDS_REAL_EQUITY_DATA|Acquire US equity daily/RS data|

## 14. Stage 2 Recommendation
Run Stage 2 only for audited WEAK_CANDIDATE rows: Kell, Martin Luke proxy, Slingshot, Crabel, BigBeluga, Linda. Requirements: per-year split, holdout assets, fee 2x/3x/5x, drawdown clustering, asset concentration, baseline/random-entry comparisons.

## 15. MTC/Pine Recommendation
- Direct MTC integration: no.
- Pine conversion: no.
- Reason: no candidate passed drawdown/proxy/robustness gates.

## 16. Data Acquisition Plan for Tomorrow
1. US equities daily OHLCV + RS benchmark for CANSLIM/Weinstein.
2. US high-beta 5m session/gap data for HighBeta.
3. US microcap 1m + premarket/borrow/locate/dilution/halt data for Ty.
4. Continue using existing crypto 5m only for proxy experiments.

## 17. Exact Files Created
See `FILES_CREATED.txt`.

## 18. Exact Commands Run
See `COMMAND_LOG.txt`.

## 19. Validation Results
See `VALIDATION_REPORT.md`.

## 20. Known Limitations
- Audited candidate extraction still uses deterministic report parsing and fixed known candidate taxonomy.
- Some intakes are covered as pooled process/research ideas rather than one candidate each.
- No new external data acquisition was performed.

## 21. Recommended Next Codex Prompt
Use the prompt included in the final response: run Stage 2 robustness only on audited WEAK_CANDIDATE rows, no Pine/MTC integration.
