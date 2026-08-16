# PHASE_WATCH — deployment Phase 1 / Phase 2 daily monitoring

> Owner request 2026-08-16: Phase 1 and Phase 2 of the post-deployment plan must be
> monitored daily. Any AI session doing daily work reads this file; a Hermes agent
> cron checks it every 4 hours (see "Hermes cron" below). Update the STATUS block
> whenever state changes. **Name the host in every status row**
> (see memory rule "two hosts, never conflate": GATEA-STAGING = local Hyper-V VM,
> retired staging; KVM2 = the real Hostinger VPS target).

## STATUS (machine-read by the Hermes cron wrapper — keep the exact `KEY: value` format)

WATCH_ACTIVE: NO
PHASE: 0-PRE-DEPLOY
HOST: KVM2 (install pending owner signature; payload uploaded, python3.12-venv installed, NOTHING else)
STATUS_SOURCE: see "STATUS_SOURCE map" section below (concrete read-only locations per check; access route TO FILL AT ACTIVATION)
LAST_HUMAN_UPDATE: 2026-08-16 (initial authoring)

Activation (owner ruling 2026-08-16 late evening): `WATCH_ACTIVE` stays `NO` until
the **deployment-owner session** (the other active Fable session — sole owner of
KVM2, deployment, credentials, ARM, TESTNET) confirms a successful DISARMED start.
Only after that confirmation does a Lead flip `WATCH_ACTIVE: YES`, set `PHASE: 1`,
and fill `STATUS_SOURCE` with the concrete places to look (bridge log path on KVM2,
dashboard/health endpoint, backup dir). Until then the cron logs "PENDING" and
spends no AI tokens. No other session may pre-activate the watch.

## Phase 1 — prove it breathes (first week after DISARMED start, cheap)

Bridge runs DISARMED on Hyperliquid TESTNET on KVM2 for 3–7 days. Daily checks
(each row must name the host = KVM2):

- [ ] Service alive: systemd unit active, no unexpected restarts since last check.
- [ ] Mode still DISARMED (never assume — read it).
- [ ] Logs rotating (no unbounded growth; note current size).
- [ ] Backup ran AND a restore drill has been proven at least once during the window.
- [ ] Memory/disk footprint small and flat (record numbers, compare to yesterday).
- [ ] Error scan: new ERROR/WARN lines in last 24 h — count + one-line triage.
- [ ] Dashboard reachable via the audited SSH-tunnel launcher (once Dashboard V2 lands, one glance = alive/version/DISARMED/equity/errors).

Phase-1 exit: 3–7 clean days recorded here → report to owner, ask to open Phase 2 gates.

## STATUS_SOURCE MAP — Phase 1 (concrete, read-only; from the accepted deploy package on master)

Facts source: `IBKR_PAPER_BRIDGE/deploy/linux/README.md` (target layout),
`logrotate/mtc-bridge`, `bridge/api/routes.py`. Unit = `mtc-bridge-first-start.service`
(`Restart=no`; the steady profile is a separately gated artifact). API binds
loopback only, `127.0.0.1:8790`. `<KVM2>` = read-only SSH alias the
deployment-owner session provides at activation — until then every KVM2 row is
SKIP, and nothing below may be executed against KVM2.

| # | Check | Read-only source | Exact command |
|---|---|---|---|
| 1 | Service alive | systemd unit state | `ssh <KVM2> "systemctl is-active mtc-bridge-first-start; systemctl status mtc-bridge-first-start --no-pager -n 0"` |
| 2 | DISARMED mode | `GET /api/status` on loopback | `ssh <KVM2> "curl -s http://127.0.0.1:8790/api/status"` — assert armed=false, TESTNET |
| 3 | Logs rotating | `/var/log/mtc-bridge/` + policy `/etc/logrotate.d/mtc-bridge` (daily, 30 kept, 64M early, copytruncate, dateext) | `ssh <KVM2> "ls -lh /var/log/mtc-bridge/; tail -3 /var/log/mtc-bridge/bridge.log"` — expect dated rotated files, sizes < 64M |
| 4 | Backup ran / restore drill | WAL-safe bundles from `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py`; backup dir per deployment plan — **fill at activation** | `ssh <KVM2> "ls -lh <backup-dir>"` — fresh bundle ≤ 24 h old; restore drill is a manual Lead/owner action recorded in the update log |
| 5 | Memory/disk flat | systemd accounting + df | `ssh <KVM2> "systemctl show mtc-bridge-first-start -p MemoryCurrent; df -h /var/lib/mtc-bridge /var/log/mtc-bridge"` |
| 6 | Error scan | `/var/log/mtc-bridge/bridge.err.log` + journal | `ssh <KVM2> "tail -50 /var/log/mtc-bridge/bridge.err.log"; ssh <KVM2> "journalctl -u mtc-bridge-first-start --since -24h -p warning --no-pager \| tail -20"` |
| 7 | Dashboard reachable | audited SSH-tunnel launcher `11_TRIAGE/KVM2_RUNKIT/Open-BridgeDashboard.ps1` (rp7 branch) → tunnel → `/api/status`, `/api/equity` | launcher (manual or Lead-run), then `curl -s http://127.0.0.1:<tunnel-port>/api/status` |

Hard limits for every row: read-only commands only; **never** read
`/etc/mtc-bridge/mtc-bridge.env` (secret contract file), never `sudo`, never
write/restart/unmask anything on KVM2. `deploy/linux/verify.sh` (full read-only
assertion pass, needs root) is a deployment-owner weekly action, not a watch task.

## STATUS_SOURCE map — Phase 1 (concrete read-only locations, owner-required 2026-08-16)

Sources derived from the accepted deploy package on `master`
(`IBKR_PAPER_BRIDGE/deploy/linux/` — systemd/logrotate/env templates, `COMMANDS.md`).
All commands are READ-ONLY. Host = KVM2 in every row.

| Phase-1 check | Concrete source | Exact read-only command / location |
|---|---|---|
| Service alive | systemd unit `mtc-bridge-first-start.service` (the steady restart profile is a GATED artifact, not installed) | `systemctl is-active mtc-bridge-first-start.service` · `systemctl show -p NRestarts --value mtc-bridge-first-start.service` (expect 0) |
| Mode DISARMED | loopback API, never public | `curl -s http://127.0.0.1:8790/api/status` → expect DISARMED + testnet (`COMMANDS.md` Stage F check) |
| Logs rotating | logrotate policy `/etc/logrotate.d/mtc-bridge` (daily, 30 gens, 64M early-rotate, dateext) | `ls -lh /var/log/mtc-bridge/` → dated rotated files appear, live `bridge.log` < 64M |
| Backup + restore drill | WAL-safe bundle tool (plain file copy of a live WAL DB is NOT a valid backup) | `python IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py create` / `... verify` against `/var/lib/mtc-bridge/bridge.db`; `verify` output = the restore-drill evidence. Backup destination dir: **TO FILL AT ACTIVATION** |
| Memory/disk flat | systemd accounting + filesystem | `systemctl show -p MemoryCurrent --value mtc-bridge-first-start.service` · `df -h /var/lib/mtc-bridge` · `du -sh /var/log/mtc-bridge` |
| Error scan | journal + stderr log | `journalctl -u mtc-bridge-first-start.service --since "24 hours ago" -p warning` · `tail -n 50 /var/log/mtc-bridge/bridge.err.log` |
| Dashboard reachable | audited SSH-tunnel launcher to loopback 8790 | `11_TRIAGE/KVM2_RUNKIT/Open-BridgeDashboard.ps1` (currently on branch `codex/rp7-r1-r4-repair-20260815`; path valid after its merge) |

Explicitly NOT a status source, never read by any watcher: `/etc/mtc-bridge/mtc-bridge.env`
(secret file, root 0600 — names-only contract; watching never touches it).

**Access route — TO FILL AT ACTIVATION by the deployment-owner session:** the SSH
host alias/user for the read-only checks above. Until the owner approves a read-only
access route for Hermes, the Hermes cron runs LOCAL-ONLY (reads this file and any
locally mirrored status the deployment session publishes); it never initiates a
KVM2 connection on its own and never handles credentials.

Parallel work item (already in the live queue, not a watch task): Dashboard V2
package — T1 for local read-only visual work, T0 for anything host/control.

## Phase 2 — TESTNET with keys (two owner-only gates)

Gates — NEVER performed or pre-filled by an AI (see safety fence below):
1. Barış types the TESTNET wallet key in himself.
2. Barış gives his separate ARM sentence — TESTNET only.

Then the 10-day observation plan, daily checks on KVM2 (adds to Phase-1 list):

- [ ] Trades sane: orders match strategy intent; no runaway loops; reduce-only SL/TP behave.
- [ ] Restart recovery: after any restart, position/order state reconciles against Hyperliquid (exchange = truth).
- [ ] Risk gates respected: daily-loss and size limits actually block when they should (record one observed instance or state "not triggered").
- [ ] Equity curve recorded daily; P&L drift vs expectation noted.
- [ ] WAL-safe backups continue; one restore drill during the window.

Phase-2 exit: 10 sane days → owner report. MAINNET stays forbidden — it needs a
promotable strategy (Phase 3, QuantLens research) and its own gate. No shortcut.

## Hermes cron (machine watch, every 4 h)

- Wrapper: `C:\LAB\HERMES_WATCH\phase_watch_check.ps1`, Windows scheduled task
  `MTC-HermesPhaseWatch`, every 4 hours.
- Reads this file's STATUS block. `WATCH_ACTIVE: NO` → appends one PENDING line to
  `C:\LAB\HERMES_WATCH\log\phase_watch.log` and exits (zero AI cost).
- `WATCH_ACTIVE: YES` → runs Hermes (`hermes -z … --provider deepseek -m deepseek-chat --cli`;
  verified 2026-08-16 — the default provider returns "no final response", DeepSeek works)
  against `STATUS_SOURCE`, appends a ≤10-line OK/WARN/FAIL report to the same log.
- Daily AI sessions: read the last ~6 log entries, escalate any WARN/FAIL into
  `NEXT_STEPS.md`, tick the day's boxes above.
- Hermes is read-only here: it never ARMs, never touches keys, never edits repo files.

## Safety fence

Watching only. Nothing in this file authorizes: install/start actions, ARM/KILL,
wallet or credential entry, TESTNET trading changes, MAINNET anything, config or
host changes. Wallet key entry and the ARM sentence are Barış-personal actions —
an AI must never type, store, or request the actual key material.

## Update log

| Date | Who | Change |
|------|-----|--------|
| 2026-08-16 | Fable Lead | File created; WATCH_ACTIVE NO; Hermes cron installed. |
