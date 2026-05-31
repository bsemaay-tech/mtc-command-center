# Audited Master Comparison

|audited_rank|candidate_id|strategy_family|horizon|data_type|assets_tested|trades|PF_base|PF_fee_2x|max_DD|final_classification|next_action|
|---|---|---|---|---|---|---|---|---|---|---|---|
|1|CANDIDATE_003|trend_pullback|SWING|CRYPTO_PROXY|10|1388|1.4581|1.3872|-86.417|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|2|CANDIDATE_001|trend_pullback|SWING|CRYPTO_PROXY|10|111|1.7481|1.6786|-46.3269|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|3|CANDIDATE_004|breakout|SWING|CRYPTO_PROXY|10|8105|1.251|1.1866|-98.442|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|4|CANDIDATE_012|baseline_trend|SWING|CRYPTO_PROXY|10|135|1.8741|1.8376|-82.1442|BASELINE_ONLY|Keep for benchmark comparisons|
|5|CANDIDATE_009|intraday_momentum|DAY_TRADE|5M_PROXY|5|151|1.0861|0.716|-7.1457|NEEDS_INTRADAY_SESSION_DATA|Acquire US high-beta 5m gap/session data|
|6|CANDIDATE_007|mean_reversion_pullback|SWING|CRYPTO_PROXY|10|687|1.3096|1.2609|-85.9357|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|7|CANDIDATE_005|reversal_structure|SWING|CRYPTO_PROXY|10|465|1.4516|1.4236|-79.8493|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|8|CANDIDATE_002|support_reclaim|SWING|CRYPTO_PROXY|10|584|1.4435|1.4078|-91.7686|WEAK_CANDIDATE|Stage 2 robustness only; no Pine|
|9|CANDIDATE_008|intraday_breakout|DAY_TRADE|5M_PROXY|5|4259|0.5383|0.3067|-99.4799|REJECT_NO_EDGE|Do not pursue|
|10|CANDIDATE_006|position_breakout|POSITION|DATA_BLOCKED|0|0|0.0|0.0|0.0|NEEDS_REAL_EQUITY_DATA|Acquire US equity daily/RS data|
|11|CANDIDATE_010|microcap_short|SWING|DATA_BLOCKED|0|0|0.0|0.0|0.0|NEEDS_REAL_MICROCAP_DATA|Acquire microcap 1m/borrow/locate/halt/dilution data|
|12|CANDIDATE_013|position_trend|POSITION|DATA_BLOCKED|0|0|0.0|0.0|0.0|NEEDS_REAL_EQUITY_DATA|Acquire US equity daily/RS data|
|13|CANDIDATE_014|process|PROCESS|REAL_NATIVE|0|0|0.0|0.0|0.0|PROCESS_ONLY|Do not pursue|
|14|CANDIDATE_011|filter|FILTER|CRYPTO_PROXY|10|111|0.5201|0.5031|-98.614|FILTER_ONLY|Test as gate on existing producer trade sets|