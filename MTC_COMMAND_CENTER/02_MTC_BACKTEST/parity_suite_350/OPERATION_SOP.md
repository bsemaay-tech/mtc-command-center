# MTC Parity Suite - Operation SOP (v2, Clean Restart)

## 1) Objective
MTC (Pine) ve `mtc_backtest` (Python) parity kontrolunu sifirdan, tek bir baseline referansi uzerinden, tekrar etmeyen ve dependency-aware case seti ile yapmak.

## 2) Hard Rules (Non-Negotiable)
1. Sabit case hedefi yok (`350` zorunlu degil). Gerekli coverage kadar case uretilir.
2. UI'da degistirilebilen, davranisa etkili her ayar en az 1 kez aktif etkide test edilir.
3. UI'da degistirilemeyen gomulu ayarlar icin case uretilmez.
4. Sadece Python tarafinda (Codex-run internal) degisen ayarlar icin case uretilmez.
5. Baseline ile ayni case uretilmez.
6. Birbiriyle semantik olarak ayni case uretilmez (strict dedupe).
7. Trade list ve metrik karsilastirmasindan once `Properties` setup parity zorunludur.
8. Ongoing live operation icin historical freeze count (`240`) kullanilmaz; current downloaded baseline XLSX authoritative kaynaktir.

## 3) Baseline Freeze (Phase-0 Gate)
Phase-1, asagidaki baseline kaydi tamamlanmadan baslamaz:
- `baseline_case_id`
- TV source XLSX:
  `mtc_backtest/parity_suite_350/manifests/baseline_sources/baseline_tv_export_FILLED_v6.xlsx`
- Symbol, timeframe, trading range, backtest range
- Pine script version/tag
- Python commit hash
- Frozen baseline JSON snapshot
- Historical freeze record:
  `manifests/baseline_freeze_record.json -> tv_metrics_snapshot.total_trades = 240`

Current live operation note:
- Historical freeze record retained for audit history only.
- Current live source-of-truth baseline is the downloaded XLSX under:
  `mtc_backtest/parity_suite_350/tv_manual_inputs/001_parity_core_005_enable_long_trades_v01/`
- Current verified live parity count: `241`

## 4) Case Design Rules
1. Case paketleri: `core`, `boundary`, `pairwise`.
2. Her case tek test niyeti tasir.
3. Pairwise sampling gerekiyorsa deterministic calisir: `RANDOM_SEED=42`.
4. Dedupe iki katmanli yapilir:
   - `canonical_config_hash`: sadece aktif, davranisa etkili alanlar
   - `semantic_fingerprint`: test niyeti + aktif parametre kombinasyonu
5. Parent-off oldugunda child parametreler hash/fingerprint disina atilir.

## 5) Dependency Matrix (Mandatory)
`case_rules.json` zorunludur; koddan dogrulanir (`defaults.py`, `mtc_runner.py`).
Asgari bagimliliklar:
- `exit_if_selected_filter_blocks_while_in_position=false` ise Exit Trigger Filter Block altindaki child filtre case'leri inerttir.
- `use_time_stop=false` ise `exit_end_of_day`, `exit_end_of_week`, `time_stop_bars`, `time_stop_condition` inerttir.
- `signal_mode != Supertrend` ise Supertrend alt ayarlari inerttir.
- `signal_mode != Range Filter Hybrid` ise Range Hybrid alt ayarlari inerttir.
- `signal_mode == None` ise `ZERO_TRADE_EXPECTED`.
- `use_daily_loss_limit=false` ise `max_daily_loss_pct` inerttir.
- `use_max_trades_per_day=false` ise `max_trades_per_day` inerttir.
- `use_stop_loss=false` ise tum SL mode/SL params inerttir.
- `sl_mode != ATR` ise ATR SL params inerttir (diger SL mode'larda da ayni parent-child kurali gecerlidir).
- `use_tp=false` ise TP mode ve TP params inerttir.
- `use_multi_tp=true` ise single TP path override edilir; single TP case'i icin once multi TP kapatilir.
- Break-even ve trailing icin parent-off => child inert.
- MACD Filter Hub secili degilse MACD alt modlari inert.
- Confirmation secili degilse confirmation alt ayarlari inert.
- Range & Volatility Entry Pause secili degilse alt range filtreleri inert.
- Entry Pause mode `COUNT` ise `minimum_pass_count` zorunludur.
- Hicbir guard aktif degilse `use_guard_recovery` etkisizdir.
- `use_guard_recovery=false` ise recovery mode child'lari inerttir.
- Time-stop/timeframe logical incompatibility case generator'da `exclude_when` ile engellenir.

## 6) TV Collection Model
Manual hatayi azaltmak icin:
1. User-friendly takip dosyasi zorunlu:
   - `CASE_SETUP_GUIDE.xlsx`
   - `scripts/build_case_setup_guide.py` ile manifestten uretilir/guncellenir
   - TV tarafinda hangi ayarin degisecegi, case folder, XLSX indirme durumu ve setup dogrulama durumu bu dosyadan takip edilir.
   - Bu dosya, manuel toplama sirasinda tek source-of-truth'tur.
2. Tum TV export XLSX dosyalari:
   `mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/`
3. `scripts/route_tv_xlsx.py`:
   - `Properties` sekmesini parse eder
   - manifest beklenen config ile eslestirir
   - eslesen dosyayi `tv_manual_inputs/{run_order}_{case_id}/` altina tasir
   - eslesmeyeni `tv_manual_inputs/unmatched/` altina alir
   - `CASE_SETUP_GUIDE.xlsx` icinde ilgili case satirinin XLSX status kolonlarini gunceller
4. Cikti:
   - `manifests/tv_collection_status.csv`
   - `manifests/tv_unmatched.csv`

## 7) Python Execution + Safety
1. Run order: `core -> boundary -> pairwise`
2. Case-level hata olursa devam edilir.
3. Circuit breaker: ardisik `5` case exception olursa batch durur.
4. Her case icin:
   - `metrics.json`
   - `trades.csv`
   - (`signals.csv` opsiyonel)
5. Live parity status mutlaka compare-run markdown/csv ile yazili hale getirilir; yeni sohbet/handoff bu dosyalar uzerinden devam eder.

## 8) Comparison Rules (TV vs Python)
Karsilastirma sirasi:
1. Setup parity (`Properties` vs case JSON)
2. Trade count
3. Trade-level matching
4. Aggregate metrics
5. Zorunlu cift gorunum:
   - `raw strict` (tum horizon)
   - `clip-overlap strict` (ortak pencere)

Default tolerances:
- `time_tolerance_bars = 0`
- `price_tolerance = 0.01 * mintick`
- aggregate metric tolerance = `0` (case bazli override yoksa exact)

Status kurallari:
- `PASS`: tum kontroller gecer
- `SETUP_MISMATCH`: setup parity fail
- `MISMATCH`: setup dogru ama output farkli
- `NO_TRADE_EXPECTED_PASS`: sadece case `ZERO_TRADE_EXPECTED` ve TV=0/Python=0 ise
- `ERROR`: parser/execution crash

Cift raporlama notu:
- Pipeline notlarinda hem `clip=PASS/FAIL` hem `raw=PASS/FAIL` yazilir.
- `clip=PASS` ve `raw=FAIL` olursa, case `TV_EARLY_TRADE_END_CANDIDATE` olarak etiketlenir (gap-days ile birlikte) ve workbook `notes` kolonuna otomatik islenir.
- Tracker zorunlu kolonlari:
  - `compare_status` (kanonik karar, raw strict)
  - `clip_strict_status`, `raw_strict_status`
  - `early_trade_end_candidate`, `gap_days`
  - `clip_tv_trades`, `clip_py_trades`, `raw_tv_trades`, `raw_py_trades`

## 9) Unified Mismatch Taxonomy
Tek bucket sistemi:
- `SETUP`
- `DEPENDENCY_MODEL`
- `MISSING_TRADES`
- `EXTRA_TRADES`
- `TIMING`
- `PRICE_PNL`
- `EXIT_REASON`
- `UNKNOWN`

## 10) Correction Loop
1. Bir bucket sec
2. Root cause bul
3. Patch uygula
4. Affected case rerun
5. Core smoke rerun
6. Closure note yaz
7. README + handoff note guncelle

## 11) Exit Criteria
1. Core package `100% PASS`
2. Total PASS `>=95%`
3. Acik `P0/P1` mismatch kalmamis olmali
4. Final ciktilar:
   - `FINAL_PARITY_REPORT.md`
   - frozen baseline record
   - suite freeze record
