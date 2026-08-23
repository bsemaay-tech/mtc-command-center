# Ops baseline — repo-side evidence only (wayfinder research ticket #106)

Scope: what the repository itself proves about the KVM2 Bridge deployment's
deploy/release chain, rollback, backup, observability, credentials, and
scheduling — nothing from connecting to KVM2 or any host. Every claim below
is sourced to a specific file or commit; every gap is called out explicitly
rather than assumed closed. Research performed against `origin/master` at
`ab35ca66`, with git history search across all pushed branches for the
deployment execution record (see Finding 0 — it is not on master).

## Finding 0 — the deployment evidence trail is NOT on master (structural gap)

The most consequential finding first, because it conditions everything else.

`origin/master` contains only the **pre-deployment design** for the Bridge
Linux deploy assets. `IBKR_PAPER_BRIDGE/deploy/linux/README.md` (on master)
still reads, verbatim:

> "Status: **PREPARATION ONLY — nothing here has been executed on any host.**"
> and later: "These assets have **never been executed**, on KVM2 or anywhere
> else. No Ubuntu run, no `install.sh` invocation, no `systemctl` call has
> happened."

That statement is stale. The actual execution happened on 2026-08-17 — but
its evidence lives entirely on branch `codex/rp7-r1-r4-repair-20260815`
(pushed to `origin`, tip `810f5e7e`, still checked out locally at
`C:\R7FINAL`), which **has never been merged to master**:

| Commit (on `codex/rp7-r1-r4-repair-20260815` only) | Content |
|---|---|
| `4f6f1d4e` | "owner signed the V6 section-3 installation sentence - execution begins" |
| `eb7fc4eb` | "owner approves python3.12-venv package install on KVM2" |
| `c60da675` | "owner authorizes UFW comment-normalization repair cycle; execution record corrected" |
| `2bfb26d6` | "overnight completion authorization recorded (conditional, fail-closed)" |
| `4274a7ef` | **"KVM2 deployment EXECUTED - bridge running DISARMED, D3 matrix recorded"** — the primary evidence document, `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_DEPLOYMENT_EXECUTED_2026-08-17.md` |
| `9d20c84f` | "morning handoff - bridge deployed and running DISARMED on KVM2" |

`git merge-base --is-ancestor <each of these> origin/master` returns **NO**
for all six. The `KVM2_RUNKIT/` directory (the owner-facing dashboard
launcher scripts) is likewise only present on that branch — `PHASE_WATCH.md`
on master cites it as `11_TRIAGE/KVM2_RUNKIT/Open-BridgeDashboard.ps1 (rp7
branch)`, explicitly flagging the fact that it is not on master.

**Consequence:** anyone auditing this repo from `origin/master` alone — as
this ticket's own instructions initially pointed to — would conclude the
Bridge has never been deployed anywhere. That conclusion would be wrong. The
branch is not deleted and is recoverable today, but nothing enforces that it
stays that way, and no master-side pointer/index says "the deployment record
lives on branch X." This is a single point of loss for the only execution
evidence of a real host deployment.

Master-side planning documents do assume the deployment is real and current:
`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` (on master,
dated one day before this research) states as a standing constraint: "Bridge
V1 keeps soaking, isolated and untouched. No package below modifies the
deployed V1 candidate, its configuration or its host." So the planning layer
treats the KVM2 deployment as settled fact while the evidence proving that
fact sits off-trunk.

**GAP: merge or otherwise durably anchor the `codex/rp7-r1-r4-repair-20260815`
deployment-evidence commits into master, or explicitly record a pointer to
them from a master-side ops-baseline doc, before that branch is ever pruned.**

## 1. Deployment / release chain

Design (on master, `IBKR_PAPER_BRIDGE/deploy/linux/`): `package.sh` builds an
immutable per-commit-SHA payload (`git archive` + `RELEASE_SHA` +
`RELEASE_SHA256SUMS`) on a trusted build host, never on the target.
`install.sh` performs one bounded, non-interactive, fail-closed install:
hash-locked Python 3.12 venv (`--require-hashes --no-deps
--only-binary=:all:`), release tree sealed root:root read-only, unit
installed **masked**, secrets file created names-only. `verify.sh` is a
read-only assertion pass. Every release lives at
`/opt/mtc-bridge/releases/<40-hex-sha>/`, so the unit can never silently
follow a mutable "current" symlink to a different build.

Execution (per `KVM2_DEPLOYMENT_EXECUTED_2026-08-17.md`, off-master — see
Finding 0): release `be007fd802bbfd2eb181d66038c374865d1562ee` installed on
host `srv1856225` (Hostinger KVM2, `152.239.123.231`); `verify.sh` returned
**VERIFY PASS**; `mtc-bridge-first-start.service` went active
`2026-08-17T00:25:02Z`, PID 76403, `NRestarts=0`; listener confirmed
loopback-only `127.0.0.1:8790` (public probe `TcpTestSucceeded=False`); ARM
attempted and correctly refused with HTTP 409 ("ARM unavailable in
credential-free DISARMED start mode"). This was independently corroborated by
a live read-only SSH check the same day
(`PHASE_WATCH_COLLECTOR_SELFVERIFY_2026-08-17.md`, on master): service
active ~13h, `release_sha=be007fd8…`, `state=DISARMED`,
`service_health=healthy`.

One item in the deployment record has **no corresponding script in the repo**:
Stage 2 lists "logrotate + **hourly cron runner**" as installed, but neither
`install.sh` nor `lib/common.sh` contains any `cron`/`crontab`/`timer`
reference anywhere (grepped both files, zero hits). The logrotate policy
itself is tracked (`deploy/linux/logrotate/mtc-bridge` — daily, 30
generations, 64M trigger, `copytruncate`), but whatever runs it hourly on the
host was not built by any script this repo tracks.

**GAP: the "hourly cron runner" installed on KVM2 has no source-of-truth
script in the repository — its exact command and failure behavior are not
independently verifiable from repo evidence.**

No execution has touched KVM2 since 2026-08-17 (searched `git log --all
--since=2026-08-17 -i --grep=rollback`, and no later
deploy/install/rollback-titled doc exists) — the deployment is a single
one-time event as far as the repo can prove, and `Bridge V1 keeps soaking,
isolated and untouched` (master, 2026-08-22) implies it is still the running
state as of the day before this research.

## 2. Rollback capability

`deploy/linux/rollback.sh` (on master) is well-designed on paper: stop (SIGTERM,
45s grace) + mask the unit; **optionally** re-bind to a *different,
already-installed* prior release SHA after verifying its checksums and
hash-locked venv; write a `rollback_manifest.json`; **never** touches
`/var/lib/mtc-bridge` (state/risk history is preserved as evidence, never
reset). A real rollback with re-binding requires a second release directory
to already exist under `/opt/mtc-bridge/releases/` — verified by
`[ -d "${TARGET_DIR}" ] || die "rollback release is not installed"`.

What actually happened on KVM2: the deployment record's Stage 3.2 describes a
"rollback rehearsal" that ran with rc 0, but it is explicitly self-described
as a **no-op**: "wrote `rollback_manifest.json`, unit stop/mask no-op
recorded" — the unit had not even been started yet at that point in the
sequence, so there was nothing running to actually stop, and no second
release exists on the host to re-bind to.

**GAP: rollback has never been exercised as a real rollback (stop a running
service, re-bind to a genuinely different, verified prior release) anywhere
in the repo's evidence. Only a dry rehearsal against an inactive unit with no
alternate release present has occurred. Real rollback capability is designed
and unit-tested in isolation (`tests/test_linux_deployment.py::
test_rollback_is_exact_preserves_state_and_never_starts`, cited in
`SECURITY_BASELINE.md`) but structurally unproven end-to-end on the actual
host.**

The `mtc-bridge-steady.service.template` (restart-enabled profile) exists in
the repo but is explicitly gated as never-installed: "Gated artifact — never
installed or enabled by any script here" until a fault-injection matrix
(crash/kill/reboot) proves DISARMED startup and reconcile safety. No such
matrix has run. So there is also no recovery-after-crash story beyond manual
human intervention (see §6).

## 3. Backup state — what is backed up, has restore ever been proven?

**What exists and was proven, once:** `IBKR_PAPER_BRIDGE/tools/
wal_state_bundle.py` (on master) is a genuinely careful tool — it uses
SQLite's online backup API rather than a naive file copy (explicitly because
the runtime DB is WAL-mode and a plain copy of the `.db`/`-wal`/`-shm` trio
can silently lose committed trades or risk history), runs
`PRAGMA integrity_check` + `foreign_key_check`, and re-derives sanitized
risk/history invariants on `verify`. During the 2026-08-17 install (Stage
3.1–3.5, off-master evidence) this tool produced exactly one archive,
`bridge-state-initial.tar.gz` (sha256
`2a1c42c5001e38e2925ae2565831cc7eb899a74babf4253f989abd1ee7161dc2`), which
was copied to an EFS-encrypted Windows directory
(`C:\tmp\KVM2_BRIDGE_ENCRYPTED`) and **restored to that directory with a
member-by-member sha256 compare (2 members, 0 mismatches)** — a genuine,
if narrow, restore proof for that one snapshot.

**What does not exist:** any ongoing, scheduled backup. `PHASE_WATCH.md`
(on master) defines the daily check "Backup ran / restore drill" against a
"backup dir per deployment plan — **fill at activation**" — that placeholder
was never filled. The live collector run the same day recorded this
explicitly as a blocker:

> "check4 backup-bundle — BLOCKER (no path): no real backup directory is
> defined in the deployment records; recorded `SKIPPED-NO-BACKUP-DIR`. Path
> NOT invented." (`PHASE_WATCH_COLLECTOR_SELFVERIFY_2026-08-17.md`, master)

The forward plan confirms this is a known, still-open gap rather than an
oversight this research is discovering fresh:
`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` §WP-P0-26
(OPS-A, wayfinder-fold ticket #38/#39, **not yet built, not yet authorized**)
states the objective as literally "backups that restore, and a watchdog that
tells the owner within minutes when a watched process dies — before any
forward clock exists to lose," and requires as its acceptance gate "a
restore drill proven RED/GREEN (a deliberately damaged copy shown
unrecoverable without the backup, recovered with it)." None of that exists
today.

A separate, unrelated backup tool exists in the repo
(`MTC_COMMAND_CENTER/02_MTC_BACKTEST/scripts/backup_restore.py` +
`docs/backup_restore_runbook.md`) — file-level tar/restore for backtest
results/reports/debug artifacts. It is a different subsystem entirely (not
wired to the Bridge or KVM2) and is explicitly named in WP-P0-26 as a
"harvestable existing asset" for the not-yet-built OPS-A package, not as
something currently protecting Bridge state.

**GAP: no recurring/automated backup exists for the live KVM2 Bridge state.
The only backup is the single archive made at install time, and its
restorability was proven exactly once, to a local Windows path, not as a
repeatable drill. Recurring backup + proven restore is explicitly future,
unauthorized work (WP-P0-26 / OPS-A).**

Separately, `WPI_ARTIFACT_RETENTION_INVENTORY_2026-08-17.md` (master) records
that the large historical release archives on the Windows build host
(`C:\WPI_ARTIFACTS`, ~4.85 GiB across 152 objects, including three older
extracted releases at ~2.9 GiB) have **never had a restoration test performed
before any cleanup decision** — the doc's own required gate (§10) states "The
restoration test must happen before cleanup, not after space has already
been reclaimed," and that gate had not been executed as of the doc's writing.
This is a second, independent instance of "restore not proven," on a
different artifact class (build-time staging candidates, not the live KVM2
state).

## 4. Observability toolkit + logging

**What is built and merged (Package 5a, T1, on master,
`IBKR_PAPER_BRIDGE/tools_v2/observability/`):** entirely local, offline,
read-only tooling — `export_audit_pack.py` (stdlib-only CLI, requires an
explicit `--store` path, opens SQLite `mode=ro`, builds one Markdown report;
"no default live path," never invents data), `readiness_checklist.html`
(a static pre-flight page, in-page state only, under a permanent "this page
controls nothing" banner), and `CHAOS_DRILLS_DESIGN.md` (a **design-only**
matrix of MockBroker chaos drills — the package's own "Trim statement" says
plainly: "Chaos-drill implementation is deferred. Only the design document
ships here."). None of this connects to KVM2, tails a live log, or alerts
anyone — it is a manual, explicit-input auditing aid, not monitoring.

**Live monitoring design exists but is not active.** `PHASE_WATCH.md`
(master) defines a 7-check daily Phase-1 checklist (service alive, DISARMED
mode, logs rotating, backup+restore-drill, memory/disk flat, error scan,
dashboard reachable) plus a 4-hourly Hermes-driven cron wrapper
(`C:\LAB\HERMES_WATCH\phase_watch_check.ps1`, Windows scheduled task
`MTC-HermesPhaseWatch`). Its own status block reads `WATCH_ACTIVE: NO` and
has a single update-log row dated 2026-08-16 — it has not been updated since,
even though a live collector run did happen the next day. That run's own
verdict: **"T0 review DISPATCHED... NOT accepted; `WATCH_ACTIVE` stays NO."**
Two of its seven checks came back blocked, not merely unimplemented:

- **check3 (logs rotating) — BLOCKER (permission):** the read-only SSH
  monitoring user `baris` got `Permission denied` on `/var/log/mtc-bridge/`
  (not in the `adm`/`systemd-journal` group).
- **check6 (error scan) — PARTIAL:** journal returned nothing for the same
  permission reason; `bridge.err.log` likewise `Permission denied`.

So even if the watch were activated today, two of its seven daily checks
would still be non-functional without a separate, KVM2-side group-membership
change (explicitly flagged in the same doc as "a KVM2 change, separately
gated," not fixed by anything in the repo).

**No alerting is currently live.** A Telegram notifier exists in code
(`PHASE_WATCH_TELEGRAM_NOTIFIER_DESIGN_2026-08-16.md`, master) and passed one
supervised fake-WARN test, but master's own status says: "Notifications:
Telegram notifier code present but **DEPLOYMENT HELD** — owner classified
watcher + credential/network handling as T0; review pending." There is
therefore no channel today that would tell anyone if the Bridge crashed,
KVM2 rebooted, or disk filled.

**GAP: observability = one merged local read-only audit tool (not
monitoring) + one designed-but-never-activated daily-watch system, two of
whose seven checks are permission-blocked even in design, + one
built-but-undeployed alert channel. There is no live monitoring or alerting
of the KVM2 deployment today.**

## 5. Credential storage — verifying the "credential-free bridge" boundary

Design + execution agree on the mechanism:
`/etc/mtc-bridge/mtc-bridge.env` is `root:root 0600`, created from a
comment-only template (`env/mtc-bridge.env.template` — names only, no
values, ever). `install.sh` **never writes a value into it**; if the file
already exists it is not read and not modified, only mode/ownership are
re-asserted. `HL_LIVE_ACK` is a hard-blocked variable name: `install.sh`
refuses to run if it is set in the invoking shell, and `verify.sh` fails if
it appears in the env file.

The deployment record states plainly: "Secrets: none exist; env file
names-only `0600 root:root`." This is the exact, narrow boundary of the
"credential-free bridge" claim as of 2026-08-17: **the first-start deployment
carries zero Hyperliquid exchange credentials of any kind.** The claim's
scope is that specific bring-up mode; the record itself names the boundary
explicitly — "Next separately gated steps: TESTNET secret provisioning
(owner-only), TESTNET ARM (own sentence)" — meaning credential-free is a
current state, not a permanent architectural guarantee, and would end the
moment KVM2-P4-03 (TESTNET secret provisioning, a distinct, still-unexecuted
owner gate) happens. No commit anywhere in the repo (master or the rp7
branch) records that gate having been exercised since 2026-08-17.

Two other credential classes exist adjacent to, but outside, the bridge
process itself, worth naming so the boundary isn't misread as "nothing on
the host has any credential":

- **Operator SSH access to KVM2** — used for the read-only monitoring checks
  and the original deployment transport. `PHASE_WATCH_COLLECTOR_SELFVERIFY_
  2026-08-17.md` describes it as "the audited SSH route (pinned host
  152.239.123.231, user `baris`, pinned known_hosts + agent fingerprint;
  agent-only, no key material read)." This is an operator/admin credential,
  not a Bridge application credential — but it is real standing access to
  the host.
- **Telegram bot token** — referenced only as "the owner-managed USER env
  vars `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`" on the Windows side for the
  still-undeployed notifier (§4). It is not present on KVM2 at all today
  because the notifier itself is not deployed.

One small provenance note, not a defect claim: the exact JSON field the
deployment/verification reports quote, `"mode":"credential_free_disarmed"`,
does not appear verbatim anywhere in `IBKR_PAPER_BRIDGE/bridge/` on master
(grepped case-insensitively for `credential_free`/`credential-free`, zero
hits; `bridge/api/routes.py` only shows `"mode": "paper"` as a status-route
default and `app_state` values of `"DISARMED"`). This is most likely a
synthesized descriptor written by the deploying/auditing session rather than
a literal API field, or the field lives in a code path not grepped by name —
either way it's not independently confirmable from the current source tree,
so treat the exact field name as reported-not-verified.

**GAP: "credential-free" is correctly scoped to the 2026-08-17 first-start
snapshot and is well-documented as temporary by the deployment's own record
— but nothing in the repo tracks whether TESTNET secret provisioning
(KVM2-P4-03) has since happened, so the claim's current truth cannot be
confirmed from repo evidence alone as of today.**

## 6. systemd / scheduling units

Only one unit is installed on KVM2: `mtc-bridge-first-start.service`
(template on master, `deploy/linux/systemd/
mtc-bridge-first-start.service.template`). Deliberate, documented safety
properties:

- `Restart=no` — a crash stays crashed for human inspection; auto-restart is
  explicitly forbidden until a fault-injection matrix proves DISARMED
  startup, reconcile gating, state continuity, duplicate-order prevention and
  throttling (that matrix has not run — see §2).
- **No `[Install]` section** — `systemctl enable` is structurally impossible.
  This means if KVM2 reboots for any reason, the service does **not** come
  back on its own even if it were left unmasked; a human must run
  `systemctl unmask` + `systemctl start` again, every time.
- **Installed masked** — a second, independent barrier requiring deliberate
  human action before any start is even possible.
- Genuinely hardened otherwise: `NoNewPrivileges`, `ProtectSystem=strict`,
  `PrivateTmp`/`PrivateDevices`, `RestrictAddressFamilies=AF_INET AF_INET6
  AF_UNIX`, `SystemCallFilter=@system-service`, `UMask=0077`, writable
  surface limited to exactly `/var/lib/mtc-bridge` and `/var/log/mtc-bridge`.

The restart-enabled "steady" profile
(`mtc-bridge-steady.service.template`) exists in the repo only as an inert
template — "never installed or enabled by any script here" until its own
separate Gate 5/6 acceptance, which has not happened.

**No systemd timer and no cron unit is defined anywhere in the repo's deploy
assets.** The only scheduling-adjacent artifact tracked in git is the
logrotate policy, which itself depends on the OS's own logrotate
cron/timer mechanism rather than anything `install.sh` sets up. The "hourly
cron runner" named in the deployment record (§1) is the one scheduled task
known to run on the host and has no matching script in the repo.

**GAP (compounding with §3 and §4): if the bridge process crashes or KVM2
reboots, nothing restarts it automatically, and — because Phase-Watch is not
activated and the Telegram notifier is not deployed — nothing currently
tells anyone that it happened. The design intentionally trades availability
for safety (a crashed trading bridge should not silently self-heal into an
unknown risk state), but the compensating control (a human finding out
quickly) is not yet built.**

## 7. Zero-functioning-CI fact + OPS-C planned scope

Verified directly: there is **no `.github/` directory at the repository
root** (`find .github` from repo root returns nothing). The only GitHub
Actions workflow files anywhere in the tree are
`MTC_COMMAND_CENTER/02_MTC_BACKTEST/.github/workflows/parity.yml` and
`.../tests.yml` — nested under a subdirectory, not the repo root, so GitHub
Actions would never discover or run them on this repository regardless of
their content. This independently confirms
`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`'s own
characterization (§WP-P0-27): "the repository currently has **no functioning
CI at all** (no root workflows; the two `02_MTC_BACKTEST` workflows are
inert imported artifacts that never ran in this repo)."

**Planned scope — WP-P0-27 / OPS-C ("continuous-check home"), wayfinder-fold
ticket #43, added 2026-08-23, not yet started or authorized:**

- Repo-root `.github/workflows/` on GitHub-hosted runners; explicitly **no
  secrets** in CI ("the guards are local RED/GREEN fixtures with no venue
  contact").
- Day-one job: run the Bridge pytest suite + light lint.
- Progressive required-check policy: checks required on PRs into master;
  **direct Lead pushes to master remain allowed** (the standing git
  delegation to the Lead is explicitly preserved, not overridden by CI); a
  red master run triggers immediate notification and master is never allowed
  to stay red (fix forward or revert).
- Other in-flight guard packages (WP-P0-10 golden suite, WP-P0-23 no-`alert(`
  guard, WP-P0-21 admission fixtures, the §9.6 parity set, contract tests)
  are meant to plug into this CI home once each lands — but per the
  acceptance gate, none of them may claim continuous protection until
  WP-P0-27 itself is accepted.
- Acceptance gate requires a D026 proof: the root workflow runs green on the
  Bridge suite, and a deliberately broken test is shown to turn the run red
  and trigger notification.
- Non-goals stated explicitly: no self-hosted runner (kept off the trading
  host by decision), no scheduled data jobs (that's WP-P0-30/VEN-E), no
  porting of the two inert retired-engine workflows.

**GAP: today, nothing in this repository runs any test, lint, or guard
automatically on any push or PR — CI is 100% planned, 0% built. Every claim
in this document about "the tests pass" or "verify.sh returned PASS" is
therefore evidence of a specific, manually-run, one-time execution, never of
a standing, continuously-enforced gate.**

## Summary — gaps flagged, by severity

1. **[Structural]** The only evidence that KVM2 deployment ever happened
   lives on an unmerged branch (`codex/rp7-r1-r4-repair-20260815`), invisible
   from `origin/master`. (Finding 0)
2. **[High]** No recurring backup and no proven-repeatable restore drill for
   the live KVM2 Bridge state — only one archive, backed up and restored
   once, at install time. Recurring backup is explicitly future,
   unauthorized work (WP-P0-26/OPS-A). (§3)
3. **[High]** No live monitoring or alerting exists today. The Phase-Watch
   design is unactivated (blocked at T0 review), two of its seven daily
   checks are permission-blocked by design even once activated, and the
   Telegram notifier is built but deployment-held. (§4)
4. **[High]** Rollback has never been exercised as a real rollback (only a
   no-op rehearsal against an inactive unit with no alternate release
   present to roll back to). (§2)
5. **[Medium]** No automatic recovery from crash or host reboot — the unit is
   `Restart=no` and has no `[Install]` section by design — combined with #3,
   an outage could go unnoticed indefinitely. (§6)
6. **[Medium]** Zero functioning CI; all test/verify evidence in this repo
   for the Bridge is manually triggered, one-time, and not continuously
   enforced. A concrete remediation package (WP-P0-27/OPS-C) is scoped but
   not started. (§7)
7. **[Low/Process]** An "hourly cron runner" is running on KVM2 with no
   matching script anywhere in the repo. (§1)
8. **[Low/Provenance]** The credential-free claim is correctly scoped and
   well-documented as of 2026-08-17, but nothing in the repo confirms
   whether the still-unexecuted TESTNET secret-provisioning gate
   (KVM2-P4-03) has since changed that state. (§5)

## Primary sources cited

- `IBKR_PAPER_BRIDGE/deploy/linux/README.md`, `install.sh`, `rollback.sh`,
  `verify.sh`, `SECURITY_BASELINE.md`, `systemd/
  mtc-bridge-first-start.service.template`, `systemd/
  mtc-bridge-steady.service.template`, `logrotate/mtc-bridge` (master)
- `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` (master)
- `IBKR_PAPER_BRIDGE/tools_v2/observability/README.md`,
  `CHAOS_DRILLS_DESIGN.md` (master)
- `MTC_COMMAND_CENTER/_AI_MEMORY/PHASE_WATCH.md`,
  `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` (master)
- `MTC_COMMAND_CENTER/11_TRIAGE/PHASE_WATCH_COLLECTOR_SELFVERIFY_2026-08-17.md`,
  `WORKTREE_CLEANUP_EXECUTION_2026-08-18.md`,
  `WORKTREE_NONRETIREMENT_CLASSIFICATION_2026-08-17.md`,
  `WPI_ARTIFACT_RETENTION_INVENTORY_2026-08-17.md`,
  `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` (master)
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/docs/backup_restore_runbook.md`,
  `.github/workflows/{parity,tests}.yml` (master)
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_DEPLOYMENT_EXECUTED_2026-08-17.md` (commit
  `4274a7ef`, branch `codex/rp7-r1-r4-repair-20260815` only — NOT on master;
  read via `git show 4274a7ef:<path>`)
- git history: `git log --all --oneline --since=2026-08-16 --until=2026-08-18`,
  `git merge-base --is-ancestor <sha> origin/master` checks, `git ls-remote
  --heads origin codex/rp7-r1-r4-repair-20260815`
