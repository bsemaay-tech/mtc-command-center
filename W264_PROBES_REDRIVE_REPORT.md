# W264 Probes Re-drive Report — Seal #10

## Verdict and refusal list

**IMPLEMENTED AND SELF-QA GREEN; canonical gate honestly REFUSED only on the missing semantic
coverage review.** Final probe mode measured **10/10 DETECTED**, **10/10 canonical variant-tree
digests MATCH**, and **10/10 modification-manifest digests MATCH**. The one canonical full-gate run
returned exit 2 with `BOUNDED_CORRECTION_EVIDENCE_REFUSED`, while its comparison pipeline reported
`acceptance_reachable: true`, zero acceptance blockers, 17 scenario receipts, and 10 DETECTED probe
receipts. The bundle itself declares that the section-16 review is pending and required before
acceptance
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:679-682`).

Exact emitted refusal list, in emitted order:

```json
[
  {
    "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
    "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
  }
]
```

This is T1 non-economic verifier work, not an acceptance verdict. The branch is
`feature/wp-p0-12-corrected-vnext-20260831` in `C:\WP012BUILD`, exactly as authorized by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W264_PROBES_REDRIVE_SEAL10.md:3-9`). No live, scheduled,
broker, venue, host, network, credential, deployment, Pine, adapter, backtest, optimization, server,
launcher, baseline-generation, or trading action occurred. No kernel, golden, input, baseline, or
seal byte changed. Nothing was pushed or merged.

## Mechanical bundle refresh

Source: `C:\tmp\P012_CONTRACT_TABLES_W127\`. Before copying, all 19 `files[]` members were
re-hashed and re-sized: **19 present, 0 digest mismatches, 0 size mismatches**. SHA-256 over the
1,996-byte payload formed from LF-joined, ordinally sorted `path:sha256` lines recomputed to
`d763f62f9a423d2c3ca0887224d91e520c5bb1849aaa1958df1e3bb1d46dae29`, equal to both recorded
seal values (`CONTRACT_TABLES_MANIFEST.json:674-688`). The manifest identifies this as re-seal #10,
names the ten pinned probes, and pins design v1.11 (`CONTRACT_TABLES_MANIFEST.json:923-944`).

The four bundle files were copied byte-for-byte. The detached anchor sidecar was mechanically
re-derived as the lowercase SHA-256 of the refreshed anchor plus one final LF; its content is the
anchor digest at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`.

| Repository file | Before SHA-256 | After SHA-256 | Verification |
|---|---|---|---|
| `contracts/scenario_catalog.json` | `f8e788d808f26c427eaefdd3f521998b0fdcea57a469792792abab260efea603` | `941da56a0377c77bd10d03f5ecba899714e36fdef6c1e97e68bd240519ea6de9` | exact source bytes, 46,256 bytes |
| `contracts/CONTRACT_TABLES_MANIFEST.json` | `b1e73cf2b668854515a99ef4f9ea8836413a71354b437301d79f451eea8c3061` | `95cfe0594feb4d49159693fe674b7f07a1b35e2355722f26f67a9c79d73f53c3` | exact source bytes, 67,035 bytes |
| `contracts/implementation_anchor.json` | `e2c72b1283fd7ff75ea0acee950ca82710c1ffcb6eab5e46eb0fa620c1ffca38` | `8c60bd3fd13c9f3586d79e9adab63ab3bac445023d0aa54a7d9a7c1295775d51` | exact source `IMPLEMENTATION_ANCHOR_DRAFT.json` bytes, 6,773 bytes |
| `contracts/implementation_anchor.json.sha256` | `4f1203f2672b727169e17edb7f7f55e65d0fc92b37668c47a3c9f640676ff819` | `35fe2567da7f4f2186b0da6699f0d8493160247ba2f4b9b28b629d348536cebc` | content = refreshed anchor digest plus LF, 65 bytes |
| `contracts/DERIVATIONS.md` | `a8440a1250fed65e77ed760a0ab16db889592e737a731d12aa823f65fcc4ad50` | `73bce8e91a8c0a2b44dbc8bf6b766882f56d635d6f083826e74b37a7715897f3` | exact source bytes, 277,385 bytes |

The refreshed catalog contains exactly 10 PROBE rows. Every row has a 64-hex
`modified_copy_digest`, a 64-hex `modification_manifest_digest`,
`expected_first_changed_node`, `comparator_first_differing_node`, and `design_lines`; the ten row
spans are `scenario_catalog.json:737-753,758-774,779-795,800-816,821-837,842-858,863-879,884-900,905-921,926-942`.
The manifest independently records the same ten digest pairs
(`CONTRACT_TABLES_MANIFEST.json:619-669`). Refresh commit:
`862b97851ec4c080182d1f385a1ff510d6b8ce57`.

## v1.11 rule and driver disposition

The current design retains the v1.11 amendment verbatim:

> A probe is `DETECTED` only when the real top-level gate refuses before an accepting receipt, the
> failed check id equals `expected_failed_check`, and `expected_first_changed_node` is in the
> complete changed-node/path set. The receipt records the traversal-first node separately as
> `comparator_first_differing_node`.

The authoritative text and UTF-8-key / ascending-index traversal rule are at
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:481-493`; the detection-row interpretation is
at `:568-571`, and the accepting-receipt condition is at `:583-586`.

The pre-change driver did not conform: it compared the child's first node for exact equality with
the catalog target. W262 had already recorded that mismatch and the later implementation duty
(`C:\tmp\P012_CONTRACT_TABLES_W127\W262_PROBE_ROWS_REPORT.md:251-254,299-307`). The new driver:

- collects every changed corrected-surface node in traversal order while preserving the existing
  first-difference wrapper (`verify_bceg.py:994-1060`);
- requires the v1.11 comparator member in every PROBE catalog row (`verify_bceg.py:1363-1371`);
- carries the complete changed-node list through the child receipt and records its first member as
  `comparator_first_differing_node` (`verify_bceg.py:1810-1828`);
- validates the child list and applies refusal + exact check id + target-membership as the DETECTED
  predicate (`verify_bceg.py:2028-2068`).

The catalog, not the historical modification manifest, is now the authority for the current target
node. The modification manifest remains closed-schema and still binds probe id, target kind, copy
path, expected check, and one modification, but its pre-v1.11 node label is not compared to the
catalog target (`verify_bceg.py:1507-1534`). Driver/test commit:
`73c0b911c8fdc4d16234ef42821ed3ee397609a3`.

## RED-to-GREEN evidence

The new focused self-test uses `PROBE-P012-08-A`, where the catalog target funding node is later than
the comparator-first cash node, drives the real child entrypoint, and requires DETECTED plus both
node identities (`test_verify_bceg.py:664-694`).

Exact focused command before the driver edit:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k "target_membership_not_first_node" -vv
collected 104 items / 103 deselected / 1 selected
FAILED test_probe_detection_uses_target_membership_not_first_node
E       AssertionError: assert 'NOT_DETECTED' == 'DETECTED'
1 failed, 103 deselected in 0.75s
```

Exact focused command after the driver edit (run together with the carried probe-driver test):

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k "target_membership_not_first_node or probe_driver_rejects_identity" -vv
collected 104 items / 102 deselected / 2 selected
PASSED test_probe_driver_rejects_identity_copy_and_detects_modified_copy
PASSED test_probe_detection_uses_target_membership_not_first_node
2 passed, 102 deselected in 2.89s
```

This is discriminating RED/GREEN evidence against the exact old behavior, not a simulated helper
result.

## Digest verification

Canonical method: recursively enumerate every regular file in UTF-8 byte-sorted relative-path
order; hash each file's exact bytes; serialize `{digest_method, files}` as sorted-key compact UTF-8
JSON with a final LF; and SHA-256 those canonical bytes (`verify_bceg.py:394-413`). Before execution,
the driver requires the stored canonical tree manifest to equal the recomputed manifest and requires
its canonical digest to match the tree-manifest file, the modification manifest's two tree pins, and
the catalog's tree pin. It separately hashes the modification manifest's exact bytes and compares
that digest with the catalog pin. Any mismatch raises `PROBE_CATALOG_DIGEST_MISMATCH`
(`verify_bceg.py:1549-1579`).

Final probe mode produced `PROBE_DIGEST_MATCH` on every row:

| Probe | Variant-tree digest | Modification-manifest digest | Result |
|---|---|---|---|
| `PROBE-P012-01-A` | `0f956819c8b5d2a3a9c1776420f117b050b662fb1ff0aa1f63d819a382b84aca` | `50fc3ce1da1ca51feafc44dcd3c537e31d5547eec8c6f854f7260f80f8b8c4c8` | MATCH |
| `PROBE-P012-01-B` | `e5fc81ec6bac4b93e490ffc538586a253423003f2cd3930331b67e61a5d82f08` | `8686e9c8f5a8af557f9ecae1b0cf6ba81e6b0af9ee50af303f5ea48c4efef07a` | MATCH |
| `PROBE-P012-02-A` | `34e963a8b75209f7a8ab77aeb3d3834251f1bc6847cc2875ec6ba36275e3df25` | `80a66bec7ea77b64897820c4a429e687a2c20e2b90c4860c34ac01ad98de5d5e` | MATCH |
| `PROBE-P012-03-A` | `35193efcfc568ec582e430b0acdc35fa4bcc3e7866313ad9f4798fd2e4e0d304` | `d2ec9000ed503947e4b86893b2a9b0cc258c765cecfb5b638a99840cb9dd1ebe` | MATCH |
| `PROBE-P012-04-A` | `d6082460482da78706d50b3c52176f0bba8fadbc1492456b721178daa84196f8` | `e2c09190b4e32c0f9605d5cc54ad26957b5292e9e8cef49d097070e85892b5dc` | MATCH |
| `PROBE-P012-05-A` | `1336f129f33de9ea1c4866fce91077e8a55e03e30266e56e9ca20dc5b178ed54` | `7862007188811445a3a7df11063e36dd5048f924c1af9259e246afd0256ae494` | MATCH |
| `PROBE-P012-05-B` | `b06895e2543d4f768563d618fe99669f788a1fbaddf317d81d5553c84f71900b` | `4bd13c499516a61c12313da4fdaba2c122b37782911893f0a81fcb0ee794d67e` | MATCH |
| `PROBE-P012-06-A` | `ad1ec938b0654ba58bc8bc90e9fad1a9781a2070b7f3951794181deb7fb6450c` | `427b29ce60b21ce0a261f35c468392b050d38366b3c986c676adeea43f8e13d7` | MATCH |
| `PROBE-P012-07-A` | `dbef7fad26afb8c40beb049770bf867f4a492cb10025a629341eb3fef1b1b1bb` | `f9897b826a9657e3937bcb794a0d59df0c6021a4e729edad3e3608f6f7c34914` | MATCH |
| `PROBE-P012-08-A` | `f97ce0655b57fee069a161b6584534e299d19253eac4c56aa5da0197f03a62c6` | `e466e79458bcc5368b2f9c2ecb0b314bc0825f71638d39327a1842031f446a9f` | MATCH |

## Ten-probe result

Final command:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode probe --baseline-root C:\tmp\P012_BASELINE_RUN
exit=0
claim_label=NON_ACCEPTING_PROBE_EVIDENCE
catalog_counts={"GREEN":8,"PROBE":10,"RED":9}
probe_blockers=[]
```

| Probe | Expected check | Expected node | Measured check | Comparator-first node | Outcome |
|---|---|---|---|---|---|
| `PROBE-P012-01-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | DETECTED |
| `PROBE-P012-01-B` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | DETECTED |
| `PROBE-P012-02-A` | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | `/RESULT_SURFACE/admitted` | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | `/RESULT_SURFACE/admitted` | DETECTED |
| `PROBE-P012-03-A` | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | DETECTED |
| `PROBE-P012-04-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | DETECTED |
| `PROBE-P012-05-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | DETECTED |
| `PROBE-P012-05-B` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | DETECTED |
| `PROBE-P012-06-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/exit_id` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | DETECTED |
| `PROBE-P012-07-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fee_events/1/liquidity_role` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/1/signed_delta` | DETECTED |
| `PROBE-P012-08-A` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | DETECTED |

Measured summary: **10 DETECTED, 0 NOT_DETECTED, 0 COULD_NOT_EVALUATE; 0 probe blockers.**

## Canonical full gate

The full gate was run exactly once, after the successful final probe-mode run:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
exit=2
claim_label=BOUNDED_CORRECTION_EVIDENCE_REFUSED
acceptance_reachable=true
catalog_counts={"GREEN":8,"PROBE":10,"RED":9}
scenario_receipts=17
probe_receipts=10
acceptance_blockers=[]
refusal_count=1
refusals=[{"check_id":"SEMANTIC_COVERAGE_REVIEW_MISSING","detail":"C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"}]
```

The refusal matches the manifest's explicit pending-review state
(`CONTRACT_TABLES_MANIFEST.json:679-682`). No flag or bypass was used.

## Contract self-tests and counts

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
232 passed in 3.14s
exit=0
```

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest
exit=0
claim_label=NON_ACCEPTING_SELFTEST
checks=18: 3 PASS, 14 DETECTED, 1 DETECTED:/a/1
```

`git diff --check` was clean before both commits. The refresh commit changed five authorized paths
(472 insertions, 101 deletions); the driver commit changed the verifier and one self-test file
(121 insertions, 52 deletions). The complete contract suite includes the new discriminating test at
`test_verify_bceg.py:664-694`.

## Commits and explicit paths

- `862b97851ec4c080182d1f385a1ff510d6b8ce57` — `chore(mtc-v2): refresh contract bundle seal 10`
  - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json`
  - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md`
  - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json`
  - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256`
  - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json`
- `73c0b911c8fdc4d16234ef42821ed3ee397609a3` — `fix(mtc-v2): detect probes by changed-node membership`
  - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py`
  - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`
- Report commit — this report is the sole path; its SHA is reported in the final chat because a
  commit cannot contain its own stable hash.

Every commit staged exact paths only and carries `APPROVED-PATCH-PLAN: W264`. No `git add .`,
`git add -A`, `--no-verify`, push, merge, rebase, reset, stash, or destructive Git action was used.

## Discrepancies

1. **The live design file is now v1.12, and the prompt's section locator is wrong.** The lane calls
   the rule v1.11 and directs the reader to a “section 22 probe step”
   (`LANE_W264_PROBES_REDRIVE_SEAL10.md:25-31`). The current design title is v1.12
   (`P012_FRESH_DESIGN_V1.md:1`) because W266 appended an unrelated trade-quantity amendment; the
   v1.11 probe rule is unchanged at section 15.2 lines 481-493, not section 22. The seal-10 manifest
   intentionally pins v1.11 (`CONTRACT_TABLES_MANIFEST.json:612-617,923-944`). The repository and
   exact rule text were followed.
2. **Four pinned modification manifests retain historical node labels.** `PROBE-P012-03-A`,
   `06-A`, `07-A`, and `08-A` each carry the pre-v1.11 value in their one-line
   `modification_manifest.json`, while the re-derived catalog carries the current design target at
   `scenario_catalog.json:813-814,897-898,918-919,939-940`. Those manifests and their pinned digests
   were outside the write fence. The design assigns the current target to the PROBE catalog row
   (`P012_FRESH_DESIGN_V1.md:468-493`), so the driver continues to authenticate the complete
   manifest and its expected check but no longer treats its historical node label as a second
   authority (`verify_bceg.py:1507-1534`).
3. **The first all-ten probe attempt was 9 DETECTED plus one implementation error.** My initial
   full-set collector continued from `PROBE-P012-02-A`'s terminal admission mismatch into fill
   projections that are undefined after admission changes, producing
   `IndexError: list index out of range` and `COULD_NOT_EVALUATE`. I restored the pre-existing
   admission-first terminal behavior, reran the two focused tests GREEN, and reran all ten probes to
   the final 10/10 result above. The failed output is recorded here rather than omitted.
4. **A report commit cannot truthfully embed its own hash.** The lane requires a committed report
   containing commit hashes (`LANE_W264_PROBES_REDRIVE_SEAL10.md:45-49`). The two prior commit hashes
   are embedded above; the report commit SHA is necessarily supplied in the final chat, matching the
   repository's prior W258 handling (`W258_PIN_CONSUMER_REPORT.md`, “Commits”).

## Finding count

- Unresolved implementation findings: **0**.
- Expected canonical refusals: **1**, `SEMANTIC_COVERAGE_REVIEW_MISSING`.
- Recorded discrepancies: **4**; one is a transient implementation error repaired and re-tested,
  one is an immutable historical-label residue handled by authority separation, and two are
  documentation/self-reference facts.
