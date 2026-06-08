# ROUND-2 PLAN AUDIT — DeepSeek v4 Pro

> Auditor: DeepSeek · Date: 2026-06-07 · Plan under audit: `ROUND2_PLAN.md`
> Code verified against actual `app.js` (2800 lines), `scorecard_reader.py` (329 lines), `read_model.py` (234 lines), `quantlens_reader.py` (203 lines). All line numbers confirmed unless noted.

## 1. Per-finding verdicts

Format: `ID | VERDICT (CONFIRM / CONFIRM-BUT / DISPUTE / NEED-DATA) | SEVERITY (BLOCKER/HIGH/MED/LOW) | NOTES (≤2 sentences; if CONFIRM-BUT give the corrected fix)`

### Carry-overs (§0)

| ID | VERDICT | SEVERITY | NOTES |
|----|---------|----------|-------|
| R2-02 (UI-7) | CONFIRM-BUT | HIGH | The map+tooltip exist (:594/610), but the fault is NOT that the map key misses — it's that `mtcV2Row.status_label` supplies *human-readable* "Low Score Review" (spaces) while `friendlyStatus` map key is `LOW_SCORE_REVIEW` (underscores). `statusText` returns "Low Score Review" unchanged; tooltip `includes("needs review")` fails. Fix: normalize input in `friendlyStatus` (uppercase+underscore before map lookup) OR add space-separated variants to the map. Plan's diagnosis of "label doesn't hit the map key" is correct, but the mechanism is wrong — not a key mismatch in the tooltip function, a key mismatch in `friendlyStatus`. |
| R2-06 (UI-10) | CONFIRM | BLOCKER | Confirmed. :688-691: canonical.blocking path works, but empty-case falls to `blocked_reason` → stale "score below 65" leaks. The fix (kill the fallback entirely, derive blocker from `gate_summary.blocking` only) is correct. Plan's Phase R2-D placement in backend phase is correct. |
| R2-15 (UI-16) | CONFIRM | MED | Confirmed. :877: sub-score detail only for `(status === "PASS" \|\| safeGate.pass === true)`. FAIL/INCOMPLETE get no breakdown. Plan's fix (show breakdown for all statuses when sub_scores exist) is correct. Note: this also interacts with R2-12 — the "6/?" bug shows for PASS gates, but FAIL/INCOMPLETE don't even show the sub-score table. |
| R2-23/24 (UI-26) | CONFIRM-BUT | BLOCKER | **R2-23:** Confirmed that journey and scorecard can desync. Root cause: `renderReviewJourney` (:1015) uses `can.backtest_status` while Scorecard Gate2 uses `scorecardV2.gate2.status` directly. When `canonical` is empty `{}` (before API attachment or cache miss) but `scorecardV2` IS populated, journey shows "pending" while scorecard shows FAIL. **Fix is NOT routine canonical populate** — backend already does it (`_canonical_backtest_status` returns `gate2_status` at scorecard_reader:253-258). Fix is frontend: at :1133, `renderBacktestEvidence` already falls back `can.gate2_status \|\| g2.status` — journey should do the same. Add `const g2Status = can.backtest_status \|\| (scorecardV2 && scorecardV2.gate2 && scorecardV2.gate2.status)` to `renderReviewJourney`. **R2-24:** Confirmed — score-view (Scorecard) and metric-view (Backtest Evidence) read as two sections. Both render from same data now (Phase 0 merge), but visually they're separate sections. Plan's "explicit link" approach is right. |
| R2-08a (UI-32) | CONFIRM | MED | Confirmed. :726: `"Repaint status unknown"` hardcoded in riskFlags array. Trading Rules at :1080-1088 correctly wire real repaint data. Plan's fix (remove the hardcoded chip) is correct. Note: the `!deterministic` helper at :723 also produces "Undefined rules" chip — if `eligible_for_backtest` is true, this chip may be misleading. Minor interaction with R2-08b. |

### Round-2 findings

| ID | VERDICT | SEVERITY | NOTES |
|----|---------|----------|-------|
| R2-01 | CONFIRM | LOW | Confirmed. :464 renders `title`, :466 renders `displayDescription` — both produce same text when strategy_name == description. Fix: if title equals description, suppress description line; or dedupe by comparing values before rendering. |
| R2-03 | CONFIRM-BUT | LOW | Confirmed gap — no tooltip on "QuantLens: Not evaluated yet". But the NON-evaluated state tooltip already exists in `renderQuantlensVerdict` (:636-642) providing full explanation. Plan wants a *badge-level* tooltip. Better fix: make the badge's `title` attribute point to the section's explanatory text, rather than duplicating explanation in two places. |
| R2-04 | CONFIRM | MED | Confirmed. :702-721: 6-level verdict ladder exists in `buildWaveADecision` but `renderVerdictDecision` shows only primary verdict + one badge (:759-785). Plan's fix (primary big + alternatives small below) is correct. Note: the ladder is *gate_summary-aware* since Phase 0 (line 700-701) — good. But the visual rendering doesn't expose it. |
| R2-05 | CONFIRM | LOW | Confirmed. :760-762: 3-state badge exists (Promotable/Can test/Blocked) but only one state shown at a time. Plan's fix (show all 3 as graded ladder with current highlighted) is UX polish, correct. |
| R2-07 | CONFIRM | MED | Confirmed. :724: `friendlyStatus(blocker)` in riskFlags chip + :774: `Blocking item · ${decision.blocker}` in terminal facts. Same value printed twice. Plan's fix (remove the riskFlags blocker chip, keep the fact row) is correct. |
| R2-08b | CONFIRM | LOW | Confirmed. :738: `evidenceLevel.includes("Backtested") ? "Documented and internally tested" : "Documented, not proven"`. Plan's rewording to "Rules written · internally tested" / "Rules written · not proven" is clearer. Good. |
| R2-09 | CONFIRM | MED | Confirmed. :808: `renderScorecardCaseList` renders 7-run list under Scorecard heading. The cases are backtest run data, not scorecard logic. Plan's proposal to clarify placement/label is correct. But moving the list *below* gates (R2-10) should come first — then label clarification. |
| R2-10 | CONFIRM | MED | Confirmed. :808: case list renders before :814: gate rows. Plan's fix (gates directly under Scorecard heading, run-list below) is correct layout. |
| R2-11 | CONFIRM | MED | Confirmed. :879: `s.source_metric \|\| s.criterion \|\| "—"` renders raw internal names like `intake.entry_pseudo_present`. :945: `row.source_metric \|\| row.criterion \|\| "unknown"` same for missing fields. Plan's fix (gate-field label dictionary: human-readable map per metric name) is correct. Note: this dictionary should live in ONE place, reused by both sub-scores and missing-fields. |
| R2-12 | CONFIRM | HIGH | Confirmed. :881: `s.max_points \|\| "?"` — when `max_points` is `null` or `undefined`, `\|\| "?"` fires correctly, but for `max_points=0` it would also return "?" (falsy). Should use `!= null` check instead: `s.max_points != null ? s.max_points : "?"`. Plan's Phase R2-0 placement is correct, but the fix description "null guard" should explicitly handle `0` case. |
| R2-13 | CONFIRM | LOW | Confirmed. :876-884: sub-scores table shows metric/value/points but no WHY line. Plan wants short deduction reason next to score. Correct, but this needs backend data (reason text per sub_score row). Plan correctly defers deep reasons to backlog (Phase R2-C surface, R2-13-deep backlog). |
| R2-14 (keystone) | CONFIRM | BLOCKER | Confirmed. :891: `<em>${statusText(status)} · ${passLabel}</em>`. `statusText` just replaces `_` with spaces. For PASS: "PASS · Pass", FAIL: "FAIL · Fail", INCOMPLETE: "INCOMPLETE · Pending". Three mappings produce doubled information. **This IS the highest-leverage fix** — one line change kills 3 visible duplications. Collapse: `status === "PASS" \|\| safeGate.pass === true ? "Pass" : status === "FAIL" \|\| safeGate.pass === false ? "Fail" : status === "INCOMPLETE" ? "Pending" : statusText(status)`. |
| R2-16 | CONFIRM-BUT | MED | Confirmed. :867-868: Gate3 INCOMPLETE → "Pending". Plan says change to "Not evaluated (scorer not built)". But this is a SYSTEM-WIDE gap — ALL strategies have INCOMPLETE Gate3. Better: add a system-gap banner above Gate3 (like Trading Rules' `systemic-gap-banner` at :1095-1096) saying "Gate3 scorer is not yet built — all strategies INCOMPLETE." Then keep `passLabel` as "Pending" but add the banner context. Also: the `renderGateRow` function has no per-gate customization — Gate3-specific wording requires a `key`-aware branch or a per-gate label override param. |
| R2-17 | CONFIRM | LOW | Confirmed. :897: `<span>Missing / not scored</span>` has no tooltip. Plan's fix is correct. |
| R2-18 | CONFIRM | LOW | Confirmed. :2616: `<span class="terminal-badge amber">Action required</span>` — generic text. Plan wants gate-specific action. Fix: derive action text from blocking gate names (already available from `gate_summary.blocking`). `blockingGateTooltip` at :917-926 already maps gate→description; reuse that logic. |
| R2-19 | CONFIRM | MED | Confirmed. Gate3 fields like `alert_adapter.*` / `state_sync.*` appear raw in `gateMissingFields` output (:940-948). Plan's fix (extend the label dictionary from R2-11) is correct. Note: for Gate3 specifically, these fields are N/A because the scorer isn't built — the dictionary + per-N/A reason is more honest than just relabeling. |
| R2-20 | CONFIRM | MED | Confirmed. :470: badge `decision.quantlensLabel` (top of hero) + :476: `quantlensVerdict` section. Plan says remove top badge, keep single section under Scorecard. Per R2-D1, the badge label should become "Gemini Pre-Screen" not "QuantLens". The plan's Phase R2-B placement is correct. |
| R2-21 | CONFIRM | — | Plan is correct: QuantLens = Claude verdict (separate project), no score. Single scoring = Scorecard. Phase R2-E separate project. No code change needed now beyond R2-D1 rename. |
| R2-22 | CONFIRM-BUT | HIGH | Confirmed. :951-1003: all taxonomy fields are heuristic inference (`inferTimeHorizon`, `inferMarketCondition`, `inferMethod`) from strategy name/IP. :963: "Complexity: Not defined yet" hardcoded. Per R2-D5, label as "estimated (inferred from name)". **BUT plan puts this in Phase R2-D (backend)** — the fix is display-only: add `(estimated)` suffix to each chip label. Move to Phase R2-A. The real backend SST (bind to `producer_spec.strategy_type`/`market_type`) is correctly backlogged. |
| R2-24 | CONFIRM | MED | (Covered under R2-23/24 carry-over above). Plan's fix: explicit link between Scorecard score and Backtest Evidence metrics is correct. |
| R2-25 | CONFIRM | MED | Confirmed. :156: `renderAcceptancePanel()` called in `render()` which runs on every page. index.html:51: `mccStatusPanel` sits before `strategyDetail` — visible on all tabs including detail. Per R2-D4 (hide on detail page), fix: add `if (state.selectedStrategyId)` guard to `renderAcceptancePanel` OR hide element when `synStrategyDetail` is visible. Phase R2-B. |
| R2-26 | CONFIRM | MED | Confirmed. :2578-2589: `renderAcceptanceRow` produces `<div class="mcc-status-row">` — not a sortable table. Per R2-D4, convert to `<table>` with sortable columns. Plan correctly places in Phase R2-B. |
| R2-27 | CONFIRM | MED | Confirmed. :2552: `summary.total` = `cards.length` = all scorecard cards (runs, not unique strategies). Per R2-D6, change to "N strategies · M backtest runs". Plan places in Phase R2-D — but this is FRONTEND label change only, could move to Phase R2-A. Backend already returns `scorecards.by_strategy` with distinct strategy count. |

## 2. Cross-cutting

**A. Carry-over diagnosis** (happy-path-fixed/edge-left accurate? other leaky Round-1 fixes not in §0?):

**Accurate but incomplete.** The "happy-path fixed, edge-case left" pattern IS the root cause for all 5 carry-overs. However, there are **at least 3 additional leaky Round-1 fixes NOT in the §0 list:**

1. **UI-18 → R2-16 partial:** Round 1 changed INCOMPLETE passLabel → "Pending" (line 867). But the `autoOpen` at :873 opens PASS and INCOMPLETE gates but NOT FAIL gates — FAIL gates stay closed. If a FAIL gate has sub_scores (possible: gate2 scoring can produce sub_scores even when aggregate FAIL), the user can't see the breakdown without manually clicking. This interacts with R2-15.

2. **UI-19 `scoreForGate` fix:** Round 1 removed the `status !== "OK"` guard → now shows score whenever `score != null` (:906-909). But `max_points` null shows "?" (R2-12) — this was a collateral gap from the Round 1 fix that was not caught.

3. **UI-4 "scored" counter:** Round 1 added `cards.length` tooltip text at :2553. But the root cause (counting runs not strategies) was only partially addressed — the tooltip explains the ambiguity but the number still says "360" which implies 360 strategies. R2-27 finally fixes this with R2-D6.

**B. Theme grouping** (7 themes right? is R2-14 truly highest-leverage?):

7 themes are correct and well-partitioned. **R2-14 IS the highest-leverage fix** — one line (891) kills three visible double-label complaints simultaneously. The second-highest is **R2-06** (stale blocker leak) because it's a data contradiction that directly misleads decisions. After that: R2-23 (journey desync) and R2-12 (max_points "?"). Cosmetic fixes (R2-08b, R2-16, R2-17) should come AFTER trust-critical data fixes.

**C. Missed findings** (in screenshots/code, not covered by R2-01..27):

1. **MISS-R2-1 — Gate2 threshold copy inconsistency:** Although D3b resolved to binary ≥75 PASS / <75 FAIL and the caption at :807 says "≥75 PASS · <75 FAIL", the `_gate2_band` backend function at scorecard_reader:245-250 also returns only PASS/FAIL. Good — consistent. BUT the `blockingGateTooltip` at :922 still says "score below 75, backtest metrics missing, or walk-forward incomplete" — the "walk-forward incomplete" part is a ghost requirement (no walk-forward data exists). Remove or qualify.

2. **MISS-R2-2 — `documentedVsProven` at :738 uses `evidenceLevel` from `buildWaveADecision`:** But `evidenceLevel` (:694) comes from `can.evidence_level` which is set by `_canonical_evidence_level` (scorecard_reader:261-282). This function can return `gate2_fail` when gate2 fails — but `evidenceLevel.includes("Backtested")` at :738 would be FALSE for "gate2_fail" → shows "Documented, not proven" for a strategy that WAS backtested (just failed). Should check `gate2_status` directly: "Backtested (not passed)" vs "Not backtested".

3. **MISS-R2-3 — FAIL gate `autoOpen` at :873:** `status === "PASS" \|\| safeGate.pass === true` opens gates, `status === "INCOMPLETE"` opens gates, but FAIL gates stay closed. Users can't see WHY a gate failed without clicking. Given R2-15 wants breakdown for FAIL gates, auto-open FAIL gates too. Add `status === "FAIL"` to the condition.

4. **MISS-R2-4 — Data freshness on detail page:** Round 1 had UI-35 (data-freshness timestamp). `snapshotFreshness()` at :524-529 exists and is called at :463. But it reads `current_status.last_updated` — this is the SNAPSHOT timestamp, not the SCORECARD timestamp. Scorecard data comes from backtest run files which have their own timestamps. The freshness tag says "Data: 2026-06-07T..." but the backtest might be from last week. Add scorecard-specific freshness.

5. **MISS-R2-5 — Gate3 field names are not the same across strategies:** The `alert_adapter.*` / `state_sync.*` fields from R2-19 are data model specific to the Gate3 scorer builder (not implemented). Since ALL Gate3s are INCOMPLETE, these field names come from a template, not actual data. The R2-19 fixture should check: are the field names in `sub_scores` actually populated or are they placeholder stubs? If stubs, don't display them at all — just show "Gate3 scorer not built".

**D. False positives** (R2 finding that is correct behavior → drop):

**None outright false.** But two are borderline:

1. **R2-03** is very low priority — the tooltip gap is small (QuantLens section already has full explanation). Could be deferred to Phase R2-E when QuantLens is actually built.

2. **R2-09** (7-run list under Scorecard) — the case list IS scorecard data (each case is a scorecard run). Calling it "Backtest data" is misleading. Better framing: keep it under Scorecard but label it "Scored runs" (not "Backtest data").

**E. Fix-masks-bug** (tooltip/relabel hiding a real data-model bug → fix backend instead):

| Finding | Mask risk | Verdict |
|---------|-----------|---------|
| **R2-22** taxonomy "estimated" label | LOW — R2-D5 explicitly wants honest estimation until real source exists. Not masking. | Accept. |
| **R2-23** journey desync | HIGH — the plan says "sync canonical.backtest_status populate" (backend). But as shown in §1, the backend ALREADY populates it. The real fix is frontend (fallback to `scorecardV2.gate2.status` when canonical is empty). The plan's diagnosis of "backend canonical not populated" may be wrong — verify with real snapshot data before writing backend code. | Investigate first. |
| **R2-06** blocker fallback | HIGH — adding a tooltip on "score below 65" would mask stale data. Plan correctly fixes the root: kill the `blocked_reason` fallback. | Correct approach. |
| **R2-16** Gate3 "Not evaluated (scorer not built)" | NONE — this is honest labeling of a genuine system gap. | Correct approach. |
| **R2-19** Gate3 field relabeling | MEDIUM — relabeling `alert_adapter.something` to a human name doesn't change the fact that these are placeholder/stub fields with no real data. Better to suppress the fields entirely and show a system-gap message. | Fix: suppress, don't relabel. |
| **R2-08b** wording change | NONE — pure copy. | Accept. |

**F. Phase order & dependencies** (R2-0→A→B→C→D→E correct? any "display-only" item secretly backend?):

**Partially wrong.** Issues:

1. **R2-22 (taxonomy) is in Phase R2-D (backend) but is display-only** — the fix per R2-D5 is `(estimated)` suffix. Move to Phase R2-A.

2. **R2-23 (journey desync) is in Phase R2-D but may be frontend-only** — as shown above, backend already populates canonical. The frontend fallback chain is the likely issue. Investigate before backend work. If frontend, move to Phase R2-C or earlier.

3. **R2-27 (scored counter) is in Phase R2-D but is frontend-only** — just a label change + distinct count from `scorecards.by_strategy`. Move to Phase R2-A.

4. **R2-12 fix should handle `max_points=0`** — currently only handles `null/undefined`. The fix description in Phase R2-0 should note this.

5. **R2-16 and R2-19 interact:** Gate3-specific wording (R2-16) and Gate3 field relabeling (R2-19) both touch the `renderGateRow` function. Should be serialized or merged into one pass.

**Revised phase order recommendation:**

| Phase | Items | Rationale |
|-------|-------|-----------|
| **R2-0** | R2-14, R2-07, R2-08a, R2-12, R2-01 | Keystone dedup. No change. |
| **R2-A** | R2-11, R2-19, R2-02, R2-03, R2-08b, R2-16, R2-17, R2-18, **R2-22** (moved), **R2-27** (moved) | Dictionary + wording. R2-22 and R2-27 are display-only, belong here. |
| **R2-B** | R2-10, R2-09, R2-20, R2-24, R2-25, R2-26 | Layout. No change. |
| **R2-C** | R2-04, R2-05, R2-15, R2-13, **R2-23 frontend fix** (moved if confirmed) | Verdict ladder + score breakdown. |
| **R2-D** | R2-06, R2-23 (only if backend fix needed) | Backend SST — verify R2-23 diagnosis first. |
| **R2-E** | R2-21, D1 rename | Separate project. No change. |

**G. Read-only safety** (any fix risks a write path / Pine/MTC_V2/parity violation?):

**No violations.** All planned fixes are:
- app.js: display-only HTML/CSS/label changes
- scorecard_reader.py: read-only JSON parsing (already read-only)
- read_model.py: data assembly (already read-only)
- quantlens_reader.py: YAML reading (already read-only, Phase 0 added `strategies/` scan)

Phase R2-E (QuantLens Claude verdict) is a SEPARATE project with its own Gate 0 read of design docs. No Pine, MTC_V2, or parity files touched. No write paths introduced (R2-D2 explicitly cancelled write-back). **ALL SAFE.**

**H. Top 5 to fix first** for maximum trust gain given limited effort/credit:

| Rank | ID | Effort | Rationale |
|------|----|--------|-----------|
| 1 | **R2-14** | 1 line | Keystone — kills 3 visible double-labels. Maximum impact per character typed. |
| 2 | **R2-06** | ~5 lines | Stale blocker leak = data contradiction. Directly misleads promotion decisions. Kill `blocked_reason` fallback entirely. |
| 3 | **R2-12** | 1 line | "6/?" looks broken. Simple `!= null` check. |
| 4 | **R2-23** | ~3 lines | Journey desync with scorecard erodes trust in the page's consistency. Add `scorecardV2` fallback to journey backtest_status. |
| 5 | **R2-02** | ~3 lines | "Low Score Review" tooltip never fires — users can't understand what it means. Normalize key in `friendlyStatus`. |

Honorable mention: **R2-22** taxonomy "estimated" label — trivial display fix, high trust impact because it's honest about data limitations. Could swap with #5.

## 3. Line-number corrections (any `app.js:LINE` in the plan that is wrong)

| Plan claim | Plan line | Actual verified | Correction |
|------------|-----------|-----------------|------------|
| R2-01: app.js:464/466 | 464, 466 | ✅ Correct — 464=h3 title, 466=p description | — |
| R2-02: app.js:594/610 | 594, 610 | ✅ Correct — 594=map entry, 610=tooltip check | But mechanism wrong (see §1 R2-02) |
| R2-03: no line ref | — | ✅ N/A — no line number claimed | — |
| R2-04: app.js:702-721 | 702-721 | ✅ Correct — verdict ladder in buildWaveADecision | — |
| R2-05: app.js:761 | 761 | ✅ Correct — verdictBadgeLabel | — |
| R2-06: app.js:688-691 | 688-691 | ✅ Correct — 690=blocked_reason fallback | — |
| R2-07: app.js:774 | 774 | ✅ Correct — Blocking item fact | Also :724 = riskFlags chip |
| R2-08a: app.js:726 | 726 | ✅ Correct — hardcoded chip | — |
| R2-08b: app.js:738 | 738 | ✅ Correct — documentedVsProven | — |
| R2-09/10: app.js:808 vs 814 | 808, 814 | ✅ Correct — 808=caseList, 814=gates | — |
| R2-11: app.js:879/945 | 879, 945 | ✅ Correct — 879=sub_scores metric, 945=missing field source | — |
| R2-12: app.js:881 | 881 | ✅ Correct — max_points \|\| "?" | — |
| R2-13: app.js:876 | 876 | ✅ Correct — subScores array start | — |
| R2-14: app.js:891/867 | 891, 867 | ✅ Correct — 891=statusText·passLabel, 867=passLabel | — |
| R2-15: app.js:877 | 877 | ✅ Correct — PASS-only guard | — |
| R2-16: app.js:881 | (no specific line) | Uses line 867-868 — passLabel logic | Reference is approximate |
| R2-17: app.js:897 | 897 | ✅ Correct — "Missing / not scored" span | — |
| R2-18: app.js:2616 | 2616 | ✅ Correct — "Action required" badge | — |
| R2-20: app.js:470/476 | 470, 476 | ✅ Correct — 470=top badge, 476=section | — |
| R2-22: app.js:951/984/993/1003 | 951, 984, 993, 1003 | ✅ Correct — 951=renderTaxonomy, 984=inferTimeHorizon, 993=inferMarketCondition, 1003=inferMethod | :963 = "Complexity: Not defined yet" hardcoded |
| R2-23: app.js:1015 | 1015 | ✅ Correct — backtestStatus line | — |
| R2-25: app.js:156, index.html:51 | 156, 51 | ✅ Correct — 156=renderAcceptancePanel call, index.html:51=mccStatusPanel element | — |
| R2-26: app.js:2578 | 2578 | ✅ Correct — renderAcceptanceRow start | — |
| R2-27: app.js:2552 | 2552 | ✅ Correct — countLabel construction | — |

**All line numbers verified. None are wrong.** Minor: R2-16 has no explicit line ref in the plan; it's the `passLabel` logic at :867-868.

## 4. Additional observations

- **Phase 0 (Round 1) already shipped `isPromotable` unification** at :911-914 — checks `v === true \|\| v === 1 \|\| v === "1" \|\| v === "true"`. This is the same helper used everywhere. UI-37 resolved. ✅
- **`build_canonical_display_row` at scorecard_reader:180** correctly derives all canonical fields from scorecard_v2. The function is clean. The issue for R2-23 is NOT backend but frontend fallback. ✅
- **`renderGateRow` at :862** is a general-purpose renderer with no per-gate customization. Several R2 fixes (R2-16, R2-19) need gate-specific behavior. Adding a `gateKey`-aware branch at the summary line would handle both without restructuring.
- **R2-25 index.html:51:** The `#mccStatusPanel` element at index.html:51 is a `<section>` with class `mcc-status-panel`, NOT hidden by default. The plan says "pipeline-only" — consider adding `data-panel="pipeline"` attribute for visibility sync with tab system, same approach as other tab panels.

---
*End of audit.* All code line numbers verified against actual source. Cross-cutting concerns flagged with severity. Top 5 correctly ordered for execution.
