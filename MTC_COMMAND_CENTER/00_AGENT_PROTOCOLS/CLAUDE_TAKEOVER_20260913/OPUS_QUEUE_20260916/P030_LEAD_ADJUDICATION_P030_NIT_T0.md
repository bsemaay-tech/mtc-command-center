# LEAD_ADJUDICATION - lane 3 attempt 4: exact-Opus read of the WP-P0-30 NIT slice `d426e79f` (2026-09-18 11:50-12:10 UTC+3; adjudicated Sat 2026-09-19 09:0x UTC+3)

**Verdict as written:** REQUEST_CHANGES - one REQUIRED (F-1), four NITs (F-2..F-5); the earlier N1-N5 otherwise closed. 437 lines, 146 turns, launcher exit 0, no cap. Pinned interpreter used by the reviewer: `C:/tmp/P020_IMPL_20260912/.../.venv/Scripts/python.exe` = **Python 3.12.12**.

## F-1 (REQUIRED) - reproduced by the Lead
Claim: the N4 walk guards (`p030_archive_exporter.py:273-276`; adapter `:119-123` and `:201-205`) are exercised by nothing - both checkers' nesting arms use depth 3000, where on Python 3.12 `json.loads` raises `RecursionError` FIRST, so only the parser clause is tested; deleting any walk guard leaves both checkers green (mutC1 28 OK, mutC3/mutC4 44 OK). The slice's D026 evidence ("walk guard removed -> 1 error"; "the parser-clause mutant SURVIVED, superseded") is therefore INVERTED on the pinned interpreter.
Reproduction (`P030_NIT_SLICE_20260918/ADJUDICATION_R1_20260919/`): `LEAD_REPRO_F1_depth_by_interpreter_py312.txt` - Python 3.12.12, recursionlimit 1000: depth 1200 `json.loads` OK, depth 3000 `RecursionError`; `..._py314.txt` - Python 3.14.2 (the `python` the Lead's RED arms ran under): depth 1200 OK, depth 3000 OK. So the Lead's arms were TRUE on 3.14 (the walk raised at 3000) and FALSE on 3.12 (the parser raised at 3000); the record did not name the interpreter and the fence is interpreter-dependent. F-1 stands. The shipped guards are correct at every depth on both interpreters (the reviewer's own probes: no raw exception escapes at HEAD); the defect is the evidence and the fence, "delete it and the suite stays green" on the pinned interpreter.
**Lesson (permanent):** a fence that depends on which layer raises first must be derived at test time, and RED evidence must be produced on the PINNED interpreter (the one the lane runs), not on whatever `python` resolves to.

## NITs
- **F-2** the adapter has a THIRD parse site with no `RecursionError` guard (the "both" parity claim is wrong) - fix with F-1.
- **F-3** the receipt-side no-clobber arm is untested (only the target-side race is).
- **F-4** the exporter's walk-guard message ("nested too deeply") is unreachable on 3.12 (the parser raises first) - unify the message or derive the depth.
- **F-5** `_publish`'s POSIX docstring over-states the alternatives (link+unlink / renameat2) - trim.
- Record-side: the reviewer could not find `P030_NIT_SLICE_20260918/LEAD_VERIFICATION_P030_NIT.md` in CT13 (wave 23 pushed it after the read ran) - now present.

## Repair (NOT built today - owner: "complete unfinished work, start nothing new"; this is session 7's first task)
1. Both checkers: derive the nesting depth at test time - the smallest depth at which `json.loads` succeeds but the recursive walk raises (probe upward from 1000 in steps until `json.loads` no longer raises; assert the refusal there) - PLUS keep a depth-3000 arm (the parser clause on 3.12); produce RED for the walk-guard mutants AND the parser-clause mutants on BOTH interpreters (the pinned 3.12 venv and 3.14) and record which layer raised where.
2. Guard the adapter's third parse site the same way (F-2); one message per site (F-4).
3. Add the receipt-side race arm (F-3); trim the POSIX docstring (F-5).
4. Correct `LEAD_VERIFICATION_P030_NIT.md` (name the interpreter per arm) and the commit message's claim in the new commit's message; Gemini delta; exact-Opus re-read (lane 3 attempt 5); Sol on the final bytes.
Until repaired, the Sol P030 lane should read `45a7f50e` (the bytes exact-Opus passed) rather than `d426e79f` - or wait for the repaired pin if session 7 lands it before 18:47.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`); machine stamps in the queue log.
