# METRIC BUG AUDIT

## Verdict
- Old MASTER_BATCH_REPORT.md is not reliable for ordering or fee-stress robustness claims.
- Core strategy backtest rows were reproducible, but master ranking and fee-stress comparisons mixed unlike sets.

## Root Causes
- Test order bug: `main()` sorted strategy rows by `final_classification` and `aggregate_pf`; the report then assigned rank after that sort. CANSLIM appeared first because `BASELINE_ONLY` sorted before BLOCKED/FILTER/WEAK, not because it was executed first.
- Fee stress bug: old fee stress loop used `timeframes[:1]`; aggregate metrics used the selected best parameter across all primary asset/timeframe rows. Therefore `fee_2x_pf` and `fee_3x_pf` were sometimes calculated on a different trade set.
- Best variant vs aggregate: audited output keeps the same best `parameter_set`, then recomputes base/2x/3x fees on the same asset/timeframe set.
- Fee sign/classification: long and short slippage signs are directionally correct in `shared/backtest_utils.py`; profit factor is computed from net trade returns after costs.

## Suspicious Old Rows
| strategy_id                              | aggregate_pf_old | fee_2x_pf_old | fee_3x_pf_old | aggregate_pf_new | fee_2x_pf_new | fee_3x_pf_new |
| ---------------------------------------- | ---------------- | ------------- | ------------- | ---------------- | ------------- | ------------- |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 1.59             | 1.73          | 1.66          | 1.59             | 1.54          | 1.49          |
| QL_EMA20_50_TWO_RETEST_BASELINE_v0       | 1.06             | 1.15          | 1.12          | 1.06             | 0.96          | 0.87          |
| QL_KELL_WEDGE_POP_CROSSBACK_10_20EMA_v0  | 1.24             | 8.78          | 8.28          | 1.24             | 1.14          | 1.04          |

## Independent Recompute Basis
- Aggregate PF is recomputed from strategy `trades.csv` net trade returns for the selected best parameter.
- Trade count is recomputed from the same selected best-parameter trade set.
- Fee stress is now recomputed from the same selected best-parameter asset/timeframe pairs.
- Independent recompute output: `06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/METRIC_RECOMPUTE_CHECK.csv`.
- Recompute result: all audited rows have matching trade count, matching PF, and monotonic fee stress (`base >= 2x >= 3x`).

## Classification Logic Audit
- `QL_EMA20_50_TWO_RETEST_BASELINE_v0` was incorrectly left as `WEAK_CANDIDATE` in the old report because a LOW_SAMPLE cap path was applied before recognizing the strategy as a baseline reference.
- Audited classification moves it to `BASELINE_ONLY`; fee stress falls below 1.0 at 2x and 3x costs, so it is not a Stage 2 producer candidate.
