# KICKOFF — Claude flagship T0 audit slot: RP6-P0.sh full block (read-only, xhigh)

You are `claude-opus-5` at xhigh in a fresh session — the Claude flagship slot of the T0
contract (`AUDIT_TIER_CLASSIFICATION_2026-08-10.md`). Audit the ENTIRE block, not only
the recent rounds. Note: rounds R3/R4 of the C13 arm were implemented by a claude-opus-5
session — audit them extra adversarially; the Codex xhigh slot is the cross-model check,
but your slot must not rubber-stamp same-family work. Report only — modify nothing.
No host contact, no network; local Git Bash fixture execution expected.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP6-P0.sh` — current bytes (claimed SHA-256
   `bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf`, 57441 B).
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md` — full QA history (F4 arms, C13 arm harnesses 1–2
   at 27 + 4 cases, supplemental fences).
3. `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md` — round history.
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.6 spec, §8.1 P0
   rows + cross-cutting rules.
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — attack with all ten patterns.
6. Audit trail for context: `RP6_P0_GLM_AUDIT_2026-08-10.md`,
   `LEAD_ADJUDICATION_RP6_2026-08-10.md`, `RP6_P0_GLM_REAUDIT_2026-08-10.md`,
   `RP6_C13_CODEX_AUDIT_2026-08-10.md`, `RP6_C13_REAUDIT_CODEX_2026-08-10.md`,
   `RP6_C13_REPAIR_R3_REPORT.md`.

## Contract

- Verify every P0 row (§8.1 rows 1–9) is implemented at its exact FAIL/STOP grammar;
  STOP-vs-FAIL truthfulness on every branch; numeric-identity rule; capability ledger;
  getent arm incl. the R4 sentinel capture (re-run its RED/GREEN yourself — including
  the newline-only rc-2 fixture); `:?` backstops; tool inventory (12 tools);
  namespace/manager arms; evidence-leaf binding; read-only scope.
- Re-derive hash + bytes; `bash -n`; re-run at least harness 1 (27 cases) and
  harness 2 (4 cases) verbatim.
- Hunt for anything the five prior audit rounds missed — you are not bound by their
  finding lists.

Output: print the full report as your final output. Verdict line first — `PASS` /
`PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>` — then per-row/V-item evidence,
then findings most severe first with executed falsifications where possible.
