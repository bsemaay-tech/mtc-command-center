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
STATUS_SOURCE: (none yet — fill with log path / health URL / SSH command after first DISARMED start)
LAST_HUMAN_UPDATE: 2026-08-16 (initial authoring)

Activation: after the KVM2 install + separate first-start sentence are executed
(live queue steps in `NEXT_STEPS.md`), the Lead flips `WATCH_ACTIVE: YES`, sets
`PHASE: 1`, and fills `STATUS_SOURCE` with the concrete places to look
(bridge log path on KVM2, dashboard/health endpoint, backup dir). Until then the
cron logs "PENDING" and spends no AI tokens.

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
