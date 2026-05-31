# QuantLens Intake Report — Tito Adhikary / Options Momentum Breakout

```yaml
report_type: QuantLens Strategy Intake
source_title: "2,115% Return in 1 Year: How a Harvard Cancer Scientist Beat Wall Street"
source_url: "https://youtu.be/NGyE4YIgGpU?si=gj_6ZcIyjUFAEGhk"
speaker: "Tito Adhikary"
podcast: "TraderLion / Richard Moglen"
created_at: "2026-05-03"
status: "INTAKE_ONLY"
backtest_run: false
pine_implemented: false
production_runner_modified: false
```

---

## 1. Executive Verdict

```yaml
verdict: CANDIDATE_AS_OPTIONS_RISK_EXECUTION_OVERLAY
direct_mtc_producer_candidate: false
python_research_candidate: true
pine_now: false
priority:
  risk_module: VERY_HIGH
  entry_model: MEDIUM_HIGH
  options_wrapper: HIGH_FOR_US_EQUITIES_ONLY
  crypto_transferability: MEDIUM
  trader_wiki_value: VERY_HIGH
```

Bu video tek başına bağımsız bir “MTC producer” olarak alınmamalı. Asıl değer şu üç katmanda:

1. **Momentum setup seçimi:** güçlü hisse / güçlü sektör / güçlü piyasa bağlamı.
2. **Options execution wrapper:** aynı teknik setup’ı hisse yerine opsiyonla trade etme mantığı.
3. **Risk ve davranış modülü:** net liquidation bazlı risk, günlük/haftalık/aylık circuit breaker, mental equity curve, profit withdrawal.

Bu nedenle bu video QuantLens içinde **entry producer’dan çok risk-management, sizing, execution ve options-wrapper** referansı olarak tutulmalı.

---

## 2. Video Kalitesi ve Güvenilirlik Notu

```yaml
quality_assessment:
  channel_quality: high
  trader_track_record_claim: high_but_external_verification_required
  specificity: medium_high
  backtest_specificity: medium
  execution_specificity: high
  risk_specificity: very_high
  immediate_python_testability: medium
  direct_crypto_transferability: medium
```

Güçlü taraflar:

- Konuşmacı açık şekilde kayıplarını, hatalarını ve süreç dönüşümünü anlatıyor.
- Sadece “setup” değil; **risk, psikoloji, position sizing ve drawdown sonrası davranış** anlatılıyor.
- Opsiyon kullanımı, IV, expiry/strike seçimi ve spread yapıları pratik şekilde açıklanıyor.
- Piyasa rejimi filtresi net: QQQ/SPY kısa vadeli ortalamaların altındaysa A+ sizing yapmıyor.

Zayıf taraflar:

- Setup’lar tamamen mekanik kurala çevrilmiş değil.
- Options getirileri doğrudan OHLC backtest ile ölçülemez; option chain / IV / greeks verisi gerekir.
- US equity/options odaklıdır; crypto’ya doğrudan taşınamaz.
- “2,115%” performans örneği çok etkileyici olsa da strategy robustness kanıtı değildir; özellikle options convexity ve 2025 market regime etkisi ayrıştırılmalı.

---

## 3. Ana Strateji Özeti

```yaml
style:
  direction:
    - long_primary
    - selective_short_possible
  instrument:
    - listed_options_primary
    - underlying_stock_analysis
    - occasional_leaps
    - occasional_debit_spreads
    - occasional_credit_spreads
    - leveraged_single_stock_etfs_possible
  holding_period:
    - intraday
    - multi_day
    - occasionally_multi_week
  core_philosophy:
    - price_is_king
    - right_stock
    - right_sector
    - right_market
    - respect_market_regime
    - use_options_only_after_underlying_setup_is_valid
```

Konuşmacının ana çerçevesi:

> Önce underlying chart setup doğrulanır. Opsiyon sadece trade aracıdır; setup opsiyon grafiğinden değil, hisse grafiğinden gelir.

Bu, QuantLens için önemli: **sinyal producer underlying OHLC’den çıkarılmalı; opsiyon tarafı ayrı execution/risk wrapper olmalı.**

---

## 4. En Önemli Çıkarımlar

## 4.1 Right Stock / Right Sector / Right Market

```yaml
selection_stack:
  right_stock:
    - relative_strength_vs_index
    - tight_setup
    - bull_flag_or_pennant_or_wedge
    - volume_dry_up_before_breakout
    - volume_confirmation_on_breakout
    - catalyst_preferred
    - sales_earnings_growth_preferred
  right_sector:
    - multiple_leaders_in_same_theme
    - sector_tailwind
    - AI_semis_energy_crypto_space_examples
  right_market:
    - QQQ_SPY_above_short_term_MAs_preferred
    - market_supports_breakouts
    - reduce_size_when_indices_under_short_term_MAs
```

Bu bölüm önceki Oliver Kell / VCP / Martin pullback videolarıyla örtüşüyor. Farkı, Tito’nun bunu opsiyon risk yapısına bağlaması.

---

## 4.2 Setup Tipleri

Transcriptte tekrarlanan trade setup ailesi:

```yaml
setups:
  - bull_flag
  - pennant
  - wedge
  - volatility_compression
  - squeeze_or_VCP_style_base
  - crossback
  - multi_week_base
  - SMA_surfing
  - earnings_reaction_red_to_green
  - breakout_after_volume_dry_up
```

Objektifleştirilebilir sinyaller:

```yaml
objective_features:
  trend:
    - close > SMA10
    - close > SMA20
    - close > SMA50
    - SMA10 > SMA20 or recent reclaim
  compression:
    - ATR_percentile_declining
    - rolling_range_percent_contracting
    - volume_below_average_before_breakout
  breakout:
    - close > pivot_high
    - intraday_break_above_local_high
    - volume > volume_SMA
  market_regime:
    - benchmark_close > benchmark_SMA10
    - benchmark_close > benchmark_SMA20
    - benchmark_close > benchmark_SMA50
```

---

## 4.3 Options Strike / Expiry Selection

Tito’nun opsiyon seçim mantığı:

```yaml
options_selection:
  primary_rule:
    - choose_strike_and_expiry_where_underlying_can_realistically_reach_by_expiration
  avoid:
    - too_far_OTM_lottery_contracts
    - ignoring_IV
    - using_fixed_percent_stop_on_options_without_account_risk_context
  prefer_when_low_IV:
    - naked_long_calls_or_puts
  prefer_when_high_IV:
    - debit_spreads
    - credit_spreads
  rangebound_market:
    - iron_fly
    - iron_butterfly
  longer_theme:
    - LEAPS
```

QuantLens açısından:

- Bu doğrudan Binance crypto futures tarafına taşınmaz.
- Ama **underlying hareket hedefi / beklenen range / expiry uyumu** fikri, futures için “holding horizon vs expected ATR move” olarak çevrilebilir.

Crypto/futures karşılığı:

```yaml
crypto_translation:
  option_strike_distance -> target_distance_ATR
  expiry -> max_holding_bars
  IV_expensive -> realized_volatility_high
  debit_spread_risk_cap -> fixed_R_stop_or_position_size_cap
```

---

## 4.4 Risk Mantığı: Net Liquidation Bazlı Dollar Risk

En değerli bölüm burasıdır.

```yaml
risk_framework:
  risk_unit:
    - dollar_risk
    - percent_of_net_liquidation
  not_primary:
    - option_contract_percent_loss
  example_logic:
    forgiving_momentum_market:
      - allow_option_premium_drawdown_40_to_50_percent_if_dollar_risk_fixed
    volatile_whipsaw_market:
      - size_so_100_percent_option_loss_equals_allowed_dollar_risk
  thesis_exit:
    - if_underlying_support_breaks_exit
    - if_trade_thesis_wrong_exit
  hard_limit:
    - max_loss_predefined_before_entry
```

Önemli ayrım:

> Opsiyonda “%20 stop” çoğu zaman anlamsız olabilir; önemli olan hesabın kaç dolar / kaç yüzde risk altında olduğudur.

Bu fikir MTC için çok değerlidir: stop tipi ne olursa olsun position sizing her zaman **equity risk** üzerinden kalmalı.

---

## 4.5 Circuit Breakers / Risk Throttle

```yaml
circuit_breakers:
  daily:
    - if_daily_loss_hits_configured_amount_stop_trading
    - example_current_threshold_around_20000_USD_for_him
  weekly:
    - if_week_is_profitable_allow_small_risk_from_weekly_cushion
    - if_week_is_bad_reduce_risk
  monthly:
    - if_drawdown_around_10_to_15_percent_reduce_size_and_frequency
  mental_equity:
    - after_large_loss_size_down
    - rebuild_confidence_before_restoring_size
  account_structure:
    - uses_cash_account_as_guardrail
    - can intentionally consume buying_power_to_stop_overtrading
  profit_protection:
    - wire_out_profits
    - reduce_capital_at_risk_after_big_gains
```

Bu bölüm doğrudan QuantLens/MTC risk engine’e çevrilebilir.

---

## 5. Proposed QuantLens Modules

---

## 5.1 Candidate A — Tito RS Momentum Breakout / Crossback Model

```yaml
candidate_id: QL_TITO_RS_MOMENTUM_BREAKOUT_CROSSBACK_v0
type: signal_producer_research
priority: MEDIUM_HIGH
direction: long_primary
asset_class:
  - US_equities
  - liquid_crypto_proxy
  - high_beta_crypto_pairs
timeframe:
  context:
    - daily
    - weekly
  execution:
    - 1h
    - 30m
    - 15m
```

### Core Thesis

Güçlü piyasa ve güçlü tema içinde, relative strength gösteren varlık; 10/20/50 SMA üzerinde veya bu ortalamaları reclaim ettikten sonra sıkışır, volume/volatility dry-up yapar ve pivot kırılımı ile momentum başlatır.

### Objective v0 Rules

```yaml
universe_filter:
  liquidity:
    - dollar_volume_rank_high
  relative_strength:
    - asset_return_20d > benchmark_return_20d
    - asset_return_60d > benchmark_return_60d
  theme_proxy:
    crypto:
      - asset_outperforms_BTC_and_ETH
    stocks:
      - sector_RS_rank_high

market_regime_filter:
  benchmark:
    - close > SMA20
    - close > SMA50
  reject_or_reduce:
    - benchmark_close < SMA20
    - benchmark_SMA20_slope < 0

setup:
  trend:
    - close > SMA10
    - close > SMA20
    - close > SMA50
  base_or_crossback:
    any:
      - pullback_to_SMA10_or_SMA20_and_reclaim
      - multi_day_tight_base_above_SMA20
      - crossback_after_prior_move
  compression:
    - ATR_pct_5d < ATR_pct_20d
    - range_5d_pct <= configurable_threshold
    - volume_5d_avg < volume_20d_avg
  trigger:
    - close > highest_high_N_days
    - or intraday_break_above_local_pivot

stop:
  options:
    - below_base_low
    - below_crossback_low
    - ATR_2
    - SMA20_close_break

exit:
  partials:
    - optional_R_based_scale_out
  trail:
    - SMA10_or_SMA20
    - structure_low
  fail_fast:
    - close_back_below_breakout_pivot
    - close_below_SMA20
```

### First Backtest Parameters

```yaml
parameter_grid:
  sma_fast: [10]
  sma_mid: [20]
  sma_slow: [50]
  rs_lookback: [20, 60]
  base_lookback: [5, 10, 15]
  max_base_range_pct: [5, 8, 12]
  atr_compression_ratio_max: [0.75, 0.9, 1.0]
  breakout_lookback: [5, 10, 20]
  stop_mode:
    - base_low
    - ATR_2
    - SMA20_close
  exit_ma:
    - SMA10
    - SMA20
```

### Verdict

```yaml
verdict: TRY_AS_RESEARCH_MODEL
not_first_priority_if_Kell_model_already_exists: true
best_use: "Compare against Oliver Kell wedge-pop/crossback; possibly merge rather than duplicate."
```

---

## 5.2 Candidate B — Tito Options-Aware Risk Overlay

```yaml
candidate_id: QL_TITO_OPTIONS_AWARE_RISK_OVERLAY_v0
type: risk_sizing_overlay
priority: VERY_HIGH
asset_class:
  - all
  - especially_options
  - adaptable_to_futures
```

### Core Logic

Risk should be based on account net liquidation, not naive instrument percent stop.

```yaml
inputs:
  account_equity: float
  current_daily_pnl: float
  current_weekly_pnl: float
  current_monthly_pnl: float
  current_drawdown_pct: float
  market_regime: enum
  setup_quality: enum
  instrument_volatility_bucket: enum
  recent_trade_feedback: enum

outputs:
  allowed_risk_pct: float
  allowed_dollar_risk: float
  max_position_value: float
  trade_allowed: bool
  throttle_reason: string
```

### Risk Throttle Rules v0

```yaml
base_risk_pct:
  A_plus_setup_strong_market: 1.00
  normal_setup_good_market: 0.50
  choppy_market: 0.25
  weak_market: 0.00

drawdown_throttle:
  if_monthly_dd_pct <= -10:
    risk_multiplier: 0.50
    frequency_multiplier: 0.50
  if_monthly_dd_pct <= -15:
    risk_multiplier: 0.25
    frequency_multiplier: 0.25
  if_daily_loss_limit_hit:
    trade_allowed: false

weekly_cushion_logic:
  if_weekly_pnl_positive:
    allow_fraction_of_weekly_profit_as_risk: true
  if_weekly_pnl_negative:
    reduce_risk: true

mental_equity_proxy:
  after_large_loss:
    cooldown_trades_or_days: configurable
    reduce_size_until_new_equity_high_or_recovery_threshold: true
```

### MTC Fit

```yaml
mtc_fit:
  portfolio_state_guard: true
  position_sizing_module: true
  entry_gate: true
  producer: false
```

Bu modül MTC’ye producer olarak değil, **PortfolioState okuyan guard/risk throttle** olarak daha uygundur.

---

## 5.3 Candidate C — Profit Withdrawal / Capital-at-Risk Cap

```yaml
candidate_id: QL_TITO_PROFIT_WITHDRAWAL_CAPITAL_AT_RISK_v0
type: bankroll_management
priority: HIGH
```

### Rules v0

```yaml
profit_withdrawal:
  monthly_profit_threshold:
    - if_month_profit > X
  action:
    - move_fraction_to_locked_equity
    - reduce_tradable_capital
    - preserve_tax_reserve
  purpose:
    - prevent_full_year_profit_from_remaining_at_risk
    - psychologically_depressurize
```

Backtest simulation:

```yaml
simulate:
  variants:
    - no_withdrawal
    - withdraw_25_percent_monthly_profit
    - withdraw_50_percent_monthly_profit
    - withdraw_75_percent_monthly_profit
  outputs:
    - terminal_equity
    - locked_profit
    - max_drawdown_on_total_equity
    - max_drawdown_on_trading_equity
    - risk_of_ruin_proxy
```

---

## 6. Options Wrapper — Research Warning

Bu transcriptte opsiyon tarafı çok değerli ama backtest için veri gereksinimi yüksektir.

```yaml
required_for_real_options_backtest:
  - option_chain_history
  - bid_ask_spread
  - implied_volatility_history
  - greeks
  - assignment/exercise assumptions for spreads
  - liquidity/open_interest
  - commissions
  - slippage
```

Eğer bunlar yoksa yapılacak şey:

```yaml
proxy_backtest_only:
  - underlying_signal_backtest
  - ATR_based_expected_move
  - synthetic_option_multiplier_model
  - max_loss_as_premium_proxy
```

Bu nedenle ilk aşamada **opsiyon PnL backtest yapılmasın**; önce underlying setup ve risk overlay test edilsin.

---

## 7. Crypto Transferability

```yaml
crypto_transferability: MEDIUM
transferable:
  - relative_strength_vs_BTC_ETH
  - compression_before_breakout
  - market_regime_filter
  - 10_20_50_MA_structure
  - risk_throttle
  - circuit_breakers
  - mental_equity_size_down
  - capital_at_risk_cap
partially_transferable:
  - options_convexity
  - IV_expansion
  - earnings_gap_logic
not_transferable:
  - US_equity_options_chain_without_data
  - earnings_specific_reaction
  - single_stock_option_spreads
```

Crypto için en iyi kullanım:

```yaml
crypto_version:
  signal:
    - RS leader among crypto majors/alts
    - compression above 10/20 MA
    - breakout with volume/volatility expansion
  risk:
    - account_risk_pct fixed
    - dynamic throttle by BTC/ETH regime
    - reduce size after daily/weekly/monthly losses
  exit:
    - SMA10/SMA20 trail
    - ATR trail
    - fail-fast pivot break
```

---

## 8. Relationship to Existing QuantLens Candidates

```yaml
overlap_with_existing:
  Oliver_Kell:
    overlap: HIGH
    difference: "Tito adds options wrapper and stricter market-regime/sizing discussion."
  Martin_Luke:
    overlap: MEDIUM_HIGH
    difference: "Martin pullback has tighter intraday support/reclaim model; Tito is more breakout/options-focused."
  CANSLIM:
    overlap: MEDIUM
    difference: "Tito is more short-term and options-execution oriented."
  Roppel:
    overlap: MEDIUM
    difference: "Roppel is position trading / mega trend patience; Tito is active options momentum with risk guardrails."
```

Recommendation:

> Do not create a completely redundant producer if Oliver Kell already exists. Instead, extract Tito’s unique parts into **risk overlay**, **options wrapper**, and **market-regime sizing gate**.

---

## 9. Suggested Codex Research Tasks

```text
TASK 1 — Build Tito Risk Overlay Prototype
Create:
06_QUANTLENS_LAB/research/tito_options_risk_overlay/

Files:
- README.md
- SPEC.md
- tito_risk_overlay.py
- simulate_profit_withdrawal.py
- test_tito_risk_overlay.py
- TITO_RISK_OVERLAY_REPORT.md

Implement:
- account equity risk sizing
- daily loss limit
- weekly cushion risk logic
- monthly drawdown throttle
- recent-trade-feedback throttle
- profit withdrawal simulation
- no changes to MTC_V2.pine
- no changes to production runner
```

```text
TASK 2 — Compare Tito Breakout Model Against Existing Kell Model
Create:
06_QUANTLENS_LAB/research/tito_rs_momentum_breakout/

Implement only Python research prototype:
- underlying OHLC model
- no options PnL yet
- run on at least 5 crypto assets and available US-equity data if present
- compare against QL_KELL_WEDGE_POP_CROSSBACK_10_20EMA_v0
- output overlap analysis: are trades redundant or complementary?
```

```text
TASK 3 — Options Wrapper Feasibility Report
Do not implement full options backtest unless historical options chain data exists.
Create a feasibility report listing:
- data providers needed
- synthetic proxy assumptions
- why OHLC-only options PnL is unreliable
- minimum viable proxy for research
```

---

## 10. Data Requirements

### For Underlying Setup

```yaml
required:
  - OHLCV daily
  - OHLCV intraday optional
  - benchmark OHLCV
  - relative strength calculation
  - sector/theme grouping if US equities
  - volume data
```

### For Options Version

```yaml
required:
  - option chain snapshots
  - historical IV
  - historical bid/ask
  - expiry calendar
  - strike availability
  - open interest
  - commissions/slippage model
```

### For Crypto Proxy

```yaml
required:
  - Binance futures OHLCV
  - BTC/ETH benchmark
  - funding rate optional
  - open interest optional
  - volatility regime
```

---

## 11. Backtest Plan

```yaml
phase_1:
  name: underlying_signal_only
  assets_minimum:
    - BTCUSDT
    - ETHUSDT
    - SOLUSDT
    - BNBUSDT
    - XRPUSDT
  timeframes:
    - 1D
    - 4H
    - 1H
  outputs:
    - trade_count
    - PF
    - net_return
    - max_DD
    - win_rate
    - average_R
    - fee_stress_2x_3x
    - market_regime_bucket
    - RS_bucket
    - compression_bucket

phase_2:
  name: risk_overlay_simulation
  use_existing_trade_sets:
    - Crabel
    - Kell
    - Martin
    - BigBeluga
  compare:
    - base
    - with_daily_stop
    - with_weekly_cushion
    - with_monthly_throttle
    - with_profit_withdrawal

phase_3:
  name: US_equity_options_feasibility
  only_if_data_available: true
```

---

## 12. MTC V2 Fit

```yaml
mtc_fit:
  signal_producer:
    status: not_direct_first_choice
    reason: overlaps_with_Kell_and_VCP
  gates:
    - market_regime_gate
    - relative_strength_gate
    - compression_gate
  position_manager:
    - daily_loss_circuit_breaker
    - weekly_cushion_sizing
    - monthly_drawdown_throttle
    - recent_trade_feedback_throttle
  exits:
    - SMA10/SMA20 trail
    - pivot_failure_exit
    - support_break_exit
  sizing:
    - net_liquidation_percent_risk
    - instrument_volatility_adjusted_size
```

Best integration path:

1. Risk overlay as independent Python module.
2. Apply overlay to existing strategy trade logs.
3. If overlay improves drawdown/stability, port concept into MTC position manager / guard layer.
4. Only after that evaluate Tito/Kell merged producer.

---

## 13. Pine Feasibility

```yaml
pine_possible:
  - SMA10/SMA20/SMA50 structure
  - compression detection
  - pivot breakout marker
  - benchmark regime filter if single request.security benchmark used
  - risk visualization
  - daily loss guard approximate if strategy equity accessible

pine_not_good_for:
  - options chain logic
  - IV-aware strike selection
  - profit withdrawal simulation
  - multi-symbol sector/theme detection
  - robust portfolio-state risk throttling
```

Decision:

```yaml
pine_now: false
reason: "Python research and risk overlay simulation should come first."
```

---

## 14. Final Ranking

```yaml
final_rating:
  research_value: 9/10
  immediate_strategy_value: 7/10
  risk_module_value: 10/10
  options_execution_value: 9/10_for_US_equities
  crypto_adaptability: 6/10
  MTC_position_manager_value: 10/10
  MTC_producer_value: 6/10
```

Final conclusion:

> Bu video, doğrudan yeni bir producer’dan çok **QuantLens/MTC risk ve execution katmanını güçlendirecek** bir video. En değerli çıktı: daily/weekly/monthly circuit breaker + net liquidation bazlı sizing + market-regime dependent risk throttle. Entry tarafı Oliver Kell/VCP/Martin modelleriyle birleştirilmeli; ayrı duplicate strateji olarak şişirilmemeli.

---

## 15. Decision

```yaml
decision:
  keep_in_quantlens: true
  classify_as:
    - CANDIDATE_RISK_OVERLAY
    - OPTIONS_EXECUTION_REFERENCE
    - MOMENTUM_BREAKOUT_SECONDARY_CANDIDATE
  next_action:
    - build_risk_overlay_first
    - compare_entry_model_against_existing_Kell
    - do_not_port_to_Pine_yet
    - do_not_live_trade
```

