# KICKOFF — Codex: build §8.2 rows 1–9 into RP7-WPI-RO.sh (owner-decided BUILD ALL NINE)

**DO NOT DISPATCH THIS UNTIL RP7 HOLDS DUAL FLAGSHIP ACCEPTANCE.** The owner's decision is
explicit: all nine rows are bound into `RP7-WPI-RO.sh` **only after the currently reviewed RP7
bytes receive their dual flagship acceptance** (prereg R3 §4.6). Codex holds `RP7_CODEX_T0_AUDIT_R9`
PASS; the second flagship (Claude Pro) audit is scheduled 2026-08-12 23:00. If that audit returns
anything non-accepting, this kickoff waits for the repair and its re-audit.

You are Codex `gpt-5.6-sol` xhigh, IMPLEMENTER. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.
No host, no network, no commit. **`RP7-WPI-RO.sh` is a protected-scope block file** — you are
authorized to edit it ONLY for this owner-decided extension, and for nothing else. Do not touch
`RP6-P0.sh`, the transport set, `composite_pathproof.py`, `pathscope_prover.py`, or the prereg
drafts. Never git checkout/reset/stash any tracked file.

**Auditor note (routing):** because you implement this, the audit goes to a DIFFERENT model —
Claude Pro (`claude-opus-5` xhigh) or GLM — never Codex-on-Codex. Write for that reader.

## The decision and the design (both already settled — implement, do not re-litigate)
- **Owner decision:** BUILD ALL NINE. Not deferred, not narrowed.
- **Design of record:** `WPI_PREREG_DRAFT_ROUND1/ROWS_1_9_OPTIONS_CODEX_2026-08-10.md` §D —
  your own analysis, accepted. Read §D.1–D.5 before writing a line. The shape is settled:
  **extend RP7; do not author a new block or a new transport stage.**

## Required shape (§D.1)
Two new sections placed between the manager preflight and `RP7_SECTION B3_rows_10_15`, in the
preregistered first-divergence order:

1. **`RP7_SECTION B2_rows_1_7`** — ONE bounded `show` capture with explicit per-property
   selection covering rows 1–5, adjudicated record-by-record with **presence proven before
   value**; then rows 6–7 over the fragment path, reusing `wpi_assert_regular_digest` for row 7
   and adding one trusted-`python3` unit-file line-grammar parser for row 6.
2. **`RP7_SECTION B4_rows_8_9`** — ONE bounded `show` capture covering the ten sandbox
   properties plus `Environment`, then the environment tokenizer.

**Two captures, not eleven.** Each adjudicated under the existing precedence rule (timeout, then
rc and complete diagnostics, then stdout), so `wpi_capture` is reused unchanged and the number
of new bounded children stays small.

## Reuse, do not rebuild (§D.1 table)
`wpi_assert_manager_ready` (STOP-first, already runs before any comparison), the existing tool
binding inside the mount window, projection v2's `$WPI_UNIT_FRAGMENT` and
`/proc/$WPI_MAINPID/ns/net`, the `-I -S` isolated trusted-Python adjudicator discipline, the
`EV_DIR` create-once leaves and `wpi_capture`. **`wpi_alloc_leaf` is DELETED as of r9** — the
name-only allocator is gone; use `wpi_open_leaf` and keep the descriptor discipline r9
established (the leaf is bound by descriptor, never re-addressed by name). Do not reintroduce
name-based leaf addressing anywhere in the new sections; that was a BLOCK-level finding.

## Claims and pins that must move with the code (§D.2)
- RP7 terminal claim: `establishes=rows_10_23…` becomes `rows_1_23…`. The `does_not_establish`
  list must keep `identity_of_the_manager_that_answered` **in substance** — every claim sentence
  stays about *the manager that answered in the attested execution domain*, never about "the
  host". Row 24 stays operator-side.
- One new pin class: ten **rendered** expected sandbox values for row 8, plus the expected
  `FragmentPath` and an expected-empty drop-in set for row 5. Rows 6, 7, 9 need no new pin.
- `TRANSPORT_PLAN.tsv` op 05 argv is UNCHANGED; `run_ro.sh` shape unchanged (its
  `stdin_sha256` is already a freeze-time fill). Do NOT renumber operations.
- `RP6-P0.sh` stays unchanged — its out-of-scope line stays true.
- Draft §8.2 is NOT re-authored; the nine rows stand as written. Draft §9's conditional
  DEFER-ROOT-SIDE bullet stays exactly as written (it is the correct fallback if readiness
  fails on the day).

## D026 fixtures you must produce (§D.5 — this is the acceptance floor)
For every one of the nine rows: a RED that fails for the row's own reason and a GREEN on the
repaired/expected state, with the exact command, the exact output, and the mutation identity
recorded. A row whose RED cannot be produced is a row whose check cannot fail — say so plainly
rather than shipping it. Include at minimum: a missing property record (presence-before-value),
a wrong-token value, a fragment-path mismatch, a fragment-digest mismatch, a drop-in that should
be empty and is not, a sandbox property that renders differently from its pin, and an
environment token that must not be present.

## Failure modes to design against (§D.4)
Read §D.4 and design against each. Above all: a `show` record that is ABSENT must never read as
a passing value — presence is proven first, and an absent record is a STOP, not a default.

## Deliverables
Modified `RP7-WPI-RO.sh`; `SELF_QA_RP7.md` extended with the new sections' evidence and the
complete D026 matrix; `STATUS_RP7.md` updated (status becomes rows-1-9-EXTENDED-PENDING-REAUDIT,
new pin class named, terminal claim change recorded); `RP7_ROWS_1_9_REPORT_<date>.md`. Re-derive
`RP7-WPI-RO.sh` size + SHA-256 and state that the identity CHANGED (it must — this is the one
authorized byte change) so the freeze-gate and Audit-2 acceptance matrix can be updated. No
commit — the Lead commits and reproduces the harness verbatim, then routes the audit to a
different model.

## The honest framing for your report
This extension re-opens RP7's acceptance: the changed bytes need fresh dual-flagship acceptance,
and the Audit-2 matrix row for RP7 returns to PENDING on both auditors. Say that plainly. The
prereg's freeze-gate item 1 waits on RP7's acceptance *including* these sections.
