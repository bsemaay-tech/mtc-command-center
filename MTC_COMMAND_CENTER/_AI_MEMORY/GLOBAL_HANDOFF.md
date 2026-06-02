# GLOBAL_HANDOFF

Last updated: 2026-06-02 (dashboard entegrasyon UYGULANDI + doğrulandı)
Updated by: Claude Opus 4.8
Active project: TradingView-LAB / MTC Command Center
Current objective: Dashboard'u sprint_runs sonuçlarına bağla (Option B). — DONE
Current phase: Uygulama bitti. Backtest sekmesi MEGA sonuçlarıyla doluyor (32 run, doğrulandı).
Current blockers: (none)

## Claude Opus 4.8 2026-06-02 — "Dashboard açılmıyor" fix

Kök neden: bare `python -m mcc_readonly` (step 5'in söylediği komut) argparse `required=True` subcommand yüzünden exit 2 veriyordu ("the following arguments are required: command"). Doğru komut `serve` idi → kullanıcı "açılmıyor" gördü.
Fix:
- `cli.py` — subparsers `required=False`. Komut yoksa otomatik `serve` (127.0.0.1:8765) + `webbrowser.open(/dashboard)`.
- Yeni `08_DASHBOARD_APP/START_DASHBOARD.bat` — çift tık launcher (apps\api'ye cd + bare modül + pause).
Doğrulama: py_compile PASS; bare invocation serve OK; `GET /dashboard` HTTP 200.

## Claude Opus 4.8 2026-06-02 — Dashboard ↔ MEGA entegrasyonu (Option B UYGULANDI)

Plan uygulandı + canlı doğrulandı. 5 adım:
1. `00_CONFIG/paths.local.json` oluşturuldu (mcc_root=.../MTC_COMMAND_CENTER, mtc_v2_root=C:/LAB/Tradingview_LAB_CLEAN, reports_root). Zaten `MTC_COMMAND_CENTER/.gitignore:3` ile ignore'lu → commit edilmez.
2. `03_QUANTLENS/05_BACKTEST_RESULTS/` zaten vardı (oluşturmaya gerek yok).
3. `aggregate_overnight_iters.py` — `export_to_backtest_results()` eklendi. sprint_runs MEGA JSON'larını `05_BACKTEST_RESULTS/`'a `{stem}_results.json` adıyla KOPYALAR (reader glob `*_results.json` ile eşleşsin diye rename şart). Mevcut mantığa dokunulmadı. Çıktı: "Exported 16 files to 05_BACKTEST_RESULTS".
4. `single_strategy_backtest.py` — workflow sonuna non-fatal aggregate hook eklendi (`--runs-dir sprint_runs`). Başarılı → "Dashboard updated".

**KÖK NEDEN DÜZELTMESİ (plan dışıydı, gerekti):** `backtest_reader.py` `mtc_v2_root/06_QUANTLENS_LAB/05_BACKTEST_RESULTS` HARDCODE ediyordu — bu dizin CLEAN repo'da YOK. Plan'ın "reader zaten okuyabiliyor" varsayımı yanlıştı (format uyumlu, ama dizin değil). `registry_reader.py:21` zaten doğru pattern'i kullanıyor: `default_quantlens_root(root)` (03_QUANTLENS tercih, 06 fallback). `backtest_reader.py` aynı pattern'e çevrildi (`_collect_quantlens_results` + `_collect_detached_statuses` artık quantlens_root alıyor). Tek outlier oydu — diğer reader'lar dokunulmadı.

**Doğrulama (canlı):**
- py_compile PASS (2 script)
- `aggregate --runs-dir sprint_runs` → 16 iter, 149 robust winner, 16 export
- `build_backtest_status()` → 32 run, 16 MEGA surfaced, matrix format parse OK (3655 evals)
- `python -m mcc_readonly snapshot` → backtest_status.summary total_runs=32, source=C:/LAB/Tradingview_LAB_CLEAN
- HTTP `serve --port 8770` + `GET /api/snapshot` → 32 run, last=MEGA_results_iter_13. Server kapatıldı.

**Değişen dosyalar:** `00_CONFIG/paths.local.json` (yeni, ignored), `03_QUANTLENS/tools/aggregate_overnight_iters.py`, `03_QUANTLENS/tools/single_strategy_backtest.py`, `08_DASHBOARD_APP/apps/api/mcc_readonly/backtest_reader.py`. Export JSON'lar (`05_BACKTEST_RESULTS/MEGA_*_results.json`) gitignore'lu — repo bloat yok. Henüz commit EDİLMEDİ (kullanıcı onayı bekliyor).

## Claude Sonnet 4.6 2026-06-02 — Sabah oturumu (Loop tamamlandı + Dashboard analizi)

### MEGA Overnight Loop — TAMAMLANDI
- 16 iter başarılı: 3 sprint + 13 gece (2026-06-01 23:36 → 2026-06-02 06:33)
- **149 robust winner** (≥8/16 iter PASS) — dün sabah 117 idi (+32)
- 16/16 STRONG çift: `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY/TRXUSDT/2h` (ret%101, PF=1.82), `QL_DEEPAK_153_FILTER_1D/SOLUSDT/2h` (ret%56, PF=1.70)
- Aggregate çalıştırıldı → `03_QUANTLENS/tools/OVERNIGHT_AGGREGATED_REPORT.md`
- 17 JSON sprint_runs'ta: `MEGA_results_iter_1..13_*.json`

### Dashboard Bağlantı Sorunu — TESPİT EDİLDİ, FIX PLANLI
Dashboard (08_DASHBOARD_APP) Audit ve Pipeline sekmelerinde gece sonuçları GÖRÜNMÜYOR.
Kök neden 3 katmanlı:
1. `paths.local.json` YOK → dashboard `paths.example.json`'daki eski `C:/LAB/tradingview-lab/` path'ini kullanıyor (silinmiş dizin)
2. `backtest_reader.py` → `mtc_v2_root/06_QUANTLENS_LAB/05_BACKTEST_RESULTS/` okuyor (eski path)
3. MEGA sonuçları `sprint_runs/` altında — dashboard bilmiyor

**Onaylanan Fix Planı (Option B):**
Yeni oturumda yapılacaklar:
1. `paths.local.json` oluştur → doğru `C:/LAB/Tradingview_LAB_CLEAN/` path'i ver
2. `aggregate_overnight_iters.py` → sonunda MEGA JSON'larını `03_QUANTLENS/05_BACKTEST_RESULTS/` 'e kopyala
3. `single_strategy_backtest.py` → bitince aggregate'i otomatik çağır
4. Dashboard yeniden başlatınca Audit/Pipeline güncel veri gösterir

**Gerekli dosyalar:**
- `00_CONFIG/paths.local.json` (yeni, oluşturulacak)
- `03_QUANTLENS/tools/aggregate_overnight_iters.py` (değiştirilecek — export adımı eklenecek)
- `03_QUANTLENS/tools/single_strategy_backtest.py` (değiştirilecek — post-run aggregate hook)
- `03_QUANTLENS/05_BACKTEST_RESULTS/` (yeni dizin, oluşturulacak)

**Bağlamlar (yeni oturumda lazım):**
- `backtest_reader.py` `_is_matrix_walk_forward()`: `results` listesindeki her dict'te `classification` + `summary` (dict) varsa MEGA formatı tanıyor → MEGA JSON'lar doğrudan okunabilir, format uyumlu
- `paths.example.json` içeriği: `mtc_v2_root = C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2` → GEÇERSİZ
- Doğru path: `C:/LAB/Tradingview_LAB_CLEAN`

## Claude Sonnet 4.6 2026-06-02 — LLM Audit Fixes

Multi-model audit (ChatGPT 5.5 / DeepSeek V4 Pro / Grok Build 01 / Antigravity) incelendi.
**Fixed this session:**
- `aggregate_overnight_iters.py:148,164` — `or 1` → explicit `is None` check (0.0 p-value inversion fix)
- `mega_walk_forward.py:698` — `hash()` → `hashlib.md5()` deterministic bootstrap seed
- `mega_walk_forward.py:708` — PASS threshold `n_folds // 2` → `math.ceil(n_folds / 2)`
- `mega_walk_forward.py:653,690` — tuple direction detection: `result[2] in {"long","short"}` guard
- `audit_hardcoded_paths.py:31` — SKIP_DIRS'e `single_strategy_runs`, `cpcv_runs`, `pbo_runs` eklendi
- `.gitignore` — 5 run output dizini eklendi (`overnight_runs`, `sprint_runs`, `single_strategy_runs`, `cpcv_runs`, `pbo_runs`)
- `mega_walk_forward.py:523` — short R-multiple işareti (önceki oturum)
- `mega_walk_forward.py:778` — `_atomic_write_text` mkdir guard (önceki oturum)
- `ingest.py:30` — `EMBEDDED_TRANSCRIPT_MIN_SIZE` 500→5000 regression fix (önceki oturum)

Later same session — Mimo v2.5 Free audit (10 run) incelendi:
- `audit_reader.py` duplicate `_lookup_source_record` (419+872 byte-identical) → ikinci silindi
- AUDIT-008 (rolling fold OOS 113-bar overlap), AUDIT-009 (bars_per_day=78 crypto), AUDIT-010 (ingest transcript re-write race) eklendi
- Mimo false positives doğrulandı: DSR `cdf` doğru (sf değil), MEGA_WORKERS env cap'i atlıyor — bunlar fix edilmedi (gerçek değil)

**Open audit items → NEXT_STEPS.md AUDIT-001..AUDIT-010**

## Claude Sonnet 4.6 2026-06-02 — Overnight session (T-01..T-08)

### T-04 MEGA Overnight Loop
- `overnight_loop_2026-06-01_night.ps1` oluşturuldu ve başlatıldı (PID 34672)
- Deadline: 2026-06-02 06:00, 20 worker, MEGA_OUTPUT_DIR doğru
- Log: `overnight_runs/night_loop_2026-06-01.log`

### T-01 Buy & Hold Baseline
- `buy_hold_baseline.py` yazıldı → `sprint_runs/BH_BASELINE.md`
- **Kritik bulgu:** 189 ROBUST hücreden **117/189 pozitif alpha** (B&H'yi geçiyor)
- 72 hücre FAIL: TRXUSDT (+107.7% B&H) ve XRPUSDT (+124.8% B&H) bull market döneminde
- SOLUSDT, ETH, BNB, LINK gibi düşen semboller → strateji alpha'sı yüksek

### T-02 CPCV + PBO Gate
- `sprint_runs/cpcv_input_top_alpha.json` — 13 top alpha hücre filtrelendi
- CPCV: `cpcv_runs/top_alpha/CPCV_VALIDATION_REPORT.md`
- PBO: `pbo_runs/top_alpha/PBO_REPORT.md` — **PBO=0.0** (sıfır overfitting)
- `QL_DEEPAK_153_FILTER_1D SOLUSDT 2h` 3003 CPCV kombinasyonun hepsini kazanıyor

### T-03 Promotion Assessment
`sprint_runs/PROMOTION_ASSESSMENT_2026-06-01.md` — Barış onayına:

| Öneri | Strateji | Sembol/TF | CPCV | Excess |
|---|---|---|---|---|
| **ELITE** | SP500_TWO_CANDLE_SENTIMENT_SR | ADAUSDT 1h | 14/15 (93%) | +109.7% |
| **ELITE** | 8EMA_EXIT_TRAIL | LINKUSDT 1h | 14/15 (93%) | +96.0% |
| **ELITE?** | DEEPAK_153_FILTER_1D | SOLUSDT 2h | 14/15 (93%) | +121.2% |
| **STRONG** | OPEN_RANGE_5PCT_STOP | NEARUSDT 4h | 13/15 (87%) | +144.4% |
| **STRONG** | CANDLESTICK_7_PA_CONFLUENCE | APTUSDT 1h | 12/15 (80%) | +110.9% |
| **STRONG** | DEEPAK_153_FILTER_1D | ETHUSDT 2h | 12/15 (80%) | +74.1% |

### T-05 QQE Salvage
- `overnight_v2_runner.py` → `QL_QQE_SIGNALS` (strateji 43, grid 108 param)
- SOLUSDT 2h: fold +53.9% avg, lockbox -14.7% → **FILTER_OVERLAY** (overfitting)
- `03_SALVAGE_IDEAS/.../06_next_action.md` güncellendi

### T-07 SP-001 MVP-0 CLI Skeleton
- `mtc_cli/` oluşturuldu (sadece bu klasör, Pine/MTC'ye dokunulmadı)
- Dosyalar: `__main__.py`, `contract.py`, `commands/audit.py`, `tests/test_audit.py`
- Komut: `python -m mtc_cli audit repo [--json]`
- **8/8 test PASS**

### T-08 SP-002 vectorbt Enrichment
- `03_QUANTLENS/tools/vbt_enrichment.py` oluşturuldu
- API: `enrich_from_trades(tv_trades, price_df)` + `enrich_from_mega_result(lockbox_oos)`
- Metrikler: Calmar, Sortino, Omega, rolling Sharpe, underwater equity, Monte Carlo
- Smoke: DEEPAK_153 SOLUSDT 2h → Calmar=3.70, Sortino=11.63, Omega=1.63

### Sabah Yapılacaklar (Barış)
1. MEGA loop sonuçlarını aggregate: `python aggregate_overnight_iters.py --runs-dir sprint_runs`
2. B&H güncelle: `python buy_hold_baseline.py --sprint-dir sprint_runs`
3. Promotion kararları: `sprint_runs/PROMOTION_ASSESSMENT_2026-06-01.md` oku
4. 31 transcript kandidat review: `11_TRIAGE/reclassification_audit_2026-06-01.md`

## 2026-06-01 Codex sequential task run

- **IM-001 complete:** `11_TRIAGE/analyze_transcripts.py` now resolves transcript paths via the current QuantLens root before falling back to legacy paths. Verified `00_INBOX_REPORTS/Transcrips` resolves to `MTC_COMMAND_CENTER/03_QUANTLENS/...`; `py_compile` PASS.

## 2026-06-01 DeepSeek V4 Pro transcript follow-up

- **IM-001 verification + basename fallback:** Ran `analyze_transcripts.py` — initial run resolved 98/165 transcripts (67 had legacy `06_QUANTLENS_LAB\` prefix in stored path, not matching migrated `03_QUANTLENS/00_INBOX_REPORTS/Transcrips/` location). Added basename-based fallback to `resolve_transcript_path()` — searches `Transcrips/` and `00_INBOX_REPORTS/Transcrips/` by filename. Re-run: **165/165 analyzed, 0 missing.**
- **Audit results (2026-06-01):** 115 ALREADY_OK, 17 LIKELY_MISCLASSIFIED, 14 REVIEW_HUMAN, 19 KEEP_REJECTED, 0 SPLIT_RECOMMENDED. Reports: `11_TRIAGE/reclassification_audit_2026-06-01.md`, `split_candidates_2026-06-01.md`.
- **Actionable:** 17 LIKELY_MISCLASSIFIED + 14 REVIEW_HUMAN need Barış manual review. 19 KEEP_REJECTED have no numeric thresholds → correctly rejected.
- **UI integration (transcript verdict in Audit tab):**
  - `analyze_transcripts.py` now writes `11_TRIAGE/transcript_reclassification.json` (candidate_id → verdict + signals mapping).
  - `read_model.py` loads this JSON into the dashboard snapshot as `transcript_reclassification`.
  - `index.html`: added "Transcript" column to Audit table, "Tx verdict" filter dropdown.
  - `app.js`: `renderAudit()` shows verdict badge per row + verdict counts in summary. `filterAuditRows()` supports transcript verdict filter.
  - Verified: server at `http://127.0.0.1:8765/dashboard` → Audit tab shows transcript verdict column.
- **Q Trend split + backtest + classification:** `QL_2026-05-01_TV_BUYSELL_INDICATOR_PACK`'ten Q Trend (Tosenko) ayrıştırıldı.
  - **Pine → Python:** `overnight_v2_runner.py` — `_qtrend_signal()` (iteratif Pine trend line) + `_compute_adx()` + 3 grid builder + 3 signals_new branch.
  - **Motor upgrade:** `mega_walk_forward.py` `simulate_slice()` short desteği eklendi (`direction="long"/"short"`). `_worker` 3-tuple `(sig, stop, direction)` dönüşü destekler.
  - **Multi-symbol backtest (4 sym × 3 varyant, 1h):**
    - V1 Long: ETHUSDT +110.7% lockbox ama cross-symbol tutarsız → FAIL
    - V1 Short: SOLUSDT +70.8% lockbox ama fold'lar negatif → FAIL
    - V2 Strong+ADX: SOLUSDT +9.2% ama trade < 30 → INSUFFICIENT_TRADES
  - **Final classification: FILTER_OVERLAY** — standalone edge yok, confirmation/guard filter olarak kullanılabilir. Salvage dosyası güncellendi: `03_SALVAGE_IDEAS/QL_2026-05-01_TV_BUYSELL_INDICATOR_PACK/` (triage, metadata, next_action).
  - Diğer 4 indikatör (QQE, UT Bot, Pivot SuperTrend, Lorentzian) SALVAGE_ONLY — henüz split edilmedi.
  - **Artifact'lar:** `single_strategy_runs/qtrend_optimize/`, `qtrend_short_v2/`, `qtrend_strong/`
- **Modified files:** `11_TRIAGE/analyze_transcripts.py`, `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`, `08_DASHBOARD_APP/apps/web/index.html`, `08_DASHBOARD_APP/apps/web/app.js`, `03_QUANTLENS/tools/overnight_v2_runner.py`, `03_QUANTLENS/tools/mega_walk_forward.py`, `03_QUANTLENS/03_SALVAGE_IDEAS/QL_2026-05-01_TV_BUYSELL_INDICATOR_PACK/*`, `_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`.

- **IM-002 complete:** added `03_QUANTLENS/tools/audit_hardcoded_paths.py` and wired `09_DOCS/hooks/protected_paths_hook.py` to run it on staged code-like files. Verification: `py_compile` PASS; staged audit PASS; full default audit reports 2,488 existing legacy references after generated-result dirs are skipped.
- **Sprint aggregation complete:** `aggregate_overnight_iters.py` now accepts `--runs-dir` and `--out`; sprint JSONs aggregated to `03_QUANTLENS/tools/sprint_runs/SPRINT_AGGREGATED_REPORT.md`. Result: 3 iters, 189 PASS cells, robust threshold corrected to `ceil(50%)` = 2/3.
- **IM-003 complete:** `mega_walk_forward.py` now supports `--resume <pickle>`, `--checkpoint-every N`, atomic checkpoint pickle writes, partial JSON writes, completed-job skipping, and atomic final JSON replace. Verification: `py_compile` PASS; synthetic checkpoint save/load + partial JSON helper PASS. Full engine run not executed.
- **IM-004 complete:** `mega_walk_forward.py` writes minute-level progress heartbeat from the same event that prints `[done/total] elapsed=... counts=...`; loop scripts pass heartbeat context via `MEGA_HEARTBEAT_*`. Verification: `py_compile` PASS; synthetic heartbeat JSON helper PASS. `bash -n` unavailable in this Windows shell, so shell syntax was not machine-checked.
- **IM-005 complete:** ran `register_overnight_monitor.ps1`; Windows scheduled task `MCC_Overnight_Monitor` registered successfully and is `Ready`.
- **IM-006 complete:** added `03_QUANTLENS/tools/cpcv_validator.py` and added a CPCV Gate to `07_BACKTEST_AND_OPTIMIZATION_RULES.md`. Smoke: 2 sprint candidates, 4 groups, 1 test group, V2 monkey-patch enabled; report at `03_QUANTLENS/tools/cpcv_runs/smoke/CPCV_VALIDATION_REPORT.md`.
- **IM-007 complete:** added `03_QUANTLENS/tools/probabilistic_pbo.py` and added a PBO Gate to the rules. Smoke used CPCV smoke artifact and wrote `03_QUANTLENS/tools/pbo_runs/smoke/PBO_REPORT.md`; PBO smoke value 0.0 is only tool verification.
- **IM-008 complete:** added `03_QUANTLENS/tools/single_strategy_backtest.py` and MEGA filters `--strategy/--symbol/--tf`. Smoke run: `QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK BTCUSDT 4h`, output `03_QUANTLENS/tools/single_strategy_runs/smoke_IM008/`.
- **IM-009 complete:** added `03_QUANTLENS/tools/data_check.py` with `verify_actual_range(symbol, tf)` and CLI; `single_strategy_backtest.py` now imports it. Verification: BTCUSDT 4h data check PASS; single-strategy smoke rerun output `single_strategy_runs/smoke_IM009/`; final `py_compile` PASS.

## 2026-06-01 sprint result (overnight 23:29 → 06:33 + 1h sprint)

- **Overnight 2-worker loop (23:29 → 04:06):** 3 iter crash, 0 JSON kayıt. Kök neden: `mega_walk_forward.py:37` `OUTPUT_DIR` legacy frozen path (`C:\LAB\tradingview-lab\...`) read-only. ~5.5h hesaplama veri kaybı.
- **Fix applied 04:06:** `MEGA_OUTPUT_DIR` env override + CLEAN repo default → `03_QUANTLENS/05_BACKTEST_RESULTS/`. Mega_walk_forward.py:37-42 + :742-746 (env reads).
- **Sprint 20-worker loop (05:46 → 06:46):** 3 başarılı iter (~15dk/iter). 0 crash. JSON kayıt OK.
  - `sprint_runs/MEGA_results_iter_1_20260601_054633.json` (4.6MB)
  - `sprint_runs/MEGA_results_iter_2_20260601_060216.json`
  - `sprint_runs/MEGA_results_iter_3_20260601_061755.json`
  - Iter 4 yarıda kesildi (kullanıcı kapatma talebi).

## Workflow konsolidasyonu (en önemli)

Önceki sessions'da overnight workflow her seferinde sıfırdan icat ediliyordu. Bu seansta:

### Canonical chain (HER backtest için, in-day single dahil)
1. `AGENTS.md` → iki dosya pre-read zorunlu
2. `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` ← **canonical 299 satır** (4 gate, classification, promotion, antigravity, MORNING_REPORT format)
3. `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` ← **operasyonel** (tool komutları, worker, monitor, anti-pattern arşivi)
4. `04_SHARED/prompts/05_ai_workflow/08_backtest_launch.md` ← Gate 0-G7 prompt (in-day single / sprint / overnight üç senaryo)
5. `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_INDEX.md` ← arşiv

### Wired files (bu seansta değişen)
- `AGENTS.md` — iki dosya pre-read satırı eklendi
- `_AI_MEMORY/START_HERE.md` — aynı zincir
- `04_SHARED/prompts/05_ai_workflow/00_index.md` — 08 satırı in-day dahil edilecek şekilde güncellendi
- `04_SHARED/prompts/05_ai_workflow/08_backtest_launch.md` — rename + üç senaryolu Gate 1.5
- `03_QUANTLENS/tools/mega_walk_forward.py` — OUTPUT_DIR + MEGA_WORKERS env override
- `03_QUANTLENS/tools/monitor_overnight.ps1` (yeni) — taskschd health monitor
- `03_QUANTLENS/tools/register_overnight_monitor.ps1` (yeni) — admin kurulum
- `03_QUANTLENS/tools/overnight_loop_2026-06-01_sprint.sh` (yeni) — 20-worker 1h sprint şablon
- `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` (yeni) — operasyonel runbook
- `11_TRIAGE/lessons_archive/` (yeni klasör) — arşiv + INDEX
- `_AI_MEMORY/NEXT_STEPS.md` — IM-001..IM-009 eklendi (CPCV, PBO, in-day script, data_check, vs)

## DeepSeek/Codex "ne yapacaksın" testi

Akşam herhangi bir model (Claude / DeepSeek V4 Pro / Codex / Gemini) "backtest iş akışım ne" sorulduğunda:
1. AGENTS.md okur (root) → pre-read zorunlu iki dosya görür
2. RULES okur → 4 gate + buy&hold + classification + promotion
3. RUNBOOK okur → in-day/sprint/overnight senaryo seçer + tool komutları
4. prompt 08 okur → Gate 0-G7 sırası

Üç farklı modelin yanıtı aynı içeriği vermeli. Tetik kelimeler: "backtest", "optimization", "walk-forward", "overnight".

Where to continue:
  - 17 LIKELY_MISCLASSIFIED + 14 REVIEW_HUMAN candidates need Barış manual transcript review. See `11_TRIAGE/reclassification_audit_2026-06-01.md`.
  - Sprint results (3 JSON) already aggregated to `03_QUANTLENS/tools/sprint_runs/SPRINT_AGGREGATED_REPORT.md`.
  - Side project SP-001 parked.
  - If asked "backtest workflow": cevap canonical chain'den okunmalı, **reinvention yasak**.
Warnings:
  - SP-001 plan in NEXT_STEPS is intent, not contract. Repo may have moved
    by scaffold time — re-check first.
  - Gate 5 (cross-model adversarial review) is discipline-only, no hook
    enforcement. Implementer must explicitly hand off to a different model
    (Codex or Gemini) for review.
  - Hard safety rules (AI_RULES.md): no Pine/MTC/parity edits without
    explicit Barış approval; no live trading; no destructive git ops; no
    `--no-verify`.
