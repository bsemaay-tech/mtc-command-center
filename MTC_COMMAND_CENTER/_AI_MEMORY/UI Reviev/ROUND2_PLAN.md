# MCC Strategy-Detail UI — Round 2 Plan

**Date:** 2026-06-07 · **Author:** Claude Opus 4.8 · **Scope:** `08_DASHBOARD_APP/apps/web/app.js` + `apps/api/mcc_readonly/` (scorecard_reader / read_model)
**Source:** Barış section-by-section walkthrough (round 2), screenshots in `UI Reviev/Ekran görüntüsü 2026-06-07 2117*.png`.
**Predecessor:** `ARCHİVE 1/MCC_UI_AUDIT_PLAN.md` (round 1, 38 shipped + UI-5 parked).

> **Constraints (unchanged):** display-only + read-only API. No Pine / MTC_V2 / parity / trading-logic edits without explicit approval. Tooltip language = English. Orchestrator does NOT write code (low credit) — spec + dispatch to cheap agents (Antigravity/Codex/DeepSeek), audit on real data. app.js = single-file serial owner; backend readers = parallel side-track.

---

## 0. Round-1 carry-over (verified partial/leaky — fold into Round 2)

| Carry | Was | Residual gap (round-2 finding) |
|---|---|---|
| UI-7 | Low Score Review tooltip | `LOW_SCORE_REVIEW→"Needs review"` map+tooltip exist (app.js:594/610) but displayed label "Low Score Review" doesn't hit the map → tooltip never fires for real data. → **R2-02** |
| UI-10 | stale blocker removed | canonical.blocking precedence ✓ but empty-case falls back to legacy `blocked_reason` → "score below 65" still leaks (app.js:690). → **R2-06** |
| UI-16 | gate sub-score detail | only PASS gates render breakdown (app.js:877); FAIL/INCOMPLETE show none. → **R2-15** |
| UI-26 | backtest SST merged | Evidence section merged ✓ but Journey backtest_status desyncs from scorecard FAIL + score-view vs metric-view still read as two backtests. → **R2-23 / R2-24** |
| UI-32 | repaint wired | Trading Rules ✓ but a separate hardcoded "Repaint status unknown" chip remains in Verdict riskFlags (app.js:726). → **R2-08a** |

**Root pattern:** round-1 fixed the happy path (PASS / promotable / canonical-populated); edge cases (FAIL, empty canonical, legacy fallback) left untreated.

---

## 1. Round-2 findings (R2-01 … R2-24)

### Strategy name / header
- **R2-01** Title vs description render the same text → duplicate (app.js:464/466). [dedupe]
- **R2-02** "Low Score Review" no tooltip — statusBadgeTooltip map miss (carry UI-7). [tooltip]
- **R2-03** "QuantLens: Not evaluated yet" no explanatory tooltip. [tooltip]

### Verdict & Decision
- **R2-04** 6-level verdict ladder hidden (only primary shown). Want primary big + alternatives small below + tooltip (app.js:702-721). [UX]
- **R2-05** "CAN TEST" badge 3-state ladder hidden (app.js:761). [UX]
- **R2-06** stale legacy "score below 65" leaks via `blocked_reason` fallback (carry UI-10). [data/display]
- **R2-07** blocker text duplicated: "Blocking item" fact (app.js:774) + riskFlags chip (app.js:724). [dedupe]
- **R2-08a** hardcoded "Repaint status unknown" chip in riskFlags (carry UI-32). Remove (no real data). [remove]
- **R2-08b** "Documented and internally tested" unclear → "Rules written · internally tested" + tooltip; other state "Rules written · not proven" (app.js:738). [wording]

### Scorecard
- **R2-09** 7-run case-list lives under Scorecard but is conceptually Backtest data — clarify placement/label. [layout]
- **R2-10** Gate 1/2/3 should sit directly under Scorecard heading; run-list below (app.js:808 vs 814). [layout]
- **R2-11** Gate detail shows raw code names (`intake.entry_pseudo_present`) → human-readable label dictionary (app.js:879/945). [wording]
- **R2-12** "6/?" — `max_points` null → "?" (app.js:881). Hide/resolve. [bug]
- **R2-13** Show short why-points-deducted next to score (deep AI reasons → backlog) (app.js:876). [display + backlog]
- **R2-14** **KEYSTONE** — `statusText(status) · passLabel` emits doubled labels: "OK·Pass", "FAIL·Fail", "INCOMPLETE·Pending" (app.js:891/867). One fix kills R2(Q6/Q7-double/Q8-double). Collapse to single clear label. [dedupe]
- **R2-15** FAIL/INCOMPLETE gates show no sub-score breakdown (carry UI-16). [display]
- **R2-16** Gate3 "Incomplete·Pending" → "Not evaluated (Gate3 scorer not built)". [wording]
- **R2-17** Gate2 "Missing / not scored" tooltip — "metrics not produced by this run" (app.js:897). [tooltip]
- **R2-18** "Action required" gate-blockers gives no action → gate-specific actionable text (app.js:2616). [wording]
- **R2-19** Gate3 fields (alert_adapter.* / state_sync.*) raw + bare N/A → human dictionary + per-N/A reason. [wording]

### QuantLens / Taxonomy / Journey / Backtest Evidence
- **R2-20** QuantLens shown twice (top badge app.js:470 + full section app.js:476). Keep one, under Scorecard. [dedupe/layout]
- **R2-21** QuantLens must write expert opinion, NO score — single scoring = Scorecard. [→ project, see §4]
- **R2-22** Strategy Taxonomy = heuristic keyword inference (app.js:951/984/993/1003), no SST, some hardcoded ("Complexity: Not defined yet" :963) → bind to real source OR label as "estimated". [data/wording]
- **R2-23** **BUG** Journey "Backtested pending" while Scorecard shows FAIL — `canonical.backtest_status` not synced (app.js:1015). [bug/SST]
- **R2-24** Scorecard score-view ↔ Backtest-Evidence metric-view = same backtest, two sections read as separate (UI-26 residual). Merge / explicit "this score came from these metrics" link. [layout/UX]

### Acceptance panel (top global banner — from earlier turn)
- **R2-25** Panel renders above #strategyDetail → appears on every detail page, read as strategy-specific. Hide when detail open / move into pipeline view only (app.js:156, index.html:51). [layout]
- **R2-26** Promotable list is loose `<div>` rows, not a sortable table (Name·Family·Symbol·TF·Gate2·Date·Run) (app.js:2578). [UX]
- **R2-27** "1 Promotable / 360 scored" misleading — 360 = scorecard cards (≈80 distinct strategies × runs), not 360 strategies. Relabel / clarify tooltip (app.js:2552). [wording]

---

## 2. Themes (R2 findings collapse to 7)

| Theme | Findings | Core |
|---|---|---|
| **T1 — Double-label / dedup** | R2-01, 07, 08a, 14★, 20 | Same value printed twice; `status·passLabel` keystone. |
| **T2 — Plain-language + field dictionary** | R2-02, 03, 08b, 11, 16, 17, 18, 19 | Raw codes, missing tooltips, unclear wording; needs a gate-field label map. |
| **T3 — Layout / placement** | R2-09, 10, 20, 24, 25, 26 | Gate order, run-list, QuantLens single spot, acceptance panel scope, backtest two-view. |
| **T4 — Verdict ladder UX** | R2-04, 05 | Surface the existing 6-level verdict + 3-state badge as a graded ladder. |
| **T5 — Score breakdown** | R2-12, 13, 15 | `6/?` bug, deduction reason, breakdown for non-PASS gates. |
| **T6 — SST / data bugs (backend)** | R2-06, 22, 23, 27 | Legacy blocker leak, taxonomy no-SST, journey backtest desync, scored-count semantics. |
| **T7 — QuantLens conceptual project** | R2-21 (+R2-03b/R2-20 link) | MCC QuantLens = Claude verdict, not Gemini import. Rename + workflow. **Separate.** |

★ R2-14 is the highest-leverage single fix (resolves 3 complaints).

---

## 3. Decisions — RESOLVED (Barış, 2026-06-07)

| # | Decision | Resolution |
|---|---|---|
| **R2-D1** ✅ | QuantLens rename + Claude-verdict workflow | **CONFIRMED: Gemini-origin data → "Gemini Pre-Screen"** (Barış 2026-06-07). Name "QuantLens" reserved for Claude's own verdict. Rename NOW (display, ALL sites: Verdict / QuantLens Verdict / Salvageable Ideas / source labels — cross-cutting per audit); Claude-verdict pass = separate project (Phase R2-E). |
| **R2-D2** ✅ | Low-score decision mechanism | **A only — B NEVER.** Display-only note "⚠ Needs your decision: promote / retest / park". No write-back, no dropdown. Dashboard stays read-only forever. **Backlog N2-B deleted.** |
| **R2-D3** ✅ | UI language | English everywhere. |
| **R2-D4** ✅ | Acceptance panel | **Hide on detail page (pipeline-only)** + **convert promotable list to sortable table** (cols: Strategy · Family · Symbol · TF · Gate2 · Accept date · Run). Display-only. |
| **R2-D5** ✅ | Taxonomy source | **Estimate now, real source later.** Label chips "estimated (inferred from name)" now; design to swap to real source later (producer_spec strategy_type/market_type + QuantLens verdict once built). |
| **R2-D6** ✅ | scored counter | **"N strategies · M backtest runs"** (e.g. "1 promotable · ~80 strategies · 360 runs"). |

→ All decisions resolved. Only open item: confirm the rename string for R2-D1 ("Gemini Pre-Screen"?).

---

## 4. Execution phases

**Sequencing principle (learned from round-1):** treat edge cases, not just happy path. Backend SST before cosmetic copy where they interact. app.js serial (one owner); readers parallel.

### Phase R2-0 — Keystone dedup (do first, tiny, decision-free)
- **R2-14** collapse `status · passLabel` → single label (PASS/FAIL/INCOMPLETE→Pending). Kills R2-Q6/Q7-double/Q8-double.
- **R2-07** remove duplicate blocker chip (keep the "Blocking item" fact).
- **R2-08a** remove hardcoded "Repaint status unknown" chip.
- **R2-12** fix "6/?" (`max_points` null guard).
- **R2-01** dedupe title vs description.
→ single app.js pass, cheap agent, orchestrator audit.

### Phase R2-A — Field dictionary + wording + tooltips (T2, decision-free except language)
- Build **gate-field label dictionary** (intake.* / gate2 sub_scores / gate3 alert_adapter.*+state_sync.*) → human labels (R2-11, R2-19).
- **R2-02** fix Low Score Review tooltip (normalize label → map key, or add "low score" branch).
- **R2-03** QuantLens "Not evaluated" tooltip.
- **R2-08b** "Documented and internally tested" → clearer + tooltip.
- **R2-16** Gate3 "Not evaluated (scorer not built)".
- **R2-17** "Missing / not scored" tooltip.
- **R2-18** "Action required" → gate-specific action text.
→ app.js + maybe a shared label map; one pass.

### Phase R2-B — Layout (T3, needs R2-D4)
- **R2-10** gates directly under Scorecard heading; run-list below.
- **R2-09** label/relocate 7-run list as backtest data.
- **R2-20** remove top QuantLens badge, keep single section under Scorecard.
- **R2-24** link/merge Scorecard score-view ↔ Backtest-Evidence metric-view.
- **R2-25** hide Acceptance panel on detail page (pipeline-only).
- **R2-26** Acceptance list → sortable table.

### Phase R2-C — Verdict ladder + score breakdown (T4+T5)
- **R2-04** 6-level verdict ladder (primary big, alternatives small, highlight current) + tooltip.
- **R2-05** 3-state badge ladder.
- **R2-15** sub-score breakdown for FAIL/INCOMPLETE gates too.
- **R2-13** short why-deducted line (deep reasons → backlog).

### Phase R2-D — SST / data bugs (T6, backend; needs canonical work)
- **R2-06** complete UI-10: stop legacy `blocked_reason` fallback leaking "score below 65"; derive only from gate_summary.blocking (or scrub stale text).
- **R2-23** sync Journey backtest_status with scorecard gate2 (canonical.backtest_status populate).
- **R2-22** taxonomy: bind to source / label as estimated.
- **R2-27** scored counter: distinct-strategy vs run count (needs R2-D6).
→ scorecard_reader.py / read_model.py + app.js. Parallel-safe on readers.

### Phase R2-E — QuantLens conceptual project (T7, needs R2-D1) — SEPARATE
- Rename Gemini-origin data + label.
- Define Claude QuantLens verdict prompt (rubric already in `03_QUANTLENS/_user_guide/11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md §4.2-4.4`).
- Manual AI pass over each strategy → write verdict data → dashboard reads it.
- Opinion only, NO score (single scoring = Scorecard).

---

## 5. Backlog (separate projects, not this batch)
- **W1** Wire MTC_V2 parity into approved night flow.
- **W2** Auto "needs-backtest" selector (registry: eligible AND no gate2). = NIGHT_BATCHES N5.
- ~~**N2-B** Low-score decision write-back~~ — **CANCELLED (R2-D2: never; read-only forever).**
- **R2-13-deep** AI-authored deduction explanations.
- **Gate3 builder** — production-readiness scorer (system-wide gap; all strategies INCOMPLETE).
- **UI-30 fill** — producer_spec SL/TP/risk targeted field-fill.

---

## 6. Dispatch model (token discipline)
- **app.js owner** = one cheap agent, serial (R2-0 → A → B → C in sequence on the single file).
- **Backend readers** (R2-D) = parallel side-track (different files).
- **Phase R2-E** = own project, decisions first.
- Orchestrator (Claude): spec each phase, dispatch, **audit on real snapshot data** (never trust agent reports). `node --check app.js` + reader unittests each phase.
- Commit per phase, one finding-group per commit.

---

## 7. AUDIT RECONCILIATION (2026-06-07) — 4/4 reports in, strong convergence

**Status:** ALL FOUR submitted — Codex (GPT-5), Claude (Opus 4.8), DeepSeek v4 Pro, Antigravity (Opus 4.6) — each verified against LIVE code + `build_dashboard_snapshot()` data. (DeepSeek's auto-driver harness threw `OSError [Errno 22]` but the manual report landed.) Antigravity baselined at commit `40032cd` (post-B3, slightly older than current `d26dbd5`). **Zero DISPUTEs across all four; findings converge.** Claude tally: 21 CONFIRM / 9 CONFIRM-BUT / 0 DISPUTE / 2 BLOCKER-class.

### 7.1 Live-data ground truth (Codex, verified)
- `scorecards.cards = 360`, `scorecards.by_strategy = 38`, `promotable_cards = 1`. → **R2-27 real label = "1 promotable · 38 strategies · 360 runs"** (38 distinct, NOT ~80).
- Sampled `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`: canonical `defined_tf=10m`, `tested_tf=1D`, `backtest_status=FAIL`, `gate2_score=68.76`, `blocking=[gate2,gate3]`.
- An MTC_V2 readiness row still carries `status_label='Low Score Review'`, `blocker='score below 65'` from `mtc_v2_reader.py`.
- `build_quantlens()` already scans BOTH `03_SALVAGE_IDEAS/` + `strategies/`; `scoreForGate` no longer needs `status==="OK"`. **Round-1 UI-8/21 genuinely fixed** — no R2 finding wrongly re-flags them.

### 7.2 Plan corrections (both auditors agree)
1. **KEYSTONE CHANGED.** R2-14 is the *cheapest visible* win, NOT the keystone. **True keystone = T6 (canonical as the enforced single source).** If every render site read ONLY `canonical` (no `auditRow.blocked_reason` / `mtcV2Row.blocker` / keyword-taxonomy fallbacks), then **R2-06, R2-22, R2-23, R2-27 collapse into one backend change.** Re-rank T6 above T1.
2. **META-DEFECT (the real Round-3 preventer):** Round 1 fixed *render sites one-by-one* instead of normalizing at the canonical layer, so each new render site re-imports the old fallbacks. **Round-2 strategy = enforce canonical at every site + DELETE the fallback chains.** This is the architectural fix.
3. **NEW finding R2-28:** second stale-blocker leak at **app.js:1294** (`mtcV2Row.blocker || auditRow.blocked_reason`) — same bug as R2-06, different call site, uncaught. Must scrub BOTH + remove the stale source in `mtc_v2_reader.py`.
4. **R2-23 REFRAMED — small frontend fallback, NOT a backend populate.** Backend already maps gate2→backtest_status (`scorecard_reader.py:253`); sampled row is FAIL/correct. DeepSeek pinned the mechanism: **when `canonical` is empty `{}` (API not-yet-attached / cache miss) but `scorecardV2` IS populated, `renderReviewJourney` (:1015) shows "pending" while Scorecard shows FAIL.** `renderBacktestEvidence` (:1133) already guards with `can.gate2_status || g2.status`; **Journey must mirror it:** `const g2Status = can.backtest_status || (scorecardV2 && scorecardV2.gate2 && scorecardV2.gate2.status)`. ACTION: 10-min diagnosis on real `*.scorecard.json` to confirm the empty-canonical case, then apply the frontend fallback (do NOT re-populate backend). Antigravity flagged it BLOCKER; the fix is small but the symptom (DONE-vs-FAIL) misleads decisions.
5. **R2-04 / R2-05 → BACKLOG.** Verdict/badge ladders are nice-to-have UX competing for the serial app.js owner against real bugs. Lighter fix if wanted later: a tooltip listing the ladder, NOT a stacked widget.
6. **R2-08a synthesis:** don't blind-remove the repaint chip — **drive it from canonical/metadata repaint flag, omit when no data.** Deleting loses a real signal where data exists.
7. **R2-11 + R2-19 = ONE label dictionary** (gate sub_scores + missing-fields + Gate3 alert_adapter/state_sync). Build once, not twice. Biggest single legibility win.
8. **R2-27 is not a relabel** — needs a real distinct-`base_strategy_id` count (=38) from the API/derived, AND the current tooltip ("Scored = has a Gate2 scorecard") is **actively wrong** (counts runs) → fix count + tooltip TOGETHER.
9. **Mechanism refinements (DeepSeek):** R2-02 root = `mtcV2Row.status_label` is humanized "Low Score Review" (spaces) vs `friendlyStatus` key `LOW_SCORE_REVIEW` (underscores) → normalize input (uppercase+underscore) before map lookup. R2-12 `max_points || "?"` also breaks for `max_points===0` (falsy) → use `!= null`. R2-16 better fix = a **system-gap banner above Gate3** (mirror Trading Rules banner :1095) "Gate3 scorer not built — all strategies INCOMPLETE", since `renderGateRow` has no per-gate branch; keep passLabel logic, add context.

### 7.3 Fix-masks-bug flags (question E — do NOT solve with copy alone)
- **R2-22 taxonomy:** "estimated" label is acceptable ONLY if shown **adjacent to the real tested TF/symbol** so the 10m-inferred "Scalping" vs tested-1D contradiction is visible. Otherwise the tag masks a data-model gap (no producer_spec strategy_type).
- **R2-06 blocker:** remove the fallback SOURCE (+1294 twin + mtc_v2_reader text), not just the visible string.
- **R2-23 journey:** do NOT tooltip/relabel in frontend — that hides a backend canonical/gate2-source bug.
- **R2-27 count:** fix the number, then label.
- **R2-12 "6/?":** real fix = scorecard PRODUCER emits `max_points`; UI null-guard is a stopgap — tag it as such.

### 7.4 Revised phase order (consensus)
**Front-load R2-23 diagnosis (10-min, backend, no commit).** Then:
1. **Trust-blockers first:** R2-27 (distinct count + tooltip), R2-06 + R2-28 twin (kill stale blocker at both sites + source), R2-22 (estimated label adjacent to tested TF).
2. **Gate readability:** R2-14 (status·passLabel collapse), R2-15 (FAIL/INCOMPLETE breakdown), R2-11 + R2-19 (one label dict), R2-12 (UI guard + producer note).
3. **Acceptance panel:** R2-25 (hide on detail) + R2-26 (sortable table, client-side only — no server sort param, read-only).
4. **QuantLens rename/placement:** R2-D1 "Gemini Pre-Screen" across ALL sites + R2-20 single placement.
5. **Low-risk copy/tooltips LAST:** R2-01, 03, 07, 08a, 08b, 09, 10, 13, 16, 17, 18.
- **Backend/reader work is hidden inside R2-06, R2-12, R2-22, R2-23, R2-27** → parallel side-track on `scorecard_reader.py` / `mtc_v2_reader.py` / `read_model.py`, NOT app.js.
- **Baseline drift:** several findings are stale vs current code (R2-03 tooltip now exists; R2-23 sampled row fixed). **Revalidate each finding against current code at dispatch time** before editing.

### 7.5 Read-only safety (question G) — confirmed safe
No planned fix introduces a write path. R2-D2 (display-only note, no dropdown, N2-B cancelled) respected. One watch: R2-26 sortable table must sort **client-side over loaded snapshot data** — no server sort param. No Pine/MTC_V2/parity edits in scope.

### 7.6 Outstanding
- All 4 reports in. **Reconciliation complete — ready to dispatch.**
- Top-5 first-fixes (merged 4-way consensus): **R2-23 diagnose+frontend-fallback → R2-27 count+tooltip → R2-06+R2-28 twin → R2-14 → R2-11+R2-19 label dict.**

### 7.7 New missed findings (DeepSeek + Antigravity, added)
- **R2-29** `documentedVsProven` shows "Documented and internally tested" even when gate2 = FAIL (evidence_level includes "Backtested" but the gate failed) — desync on FAIL. (app.js:738)
- **R2-30** FAIL gates do NOT auto-open (`autoOpen` only INCOMPLETE/PASS, app.js:873) — user can't see why Gate2 FAILed without clicking. Pair with R2-15.
- **R2-31** Data-freshness shows the *snapshot* timestamp, not the *scorecard* timestamp (UI-35 residual) — score could be days old while snapshot is fresh.
- **R2-32** Gate3 shows 10+ `alert_adapter.*`/`state_sync.*` N/A stubs even though the scorer was never built — consider hiding the stub list behind the "Gate3 scorer not built" banner (R2-16) instead of listing dead fields.
- **R2-33** Taxonomy "Tested timeframe: Not tested yet" while 7 TRXUSDT 1D runs are visible — `tested_tf` not reaching taxonomy chip.
- **R2-34** "Market not defined" while backtested on TRXUSDT — symbol not propagated to canonical/taxonomy.
- **R2-35** Taxonomy "Pullback / mean reversion" vs description "continuation pullbacks" — UI-25 misclassification STILL present for this strategy (`inferMarketCondition` order). 
- **R2-36** A Gate2 tooltip references a field that isn't emitted ("ghost requirement") — verify and drop.

### 7.9 IMPLEMENTATION PROGRESS (2026-06-07, Claude — Barış authorized direct coding)
**8 commits on master**, each `node --check` clean + key helpers verified on live data:
- `16c3c58` R2-0: R2-14 (label dedup), R2-23 (journey fallback), R2-12, R2-07, R2-08a, R2-01, R2-25
- `aaa089a` R2-06 (stale blocker source removed), R2-27 ("1 promotable · 38 strategies · 360 runs", verified =38)
- `0f684b8` R2-11/19 (humanizeMetric label dict), R2-15 (FAIL breakdown), R2-30 (auto-open FAIL), R2-17, R2-29/08b
- `5a92065` R2-16 (Gate3 "Not evaluated" + note), R2-18 (gate actions), R2-22/35/34 (taxonomy estimated + continuation + symbol)
- `e2bf40b` R2-D1 (QuantLens→"Gemini Pre-Screen" all visible text) + R2-20 (single placement, top badge removed)
- `cec2cf6` R2-09/10 (gates-first, run-list labelled), R2-24 (score↔evidence link), R2-26 (sortable acceptance table)
- `5f5f1a4` R2-02 (low-score tooltip fires via friendlyStatus normalize), R2-32 (hide dead Gate3 stubs)
- dead-code task spawned (renderDecisionPanel)

**SHIPPED: ~26 findings.** **REMAINING (minor/backlog):** R2-31 (scorecard-vs-snapshot freshness timestamp — low), R2-13-deep (AI deduction reasons — backlog), R2-36 (Gate2 "ghost" tooltip — unverified, low), R2-04/R2-05 (verdict/badge ladders — backlogged per audit). **SEPARATE PROJECT:** R2-E / R2-21 — QuantLens = Claude-authored verdict workflow (rubric in `11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md §4.2-4.4`).

### 7.8 Phase-order tweaks (consensus)
- **R2-22 + R2-27 → move to R2-A** (they're display/derived-count, not heavy backend).
- **R2-25 → R2-0** (1-line/CSS visibility toggle, trivial).
- **R2-23 → parallel side-track, investigate first** (frontend fallback, different concern from app.js cosmetics).
- **R2-33/34/35 → fold into R2-22** (same taxonomy/canonical-propagation cluster).
- **R2-29/30 → fold into R2-15** (FAIL-gate display cluster).
