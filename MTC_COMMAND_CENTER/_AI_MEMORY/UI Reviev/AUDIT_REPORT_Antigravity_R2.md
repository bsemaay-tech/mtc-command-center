# AUDIT REPORT — Round 2 Plan · Antigravity

**Date:** 2026-06-07 · **Auditor:** Antigravity (Claude Opus 4.6 Thinking)  
**Source of truth:** `app.js` at commit `40032cd` (post-Phase B3), verified line-by-line.  
**Screenshots:** 5 screenshots viewed and cross-referenced.

---

## 1. Per-Finding Verdicts

### §0 Carry-Over Partials

| ID | VERDICT | SEV | NOTES |
|----|---------|-----|-------|
| R2-02 (UI-7) | **CONFIRM-BUT** | MED | The plan says `LOW_SCORE_REVIEW→"Needs review"` map at L594 exists but "displayed label doesn't hit the map key." **Verified correct.** `friendlyStatus` (L590-605) maps `LOW_SCORE_REVIEW` → `"Needs review"` and `statusBadgeTooltip` (L608-615) checks `text.includes("needs review")`. **The real question is whether the input is the raw constant `"LOW_SCORE_REVIEW"` or a pre-humanized `"Low Score Review"`.** If the MTC_V2 reader passes `status_label="Low Score Review"` (already humanized), `friendlyStatus` won't match the map → returns `statusText("Low Score Review")` = `"Low Score Review"` → tooltip `includes("needs review")` still fires (lowercase match). **BUT** the badge then reads "Low Score Review" not "Needs review". Fix should normalize the input: `friendlyStatus` should also match case-insensitive or the reader should be checked. |
| R2-06 (UI-10) | **CONFIRM** | BLOCKER | Verified at L688-691. `canBlocking.length` check is correct, but when `canonical.blocking` is an empty array (which it is for strategies without gate_summary), the fallback to `auditRow.blocked_reason` fires — confirmed stale "score below 65" leak. This is a data-model bug being masked by display fallback. The plan correctly identifies this. Fix: default to `"None"` when canonical.blocking is empty AND eligible, never fall through to legacy. |
| R2-15 (UI-16) | **CONFIRM** | HIGH | Verified at L877: `(status === "PASS" || safeGate.pass === true) && subScores.length` — only PASS gets breakdown. FAIL gates with `sub_scores` present (like Gate 2 with 68.76) show no breakdown at all. The plan's fix (show for all gates) is correct. |
| R2-23 (UI-26) | **CONFIRM** | BLOCKER | **Screenshot 4 confirms:** Journey says "Backtested: PENDING — Backtest evidence not available yet" while Backtest Evidence section shows "FAIL 68.76/100". Code at L1015-1016: `can.backtest_status` is checked, but this strategy's `canonical.backtest_status` is apparently empty/null despite having a `gate2.status = FAIL` in the scorecard. The root cause is in `build_canonical_display_row` — it may not be populating `backtest_status` from `gate2.status` for FAIL cases. **This is a backend bug, not just a display fix.** |
| R2-08a (UI-32) | **CONFIRM** | MED | Verified at L726: `"Repaint status unknown"` is a hardcoded string in riskFlags array, always emitted regardless of whether repaint data exists. Screenshot 1 confirms "REPAINT STATUS UNKNOWN" chip visible. Remove it; the Trading Rules section already shows the real repaint data. |

### R2-01 … R2-27

| ID | VERDICT | SEV | NOTES |
|----|---------|-----|-------|
| R2-01 | **CONFIRM** | LOW | Title (L464 `title`) and description (L466 `displayDescription`) can be identical when the only source for both is `description.family` or `row.name`. Screenshot 1 confirms: "8 EMA purple line Amazon trade" appears as both title and description text "Buys continuation pullbacks to the 8 EMA during an uptrend." — these are different here, but for many strategies they'll be the same. Fix: suppress description if `title === displayDescription`. |
| R2-02 | **CONFIRM-BUT** | MED | See carry-over analysis above. Plan says "normalize label → map key" — correct direction, but the actual fix depends on what `mtcV2Row.status_label` contains. Check the reader first. |
| R2-03 | **CONFIRM** | LOW | L470: QuantLens badge has a long inline `title` attribute now (added in Phase B2). Plan says "no tooltip" — **this was partially fixed in Round 1 Phase B2.** The current tooltip reads "QuantLens is a separate AI pre-screen…" BUT the text says "QuantLens: Not in scope (separate AI pre-screen)" — it IS there. **Downgrade to cosmetic: the tooltip exists now, just may need wordsmith.** |
| R2-04 | **CONFIRM** | MED | L702-721 has the 6-level cascade but only the winner is shown (L770). The plan to show all levels as a graded ladder is a UX enhancement, not a bug. Correct finding, correct priority. |
| R2-05 | **CONFIRM** | LOW | L760-761: 3-state badge (Promotable/Can test/Blocked) exists but is a single badge, not a visible ladder. This is UX polish — the badge already shows the correct state. |
| R2-06 | **CONFIRM** | BLOCKER | See carry-over. Verified stale leak path. |
| R2-07 | **CONFIRM** | MED | L774 "Blocking item: None" in facts + L724 adds `friendlyStatus(blocker)` to riskFlags chips. When blocker != "None", the same text appears in both locations. Plan says remove the chip, keep the fact — correct, the fact row is more informative. |
| R2-08a | **CONFIRM** | MED | See carry-over. L726 hardcoded string. |
| R2-08b | **CONFIRM** | LOW | L738: `"Documented and internally tested"` vs `"Documented, not proven"`. Wording is functional but could be clearer. Low priority. Plan ref says L738 — **verified correct.** |
| R2-09 | **CONFIRM** | MED | L808: `renderScorecardCaseList` (the 7-run list) renders inside the Scorecard section but is conceptually backtest run data. Screenshot 2 confirms: 7 case rows (TRXUSDT Tested: 1D) with scores appear above the gates. Plan's suggestion to label/relocate is valid. |
| R2-10 | **CONFIRM** | MED | L808 vs L814: case list renders before gates. Plan says gates should be directly under heading, case list below. This is a layout preference — both orderings are defensible, but gates-first-then-runs is clearer for the "gate verdict → supporting evidence" flow. |
| R2-11 | **CONFIRM** | HIGH | Screenshot 2 confirms raw code names: `intake.entry_pseudo_present`, `intake.exit_pseudo_or_delegated`, `feasibility.signal_reducible`. L879/945: `source_metric || criterion` is rendered raw. **No human-label dictionary exists.** This is a real readability problem. Plan's fix (field dictionary) is correct. |
| R2-12 | **CONFIRM** | HIGH | Screenshot 2 confirms `6/?`, `16/?`, `20/?`, etc. L881: `s.max_points || "?"` — when `max_points` is null/0, it shows "?". **All sub_scores in Gate 1 and Gate 1B show `/?" in the screenshot.** This is a widespread data issue, not just one gate. Fix: if `max_points` is null, don't show denominator at all, or look up from gate total. |
| R2-13 | **CONFIRM** | LOW | L876: sub-score shows metric/value/points but no deduction reason. Plan correctly defers deep AI reasons to backlog — correct prioritization. |
| R2-14 | **CONFIRM** | HIGH | **Verified as keystone.** L891: `${escapeHtml(statusText(status))} · ${escapeHtml(passLabel)}` emits "OK · Pass", "FAIL · Fail", "INCOMPLETE · Pending". Screenshot confirms all three visible. `statusText("OK")` → "OK" (no transform), passLabel = "Pass" — semantically identical, just different casing. Single collapsed label is the right fix. **Line number plan says `:891/867` — actual is L891 (render) and L866-868 (passLabel logic). Confirmed.** |
| R2-15 | **CONFIRM** | HIGH | See carry-over. FAIL Gate 2 in screenshot 3 shows "FAIL · Fail" label only — no sub-score breakdown despite having `sub_scores` data. |
| R2-16 | **CONFIRM** | MED | Screenshot 3: Gate 3 shows "INCOMPLETE · Pending". Plan says show "Not evaluated (Gate3 scorer not built)". This is accurate — Gate 3 scorer is a known system gap, and "Pending" misleadingly implies it's coming. |
| R2-17 | **CONFIRM** | LOW | L897: "Missing / not scored" heading has no tooltip. Screenshot 3 shows the list but no explanation of why these metrics are N/A. Tooltip would help but is low impact. |
| R2-18 | **CONFIRM-BUT** | MED | Plan ref says L2616 — **incorrect line number.** The "Action required" badge is in `renderPromotabilityPanel` (now "Gate Blockers" panel). Actual location is approximately L2549-2558 (the repurposed function). The badge just says "Action required" with no gate-specific guidance. Plan's fix is right but the line number in the plan is wrong by ~35 lines. |
| R2-19 | **CONFIRM** | HIGH | Screenshot 3 confirms: `alert_adapter.tv_alert_json_convertible`, `state_sync.strategy_vs_broker_state_comparable`, etc. — all raw internal names with bare `(N/A)`. Same dictionary fix as R2-11 but for Gate 3 fields specifically. These are production-readiness checks that need human labels. |
| R2-20 | **CONFIRM** | MED | Screenshot 1 confirms: hero badge "QUANTLENS: NOT IN SCOPE (SEPARATE AI PRE-SCREEN)" (L470) + full "QuantLens Verdict" section below (L476 → `quantlensVerdict`). Two visual representations. Plan says remove top badge, keep section — reasonable. **But note:** when QuantLens IS present (has data), the badge shows the actual decision label, which is useful quick-glance info. Consider keeping badge for present case, removing only for empty case. |
| R2-21 | **CONFIRM** | HIGH | This is a separate project (Phase R2-E). Plan correctly isolates it. The rename from "QuantLens" to "Gemini Pre-Screen" for the current data is the right first step. No code action needed now beyond the rename. |
| R2-22 | **CONFIRM-BUT** | MED | L951-963: taxonomy is entirely heuristic (`inferTimeHorizon`, `inferMarketCondition`, `inferMethod`). "Complexity" at L963 is hardcoded `"Not defined yet"`. Plan says "label as estimated" (R2-D5) — **correct, but the plan's Phase R2-D placement (SST/data bugs, backend) is wrong.** This is a pure display label fix: add "(estimated)" suffix to taxonomy heading. It's Phase R2-A work (wording), not backend. |
| R2-23 | **CONFIRM** | BLOCKER | See carry-over. **Screenshot 4 provides smoking gun:** Journey says "PENDING" for Backtested while screenshot 5 shows "Backtest Evidence: FAIL 68.76/100". Root cause: `canonical.backtest_status` is not populated from `gate2.status`. **This is a backend fix** in `build_canonical_display_row`. |
| R2-24 | **CONFIRM** | MED | Screenshot 2 (Scorecard with case list showing 68.76/100 FAIL) vs screenshot 5 (Backtest Evidence with 68.76/100 FAIL) — same data, two sections. Plan says merge or link. Since R1 Phase A1 already merged them into one `renderBacktestEvidence`, this may be about the Scorecard case-list score column vs the Backtest Evidence card. The "two views" is now: (1) case-list row "68.76/100 FAIL" and (2) evidence card "Gate 2 Score: 68.76/100, Gate 2 Status: FAIL". A cross-link or just removing the score from the case-list would fix this. |
| R2-25 | **CONFIRM** | HIGH | Screenshot 1 confirms: MCC Acceptance Status banner (with "Q1 Fam Momentum…" promotable row showing TRXUSDT·4h) is visible above the STG084 detail page. `index.html` L51: `#mccStatusPanel` is a sibling of `#strategyDetail` (L53). The acceptance panel renders globally and is visible on detail view. **Plan's fix (hide on detail) is correct and simple:** CSS `#strategyDetail:not([hidden]) ~ #mccStatusPanel { display:none }` or JS toggle. |
| R2-26 | **CONFIRM** | LOW | The acceptance list is div-based rows. Sortable table is a UX improvement, low priority given only 1 promotable strategy exists. |
| R2-27 | **CONFIRM** | MED | L2552: `${summary.total} scored` where `summary.total = cards.length`. Screenshot 1 shows "360 SCORED" — this counts scorecard cards (multiple runs per strategy), not distinct strategies. Plan's R2-D6 decision ("N strategies · M backtest runs") is the correct fix. **Needs backend support:** `buildAcceptanceSummary` must deduplicate by `base_strategy_id`. |

---

## 2. Cross-Cutting Questions

### A. Carry-over diagnosis accuracy

**The "happy-path fixed, edge-case left" diagnosis is accurate** — confirmed for all 5 carry-overs. However, there are **2 additional Round-1 fixes that are similarly leaky and NOT in §0:**

1. **UI-28 (Parity step):** Added in Phase B1 but reads from `row.pinets_parity_proof` which is almost always empty (most strategies have no parity proof). The step shows "Pending — not run" universally. This is **correct behavior** (not a leak), but it's worth noting that the parity step will be permanently pending for the vast majority of strategies until parity tests run.

2. **UI-30 (Trading Rules gap banner):** Phase B3 added the systemic gap banner, but the `majorGap` threshold (≥50%) means a strategy with exactly 6/14 fields undefined (43%) shows NO banner despite having a significant gap. The threshold may be too conservative. Not a leak per se, but an edge case.

3. **R1 Phase A2 `inferMarketCondition` fix:** The "continuation before pullback" fix was correct, but `inferMarketCondition` still returns `"Pullback / mean reversion"` for the example strategy (screenshot 4 shows this). The strategy title says "pullback" but the described behavior is trend-continuation entry at the 8 EMA. **The heuristic itself is unreliable** — R2-22 correctly identifies this.

### B. Theme grouping

The 7 themes are correctly identified. **R2-14 IS the highest-leverage single fix** — confirmed. One `statusText(status) · passLabel` line change at L891 eliminates "OK · Pass", "FAIL · Fail", and "INCOMPLETE · Pending" across ALL gate rows (4 gates × N strategies). No other single fix has comparable blast radius.

**However:** R2-12 (`6/?`) is arguably **equal leverage** — it affects every sub-score row across Gate 1, Gate 1B, and Gate 3 (screenshot shows 12+ instances of `/?" on one gate alone). Both should be in R2-0.

### C. Missed findings

**Yes — 3 findings not covered by R2-01..27:**

1. **MISS-R2-A: "Tested timeframe: Not tested yet" in Taxonomy while Scorecard shows 7 TRXUSDT 1D runs.** Screenshot 4 shows "Tested timeframe: Not tested yet" but the strategy HAS been backtested on 1D (visible in case list). `canonical.tested_tf` is empty → taxonomy shows "Not tested yet." This is the same root as R2-23 (canonical not populated for this strategy's backtest data) but manifests separately in taxonomy. **Not covered by any R2 finding explicitly.**

2. **MISS-R2-B: "Market / bias: Not defined yet" + "Instrument / market fit: Market not defined" in Trading Rules + Taxonomy while the strategy was backtested on TRXUSDT.** The strategy has `symbol = null` at the pipeline level but the scorecard cards have `symbol = "TRXUSDT"`. The canonical should propagate this. **Backend gap.**

3. **MISS-R2-C: "Expected market condition" in Taxonomy says "Pullback / mean reversion" while the header description says "continuation pullbacks to the 8 EMA during an uptrend."** The heuristic matches "pullback" from the description text. R2-22 covers taxonomy being heuristic but doesn't call out this specific mis-classification.

### D. False positives

**R2-03 is partially a false positive.** The plan says "QuantLens: Not evaluated" has "no explanatory tooltip" — but Phase B2 already added a detailed tooltip at L470. The badge now reads "QUANTLENS: NOT IN SCOPE (SEPARATE AI PRE-SCREEN)" with a long title attribute explaining independence from gate verdict. The tooltip exists. What remains is wordsmithing, not a missing tooltip.

**R2-05 is borderline.** The 3-state badge (Promotable/Can test/Blocked) at L760-761 already shows the correct state with correct color coding (ok/amber/bad). Showing a "ladder" of all 3 states with the current one highlighted is a UX preference, not a gap. Could be deprioritized.

### E. Fix-masks-bug check (tooltip masking data bugs)

**Three cases where T2 tooltip/wording fixes would mask real backend bugs:**

1. **R2-06 (blocker leak):** Adding a tooltip or rewording "score below 65" masks the real bug: `canonical.blocking` is empty when it shouldn't be, causing fallback to stale legacy data. **Fix the canonical populate first**, THEN the display.

2. **R2-22 (taxonomy heuristic):** Labeling taxonomy as "estimated (inferred from name)" is the RIGHT interim fix per R2-D5. But it masks the real gap: no real taxonomy source exists. **Acceptable as interim** because the heuristic IS an estimate, and the label is honest about it.

3. **R2-23 (journey backtest desync):** Any display-side fix (rewording the Journey step) would mask the real bug: `canonical.backtest_status` is not populated from `gate2.status`. **Must fix backend first.** The plan correctly places this in Phase R2-D (backend).

4. **R2-16 (Gate 3 "Not evaluated"):** Rewording from "Incomplete · Pending" to "Not evaluated (scorer not built)" is HONEST labeling, not masking. The scorer genuinely isn't built. **This is the correct approach.**

### F. Phase order & dependencies

The R2-0→A→B→C→D→E sequence is **mostly correct but has two issues:**

1. **R2-22 taxonomy label is misplaced in Phase R2-D (backend).** Adding "(estimated)" to the taxonomy heading is a pure `app.js` display change. It should be in Phase R2-A (wording). The "bind to real source later" part is indeed backend/future work, but the label change is immediate.

2. **R2-23 and R2-27 genuinely need backend work** (canonical populate, distinct-strategy counting). These ARE correctly in Phase R2-D. But R2-23 is a BLOCKER and should not wait for all of R2-0/A/B/C to complete first. **Consider promoting R2-23 backend fix to run in parallel** with R2-0/A since it's in different files (readers, not app.js).

3. **R2-25 (hide acceptance on detail)** could be done in R2-0 (it's a 1-line CSS/JS toggle, decision-free). Keeping it in R2-B means the confusing global banner remains visible through two more phases.

**No "display-only" items are secretly backend work** — confirmed. All Phase R2-0/A/B/C changes are pure `app.js`. Only Phase R2-D touches readers.

### G. Read-only safety

**No planned fix introduces a write path.** All changes are display-only:
- R2-D2 (cancelled: no write-back ever) is correctly handled.
- R2-26 (sortable table) is client-side sort, no server write.
- R2-21 (QuantLens Claude verdict) writes verdict data as a separate project, not dashboard writes.
- No Pine/MTC_V2/parity constraint violations detected.

**Confirmed safe.**

### H. Top 5 to fix first (maximum trust gain, limited effort)

1. **R2-14 (keystone)** — Collapse `statusText(status) · passLabel` to single label. 1 line change, kills 3+ complaints, visible on every gate row. [~5 min]

2. **R2-12** — Fix `max_points || "?"` → hide denominator when null, or show `{pts}/–`. Removes all `6/?`, `16/?`, `20/?` etc. across every gate. [~5 min]

3. **R2-08a** — Remove hardcoded `"Repaint status unknown"` from riskFlags. 1 line deletion. Removes false alarm chip from every strategy. [~2 min]

4. **R2-23 (backend)** — Populate `canonical.backtest_status` from `gate2.status` in `build_canonical_display_row`. Fixes Journey desync BLOCKER. [~30 min, different file, can run in parallel]

5. **R2-25** — Hide acceptance panel on detail page. 1 CSS rule or JS toggle. Removes the confusing global banner from strategy detail view. [~5 min]

**Honorable mention:** R2-11/R2-19 (field dictionary) is HIGH impact but HIGH effort — needs a full label map for ~30 raw metric names. Do it in Phase R2-A, not R2-0.

---

## 3. Line Number Verification Summary

| Plan ref | Plan line | Actual line | Status |
|----------|-----------|-------------|--------|
| R2-01 title | :464 | L464 | ✅ correct |
| R2-01 description | :466 | L466 | ✅ correct |
| R2-02 map | :594 | L594 | ✅ correct |
| R2-02 tooltip | :610 | L610 | ✅ correct |
| R2-03 badge | :470 | L470 | ✅ correct |
| R2-04 verdict | :702-721 | L702-721 | ✅ correct |
| R2-05 badge | :761 | L761 | ✅ correct |
| R2-06 fallback | :690 | L688-691 | ✅ ~correct (off by 2) |
| R2-07 fact | :774 | L774 | ✅ correct |
| R2-07 chip | :724 | L724 | ✅ correct |
| R2-08a repaint | :726 | L726 | ✅ correct |
| R2-08b wording | :738 | L738 | ✅ correct |
| R2-09 case list | :808 | L808 | ✅ correct |
| R2-10 gates | :814 | L814 | ✅ correct |
| R2-11 raw names | :879/945 | L879/L945 | ✅ correct |
| R2-12 max_points | :881 | L881 | ✅ correct |
| R2-14 status·pass | :891/867 | L891/L866-868 | ✅ correct |
| R2-15 PASS-only | :877 | L877 | ✅ correct |
| R2-16 Gate3 | implied | L867 | ✅ |
| R2-17 missing | :897 | L897 | ✅ correct |
| R2-18 action | :2616 | ~L2549-2558 | ❌ **off by ~60 lines** |
| R2-19 Gate3 fields | implied | L897/L940-948 | ✅ |
| R2-20 badge | :470 | L470 | ✅ correct |
| R2-20 section | :476 | L476 | ✅ correct |
| R2-22 taxonomy | :951/984/993/1003 | L951 only confirmed | ⚠️ 984/993/1003 are shifted |
| R2-22 complexity | :963 | L963 | ✅ correct |
| R2-23 journey | :1015 | L1015-1016 | ✅ correct |
| R2-25 panel | :156, html:51 | L2544, html:51 | ⚠️ :156 is wrong; render is at ~L2544 |
| R2-26 rows | :2578 | ~L2580 | ⚠️ off by ~2 |
| R2-27 counter | :2552 | L2552 | ✅ correct |

**Overall: 23/28 exact or ±2 lines, 3 off by >10 lines, 2 approximate.** Good accuracy for a post-Phase-A/B shifted file.

---

## 4. Final Assessment

**The plan is sound.** The 27 findings are real (only R2-03 is partially already-addressed, and R2-05 is borderline). The theme grouping is correct. The phase sequencing is mostly right with the caveats noted (R2-22 taxonomy label → move to R2-A; R2-23 backend → run in parallel; R2-25 → promote to R2-0).

**Critical path:** R2-14 (keystone) → R2-12 → R2-08a → R2-11/R2-19 (dictionary) → R2-23 (backend, parallel).

**The single biggest risk** is R2-23: the Journey backtest desync is a BLOCKER that erodes trust in the entire dashboard. It's the only finding where a user sees directly contradictory information ("PENDING" vs "FAIL") on the same page. Fix the backend canonical populate first, or at minimum add a `gate2.status` fallback in the Journey renderer as a temporary shim.
