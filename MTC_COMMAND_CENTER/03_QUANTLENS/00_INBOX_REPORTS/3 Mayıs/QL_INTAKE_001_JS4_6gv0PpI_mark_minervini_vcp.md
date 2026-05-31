# QuantLens Transcript Intake Report — JS4_6gv0PpI

## 1. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate Type:** `LONG_BREAKOUT_VCP_PROGRESSIVE_EXPOSURE`
- **Confidence:** `MEDIUM-HIGH`
- **Reason:** Transcript içinde kodlanabilir bir trade fikri var: VCP / cup-with-handle / cheat pivot yapısı, sıkışma ve hacim daralması, breakout, sıkı stop, kademeli pozisyon büyütme, güce satışla riski finanse etme ve piyasa/traction filtresi. Parametrelerin tamamı net verilmediği için doğrudan Pine'a geçilmemeli; önce Python prototip + görsel olay etiketleme yapılmalı.
- **Trader Wiki Değeri:** `YES` — ayrıca risk yönetimi, post-trade analysis, mindset ve process disiplini için wiki notu çıkarılabilir.

## 2. Metadata

- **Source File:** `33,500% RETURN - Mark Minervini's VCP Setup that made him Millions.md`
- **Original URL:** `https://youtu.be/JS4_6gv0PpI?si=GdGc-i9bA1G9F8BS`
- **Normalized URL:** `https://www.youtube.com/watch?v=JS4_6gv0PpI`
- **Video ID:** `JS4_6gv0PpI`
- **Title:** `33,500% RETURN - Mark Minervini's VCP Setup that made him Millions`
- **Channel:** `UNKNOWN_CHANNEL`
- **Channel Quality State:** `UNKNOWN`
- **Processed Date:** `2026-05-03`
- **Transcript Hash SHA256:** `2040f8f4de140606ae8d2c51ac57eef231cf2fcae4e8ab8959f6a73e62586b2a`
- **Normalized Transcript Word Count:** `25045`

## 3. Duplicate / Registry Check

- **Duplicate by video_id:** `NOT_CONFIRMED`
- **Duplicate by transcript_hash:** `NOT_CONFIRMED`
- **Reason:** Bu çalışmada `_registry/youtube_video_index.csv`, `channel_blacklist.yaml` veya `channel_quality_registry.csv` dosyaları verilmedi. Bu nedenle gerçek repo registry kontrolü yapılamadı.
- **Action:** Repo içinde bu intake işlenmeden önce Codex şu kontrolü yapmalı:
  1. `_registry/youtube_video_index.csv` içinde `video_id = JS4_6gv0PpI` ara.
  2. Yoksa `transcript_hash = 2040f8f4de140606ae8d2c51ac57eef231cf2fcae4e8ab8959f6a73e62586b2a` ara.
  3. Aynı kanal + aynı başlık + benzer transcript varsa `POSSIBLE_DUPLICATE` olarak durdur.

## 4. Channel Quality Decision

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist Decision:** `NO_BLACKLIST_DECISION`
- **Reason:** Kanal adı / kanal id transcript içinde güvenilir biçimde verilmedi. Kural gereği kanal bilgisi yoksa blacklist kararı verilmemeli.
- **Suggested Registry Update:** Eğer video yeni ise `youtube_video_index.csv` içine `status = CANDIDATE`; `channel_quality_registry.csv` için kanal bilinmediğinden `UNKNOWN_CHANNEL` altında yalnızca geçici kayıt önerilir.

## 5. İçerik Özeti

Video; Mark Minervini, Mark Ritchie II ve Brandon Hedgepath çevresinde yapılan uzun bir trader söyleşisi. Ana tema; Minervini tarzı büyüme hissesi / momentum breakout trading. İçerik, tek bir mekanik sistemden ziyade şu bileşenleri bir araya getiriyor:

- Güçlü earnings / revenue growth veya güçlü tema / sektör ivmesi olan enstrümanları tercih etmek.
- Cup-with-handle, VCP, cheat pivot ve low-cheat gibi sıkışma tabanlı giriş bölgelerini takip etmek.
- Breakout'ların her dönem çalışmadığını kabul edip sadece setup + market traction beraber olduğunda agresifleşmek.
- Büyük kayıpları kesin şekilde engellemek; stop disiplinini sistemin omurgası yapmak.
- Güçlü hareketlerde kısmi satışla riski finanse edip kalan pozisyonu asimetrik kazanç için taşımak.
- İşlem sonrası analizle ortalama kazanç, ortalama kayıp, win rate, R-multiple ve hata tekrarlarını ölçmek.

## 6. Strateji Adayı — Mekanik Çekirdek

### 6.1 Producer Önerisi

- **Producer Name:** `producer_vcp_pivot_breakout_v1`
- **Direction:** Long-only başlangıç önerilir.
- **Market:** İlk test için hisse senedi datası daha uygun; crypto için fundamental growth filtresi yerine RS / trend / hacim / tema proxy kullanılmalı.
- **Timeframe:** Daily ana hedef; daha sonra 4H / 1H adaptasyonu denenebilir.

### 6.2 Setup Tanımı

Kodlanabilir setup aşağıdaki yapıdan çıkarılabilir:

1. **Prior Trend / Leadership:** Enstrüman önce güçlü bir trend veya güçlü RS göstermiş olmalı.
2. **Base Formation:** Fiyat bir base / cup / handle / VCP benzeri yapı içinde konsolide olmalı.
3. **Volatility Contraction:** Ardışık swing genişlikleri daralmalı.
4. **Tightness:** Son pivot alanında fiyat dar bantta kalmalı ve kazançlarını korumalı.
5. **Volume Contraction:** Pivot sırasında hacim azalmalı; breakout sırasında hacim artışı aranmalı.
6. **Pivot Level:** Son sıkışma yüksek seviyesi veya handle/cheat pivot seviyesi breakout eşiği olmalı.
7. **Breakout Entry:** Fiyat pivot üstüne çıkınca giriş sinyali üretmeli; parity için bar kapanışı onayı kullanılmalı.

### 6.3 Pivot Tipleri

| Pivot Tipi | Transcript Yorumu | Kodlama Önceliği |
|---|---|---:|
| `LOW_CHEAT` | Base'in alt üçte birlik kısmındaki erken giriş; overhead supply riski yüksek. | Düşük / ileri seviye |
| `CHEAT` | Base'in orta kısmında handle/pivot benzeri erken giriş. | Orta |
| `HANDLE_TOP_PIVOT` | Eski zirvelere yakın klasik handle / breakout. | Yüksek |
| `VCP_TIGHT_PIVOT` | Daralan fiyat ve hacimle oluşan sıkı pivot. | En yüksek |

## 7. Giriş Kuralları — Python Prototip Taslağı

```text
candidate_long =
    trend_ok
    AND base_ok
    AND contraction_ok
    AND tight_pivot_ok
    AND volume_contracting_before_breakout
    AND breakout_above_pivot
    AND market_regime_ok
    AND traction_ok
```

Önerilen ilk parametre alanları:

```yaml
producer_vcp_pivot_breakout_v1:
  side: long_only
  base_lookback_min: 30
  base_lookback_max: 180
  contraction_swings_min: 2
  contraction_ratio_required: true
  tight_pivot_lookback: 5-15
  max_pivot_range_pct: parameterize
  breakout_buffer_pct: parameterize
  volume_contraction_lookback: 10-30
  breakout_volume_multiple: parameterize
  require_close_confirmation: true
```

## 8. Risk / Exit / Position Management

### 8.1 Initial Stop

- Transcriptte ortalama stopun iyi piyasada yaklaşık `3% - 4%`; zayıf piyasada `5% - 6%`; maksimum çizginin yaklaşık `8%`; bazı durumlarda staggered stop ile `4% / 10%` benzeri yapı kullanıldığı anlatılıyor.
- Python prototipte ilk etapta:
  - `initial_sl_pct = 5%` default,
  - `hard_max_sl_pct = 8%`,
  - `expert / volatile asset mode` için `10%` maksimum test parametresi kullanılabilir.

### 8.2 Reward / Risk

- Minimum hedef: ortalama kazanç / ortalama kayıp oranı en az `2:1`.
- Daha iyi trade'lerde `3R - 5R`; nadiren daha yüksek R hedeflenebilir.
- Backtest raporunda mutlaka `avg_gain`, `avg_loss`, `win_rate`, `expectancy`, `profit_factor`, `max_drawdown`, `R_multiple_distribution` olmalı.

### 8.3 Partial Exit / Risk Financing

İlk test için iki farklı exit modu denenebilir:

```yaml
exit_model_A_simple:
  tp1_R: 2.0
  tp1_qty_pct: 50
  move_stop_to_breakeven_after_tp1: true
  runner_exit: trailing_or_ma_violation

exit_model_B_strength_reduction:
  reduce_into_strength_pct: parameterize
  finance_risk_when_unrealized_gain_ge_initial_risk: true
  runner_qty_pct: 10-50
  runner_exit: 50ma_or_trailing_stop_or_price_violation
```

### 8.4 Re-entry

Transcriptte stop sonrası setup bozulmadıysa tekrar hızlı giriş fikri var. MTC_V2 için bu konu dikkatli ele alınmalı:

- Aynı bar re-entry kapalı başlasın.
- Re-entry yalnızca yeni bar + pivot tekrar kırılımı + setup hâlâ geçerliyse olsun.
- `closed_this_bar_reason` ve `block_new_entries_this_bar` kuralları korunmalı.

## 9. Market Regime / Progressive Exposure

Progressive exposure için mekanik öneri:

```text
exposure_level = f(
    market_trend_score,
    breakout_success_rate_recent,
    own_trade_traction,
    number_of_valid_setups,
    drawdown_state
)
```

İlk Python prototipte basit skor:

```yaml
market_regime:
  index_above_ma50: true
  index_above_ma200: true
  rs_leadership_filter: optional
  recent_breakout_success_window: 20-50 trades/signals
  min_success_rate_to_scale_up: parameterize

portfolio_guard:
  reduce_risk_after_N_losses: true
  increase_risk_only_after_realized_profit_or_open_trade_cushion: true
  no_scale_up_while_equity_drawdown: true
```

## 10. MTC_V2 ile Bağlantı

Bu video MTC_V2'nin mevcut modülleriyle iyi eşleşiyor:

| MTC_V2 Katmanı | Kullanım |
|---|---|
| Signal Producer | Yeni `producer_vcp_pivot_breakout_v1` üretilebilir. |
| Signal Transform | Confirmation / level retest opsiyonel denenebilir. |
| Entry Gates | HTF Trend, MA/McGinley, Volume, ADX/Chop, ATR Vol Floor, Momentum, Level Proximity. |
| Position Manager | Long-only, cooldown, max entries, progressive exposure guard. |
| Position Sizing | Risk % ve hard max stop üzerinden position sizing. |
| Exit Rules | Initial SL, TP1 partial, BE, trailing, MA violation, time stop. |
| PortfolioState Guards | Son trade traction, drawdown guard, loss streak guard. |

**Önemli:** İlk etapta Pine'a geçilmemeli. Önce Python tarafında event label + chart review + küçük dataset prototipi yapılmalı.

## 11. Backtest / Prototype Planı

### Phase 1 — Event Labeling

- Daily OHLCV datası üzerinde VCP / pivot / breakout event label oluştur.
- Her sinyal için aşağıdaki debug alanları export edilsin:
  - `base_start`, `base_end`
  - `pivot_type`
  - `pivot_price`
  - `base_depth_pct`
  - `contraction_count`
  - `last_pivot_range_pct`
  - `volume_contraction_score`
  - `breakout_volume_ratio`
  - `market_regime_score`
  - `traction_score`

### Phase 2 — Visual Review

- 50-100 sinyali chart üzerinde manuel incele.
- Low-cheat / cheat / top-handle pivot sınıfları ayrı ayrı değerlendirilsin.
- False positive nedenleri sınıflandırılsın: sloppy base, wide/loose pivot, no volume contraction, overhead supply, weak market, late-stage extension.

### Phase 3 — Backtest

- Önce tek enstrüman değil; geniş growth-stock evreni veya en az çoklu sembol kullanılsın.
- Walk-forward / cross-market validation öncesi minimal parameter sweep yeterli.
- Crypto adaptasyonu ancak VCP producer stabil olduktan sonra denenmeli.

## 12. Riskli / Şüpheli İddialar

- Video başlığındaki yüksek getiri ifadesi doğrudan strateji performansı olarak alınmamalı; survivor bias ve kişisel trader skill etkisi yüksek olabilir.
- VCP ve breakout anlatımı değerli; fakat transcriptte net matematiksel parametreler yok. Parametreleri Codex'in kendisi uydurmamalı; parametre aralıkları ayrı test edilmeli.
- Low-cheat / expert buy konsepti yüksek öznellik içeriyor. İlk prototipte top pivot / tight VCP daha güvenli.
- “Breakout çalışır / çalışmaz” dönemleri regime bağımlı; tek market döneminde optimize edilirse overfit riski yüksek.
- Fundamental revenue/earnings filtresi crypto için doğrudan kullanılamaz.

## 13. Final Dosya / Registry Önerileri

Gerçek repo çalışmasında önerilen kayıtlar:

```text
_registry/youtube_video_index.csv
  video_id: JS4_6gv0PpI
  normalized_url: https://www.youtube.com/watch?v=JS4_6gv0PpI
  transcript_hash: 2040f8f4de140606ae8d2c51ac57eef231cf2fcae4e8ab8959f6a73e62586b2a
  status: CANDIDATE
  codex_status: READY_FOR_PYTHON_PROTOTYPE
  candidate_id: CAND_VCP_PIVOT_BREAKOUT_JS4_6gv0PpI
```

Önerilen candidate klasörü:

```text
YOUTUBE_STRATEGY_INTAKE/candidates/CAND_VCP_PIVOT_BREAKOUT_JS4_6gv0PpI/
  INTAKE_REPORT.md
  TRANSCRIPT_SOURCE.md
  PROTOTYPE_SPEC.md
```

Opsiyonel Trader Wiki notu:

```text
11_TRADER_WIKI/01_RISK_MANAGEMENT/TW_2026-05-03_RISK_MANAGEMENT_mark_minervini_vcp.md
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/TW_2026-05-03_SYSTEM_DEVELOPMENT_post_trade_analysis.md
```

## 14. Dokunulmaması Gerekenler

Bu intake raporu kapsamında aşağıdakilere dokunulmamalı:

- `01_PINE/MTC_V2.pine`
- Production Python runner dosyaları
- Optimization result klasörleri
- Büyük CSV / cache / data bundle dosyaları
- API key / webhook / exchange secret içeren herhangi bir dosya

## 15. Next Action

**Codex'e verilecek sonraki görev:**

```text
Bu videoyu CANDIDATE olarak işle. Önce registry duplicate kontrolü yap. Duplicate değilse CAND_VCP_PIVOT_BREAKOUT_JS4_6gv0PpI candidate klasörünü oluştur. Pine dosyasına dokunma. Backtest veya optimization çalıştırma. Sadece Python prototype spec, event schema ve debug export taslağı hazırla. Low-cheat/cheat/top-handle pivot tiplerini ayrı sınıflandır. İlk gerçek kodlamada top-handle/VCP tight pivotu önceliklendir; low-cheat'i ileri seviye opsiyon olarak bırak.
```

## 16. Kısa Karar

Bu video **reddedilmemeli**. En iyi kullanım şekli, doğrudan kârlı sistem varsaymak değil; `VCP tight pivot breakout + strict stop + progressive exposure + risk financing` şeklinde Python tarafında prototiplenebilir bir aday stratejiye dönüştürmektir.
