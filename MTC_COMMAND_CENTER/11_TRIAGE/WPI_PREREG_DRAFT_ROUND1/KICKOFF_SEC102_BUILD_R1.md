# KICKOFF — §10.2 composite whole-program proof: build round 1 (scaffold + allocate stage)

Date: 2026-08-11. Dispatched by the Lead (Fable session). You are Codex `gpt-5.6-sol`,
IMPLEMENTER of new tooling. You authored the accepted design
(`SEC102_COMPOSITE_DESIGN_CODEX_2026-08-10.md`); the Claude flagship will audit the
implementation, so separation holds. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host
contact, no network, no commit, no edits to any block file or the preregistration drafts.

## Context

The §10.2 path-scope prover (`pathscope_prover.py`) is UNSOUND pending its own repair
round (9 T1 findings, 4 CRITICAL silent-sink classes — `PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md`).
Its repair is assigned to a NON-Codex implementer and is not your task. Your design note
already established that even a repaired prover cannot close a block alone: the gate needs
one entrypoint-driven whole-program proof per stage, in allocate → render → freeze order.

## Task — round 1 of several

Build the composite proof harness scaffold in
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/`:

1. New tool `composite_pathproof.py` implementing, per your design: entrypoint discovery,
   stage model (allocate/render/freeze), per-stage whole-program traversal skeleton, and
   verdict/report contract. Treat `pathscope_prover.py` strictly as a swappable component
   behind an interface — do NOT depend on its unrepaired internals; define the interface
   your design requires and stub the call.
2. Implement the ALLOCATE stage proof end-to-end first (deepest-risk stage per the design),
   with executable fixtures: at least one GREEN fixture and one RED fixture per claim the
   stage makes. An inability to evaluate must STOP (rc 3), never PASS and never FAIL
   (defect pattern 1). Every input member needs a disposition (pattern 13).
3. `SELF_QA_SEC102_R1.md`: literal commands + rc + output for every fixture, RED shown
   before GREEN (D026 — a test that has not failed proves nothing). If your session cannot
   execute, mark entries `PENDING-LEAD-EXECUTION`; never fabricate transcripts.
4. `STATUS_SEC102.md`: what round 1 covers, what rounds 2+ must add (render, freeze,
   prover-component integration), and every known limitation stated as a limitation — a
   disclosure is not a control, so no claim may exceed what the code enforces.

Read `../DESIGN_DEFECT_PATTERNS_2026-08-10.md` (all 13) before writing code.
New files only; re-derive and record size + SHA-256 for each artifact you create.
