# Codex Stage-2B Master Report

## 1. Kisa karar
Onceki LLM backtestleri tamamen guvenilir degil. Kodlar bazi yerlerde calisiyor, fakat execution, contract ve metrik raporlama katmaninda kritik zayifliklar var. PASS_STAGE3_CODE_VERIFIED yok.

## 2. Onceki backtest kodlari guvenilir miydi?
Kismen. Trade trace dosyalari yeniden hesaplanabilir, fakat onceki kararlar compounded return sismesi, crypto proxy, eksik native veri, eksik golden-case testleri ve bazi contract sapmalari yuzunden dogrudan guvenilir degil.

## 3. Her aday icin code mapping sonucu
- KELL_WEDGE: NEEDS_NATIVE_DATA - only 17 trades and Claude contract audit says the previous proxy dropped Kell cycle preconditions
- CRABEL_RANGE_EXPANSION: NEEDS_NATIVE_DATA - Claude contract audit says canonical Crabel is intraday/session based; crypto-daily prior backtest is not a fair test
- SLINGSHOT_EMA_PULLBACK: WEAK_STAGE3_CODE_VERIFIED - coded contract is simple enough, but OOS PF broke below 1 and drawdown is unacceptable
- BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR: NEEDS_CONTRACT_REWRITE - previous code uses RSI recovery plus CHoCH, not a strict divergence contract
- MARTIN_LUKE_PULLBACK: NEEDS_NATIVE_DATA - AVWAP/relative strength context is equity-native; crypto proxy OOS failed
- LINDA_5SMA_PULLBACK: NEEDS_NATIVE_DATA - RS is proxied, not native; base edge is weak and drawdown is extreme

## 4. Her aday icin synthetic test sonucu
Tum adaylarda Stage-2B synthetic execution testleri tanimlandi ve validation fazinda calistirilmak uzere hazirlandi.

## 5. Her aday icin golden case sonucu
Her aday icin 10 proxy real-data golden case yazildi; bunlar trace/recompute tutarliligini dogrular, native piyasa edge kaniti degildir.

## 6. Her aday icin repaired backtest sonucu
Repaired harness onceki trade_trace uzerinden metrikleri yeniden hesaplar; onceki klasorler degistirilmedi.

## 7. Her aday icin baseline/random comparison
Random same-hold onceki Stage-2 baseline dosyalarindan okundu; opposite/shuffled baseline Stage-2B trace uzerinden yeniden hesaplandi.

## 8. Her aday icin fee stress sonucu
Fee stress ayni trade setinde 1x/2x/3x/5x olarak tekrar hesaplandi ve monotonic gate uygulandi.

## 9. Her aday icin OOS sonucu
OOS onceki walkforward_results.csv dosyalarindan okundu; Slingshot, BigBeluga, Martin ve Linda dogrudan guclu OOS gecemiyor.

## 10. Kodlama hatasi bulunan yerler
BigBeluga divergence eksik; Martin AVWAP proxy; Linda RS proxy; Crabel same-bar/gap fill; onceki compounded return raporu karar icin riskli.

## 11. Onceki LLM raporlarindan dogrulananlar
No Pine/MTC-ready aday; crypto proxy caveat; weak swing list; Stage-3 oncesi native veri gereksinimi.

## 12. Onceki LLM raporlarindan curutulenler
Yuksek compounded return degerleri rescue kaniti degil; baseline beaten tek basina yeterli degil; crypto proxy US equity edge kaniti degil.

## 13. PASS_STAGE3_CODE_VERIFIED var mi?
Yok.

## 14. WEAK_STAGE3_CODE_VERIFIED var mi?
Var: SLINGSHOT_EMA_PULLBACK sadece research-only zayif aday olarak kalabilir.

## 15. NEEDS_CONTRACT_REWRITE olanlar
BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR.

## 16. NEEDS_NATIVE_DATA olanlar
KELL_WEDGE, CRABEL_RANGE_EXPANSION, MARTIN_LUKE_PULLBACK ve LINDA_5SMA_PULLBACK.

## 17. Pine/MTC'ye gecis onerisi
Gecilmeyecek.

## 18. Stage-3 icin onerilen tek producer adayi varsa adi
Yok. En yakin code-verified research-only aday SLINGSHOT; en iyi native-data retest CRABEL.

## 19. Hangi adaylar cope atilmamali?
CRABEL ve SLINGSHOT cope atilmamali; Linda/Kell native veri gelirse tekrar bakilabilir.

## 20. Acik riskler
Native veri eksigi, intrabar execution belirsizligi, contract formalizasyonu, proxy veri siniri.

## 21. Dosyalar
Bu klasor altinda aday bazli audit, trace, metric, synthetic, golden ve verdict dosyalari uretildi.

## 22. Komutlar
COMMAND_LOG.txt icinde kayitli.

## 23. Validasyon
py_compile, synthetic tests, metric recompute, fee monotonic, CSV readable, verdict files, git status ve untouched kontrolleri validation fazinda kayit altina alindi.
