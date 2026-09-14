# REPORT_R7 - D9-A V3 instrument repair and V1.6 re-freeze

Lane: P20R7, 2026-09-14. Builder role (Codex Plus). Not a reviewer, not Lead, not acceptance.

Status: repaired and re-frozen as V1.6, NOT reviewed, NOT accepted, NOT executed on the real 45-cell matrix or 15 locked trials. No `--oneshot`, no `run_bounded_benchmark.py --run`, and no real-dataset simulation was run in this lane.

## Diff summary per item

| Item | Change | Evidence |
| --- | --- | --- |
| 1 Instrument record V3 | Added V3 with V2 interval unchanged, `record_id = SYNTH-P020-BOUNDED-INSTRUMENT-V3`, `quantity_step = 0.00001`, and required D9-A provenance. V1/V2 bytes were not edited. | `C:/tmp/P020_LEAD_20260912/benchmark/SYNTH-P020-BOUNDED-INSTRUMENT-V3.json:3`, `:25`, `:38`, `:39` |
| 2 Plan and driver re-pin | `BENCHMARK_PLAN.json` now pins V3 path/hash/id and the new driver digest; `RECORD_PATHS["instrument"]` points at V3. | `C:/tmp/P020_LEAD_20260912/benchmark/BENCHMARK_PLAN.json:27`, `:291`, `:292`, `:293`; `C:/tmp/P020_LEAD_20260912/benchmark/run_bounded_benchmark.py:25` |
| 3 Sizing-floor regression | Added synthetic BTC-scale V3 GREEN / V2 RED pair across 15m, 1h, 2h, 4h, 1D; the RED arm asserts the exact `no actual trade-bearing 2.1.0 successor result` clause. | `C:/tmp/P020_PRESELECT_20260913/tests/test_sizing_floor.py:1`, `:81`, `:94`, `:106` |
| 4 Runbook/prereg text | Runbook and prereg now name V1.6, mark V1.5 `b754...` dead after sizing-artifact BLOCKED, and describe D9-A V3 without changing selection rules/windows/prefixes. | `C:/tmp/P020_PRESELECT_20260913/PRESELECT_RUNBOOK.md:4`, `:66`, `:69`, `:74`, `:85`; `C:/tmp/P020_PRESELECT_20260913/PRESELECTION_PREREG_V1.md:3`, `:11`, `:12`, `:19`, `:20`, `:46` |
| 5 Re-freeze V1.6 | `preselect_profile.py` emits `p020-preselection-frozen-v1.6`, superseding V1.5. Two freezes were byte-identical. | `C:/tmp/P020_PRESELECT_20260913/preselect_profile.py:778`, `:779` |
| 6 Plan-derivation tool | Re-pinned `EXPECTED_FROZEN_SHA256` to V1.6 and refreshed `DERIVATION_RULE.md` V1.6 citations/pins. | `C:/tmp/P020_PLAN_DERIVE_20260913/derive_benchmark_plan.py:12`; `C:/tmp/P020_PLAN_DERIVE_20260913/DERIVATION_RULE.md:11`, `:48`, `:52` |
| 7 Benchmark runbook | Updated the benchmark runbook instrument row and V3 quantity-step sentence. | `C:/tmp/P020_LEAD_20260912/benchmark/BENCHMARK_RUNBOOK.md:55`, `:61` |

Required-read discrepancy: `REPORT_FIX1.md` was not present in `C:/tmp/P020_PRESELECT_20260913`; the only matching file found was `C:/tmp/P020_PLAN_DERIVE_20260913/REPORT_FIX1.md`, so that file was read and this discrepancy is recorded here.

## Validation output

Repository identity guard:

```text
tasklist /FI "IMAGENAME eq agy.exe"
ERROR: Access denied

Get-Process -Name agy -ErrorAction SilentlyContinue
<no output>

git -c safe.directory=* -C C:/P020_IMPL_20260912 rev-parse HEAD
b9b72f858dc830a9389517f79da5ea3c1fa6122c
```

Plan validation, cwd `C:/tmp/P020_LEAD_20260912/benchmark`:

```text
C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe .\run_bounded_benchmark.py --validate-plan
PLAN_VALID: frozen manifest, selections, hashes, and 15-trial shape verified
```

Sizing-floor pair, cwd `C:/tmp/P020_PRESELECT_20260913`:

```text
C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe -m pytest tests/test_sizing_floor.py -vv -p no:cacheprovider
============================= test session starts =============================
platform win32 -- Python 3.12.12, pytest-9.1.1, pluggy-1.6.0 -- C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe
rootdir: C:\tmp\P020_PRESELECT_20260913
collecting ... collected 10 items

tests/test_sizing_floor.py::test_v3_quantity_step_is_trade_bearing_for_synthetic_btc_scale_frame[15m] PASSED [ 10%]
tests/test_sizing_floor.py::test_v3_quantity_step_is_trade_bearing_for_synthetic_btc_scale_frame[1h] PASSED [ 20%]
tests/test_sizing_floor.py::test_v3_quantity_step_is_trade_bearing_for_synthetic_btc_scale_frame[2h] PASSED [ 30%]
tests/test_sizing_floor.py::test_v3_quantity_step_is_trade_bearing_for_synthetic_btc_scale_frame[4h] PASSED [ 40%]
tests/test_sizing_floor.py::test_v3_quantity_step_is_trade_bearing_for_synthetic_btc_scale_frame[1D] PASSED [ 50%]
tests/test_sizing_floor.py::test_v2_quantity_step_blocks_the_same_synthetic_btc_scale_frame[15m] PASSED [ 60%]
tests/test_sizing_floor.py::test_v2_quantity_step_blocks_the_same_synthetic_btc_scale_frame[1h] PASSED [ 70%]
tests/test_sizing_floor.py::test_v2_quantity_step_blocks_the_same_synthetic_btc_scale_frame[2h] PASSED [ 80%]
tests/test_sizing_floor.py::test_v2_quantity_step_blocks_the_same_synthetic_btc_scale_frame[4h] PASSED [ 90%]
tests/test_sizing_floor.py::test_v2_quantity_step_blocks_the_same_synthetic_btc_scale_frame[1D] PASSED [100%]

============================= 10 passed in 1.51s ==============================
```

Package tests, final run:

```text
C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
........................................................................ [ 67%]
..................................                                       [100%]
106 passed in 4.67s
```

Benchmark tests:

```text
C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
.....                                                                    [100%]
5 passed in 0.06s
```

Plan-derivation tests:

```text
C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
...............                                                          [100%]
15 passed in 0.27s
```

## Re-freeze output

Command-local safe-directory environment was used for both freezes: `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=safe.directory`, `GIT_CONFIG_VALUE_0=C:/P020_IMPL_20260912`.

```text
CODE1=0
CODE2=0
SHA1=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
SHA2=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
BYTES1=21417
BYTES2=21417
BYTE_IDENTICAL=True
TAIL1=FROZEN_WRITTEN C:\tmp\P020_PRESELECT_20260913\PRESELECTION_FROZEN.json sha256=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
TAIL2=FROZEN_WRITTEN C:\tmp\P020_PRESELECT_20260913\PRESELECTION_FROZEN.json sha256=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
```

Frozen JSON diff against V1.5 `b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b` from `C:/tmp/CLAUDE_P0_RUN_20260913/laneP20R6_repair/builder_artifacts/PRESELECTION_FROZEN.freeze1.json`:

```text
OK artifact_version :: 'p020-preselection-frozen-v1.5' -> 'p020-preselection-frozen-v1.6'
OK instrument_record_interval.record_id :: 'SYNTH-P020-BOUNDED-INSTRUMENT-V2' -> 'SYNTH-P020-BOUNDED-INSTRUMENT-V3'
OK instrument_record_interval.sha256 :: '1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15' -> '69b6f246ad721ccfde23f87c0b21b6470b8fb75b88552bfad004ef8c69d557f9'
OK prereg_sha256 :: '3f2ae546cd3a78111bb3eeb05e3a5f69163711b7515e8a664cd8620f28b62eab' -> '39f52ed0fc01bcc1017b36b9f2071ee59a66ecb46a07e89a60b0890c4a605d4c'
OK procedure_code_sha256 :: '54f35c8c82aea844637710eb74d490381dc0aeb071588100e76923ec3c31c877' -> 'c82693d492268944a7b3ed42aebe57a03ce033c3e9e23b4ccc24a60d6931c8d5'
OK runbook_sha256 :: '63874fc578579b4ae5ce2debfa39fbd453739e912d1740f9686584e83eae138d' -> '53faa45e583617be11f80cbc1550a3ee806175daa684e8f1620d288e03aab344'
OK source_pins.BENCHMARK_PLAN.json :: '8cf52e3d2a91cccdb1e36661f4f97c2b0f165725d4cf3841d4d252fe6fd5b448' -> 'c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7'
OK source_pins.run_bounded_benchmark.py :: 'b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3' -> '3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324'
OK supersedes :: 'p020-preselection-frozen-v1.4' -> 'p020-preselection-frozen-v1.5'
CHANGE_COUNT 9
CHECK_COUNT 0
STABLE selection_rule True
STABLE family_order True
STABLE datasets True
STABLE timeframe_order True
STABLE calibration_windows True
STABLE measurement_inputs True
```

## Digest table

| Artifact | Before | After |
| --- | --- | --- |
| Instrument record | V2 `1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15` | V3 `69b6f246ad721ccfde23f87c0b21b6470b8fb75b88552bfad004ef8c69d557f9` |
| Frozen artifact | V1.5 `b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b` | V1.6 `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` |
| `BENCHMARK_PLAN.json` | `8cf52e3d2a91cccdb1e36661f4f97c2b0f165725d4cf3841d4d252fe6fd5b448` | `c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7` |
| `run_bounded_benchmark.py` | `b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3` | `3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324` |
| Plan derivation expected freeze | `b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b` | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` |

## NOT VERIFIED

- No T0 review, Opus review, Sol review, Gemini corroboration, Lead reproduction, or acceptance has occurred on V1.6.
- The real 45-cell calibration matrix and the real 15 locked trials are still unproven; no valid real eligibility result was produced in this lane.
- The V1.5 one-shot returned `BENCHMARK_PROFILE_BLOCKED`; this repair does not prove the future V1.6 matrix or trials will pass.
- The 1D window may still be short of signals for reasons unrelated to sizing; its 361-row/161-usable-bar limitation remains.
- `tasklist` could not be used because the environment returned `Access denied`; `Get-Process -Name agy` was the fallback.
- Worktree cleanliness was not checked because the task forbids git commands other than the single `rev-parse HEAD`.
- `PRESELECTION_CALIBRATION.json` and `PRESELECTION_ELIGIBILITY.json` already existed in the package and were not deleted; refusal tests now assert such residue is unchanged.

