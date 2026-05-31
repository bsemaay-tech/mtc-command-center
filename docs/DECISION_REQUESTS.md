# Approval Request

## Proposed Folder Structure
~~~text
C:\LAB\Tradingview_LAB_CLEAN
├── README.md
├── .gitignore
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── .chatgpt-instructions.md
├── .cursorrules
├── .vscode
├── docs
└── MTC_COMMAND_CENTER
    ├── _AI_MEMORY
    ├── 01_MTC_PROJECT
    ├── 02_MTC_BACKTEST
    ├── 03_QUANTLENS
    ├── 04_SHARED
    └── 99_ASSETS
~~~

## Exact Source Folders Proposed for Migration
- `C:\LAB\tradingview-lab\MTC_COMMAND_CENTER`
- `C:\LAB\tradingview-lab\mtc_backtest`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\MTC_V2_PORTABLE_HANDOFF`
- `C:\LAB\tradingview-lab\20_MODULES_REUSABLE`
- `C:\LAB\tradingview-lab\30_PROMPTS`
- `C:\LAB\tradingview-lab\tools\parity`
- `C:\LAB\tradingview-lab\scripts`
- `C:\LAB\tradingview-lab\60_SCREENSHOOTS` only for approved referenced assets.

## Exact Target Folders Proposed
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\01_MTC_PROJECT`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\02_MTC_BACKTEST`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\04_SHARED`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\99_ASSETS\screenshots`
- `C:\LAB\Tradingview_LAB_CLEAN\docs`

## Source-of-Truth and Conflicts
- Source-of-truth: legacy `C:\LAB\tradingview-lab\MTC_COMMAND_CENTER` is canonical and should be copied byte-for-byte to the clean `MTC_COMMAND_CENTER` after approval.
- `01_MASTER TEMPLATE_V2\MTC_V2_PORTABLE_HANDOFF` is not canonical when byte-identical duplicates exist; it should be used as handoff/archive input and condensed into AI memory.
- Duplicate files such as `Agents.md`, `Claude.md`, and `SETUP_WINDOWS.md` between V2 and portable handoff should resolve to the V2/current command-center version unless hashes prove the portable copy is uniquely newer.
- `external\traderspost-command-dash` and `MTC_COMMAND_CENTER\08_DASHBOARD_APP` require a Phase 0B relation check before either is treated as canonical dashboard code.

## High-Risk Items
- Root scripts with hardcoded path dependencies: `add_htf_cols.py, add_l12_cases.py, mtc_bridge.mjs, optimize.py, parity_compare.py`.
- Pine/parity files must be byte-preserved and checksum-verified.
- QuantLens pipeline buckets are not strategies.
- Dashboard canonical source remains unresolved.

## NEEDS_BARIS_DECISION Items
- Git strategy.
- Dashboard canonical source.
- Root script placement and path rewrite policy.
- QuantLens STG naming approval.
- Old reports/memory archive policy.

## Git Strategy Decision
- A. New clean repo with fresh git init and no old history.
- B. Preserve selected history using a git subtree/filter-repo-style plan.
- C. Keep clean folder outside git until manually reviewed.

Recommended: A unless old history is required.

## QuantLens STG Naming Decision Table
Corrected STG count: `46`. The requested detection rules produce 46 real strategy directories in this repository; pipeline buckets and parent folders are excluded.

| STG | Candidate source | Proposed target path | Bucket | Evidence | Confidence | Needs Barış? |
| --- | --- | --- | --- | --- | --- | --- |
| STG001_alpha_ada_two_candle_sr_1h | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_ALPHA_ADA_TWO_CANDLE_SR_1H | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG001_alpha_ada_two_candle_sr_1h | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG002_alpha_link_8ema_1h | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_ALPHA_LINK_8EMA_1H | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG002_alpha_link_8ema_1h | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG003_alpha_ltc_rsi_oversold_1h | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_ALPHA_LTC_RSI_OVERSOLD_1H | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG003_alpha_ltc_rsi_oversold_1h | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG004_avwap_brian_earnings_anchor_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_AVWAP_BRIAN_EARNINGS_ANCHOR_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG004_avwap_brian_earnings_anchor_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG005_avwap_brian_gap_reclaim_5m | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_AVWAP_BRIAN_GAP_RECLAIM_5M | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG005_avwap_brian_gap_reclaim_5m | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG006_avwap_brian_intraday_or_5m | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_AVWAP_BRIAN_INTRADAY_OR_5M | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG006_avwap_brian_intraday_or_5m | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG007_avwap_brian_stage2_emerging_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_AVWAP_BRIAN_STAGE2_EMERGING_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG007_avwap_brian_stage2_emerging_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG008_connell_event_driven_gap_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_CONNELL_EVENT_DRIVEN_GAP_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG008_connell_event_driven_gap_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG009_connell_event_driven_gap_5m | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_CONNELL_EVENT_DRIVEN_GAP_5M | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG009_connell_event_driven_gap_5m | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG010_deepak_153_filter_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_DEEPAK_153_FILTER_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG010_deepak_153_filter_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG011_deepak_259_risk_overlay | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_DEEPAK_259_RISK_OVERLAY | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG011_deepak_259_risk_overlay | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG012_deepak_snapback_50sma_intraday | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_DEEPAK_SNAPBACK_50SMA_INTRADAY | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG012_deepak_snapback_50sma_intraday | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG013_episodic_pivot_christian_5m | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_EPISODIC_PIVOT_CHRISTIAN_5M | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG013_episodic_pivot_christian_5m | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG014_highest_volume_edge_proswing_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_HIGHEST_VOLUME_EDGE_PROSWING_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG014_highest_volume_edge_proswing_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG015_launchpad_proswing_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_LAUNCHPAD_PROSWING_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG015_launchpad_proswing_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG016_open_range_5pct_stop_christian_5m | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG016_open_range_5pct_stop_christian_5m | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG017_rs_phase_days_proswing_overlay | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_RS_PHASE_DAYS_PROSWING_OVERLAY | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG017_rs_phase_days_proswing_overlay | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG018_sell_rules_market_wizards_overlay | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_SELL_RULES_MARKET_WIZARDS_OVERLAY | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG018_sell_rules_market_wizards_overlay | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG019_trail_20ma_christian_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_TRAIL_20MA_CHRISTIAN_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG019_trail_20ma_christian_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG020_vcp_early_entry_christian_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_VCP_EARLY_ENTRY_CHRISTIAN_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG020_vcp_early_entry_christian_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG021_vcp_minervini_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_VCP_MINERVINI_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG021_vcp_minervini_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG022_vcp_richard_1d | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\QL_VCP_RICHARD_1D | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG022_vcp_richard_1d | promoted_to_parity | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG023_kell_wedge_pop_crossback | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\01_kell_wedge_pop_crossback | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG023_kell_wedge_pop_crossback | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG024_martin_luke_pullback_avwap | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\02_martin_luke_pullback_avwap | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG024_martin_luke_pullback_avwap | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG025_slingshot_4ema_high_pullback | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\03_slingshot_4ema_high_pullback | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG025_slingshot_4ema_high_pullback | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG026_crabel_range_expansion_stage2 | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\04_crabel_range_expansion_stage2 | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG026_crabel_range_expansion_stage2 | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG027_bigbeluga_rsi_choch_atr | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\05_bigbeluga_rsi_choch_atr | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG027_bigbeluga_rsi_choch_atr | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG028_canslim_shakeout_plus3 | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\06_canslim_shakeout_plus3 | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG028_canslim_shakeout_plus3 | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG029_linda_5sma_rs_pullback | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\07_linda_5sma_rs_pullback | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG029_linda_5sma_rs_pullback | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG030_linda_8am_opening_range | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\08_linda_8am_opening_range | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG030_linda_8am_opening_range | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG031_highbeta_openingbar_gapandgo | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\09_highbeta_openingbar_gapandgo | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG031_highbeta_openingbar_gapandgo | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG032_ty_microcap_short | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\10_ty_microcap_short | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG032_ty_microcap_short | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG033_daily_extension_anti_chase_filter | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\11_daily_extension_anti_chase_filter | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG033_daily_extension_anti_chase_filter | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG034_ema20_50_two_retests_baseline | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\12_ema20_50_two_retests_baseline | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG034_ema20_50_two_retests_baseline | audited_research_batch | Real strategy directory matched approved STG detection rule. | High | Yes |
| STG035_2026_05_01_any_1h_rsi_confluence_playboo | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG035_2026_05_01_any_1h_rsi_confluence_playboo | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG036_2026_05_01_any_bollinger_bands_20_2_tri | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG036_2026_05_01_any_bollinger_bands_20_2_tri | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG037_2026_05_01_any_candlestick_7_pattern_pa | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG037_2026_05_01_any_candlestick_7_pattern_pa | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG038_2026_05_01_liquid_intraday_vwap_pullback | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG038_2026_05_01_liquid_intraday_vwap_pullback | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG039_2026_05_01_sp500_5m_two_candle_sentiment | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG039_2026_05_01_sp500_5m_two_candle_sentiment | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG040_2026_05_01_swing_1h_dual_rsi_60_40_pullb | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG040_2026_05_01_swing_1h_dual_rsi_60_40_pullb | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG041_2026_05_01_unknown_multi_ema_channel_pul | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG041_2026_05_01_unknown_multi_ema_channel_pul | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG042_2026_05_01_us_equities_10m_8ema_pullback | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG042_2026_05_01_us_equities_10m_8ema_pullback | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG043_2026_05_01_us_equities_intraday_8ema_exi | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG043_2026_05_01_us_equities_intraday_8ema_exi | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG044_2026_05_01_us_equities_intraday_le_model | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG044_2026_05_01_us_equities_intraday_le_model | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG045_2026_05_01_us_equities_intraday_purple_p | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES\QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG045_2026_05_01_us_equities_intraday_purple_p | triaged_candidate | Real strategy directory matched approved STG detection rule. | Medium | Yes |
| STG046_r215f4fj7v8 | C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\strategy_sandboxes\QLR_R215f4fj7V8 | C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG046_r215f4fj7v8 | sandbox | Real strategy directory matched approved STG detection rule. | Medium | Yes |

## Approval Checklist
[ ] Target structure approved
[ ] Migration map approved
[ ] Exclusions approved
[ ] Deprecated/archive decisions approved
[ ] AI memory system approved
[ ] QuantLens STG naming approved
[ ] Git strategy approved
[ ] Future apply_migration.ps1 plan approved
[ ] Future verify_migration.ps1 plan approved
[ ] Barış requested revisions instead of approval

## Approval Protocol
If approved, reply exactly:

~~~text
APPROVE_PHASE_1_MIGRATION
~~~

If revisions are needed, reply exactly:

~~~text
REVISION_REQUEST:
~~~

If deeper Phase 0 detail is needed, reply exactly:

~~~text
APPROVE_PHASE_0B_DETAIL:
~~~
