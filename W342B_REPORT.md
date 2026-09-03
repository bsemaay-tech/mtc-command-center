# W342B - contract self-test re-alignment after W341B

## Verdict

**COMPLETE.** The two stale literals in
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`
were re-aligned after W341B. The catalog-bound literal now equals the sealed
`PROBE-P012-08-A.comparator_first_differing_node` value
`/EVENT_SURFACE/cash_events/0/signed_delta` (`scenario_catalog.json:2398`; `test_verify_bceg.py:1432-1435`).
The same test's stale array-container expectation now names the measured first unequal leaf
`/EVENT_SURFACE/cash_events/0/funding_event_id` (`test_verify_bceg.py:1454-1458`;
`W342B_GATE_RECEIPT.json:1038-1048`). No kernel, harness, golden, input, catalog, manifest,
anchor, probe, design, or baseline byte changed.

Worktree: `C:\WP012BUILD`. Branch: `feature/wp-p0-12-corrected-vnext-20260831`.
Starting HEAD: `05af785e3bec9c31aa1323bb897d72cd71b9642d`. Gate-1 tier: T1 because an
executable contract self-test changed. Exact write paths: the one self-test above,
`W342B_GATE_RECEIPT.json`, and this report. Live-dependency status: none. The completion marker is
written outside the repository only after the commit.

## Before and after literals

| Assertion | Before | After | Authority/evidence |
|---|---|---|---|
| catalog comparator pointer | `/EVENT_SURFACE/cash_events/1/signed_delta` | `/EVENT_SURFACE/cash_events/0/signed_delta` | sealed row at `scenario_catalog.json:2397-2399`; assertion at `test_verify_bceg.py:1432-1435` |
| measured receipt pointer | `/EVENT_SURFACE/cash_events` | `/EVENT_SURFACE/cash_events/0/funding_event_id` | GM83D-F02 at `C:\tmp\LANE_PROMPTS_20260828\DETECT_GM83D_BRANCH.md:28-43`; assertion at `test_verify_bceg.py:1454-1458` |

The owner-decision/design authority comment was retained and carries the required suffix
`; re-aligned to the W341B catalog value (W342B)` (`test_verify_bceg.py:1432`).

## Initial self-test suite - RED

Command, run from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
```

The two failures were:

```text
______ test_probe_driver_refuses_unclosed_base_before_variant_comparison ______

>       assert identity_receipt["measured_failed_check"] == "CLOSED_SET_VIOLATION"
E       AssertionError: assert 'CORRECTED_EXPECTATION' == 'CLOSED_SET_VIOLATION'
E
E         - CLOSED_SET_VIOLATION
E         + CORRECTED_EXPECTATION

mtc_v2\tests\corrected_vnext\contracts\selftests\test_verify_bceg.py:1393: AssertionError
```

```text
_______ test_probe_cannot_claim_target_membership_when_base_is_refused ________

>       assert probe["comparator_first_differing_node"] == comparator_first_node
E       AssertionError: assert '/EVENT_SURFA.../signed_delta' == '/EVENT_SURFA.../signed_delta'
E
E         - /EVENT_SURFACE/cash_events/1/signed_delta
E         ?                            ^
E         + /EVENT_SURFACE/cash_events/0/signed_delta
E         ?                            ^

mtc_v2\tests\corrected_vnext\contracts\selftests\test_verify_bceg.py:1435: AssertionError
```

```text
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_probe_driver_refuses_unclosed_base_before_variant_comparison
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_probe_cannot_claim_target_membership_when_base_is_refused
2 failed, 311 passed in 6.65s
```

The first failure is the deliberately open 02-A case, whose unchanged assertion remains at
`test_verify_bceg.py:1392-1398`. The second is the W342B target at `test_verify_bceg.py:1422-1459`.

## Full self-test suite after - GREEN for W342B

Command, run from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
```

The remaining failure and summary were:

```text
______ test_probe_driver_refuses_unclosed_base_before_variant_comparison ______

>       assert identity_receipt["measured_failed_check"] == "CLOSED_SET_VIOLATION"
E       AssertionError: assert 'CORRECTED_EXPECTATION' == 'CLOSED_SET_VIOLATION'
E
E         - CLOSED_SET_VIOLATION
E         + CORRECTED_EXPECTATION

mtc_v2\tests\corrected_vnext\contracts\selftests\test_verify_bceg.py:1393: AssertionError
```

```text
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_probe_driver_refuses_unclosed_base_before_variant_comparison
1 failed, 312 passed in 6.97s
```

The W342B target is therefore GREEN, while the deliberately open 02-A case remains RED at
`test_verify_bceg.py:1367-1419`.

## Frozen legacy replay

The W249 in-memory replay method documented at
`C:\tmp\LANE_PROMPTS_20260828\W276C_REPORT.md:207-229` was executed without writing a baseline:

```text
SURFACES_EQUAL=34 MISMATCH=0
```

## Canonical gate - invoked once

Command, invoked exactly once from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W342B_GATE_RECEIPT.json
exit=1
```

The receipt records mode `full-gate` and claim label
`BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED` (`W342B_GATE_RECEIPT.json:527,605`). It is
92,400 bytes with SHA-256
`436880728afbaebe56a41674b87ee5fa9129567c131648221ff0415ae2d0228f`. Its six-object refusal
array (`W342B_GATE_RECEIPT.json:1056-1108`) was compared structurally with W343's and was equal.

## Refusal list - verbatim

Copied verbatim from `W342B_GATE_RECEIPT.json:1056-1108`:

```json
  "refusals": [
    {
      "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
      "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
    },
    {
      "check_id": "EXPECTED_PATH_CHANGED_AFTER_BASE",
      "count": 18,
      "detail": "18 expected paths changed after the implementation base",
      "pointer": "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-RED.json",
      "pointers": [
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-03-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-03-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-04-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-04-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-05-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-05-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json"
      ]
    },
    {
      "check_id": "PROBE_NOT_DETECTED",
      "comparator_first_differing_node": "/RESULT_SURFACE/admitted",
      "measured_failed_check": "CLOSED_SET_VIOLATION",
      "scenario_id": "PROBE-P012-02-A"
    },
    {
      "check_id": "OBSERVED_EXTRA_MEMBER",
      "pointer": "/EVENT_SURFACE/cash_events/0/funding_event_id",
      "scenario_id": "RULE2-08-RED"
    },
    {
      "check_id": "OBSERVED_EXTRA_MEMBER",
      "pointer": "/RESULT_SURFACE/run_manifest/cost_schedule_digest",
      "scenario_id": "RULE2-08-RED"
    },
    {
      "check_id": "OBSERVED_EXTRA_MEMBER",
      "pointer": "/RESULT_SURFACE/run_manifest/cost_schedule_digest",
      "scenario_id": "RULE2-08-GREEN"
    }
  ],
```

## Scope verification

The substantive source diff is confined to two literals and the required comment suffix in the one
authorized test (`test_verify_bceg.py:1432-1433,1454-1458`). The required receipt and this report are
the only other repository outputs. No other assistant, model, network endpoint, host, broker,
venue, deploy, backtest, optimization, or trading action was used.

The repository guard ran with Windows PowerShell after staging the exact three paths and returned
`RESULT: PASS`; it reported the branch merge-base one commit behind local `origin/master`, within
its limit of 30, and reported no protected path according to its mechanical matcher
(`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md:25-32,50-51`).

## Discrepancies

1. The lane names `mtc_v2/tests/...` as a repository-root path, but that path does not exist in this
   worktree. The tracked repository path is
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/...`, as also embedded in the canonical
   receipt's changed-path pointer list (`W342B_GATE_RECEIPT.json:1066-1085`). The repository path was
   used under C-2.
2. The lane points to `BRANCH_DIFF_SINCE_de7c5c01.patch` lines 290-313 for the GM83D-F02 test
   assertions. Those physical packet lines describe re-seal metadata, not this test. The actual
   GM83D-F02 record is at `C:\tmp\LANE_PROMPTS_20260828\DETECT_GM83D_BRANCH.md:28-43`, and the test
   diff appears later in the packet. The finding's two named stale expectations were followed.
3. The retained authority comment above the second assertion still says the comparator "emits the
   unequal container before children" (`test_verify_bceg.py:1454`), while W341B's equalized array
   lengths now make the measured first difference a child leaf (`W342B_GATE_RECEIPT.json:1042`). It
   was left unchanged because the lane authorizes only the named assertions and explicitly requires
   the authority comment to be kept.
4. The documented guard command uses `pwsh` (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_USAGE.md:24-29`),
   but `pwsh` is not installed in this environment. The same read-only guard script was run with
   `powershell -NoProfile -ExecutionPolicy Bypass -File` and returned `RESULT: PASS`.
