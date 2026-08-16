# Phase Watch — Telegram notifier DESIGN (prepared, NOT deployed)

**STATUS: DESIGN ONLY — owner requested 2026-08-16 late evening. Nothing installed,
no wrapper change, no scheduled-task change, no bot created, no credential touched.
Deployment requires explicit owner approval of §6.**

## 1. Current state (verified 2026-08-16)

The Hermes Phase Watch (`C:\LAB\HERMES_WATCH\phase_watch_check.ps1`, scheduled task
`MTC-HermesPhaseWatch`, every 4 h) writes ONLY local files:
`C:\LAB\HERMES_WATCH\log\phase_watch.log` and the checklist snapshot
`PHASE_WATCH.current.md`. It has **no notification channel** — a WARN/FAIL sits in
the local log until someone reads it. Network use today: `git fetch` (repo remote)
and the DeepSeek call inside Hermes when active. Nothing else.

## 2. Requirements (owner, 2026-08-16)

1. Immediate Telegram message on WARN or FAIL.
2. Exactly one daily OK summary when everything is green.
3. Never message on PENDING (watch inactive).
4. No secrets in messages and no secrets in the repo.
5. Credentials owner-managed, outside Git.
6. Prepare only; approval required before installing or changing anything.

## 3. Design

**Transport:** plain Telegram Bot API `sendMessage` over HTTPS from PowerShell
(`Invoke-RestMethod https://api.telegram.org/bot<token>/sendMessage`). No new
software. (Alternative considered: `hermes send` via the Hermes Telegram gateway —
works, but adds a running gateway + Hermes config as moving parts between an alarm
and the owner's phone; rejected for the alarm path. Can be revisited later.)

**Hook point:** a small `Send-WatchAlert` function inside the existing wrapper,
called only after a completed Hermes run:

- Run report contains `FAIL` or `WARN` (or the run itself errored/timed out) →
  send immediately. Message = status lines only (the `CHECK <name> - OK|WARN|FAIL`
  lines + `SUMMARY`), host-labelled `KVM2`, max ~15 lines. Raw tool output, paths
  under `/etc/mtc-bridge/`, env values, tokens: never included — the message is
  built exclusively from the check-status lines, which contain no secret material
  by construction.
- All checks OK → no immediate message; the run appends to the local log only.
- Daily summary: the first run after 07:00 local also sends
  `Phase watch KVM2 — last 24 h: N runs, all OK` when the last 24 h contain no
  WARN/FAIL (dedup guard: a `last_summary_date` stamp file in `C:\LAB\HERMES_WATCH\`).
  No extra scheduled task needed — reuses the 4-hour cadence.
- `PENDING` (WATCH_ACTIVE: NO) → never a message, unchanged zero-cost exit.
- Telegram send failure → logged locally (`NOTIFY-FAIL` line), never blocks or
  retries aggressively (one retry after 30 s, then give up until next run).

**Credentials (owner-managed, outside Git):** Windows Credential Manager, the same
mechanism the GLM audit route already uses. Barış creates the bot with BotFather in
his own Telegram, obtains his chat id, then runs himself (AI never sees or types
the token — same rule as every other credential here):

```bash
cmdkey /generic:MTC-TG-BOT-TOKEN /user:bot /pass:<token-from-BotFather>
```

```bash
cmdkey /generic:MTC-TG-CHAT-ID /user:chat /pass:<numeric-chat-id>
```

The wrapper reads both at runtime (same read technique as `glm.ps1`), keeps them in
process memory only, never logs them, never echoes them. Nothing credential-shaped
enters the repo; this design doc contains names, not values. Fallback if Credential
Manager read proves brittle: owner-created `%LOCALAPPDATA%\MTC_PHASE_WATCH\telegram.env`
(outside Git, plain NTFS user-only ACL) — decision at deploy time.

## 4. Windows or KVM2?

**Recommendation: Windows (this PC), clearly.**

1. The watcher, its log, and Hermes already run on Windows — the notifier should
   observe the observer, one hop, same host.
2. KVM2 must stay minimal and hardened: adding a Telegram bot token + new outbound
   channel + a script to the trading host is exactly the kind of surface the
   deployment governance (T0, owner-gated) exists to prevent. A notifier there
   would itself need a T0 review.
3. The failure we most want to hear about is "KVM2 unreachable / bridge dead" — a
   KVM2-hosted notifier cannot report its own host being down. The Windows side
   sees that as a failed check and alerts.

Honest weakness: if this PC is off or asleep, there is no watch and no alert.
Mitigation available today: absence of the daily OK summary is itself a signal.
A proper dead-man's-switch (KVM2-side heartbeat the phone notices going quiet)
is future Dashboard-V2/V2+ territory, owner-gated, not part of this design.

## 5. Explicitly out of scope

No KVM2 changes, no ARM/credential/TESTNET interaction, no repo secrets, no new
always-on process (the notifier lives inside the existing 4-hour task), no
Telegram *commands* into the system — one-way outbound messages only; the bot
never accepts input that changes anything.

## 6. What deployment would change (the approval ask)

1. Edit `C:\LAB\HERMES_WATCH\phase_watch_check.ps1`: add `Send-WatchAlert` +
   daily-summary stamp logic (local file outside repo).
2. Barış creates the bot and stores the two Credential Manager entries himself
   (§3 commands).
3. One supervised test: a deliberate fake-WARN run must produce exactly one
   Telegram message; a green run must produce none; a PENDING run must produce none.
4. No other change. Scheduled task, PHASE_WATCH.md, KVM2: untouched.

**OWNER ASK (plain language):** may I make change §6.1 and run test §6.3 after you
do §6.2? Answer "approve telegram notifier" (or say what to change). Until then,
nothing is installed.
