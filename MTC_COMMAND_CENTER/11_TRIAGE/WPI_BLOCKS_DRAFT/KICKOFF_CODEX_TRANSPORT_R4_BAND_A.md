# KICKOFF — Codex T0 transport round-4 audit, BAND A (structural, no exploit reproduction)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing, no git mutation, no host, no network. T0 surface.

## Why this is split

A prior full-audit run reproduced every fixture correctly but the provider content filter
terminated it before it could write its verdict — the fixture that trips the filter is the
F1 startup-plant falsification. This band audits everything EXCEPT that reproduction, so it
completes and persists. Band B judges the F1 residual from the report text only, without
re-running any plant.

## Scope of BAND A — F2, F3, F4, T5, T6, T7, T8, census, prereg edits

Bytes at commit `99f33c33` (use `git cat-file blob 99f33c33:<path>` — the working tree may
be mid-edit by a parallel RP6 session; `RP6-P0.sh`/`SELF_QA_RP6.md` are OUT of scope).

Evidence to audit:
1. `TRANSPORT_R4_REPORT_2026-08-11.md` — dispositions for F2/F3/F4/T5–T8 and the superseded
   `cf049b6b` kept/dropped table (incl. the `declare -F` under `set -e` second-defect claim).
2. `SELF_QA_TRANSPORT.md` §R4-0..R4-6 EXCEPT the F1 startup-plant blocks — the runner probe
   (F4 decisive fixture: round-3 `deviant=0` STOP vs round-4 `deviant=1` FAIL; the Claude
   scenario; the two distinct cleanup reasons), the F2 `TMPDIR`-into-evidence fixture, the
   F3 mixed-probe fixture, and the T5 `_r4_t5_compose.sh` composition (`P0_ATTESTED_*` 0→5,
   real gate `preregistered_value_missing` → `P0_GATE_PASSED`).
3. Draft edits in `WPI_PREREGISTRATION_DRAFT.md` + `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`
   (per-branch prerequisite map 07<-04…12<-08+10; provenance-marker family binding).

## Contract

- Reproduce the F4 runner probe both variants and the T5 composition yourself; state which
  you executed. Non-execution is not acceptance (D025 rule 1). Verify each RED is real
  prior-bytes execution (D026).
- Census delta 36/33 → 37/38: verify line by line.
- Hunt new defects with the 13 patterns (`DESIGN_DEFECT_PATTERNS_2026-08-10.md`).
- Do NOT reproduce, quote, or construct any `BASH_ENV`/`PATH`-plant startup fixture — that
  is Band B's descriptive scope. If you need to reference F1 at all, reference it by name.
- Verdict grammar: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK, scoped to Band A items.

Write ONE new file: `TRANSPORT_CODEX_R4_AUDIT_BAND_A_2026-08-11.md`.
