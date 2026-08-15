# W5 — KVM2 identity and filesystem contracts (gap-only draft)

## 0. Status, source pins, and drafting boundary

This is a **gap-only preparation draft**, not a replacement for the existing
combined contract. P2-03 requires users/groups, login/sudo policy, directories,
ownership, modes, a read-only release path, writable state/log paths, and
explicit cross-user denial tests for both profiles
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:114-118`
@ `01269f56`). The existing
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md`
already supplies the identity baseline, path/mode matrix, service sandbox, and a
denial-check list; the inventory therefore grades P2-03 **EXISTS — LARGELY
SATISFIES AS DESIGN** and identifies the remaining gap as binding and executing
the denial checks (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:135-160`
@ `36e06f92`).

The existing KVM2 programme documents are byte-identical at detached HEAD
`25564449` and Gate-A candidate `2ce41e34`; the candidate contributes
implementation bytes rather than a newer identity/filesystem design
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:29-37,470-473`
@ `36e06f92`). The existing kit has builder self-QA only, no independent audit
verdict, and open final acceptance
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:38-54`
@ `36e06f92`). Nothing below changes that state.

Source-version convention used below:

- `@ 25564449` means the detached mainline bytes examined by the inventory
  (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:5-9`
  @ `36e06f92`).
- `@ 2ce41e34` means the Gate-A candidate bytes named by the inventory
  (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:5-7`
  @ `36e06f92`).
- The candidate's relevant improvement is a fail-closed writable-path audit;
  mainline retains the weaker error-swallowing variant
  (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:429-452`
  @ `36e06f92`; `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:95-104`
  @ `2ce41e34`). This draft requires the candidate's fail-closed semantics but
  does not select, merge, or accept a release candidate.

## 1. Identity contract — gap-closing addendum

### 1.1 What it governs

This contract governs the bridge service user and group, login and privilege
boundaries, the identity declared by the service unit, the presence or absence
of lab identities in each machine profile, and negative proof that a lab or
other non-bridge identity cannot read protected bridge material or control the
bridge service. Those are the identity portions of the P2-03 evidence and stop
condition (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:114-118`
@ `01269f56`).

### 1.2 Exact required end state

#### Shared bridge identity baseline

1. A dedicated system user `mtc-bridge` and primary group `mtc-bridge` exist.
   The account home is `/var/lib/mtc-bridge`; its shell is a non-login shell; it
   has no sudo, admin, Docker, journal-reader, or other privileged supplementary
   group (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:3-8`
   @ `25564449`).
2. The first-start unit runs as `User=mtc-bridge` and `Group=mtc-bridge`, from
   the exact-SHA release and venv paths
   (`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:29-34`
   @ `2ce41e34`).
3. The bridge account has no login or sudo path. An existing account with
   different primary group, home, shell, or prohibited group membership is a
   hard failure, not an account to repair silently
   (`IBKR_PAPER_BRIDGE/deploy/linux/install.sh:198-214,221-250`
   @ `25564449`).

#### Profile-specific end state

| Profile | Required identity state | Required denial result |
|---|---|---|
| `temporary-testnet-lab`, before any later lab admission | `mtc-bridge` exists as above. `ai-lab`, lab child processes, and all other lab identity/package/service/credential surfaces are absent; laboratory admission is optional and deferred (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rebuild/profiles/temporary-testnet-lab.md:7-26` @ `25564449`; `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rebuild/profiles/PROFILE_DIFF.md:3-9` @ `25564449`). | The absence checks pass. The cross-user read/control probe is recorded **BLOCKED / UNVERIFIED — lab identity not admitted**, not falsely marked PASS; the existing contract says no lab identity or child process exists in the batch (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:33-40` @ `25564449`). |
| `temporary-testnet-lab`, only if a later admission is separately opened | Before admission is accepted, the named lab identity is not a member of `mtc-bridge` or a privileged/control-capable group and receives no bridge service-control authority. | Acting as that exact lab identity, attempts to read the env file, state, raw logs, or release-private material; to write any bridge path; and to control the bridge unit all fail. These are the existing required denials, not new permissions (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:33-40` @ `25564449`). |
| `future-trading-only` | `mtc-bridge` exists as above; no lab user, lab home, agent, runner, browser automation, container storage, workflow runner, lab scheduler, lab credential, cached lab data, lab package state, or lab snapshot exists (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rebuild/profiles/future-trading-only.md:7-17` @ `25564449`). | The profile inventory proves every lab identity and lab-owned surface absent. Any non-bridge identities that remain after the final user/group inventory must pass the same protected-read, write, and service-control denials; the exact remaining identity set is currently **UNKNOWN** because no per-profile user/group inventory exists (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:86-95` @ `36e06f92`). |

### 1.3 How the state is verified

The executable proof is a named, profile-specific case set. Each case records
the profile, exact source SHA, named expendable environment, named executor,
named independent verifier, expected result, actual result, return code or
equivalent machine result, and a content-free evidence hash. The source rehearsal
contract requires a named executor/verifier and named expendable environment,
with secrets excluded and an honest `VERIFIED` or `BLOCKED/UNVERIFIED` verdict
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:376-386`
@ `36e06f92`; `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rehearsals/STAGING_MATRIX.md:30-57`
@ `25564449`).

Required cases:

| Case | Pass condition | Present implementation coverage |
|---|---|---|
| ID-01 — service identity | `mtc-bridge` exists; its primary group is `mtc-bridge`; home is `/var/lib/mtc-bridge`; shell is non-login. | Installer validates all four attributes (`IBKR_PAPER_BRIDGE/deploy/linux/install.sh:198-214,221-250` @ `25564449`). `verify.sh` currently rechecks existence, shell, and primary group, but not the home (`IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:54-75` @ `2ce41e34`). The verifier-side home assertion is therefore part of this gap. |
| ID-02 — privileged groups | `mtc-bridge` has no prohibited supplementary group. | Current installer/verifier explicitly reject `sudo`, `admin`, `docker`, `adm`, and `systemd-journal` (`IBKR_PAPER_BRIDGE/deploy/linux/install.sh:212-214` @ `25564449`; `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:68-72` @ `2ce41e34`). The complete OS/profile-specific privileged-group universe is **UNKNOWN**; settle it by freezing the P2-01 user/group inventory and the prohibited-group list for the selected Ubuntu image before rehearsal (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:86-97` @ `36e06f92`). |
| ID-03 — login and sudo denial | Interactive login as `mtc-bridge` fails, and the account cannot obtain sudo/admin execution. | The design requires login denial, but no executed result exists (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:33-40` @ `25564449`; `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:151-160` @ `36e06f92`). Exact command grammar is **UNKNOWN**; settle it in the frozen P2-09/P4-02 verification harness and record expected/actual results. |
| ID-04 — unit identity | The rendered unit contains `User=mtc-bridge` and `Group=mtc-bridge`, is bound to the exact release, and exactly matches the accepted template. | The template declares the identity and exact-SHA paths (`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:29-34` @ `2ce41e34`); `verify.sh` checks the user, exact release/venv references, and exact template bytes (`IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:155-195` @ `2ce41e34`). An explicit verifier needle for `Group=mtc-bridge` is **ABSENT** from that list; add it to the future harness or record an equivalent parsed assertion. |
| ID-05 — profile identity inventory | The recorded user/group inventory matches the selected profile exactly; `temporary-testnet-lab` has no lab identity before admission, and `future-trading-only` never has one. | Mechanical per-profile inventories are required but not yet populated (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rebuild/profiles/PROFILE_DIFF.md:18-20` @ `25564449`; `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:86-95` @ `36e06f92`). Verdict remains **BLOCKED / UNVERIFIED** until they exist. |
| ID-06 — cross-user denial | For each identity required by the selected profile, all applicable protected-read, bridge-write, and service-control probes have the expected denial result; absence-only cases prove the forbidden identity is absent. | The denials are specified but not executed, and the inventory explicitly assigns their binding to P2-09/P4-02 (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:151-160` @ `36e06f92`). |

### 1.4 What constitutes a violation

Any of the following is a contract violation: wrong/missing service user or
primary group; a login-capable shell; wrong home; any prohibited supplementary
group; unit user/group drift; a lab identity present where the profile forbids
it; a lab/non-bridge identity able to read protected bridge material, write a
bridge path, or control the unit; an undocumented identity; a denial test that
unexpectedly succeeds; or an unexecutable/missing denial test presented as PASS.
The P2-03 stop condition is specifically that a lab identity can read or control
bridge material (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:114-118`
@ `01269f56`). A violation or incomplete evidence yields
**BLOCKED / UNVERIFIED**, never acceptance.

### 1.5 Identity UNKNOWNs that block a complete proof

1. **UNKNOWN — exact per-profile user/group inventory.** Only `mtc-bridge` is
   enumerated today. Settle it by producing and mechanically diffing the P2-01
   inventories (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:86-95`
   @ `36e06f92`).
2. **UNKNOWN — complete privileged-group denylist.** Existing code names five
   groups while the design also forbids any other privileged supplementary
   group (`IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:68-72` @ `2ce41e34`;
   `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:5-8`
   @ `25564449`). Settle it against the selected OS image's frozen group and
   privilege inventory.
3. **UNKNOWN — exact cross-user probe identity and executable command grammar.**
   No lab identity exists in the current batch and no source supplies the exact
   probe commands (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:33-40`
   @ `25564449`). Settle it with a Lead-scoped P2-09/P4-02 harness that names the
   probe identity, commands, expected denials, and evidence grammar; the
   inventory identifies this harness binding as remaining work
   (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:151-160`
   @ `36e06f92`).

### 1.6 Identity out of scope

Lab admission, identity creation on a host, service start/control, credential
provisioning, broker/exchange contact, ARM, orders, deployment, cutover,
TESTNET/mainnet execution, acceptance, and authorization are out of scope for
this preparation draft (`C:\tmp\lane_kick\W5.md:45-49`). The owner has also
deferred the KVM2-specific wallet; no key may be requested, generated, stored,
or referenced by value (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:80-87`
@ `e0529896`).

## 2. Filesystem contract — gap-closing addendum

### 2.1 What it governs

This contract governs the canonical release, venv, state, log, configuration,
environment, manifest, unit, mask, and logrotate paths; their ownership, modes,
symlink rules, immutable-content rules, writable-surface boundary, and
cross-user read/write denials. These are the filesystem portions of P2-03
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:114-118`
@ `01269f56`).

### 2.2 Exact required end state

The following matrix is the required installed-state contract. It makes the
existing combined matrix concrete with the actual Linux installer and templates.

| Path | Required owner:group | Required mode/state | Writable by bridge service? | Source |
|---|---|---|---|---|
| `/opt/mtc-bridge/releases/<exact-40-hex-sha>/` | `root:root`, recursively | directories `0555`; executable files `0555`; non-executable files `0444`; ordinary directories/files only; exact `RELEASE_SHA256SUMS` inventory; no write bit anywhere | No | `IBKR_PAPER_BRIDGE/deploy/linux/README.md:33-39,51-53` @ `2ce41e34`; `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:263-278,312-328` @ `25564449` |
| `/opt/mtc-bridge/venvs/<exact-40-hex-sha>/` | `root:root`, recursively | directories `0555`; executable files `0555`; non-executable files `0444`; no write bit anywhere | No | `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:280-328` @ `25564449` |
| `/var/lib/mtc-bridge/` | `mtc-bridge:mtc-bridge` | directory `0750`; canonical state DB `/var/lib/mtc-bridge/bridge.db` | Yes | `IBKR_PAPER_BRIDGE/deploy/linux/README.md:40-45` @ `2ce41e34`; `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:14-19` @ `2ce41e34` |
| `/var/log/mtc-bridge/` | `mtc-bridge:mtc-bridge` | directory `0750`; rotated log files created `0640 mtc-bridge:mtc-bridge` | Yes | `IBKR_PAPER_BRIDGE/deploy/linux/README.md:40-45` @ `2ce41e34`; `IBKR_PAPER_BRIDGE/deploy/linux/logrotate/mtc-bridge:13-25` @ `25564449` |
| `/etc/mtc-bridge/` | `root:root` | directory `0750` | No | `IBKR_PAPER_BRIDGE/deploy/linux/README.md:40-45` @ `2ce41e34`; `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:252-260` @ `25564449` |
| `/etc/mtc-bridge/mtc-bridge.env` | `root:root` | regular file `0600` | No | `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:330-341` @ `25564449`; `IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template:1-10` @ `2ce41e34` |
| `/etc/mtc-bridge/install_manifest.json` | `root:root` | regular file `0640` | No | `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:399-428` @ `25564449` |
| `/usr/local/lib/systemd/system/mtc-bridge-first-start.service` | `root:root` | regular file `0644`; exact rendered bytes for `<exact-40-hex-sha>` | No | `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:343-360` @ `25564449` |
| `/etc/systemd/system/mtc-bridge-first-start.service` | systemd mask | the one intentional symlink: resolves exactly to `/dev/null` | No | `IBKR_PAPER_BRIDGE/deploy/linux/README.md:46-48` @ `2ce41e34`; `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:201-205` @ `25564449` |
| `/etc/logrotate.d/mtc-bridge` | `root:root` | regular file `0644`; frozen policy bytes | No | `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:381-384` @ `25564449` |

All canonical paths other than the explicit systemd mask above must not be
symlinks. The installed release must contain exactly the hash-bound payload and
no injected file; the venv must match the fully hashed lock
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:23-26`
@ `25564449`; `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:45-52,77-121`
@ `2ce41e34`).

The service's filesystem view is read-only under `ProtectSystem=strict`; its only
declared writable paths are `/var/lib/mtc-bridge` and `/var/log/mtc-bridge`.
`NoNewPrivileges=yes`, empty capability sets, `ProtectHome=yes`, and the other
unit restrictions remain part of the hashed unit
(`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:63-93`
@ `2ce41e34`). No additional writable bridge path is permitted by either machine
profile; the profile diff says state and logs only for both
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rebuild/profiles/PROFILE_DIFF.md:3-16`
@ `25564449`).

### 2.3 How the state is verified

The filesystem cases below are appended to the same profile-specific evidence
record defined in §1.3. The existing Ubuntu rehearsal matrix already requires
verification of users, groups, paths, ownership, modes, no symlinks, immutable
trees, rendered unit hardening, fail-closed mismatch cases, and idempotent
re-verification (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rehearsals/STAGING_MATRIX.md:30-53`
@ `25564449`).

| Case | Pass condition | Present implementation coverage / remaining gap |
|---|---|---|
| FS-01 — canonical path type | Every matrix path exists with the required file/directory type; no canonical path is a symlink except the exact `/dev/null` systemd mask. | `verify.sh` rejects symlinks for its canonical-path list and separately checks the mask (`IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:45-52,201-205` @ `25564449`). Record one result per matrix path; a missing result is not PASS. |
| FS-02 — owner and mode | Every matrix row has the exact owner/group and mode; release and venv ownership/modes are verified recursively, not only at the root. | `verify.sh` checks root modes/owners for release, venv, state, log, config, env, and install manifest (`IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:77-128` @ `2ce41e34`). The install seals release/venv ownership and modes recursively (`IBKR_PAPER_BRIDGE/deploy/linux/install.sh:312-328` @ `25564449`). Exact verifier coverage for recursive owner/mode, the real unit's `0644 root:root`, logrotate's `0644 root:root`, and rotated log files is **ABSENT** from the cited verifier; add these assertions to the future harness or record equivalent machine evidence. |
| FS-03 — immutable inventory | Release marker equals the named SHA; manifest hash equals the separately supplied SHA-256; all payload hashes pass; actual inventory exactly equals `RELEASE_SHA256SUMS`; release and venv contain no writable node. | Current verifier covers these assertions (`IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:77-121` @ `2ce41e34`). Writable-path enumeration must use the candidate's fail-closed behavior: an inventory error is FAIL, not an empty success (`IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:95-104` @ `2ce41e34`). |
| FS-04 — service write boundary | Acting as the service identity, create/write/rename/delete probes succeed only under `/var/lib/mtc-bridge` and `/var/log/mtc-bridge`; equivalent probes fail for release, venv, config, env, manifest, real unit, mask parent, and logrotate policy. | The unit declares only the two writable paths (`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:63-93` @ `2ce41e34`), but the existing denial checks are unexecuted (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:151-160` @ `36e06f92`). Exact non-starting probe commands are **UNKNOWN**; settle them in the frozen P2-09/P4-02 harness without starting the service. |
| FS-05 — cross-user protected-read denial | For the admitted lab probe identity, reads of env, state, raw logs, and any release-private material fail; for absence-only profiles, the forbidden lab identity and its filesystem surfaces are proved absent. | This is specified by the existing denial list and profile rules but has not been executed (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:33-40` @ `25564449`; `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:151-160` @ `36e06f92`). |
| FS-06 — profile diff | Package, user, service, listener, unit, filesystem, and credential-name inventories mechanically match the selected profile; every undeclared difference blocks. | The profile contract requires the mechanical diff, but the inventories are not yet populated (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rebuild/profiles/PROFILE_DIFF.md:18-20` @ `25564449`; `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:86-95` @ `36e06f92`). |

### 2.4 What constitutes a violation

Any missing path; wrong type, owner, group, or mode; unexpected symlink; mask not
resolving exactly to `/dev/null`; writable release/venv node; injected, missing,
or hash-mismatched release file; wrong release marker; venv/lock drift;
additional service-writable path; protected material readable by the lab probe;
bridge path writable by a non-authorized identity; undeclared profile
difference; or a filesystem-enumeration error treated as PASS is a violation.
The executable verifier is fail-closed and exits non-zero when any assertion
fails (`IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:1-13,246-252`
@ `25564449`). A violation or incomplete case set yields
**BLOCKED / UNVERIFIED**.

### 2.5 Filesystem UNKNOWNs that block a complete proof

1. **UNKNOWN — meaning of “bridge material” for world-readable immutable
   release files.** The P2-03 stop text forbids a lab identity reading or
   controlling bridge material, while the existing release contract sets
   non-executable release files to `0444` and the existing denial list narrows
   its wording to “release-private material”
   (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:114-118`
   @ `01269f56`; `IBKR_PAPER_BRIDGE/deploy/linux/README.md:33-39`
   @ `2ce41e34`; `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:35-40`
   @ `25564449`). The sources do not reconcile whether immutable non-secret
   release code is intended to be lab-readable. Settle this with an explicit
   Lead/owner definition of protected “bridge material” and then freeze the
   corresponding modes or sandbox denial test. Until then, later lab admission
   remains blocked; the temporary profile already defers it pending OS-enforced
   isolation and denial tests
   (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rebuild/profiles/temporary-testnet-lab.md:20-26`
   @ `25564449`).
2. **UNKNOWN — exact recursive owner/mode verifier and cross-user probe
   commands.** The source matrix says what to verify, but does not supply the
   complete executable grammar (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rehearsals/STAGING_MATRIX.md:30-53`
   @ `25564449`). Settle it by freezing the P2-09/P4-02 producer, command,
   expected-result, and evidence contract before execution; the inventory names
   that binding as the P2-03 remaining work
   (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:151-160`
   @ `36e06f92`).
3. **UNKNOWN — final candidate identity.** The Phase-2 documents close against
   whichever candidate the owner's plan authority eventually binds; the current
   programme documents themselves do not select it
   (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:470-473`
   @ `36e06f92`). This draft imports the candidate's fail-closed verification
   semantics only as a required property, not as candidate selection.

### 2.6 Filesystem out of scope

This contract does not execute the installer or verifier, create/change any
path or account, start/unmask/enable/control a service, provision/read a secret,
change a firewall, contact a host or network, migrate/reset state, perform
cutover, or authorize deployment or first start. Phase 2 is preparation only,
with no reprovision or install
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:92-94`
@ `01269f56`). The lane itself excludes every host/network/deployment/service/
credential/trading/economic action, product-code change, acceptance, and
authorization (`C:\tmp\lane_kick\W5.md:45-49`).

The candidate's unit-pinned DISARMED start mode and env-override rejection are
real candidate properties, but start-mode and first-start behavior are outside
this identity/filesystem gap draft
(`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:36-45`
@ `2ce41e34`; `IBKR_PAPER_BRIDGE/deploy/linux/README.md:112-116`
@ `2ce41e34`).

## 3. Required verdict and evidence binding

The identity and filesystem gap can be recorded **VERIFIED** only when every
applicable ID/FS case above has executed on the named expendable environment for
the selected profile, all expected denials have been observed, all mechanical
inventories are present, and the independent verifier confirms the evidence.
If an environment or prerequisite identity is absent, a check cannot execute,
an inventory is missing, an `UNKNOWN` remains material, or any assertion fails,
the only honest result is **BLOCKED / UNVERIFIED**. The existing P2-09 record is
currently BLOCKED/UNVERIFIED because no expendable Ubuntu environment was named
or used, and it cannot be cited as reproducibility proof
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:376-427`
@ `36e06f92`). No rehearsal is requested or authorized here.

## 4. Estimate discipline

**NO SOURCED ESTIMATE.** The work catalogue assigns no sourced estimate to R31
or R32 (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:70-71`
@ `fb0bf496`). The inventory likewise states that every Phase-2 artifact and R32
has no sourced estimate and says the settler is a frozen write/validation
contract plus timed execution, not an invented number
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_REBUILD_KIT_INVENTORY_2026-08-15.md:475-490`
@ `36e06f92`).

## 5. Final boundary statement

This file is design material only. It performs and authorizes no host, network,
SSH, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, product-code,
or economic action; it issues no acceptance or authorization
(`C:\tmp\lane_kick\W5.md:45-49`).
