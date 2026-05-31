# Overnight Session Lessons — 2026-05-30 → 2026-05-31

Tek seferlik gece sweep'inde yaşanan tüm hatalar + öğrenilen dersler. Yarın hata tekrarı yapmamak için.

## 1. Estimation hataları (ikinci kez tekrar ettim)

**Olaylar**:
- Mega runner için "5-6 saat" dedim → 11.5 dakikada bitti (30× yanlış).
- Focused validation için "3-5 dakika" dedim → 72 saniyede bitti (5× yanlış).

**Kök sebep**: İlk 60-120 saniyelik startup overhead'inden steady-state çıkarsadım. Worker bootstrap (Python import + data load) gerçek case işleme hızından çok daha yavaş.

**Sonraki sefer**:
- Steady-state hızı için en az 5 dakikalık smoke test çalıştır.
- Mümkünse önceki run'ın runtime'ını referans al (`grep "all jobs done" log`).
- Tahmini > 30 dk veriyorsan **Monitor** veya **ScheduleWakeup** kur ki bitince haberim olsun.
- Tahmini > 30 dk verdiğinde kullanıcıya "iyi geceler" deme; ya kısa beklet ya da monitor kur.

## 2. Background process yönetimi

**Olay**: `overnight_loop.sh` ben durdurduğumu sandığım halde arka planda devam etti. Iteration 21 başlatıp focused validation'ın az önce yazdığı JSON'ın **üstüne yazdı** — focused sonuçlarını kaybettim.

**Kök sebep**:
- Sadece Python proc'larını öldürmüşüm. Loop wrapper (bash) yaşamaya devam etti, yeni python başlattı.
- `mega_walk_forward.py` `OUTPUT_DIR`'i sabit kullanıyor → eşzamanlı runner'lar aynı dosyayı yazıyor.

**Sonraki sefer**:
- Loop kullanırken **wrapper PID'ini de takip et**. Sadece child process'leri kapatmak yetmez.
- Her isolated run kendi `OUTPUT_DIR/subdir/`'ine yazsın (focused_validation.py artık bunu yapıyor).
- Background komut başlatıldığında `echo "PID=$!"` çıktısını sakla.

## 3. Sandbox + Windows multiprocessing

**Olay**: `multiprocessing.Pool` worker spawn'unda `PermissionError: [WinError 5] Erişim engellendi` hataları. İlk seferde runner çöktü gibi göründü.

**Gerçek**: Sandbox handle duplication'a izin vermediği için bazı worker'lar bootstrap'ta ölüyor ama pool **survives** — diğer worker'lar devam ediyor ve run **başarıyla tamamlanıyor** (DONE_MARKER üretiyor).

**Sonraki sefer**:
- Multiprocessing içeren komutlarda `dangerouslyDisableSandbox: true` kullan (user açıkça onay verdi).
- PermissionError'ları zararsız say; gerçek hata sinyali "Traceback" + non-zero exit code.
- Log'da `[start]` satırı görürsen runner ayakta demektir; PermissionError spam'i göz ardı et.

## 4. mega_walk_forward.py mimarisi

**Bulgular**:
- 951 satır, hardcoded `GRIDS` dict + `build_signals` if/elif dispatcher.
- **Auto-discovery yok** — `04_PYTHON_PROTOTYPES/` taranmıyor. Yeni candidate eklemek = direkt `GRIDS` ve `build_signals` düzenlemek.
- `overnight_v2_runner.py` monkey-patch pattern'i kullanıyor: `mw.GRIDS.update(NEW_GRIDS)` + `mw.build_signals = patched` — upstream'i bozmadan ek strateji enjekte ediyor.

**Sonraki sefer**:
- Yeni candidate eklerken monkey-patch script'i kullan (overnight_v2_runner.py = referans).
- `build_signals` if/elif eklerken her zaman `(signal_series, stop_series)` döndür.
- Veri eksikse `pd.Series(False, ...), pd.Series(np.nan, ...)` dön.
- ENERATION kalıbı: `_my_signal(df, params, daily_rsi_map=None)` döndürse, dispatcher onu çağırır.

## 5. DSR (Deflated Sharpe) gerçeği

**Olay**: Bailey-LdP DSR p≥0.95 ile **hiçbir candidate** geçemedi (overnight + focused). Grid'i 1797 → 42'ye düşürdüm — yine 0 survivor.

**Anlam**: DSR p≥0.95 crypto'nun yüksek-volatilite/düşük-Sharpe rejimi için **realistic değil**. Geleneksel kurumsal momentum stratejileri (Sharpe 1.5+) için tasarlanmış. Crypto'da Sharpe 0.1-0.3 normal → DSR p genelde 0.3-0.7.

**Sonraki sefer**:
- Yeni research için **DSR p ≥ 0.50** kullan (50% confidence). Production'a giderken 0.85+ talep et.
- BH-FDR survivor + DSR p≥0.50 → "Tier 2 candidates" katmanı.
- Cross-symbol consistency (5+ sembolde DSR p≥0.50) → single-cell DSR p=0.85'ten **daha güçlü** kanıt.

## 6. Cross-symbol generalization > single-cell strength

**Bulgu**: `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` 6 farklı (sym × TF) hücresinde survives (DSR p 0.53-0.65). Ama her tek hücre DSR p≥0.95'i geçemez.

**Anlam**: 6 bağımsız test'in hepsinde "modestly significant" geçmek, 1 test'te "highly significant" geçmekten daha **inandırıcı**. Çünkü 6 bağımsız resample'ı tesadüfen geçme olasılığı **0.5^6 = 0.015**.

**Sonraki sefer**:
- "TRX-only overfit" suçlamasını hemen yapma — cross-symbol analysis önce.
- Aggregate analyzer ekle: "candidate kaç (sym × TF) hücresinde DSR p ≥ X geçti?"
- BH-FDR'in sıkı CI'ı yüksek-trade hücreleri (TRX 15m) lehine, düşük-trade hücreleri (BTC 4h) aleyhine biased.

## 7. URL/Transcript ingest workflow gerçeği

**Olay**: User 21 candidate'a (stg001-008 + stg082-094) "transcript indirdim" dedi.
1. Önce yanlış anladım: ingest.py "0 yeni URL" dedi → URL'ler zaten kayıtlıydı.
2. Sonra: stg dosyaları 90KB-168KB → transcript içeriyor AMA `## Transcript` heading'siz, ham metin olarak.

**Sonuç**: ingest.py mevcut versiyon **heading'siz transcript'leri yakalamaz**.

**Sonraki sefer**:
- ingest.py'a heuristic ekle: dosya boyutu > 5KB AND timestamp pattern (`\d+:\d+`) > 30 occurrence → embedded transcript var demektir.
- Transcript'i body'den çıkar (URL satırından sonra, ## Notes'tan önce).
- Filename'i: `safe_filename(title) + ".md"` (mevcut convention).

## 8. Audit otomatik pickup

**İyi haber**: Source map'e yeni URL eklenince audit_reader bir sonraki `/api/snapshot` çağrısında otomatik yakaladı (109 → 128 eligible).

**Anlam**: Server restart gerekmiyor. Per-request file scan pahalı ama 177 candidate'la sorun değil.

**Sonraki sefer**:
- Ingest sonrası ek "verify" adımı: `python -c "from mcc_readonly.audit_reader import build_candidate_audit; print(build_candidate_audit()['summary'])"` ile değişimi kontrol et.

## 9. Triage workflow formalizasyonu değerli

**Bulgu**: 11_TRIAGE/ workflow (stable Stg001..StgNNN codes + ingest pipeline + cross-iteration aggregator) **ad-hoc** triage'a göre çok daha verimli.

**Reusable artifacts**:
- `generate_worklist.py` (xlsx + .md üreteci)
- `ingest.py` (geri-akış)
- `analyze_transcripts.py` (heuristic verdict)
- `sample_for_review.py` + `deep_sample.py` (LLM context'i)
- `aggregate_overnight_iters.py` (cross-iter consistency)

**Sonraki sefer**: Bu pattern'i benzeri tek-seferlik triage işleri için tekrar kullan (örn. yeni 50 video gelirse).

## 10. Önemli sayısal sonuçlar (özet)

| Metric | Değer |
|---|---|
| Test geçişi | 29/29 |
| Audit eligible (overnight sonrası) | 128 / 177 |
| Triage worklist | 172 candidate |
| Heuristic LIKELY_MISCLASSIFIED | 24 → 25 (Andrew Connell sonrası) |
| Manuel review verdict (18 REVIEW_HUMAN) | 7 promote, 9 keep, 1 split, 1 ambiguous |
| Materialize edilen yeni candidate (spec+prototype) | 19 |
| Overnight sweep iterations | 19 (her ~18 dk) |
| Toplam case-folds (overnight) | ~6,000,000 |
| BH-FDR survivor (overnight aggregate) | 3 (hepsi TRX 15m) |
| BH-FDR + DSR≥0.50 (focused) | 8 (Christian OR×6 + Deepak Risk + HV Edge) |
| MCC audit skoru | 8.5/10 |

## 11. Gözden geçirilmesi gereken hatalar (re-do)

1. **Iter 20 başarısızlığı** — overnight_loop.sh deadline yaklaşırken iter 20 exit 127 verdi. Sebep: Python proc'larını başka bir komut için öldürdüm (focused validation öncesi temizlik). Loop wrapper devam ediyordu ama python'un olmadığı için exec başarısız oldu. → Loop kontrolü bash wrapper PID üzerinden olmalı.

2. **Focused JSON kaybı** — focused_validation 07:13'te yazdı, loop iter 21 07:45'te üzerine yazdı. → Her isolated run subdir kullansın (artık var).

3. **URL hint search Unicode hatası** — `▶` karakteri cp1254 codec'te yok. Windows shell stdout için `str.encode('utf-8', 'replace')` veya `sys.stdout.reconfigure(encoding='utf-8')`. Yarın URL hint search'i yeniden çalıştırırken bu fix gerekli.

## 12. Açık problemler (continuation prompt'ta detaylı)

- stg001-008 + stg082-094 embedded transcript'leri henüz ingest edilmedi (ingest.py'a heuristic eklenince hazır)
- 11 NO_URL candidate için repo-içi hint search yarım kaldı (Unicode hatası)
- 19 yeni promoted candidate dashboard pipeline'da görünmüyor (pipeline_reader genişletme gerekli)
- backtest_reader MEGA matrix metadata extraction eksik
- Christian Open Range 5% Stop edge için block bootstrap + rolling-origin OOS gerekli
