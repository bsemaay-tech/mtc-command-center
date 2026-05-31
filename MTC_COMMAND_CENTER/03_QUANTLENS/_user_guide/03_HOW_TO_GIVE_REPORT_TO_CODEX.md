# How To Give Report To Codex

## Prompt nasıl kullanılır?

`06_QUANTLENS_LAB\_prompts\01_quantlens_candidate_intake_prompt.md` dosyasını aç ve içeriğini Codex'e ver.

## Rapor nereye yapıştırılır?

Promptun altına şu başlığı ekle:

```text
## QuantLens Report
```

Sonra raporu aynen yapıştır.

## Codex çıktı olarak ne üretmeli?

- Inbox rapor dosyası.
- Candidate klasörü.
- Metadata YAML.
- Triage raporu.
- MTC module mapping.
- Experiment plan.
- Risk ve unknowns notu.
- Next action dosyası.
- CSV ve JSONL registry kaydı.

## Candidate ID nerede bulunur?

- `_registry\quantlens_candidate_registry.csv`
- Candidate klasör adı
- `01_candidate_metadata.yaml`
- Codex final raporu
