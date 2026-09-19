# LEAD_VERIFICATION - WP-P0-30 NIT slice, repair round 2 (`d426e79f` -> `b4df1413`) - Sat 2026-09-19 (built 09:3x-09:4x UTC+3; committed 09:45, pushed 09:45)

**Trigger:** lane 3 attempt 4 (exact-Opus read of the NIT slice `d426e79f`, 2026-09-18) = REQUEST_CHANGES, one REQUIRED (F-1) + four NITs (F-2..F-5); adjudicated in `OPUS_QUEUE_20260916/P030/LEAD_ADJUDICATION_P030_NIT_T0.md`. **Role:** Lead = disclosed builder (the Lead never accepts its own code). **Scope:** the same four files - `p030_archive_exporter.py`, `check_p030_archive_exporter.py`, `p030_closed_partition_backup_adapter.py`, `check_p030_closed_partition_backup_adapter.py`; blob OIDs at the new HEAD in `BLOB_OIDS_b4df1413.txt`.

## Interpreters (named per arm below - the lesson of F-1)
- **pinned 3.12** = `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` = Python 3.12.12 (the interpreter the lane brief pins and the reviewer used).
- **3.14** = `C:/Python314/python.exe` = Python 3.14.2 (the shell's `python`, the one the d426e79f record was made on).

## Why d426e79f's evidence was inverted (reproduced first, `LEAD_REPRO_R2_nesting_arms_*.txt` + the session-6 `ADJUDICATION_R1_20260919/` probes)
The recursive non-finite walk hits the Python recursion limit (1000 frames) on both interpreters; the parser (`json.loads`) hits a C-level limit that differs: **3.12 raises at ~2998 levels, 3.14 at ~16922**. A hard-coded depth of 3000 therefore reaches the PARSER clause on 3.12 (walk guards untouched) and the WALK guard on 3.14. The d426e79f arms used 3000 and the record was made on 3.14 - true there, false on the pinned interpreter.

## What changed
- **F-1 / F-4:** both checkers gain `nesting_arms()` = `(("walk", d), ("parser", d))` derived on the running interpreter: exponential + binary search (through one fixed frame path) for the smallest depth where anything raises and the smallest depth where the parser raises; the parser raised first iff the two depths coincide; a `_STACK_MARGIN = 64` is added to each depth so the code under test (a few frames deeper or shallower than the search) is on the raising side; each arm asserts its layer's EXACT message, so an arm that lands on the wrong layer fails loudly instead of passing. Arms: exporter `test_pathologically_nested_line_is_a_refusal_not_a_crash` (walk -> `source line 3 is nested too deeply`, parser -> `source line 3 is not parseable JSON`); adapter capture (`_prefix_facts`, both layers -> `prefix record is not canonical JSONL`), NEW `test_manifest_refuses_pathological_nesting_before_p026` (`_decode_strict_jsonl`, both layers -> `invalid P026 manifest line 1`), NEW `test_config_and_receipt_refuse_pathological_nesting_before_p026` (`_decode_json_object`, config and receipt, both layers -> `invalid backup config` / `invalid stable-prefix receipt`). A layer that never raises below 2**20 on some interpreter is skipped by name inside its subTest (neither interpreter here does).
- **F-2:** `_decode_json_object` (the adapter's third parse site: config, receipt, isolated-config reads) catches `RecursionError` at the parser and around the walk -> `ValueError(f"invalid {description}")`, like the other two sites.
- **F-3:** `test_publication_never_replaces_a_receipt_that_appeared_after_the_check` mirrors the target-side race arm with the receipt mocked absent: `receipt_exists` "appeared before publication", foreign receipt bytes intact, target never created, both staging files remain; skipped on POSIX like its twin.
- **F-5:** `_publish` docstring: `os.link` is a delete-free no-clobber form on POSIX at the cost of a permanent second hard link under the staging name and cross-filesystem failure; the exists-check stays the guard and the window stays documented.
- The exporter's walk-guard comment now says why the checker derives the depth.

## Evidence (all files in this directory; scratch trees `C:/tmp/LEAD_P030_SCRATCH_R2/<mutant>/` = worktree `*.py` + `p030_opsa_backup_config.json` + `MTC_COMMAND_CENTER/tools/opsa`; ASCII TEMP `C:/bt_s4/p030_tmp` unless stated; runner `p030_r2_mutants.py` in the session scratchpad)

### Derived depths (search frame; the arms report their own, a few levels lower)
| Interpreter | walk | parser | file |
|---|---|---|---|
| pinned 3.12 | 1060 | 3062 | `LEAD_REPRO_R2_nesting_arms_py312.txt` |
| 3.14 | 1060 | 16987 | `LEAD_REPRO_R2_nesting_arms_py314.txt` |

### RED - one mutant per guard, BOTH interpreters, each errors exactly its own arm
| Mutant (scratch) | pinned 3.12 | 3.14 | files |
|---|---|---|---|
| mutC1 exporter walk guard removed | **1 error**: walk arm (`layer='walk', depth=1049`) RecursionError | same | `LEAD_RED_R2_mutC1_exporter_walk_guard_removed_py31{2,4}.txt` |
| mutC2 exporter parser clause removed | **1 error**: parser arm (`depth=3044`) RecursionError | **1 error**: parser arm (`depth=16877`) | `..._mutC2_..._py31{2,4}.txt` |
| mutD1 receipt-side appeared arm removed (F-3) | **1 failure**: `receipt_unwritable` "could not be published" instead of `receipt_exists` | same | `..._mutD1_..._py31{2,4}.txt` |
| mutC3 adapter `_prefix_facts` walk guard removed | **1 error**: capture arm (`site='_prefix_facts', layer='walk'`) | same | `..._mutC3_...` |
| mutC4 adapter `_decode_strict_jsonl` walk guard removed | **1 error**: manifest arm (`layer='walk'`) | same | `..._mutC4_...` |
| mutC5 adapter `_prefix_facts` parser clause removed | **1 error**: capture arm (`layer='parser'`, 3044) | same (16877) | `..._mutC5_...` |
| mutC6 adapter `_decode_strict_jsonl` parser clause removed | **1 error**: manifest arm (`layer='parser'`) | same | `..._mutC6_...` |
| mutC7 adapter `_decode_json_object` parser clause removed (F-2) | **2 errors**: config + receipt arms (`layer='parser'`) | same | `..._mutC7_...` |
| mutC8 adapter `_decode_json_object` walk guard removed (F-2) | **2 errors**: config + receipt arms (`layer='walk'`) | same | `..._mutC8_...` |

Every other test stays green under every mutant (29 - 1 / 46 - n), so each fence is the ONLY detector of its guard; the summary lines are in `LEAD_MUTANT_RUN_SUMMARY.txt`.

### GREEN
| Run | Result | file |
|---|---|---|
| exporter checker, scratch base, pinned 3.12 / 3.14 | **Ran 29 tests OK** (28 -> 29; 0 skipped) both | `LEAD_GREEN_R2_check_p030_archive_exporter_py31{2,4}.txt` |
| adapter checker, scratch base, pinned 3.12 / 3.14 | **Ran 46 tests OK** (44 -> 46; 0 skipped) both | `LEAD_GREEN_R2_check_p030_closed_partition_backup_adapter_py31{2,4}.txt` |
| exporter checker, WORKTREE, pinned 3.12 | Ran 29 OK; D-13 RED RAW REFUSAL / GREEN EXPORTED CAPTURE: PASS | `LEAD_GREEN_R2_worktree_exporter_checker_py312.txt` |
| adapter checker, WORKTREE, pinned 3.12, ASCII TEMP | Ran 46 OK | `LEAD_GREEN_R2_worktree_adapter_checker_py312_ascii_TEMP.txt` |
| adapter checker, WORKTREE, pinned 3.12, long-form non-ASCII TEMP (F8 arm) | Ran 46 OK | `LEAD_GREEN_R2_worktree_adapter_checker_py312_nonascii_TEMP.txt` |
| sibling checkers, pinned 3.12 | contracts PASS; collector PASS | (console) |
| Ruff (uvx ruff 0.16.8, worktree config) | per file identical to HEAD by rule: exporter 0; checker I001/RUF059/SIM117; adapter E402x3/I001x2/RUF100x3/TRY004x3; adapter checker B023x10/S102x4/SIM117x28; `ruff format --check` clean on the exporter pair; adapter files not reformatted (they "would be reformatted" at HEAD too) | (console) |
| Guard (dry-run, worktree, four files staged) | `RESULT: PASS`, protected none | `LEAD_GUARD_P030_NIT_R2.txt` |

## Not done / carried
POSIX window unchanged (documented, not closed). The `test_committed_configuration_is_explicitly_non_runnable` scratch artefact of the d426e79f record does not recur (the scratch now carries `p030_opsa_backup_config.json`). Roster: Gemini delta `P030_R2_GEMINI` (packet `P030_R2_20260919`) -> lane 3 attempt 5 = exact-Opus read of `b4df1413` (repair round 1 of the slice read's cap 3) -> Sol on the final bytes tonight (Codex reset 18:47). The Lead never accepts its own code.

Recorded by Claude Fable 5.1 Lead (session 7, `18c1b8`); machine stamps in `OPUS_QUEUE_20260916/QUEUE_LOG.txt`.
