# Audit 2 D026 RED locations

Status: corrected location index; not a closure decision. [refreshed 2026-08-12]

[refreshed 2026-08-12] A test without an exact RED command and real output is
supplemental, not closure evidence. A candidate directory or a passing report is not a
located RED. The paths below incorporate the Lead correction directly; there is no trailing
narrative override.

Base directory for the older B3 repair cycle:

`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\`

## Corrected WP-L Phase 2 / B3 register

| Closure test or falsification | RED location | GREEN location | Classification and auditor action |
|---|---|---|---|
| R4-5 symlink-guard deletion | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\05_TRANSPORT_R45B\STAGE3B_TRANSPORT_RECORD.md` | Same record; supporting log under `05_TRANSPORT_R45B\operator_record\evidence\WPLP2-20260809T125940Z-8dc78f08-R45B\r45b.log` | LOCATED [refreshed 2026-08-12]. Rerun both arms, prove the mutation is the unique file-wide delta, and compare output and side effects. |
| Original B3 environment-file admission versus repaired EACCES boundary | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\03_TRANSPORT\B3_STOP_ADJUDICATION.md` is a prior-behavior record, but no exact D026 designation is supplied | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\09_TRANSPORT_B3B\STAGE3B_B3B_RECORD.md` | UNLOCATED AS A D026 PAIR [refreshed 2026-08-12]. Supplemental unless the dispatcher supplies an exact RED command/output mapping and both arms reproduce. |
| Nested-decoy JSON manifest | `audit2\AUDIT2_REPORT.md` (round-1 RED) | `audit3\AUDIT3_REPORT.md` (round-3 GREEN rerun) | LOCATED [refreshed 2026-08-12]. Auditor-executed fixture with actual rc/output. |
| Duplicate-key JSON manifest | `audit2\AUDIT2_REPORT.md` | `audit2\AUDIT2_REPORT.md` | LOCATED [refreshed 2026-08-12]. Auditor-executed fixture with actual rc/output. |
| Symlinked `/etc/mtc-bridge` parent | `audit2\AUDIT2_REPORT.md` | `audit3\AUDIT3_REPORT.md` (`conf_dir_is_symlink`, rc 1) | LOCATED [refreshed 2026-08-12]. |
| Name-mapped `root:root` ownership | `audit3\AUDIT3_REPORT.md` | `audit3\AUDIT3_REPORT.md` (`owner_numeric=1000:1000 expected=0:0`, rc 1) | LOCATED [refreshed 2026-08-12]. |
| Shared-path probe creates temporary files despite a no-mutation claim | No exact RED command/output mapping supplied | No exact GREEN mapping supplied | UNLOCATED [refreshed 2026-08-12]; supplemental only. |
| ENOENT at the conf-dir boundary | `audit3\AUDIT3_REPORT.md` | `audit3\AUDIT3_REPORT.md` (`conf_dir_search_permitted_name_absent`, rc 1) | LOCATED [refreshed 2026-08-12]. |
| Unguarded `tr` leaks a raw exit status outside the 0/1/3 contract | No exact RED command/output mapping supplied | No exact GREEN mapping supplied | UNLOCATED [refreshed 2026-08-12]; supplemental only. |
| PYTHONPATH/cwd `json` module hijack | `audit3\AUDIT3_REPORT.md` | `audit3\AUDIT3_REPORT.md` (`install_manifest_unparsable`, rc 3) | LOCATED [refreshed 2026-08-12]. |
| Non-finite `NaN` / `Infinity` accepted as JSON | `audit3\AUDIT3_REPORT.md` | `audit3\AUDIT3_REPORT.md` (`install_manifest_non_json_constant`, rc 3) | LOCATED [refreshed 2026-08-12]. |
| Unterminated final mount record silently skipped | `audit3\AUDIT3_REPORT.md` | `audit3\AUDIT3_REPORT.md` (`mount_table_unterminated_final_record`, rc 3) | LOCATED [refreshed 2026-08-12]. |
| Empty-nonzero-read mount source (directory) | `audit4\AUDIT4_REPORT.md` (round-3 false PASS rc 0) | `audit4\AUDIT4_REPORT.md` (round-4 `mount_table_read_error`, rc 3) | LOCATED [refreshed 2026-08-12]. |
| Ambiguous multiline EACCES+ENOENT diagnostic | `audit3\AUDIT3_REPORT.md` | `audit6\AUDIT6_REPORT.md` (`boundary_diagnostic_multiline`, rc 3) | LOCATED [refreshed 2026-08-12]. |
| Full round-6 QA arm set | `round6\SELF_QA.md` supplies the literal blocks and prior arms | `audit6\AUDIT6_REPORT.md` records the fresh unmodified rerun and vector `3,3,3,3,0,0,1,3,3,3,1` | LOCATED [refreshed 2026-08-12] as a paste-and-run reproduction; verify each named closure still maps to its own RED/GREEN pair. |
| RR2-1..4 from the earlier proposals-acceptance cycle | No exact per-row RED file is referenced in this unit | No exact per-row GREEN mapping is supplied | UNLOCATED [refreshed 2026-08-12]; supplemental only. |

## Current WP-I D026 map status

[refreshed 2026-08-12] The complete current-work D026 packet is
`NOT-YET-AVAILABLE`. The records below are partial sources, not a substitute for the final
per-test map.

| Artifact | Existing exact source(s) | What remains missing |
|---|---|---|
| RP6-P0 | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\SELF_QA_RP6.md`; `RP6_CODEX_T0_AUDIT_R16_2026-08-12.md` | [refreshed 2026-08-12] Consolidate every claimed closure across the current cycle to exact RED command/output, mutation or pre-fix identity, GREEN command/output, and finally dual-accepted bytes. The r16 report establishes the named final census closures but Claude current-byte acceptance is pending. |
| RP7-WPI-RO | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\SELF_QA_RP7.md`; `RP7_CODEX_T0_AUDIT_R9_2026-08-11.md` | [refreshed 2026-08-12] Codex records RED/GREEN for the five r8 findings, but current-byte Claude acceptance is pending and the owner-directed rows 1-9 do not yet exist. |
| Transport | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\SELF_QA_TRANSPORT.md`; `TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md` plus the cited earlier Codex round reports | [refreshed 2026-08-12] Consolidate each r4-r6 closure test against the final nine-file identity and append the pending Claude execution verdict. |
| SEC102 composite | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\SEC102_CODEX_T1_AUDIT_R8_2026-08-12.md`; `KICKOFF_SEC102_BUILD_R9.md` | [refreshed 2026-08-12] The r8 LF-to-CRLF byte-identity RED is located, but r9 repair, real GREEN, Codex r9 acceptance, and GLM second opinion are pending. |
| Pathscope prover | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\SELF_QA_PATHSCOPE.md`; `PATHSCOPE_R2_GLM_AUDIT_2026-08-11.md`; `KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md` | [refreshed 2026-08-12] Lead execution and GLM read review are supplemental for acceptance; the fresh flagship execution audit and final per-test bindings are pending. |
| Section 8.2 rows 1-9 | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-11.md` | [refreshed 2026-08-12] No implementation, RED/GREEN record, or accepted bytes exist. Build begins only after RP7 dual acceptance. |

## Non-substitutes

[refreshed 2026-08-12] Syntax checks, digest tables, PASS logs, RUNID ledgers, a
candidate filename, or a statement that a test passed do not by themselves demonstrate
that the regression test fails without the fix.
