# KVM2 Phase-2 v2 cross-check — lane HLCHK — 2026-08-16

## Verdict

**Overall: NEEDS-REWORK.** This is a T2 documentation/evidence verdict only. It is not
acceptance or authorization.

The v1 direct contradiction has been narrowed but **not closed**. The service contract now
defines a normative `HL_LIVE_ACK` boundary and says the secret contract must reproduce or
normatively cross-reference its exact surface list. The secret contract instead claims to
have the same boundary while carrying only a shorter subset. It does not cross-reference the
service rule, and it omits service-manager environment, pass-through/command-injection forms,
several unstructured egress surfaces, evidence-reader exposure, and the mandatory effective
`UnsetEnvironment=HL_LIVE_ACK` defense. Thus there is no longer an obvious policy-name/comment
contradiction, but there is a **deference/coverage gap**: a secret-side check can pass while a
service-side forbidden form exists.

The source artifacts reviewed are the actual parallel-lane outputs
`C:\tmp\lane_out\PH2A_CONTRACTS_V2_A.md` and
`C:\tmp\lane_out\PH2B_CONTRACTS_V2_B.md`. The v1 review is the actual lane output
`C:\tmp\lane_out\V2_PHASE2_CONTRACT_REVIEW.md`. The task's proposed integrated repository
paths do not exist in the detached `C:\RO` worktree or its `HEAD`; no substitute old contract
was silently used. Citations below therefore name the real reviewed files and lines.

Status terms in this report:

- **CLOSED** — the rewritten contract now states a discriminating rule that addresses the v1
  finding. This does not claim that its future verifier or RED/GREEN evidence exists.
- **PARTLY CLOSED** — false PASS is blocked or much less likely, but a required surface,
  expectation, decision, or executable specification is still missing.
- **OPEN** — the v1 defect remains materially unresolved.

## The `HL_LIVE_ACK` agreement test

The two drafts agree on two important points: identifier-only policy/comment mentions are
allowed, while active definitions and the effective process-environment key are forbidden
(`PH2A_CONTRACTS_V2_A.md:424-457`; `PH2B_CONTRACTS_V2_B.md:43-56`). That closes the literal
comment contradiction identified in v1 (`V2_PHASE2_CONTRACT_REVIEW.md:161-181`).

They do not agree on the complete enforcement universe:

| Surface or control | Service contract | Secret contract | Result |
|---|---|---|---|
| Identifier-only prose/comment/scanner result | Allowed at `PH2A_CONTRACTS_V2_A.md:450-457` | Allowed at `PH2B_CONTRACTS_V2_B.md:43-55` | Agree |
| Environment source assignment | Forbidden at `PH2A_CONTRACTS_V2_A.md:439-441` | Forbidden at `PH2B_CONTRACTS_V2_B.md:45-47` | Agree |
| Effective process environment | Forbidden at `PH2A_CONTRACTS_V2_A.md:437-438,466-468` | Forbidden at `PH2B_CONTRACTS_V2_B.md:46-49` | Agree |
| systemd **manager** environment | Explicitly forbidden and probed at `PH2A_CONTRACTS_V2_A.md:437-438,466-468` | Not named in the frozen universe or exact boundary at `PH2B_CONTRACTS_V2_B.md:43-54,63-72` | **Gap** |
| `PassEnvironment`, credential injection, and `ExecStart*`/other command injection | Explicitly forbidden at `PH2A_CONTRACTS_V2_A.md:442-445` | “effective unit environment” and active definition are named, but these source forms are not exhaustively named at `PH2B_CONTRACTS_V2_B.md:43-54` | **Gap** |
| argv | Forbidden at `PH2A_CONTRACTS_V2_A.md:446-449` | Forbidden at `PH2B_CONTRACTS_V2_B.md:49-50` | Agree |
| stdout/stderr, journal, logs, crash/core output, screenshots, backups, exported evidence | Every value-bearing `HL_LIVE_ACK` representation is forbidden at `PH2A_CONTRACTS_V2_A.md:446-449` | The exact boundary mentions only arguments and structured manifest/evidence/diagnostic fields; the broader rule at `PH2B_CONTRACTS_V2_B.md:39-42` applies to a **secret value**, not unambiguously to any `HL_LIVE_ACK` value | **Gap** |
| Evidence/verifier reads or emits the value | Explicitly forbidden at `PH2A_CONTRACTS_V2_A.md:449` | No equivalent exact prohibition at `PH2B_CONTRACTS_V2_B.md:43-54,63-76` | **Gap** |
| Effective `UnsetEnvironment=HL_LIVE_ACK` | Mandatory defense at `PH2A_CONTRACTS_V2_A.md:463-465` and mandatory PASS condition at `PH2A_CONTRACTS_V2_A.md:504` | Not required at `PH2B_CONTRACTS_V2_B.md:43-76` | **Gap** |
| Exact synthetic mutation matrix | Nine forbidden forms plus inaccessible-surface STOP at `PH2A_CONTRACTS_V2_A.md:474-480` | Generic “each named surface” wording at `PH2B_CONTRACTS_V2_B.md:73-76`, but the shorter named universe controls what is tested | **Gap** |

The service draft itself sets the agreement criterion: omission of a listed egress surface or
failure to reproduce/cross-reference the exact list blocks both contracts
(`PH2A_CONTRACTS_V2_A.md:482-486`). PH2B neither reproduces that list nor cross-references
PH2A. Therefore:

- **Service-side `HL_LIVE_ACK` repair: CLOSED as a standalone normative definition.**
- **Secret-side `HL_LIVE_ACK` repair: PARTLY CLOSED.**
- **Cross-contract agreement: OPEN / REQUEST_CHANGES.**

Minimal repair: make Contract 1 in PH2B normatively incorporate the complete PH2A §4.2
surface/control list, including manager environment, pass-through/command forms, all egress
surfaces, evidence-reader exposure, and effective `UnsetEnvironment`; then use one shared
mutation matrix. A prose claim that the boundaries are “the same” is not a substitute.

## Per-contract v1 finding closure and verdicts

### 1. Identity — PARTLY CLOSED; contract verdict: BLOCKED-PREREQUISITES

- **Numeric UID/GID and privileged/profile universes: PARTLY CLOSED.** The rewrite requires
  independently frozen numeric identities and complete allowed/privileged sets, but the values
  remain `UNKNOWN` (`PH2A_CONTRACTS_V2_A.md:54-85,110-119`). That is honest and fail-closed,
  but the contract is not executable until the independent record exists.
- **NSS/tool failure previously becoming “not a member”: CLOSED.** The common grammar
  adjudicates rc/stderr/completeness first, and ID-01/ID-02 STOP on NSS or enumeration failure
  (`PH2A_CONTRACTS_V2_A.md:26-47,147-148`).
- **Exact login, sudo, service-control, read/write, and effective-identity probes: CLOSED as
  design.** The probes, expected denial classes, canary behavior, stable numeric identity, and
  failure conditions are specified (`PH2A_CONTRACTS_V2_A.md:149-153,156-181`). The helper and
  canary hashes are still `UNKNOWN`, so no present proof exists (`PH2A_CONTRACTS_V2_A.md:182-187`).
- **RED/STOP requirements: CLOSED as design, not evidence.** Concrete NSS-remap, omitted-group,
  authorization, ACL, and drop-in mutants are named (`PH2A_CONTRACTS_V2_A.md:147-153`).

### 2. Filesystem — PARTLY CLOSED; contract verdict: OWNER/LEAD DECISION REQUIRED

- **Intermediate symlink/mount and final-leaf gap: CLOSED.** FS-01 verifies every component,
  mount identity, and the one mask exception; parent-symlink and overlay mutants must fail
  (`PH2A_CONTRACTS_V2_A.md:235-239,269-272`).
- **Resolver names instead of numeric owners: CLOSED.** The matrix and recursive verifier use
  numeric UID:GID (`PH2A_CONTRACTS_V2_A.md:216-226,272`).
- **File-only/incomplete recursive inventory: CLOSED.** FS-02 accounts for files, directories,
  special nodes, duplicates, omissions, and unreadable subtrees (`PH2A_CONTRACTS_V2_A.md:272`).
- **Substring manifest binding and same-producer expectation: CLOSED.** FS-03 requires strict
  parsing, duplicate-key/non-JSON rejection, independent identities, and exact tree binding
  (`PH2A_CONTRACTS_V2_A.md:273`).
- **DAC-only probe versus effective systemd sandbox: CLOSED.** FS-05 enters the running unit's
  attested mount namespace and tests create/write/rename/delete in both allowed and forbidden
  directions (`PH2A_CONTRACTS_V2_A.md:275`).
- **World-readable `0444` release material versus “lab cannot read bridge material”: OPEN.**
  The rewrite correctly refuses to guess and blocks lab admission, but the protected subset is
  still undecided (`PH2A_CONTRACTS_V2_A.md:241-265,276`). This is the v1 owner/Lead seam, not a
  closed contract value.

### 3. Network — PARTLY CLOSED; contract verdict: NEEDS-REWORK

- **Source grep versus executed listener: CLOSED.** Source text is demoted to lint; complete
  per-namespace socket census and process/artifact binding are required
  (`PH2A_CONTRACTS_V2_A.md:331-344`).
- **`ss`/query failure becoming empty-success: CLOSED.** NET-02 and NET-04 STOP on query,
  backend, parse, or completeness failure (`PH2A_CONTRACTS_V2_A.md:343,345`).
- **IPv6, alternate listener, decoy process, proxy/NAT/container/provider universe, and direct
  reachability: CLOSED as design.** Each has a named observation and RED fixture
  (`PH2A_CONTRACTS_V2_A.md:343-347`).
- **New self-confirming hole: OPEN.** NET-07 promises to catch an installer that adds and then
  removes a transient firewall rule, but its real observation specifies only pre/post hashes
  and semantic snapshots. Identical pre/post state can pass after the transient mutation; the
  RED cell mentions an “event/semantic capture” that the actual observation never defines
  (`PH2A_CONTRACTS_V2_A.md:348`). This is exactly a claim outrunning its probe. Add a pinned,
  independently collected event/audit stream or narrow the claim to net state at the two
  snapshots.

### 4. Service — PARTLY CLOSED; contract verdict: NEEDS-REWORK

- **Same-release template comparison and comment/duplicate/drop-in false PASS: CLOSED.** The
  rewrite requires externally frozen hashes, enumerates all unit sources/drop-ins, and checks
  systemd's loaded effective properties (`PH2A_CONTRACTS_V2_A.md:412-414,496-497`).
- **Process/artifact identity: CLOSED.** Runtime PID/invocation/argv/cwd/executable/module/cgroup
  binding is explicit (`PH2A_CONTRACTS_V2_A.md:499`).
- **Graceful stop, `Restart=no`, throttling, and logrotate behavior: CLOSED as bounded design.**
  Measurable outcomes and falsifications are given (`PH2A_CONTRACTS_V2_A.md:500-503`).
- **Resource values: OPEN but safely blocked.** The draft does not invent Slice/CPU/Memory/Task
  values and makes SVC-10 unverified until an owner-accepted record exists
  (`PH2A_CONTRACTS_V2_A.md:415-420,505`).
- **Secret/service contradiction: service side CLOSED, cross-contract OPEN.** See the seam table
  above.
- **New temporal universe gap: PARTLY OPEN.** SVC-05 observes 600 seconds and says an external
  restart trigger must fail, but it does not independently enumerate timers, path units,
  schedulers, or other activation sources. A trigger scheduled after the window can satisfy the
  check while the broad “no automatic retry/restart loop” claim is false
  (`PH2A_CONTRACTS_V2_A.md:397-405,500`). Either enumerate all activation sources or narrow the
  claim to the observed interval.

### 5. Secret — PARTLY CLOSED; contract verdict: NEEDS-REWORK

- **D4 wallet deferral and first-start block: CLOSED.** No wallet is requested, inferred,
  generated, stored, or represented by a key value; item 4 remains blocking
  (`PH2B_CONTRACTS_V2_B.md:29-31,58-62`).
- **One store versus runtime copy: CLOSED.** It now says one at-rest source and distinguishes
  the process environment copy (`PH2B_CONTRACTS_V2_B.md:32-38`).
- **“Present in any form” literal contradiction: PARTLY CLOSED.** Identifier-only policy
  mentions are allowed, but the shorter exact boundary does not cover the full service-side
  universe (`PH2B_CONTRACTS_V2_B.md:43-56`).
- **Frozen secret-scan universe and STOP on inaccessible scope: PARTLY CLOSED.** Candidate,
  unit, environment, evidence, log/crash, and backup categories are named and incomplete
  enumeration STOPs (`PH2B_CONTRACTS_V2_B.md:63-72`). External chat/history/screenshot
  universes remain explicitly `UNKNOWN`, which is safe but not a completeness proof
  (`PH2B_CONTRACTS_V2_B.md:86-91`).
- **Synthetic RED/GREEN scanner evidence: CLOSED as design, not execution.** The real scanner
  must reject active definitions and synthetic egress sentinels, accept bare comments, and
  STOP on unreadable members (`PH2B_CONTRACTS_V2_B.md:73-76`).
- **Missing complete `HL_LIVE_ACK` egress/control boundary: OPEN.** This is the blocking seam.

### 6. State — PARTLY CLOSED; contract verdict: BLOCKED ON EXACT SEMANTICS

- **D5 fresh reset and all four preserve-or-block evidence classes: CLOSED.** Daily loss,
  consecutive loss, order history, and foreign-position state are all named; source capture
  and retrievability block reset/start if absent (`PH2B_CONTRACTS_V2_B.md:97-108`).
- **Archive question: CLOSED as an open branch.** Both off-host archive and retained old-host
  state remain admissible, and no branch is presumed (`PH2B_CONTRACTS_V2_B.md:109-113`).
- **Reset producer supplying its own zeros: CLOSED structurally.** Producer and read-only
  verifier must be separate; byte digests are supplemental (`PH2B_CONTRACTS_V2_B.md:114-118`).
- **Exact clean predicates: OPEN.** Exact tables, columns, risk day, and representations remain
  `UNKNOWN`, and the exact reset command is out of scope (`PH2B_CONTRACTS_V2_B.md:100-104,147-151`).
  Blocking is correct, but the v1 demand to define exact schema/query predicates is not yet
  fulfilled.
- **Semantic RED fixtures: CLOSED as design.** Non-empty, stale, wrong-day, missing-table,
  malformed, corrupt, byte-matching/semantically-wrong, and incomplete-read cases are named
  (`PH2B_CONTRACTS_V2_B.md:120-138`).

### 7. Recovery — PARTLY CLOSED; contract verdict: BLOCKED-PREREQUISITES

- **State/recovery ownership seam: CLOSED.** Recovery consumes state's accepted source/destination
  evidence instead of re-adjudicating the reset branch (`PH2B_CONTRACTS_V2_B.md:158-160`).
- **Open archive branch: CLOSED as conditional design.** Both owner choices use the same identity
  and semantic verifier and block on loss/mismatch (`PH2B_CONTRACTS_V2_B.md:161-165`).
- **Producer-authored rollback manifest: CLOSED.** It is supplemental; postconditions are
  independently observed against identities frozen before rollback
  (`PH2B_CONTRACTS_V2_B.md:172-175,186-188`).
- **Restore semantics and retention denial: CLOSED as design.** Isolated semantic restore and
  denied deletion/retention mutation with the routine role are required
  (`PH2B_CONTRACTS_V2_B.md:180-195`).
- **Provider, retention duration, and RPO/RTO: OPEN/UNKNOWN.** The rewrite preserves those owner
  decisions as prerequisites rather than guessing (`PH2B_CONTRACTS_V2_B.md:166-171,204-207`).

### 8. Teardown — CLOSED as contract; contract verdict: BLOCKED ON FROZEN ALLOWLIST

- **Self-declared T1 inventory: CLOSED.** The universe is the union of admission records and
  independent discovery over the full named category set (`PH2B_CONTRACTS_V2_B.md:213-216`).
- **Omitted member and conservation: CLOSED.** Every discovered member retains a stable identity
  and one terminal disposition; discovered-unregistered members block
  (`PH2B_CONTRACTS_V2_B.md:217-220,231-236`).
- **Post-reprovision proof: CLOSED as design.** Independent rediscovery compares with a pre-frozen
  clean-profile allowlist and STOPs on inaccessible namespaces/categories
  (`PH2B_CONTRACTS_V2_B.md:222-224,237-239`).
- **Injected omitted member: CLOSED as design.** The real proof must discover it and go RED/BLOCK
  (`PH2B_CONTRACTS_V2_B.md:240-243`).
- The exact clean allowlist remains `UNKNOWN`, so no execution verdict is possible
  (`PH2B_CONTRACTS_V2_B.md:251-254`).

### 9. Maintenance — PARTLY CLOSED; contract verdict: BLOCKED ON OWNER POLICY

- **Undefined unattended-upgrade/restart policy: OPEN but safely blocked.** Automatic updates
  remain disabled; allowed origins/packages/grammar/blackout/reboot/restart values are still
  `UNKNOWN` (`PH2B_CONTRACTS_V2_B.md:258-263`).
- **Operator explains its own drift: CLOSED.** Every delta must map to a pre-frozen allowed
  disposition, and exceptions require an independent adjudicator
  (`PH2B_CONTRACTS_V2_B.md:264-270`).
- **Same-producer hashes/source-only unit check: CLOSED.** Independent collectors include effective
  unit/drop-in state; digests do not adjudicate correctness (`PH2B_CONTRACTS_V2_B.md:271-284`).
- **Required mutants: CLOSED as design.** Undeclared package, drop-in, reboot/restart, stale
  reconciliation, and unexplained drift must fail (`PH2B_CONTRACTS_V2_B.md:286-289`).

### 10. Incident — CLOSED as contract; contract verdict: BLOCKED-PREREQUISITES

- **Unsafe exactly-one classification: CLOSED.** Two independent booleans permit combined
  resource/security incidents and give the security branch conservative precedence
  (`PH2B_CONTRACTS_V2_B.md:307-310`).
- **Responder supplies expected result: CLOSED.** An independent scenario author freezes both
  expected booleans before response (`PH2B_CONTRACTS_V2_B.md:326-330`).
- **Monitoring capability assertion: CLOSED.** Capability is independently enumerated and a safe
  mutation attempt must be denied (`PH2B_CONTRACTS_V2_B.md:331-334`).
- **Revocation inventory omission: CLOSED structurally.** Names-only inventory is unioned with
  independent discovery and terminal accounting (`PH2B_CONTRACTS_V2_B.md:318-321,335-338`).
- **Dual-event, omission, mutation, heartbeat, and secret-egress mutants: CLOSED as design**
  (`PH2B_CONTRACTS_V2_B.md:339-342`). Exact thresholds/provider/timing remain `UNKNOWN`
  prerequisites (`PH2B_CONTRACTS_V2_B.md:351-355`).

## Cross-cutting findings

1. **REQUIRED — `HL_LIVE_ACK` agreement remains open.** The service rule is broader and
   explicitly requires exact reproduction/cross-reference; the secret rule supplies neither.
2. **REQUIRED — protected “bridge material” remains open.** The filesystem draft safely blocks
   admission but does not decide whether the `0444` release subset is protected
   (`PH2A_CONTRACTS_V2_A.md:241-265`).
3. **PARTLY CLOSED — producer/expectation separation.** Both drafts impose independent frozen
   expectations (`PH2A_CONTRACTS_V2_A.md:54-85`; `PH2B_CONTRACTS_V2_B.md:12-23`), but the
   actual identity, hash, semantic, allowlist, provider, and policy records remain absent or
   `UNKNOWN`. No PASS may be issued yet.
4. **CLOSED as contract rule — observation failures STOP.** Both drafts bind this ordering
   (`PH2A_CONTRACTS_V2_A.md:26-47`; `PH2B_CONTRACTS_V2_B.md:12-23`).
5. **CLOSED as contract rule — effective state replaces source text.** Filesystem runtime
   sandboxing, listener/process binding, loaded systemd properties, rollback observation, and
   maintenance effective-state collection are specified.
6. **PARTLY CLOSED — universe gaps.** The contracts now require independent multi-source
   discovery and terminal accounting, but the actual identity/group, provider, protected-file,
   secret-egress, clean-profile, and credential-name universes are not yet frozen. The drafts
   block rather than pass, which removes the false-positive path but does not supply the
   missing universes.
7. **CLOSED — state/recovery seam.** State owns capture/reset/clean semantics/preserve-or-block;
   recovery owns later backup/restore/rollback/objectives
   (`PH2B_CONTRACTS_V2_B.md:114-118,158-175`).
8. **PARTLY CLOSED — one secret-egress boundary.** PH2B Contract 1 is reused by recovery,
   teardown, maintenance, and incident, but it is not coextensive with PH2A's exact
   `HL_LIVE_ACK` egress boundary. One normative shared list is still missing.
9. **PARTLY CLOSED — ten-contract index.** The outputs consistently say four plus six equals ten
   and name the sets (`PH2A_CONTRACTS_V2_A.md:1-16`; `PH2B_CONTRACTS_V2_B.md:1-9`), but no
   single frozen index binds all ten contract identities/versions. The v1 omission risk is
   reduced, not eliminated.
10. **NEW REQUIRED — NET-07 can pass after transient mutation.** Pre/post equality does not prove
    no intervening change; its proposed transient mutant needs an actual event/audit source
    (`PH2A_CONTRACTS_V2_A.md:348`).
11. **NEW REQUIRED — SVC-05's broad no-restart claim exceeds its bounded observation.** Either
    enumerate every activation source or scope the claim to the observed 600-second interval
    (`PH2A_CONTRACTS_V2_A.md:397-405,500`).

## New cross-lane contradictions or ambiguities

No additional direct A-versus-B logical contradiction was found in wallet deferral,
start-clean, archive branching, state/recovery ownership, secret-free backups, teardown
exports, maintenance, or incident handling. Two cross-lane ambiguities require explicit
resolution:

1. **The asserted `HL_LIVE_ACK` equivalence is false.** PH2B says it gives the service
   contract “the same checkable boundary” (`PH2B_CONTRACTS_V2_B.md:52-56`), while PH2A's
   mandatory agreement test includes surfaces and controls PH2B omits
   (`PH2A_CONTRACTS_V2_A.md:437-486`). This is a new claim-to-content contradiction created
   by the rewrites.
2. **Wallet delivery channel versus canonical env path is ambiguous, not yet a proven direct
   contradiction.** PH2B says the concrete future delivery channel is `UNKNOWN`
   (`PH2B_CONTRACTS_V2_B.md:32-38`), while PH2A requires an
   `/etc/mtc-bridge/mtc-bridge.env` file in the filesystem matrix and treats it as an
   environment source (`PH2A_CONTRACTS_V2_A.md:222-224,439-441`). The documents can agree if
   that path currently carries only non-wallet configuration and does not preselect the wallet
   channel. They do not say so. The wallet mechanism must remain `UNKNOWN` unless a later
   owner record selects it; PH2A should explicitly state that its path does not make that
   selection.

## Owner-decision consistency

- **Wallet deferred: CONSISTENT.** PH2B carries the no-request/no-inference/no-generation/
  no-storage/no-key-value rule and blocks first start (`PH2B_CONTRACTS_V2_B.md:29-31`). PH2A
  also states no first start and preserves the wallet blocker (`PH2A_CONTRACTS_V2_A.md:421-422`).
  This matches D4 (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:80-87`
  @ `a4833939`).
- **Start clean plus preserve-or-block: CONSISTENT.** PH2B requires a fresh destination and
  explicitly names daily loss, consecutive loss, orders, foreign positions, retrievable
  pre-reset capture, and unchanged single-writer evidence (`PH2B_CONTRACTS_V2_B.md:97-108`).
  This matches D5 (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-110` @ `a4833939`).
- **Archive question: CONSISTENTLY OPEN.** State and recovery both preserve the off-host versus
  retained-old-host branches, require a recorded owner choice before cutover/recovery, and do
  not assume either (`PH2B_CONTRACTS_V2_B.md:109-113,161-165`). This matches the open owner
  sub-question (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:112-116` @ `a4833939`).
- **No guessed values:** candidate identities, numeric IDs, semantic predicates, resource
  ceilings, archive choice, provider, retention, and policy values are explicitly `UNKNOWN`
  or blocked where the sources do not establish them (`PH2A_CONTRACTS_V2_A.md:81-85,412-420`;
  `PH2B_CONTRACTS_V2_B.md:100-104,109-113,166-171,258-263`).

## Secret-hygiene grep

Both complete rewritten documents were scanned for credential-like assignments, common
token/key prefixes, PEM/OpenSSH material, long hexadecimal values, and key/secret/token/
wallet/password/credential-shaped placeholders. Every hit is reported here:

1. `PH2A_CONTRACTS_V2_A.md:170` contains the option `--no-ask-password`; it is a command-line
   switch, not a password or value.
2. `PH2A_CONTRACTS_V2_A.md:326,382,411,419` were heuristic prefix hits caused by the substring
   `rk-` inside `NETWORK-...` path/citation text; they contain no credential value.
3. `PH2A_CONTRACTS_V2_A.md:454,464` contain
   `UnsetEnvironment=HL_LIVE_ACK`; this is the identifier-only enforcement directive the
   contract deliberately allows, not an acknowledgment or secret value.
4. `PH2A_CONTRACTS_V2_A.md:215` contains the artifact placeholder
   `<exact-40-hex-sha>`. It is SHA-shaped and therefore reported, but it denotes a Git/release
   identity, not a wallet/key placeholder. No 32-or-more literal hex value appears in either
   draft.
5. `PH2A_CONTRACTS_V2_A.md:398` contains the non-secret configuration literal
   `credential_free_disarmed` as the required start mode. It is not a credential value.

Result: **no wallet key value, key-shaped wallet placeholder, token, password, private-key
material, bearer value, long literal hex value, or plausible secret example value was found**
in either document. Published variable names, short Git citations, numeric modes/ports, and
the artifact-SHA placeholder are not secret values. This hygiene result does not repair the
secret/service coverage gap.

## Required repair set

1. Make PH2B Contract 1 normatively incorporate PH2A §4.2's complete `HL_LIVE_ACK` surface,
   enforcement, STOP, and mutation list; do not rely on an assertion of sameness.
2. Add event/audit observation to NET-07 or narrow its claim so add-then-remove mutations are
   outside the asserted property.
3. Enumerate every service activation source for SVC-05 or narrow the no-restart claim to the
   recorded interval.
4. Resolve the protected `0444` release-material owner/Lead seam before lab admission.
5. Freeze the exact state semantic predicates before cutover; preserve the archive branch as
   an owner choice.
6. Add one frozen ten-contract index binding both v2 artifacts and all ten contract names.
7. Clarify that PH2A's environment-file path does not select the deferred wallet delivery
   channel.

## Boundary

No host, network, SSH, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, product-code, or economic
action was performed. Nothing in this report is acceptance or authorization.
