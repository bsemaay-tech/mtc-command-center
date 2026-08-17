# Phase-watch Option B collector + notifier — T0 review Round 1 result

**Outcome: NOT ACCEPTED. One flagship verdict = BLOCK (13 REQUIRED + 2 nits). The
second flagship could not run. `WATCH_ACTIVE` stays NO; the notifier/collector are
NOT accepted and do NOT activate.**

## Dispatch record

| Auditor | Model / effort | Route | Result |
|---|---|---|---|
| Codex | `gpt-5.6-sol` xhigh, fresh read-only sandbox | account `free` | **BLOCK — 13 REQUIRED, 2 nits** (full text: `11_TRIAGE/audits/CODEX_T0_COLLECTOR_gpt56sol_xhigh_20260817.txt`) |
| Claude | `claude-opus-5` xhigh | Claude Pro/Max weekly window | **BLOCKED — capacity: weekly limit, resets 2026-08-19 23:00 Europe/Chisinau.** Codex `secondary`→Aug 22 and `fourth`→Aug 20 are also exhausted. Not run. |

Per `AGENTS.md` (exact model/effort unavailable → BLOCK unless owner waives) and the
four-auditor acceptance floor (both flagships must accept), acceptance is impossible
this session regardless of repair. Recorded honestly; no acceptance claimed.

## The BLOCK is correct — the review found real defects

The Option B collector is a genuine improvement over an LLM-with-SSH design, but the
xhigh review showed it is not yet safe to activate. Highest-value REQUIRED findings
(full list in the archived verdict):

1. **Hermes ambient capability (core):** giving Hermes only the evidence-dir path is
   not isolation — the Hermes PROCESS still runs as the user with filesystem,
   network, registry, and ssh-agent access. Prompt-injection text in evidence is
   contained only by instruction, not by capability. Real fix needs a tool-free
   summarization API or a restricted identity, not just a careful prompt.
2. **`-BackupDir` accepts the secret file:** `/etc/mtc-bridge/mtc-bridge.env` passes
   the absolute-path regex → `ls -lh /etc/mtc-bridge/mtc-bridge.env`, violating the
   never-reference-env-file rule. Needs a finite reviewed path allowlist, not a
   regex.
3. **SSH hardening:** `$USERPROFILE` interpolated into a hand-quoted ssh arg; ssh
   still loads user config (ProxyCommand/LocalCommand/SendEnv); no `IdentitiesOnly`;
   no server-side forced-command allowlist.
4. **Env scrub incomplete:** only the two exact names are stripped (not all
   `TELEGRAM_*`), and the collector/git/ssh children inherit them; credentials may
   be read from process scope, not only User scope.
5. **Evidence selection hijack:** predictable second-resolution dir names created
   with `-Force`, then "latest by name" globbing — a pre-created `999…` dir,
   same-second collision, or reparse point can feed Hermes stale/hostile evidence.
6. **Sanitizer gaps:** JWT/bearer/cookie/base64/PEM/URI-credential shapes evade the
   regex; the 20 KB cap counts UTF-16 chars, so multibyte output can exceed it.
7. **Exit-code masking / self-confirming:** `;`-chains and `journalctl | tail` expose
   only the last command's status; empty output and HTTP-error bodies still record
   `COLLECTED`; the collector exits 0 even with ERROR entries.

(8–13 cover git-fetch ref semantics, `WATCH_ACTIVE` default-NO passing, exit-zero
monitoring blackout, `-FixtureDir \\UNC\share` network access, and daily-summary
logfile reparse. Nits 14–15: `[bool]$env:` cannot distinguish absent vs empty;
`Send-WatchAlert` prefix enforced only by caller discipline.)

## Lead pre-review hardening already applied (partial, not closure)

Two small fixes made this session — strict improvements, no regression, wrapper
still parses and the PENDING path is unchanged — acknowledging but NOT closing
findings 4 and 5:
- The collector child is now launched via `Invoke-SanitizedProcess` too (its
  TELEGRAM_* names stripped) — partial toward #4.
- The wrapper now takes the exact run directory from the collector's own
  `Evidence written:` line instead of "newest by name" — partial toward #5.

These do not resolve the findings (which demand all-`TELEGRAM_*` stripping +
User-scope-only reads, and atomic/locked/non-reparse dir creation). They are logged
as partial so the repair round starts from an honest baseline.

## What this means / next

- The bounded live run already proved the BRIDGE itself is healthy and DISARMED
  (`PHASE_WATCH_COLLECTOR_SELFVERIFY_2026-08-17.md`) — that finding stands. The
  BLOCK is about the WATCHER's safety to run unattended every 4h, not the bridge.
- A real repair round against the 13 findings is required before re-dispatch. Some
  findings (Hermes capability confinement #1; server-side forced-command #3) involve
  design choices and possibly KVM2-side configuration — owner/deployment-owner
  input needed, not a pure local fix.
- The second flagship (`claude-opus-5` xhigh) cannot run until 2026-08-19 23:00
  anyway, so the clean dual-flagship pair is gated on that date regardless.

**Owner decision needed** (do not proceed without it): repair the collector against
these findings now and re-dispatch after Aug 19, or pause the watcher work and
rely on the cheap manual DISARMED health glances until then. Either way,
`WATCH_ACTIVE` stays NO and no activation happens without an accepting T0 pair plus
the still-open activation-input blockers (real backup directory; `baris` log-read
permission).
