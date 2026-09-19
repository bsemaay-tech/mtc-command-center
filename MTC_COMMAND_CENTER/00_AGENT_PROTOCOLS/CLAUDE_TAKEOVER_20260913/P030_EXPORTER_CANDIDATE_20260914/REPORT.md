# P030 Shape-B Archive Exporter Report

Worktree: `C:\tmp\P030_INTEGRATION_20260913`
Branch: `feature/p030-integrated-20260913`
Owner/scope: `O-9 implement GO`, `OD-20260914-P030-EXPORTER-GO-1`, shape `OD-20260914-P030-BRIDGE-SHAPE-1`
Owned paths: `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py`, `C:\tmp\P030_INTEGRATION_20260913\check_p030_archive_exporter.py`, `C:\tmp\CLAUDE_P0_RUN_20260913\laneO9EXP_build\REPORT.md`, `C:\tmp\CLAUDE_P0_RUN_20260913\laneO9EXP_build\SHA256SUMS.txt`
Live/scheduled dependency check: `Get-Process agy -ErrorAction SilentlyContinue` returned no process output before Git/edit work.

## Design Conformance

| Shape-B promise | Evidence |
|---|---|
| Collector stays byte-for-byte untouched. | No edits were made to `C:\tmp\P030_INTEGRATION_20260913\market_data_collector.py`; the task-relevant collector writer remains `MonthlyArchive._append` at `C:\tmp\P030_INTEGRATION_20260913\market_data_collector.py:295` and the bare hash return remains `C:\tmp\P030_INTEGRATION_20260913\market_data_collector.py:80`. `git -c safe.directory=* diff -- market_data_collector.py` produced no output. |
| Separate exporter function is the bridge. | `export_partition(...)` is implemented at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:236`. |
| Reads one collector-written partition once as bytes and refuses empty/partial source. | `export_partition` calls `_read_source_once` at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:253`; the one-read helper starts at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:123`. |
| Parses source lines strictly without requiring sorted-key source bytes. | `_decode_source_line` starts at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:141`; the collector source shape is the dataclass order from `C:\tmp\P030_INTEGRATION_20260913\market_data_collector.py:90` and compact append at `C:\tmp\P030_INTEGRATION_20260913\market_data_collector.py:298`. |
| Recomputes producer and observation identities through frozen contract prefixes. | Recompute calls are at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:186` and `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:200`; the contract emits `p030payload-v1` at `C:\tmp\P030_INTEGRATION_20260913\p030_market_data_contracts.py:198` and `p030obs-v1` at `C:\tmp\P030_INTEGRATION_20260913\p030_market_data_contracts.py:222`. |
| Collector bare hex ids are expected; bad prefixed ids are refused. | Bare-or-recomputed payload logic is at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:190`; bad prefixed observation refusal is at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:204`. The test is `C:\tmp\P030_INTEGRATION_20260913\check_p030_archive_exporter.py:239`. |
| Preserves all non-identity row fields and uses DATASET_ROW_FIELDS semantics. | Reidentified rows are returned in `DATASET_ROW_FIELDS` order at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:210`; contract field order is `C:\tmp\P030_INTEGRATION_20260913\p030_market_data_contracts.py:53`. Preservation is asserted in `C:\tmp\P030_INTEGRATION_20260913\check_p030_archive_exporter.py:144`. |
| Emits backup-facing canonical JSONL with sorted keys and LF. | Export serialization uses `sort_keys=True` at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:267`. The adapter canonical refusal it satisfies is `C:\tmp\P030_INTEGRATION_20260913\p030_closed_partition_backup_adapter.py:208`. |
| Writes target with exclusive create and re-reads exact bytes. | Target `xb` open is `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:278`; re-read verification is `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:286`. The byte-identity refusal test is `C:\tmp\P030_INTEGRATION_20260913\check_p030_archive_exporter.py:198`. |
| Computes dataset_content_hash over exported rows. | The call is `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:275`; the contract implementation starts at `C:\tmp\P030_INTEGRATION_20260913\p030_market_data_contracts.py:334`. |
| Writes `<target>.p030export.json` receipt with source/export hashes and identity flag. | Receipt construction starts at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:294`; receipt exclusive write is `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:316`. Receipt assertions are `C:\tmp\P030_INTEGRATION_20260913\check_p030_archive_exporter.py:100`. |
| D-13 RED raw collector partition and GREEN exported partition are executable. | Raw capture attempt starts at `C:\tmp\P030_INTEGRATION_20260913\check_p030_archive_exporter.py:68`; exported capture starts at `C:\tmp\P030_INTEGRATION_20260913\check_p030_archive_exporter.py:86`; printed messages are `C:\tmp\P030_INTEGRATION_20260913\check_p030_archive_exporter.py:97`. |

## Receipt Schema

`C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:36` defines `ExportReceipt`. The persisted receipt keys are: `schema`, `source_path`, `source_sha256`, `source_record_count`, `exporter_sha256`, `exported_sha256`, `exported_record_count`, `dataset_content_hash`, `exported_at_utc`, `identity_recomputed`. The schema literal is `p030.archive_export/v1` at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:294`.

## Refusal Codes

`ExportRefused` carries `.code` at `C:\tmp\P030_INTEGRATION_20260913\p030_archive_exporter.py:27`. Implemented codes: `invalid_timestamp`, `source_outside_root`, `source_unreadable`, `short_read`, `empty_partition`, `source_line_invalid`, `source_line_noncanonical`, `source_fields_mismatch`, `contract_refused`, `identity_mismatch`, `mixed_dataset_descriptor`, `target_exists`, `receipt_exists`, `target_unwritable`, `target_verify_failed`, `receipt_unwritable`.

## D-13 RED -> GREEN Pair

```text
test output: D-13 RED RAW REFUSAL: prefix record is not canonical JSONL
test output: D-13 GREEN EXPORTED CAPTURE: PASS
```

The RED message is one of the exact adapter refusals at `C:\tmp\P030_INTEGRATION_20260913\p030_closed_partition_backup_adapter.py:208` and `C:\tmp\P030_INTEGRATION_20260913\p030_closed_partition_backup_adapter.py:213`.

## Collector Untouched Proof

```text
$ git -c safe.directory=* diff -- market_data_collector.py
(no output)
```

```text
$ git -c safe.directory=* diff --stat
(no tracked diff output before staging; new files were untracked at that point)
```

## Verbatim Check Outputs

### `python check_p030_archive_exporter.py`

```text
test_empty_partition_refusal (__main__.ArchiveExporterTests.test_empty_partition_refusal) ... ok
test_exported_collector_fixture_is_accepted_by_stable_prefix_adapter (__main__.ArchiveExporterTests.test_exported_collector_fixture_is_accepted_by_stable_prefix_adapter) ... ok
test_malformed_line_refusal (__main__.ArchiveExporterTests.test_malformed_line_refusal) ... ok
test_prefixed_identity_mismatch_is_refused (__main__.ArchiveExporterTests.test_prefixed_identity_mismatch_is_refused) ... ok
test_receipt_fields_hashes_and_identity_rewrite_are_correct (__main__.ArchiveExporterTests.test_receipt_fields_hashes_and_identity_rewrite_are_correct) ... ok
test_target_exists_refusal (__main__.ArchiveExporterTests.test_target_exists_refusal) ... ok
test_target_reread_byte_identity_refusal (__main__.ArchiveExporterTests.test_target_reread_byte_identity_refusal) ... ok
test_two_exports_are_byte_identical (__main__.ArchiveExporterTests.test_two_exports_are_byte_identical) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.065s

OK
D-13 RED RAW REFUSAL: prefix record is not canonical JSONL
D-13 GREEN EXPORTED CAPTURE: PASS
```

### `python check_market_data_collector.py`

```text
INGEST REPLAY/GAP ATOMICITY (fixture transport): PASS
RESTART REPLAY SEEDS LIVE CURSOR: PASS
RESTART PERSISTED LATEST CURSOR: PASS
RESTART PERSISTED GAP REFUSED: PASS
RESTART PERSISTED ORDER (reverse 0,1,0 + duplicate 0,1,1) REFUSED: PASS
RESTART PERSISTED SORTING COUNTEREXAMPLE REFUSED: PASS
PERSISTED WS_LIVE INTERVAL IDENTITY (mismatching/unsupported) REFUSED: PASS
FIRST FORMING FRAME RECONSTRUCTS/VALIDATES HISTORY WITHOUT WRITE: PASS
PERSISTED HUGE TIMESTAMP GAP DIAGNOSTIC FAILS CLOSED: PASS
PERSISTED HUGE TIMESTAMP PUBLIC INGEST (single/contiguous) REFUSED: PASS
PERSISTED WS_ONLY CONTINUITY (snapshots do not fill WS gap): PASS
PERSISTED TIMESTAMP TYPE FENCES (string/float/bool/null/missing): PASS
PERSISTED INTEGER OFF-GRID OPENS REFUSED: PASS
SYNTHETIC SAME-ID CONFLICT THROUGH INGEST: PASS
APPEND FAILURE LEAVES LIVE CURSOR RETRYABLE: PASS
COMPLETE PERSISTED RECORDS (21 fields, two bars): PASS
PERSISTED FENCE PROOF (open): OLD_FENCE_ACCEPTS_DEVIANT; NEW_FENCE_REJECTS_DEVIANT
REINTRODUCTION MUTANT (persisted open corrupted): DETECTED
PERSISTED FENCE PROOF (env_lineage_id): OLD_FENCE_ACCEPTS_DEVIANT; NEW_FENCE_REJECTS_DEVIANT
REINTRODUCTION MUTANT (persisted env_lineage_id corrupted): DETECTED
FOUR-INTERVAL ARCHIVE/GAP/ROLLOVER MATRIX: PASS
INTERVAL-STEP MUTANT (1h/4h swapped): DETECTED
GAP-REPORT CLI (gap + complete): PASS
OFFLINE COLLECTOR LIFECYCLE (success + wait error): PASS
LIFECYCLE MUTANT (close skipped after wait error): DETECTED
MODIFIED COPY (gap detection removed): DETECTED
CARRIED FENCE PROOF (forming bar): OLD_FENCE_ACCEPTS_DEVIANT; NEW_FENCE_REJECTS_DEVIANT
CARRIED FENCE PROOF (refusal): OLD_FENCE_ACCEPTS_DEVIANT; NEW_FENCE_REJECTS_DEVIANT
REINTRODUCTION MUTANT (packet interpretation): DETECTED
REINTRODUCTION MUTANT (packet interpretation (static boundary)): DETECTED
REINTRODUCTION MUTANT (durable gap event): DETECTED
REINTRODUCTION MUTANT (concrete SDK import): DETECTED
REINTRODUCTION MUTANT (forming bar written): DETECTED
REINTRODUCTION MUTANT (append before gap): DETECTED
REINTRODUCTION MUTANT (replay does not seed cursor): DETECTED
REINTRODUCTION MUTANT (restart does not rehydrate cursor): DETECTED
REINTRODUCTION MUTANT (persisted gap validation removed): DETECTED
REINTRODUCTION MUTANT (persisted order sorted): DETECTED
REINTRODUCTION MUTANT (persisted interval filtered): DETECTED
REINTRODUCTION MUTANT (forming history not reconstructed): DETECTED
REINTRODUCTION MUTANT (persisted timestamp diagnostic leaked): DETECTED
REINTRODUCTION MUTANT (persisted timestamp representability removed): DETECTED
REINTRODUCTION MUTANT (persisted WS-only filter removed): DETECTED
REINTRODUCTION MUTANT (persisted timestamp coerced): DETECTED
REINTRODUCTION MUTANT (persisted grid validation removed): DETECTED
REINTRODUCTION MUTANT (eth_account import): DETECTED
REINTRODUCTION MUTANT (os.environ read): DETECTED
REINTRODUCTION MUTANT (order call): DETECTED
NETWORK ATTEMPTS: 0
MARKET DATA COLLECTOR CHECK: PASS
```

### `python check_p030_market_data_contracts.py`

```text
PAYLOAD MUTANTS (omitted/reordered member): DETECTED
MAPPING KEY/SOURCE/TRACK/PROXY REFUSALS: PASS
OBSERVATION/CORRECTION GOLDENS: PASS
SECOND INITIAL GUARD MUTATION: DETECTED
CORRECTION GENERATOR MUTATION: DETECTED
CORRECTION MUTANT (missing_predecessor): DETECTED
CORRECTION MUTANT (cross_slot): DETECTED
CORRECTION MUTANT (fork): DETECTED
CORRECTION GRAPH CYCLE GUARD MUTATION: DETECTED
EVENT PRODUCER ALLOWLIST MUTATION: DETECTED
EXACT SCALAR/CARRIER GUARD MUTANTS: DETECTED
EXACT OBSERVATION LIST SNAPSHOT MUTANT: DETECTED
EVENT MEMBER/DEPLOYMENT HASH REFUSALS: PASS
EVENT MUTANT (sorted correction ids): DETECTED
NINE EVENT FAMILY GOLDENS: PASS
DATASET OBSERVATION ID EXACT-TYPE GUARD: LOAD-BEARING
DATASET GENERATOR MUTATION: DETECTED
DATASET MUTANT (input-order hash): DETECTED
DATASET PAYLOAD/SLOT/DESCRIPTOR MUTANTS: DETECTED
DATASET IDENTITY GOLDEN/PERMUTATION: PASS
EXACT PROVENANCE PARTITIONS SNAPSHOT MUTANT: DETECTED
PRODUCER/TRACK/PROXY MAPPING MUTANTS: DETECTED
PROVENANCE CANONICAL RELATIVE POSIX PATH REFUSALS: PASS
PROVENANCE MUTANT (path): DETECTED
PROVENANCE MUTANT (size_bytes): DETECTED
PROVENANCE MUTANT (partition_state): DETECTED
PROVENANCE MUTANT (high_water_bytes): DETECTED
PROVENANCE MUTANT (file_sha256): DETECTED
PROVENANCE MUTANT (dataset_content_hash): DETECTED
IDENTITY MUTANT (omitted predecessor): DETECTED
EVENT MUTANT (four-family allowlist): DETECTED
PROVENANCE MUTANT (file-hashes only): DETECTED
EVENT DETAIL COLLISION/TYPE MUTANTS: DETECTED
TYPE/CANONICALIZATION REFUSALS: PASS
NETWORK ATTEMPTS: 0
P030 MARKET DATA CONTRACTS CHECK: PASS
```

### `python check_p030_closed_partition_backup_adapter.py`

```text
test_backup_binds_bytes_from_the_same_read_that_validated_them (__main__.StablePrefixBackupAdapterTests.test_backup_binds_bytes_from_the_same_read_that_validated_them) ... ok
test_backup_consumes_bound_config_when_original_is_swapped (__main__.StablePrefixBackupAdapterTests.test_backup_consumes_bound_config_when_original_is_swapped) ... ok
test_backup_rechecks_source_and_snapshot_after_p026_success (__main__.StablePrefixBackupAdapterTests.test_backup_rechecks_source_and_snapshot_after_p026_success) ... ok
test_backup_refuses_archived_pair_that_differs_from_prevalidated_staging (__main__.StablePrefixBackupAdapterTests.test_backup_refuses_archived_pair_that_differs_from_prevalidated_staging) ... ok
test_backup_refuses_coordinated_valid_staging_replacement_after_p026 (__main__.StablePrefixBackupAdapterTests.test_backup_refuses_coordinated_valid_staging_replacement_after_p026) ... ok
test_backup_refuses_prefix_mutation_or_truncation_before_p026 (__main__.StablePrefixBackupAdapterTests.test_backup_refuses_prefix_mutation_or_truncation_before_p026) ... ok
test_capture_and_prebackup_refuse_real_junction_ancestor (__main__.StablePrefixBackupAdapterTests.test_capture_and_prebackup_refuse_real_junction_ancestor) ... ok
test_capture_binds_exact_canonical_complete_prefix_and_allows_later_append (__main__.StablePrefixBackupAdapterTests.test_capture_binds_exact_canonical_complete_prefix_and_allows_later_append) ... ok
test_capture_refuses_caller_supplied_symlink_before_resolution (__main__.StablePrefixBackupAdapterTests.test_capture_refuses_caller_supplied_symlink_before_resolution) ... ok
test_capture_refuses_intermediate_symlink_or_junction_component (__main__.StablePrefixBackupAdapterTests.test_capture_refuses_intermediate_symlink_or_junction_component) ... ok
test_capture_refuses_noncontract_dataset_and_observation_identities (__main__.StablePrefixBackupAdapterTests.test_capture_refuses_noncontract_dataset_and_observation_identities) ... ok
test_capture_refuses_nonfinite_json_constants (__main__.StablePrefixBackupAdapterTests.test_capture_refuses_nonfinite_json_constants) ... ok
test_capture_refuses_partial_line_and_noncanonical_jsonl (__main__.StablePrefixBackupAdapterTests.test_capture_refuses_partial_line_and_noncanonical_jsonl) ... ok
test_committed_configuration_is_explicitly_non_runnable (__main__.StablePrefixBackupAdapterTests.test_committed_configuration_is_explicitly_non_runnable) ... ok
test_config_and_receipt_refuse_nested_overflowed_numbers_before_p026 (__main__.StablePrefixBackupAdapterTests.test_config_and_receipt_refuse_nested_overflowed_numbers_before_p026) ... ok
test_config_refuses_duplicate_keys_and_nonfinite_json_before_p026 (__main__.StablePrefixBackupAdapterTests.test_config_refuses_duplicate_keys_and_nonfinite_json_before_p026) ... ok
test_file_only_restored_inventory_reversion_is_detected (__main__.StablePrefixBackupAdapterTests.test_file_only_restored_inventory_reversion_is_detected) ... ok
test_intruder_after_check_only_blocks_actual_restore (__main__.StablePrefixBackupAdapterTests.test_intruder_after_check_only_blocks_actual_restore) ... ok
test_intruder_after_restore_config_verification_blocks_actual_restore (__main__.StablePrefixBackupAdapterTests.test_intruder_after_restore_config_verification_blocks_actual_restore) ... ok
test_isolated_config_redirect_after_check_never_reaches_restore (__main__.StablePrefixBackupAdapterTests.test_isolated_config_redirect_after_check_never_reaches_restore) ... ok
test_manifest_is_rechecked_between_check_only_and_restore (__main__.StablePrefixBackupAdapterTests.test_manifest_is_rechecked_between_check_only_and_restore) ... ok
test_manifest_refuses_boolean_size_and_byte_totals_before_p026 (__main__.StablePrefixBackupAdapterTests.test_manifest_refuses_boolean_size_and_byte_totals_before_p026) ... ok
test_manifest_refuses_duplicate_keys_and_nonfinite_json_before_p026 (__main__.StablePrefixBackupAdapterTests.test_manifest_refuses_duplicate_keys_and_nonfinite_json_before_p026) ... ok
test_manifest_refuses_inconsistent_byte_total_before_p026 (__main__.StablePrefixBackupAdapterTests.test_manifest_refuses_inconsistent_byte_total_before_p026) ... ok
test_manifest_refuses_overflowed_size_and_byte_totals_before_p026 (__main__.StablePrefixBackupAdapterTests.test_manifest_refuses_overflowed_size_and_byte_totals_before_p026) ... ok
test_manifest_swap_immediately_before_restore_never_yields_receipt (__main__.StablePrefixBackupAdapterTests.test_manifest_swap_immediately_before_restore_never_yields_receipt) ... ok
test_partial_run_that_p026_check_only_accepts_never_reaches_restore (__main__.StablePrefixBackupAdapterTests.test_partial_run_that_p026_check_only_accepts_never_reaches_restore) ... ok
test_post_backup_verification_refuses_replaced_intermediate_component (__main__.StablePrefixBackupAdapterTests.test_post_backup_verification_refuses_replaced_intermediate_component) ... ok
test_receipt_always_refuses_absolute_or_noncanonical_source_path (__main__.StablePrefixBackupAdapterTests.test_receipt_always_refuses_absolute_or_noncanonical_source_path) ... ok
test_receipt_refuses_duplicate_keys_and_nonfinite_json (__main__.StablePrefixBackupAdapterTests.test_receipt_refuses_duplicate_keys_and_nonfinite_json) ... ok
test_receipt_strictly_validates_types_identities_and_lower_hex (__main__.StablePrefixBackupAdapterTests.test_receipt_strictly_validates_types_identities_and_lower_hex) ... ok
test_restore_checks_first_and_produces_verified_receipt (__main__.StablePrefixBackupAdapterTests.test_restore_checks_first_and_produces_verified_receipt) ... ok
test_restore_consumes_isolated_validated_archive_snapshot (__main__.StablePrefixBackupAdapterTests.test_restore_consumes_isolated_validated_archive_snapshot) ... ok
test_restore_refuses_nonempty_target_before_p026 (__main__.StablePrefixBackupAdapterTests.test_restore_refuses_nonempty_target_before_p026) ... ok
test_restore_refuses_post_p026_empty_target_directory (__main__.StablePrefixBackupAdapterTests.test_restore_refuses_post_p026_empty_target_directory) ... ok
test_restore_refuses_post_p026_extra_target_member (__main__.StablePrefixBackupAdapterTests.test_restore_refuses_post_p026_extra_target_member) ... ok
test_restore_refuses_post_p026_target_substitution (__main__.StablePrefixBackupAdapterTests.test_restore_refuses_post_p026_target_substitution) ... ok
test_restore_refuses_rehashed_archive_with_dot_source_path (__main__.StablePrefixBackupAdapterTests.test_restore_refuses_rehashed_archive_with_dot_source_path) ... ok
test_restore_requires_exact_run_envelope_store_and_members (__main__.StablePrefixBackupAdapterTests.test_restore_requires_exact_run_envelope_store_and_members) ... ok
test_run_envelope_guards_are_independently_load_bearing (__main__.StablePrefixBackupAdapterTests.test_run_envelope_guards_are_independently_load_bearing) ... ok
test_shared_archive_reversion_mutant_is_detected (__main__.StablePrefixBackupAdapterTests.test_shared_archive_reversion_mutant_is_detected) ... ok
test_speculative_replay_opening_api_is_absent (__main__.StablePrefixBackupAdapterTests.test_speculative_replay_opening_api_is_absent) ... ok
test_tampered_backup_never_reaches_p026_restore (__main__.StablePrefixBackupAdapterTests.test_tampered_backup_never_reaches_p026_restore) ... ok
test_validate_then_reopen_reversion_is_detected (__main__.StablePrefixBackupAdapterTests.test_validate_then_reopen_reversion_is_detected) ... ok

----------------------------------------------------------------------
Ran 44 tests in 3.015s

OK
{"mode": "backup", "run_id": "opsa-20260914T154738.912Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp7qud17iw\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:38Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=495517a1abc0e322… readback=match
OK    fixture-p030-archive/live.jsonl size=108 sha256=d83245989ffd56ef… readback=match
{"run_id": "opsa-20260914T154738.912Z", "status": "ok", "files": 2, "bytes": 633, "errors": 0, "finished_at": "2026-09-14T15:47:38Z"}
{"mode": "backup", "run_id": "opsa-20260914T154738.947Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpltqmrvz5\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:38Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154738.947Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:38Z"}
{"mode": "backup", "run_id": "opsa-20260914T154738.986Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpdym_s5j2\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:38Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154738.986Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:38Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.019Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp511umwrw\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.019Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.049Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmphptbru0j\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=495517a1abc0e322… readback=match
OK    fixture-p030-archive/live.jsonl size=108 sha256=d83245989ffd56ef… readback=match
{"run_id": "opsa-20260914T154739.049Z", "status": "ok", "files": 2, "bytes": 633, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.086Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpb387cfpz\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.086Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.195Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp7l3m3zr5\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.195Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.333Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpurmkcn2u\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.333Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154739.333Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-yvsb20sp\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154739.333Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "restore", "run_id": "opsa-20260914T154739.333Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-yvsb20sp\\backup\\manifest.jsonl", "target": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpurmkcn2u\\restore-target", "records_selected": 2, "manifest_malformed_lines": 0}
RESTORED fixture-p030-archive/_P030_STABLE_PREFIX.json sha256=7357ae914a4fffee…
RESTORED fixture-p030-archive/live.jsonl sha256=5ece6f43917414e8…
{"mode": "restore", "run_id": "opsa-20260914T154739.333Z", "status": "ok", "verified_against_manifest": 2, "restored": 2, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.419Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpkd_2dopm\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.419Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154739.419Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-z240jdgz\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154739.419Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.487Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpn5l5xm4g\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.487Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154739.487Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-hqi581i8\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154739.487Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.562Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp2csbcsd_\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.562Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154739.562Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-ozi7x0ul\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154739.562Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.634Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpj894cmpd\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.634Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154739.634Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-421xdhe1\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154739.634Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.705Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpbsm69o9v\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.705Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154739.705Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-vgdqdhz9\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154739.705Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.776Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpsglqh1vo\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.776Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.839Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp6ahg8myu\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.839Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.898Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp4xs44ueo\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.898Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154739.955Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpofkqt65x\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:39Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154739.955Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:39Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.006Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpklmihany\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.006Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.058Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpralm9gvu\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.058Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.112Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpm0cvb1qm\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.112Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.163Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpew8fhnhb\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.163Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154740.163Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-5bsc4xmw\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154740.163Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "restore", "run_id": "opsa-20260914T154740.163Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-5bsc4xmw\\backup\\manifest.jsonl", "target": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpew8fhnhb\\restore-target", "records_selected": 2, "manifest_malformed_lines": 0}
RESTORED fixture-p030-archive/_P030_STABLE_PREFIX.json sha256=7357ae914a4fffee…
RESTORED fixture-p030-archive/live.jsonl sha256=5ece6f43917414e8…
{"mode": "restore", "run_id": "opsa-20260914T154740.163Z", "status": "ok", "verified_against_manifest": 2, "restored": 2, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.261Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp6zz8udk6\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.261Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154740.261Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp6zz8udk6\\backups\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154740.261Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.321Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp_kzid27w\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.321Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.519Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpbe1cnjao\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.519Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154740.519Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-g_8u81ot\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154740.519Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "restore", "run_id": "opsa-20260914T154740.519Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-g_8u81ot\\backup\\manifest.jsonl", "target": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpbe1cnjao\\restore-target", "records_selected": 2, "manifest_malformed_lines": 0}
RESTORED fixture-p030-archive/_P030_STABLE_PREFIX.json sha256=7357ae914a4fffee…
RESTORED fixture-p030-archive/live.jsonl sha256=5ece6f43917414e8…
{"mode": "restore", "run_id": "opsa-20260914T154740.519Z", "status": "ok", "verified_against_manifest": 2, "restored": 2, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.620Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpzmq5d5c5\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.620Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154740.620Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-ux_lcygi\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154740.620Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "restore", "run_id": "opsa-20260914T154740.620Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-ux_lcygi\\backup\\manifest.jsonl", "target": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpzmq5d5c5\\restore-target", "records_selected": 2, "manifest_malformed_lines": 0}
RESTORED fixture-p030-archive/_P030_STABLE_PREFIX.json sha256=7357ae914a4fffee…
RESTORED fixture-p030-archive/live.jsonl sha256=5ece6f43917414e8…
{"mode": "restore", "run_id": "opsa-20260914T154740.620Z", "status": "ok", "verified_against_manifest": 2, "restored": 2, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.757Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpc3zarhcw\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.757Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.803Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpsd6epxnl\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.803Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154740.803Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-npqlnlrb\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154740.803Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "restore", "run_id": "opsa-20260914T154740.803Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-npqlnlrb\\backup\\manifest.jsonl", "target": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpsd6epxnl\\restore-target", "records_selected": 2, "manifest_malformed_lines": 0}
RESTORED fixture-p030-archive/_P030_STABLE_PREFIX.json sha256=7357ae914a4fffee…
RESTORED fixture-p030-archive/live.jsonl sha256=5ece6f43917414e8…
{"mode": "restore", "run_id": "opsa-20260914T154740.803Z", "status": "ok", "verified_against_manifest": 2, "restored": 2, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154740.895Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmps35m9qq7\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:40Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154740.895Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154740.895Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-84ozbunk\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154740.895Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "restore", "run_id": "opsa-20260914T154740.895Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-84ozbunk\\backup\\manifest.jsonl", "target": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmps35m9qq7\\restore-target", "records_selected": 2, "manifest_malformed_lines": 0}
RESTORED fixture-p030-archive/_P030_STABLE_PREFIX.json sha256=7357ae914a4fffee…
RESTORED fixture-p030-archive/live.jsonl sha256=5ece6f43917414e8…
{"mode": "restore", "run_id": "opsa-20260914T154740.895Z", "status": "ok", "verified_against_manifest": 2, "restored": 2, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:40Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.010Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp9dc3qxk_\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.010Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154741.010Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-qmyg5gd2\\backup\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154741.010Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "restore", "run_id": "opsa-20260914T154741.010Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\p030-isolated-restore-qmyg5gd2\\backup\\manifest.jsonl", "target": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp9dc3qxk_\\restore-target", "records_selected": 2, "manifest_malformed_lines": 0}
RESTORED fixture-p030-archive/_P030_STABLE_PREFIX.json sha256=7357ae914a4fffee…
RESTORED fixture-p030-archive/live.jsonl sha256=5ece6f43917414e8…
{"mode": "restore", "run_id": "opsa-20260914T154741.010Z", "status": "ok", "verified_against_manifest": 2, "restored": 2, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.106Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpux5bq0re\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.106Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.172Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp123eg2m6\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.172Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.228Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp0zri6kpe\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.228Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.284Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmprnc59hrt\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.284Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.338Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpzluwudpr\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.338Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.391Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpg0rgjqpk\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.391Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.442Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp_q6603a0\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.442Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.503Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpzntc2n1g\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.503Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.580Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmplad5msnx\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.580Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.655Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmpwxsi9228\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.655Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.739Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp4_4ma1er\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.739Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "check-only", "run_id": "opsa-20260914T154741.739Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp4_4ma1er\\backups\\manifest.jsonl", "target": null, "records_selected": 2, "manifest_malformed_lines": 0}
VERIFIED fixture-p030-archive/_P030_STABLE_PREFIX.json
VERIFIED fixture-p030-archive/live.jsonl
{"mode": "check-only", "run_id": "opsa-20260914T154741.739Z", "status": "ok", "verified_against_manifest": 2, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "restore", "run_id": "opsa-20260914T154741.739Z", "manifest": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp4_4ma1er\\backups\\manifest.jsonl", "target": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp4_4ma1er\\restore-target", "records_selected": 2, "manifest_malformed_lines": 0}
RESTORED fixture-p030-archive/_P030_STABLE_PREFIX.json sha256=495517a1abc0e322…
RESTORED fixture-p030-archive/live.jsonl sha256=d83245989ffd56ef…
{"mode": "restore", "run_id": "opsa-20260914T154741.739Z", "status": "ok", "verified_against_manifest": 2, "restored": 2, "overwritten": 0, "dirs_recreated": 0, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.834Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmp3al_p3l0\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=7357ae914a4fffee… readback=match
OK    fixture-p030-archive/live.jsonl size=216 sha256=5ece6f43917414e8… readback=match
{"run_id": "opsa-20260914T154741.834Z", "status": "ok", "files": 2, "bytes": 741, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
{"mode": "backup", "run_id": "opsa-20260914T154741.885Z", "backup_root": "C:\\tmp\\CLAUDE_P0_RUN_20260913\\laneO9EXP_build\\tmp\\tmptxn80ugg\\backups", "stores": ["fixture-p030-archive"], "started_at": "2026-09-14T15:47:41Z"}
OK    fixture-p030-archive/_P030_STABLE_PREFIX.json size=525 sha256=495517a1abc0e322… readback=match
OK    fixture-p030-archive/live.jsonl size=108 sha256=d83245989ffd56ef… readback=match
{"run_id": "opsa-20260914T154741.885Z", "status": "ok", "files": 2, "bytes": 633, "errors": 0, "finished_at": "2026-09-14T15:47:41Z"}
```

## Git Commit Status

BLOCKED. The implementation and checks are written, but the required local commit could not be created because Git metadata for this worktree resolves outside the writable sandbox.

```text
$ git -c safe.directory=* add -- p030_archive_exporter.py check_p030_archive_exporter.py
fatal: Unable to create 'C:/LAB/Tradingview_LAB_CLEAN/.git/worktrees/P030_INTEGRATION_20260913/index.lock': Permission denied
```

```text
$ git -c safe.directory=* rev-parse HEAD
f42fd5400b2c2ecb805644d406999cb55c8178c8
```

```text
$ git -c safe.directory=* status --short
?? TASK_O9EXP.md
?? check_p030_archive_exporter.py
?? p030_archive_exporter.py
warning: unable to access 'C:\Users\BarışSemaay/.config/git/ignore': Permission denied
warning: unable to access 'C:\Users\BarışSemaay/.config/git/ignore': Permission denied
```
## NOT VERIFIED

- Not reviewed by an independent reviewer in this lane.
- No real archive was read or exported; all archive data was deterministic fixture data.
- No production, host, credential, network, schedule, backup root, push, PR, merge, or acceptance action was performed.
- Nothing in this implementation accepts P026/P030 overall; acceptance edges are unmoved.
- The collector archive itself still needs the separate P026 second-location policy path described outside this Shape-B exporter.

## SHA256SUMS

See `C:\tmp\CLAUDE_P0_RUN_20260913\laneO9EXP_build\SHA256SUMS.txt`.