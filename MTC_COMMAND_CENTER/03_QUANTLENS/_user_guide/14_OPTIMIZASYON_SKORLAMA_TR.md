# Optimizasyon Skorlama Sistemi — MTC Command Center

**⚠️ Durum:** PLANLANMIŞ — Henüz tam implemente değil. Foundation (Phase 1) henüz oluşturulmamış.

**Kaynak Plan:** `01_MTC_PROJECT/handoff/MTC_V2_PORTABLE_HANDOFF/03_DOCS/PLANS/MTC_V2_OPTIMIZATION_LOOP_SCORING_CROSS_MARKET_PLAN.md`

---

## Amaç

Optimizasyon parametre taramalarından çıkan adayları sıralamak. **Sadece kâra dayalı sıralama yapılmamalıdır.**

Skor sistemi şunlara karşı koruma sağlamalıdır:

- Yüksek drawdown
- Çok az trade
- Overfitting
- Tek-piyasa başarısı
- Dengesiz parametre adaları
- Aşırı trade frekansı
- Düşük exposure ile tesadüfi kâr
- Gerçek dışı kaldıraç/marj varsayımları

---

## Skorlama Profilleri

Dört farklı profil planlanmıştır:

```
optimization/scoring_profiles/
├── parity_first.yml     ← Parity doğrulaması ağırlıklı
├── conservative.yml     ← Düşük risk odaklı
├── balanced.yml         ← Dengeli (varsayılan başlangıç noktası)
└── aggressive.yml       ← Yüksek getiri odaklı
```

**Not:** Bu profil dosyaları henüz disk üzerinde oluşturulmamıştır. Sadece plan dokümanında tanımlanmıştır.

---

## Ortak Skorlama Bileşenleri

Tüm profiller aşağıdaki bileşenleri kullanır:

```yaml
metrics:
  profit_score:
    source: net_profit_pct
    direction: maximize

  drawdown_penalty:
    source: max_drawdown_pct
    direction: minimize

  profit_factor_score:
    source: profit_factor
    direction: maximize

  win_rate_score:
    source: win_rate
    direction: maximize

  trade_count_quality:
    source: total_trades
    min_required: 20
    max_preferred: 500

  robustness_score:
    source: cross_market_median_rank
    direction: minimize

  stability_score:
    source: parameter_neighborhood_stability
    direction: maximize
```

---

## Dengeli Skorlama Formülü

Başlangıç noktası olarak önerilen formül:

```
score =
  0.30 × normalized_net_profit_pct
+ 0.20 × normalized_profit_factor
+ 0.15 × normalized_win_rate
+ 0.20 × inverse_normalized_max_drawdown_pct
+ 0.10 × trade_count_quality
+ 0.05 × robustness_score
```

### Ağırlık Dağılımı

| Bileşen | Ağırlık |
|---|---:|
| **Net Kâr %** | %30 |
| **Profit Factor** | %20 |
| **Max Drawdown (ters)** | %20 |
| **Win Rate** | %15 |
| **Trade Sayısı Kalitesi** | %10 |
| **Sağlamlık** | %5 |

### Normalizasyon Notu

Her metrik kendi aralığında normalize edildikten sonra ağırlıklara çarpılır. `inverse_normalized_max_drawdown_pct` drawdown'un **düşük** olmasının ödüllendirildiği anlamına gelir.

---

## Hard Reject Kuralları

Aşağıdaki koşullardan **herhangi biri** varsa, skordan bağımsız olarak aday **reddedilir:**

| Kural | Açıklama |
|---|---|
| `feature_parity_not_passed` | Feature parity gate'i geçmedi |
| `dataset_manifest_invalid` | Dataset manifesto doğrulanamıyor |
| `total_trades < min_trades` | Minimum trade sayısının altında |
| `max_drawdown_pct > max_drawdown_cap` | Maksimum drawdown kapağını aştı |
| `profit_factor <= 1.0` | Profit factor 1'in altında (kaybeden sistem) |
| `net_profit_pct <= 0` | Net kâr negatif veya sıfır |
| `too_many_failed_cross_market_runs` | Çok fazla başarısız cross-market çalışması |
| `result_contains_nan_or_inf` | Sonuçlarda NaN veya infinity |

---

## MTC Parity Kuralı

```
Parity çalışmaları için:
  Commission = 0
  Slippage = 0

Optimizasyon araştırması için:
  Commission/slippage ayrı profillerde etkinleştirilebilir,
  ANCAK parity sonuçları ile optimizasyon sonuçları
  etiketlemeden asla karıştırılmamalıdır.
```

---

## Per-Variant Sonuç Alanları

Her parametre kombinasyonu çalışması şu alanları üretir:

```
variant_id, feature_id, params_hash, dataset_id,
symbol, timeframe, start, end,
net_profit, net_profit_pct,
max_drawdown, max_drawdown_pct,
gross_profit, gross_loss, profit_factor,
win_rate, total_trades, avg_trade, median_trade,
max_consecutive_losses, exposure_pct,
sharpe_like, sortino_like, expectancy,
score, status, failure_reason
```

---

## Cross-Market Doğrulama (Phase 6)

**Amaç:** Optimizörün sadece tek sembolde veya tek dönemde çalışan parametreler bulmasını engellemek.

### Cross-Market Metrikleri

Her aday için:

| Metrik | Açıklama |
|---|---|
| `median_score` | Piyasalar arası medyan skor |
| `mean_score` | Piyasalar arası ortalama skor |
| `worst_market_score` | En kötü piyasa skoru |
| `positive_market_count` | Pozitif sonuçlu piyasa sayısı |
| `negative_market_count` | Negatif sonuçlu piyasa sayısı |
| `median_drawdown` | Medyan drawdown |
| `worst_drawdown` | En kötü drawdown |
| `trade_count_distribution` | Trade sayısı dağılımı |
| `rank_stability` | Sıralama stabilitesi |

### Sağlamlık (Robustness) Terfi Kuralları

Bir aday ancak şu koşulları karşılarsa sağlam sayılır:

```
positive_market_count >= required_positive_markets
worst_drawdown <= max_allowed_worst_drawdown
median_score >= minimum_median_score
Tek piyasa max_profit_concentration_pct'den fazla katkı yapamaz
```

### Örnek Doğrulama Suite'i

```yaml
suite_id: crypto_major_15m_core
datasets:
  - BTCUSDT_15m_2024_Q1
  - ETHUSDT_15m_2024_Q1
  - SOLUSDT_15m_2024_Q1
  - BNBUSDT_15m_2024_Q1
  - ADAUSDT_15m_2024_Q1
```

---

## In-Sample / Out-of-Sample Doğrulama (Phase 7)

**Amaç:** Eğitim dönemine overfitting'i engellemek.

### Ayrım Türleri

| Tür | Açıklama |
|---|---|
| `fixed_date_split` | Sabit tarih ayrımı |
| `rolling_walk_forward` | Hareketli walk-forward |
| `anchored_walk_forward` | Sabitlenmiş walk-forward |
| `regime_based_split` | Rejim tabanlı ayrım |

### Kabul Kuralı

Aday, sadece in-sample'da performans gösterip out-of-sample'da çökerse terfi edemez:

```
out_of_sample_score >= %60 of in_sample_score
out_of_sample_net_profit_pct > 0
out_of_sample_max_drawdown_pct <= max_oos_drawdown_cap
out_of_sample_total_trades >= min_oos_trades
```

---

## Terfi Seviyeleri (Phase 8)

"İyi optimizasyon sonucu" ile "entegrasyona değer aday" ayrı kavramlardır.

| Seviye | Ad | Anlamı |
|---|---|---|
| LEVEL_0 | `FEATURE_TRACE_PASS` | Feature izleme geçti |
| LEVEL_1 | `SELECTABLE_INTEGRATION_PASS` | Seçilebilir entegrasyon geçti |
| LEVEL_2 | `LOCAL_FAST_SUITE_PASS` | Yerel hızlı suite geçti |
| LEVEL_3 | `OPTIMIZATION_PASS` | Optimizasyon geçti |
| LEVEL_4 | `CROSS_MARKET_PASS` | Cross-market doğrulama geçti |
| LEVEL_5 | `OUT_OF_SAMPLE_PASS` | OOS doğrulama geçti |
| LEVEL_6 | `RELEASE_AUDIT_READY` | Release denetimi hazır |
| LEVEL_7 | `TRADINGVIEW_AUDITED` | TradingView denetimi tamamlanmış |

### Aday Dosya Formatı

```yaml
candidate_id: candidate_range_filter_v1_balanced_001
feature_id: producer_range_filter_v1
source_job: opt_range_filter_v1_balanced_001
params:
  length: 40
  multiplier: 2.0
  source: hl2

promotion_level: LEVEL_5_OUT_OF_SAMPLE_PASS

evidence:
  feature_parity_report: reports/parity/.../FEATURE_PARITY_REPORT.json
  fast_suite_report: reports/parity/...
  optimization_report: reports/optimization/...
  cross_market_report: reports/optimization/.../CROSS_MARKET_REPORT.md
  walk_forward_report: reports/optimization/.../WALK_FORWARD_REPORT.md

risk_notes:
  - Not yet TradingView audited.
  - Do not use live.
```

---

## Raporlama Standartları (Phase 10)

Her optimizasyon işi şu dosyayı üretmelidir: `OPTIMIZATION_REPORT.md`

### Zorunlu Bölümler

| Bölüm | İçerik |
|---|---|
| A | Executive summary |
| B | Job metadata |
| C | Feature contract |
| D | Preconditions checked |
| E | Dataset manifest summary |
| F | Parameter search space |
| G | Scoring profile |
| H | Number of variants |
| I | Failed variants |
| J | Top 20 candidates |
| K | Rejected candidates |
| L | Best candidate details |
| M | In-sample performance |
| N | Out-of-sample performance (varsa) |
| O | Cross-market validation (varsa) |
| P | Robustness notes |
| Q | Risk notes |
| R | Promotion recommendation |
| S | Exact commands run |
| T | Output files |
| U | Final verdict |

### İzin Verilen Kararlar

```
OPTIMIZATION_PASS_CANDIDATES_FOUND      ← Aday bulundu
OPTIMIZATION_PASS_NO_ROBUST_CANDIDATE   ← Sağlam aday yok
OPTIMIZATION_BLOCKED_FEATURE_PARITY     ← Feature parity engeli
OPTIMIZATION_BLOCKED_DATASET            ← Dataset engeli
OPTIMIZATION_FAILED_RUNNER_ERROR        ← Runner hatası
OPTIMIZATION_NOT_COMPARABLE             ← Karşılaştırılamaz
```

---

## İmplementasyon Durumu

| Phase | Ad | Durum |
|---|---|---|
| 1 | Optimization Foundation | ❌ Oluşturulmadı |
| 2 | Dataset Manifest + Market Regime Registry | ❌ Oluşturulmadı |
| 3 | Optimization Job Schema | ❌ Oluşturulmadı |
| 4 | Optimization Runner | ❌ Oluşturulmadı |
| 5 | Scoring Profiles | ❌ Oluşturulmadı |
| 6 | Cross-Market Validation | ❌ Oluşturulmadı |
| 7 | In-Sample / Out-of-Sample Validation | ❌ Oluşturulmadı |
| 8 | Candidate Promotion | ❌ Oluşturulmadı |
| 9 | Codex Agent Rules | ❌ Oluşturulmadı |
| 10 | Reporting Standards | ❌ Oluşturulmadı |
| 11 | Minimal First Implementation (Range Filter) | ❌ Başlanmadı |
| 12 | Feature Factory Integration | ❌ Oluşturulmadı |
| 13–14 | Codex Prompts | 📄 Dokümante edildi |

### Planlanan Dosya Yapısı

```
optimization/
├── README.md
├── schema/
│   ├── optimization_job.schema.json
│   ├── optimization_result.schema.json
│   ├── scoring_profile.schema.json
│   └── dataset_manifest.schema.json
├── scoring_profiles/
│   ├── parity_first.yml
│   ├── conservative.yml
│   ├── balanced.yml
│   └── aggressive.yml
├── datasets/
│   ├── dataset_manifest.yml
│   └── regimes.yml
├── jobs/
│   └── examples/
│       └── range_filter_balanced_grid.yml
├── candidates/
│   └── <candidate_id>.yml
└── docs/
    └── CODEX_OPTIMIZATION_AGENT_RULES.md

tools/
├── run_feature_optimization.py
├── rank_optimization_results.py
├── validate_cross_market.py
├── build_dataset_manifest.py
└── verify_dataset_manifest.py

reports/optimization/<job_id>/
├── job_snapshot.yml
├── parameter_grid.csv
├── all_results.csv
├── ranked_results.csv
├── best_candidates.json
├── failed_variants.json
├── OPTIMIZATION_REPORT.md
├── cross_market/
│   ├── CROSS_MARKET_REPORT.md
│   ├── cross_market_results.csv
│   ├── cross_market_ranked_candidates.csv
│   └── rejected_candidates.json
├── walk_forward/
│   ├── WALK_FORWARD_REPORT.md
│   ├── windows.csv
│   ├── per_window_results.csv
│   └── promoted_candidates.json
└── logs/
```

---

## Codex Agent Kuralları (Phase 9 — Planlanmış)

### Codex YAPMALI

- Optimizasyon öncesi feature parity doğrula
- Çalıştırma öncesi dataset manifesto doğrula
- Her job snapshot'ını kaydet
- Her parametre kombinasyonunu kaydet
- Her sonucu kaydet
- Scoring profile kullanarak sırala
- Başarısız varyantları raporla
- Reddedilen adayları raporla
- Kötü sonuçları asla gizleme
- Optimizasyon sonuçlarını parity sonuçlarından ayır
- Exact hash'ler kullan

### Codex YAPMAMALI

- Optimizasyon sırasında `01_PINE/MTC_V2.pine` değiştirme
- Prodüksiyon Python davranışını değiştirme
- TradingView export'u normal döngü olarak kullanma
- Canlı exchange API'leri kullanma
- Final audit verisinde doğrudan optimize etme
- Sadece kâra dayalı skorlama kullanma
- Kullanıcı açıkça istemedikçe başarısız varyantları silme
- Terfi kanıtı olmadan "hazır" iddia etme
- Parity raporlarında commission/slippage etkinleştirme
- Parity ve optimizasyon ayarlarını sessizce karıştırma

---

## Veri Akışı

```
[Girdiler]
  ├── Feature Parity Report
  ├── Dataset Manifest (YAML)
  ├── Job Tanımı (YAML)
  └── Scoring Profile (YAML)
         │
         ▼
[Optimization Runner — tools/run_feature_optimization.py]
  1. Precondition Check (parity + dataset doğrulama)
  2. Parameter Grid Generation
  3. Python MTC Engine × N varyant çalıştır
  4. Per-Variant Results kaydet
         │
         ▼
[Skorlama]
  1. Metrikleri normalize et
  2. Ağırlıklı skor hesapla (balanced formül)
  3. Hard reject filtre uygula
  4. Sırala (rank)
         │
         ▼
[Doğrulama]
  1. Cross-Market Validation (5+ sembol)
  2. Out-of-Sample Validation (IS/OOS split)
         │
         ▼
[Çıktılar]
  ├── ranked_results.csv
  ├── best_candidates.json
  ├── OPTIMIZATION_REPORT.md
  └── Candidate Promotion (LEVEL_0 → LEVEL_7)
```

---

## İlk POC Hedefi (Phase 11)

**Range Filter** kullanılması önerilir çünkü:

1. Gerçek bir yeni feature
2. İzole feature parity'yi geçmiş
3. Sinyal producer'ıdır
4. Henüz kanonik MTC_V2.pine'a entegre edilmemiş

### Minimum Uygulama Sırası

1. Range Filter için selectable draft entegrasyonu tamamla
2. Seçilmiş FAST_SUITE'i lokalde çalıştır
3. Optimization foundation klasör/şema oluştur
4. Range Filter için basit bir grid job oluştur
5. Grid'i tek dataset üzerinde çalıştır
6. Sonuçları sırala
7. Top 5 adayı 2-3 cross-market dataset'te çalıştır
8. Aday raporu üret

### İlk aşamada YAPILMAMASI gerekenler

- ❌ 100+ dataset
- ❌ Bayesian optimization
- ❌ PyneCore
- ❌ vectorbt
- ❌ TradingView automation
- ❌ Live trading
