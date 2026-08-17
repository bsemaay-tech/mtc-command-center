# KICKOFF — Codex T1 execution re-audit of pathscope round 3

Tier T1 execution audit. Codex `-Account fourth` (`gpt-5.6-sol`), effort **high** (T1).
Read-only except your single verdict file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CODEX_T1_EXEC_AUDIT_R3_2026-08-13.md`.
No git mutation. No sub-delegation. You must be the auditor because both implementers are
excluded: r2 was `claude-opus-5`, r3 was GLM-5.2.

**Content-filter protection (this lane was filter-blocked on this source once before):** work
in narrow bands, never paste large source or fixture bodies, redirect all harness output to
scratch outside the repo and quote only summary lines, use symbolic fixture names.

## Subject

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py` — **124251 B,
SHA-256 `0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7`** (re-derive,
case-insensitive hex compare).

## Inputs, in order

1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`
   — the flagship execution audit that found CRITICAL C-1 (assignment-prefix silent sink).
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_GLM_T1_R3_REPAIR_REPORT_2026-08-13.md`
   — the r3 repair (construct-level `record_assignment_value` at three holes).
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md` — harness +
   executed round-3 evidence (Lead ran the full harness: rc 0; seven P9 fixtures confirmed).

## Contract

1. Re-derive the identity; extract the published harness (fenced block, run from repo root:
   `powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r2_harness.ps1"`)
   and run it verbatim. Compare stdout to the recorded round-3 stdout in the doc.
2. Adjudicate C-1's closure adversarially: try constructs the repair might miss within its
   lexical contract (the bare-soname residual is DISCLOSED — judge the disclosure's honesty,
   not the absence). Any NEW surviving silent sink is CRITICAL per the standing contract.
3. Adjudicate the cheap items (`:325-327` wording, U-3 citation, NIT-1 ENDPOINT label) and the
   disclosed residual.
4. Verdict PASS / PASS-WITH-NITS / REQUEST_CHANGES; if accepting, state the flagship
   EXECUTION acceptance sentence. Path-scoped delta gate governs; whole-status advisory with
   attribution. Session model/effort line at the end.
