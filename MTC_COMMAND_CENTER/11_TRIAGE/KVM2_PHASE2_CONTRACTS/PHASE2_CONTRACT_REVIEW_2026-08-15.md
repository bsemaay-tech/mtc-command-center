# KVM2 Phase-2 contract review — Lane V2 — 2026-08-15

## Verdict

**Overall: NEEDS-REWORK.** All ten contracts present in the four committed files
need at least one required repair before they are verification-ready. The owner
decisions themselves are carried in the secret and state drafts, but multiple
checks can still pass without proving their claims. This is a T2 documentation /
evidence review only. It is not acceptance or authorization.

## Reviewed bytes and scope note

The detached checkout is at `25564449b8a8254eaa75535039acef4993f5f27e`; the
four named files and the named self-confirming-pattern file are not in that tree.
Read-only `git log --all` located all five at commit
`a4833939b02a60815cfb321287d089cc6fdf8332`. This review uses these exact blobs:

| File | Git blob |
|---|---|
| `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md` | `c1f41c4dadae32b7945ae4466bd22df19828a6b1` |
| `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md` | `797d4950eb513984ae779d1639a476591928a74d` |
| `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_AND_STATE_CONTRACTS_2026-08-15.md` | `3d11879a43fe39b626317e36a089901751536141` |
| `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md` | `b330f0671cb5d4c8186bc5db0c1e500e0163e829` |
| `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md` | `592764f370958efb292ed54bbf4db1d0069a8acf` |

The task says “eight” contracts (`C:\tmp\lane_kick\V2.md:1,5,17`), but the
four source files contain **ten**: identity, filesystem, network, service,
secret, state, recovery, teardown, maintenance, and incident. The last file
alone defines four contracts
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:57,138,199,264`
@ `a4833939`). I reviewed all ten. **UNKNOWN:** whether “eight” was intended to
exclude or combine two of them. A corrected contract index or explicit list
would settle the count; it does not change the findings below.

The applicable test is the committed rule: identify what makes a check fail,
where its expected value comes from, what lies outside its universe, and whether
the property is enforced or merely asserted
(`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`
@ `a4833939`).

## Per-contract verdicts

### 1. Identity contract — NEEDS-REWORK

- **End state:** Mostly concrete for the service account, home, shell, unit
  identity, and profile-specific absence rules
  (`IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:54-79`). It is not complete:
  the exact profile inventory, complete privileged-group universe, and executable
  cross-user command grammar are explicitly UNKNOWN
  (`IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:117-136`).
- **Check quality:** ID-02 cites the current name-based supplementary-group
  verifier (`IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:95-102`). That
  verifier treats the `id -nG | tr | grep` pipeline's non-match as proof of no
  prohibited group (`IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:55-71` @
  `2ce41e34`). It can therefore print PASS when `id`/NSS evaluation fails, and its
  five-name expectation comes from an admitted-incomplete list. The check fails
  only when one of those five rendered names is returned; it does not fail for an
  omitted privileged group or an inability to enumerate groups.
- **Violation signature:** The prose list correctly treats wrong identity,
  privilege, or unexpectedly successful denial as violations
  (`IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:104-115`), but the cited
  executable check cannot reliably distinguish “not a member” from “membership
  was not evaluated.”
- **Required repair:** Freeze the numeric service UID/GID and the OS/profile
  privileged-group universe from an independent image inventory; capture and
  adjudicate command rc/stdout/stderr before comparing numeric group IDs; define
  exact login, sudo, read, write, and service-control probes; show RED for each
  prohibited capability and STOP for an unevaluable identity source.

### 2. Filesystem contract — NEEDS-REWORK

- **End state:** The path/owner/mode matrix and two writable directories are
  concrete (`IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:159-192`). One
  material permission boundary is knowingly unresolved: world-readable `0444`
  release files conflict with the broader prohibition on a lab identity reading
  “bridge material” (`IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:225-242`).
- **Check quality:** FS-01 relies on final-component `-L` checks
  (`IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:203-210`;
  `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:72-77` @ `2ce41e34`). A symlink or
  mount earlier in a path can still present a compliant-looking leaf. Owner checks
  compare resolver-rendered names rather than numeric IDs
  (`IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:80-92` @ `2ce41e34`). FS-04's
  not-yet-defined “acting as the service identity” probes test DAC only unless
  executed in the effective systemd sandbox; static `ReadWritePaths=` text does
  not prove the service view. The install-manifest binding is substring `grep`,
  not a whole structured parse (`IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:123-134`
  @ `2ce41e34`).
- **Violation signature:** The prose signature is broad enough
  (`IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:212-223`), but the current
  checks can pass a compliant leaf reached through a deviant path, wrong numeric
  ownership rendered with an accepted name, a decoy manifest string, or an
  ineffective sandbox.
- **Required repair:** Verify every path component and relevant mount boundary;
  use numeric ownership; parse the manifest with duplicate-key rejection and an
  independently pinned expected identity; enumerate recursive file **and
  directory** dispositions; test create/write/rename/delete inside the effective
  unit sandbox; falsify parent symlink, mount overlay, NSS-name remap, decoy JSON,
  added empty directory, and extra writable-path cases.

### 3. Network contract — NEEDS-REWORK

- **End state:** Concrete and mutually clear: exactly `127.0.0.1:8790`, SSH local
  forward only, UFW active/default-deny/SSH-only, no 8790 publication or proxy
  (`NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:11-18`).
- **Check quality:** The static proof cited at lines 24-25 is a literal source
  `grep`: it passes when the accepted bind string appears anywhere and the two
  forbidden strings do not (`IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:183-193`
  @ `2ce41e34`). Dead code or a comment can satisfy it while the executed bind is
  wrong. Worse, both socket helpers discard `ss` errors and append `|| true`, so
  empty output caused by an observation failure becomes PASS
  (`IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:196-219` @ `2ce41e34`). These are
  exactly checks that can pass without observation. The future tunnel/direct
  probe is useful but is not an independent proof that every proxy/NAT/publication
  path is absent (`NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:20-30`).
- **Violation signature:** The listed states distinguish intended compliance
  from violation (`NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:32-41`), but the
  verifier collapses “socket query failed” into “no socket” and cannot enforce
  the list.
- **Required repair:** Replace source-text proof with executed listener evidence;
  adjudicate tool rc/stderr/completeness before stdout; STOP on an unevaluable
  firewall/socket observation; bind the runtime process/executable to the frozen
  artifact; independently inventory host/container/proxy/provider exposure; show
  RED for dead-code decoy, `ss` failure, IPv6 listener, alternate port, proxy,
  published port, and direct-remote-reachability mutants.

### 4. Service contract — NEEDS-REWORK

- **End state:** First-start identity, ordering, hardening, graceful stop,
  `Restart=no`, DISARMED start, log policy, and steady-profile separation are
  concrete (`NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:51-61`). Resource-slice
  values remain UNKNOWN and require a separate measured owner decision
  (`NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:62`).
- **Check quality:** The directive audit and byte comparison inspect text produced
  from the accepted release template (`NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:65-76`;
  `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:155-201` @ `2ce41e34`). Text needles
  can sit in comments or overridden directives, and matching an installed unit to
  a template from the same release is self-consistency, not proof of effective
  systemd state. An external drop-in can change effective `User`, `Restart`,
  writable paths, environment, or hardening while both checks pass. Future start,
  stop, restart, and rotation observations are real in principle but have no RED
  demonstrations here.
- **Violation signature:** The violation list is semantically useful
  (`NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:80-90`), but static file checks do
  not distinguish an effective override from compliance.
- **Required repair:** Pin the expected unit hash outside the install process;
  enumerate and reject unapproved drop-ins; parse the unit; verify effective
  properties with systemd's own loader; bind the executed process/argv to the
  frozen release; specify measurable graceful-stop and restart-throttle outcomes;
  RED-test override, duplicate-directive, comment-decoy, premature SIGKILL,
  automatic restart, and logrotate-restart cases. Keep resource verification
  BLOCKED until the owner decision exists.

### 5. Secret contract — NEEDS-REWORK

- **End state and owner decision:** D4 is carried correctly: the wallet is
  deferred, item 4 blocks first start, and no key value may be requested,
  generated, stored, or referenced (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:30-36,58-63`;
  `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:80-87`).
  The future mechanism is conditional and contains names, not values
  (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:64-98`).
- **Contradiction:** The contract requires `HL_LIVE_ACK` to be absent from “the
  unit” and “evidence,” then declares its presence “in any form” a violation
  (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:87-89,117-133`). The service contract
  requires exact equality to a template whose comment literally contains that
  identifier (`NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:69-71`;
  `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:43-45`
  @ `2ce41e34`). Exact service compliance therefore violates the secret contract.
  The secret contract also contains the identifier itself, so “in any form” is
  not a discriminating signature.
- **Check quality:** “Absence of any request, generation, storage, or reference”
  across repository, chat, history, screenshots, backups, unit, process, and
  evidence has no frozen universe or executable producer
  (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:100-115`). It can currently pass by
  declaration. “One store only” also needs to say “one at-rest source”; the
  service process necessarily receives a runtime copy via `EnvironmentFile=`.
- **Required repair:** Define violation as a value-bearing assignment/exposure,
  not a policy-name mention; define the exact scoped artifact universe and an
  independent names-only scanner; forbid values in logs, journal, crash/core
  dumps, argv, diagnostics, evidence, and backups; define runtime consumer and
  at-rest-store boundaries; prove the scanner RED on injected synthetic
  value-shaped fixtures without using a real secret; STOP on inaccessible scope.

### 6. State contract — NEEDS-REWORK

- **End state and owner decision:** D5 is carried correctly: a fresh database,
  no inherited counters/history/foreign-position record, preserve-or-block, and
  unchanged single-writer proof (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:152-200`;
  `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-110`).
  The off-host archive question remains explicitly undecided, as the owner record
  requires (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:201-210`;
  `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:112-116`).
- **Check quality:** The “zero-invariant digest” and source-capture hash prove
  byte identity only if independently sourced; they do not themselves prove the
  database semantics (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:161-179`). The
  exact reset producer is UNKNOWN (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:265-280`),
  so the author of the artifact can also author the claimed zeros. “Absent/zero”
  is not one exact expected state. The preservation location, custody, retention,
  and later retrievability are also unspecified while the off-host choice remains
  open.
- **Violation signature:** The listed missing capture, mismatch, unknown,
  provenance, and start-blind cases are correct
  (`SECRET_AND_STATE_CONTRACTS_2026-08-15.md:232-249`), but no independent
  semantic verifier yet makes them observable.
- **Required repair:** Freeze the reset producer separately from a read-only
  verifier; define exact schema/query predicates for all four risk classes;
  capture source semantics before reset and destination semantics after reset;
  obtain expected values from the pre-cutover evidence and owner decision, not
  from the reset producer; require a chosen retrievable preservation location
  before cutover while leaving “off-host or old host” to the owner; show RED for
  non-empty, malformed, stale, missing-table, wrong-risk-day, corrupt, and
  hash-correct-but-semantically-wrong fixtures.

### 7. Recovery contract — NEEDS-REWORK

- **End state:** Baseline identity, rollback target, encrypted/versioned/locked
  backups, restore semantics, recovery-start gates, and access recovery are
  directionally concrete (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:64-105`).
  Provider, retention, credential choices and RPO/RTO remain OPEN/UNKNOWN
  (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:128-134,344-353`).
- **Check quality:** Verification accepts a rollback manifest containing both
  SHAs/unit hash plus exit 0 (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:107-117`).
  The rollback producer itself writes booleans claiming the service is masked,
  inactive, state preserved, secrets untouched, firewall unchanged, and Windows
  authority not restored (`IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh:157-184` @
  `25564449`). Checking that producer-authored manifest and its hash is
  self-confirming. The rollback also inherits the socket helper that can PASS on
  `ss` failure (`rollback.sh:88-100`; `common.sh:210-219` @ `2ce41e34`).
- **Violation signature:** It catches missing evidence but not false
  producer-authored evidence (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:119-126`).
- **Required repair:** Independently observe every rollback postcondition; pin
  expected release/unit/state identities before rollback; test restore from the
  retained backup into isolation and compare independent semantic queries; test
  retention/deletion denial with the write credential; RED-test no-op rollback,
  false manifest booleans, socket-observation failure, wrong release, missing
  risk evidence, and deletion-capable backup credentials.

### 8. Teardown contract — NEEDS-REWORK

- **End state:** The category list, never-restore list, export allowlist, and two
  route packets are useful and concrete at category level
  (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:144-174`).
- **Check quality:** The absence matrix quantifies only over the T1 inventory
  produced by the teardown process (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:176-181`).
  An omitted service, user, cache, credential name, container object, or network
  rule is outside the universe and silently passes. Calling the present category
  schema “correct, not a gap” does not establish future enumeration completeness
  (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:190-195`).
- **Violation signature:** It catches restoration of a listed T4 item or an
  incomplete declared inventory, but not an undeclared surviving member
  (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:183-188`).
- **Required repair:** Derive the pre-teardown universe from at least two
  independent sources (admission ledger plus actual OS/service/package/network/
  filesystem discovery), give every admitted member one terminal disposition,
  compare post-reprovision state with a frozen clean-profile allowlist, STOP on
  inaccessible namespaces or incomplete discovery, and show an injected omitted
  member makes the proof RED.

### 9. Maintenance contract — NEEDS-REWORK

- **End state:** The procedure and safety ordering are useful, but the actual
  unattended-upgrade scope/restart behavior is still only a requirement to write
  something later (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:205-239`).
  Thus a core end-state value is UNKNOWN. An owner-accepted package/origin,
  blackout, reboot, and restart policy would settle it.
- **Check quality:** “Pre/post diffs recorded and clean or explained” lets the
  same operator explain any drift, and a “hashed outcome” authenticates bytes,
  not correctness (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:241-246`).
  Unit-hash comparison against an install-produced manifest has no independent
  expectation unless that hash was frozen before the window.
- **Violation signature:** The list catches obvious unsafe updates/restarts but
  omits the undefined M1 scope and author-approved explanations
  (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:248-254`).
- **Required repair:** Freeze the exact allowed change set and expected hashes
  before the window; use an independent pre/post collector; require every delta
  to map to a preregistered allowed disposition or block; define an external
  adjudicator for exceptions; RED-test an undeclared package, unit drop-in,
  auto-reboot, armed restart, stale reconcile, and unexplained hash drift.

### 10. Incident contract — NEEDS-REWORK

- **End state:** Signals, alert-only automation, contamination steps,
  provider-panel handling, off-host detection, and evidence fields are concrete
  (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:270-307`).
  Requiring every incident to resolve to **exactly one** of resource/SLO or
  security-boundary breach is unsafe: one incident can be both. The contract
  supplies no precedence or combined class.
- **Check quality:** A drill using the same signal-to-response map for both
  expected and actual classification can confirm itself, and hashing the outcome
  does not validate the classification. Comparing revocation names only with the
  current secret inventory also misses any credential omitted from that inventory
  (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:309-314`).
- **Violation signature:** It catches missing distinctions and mutation-capable
  monitoring, but cannot distinguish a self-classified scenario or inventory
  omission from compliance (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:316-321`).
- **Required repair:** Permit dual classification or define conservative
  precedence; preregister scenarios and expected outcomes independently from the
  responder; test observer credentials/capabilities with a denied mutation
  attempt; derive the credential universe independently; RED-test combined
  resource/security incidents, misclassification, omitted revocation names,
  monitor mutation, and missing off-host heartbeat.

## Cross-cutting findings

1. **Required — resolve the secret/service literal contradiction.** The secret
   contract's “absent/present in any form” rule is incompatible with the exact
   service template. Scope it to definitions, assignments, and values.
2. **Required — resolve “bridge material.”** Identity prohibits lab reads of
   bridge material while filesystem mode `0444` deliberately permits reads of
   immutable non-executable release files. The identity/filesystem author already
   marks this UNKNOWN (`IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:225-242`).
   Owner/Lead must define protected material before lab admission.
3. **Required — separate frozen expectations from producer output.** Unit hashes,
   install/rollback manifests, invariant digests, evidence hashes, inventory
   universes, drill classifications, and “explained” diffs repeatedly come from
   the process being checked. Hashes establish byte identity, not truth.
4. **Required — STOP observation failures.** Identity enumeration and network
   socket checks can currently turn tool/NSS/query failure into compliance. Every
   probe must capture rc, stdout, stderr, and completeness before interpreting
   content.
5. **Required — verify effective state, not source text.** Grep and exact-template
   comparisons do not prove executed bind behavior, effective systemd properties,
   path ancestry/mount identity, or sandbox write boundaries.
6. **Required — close universe gaps.** Profile identity, privileged groups,
   teardown surfaces, proxies/publication paths, secret-storage surfaces, and
   revocation names all depend on declared lists that no independent process
   proves complete. Apply terminal accounting to every discovered member.
7. **Required — assign the state/recovery seam.** State should own cutover source
   capture, reset production, zero semantics, and preserve-or-block. Recovery
   should own later backup, restore, rollback, RPO/RTO, and access recovery. The
   current recovery R4 calls restore discipline “the fresh-reset branch”
   (`RECOVERY_TEARDOWN_MAINTENANCE_INCIDENT_CONTRACTS_2026-08-15.md:80-88`),
   duplicating state ownership and inviting divergence.
8. **Required — add the missing secret egress boundary.** Secret, service logging,
   recovery evidence, maintenance diffs, and incident raw evidence do not jointly
   define one enforceable rule for logs, journal, crash/core output, argv,
   diagnostics, screenshots, and evidence export. Define it once and cross-reference
   it from all contracts.
9. **Required — correct the contract count/index.** Four files contain ten
   contracts, not eight. A frozen index is needed so later acceptance cannot omit
   two contracts by scope ambiguity.

## Owner-decision consistency

- **D4 wallet deferral:** **CONSISTENT IN INTENT.** The secret contract preserves
  the deferral, first-start block, and prohibition on requesting/generating/
  storing/referencing a key value. It contains only published variable names, no
  value. The literal `HL_LIVE_ACK` wording still needs the repair above.
- **D5 start clean + preserve-or-block:** **CONSISTENT IN INTENT, INCOMPLETE AS A
  PROOF.** The state contract selects a fresh DB and carries all four evidence
  classes plus single-writer proof. It correctly leaves the archive-location
  choice open. The exact reset producer, semantic verifier, and guaranteed
  retrievable preservation location remain UNKNOWN; those must be frozen before
  cutover, not inferred from a hash.

## Secret-hygiene result

**Committed contract blobs: CLEAN for actual secret values and value-shaped
placeholders.** A targeted pattern scan plus full manual read found no credential
value or credential-shaped placeholder in the four files. The sole long hex value
is the published Gate-A candidate Git SHA at
`NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:5`; generic exact-SHA placeholders
are artifact identities, not credentials. Published environment-variable names
are identifiers, not values. This hygiene result does not cure the secret
contract's overbroad identifier-absence wording.

## Exit boundary

No host, network, SSH, deployment, service, credential, broker/exchange, ARM,
order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push,
product-code, or economic action was performed. No acceptance or authorization is
issued.
