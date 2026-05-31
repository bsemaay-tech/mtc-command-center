# Intake Prompt Applied

The finalized QuantLens intake prompt was read and applied as the normalization intent for candidate extraction.

```text
# QuantLens Candidate Intake Prompt

Bu promptu, Gemini QuantLens raporunu Codex'e verirken kullan.

## Görev

QuantLens raporunu oku, raporu arşivle, Candidate ID üret, STOP / REJECT / SALVAGE / READY_FOR_PYTHON_PROTOTYPE kararını ver ve sadece dokümantasyon/registry dosyaları oluştur.

## Kesin Kurallar

- `01_PINE/MTC_V2.pine` dosyasını değiştirme.
- Production Python runner dosyalarını değiştirme.
- Pine, Python, backtest veya optimization kodu yazma.
- Backtest veya optimization çalıştırma.
- Secret, API key, webhook, broker hesabı veya canlı işlem bilgisi yazma.
- Mevcut dosyayı overwrite etme; önce oku.

## Candidate ID Kuralı

Format:

```text
QL_YYYY-MM-DD_<MARKET>_<TF>_<SHORT_STRATEGY_SLUG>
```

Slug çakışırsa:

```text
QL_YYYY-MM-DD_<MARKET>_<TF>_<SHORT_STRATEGY_SLUG>_V2
```

## Yapılacaklar

1. QuantLens raporunu oku.
2. Raporu `06_QUANTLENS_LAB\00_INBOX_REPORTS` içine `.md` olarak kaydet.
3. Candidate ID üret.
4. STOP / REJECT / SALVAGE / READY_FOR_PYTHON_PROTOTYPE kararı ver.
5. Uygun candidate klasörünü oluştur:
   - `01_TRIAGED_CANDIDATES`
   - `02_REJECTED`
   - `03_SALVAGE_IDEAS`
   - veya `04_PYTHON_PROTOTYPES`
6. Candidate klasörüne şu dosyaları oluştur:

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

7. `_registry\quantlens_candidate_registry.csv` ve `.jsonl` dosyalarını güncelle.
8. Finalde Candidate ID, status, path ve next action raporla.

## Metadata YAML Alanları

```yaml
candidate_id:
source_url:
video_title:
quantlens_decision:
codex_status:
market_type:
primary_timeframe:
strategy_type:
commercial_value_score:
complexity_score:
repaint_risk:
lookahead_risk:
overfit_risk:
closed_source_risk:
risk_management_quality:
candidate_kind:
  producer:
  entry_gate:
  guard:
  confirmation:
  exit_rule:
  sl_tp_method:
  trailing_be_method:
  money_management:
existing_mtc_overlap:
new_feature_required:
recommended_next_step:
created_at:
updated_at:
```

```
