# DISPOSITION_P26FIX — GROK detection audit findings

Audit: `C:/tmp/CLAUDE_P0_RUN_20260913/laneGKP26_grok_audit/GROK_AUDIT_REPORT.md`.
Lane: P26FIX · grok-4.6 · text edits only inside `C:/tmp/P026_PREP_20260913/`.

| # | severity | FIXED / REBUTTED | what changed (file:line) or the exact refuting source quote |
|---|---|---|---|
| 1 | CORRECTION | FIXED | `BACKUP_COMPLETION_REPAIR_DESIGN.md:5`, `:246`, `:370` — O-9 pin `P030_P026_CONFIG_DRILL_CHOICES_V3.md:587` retargeted to `:586`. Source `:586` is O-9 ("An **implementation scope** for the producer/exporter bridge of §4.1"); `:587` is O-10 ("Records hygiene: should the P021/P030 owner answers … be added to `DECISIONS.md`?"). |
| 2 | CORRECTION | FIXED | `BACKUP_COMPLETION_REPAIR_DESIGN.md:323`; `DEPLOY_RESTORE_ALERT_PACKET.md:38` — D-13 RED-only fence pin `:445, 557` retargeted to `:445, 550`. Source `:445` still fences GREEN behind O-9; `:550` is "its GREEN half needs O-9"; `:557` is `[notifier scope, local stub only] NtfyNotifier-shaped class + unit tests (O-8)`. |
| 3 | CORRECTION | FIXED | `BACKUP_COMPLETION_REPAIR_DESIGN.md:219` — dropped `check_market_data_collector.py:27` as a hit for `p030_market_data_contracts` / the backup adapter. That line is `import market_data_collector as subject`. Remaining hits: adapter check `:15`, contracts check `:579/675/732`. Heartbeat-adapter check `:12` labelled as importing `p030_opsa_heartbeat_adapter` (a third name). |
| 4 | CORRECTION | FIXED | `DEPLOY_RESTORE_ALERT_PACKET.md:38` (P-2) — D-8, D-9, D-10 taken off the after-P-1 list and placed on V3's parallel T-A branch (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:476-489`: `D-8 heartbeat ── D-9 watchdog matrix ── D-10 recovery ledger`). After P-1 remains D-13 GREEN, D-3, D-3b, D-4, D-5, D-6, D-7. Matches `BACKUP_COMPLETION_REPAIR_DESIGN.md:360`. |
| 5 | CORRECTION | FIXED | `P030_INTERFACE_COORDINATION_NOTE.md:174` — T11 no longer claims config-byte re-read after every P026 call. `_bound_strict_config` (`p030_closed_partition_backup_adapter.py:410-436`) copies/validates before `yield` with no `finally` re-read; post-`backup.run_backup` compare is receipt/snapshot bytes (`:651-660`); isolated-restore config `finally` re-verify is `:439-466` only. |
| 6 | NIT | FIXED | `REPORT.md:37-48, 54` — whole-file `(1-N)` last-line counts reduced by 1 to match EOF: collector 542, contracts 470, adapter 816, heartbeat-adapter 174, watchdog 296, backup 219, restore 238, heartbeat 112, `opsa_common` 245, README 110, `config.example.json` 16, `NOTIFIER_PROPOSAL.md` 96. Left unchanged: `p030_opsa_backup_config.json` (1-11) exact; `LANE_REPORT.md` (1-320+) last line 320. |
| 7 | NIT | FIXED | `DEPLOY_RESTORE_ALERT_PACKET.md:103` — S-B3 evidence pin `:88` retargeted. `RESTORE_DRILL_EVIDENCE.md:15-16` remains the D026 RED/GREEN statement; `:88` is heading `### A3. RED — deliberate damage…`; command block is `:93-98`. NV-P7 / NV-I6 / NV-R11 not shrunk. |
| 8 | NIT | FIXED | `DEPLOY_RESTORE_ALERT_PACKET.md:58` — S-A3 evidence artefact now records that `REPORT.md`'s ten-file table omits `opsa_common.py` (`backup.py:37-39` `from opsa_common import`) and omits README / `config.example.json`. Copy step still places the tree; hash list not expanded (no new numbers). |
| 9 | NIT | FIXED | `BACKUP_COMPLETION_REPAIR_DESIGN.md:315` — heading `**Owner decision (O-9), with recommended answer:**` reworded to `**Recommended answer to owner item O-9 (not in force until the owner answers):**`. Surrounding hedges at `:4`, `:305`, `:401` unchanged. |

## Tally

| result | n |
|---|---|
| FIXED | 9 |
| REBUTTED | 0 |
| BLOCKING | 0 |

9 findings · 9 FIXED · 0 REBUTTED
