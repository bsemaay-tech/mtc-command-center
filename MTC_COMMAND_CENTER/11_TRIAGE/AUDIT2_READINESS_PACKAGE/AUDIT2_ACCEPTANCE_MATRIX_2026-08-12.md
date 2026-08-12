# Audit 2 current acceptance matrix

Snapshot: 2026-08-12 midday. [refreshed 2026-08-12]

[refreshed 2026-08-12] This matrix records current working identities and review state;
it is not a freeze manifest or an Audit 2 acceptance. Codex currently accepts three of the
five executable/proof-tool workstreams tracked for pre-freeze convergence: RP6, RP7, and
transport. None of the three executable sets has dual-flagship acceptance.

**[updated 2026-08-12 ~16:00] Same-day movement, so the rows below are read correctly:**
SEC102 is now **ACCEPTED-WITH-DISCLOSURE** by owner decision — freeze blocker #4 cleared.
RP6's evidence document advanced to **round 17**, so Codex's r16 acceptance no longer
describes the document under review; the block bytes are still `5132bacd…`. Four
**ADVANCE-SUPPLEMENTAL** GLM read-audits ran ahead of tonight's Claude Pro window
(transport PASS-WITH-NITS, RP7 PASS-WITH-NITS, pathscope disclosure-honesty
PASS-WITH-NITS, RP6 REQUEST_CHANGES whose central claim proved false). **None of them
closes a second-flagship slot** — that still requires Claude `claude-opus-5` and is why
every PENDING row below remains PENDING.

## Per-artifact review state

| Artifact | Exact current identity | Auditor / authority | Latest current-state result | Acceptance still missing |
|---|---|---|---|---|
| RP6-P0 | `WPI_BLOCKS_DRAFT/RP6-P0.sh`; 110817 B; SHA-256 `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330` — **block unchanged r10a→r17** [refreshed 2026-08-12] | Codex `gpt-5.6-sol` xhigh | `RP6_CODEX_T0_AUDIT_R16_2026-08-12.md`: PASS-WITH-NITS, zero required repairs; exact-byte-span census fixpoint. **Scoped to constructs in the published detection vocabulary.** [refreshed 2026-08-12] | Current-byte Claude `claude-opus-5` xhigh acceptance — **now of the r17 evidence document, not r16**. [updated 2026-08-12 ~16:00] |
| RP6-P0 — evidence doc moved to r17 | `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md` is now **1038848 B, SHA-256 `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`** at commit `671d9b40`. The r16 identity Codex actually accepted was 1024538 B / `897a5a4d…`. [updated 2026-08-12 ~16:00] | Codex `gpt-5.5` xhigh implemented r17; Lead ran the fence verbatim | Round 17 closed D026 row `RP6-11` by inversion: a closed bare-word effect model, and `dynamic_targets` converted from a hardcoded literal into a real measurement (six such literal-zero fields found across three r16 lines; `r17_literal_zero_measurements=0`). Lead run: `cases=15 pass=15 fail=0`, carried r16 grammar `50/50`, block identity unchanged. [updated 2026-08-12 ~16:00] | **No independent audit of the r17 bytes yet.** Codex's r16 acceptance does not carry forward to them. [updated 2026-08-12 ~16:00] |
| RP6-P0 - PENDING | The **r17** evidence identity above, with the block still at `5132bacd…`. [updated 2026-08-12 ~16:00] | Claude `claude-opus-5` xhigh, fresh second flagship | **PENDING** via `WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md`, repointed at r17 and asked to verify the r17 correction itself — two models disagreed about whether the r16 fence refuses `eval` (it does; the GLM claim was false). [updated 2026-08-12 ~16:00] | Lead appends the verdict; only an accepting verdict on the **r17** bytes creates dual acceptance. [updated 2026-08-12 ~16:00] |
| RP7-WPI-RO | `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`; 108301 B; SHA-256 `0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62` [refreshed 2026-08-12] | Codex `gpt-5.6-sol` xhigh | `RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`: PASS, zero required findings; descriptor-bound status body and `wpi_alloc_leaf` deleted. [refreshed 2026-08-12] | Current-byte Claude acceptance, then the separately authorized rows 1-9 build and review on changed bytes. [refreshed 2026-08-12] |
| RP7-WPI-RO - PENDING | Same exact identity above. [refreshed 2026-08-12] | Claude `claude-opus-5` xhigh, fresh second flagship | **PENDING** via `WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md`. [refreshed 2026-08-12] | Lead appends the verdict. The existing identity will be superseded when owner-directed rows 1-9 are added. [refreshed 2026-08-12] |
| Transport set | Nine-file identity detailed below. [refreshed 2026-08-12] | Codex `gpt-5.6-sol` xhigh | `TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md`: PASS. F1 remains honestly OPEN but owner-ratified accept-with-disclosure and is not a freeze blocker. [refreshed 2026-08-12] | Current-set Claude `claude-opus-5` xhigh acceptance. [refreshed 2026-08-12] |
| Transport set - PENDING | Same nine-file identity below. [refreshed 2026-08-12] | Claude `claude-opus-5` xhigh, fresh second flagship | **PENDING** via `WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md`. [refreshed 2026-08-12] | Lead appends the verdict; only an accepting current-set verdict creates dual acceptance. [refreshed 2026-08-12] |
| SEC102 composite pathproof | `WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py`; 129658 B; SHA-256 `adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a` — **module unchanged r8→r11 and HEAD** [updated 2026-08-12 ~16:00] | Codex `gpt-5.6-sol` T1; GLM-5.2 second opinion; **owner** | **ACCEPTED-WITH-DISCLOSURE — owner decision 2026-08-12 ~13:10** (Option 1, with Codex's explicit concurrence that no round 12 be opened). Evidence harness hardened r9→r11: byte-identity, object pinning, then the nameless-channel construction. GLM second opinion `SEC102_GLM_T1_2ND_OPINION_2026-08-12.md`: PASS-WITH-NITS source-level, supplemental on execution. [updated 2026-08-12 ~16:00] | **Nothing — freeze blocker #4 is CLEARED.** Four trusted-base assumptions ride forward as disclosures and must be carried verbatim into the successor prereg: outer Python runtime, PATH-resolved interpreter image, on-disk-vs-fresh-clone byte identity (fails LOUD), interpreter vocabulary (owner-ratified decision C). [updated 2026-08-12 ~16:00] |
| Pathscope prover r2 | `WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py`; 122446 B; SHA-256 `890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d` [refreshed 2026-08-12] | Codex / GLM-5.2 | Codex is FILTER-BLOCKED on source and has no accepting verdict. `PATHSCOPE_R2_GLM_AUDIT_2026-08-11.md` is favorable but SUPPLEMENTAL because it could not execute. [refreshed 2026-08-12] | Fresh flagship execution acceptance. Finding 6 remains the honest `ALLOW-LEXICAL` disclosure with residual R1. [refreshed 2026-08-12] |
| Pathscope prover r2 - PENDING | Same exact identity above. [refreshed 2026-08-12] | Claude `claude-opus-5` execution auditor | **PENDING** via `WPI_PREREG_DRAFT_ROUND1/KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md`. [refreshed 2026-08-12] | Lead appends the executing verdict and final D026 mapping. [refreshed 2026-08-12] |
| Successor preregistration R3 | `WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`; 66205 B; SHA-256 `22954e2f41e4ab21c04eff9ad51abdd657f628892f8dc81c983b6473f9c85bcd` [refreshed 2026-08-12] | Codex assembly / Lead and owner adjudication | R3 merges all 13 skeleton gaps, six RUNID changes, section 10.1, and two-commit ordering; the Lead records 34/34 conservation. MC-01..03 are owner-resolved on 2026-08-12. This is not an independent accepting final-prereg verdict. [refreshed 2026-08-12] | Implement the ratified families in the frozen composite, fill allocations and pins after the committed attestation capture, reconcile final accepted artifacts, and obtain the required final review on the frozen successor. [refreshed 2026-08-12] |
| Successor preregistration R3 - PENDING | Current draft identity above; final frozen successor identity does not yet exist. [refreshed 2026-08-12] | Final reviewer / Lead acceptance authority | **PENDING** after targeted fills and Stage-1 Commit 2. [refreshed 2026-08-12] | Lead appends the exact final identity, review verdict, and order proof. [refreshed 2026-08-12] |

## Exact transport nine-file identity

**[added 2026-08-12 ~18:20] Seven of these nine are TARGETS; two are DOCUMENTS.** The first seven
(`run_p0.sh` through `remote_close_tree_wpi.sh`) are the frozen target set. `SELF_QA_TRANSPORT.md`
and `STATUS_TRANSPORT.md` are evidence/status documents that legitimately change as rounds land.
This table is a list of **current identities**, not a claim that all nine are unchanged — the
round-6 Codex audit returned REQUEST_CHANGES on exactly that false "nine-file unchanged" claim,
and the self-QA now correctly scopes its unchanged claim to the seven targets. Do not restate the
nine-file version.

| File | Bytes | SHA-256 |
|---|---:|---|
| `run_p0.sh` | 13608 | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c` [refreshed 2026-08-12] |
| `run_ro.sh` | 13470 | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c` [refreshed 2026-08-12] |
| `transport_runner.ps1` | 71137 | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2` [refreshed 2026-08-12] |
| `TRANSPORT_PLAN.tsv` | 7970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` [refreshed 2026-08-12] |
| `remote_setup_wpi.sh` | 26483 | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5` [refreshed 2026-08-12] |
| `remote_extract_verify_wpi.sh` | 23592 | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b` [refreshed 2026-08-12] |
| `remote_close_tree_wpi.sh` | 32630 | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` [refreshed 2026-08-12] |
| `SELF_QA_TRANSPORT.md` | 194204 | `0a11d035f439906972386e354fa2dfb6bac5545fcd2db298adf64019bad25175` [refreshed 2026-08-12] |
| `STATUS_TRANSPORT.md` | 22791 | `0f30944c1b7a1559ac8b7867984daa5c05cb0b14b7472a68a9932027f0380890` [refreshed 2026-08-12] |

[refreshed 2026-08-12] The first seven identities are reproduced in the Codex transport
confirmation. The final two are the exact current package-document identities at this
refresh and must be re-derived by the pending Claude auditor before acceptance.
