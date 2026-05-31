# QUANTLENS TRANSCRIPT INTAKE REPORT — Critical Review  
## EMA 20/50 Crossover + Two Retests Strategy

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/RHlsVNSM8Aw?si=g54Kry_ryc8pYWPK  
**Normalized URL:** https://www.youtube.com/watch?v=RHlsVNSM8Aw  
**Video ID:** `RHlsVNSM8Aw`  
**Transcript Status:** Provided by user in chat  
**Review Mode:** Critical / skeptical  
**Transcript Digest SHA256:** `083a8946c1681e3b28f6a992144ff4432402c13f090de73e1a460a010d9e395c`

---

## 1. Executive Verdict

```yaml
classification: LOW_VALUE_GENERIC_STRATEGY
quantlens_priority: LOW
codex_status: DO_NOT_IMPLEMENT_FULL_STRATEGY_NOW
production_ready: false
python_backtest_ready: only_as_baseline_test
pine_visual_ready: possible_but_low_priority
decision: REJECT_AS_PRIMARY_STRATEGY
```

Bu video, önceki **Martin Luke pullback / anchored VWAP** ve **Ty Rajnus systematic short** videolarına göre çok daha zayıf. Buradaki anlatım basit bir **20 EMA / 50 EMA crossover + iki retest bekleme** fikrinden ibaret.

Ana sorun: strateji “kurala benziyor” ama gerçek bir backtest stratejisi olmak için gerekli parçaların çoğu yok.

---

## 2. Videoda Anlatılan Strateji

```yaml
indicators:
  - 20 EMA
  - 50 EMA

short_setup:
  - price below both 20 EMA and 50 EMA
  - 20 EMA crosses below 50 EMA
  - wait for two successful retests after crossover
  - then sell

long_setup:
  implied_but_not_clearly_explained:
    - price above both 20 EMA and 50 EMA
    - 20 EMA crosses above 50 EMA
    - wait for two successful retests
    - then buy
```

Videonun çekirdeği:

> EMA crossover tek başına yetmez; crossover sonrası trendin gelişmesi için iki başarılı retest beklenir.

Bu fikir tamamen değersiz değil; fakat çok genel.

---

## 3. Kritik Eksikler

## 3.1 Timeframe yok

Strateji hangi zaman diliminde uygulanacak?

```yaml
missing_timeframe:
  - 1m?
  - 5m?
  - 15m?
  - 1h?
  - daily?
```

EMA crossover stratejilerinde zaman dilimi sonucu tamamen değiştirir. 5 dakikalık grafikte çok fazla whipsaw üretir; daily grafikte geç kalabilir. Video bu ayrımı yapmıyor.

---

## 3.2 Stop-loss yok

En büyük eksik budur.

```yaml
missing_risk:
  - initial_stop_loss
  - invalidation_level
  - max_stop_distance
  - risk_per_trade
  - position_sizing
```

Bir stratejide giriş sinyali tek başına strateji değildir. Stop yoksa backtest anlamlı olmaz.

---

## 3.3 Take-profit / exit yok

Video sadece giriş mantığı veriyor.

```yaml
missing_exit:
  - profit_target
  - trailing_stop
  - opposite_cross_exit
  - close_below_ema_exit
  - time_stop
  - partial_take_profit
```

EMA crossover sistemlerinde exit kuralı performansı entry kadar etkiler. Burada exit tanımı yok.

---

## 3.4 “İki başarılı retest” tanımı belirsiz

Bu ifade mekanik değil.

```yaml
ambiguous_retest_questions:
  - Retest hangi EMA'ya yapılacak?
  - 20 EMA mı?
  - 50 EMA mı?
  - iki EMA arasındaki bölge mi?
  - crossover seviyesi mi?
  - swing support/resistance mı?
  - retest wick ile mi sayılır?
  - close ile mi sayılır?
  - kaç bar içinde olmalı?
  - retest sonrası giriş trigger'ı ne?
```

Bu belirsizlik çözülmeden Codex’in doğru backtest yazması mümkün olmaz.

---

## 3.5 Backtest / istatistik yok

Video hiçbir performans kanıtı vermiyor.

```yaml
missing_evidence:
  - win_rate
  - profit_factor
  - max_drawdown
  - average_R
  - sample_size
  - tested_symbols
  - tested_timeframes
  - commission/slippage
  - out_of_sample_test
```

Bu nedenle strateji “kanıtlanmış edge” değil, sadece “test edilebilir fikir” kabul edilmeli.

---

## 3.6 Çok genel pazarlama iddiası var

Video “forex, stocks, crypto” için kullanılabileceğini söylüyor. Bu iddia fazla geniş.

```yaml
claim_quality:
  broad_asset_claim: weak
  reason:
    - forex mean-reversion/volatility yapısı farklı
    - stocks gap riski taşır
    - crypto 24/7 olduğu için gap ve session yapısı farklıdır
    - EMA crossover tüm piyasalarda whipsaw üretebilir
```

“Price action her yerde aynıdır” ifadesi kısmen doğru ama strateji validasyonu için yeterli değildir.

---

## 4. Önceki Videolarla Karşılaştırma

| Kriter | Martin Luke | Ty Rajnus | Bu EMA Videosu |
|---|---:|---:|---:|
| Gerçek trader performansı | Güçlü | Güçlü | Yok |
| Risk yönetimi | Var | Çok güçlü | Yok |
| Entry detayı | Detaylı | Detaylı | Zayıf |
| Exit detayı | Orta | Güçlü | Yok |
| Backtest yaklaşımı | Kısmen | Çok güçlü | Yok |
| Uygulanabilirlik | Yüksek | Niş ama güçlü | Düşük |
| QuantLens önceliği | Çok yüksek | Yüksek / niş | Düşük |

---

## 5. Stratejinin İyi Tarafı Var mı?

Evet, ama sınırlı.

Alınabilecek fikir:

```yaml
useful_kernel:
  idea: EMA crossover sonrası hemen girmek yerine retest beklemek
  reason:
    - false breakout azaltabilir
    - trendin oturmasını bekler
    - entry fiyatını iyileştirebilir
    - whipsaw sayısını azaltabilir
```

Bu fikir QuantLens’te bir **trend-confirmation filter** olarak denenebilir.

Ama bağımsız ana strateji olarak zayıf.

---

## 6. QuantLens İçin Olası Baseline Test

Tam strateji değil, yalnızca baseline araştırma:

```yaml
candidate_id: QL_BASELINE_EMA20_50_RETEST_001
priority: LOW
purpose:
  - compare against stronger strategies
  - test whether two-retest filter improves basic EMA crossover
  - use as benchmark, not production strategy
```

---

## 7. Mekanik Hale Getirilmiş Test Versiyonu

Video belirsiz olduğu için test etmek istersek kuralları bizim tanımlamamız gerekir.

## 7.1 Long v0

```yaml
long_conditions:
  trend:
    - ema20 > ema50
    - close > ema20
    - close > ema50
  crossover:
    - ema20 crossed above ema50 within last N bars
  retest:
    - price touches or comes within X percent of ema20 or ema50
    - close remains above ema50
    - two separate retest events required
  entry:
    - buy on break above high of second retest candle
```

## 7.2 Short v0

```yaml
short_conditions:
  trend:
    - ema20 < ema50
    - close < ema20
    - close < ema50
  crossover:
    - ema20 crossed below ema50 within last N bars
  retest:
    - price touches or comes within X percent of ema20 or ema50
    - close remains below ema50
    - two separate retest events required
  entry:
    - sell/short on break below low of second retest candle
```

---

## 8. Stop ve Exit Bizim Eklememiz Gerekir

Önerilen test parametreleri:

```yaml
risk_model_v0:
  stop_options:
    - ATR_stop: 1.5_ATR
    - structure_stop: below_second_retest_swing_low_for_long
    - structure_stop_short: above_second_retest_swing_high_for_short
  take_profit_options:
    - 2R
    - 3R
    - trailing_ema20
    - opposite_cross
  time_stop:
    - exit_after_50_bars_if_no_1R
```

---

## 9. Beklenen Zayıflıklar

```yaml
expected_failure_modes:
  - late_entries_after_crossover
  - whipsaw_in_range_market
  - poor_R_if_stop_is_wide
  - trend_already_extended_after_two_retests
  - ambiguous_retest_detection
  - underperformance_vs_simple_trend_following
```

Özellikle iki retest beklemek bazen faydalı olur, ama güçlü trendlerde girişi çok geciktirebilir.

---

## 10. Backtest Edilecekse Minimum Test Planı

```yaml
test_plan:
  symbols:
    crypto:
      - BTCUSDT
      - ETHUSDT
      - SOLUSDT
      - BNBUSDT
      - XRPUSDT
    stocks_optional:
      - QQQ
      - SPY
      - TSLA
      - NVDA
      - AMD
  timeframes:
    - 15m
    - 1h
    - 4h
    - daily
  variants:
    - basic_ema_cross
    - ema_cross_plus_one_retest
    - ema_cross_plus_two_retests
    - ema_cross_plus_two_retests_plus_atr_stop
    - ema_cross_plus_two_retests_plus_ema_trailing_exit
```

Önemli karşılaştırma:

```yaml
benchmark_required:
  - two_retest_model_vs_basic_ema_cross
  - two_retest_model_vs_buy_and_hold
  - two_retest_model_vs_supertrend
  - two_retest_model_vs_martin_pullback_model
```

---

## 11. Codex’e Verilecek Kısa Eleştirel Prompt

Bu stratejiye büyük geliştirme zamanı harcanmamalı. Yalnızca hızlı sanity-check yapılmalı.

```text
You are working inside the QuantLens repo.

Task:
Create a very small Python baseline backtest for a low-priority EMA 20/50 crossover + two-retest idea.

Important:
This is a skeptical test. Do not treat the YouTube strategy as proven.
The source video provides no stop-loss, no take-profit, no timeframe, no statistics, and no precise retest definition.
Your job is to create a minimal test harness and report whether the retest filter adds value compared with a plain EMA crossover.

Create folder:
06_QUANTLENS_LAB/strategies/BASELINE_EMA20_50_RETEST/

Create files:
- README.md
- SPEC.md
- configs/ema20_50_retest_v0.yml
- src/backtest.py
- src/features.py
- src/rules.py
- src/report.py
- tests/test_retest_detection.py

Define mechanical rules:
Long:
- EMA20 > EMA50
- EMA20 crossed above EMA50 within lookback bars
- price remains above EMA50
- detect two separate retests of EMA20/EMA50 zone
- enter on break above second retest candle high

Short:
- EMA20 < EMA50
- EMA20 crossed below EMA50 within lookback bars
- price remains below EMA50
- detect two separate retests of EMA20/EMA50 zone
- enter on break below second retest candle low

Risk:
- ATR stop default 1.5 ATR
- alternative structure stop below/above second retest swing
- take profit test variants: 2R, 3R, EMA20 trailing, opposite cross
- commission and slippage must be included

Test:
- Compare plain EMA crossover vs one-retest vs two-retest versions
- Test on BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
- Timeframes: 15m, 1h, 4h
- Report win rate, profit factor, max drawdown, average R, trade count, expectancy

Final report:
06_QUANTLENS_LAB/strategies/BASELINE_EMA20_50_RETEST/EMA20_50_RETEST_BASELINE_REPORT.md

Final verdict must be one of:
- REJECTED_NO_EDGE
- WEAK_FILTER_ONLY
- KEEP_FOR_FURTHER_RESEARCH

Do not over-engineer.
Do not build Pine yet.
Do not add to production strategy library unless results are clearly robust.
```

---

## 12. Final Decision

```yaml
final_decision: REJECT_AS_PRIMARY_STRATEGY
useful_as:
  - low_priority_baseline
  - EMA trend filter comparison
  - retest filter experiment
not_useful_as:
  - production strategy
  - high-confidence QuantLens module
  - Codex full implementation project
```

Sonuç:

> Bu videodan doğrudan ciddi bir strateji çıkarmak doğru olmaz. En fazla “EMA crossover sonrası retest beklemek whipsaw’ı azaltıyor mu?” sorusu için küçük bir Python baseline testi yapılabilir. Martin Luke ve Ty Rajnus raporlarındaki edge kalitesiyle aynı seviyede değildir.
