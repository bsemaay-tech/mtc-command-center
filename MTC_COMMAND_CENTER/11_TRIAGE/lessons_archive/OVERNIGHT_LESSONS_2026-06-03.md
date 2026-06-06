# Overnight Lessons — 2026-06-03 (gece çalışması 2026-06-02 → 06-03)

## Özet
- **Hedef:** ≥1M parametre overnight, mevcut stratejileri optimize et, sabaha kadar makine boş durmasın.
- **Sonuç:** **21 iter tamam, 0 crash**, ~3.6M param-evaluation (1M hedef 3.6×). 20 worker, 20:12 → 07:19 (11h deadline cap).
- **Çıktı:** 149 robust PASS cell (≥11/21 iter), 89 beat b&h, 8 down-market alpha. **AMA tüm adaylar DSR p < 0.50 → kanıtlı edge YOK.**
- **Genel ders:** Önceki gecelerin (06-01, 05-31) tüm anti-pattern fix'leri (A1-A4) çalıştı; ilk kez sıfır-crash overnight. İstatistiki darboğaz artık operasyonel değil, **metodolojik** (search-space inflation).

## Bulgular

### G1 — Sıfır-crash overnight: önceki fix'ler doğrulandı (pozitif)
- `MEGA_OUTPUT_DIR` env override (A1 fix) + thread pinning OMP/MKL/OpenBLAS/NumExpr=1 (A12) + iter-içi heartbeat (A4) + çift kanal monitor (taskschd + ScheduleWakeup, A2) → **21 iter boyunca sıfır kesinti.**
- Per-iter süre deterministik ~30dk (20w, ~172k config). Dün geceyle (13 iter) birebir tutarlı, sürpriz yok.
- **Ders:** Reçete olgun. Yeni gece için `overnight_loop_<date>_night.sh`'yi sprint script'ten kopyala, sadece deadline + heartbeat path değiştir. Reinvention yasak.

### G2 — DSR p < 0.50: search-space inflation (kritik, metodolojik)
- 149 PASS hücrenin **hepsi** Deflated Sharpe'ta çakıldı (p 0.00–0.07). En iyi down-market alpha bile (APT 1h, +110.9% excess) DSR p=0.00.
- Kök neden: DSR trial sayısını cezalandırır. Family = 43 strateji × 2031 param × 85 hücre çok büyük → DSR power yere yapışıyor. Bu, 2026-05-30'daki "full search-space altında zero noise-distinguishable config" bulgusunun tekrarı.
- **Ders:** Geniş tarama keşif (discovery) için iyi, **onay (confirmation) için değil.** Down-market 8 adayı için **dar pre-registered hipotez grid'i** ile confirmation-only run yap (örn. sadece ANY_CANDLESTICK_7 × APT/ADA + komşu paramlar). Küçük family → yüksek DSR gücü. İki aşamalı protokol: geniş discovery → dar confirmation.

### G3 — generate_morning_report.py legacy hardcoded OUTPUT_DIR (A16, yeni anti-pattern)
- `generate_morning_report.py:11` hâlâ hardcoded:
  ```python
  OUTPUT_DIR = Path(r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\05_BACKTEST_RESULTS")
  ```
- A1 fix `mega_walk_forward.py`'a uygulandı ama bu tool'a **sıçramadı.** `alpha_vs_buyhold.py` `M.OUTPUT_DIR` üzerinden env'i miras alıyor (OK), ama morning generator kendi legacy sabitini okuyor → CLEAN repo'da boş/stale.
- **Workaround:** Rapor `alpha_summary.json` + `AGGREGATE_*.json` verisinden elle yazıldı.
- **Ders:** A1 fix'i tüm tool'lara tara. `audit_hardcoded_paths.py` morning generator'ı yakalamalı (NEXT_STEPS NIGHT-FOLLOWUP-003).

### G4 — aggregate --runs-dir → otomatik dashboard görünürlüğü (pozitif pattern)
- `aggregate_overnight_iters.py --runs-dir night_runs` çalıştırınca yan etki olarak 21 iter JSON'u `05_BACKTEST_RESULTS`'a `*_results.json` olarak export etti ("Exported 21 files").
- Dashboard `backtest_reader.py` `05_BACKTEST_RESULTS/*_results.json` glob'unu okuyor → **ekstra adım olmadan** gece sonuçları Command Center backtest sekmesinde göründü (doğrulandı: 53 run, en yeni `MEGA_results_iter_21` COMPLETED).
- **Ders:** Aggregation = dashboard refresh tetikleyici. Sabah ayrı "dashboard'a yükle" adımı gerekmiyor; aggregate yeterli.

### G5 — Bash launch çift-background karışıklığı (minör)
- `nohup bash loop.sh & ` komutu `run_in_background:true` ile çağrılınca çift background oldu, ilk verify komutu 143 (timeout) ile düştü.
- **Ders:** Loop launch için tek mekanizma seç — ya `nohup ... &` (foreground Bash call) ya da `run_in_background:true` (nohup'sız). İkisini birden kullanma. Doğrulama PowerShell `Get-Process python` ile yapıldı (temiz).

## Aksiyon (NEXT_STEPS'e işlendi)
- NIGHT-FOLLOWUP-001: down-market 8 → forward-paper-trade [Barış]
- NIGHT-FOLLOWUP-002: DSR confirmation grid (dar family) [Claude/DeepSeek]
- NIGHT-FOLLOWUP-003: generate_morning_report.py legacy path fix [Claude]

## Artifact
- Rapor: `03_QUANTLENS/05_BACKTEST_RESULTS/MORNING_REPORT.md`
- Aggregate: `03_QUANTLENS/tools/night_runs/AGGREGATE_night_2026-06-02.json`
- Alpha: `03_QUANTLENS/05_BACKTEST_RESULTS/alpha_summary.json`
- Run log: `03_QUANTLENS/tools/overnight_runs/night_loop_2026-06-02.log`
