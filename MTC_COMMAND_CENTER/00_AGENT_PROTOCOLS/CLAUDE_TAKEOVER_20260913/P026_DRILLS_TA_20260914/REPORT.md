# REPORT

Corrector pass P26FIX1 (grok-4.6) over the T-A D-1..D-14 fixture drills. Nothing here is acceptance or authorization.

## Interpreter

- `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` (3.12)
- Each `drills/D-*/run.py` binds `TEMP`/`TMP` to `C:/tmp/P026_DRILLS_TA_20260914/tmp` and `PYTHONUTF8=1`.
- Stdout/stderr captured through Python as UTF-8 (no PowerShell `>` UTF-16).

## Copied-source digests

- See `wt/COPIED_SOURCES_SHA256SUMS.txt`. Drills import only from `wt/` (plus stdlib and the pinned interpreter).

## Verbatim summary outputs (UTF-8 stdout)

- `drills/D-1/stdout.txt:1-6`: (a) wrap + inner `backup config field 'backup_root' must be a non-empty string`; (b)(c) named refusals; (d) parsed config.
- `drills/D-2/stdout.txt:1-7`: dry-run header, two PLAN lines, footer `files: 0, bytes: 0`, empty `backup_root_d2` listing.
- `drills/D-3/stdout.txt:1-9`: D-3 six receipt fields; D-3b inside-file GREEN 620/1860; mid-record newline RED; truncated-high-water RED.
- `drills/D-4/stdout.txt:1-15`: three byte comparisons, `run_id=opsa-20260914T061919.156Z`, manifest types, `readback=match`, member-set.
- `drills/D-5/stdout.txt:1-23`: check-only then restore; receipt identity + six fields; type checks; restored=archived.
- `drills/D-6/stdout.txt:1-6`: snapshot-only hits `:347`; receipt tamper hits `:315`; targets empty; named P026 string not reached.
- `drills/D-7/stdout.txt:1-6`: five complete-run refusals plus `invalid P026 manifest line 13`.
- `drills/D-8/stdout.txt:1-10`: four isolated falsifications then GREEN emit/verify/available sidecar; leftover hb is P026-shaped.
- `drills/D-9/stdout.txt:1-63`: nine isolated states, rc 0/2/3, notifier events including `_watchdog_check`.
- `drills/D-10/stdout.txt:1-13`: silent → recovered (`recovered_from=silent`) → silent.
- `drills/D-11/stdout.txt:1-7`: IDENTICAL_REPLAY_NOOP + cursor seed; correction-contract OR; WS_LIVE gap.
- `drills/D-12/stdout.txt:1-3`: one GAP line, `GAPS: 1`, rc=0.
- `drills/D-13/stdout.txt:1`: RED half `prefix record is not canonical JSONL`.
- `drills/D-14/stdout.txt:1-5`: GREEN `lines=4`; empty page; `snapshot cursor made no progress`; `snapshot left 1 bar(s) missing`.

## DRILL_RESULTS

- See `DRILL_RESULTS.md` (per-case outcomes + true deviations).
- See `DISPOSITION_FIX1.md` for audit findings 1–13.

## Not verified / not proven

- T-B and T-C drills are not run (`D-15`, `D-16`, `D-17`).
- No real archive/backups roots were used (all fixtures under `fixtures/`).
- Nothing from this lane is acceptance or authorization.
- `D-13`: RED half completed; GREEN transform not executed (requires O-9).
- `D-14`: gap-backfill uses a stub source (`SnapshotSource`) rather than a live venue path.
- D-6 snapshot-only tamper does not exercise `restore.py` `sha256 mismatch` / adapter `:727-728`; the receipt check at `:347` fires first by design.
- Byte-identity of `wt/` against worktree `C:/tmp/P030_INTEGRATION_20260913` at HEAD `f42fd5400b2c2ecb805644d406999cb55c8178c8` was not re-hashed (no git).
