# Phase-watch collector — repair ledger vs T0 Round-1 BLOCK

Owner decision 2026-08-17: repair now, re-audit after 2026-08-19 (when
`claude-opus-5` xhigh reopens for the clean dual-flagship pair). This ledger maps
every finding from `PHASE_WATCH_COLLECTOR_T0_ROUND1_2026-08-17.md` /
`audits/CODEX_T0_COLLECTOR_gpt56sol_xhigh_20260817.txt` to its disposition.
`WATCH_ACTIVE` stays NO throughout; nothing activates without an accepting pair.

## Disposition

| # | Sev | Finding | Status | What was done / what remains |
|---|-----|---------|--------|------------------------------|
| 1 | REQ | Hermes retains ambient capability under prompt-injection | **DEFERRED — owner/design** | Prompt text is not isolation. Recommended fix: replace the Hermes *agent* summarize step with a capability-free direct LLM completion call (evidence text in → summary out; no tools, no filesystem/network/ssh-agent beyond the one API request). Needs owner endorsement + an API key. This is the one finding the current mechanism cannot satisfy by hardening alone. |
| 2 | REQ | `-BackupDir` regex accepts `/etc/mtc-bridge/mtc-bridge.env` | **FIXED** | Regex replaced by a reviewed exact-match allowlist (`$AllowedBackupDirs`, empty until a real dir is defined). Secret path now refused (verified: exit 2). |
| 3 | REQ | SSH config loading / no IdentitiesOnly / hand-quoted `$USERPROFILE` | **PARTIAL** | ssh now via arg array (no injection), `-F NUL` disables user config (ProxyCommand/LocalCommand/SendEnv), `IdentitiesOnly=yes`, `ClearAllForwardings`, `PermitLocalCommand=no`, `ForwardAgent=no`; `curl -q`. **Remaining (DEFERRED, KVM2-side):** server-side forced-command allowlist on the `baris` key — deployment-owner action. |
| 4 | REQ | Only two exact `TELEGRAM_*` stripped; process-scope creds; children inherit | **FIXED** | Creds read User-scope ONLY; `Invoke-SanitizedProcess` strips EVERY `TELEGRAM_*` (case-insensitive); collector now launched through it too (verified: env probe GREEN False/False, nonzero-on-inherit). git child still inherits (needs no TG vars, local-only) — noted for reviewer. |
| 5 | REQ | Evidence "latest by name" hijack | **FIXED** | Run dir now atomic (`New-Item` fail-if-exists), UTC+GUID name, reparse-point refused, `COMPLETE` marker written; wrapper consumes the exact dir from the collector's `Evidence written:` line, not a newest-by-name glob. |
| 6 | REQ | Sanitizer misses JWT/PEM/base64/bearer/URI; UTF-16 vs UTF-8 cap | **FIXED** | Added patterns for authorization/bearer/cookie, JWT, PEM, long base64, URI creds; hex threshold 32; truncation on a UTF-8 byte boundary (verified: JWT+PEM+hex all redacted). |
| 7 | REQ | `;`/pipe mask exit codes; empty output → COLLECTED | **FIXED** | Empty stdout → `EMPTY`, nonzero → `ERROR`, both flip an aggregate nonzero exit (5); activation-blocking skip → exit 6 (verified). |
| 8 | REQ | `git fetch` ref semantics / stale ref can authorize live contact | **TODO (before re-audit)** | Add fetch exit-code check + verify `origin/master` OID actually advanced before trusting `WATCH_ACTIVE`. |
| 9 | REQ | Malformed/duplicate `WATCH_ACTIVE` defaults to NO; param sets | **PARTIAL** | Default-NO is fail-safe for activation (NO = no action). Remaining: enforce mutually-exclusive `-TestReport/-FakeWarnTest/-EnvProbe`, reject duplicate/malformed `WATCH_ACTIVE` as an explicit error. |
| 10 | REQ | Hermes output not schema-validated; free-form clauses sent to Telegram | **TODO** | Require exact schema (each expected check once + one SUMMARY); build the notification from fixed status codes, not model free-text. |
| 11 | REQ | Exit-zero monitoring blackout | **PARTIAL** | Collector now returns nonzero on incomplete. Remaining: wrapper active path should propagate a nonzero task exit (currently logs FAIL then exit 0) so Task Scheduler sees failure. |
| 12 | REQ | `-FixtureDir \\UNC` network access; file-not-dir passes; missing fixtures pass | **FIXED** | UNC rejected; must be a real directory under `C:\LAB\HERMES_WATCH`; reparse rejected; missing fixture → ERROR (verified). |
| 13 | REQ | Daily-summary reparses the model-text logfile; dedup race | **TODO** | Separate machine per-run JSON state from model text; count every incomplete/ERROR; cross-process mutex + atomic dedup stamp. |
| 14 | nit | `[bool]$env:` can't tell absent vs empty; probe exit ignored | **FIXED (stub)** | Stub enumerates the process env key collection and exits with the still-present count. Remaining nit: wrapper `-EnvProbe` should assert the GREEN exit == 0. |
| 15 | nit | `Send-WatchAlert` prefix caller-supplied | **FIXED** | Base `[PHASE WATCH][KVM2]` prefix is now prepended inside the function and immutable; callers may only add a validated bracketed-uppercase suffix (e.g. `[TEST]`). |

## Summary

- **Fixed and re-verified this session:** #2, #4, #5, #6, #7, #12, #15 (+ #14 stub).
- **Partial:** #3 (local done; server-side deferred), #9, #11, #14 (wrapper assert).
- **TODO before the Aug-19 re-audit:** #8, #10, #13, and finishing the partials.
- **Deferred to owner/design:** #1 (capability-free summarizer — the key decision),
  #3 server-side forced-command (KVM2/deployment-owner).

Re-verification evidence stays local (parse 0 errors; env-probe RED True/True →
GREEN False/False; secret-path backup refused; JWT/PEM/hex redacted; fail-closed
exit codes). No Telegram message was sent during repair (the one 2026-08-16
23:48:18 TEST remains the only send). Artifacts staged for re-audit in
`C:\tmp\t0_collector`.

## Also still open (activation inputs, unchanged)

Real backup directory undefined; `baris` lacks read permission on
`/var/log/mtc-bridge/`. Both are owner/deployment-owner items, not collector bugs.

---

## ROUND 1b UPDATE — 2026-08-17 evening (owner-approved summarizer + remaining repairs)

Owner approved the tool-free direct summarizer for finding #1 with the honest
descriptor: **it is NOT literally capability-free — it performs one outbound HTTPS
request to a fixed endpoint and holds a provider credential for that request.**
Constraints implemented exactly: existing owner-managed `DEEPSEEK_API_KEY` reused
from its existing source (User-scope env var, the same one `_deepseek_driver`
uses); value never displayed/copied/rotated/deleted/logged; no new credential
entries; sanitized evidence passed as CONTENT (never a path); no filesystem/SSH/
shell/subprocess/agent tools; fixed endpoint `api.deepseek.com` + fixed model
`deepseek-chat`; 60 s timeout; 48 KB input cap; schema-validated output.

| # | Status now | Evidence |
|---|---|---|
| 1 | **IMPLEMENTED (honest descriptor above)** | `Invoke-DirectSummary` replaces Hermes on the ACTIVE path. `-SummarizerProbe` ran ONE bounded real call on injection-laced fixtures: schema-valid, `error-scan -> FAIL` (bait correctly judged from data), `SUMMARY=FAIL`, exit 0. Hermes remains only in the local `-TestReport` demo. |
| 8 | **FIXED** | `Resolve-PhaseWatch` verifies fetch exit + `rev-parse --verify origin/master`; ACTIVE runs REFUSE (exit 1, INCOMPLETE state) unless state came from a freshly verified `origin/master` — stale/local never authorizes live contact. |
| 9 | **FIXED** | Mode switches mutually exclusive (verified exit 2); `WATCH_ACTIVE` must appear EXACTLY once or the run fails closed (exit 1). |
| 10 | **FIXED** | Strict schema: every expected check exactly once + one SUMMARY, extras rejected; Telegram alert text rebuilt from parsed fixed statuses only, never model free text. |
| 11 | **FIXED** | Every failure path writes run state and exits nonzero; a non-OK outcome exits 1 so Task Scheduler sees failure. |
| 13 | **FIXED** | Daily summary reads machine-written per-run JSON state (never the text log); unreadable state counts bad; `Global\` named mutex + atomic stamp-file creation for dedup. |
| 14 | **FIXED fully** | Stub enumerates env keys and exits with present-count; `-EnvProbe` asserts RED>0 / GREEN==0 (verified: RED exit 2, GREEN exit 0, PASS). |
| 3 | **Design + T0 package PREPARED** | `PHASE_WATCH_FORCED_COMMAND_DESIGN_2026-08-17.md` — dedicated owner-generated key, server-side forced-command menu (check IDs, not commands, cross the wire), log-ACL options. NOTHING applied to KVM2; server change needs separate owner approval after review. |

Verification session evidence: parse 0 errors; mode-exclusion exit 2; env-probe
PASS; PENDING regression clean; one summarizer API call (the only network use —
no Telegram send, no KVM2 contact). All 13 REQUIRED findings now FIXED except
#3-server-side (designed, owner-gated). Artifacts staged in `C:\tmp\t0_collector`
for the 2026-08-19 exact `claude-opus-5` xhigh + `gpt-5.6-sol` xhigh re-audit.

---

## OWNER RULING 2026-08-17 late — local repairs accepted for continued review

Collector local repairs ACCEPTED FOR CONTINUED REVIEW (not final acceptance).
`WATCH_ACTIVE: NO` unchanged. Finding #3 design revised to V2 per six owner
requirements (dedicated unprivileged `mtc-watch` account, owner-generated key +
restrict, DPAPI agent-service reboot story with the honest logged-on-only
limitation, exact-file ACLs with journal access dropped by default, a real
backup CONTRACT separate from monitoring, frozen pre-application artifact set)
— see `PHASE_WATCH_FORCED_COMMAND_DESIGN_2026-08-17.md` (V2, supersedes V1 in
place). **The acceptance re-audit is GATED, not scheduled: it must NOT be
dispatched while finding #3 or the backup contract is incomplete.** The earlier
"automatic Aug-19 dispatch" wording is WITHDRAWN — capacity reopens then, but
dispatch depends on the gate chain in the design doc, and no real scheduled
follow-up exists.
