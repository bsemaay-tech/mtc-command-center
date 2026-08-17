# KICKOFF — C13 arm bounded repair round 3 (three audit findings)

You are Claude Opus 5, acting as IMPLEMENTER for this bounded round (GLM, the original
implementer, is quota-blocked; you did not author or audit this arm — the C13 auditor is
Codex, who will re-audit your repair). Working directory: C:\LAB\Tradingview_LAB_CLEAN.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`)

1. `RP6_C13_CODEX_AUDIT_2026-08-10.md` — the three findings; it is the repair contract.
2. `RP6-P0.sh` — repair target (current `cfdb23b8…`, 54109 B).
3. `SELF_QA_RP6.md` — QA to extend per finding 2.
4. `STATUS_RP6_P0.md` — status to update.

## Scope — exactly the three findings

- **F1 (HIGH):** in `p0_resolve_passwd`, rc 2 may become `nomatch` ONLY when the
  complete merged capture is empty (the interface's valid no-match shape). rc 2 with
  any diagnostic/partial bytes → `error`, and the caller emits
  `identity_unresolvable` rc 3. Preserve all other arms byte-identical.
- **F2 (MEDIUM):** make the C13 QA D026-grade: add real RED runs against mutations that
  (a) remove/bypass the production arm integration call (the harness must go RED, not
  stay green), (b) remove each new `:?` backstop itself, and (c) drive the F1 fix
  (rc-2-plus-diagnostic fixture → error/rc 3 GREEN on repaired bytes, and show the
  pre-repair bytes classify it nomatch — RED). Real captured output only; run locally
  in Git Bash; no host contact, no network.
- **F3 (MEDIUM):** narrow the header claim at lines ~31-35 to the truth: names are
  queried via getent and recorded diagnostically, admission is numeric only, NSS
  source identity is not established.

Preserve: read-only scope, rc 0/1/3 contract, all pre-existing arms untouched.
`bash -n` PASS; record new SHA-256 + byte count in QA and status.

## Deliverables

Repaired `RP6-P0.sh`, extended `SELF_QA_RP6.md`, updated `STATUS_RP6_P0.md`, plus your
report `RP6_C13_REPAIR_R3_REPORT.md` (finding → disposition → evidence). Touch ONLY
those four files. Do not commit — the Lead verifies, routes the Codex re-audit, commits.
