# W204 Gate Rerun Report

## Verdict

**13/17 MATCH; 0 KERNEL-SHORT, 0 GOLDEN-OVER, 4 DESIGN-GAP.** The measured result is one
MATCH below the lane's non-binding 14/17 prediction
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W204_GATE_RERUN.md:18-19`). The three repaired
GOLDEN-OVER assertions are gone, but `RULE2-07-RED` now exposes a later, previously masked
trade-row member mismatch. No behavior or sealed artifact was authored to force the predicted
count.

Finding count: **4 remaining gate mismatches, all DESIGN-GAP; 3 discrepancies recorded.**

This was a **T2 evidence rerun** on branch
`feature/wp-p0-12-corrected-vnext-20260831` in `C:\WP012BUILD`, the exact branch/worktree fixed by
the lane specification, which also states this is the only lane in the worktree
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W204_GATE_RERUN.md:3-5`). Pre-write Git status was clean.
No live, scheduled, host, broker, venue, deployment, credential, Pine, adapter, schema, parity, or
network dependency was used. Durable live-dependency status remains **NOT VERIFIED** because the
repository's session-lock file is a mirror/history rather than a collision guard (`AGENTS.md:50-56`).

## Phase-A exact-source refresh

Source: `C:\tmp\P012_CONTRACT_TABLES_W127\`. Before copying, an independent byte-level check
recomputed all **19/19** manifest member digests and byte counts, recomputed the manifest-defined
sorted `path:sha256` seal, and recomputed all **17/17** catalog-to-2.0.0-golden bindings. All
matched. The source manifest records `DERIVATIONS.md` and `scenario_catalog.json` as seal members
(`C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:75-83`) and records seal
`d642252ed2e16b6a8a2f336e21cb9acb63890008864062c8706fce4672eab438`
(`C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:377-391`).

Of the same 38 source-to-repository mappings W188 compared, 31 were already byte-identical and
seven differed. Only the seven differing source members were copied, byte-for-byte. The anchor
sidecar was then updated to the copied anchor's exact SHA-256, the procedure W188 recorded
(`W188_KERNEL_RESUME_REPORT.md:20-29`). SHA-256 values below are measured file digests; every
copied member's after digest equals its source digest.

| Repository member | Before SHA-256 | After/source SHA-256 | Action |
|---|---|---|---|
| `golden/corrected_vnext/RULE2-07-GREEN.json` | `a7e6a59a4040d6eee8be42c24d28f46a5c9f4af2bd131c19bf6e768f9819ee48` | `1acd5a74f98d22165971486d6a2ede029f58bf984f85181617055ca473644a4a` | Exact source copy |
| `golden/corrected_vnext/RULE2-07-RED.json` | `88b446ad3a5d7974616ba1253c345f7a8f321fc60b5a5a55f70c57ebf74bf4ef` | `0634a43fa242351072de26e027584105dae81426a5ac622219f3a6ccac706da0` | Exact source copy |
| `golden/corrected_vnext/RULE2-08-RED.json` | `926a3318123e1b5380b152cb08dd2b07bebbf18894b15771b20126cc916a8809` | `6e76d54f82a5486d0500a9a8c2e0792e186db3a5d1f8ec8d18eff8eee27e4b17` | Exact source copy |
| `tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json` | `4f60cf7ad5055f87381262dce1d196f4d2c992f5f5d31d8a2cdd5d5b51055c8c` | `7970a21075caef2b77249bf106112b306d88564262b818cee5a7ad1b94d501d4` | Exact source copy |
| `tests/corrected_vnext/contracts/DERIVATIONS.md` | `ac12f8a24c9b45da879046b35e2b4f7399c04d447d8de1324c99e1515ef679b4` | `b0fa1e4136eda00b82bfacfe0c2dee67f928f3dcbcdb3a5e383c958129f41218` | Exact source copy |
| `tests/corrected_vnext/contracts/scenario_catalog.json` | `795891500bb93763fe91dde7cfcc11687e414b9118d301b3f422789f02eb9da2` | `5e8f1ce4c1e9a148b21ed3a5f76bb0a076947013feeb182a684fe0971e461570` | Exact source copy |
| `tests/corrected_vnext/contracts/implementation_anchor.json` | `c85a77b492e27c91d716ea044e22470d8b8483d95c7259327047aa1c66be14b6` | `2c8969e073cb97385e8760b764766732d95768a76cd05a5e4ee562c959460a9f` | Exact source copy from `IMPLEMENTATION_ANCHOR_DRAFT.json` |
| `tests/corrected_vnext/contracts/implementation_anchor.json.sha256` | `afa6e281f8efb68b876ceda36de6a666cb55c8d13464e2115e2e976770c93072` | `ea3f898013e2681beab4494263a99e24e67d63e345afbd62aa4bab5d932bbff2` | Sidecar content changed from the old anchor digest to `2c8969e0...` |

After refresh, the repository copy independently re-verified **19/19** manifest members,
**17/17** catalog bindings, the anchor sidecar, and the same computed/recorded seal
`d642252ed2e16b6a8a2f336e21cb9acb63890008864062c8706fce4672eab438`. The verifier implements
these member, seal, anchor, and sidecar checks at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:938-962`.

Refresh commit: `8c7ef852` - `chore(mtc-v2): refresh contract bundle seal 5`.

## Canonical gate first

The canonical command was run from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` before the direct
per-row measurement:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
```

Exact Python exit code: **2**. Full refusal output:

```json
{
  "claim_label": "BOUNDED_CORRECTION_EVIDENCE_REFUSED",
  "mode": "full-gate",
  "refusal": {
    "check_id": "BASELINE_SEAL_IDENTITY_MISMATCH",
    "detail": "d642252ed2e16b6a8a2f336e21cb9acb63890008864062c8706fce4672eab438"
  }
}
```

The two compared identities are:

- Current computed and anchor-pinned seal:
  `d642252ed2e16b6a8a2f336e21cb9acb63890008864062c8706fce4672eab438`
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-4`).
- Frozen baseline-consumed seal:
  `02b47a8e5c4a1a9ab9a671f5a14a3dc89f13fb80584dfd8648784d69515a0858`
  (`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:13`).

The verifier compares those identities and raises this refusal at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:965-968`.
That validation is called before the scenario loop begins
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1315-1327`).
No baseline file was edited, no baseline was re-run, and no bypass flag was passed.

## Seventeen-row direct measurement

Because the canonical gate correctly refused before its row loop, all 17 RED/GREEN rows were then
measured in memory by importing and calling the repaired harness's
`execute_corrected_scenario()` followed by `compare_scoped_expected()`. Those are the real executor
and scoped comparator at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:584-716`
and `:717-760`; the repaired canonical pipeline calls the same pair at `:1325-1327`. No observed
artifact was written.

Canonical node notation comes from `canonical_node()` at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:157-175`:
`I` is an integer and `S` is a length-tagged Base64 UTF-8 string.

| Scenario | Result | First differing pointer | Observed | Golden | Classification |
|---|---|---|---|---|---|
| RULE2-01-RED | MATCH | - | - | - | MATCH |
| RULE2-01-GREEN | MATCH | - | - | - | MATCH |
| RULE2-02-RED | MATCH | - | - | - | MATCH |
| RULE2-02-GREEN | MATCH | - | - | - | MATCH |
| RULE2-03-RED | MATCH | - | - | - | MATCH |
| RULE2-03-GREEN | MATCH | - | - | - | MATCH |
| RULE2-04-RED | MISMATCH | `/RESULT_SURFACE/trades/0/exit_fill_price` | absent | `I:90` | **DESIGN-GAP** - lifecycle trade rows are required, but their member set is not closed (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:480`, `:1130-1139`). |
| RULE2-04-GREEN | MATCH | - | - | - | MATCH |
| RULE2-05-RED | MATCH | - | - | - | MATCH |
| RULE2-05-GREEN | MATCH | - | - | - | MATCH |
| RULE2-06-RED | MISMATCH | `/EVENT_SURFACE/decision_events/2/touched_exit_ids/0` | `S:4:U1RPUA==` (`STOP`) | `S:11:VEFSR0VULU5FQVI=` (`TARGET-NEAR`) | **DESIGN-GAP** - the chosen target order is fixed, but the all-touched receipt order is not (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:339-353`, `:1035`). |
| RULE2-06-EQUAL-PRICE-RED | MISMATCH | `/EVENT_SURFACE/decision_events/2/touched_exit_ids/0` | `S:4:U1RPUA==` (`STOP`) | `S:11:VEFSR0VULU5FQVI=` (`TARGET-NEAR`) | **DESIGN-GAP** - the same unset all-touched ordering. |
| RULE2-06-GREEN | MATCH | - | - | - | MATCH |
| RULE2-07-RED | MISMATCH | `/RESULT_SURFACE/trades/0/exit_fill_price` | absent | `I:100` | **DESIGN-GAP** - the design fixes a timed exit final fill of 100 but does not close the lifecycle trade-row member set (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:390-392`, `:480`, `:1130-1139`). The golden asserts `exit_fill_price` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-RED.json:50`), while the kernel's existing closed-lifecycle representation emits `exit_ids` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:696-721`). Choosing either schema here would invent the missing contract. |
| RULE2-07-GREEN | MATCH | - | - | - | MATCH |
| RULE2-08-RED | MATCH | - | - | - | MATCH |
| RULE2-08-GREEN | MATCH | - | - | - | MATCH |

Measured summary: **13/17 MATCH, 4/17 MISMATCH; 0 KERNEL-SHORT, 0 GOLDEN-OVER, 4 DESIGN-GAP.**

## What changed versus W188

W188 measured **11/17 MATCH, 3 GOLDEN-OVER, 3 DESIGN-GAP**
(`W188_KERNEL_RESUME_REPORT.md:121-126`). The re-sealed source repairs all three former
GOLDEN-OVER assertions: both RULE2-07 guard-basis values now use `GROSS-MINUS-FEES`, and
RULE2-08-RED no longer carries a guards object
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-RED.json:54-55`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-GREEN.json:38`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-RED.json:93-95`).

Consequently, RULE2-07-GREEN and RULE2-08-RED move to MATCH. RULE2-07-RED does not: once its old
guard-basis first difference is repaired, the comparator advances to the later
`/RESULT_SURFACE/trades/0/exit_fill_price` mismatch. The three W188 DESIGN-GAP rows remain
unchanged (`W188_KERNEL_RESUME_REPORT.md:114-119`). Net movement is therefore **+2 MATCH**, not
+3: `11/17 -> 13/17`.

## Contract self-tests

Both commands were run after the 17-row measurement:

| Command | Exit | Measured result |
|---|---:|---|
| `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q` | 0 | **220 passed** |
| `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest` | 0 | **18 checks:** 3 `PASS`, 14 `DETECTED`, 1 `DETECTED:/a/1` |

The built-in selftest is explicitly non-accepting and returns its check receipt from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1375-1430`.

## Discrepancies

1. The lane predicted 14/17 but explicitly said the number must be measured
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W204_GATE_RERUN.md:18-19`). The measured value is 13/17
   because repaired RULE2-07-RED exposes a later DESIGN-GAP trade-row mismatch.
2. W188 reported the canonical refusal as exit 1 (`W188_KERNEL_RESUME_REPORT.md:96-99`). The exact
   Python process exit measured now is 2, matching the verifier's refusal returns
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1477-1488`).
3. W204's refresh shorthand names goldens, catalog, manifest, and anchor
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W204_GATE_RERUN.md:23-25`), but the new sealed manifest also
   pins changed `DERIVATIONS.md` bytes (`C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:75-78`).
   Following W188's actual refresh method and the repository seal required copying that differing
   member too; omitting it would make the repository bytes disagree with the sealed manifest.

## Explicit scope statement

- **No golden, catalog, manifest, seal, input, sidecar, or baseline file was hand-edited.** The
  only sealed-member changes were the seven mandated exact byte copies listed in the digest table;
  the anchor sidecar was updated only to the copied anchor's exact SHA-256. No input or baseline
  byte changed, and no sealed content was authored or transformed by this lane.
- No DESIGN-GAP behavior was implemented. In particular, no trade-row member set and no
  `touched_exit_ids` ordering rule was invented.
- No baseline run, observed-artifact generation, backtest, optimization, server, launcher, broker,
  venue, host, network, credential, deployment, Pine, adapter, schema, parity, push, pull request,
  merge, or live-trading action was performed.
