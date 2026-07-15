# Impeccable UI Pilot R3 — critique re-score

Date: 2026-07-13
Target: MCC Strategy Detail (`renderIntelligence`)
Pilot strategy: `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`
Original critique: `.impeccable/critique/2026-06-21T15-56-19Z__r-08-dashboard-app-apps-web-app-js-strategy-detail.md`

## Verdict

**32/40 — Good.** Up from 30/40. This is a real improvement, not an “impeccable” claim.
All five queued critique fixes are present, but the remaining power-user and loading-state gaps
prevent a higher score.

## Heuristic re-score

| # | Heuristic | Before | After | Rationale |
|---|---|---:|---:|---|
| 1 | Visibility of System Status | 3 | 3 | Gate/blocker state is strong; async detail loading still has no skeleton. |
| 2 | Match System / Real World | 4 | 4 | Expert domain language and gate ordering remain exact. |
| 3 | User Control and Freedom | 3 | 3 | Focus and native workflow buttons are fixed; the dossier remains intentionally read-only. |
| 4 | Consistency and Standards | 3 | 4 | One canonical gate verdict remains; side-stripe and duplicate gate-card vocabulary are gone. |
| 5 | Error Prevention | 3 | 3 | Read-only constraints and blockers remain clear. |
| 6 | Recognition Rather Than Recall | 4 | 4 | Sticky Decision Summary remains visible and canonical. |
| 7 | Flexibility and Efficiency | 2 | 2 | No command palette or keyboard shortcuts for expert navigation. |
| 8 | Aesthetic and Minimalist Design | 2 | 3 | Repeated full-credit notes and two duplicate verdict surfaces were removed; taxonomy remains dense. |
| 9 | Error Recovery | 3 | 3 | Missing states remain honest and readable. |
| 10 | Help and Documentation | 3 | 3 | Inline gate descriptions remain; no new separate help layer. |
| **Total** | | **30** | **32** | **P0: 0; original P1 issues: 0 remaining.** |

## Five-fix evidence

1. **A11y contrast — PASS.** Empty/missing values use readable `--muted #94a3b8`; the original
   P1 contrast blocker is closed.
2. **A11y focus — PASS.** Global `:focus-visible`, native workflow `<button>` controls, and
   reduced-motion fallback are present. Focused static contract: `2 passed`.
3. **Side-stripe bars — PASS.** Commit `0172d940` removed the one-sided status stripe in favor of
   full-border tint. The obsolete gate-card CSS is now fully removed.
4. **Boilerplate dedup — PASS.** Implementation `6da2735c`; screenshot evidence `adeb889b`.
   Full-credit rows rely on their green score chips; partial/zero-credit explanations remain.
   Evidence: `screenshots/fix4_dedup_BEFORE.png`, `screenshots/fix4_dedup_AFTER.png`.
5. **Triple gate-state — PASS.** Implementation `e819ac02`; cleanup/evidence `93114a61`.
   The hero KPI strip and Gate Status Summary are gone; the persistent right rail is canonical.
   Evidence: `screenshots/fix5_verdict_BEFORE.png`, `screenshots/fix5_verdict_AFTER.png`.

## Verification

- Live page: `http://127.0.0.1:8765/dashboard`, read-only API healthy.
- DOM: `heroGatePanels=0`, `gateSummaryGrids=0`, `decisionSummaries=1`.
- `node --check MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js` — PASS.
- `python -m pytest MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_strategy_detail_a11y_static.py -q` — `2 passed`.
- From `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api`: `python -m unittest discover -s tests -p 'test_*.py' -q` — `Ran 120 tests`, `OK`.
- Visual review: fix 4 exposes only exception notes; fix 5 removes the two non-canonical verdict surfaces without hiding blockers or workflow state.

## Remaining, intentionally not inflated away

- No skeleton while scorecard detail loads.
- No command palette or keyboard shortcuts for the expert operator.
- The eight-field taxonomy remains dense.
- The dossier is long; the sticky rail mitigates this but does not eliminate scroll cost.

No backend, reader, data contract, QuantLens, engine, Pine, parity, schema, or execution behavior changed.
