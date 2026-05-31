# CODEX — QUANTLENS OVERNIGHT MASTER PROMPT

## Absolute Mission

Bu gece görevin; 66 adet QuantLens intake `.md` raporunu kontrollü, restartable/resumable ve evidence-first şekilde işlemek; önce her rapora `01_quantlens_candidate_intake_prompt.md` akışını uygulamak; sonra sadece uygun statüye gelen adaylar için `02_quantlens_python_experiment_runner_prompt.md` ile izole Python prototype / bounded validation yapmak; backtest sonucu gerçekten `BACKTEST_PROMISING` veya `BACKTEST_PASSED` olanları ise sadece dokümantasyon/contract aşamasına, yani `03_quantlens_parity_promoter_prompt.md` aşamasına taşımaktır.

Bu gece `04_quantlens_pine_integration_prompt.md` çalıştırma. `01_PINE/MTC_V2.pine` dosyasını değiştirme. Pine patch, TradingView entegrasyonu ve canlı kullanım kararı yarın manuel incelemeden sonra yapılacak.

---

## User Context

Kullanıcı sabah kalktığında şunları görmek istiyor:

1. Tüm intake raporları işlendi mi?
2. Hangileri `REJECT`, `SALVAGE`, `WIKI_ONLY`, `READY_FOR_PYTHON_PROTOTYPE` oldu?
3. Hangi adaylar day trade strateji adayı?
4. Hangi adaylar swing trade strateji adayı?
5. Hangi adaylar uzun süreli yatırım / position trading adayı?
6. Hangi adaylar test edildi?
7. Test sonuçlarında gerçekten umut vadeden adaylar hangileri?
8. Her aday için next action nedir?
9. Hatalar varsa nerede ve nasıl tekrar devam edilir?

---

## Source Prompt Files

Repo içindeki promptları oku ve bunlara bağlı kal:

```text
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\README_PROMPTS.md
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\01_quantlens_candidate_intake_prompt.md
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\02_quantlens_python_experiment_runner_prompt.md
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\03_quantlens_parity_promoter_prompt.md
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\04_quantlens_pine_integration_prompt.md
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\05_quantlens_nightly_batch_prompt.md
```

Bu master prompt, yukarıdaki promptların yerine geçmez; onları orkestre eder. Eğer çelişki varsa daha güvenli olan kuralı uygula.

---

## Hard Safety Rules

- `01_PINE/MTC_V2.pine` dosyasını değiştirme.
- Production Python runner / engine davranışını değiştirme.
- Büyük exhaustive grid başlatma.
- Pine kodu yazma.
- Pine patch hazırlama.
- Broker, webhook, API key, secret veya canlı işlem bilgisi yazma.
- Canlı trade önerisi üretme.
- Mevcut dosyaları overwrite etme; önce oku, sonra gerekiyorsa timestamped veya versioned dosya oluştur.
- Hata olursa durma; hatayı ilgili candidate klasörüne yaz, sonra sıradaki candidate’a geç.
- Tüm çalışma restartable/resumable olmalı.
- Her uzun iş için runtime sınırı koy.
- Trade count düşükse sonucu güvenilir kabul etme.
- Net profit tek başına pass kriteri değildir.
- Commission/slippage varsayımlarını açık yaz.
- Dataset manifest, dataset_id ve source_type raporla.
- Sabah raporu üretmeden işi bitmiş sayma.

---

## Overnight Strategy

### Phase 0 — Repo State / Preflight

1. `git status --short` çalıştır.
2. Çalışma dizinini doğrula:

```text
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2
```

3. Prompt dosyalarının varlığını doğrula.
4. Intake raporlarının bulunduğu klasörü bul. Öncelik sırası:

```text
06_QUANTLENS_LAB\00_INBOX_REPORTS
06_QUANTLENS_LAB\intake_reports
06_QUANTLENS_LAB\_incoming_intake_reports
```

Eğer kullanıcı özel input klasörü verdiyse onu kullan.

5. Registry dosyalarını bul veya yoksa güvenli şekilde oluştur:

```text
06_QUANTLENS_LAB\_registry\quantlens_candidate_registry.csv
06_QUANTLENS_LAB\_registry\quantlens_candidate_registry.jsonl
```

6. Önceden işlenmiş candidate/video/report varsa tekrar işlemeye çalışma; registry ve hash kontrolü yap.

---

## Phase 1 — Process All Intake Reports With Prompt 01

Amaç: 66 intake raporunun tamamını registry’ye ve doğru klasörlere almak.

Her `.md` intake raporu için:

1. Raporu oku.
2. Duplicate kontrolü yap:
   - source_url
   - video_id varsa
   - transcript hash / report hash
   - title similarity
   - candidate slug collision
3. `01_quantlens_candidate_intake_prompt.md` kurallarını uygula.
4. Candidate ID üret.
5. Şu statülerden birini ver:
   - `REJECT`
   - `SALVAGE`
   - `WIKI_ONLY`
   - `READY_FOR_PYTHON_PROTOTYPE`
   - `NEEDS_MORE_INFO`
6. Uygun klasörü oluştur:
   - `01_TRIAGED_CANDIDATES`
   - `02_REJECTED`
   - `03_SALVAGE_IDEAS`
   - `04_PYTHON_PROTOTYPES`
7. Her candidate için şu dosyaları oluştur:
```text
<CandidateID>\
├─ 00_raw_quantlens_report.md
├─ 01_candidate_metadata.yaml
├─ 02_codex_triage.md
├─ 03_mtc_module_mapping.md
├─ 04_experiment_plan.md
├─ 05_risks_and_unknowns.md
└─ 06_next_action.md
```
8. Registry CSV ve JSONL güncelle.
9. Her candidate için bir log satırı yaz:

```text
06_QUANTLENS_LAB\logs\nightly_intake_YYYY-MM-DD.log
```

---

## Phase 2 — Rank READY_FOR_PYTHON_PROTOTYPE Candidates

Tüm intake bittikten sonra sadece `READY_FOR_PYTHON_PROTOTYPE` adayları listele ve önceliklendir.

Adayları üç bucket’a ayır:

```text
DAY_TRADE_CANDIDATES
SWING_TRADE_CANDIDATES
POSITION_INVESTING_CANDIDATES
```

Her aday için puanla:

```yaml
commercial_value_score: 1-10
rule_clarity_score: 1-10
codability_score: 1-10
data_availability_score: 1-10
risk_management_quality: 1-10
mtc_v2_overlap_score: 1-10
overfit_risk: LOW/MEDIUM/HIGH
repaint_risk: LOW/MEDIUM/HIGH
lookahead_risk: LOW/MEDIUM/HIGH
expected_runtime: LOW/MEDIUM/HIGH
bucket:
  - DAY_TRADE
  - SWING_TRADE
  - POSITION_INVESTING
priority:
  - P0
  - P1
  - P2
  - SKIP_FOR_NOW
```

Sabaha yetişmesi için test önceliği:

1. P0 day trade adayları
2. P0 swing trade adayları
3. P0 position/long-term adayları
4. P1 adaylar, zaman kalırsa

Eğer P0 aday sayısı çok fazlaysa her bucket’tan en iyi 2-3 adayı seç. Kaliteyi quantity’ye tercih et.

---

## Phase 3 — Run Bounded Python Prototype / Validation With Prompt 02

Sadece `READY_FOR_PYTHON_PROTOTYPE` ve `P0/P1` adayları için `02_quantlens_python_experiment_runner_prompt.md` uygula.

Her candidate için:

1. Candidate metadata oku.
2. Experiment plan oku.
3. Eksik kritik bilgi varsa:
   - status: `NEEDS_MORE_INFO`
   - sebebi yaz
   - sonraki adaya geç
4. Production runner’ı değiştirme.
5. İzole prototype / adapter yaklaşımı kullan.
6. Büyük exhaustive grid yapma.
7. Bounded validation yap.

### Dataset / Symbol Guidance

Mevcut data bundle’ları ve manifestleri ara. Öncelik:

```text
BTCUSDT
ETHUSDT
SOLUSDT
BNBUSDT
XRPUSDT
```

Eğer strateji stock-specific ise, kriptoya körlemesine uyarlama yapma. Uygun veri yoksa `NEEDS_MORE_INFO` veya `DATA_UNAVAILABLE` olarak raporla.

Eğer elde stock/equity datası yoksa, stock-specific stratejiyi “prototype spec only / no valid backtest data” olarak bırak; kripto sonucunu gerçek edge gibi sunma.

### Validation Minimums

Her test edilen aday için mümkünse:

```text
symbol_results.csv
walk_forward_results.csv
robustness_summary.md
pass_fail_decision.md
next_action.md
backtest_config.yaml
```

Output path:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\<CandidateID>\
```

### Pass/Fail Decision Values

Şunlardan birini kullan:

```text
BACKTEST_FAILED
BACKTEST_PROMISING
BACKTEST_PASSED
NEEDS_MORE_INFO
DATA_UNAVAILABLE
```

### Backtest Decision Criteria

Sadece net profit ile pass verme. Şunlara bak:

```text
trade_count
profit_factor
max_drawdown
expectancy
win_rate + average R
multi-symbol consistency
walk-forward / OOS stability
sensitivity robustness
commission/slippage sensitivity
parameter fragility
market regime dependency
```

Eğer trade count düşükse sonucu güvenilmez kabul et.

---

## Phase 4 — Promote Only Truly Promising/PASSED Candidates With Prompt 03

Sadece şu statülerden biri varsa:

```text
BACKTEST_PROMISING
BACKTEST_PASSED
```

`03_quantlens_parity_promoter_prompt.md` uygula.

Output:

```text
06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\<CandidateID>\
├─ 00_backtest_summary.md
├─ 01_feature_contract.yaml
├─ 02_python_reference_logic.md
├─ 03_pine_integration_plan.md
├─ 04_parity_test_plan.md
├─ 05_expected_risks.md
└─ 06_go_no_go.md
```

Bu aşamada da:

- Pine kodu yazma.
- `MTC_V2.pine` değiştirme.
- Production Python runner değiştirme.
- Sadece contract / plan / parity hazırlığı yap.

---

## Phase 5 — Do NOT Run Prompt 04 Tonight

`04_quantlens_pine_integration_prompt.md` bu gece çalıştırılmayacak.

Sebep:

- Pine entegrasyonu son aşamadır.
- Önce kullanıcı sabah backtest ve parity hazırlık sonuçlarını inceleyecek.
- Yeni özellikler default OFF ve feature-gated olmalı.
- Patch öncesi ayrı manuel karar gereklidir.

Sabah raporunda sadece şunu yaz:

```text
PINE_INTEGRATION_NOT_RUN_BY_DESIGN
```

---

## Phase 6 — Morning Summary Report

Sabah okunacak ana raporu oluştur:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_summary_YYYY-MM-DD.md
```

Rapor şu bölümleri içersin:

```text
# QuantLens Overnight Summary

## 1. Executive Summary
- total intake reports found
- processed count
- skipped duplicates
- rejected count
- salvage/wiki count
- ready for prototype count
- tested count
- promising count
- passed count
- failed count
- needs more info count
- data unavailable count

## 2. Best Day Trade Candidates
Table:
CandidateID | Strategy | Status | Symbols Tested | PF | MaxDD | Trade Count | Decision | Path | Next Action

## 3. Best Swing Trade Candidates
Same table.

## 4. Best Position / Long-Term Investment Candidates
Same table.

## 5. Promoted To Parity
CandidateID | Feature Type | Output Path | Go/No-Go | Main Risk

## 6. Rejected / Salvage / Wiki Summary
CandidateID | Status | Reason | Path

## 7. Errors
CandidateID | Error | File Path | Resume Action

## 8. Registry Updates
CSV path
JSONL path
counts by status

## 9. Important Warnings
- no Pine modified
- no production runner modified
- no exhaustive grid
- no live trading approval
- stock-specific strategies not blindly accepted on crypto data
- low trade-count results are not reliable

## 10. Recommended Next Manual Actions For User
Top 3 actions for tomorrow.
```

---

## Required Final Console Response

Çalışma sonunda kısa cevap ver:

```text
OVERNIGHT_WORK_COMPLETE

Summary:
- Intake processed: X / Y
- Ready for Python: X
- Tested: X
- Promising/PASSED: X
- Promoted to parity docs: X
- Pine modified: NO
- Production runner modified: NO
- Main summary:
  06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_summary_YYYY-MM-DD.md

If incomplete:
- Reason:
- Resume command / next prompt:
```

---

## If Runtime Is Running Out

Eğer her şeyi bitiremiyorsan öncelik sırası:

1. Tüm 66 intake raporunu registry’ye işle.
2. READY adayları bucket ve priority’ye göre sırala.
3. En iyi P0 day trade adaylarını bounded test et.
4. En iyi P0 swing adaylarını bounded test et.
5. En iyi P0 position adayını bounded test et veya data yoksa spec-only bırak.
6. Morning summary yaz.

Asla yarım kalan işi sessiz bırakma. Her yarım kalan candidate için `next_action.md` yaz.

---

## Start Now

Şimdi çalışmaya başla.

Önce preflight yap, sonra Phase 1’den başla. Soru sorma. Mevcut repo durumuna göre en güvenli varsayımlarla ilerle. Hata olursa candidate-level hata raporu yaz ve sıradaki candidate’a geç.
