# W283R3 Repair Round 3 Report

## Verdict

**R4 is REFUTED by the required runner-level test; zero kernel fixes were needed.** A funding
schedule event whose venue id already exists in the persisted key set, but which arrives while
`position is None`, is dispositioned as `FUNDING_ELIGIBILITY eligible=false`. It produces no cash
row, no funding row, no equity change, and no key-set change. This is the alternative explicitly
allowed by the lane prompt when the new test proves the event is already dispositioned rather than
applied (`C:\tmp\LANE_PROMPTS_20260828\LANE_W283R3_REPAIR_ROUND3.md:14-17`).

The focused regression is commit
`70366e038f65b409112b2c2d9f715e3bb9d064c6`
(`test(mtc-v2): cover no-position funding disposition`). It changes only
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py`.
No kernel, golden, catalog, input, baseline, seal, harness, design, schema, Pine, or adapter byte was
changed. No broker, venue, host, credential, deployment, backtest, optimization, launcher, or
live-trading operation was invoked. The authorization and byte fences are owner decisions 80-81
(`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:695-716`).

The required marker existed, the branch was
`feature/wp-p0-12-corrected-vnext-20260831`, and the worktree was clean before the first edit, as
required by the lane preconditions
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W283R3_REPAIR_ROUND3.md:3-8`). No push or history rewrite was
performed.

## R4 - no-position duplicate funding case

### Controlling design and implementation

- Funding applies to eligible open positions only
  (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:412`). Eligibility is controlled by the
  frozen position-snapshot rule (`P012_FRESH_DESIGN_V1.md:426`), one funding row exists per eligible
  position/event (`P012_FRESH_DESIGN_V1.md:428-435`), and the refused duplicate identity is the pair
  `(funding_event_id,lifecycle_id)` (`P012_FRESH_DESIGN_V1.md:437-439`).
- The runner maps `position is None` to `lifecycle_id=None`, `position_side=None`, and quantity
  `0.0`, while preserving the prior applied pair set in the economic state
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:507-519`). It sends the selected
  schedule event through the corrected adapter and applies the returned transition
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:775-796`).
- The adapter therefore computes `eligible=False`. Because no current lifecycle exists, there is no
  duplicate pair to refuse; it emits the typed `FUNDING_ELIGIBILITY` decision and returns an empty
  transition before any cash/funding construction
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:1131-1157`).

### New regression and quoted run

The new test explicitly sets `runner.state.position = None`, preserves prior pair
`("TEST-FUND-1", 1)`, invokes the runner funding path, and requires exactly one false eligibility
disposition, unchanged equity, no cash/funding rows, and the unchanged prior key set
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:323-347`).

Focused post-commit command:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py::test_w283r3_r4_runner_dispositions_duplicate_funding_without_position -q
.                                                                        [100%]
1 passed in 0.11s
```

There is no valid behavioral RED on the current code, so no kernel repair follows. The lane prompt
explicitly permits refutation when this test passes (`LANE_W283R3_REPAIR_ROUND3.md:16`). During test
construction, an initial draft incorrectly expected snapshot label
`IMMEDIATELY_BEFORE_FUNDING_TIMESTAMP` and failed only on that self-authored expectation. The frozen
record's actual label is `END_OF_INTERVAL_INCLUDE_SAME_TIMESTAMP_V1`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economic_records/funding/SYNTH-FUNDING-RULE2-08-V1.json:1`).
That draft failure is not defect evidence and is not reported as RED.

### Frozen legacy replay after the finding commit

The exact W249 in-memory replay method imports the current kernel, runs the frozen 17-row catalog,
and byte-compares both surfaces with the frozen baseline
(`W249_KERNEL_ORDERED_EQUITY_REPORT.md:206-252`). It ran after commit `70366e03` and returned:

```text
LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact
```

## R2 note - pin, not discriminator

R2 remains a construction pin, not a discriminator against the old implementation, exactly as the
current task requires the report to record (`LANE_W283R3_REPAIR_ROUND3.md:17`). The test constructs
the real Runner and checks the exact seed invariant
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:149-157`),
while the constructor explicitly supplies both `initial_capital=self.initial_capital` and
`equity=self.initial_capital`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:189-194`). Old code already had
that constructor behavior, so the test is assurance only.

The discriminating modified copy would change the constructor's one line
`equity=self.initial_capital` to `equity=0.0`; with configured initial capital `1234.5`, the existing
exact assertion at test line 157 would fail. The mutation was named only and was not implemented,
as directed by the report-only disposition (`LANE_W283R3_REPAIR_ROUND3.md:17`).

## Final verification

Commands ran from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` unless stated otherwise.

| Command | Exit | Measured result |
|---|---:|---|
| Focused R4 regression above | 0 | `1 passed in 0.11s` |
| W249 frozen replay | 0 | `17/17` scenarios, `34/34` surfaces byte-exact |
| `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q` | 0 | `256 passed in 4.37s` |
| `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest` | 0 | 18/18 declared dispositions: 3 `PASS`, 14 `DETECTED`, 1 `DETECTED:/a/1`; `NON_ACCEPTING_SELFTEST` |
| `$env:PYTHONPATH='00_PYTHON'; python -m pytest 00_PYTHON/mtc_v2/tests --ignore=00_PYTHON/mtc_v2/tests/corrected_vnext -q` from the stage root | 0 | `142 passed in 2.06s` |
| `git diff --check 725a20cf..HEAD` before the gate | 0 | clean |

The repair diff from the preceding report commit `725a20cf` through the finding commit contains
exactly the one self-test path named above. No active source path changed.

### Canonical gate - run exactly once

The single authorized invocation ran at clean finding commit `70366e03`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
exit=1
claim_label=BOUNDED_CORRECTION_EVIDENCE_REFUSED
acceptance_reachable=true
catalog_counts: RED=9 GREEN=8 PROBE=10
acceptance_blockers=9
refusals=10
```

Complete refusal list:

1. `SEMANTIC_COVERAGE_REVIEW_MISSING` -
   `mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.json`.
2. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-01-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
3. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-01-B`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
4. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-02-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
5. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-04-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
6. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-05-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
7. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-05-B`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
8. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-06-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
9. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-07-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
10. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-08-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.

The nine probe refusals are the known condition the prompt requires this lane not to alter
(`LANE_W283R3_REPAIR_ROUND3.md:19-22`). The gate was not rerun, and no probe byte was touched.

## Commits

| Purpose | Commit | Subject |
|---|---|---|
| R4 runner regression/refutation | `70366e038f65b409112b2c2d9f715e3bb9d064c6` | `test(mtc-v2): cover no-position funding disposition` |

The report-containing commit cannot include its own stable SHA; that SHA is supplied in the final
chat close, following the existing repository report convention
(`W283R2_REPAIR_ROUND2_REPORT.md:323-325`).

## Discrepancies

1. **The prompt's statement that the no-position duplicate "is applied" is not reproduced.** The
   runner supplies `lifecycle_id=None` and quantity `0.0`, and the adapter returns the typed false
   eligibility disposition before cash/funding construction (`core/runner.py:507-519`;
   `core/economics.py:1131-1157`). The new exact-case runner test passes and proves zero application
   (`test_runner_corrected.py:323-347`). Repository evidence therefore wins under C-2.
2. **A no-position event is not a duplicate pair under the design's declared identity.** Design
   line 439 defines duplication as `(funding_event_id,lifecycle_id)`. With no lifecycle, the event
   reuses a venue id but cannot form that pair; the existing false eligibility disposition is the
   bounded design-consistent outcome (`P012_FRESH_DESIGN_V1.md:412,428-439`). No substitute identity
   was invented.
3. **The valid test has no RED phase because the reported behavior is already correct.** The task
   itself allows the finding to be refuted by the test's passing run
   (`LANE_W283R3_REPAIR_ROUND3.md:16`). No source mutation was manufactured and no kernel fix was
   made.
