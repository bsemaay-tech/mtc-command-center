# ROUND-2 PLAN AUDIT - Codex

> Auditor: Codex GPT-5 - Date: 2026-06-07 - Plan under audit: `ROUND2_PLAN.md`
> Scope: plan stress-test against current `app.js`, API readers, screenshots, and a live `build_dashboard_snapshot()` sample. No trading/Pine/MTC/parity logic reviewed or changed.

## 1. Per-finding verdicts

Format: `ID | VERDICT | SEVERITY | NOTES`

### Carry-overs (§0)
| ID | VERDICT | SEVERITY | NOTES |
|----|---------|----------|-------|
| R2-02 (UI-7) | CONFIRM | LOW | Current detail status source can pass `"Low Score Review"` from `mtc_v2_readiness.status_label`, so `friendlyStatus()` does not map `LOW_SCORE_REVIEW` and `statusBadgeTooltip()` misses because it only checks `"needs review"`. Fix should normalize status keys before display/tooltip, not only add another display string. |
| R2-06 (UI-10) | CONFIRM-BUT | HIGH | The stale `"score below 65"` text still exists in `mtc_v2_reader.py`, but the plan's app.js fallback diagnosis is incomplete: current detail blocker uses canonical blocking first, then `auditRow.blocked_reason`, not `mtcV2Row.blocker`. Correct fix is to remove/suppress the stale MTC_V2 blocker source everywhere and keep detail blockers sourced from `gate_summary/canonical` only. |
| R2-15 (UI-16) | CONFIRM | MED | `renderGateRow()` still renders sub-score detail only when `status === "PASS"` or `pass === true`; FAIL/INCOMPLETE gates hide the breakdown. This is visible in the Gate2 FAIL and Gate3 INCOMPLETE screenshot. |
| R2-23/24 (UI-26) | CONFIRM-BUT | HIGH | R2-23 is already fixed in current API/UI for the sampled row: canonical `backtest_status` is `FAIL` and `renderReviewJourney()` reads canonical. R2-24 remains partially real because Scorecard and Backtest Evidence are still separate sections, even though Backtest Evidence now explicitly says it is unified from scorecard_v2/canonical. |
| R2-08a (UI-32) | CONFIRM | MED | `buildWaveADecision()` still appends hardcoded `"Repaint status unknown"` to risk flags even though Trading Rules now reads repaint/lookahead notes. Remove the chip unless a real source field says unknown. |

### Round-2 findings
| ID | VERDICT | SEVERITY | NOTES |
|----|---------|----------|-------|
| R2-01 | CONFIRM-BUT | LOW | The code has no guard against title and description being equal, but the live screenshot example no longer duplicates them. Fix should conditionally hide `detail-description` only when normalized title equals normalized description. |
| R2-03 | CONFIRM-BUT | LOW | Current code has a QuantLens badge title and section explanation, so "no tooltip" is stale. The real issue is D1 naming: Gemini-origin pre-screen data is still displayed as QuantLens. |
| R2-04 | CONFIRM | LOW | The decision ladder is compressed to one primary verdict and one reason; no alternate ladder is shown. This is UX polish, not a data blocker. |
| R2-05 | CONFIRM | LOW | The `Can test` badge is still a single state, not a visible ladder. Keep this behind data/SST fixes. |
| R2-07 | CONFIRM | MED | Blocking is shown as a Verdict fact, Scorecard blocking chips, and a separate Gate Blockers panel. Pick one primary placement and keep detail/tooltips there. |
| R2-08b | CONFIRM | LOW | `"Documented and internally tested"` is still current wording. The planned copy change is safe display-only work. |
| R2-09 | CONFIRM-BUT | LOW | The case list is still under Scorecard, but current labels already include tested timeframe/run and an active marker. Treat as layout polish, not a correctness bug. |
| R2-10 | CONFIRM | LOW | Gates still render after the case list (`renderScorecardCaseList()` before `gates.map(...)`). If the owner wants gates first, phase order is straightforward. |
| R2-11 | CONFIRM | MED | Sub-score rows and missing fields still expose raw names such as `intake.entry_pseudo_present` and `alert_adapter.*`. Needs a label dictionary for both rendered tables and missing-field lists. |
| R2-12 | CONFIRM | LOW | `s.max_points || "?"` still emits `6/?` when `max_points` is null/missing. Prefer criterion max from schema/rubric if available; otherwise show points only without a fake denominator. |
| R2-13 | CONFIRM | LOW | Gate-level reason exists, but short per-criterion "why deducted" is not present. Correctly keep deep AI-authored reasons in backlog. |
| R2-14 (keystone) | CONFIRM | HIGH | `statusText(status) + passLabel` still emits doubled labels such as `OK - Pass`, `FAIL - Fail`, and `INCOMPLETE - Pending`. This is the highest-leverage single app.js fix because it reduces repeated confusion across all gates. |
| R2-16 | CONFIRM | MED | Gate3 still displays generic `INCOMPLETE - Pending` even though the system gap is scorer/evidence not complete. Copy should say "Not evaluated / production-readiness evidence missing" without pretending the dashboard can score it. |
| R2-17 | CONFIRM | LOW | "Missing / not scored" has no explanatory tooltip/source reason. This is display-only unless the backend cannot distinguish missing metric vs intentionally N/A. |
| R2-18 | CONFIRM | LOW | Gate Blockers still says generic "Action required". The better fix is gate-specific text derived from the same helper used by blocking chip tooltips. |
| R2-19 | CONFIRM | MED | Gate3 missing fields are raw `alert_adapter.*` / `state_sync.*` with bare `N/A`. Use a field dictionary plus reason classes; do not hide the fact that data is absent. |
| R2-20 | CONFIRM | MED | QuantLens appears as a top badge and a full section. Keep one section after Scorecard/Backtest context and rename Gemini-origin data per D1. |
| R2-21 | CONFIRM | MED | The conceptual rule is right: future Claude QuantLens should be opinion-only and must not create a second score. Existing Gemini pre-screen may retain its own commercial/complexity metadata if renamed away from "QuantLens". |
| R2-22 | CONFIRM-BUT | HIGH | Taxonomy is still heuristic (`inferTimeHorizon`, `inferMarketCondition`, `inferMethod`) and unlabeled as estimated. A tooltip alone would mask a source-of-truth gap; label as estimated now and plan a backend/source binding later. |
| R2-24 | CONFIRM-BUT | MED | Backtest Evidence now reads from scorecard_v2/canonical and shows Gate2 score/status, so the data contradiction is mostly fixed. Remaining problem is UX duplication: two sections still feel like two backtests unless visually linked or merged. |
| R2-25 | CONFIRM | MED | `renderAcceptancePanel()` runs globally and `syncUnifiedDetailVisibility()` does not hide `#mccStatusPanel` when detail is open. The current "Global summary - all strategies" label helps but does not fully solve detail-page adjacency. |
| R2-26 | CONFIRM | LOW | The promotable list is still loose div rows, not a sortable table. This is display-only and safe. |
| R2-27 | CONFIRM | HIGH | Live snapshot: `scorecards.cards=360`, `scorecards.by_strategy=38`, `promotable_cards=1`. "1 Promotable / 360 scored" is materially misleading because 360 is runs/cards, not strategies. |

## 2. Cross-cutting

**A. Carry-over diagnosis** (happy-path-fixed/edge-left accurate? other leaky Round-1 fixes not in §0?):
Mostly accurate, but the current code has already fixed several Round-1 leaks after the screenshots: `scoreForGate()` now shows FAIL scores, `isPromotable()` normalizes `1/true`, `build_canonical_display_row()` exists, canonical backtest status feeds Journey, and QuantLens now scans both salvage and strategies. Other still-leaky items not emphasized enough: global Acceptance panel remains adjacent to detail, Gate Blockers duplicates Scorecard blockers, and `mtc_v2_reader.py` still emits stale "score below 65" text.

**B. Theme grouping** (7 themes right? is R2-14 truly highest-leverage?):
The seven themes are directionally right, but T6 should explicitly split "backend SST" from "old data source still exists but detail no longer reads it". R2-14 is the highest-leverage single app.js polish fix; R2-27/R2-22 are more fundamental for trust because they affect what the numbers mean.

**C. Missed findings** (in screenshots/code, not covered by R2-01..27):
Baseline drift itself is missed: the plan describes some defects that are already fixed in current code, so execution phases need revalidation before dispatch. Also, QuantLens/Gemini naming is cross-cutting across Verdict, QuantLens Verdict, Salvageable Ideas, and source labels, not only R2-03/R2-20/R2-21.

**D. False positives** (R2 finding that is correct behavior -> drop):
R2-23 should be dropped as an active current-code bug; canonical sample data reports Gate2 FAIL and the current Journey renderer reads canonical. Keep a regression check, not an implementation task.

**E. Fix-masks-bug** (tooltip/relabel hiding a real data-model bug -> fix backend instead):
R2-06, R2-22, R2-23, and R2-27 must not be solved with copy only. R2-06 needs stale MTC_V2 blocker suppression/removal; R2-22 needs either an estimated label or a real source; R2-23 is canonical/API contract; R2-27 needs distinct strategy/run counts from the API or a local derived count.

**F. Phase order & dependencies** (R2-0->A->B->C->D->E correct? any "display-only" item secretly backend?):
Do not execute the plan exactly as written without rebasing it on current code. Recommended order now: (1) trust blockers R2-27/R2-06/R2-22, (2) R2-14/R2-15/R2-11/R2-12 gate readability, (3) R2-25/R2-26 acceptance panel scope/table, (4) QuantLens rename/placement, (5) low-risk copy/tooltips. Backend/API work is hidden inside R2-06, R2-22, R2-23 regression protection, and R2-27.

**G. Read-only safety** (any fix risks a write path / Pine/MTC_V2/parity violation?):
No planned dashboard fix needs Pine, MTC_V2 strategy behavior, or parity edits. The only risk is R2-D2/R2-21 style "decision" UI drifting into write-back; keep all decisions as display-only notes and do not add dropdowns/forms that persist state.

**H. Top 5 to fix first**:
1. R2-27: relabel/count as `N strategies - M backtest runs`.
2. R2-14: collapse `status - passLabel` into one clear status.
3. R2-22: mark taxonomy as estimated now; plan real source binding later.
4. R2-06/R2-02: remove stale `score below 65` source and normalize low-score status tooltip.
5. R2-15/R2-11/R2-12: make FAIL/INCOMPLETE gate details readable with human labels and sane denominators.

## 3. Line-number corrections (any `app.js:LINE` in the plan that is wrong)

- Most `app.js` line refs are close enough on current file: R2-01 464/466, R2-08a 726, R2-10 808/814, R2-11 879/945, R2-12 881, R2-14 891/867, R2-18 2616, R2-22 951/984/993/1003, R2-25 156 + `index.html:51`, R2-27 2552.
- R2-06 line refs 688-691 are only part of the issue. Current detail fallback is `auditRow.blocked_reason`; the stale `"score below 65"` source confirmed in live data is `mtc_v2_reader.py` and `mtc_v2_readiness.rows[*].blocker`.
- R2-23 line 1015 now reads `canonical.backtest_status`; live sample canonical says `FAIL`. Treat the plan's desync claim as stale for current code.
- R2-03 wording is stale: current code has a top badge title and a full explanatory section, but still uses the wrong QuantLens/Gemini concept label.

## 4. Verification notes

- Live snapshot check: `scorecards.cards=360`, `scorecards.by_strategy=38`, `promotable_cards=1`; sampled `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK` canonical has `defined_tf=10m`, `tested_tf=1D`, `backtest_status=FAIL`, `gate2_score=68.76`, `blocking=['gate2','gate3']`.
- MTC_V2 readiness check: at least one row still has `status='LOW_SCORE_REVIEW'`, `status_label='Low Score Review'`, and `blocker='score below 65'`.
- QuantLens reader check: current `build_quantlens()` scans both `03_QUANTLENS/03_SALVAGE_IDEAS` and `03_QUANTLENS/strategies`, so the older "salvage-only scan" diagnosis is no longer current.
- Cheap-agent dispatch was attempted through `_deepseek_driver/ds_agent.py`, but it failed with a Windows stdout `OSError: [Errno 22] Invalid argument` before producing `C:/tmp/ds_mcc_r2_plan_audit_mechanical_report.md`; this report therefore relies on direct Codex verification.
