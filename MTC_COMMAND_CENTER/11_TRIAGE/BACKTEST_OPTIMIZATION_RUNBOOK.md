# BACKTEST + OPTIMIZATION RUNBOOK (cold-start uyumlu)

> **CANONICAL STANDART:** [`03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`](../03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md)
> Bu dosya **resmi kurallar** — 4 gate, buy&hold + alpha, DSR, BH-FDR, classification, promotion levels, antigravity checklist. **Her backtest'te zorunlu pre-read.**
>
> Bu runbook (`BACKTEST_OPTIMIZATION_RUNBOOK.md`) sadece **operasyonel katman**:
> - Hangi tool'u nasıl çalıştırırsın (mega_walk_forward, overnight_v2_runner, alpha_vs_buyhold)
> - Overnight loop mekaniği (worker, heartbeat, taskschd)
> - In-day single-strategy backtest akışı
> - Anti-pattern arşivi (geçmiş lessons konsolidasyonu)
>
> **Kural soruları → rules dosyası.** Yürütme soruları → bu dosya.
>
> **Amaç:** Bu repoyu hiç görmemiş bir AI (Claude / DeepSeek V4 Pro / Gemini / Codex)
> rules + runbook'u okuyup `06_PROMOTED_TO_PARITY` kalitesinde backtest + optimizasyon yürütebilsin.
> Reinvention yasak.
>
> **Versiyon:** 2026-06-01 (rules dosyasına bağlandı). Living doc.
> **Arşiv:** `lessons_archive/OVERNIGHT_LESSONS_YYYY-MM-DD.md`
> **Geçmiş runbook'lar (her biri kısmi kapsam):**
> - `01_MTC_PROJECT/docs/optimization/BIG_OVERNIGHT_OPTIMIZATION_RUNBOOK.md` (MTC V2 dar kapsam)
> - `02_MTC_BACKTEST/backtest_assets/00_RUNBOOK.md` (legacy mtc_backtest autopilot)
> - `09_DOCS/AI_WORKFLOW.md` (multi-AI rol bölüşümü)
> - `_AI_MEMORY/SPRINT_WORKFLOW.md` (sprint mekaniği)
> - `01_MTC_PROJECT/docs/optimization/OPTIMIZATION_LESSONS_LEARNED_20260427.md`

---

## 0. PRE-READ (zorunlu, 5dk)

1. `AGENTS.md` + `_AI_MEMORY/START_HERE.md` + `_AI_MEMORY/AI_RULES.md`
2. **`03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`** ← CANONICAL STANDART (4 gate, classification, promotion, antigravity, morning report format)
3. **Bu dosya** (BACKTEST_OPTIMIZATION_RUNBOOK.md) — operasyonel yürütme
4. `_AI_MEMORY/GLOBAL_HANDOFF.md` + `NEXT_STEPS.md` (mevcut iş listesi)
5. Son arşiv: `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_*.md` (en yeni 1 tane)
6. `git status` + `git log --oneline -10`

Atlama yasak. Her biri spesifik tuzak öğretir.

**Kural vs yürütme ayrımı:**
- "Bir candidate'ı PROMOTE_TO_PARITY için hangi gate'leri geçmesi gerek?" → **rules dosyası §8**
- "Loop crash olursa nasıl recover ederim?" → **bu runbook §7**
- "Buy&hold karşılaştırma nasıl yapılır?" → **rules dosyası §4 + `alpha_vs_buyhold.py`**
- "Workers'ı kaç yapayım?" → **bu runbook §5**

---

## 0.5 KAPSAM — overnight DEĞİL her backtest

Bu runbook üç senaryo için aynı kalite eşiğini garanti eder:

| Senaryo | Tipik süre | Worker | Tetik |
|---|---|---|---|
| **In-day single strategy** | 5-60dk | 4-8 | "Bu stratejiyi BTC 1h'de backtest et" |
| **Multi-strategy sprint** | 1-3 saat | 16-20 | "Mevcut 39 stratejiyi 1 saatte sweep et" |
| **Overnight sweep** | 6-12 saat | 16 | "Gece sabaha kadar koşsun" |

Üçü için de aynı 4 gate uygulanır (rules dosyası §8). Single strategy = daha az config ama **aynı statistical rigor**. Farklı olan sadece worker sayısı, deadline, monitor yoğunluğu.

### 0.5.1 In-day single strategy akışı (özet)
```bash
# 1. Pre-read: rules dosyası + bu runbook §4 (overfit gates)
# 2. Veri validation
python -c "from pathlib import Path; p = Path('...'); print('first/last bar:', ...)"

# 3. Sandbox backtest (küçük grid)
python tools/walk_forward_processor.py --strategy <id> --symbol BTC --tf 1h --grid small

# 4. 4-gate validation
#    a. Rolling WF + lockbox OOS — built-in
#    b. Bootstrap p (50k resample) + BH-FDR
#    c. Deflated Sharpe Ratio
#    d. Multi-window (Q1-Q4) + parameter neighborhood
python tools/finalize_bootstrap_bh.py --input <result.json>
python tools/multiwindow_oos.py --candidate <id>

# 5. Buy&hold karşılaştırma (ZORUNLU — rules §4)
python tools/alpha_vs_buyhold.py --result <result.json>

# 6. Morning report formatında çıktı (rules §10)
python tools/generate_morning_report.py --single-candidate <id>
```

**In-day kısayolu:** Tek strateji için 4-gate çalıştırma overhead'i ~30-60 saniye. Atlanması yasak — rules §7 "Antigravity Error-Prevention Checklist" madde 3, 4, 7, 10, 11.

---

## 1. BACKTEST STACK — SINGLE SOURCE OF TRUTH

| Katman | Konum | Amaç |
|---|---|---|
| **MTC V2 backtest (Pine parity)** | `01_MTC_PROJECT/src/`, `02_MTC_BACKTEST/` | TradingView Pine ↔ Python parity test |
| **QuantLens research backtest** | `03_QUANTLENS/tools/mega_walk_forward.py` (951 satır) | Çoklu strateji × sembol × TF walk-forward + DSR + BH-FDR |
| **Triage + ingest** | `11_TRIAGE/` | YouTube transcript → candidate prototype boru hattı |
| **Prototypes** | `03_QUANTLENS/04_PYTHON_PROTOTYPES/` | Tek strateji Python implementasyonu |
| **Promoted (parity ready)** | `03_QUANTLENS/06_PROMOTED_TO_PARITY/` | Pine'a aktarmaya hazır spec'ler |

**Engine seçimi:**
- **MTC V2 parity / Pine release:** `01_MTC_PROJECT/docs/optimization/BIG_OVERNIGHT_OPTIMIZATION_RUNBOOK.md` (resume registry, 16 worker, thread pinning)
- **Yeni QuantLens stratejisi research:** `03_QUANTLENS/tools/mega_walk_forward.py` + `overnight_v2_runner.py` monkey-patch
- **Custom 1-shot backtest:** `03_QUANTLENS/tools/walk_forward_processor.py`

Bu runbook **QuantLens overnight research** akışını anlatır. MTC V2 parity için yukarıdaki BIG_OVERNIGHT dosyasına git.

---

### 1.1 MTC-Engine Validation for shortlisted producers

Use this after cheap naked QuantLens screening, not during mass discovery. The goal is to test whether
raw producer signals still have an edge when routed through the existing MTC Python risk engine.

```bash
cd MTC_COMMAND_CENTER/02_MTC_BACKTEST
python -m src.cli.mtc_engine_validate ^
  --producer supertrend ^
  --data data/BTCUSDT_15m_20240101_20241231.parquet ^
  --symbol BTCUSDT ^
  --timeframe 15m ^
  --output results/mtc_engine_validation_runs/supertrend_smoke
```

Required artifacts: `report.md`, `results.json`, `manifest.json`, `trades.csv`.

Rules:
- `MTCRunner` remains the engine; do not fork or duplicate it.
- `src/config/profiles/light_risk.py` must prove filters/guards OFF and risk ON.
- Producer adapters live in `src/modules/signals/producers/` and emit raw long/short signals only.
- Standalone Pine producer adapters live in `01_MTC_PROJECT/parity_oracles/feature_adapters/pinets/`.
- If a producer-level parity command exists, pass it with `--parity-command`; otherwise the report must say `NOT_RUN`.
- This stage never edits `MTC_V2.pine` and never claims full lifecycle parity.

---

## 2. PRE-FLIGHT CHECKLIST (her gece, sırayla)

### 2.1 Path & writability
- [ ] `MEGA_OUTPUT_DIR` env yazılabilir mi? Default = `03_QUANTLENS/05_BACKTEST_RESULTS/`
- [ ] Legacy `C:\LAB\tradingview-lab\` dizini **read-only** (`-r--r--r--`). Asla hedef olarak alma.
- [ ] Disk doluluk < %90 (`Get-PSDrive C`)

### 2.2 Veri bütünlüğü
- [ ] OHLCV bundle erişilebilir
- [ ] Symbol listesi gerçekçi (17 crypto USDT default)
- [ ] Timeframe listesi gerçekçi (`["15m","1h","2h","4h","1D"]` default)

### 2.3 Strateji + grid kontrolü
- [ ] `GRIDS` dict'inde tüm stratejilerin grid sayısı > 0
- [ ] `build_signals` dispatcher her strateji için `(signal_series, stop_series)` döner
- [ ] Yeni strateji eklerken **monkey-patch pattern** (overnight_v2_runner.py referans) — upstream'i değiştirme

### 2.4 Smoke test (HARD GATE)
Loop launch'tan ÖNCE 1 dakikalık dummy:
```bash
cd 03_QUANTLENS/tools
MEGA_WORKERS=2 MEGA_OUTPUT_DIR=/tmp/smoke timeout 120 python overnight_v2_runner.py > /tmp/smoke.log
grep -q "all jobs done" /tmp/smoke.log && echo PASS || echo FAIL
ls -la /tmp/smoke/MEGA_walk_forward_results.json  # MUST exist
```
JSON yazımı kanıtlanmadan loop **başlatma**. Kanıt yoksa OUTPUT_DIR audit yap.

### 2.5 Monitör hazır
- [ ] `monitor_overnight.ps1` script mevcut, syntax temiz
- [ ] taskschd kayıt komutu hazır (admin yetkisi gerek): `register_overnight_monitor.ps1`
- [ ] Heartbeat path standart: `overnight_runs/_heartbeat.json` (sprint için `_heartbeat_sprint.json`)
- [ ] Wakeup zinciri planı: 30dk interval, ilk fire +30dk

### 2.6 Resource hijack önle
- Chrome / TradingView / Excel / Outlook / OneDrive sync KAPAT
- Keep-awake script: `01_MTC_PROJECT/scripts/keep_awake_*.ps1` ayrı PS sessions'da

---

## 3. WALK-FORWARD + MULTI-SYMBOL + MULTI-TIMEFRAME

### 3.1 Walk-forward yapı (mega_walk_forward.py defaults)
- `NUM_ROLLING_FOLDS = 3` (research için 6'ya çıkar — overnight_v2_runner.py bunu yapıyor)
- `FOLD_TRAIN_FRACTION = 0.60`, `FOLD_TEST_FRACTION = 0.20`
- `LOCKBOX_FRACTION = 0.25` (son %25 hiçbir fold'a girmez → final OOS)
- `MIN_BARS_REQUIRED = 1500`
- `MIN_TRADES_FOR_PASS = 30`

### 3.2 Multi-symbol stratejisi
- Minimum 8 sembol; default 17 USDT pair (BTC, ETH, SOL, BNB, XRP, ADA, AVAX, MATIC, LINK, LTC, DOT, ATOM, UNI, AAVE, FIL, NEAR, APT)
- **Single-cell pass kabul etme.** Cross-symbol consistency = ana sinyal:
  - "5+ sembolde DSR p≥0.50" ≫ "1 sembolde DSR p≥0.95"
  - 5 bağımsız resample'ı tesadüfen geçme olasılığı ~0.5⁵ = 0.031

### 3.3 Multi-timeframe stratejisi
- Default TF set: `["15m","1h","2h","4h","1D"]`
- 5m TF sadece intraday/OR stratejileri için (gap reclaim, episodic pivot)
- 1D ayrı profil; CHOPPY/CONSOLIDATING rejiminde zayıf → regime-mitigation katmanı

### 3.4 Aggregate analyzer
Loop sonrası `aggregate_overnight_iters.py` çalıştır:
- Cross-iter consistency: bir candidate kaç iter'de PASS?
- Cross-cell coverage: candidate kaç (sym × TF) hücresinde geçti?
- Best/worst split: highest avg return vs most defensive seed

---

## 4. OVERFIT-SKEPTIK VALİDASYON (zorunlu sıra)

```
PASS classification (return + sharpe + trades)
     ↓
Bootstrap p-value (2000 resample, lockbox OOS)
     ↓
BH-FDR survivor (Q=0.10, family = tüm valid boot_p)
     ↓
DSR p-value (Bailey-LdP, grid_n trial)
     ↓
robust_final = PASS ∧ bh_fdr_survivor ∧ dsr_robust
     ↓
Cross-symbol consistency check (≥5 hücre)
     ↓
Cross-iter consistency check (≥3 iter aynı candidate)
     ↓
06_PROMOTED_TO_PARITY/ aday
```

### 4.1 DSR eşik kalibrasyonu (crypto için)
- **DSR p≥0.95** klasik akademik eşik — kurumsal hisse momentum (Sharpe 1.5+) için tasarlanmış. Crypto'da hemen hiçbir candidate geçemez.
- **DSR p≥0.50** crypto research için pragmatik (50% confidence).
- **Production'a giderken DSR p≥0.85** talep et.

### 4.2 BH-FDR caveat
BH-FDR sıkı CI'ı yüksek-trade hücreleri (örn. TRX 15m) lehine biased. Düşük-trade BTC 4h hücreleri aleyhine. Cross-symbol agg'a güven, single-cell BH-FDR survivor'ı aşırı yorumlama.

### 4.3 Lockbox testinin korunması
- Lockbox'a sweep'in HİÇBİR aşamasında bakma (parameter tuning dahil)
- Lockbox sonucu fold-OOS'tan kategori farklı kötüyse → temporal overfit göstergesi
- Lockbox testinde min 30 trade gerekir; az ise NO_DATA olarak işaretle, PASS verme

---

## 5. WORKER POLİTİKASI

### 5.1 Çevre tabanı
| Senaryo | Worker | Kural |
|---|---|---|
| Smoke / debug | 1-2 | Hızlı fail için |
| MTC V2 parity gece (BIG_OVERNIGHT) | **16** (onaylı benchmark — DEĞİŞTİRME) | `--max-workers 16` zorunlu |
| QuantLens research gece (sessiz oda, kullanıcı uyuyor) | 16-20 (cpu_count'a göre) | Fan zaten audible değil |
| QuantLens research gündüz (kullanıcı çalışıyor) | 2-4 | Fan sessiz |
| Sprint / kısa süre | cpu_count | Maksimum throughput |

### 5.2 Override mekanizması
- `mega_walk_forward.py:742` — `MEGA_WORKERS` env okur
- Loop script'inde `export MEGA_WORKERS=N` ile sabitle
- Runtime'da değiştirme imkanı YOK (Python pool init'te kilit) — yeni iter için yeni env gerekir

### 5.3 Thread pinning (BIG_OVERNIGHT zorunlu, QuantLens önerilen)
```powershell
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:NUMEXPR_NUM_THREADS='1'
```
Numpy/pandas BLAS thread'leri worker'larla çakışırsa süre 2-3× yavaşlar.

---

## 6. LAUNCH SEQUENCE

### 6.1 Standart akış
```bash
# 1. Pre-flight
cd 03_QUANTLENS/tools
python -c "import mega_walk_forward as mw; print('OUTPUT_DIR=', mw.OUTPUT_DIR, 'writable=', __import__('os').access(str(mw.OUTPUT_DIR), 2))"

# 2. Smoke (HARD GATE)
MEGA_WORKERS=2 timeout 120 python overnight_v2_runner.py 2>&1 | tail -10
# Bekle: "all jobs done" + JSON file timestamp güncel

# 3. Loop launch (background)
bash overnight_loop_YYYY-MM-DD.sh > overnight_runs/loop_master.out 2>&1 &
echo $! > overnight_runs/loop.pid

# 4. Monitor kanalları
# 4a. taskschd (admin PS):
& "tools/register_overnight_monitor.ps1"

# 4b. Wakeup zinciri (AI session'da):
# ScheduleWakeup 1800s, prompt = bu runbook'tan "monitor tick" bölümü
```

### 6.2 Loop script şablonu (her gece için 1 kopya)
- Konum: `03_QUANTLENS/tools/overnight_loop_YYYY-MM-DD.sh`
- Şablon: `03_QUANTLENS/tools/overnight_loop_2026-06-01_sprint.sh` (referans)
- Zorunlu bileşenler:
  - `export MEGA_WORKERS=N` + `export MEGA_OUTPUT_DIR=...`
  - Deadline cap (NOW + Xs)
  - Heartbeat dosyası her iter sonu güncellenir
  - EC≠0 → auto-restart (10s sleep, log'a tail)
  - PASS → JSON + MD `overnight_runs/`'a kopyala (timestamped)
  - `[loop] === DEADLINE REACHED ===` final marker

### 6.3 Monitor tick (wakeup her 30dk)
```bash
cd 03_QUANTLENS/tools/overnight_runs
cat _heartbeat.json
tail -30 loop_*.log
ls -t MEGA_results_iter_*.json | head -3
ls -t v2_iter_*.log | head -1 | xargs tail -10
```
Anormallik (crashes≥3, heartbeat eski>60dk, disk %90+) → user'a uyar.

### 6.4 GECE SONU KAPANIŞ (zorunlu — her gece, loop DEADLINE sonrası)

Loop `=== DEADLINE ===` marker yazınca sırayla, **atlama yasak**:

1. **Aggregate** — `python aggregate_overnight_iters.py --runs-dir <night/sprint_runs> --out <runs>/AGGREGATE_<date>.json`
   - Robust winner eşiği `ceil(N*0.5)` (rules §13). Yan etki: iter JSON'ları `05_BACKTEST_RESULTS`'a `*_results.json` export edilir.
2. **Alpha vs buy&hold** — `MEGA_OUTPUT_DIR=<CLEAN 05_BACKTEST_RESULTS> python alpha_vs_buyhold.py` → `alpha_summary.json` (149/premium/down_market).
3. **Morning report** — `05_BACKTEST_RESULTS/MORNING_REPORT.md` üret (rules §10 format). A16 nedeniyle `generate_morning_report.py` legacy path okuyorsa raporu `alpha_summary.json` + `AGGREGATE_*.json` verisinden elle yaz.
4. **MTC Command Center upgrade (zorunlu)** — gece sonucu dashboard'da görünmeli:
   - Dashboard `backtest_reader.py` → `05_BACKTEST_RESULTS/*_results.json` glob okur. Adım 1'in export'u bunu besler.
   - **Doğrula:** `cd 08_DASHBOARD_APP/apps/api && python -c "from mcc_readonly.backtest_reader import build_backtest_status; from pathlib import Path; bs=build_backtest_status(Path('<MCC_ROOT>')); print(len(bs['runs']), bs['runs'][0]['run_id'])"` → run sayısı arttı + en yeni `MEGA_results_iter_<son>` COMPLETED görünüyor mu? Görünmüyorsa adım 1 export'u veya QuantLens root resolution'ı kontrol et.
5. **Lessons arşivi (zorunlu)** — gece tecrübelerini ilgili dosyaya yaz (runbook §11):
   - `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_<date>.md` yaz (özet + bulgular G1..Gn + aksiyon + artifact).
   - `lessons_archive/OVERNIGHT_LESSONS_INDEX.md`'e satır ekle.
   - Yeni anti-pattern → bu runbook §8 tablosuna (A-serisi). Yeni guideline → ilgili bölüme. CHANGELOG'a 1 satır.
6. **Handoff güncelle** — `GLOBAL_HANDOFF.md` (model+tarih başlık), `NEXT_STEPS.md` (AI-tag'li followup), `SESSION_LOG.md` (1 satır).
7. **Loop'u durdur** — reschedule yok. Kullanıcı uyuyorsa `PushNotification` ile tek satır sonuç.

> Kapanış 4 (dashboard) ve 5 (lessons) **birlikte** sabah teslimatının parçası. Sadece rapor yazıp bırakma — Command Center güncellenmemişse ve ders arşivlenmemişse gece **tamamlanmamış** sayılır.

---

## 7. RESUME / RECOVERY

### 7.1 MTC V2 BIG_OVERNIGHT için (resume_registry.sqlite)
- Var olan `--out` dizinine işaret et, yeni dizin AÇMA
- `evaluation_key` üzerinden duplicate skip
- `skipped_already_completed > 0` smoke kontrolü zorunlu
- Resume sonrası `ranked/all_evaluations.csv` slice kapsamlı mı doğrula (cumulative rerank gerekebilir)

### 7.2 QuantLens overnight için (mevcut state pickle YOK)
- Crash sonrası iter baştan başlar — Python pool stateless
- **Aksiyon:** `--resume <pickle>` desteği `NEXT_STEPS` A5'e eklendi
- Şimdilik: crash öncesi tamamlanan iter JSON'ları `overnight_runs/`'da kalır, aggregate analyzer onlardan yararlanır

### 7.3 Yarım iter veri kurtarma
- Mega'nın `[N/total] elapsed=Xs counts=...` her dakikalık print'i log'da → manuel re-construct mümkün ama zahmetli
- Tercih: iter sürelerini kısa tut (max 15dk hedefle 20 worker ile), kayıp riskini minimize et

---

## 8. SIK YAPILAN HATALAR (ANTI-PATTERN)

| # | Hata | Çözüm | Kaynak |
|---|---|---|---|
| A1 | OUTPUT_DIR legacy path, read-only, %94'te crash | `MEGA_OUTPUT_DIR` env override + CLEAN repo default | LESSONS_2026-06-01 B1 |
| A2 | Wakeup tek mekanizma, kopunca 4+ saat sessizlik | taskschd + wakeup BİRLİKTE (çift kanal) | LESSONS_2026-06-01 B2 |
| A3 | Crash = %94 hesap bellekte ölür | Smoke gate + iter süresini ≤15dk tut | LESSONS_2026-06-01 B3 |
| A4 | Heartbeat iter-arası → iter-içi sessizlik | Mega print'ini parse et, dakikalık hb | LESSONS_2026-06-01 B4 |
| A5 | Estimation 30× yanlış | Steady-state için 5dk smoke gözle | LESSONS_2026-05-31 #1 |
| A6 | Background loop wrapper yaşar, child'lar değişir | Wrapper PID takip et, sadece python kill etme | LESSONS_2026-05-31 #2 |
| A7 | Sandbox PermissionError'ları gerçek crash sanıldı | `dangerouslyDisableSandbox: true` MP komutlarda | LESSONS_2026-05-31 #3 |
| A8 | DSR p≥0.95 crypto'da imkansız | 0.50 research / 0.85 production | LESSONS_2026-05-31 #5 |
| A9 | Tek hücre survivor'a güven | Cross-symbol ≥5 hücre kuralı | LESSONS_2026-05-31 #6 |
| A10 | Eşzamanlı runner aynı OUTPUT_DIR'e yazar | Her isolated run subdir kullansın | LESSONS_2026-05-31 #2 |
| A11 | Unicode `▶` cp1254 codec crash | `sys.stdout.reconfigure(encoding='utf-8')` | LESSONS_2026-05-31 #11 |
| A12 | `--max-workers` 6 default outdated | MTC V2 için 16, asla 20+ | OPTIMIZATION_LESSONS_20260427 + BIG_OVERNIGHT |
| A13 | Codex/Claude UI terminal'inde uzun komut | Detached PowerShell runner (BIG_OVERNIGHT) | BIG_OVERNIGHT |
| A14 | İlk run veri çürür, resume yoksa baştan | resume_registry.sqlite + idempotent output dir | BIG_OVERNIGHT |
| A15 | Hardcoded path migration sonrası rotate edilmedi | `tools/audit_hardcoded_paths.py` (NEXT_STEPS A4) | LESSONS_2026-06-01 |
| A16 | `generate_morning_report.py` legacy hardcoded OUTPUT_DIR okuyor (A1 fix sıçramadı) | Raporu `alpha_summary.json` + `AGGREGATE_*.json` verisinden üret; generator'a env override ekle | LESSONS_2026-06-03 |
| A17 | Geniş search-space DSR power'ı öldürür (tüm aday p<0.50) | İki aşama: geniş discovery → dar pre-registered confirmation grid | LESSONS_2026-06-03 |
| A18 | Morning report down-market alpha yanlış sayım/etiket (rapor 78, log 8); down-market tablosu beat-b&h tablosunun kopyası | Sayıları alpha log `ALPHA_DONE` satırı ile assert; down-market tablosunu b&h<0 filtresinden üret. **FIXED 2026-06-05:** `write_overnight_morning_report.py` artık canonical `alpha_summary.json` (`down_market_alpha`/`premium`) okur + drift assert | LESSONS_2026-06-04 / 06-05 C2 |
| A19 | Deterministic confirmation run dar grid'i dakikada bitirir → makine gece boyu idle-awake watchdog'da bekler (boşa) | Determinizm yüzünden tekrar değer üretmez (seed=md5, mega:731). Idle wall-clock'u NON-identical ağır validasyona harca: 50k bootstrap, multi-seed DSR stability, CPCV-all-cells, ±2-step pre-registered grid, 4h/1D TF. Yoksa makineyi bırak (keep-awake yok) | LESSONS_2026-06-05 C4/C5 |
| A20 | `probabilistic_pbo` tam `C(n_splits, n_splits/2)` combo listesini `--max-combinations` slice'ından ÖNCE enumerate eder (pbo:63-68); derin CPCV (n_groups=10→44 split) → C(44,22)≈2T → MemoryError, cap işe yaramaz | PBO'yu standart 15-split CPCV'den besle (`cpcv15/`, C(14,7)=1716); derin 45-split CPCV'yi yalnız ek robustness tablosu olarak tut. Uzun vade: estimate_pbo capli iken lazy/random örnekleme | LESSONS_2026-06-05 A20 |
| A21 | Derin CPCV (45 split) DSR'ı KURTARMAZ — daha çok OOS split CPCV güvenini artırır ama DSR trial count = grid size (A17), split sayısı değil. Geniş 43-strateji discovery DSR'ı yine sıfırlar (72 hücrede 0 final) | Discovery'yi derinleştirme/genişletme; dar pre-registered confirmation grid'e geç (NIGHT-FOLLOWUP-002) | LESSONS_2026-06-05 C7 |

---

## 9. INTEGRATION POINTS

### 9.1 Bu runbook çağrı zinciri
`AGENTS.md` → "overnight backtest planlıyorsan bu dosyayı oku" satırı
`04_SHARED/prompts/05_ai_workflow/08_overnight_backtest_launch.md` → adım listesi bu dosyayı işaret eder
Her gece sonu: `OVERNIGHT_LESSONS_YYYY-MM-DD.md` yaz → `lessons_archive/`'e at → delta'yı bu runbook'a merge et

### 9.2 Diğer modellerle uyumluluk
- **Claude Code:** Bu dosyayı direkt okur (CLAUDE.md zaten AGENTS.md → START_HERE → bu dosyaya işaret edecek)
- **Codex:** AGENTS.md aynı pre-read zinciri
- **DeepSeek V4 Pro / Gemini:** İlk prompt'a "Read 11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md tamamen, sonra başla" ekle
- **Yeni model:** Aynı pattern. Bu dosya self-contained — cold start yeterli.

---

## 10. KAYNAK ARŞİVİ

Geçmiş tüm lessons (bu runbook'un kaynak materyali):

| Tarih | Dosya | Ana ders |
|---|---|---|
| 2026-04-27 | `01_MTC_PROJECT/docs/optimization/OPTIMIZATION_LESSONS_LEARNED_20260427.md` | Worker scaling benchmark, 16 sabit |
| 2026-05-01 | `01_MTC_PROJECT/reports/optimization/12h_backtesting_session/POST_RESUME_RESULT_AND_LESSONS_20260501.md` | Resume registry pattern, dedup verification |
| 2026-05-XX | `01_MTC_PROJECT/reports/optimization/worker_scaling_benchmark/WORKER_BENCHMARK_LESSONS_UPDATE_REPORT.md` | Thread pinning OMP/MKL/OPENBLAS/NUMEXPR |
| 2026-05-31 | `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_2026-05-31.md` | Estimation, DSR crypto kalibrasyon, monkey-patch, cross-symbol agg |
| 2026-06-01 | `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_2026-06-01.md` | OUTPUT_DIR legacy crash, wakeup zinciri kopması |

Legacy repo (`C:\LAB\tradingview-lab\`):
- `01_MASTER TEMPLATE_V2/docs/optimization/OPTIMIZATION_LESSONS_LEARNED_20260427.md` (mirror)
- `01_MASTER TEMPLATE_V2/MTC_V2_PORTABLE_HANDOFF/docs/optimization/...` (mirror)
- Yeni iş için legacy'e dokunma — freeze policy.

---

## 11. LIVING UPDATES

Bu dosya değiştirilir. Her gece sonu:
1. `OVERNIGHT_LESSONS_YYYY-MM-DD.md` yaz (ham gözlem)
2. `lessons_archive/` taşı
3. Yeni anti-pattern → bu dosya bölüm 8 tablosuna eklenir
4. Yeni guideline → ilgili bölüme merge
5. CHANGELOG bölümü buraya, son 5 değişiklik

### CHANGELOG
- 2026-06-05 (akşam) — Heavy-tier gece (Claude). Determinizm tuzağı baştan tanındı, loop-pad reddedildi. İlk 43-strateji enriched sweep (3655 hücre, 72 PASS+), 3× derin CPCV (45 split, 24 hücre ≥0.80), PBO=0.0, Gate2 53 PASS/19 FAIL, scorecard_v2 promotable 0 (Gate3 INCOMPLETE). **C7/A21:** derin CPCV DSR'ı kurtarmıyor (Gate2∧CPCV≥0.80∧DSR≥0.50 = 0/72). A20 (PBO OOM derin CPCV'de) + C8 (alpha short-trap) eklendi. Çıktı: `05_BACKTEST_RESULTS/heavy_tier_2026-06-05/`. LESSONS_2026-06-05.
- 2026-06-05 — Confirmation (Option B) gece: dar pre-registered grid DSR power'ı geri getirdi (en iyiler 0.0→0.34-0.38) ama hiçbir aday 0.50 eşiğini geçmedi → `STATISTICALLY_UNCONFIRMED`. A18 morning-report fix doğrulandı (down_market=6 == ALPHA_DONE). A19 eklendi (deterministic run idle-awake israfı). Determinizm mekanizması belgelendi (md5 seed, mega:731): tekrar = sıfır bilgi. LESSONS_2026-06-05.
- 2026-06-04 — Added MTC-Engine Validation operational stage: light-risk profile, manual producer adapters, bridge CLI, report/artifact contract, and raw-signal parity limitation.
- 2026-06-04 — Overnight 20-iter 2. sıfır-crash gece (3.44M eval, Codex çalıştırdı). A18 (morning report down-market yanlış sayım) eklendi. Gece-sonu konvansiyonu Codex tarafından atlanmıştı, ertesi sabah elle tamamlandı. LESSONS_2026-06-04.
- 2026-06-03 — Overnight 21-iter sıfır-crash gece. A16 (morning generator legacy path) + A17 (DSR search-space inflation → confirmation grid) eklendi. LESSONS_2026-06-03.
- 2026-06-01 — İlk konsolidasyon. 5 ayrı runbook + 3 lessons dosyası sentezi. B1-B5 + A1-A15 eklendi.
