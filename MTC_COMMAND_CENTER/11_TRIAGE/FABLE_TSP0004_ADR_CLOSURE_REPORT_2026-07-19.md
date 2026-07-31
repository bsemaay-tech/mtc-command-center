# TS-P0-004 — ADR-0018/0025 Status Closure — Verification Report

- Date: 2026-07-19
- Author: Claude Fable 5 (builder session, TS-P0 chain)
- Task class: verify-and-record. The owner decision already exists — D016 +
  same-day addendum (2026-07-18) in `_AI_MEMORY/DECISIONS.md`. No decision
  content was invented or altered.

## Decision evidence (D016, verified this session)

`_AI_MEMORY/DECISIONS.md` entry D016 (2026-07-18), read directly this
session, states: ADR-0018–0029 all ratified Accepted by Barış in writing on
2026-07-18 (0026/0028/0029 via the same-day addendum). Qualifications: 0020 and
0024 direction-only/evidence-gated; 0029 framework-only — `LIVE_TRADING_GATE.md`
unsigned, live/mainnet blocked. Explicit sentence: **"TS-P0-004 is DECIDED:
continue the existing Python system, build core risk/order/reconciliation
internally, borrow bounded tools behind owned interfaces."**

## Verification performed (all 2026-07-19, main worktree, read + docs-only fixes)

| Check | Result |
| --- | --- |
| ADR-0018 header | `Status: Accepted` + ratification line citing Barış 2026-07-18 / D016 ✓ |
| ADR-0025 header | `Status: Accepted` + ratification line citing Barış 2026-07-18 / D016 ✓ |
| All twelve ADR-0018..0029 headers | `Status: Accepted` (grep verified) ✓ |
| ADR_INDEX.md table rows 0018–0029 | `Accepted (D016 …)` with correct qualifications ✓ |
| ADR_INDEX.md prose | consistent ✓ except one stale clause (fixed, below) |
| Cross-links 0018↔0025 | present and correct ✓ |

## Inconsistencies found and fixed (docs-only, status-wording only)

1. `ADR-0025` §Context said "The route decision **remains Proposed** pending
   OQ-001." → now states initial Proposed status was ratified Accepted by D016
   (2026-07-18), OQ-001 still tracked as follow-up evidence.
2. `ADR-0018` §Rationale said "The conservative `Proposed` status **reflects**…"
   → now past tense with explicit D016 ratification reference.
3. `ADR_INDEX.md` blockers paragraph said "their **Proposed status** does not
   relax these safety boundaries…" → now "these safety boundaries remain
   enforced by standing project rules regardless of ADR status".

No other content changed. Residual historical wording intentionally left
untouched (e.g. ADR-0018 adoption condition "Resolve OQ-001 … before final
acceptance" — a pre-ratification condition statement; the header ratification
line governs precedence, and rewriting conditions would alter decision
content).

## Observation (not acted on)

D016's main body contains one internally stale sentence ("ADR-0026, ADR-0028,
and ADR-0029 remain Proposed pending separate discussion") that predates the
same-day addendum ratifying them. DECISIONS.md is an owner decision record —
NOT edited by this session. Flagged for Barış if he wants a cleanup note there.

## Closure

TS-P0-004 deliverable = this verification report + the three status-wording
fixes. The ADR record now consistently reflects the ratified D016 state.
Task closed as verify-and-record; no code, runtime, threshold, or execution
change involved.
