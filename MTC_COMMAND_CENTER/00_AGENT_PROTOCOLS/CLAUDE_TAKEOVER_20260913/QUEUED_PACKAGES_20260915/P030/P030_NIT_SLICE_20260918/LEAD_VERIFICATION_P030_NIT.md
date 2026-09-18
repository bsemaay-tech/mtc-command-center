# LEAD_VERIFICATION - WP-P0-30 NIT slice (`d426e79f` = `45a7f50e` + N1-N5/F8) - 2026-09-18, built while the owner's "build the NIT slices now" plan runs (Sol reads the final bytes on 2026-09-19)

**Base:** `45a7f50e` - exact-Opus PASS-WITH-NITS (0 REQUIRED, `OPUS_QUEUE_20260916/P030/LEAD_ADJUDICATION_P030_R1_T0.md`), Gemini `P030_R1` PASS-WITH-NITS. **Role:** Lead = disclosed builder. **Scope:** four files - `p030_archive_exporter.py` (blob `62779b39`), `check_p030_archive_exporter.py` (`ba6089d7`), `p030_closed_partition_backup_adapter.py` (`e67e885e`), `check_p030_closed_partition_backup_adapter.py` (`2c5685f1`); +157/-18; the adapter files carry ONLY the semantic lines (they were not ruff-formatted at HEAD and were not reformatted - a first `ruff format` pass on them was reverted).

## What changed
- **N1** `_publish(staging, final)`: Windows `os.rename` (refuses an existing destination with `FileExistsError`; nothing unlinked); POSIX: exists-check immediately before `os.replace`, residual window documented in the docstring, not closed (link+unlink would add a delete path; renameat2 is not portable). Both publication sites (receipt first, then target) refuse a destination that appeared with `receipt_exists` / `target_exists` naming the staging file that remains; the existing `OSError -> target_unwritable / receipt_unwritable` paths are unchanged (FileExistsError is caught first).
- **N2** the `STAGING_SUFFIX` comment and the stage/verify/publish comment claim only what the bytes support.
- **N3** D-13 GREEN arm: `stable["prefix_sha256"] == receipt.exported_sha256 == sha256(target bytes)`.
- **N4** exporter: `RecursionError` added to the parser's except (defence in depth) AND a new `except RecursionError -> source_line_invalid ("nested too deeply")` around the non-finite walk - on this interpreter (3.14) `json.loads` accepts 3000 levels and the recursive walk is where the error arises. Adapter: `RecursionError` in both parse sites' excepts AND a `try/except RecursionError` around both walks -> the sites' existing `ValueError` messages (parity).
- **N5 / F8** adapter checker: the config anchor and replacement built with `json.dumps(..., ensure_ascii=False)` like the config writer; a deep-nesting arm added to `test_capture_refuses_partial_line_and_noncanonical_jsonl`; the publish-failure test denies the platform primitive (`os.rename` on Windows, `os.replace` elsewhere).

## Evidence (`P030_NIT_SLICE_20260918/`; mutants on the scratch copy `C:/tmp/LEAD_P030_SCRATCH_NIT/` (worktree `*.py` + `MTC_COMMAND_CENTER/tools/opsa`), ASCII TEMP `C:/bt_s4/p030_tmp`)
| Arm | Result | File |
|---|---|---|
| N1 - publish by `os.replace` again | **2 failed** (the new race test; the publish-failure test) | `LEAD_RED_P030_N1_publish_overwrites_again.txt` |
| N3 - extra byte written to the staging target after hashing | 3 failed + 4 errors (capture refuses non-canonical bytes before the binding assertion - not the clean fence) | `LEAD_RED_P030_N3_exported_bytes_drift_from_receipt.txt` |
| **N3b** - receipt `exported_sha256` computed over other bytes (bytes stay canonical) | **2 failed**: the D-13 binding assertion (`prefix_sha256 != exported_sha256`) and the receipt-fields test | `LEAD_RED_P030_N3b_receipt_hash_over_other_bytes.txt` |
| N4 exporter - parser-clause mutant (first attempt) | **SURVIVED** (28 OK): the error arises in the walk, not the parser, on this interpreter - superseded | `LEAD_RED_P030_N4_exporter_recursion_escapes.txt` |
| **N4 exporter - walk guard removed** | **1 error** (`RecursionError` escapes the nesting test) | `LEAD_RED_P030_N4_exporter_walk_guard_removed.txt` |
| N4 adapter - parser-clause mutant (first attempt) | 2 errors (the nesting arm + the scratch artefact below) - superseded by the walk-guard arm after the adapter's walk was guarded | `LEAD_RED_P030_N4_adapter_recursion_escapes.txt` |
| **N4 adapter - prefix walk guard removed** | **1 error** (the nesting arm) + the scratch artefact | `LEAD_RED_P030_N4_adapter_walk_guard_removed.txt` |
| Scratch baselines | exporter checker 28 OK; adapter checker 44 with ONE error `test_committed_configuration_is_explicitly_non_runnable` - a scratch artefact (the test resolves a committed config under the repository tree, absent from the scratch copy); it passes in the worktree | `LEAD_RED_P030_BASELINE_*.txt` |
| **F8 RED at HEAD** under the long-form non-ASCII TEMP (`C:/Users/Bar??Semaay/...`) | `test_isolated_config_redirect_after_check_never_reaches_restore ... AssertionError: 0 != 1` | `LEAD_RED_F8_adapter_checker_HEAD_under_nonascii_TEMP.txt` |
| GREEN exporter checker (worktree, ASCII TEMP) | **Ran 28 tests OK** (26 -> 28) | `LEAD_GREEN_exporter_checker.txt` |
| GREEN adapter checker (worktree) under the short-form TEMP and under the long-form non-ASCII TEMP | **Ran 44 tests OK** both | `LEAD_GREEN_adapter_checker_nonascii_TEMP.txt`, `LEAD_GREEN_F8_adapter_checker_patched_under_nonascii_TEMP.txt` |
| Ruff (uvx ruff 0.16.8, worktree config) | findings per file identical to HEAD by rule text (exporter 0; checker I001/RUF059/SIM117 = 3; adapter 8; adapter checker 42); exporter + checker formatted, adapter files untouched by the formatter | (counts in the queue log) |
| Guard | `RESULT: PASS`; staged exactly the four files | `LEAD_GUARD_P030_NIT.txt` |
| Gemini delta `P030_NIT_GEMINI` (packet `P030_NIT_20260918`, 24 files) | see `GEMINI/` and the queue log | `GEMINI/` |

## Not done / carried
The POSIX race window stays open by design (documented). The Bridge full suite is not the exporter's home (the P0-30 tools live at the repository root with their own checkers - both run). Roster: exact-Opus re-read of `d426e79f` on the next free Pro lane (after the DD-06 fifth read), Sol Saturday on the same bytes; the Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`); machine stamps in `OPUS_QUEUE_20260916/QUEUE_LOG.txt`.
