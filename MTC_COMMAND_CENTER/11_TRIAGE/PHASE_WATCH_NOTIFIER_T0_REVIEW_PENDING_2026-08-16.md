# Phase-watch active watcher + Telegram notifier — T0 REVIEW PENDING

**Classification (owner, 2026-08-16 late evening): T0** — the ACTIVE Hermes watcher
and the Telegram credential/network handling. Rationale: credential handling plus a
new outbound network channel adjacent to trading-host monitoring is a T0 surface
under the permanent audit-tier policy (`AGENTS.md` §AUDIT TIER POLICY).

**Consequence:** the notifier stays DORMANT (no credentials stored, `NOTIFY-SKIP`
path verified) and the watch stays `WATCH_ACTIVE: NO` until BOTH of the following
complete, in order:

1. **T0 review** of the surfaces below by the two flagship auditors
   (`claude-opus-5` xhigh + `gpt-5.6-sol` xhigh), per the canonical roster.
2. The existing activation preconditions in `_AI_MEMORY/PHASE_WATCH.md`
   (deployment-owner DISARMED-start confirmation, access alias, backup dir,
   separately authorized bounded read-only live check).

## Review scope (exact artifacts, all outside the repo — reviewers get copies)

| Artifact | What it does |
|---|---|
| `C:\LAB\HERMES_WATCH\phase_watch_check.ps1` | 4-hour cron wrapper (binding-spec rewrite 2026-08-16 ~23:52): checklist snapshot from `origin/master`, PENDING gate, Hermes (DeepSeek) invocation, `Send-WatchAlert` (existing USER env vars `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`, presence-check only → Telegram sendMessage, fixed `[PHASE WATCH][KVM2]` prefix), generic-status-only failure logs (no exception text, no URI), daily-summary dedup, `-TestReport` / `-FakeWarnTest` (single attempt, `[TEST]` prefix, before/after `WATCH_ACTIVE: NO` assertions) |
| `C:\LAB\HERMES_WATCH\Set-TelegramCredentials.ps1` | WITHDRAWN inert stub (prints the binding directive, exits 1) — no Credential Manager entries can be created; kept only so the withdrawal is auditable |
| Scheduled task `MTC-HermesPhaseWatch` | Interactive-user task, every 4 h |

## Known findings for the reviewers (Lead-identified, to be independently re-checked)

1. **Token-in-URI exception leak (superseded by stronger fix):** the Bot API URL
   embeds the token; a thrown `Invoke-RestMethod` exception can carry the URI. The
   earlier token-mask was REPLACED (binding-spec rewrite): `NOTIFY-FAIL` now logs
   only exception TYPE name + HTTP status code — never exception message, URI, or
   `ErrorDetails`. Verify no other code path (transcripts, `$Error`, -Verbose
   streams) can persist the raw exception.
2. **Message content fencing:** alert text is built from `CHECK/SUMMARY/TEST` status
   lines only (`Get-StatusLines`); verify no path lets raw Hermes output or env
   values into a message.
3. **P/Invoke surface — ELIMINATED:** both Add-Type blocks are gone (CredRead
   removed with the env-var route; the CredWrite helper is an inert stub). Verify
   nothing reintroduces them.
4. **Daily-summary log parsing:** regex over the log for WARN/FAIL counting —
   verify a crafted log line cannot suppress or force a summary.
5. **Self-confirming-check discipline:** every check must fail loudly on empty
   output (see the 2026-08-16 zombie-worktree false-PASS instance in session
   memory) — verify the wrapper's git/Hermes failure paths distinguish
   "no output" from "OK".
6. **Header/code credential-route mismatch — RESOLVED IN CODE 2026-08-16 late
   night by explicit owner directive, review now verifies:** `Send-WatchAlert`
   reads the existing @MTCHyperbot USER env vars
   (`TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`; User scope, process fallback), the
   CredRead Add-Type block was removed, every message carries the fixed
   `[PHASE WATCH][KVM2]` prefix. Reviewers: verify the env-var route does not leak
   values into child-process environments (note: the wrapper spawns hermes.exe,
   which inherits process env — assess) or logs, and that the prefix cannot be
   omitted on any send path.

**Timeline note for reviewers:** on the same owner directive, exactly one
supervised `-FakeWarnTest` run was executed 2026-08-16 23:48:18 → `NOTIFY-SENT`
attempt 1 (one TEST-labelled message, no KVM2 contact, `WATCH_ACTIVE: NO`
unchanged). Owner-ordered bounded test, recorded as evidence — not deployment;
automatic alerting remains unreachable until activation, which requires this
review's accepting pair. The `Set-TelegramCredentials.ps1` helper is now an
INERT WITHDRAWN stub under the finalized env-var route (no new bot, no new
Credential Manager entries — binding owner instruction).

## Explicitly out of scope

KVM2, deployment, bridge credentials, ARM, TESTNET, trading — untouched by this
review and by the notifier itself (one-way outbound messages only).

**Status: review NOT yet dispatched.** Dispatch is the next Lead action after owner
confirms sequencing; no activation before an accepting T0 verdict pair.
