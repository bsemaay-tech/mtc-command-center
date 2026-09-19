# DISPOSITION_O9FIX — Gemini NITs K-01..K-05 on the WP-P0-30 Shape-B exporter candidate `daf6a43b` — 2026-09-15 night

**Builder:** the Claude Opus 5 Lead (session 5, `03c6c8`) under `OD-20260915-BUILD-ABC-1` item (a) (owner "all"; the brief was written for Codex Plus, which is weekly-capped until Sep 19). Disclosed authorship; the Lead does not accept its own change. Worktree `C:/tmp/P030_INTEGRATION_20260913`, branch `feature/p030-integrated-20260913`, base `daf6a43b0c4eaafd78e84df776d30d3e41d81d7b`. Interpreter: pinned Python 3.12.12 (`C:/tmp/P020_IMPL_20260912/…/.venv/Scripts/python.exe`). Exactly two files changed, nothing added: `p030_archive_exporter.py` (+19/−2 (corrected 2026-09-16, lane-3 review finding 6)) and `check_p030_archive_exporter.py` (+203). The collector, the adapter and the contracts module are untouched (`git diff --stat -- market_data_collector.py` empty; see the commit).

## K-01..K-05
| Finding | Disposition | Where (HEAD) | Test |
|---|---|---|---|
| K-01 float overflow (`1e999`) raised a raw `ValueError` from `_reject_nonfinite_numbers` outside the `json.loads` guard | **FIXED** — the walk is wrapped: `ValueError` → `ExportRefused("source_line_invalid", "… carries a non-finite number")` | `p030_archive_exporter.py:159-167` | `test_source_line_invalid_for_overflow_and_nan_literals` (`:352`): `1e999`, `NaN` literal, nested `-1e999` |
| K-02 `dataset_content_hash` refusals leaked as raw `ContractRefused` from `export_partition` | **FIXED** — the call (with `_descriptor` inside it) is wrapped: `ContractRefused` → `ExportRefused("contract_refused", str(exc))`; `mixed_dataset_descriptor` (raised by `_descriptor`, already an `ExportRefused`) passes through unchanged | `p030_archive_exporter.py:287-292` | `test_contract_refused_from_slice_validation` (`:389`): duplicate rows → "duplicate observation_id"; `bar_close_time == bar_open_time` → "must be after bar_open_time" |
| K-03 `_utc_z` accepted sub-second timestamps although the adapter refuses them (`p030_closed_partition_backup_adapter.py:139` `must use whole seconds`) | **FIXED** — `parsed.microsecond != 0` → `ExportRefused("invalid_timestamp", "exported_at_utc must use whole seconds")` | `p030_archive_exporter.py:109-112` | `test_invalid_timestamp_refusals_including_sub_second` (`:301`): `.500Z` and `.000001Z` refused; `+00:00`, no-`Z`, `not-a-time`, an int → the existing "UTC Z timestamp" refusal |
| K-04 11 of 16 refusal codes had no negative test | **FIXED** — new class `ArchiveExporterRefusalCodeTests` (`:263-451 (corrected 2026-09-16, finding 6)`), one explicit test per code; the D-13 RED/GREEN pair and the eight existing tests are unchanged | `check_p030_archive_exporter.py:266-462` | table below |
| K-05 `REPORT.md:19` cited `p030_archive_exporter.py:210` for the `DATASET_ROW_FIELDS`-ordered return (actual at `daf6a43b`: `:211`) and `check_p030_archive_exporter.py:144` for field preservation (actual: the loop at `:151-153`; `:144` asserts the observation-id regex) | **CORRECTED HERE** (the previous lane's `REPORT.md` is not edited): at this HEAD the return is `p030_archive_exporter.py:223` and the preservation loop is `check_p030_archive_exporter.py:151-153` (unchanged lines) | — | — |

## Refusal-code coverage after O9FIX (16/16)
| Code | Test (all in `check_p030_archive_exporter.py`) |
|---|---|
| `target_exists` | `test_target_exists_refusal` (existing) |
| `receipt_exists` | `test_receipt_exists_refusal` (new) |
| `invalid_timestamp` | `test_invalid_timestamp_refusals_including_sub_second` (new; six arms) |
| `source_outside_root` | `test_source_outside_root_refusal` (new) |
| `source_unreadable` | `test_source_unreadable_refusal` (new) |
| `short_read` | `test_short_read_refusals` (new; missing trailing newline; `stat` size larger than the bytes read) |
| `empty_partition` | `test_empty_partition_refusal` (existing) |
| `source_line_invalid` | `test_malformed_line_refusal` (existing) + `test_source_line_invalid_for_overflow_and_nan_literals` (new) |
| `source_line_noncanonical` | `test_source_line_noncanonical_refusal` (new) |
| `source_fields_mismatch` | `test_source_fields_mismatch_refusal` (new) |
| `contract_refused` | `test_contract_refused_from_row_identity` (new; non-decimal `open`) + `test_contract_refused_from_slice_validation` (new; K-02) |
| `identity_mismatch` | `test_prefixed_identity_mismatch_is_refused` (existing) |
| `mixed_dataset_descriptor` | `test_mixed_dataset_descriptor_refusal` (new) |
| `target_unwritable` | `test_target_and_receipt_unwritable_refusals` (new; `Path.open` denied for the target) |
| `target_verify_failed` | `test_target_reread_byte_identity_refusal` (existing) |
| `receipt_unwritable` | `test_target_and_receipt_unwritable_refusals` (new; `Path.open` denied for the receipt; target written, receipt absent) |

## Evidence (verbatim tails in `LEAD_*.txt` beside this file)
| Check | Result |
|---|---|
| `python check_p030_archive_exporter.py` | `Ran 20 tests … OK` (was 8) — `LEAD_check_p030_archive_exporter.txt` |
| `python check_market_data_collector.py` | exit 0 — `LEAD_check_market_data_collector.txt` |
| `python check_p030_market_data_contracts.py` | exit 0 — `LEAD_check_p030_market_data_contracts.txt` |
| `python check_p030_closed_partition_backup_adapter.py` | `Ran 44 tests … OK`, exit 0 — `LEAD_check_p030_closed_partition_backup_adapter.txt` |
| **RED arm** — the NEW checker against the OLD exporter (`git show daf6a43b:p030_archive_exporter.py`, sha256 `1389c1aa…`, scratch copy) | `Ran 20 tests`, `FAILED (failures=1, errors=2)`: K-01 arm ERROR `ValueError: non-finite JSON number` (raw leak), K-02 arm ERROR (raw `ContractRefused`), K-03 arm FAIL `ExportRefused not raised` — exactly the three behaviours the fix changes; the other 17 pass on both — `LEAD_RED_ARM_new_checker_old_exporter.txt` |
| Ruff `--select E9,F821,F811,F401,F841` on both files | `All checks passed!` — `LEAD_RUFF_O9FIX.txt` (`ruff format` deliberately NOT applied: the base files were not format-clean before O9FIX; the lane's style is kept) |
| repo guard / `git diff --check` | PASS / clean (in the commit record) |
| Collector untouched | `git diff --stat daf6a43b HEAD -- market_data_collector.py` → empty |

## Notes for the roster
- One expectation the Lead first wrote was wrong and was removed from the test, not from the code: `datetime.fromisoformat` (3.11+) accepts a space separator, so `2026-09-14 00:00:00Z` is a valid receipt timestamp for the exporter; the test now uses `2026-09-14T00:00:00` (no `Z`) for the "not a UTC Z timestamp" arm.
- The `short_read` second arm stubs `Path.stat` to report one byte more than the file holds; it exercises the `observed_size != expected_size` branch (`p030_archive_exporter.py:136 (corrected 2026-09-16, finding 6; :131 is the open line)`), which no real filesystem produces on demand.
- Next: Gemini DELTA review of `daf6a43b..<O9FIX HEAD>` (root `P030_O9FIX_GEMINI`), then the Wednesday exact-Opus lane 3 is re-pinned to the new HEAD; exact Sol Fri 2026-09-19.

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).
