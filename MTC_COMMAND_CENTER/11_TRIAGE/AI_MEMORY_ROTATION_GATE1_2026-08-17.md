# AI memory live-journal rotation — Gate 1

**Date:** 2026-08-17  
**Owner authorization:** overnight seven-workstream instruction, item 6  
**Audit tier:** T2 — documentation/history preservation; one reviewer, one round

## Purpose

Reduce repeated context cost without deleting or summarizing any historical
memory. This package is a lossless rotation only.

## Allowed files

- `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
- new `MTC_COMMAND_CENTER/_AI_MEMORY/archive/GLOBAL_HANDOFF_2026-08-01_to_2026-08-15.md`
- new `MTC_COMMAND_CENTER/_AI_MEMORY/archive/NEXT_STEPS_2026-08-01_to_2026-08-10.md`
- new `MTC_COMMAND_CENTER/_AI_MEMORY/archive/START_HERE_STALE_BANNER_2026-08-12.md`

No other file may change. In particular, do not touch `SESSION_LOCK.md`,
`ACTIVE_FILES.md`, existing archives, Bridge code/docs, the dirty V2 decisions
file, Git refs, hosts, credentials, or runtime state.

## Exact rotation contract

1. `GLOBAL_HANDOFF.md`: preserve the existing original lines 1-245 as the live
   payload. Move original lines 246-end, beginning with the 2026-08-15 heading,
   verbatim into the new archive below a short non-payload archive header. Add a
   short archive pointer after the preserved live payload.
2. `NEXT_STEPS.md`: preserve original lines 1-230 as the live payload. Move
   original lines 231-end verbatim into the new archive below a short
   non-payload archive header. Add a short archive pointer after the preserved
   live payload.
3. `START_HERE.md`: replace only the stale time-sensitive banner at original
   lines 3-9 with a neutral instruction to read the newest top sections of
   `GLOBAL_HANDOFF.md` and `NEXT_STEPS.md`. Preserve the removed banner verbatim
   in its own archive file.
4. Never summarize, reorder, rewrap, normalize, or otherwise rewrite historical
   payload. Preserve line endings deliberately and record any necessary
   normalization in the verification report.
5. Archive headers and live pointers must clearly delimit themselves from the
   preserved payload so reconstruction is deterministic.

## Acceptance evidence

- Record pre-edit SHA-256 and byte/line counts for the three live files.
- Record post-edit SHA-256 and byte/line counts for all six files.
- Reconstruct each original journal from the preserved live payload plus archive
  payload and require byte-for-byte equality with its pre-edit snapshot.
- Require the archived stale `START_HERE` banner to equal the removed bytes.
- Check every current heading from the preserved live payload remains present.
- `git diff --check` passes and only the six allowlisted files change.
- A fresh T2 reviewer returns `PASS` or `PASS-WITH-NITS` before acceptance.

This package authorizes no deletion, worktree removal, log compression, branch
cleanup, deployment, trading, or host action.
