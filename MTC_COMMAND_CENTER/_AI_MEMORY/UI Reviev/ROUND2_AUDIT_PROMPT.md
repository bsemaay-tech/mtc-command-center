# AUDIT REQUEST — MCC Strategy-Detail Dashboard UI · ROUND 2 PLAN (27 findings + 5 carry-overs)

You are auditing a **plan**, not raw findings. Another engineer (Claude Opus 4.8, orchestrator) ran a second section-by-section walkthrough of the strategy-detail page WITH the product owner (Barış), after Round 1 already shipped 38 fixes. The output is `ROUND2_PLAN.md` in this folder. **Your job: stress-test that plan** — confirm/challenge each finding, catch fixes that merely mask data bugs, verify the carry-over diagnosis, check phase order and dependencies, flag anything missed, and confirm the plan respects the hard constraints. Do NOT redo the review from scratch.

## Files & environment (everything is in THIS folder)

All paths below are relative to `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/`.

- **`ROUND2_PLAN.md`** — THE PLAN UNDER AUDIT. Read it fully first. It contains: carry-over partials (§0), findings R2-01..R2-27 (§1, each with `app.js:LINE` refs), 7 themes (§2), 6 resolved decisions (§3), 6 execution phases (§4), backlog (§5), dispatch model (§6).
- **`ARCHİVE 1/MCC_UI_AUDIT_PLAN.md`** — Round-1 plan (the 38 findings UI-1..UI-39 + decisions D1..D9) for context on what was already done.
- **5 round-2 screenshots** (current post-Round-1 state, one strategy detail, top→bottom):

| # | File | Section shown |
|---|------|---------------|
| 1 | `Ekran görüntüsü 2026-06-07 211721.png` | MCC Acceptance Status (global banner) |
| 2 | `Ekran görüntüsü 2026-06-07 211746.png` | Strategy header + Verdict & Decision |
| 3 | `Ekran görüntüsü 2026-06-07 211806.png` | Scorecard — gates + 7-run case list + Missing/not scored |
| 4 | `Ekran görüntüsü 2026-06-07 211857.png` | Gate 3 fields + QuantLens Verdict + Strategy Taxonomy |
| 5 | `Ekran görüntüsü 2026-06-07 211911.png` | Review Journey + Trading Rules + Backtest Evidence |

**Source of truth = the actual code.** Verify every `app.js:LINE` claim against `08_DASHBOARD_APP/apps/web/app.js` and the API readers in `08_DASHBOARD_APP/apps/api/mcc_readonly/` (`scorecard_reader.py`, `read_model.py`, `quantlens_reader.py`). If you can run it, check against a real snapshot (`/api/snapshot`) and a real `*.scorecard.json`. Do not trust the plan's line numbers blindly — confirm them.

**Where to write your report** — fill ONLY your own file; do not touch others, the prompt, or the plan:
- Codex → `AUDIT_REPORT_Codex_R2.md`
- DeepSeek → `AUDIT_REPORT_DeepSeek_R2.md`
- Antigravity → `AUDIT_REPORT_Antigravity_R2.md`
- Claude → `AUDIT_REPORT_Claude_R2.md`

Each file has a skeleton (per-finding table + cross-cutting questions). Fill it. If you cannot write files, output the full report in chat in the same structure.

---

## System context (read before judging)

- **MCC = "MTC Command Center"** — a **read-only** dashboard over a strategy-research pipeline. It displays artifacts; it does NOT compute scores. **HARD CONSTRAINT: the dashboard must stay read-only.** Any "fix" that writes user state back (e.g. a decision dropdown) is OUT — the owner ruled this out permanently (R2-D2).
- **Stack:** single-file vanilla-JS frontend (`app.js`, template-string rendering) + read-only Python API (`scorecard_reader.py` loads `scorecard_v2` JSON; `read_model.py`; `quantlens_reader.py`). Round 1 added a **canonical derived display-row** (`build_canonical_display_row`) in the API as the single source of truth (UI-36).
- **4 gates:** Gate1 Intake, Gate1B MTC Feasibility, Gate2 Backtest Evidence (/100; **binary ≥75 PASS · <75 FAIL** per owner decision D3b — no CONDITIONAL band exists in the backend), Gate3 Production Readiness.
- **Known system gaps (real, not per-strategy bugs):** Gate3 scoring builder **not implemented** (all strategies INCOMPLETE on Gate3); `producer_spec` SL/TP/risk fields empty for many strategies; QuantLens-as-Claude-verdict not built yet.
- **QuantLens naming (critical for Round 2):** the data currently labeled "QuantLens" in the dashboard comes from a **Gemini GEM pre-screen import** (`quantlens_reader.py` scanning candidate metadata). The owner clarified this is NOT what he means by QuantLens: he wants "QuantLens" to be **Claude's own expert verdict** (opinion only, **no score** — the only score is the Scorecard). Round-2 decision R2-D1: **rename the Gemini-origin data to "Gemini Pre-Screen"**, reserve "QuantLens" for the future Claude-verdict workflow (separate project, Phase R2-E). Rubric for the Claude verdict already exists at `03_QUANTLENS/_user_guide/11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md §4.2-4.4`.
- **The example strategy:** YouTube "8 EMA purple line Amazon trade", defined TF 10m, backtested TRXUSDT 1D.

### What changed since Round 1 (so you judge the right baseline)
Round 1 shipped 33 fixes fully + 5 partial. The orchestrator's own re-verification found the 5 partials all share one pattern: **Round 1 fixed the happy path (PASS / promotable / canonical-populated) but left edge cases (FAIL, empty canonical, legacy fallback) untreated.** These are §0 carry-overs in the plan. **Independently confirm this diagnosis** — is it accurate, and is it the *only* such pattern, or are there other Round-1 fixes that are similarly leaky and NOT yet caught?

### Carry-over partials to verify (Round-1 "done" that leak)
- **R2-02 (UI-7):** `LOW_SCORE_REVIEW→"Needs review"` map + tooltip exist (`app.js:594/610`) but the on-screen label "Low Score Review" doesn't hit the map key → tooltip never fires. Confirm the actual data value vs the map key.
- **R2-06 (UI-10):** blocker uses `canonical.blocking` first (good) but empty-case falls back to legacy `blocked_reason` → stale "score below 65" still shows (`app.js:688-691`). Confirm the fallback path.
- **R2-15 (UI-16):** sub-score breakdown renders only for PASS gates (`app.js:877`); FAIL/INCOMPLETE show none.
- **R2-23/24 (UI-26):** Evidence section merged, but Journey `backtest_status` desyncs from the Scorecard FAIL (`app.js:1015-1016`), and score-view vs metric-view still read as two backtests.
- **R2-08a (UI-32):** repaint wired into Trading Rules, but a separate hardcoded "Repaint status unknown" chip remains in Verdict riskFlags (`app.js:726`).

---

## The Round-2 findings to audit (R2-01 … R2-27)

Full text + line refs in `ROUND2_PLAN.md §1`. Compact list (verify each against code):

**T1 dedup / double-label:** R2-01 title==description dup · R2-07 blocker shown twice (fact + chip) · **R2-14 (keystone)** `statusText(status) · passLabel` emits "OK·Pass"/"FAIL·Fail"/"INCOMPLETE·Pending" (`app.js:891/867`) · R2-20 QuantLens shown twice (top badge `:470` + section `:476`) · R2-08a repaint hardcoded chip.

**T2 wording / field dictionary / tooltips:** R2-02 low-score tooltip · R2-03 "QuantLens: Not evaluated" tooltip · R2-08b "Documented and internally tested" wording · R2-11 raw code names in gate detail (`intake.entry_pseudo_present`, `app.js:879/945`) · R2-16 Gate3 "Incomplete·Pending"→"Not evaluated (scorer not built)" · R2-17 "Missing / not scored" tooltip · R2-18 "Action required" → gate-specific action · R2-19 Gate3 fields (`alert_adapter.*`/`state_sync.*`) raw + bare N/A.

**T3 layout:** R2-09 7-run list is backtest data under Scorecard · R2-10 gates should sit directly under Scorecard heading (`:808` vs `:814`) · R2-20 QuantLens single placement · R2-24 Scorecard score-view ↔ Backtest-Evidence metric-view merge/link · R2-25 Acceptance banner appears on every detail page · R2-26 Acceptance list → sortable table.

**T4 verdict ladder:** R2-04 6-level verdict ladder hidden (`app.js:702-721`) · R2-05 3-state badge ladder hidden (`:761`).

**T5 score breakdown:** R2-12 "6/?" `max_points` null (`:881`) · R2-13 short why-deducted (deep→backlog) · R2-15 breakdown for FAIL/INCOMPLETE.

**T6 SST / data bugs (backend):** R2-06 stale blocker leak · R2-22 taxonomy heuristic, no SST (`:951/984/993/1003`, "Complexity" hardcoded `:963`) · R2-23 Journey backtest_status desync · R2-27 "360 scored" = card count not strategies (`:2552`).

**T7 QuantLens project (separate):** R2-21 QuantLens writes opinion, NO score — single scoring = Scorecard.

### Resolved owner decisions (do NOT relitigate; judge whether the plan implements them correctly)
- **R2-D1** Gemini-origin → "Gemini Pre-Screen"; "QuantLens" = future Claude verdict (separate project).
- **R2-D2** Low-score = display-only note ("Needs your decision: promote/retest/park"). **No write-back, ever. Dashboard read-only forever.**
- **R2-D3** UI language = English.
- **R2-D4** Acceptance banner hidden on detail page (pipeline-only) + promotable list → sortable table.
- **R2-D5** Taxonomy labeled "estimated (inferred from name)" now; swap to real source later (producer_spec / QuantLens verdict).
- **R2-D6** scored counter → "N strategies · M backtest runs".

---

## What I want from you

### 1. Per-finding verdicts
For **each** R2-01..R2-27 (and each §0 carry-over), one compact row:

`ID | VERDICT | SEVERITY | NOTES`

- **VERDICT:** `CONFIRM` (real, plan's fix is right) · `CONFIRM-BUT` (real, but the planned fix is wrong/incomplete/masks a data bug — give the better fix) · `DISPUTE` (not a real problem — explain) · `NEED-DATA` (can't judge; say what data).
- **SEVERITY:** `BLOCKER` (data contradiction misleading decisions) · `HIGH` · `MED` · `LOW` (cosmetic/copy).
- **NOTES:** ≤2 sentences. If CONFIRM-BUT, state the corrected fix.

### 2. Cross-cutting questions
- **A. Carry-over diagnosis:** Is the "happy-path fixed, edge-case left" pattern accurate? Are there OTHER Round-1 fixes that are similarly leaky but NOT in the §0 list? Name them.
- **B. Theme grouping:** Are the 7 themes right? Is **R2-14 (status·passLabel)** truly the highest-leverage single fix, or is something else more fundamental?
- **C. Missed findings:** Anything in the 5 screenshots or implied by the code that R2-01..27 do NOT cover? (Look especially at sections Round 1 claimed done.)
- **D. False positives:** Any R2 finding that is actually correct behavior and should be dropped?
- **E. Fix-masks-bug check:** For T2 (wording/tooltips), flag any case where adding a tooltip/relabel hides a real data-model bug that should be fixed in the backend instead (e.g. R2-22 taxonomy, R2-23 journey desync, R2-06 blocker leak).
- **F. Phase order & dependencies:** Is the R2-0→A→B→C→D→E sequence correct given the read-only constraint and the app.js-single-file serial bottleneck? What must move? Are any "display-only" items secretly backend (canonical/reader) work?
- **G. Read-only safety:** Does any planned fix risk introducing a write path or violating the read-only / no-Pine/MTC_V2/parity constraint?
- **H. Top 5 to fix first** for maximum trust gain given limited effort/credit.

Be blunt. Prioritize correctness contradictions over cosmetics. **If a planned "fix" is a tooltip masking a data-model bug, say so explicitly (question E).** Confirm line numbers against the real code — flag any that are wrong.
