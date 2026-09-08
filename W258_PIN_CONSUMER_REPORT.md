# W258 Pin Consumer Report

## Verdict and canonical refusal list

**IMPLEMENTED AND SELF-QA GREEN; canonical gate remains honestly REFUSED by 17 expected
non-pin blockers.** The one authorized canonical run returned exit 2 with
`BOUNDED_CORRECTION_EVIDENCE_REFUSED`. Its receipt recorded
`legacy_event_order_map_pin.status = MATCH` and digest
`0c8a04ddd671b1c9c5585b93369a1341d93bd50f01a4fa14dd8d74beab179862`; that is the digest pinned
by both refreshed bundle records
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:791-862`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:79-85`).
`LEGACY_EVENT_ORDER_MAP_PIN_MISSING` and `LEGACY_EVENT_ORDER_MAP_PIN_MISMATCH` were absent from the
gate refusal list. The implemented receipt field is emitted by the comparison pipeline
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2201-2206,2255-2265`).

The refusal list below is quoted in emitted order from that single run. It contains one required
semantic-review refusal, six probe-detection refusals, and ten probe-digest refusals. Those are the
only classes permitted by the lane stopping rule
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W258_PIN_CONSUMER.md:43-45`).

1. `{"check_id":"SEMANTIC_COVERAGE_REVIEW_MISSING","detail":"C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"}`
2. `{"check_id":"PROBE_NOT_DETECTED","measured_failed_check":"CORRECTED_EXPECTATION","measured_first_changed_node":"/EVENT_SURFACE/cash_events/0/signed_delta","scenario_id":"PROBE-P012-01-A"}`
3. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"50fc3ce1da1ca51feafc44dcd3c537e31d5547eec8c6f854f7260f80f8b8c4c8","modified_copy_digest":"0f956819c8b5d2a3a9c1776420f117b050b662fb1ff0aa1f63d819a382b84aca","scenario_id":"PROBE-P012-01-A"}`
4. `{"check_id":"PROBE_NOT_DETECTED","measured_failed_check":"CORRECTED_EXPECTATION","measured_first_changed_node":"/EVENT_SURFACE/cash_events/0/signed_delta","scenario_id":"PROBE-P012-01-B"}`
5. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"8686e9c8f5a8af557f9ecae1b0cf6ba81e6b0af9ee50af303f5ea48c4efef07a","modified_copy_digest":"e5fc81ec6bac4b93e490ffc538586a253423003f2cd3930331b67e61a5d82f08","scenario_id":"PROBE-P012-01-B"}`
6. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"80a66bec7ea77b64897820c4a429e687a2c20e2b90c4860c34ac01ad98de5d5e","modified_copy_digest":"34e963a8b75209f7a8ab77aeb3d3834251f1bc6847cc2875ec6ba36275e3df25","scenario_id":"PROBE-P012-02-A"}`
7. `{"check_id":"PROBE_NOT_DETECTED","measured_failed_check":"RECORD_IDENTITY_PREFLIGHT","measured_first_changed_node":"core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json","scenario_id":"PROBE-P012-03-A"}`
8. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"d2ec9000ed503947e4b86893b2a9b0cc258c765cecfb5b638a99840cb9dd1ebe","modified_copy_digest":"35193efcfc568ec582e430b0acdc35fa4bcc3e7866313ad9f4798fd2e4e0d304","scenario_id":"PROBE-P012-03-A"}`
9. `{"check_id":"PROBE_NOT_DETECTED","measured_failed_check":"CORRECTED_EXPECTATION","measured_first_changed_node":"/EVENT_SURFACE/cash_events/0/signed_delta","scenario_id":"PROBE-P012-04-A"}`
10. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"e2c09190b4e32c0f9605d5cc54ad26957b5292e9e8cef49d097070e85892b5dc","modified_copy_digest":"d6082460482da78706d50b3c52176f0bba8fadbc1492456b721178daa84196f8","scenario_id":"PROBE-P012-04-A"}`
11. `{"check_id":"PROBE_NOT_DETECTED","measured_failed_check":"CORRECTED_EXPECTATION","measured_first_changed_node":"/EVENT_SURFACE/cash_events/0/signed_delta","scenario_id":"PROBE-P012-05-A"}`
12. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"7862007188811445a3a7df11063e36dd5048f924c1af9259e246afd0256ae494","modified_copy_digest":"1336f129f33de9ea1c4866fce91077e8a55e03e30266e56e9ca20dc5b178ed54","scenario_id":"PROBE-P012-05-A"}`
13. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"4bd13c499516a61c12313da4fdaba2c122b37782911893f0a81fcb0ee794d67e","modified_copy_digest":"b06895e2543d4f768563d618fe99669f788a1fbaddf317d81d5553c84f71900b","scenario_id":"PROBE-P012-05-B"}`
14. `{"check_id":"PROBE_NOT_DETECTED","measured_failed_check":"CORRECTED_EXPECTATION","measured_first_changed_node":"/EVENT_SURFACE/cash_events/0/signed_delta","scenario_id":"PROBE-P012-06-A"}`
15. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"427b29ce60b21ce0a261f35c468392b050d38366b3c986c676adeea43f8e13d7","modified_copy_digest":"ad1ec938b0654ba58bc8bc90e9fad1a9781a2070b7f3951794181deb7fb6450c","scenario_id":"PROBE-P012-06-A"}`
16. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"f9897b826a9657e3937bcb794a0d59df0c6021a4e729edad3e3608f6f7c34914","modified_copy_digest":"dbef7fad26afb8c40beb049770bf867f4a492cb10025a629341eb3fef1b1b1bb","scenario_id":"PROBE-P012-07-A"}`
17. `{"check_id":"PROBE_DIGEST_UNPINNED","modification_manifest_digest":"e466e79458bcc5368b2f9c2ecb0b314bc0825f71638d39327a1842031f446a9f","modified_copy_digest":"f97ce0655b57fee069a161b6584534e299d19253eac4c56aa5da0197f03a62c6","scenario_id":"PROBE-P012-08-A"}`

Canonical command, run once from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` as explicitly authorized by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W258_PIN_CONSUMER.md:3-5,43-45`):

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
exit=2
claim_label=BOUNDED_CORRECTION_EVIDENCE_REFUSED
legacy_event_order_map_pin={"legacy_event_order_map_sha256":"0c8a04ddd671b1c9c5585b93369a1341d93bd50f01a4fa14dd8d74beab179862","status":"MATCH"}
computed_legacy_event_order_map_digest=0c8a04ddd671b1c9c5585b93369a1341d93bd50f01a4fa14dd8d74beab179862
catalog_counts={"GREEN":8,"PROBE":10,"RED":9}
scenario_receipts=17
probe_receipts=10
refusal_count=17
```

## Scope, lane, and safety

This was a T1 non-economic verifier change on branch
`feature/wp-p0-12-corrected-vnext-20260831`, worktree `C:\WP012BUILD`, with this session as the only
writer. The lane fixes those identities and authorizes only the harness, its selftests, the three
mechanical bundle-copy paths, and this report
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W258_PIN_CONSUMER.md:4-8,49-52`). No live, scheduled, host,
broker, venue, deployment, credential, or network endpoint was contacted. No Pine, adapter,
baseline, golden, catalog, input, kernel, or seal-member byte was changed. The only execution beyond
local selftests was the single explicitly authorized canonical verifier run, which read the frozen
baseline and exercised the local verifier and its cataloged probe rows.

Exact implementation write set:

- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256`
- `W258_PIN_CONSUMER_REPORT.md`

No push, merge, pull request, rebase, destructive Git action, or `master` write was performed, as
required by the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W258_PIN_CONSUMER.md:5-8,46-47`).

## Mechanical bundle refresh

Source bundle: `C:\tmp\P012_CONTRACT_TABLES_W127\`. The manifest and anchor were copied as exact
bytes; their staged Git blob OIDs independently equalled the source blob OIDs. The sidecar value was
mechanically changed to the refreshed anchor's SHA-256 plus LF, matching the W246 method required by
the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W258_PIN_CONSUMER.md:25-27`).

| Repository file | Before SHA-256 | After SHA-256 | Source/content verification |
|---|---|---|---|
| `CONTRACT_TABLES_MANIFEST.json` | `974fca3278832c2a565e626e3f6ed385fcae3ac64d2141e3398d5fa29d63fc77` | `b1e73cf2b668854515a99ef4f9ea8836413a71354b437301d79f451eea8c3061` | exact source bytes; index/source blob `a7598bb590250dd247fe726c6bf924de7e4107ad` |
| `implementation_anchor.json` | `343aa91b2bcd5f3087f3d4170f330047ab72c6992f38f253e1376904b0859ce8` | `e2c72b1283fd7ff75ea0acee950ca82710c1ffcb6eab5e46eb0fa620c1ffca38` | exact source bytes; index/source blob `7efe5b8df01755fbcfd24fd00ed36d9a345ea587` |
| `implementation_anchor.json.sha256` | `d64cb184873c89db32931f70d4927ea6fa4f6a31b7ffab0cf67489991577709c` | `4f1203f2672b727169e17edb7f7f55e65d0fc92b37668c47a3c9f640676ff819` | content is refreshed anchor digest `e2c72b12...ca38` plus LF |

`EXPECTED_SEAL_SHA` measured
`4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461` before and after refresh,
and the refreshed anchor records the same value
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:543-556,779-788`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-4,73-85`).
The source manifest explicitly records `files_changed: []`, the added pin member, and byte identity
for everything else
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:779-788`).

## Implementation diff

`consume_legacy_event_order_map_pin()` now reads the authenticated manifest member, compares its
digest to the map computed from the current baseline, compares the pinned and computed maps over
their complete key union, reports the first differing key, and finally checks the anchor digest
against the manifest digest
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2135-2197`).
The pipeline consumes that result, includes its receipt, and inserts only conditional pin blockers
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2201-2206,2255-2265`).

Measured commit diff:

- Harness + selftests: 2 files, 232 insertions, 1 deletion.
- Bundle refresh: 3 files, 104 insertions, 5 deletions.
- `git diff --check`: clean before both commits.

The three required tests construct an independent synthetic pin fixture, remove the member, alter
one digest hex character, and flip one map entry to `LEGACY_SEQUENCE_FIELD_V1` while leaving its
digest unchanged
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:122-165,209-302`).
The missing-pin test also proves that an exact match clears the blocker and that a manifest/anchor
digest disagreement refuses
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:209-253`).

## RED-to-GREEN evidence

The focused command was executed first with only the three new tests present and the pre-edit
harness still inserting its unconditional blocker. All three tests failed at the same absent
`legacy_event_order_map_pin` receipt field, proving that the pre-edit harness did not distinguish
the three variants. This is the required pre-edit failure set
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W258_PIN_CONSUMER.md:39-42`).

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k "legacy_event_order_pin" -vv
collected 98 items / 95 deselected / 3 selected
FAILED test_legacy_event_order_pin_missing_is_distinct_and_match_clears_blocker - KeyError: 'legacy_event_order_map_pin'
FAILED test_legacy_event_order_pin_digest_modified_copy_is_mismatch - KeyError: 'legacy_event_order_map_pin'
FAILED test_legacy_event_order_pin_map_modified_copy_names_first_key - KeyError: 'legacy_event_order_map_pin'
3 failed, 95 deselected in 0.24s
```

The identical command after the consumer edit passed all three tests:

```text
collected 98 items / 95 deselected / 3 selected
PASSED test_legacy_event_order_pin_missing_is_distinct_and_match_clears_blocker
PASSED test_legacy_event_order_pin_digest_modified_copy_is_mismatch
PASSED test_legacy_event_order_pin_map_modified_copy_names_first_key
3 passed, 95 deselected in 0.14s
```

## Contract selftests and counts

Final contract suite:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
226 passed in 1.91s
```

The first full-suite run exposed one existing pipeline unit fixture that mocked catalog/seal
validation but did not create the newly consumed manifest and anchor paths: `225 passed, 1 failed`.
The fixture was completed with a matching synthetic empty-map pin
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:342-378`),
then the exact full command passed 226/226.

Built-in non-accepting selftest:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest
exit=0
checks=18: 3 PASS, 14 DETECTED, 1 DETECTED:/a/1
```

The built-in selftest remains explicitly labelled `NON_ACCEPTING_SELFTEST` by the harness
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2270-2322`).

## Commits

- `4db4bef5` — `fix(mtc-v2): consume legacy event order map pin` — harness + tests.
- `2713a5fd` — `chore(mtc-v2): refresh contract bundle seal 9` — exact manifest/anchor refresh + mechanical sidecar.
- Report commit: committed separately after the two substantive SHAs; its SHA is necessarily
  reported in the final chat because a commit cannot contain its own hash.

Every staged set used explicit paths. No `git add .` or `git add -A` was used.

## Discrepancies

1. The lane says the unconditional blocker was around `verify_bceg.py:1370`
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W258_PIN_CONSUMER.md:19-21`). At the actual pre-edit branch
   head, after intervening W255/W256 changes, it was at line 2190. The behavior matched the prompt;
   only the approximate line reference had drifted.
2. No behavioral, digest, scope, or expected-refusal discrepancy was measured. The canonical gate
   produced only the semantic-review and probe-row refusal classes permitted by the prompt
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W258_PIN_CONSUMER.md:43-45`).

## Finding count

- Unexpected implementation or scope findings: **0**.
- Expected canonical refusals: **17** (1 semantic-review, 6 probe-detection, 10 probe-digest).
- Recorded prompt/repository discrepancies: **1**, line-location drift only.
