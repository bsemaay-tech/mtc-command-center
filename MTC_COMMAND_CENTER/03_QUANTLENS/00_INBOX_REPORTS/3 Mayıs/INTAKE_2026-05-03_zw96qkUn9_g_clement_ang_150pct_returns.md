# QuantLens Transcript Intake Report — How Clement Ang Achieved 150%+ Returns in the US Investing Championship

## 1. İşlem Sonucu

- **Verdict:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate ID:** `QL_20260503_ZW96QKUN9_G_CLEMENT_ANG_VCP_EP_RISK`
- **Ek Not:** Video yalnızca motivasyon/psikoloji içeriği değil; içinde kodlanabilir trade setup bileşenleri var. Ancak anlatım röportaj formatında olduğu için strateji doğrudan Pine'a geçirilmemeli; önce Python prototip + vaka inceleme yapılmalı.
- **İşlem tarihi:** 2026-05-03
- **Backtest / optimization çalıştırıldı mı?:** Hayır
- **MTC_V2 Pine dosyası değiştirildi mi?:** Hayır
- **Production Python runner değiştirildi mi?:** Hayır

---

## 2. Kaynak Metadata

| Alan | Değer |
|---|---|
| Source URL | `https://www.youtube.com/watch?v=zw96qkUn9_g` |
| Orijinal URL | `https://youtu.be/zw96qkUn9_g?si=lYvUhy_G4u0p8zkl` |
| Video ID | `zw96qkUn9_g` |
| Başlık | `How Clement Ang Achieved 150%+ Returns in the US Investing Championship` |
| Kanal | `Trader Lion / TraderLine Podcast (transcript içinde geçiyor; kanal id doğrulanmadı)` |
| Süre | `3:26:49` |
| Transcript dosyası | `How Clement Ang Achieved 150%+ Returns in the US Investing Championship.md` |
| Transcript hash | `4fd739619270e62b7c2edf7a91fff3e0d2301253972ecc3ffe2f214dc587b38f` |
| Kısa hash | `4fd739619270` |

---

## 3. URL Normalize / Duplicate / Channel Kontrolü

### 3.1 URL Normalize

- Tracking parametresi `si=...` yok sayıldı.
- Normalize URL üretildi:

```text
https://www.youtube.com/watch?v=zw96qkUn9_g
```

### 3.2 Duplicate Kontrol Durumu

Bu ChatGPT oturumunda repo registry dosyaları (`_registry/youtube_video_index.csv`, `channel_blacklist.yaml`, `channel_quality_registry.csv`) verilmediği için gerçek repo-level duplicate kontrolü yapılamadı.

Bu raporda yapılan lokal kontrol:

- Aynı `video_id` için mevcut indirilebilir intake raporu bulunmadı.
- Aynı transcript hash için mevcut lokal kayıt bulunmadı.
- Bu nedenle işlem **duplicate olarak durdurulmadı**.

Repo içinde çalışacak Codex için zorunlu kontrol:

1. `_registry/youtube_video_index.csv` içinde `video_id = zw96qkUn9_g` aranmalı.
2. `video_id` yoksa `transcript_hash = 4fd739619270e62b7c2edf7a91fff3e0d2301253972ecc3ffe2f214dc587b38f` aranmalı.
3. Aynı kanal + benzer başlık + benzer transcript varsa `POSSIBLE_DUPLICATE` veya `MANUAL_REVIEW` yapılmalı.

### 3.3 Kanal Kalite Kontrolü

- Kanal transcript içinde Trader Lion / TraderLine bağlamında geçiyor.
- Kanal ID yok.
- `channel_blacklist.yaml` verilmedi.
- Bu nedenle blacklist kararı verilmedi.
- Tek video üzerinden kanal blacklist'e alınmamalı.

**Önerilen channel state:** `UNKNOWN`

---

## 4. Sınıflandırma Kararı

### Karar

Bu video `CANDIDATE` olarak sınıflandırıldı.

### Gerekçe

Videoda doğrudan kodlanabilir birden fazla setup bileşeni var:

- Long tarafında volatility contraction / VCP / base breakout
- 10 EMA / 20 EMA / 50 SMA / 200 SMA bağlamı
- Volume dry-up ve breakout volume confirmation
- Relative strength / indexe göre dirençli kalma
- Episodic Pivot / news gap / opening range high fikirleri
- Short tarafında late-stage failed base, MA rejection, VWAP altı yaşama, 6/20 MACD momentum teyidi
- Risk per trade, günlük execution limiti, kayıplı dönemlerde size azaltma
- Kısmi satış, break-even stop, ATR extension bazlı profit taking

### Neden `WIKI_ONLY` Değil?

Risk yönetimi, psikoloji ve post-trade review kısımları güçlü bir Trader Wiki notu üretmeye uygundur. Ancak video yalnızca genel dersler içermiyor; mekanik strateji prototipine çevrilebilecek setup parametreleri de içeriyor. Bu yüzden ana sınıf `CANDIDATE`, yan çıktı olarak `Trader Wiki` notu önerilir.

---

## 5. Strateji Aday Özeti

## 5.1 Ana Fikir

Clement Ang'ın röportajda anlattığı süreç; güçlü piyasa rejiminde, güçlü tema / lider hisselerde, volatilite daralması sonrası volume destekli breakout yakalamaya; zayıf piyasa rejiminde ise eski liderlerde MA rejection / failed base short setup'larına odaklanıyor.

Bu yaklaşım tamamen tek bir indikatör stratejisi değil; daha çok şu birleşimdir:

```text
Market Regime + Relative Strength + Volatility Contraction + Volume Confirmation + Tight Risk + Progressive Sizing
```

---

## 5.2 Candidate Setup A — Long VCP / Wedge-Pop / Base Breakout

### Tez

Güçlü hisseler, büyük hareketten sonra düşük hacimli daralan konsolidasyon yapar. Arz azalır; talep geldiğinde breakout hacimle teyitlenirse fiyat hızlı devam edebilir.

### Kodlanabilir Gözlemler

| Bileşen | Mekanikleştirme Fikri |
|---|---|
| Market regime | SPY/QQQ close > 20/50 SMA veya index trend skoru pozitif |
| Trend filter | Hisse close > 50 SMA ve tercihen > 200 SMA |
| Kısa MA yapısı | Close > 10 EMA / 20 EMA veya bu ortalamalara checkback sonrası tekrar güçlenme |
| Volatility contraction | ATR%, true range veya high-low range son N barda daralıyor |
| Volume dry-up | Konsolidasyonda volume < SMA(volume, 20) |
| Pivot | Son N barın local high / consolidation high seviyesi |
| Breakout | Close > pivot veya intraday ORH kırılımı |
| Volume confirmation | Breakout volume > 1.5x / 2.0x volume SMA20 |
| Extension guard | Entry öncesi fiyatın 50 SMA'dan uzaklığı örn. `< 4 ATR` |
| Stop | LOD, setup low, 10/20 EMA altı veya pivot failure |
| Partial exit | İlk 1/3 yaklaşık +2R; sonraki 1/3 8-10 ATR from 50 SMA; kalan pozisyon weakness/trailing |

### İlk Python Prototip Parametreleri

```yaml
producer: long_vcp_breakout_v1
timeframe: daily
market_filter:
  benchmark: QQQ
  close_above_sma50: true
  sma20_slope_positive: true
trend_filter:
  close_above_sma50: true
  close_above_sma200: true
  ema10_above_ema20_optional: true
contraction:
  lookback: 15
  atr_pct_decline_required: true
  volume_dry_up_required: true
pivot:
  lookback: 10
entry:
  close_breaks_pivot: true
  volume_multiple_min: 1.5
risk:
  default_risk_pct: 0.003
  max_risk_pct_hot: 0.005
  initial_stop: setup_low_or_low_of_day
exit:
  partial_1_r_multiple: 2.0
  move_stop_to_breakeven_after_partial: true
  partial_2_atr_from_sma50: 8
  final_exit: weakness_or_trailing_stop
```

### MTC_V2 Bağlantısı

MTC_V2 tarafında doğrudan Pine'a geçmeden önce şu modüllerle uyumlandırılabilir:

- **Signal Producer:** `long_vcp_breakout_v1`
- **Entry Gates:** MA, MA slope, HTF trend, Volume, ATR Vol Floor, Momentum, Level Proximity
- **Position Sizing:** risk_pct temelli sizing, SL mesafesine göre pozisyon
- **Position Manager:** cooldown, max entries, no-trade after losing streak guard
- **Exit Rules:** Initial SL, BE, ATR/R multiple TP, trailing, time stop
- **Parity Notu:** Intraday ORH kullanılacaksa Python tarafında intraday veri gerekir. İlk prototip daily-only yapılırsa ORH yerine `close > pivot` kullanılmalı.

---

## 5.3 Candidate Setup B — Episodic Pivot / News Gap / Opening Range

### Tez

Güçlü haber/katalizörle gap-up yapan ve yüksek volume alan hisselerde, opening range high kırılımı ve VWAP üstünde kalma kısa vadeli momentum fırsatı verebilir.

### Kodlanabilir Gözlemler

| Bileşen | Mekanikleştirme Fikri |
|---|---|
| Gap | Open > previous close + X% |
| Catalyst proxy | Gap + unusual volume; haber datası yoksa sadece price/volume proxy |
| Opening range | İlk 1 / 5 / 15 dakika high seviyesi |
| Intraday trend | Price > VWAP |
| Momentum | 6/20 MACD cross veya intraday momentum positive |
| Stop | Opening range low veya LOD |
| Exit | R multiple, ATR extension, VWAP loss, end-of-day veya weakness |

### İlk Prototip Notu

Bu setup daily veriyle eksik kalır. Gerçek test için en az 5m intraday veri gerekir. MTC_V2 parity açısından intrabar ordering kritik olacağı için başlangıçta ayrı feature oracle olarak tutulmalı.

---

## 5.4 Candidate Setup C — Short Late-Stage Failed Base / MA Rejection

### Tez

Piyasa negatife döndüğünde eski lider hisseler doğal short adaylarına dönüşür. Hisse 20 EMA / 50 SMA gibi kritik ortalamaları ihlal ettikten sonra düşük hacimli rally ile bu ortalamalara yaklaşır; intraday reversal ve VWAP altı yaşamaya başlarsa short fırsatı oluşur.

### Kodlanabilir Gözlemler

| Bileşen | Mekanikleştirme Fikri |
|---|---|
| Market regime | QQQ/SPY trend negatif veya index 20/50 altı |
| Former leader universe | Son 3-12 ayda yüksek RS / yüksek momentum gösteren hisseler |
| Breakdown | Close < 20 EMA veya 50 SMA |
| Rally into resistance | Price düşük hacimle 20 EMA / 50 SMA / 200 SMA bölgesine yaklaşır |
| Intraday reversal | Price VWAP altına iner ve orada yaşar |
| Momentum confirmation | 6/20 MACD below zero veya bearish cross |
| Entry | VWAP kırılımı / prior intraday low kırılımı |
| Stop | HOD veya resistance üstü |
| Cover | Prior low, undercut & rally, 50 SMA / 200 SMA yakınlığı, R multiple |

### Risk Notu

Short setup'lar gap, borrow, squeeze ve haber riskine çok açık. Bu yüzden ilk prototipte:

- Lower risk_pct
- Max daily aggregate risk
- No overnight short opsiyonu
- Gap-risk penalty
- Borrow/slippage placeholder

kullanılmalı.

---

## 5.5 Candidate Setup D — Index Undercut & Rally Sonrası Relative Strength Rotation

### Tez

Index önceki dipleri undercut edip rally yaptığında, düşüşte en az zarar gören ve moving average'larda higher low yapan sektör/hisseler yeni lider olabilir. Piyasa baskısı kalktığında en hızlı hareket edenler genellikle bu dirençli hisselerdir.

### Kodlanabilir Gözlemler

| Bileşen | Mekanikleştirme Fikri |
|---|---|
| Index event | QQQ/SPY previous swing low undercut + close back above |
| RS filter | Hisse drawdown < index drawdown veya RS line rising |
| Structure | Higher low, MA support, overhead resistance az |
| Entry | 20 EMA undercut & rally, pivot break, pullback buy |
| Stop | U&R low veya setup low |
| Exit | R multiple / ATR extension / MA loss |

---

## 6. Risk Yönetimi ve Position Sizing Dersleri

Videodaki en güçlü bölüm risk yönetimidir. Strateji tarafında şu guard'lar özellikle değerli:

### 6.1 Progressive Exposure

- Kötü / bulanık markette risk azalt.
- Son 5-10 trade kötü gidiyorsa size düşür.
- İyi trade serisi ve equity cushion oluşmadan agresifleşme.
- Büyük getiri hedefinden önce sermayeyi koru.

### 6.2 Önerilen Risk Parametreleri

| Durum | Önerilen Risk |
|---|---:|
| Default prototip | 0.30% equity risk / trade |
| İyi rejim + iyi son trade serisi | 0.50% |
| Çok güçlü setup / hot streak | 0.75% maksimum araştırma modu |
| Murky market | 0.10% - 0.25% |
| Günlük toplam açık risk | 1.00% cap |
| Günlük execution limiti | 3 pozisyon / gün, piyasa net değilse |

### 6.3 MTC_V2 Guard Önerileri

```yaml
guards:
  losing_streak_guard:
    enabled: true
    lookback_trades: 5
    reduce_risk_after_losses: 3
  daily_execution_cap:
    enabled: true
    max_new_positions_per_day: 3
  daily_risk_cap:
    enabled: true
    max_total_new_risk_pct: 0.01
  market_murkiness_guard:
    enabled: research
    conditions:
      - benchmark_chop_high
      - benchmark_below_sma20
      - low_setup_count
```

---

## 7. Exit / Sell Rules Intake

### Videodan Çıkan Sell Mantığı

- İlk hedef: yaklaşık +2R veya riskin 2 katı kârda pozisyonun bir kısmını sat.
- İlk partial sonrası stop'u break-even'a çek.
- İkinci partial: fiyat 50 SMA'dan 8-10 ATR uzaklaştığında satış düşün.
- Son parça: güce satmak yerine zayıflığa / trailing weakness'a bırakılmalı.
- Loser'lar kısa tutulmalı; röportajda ortalama loser süresinin 1 günden az olduğu vurgulanıyor.
- Winner'lar daha uzun tutulmalı; ortalama winner süresi yaklaşık birkaç gün.

### MTC_V2 Exit Entegrasyonu

| Exit Modülü | Kullanım |
|---|---|
| Initial SL | setup low / LOD / swing low |
| Break-even | partial sonrası aktif |
| TP Multi | R multiple ve ATR extension |
| Trailing | son 1/3 için |
| Time stop | breakout sonrası ilerleme yoksa |
| Opp signal | ters sinyalde çıkış |
| Filter block exit | piyasa rejimi bozulursa opsiyonel |

---

## 8. Trader Wiki Notu

Bu video ayrıca Trader Wiki için yüksek değerli bir kaynak.

### Önerilen Wiki Sınıfları

- `01_RISK_MANAGEMENT`
- `02_TRADING_PSYCHOLOGY`
- `04_SYSTEM_DEVELOPMENT`
- `05_BACKTESTING_AND_OPTIMIZATION`

### Wiki ID Önerisi

```text
TW_2026-05-03_01_RISK_MANAGEMENT_clement_ang_150pct_returns
```

### Kısa Özet

Clement Ang'ın ana dersi; büyük getiriyi doğrudan kovalamak yerine önce sermayeyi korumak, sonra tutarlı kârlılık, en son üstün getiri hedeflemektir. Büyük drawdown sonrası sistemi yazılı kurallara bağlamış, model book çalışması yapmış, post-trade review ile hataları sınıflandırmış ve riskini piyasa koşullarına göre düşürmüştür.

### Ana Dersler

- Sermaye korunmadan edge kullanılamaz.
- Büyük bull market kazancı trader yetkinliğiyle karıştırılmamalı.
- Averaging down ve stopsuz işlem büyük risk.
- Kayıplı dönemde size azaltmak, strateji değiştirmekten daha önce gelir.
- Setup olmayan trade'leri filtrelemek kârlılığı ciddi şekilde artırabilir.
- Winner/loser analizi aylık yapılmalı; yıl sonuna bırakılmamalı.
- Market regime kötü olduğunda long-only trader'ın görevi trade sayısını azaltmak olabilir.
- Relative strength, güçlü setup'ların erken ipucudur.
- 30-40% win rate ile yüksek getiri mümkündür; ama average win / average loss asimetrisi şarttır.

### MTC_V2 / Algo Trading İçin Bağlantı

- Risk guard'ları strateji sinyalinden bağımsız ve merkezi olmalı.
- Signal producer iyi olsa bile market regime + execution cap + losing streak guard gerekir.
- Post-trade review çıktıları otomatik etiketlere dönüştürülebilir: `NO_SETUP`, `FOMO`, `RETRY_TOO_MANY`, `OVERSIZED`, `MARKET_MURKY`, `GOOD_RS`, `GOOD_VOLUME_CONFIRMATION`.
- Parity-first yaklaşımda discretionary anlatımlar önce feature contract / Python prototype / trace export seviyesine indirgenmeli.

---

## 9. Riskli veya Şüpheli İddialar

| İddia / Alan | Risk |
|---|---|
| 150%+ performans | Transcript içindeki self-reported bilgi; bağımsız doğrulama yapılmadı. |
| Röportaj formatı | Kurallar tamamen mekanik değil; discretionary yorum çok fazla. |
| EP / gap setup | Haber ve premarket etkisi nedeniyle daily-only backtest yanıltıcı olabilir. |
| Short setup | Borrow, gap, squeeze, SSR, slippage gibi gerçek piyasa maliyetleri eklenmezse sonuçlar abartılı çıkabilir. |
| ATR extension exit | Strong trendlerde erken satışa; mean reversion dönemlerinde iyi korumaya sebep olabilir. Parametre hassasiyeti test edilmeli. |
| Winner örnekleri | Survivorship bias riski var; sadece başarılı örneklerden rule çıkarılmamalı. |
| 2025 piyasa koşulları | Belirli dönemlerin hot-theme ortamı genel rejime taşınmamalı. |

---

## 10. Python Prototype Planı

### Faz 1 — Daily Long VCP Prototype

Amaç: Intraday gerektirmeyen en sade ve parity-safe long setup'ı test etmek.

```yaml
prototype_name: long_vcp_breakout_daily_v1
data:
  timeframe: 1D
  universe: liquid_us_equities
  benchmark: QQQ
entry_logic:
  - benchmark_close_above_sma50
  - stock_close_above_sma50
  - stock_close_above_sma200
  - distance_from_sma50_atr < 4
  - volume_dry_up_in_base
  - range_contraction_in_base
  - close_breaks_pivot
  - breakout_volume_multiple >= 1.5
risk:
  initial_stop: min(setup_low, recent_swing_low)
  risk_pct: 0.003
exits:
  - partial_at_2R
  - breakeven_after_partial
  - partial_when_distance_from_sma50_atr >= 8
  - trailing_stop_for_runner
```

### Faz 2 — Relative Strength Rotation

```yaml
prototype_name: index_ur_rs_rotation_v1
data:
  timeframe: 1D
  benchmark: QQQ
entry_logic:
  - benchmark_undercut_and_rally
  - stock_rs_line_rising
  - stock_drawdown_less_than_benchmark
  - stock_higher_low_near_ma
  - pivot_or_20ema_ur_entry
risk:
  stop: ur_low_or_setup_low
```

### Faz 3 — Intraday EP / ORH

```yaml
prototype_name: episodic_pivot_orh_5m_v1
data:
  timeframe: 5m
  daily_context_required: true
entry_logic:
  - daily_gap_up_pct >= threshold
  - opening_range_high_break
  - price_above_vwap
  - volume_spike
  - optional_macd_6_20_positive
risk:
  stop: opening_range_low_or_lod
```

### Faz 4 — Short MA Rejection

```yaml
prototype_name: short_failed_base_ma_rejection_v1
data:
  timeframe: 5m_with_daily_context
entry_logic:
  - benchmark_weak
  - former_leader_filter
  - stock_below_20ema_or_50sma
  - low_volume_rally_into_ma
  - intraday_vwap_rejection
  - macd_6_20_bearish
risk:
  stop: high_of_day
  max_overnight_short: false
```

---

## 11. Önerilen Feature Contract Dosyaları

Repo içinde Pine'a geçmeden önce şu draft contract'lar oluşturulabilir:

```text
06_QUANTLENS_LAB/feature_contracts/drafts/long_vcp_breakout_daily_v1.yml
06_QUANTLENS_LAB/feature_contracts/drafts/index_ur_rs_rotation_v1.yml
06_QUANTLENS_LAB/feature_contracts/drafts/episodic_pivot_orh_5m_v1.yml
06_QUANTLENS_LAB/feature_contracts/drafts/short_failed_base_ma_rejection_v1.yml
```

---

## 12. Registry Satır Önerileri

Gerçek repo registry dosyaları bu oturumda mevcut olmadığı için aşağıdakiler sadece öneridir; otomatik yazılmadı.

### `_registry/youtube_video_index.csv`

```csv
processed_at,video_id,normalized_url,title,channel,transcript_hash,status,candidate_id,report_path,process_count,duplicate_of
2026-05-03,zw96qkUn9_g,https://www.youtube.com/watch?v=zw96qkUn9_g,"How Clement Ang Achieved 150%+ Returns in the US Investing Championship","Trader Lion / TraderLine Podcast (transcript içinde geçiyor; kanal id doğrulanmadı)",4fd739619270e62b7c2edf7a91fff3e0d2301253972ecc3ffe2f214dc587b38f,CANDIDATE,QL_20260503_ZW96QKUN9_G_CLEMENT_ANG_VCP_EP_RISK,06_QUANTLENS_LAB/YOUTUBE_STRATEGY_INTAKE/reports/INTAKE_2026-05-03_zw96qkUn9_g_clement_ang_150pct_returns.md,1,
```

### `channel_quality_registry.csv`

```csv
channel,quality_state,processed_count,candidate_count,wiki_count,reject_count,stop_count,last_processed_at,notes
"Trader Lion / TraderLine Podcast",UNKNOWN,1,1,0,0,0,2026-05-03,"Channel ID yok; blacklist kararı verilmedi."
```

---

## 13. Dosya Etki Raporu

### Oluşturulması Önerilen Dosyalar

```text
06_QUANTLENS_LAB/YOUTUBE_STRATEGY_INTAKE/reports/INTAKE_2026-05-03_zw96qkUn9_g_clement_ang_150pct_returns.md
06_QUANTLENS_LAB/feature_contracts/drafts/long_vcp_breakout_daily_v1.yml
06_QUANTLENS_LAB/feature_contracts/drafts/index_ur_rs_rotation_v1.yml
06_QUANTLENS_LAB/feature_contracts/drafts/episodic_pivot_orh_5m_v1.yml
06_QUANTLENS_LAB/feature_contracts/drafts/short_failed_base_ma_rejection_v1.yml
11_TRADER_WIKI/01_RISK_MANAGEMENT/TW_2026-05-03_01_RISK_MANAGEMENT_clement_ang_150pct_returns.md
```

### Dokunulmaması Gereken Dosyalar

```text
01_PINE/MTC_V2.pine
Production Python runner dosyaları
Mevcut optimization result klasörleri
Mevcut large CSV / data bundle / cache dosyaları
Broker / exchange / webhook secret dosyaları
```

---

## 14. Codex İçin Net Next Action

1. Repo registry dosyalarında duplicate kontrolü yap.
2. Duplicate değilse bu videoyu `CANDIDATE` olarak indexle.
3. Pine'a geçme.
4. İlk olarak `long_vcp_breakout_daily_v1` Python prototipini üret.
5. MTC_V2 risk / SL / TP / BE / trailing yapılarını referans al, ama production runner'ı değiştirme.
6. Daily prototype sonrası yalnızca rapor üret; optimization çalıştırma.
7. EP ve short setup'ları intraday veri gerektirdiği için ayrı feature contract olarak beklet.
8. Final raporda özellikle şunları göster:
   - Hangi kurallar mekanikleşti?
   - Hangi kurallar discretionary kaldı?
   - Hangi MTC_V2 modülleriyle eşleşti?
   - Hangi dosyalara dokunulmadı?
   - Sonraki karar: Python prototype devam mı, reject mi, wiki-only mi?

---

## 15. Nihai Karar

```text
VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
PRIMARY_SETUP: long_vcp_breakout_daily_v1
SECONDARY_SETUPS: episodic_pivot_orh_5m_v1, short_failed_base_ma_rejection_v1, index_ur_rs_rotation_v1
WIKI_VALUE: HIGH
MTC_V2_CHANGE_ALLOWED_NOW: NO
PINE_CONVERSION_ALLOWED_NOW: NO
BACKTEST_ALLOWED_NOW: NO
```
