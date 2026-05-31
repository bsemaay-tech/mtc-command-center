# STRATEGY RECLASSIFICATION

## Changed Classifications
| strategy_id                        | final_classification_old | final_classification_new | aggregate_pf_new | fee_2x_pf_new | trade_count_new |
| ---------------------------------- | ------------------------ | ------------------------ | ---------------- | ------------- | --------------- |
| QL_EMA20_50_TWO_RETEST_BASELINE_v0 | WEAK_CANDIDATE           | BASELINE_ONLY            | 1.06             | 0.96          | 5614            |

## Stage 2 Candidates
| rank | strategy_id                              | aggregate_pf | fee_2x_pf | fee_3x_pf | trade_count | final_classification |
| ---- | ---------------------------------------- | ------------ | --------- | --------- | ----------- | -------------------- |
| 1    | QL_KELL_WEDGE_POP_CROSSBACK_10_20EMA_v0  | 1.24         | 1.14      | 1.04      | 1840        | WEAK_CANDIDATE       |
| 2    | QL_MARTIN_LUKE_PULLBACK_AVWAP_v0         | 1.12         | 1.03      | 0.94      | 2239        | WEAK_CANDIDATE       |
| 3    | QL_SLINGSHOT_4EMA_HIGH_PULLBACK_v0       | 1.66         | 1.48      | 1.32      | 44          | WEAK_CANDIDATE       |
| 4    | QL_CRABEL_RANGE_EXPANSION_STAGE2_v0      | 2.02         | 1.98      | 1.94      | 208         | WEAK_CANDIDATE       |
| 5    | QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 1.59         | 1.54      | 1.49      | 302         | WEAK_CANDIDATE       |
| 7    | QL_LINDA_5SMA_RS_PULLBACK_v0             | 1.61         | 1.52      | 1.44      | 559         | WEAK_CANDIDATE       |

## Filter/Gate Candidates
| rank | strategy_id                             | aggregate_pf | fee_2x_pf | trade_count | final_classification |
| ---- | --------------------------------------- | ------------ | --------- | ----------- | -------------------- |
| 11   | QL_DAILY_EXTENSION_ANTI_CHASE_FILTER_v0 | 1.59         | 1.55      | 795         | FILTER_ONLY          |

## Blocked
| rank | strategy_id                                 | next_action                                                                                                                        |
| ---- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 8    | QL_8AM_ET_OPENING_RANGE_BREAKOUT_v0         | BLOCKED_DATA: repo-local manifest has no 5m datasets; requires at least 5 liquid assets with 5m OHLCV and 08:00 ET session anchor. |
| 9    | QL_HIGHBETA_OPENINGBAR_GAPANDGO_v0          | BLOCKED_DATA: no US high-beta intraday equities and no 5m crypto session data; requires 5m OHLCV/session gap data.                 |
| 10   | QL_TY_MICROCAP_LIQUIDITY_REVERSION_SHORT_v0 | BLOCKED_DATA: requires US microcap 1m OHLCV, premarket/afterhours, market cap, borrow/locate, dilution, halt flags.                |

## Final Gate
- Pine stage: no strategy is ready for Pine from this audited batch.
- MTC producer research: only WEAK_CANDIDATE rows can go to Stage 2 robustness, not direct production/Pine.
- Gate/filter research: FILTER_ONLY rows can be kept as research-only filters.
