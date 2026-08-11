# KICKOFF — Preregistration merge round 3: fold lane-B application into draft R2

Date: 2026-08-11. Dispatched by the Lead (Fable session). You are Codex `gpt-5.6-sol`,
AUTHOR of merged preregistration text (T2 surface). Work entirely inside
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/`.

## Task

Merge the two accepted lane outputs into one coherent successor draft:

1. Base: `WPI_SUCCESSOR_PREREG_DRAFT_R2_2026-08-11.md` (commit `784693e4`) — contains two
   explicit `LANE-B` placeholders (§4.5 access grammar / section-10.1, and the two-commit
   attestation ordering).
2. Insert: `SEC101_ATTESTATION_APPLICATION_2026-08-11.md` (commit `c0dea12d`) — the full
   §10.1 replacement text (11 EXTEND applied), the three family proposals, and the
   two-commit ordering procedure with its order-violation check.

## Rules

- Replace each `LANE-B` placeholder with the corresponding lane-B text, adjusting only
  cross-references and numbering — no substantive rewording of either side.
- The three family decisions stay marked `PROPOSED — LEAD/OWNER DECISION REQUIRED`.
  You decide nothing.
- Do NOT edit any existing file. Write ONE new file:
  `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`.
- Conservation: every disposition row of R2 (19) and every lane-B member (15) must appear
  in R3's combined disposition table with its terminal state; nothing silently dropped
  (defect pattern 13). Flag any contradiction between R2 text and lane-B text as an
  explicit `MERGE-CONFLICT` item rather than resolving it yourself.
- End with SELF-QA: both placeholders resolved (quote the seam lines), conservation count
  19 + 15, list of MERGE-CONFLICT items (may be empty). No git, no execution.
