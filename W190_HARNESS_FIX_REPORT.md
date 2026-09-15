# W190 Harness Fix Report

## Verdict

**IMPLEMENTATION PASS; CANONICAL FULL GATE STILL REFUSED.** Both requested harness defects were
repaired in the binding order: pipeline first, seal second. The canonical post-fix `full-gate`
run exits 2 at `BASELINE_SEAL_IDENTITY_MISMATCH`, before scenario execution, because the supplied
baseline manifest still consumes `02b47a8e...` while the contract manifest and implementation
anchor carry `c9fef155...` (`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:13`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:283`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:4`).

Finding count: **2 requested defects repaired; 3 discrepancies/state divergences recorded.**

## Defect 1 - pipeline measured the golden instead of the engine

### Change

`run_comparison_pipeline()` now loads the sealed golden separately, calls
`execute_corrected_scenario()` exactly once for each RED/GREEN row, and compares that executed
output with the golden through the existing `compare_scoped_expected()` seam
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1334-1346`).
The executed output, not the golden, continues into the existing projection builder; no projection
selector, tolerance, scenario inclusion rule, or comparison surface changed
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1355-1368`).

Each scenario now records `corrected_expectation` and `first_corrected_mismatch`; every mismatch
also creates `CORRECTED_EXPECTATION_MISMATCH` in `acceptance_blockers`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1346-1354`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1369-1391`).
`main()` copies those pipeline blockers into the terminal full-gate predicate, so a
`STOP_MISMATCH` cannot reach the accepting branch
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1477-1490`).

### Proving test and D026 RED/GREEN

The test supplies one catalog row, changes the executed modified copy only at
`/RESULT_SURFACE/final_position/quantity`, and asserts one execution, `STOP_MISMATCH`, the exact
pointer, and the acceptance blocker
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:197-279`).

Command:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_comparison_pipeline_measures_executed_output_once_per_row -q
```

- RED on pre-fix behavior: **1 failed**; `executed == []`, expected
  `['RULE2-05-RED']`.
- GREEN after the fix: **1 passed**.

This is the required non-identity witness: the changed node is invisible when the pipeline loads
the golden as `corrected`, and visible only when the pipeline consumes the executor result
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:254-278`).

### Acceptance blocker decision

`LEGACY_EVENT_ORDER_MAP_PIN_MISSING` was **not removed**. Its declared condition remains unresolved
in the supplied bundle, so it stays alongside corpus blockers and the new corrected-expectation
blockers (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1382-1391`).
Real measurement and the widened predicate landed together before the seal relaxation, satisfying
the required safe order; the two code commits are `d994fc81` then `88df4dc9`.

## Defect 2 - validator hardcoded the superseded seal

### Change

`validate_sealed_producers()` now accepts the recomputed seal exactly when it equals the
manifest-recorded seal. The existing anchor, sidecar, baseline seal, catalog, driver, member, and
run-summary checks remain in sequence
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:952-1009`).
The obsolete literal no longer appears in the implementation; it remains only in the regression
test as the value a refreshed synthetic seal must differ from
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:121-132`).

### Proving tests and D026 RED/GREEN

The fixture builds a temporary 19-member contract manifest with matching recomputed seal, anchor,
anchor sidecar, catalog identity, driver identity, and 36-member baseline manifest
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:35-118`).
The positive test requires that refreshed self-consistent bundle to return its current seal; the
negative control modifies a member and updates its member digest while leaving the recorded bundle
seal stale, which must still refuse `EXPECTED_SEAL_MISMATCH`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:121-159`).

Command:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -q -k sealed_producer_validation
```

- RED before removing the literal: **1 failed, 1 passed**; the self-consistent temporary seal
  `59e35d49...` refused at `EXPECTED_SEAL_MISMATCH`, while the negative control was detected.
- GREEN after removing the literal: **2 passed**.

## Blast radius

- `red-evidence` and `full-gate` share the repaired pipeline invocation; `red-evidence` remains
  structurally non-accepting, and only `full-gate` owns the accepting branch
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1468-1490`).
- The `observe` caller was already executing the corrected engine, comparing it with the golden,
  and feeding the executed output into projections; its behavior was not changed
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:849-875`).
- The only production invocation of `run_comparison_pipeline()` found under `mtc_v2` is `main()`;
  the other invocation is the new regression test
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1468`;
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:266`).
- `validate_sealed_producers()` still flows through `validate_catalog()`, whose two production
  entry paths are `observe` and the comparison pipeline
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1013-1015`;
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:852`;
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1335`).

No third production caller required adaptation.

## Measured full-gate result before and after

Command both times:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
```

| State | Exit | Claim | First refusal | Measured detail |
|---|---:|---|---|---|
| Before both fixes | 2 | `BOUNDED_CORRECTION_EVIDENCE_REFUSED` | `EXPECTED_SEAL_MISMATCH` | recorded and computed were both `c9fef155ef86004313c2602048884f9d0f49faea085377d7e9bf9c06753454d0` |
| After both fixes | 2 | `BOUNDED_CORRECTION_EVIDENCE_REFUSED` | `BASELINE_SEAL_IDENTITY_MISMATCH` | current computed seal was `c9fef155ef86004313c2602048884f9d0f49faea085377d7e9bf9c06753454d0` |

The post-fix stop is the explicit baseline-vs-current-seal check
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:983-990`).
Because `validate_catalog()` runs before the executor loop, this canonical run measured **no
scenario MATCH/MISMATCH count**, and none is inferred
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1334-1345`).

## Verification summary

- Full corrected-vNext selftest directory:
  `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q` -> **218 passed**.
- Built-in verifier selftest:
  `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest` -> exit 0,
  **18 checks**: 3 `PASS`, 14 `DETECTED`, 1 `DETECTED:/a/1`. The built-in checks are constructed
  and returned by `run_selftests()`
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1396-1448`).
- Focused verifier test file after both fixes:
  `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -q`
  -> **93 passed**.

## Discrepancies

1. The packet's `HARNESS.py` and older `verify_bceg.py` line coordinates do not identify the live
   repository positions. DS41 explicitly warns that its spans must be re-derived; this report uses
   current `C:\WP012BUILD` lines
   (`C:\tmp\LANE_PROMPTS_20260828\DS41_RUN.log:78`;
   `C:\tmp\LANE_PROMPTS_20260828\N114_FALSE_GREEN_VERIFY.md:89`).
2. The statement that `LEGACY_EVENT_ORDER_MAP_PIN_MISSING` is the current state's only blocker is
   not true for the supplied catalog. Ten PROBE rows still carry two
   `BLOCKED-BUILD-ARTIFACT` digest fields each, and the validator creates one blocker per marked
   member
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:746-928`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1102-1114`;
   `C:\tmp\LANE_PROMPTS_20260828\N114_FALSE_GREEN_VERIFY.md:88`).
3. The default supplied baseline manifest is not refreshed to the repository's current seal: it
   consumes `02b47a8e...`, while the current contract manifest and anchor carry `c9fef155...`
   (`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:13`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:283`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:4`).

## Specification items not performed

- The unconditional legacy-map blocker was not removed because this lane did not add or verify a
  seal-pinned map/digest (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1388`).
- The supplied baseline manifest, PROBE artifacts, semantic review, goldens, catalog, kernel,
  tolerances, scenario set, and protected schemas were not changed. The current PROBE markers are
  visible in the catalog and are converted to blockers by the existing validator
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:746-928`;
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1102-1114`).
- No canonical per-scenario result is reported because the post-fix full gate refused at baseline
  identity before `execute_corrected_scenario()`
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:983-987`;
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1334-1345`).
- The separately identified PROBE execution ownership gap was not changed; N114 records its owner
  as not verified from the named objects (`C:\tmp\LANE_PROMPTS_20260828\N114_FALSE_GREEN_VERIFY.md:69`).

## Commits

1. `d994fc81` - `fix(mtc-v2): measure corrected gate output`
2. `88df4dc9` - `fix(mtc-v2): validate current contract seal`

No push, pull request, or merge was performed.
