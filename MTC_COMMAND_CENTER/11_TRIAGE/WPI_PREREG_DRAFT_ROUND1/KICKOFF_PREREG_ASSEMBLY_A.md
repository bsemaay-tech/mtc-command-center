# KICKOFF — Preregistration assembly, lane A: skeleton gaps + RUNID minting changes

Date: 2026-08-11. Dispatched by the Lead (Fable session). You are Codex `gpt-5.6-sol`
acting as AUTHOR of preregistration text (T2 surface — prereg text, no executable blocks).
Work entirely inside `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/`.

## Task

Produce the round-2 successor preregistration draft by applying two accepted review
work-lists to the existing skeleton:

1. `SKELETON_REVIEW_CODEX_2026-08-10.md` — all 13 NEEDS-WORK items.
2. `RUNID_MINTING_REVIEW_CODEX_2026-08-11.md` — all 6 NEEDS-WORK items.

Base document: `WPI_SUCCESSOR_PREREG_SKELETON_2026-08-10.md`.
Context (read-only, do not edit): `WPI_PREREGISTRATION_DRAFT.md`,
`SEC102_COMPOSITE_DESIGN_CODEX_2026-08-10.md`, `ROWS_1_9_OPTIONS_CODEX_2026-08-10.md`,
`../DESIGN_DEFECT_PATTERNS_2026-08-10.md` (13 patterns — numbering frozen).

## Output contract

- Write ONE new file: `WPI_SUCCESSOR_PREREG_DRAFT_R2_2026-08-11.md` in this directory.
- Do NOT edit the skeleton, the reviews, or any other existing file.
- For each of the 19 items (13 + 6), the draft must contain a disposition table row:
  item id → APPLIED (with section anchor) or DEFERRED (with reason). Every member needs
  a disposition — silent omission is defect pattern 13.
- Do NOT resolve the three unresolved §10.1 families or the attestation ordering here —
  lane B owns those; leave explicit `LANE-B` placeholders where they land.
- Do NOT design §8.2 rows 1–9 content — owner decision binds them into RP7-WPI-RO.sh
  after RP7 dual acceptance, not into this draft beyond the existing references.
- End the file with a SELF-QA section: for each review item, quote the one line of your
  draft that satisfies it. No git operations. No execution of any block.
