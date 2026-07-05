# System Test / Fake Money Lab — Dashboard Page Design (2026-07-05)

Author: Claude Opus 4.8. Approved by Barış 2026-07-05 ("onaylıyorum tasarım dokümanı +
implementasyon. yap master merge de yap"). Follows audit `MCC_APP_AUDIT_2026-07-05.md` §7 item 10.

## Purpose

Give the fake-money / systems-plumbing benchmark work (STG002 vertical slice V1.x) a home in the
dashboard. Today its evidence — 888 emitted signals, 888 reconciled, 0 unexplained — lives only in
git-ignored `03_QUANTLENS/system_test/<run>/` files + NEXT_STEPS markdown. A cold session opening
MCC cannot see it exists.

## Hard constraints (non-negotiable)

- **READ-ONLY. DISPLAY ONLY.** No run button, no emitter trigger, no broker/exchange/testnet/paper
  link, no execution UI of any kind. The page reads existing on-disk artifacts and renders them.
  (Barış's standing rule: any dashboard *execution* UI needs separate approval — this crosses no
  such line because it executes nothing.)
- **VISUAL FIREWALL.** A permanent page-level banner and a distinct accent make it impossible to
  confuse system-test plumbing with paper trading, testnet, or live trading. The banner text is the
  literal contract string already stamped in every artifact:
  `SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY`.
- **NO KPI FABRICATION.** If no run dir exists, the page shows an honest empty state. It never
  invents fills, round trips, or a status.
- **NO NEW EXECUTION PATH, NO SCHEMA EDIT, NO PROTECTED SCOPE.** Frontend + one read-only reader
  module + read_model wiring + tests only. No Pine/MTC_V2/parity/02_MTC_BACKTEST/07_ADAPTERS/
  06_SCHEMAS change.

## Placement decision

New top-level nav page **"System Test Lab"**, NOT a section inside Strategy Intelligence (that page
is strategy *evidence*; this is plumbing evidence) and NOT inside LiveOps (nothing is live). The
existing **"Paper Trading"** nav item is renamed **"Promotion Readiness"** so the word "paper" stops
denoting two different concepts. (The renamed page keeps its current gate-readiness content
unchanged; only its label + subtitle change.)

## Data source

Reader scans `03_QUANTLENS/system_test/*/` (git-ignored runtime output; safe to read). Per run dir:

| File | Role in page |
|---|---|
| `emitter_manifest.json` | benchmark identity: candidate_id, engine_strategy_id, symbol/tf, expected_payload_count, approval status, banner, robustness_note, promotable(false) |
| `reconciliation_summary.json` | the numbers: status, expected/received/filled/rejected/duplicates/unexplained counts, expected_not_received / received_not_expected / received_not_filled lists |
| `reconciliation_report.md` | human-readable reconciliation narrative (linked, not inlined beyond first lines) |
| `*.jsonl` (expected/received/fills) | NOT parsed (large; counts already in summary). Listed as artifact links with sizes only. |

Run status states derived from `reconciliation_summary.json.status` + the mismatch lists:
`OK` (0 unexplained, all lists empty), `MISMATCH` (any non-empty diff list or unexplained>0),
`INCOMPLETE` (manifest present but no reconciliation), `INVALID` (unparseable).

## States tracked (from audit question 5 list)

- Selected benchmark: candidate_id + engine_strategy_id + symbol/tf (from manifest).
- Replay approval: strategy_approval_status = NOT_APPROVED + benchmark_role = SYSTEM_TEST_ONLY.
- Local replay output: expected_payload_count vs received/filled.
- Accepted / rejected events: received_count, rejected_count, duplicates_dropped.
- Simulated fills: filled_count.
- Round trips: derived = filled_count / 2 when entry+exit paired (888 → 444), shown as "≈".
- Unexplained events: unexplained_count + the three mismatch lists.
- Promotion blockers: promotable=false + robustness_note (robust_final=0 library-wide) +
  strategy_approval_status.
- Next approved action: static, sourced from the vertical-slice gate model — "Slice V1.1 CLOSED;
  legs V2-V4 gated (not opened); Gate V5 day-30 review 2026-08-01." Rendered as reference text,
  NOT derived from a live writer (there is none).
- Gate legs V2 (TV alerts) / V3 (Wunder demo) / V4 (testnet): shown as CLOSED/NOT_OPENED chips so
  the boundary between done plumbing and un-opened outward legs is explicit.

## Layout

1. **Firewall banner** (full width, distinct color, lock icon): the contract string, always visible.
2. **Benchmark card**: candidate, engine strategy, symbol/tf, approval status, promotable=NO.
3. **Reconciliation metrics grid**: expected / received / filled / rejected / duplicates /
   unexplained / ≈round-trips, with the status pill (OK green / MISMATCH red).
4. **Promotion blockers panel**: robustness_note, approval status, why nothing promotes.
5. **Vertical-slice gate ladder**: V1.1 CLOSED, V2-V4 NOT_OPENED (gated), V5 review date.
6. **Artifacts list**: run dir files with sizes + link to reconciliation_report.md.
7. Empty state when no run dir: "No system-test replay runs found. This lab displays fake-money
   plumbing benchmark evidence only." + the firewall banner still shown.

## Non-goals / anti-confusion guarantees

- The page never shows P&L, returns, or anything resembling trading performance — only plumbing
  counts (did every emitted signal arrive and reconcile).
- The word "fill" is always "simulated fill". The word "trade" is avoided; "round trip" is a
  plumbing pairing, marked ≈.
- Distinct amber/orange "SYSTEM TEST" accent, different from the teal/blue used for real strategy
  evidence and the red used for live-danger.

## Contract for future writers

When a new system-test replay runs, it already writes `emitter_manifest.json` +
`reconciliation_summary.json` into `03_QUANTLENS/system_test/<run>/`. No extra step is needed for
the dashboard to see it — the reader auto-discovers all run dirs. This is the run-manifest pattern
the audit recommends, already satisfied for this vertical.
