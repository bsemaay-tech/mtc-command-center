# W306 Kernel Flagship 2b Report

## Verdict

**IMPLEMENTATION COMPLETE; CANONICAL GATE REFUSED ON AN OUT-OF-SCOPE DESIGN-PIN MISMATCH.**
All three authorized kernel findings are closed in separate commits with real RED/GREEN tests:
F02 now keys `cumulative_funding` on declared `DEF-P012-08`; F13 folds funding and fee counters
row by row; and F11 replaces the per-instance object with a deterministic empty-transition content
key (`C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:16-20`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:967-970`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:117-149,436-468`).

The independent legacy replay remained byte-exact at 34/34 surfaces after every item commit. The
final focused regression set is 4/4 GREEN. The complete contract self-test directory executed but
is not green: 304 passed and 7 failed, consisting of five stale harness-test expectations for the
old F02 behavior and two tests stopped by the external design-pin mismatch. Those bytes are outside
this lane's explicit fence (`C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:8-9,23-24`).

The one canonical gate invocation returned the non-accepting label
`BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED` and exactly one refusal,
`DESIGN_PIN_MISMATCH` (`W306_GATE_RECEIPT.json:1-9`). No acceptance, merge, deployment, or trading
claim is made.

## Authority, preflight, and write lane

- Authority is owner decision 136 for exactly F02, F13, and F11; golden, catalog, input, baseline,
  seal, probe, harness, and design bytes are expressly excluded
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:7-9`).
- Required preflight was satisfied before the first write: `W305_DONE.txt` existed, the branch was
  `feature/wp-p0-12-corrected-vnext-20260831`, the worktree was clean, and starting HEAD was
  `ac2d2ca9a73548b22574bf880b923e1df2141bbc`. The marker, branch, cleanliness, and STOP condition
  are specified at `C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:3-9`.
- The read-only repository guard passed before the first write and before every commit. It reported
  the branch merge-base one commit behind local `origin/master`, within its limit of 30; no fetch was
  performed. The lane forbids master work and pushing
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:4-9,23-24`).
- No other CLI assistant, agent, or model was invoked, as required by C-1
  (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).
- Live-dependency status is **NOT VERIFIED**. No broker, venue, host, credential, deployment,
  backtest, optimization, server, or launcher action was taken; execution was limited to the local
  unit tests, read-only replay, repository guard, and verifier allowed by the lane
  (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:33-36`).

Exact substantive paths changed by the three item commits:

```text
M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py
M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py
M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py
M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_position_manager_corrected.py
M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py
M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_w285_kernel_remaining.py
```

Evidence outputs are `W306_GATE_RECEIPT.json` and this report, as required by the report clause
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:26-28`). No prohibited artifact path
was changed.

## Item 1 - W279B-F02 - declared DEF controls funding-result membership

The flagship report identified the runtime-state predicate and the missing member on both Rule-8
rows (`C:\tmp\LANE_PROMPTS_20260828\W279B_FLAGSHIP2_RERUN_REPORT.md:79-119`). The independent
second-family report agreed that every declared DEF-P012-08 result must carry the member even when
the funding-event list is empty
(`C:\tmp\LANE_PROMPTS_20260828\_packets_T279B\T279B_REPORT.md:19,29-47`). The currently named
design still requires the member on every eligible or ineligible DEF-P012-08 result
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1224-1228`).

`corrected_surfaces` now accepts only the declared DEF identities for this decision and emits
`state.cumulative_funding` exactly when `DEF-P012-08` is declared
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:841-852,967-970`). The regression
constructs a result with no funding events, declares DEF-P012-08, and requires the zero-valued member
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py:161-179`).

Quoted RED:

```text
FAILED test_def_p012_08_result_includes_zero_cumulative_funding_without_events
E       KeyError: 'cumulative_funding'
1 failed in 0.14s
```

Quoted GREEN:

```text
.
1 passed in 0.05s
```

Full related file after the fix:

```text
......
6 passed in 0.06s
```

Commit: `4b1853c48ac94a75d4f633c3dd0af75cc6701580` -
`fix(mtc-v2): key funding result on declared definition`.

## Item 2 - W279B-F13 - ordered counter folds

The flagship report showed that equity was already accumulated in transition order while funding
and fees were still grouped before addition
(`C:\tmp\LANE_PROMPTS_20260828\W279B_FLAGSHIP2_RERUN_REPORT.md:399-429`). The independent family
confirmed that exact latent defect (`C:\tmp\LANE_PROMPTS_20260828\_packets_T279B\T279B_REPORT.md:25,100-101`).
The design orders fee/gross rows in fill sequence, emits the transition once, and applies cash rows
in array order (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:94-111,1135-1141`).

Funding cumulative validation now folds funding cash rows in order before checking the typed final
cumulative value. State mutation folds funding within the same ordered cash loop and fees within the
typed fee-row loop
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:436-468`). The two
regressions use binary64-sensitive `1e16`/`1.0` inputs independently for funding and fees
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_position_manager_corrected.py:169-219,222-271`).

Quoted RED:

```text
FAILED test_w279b_f13_cumulative_funding_applies_rows_in_order
E mtc_v2.core.types.EconomicTransitionError: REFUSED_INVALID_CASH_LEDGER_JOIN: funding cumulative mismatch

FAILED test_w279b_f13_cumulative_fee_applies_rows_in_order
E       assert 0.0 == 1.0
2 failed in 0.16s
```

Quoted GREEN:

```text
..
2 passed in 0.04s
```

Full related file after the fix:

```text
............
12 passed in 0.05s
```

Commit: `4cc007146cba6dd45103af7c0fddf201164191b8` -
`fix(mtc-v2): fold funding and fee counters in order`.

## Item 3 - W279B-F11 - deterministic empty-transition content identity

The flagship finding showed that the former `_application_identity` stored a new `object()` in each
empty transition, defeating content-based reapplication detection and retaining a live object in the
state key (`C:\tmp\LANE_PROMPTS_20260828\W279B_FLAGSHIP2_RERUN_REPORT.md:362-386`). The independent
family confirmed the same defect (`C:\tmp\LANE_PROMPTS_20260828\_packets_T279B\T279B_REPORT.md:24`).

The per-instance field is gone from `EconomicTransition`; its data contract now ends at the five
ordered event containers
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py:153-180`). An empty transition key
now consists only of deterministic content: semantics and record digests, a versioned key tag,
market timestamp, bar ordinal, lifecycle/side, and exact binary64 position facts
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:117-149`).

The regression launches two fresh Python processes with the same transition input, serializes each
applied key to UTF-8 JSON, requires byte identity, then confirms that independently resolved equal
empty-transition content cannot be applied twice in one state
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_w285_kernel_remaining.py:248-332`).

Quoted RED:

```text
FAILED test_w279b_f11_equal_empty_transition_keys_are_process_stable
TypeError: Object of type object is not JSON serializable
when serializing tuple item 4
assert [1, 1] == [0, 0]
1 failed in 0.32s
```

Quoted GREEN:

```text
.
1 passed in 0.25s
```

Related transition, manager, and W285 test files after the fix:

```text
............................
28 passed in 0.43s
```

Commit: `67f86ad247c4ca9f1d57090ea11f8be557971db1` -
`fix(mtc-v2): stabilize empty transition identity`.

## Legacy replay after every item commit

The replay loaded the digest-checked frozen legacy driver, executed KERNEL_1, canonicalized the live
surfaces, and compared their bytes directly with the sealed baseline surfaces. The called verifier
code checks the frozen driver digest before import and execution
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1581-1674`)
and compares canonical live bytes with each baseline event/result file
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1682-1730`).

```text
after 4b1853c48ac94a75d4f633c3dd0af75cc6701580:
SURFACES_EQUAL=34 MISMATCH=0 SKIPPED=0

after 4cc007146cba6dd45103af7c0fddf201164191b8:
SURFACES_EQUAL=34 MISMATCH=0 SKIPPED=0

after 67f86ad247c4ca9f1d57090ea11f8be557971db1:
SURFACES_EQUAL=34 MISMATCH=0 SKIPPED=0
```

No baseline output was generated or overwritten.

## Contract self-tests

Command executed from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
304 passed, 7 failed in 6.50s
```

The seven failures are fully classified:

1. Two pipeline-level tests stop in `validate_design_pin`, whose implementation refuses when the
   actual external file digest or line count differs from the manifest pin
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2220-2236`).
2. One probe-driver test still requires F02's pre-fix `CLOSED_SET_VIOLATION` at
   `/RESULT_SURFACE/cumulative_funding`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1381-1416`).
3. Two parameterized result-membership cases omit the design-required DEF-P012-08 conditional member
   from their expected set
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1894-1916`).
4. Two parameterized Rule-8 cases explicitly assert that `cumulative_funding` is absent even with
   empty funding events
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2058-2073`).

The final lane-specific regressions all pass at final implementation HEAD:

```text
python -m pytest <F02 test> <F13 funding test> <F13 fee test> <F11 test> -q
....
4 passed in 0.29s
```

The failing harness-test assertions were not rewritten because harness bytes are expressly outside
W306 scope (`C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:8-9`).

## Canonical gate - exactly one invocation

Executed once, after all three item commits, from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W306_GATE_RECEIPT.json
```

Receipt verification:

```text
bytes: 465
SHA-256: 37BFD44B8CBDAC791D8C6915BCFD2B7E245A0147E9992529458F6F3889205E5B
JSON parse: PASS
```

Full refusal output, with no omission:

```json
{
  "claim_label": "BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED",
  "mode": "full-gate",
  "refusal": {
    "check_id": "DESIGN_PIN_MISMATCH",
    "detail": "C:\\tmp\\LANE_PROMPTS_20260828\\P012_FRESH_DESIGN_V1.md: recorded_sha256=1f506c923c700df3a2a757ab3d49efabcd4d06bf39c251f8965c55bc10de8b75, actual_sha256=262d8f6b5127f825dcb88765ab0d05205451f75001474fce7fe942f2374fcd12, recorded_total_lines=1419, actual_total_lines=1469",
    "pointer": "/design"
  }
}
```

This is the complete singular preflight refusal, not a truncated `refusals[]` array
(`W306_GATE_RECEIPT.json:1-9`). Receipt commit:
`8b9e2964280431a3a3f77deaee483f2734d657fd` -
`test(mtc-v2): record W306 canonical gate receipt`.

## Discrepancies

1. **Design version and line ranges drifted.** The lane names design v1.12 and its v1.12 line ranges
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:13-14`), while the currently named
   external file identifies itself as v1.13
   (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1`). The repository manifest still pins
   v1.12, SHA-256 `1f506c...8b75`, and 1,419 lines
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-18`),
   whereas the gate measured SHA-256 `262d8f...fd12` and 1,469 lines
   (`W306_GATE_RECEIPT.json:4-7`). The current v1.13 text retains the required F02 member rule
   (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1224-1228`), so no authorized kernel
   disposition changed; the pin itself is owner/Lead work outside this lane.
2. **Contract self-tests retain F02's old expected absence.** Five test cases require the exact
   behavior W306 was ordered to remove
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1389-1416,1894-1916,2058-2073`),
   while both the lane and current design require presence
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:18`;
   `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1228`). C-2 says repository evidence wins
   and discrepancies must be reported, while this lane prohibits harness-byte edits
   (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`;
   `C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:8-9`). They remain failing and
   explicitly reported rather than silently changed.
3. **The gate's early refusal path does not write `--output`.** Normal receipts write the output
   file before return, but a `GateRefusal` is caught by a separate branch that writes JSON only to
   stdout
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3921-3941`).
   The lane nevertheless requires `W306_GATE_RECEIPT.json`
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W306_KERNEL_FLAGSHIP2B.md:26-28`). The gate was not invoked a
   second time; its exact emitted JSON was preserved as the required receipt (`W306_GATE_RECEIPT.json:1-9`).

## Commit inventory and close-out

| Item | Commit | Subject |
|---|---|---|
| F02 | `4b1853c48ac94a75d4f633c3dd0af75cc6701580` | `fix(mtc-v2): key funding result on declared definition` |
| F13 | `4cc007146cba6dd45103af7c0fddf201164191b8` | `fix(mtc-v2): fold funding and fee counters in order` |
| F11 | `67f86ad247c4ca9f1d57090ea11f8be557971db1` | `fix(mtc-v2): stabilize empty transition identity` |
| Gate receipt | `8b9e2964280431a3a3f77deaee483f2734d657fd` | `test(mtc-v2): record W306 canonical gate receipt` |

This report is the final lane commit; its own commit hash cannot be embedded without making the hash
self-referential. Explicit-path staging was used throughout; `git add .` and `git add -A` were not
used, matching C-5 (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-31`). No push, merge, PR,
master write, history cleanup, protected non-kernel behavior change, or prohibited artifact edit was
performed.
