# KVM2 Phase-2 contracts v2 — secret, state, recovery, teardown, maintenance, incident

Status: **T2 contract draft / preparation only / no action / no acceptance / no authorization**.
This rewrites six of the ten reviewed contracts; the ten-contract scope is established at
`PHASE2_CONTRACT_REVIEW_2026-08-15.md:26-33`. The governing quality rule is that every
check must have an independent expectation, a closed universe, a concrete RED world, and
a STOP result when observation is incomplete
(`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`). Canonical source directories are
`MTC_COMMAND_CENTER/11_TRIAGE/`, its `KVM2_PHASE2_CONTRACTS/` child, and
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/`.

## Common verification rule

- A producer's manifest, digest, explanation, classification, or inventory is evidence of
  what that producer emitted, not proof that the claim is true. Expected state must come
  from an owner decision, a record frozen before the checked operation, or independent
  discovery (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:312-326`).
- Every probe captures status, output, diagnostics, and completion before interpreting
  content. Inaccessibility, incomplete enumeration, malformed input, or an unmodelled
  member is **STOP/BLOCK**, never PASS (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:316-326`).
- Before operational use, the real verifier must be shown RED against an independently
  made deviant fixture and GREEN against the conforming fixture. Reimplementing the
  verifier's logic is not evidence (`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:25-28,73-83`).

## 1. Secret contract

### Required end state

1. The wallet remains deferred. No wallet is provisioned, requested, inferred, generated,
   stored, or represented by a key value; checklist item 4 remains open and blocks the
   first start (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:80-87`).
2. After a future separate owner decision, the mechanism is one sanctioned root-owned
   at-rest environment source with mode `0600`, consumed only through the service's
   effective environment. The runtime environment copy is not a second at-rest store.
   Backups exclude secret values (`SECRET_INVENTORY.md:6-13,20-21`;
   `PHASE2_CONTRACT_REVIEW_2026-08-15.md:170-181`). The concrete delivery channel is
   **UNKNOWN** until that future owner record establishes it
   (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:135-148`).
3. A secret value may never enter arguments, logs, journal records, diagnostics, crash or
   core output, manifests, evidence, screenshots, exports, or backups. The only permitted
   runtime consumer is the intended service process; all other copies are violations
   (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:176-181,333-337`).
4. **Exact `HL_LIVE_ACK` boundary.** A bare policy-name mention is allowed only in prose,
   comments, scanner rules, and names-only result labels. It is forbidden as:
   - an active definition, assignment, or exported name in any environment source;
   - an effective unit environment entry, including one supplied by a drop-in or included
     environment source;
   - a name in the service process's effective environment;
   - an argument, or a structured manifest/evidence/diagnostic field paired with any value.

   Comments and documentation are outside the active-definition universe, so a unit-template
   comment containing the bare name is compliant. Parsing an active definition or observing
   the name in either effective environment is non-compliant. This replaces the contradictory
   “present in any form” wording and gives the service contract the same checkable boundary
   (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:161-181,304-306`;
   `SECRET_INVENTORY.md:15-21`).

### Verification

- **Deferred gate:** the first-start packet must contain a later owner lift and its separate
  provisioning authority. Their absence makes the gate RED/BLOCK; no declaration by the
  installer can substitute (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:84-87`).
- **Frozen universe:** before verification, an independent names-only scope record enumerates
  the candidate tree, all unit sources and drop-ins, every included environment source, the
  effective unit and process environment name sets, manifests, evidence/export sets, log and
  crash-output sources, and backup indexes. Every member receives exactly one disposition.
  An inaccessible source, unknown include, or count mismatch is STOP, not absence
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:170-181,323-326`).
- **Parsed checks:** environment and unit grammars are parsed; comments are excluded by the
  parser, not by text filtering. Effective environment checks consume names only. Evidence
  records scope identity and dispositions, never environment values
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:176-181,320-326`).
- **Falsification:** the real scanner must go RED when an independent fixture adds an active
  forbidden definition on each named surface or places a synthetic non-secret sentinel on an
  egress surface; it must remain GREEN for a bare comment and STOP for an unreadable member.
  No real or value-shaped secret fixture belongs in this contract
  (`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:50-63,75-83`).

### Violation signature

First start is not blocked while deferral stands; any key value is requested, generated,
stored, represented, or exposed; more than one at-rest source exists; a secret reaches an
egress surface; `HL_LIVE_ACK` is actively defined or appears in an effective environment;
or an incomplete scan is reported as PASS.

### Out of scope

Provisioning or inspecting a secret, choosing its concrete delivery channel, any host or
service action, and proving inaccessible external chat/history/screenshot universes.
Those external universes are **UNKNOWN** unless separately inventoried; they cannot be
declared clean from this artifact (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:170-181`).

## 2. State contract

### Required end state

1. Cutover starts with a fresh destination database, not inherited database state. It has
   no inherited daily-loss counter, consecutive-loss counter, order history, or
   foreign-position record (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-101`).
2. “Clean” is four exact schema-aware predicates, not the ambiguous phrase “absent/zero.”
   The exact table, column, risk-day, and representation predicates are **UNKNOWN** until a
   read-only verifier specification independent of the reset producer freezes one expected
   result for each class. Cutover remains blocked until then
   (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:192-211`).
3. Before reset, the state contract owns a complete semantic source capture for all four
   risk classes and the unchanged single-writer evidence. The capture must be retrievable
   at the owner-selected preservation location; otherwise reset/start blocks. “Start clean”
   never permits “start blind” (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:98-110`).
4. The archive location remains open: off-host archive and retained old-host state are both
   admissible contract branches until the owner chooses. A recorded choice and a successful
   retrieval proof are required before cutover; neither branch is presumed
   (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:112-116`).
5. The reset producer and semantic verifier are separate frozen artifacts. Digests bind
   bytes only; they supplement, never replace, the independent semantic result
   (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:192-211`). State owns source capture, reset
   production, clean-state semantics, and preserve-or-block; recovery owns later backup,
   restore, rollback, and recovery objectives
   (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:327-332`).

### Verification

- **Source before reset:** the independent verifier records schema census and one result for
  each risk class before any reset step. Missing tables, wrong risk day, stale capture,
  malformed state, or incomplete observation is STOP/BLOCK
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:204-211`).
- **Preservation:** retrieve the frozen source capture from the recorded owner-selected
  location and re-run the same semantic verifier before the destructive branch can proceed.
  Failure to retrieve or semantic mismatch is RED/BLOCK; producer-authored hashes alone
  cannot turn it GREEN (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:102-116`;
  `PHASE2_CONTRACT_REVIEW_2026-08-15.md:192-211`).
- **Destination after reset:** the verifier independently establishes integrity, complete
  schema visibility, and the four exact clean predicates. Expectations come from D5 and the
  frozen verifier specification, never from reset output
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:204-211`).
- **Falsification:** the real verifier must be RED for non-empty, stale, wrong-risk-day,
  missing-table, malformed, corrupt, and byte-matching-but-semantically-wrong fixtures; it
  must STOP when it cannot complete the read. Each new closure test needs its own demonstrated
  RED and GREEN (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:204-211`).

### Violation signature

Any inherited member of the four risk classes; reset before complete retrievable source
capture; no recorded archive-mode choice at cutover; missing or ambiguous predicate;
reset producer supplying its own expected result; digest equality treated as semantic proof;
missing single-writer evidence; or observation failure reported as clean.

### Out of scope

The owner archive choice, the exact reset command, exact schema predicates, and all cutover
execution are out of scope and currently **UNKNOWN** where noted
(`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:265-283`). WAL migration is not the selected
destination-state branch (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-97`).

## 3. Recovery contract

### Required end state

1. Recovery consumes the state contract's independently accepted source capture,
   destination semantics, and frozen identities; it does not recreate or re-adjudicate the
   clean-reset branch (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:327-332`).
2. The owner-selected preservation branch is explicit. If off-host archive is selected,
   recovery retrieves from that archive. If retained old-host state is selected, recovery
   retrieves the preserved capture there. Both branches use the same identity and semantic
   verifier and block on loss, inaccessibility, or mismatch. The choice remains **OPEN**
   (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:112-116`).
3. Later backups are encrypted, off-host, versioned, retention-locked, restorable in
   isolation, and exclude secret values. The routine write role cannot delete versions or
   alter retention; a separately held recovery role exists
   (`STATE_CONTINUITY.md:28-43`). Provider, retention duration, and recovery-objective values
   are **UNKNOWN** pending owner decisions
   (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:128-134`).
4. Rollback has identities frozen before rollback and independently observed postconditions:
   selected release, effective unit state, writer absence, state preservation, secret-store
   non-mutation, and exposure state. A rollback-produced manifest is supplemental only
   (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:220-235`).
5. Access recovery records roles and procedures without private identifiers or values and
   must not depend on one powered-on device or one untested recovery path
   (`ACCESS_RECOVERY.md:3-18,25-26`).

### Verification

- **Restore:** retrieve the selected branch into isolation, bind it to expectations frozen
  before recovery, then run the independent integrity and four-class semantic verifier.
  Missing risk evidence, wrong release, or inaccessible capture is RED/BLOCK
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:230-235`).
- **Rollback:** observe every postcondition directly after the procedure. A no-op procedure
  or false producer-authored boolean must make the independent observer RED; incomplete
  observation is STOP (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:220-235`).
- **Retention:** with the routine write role, a deletion or retention-change attempt must be
  denied; an allowed attempt is RED. An isolated recovery using the separate recovery role
  must be GREEN. No value is recorded (`STATE_CONTINUITY.md:36-43`).
- **Falsification:** demonstrate RED for wrong release, missing risk evidence, altered
  semantics with matching packaging metadata, no-op rollback, false manifest claims,
  incomplete observation, and deletion-capable routine backup access
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:230-235`).

### Violation signature

Either archive branch is assumed before the owner chooses; the selected capture cannot be
retrieved; restore hides or resets risk evidence; rollback acceptance relies on its own
manifest; routine backup access can delete or weaken retention; a secret value enters a
backup/evidence surface; or an untested single-device recovery dependency remains.

### Out of scope

Choosing the archive branch, provider, retention duration, recovery objectives, or private
recovery details; performing backup, restore, rollback, access recovery, or any start action.

## 4. Teardown contract

### Required end state

1. The pre-teardown universe is the union of at least two independent sources: the admission
   ledger and actual discovery across service, identity, package, scheduler, unit, file,
   network-rule, namespace, container, browser, cache, monitoring, and credential-name
   categories (`TEARDOWN_AND_REPROVISION.md:3-9`;
   `PHASE2_CONTRACT_REVIEW_2026-08-15.md:251-256`).
2. Every discovered member receives a stable identity and exactly one terminal disposition:
   removed, explicitly retained by the sanitized export allowlist, rejected from export, or
   unresolved/BLOCK. No member may disappear between discovery and proof
   (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:242-256`).
3. Post-reprovision state is compared with a clean-profile allowlist frozen independently
   before teardown. Uninstall output is never absence proof
   (`TEARDOWN_AND_REPROVISION.md:5-9`).
4. Only owner-reviewed sanitized reports and independently verified release, configuration,
   and accepted state artifacts may be exported. Lab images, homes, workspaces, caches,
   package/container/browser state, scheduled tasks, lab logs, and lab backups are never
   restored into trading-only (`TEARDOWN_AND_REPROVISION.md:11-27`). Secret egress follows
   Contract 1.

### Verification

- **Conservation:** reconcile the two source inventories and carry every member through a
  terminal-disposition ledger. A member present in discovery but absent from the admission
  ledger is added as discovered-unregistered and blocks; it is not dropped
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:242-256`).
- **Post-state:** independently discover again and compare against the frozen clean allowlist.
  An unexpected survivor or unapproved addition is RED; inaccessible categories or
  namespaces are STOP (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:251-256`).
- **Falsification:** inject one member omitted from the declared ledger. The real proof must
  discover it and go RED/BLOCK. Also test duplicate identities, representation drift, an
  inaccessible category, and one never-restore member in the export packet
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:251-256`).

### Violation signature

A one-source or incomplete universe; an admitted/discovered member with no terminal
disposition; uninstall treated as proof; incomplete discovery reported as clean; export of
an unverified or prohibited member; or secret value exposure.

### Out of scope

Performing teardown, wipe, reprovision, export, restore, or selecting either future route.
The exact clean-profile allowlist is **UNKNOWN** until independently frozen before execution.

## 5. Maintenance contract

### Required end state

1. Automatic updates remain disabled until exact allowed origins, packages, command grammar,
   blackout interaction, reboot behavior, and restart behavior are owner-accepted and frozen
   before a window. Those values are currently **UNKNOWN**
   (`MAINTENANCE.md:3-8`; `PHASE2_CONTRACT_REVIEW_2026-08-15.md:258-264`).
2. Every window has a frozen allowed-change set, named executor, accepted pre-change recovery
   artifact, bounded commands, independent pre/post collection, separately authorized
   DISARMED restart only when required, reconciliation proof, and rollback on drift or
   failure (`MAINTENANCE.md:10-21`).
3. Every observed delta receives exactly one preregistered allowed disposition or blocks.
   The executor cannot make a delta acceptable by explaining it after the fact; exceptions
   require an independently named adjudicator (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:265-277`).
4. Effective unit state, including drop-ins, is verified; source text and an installer
   manifest are not substitutes. Package/unit/config drift, reboot, restart, reconciliation
   gap, evidence gap, provider action, or profile-identity change triggers the specified
   reset/reclassification (`MAINTENANCE.md:23-28`). Secret egress follows Contract 1.

### Verification

- **Pre-window gate:** compare the proposed command/change set with the independently frozen
  allowed set. Any undeclared member is RED/BLOCK; no frozen set is STOP
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:273-277`).
- **Independent diff:** collectors frozen before the window census packages, effective unit
  and drop-ins, configuration/release identities, runtime state, identity, storage, and log
  state. Every before-member and after-member has one disposition; incomplete collection is
  STOP. Digests bind bytes but do not adjudicate correctness
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:265-277`).
- **Falsification:** the real verifier must be RED for an undeclared package, added unit
  drop-in, automatic reboot, automatic or armed restart, stale reconciliation evidence, and
  unexplained drift. A producer-authored “explained” label must not change the result
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:273-277`).

### Violation signature

Maintenance proceeds while scope is UNKNOWN; a command or delta lies outside the frozen
set; reboot/restart occurs without its separate rule; effective unit drift is missed;
reconciliation is stale or absent; the executor self-approves an exception; incomplete
collection passes; or egress exposes a secret value.

### Out of scope

Choosing the currently UNKNOWN update/blackout/reboot/restart values; executing updates,
reboot, restart, reconcile, rollback, or the drill; defining later monitoring-window length.

## 6. Incident contract

### Required end state

1. Classification uses two independent booleans: resource/SLO impact and security-boundary
   impact. Neither, either, or both may be true. If security-boundary impact is true, the
   conservative contamination response applies even when resource impact is also true; this
   removes the unsafe exactly-one rule (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:279-300`).
2. Signals and expected responses are preregistered independently from the responder.
   Automation is alert-only and has no bridge-mutating capability
   (`INCIDENT_RESPONSE.md:3-22`; `PHASE2_CONTRACT_REVIEW_2026-08-15.md:295-300`).
3. The contamination response preserves evidence without mutation, marks contamination,
   notifies the owner, blocks resume, and routes containment, credential-name revocation,
   and clean recovery through separate authority (`INCIDENT_RESPONSE.md:9-22`). No value is
   present in the revocation inventory or incident record.
4. The credential-name universe is the union of the names-only inventory and independent
   discovery of configured consumers/stores. Every name receives one disposition, including
   not-provisioned where independently established; omissions and inaccessible sources block
   (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:287-300,323-326`).
5. Detection has an independent off-host heartbeat; without it, the dependency is a BLOCKER.
   Incident evidence is sanitized, with restricted raw material outside ordinary evidence
   exports and no secret value (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:297-307`).

### Verification

- **Independent scenarios:** a scenario author freezes inputs and both expected booleans
  before the responder runs. The real response record is compared to that table; the
  responder's own classification and outcome digest cannot supply the expectation
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:287-300`).
- **Capability denial:** the observer's effective capabilities are independently enumerated,
  and a safe mutation attempt must be denied. An allowed attempt is RED; inability to
  evaluate capability is STOP (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:295-300`).
- **Universe and heartbeat:** reconcile both credential-name sources with terminal
  accounting and independently observe the off-host heartbeat. Missing names, incomplete
  discovery, or absent heartbeat is RED/BLOCK
  (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:287-300`).
- **Falsification:** demonstrate RED for a combined resource/security scenario that is
  reduced to resource-only, any misclassification, an omitted revocation name, monitor
  mutation capability, missing off-host heartbeat, and secret-bearing raw evidence entering
  the sanitized export (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:295-300`).

### Violation signature

Exactly-one classification is enforced; a dual incident avoids the contamination branch;
expected classification comes from the responder; automation can mutate state; a discovered
credential name has no disposition; off-host detection is absent; an incomplete observation
passes; or a secret value enters incident evidence/export.

### Out of scope

Running a drill or response, containment, workload termination, provider contact, revocation,
rotation, recovery, or any bridge-state action. Exact signal thresholds, provider details,
and retry timing are **UNKNOWN** until separately frozen and authorized.

## Boundary

This document performs and authorizes no host, network, SSH, deployment, service,
credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading,
merge-to-master, push, product-code, or economic action. It is not acceptance.
