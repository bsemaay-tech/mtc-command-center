# KICKOFF — GLM independent audit of RP7-WPI-RO.sh (read-only)

You are GLM-5.2, the independent auditor for this round. Codex authored the WP-I
RO-stage block and claims all self-QA fixtures passed. Attack it adversarially. Report
only — modify nothing.

Read (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`):

1. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — the block (claimed 44198 B, SHA-256
   `81a292418d78a2fb6ed94435fb05d1e2b70124af0a469f73611b7a259cdc6c3c`).
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md` — its QA.
3. `WPI_BLOCKS_DRAFT/STATUS_RP7.md` — row → function map.
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.5, the BINDING
   spec: section 8.2 rows 10–24 + every binding rule paragraph after the table.
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — attack with all ten patterns.

Verify at minimum:

- **V1** Row coverage: every row 10–23 implemented per its exact FAIL/STOP grammar
  (reason tokens, admissibility preconditions); row 24 correctly left operator-side.
- **V2** Ordering: sweep budget → walk completeness → write bits; interpreter +
  metadata preflight before parity; shared netns preflight before ANY curl/ss
  interpretation; status-before-stdout everywhere.
- **V3** Path-object binding rule implemented (component-wise non-following walk,
  numeric ownership, mount binding, atomic with leaf checks) — not just leaf checks.
- **V4** STOP-vs-FAIL truthfulness on every branch: enumerate the error classes each
  probe can raise and check each maps to the truthful class. Hunt Pattern 1
  violations hard.
- **V5** Structured parsing: ss table, strict JSON, unit properties — no substring
  shortcuts (Pattern 5). Line-reader completion on any multi-line consumer (Pattern 7).
- **V6** Probe execution-environment rule: children launched per the round-1.4/1.5
  contract (Pattern 4); read-only scope (no mutation outside the evidence tree, no
  file content printed).
- **V7** Self-QA: transcripts literally re-runnable; commands match what they claim to
  test; RED cases actually falsify (a QA that cannot fail proves nothing — Pattern 10).
  Re-run at least two RED/GREEN pairs yourself if your environment permits; if
  execution is gated, say so explicitly and verify by code+diff reasoning, never
  assert an execution you did not perform.
- **V8** Byte identity: re-derive the SHA-256 and byte count; compare to claims.

Output: verdict line first — `PASS` or `BLOCK: <n> findings` — then one row per V-item
with PASS/FAIL + one-line evidence, then findings (location, defect, falsification,
minimal fix), most severe first.
