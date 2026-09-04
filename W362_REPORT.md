# W362 Report — re-seal #18 copy refresh and canonical gate

## Verdict

The in-repo bundle copies were refreshed byte-for-byte and committed at content commit
`598224f595a6f959da1d81d8d8f2e3ca1fe0bd0e`. The 19-member seal recomputed as
`12fc3d4a5b0ed199ef9173f03c78cf35dea9e621f6b9d3384f6530625b4d2be4`, matching the copied anchor
and the manifest's re-seal #18 record
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1003-1006`).

The canonical gate was invoked exactly once and returned 1 on the early refusal
`EXPECTED_DIGEST_MISMATCH` for `RULE2-01-RED`. The verifier did not write the requested output
file, so `W362_GATE_RECEIPT.json` is a manual verbatim capture of stdout, as the lane directs for
that path (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:28-33`;
`W362_GATE_RECEIPT.json:1-8`). No bundle byte was changed in response.

## Preconditions, routing, and scope

The lane requires `RESEAL18_DONE.txt` and `W361_DONE.txt` to read `exit=0`, a clean worktree, a
recorded HEAD, and a recomputed source-bundle seal matching the re-seal marker
(`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:7-10`). Both markers were present and
read `exit=0` (`C:/tmp/LANE_PROMPTS_20260828/RESEAL18_DONE.txt:1`;
`C:/tmp/LANE_PROMPTS_20260828/W361_DONE.txt:1`). The measured start was worktree
`C:\WP012BUILD`, branch `feature/wp-p0-12-corrected-vnext-20260831`, full HEAD
`d32e903a4007593b85aad9aa882a1f049196980d`, and empty porcelain status.

The source bundle's 19 member hashes and byte counts matched its manifest. Recomputing SHA-256 over
the LF-joined, lexicographically sorted `path:sha256` rows produced
`12fc3d4a5b0ed199ef9173f03c78cf35dea9e621f6b9d3384f6530625b4d2be4`; this matches the marker,
the copied anchor, and the manifest's re-seal #18 value
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1003-1014`).

Primary changes are protected expected economic artifacts under
`MTC_COMMAND_CENTER/01_MTC_PROJECT/**`, so Gate 1 is T0. The write lane was the branch and worktree
named above, with exact paths enumerated in the SHA tables below. Live-dependency status was none:
no broker, venue, host, deploy, Pine, kernel, baseline, or base-anchor path was touched. The lane
authorizes only the named copy paths, forbids changing the base, and forbids observe mode
(`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:13-26`).

## Design-pin measurement

The design file measured SHA-256
`03fdf5952a2365b2de60b55292a1bd50fce8c6c51788c19b59cecc5d8f5b3c94` and 1,843 lines. Both
values match the copied manifest's v1.18 whole-file pin
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-18`).

## Source/destination SHA-256 table

Every manifest member differed from the starting in-repo seal-#16 copy and was therefore refreshed.
After copying, every source and destination pair was byte-identical and matched the manifest's
recorded SHA-256 and byte count
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:62-158`).

| File | Source SHA-256 | Destination SHA-256 | Result |
|---|---|---|---|
| `DERIVATIONS.md` | `9bc0b6bfa442465cee5769a9392270f8b88e6ccb93fae25be542dfd8ec4cc08f` | `9bc0b6bfa442465cee5769a9392270f8b88e6ccb93fae25be542dfd8ec4cc08f` | byte-identical |
| `scenario_catalog.json` | `f4f19c255355942cacdc705b0362ea9c4955877d3128f5a94c8505448095f940` | `f4f19c255355942cacdc705b0362ea9c4955877d3128f5a94c8505448095f940` | byte-identical |
| `golden/corrected_vnext/RULE2-01-GREEN.json` | `03a70ee7d9dbb0c0f7988135efe1577c16b149df8822af94b03cdb96f9c10dbd` | `03a70ee7d9dbb0c0f7988135efe1577c16b149df8822af94b03cdb96f9c10dbd` | byte-identical |
| `golden/corrected_vnext/RULE2-01-RED.json` | `31646561c134e4e6097a43ff1a9ffee8cbcc68439acc05b3947690ab8782a4fb` | `31646561c134e4e6097a43ff1a9ffee8cbcc68439acc05b3947690ab8782a4fb` | byte-identical |
| `golden/corrected_vnext/RULE2-02-GREEN.json` | `59acd8f75d35f384b89417fba4df289ebdf7bf768e4e9b22bf560bbeeaef3dfe` | `59acd8f75d35f384b89417fba4df289ebdf7bf768e4e9b22bf560bbeeaef3dfe` | byte-identical |
| `golden/corrected_vnext/RULE2-02-RED.json` | `9511084b30fb45a710ee56484f443042233ebcc700621f1582efd86bad851425` | `9511084b30fb45a710ee56484f443042233ebcc700621f1582efd86bad851425` | byte-identical |
| `golden/corrected_vnext/RULE2-03-GREEN.json` | `b38a9b65ad965280e93f6763ef0cf95c80b5c1b27774e3e65ecafef210f9524e` | `b38a9b65ad965280e93f6763ef0cf95c80b5c1b27774e3e65ecafef210f9524e` | byte-identical |
| `golden/corrected_vnext/RULE2-03-RED.json` | `7a12c41910edb62a1066e99a6a5306e4974d71edad40af670504f7e10db822b0` | `7a12c41910edb62a1066e99a6a5306e4974d71edad40af670504f7e10db822b0` | byte-identical |
| `golden/corrected_vnext/RULE2-04-GREEN.json` | `e192b8b6dedd8c05ae1055a2d7b2b56ac39fdc173cb2c18ac61567ed82f05fe6` | `e192b8b6dedd8c05ae1055a2d7b2b56ac39fdc173cb2c18ac61567ed82f05fe6` | byte-identical |
| `golden/corrected_vnext/RULE2-04-RED.json` | `65fe5ccefe4d04ae0b360e733b5632903ec29b71887d1ae27de8d6b27c9c05d1` | `65fe5ccefe4d04ae0b360e733b5632903ec29b71887d1ae27de8d6b27c9c05d1` | byte-identical |
| `golden/corrected_vnext/RULE2-05-GREEN.json` | `53ed07441c81bd5d49323a209af4ebee51eddad333f831f60eff802a2140ad23` | `53ed07441c81bd5d49323a209af4ebee51eddad333f831f60eff802a2140ad23` | byte-identical |
| `golden/corrected_vnext/RULE2-05-RED.json` | `6833c49e1d4d48ae7ad36406377358caa5a0387d48d067dfd8f086528b0b8760` | `6833c49e1d4d48ae7ad36406377358caa5a0387d48d067dfd8f086528b0b8760` | byte-identical |
| `golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json` | `d5eb751edac5bec0de32cc41aae23455b73357d6b73c43ffacd1a1bd3d64ea67` | `d5eb751edac5bec0de32cc41aae23455b73357d6b73c43ffacd1a1bd3d64ea67` | byte-identical |
| `golden/corrected_vnext/RULE2-06-GREEN.json` | `7057c3da1ede144725cb2edfdb34fe8c104bd2fe519fc3ca2af79628652e2ff6` | `7057c3da1ede144725cb2edfdb34fe8c104bd2fe519fc3ca2af79628652e2ff6` | byte-identical |
| `golden/corrected_vnext/RULE2-06-RED.json` | `b734e65a9806dbd9ba48d0b3a3104b9a3a92d008516a9345199c083170707371` | `b734e65a9806dbd9ba48d0b3a3104b9a3a92d008516a9345199c083170707371` | byte-identical |
| `golden/corrected_vnext/RULE2-07-GREEN.json` | `8ebdb0b8dcee9b4430c06af96cc21c5b2beea5c59a6a0fc81b6e4ab757f73bb2` | `8ebdb0b8dcee9b4430c06af96cc21c5b2beea5c59a6a0fc81b6e4ab757f73bb2` | byte-identical |
| `golden/corrected_vnext/RULE2-07-RED.json` | `82d11b9b826df4288e5e96f64d3f1ee6e6b4cf52b1a1b49af50807eb2e84a417` | `82d11b9b826df4288e5e96f64d3f1ee6e6b4cf52b1a1b49af50807eb2e84a417` | byte-identical |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | `7e3b886e4899472c0a92c921f8e27e8c172e46d4bb7c8e29ff6c1314aab4ee69` | `7e3b886e4899472c0a92c921f8e27e8c172e46d4bb7c8e29ff6c1314aab4ee69` | byte-identical |
| `golden/corrected_vnext/RULE2-08-RED.json` | `7302ad0eda8a461ce70c19b25264a260fec85bd34aa02bbaf051faba11da8ae3` | `7302ad0eda8a461ce70c19b25264a260fec85bd34aa02bbaf051faba11da8ae3` | byte-identical |

There were zero unchanged-before-copy “other” manifest members: all 19 differed and all 19 were
refreshed. The manifest records that re-seal #17 changed all 19 members and re-seal #18 then changed
three of them (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:974-1014`).

The copied control files and regenerated sidecar also match:

| File | Source SHA-256 | Destination SHA-256 | Result | Evidence |
|---|---|---|---|---|
| `CONTRACT_TABLES_MANIFEST.json` | `fbae58edd44925eaeffbb923f6e12b42168fa956581219a19dd76bb11d008084` | `fbae58edd44925eaeffbb923f6e12b42168fa956581219a19dd76bb11d008084` | byte-identical | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1-3` |
| `implementation_anchor.json` from `IMPLEMENTATION_ANCHOR_DRAFT.json` | `f0851c60cf37288e91539ae257dcd0b631693b50bcdf1cd788a2222bbb4d31ca` | `f0851c60cf37288e91539ae257dcd0b631693b50bcdf1cd788a2222bbb4d31ca` | byte-identical | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:1-7` |
| `implementation_anchor.json.sha256` | `f0851c60cf37288e91539ae257dcd0b631693b50bcdf1cd788a2222bbb4d31ca` | `f0851c60cf37288e91539ae257dcd0b631693b50bcdf1cd788a2222bbb4d31ca` | regenerated and matches anchor | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1` |

The content commit staged exactly these 22 paths. `git diff --check` returned 0 before the commit.
Its subject is exactly the lane-prescribed subject
(`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:27`).

## Canonical gate

Exactly one invocation was issued from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W362_GATE_RECEIPT.json
```

The process returned 1. It did not create `W362_GATE_RECEIPT.json`; the file now at that path was
written afterward as a manual verbatim capture of the single stdout document, following the lane's
explicit early-refusal instruction (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:28-30`;
`W362_GATE_RECEIPT.json:1-8`). `--mode observe` was not invoked
(`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:24-26`).

## Full refusal output — verbatim

The early path emitted a singular `refusal` object rather than a `refusals` list. This is the full
stdout document captured verbatim in `W362_GATE_RECEIPT.json:1-8`:

```json
{
  "claim_label": "BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED",
  "mode": "full-gate",
  "refusal": {
    "check_id": "EXPECTED_DIGEST_MISMATCH",
    "detail": "RULE2-01-RED"
  }
}
```

## Refusal pointer and both values

The catalog's `RULE2-01-RED` row points to the named golden and carries the stale expected digest
shown below (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:26-31`).
The actual digest is independently measured and is also the digest pinned for that exact member by
the copied manifest
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:78-81`).
The verifier hashes the pointed file and refuses on inequality before loading the golden
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2445-2453`).

| Pointer | Catalog expected digest | Actual file digest | Result |
|---|---|---|---|
| `golden/corrected_vnext/RULE2-01-RED.json` | `3cf30e13db25a99093d9087c374c05dabbc6ca0a33ad6cebdfdd1d28df42b94d` | `31646561c134e4e6097a43ff1a9ffee8cbcc68439acc05b3947690ab8782a4fb` | mismatch; refused |

## Probe table

The lane's 10/10 `DETECTED` value was a prediction to measure, not an inherited result
(`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:31-33`). The early stdout document
contains no probe section (`W362_GATE_RECEIPT.json:1-8`), so no probe result or count is claimed.

| Measure | Predicted | Measured |
|---|---:|---|
| Probe rows | 10 | NOT PRODUCED |
| `DETECTED` | 10 | NOT PRODUCED |
| `NOT DETECTED` | 0 | NOT PRODUCED |

## Contract-suite counts

The full-gate implementation starts the contract self-test suite before the comparison pipeline,
but constructs the receipt only after the pipeline returns
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:4241-4246`).
The pipeline refusal therefore discarded the in-memory suite result, and the emitted stdout has no
suite-count section (`W362_GATE_RECEIPT.json:1-8`).

| Measure | Measured |
|---|---|
| Suite return code | NOT PRODUCED |
| Passed tests | NOT PRODUCED |
| Failed tests | NOT PRODUCED |

## Discrepancies

1. The lane predicts the complete refusal list is exactly
   `["SEMANTIC_COVERAGE_REVIEW_MISSING"]`
   (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:31-33`). The one gate invocation
   instead stopped earlier with the singular refusal `EXPECTED_DIGEST_MISMATCH` for
   `RULE2-01-RED` (`W362_GATE_RECEIPT.json:1-8`).
2. The copied bundle is internally inconsistent at the refusal pointer: the catalog pins
   `3cf30e13db25a99093d9087c374c05dabbc6ca0a33ad6cebdfdd1d28df42b94d`, while the copied golden
   and the copied manifest pin measure
   `31646561c134e4e6097a43ff1a9ffee8cbcc68439acc05b3947690ab8782a4fb`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:26-31`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:78-81`).
   Per the lane's explicit “fix nothing” instruction, this was not repaired
   (`C:/tmp/LANE_PROMPTS_20260828/LANE_W362_COPIES_SEAL17_GATE.md:31-33`).
3. Because the gate stopped on that early refusal, the predicted 10/10 probe result and green
   contract-suite counts were not emitted and are `NOT PRODUCED`, not PASS
   (`W362_GATE_RECEIPT.json:1-8`).
