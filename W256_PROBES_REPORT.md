# W256 fail-probe materialization and driving report

## Verdict

**IMPLEMENTATION COMPLETE; PACKAGE REFUSED.** All ten cataloged PROBE variants were materialized and driven through the real `verify_bceg.py` top-level entrypoint. Four were `DETECTED` at the exact cataloged check/node; six were `NOT_DETECTED` because the verifier measured a different first changed node. All ten artifacts validated but remain `PROBE_DIGEST_UNPINNED`, because the catalog still contains the honest marker. The canonical full gate returned exit 2 with `BOUNDED_CORRECTION_EVIDENCE_REFUSED` and 18 refusals. The design requires exact check/node equality for `DETECTED`, and makes every non-`DETECTED` result refusing (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:469-473,542-554).

Finding count: **6** probe-sensitivity findings (`01-A`, `01-B`, `03-A`, `04-A`, `05-A`, `06-A`). They were not “fixed” by strengthening a modification, as explicitly fenced by the lane (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:68-71).

## Authority, lane, and scope

- Worktree: `C:\WP012BUILD`; branch: `feature/wp-p0-12-corrected-vnext-20260831`; implementation commit: `33fdbb685a0e25faf645e6bf77ca3c3c6718fd47`. The lane names this worktree/branch, forbids master/push, and authorizes only the probe tree plus the probe-driving verifier/self-test paths (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:3-9).
- Classification: **T1**, non-economic test/harness code. Live dependency: **none**. No real `mtc_v2/core/**`, golden, catalog, manifest, baseline, or seal byte was changed; these are expressly fenced (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:7-9,66-72).
- The implementation commit contains 1,105 explicit paths: the two authorized harness/test files and 1,103 files below the authorized probes root. Local tests/verifiers are permitted (C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-36).
- No other assistant, model, lane, push, PR, server, backtest, broker, venue, host, or network endpoint was used. Those actions are prohibited by C-1/C-5/C-6 (C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7,25-36).

## Read-before-build declarations

Each catalog quotation below reproduces all execution-binding fields requested by the lane. The cited line span contains the complete row, including its full `note` and both honest digest markers (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:734-933).

### PROBE-P012-01-A

> “`PROBE-P012-01-A` replaces the corrected multiplier with `1` after record validation; the corrected expected producer remains at `5`, so the corrected-expectation check must refuse at the quantity node.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:227)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-01-A; base_scenario_id=RULE2-01-RED; subject_producer_id=KERNEL_2; target_kind=KERNEL; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-01-A/kernel/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-01-A/modification_manifest.json; expected_failed_check=CORRECTED_EXPECTATION; expected_first_changed_node=/EVENT_SURFACE/fill_events/0/quantity; design_lines=220; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT`. The note records D-14 ordering risk at `decision_events` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:734-753).

Exact one modification: `kernel/economics.py`, `_size_quantity`, replace the corrected contract multiplier selection with `multiplier = 1.0`. The recorded one-line patch is the complete change (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/modification.patch:1-5; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/kernel/economics.py:240).

### PROBE-P012-01-B

> “`PROBE-P012-01-B` changes the corrected selector so a supplied binary64 NaN stop returns zero; `RULE2-01-GREEN` still expects fallback quantity `1`, so the corrected-expectation check must refuse at the quantity node.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:227)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-01-B; base_scenario_id=RULE2-01-GREEN; subject_producer_id=KERNEL_2; target_kind=KERNEL; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-01-B/kernel/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-01-B/modification_manifest.json; expected_failed_check=CORRECTED_EXPECTATION; expected_first_changed_node=/EVENT_SURFACE/fill_events/0/quantity; design_lines=220; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:754-773).

Exact one modification: `kernel/economics.py`, `_size_quantity`, change `if stop is not None and math.isfinite(stop):` to `if stop is not None:` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-B/modification.patch:1-5; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-B/kernel/economics.py:241).

### PROBE-P012-02-A

> “Fail probe `PROBE-P012-02-A`: change the corrected comparison to `>` so equality refuses. The RULE-2-GREEN cross-version check must refuse on the admission/refusal projection for `RULE2-02-GREEN`.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:252)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-02-A; base_scenario_id=RULE2-02-GREEN; subject_producer_id=KERNEL_2; target_kind=KERNEL; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-02-A/kernel/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-02-A/modification_manifest.json; expected_failed_check=RULE2_GREEN_CROSS_VERSION_EXPECTATION; expected_first_changed_node=/RESULT_SURFACE/admitted; design_lines=245; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:774-793).

Exact one modification: `kernel/economics.py`, `_resolve_open`, change the minimum-notional refusal predicate from `<` to `<=`, which implements a passing comparison of `>` rather than `>=` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-02-A/modification.patch:1-5; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-02-A/kernel/economics.py:646).

### PROBE-P012-03-A

> “Fail probe `PROBE-P012-03-A`: mutate one record byte without updating the detached digest. The record-identity preflight must refuse before any scenario output exists.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:270)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-03-A; base_scenario_id=RULE2-03-RED; subject_producer_id=KERNEL_2; target_kind=INPUT; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-03-A/record/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json; expected_failed_check=RECORD_IDENTITY_PREFLIGHT; expected_first_changed_node=BLOCKED-MISSING-RECORD-BYTES; design_lines=263; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT`. The note says exact record bytes still do not exist (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:794-813).

Exact one modification: in the INPUT variant, change byte offset 201 from ASCII `5` to `6`, making `price_tick:0.5` become `price_tick:0.6`, while copying the detached `.sha256` byte-for-byte unchanged. The manifest records the one-byte before/after values and the one `INPUT_FILE_PATCH` operation (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json:1; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification.patch:1-5).

### PROBE-P012-04-A

> “Fail probe `PROBE-P012-04-A`: return stop `100` rather than open `90` on RED; the corrected-expectation check must refuse at the fill-price node.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:298)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-04-A; base_scenario_id=RULE2-04-RED; subject_producer_id=KERNEL_2; target_kind=KERNEL; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-04-A/kernel/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-04-A/modification_manifest.json; expected_failed_check=CORRECTED_EXPECTATION; expected_first_changed_node=/EVENT_SURFACE/fill_events/0/final_fill_price; design_lines=291; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT`. The note records D-14 earlier-node risk (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:814-833).

Exact one modification: `kernel/economics.py`, `_touched_candidates`, use `candidate.price` instead of `market.open` for a long stop gap (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-04-A/modification.patch:1-5; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-04-A/kernel/economics.py:544).

### PROBE-P012-05-A

> “Fail probes: `PROBE-P012-05-A` omits the application (actual `100`) and `PROBE-P012-05-B` applies it twice (actual `102`). Each must make the corrected-expectation check refuse at the fill-price node against independent corrected expected `101`.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:326)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-05-A; base_scenario_id=RULE2-05-RED; subject_producer_id=KERNEL_2; target_kind=KERNEL; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-05-A/kernel/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-05-A/modification_manifest.json; expected_failed_check=CORRECTED_EXPECTATION; expected_first_changed_node=/EVENT_SURFACE/fill_events/0/final_fill_price; design_lines=319; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:834-853).

Exact one modification: `kernel/economics.py`, `_fill_price`, return `ceil_price(reference)` for BUY instead of `ceil_price(reference + impact)` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-A/modification.patch:1-5; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-A/kernel/economics.py:275).

### PROBE-P012-05-B

> “Fail probes: `PROBE-P012-05-A` omits the application (actual `100`) and `PROBE-P012-05-B` applies it twice (actual `102`). Each must make the corrected-expectation check refuse at the fill-price node against independent corrected expected `101`.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:326)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-05-B; base_scenario_id=RULE2-05-RED; subject_producer_id=KERNEL_2; target_kind=KERNEL; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-05-B/kernel/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-05-B/modification_manifest.json; expected_failed_check=CORRECTED_EXPECTATION; expected_first_changed_node=/EVENT_SURFACE/fill_events/0/final_fill_price; design_lines=319; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:854-873).

Exact one modification: `kernel/economics.py`, `_fill_price`, return `ceil_price(reference + impact + impact)` for BUY (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-B/modification.patch:1-5; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-B/kernel/economics.py:275).

### PROBE-P012-06-A

> “Its sole recorded modification reverses the `TARGET_FIRST` target-event order in the isolated kernel variant while leaving the declared scenario input and independent `CONTRACT_TABLES` expected artifact unchanged. The corrected-expectation check must refuse at the first changed event sequence node: expected first fill `TARGET-NEAR`, modified-kernel first fill `TARGET-FAR`.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:355)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-06-A; base_scenario_id=RULE2-06-RED; subject_producer_id=KERNEL_2; target_kind=KERNEL; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-06-A/kernel/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-06-A/modification_manifest.json; expected_failed_check=CORRECTED_EXPECTATION; expected_first_changed_node=/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids/0; design_lines=347; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT`. The note records D-14 between the design-named fill event and the cataloged earlier decision event (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:874-893).

Exact one modification: `kernel/economics.py`, `_resolve_exit`, reverse long target price ordering by changing the primary sort key from `price` to `-price` while retaining the exit-id tie-breaker (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-06-A/modification.patch:1-5; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-06-A/kernel/economics.py:787).

### PROBE-P012-07-A

> “Fail probe `PROBE-P012-07-A`: classify one declared taker exit as maker. The corrected-expectation check must refuse at the event-role/rate/fee nodes even if a coincidental rounded total is equal.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:396)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-07-A; base_scenario_id=RULE2-07-RED; subject_producer_id=KERNEL_2; target_kind=KERNEL; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-07-A/kernel/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-07-A/modification_manifest.json; expected_failed_check=CORRECTED_EXPECTATION; expected_first_changed_node=/EVENT_SURFACE/cash_events/1/signed_delta; design_lines=388; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:894-913).

Exact one modification: `kernel/economics.py`, `_fee_rows`, classify only `MARKET_EXIT` as `MAKER`, leaving the declared entry role unchanged and misclassifying the selected exit (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification.patch:1-5; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/kernel/economics.py:299).

### PROBE-P012-08-A

> “Fail probe `PROBE-P012-08-A`: flip the sign for the long positive-rate event. The corrected-expectation check must refuse at the cash-delta node because independent expected `-0.1` differs from actual `+0.1`.” (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:441)

> Catalog row: `role=PROBE; probe_id=PROBE-P012-08-A; base_scenario_id=RULE2-08-RED; subject_producer_id=KERNEL_2; target_kind=KERNEL; modified_copy_path=tests/corrected_vnext/probes/PROBE-P012-08-A/kernel/; modification_manifest_path=tests/corrected_vnext/probes/PROBE-P012-08-A/modification_manifest.json; expected_failed_check=CORRECTED_EXPECTATION; expected_first_changed_node=/EVENT_SURFACE/cash_events/0/signed_delta; design_lines=433; modified_copy_digest=BLOCKED-BUILD-ARTIFACT; modification_manifest_digest=BLOCKED-BUILD-ARTIFACT` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:914-933).

Exact one modification: `kernel/economics.py`, `_resolve_funding`, invert the long-payer sign selection (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/modification.patch:1-5; MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/kernel/economics.py:1132).

## Materialization and reproducible digests

For each KERNEL probe I used the tracked Git `mtc_v2/core` tree as the complete base: tree OID `2c749345ed9be5186659369f091ce77a2e42d61a`, 119 regular files, no symlinks. Each variant contains the same 119 paths, with exactly one `economics.py` byte change described by its patch and manifest. Each KERNEL manifest records that base OID and one `KERNEL_FILE_PATCH` (for example, MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/modification_manifest.json:1). The design requires a complete variant and exactly one changed regular file (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:471).

The INPUT probe uses base instruments-tree OID `fa09741dce7084404de423df6cb6ec2718f65193`. Its two-member variant contains the changed record and the unchanged detached digest; its manifest records exactly one byte change and one `INPUT_FILE_PATCH` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json:1).

Digest method: enumerate every regular file below the variant root by UTF-8 byte-sorted POSIX relative path, SHA-256 each exact file byte sequence, then SHA-256 canonical UTF-8 JSON `{"digest_method":"SHA256_CANONICAL_TREE_MANIFEST_V1","files":[...]}` with sorted keys, compact separators, and one final LF. The implementation is at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:151-170, and every case records the same method in `modification_manifest.json:1`.

Measured materialized tree inventory: 1,103 files / 4,073,645 bytes, including 1,071 KERNEL-tree members, ten modification manifests, ten tree manifests, ten patches, and zero `.pyc` files. The committed probe root is MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/.

| Probe | Modified-copy digest | Modification-manifest SHA-256 |
|---|---|---|
| PROBE-P012-01-A | `0f956819c8b5d2a3a9c1776420f117b050b662fb1ff0aa1f63d819a382b84aca` | `50fc3ce1da1ca51feafc44dcd3c537e31d5547eec8c6f854f7260f80f8b8c4c8` |
| PROBE-P012-01-B | `e5fc81ec6bac4b93e490ffc538586a253423003f2cd3930331b67e61a5d82f08` | `8686e9c8f5a8af557f9ecae1b0cf6ba81e6b0af9ee50af303f5ea48c4efef07a` |
| PROBE-P012-02-A | `34e963a8b75209f7a8ab77aeb3d3834251f1bc6847cc2875ec6ba36275e3df25` | `80a66bec7ea77b64897820c4a429e687a2c20e2b90c4860c34ac01ad98de5d5e` |
| PROBE-P012-03-A | `35193efcfc568ec582e430b0acdc35fa4bcc3e7866313ad9f4798fd2e4e0d304` | `d2ec9000ed503947e4b86893b2a9b0cc258c765cecfb5b638a99840cb9dd1ebe` |
| PROBE-P012-04-A | `d6082460482da78706d50b3c52176f0bba8fadbc1492456b721178daa84196f8` | `e2c09190b4e32c0f9605d5cc54ad26957b5292e9e8cef49d097070e85892b5dc` |
| PROBE-P012-05-A | `1336f129f33de9ea1c4866fce91077e8a55e03e30266e56e9ca20dc5b178ed54` | `7862007188811445a3a7df11063e36dd5048f924c1af9259e246afd0256ae494` |
| PROBE-P012-05-B | `b06895e2543d4f768563d618fe99669f788a1fbaddf317d81d5553c84f71900b` | `4bd13c499516a61c12313da4fdaba2c122b37782911893f0a81fcb0ee794d67e` |
| PROBE-P012-06-A | `ad1ec938b0654ba58bc8bc90e9fad1a9781a2070b7f3951794181deb7fb6450c` | `427b29ce60b21ce0a261f35c468392b050d38366b3c986c676adeea43f8e13d7` |
| PROBE-P012-07-A | `dbef7fad26afb8c40beb049770bf867f4a492cb10025a629341eb3fef1b1b1bb` | `f9897b826a9657e3937bcb794a0d59df0c6021a4e729edad3e3608f6f7c34914` |
| PROBE-P012-08-A | `f97ce0655b57fee069a161b6584534e299d19253eac4c56aa5da0197f03a62c6` | `e466e79458bcc5368b2f9c2ecb0b314bc0825f71638d39327a1842031f446a9f` |

Each digest pair is also pinned inside its case's committed `modification_manifest.json:1`; the table is a convenience for the Lead, not a substitute for those bytes.

## Driver diff summary

- Added deterministic tree enumeration/digest support (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:151-170).
- Added artifact validation binding catalog paths, manifest schema, tree manifest, Git base OID/member set, exact one operation, patch digest/application result, and catalog marker/pin state (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1220-1525).
- Added child-process import attestation: the only `mtc_v2` package root must be the scratch root and each loaded `mtc_v2.core*` module path/digest must belong to the variant manifest (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1528-1552).
- Added the real child path for the base scenario, including pre-output record-identity failures and the catalog-named corrected/cross-version checks (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1598-1675).
- Added fresh per-probe scratch isolation. KERNEL variants become the scratch process's only import root; INPUT variants replace only the named record members in a scratch record tree (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1678-1755).
- A receipt is `DETECTED` only when the child exits refused and both measured check and node equal the catalog (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1763-1789).
- Added ten-row suite/probe mode and distinct `PROBE_NOT_DETECTED`, `PROBE_ARTIFACT_NOT_MATERIALIZED`, and `PROBE_DIGEST_UNPINNED` blockers (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1795-1922).
- Integrated the suite into the unchanged RED/GREEN full comparison pipeline and exposed `probe`/internal `probe-child` modes (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2135-2194,2255-2274).

## Driver RED/GREEN evidence

The regression requires an identical copy to return `NOT_DETECTED` with no failed node, then the materialized 08-A variant to return `DETECTED` at `/EVENT_SURFACE/cash_events/0/signed_delta` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:283-330).

RED command and measured output before the driver existed:

```text
python -m pytest -q mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k probe_driver_rejects_identity_copy_and_detects_modified_copy
FAILED ... AttributeError: module 'mtc_v2.tests.corrected_vnext.verify_bceg' has no attribute 'canonical_tree_manifest'
1 failed, 94 deselected in 0.24s
```

GREEN command and measured output after implementation:

```text
python -m pytest -q mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -k probe_driver_rejects_identity_copy_and_detects_modified_copy
.                                                                        [100%]
1 passed, 94 deselected in 1.43s
```

An intermediate attempt used 05-A and correctly got `NOT_DETECTED` for both identity and modified copies because its measured first node was not the catalog node. That finding was preserved; the driver regression uses 08-A, whose modified copy genuinely satisfies the exact detection contract. The classification code itself compares both values exactly (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1772-1789).

## Ten-probe run

Command (from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`):

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode probe
exit 0
claim_label = NON_ACCEPTING_PROBE_EVIDENCE
catalog_counts = {RED: 9, GREEN: 8, PROBE: 10}
```

The probe mode is deliberately non-accepting even when execution completes (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1908-1922).

| Probe | Expected check | Expected node | Measured check | Measured node | Status | Exact match |
|---|---|---|---|---|---|---|
| 01-A | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | NOT_DETECTED | no |
| 01-B | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/quantity` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | NOT_DETECTED | no |
| 02-A | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | `/RESULT_SURFACE/admitted` | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | `/RESULT_SURFACE/admitted` | DETECTED | yes |
| 03-A | `RECORD_IDENTITY_PREFLIGHT` | `BLOCKED-MISSING-RECORD-BYTES` | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | NOT_DETECTED | no |
| 04-A | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | NOT_DETECTED | no |
| 05-A | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | NOT_DETECTED | no |
| 05-B | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | DETECTED | yes |
| 06-A | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids/0` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | NOT_DETECTED | no |
| 07-A | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/1/signed_delta` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/1/signed_delta` | DETECTED | yes |
| 08-A | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` | DETECTED | yes |

Summary: **4 DETECTED, 6 NOT_DETECTED, 10 PROBE_DIGEST_UNPINNED**. The comparison walks object keys in UTF-8 order, so `cash_events` precedes `decision_events` and `fill_events`; it returns the first difference it encounters (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:751-805).

## Canonical full-gate run

The canonical full gate was run exactly once after the successful all-ten probe run, as ordered by the lane (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:59-62).

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate
exit = 2
mode = full-gate
claim_label = BOUNDED_CORRECTION_EVIDENCE_REFUSED
acceptance_reachable = true
catalog_counts = {RED: 9, GREEN: 8, PROBE: 10}
scenario_rows = 17
probe_rows = 10
refusal_count = 18
```

The top-level implementation emits this refused label and exit 2 whenever blockers remain (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2298-2327).

Exact ordered refusal list:

| # | Check | Probe / detail |
|---:|---|---|
| 0 | `SEMANTIC_COVERAGE_REVIEW_MISSING` | `C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\tests\corrected_vnext\contracts\semantic_coverage_review.json` |
| 1 | `LEGACY_EVENT_ORDER_MAP_PIN_MISSING` | `no seal-pinned map/digest exists in the supplied bundle` |
| 2 | `PROBE_NOT_DETECTED` | `PROBE-P012-01-A`; measured `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/cash_events/0/signed_delta` |
| 3 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-01-A`; digest pair printed above |
| 4 | `PROBE_NOT_DETECTED` | `PROBE-P012-01-B`; measured `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/cash_events/0/signed_delta` |
| 5 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-01-B`; digest pair printed above |
| 6 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-02-A`; digest pair printed above |
| 7 | `PROBE_NOT_DETECTED` | `PROBE-P012-03-A`; measured `RECORD_IDENTITY_PREFLIGHT`, `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` |
| 8 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-03-A`; digest pair printed above |
| 9 | `PROBE_NOT_DETECTED` | `PROBE-P012-04-A`; measured `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/cash_events/0/signed_delta` |
| 10 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-04-A`; digest pair printed above |
| 11 | `PROBE_NOT_DETECTED` | `PROBE-P012-05-A`; measured `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/cash_events/0/signed_delta` |
| 12 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-05-A`; digest pair printed above |
| 13 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-05-B`; digest pair printed above |
| 14 | `PROBE_NOT_DETECTED` | `PROBE-P012-06-A`; measured `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/cash_events/0/signed_delta` |
| 15 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-06-A`; digest pair printed above |
| 16 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-07-A`; digest pair printed above |
| 17 | `PROBE_DIGEST_UNPINNED` | `PROBE-P012-08-A`; digest pair printed above |

The verifier creates `PROBE_NOT_DETECTED` for non-matching receipts and independently creates `PROBE_DIGEST_UNPINNED` for marker-state rows (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1875-1904). Thus none of the ten now raises `PROBE_ARTIFACT_NOT_MATERIALIZED`; materialization and digest pinning are distinguishable as required by the lane (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:48-56).

## Self-tests and validation

Measured commands and outputs:

```text
python -m pytest -q mtc_v2/tests/corrected_vnext/contracts/selftests
223 passed in 2.31s

python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest
18 checks; all PASS or expected DETECTED
claim_label = NON_ACCEPTING_SELFTEST
exit 0

python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode probe
10 receipts; 4 DETECTED; 6 NOT_DETECTED; exit 0
```

Patch reproduction was also checked for every KERNEL variant with `git -c core.autocrlf=false apply --check --unidiff-zero`; artifact validation repeats the base/member/patch/result checks before every drive (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1220-1525).

## Discrepancies

1. **Six measured first nodes differ from the catalog.** The exact pairs are in the ten-probe table: `01-A`, `01-B`, `04-A`, `05-A`, and `06-A` first differ at `cash_events/0/signed_delta`; `03-A` names the actual record path instead of the marker. Per the lane, these are findings, not authorization to edit the catalog or strengthen variants (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:35-40,68-71). UTF-8 object-key enumeration explains the five `cash_events` results (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:778-805).
2. **Catalog `design_lines` are stale relative to design v1.10.** Catalog values `220,245,263,291,319,347,388,433` occur in the complete rows (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:734-933); the current design sentences are at `227,252,270,298,326,355,396,441` (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:24-31). No catalog edit was permitted.
3. **03-A's catalog note/expected node says record bytes are missing, but the repository contains the record and detached digest.** The row still says `BLOCKED-MISSING-RECORD-BYTES` (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:794-813), while the variant's exact byte-level manifest could be created from the present source bytes (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json:1). The measured preflight therefore names the real record path.
4. **The design specifies a detailed mechanical substitution contract only for target kind KERNEL.** It says INPUT/expected/observed bytes remain outside a KERNEL variant (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:471-473), while 03-A says only to mutate a record byte without its detached digest (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:270). I implemented INPUT isolation by copying the real record tree into a fresh scratch tree and substituting the variant's record plus unchanged sidecar; that behavior is explicit in the driver (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1728-1743).
5. **The lane's expected full-gate refusal list was incomplete.** It anticipated review missing, map pin missing, and ten unpinned blockers (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:59-62). The measured list has those 12 plus six honest `PROBE_NOT_DETECTED` blockers, for 18 total. The lane's fence requires preserving those findings (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:68-71).
6. **The literal direct-script command form cannot import `mtc_v2` from its script directory.** `python mtc_v2/tests/corrected_vnext/verify_bceg.py --mode probe` stopped before probe execution with `ModuleNotFoundError: No module named 'mtc_v2'`. The package's canonical module form, `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode probe`, was used for the all-ten run. The parser's root default is relative to the installed module path (MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2255-2274).
7. **The tracked base contains whitespace that makes `git diff --check` warn inside copied variants.** Existing trailing whitespace in copied `gates.py`, `ma.py`, and `runner.py`, plus an existing blank EOF, was preserved byte-for-byte. Removing it would make extra changed files and violate the exact-copy/one-modification contract (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:471). The real core tree was not edited.
8. **The physical source tree contained ignored Python cache files, while its Git tree OID cannot name them.** Nine initially copied variant trees had 153 cache members removed; the real core caches were untouched. The final variants use the 119 tracked members defined by the recorded Git base tree, have zero `.pyc` members, and are reproducible from the recorded OID. This is consistent with the manifest-pinned exact-tree requirement (C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:471).
9. **A committed report cannot contain the hash of the same commit that first contains it.** The implementation commit is recorded above. The report commit is identified as `SELF` here and its exact hash is supplied in the final chat handoff. No push was performed, as fenced (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:63-64).

## Commit handoff

- Implementation: `33fdbb685a0e25faf645e6bf77ca3c3c6718fd47` — `test: materialize and drive corrected-vNext probes`.
- Report: `SELF` — the commit containing this file; exact hash printed in the final chat response.
- Branch: `feature/wp-p0-12-corrected-vnext-20260831`.
- Push/PR: none. The lane explicitly forbids push (C:\tmp\LANE_PROMPTS_20260828\LANE_W256_PROBES_MATERIALIZE.md:5-9,63-64).
