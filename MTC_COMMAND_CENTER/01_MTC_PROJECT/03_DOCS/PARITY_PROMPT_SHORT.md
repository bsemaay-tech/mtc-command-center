# Parity Prompt - Short

Bu klasorde benim export ettigim en son `.xlsx` dosyalarini kullan.

Once oku:
- `03_DOCS/HANDOFF.md`
- `05_PARITY/MTC_V2_TW_EXPORT_CASE_TRACKER.xlsx`
- ilgili `TW_EXPORT_CASES_V2/case_XXX/` klasoru

Zorunlu sira:
1. Case klasorundeki en son `.xlsx` dosyasini sec.
2. `Properties` sheet'ten ayarlari oku ve tracker / case plan ile karsilastir. Fark varsa once kisa `WARN` yaz.
3. Bu ayarin baseline'a veya ilgili onceki case'e gore trade sayisinda ve outcome tarafinda beklenen etkiyi yapip yapmadigini kontrol et.
4. Beklenen etki yoksa parity'e gecmeden once sebebini audit et ve kisa acikla.
5. Tautology, non-binding, inactive-path, unsupported-feature, missing-data gibi durumlari ozel olarak uyar.
6. Beklenen etki varsa, `.xlsx` ayarlarina gore `TW`, `PineTS` ve `Python` parity kontrolu yap.
7. Tracker gerekiyorsa observed ayarla guncellensin.

Ozel uyarilar:
- `MACD Zero Dist Min = 0` ise trade/outcome degismemesi normal olabilir.
- `max_entries > 1` ama model re-arm etmiyorsa trade sayisi degismeyebilir.
- HTF case'lerde feed / mock data yoksa bunu acik yaz.
- Margin ile `max_leverage_cap` uyumsuzsa bunu parity oncesi uyar.

Temizlik kurali:
- Gereksiz yeni report / temp / artifact dosyasi birakma.
- Analiz sirasinda olusan gecici dosyalar gerekiyorsa is bitince sil.
- Repo temizligini bozacak gereksiz kopya workbook veya json/csv rapor birakma.

Kisa rapor formati:
- `settings: OK|WARN`
- `expected effect: PASS|FAIL`
- `TW-PineTS: PASS|FAIL|BLOCKED`
- `TW-Python: PASS|FAIL|BLOCKED`
- `PineTS-Python: PASS|FAIL|BLOCKED`
- `reason: tek kisa cumle`

Kurallar:
- Workbook `Properties` source of truth.
- En son `.xlsx` kazanir.
- Once etki, sonra parity.
- Workbook ayari yetersizse silent fallback yapma; bunu acik `WARN` veya `BLOCKED` yaz.
- Rapor cok kisa olsun.
