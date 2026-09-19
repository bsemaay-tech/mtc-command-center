# LEAD_ADJUDICATION - lane 4 attempt 2: exact-Opus read of the WP-P0-26 NIT slice `505af399` (Sat 2026-09-19 08:58-09:21 UTC+3)

**Verdict as written:** **PASS-WITH-NITS, 0 REQUIRED, 5 NITs.** 650 lines, 154 turns, launcher exit 0, no cap. HEAD and subject digests computed by the reviewer; scope exactly the five files of the slice; both NIT-1 checks individually load-bearing under the reviewer's own mutants (a1/a2/a3 each fail the tampered-marker test; a gate bypass fails 7+3); NIT-5 deadness confirmed by reading; no restore path bypasses `verify_completion_evidence`; the doc changes judged honest; Lead records vs bytes consistent. Gemini `P026_NIT_GEMINI` PASS on the same bytes. **P0-26 candidate `505af399`: exact-Opus PASS-WITH-NITS + Gemini PASS → Sol tonight.**

## NITs (Lead disposition)
- **NIT-1** four refusals in the completion gate are sole guards with no test (`opsa_common.py:213-214` marker schema; `restore.py:92-93` per-run malformed lines, `:94-96` header, `:111-112` per-record readback): delete any one and the 39-test suite stays green; two more degrade to uncaught exceptions. Real, the "delete it and the suite stays green" shape; the shipped code is correct. **Carried to the next P0-26 slice (fence all six).**
- **NIT-2** the gate's per-run manifest read is unguarded for non-UTF-8 bytes (uncaught `UnicodeDecodeError` instead of `run_not_complete`). Carried (same slice).
- **NIT-3** the NIT-4 note covers Part A only; one `--latest` command survives unmarked in section C4 of the evidence doc. Carried (doc).
- **NIT-4 (authority)** `RESTORE_DRILL_EVIDENCE.md` is the eighth file on the branch, outside the packet's five-file ceiling, and no owner row names it (`OD-20260918-P026-N2-DOC-1` covered README/runbook text; the evidence doc is a triage transcript). The reviewer is right: the Lead deferred that question in the first adjudication and then edited the file. **Owner one-liner `P26-EVID A|B`: A = keep the dated note in the merge PR (record a row), B = drop that one hunk to the follow-up slice.** Default (silence): B before the merge PR - the note is re-applied in the follow-up slice with its own row.
- **NIT-5** README `:74` and `watchdog.py:38` usage examples still show `--silence-seconds 900` while `OD-20260914-P030-P026-CONFIG-1` ratified 300 s (the code has no default; pre-existing, byte-identical to base). Carried (doc fix, next slice).

## Standing
Roster for P0-26 at `505af399`: exact-Opus PASS-WITH-NITS (this read) + Gemini PASS; Sol tonight (Codex reset 18:47) on the same bytes; then the merge PR (PR-only serial merge; NIT-3 of the first read = P0-30 F8 lives on the P0-30 branch - the second PR to land rebases the adapter checker). The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`); machine stamps in the queue log.
