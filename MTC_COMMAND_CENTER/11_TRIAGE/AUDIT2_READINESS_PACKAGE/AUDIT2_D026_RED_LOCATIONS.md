# Audit 2 D026 RED locations

Status: index only. This document does not decide whether a defect is closed. It reports
only whether the permitted kickoff inputs identify an exact RED location.

Rule for dispatch: a test without a located RED command and real output is supplemental,
not closure evidence. A candidate filename without a per-test mapping is not a located RED.

## Location register

| Closure test or falsification named by the permitted records | RED location | GREEN location | Package classification and auditor action |
|---|---|---|---|
| R4-5 symlink-guard deletion: delete the two-line `dst_path.is_symlink()` guard and show a real SQLite database written outside the restore root | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\05_TRANSPORT_R45B\STAGE3B_TRANSPORT_RECORD.md` | Same record; accepted bytes must raise `restore destination is a symlink` and leave the target absent. Supporting log: `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\05_TRANSPORT_R45B\operator_record\evidence\WPLP2-20260809T125940Z-8dc78f08-R45B\r45b.log` | LOCATED in the permitted inputs. Auditor must rerun both arms, confirm the mutation is the unique file-wide delta, and compare real output and side effects. |
| B3 original environment-file admission versus repaired EACCES boundary | Candidate prior-behavior record: `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\03_TRANSPORT\B3_STOP_ADJUDICATION.md`; however, the permitted inputs do not explicitly designate it as the D026 RED for the repaired test. | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\09_TRANSPORT_B3B\STAGE3B_B3B_RECORD.md` | UNLOCATED as a D026 pair. Treat as supplemental unless the dispatcher supplies an exact mapping with RED command/output and the auditor reproduces RED and GREEN. |
| Nested-decoy JSON manifest falsification | No exact RED location recorded in the permitted inputs. Candidate files are indexed under `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\`, but no test-to-file mapping is given. | No exact GREEN location recorded. | UNLOCATED; supplemental only. Auditor must be given and reproduce the exact mutation, command, RED output, accepted bytes, and GREEN output. |
| Duplicate-key JSON manifest falsification | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |
| Symlinked `/etc/mtc-bridge` parent falsification | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |
| Name-based `root:root` ownership spoof through NSS mapping | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |
| Shared-path probe creates temporary files despite a no-mutation claim | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |
| ENOENT misrouted to STOP instead of the recorded deviation result | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |
| Unguarded `tr` leaks a raw exit status outside the 0/1/3 contract | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |
| PYTHONPATH-shadowed `json` module returns a false bound result | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |
| Non-finite `NaN` accepted as JSON | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |
| Unterminated final mount record silently skipped | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |
| Ambiguous two-line diagnostic selects the pass arm | No exact RED location recorded; same candidate directory as above. | No exact GREEN location recorded. | UNLOCATED; supplemental only. |

## Indexed candidate containers that were not read

The evidence index lists these possible containers but does not map any named test to an
exact RED command/output location:

- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\audit1\AUDIT1_REPORT.md`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\audit2\AUDIT2_REPORT.md`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\audit3\AUDIT3_REPORT.md`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\audit4\AUDIT4_REPORT.md`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\audit5\AUDIT5_REPORT.md`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\audit6\AUDIT6_REPORT.md`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\round1\SELF_QA.md` through `round6\SELF_QA.md`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\06_B3_REPAIR\B3_REPAIR_CYCLE_RECORD.md`

Per the kickoff, the audit reports themselves were not read for this assembly. Before
dispatch, either provide a verified per-test mapping into these files or keep every
unlocated test explicitly supplemental.

## Records that are not D026 RED demonstrations by themselves

Syntax-validation files, block-digest tables, PASS transport logs, RUNID ledgers, and a
report that a test passed are useful evidence, but none alone demonstrates that a regression
test failed without the fix. They must not be substituted for a RED record.

---

## Lead correction (2026-08-10) — several "no location recorded" entries DO have located REDs

The assembling agent was deliberately given a narrow input set that EXCLUDED the audit
reports, so it could index without re-adjudicating. That scoping means some entries above
say "no exact RED location recorded in the permitted inputs" when the RED demonstration
does in fact exist, reproduced by an independent auditor with real command output. Treating
those as supplemental would understate the evidence.

The B3 repair-cycle falsifications live in the audit reports under
`WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/06_B3_REPAIR/`:

| Falsification | RED/GREEN location | Nature of the record |
|---|---|---|
| Nested-decoy JSON manifest | `audit2/AUDIT2_REPORT.md` (round-1 RED) and `audit3/AUDIT3_REPORT.md` (round-3 GREEN rerun) | auditor-executed fixture, actual rc and output quoted |
| Duplicate-key JSON manifest | `audit2/AUDIT2_REPORT.md` | same |
| Symlinked `/etc/mtc-bridge` parent | `audit2/AUDIT2_REPORT.md` RED, `audit3/AUDIT3_REPORT.md` GREEN (`conf_dir_is_symlink`, rc 1) | same |
| Name-mapped `root:root` ownership | `audit3/AUDIT3_REPORT.md` (`owner_numeric=1000:1000 expected=0:0`, rc 1) | same |
| PYTHONPATH / cwd `json` module hijack | `audit3/AUDIT3_REPORT.md` (`install_manifest_unparsable`, rc 3) | same |
| `NaN` / `Infinity` accepted as JSON | `audit3/AUDIT3_REPORT.md` (`install_manifest_non_json_constant`, rc 3) | same |
| Unterminated final mount record | `audit3/AUDIT3_REPORT.md` (`mount_table_unterminated_final_record`, rc 3) | same |
| Empty-nonzero-read mount source (directory) | `audit4/AUDIT4_REPORT.md` — round-3 RED rc 0 false pass vs round-4 GREEN `mount_table_read_error` rc 3, both blocks | same |
| Ambiguous two-line EACCES+ENOENT diagnostic | `audit3/AUDIT3_REPORT.md` and `audit6/AUDIT6_REPORT.md` (`boundary_diagnostic_multiline`, rc 3) | same |
| ENOENT at the conf-dir boundary | `audit3/AUDIT3_REPORT.md` (`conf_dir_search_permitted_name_absent`, rc 1) | same |
| Full QA arm set, round 6 | `round6/SELF_QA.md`, re-run verbatim by the auditor in `audit6/AUDIT6_REPORT.md` | paste-and-run reproduction, zero edits |

The strongest single item: `audit6/AUDIT6_REPORT.md` records the auditor pasting the QA
prerequisite and four closure blocks into a fresh shell unmodified, with the eleven-arm
result vector `3,3,3,3,0,0,1,3,3,3,1` matching the recorded table exactly.

**What remains genuinely unlocated** is unchanged by this correction: the RR2-1..4 rows from
the earlier proposals-acceptance cycle, whose RED demonstrations are not referenced by file
anywhere in this unit. Those are still supplemental, not closure, and the auditor must be
told so — see the rows above that this note does not supersede.
