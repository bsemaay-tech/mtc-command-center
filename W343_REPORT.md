# W343 Report — re-seal #15 copy refresh and canonical gate

## Verdict

The in-repo copies named by lane W343 were refreshed to re-seal #15 and committed as `6bed8ad1`. The canonical `full-gate` invocation then refused with 6 entries in its full refusal list, 5 acceptance blockers, and 9 of 10 probes `DETECTED` (`W343_GATE_RECEIPT.json:1-51,884-1108`). No refusal was fixed.

## Preconditions and scope

- Re-seal #15 identifies seal `27bf72e826432c7f278b35b2d58dd9f071e56c969a244a42d0e30833a20348fe`, base `5e8e5794`, and design digest prefix `137180aee483` over 1664 lines (`C:\tmp\LANE_PROMPTS_20260828\RESEAL15_DONE.txt:1`).
- The baseline prerequisite and W342 prerequisite both recorded `exit=0` (`C:\tmp\LANE_PROMPTS_20260828\W300D_DONE.txt:1`; `C:\tmp\LANE_PROMPTS_20260828\W342_DONE.txt:1`).
- The measured starting branch was `feature/wp-p0-12-corrected-vnext-20260831`, starting HEAD was `91c3a54b3b56c870c0c66feb58faa50cf043b2eb`, and `git status --porcelain=v1 --untracked-files=all` emitted no paths. These are recorded command results from the precondition check.
- The write lane touched only the seven authorized in-repo copy/sidecar paths, then the two required root evidence paths. No observed artifact was regenerated; the receipt identifies `full-gate` mode (`W343_GATE_RECEIPT.json:605`).

## Refreshed copy SHA-256 table

Each source and destination digest below was computed from disk after the copy. The re-seal marker independently records all six source digests (`C:\tmp\LANE_PROMPTS_20260828\RESEAL15_DONE.txt:2-7`).

| Bundle member | Source SHA-256 | In-repo SHA-256 | Result | Evidence |
|---|---|---|---|---|
| `golden/corrected_vnext/RULE2-08-RED.json` | `b4da2832a3218750935f464d4fd91a3a3dd1fdf6d6a46f661f6a3a884d6bba5f` | `b4da2832a3218750935f464d4fd91a3a3dd1fdf6d6a46f661f6a3a884d6bba5f` | equal | `RESEAL15_DONE.txt:2`; `CONTRACT_TABLES_MANIFEST.json:154-156` |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | `1185758e987bca067eaed98b7dd2ecca322837893010b9a04dfcc04ceb0b796c` | `1185758e987bca067eaed98b7dd2ecca322837893010b9a04dfcc04ceb0b796c` | equal | `RESEAL15_DONE.txt:3`; `CONTRACT_TABLES_MANIFEST.json:149-151` |
| `scenario_catalog.json` | `726cbc95aaacfc7024522c4c46f28deeb440b8bf56d4087ff446713fa27f03a8` | `726cbc95aaacfc7024522c4c46f28deeb440b8bf56d4087ff446713fa27f03a8` | equal | `RESEAL15_DONE.txt:4`; `CONTRACT_TABLES_MANIFEST.json:68-71` |
| `DERIVATIONS.md` | `c1ca836757b05b3f57c619fc82d9229fe47baccd219e4420b77c49fb729329a6` | `c1ca836757b05b3f57c619fc82d9229fe47baccd219e4420b77c49fb729329a6` | equal | `RESEAL15_DONE.txt:5`; `CONTRACT_TABLES_MANIFEST.json:63-66` |
| `CONTRACT_TABLES_MANIFEST.json` | `ca3ed9b730ef67cc294b66e05102cc081a2de9439d1cc262bba16465c6c1e804` | `ca3ed9b730ef67cc294b66e05102cc081a2de9439d1cc262bba16465c6c1e804` | equal | `C:\tmp\LANE_PROMPTS_20260828\RESEAL15_DONE.txt:6`; destination file read at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1` |
| `IMPLEMENTATION_ANCHOR_DRAFT.json` → `implementation_anchor.json` | `b53a9df8ce8e8f658b465b67295f2d59feb6a43d20f9cf8c670cba426e066ba2` | `b53a9df8ce8e8f658b465b67295f2d59feb6a43d20f9cf8c670cba426e066ba2` | equal | `C:\tmp\LANE_PROMPTS_20260828\RESEAL15_DONE.txt:7`; `implementation_anchor.json.sha256:1` |
| regenerated `implementation_anchor.json.sha256` | n/a | `b53a9df8ce8e8f658b465b67295f2d59feb6a43d20f9cf8c670cba426e066ba2\n` | bare lowercase hex, one line | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1` |

## Other manifest-member identity table

All 15 other `files[]` members were hashed at source and destination before the refresh; every source digest, destination digest, and manifest digest was equal. The manifest enumerates those members and hashes at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:73-146`.

| Other member | SHA-256 | Result |
|---|---|---|
| `RULE2-01-GREEN.json` | `38b79ef1cd114724c63e665f3f0e18a478e0693b79ee49356426561a6aaa597a` | equal |
| `RULE2-01-RED.json` | `74f6f80cd44f7f980c3f0b332681bcc34e0a4f5a21bf567c84a17b14aacc38fa` | equal |
| `RULE2-02-GREEN.json` | `aefa016537dd342e307a974c97b513fcbd1c9ef140ef7bfaee5a62b648b6a146` | equal |
| `RULE2-02-RED.json` | `b6b4e4bfb21c162cdee84e49762357f543afc6bf72320765748d70bdc030388d` | equal |
| `RULE2-03-GREEN.json` | `c10b5e71d7c84ccdc8668cb081ba5b394d3fbeba2119a0a53eeb96c9f4fea880` | equal |
| `RULE2-03-RED.json` | `e04ddf0cdd14c68076ddd1b081467ee21fafb836d7a51751990bfb361b1bb724` | equal |
| `RULE2-04-GREEN.json` | `7309d4cbe1445cea9d8ccb4ca44bc91e81e45fd8c157fa3daed3b295561ba7f7` | equal |
| `RULE2-04-RED.json` | `50a990c2005ade1fa5db41cdd00f7bd194e0e89db1f3cd1b24d3d71e693aa85c` | equal |
| `RULE2-05-GREEN.json` | `26bbb48caf2fb2c5f9f13f08f23664ede89f31c9bfa337d9b878ab68ffa19798` | equal |
| `RULE2-05-RED.json` | `88197710a9a767a130d794dbbebe56a81fe9ef990081d3c15171b574e25dbc9a` | equal |
| `RULE2-06-EQUAL-PRICE-RED.json` | `c05a51eb1e03b8864c495a3d48d3ccd722a2d598489038f055d755f32cb31de0` | equal |
| `RULE2-06-GREEN.json` | `45f10ddb072e19b2dae4473e09c6af74268bef11bb64247eea94dc8d0538cda2` | equal |
| `RULE2-06-RED.json` | `9d9d3a9748571d63c8790d9b7ef5df398ed945f75c59b7148975debfe167a581` | equal |
| `RULE2-07-GREEN.json` | `1acd5a74f98d22165971486d6a2ede029f58bf984f85181617055ca473644a4a` | equal |
| `RULE2-07-RED.json` | `e4d966eee8587ca3d645e3abd9a98847daf8f41a3743250563624975f926435b` | equal |

## Canonical gate

Exactly one invocation was made from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W343_GATE_RECEIPT.json
```

It exited `1`. The receipt labels the result `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED` and mode `full-gate` (`W343_GATE_RECEIPT.json:527,605`).

## Full refusal list — verbatim

The following block is copied verbatim from `W343_GATE_RECEIPT.json:1056-1108`.

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

## Remaining RULE2-08 pointer/value evidence

| Scenario and refusal | Pointer | Expected value/state | Observed value verbatim | Evidence |
|---|---|---|---|---|
| `RULE2-08-RED / OBSERVED_EXTRA_MEMBER` | `/EVENT_SURFACE/cash_events/0/funding_event_id` | `ABSENT` | `"TEST-FUND-1"` | refusal: `W343_GATE_RECEIPT.json:1094-1096`; expected closed object: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-RED.json:33-35`; observed scalar: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/observed/2.0.0/RULE2-08-RED.json:1` |
| `RULE2-08-RED / OBSERVED_EXTRA_MEMBER` | `/RESULT_SURFACE/run_manifest/cost_schedule_digest` | `ABSENT` | `"806e98512a3eb336538c8b68a52cef3ed80897cd2a87d9f270900c7ba094f29b"` | refusal: `W343_GATE_RECEIPT.json:1099-1101`; expected object: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-RED.json:50-60`; observed scalar: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/observed/2.0.0/RULE2-08-RED.json:1` |
| `RULE2-08-GREEN / OBSERVED_EXTRA_MEMBER` | `/RESULT_SURFACE/run_manifest/cost_schedule_digest` | `ABSENT` | `"040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe"` | refusal: `W343_GATE_RECEIPT.json:1104-1106`; expected object: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-GREEN.json:43-53`; observed scalar: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/observed/2.0.0/RULE2-08-GREEN.json:1` |

There is no remaining `CORRECTED_EXPECTATION_MISMATCH` entry in the complete refusal array (`W343_GATE_RECEIPT.json:1056-1108`).

## Probe table

The receipt contains 10 probe rows at `W343_GATE_RECEIPT.json:884-1055`: 9 `DETECTED` and 1 `NOT_DETECTED`.

| Probe | Base scenario | Expected failed check | Measured failed check | Comparator first differing node | Status | Evidence |
|---|---|---|---|---|---|---|
| `PROBE-P012-01-A` | `RULE2-01-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W343_GATE_RECEIPT.json:885-900` |
| `PROBE-P012-01-B` | `RULE2-01-GREEN` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W343_GATE_RECEIPT.json:902-917` |
| `PROBE-P012-02-A` | `RULE2-02-GREEN` | `CORRECTED_EXPECTATION` | `CLOSED_SET_VIOLATION` | `/RESULT_SURFACE/admitted` | `NOT_DETECTED` | `W343_GATE_RECEIPT.json:919-934` |
| `PROBE-P012-03-A` | `RULE2-03-RED` | `RECORD_IDENTITY_PREFLIGHT` | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | `DETECTED` | `W343_GATE_RECEIPT.json:936-951` |
| `PROBE-P012-04-A` | `RULE2-04-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W343_GATE_RECEIPT.json:953-968` |
| `PROBE-P012-05-A` | `RULE2-05-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W343_GATE_RECEIPT.json:970-985` |
| `PROBE-P012-05-B` | `RULE2-05-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `DETECTED` | `W343_GATE_RECEIPT.json:987-1002` |
| `PROBE-P012-06-A` | `RULE2-06-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `DETECTED` | `W343_GATE_RECEIPT.json:1004-1019` |
| `PROBE-P012-07-A` | `RULE2-07-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/1/signed_delta` | `DETECTED` | `W343_GATE_RECEIPT.json:1021-1036` |
| `PROBE-P012-08-A` | `RULE2-08-RED` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/funding_event_id` | `DETECTED` | `W343_GATE_RECEIPT.json:1038-1053` |

## Discrepancies

1. The lane prediction that no RULE2-08 `OBSERVED_EXTRA_MEMBER` would remain did not hold. The gate reports three such refusals: two for `RULE2-08-RED` and one for `RULE2-08-GREEN` (`W343_GATE_RECEIPT.json:1093-1107`). The prediction was treated as a prediction; no file was repaired.
2. The receipt records each remaining extra-member pointer but does not emit its expected/observed scalar pair (`W343_GATE_RECEIPT.json:1093-1107`). To satisfy the lane's value-reporting requirement, the expected `ABSENT` states were verified from the closed golden objects and the exact observed strings were read from the corresponding observed files at the cited lines in the pointer/value table.
