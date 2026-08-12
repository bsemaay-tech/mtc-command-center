# Claude Pro kickoff preflight — 2026-08-12

**Verdict: NO-GO overall.** All four kickoffs are NOT ready to dispatch before 23:00. This is a static T2 audit against snapshot HEAD `416d68befd45500d0e5f77e8c66881e66c2867f4` (read-only `git rev-parse HEAD`); no harness was run, no source or kickoff file was edited, and no Git mutation was performed. Only this report is authorized.

## Kickoff identities audited

| Kickoff | Path | SHA-256 | Size / lines |
|---|---|---|---|
| Transport | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md` | `a8f83219dae4ce95337dfd5a834b57d5a64736262552e91ff2a2e8af32f3391c` | 4509 B / 66 |
| RP7 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md` | `fc8dc912e4cab20c4e75edf345e6a65e403b7ee56ab465c8640b5d7dcca80610` | 4929 B / 72 |
| RP6 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md` | `0bc3b584238efffc45c647cf7a21394f9e517b84c35d5f8504df982bfc3e49dd` | 10502 B / 158 |
| Pathscope | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md` | `440e486a2a8d098b308fbbf7e5b6c3d9aa04f2e6925998759eebdb8e2b39ea6d` | 4787 B / 71 |

The four SHA-256 values, byte sizes and line counts above are exact **at snapshot HEAD `416d68befd45500d0e5f77e8c66881e66c2867f4`** and are not asserted for any other tree state.

Kickoff citations below use the exact kickoff basename plus `:line`; every repo path referenced in a correction is given repo-relative in full.

---

## Transport — NOT ready

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:5`** — block reference is not exact. Correction: cite exactly `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md`.

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:12-16`** — the input list names files without byte/hash identities, so the lane cannot prove it read the same bytes. Correction: add these identities, written repo-relative in full.

| Path | Bytes | SHA-256 |
|---|---|---|
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh` | 13608 | `4f608ad5b61ee553a7e0c42fc238fbba0a48c383e4365f8535184689be213c0c` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh` | 13470 | `3dea6e64a2ed20b7f81553888f86149836ec7796b7bf03c8b5561ea304cf43e3c` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/transport_runner.ps1` | 71137 | `4db0fbd16889667107329a4df77aa2b7713c87f17929a4d646b062280b47fd2` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv` | 7970 | `e3c11218a8cb057bebba0f5a7ad6684a82ad10f7943990491db9ab0abbf50e3c` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_setup_wpi.sh` | 26483 | `4428a60d99e8518a238e88f85f068bff6cb596ad1f8879bdbbbd3181ac9b5aa5` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_extract_wpi.sh` | 23592 | `5b3c0b22647039903405e7757da5863366084ad519369bf199ef60b9ee40a55b` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh` | 32630 | `8892574f52be1468930de159014cf3bc3c5f6510b42be7728beaa10ce68732cf` |

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:27`** — source-audit reference is not exact. Correction: cite exactly `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:28`** — finding count is wrong: says five, the source carries four. Correction: change "five" to "four". The source set F1, F2, U1, U2 is complete, its citations are correct, and r6 is the current round — no further carry needed.

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:53-55`** — the "verbatim" command is incomplete and will not reproduce. The Transport SELF_QA at `:2752-55` requires `<scratch>/r6/pre`, and the harness `_r5_wsl_fixtures.sh` does exist (21221 B, sha `a2bb6f6e3c0022aa001db7adb58189649acab9b23b522dc0544b018f9ce7971b`), so the gap is setup, not availability. Correction: materialize blob `61696132a5f2fce97aad4054d41a780297ff21a1` as `<scratch>/r6/pre/remote_close_tree_wpi.sh`, then pass the directory as arg2 per `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_R6_REPORT_2026-08-11.md:269-272`.

**`KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md:66`** — the exit gate demands a global clean working-tree status, which cannot hold in this repo state. Correction: replace with the exact dirty-worktree procedure given under *Cross-kickoff findings → Dirty-status gate*, using this lane's verdict path `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`.

---

## RP7 — NOT ready

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:5`** — block reference is not exact. Correction: cite exactly `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`.

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:13-16`** — missing artifact identity. Correction: add 108301 B, sha `0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`.

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:16`** — cites `RP7_R9_REPORT`, which does not exist. Correction: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_REPAIR_R9_REPORT.md`.

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:29`** — source-audit reference is not exact. Correction: cite exactly `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP7_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:59-60`** — self-contradicting instruction. The kickoff prohibits extraction, but the published invocation at `SELF_QA_RP7.md:177-182` is itself an extractor. The literal exact published invocation is:

```
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

It is published at `SELF_QA_RP7.md:177-182`, and the fenced command body it extracts is delimited by the `# RP7_EXACT_COMMAND_BEGIN` / `# RP7_EXACT_COMMAND_END` markers inside that same `SELF_QA_RP7.md`. The `SELF_QA_RP7.md` argument is relative to the invocation's own working directory as published; the lane must resolve it from the repo-relative SELF_QA path stated in its own input list (`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:13-16`) rather than assume the repo root. Following the prohibition forces retyping, which is exactly what the block forbids. Correction: replace the no-extract instruction with "use the exact published extractor above; no retyping and no ad-hoc extraction."

**`KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:72`** — global clean-status gate. Correction: use the exact dirty-worktree procedure under *Cross-kickoff findings → Dirty-status gate*, with this lane's verdict path `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`.

The six source findings (3 false, 1 scope, 2 unsupported) are complete and correctly characterized, and r9 is the current round.

---

## RP6 — NOT ready

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:1`** — scoped to r16. Correction: r16 → r17 for the evidence and effect model.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:4-7`** — false claim that r16 coverage lands "on these bytes." r16 Codex covered `SELF_QA_RP6.md` at 1024538 B, sha `897a5a4d…`; r17 is 1038848 B, sha `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac` at commit `671d9b40`. Correction: state that r16 covers the unchanged block and prior evidence, not r17, per the acceptance matrix at `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:24-26`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:15-17`** — reading order pinned to the stale identity. Correction: use the r17 identity; read `STATUS_RP6_P0.md`, then `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R17_REPORT_2026-08-12.md`, and treat the r16 verdict as context only.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:42`** — wrong citation. Correction: `SELF_QA_RP6.md:17925`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:42-44`** — presents the r17 "six" and "r17 zero" figures as measurements. They are literals asserted by r17, not counted values, and `STATUS_RP6_P0.md:53-71` now records the true count as INDETERMINATE. Correction: restate both as asserted literals and carry the INDETERMINATE status forward.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:64`** — reference is not exact. Correction: cite exactly `MTC_COMMAND_CENTER/11_TRIAGE/WPI_ROUND_REPORT_CLAIM_AUDIT_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:78`** — unresolved status placeholder. Correction: the current exact value is `STATUS_RP6_P0.md:299` — cite it in full, not as a bare `:299`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:86`** — reference is not exact. Correction: cite exactly `MTC_COMMAND_CENTER/11_TRIAGE/WPI_UNFILLED_SLOT_SWEEP_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:63-140`** — finding set is incomplete against `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md`. Existing coverage is F1, F2, U1, U2, U3. Correction: add **S1** — the global no-temp claim at `SELF_QA_RP6.md:5-7` is contradicted by `SELF_QA_RP6.md:320-353`, `:1669-70`, `:3128` and `:3132`; and add **U4** — the broad session-negative claims are attestations, not transcript proof.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:107`** — position count wrong. Correction: three → eleven positions.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:113-140`** — findings restated without provenance. Correction: cite source audit `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md:63-71`.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:143`** — round span stale. Correction: r10a–r16 → r10a–r17.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:155`** — misstates what Claude acceptance achieves. Claude accepting fills only the Claude r17 slot; **a fresh gpt-5.6-sol xhigh r17 audit still remains outstanding.** The acceptance matrix at `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:25-26` is internally inconsistent — `:25` says no carry while `:26` says Claude creates a dual — and the current-coverage rule wins. Correction: rewrite `:155` to the current-coverage reading, citing `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:25-26`, and reconcile those two lines.

**`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:158`** — global clean-status gate. Correction: the exact dirty-worktree procedure under *Cross-kickoff findings → Dirty-status gate*, with this lane's verdict path `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`. The block figure 110817, its hash, and the commit are correct.

---

## Pathscope — NOT ready

**`KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:3`** — tier/effort is wrong: it currently declares T1/xhigh. Correction: T1/xhigh → T1/high.

**`KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:31`** — source-audit reference is not exact. Correction: cite exactly `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`.

**`KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:56-57`** — treats four real-block runs as if they were current coverage. That is the whole defect: the four runs are historical pinned regressions (`SELF_QA_PATHSCOPE.md:19-25` pins the old blobs) and must not be represented as current RP6/RP7 coverage. The embedded harness itself exists and is current — self-contained at `SELF_QA_PATHSCOPE.md:27-320` with its command at `:29-34`. Correction: state the historical-pinned-regression framing explicitly and require that these runs not be presented as current RP6/RP7 coverage.

**`KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md:71`** — global clean-status gate. Correction: the exact dirty-worktree procedure under *Cross-kickoff findings → Dirty-status gate*, with this lane's verdict path `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`.

Identity is correct; F3/U3 coverage is complete; r2 is the current round.

---

## Cross-kickoff findings

- **Dirty-status gate (all four).** Every kickoff gates its verdict on a globally clean working tree. In this repo state that gate can never pass, so all four would self-block. Each lane's verdict path is exactly:

  | Lane | Verdict path |
  |---|---|
  | Transport | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` |
  | RP7 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` |
  | RP6 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` |
  | Pathscope | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md` |

  Replace the gate uniformly with this exact procedure, in each kickoff, using that exact lane verdict path from the table above:
  1. **Before execution**, capture the baseline: `git status --porcelain` → `before`.
  2. Run the lane.
  3. **At the end**, capture `git status --porcelain` → `after`, and prove that `after` minus `before` contains **only** that exact lane verdict path and nothing else. Any other entry in the delta fails the gate.
  4. Also run `git status --porcelain -- <that exact lane verdict path>` and record its output as the path-scoped confirmation.
- **Tier consistency.** Transport, RP7 and RP6 correctly declare T0/xhigh. Pathscope currently declares T1/**xhigh**, which is the incorrect value; the correct replacement is T1/**high**.
- **Currency of the Codex/dual claim.** RP6 is the only kickoff that misstates the current Codex coverage and the dual-acceptance rule; the other three are accurate on this point.
- **Basename resolution.** The cited audit/report basenames identified above do not resolve from the repo root. Every path must be written repo-relative in full.
- **No output collision and no permission contradiction** were found across the four kickoffs.

### Harness readiness

| Lane | Harness | State |
|---|---|---|
| Transport | exists — `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/_r5_wsl_fixtures.sh` | setup incomplete — `<scratch>/r6/pre` not materialized; see `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_R6_REPORT_2026-08-11.md:269-272` |
| RP7 | exists — published extractor at `SELF_QA_RP7.md:177-182` | prohibition at `KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md:59-60` contradicts that published extractor |
| RP6 | r17 command exists at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R17_REPORT_2026-08-12.md:71` | scope stale (r16-pinned) in `KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:1` |
| Pathscope | current, embedded and self-contained at `SELF_QA_PATHSCOPE.md:27-320`, command at `:29-34` | historical pinned regression blobs (`SELF_QA_PATHSCOPE.md:19-25`), not current coverage |

## Disposition

Dispatch is blocked on all four lanes until the corrections above are applied to the kickoff files. The dirty-status gate and the RP6 r16→r17 scope error are the two blockers that would invalidate a lane's verdict even if everything else were dispatched as-is.

## Verification of this audit's own conduct

- **No harness was run** — no lane harness, extractor, runner script or published command was executed.
- **No WSL invocation** — no `bash`, no WSL entry, no shell fixture execution.
- **No host or network action** — no remote setup/extract/close, no SSH, no fetch.
- **No source or kickoff edit** — none of the four kickoff files, no SELF_QA, no pre-existing audit/evidence report, no acceptance matrix was modified.
- **No Git mutation** — the only Git command run was read-only `git rev-parse HEAD`, returning `416d68befd45500d0e5f77e8c66881e66c2867f4`.
- **Sole repo file created or edited by this audit:** `MTC_COMMAND_CENTER/11_TRIAGE/WPI_CLAUDEPRO_KICKOFF_PREFLIGHT_2026-08-12.md` — this report.