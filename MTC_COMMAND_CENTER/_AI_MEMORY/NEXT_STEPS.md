# NEXT_STEPS

## MTC-Engine Validation step (2026-06-04)

### MEV-001 | OPEN | Spec review + implementation plan [AI: Claude | Barış onayı]
- Spec hazır: `docs/superpowers/specs/2026-06-04-mtc-engine-validation-step-design.md`.
- Barış spec'i okuyup onaylayınca → writing-plans skill ile fazlı uygulama planı.
- Amaç: shortlist producer'ı MTC risk motoruyla (SL/TP/trailing, filtre OFF) test eden
  yeni funnel halkası. All-additive, MTC_V2.pine'a dokunmaz.

## Immediate — Sabah Görevleri (2026-06-03)

### NIGHT-2026-06-03 | DONE | 21-iter overnight sweep + morning report [Claude]
- 21 iter / 0 crash / ~3.6M param-eval. Rapor: `05_BACKTEST_RESULTS/MORNING_REPORT.md`.
- 149 robust PASS, 89 beat b&h, 8 down-market alpha — hepsi DSR p<0.50 (kanıtsız).

### NIGHT-FOLLOWUP-001 | OPEN | Down-market 8 adayı forward-paper-trade [Barış onayı]
- APT/ADA/LINK 1h hücreleri en güçlü. Live-bar OOS topla, parity öncesi izle.
- Kaynak: `05_BACKTEST_RESULTS/alpha_summary.json` (down_market_alpha).

### NIGHT-FOLLOWUP-002 | OPEN | DSR ~0 kök neden: search-space inflation [AI: Claude|DeepSeek]
- Tüm adaylar DSR'da çakılıyor. Dar pre-registered hipotez grid'i ile confirmation-only run (küçük family → yüksek DSR gücü).

### NIGHT-FOLLOWUP-003 | OPEN | generate_morning_report.py legacy hardcoded OUTPUT_DIR fix [AI: Claude]
- Hâlâ `C:\LAB\tradingview-lab\...` okuyor (A1). Rapor elle üretildi. `hardcoded_path_rewrite_TODO`'ya bağlı.

### MORNING-001 | OPEN | Buy&Hold baseline güncelle [AI veya Barış]
- Aggregate tamamlandı: 16 iter, 149 robust winner (≥8/16).
- Çalıştır: `python buy_hold_baseline.py --sprint-dir sprint_runs`
- Amaç: TRXUSDT (+107%) / XRPUSDT (+124%) bull market etkisini filtrele, net alpha gör.

### MORNING-002 | OPEN | Promotion assessment güncelle [Barış onayı]
- Mevcut assessment 2026-06-01 tarihli, sadece 13 iter bazlı.
- 149 robust cell ile ADAUSDT/LINKUSDT/SOLUSDT stratejiler ELITE adayı.
- Güncelle: `sprint_runs/PROMOTION_ASSESSMENT_2026-06-01.md`
- Önerilen ELITE onaylar: `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY/TRXUSDT/2h`, `QL_DEEPAK_153_FILTER_1D/SOLUSDT/2h`

### MORNING-003 | OPEN | Transcript manual review [Barış — 31 aday]
- 31 aday bekliyor: 17 LIKELY_MISCLASSIFIED + 14 REVIEW_HUMAN
- Dosya: `11_TRIAGE/reclassification_audit_2026-06-01.md`

---

## Strategy Research Lab (infra eklendi 2026-06-03)

### RESEARCH-001 | OPEN | Retro-consolidate scattered intake files [AI: Claude|Any]
- Move existing intake/transcript files from `03_QUANTLENS/00_INBOX_REPORTS/`
  and `03_QUANTLENS/03_SALVAGE_IDEAS/` into the matching strategy's
  `STGxxx/source_intake/` (folders already created, currently empty).
- Use `03_QUANTLENS/tools/route_user_intake.py` logic as a guide; document moves.

### RESEARCH-002 | OPEN | Classification review for review_needed fields [AI: Claude|Barış]
- 43 strategies have `review_needed` in category/method/regime (mostly 1d set).
- Edit each `STGxxx/01_candidate_metadata.yaml` / `producer_spec.json`, then
  re-run `python 03_QUANTLENS/tools/build_strategy_research_registry.py`.
- Track via **Strategy Research Lab → Missing Metadata** tab.

### RESEARCH-003 | OPEN | Full indicator inventory from MTC_V2.pine [AI: Claude]
- INDICATOR_REGISTRY.json is seeded from strategy references + curated list.
- Extract the complete MTC_V2 indicator set (read-only; do NOT modify the .pine).

### RESEARCH-004 | IN PROGRESS (3/90 pilot done) | Re-triage transcript-now-present candidates [AI: Claude — batched]
- Pilot batch (3 HIGH) done 2026-06-04, review-first. Dispositions: `11_TRIAGE/retriage_dispositions_2026-06-04.md`.
  - Stg083 -> CANDIDATE -> created `03_QUANTLENS/strategies/STG047_brian_lee_smallcap_gap_mr_short`.
  - Stg082 -> WIKI_ONLY (Ted Zhang momentum podcast). Stg087 -> DUPLICATE (8EMA exit; overlaps STG002/042/043).
- Finding: top HIGH candidates are interview/educational -> expect WIKI/SALVAGE/DUPLICATE for most; far fewer than 90 new strategies.
- Remaining ~87: continue per disposition workflow; append to dispositions log.
- 172 triage worklist now reconciled with on-disk transcripts: 159 have transcripts,
  **90 eligible** (87 HIGH + 3 MEDIUM) — previously rejected only for missing transcript.
- Worklist: `11_TRIAGE/retriage_worklist_2026-06-04.md`. Live registry:
  `05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json` (regen `build_triage_registry.py`).
- Process per row via `09_TRANSCRIPT_INTAKE_WORKFLOW.md`: extract deterministic spec →
  create `03_QUANTLENS/strategies/STGxxx_<slug>/` → re-run `build_strategy_research_registry.py`.
- Do in batches with human review; check for duplicates vs existing 46 before creating.
- Visible in **Strategy Research Lab → Triage Worklist** tab.

---

## Completed Sprint (2026-06-01 — overnight)
- T-01 Buy&Hold baseline: DONE (117→ şimdi 149 robust, güncelleme gerekli)
- T-02 CPCV + PBO gate: DONE
- T-03 Promotion assessment: DONE (güncelleme gerekli — MORNING-002)
- T-04 MEGA overnight loop: DONE (16 iter, tamamlandı 06:33 yerel)
- T-05 QQE smoke test: DONE (FILTER_OVERLAY — overfitting, kaydedildi)
- T-07 SP-001 MVP-0 CLI: DONE (`mtc_cli/`, 8 test PASS)
- T-08 SP-002 vectorbt enrichment: DONE (`vbt_enrichment.py`, smoke PASS)

## Active (2026-06-01 — overnight workflow consolidation aftermath)

### IM-001 | DONE | analyze_transcripts.py path-resolution fix + basename fallback
- Completed 2026-06-01 by Codex (initial). Verified + basename fallback added by DeepSeek V4 Pro 2026-06-01.
- 165/165 transcripts now resolved and analyzed. 67 had legacy `06_QUANTLENS_LAB\` prefix → basename fallback finds them in `03_QUANTLENS/00_INBOX_REPORTS/Transcrips/`.
- Audit results: 115 ALREADY_OK, 17 LIKELY_MISCLASSIFIED, 14 REVIEW_HUMAN, 19 KEEP_REJECTED, 0 SPLIT_RECOMMENDED.
- 17 + 14 = 31 candidates need Barış manual review. See `11_TRIAGE/reclassification_audit_2026-06-01.md`. [AI: Barış]

### IM-002 | DONE | OUTPUT_DIR / hardcoded path audit script
- Completed 2026-06-01 by Codex. Added `03_QUANTLENS/tools/audit_hardcoded_paths.py`; pre-commit hook calls staged audit. Full default scan currently reports 2,488 existing legacy references.
- `tools/audit_hardcoded_paths.py` yaz — repo'da `C:\LAB\tradingview-lab\` veya benzeri legacy işaretleri grep'le, listele.
- CI/precommit hook'a ekle.
- Mevcut bilinen: `mega_walk_forward.py:32-36` (DATA_BUNDLE_PATH hala legacy işaret ediyor — `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427` yolu).

### IM-003 | DONE | mega_walk_forward resumable iter
- Completed 2026-06-01 by Codex. `mega_walk_forward.py` supports `--resume`, periodic checkpoint pickle, partial JSON, completed-job skip, and atomic final JSON replace. Verification used synthetic checkpoint helpers; full engine run not executed.
- Crash sonrası iter baştan başlıyor; %94 hesap kayıp.
- `--resume <pickle>` arg ekle. Her N iter'de pickled checkpoint.
- Atomik temp-rename ile partial JSON.

### IM-004 | DONE | Heartbeat in-iter granularity
- Completed 2026-06-01 by Codex. Mega now refreshes heartbeat during in-iteration progress events using `MEGA_HEARTBEAT_*`; loop scripts export context. Verification: Python helper PASS; bash syntax check unavailable.
- Mevcut: heartbeat sadece iter-arası. 75dk sessizlik mümkün.
- Mega'nın `[N/total] elapsed=Xs counts=...` her dakika print'ini parse et, heartbeat dakikalık güncelle.
- Monitor script anomaly threshold için bu lazım.

### IM-005 | DONE | Windows taskschd kurulum
- Completed 2026-06-01 by Codex. `MCC_Overnight_Monitor` scheduled task registered successfully; state `Ready`.
- `tools/register_overnight_monitor.ps1` admin PS ile TEK SEFER çalıştır.
- Çift kanal (taskschd + wakeup) — wakeup tek mekanizma riski yeniden yaşanmasın.

### IM-006 | DONE | CPCV (Combinatorial Purged Cross-Validation)
- Completed 2026-06-01 by Codex. Added `cpcv_validator.py` and rules CPCV Gate. Smoke report: `03_QUANTLENS/tools/cpcv_runs/smoke/CPCV_VALIDATION_REPORT.md`.
- Mevcut 4-gate'e **5. gate** olarak eklenecek.
- Rolling WF + lockbox bağımlı fold'lar yaratıyor; CPCV tüm `(N choose k)` train/test ayrımlarını test eder.
- Embargo + purge (overlap silme) lookahead riskini sıfırlar.
- Referans: López de Prado, "Advances in Financial Machine Learning" Ch.12
- Hedef: `03_QUANTLENS/tools/cpcv_validator.py` — mevcut `mega_walk_forward.py` `_worker` çıktısını alıp CPCV yeniden çalıştırır
- Rules dosyası §8'e "CPCV Gate" satırı eklenecek

### IM-007 | DONE | Probabilistic OOS / PBO
- Completed 2026-06-01 by Codex. Added `probabilistic_pbo.py` and PBO Gate. Smoke report: `03_QUANTLENS/tools/pbo_runs/smoke/PBO_REPORT.md`.
- Mevcut bootstrap_p_positive zaten Probabilistic Sharpe Ratio'nun bir formu
- **Probabilistic Backtest Overfitting (PBO)** ekle — combinatorically symmetric cross-validation
- DSR + PBO birlikte → en katı statistical layer
- Hedef: `tools/probabilistic_pbo.py`

### IM-008 | DONE | In-day single strategy hizli akis scripti
- Completed 2026-06-01 by Codex. Added `single_strategy_backtest.py`; MEGA supports `--strategy/--symbol/--tf`. Smoke output: `03_QUANTLENS/tools/single_strategy_runs/smoke_IM008/`.
- `tools/single_strategy_backtest.py <strategy_id> <symbol> <tf>`
- Tek komut → veri validation + sandbox WF + 4-gate + buy&hold + morning_report
- "1 strateji 5dk" akışı 4-gate atlanmadan otomatik
- Rules §2'deki "Standard Backtest Workflow" 10 adımını sırayla çalıştırır

### IM-009 | DONE | data_check module
- Completed 2026-06-01 by Codex. Added `data_check.py` and wired `single_strategy_backtest.py` to it. Smoke output: `03_QUANTLENS/tools/single_strategy_runs/smoke_IM009/`.
- `tools/data_check.py` — `verify_actual_range(symbol, tf)` API
- Rules §3 "Mandatory Data Validation Rules" first-class destek
- Cache disk içeriği (parquet/csv) ilk/son timestamp ve bar count
- Yanlış manifest claim'lerine karşı tek-doğru-kaynak

## Waiting On
- (none)

## Audit Backlog — LLM Code Review Findings (2026-06-02)

Aşağıdakiler ChatGPT 5.5 / DeepSeek V4 Pro audit'inden çıkan, henüz fix edilmemiş bulgular.
Her item yanında hangi modelin yapması uygun yazıyor.

### AUDIT-001 | OPEN | ADX yön hatası [AI: Barış onayı gerekli önce]
- `overnight_v2_runner.py:594` — `QL_QTREND_V2_STRONG_ADX` strateji `adx_14 < adx_threshold` kullanıyor.
- Strateji ismi "STRONG ADX" → yüksek ADX (trend) demek; ama kod düşük ADX'de giriyor.
- **Barış'ın kararı:** `<` mı doğru (ranging breakout intent) yoksa `>=` mi (güçlü trend intent)?
- Fix: yönü onayla, gerekirse `>=` yap ve strateji adını güncelle. [AI: Claude Sonnet — 1 satır fix]

### AUDIT-002 | OPEN | CPCV 3-tuple short strategy desteği [AI: DeepSeek / Claude Sonnet]
- `cpcv_validator.py:86` — CPCV `build_signals()` her zaman 2-tuple varsayıyor.
- `QL_QTREND_V1_SHORT` 3-tuple döndürüyor → crash veya yanlış direction.
- Fix: `mega_walk_forward.py` ile aynı 3-tuple parse logic'i ekle + `direction` parametresini `simulate_slice`'a ilet.

### AUDIT-003 | OPEN | rigorous_walk_forward.py short desteği yok [AI: Claude Sonnet]
- `rigorous_walk_forward.py:266` ve `rigorous_walk_forward_parallel.py:254` — `simulate_slice` `direction` parametresi yok.
- Short strategy feed edilirse sıfır trade / NaN sonuç üretir sessizce.
- Fix: `mega_walk_forward.py:simulate_slice` ile aynı short branch'i ekle (direction param + is_short logic).

### AUDIT-004 | OPEN | BUNDLE_MANIFEST env override yok [AI: Claude Sonnet]
- `mega_walk_forward.py:35-38` — `BUNDLE_MANIFEST` hardcoded arşiv path, `MEGA_OUTPUT_DIR` gibi env override yok.
- Fix: `MEGA_BUNDLE_MANIFEST = os.environ.get("MEGA_BUNDLE_MANIFEST")` ekle, yoksa legacy path fallback.

### AUDIT-005 | OPEN | PBO asimetrik CSCV split sorunu [AI: DeepSeek Max]
- `probabilistic_pbo.py:54` — default CPCV 15 sütun emit eder (tek sayı), PBO `n_splits // 2` ile 7/8 asimetrik partition oluşturur.
- Fix: çift sayı split veya sütunları çiftler hâlinde grupla. İstatistiksel analiz gerektiriyor.

### AUDIT-006 | OPEN | rolling_fold_indices min bars guard [AI: Claude Sonnet]  
- `mega_walk_forward.py:590` — `span_end < 1000` guard. 1000 bar altı dataset (yüksek TF, kısa tarih) sessizce `[]` döner; cell test edilmeden skip.
- Fix: `INSUFFICIENT_DATA` classification + warning log ekle. Guard'ı kaldırmak yerine görünür hata ver.

### AUDIT-008 | OPEN | Rolling fold OOS window overlap [AI: Claude Sonnet]
- `mega_walk_forward.py:600-607` — step = remaining//(NUM_FOLDS-1).
- n=1500: fold0 OOS [675,900), fold1 OOS [787,1012) → **113 bar overlap confirmed**.
- Same trades count in 2 OOS folds → `folds_positive` inflated → false PASS.
- CPCV gate (AUDIT-002) mitigates. But fold PASS count is statistically dependent.
- Fix: `step = test_size` (disjoint OOS) or document + raise PASS threshold.

### AUDIT-007 | OPEN | paths.py empty dir silent select [AI: Claude Sonnet]
- `paths.py:30` — `03_QUANTLENS` boş olsa da ilk `exists()` match seçiliyor.
- Fix: `any(candidate.iterdir())` guard veya warning. registry_reader + audit_reader da aynı logic'i inherit ediyor.

### AUDIT-009 | OPEN | bars_per_day=78 crypto'ya yanlış [AI: Barış onayı gerekli önce]
- `overnight_v2_runner.py:418,447,474,506,509` — `bars_per_day = 78` hardcoded (US equity 5m session = 6.5h).
- Etkilenen stratejiler: QL_CONNELL_EVENT_DRIVEN_GAP_5M, QL_AVWAP_BRIAN_INTRADAY_OR_5M, QL_EPISODIC_PIVOT_CHRISTIAN_5M (opening range).
- Crypto 24/7 → session open yok. `bar_idx % 78` her 24h crypto gününün ilk 78 barını yanlışlıkla "opening range" etiketliyor. Gün sınırı (`bar_idx // 78`) takvim günleriyle hizalanmıyor.
- **Barış kararı:** Bu OR stratejileri sadece US equity sembollerinde mi çalışmalı? Yoksa crypto için bars_per_day sembol-aware mi olmalı (288 bar/gün @ 5m)?
- Fix: sembol-aware `bars_per_day` veya OR stratejilerini US session sembol/TF'ye gate et.
- Doğrulandı: kod incelendi 2026-06-02 (Mimo v2.5 audit Run 7,11 — gerçek bulgu).

### AUDIT-010 | OPEN | ingest.py transcript re-write race [AI: Claude Sonnet]
- `ingest.py:249-251` — `if not target.exists() or sha != state_sha:` dış koşul, ama iç `if not target.exists():` sadece yeni dosya append ediyor.
- Bug: dosya VAR + içerik DEĞİŞTİ (sha farklı) durumunda → dış koşul True, iç koşul False → **dosya hiç güncellenmiyor**, sadece `transcript_main_sha` state set ediliyor.
- Sonuç: sonraki run'da sha eşleşir → değişen transcript kalıcı stale kalır.
- Fix: sha-mismatch dalında da `new_transcripts.append((target, ...))` ekle (overwrite queue).
- Doğrulandı: kod incelendi 2026-06-02 (Mimo v2.5 audit Run 7,11 — gerçek bulgu).

## Side Projects (parked — pick up when ready)

### SP-005 | Strategy Detail Page Redesign (trading-review dashboard) [AI: Claude lead + Barış]
Status: plan v3 ready, not started. Proposed 2026-06-02, revised 2026-06-03 (v2→v3).
Trigger: Barış flagged the strategy-detail page as confusing/too technical.
**Direction LOCKED: terminal** (`proto_B2_terminal.html`; single-scroll; A/clinical/
editorial dropped). v3 structural rules: (1) ONE scoring system = Scorecard;
QuantLens = commentary that references it, no double scoring. (2) Verdict & Decision
MERGED into one top block. (3) Scorecard directly under verdict, click-to-expand
gates. (4) Backtest = TradingView-tester-style CASES (video-settings + optimized
best, each w/ settings·symbol·timeframe on one standard window). (5) Stage prototypes
built (rules-extracted/testability/backtested/promotion). Prototypes + shared
`proto_terminal.css` in `08_DASHBOARD_APP/apps/web/prototypes/`.

Problem: current page (`08_DASHBOARD_APP/apps/web/app.js:389` `renderUnifiedStrategyDetail`)
is a debug dump — raw ID as title, two dense parallel tables, one misleading
`57/100` headline, bare machine terms. Raw decision sentence from
`mtc_v2_reader.py:217` (interpolates raw ID + raw status).

Fix: single-scroll trading-review dashboard — English-only UI, human name +
translated-to-English description, sticky mini-summary, decision summary,
**QuantLens Verdict** (ruthless audit layer), **Strategy Taxonomy** chips,
review-journey stepper, expanded trading rules, 4 gate bars, honest backtest
evidence, **Salvageable Ideas** (mandatory), debug collapsed into Technical.

KEY FINDING (2026-06-03): QuantLens is **already a real pipeline** —
`03_QUANTLENS/03_SALVAGE_IDEAS/<candidate>/` has 7 artifacts each;
`01_candidate_metadata.yaml` already carries `quantlens_decision`,
`commercial_value_score`, `complexity_score`, `repaint_risk`, `lookahead_risk`,
`closed_source_risk`, `candidate_kind` (salvage categories), `market_type`,
`recommended_next_step`. Dashboard readers **ignore these today**. QuantLens
Verdict section surfaces existing data via a new read-only `quantlens_reader.py`.

**Full plan:** `03_QUANTLENS/_user_guide/11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md` (v3)
**Prototypes (DONE, approved 2026-06-03):** `08_DASHBOARD_APP/apps/web/prototypes/` —
terminal set: `proto_B2_terminal.html` (blocked), `proto_stage_rules_extracted.html`,
`proto_stage_testability.html`, `proto_stage_backtested.html`, `proto_stage_promotion.html`.
English-only, single-scroll, CSS inlined.
**Depends on:** SP-004 (scoring) for Wave C gate bars.
**NEXT: awaiting Barış go-ahead to start Wave A coding (not yet authorized).**

Three waves:
- Wave A — single-scroll UI/wording/layout on EXISTING data: `ui_labels` map,
  decision-object refactor (ID-free), header + sticky summary + decision summary,
  taxonomy shell, review-journey stepper, trading-rules card ("Not defined yet"),
  Technical `<details>`, source slim-down, responsive CSS. [Claude/Any]
- Wave B — QuantLens structured data: new `quantlens_reader.py` (parses salvage
  YAML/markdown), QuantLens Verdict card, Salvageable Ideas section, conditional
  render matrix (garbage/closed-source/complexity stops), repaint/lookahead/
  marketing/unverified-claim warnings, commercial-value + testability +
  evidence-level + documented-vs-proven derivations. Schema add for
  CLOSED_SOURCE_STOP/COMPLEXITY_OVERLOAD + structured `salvageable_ideas[]`. [Claude]
- Wave C — `scorecard_v2` (SP-004 P2) gate bars + N/A + backtest-evidence visuals
  (equity, metrics, B&H, source-claim-vs-result) + filter migration. [Claude]

Files: `apps/web/{app.js,index.html,styles.css}`, `mtc_v2_reader.py` (decision
object), new `mcc_readonly/ui_labels.py`, new `mcc_readonly/quantlens_reader.py`,
`audit_reader.py` (join verdict to row). No scoring math here (consumes
`scorecard_v2`). Constraint: presentation + read-only QuantLens reader — no live
trading, no Pine/parity/pipeline change, audit data moved not deleted.

Barış decisions (2026-06-03, all = plan's recommended): QuantLens above Taxonomy;
AI-generated names (editable); provisional commercial-value bands; **ship Wave A
first**; closed-source → still show independent sub-ideas; derive stop-states (no
YAML schema change now). No open questions. Awaiting go-ahead to start Wave A
(not yet authorized).

### SP-004 | Strategy Scorecard Redesign (gate-based, edge-weighted) [AI: Claude lead + DeepSeek + Barış]
Status: planned, not started. Proposed 2026-06-02.
Trigger: when ready to fix the strategy-detail score Barış flagged as
"yetersiz ve hatalı".

Problem: current `build_scorecard()` (`08_DASHBOARD_APP/apps/api/mcc_readonly/presentation_reader.py:65`)
is one flat 100-blend that measures **pipeline progress, not edge** — 25/35
backtest points are pure stage maturity, return/PF are risk-blind, no drawdown /
Sharpe / benchmark / OOS / PBO / repaint hard-fail.

Fix: replace single composite with 4 separate gates + hard-fail flags
(Gate1 intake /100, Gate1B feasibility /50, repaint pass/fail, Gate2 backtest
/100 risk-adjusted, Gate3 production /100). Never recollapse to one number.
~Half the Gate2 inputs (WFO/CPCV/PBO/B&H) already computed by overnight tooling.

**Full plan:** `03_QUANTLENS/_user_guide/10_STRATEGY_SCORECARD_REDESIGN_PLAN.md`
**Source rubric (DELETE when done):** `11_TRIAGE/_eval_pipeline_source_TEMP/`

Phases (~8–10 days, order revised after 2 LLM audits — see plan §9):
- P0A rubric mapping + 2 JSON schemas (eval + production_readiness) + template
  fields (thesis_en, hard-fail reasons, run_id, phase_current) [Claude → Barış]
- P1A fix CPCV 3-tuple (AUDIT-002) + PBO split (AUDIT-005) + N_A fallback
  BEFORE hard-gating [DeepSeek/Sonnet]
- P1 emit `evaluation_artifact_v1` w/ status envelope on 5–10 strategies [Claude/DeepSeek]
- P1.5 finalize numeric bands FROM real distributions, not guessed [Claude → Barış]
- P2 gate scoring engine → `scorecard_v2` (parallel to legacy) + golden tests [Claude, cross-model review]
- P3 dashboard: thesis title + gate bars + migrate filters to gate-status [Claude/Any]
- P4 backfill w/ completeness check + ranking validation [DeepSeek + Barış]
- P5 cleanup: legacy flag removal + **delete TEMP** (only now) [Claude]

Open for Barış (plan §8): numeric bands (set in P1.5), trade-count minimums,
PBO≥0.5→OVERFIT_SUSPECT?, AI-vs-human thesis title, Gate1B /50-vs-PASS,
Gate3 separate production artifact.
Constraint: read-only on trading/Pine/parity — only adds output writer + scoring + UI.

### SP-003 | Python Live Trading Engine (Pine Script bypass) [AI: Claude]
Status: planned, not started. Proposed 2026-06-01.

**Sistem Özeti:**
Mevcut MTC pipeline (backtest → optimizasyon → sinyal) çıktısını doğrudan
Binance'e bağlayan, TradingView/Pine Script bağımlılığını kaldıran tam otonom
canlı trade altyapısı.

**Mimari:**
```
mega_walk_forward.py        → optimal parametre çıktısı
      ↓
signal_generator.py         → BUY/SELL/HOLD sinyali (mevcut strateji mantığı)
      ↓
binance_executor.py         → ccxt ile Binance API order
      ↓
VPS (Hetzner/DigitalOcean)  → 7/24 çalışır, bilgisayardan bağımsız
```

**Neden Pine Script'e gerek kalmaz:**
- Pine Script sadece görsel + alert üretir; trade execution yok
- ccxt kütüphanesi 100+ exchange destekler, Binance tam uyumlu
- Python: backtest + sinyal + execution tek yerde → debug kolaylığı
- ML entegrasyonu, CPCV, PBO gibi mevcut katmanlar doğrudan bağlanabilir

**Teknik Bileşenler:**
- `ccxt` → Binance Spot / USD-M Futures / COIN-M Futures API
- Binance Testnet → gerçek para olmadan tam test (`set_sandbox_mode(True)`)
- `systemd` service veya `nohup` → VPS'te arka plan çalışma
- Position sizing → risk per trade sabit ($, % veya ATR bazlı)
- Stop-loss / take-profit → `create_order` ile OCO order

**VPS Gereksinimi:**
- Minimum: 1 CPU, 1GB RAM → Hetzner CX11 (~4€/ay)
- Lokasyon: Frankfurt veya Tokyo (Binance sunuculara düşük latency)
- Scalping varsa lokasyon kritik; swing/daily için fark yok

**Scope:**
- Yeni klasör: `MTC_COMMAND_CENTER/05_LIVE_ENGINE/` (önerilir)
- `binance_executor.py` — order yönetimi, rate limit handling
- `signal_bridge.py` — mevcut backtest çıktısını live sinyale dönüştürür
- `risk_manager.py` — position sizing, max drawdown kill switch
- `monitor_live.py` — açık pozisyon takip, heartbeat log

**Kritik Riskler:**
- Backtest → live performans farkı (slippage, funding rate, latency)
- API key güvenliği → .env, IP whitelist zorunlu
- Kill switch eksikliği → runaway loss riski
- Pine Script'te olan görsel analiz burada yok → TV charts korunabilir

**TradingView korunabilir mi:**
- Evet. TV sadece görsel analiz + chart için tutulabilir
- Sinyal ve execution Python'a taşınır
- Hibrit mimari mümkün: TV chart → alert → Python webhook → ccxt order

**Pickup trigger:**
- Backtest pipeline stabil ve tutarlı OOS sonuç ürettiğinde
- En az 3 ay paper trading (testnet) başarısı sonrası canlıya geçiş

**Out of scope (bu SP altında yapılmaz):**
- Pine Script veya MTC_V2.pine değişikliği
- Mevcut backtest/WF/CPCV pipeline değişikliği
- High-frequency / scalping (swing/daily ile başla)
- Multi-exchange (sadece Binance ile başla)

### SP-002 | vectorbt analytics layer (post-processing enrichment) [AI: Claude|DeepSeek]
Status: planned, not started. Proposed 2026-06-01.
Goal: wire vectorbt as post-processing layer on top of TradingView trade data.
`data_get_trades` MCP → `vbt.Portfolio.from_orders()` → richer metrics (Calmar,
Sortino, Omega, rolling Sharpe, underwater equity curve, Monte Carlo) not
natively available in TV. Does NOT replace Pine strategies or MCP tooling.
Optionally: validate/replace `cpcv_validator.py` with vectorbt's built-in CPCV.

Scope: new helper `03_QUANTLENS/tools/vbt_enrichment.py` only.
No Pine / MTC / parity edits. No replacement of `mega_walk_forward.py`.
Pre-req: `pip install vectorbt` (or `vectorbt-pro` if available).

Acceptance:
- Takes a list of TV trade dicts (from `data_get_trades`) + price series
- Returns enriched stats dict + optional HTML report
- Integrates as optional post-step in `single_strategy_backtest.py`

Pickup trigger: whenever a sprint or single-strategy result needs deeper
analytics than the current 4-gate pipeline provides.

### SP-001 | Internal CLI layer + dashboard buttons (`mtc_cli/`) [AI: Claude]
Status: planned, not started. Approved 2026-05-31 by Barış.
Goal: agent-native CLI surface + 1:1 dashboard buttons so any AI model (and
Barış) can drive recurring workflows without memorizing commands or scanning
the repo. Cuts next-session context cost. Wraps existing scripts + MCP — no
replacement of `MTC_V2.pine`, parity logic, or TradingView MCP tools.

Decision reference: `DECISIONS.md` D002 (adopt internal CLI; reject CLI-Anything).

Hard constraint: at scaffold time, re-read all `_AI_MEMORY/` anchors,
`AGENTS.md`, `AI_RULES.md`, `DO_NOT_TOUCH.md`, run `git status` +
`git log --oneline -20`, diff intent vs reality, surface drift to Barış,
**no write until approval**. Treat plan below as intent, not contract.

Must obey 7-gate workflow (AI_RULES.md). Start at Gate 1.

#### MVP-0 — CLI skeleton + read-only audit (~1 evening)
- Whitelist (declare in G1): new folder `mtc_cli/` only.
- Deliverables: `mtc_cli/__main__.py`, `mtc_cli/contract.py` (envelope,
  exit codes, error categories), `mtc_cli/commands/audit.py`,
  `mtc_cli/tests/`.
- Command: `python -m mtc_cli audit repo [--json]` — read-only snapshot.
- Acceptance: valid JSON envelope, exit 0 on clean repo, exit 2 on missing
  memory file fixture, byte-stable on unchanged repo.
- Touches Pine / MTC / parity: **no**. Skip explicit Barış approval gate.
- Gates: G1 → G2 → G3 → G4 → G5 (reviewer must be Codex or Gemini, not
  Claude) → G6 (subprocess + file IO surface = required) → G7.

#### MVP-0.5 — One dashboard button (~1 evening)
- Whitelist: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/` only.
- Deliverable: minimal page with "Audit Repo" button calling the CLI via
  existing API. Tooltip = one-line explanation.
- Acceptance: click → JSON envelope rendered to screen, no business logic
  in dashboard (thin wrapper only).
- Reuses existing `08_DASHBOARD_APP/apps/api` pattern. No new app.

#### MVP-1 — Memory + handoff writes (~2–3 evenings)
- Whitelist: `mtc_cli/` + dashboard button extensions only.
- Deliverables: `mtc memory append`, `mtc handoff write`,
  `mtc handoff lock/unlock`. `.bak` rotation, mtime guard, append-only
  defaults, `--dry-run` default for first week.
- CLI becomes sole programmatic writer for `GLOBAL_HANDOFF.md`,
  `SESSION_LOG.md`, `NEXT_STEPS.md`, `DECISIONS.md` — automates Gate 7.
- Hand-edits still allowed (Barış) but a pre-commit hook warns.
- Acceptance: idempotent (run twice unchanged repo = byte-identical),
  hostile-input tests pass, generated handoff < 2KB.
- Gates: full G1 → G7. G6 mandatory.

#### MVP-2+ (later, not committed)
- `mtc pine check` (wrap MCP `pine_smart_compile` — read-only).
- `mtc report build` (deterministic report from backtest artifact dir).
- `mtc route classify` (cheap-model intake classifier with JSON-schema gate).
- CLI-Anything evaluation: deferred indefinitely. Revisit Q3 2026 only if
  trigger condition (need to drive an unscriptable external GUI) appears.

#### Out of scope (do NOT do under SP-001)
- Any edit to `MTC_V2.pine`, parity files, or MTC strategy behavior.
- Live trading anything.
- New root-level handoff files.
- New prompt folder at root — templates (if any) go in
  `04_SHARED/prompts/05_ai_workflow/`.
- Replacing `mcp__tradingview__*` tools. CLI wraps, never replaces.
- Auto-execution of `next_action` suggestions in CLI output.
- New runtimes (node, rust, go). Python + PowerShell only.

#### Open risks to carry into G1
- `PROJECT_MEMORY.md` (stable) vs `ACTIVE_FILES.md` (volatile) boundary —
  CLI's audit must respect, not blur.
- Gate 5 cross-model review not hook-enforced — must invoke Codex/Gemini
  manually for MVP-0.
- Parity smoke command not pinned — N/A for MVP-0/0.5/1, but record gap
  forward to first parity-touching sprint.

## Recently Closed (2026-05-31, Phase 6 follow-ups)
- I: source-parent cleanup completed for the Command Center audit. `QLR_*` parent rows that share a YouTube URL with extracted child candidates, or contain multi-case split evidence, are now `SOURCE_PARENT`, hidden from normal strategy/MTC_V2 queues, and protected by tests. Remaining visible rejected rows have transcripts and are rejected for source/classification reasons, not missing transcript.
- G: transcript/source-map repair for `11_TRIAGE/2026-05-30_rejected_worklist.xlsx` completed in the clean repo. The 99 HAS_URL_NO_TRANSCRIPT worklist candidates now resolve with transcript links in the refreshed audit; NO_URL_NO_TRANSCRIPT remains unresolved by user report.
- H: repeated-URL audit completed for the same workbook. See `MTC_COMMAND_CENTER/11_TRIAGE/duplicate_url_strategy_audit_2026-05-31.md`; no clear accidental duplicate group found.
- A: audit artifacts committed (`2a38d19`).
- B: legacy freeze policy ratified — accept + document, no NTFS DACL (`dcdf913`).
- C: xlsx-missing warning suppressed in CSV-only mode + AUTO_002 smoke PASS (`d35e620`).
- D: Phase 4 manifest full SHA256 + Phase 5 divergence notes (`c3e78f4`).
- E: `update_tracker.py` documented as deferred one-shot (`1b7caff`).
- F: Phase 1 verification reviewed — PASS; path rewrite policy ratified
  (active set complete, deferred set fix-on-demand). See
  `docs/migration_manifests/PATH_REWRITE_POLICY.md`.

## Reference Documents
- Migration audit: `docs/migration_manifests/phase6_audit_report.md`
- Legacy freeze policy: `docs/migration_manifests/LEGACY_FREEZE_POLICY.md`
- Path rewrite policy: `docs/migration_manifests/PATH_REWRITE_POLICY.md`
- Per-script TODO: `MTC_COMMAND_CENTER/02_MTC_BACKTEST/hardcoded_path_rewrite_TODO.md`
