# MTC V2

Bu klasör, MTC V2'nin aktif geliştirme alanıdır.

## Amaç
Pine Script ve Python backtest engine'i **birlikte**, **katman katman** ve **parity-first** yaklaşımıyla geliştirmek.

## Aktif klasörler
- `00_PYTHON/` → aktif Python geliştirme
- `01_PINE/` → aktif Pine geliştirme
- `03_DOCS/` → mimari, UI spec, handoff, runbook
- `04_AUDIT/` → audit raporları

## Önce okunacak dosyalar
1. `AGENTS.md`
2. `03_DOCS/HANDOFF.md`
3. Gerekirse `03_DOCS/MTC_V2_ARCHITECTURE.md`
4. Gerekirse `03_DOCS/MTC_V2_INPUT_UI_SPEC.md`
5. Çalıştırma gerekiyorsa `03_DOCS/RUNBOOK.md`

## Çalışma modeli
- **Build phase:** kod yazma / refactor / parity implementation
- **Validate phase:** test, parity run, audit, raporlama
- Bu iki faz birbirine karıştırılmaz.

## Proje kuralları
- Aktif hedef yalnız **MTC V2**
- V1 ve eski engine sadece **referans**
- Pine tarafı **tek dosya** yaklaşımıyla geliştirilir
- Katman parity geçmeden sonraki katmana geçilmez
