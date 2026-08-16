# WPI artifact retention inventory — 2026-08-17

## 0. Scope and non-action boundary

This is a read-only inventory of every top-level object under
`C:\WPI_ARTIFACTS`. No object was deleted, moved, compressed, modified, staged,
committed, transferred, or used against a host. No secret-bearing file was
opened, no credential value was inspected, and no new content hash was computed.

Sizes are exact filesystem bytes observed on 2026-08-17. Existing manifest
records and hashes were read only from safe identity/manifests and repository
evidence. A classification of `archive candidate` is not deletion approval.

## 1. Executive result

The root contains **152 top-level objects** totalling **5,208,923,013 bytes
(4.851 GiB)**.

| Family | Top-level objects | Exact bytes | Retention finding |
|---|---:|---:|---|
| Release directories/product tar | 5 | 5,199,251,082 | 99.81% of all bytes; evidence/rollback sensitive |
| Scratch/cache directories | 5 | 7,520,790 | Likely regenerable; only 7.17 MiB |
| Gate-A audit/support | 54 | 1,176,713 | Historical prompts, reports, wrappers and audit outputs |
| Gate-A run-kit dirs/tars | 11 | 835,915 | Hash-bound execution inputs; includes accepted and rejected evidence |
| Gate-A execution/preflight/postcheck | 74 | 75,292 | Small but historically non-reproducible evidence |
| WPL transport captures | 3 | 63,221 | Copies have corresponding Git evidence trees |

The only material storage opportunity is the three older extracted releases:

- `1adf9ae5...`: 1,051,904,669 bytes;
- `ebada020...`: 1,033,359,158 bytes;
- `ed3d0534...`: 1,033,359,494 bytes.

Together they occupy **3,118,623,321 bytes (2.904 GiB)**. They are not approved
for deletion. The safe next step is a retention ledger plus verified cold-copy
and restore drill, not an immediate cleanup.

## 2. Evidence-reference codes used below

| Code | Repository evidence |
|---|---|
| `ER1` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_CANDIDATE_ACCEPTANCE_RECORD_2026-08-01.md` |
| `ER2` | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_ARTIFACT_IDENTITY_AND_SECRET_SCAN_EBADA020_2026-08-03.md` |
| `ER3` | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_PREREGISTRATION_ADDENDUM_C_2026-08-08.md` |
| `ER4` | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md` |
| `ER5` | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08B.md` and `...08C.md` |
| `ER6` | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_PACKAGE_TRANSFER_2026-08-09.md` |
| `ER7` | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A5_E_PACKAGE_2026-08-09.md`, `GATE_A_A5_E_TRANSFER_2026-08-09.md`, and `GATE_A_A5_E_CANONICAL_ACCEPTANCE_2026-08-09.md` |
| `ER8` | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md` plus the A5–A9 pass reports |
| `ER9` | `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/EVIDENCE_INDEX.md` and `FINAL_HANDOFF.md` |
| `ER10` | `_AI_MEMORY/archive/GLOBAL_HANDOFF_2026-08-01_to_2026-08-15.md` and archived `NEXT_STEPS` chronology |

## 3. Release and product-transfer objects

All four commit objects are currently available in local Git, so a new source
export is possible. That does not make the accepted artifact bytes disposable:
the existing manifest, export behavior, tar metadata, audit evidence, and any
rollback use are separate identities.

| Path | Files | Exact bytes | Candidate / existing identity | Likely role | Duplicate/rebuild/retention |
|---|---:|---:|---|---|---|
| `C:\WPI_ARTIFACTS\1adf9ae51b0ddfe81057860aec5c23bb842f5a84` | 7,061 | 1,051,904,669 | SHA `1adf...`; `RELEASE_SHA256SUMS` present; manifest SHA-256 `bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02` (`ER1`) | Locally/static accepted WP-I candidate, later historical/superseded (`ER1`, `ER10`) | Commit exists. Rebuildable as source in principle, but exact accepted artifact should be cold-retained until its evidence obligations are closed. Archive candidate, not deletion candidate. |
| `C:\WPI_ARTIFACTS\ebada020a59edf539f60acfbb3a6bf870c8679e9` | 7,060 | 1,033,359,158 | SHA `ebada...`; manifest present; manifest SHA-256 `8fc30864ba342e53dcfc6b2938124f91d005f02671a332580a723f38fd4700c9` (`ER2`) | Accepted predecessor; previously installed on staging, later torn down and superseded (`ER2`, `ER8`) | Commit exists. Historical artifact; remote inert tar has a separate retained role. Archive only after evidence/rollback ledger and restore proof. |
| `C:\WPI_ARTIFACTS\ed3d053432fb496123ac43bcb7d40cfb64edbb8b` | 7,060 | 1,033,359,494 | SHA `ed3d...`; manifest present; manifest SHA-256 `8964cc43b802bada1ad5611e5b445e19b4332c45133af3e8473a85bb57e7ee4b` (`ER3`) | Validly built repair-round-1 parent, explicitly not accepted; superseded by `2ce41e34` (`ER3`, `ER4`) | Commit exists. Strongest large archive candidate, but preserve rejection/repair provenance before relocation. |
| `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b` | 7,060 | 1,033,362,481 | SHA `2ce...`; manifest present; manifest SHA-256 `edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26` (`ER4`, `ER5`) | Accepted frozen candidate; Gate-A A0–A9 staging evidence anchor; current V1/rollback-critical object | **Keep active and immutable.** Commit exists, but rebuilding is not a substitute for this accepted instance. |
| `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b.tar` | 1 | 1,047,265,280 | Candidate `2ce...`; recorded tar SHA-256 `d78b9e82f5f28a35a51033c5405fc1501e2c8fd4385b6d7fe012e92745b905f2` (`ER5`, `ER8`) | Accepted transfer serialization of current V1 | Serialized duplicate of the extracted candidate plus tar metadata. **Keep active** until another verified recoverable transfer copy and restore test exist. Exact tar-byte rebuild is not assumed. |

This inventory confirms that the named manifests are present; it does not rerun
`sha256sum -c` over the four large trees. Their current byte integrity therefore
continues to rest on the cited accepted evidence until a future authorized
retention gate re-verifies it.

### Existing-manifest duplicate relationships

No release file was rehashed. The comparisons below use the four already-present
`RELEASE_SHA256SUMS` files.

| Pair | Common paths | Identical existing hashes | Meaning |
|---|---:|---:|---|
| `ebada020` vs `ed3d0534` | 7,059 | 7,055 | Near-duplicate release; 4 content changes |
| `ebada020` vs `2ce41e34` | 7,059 | 7,053 | Near-duplicate release; 6 content changes |
| `ed3d0534` vs `2ce41e34` | 7,059 | 7,054 | Near-duplicate release; 5 content changes |
| `1adf9ae5` vs each later release | 7,058 | 568 | Same broad tree shape but not byte-identical export; do not treat as simple duplicate without preserving its own manifest |

## 4. Gate-A run-kit objects

Common candidate: `2ce41e34...`. Directory rows have their own `SHA256SUMS`.
Tar hashes below are pre-existing repo records; none was recomputed. A directory
and its tar are logical duplicates in different formats, but the tar metadata is
part of accepted transfer identity.

| Path | Type/files | Exact bytes | Existing manifest/hash | Likely role and evidence | Duplicate/rebuild/retention |
|---|---:|---:|---|---|---|
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260808B-2ce41e34` | dir/8 | 45,334 | `SHA256SUMS` present | Historical prepared B kit (`ER5`) | Superseded only where C corrected A3. Retain chronology; source scripts may be reconstructed but historical package identity is not assumed reproducible. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260808B-2ce41e34.tar` | file/1 | 61,440 | SHA-256 `ac0fbaf2fefa8241c5c92f5bf35a3f9fc5258a4b7e30614988ed305afa61c0fb` | Frozen B transfer form (`ER5`) | Serialized B directory; historical. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260808C-2ce41e34` | dir/8 | 46,545 | `SHA256SUMS` present | C corrected A3 checker; transferred/used, canonical A3/A4 chain input (`ER5`) | Retain as accepted evidence input. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260808C-2ce41e34.tar` | file/1 | 53,760 | SHA-256 `4ee5ba920800ceff8f55338bcba5b388d39d2457f9970795af89c9333767f855` | Accepted C transfer form (`ER5`) | Serialized C directory; retain. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34` | dir/8 | 55,514 | `SHA256SUMS` present | Accepted D kit; A5 D failed, A6–A9 used D (`ER6`, `ER8`) | Mixed canonical/repaired history; retain. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.tar` | file/1 | 71,680 | SHA-256 `e8a52e3cdeaa9da9315d0cbeb1fde7dd75e9ecc8a4ad4c926e4084c37c55e0d3` | Accepted/transferred D tar (`ER6`) | Serialized accepted D directory; retain. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.rejected-crlf` | dir/8 | 56,698 | `SHA256SUMS` present | Explicitly rejected CRLF package, negative evidence (`ER6`) | Near-duplicate of D but deliberately non-acceptable. Never execute; retain until rejection evidence is archived. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.rejected-crlf.tar` | file/1 | 71,680 | SHA-256 `66ce7a1e148d17626f68962ccdd3bb6bcacdf4c49a6eb815713caa64899634a8` | Rejected CRLF transfer object (`ER6`) | Same byte count as accepted D tar but different hash; negative evidence, not a duplicate safe to conflate. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260809E-2ce41e34` | dir/4 | 120,072 | `SHA256SUMS` present | Accepted A5 repair E kit (`ER7`) | Retain as canonical A5 input. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260809E-2ce41e34-verify` | dir/4 | 120,072 | Nested extracted `SHA256SUMS`; same four names/sizes and same manifest lines as E | Local extraction/verification copy (`ER7`) | Declared verification copy with matching manifest text/names/sizes; current member bytes were not freshly rehashed. First small relocation candidate after the canonical E dir/tar has independent restore proof. |
| `C:\WPI_ARTIFACTS\gatea-run-kit-20260809E-2ce41e34.tar` | file/1 | 133,120 | SHA-256 `895fe530f4fe85b9dc0c86332776899c88492197c2748c1de14f950f0e6f1cef` | Accepted/transferred E tar (`ER7`) | Serialized E directory; retain. |

## 5. WPL transport capture directories

Common candidate: `2ce41e34...`. Each directory contains
`TRANSPORT_RECORD.txt` and `TRANSPORT_SHA256SUMS.txt`. For each row, the file
count and every relative path/size match the corresponding Git operator-record
tree. No fresh content rehash was performed; `ER9` contains the recorded hashes.

| Path | Files | Exact bytes | Git counterpart / likely role | Duplicate/rebuild/retention |
|---|---:|---:|---|---|
| `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08` | 36 | 27,043 | `.../03_TRANSPORT/operator_record`; original B3 transport capture (`ER9`) | Likely exact evidence copy; verify its internal manifest against Git before any relocation. Git contains the durable counterpart. |
| `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08-R45B` | 15 | 14,285 | `.../05_TRANSPORT_R45B/operator_record`; R45B capture (`ER9`) | Same retention rule. |
| `C:\WPI_ARTIFACTS\WPLP2B_TRANSPORT_WPLP2B-20260809T210610Z-834380c5` | 31 | 21,893 | `.../09_TRANSPORT_B3B/operator_record`; B3B successor capture (`ER9`) | Same retention rule. |

## 6. Scratch/cache directories

Common candidate/context: Gate-A E / `2ce41e34`. No adjacent manifest or
authoritative hash record was found. These look regenerable and are the lowest
risk cleanup family, but together save only 7.17 MiB. Do not remove them until a
later approved cleanup confirms no report points to their exact paths.

| Path | Files | Exact bytes | Likely role | Duplicate/rebuild |
|---|---:|---:|---|---|
| `C:\WPI_ARTIFACTS\gatea-e-codex2-temp` | 63 | 1,700,336 | Temporary Codex audit/test tree | Regenerable in principle; no manifest. |
| `C:\WPI_ARTIFACTS\gatea-e-lead-pycache-r3` | 57 | 1,464,664 | Python bytecode/cache from round 3 | Regenerable cache. |
| `C:\WPI_ARTIFACTS\gatea-e-lead-pycache-r3-final` | 57 | 1,464,664 | Final-named copy of round-3 cache | Same count/bytes as prior row; likely duplicate, content identity not newly proven. |
| `C:\WPI_ARTIFACTS\gatea-e-pycache` | 57 | 1,430,629 | Earlier Python cache | Regenerable cache. |
| `C:\WPI_ARTIFACTS\gatea-e-r2-pycache` | 57 | 1,460,497 | Round-2 Python cache | Regenerable cache. |

## 7. Gate-A audit/support top-level files

All 54 rows below concern Gate-A D/E work on candidate `2ce41e34`. Their primary
repo references are `ER6`, `ER7`, `ER8`, and `ER10`. There is no adjacent
top-level manifest for these individual files. Prompts/wrappers are mechanically
reconstructable in principle; audit/session outputs and reports are not
reproducible as the same historical evidence. Do not delete individual files
merely because a similarly named committed report exists.

| Path | Type | Files | Exact bytes |
|---|---|---:|---:|
| `C:\WPI_ARTIFACTS\audit-claude-e.ps1` | file | 1 | 470 |
| `C:\WPI_ARTIFACTS\audit-codex-e.ps1` | file | 1 | 381 |
| `C:\WPI_ARTIFACTS\audit-deepseek-e.ps1` | file | 1 | 336 |
| `C:\WPI_ARTIFACTS\audit-glm-e.ps1` | file | 1 | 235 |
| `C:\WPI_ARTIFACTS\build_gatea_e_package.py` | file | 1 | 4,134 |
| `C:\WPI_ARTIFACTS\claude_a6_pass_checkpoint_task.md` | file | 1 | 4,631 |
| `C:\WPI_ARTIFACTS\claude_a7_pass_checkpoint_task.md` | file | 1 | 4,590 |
| `C:\WPI_ARTIFACTS\claude_a8_pass_checkpoint_task.md` | file | 1 | 4,343 |
| `C:\WPI_ARTIFACTS\claude_a9_pass_final_checkpoint_task.md` | file | 1 | 4,468 |
| `C:\WPI_ARTIFACTS\claude-gatea-a5-readiness-e-repair1-report.md` | file | 1 | 6,421 |
| `C:\WPI_ARTIFACTS\claude-gatea-a5-readiness-e-repair1-task.md` | file | 1 | 6,458 |
| `C:\WPI_ARTIFACTS\claude-gatea-a5-readiness-e-repair2-report.md` | file | 1 | 5,685 |
| `C:\WPI_ARTIFACTS\claude-gatea-a5-readiness-e-repair2-task.md` | file | 1 | 3,210 |
| `C:\WPI_ARTIFACTS\claude-gatea-a5-readiness-e-report.md` | file | 1 | 4,281 |
| `C:\WPI_ARTIFACTS\claude-gatea-a5-readiness-e-task.md` | file | 1 | 7,579 |
| `C:\WPI_ARTIFACTS\gatea-e-audit-claude.md` | file | 1 | 4,423 |
| `C:\WPI_ARTIFACTS\gatea-e-audit-codex-round2.md` | file | 1 | 1,388 |
| `C:\WPI_ARTIFACTS\gatea-e-audit-codex-round3.md` | file | 1 | 815 |
| `C:\WPI_ARTIFACTS\gatea-e-audit-codex.md` | file | 1 | 464,012 |
| `C:\WPI_ARTIFACTS\gatea-e-audit-deepseek.md` | file | 1 | 660 |
| `C:\WPI_ARTIFACTS\gatea-e-audit-glm.md` | file | 1 | 7,342 |
| `C:\WPI_ARTIFACTS\gatea-e-boundary-repro.sh` | file | 1 | 1,643 |
| `C:\WPI_ARTIFACTS\gatea-e-canonical-audit-prompt.md` | file | 1 | 1,513 |
| `C:\WPI_ARTIFACTS\gatea-e-repair-round3-claude-prompt.md` | file | 1 | 4,129 |
| `C:\WPI_ARTIFACTS\gatea-e-round3-audit-claude.md` | file | 1 | 6,350 |
| `C:\WPI_ARTIFACTS\gatea-e-round3-audit-codex-rerun.jsonl` | file | 1 | 518,823 |
| `C:\WPI_ARTIFACTS\gatea-e-round3-audit-codex-rerun.md` | file | 1 | 2,934 |
| `C:\WPI_ARTIFACTS\gatea-e-round3-audit-codex.md` | file | 1 | 6 |
| `C:\WPI_ARTIFACTS\gatea-e-round3-audit-deepseek.md` | file | 1 | 659 |
| `C:\WPI_ARTIFACTS\gatea-e-round3-audit-glm.md` | file | 1 | 8,469 |
| `C:\WPI_ARTIFACTS\gatea-e-round3-canonical-audit-prompt.md` | file | 1 | 2,740 |
| `C:\WPI_ARTIFACTS\glm_a6_preflight_checkpoint_task.md` | file | 1 | 4,192 |
| `C:\WPI_ARTIFACTS\glm_a7_preflight_checkpoint_task.md` | file | 1 | 3,636 |
| `C:\WPI_ARTIFACTS\glm_a8_preflight_checkpoint_task.md` | file | 1 | 3,727 |
| `C:\WPI_ARTIFACTS\glm_a9_preflight_checkpoint_task.md` | file | 1 | 4,052 |
| `C:\WPI_ARTIFACTS\glm-a5a9-implement-report-20260808D.md` | file | 1 | 4,014 |
| `C:\WPI_ARTIFACTS\glm-a5a9-implement-task-20260808D.md` | file | 1 | 8,503 |
| `C:\WPI_ARTIFACTS\glm-a5a9-prereg-report-20260808C.md` | file | 1 | 14,657 |
| `C:\WPI_ARTIFACTS\glm-a5a9-prereg-task-20260808C.md` | file | 1 | 5,152 |
| `C:\WPI_ARTIFACTS\glm-a5a9-repair1-report-20260808D.md` | file | 1 | 3,811 |
| `C:\WPI_ARTIFACTS\glm-a5a9-repair1-task-20260808D.md` | file | 1 | 4,866 |
| `C:\WPI_ARTIFACTS\glm-a5a9-repair2-report-20260808D.md` | file | 1 | 4,192 |
| `C:\WPI_ARTIFACTS\glm-a5a9-repair2-task-20260808D.md` | file | 1 | 2,812 |
| `C:\WPI_ARTIFACTS\glm-a5a9-repair3-report-20260808D.md` | file | 1 | 3,074 |
| `C:\WPI_ARTIFACTS\glm-a5a9-repair3-task-20260808D.md` | file | 1 | 2,098 |
| `C:\WPI_ARTIFACTS\glm-gatea-a5-fail-checkpoint-report.md` | file | 1 | 2,662 |
| `C:\WPI_ARTIFACTS\glm-gatea-a5-fail-checkpoint-task.md` | file | 1 | 6,628 |
| `C:\WPI_ARTIFACTS\glm-gatea-d-package-transfer-checkpoint-report.md` | file | 1 | 2,474 |
| `C:\WPI_ARTIFACTS\glm-gatea-d-package-transfer-checkpoint-task.md` | file | 1 | 5,482 |
| `C:\WPI_ARTIFACTS\invoke-claude-opus5-gatea-e-repair1.ps1` | file | 1 | 1,150 |
| `C:\WPI_ARTIFACTS\invoke-claude-opus5-gatea-e-repair2.ps1` | file | 1 | 1,021 |
| `C:\WPI_ARTIFACTS\invoke-claude-opus5-gatea-e.ps1` | file | 1 | 1,146 |
| `C:\WPI_ARTIFACTS\run-gatea-e-audits.ps1` | file | 1 | 2,284 |
| `C:\WPI_ARTIFACTS\verify_gatea_e_remote.sh` | file | 1 | 1,952 |

## 8. Gate-A execution, preflight, postcheck, and transition objects

All 74 rows concern candidate `2ce41e34`; evidence references are `ER7`, `ER8`,
and `ER10`. Individual `.log`, `.out`, and `.err` files have no adjacent
manifest at the top level. Many hashes are recorded in their corresponding pass
reports. Execution outputs cannot be recreated as the same historical evidence;
scripts can be reconstructed but do not replace their captured outputs.

Canonical existing hashes explicitly indexed by `ER8` include:

| Object | Existing SHA-256 |
|---|---|
| `gatea-A5-20260809E.log` | `83d947a3285a595a1df21652c8c85aa9b8e14a8a0ec2eab229f1384516fdd19c` |
| `gatea-A6-20260808D.log` | `75ed426247c2a26f6c4377f8e910826ecb4f0669565f292d538df65f2e52488c` |
| `gatea-A7-20260808D.log` | `09443b51fe01498e6530d8729b73bf2e26671b24b2a7e7b1085f8a700bbb2bf5` |
| `gatea-A8-20260808D.log` | `a7ef34a18145aee61196110dda6882c80992e189573003eb7fbf1119f829f0d7` |
| `gatea-A8-host-20260808D.log` | `abad3225fe530c00c1ef60a9cd46a0048fa1cac40135525484389d2703fee2e6` |
| `gatea-A9-20260808D.log` | `23d61687ce6cbf290b134d6bd72763f7bb4be27b15daae457373d6bb004bd5e9` |
| `post_gate_transition_inventory_20260809.out` | `b715363b9027479f3520ba0216bd486880e08852cdc7cb08eadf0c1f42719051` |
| `post_gate_transition_inventory_detail_20260809.out` | `232bb01e30f61418de411342af9d762d0649480f56b2bdd723c613077fa5157b` |
| `post_gate_transition_inventory_manifest_flags_20260809.out` | `c68c75e0be47a3cab0cc71aab4f4a51395cdc68e0ec99032b02d8103413a9fea` |

All zero-byte `.err`/`.out` objects are byte-duplicates of one another, but their
paths encode distinct successful-empty/error-empty observations. Content
deduplication must not erase that semantic evidence.

| Path | Type | Files | Exact bytes |
|---|---|---:|---:|
| `C:\WPI_ARTIFACTS\gatea-A5-20260808D.log` | file | 1 | 1,933 |
| `C:\WPI_ARTIFACTS\gatea-A5-20260809E-postcheck.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A5-20260809E-postcheck.out` | file | 1 | 691 |
| `C:\WPI_ARTIFACTS\gatea-A5-20260809E.log` | file | 1 | 3,284 |
| `C:\WPI_ARTIFACTS\gatea-A6-20260808D-command.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A6-20260808D-command.out` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A6-20260808D.log` | file | 1 | 2,007 |
| `C:\WPI_ARTIFACTS\gatea-A7-20260808D-command.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A7-20260808D-command.out` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A7-20260808D.log` | file | 1 | 4,269 |
| `C:\WPI_ARTIFACTS\gatea-A8-20260808D-command.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A8-20260808D-command.out` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A8-20260808D.log` | file | 1 | 1,087 |
| `C:\WPI_ARTIFACTS\gatea-A8-host-20260808D-command.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A8-host-20260808D-command.out` | file | 1 | 111 |
| `C:\WPI_ARTIFACTS\gatea-A8-host-20260808D.log` | file | 1 | 321 |
| `C:\WPI_ARTIFACTS\gatea-A9-20260808D-command.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A9-20260808D-command.out` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-A9-20260808D.log` | file | 1 | 876 |
| `C:\WPI_ARTIFACTS\gatea-e-preflight.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-e-preflight.out` | file | 1 | 481 |
| `C:\WPI_ARTIFACTS\gatea-e-remote-verify4.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-e-remote-verify4.out` | file | 1 | 115 |
| `C:\WPI_ARTIFACTS\gatea-e-remote-verify5.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\gatea-e-remote-verify5.out` | file | 1 | 1,846 |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_20260809.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_20260809.out` | file | 1 | 6,481 |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_20260809.sh` | file | 1 | 4,349 |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_detail_20260809.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_detail_20260809.out` | file | 1 | 1,184 |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_detail_20260809.sh` | file | 1 | 2,031 |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_manifest_flags_20260809.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_manifest_flags_20260809.out` | file | 1 | 687 |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_manifest_flags_20260809.sh` | file | 1 | 737 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a5_e.sh` | file | 1 | 3,706 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a6_d.err` | file | 1 | 129 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a6_d.out` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a6_d.sh` | file | 1 | 2,956 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a6_d.v2.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a6_d.v2.out` | file | 1 | 367 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a7_d.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a7_d.out` | file | 1 | 134 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a7_d.sh` | file | 1 | 4,416 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a7_d.v2.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a7_d.v2.out` | file | 1 | 767 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a8_host_d.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a8_host_d.out` | file | 1 | 305 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a8_host_d.ps1` | file | 1 | 2,809 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a8_remote_d.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a8_remote_d.out` | file | 1 | 339 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a8_remote_d.sh` | file | 1 | 2,574 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a9_d.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a9_d.out` | file | 1 | 427 |
| `C:\WPI_ARTIFACTS\postcheck_gatea_a9_d.sh` | file | 1 | 3,156 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a5_e.sh` | file | 1 | 2,107 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a6_d.err` | file | 1 | 56 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a6_d.out` | file | 1 | 117 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a6_d.sh` | file | 1 | 2,950 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a6_d.v2.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a6_d.v2.out` | file | 1 | 560 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a7_d.err` | file | 1 | 29 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a7_d.out` | file | 1 | 157 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a7_d.sh` | file | 1 | 3,211 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a7_d.v2.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a7_d.v2.out` | file | 1 | 628 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a8_host_d.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a8_host_d.out` | file | 1 | 307 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a8_host_d.ps1` | file | 1 | 1,836 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a8_remote_d.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a8_remote_d.out` | file | 1 | 586 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a8_remote_d.sh` | file | 1 | 2,735 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a9_d.err` | file | 1 | 0 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a9_d.out` | file | 1 | 727 |
| `C:\WPI_ARTIFACTS\preflight_gatea_a9_d.sh` | file | 1 | 4,711 |

## 9. Retention decisions still required

### Keep active now

- accepted `2ce41e34` extracted release and product tar;
- accepted C, D, and E run-kit directories/tars;
- rejected CRLF D objects until the rejection/falsification chain has a verified
  archival copy;
- canonical A5–A9 and transition evidence;
- WPL transport captures until their internal manifests are rechecked against
  the committed operator-record trees.

### Candidates for verified cold archive, not deletion

- `1adf9ae5`, `ebada020`, and `ed3d0534` extracted releases;
- B run-kit after its exact supersession/retention obligation is recorded;
- E `-verify` extraction after E directory/tar restore proof;
- local WPL transport copies after manifest equality with Git is independently
  verified.

### Likely cleanup candidates after explicit approval

- five pycache/temp directories (7,520,790 bytes total).

Removing every support/log/cache/run-kit object outside the five product release
objects would save only 9,671,931 bytes (9.22 MiB). Cleanup effort should not
focus there for capacity reasons.

## 10. Required retention-ledger and restoration gate

Before moving or deleting any material object, record:

1. exact path, type, byte count, candidate SHA and role;
2. existing manifest path and recorded hash, without reading secret values;
3. every repo evidence reference that names the object;
4. accepted/rejected/superseded/rollback status and the authority for it;
5. whether another local, host, or cold-storage copy exists;
6. cold-copy destination, object hash, access controls, and retention period;
7. successful restore into a new empty path;
8. restored byte count, manifest verification, exact member inventory, and tar
   identity where the tar itself is evidence;
9. explicit confirmation that the object is not the only accepted rollback or
   audit input;
10. owner approval for the exact paths to be moved or removed.

The restoration test must happen before cleanup, not after space has already
been reclaimed. Git commit availability proves source history, not exact release
artifact, tar, execution log, or accepted evidence recoverability.

## 11. Conclusion

`C:\WPI_ARTIFACTS` is dominated by four extracted monorepo releases and one tar.
The current `2ce41e34` pair is an active accepted evidence/rollback boundary.
The three older release directories offer 2.904 GiB of potential cold-archive
savings, but only after their status and restoration guarantees are made
explicit. The remaining 147 top-level objects total only about 9.22 MiB and are
mostly cheap but historically valuable evidence; deleting them first would add
risk without solving the storage problem.
