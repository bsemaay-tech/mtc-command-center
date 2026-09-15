# WP-P0-26 (OPS-A) — deployment-and-drill decision packet, draft 1 (2026-09-15)

Prepared by the Claude Opus 5 Lead (session 743291) on the owner's 2026-09-12 queue decision (`20260912-214745-p026-queued-for-existing-lead.md`, item 3). Facts were refreshed today; host-side facts are marked UNKNOWN because no host contact (G9) is authorized by this packet. Nothing here installs, schedules, sends, deletes or accepts.

## 0. State refreshed at pickup
- Master `fcac0ac6` carries the OPS-A local half (`MTC_COMMAND_CENTER/tools/opsa/`: `backup.py`, `restore.py`, `heartbeat.py`, `watchdog.py`, `opsa_common.py`, `test_opsa.py`, `config.example.json`; delivered 2026-08-25, T1 partial; no delete code path; append-only `manifest.jsonl`; only the `local_log` notifier). The watchdog repair `53d33dbc` is in.
- **The bounded repair the owner accepted on 2026-09-12 (scope packet `C:/tmp/P026_LOCAL_SCOPE_DECISION_20260907.md` §2-§5) is still ABSENT:** `backup.py` writes no per-run `RUN_MANIFEST.jsonl` + `COMPLETE.json`; `restore.py` still selects by manifest run without a completion marker (and still offers `--latest`). **Correction on re-read:** the watchdog half of the packet (explicit silence bound, no 900-second default, alert → recovery → alert transition ledger, corrupt-state fail-safe) already landed in `53d33dbc` with its three tests — only `backup.py` / `restore.py` / `opsa_common.py` (+ tests) remain. Builder: the owner answered "A" at ~08:34Z (`OD-20260915-P026-REPAIR-LEAD-1`) — the Lead builds it today.
- P0-30 overlap is closed: the P030 batch (PR #187, 2026-09-13) delivered the OPSA backup heartbeat/closed-partition backup adapters (`check_p030_closed_partition_backup_adapter.py`, `check_p030_opsa_heartbeat_adapter.py`, both green locally); the exporter candidate `daf6a43b` (2026-09-14) writes canonical partitions the backup adapter consumes. No duplicate adapter is needed; the P0-26 repair must keep those adapters' interfaces (run directory layout, manifest records) unchanged — the P0-30 Lead lane is this session, so ownership is not contested.

## 1. Evidence-store inventory (measured on the owner PC, 2026-09-15; host side UNKNOWN)
| Store | Location | Class (plan §12.6.2(b)) | Size | Second copy today |
|---|---|---|---|---|
| Governance records (CT13 takeover records, DECISIONS, handoffs) | `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/` (git) | text / protected | 4.7 MB | **GitHub** (branch pushed; `98d67348`) ✔ |
| P0 run root (lane briefs, launcher logs, review adjudications, Path 1 capture r1, derived plan) | `C:/tmp/CLAUDE_P0_RUN_20260913/` | protected (evidence + audit logs) | 61 MB | **none** (copies of the accepted parts live in CT13; the rest only here) ✖ |
| Gemini review roots (prompts, raw REVIEW.log, native-read verifications) | `C:/tmp/P012_S16_REVIEWS_20260913/` | protected (audit logs) | 4.2 MB | none ✖ |
| Gemini packets (frozen review inputs) | `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/` (untracked in git) | reproducible from git + records | 26 MB | none (reproducible) |
| P020 frozen preselection package + one-shot outputs | `C:/tmp/P020_PRESELECT_20260913/` | protected (frozen artifact + one-shot records) | 1.8 MB | digests in CT13; bytes only here ✖ |
| P020 benchmark dir (plan, driver, records) | `C:/tmp/P020_LEAD_20260912/` | protected | 18 MB | git worktree (branch pushed?) — verify |
| P020 derived datasets (93 CSVs + manifest) | `C:/tmp/P020_DERIVED_20260912/` | bulk (reproducible from the frozen recipe) | 249 MB | none |
| Package worktrees (P012/P020/P031/P030/P1CAP…) | `C:/tmp/*`, `C:/P020_IMPL_20260912` | git (branches pushed) | — | GitHub for committed state; lane files untracked |
| Bridge runtime stores on KVM2 (WAL state, order ledger, admission records) | KVM2-P4-03 (`be007fd8` deployed DISARMED; TESTNET provisioned 2026-09-14) | protected | **UNKNOWN** (G9) | **UNKNOWN** ✖ |
| Owner wallet / venue evidence | venue + owner's browser; captured bytes in CT13 | protected | — | CT13/GitHub ✔ |
**Consistent-snapshot method proposed:** for git-tracked stores the pushed commit IS the snapshot; for the run/review roots (`C:/tmp/...`) a `backup.py` run over the listed paths (read-only copy + hash + append-only manifest) into the backup root, with the P0-26 repair's `COMPLETE.json` marking each run; for the KVM2 stores, the P0-30 closed-partition backup adapter + the same `backup.py` from the host (G9 step).

## 2. Decisions the owner will be asked to make (after the repair lands; not now)
| # | Decision | Options prepared | Measured value still missing |
|---|---|---|---|
| D-A | Backup locations: owner PC ↔ VPS cross-copy (plan) | (A1) owner PC backup root on a second physical drive + KVM2 as the cross copy; (A2) owner PC + a second cloud object store (not in the plan; needs a decision) | free space on the owner PC drives and on KVM2 (UNKNOWN); daily delta size (measure with one dry run of `backup.py`) |
| D-B | External dead-man checker location (must be OUTSIDE the watched host) | (B1) owner PC checks KVM2 heartbeats; (B2) a free cron host — **GitHub Actions `schedule:` is NOT available**: WP-P0-27's non-goal excludes scheduled jobs and its ruleset would need a plan amendment; listed only so the exclusion is explicit; (B3) the phone channel provider's own uptime monitor | detect-to-delivery elapsed time on the real channel (the `[OPEN]` bound the owner must ratify from a measurement, never from a default) |
| D-C | Phone channel | (C1) Telegram bot (the Bridge already has `bridge.engine.notify` with Telegram credential resolution — reuse; no key in repo); (C2) e-mail-to-SMS; (C3) a push app | one measured end-to-end push from a killed heartbeat (the plan's acceptance test) |
| D-D | Schedules | daily all-store + hourly critical-ledger sync during active windows (ratified cadence, unchanged) — the owner only confirms the clock hours of "active windows" | none |
| D-E | Restore / reconciliation procedure | explicit-run restore into a scratch dir, byte-hash verify, then a reconciliation read (P0-12 style) against the live store — never in place | the RED/GREEN drill on a copy (after the repair) |
| D-F | Deletions | none by tooling; owner-approved exact list only (unchanged) | — |

## 3. Drill plan (executed only after the repair and under the usual gates)
1. **Restore drill RED/GREEN (D026):** copy of a protected store → damage one file in the copy → `restore.py <run-id>` must refuse the damaged run (no `COMPLETE.json`/hash mismatch) → restore from the backed-up run → byte-identical (hashes). Fixture-only in the repair's tests; the real drill runs on a copy of the run root, never on a live store.
2. **Dead-man drill:** `heartbeat.py --loop` on the watched process → kill it → external `watchdog.py` (location per D-B) detects silence → notifier delivers the push (channel per D-C) → **measure detect-to-delivery** → put the number to the owner for ratification of the bound.
3. Both drills are recorded like every other evidence (commands, cwd, outputs, hashes) and reviewed T1; the KVM2 step is T0/G9 per session.

## 4. What this packet does NOT do
No host contact, credentials, deployment, phone send, schedule creation, deletion, or acceptance. The forward clocks (paper/TESTNET timing) stay gated on P0-26 acceptance as before.

## 5. Next action
Owner answered "A" (~08:34Z): the Lead builds the accepted repair today (record in `P026_REPAIR_20260915/`). Then the measurements in §2 and the drills in §3, one G9 step at a time, each on its own owner word.
