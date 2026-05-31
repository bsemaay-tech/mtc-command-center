# Nightly Run Instructions

## Prompt nasıl kullanılır?

`06_QUANTLENS_LAB\_prompts\05_quantlens_nightly_batch_prompt.md` içeriğini Codex'e ver.

## Kaç candidate test edilecek?

Limit yoksa küçük batch kullanılmalı. İlk güvenli seçim 1 veya 2 candidate'dır.

## Gece testlerinde ne değişmemeli?

- `01_PINE/MTC_V2.pine` değişmemeli.
- Production Python runner davranışı değişmemeli.
- Büyük exhaustive grid başlatılmamalı.
- Secret veya API key yazılmamalı.

## Sabah summary nerede olur?

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_summary_YYYY-MM-DD.md
```

Sabah bu summary, registry ve candidate sonuç klasörleri Codex'e özetletilir.
