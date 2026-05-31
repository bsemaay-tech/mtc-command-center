# QuantLens Pine Integration Prompt

Bu prompt sadece `READY_FOR_PINE_INTEGRATION` statüsündeki adaylar içindir.

## Uyarı

Bu aşama son aşamadır ve dikkatli kullanılmalıdır. `MTC_V2.pine` sadece bu aşamada ve yalnız doğrulanmış plan üzerinden değişebilir.

## Görev

Feature contract ve parity planını oku. Patch hazırlamadan önce planı doğrula, gerekli testleri ve rollback planını yaz.

## Kesin Kurallar

- Yeni özellik default OFF olmalıdır.
- Yeni özellik feature-gated olmalıdır.
- Existing behavior değişmemelidir.
- Pine ve Python mantığı aynı kalmalıdır.
- Input surface, strategy declaration, orchestration ve final wiring sınırları açıkça korunmalıdır.
- Patch öncesi `git status --short`, hedef diff kapsamı ve rollback planı raporlanmalıdır.
- Backtest başarısı canlı kullanım onayı değildir.

## Required Plan Check

1. Feature contract mevcut mu?
2. Python reference logic mevcut mu?
3. Pine integration point açık mı?
4. PineTS parity planı açık mı?
5. TradingView export final audit planı açık mı?
6. Repaint/lookahead riski kapatıldı mı?
7. Default OFF ve feature gate açık mı?
