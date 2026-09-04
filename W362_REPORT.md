# W362 Report — re-seal #20 copy refresh and canonical gate

## Verdict

The authorized in-repo copies were refreshed and committed at content commit
`bdacf8e42399f9a3e9a753ca0ab30e5210ae98cf`. The copied bundle records seal
`9ef73ef6b8d081a3ea3c945a43e69f603db85fe871f5742f360d27a63bb562a0` in both seal locations,
and the copied anchor records the same value
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:572-585`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5`).

The one canonical `full-gate` invocation refused with three entries, not the predicted one. All
10 probes were `DETECTED`. The contract self-test suite was not green: a direct diagnostic rerun of
that suite measured 322 passed and 3 failed; the receipt names the same three failures
(`W362_GATE_RECEIPT.json:499-670,671-712`). No refusal or failing test was fixed.

## Preconditions, routing, and scope

The lane required two `exit=0` markers, a clean non-`master` worktree, a recorded starting HEAD,
and an independently recomputed seal matching the marker
(`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:7-10`). Both markers were present
and read `exit=0` (`C:/tmp/LANE_PROMPTS_20260828/RESEAL20_DONE.txt:1`;
`C:/tmp/LANE_PROMPTS_20260828/W361_DONE.txt:1`). The measured start was branch
`feature/wp-p0-12-corrected-vnext-20260831`, full HEAD
`9f9136bb318ad576d896447d1fd5241bde77d3f7`, and an empty porcelain status.

Primary changes are under `MTC_COMMAND_CENTER/01_MTC_PROJECT/**`, so the routed stage is the MTC
build stage (`CONTEXT_MAP.md:8-10`). Scope is T0 because protected expected economic artifacts were
explicitly authorized for copy refresh. No Pine, kernel, baseline, broker, venue, host, deploy, or
live path was changed. The implementation base was not changed, as the lane required
(`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:13-15`).

The 19 lexicographically sorted `path:sha256` members independently recomputed to
`9ef73ef6b8d081a3ea3c945a43e69f603db85fe871f5742f360d27a63bb562a0`, equal to the marker,
manifest seal state, manifest seal, and draft-anchor value
(`C:/tmp/LANE_PROMPTS_20260828/RESEAL20_DONE.txt:1`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:62-158,572-585`).

The fresh design independently measured SHA-256
`03fdf5952a2365b2de60b55292a1bd50fce8c6c51788c19b59cecc5d8f5b3c94` and 1,843 lines. These
values exactly match the manifest's v1.18 pin and the gate's measured producer identity
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-17`;
`W362_GATE_RECEIPT.json:1982-1989`).

## Refreshed copy SHA-256 table

Every row below was measured from the named source and destination after copying. All 19 manifest
members match the source bytes and the manifest pins
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:62-158`).
The starting worktree was clean; after the copy pass, only `scenario_catalog.json` was modified
among these 19 members. Thus the other 18 members were already byte-identical and remained so.

| Manifest member | Source SHA-256 | Destination SHA-256 | Start action |
|---|---|---|---|
| `DERIVATIONS.md` | `9bc0b6bfa442465cee5769a9392270f8b88e6ccb93fae25be542dfd8ec4cc08f` | `9bc0b6bfa442465cee5769a9392270f8b88e6ccb93fae25be542dfd8ec4cc08f` | already identical |
| `scenario_catalog.json` | `bca5a072ac4d893bcc62e1965fabfc6558c4408691c8ac24ee07e08cc48ea95f` | `bca5a072ac4d893bcc62e1965fabfc6558c4408691c8ac24ee07e08cc48ea95f` | copied |
| `golden/corrected_vnext/RULE2-01-GREEN.json` | `03a70ee7d9dbb0c0f7988135efe1577c16b149df8822af94b03cdb96f9c10dbd` | `03a70ee7d9dbb0c0f7988135efe1577c16b149df8822af94b03cdb96f9c10dbd` | already identical |
| `golden/corrected_vnext/RULE2-01-RED.json` | `31646561c134e4e6097a43ff1a9ffee8cbcc68439acc05b3947690ab8782a4fb` | `31646561c134e4e6097a43ff1a9ffee8cbcc68439acc05b3947690ab8782a4fb` | already identical |
| `golden/corrected_vnext/RULE2-02-GREEN.json` | `59acd8f75d35f384b89417fba4df289ebdf7bf768e4e9b22bf560bbeeaef3dfe` | `59acd8f75d35f384b89417fba4df289ebdf7bf768e4e9b22bf560bbeeaef3dfe` | already identical |
| `golden/corrected_vnext/RULE2-02-RED.json` | `9511084b30fb45a710ee56484f443042233ebcc700621f1582efd86bad851425` | `9511084b30fb45a710ee56484f443042233ebcc700621f1582efd86bad851425` | already identical |
| `golden/corrected_vnext/RULE2-03-GREEN.json` | `b38a9b65ad965280e93f6763ef0cf95c80b5c1b27774e3e65ecafef210f9524e` | `b38a9b65ad965280e93f6763ef0cf95c80b5c1b27774e3e65ecafef210f9524e` | already identical |
| `golden/corrected_vnext/RULE2-03-RED.json` | `7a12c41910edb62a1066e99a6a5306e4974d71edad40af670504f7e10db822b0` | `7a12c41910edb62a1066e99a6a5306e4974d71edad40af670504f7e10db822b0` | already identical |
| `golden/corrected_vnext/RULE2-04-GREEN.json` | `e192b8b6dedd8c05ae1055a2d7b2b56ac39fdc173cb2c18ac61567ed82f05fe6` | `e192b8b6dedd8c05ae1055a2d7b2b56ac39fdc173cb2c18ac61567ed82f05fe6` | already identical |
| `golden/corrected_vnext/RULE2-04-RED.json` | `65fe5ccefe4d04ae0b360e733b5632903ec29b71887d1ae27de8d6b27c9c05d1` | `65fe5ccefe4d04ae0b360e733b5632903ec29b71887d1ae27de8d6b27c9c05d1` | already identical |
| `golden/corrected_vnext/RULE2-05-GREEN.json` | `53ed07441c81bd5d49323a209af4ebee51eddad333f831f60eff802a2140ad23` | `53ed07441c81bd5d49323a209af4ebee51eddad333f831f60eff802a2140ad23` | already identical |
| `golden/corrected_vnext/RULE2-05-RED.json` | `6833c49e1d4d48ae7ad36406377358caa5a0387d48d067dfd8f086528b0b8760` | `6833c49e1d4d48ae7ad36406377358caa5a0387d48d067dfd8f086528b0b8760` | already identical |
| `golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json` | `d5eb751edac5bec0de32cc41aae23455b73357d6b73c43ffacd1a1bd3d64ea67` | `d5eb751edac5bec0de32cc41aae23455b73357d6b73c43ffacd1a1bd3d64ea67` | already identical |
| `golden/corrected_vnext/RULE2-06-GREEN.json` | `7057c3da1ede144725cb2edfdb34fe8c104bd2fe519fc3ca2af79628652e2ff6` | `7057c3da1ede144725cb2edfdb34fe8c104bd2fe519fc3ca2af79628652e2ff6` | already identical |
| `golden/corrected_vnext/RULE2-06-RED.json` | `b734e65a9806dbd9ba48d0b3a3104b9a3a92d008516a9345199c083170707371` | `b734e65a9806dbd9ba48d0b3a3104b9a3a92d008516a9345199c083170707371` | already identical |
| `golden/corrected_vnext/RULE2-07-GREEN.json` | `8ebdb0b8dcee9b4430c06af96cc21c5b2beea5c59a6a0fc81b6e4ab757f73bb2` | `8ebdb0b8dcee9b4430c06af96cc21c5b2beea5c59a6a0fc81b6e4ab757f73bb2` | already identical |
| `golden/corrected_vnext/RULE2-07-RED.json` | `82d11b9b826df4288e5e96f64d3f1ee6e6b4cf52b1a1b49af50807eb2e84a417` | `82d11b9b826df4288e5e96f64d3f1ee6e6b4cf52b1a1b49af50807eb2e84a417` | already identical |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | `7e3b886e4899472c0a92c921f8e27e8c172e46d4bb7c8e29ff6c1314aab4ee69` | `7e3b886e4899472c0a92c921f8e27e8c172e46d4bb7c8e29ff6c1314aab4ee69` | already identical |
| `golden/corrected_vnext/RULE2-08-RED.json` | `7302ad0eda8a461ce70c19b25264a260fec85bd34aa02bbaf051faba11da8ae3` | `7302ad0eda8a461ce70c19b25264a260fec85bd34aa02bbaf051faba11da8ae3` | already identical |

The copied control files and regenerated sidecar also match:

| File | Source SHA-256/value | Destination SHA-256/value | Result |
|---|---|---|---|
| `CONTRACT_TABLES_MANIFEST.json` | `09c91041bf0b768b3e4264ece84655a122d5f7bfd7604fc310d41d90f3740b9c` | `09c91041bf0b768b3e4264ece84655a122d5f7bfd7604fc310d41d90f3740b9c` | byte-identical |
| `implementation_anchor.json` from `IMPLEMENTATION_ANCHOR_DRAFT.json` | `79f6d4a23a94cebdb1af17d2db056040c98279c6f444712337f94b64bf3bc77d` | `79f6d4a23a94cebdb1af17d2db056040c98279c6f444712337f94b64bf3bc77d` | byte-identical |
| `implementation_anchor.json.sha256` | anchor SHA-256 above | `79f6d4a23a94cebdb1af17d2db056040c98279c6f444712337f94b64bf3bc77d` | regenerated and matches (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`) |

The content commit staged exactly the four changed paths: `scenario_catalog.json`,
`CONTRACT_TABLES_MANIFEST.json`, `implementation_anchor.json`, and
`implementation_anchor.json.sha256`. `git diff --check` returned exit 0 before commit.

## Canonical gate

Exactly one canonical invocation was issued from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W362_GATE_RECEIPT.json
```

It returned 1 and wrote the receipt; it was not rerun. The receipt records `mode: full-gate`, the
refused claim label, 17 RED/GREEN scenarios, and 10 probes
(`W362_GATE_RECEIPT.json:137-142,220,499-670`). `--mode observe` was not invoked.

## Full refusal list — verbatim

The following is the complete `refusals` value copied verbatim from
`W362_GATE_RECEIPT.json:671-712`:

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

| Probe | Base scenario | Expected failed check | Measured failed check | Expected first changed node | Comparator first differing node | Status | Evidence |
|---|---|---|---|---|---|---|---|
| `PROBE-P012-01-A` | `RULE2-01-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W362_GATE_RECEIPT.json:500-515` |
| `PROBE-P012-01-B` | `RULE2-01-GREEN` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W362_GATE_RECEIPT.json:517-532` |
| `PROBE-P012-02-A` | `RULE2-02-GREEN` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/RESULT_SURFACE/admitted` | `/EVENT_SURFACE/cash_events` | `DETECTED` | `W362_GATE_RECEIPT.json:534-549` |
| `PROBE-P012-03-A` | `RULE2-03-RED` | `RECORD_IDENTITY_PREFLIGHT` | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | same | `DETECTED` | `W362_GATE_RECEIPT.json:551-566` |
| `PROBE-P012-04-A` | `RULE2-04-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W362_GATE_RECEIPT.json:568-583` |
| `PROBE-P012-05-A` | `RULE2-05-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W362_GATE_RECEIPT.json:585-600` |
| `PROBE-P012-05-B` | `RULE2-05-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `DETECTED` | `W362_GATE_RECEIPT.json:602-617` |
| `PROBE-P012-06-A` | `RULE2-06-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/exit_id` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W362_GATE_RECEIPT.json:619-634` |
| `PROBE-P012-07-A` | `RULE2-07-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fee_events/1/liquidity_role` | `/EVENT_SURFACE/cash_events/1/signed_delta` | `DETECTED` | `W362_GATE_RECEIPT.json:636-651` |
| `PROBE-P012-08-A` | `RULE2-08-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W362_GATE_RECEIPT.json:653-668` |

Measured total: 10 `DETECTED`, 0 `NOT DETECTED` (`W362_GATE_RECEIPT.json:499-670`).

## Contract self-test suite

The gate's receipt records three failing self-test IDs but no passed count
(`W362_GATE_RECEIPT.json:703-710`). To capture complete counts and assertion values without
rerunning the canonical gate, this direct diagnostic command was run once from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q --tb=short
```

Measured result: 325 tests total; 322 passed and 3 failed in 14.04 seconds. The expected and actual
values were:

| Test pointer | Expected value | Actual value |
|---|---|---|
| `test_verify_bceg.py:826` | `.../contracts/expected_provenance_exceptions.json` | `.../golden/corrected_vnext/RULE2-01-GREEN.json` |
| `test_verify_bceg.py:939` | `.../contracts/expected_provenance_exceptions.json` | `.../golden/corrected_vnext/RULE2-01-GREEN.json` |
| `test_verify_bceg.py:1043` | `[MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json, MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json]` | `[MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json, MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json, MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json]` |

The asserted expected paths are defined at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:829-844`,
and the three assertions are at that file's lines 817-826, 924-939, and 1029-1045. No test or
provenance file was changed.

## Discrepancies

1. The lane predicted the refusal list would be exactly
   `["SEMANTIC_COVERAGE_REVIEW_MISSING"]` and the contract suite would be green
   (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:31-33`). The measured refusal
   list has three entries and the suite has 322 passed / 3 failed
   (`W362_GATE_RECEIPT.json:671-712`). The extra provenance refusal points first to
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json`
   and names 19 paths. Both identity values are: manifest/anchor implementation base
   `63cfe2dd2dcb3373f2fa18c385f67a1c2d113bb5` versus observed build
   `bdacf8e42399f9a3e9a753ca0ab30e5210ae98cf`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:572-585`;
   `W362_GATE_RECEIPT.json:677-700`). The lane forbade a base change, so no value was repaired.
2. The three contract tests retain expectations for the earlier two-path provenance model: first
   pointer `expected_provenance_exceptions.json`, and the two-item list
   `[expected_provenance_exceptions.json, implementation_anchor.json]`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:829-844,817-826,924-939,1029-1045`).
   The actual first pointer is `RULE2-01-GREEN.json`, and the actual synthetic list contains that
   golden before the expected two paths. These are the exact assertion mismatches measured above;
   no test was repaired.
3. The lane's “Only prose moved” explanation describes re-seal #17
   (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:12-15`), but the source bundle
   subsequently records re-seal #19 changing catalog expected-artifact digest leaves and re-seal
   #20 changing two probe modification-manifest digest leaves
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1017-1038`).
   This explains why `scenario_catalog.json` was the only manifest member that differed at the
   lane start; the source bytes were copied unchanged.
4. The copied manifest's current seal reason and final history row say re-seal #20, while
   `seal.set_by` still says `Lead re-seal act #17 2026-09-04T12:46:33+03:00`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:572-586,1028-1038`).
   The lane authorized byte-for-byte copying only, so this source-authored residue was preserved.
