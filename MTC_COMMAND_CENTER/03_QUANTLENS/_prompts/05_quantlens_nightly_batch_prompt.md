# QuantLens Nightly Batch Prompt

Bu prompt gece çalışmasında registry'deki küçük bir candidate batch'ini kontrollü şekilde işlemek için kullanılır.

## Görev

Registry oku, `READY_FOR_PYTHON_PROTOTYPE` adayları sırayla seç, kullanıcı limit verdiyse o kadar aday işle. Limit yoksa güvenli küçük batch kullan.

## Kesin Kurallar

- `01_PINE/MTC_V2.pine` değiştirme.
- Production Python runner davranışını değiştirme.
- Büyük exhaustive grid başlatma.
- Runtime sınırı koy.
- Bilgisayarı uyutma veya kapatma komutu verme; sadece raporla.
- Her candidate için ayrı sonuç klasörü kullan.
- Hata olursa hatayı candidate klasörüne yaz ve bir sonraki candidate'a geç.
- Sonuçlar restartable/resumable olmalı.

## Output

Her candidate sonucu:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\<CandidateID>\
```

Sabah okunacak özet:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_summary_YYYY-MM-DD.md
```

Özet içinde işlenen candidate, status, hata, output path ve next action yaz.
