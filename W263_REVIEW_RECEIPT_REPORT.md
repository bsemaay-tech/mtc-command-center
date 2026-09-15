# W263 review-receipt validation report

## Verdict

PASS. `full-gate` now preserves the existing missing-file refusal and validates a present section-16
receipt before evaluating acceptance. Invalid receipts produce
`SEMANTIC_COVERAGE_REVIEW_INVALID`; the valid synthetic receipt clears only that blocker
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2618-2652`).

## Schema and documentation

The added JSON Schema is closed and requires the fixed receipt id, reviewer, measured identities,
six keyed items, empty unresolved list, owner ratification, and signing time
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.json:2-18`,
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.json:50-130`). Its item object closes disposition, evidence paths, and notes
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.json:164-190`).

The sibling documentation preserves all six live section-16 item texts in order
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.md:7-17`)
and documents identity measurement plus the #5-through-#9 ratification chain
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.md:26-40`).

## Validator diff

The gate measures worktree `HEAD`, the `mtc_v2/core` tree, bundle seal, anchor SHA-256, baseline
manifest SHA-256, and live design SHA-256/version
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:184-237`).
The receipt validator checks exact members, reviewer independence, all measured identities, exactly
six items, the closed disposition domain, `NOT_VERIFIED`, `REFUSED`, evidence existence, empty
unresolved items, ratification, and timezone-qualified signing time
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:240-375`). `main()` retains
`SEMANTIC_COVERAGE_REVIEW_MISSING` for absence and inserts the member-naming invalid refusal for a
present bad receipt before the acceptance predicate
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2618-2652`).

## RED and GREEN evidence

The five tests drive the public `main()` full-gate seam against a temporary root; they never create
the real receipt (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:47-123`,
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:126-201`).

Pre-edit command and measured output:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k semantic_coverage_review -q
FFFF.
4 failed, 1 passed, 98 deselected in 0.24s
```

The empty file, missing item, `REFUSED` item, and stale `HEAD` were incorrectly accepted; the fully
valid synthetic receipt was the passing control. Those four failure expectations correspond to the
four invalid-variant tests (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:126-186`),
and the valid control is at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:188-201`.

Post-edit targeted command and measured output:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k semantic_coverage_review -q
.....
5 passed, 98 deselected in 0.26s
```

Final contract-selftest command and measured output:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -q
103 passed in 1.96s
```

## Canonical full-gate output

Exactly one canonical run was made, as authorized by the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W263_REVIEW_RECEIPT_CHECK.md:47-49`):

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate \
  --root C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2 \
  --baseline-root C:\tmp\P012_BASELINE_RUN

claim_label: BOUNDED_CORRECTION_EVIDENCE_REFUSED
catalog_counts: RED=9, GREEN=8, PROBE=10
legacy_event_order_map_pin.status: MATCH
legacy_event_order_map_pin.sha256: 0c8a04ddd671b1c9c5585b93369a1341d93bd50f01a4fa14dd8d74beab179862
refusals: 17
  1 SEMANTIC_COVERAGE_REVIEW_MISSING
  6 PROBE_NOT_DETECTED
 10 PROBE_DIGEST_UNPINNED
```

The result is the same 17-refusal shape previously recorded for W258: one review refusal, six
not-detected probes, ten unpinned probe digests, and a matching legacy-order pin
(`C:\tmp\LANE_PROMPTS_20260828\DETECT_DS92_HARNESS.md:57-58`). The receipt path remains absent,
so the first refusal stayed `SEMANTIC_COVERAGE_REVIEW_MISSING`, as required by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W263_REVIEW_RECEIPT_CHECK.md:47-48`).

## Counts

- Schema files added: 2
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.json:1-191`,
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.md:1-40`).
- Validator/selftest files changed: 2
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:184-375`,
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:47-201`).
- Required receipt variants: 5; final targeted result: 5 passed
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:126-201`).
- Final contract selftests: 103 passed (`W263_REVIEW_RECEIPT_REPORT.md:64-68`).
- Canonical catalog counts: 9 RED, 8 GREEN, 10 PROBE; refusals: 17 (measured console output in
  `W263_REVIEW_RECEIPT_REPORT.md:75-88`).
- Discrepancies: 1 (below).

## Discrepancies

1. The lane prompt names design v1.10 and cites section 16 at lines 588-599
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W263_REVIEW_RECEIPT_CHECK.md:15-18`), but the live design
   heading is v1.11 (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1`) and section 16 is at
   lines 620-631 (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:620-631`). The six item
   texts are unchanged and were copied from the live lines 624-629. The contract manifest still
   records the older v1.10 design pin
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-18`);
   it was not edited because manifest bytes are explicitly out of scope
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W263_REVIEW_RECEIPT_CHECK.md:6-8`). The validator therefore
   measures the live design file and parses its live heading
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:211-236`).

## Commits

- Starting HEAD: `8622445b95bbf309d8036d1a06b960d3b0e73627`.
- Implementation: `eeaf7cff1a56af19d29c60b605068bdb09c5a313`.
- Branch: `feature/wp-p0-12-corrected-vnext-20260831`; no push was performed, matching the lane's
  branch and push fence (`C:\tmp\LANE_PROMPTS_20260828\LANE_W263_REVIEW_RECEIPT_CHECK.md:4-8`,
  `C:\tmp\LANE_PROMPTS_20260828\LANE_W263_REVIEW_RECEIPT_CHECK.md:47-49`).

## Explicit paths

- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.json`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.md`
- `W263_REVIEW_RECEIPT_REPORT.md`
