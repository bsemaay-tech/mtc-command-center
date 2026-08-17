# KICKOFF — Preregistration assembly, lane B: §10.1 reconciliation + attestation ordering

Date: 2026-08-11. Dispatched by the Lead (Fable session). You are Codex `gpt-5.6-sol`
acting as AUTHOR of a standalone application document (T2 surface). Work entirely inside
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/`.

## Task

Turn two open freeze-blockers into concrete, mergeable preregistration text. A parallel
lane is editing the successor draft, so you must NOT edit any existing file — produce a
standalone document the Lead merges afterwards.

1. **§10.1 reconciliation** — from `SEC101_RECONCILIATION_CODEX_2026-08-10.md`: draft the
   final §10.1 text applying all 11 EXTEND items including the access-qualifier grammar.
   For the 3 unresolved families: draft a decided proposal per family with a one-paragraph
   rationale and the falsification that would show the choice wrong; mark each
   `PROPOSED — LEAD/OWNER DECISION REQUIRED`.
2. **Attestation ordering** — the circular attestation/preregistration/commit order:
   specify the two-commit fix as exact procedure text (what is committed in commit 1,
   what values only then become computable, what is committed in commit 2, and the check
   that detects violation of the order). State the invariant that breaks the circle.

Context (read-only): `WPI_SUCCESSOR_PREREG_SKELETON_2026-08-10.md`,
`WPI_PREREGISTRATION_DRAFT.md`, `SEC102_COMPOSITE_DESIGN_CODEX_2026-08-10.md`,
`../DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

## Output contract

- Write ONE new file: `SEC101_ATTESTATION_APPLICATION_2026-08-11.md` in this directory.
- Disposition table: each of the 11 EXTEND items + 3 families + ordering fix → section
  anchor in your document. Every member gets a disposition (defect pattern 13).
- End with SELF-QA: for each item, the one line that satisfies it; for the ordering fix,
  walk the two-commit sequence once and show no value is needed before it exists.
- No git operations. No execution. Do not edit existing files.
