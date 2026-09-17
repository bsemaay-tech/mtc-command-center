# LEAD_ADJUDICATION — lane 4: exact `claude-opus-5` xhigh T0 review of WP-P0-26 OPS-A candidate `e114ed31` (README + restore contract repair) — 2026-09-17 13:2x-13:3x UTC+3

**Lane:** `OPUS_QUEUE_20260916/P026/opus/run.ps1`, Claude PRO profile, launched by hand 13:02 UTC+3 when the Pro window reopened; 13:02-13:22 (10:02:20-10:22:19Z), launcher exit 0, 157 turns, no 429; report `opus/OPUS_T0_REPORT.md`, 480 lines; own RED arms A1-A13 incl. the original defect reproduced on the pre-fix modules (§2 arm c), D026 RED on the pre-fix behaviour (§3), contract-change blast radius (§4), Lead authorship weighed (§6; `OD-20260915-P026-ADAPTER-LEAD-1` "A"), the Lead's record checked line by line against the bytes (§7), the author-disclosed README residual graded (§8).
**Verdict as returned:** `VERDICT: PASS-WITH-NITS` — **0 REQUIRED**, five NITs, eight NOT VERIFIED items. The reviewer accepts nothing; the Lead never accepts its own code.

## Lead reproduction
| Check | Result |
|---|---|
| Citations — `restore.py:71-112`, `:99-107`, `:200`; `backup.py:227`, `:237`, `:260`, `:268-278`; `opsa_common.py:153-165`; `check_p030_closed_partition_backup_adapter.py:837`; `RESTORE_DRILL_EVIDENCE.md:10,120,152,477` | **EXACT** at the `e114ed31` blobs (the completion gate reads `schema`, `run_id`, `run_manifest_sha256`, `files` only — `readback`/`bytes`/`skipped`/`dirs`/`started_at`/`finished_at` never read, as stated) |
| NIT-3 (checker anchor `ensure_ascii=True` vs the adapter's `ensure_ascii=False`) | **CONFIRMED today** in the P0-30 lane (same file, same test: ASCII `TEMP` → OK, long-form user `TEMP` → `AssertionError: 0 != 1`); the reviewer's base-tree run shows it is inherited from master, not introduced |
| NIT-5 (dead `and status == "ok"` at `backup.py:237`) | confirmed by reading `:227` (`status` is derived from `errors` alone) |
| NIT-1 / NIT-2 / NIT-4 | read against the bytes; the arms A9 (falsified marker fields → restore rc 0, label `verified`) and A13 (torn marker strands an intact run) are as described; not re-run by the Lead — the reviewer's arms are in `C:/tmp/OPUS_P026_SCRATCH/` |

## NITs — disposition (carried; the candidate pin `e114ed31` is NOT moved before the Sol read)
| # | Finding | Lead reading | Disposition |
|---|---|---|---|
| NIT-1 | `COMPLETE.json` fields beyond the four checked are never validated, yet restore prints `"completion_marker": "verified"` | true; not a data-integrity fail-open (digest-bound manifests + per-file sha256 guard the restore) — an operator-facing over-claim | **carried, engineering follow-up** (assert `readback == "all_match"` and `run_manifest == RUN_MANIFEST_NAME`, or narrow the label to `pair_verified`; + test) |
| NIT-2 | `write_once_bytes` is O_EXCL, not atomic publication: a torn `COMPLETE.json` strands a run whose data is intact, and the package has no delete primitive to clear it | true; the tmp+rename fix collides with the no-delete guarantee on POSIX | **owner one-liner** `P26-N2 doc|change` — `doc` = one README line ("a run with an unreadable marker is re-backed-up under a new run id; its data is not lost"); `change` = a separately scoped `COMPLETE.json.tmp` + fsync + `Path.rename` onto a non-existent target (Windows-atomic, no delete) |
| NIT-3 | the P0-30 adapter checker's config anchor is ASCII-only (`json.dumps` default) while the adapter writes UTF-8 — red gate under a non-ASCII temp path (inherited from master) | true; = P0-30 F8 / N5, now hit by three reviewers | **carried into the same follow-up slice** (`json.dumps(configured_root, ensure_ascii=False)` + a non-ASCII temp-path arm); the candidate legitimately touches this file |
| NIT-4 | `RESTORE_DRILL_EVIDENCE.md` still instructs `--latest` (removed on this branch); its commands now exit 2 and the 2026-08-24 run has no `COMPLETE.json` | true; failure is safe (rc 2/3) | **record fix** (a dated note at the top of Part A: contract changed, `--latest` removed, reproduce with an explicit `--run <id>` of a run backed up by the current tool; recorded transcript = pre-change tool) — never rewrite the recorded output; rides with the follow-up slice unless the owner wants it in the merge PR |
| NIT-5 | dead condition `backup.py:237` | harmless | **carried** (delete with the follow-up slice) |

## Standing
Lane 4 COUNTED: exact-Opus PASS-WITH-NITS on `e114ed31`, 0 REQUIRED; Gemini delta on `e114ed31` COUNTED PASS (2026-09-15). Roster still needs the second flagship (exact Sol, Sep 19) before any merge; the Lead built the candidate and cannot accept it. NITs 1/3/4/5 → one follow-up slice after the Sol read; NIT-2 → owner one-liner.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
