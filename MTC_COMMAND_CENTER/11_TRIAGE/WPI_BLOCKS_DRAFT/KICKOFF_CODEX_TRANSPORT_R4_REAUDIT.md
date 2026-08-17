# KICKOFF — Codex T0 re-audit: transport round 4 bytes

Date: 2026-08-11. Dispatched by the Lead (Fable session). You are Codex `gpt-5.6-sol`
xhigh, AUDITOR of record for the transport set, fresh session. Read-only intent: audit in
place, edit nothing, no git mutation, no host contact, no network. T0 surface.

## Bytes under audit

The nine transport files in `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/` at commit
`99f33c33` (current working tree also carries a PARALLEL session editing `RP6-P0.sh` and
`SELF_QA_RP6.md` — those two files are OUT of your scope this round; audit transport bytes
as committed at `99f33c33`, via `git cat-file blob 99f33c33:<path>` if the working tree
looks mid-edit).

## Your prior findings (round-3 final audit, REQUEST_CHANGES)

`TRANSPORT_CODEX_FINAL_AUDIT_2026-08-10.md` — F1 (launch domain + marker family), F2
(TMPDIR into evidence), F3 (mixed probe as absence), F4 (global `$sequenceOk` — your
decisive fixture), plus the skeleton-review transport items T5 (`P0_ATTESTED_*` wiring),
T6 (close contract), T7 (inert pin), T8 (stale summary).

## Round-4 evidence to audit

1. `TRANSPORT_R4_REPORT_2026-08-11.md` — per-item dispositions, including the superseded
   `cf049b6b` edit's kept/dropped table and a second masked defect claim (`declare -F`
   under `set -e`).
2. `SELF_QA_TRANSPORT.md` §R4-0..R4-6 — three harnesses (`_r4_runner_probe.ps1`,
   `_r4_wsl_fixtures.sh`, `_r4_t5_compose.sh`), RED from the round-3 blob at `78173bfd`,
   declared fixture retargeting, and one disclosed F1 residual (`BASH_ENV` startup plant
   forging the record via exit — claimed closed ONLY plan-side by `env -i` with a complete
   variable list).
3. Draft edits: `WPI_PREREGISTRATION_DRAFT.md` + `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`
   (transport-semantics sentence, per-branch prerequisite map, derivation classes 5/6
   flagged as NEW PERMISSIONS pending owner ratification).

## Audit contract

- Execute, don't read: reproduce the decisive fixtures yourself (runner probe both
  variants; WSL fixtures if you have a kernel, else mark which you could not execute —
  non-execution is never acceptance and must be stated per D025 rule 1).
- Verify every RED is a real prior-bytes execution, not narration (D026).
- Judge the F1 residual: is the plan-side `env -i` closure real and enforced by frozen
  bytes, or is the unqualified F1 "closed on the composition" claim an overclaim? A
  disclosure is not a control.
- Judge the census delta 36/33 → 37/38 line by line.
- Hunt NEW defects with the 13 defect patterns (`DESIGN_DEFECT_PATTERNS_2026-08-10.md`).
- Verdict per the standard grammar (PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK).

Write ONE new file: `TRANSPORT_CODEX_R4_AUDIT_2026-08-11.md` in the same directory.
