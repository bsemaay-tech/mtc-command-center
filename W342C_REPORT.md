# W342C provenance self-test re-anchor report

## Verdict

**PASS; 0 findings.** The seven named self-tests now exercise synthetic post-base conditions while
retaining the re-anchored `63cfe2dd2dcb3373f2fa18c385f67a1c2d113bb5` declaration. The full
contract suite measured 314 passed, the frozen legacy replay measured 34 matching surfaces, and the
single canonical gate invocation contains only `SEMANTIC_COVERAGE_REVIEW_MISSING`
(`W342C_GATE_RECEIPT.json:117-126,193-198,650-655`).
Measured at HEAD `4642998d` and appended by lane W353, that coverage is not uniform: of the seven, ONE
(`test_expected_source_provenance_refuses_expected_path_changed_after_base`, `test_verify_bceg.py:698-707`) keeps a live
`git diff` measurement, calling `validate_expected_source_provenance` against the paths that really changed after base
`63cfe2dd`; FOUR (`test_verify_bceg.py:805-820,823-840,843-857,910-926`) exercise the exception-lifting logic over a
synthesized changed-path list built by the helper `w305_provenance` (`test_verify_bceg.py:754-802`, which replaces
`subprocess.check_output` for `git diff --name-only`); ONE (`test_verify_bceg.py:884-907`) only pins the committed exception
record's values and reads no changed-path list at all; and ONE
(`test_probe_cannot_claim_target_membership_when_base_is_refused`, `test_verify_bceg.py:1632-1681`) drives a probe against a
synthetic child receipt rather than any changed-path list - the split exists because owner decision 147 required lane W342C to
re-anchor these tests onto synthetic post-base conditions instead of the historical live repository state.

The worktree started clean at required HEAD `cb7998e2c379183bc49a76f43fb160f83bc57c33`
on non-master branch `feature/wp-p0-12-corrected-vnext-20260831`. The lane authorizes only the
contract self-tests plus this report and the named receipt, and forbids verifier, kernel, golden,
input, catalog, manifest, anchor, probe, design, push, and master changes
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W342C_PROVENANCE_SELFTESTS_REANCHOR.md:3-6,27-32`).
The write lane is `C:\WP012BUILD`; exact writable paths are
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`,
`W342C_GATE_RECEIPT.json`, and `W342C_REPORT.md`; no tracked live or scheduled dependency was
identified. This is T1 test-only work with no Pine, kernel, strategy, broker, venue, host, deploy,
credential, or trading action.

## Initial RED suite - seven failures quoted verbatim

The suite was run from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` before any test edit:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
7 failed, 307 passed in 6.25s
```

The seven pytest summary lines were:

```text
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_expected_source_provenance_refuses_expected_path_changed_after_base
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item3_recorded_exception_lifts_only_the_decision_134_path
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item3_wrong_current_oid_does_not_lift_the_refusal
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item3_wrong_base_state_does_not_lift_the_refusal
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item3_committed_record_states_it_is_not_evidence
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item8_provenance_refusal_reports_every_unlifted_path
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_probe_cannot_claim_target_membership_when_base_is_refused
```

Those exact node ids are also persisted by the immediately preceding W346 canonical receipt
(`W346_GATE_RECEIPT.json:656-665`). The terminal failure reasons, quoted verbatim, were:

```text
E       Failed: DID NOT RAISE <class 'mtc_v2.tests.corrected_vnext.verify_bceg.GateRefusal'>
E       AssertionError: assert False
E       AssertionError: assert False
E       AssertionError: assert False
E       AssertionError: assert ['W156', 'W16...316D', 'W350'] == ['W156', 'W16...172', 'W316D']
E       AssertionError: assert False
E       AssertionError: assert '/EVENT_SURFA.../signed_delta' == '/EVENT_SURFA...ding_event_id'
```

The old assertions depended on a historical live refusal even though current provenance is MATCH
with zero changed expected paths; the gate now records that state directly
(`W342C_GATE_RECEIPT.json:117-126`).

## Re-anchored fixture and recorded values

Decision 147's design amendment defines the base as the commit carrying the latest owner-directed
in-repo re-seal and narrows the machine predicate to changes after that re-seal
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:722-730`). L14 separately carries the
historical pre-implementation property and repeats the bounded post-re-anchor meaning
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:836-844`).

The shared fixture moves manifest members in memory to `expected_provenance_exceptions.json` and
`implementation_anchor.json`, then supplies a synthetic changed-path list while leaving the real
manifest, anchor, record, and expected files untouched
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:647-677,684-732`).
The record substitution uses a temporary file and the production record loader, so invalid-record
tests still exercise the real closed-schema checks (`test_verify_bceg.py:696-717`).

All authoritative values come from the committed record: base and current blob OID
`0ad42dafc7c6634319afddc9ff12a43d095438ae`, `PRESENT_AT_BASE`, lane ids through `W350`, decision
134, and the full `63cfe2dd...` implementation base
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:5-20`).

## Per-test RED/GREEN evidence

Each RED check used an in-memory modified condition and restored it immediately; the forbidden
`verify_bceg.py` file was never edited. The combined RED run exited 0 only after all seven repaired
tests raised a pytest failure under their corresponding removed behavior. The unmodified focused
test module then measured `151 passed in 5.25s`, and the complete suite measured `314 passed in
5.79s`.

| Test | Guarded behavior | Old assertion | New fixture | RED evidence when guard removed | GREEN evidence |
|---|---|---|---|---|---|
| `test_expected_source_provenance_refuses_expected_path_changed_after_base` | A post-base expected-path change is refused. | Expected the clean live manifest to refuse. | Moves one expected member in memory to a path changed after `63cfe2dd` and requires the exact pointer (`test_verify_bceg.py:628-637`). | Replaced the predicate with MATCH: `Failed: DID NOT RAISE ... GateRefusal`. | Exact refusal id and moved pointer pass (`test_verify_bceg.py:633-637`). |
| `test_w305_item3_recorded_exception_lifts_only_the_decision_134_path` | The record lifts only its declared path. | Used historical live changes and asserted only that the next pointer differed. | Supplies the decision path plus one moved path; without the record the decision path refuses, with it only the moved path refuses (`test_verify_bceg.py:735-750`). | Modified the exception outcome to lift every path: `AssertionError`. | Both exact pointers pass (`test_verify_bceg.py:742-750`). |
| `test_w305_item3_wrong_current_oid_does_not_lift_the_refusal` | A wrong current blob OID cannot lift. | Used invented `000...` against a live state with no changes. | Uses the Git-measured OID of the moved path as a valid but wrong OID, then requires the declared path to remain refused (`test_verify_bceg.py:753-770`). | Modified the identity check to accept the wrong OID: `AssertionError`. | Exact declared-path refusal passes (`test_verify_bceg.py:765-770`). |
| `test_w305_item3_wrong_base_state_does_not_lift_the_refusal` | A wrong base state cannot lift. | Reassigned `PRESENT_AT_BASE` to itself and paired it with an invented blob. | First pins committed `PRESENT_AT_BASE`, then supplies valid-but-wrong `ABSENT_AT_BASE`/null in the temporary record (`test_verify_bceg.py:773-787`). | Modified the state check to accept the wrong state: `AssertionError`. | Exact declared-path refusal passes (`test_verify_bceg.py:782-787`). |
| `test_w305_item3_committed_record_states_it_is_not_evidence` | The committed record is a declaration with the re-anchored values. | Pinned the pre-W350 lanes and M5 blob. | Pins declaration wording, `63cfe2dd...`, W350-inclusive lanes, `PRESENT_AT_BASE`, and both committed OIDs (`test_verify_bceg.py:814-837`). | Modified the fixture declaration kind to evidence: `AssertionError`. | Every committed value passes (`test_verify_bceg.py:817-837`). |
| `test_w305_item8_provenance_refusal_reports_every_unlifted_path` | Every unlifted path is reported. | Expected all historical manifest members except the decision path to refuse. | Lifts the decision path and requires both synthetic moved paths in exact order and count (`test_verify_bceg.py:840-856`). | Modified the refusal to omit one path: `AssertionError`. | Exact two-path list/count passes (`test_verify_bceg.py:844-856`). |
| `test_probe_cannot_claim_target_membership_when_base_is_refused` | A refused probe base cannot claim an absent target node. | Drove the live 08-A modified copy to DETECTED, then asserted a stale comparator node. | Supplies a refused child receipt containing only the comparator node; target membership is false and status must be NOT_DETECTED (`test_verify_bceg.py:1562-1611`). | Modified the driver result to claim DETECTED with target membership false: `AssertionError`. | NOT_DETECTED, false membership, and false measured match pass (`test_verify_bceg.py:1606-1611`). |

## Final contract suite

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
314 passed in 5.79s
```

The canonical gate independently confirms the suite is no longer a refusal source: its sole refusal
is at `W342C_GATE_RECEIPT.json:650-655`; W346 previously recorded `CONTRACT_SELFTEST_RED` with all
seven ids at `W346_GATE_RECEIPT.json:655-667`.

## Frozen legacy replay

The authorized no-write replay used the digest-checked frozen executor and compared both surfaces
for all 17 RED/GREEN rows. The verifier loads and digest-checks that driver at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1638-1681`
and compares canonical live bytes with baseline bytes at `verify_bceg.py:1684-1732`.

```text
SURFACES_EQUAL=34 MISMATCH=0 SKIPPED=0
```

The canonical receipt corroborates producer `KERNEL_1`, 17 scenarios, MATCH, and 34 surfaces
(`W342C_GATE_RECEIPT.json:193-198`). No baseline file was generated or rewritten.

## Canonical gate - invoked once

Exactly one invocation was made from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W342C_GATE_RECEIPT.json
EXIT_CODE=2
```

The exit is the expected non-accepting result. The refusal list, quoted verbatim, is
(`W342C_GATE_RECEIPT.json:650-655`):

```json
[
  {
    "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
    "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
  }
]
```

`CONTRACT_SELFTEST_RED` is absent, provenance is MATCH with zero changed expected paths, and the
receipt reports no acceptance blockers (`W342C_GATE_RECEIPT.json:2-3,117-126,650-655`).

## Discrepancies

1. The first suite attempt from repository root collected 13 import errors because `mtc_v2` was not
   on that working directory's import path. The repository's established command is run from
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` (`W346_REPORT.md:80-90`); rerunning there produced
   the required seven RED failures. No file changed during the incorrect invocation.
2. The product-stage output guide ordinarily requires a `HANDOFF.md` update
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/OUTPUTS.md:6-8`), and the checked lane mirror ordinarily asks
   for a row before the first write (`MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:14-25`). The
   lane's stricter exact-path fence permits only contract self-tests and requires only the receipt
   and report in its commit (`C:\tmp\LANE_PROMPTS_20260828\LANE_W342C_PROVENANCE_SELFTESTS_REANCHOR.md:5-6,30-32`),
   while common clause C-5 forbids every unnamed path (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-31`).
   Therefore neither repository metadata file was changed; the write-lane facts are recorded in
   this report.

No result discrepancy or additional gate refusal was found. Finding count: **0**.
