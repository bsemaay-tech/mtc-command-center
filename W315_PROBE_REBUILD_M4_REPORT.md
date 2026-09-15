# W315 Probe Rebuild and M4 Re-pin Report

## Verdict

**PASS for the bounded probe-artifact rebuild and external catalog re-pin.** The nine KERNEL variants now pin core tree `efac978355c89fc38f7592d68556b7c5d7bc9eef`, each has the current core's 119-member set plus exactly one unchanged `economics.py` patch, and all ten probe artifacts (including unchanged INPUT-kind `PROBE-P012-03-A`) passed `_validate_probe_artifact` against the updated external catalog pins (`W315_PROBE_REBUILD_M4_REPORT.md:32-44`). The verifier derives the HEAD tree, requires the exact member set, and requires exactly the recorded changed file (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2422-2465,2758-2790`).

The one authorized canonical full gate was **REFUSED before probe evaluation** with the single refusal `DESIGN_PIN_MISMATCH`; this is not a probe-artifact failure. The early-refusal path wrote no `--output` file, so the exact stdout JSON was saved manually to `W315_GATE_RECEIPT.json` as required (`C:\tmp\LANE_PROMPTS_20260828\LANE_W315_PROBE_MANIFESTS_M4.md:43-49`; `W315_GATE_RECEIPT.json:1-10`).

This result grants no deployment, host, broker, exchange, live-trading, or strategy authority. The lane changes only named test artifacts, its required evidence files, and the external bundle catalog PROBE digest pins (`AGENTS.md:20-31`; `C:\tmp\LANE_PROMPTS_20260828\LANE_W315_PROBE_MANIFESTS_M4.md:19-49`).

## Authority, tier, and start gate

- Gate-1 tier: **T1**, because this is a non-economic test-artifact change with no live dependency (`AGENTS.md:38-40`).
- Write lane: `C:\WP012BUILD`, branch `feature/wp-p0-12-corrected-vnext-20260831`; starting HEAD `f37f2677f8f583e99d1abb30f6621b90daf1bc35`; initial worktree clean. These are the lane's exact start conditions (`C:\tmp\LANE_PROMPTS_20260828\LANE_W315_PROBE_MANIFESTS_M4.md:3-7`).
- External prerequisites were present: `W314_DONE.txt` contained `exit=0`, and the W312/W321 Lead acceptance markers existed (`C:\tmp\LANE_PROMPTS_20260828\W314_DONE.txt:1`; `C:\tmp\LANE_PROMPTS_20260828\W312_ACCEPTED.txt:1`; `C:\tmp\LANE_PROMPTS_20260828\W321_ACCEPTED.txt:1`).
- Exact write scope: nine probe `kernel/**` trees, their `modified_tree_manifest.json` and `modification_manifest.json` files, `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json`, `W315_GATE_RECEIPT.json`, and this report. Live dependency: none (`C:\tmp\LANE_PROMPTS_20260828\LANE_W315_PROBE_MANIFESTS_M4.md:19-49`).

## Method and preservation

The live core tree measured from HEAD is `efac978355c89fc38f7592d68556b7c5d7bc9eef`; the INPUT base tree remains `fa09741dce7084404de423df6cb6ec2718f65193`. The verifier derives those identities from Git while hashing exact working-tree member bytes (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2422-2465`).

Before rebuilding, every KERNEL variant was measured as the same 119 paths as the current tracked core, with zero extras, zero missing members, and zero symlinks (`W315_PROBE_REBUILD_M4_REPORT.md:32-34`). The recursive-delete command was rejected before execution; each of the exact 119 live-core members was therefore overwritten byte-for-byte, and the unchanged one-line patch was applied at the exact matching offset. See Discrepancy 1. The resulting variant artifacts were then independently replayed by `_validate_probe_artifact` (`W315_PROBE_REBUILD_M4_REPORT.md:35-44`), whose checks cover canonical manifest bytes and digests, base-tree identity, member conservation, the one-file diff, before/after hunks and file hashes, one-hunk patch form, and replay equality (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2642-2729,2747-2885`).

`modified_tree_manifest.json` was serialized through the verifier's `canonical_tree_manifest` / `canonical_json_bytes` rules: UTF-8-sorted regular-file members, exact SHA-256, sorted JSON keys, compact separators, and final LF (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:466-501`). No `modification.patch` byte changed.

The external catalog was snapshotted before editing at `C:\tmp\SNAPSHOTS\20260903_1356_preW315\scenario_catalog.json`; snapshot and pre-edit catalog SHA-256 were both `74c9511607f28412c85aa105f86dd15412a2deb2519e384c7a89144c0ba45d93`. The final external catalog SHA-256 is `555c4441b40c3f6fe5e00729f7d4d496c9a5cf78215fcfddd82d6243d2a7bb14`. All 17 RED/GREEN row objects and their order were byte-identical before/after; only the two digest members of each of the nine KERNEL PROBE rows changed (`W315_PROBE_REBUILD_M4_REPORT.md:45`; `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2193-2397`).

## Condensed measured command evidence

```text
START_GATE branch=feature/wp-p0-12-corrected-vnext-20260831 head=f37f2677f8f583e99d1abb30f6621b90daf1bc35 status=clean markers=W314:exit=0,W312:present,W321:present
TREE_OID core=efac978355c89fc38f7592d68556b7c5d7bc9eef input=fa09741dce7084404de423df6cb6ec2718f65193 core_members=119
PATCH_DRY_CHECK probes=10 exit_0=10 conflicts=0
KERNEL_MEMBER_SET probes=9 base_members=119 variant_members=119 extras=0 missing=0 symlinks=0
DIRECT_ARTIFACT PROBE-P012-01-A valid=true pinned=true tree=53601f03974d3c6d815bb598f7c87453dad170f6e2e230bb7b96dee621f3050b manifest=18268dce2927dffb70bd2dcafb78a46a712056e0d3adc9a07e8083293b7916da
DIRECT_ARTIFACT PROBE-P012-01-B valid=true pinned=true tree=728847388090267c44907e6eb272103f12b83c14ec1175c5ef591a31ddf629d2 manifest=ff2d87846239ec9eeffe5a52f2fd92346ee360ebf1c417e7eb7e15cda7cc2474
DIRECT_ARTIFACT PROBE-P012-02-A valid=true pinned=true tree=767f89a4e4d0b267fe9036afce4e7b12cc86e6403cb4da319791943a2a4bfe31 manifest=cfeb3a6bd60bc8159e943dd76f3386f94f94f71c1759f38dc48d97d77dad0c89
DIRECT_ARTIFACT PROBE-P012-03-A valid=true pinned=true tree=35193efcfc568ec582e430b0acdc35fa4bcc3e7866313ad9f4798fd2e4e0d304 manifest=d2ec9000ed503947e4b86893b2a9b0cc258c765cecfb5b638a99840cb9dd1ebe
DIRECT_ARTIFACT PROBE-P012-04-A valid=true pinned=true tree=72889d6ec0bc33481fdb862b20edf4861afbd2270b16ed1f6d14d55b4a8d91c6 manifest=9d7f6bd538280d3e60b0d63c98b2d757888ff27f0626118abbc5f75c344bb478
DIRECT_ARTIFACT PROBE-P012-05-A valid=true pinned=true tree=1af733383c1fc9bfbbf2b769e1a63816ed3b676fa8a2ce19984e84be40c57f1c manifest=4f94bd6c01de0da1dbd41bf2117a8447f3afff5d877f187846669944b8b6afe2
DIRECT_ARTIFACT PROBE-P012-05-B valid=true pinned=true tree=46e4c7bfa8d5a219d9ad904ca6f86e07a8ccb8efdf5153a23f5241bd8e9025c3 manifest=7f1f9c6e80f7bcbdf51e6a8f7b714640122c1e5a35c98456c1c38a8682a55bfb
DIRECT_ARTIFACT PROBE-P012-06-A valid=true pinned=true tree=66536389fe9f05a97ff84a1c5db13170ad9e0bb4794f383708c91e3605f11346 manifest=baecbd0e2569a6302d5f63b5f54e45c8f956169ec74a130030d3369c4898ca00
DIRECT_ARTIFACT PROBE-P012-07-A valid=true pinned=true tree=1259f010f19dd9082fcfbc83632ee19fdd4720e744062e7b577b84ac821d0d88 manifest=ed5bf6bdf3e3c1548a07c56f1bf0702798edb61b28abe1f8abc81f77d9e614f0
DIRECT_ARTIFACT PROBE-P012-08-A valid=true pinned=true tree=0b8ed6759544e3817762777bb3ba347af54cacfee098f2f0678e00e3ef46fe50 manifest=3f939edd8ad56bb48a06de178bb64dda1d1a190407c7e946796e79fec6f1c1ac
CATALOG before=74c9511607f28412c85aa105f86dd15412a2deb2519e384c7a89144c0ba45d93 after=555c4441b40c3f6fe5e00729f7d4d496c9a5cf78215fcfddd82d6243d2a7bb14 red_green_byte_identical=true probe_rows_changed=9 changed_members_each=modified_copy_digest,modification_manifest_digest
SCOPE repository_probe_files=45 out_of_scope=0 patch_changes=0 in_repo_catalog_changes=0 diff_check=PASS
FULL_GATE runs=1 exit=1 refusal=DESIGN_PIN_MISMATCH output_file_written=false stdout_saved_manually=true
```

## Per-probe rebuild measurements

`Base -> variant SHA` is the manifest's changed file `before_sha256 -> after_sha256`. `Variant SHA pre -> post` proves that the existing patch result itself did not change while the three post-K core members were refreshed. All KERNEL rows have 119 members; INPUT 03-A has 2 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2781-2857`).

| Probe | Old base OID -> new base OID | Patch SHA-256 (pre = post) | Changed file; base -> variant SHA-256 | Variant SHA-256 pre -> post | Expectation old -> new | New tree digest / new modification-manifest digest | Evidence |
|---|---|---|---|---|---|---|---|
| `PROBE-P012-01-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` -> `efac978355c89fc38f7592d68556b7c5d7bc9eef` | `e63171a8789d8f674dfac194e05a050ed0d853cfd59e3f3b1edfb177eb23651c` | `economics.py`; `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` -> `77b919ff11b5d8109447135f8d1f4b8e9abc1256270644fd33132036b0b75a17` | `77b919ff11b5d8109447135f8d1f4b8e9abc1256270644fd33132036b0b75a17` -> same | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/fill_events/0/quantity` -> unchanged | `53601f03974d3c6d815bb598f7c87453dad170f6e2e230bb7b96dee621f3050b` / `18268dce2927dffb70bd2dcafb78a46a712056e0d3adc9a07e8083293b7916da` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/modification_manifest.json:1` |
| `PROBE-P012-01-B` | `457a06d6e5e67b255c2830be8989f4e0610fba63` -> `efac978355c89fc38f7592d68556b7c5d7bc9eef` | `2dd219c0daaf553ea2a326a7405af2a9ae863e023b50b73b1ed2afc70b3f4b07` | `economics.py`; `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` -> `8f849953ecece375ec5435268208fe8edc3628b93f24658455ae6e4662795cde` | `8f849953ecece375ec5435268208fe8edc3628b93f24658455ae6e4662795cde` -> same | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/fill_events/0/quantity` -> unchanged | `728847388090267c44907e6eb272103f12b83c14ec1175c5ef591a31ddf629d2` / `ff2d87846239ec9eeffe5a52f2fd92346ee360ebf1c417e7eb7e15cda7cc2474` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-B/modification_manifest.json:1` |
| `PROBE-P012-02-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` -> `efac978355c89fc38f7592d68556b7c5d7bc9eef` | `ff79c24d66200a0601127da2cc4cbfcb7f58a614f6062e8d40f760a57c87069e` | `economics.py`; `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` -> `2d7f79328ccb7f3f9d8be670fe4fd00c44cf2500bc6684bebbbb37789111dda0` | `2d7f79328ccb7f3f9d8be670fe4fd00c44cf2500bc6684bebbbb37789111dda0` -> same | `RULE2_GREEN_CROSS_VERSION_EXPECTATION`, `/RESULT_SURFACE/admitted` -> `CORRECTED_EXPECTATION`, `/RESULT_SURFACE/admitted` | `767f89a4e4d0b267fe9036afce4e7b12cc86e6403cb4da319791943a2a4bfe31` / `cfeb3a6bd60bc8159e943dd76f3386f94f94f71c1759f38dc48d97d77dad0c89` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-02-A/modification_manifest.json:1`; `C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:356-368`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V312\V312_REPORT.md:185-192`; `C:\tmp\LANE_PROMPTS_20260828\W321_TABLES_M1_REPORT.md:33-38`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V321\V321_REPORT.md:58-65` |
| `PROBE-P012-03-A` (INPUT) | `fa09741dce7084404de423df6cb6ec2718f65193` -> same | `30b8e5832cc59e9b3866baa09259a6618c9996f0ed2377cf7a9d0237b1494fd2` | `SYNTH-INSTRUMENT-RULE2-03-RED-V1.json`; `498ae36ea28a7f40df519724b1fb80d98a68c7261cda8fc7c0c3d6893c909a9a` -> `e0c6425a13ebc312eb00c3497510f804e3a092ab1627a5f1b3aa744ffe54221f` | `e0c6425a13ebc312eb00c3497510f804e3a092ab1627a5f1b3aa744ffe54221f` -> same | `RECORD_IDENTITY_PREFLIGHT`, `BLOCKED-MISSING-RECORD-BYTES` -> unchanged | `35193efcfc568ec582e430b0acdc35fa4bcc3e7866313ad9f4798fd2e4e0d304` / `d2ec9000ed503947e4b86893b2a9b0cc258c765cecfb5b638a99840cb9dd1ebe` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json:1` |
| `PROBE-P012-04-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` -> `efac978355c89fc38f7592d68556b7c5d7bc9eef` | `969dc7c3771cdb73ab74115305a649437b57321b62e0735c87929922c446ae50` | `economics.py`; `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` -> `ea81ad343a31b73fd6788a7a400633f34739f933fc8e9ba073dcdaf6efa0db88` | `ea81ad343a31b73fd6788a7a400633f34739f933fc8e9ba073dcdaf6efa0db88` -> same | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/fill_events/0/final_fill_price` -> unchanged | `72889d6ec0bc33481fdb862b20edf4861afbd2270b16ed1f6d14d55b4a8d91c6` / `9d7f6bd538280d3e60b0d63c98b2d757888ff27f0626118abbc5f75c344bb478` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-04-A/modification_manifest.json:1` |
| `PROBE-P012-05-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` -> `efac978355c89fc38f7592d68556b7c5d7bc9eef` | `74a2ca6813bdd032000b3b07d7ac38dca3134433157ecc94e3c533e7581bba89` | `economics.py`; `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` -> `855a020f908542256236ee4df4c4a15d66985b01e3b22542a332c90ddf213e5c` | `855a020f908542256236ee4df4c4a15d66985b01e3b22542a332c90ddf213e5c` -> same | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/fill_events/0/final_fill_price` -> unchanged | `1af733383c1fc9bfbbf2b769e1a63816ed3b676fa8a2ce19984e84be40c57f1c` / `4f94bd6c01de0da1dbd41bf2117a8447f3afff5d877f187846669944b8b6afe2` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-A/modification_manifest.json:1` |
| `PROBE-P012-05-B` | `457a06d6e5e67b255c2830be8989f4e0610fba63` -> `efac978355c89fc38f7592d68556b7c5d7bc9eef` | `bb8a7259bce5872c9e41531095c5394048070c30623e9777581f597c24fcc291` | `economics.py`; `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` -> `15fb0998a62bf9faa24958e0567a079b2e6507493a6a60242b6908c83788bc31` | `15fb0998a62bf9faa24958e0567a079b2e6507493a6a60242b6908c83788bc31` -> same | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/fill_events/0/final_fill_price` -> unchanged | `46e4c7bfa8d5a219d9ad904ca6f86e07a8ccb8efdf5153a23f5241bd8e9025c3` / `7f1f9c6e80f7bcbdf51e6a8f7b714640122c1e5a35c98456c1c38a8682a55bfb` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-B/modification_manifest.json:1` |
| `PROBE-P012-06-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` -> `efac978355c89fc38f7592d68556b7c5d7bc9eef` | `5dd7a081ef14538d5ff21ca24cee2a9ad52056949edf0779fbad6e16346e2e37` | `economics.py`; `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` -> `3439ce5f4673957773e5794c9a739ece8656e85b3df98fa12ccc30803d4c9180` | `3439ce5f4673957773e5794c9a739ece8656e85b3df98fa12ccc30803d4c9180` -> same | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids/0` -> `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/fill_events/0/exit_id` | `66536389fe9f05a97ff84a1c5db13170ad9e0bb4794f383708c91e3605f11346` / `baecbd0e2569a6302d5f63b5f54e45c8f956169ec74a130030d3369c4898ca00` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-06-A/modification_manifest.json:1`; `C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:388-400`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V312\V312_REPORT.md:194-201` |
| `PROBE-P012-07-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` -> `efac978355c89fc38f7592d68556b7c5d7bc9eef` | `57f9c4d2c0d7003f25ca42c371d74ae9be4c2f6e1a7207bc35a0b6521d49c2c6` | `economics.py`; `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` -> `19783a5ec51d34952fd4c22a8435758149455e7dda47f12fe6727a3d325a1a46` | `19783a5ec51d34952fd4c22a8435758149455e7dda47f12fe6727a3d325a1a46` -> same | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/cash_events/1/signed_delta` -> unchanged | `1259f010f19dd9082fcfbc83632ee19fdd4720e744062e7b577b84ac821d0d88` / `ed5bf6bdf3e3c1548a07c56f1bf0702798edb61b28abe1f8abc81f77d9e614f0` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification_manifest.json:1` |
| `PROBE-P012-08-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` -> `efac978355c89fc38f7592d68556b7c5d7bc9eef` | `cabe3f20c12a5fd5d730c46d13e26e97133e4680dce711ac32e565ee6eb1e4eb` | `economics.py`; `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` -> `51e7a42faeab322234312d38a5bf49351c15ad6c3fb2cf98b469dee931da5264` | `51e7a42faeab322234312d38a5bf49351c15ad6c3fb2cf98b469dee931da5264` -> same | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/cash_events/0/signed_delta` -> `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | `0b8ed6759544e3817762777bb3ba347af54cacfee098f2f0678e00e3ef46fe50` / `3f939edd8ad56bb48a06de178bb64dda1d1a190407c7e946796e79fec6f1c1ac` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/modification_manifest.json:1`; `C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:421-425`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V312\V312_REPORT.md:203-204`; `C:\tmp\LANE_PROMPTS_20260828\W321_TABLES_M1_REPORT.md:33-38`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V321\V321_REPORT.md:58-65` |

All unchanged patches applied without `PATCH_CONFLICT`. Their measured exact offsets were `+2`, `+2`, `+3`, `+3`, `+2`, `+2`, `+4`, `+3`, and `+40` in the KERNEL-probe order shown above, matching the earlier rebuild mechanics (`W299C_VARIANT_REBUILD_REPORT.md:30-38`).

## M4 expectation values

- `PROBE-P012-02-A`: W312 originally carried `RULE2_GREEN_CROSS_VERSION_EXPECTATION` and `/RESULT_SURFACE/admitted` (`C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:356-368`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V312\V312_REPORT.md:185-192`). W321 supersedes the check with `CORRECTED_EXPECTATION` while retaining `/RESULT_SURFACE/admitted`; V321 accepts exactly that pair (`C:\tmp\LANE_PROMPTS_20260828\W321_TABLES_M1_REPORT.md:33-38,87-89`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V321\V321_REPORT.md:58-65`).
- `PROBE-P012-06-A`: wrote exactly `CORRECTED_EXPECTATION` and `/EVENT_SURFACE/fill_events/0/exit_id` from W312; V312 accepts both (`C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:388-400`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V312\V312_REPORT.md:194-201`).
- `PROBE-P012-08-A`: W312/V312 explicitly stopped without a value (`C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:421-425`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V312\V312_REPORT.md:203-204`). W321 supplies `CORRECTED_EXPECTATION` and `/EVENT_SURFACE/funding_events/0/funding_cash_delta`, and V321 accepts the pair (`C:\tmp\LANE_PROMPTS_20260828\W321_TABLES_M1_REPORT.md:33-38`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V321\V321_REPORT.md:58-65`).

## External catalog PROBE row delta

The accepted 02-A, 06-A, and 08-A expectations already existed in the external catalog, so their expectation bytes did not move; only stale digest pins changed. INPUT 03-A did not change. The catalog schema requires both digest pins and both expectation members on PROBE rows (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2393-2410`).

| Probe | Members changed | `modified_copy_digest` old -> new | `modification_manifest_digest` old -> new | Expectation old -> new | Evidence |
|---|---|---|---|---|---|
| `PROBE-P012-01-A` | two digests | `bf3d60086b94fc6ac1987ac3be48d4043295c046b3bf965d8f0db1bc082c1d5f` -> `53601f03974d3c6d815bb598f7c87453dad170f6e2e230bb7b96dee621f3050b` | `dcad00109d4f0ceb49e01f644fbfb167b69fac5ef23f85ac4dd0c76a6b729643` -> `18268dce2927dffb70bd2dcafb78a46a712056e0d3adc9a07e8083293b7916da` | unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2193-2208` |
| `PROBE-P012-01-B` | two digests | `a68dd872f75977c85931c762d24f6525a53e978ee633aff023c14644e5ed9d8a` -> `728847388090267c44907e6eb272103f12b83c14ec1175c5ef591a31ddf629d2` | `3721ff47900bb4d134827206009012b48d94e845c162ce18f3f852f15b289ba2` -> `ff2d87846239ec9eeffe5a52f2fd92346ee360ebf1c417e7eb7e15cda7cc2474` | unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2214-2229` |
| `PROBE-P012-02-A` | two digests | `0e51bd03658fa54a255560459038abfadd030aac8e65b703dcfaedf9aa15f316` -> `767f89a4e4d0b267fe9036afce4e7b12cc86e6403cb4da319791943a2a4bfe31` | `f37e6d9f3443292d9458ec5de609c1b4854fa2b4f67a3289b64ff9fdf91036c8` -> `cfeb3a6bd60bc8159e943dd76f3386f94f94f71c1759f38dc48d97d77dad0c89` | `CORRECTED_EXPECTATION`, `/RESULT_SURFACE/admitted` -> unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2235-2250` |
| `PROBE-P012-03-A` | none | `35193efcfc568ec582e430b0acdc35fa4bcc3e7866313ad9f4798fd2e4e0d304` -> same | `d2ec9000ed503947e4b86893b2a9b0cc258c765cecfb5b638a99840cb9dd1ebe` -> same | unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2256-2271` |
| `PROBE-P012-04-A` | two digests | `c35479033870e5c1811626ce623ca67a4a779bf3dea66f03375d2f8fa4022f9c` -> `72889d6ec0bc33481fdb862b20edf4861afbd2270b16ed1f6d14d55b4a8d91c6` | `24f70876403398f1663a659bdc1a63b44af355f5d4118c02ed4e95c94b7c0d72` -> `9d7f6bd538280d3e60b0d63c98b2d757888ff27f0626118abbc5f75c344bb478` | unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2277-2292` |
| `PROBE-P012-05-A` | two digests | `59eff888dbb654e8cda576132fe4244aa7f2a3f7d55f7501e620a716586838ac` -> `1af733383c1fc9bfbbf2b769e1a63816ed3b676fa8a2ce19984e84be40c57f1c` | `44251938704af7f92d1e880b4dd3b4239c21ac927daae4db3840fc23c19643d5` -> `4f94bd6c01de0da1dbd41bf2117a8447f3afff5d877f187846669944b8b6afe2` | unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2298-2313` |
| `PROBE-P012-05-B` | two digests | `41844cf3db3790a028cd6bf71f7859ec90db94bb83083fb07785b76497090365` -> `46e4c7bfa8d5a219d9ad904ca6f86e07a8ccb8efdf5153a23f5241bd8e9025c3` | `709a543786be9a07e77d1b81f6676d6c95c5bd027248e0aa85ea4dad78198661` -> `7f1f9c6e80f7bcbdf51e6a8f7b714640122c1e5a35c98456c1c38a8682a55bfb` | unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2319-2334` |
| `PROBE-P012-06-A` | two digests | `2fe755a71836585361592e9bd3b913f843ccb3a9c0ba523a44e1d65561048869` -> `66536389fe9f05a97ff84a1c5db13170ad9e0bb4794f383708c91e3605f11346` | `39c8af08f17c7bf3f8d7c689b8ce0db7d3d1ee8504aa5fedf5d401c0149e5380` -> `baecbd0e2569a6302d5f63b5f54e45c8f956169ec74a130030d3369c4898ca00` | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/fill_events/0/exit_id` -> unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2340-2355` |
| `PROBE-P012-07-A` | two digests | `b65811b6d77e376d34ffad34b7210cf6a0f983ee3bdf9c5efd0c2e88c4ca2e9c` -> `1259f010f19dd9082fcfbc83632ee19fdd4720e744062e7b577b84ac821d0d88` | `57fee87191150d2afb983017339e1cec1a63faed80694155af803313afd40f37` -> `ed5bf6bdf3e3c1548a07c56f1bf0702798edb61b28abe1f8abc81f77d9e614f0` | unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2361-2376` |
| `PROBE-P012-08-A` | two digests | `98e73b51a0ee3ac05a285a8a0710f73ea0a9e621171317b4806cf0eb335c04c1` -> `0b8ed6759544e3817762777bb3ba347af54cacfee098f2f0678e00e3ef46fe50` | `96aaa32930b1bfff487fadb7cdea34e14408e62fe939787c0c5e162ddb35c47d` -> `3f939edd8ad56bb48a06de178bb64dda1d1a190407c7e946796e79fec6f1c1ac` | `CORRECTED_EXPECTATION`, `/EVENT_SURFACE/funding_events/0/funding_cash_delta` -> unchanged | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2382-2397` |

## Complete before/after SHA-256 inventory

The final repository diff has 45 probe files plus this report and the receipt. For every KERNEL probe, the byte-changing core-copy members are the same three paths:

| Path in each of nine `kernel/` trees | Files covered | Pre-lane SHA-256 -> post-lane SHA-256 |
|---|---:|---|
| `position_manager.py` | 9 | `2373494c2dac8caa1452e7164d5a22db1efac5b439f6dcd3080744d80c1ee0fa` -> `12ab981b48b41d8ba90cbb839567db544001748e46c32bd3168680d010c6cfd6` |
| `results.py` | 9 | `5cc91cf30b75ee1f0a3ff55c31078061f5f40e181579666384da005f7bdd7e70` -> `82006bfda9db69bec756f0b1ea3bdcf13e082f77bdab8539c1e036154e06bb4f` |
| `types.py` | 9 | `95bd536ed5f0905a3ee2e60214bd36a5bad6e91ca886bed9581be822439b99aa` -> `9e61d0d585f1d3383ddc39f612e12a3361dc8c9a3a10ceb30fbaaab25c935d52` |

The per-probe table above gives pre/post SHA-256 for every overwritten `economics.py` (all unchanged as variant files), every patch, every changed-file base/result pair, every tree-manifest file, and every modification-manifest file. The old and new canonical tree manifests enumerate the complete per-member SHA-256 inventory: comparison found only `position_manager.py`, `results.py`, and `types.py` changed in each 119-member variant; `economics.py` and the other 115 members are byte-identical pre/post. Each current inventory is stored on line 1 of its probe's `modified_tree_manifest.json`, under the canonical rules cited above.

Additional touched evidence:

| File | Pre-lane SHA-256 -> post-lane SHA-256 |
|---|---|
| `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json` | `74c9511607f28412c85aa105f86dd15412a2deb2519e384c7a89144c0ba45d93` -> `555c4441b40c3f6fe5e00729f7d4d496c9a5cf78215fcfddd82d6243d2a7bb14` |
| `W315_GATE_RECEIPT.json` | absent -> `de62cffca82acb31ae07291ff1ab7db268ce9e560ec68c84e19c11309ed05924` |
| `W315_PROBE_REBUILD_M4_REPORT.md` | absent -> self-referential final digest cannot be embedded in its own bytes; reviewer can hash the committed file |

## Verification and canonical refusal

- Ten unchanged-patch dry checks returned exit `0`; all nine KERNEL patch applications then found the exact removed line and produced the recorded after SHA-256. Patch replay is also part of the direct artifact validator (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2852-2885`).
- Direct `_validate_probe_artifact` returned valid for all 10 probes against the updated external catalog: 10 pinned artifacts, 0 refusals (`W315_PROBE_REBUILD_M4_REPORT.md:35-44`). It validates the catalog pins against computed tree and manifest digests before the base/diff checks (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2715-2745`).
- Scope check before the canonical gate: 45 repository files changed, all under the nine named probe cases; 0 patch changes; 0 in-repo catalog changes; `git diff --check` PASS (`W315_PROBE_REBUILD_M4_REPORT.md:46`).
- Canonical command, run exactly once from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`: `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W315_GATE_RECEIPT.json` (`C:\tmp\LANE_PROMPTS_20260828\LANE_W315_PROBE_MANIFESTS_M4.md:43-48`). Exit: `1`.
- `validate_design_pin` runs before catalog/probe validation and refuses on a recorded/actual digest or line-count mismatch (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2202-2251`). The early-refusal path wrote no output file; the following full stdout refusal object was saved manually and byte-checked at `W315_GATE_RECEIPT.json:1-10`:

```json
{
  "claim_label": "BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED",
  "mode": "full-gate",
  "refusal": {
    "check_id": "DESIGN_PIN_MISMATCH",
    "detail": "C:\\tmp\\LANE_PROMPTS_20260828\\P012_FRESH_DESIGN_V1.md: recorded_sha256=1f506c923c700df3a2a757ab3d49efabcd4d06bf39c251f8965c55bc10de8b75, actual_sha256=137180aee4834fa6b87932e289d7ce8cf56d9471c08e7b53982445598347c62f, recorded_total_lines=1419, actual_total_lines=1664",
    "pointer": "/design"
  }
}
```

Full refusal list, verbatim: **`DESIGN_PIN_MISMATCH`**. No probe disposition was produced because the design-pin check refused first.

## Git diff stat

Final pre-commit `git diff --stat`: **47 files changed, 453 insertions(+), 198 deletions(-)**. The 45 probe files account for 288 insertions and 198 deletions before adding this 156-line report and the 9-line receipt.

## Discrepancies

1. **Recursive delete was rejected before execution.** The lane directs deleting each variant copy before recreation (`C:\tmp\LANE_PROMPTS_20260828\LANE_W315_PROBE_MANIFESTS_M4.md:19-24`), but the shell safety layer rejected the exact resolved recursive-delete command and then the file-by-file delete form before either executed. The existing variants had already been measured as the exact 119-path core member set with no extras, missing paths, or symlinks, so overwriting all 119 tracked members produced the same byte state. This is the same policy/result distinction recorded by the mandated precedent (`W299C_VARIANT_REBUILD_REPORT.md:113-116`). The direct validator's exact member/digest/diff/patch-result checks passed all nine rebuilt KERNEL variants.
2. **The phrase “as W299C did” is factually inaccurate for catalog edits.** W315 Part C says to update catalog PROBE rows “as W299C did” (`C:\tmp\LANE_PROMPTS_20260828\LANE_W315_PROBE_MANIFESTS_M4.md:34-38`), but W299C explicitly left the catalog unchanged for a later act (`W299C_VARIANT_REBUILD_REPORT.md:58-68,111,118`). W315's direct instruction to update the external catalog controlled; the update was made only to the nine stale digest pairs.
3. **Two pre-existing catalog/manifest `expected_first_changed_node` differences remain outside the named M4 write.** INPUT 03-A's manifest carries `BLOCKED-MISSING-RECORD-BYTES`, while the external catalog carries the now-materialized record path (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-03-A/modification_manifest.json:1`; `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2256-2273`). KERNEL 07-A's manifest carries `/EVENT_SURFACE/cash_events/1/signed_delta`, while the external catalog carries `/EVENT_SURFACE/fee_events/1/liquidity_role` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification_manifest.json:1`; `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:2361-2378`). Part B authorizes expectation writes only for 02-A, 06-A, and 08-A, and INPUT 03-A had to be left unchanged because its base tree did not move (`C:\tmp\LANE_PROMPTS_20260828\LANE_W315_PROBE_MANIFESTS_M4.md:19,26-32`). No unsupported adaptation was made. The current artifact validator binds manifest/catalog `expected_failed_check` but not `expected_first_changed_node` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2691-2700`), so both artifacts still validated; this does not claim the two expectation differences are resolved.

No repository-content discrepancy prevented the authorized target result. The predicted early gate refusal occurred, with the actual one-item list quoted above (`C:\tmp\LANE_PROMPTS_20260828\LANE_W315_PROBE_MANIFESTS_M4.md:45-48`).

## Findings

- Patch conflicts: **0**.
- Direct artifact-validation findings: **0** (10/10 valid).
- External catalog out-of-scope row/member changes: **0**.
- Canonical gate refusals: **1**, the expected early `DESIGN_PIN_MISMATCH` boundary.
- Discrepancies recorded: **3**.

## Commit

One commit is used for the probe artifacts, receipt, and report with the required subject: `chore(mtc-v2): rebuild probe variants on the post-K core and re-pin M4 expectations (decisions 136/140)`. The commit hash is supplied in the chat close because a commit cannot contain its own hash.
