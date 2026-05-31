# AGENTS.md

## Scope
Bu repo içindeki aktif geliştirme hedefi: **MTC V2**.
V1 ve legacy backtest engine yalnızca referans amaçlıdır.

## Source of truth
- Mimari gerçek kaynak: `03_DOCS/MTC_V2_ARCHITECTURE.md`
- Pine UI gerçek kaynak: `03_DOCS/MTC_V2_INPUT_UI_SPEC.md`
- Oturum durumu: `03_DOCS/HANDOFF.md`
- Çalıştırma/validasyon komutları: `03_DOCS/RUNBOOK.md`

## Non-negotiables
1. Parity-first geliştirme uygula.
2. Pine ve Python birlikte, aynı katmanda ilerlesin.
3. Katman parity geçmeden sonraki katmana geçme.
4. Yeni feature ekleme; yalnız istenen scope içinde çalış.
5. Mimariyi implementation sırasında yeniden tasarlama.
6. Belirsizlik varsa davranış uydurma; kısa not düş ve blokajı belirt.
7. Session sonunda `03_DOCS/HANDOFF.md` güncelle.

## Build vs Validate
- **Build:** kod yazma/değiştirme
- **Validate:** çalıştırma, test, parity comparison, audit
- Validate gerekmiyorsa run komutu önerme veya çalıştırma varsayma.

## Pine policy
- Pine tarafı fiziksel olarak **tek dosya** yaklaşımıyla ele alınır.
- `LIB_*` isimleri mantıksal modül ailesidir; gerçek ayrı Pine library varsayma.
- Input surface, strategy declaration, orchestration ve final wiring ana Pine dosyasında kalır.

## Coding policy
- Minimal değişiklik yap.
- Owner boundary bozma.
- State owner'lığını çoğaltma.
- Aynı mantığı iki yere kopyalama.
- Test/kontrol olmadan geniş refactor yapma.

## Current delivery style
- Kısa, net, uygulanabilir task'lar
- Gereksiz açıklama yok
- Önce mevcut dosyaları oku, sonra patch öner
