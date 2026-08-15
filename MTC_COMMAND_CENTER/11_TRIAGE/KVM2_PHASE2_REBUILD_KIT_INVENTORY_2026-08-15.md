# Lane L10 — KVM2 Phase-2 rebuild-kit inventory (input to R31/R32)

- Lane output for the Lead and the owner. **Not a gate verdict, not an acceptance,
  not an authorization.** Material only.
- Repo state examined: `C:\RO` detached at `25564449`, clean; Gate-A candidate
  `2ce41e34bceb599d80af24c5c33d835820ec321b` ("fix(deploy): reject start-mode env
  override", 2026-08-08) compared read-only via `git diff`/`git log`/`git show`/
  `git merge-base`. No index-locking command was run; nothing in the repo was
  written, created, deleted or modified. This file is the lane's only output.
- Task-contract source for every P2 item:
  `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
  (below: `EXECUTION_TASKS`). Work-catalogue rows R31/R32:
  `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:70-71`.

## 0. Headline

All ten R31 artifacts **already exist as committed design documents** under
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/`, and every one of them **partly
satisfies** its task contract — none fully satisfies it, and none has any
independent acceptance. The P2-09 rehearsal record exists and its verdict is
**BLOCKED / UNVERIFIED**. So R31 is not an authoring-from-zero row; it is a
gap-closing, staleness-repairing, and acceptance row. Every per-artifact
remaining-work figure is **NO SOURCED ESTIMATE** (§5); the standing rule against
invented figures is applied, and §5.2 lists the nearby sourced ranges that must
*not* be booked against R31/R32.

## 1. Provenance and acceptance state of the existing kit

- The entire `KVM2_PROGRAM` tree was created in one commit, `6fe0130f`
  "feat(kvm2): complete Cycle 4 VPS bridge readiness" (2026-07-26), and **no later
  commit on the HEAD line touches it** (`git log 25564449 -- …/KVM2_PROGRAM`
  returns only `6fe0130f`). `6fe0130f` is an ancestor of HEAD
  (`git merge-base --is-ancestor` → true).
- The same tree is **byte-identical in `2ce41e34` and HEAD**
  (`git diff --stat 2ce41e34 25564449 -- …/KVM2_PROGRAM` → empty). The Gate-A
  candidate therefore adds nothing to the ten design artifacts themselves; what it
  adds is implementation bytes (§4).
- Acceptance state, in the kit's own words: "Classification: builder self-QA only;
  Independent audit verdict: **NONE / OPEN**; Final acceptance: **OPEN — Codex
  Lead**" (`KVM2_PROGRAM/audits/READINESS_STATUS.md:3-6`). The index adds
  "Release candidate: **OPEN** until the completed diff is committed, hashed,
  staged on Ubuntu 24.04, and independently accepted"
  (`KVM2_PROGRAM/INDEX.md:8-9`) and "P2-09 reproducibility rehearsal | BLOCKED /
  UNVERIFIED" (`KVM2_PROGRAM/INDEX.md:17`).
- The WP-L record independently confirms the caveat that survives merging:
  `6fe0130f` is already an ancestor of master with the deploy package
  byte-identical, but "the package is builder-self-QA-only and independently
  unaccepted still binds: being on master is not acceptance"
  (`MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:2669`; same point at
  `:2498,:2517`).
- Phase-2's own frame is "Preparation artifacts only; no reprovision or install"
  (`EXECUTION_TASKS:92-94`), closed only by owner acceptance at P2-12
  (`EXECUTION_TASKS:188-192`), which is work-catalogue row R33 (OWNER)
  (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:72`). No P2-12 acceptance exists.
- Post-2026-07-26 audit of these artifacts: **UNKNOWN** — the repo shows no commit
  touching the tree and no 2026-08-15 triage document recording one (grep of
  `11_TRIAGE` for `P2-0x` finds only the 2026-07-26 cycle records, the two
  governing KVM2 plans, the work breakdown, and the plan-authority
  reconciliation). What would settle it: a Lead-ordered search of audit records
  or a fresh reviewer dispatch under the audit-tier policy — not requested here.

## 2. The ten artifacts, one by one

Verdict scale: EXISTS / EXISTS — PARTLY SATISFIES / ABSENT. "Contract" cites are
the task's own Evidence lines; all gap statements below are document-grounded.

### 2.1 P2-01 — two machine profiles — EXISTS — PARTLY SATISFIES

Contract: "`temporary-testnet-lab` and `future-trading-only` profiles with an
explicit diff of packages, users, services, network, writable paths, forbidden
components" (`EXECUTION_TASKS:96-101`).

What exists:

- `rebuild/profiles/temporary-testnet-lab.md` — required bridge baseline
  (Ubuntu 24.04.x, Python 3.12, non-login `mtc-bridge`, immutable `/opt` release,
  state/log-only writable paths, `127.0.0.1:8790`, masked first-start unit;
  `:7-18`), optional-lab deferral (`:20-26`), forbidden list (`:28-33`).
- `rebuild/profiles/future-trading-only.md` — inheritance-based trading-only
  definition with an explicit no-lab-components list (`:12-17`) and post-build
  audit/mainnet gate (`:19-21`).
- `rebuild/profiles/PROFILE_DIFF.md` — a surface-by-surface diff table (bridge,
  identities, containers, listeners, control, writable paths, restore source,
  credentials, host trust, mainnet; `:3-16`).

Gap / what remains: the diff is at **policy level, not inventory level** — no
per-profile package list, no user/group list beyond `mtc-bridge`, no service
inventory beyond the bridge unit. The artifact itself defers this: "Package,
user, service, listener, unit, filesystem, and credential-name inventories must
be mechanically diffed during rehearsal and final build"
(`PROFILE_DIFF.md:18-20`). The Stop condition (trading-only containing an
agent/lab user/browser/etc.) is met by construction in text
(`future-trading-only.md:12-17`). Remaining: enumerate the two inventories (the
package side is blocked on P2-02's OPEN OS rows, §2.2) and wire the mechanical
diff into the P2-09 rehearsal and final build. Estimate: **NO SOURCED ESTIMATE**
— no source prices it; settler: a scoped write contract plus a timed authoring
session per artifact (§5).

### 2.2 P2-02 — trusted-input manifest — EXISTS — PARTLY SATISFIES, downstream-blocked

Contract: "Ubuntu source/version, repositories, package/version lock, Python
lock+hashes, release artifact SHA, source commit, systemd-unit hashes, bootstrap
hash, verification procedure" plus OS-provenance rules
(`EXECUTION_TASKS:102-113`).

What exists:

- `rebuild/manifests/TRUSTED_INPUTS.md` — self-declared "**PARTIALLY POPULATED /
  NOT A RELEASE**" (`:3`), with a freeze table in which **8 of 11 rows are OPEN**:
  Ubuntu image, apt repositories, OS packages, Python runtime, release source,
  payload, rendered unit hashes, bootstrap/installer, state artifact
  (`:15-27`); the lock row is "Prepared locally; Ubuntu install UNVERIFIED"
  (`:21`).
- Implementation-side inputs that partly satisfy the lock/verification rows:
  `IBKR_PAPER_BRIDGE/requirements.in`/`requirements.lock` resolved for CPython
  3.12/Linux with full hashes, `verify_lock.py`, and the hash-locked
  venv installer (`IBKR_PAPER_BRIDGE/deploy/linux/README.md:58-78`).
- A built-payload verification record exists for the **WP-I** candidate
  `1adf9ae5…` (RELEASE_SHA256SUMS SHA-256, `sha256sum -c` all-entries pass,
  zero-hit secret scan) — but it binds the WP-I frozen source `637307e8…`, not
  any KVM2 Phase-2/Phase-3 candidate
  (`IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:44-49,97-100`; HEAD-only
  file, §4).

Gap / what remains: the OPEN rows cannot close inside Phase 2 — the release
source/payload/unit rows wait on the integrated release candidate (catalogue
rows R03–R08), and the Ubuntu rows wait on the P2-09/P3-03 environment
(`TRUSTED_INPUTS.md:29-33`). One staleness repair is needed: row "Release
source … OPEN **because this batch is uncommitted**" (`:22`) — the 2026-07-26
batch is now committed as `6fe0130f`; the OPEN status is still correct (no
integrated candidate exists) but that reason string is stale. Estimate: **NO
SOURCED ESTIMATE** — settler: freeze the per-row producer/command/evidence
contract and time one population pass after the candidate identity exists.

### 2.3 P2-03 — identity/filesystem boundaries — EXISTS — LARGELY SATISFIES AS DESIGN

Contract: "users/groups, login/sudo policy, directories, ownership, modes,
read-only release path, writable state/log paths, explicit cross-user denial
tests for both profiles" (`EXECUTION_TASKS:114-118`).

What exists: `boundaries/IDENTITY_AND_FILESYSTEM.md` — identity definition with
no-privileged-groups rule (`:3-8`); a full path/owner/mode matrix covering
release, venv, state, logs, config, env, unit, logrotate (`:12-23`); unit
sandboxing summary (`:28-31`); a "Required denial checks" list (`:35-41`).
The shipped unit template implements the sandbox concretely —
`ProtectSystem=strict`, `ReadWritePaths=/var/lib/mtc-bridge
/var/log/mtc-bridge`, `PrivateTmp`, `ProtectHome`, `NoNewPrivileges`, empty
capability set, syscall filter
(`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:62-91`).

Gap / what remains: the denial checks are **specified, not executed** — they are
host-side assertions at install/admission time, and the cross-user (lab) checks
cannot run before a lab identity exists ("No lab identity or child process
exists in the current batch; Phase 6 remains blocked",
`IDENTITY_AND_FILESYSTEM.md:39-40`). So the Stop condition ("lab identity can
read or control bridge material") is not yet triggerable, which is correct, not
a defect. Remaining: bind these checks into the P2-09/P4-02 execution matrices
(the staging matrix already carries "verify users, groups, paths, ownership,
modes, no symlinks, immutable trees" as case 7,
`rehearsals/STAGING_MATRIX.md:42`). Estimate: **NO SOURCED ESTIMATE**.

### 2.4 P2-04 — network and service blueprints — EXISTS — PARTLY SATISFIES

Contract: "firewall manifest, listener inventory, loopback assertions, hardened
service definitions, restart throttling, resource slices, graceful stop, log
ownership, hashes… log rotation/retention/compression policy with config hash
frozen here; forced-rotation test at P4-07" (`EXECUTION_TASKS:119-130`).

What exists:

- `boundaries/NETWORK_AND_SERVICE.md` — network contract incl. default-deny
  SSH-only UFW, read-only firewall assertions, never-public 8790 (`:3-11`);
  two-unit profile discipline (first-start masked/`Restart=no`/no `[Install]`;
  steady unit inert until fault-injection proof) (`:13-27`); frozen log policy
  (daily, 30 generations, 64 MiB early rotate, delayed compress, `copytruncate`,
  `0640 mtc-bridge:mtc-bridge`) with the forced-rotation test explicitly deferred
  to the first-start matrix (`:29-34`).
- Real templates: the first-start unit (`Restart=no` at
  `mtc-bridge-first-start.service.template:53`; throttling keys `:26-27`;
  graceful stop `:45-50`; persistent log ownership `:56-59`) and
  `logrotate/mtc-bridge` implementing exactly the frozen policy
  (`:13-26`, with the P4-07 forced-rotation note at `:7-11`).
- README design decisions covering masked-not-disabled, loopback-only,
  firewall-never-touched, and the honest same-host-isolation limit
  (`deploy/linux/README.md:80-98,133-135`).

Gap / what remains:

1. **Resource slices are ABSENT.** The contract lists "resource slices" among
   the required evidence (`EXECUTION_TASKS:119-124`); grep of both unit
   templates for `Slice|CPUQuota|MemoryMax|TasksMax|MemoryLimit|CPUAccounting`
   returns nothing, and neither `NETWORK_AND_SERVICE.md` nor the README names a
   bridge-service slice/cgroup budget. What it must contain: the bridge
   service's slice/cgroup ceilings (or an explicit owner-accepted decision that
   none are set pre-Phase-6, with the reason recorded), folded into the hashed
   unit/profile.
2. **Rendered hashes are OPEN** — templates exist, but "First-start unit |
   Rendered exact-SHA filename and SHA-256 | Template prepared; rendered hash
   OPEN" (`TRUSTED_INPUTS.md:24-25`); they can only be computed against a real
   release candidate.
3. Forced-rotation test and the steady-profile fault-injection matrix are
   deliberate later gates (P4-07 / P5-03A), not Phase-2 gaps.

Estimate: **NO SOURCED ESTIMATE**.

### 2.5 P2-05 — secret inventory — EXISTS — PARTLY SATISFIES

Contract fields: "secret name/purpose, owner, issuer, allowed consumer, storage
class, mode requirement, rotation trigger, revocation procedure, backup
inclusion/exclusion. Values absent" (`EXECUTION_TASKS:131-135`).

What exists: `recovery/SECRET_INVENTORY.md` — a six-name table (HL account
address, HL API wallet key, Telegram token/chat, Anthropic key, xAI key) with
purpose, allowed consumer, storage, backup exclusion, rotation trigger
(`:6-13`); `HL_LIVE_ACK` forbidden everywhere (`:15-16`); monitoring/backup
credentials deferred to P5-01 (`:17-18`); installer contract-only behaviour
(`:20-21`). Values are absent, satisfying the Stop condition by construction.

Gap / what remains: three contract fields have no column and no text —
**owner**, **issuer**, and a **revocation procedure** (the table has a rotation
*trigger*, not the procedure steps). Mode requirement is covered implicitly by
"Root-owned 0600 env file" (`:8-13`). What the additions must contain: per-secret
owner and issuer (by role, no private identifiers, same discipline as
`ACCESS_RECOVERY.md:25-26`) and a revocation runbook per name. Note D4
(2026-08-15) deferred the TESTNET wallet, so the `HL_API_WALLET_KEY` row stays
unprovisioned by design (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:80-87`).
Estimate: **NO SOURCED ESTIMATE**.

### 2.6 P2-06 — state continuity and recovery — EXISTS — PARTLY SATISFIES

Contract: owner-accepted RPO/RTO per class, backup cadence/retention,
WAL-consistent capture rules, SQLite `integrity_check` plus application-level
risk-state invariants, off-PC encryption-key recovery, exact-release restore
order, WAL-or-fresh option per P3-01, loss/foreign-order handling, backup
encryption/retention, isolated restore drill; failed checks block ARM/resume
(`EXECUTION_TASKS:136-146`).

What exists: `recovery/STATE_CONTINUITY.md` — the WAL migration contract bound
to `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` (read-only source, online
backup, integrity + foreign-key checks, provenance hashes, sanitized invariants,
blocks on any mismatch; `:7-26`); recovery-class table (`:28-35`); off-host
encrypted versioned backup requirements with retention lock and off-PC key
recovery (`:36-39`); no-restore-without-drill rule (`:41-43`). The rehearsal
matrix carries the WAL happy/failure cases (`STAGING_MATRIX.md:24-25,47-48`) and
the P3-01 adversarial scenarios (`:59-67`).

Gap / what remains:

1. **RPO/RTO are OPEN owner decisions** in all three classes
   (`STATE_CONTINUITY.md:30-34`) — the Stop condition "RPO/RTO undefined or not
   per-class" is currently met *against* the kit.
2. **Stale against D5.** The artifact says "Conservative fresh-state reset: not
   selected, not approved" (`:5`); the owner selected **start clean** on
   2026-08-15 (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-96`). D5's own wording
   makes the fresh reset carry a preserve-or-block obligation over lost
   daily-loss/consecutive-loss/order/foreign-position evidence
   (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:98-107`), and leaves an open
   archive-off-host sub-question (`:112-116`). The fresh-reset branch therefore
   needs its own written contract (what is archived or refused, and the proof
   that "start clean" is not "start blind"); none exists today.
3. **The WAL tool's Linux fixes are not on mainline.** A 2026-08-02 Gate-A
   failure analysis records that on the locked Python 3.12 runtime ~21
   `wal_state_bundle` tests failed with `source_changed_during_capture` — "the
   Stage E cutover tool, so the KVM2 cutover as written cannot produce a valid
   state bundle on Linux" (`GLOBAL_HANDOFF.md:2316`, section "[Claude Opus 5]
   2026-08-02 — Gate A EXECUTED and FAILED at A-2"). The fixes exist only on the
   Gate-A line (`f1ac2565` attach the WAL before the capture bracket opens;
   `df00634f` reject a hot WAL before connecting; `7aad0377` validate the WAL
   index before capture — `git log 4d2228cf..2ce41e34`), and
   `git diff 2ce41e34 25564449 -- …/wal_state_bundle.py` shows HEAD **lacks 162
   lines** of that fix work. Whether the fixes fully close the 3.12 finding on a
   future integrated candidate is UNKNOWN until R06/R07 matrices run; no PASS
   transfers (`BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:234`).
4. Isolated restore drill and off-PC key-recovery test: not run (by design,
   later phases), consistent with `:41-43`.

Estimate: **NO SOURCED ESTIMATE**.

### 2.7 P2-07 — access recovery / external dependencies — EXISTS — PARTLY SATISFIES (structure only)

Contract: "SSH public-key recovery procedure; DNS/domain/certificate inventory;
provider/account ownership; off-host backup destination; emergency-console
procedure — all without credentials" (`EXECUTION_TASKS:147-151`).

What exists: `recovery/ACCESS_RECOVERY.md` — the no-single-PC/no-untested-
credential principle (`:5-7`) and the exact list of owner recordings required
before execution (key custody roles, provider-panel ownership + MFA +
emergency console, second-device recovery test, revocation authority, backup
provider + recovery credential, DNS/domain/cert inventory or explicit `NONE`,
expiry/billing/renewal owners; `:9-18`), provider-panel action prohibition with
P5-04 reset and master-stop rule (`:20-23`), no-private-identifier rule
(`:25-26`).

Gap / what remains: **every concrete item is OPEN** — the artifact's own status
is "design only; owner/provider details remain OPEN" (`:3`). What would close it
is owner recordings (roles and procedures by name, no values), not further
design. The Stop condition ("recovery depends on one unavailable PC or one
untested credential") is currently untestable because nothing has been recorded
or tested. Estimate: **NO SOURCED ESTIMATE** — the recording burden is
owner-side; no source prices the document assembly around it.

### 2.8 P2-08 — teardown / destructive-reprovision manifests — EXISTS — PARTLY SATISFIES (schema, not inventory)

Contract: "lab service/user/package/container/cron/timer/network inventory;
data export list; credential rotation list; verified-only restore allowlist;
items that must never cross into trading-only" (`EXECUTION_TASKS:152-157`).

What exists: `recovery/TEARDOWN_AND_REPROVISION.md` — the enumeration duty with
absence-must-be-proved rule (`:3-9`), export allowlist rules with
rotate-not-copy credentials (`:11-15`), the never-restore-into-trading-only list
(lab OS image/snapshot, lab home, agent workspace, cached credential, package
environment, container storage, browser data, scheduled task, lab log, lab
backup; `:17-21`), and Option A/B packet requirements (`:23-27`). The companion
"critical rule" — a post-lab snapshot is a lab recovery snapshot, not a clean
trading image — is carried at `EXECUTION_TASKS:194-195` and enforced by the
never-restore list.

Gap / what remains: the inventory is necessarily **empty** because no lab
component exists yet; the artifact defines the categories, not instances. It
populates only as Phase 6/7 admit workloads, and the export/rotation lists
finalize at Option A/B time. Remaining Phase-2 work is at most a cross-check
that the category list matches the profile diff (§2.1). Estimate: **NO SOURCED
ESTIMATE** (and near-zero doc-side work; the real work is inherently later).

### 2.9 P2-10 — maintenance contract — EXISTS — PARTLY SATISFIES

Contract: "unattended-upgrade config/scope; auto-restart/auto-reboot policy;
owner maintenance window; pre-update recovery procedure; package/unit/config
diff before/after updates; DISARMED restart+reconcile sequence; rollback
procedure; rules triggering monitoring reset, re-audit, or lab re-admission.
Drill spec … as design; execution deferred to P4-07A"
(`EXECUTION_TASKS:168-177`).

What exists: `recovery/MAINTENANCE.md` — status "specification only; drill
execution OPEN" (`:3`); the default-off policy for automatic reboot/restart
(`:5-8`); a nine-step maintenance-window procedure including pre/post manifests,
unit-hash comparison, one separately authorized DISARMED restart, reconcile
proof, rollback on drift (`:10-20`); drift/reset/reclassification rules bound to
the future P5-04 contract (`:22-25`); P4-07A drill noted OPEN (`:27-28`).

Gap / what remains: **the unattended-upgrades scope/config is not specified** —
the contract's first required element exists only as a precondition sentence
("may be configured only after exact scope and restart behavior are frozen",
`:5-8`); what must be added is the actual scope (which origins/classes, restart
behaviour, blackout interaction with the ≥10-day window semantics owned by
P5-04). The rollback "procedure" is one step (`:20`), not a runbook. The drill
*spec* format (expected pre/post manifest format, pass/fail criteria) is named
in the task but only sketched at `:15-16`. Estimate: **NO SOURCED ESTIMATE**.

### 2.10 P2-11 — incident and contamination runbook — EXISTS — PARTLY SATISFIES

Contract: "resource/SLO vs. security-boundary classification; CONTAMINATED
response (kill lab workloads, preserve evidence, DISARM, notify owner,
revoke/rotate TESTNET credentials, prohibit bridge resume until clean
reprovision/migration); provider-panel-action branch covering Kodee
snapshot/restore/reboot/firewall/service action, P5-04 reset/reclassification,
master stop for unexplained action; incident drill record (table-top with hashed
outcome)" (`EXECUTION_TASKS:178-187`).

What exists: `recovery/INCIDENT_RESPONSE.md` — the two classifications (`:3-7`,
`:9-22`); the eight-step CONTAMINATED response including human-controlled DISARM,
credential revocation **by name**, resume prohibition, and
reprovision/migration requirement (`:13-22`) — so the Stop condition "CONTAMINATED
response omits credential revocation" is not met, i.e. satisfied; the
provider-panel branch with P5-04 reset and the unexplained-action master stop
(`:24-29`); the evidence record fields (`:31-35`).

Gap / what remains: (1) the **tabletop drill record with hashed outcome is
OPEN** (`:36-37`) — the contract's last required element does not exist; what it
must contain: scenario, expected vs. actual classification, per-step actions,
outcome hash, no private identifiers. (2) The provider branch is generic
"provider-panel"; the task text names **Kodee** explicitly (`EXECUTION_TASKS:186`,
Phase-7 note `:691-693`) — a one-line naming reconciliation, not a structural
gap. Estimate: **NO SOURCED ESTIMATE**.

## 3. R32 / P2-09 — what the rehearsal requires, and its current verdict

The task contract (`EXECUTION_TASKS:158-167`): a **named executor and a named
independent verifier recorded before execution**; checksum/signature
verification; rehearsal **on an expendable clean environment** — candidates
"Hyper-V, VirtualBox, QEMU VM, or separately authorized scratch VPS" — producing
the expected manifest **without secrets**; verdict `VERIFIED` or
`BLOCKED/UNVERIFIED`; if no environment, record BLOCKED/UNVERIFIED and carry it
into Phase 3. Stop conditions include any manual undocumented step,
non-idempotent result, missing checksum, unexplained drift, no expendable
environment, or **active KVM2 proposed as host**.

The frozen specification already exists: Matrix B of
`rehearsals/STAGING_MATRIX.md` — 14 ordered cases on a named-and-recorded
Ubuntu 24.04 environment class (`:30-53`): image/provenance and Python 3.12
source verification, external payload build from a clean exact-SHA checkout,
manifest hash recording, installer dry-run then exactly one disposable install
with the service still masked/disabled/inactive/secret-free, locked-wheel venv
proof, users/paths/modes/no-symlink verification, rendered unit hash, UFW
SSH-only and loopback assertions without firewall mutation, structural/full
tests without starting the service, WAL bundle cases, idempotent re-verification
and fail-closed mismatch cases, rollback in a disposable stopped setup, and
environment teardown/record (`:34-53`), with active KVM2, broker/exchange
calls, secrets, first start, cutover, ARM, firewall mutation and mainnet
deliberately excluded (`:55-57`).

Current record: verdict **BLOCKED / UNVERIFIED** (2026-07-26) — "No expendable
Ubuntu 24.04 environment was named or used… This record cannot be cited as
reproducibility proof" (`rehearsals/summaries/P2_09_REPRODUCIBILITY.md:3-12`).
The same environment class is the recorded blocker on the Gate-A line: "Gate A
remains BLOCKED solely because no named/reachable expendable Ubuntu 24.04
staging host exists; active KVM2 forbidden" (`GLOBAL_HANDOFF.md:2404`).

Two sequencing facts the Lead should carry into any future R32 dispatch:
- No Gate-A result transfers to a new candidate ("No A-0..A-9 PASS transfers",
  `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:234`; the old candidate's
  pass is explicitly inputs/templates only,
  `DEPLOY_WORK_BREAKDOWN_2026-08-15.md:47`).
- The plan-authority reconciliation flags the P2-09-versus-Gate-A ordering as
  unresolved: under the cumulative reading the P2-09 rehearsal "must occur only
  now [after Gate A] and must be expressly included within the one named Gate-A
  staging action (or be covered by a new owner reconciliation)"
  (`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:124`), and names false
  deduplication between similarly named evidence as the principal risk of the
  combined programme (`:138`).

**Explicit statement required by the lane: the P2-09 rehearsal is NOT authorized
and is NOT being requested here.** This lane named no executor, named no
verifier, provisioned or contacted no environment, and ran nothing. Executing
R32 requires a separate owner/Lead authorization, a named expendable
environment, and the executor/verifier recording above; until then the honest
verdict remains BLOCKED / UNVERIFIED and P2-12 may not treat it as VERIFIED.

## 4. Mainline vs Gate-A candidate — what `2ce41e34` has that HEAD lacks

`2ce41e34` is the "Gate-A staging-accepted candidate"
(`BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:37`); it "was installed/executed
on the disposable Gate-A staging host and passed A-0..A-9 under the recorded
boundary" (`:164-166`), while the acceptance "denies merge/live/ARM/order
authority" (`:53`). It is **not** an ancestor of HEAD (merge-base
`4d2228cf…`). `git diff 2ce41e34 25564449` over `IBKR_PAPER_BRIDGE/` shows the
Gate-A line carrying, and HEAD lacking:

1. **Start-mode env-override rejection** — README section "Start mode is
   unit-owned, not env-owned" (removed at HEAD), the
   `MTC_BRIDGE_START_MODE=` env-file rejection in `verify.sh` (removed at HEAD),
   and the matching env-template note (removed at HEAD).
2. **Unit-pinned DISARMED mode** — the
   `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` line in the
   first-start unit template plus its `verify.sh` needle assertion (both removed
   at HEAD).
3. **package.sh build-determinism hardening** (~88 lines removed at HEAD): the
   `core.autocrlf=false core.eol=lf tar.umask` archive pins, GNU-toolchain
   checks, the exported-inventory-and-sizes match against
   `git ls-tree -rz --long`, and the CR-byte checks over LF-required files.
4. **Fail-closed writable-path audit** in `lib/common.sh` (HEAD keeps the weaker
   `|| true` variant).
5. **`wal_state_bundle.py` WAL-capture fixes** — commits `f1ac2565`,
   `df00634f`, `7aad0377`; HEAD lacks 162 lines of that work (§2.6).
6. **Expanded deployment/WAL test suites** — Gate-A adds fail-closed
   writable-tree/package/CR/locale/tar-umask/start-mode tests and
   schema-attachment, hot-WAL/WAL-index, damaged-header and concurrent-writer
   tests, with blob identities recorded
   (`BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:76-77`).

Conversely, **HEAD alone has** `deploy/linux/SECURITY_BASELINE.md` (299 lines:
WP-I pre-Gate-A pinned inventory, content-redacted secret-scan result,
outbound-network inventory; new-file in the same diff,
`deploy/linux/SECURITY_BASELINE.md:44-49`). The integration design already
prescribes the merge that reunifies both sides under a 33-path blob fence —
that is catalogue rows R03–R08, not this lane
(`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:43-47`;
`BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:76-90`).

Relevance to R31 specifically: items 1–5 are implementation bytes behind the
P2-02/P2-04/P2-06 *contracts*, not the design documents. The Phase-2 artifacts
close against whichever candidate the owner's plan authority eventually binds —
and the KVM2_PROGRAM documents themselves are identical on both lines (§1).

## 5. Remaining-work estimates

### 5.1 Per artifact

Standing rule applied: a sourced range or an explicit `NO SOURCED ESTIMATE`,
never an invented figure. **Every one of the ten artifacts, and R32, is
`NO SOURCED ESTIMATE`.** No document read in this lane prices any subset of the
Phase-2 design work: the work breakdown itself records R31/R32 as such
(`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:70-71`), and the only KVM2-adjacent hour
figures in the corpus are the ones §5.2 shows are already assigned elsewhere.
What would settle each: a Lead-scoped write/validation contract per artifact
(producer, allowlist, evidence grammar) plus one timed execution — the same
settler the catalogue names for R27 ("Estimate each artifact after its
write/validation contract is frozen", `DEPLOY_WORK_BREAKDOWN_2026-08-15.md:66`)
and for R32 ("Produce a frozen rehearsal command/environment contract and time
it", `:71`).

Qualitative remaining-work drivers, per artifact (no hours implied):

| Artifact | Doc-side gap | Blocked-on / owner-side |
|---|---|---|
| P2-01 | enumerate packages/users/services per profile | package rows need P2-02 OS inputs; mechanical diff lands in P2-09/final build |
| P2-02 | repair stale "uncommitted" reason; freeze per-row producer contract | release identity (R03–R08) and Ubuntu environment (P2-09/P3-03) |
| P2-03 | bind denial checks into execution matrices | execution is install-time (R37) / Phase-6 |
| P2-04 | add resource-slice decision+spec; drill-spec detail for P2-10 overlap | rendered hashes need candidate; forced-rotation is P4-07 |
| P2-05 | add owner/issuer/revocation-procedure fields | wallet deferred by D4 |
| P2-06 | write the D5 fresh-reset preserve-or-block contract; refresh stale status | RPO/RTO + archive sub-question are owner decisions; WAL fixes ride the merge (R04) |
| P2-07 | assemble around owner recordings | all recordings OPEN (owner) |
| P2-08 | cross-check categories vs profile diff | inventory populates only via Phase 6/7 admissions |
| P2-09 | freeze executor/verifier/environment record | environment + authorization (not requested) |
| P2-10 | specify unattended-upgrades scope/config; expand rollback runbook | drill execution is P4-07A |
| P2-11 | write the tabletop drill record (hashed outcome); name Kodee | drill needs its own authorization context |

### 5.2 Sourced ranges that must NOT be booked to R31/R32

To prevent double-booking (the catalogue's own overlap-removal discipline,
`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:161-183`):

- **2–4 h** — KVM2 baseline+install bundle, deliberately assigned to *neither*
  R29 nor R37 (`:68-69,76`).
- **5–9 h** — fresh candidate-bound staging A-0..A-9 = R08 (`:47`). Its shape
  overlaps P2-09's Matrix B but is a distinct candidate-bound contract; treating
  one as the other is the exact false-deduplication risk the reconciliation
  names (`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:138`).
- **3–6 h / 1.5–3 h / 1–2 h** — operations package / cutover / first start =
  R41 / R42 / R44 (`:80-83`).
- **21–41 h and 16–34 h** — integration end-to-end subtotals covering R04–R08
  (`BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:300-301`).
- **55–105 h** — the withdrawn synthesis total, explicitly not used
  (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:162-165`).

## 6. Consistency notes for the Lead (no write performed)

1. `STATE_CONTINUITY.md:3-5` predates D5 ("start clean") and still marks the
   fresh reset "not selected" — needs a plan-maintenance update under separate
   write authorization, preserving the preserve-or-block obligation
   (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:98-107`).
2. `TRUSTED_INPUTS.md:22` carries the stale "batch is uncommitted" reason (the
   2026-07-26 batch is committed as `6fe0130f`); status OPEN remains correct.
3. `INDEX.md`/`READINESS_STATUS.md` are dated 2026-07-26 and predate D1–D5; their
   P3-01 row ("OPEN") is superseded-in-part by D5 for the *cutover* choice while
   the R34 owner row remains open in the catalogue (`:73`).
4. `deploy/linux/README.md:4,118-120` says nothing there "has been executed on
   any host" — true of HEAD's bytes; the Gate-A line's bytes were executed and
   accepted on the disposable staging host, and the integration design already
   prescribes the time-scoped rewrite for the merged README
   (`BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:90,164-166`).

## 7. Boundary statement

This lane performed no host, network, SSH, deployment, service, credential,
broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading,
merge-to-master, push, or economic action; no product code changed; no
acceptance or authorization is granted or implied by anything above. No other AI
CLI or agent was invoked. The repository was treated read-only; exactly one
output file was written: this one.
