# W299C Variant Rebuild Report

## Verdict

**PASS for the bounded variant-artifact rebuild.** All nine KERNEL variants now have the same 119-member set as HEAD core tree `457a06d6e5e67b255c2830be8989f4e0610fba63`, differ from that tree only in `economics.py`, and pass the verifier's own artifact validator with current measured pins (`W299C_VARIANT_REBUILD_REPORT.md:29,39-47`). This closes the `PROBE_KERNEL_DIFF_INVALID` artifact defect described by W303C-F01, but it does not re-pin the intentionally unchanged catalog (`W303C_REFRESH_ANCHOR_REPORT.md:194-204`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2393-2423`).

The result is bounded to probe artifacts. It does not claim gate acceptance, deployment readiness, or trading authority. Probe mode still records the expected catalog-pin mismatch for these nine probes, exactly at the boundary reserved for the Lead's next act (`W299C_VARIANT_REBUILD_REPORT.md:58-68`; `C:\tmp\LANE_PROMPTS_20260828\LANE_W299C_PROBE_VARIANT_REBUILD_OFFSET.md:48-51`).

## Scope and start gate

- Gate-1 tier: **T1**, because the lane changes non-economic test artifacts under the MTC Python tree and no live, host, security, deployment, strategy, threshold, schema, broker, or exchange behavior (`AGENTS.md:38-40`).
- Worktree/branch: `C:\WP012BUILD` / `feature/wp-p0-12-corrected-vnext-20260831`; starting HEAD `1d2dd8652ff63c9121cbe3dbfc679da21f7cd251`; initial status clean; external marker `C:\tmp\LANE_PROMPTS_20260828\W304_DONE.txt:1` was `exit=0` (`W299C_VARIANT_REBUILD_REPORT.md:27`). These are the prompt's mandatory start conditions (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299C_PROBE_VARIANT_REBUILD_OFFSET.md:3-11`).
- Write lane: this worktree and branch; exact write paths were the nine named `kernel/**` trees, their `modified_tree_manifest.json` and `modification_manifest.json` files, plus this required report. Live dependency: none (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299C_PROBE_VARIANT_REBUILD_OFFSET.md:8-11,53-56`).
- Commit strategy: one artifact commit for all nine probes with the full table below, followed by one report-only commit. No push or PR action was performed (`W299C_VARIANT_REBUILD_REPORT.md:70-71`; `C:\tmp\LANE_PROMPTS_20260828\LANE_W299C_PROBE_VARIANT_REBUILD_OFFSET.md:46,53-56`).

## Method

The live core tree was measured from HEAD, and every variant's existing 119-member set was first confirmed equal to that tracked tree with zero extras, zero missing members, and zero `__pycache__` directories. Every tracked core member was then copied byte-for-byte over the variant before the unchanged patch was applied with `patch -p1 -F0`; the measured final member/diff state and patch offsets are recorded below (`W299C_VARIANT_REBUILD_REPORT.md:29-47`). GNU patch's offset-created `.orig` backup was removed from each in-scope variant before hashing. The design requires a complete exact kernel copy plus exactly one recorded file patch (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:495-497`).

The manifests were rebuilt through `verify_bceg.canonical_tree_manifest` and `verify_bceg.canonical_json_bytes`, which UTF-8-sort members, hash exact file bytes, sort JSON keys, use compact separators, and require a final LF (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:451-483`). The direct artifact validation exercised canonical-manifest equality, both digest bindings, catalog-pin shape, HEAD base-tree identity, member-set equality, one-file diff, before/after hunk presence, before/after file digests, one-hunk patch form, and patch-result equality (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2327-2341,2343-2357,2368-2423,2464-2497`).

## Condensed command evidence

The following is a condensed transcription of outputs measured in this session. `FINAL_ARTIFACT` was emitted only after `_validate_probe_artifact` returned normally.

```text
START_GATE worktree=C:/WP012BUILD branch=feature/wp-p0-12-corrected-vnext-20260831 start_head=1d2dd8652ff63c9121cbe3dbfc679da21f7cd251 marker_exit=0 status=clean
DELETE_ATTEMPT policy_blocked=true command_executed=false
CORE_OID 457a06d6e5e67b255c2830be8989f4e0610fba63 tracked_members=119
PATCH_APPLY PROBE-P012-01-A exit=0 offset=+2 applied_line=242 fuzz=0
PATCH_APPLY PROBE-P012-01-B exit=0 offset=+2 applied_line=243 fuzz=0
PATCH_APPLY PROBE-P012-02-A exit=0 offset=+3 applied_line=649 fuzz=0
PATCH_APPLY PROBE-P012-04-A exit=0 offset=+3 applied_line=547 fuzz=0
PATCH_APPLY PROBE-P012-05-A exit=0 offset=+2 applied_line=277 fuzz=0
PATCH_APPLY PROBE-P012-05-B exit=0 offset=+2 applied_line=277 fuzz=0
PATCH_APPLY PROBE-P012-06-A exit=0 offset=+4 applied_line=791 fuzz=0
PATCH_APPLY PROBE-P012-07-A exit=0 offset=+3 applied_line=302 fuzz=0
PATCH_APPLY PROBE-P012-08-A exit=0 offset=+40 applied_line=1172 fuzz=0
FINAL_ARTIFACT PROBE-P012-01-A base_members=119 variant_members=119 changed=['economics.py'] added=[] deleted=[] valid=true tree_digest=bf3d60086b94fc6ac1987ac3be48d4043295c046b3bf965d8f0db1bc082c1d5f manifest_digest=dcad00109d4f0ceb49e01f644fbfb167b69fac5ef23f85ac4dd0c76a6b729643
FINAL_ARTIFACT PROBE-P012-01-B base_members=119 variant_members=119 changed=['economics.py'] added=[] deleted=[] valid=true tree_digest=a68dd872f75977c85931c762d24f6525a53e978ee633aff023c14644e5ed9d8a manifest_digest=3721ff47900bb4d134827206009012b48d94e845c162ce18f3f852f15b289ba2
FINAL_ARTIFACT PROBE-P012-02-A base_members=119 variant_members=119 changed=['economics.py'] added=[] deleted=[] valid=true tree_digest=0e51bd03658fa54a255560459038abfadd030aac8e65b703dcfaedf9aa15f316 manifest_digest=f37e6d9f3443292d9458ec5de609c1b4854fa2b4f67a3289b64ff9fdf91036c8
FINAL_ARTIFACT PROBE-P012-04-A base_members=119 variant_members=119 changed=['economics.py'] added=[] deleted=[] valid=true tree_digest=c35479033870e5c1811626ce623ca67a4a779bf3dea66f03375d2f8fa4022f9c manifest_digest=24f70876403398f1663a659bdc1a63b44af355f5d4118c02ed4e95c94b7c0d72
FINAL_ARTIFACT PROBE-P012-05-A base_members=119 variant_members=119 changed=['economics.py'] added=[] deleted=[] valid=true tree_digest=59eff888dbb654e8cda576132fe4244aa7f2a3f7d55f7501e620a716586838ac manifest_digest=44251938704af7f92d1e880b4dd3b4239c21ac927daae4db3840fc23c19643d5
FINAL_ARTIFACT PROBE-P012-05-B base_members=119 variant_members=119 changed=['economics.py'] added=[] deleted=[] valid=true tree_digest=41844cf3db3790a028cd6bf71f7859ec90db94bb83083fb07785b76497090365 manifest_digest=709a543786be9a07e77d1b81f6676d6c95c5bd027248e0aa85ea4dad78198661
FINAL_ARTIFACT PROBE-P012-06-A base_members=119 variant_members=119 changed=['economics.py'] added=[] deleted=[] valid=true tree_digest=2fe755a71836585361592e9bd3b913f843ccb3a9c0ba523a44e1d65561048869 manifest_digest=39c8af08f17c7bf3f8d7c689b8ce0db7d3d1ee8504aa5fedf5d401c0149e5380
FINAL_ARTIFACT PROBE-P012-07-A base_members=119 variant_members=119 changed=['economics.py'] added=[] deleted=[] valid=true tree_digest=b65811b6d77e376d34ffad34b7210cf6a0f983ee3bdf9c5efd0c2e88c4ca2e9c manifest_digest=57fee87191150d2afb983017339e1cec1a63faed80694155af803313afd40f37
FINAL_ARTIFACT PROBE-P012-08-A base_members=119 variant_members=119 changed=['economics.py'] added=[] deleted=[] valid=true tree_digest=98e73b51a0ee3ac05a285a8a0710f73ea0a9e621171317b4806cf0eb335c04c1 manifest_digest=96aaa32930b1bfff487fadb7cdea34e14408e62fe939787c0c5e162ddb35c47d
FILE_DIFF PROBE-P012-01-A economics.py | 2 +- ; 1 file changed, 1 insertion(+), 1 deletion(-)
FILE_DIFF PROBE-P012-01-B economics.py | 2 +- ; 1 file changed, 1 insertion(+), 1 deletion(-)
FILE_DIFF PROBE-P012-02-A economics.py | 2 +- ; 1 file changed, 1 insertion(+), 1 deletion(-)
FILE_DIFF PROBE-P012-04-A economics.py | 2 +- ; 1 file changed, 1 insertion(+), 1 deletion(-)
FILE_DIFF PROBE-P012-05-A economics.py | 2 +- ; 1 file changed, 1 insertion(+), 1 deletion(-)
FILE_DIFF PROBE-P012-05-B economics.py | 2 +- ; 1 file changed, 1 insertion(+), 1 deletion(-)
FILE_DIFF PROBE-P012-06-A economics.py | 2 +- ; 1 file changed, 1 insertion(+), 1 deletion(-)
FILE_DIFF PROBE-P012-07-A economics.py | 2 +- ; 1 file changed, 1 insertion(+), 1 deletion(-)
FILE_DIFF PROBE-P012-08-A economics.py | 2 +- ; 1 file changed, 1 insertion(+), 1 deletion(-)
PRESERVATION all_nine top_changed=['base_tree_oid','modified_copy_digest','modified_tree_manifest_sha256'] modification_fields_changed=[] patch_changed=false
PROBE_MODE exit=0 mode=probe claim_label=NON_ACCEPTING_PROBE_EVIDENCE blockers=9
PROBE_DISPOSITION PROBE-P012-01-A status=COULD_NOT_EVALUATE digest_status=PROBE_ARTIFACT_INVALID refusal=PROBE_CATALOG_DIGEST_MISMATCH
PROBE_DISPOSITION PROBE-P012-01-B status=COULD_NOT_EVALUATE digest_status=PROBE_ARTIFACT_INVALID refusal=PROBE_CATALOG_DIGEST_MISMATCH
PROBE_DISPOSITION PROBE-P012-02-A status=COULD_NOT_EVALUATE digest_status=PROBE_ARTIFACT_INVALID refusal=PROBE_CATALOG_DIGEST_MISMATCH
PROBE_DISPOSITION PROBE-P012-03-A status=DETECTED digest_status=PROBE_DIGEST_MATCH refusal=none
PROBE_DISPOSITION PROBE-P012-04-A status=COULD_NOT_EVALUATE digest_status=PROBE_ARTIFACT_INVALID refusal=PROBE_CATALOG_DIGEST_MISMATCH
PROBE_DISPOSITION PROBE-P012-05-A status=COULD_NOT_EVALUATE digest_status=PROBE_ARTIFACT_INVALID refusal=PROBE_CATALOG_DIGEST_MISMATCH
PROBE_DISPOSITION PROBE-P012-05-B status=COULD_NOT_EVALUATE digest_status=PROBE_ARTIFACT_INVALID refusal=PROBE_CATALOG_DIGEST_MISMATCH
PROBE_DISPOSITION PROBE-P012-06-A status=COULD_NOT_EVALUATE digest_status=PROBE_ARTIFACT_INVALID refusal=PROBE_CATALOG_DIGEST_MISMATCH
PROBE_DISPOSITION PROBE-P012-07-A status=COULD_NOT_EVALUATE digest_status=PROBE_ARTIFACT_INVALID refusal=PROBE_CATALOG_DIGEST_MISMATCH
PROBE_DISPOSITION PROBE-P012-08-A status=COULD_NOT_EVALUATE digest_status=PROBE_ARTIFACT_INVALID refusal=PROBE_CATALOG_DIGEST_MISMATCH
EXACT_DIRECTORY_DIFF each_probe=18_files_changed cause=17_ignored_core_pyc_plus_economics.py
ARTIFACT_COMMIT 1c2b710cf836cbd3ec88ca94ff0e772f63d13d82 files=27 insertions=189 deletions=117
FINAL_SCOPE artifact_commit_paths=27 all_authorized=true out_of_scope=0 patch_changes=0 push=false pr=false
```

## Per-probe artifact table

`Tree digest` is both `modified_copy_digest` and `modified_tree_manifest_sha256`; `manifest digest` is the SHA-256 of `modification_manifest.json` needed for the later catalog re-pin. The direct artifact result is `valid`, not a probe-detection result (`W299C_VARIANT_REBUILD_REPORT.md:39-47`).

| Probe | Core OID | Offset | Changed file and diff stat | Before SHA-256 | After SHA-256 | Tree digest | Modification-manifest digest | Artifact result | Evidence |
|---|---|---:|---|---|---|---|---|---|---|
| `PROBE-P012-01-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | `+2` | `economics.py`; `1 file changed, 1 insertion(+), 1 deletion(-)` | `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` | `77b919ff11b5d8109447135f8d1f4b8e9abc1256270644fd33132036b0b75a17` | `bf3d60086b94fc6ac1987ac3be48d4043295c046b3bf965d8f0db1bc082c1d5f` | `dcad00109d4f0ceb49e01f644fbfb167b69fac5ef23f85ac4dd0c76a6b729643` | `valid`; one changed member; no add/delete | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/modification_manifest.json:1`; `W299C_VARIANT_REBUILD_REPORT.md:30,39,48` |
| `PROBE-P012-01-B` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | `+2` | `economics.py`; `1 file changed, 1 insertion(+), 1 deletion(-)` | `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` | `8f849953ecece375ec5435268208fe8edc3628b93f24658455ae6e4662795cde` | `a68dd872f75977c85931c762d24f6525a53e978ee633aff023c14644e5ed9d8a` | `3721ff47900bb4d134827206009012b48d94e845c162ce18f3f852f15b289ba2` | `valid`; one changed member; no add/delete | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-B/modification_manifest.json:1`; `W299C_VARIANT_REBUILD_REPORT.md:31,40,49` |
| `PROBE-P012-02-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | `+3` | `economics.py`; `1 file changed, 1 insertion(+), 1 deletion(-)` | `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` | `2d7f79328ccb7f3f9d8be670fe4fd00c44cf2500bc6684bebbbb37789111dda0` | `0e51bd03658fa54a255560459038abfadd030aac8e65b703dcfaedf9aa15f316` | `f37e6d9f3443292d9458ec5de609c1b4854fa2b4f67a3289b64ff9fdf91036c8` | `valid`; one changed member; no add/delete | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-02-A/modification_manifest.json:1`; `W299C_VARIANT_REBUILD_REPORT.md:32,41,50` |
| `PROBE-P012-04-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | `+3` | `economics.py`; `1 file changed, 1 insertion(+), 1 deletion(-)` | `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` | `ea81ad343a31b73fd6788a7a400633f34739f933fc8e9ba073dcdaf6efa0db88` | `c35479033870e5c1811626ce623ca67a4a779bf3dea66f03375d2f8fa4022f9c` | `24f70876403398f1663a659bdc1a63b44af355f5d4118c02ed4e95c94b7c0d72` | `valid`; one changed member; no add/delete | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-04-A/modification_manifest.json:1`; `W299C_VARIANT_REBUILD_REPORT.md:33,42,51` |
| `PROBE-P012-05-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | `+2` | `economics.py`; `1 file changed, 1 insertion(+), 1 deletion(-)` | `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` | `855a020f908542256236ee4df4c4a15d66985b01e3b22542a332c90ddf213e5c` | `59eff888dbb654e8cda576132fe4244aa7f2a3f7d55f7501e620a716586838ac` | `44251938704af7f92d1e880b4dd3b4239c21ac927daae4db3840fc23c19643d5` | `valid`; one changed member; no add/delete | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-A/modification_manifest.json:1`; `W299C_VARIANT_REBUILD_REPORT.md:34,43,52` |
| `PROBE-P012-05-B` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | `+2` | `economics.py`; `1 file changed, 1 insertion(+), 1 deletion(-)` | `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` | `15fb0998a62bf9faa24958e0567a079b2e6507493a6a60242b6908c83788bc31` | `41844cf3db3790a028cd6bf71f7859ec90db94bb83083fb07785b76497090365` | `709a543786be9a07e77d1b81f6676d6c95c5bd027248e0aa85ea4dad78198661` | `valid`; one changed member; no add/delete | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-B/modification_manifest.json:1`; `W299C_VARIANT_REBUILD_REPORT.md:35,44,53` |
| `PROBE-P012-06-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | `+4` | `economics.py`; `1 file changed, 1 insertion(+), 1 deletion(-)` | `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` | `3439ce5f4673957773e5794c9a739ece8656e85b3df98fa12ccc30803d4c9180` | `2fe755a71836585361592e9bd3b913f843ccb3a9c0ba523a44e1d65561048869` | `39c8af08f17c7bf3f8d7c689b8ce0db7d3d1ee8504aa5fedf5d401c0149e5380` | `valid`; one changed member; no add/delete | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-06-A/modification_manifest.json:1`; `W299C_VARIANT_REBUILD_REPORT.md:36,45,54` |
| `PROBE-P012-07-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | `+3` | `economics.py`; `1 file changed, 1 insertion(+), 1 deletion(-)` | `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` | `19783a5ec51d34952fd4c22a8435758149455e7dda47f12fe6727a3d325a1a46` | `b65811b6d77e376d34ffad34b7210cf6a0f983ee3bdf9c5efd0c2e88c4ca2e9c` | `57fee87191150d2afb983017339e1cec1a63faed80694155af803313afd40f37` | `valid`; one changed member; no add/delete | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification_manifest.json:1`; `W299C_VARIANT_REBUILD_REPORT.md:37,46,55` |
| `PROBE-P012-08-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | `+40` | `economics.py`; `1 file changed, 1 insertion(+), 1 deletion(-)` | `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f` | `51e7a42faeab322234312d38a5bf49351c15ad6c3fb2cf98b469dee931da5264` | `98e73b51a0ee3ac05a285a8a0710f73ea0a9e621171317b4806cf0eb335c04c1` | `96aaa32930b1bfff487fadb7cdea34e14408e62fe939787c0c5e162ddb35c47d` | `valid`; one changed member; no add/delete | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/modification_manifest.json:1`; `W299C_VARIANT_REBUILD_REPORT.md:38,47,56` |

Each row's core OID, before/after digests, tree digest, patch identity, and unchanged binding fields are recorded at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/<probe-id>/modification_manifest.json:1`; each exact 119-member digest set is recorded at the sibling `modified_tree_manifest.json:1`. The verifier independently derives the HEAD tree OID and member digests from Git (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2168-2211`).

The preservation comparison against the artifact commit's parent showed that each modification manifest changed only `base_tree_oid`, `modified_copy_digest`, and `modified_tree_manifest_sha256`; the recomputed `before_sha256` and `after_sha256` remained byte-identical because W304 did not change `economics.py`. All modification-operation fields, including `expected_failed_check`, `expected_first_changed_node`, `patch_path`, `patch_sha256`, and every `modification.patch`, remained unchanged (`W299C_VARIANT_REBUILD_REPORT.md:57`).

## Probe-mode dispositions

Command: `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode probe --baseline-root C:\tmp\P012_BASELINE_RUN` from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`, with `PYTHONDONTWRITEBYTECODE=1` (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299C_PROBE_VARIANT_REBUILD_OFFSET.md:48-51`).

| Probe | Status | Digest status | Refusal | Evidence |
|---|---|---|---|---|
| `PROBE-P012-01-A` | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_CATALOG_DIGEST_MISMATCH` | `W299C_VARIANT_REBUILD_REPORT.md:59` |
| `PROBE-P012-01-B` | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_CATALOG_DIGEST_MISMATCH` | `W299C_VARIANT_REBUILD_REPORT.md:60` |
| `PROBE-P012-02-A` | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_CATALOG_DIGEST_MISMATCH` | `W299C_VARIANT_REBUILD_REPORT.md:61` |
| `PROBE-P012-03-A` | `DETECTED` | `PROBE_DIGEST_MATCH` | none | `W299C_VARIANT_REBUILD_REPORT.md:62` |
| `PROBE-P012-04-A` | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_CATALOG_DIGEST_MISMATCH` | `W299C_VARIANT_REBUILD_REPORT.md:63` |
| `PROBE-P012-05-A` | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_CATALOG_DIGEST_MISMATCH` | `W299C_VARIANT_REBUILD_REPORT.md:64` |
| `PROBE-P012-05-B` | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_CATALOG_DIGEST_MISMATCH` | `W299C_VARIANT_REBUILD_REPORT.md:65` |
| `PROBE-P012-06-A` | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_CATALOG_DIGEST_MISMATCH` | `W299C_VARIANT_REBUILD_REPORT.md:66` |
| `PROBE-P012-07-A` | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_CATALOG_DIGEST_MISMATCH` | `W299C_VARIANT_REBUILD_REPORT.md:67` |
| `PROBE-P012-08-A` | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_CATALOG_DIGEST_MISMATCH` | `W299C_VARIANT_REBUILD_REPORT.md:68` |

Exit was `0`; mode was `probe`; claim label was `NON_ACCEPTING_PROBE_EVIDENCE`; blocker count was `9` (`W299C_VARIANT_REBUILD_REPORT.md:58-68`). The verifier reports catalog-pin mismatches as could-not-evaluate artifact outcomes before driving a child process (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2905-2935`). This is the exact expected intermediate state, not an artifact-validation failure: direct checks with the newly measured pins all returned `valid=true` (`W299C_VARIANT_REBUILD_REPORT.md:39-47`).

## Discrepancies

1. **The literal delete/recreate operation could not be executed.** The task requires deleting each tree before recreating it (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299C_PROBE_VARIANT_REBUILD_OFFSET.md:26-28`), but the shell safety policy rejected both recursive-delete forms before execution (`W299C_VARIANT_REBUILD_REPORT.md:28`). The already-measured 119/119 identical member sets, zero extras, and zero variant caches allowed a full tracked-member overwrite to produce the required byte state without broadening scope (`W299C_VARIANT_REBUILD_REPORT.md:39-47`). This procedural deviation did not change the resulting artifact contract; the verifier's exact member/digest/diff/patch-result checks passed. The rejection has no independent repository source beyond this durable command transcript.
2. **The literal directory-level `git diff --no-index --stat core/ probe/kernel/` cannot show one file in this worktree.** The live `core/` working directory contains 17 pre-existing ignored `.pyc` files; the repository explicitly ignores `__pycache__/` and `*.pyc` (`MTC_COMMAND_CENTER/.gitignore:19-20`). Because the variant correctly excludes caches, the literal directory command reports `18 files changed` for every probe: 17 cache deletions plus `economics.py` (`W299C_VARIANT_REBUILD_REPORT.md:69`). Removing out-of-scope core bytes would violate the lane fence (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299C_PROBE_VARIANT_REBUILD_OFFSET.md:8-11`). I therefore quoted the file-level `--no-index --stat` for the sole tracked change (`W299C_VARIANT_REBUILD_REPORT.md:48-56`) and used the verifier's HEAD-tree enumeration to prove 119/119 members, exactly `['economics.py']` changed, and zero added/deleted members (`W299C_VARIANT_REBUILD_REPORT.md:39-47`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2168-2211,2393-2402`).

No repository-content discrepancy changed the requested target result. The catalog mismatch is expected and intentionally left for the Lead (`W299C_VARIANT_REBUILD_REPORT.md:58-68`); catalog, canonical manifest, anchor, core, harness, golden, and patch bytes were not changed (`W299C_VARIANT_REBUILD_REPORT.md:57,71`).

## Commits

- Starting HEAD: `1d2dd8652ff63c9121cbe3dbfc679da21f7cd251` (`W299C_VARIANT_REBUILD_REPORT.md:27`).
- Nine-probe artifact commit: `1c2b710cf836cbd3ec88ca94ff0e772f63d13d82` (`27 files changed, 189 insertions, 117 deletions`; `W299C_VARIANT_REBUILD_REPORT.md:70`).
- Report: committed separately after authoring; its commit hash cannot be embedded in its own bytes and is supplied in the chat close.

## Findings

- Artifact findings: **0**. All nine direct artifact validations are valid (`W299C_VARIANT_REBUILD_REPORT.md:39-47`).
- Expected remaining boundary: **9** catalog digest mismatches, one for each rebuilt KERNEL probe (`W299C_VARIANT_REBUILD_REPORT.md:58-68`); catalog re-pin/re-seal is expressly out of this lane and is the Lead's next act (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299C_PROBE_VARIANT_REBUILD_OFFSET.md:48-51`).
