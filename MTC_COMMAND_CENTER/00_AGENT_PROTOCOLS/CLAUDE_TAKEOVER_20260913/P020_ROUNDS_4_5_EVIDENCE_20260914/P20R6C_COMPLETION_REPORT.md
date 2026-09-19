# P20R6C COMPLETION REPORT

Lane: P20R6C (Grok tool-running completer). Task: complete the interrupted V1.5 builder lane.
No code changes. Builder was cut by the Codex Plus usage limit at 07:12Z after 140 commands.

Identity:

```text
git -c safe.directory=* -C C:/P020_IMPL_20260912 rev-parse HEAD
b9b72f858dc830a9389517f79da5ea3c1fa6122c
```

## Verifications (observed)

### Package tests (`C:/tmp/P020_PRESELECT_20260913`)

Command: pinned interpreter `-m pytest tests -q -p no:cacheprovider`

```text
........................................................................ [ 75%]
........................                                                 [100%]
96 passed in 2.61s
```

Expected 96. Observed 96 passed.

### Scratch re-freeze

Copied `preselect_profile.py`, `PRESELECTION_PREREG_V1.md`, `PRESELECT_RUNBOOK.md`,
`PRESELECTION_FROZEN.json` to `C:/tmp/GROK_SCRATCH_P20R6C_20260914/pkg/`. Ran
`--freeze` ONCE with `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory
GIT_CONFIG_VALUE_0=C:/P020_IMPL_20260912`.

```text
FROZEN_WRITTEN C:\tmp\GROK_SCRATCH_P20R6C_20260914\pkg\PRESELECTION_FROZEN.json sha256=b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
```

Package freeze, freeze1 copy (now moved), and scratch freeze are byte-identical:
`b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b` (21417 bytes).
Builder captures `freeze_r6_1.out` / `freeze_r6_2.out` are byte-identical to each
other (UTF-16 LE, 43436 bytes) and both tails name the same digest.

### `--oneshot` refusals (scratch copy)

No token:

```text
PRESELECT_REFUSED_NO_T0_REVIEW: --i-have-t0-review-authorization <sha256 of PRESELECTION_FROZEN.json> is required
exit 2
```

Dead V1.4 token `f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff`:

```text
PRESELECT_REFUSED_T0_TOKEN_MISMATCH: token does not match the frozen artifact digest
exit 2
```

No `PRESELECTION_CALIBRATION.json` or `PRESELECTION_ELIGIBILITY.json` created in
the copy or in the package directory.

### Benchmark tests and `--validate-plan`

Confirmed from source before running: `run_bounded_benchmark.py:682-686` loads the
plan, calls `_validate_plan`, prints `PLAN_VALID`, and returns 0. `_run` /
`_reserve_output_root` are not reached on `--validate-plan`.

```text
.....                                                                    [100%]
5 passed in 0.04s
```

```text
PLAN_VALID: frozen manifest, selections, hashes, and 15-trial shape verified
```

### Derivation tests

```text
...............                                                          [100%]
15 passed in 0.19s
```

Expected 15. Observed 15 passed.

### Real-stack precondition arm

Pinned interpreter; python root
`C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`.
`EconomicRecords.from_record_paths` over V2 instrument + cost V1 + funding V1.
`records.instrument.for_evaluation(ts, records.runtime_instrument_config or {})`
(`runtime_instrument_config` was `None`, so `{}`).

20/20 accepted (first and last timestamp of each of five calibration windows and
each of five 2048-row measurement prefixes). Values taken from frozen
`instrument_record_interval` / per-window / per-prefix bounds.

CSV cross-check (two windows):

- 15m rows 2049/4096: frozen and CSV both `2025-09-22T08:00:00Z` /
  `2025-10-13T15:45:00Z`
- 1D rows 2049/2409: frozen and CSV both `2025-04-17T00:00:00Z` /
  `2026-04-12T00:00:00Z`

V1 control: `for_evaluation("2025-09-22T08:00:00Z", {})` on
`SYNTH-P020-BOUNDED-INSTRUMENT-V1.json` refused
`REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE: evaluation timestamp is outside the record interval`.

### Frozen JSON identity vs V1.4

Selection rule, family order, canonical bytes, calibration window rows/hashes, and
measurement prefix hashes UNCHANGED. Differing keys listed in `REPORT_R6.md`.

## Files written

- `C:/tmp/P020_PRESELECT_20260913/REPORT_R6.md` (16353 bytes, sha256 `7b515c3dea93ab358caa9074c38716e4b0fb4a9472e4cb81fbdb57925f24fede`)
- `C:/tmp/P020_PLAN_DERIVE_20260913/REPORT_FIX1.md` (4690 bytes, sha256 `8467360c2c03ae0d0e57903208ff1a896a9dc9104640b7e98006812f16ccbcfe`)
- `C:/tmp/P020_PLAN_DERIVE_20260913/DERIVATION_RULE.md` refreshed (16210 bytes, sha256 `b7ea77b869c412f6fce478d1444f4ffcaa2fe035956de4cfb26efd165b7090b9`)
- `C:/tmp/P020_PRESELECT_20260913/SHA256SUMS.txt` (918 bytes, sha256 `dfbe9162eb58c4f9ea04b604bf6d12fdfbf926ce858090d4227c28f785a8a058`, CR=False)
- `C:/tmp/P020_PLAN_DERIVE_20260913/SHA256SUMS.txt` (435 bytes, sha256 `3856a722540e7f45ee401cd5415dcd472e3f4285dcd37aa25870d6a28792d0d8`, CR=False)
- `C:/tmp/P020_LEAD_20260912/benchmark/SHA256SUMS_V15.txt` (584 bytes, sha256 `21f3a3b2a843f50b09b1a9fc387064dae381b3cf50f45cbaf3a99959c7b02852`, CR=False)
- `C:/tmp/CLAUDE_P0_RUN_20260913/laneP20R6C_grok/COMPLETION_REPORT.md` (this file)

Scratch-only (not deliverables): `C:/tmp/GROK_SCRATCH_P20R6C_20260914/pkg/` (freeze copy),
`collect_evidence.py`, `diff_summary.py`, `housekeeping.py`, `evidence.json`,
`diff_summary.json`.

## Files moved

Destination: `C:/tmp/CLAUDE_P0_RUN_20260913/laneP20R6_repair/builder_artifacts/`
(move, not delete). Still present in package: [].

- `C:\tmp\P020_PRESELECT_20260913\PRESELECTION_FROZEN.freeze1.json` -> `C:\tmp\CLAUDE_P0_RUN_20260913\laneP20R6_repair\builder_artifacts\PRESELECTION_FROZEN.freeze1.json` (21417 bytes, sha256 `b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b`)
- `C:\tmp\P020_PRESELECT_20260913\freeze_r6_1.out` -> `C:\tmp\CLAUDE_P0_RUN_20260913\laneP20R6_repair\builder_artifacts\freeze_r6_1.out` (43436 bytes, sha256 `b24ab207a60b649c11564d4d740ba3511da4e1830ec87875d84468a28cd2b739`)
- `C:\tmp\P020_PRESELECT_20260913\freeze_r6_2.out` -> `C:\tmp\CLAUDE_P0_RUN_20260913\laneP20R6_repair\builder_artifacts\freeze_r6_2.out` (43436 bytes, sha256 `b24ab207a60b649c11564d4d740ba3511da4e1830ec87875d84468a28cd2b739`)
- `C:\tmp\P020_PRESELECT_20260913\TASK_R6.md` -> `C:\tmp\CLAUDE_P0_RUN_20260913\laneP20R6_repair\builder_artifacts\TASK_R6.md` (10191 bytes, sha256 `6a26fb42689c3e03bb4d1123d495a29c91e9a9291b8bb1e4d835d531d94f9d88`)

## SHA256SUMS contents

Package `SHA256SUMS.txt`:

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
| `REPORT_R6.md` | 16353 | `7b515c3dea93ab358caa9074c38716e4b0fb4a9472e4cb81fbdb57925f24fede` |
| `preselect_profile.py` | 61729 | `54f35c8c82aea844637710eb74d490381dc0aeb071588100e76923ec3c31c877` |
| `tests/test_preselect.py` | 84248 | `b88031729e8243264be1b69fccb9d4a8b10f3b513a40054682c44875efd2c2a2` |

Derivation `SHA256SUMS.txt`:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `derive_benchmark_plan.py` | 8865 | `d7bdfab90189d2364e0105436bd7b9dcf9be4ef906136d00e2dc0e64d4821c85` |
| `tests/test_derive_benchmark_plan.py` | 10826 | `4adb69a08bee0688199ca0415794208067ba9e710ada501500215d7ba0fdb4e8` |
| `DERIVATION_RULE.md` | 16210 | `b7ea77b869c412f6fce478d1444f4ffcaa2fe035956de4cfb26efd165b7090b9` |
| `REPORT.md` | 3062 | `8394279ef22e6d6ea410f73d4d633c88c46d810cfafbffe07d354d70099075bb` |
| `REPORT_FIX1.md` | 4690 | `8467360c2c03ae0d0e57903208ff1a896a9dc9104640b7e98006812f16ccbcfe` |

Benchmark `SHA256SUMS_V15.txt`:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `SYNTH-P020-BOUNDED-INSTRUMENT-V2.json` | 1526 | `1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15` |
| `SYNTH-P020-BOUNDED-INSTRUMENT-V2.json.sha256` | 65 | `3ffa5d503076ec1c6962b2540e86134ed37ca75c62b56f446a8cce20dcc5b160` |
| `BENCHMARK_PLAN.json` | 19814 | `8cf52e3d2a91cccdb1e36661f4f97c2b0f165725d4cf3841d4d252fe6fd5b448` |
| `run_bounded_benchmark.py` | 30031 | `b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3` |
| `BENCHMARK_RUNBOOK.md` | 7973 | `29b20fce93c484bc660605580791490505b5d60acb79a634db4136f105c3f82e` |
| `tests/test_validate_plan_family_set.py` | 4757 | `b8218f2eccd45c6e1621c5b5fcd49ce063560844c86ed37e7601b825a6791486` |

## Could NOT verify

- No T0 / Sol / Gemini / Opus / Lead review of V1.5.
- The real 45-cell / 15-trial run is still unproven. `--oneshot` was only run on
  refusal paths. `run_bounded_benchmark.py --run` was not invoked.
- Builder freeze process exit codes were not captured as numeric EXIT1/EXIT2;
  identity is from byte-identical freeze captures and matching frozen-file digests.
- Git worktree cleanliness was not checked (forbidden).
- Completer did not re-author procedure/driver/derivation code; it verified the
  already-present V1.5 work and wrote documentation/digests.

P20R6C_RESULT: COMPLETE
