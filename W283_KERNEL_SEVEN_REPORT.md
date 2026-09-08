# W283 Kernel Seven Report

## Verdict

**All seven authorized kernel defects were reproduced, repaired, and committed in the required
order; no item was stopped.** The post-repair row measurement is **17/17 MATCH** and frozen legacy
replay remained **17/17 scenarios, 34/34 surfaces byte-exact** after every item commit. The
ten-probe prediction did not hold: the measured result is **1/10 DETECTED and 9/10
COULD_NOT_EVALUATE** because nine immutable probe manifests pin the pre-repair kernel tree. The one
canonical full-gate run therefore refused on the missing review plus those nine probe preflight
refusals.

This was the bounded W283 lane on branch
`feature/wp-p0-12-corrected-vnext-20260831` in `C:\WP012BUILD`. The prompt authorizes exactly these
seven kernel items and prohibits changes to goldens, catalogs, inputs, baselines, seals, the
verifier harness, and the design (`C:\tmp\LANE_PROMPTS_20260828\LANE_W283_KERNEL_SEVEN.md:3-11,13-23`).
Owner decisions 80 and 81 independently authorize the same seven findings and require a
failing-then-passing test plus byte-exact legacy replay
(`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:695-715`).

Preconditions were checked before the first edit: the W280 done marker existed, the branch was the
required feature branch, `HEAD` was `7aaf6853`, and `git status --porcelain` was empty. No push,
merge, live/scheduled dependency, network, venue, broker, credential, deployment, trading,
backtest, optimization, server, launcher, baseline generation, or result-artifact generation was
performed.

## Item 1 - W276-F01 ordered runtime equity cash events

Design authority: cash events are the sole cash ledger, must be consumed in their stored order,
and define the runtime equity window (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:67-83,94-109,1102-1119`).

- Commit: `4f832b220ea93c30d7d4286408f524d9c160e002` (`fix(mtc-v2): preserve runtime cash event order`).
- Diff: 2 files, 41 insertions, 3 deletions. `PositionManager.apply_transition` now applies each
  `signed_delta` directly to both runtime equity fields in array order
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:426-429`). The
  discriminating test is
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_position_manager_corrected.py:122-159`.
- RED command:
  `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_position_manager_corrected.py::test_w276_f01_runtime_equity_applies_cash_events_in_order -q`
  -> `FAILED`; quoted failure: `assert 0.0 == 1.0`.
- GREEN: the same command -> `1 passed`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## Item 2 - W276-F02 / W279-F10 lifecycle-aware funding dedupe

Design authority: duplicate funding identity is the pair `(funding_event_id, lifecycle_id)`
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:412-439`).

- Commit: `eac4f52d190dc1f0282f1e186568b8cb6e4292ff` (`fix(mtc-v2): key funding dedupe by lifecycle`).
- Diff: 6 files, 54 insertions, 12 deletions. A shared `FundingEventKey` type and paired state key
  now flow through types, economics, runner, adapter-facing state, and manager
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py:16,434`;
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:114,1131`;
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:518-520,783-790`;
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:325-331,438-440`).
  The named test is
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_economics.py:349-374`.
- RED command:
  `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_economics.py::test_w276_f02_funding_duplicate_identity_includes_lifecycle_id -q`
  -> `FAILED`; quoted failure: `TypeError: EconomicState.__init__() got an unexpected keyword argument 'applied_funding_event_keys'`.
- GREEN: the same command -> `1 passed`; the five focused funding tests also passed.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## Item 3 - W276-F03 typed missing-funding refusal

Design authority: a missing required funding event must produce the typed
`REFUSED_MISSING_FUNDING_EVENT` refusal (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:428-439`).

- Commit: `4f9e12e1b71d932bf997656e424f61aa22910c14` (`fix(mtc-v2): type missing funding event refusal`).
- Diff: 2 files, 28 insertions. The runner validates the production `events` collection before
  iteration and raises the typed economics refusal
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:751-760`). The named test is
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:329-348`.
- RED command:
  `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py::test_w276_f03_missing_production_funding_events_are_typed_refusal -q`
  -> `FAILED`; quoted failure: `TypeError: 'NoneType' object is not iterable`.
- GREEN: the same command -> `1 passed` and asserts the exact refusal token.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## Item 4 - W279-F09 unbracketed funding disposition

Design authority: every funding schedule event receives an eligibility decision with a typed
disposition; eligibility is not limited to an event strictly bracketed by two bars
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:412-439,867-872,1028-1100`).

- Commit: `0c38e460ca9e2cecc2821c6995114351c2e82c73` (`fix(mtc-v2): disposition unbracketed funding events`).
- Diff: 2 files, 42 insertions, 6 deletions. The funding evaluator accepts an absent previous or
  current boundary, records each evaluated event, and applies a transition for its eligibility
  disposition (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:722-809`). The
  parametrized named test is
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:277-292`.
- RED command:
  `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py::test_w279_f09_unbracketed_funding_event_gets_eligibility_disposition -q`
  -> `2 failed`; quoted failure in both cases: `assert len(decisions) == 1` with actual length `0`.
- GREEN: the same command -> `2 passed`; the full corrected runner test file measured `26 passed`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## Item 5 - W279-F08 funding snapshot and interval boundary rules

Design authority: the schedule carries explicit `position_snapshot_rule` and
`interval_boundary_convention` fields, while owner decision 46 requires a fill at the exact payment
timestamp to count (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:412-439,867-872`;
`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:303-311`).

- Commit: `a52165ac2675d1beca67420549bfdb7d43a34d85` (`fix(mtc-v2): apply funding schedule boundary rules`).
- Diff: 2 files, 80 insertions, 4 deletions. The runner validates both closed vocabulary values,
  requires hourly end timestamps, evaluates strictly earlier events before the bar, evaluates an
  equal-timestamp event after entry processing, and dispositions later events after the last bar
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:129-130,735-754,838-844,1644-1649`).
  The named test is
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:294-327`.
- RED command:
  `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py::test_w279_f08_position_snapshot_and_interval_boundary_are_applied -q`
  -> `FAILED`; quoted failure: `IndexError: list index out of range` because no funding event was
  emitted for the same-timestamp entry.
- GREEN: the same command -> `1 passed`; the full corrected runner test file measured `27 passed`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## Item 6 - W279-F11 corrected entry capital admission

Design authority: capital/margin admission precedes entry mutation in design section 3 step 8
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:94-109`).

- Commit: `29e095ac136cd10856e357e89822ea5621da28d0` (`fix(mtc-v2): enforce corrected entry margin admission`).
- Diff: 2 files, 36 insertions. `_apply_corrected_entry` applies the existing total-margin admission
  check to the final fill price and quantity before state mutation, covering both corrected call
  arms (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:596-612,2103-2125`). The
  named test is
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:537-565`.
- RED command:
  `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py::test_w279_f11_corrected_entry_applies_total_margin_admission -q`
  -> `FAILED`; quoted failure: `assert not True` (the pre-fix corrected entry was admitted).
- GREEN: the same command -> `1 passed`; the full corrected runner test file measured `28 passed`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

The first local fixture draft used existing quantity `6`; the sizer reduced the requested addition
to `1`, leaving required margin below available capital, so it could not discriminate the defect.
Before accepting RED evidence, the fixture was corrected to existing quantity `10`, the source fix
was removed, the exact pre-fix failure above was observed, and the source fix was restored for the
GREEN run. No non-discriminating run is presented as RED evidence.

## Item 7 - W279-F12 symmetric short stop and collision receipts

Design authority: short positions use the symmetric high-touch stop predicate and descending target
ordering; collision resolution follows stop-first execution
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:278-296,340-353,1028-1100`). Owner decision
72 fixes the all-touched receipt order as stop first, then targets in declared order
(`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:612-623`).

- Commit: `cae4b7e676a7f681c6410b3b3c29f5a37cfab21b` (`fix(mtc-v2): emit symmetric exit receipts`).
- Diff: 2 files, 54 insertions, 12 deletions. Exit evaluation now emits short
  `PROTECTIVE_STOP_EVALUATED` with `HIGH_TOUCH`, emits collision receipts for either side, records
  short target ordering as `SHORT_DESCENDING_TARGET_PRICE`, and puts the touched stop before target
  IDs (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:802-821,867-901`). The
  named test and its receipt assertions are
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_economics.py:152-188`.
- RED command:
  `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_economics.py::test_w279_f12_short_stop_and_collision_receipts_are_emitted_stop_first -q`
  -> `FAILED`; quoted failure: `StopIteration` while looking for the missing short protective-stop
  decision.
- GREEN: the same command -> `1 passed`; the full corrected economics test file measured `14 passed`.
- Post-commit W249 replay: `LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact`.

## Legacy replay after every item commit

The exact W249 method from `W249_KERNEL_ORDERED_EQUITY_REPORT.md:203-259` was run from the project
Python root after each commit. It recomputed both frozen legacy surfaces in memory and compared
their exact canonical bytes; it did not write observed results.

| Item | Commit | Scenarios | Surfaces | Result |
|---:|---|---:|---:|---|
| 1 | `4f832b22` | 17/17 | 34/34 | exact |
| 2 | `eac4f52d` | 17/17 | 34/34 | exact |
| 3 | `4f9e12e1` | 17/17 | 34/34 | exact |
| 4 | `0c38e460` | 17/17 | 34/34 | exact |
| 5 | `a52165ac` | 17/17 | 34/34 | exact |
| 6 | `29e095ac` | 17/17 | 34/34 | exact |
| 7 | `cae4b7e6` | 17/17 | 34/34 | exact |

## Seventeen-row measurement

The direct in-memory W246 executor/comparator method was run after all seven commits. It wrote no
observed artifact. The measured prediction is **17/17 MATCH, 0/17 MISMATCH**.

| Scenario | Result | First differing pointer | Classification |
|---|---|---|---|
| `RULE2-01-RED` | MATCH | - | MATCH |
| `RULE2-01-GREEN` | MATCH | - | MATCH |
| `RULE2-02-RED` | MATCH | - | MATCH |
| `RULE2-02-GREEN` | MATCH | - | MATCH |
| `RULE2-03-RED` | MATCH | - | MATCH |
| `RULE2-03-GREEN` | MATCH | - | MATCH |
| `RULE2-04-RED` | MATCH | - | MATCH |
| `RULE2-04-GREEN` | MATCH | - | MATCH |
| `RULE2-05-RED` | MATCH | - | MATCH |
| `RULE2-05-GREEN` | MATCH | - | MATCH |
| `RULE2-06-RED` | MATCH | - | MATCH |
| `RULE2-06-EQUAL-PRICE-RED` | MATCH | - | MATCH |
| `RULE2-06-GREEN` | MATCH | - | MATCH |
| `RULE2-07-RED` | MATCH | - | MATCH |
| `RULE2-07-GREEN` | MATCH | - | MATCH |
| `RULE2-08-RED` | MATCH | - | MATCH |
| `RULE2-08-GREEN` | MATCH | - | MATCH |

## Ten-probe measurement

Exact command, run after the 17-row measurement:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode probe --baseline-root C:\tmp\P012_BASELINE_RUN
claim_label=NON_ACCEPTING_PROBE_EVIDENCE
probe_blockers=9
```

| Probe | Expected check | Expected first changed node | Measured disposition | Measured check/reason |
|---|---|---|---|---|
| `PROBE-P012-01-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | COULD_NOT_EVALUATE | `PROBE_ARTIFACT_INVALID / PROBE_BASE_TREE_OID_MISMATCH` |
| `PROBE-P012-01-B` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | COULD_NOT_EVALUATE | `PROBE_ARTIFACT_INVALID / PROBE_BASE_TREE_OID_MISMATCH` |
| `PROBE-P012-02-A` | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | `/RESULT_SURFACE/admitted` | COULD_NOT_EVALUATE | `PROBE_ARTIFACT_INVALID / PROBE_BASE_TREE_OID_MISMATCH` |
| `PROBE-P012-03-A` | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | DETECTED | `RECORD_IDENTITY_PREFLIGHT`; exact node matched |
| `PROBE-P012-04-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | COULD_NOT_EVALUATE | `PROBE_ARTIFACT_INVALID / PROBE_BASE_TREE_OID_MISMATCH` |
| `PROBE-P012-05-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | COULD_NOT_EVALUATE | `PROBE_ARTIFACT_INVALID / PROBE_BASE_TREE_OID_MISMATCH` |
| `PROBE-P012-05-B` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | COULD_NOT_EVALUATE | `PROBE_ARTIFACT_INVALID / PROBE_BASE_TREE_OID_MISMATCH` |
| `PROBE-P012-06-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/exit_id` | COULD_NOT_EVALUATE | `PROBE_ARTIFACT_INVALID / PROBE_BASE_TREE_OID_MISMATCH` |
| `PROBE-P012-07-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fee_events/1/liquidity_role` | COULD_NOT_EVALUATE | `PROBE_ARTIFACT_INVALID / PROBE_BASE_TREE_OID_MISMATCH` |
| `PROBE-P012-08-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | COULD_NOT_EVALUATE | `PROBE_ARTIFACT_INVALID / PROBE_BASE_TREE_OID_MISMATCH` |

The nine kernel probe manifests pin base tree
`2c749345ed9be5186659369f091ce77a2e42d61a`, while the repaired `mtc_v2/core` tree is
`d4123e459840fd51c84e0225fee367679dbdf35a`. The verifier is required to compare that pin before
executing a probe and raises `PROBE_BASE_TREE_OID_MISMATCH` on inequality
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1637-1639`).
`PROBE-P012-03-A` changes an instrument record instead of the kernel subtree and remained valid.
Refreshing probe manifests or their bound artifacts would violate W283's explicit no-probe/no-seal/
no-harness write fence, so no such adjustment was made.

## Test and hygiene counts

Commands below were run from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` unless an absolute path is shown.

| Command | Exit | Measured result |
|---|---:|---|
| `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q` | 0 | **243 passed in 5.75s** |
| `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest` | 0 | **18 expected dispositions:** 3 PASS, 14 DETECTED, 1 `DETECTED:/a/1`; `NON_ACCEPTING_SELFTEST` |
| `$env:PYTHONPATH='00_PYTHON'; python -m pytest 00_PYTHON/mtc_v2/tests --ignore=00_PYTHON/mtc_v2/tests/corrected_vnext -q` from the stage root | 0 | **142 passed in 1.84s** |
| `git diff --check 7aaf6853..HEAD` | 0 | clean |

The changed implementation/tests are exactly four kernel files and three contract self-test files:

- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_economics.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_position_manager_corrected.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_runner_corrected.py`

No golden, catalog, input, baseline, seal, probe artifact, `verify_bceg.py`, design, adapter,
schema, Pine, or parity corpus byte changed in the seven item commits.

## Canonical full gate - run exactly once

The canonical gate was run exactly once, at the end, as required
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W283_KERNEL_SEVEN.md:32-36`).

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
exit=1
claim_label=BOUNDED_CORRECTION_EVIDENCE_REFUSED
acceptance_reachable=true
scenario_receipts=17
acceptance_blockers=9
refusal_count=10
```

All 17 scenario receipts reported `corrected_expectation=MATCH`, and the legacy event-order pin
reported MATCH. The complete refusal list was:

1. `SEMANTIC_COVERAGE_REVIEW_MISSING` - `semantic_coverage_review.json`.
2. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-01-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
3. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-01-B`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
4. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-02-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
5. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-04-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
6. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-05-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
7. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-05-B`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
8. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-06-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
9. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-07-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.
10. `PROBE_COULD_NOT_EVALUATE` - `PROBE-P012-08-A`; inner `PROBE_BASE_TREE_OID_MISMATCH`.

This is an evidence refusal, not authorization or an acceptance verdict.

## Commits

| Item | Commit | Subject |
|---:|---|---|
| 1 | `4f832b220ea93c30d7d4286408f524d9c160e002` | `fix(mtc-v2): preserve runtime cash event order` |
| 2 | `eac4f52d190dc1f0282f1e186568b8cb6e4292ff` | `fix(mtc-v2): key funding dedupe by lifecycle` |
| 3 | `4f9e12e1b71d932bf997656e424f61aa22910c14` | `fix(mtc-v2): type missing funding event refusal` |
| 4 | `0c38e460ca9e2cecc2821c6995114351c2e82c73` | `fix(mtc-v2): disposition unbracketed funding events` |
| 5 | `a52165ac2675d1beca67420549bfdb7d43a34d85` | `fix(mtc-v2): apply funding schedule boundary rules` |
| 6 | `29e095ac136cd10856e357e89822ea5621da28d0` | `fix(mtc-v2): enforce corrected entry margin admission` |
| 7 | `cae4b7e676a7f681c6410b3b3c29f5a37cfab21b` | `fix(mtc-v2): emit symmetric exit receipts` |

The report commit cannot include its own stable SHA; that containing commit is supplied in the
final chat.

## Discrepancies

1. **The predicted probe result was not measured.** W283 predicts 10/10 but explicitly labels that
   number a prediction (`C:\tmp\LANE_PROMPTS_20260828\LANE_W283_KERNEL_SEVEN.md:32-34`). The measured
   result is 1/10 DETECTED and 9/10 COULD_NOT_EVALUATE because the authorized repairs necessarily
   changed the kernel tree OID while nine immutable probe manifests bind its old OID. The prompt
   forbids changing those artifacts, so the mismatch is reported rather than concealed.
2. **The gate did not refuse on the review only.** The expected review-only refusal
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W283_KERNEL_SEVEN.md:35`) was accompanied by the nine probe
   preflight refusals above. The canonical gate was not rerun because W283 permits it exactly once.
3. **The sealed contract manifest describes an older design byte.** The live design identifies
   itself as v1.12 and hashes to
   `1f506c923c700df3a2a757ab3d49efabcd4d06bf39c251f8965c55bc10de8b75`, while the repository
   manifest still identifies v1.11 re-seal #10 and pins
   `2d8d0e38c5c9b426abfab50ca647a58fd4312d1cae7864aa9cb991d269bda99a`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-17`).
   This pre-existing state was left untouched because manifest and design changes are expressly
   forbidden in W283.
