# YouTube Strategy Transcript Intake Report

## 1. Intake Metadata

- Intake ID: `INTAKE_2026-05-03_q43pkYBo1hU`
- Candidate ID Önerisi: `YT_Q43PKYBO1HU_SWING_MOMENTUM_POST_EARNINGS_V1`
- Kaynak Dosya: `+259% in 1 Year - Swing Trading Performance Strategy.md`
- Prompt Dosyası: `00_quantlens_transcript_intake_prompt.md`
- Source URL: `https://youtu.be/q43pkYBo1hU?si=JM_zb7YAWo5N2rls`
- Normalized URL: `https://www.youtube.com/watch?v=q43pkYBo1hU`
- Video ID: `q43pkYBo1hU`
- Başlık: `+259% in 1 Year - Swing Trading Performance Strategy`
- Kanal: `UNKNOWN_CHANNEL`  
  - Not: Transcript içinde podcast/host referansı var; fakat güvenilir kanal adı ve kanal ID alanı ayrı verilmediği için blacklist kararı verilmedi.
- Transcript Hash SHA256: `2cdbb9e4f47bb5579a07686ba58ed8f1e45baa863969df4d5269db68c1ebaae3`
- Transcript Hash Short: `2cdbb9e4f47bb557`
- Rapor Tarihi: `2026-05-03`

---

## 2. Kesin Kural Uyumluluk Durumu

- `01_PINE/MTC_V2.pine` değiştirilmedi.
- Production Python runner dosyaları değiştirilmedi.
- Backtest çalıştırılmadı.
- Optimization çalıştırılmadı.
- Büyük CSV, data bundle, cache veya optimization sonucu oluşturulmadı.
- Secret/API key/webhook/broker/exchange bilgisi yazılmadı.
- Bu rapor sadece transcript intake/triage amaçlıdır.

---

## 3. Duplicate / Registry Kontrolü

### 3.1 Repo Registry Durumu

- `_registry/youtube_video_index.csv`: Bu çalışma ortamında erişilemedi.
- `channel_blacklist.yaml`: Bu çalışma ortamında erişilemedi.
- `channel_quality_registry.csv`: Bu çalışma ortamında erişilemedi.

### 3.2 Bu Konuşma İçi Kontrol

- Aynı `video_id` ile daha önce bu konuşma içinde işlenmiş bir rapor görülmedi.
- Aynı transcript hash ile daha önce bu konuşma içinde işlenmiş bir rapor görülmedi.

### 3.3 Sonuç

- Duplicate Status: `NOT_DUPLICATE_IN_CURRENT_SESSION`
- Repo-Level Duplicate Status: `NOT_VERIFIED_REPO_REGISTRY_UNAVAILABLE`
- Aksiyon: Codex repo içinde çalışırken önce gerçek registry dosyalarını okumalıdır. Eğer `video_id` veya `transcript_hash` daha önce varsa yeni candidate oluşturmamalıdır.

---

## 4. Channel Quality / Blacklist Kontrolü

- Kanal: `UNKNOWN_CHANNEL`
- Blacklist kontrolü: `NOT_VERIFIED_CHANNEL_ID_UNAVAILABLE`
- Kanal kalite kararı: `UNKNOWN`
- Blacklist aksiyonu: Yok.

Not: Kanal ID veya güvenilir kanal adı gelmediği için tek video üzerinden blacklist/watchlist kararı verilmemelidir.

---

## 5. Sınıflandırma Kararı

- Ana Sınıflandırma: `CANDIDATE`
- Codex Status Önerisi: `READY_FOR_PYTHON_PROTOTYPE`
- İkinci Etiket: `SALVAGE_KNOWLEDGE_AVAILABLE`
- Trader Wiki Etiketi: `OPTIONAL_WIKI_NOTE`
- Usefulness Score: `8/10`
- Prototype Priority: `HIGH`
- Pine’a Geçiş: `NO_FOR_NOW`

### Gerekçe

Transcript yalnızca motivasyon/psikoloji anlatımı değildir. Kodlanabilir strateji bileşenleri içerir:

- Hisse seçimi için sayısal filtreler: fiyat, relative strength, ATR, ortalama hacim, sektör, pozitif kârlılık.
- Trend/regime kontrolü: 50/200 MA, QQQ trendi, VIX, put/call, market theme.
- Entry setup aileleri: breakout, pullback, flag/consolidation, post-earnings reversal, ETF regime test.
- Risk ve position sizing: trade başına %1-1.5 hesap riski, 3R hedef, teknik stop.
- Exit kuralları: teknik stop, abnormal action exit, partial scale-out, market extension azaltımı.

Buna rağmen anlatım tamamen mekanik değil. Bu yüzden doğrudan Pine stratejiye değil, önce Python research prototype ve kural netleştirme aşamasına alınmalıdır.

---

## 6. Kısa Özet

Video, Deepak Uppal’ın yüksek getirili swing trading yaklaşımını anlatıyor. Strateji ana hatlarıyla yüksek fiyatlı, yüksek ATR’li, güçlü relative strength gösteren, çoğunlukla teknoloji/yarı iletken/perakende hisselerinde kısa-orta vadeli swing trade arıyor. Trader, market ortamı iyi olduğunda yoğun pozisyon ve margin kullanıyor; market zayıf veya belirsiz olduğunda ETF’lerle test ediyor veya riski azaltıyor. Risk yönetimi yaklaşımı trade başına yaklaşık %1-%1.5 hesap riski ve en az 3R hedef üzerine kuruluyor.

Ana fikir: büyük getiriler tek başına iyi entry’den değil, doğru market ortamı + dar teknik risk + yoğun ama kontrollü pozisyon + hızlı loss cutting + kazananlarda kademeli çıkış kombinasyonundan geliyor.

---

## 7. Strateji Hipotezi

### 7.1 Ana Hipotez

Yüksek relative strength, yüksek ATR ve güçlü sektör temasına sahip hisselerde; piyasa uptrend veya yeni toparlanma rejimindeyken breakout/pullback/post-earnings reversal girişleri, teknik stop ve 3R+ hedeflerle pozitif expectancy üretebilir.

### 7.2 Alt Hipotezler

1. `High RS + High ATR + Price >= 75` filtresi, küçük hareketlerin bile hesap üzerinde anlamlı dolar etkisi yaratmasını sağlar.
2. 50 MA > 200 MA ve her iki ortalamanın yukarı eğimli olması, zayıf trendleri filtreler.
3. Market regime iyi olduğunda konsantre pozisyonlar getiriyi büyütür; kötü regime’de aynı agresiflik drawdown üretir.
4. Earnings sonrası ilk negatif/karışık reaksiyondan sonra opening high reclaim veya intraday reversal, yüksek momentumlu kısa swing fırsatı verebilir.
5. Teknik stop düşük riskliyse, yoğun pozisyon bile hesap riski açısından yönetilebilir olabilir.

---

## 8. Kodlanabilir Strateji Bileşenleri

### 8.1 Universe / Asset Selection

Önerilen başlangıç universe:

- US equities.
- Ana sektörler: teknoloji, yarı iletkenler, perakende.
- Alternatif olarak leveraged ETF’ler: QQQ/Russell/sector ETF türevleri; Python prototype’ta ayrı modül olarak tutulmalı.
- Hariç tutulanlar: metals, energy, financials, individual biotech, commodity-linked names.

Kodlanabilir filtreler:

```yaml
universe_filters:
  price_min: 75
  relative_strength_min: 85
  atr_abs_min: 5
  avg_volume_shares_min: 150000
  sector_allowlist:
    - technology
    - semiconductors
    - retail
    - leveraged_etf
  require_positive_earnings: true
  require_positive_sales_growth: optional
  exclude_groups:
    - metals
    - energy
    - financials
    - biotech_individual_stocks
```

### 8.2 Trend Filter

```yaml
trend_filter:
  ma_fast: 50
  ma_slow: 200
  require_fast_above_slow: true
  require_slow_slope_positive: true
  require_fast_slope_positive: true
  min_uptrend_age_days: 20_to_40
  optional_ma_short: 21
```

### 8.3 Market Regime Filter

```yaml
market_regime:
  benchmark: QQQ
  bullish_if:
    - benchmark_price_above_50dma
    - benchmark_50dma_above_200dma_or_recovering
    - breakouts_follow_through_recently
  defensive_if:
    - benchmark_below_50dma
    - failed_breakouts_cluster
    - vix_expanding
    - put_call_extreme_not_confirmed
  aggression_scale:
    bullish: 1.0
    neutral: 0.35_to_0.60
    bearish: 0.0_to_0.25
```

Not: “breakouts working” gibi discretionary kavramlar Python’da breadth/follow-through proxy ile ölçülmelidir.

### 8.4 Entry Setup A — Trend Breakout / Pivot Reclaim

```yaml
entry_setup_breakout:
  pattern_family:
    - cup_handle
    - flag
    - horizontal_consolidation
    - pullback_to_support
  trigger_options:
    - close_above_pivot
    - intraday_cross_above_prior_bar_high
    - break_downtrend_line
    - buy_stop_at_breakout_level
  confirmation:
    volume_above_average: preferred
    market_regime_not_bearish: required
  invalidation:
    technical_stop_below_low_or_support
```

### 8.5 Entry Setup B — Post-Earnings Overreaction Reversal

```yaml
entry_setup_post_earnings_reversal:
  preconditions:
    - earnings_event_recent: true
    - earnings_quality_not_bad: required_if_data_available
    - sector_theme_positive: preferred
    - initial_market_reaction_negative_or_muted: true
  trigger_options:
    - price_crosses_opening_high_after_gap_down
    - price_reclaims_intraday_downtrend_line
    - price_reclaims_key_ma_or_prior_support
  holding_period_expected_days: 3_to_10
  risk:
    stop_below_intraday_low_or_event_day_low
```

### 8.6 Entry Setup C — Leveraged ETF Market Test / Snapback

```yaml
entry_setup_etf_test:
  instruments:
    - TQQQ
    - QQQ_related_ETF
    - Russell_related_ETF
    - sector_ETF
  use_case:
    - uncertain_market_recovery
    - market_pullback_snapback
    - avoid_single_stock_specific_risk
  trigger_options:
    - trendline_hold
    - oversold_put_call_extreme
    - vix_stabilization
    - reclaim_short_ma
  exit:
    - into_50dma_resistance
    - volatility_reexpansion
    - failed_reclaim
```

---

## 9. Position Sizing / Risk Model

### 9.1 Risk Per Trade

```yaml
risk_model:
  account_risk_per_trade_pct_min: 1.0
  account_risk_per_trade_pct_max: 1.5
  target_r_multiple_min: 3.0
  max_simultaneous_full_risk_trades: 3
  drawdown_warning_if_multiple_stops_hit_same_time: true
```

### 9.2 Concentration

Transcriptte anlatılan discretionary yaklaşım yüksek konsantrasyon ve margin kullanıyor. MTC/Python prototype için bu doğrudan agresif uygulanmamalı; önce güvenli cap ile test edilmeli.

```yaml
position_concentration:
  baseline_max_positions: 3_to_5
  prototype_max_position_equity_pct: 25_to_40
  aggressive_research_only_max_position_equity_pct: 80
  margin_allowed_in_research: optional
  margin_cap_required: true
```

### 9.3 Sizing Formula

```text
risk_amount = account_equity * risk_pct
stop_distance = abs(entry_price - stop_price)
shares = floor(risk_amount / stop_distance)
notional = shares * entry_price
notional = min(notional, account_equity * max_position_equity_pct * leverage_cap)
```

---

## 10. Exit Logic

### 10.1 Stop Loss

```yaml
stop_loss:
  type: technical
  sources:
    - low_of_day
    - recent_swing_low
    - consolidation_low
    - intraday_5m_structure_low
    - event_day_low_for_earnings_setup
  buffer:
    high_price_stock_usd_buffer: 0.75_to_1.00
    atr_buffer_optional: 0.05_to_0.15_ATR
  avoid_too_tight_stop: true
```

### 10.2 Take Profit / Partial Exits

```yaml
take_profit:
  target_r_min: 3.0
  partial_exit_if_r_multiple_high:
    enabled: true
    first_partial: 50_percent_if_8R_or_9R
  scale_out:
    enabled: true
    chunk_pct: 20
  sell_if:
    - stock_acts_abnormal
    - market_extended
    - failed_follow_through
    - key_resistance_reached
```

### 10.3 Break-Even / Stop Adjustment

```yaml
break_even:
  move_to_break_even_early: false
  consider_after_r: 2.0
  note: trader_prefers_not_to_choke_trade_before_3R_unless_market_or_stock_is_extended
```

---

## 11. MTC_V2 ile Bağlantı

### 11.1 Kullanılabilecek MTC_V2 Katmanları

- `ENTRY GATES`
  - MA trend gate: 50/200 uptrend.
  - ATR volatility floor: ATR absolute veya ATR% uyarlaması.
  - Volume gate: volume > average volume.
  - Momentum/RS proxy gate.
  - HTF trend gate: daily/weekly trend alignment.
  - Session gate: özellikle market open sonrası ilk 15-20 dk davranışı ayrı test edilebilir.

- `POSITION MANAGER`
  - Max positions: 3-5.
  - Regime lock: market bearish ise yeni long engelle.
  - Cooldown: failed breakout sonrası tekrar giriş için kontrollü bekleme.
  - Allow flip: equity swing sistemi için ilk aşamada kapalı.

- `POSITION SIZING`
  - Risk pct: %1-%1.5.
  - Stop-distance based sizing.
  - Max leverage cap.
  - Notional cap.

- `EXIT RULES`
  - Initial technical SL.
  - R-based TP.
  - Partial exits.
  - Delayed break-even.
  - Trail optional.
  - Time stop: 3-10 günlük swing holding için prototiplenebilir.

### 11.2 MTC_V2’de Eksik veya Dış Veri Gerektiren Alanlar

- Earnings calendar.
- Earnings quality / sales growth / profitability filtresi.
- IBD/MarketSmith tarzı proprietary relative strength rank.
- Sector/theme leadership ölçümü.
- Put/call ratio ve VIX regime verisi.

Bunlar ilk etapta Python research layer’da dış veri adaptörü veya proxy metriklerle modellenmelidir. Pine’a geçiş için bu dış veri bağımlılıkları azaltılmalı veya sade proxy’lere çevrilmelidir.

---

## 12. Python Prototype Önerisi

### 12.1 Prototype Dosya Önerileri

```text
06_QUANTLENS_LAB/candidates/YT_Q43PKYBO1HU_SWING_MOMENTUM_POST_EARNINGS_V1/
  README.md
  strategy_spec.yml
  research_notes.md
  data_requirements.md
  prototype_plan.md
  validation_plan.md
  trader_wiki_note.md
```

### 12.2 İlk Python Araştırma Modülleri

```text
research/strategies/swing_momentum_post_earnings/
  universe.py
  trend_filters.py
  regime.py
  entries.py
  exits.py
  sizing.py
  backtest_stub.py   # only after intake phase; not in this report
```

### 12.3 İlk Test Edilecek Varyantlar

1. `V1_BREAKOUT_ONLY`
   - Price >= 75
   - ATR >= 5
   - 50MA > 200MA
   - 50MA slope > 0
   - Breakout over 20-day high or consolidation pivot
   - Technical stop under recent swing low
   - 3R target + time stop

2. `V2_PULLBACK_RECLAIM`
   - Same universe filter
   - Pullback to 21/50MA or trendline
   - Reclaim prior day high
   - Stop under pullback low

3. `V3_POST_EARNINGS_REVERSAL`
   - Earnings event last 1-3 sessions
   - Gap down or muted open after non-bad earnings
   - Opening high reclaim
   - Stop under event-day low
   - 3-10 day hold

4. `V4_ETF_REGIME_TEST`
   - QQQ/TQQQ/Russell ETF only
   - Put/call/VIX oversold proxy
   - Trendline or MA reclaim
   - Exit into 50MA/resistance or fixed R

---

## 13. Backtest / Validation Planı

Bu intake raporu backtest çalıştırmadı. Codex’in sonraki aşamada uygulaması gereken validation planı:

1. Önce veri uygunluğunu kontrol et.
2. Fundamental/earnings verisi yoksa yalnızca teknik varyantları test et.
3. Survivorship bias’a dikkat et; current universe ile geçmiş test yanıltıcı olabilir.
4. Komisyon, slippage ve gap riskini dahil et.
5. Walk-forward validation kullan.
6. Market regime kırılımı yap:
   - Bull trend
   - Correction
   - Bear trend
   - Post-correction recovery
7. Sadece toplam getiriye bakma; expectancy, max drawdown, win/loss, R distribution ve average holding period raporla.
8. Çok yüksek concentration/margin testlerini ayrı “research-risk” modunda tut.

---

## 14. Riskli / Şüpheli İddialar

- +259% performans iddiası transcript içinde geçiyor; bu rapor bağımsız doğrulama yapmadı.
- Yoğun pozisyon ve margin kullanımı, küçük hesaplarda veya düşük disiplinli sistemlerde büyük drawdown riski üretir.
- “Dolar bazlı düşünme” yaklaşımı position sizing açısından yanıltıcı olabilir; sistem mutlaka yüzde risk ve R-multiple üzerinden normalize edilmelidir.
- Strategy logic büyük ölçüde discretionary; kodlanırken fazla serbest yorum overfit riskini artırır.
- Earnings stratejisi dış veri ve event handling gerektirir; veri kalitesi düşükse sonuçlar güvenilmez olur.
- US equities için anlatılan kurallar crypto/futures/FX’e doğrudan taşınmamalıdır.

---

## 15. Trader Wiki Notu Önerisi

Bu video aynı zamanda Trader Wiki için de faydalı dersler içeriyor. Fakat ana sınıflandırma `CANDIDATE` olduğu için wiki ayrı ikincil çıktı olmalıdır.

Önerilen wiki topic:

```text
11_TRADER_WIKI/01_RISK_MANAGEMENT/TW_2026-05-03_RISK_MANAGEMENT_DEEPAK_UPPAL_SWING_TRADING.md
```

Wiki’ye alınacak dersler:

- Trade başına sabit hesap riski.
- Stop koymamanın performansı nasıl bozduğu.
- Market iyi değilken para kazanma baskısının zararı.
- Account balance yerine process/stocks odaklı düşünme.
- Concentration sadece doğru market ortamında anlamlıdır.
- Kaybeden trade’den çıkmak tekrar giriş hakkını yok etmez.

---

## 16. Repo Registry İçin Önerilen Kayıt Alanları

### `_registry/youtube_video_index.csv` önerisi

```csv
video_id,normalized_url,title,channel,status,codex_status,transcript_hash,candidate_id,first_seen_at,last_seen_at,process_count
q43pkYBo1hU,https://www.youtube.com/watch?v=q43pkYBo1hU,+259% in 1 Year - Swing Trading Performance Strategy,UNKNOWN_CHANNEL,CANDIDATE,READY_FOR_PYTHON_PROTOTYPE,2cdbb9e4f47bb5579a07686ba58ed8f1e45baa863969df4d5269db68c1ebaae3,YT_Q43PKYBO1HU_SWING_MOMENTUM_POST_EARNINGS_V1,2026-05-03,2026-05-03,1
```

### `channel_quality_registry.csv` önerisi

Kanal `UNKNOWN_CHANNEL` olduğu için kanal kalite registry’sine güçlü karar yazılmamalı. Eğer Codex gerçek kanal adını/ID’sini repo veya metadata’dan çıkarırsa şu şekilde işleyebilir:

```csv
channel_id,channel_name,total_processed,candidate_count,wiki_count,salvage_count,reject_count,stop_count,quality_state,last_updated
UNKNOWN,UNKNOWN_CHANNEL,1,1,0,0,0,0,UNKNOWN,2026-05-03
```

---

## 17. Codex Next Action

Codex’e verilecek uygulanabilir sonraki iş:

1. Repo’daki `_registry/youtube_video_index.csv` dosyasını oku.
2. `video_id=q43pkYBo1hU` veya aynı `transcript_hash` varsa duplicate formatında dur.
3. Duplicate değilse candidate klasörünü oluştur.
4. Bu intake raporunu candidate klasörüne kopyala.
5. `strategy_spec.yml` oluştur.
6. `data_requirements.md` oluştur.
7. `prototype_plan.md` oluştur.
8. İlk aşamada Pine dosyasına dokunma.
9. Production runner dosyalarına dokunma.
10. Backtest/optimization çalıştırma; sadece prototype plan ve veri gereksinimi hazırla.

---

## 18. Nihai Karar

```text
VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
PINE_NOW: NO
WIKI_ONLY: NO
OPTIONAL_WIKI: YES
DUPLICATE_STATUS: NOT_DUPLICATE_IN_CURRENT_SESSION__REPO_NOT_VERIFIED
CHANNEL_STATUS: UNKNOWN
```

Bu video, QuantLens/Research pipeline için güçlü bir adaydır. En uygun yön, doğrudan Pine’a geçmeden önce Python’da modüler prototype + event/fundamental veri gereksinimi + MTC_V2 risk/exit mapping çalışmasıdır.

---

## 19. Dosya Dokunma Özeti

Bu çalışma sırasında oluşturulan dosya:

```text
YT_q43pkYBo1hU_Intake_Report_2026-05-03.md
```

Bu çalışma sırasında dokunulmayan dosyalar:

```text
01_PINE/MTC_V2.pine
Production Python runner files
_registry/youtube_video_index.csv
channel_blacklist.yaml
channel_quality_registry.csv
```
