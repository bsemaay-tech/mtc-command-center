# QuantLens Candidate Status Legend

Bu registry, YouTube strateji raporlarindan gelen adaylarin MTC_V2 workflow icindeki durumunu takip eder.

## Status Values

- `NEW`: Rapor geldi, henuz Codex triage yapilmadi.
- `TRIAGED`: Rapor okundu ve temel siniflandirma tamamlandi.
- `REJECTED`: Strateji yetersiz, kapali kaynak, repaint/lookahead riski yuksek veya MTC_V2 icin uygunsuz.
- `SALVAGE_ONLY`: Tam strateji olarak zayif; sadece filtre, guard, exit, SL/TP, trailing veya confirmation fikri alinabilir.
- `READY_FOR_PYTHON_PROTOTYPE`: Kurallar yeterince acik; izole Python prototip planlanabilir.
- `PYTHON_PROTOTYPE_DONE`: Izole prototip tamamlandi; henuz backtest verdict yok.
- `BACKTEST_FAILED`: Bounded validation, walk-forward veya robustness sonucunda basarisiz.
- `BACKTEST_PROMISING`: Sonuclar arastirmaya deger; daha fazla OOS, sembol veya hassasiyet kontrolu gerekir.
- `BACKTEST_PASSED`: Backtest esigini gecti; parity promotion icin aday olabilir.
- `NEEDS_MORE_INFO`: Kritik kural, veri, kaynak veya risk bilgisi eksik.
- `READY_FOR_PARITY`: Backtest sonrasi feature contract ve parity hazirligina alinabilir.
- `PARITY_BLOCKED`: Repaint, lookahead, veri, PineTS veya Python/Pine esleme riski cozulmeden ilerlenemez.
- `PARITY_FAILED`: Pine/Python/PineTS/TradingView karsilastirma yuzeyinde basarisiz.
- `PARITY_PASSED`: Tanimli parity yuzeyi gecti; canli kullanim onayi degildir.
- `READY_FOR_PINE_INTEGRATION`: Feature contract, parity plani ve risk listesi hazir.
- `APPROVED_FOR_MTC`: Default OFF ve feature-gated MTC_V2 entegrasyon adayi olarak onaylandi.
- `WIKI_ONLY`: Kodlanabilir strateji yok; faydali trader/yatirim bilgisi Trader Wiki'ye kaydedildi.
- `DUPLICATE`: Video veya transcript daha once islenmis; yeni candidate olusturulmadi.
- `ARCHIVED`: Kapanmis veya tarihsel kayit olarak saklaniyor.

## Hard Rules

- `BACKTEST_PASSED`, dogrudan MTC_V2'ye alinacak anlamina gelmez.
- `PARITY_PASSED`, canli kullanim onayi anlamina gelmez.
- `APPROVED_FOR_MTC`, sadece default OFF ve feature-gated entegrasyon adayligi anlamina gelir.
- `WIKI_ONLY`, MTC_V2 strategy candidate anlamina gelmez.
- `DUPLICATE`, tekrar islem yapilmadigi ve onceki kaydin referans alinacagi anlamina gelir.
- `MTC_V2.pine` sadece final Pine integration asamasinda degisebilir.
