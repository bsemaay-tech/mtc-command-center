# QuantLens Prompt Guide

## Hangi prompt ne zaman kullanilir?

- `00_quantlens_transcript_intake_prompt.md`: YouTube transcript veya video URL + transcript dogrudan verildiginde; duplicate, kanal kalite ve Trader Wiki ayrimini once yapar.
- `01_quantlens_candidate_intake_prompt.md`: Yeni QuantLens raporu geldiğinde.
- `02_quantlens_python_experiment_runner_prompt.md`: Status `READY_FOR_PYTHON_PROTOTYPE` oldugunda.
- `03_quantlens_parity_promoter_prompt.md`: Status `BACKTEST_PASSED` veya `BACKTEST_PROMISING` oldugunda.
- `04_quantlens_pine_integration_prompt.md`: Sadece status `READY_FOR_PINE_INTEGRATION` oldugunda.
- `05_quantlens_nightly_batch_prompt.md`: Gece kucuk batch prototype/backtest calismasi icin.

## Yeni video transcripti gelince

Once `00_quantlens_transcript_intake_prompt.md` kullanilir. Bu prompt:

- video_id ve normalized_url uretir,
- transcript_hash ile duplicate kontrolu yapar,
- channel blacklist/watchlist kontrolu yapar,
- strateji varsa candidate workflow'a yonlendirir,
- strateji yok ama faydali bilgi varsa `WIKI_ONLY` Trader Wiki notu olusturur.

## Yeni QuantLens raporu gelince

STOP raporuysa birak. Uygun raporu Codex'e `01_quantlens_candidate_intake_prompt.md` ile ver.

## Gece hangi prompt kullanilir?

`05_quantlens_nightly_batch_prompt.md` kullanilir. Limit yoksa kucuk batch ile ilerlenir.

## Parity asamasina ne zaman gecilir?

Backtest `BACKTEST_PASSED` veya arastirmaya deger sekilde `BACKTEST_PROMISING` olursa parity promoter promptu kullanilir.

## MTC_V2.pine hangi asamaya kadar degistirilmez?

`04_quantlens_pine_integration_prompt.md` asamasina kadar degistirilmez. O asamada bile yeni feature default OFF ve feature-gated olmalidir.
