# Duplicate URL Strategy Audit - 2026-05-31

Scope: `MTC_COMMAND_CENTER/11_TRIAGE/2026-05-30_rejected_worklist.xlsx`. YouTube URLs were normalized by video id, so `youtu.be/<id>` and `youtube.com/watch?v=<id>` are treated as the same source.

## Summary

- Workbook rows reviewed: 172
- Rows with a YouTube URL: 161
- Unique YouTube video IDs: 76
- Video IDs attached to more than one strategy row: 23
- Strategy rows inside repeated-URL groups: 108

- INTENTIONAL_SPLIT_OR_MODULES: 9 group(s)
- LIKELY_INTENTIONAL_MULTI_MODULE: 1 group(s)
- SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES: 13 group(s)

## Conclusion

No clear accidental duplicate group was found. Repeated URLs mostly represent either a source/interview parent row plus extracted strategy/module candidates, or an explicit split where one video contains multiple codifiable ideas. Rows marked `INTENTIONAL_SPLIT_OR_MODULES` should not be backtested as one combined strategy until each module is reviewed separately.

## Repeated URL Groups

| Video ID | Rows | Verdict | Stg codes | Reason | Video name |
|---|---:|---|---|---|---|
| kTqKRi-j9kM | 9 | INTENTIONAL_SPLIT_OR_MODULES | Stg056, Stg125, Stg126, Stg127, Stg128, Stg129, Stg130, Stg131, Stg132 | audit split signal present; 8 extracted child row(s), 1 source/parent row(s) | The 5 Essential Sell Rules from a Market Wizard - Linda Bradford Raschke |
| -JyH5PAJ4-Y | 8 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg009, Stg136, Stg138, Stg139, Stg140, Stg141, Stg144, Stg148 | same source parent plus 7 extracted candidate/module row(s); no duplicate flag | I Stopped Trading So Much and My Profits Skyrocketed |
| O0GpSPtmCuM | 8 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg036, Stg160, Stg161, Stg162, Stg163, Stg164, Stg165, Stg166 | same source parent plus 7 extracted candidate/module row(s); no duplicate flag | Stage Analysis Warnings for Current Markets - Exclusive Interview with Stan Weinstein |
| _QewlGLBaeA | 8 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg048, Stg088, Stg089, Stg090, Stg091, Stg092, Stg093, Stg094 | same source parent plus 7 extracted candidate/module row(s); no duplicate flag | Trading Millions How I Finally Became a Profitable Swing Trader |
| ivL6E6Lc6gM | 8 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg054, Stg107, Stg108, Stg109, Stg110, Stg111, Stg112, Stg113 | same source parent plus 7 extracted candidate/module row(s); no duplicate flag | a Hedge Fund Manager Reveals his Perfect Pullback Trading Setup |
| 10pHBNVi4Jc | 7 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg010, Stg115, Stg116, Stg117, Stg118, Stg119, Stg120 | same source parent plus 6 extracted candidate/module row(s); no duplicate flag | The Trading Setups of the Record Breaking Trading Champion |
| 62OaP91Jz9k | 7 | INTENTIONAL_SPLIT_OR_MODULES | Stg013, Stg137, Stg142, Stg143, Stg145, Stg146, Stg147 | audit split signal present; 6 extracted child row(s), 1 source/parent row(s) | 120% Return A Simple Weekly Strategy Anyone Can Use |
| UmLa9FAlMgw | 7 | INTENTIONAL_SPLIT_OR_MODULES | Stg043, Stg096, Stg097, Stg098, Stg099, Stg100, Stg101 | audit split signal present; 6 extracted child row(s), 1 source/parent row(s) | The AVWAP Trading Indicator Secrets and Setups Brian Shannon, CMT |
| KQRuUWSZvLE | 6 | INTENTIONAL_SPLIT_OR_MODULES | Stg028, Stg154, Stg155, Stg156, Stg157, Stg158 | audit split signal present; 5 extracted child row(s), 1 source/parent row(s) | 10 Steps to Profitable Trading in 2024  Ryan Pierpont |
| MnXQOt7_ZP0 | 6 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg032, Stg149, Stg150, Stg151, Stg152, Stg153 | same source parent plus 5 extracted candidate/module row(s); no duplicate flag | +85% Return in 30 Days The AI Bull Market Can Change your Life Hedge Fund Manager |
| fYxSQvuwOQc | 5 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg008, Stg121, Stg122, Stg123, Stg124 | same source parent plus 4 extracted candidate/module row(s); no duplicate flag | The Wedge Pop Swing Trading Setup - How a Trading Champion Enters a Position2026-05-03_fYxSQvuwOQc_quantlens_oliver_kell_cycle_intake |
| NGyE4YIgGpU | 4 | INTENTIONAL_SPLIT_OR_MODULES | Stg033, Stg167, Stg168, Stg169 | audit split signal present; 3 extracted child row(s), 1 source/parent row(s) | 2,115% Return in 1 Year How a Harvard Cancer Scientist Beat Wall Street |
| 9ZJK8175drM | 3 | INTENTIONAL_SPLIT_OR_MODULES | Stg001, Stg105, Stg106 | audit split signal present; 2 extracted child row(s), 1 source/parent row(s) | The 6 Steps to Learning Trading - Full Crash Course2026-05-03_9ZJK8175drM_quantlens_canslim_detailed_intake |
| VKNEJA5r8zw | 3 | LIKELY_INTENTIONAL_MULTI_MODULE | Stg133, Stg134, Stg135 | multiple extracted candidates share one source; no duplicate flag; max similarity=0.40 | +969% Return in 1 Year: The Pullback Strategy of a Trading Champion |
| c7ZSb2wNcOc | 3 | INTENTIONAL_SPLIT_OR_MODULES | Stg007, Stg114, Stg159 | audit split signal present; 2 extracted child row(s), 1 source/parent row(s) | The Slingshot Pullback Pattern - How To Trade Pullbacks2026-05-03_c7ZSb2wNcOc_quantlens_detailed_intake |
| DPA35Gug3Y4 | 2 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg019, Stg083 | same source parent plus 1 extracted candidate/module row(s); no duplicate flag | Gamer Trades $5k into over $1 Million with just a 30% Win Rate - Brian Lee Trades |
| HAN1kymVbTc | 2 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg025, Stg082 | same source parent plus 1 extracted candidate/module row(s); no duplicate flag | Trading $30 Million at Age 25 - The Story of Ted Zhang, Momentum Portfolio Manager |
| KWxhLIOchvY | 2 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg029, Stg102 | same source parent plus 1 extracted candidate/module row(s); no duplicate flag | 409% Return in 1 Year Aggressive Swing Trading Tactics and Setups |
| Nq-p7Bu1YT0 | 2 | INTENTIONAL_SPLIT_OR_MODULES | Stg034, Stg103 | audit split signal present; 1 extracted child row(s), 1 source/parent row(s) | How A Day Trader Turned into a Super-Performance Swing Trader - Real Simple Ariel |
| RHlsVNSM8Aw | 2 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg003, Stg095 | same source parent plus 1 extracted candidate/module row(s); no duplicate flag | 100% Most Effective MOVING AVERAGE (EMA) Trading Strategy / (Easy MA Crossover Strategy) |
| bRXO6F_vGjM | 2 | INTENTIONAL_SPLIT_OR_MODULES | Stg006, Stg170 | audit split signal present; 1 extracted child row(s), 1 source/parent row(s) | +382% Return in 1 Year - Why Most Traders FAIL at Shorting from a Trading ChampionQUANTLENS_TY_RAJNUS_MICROCAP_SHORT_INTAKE_REPORT |
| eWtY7uoJL_0 | 2 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg052, Stg104 | same source parent plus 1 extracted candidate/module row(s); no duplicate flag | Trading The Battle With Yourself  Market Wizard David Ryan |
| m8F3KkBDtC0 | 2 | SOURCE_PARENT_PLUS_EXTRACTED_CANDIDATES | Stg061, Stg172 | same source parent plus 1 extracted candidate/module row(s); no duplicate flag | The Wedge Pop Trading Setup of Trading Champion Oliver Kell |

## Candidate Detail

| Video ID | Stg | Candidate | Audit status | Blocked reason | Next step | Title |
|---|---|---|---|---|---|---|
| kTqKRi-j9kM | Stg056 | `QLR_kTqKRi-j9kM` | CANONICAL |  | Review | The 5 Essential Sell Rules from a Market Wizard - Linda Bradford Raschke |
| kTqKRi-j9kM | Stg125 | `QL_LBR_ADTR_POSITION_SIZING_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_LBR_ADTR_POSITION_SIZING_v0 |
| kTqKRi-j9kM | Stg126 | `QL_LBR_ATR_VOLATILITY_EXIT_OVERLAY_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_LBR_ATR_VOLATILITY_EXIT_OVERLAY_v0 |
| kTqKRi-j9kM | Stg127 | `QL_LBR_BOX_MIDPOINT_RECLAIM_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_LBR_BOX_MIDPOINT_RECLAIM_v0 |
| kTqKRi-j9kM | Stg128 | `QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0 |
| kTqKRi-j9kM | Stg129 | `QL_LBR_EQUITY_CURVE_RISK_THROTTLE_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_LBR_EQUITY_CURVE_RISK_THROTTLE_v0 |
| kTqKRi-j9kM | Stg130 | `QL_LBR_PREV_DAY_HIGH_LOW_TAYLOR_RHYTHM_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_LBR_PREV_DAY_HIGH_LOW_TAYLOR_RHYTHM_v0 |
| kTqKRi-j9kM | Stg131 | `QL_LBR_ROC2_REVERSAL_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_LBR_ROC2_REVERSAL_v0 |
| kTqKRi-j9kM | Stg132 | `QL_LBR_THREE_BAR_BREAKOUT_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_LBR_THREE_BAR_BREAKOUT_v0 |
| -JyH5PAJ4-Y | Stg009 | `QLR_-JyH5PAJ4-Y` | BLOCKED | wiki-only source | Source audit / park | I Stopped Trading So Much and My Profits Skyrocketed |
| -JyH5PAJ4-Y | Stg136 | `QL_NICK_10W_30W_RESPECT_ENTRY_001` | CANONICAL |  | Review | QL_NICK_10W_30W_RESPECT_ENTRY_001 |
| -JyH5PAJ4-Y | Stg138 | `QL_NICK_CONTROLLED_WEAKNESS_BASE_RETEST_001` | CANONICAL |  | Review | QL_NICK_CONTROLLED_WEAKNESS_BASE_RETEST_001 |
| -JyH5PAJ4-Y | Stg139 | `QL_NICK_EARNINGS_CUSHION_RULE_001` | CANONICAL |  | Review | QL_NICK_EARNINGS_CUSHION_RULE_001 |
| -JyH5PAJ4-Y | Stg140 | `QL_NICK_TRADE_FREQUENCY_GUARD_001` | CANONICAL |  | Review | QL_NICK_TRADE_FREQUENCY_GUARD_001 |
| -JyH5PAJ4-Y | Stg141 | `QL_NICK_UP_ON_VOLUME_RADAR_001` | CANONICAL |  | Review | QL_NICK_UP_ON_VOLUME_RADAR_001 |
| -JyH5PAJ4-Y | Stg144 | `QL_NICK_WEEKLY_CHARACTER_CHANGE_001` | CANONICAL |  | Review | QL_NICK_WEEKLY_CHARACTER_CHANGE_001 |
| -JyH5PAJ4-Y | Stg148 | `QL_NICK_WEEKLY_SELL_DECISION_FRAMEWORK_001` | CANONICAL |  | Review | QL_NICK_WEEKLY_SELL_DECISION_FRAMEWORK_001 |
| O0GpSPtmCuM | Stg036 | `QLR_O0GpSPtmCuM` | CANONICAL |  | Review | Stage Analysis Warnings for Current Markets - Exclusive Interview with Stan Weinstein |
| O0GpSPtmCuM | Stg160 | `QL_STAN_FAILED_RALLY_200D_SHORT_AVOID_v0` | CANONICAL |  | Review | QL_STAN_FAILED_RALLY_200D_SHORT_AVOID_v0 |
| O0GpSPtmCuM | Stg161 | `QL_STAN_FOREST_GROUP_TREE_FILTER_v0` | CANONICAL |  | Review | QL_STAN_FOREST_GROUP_TREE_FILTER_v0 |
| O0GpSPtmCuM | Stg162 | `QL_STAN_GOOD_COMPANY_BAD_CHART_BLOCK_v0` | CANONICAL |  | Review | QL_STAN_GOOD_COMPANY_BAD_CHART_BLOCK_v0 |
| O0GpSPtmCuM | Stg163 | `QL_STAN_SPLIT_TAPE_BREADTH_FILTER_v0` | CANONICAL |  | Review | QL_STAN_SPLIT_TAPE_BREADTH_FILTER_v0 |
| O0GpSPtmCuM | Stg164 | `QL_STAN_STAGE_1B_TO_2A_BREAKOUT_v0` | CANONICAL |  | Review | QL_STAN_STAGE_1B_TO_2A_BREAKOUT_v0 |
| O0GpSPtmCuM | Stg165 | `QL_STAN_STAGE_2A_PULLBACK_SUPPORT_v0` | CANONICAL |  | Review | QL_STAN_STAGE_2A_PULLBACK_SUPPORT_v0 |
| O0GpSPtmCuM | Stg166 | `QL_STAN_UNFILLED_GAP_CONTINUATION_v0` | CANONICAL |  | Review | QL_STAN_UNFILLED_GAP_CONTINUATION_v0 |
| _QewlGLBaeA | Stg048 | `QLR__QewlGLBaeA` | BLOCKED | rejected source classification | Source audit / park | Trading Millions How I Finally Became a Profitable Swing Trader |
| _QewlGLBaeA | Stg088 | `QL_ANTHONY_BACKWATCH_BREAKOUT_HEALTH_ENGINE_v0` | CANONICAL |  | Review | QL_ANTHONY_BACKWATCH_BREAKOUT_HEALTH_ENGINE_v0 |
| _QewlGLBaeA | Stg089 | `QL_ANTHONY_BREAKOUT_PULLBACK_RS_v0` | CANONICAL |  | Review | QL_ANTHONY_BREAKOUT_PULLBACK_RS_v0 |
| _QewlGLBaeA | Stg090 | `QL_ANTHONY_CYCLE_AWARE_EXPOSURE_CONTROL_v0` | CANONICAL |  | Review | QL_ANTHONY_CYCLE_AWARE_EXPOSURE_CONTROL_v0 |
| _QewlGLBaeA | Stg091 | `QL_ANTHONY_EP_EARNINGS_THEME_BREAKOUT_v0` | CANONICAL |  | Review | QL_ANTHONY_EP_EARNINGS_THEME_BREAKOUT_v0 |
| _QewlGLBaeA | Stg092 | `QL_ANTHONY_OUTLIER_LEADER_BREAKOUT_v0` | CANONICAL |  | Review | QL_ANTHONY_OUTLIER_LEADER_BREAKOUT_v0 |
| _QewlGLBaeA | Stg093 | `QL_ANTHONY_THEME_LEADERSHIP_ENGINE_v0` | CANONICAL |  | Review | QL_ANTHONY_THEME_LEADERSHIP_ENGINE_v0 |
| _QewlGLBaeA | Stg094 | `QL_ANTHONY_UNDERCUT_RECLAIM_LEADER_v0` | CANONICAL |  | Review | QL_ANTHONY_UNDERCUT_RECLAIM_LEADER_v0 |
| ivL6E6Lc6gM | Stg054 | `QLR_ivL6E6Lc6gM` | CANONICAL |  | Review | a Hedge Fund Manager Reveals his Perfect Pullback Trading Setup |
| ivL6E6Lc6gM | Stg107 | `QL_CHARLES_21EMA_PULLBACK_ADDON_001` | CANONICAL |  | Review | QL_CHARLES_21EMA_PULLBACK_ADDON_001 |
| ivL6E6Lc6gM | Stg108 | `QL_CHARLES_FIRST_PULLBACK_50DMA_001` | CANONICAL |  | Review | QL_CHARLES_FIRST_PULLBACK_50DMA_001 |
| ivL6E6Lc6gM | Stg109 | `QL_CHARLES_PRIOR_BASE_TOP_SUPPORT_PULLBACK_001` | CANONICAL |  | Review | QL_CHARLES_PRIOR_BASE_TOP_SUPPORT_PULLBACK_001 |
| ivL6E6Lc6gM | Stg110 | `QL_CHARLES_REVERSE_PYRAMID_PULLBACK_SCALEIN_001` | CANONICAL |  | Review | QL_CHARLES_REVERSE_PYRAMID_PULLBACK_SCALEIN_001 |
| ivL6E6Lc6gM | Stg111 | `QL_CHARLES_SWING_AROUND_CORE_001` | CANONICAL |  | Review | QL_CHARLES_SWING_AROUND_CORE_001 |
| ivL6E6Lc6gM | Stg112 | `QL_CHARLES_UPSIDE_REVERSAL_PULLBACK_001` | CANONICAL |  | Review | QL_CHARLES_UPSIDE_REVERSAL_PULLBACK_001 |
| ivL6E6Lc6gM | Stg113 | `QL_CHARLES_WEEKLY_SHAKEOUT_CONFIRMATION_GUARD_001` | CANONICAL |  | Review | QL_CHARLES_WEEKLY_SHAKEOUT_CONFIRMATION_GUARD_001 |
| 10pHBNVi4Jc | Stg010 | `QLR_10pHBNVi4Jc` | BLOCKED | rejected source classification | Source audit / park | The Trading Setups of the Record Breaking Trading Champion |
| 10pHBNVi4Jc | Stg115 | `QL_GON_HALT_MOMENTUM_CONTINUATION_v0` | CANONICAL |  | Review | QL_GON_HALT_MOMENTUM_CONTINUATION_v0 |
| 10pHBNVi4Jc | Stg116 | `QL_GON_NEXT_DAY_LOW_FLOAT_CONTINUATION_v0` | CANONICAL |  | Review | QL_GON_NEXT_DAY_LOW_FLOAT_CONTINUATION_v0 |
| 10pHBNVi4Jc | Stg117 | `QL_GON_OG_BULL_FLAG_HIGH_TIGHT_v0` | CANONICAL |  | Review | QL_GON_OG_BULL_FLAG_HIGH_TIGHT_v0 |
| 10pHBNVi4Jc | Stg118 | `QL_GON_SHORT_SQUEEZE_REVERSAL_BALL_UNDER_WATER_v0` | CANONICAL |  | Review | QL_GON_SHORT_SQUEEZE_REVERSAL_BALL_UNDER_WATER_v0 |
| 10pHBNVi4Jc | Stg119 | `QL_GON_STRONG_DEMAND_LOW_VOLUME_EMA_TOUCH_v0` | CANONICAL |  | Review | QL_GON_STRONG_DEMAND_LOW_VOLUME_EMA_TOUCH_v0 |
| 10pHBNVi4Jc | Stg120 | `QL_GON_STRONG_DEMAND_SLOW_FADER_RECLAIM_v0` | CANONICAL |  | Review | QL_GON_STRONG_DEMAND_SLOW_FADER_RECLAIM_v0 |
| 62OaP91Jz9k | Stg013 | `QLR_62OaP91Jz9k` | CANONICAL |  | Review | 120% Return A Simple Weekly Strategy Anyone Can Use |
| 62OaP91Jz9k | Stg137 | `QL_NICK_ASYMMETRIC_RISK_REWARD_FILTER_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_NICK_ASYMMETRIC_RISK_REWARD_FILTER_001 |
| 62OaP91Jz9k | Stg142 | `QL_NICK_UP_ON_VOLUME_UNIVERSE_SCAN_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_NICK_UP_ON_VOLUME_UNIVERSE_SCAN_001 |
| 62OaP91Jz9k | Stg143 | `QL_NICK_WEEKLY_BASE_TIGHTNESS_ACCUMULATION_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_NICK_WEEKLY_BASE_TIGHTNESS_ACCUMULATION_001 |
| 62OaP91Jz9k | Stg145 | `QL_NICK_WEEKLY_CHARACTER_CHANGE_TREND_STARTER_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_NICK_WEEKLY_CHARACTER_CHANGE_TREND_STARTER_001 |
| 62OaP91Jz9k | Stg146 | `QL_NICK_WEEKLY_CLOSE_STOP_POLICY_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_NICK_WEEKLY_CLOSE_STOP_POLICY_001 |
| 62OaP91Jz9k | Stg147 | `QL_NICK_WEEKLY_SCALE_IN_ON_PROOF_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_NICK_WEEKLY_SCALE_IN_ON_PROOF_001 |
| UmLa9FAlMgw | Stg043 | `QLR_UmLa9FAlMgw` | CANONICAL |  | Review | The AVWAP Trading Indicator Secrets and Setups Brian Shannon, CMT |
| UmLa9FAlMgw | Stg096 | `QL_BRIAN_SHANNON_5DMA_AVWAP_MOMENTUM_ENTRY_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_BRIAN_SHANNON_5DMA_AVWAP_MOMENTUM_ENTRY_v0 |
| UmLa9FAlMgw | Stg097 | `QL_BRIAN_SHANNON_AVWAP_GAP_PULLBACK_STRENGTH_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_BRIAN_SHANNON_AVWAP_GAP_PULLBACK_STRENGTH_v0 |
| UmLa9FAlMgw | Stg098 | `QL_BRIAN_SHANNON_AVWAP_HANDOFF_TREND_CONTINUATION_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_BRIAN_SHANNON_AVWAP_HANDOFF_TREND_CONTINUATION_v0 |
| UmLa9FAlMgw | Stg099 | `QL_BRIAN_SHANNON_AVWAP_PINCH_BREAKOUT_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_BRIAN_SHANNON_AVWAP_PINCH_BREAKOUT_v0 |
| UmLa9FAlMgw | Stg100 | `QL_BRIAN_SHANNON_BREAKAWAY_GAP_AVWAP_CONTINUATION_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_BRIAN_SHANNON_BREAKAWAY_GAP_AVWAP_CONTINUATION_v0 |
| UmLa9FAlMgw | Stg101 | `QL_BRIAN_SHANNON_FAILED_AVWAP_TRAP_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_BRIAN_SHANNON_FAILED_AVWAP_TRAP_v0 |
| KQRuUWSZvLE | Stg028 | `QLR_KQRuUWSZvLE` | BLOCKED | rejected source classification | Source audit / park | 10 Steps to Profitable Trading in 2024  Ryan Pierpont |
| KQRuUWSZvLE | Stg154 | `QL_RYAN_LATE_ENTRY_CHASE_FILTER_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_RYAN_LATE_ENTRY_CHASE_FILTER_001 |
| KQRuUWSZvLE | Stg155 | `QL_RYAN_MARKET_AWARENESS_GATE_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_RYAN_MARKET_AWARENESS_GATE_001 |
| KQRuUWSZvLE | Stg156 | `QL_RYAN_PULLBACK_DANGER_ZONE_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_RYAN_PULLBACK_DANGER_ZONE_001 |
| KQRuUWSZvLE | Stg157 | `QL_RYAN_SELL_INTO_STRENGTH_RUNNER_EXIT_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_RYAN_SELL_INTO_STRENGTH_RUNNER_EXIT_001 |
| KQRuUWSZvLE | Stg158 | `QL_RYAN_TIGHT_BREAKOUT_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_RYAN_TIGHT_BREAKOUT_001 |
| MnXQOt7_ZP0 | Stg032 | `QLR_MnXQOt7_ZP0` | CANONICAL |  | Review | +85% Return in 30 Days The AI Bull Market Can Change your Life Hedge Fund Manager |
| MnXQOt7_ZP0 | Stg149 | `QL_ROPPEL_357_SCALEOUT_RISK_MODULE_v0` | CANONICAL |  | Review | QL_ROPPEL_357_SCALEOUT_RISK_MODULE_v0 |
| MnXQOt7_ZP0 | Stg150 | `QL_ROPPEL_50D_RECLAIM_TIGHT_ACTION_v0` | CANONICAL |  | Review | QL_ROPPEL_50D_RECLAIM_TIGHT_ACTION_v0 |
| MnXQOt7_ZP0 | Stg151 | `QL_ROPPEL_EXTENSION_OVER_50D_HEDGE_SIGNAL_v0` | CANONICAL |  | Review | QL_ROPPEL_EXTENSION_OVER_50D_HEDGE_SIGNAL_v0 |
| MnXQOt7_ZP0 | Stg152 | `QL_ROPPEL_LEADERSHIP_THEME_SCORE_v0` | CANONICAL |  | Review | QL_ROPPEL_LEADERSHIP_THEME_SCORE_v0 |
| MnXQOt7_ZP0 | Stg153 | `QL_ROPPEL_POSITION_TRADING_HOLD_ENGINE_v0` | CANONICAL |  | Review | QL_ROPPEL_POSITION_TRADING_HOLD_ENGINE_v0 |
| fYxSQvuwOQc | Stg008 | `QLR_fYxSQvuwOQc` | BLOCKED | rejected source classification | Source audit / park | 2026-05-03_fYxSQvuwOQc_quantlens_oliver_kell_cycle_intake |
| fYxSQvuwOQc | Stg121 | `QL_KELL_BASIN_BREAK_001` | CANONICAL |  | Review | QL_KELL_BASIN_BREAK_001 |
| fYxSQvuwOQc | Stg122 | `QL_KELL_EMA_CROSSBACK_001` | CANONICAL |  | Review | QL_KELL_EMA_CROSSBACK_001 |
| fYxSQvuwOQc | Stg123 | `QL_KELL_WEDGE_DROP_EXIT_001` | CANONICAL |  | Review | QL_KELL_WEDGE_DROP_EXIT_001 |
| fYxSQvuwOQc | Stg124 | `QL_KELL_WEDGE_POP_001` | CANONICAL |  | Review | QL_KELL_WEDGE_POP_001 |
| NGyE4YIgGpU | Stg033 | `QLR_NGyE4YIgGpU` | CANONICAL |  | Review | 2,115% Return in 1 Year How a Harvard Cancer Scientist Beat Wall Street |
| NGyE4YIgGpU | Stg167 | `QL_TITO_OPTIONS_AWARE_RISK_OVERLAY_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_TITO_OPTIONS_AWARE_RISK_OVERLAY_v0 |
| NGyE4YIgGpU | Stg168 | `QL_TITO_PROFIT_WITHDRAWAL_CAPITAL_AT_RISK_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_TITO_PROFIT_WITHDRAWAL_CAPITAL_AT_RISK_v0 |
| NGyE4YIgGpU | Stg169 | `QL_TITO_RS_MOMENTUM_BREAKOUT_CROSSBACK_v0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_TITO_RS_MOMENTUM_BREAKOUT_CROSSBACK_v0 |
| 9ZJK8175drM | Stg001 | `QLR_9ZJK8175drM` | BLOCKED | rejected source classification | Source audit / park | 2026-05-03_9ZJK8175drM_quantlens_canslim_detailed_intake |
| 9ZJK8175drM | Stg105 | `QL_CANSLIM_O_NEIL_GROWTH_STOCK_SYSTEM` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_CANSLIM_O_NEIL_GROWTH_STOCK_SYSTEM |
| 9ZJK8175drM | Stg106 | `QL_CANSLIM_SHAKEOUT_PLUS_3_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_CANSLIM_SHAKEOUT_PLUS_3_001 |
| VKNEJA5r8zw | Stg133 | `QL_MARTIN_PARABOLIC_LONG_001` | CANONICAL |  | Review | QL_MARTIN_PARABOLIC_LONG_001 |
| VKNEJA5r8zw | Stg134 | `QL_MARTIN_PULLBACK_CONFLUENCE_LONG_001` | CANONICAL |  | Review | QL_MARTIN_PULLBACK_CONFLUENCE_LONG_001 |
| VKNEJA5r8zw | Stg135 | `QL_MARTIN_PULLBACK_SHORT_001` | CANONICAL |  | Review | QL_MARTIN_PULLBACK_SHORT_001 |
| c7ZSb2wNcOc | Stg007 | `QLR_c7ZSb2wNcOc` | BLOCKED | rejected source classification | Source audit / park | 2026-05-03_c7ZSb2wNcOc_quantlens_detailed_intake |
| c7ZSb2wNcOc | Stg114 | `QL_FISHHOOK_EP_DAY1_RETAKE_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_FISHHOOK_EP_DAY1_RETAKE_001 |
| c7ZSb2wNcOc | Stg159 | `QL_SLINGSHOT_4EMA_HIGH_PULLBACK_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_SLINGSHOT_4EMA_HIGH_PULLBACK_001 |
| DPA35Gug3Y4 | Stg019 | `QLR_DPA35Gug3Y4` | CANONICAL |  | Review | Gamer Trades $5k into over $1 Million with just a 30% Win Rate - Brian Lee Trades |
| DPA35Gug3Y4 | Stg083 | `CAND_BRIAN_LEE_SMALLCAP_GAP_MR_SHORT_V1` | CANONICAL |  | Review | CAND_BRIAN_LEE_SMALLCAP_GAP_MR_SHORT_V1 |
| HAN1kymVbTc | Stg025 | `QLR_HAN1kymVbTc` | CANONICAL |  | Review | Trading $30 Million at Age 25 - The Story of Ted Zhang, Momentum Portfolio Manager |
| HAN1kymVbTc | Stg082 | `CAND_20260503_TED_ZHANG_MAGIC_ELIXIR_MOMENTUM_HAN1kymVbTc` | CANONICAL |  | Review | CAND_20260503_TED_ZHANG_MAGIC_ELIXIR_MOMENTUM_HAN1kymVbTc |
| KWxhLIOchvY | Stg029 | `QLR_KWxhLIOchvY` | BLOCKED | rejected source classification | Source audit / park | 409% Return in 1 Year Aggressive Swing Trading Tactics and Setups |
| KWxhLIOchvY | Stg102 | `QL_CAND_003_KWxhLIOchvY` | BLOCKED | rejected source classification | Source audit / park | QL_CAND_003_KWxhLIOchvY |
| Nq-p7Bu1YT0 | Stg034 | `QLR_Nq-p7Bu1YT0` | BLOCKED | rejected source classification | Source audit / park | How A Day Trader Turned into a Super-Performance Swing Trader - Real Simple Ariel |
| Nq-p7Bu1YT0 | Stg103 | `QL_CAND_004_Nq-p7Bu1YT0` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_CAND_004_Nq-p7Bu1YT0 |
| RHlsVNSM8Aw | Stg003 | `QLR_RHlsVNSM8Aw` | BLOCKED | rejected source classification | Source audit / park | QUANTLENS_EMA20_50_RETEST_CRITICAL_INTAKE_REPORT |
| RHlsVNSM8Aw | Stg095 | `QL_BASELINE_EMA20_50_RETEST_001` | CANONICAL |  | Review | QL_BASELINE_EMA20_50_RETEST_001 |
| bRXO6F_vGjM | Stg006 | `QLR_bRXO6F_vGjM` | BLOCKED | rejected source classification | Source audit / park | QUANTLENS_TY_RAJNUS_MICROCAP_SHORT_INTAKE_REPORT |
| bRXO6F_vGjM | Stg170 | `QL_TY_MICROCAP_LIQUIDITY_REVERSION_SHORT_001` | SPLIT_REQUIRED | needs indicator split | Split into indicator cases | QL_TY_MICROCAP_LIQUIDITY_REVERSION_SHORT_001 |
| eWtY7uoJL_0 | Stg052 | `QLR_eWtY7uoJL_0` | CANONICAL |  | Review | Trading The Battle With Yourself  Market Wizard David Ryan |
| eWtY7uoJL_0 | Stg104 | `QL_CAND_2026-05-03_eWtY7uoJL0_RYAN_PRICE_VOLUME_STAGE` | CANONICAL |  | Review | QL_CAND_2026-05-03_eWtY7uoJL0_RYAN_PRICE_VOLUME_STAGE |
| m8F3KkBDtC0 | Stg061 | `QLR_m8F3KkBDtC0` | CANONICAL |  | Review | The Wedge Pop Trading Setup of Trading Champion Oliver Kell |
| m8F3KkBDtC0 | Stg172 | `YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1` | CANONICAL |  | Review | YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1 |
