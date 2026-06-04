# Overnight Lessons — 2026-06-04 (gece çalışması 2026-06-03 → 06-04)

## Özet
- **Hedef:** ≥3M parametre overnight (kullanıcı talebi), sabaha rapor hazır, makine uyumasın, soru sorma.
- **Sonuç:** **20 iter tamam, 0 crash**, 3,435,700 param-evaluation (3M hedef 1.15×). 20 worker, 19:37 → 07:07 (06:37 deadline cap'e yakın). `last_exit_code: 0`.
- **Çalıştıran:** Codex (Claude kredisi bitti). 13dk "aktif" görünüyor ama asıl loop 11.5h arka planda döndü.
- **Çıktı:** 149 robust PASS cell (≥10/20 iter), 89 beat b&h, **gerçek down-market alpha=8** (alpha log ground truth). Tüm adaylar hâlâ DSR p<0.50 dominant → kanıtlı edge YOK.
- **Genel ders:** Reçete 2. kez üst üste sıfır-crash (06-03 gecesinin tekrarı) — operasyonel olgunluk doğrulandı. Yeni problem **rapor üretim katmanında** (A18) ve **süreç disiplininde** (G5).

## Bulgular

### G1 — İkinci sıfır-crash gece: reçete stabil (pozitif)
- Sprint script'ten kopyalanan `overnight_loop_2026-06-03_night.sh` + keep-awake launcher (`start_overnight_2026-06-03_keepawake.ps1`) + izole `night_runs/night_2026-06-03` subdir → 20 iter sıfır kesinti, exit 0.
- Per-iter ~34dk deterministik (20w, ~172k config). Önceki gecelerle tutarlı.
- **Ders:** Runbook §6.2 reçetesi olgun. A10 (izole subdir) burada doğru uygulandı — Codex ilk yanlış başlangıcı (eski night_runs'a karışacaktı) fark edip durdurup ayrı subdir'le yeniden başlattı. Reçete + A10 disiplini çalışıyor.

### G2 — A16 yeni tool ile aşıldı (pozitif, ama A18 doğurdu)
- Legacy `generate_morning_report.py` (A16 hardcoded path) yerine Codex **yeni** `write_overnight_morning_report.py` (237 satır) yazdı → rapor `alpha_summary.json` + `AGGREGATE_*.json`'dan üretildi, doğru dizine düştü.
- **Ders:** A16 workaround'u tool'laştırmak doğru yön. AMA yeni tool kendi sayım hatasını getirdi → bkz A18.

### G3 — A18 (YENİ): morning report down-market alpha yanlış sayım/etiket (kritik-rapor)
- Rapor başlığı: *"78 are down-market alpha. DSR research-threshold confirmations: 2."*
- Alpha log ground truth: `ALPHA_DONE passes=149 beat_buyhold=89 premium=13 down_market_alpha=8`.
- **78 ≠ 8.** Ayrıca raporun "Down-Market Alpha" tablosu (satır 98–117) "Strategy vs Buy-and-Hold" tablosunun (satır 71–90) **birebir kopyası** — b&h<0 filtresi uygulanmamış, beat-b&h excess>100 satırları yanlış etiketle tekrarlanmış.
- Kök neden: `write_overnight_morning_report.py` down-market sayımını yanlış kaynak/filtre ile hesaplıyor; tabloyu da yanlış slice'tan dolduruyor.
- **Etki:** Rapor güveni düşük. Sayı yanlış → karar (forward-paper-trade aday seçimi) yanlış adayları gösterebilir.
- **Ders (A18):** Morning report sayıları **alpha log `ALPHA_DONE` satırı = single source of truth** ile cross-check edilmeli. Generator'a assert ekle: rapor `down_market_alpha` == log `down_market_alpha`. Down-market tablosu b&h<0 filtresinden gelmeli, beat-b&h tablosundan değil.

### G4 — DSR <0.50 dominant: A17 hâlâ açık (metodolojik, devam)
- 149 PASS'in büyük çoğunluğu DSR p<0.50 (en güçlü OPUSDT cell'leri 0.65 civarı ama düşük-trade; yüksek-trade cell'ler p≈0.00).
- Önceki gecenin G2/A17 bulgusu aynen geçerli: geniş search-space DSR power'ı eziyor.
- **Ders:** Confirmation-only dar pre-registered grid run hâlâ yapılmadı (NIGHT-FOLLOWUP-001 devrediyor). Geniş tarama tekrarı yeni bilgi getirmiyor — sıradaki gece **discovery değil confirmation** olmalı.

### G5 — Gece sonu konvansiyonu tamamlanmadı (süreç, kritik)
- INDEX convention 5 adım emrediyor: (1) dated lessons, (2) index güncelle, (3) runbook §8 merge, (4) guideline merge, (5) CHANGELOG.
- Codex **0/5** yaptı — sadece MORNING_REPORT üretti. Dated lessons yok, index güncellenmedi, A18 runbook'a işlenmedi.
- **Ders:** Loop §6.4 "GECE SONU KAPANIŞ" adımı raporla bitmiyor; lessons+index+runbook merge zorunlu. Bunu morning report writer'ın POST adımına bağla (otomatize et) ya da gece-sonu checklist'i ayrı script yap. Aksi halde her model bu adımı atlıyor.
  - (Bu dosya + index + A18 merge, sonraki sabah Claude tarafından elle tamamlandı — 2026-06-04.)

## Aksiyon
- NIGHT-FOLLOWUP-001 (devir): down-market 8 aday → dar confirmation grid run (discovery değil). [Barış]
- NIGHT-FOLLOWUP-A18: `write_overnight_morning_report.py` down-market sayım + tablo filtresi düzelt; `ALPHA_DONE` ile assert. [kod]
- NIGHT-FOLLOWUP-G5: gece-sonu kapanış (lessons+index+runbook) otomatize et veya checklist script. [kod]
- MTC_v2 entegrasyon: YOK — rapor `APPROVED_FOR_MTC_V2_INTEGRATION: none`. Registry/dashboard tadilatı başka sohbette sürüyor; bu sonuçlar sadece read-only research view.
