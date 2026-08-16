# Phase Watch — Telegram notifier DESIGN (prepared, NOT deployed)

**STATUS: DEPLOYMENT HELD by owner ruling (2026-08-16, after the initial approval)
— T0 REVIEW REQUIRED BEFORE ACTIVATION.** The owner classified the active Hermes
watcher plus the Telegram credential/network handling as **T0** and required the
tier-mandated review to complete before the notifier goes live. §6.1 code exists in
`C:\LAB\HERMES_WATCH\phase_watch_check.ps1` but is dormant (no credentials stored;
credentials absent → clean `NOTIFY-SKIP`, watch unaffected; PENDING → zero
notifications — both verified). **Credential entry REDESIGNED per the same ruling:**
the original §3 `cmdkey` commands are WITHDRAWN (they place the token on a command
line and in shell history). Two compliant routes now exist, to be finalized in the
T0 review: (a) **reuse the existing owner-managed USER environment variables**
`TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` of the existing @MTCHyperbot (per the owner
directive recorded in the wrapper header — no new entry, token never re-typed
anywhere; messages prefixed `[PHASE WATCH][KVM2]` to stay distinguishable); or
(b) a dedicated credential entered via the interactive helper
`C:\LAB\HERMES_WATCH\Set-TelegramCredentials.ps1` (hidden `Read-Host
-AsSecureString` prompts → advapi32 CredWrite; accepts no arguments by design).
Either way the token can never appear in a command line, history, log, or the repo.

**UPDATE 2026-08-16 late night — route (a) FINALIZED and implemented by explicit
owner directive** ("Reuse the existing MTC_Telegram bot @MTCHyperbot … existing
owner-managed user environment variables TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID"):
`Send-WatchAlert` now reads those two USER env vars at runtime (User scope with
process fallback), the CredRead Add-Type block was removed, and every message is
prefixed `[PHASE WATCH][KVM2]`. The route mismatch (former T0-review finding 6) is
therefore RESOLVED in code; the review verifies rather than picks. Values were
never displayed, copied, rotated, deleted, or logged; presence had been verified by
the owner without reading values. Helper route (b) stays unused; the helper file
remains for review reference only. **§6.3 supervised test EXECUTED on the same
owner directive: exactly one fake-WARN run at 23:48:18 → `NOTIFY-SENT` attempt 1 —
one TEST-labelled, `[PHASE WATCH][KVM2]`-prefixed message via @MTCHyperbot; only
api.telegram.org contacted, no KVM2 endpoint touched, `WATCH_ACTIVE: NO`
unchanged.** This is recorded as review evidence, not as deployment.
Pre-review hardening already applied: `NOTIFY-FAIL` log line masks the token if an
exception message embeds the request URI. T0 review record:
`PHASE_WATCH_NOTIFIER_T0_REVIEW_PENDING_2026-08-16.md`. Order now: T0 review →
activation preconditions (PHASE_WATCH.md) → activation. Automatic alerting on real
runs stays structurally unreachable until then (active runs require activation,
which requires the accepting T0 pair). Scheduled task, KVM2: untouched.

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

> **WITHDRAWN (owner ruling 2026-08-16):** the original `cmdkey /pass:<token>`
> commands are forbidden — they put the token on the command line and into shell
> history. Use the interactive helper instead:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\LAB\HERMES_WATCH\Set-TelegramCredentials.ps1
```

The helper takes no arguments (refuses any), prompts twice with hidden input
(`Read-Host -AsSecureString`), writes both values straight into Credential Manager
via advapi32 `CredWrite`, zeroes the in-memory copies, and never echoes or logs a
value. Deleting later by name (`cmdkey /delete:MTC-TG-BOT-TOKEN`) is fine — a
delete carries no secret.

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
