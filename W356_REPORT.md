# W356 Report — Probe Manifest Agreement

Verdict: **PASS with the two expected pre-existing design-pin self-test failures.** The two incorrect probe declarations now agree with the sealed catalog, and the verifier refuses any future catalog/manifest disagreement.

All repository-relative evidence paths below are rooted at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/` unless stated otherwise.

## Scope and starting state

- Worktree: `C:\WP012BUILD`.
- Starting commit: `eaad10f698f3f6e8edf800ccd2e522c98bd39763`, measured with `git rev-parse HEAD` before any write.
- Branch: `feature/wp-p0-12-corrected-vnext-20260831`, measured with `git branch --show-current`; it is not `master`, as required by `AGENTS.md:48-49`.
- Starting worktree: clean, measured with `git status --short --branch` before any write.
- Gate-1 tier: **T1**, because the primary change is a non-economic verifier change; the manifest corrections and this report are supporting T2 artifacts. The repository requires the highest-overlap T0/T1/T2/T3 classification at `AGENTS.md:38-40`.
- Write lane: the branch and worktree above; exact changed paths are listed below. Live-dependency status: none—only local files and the authorized local self-tests were used.

## Pre-change ten-probe measurement

This table was measured before any write. For the two files later edited, `eaad10f6:` identifies the exact starting-commit byte at line 1.

| Probe | Catalog `expected_first_changed_node` | Probe manifest value at start | Agreement |
|---|---|---|---|
| `PROBE-P012-01-A` | `/EVENT_SURFACE/fill_events/0/quantity` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2208`) | `/EVENT_SURFACE/fill_events/0/quantity` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/modification_manifest.json:1`) | Yes |
| `PROBE-P012-01-B` | `/EVENT_SURFACE/fill_events/0/quantity` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2229`) | `/EVENT_SURFACE/fill_events/0/quantity` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-B/modification_manifest.json:1`) | Yes |
| `PROBE-P012-02-A` | `/RESULT_SURFACE/admitted` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2250`) | `/RESULT_SURFACE/admitted` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-02-A/modification_manifest.json:1`) | Yes |
| `PROBE-P012-03-A` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2271`) | `BLOCKED-MISSING-RECORD-BYTES` (`eaad10f6:mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json:1`) | **No** |
| `PROBE-P012-04-A` | `/EVENT_SURFACE/fill_events/0/final_fill_price` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2292`) | `/EVENT_SURFACE/fill_events/0/final_fill_price` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-04-A/modification_manifest.json:1`) | Yes |
| `PROBE-P012-05-A` | `/EVENT_SURFACE/fill_events/0/final_fill_price` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2313`) | `/EVENT_SURFACE/fill_events/0/final_fill_price` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-A/modification_manifest.json:1`) | Yes |
| `PROBE-P012-05-B` | `/EVENT_SURFACE/fill_events/0/final_fill_price` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2334`) | `/EVENT_SURFACE/fill_events/0/final_fill_price` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-B/modification_manifest.json:1`) | Yes |
| `PROBE-P012-06-A` | `/EVENT_SURFACE/fill_events/0/exit_id` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2355`) | `/EVENT_SURFACE/fill_events/0/exit_id` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-06-A/modification_manifest.json:1`) | Yes |
| `PROBE-P012-07-A` | `/EVENT_SURFACE/fee_events/1/liquidity_role` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2376`) | `/EVENT_SURFACE/cash_events/1/signed_delta` (`eaad10f6:mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification_manifest.json:1`) | **No** |
| `PROBE-P012-08-A` | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2397`) | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/modification_manifest.json:1`) | Yes |

Result: exactly `PROBE-P012-03-A` and `PROBE-P012-07-A` disagreed; the other eight agreed. The measured table contains all ten catalog probe rows, whose conservation count is also enforced by `mtc_v2/tests/corrected_vnext/verify_bceg.py:2490-2493`.

## Pre-change harness sites

The probe manifest member was required but not bound to the catalog:

```python
required_manifest = {
    # ...
    "expected_first_changed_node",
}
```

Evidence: `mtc_v2/tests/corrected_vnext/verify_bceg.py:2752-2769`.

The only existing catalog/manifest binding comparison checked `target_kind`, `modified_copy_path`, and `expected_failed_check`, but omitted `expected_first_changed_node`:

```python
manifest["target_kind"] != row["target_kind"]
or manifest["modified_copy_path"] != row["modified_copy_path"]
or manifest["expected_failed_check"] != row["expected_failed_check"]
```

Evidence: `mtc_v2/tests/corrected_vnext/verify_bceg.py:2770-2779`. These lines are unchanged by W356; the new standalone comparison follows them at `mtc_v2/tests/corrected_vnext/verify_bceg.py:2780-2791`.

## Which declaration was wrong

### `PROBE-P012-03-A`

The manifest was wrong; the catalog is supported by the actual modified copy.

- The probe row identifies an input probe based on `RULE2-03-RED`, points to the record directory, expects `RECORD_IDENTITY_PREFLIGHT`, and names the record path as both expected and comparator-first changed artifact (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2256-2272`).
- The patch changes one byte in the named record: `price_tick` changes from `0.5` to `0.6` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification.patch:1-5`).
- The artifact validator requires that the modified-copy member set contain that named JSON plus its sidecar, that the sidecar remain unchanged, and that the JSON differ at exactly the declared byte offset (`mtc_v2/tests/corrected_vnext/verify_bceg.py:2892-2929`).
- The retained detached digest is `498ae36ea28a7f40df519724b1fb80d98a68c7261cda8fc7c0c3d6893c909a9a` (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/record/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json.sha256:1`), while the modified JSON measured `e0c6425a13ebc312eb00c3497510f804e3a092ab1627a5f1b3aa744ffe54221f`. The record-reference verifier refuses when actual, expected, and sidecar digests disagree (`mtc_v2/tests/corrected_vnext/verify_bceg.py:1171-1189`).
- Therefore the concrete changed artifact is `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json`; the old placeholder `BLOCKED-MISSING-RECORD-BYTES` was stale. The catalog note records the same closure and path (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2273`).

### `PROBE-P012-07-A`

The manifest was wrong; it carried the comparator-first cash node rather than the design-named expected changed node.

- The patch changes `_fee_rows` so a `MARKET_EXIT` is classified as `MAKER` instead of using the declared role (`mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification.patch:1-5`).
- The sealed cost record declares `MARKET_EXIT` as `TAKER`, `maker_rate` as `0.00015`, and `taker_rate` as `0.001` (`mtc_v2/core/economic_records/costs/SYNTH-COST-RULE2-07-RED-V1.json:1`).
- `_fee_rows` uses the role to select the rate, derives the negative cash delta, and writes that same role to `FeeEvent.liquidity_role` (`mtc_v2/core/economics.py:299-335`).
- The expected surface's second row is the `MARKET_EXIT`; it records `fee_events[1].liquidity_role = TAKER`, rate `0.001`, fee `0.1`, and delta `-0.1` (`mtc_v2/golden/corrected_vnext/RULE2-07-RED.json:39-40`). The joined second cash row records `signed_delta = -0.1` (`mtc_v2/golden/corrected_vnext/RULE2-07-RED.json:33-36`).
- The catalog deliberately separates the design-named changed member `/EVENT_SURFACE/fee_events/1/liquidity_role` from the UTF-8 traversal-order comparator-first member `/EVENT_SURFACE/cash_events/1/signed_delta` (`mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2375-2378`). The manifest had copied the latter into the former field.

The evidence supports moving only the two manifest declarations. No catalog, kernel, golden, input, bundle manifest, anchor, or baseline byte was changed.

## Manifest corrections and hashes

| Manifest | Before SHA-256 | After SHA-256 | Corrected value |
|---|---|---|---|
| `mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json:1` | `d2ec9000ed503947e4b86893b2a9b0cc258c765cecfb5b638a99840cb9dd1ebe` | `a496c97b16db3d219e3b2a7ff0222c70e9ce00fb38f057082a2706fbfc64e578` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` |
| `mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification_manifest.json:1` | `ed5bf6bdf3e3c1548a07c56f1bf0702798edb61b28abe1f8abc81f77d9e614f0` | `a872886751d72851f5fbfcba6027377e1d91948972bef99a74ba55126c2033a5` | `/EVENT_SURFACE/fee_events/1/liquidity_role` |

The before and after hashes were measured over exact file bytes with SHA-256. A post-change byte check measured, for each file, first byte `{` (`0x7b`), exactly one LF, no CR, and final byte LF (`0x0a`). The diff changes only the property value, so compact formatting and key order are preserved. The catalog still carries the two old manifest digest pins at `mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2268-2269` and `mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:2373-2374`; re-seal #17 must re-pin them as directed by the lane specification.

## New refusal

Refusal id: `PROBE_MODIFICATION_MANIFEST_CATALOG_MISMATCH`.

The verifier now directly compares `manifest["expected_first_changed_node"]` with `row["expected_first_changed_node"]` and refuses disagreement while reporting both values (`mtc_v2/tests/corrected_vnext/verify_bceg.py:2780-2791`). The pre-existing binding refusal remains unchanged immediately above it (`mtc_v2/tests/corrected_vnext/verify_bceg.py:2770-2779`); no other refusal was edited.

## Self-tests and RED/GREEN evidence

### 1. Agreeing documents pass

`test_w356_agreeing_probe_manifest_and_catalog_are_accepted` drives an agreeing real probe through the artifact validator and requires a pinned accepted artifact (`mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1678-1683`). If agreement were incorrectly refused (for example, an inverted comparison), the uncaught refusal would fail this test before the assertion.

### 2. Synthetic disagreement is refused

`test_w356_probe_manifest_catalog_disagreement_is_refused` changes only the catalog row copy's node and requires the new refusal id (`mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1686-1699`). If the comparison/refusal is removed, the validator returns normally and `pytest.raises` fails with `DID NOT RAISE`.

RED command before the check existed:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -q -k 'w356_agreeing or w356_probe_manifest_catalog_disagreement'
.F
FAILED test_w356_probe_manifest_catalog_disagreement_is_refused - Failed: DID NOT RAISE
1 failed, 1 passed, 159 deselected in 1.59s
```

GREEN after the check:

```text
..
2 passed, 159 deselected in 0.67s
```

### 3. All ten real probe documents agree and do not trigger the new refusal

`test_w356_all_real_probe_manifests_agree_with_catalog` requires exactly ten rows, independently asserts every catalog/manifest node is equal, then drives every real artifact through the validator (`mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1702-1734`). Because the sealed catalog cannot move in this lane, the test substitutes each manifest's measured current digest into a row copy at lines 1725-1728; this models only the pending re-seal #17 digest re-pin and does not weaken the node comparison. Reverting either manifest correction fails the equality assertion at lines 1715-1718; an erroneous refusal on agreement fails the validator call at lines 1730-1734.

Targeted result after all W356 changes:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -q -k w356
...
3 passed, 159 deselected in 6.19s
```

## Authorized suite

Exact command, run from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
```

Measured starting result at `eaad10f6`: **320 passed, 2 failed, 322 total** in 7.11 seconds. Measured final result: **323 passed, 2 failed, 325 total** in 13.39 seconds. The three-test increase is exactly the three W356 tests at `mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1678-1734`.

The same two tests failed before and after W356:

- `test_legacy_reproduction_refuses_one_ulp_actual` (`mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1602-1630`).
- `test_receipt_accounts_for_every_blocked_expected_node` (`mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1632-1659`).

Both stop in the pre-existing `DESIGN_PIN_MISMATCH` check, which measures the actual design SHA-256 and line count and refuses disagreement with the manifest pin (`mtc_v2/tests/corrected_vnext/verify_bceg.py:2281-2316`). No W356 test failed.

## Canonical gate not run

**No canonical gate run was made.** The bundle manifest pins design v1.17, SHA-256 `5c657ec93c714b59d56a9ca99e7f42005061ceaad6f8d2889e2d691af3381c09`, and 1800 lines (`mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-17`). The absolute-path design authority currently identifies itself as v1.18 (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1`) and measured SHA-256 `03fdf5952a2365b2de60b55292a1bd50fce8c6c51788c19b59cecc5d8f5b3c94` over 1843 lines. Therefore the gate would stop at `DESIGN_PIN_MISMATCH` before reaching W356; the lane explicitly authorizes only the contract self-test suite (`C:\tmp\LANE_PROMPTS_20260828\LANE_W356_PROBE_MANIFEST_AGREEMENT.md:9-14`). Re-seal #17 is the authorized place to absorb the design and changed-manifest pins.

## Changed paths

- `mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json:1`
- `mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification_manifest.json:1`
- `mtc_v2/tests/corrected_vnext/verify_bceg.py:2780-2791`
- `mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1662-1734`
- `W356_REPORT.md`

`git diff --check` produced no errors before report creation. The measured diff before this report contained only the four authorized implementation/test/manifest paths above; this report is the fifth authorized path. No host, network, broker, venue, deployment, backtest, optimization, server, launcher, or artifact-generation action was performed.

## Discrepancies

1. The lane prompt says the two pre-existing design-pin failures make the HEAD suite `316/318` (`C:\tmp\LANE_PROMPTS_20260828\LANE_W356_PROBE_MANIFEST_AGREEMENT.md:13-14`). The repository measured **320 passed / 322 total** before W356 and **323 passed / 325 total** after adding the three W356 tests, with exactly the same two pre-existing failures. Per C-2, the measured repository counts control.

No other prompt/repository discrepancy was measured.
