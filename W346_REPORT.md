# W346 report — full-gate refusal when contract self-tests are red

## Verdict

**IMPLEMENTED; AWAITING INDEPENDENT VERIFICATION.** The full gate now executes the contract
self-test suite and appends exactly one new refusal source, `CONTRACT_SELFTEST_RED`, whenever that
suite exits non-zero. The canonical gate refused with the prior
`SEMANTIC_COVERAGE_REVIEW_MISSING` entry followed by the new refusal and all seven measured failing
test ids (`W346_GATE_RECEIPT.json:650-667`).

## Gate, scope, and lane record

- The owner marker existed before work began and records `Q-D a`
  (`C:\tmp\LANE_PROMPTS_20260828\OWNER_QD_A.txt:1`).
- The required initial state was measured as branch
  `feature/wp-p0-12-corrected-vnext-20260831`, HEAD
  `942fa18b7c63dfebf7bccc4f5a6f654b389b5c13`, with empty `git status --short`; this matches the
  lane's fixed point and non-master requirement
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W346_GATE_RED_SUITE_REFUSAL.md:3-6`).
- Gate-1 tier is **T1**: this is non-economic product verifier/test code, with no live, host,
  deploy, credential, broker, exchange, or trading action (`AGENTS.md:38-39`).
- Write lane: worktree `C:\WP012BUILD`; branch above; exact product paths are
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py` and
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`.
  The required generated outputs are `W346_GATE_RECEIPT.json` and this report. The Lead-issued
  prompt grants these exact paths and forbids push (`C:\tmp\LANE_PROMPTS_20260828\LANE_W346_GATE_RED_SUITE_REFUSAL.md:5-6,18-22`).
- Live-dependency status: none. Execution was confined to local self-tests, the frozen in-memory
  replay, and the one local canonical gate authorized by the lane
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W346_GATE_RED_SUITE_REFUSAL.md:4-6`).
- Parity/Pine/MTC strategy risk: none detected. No Pine, golden, parity corpus, core strategy,
  schema, broker, or exchange path changed; the product-stage rule requires no unrequested second
  behavior owner (`MTC_COMMAND_CENTER/01_MTC_PROJECT/AGENTS.md:21-23`).

## Design line implemented

Section 20 requires the real top-level verifier to drive the evidence mechanisms and refuse when a
modified copy reaches acceptance; that is the declared-but-unchecked prevention implemented here
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:886-893`).

The new suite runner invokes `python -m pytest` on the complete contract self-test directory,
captures the same-invocation result, and extracts every pytest `FAILED` node id
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4068-4106`).
Only `full-gate` calls that runner; `red-evidence` and every other mode retain their prior path
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4151-4164`).
On a non-zero suite result, one appended refusal carries the code, measured count, and failing ids;
the existing accepting branch remains reachable only when the complete blocker list is empty
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4189-4212`).

## RED first

Method: the synthetic full-gate helper exposes a monkeypatched suite-result marker. The regression
injects return code `1` plus the named PROBE-P012-02-A test id while keeping the comparison pipeline
and semantic review valid, then requires exit `2`, the refusal label, and the exact one-entry refusal
object (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:96-142,367-396`).

Against the pre-fix full-gate path, the new test failed exactly because the gate accepted:

```text
test_full_gate_refuses_a_red_contract_selftest_suite FAILED
E       AssertionError: assert 0 == 2
Captured stdout:
  "claim_label": "BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED"
============================== 1 failed in 0.32s ==============================
```

This is a real discriminator: the injected failing id was present, while pre-fix `main()` never
read the marker and returned the accepting result; the fixed path reads it at the full-gate call
site (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4151-4157`).

## GREEN and suite measurement

The identical focused command passed after the implementation:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_full_gate_refuses_a_red_contract_selftest_suite -vv
... test_full_gate_refuses_a_red_contract_selftest_suite PASSED [100%]
============================== 1 passed in 0.14s ==============================
```

The complete suite was then run directly:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
7 failed, 307 passed in 5.36s
```

The seven failing node ids are persisted by the canonical gate
(`W346_GATE_RECEIPT.json:656-665`). The new W346 regression is not among them and passed in the
same complete-suite run; its exact assertions remain at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:367-396`.

## Frozen legacy replay

The W249 in-memory replay compared all 17 RED/GREEN scenarios and both surfaces without rewriting
the baseline:

```text
SURFACES_EQUAL=34 MISMATCH=0 SKIPPED=0
```

The product-stage rule forbids changing goldens to obtain a pass; no golden or baseline path is in
the diff (`MTC_COMMAND_CENTER/01_MTC_PROJECT/AGENTS.md:8-10`).

## Canonical gate — invoked once

Exactly one canonical invocation was made, as required by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W346_GATE_RED_SUITE_REFUSAL.md:18-20`):

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W346_GATE_RECEIPT.json
EXIT_CODE=2
```

The receipt reports `acceptance_blockers: []`, `acceptance_reachable: true`, and the refusal claim
label (`W346_GATE_RECEIPT.json:2-3,114`). Its refusal list, quoted verbatim, is:

```json
[
  {
    "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
    "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
  },
  {
    "check_id": "CONTRACT_SELFTEST_RED",
    "detail": "7 contract self-tests failed",
    "failing_test_ids": [
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_expected_source_provenance_refuses_expected_path_changed_after_base",
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item3_recorded_exception_lifts_only_the_decision_134_path",
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item3_wrong_current_oid_does_not_lift_the_refusal",
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item3_wrong_base_state_does_not_lift_the_refusal",
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item3_committed_record_states_it_is_not_evidence",
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item8_provenance_refusal_reports_every_unlifted_path",
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_probe_cannot_claim_target_membership_when_base_is_refused"
    ]
  }
]
```

That is the previous one-entry refusal list plus `CONTRACT_SELFTEST_RED`, in the required order
(`W344_GATE_RECEIPT.json:650-655`; `W346_GATE_RECEIPT.json:650-667`).

## Discrepancies

1. The prompt's history says ten self-tests were red at seal #14, but the required HEAD is later:
   `git log -1` is W344 at `942fa18b`, and the current complete suite measured 7 failed / 307 passed.
   The canonical receipt therefore names seven failures, not ten
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W346_GATE_RED_SUITE_REFUSAL.md:5,8-9`; `W346_GATE_RECEIPT.json:656-665`).
2. The prompt allows the 02-A id to be absent once W344 has landed. W344 is the required HEAD, its
   report shows PROBE-P012-02-A DETECTED, and 02-A is not in the current seven-id failure list
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W346_GATE_RED_SUITE_REFUSAL.md:15-20`; `W344_REPORT.md:99-115`; `W346_GATE_RECEIPT.json:658-665`).
3. The product-stage output guide ordinarily asks for a `HANDOFF.md` update, while this lane
   expressly limits changes to the verifier, contract self-tests, and its named root evidence
   outputs. No `HANDOFF.md` write was made so the lane's narrower protected-path fence is preserved
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/OUTPUTS.md:6-8`; `C:\tmp\LANE_PROMPTS_20260828\LANE_W346_GATE_RED_SUITE_REFUSAL.md:5-6,21-22`).
4. The guard usage page names `pwsh`, but this host has no `pwsh` executable. The same checked-in
   guard script was run under Windows PowerShell instead; it returned `RESULT: PASS`, with exactly
   four staged files, no protected-path detection, and branch freshness 1 commit behind local
   `origin/master` against a limit of 30
   (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_USAGE.md:27-35`).

## Final checks

```text
git diff --check
exit=0

powershell -NoProfile -ExecutionPolicy Bypass -File MTC_COMMAND_CENTER\tools\repo_guard.ps1
RESULT: PASS
```

The staged set contains exactly the two scoped product files plus the required receipt and report;
the repository protocol requires this exact staged-file verification before commit
(`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md:9-15`).

## Commit and next verification

The exact authorized commit message is:

```text
feat(mtc-v2): refuse the full gate when the contract self-test suite is red (decision Q-D, W346)
```

The next verification belongs to a family that did not write this change
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W346_GATE_RED_SUITE_REFUSAL.md:21-22`). No push, PR, merge,
deploy, host contact, or trading action is authorized (`C:\tmp\LANE_PROMPTS_20260828\LANE_W346_GATE_RED_SUITE_REFUSAL.md:5-6`).
