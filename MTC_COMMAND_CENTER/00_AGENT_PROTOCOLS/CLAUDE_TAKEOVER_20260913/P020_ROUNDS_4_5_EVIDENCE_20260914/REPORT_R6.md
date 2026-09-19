# REPORT_R6 — repairing the P0-20 preselection package after the aborted V1.4 one-shot, and re-freezing as V1.5

Lane: P20R6 / P20R6C, 2026-09-14. Builder role (Codex Plus) produced the code repairs
and the two byte-identical freezes; this completion report was written by a different
agent (Grok, lane P20R6C) after the builder was cut by a usage limit. Not a reviewer,
not Lead.

**Status: repaired and re-frozen, NOT executed, NOT reviewed, NOT accepted.** No
calibration, eligibility check, benchmark, or simulation on real datasets was run. No
valid tokened `--oneshot` was run. `check_p020_acceptance.py` was not touched. The V1.4
token `f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff` is dead.

Identity check allowed by the brief:

```text
git -c safe.directory=* -C C:/P020_IMPL_20260912 rev-parse HEAD
b9b72f858dc830a9389517f79da5ea3c1fa6122c
```

## Diff summary per item

Compared against `C:/tmp/CLAUDE_P0_RUN_20260913/laneP20R6_repair/PRE_STATE_SHA256.json`
and V1.4 bytes in `C:/tmp/P020_PRESELECT_LEAD_REPRO_V14_20260913/`. V1 instrument record
bytes are unchanged (`b55287f26d5ff0a4bd6afb7a9112844bc64cb68014b5e12f40b7e536f436e91e`).

| Item | Repair | file:line |
| --- | --- | --- |
| 1 Instrument record V2 | New `SYNTH-P020-BOUNDED-INSTRUMENT-V2.json` (1526 bytes, sha256 `1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15`) plus sidecar. Byte-identical to V1 except `record_id` = `SYNTH-P020-BOUNDED-INSTRUMENT-V2`, `effective_interval.end_exclusive` = `2026-05-01T00:00:00Z`, and provenance `interval_extension` (`OD-20260914-P020-RECORD-V2-1`). V1 untouched. | `C:/tmp/P020_LEAD_20260912/benchmark/SYNTH-P020-BOUNDED-INSTRUMENT-V2.json:25,32` (`end_exclusive`, `record_id`); `:16-22` (`interval_extension`) |
| 2 Plan re-pin | `BENCHMARK_PLAN.json` `p020_profile.records.instrument` path/sha256/`record_id` now name V2. Driver `RECORD_PATHS["instrument"]` points at V2. Plan digest `1d98291fe…` → `8cf52e3d2a91cccdb1e36661f4f97c2b0f165725d4cf3841d4d252fe6fd5b448`. Driver digest `4b293de6c…` → `b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3`. `--validate-plan` accepts (identity only; see Tests). | `C:/tmp/P020_LEAD_20260912/benchmark/BENCHMARK_PLAN.json:290-293`; `run_bounded_benchmark.py:25`; plan `implementation_sources.run_bounded_benchmark.py` `:25-27` |
| 3 Freeze-time interval precondition | New `PRESELECT_REFUSED_RECORD_INTERVAL`. `instrument_record_interval`, `assert_instrument_interval`, `verify_frozen_record_interval` parse the pinned record once and check first/last timestamps of every calibration window and every measurement prefix. Frozen artifact records `instrument_record_interval` and per-window/prefix `first_ts`/`last_ts`. Real-stack smoke: `EconomicRecords.from_record_paths` + `for_evaluation` on window/prefix bounds. | `preselect_profile.py:166-253` (`parse_utc`, `row_timestamp`, `instrument_record_interval`, `assert_instrument_interval`, `verify_frozen_record_interval`); `:733`, `:766-773`, `:792`; `:628` (re-check before reservation); `tests/test_preselect.py:339-364` (`InstrumentRecordInterval`); `:1808-1842` (`RealInstrumentRecordSmoke`) |
| 4 Round-4 NIT residuals | N4-1/Sol-5: V1.3 line citations in prereg §(d)/(e)/(g) marked historical; function names authoritative. N4-2/Sol-2: `handle.truncate()` after each successful write in `ReservedOutputs.commit`; runbook wording "exclusive create, not an exclusive lock". N4-3/Sol-3: per-handle best-effort ABORTED recovery in `abort`; phase table names the residual. N4-4/Sol-1: freeze and re-check `prereg_sha256` / `runbook_sha256` computed LAST; field renamed `procedure_code_sha256`. Sol-4: runbook test command `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. | `PRESELECTION_PREREG_V1.md:47-48,58-70`; `preselect_profile.py:664,667` (truncate); `:677-697` (`abort`); `:873-877` (digests last); `PRESELECT_RUNBOOK.md:32-33,108,173`; `tests/test_preselect.py:1424,1436` |
| 5 Re-freeze V1.5 | Two builder freezes plus one completer scratch freeze; all three artifacts sha256 `b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b`, 21417 bytes, `artifact_version` `p020-preselection-frozen-v1.5`. Selection rule, family order, canonical bytes, calibration window rows/hashes, and measurement prefix hashes UNCHANGED vs V1.4 (see frozen-JSON diff below). V1.4 token stated dead in the runbook. | `preselect_profile.py:778-779`; `PRESELECT_RUNBOOK.md:66-72`; `PRESELECTION_FROZEN.json` sha256 `b75489841a09…` |
| 6b Driver family-set (D5=A) | `_validate_plan` keeps the original five-name check when `derivation` is absent; a derived plan requires exactly five distinct `strategy_id` values all contained in `plan["derivation"]["family_order"]`. Driver does not read `PRESELECTION_FROZEN.json`. `BENCHMARK_RUNBOOK.md:63` documents both branches. Tests cover original five, any five frozen families, outside-order, duplicate, wrong sizes. Current hand-written plan still validates. | `run_bounded_benchmark.py:181-196`; `BENCHMARK_RUNBOOK.md:63`; `tests/test_validate_plan_family_set.py:94-129` |
| 6c Plan-derivation tool (GKPD 1-6) | Single-read `load_json_once`; `REFUSED_SELECTION_FAMILY_NOT_FROZEN`; `derivation.family_order` copied from frozen; `EXPECTED_FROZEN_SHA256` re-pinned to V1.5 `b75489841a09…`; `strategy_family` = `strategy_id`; tests for malformed / non-object / frozen-file-vs-pin; rule text is value-for-value, not byte-for-byte. See `C:/tmp/P020_PLAN_DERIVE_20260913/REPORT_FIX1.md`. | `derive_benchmark_plan.py:12,30-39,67-77,96-99,134,167`; `tests/test_derive_benchmark_plan.py:233-298` |

## Frozen JSON: every differing key (V1.4 `f839c960…` vs V1.5 `b75489841a09…`)

Unchanged (required by item 5): `selection_rule`; `family_order` strategy ids and
`fixed_parameter_record_canonical` / `_sha256`; `datasets`; `timeframe_order`;
calibration window `start_row` / `end_row` / `row_count` / `sha256`; measurement
prefix `input_rows` / `sha256`.

Changed leaves present in both artifacts:

| key | V1.4 | V1.5 |
| --- | --- | --- |
| `artifact_version` | `p020-preselection-frozen-v1.4` | `p020-preselection-frozen-v1.5` |
| `supersedes` | `p020-preselection-frozen-v1.3` | `p020-preselection-frozen-v1.4` |
| `execution_identity_recheck` | names `procedure_sha256`; no prereg/runbook/interval re-check | names `procedure_code_sha256`, `prereg_sha256`, `runbook_sha256`, and interval re-check |
| `source_pins.BENCHMARK_PLAN.json` | `1d98291fea2783fb4e5dbff37386f21563c9a7c8757ee127eea404a1f6c1201d` | `8cf52e3d2a91cccdb1e36661f4f97c2b0f165725d4cf3841d4d252fe6fd5b448` |
| `source_pins.run_bounded_benchmark.py` | `4b293de6c26ae61ffec22c8205b81a1bad0c6561c0c642e19a37596b5fd62736` | `b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3` |

Removed: `procedure_sha256` (renamed).

Added: `procedure_code_sha256` = `54f35c8c82aea844637710eb74d490381dc0aeb071588100e76923ec3c31c877`;
`prereg_sha256` = `3f2ae546cd3a78111bb3eeb05e3a5f69163711b7515e8a664cd8620f28b62eab`;
`runbook_sha256` = `63874fc578579b4ae5ce2debfa39fbd453739e912d1740f9686584e83eae138d`;
`instrument_record_interval` `{record_id: SYNTH-P020-BOUNDED-INSTRUMENT-V2, sha256: 1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15, start_inclusive: 2019-09-08T00:00:00Z, end_exclusive: 2026-05-01T00:00:00Z}`;
`first_ts`/`last_ts` on all five `calibration_windows` and all fifteen measurement prefixes.

`execution_identity_recheck` and `supersedes` are versioning/recheck-text, not selection,
family-order, canonical-bytes, window-row, or prefix-hash changes.

## Tests

Command, cwd `C:\tmp\P020_PRESELECT_20260913`:

```text
C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
........................................................................ [ 75%]
........................                                                 [100%]
96 passed in 2.61s
```

Command, cwd `C:\tmp\P020_LEAD_20260912\benchmark`:

```text
C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
.....                                                                    [100%]
5 passed in 0.04s
```

Command, cwd `C:\tmp\P020_PLAN_DERIVE_20260913`:

```text
C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
...............                                                          [100%]
15 passed in 0.19s
```

`--validate-plan` confirmed from source before running: `run_bounded_benchmark.py:682-686`
loads the plan, calls `_validate_plan`, prints `PLAN_VALID`, and returns 0; `_run` is
not reached. Observed:

```text
PLAN_VALID: frozen manifest, selections, hashes, and 15-trial shape verified
```

Added / extended coverage:

| Item | Test evidence |
| --- | --- |
| 3 | `InstrumentRecordInterval` records and refuses out-of-range timestamps; `RealInstrumentRecordSmoke` calls `for_evaluation` on real pinned records. Completer also ran first+last timestamps of all five calibration windows and all five 2048-row prefixes: 20/20 accepted. V1 control `2025-09-22T08:00:00Z` refused `REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE`. CSV cross-check of 15m and 1D window bounds matched the frozen `first_ts`/`last_ts`. |
| 4 | `test_successful_commit_truncates_after_each_write`; `test_abort_is_best_effort_per_handle`; procedure/prereg/runbook digest re-check in `verify_frozen_identity`. |
| 6b | original five accepted without `derivation`; any five distinct frozen families accepted with `derivation.family_order`; family outside order refused; duplicate refused; wrong sizes refused. |
| 6c | single-read counts; malformed JSON; non-object JSON; frozen-file digest vs pin. |

`--oneshot` on a scratch copy of the package (cwd `C:/tmp/GROK_SCRATCH_P20R6C_20260914/pkg/`),
no output files created:

```text
--oneshot
PRESELECT_REFUSED_NO_T0_REVIEW: --i-have-t0-review-authorization <sha256 of PRESELECTION_FROZEN.json> is required
exit 2

--oneshot --i-have-t0-review-authorization f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff
PRESELECT_REFUSED_T0_TOKEN_MISMATCH: token does not match the frozen artifact digest
exit 2
```

Package dir has no `PRESELECTION_CALIBRATION.json` / `PRESELECTION_ELIGIBILITY.json`.

## Re-freeze

Builder `--freeze` was run twice into the package with command-local
`GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=safe.directory`,
`GIT_CONFIG_VALUE_0=C:/P020_IMPL_20260912`. Captures
`freeze_r6_1.out` and `freeze_r6_2.out` are byte-identical UTF-16 LE files
(43436 bytes, sha256 `b24ab207a60b649c11564d4d740ba3511da4e1830ec87875d84468a28cd2b739`).
`PRESELECTION_FROZEN.freeze1.json` is byte-identical to `PRESELECTION_FROZEN.json`.

```text
SHA1=b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b
SHA2=b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b
BYTES1=21417
BYTES2=21417
BYTE_IDENTICAL=True
TAIL1=FROZEN_WRITTEN C:\tmp\P020_PRESELECT_20260913\PRESELECTION_FROZEN.json sha256=b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
TAIL2=FROZEN_WRITTEN C:\tmp\P020_PRESELECT_20260913\PRESELECTION_FROZEN.json sha256=b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
```

Completer re-ran `--freeze` ONCE more into a scratch copy under
`C:/tmp/GROK_SCRATCH_P20R6C_20260914/pkg/` with the same command-local git env.
The copy is byte-identical to the package freeze:

```text
FROZEN_WRITTEN C:\tmp\GROK_SCRATCH_P20R6C_20260914\pkg\PRESELECTION_FROZEN.json sha256=b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
PKG_COPY_BYTE_IDENTICAL=True
```

New frozen digest:

```text
b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b
```

## Digests

`SHA256SUMS.txt` is written last with LF line endings and covers the review packet.
Current file digests before writing this report's checksum file:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `PRESELECTION_PREREG_V1.md` | 53736 | `3f2ae546cd3a78111bb3eeb05e3a5f69163711b7515e8a664cd8620f28b62eab` |
| `PRESELECTION_FROZEN.json` | 21417 | `b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b` |
| `PRESELECT_RUNBOOK.md` | 14657 | `63874fc578579b4ae5ce2debfa39fbd453739e912d1740f9686584e83eae138d` |
| `REPORT.md` | 21847 | `47efb87f7e01435a2fcbf9ede484b59f6b41a3673758ea3bdb1f14686766050e` |
| `REPORT_R2.md` | 23752 | `3969621dd0b882b8b88dafe10be02ef71365a73336f46396e9d7c562f15b6541` |
| `REPORT_R3.md` | 33253 | `fe9f765d2a8deeb2861868bc36fc38b731c8bee0cf5b9ab4618614be3ae5ffd5` |
| `REPORT_R4.md` | 33559 | `ee88be55a6a430162a8737112e1739090b9cb77efc25fbab43efbf7b7790ade4` |
| `REPORT_R5.md` | 6586 | `385c4c33dc3793e71f6716d38268a52325e8aa93f67ba3c92a2992bb04c77226` |
| `preselect_profile.py` | 61729 | `54f35c8c82aea844637710eb74d490381dc0aeb071588100e76923ec3c31c877` |
| `tests/test_preselect.py` | 84248 | `b88031729e8243264be1b69fccb9d4a8b10f3b513a40054682c44875efd2c2a2` |
| `C:/tmp/P020_LEAD_20260912/benchmark/BENCHMARK_PLAN.json` | 19814 | `8cf52e3d2a91cccdb1e36661f4f97c2b0f165725d4cf3841d4d252fe6fd5b448` |
| `C:/tmp/P020_LEAD_20260912/benchmark/run_bounded_benchmark.py` | 30031 | `b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3` |
| `C:/tmp/P020_LEAD_20260912/benchmark/BENCHMARK_RUNBOOK.md` | 7973 | `29b20fce93c484bc660605580791490505b5d60acb79a634db4136f105c3f82e` |
| `C:/tmp/P020_LEAD_20260912/benchmark/SYNTH-P020-BOUNDED-INSTRUMENT-V2.json` | 1526 | `1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15` |
| `C:/tmp/P020_PLAN_DERIVE_20260913/derive_benchmark_plan.py` | 8865 | `d7bdfab90189d2364e0105436bd7b9dcf9be4ef906136d00e2dc0e64d4821c85` |

## Review packet

Reviewable files under `C:/tmp/P020_PRESELECT_20260913/`:

1. `PRESELECTION_PREREG_V1.md`
2. `PRESELECTION_FROZEN.json`
3. `preselect_profile.py`
4. `tests/test_preselect.py`
5. `PRESELECT_RUNBOOK.md`
6. `REPORT.md`
7. `REPORT_R2.md`
8. `REPORT_R3.md`
9. `REPORT_R4.md`
10. `REPORT_R5.md`
11. `REPORT_R6.md`
12. `SHA256SUMS.txt`

Companion files outside the package: instrument V2 + sidecar, `BENCHMARK_PLAN.json`,
`run_bounded_benchmark.py`, `BENCHMARK_RUNBOOK.md`, `tests/test_validate_plan_family_set.py`,
`C:/tmp/P020_PLAN_DERIVE_20260913/` (`derive_benchmark_plan.py`, tests, `DERIVATION_RULE.md`,
`REPORT_FIX1.md`).

## NOT VERIFIED

- No T0 review, Sol review, Gemini corroboration, Opus review, or Lead acceptance has occurred on
  V1.5.
- The real 45-cell calibration / 15-trial eligibility run is still unproven; no matrix, selection, or
  eligibility result exists. The V1.4 one-shot aborted before producing a usable result; those
  ABORTED files were archived by the Lead and were not re-executed here.
- The real driver/profile stack was not run end to end; `--oneshot` was only exercised on refusal
  paths (no token; dead V1.4 token). Tests use synthetic doubles plus one real-stack
  `for_evaluation` smoke arm. No `_profile`, no `simulate_slice`, no `run_bounded_benchmark.py --run`.
- The Codex Plus builder (lane P20R6) was cut by a usage limit at 07:12Z after 140 commands. This
  completion was written by a different agent (Grok, lane P20R6C). The completer did not re-author
  the code; it verified the already-frozen V1.5 package, wrote this report, refreshed the
  derivation-rule citations, and regenerated digests.
- Worktree cleanliness was not checked because the task forbids git status/diff.
- The command-local `safe.directory` workaround was used only for `--freeze`; no git config was
  written.
- Builder freeze process exit codes were not separately captured; identity is taken from the
  byte-identical `freeze_r6_*.out` tails and from the frozen file / freeze1 copy / scratch re-freeze
  digest match.

This report is a builder/completer report only. It is not a review, not acceptance, and not
authorization to execute.
