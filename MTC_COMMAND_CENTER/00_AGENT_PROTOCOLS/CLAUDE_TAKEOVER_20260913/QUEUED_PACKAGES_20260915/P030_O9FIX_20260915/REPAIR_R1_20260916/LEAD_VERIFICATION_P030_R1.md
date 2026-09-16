# LEAD_VERIFICATION — WP-P0-30 archive exporter, T0 repair round 1 (`0be0a8aa`) after the lane-3 exact-Opus REQUEST_CHANGES on `153edee9` — 2026-09-16 15:2x UTC+3 (12:2xZ)

**Trigger:** Wednesday lane 3 run early (owner: use the Pro allowance) 14:21-15:07 UTC+3: exact `claude-opus-5` xhigh T0 review of `153edee9` → **REQUEST_CHANGES**, 2 REQUIRED + 6 NITs (`OPUS_QUEUE_20260916/P030/ATTEMPT1_REQUEST_CHANGES_153edee9/OPUS_T0_REPORT.md`, 417 lines). **Role:** Lead = the same implementer as O9FIX (disclosed builder, `OD-20260915-BUILD-ABC-1` item a); repair dispatch is the Lead's role; T0 cap 3 rounds — this is round 1. The Lead never accepts its own code: a fresh exact-Opus read (lane 3 re-pinned) and Sol (Fri) decide.

## 1. Lead reproduction of the REQUIRED findings BEFORE the repair (`LEAD_REPRO_lane3_F1_F2.txt`, pinned interpreter 3.12.12, worktree `153edee9`)
| Finding | Lead probe | Result |
|---|---|---|
| F1 — refusal after the target exists leaves a consumable / truncated partition | `Path.open` wrapped so the target's write stores half the bytes then raises `OSError(28)` | refusal `target_unwritable`; **target exists, 616 of 1232 bytes, LF-terminated strict prefix; the backup adapter `capture_stable_prefix` ACCEPTED it** and wrote a stable-prefix receipt |
| F2a — `..` traversal | declared root `…/bars`, path `…/bars/../../outside/2026-02.jsonl` | **ACCEPTED**, receipt `source_path = ../../outside/2026-02.jsonl` |
| F2b — junction component | `mklink /J root/link → outside`, path `root/link/2026-02.jsonl` | **ACCEPTED** (`link/2026-02.jsonl`) while the adapter refuses the same path ("must not be a symlink or junction component") |
Both findings are real; both were reproduced independently of the reviewer's transcript.

## 2. The repair (`0be0a8aa`; parent `53b43c21` = format-only reflow of the two files, verifiable with `ruff format --check`; old 20 tests pass at those bytes)
- **F1:** `STAGING_SUFFIX = ".p030partial"`; the partition and the receipt are written under staging names (`xb`, flush + fsync), the bytes re-read against the staging file, and both published by `os.replace` — the receipt FIRST (inert without its partition), then the target, each name re-checked for existence immediately before publication. No refusal path leaves bytes under the target's own name; a leftover staging partial is never a partition name, stays in place (no delete code path — `opsa_common.py` invariant) and is named in the refusal; a later run refuses `target_exists` on it. Documented residual window: if publishing the target fails after the receipt was published, a receipt-without-partition remains (inert) and the staging partial stays.
- **F2:** `_source_rel` now: literal relative_to → canonical relative POSIX rule (no `.`/`..`/empty segment, no backslash/NUL, no drive/root, spelling stable) → no symlink/junction component on the way down from the filesystem root (the adapter's `_refuse_source_links` walk) → resolved source under resolved root (non-strict resolve so a missing leaf still reports `source_unreadable`). Refusal code `source_outside_root` reused; **no new refusal code** (the 16-code table stands).
- **NITs applied:** F3/K-06 (one exact message per overflow/NaN arm), F5 (`exporter_sha256` LF-normalised: equals the sha256 of the git blob bytes on any checkout; test forces a CRLF read and expects the same digest), F7 (unwritable/verify tests assert nothing under the target name). **Not in this commit:** F4/K-07 (the O9FIX packet's `SHA256SUMS.txt` hashed the CRLF checkout — a packet-craft note; the repair packet below hashes `git show` blobs), F6 (citation offsets in the O9FIX records — corrected in the records, see §5), F8 (adapter checker `ensure_ascii` vs a non-ASCII temp path — out-of-scope file; follow-up).

## 3. Evidence
| Item | Result | File |
|---|---|---|
| GREEN | `check_p030_archive_exporter.py`: **Ran 25 tests … OK** (20 → 25: mid-write ENOSPC, publish-failure residual window, LF digest on a CRLF checkout, `..` traversal (+ adapter parity), junction component (+ adapter parity)); D-13 RED/GREEN lines unchanged | `LEAD_CHECKER_R1_GREEN.txt` |
| RED arm | new checker vs the pre-repair exporter bytes (file swap inside the worktree, restored byte-identical): **7 of 25 fail** — traversal, junction, LF-digest by behaviour; the four staging-dependent tests error on the missing constant | `LEAD_RED_ARM_new_checker_vs_153edee9.txt` |
| Sibling checkers | `check_p030_closed_partition_backup_adapter.py` OK; `check_p030_market_data_contracts.py` PASS; `check_market_data_collector.py` PASS | console (§ run at 15:1x) |
| Ruff | `ruff format` applied (format-only commit first); `ruff check`: the three pre-existing findings only (I001, SIM117, RUF059 at the old test) — 0 new | `LEAD_RUFF_R1.txt` |
| Guard | `RESULT: PASS`; staged exactly the two files | `LEAD_GUARD_R1.txt` |
| Push | `feature/p030-integrated-20260913` = origin @ `0be0a8aa` | git |

## 4. Roster
- Lane 3 re-pinned to `0be0a8aa` (`run.ps1`, `REVIEW_BRIEF.md` + addendum naming the two closures to re-probe, agent brief, queue row); attempt 1 archived under `P030/ATTEMPT1_REQUEST_CHANGES_153edee9/`. Tonight's launcher re-runs it (no `launch.exit`).
- Gemini detection of the delta `153edee9..0be0a8aa` (`P030_R1_GEMINI`, prepared; launched once no Pro lane runs).
- Sol Friday generates from the re-pinned brief.

## 5. Records corrected (F6, documentary)
`DISPOSITION_O9FIX.md:3` exporter delta `+17/−2` → `+19/−2`; `GEMINI/LEAD_ADJUDICATION.md:26` `+21/−2` → `+19/−2`; `DISPOSITION_O9FIX.md:11` class span `:266-462` → `:263-451`; `DISPOSITION_O9FIX.md:48` branch line `:131` → `:136` (all as recomputed by the reviewer from the blobs at `153edee9`; the Lead re-checked the first two by `git diff --numstat`).

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
