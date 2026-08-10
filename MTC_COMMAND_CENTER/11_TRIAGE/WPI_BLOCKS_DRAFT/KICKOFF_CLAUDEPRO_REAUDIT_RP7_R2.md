# KICKOFF — Re-audit of RP7-WPI-RO round-2 repair (auditor 2, read-only)

You are Claude Opus 5, the auditor who produced the round-1 BLOCK
(`RP7_CLAUDEPRO_AUDIT_2026-08-10.md`, 13 findings). Codex repaired all 13 and applied
the five Lead adjudications (draft round 1.6). Verify closure adversarially. Report
only — modify nothing. Never contact any host or network; local Git Bash execution of
fixtures is expected.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — repaired bytes (claimed SHA-256
   `ed9aa6b3c1caab1360bdde499ebc893eb431084a15b643a019fb98c4d8837cfa`, 54001 B;
   round-1 baseline `81a29241…`, 44198 B at `f503af55^`).
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md` — executed QA (WSL2 D026 run claimed).
3. `WPI_BLOCKS_DRAFT/RP7_REPAIR_R2_REPORT.md` — finding → disposition map.
4. `WPI_BLOCKS_DRAFT/RP7_CLAUDEPRO_AUDIT_2026-08-10.md` — your 13 findings (closure
   contract).
5. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.6: verify the
   draft edits match the five Lead adjudications recorded in
   `WPI_BLOCKS_DRAFT/KICKOFF_RP7_REPAIR_R2.md` and nothing else changed.

## Verify

- **V1–V13**: one row per original finding — closed / partially closed / not closed,
  each with evidence. RE-RUN your own round-1 falsification fixtures against the
  repaired bytes: each must now land on the repaired outcome. Sample at least
  findings 1, 2, 3, 4, 6 by execution; the rest by code+diff if execution is
  impractical, saying which.
- **V14** Regression: no round-1-passing behaviour broken; V2/V6/V8 of your original
  audit still PASS; adjudication order intact.
- **V15** Draft round 1.6: edits confined to the adjudicated rows/paragraphs; no
  weakening; `<PIN-AT-FREEZE>` mount-projection digest and remaining placeholders
  intact.
- **V16** Hash + bytes re-derived; `bash -n`.

Output: full report printed as your final output. Verdict line first — `PASS`,
`PASS-WITH-NITS`, or `BLOCK: <n> findings` — then the V-rows, then findings most
severe first.
