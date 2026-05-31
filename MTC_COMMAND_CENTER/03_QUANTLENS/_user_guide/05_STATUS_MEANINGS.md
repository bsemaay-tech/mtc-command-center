# Status Meanings

## Registry status anlamlari

- `NEW`: Yeni rapor, triage bekliyor.
- `TRIAGED`: Incelendi, karar yazildi.
- `REJECTED`: Uygun degil.
- `SALVAGE_ONLY`: Sadece fikir alinabilir.
- `READY_FOR_PYTHON_PROTOTYPE`: Izole prototype'a hazir.
- `PYTHON_PROTOTYPE_DONE`: Prototype tamam, verdict bekliyor.
- `BACKTEST_FAILED`: Testten kaldi.
- `BACKTEST_PROMISING`: Ilginc ama daha kanit gerekir.
- `BACKTEST_PASSED`: Backtest esigini gecti, parity hazirligina aday.
- `NEEDS_MORE_INFO`: Kullanici veya kaynak ek bilgi vermeli.
- `READY_FOR_PARITY`: Parity hazirligina gecebilir.
- `PARITY_BLOCKED`: Parity riski cozulmeden ilerleyemez.
- `PARITY_FAILED`: Karsilastirma basarisiz.
- `PARITY_PASSED`: Tanimli parity yuzeyi gecti.
- `READY_FOR_PINE_INTEGRATION`: Final integration planina hazir.
- `APPROVED_FOR_MTC`: Default OFF feature-gated MTC adayi.
- `WIKI_ONLY`: Strateji yok; faydali bilgi Trader Wiki'ye kaydedildi.
- `DUPLICATE`: Video/transcript daha once islenmis; yeni candidate olusturulmadi.
- `ARCHIVED`: Kapanmis kayit.

## Hangi status kullanici aksiyonu ister?

`NEEDS_MORE_INFO`, `PARITY_BLOCKED`, `BACKTEST_PROMISING`, `READY_FOR_PINE_INTEGRATION`, `DUPLICATE`.

## Hangi status otomatik devam edebilir?

`READY_FOR_PYTHON_PROTOTYPE`, `BACKTEST_PASSED`, `READY_FOR_PARITY`.

## Hangi status strategy candidate degildir?

`WIKI_ONLY` strategy candidate degildir. `DUPLICATE` durumunda onceki kayit kullanilir.

## Guvenlik notu

`BACKTEST_PASSED` ve `PARITY_PASSED` canli kullanim onayi degildir.
