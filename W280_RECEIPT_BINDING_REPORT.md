# W280 Receipt Identity Binding Report

## Verdict

PASS. The one specified receipt-lifetime defect is fixed: the receipt records a reviewed commit as
required information and validates its ancestry, while acceptance is bound to the reviewed content
identities. The content set explicitly includes the harness and catalog digests
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:50-63`,
`:244-245`, `:338-351`).

Finding count: **1 defect fixed**. Discrepancy count: **1**, recorded below.

## Binding rule

The signature covers the engine, the answer sheets, the reference and the design as they were;
adding the signature file itself, or a report, does not void it; changing any of those five does.
`worktree_head_commit` remains required information: it must be a 40-character Git OID and must be
an ancestor of the measured `HEAD`, but it is not compared for equality with `HEAD`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.md:30-42`).

The validator freshly measures and compares the `core` tree OID, expected seal SHA-256,
implementation-anchor SHA-256, baseline-manifest SHA-256, design-file SHA-256 and version,
`verify_bceg.py` SHA-256, and `scenario_catalog.json` SHA-256
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:50-63`,
`:184-245`, `:347-351`). The ancestor decision is made by
`git merge-base --is-ancestor <reviewed_commit> <measured_HEAD>`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:249-274`,
`:338-346`).

The closed JSON schema requires both new SHA-256 members and retains the required commit member
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.json:54-62`,
`:65-92`). The synthetic valid receipt contains the complete identity set
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:31-42`,
`:73`).

## Diff

Implementation commit command evidence:

```text
commit 9dc27b4d9e69b8b7399ac9de03953c8cf37b31e4
153  4  MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
9    1  MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.json
7    2  MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.md
48   3  MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py
4 files changed, 217 insertions(+), 10 deletions(-)
```

No kernel, golden, catalog, input, baseline, seal, or review-receipt byte is part of that commit;
the four paths above are the exact implementation scope authorized by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W280_RECEIPT_BINDING.md:6-8`, `:38`).

## Four RED/GREEN tests

The test seam is the real `full-gate` CLI path with a synthetic comparison pipeline. The ancestry
variants use a real temporary two-commit Git repository
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:92-126`,
`:139-188`, `:253-296`).

Pre-fix command and measured result:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k w280 -q
FFFF
4 failed, 104 deselected in 1.29s
```

| Variant | Pre-fix result | Post-fix contract |
|---|---|---|
| Matching content with older ancestor commit | RED: expected accepted return `0`, received refused return `2`; first detail was `reviewed_identities.catalog_sha256: unknown member` | Accepted; the reviewed commit is proven ancestral (`test_verify_bceg.py:253-272`) |
| Commit is not an ancestor | RED: expected the ancestry-specific refusal, received the same unknown-member refusal | Refused with `reviewed_identities.worktree_head_commit: not an ancestor of measured HEAD` (`test_verify_bceg.py:275-296`) |
| Matching HEAD with changed core tree OID | RED: expected the core-identity refusal, received the same unknown-member refusal | Refused with `reviewed_identities.core_tree_oid: does not match measured identity` (`test_verify_bceg.py:299-315`) |
| Harness SHA-256 mismatch | RED: expected the harness-identity refusal, received the same unknown-member refusal | Refused with `reviewed_identities.harness_sha256: does not match measured identity` (`test_verify_bceg.py:318-334`) |

The abbreviated `test_verify_bceg.py` citations in the table mean
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`.

Post-fix command and measured result:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k w280 -q
....
4 passed, 104 deselected in 1.20s
```

## W263 preservation and contract-test counts

W263's five receipt tests remain present at `test_verify_bceg.py:191-250` and `:337-353`.

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k "semantic_coverage_review and not w280" -q
.....
5 passed, 103 deselected in 0.15s

python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
236 passed in 4.00s

python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest
DETECTED=15
PASS=3
TOTAL=18

python -m json.tool mtc_v2/tests/corrected_vnext/contracts/semantic_coverage_review.schema.json
exit code 0

python -m py_compile mtc_v2/tests/corrected_vnext/verify_bceg.py mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
exit code 0

git diff --check
exit code 0
```

The built-in self-test enumerates its checks at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2589-2641`.

## Canonical gate output

The canonical gate was run once as authorized by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W280_RECEIPT_BINDING.md:3-8`, `:37`). Its measured output was
refused only because the review receipt is missing; the pipeline itself reported no acceptance
blockers.

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate
exit code 2
{
  "acceptance_blockers": [],
  "catalog_counts": {
    "GREEN": 8,
    "PROBE": 10,
    "RED": 9
  },
  "claim_label": "BOUNDED_CORRECTION_EVIDENCE_REFUSED",
  "mode": "full-gate",
  "refusals": [
    {
      "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
      "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
    }
  ]
}
```

The missing-receipt branch inserts exactly that refusal before evaluating a receipt
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2695-2708`).

## Commit hashes

- Starting commit: `a943da835dd9e0349f96e2e8461d2c982154b65f`.
- Harness/schema/doc/tests implementation commit:
  `9dc27b4d9e69b8b7399ac9de03953c8cf37b31e4`.
- This report's commit hash is self-referential and therefore cannot be embedded in the report it
  hashes; it is reported in the final chat close after the report commit is created.

## Discrepancies

1. The prompt asks whether a matching-HEAD receipt with a changed core-tree OID "was accepted
   before" (`C:\tmp\LANE_PROMPTS_20260828\LANE_W280_RECEIPT_BINDING.md:31-34`). It was not: the
   pre-fix validator compared every identity, including `core_tree_oid`, with the measured value and
   refused any mismatch
   (`a943da835dd9e0349f96e2e8461d2c982154b65f:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:279-306`).
   The W280 core variant was RED before the fix because the newly required digest members were
   rejected first as unknown; after the fix it reaches and proves the pre-existing core mismatch
   refusal (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:299-315`).
