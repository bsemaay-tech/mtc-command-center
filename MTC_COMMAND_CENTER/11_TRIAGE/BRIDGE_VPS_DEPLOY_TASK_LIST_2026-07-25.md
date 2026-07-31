# Bridge VPS Deploy Task List

- Date: 2026-07-25
- Status: **BLOCKED / preparation only**
- Scope: durable planning and handoff only; this file grants no execution authority.

## Dated readiness snapshot

The Hostinger KVM2 VPS baseline is **READY** for a future, separately approved
deployment:

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

## Current bridge and release identity

These are 2026-07-25 snapshot facts and must be verified again before any future
action:

- `origin/master` and the clean active Windows runtime worktree `C:\P2RT` are at
  exact commit `008e065e8e0ffa68f46134da6698d58f91ef2dcb`.
- The Windows task/runtime is running and `127.0.0.1:8790` is listening. Runtime
  state is deliberately **unknown and possibly ARMED**; do not infer DISARMED from
  this handoff.
- PR #25 is open and unmerged at
  `cfb08b819aa9890725344e8315571299718cd554`.
- Local `C:\TSP1001` is at
  `e19471e1cb5dd5573a6e85cb4473bc184a2dd71f` and is unpublished.
  TS-P1-001 remains **PROPOSED**, and no accepting independent audit was supplied
  for that commit.
- The dirty main worktree is forbidden as a deployment source.

There is therefore no canonical, clean, merged, independently accepted deployment
SHA today.

## Independent audit stop

The independent 2026-07-25 exact `gpt-5.6-sol` `xhigh` Gate-5/Gate-6 verdict is:

**BLOCK — zero optional nits.**

Opus 5 availability was confirmed, but the audit attempt reached subscription HTTP
429 before a verdict. A fresh exact `claude-opus-5` `xhigh`, no-fallback,
no-resume audit is deferred until credits/session capacity returns. The failed
attempt is not audit evidence and must not be presented as a review result. No
repository audit-report file exists for this session verdict, so none is invented
or cited here.

## Blocking findings

Deployment remains blocked for all of the following reasons:

1. There is no canonical audited deploy SHA containing the required TS-P0 baseline
   plus accepted Linux deployment repairs.
2. The current Ubuntu direction depends on global pip and unpinned dependencies,
   so the environment is neither reproducible nor safely rollbackable.
3. The proposed root-owned systemd service lacks adequate hardening, privilege
   separation, restart throttling, and explicit state/log ownership.
4. Starting with a fresh database can reset daily-loss and consecutive-loss
   evidence and can ignore positions created by a foreign/previous host.
5. The active Windows runtime is still a writer. Starting the VPS before a proven
   cutover would create a dual-writer risk.
6. The unauthenticated control API must remain loopback-only and reachable only
   through an SSH tunnel; it is not safe for direct public exposure.
7. Release identity, rollback evidence, backup/restore behavior, persistent logs,
   monitoring, and risk-state continuity are incomplete.

## Ordered checklist — complete before deploy

No item below authorizes the next item. Stop at every audit, owner, runtime, and ARM
gate.

1. **[AI: Claude] Produce the exact release candidate.** Start from a clean merged
   release SHA containing accepted TS-P0 work plus the Linux deployment repairs.
   Record the exact SHA and diff, then obtain fresh independent Gate 5 and Gate 6
   acceptance on that immutable candidate. A branch, PR, local commit, builder
   report, or prior audit is not a deploy release.
2. **[AI: Claude] Make Python reproducible.** Use Python 3.12 in an application
   virtual environment. Replace global-pip installation and floating requirements
   with fully pinned, hash-locked dependencies whose clean offline/install
   procedure is tested.
3. **[AI: Claude] Harden the service boundary.** Create a dedicated non-login
   `mtc-bridge` user; use a root-owned immutable release directory; define explicit
   writable state and log directories; and supply a hardened systemd unit with
   least privilege, `network-online` ordering, restart throttling, and graceful
   stop behavior.
4. **[AI: Barış] Provision only a VPS-specific TESTNET agent wallet.** Store it in
   a safe root-owned `0600` environment file or an equivalently protected secret
   mechanism. Put no secret in `.env`, the repository, chat, shell history, or
   plaintext backups. `HL_LIVE_ACK` must be absent.
5. **[AI: Barış] Choose the risk-state continuity policy before implementation.**
   Formally select and test either a WAL-consistent database migration or a
   conservative, explicitly approved fresh-database reset that preserves or blocks
   on lost daily-loss, consecutive-loss, order, and foreign-position evidence.
6. **[AI: Any] Execute no cutover until this exact single-writer proof can be
   followed and recorded in order:** record exact SHA/config; confirm DISARMED;
   obtain a fresh reconcile; capture raw empty positions and raw empty orders; stop
   and disable the Windows task; prove wrapper and child processes are gone and
   port 8790 is closed; revoke the old-host agent; reconfirm raw empty positions and
   orders; only then permit the first VPS service start. Any failed or ambiguous
   check stops the cutover.
7. **[AI: Claude] Keep the control plane private.** Bind only to
   `127.0.0.1:8790` and access it only through an SSH tunnel. Keep UFW limited to
   port 22. Do not publish 8790 and do not add a reverse proxy.
8. **[AI: Claude] Complete operations evidence.** Produce a release/baseline
   manifest, rollback SHA and tested rollback procedure, systemd-unit hash,
   encrypted backups with a restore check, rotated persistent logs, and monitoring
   for health, restart loops, reconciliation freshness, and disk/log growth.
9. **[AI: Any] Pass the exact-SHA test matrices before the first start.** Run the
   complete local offline matrix on the immutable release and then an Ubuntu staging
   matrix. The first VPS start must remain DISARMED, TESTNET-only, loopback-only,
   reconcile-ready, and free of restart loops.
10. **[AI: Barış] Close the final gates.** First obtain a fresh exact
    `claude-opus-5` `xhigh`, no-fallback, no-resume audit of the exact repair
    diff and tests. Then require a separate owner deploy authorization. ARM remains
    another separate, explicit owner action. The monitoring counter of at least
    10 days starts only at the final approved VPS ARM, never at install, deploy,
    first DISARMED start, or migration.

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
- `IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md` (currently in the PR #25
  TS-P0 candidate, not merged into `origin/master`)
- `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md` (currently in the PR #25
  TS-P0 candidate, not merged into `origin/master`)
- `IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md` (currently in the PR #25
  TS-P0 candidate, not merged into `origin/master`)
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
