Status: PHASE2 CONTRACT SET V3 — identity/filesystem/network/service — SUPERSEDES V2 — NOT ACCEPTED

# KVM2 Phase-2 V3 identity, filesystem, network, and service contracts

## Finding-closure table

| Finding | V3 mechanism | Cite |
|---|---|---|
| Identity admission values/universes were still absent | One exact record, `KVM2_PHASE2_ADMISSION_RECORD_V3`, has a mandatory `identity` object containing numeric `SERVICE_UID`, `SERVICE_GID`, the complete selected-profile identity/membership universe, and the complete privileged/control-capable numeric-GID universe. Its independent producer, source reconciliation, freeze order, validation, and absence-to-STOP rule are binding. Values remain `UNKNOWN`; none is invented here. | `KV1_PHASE2_V2_VERDICTS.md:11`; `KR1_IFNS_CONTRACTS_V3.md:65-117` |
| The path-level decision for the `0444` release subset was absent | One owner/Lead input, `KVM2_0444_PROTECTED_MATERIAL_DECISION_V1`, must disposition every `0444` release path. FS-00 and the aggregate filesystem verdict STOP while it is absent, incomplete, or not bound to the exact candidate inventory. No other filesystem check can produce an aggregate PASS around it. | `KV1_PHASE2_V2_VERDICTS.md:12`; `KR1_IFNS_CONTRACTS_V3.md:123-141,277` |
| FS-01 demanded impossible pre-install inode pins or allowed post-install blessing | FS-01 no longer compares installer-created inode numbers with an expectation. It uses pre-install path/type/mount-policy expectations, fd-relative no-follow resolution, and start/end device/inode observations only as within-run replacement/race detectors. A post-install snapshot is never an expectation. | `KV1_PHASE2_V2_VERDICTS.md:24`; `KR1_IFNS_CONTRACTS_V3.md:278` |
| NET-07 could not see add-then-remove mutations | V3 deliberately narrows NET-07 to equality of two independently captured endpoints. It makes no claim about transient mutations between them because no concrete pinnable event/audit stream is established in the reviewed KVM2 design. | `KV1_PHASE2_V2_VERDICTS.md:25`; `KR1_IFNS_CONTRACTS_V3.md:329` |
| SVC-05 converted 600 seconds into an unbounded no-restart claim | V3 limits SVC-05 to the closed recorded interval from watcher-ready through at least 600 continuous seconds. It makes no claim before or after that interval because no complete activation-source enumeration mechanism is established. | `KV1_PHASE2_V2_VERDICTS.md:26`; `KR1_IFNS_CONTRACTS_V3.md:415` |
| Service egress prohibition exceeded scanner coverage | The service-egress universe now covers manager/process environment, unit/environment/command sources, argv, stdout/stderr, journal, logs, diagnostics, crash/core output, screenshots, backups, and exported evidence. A named independent universe record supplies every collector and scope; any inaccessible or unenumerated surface STOPs SVC-09 and the service aggregate. | `KV1_PHASE2_V2_VERDICTS.md:29`; `KR1_IFNS_CONTRACTS_V3.md:144-170,373-404,419` |

The v1 review required numeric identities, complete universes, path/mount checks,
runtime network evidence, effective systemd state, independent expectations, and
STOP on inability (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:43-151,302-337`). V2
closed the named executable-check defects but retained the prerequisites and new
false-PASS paths listed above (`PHASE2_V2_CROSSCHECK_2026-08-16.md:71-144`). V3
keeps every closed mechanism and repairs only those remaining paths.

## 0. Common contract

### 0.1 Scope and authority

This is a full replacement for
`IDENTITY_FILESYSTEM_NETWORK_SERVICE_V2_2026-08-15.md`. It defines four design
contracts. It is documentation/evidence only: no host observation, RED/GREEN
execution, owner decision, admission, acceptance, or authorization exists here.
All current host values and states are `UNKNOWN`.

No host, network, SSH, deployment, service, credential, broker/exchange, ARM,
order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, Git
mutation, product-code, or economic action is authorized or performed.

### 0.2 Outcome grammar and aggregation

Every check has exactly one terminal outcome:

- `PASS`: every named observation completed, its domain and universe were
  established, and the result equals an expectation frozen by an independent
  producer before the checked producer ran.
- `FAIL`: the observation completed and positively found deviant state. An
  observably absent required object is FAIL, not STOP.
- `STOP`: the property could not be evaluated because an expectation, source,
  identity, namespace, tool, parser, walk, event interval, provider scope, or
  evidence surface was absent, inaccessible, incomplete, raced, timed out, or
  returned an unclassified result. STOP is never converted to PASS or FAIL.

Each probe records the case ID, profile, candidate identity, host/namespace
attestation, verifier identity, pinned tool paths/hashes, expectation-record ID
and hash, start/end monotonic times, rc, complete stdout/stderr or separately
retained content-free captures, parsed result, terminal outcome, and reason.
The verifier adjudicates rc, stderr, completeness, and read termination before
interpreting stdout (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:368-420`).

Contract aggregation is fail-closed: any required FAIL makes the contract FAIL;
otherwise any required STOP makes the contract STOP; PASS requires every
required case to PASS. A local PASS cannot bypass a prerequisite STOP. The host
claim is limited to the named KVM2 image in its externally attested initial user,
mount, PID, and network namespaces; equality with locally visible PID 1 is not
enough (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:111-176`).

### 0.3 The one independent admission record

The only admission expectation record for these four contracts is named
`KVM2_PHASE2_ADMISSION_RECORD_V3`. Its storage locator, record ID, hash, values,
and approved instance are currently `UNKNOWN`; therefore every case consuming
it currently STOPs.

Its exact schema is:

1. `metadata`: schema/version; immutable record ID; exact base-image identity;
   exact selected profile; exact candidate Git/release/venv identities; creation
   time; producer executable identity/hash; owner/Lead approval identity and
   detached record hash; and a freeze-order statement proving the record was
   sealed before installer, renderer, service, resetter, or verifier execution.
2. `sources`: stable ID, capture time, producer identity/hash, content hash,
   completeness result, and terminal member count for every accepted-image,
   profile-policy, Git-object, package, NSS/account/group, filesystem/mount,
   systemd, host/network, provider-control-plane, and evidence-custody source.
3. `identity`: numeric `SERVICE_UID`; numeric `SERVICE_GID`; exact non-login
   shell path/hash; and, for each selected profile, the complete expected user,
   group, membership, absent-identity, allowed-supplementary-GID, and
   service-control-denial universes. `privileged_gids` contains every numeric
   privileged/control-capable GID plus the exact policy/object/source that makes
   it privileged. Every source member has one stable identity and one terminal
   disposition; counts must conserve across capture, parse, normalization, and
   record emission.
4. `filesystem`: exact path/type/numeric-owner/mode/size/digest inventories for
   release, venv, configuration, state, logs, unit, mask, and logrotate objects;
   the allowed mount/topology policy and stable backing-filesystem identities;
   and the hash of `KVM2_0444_PROTECTED_MATERIAL_DECISION_V1`. It contains no
   expected inode number for an object the installer will create.
5. `network`: the admitted namespace, listener, firewall, proxy, container,
   tunnel-policy, provider-object, and external-observer universes, with exact
   collectors, scopes, schemas, and terminal counts.
6. `service`: independently rendered vendor-unit and logrotate hashes; approved
   fragment/mask/drop-in/alias universe; exact effective systemd properties;
   process/artifact identities; event-watcher identity; bounded timing values;
   and the hash of `KVM2_PHASE2_SERVICE_EGRESS_UNIVERSE_V1`.
7. `verifier`: exact verifier/harness and pinned helper identities/hashes,
   evidence schema, denial result grammar, timeout grammar, and expected
   terminal reason set for every check.

The named producer is `KVM2_PHASE2_ADMISSION_RECORD_PRODUCER_V1`, operated under
owner/Lead control against accepted image/profile/Git/provider sources before
the checked producers run. It must not import an installer/service/verifier
manifest as an expectation, and its executable identity/hash must differ from
the checked installer, renderer, service, and verification harness. The producer
must reconcile every configured NSS backend and every named source to terminal
accounting; inability to enumerate even one backend/source makes record
production STOP. A value copied or blessed after installation is invalid and
makes consumption STOP. This is the independent-input rule required by the
self-confirming-check pattern (`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`).

`SERVICE_UID`, `SERVICE_GID`, both profile universes, the privileged-GID
universe, candidate identities, hashes, mount identities, provider inventories,
and resource values are `UNKNOWN`. V3 defines where they must come from; it does
not invent them.

### 0.4 Single owner/Lead input for the `0444` subset

The sole decision input is named
`KVM2_0444_PROTECTED_MATERIAL_DECISION_V1`. The owner/Lead—not this contract,
the installer, or the verifier—must sign it. It contains the exact candidate
inventory hash and one row for every regular release member whose required mode
is `0444`: canonical relative path, artifact digest, and exactly one disposition:
`PROTECTED_DENY_LAB_READ` or `INTENTIONALLY_LAB_READABLE_NONPROTECTED`.

The set of decision paths must equal the independently frozen `0444` release
inventory exactly, with no missing, extra, duplicate, glob, prefix, inherited,
or default disposition. For protected rows it must also name the independently
approved denial mechanism and expected denial class. The decision's locator,
hash, rows, and owner/Lead choice are currently `UNKNOWN`.

Absence, wrong candidate binding, incomplete conservation, or an undecided row
makes FS-00, FS-06, the profile diff, and the aggregate filesystem contract
STOP. No other filesystem result can yield aggregate PASS around this STOP.
This preserves the v1 owner/Lead seam instead of deciding it in the contract
(`PHASE2_CONTRACT_REVIEW_2026-08-15.md:70-98,304-311`).

### 0.5 Independent service-egress universe record

`KVM2_PHASE2_SERVICE_EGRESS_UNIVERSE_V1` is a mandatory names-only record
produced by an evidence-custody collector independent of the service, installer,
unit renderer, backup/export producer, and scanner. It is frozen for the exact
candidate and rehearsal before SVC-09 runs, and its hash is sealed into the
admission record. It supplies exact collectors, roots/provider scopes, object
IDs, schemas, and terminal counts for every prohibited surface:

1. systemd manager environment and NUL-delimited service-process environment;
2. vendor/drop-in/transient unit sources, all `EnvironmentFile` sources, launch
   wrappers, profiles, generated environment sources, and every `ExecStart*` or
   other service-command source;
3. NUL-delimited runtime argv;
4. service stdout/stderr captures, journal records, current/rotated logs, and
   diagnostic bundles;
5. crash reports, core-dump metadata/content custody, and failure captures;
6. every screenshot object in the frozen rehearsal/evidence-custody scope;
7. every local/provider backup catalog, version, object manifest, and backup
   index in the frozen scope; and
8. every exported-evidence manifest, export object, report, attachment, and
   verifier capture in the frozen scope.

Each category must reconcile at least the preregistered custody/catalog source
with actual filesystem/provider/runtime discovery. Every discovered member gets
one stable identity and terminal disposition. An absent root/scope, inaccessible
catalog, unsupported format, dropped member, or unexplained count difference
makes SVC-09 and the service aggregate STOP. The record and all scope values are
currently `UNKNOWN`; no service-egress PASS exists while it is absent.

### 0.6 Falsification and evidence rule

Every check below names an independent expectation source, an inability-to-
evaluate STOP, and one sentence beginning “This check fails when”. A check does
not count as evidence until its real top-level verifier is shown RED against that
fixture or an equivalent deliberate mutation and GREEN with the conforming
state, with literal commands and real outputs retained. A reimplementation of
the predicate is supplemental only (`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-83`).

### 0.7 V3 change log

| Area | Choice | Why |
|---|---|---|
| Identity | Defined one exact admission record and made its absence STOP. | The required numeric values and complete universes do not yet exist; inventing them would be false evidence (`KV1_PHASE2_V2_VERDICTS.md:11`). |
| Filesystem `0444` | Reserved the decision to one named owner/Lead input with an aggregate STOP. | The sources do not establish the protected-material disposition (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:70-98`). |
| FS-01 inode | Removed pre-install inode expectations; retained inode/device only for within-run stability. | Installer-created inode numbers cannot be independently known before creation, while a post-install baseline can bless a replacement (`KV1_PHASE2_V2_VERDICTS.md:24`). |
| NET-07 | Narrowed to endpoint equality only. | No concrete pinnable independent event/audit stream exists in the reviewed KVM2 design; pre/post equality cannot prove no transient mutation (`KV1_PHASE2_V2_VERDICTS.md:25`). |
| SVC-05 | Narrowed to the continuously observed interval. | No complete mechanism enumerates all timers, path units, schedulers, external orchestrators, or later activations (`KV1_PHASE2_V2_VERDICTS.md:26`). |
| Service egress | Extended the independent scanner universe to every prohibited surface. | V2 omitted argv, screenshots, backups, and some exported evidence from the scanner mechanism (`KV1_PHASE2_V2_VERDICTS.md:29`). |

## 1. Identity contract

### 1.1 Required end state

1. One dedicated system account and primary group named `mtc-bridge` exist with
   home `/var/lib/mtc-bridge` and the independently frozen non-login shell. A
   pre-existing identity with different attributes fails.
2. Its numeric UID and primary GID equal `SERVICE_UID:SERVICE_GID` from the one
   admission record. Resolver-rendered names are diagnostic only.
3. Its complete supplementary numeric-GID set equals the selected profile's
   frozen allowed set and is disjoint from the complete frozen privileged-GID
   set. No fixed five-name list is accepted as complete.
4. In `temporary-testnet-lab`, `mtc-bridge` exists and every lab identity and
   lab-owned surface is absent before any separate lab admission. A cross-user
   probe STOPs while its exact probe identity is absent.
5. In `future-trading-only`, every lab user, membership, home, agent, runner,
   browser-automation identity, scheduler/workflow identity, container identity,
   and lab credential owner is absent. Every remaining identity has one terminal
   disposition in the frozen profile universe.
6. Effective loaded-unit and process identities equal the numeric frozen tuple;
   source text alone is insufficient.

These preserve the v1 end state while closing its name/failure/universe defects
(`PHASE2_CONTRACT_REVIEW_2026-08-15.md:43-68`).

### 1.2 Verification

| Case | Observation and independent expectation | PASS / FAIL / STOP | One-line falsification |
|---|---|---|---|
| ID-01 account tuple | Parse exactly one complete `getent passwd mtc-bridge` record and reconcile `id -u`, `id -g`, and `getent group` numeric results with the admission record's identity object. | PASS only for one consistent frozen tuple, home, and shell. Missing/mismatched observed identity FAILs. Record/NSS/tool/parse/timeout or duplicate inconsistency STOPs. | This check fails when wrong numeric IDs render with accepted names; an NSS evaluation failure must STOP. |
| ID-02 complete group disposition | Capture numeric primary and all numeric supplementary GIDs; assign every returned and expected GID exactly one stable disposition and compare with the admission record's complete profile and privileged-GID universes. | PASS requires exact conservation and no privileged GID. Extra/prohibited GID FAILs. Missing record, backend/enumeration error, duplicate identity, or unclassified GID STOPs. | This check fails when a privileged GID omitted by the old five-name list is added; nonzero `id` with empty output must STOP. |
| ID-03 login and sudo denial | Use the admission record's shell, image-policy sources, probe/helper hashes, and exact denial grammar; execute login-style and `sudo -n` inert-marker probes under the numeric service tuple with cleared groups. | PASS requires both frozen authority-denial classes and no marker. Command execution or sudo success FAILs. Missing policy/tool/canary or ambiguous status STOPs. | This check fails when the shell becomes login-capable or a matching passwordless sudo rule lets the frozen marker execute. |
| ID-04 service-control denial | Independently enumerate sudoers, polkit, D-Bus, and unit-specific authorization sources recorded by the admission producer; run `pkcheck` and attempt a loaded inert canary whose only action is a marker. | PASS requires a classified authority denial, no marker, and complete rule accounting. Authorization or marker success FAILs. Missing canary/source, inaccessible policy, or non-classified denial STOPs. | This check fails when a matching control grant is added and the canary marker executes. |
| ID-05 profile identity universe | Enumerate every configured NSS backend plus local account/group databases and profile admissions; compare stable numeric identities with the complete admission-record universe using terminal conservation. | PASS requires exact selected-profile equality. Undeclared/forbidden observed identity FAILs. Any backend/source inability, malformed readable member, or count drift STOPs. | This check fails when an unlisted lab account is added or a malformed readable group member would otherwise disappear. |
| ID-06 cross-user path denials | With the admission record's exact numeric probe identity and protected-path matrix, use a pinned `openat2` syscall helper with cleared groups to attempt read/create/write/rename/delete and classify actual errno. | PASS requires the frozen denial class for every operation and no mutation. Any forbidden success FAILs. Missing probe identity, open `0444` decision, incomplete set, namespace/helper error, or unknown errno STOPs. | This check fails when one ACL or supplementary GID grants an operation that the protected matrix forbids. |
| ID-07 effective service identity | From the loaded unit capture effective identity properties and bind MainPID `/proc` numeric Uid/Gid/Groups to the one admission record. | PASS requires exact effective/process tuple and allowed groups. Drift FAILs. Manager/proc race/access failure or absent pins STOPs. | This check fails when an external drop-in changes `User` or `SupplementaryGroups` while vendor bytes stay unchanged. |

### 1.3 Violation signature and boundary

Missing/wrong identity; name-only substitution; login/sudo/control authority;
privileged or unaccounted GID; forbidden lab identity; effective process drift;
successful protected operation; reduced universe; or inability represented as
PASS violates this contract. The contract creates no identity or probe and
grants no lab/service authority. Current identity proof status is STOP because
`KVM2_PHASE2_ADMISSION_RECORD_V3` and all named values are `UNKNOWN`.

## 2. Filesystem contract

### 2.1 Required installed-state matrix

| Path | Numeric owner | Required type/mode/state | Service write |
|---|---|---|---|
| `/opt/mtc-bridge/releases/<exact-40-hex-sha>/` | `0:0` recursively | ordinary directories `0555`; executable regular files `0555`; non-executable regular files `0444`; exact independent file-and-directory inventory; no special or write-bit member | No |
| `/opt/mtc-bridge/venvs/<exact-40-hex-sha>/` | `0:0` recursively | same type/mode discipline and exact independent venv inventory | No |
| `/var/lib/mtc-bridge/` | `SERVICE_UID:SERVICE_GID` | directory `0750`; canonical DB and admitted SQLite sidecars only | Yes |
| `/var/log/mtc-bridge/` | `SERVICE_UID:SERVICE_GID` | directory `0750`; admitted logs; created logs `0640` | Yes |
| `/etc/mtc-bridge/` | `0:0` | ordinary directory `0750` | No |
| `/etc/mtc-bridge/mtc-bridge.env` | `0:0` | regular file `0600` | No |
| `/etc/mtc-bridge/install_manifest.json` | `0:0` | regular file `0640`; strict independently pinned JSON schema | No |
| `/usr/local/lib/systemd/system/mtc-bridge-first-start.service` | `0:0` | regular file `0644`; independent rendered hash | No |
| `/etc/systemd/system/mtc-bridge-first-start.service` | mask | sole allowed final symlink resolving exactly to `/dev/null` | No |
| `/etc/logrotate.d/mtc-bridge` | `0:0` | regular file `0644`; independent hash | No |

Every canonical component from `/` downward is an ordinary non-symlink
directory except the final mask. No unapproved mount, bind, overlay, magic link,
or namespace substitution may change the reached object. Effective service
write access is only state and logs. These retain the path/mode and sandbox
repairs the review required (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:70-98`).

### 2.2 Protected-material decision gate

FS-00 consumes only `KVM2_0444_PROTECTED_MATERIAL_DECISION_V1` defined in §0.4.
This contract makes no path-level choice. Env/configuration, state/SQLite, raw
logs, service-control surfaces, and host-specific manifests/evidence remain
protected. Every `0444` release member remains `UNKNOWN` until its owner/Lead row
exists. Lab admission and the aggregate filesystem verdict STOP while FS-00 does
not PASS; there is no fallback, default-readable classification, or broader
check that can pass around it.

### 2.3 Verification

| Case | Observation and independent expectation | PASS / FAIL / STOP | One-line falsification |
|---|---|---|---|
| FS-00 `0444` owner/Lead decision | Validate the decision signature/hash and exact candidate binding; compare its path/digest rows with the admission record's complete `0444` inventory and require one disposition per member. | PASS only for exact conservation. A contradictory disposition or wrong observed candidate FAILs. Missing/unapproved record, undecided/missing/extra/duplicate row, or unavailable inventory STOPs; aggregate filesystem PASS is impossible. | This check fails to PASS when one `0444` path is omitted, defaulted, or bound to another candidate; the result must STOP. |
| FS-01 path ancestry, mount policy, and within-run stability | A pinned fd-relative `openat2`/`fstatat` verifier walks from the attested host root with no symlink/magic-link traversal, compares types and mount/backing identity with the pre-install admission policy, and captures device/inode/mount IDs at open and close only to prove the same live objects were observed. Installer-created inode numbers are not expectations and no post-install baseline is accepted. | PASS requires canonical no-follow ancestry, allowed mount policy, correct types, and unchanged within-run IDs. Symlink, wrong type, or observable unapproved mount/overlay FAILs. Unsupported syscall, inaccessible component, unmappable mount, concurrent ID change, or unknown topology STOPs. | This check fails when a parent is replaced by a compliant decoy symlink or overlay; an installer-created path with no inode pin can still PASS on semantics, but an inode change during the run must STOP. |
| FS-02 numeric owner/mode and recursive universe | One fd-relative walk emits stable relative path, type, numeric owner, mode, size, and applicable digest for every file and directory; compare with the pre-install Git/artifact inventory and admission matrix using terminal conservation. | PASS requires exact tuples and no extra/missing/duplicate/special/writable node. Observable drift FAILs. Walk/read/race/canonicalization/count error STOPs. | This check fails when an empty directory, FIFO, writable node, or wrong numeric owner is added; an unreadable subtree must STOP. |
| FS-03 manifest/artifact binding | Parse the manifest with the admission record's pinned isolated parser, rejecting duplicate keys, non-JSON constants, unknown/missing keys, and wrong types; compare top-level identities and independently hash the exact tree. | PASS requires strict schema and exact independent identities/tree. Semantic or inventory mismatch FAILs. Parser/tool/read/source-pin error STOPs. | This check fails when accepted strings exist only in nested decoys, a duplicate key or `NaN` is added, or an empty directory is omitted. |
| FS-04 venv binding | Compare every distribution and filesystem member with the independently frozen lock/bootstrap exceptions, after validating the pinned interpreter's numeric metadata/hash. | PASS requires exact distribution and tuple conservation. Drift FAILs. Interpreter/import/metadata error, missing identity, duplicate canonical identity, or unclassified member STOPs. | This check fails when a readable distribution lacks identity metadata or two distributions collapse to one normalized name. |
| FS-05 effective service write boundary | In a separately authorized rehearsal, attest and enter MainPID's mount namespace, drop to the frozen numeric service tuple with cleared groups, and run create/write/rename/delete sentinels under every matrix parent; compare with the admission write matrix and effective systemd properties. | PASS requires allowed operations only under state/logs, frozen denials elsewhere, cleanup, and re-inventory. Forbidden success or policy-caused allowed failure FAILs. Namespace/probe/cleanup/path coverage uncertainty STOPs. | This check fails when a drop-in adds a third writable path, an allowed path is removed, or an ACL grants forbidden write access. |
| FS-06 protected-read denial | After FS-00 PASS, run the ID-06 syscall probe against every `PROTECTED_DENY_LAB_READ` path under the exact admitted lab tuple and frozen denial grammar. | PASS requires classified denial for every protected row. Any read success FAILs. FS-00 not PASS, missing lab identity, incomplete row set, or observation error STOPs. | This check fails when one protected path becomes readable through mode, ACL, group, mount, or sandbox drift. |
| FS-07 effective profile diff | Independently enumerate package, identity, unit, mount, listener, filesystem, and credential-name surfaces and compare with the selected-profile admission universe using stable IDs and terminal accounting. | PASS requires exact profile conservation and FS-00 PASS. Observable undeclared difference FAILs. Inaccessible source, dropped/overwritten member, open prerequisite, or count drift STOPs. | This check fails when an omitted empty directory or a second object collapsing to an existing key is introduced. |

### 2.4 Violation signature and boundary

Wrong/missing/extra path; numeric-owner/mode/type drift; unapproved symlink,
mount, overlay, mask, special or writable member; invalid/decoy manifest; venv
drift; write outside state/logs; protected read; profile difference; post-install
self-blessing; incomplete decision/walk represented as PASS; or aggregate PASS
around FS-00 violates this contract. No path, mount, ACL, unit, profile, or
owner/Lead decision is created here. Current filesystem proof status is STOP.

## 3. Network contract

### 3.1 Required end state

1. In the attested host and every admitted network namespace, the running bridge
   control plane has exactly one listener, `127.0.0.1:8790`, owned by the exact
   effective first-start process/artifact; before start it has none.
2. Operator access is only through a separately authorized SSH local forward of
   local 8790 to host `127.0.0.1:8790`. Port 8790 is never directly published,
   DNATed, proxied, or opened.
3. UFW is active/default-deny and the sole inbound allowance is SSH/22; effective
   lower-level and provider rules expose no 8790 path.
4. Installer and verifier policy remains read-only for firewall, SSH, NAT,
   proxy, container publication, and provider controls. NET-07 proves only
   equality at its two named snapshots, not absence of a transient mutation.
5. Loopback is not same-host process isolation; lab admission remains blocked on
   its separate OS-enforced isolation contract.

The runtime/proxy/provider mechanisms retain the v1 closure
(`PHASE2_CONTRACT_REVIEW_2026-08-15.md:100-124`). Current listener, firewall,
provider, proxy, observer, and reachability values are `UNKNOWN`.

### 3.2 Verification

Static source search is lint only and never substitutes for these observations.

| Case | Observation and independent expectation | PASS / FAIL / STOP | One-line falsification |
|---|---|---|---|
| NET-01 namespace universe | Reconcile namespace inodes from `/proc`, `lsns`, configured container runtimes, and the admission record; assign every source/member a representative and terminal disposition. | PASS requires complete source reconciliation and every admitted namespace observable. Undeclared observed namespace FAILs. Source/tool/access error or no observable representative STOPs. | This check fails when a container namespace is omitted by one source or one `/proc` link becomes inaccessible. |
| NET-02 complete socket census | In every NET-01 namespace run pinned `ss -H -ltnp` and independently join `/proc` socket inodes with `tcp`/`tcp6`; compare with the admission phase/listener set after rc/completeness adjudication. | PASS requires the exact phase set. Wrong listener FAILs. Query disagreement/failure, partial output, namespace exit, or owner ambiguity STOPs. | This check fails when `ss` returns nonzero/empty or an IPv6, wildcard, alternate, or second control listener exists. |
| NET-03 process/artifact binding | Bind effective MainPID/InvocationID, numeric identity, cgroup, exe, cwd, NUL argv, executable/module hashes, and socket inodes to admission-record service artifacts. | PASS requires the exact process/artifact owning the sole socket. Wrong owner/artifact or extra control socket FAILs. PID race, proc denial, unverifiable module, or absent pin STOPs. | This check fails when a decoy process owns `127.0.0.1:8790` while accepted source text remains. |
| NET-04 effective firewall | Capture and parse complete UFW, nftables, and any active legacy iptables state; reconcile with the independently frozen SSH-only host policy. | PASS requires active/default-deny and SSH-only inbound with no 8790 path. Any other allow/DNAT/forward FAILs. Backend/tool/parse/scope ambiguity STOPs. | This check fails when a direct nft/DNAT 8790 rule bypasses UFW; a failed UFW query must STOP. |
| NET-05 publication/proxy universe | Terminally account for every listener process, systemd socket, container map, NAT/forward rule, proxy, SSH forwarding policy, and provider firewall/LB/NAT object from admission-record collectors and read-only provider capture. | PASS requires no 8790 publication/proxy and exact conservation. Any publication FAILs. Missing provider scope/runtime, unknown owner, or unaccounted object STOPs. | This check fails when a container port, proxy, systemd socket, provider LB, or DNAT publishes 8790. |
| NET-06 external reachability/local forward | From independently named admission-record observers, require the frozen direct-unreachable class without a tunnel; under separate authority require an exact local forward to reach the same InvocationID/status endpoint. | PASS requires direct denial, authorized forward success, correct backend, and unchanged endpoint inventories. Direct/non-tunnel/wrong-backend access FAILs. Observer/tunnel/DNS/routing ambiguity STOPs. | This check fails when 8790 is published or the tunnel terminates at a decoy backend. |
| NET-07 snapshot endpoint equality—bounded claim | Independent collectors capture and authenticate complete semantic snapshots of UFW, nftables/iptables, SSH, container publication, proxy, and provider objects immediately before installer/verifier entry and immediately after its exit; compare them with each other and the admission schema. | PASS means only that the two captured endpoint states are equal. An observed endpoint delta FAILs. Missing/incomplete capture, collector error, unknown object, or unadjudicated authorized delta STOPs. No result asserts anything about changes between snapshots. | This check fails when a mutation remains in the post snapshot; add-then-remove between snapshots is explicitly outside this check's claim and cannot be cited as PASS evidence for read-only execution. |

### 3.3 Violation signature and boundary

Wrong listener set/owner/artifact; wildcard/IPv6/non-loopback/alternate socket;
non-SSH inbound allowance; any 8790 publication/proxy/NAT/provider path; direct
remote reachability; wrong tunnel backend; observed endpoint delta; incomplete
exposure universe; or observation error represented as PASS violates this
contract. Transient mutation between NET-07 endpoints is `UNKNOWN`, not PASS or
FAIL. No network/provider/tunnel/scan action is performed or authorized here.

## 4. Service contract

### 4.1 Required end state

1. `mtc-bridge-first-start.service` is the only installer-delivered unit; it has
   no Install section, is installed masked, is neither enabled nor started by
   the installer, and binds working directory/executable to one frozen release.
2. Effective ordering includes `Wants`/`After=network-online.target`; effective
   and process identities equal the frozen numeric service tuple; no root, sudo,
   ambient, or capability path exists.
3. Effective least privilege includes the independently frozen
   `NoNewPrivileges`, capability, private-device/tmp, filesystem/home,
   proc/kernel/cgroup, namespace, syscall, address-family, UMask, and writable-
   path properties. Resource ceilings remain `UNKNOWN` and STOP SVC-10.
4. Graceful stop sends SIGTERM first, uses `KillMode=mixed`, permits SIGKILL only
   after 45 seconds, and passes only on normal status 0 before timeout with no
   new invocation during the observed stop case.
5. First start is DISARMED/TESTNET-only, exactly once at its authorized gate;
   effective `Restart=no` and `NRestarts=0`. The no-reactivation claim is limited
   strictly to each SVC-05 interval from authenticated watcher-ready timestamp
   through at least 600 continuously observed seconds. V3 makes no automatic-
   activation claim before or after that interval.
6. The later steady restart-enabled profile remains absent/inert until its own
   gates; SVC-07 cannot authorize it.
7. Logs stay under `/var/log/mtc-bridge`; rotation is daily, retains 30, rotates
   at 64 MiB, delays compression once, uses copytruncate, recreates `0640` with
   the frozen numeric owner, and causes no new invocation during SVC-08.
8. Unit/logrotate hashes come only from the admission record. Resource-slice and
   wallet mechanism values remain `UNKNOWN`; no first start is permitted here.

These keep the effective-state/process/stop/log mechanisms the v1 review
required (`PHASE2_CONTRACT_REVIEW_2026-08-15.md:126-151`).

### 4.2 Normative `HL_LIVE_ACK` and egress boundary

Identifier-only policy, schema/name inventory, absence result, scanner result,
or enforcement configuration is allowed. The service contract prohibits:

1. the exact key in manager or final process environment, empty or nonempty;
2. any assignment/export/definition in an environment source;
3. any unit/vendor/drop-in/transient directive, credential route,
   `PassEnvironment`, or `ExecStart*`/other command form that defines, passes, or
   injects the key;
4. any value-bearing key representation in argv, stdout/stderr, journal, logs,
   diagnostics, crash/core output, screenshots, backups, exported evidence, or
   verifier captures; and
5. any evidence/verifier action that reads or emits the value.

Enforcement has four layers: structural parsing of every unit/environment/
wrapper/command source; effective `UnsetEnvironment=HL_LIVE_ACK`; exact-key
manager and NUL-delimited process-environment probes; and a scanner over the
complete `KVM2_PHASE2_SERVICE_EGRESS_UNIVERSE_V1` defined in §0.5. The scanner
parses argv and every record/object type structurally, never prints a value, and
assigns every universe member one disposition. Any missing category, source,
scope, collector, member, or parser makes SVC-09 STOP.

Mandatory isolated synthetic fixtures place a value-bearing key record in each
of: assignment; unit directive; drop-in; pass-through; manager environment;
process environment; argv; stdout/stderr; journal; current/rotated log;
diagnostic; crash/core; screenshot; backup catalog/object; exported evidence;
and verifier capture. Each must FAIL. An identifier-only comment, schema name,
absence result, and `UnsetEnvironment` defense must remain GREEN. An inaccessible
member in every category must STOP. No real secret value is used.

The exact external secret-contract relationship remains outside this four-
contract document; nothing here narrows this whole service boundary.

### 4.3 Verification

| Case | Observation and independent expectation | PASS / FAIL / STOP | One-line falsification |
|---|---|---|---|
| SVC-01 bytes and complete unit sources | Hash installed unit/logrotate bytes against admission pins; enumerate systemd search paths, fragment/source/drop-in paths, transient/generated units, aliases, and masks against the independently frozen source universe. | PASS requires exact external hashes and no unapproved source. Drift FAILs. Manager/search/query or missing pin STOPs. | This check fails when an external drop-in is added or installed bytes and installer-authored expected hash drift together. |
| SVC-02 parsed/effective properties | Run the pinned systemd loader/verifier and query all loaded properties, comparing with exact admission-record expectations including ordering, identity, command, restart, kill, environment, writable path, capability, sandbox, and decided resource fields. | PASS requires the exact effective set and no parser warning/error. Override/missing decided property FAILs. Manager/loader/query error or undecided resource property STOPs that property. | This check fails when accepted text is only a comment, a later duplicate sets `Restart=always`, or a drop-in changes user/write paths. |
| SVC-03 pre-start state | Query load/file/active/sub states, restart count, invocation ID, installed steady-unit paths, and FS-01 mask result against the admission pre-start state. | PASS requires loaded, masked, inactive, never invoked, `NRestarts=0`, not enabled, no effective Install admission, and no steady unit. Drift FAILs. Query/mask error STOPs. | This check fails when the fixture is unmasked/enabled or a steady unit/drop-in is installed. |
| SVC-04 process/artifact and single start | Under a future gate, bind MainPID/InvocationID/argv/cwd/exe/module/cgroup, activation count from the independent watcher, mode evidence, and NET-03 to admission expectations. | PASS requires one exact invocation, DISARMED/TESTNET evidence, and one loopback listener. Wrong artifact/mode/network or count over one FAILs. Event gap/race/incomplete evidence STOPs. | This check fails when a decoy artifact runs, mode is overridden, or two starts occur in the recorded event stream. |
| SVC-05 bounded `Restart=no` interval | In an authorized expendable rehearsal, authenticate the watcher-ready timestamp, abnormally terminate the exact invocation once, and continuously observe for at least 600 seconds. Compare effective `Restart=no`, activation count, InvocationID/MainPID, and `NRestarts=0` with admission expectations. | PASS means only no new activation from watcher-ready through the authenticated interval end. Any new invocation in that interval FAILs. Watcher gap, clock/manager reset, reboot, or incomplete interval STOPs. No result claims anything before/after. | This check fails when `Restart=on-failure` or an external trigger creates a new invocation inside the interval; a trigger at second 601 after a 600-second closed interval is outside the claim. |
| SVC-06 graceful stop | From an exact running invocation record stop request, SIGTERM delivery, exit, effective systemd result/status, invocation identity, PID, restart count, and continuous event trace against frozen 45-second semantics. | PASS requires SIGTERM first, normal status-0 exit before 45 seconds, no timeout/SIGKILL, and no new invocation during the case. Deviance FAILs. Missing timing/signal/event evidence STOPs. | This check fails when the fixture ignores SIGTERM past 45 seconds or receives a premature SIGKILL. |
| SVC-07 later-profile throttling | Only after separate admission, drive four classified crashes inside 600 seconds and observe the independently frozen delay/burst/interval plus DISARMED/reconcile/single-writer invariants. | PASS requires exact admitted throttle behavior and invariants. Extra/early activation or invariant loss FAILs. Unadmitted profile or incomplete event trace STOPs. | This check fails when a throttle key changes or an external trigger exceeds the frozen admitted count. |
| SVC-08 logrotate without restart | Bind pre/post PID, InvocationID, restart and activation counts, file descriptors, complete generation set, numeric metadata, compression delay, and independent policy hash. | PASS requires the frozen rotation result and same invocation. Drift/new invocation FAILs. Rotation/query/inventory error STOPs. | This check fails when postrotate restarts the service or create mode/retention differs. |
| SVC-09 `HL_LIVE_ACK`/egress boundary | Execute all four enforcement layers using §4.2 semantics and the independent egress-universe record; require terminal conservation and the complete synthetic matrix. | PASS requires zero forbidden forms, effective defense, complete accounting, RED for every prohibited surface, and GREEN only for identifier-only fixtures. A forbidden form FAILs. Missing/unreadable/incomplete surface, collector, or universe record STOPs the case and service aggregate. | This check fails when a synthetic value-bearing record exists only in argv, a screenshot, backup object/index, exported evidence, or any other §4.2 surface; an inaccessible member must STOP. |
| SVC-10 resources | Compare effective resource properties and measured behavior with exact values from a future owner-approved admission-record amendment produced independently of the unit renderer. | Currently STOP / `UNKNOWN`. Once frozen, observable mismatch FAILs and observation inability STOPs. | This check fails when one frozen ceiling is omitted or overridden; before any ceiling exists it must STOP, never PASS. |

### 4.4 Violation signature and boundary

Unapproved unit source/drop-in/alias; wrong independent hash; enabled/unmasked/
active/pre-invoked first-start; installed steady profile; wrong effective
identity/artifact; missing ordering; capability/sandbox/write-path weakening;
effective `Restart` drift; nonzero restart count; a new activation within a
claimed bounded interval; stop/rotation/throttle drift; any forbidden
`HL_LIVE_ACK` form on any §4.2 surface; invented resource value; reduced egress
universe; or observation failure represented as PASS violates this contract.

The contract makes no claim about SVC-05 time outside its recorded interval and
no claim about inaccessible/unfrozen egress scope. It installs, loads, starts,
stops, faults, rotates, provisions, or contacts nothing and grants no authority.

## 5. Present proof status

This V3 is a corrected design contract, not executed evidence. No admission
record, owner/Lead `0444` decision, service-egress universe, host observation,
RED/GREEN transcript, candidate pin, resource decision, or acceptance was
created. Their values and live state are `UNKNOWN`.

Therefore all four aggregate contracts currently STOP / remain UNVERIFIED. No
STOP can be reported as PASS, and nothing in this document authorizes admission,
deployment, first start, service action, secret handling, or economic action.
