# LEAD_VERIFICATION - WP-P0-26 OPS-A NIT slice (`505af399` = `e114ed31` + NIT-1/2/4/5) - 2026-09-18 (owner: build the slices before Sol; `OD-20260918-P026-N2-DOC-1` = doc)

**Base:** `e114ed31` - exact-Opus PASS-WITH-NITS (0 REQUIRED; `OPUS_QUEUE_20260916/P026/LEAD_ADJUDICATION_P026_T0.md`), Gemini delta PASS. **Role:** Lead = disclosed builder. **Scope:** five files (blobs: `restore.py` `7a5d39e2`, `backup.py` `074904cc`, `test_opsa.py` `79720612`, `README.md` `9980c77b`, `RESTORE_DRILL_EVIDENCE.md` `528f9a43`); +46/-6. **NIT-3** (the P0-30 adapter checker's ASCII-only anchor) is fixed on the P0-30 branch (`d426e79f`, F8) and deliberately NOT touched here - the same lines on two branches would collide at merge; the second PR to land rebases.

## What changed
- **NIT-1** `restore.verify_completion_evidence`: after every existing check (pair integrity via `load_complete_marker`, exactly one successful global `run_end`, per-run manifest well-formed and equal to the global file records, declared counts, per-record readbacks) it now checks the marker's OWN claims - `readback == "all_match"` and `run_manifest == RUN_MANIFEST_NAME` - and refuses `run_not_complete` naming the value. Placed LAST so the existing refusal reasons keep precedence (a first placement right after the loader made five existing tests report the new reason instead of the `run_end` one - moved). `RUN_MANIFEST_NAME` imported from `opsa_common`. The forged-evidence helper in `test_partial_run_declaring_files_but_having_no_records_fails_closed` now carries the two fields so the "nothing to verify" fence BEHIND the gate is still exercised (that test's purpose).
- **NIT-2 (doc)** README step 4: the marker is O_EXCL, not atomic; a torn/unreadable marker = not complete, re-backed-up under a NEW run id (each backup run has its own id - no automatic retry is implied), data left in place (no delete primitive), never restored from.
- **NIT-4** `RESTORE_DRILL_EVIDENCE.md`: dated note at the top of Part A (contract changed; `--latest` removed; the recorded commands exit 2; the 2026-08-24 run has no `COMPLETE.json`; how to reproduce with the current tool; transcript kept as the pre-change record).
- **NIT-5** `backup.py`: `return RC_OK if not errors else RC_ERROR` (status derives from errors alone; the `run_end` record still carries `status`).

## Evidence (`P026_NIT_SLICE_20260918/`; mutants on a scratch copy of `tools/opsa`, ASCII TEMP `C:/bt_s4/p026_tmp`)
| Arm | Result | File |
|---|---|---|
| NIT-1a - the readback claim unchecked (`if False and ...`) | **1 failed** (`test_tampered_marker_or_run_manifest_is_refused`, the new readback arm) | `LEAD_RED_P026_NIT1a_readback_claim_unchecked.txt` |
| NIT-1b - the run_manifest claim unchecked | **1 failed** (the new run_manifest arm) | `LEAD_RED_P026_NIT1b_run_manifest_claim_unchecked.txt` |
| Baseline scratch | 39 OK | `LEAD_RED_P026_BASELINE.txt` |
| GREEN `test_opsa.py` in the worktree | **Ran 39 tests OK** | `LEAD_GREEN_test_opsa.txt` |
| Ruff (worktree config) | per file identical to HEAD: restore 2, backup 4, test_opsa 7 | (queue log) |
| Guard | `RESULT: PASS`; staged exactly the five files | `LEAD_GUARD_P026_NIT.txt` |
| Gemini delta `P026_NIT_GEMINI` (packet `P026_NIT_20260918`, 17 files) | see `GEMINI/` and the queue log | `GEMINI/` |
NIT-5 has no behavioural fence (a pure simplification; the suite's rc assertions cover the return).

## Roster
Lane 4 re-pinned to `505af399` (launcher, agent brief, REVIEW_BRIEF HEAD + addendum, queue row); attempt 1 archived. Exact-Opus re-read on the next free Pro lane (after lane 3's P0-30 slice read); Sol Saturday on the same bytes; the Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`); machine stamps in `OPUS_QUEUE_20260916/QUEUE_LOG.txt`.
