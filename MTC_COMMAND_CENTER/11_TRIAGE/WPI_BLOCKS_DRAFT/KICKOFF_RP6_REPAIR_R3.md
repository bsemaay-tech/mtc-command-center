# KICKOFF — RP6-P0 round 3 (FINAL T0 round): three re-audit residuals

You are Claude Opus 5 xhigh, implementer. The round-2 re-audit
(`RP6_CLAUDE_REAUDIT_R2_2026-08-10.md`) confirmed all 7 findings CLOSED, verdict
REQUEST_CHANGES on 3 MEDIUM residuals. This is round 3 of the T0 cap — last round.
Apply the auditor's exact minimal fixes. Working dir: C:\LAB\Tradingview_LAB_CLEAN.
No host/network. No commit.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`)

`RP6_CLAUDE_REAUDIT_R2_2026-08-10.md` (findings 1–3 + 2 nits = the contract), `RP6-P0.sh`
(current `041c9da9…`), `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_FULLBLOCK_REPAIR_REPORT.md`.
Draft `../WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — edit only if fixing
finding 1 requires the §8.1 row-1 `rc=<n>` grammar change described.

## The three, exact fixes

- **F1 (MEDIUM)** — `:531-532`: emit
  `tool_not_evaluable tool=$t path=$resolved rc=na detail=access_builtin_x_denied mechanism=access_builtin_x`
  — restore the resolved path, stop asserting `rc=126` (no invocation happened). If
  §8.1 row 1 forces a numeric `rc=`, amend that row instead (P0 never invokes an
  inventory tool, so no arm can carry an honest invocation status) and record why.
- **F2 (MEDIUM)** — D026 evidence reproducibility: pin the full-block fence's RED side
  to the immutable `90d8d447^` blob (or literal `bff3c86e…`), and the row-3 comparison
  to a fixed prereg revision (the doc already uses `$pre_rev`/`$r3_rev` idiom at
  :697/:1196 — copy it). Then RE-EXECUTE and replace all four stale transcripts (full-
  block fence + C13 R3 arm + R3 backstop + C13 R4 arm) with real current output. This
  is mandatory — the repair's own closure evidence must reproduce for the next auditor.
- **F3 (LOW/MED)** — row 8: either add the `stat -L -c '%d'` procfs discrimination
  (compare `/proc/self/ns/user` device vs `/`; nsfs ≠ rootfs) — preferred, no new tool
  — or add `procfs_identity=not_established` to the `P0_execution_domain` line and the
  residual to `does_not_establish`.
- **Nit 1** — correct the `(os error 2)` attribution in `RP6_FULLBLOCK_REPAIR_REPORT.md:29`
  and `STATUS_RP6_P0.md:24` (it is a uutils/basename rendering, not "GNU's observed"
  form; the absolute-prefix + os-error-2 combination is unreachable). Fix attribution,
  keep the harmless dead alternative or drop it — your call, state which.
- **Nit 2** — one header sentence naming the GNU-producer assumption (uutils host makes
  the F1 class return fail-closed at rc 3).

## Deliverables

Repaired `RP6-P0.sh` + `SELF_QA_RP6.md` with all four transcripts regenerated real +
`STATUS_RP6_P0.md` + `RP6_FULLBLOCK_REPAIR_REPORT.md` + `RP6_REPAIR_R3_REPORT.md`
(finding → disposition → evidence) + any draft edit. `bash -n` PASS; new SHA-256 +
bytes; re-run the C13 harnesses green on new bytes. Touch ONLY those five (+draft).
Do not commit.
