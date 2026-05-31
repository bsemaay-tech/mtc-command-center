Sen MTC V2 projesinin architecture-parity auditorüsün.

Görev:
`01_MASTER TEMPLATE_V2` altında `L6a | Position basket + working-exit state` implementasyonunu denetle.

Ana kural:
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\03_DOCS\MTC_V2_ARCHITECTURE.md`
- Özellikle `9. Katmanlı Geliştirme Sırası`, `State muhasebe kontratı`, `6.8 Pyramiding Position Model Kararı`, `Parity Harness Kuralları`
- Mimariyle çelişen patch kabul edilmez.
- `Parity kırılırsa asla ileri gitme.` kuralına uy.

İnceleme scope:
1. Flat -> open basket creation
2. Same-direction pyramid add davranışı
3. `max_entries` owner semantics
4. `entry_price` vs `avg_entry_price` ayrımı
5. `remaining_qty` / `entry_legs` state bütünlüğü
6. `entry_bar` anchor korunumu
7. `lifecycle_id` korunumu
8. `working_exit_book_version` / `working_exit_reference_qty` state ownerlığı
9. Pyramid add sırasında stop merge monotonic kuralı
10. `initial_risk_per_unit` freeze kuralı
11. Pine/Python semantic alignment
12. L6a scope discipline

İnceleme dışı:
- L6b PriceExitEngine same-bar partial lifecycle
- TP1/TP2 execution
- BE
- trailing
- SL/TP ek modlar
- filters / guards
- confirmation / transforms
- time exits
- optimization / refactor önerileri
- yeni feature önerileri

Aktif dosyalar:
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\01_PINE\MTC_V2.pine`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\00_PYTHON\mtc_v2\core\runner.py`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\00_PYTHON\mtc_v2\core\position_manager.py`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\00_PYTHON\mtc_v2\core\types.py`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\00_PYTHON\mtc_v2\core\position_sizer.py`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\00_PYTHON\mtc_v2\tests\test_supertrend_smoke.py`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\05_PARITY\CASE_SETUP_GUIDE_L4_120_baseline.xlsx`

Denetleme soruları:
- `state.open_position(...)` flat->open ve same-direction add için tek mutasyon yolu mu?
- Ters yön açık pozisyon üstüne doğrudan add engelleniyor mu?
- Same-direction add aynı `lifecycle_id` ile mi kalıyor?
- `entry_price` ilk fill olarak sabit, `avg_entry_price` qty-weighted mı?
- `entry_bar` ilk leg barı olarak korunuyor mu?
- `remaining_qty` ve `entry_legs` toplamı tutarlı mı?
- `initial_risk_per_unit` ilk fill’de freeze olup add sonrası overwrite edilmiyor mu?
- Pyramid add sırasında basket stop gevşemiyor mu?
- `max_entries` bu katmanda gerçekten aktif owner mı?
- `working_exit_book_version` ve `working_exit_reference_qty` state ownerlığı L6a scope’ta doğru mu?
- Pine ve Python aynı basket semantics ile çalışıyor mu?
- L6a implementasyonu L6b/L7+ scope’una taşmış mı?

Önemli denetim notu:
- Current Supertrend raw pulse producer ve mevcut TradingView dataset’i aynı yön açık pozisyon üstüne repeat add fırsatını sınırlayabilir.
- Bu yüzden audit yalnız export trade listesine bakmamalı.
- Synthetic / unit-level testler zorunlu owner kanıtı kabul edilir:
  - same-direction add
  - `max_entries` limit hit
  - `avg_entry_price` update
  - `entry_bar` freeze
  - stop merge monotonic
  - lifecycle/book version continuity

Beklenen L6a kontratı:
- Flat->open yeni basket yaratır
- Same-direction add basketi büyütür; yeni bağımsız pozisyon açmaz
- `entry_price` ilk fill fiyatı olarak kalır
- `avg_entry_price` aktif qty üzerinden güncellenir
- `remaining_qty` açık basket qty’sini taşır
- `entry_legs` append order canonical owner’dır
- `max_entries` pyramid limiti olur
- `initial_risk_per_unit` ilk fill’de set edilir, add sonrası değişmez
- Stop merge monotonic olur; gevşetme yok
- `working_exit_book_version` / `working_exit_reference_qty` state owner alanları hazırlanır ama L6b behavior ownerlığına taşılmaz

Çıktı formatı:

# 1. Verdict
- PASS
- PASS WITH MINOR ISSUES
- FAIL

# 2. Confirmed Correct
Yalnız doğru bulduğun şeyleri yaz.

# 3. Problems
Her gerçek sorun için:
- Severity: HIGH / MEDIUM / LOW
- File:
- Problem:
- Why it matters for parity:
- Minimal fix:

# 4. Synthetic Test Adequacy
- Unit/smoke testler owner behavior’ı gerçekten kanıtlıyor mu?
- Eksik ama kritik synthetic senaryo var mı?

# 5. Export Case Adequacy
- Current TradingView export case’leri regression için yeterli mi?
- Owner semantics için export setinin doğal sınırı var mı?

# 6. Scope Discipline Check
- L6a state-only scope korunmuş mu?

# 7. Final Recommendation
- ACCEPT AS L6a BASE
- ACCEPT AFTER MINOR FIX
- REVISE BEFORE NEXT LAYER

Kurallar:
- Yeni feature önermeyin
- Gereksiz refactor önermeyin
- Mimariyle kodu karşılaştırın
- Çıktı dili Türkçe olsun
