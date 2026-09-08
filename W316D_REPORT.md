# W316D decision-134 provenance re-measurement report

Date: 2026-09-03
Actor: Codex lane
Status: **REFUSED**
Canonical refusal count: **6**
Acceptance-blocker count: **5**
Probe DETECTED count: **9 of 10**

The lane began on `feature/wp-p0-12-corrected-vnext-20260831` at required HEAD `443457d7`
with exactly the 14 W316C paths dirty. The manifest SHA-256 was
`f89cee3a11cd01d3a8c785c262073df3e2441d95027d472b153e800b7454cca2` and exactly the
ten lane-named observed artifacts differed; these are the predecessor facts that W316C also
recorded (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316D_PROVENANCE_RECORD_M5_BASE.md:5-14`;
`W316C_REPORT.md:19-21`; `W316C_REPORT.md:112-115`).

## W316C commit

The 14-path predecessor package was staged by exact path and committed unchanged as:

- commit `eda17c3f96742ba9c8f3b73985a02011b40651d7`
- `chore(mtc-v2): copy manifest #14b and materialize catalog-bound observed artifacts (W316C)`

No other path was staged in that commit. This satisfies the first prescribed action
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W316D_PROVENANCE_RECORD_M5_BASE.md:14-17`).

## Decision-134 record re-measurement

For
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json`,
read-only `git rev-parse` resolved the M5 base blob to
`b811ce9d9d4efe574828c6d3fc2703bea71b71a8`, so the record now says
`PRESENT_AT_BASE`. After the W316C commit, `HEAD:<path>` resolved to
`f7b72d452e1d2abed58a97e541ee156d3e5821c2`, exactly equal to the previously recorded
current blob; the golden did not move (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:5-7`).

The record now contains the full M5 base, appends `W316D`, retains integer owner decision 134,
and appends the one prescribed sentence (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:8-19`).
A byte-level formatting check confirmed sorted keys, two-space indentation, one trailing LF, and no
CR bytes. The harness requires the closed top-level/member key sets, the declaration/schema values,
an integer owner decision, and a non-empty lane list
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1990-2006`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2013-2041`).

### Record before/after diff

```diff
-      "base_blob_oid": null,
-      "base_state": "ABSENT_AT_BASE",
+      "base_blob_oid": "b811ce9d9d4efe574828c6d3fc2703bea71b71a8",
+      "base_state": "PRESENT_AT_BASE",
       "current_blob_oid": "f7b72d452e1d2abed58a97e541ee156d3e5821c2",
       "lane_ids": [
         "W156",
         "W167",
-        "W172"
+        "W172",
+        "W316D"
       ],
       "owner_decision": 134,
       "path": "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json",
-      "reason": "Owner decision 134: the RULE2-01-GREEN golden was revised by the design-directed lanes W156 (design v1.5), W167 (v1.8) and W172 (owner Reading Y), each verified at the time; those three repairs are recorded as the authorized section 15.4 exception. Measured here: the path does not exist at IMPLEMENTATION_BASE_SHA at all, so there is no base blob object id to record and the change since the base is a creation, not a revision of a base blob."
+      "reason": "Owner decision 134: the RULE2-01-GREEN golden was revised by the design-directed lanes W156 (design v1.5), W167 (v1.8) and W172 (owner Reading Y), each verified at the time; those three repairs are recorded as the authorized section 15.4 exception. Measured here: the path does not exist at IMPLEMENTATION_BASE_SHA at all, so there is no base blob object id to record and the change since the base is a creation, not a revision of a base blob. Re-measured at the M5 base 5e8e5794 (owner decision 135) by lane W316D on 2026-09-03; the owner decision 134 authorization is unchanged."
     }
   ],
-  "implementation_base_sha": "108ea066a710ff7ef5c09246903fe3d523da1d56",
+  "implementation_base_sha": "5e8e579410ee55008bfd2d2d85054fd1d782f32c",
```

### SHA table

| Item | Algorithm | Measured value |
|---|---|---|
| M5 implementation base | Git SHA-1 | `5e8e579410ee55008bfd2d2d85054fd1d782f32c` |
| W316C commit | Git SHA-1 | `eda17c3f96742ba9c8f3b73985a02011b40651d7` |
| exception record before | Git blob SHA-1 | `e3973c3397e7a155e19b883c8d27ea71b150b7dd` |
| exception record after | Git blob SHA-1 | `d56dcf860e155b0d5ac6a22c3f52d87fabcf136e` |
| golden at M5 base | Git blob SHA-1 | `b811ce9d9d4efe574828c6d3fc2703bea71b71a8` |
| golden at W316C HEAD | Git blob SHA-1 | `f7b72d452e1d2abed58a97e541ee156d3e5821c2` |
| exception record after | SHA-256 | `34d554e938cfb3bc408284f5f89124c295ed8fa365369d4ad8382d64fd025d1b` |
| W316D gate receipt | SHA-256 | `0b0d1e2c53dd846da3cf613f550fa7e25a7fe07aee5ffdac818f1c246ae5485d` |

The record fields carrying the base/current blob IDs and implementation base are independently
visible in the file (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:5-7`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:19`).

## Canonical gate

The prescribed command was invoked exactly once from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` and returned exit 1. It wrote
`W316D_GATE_RECEIPT.json` itself, so no stdout-to-file fallback was needed. The receipt is 2,422
lines, identifies `full-gate`, reaches the comparison pipeline, and labels the claim
`BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED` (`W316D_GATE_RECEIPT.json:51`;
`W316D_GATE_RECEIPT.json:557-567`; `W316D_GATE_RECEIPT.json:636-640`).

The observed-artifact pins are current with `stale_count` zero
(`W316D_GATE_RECEIPT.json:909-917`).

## Full refusal list, verbatim

The following array is copied verbatim from `W316D_GATE_RECEIPT.json:1091-1143`:

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
      "pointer": "/RESULT_SURFACE/run_manifest/cost_schedule_digest",
      "scenario_id": "RULE2-08-RED"
    },
    {
      "check_id": "CORRECTED_EXPECTATION_MISMATCH",
      "pointer": "/EVENT_SURFACE/cash_events",
      "scenario_id": "RULE2-08-RED"
    },
    {
      "check_id": "OBSERVED_EXTRA_MEMBER",
      "pointer": "/RESULT_SURFACE/run_manifest/cost_schedule_digest",
      "scenario_id": "RULE2-08-GREEN"
    }
  ],
```

## Unexpected refusal detail

The unexpected refusal is `EXPECTED_PATH_CHANGED_AFTER_BASE`. The receipt identifies 18 changed
expected-source paths (`W316D_GATE_RECEIPT.json:1097-1121`). The table gives both read-only Git blob
values measured at the M5 base and W316C HEAD:

| Pointer | M5-base blob | W316C-HEAD blob |
|---|---|---|
| `golden/corrected_vnext/RULE2-01-RED.json` | `969f24bb3770b1e4ae39312cb05fea0618e9fc31` | `ad2193d9117a811c2a8bdb50e09f547de361c457` |
| `golden/corrected_vnext/RULE2-02-GREEN.json` | `fc5d35ffe7a58faf7b68412f593fdbb38c78a657` | `c9593099add3499fd978fb212efbe2de62c0f132` |
| `golden/corrected_vnext/RULE2-02-RED.json` | `960d8513e4072b70e974ba4aad952aa4dddfd01f` | `4179162792756e108ed2140213d3a575f41cbd54` |
| `golden/corrected_vnext/RULE2-03-GREEN.json` | `f3ea6c20cd2c686d11f977640547f48eab4bd9b2` | `179babd67d9b5f20bd00c3761be7f8db06ecbca4` |
| `golden/corrected_vnext/RULE2-03-RED.json` | `a742f555185ab0e579463017708a83ffce394d05` | `0c9116a27bc52296c61e9ac1e21d17b8f9714f6f` |
| `golden/corrected_vnext/RULE2-04-GREEN.json` | `248a66b2dd4f9b5ad34fb618f703705593059c35` | `2eb54d43a55fd868a5afc152f40284154c25d1cb` |
| `golden/corrected_vnext/RULE2-04-RED.json` | `2c37bca47fd21399384aaea41e0fe7b54988d351` | `e32dcaad6e2978b0c102259a370008f6c7871904` |
| `golden/corrected_vnext/RULE2-05-GREEN.json` | `24c04d3121081a524472c32f5101948a553f37fa` | `6158e0837c6ad1d32b3de9c42c5de2716e897bca` |
| `golden/corrected_vnext/RULE2-05-RED.json` | `59f00221583b312e55886b6e2189fb251f359ceb` | `c098bfc5248bc9663c0c014864172e2237e53fae` |
| `golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json` | `2037cbd608dc5f4998a2bece9c5282425d4a5f02` | `17ed6e235205f6f8663c4929cb4fd514c21fb2f1` |
| `golden/corrected_vnext/RULE2-06-GREEN.json` | `a3f59d76d3e3d4632dfc6782ba4ad56f9fda7265` | `15858704f5ce584c31ce9b824fe85d61410082a8` |
| `golden/corrected_vnext/RULE2-06-RED.json` | `a15c4251dda164107a93cd646522c11c424d8be7` | `852593a4d8e07ed71fe3adce9673101151f5e4ab` |
| `golden/corrected_vnext/RULE2-07-GREEN.json` | `0d5313d3f1425cfe73575dbcc61308ae0f1d67fe` | `91fb95f53d223d66cce7a427b6dfa83adb36e927` |
| `golden/corrected_vnext/RULE2-07-RED.json` | `877003ba06024c9247de498ae94c12ec8b87a893` | `89e68b1c53900131eb333f7db0dbf080e996869e` |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | `86b13f50a647156812017a1b66c3ff634a468911` | `9730e7b4270b4deba96ec6c490f63eccfb30ddeb` |
| `golden/corrected_vnext/RULE2-08-RED.json` | `9e90b3fa2f11b25438601aebdaa7b2448e4d72ff` | `3ea6820ec1bb40914320435788bd30f95203080f` |
| `tests/corrected_vnext/contracts/DERIVATIONS.md` | `b401181d0b5d08fcef9609adb4a2b2f13a4ea427` | `f4fb760ee7e5b58efec566ce26c4b0f001588e9c` |
| `tests/corrected_vnext/contracts/scenario_catalog.json` | `a4fe0996497966fe71eb720a262ea8536e04bb86` | `ab7fc100c7245f4dce0c5af0d850b2d272971101` |

Every pointer in this table is relative to
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/`; the receipt emits the corresponding full
repository paths (`W316D_GATE_RECEIPT.json:1101-1120`). No refusal was repaired.

## Probe table

All ten probes evaluated. The first changed node below is the receipt field
`comparator_first_differing_node` (`W316D_GATE_RECEIPT.json:919-1089`).

| Probe | Result | Expected failed check | Measured failed check | First changed node |
|---|---|---|---|---|
| `PROBE-P012-01-A` | DETECTED | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-01-B` | DETECTED | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-02-A` | NOT DETECTED | `CORRECTED_EXPECTATION` | `CLOSED_SET_VIOLATION` | `/RESULT_SURFACE/admitted` |
| `PROBE-P012-03-A` | DETECTED | `RECORD_IDENTITY_PREFLIGHT` | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` |
| `PROBE-P012-04-A` | DETECTED | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-05-A` | DETECTED | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-05-B` | DETECTED | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` |
| `PROBE-P012-06-A` | DETECTED | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-07-A` | DETECTED | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/1/signed_delta` |
| `PROBE-P012-08-A` | DETECTED | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events` |

The measured total is nine DETECTED and one NOT DETECTED; the latter is also promoted into the
refusal list (`W316D_GATE_RECEIPT.json:955-969`; `W316D_GATE_RECEIPT.json:1122-1127`).

## Discrepancies

1. The prompt predicts that provenance passes and five refusals remain. The valid decision-134
   exception record no longer triggers `EXPECTED_PROVENANCE_EXCEPTION_INVALID`, but the broader
   expected-source provenance check is `MISMATCH` and adds
   `EXPECTED_PATH_CHANGED_AFTER_BASE` for 18 paths. The measured full refusal count is therefore six,
   not five (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316D_PROVENANCE_RECORD_M5_BASE.md:39-41`;
   `W316D_GATE_RECEIPT.json:565-568`; `W316D_GATE_RECEIPT.json:1091-1143`).
2. The prompt's other five predicted refusals are present: the semantic-coverage review is missing,
   `PROBE-P012-02-A` is NOT DETECTED, the RULE2-08 pair has two
   `OBSERVED_EXTRA_MEMBER` refusals, and RULE2-08-RED has the
   `CORRECTED_EXPECTATION_MISMATCH` at `/EVENT_SURFACE/cash_events`
   (`W316D_GATE_RECEIPT.json:1092-1095`; `W316D_GATE_RECEIPT.json:1122-1142`).
3. The canonical process returned exit 1 while writing the requested receipt; no early-path
   stdout-only fallback was needed. The prompt did not predict an exit code, so this is recorded as
   measured execution detail, not a specification conflict
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W316D_PROVENANCE_RECORD_M5_BASE.md:36-41`;
   `W316D_GATE_RECEIPT.json:562`; `W316D_GATE_RECEIPT.json:640`).

No kernel, harness code, golden, input, catalog, probe, or design byte was changed. The only W316D
repository writes are the exact exception record, gate receipt, and this report named by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W316D_PROVENANCE_RECORD_M5_BASE.md:8-9`;
`C:\tmp\LANE_PROMPTS_20260828\LANE_W316D_PROVENANCE_RECORD_M5_BASE.md:42-45`).
