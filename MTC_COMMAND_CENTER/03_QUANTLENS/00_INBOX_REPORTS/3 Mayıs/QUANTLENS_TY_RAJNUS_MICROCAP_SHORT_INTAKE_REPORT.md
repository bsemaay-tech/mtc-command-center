# QUANTLENS TRANSCRIPT INTAKE REPORT — Ty Rajnus Short-Only System

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/bRXO6F_vGjM?si=N4P30T_3_i-IHPP4  
**Normalized URL:** https://www.youtube.com/watch?v=bRXO6F_vGjM  
**Video ID:** `bRXO6F_vGjM`  
**Transcript Status:** Provided by user in chat  
**Speaker:** Ty Rajnus / Rajnus Capital  
**Topic:** Systematic short-only nano-cap / micro-cap day trading  
**Transcript Digest SHA256:** `b5ceb561239449d1bc272fc297314cddaf64821e4017bc143a62cb046c4874ee`

---

## 1. Executive Verdict

```yaml
classification: RESEARCH_CANDIDATE_WITH_EXECUTION_CONSTRAINTS
quantlens_priority: HIGH_FOR_RESEARCH
codex_status: SPEC_FIRST_THEN_BACKTEST
production_ready: false
tradingview_pine_ready: partial_only
python_backtest_ready: yes_but_requires_special_data
crypto_transferability: low_to_medium
direct_live_recommendation: no
primary_reason_to_study: >
  This is a rare, clearly described, data-driven short-only edge based on
  overextension, low-liquidity price distortion, dilution pressure,
  and regular-session liquidity normalization.
```

Bu video **yüksek değerli**, ama bizim sistem için “hemen stratejiye çevir” tarzı bir aday değil. Çünkü edge şu unsurlara çok bağlı:

- ABD nano-cap / micro-cap hisseler;
- short locate / borrow maliyeti;
- premarket ve after-hours veri;
- dilution / shelf / ATM offering bilgisi;
- LUDP / T1 / T12 halt riski;
- broker kısıtları;
- gün içi short execution.

Bu yüzden QuantLens için en doğru kullanım:

```yaml
recommended_use:
  - microcap_short_research_module
  - liquidity_transition_reversal_model
  - overextension_factor_library
  - backtest_methodology_template
  - risk_engine_reference
not_recommended_as:
  - direct_crypto_strategy
  - simple_TradingView_indicator_strategy
  - retail_user_live_short_system_without_borrow_data
```

---

## 2. Video İçinden Ana Strateji Özeti

Ty Rajnus’un sistemi:

```yaml
style:
  direction: short_only
  market: US nano-cap / micro-cap stocks
  holding_period: intraday_only
  typical_hold: 4_to_6_hours
  overnight: avoided
  discretion: near_zero
  implementation: systematic
  data_method: Excel/backtest driven
  primary_timeframe: 1_minute
  secondary_timeframe: daily for dilution/chart context
```

Ana mantık:

> Çok küçük piyasa değerli, dilutive şirketlerde; premarket / after-hours / düşük likidite ortamında yapay veya sürdürülemez aşırı yükseliş oluşur. Normal seans likiditesi geldiğinde fiyat çoğu zaman çöker.

---

## 3. Performans ve Risk Verileri

Transcript’te verilen metrikler:

```yaml
2025_usic:
  starting_equity: 80000
  ending_equity: 386000
  return: 382%
  trade_count: 238
  winners: 157
  losers: 81
  win_rate: 66%
  direction: all_short
  losing_months: 0
  largest_winner: 29000
  largest_loser: 19000
  largest_drawdown: 38000
  largest_drawdown_percent: 41%
  typical_hold: 4_to_6_hours
```

Önemli yorum:

- Performans çok güçlü;
- ama sistem **tail-risk** açısından tehlikeli;
- 41% drawdown kabul edilebilir bir retail risk seviyesi değildir;
- edge’in büyük kısmı “short locate + execution + broker erişimi” ile ilgilidir.

---

## 4. Ana Edge Bileşenleri

## 4.1 En önemli faktör: upside overextension

Transcript’te açık şekilde en önemli faktör olarak anlatılıyor:

```yaml
factor_1:
  name: upside_overextension
  importance: highest
  definition:
    - price moved up very far
    - price moved up very quickly
    - especially during low liquidity
```

Ölçülebilir aday metrikler:

```yaml
overextension_metrics:
  intraday_return_from_prev_close: high
  premarket_return_from_prev_close: high
  afterhours_return: high
  multi_day_return_3d: high
  range_expansion_vs_atr: high
  price_distance_from_vwap_or_open: high
  price_multiple_from_recent_low: high
```

Video örnekleri:

- %50 üzeri hızlı yükseliş ilgi alanına giriyor;
- bazı hisseler 100%–1000% arası hareket edebiliyor;
- düşük likidite premarket hareketleri “fake price” gibi değerlendiriliyor.

---

## 4.2 Düşük likidite → normal seans likiditesi geçişi

En güçlü fikirlerden biri budur:

```yaml
liquidity_transition_edge:
  preferred_distortion_periods:
    - premarket
    - afterhours
    - extremely_low_liquidity_windows
  preferred_entry_period:
    - just_before_regular_open
    - regular_session_open
  thesis: >
    Price can be distorted upward during low liquidity.
    When regular session liquidity returns, selling pressure/dilution/shorting
    can dominate and price can collapse.
```

Bu, QuantLens açısından güçlü bir “regime / session edge” tanımıdır.

---

## 4.3 Dilution / shelf / ATM offering

Ty’nin short edge’inin temel fundamental ayağı:

```yaml
dilution_components:
  - at_the_market_offering
  - private_placement
  - warrants
  - convertible_notes
  - shelf_registration
  - cash_reserve_pressure
```

Pratik bilgi:

```yaml
preferred_data_tool:
  - Dilution Tracker
uses:
  - cash remaining
  - shelf amount
  - ATM availability
  - warrants / convertibles
  - offering type
```

Backtest için bu veriyi dahil etmek büyük fark yaratabilir; ama bu veri TradingView Pine’da doğal olarak yoktur.

---

## 4.4 Market cap filtresi

Transcript’te en önemli filtrelerden biri:

```yaml
market_cap_filter:
  preferred: under_50_million
  common_range:
    - nano_cap
    - micro_cap
  industry_filter: not_important
```

Önemli nokta: Sektörün fazla önemi olmadığını söylüyor. Biotech, mining, oil/gas, tech, crypto-themed microcaps; hepsi aynı davranışı gösterebiliyor.

---

## 4.5 Fiyat filtresi

```yaml
price_filter:
  preferred: above_1_usd
  reason:
    - sub_1_dollar_locates_can_be_expensive
    - share_count_required_becomes_large
    - locate_fee_as_percent_position_increases
  best_case:
    - started_low
    - spiked_to_double_digits
```

---

## 4.6 Volume filtresi ve T12/T1 halt riskinden kaçınma

Ty, T12/T1 tarzı bilgi talebi veya news pending halt risklerini azaltmak için volume’a önem veriyor:

```yaml
halt_risk_filter:
  avoid:
    - extremely_low_volume_spikers
    - only_few_hundred_thousand_shares_traded
  prefer:
    - millions_of_premarket_volume
```

Sebep:

- düşük volume’lu microcap’lerde T12/T1 halt riski daha yüksek olabilir;
- short açıkken haftalarca halted kalmak yıkıcı borrow fee yaratabilir;
- örnekte 1000%+ interest ve günlük yüksek maliyet anlatılıyor.

---

## 5. Aday Strateji 1 — Microcap Liquidity Reversion Short

## 5.1 Verdict

```yaml
candidate_id: QL_TY_MICROCAP_LIQUIDITY_REVERSION_SHORT_001
classification: RESEARCH_CANDIDATE
priority: HIGH
implementation_path: python_first
pine_status: not_sufficient_without_external_data
```

Bu videodan çıkarılabilecek ana strateji budur.

---

## 5.2 Objective rule v0

```yaml
strategy_name: QL_TY_MICROCAP_LIQUIDITY_REVERSION_SHORT_v0
direction: short
holding_period: intraday
entry_window:
  - 2_minutes_before_regular_open
  - regular_open
  - first_minutes_after_open
exit_window:
  - near_regular_close
  - no_overnight

universe:
  market: US_equities
  market_cap_max: 50_000_000
  price_min: 1.00
  premarket_volume_min: 1_000_000_shares
  borrow_available: true
  locate_fee_max_pct_position: 3

setup:
  overextension:
    any:
      - premarket_return_from_prev_close >= threshold
      - afterhours_return_previous_day >= threshold
      - multi_day_return_3d >= threshold
      - price_multiple_from_recent_low >= threshold
  liquidity_distortion:
    any:
      - move_occurred_premarket
      - move_occurred_afterhours
      - move_occurred_during_low_liquidity
  dilution_context:
    score_inputs:
      - active_shelf
      - ATM_available
      - warrants_or_convertibles
      - weak_cash_position
      - history_of_pop_and_drop
    required: optional_but_boosts_score

entry:
  mode: short_at_or_near_regular_open
  exact_trigger:
    - open_short
    - or first_1m_failure_after_open
  stop:
    type: fixed_percent_stop
    source: backtest_optimized
    not_based_on_chart_resistance: true

exit:
  primary: cover_near_regular_close
  optional:
    - partial_cover_after_extreme_intraday_drop
    - recycle_on_bounce_only_if_backtested
```

---

## 5.3 Neden Pine ile doğrudan olmaz?

TradingView Pine sadece OHLCV ve sınırlı sembol datası ile çalışır. Bu strateji için gereken kritik veriler:

```yaml
external_data_required:
  - market_cap
  - float
  - borrow availability
  - locate fee
  - regulation SHO status
  - dilution / shelf / ATM data
  - halt status
  - premarket and afterhours intraday data
  - delisted symbols for survivorship-bias-free backtest
```

Pine sadece görselleştirme / alarm prototipi için kullanılabilir. Asıl test Python’da yapılmalıdır.

---

## 6. Entry ve Stop Mantığı

## 6.1 Entry

Ty çoğu trade’de:

- open’a yakın short;
- bazen open’dan hemen önce;
- sistematik sinyal varsa doğrudan short;
- 1-minute zaman dilimi;
- regular session likidite değişimini hedefliyor.

```yaml
entry_style:
  primary: short_near_open
  reason: regular_session_liquidity_influx
  avoid:
    - midday_consolidation_entries
    - no_liquidity_change_zones
```

---

## 6.2 Stop

Çok önemli fark:

> Stop chart resistance’a göre değil; backtest edilmiş sabit yüzde stop’a göre.

```yaml
stop_logic:
  type: fixed_percent_from_entry
  rationale:
    - microcaps do not respect intraday support/resistance cleanly
    - volatility is extreme
    - systematic consistency needed
  wide_stop_reason:
    - one locate / one bullet problem
    - regulation SHO
    - avoid obvious squeeze levels
```

Bu, Martin Luke videosundaki tight-stop mantığının neredeyse tersidir:

```yaml
contrast:
  martin_luke:
    style: tight_stop_pullback_momentum
    stop: support_or_candle_low
  ty_rajnus:
    style: wide_stop_systematic_short
    stop: fixed_percent_loss_from_entry
```

---

## 7. Exit Mantığı

```yaml
exit:
  primary: cover_near_regular_close
  avoid_overnight: true
  reason:
    - afterhours_liquidity_thins
    - short can spike hundreds/thousands_percent
    - borrow fees continue
    - T1/T12 halt risk
```

Önemli örnek:

- stock yaklaşık $5’ten $125’e afterhours/premarket spike;
- unrealized loss > $250k;
- bu olaydan sonra overnight short bırakmama kuralı.

---

## 8. Locate / Borrow Fee Modülü

Bu stratejide “hisseyi shortlamak” kadar “locate etmek” de ayrı bir edge.

```yaml
locate_rules:
  preferred_fee_pct_position: <= 2_to_3_percent
  average_fee_reported: about_1_percent
  avoid:
    - 5_percent_plus_fees
    - 10_percent_plus_fees
    - 15_to_20_percent_fees
```

Çok yüksek locate fee bazen squeeze riskini artırabilir:

```yaml
high_locate_fee_interpretation:
  meaning:
    - many shorts want shares
    - shares scarce
    - squeeze potential higher
  action:
    - reduce
    - skip
    - treat_as_warning
```

---

## 9. Halt Risk Modülü

## 9.1 LUDP halt

```yaml
LUDP_risk:
  issue:
    - stock can gap violently after halt resume
    - stop can be bypassed
  mitigation:
    - avoid halt-resume-halt-resume names
    - scale out before stop on halt-prone names
    - use multiple partial stop levels
```

Ty’nin örnek risk yönetimi:

```yaml
halt_prone_scaleout_example:
  statistical_stop: 50%
  scaleout_levels:
    - 30%
    - 40%
    - 50%
    - 60%
    - 70%
  purpose: reduce gap-through-stop damage
```

---

## 9.2 T1 / T12 halt

```yaml
T1_T12_risk:
  danger: extreme
  issue:
    - stock may be halted days/weeks/months
    - short borrow fee continues
    - impossible_to_exit
  avoidance:
    - avoid very_low_volume names
    - require millions of premarket volume
    - avoid suspicious halt-heavy tickers
```

---

## 10. Backtest Metodolojisi

Video, QuantLens açısından çok değerli bir backtest yaklaşımı içeriyor.

```yaml
backtest_principles:
  - start from broad directional bias
  - define market cap range
  - define timeframe
  - define catalyst/price action
  - keep strategy simple
  - avoid overfitting
  - include delisted symbols
  - compare forward result to theoretical result daily
  - optimize size from max historical drawdown
```

---

## 10.1 Önerilen Python data schema

```yaml
table: microcap_short_events

columns:
  date: datetime
  ticker: string
  market_cap: float
  price_prev_close: float
  premarket_open: float
  premarket_high: float
  premarket_low: float
  premarket_last_before_open: float
  regular_open: float
  regular_high: float
  regular_low: float
  regular_close: float
  afterhours_high_previous_day: float
  volume_premarket: float
  volume_regular: float
  dollar_volume_premarket: float
  dollar_volume_regular: float
  percent_gap: float
  percent_premarket_run: float
  percent_multiday_run_3d: float
  float_shares: float
  short_interest: float
  locate_fee_pct: float
  borrow_available: bool
  reg_sho: bool
  halted_intraday: bool
  halt_count: int
  dilution_active_shelf: bool
  atm_available: bool
  shelf_shares_available: float
  cash_months_remaining: float
  news_theme: string
  entry_price: float
  stop_price: float
  exit_price: float
  pnl_pct: float
```

---

## 10.2 Basit Excel backtest mantığı

Ty’nin yaklaşımı Excel ile de yapılabilir. Bölgesel Excel ayarı için `;` kullanılarak örnek:

```excel
=EĞER([@[MaxAdverseMovePct]]>=[@[StopPct]];-[@[StopPct]];[@[ExitReturnPct]])
```

İngilizce Excel fonksiyonu kullanan sistemlerde:

```excel
=IF([@[MaxAdverseMovePct]]>=[@[StopPct]];-[@[StopPct]];[@[ExitReturnPct]])
```

Not: Senin Excel ayarında argüman ayırıcı olarak `;` kullanılmalı.

---

## 11. Position Sizing / Drawdown Engine

Ty’nin sizing yaklaşımı:

```yaml
sizing:
  source: historical_backtest_max_drawdown
  goal:
    - find sweet spot between high return and tolerable drawdown
  principle:
    - if historical worst drawdown repeats, account still survives
  compounding:
    - dynamic position size increases as equity grows
    - does not decrease size during year
    - leaves buffer to size up during deep drawdown
```

Bu, QuantLens için ayrı bir modül olmalı:

```yaml
module: QL_BACKTEST_DRAWDOWN_SIZING_ENGINE
inputs:
  - trade_return_series
  - position_size_grid
  - max_drawdown_by_grid
  - annual_return_by_grid
outputs:
  - recommended_position_size
  - expected_drawdown
  - expected_return
  - risk_of_ruin_proxy
```

---

## 12. Best Trade Case Study — CWD

```yaml
case_study: CWD
theme: crypto_treasury_microcap
context:
  - post_election_crypto_hype
  - many tiny companies announcing crypto treasury plans
  - news cycle was late-stage
  - stock spiked from around $5-$6 to $56 premarket
  - true parabolic
  - active ATM/shelf shares available
setup_quality: A+
entry:
  - short near/open just before regular session
exit:
  - hold most of day
  - cover near close
result:
  - largest trade around $29k
```

Key lesson:

```yaml
why_it_worked:
  - extreme low-liquidity premarket price distortion
  - late-cycle hype catalyst
  - dilution available
  - regular session liquidity allowed selling pressure
  - clean collapse after open
```

---

## 13. Worst Risk Case Studies

## 13.1 LUDP halt gap

```yaml
risk_case: LUDP_halt_gap
danger:
  - price can gap from 65 to over 100 after halt
  - stop can be bypassed
mitigation:
  - avoid halt-heavy names
  - scale out before statistical stop
```

## 13.2 T12 halt

```yaml
risk_case: T12_information_requested
danger:
  - halted for weeks/months
  - borrow fees continue
  - no exit possible
mitigation:
  - avoid low-volume suspicious names
  - require millions of shares volume
```

## 13.3 Overnight spike

```yaml
risk_case: overnight_short_tail
example:
  - stock spiked from around $5 to $125 overnight/premarket
lesson:
  - no overnight holding in this strategy
```

---

## 14. Codex Implementation Plan

## Phase 0 — Research Folder

Create:

```text
06_QUANTLENS_LAB/
  strategies/
    TY_MICROCAP_SHORT/
      README.md
      SPEC.md
      DATA_SCHEMA.md
      BACKTEST_PLAN.md
      RISK_NOTES.md
      configs/
        ty_microcap_short_v0.yml
      src/
        universe.py
        features.py
        backtest.py
        sizing.py
        reports.py
      tests/
        test_features.py
        test_sizing.py
```

---

## Phase 1 — Event Dataset Builder

Build a dataset from daily/intraday US equities data:

```yaml
required:
  - premarket OHLCV
  - regular session 1m OHLCV
  - afterhours OHLCV
  - delisted symbol support
optional_but_important:
  - market cap
  - float
  - dilution data
  - locate fee
  - borrow availability
  - halt status
```

If borrow/locate data is unavailable, run as **theoretical edge only**.

---

## Phase 2 — Feature Engineering

Implement:

```yaml
features:
  - premarket_return_pct
  - afterhours_return_pct
  - regular_previous_day_extension_pct
  - multi_day_return_3d
  - volume_premarket
  - dollar_volume_premarket
  - market_cap_filter
  - price_filter
  - dilution_score
  - halt_risk_score
  - locate_fee_filter
```

---

## Phase 3 — Backtest Engine

Core simulation:

```yaml
entry:
  - short at regular open
  - or short 1 minute before open if data supports
stop:
  - fixed percent adverse move
  - test grid: 20%, 30%, 40%, 50%, 60%, 70%, 100%
exit:
  - regular close
  - or N minutes before close
fees:
  - commissions
  - locate_fee_pct
  - borrow_fee_intraday
slippage:
  - configurable
```

---

## Phase 4 — Risk Engine

Add:

```yaml
risk_controls:
  - skip if halt_count_today > threshold
  - skip if volume_premarket < threshold
  - skip if locate_fee_pct > threshold
  - scaleout on halt-prone names
  - no overnight hold
  - max_daily_loss
  - max_trade_count_per_day
  - max_strategy_drawdown_pause
```

---

## Phase 5 — Reporting

Generate:

```yaml
report_metrics:
  - trade_count
  - win_rate
  - avg_win
  - avg_loss
  - profit_factor
  - max_drawdown
  - monthly_returns
  - largest_winner
  - largest_loser
  - theoretical_vs_actual
  - stop_grid_heatmap
  - locate_fee_sensitivity
  - premarket_volume_sensitivity
  - market_cap_bucket_performance
```

---

## 15. Codex Prompt

Aşağıdaki prompt doğrudan Codex’e verilebilir.

```text
You are working inside the QuantLens repo.

Task:
Create a research-only Python prototype for the Ty Rajnus microcap short strategy.

Important:
This is not a live trading system. It is a research/backtest module only.
Do not add broker execution. Do not add live order placement.

Strategy concept:
Short-only US nano-cap/micro-cap stocks that have extreme upside overextension, especially when the move occurs in premarket/afterhours/low-liquidity conditions. The expected edge is regular-session liquidity normalization plus dilution/selling pressure.

Implement folder:
06_QUANTLENS_LAB/strategies/TY_MICROCAP_SHORT/

Create files:
- README.md
- SPEC.md
- DATA_SCHEMA.md
- BACKTEST_PLAN.md
- RISK_NOTES.md
- configs/ty_microcap_short_v0.yml
- src/features.py
- src/backtest.py
- src/sizing.py
- src/reports.py
- tests/test_features.py
- tests/test_sizing.py

Core rules v0:
Universe:
- US equities only
- market_cap <= 50_000_000 if market cap data exists
- price >= 1.00
- premarket_volume >= configurable threshold, default 1_000_000 shares
- locate_fee_pct <= configurable threshold, default 3%, if locate data exists

Setup:
- premarket_return_from_prev_close >= configurable threshold
OR afterhours_return_previous_day >= configurable threshold
OR multi_day_return_3d >= configurable threshold
- optional dilution_score from active_shelf, ATM_available, warrants, convertibles
- skip if low volume and halt-risk flags are present

Entry:
- short at regular session open by default
- allow config option for short 1 minute before open if data supports it

Stop:
- fixed percent adverse stop, not chart-level based
- grid test stop values: 20%, 30%, 40%, 50%, 60%, 70%, 100%

Exit:
- cover near regular session close
- no overnight holding

Fees:
- commission
- slippage
- locate_fee_pct
- optional borrow fee

Backtest outputs:
- trade_count
- win_rate
- avg_win
- avg_loss
- profit_factor
- max_drawdown
- monthly returns
- largest winner/largest loser
- stop grid results
- market cap bucket results
- premarket volume bucket results
- locate fee sensitivity

Sizing module:
- evaluate position-size grid against historical max drawdown
- recommend a size where return is high but max drawdown remains below configured tolerance

Tests:
- feature calculations for percent returns and filters
- fixed percent stop logic
- no overnight exit rule
- sizing grid max drawdown calculation

Deliver final report:
06_QUANTLENS_LAB/strategies/TY_MICROCAP_SHORT/TY_MICROCAP_SHORT_IMPLEMENTATION_REPORT.md

The final report must include:
- files created
- assumptions
- what was implemented
- what was not implemented
- missing data requirements
- how to run tests
- next steps
```

---

## 16. QuantLens “Try / Skip” Recommendation

```yaml
try_now:
  - Python research prototype
  - feature library for overextension/liquidity transition
  - stop grid backtest
  - drawdown-based sizing engine
  - theoretical-vs-actual report template

do_not_try_now:
  - live short execution
  - Pine-only implementation
  - crypto direct port
  - strategy without borrow/locate/halt modeling
```

---

## 17. TradingView / Pine Adaptation

Pine can only implement a simplified visual scanner:

```yaml
pine_possible:
  - detect huge percent gain
  - detect extension from EMA/VWAP
  - detect abnormal volume
  - mark regular session open fade
  - plot risk zones

pine_not_possible_cleanly:
  - market cap filter
  - dilution / shelf
  - borrow availability
  - locate fees
  - halt/T12 risk
  - delisted data
```

A Pine version should be called:

```text
TY_MICROCAP_SHORT_VISUAL_SCANNER_ONLY
```

Not a production strategy.

---

## 18. Crypto Transferability

```yaml
crypto_transferability: LOW_TO_MEDIUM
transferable_concepts:
  - low liquidity pump
  - overextension
  - session liquidity transition
  - fake price in thin books
  - mean reversion after hype
not_transferable:
  - equity dilution
  - ATM offering
  - locate fees
  - borrow mechanics
  - exchange halt rules
```

Crypto için en yakın karşılık:

```yaml
crypto_equivalent:
  - low-liquidity altcoin pump
  - CEX listing pump
  - funding/short squeeze unwind
  - liquidation cascade reversal
  - session open liquidity shift
```

Fakat bu doğrudan aynı strateji değildir.

---

## 19. Risk Warning

This system is dangerous for inexperienced traders.

```yaml
major_risks:
  - unlimited short loss
  - halt gap through stop
  - T1/T12 halt with no exit
  - borrow fee explosion
  - locate unavailability
  - broker restriction
  - slippage
  - low-liquidity manipulation
  - regulatory constraints
```

This should stay in QuantLens as **research only** until execution realism is modeled.

---

## 20. Final Rating

```yaml
final_rating:
  research_value: 9/10
  implementation_clarity: 8/10
  direct_live_suitability: 2/10
  python_backtest_priority: 8/10
  pine_strategy_priority: 3/10
  risk_engine_value: 10/10
  process_value: 10/10
```

Final conclusion:

> Bu video, QuantLens için “hemen trade edilecek strateji” değil; ama **çok değerli bir systematic short research framework**. En iyi çıkarım, microcap short stratejisinden ziyade; overextension ölçümü, liquidity-transition entry mantığı, stop-grid backtest, drawdown-based sizing ve theoretical-vs-actual execution tracking modülleridir.

---

## 21. Short Checklist

```yaml
candidate_trade_checklist:
  - Is stock nano/micro cap?
  - Is price above $1?
  - Did it move at least 50% quickly?
  - Did move occur in premarket/afterhours/low liquidity?
  - Is regular session open near?
  - Is premarket volume in millions?
  - Are locates available?
  - Is locate fee below 2-3%?
  - Is there active dilution/shelf/ATM?
  - Is halt risk acceptable?
  - Is fixed percent stop defined before entry?
  - Is no-overnight rule enforced?
  - Is position size compatible with historical max drawdown?
```

---

## 22. Decision

```yaml
decision: KEEP_AND_PROTOTYPE
next_action:
  - give Codex the implementation prompt
  - build research-only Python module
  - do not live trade
```
