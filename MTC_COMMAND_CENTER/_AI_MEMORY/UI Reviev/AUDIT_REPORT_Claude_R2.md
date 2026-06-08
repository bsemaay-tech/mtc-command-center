# ROUND-2 PLAN AUDIT — Claude

> Auditor: Claude (Opus 4.8) · Date: 2026-06-07 · Plan under audit: `ROUND2_PLAN.md`
> Every `app.js:LINE` and reader claim verified against live `apps/web/app.js` + `apps/api/mcc_readonly/{scorecard_reader,read_model}.py`. Line corrections in §3.

## 1. Per-finding verdicts

### Carry-overs (§0)
| ID | VERDICT | SEVERITY | NOTES |
|----|---------|----------|-------|
| R2-02 (UI-7) | CONFIRM | MED | Confirmed: badge passes raw `statusLabel` ("Low Score Review") to `statusBadgeTooltip` (app.js:469), which only matches `"needs review"` (610). `friendlyStatus` map (594) is never applied to the label, so tooltip returns "". Fix (add "low score" branch OR run label through friendlyStatus first) is right. |
| R2-06 (UI-10) | CONFIRM | HIGH | Confirmed leak at app.js:690: when `canBlocking` empty, falls back to `auditRow.blocked_reason` → stale "score below 65" shows. Fix correct, but **also scrub the SECOND path at app.js:1294** (`mtcV2Row.blocker || auditRow.blocked_reason`) — not in §0 or R2-06's ref. |
| R2-15 (UI-16) | CONFIRM | MED | Confirmed app.js:877: `subScoreDetail` gated on `status==="PASS" \|\| pass===true`. FAIL/INCOMPLETE render no breakdown. Fix right; pair with R2-12 (max_points null) or breakdown shows "6/?". |
| R2-23/24 (UI-26) | CONFIRM-BUT | BLOCKER | Frontend render at app.js:1015-1019 is ALREADY correct (reads `can.backtest_status`, maps FAIL→"executed (not passed)"). Backend `_canonical_backtest_status` (scorecard_reader.py:253) already returns gate2_status. So "populate backtest_status" mischaracterizes it — the real desync is either the gate2 status being UNKNOWN in the source JSON (`_gate2_status` finds neither `gate2.status` nor `gate_summary.statuses.gate2`) or the canonical not reaching the *detail* row. Verify on the real `*.scorecard.json` before coding. |
| R2-08a (UI-32) | CONFIRM | MED | Confirmed app.js:726: `"Repaint status unknown"` is an unconditional literal in `riskFlags`. Better than blind-remove: drive from canonical/metadata repaint flag, omit when unknown — deleting loses a real signal where data exists. |

### Round-2 findings
| ID | VERDICT | SEVERITY | NOTES |
|----|---------|----------|-------|
| R2-01 | CONFIRM | MED | app.js:464 (`title`) + 466 (`displayDescription`) can resolve to the same string — `strategyDisplayName` candidates include `description.family`/`producerSpec.title`, which often == the description. Dedupe correct; suppress description when equal (case/space-normalized) to title. |
| R2-03 | CONFIRM | LOW | Copy. Tooltip on "QuantLens: Not evaluated/Not in scope" (label now "Not in scope (separate AI pre-screen)" at app.js:741). Fold into R2-D1 rename so the string isn't tooltipped twice. |
| R2-04 | CONFIRM-BUT | LOW | Real: 6-branch verdict computed (app.js:702-721) but only the chosen one shown. BUT this is an enhancement, not a bug; "show the whole ladder" risks clutter. Lighter fix: keep one primary + a tooltip listing where it sits. Don't elevate above the SST bugs. |
| R2-05 | CONFIRM-BUT | LOW | Same as R2-04 — surfacing the 3-state badge ladder is cosmetic polish. Tooltip, not a stacked widget. |
| R2-07 | CONFIRM | MED | Confirmed dup: blocker in `riskFlags` chip (app.js:724) AND "Blocking item" fact (renderVerdictDecision). Keep the fact, drop the chip. |
| R2-08b | CONFIRM | LOW | app.js:738 wording. Pure copy. |
| R2-09 | CONFIRM | MED | 7-run case list sits under Scorecard but is backtest data. Relabel/relocate is right; ties to R2-24 (same backtest, two views). |
| R2-10 | CONFIRM | LOW | Layout: gates should precede run-list under the heading. Cosmetic ordering. |
| R2-11 | CONFIRM | MED | Confirmed raw keys (`intake.entry_pseudo_present`, gate2 `source_metric`) render verbatim (app.js:879,947). Label dictionary right — this is the single biggest legibility win in T2. |
| R2-12 | CONFIRM-BUT | MED | Confirmed app.js:881 `${s.max_points \|\| "?"}` → "6/?". A null-guard hides it, but `max_points` missing is a **data gap** — the scorer didn't emit the denominator. Prefer fixing the scorecard producer to emit max_points; UI guard is a stopgap, label it as such. |
| R2-13 | CONFIRM | LOW | Display + backlog split is sensible. |
| R2-14 (keystone) | CONFIRM | HIGH | Confirmed app.js:891 `${statusText(status)} · ${passLabel}` with passLabel (866-868) → "PASS · Pass", "FAIL · Fail", "INCOMPLETE · Pending". Doubled. Collapse to one label. Correctly the cheapest high-visibility win — but it is cosmetic, not the most *fundamental* (see B). |
| R2-16 | CONFIRM | MED | Gate3 INCOMPLETE·Pending → "Not evaluated (scorer not built)". Honest framing of a system-wide gap. Good. |
| R2-17 | CONFIRM | LOW | Tooltip on "Missing / not scored" (app.js:897). Copy. |
| R2-18 | CONFIRM | MED | Confirmed app.js:2616 "Action required" + blocker list (2620) gives gate name + "Blocking", no action. Gate-specific action text right. |
| R2-19 | CONFIRM | MED | Gate3 `alert_adapter.*`/`state_sync.*` raw + bare N/A. Same dictionary as R2-11; merge into one label map, don't build two. |
| R2-20 | CONFIRM | MED | Confirmed two placements: top badge app.js:470 + `${quantlensVerdict}` section at 476. Keep one. Sequence with R2-D1 rename to avoid double work. |
| R2-21 | CONFIRM | HIGH | Correct as a SEPARATE project. Single scoring authority = Scorecard; QuantLens = opinion only. Right call; do not let it block Round-2 display fixes. |
| R2-22 | CONFIRM-BUT | HIGH | Confirmed heuristic taxonomy + hardcoded `["Complexity","Not defined yet"]` (app.js:963). "Label as estimated now" (R2-D5) is acceptable ONLY if the label is honest — but a keyword-guessed "Scalping/Pullback" that contradicts the tested 1D timeframe is **wrong data**, not just unlabeled. Estimated-tag must sit next to the real tested TF/symbol so the user sees the conflict; otherwise the tag masks a contradiction. |
| R2-24 | CONFIRM | HIGH | Score-view (Scorecard) and metric-view (Backtest Evidence) are the same backtest. `renderBacktestEvidence` already tags "source: scorecard_v2 + canonical" (app.js:1170) — link/merge so the score visibly derives from those metrics. |
| R2-25 | CONFIRM | MED | Acceptance banner (`#mccStatusPanel`) is global and renders regardless of detail view → reads as strategy-specific. Hide on detail (R2-D4). Correct. |
| R2-26 | CONFIRM | LOW | Loose `<div>` rows (app.js:2578); sortable table per R2-D4. UX. |
| R2-27 | CONFIRM-BUT | HIGH | Confirmed app.js:2552/2575: `total = cards.length` (runs), not strategies. The tooltip added at 2553 ("Scored = has a Gate2 scorecard") is **itself wrong** — it counts runs. R2-D6 "N strategies · M runs" needs a real distinct-by-`base_strategy_id` count, not a relabel of the same number. |

## 2. Cross-cutting

**A. Carry-over diagnosis.** Accurate — every §0 item is the same "happy-path shipped, edge untreated" pattern (PASS rendered, FAIL/INCOMPLETE/empty-canonical/legacy-fallback skipped). But it is **not the only leaky pattern**, and the plan should not assume §0 is exhaustive:
- **Second stale-blocker path** at app.js:1294 (`mtcV2Row.blocker || auditRow.blocked_reason`) — same leak as R2-06 but a different call site, uncaught.
- **`humanizeStrategyId` vs raw id** inconsistency: acceptance rows now humanize (app.js:2586) but case-list/other spots still print raw — a partial UI-5-adjacent fix.
- **`max_points` null (R2-12)** is itself evidence the scorecard *producer* is leaky, not just the UI.
The deeper meta-pattern: Round 1 fixed *render sites* one by one rather than normalizing the data at the canonical layer, so every new render site re-introduces the same fallbacks. That is the actual recurring defect.

**B. Theme grouping.** 7 themes are reasonable. But **R2-14 is the highest-*visibility* fix, not the highest-*leverage*.** It's a cosmetic dedup of a label. The highest-leverage fix is **R2-23/R2-06 (canonical as the enforced single source)** — i.e. T6. If canonical were authoritative and every render site read only canonical (no `auditRow.blocked_reason`/`mtcV2Row.blocker`/keyword-taxonomy fallbacks), R2-06, R2-22, R2-23, R2-27 collapse into one backend change. T6 should be flagged the keystone theme; R2-14 is just the cheapest quick win.

**C. Missed findings.**
1. **app.js:1294 second stale-blocker leak** (above).
2. **`_gate2_status` UNKNOWN-collapse**: if the source JSON has neither `gate2.status` nor `gate_summary.statuses.gate2`, canonical backtest_status = UNKNOWN → journey "pending" even when a score exists. This is the likely real cause of R2-23 and is not called out.
3. **Acceptance "scored" tooltip is wrong** (app.js:2553) — counted as a fix in R2-27 but it actively misinforms now.
4. **Taxonomy contradicts tested TF on the same page** — R2-22 treats it as "no SST"; it's also a visible contradiction (10m-inferred "Scalping" vs tested 1D) that the estimated-tag alone won't resolve.

**D. False positives.** None are pure false positives, but **R2-04 and R2-05 (verdict/badge ladders) are over-scoped** — they're nice-to-have UX, not problems. Drop them to backlog; they compete for the single-file serial app.js owner against real bugs.

**E. Fix-masks-bug check (the important one).**
- **R2-22 (taxonomy)** — MASKS A BUG. "Label as estimated" leaves wrong inferred categories on screen next to the real tested TF. The estimate tag is cosmetic cover over a data-model gap (no producer_spec strategy_type). Acceptable as interim ONLY if shown adjacent to the real tested TF/symbol so the contradiction is visible.
- **R2-06 (blocker)** — would be masked if "fixed" by scrubbing the visible string only. Must remove the *fallback source* (and the 1294 twin), not the text.
- **R2-23 (journey)** — do NOT "fix" in the frontend; render is already correct. Tooltiping or re-labeling the journey would hide a backend canonical/gate2-source bug.
- **R2-27 (count)** — the added tooltip currently masks a wrong number. Fix the count, then label.
- **R2-12 (6/?)** — UI null-guard masks a missing `max_points` from the producer. Fine as stopgap if tagged.
T2 items R2-03/08b/11/16/17/19 are genuine copy/legibility with no data bug behind them — safe.

**F. Phase order & dependencies.** Mostly sound, two corrections:
1. **R2-23 is wrongly only in Phase R2-D as "populate".** Its diagnosis must happen FIRST (it may be a join/source bug, not a populate task) — front-load a 10-min check on the real scorecard.json before any phase commits.
2. **R2-D (SST backend) should precede R2-A/B/C where they overlap**, consistent with the plan's own stated principle but violated by ordering cosmetics (Phase 0/A) ahead of it. Specifically R2-27's relabel (Phase D) and its tooltip (Phase A) must land together or the Phase-A tooltip ships a known-wrong string.
3. **Secretly-backend items mislabeled "display":** R2-22 (needs producer_spec binding), R2-27 (needs distinct count), R2-12 (needs producer max_points), R2-23 (canonical). These are reader work, not app.js — correctly parallel-track them, but R2-12 is filed in Phase 0 as a UI guard; flag that the real fix is backend.

**G. Read-only safety.** No planned fix introduces a write path — R2-D2 (display-only note, no dropdown, N2-B cancelled) is the right guard and is respected. Watch one thing: R2-26 "sortable table" must sort client-side over already-loaded snapshot data; do not add a server sort param that could mutate query state. No Pine/MTC_V2/parity edits in scope. Safe.

**H. Top 5 to fix first (max trust per credit).**
1. **R2-14** — collapse `status · passLabel`. Trivial, page-wide, kills the most-noticed double-label.
2. **R2-06 + the app.js:1294 twin** — kill stale "score below 65" at BOTH sites; derive blocker only from `canonical.blocking`.
3. **R2-23** — diagnose then fix the journey/scorecard backtest desync at the canonical/gate2-source layer (BLOCKER: DONE-vs-FAIL misleads decisions).
4. **R2-11 + R2-19** — one gate-field label dictionary; biggest legibility gain for one artifact.
5. **R2-27** — correct the count to distinct strategies AND fix its tooltip together (it currently misinforms).

## 3. Line-number corrections
- **R2-01** plan says title/description at `464/466` → correct (464 title, 466 description). ✓
- **R2-02** map `594` ✓, tooltip `610` ✓ — but the miss is at the **call site app.js:469** (raw label passed), which the plan doesn't cite.
- **R2-06** plan `688-691` / `690` → correct (690). ✓ Missing twin at **1294**.
- **R2-07** chip `724` ✓; "Blocking item" fact is in `renderVerdictDecision` (~770s), plan's `774` is approximately right.
- **R2-14** plan `891/867` → `891` ✓ (`statusText·passLabel`); passLabel is **866-868**, not 867.
- **R2-15** `877` ✓.
- **R2-08a** `726` ✓.
- **R2-12** `881` ✓.
- **R2-22** `963` (hardcoded Complexity) ✓; heuristics around 951-1003 ✓.
- **R2-23** `1015` ✓ — but render is correct; backend `scorecard_reader.py:253` (`_canonical_backtest_status`) + `236` (`_gate2_status`) are the real targets, not cited.
- **R2-27** `2552` ✓; `total` set at **2575**.
- **R2-18** `2616` ✓.
- **R2-20** `470` (badge) ✓; section is rendered via `${quantlensVerdict}` at **476**, defined elsewhere — plan's "476" is the placement, not the renderer.
- **Note:** `scoreForGate` (906) no longer requires `status==="OK"` — Round 1's blocker is genuinely fixed; no R2 finding wrongly re-flags it. Good.
