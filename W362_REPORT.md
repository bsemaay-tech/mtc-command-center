# W362 Report - re-seal #19 copy refresh and canonical gate

## Verdict

The in-repo bundle copies were refreshed byte-for-byte and committed at content commit
`f3f72773934de0f23e0144610ace76a486baab69`. The independently recomputed 19-member seal is
`555075146636af3442424035e2544e73e07961dd14661de9c019e203f6720024`; it matches the source
manifest, `RESEAL19_DONE.txt`, the baseline-consumed seal, and the copied anchor. The receipt also
records that seal and anchor identity
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:573-585`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5`;
`W362_GATE_RECEIPT.json:1998-2005`).

The canonical gate was invoked exactly once and returned 1 after writing `W362_GATE_RECEIPT.json`.
It refused with five entries, not the single predicted entry. Eight of ten probes were `DETECTED`;
two could not evaluate because their modification-manifest digests do not match their catalog
pins. The gate recorded three failed contract self-tests, and a separate same-suite reproduction
measured 322 passed and 3 failed. No refusal was fixed (`W362_GATE_RECEIPT.json:515-727`).

## Preconditions, routing, and scope

The lane requires `RESEAL19_DONE.txt` and `W361_DONE.txt` to exist and read `exit=0`, a clean
worktree, a recorded HEAD, and a recomputed source-bundle seal matching the re-seal marker
(`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:5-9`). Both markers were present and
read `exit=0` (`C:/tmp/LANE_PROMPTS_20260828/RESEAL19_DONE.txt:1`;
`C:/tmp/LANE_PROMPTS_20260828/W361_DONE.txt:1`). The measured start was worktree
`C:\WP012BUILD`, branch `feature/wp-p0-12-corrected-vnext-20260831`, full HEAD
`678815c24951bc684ce324012b6325a34bf886fe`, and empty porcelain status.

All 19 source member hashes and byte counts matched the source manifest. Recomputing SHA-256 over
the LF-joined, lexicographically sorted `path:sha256` rows produced
`555075146636af3442424035e2544e73e07961dd14661de9c019e203f6720024`. The copied manifest records
the same operative seal and unchanged implementation base
`63cfe2dd2dcb3373f2fa18c385f67a1c2d113bb5`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:573-585`).

Primary changes are protected expected economic artifacts under
`MTC_COMMAND_CENTER/01_MTC_PROJECT/**`, so Gate 1 is T0. The exact write paths are the four changed
contract-copy paths in the SHA tables plus `W362_GATE_RECEIPT.json` and this report. Live-dependency
status was none: no broker, venue, host, deploy, Pine, kernel, baseline, or base-anchor path was
touched. The lane authorizes only the named copies and gate evidence, forbids changing the base,
and forbids observe mode (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:11-31`).

## Design-pin measurement

The design file measured SHA-256
`03fdf5952a2365b2de60b55292a1bd50fce8c6c51788c19b59cecc5d8f5b3c94` and 1,843 lines. Both
measurements match the copied manifest's v1.18 whole-file pin and the gate's sealed producer
identity
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-18`;
`W362_GATE_RECEIPT.json:1998-2005`). The design-pin mismatch that motivated this lane is absent.

## Source/destination SHA-256 table

Every row below was measured after copying. All 19 destination members are byte-identical to the
source and match their manifest pins and byte counts
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:62-158`).

| File | Source SHA-256 | Destination SHA-256 | Result |
|---|---|---|---|
| `DERIVATIONS.md` | `9bc0b6bfa442465cee5769a9392270f8b88e6ccb93fae25be542dfd8ec4cc08f` | `9bc0b6bfa442465cee5769a9392270f8b88e6ccb93fae25be542dfd8ec4cc08f` | byte-identical; already current |
| `scenario_catalog.json` | `70da8796451c506d220417c2c80aa4eba9ddef2a57a97219e2a260b4a470f057` | `70da8796451c506d220417c2c80aa4eba9ddef2a57a97219e2a260b4a470f057` | byte-identical; refreshed |
| `golden/corrected_vnext/RULE2-01-GREEN.json` | `03a70ee7d9dbb0c0f7988135efe1577c16b149df8822af94b03cdb96f9c10dbd` | `03a70ee7d9dbb0c0f7988135efe1577c16b149df8822af94b03cdb96f9c10dbd` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-01-RED.json` | `31646561c134e4e6097a43ff1a9ffee8cbcc68439acc05b3947690ab8782a4fb` | `31646561c134e4e6097a43ff1a9ffee8cbcc68439acc05b3947690ab8782a4fb` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-02-GREEN.json` | `59acd8f75d35f384b89417fba4df289ebdf7bf768e4e9b22bf560bbeeaef3dfe` | `59acd8f75d35f384b89417fba4df289ebdf7bf768e4e9b22bf560bbeeaef3dfe` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-02-RED.json` | `9511084b30fb45a710ee56484f443042233ebcc700621f1582efd86bad851425` | `9511084b30fb45a710ee56484f443042233ebcc700621f1582efd86bad851425` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-03-GREEN.json` | `b38a9b65ad965280e93f6763ef0cf95c80b5c1b27774e3e65ecafef210f9524e` | `b38a9b65ad965280e93f6763ef0cf95c80b5c1b27774e3e65ecafef210f9524e` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-03-RED.json` | `7a12c41910edb62a1066e99a6a5306e4974d71edad40af670504f7e10db822b0` | `7a12c41910edb62a1066e99a6a5306e4974d71edad40af670504f7e10db822b0` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-04-GREEN.json` | `e192b8b6dedd8c05ae1055a2d7b2b56ac39fdc173cb2c18ac61567ed82f05fe6` | `e192b8b6dedd8c05ae1055a2d7b2b56ac39fdc173cb2c18ac61567ed82f05fe6` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-04-RED.json` | `65fe5ccefe4d04ae0b360e733b5632903ec29b71887d1ae27de8d6b27c9c05d1` | `65fe5ccefe4d04ae0b360e733b5632903ec29b71887d1ae27de8d6b27c9c05d1` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-05-GREEN.json` | `53ed07441c81bd5d49323a209af4ebee51eddad333f831f60eff802a2140ad23` | `53ed07441c81bd5d49323a209af4ebee51eddad333f831f60eff802a2140ad23` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-05-RED.json` | `6833c49e1d4d48ae7ad36406377358caa5a0387d48d067dfd8f086528b0b8760` | `6833c49e1d4d48ae7ad36406377358caa5a0387d48d067dfd8f086528b0b8760` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json` | `d5eb751edac5bec0de32cc41aae23455b73357d6b73c43ffacd1a1bd3d64ea67` | `d5eb751edac5bec0de32cc41aae23455b73357d6b73c43ffacd1a1bd3d64ea67` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-06-GREEN.json` | `7057c3da1ede144725cb2edfdb34fe8c104bd2fe519fc3ca2af79628652e2ff6` | `7057c3da1ede144725cb2edfdb34fe8c104bd2fe519fc3ca2af79628652e2ff6` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-06-RED.json` | `b734e65a9806dbd9ba48d0b3a3104b9a3a92d008516a9345199c083170707371` | `b734e65a9806dbd9ba48d0b3a3104b9a3a92d008516a9345199c083170707371` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-07-GREEN.json` | `8ebdb0b8dcee9b4430c06af96cc21c5b2beea5c59a6a0fc81b6e4ab757f73bb2` | `8ebdb0b8dcee9b4430c06af96cc21c5b2beea5c59a6a0fc81b6e4ab757f73bb2` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-07-RED.json` | `82d11b9b826df4288e5e96f64d3f1ee6e6b4cf52b1a1b49af50807eb2e84a417` | `82d11b9b826df4288e5e96f64d3f1ee6e6b4cf52b1a1b49af50807eb2e84a417` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | `7e3b886e4899472c0a92c921f8e27e8c172e46d4bb7c8e29ff6c1314aab4ee69` | `7e3b886e4899472c0a92c921f8e27e8c172e46d4bb7c8e29ff6c1314aab4ee69` | byte-identical; already current |
| `golden/corrected_vnext/RULE2-08-RED.json` | `7302ad0eda8a461ce70c19b25264a260fec85bd34aa02bbaf051faba11da8ae3` | `7302ad0eda8a461ce70c19b25264a260fec85bd34aa02bbaf051faba11da8ae3` | byte-identical; already current |

Before copying, `scenario_catalog.json` was the only differing manifest member. `DERIVATIONS.md`
and all 17 goldens were already byte-identical and therefore produced no worktree change. The
manifest's re-seal #19 record likewise names only `scenario_catalog.json` as the changed member
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1016-1026`).

The copied controls and regenerated sidecar also match their sources:

| File | Source SHA-256 | Destination SHA-256 | Result |
|---|---|---|---|
| `CONTRACT_TABLES_MANIFEST.json` | `49697fed0fc0353f637584e1899e6f84d107e366f717631193071b4f1028cbbb` | `49697fed0fc0353f637584e1899e6f84d107e366f717631193071b4f1028cbbb` | byte-identical; refreshed |
| `implementation_anchor.json` from `IMPLEMENTATION_ANCHOR_DRAFT.json` | `56ccbc164ba584e93e98af6c7037661bb17841771e382ad7810d72be30642112` | `56ccbc164ba584e93e98af6c7037661bb17841771e382ad7810d72be30642112` | byte-identical; refreshed |
| `implementation_anchor.json.sha256` | `56ccbc164ba584e93e98af6c7037661bb17841771e382ad7810d72be30642112` | `56ccbc164ba584e93e98af6c7037661bb17841771e382ad7810d72be30642112` | regenerated; matches anchor |

The content commit staged exactly the four changed destinations: the manifest, anchor, anchor
sidecar, and scenario catalog. `git diff --check` returned 0 before commit. Its subject is exactly
`chore(mtc-v2): refresh in-repo bundle copies to re-seal #19 and pin design v1.18 (decisions 153/154/155)`
as directed by the lane (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:20-23`).

## Canonical gate

Exactly one canonical invocation was issued from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W362_GATE_RECEIPT.json
```

The process returned 1 and wrote the requested receipt. The receipt confirms `mode: full-gate`,
17 RED/GREEN scenarios, 10 probe rows, and a refused claim (`W362_GATE_RECEIPT.json:153-158,236`).
`--mode observe` was not invoked, consistent with the lane prohibition
(`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:18-20`).

## Full refusal list - verbatim

The following is the complete `refusals` value copied verbatim from
`W362_GATE_RECEIPT.json:671-727`:

```json
"refusals": [
  {
    "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
    "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
  },
  {
    "check_id": "EXPECTED_PATH_CHANGED_AFTER_BASE",
    "count": 19,
    "detail": "19 expected paths changed after the implementation base",
    "pointer": "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json",
    "pointers": [
      "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json",
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
    "check_id": "PROBE_COULD_NOT_EVALUATE",
    "detail": {
      "check_id": "PROBE_CATALOG_DIGEST_MISMATCH",
      "detail": "PROBE-P012-03-A"
    },
    "scenario_id": "PROBE-P012-03-A"
  },
  {
    "check_id": "PROBE_COULD_NOT_EVALUATE",
    "detail": {
      "check_id": "PROBE_CATALOG_DIGEST_MISMATCH",
      "detail": "PROBE-P012-07-A"
    },
    "scenario_id": "PROBE-P012-07-A"
  },
  {
    "check_id": "CONTRACT_SELFTEST_RED",
    "detail": "3 contract self-tests failed",
    "failing_test_ids": [
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_expected_source_provenance_refuses_expected_path_changed_after_base",
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item3_recorded_exception_lifts_only_the_decision_134_path",
      "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_w305_item8_provenance_refusal_reports_every_unlifted_path"
    ]
  }
],
```

## Probe table

| Probe | Base scenario | Expected failed check | Measured failed check | Expected changed node | Comparator first differing node | Status |
|---|---|---|---|---|---|---|
| `PROBE-P012-01-A` | `RULE2-01-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` |
| `PROBE-P012-01-B` | `RULE2-01-GREEN` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` |
| `PROBE-P012-02-A` | `RULE2-02-GREEN` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/RESULT_SURFACE/admitted` | `/EVENT_SURFACE/cash_events` | `DETECTED` |
| `PROBE-P012-03-A` | `RULE2-03-RED` | `RECORD_IDENTITY_PREFLIGHT` | not produced | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | not produced | `COULD_NOT_EVALUATE` |
| `PROBE-P012-04-A` | `RULE2-04-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` |
| `PROBE-P012-05-A` | `RULE2-05-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` |
| `PROBE-P012-05-B` | `RULE2-05-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `DETECTED` |
| `PROBE-P012-06-A` | `RULE2-06-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/exit_id` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` |
| `PROBE-P012-07-A` | `RULE2-07-RED` | `CORRECTED_EXPECTATION` | not produced | `/EVENT_SURFACE/fee_events/1/liquidity_role` | not produced | `COULD_NOT_EVALUATE` |
| `PROBE-P012-08-A` | `RULE2-08-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` |

Measured total: 8 `DETECTED`, 0 `NOT DETECTED`, and 2 `COULD_NOT_EVALUATE`
(`W362_GATE_RECEIPT.json:515-669`).

## Contract-suite counts

The gate's refusal records exactly three failing test IDs (`W362_GATE_RECEIPT.json:719-726`). A
separate reproduction of the same self-test directory, with the cache provider disabled, returned
the following measured count:

```text
3 failed, 322 passed in 15.82s
```

The three targeted failures were reproduced again in 0.87 seconds. Two tests expected the first
refusal pointer to be
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json`
but measured
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json`.
The third expected two pointers but measured those two plus the RULE2-01-GREEN path. The assertions
that encode the expected values are at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:817-826,924-939,1029-1045`.

## Discrepancies

1. The lane predicts the refusal check-id list is exactly
   `["SEMANTIC_COVERAGE_REVIEW_MISSING"]`
   (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:25-29`). The measured list has
   five entries: `SEMANTIC_COVERAGE_REVIEW_MISSING`, `EXPECTED_PATH_CHANGED_AFTER_BASE`, two
   `PROBE_COULD_NOT_EVALUATE` entries, and `CONTRACT_SELFTEST_RED`
   (`W362_GATE_RECEIPT.json:671-727`).
2. The unexpected provenance refusal reports 19 changed expected paths. Its first pointer is
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json`;
   the two comparison identities are implementation base
   `63cfe2dd2dcb3373f2fa18c385f67a1c2d113bb5` and current content commit
   `f3f72773934de0f23e0144610ace76a486baab69`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:573-585`;
   `W362_GATE_RECEIPT.json:677-701`). No provenance refusal was fixed.
3. `PROBE-P012-03-A` could not evaluate at its modification-manifest pointer
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json`.
   The catalog pin is `d2ec9000ed503947e4b86893b2a9b0cc258c765cecfb5b638a99840cb9dd1ebe`;
   the actual file digest is `a496c97b16db3d219e3b2a7ff0222c70e9ce00fb38f057082a2706fbfc64e578`.
   Its modified-copy tree pin and actual digest both equal
   `35193efcfc568ec582e430b0acdc35fa4bcc3e7866313ad9f4798fd2e4e0d304`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2256-2274`;
   `W362_GATE_RECEIPT.json:567-575`). No probe artifact or catalog pin was changed.
4. `PROBE-P012-07-A` could not evaluate at its modification-manifest pointer
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification_manifest.json`.
   The catalog pin is `ed5bf6bdf3e3c1548a07c56f1bf0702798edb61b28abe1f8abc81f77d9e614f0`;
   the actual file digest is `a872886751d72851f5fbfcba6027377e1d91948972bef99a74ba55126c2033a5`.
   Its modified-copy tree pin and actual digest both equal
   `1259f010f19dd9082fcfbc83632ee19fdd4720e744062e7b577b84ac821d0d88`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2361-2379`;
   `W362_GATE_RECEIPT.json:644-651`). No probe artifact or catalog pin was changed.
5. The lane predicts 10/10 probes `DETECTED` and a green contract suite
   (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:25-29`). The measured values are
   8/10 `DETECTED`, 2/10 `COULD_NOT_EVALUATE`, and a suite result of 322 passed / 3 failed
   (`W362_GATE_RECEIPT.json:515-669,719-726`). The three failures all include the unlifted
   RULE2-01-GREEN provenance path where the tests expected it to be lifted; the exact expected and
   measured pointer values are recorded above. No test or provenance file was changed.
6. The copied manifest's operative `seal_state` and `seal` both carry the re-seal #19 digest, and
   revision history identifies re-seal #19, but `seal.set_by` still says "Lead re-seal act #17"
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:573-586,1016-1026`).
   Byte-for-byte copying was required, so this source-authored residue was preserved.
