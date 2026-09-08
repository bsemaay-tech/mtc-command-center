# W246 Gate Rerun Report — Seal #8

## Verdict

**15/17 MATCH, 2/17 MISMATCH; 2 KERNEL-SHORT, 0 GOLDEN-OVER, 0 DESIGN-GAP.**

The two remaining mismatches are one-binary64-step differences at
`/RESULT_SURFACE/equity_curve/last` in `RULE2-06-RED` and
`RULE2-06-EQUAL-PRICE-RED`. The design requires `last` to be formed from `first` by adding every
in-window `cash_events.signed_delta` in array order
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1070-1078`), while the kernel groups the
in-window deltas with `sum()` before adding that group to `first`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:790-811`). The exact-node
comparator distinguishes the resulting adjacent binary64 values
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:151-173`).

Finding count: **2 gate mismatches, both KERNEL-SHORT; 3 discrepancies recorded.** No repair was
attempted because the lane requires an honest classification and stop rather than changing a number
to reach the prediction (`C:\tmp\LANE_PROMPTS_20260828\LANE_W246_GATE_RERUN_SEAL8.md:26-29,56-60`).

This was a **T2 evidence rerun** on branch
`feature/wp-p0-12-corrected-vnext-20260831` in `C:\WP012BUILD`. Those are the branch/worktree fixed
by the lane specification, which also records this as the only lane there
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W246_GATE_RERUN_SEAL8.md:4-6`). The exact write set was the
nine refresh paths below plus this report. No live, scheduled, host, broker, venue, deployment,
credential, Pine, adapter, schema, parity, or network dependency was used. No push, merge, pull
request, or `master` write was performed.

## Phase-A exact-source refresh

Source: `C:\tmp\P012_CONTRACT_TABLES_W127\`.

Before copying, an independent byte-level check measured **19/19 manifest members**, **17/17
catalog-to-2.0.0-golden bindings**, and **17/17 catalog input bindings** valid. Recomputing SHA-256
over the LF-joined, ordinally sorted manifest `path:sha256` lines produced
`4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461`, equal to the manifest and
anchor pins (`C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:543-556`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5`).
The verifier's corresponding member, seal, anchor, and sidecar checks are at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:933-962`.

Of W204's 38 source-to-repository mappings, 30 were already byte-identical and eight differed. Only
those eight were copied byte-for-byte. The detached sidecar was then changed mechanically to the
copied anchor's exact SHA-256, as W204 did (`W204_GATE_RERUN_REPORT.md:32-49`). The source manifest
identifies the revised sealed members and says the other source members stayed byte-identical
(`C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:735-776`). All values below are
SHA-256 digests measured from the bytes immediately before and after the copy.

| Repository member | Before SHA-256 | After/source SHA-256 | Action |
|---|---|---|---|
| `golden/corrected_vnext/RULE2-04-RED.json` | `9f7a541c08bb477b0f0a68708f01ff5eff39bc736120ad8122f77293f6bd02d1` | `50a990c2005ade1fa5db41cdd00f7bd194e0e89db1f3cd1b24d3d71e693aa85c` | Exact source copy |
| `golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json` | `102aa04e93dfa9c56cebc5932b3e330773370fa3f0de82770b776c7e55e661f3` | `c05a51eb1e03b8864c495a3d48d3ccd722a2d598489038f055d755f32cb31de0` | Exact source copy |
| `golden/corrected_vnext/RULE2-06-RED.json` | `25c747ac53111c5106fd9bf393f4aced9d5ebe1b3467ad9fd6b33a3fc4605613` | `9d9d3a9748571d63c8790d9b7ef5df398ed945f75c59b7148975debfe167a581` | Exact source copy |
| `golden/corrected_vnext/RULE2-07-RED.json` | `0634a43fa242351072de26e027584105dae81426a5ac622219f3a6ccac706da0` | `e4d966eee8587ca3d645e3abd9a98847daf8f41a3743250563624975f926435b` | Exact source copy |
| `tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json` | `7970a21075caef2b77249bf106112b306d88564262b818cee5a7ad1b94d501d4` | `974fca3278832c2a565e626e3f6ed385fcae3ac64d2141e3398d5fa29d63fc77` | Exact source copy |
| `tests/corrected_vnext/contracts/DERIVATIONS.md` | `b0fa1e4136eda00b82bfacfe0c2dee67f928f3dcbcdb3a5e383c958129f41218` | `a8440a1250fed65e77ed760a0ab16db889592e737a731d12aa823f65fcc4ad50` | Exact source copy |
| `tests/corrected_vnext/contracts/scenario_catalog.json` | `5e8f1ce4c1e9a148b21ed3a5f76bb0a076947013feeb182a684fe0971e461570` | `f8e788d808f26c427eaefdd3f521998b0fdcea57a469792792abab260efea603` | Exact source copy |
| `tests/corrected_vnext/contracts/implementation_anchor.json` | `2c8969e073cb97385e8760b764766732d95768a76cd05a5e4ee562c959460a9f` | `343aa91b2bcd5f3087f3d4170f330047ab72c6992f38f253e1376904b0859ce8` | Exact source copy from `IMPLEMENTATION_ANCHOR_DRAFT.json` |
| `tests/corrected_vnext/contracts/implementation_anchor.json.sha256` | `ea3f898013e2681beab4494263a99e24e67d63e345afbd62aa4bab5d932bbff2` | `d64cb184873c89db32931f70d4927ea6fa4f6a31b7ffab0cf67489991577709c` | Mechanical sidecar value `343aa91b...` plus final LF |

The four new golden member digests and the new `DERIVATIONS.md` and catalog digests are independently
pinned in the source manifest (`C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:143-152,189-227`).
After refresh, all **38/38** source-to-repository mappings were byte-identical; the anchor sidecar
contained the anchor digest exactly. Refresh commit: **`18dbe5de`**, `chore(mtc-v2): refresh
contract bundle seal 8`, with `APPROVED-PATCH-PLAN: W246` and nine explicitly staged paths.

## Canonical gate first

This exact command was run from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` after the refresh
commit and before any direct row measurement, as required
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W246_GATE_RERUN_SEAL8.md:31-42`):

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
    "detail": "4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461"
  }
}
```

The two identities compared were:

- current computed and anchor-pinned seal:
  `4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461`
  (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5`);
- frozen baseline-consumed seal:
  `02b47a8e5c4a1a9ab9a671f5a14a3dc89f13fb80584dfd8648784d69515a0858`
  (`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:9-18`).

The verifier raises this refusal before its scenario loop
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:964-968,1315-1327`)
and returns process exit 2 for a refusal
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1477-1487`).
No baseline file was edited, no baseline was re-run, and no bypass flag was used, preserving owner
Q3 (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:625-636`).

## Seventeen-row direct measurement

Because the canonical gate refused before its row loop, the 17 RED/GREEN rows were measured in
memory with the repaired executor `execute_corrected_scenario()` followed immediately by the scoped
comparator `compare_scoped_expected()`. These are the same functions the canonical pipeline calls
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:584-716,717-770,1320-1327`).
No observed artifact was written.

Evidence-path shorthand in the table: `P012_FRESH_DESIGN_V1.md` is
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`; `golden/...` and `core/...` are beneath
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/`.

An initial measurement wrapper resolved the package root one directory too high and exited 1 on a
missing catalog before entering the row loop. The corrected wrapper used the `mtc_v2` package root,
exited 0, and executed each of the 17 RED/GREEN rows once. The table below is that successful run.
`F` is the verifier's canonical IEEE-754 binary64 node notation
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:151-173`).

| Scenario | Result | First differing pointer | Observed | Golden | Classification |
|---|---|---|---|---|---|
| RULE2-01-RED | MATCH | - | - | - | MATCH |
| RULE2-01-GREEN | MATCH | - | - | - | MATCH |
| RULE2-02-RED | MATCH | - | - | - | MATCH |
| RULE2-02-GREEN | MATCH | - | - | - | MATCH |
| RULE2-03-RED | MATCH | - | - | - | MATCH |
| RULE2-03-GREEN | MATCH | - | - | - | MATCH |
| RULE2-04-RED | MATCH | - | - | - | MATCH |
| RULE2-04-GREEN | MATCH | - | - | - | MATCH |
| RULE2-05-RED | MATCH | - | - | - | MATCH |
| RULE2-05-GREEN | MATCH | - | - | - | MATCH |
| RULE2-06-RED | MISMATCH | `/RESULT_SURFACE/equity_curve/last` | `F:0x1.fb68189374bc6p+9` | `F:0x1.fb68189374bc7p+9` | **KERNEL-SHORT** — design requires ordered addition to `first`; the golden records that ordered formula, while the kernel changes the binary64 grouping (`P012_FRESH_DESIGN_V1.md:1072-1078`; `golden/corrected_vnext/RULE2-06-RED.json:54,78`; `core/results.py:798-810`). |
| RULE2-06-EQUAL-PRICE-RED | MISMATCH | `/RESULT_SURFACE/equity_curve/last` | `F:0x1.f8e8624dd2f1ap+9` | `F:0x1.f8e8624dd2f1bp+9` | **KERNEL-SHORT** — same ordered-addition requirement and grouping defect (`P012_FRESH_DESIGN_V1.md:1072-1078`; `golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json:55,81`; `core/results.py:798-810`). |
| RULE2-06-GREEN | MATCH | - | - | - | MATCH |
| RULE2-07-RED | MATCH | - | - | - | MATCH |
| RULE2-07-GREEN | MATCH | - | - | - | MATCH |
| RULE2-08-RED | MATCH | - | - | - | MATCH |
| RULE2-08-GREEN | MATCH | - | - | - | MATCH |

Measured summary: **15/17 MATCH, 2/17 MISMATCH; 2 KERNEL-SHORT, 0 GOLDEN-OVER, 0 DESIGN-GAP.**

The classification is not based only on decimal display. The design makes `last` equal to `first`
plus every delta **in array order** (`P012_FRESH_DESIGN_V1.md:1072-1078`) and makes finite JSON
fractional numbers exact compared binary64 nodes (`P012_FRESH_DESIGN_V1.md:489-517`). The two
goldens spell the required event-by-event formulas and the expected decimal results
(`golden/corrected_vnext/RULE2-06-RED.json:54,78`;
`golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json:55,81`). The kernel instead calculates
`first + sum(in_window_deltas)` (`core/results.py:798-810`). Executing both groupings reproduced the
two adjacent node pairs in the table. This is an implementation shortfall against a closed design,
not an overreaching golden or an open design choice.

## What changed versus W204's 13/17

W204's first-difference table had four DESIGN-GAP rows: trade-row shape for `RULE2-04-RED` and
`RULE2-07-RED`, and all-touched receipt order for the two RULE2-06 RED rows
(`W204_GATE_RERUN_REPORT.md:112-130`). Owner decisions 71 and 72 closed those two contract questions
(`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:596-623`), and
design v1.10 records the resulting four-row revision
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1340-1352`).

After seal #8, `RULE2-04-RED` and `RULE2-07-RED` move to MATCH. The revised stop-first receipt also
removes the old first mismatch from both RULE2-06 RED rows, but the comparator then advances to the
later one-ULP `equity_curve.last` differences reported above. W244 measured zero numeric leaf
changes in all four revised goldens and explicitly preserved `1014.81325`
(`C:\tmp\P012_CONTRACT_TABLES_W127\W244_GOLDEN_SHAPE_REPORT.md:209-227`), so these differences were
latent behind W204's earlier receipt-order pointers rather than introduced by seal #8.

The kernel tree did not move: Git measured the same core tree object
`5b6227882ea567f22f0306c559ea04263a21c542` at W204's final report commit `4d094391` and at the
current seal-refresh commit. Net movement is therefore **+2 MATCH**, `13/17 -> 15/17`, rather than
the predicted `17/17`.

## Contract self-tests

Both required commands were run after the 17-row measurement:

| Command | Exit | Measured result |
|---|---:|---|
| `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q` | 0 | **220 passed** in 1.32 s |
| `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest` | 0 | **18 checks:** 3 `PASS`, 14 `DETECTED`, 1 `DETECTED:/a/1` |

The built-in selftest is explicitly non-accepting and constructs its receipt at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1377-1429`.

## Discrepancies

1. **The 17/17 prediction is not the measured result.** The lane correctly says the number is a
   prediction and requires the actual result (`LANE_W246_GATE_RERUN_SEAL8.md:26-29`). The measured
   result is 15/17 because the two RULE2-06 rows expose later KERNEL-SHORT differences after their
   owner-closed receipt-order mismatches disappear.
2. **The refresh shorthand omits a manifest member that W204's method includes.** The lane names
   “goldens, catalog, manifest, anchor” but also says to refresh exactly as W204 did
   (`LANE_W246_GATE_RERUN_SEAL8.md:33-36`). W204 copied changed `DERIVATIONS.md` bytes and called out
   that requirement (`W204_GATE_RERUN_REPORT.md:32-49,168-173`); seal #8 also pins
   `DERIVATIONS.md` (`CONTRACT_TABLES_MANIFEST.json:143-147`). The changed member was therefore
   copied exactly rather than leaving the repository inconsistent with the sealed manifest.
3. **The fence's word “edit” conflicts literally with the mandated refresh.** The same lane both
   requires exact-source copies and a commit (`LANE_W246_GATE_RERUN_SEAL8.md:33-36`) and says not to
   edit any golden, catalog, manifest, seal, input, sidecar, or kernel file (`:56-60`). Following
   W204's recorded interpretation (`W204_GATE_RERUN_REPORT.md:183-188`), this lane made no authored
   or transformed artifact edit: it performed only the required exact byte copies and the mechanical
   anchor-sidecar digest update.

## Explicit scope statement

- **No golden, catalog, manifest, seal, baseline, or kernel file was edited or authored by this
  lane.** The only byte changes in those artifact families were the eight mandated exact-source
  copies listed in the digest table. They matched the sealed source byte-for-byte before commit.
  The anchor sidecar was updated mechanically to the copied anchor's exact SHA-256. No sealed
  content was authored or transformed.
- No input or baseline byte changed. No kernel byte changed. The two KERNEL-SHORT findings were not
  repaired, and neither expected number was changed.
- No baseline run, observed-artifact generation, backtest, optimization, server, launcher, broker,
  venue, host, network, credential, deployment, Pine, adapter, schema, parity, push, pull request,
  merge, or live-trading action was performed.
