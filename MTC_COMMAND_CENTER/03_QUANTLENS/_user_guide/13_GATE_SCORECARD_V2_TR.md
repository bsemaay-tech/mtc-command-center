# Gate-Tabanlı Scorecard v2 — Kanonik Strateji Değerlendirme Sistemi

**Durum:** DRAFT (Phase 0A). Yazar: Claude Opus 4.8, 2026-06-04.
**Owner sign-off:** Barış 2026-06-04 — D1-D6 kararları onaylanmış.

**Kaynak Spesifikasyon:** `03_QUANTLENS/_user_guide/12_STRATEGY_EVALUATION_RUBRIC.md` (SP-004)

---

## Tasarım İlkeleri

1. **Ayrı gate'ler, asla tek bir sayı değil.** Dört puanlanmış gate + hard-fail bayrakları. Eski `build_scorecard()` flat 100 karışımı bu sistemle değiştiriliyor.
2. **Bir gate, faz verisi olana kadar N/A'dır.** Backtest artifact'i yoksa Gate 2 skoru yok; entegrasyon artifact'i yoksa Gate 3 skoru yok. UI "not evaluated" gösterir, asla sahte sayı göstermez.
3. **Her metrikte status envelope.** `{value, status, reason, source_path}` — sadece `status==OK` olan puanlanır. `N_A | NOT_COMPUTED | INSUFFICIENT_DATA | TOOL_FAILED` → otomatik sıfırlanmaz.
4. **Hard-fail gate'ler kill switch'tir.** `REJECT_REPAINT` her şeyi sıfırlar. `PBO≥0.5` → `OVERFIT_SUSPECT`, terfiyi engeller ama fikri korur. **Parity sadece danışma (advisory) niteliğindedir**, asla engel oluşturmaz.
5. **Her alt-kriter, üretilebilir bir alana eşlenir.** Runtime'da insan vibes'tan puanlama yapılmaz.

**Minimum geçiş notu: her gate 75/100.**

---

## Onaylanan Kararlar (D1-D6)

| # | Karar | Çözüm (Barış 2026-06-04) |
|---|---|---|
| D1 | Gate 1B scoring modu | **/100, PASS ≥75** — tüm gate'lerle uniform |
| D2 | PBO ≥0.5 politikası | Gate 2 `OVERFIT_SUSPECT`, terfiyi engeller, fikri korur |
| D3 | Parity | **Advisory, hard gate DEĞİL.** Mismatch → `PARITY_WARNING`; engellemez |
| D4 | Gate 3 kaynağı | Ayrı `production_readiness_artifact_v1`; var olana kadar N/A |
| D5 | Son sayısal bantlar | Phase 1.5'te gerçek veriden belirlenecek (şu anki değerler provizyon) |
| D6 | İngilizce thesis başlığı | AI taslağı oluşturur, Barış geçersiz kılabilir |

---

## Gate 1 — Candidate Intake (/100)

**Soru:** *Bu kodlamaya ve backtest'e değer mi?* Performans puanlanmaz (henüz backtest yok).

| # | Kategori | Puan |
|---|---|---:|
| 1.1 | Kural netliği & determinizm | 25 |
| 1.2 | Algoritmik kodlanabilirlik | 20 |
| 1.3 | Ön repaint / lookahead riski | 15 |
| 1.4 | Trade yaşam döngüsü tanımı | 15 |
| 1.5 | Veri & backtest fizibilitesi | 10 |
| 1.6 | Uygulama realizmi (ön) | 10 |
| 1.7 | Strateji kenar hipotezi | 5 |
| | **Toplam** | **100** |

### Alt-Kriter Detayları (Gate 1)

| Alt-kriter | Puan | Kaynak alan / kural |
|---|---:|---|
| 1.1 Entry kuralı açık | 6 | `producer_spec.entry_pseudo` non-empty & deterministik |
| 1.1 Exit yaklaşımı açık | 5 | `exit_pseudo` non-empty VEYA `mtc_exit_delegated=true` |
| 1.1 Long/short/flat tanımlı | 4 | `direction` + `strategy_type` set |
| 1.1 Same-bar collision kuralı | 4 | `opposite_signal_behavior` mevcut |
| 1.1 Parametreler açık | 3 | `rules_high_confidence` sayısal params listeler |
| 1.1 İnsan yorumlaması yok | 3 | `has_deterministic_rules=true` (audit) |
| 1.2 Pine/Python'da yazılabilir | 5 | `codable=true` / `manual_visual` flagli değil |
| 1.2 Manuel trendline/göz yok | 5 | Sınıflandırma `MANUAL_VISUAL_REVIEW_ONLY` değil |
| 1.2 Tüm girdiler numeric/boolean | 4 | `rules_high_confidence` türlerinden |
| 1.2 State machine olarak modellenebilir | 3 | `state_machine_definable` flag |
| 1.2 TV==Python mantığı reproduksibl | 3 | Kapalı kaynak/proprietary flagli değil |
| 1.3 Sinyal kapalı bar'dan | 4 | `preliminary_repaint_class` ∈ {LOW_RISK} → 4 |
| 1.3 Düşük future-bar riski | 4 | Repaint sınıfı (LOW=4, MEDIUM=2, HIGH=0) |
| 1.3 HTF lookahead yönetilebilir | 3 | `uses_htf` + `htf_safe` flags |
| 1.3 Riskli pivot/fractal/zigzag yok | 2 | `risky_structure=false` |
| 1.3 Realtime≈backtest muhtemel | 2 | Repaint sınıfından türetilir |
| 1.4 Entry sinyali net | 3 | `entry_pseudo` mevcut |
| 1.4 Mantıksal exit VEYA delegasyon net | 3 | `exit_pseudo` VEYA `mtc_exit_delegated` |
| 1.4 Karşı sinyal davranışı net | 3 | `opposite_signal_behavior` |
| 1.4 Re-entry/cooldown/piramitleme net | 2 | `reentry_policy` |
| 1.4 Flat/long/short durumu net | 2 | `state_model` |
| 1.4 Backtest exit modeli seçilmiş | 2 | `backtest_exit_model` |
| 1.5 Gerekli veri mevcut | 3 | `data_check.verify_actual_range` OK |
| 1.5 Granülarite mevcut | 2 | Timeframe mevcut sette |
| 1.5 İndikatörler tarihte hesaplanabilir | 2 | Geleceğe bağımlı değil |
| 1.5 Maliyet modeli eklenebilir | 2 | OHLCV (1) + fee config (1) |
| 1.5 Yeterli trade potansiyeli | 1 | Kural frekansından sezgisel |
| 1.6 Emir türü net | 2 | `order_type` |
| 1.6 Giriş zamanlaması net | 2 | `signal_timing` |
| 1.6 Spread/slippage tahmin edilebilir | 2 | Likit sembol seti |
| 1.6 Anti-likidite varsayımı yok | 1 | Manuel flag |
| 1.6 Intrabar belirsizliği yönetilebilir | 1 | Repaint sınıfı |
| 1.6 Aşırı latans bağımlılığı yok | 2 | `latency_sensitive=false` |
| 1.7 Mantıklı piyasa hipotezi | 3 | `strategy_thesis_en` mevcut |
| 1.7 Beklenen rejim belirtilmiş | 2 | `expected_regime` mevcut |

**Gate 1 Hard-Fail (herhangi biri → fail):** kodlanamaz · insan yorumlaması gerektirir · entry kuralı tanımsız · trade yaşam döngüsü tanımsız · açık repaint/lookahead · test için veri yok · sinyal barı tanımsız · tamamen görsel.

---

## Gate 1B — MTC Feasibility (/100, PASS ≥75)

**Soru:** *Bu MTC_v2'de temel düzeyde temsil edilebilir mi?*

**Gate 1B vs Gate 3 farkı:** Gate 1B = "temsil edilebilir mi?" (kaba, backtest öncesi, ucuz). Gate 3 §6.1 = "production-grade sözleşme?" (kesin zamanlama, çarpışma, entegrasyon sonrası).

| Kriter | Puan | Kaynak alan |
|---|---:|---|
| Sinyal long/short/close/flat'e indirgenebilir | 20 | `signal_reducible` |
| Entry-only vs tam strateji net | 16 | `strategy_type` |
| MTC risk engine ile çakışma yok | 20 | `risk_engine_conflict=false` |
| Alert formatına dönüştürülebilir | 16 | `alert_convertible` |
| State machine olarak modellenebilir | 16 | `state_machine_definable` |
| MTC standart parametrelere uyarlanabilir | 12 | `mtc_param_mappable` |
| **Toplam** | **100** | |

**Karar eşikleri:** ≥75 PASS · 60–74 CONDITIONAL (spec boşlukları düzelt) · <60 FAIL (backtest yok).

**Hard-fail:** manuel karar gerektirir · sinyal formatı tanımsız · risk engine ile çakışıyor · durum izlenemiyor · alert üretilemez.

---

## Hard Gate — Repaint / Lookahead Doğrulaması

| Sonuç | Etki |
|---|---|
| `VERIFIED_SAFE` | İlerle, ceza yok |
| `SAFE_WITH_DELAY` | İlerle, **Gate 2 §5.5'te −3 ceza** (gecikmeli dolum realizmi) |
| `NEEDS_MODIFICATION` | **Gate 2'yi engelle**, prototipe dön (RED DEĞİL) |
| `REJECT_REPAINT` | **Hard fail — tüm downstream gate'leri sıfırlar**, durum REJECTED |

Depolanma: `evaluation_artifact_v1.hard_flags.repaint_status`. Doğrulanana kadar: `NOT_VERIFIED` → Gate 2 hesaplayabilir ama terfi engellenir.

---

## Soft Gate — Pine⇄Python Parity (Danışma Niteliğinde)

**⚠️ Barış kararı (2026-06-04):** Advisory, hard kill-switch DEĞİL. Pine katmanı doğrudan Python/Binance çalıştırma lehine emekliye ayrılabilir.

| `parity_status` | Etki |
|---|---|
| `PASS` | Pine == Python doğrulanmış; flag yok |
| `WARN` | Uyumsuzluk `PARITY_WARNING` + "sonra yeniden bak" notu; **terfiyi ENGELLEMİYOR** |
| `N_A` | Pine karşılığı yok (saf Python) veya henüz çalıştırılmadı — ceza yok |

---

## Gate 2 — Backtest Evidence (/100)

**Soru:** *Backtest gerçek, risk-ayarlı, sağlam, benchmark-yenilir kenar gösteriyor mu?*

**Kaynak:** `evaluation_artifact_v1.schema.json` verileriyle

| # | Kategori | Puan |
|---|---|---:|
| 5.1 | Performans kalitesi | 18 |
| 5.2 | Risk / drawdown davranışı | 20 |
| 5.3 | Trade örneklem kalitesi | 12 |
| 5.4 | Sağlamlık / overfitting | 20 |
| 5.5 | Maliyet-sonrası realizm | 10 |
| 5.6 | Benchmark karşılaştırma | 10 |
| 5.7 | Rejim analizi | 10 |
| | **Toplam** | **100** |

### 5.1 Performans — 18 puan

| Alt-kriter | Puan | Metrik |
|---|---:|---|
| Net kar pozitif & anlamlı | 3 | `net_profit_pct` / `return_pct_compound` |
| Profit factor güçlü | 4 | `profit_factor` |
| Beklenti pozitif | 3 | `expectancy_r` |
| Sharpe kabul edilebilir | 3 | `sharpe` |
| Sortino kabul edilebilir | 2 | `sortino` |
| Equity eğrisi sağlıklı | 3 | `equity_curve_health` |

### 5.2 Risk / Drawdown — 20 puan

| Alt-kriter | Puan | Metrik |
|---|---:|---|
| Max drawdown kabul edilebilir | 5 | `max_drawdown_pct` |
| Recovery factor | 4 | `recovery_factor` |
| Ardışık kayıplar makul | 3 | `max_consecutive_losses` |
| Return / MaxDD oranı | 4 | `ret_dd_ratio` |
| Tek dönem hesabı silmez | 4 | `worst_window_drawdown_pct` |

### 5.3 Trade Örneklemi — 12 puan

| Alt-kriter | Puan | Metrik |
|---|---:|---|
| Trade sayısı yeterli | 4 | `trades` vs type-min |
| Test süresi yeterli | 3 | `calendar_days` vs type-min |
| Birden fazla rejim kapsanmış | 2 | `regime_coverage_count` |
| Birkaç büyük trade'e bağımlı değil | 2 | `top_trade_concentration` |
| Long/short dengesi aşırı değil | 1 | `long_short_ratio` |

### 5.4 Sağlamlık / Overfitting — 20 puan

| Alt-kriter | Puan | Metrik |
|---|---:|---|
| Parametre stabilitesi | 4 | `param_stability_score` |
| OOS çökmüyor | 3 | `oos_return_pct` |
| Walk-forward kararı | 3 | `wfo_pass` (robust ≥ ceil(folds/2)) |
| CPCV kararı | 4 | `cpcv_pass_ratio` |
| PBO (overfit olasılığı) | 4 | `pbo` (≥0.5 → OVERFIT_SUSPECT) |
| Dönemler arası çalışır | 2 | `multi_window_pass` |

### 5.5 Maliyet-Sonrası Realizm — 10 puan

(`SAFE_WITH_DELAY` durumunda burada −3 ceza uygulanır)

| Alt-kriter | Puan | Metrik |
|---|---:|---|
| Komisyona dayanır | 3 | `net_after_fees_pct` |
| Slippage'a dayanır | 3 | `net_after_slippage_pct` |
| Spread öldürmez | 2 | Türetilmiş |
| Ortalama trade maliyetlere göre büyük | 2 | `avg_trade_vs_cost` |

### 5.6 Benchmark — 10 puan

(Buy&Hold aynı sembol/TF/pencere/fee ile; risk-ayarlı)

| Alt-kriter | Puan | Metrik |
|---|---:|---|
| B&H'ye göre daha iyi risk-ayarlı | 3 | `beats_bh_risk_adjusted` / `excess_alpha_pct` |
| MaxDD anlamlı şekilde < B&H | 2 | `max_drawdown_pct` vs `bh_max_drawdown_pct` |
| Return/MaxDD B&H'den iyi | 2 | `ret_dd_ratio` vs `bh_ret_dd_ratio` |
| Benzer/daha iyi getiri, düşük maruz kalma | 2 | Exposure-ayarlı |
| Basit EMA benchmark'ı yener | 1 | `beats_ema_benchmark` |

### 5.7 Rejim — 10 puan

| Alt-kriter | Puan | Metrik |
|---|---:|---|
| Trend/range/yüksek-vol/düşük-vol ayrımı yapılmış | 4 | `regime_breakdown_present` |
| Zayıf rejim biliniyor | 3 | `weak_regime_identified` |
| Katastrofik rejim yok | 3 | `worst_regime_return_pct` |

### Provizyon Puanlama Bantları

(Bu bantlar provizyon anchor'larıdır. Son değerler Phase 1.5'te gerçek dağılımlardan belirlenecek — D5.)

| Metrik | 5 puan | 3 puan | 1 puan | 0 puan |
|---|---|---|---|---|
| Max drawdown | <15% | <25% | <40% | ≥40% |
| Sharpe | >1.5 | >1.0 | >0.5 | ≤0.5 |
| Sortino | >2.0 | >1.3 | >0.7 | ≤0.7 |
| Profit factor | >1.8 | >1.4 | >1.1 | ≤1.1 |
| Recovery factor | >3 | >2 | >1 | ≤1 |
| Return / MaxDD | >3 | >2 | >1 | ≤1 |
| PBO | <0.2 | <0.35 | <0.5 | ≥0.5 → OVERFIT_SUSPECT |

### Trade Sayısı / Süre Minimumları (§5.3)

| Tür | Min süre | Min trade |
|---|---|---:|
| Scalping | 6–12 ay | 1000+ |
| Intraday | 1 yıl | 300+ |
| Swing | 3 yıl | 100+ |
| Position | 5 yıl | 30–50+ |

### Gate 2 Bantları

- 85–100 → Güçlü
- 75–84 → İyi
- 60–74 → Zayıf-ama-geliştirilebilir
- 40–59 → Yetersiz
- 0–39 → Ret
- **Min geçiş: 75**

### Gate 2 Hard-Fail

Ücretler/slippage sonrası negatif · B&H'ye karşı anlamlı kenar yok · OOS tamamen çöküyor · Küçük param değişikliğinde kırılıyor · Kabul edilemez max DD · Tür için çok az trade · Tür için çok kısa · Kâr birkaç büyük trade'den · Equity tek piyasa döneminde yükselmiş · `PBO≥0.5` → OVERFIT_SUSPECT.

---

## Gate 3 — MTC Production Readiness (/100)

**Soru:** *Bu MTC_v2 otomasyon pipeline'ında güvenle, gözlemlenebilir şekilde çalışabilir mi?*

**⚠️ UYARI:** `production_readiness_artifact_v1` var olana kadar **N/A kalır**. Backtest çıktısı alert/state/risk/monitoring kanıtı sağlayamaz.

| # | Kategori | Puan | Artifact grubu |
|---|---|---:|---|
| 6.1 | Signal contract (production-grade) | 25 | `signal_contract` |
| 6.2 | Alert / execution adapter | 20 | `alert_adapter` |
| 6.3 | State synchronization | 15 | `state_sync` |
| 6.4 | MTC risk-engine uyumluluğu | 15 | `risk_engine_compat` |
| 6.5 | Monitoring / logging / debug | 10 | `monitoring` |
| 6.6 | Fail-safe / operasyonel güvenlik | 10 | `fail_safe` |
| 6.7 | Versiyonlama / reproduksibl | 5 | `reproducibility` |
| | **Toplam** | **100** | |

**Gate 3 Hard-Fail:** güvenilmez alert · duplicate-signal koruması yok · broker/strateji durumu eşleşemez · exit/reduceOnly belirsiz · sinyal sözleşmesi yok · yetersiz debug metadata · fail-safe yok · risk engine ile çakışıyor.

---

## Final Karar Matrisi

(Parity sütunu **sadece danışma niteliğindedir** — D3)

| Gate 1 | Gate 1B | Repaint | Parity (danışma) | Gate 2 | Gate 3 | Karar |
|---:|---|---|---|---:|---:|---|
| 75+ | PASS (≥75) | SAFE | PASS/WARN/N_A | 75+ | 75+ | Forward test / paper trade |
| 85+ | PASS | SAFE | PASS/WARN/N_A | 85+ | 85+ | Güçlü — kontrollü forward test |
| 75+ | PASS | SAFE | PASS/WARN/N_A | 75+ | <75 / N_A | İyi strateji; MTC entegrasyonu eksik |
| 75+ | PASS | SAFE | herhangi | <75 | — | Zayıf backtest; terfi edilmez |
| 75+ | PASS | herhangi | herhangi | 75+ (PBO≥0.5) | — | OVERFIT_SUSPECT — terfi engelli, fikir korunur |
| 75+ | CONDITIONAL (60–74) | — | — | — | — | Backtest öncesi spec'i geliştir |
| 75+ | FAIL (<60) | — | — | — | — | MTC-uygulanabilir değil; backtest yok |
| <75 | — | — | — | — | — | Kodlama/backtest için zayıf aday |
| any | any | REJECT_REPAINT | — | — | — | REJECTED (her şey sıfırlandı) |
| any | any | any | WARN | promoted | — | Terfi ilerler; `PARITY_WARNING` not edilir |

---

## Strateji Durum Etiketleri

```
IDEA → SPEC_DRAFT → SPEC_READY → BACKTEST_READY → PROTOTYPE_CODED →
REPAINT_VERIFIED → BACKTEST_PASSED → PARITY_VERIFIED → MTC_READY → FORWARD_TEST
```

**Çıkış rampaları:** `REJECTED` (herhangi hard-fail), `ARCHIVED` (düşük öncelik ama korunur), `OVERFIT_SUSPECT` (Gate 2 PBO engeli).

---

## Backend Dosya Haritası

| Dosya | Rol |
|---|---|
| `08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py` | `build_scorecards()` — scorecard_v2 JSON keşfi, normalleştirme, deduplikasyon |
| Aynı dosya, satır 128-170 | `_normalize_scorecard()` — ham JSON'u stabil yapıya dönüştürür |
| Aynı dosya, satır 213-230 | `_pick_display_card()` — en yüksek gate2.score'u seçer |
| Aynı dosya, satır 233-276 | `build_canonical_display_row()` — UI-36 kanonik display objesi |
| Aynı dosya, satır 364-387 | `attach_scorecards_to_rows()` — scorecard'ları pipeline satırlarına bağlar |
| `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` | Orkestrasyon — `build_scorecards()` → `attach_scorecards_to_rows()` |

## Frontend Dosya Haritası

| Dosya + satır | Fonksiyon | Rol |
|---|---|---|
| `app.js` satır 877-919 | `renderWaveAScorecard()` | Ana scorecard v2 section — 4 gate render |
| `app.js` satır 953-1011 | `renderGateRow()` | Tek gate satırı — puan, status, sub-score tablo |
| `app.js` satır 1013-1016 | `scoreForGate()` | Gate puanını `score/max` formatında döndürür |
| `app.js` satır 1018-1022 | `isPromotable()` | gate_summary.promotable kontrolü |
| `app.js` satır 2761-2783 | `renderPromotabilityPanel()` | Terfi engelleri paneli |
| `app.js` satır 2799-2838 | `renderGate2EvidenceBlock()` | Gate 2 key metrik kartları |
| `app.js` satır 2629-2656 | `passesGateFilter()` | Gate filtre mantığı |
| `app.js` satır 755-825 | `buildWaveADecision()` | Gate summary'den karar oluşturma |

## Şema Dosyaları

| Şema | Amaç |
|---|---|
| `06_SCHEMAS/status_envelope.schema.json` | Metrik başına zarf: `{value, status, reason, source_path}` |
| `06_SCHEMAS/evaluation_artifact_v1.schema.json` | Gate 2 girdi şeması (30+ metrik) |
| `06_SCHEMAS/production_readiness_artifact_v1.schema.json` | Gate 3 girdi şeması |

---

## Veri Akışı

```
[Veri Kaynakları]
  ├── candidate_metadata.yaml / producer_spec.json / audit row  ──→  Gate 1, Gate 1B
  ├── evaluation_artifact_v1 (backtest sonuçları)                ──→  Gate 2
  └── production_readiness_artifact_v1 (entegrasyon kanıtı)      ──→  Gate 3
         │
         ▼
[scorecard_reader.py]
  build_scorecards()
    → _normalize_scorecard()     (ham JSON → stabil yapı)
    → _pick_display_card()       (en yüksek gate2.score)
    → attach_scorecards_to_rows() (pipeline satırlarına bağla)
    → build_canonical_display_row() (UI-36 kanonik display)
         │
         ▼
[Dashboard UI — app.js]
  renderWaveAScorecard()    → 4 gate render
  renderGateRow()           → sub-score breakdown tabloları
  renderPromotabilityPanel() → terfi engelleri
  renderGate2EvidenceBlock() → key metrik kartları
  buildWaveADecision()      → gate summary → karar
```
