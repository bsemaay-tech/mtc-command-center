# WP-P0-30 Shape-B archive exporter — independent Sol T0 review

Reviewer: `gpt-5.6-sol`, `xhigh`, second flagship, independent of the Opus report. I did not read any `*OPUS_T*_REPORT.md` or Lead adjudication. The reviewed worktree was read-only; all modified copies were under `C:\tmp\SOL_P030_SCRATCH\b4df1413_sol_review`.

## Verified identities

- COMPUTED HEAD: `b4df14139501e4224e6fcfa96f4226ab90c03cbe`.
- The Subject section's older `d426e79f...` pin is superseded by the final 2026-09-19 addendum, which pins `b4df1413`.
- `p030_archive_exporter.py`: checkout-byte SHA-256 `86a508572479e37034b0cb97f727a07815989e55161d788a6f76e151393cdc6d`; LF-normalised SHA-256 `89989f4e07ed8d8e7ec54e5f6b03f6bec0d4a49a644f53effb2bb310533a4663`.
- `check_p030_archive_exporter.py`: checkout-byte SHA-256 `7eb48af6fe5fe6304a2ed537d16c8e59c939cd74613f426da50370f255058f71`; LF-normalised SHA-256 `8d6fcfd4e407ae04e212caa67383693e4d120874198f7763bef8254cef6ad00e`.
- `b4df1413` has parent `d426e79f` and changes exactly the four disclosed files: `p030_archive_exporter.py`, `check_p030_archive_exporter.py`, `p030_closed_partition_backup_adapter.py`, and `check_p030_closed_partition_backup_adapter.py`.
- `153edee9` has parent `daf6a43b` and changes exactly `p030_archive_exporter.py` and `check_p030_archive_exporter.py`.
- `git diff f42fd540 153edee9 -- market_data_collector.py` and `git diff 153edee9 b4df1413 -- market_data_collector.py` both produced no output: the collector is untouched.

Identity command and exact output:

```text
cwd: C:\tmp\P030_INTEGRATION_20260913
command: git -c safe.directory=* -C C:\tmp\P030_INTEGRATION_20260913 rev-parse HEAD
b4df14139501e4224e6fcfa96f4226ab90c03cbe
```

## Shape-B conformance

| Shape-B promise | Current evidence | Result |
|---|---|---|
| Source partition is read once and is never mutated or re-read | `p030_archive_exporter.py:221-238` performs one binary open/read; the only call is at `:403`; all later source digest/count work uses `source_bytes` at `:405-430,474-475` | EQUAL |
| Re-identification uses frozen contracts, not home-grown IDs | imports at `p030_archive_exporter.py:16-26`; calls `producer_payload_hash`, `observation_id`, and `dataset_content_hash` at `:313-358,427-432`; domains are emitted by `p030_market_data_contracts.py:172-222,314-380` | EQUAL |
| Exact source row shape is enforced | `p030_archive_exporter.py:304-311` compares against `DATASET_ROW_FIELDS`; contract field set is `p030_market_data_contracts.py:53-58` | EQUAL |
| Duplicate keys, malformed JSON, non-finite values, and pathological nesting refuse before export | `p030_archive_exporter.py:101-122,241-301`; parser and recursive-walk guards are separate at `:249-280` | EQUAL |
| Output is sorted-key UTF-8 JSONL with one LF-terminated row per record | `p030_archive_exporter.py:414-426`; the real adapter independently recomputes sorted-key LF bytes at `p030_closed_partition_backup_adapter.py:192-223` | EQUAL |
| Target bytes are staged with exclusive create, flushed/fsynced, re-read, and compared before publication | `p030_archive_exporter.py:433-469`; target and receipt staging use `xb` at `:446,498` | EQUAL |
| Final-name publication does not clobber on this Windows subject | `_publish` uses `os.rename` on Windows at `p030_archive_exporter.py:79-94`; both target-side and receipt-side appeared-after-check tests pass | EQUAL |
| Final-name publication is atomic no-clobber on POSIX | `p030_archive_exporter.py:91-94` uses an exists-check followed by `os.replace`; the residual race can overwrite a destination that appears between them | DIFFERENT — known, disclosed residual; not exercised on this Windows host |
| Receipt is published before the consumable target; no refusal publishes a partial final target | `p030_archive_exporter.py:508-539`; ENOSPC, target verification, receipt write, receipt race, and target race checks all pass | EQUAL |
| Receipt binds source bytes, exported bytes, counts, dataset identity, timestamp, and exporter bytes | schema at `p030_archive_exporter.py:37-63`; construction at `:470-496`; `source_sha256`, `exported_sha256`, both counts, and `dataset_content_hash` are asserted by `check_p030_archive_exporter.py:176-240` | EQUAL |
| Timestamp rule matches the adapter: caller-supplied UTC `Z`, whole seconds | exporter `p030_archive_exporter.py:125-147`; adapter `p030_closed_partition_backup_adapter.py:142-150` | EQUAL |
| Source path rule matches the adapter: canonical relative POSIX spelling, no escapes/links, resolved containment | exporter `p030_archive_exporter.py:150-218`; adapter `p030_closed_partition_backup_adapter.py:153-190,235-270` | EQUAL |
| Adapter ID domains are met | adapter requires `p030ds-v1` and `p030obs-v1` at `p030_closed_partition_backup_adapter.py:47-49,224-232`; contracts emit/validate them at `p030_market_data_contracts.py:187-222,314-380` | EQUAL |
| Adapter has no unguarded JSON parse site after the nesting repair | `_decode_json_object` at `p030_closed_partition_backup_adapter.py:76-94`, `_decode_strict_jsonl` at `:105-131`, and `_prefix_facts` at `:192-232`; `rg` found no fourth `json.loads` site | EQUAL |
| Production exporter has no network or subprocess boundary and writes only the target family | imports at `p030_archive_exporter.py:3-26`; writes are target parent, staging target, staging receipt, receipt, and target at `:433-539`; no delete path exists | EQUAL |
| Publication prose matches the implementation | `p030_archive_exporter.py:69` says publication is “by os.replace only” and `:80` says the function does not replace an existing final, while `:89-94` uses `os.rename` on Windows and retains a POSIX overwrite race | DIFFERENT — NIT 2 |

The initial lane `REPORT.md` and `LEAD_NOTE.md` are honest snapshots of `daf6a43b`: their semantic claims (single read, contract re-identification, canonical output, receipt fields, D-13, collector untouched, fixture-only status) match the current bytes, but their line counts, test counts, and line citations are historical rather than current. The current repair record's claimed Python 3.12 depths, 29/46 test counts, and Ruff counts match my independent results.

## Refusal-code coverage

I derived the code set and committed-test string set from the Git blobs, rather than accepting the records:

- `daf6a43b`: 16 implemented codes; exact code assertions in tests for 5 (`empty_partition`, `identity_mismatch`, `source_line_invalid`, `target_exists`, `target_verify_failed`); 11 missing.
- The 11 missing at `daf6a43b` were `contract_refused`, `invalid_timestamp`, `mixed_dataset_descriptor`, `receipt_exists`, `receipt_unwritable`, `short_read`, `source_fields_mismatch`, `source_line_noncanonical`, `source_outside_root`, `source_unreadable`, and `target_unwritable`.
- `153edee9`: 16 implemented codes and 16/16 exact code strings in negative tests.
- `b4df1413`: still 16 implemented codes and 16/16 exact code strings in negative tests.

| Code | Trigger in current bytes | Negative test present? | My observed result |
|---|---|---|---|
| `invalid_timestamp` | non-string/non-`Z`/unparseable or sub-second `exported_at_utc`; `p030_archive_exporter.py:125-147` | Yes, `check_p030_archive_exporter.py:529-556` | PASS; `.500Z` returned this code, no target |
| `source_outside_root` | lexical or resolved escape, non-canonical/percent-escaped spelling, symlink/junction component; `p030_archive_exporter.py:150-218` | Yes, `:558-568,878-970` | PASS for outside-root, `..`, percent escape, and NTFS junction |
| `source_unreadable` | source stat/open/read `OSError`; `p030_archive_exporter.py:221-231` | Yes, `:570-575` | PASS |
| `short_read` | size/tell mismatch or missing terminal newline; `p030_archive_exporter.py:232-237` | Yes, `:577-602` | PASS for both arms |
| `empty_partition` | zero source bytes or no decoded rows; `p030_archive_exporter.py:234-235,411-412` | Yes, `:275-289` | PASS |
| `source_line_invalid` | malformed/duplicate/non-finite/deep JSON; `p030_archive_exporter.py:241-280` | Yes for malformed, overflow, NaN, and both nesting layers, `:259-273,496-527,604-616`; no committed duplicate-key input | PASS; reviewer probe also refused a duplicate key with this code, no target |
| `source_line_noncanonical` | decoded line differs from the compact source form; `p030_archive_exporter.py:281-300` | Yes, `:618-623` | PASS |
| `source_fields_mismatch` | missing/extra dataset-row fields; `p030_archive_exporter.py:304-311` | Yes, `:625-638` | PASS |
| `contract_refused` | row identity contract or whole-slice dataset contract refuses; `p030_archive_exporter.py:313-317,339-343,427-432` | Yes, `:640-681` | PASS for row and slice arms; no raw `ContractRefused` |
| `identity_mismatch` | stored prefixed identity disagrees, or stored identity is neither bare hex nor recomputed ID; `p030_archive_exporter.py:319-355` | Yes, `:342-367` | PASS |
| `mixed_dataset_descriptor` | venue/track/proxy differs across rows; `p030_archive_exporter.py:361-379` | Yes, `:683-696` | PASS |
| `target_exists` | final target, target/receipt staging partial, or appeared target exists; `p030_archive_exporter.py:395-396,438-451,524-533` | Yes, `:242-257,412-452,762-808` | PASS; foreign target preserved; second run after ENOSPC refused |
| `receipt_exists` | final/staging receipt or appeared receipt exists; `p030_archive_exporter.py:397-399,438-443,502-519` | Yes, `:453-494,698-712` | PASS; foreign receipt preserved, target absent |
| `target_unwritable` | staging target open/write/flush/fsync or final publish `OSError`; `p030_archive_exporter.py:444-457,526-539` | Yes, `:714-798,810-841` | PASS, including half-write then `OSError(28)` |
| `target_verify_failed` | staging target cannot be read or differs from intended bytes; `p030_archive_exporter.py:458-468` | Yes for byte mismatch, `:291-323` | PASS; final target and receipt absent, staging remains |
| `receipt_unwritable` | staging receipt open/write/flush/fsync or publish `OSError`; `p030_archive_exporter.py:497-507,512-523` | Yes, `:714-760` | PASS; final target and receipt absent, target staging remains |

### K-01 through K-05

1. **K-01 CONFIRMED fixed.** Before: `1e999` could leak raw `ValueError`. After: `p030_archive_exporter.py:264-280` maps overflow and nested non-finite values to `ExportRefused("source_line_invalid")`. Reviewer probes: `1e999` -> `source_line_invalid` / `target_exists=False`; `NaN` -> the same code / `target_exists=False`. Neither produced an exported row.
2. **K-02 CONFIRMED fixed.** Before: row/slice `ContractRefused` could escape. After: wrappers at `p030_archive_exporter.py:314-317,340-343,427-432`. Reviewer non-decimal row -> `contract_refused`, target absent; committed duplicate/slice-window tests pass.
3. **K-03 CONFIRMED fixed.** Before: sub-second timestamps were accepted. After: `p030_archive_exporter.py:143-147`; reviewer `.500Z` probe -> `invalid_timestamp`, target absent.
4. **K-04 CONFIRMED fixed.** Counts independently reproduced as 5/16 covered at `daf6a43b` and 16/16 at `153edee9` and current HEAD.
5. **K-05 CONFIRMED as a historical citation correction.** `DISPOSITION_O9FIX.md` correctly identifies the original off-by-one/wrong-test citations and explicitly leaves the historical `REPORT.md` unchanged. Later reflow/repairs moved the current return to `p030_archive_exporter.py:358` and current preservation assertions to `check_p030_archive_exporter.py:228-240`; that expected line drift is not a code defect.

## D-13 evidence

The test calls the real `capture_stable_prefix` imported at `check_p030_archive_exporter.py:17`; the RED call is at `:135-152`, the GREEN call at `:154-172`, and both use actual exporter output/receipt data.

```text
cwd: C:\tmp\P030_INTEGRATION_20260913
interpreter: C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe (Python 3.12.12)
command: <pinned-python> check_p030_archive_exporter.py ArchiveExporterRefusalCodeTests.test_mid_write_failure_publishes_nothing_under_the_target_name ArchiveExporterRefusalCodeTests.test_target_and_receipt_unwritable_refusals ArchiveExporterTests.test_target_reread_byte_identity_refusal ArchiveExporterRefusalCodeTests.test_dotdot_traversal_is_refused_even_when_lexically_under_root ArchiveExporterRefusalCodeTests.test_junction_component_is_refused_like_the_adapter ArchiveExporterRefusalCodeTests.test_publication_never_replaces_a_target_that_appeared_after_the_check ArchiveExporterRefusalCodeTests.test_publication_never_replaces_a_receipt_that_appeared_after_the_check ArchiveExporterTests.test_exported_collector_fixture_is_accepted_by_stable_prefix_adapter

D-13 RED RAW REFUSAL: prefix record is not canonical JSONL
D-13 GREEN EXPORTED CAPTURE: PASS
test_mid_write_failure_publishes_nothing_under_the_target_name (...) ... ok
test_target_and_receipt_unwritable_refusals (...) ... ok
test_target_reread_byte_identity_refusal (...) ... ok
test_dotdot_traversal_is_refused_even_when_lexically_under_root (...) ... ok
test_junction_component_is_refused_like_the_adapter (...) ... ok
test_publication_never_replaces_a_target_that_appeared_after_the_check (...) ... ok
test_publication_never_replaces_a_receipt_that_appeared_after_the_check (...) ... ok
test_exported_collector_fixture_is_accepted_by_stable_prefix_adapter (...) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.161s

OK
```

Reviewer mutation of the published export before adapter capture:

```text
D-13 mutated exported bytes: adapter_refusal=prefix record is not canonical JSONL
```

The N3 binding assertion is independently load-bearing. Modified values: `receipt.exported_sha256 = sha256(b"other bytes")` and the two D-13 hash equality assertions removed. Observed: the D-13 test returned `OK` and printed GREEN despite the false receipt hash; `test_receipt_fields_hashes_and_identity_rewrite_are_correct` still failed on the receipt-vs-published-bytes comparison.

## Repair and NIT-slice RED/GREEN evidence

Direct `nesting_arms()` results on the pinned interpreter were `(("walk", 1060), ("parser", 3062))` in both checkers. In the deeper unittest call frame, failing mutant subtests reported walk depth `1049` and parser depth `3044`. The parser predicate and “anything raised” predicate were monotone across the exponential/binary searches used here; the 64-frame margin landed each current arm on its named layer, and the full checkers completed quickly. The skip is explicitly named by layer and only applies when that layer never raises below the ceiling.

| Modified scratch copy | Before value | After value | Observed result on pinned 3.12.12 |
|---|---|---|---|
| Exporter parser clause | catches `RecursionError` at `p030_archive_exporter.py:249-259` | `RecursionError` removed from tuple | matching parser subtest ERROR, raw `RecursionError`, exit 1 |
| Exporter walk guard | catches at `p030_archive_exporter.py:274-280` | guard deleted | matching walk subtest ERROR, raw `RecursionError`, exit 1 |
| Adapter `_prefix_facts` parser clause | catches at `p030_closed_partition_backup_adapter.py:197-204` | parser clause removed | capture parser subtest ERROR, exit 1 |
| Adapter `_prefix_facts` walk guard | catches at `:207-211` | walk guard removed | capture walk subtest ERROR, exit 1 |
| Adapter `_decode_strict_jsonl` parser clause | catches at `:114-122` | parser clause removed | manifest parser subtest ERROR, exit 1 |
| Adapter `_decode_strict_jsonl` walk guard | catches at `:125-129` | walk guard removed | manifest walk subtest ERROR, exit 1 |
| Adapter `_decode_json_object` parser clause | catches at `:77-86` | parser clause removed | config and receipt parser subtests both ERROR, exit 1 |
| Adapter `_decode_json_object` walk guard | catches at `:89-93` | walk guard removed | config and receipt walk subtests both ERROR, exit 1 |
| Receipt appeared-after-check arm | `FileExistsError` -> `receipt_exists` at `p030_archive_exporter.py:512-519` | dedicated clause deleted | F-3 test FAIL: `receipt_unwritable`/“could not be published” instead of `receipt_exists`, exit 1 |
| Windows publication | `os.rename` at `p030_archive_exporter.py:89-90` | `os.replace` | target race test FAIL: no `ExportRefused`; foreign target overwritten, exit 1 |
| D-13 receipt binding | equality at `check_p030_archive_exporter.py:167-172` | equality deleted and receipt hash changed | D-13 falsely passed; receipt-field test failed, proving separate coverage |
| F8 non-ASCII config anchor | `json.dumps(..., ensure_ascii=False)` at `check_p030_closed_partition_backup_adapter.py:993-1000` | default ASCII escaping | non-ASCII TEMP subtest FAIL `0 != 1`, exit 1 |

F-4 is closed: both exporter messages are reachable on the pinned interpreter and deletion of either guard errors only its named arm. F-5's discussion of `os.link` now names its real permanent-hard-link and cross-filesystem costs at `p030_archive_exporter.py:85-88`; however, the docstring headline and the older `os.replace only` comment still overstate the cross-platform implementation (NIT 2). No fourth adapter JSON parse site remains.

The Windows target and receipt races are closed on this subject. The POSIX residual check/replace window is disclosed in the body of `_publish`; it is not closed. That disclosure is substantively honest, while the absolute first sentence is too broad.

## Mandated checkers and tooling

All commands used cwd `C:\tmp\P030_INTEGRATION_20260913` and the pinned Python 3.12.12 interpreter.

```text
command: <pinned-python> check_p030_archive_exporter.py
D-13 RED RAW REFUSAL: prefix record is not canonical JSONL
D-13 GREEN EXPORTED CAPTURE: PASS
----------------------------------------------------------------------
Ran 29 tests in 0.585s

OK
```

```text
command: <pinned-python> check_market_data_collector.py
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

```text
command: <pinned-python> check_p030_market_data_contracts.py
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

```text
command: <pinned-python> check_p030_closed_partition_backup_adapter.py
[The checker printed its 46 named tests plus P026 backup/check/restore JSON records; all file readbacks were “match”.]
----------------------------------------------------------------------
Ran 46 tests in 4.036s

OK
```

The adapter checker was also rerun with `tempfile.tempdir` set to the existing long-form non-ASCII scratch path. Exact conclusion:

```text
Ran 46 tests in 3.662s
OK
NONASCII_TEMP_EXIT=0
```

Standalone Ruff 0.16.4 was available and run. Observed counts match the current Lead parity record: exporter `0`; exporter checker `3` (`I001`, `RUF059`, `SIM117`); adapter `8` (`I001` x2, `RUF100` x3, `TRY004` x3); adapter checker `42` (`B023` x10, `S102` x4, `SIM117` x28). `ruff format --check p030_archive_exporter.py check_p030_archive_exporter.py` returned `2 files already formatted` and exit 0. The nonzero Ruff findings are pre-existing/default-rule parity, not introduced behavioral failures; the mandated tests, not Ruff, control BLOCK under this brief.

## Standards

- No documented repository standard is violated by the reviewed behavior. The root governance rules require exact source identity, executable RED/GREEN evidence, and honest limits; those are recorded above.
- The two `nesting_arms()` helpers are structurally duplicated across checkers (`check_p030_archive_exporter.py:24-94`, `check_p030_closed_partition_backup_adapter.py:14-79`), a possible Duplicated Code smell only. Keeping each checker self-contained avoids making one product check depend on the other, so I do not raise it as a finding.
- No speculative abstraction, network dependency, subprocess boundary in production, message chain, repeated type switch, or home-grown identity implementation was added.

## Findings

1. **NIT — raw exception while computing `exporter_sha256`.** `p030_archive_exporter.py:476-480`. Trigger: after target bytes have been successfully staged and re-read, `Path(__file__).read_bytes()` raises `OSError` (reviewer used `PermissionError`). Before value: module source readable. After value: module-source read denied. Observed result: raw `PermissionError`, `target_exists=False`, `staging_exists=True`, `receipt_exists=False`; a second run safely refused `target_exists`. This cannot publish a consumable partial target, so it is a NIT under the brief's severity rule, but it is the one ordinary I/O refusal path not mapped to `ExportRefused` or covered by a committed negative test.
2. **NIT — publication comments overstate the implementation.** `p030_archive_exporter.py:69,80` versus `:79-94`. The comment says final publication is “by os.replace only”; actual values are Windows `os.rename` and POSIX `os.replace`. The docstring headline says the function moves without replacing an existing final; the body correctly discloses the POSIX check/replace race. Observed behavior: Windows no-clobber tests pass, while the `os.replace` mutant overwrote the foreign target. This is documentation precision only; the POSIX residual itself is expressly accepted as documented, not closed.
3. **NIT — D-13 RED assertion permits the wrong refusal reason.** `check_p030_archive_exporter.py:134-152`. Declared/current expected value: `prefix record is not canonical JSONL`. Accepted test values: that string **or** `observation_id must match p030obs-v1 identity`. Current observed result is the required canonical-JSONL refusal, through the real adapter, but a future change that makes raw collector bytes canonical while leaving bare IDs would keep this test green under the alternate message. An exact assertion would better preserve the stated drill.
4. **NIT — duplicate-key refusal lacks a direct committed exporter regression.** The production hook at `p030_archive_exporter.py:105-110,241-259` is correct; the reviewer input `{"open":1,"open":2}\n` produced `ExportRefused.code=source_line_invalid`, no target. Current committed tests exercise the same code with malformed JSON, overflow, NaN, and both recursion layers, but no duplicate-key input; deleting the `object_pairs_hook` would therefore evade the exporter checker. This is a test-completeness nit, not a current behavior defect.

No REQUIRED finding remains. Repair-round finding 1 (consumable partial target) is CLOSED by staging, verification, receipt-first publication, no delete path, and load-bearing failure tests. Repair-round finding 2 (`..`/junction/link containment) is CLOSED for `..`, percent escapes, resolved containment, and the successfully created NTFS junction. The host denied creation of an additional symlink, recorded below.

## NOT VERIFIED

- This report alone accepts nothing; the Lead assembles the required T0 roster and records any acceptance.
- No real archive, production backup root, host/KVM2, deployment, credentials, venue/network contact, schedule, push, PR, merge, or acceptance action was performed.
- A real symlink component was attempted but Windows returned `WinError 1314` (required privilege not held). The NTFS junction path was created and independently refused by both exporter and adapter; committed adapter tests also cover mocked symlink components.
- The POSIX publication race was inspected but not executed on this Windows host. It remains documented and unresolved by design.
- Python 3.14 was not rerun by me; all acceptance execution and every modified-copy arm above used the mandated pinned Python 3.12.12.

VERDICT: PASS-WITH-NITS
