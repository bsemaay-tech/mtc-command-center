# Codex re-audit kickoff V2 (2026-08-09) — self-contained, narrow read scope

Context: this is an authorized documentation quality audit of test-infrastructure design documents
in a private trading-system repository. Everything is docs-only; no live system, no credentials,
no network targets are involved in your task.

Do NOT read `_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`, or any `GATE_A_A*` file —
their content is not needed. This file carries all required context.

## Context (complete)

- A proposals document containing draft verification-script designs was audited earlier today by
  you (Codex) with verdict REQUEST_CHANGES, nine findings F1–F9:
  `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_AUDIT_2026-08-09.md`.
- A bounded repair specification was frozen at commit `9ac60ac6`:
  `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_REPAIR_SPEC_2026-08-09.md`.
- The counterpart implementer (claude-opus-5 xhigh) completed repair round 1 at frozen commit
  **`7194b895`**, editing exactly one file:
  `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md` (+1473/−729).
- Implementation report: `C:\tmp\CLAUDE_REPAIR_ROUND1_REPORT_2026-08-09.md`. Local RED/GREEN
  falsification evidence root: `C:\Users\BARSEM~1\AppData\Local\Temp\D026.mR6q2g` (transcript
  SHA-256 `1bbb4a469aa1503d0d5aa4775835a97c4e6bccfb3c301fde61b9be3703a742e1`).
- Owner decision (`11_TRIAGE/OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §5): this is the single
  authorized re-audit round; no additional models; process meta-artifacts get no separate audits.

## Your single unit

Fresh read-only re-audit of the repaired proposal at frozen commit `7194b895`, per repair-spec
§9.3–9.4:

1. Verify the diff touched only the one named file.
2. Check each F1–F9 closure against the repaired text and the candidate source anchors named in
   the report (`git show 2ce41e34bceb599d80af24c5c33d835820ec321b:<path>` for exact objects).
3. Reproduce claimed local falsifications where feasible from the preserved harness sources
   (listed in report §3); do not manufacture runs for paths the report declares BLOCKED
   (C1, C2 baseline dependencies, C5, R4-5).
4. Verify honest open items are declared, not silently closed: R4-5 (Windows symlink privilege),
   C1-GAP-A/B, C2 baseline dependency, platform mode-bit stubs (report §5.5).
5. Verdict: **ACCEPT** or **REQUEST_CHANGES** with reproduced required findings only.
6. Write your audit record to a new file
   `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_PROPOSALS_REAUDIT_ROUND1_2026-08-09.md`, commit it on
   branch `feature/donchian-crypto-ladder` (stage exactly that file), and push.

## Boundaries

Docs and local analysis only. Do not contact any host or remote system other than `git push` to
origin. Do not run or transfer any proposed script against any host. Do not edit the proposal
itself or any product/deploy/tool/test file. Do not touch `C:\PGRK`.
