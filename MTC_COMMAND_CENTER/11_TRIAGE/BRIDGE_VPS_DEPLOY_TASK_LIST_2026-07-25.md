# Bridge VPS Deploy Task List

- Date: 2026-07-25
- Updated: 2026-07-26 first executable preparation batch
- Status: **BLOCKED / preparation only / local candidate uncommitted**
- Scope: durable planning and handoff only; this file grants no execution authority.

## Dated readiness snapshot

The following is the historical 2026-07-25 owner-supplied KVM2 snapshot. It was
not refreshed in this local batch because VPS access was not authorized:

- Ubuntu 24.04, hardened.
- Key-only SSH; root SSH disabled.
- UFW default-deny with only SSH port 22 allowed.
- Fail2ban, automatic security updates, and time synchronization enabled.
- 96G disk and 7.8 GiB RAM.
- Python 3.12 and git present.
- pip, Docker, and the bridge application are absent.
- `/opt` is empty.

This document deliberately contains no public IP, credentials, private-key path,
secret values, or connection command.

KVM2-P1-01/P1-02/P1-03 remain **OPEN / BLOCKED** until a separately authorized
read-only host baseline is reproduced, redacted, and owner-accepted. The dated
snapshot is not current deployment evidence.

## Current bridge and release identity

Current repository facts were verified locally on 2026-07-26. Runtime/VPS facts
remain dated and must be verified under their separate gates:

- `origin/master` and this branch base are exact commit
  `423897b76b32f68cdabcae16b39c078fdd1f67cb`.
- PR #25 is merged. Its TS-P0 baseline and these three canonical contracts are
  present in merged master:
  - `IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md`
  - `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md`
  - `IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md`
- The old “PR #25 contracts absent” Phase-3 blocker is closed.
- Windows runtime/task/listener/writer/ARM/order/position facts were not queried.
  Their state is **UNKNOWN**; no inference from the old snapshot is allowed.
- The dirty main worktree is forbidden as a deployment source.

There is still no committed, immutable, independently accepted Linux deployment
SHA: the current preparation diff is deliberately uncommitted.

## Current implementation and acceptance roster

- Owner-authorized replacement implementer: this one fresh exact
  `gpt-5.6-sol`, effort `xhigh`, sole-writer session.
- Reason: Claude Opus 5 could not run because its monthly usage limit was
  reached. The owner explicitly waived the prior Claude-only implementer
  requirement and authorized Codex or Grok; Codex Lead selected Codex.
- Other writers/models/subagents: none.
- Final acceptance authority: Codex Lead.
- Independent audit status: **OPEN**. This implementer session cannot accept
  its own work and reports only builder self-QA.

The historical 2026-07-25 Codex `BLOCK` and failed Claude attempt remain
historical input only. They are not an audit of the new implementation.

## Blocking findings

Deployment remains blocked for all of the following reasons:

1. TS-P0 is merged, but the Linux preparation diff is uncommitted and has no
   immutable candidate SHA or independent acceptance.
2. Python 3.12 direct inputs and an exact transitive hash lock are prepared
   locally, but P2-09/P3-03 Ubuntu install/reproducibility evidence is absent.
3. Dedicated identity, immutable release/venv paths, hardened first-start and
   separate steady units, log rotation, and fail-closed scripts are prepared
   locally but not rehearsed on Ubuntu.
4. WAL-consistent state tooling and staging cases are prepared. P3-01 owner
   choice is still OPEN; conservative reset is not approved.
5. The Windows writer/runtime is unverified. Starting the VPS before the ordered
   cutover proof would create an unknown/dual-writer risk.
6. The unauthenticated control API must remain loopback-only and reachable only
   through an SSH tunnel; it is not safe for direct public exposure.
7. Release identity, rollback evidence, backup/restore behavior, persistent logs,
   monitoring, and risk-state continuity are incomplete.

## Ordered checklist — complete before deploy

No item below authorizes the next item. Stop at every audit, owner, runtime, and ARM
gate.

1. **[AI: Codex] Produce the exact release candidate.** Start from a clean merged
   release SHA containing accepted TS-P0 work plus the Linux deployment repairs.
   Record the exact SHA and diff, then obtain fresh independent Gate 5 and Gate 6
   acceptance on that immutable candidate. A branch, PR, local commit, builder
   report, or prior audit is not a deploy release. **Current: local preparation
   complete; commit/audit/acceptance OPEN.**
2. **[AI: Codex] Make Python reproducible.** Use Python 3.12 in an application
   virtual environment. Replace global-pip installation and floating requirements
   with fully pinned, hash-locked dependencies whose clean offline/install
   procedure is tested. **Current: local lock and enforcement prepared; Ubuntu
   install remains BLOCKED/UNVERIFIED.**
3. **[AI: Codex] Harden the service boundary.** Create a dedicated non-login
   `mtc-bridge` user; use a root-owned immutable release directory; define explicit
   writable state and log directories; and supply a hardened systemd unit with
   least privilege, `network-online` ordering, restart throttling, and graceful
   stop behavior. **Current: structural assets prepared; Ubuntu verification
   and independent acceptance OPEN.**
4. **[AI: Barış] Provision only a VPS-specific TESTNET agent wallet.** Store it in
   a safe root-owned `0600` environment file or an equivalently protected secret
   mechanism. Put no secret in `.env`, the repository, chat, shell history, or
   plaintext backups. `HL_LIVE_ACK` must be absent.
   **[owner decision 2026-08-15 night] DEFERRED — "this we will do later".**
   Record: `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md` §D4. This item stays OPEN and
   continues to block the first start. No agent may request, generate, store, or
   reference a key value, and no later step may proceed past the point that
   requires the wallet.
5. **[AI: Barış] Choose the risk-state continuity policy before cutover.**
   Formally select and test either a WAL-consistent database migration or a
   conservative, explicitly approved fresh-database reset that preserves or blocks
   on lost daily-loss, consecutive-loss, order, and foreign-position evidence.
   ~~**Current: OPEN; WAL is recommended and supported, not approved.**~~
   **[owner decision 2026-08-15 night] DECIDED: conservative fresh-database
   reset — "start clean".** This is a deliberate owner override of the
   recommendation; WAL migration was recommended and supported and was not
   chosen. Record: `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md` §D5. The
   "preserves or blocks on" clause of this item is **not** waived by the choice:
   a fresh reset must still be proven either to carry the daily-loss,
   consecutive-loss, order and foreign-position evidence forward in some
   retrievable form, or to refuse to start rather than silently lose it. Start
   clean is not start blind. The item-6 single-writer cutover proof is unchanged.
   **Open sub-question returned to the owner:** whether the pre-cutover risk
   state is archived off-host before the fresh start or left on the old machine;
   the Lead recommends archiving, as it is the only record of the paper period.
6. **[AI: Barış] Execute no cutover until this exact single-writer proof can be
   followed and recorded in order:** record exact SHA/config; confirm DISARMED;
   obtain a fresh reconcile; capture raw empty positions and raw empty orders; stop
   and disable the Windows task; prove wrapper and child processes are gone and
   port 8790 is closed; revoke the old-host agent; reconfirm raw empty positions and
   orders; only then permit the first VPS service start. Any failed or ambiguous
   check stops the cutover.
7. **[AI: Codex] Keep the control plane private.** Bind only to
   `127.0.0.1:8790` and access it only through an SSH tunnel. Keep UFW limited to
   port 22. Do not publish 8790 and do not add a reverse proxy. **Current:
   loopback/UFW assertions and unit hardening are locally covered; no host or
   listener was accessed.**
8. **[AI: Codex] Complete operations evidence.** Produce a release/baseline
   manifest, rollback SHA and tested rollback procedure, systemd-unit hash,
   encrypted backups with a restore check, rotated persistent logs, and monitoring
   for health, restart loops, reconciliation freshness, and disk/log growth.
   **Current: preparation templates/scripts/docs exist; release hashes, Ubuntu
   rollback, off-host backup/restore and monitoring evidence remain OPEN.**
9. **[AI: Codex] Pass the exact-SHA test matrices before the first start.** Run the
   complete local offline matrix on the immutable release and then an Ubuntu staging
   matrix. The first VPS start must remain DISARMED, TESTNET-only, loopback-only,
   reconcile-ready, and free of restart loops. **Current: local builder self-QA
   passed 58 targeted tests and the 276-test full suite from both supported
   working directories; Git Bash syntax passed. No committed exact SHA or Ubuntu
   environment exists, so item 9 remains OPEN/BLOCKED.**
10. **[AI: Barış] Close the final gates.** Obtain a fresh independent audit of
    the exact candidate diff/tests under the current owner-authorized roster;
    Codex Lead remains final acceptance authority. The replacement implementer
    cannot self-accept. Then require a separate owner deploy authorization. ARM
    remains another separate, explicit owner action. The monitoring counter of
    at least 10 days starts only at the final approved VPS ARM, never at install,
    deploy, first DISARMED start, or migration.

## Safety boundaries

Capturing this task authorizes **no** merge, deployment, package installation,
secret creation or transfer, runtime API call, scheduler or process action,
broker/exchange action, TESTNET action, or ARM action. It authorizes no access to or
mutation of `C:\P2RT`. Mainnet is forbidden.

Any future executor must keep the control API unauthenticated only because it is
strictly loopback-bound and reached through an SSH tunnel. If that network boundary
cannot be proven, stop.

## Canonical repo references

- `IBKR_PAPER_BRIDGE/docs/17_DEPLOYMENT.md`
- `IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md` (merged via PR #25)
- `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md` (merged via PR #25)
- `IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md` (merged via PR #25)
- `IBKR_PAPER_BRIDGE/deploy/linux/README.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/INDEX.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP0_DOC_CLOSEOUT_REPORT_2026-07-20.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/FABLE_TSP0_BLOCK_REPAIR_AUDIT_2026-07-20.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP1001_REAUDIT2_2026-07-21.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`

## Future-chat pickup

Read this task first, then read the current
`MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` and
`MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`. Verify all branch, PR, SHA, VPS,
Windows runtime, broker/exchange, reconcile, order, position, port, and audit state
live because these dated notes can drift. Preserve the dirty-main-worktree ban and
single-writer invariant. Stop at every independent-audit and owner gate; do not
infer merge, deploy, TESTNET, secret-transfer, runtime, or ARM authority from this
handoff.
