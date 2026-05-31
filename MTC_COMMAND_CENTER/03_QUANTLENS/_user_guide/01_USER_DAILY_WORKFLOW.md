# User Daily Workflow

## Gündüz yapılacaklar

- YouTube strateji videosu bul.
- Gemini QuantLens'e ver.
- STOP raporu gelirse bırak.
- Uygun raporu Codex'e `01_quantlens_candidate_intake_prompt.md` ile ver.
- Candidate ID ve registry status kontrol et.

## Akşam/gece yapılacaklar

- Registry'de `READY_FOR_PYTHON_PROTOTYPE` aday var mı kontrol ettir.
- `05_quantlens_nightly_batch_prompt.md` ile küçük batch başlat.
- Limit ver: örnek `max 2 candidate`.
- MTC_V2.pine değişmemeli.

## Sabah kontrolü

- Registry status değişimlerini özetlet.
- `05_BACKTEST_RESULTS` içindeki yeni klasörleri özetlet.
- `nightly_summary_YYYY-MM-DD.md` varsa okut.
- `BACKTEST_PROMISING` veya `BACKTEST_PASSED` adaylar için parity promoter promptuna geç.

## Kullanıcının elle değiştirmemesi gereken klasörler

- `_registry`
- `04_PYTHON_PROTOTYPES`
- `05_BACKTEST_RESULTS`
- `06_PROMOTED_TO_PARITY`
- `08_PARITY_RESULTS`

Manuel rapor koyulacaksa sadece `00_INBOX_REPORTS` kullanılmalı.
