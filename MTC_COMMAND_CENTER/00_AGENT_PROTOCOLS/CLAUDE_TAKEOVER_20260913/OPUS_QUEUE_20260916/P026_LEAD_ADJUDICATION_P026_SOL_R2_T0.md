# LEAD_ADJUDICATION - exact-Sol T0 read of WP-P0-26 `2e03a669`, attempt 2 with the amended brief (Codex PRO `free`, gpt-5.6-sol xhigh; Sat 2026-09-19 15:26-15:50 UTC+3; adjudicated 15:5x at the owner's shutdown)

**Verdict as written:** **REQUEST_CHANGES** - one REQUIRED, two NITs. 184 lines, 24 min, exit 0, no `turn.failed`; worktree clean after the lane. The reviewer computed HEAD and subject hashes, ran the three mandated GREEN suites (39 / 45 / adapter), Ruff (the brief's selection, via the standalone exe - the Ruff BLOCK of attempt 1 is gone), reproduced the original `--latest` defect and the D026 RED states, and added independent fail-open arms. The Lead records agree with the reviewer's counts.

## REQUIRED-1 - CONFIRMED by reading the `2e03a669` blob of `MTC_COMMAND_CENTER/tools/opsa/restore.py`
- `:50-68` `select_run` picks BOTH `file` and `dir` records of the explicit run from the GLOBAL manifest.
- `:97-103` the completion gate compares per-run vs global records **only where `record == "file"`** (`_key` = store_id, rel, sha256, size).
- `:245-251` restore recreates every selected `dir` record straight from the global manifest after the gate passed.
So a global-manifest `dir` record can be changed (the reviewer forged `dir.rel` after a successful backup, leaving the digest-bound per-run manifest untouched) and restore returns rc 0, creates the forged directory, skips the genuine one, and reports `status: ok`. Integrity gap in the matching-evidence contract (path confinement still holds). Repair (reviewer's wording, Lead agrees): compare every operational record restore consumes - `file` AND `dir`, type-appropriate canonical fields - between the digest-bound per-run manifest and the global manifest before any restore action; D026 test that forges only a global `dir` record and requires rc 3 with nothing restored. Not reproduced by the Lead (owner shutdown); the package session reproduces it first.
- **NIT-1** `backup.py:15-19` / `opsa_common.py:41-43` prose promises no completion artifact remains after an interruption; the two-write implementation can leave `RUN_MANIFEST.jsonl` without `COMPLETE.json` (the reviewer's crash-window arm) - restore still refuses; wording fix.
- **NIT-2** `RESTORE_DRILL_EVIDENCE.md:152` still shows `--latest`; this IS the follow-up slice that `P26-EVID B` named - fix the line and re-apply the dated note with the row.

## Standing
P0-26 `2e03a669`: exact-Opus PASS-WITH-NITS (on `505af399`, code identical) + Gemini PASS, **exact-Sol REQUEST_CHANGES** → NOT merge-ready. **T0 repair round 1** (no round used yet on this candidate) → **P0-26 package session (Sonnet 5)**, prompt `SESSION_PROMPT_P026_PACKAGE_20260919.md` (REQUIRED-1 + NIT-1/2 + the Opus slice-read NITs 1/2/3/5 + the evidence note), then Gemini delta + exact-Opus + exact-Sol on the final bytes; the Lead merges. The Lead never accepts its own code.

Recorded by Claude Fable 5.1 Lead (session 7, `18c1b8`).
