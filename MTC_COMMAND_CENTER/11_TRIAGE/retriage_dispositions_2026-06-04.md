# Re-Triage Dispositions — 2026-06-04

Disposition decisions for re-triaged candidates (transcripts now present). Each
row records the call: CANDIDATE (-> new strategy folder), WIKI_ONLY, SALVAGE, or
DUPLICATE/MERGE. Pilot batch (3) below; continue appending.

| Stg | Candidate | Disposition | Action taken | Notes |
|---|---|---|---|---|
| Stg083 | CAND_BRIAN_LEE_SMALLCAP_GAP_MR_SHORT_V1 | **CANDIDATE** | Created `03_QUANTLENS/strategies/STG047_brian_lee_smallcap_gap_mr_short` (metadata + deterministic spec + transcript copied) | Day-trading short-only small-cap gap MR. Discretionary; not prototyped. |
| Stg082 | TED_ZHANG_MAGIC_ELIXIR_MOMENTUM | **WIKI_ONLY** | No strategy folder. Belongs in `03_QUANTLENS/11_TRADER_WIKI` (thematic momentum / CANSLIM philosophy) | Podcast interview. Reusable as SALVAGE: stage-2 + ADR/linearity screen criteria. Not a closed rule set. |
| Stg087 | (labeled QL_ALPHA_LINK_8EMA_1H) 8EMA pullback + 8EMA trailing exit | **DUPLICATE / MERGE** | No new folder. Salvage "8EMA trailing exit" as a reusable trailing module | candidate_id collides with existing STG002; concept overlaps STG042 (8ema_pullback) and STG043 (8ema_exit_trail). |

## How dispositions map to the pipeline
- **CANDIDATE** -> new `STGxxx_*` folder under `03_QUANTLENS/strategies/`; re-run
  `build_strategy_research_registry.py`.
- **WIKI_ONLY** -> `03_QUANTLENS/11_TRADER_WIKI/` (knowledge, no strategy).
- **SALVAGE** -> note reusable component(s); no standalone strategy.
- **DUPLICATE/MERGE** -> point to the existing strategy; salvage any new module.

## Pilot finding
Top-3 HIGH eligible candidates were all interview/educational videos: 1 CANDIDATE,
1 WIKI, 1 DUPLICATE. Expect the remaining ~87 eligible to yield far fewer than 87
new strategies — most need WIKI/SALVAGE/DUPLICATE dispositions, not folders.

## Bulk re-triage log (RESEARCH-004)

| Stg | Disposition | Output | Note |
|---|---|---|---|
| Stg084 | DUPLICATE | STG042_ql_2026_05_01_us_equities_10m_8ema_pullback | exact candidate_id match |
| Stg085 | DUPLICATE | STG044_ql_2026_05_01_us_equities_intraday_le_model_bull_flag | exact candidate_id match |
| Stg086 | DUPLICATE | STG045_ql_2026_05_01_us_equities_intraday_purple_profits | exact candidate_id match |
| Stg088 | CANDIDATE | STG048_anthony_layered_leadership_swing_system | Anthony system sub-setup angle |
| Stg089 | CANDIDATE | STG048_anthony_layered_leadership_swing_system | Anthony system sub-setup angle |
| Stg090 | CANDIDATE | STG048_anthony_layered_leadership_swing_system | Anthony system sub-setup angle |
| Stg091 | CANDIDATE | STG048_anthony_layered_leadership_swing_system | Anthony system sub-setup angle |
| Stg092 | CANDIDATE | STG048_anthony_layered_leadership_swing_system | Anthony system sub-setup angle |
| Stg093 | CANDIDATE | STG048_anthony_layered_leadership_swing_system | Anthony system sub-setup angle |
| Stg094 | CANDIDATE | STG048_anthony_layered_leadership_swing_system | Anthony system sub-setup angle |
| Stg095 | DUPLICATE | STG034_12_ema20_50_two_retests_baseline | source video of existing baseline; transcript attached for provenance |
| Stg096 | CANDIDATE | STG049_brian_shannon_avwap_methodology | AVWAP setup angle |
| Stg097 | CANDIDATE | STG049_brian_shannon_avwap_methodology | AVWAP setup angle |
| Stg098 | CANDIDATE | STG049_brian_shannon_avwap_methodology | AVWAP setup angle |
| Stg099 | CANDIDATE | STG049_brian_shannon_avwap_methodology | AVWAP setup angle |
| Stg100 | CANDIDATE | STG049_brian_shannon_avwap_methodology | AVWAP setup angle |
| Stg101 | CANDIDATE | STG049_brian_shannon_avwap_methodology | AVWAP setup angle |
| Stg103 | CANDIDATE | STG050_ariel_market_timed_momentum_swing | Ariel momentum swing; overlaps STG048 |
| Stg104 | CANDIDATE | STG051_david_ryan_price_volume_stage | price-volume-stage; reusable accumulation filter |
| Stg105 | CANDIDATE | STG052_canslim_oneil_growth_system | full CANSLIM system + sell rules |
| Stg106 | DUPLICATE | STG028_06_canslim_shakeout_plus3 | shakeout+3 already exists; transcript attached |
| Stg107 | CANDIDATE | STG053_charles_harris_pullback_around_core | Charles Harris pullback setup angle |
| Stg108 | CANDIDATE | STG053_charles_harris_pullback_around_core | Charles Harris pullback setup angle |
| Stg109 | CANDIDATE | STG053_charles_harris_pullback_around_core | Charles Harris pullback setup angle |
| Stg110 | CANDIDATE | STG053_charles_harris_pullback_around_core | Charles Harris pullback setup angle |
| Stg111 | CANDIDATE | STG053_charles_harris_pullback_around_core | Charles Harris pullback setup angle |
| Stg112 | CANDIDATE | STG053_charles_harris_pullback_around_core | Charles Harris pullback setup angle |
| Stg113 | CANDIDATE | STG053_charles_harris_pullback_around_core | Charles Harris pullback setup angle |
| Stg114 | CANDIDATE | STG054_fishhook_ep_day1_retake | fishhook EP; slingshot=STG025 |
| Stg159 | DUPLICATE | STG025_03_slingshot_4ema_high_pullback | slingshot 4ema; transcript attached |
| Stg115 | CANDIDATE | STG055_gon_lowfloat_momentum_daytrading | Gon low-float momentum setup angle |
| Stg116 | CANDIDATE | STG055_gon_lowfloat_momentum_daytrading | Gon low-float momentum setup angle |
| Stg117 | CANDIDATE | STG055_gon_lowfloat_momentum_daytrading | Gon low-float momentum setup angle |
| Stg118 | CANDIDATE | STG055_gon_lowfloat_momentum_daytrading | Gon low-float momentum setup angle |
| Stg119 | CANDIDATE | STG055_gon_lowfloat_momentum_daytrading | Gon low-float momentum setup angle |
| Stg120 | CANDIDATE | STG055_gon_lowfloat_momentum_daytrading | Gon low-float momentum setup angle |
| Stg121 | CANDIDATE | STG056_oliver_kell_price_cycle | Kell cycle setup angle; overlaps STG023 |
| Stg122 | CANDIDATE | STG056_oliver_kell_price_cycle | Kell cycle setup angle; overlaps STG023 |
| Stg123 | CANDIDATE | STG056_oliver_kell_price_cycle | Kell cycle setup angle; overlaps STG023 |
| Stg124 | CANDIDATE | STG056_oliver_kell_price_cycle | Kell cycle setup angle; overlaps STG023 |
| Stg125 | CANDIDATE | STG057_linda_raschke_lbr_toolkit | LBR setup/module angle |
| Stg126 | CANDIDATE | STG057_linda_raschke_lbr_toolkit | LBR setup/module angle |
| Stg127 | CANDIDATE | STG057_linda_raschke_lbr_toolkit | LBR setup/module angle |
| Stg128 | CANDIDATE | STG057_linda_raschke_lbr_toolkit | LBR setup/module angle |
| Stg129 | CANDIDATE | STG057_linda_raschke_lbr_toolkit | LBR setup/module angle |
| Stg130 | CANDIDATE | STG057_linda_raschke_lbr_toolkit | LBR setup/module angle |
| Stg131 | CANDIDATE | STG057_linda_raschke_lbr_toolkit | LBR setup/module angle |
| Stg132 | CANDIDATE | STG057_linda_raschke_lbr_toolkit | LBR setup/module angle |
| Stg133 | CANDIDATE | STG058_martin_parabolic_pullback_champion | Martin parabolic/pullback angle |
| Stg134 | CANDIDATE | STG058_martin_parabolic_pullback_champion | Martin parabolic/pullback angle |
| Stg135 | CANDIDATE | STG058_martin_parabolic_pullback_champion | Martin parabolic/pullback angle |
| Stg136 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg137 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg138 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg139 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg140 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg141 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg142 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg143 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg144 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg145 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg146 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg147 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg148 | CANDIDATE | STG059_nick_weekly_stage_methodology | Nick weekly stage angle |
| Stg149 | CANDIDATE | STG060_roppel_leadership_position_trading | Roppel leadership angle |
| Stg150 | CANDIDATE | STG060_roppel_leadership_position_trading | Roppel leadership angle |
| Stg151 | CANDIDATE | STG060_roppel_leadership_position_trading | Roppel leadership angle |
| Stg152 | CANDIDATE | STG060_roppel_leadership_position_trading | Roppel leadership angle |
| Stg153 | CANDIDATE | STG060_roppel_leadership_position_trading | Roppel leadership angle |
| Stg154 | promoted_to_matured_strategy | STG061_ryan_pierpont_breakout_discipline | Ryan breakout guard module |
| Stg155 | promoted_to_matured_strategy | STG061_ryan_pierpont_breakout_discipline | Ryan market gate module |
| Stg156 | promoted_to_matured_strategy | STG061_ryan_pierpont_breakout_discipline | Ryan danger-zone module |
| Stg157 | promoted_to_matured_strategy | STG061_ryan_pierpont_breakout_discipline | Ryan sell-into-strength runner module |
| Stg158 | promoted_to_matured_strategy | STG061_ryan_pierpont_breakout_discipline | Ryan tight breakout module |
| Stg160 | promoted_to_matured_strategy | STG062_stan_weinstein_stage_analysis | Stan failed rally/200d avoid module |
| Stg161 | promoted_to_matured_strategy | STG062_stan_weinstein_stage_analysis | Stan group-tree filter module |
| Stg162 | promoted_to_matured_strategy | STG062_stan_weinstein_stage_analysis | Stan good-company bad-chart block |
| Stg163 | promoted_to_matured_strategy | STG062_stan_weinstein_stage_analysis | Stan split-tape breadth filter |
| Stg164 | promoted_to_matured_strategy | STG062_stan_weinstein_stage_analysis | Stan Stage 1B-to-2A breakout |
| Stg165 | promoted_to_matured_strategy | STG062_stan_weinstein_stage_analysis | Stan Stage 2A pullback support |
| Stg166 | promoted_to_matured_strategy | STG062_stan_weinstein_stage_analysis | Stan unfilled gap continuation |
| Stg167 | needs_manual_review | STG063_tito_options_aware_rs_breakout | Tito options risk overlay partial spec |
| Stg168 | needs_manual_review | STG063_tito_options_aware_rs_breakout | Tito profit withdrawal risk module partial spec |
| Stg169 | needs_manual_review | STG063_tito_options_aware_rs_breakout | Tito RS breakout crossback partial spec |
| Stg170 | duplicate_existing_strategy | STG032_10_ty_microcap_short | Ty microcap short duplicate; transcript attached |
| Stg171 | duplicate_existing_strategy | STG022_ql_vcp_richard_1d | VCP duplicate; transcript attached |
| Stg172 | duplicate_existing_strategy | STG056_oliver_kell_price_cycle | Oliver Kell duplicate; transcript attached |
