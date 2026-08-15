# Lane W8 — KVM2 recovery, teardown, maintenance, incident contracts (input to R31)

- Lane output for the Lead and the owner. **Not a gate verdict, not an acceptance,
  not an authorization.** These are contract drafts only; Phase 2 is "Preparation
  artifacts only; no reprovision or install"
  (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:92-94`,
  below `EXECUTION_TASKS`).
- Repository `C:\RO` treated as read-only, shared with other lanes; no Git command
  that takes the index lock was run; nothing in the repo was written. This file is
  the lane's only output.
- Sources, all read first-hand: `EXECUTION_TASKS`;
  `DEPLOY_WORK_BREAKDOWN_2026-08-15.md` (below `BREAKDOWN`);
  `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md` (D4/D5);
  `BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md` (the deploy list, below
  `READINESS`); the five existing artifacts
  `KVM2_PROGRAM/recovery/{STATE_CONTINUITY,ACCESS_RECOVERY,TEARDOWN_AND_REPROVISION,MAINTENANCE,INCIDENT_RESPONSE}.md`;
  and the three implementation anchors `IBKR_PAPER_BRIDGE/deploy/linux/install.sh`,
  `rollback.sh`, `logrotate/mtc-bridge`.
- Method: same as the other Phase-2 drafting lanes — task-contract cites for every
  requirement, `file:line` for every factual claim, `UNKNOWN`/`NO SOURCED ESTIMATE`
  where the documents do not establish a fact.

## 0. Status of the cited cutover-tabletop file

`MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md`
**does not exist in this checkout** (repo-wide `CUTOVER_TABLETOP*` glob: no match,
2026-08-15). The recovery contract below therefore aligns with the
recommendation's substance as quoted in the lane kickoff — "evidence-class backups
encrypted off-host, versioned and retention-locked, with the write credential
unable to delete versions" (`C:\tmp\lane_kick\W8.md:36-39`) — which is already the
committed policy at `KVM2_PROGRAM/recovery/STATE_CONTINUITY.md:36-39` and the P5-03
task contract (`EXECUTION_TASKS:415-428`). **Settler:** the sibling cutover lane's
output landing and the Lead committing it; this file should then be re-cited and
any divergence reconciled.

## 0.1 The deploy-list demands every contract is anchored to

The deploy list's operations item makes six demands: a release/baseline manifest,
a rollback SHA with a tested rollback procedure, a systemd-unit hash, encrypted
backups with a restore check, rotated persistent logs, and monitoring for health,
restart loops, reconciliation freshness and disk/log growth
(`READINESS:252-254`, restated as the pre-cutover evidence package at
`READINESS:338` and `BREAKDOWN:80` R41). Implementation anchors, verified in this
lane:

| Demand | Existing anchor |
|---|---|
| Release/baseline manifest | Hash-only install manifest, schema 1.0.0: `release_sha`, `release_manifest_sha256`, `first_start_unit_sha256` (state masked), `requirements_lock_sha256`, state/log/env paths, all-false action flags, `root:root 0640` — `install.sh:398-428` |
| Rollback SHA + tested procedure | `rollback.sh` implements exactly KVM2-P4-08: stop/mask, optional verified re-bind to `--to-release-sha`, manifest with both SHAs + unit hash; never start/enable/unmask/ARM, never touch `/var/lib/mtc-bridge`, firewall, secrets, Windows writer, exchange — `rollback.sh:3-29`; task contract `EXECUTION_TASKS:357-366` |
| systemd-unit hash | `install.sh:413` (`first_start_unit_sha256`), logged at `install.sh:431-433` |
| Encrypted backup + restore check | `STATE_CONTINUITY.md:36-39` (off-host, versioned, retention-locked, write credential cannot delete versions); P5-03 test contract `EXECUTION_TASKS:415-428` |
| Rotated persistent logs | Frozen logrotate policy: daily, 30 generations, 64M early rotate, `copytruncate`, no restart ever, `0640 mtc-bridge:mtc-bridge`; forced-rotation test at P4-07 — `logrotate/mtc-bridge:1-26` |
| Health / restart-loop / reconcile-freshness / disk-log monitoring | `READINESS:253-254`; first-start evidence set (health check, reconciliation, restart count zero) `EXECUTION_TASKS:337-348` |

---

## Contract R — Recovery (backup, restore, rollback, access recovery)

Task-contract sources: P2-06 recovery clauses (`EXECUTION_TASKS:136-146`), P2-07
(`EXECUTION_TASKS:147-151`), P4-08/P4-08A/P4-08B (`EXECUTION_TASKS:357-377`),
P5-03 (`EXECUTION_TASKS:415-428`). Extends `STATE_CONTINUITY.md` and
`ACCESS_RECOVERY.md`. Anchors all six deploy-list demands.

### Required end state

- **R1 Baseline identity.** Every install produces the hash-only manifest of
  `install.sh:398-428`. All recovery/restore/rollback evidence names its
  (`release_sha`, `release_manifest_sha256`) pair; no backup or rollback claim is
  accepted against an unnamed release identity.
- **R2 Rollback target.** A named immutable rollback-state artifact/manifest SHA
  plus a hash-recorded procedure tested once. At first deploy the recorded target
  state is: service stopped/disabled, state/risk artifacts preserved, writer count
  zero, no Windows authority re-enabled; a prior accepted release's rollback SHA is
  recorded when one exists (`EXECUTION_TASKS:357-366`; `rollback.sh:3-14`).
- **R3 Backups.** Evidence-class: encrypted, off-host, versioned, retention-locked;
  the KVM2 write credential cannot delete versions or change retention; a
  separately held recovery credential; off-PC encryption-key recovery exercised;
  secret values excluded (`STATE_CONTINUITY.md:36-39`;
  `EXECUTION_TASKS:417-424`; kickoff alignment `W8.md:36-39`, §0 above).
- **R4 Restore discipline.** No restore is accepted without exact-release
  ordering, bundle verification, application-level semantic checks, and an isolated
  restore drill (`STATE_CONTINUITY.md:41-43`). SQLite `integrity_check` plus the
  risk-state invariants (daily-loss, consecutive-loss, order, foreign-position) are
  preserved — a restore that would reset or hide risk evidence refuses rather than
  proceeds (`EXECUTION_TASKS:136-145`; D5's preserve-or-block wording,
  `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:98-107`). This is the written
  fresh-reset branch D5 requires ("start clean" ≠ "start blind"), which no existing
  artifact supplies.
- **R5 Recovery-start gating.** After any rollback, exactly one DISARMED,
  TESTNET-only recovery-start under its own owner sentence (P4-08A); execution
  bounded by P4-08B with hash-match, reconcile, zero-restart, loopback and
  `HL_LIVE_ACK`-absent proofs; no retry without new authority
  (`EXECUTION_TASKS:367-377`).
- **R6 Access recovery.** Recorded without private identifiers: SSH key custody
  roles, provider-panel ownership/MFA/emergency-console procedure, second-device
  recovery test, revocation authority, backup-provider ownership plus separately
  held recovery credential, DNS/domain/cert inventory or explicit `NONE`, and
  expiry/billing/renewal owners (`ACCESS_RECOVERY.md:9-18`). Recovery must not
  depend on one powered-on PC or one untested credential
  (`ACCESS_RECOVERY.md:5-7`).
- **R7 Pre-cutover archive slot.** D5 leaves open whether the pre-cutover risk
  state is archived off-host before the fresh start; the Lead recommends archiving
  as the only record of the paper period (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:112-116`).
  The contract carries this as a required owner decision feeding R3, not as a
  settled requirement.

### Verification

Bundle DB and invariant SHA-256 equality end to end — the verifier rechecks
manifest contract, path sanitization, DB hash, integrity, foreign keys, table
counts, open trades, live orders, loss streaks, realized PnL, risk-day ledger and
maximum identifiers, and any mismatch blocks transfer/start/ARM
(`STATE_CONTINUITY.md:16-26`). Restore drill produces destination-hash equality
and measured RPO/RTO per class (`EXECUTION_TASKS:422-423`). Rollback run produces
its manifest (both SHAs, unit hash) and exit 0 (`rollback.sh:14,29`). The rollback
and restore evidence package executes once on the accepted install before cutover
under Ordering A (`BREAKDOWN:108-110`, R41 at `BREAKDOWN:80`).

### Violation signature

A backup cited with no restore test or no measured RPO/RTO; the KVM2 credential
able to delete a version or alter retention; a restore that completes with
risk-state evidence absent instead of refusing; rollback claimed with no SHA pair
or no executed test; a recovery-start attempted under P4-06/P4-08 authority or a
second attempt without new P4-08A; a recovery path naming a single PC or an
untested credential. (Stops: `EXECUTION_TASKS:144-145,364-366,370-371,425-428`.)

### Out of scope

Executing anything above (host action); backup/monitoring provider, retention
period and credential choices (owner rows R38, `BREAKDOWN:77`; P5-01,
`EXECUTION_TASKS:384-399`); RPO/RTO values (OPEN owner decision per class,
`STATE_CONTINUITY.md:30-34`); WAL capture execution; ARM/resume; secret values;
deciding the D5 archive sub-question itself.

---

## Contract T — Teardown and destructive reprovision

Task-contract source: P2-08 (`EXECUTION_TASKS:152-157`), with the critical rule at
`EXECUTION_TASKS:194-195`. Extends `TEARDOWN_AND_REPROVISION.md`. Anchors: the
baseline manifest and unit hash as enumeration sources; rotated-log export rules.

### Required end state

- **T1 Enumeration inventory.** Every admitted lab service, user/group, package,
  repository, scheduler, timer, unit, output directory, credential name, network
  rule, namespace, container artifact, browser profile, cache and monitoring
  extension is enumerated (`TEARDOWN_AND_REPROVISION.md:3-9`). Bridge-side entries
  are traceable to the install manifest's hashes (release SHA, unit hash, lock
  hash; `install.sh:408-416`) so "what was installed" is mechanically enumerable
  before anything is removed.
- **T2 Absence proof.** After destructive reprovision, absence of every T1 entry
  is proved by evidence; uninstalling is not clean proof
  (`TEARDOWN_AND_REPROVISION.md:7-9`).
- **T3 Export allowlist.** Only owner-reviewed sanitized reports and separately
  verified bridge release, configuration and WAL-consistent state artifacts may be
  exported; secret values are reissued/rotated, never copied through ordinary
  backup (`TEARDOWN_AND_REPROVISION.md:11-15`).
- **T4 Never-restore list.** Into trading-only, never restore: lab OS image or
  snapshot, lab home, agent workspace, cached credential, package environment,
  container storage, browser data, scheduled task, lab log, lab backup
  (`TEARDOWN_AND_REPROVISION.md:17-21`) — carrying the rule that a post-lab
  snapshot is a lab recovery snapshot, not a clean trading image
  (`EXECUTION_TASKS:194-195`).
- **T5 Route packet.** Option A (wipe/bootstrap/restore) or Option B
  (purchase/provision/restore), each one separately authorized packet requiring
  trusted-image provenance, new host/boot/filesystem evidence, rotated
  credentials, verified-only restore, no-lab proof, rollback, and fresh
  independent post-build acceptance before any final mainnet decision
  (`TEARDOWN_AND_REPROVISION.md:23-27`).
- **T6 Log handling.** The only log exports are the sanitized ledger plus
  encrypted restricted raw evidence (`STATE_CONTINUITY.md:33`); raw persistent
  logs stay inside the T4 boundary.

### Verification

An absence-proof matrix covering every T1 entry with per-entry evidence; export
packet hashes verified against the named artifacts; the credential-rotation list
checked by name against the secret inventory; the chosen route packet complete per
T5 before any reprovision is proposed.

### Violation signature

Any proposal to restore a T4 item into trading-only (`EXECUTION_TASKS:155-157`);
absence asserted from uninstall alone; an export containing a secret value or an
unverified artifact; reprovision proposed with an incomplete inventory or without
its route packet.

### Out of scope

Performing teardown, wipe or reprovision; lab admission (later phases); the
trading-only build and any mainnet decision; choosing Option A vs B (owner packet
decision at execution time). The inventory populates only as workloads are
admitted; today it is necessarily a category schema, which is correct, not a gap.

---

## Contract M — Maintenance

Task-contract source: P2-10 (`EXECUTION_TASKS:168-177`), drill execution at
P4-07A (`EXECUTION_TASKS:349-356`). Extends `MAINTENANCE.md`. Anchors: unit hash,
pre/post manifests, rollback, DISARMED restart monitoring.

### Required end state

- **M1 Unattended-upgrades scope.** The actual scope and restart behaviour — which
  origins/package classes, restart semantics, blackout interaction with the owner
  window — written down. Today only the precondition sentence exists
  ("may be configured only after exact scope and restart behavior are frozen",
  `MAINTENANCE.md:5-8`); P2-10 requires the config/scope itself
  (`EXECUTION_TASKS:168-171`).
- **M2 Auto-reboot/auto-restart policy.** Both disabled unless separately
  designed, staged, audited and owner-approved (`MAINTENANCE.md:5-8`); leaving
  them undefined is a Stop condition (`EXECUTION_TASKS:175-177`).
- **M3 Window procedure.** The nine steps of `MAINTENANCE.md:10-20`: owner window
  and named executor; bridge DISARMED and single-writer assertions; an accepted
  state/recovery artifact before any change (cross-ref Contract R R3); pre-change
  manifests over OS packages, unit, config, release, venv, listener, user/group,
  disk and service; an exact bounded command set; post-change diff and unit-hash
  comparison; one separately authorized DISARMED restart when required;
  reconciliation and state-continuity proof; rollback on drift or failure.
- **M4 Rollback runbook.** Names the rollback SHA pair and the tested procedure
  from Contract R (P4-08; `rollback.sh:3-29`), replacing the current one-step
  rollback (`MAINTENANCE.md:20`).
- **M5 DISARMED restart+reconcile sequence.** Documented stepwise; absence is a
  Stop condition (`EXECUTION_TASKS:176-177`).
- **M6 Drift and reset rules.** Package/unit/config drift, reboot, restart,
  reconcile gap, evidence gap, provider-panel action, or a changed service-profile
  hash resets or reclassifies the monitoring window per the later accepted P5-04
  contract; isolation-affecting changes require new security acceptance and lab
  re-admission; any unit/profile change after P5-03A close invalidates P5-06
  through P5-10 and forces a rerun (`MAINTENANCE.md:22-25`;
  `EXECUTION_TASKS:429-439`).
- **M7 Drill spec (design only).** Expected pre/post manifest format, unit-hash
  comparison, DISARMED reconcile sequence and pass/fail criteria; execution
  deferred to P4-07A — exactly one attempt on the exact installed candidate, under
  its own owner sentence, pre/post hashes compared, automatic ARM a Stop
  (`MAINTENANCE.md:27-28`; `EXECUTION_TASKS:168-175,349-356`).

### Verification

Per window: pre/post manifest diffs recorded and clean or explained; unit hash
compared against the install manifest value (`install.sh:413`); DISARMED restart
plus reconcile proof retained. For the drill: a record with hashed outcome on the
exact P4-07 candidate (`EXECUTION_TASKS:350-353`).

### Violation signature

An update applied with no pre-change backup; unit-hash drift with no diff or
alert; auto-reboot/auto-restart enabled without the separate approval chain; a
restart that is not DISARMED or lacks reconcile proof; a drill run under
P4-06/P4-07 authority, run more than once, or on a non-P4-07 candidate; automatic
ARM triggered during the drill (`EXECUTION_TASKS:354-356`).

### Out of scope

Executing updates or the drill; the P5-04 window-length semantics themselves;
monitoring implementation (P5-02); enabling unattended upgrades (host-side
execution).

---

## Contract I — Incident and contamination

Task-contract source: P2-11 (`EXECUTION_TASKS:178-187`). Extends
`INCIDENT_RESPONSE.md`. Anchors: the four monitored signals as incident triggers;
alert-only automation (P5-02).

### Required end state

- **I1 Two-class classification.** Resource/SLO breach vs security-boundary breach,
  defined up front (`INCIDENT_RESPONSE.md:3-22`); every incident resolves to
  exactly one class before any response step runs.
- **I2 Signal→response map.** The deploy list's four monitored signals — health,
  restart loops, reconcile freshness, disk/log growth (`READINESS:253-254`) — plus
  provider-panel actions and drift alerts, each mapped to a class and response.
  All automated response is alert-only: automation must not restart, DISARM, ARM,
  reconcile, deploy, or modify bridge state (`INCIDENT_RESPONSE.md:7`; P5-02 Stop,
  `EXECUTION_TASKS:412-414`). Restart-loop cases cite the first-start evidence
  "restart count zero" (`EXECUTION_TASKS:341-342`) and `Restart=no`
  (`READINESS:147-150`).
- **I3 CONTAMINATED response.** The eight steps, unchanged: kill all lab
  workloads; preserve evidence without mutation; mark the host `CONTAMINATED`;
  notify the owner immediately; human-controlled DISARM under separate authority;
  revoke and rotate every TESTNET credential **by name**; prohibit bridge
  resume/ARM; require destructive trusted reprovision or migration to a separately
  clean host (`INCIDENT_RESPONSE.md:9-22`). Revocation names must match the secret
  inventory.
- **I4 Provider-panel branch.** Any provider-panel snapshot, restore, reboot,
  firewall or service action while the bridge is deployed resets/reclassifies
  P5-04 monitoring; an unexplained action invokes the master stop and is treated as
  a possible boundary incident (`INCIDENT_RESPONSE.md:24-29`;
  `ACCESS_RECOVERY.md:20-23`). Naming reconciliation: the task text names the
  provider panel **Kodee** (`EXECUTION_TASKS:182`) while the artifact says
  "provider-panel" generically — one line to fix at R31 write time.
- **I5 Off-host detection dependency.** Incident detection must not depend on
  KVM2 or the Windows PC; with no independent external heartbeat source the risk
  is recorded as BLOCKER and ARM stays blocked (`EXECUTION_TASKS:400-411`).
- **I6 Evidence record.** UTC time, classification, sanitized summary, restricted
  raw logical ID, hashes, responsible roles, containment, credential-name actions,
  recovery decision, retry history; no private identifiers, no secret values
  (`INCIDENT_RESPONSE.md:31-37`).
- **I7 Tabletop drill record.** Scenario, expected vs actual classification,
  per-step actions, outcome hash — currently OPEN
  (`INCIDENT_RESPONSE.md:36-37`); required for P2-11 closure
  (`EXECUTION_TASKS:184-187`).

### Verification

Every drill scenario resolves to exactly one class and its mapped response; the
drill record carries a hashed outcome and no private identifiers; the revocation
list equals the secret-inventory names; the alert-only property is tested (the
observer provably cannot mutate the bridge).

### Violation signature

Resource and security breaches not distinguished (`EXECUTION_TASKS:186-187`); a
CONTAMINATED response omitting credential revocation; any watchdog or monitor with
bridge-mutating capability; a provider-panel action that does not reclassify the
window; a drill absent, unhashed, or with unexplained deviations.

### Out of scope

Running the drill (it needs its own authorization context); killing workloads,
revoking credentials, or contacting the provider; the P5-04 window definition; ARM
decisions of any kind.

---

## Estimates

- Drafting these four contracts is work inside catalogue row R31, which is **NO
  SOURCED ESTIMATE** (`BREAKDOWN:70`). No document read in this lane prices any
  subset of it. Settler, same as R27's: a Lead-scoped write/validation contract
  per artifact plus one timed authoring session (`BREAKDOWN:66`).
- The **3–6 h** figure at `READINESS:338` is R41 host *execution* of the
  backup/rollback/restore/logrotate/monitoring evidence package (`BREAKDOWN:80`) —
  execution labour, not drafting; it must not be booked against R31.
- Owner-side inputs these contracts depend on (R38 provider/retention/monitoring
  choices, `BREAKDOWN:77`; P5-01 authorization, `EXECUTION_TASKS:384-399`) are
  `OWNER` rows and carry no implementer hours.

## OPEN / UNKNOWN, with settlers

| Item | Status | Settler |
|---|---|---|
| Cutover-tabletop archival recommendation (cited source) | **ABSENT** — file not in this checkout (§0) | Sibling lane output lands and Lead commits it; then re-cite and reconcile |
| RPO/RTO per recovery class | OPEN owner decision (`STATE_CONTINUITY.md:30-34`) | Owner sentences; then measured at P5-03 |
| Backup/monitoring provider, retention, recovery credentials | OPEN owner choices (`BREAKDOWN:77`; `EXECUTION_TASKS:384-399`) | R38 / P5-01 owner authorizations |
| D5 archive-off-host sub-question | Undecided (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:112-116`) | One-sentence owner follow-up |
| Release SHA and rendered unit hash these contracts must name | UNVERIFIED / not frozen — no accepted candidate for the current tree (`READINESS:100-102`) | R03–R08 integrated candidate (R23 final freeze) |
| `STATE_CONTINUITY.md:3-5` still says fresh reset "not selected" | Stale against D5 "start clean" (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-96`) | Plan-maintenance update under separate write authorization; Contract R R4 supplies the missing fresh-reset branch text |

## Boundary statement

This lane performed no host, network, SSH, deployment, service, credential,
broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading,
merge-to-master, push, or economic action; no product code changed; no acceptance
and no authorization is granted or implied. No other AI CLI or agent was invoked
or shelled out to. The repository was treated read-only; exactly one output file
was written: this one.
