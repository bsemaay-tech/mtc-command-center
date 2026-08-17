# Claude Pro kickoff preflight — 2026-08-12

**Gate: T2 static. Overall verdict: NO-GO.** All four kickoffs still require prompt corrections before the 23:00 window.

## Scope and supersession

While this audit was underway, a **separate live session edited and committed all four kickoffs** at external commit `d4a07438`; current HEAD is `b90d9b4d55edef7d626566fc9d6a08830605f3a3`. This preflight is a **current-state** audit of the post-`d4a07438` bytes and **supersedes the earlier snapshot preflight** at HEAD `416d68be`. Findings that the `d4a07438` session already fixed are recorded as fixed, not re-raised.

This audit itself did not edit any kickoff or source file and did not mutate Git. Only this report is our authorized write.

## Current kickoff identities

| Kickoff | Path | Bytes | Lines | SHA-256 |
|---|---|---|---|---|
| Transport | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md` | 5215 | 75 | `17ccf51eeda373f69d1db6a330620329f5dfe49d17637b0bfce811d927faa1e4` |
| RP7 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md` | 5623 | 81 | `2a8441e739de55628e1e33b09cc341e383309f8b1a1b4fdb5de896047ef8edad` |
| RP6 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md` | 11741 | 175 | `f54bc9f28cf080fb76392c8da376a2e4d2eb3f43702739e97acf719afc0a07dc` |
| Pathscope | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md` | 5658 | 82 | `dad89ed2cb7caafc3d6f07b012366ea929bd2a7bf19be55fd253b792e366c434` |

Findings cite the **current** kickoff basename plus `:line`. Every repo path in a correction is given repo-relative in full.

---

## Transport — NOT ready

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:5`** — non-resolving shorthand. Replace with the exact path `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md`.

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:12-16`** — `:4` says the lane audits "these bytes", but no target identity is pinned. Add this exact table:

| File | Bytes | SHA-256 |
|---|---|---|
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh` | 13608 | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh` | 13470 | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/transport_runner.ps1` | 71137 | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv` | 7970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_setup_wpi.sh` | 26483 | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_extract_verify_wpi.sh` | 23592 | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh` | 32630 | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` |

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:27`** — cite the exact source `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:28`** — says **five** claims; the exact source carries **four** Transport findings: `F1`, `F2`, `U1`, `U2`. Replace "five claims" with those four findings. Disclosures and citations are otherwise complete and correct, and the round pin `r6` is current.

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:53-55`** — "run the published harness verbatim" is an **incomplete instruction**. `SELF_QA_TRANSPORT.md:2752-2755` contains the literal token `<scratch>/r6/pre`, which the lane cannot satisfy by copy-paste. The checked-in harness does exist: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/_r5_wsl_fixtures.sh`, 21221 B, sha `a2bb6f6e3c0022aa001db7adb58189649acab9b23b522dc0544b018f9ce7971b`. The corrected instruction must first materialize blob `61696132a5f2fce97aad4054d41a780297ff21a1` as `<scratch>/r6/pre/remote_close_tree_wpi.sh`, then pass that directory as **argument 2**, per `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_R6_REPORT_2026-08-11.md:269-272`.

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:14-15`, `KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:53`** — path precision: the working directory is the repo root, so use these exact replacements:
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md`

**Fixed / correct:** the delta gate at `KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:66-75` is now correct.

---

## RP7 — NOT ready

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:5`** — use the exact path `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`.

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:13-16`** — add the current artifact identity: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`, 108301 B, sha `0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`. Separately, `:16` names a **nonexistent** file `RP7_R9_REPORT`; replace it with `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_REPAIR_R9_REPORT.md`.

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:29`** — cite the exact source `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP7_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:59-60`** — the "no extract-and-run" prohibition **contradicts the published invocation** at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:177-182`. The exact command is:

```
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

Replace "No extract-and-run" with: **"Use the published `sed|bash` extractor exactly; do not retype or invent an ad-hoc extractor."**

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:14-16`, `KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:59`** — path precision: the working directory is the repo root, so use these exact replacements:
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP7.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_REPAIR_R9_REPORT.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`

**Fixed / correct:** the six known defects are accurate and complete; the round pin `r9` is current; the delta gate at `KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:72-81` is correct.

---

## RP6 — NOT ready

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:4-6`** — **internal contradiction.** It states Codex closed a slot "on these bytes", while `:22-25` correctly records that the current r17 SELF_QA is 1038848 B / `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac` and that r16 accepted 1024538 B / `897a5a4d92b71ca626e73a75700f60db714e5b100339205b0d40d4c36431597b` **with no carry**. Exact replacement for `:4-7`: *Codex r16 PASS-WITH-NITS covers the unchanged `RP6-P0.sh` and the historical r16 evidence only; it does not fill a current-r17 flagship slot. Claude Pro is a fresh independent auditor of r17, but not yet the second of two current-byte acceptances.* Cite the prior audit exactly as `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R16_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:50`** — wrong citation; the current producer is `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:17925`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:50-52`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:68`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:123-140`** — present the "six" and the R17 zero as **measured**. The current status at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md:53-71` withdraws that; the true R17 literal-zero count is **INDETERMINATE**. Correct wording: *r17 asserted six R16 literal-zero fields; both the six and `r17_literal_zero_measurements=0` were literals, not measurements; the current count is indeterminate pending a measured scan.*

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:72`** — cite exactly `MTC_COMMAND_CENTER/11_TRIAGE/WPI_ROUND_REPORT_CLAIM_AUDIT_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:86`** — the placeholder has moved; it is now at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md:299`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:94`** — cite exactly `MTC_COMMAND_CENTER/11_TRIAGE/WPI_UNFILLED_SLOT_SWEEP_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:71-148`** — the known-defect list is **incomplete** against `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md`. The kickoff covers `F1`, `F2`, `U1`, `U2`, `U3`. Add:
- **S1** — the global every-fence / no-temp claim at `SELF_QA_RP6.md:5-7` is contradicted by `:320-353`, `:1669-1670`, `:3128`/`:3132`.
- **U4** — the broad whole-session no-host / no-network / no-Git / no-write negatives are **author attestations**, not transcript-proved.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:115-119`** — says "those three positions" immediately after enumerating **eleven** (8 SELF_QA + status + 2 reports). Replace "three" with "eleven".

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:121-148`** — F2 needs its source citation: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md:63-71`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:163`** — the dual-acceptance claim is **false** and contradicts `:22-25`. Exact replacement: *accepting the Claude verdict fills the current-r17 Claude slot only; dual acceptance still requires a fresh `gpt-5.6-sol` xhigh audit of the r17 evidence.* Cite `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:24-26`, and note that the `:25`/`:26` inconsistency in that matrix must be reconciled.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:17`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:20`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:47`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:72`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:78-88`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:94`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:128`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:153`** — path precision: expand shorthand references using this exact canonical mapping:
- `STATUS_RP6_P0.md`, `SELF_QA_RP6.md`, `RP6_R15_REPORT_2026-08-11.md`, `RP6_R16_REPORT_2026-08-11.md`, `RP6_R17_REPORT_2026-08-12.md`, `RP6_CODEX_T0_AUDIT_R16_2026-08-12.md` all resolve under `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`.
- `WPI_ROUND_REPORT_CLAIM_AUDIT_2026-08-12.md`, `WPI_UNFILLED_SLOT_SWEEP_2026-08-12.md`, `WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md` resolve under `MTC_COMMAND_CENTER/11_TRIAGE/`.

**Fixed / correct:** title and current round at `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:1`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:15-25`, `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:37-40`; the 110817 block size and its hash; the `r10a–r17` span at `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:151`; the delta gate at `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:166-175`.

---

## Pathscope — NOT ready

**`KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:33`** — cite the exact source `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:29-30`, `KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:58-59`** — omit a **material disclosure**: the four real-block runs are **historical pinned regressions**, not current RP6/RP7 coverage. The harness itself is current, embedded and self-contained, and **intentionally** reconstructs historical blobs at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md:19-320`, with the published command at `:29-34`. Correction: label those runs historical and explicitly not current coverage.

**`KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:18-21`, `KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:33`, `KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:58`** — path precision: the working directory is the repo root, so use these exact replacements:
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_REPAIR_R2_REPORT.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_GLM_T1_AUDIT_R2_2026-08-11.md`
- parent audit `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`

**Fixed / correct:** the known `F3`/`U3` set is complete and correct; the identity block is current; the `T1/high` tier at `KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:3-5` is fixed and correct; the delta gate at `KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:73-82` is correct.

---

## Cross-kickoff current state

- External commit `d4a07438` fixed the universal globally-clean-git-status blocker, the RP6 title / reading order / byte span, and the Pathscope effort tier. These are **not** current errors and are not reported as such.
- **RP6 is internally contradictory**: `:4-6` vs `:22-25` vs `:163`.
- Tier assignments are policy-consistent: the first three are T0/xhigh, Pathscope is T1/high.
- No output-path collision, no host/network permission contradiction, and no duplicate verdict path across the four.
- All cited report and audit basenames should be written full repo-relative, since the CWD is the repo root.

## Static command table

| Lane | Harness | Current static status |
|---|---|---|
| Transport | Exists | Invocation **incomplete** — missing prerequisite blob materialization |
| RP7 | Exists | Kickoff prohibition **contradicts** the published extractor |
| RP6 | Current R17 command exists at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R17_REPORT_2026-08-12.md:71` | No nonexistent harness, but acceptance-scope and current-measurement wording are **stale** |
| Pathscope | Current, embedded | Historical pin scope must be **disclosed** |

## Verification statement

This audit ran **no harness, no WSL, and no host or network access**; it edited **no source file and no kickoff**; it performed **no Git mutation**. A separate session did commit kickoff changes at `d4a07438` — that is disclosed above, and this report makes no claim that the kickoffs were unchanged. Only this report is our authorized write.
