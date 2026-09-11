# P012 instrument-record prose correction

- Branch: `feature/p012-record-prose-20260911`
- Worktree: Lead-owned `C:/tmp/P012_RECORD_PROSE_20260911`
- Base: `e42fa192507d77e2d1765702a4a9f54e56ad793f`
- Source instrument SHA-256: `8620f499d7903f5ea801d99f6654f01546ad6638f7c85dad81d441209ff73fb8`
- Proposed instrument SHA-256: `5abb99abbdb9735e95ad1084c706a3c5326fb6bb134e48a79e9bb0992b68316a`

The defects were independently reproduced. `/status` points to the superseded addendum 15 row 36 pending-approval wording instead of the recorded OPEN01 selection at addendum 16 row 42. `/field_basis/price_tick` contradicts the already-approved v1.27 integer exception by claiming a mandatory 10-unit step above 100000. Only those two explanatory strings change.

Initial apply is exactly these four paths:

1. `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json`
2. `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json.sha256`
3. `MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json`
4. `MTC_COMMAND_CENTER/_AI_MEMORY/P012_RECORD_PROSE_20260911.md`

Before applying anything beyond those four, separately enumerate and remeasure these dependent identities:

- Probe: `tests/corrected_vnext/probes/{PROBE-P012-01-A,PROBE-P012-01-B,PROBE-P012-02-A,PROBE-P012-04-A,PROBE-P012-05-A,PROBE-P012-05-B,PROBE-P012-06-A,PROBE-P012-07-A,PROBE-P012-08-A}/kernel/economic_records/instruments/HYPERLIQUID-BTC-PERP-V1.3.json`, each sidecar, and each `modified_tree_manifest.json`.
- Catalog: `tests/corrected_vnext/contracts/scenario_catalog.json`.
- Anchor: `tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json`, `implementation_anchor.json`, and `implementation_anchor.json.sha256`.
- Receipt: `tests/corrected_vnext/contracts/semantic_coverage_review.json`.

There is no core Python, numeric, behavioral, or semantic change. Original baseline34 and R34 acceptance are preserved. The current unit remains NONACCEPTED. Lead owns all writes; no other workers write source.

NEXT ACTION: commit core-only candidate then regenerate dependent probe/evidence identities.

WAITING FOR OWNER: Nothing for existing corrective authority, later genuine Section16 ratification remains separate.

## Core correction and probe refresh in progress
The four-file core correction is committed at 8f3ebe614bf330caf94eadc4566709fa1cda4416, core tree ad06d9723484d7fa7e220096a1ec9247197f7f29. Lead independently verified exactly two changed JSON strings and all 40 existing history rows preserved. No executable core file changed.
The dependent scope is now explicitly all ten probe copies of this production record and its sidecar, each modification manifest and modified-tree manifest, plus scenario_catalog.json: 41 exact paths recorded in external P012_PROSE_PROBES35_20260911/SCOPE.json. The INPUT03 synthetic fault stays byte-identical; its instruments base tree changes because the copied production record changes. Nine kernel probes have been regenerated with the existing hash-verified helper. Original probes/catalog are archived. New status remains NONACCEPTED pending the completed coordinated successor and required review/ratification.
## Lead correction of INPUT03 scope
The preceding 41-path description incorrectly assumed INPUT03 contained the production record. Direct inspection of its two-member tree and verifier proves it contains only its original synthetic record and sidecar. Both stay byte-identical, as do its patch and tree manifest. The necessary correction is solely base_tree_oid in INPUT03/modification_manifest.json and the corresponding catalog modification_manifest_digest. Nine kernel copies still require the production prose plus sidecar refresh. Corrected probe/catalog scope: 38 paths (nine times four, INPUT03 manifest, catalog), with 19 catalog pins changing. Original 41-path scope and rejected never-applied full-directory INPUT03 candidate are retained as failed preparation evidence; no acceptance inferred. R35 output-only reseal attempt A1, prepared prematurely after the Lead QA assertion failed, was never applied and is rejected. A fresh A2 is required after the verified INPUT03 fix.
Lead independently checked all 1,073 currently retained probe member bytes and all ten original patch/modification declarations. No mutant or executable file changed. Included Sol replacement prepares only the two needed metadata files and corrects external reseal-helper prose. Original R34 baseline and accepted receipt remain preserved.

## C35 sealed candidate checkpoint
Applied INPUT03 metadata-only correction after independent verification. Prepared and verified A2 seal 6f44d5beb9e2ed20fae65508bb01a01d1840258dfceb5109c9be20ab615dadd8: all19 sealed members verified; only scenario_catalog changed, 17goldens and DERIVATIONS preserved, both history prefixes exact. The reseal reason's shorthand '19 probe pins total' means 19 CHANGED digest values among the catalog's 20 probe digest fields; INPUT03 modified_copy_digest is unchanged. No extra record/tree files were added. Exact dirty candidate set is 38probe/catalog files, 3seal metadata files and this owned note. Candidate remains NONACCEPTED pending actual baseline35, F35, current independent Section16, owner ratification and required T0/CI. NEXT ACTION: commit sealed C35, run/compare baseline35. WAITING FOR OWNER: Nothing for this local preparation.

## Additional reproduced identity fixture defect
A direct run of selftests/test_economic_records.py::test_production_candidate_bytes_are_copied_exactly_but_remain_incomplete failed only because it pinned the original production JSON digest 8620f499...; the independently verified two-string correction has digest5abb99ab.... Add exactly that selftest path to the corrective scope, replacing only the single old digest literal. This expected identity is independently computed from the approved record bytes, not a kernel output or a new golden. All other assertions, including source lineage and incomplete-production refusal, remain byte-identical. The output-only Grok payload was independently reversed to the original file exactly. Lead owns application; the failed Sol F35 worker is stopped and source remained clean. Fresh F35 replacement is output-only outside the repo. This identity RED/GREEN is separate from any semantic behavior claim.

## F35 prepared and independently verified
C35 baseline35 completed17 scenarios with0 blocked, and Lead independently verified36 output hashes and34 byte-identical semantic surfaces against R34. Manifest3573282558fd8b0ffd5a403b2eb71e3fee0a51b25367b78622ceb15ced857f78. F35 changes only the six enumerated manifest/anchor/sidecar/provenance/selftest/schema identity files; the added production-digest selftest correction is exactly one literal. All histories, prior reason prefixes, golden identities and core behavior are preserved. The declaration remains NOT evidence; actual base/current blob d57b6151c3d91516a780c76097d76870fd3ee8ee was independently rechecked.
The original Sol preparation timed out after PowerShell localized JSON timestamps; its failed status and original output remain preserved. Grok replacement timed out without output. Lead extracted Sol's final already-delegated command without editing it, ran it with process-scoped ConvertFrom-Json DateKind=String, and independently verified every resulting JSON field delta, exact test reversal, source hashes and anchor sidecar. This is recovered mechanical preparation, not a successful worker review. No source writes occurred in failed attempts.
Technical QA: intended old-digest assertion RED, exact replacement GREEN;113 focused tests pass. Current canonical191 hunks include189 byte-identical R34 hunks and only2 changed instrument record/sidecar hunks, with no undocumented row. New Section16 review/ratification remains pending; current work NONACCEPTED.
NEXT ACTION: commit F35, verify current candidate, freeze the actual independent-review packet and obtain current Section16 judgment.
WAITING FOR OWNER: Nothing for current preparation; no new ratification has been inferred.
