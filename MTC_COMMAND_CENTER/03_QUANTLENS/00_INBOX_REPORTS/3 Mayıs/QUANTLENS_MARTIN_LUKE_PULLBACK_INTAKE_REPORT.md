# QUANTLENS TRANSCRIPT INTAKE REPORT — Martin Luke Pullback / Anchored VWAP System

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/VKNEJA5r8zw?si=XIbuUbrJNtP5wjop  
**Normalized URL:** https://www.youtube.com/watch?v=VKNEJA5r8zw  
**Video ID:** `VKNEJA5r8zw`  
**Transcript Status:** Provided by user in chat  
**Speaker:** Martin Luke  
**Topic:** Swing trading, pullback buys, tight stops, anchored VWAP, theme leadership  
**Transcript Digest SHA256:** `8ae84fe0bc995d5cc7e51d358073b5bb3f3afaf48426cb2140624365ab5194de`

---

## 1. Executive Verdict

```yaml
classification: HIGH_VALUE_DISCRETIONARY_TO_SYSTEMATIC_RESEARCH_CANDIDATE
quantlens_priority: VERY_HIGH
codex_status: PYTHON_FIRST_RESEARCH_MODULE
production_ready: false
tradingview_pine_ready: partial
python_backtest_ready: yes
crypto_transferability: medium_to_high
primary_reason_to_study: >
  The video contains a detailed, repeatable pullback-buy framework with
  clear risk rules, intraday execution logic, anchored VWAP context,
  EMA support levels, theme/relative-strength filtering, and post-trade
  review lessons.
```

Bu video, QuantLens için **Ty Rajnus videosundan daha doğrudan uygulanabilir**. Çünkü long momentum / pullback mantığı; crypto, hisse, endeks ve yüksek beta varlıklara daha kolay taşınabilir.

Ancak sistem tamamen mekanik değildir. Martin Luke’un yaklaşımı şunların birleşimidir:

- güçlü tema / sektör seçimi;
- weekly + daily context;
- 9/21/50/150 EMA;
- anchored VWAP;
- intraday flush-to-support;
- 1m / 5m breakout trigger;
- çok sıkı stop;
- düşük win-rate ama yüksek R mantığı;
- sell into strength + EMA trailing;
- overtrading ve choppy market filtreleri.

---

## 2. Ana Strateji Özeti

```yaml
style:
  type: swing_trading
  direction:
    - long_primary
    - short_secondary
  setups:
    - pullback_buy
    - breakout
    - episodic_pivot
    - parabolic_long
    - parabolic_short
  risk_style:
    - tight_stop
    - low_win_rate
    - high_R_winners
  main_indicators:
    - 9 EMA
    - 21 EMA
    - 50 EMA
    - 150 EMA
    - anchored VWAP
    - dollar volume
```

Martin’in 2025 performans mantığı:

```yaml
2025_style_summary:
  winners: 209
  losers: 731
  win_rate: about_22_percent
  risk_per_trade: about_0.5_percent_portfolio
  typical_stop: below_2.5_to_3_percent
  average_position_size: 25_to_30_percent
  focus: fast_moving_high_ADR_stocks
```

Önemli çıkarım:

> Büyük performans, yüksek win-rate’ten değil; sıkı stop + yüksek R kazananları yakalamaktan geliyor.

---

## 3. QuantLens İçin En Değerli Strateji Adayı

## 3.1 Candidate: Pullback Buy Into Confluence Support

```yaml
candidate_id: QL_MARTIN_PULLBACK_CONFLUENCE_LONG_001
priority: VERY_HIGH
direction: long
market:
  - US high beta stocks
  - crypto majors
  - liquid altcoins
  - sector/theme leaders
timeframes:
  context:
    - weekly
    - daily
  execution:
    - 1m
    - 5m
    - 15m
    - 1h
```

Ana fikir:

> Güçlü tema içindeki lider hisse/varlık; weekly/daily olarak yapıcı görünürken, günlük 9/21 EMA, anchored VWAP, önceki swing high/low veya gap support bölgesine hızlı pullback yapar. Intraday’de hızlı V-shape tepki ve önceki 1m/5m mum high kırılımı entry trigger olur.

---

## 3.2 Setup Conditions v0

```yaml
setup_context:
  trend_quality:
    weekly:
      - price_above_weekly_9_or_21_ema_preferred
      - weekly_base_or_constructive_pullback
      - higher_lows_or_tight_weekly_structure
    daily:
      - price_above_or_reclaiming_9_21_50_ema
      - EMA_alignment_improving
      - recent_strength_or_reversal_bar
      - not_far_extended_from_daily_EMA
  theme_filter:
    - strong_theme
    - multiple_names_in_same_group_moving
    - relative_strength_vs_market
    - high_dollar_volume
  support_confluence:
    any_two_or_more:
      - daily_9_ema
      - daily_21_ema
      - daily_50_ema
      - daily_150_ema
      - anchored_vwap
      - prior_swing_high
      - prior_swing_low
      - unfilled_gap
      - hourly_21_or_50_ema
```

---

## 3.3 Intraday Entry Logic

Martin’in anlattığı en test edilebilir entry modeli:

```yaml
intraday_entry:
  preferred_sequence:
    - stock gaps up or opens weak
    - flushes quickly into known support level
    - finds support
    - V-shaped recovery preferred
    - enter on breakout of previous 1m/5m bar high
  first_15_minutes:
    trigger_timeframe: 1m
  15_to_60_minutes_after_open:
    trigger_timeframe: 5m
  after_60_minutes:
    lower_priority: true
```

Not:

- Martin özellikle erken seans flush + hızlı toparlanmayı seviyor.
- Yavaş, gün sonuna yayılan recovery onun için daha zayıf.
- Hong Kong saat dilimi nedeniyle late-day recovery’leri pratikte tercih etmiyor.

---

## 3.4 Stop Logic

```yaml
stop_logic:
  primary:
    - low_of_day
  alternatives:
    - breakout_candle_low
    - previous_candle_low
    - entry_candle_low
  selection_rule:
    - if low_of_day_stop_too_wide: use_breakout_bar_or_previous_bar_low
  preferred_stop_width:
    - under_2.5_percent
    - rarely_above_3_percent
  portfolio_risk:
    default: 0.5_percent
```

Örnek sizing mantığı:

```yaml
position_sizing_formula:
  position_value = account_equity * risk_pct / stop_pct
example:
  account: 10000
  risk_pct: 0.5%
  risk_amount: 50
  stop_pct: 2.5%
  position_value: 2000
  position_size_pct: 20%
```

Excel örneği, senin bölgesel ayarın için `;` ile:

```excel
=HesapBakiyesi*RiskYuzdesi/StopYuzdesi
```

İngilizce Excel fonksiyonlu yapı:

```excel
=AccountEquity*RiskPct/StopPct
```

---

## 4. Anchored VWAP Kullanımı

Martin anchored VWAP’ı çok yoğun kullanıyor.

```yaml
anchored_vwap_usage:
  anchor_points:
    - swing_high_of_base
    - swing_low_of_base
    - large_gap_up_day
    - large_gap_down_day
    - major_reversal_candle
  use_cases:
    - support_on_pullback
    - resistance_on_short_pullback
    - break_and_retest
    - base_quality_assessment
    - identify_whether_price_is_above_key_cost_basis
```

Önemli not:

> Anchor noktası mekanik olarak her zaman en yüksek / en düşük mum olmak zorunda değil. Martin, fiyatın en çok reaksiyon verdiği anchor noktasını biraz ayarlayabiliyor.

Bu yüzden QuantLens’te iki seviye yapılmalı:

```yaml
anchored_vwap_modes:
  strict_mode:
    - anchor_to_exact_swing_high_or_low
    - fully_backtestable
  discretionary_mode:
    - allow_manual_anchor_adjustment
    - visual_or_research_only
```

---

## 5. Breakout ve Pullback Ayrımı

Martin’e göre pullback ve breakout birbirine zıt değildir:

```yaml
relationship:
  pullback:
    advantage:
      - better_price
      - tighter_stop
      - earlier_entry
  breakout:
    advantage:
      - clearer_confirmation
      - stronger_momentum
  combined_best_case:
    - pullback_into_support
    - then_breakout_from_small_intraday_base
```

QuantLens için en iyi mekanik formül:

```yaml
entry_model:
  stage_1: identify_daily_support_confluence
  stage_2: wait_intraday_flush
  stage_3: wait_1m_or_5m_reversal_breakout
  stage_4: stop_below_intraday_support
```

---

## 6. Selling / Exit Rules

Martin’in satış tarafı daha discretionary.

```yaml
exit_style:
  partials:
    typical_trim: 15_percent_position
    trigger:
      - up_3R_to_5R
      - extended_on_hourly
      - sharp_strength
  trailing:
    - trail_with_9_ema
    - sometimes_21_ema
    - close_below_9_ema_for_strong_movers
  discretionary_factors:
    - market_extended
    - existing_profit_cushion
    - strength_of_theme
    - position_age
    - volatility
```

Daha sistematik QuantLens versiyonu:

```yaml
exit_v0:
  partial_1:
    when: unrealized_R >= 3
    sell: 15_percent
  partial_2:
    when: unrealized_R >= 5
    sell: 15_percent
  trail:
    method: close_below_9ema_or_intraday_structure
  hard_stop:
    initial_stop_never_widen
```

---

## 7. Short Side Rules

Martin short tarafını long’un aynası gibi görüyor, ama daha seçici olmak gerektiğini söylüyor.

```yaml
short_setup_ideal:
  - first_breakdown_below_50_ema
  - first_pullback_into_50_ema
  - 9_and_21_ema_curling_down_near_50
  - anchored_vwap_resistance
  - market_below_key_moving_averages
  - avoid_when_weekly_chart_constructive
```

Önemli ders:

> Daily 9/21 altına inen bir hisse, weekly hâlâ yapıcıysa short için kötü yer olabilir.

QuantLens için short module ayrı tutulmalı:

```yaml
candidate_id: QL_MARTIN_PULLBACK_SHORT_001
priority: MEDIUM
condition:
  - only_when_market_weak
  - only_when_weekly_not_supportive
  - avoid_choppy_market
```

---

## 8. Parabolic Long Model

Martin’in TQQQ / April panic örneği:

```yaml
candidate_id: QL_MARTIN_PARABOLIC_LONG_001
priority: HIGH_BUT_RARE
setup:
  - index_or_leveraged_etf_extremely_oversold
  - consecutive_gap_down_days
  - panic_sell_condition
  - price_extreme_below_1h_ema
  - daily_extreme_below_9_ema
entry:
  - 1m_opening_range_high
  - or 1m_reversal_breakout
stop:
  - low_of_breakout_bar
target:
  - hourly_9_ema
  - hourly_21_ema
  - 5m_150_ema
exit:
  - sell_all_into_fast_strength
```

Bu model nadir ama backtest edilmeye değer.

---

## 9. Market Regime ve Trade Feedback

Martin’in en değerli derslerinden biri:

```yaml
situational_awareness:
  main_inputs:
    - own_trade_feedback
    - QQQ trend
    - IWM trend
    - market_breadth
    - watchlist_quality
    - number_of_leaders_setting_up
    - number_of_lagging_names_breaking_down
```

Özellikle December drawdown’dan çıkan ders:

```yaml
bad_regime_behaviors:
  - flipping_long_short_repeatedly
  - trying_to_make_back_losses
  - taking_hourly_only_entries_far_from_daily_support
  - shorting_when_IWM_strong
  - overtrading_choppy_market
```

QuantLens için regime filter:

```yaml
regime_filter_v0:
  long_aggression:
    high_when:
      - QQQ_above_9_21_ema
      - IWM_outperforming_or_stable
      - leaders_breaking_out
      - new_positions_working
    low_when:
      - recent_trades_fail
      - market_choppy
      - leaders_reverse
      - no_follow_through
```

---

## 10. Watchlist / Theme Selection

```yaml
theme_selection:
  process:
    - scan premarket gap ups
    - scan prior day big movers
    - review watchlists daily
    - upgrade/downgrade names
    - identify groups moving together
  preferred:
    - strong liquid leaders
    - high ADR
    - high dollar volume
    - fast moving stocks
    - leading theme
```

Tema örnekleri:

```yaml
themes_mentioned:
  - AI
  - quantum
  - memory / semiconductors
  - metals
  - crypto-related
  - energy / nuclear / SMR
  - solar
```

---

## 11. Loss Review Lessons

## 11.1 Kötü trade tipleri

```yaml
avoid:
  - buying_middle_of_nowhere
  - buying_too_extended_from_daily_9_21
  - pullback_only_to_hourly_21_when_daily_extended
  - buying_into_declining_EMAs
  - shorting_good_weekly_chart
  - repeated_long_short_flipping
  - entries_without_daily_support_confluence
```

## 11.2 Choppy market dersi

```yaml
choppy_market_solution:
  preferred: trade_less
  not_preferred:
    - taking_profit_at_1R_randomly
    - changing_entire_system_due_to_chop
    - forcing_longs_and_shorts
```

---

## 12. Winner Review Lessons

Kazanan trade ortak özellikleri:

```yaml
winner_common_features:
  - entry_at_right_time
  - tight_stop
  - strong_theme
  - relative_strength
  - constructive_weekly_context
  - support_confluence
  - early_in_move
  - enough_volatility_to_generate_high_R
```

Kazanan örnekleri:

```yaml
examples:
  BBAI:
    type: gap_breakout / theme strength
    exit: partials into strength, close below 9 EMA
  TQQQ:
    type: parabolic long after panic selloff
    result: about_13R_in_30_minutes
  HOOD:
    type: post-correction leader breakout
    lesson: sold too early; could trail with 9 EMA
  OKLO:
    type: nuclear theme leader
    better_entry: pullback into 21/150 EMA
  FUTU:
    type: inside day breakout
    exit: early but acceptable
  IONQ_RGTI_QBTS:
    type: quantum theme
    lesson: theme clustering + weekly context
  TSLA:
    type: daily 9 EMA / gap pullback with weekly context
  AMX:
    type: anchored VWAP + 21 EMA pullback
  AS:
    type: anchored VWAP / previous high support pullback
  AMD:
    type: breakout from tight EMA compression
```

---

## 13. QuantLens Strategy Modules To Build

```yaml
recommended_modules:
  - QL_MARTIN_PULLBACK_CONFLUENCE_LONG
  - QL_MARTIN_INTRADAY_FLUSH_REVERSAL_ENTRY
  - QL_MARTIN_ANCHORED_VWAP_CONTEXT
  - QL_MARTIN_TIGHT_STOP_POSITION_SIZING
  - QL_MARTIN_THEME_RELATIVE_STRENGTH_FILTER
  - QL_MARTIN_PARABOLIC_LONG
  - QL_MARTIN_CHOPPY_MARKET_TRADE_LESS_FILTER
```

---

## 14. Python Backtest Plan

## Phase 1 — Data

```yaml
required_data:
  - daily OHLCV
  - intraday 1m or 5m OHLCV
  - weekly resampled OHLCV
  - dollar volume
  - symbol universe
optional:
  - sector/theme labels
  - relative strength vs index
  - premarket data
```

## Phase 2 — Features

```yaml
features:
  ema:
    - daily_9
    - daily_21
    - daily_50
    - daily_150
    - weekly_9
    - weekly_21
  anchored_vwap:
    - strict_swing_high_anchor
    - strict_swing_low_anchor
    - gap_day_anchor
  support_confluence:
    - distance_to_ema
    - distance_to_avwap
    - distance_to_prior_high_low
    - distance_to_gap
  entry:
    - intraday_flush_pct
    - reclaim_previous_bar_high
    - time_since_open
  risk:
    - stop_pct
    - R_multiple
```

## Phase 3 — Rules v0

```yaml
long_pullback_v0:
  context:
    - daily_close_above_21ema_or_reclaiming
    - weekly_not_bearish
    - support_confluence_score >= 2
  intraday:
    - price_flushes_into_support_zone
    - 1m_or_5m_previous_bar_high_breakout
  stop:
    - min(low_of_day, breakout_bar_low) depending on max_stop_pct
  max_stop_pct: 3
  position_risk_pct: 0.5
  exits:
    - partial_at_3R
    - partial_at_5R
    - trail_below_daily_9ema
```

---

## 15. Codex Prompt

Aşağıdaki prompt doğrudan Codex’e verilebilir.

```text
You are working inside the QuantLens repo.

Task:
Create a Python-first research prototype for the Martin Luke pullback / anchored VWAP strategy.

Important:
This is research/backtest only. Do not add broker execution.

Create folder:
06_QUANTLENS_LAB/strategies/MARTIN_LUKE_PULLBACK/

Create files:
- README.md
- SPEC.md
- DATA_SCHEMA.md
- BACKTEST_PLAN.md
- RISK_NOTES.md
- configs/martin_luke_pullback_v0.yml
- src/features.py
- src/anchored_vwap.py
- src/entries.py
- src/exits.py
- src/sizing.py
- src/backtest.py
- src/reports.py
- tests/test_anchored_vwap.py
- tests/test_entries.py
- tests/test_sizing.py

Strategy concept:
Swing trading framework focused on buying pullbacks in leading names/themes when price pulls into support confluence:
- daily 9/21/50/150 EMA
- anchored VWAP
- prior swing high/low
- unfilled gap
- hourly 21/50 EMA

Context:
- weekly chart must not be bearish
- prefer constructive weekly base, higher lows, or weekly 9/21 EMA support
- daily should show improving EMA structure, reclaim, or strong reversal
- avoid entries far extended from daily EMAs
- prefer high dollar volume and high ADR names

Intraday entry:
- after open, price flushes quickly into support zone
- first 15 minutes: use 1m previous bar high breakout
- 15-60 minutes after open: use 5m previous bar high breakout
- prefer V-shaped recovery from support
- late-day slow recovery is lower priority

Stop:
- default low of day
- if too wide, use breakout candle low or previous candle low
- max stop default 3%, preferred under 2.5%
- portfolio risk default 0.5%

Sizing:
position_value = account_equity * risk_pct / stop_pct

Exits:
- partial 15% at 3R
- partial 15% at 5R
- trail remaining with daily 9 EMA or structure
- optional close on daily close below 9 EMA

Regime filter:
- reduce trading in choppy market
- reduce if recent trade feedback is poor
- reduce if QQQ/IWM weak or no leadership
- avoid flipping long/short repeatedly

Backtest outputs:
- trade count
- win rate
- average R
- median R
- profit factor
- max drawdown
- monthly returns
- R distribution
- stop width distribution
- support confluence bucket results
- time after open bucket results
- EMA support bucket results
- anchored VWAP contribution

Deliver final report:
06_QUANTLENS_LAB/strategies/MARTIN_LUKE_PULLBACK/MARTIN_LUKE_PULLBACK_IMPLEMENTATION_REPORT.md

Final report must include:
- files created
- assumptions
- implemented rules
- data requirements
- tests run
- limitations
- next steps
```

---

## 16. TradingView / Pine Feasibility

```yaml
pine_possible:
  - EMA 9/21/50/150
  - anchored VWAP from manually selected anchor
  - support confluence visual zones
  - intraday trigger markers
  - R-based stop/target visualization
  - alert prototype

pine_limitations:
  - automatic theme detection hard
  - watchlist relative strength hard
  - dynamic anchored VWAP selection subjective
  - multi-symbol breadth limited
```

Pine prototype is useful as scanner/visual aid, but Python should be the source of truth for backtesting.

---

## 17. Crypto Transferability

```yaml
crypto_transferability: MEDIUM_TO_HIGH
transferable:
  - EMA pullback
  - anchored VWAP support
  - prior high retest
  - intraday flush/reclaim
  - tight stop / high R
  - trend theme leadership
  - parabolic long after panic
less_transferable:
  - stock-specific earnings/EP
  - dollar volume leadership by sector
  - gap/unfilled gap logic in 24/7 markets
```

Crypto adaptation:

```yaml
crypto_version:
  support_levels:
    - daily_9_21_ema
    - anchored_vwap_from_swing_high_low
    - prior_range_high
    - liquidation_wick_low
  entry:
    - lower_timeframe_reclaim
    - 1m/5m candle high breakout
  regime:
    - BTC/ETH trend filter
    - sector basket strength if altcoins
```

---

## 18. Final Rating

```yaml
final_rating:
  research_value: 10/10
  python_backtest_priority: 9/10
  pine_visual_priority: 7/10
  live_readiness: 4/10
  crypto_adaptability: 8/10
  risk_framework_value: 10/10
```

Final conclusion:

> Bu video QuantLens için çok yüksek değerli. En doğru ilk test; **EMA + anchored VWAP + support confluence + intraday flush/reclaim + tight stop** long modelidir. Önce Python’da test edilmeli, sonra TradingView tarafında görsel/alert prototipine çevrilmelidir.

---

## 19. Decision

```yaml
decision: KEEP_AND_PROTOTYPE
next_action:
  - create MARTIN_LUKE_PULLBACK research folder
  - implement Python feature/backtest module
  - test on high-beta liquid stocks and crypto majors
  - compare support confluence buckets
```
