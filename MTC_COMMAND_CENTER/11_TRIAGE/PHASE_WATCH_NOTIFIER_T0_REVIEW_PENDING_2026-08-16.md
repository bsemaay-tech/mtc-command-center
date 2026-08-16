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
| `C:\LAB\HERMES_WATCH\phase_watch_check.ps1` | 4-hour cron wrapper: checklist snapshot from `origin/master`, PENDING gate, Hermes (DeepSeek) invocation, `Send-WatchAlert` (CredRead → Telegram sendMessage), daily-summary dedup, `-TestReport` / `-FakeWarnTest` switches |
| `C:\LAB\HERMES_WATCH\Set-TelegramCredentials.ps1` | Interactive-only credential entry: no arguments accepted, hidden `Read-Host -AsSecureString`, advapi32 `CredWrite`, in-memory zeroing |
| Scheduled task `MTC-HermesPhaseWatch` | Interactive-user task, every 4 h |

## Known findings for the reviewers (Lead-identified, to be independently re-checked)

1. **Token-in-URI exception leak (pre-review fix applied):** the Bot API URL embeds
   the token; a thrown `Invoke-RestMethod` exception can carry the URI into the
   `NOTIFY-FAIL` log line. A mask (`-replace` token → `<token>`) was applied
   2026-08-16 before this review — verify it covers all exception shapes
   (inner exceptions, `ErrorDetails`).
2. **Message content fencing:** alert text is built from `CHECK/SUMMARY/TEST` status
   lines only (`Get-StatusLines`); verify no path lets raw Hermes output or env
   values into a message.
3. **P/Invoke surface:** two Add-Type blocks (CredRead in the wrapper, CredWrite in
   the helper) — verify blob size arithmetic, zeroing, and failure paths.
4. **Daily-summary log parsing:** regex over the log for WARN/FAIL counting —
   verify a crafted log line cannot suppress or force a summary.
5. **Self-confirming-check discipline:** every check must fail loudly on empty
   output (see the 2026-08-16 zombie-worktree false-PASS instance in session
   memory) — verify the wrapper's git/Hermes failure paths distinguish
   "no output" from "OK".
6. **Header/code credential-route mismatch:** the wrapper header records the owner
   directive to REUSE the existing @MTCHyperbot USER env vars
   (`TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`), but `Send-WatchAlert` still reads
   Credential Manager (`MTC-TG-BOT-TOKEN`/`MTC-TG-CHAT-ID`). Review must pick one
   route, make code and docs agree, and verify the env-var route does not leak
   values into child-process environments or logs.

## Explicitly out of scope

KVM2, deployment, bridge credentials, ARM, TESTNET, trading — untouched by this
review and by the notifier itself (one-way outbound messages only).

**Status: review NOT yet dispatched.** Dispatch is the next Lead action after owner
confirms sequencing; no activation before an accepting T0 verdict pair.
