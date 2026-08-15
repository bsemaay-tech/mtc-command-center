# KVM2 Phase-2 identity, filesystem, network, and service contracts — corrected draft A

## 0. Status, scope, source pins, and outcome grammar

Status: PREPARATION ONLY / NO AUTHORITY / NO ACCEPTANCE.

This document replaces the reviewed identity, filesystem, network, and service
drafts for the purpose of the Phase-2 repair lane. It does not replace or decide
the secret, state, recovery, teardown, maintenance, or incident contracts. The
review located the source documents outside the detached worktree and pinned the
exact reviewed blobs; those pins remain the source of this repair
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:11-24
@ 4e4d42fe).

The four contracts below retain the end states the review did not fault and
repair the review's findings: independently frozen expectations, complete
universes, numeric identities, path ancestry and mounts, effective systemd
state, runtime listener evidence, and STOP on observation failure
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:43-151,302-337
@ 4e4d42fe).

### 0.1 Binding outcome grammar

Every verification case has exactly one terminal outcome:

- PASS means every named observation completed successfully, its domain and
  completeness were established, and the observed value equals an expectation
  frozen independently before the checked producer ran.
- FAIL means the observation completed and positively found a contract
  violation. A required object that is observably absent is FAIL, not STOP.
- STOP means the property could not be evaluated: a tool, namespace, identity
  source, filesystem walk, parser, service manager, provider inventory, or
  evidence channel was unavailable, incomplete, timed out, or returned an
  unadjudicated status. STOP is never converted to PASS or FAIL.

Each probe record must contain: case ID; named machine/profile; exact candidate
SHA; host/namespace attestation; verifier identity; absolute tool paths and tool
hashes; start/end monotonic times; rc; complete stdout and stderr or a
content-free hash plus a separately retained capture; parsed result; expectation
record ID; terminal outcome; and reason token. The verifier adjudicates
rc/stderr/completeness before reading stdout. This ordering is required because
failed or partial observations have previously been read as compliant state
(MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:368-420).

The host claim is about the named KVM2 image in its attested initial user, mount,
PID, and network namespaces. Equality with a locally visible PID 1 is not enough.
If the deploy channel cannot supply an external namespace/host attestation, the
case STOPs (MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:111-176).

### 0.2 Independent expectation record

Before an installer, renderer, resetter, service, or verification harness runs,
an owner/Lead-approved admission record must freeze:

1. the exact base-image identity and package/policy inventory;
2. the selected profile and complete expected user/group universe;
3. SERVICE_UID and SERVICE_GID as numeric values;
4. every privileged/control-capable numeric GID, with the policy or object that
   makes it privileged;
5. the exact candidate Git identity, release manifest identity, release and
   venv entry inventory, expected unit hash, expected logrotate hash, and
   approved unit drop-in list;
6. the allowed mount topology and filesystem tuple inventory;
7. the host/container/proxy/provider exposure universe and the independent
   external observation points; and
8. the exact verifier/harness identity and expected evidence schema.

The admission record must be produced from the accepted image, profile policy,
Git objects, and provider control plane by a process independent of the
installer and service being checked. A hash written by the installer is
diagnostic only. The checked producer may not create, amend, or select its own
expected values. The recurring defect record explains why same-producer
artifact/expectation comparisons are not checks
(MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:30-63
@ a4833939).

SERVICE_UID, SERVICE_GID, the complete privileged-group ledger, the complete
per-profile identity inventory, the final candidate identity, the expected
rendered hashes, and the resource-slice decision are currently UNKNOWN. No value
is guessed below. Any case that needs one remains BLOCKED / UNVERIFIED until the
independent record supplies it.

### 0.3 Falsification rule

No verification case counts as evidence until its real verifier is shown:

- RED against the listed deviant fixture or an equivalent deliberate mutation;
  and
- GREEN against the conforming fixture,

with literal commands and real outputs retained. Reimplementing the predicate in
a test does not count. Each table states the concrete condition that must make
the check fail. This is the standing test for avoiding decorative checks
(MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-83
@ a4833939).

## 1. Identity contract

### 1.1 Required end state

1. A dedicated system account and primary group named mtc-bridge exist. Its home
   is /var/lib/mtc-bridge and its shell is a frozen non-login binary. It has no
   sudo/admin path, no privileged supplementary GID, and no service-control
   authority. A pre-existing identity with different attributes is a hard
   failure (MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:3-8).
2. Its numeric UID and primary GID equal independently frozen SERVICE_UID and
   SERVICE_GID. Resolver-rendered names are diagnostic only. The sources do not
   establish the numeric values, so both remain UNKNOWN until §0.2 is complete.
   Name-only ownership or membership cannot establish identity
   (MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:490-543).
3. The complete supplementary-GID set equals the profile's frozen allowed set
   and is disjoint from the frozen privileged/control-capable GID ledger. The
   current five-name list is not treated as complete; that exact defect was
   identified by review
   (MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:51-68
   @ 4e4d42fe).
4. In temporary-testnet-lab before any separately approved lab admission,
   mtc-bridge exists and every lab identity and lab-owned surface is absent. A
   cross-user probe is BLOCKED / UNVERIFIED, not PASS, while no probe identity
   exists. If a later admission is opened, its exact numeric identity must be in
   the independent profile record and must pass all denial probes below.
5. In future-trading-only, every lab user, group membership, home, agent,
   runner, browser-automation identity, workflow/scheduler identity, container
   identity, and lab credential owner is absent. Every remaining non-bridge
   identity has one terminal disposition in the profile inventory.
6. The effective first-start service identity is numeric
   SERVICE_UID:SERVICE_GID and the effective unit properties also report
   User=mtc-bridge and Group=mtc-bridge. Source text alone does not satisfy this
   requirement.

The profile-level identity intent is preserved from the reviewed draft
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:54-79
@ a4833939).

### 1.2 Verification

All commands below run only in a separately authorized expendable rehearsal.
They use pinned absolute tools in a cleared environment and capture rc/stdout/
stderr before interpretation.

| Case | Real observation and independent expectation | PASS / FAIL / STOP | Required RED fixture |
|---|---|---|---|
| ID-01 account tuple | Run getent passwd mtc-bridge once and parse the single complete passwd record; run id -u, id -g, and getent group mtc-bridge. Compare numeric UID/GID, home, and shell with §0.2. | PASS only for one consistent record with SERVICE_UID, SERVICE_GID, /var/lib/mtc-bridge, and the frozen non-login shell. Missing account or mismatched fields FAIL. Tool/NSS error, timeout, duplicate/inconsistent records, or incomplete output STOP. | Remap a wrong numeric UID/GID to the accepted names; the case must FAIL. Make NSS evaluation fail; it must STOP, never print “not a member.” |
| ID-02 complete group disposition | Capture id -G mtc-bridge and id -g mtc-bridge numerically. Assign every returned GID exactly one disposition: primary, approved supplementary, or prohibited. Compare against the independently frozen allowed and privileged GID sets; require input count = terminal dispositions with no duplicate or dropped GID. | PASS only when every numeric member is accounted for and no privileged GID is present. Any extra/prohibited GID FAILs. Enumeration error, an unfrozen ledger, or an unclassified GID STOPs. | Add a privileged GID omitted by the old five-name list; FAIL. Make id return nonzero with empty stdout; STOP. Add two names mapping to one GID; duplicate identity STOP. |
| ID-03 login and sudo denial | Confirm the frozen shell is a non-login executable, account authentication is locked by the selected image policy, then run a login-style runuser invocation whose harmless command is /usr/bin/true. As the exact service UID/GID with cleared groups, run sudo -n /usr/bin/true. | PASS only when both executable attempts return the preregistered denial classes and no command executes. An executed marker or sudo success FAILs. Missing tool, PAM/policy source not inventoried, or ambiguous nonzero status STOPs. | Replace the shell with /bin/sh or add a NOPASSWD sudo rule; the real probe must execute a marker and FAIL. |
| ID-04 service-control denial | Independently enumerate sudoers, polkit, D-Bus, and unit-specific authorization rules. From the probe identity, run pkcheck for org.freedesktop.systemd1.manage-units with interaction disabled, then attempt systemctl start on a loaded, inert canary unit whose only action is to create a rehearsal marker. The canary and authorization inventory are frozen before the probe. | PASS only on a classified authorization denial, no marker, and no unaccounted rule. Authorization success, marker creation, or a bridge-unit-specific grant FAILs. Missing canary, unknown rule source, inaccessible policy, or an error other than the frozen denial STOPs. | Add a matching polkit or sudoers allow rule. The marker must appear and the case must FAIL. |
| ID-05 profile identity universe | Enumerate passwd and group identities through every configured NSS backend and independently inventory local account/group databases and profile admission records. Give every observed and expected member one terminal disposition; mechanically diff the two universes. | PASS only for exact conservation and the profile rules in §1.1. An undeclared or forbidden identity FAILs. A backend that cannot enumerate, inaccessible source, or unexplained count change STOPs. | Add a lab account under an unlisted UID or omit a malformed-but-readable group record; the case must not PASS. |
| ID-06 cross-user path denials | Using a pinned openat2-based probe under the exact numeric lab/non-bridge UID/GID and cleared supplementary groups, attempt read, create, write, rename, and delete operations against the protected-path matrix in §2. The helper records actual errno, not diagnostic text. | PASS only for the exact expected denial errno on every protected operation and no mutation. Any successful forbidden operation FAILs. Missing probe identity, inaccessible namespace, unclassified errno, or incomplete path set STOPs. | Grant one ACL or supplementary group access; the real operation must succeed and make the case FAIL. |
| ID-07 effective service identity | After systemd has loaded the installed unit, capture FragmentPath, DropInPaths, User, Group, SupplementaryGroups, DynamicUser, and MainPID with systemctl show. When running under a later gate, compare /proc/MainPID/status numeric Uid/Gid/Groups with §0.2. | PASS only when effective and process identities equal the frozen tuple and no supplementary GID is present beyond the allowed set. Drift FAILs. Manager/proc access failure, MainPID race, or missing independent pins STOPs. | Add an external drop-in changing User or SupplementaryGroups; the case must FAIL although the vendor unit bytes are unchanged. |

ID-04 uses an inert rehearsal canary because a nonzero attempt against a missing
or masked bridge unit would prove only that the unit could not start, not that
the caller lacked authority. The authorization-source inventory and successful
marker mutant make the denial discriminating.

### 1.3 Violation signature

Any of the following is a violation: missing/wrong service user or primary
group; wrong numeric UID/GID; login-capable shell; unlocked login route;
successful sudo or service-control route; prohibited or unaccounted
supplementary GID; effective unit/process identity drift; forbidden lab identity
in either profile; successful protected read/write; undeclared identity; or any
STOP/incomplete result represented as PASS. The original P2-03 stop condition
remains that a lab identity can read or control protected bridge material
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:114-118).

### 1.4 Out of scope

This contract does not create or alter an identity, admit a lab user, execute a
login/sudo/control probe now, install or control a service, handle a credential,
or authorize a later gate. It does not decide numeric IDs or the profile
inventory; those are UNKNOWN until independently frozen. Host, SSH, deployment,
broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, push,
and economic action are excluded.

## 2. Filesystem contract

### 2.1 Required end state

The required installed-state matrix is:

| Path | Numeric owner | Required type/mode/state | Service write |
|---|---|---|---|
| /opt/mtc-bridge/releases/\<exact-40-hex-sha\>/ | 0:0 recursively | ordinary directories 0555; executable regular files 0555; non-executable regular files 0444; exact independently pinned file-and-directory inventory; no write bit | No |
| /opt/mtc-bridge/venvs/\<exact-40-hex-sha\>/ | 0:0 recursively | ordinary directories 0555; executable regular files 0555; non-executable regular files 0444; exact independently pinned venv inventory; no write bit | No |
| /var/lib/mtc-bridge/ | SERVICE_UID:SERVICE_GID | directory 0750; canonical DB /var/lib/mtc-bridge/bridge.db and its admitted SQLite sidecars only | Yes |
| /var/log/mtc-bridge/ | SERVICE_UID:SERVICE_GID | directory 0750; admitted current/rotated logs; created log files 0640 | Yes |
| /etc/mtc-bridge/ | 0:0 | ordinary directory 0750 | No |
| /etc/mtc-bridge/mtc-bridge.env | 0:0 | regular file 0600 | No |
| /etc/mtc-bridge/install_manifest.json | 0:0 | regular file 0640; strict JSON schema | No |
| /usr/local/lib/systemd/system/mtc-bridge-first-start.service | 0:0 | regular file 0644; independently pinned rendered bytes | No |
| /etc/systemd/system/mtc-bridge-first-start.service | mask | the sole allowed symlink; final link resolves exactly to /dev/null and the parent path is verified | No |
| /etc/logrotate.d/mtc-bridge | 0:0 | regular file 0644; independently pinned bytes | No |

This preserves the reviewed concrete path/mode matrix and the two writable
directories
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:159-192
@ a4833939). ProtectSystem=strict remains required, and the service gets write
access only to /var/lib/mtc-bridge and /var/log/mtc-bridge
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md:28-31).

Every canonical component from / downward is an ordinary non-symlink directory,
except the final intentional mask. No unapproved mount, bind mount, overlay,
magic link, or namespace substitution may alter the object reached by a
canonical path. Checking only the leaf is insufficient
(MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:180-239).

### 2.2 Protected-material seam

The sources do not establish whether world-readable immutable release code is
inside the phrase “bridge material.” The reviewed draft correctly marked that
conflict UNKNOWN, and the review requires an owner/Lead definition before lab
admission
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/IDENTITY_AND_FILESYSTEM_CONTRACTS_2026-08-15.md:225-242
@ a4833939;
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:304-311
@ 4e4d42fe).

Therefore this contract does not pretend the conflict is settled:

- env files, credential-bearing configuration, state/SQLite files, raw logs,
  service-control authority, host-specific manifests/evidence, and every path
  explicitly placed in a frozen protected-material manifest are protected;
- immutable release material at mode 0444 remains UNKNOWN with respect to lab
  readability; and
- later lab admission is BLOCKED until the owner/Lead freezes either (A) a
  path-level declaration that the 0444 subset is intentionally lab-readable
  non-protected material, or (B) a path-level protected set plus modes/sandbox
  that make the denial true.

No broad “lab cannot read bridge material” PASS may be issued while this choice
is open.

### 2.3 Verification

| Case | Real observation and independent expectation | PASS / FAIL / STOP | Required RED fixture |
|---|---|---|---|
| FS-01 path ancestry and mount identity | A pinned openat2/fstatat verifier walks every component from the attested host root with NO_SYMLINKS and NO_MAGICLINKS, records numeric dev/inode/mount IDs and object type, and compares them with the independently frozen mount/path record. The mask is handled as one explicit final-link exception. | PASS only when every component and allowed mount has one matching disposition. Any intermediate symlink, unexpected mount, overlay, wrong type, or wrong mask target FAILs. Unsupported openat2, inaccessible component, mount-table error, concurrent replacement, or unknown expected topology STOPs. | Insert a parent symlink to a compliant decoy and mount a compliant-looking overlay above a leaf; both must FAIL. |
| FS-02 numeric owner/mode and exact recursive universe | Perform one fd-relative recursive walk that emits every directory and file tuple: stable relative path, type, numeric UID:GID, mode, size, and file digest where applicable. Capture walk rc/stderr first. Compare with the independently frozen release/venv inventory and the path matrix; enforce input = accepted + rejected + unresolved. | PASS only for exact tuples with no extra, missing, duplicate, special, or writable node. A mismatch FAILs. Walk/read error, race, duplicate canonical path, or count drift STOPs. | Add an empty directory, FIFO, writable directory, wrong numeric owner rendered with an accepted name, and unreadable subtree; the first four FAIL and the unreadable walk STOPs. |
| FS-03 manifest and artifact binding | Parse install_manifest.json with a pinned isolated parser that rejects duplicate keys, non-JSON constants, unknown/missing keys, and wrong types. Compare exact top-level release and manifest identities with §0.2, then independently hash every admitted release file and directory inventory. | PASS only for the strict schema, independent expected identities, and exact tree. Semantic mismatch or extra/missing entry FAILs. Parser/tool/read error STOPs. | Put accepted strings in a nested decoy while top-level values are wrong, add a duplicate top-level key, add NaN, and add an extra empty directory; no case may PASS. |
| FS-04 venv binding | Compare the complete venv distribution and filesystem inventory against the independently frozen lock/bootstrap exception record, using the pinned interpreter only after its numeric owner/mode/hash are validated. | PASS only for exact distributions and tuples. Drift FAILs. Interpreter/import/metadata enumeration error or an unclassified distribution STOPs. | Add a readable distribution missing identity metadata and two distributions that canonicalize to one name; both must STOP or FAIL, never disappear. |
| FS-05 effective service write boundary | Under a separately authorized running rehearsal, obtain MainPID from systemd, attest its mount namespace, enter that exact mount namespace, drop to SERVICE_UID:SERVICE_GID with cleared groups, and use a pinned syscall probe. Create/write/rename/delete must succeed on dedicated sentinels under state and logs and must return classified denial errno at dedicated canary locations under every other matrix parent. Record cleanup and re-inventory. | PASS only when all allowed operations succeed, every forbidden operation is denied, no unexpected mutation remains, and effective ReadWritePaths equals the two paths. A forbidden success or allowed failure caused by actual policy FAILs. Namespace/probe/cleanup uncertainty or an untested path STOPs. | Add a third ReadWritePaths entry or external drop-in, remove one allowed path, and grant a write ACL. The effective probe must FAIL in each direction. |
| FS-06 protected-read denial | After §2.2 is frozen, run the ID-06 syscall probe against every protected manifest member under the exact admitted lab UID/GID. | PASS only for classified denials across the complete protected set. Any read success FAILs. Open §2.2, incomplete manifest, or observation failure STOPs. | Make one protected file 0444 or grant a read ACL; the case must FAIL. |
| FS-07 effective path/profile diff | Independently enumerate package, identity, unit, mount, listener, filesystem, and credential-name surfaces for the selected profile. Carry stable IDs through parse and comparison and give every member one terminal disposition. | PASS only for exact profile conservation and no undeclared difference. Deviant state FAILs. Inaccessible namespace/source or dropped/overwritten member STOPs. | Add an omitted empty directory or a second object that canonicalizes to an existing key; neither may silently pass. |

The existing verifier's final-component symlink checks, resolver-rendered owner
names, file-only release inventory, and substring manifest binding are
supplemental only; the review explains why they cannot establish these
properties
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:77-98
@ 4e4d42fe;
IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:45-52,123-134 @ 2ce41e34).

### 2.4 Violation signature

A missing or extra path; wrong type/mode/numeric owner; intermediate/final
unapproved symlink; unexpected mount/overlay; mask not resolving exactly to
/dev/null; writable release/venv node; injected/missing/hash-mismatched file or
directory; invalid/duplicate-key/decoy manifest; venv drift; effective writable
path outside state/logs; failed allowed state/log operation; protected read;
undeclared profile difference; or an incomplete/erroring walk represented as
PASS is a violation.

### 2.5 Out of scope

This contract does not create/change a path, mount, ACL, account, unit, or
profile; run the installer/verifier; enter a host namespace; start a service;
handle a credential; or decide the protected 0444 release subset. State
migration/reset, host/network/SSH action, deployment, cutover, broker/exchange,
ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, push, acceptance, and
economic action are excluded.

## 3. Network contract

### 3.1 Required end state

1. In the attested KVM2 host and every admitted network namespace, the bridge
   control plane has exactly one listening socket: 127.0.0.1:8790, owned by the
   effective first-start MainPID/cgroup. It has no IPv6, wildcard,
   interface-address, alternate-port, or second control listener.
2. Operator access is only through a separately owner-authorized SSH local
   forward of the shape local 8790 to host 127.0.0.1:8790. Port 8790 is never
   published, DNATed, reverse-proxied, or opened directly.
3. UFW is active, incoming default is deny, and the only inbound allow is port
   22 / OpenSSH. No UFW or lower-level effective rule permits or mentions an
   inbound 8790 path.
4. Installer and verifier are read-only with respect to UFW, nftables/iptables,
   SSH, NAT, proxy, container publication, and provider controls.
5. Loopback is not claimed as same-host process isolation. Lab admission remains
   blocked on its separate OS-enforced isolation contract.

These requirements are the established blueprint
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/NETWORK_AND_SERVICE.md:3-11)
and preserve the SSH-only UFW/no-publication end state the review found concrete
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:100-104
@ 4e4d42fe).

### 3.2 Verification

The static source check is only a lint. It never substitutes for the runtime
listener and reachability observations below; a dead-code/comment decoy can
satisfy the old grep
(IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:183-193 @ 2ce41e34;
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:105-124
@ 4e4d42fe).

| Case | Real observation and independent expectation | PASS / FAIL / STOP | Required RED fixture |
|---|---|---|---|
| NET-01 namespace universe | In the attested host domain, independently enumerate unique network namespace inodes from /proc, lsns, configured container runtimes, and the profile admission record. Select one readable representative PID per namespace and require one terminal disposition per discovered source/member. | PASS only when the independent sources reconcile and every admitted namespace is observable. An undeclared namespace FAILs. Permission/tool/read error or a namespace with no observable representative STOPs. | Add a container namespace omitted by one source and deny access to one /proc namespace link; no reduced-universe PASS is allowed. |
| NET-02 complete socket census | In every NET-01 namespace run a pinned ss -H -ltnp (and independently join /proc socket inodes to /proc/net/tcp and tcp6). Capture rc/stderr/completeness first. During the running phase require exactly one 127.0.0.1:8790 socket; before start require none. | PASS only for the phase's exact set. Any wildcard, IPv6, non-loopback, second, or wrong-phase listener FAILs. ss/proc disagreement, query failure, partial output, namespace exit, or inaccessible process ownership STOPs. | Force ss nonzero/empty, add ::1:8790, 0.0.0.0:8790, and an alternate bridge-owned control port; the first STOPs and the others FAIL. |
| NET-03 process/artifact binding | Obtain MainPID and InvocationID from effective systemd state, then record numeric uid/gid, cgroup, /proc/MainPID/exe, cwd, NUL-delimited argv, executable hash, referenced module path/hash, and socket-inode ownership. Compare with the independently pinned unit/release/venv identities. | PASS only when the sole socket belongs to the exact expected process and artifact. Wrong process/artifact or extra control socket FAILs. PID race, proc denial, unverifiable module, or absent independent hash STOPs. | Run a decoy process on 127.0.0.1:8790 while the accepted source string remains; FAIL. |
| NET-04 effective firewall | Capture ufw status verbose plus the complete effective nftables ruleset and any active legacy iptables backend with pinned tools. Parse their grammars, reconcile UFW intent with effective rules, and compare with the independently frozen SSH-only profile. | PASS only for active/default-deny and one SSH-only inbound allow with no 8790 path. Any other allow/DNAT/forward FAILs. Tool/backend ambiguity, query error, unparsable output, or incomplete table access STOPs. | Add a direct nft rule or DNAT for 8790 that UFW did not create; the combined case must FAIL. Make ufw query fail with empty stdout; STOP. |
| NET-05 publication/proxy universe | Terminally account for every listening process, systemd socket, container port mapping, NAT/forward rule, reverse-proxy/listener service, SSH forwarding policy, and provider firewall/LB/NAT object discovered by the independently frozen host/provider inventories. Compare provider state through a separately authenticated read-only control-plane capture. | PASS only when no object publishes/proxies 8790 and every inventoried object has one disposition. Any publication/proxy FAILs. Missing provider scope, inaccessible runtime, unknown listener owner, or an unaccounted object STOPs. | Add a container published port, socat/nginx proxy, systemd socket, provider LB, or DNAT; each must FAIL even if the bridge still binds loopback. |
| NET-06 external reachability and SSH local forward | From independently named external observation points, with the tunnel absent, a direct TCP connection to host:8790 must return the frozen unreachable class. Under a separately authorized local-forward tunnel, the operator-side local endpoint must reach the same InvocationID/status endpoint. Capture tunnel command shape without private identifiers. | PASS only when direct access fails, the authorized local forward succeeds, and socket/provider inventories remain unchanged. Direct success, non-tunnel access, or wrong backend identity FAILs. Observer/tunnel/DNS/routing ambiguity STOPs. | Publish 8790 or enable a proxy; direct access must turn RED. Point the tunnel at a decoy backend; identity binding must FAIL. |
| NET-07 read-only enforcement | Compare pre/post hashes and semantic snapshots of UFW, nftables/iptables, SSH, container publication, proxy, and provider objects around installer/verifier execution. Expectations are frozen before execution by a collector independent of those programs. | PASS only for no semantic delta. Any mutation FAILs. Incomplete pre/post capture or author-approved unexplained delta STOPs. | Make a fixture installer add then remove a transient firewall rule; event/semantic capture must detect it and FAIL. |

The local and provider exposure inventories are both required. A local negative
scan cannot prove a provider publication path is absent, and a declared proxy
name list cannot prove completeness. Current live listener, firewall, tunnel,
proxy, provider, and reachability state remains UNKNOWN.

### 3.3 Violation signature

Any listener set other than the phase-specific exact set; listener owned by the
wrong process/artifact; IPv6/wildcard/non-loopback/alternate control socket; UFW
inactive or not default-deny; any inbound allow other than SSH/22; any 8790
firewall/NAT/container/proxy/provider publication; direct remote reachability;
operator access outside the authorized local forward; installer/verifier
network mutation; incomplete exposure universe; or observation error represented
as PASS violates the contract.

### 3.4 Out of scope

No UFW/SSH/network/DNS/certificate/NAT/proxy/container/provider setting is
changed; no tunnel, scan, public probe, installation, listener, or service is
started here. Per-destination egress and same-host lab isolation remain separate.
No host, deployment, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, push, acceptance, authorization, or
economic action is performed.

## 4. Service contract

### 4.1 Required end state

1. mtc-bridge-first-start.service is the only installer-delivered unit. It has
   no Install section, is installed masked, is not enabled or started by the
   installer, and binds WorkingDirectory and ExecStart to one exact immutable
   release/venv SHA
   (MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/NETWORK_AND_SERVICE.md:13-23).
2. It Wants and orders After network-online.target; runs as
   mtc-bridge:mtc-bridge / SERVICE_UID:SERVICE_GID; and has no root, sudo, or
   capability path.
3. Effective least privilege includes NoNewPrivileges=yes; empty capability and
   ambient-capability sets; PrivateTmp=yes; PrivateDevices=yes;
   ProtectSystem=strict; ProtectHome=yes; the frozen proc/kernel/control-group,
   namespace, syscall, address-family, and UMask restrictions; and effective
   write access only to state/log paths. The source template carries this intent
   (IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:63-93
   @ 2ce41e34).
4. Graceful stop sends SIGTERM first, uses KillMode=mixed, gives the process 45
   seconds, and allows SIGKILL only after that timeout. A passing rehearsal exits
   normally with status 0 before 45 seconds, records no SIGKILL/timeout result,
   and does not restart.
5. The first start is DISARMED and TESTNET-only, exactly once. Effective
   MTC_BRIDGE_START_MODE is credential_free_disarmed, Restart is exactly no,
   NRestarts remains zero, and there is no automatic retry/restart loop. The
   start-limit keys remain configured as protection but do not create a restart
   under Restart=no
   (IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:21-27,36-56
   @ 2ce41e34).
6. The steady restart-enabled template remains absent/inert and inadmissible
   until its separate crash/kill/reboot, reconciliation, continuity, duplicate,
   throttle, audit, and acceptance gates. It is not part of first start.
7. Logs remain under /var/log/mtc-bridge. Rotation is daily, retains 30
   generations, rotates at 64 MiB, delays compression one generation, uses
   copytruncate, recreates 0640 SERVICE_UID:SERVICE_GID files, and never causes a
   service restart
   (MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/NETWORK_AND_SERVICE.md:29-34).
8. The rendered unit and logrotate hashes come from the independent admission
   record, not from install output. Both are currently UNKNOWN until the final
   candidate is frozen.
9. Resource-slice values remain UNKNOWN / BLOCKED. No source establishes Slice,
   CPUQuota, MemoryMax, TasksMax, or equivalent values. No resource PASS is
   possible until an owner-accepted measured decision supplies exact effective
   properties. This preserves the reviewed open item
   (MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/NETWORK_AND_SERVICE_CONTRACTS_2026-08-15.md:61-63
   @ a4833939).
10. No first start is currently permitted. The separately deferred wallet item
    remains a blocker; this contract neither requests nor handles any value.

### 4.2 Normative HL_LIVE_ACK boundary — service/secret agreement point

The prohibition is semantic, not a ban on writing the identifier in policy.
The old phrase “present in any form” is invalid because the accepted unit
template contains an identifier-only policy comment, and the review identifies
that direct contradiction
(IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:43-45
@ 2ce41e34;
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:161-181
@ 4e4d42fe).

The service contract prohibits all of the following:

1. an HL_LIVE_ACK key in the systemd manager environment or final service
   process environment, regardless of whether its value is empty;
2. a shell/env assignment or export definition of that key in
   /etc/mtc-bridge/mtc-bridge.env, any additional EnvironmentFile, launch
   wrapper, profile, or generated environment source;
3. a unit/vendor/drop-in/transient directive that defines the key, passes it
   from the manager, supplies it as a credential, or injects it into ExecStart,
   ExecStartPre, ExecStartPost, or another service command;
4. a value-bearing key/value representation in argv, service stdout/stderr,
   journal, diagnostics, crash/core output, screenshots, backup, or exported
   evidence; and
5. an evidence or verification process that reads or emits the value.

Identifier-only mentions are allowed only as non-value-bearing policy,
schema/name inventory, scanner result, or enforcement configuration. Thus the
template comment at lines 43-45, a result such as
name HL_LIVE_ACK / outcome absent, and an effective
UnsetEnvironment=HL_LIVE_ACK defense do not violate the rule. A definition such
as the key followed by an equals sign, a JSON/map key with a value, a
PassEnvironment reference, or a process-environment key does violate it.

The prohibition is enforced at four independent layers:

- Admission parser: structurally parse the vendor unit, all drop-ins/transient
  properties, every EnvironmentFile, and every launch wrapper; reject every
  definition/injection/pass-through form above. Comments are not directives.
- Effective systemd defense: the final loaded service must have
  UnsetEnvironment=HL_LIVE_ACK as an effective property, so manager inheritance
  cannot create the key. Any drop-in that resets or defeats this property fails.
- Runtime probe: before start, check the manager environment by exact key; after
  a separately authorized start, parse /proc/MainPID/environ as NUL-delimited
  key/value records and require zero exact-key records. Read/query failure STOPs.
- Egress scanner: independently enumerate the generated log/journal/diagnostic/
  crash/evidence surface manifest and scan parsed records for a value-bearing
  key. Every surface gets one terminal disposition. Inaccessible or incomplete
  scope STOPs; no value is printed.

Mandatory falsifications inject only synthetic non-secret values into isolated
fixtures: env assignment, Environment directive, external drop-in,
PassEnvironment, manager environment, NUL-delimited process environment,
argv, journal/log record, JSON evidence field, and an inaccessible evidence
surface. The real check must FAIL the first nine and STOP the inaccessible
surface. An identifier-only comment, schema name, absence result, and
UnsetEnvironment directive must remain GREEN.

The secret contract must reproduce or normatively cross-reference this exact
surface list and semantic distinction. Agreement is checkable: any secret
contract wording that prohibits identifier-only policy/enforcement mentions,
permits a definition/pass-through/process key, omits a listed egress surface, or
uses “present in any form” without this qualification disagrees with the service
contract and blocks both. The reviewed secret wording at lines 87-89 and 128 is
therefore not conforming until lane PH2B repairs it
(MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/SECRET_AND_STATE_CONTRACTS_2026-08-15.md:87-89,117-133
@ a4833939).

### 4.3 Verification

| Case | Real observation and independent expectation | PASS / FAIL / STOP | Required RED fixture |
|---|---|---|---|
| SVC-01 independent bytes and complete unit sources | Hash the installed vendor unit/logrotate bytes and compare with §0.2. Enumerate systemd search paths, FragmentPath, SourcePath, DropInPaths, transient/generated units, aliases, and masks. The approved drop-in list is independently frozen and initially empty. | PASS only for exact external hashes, the expected fragment/mask, and no unapproved source. Byte/source/drop-in drift FAILs. Manager/search-path/query error or missing expected hash STOPs. | Add an external drop-in while leaving vendor/template bytes identical; FAIL. Change both installed unit and installer-produced expected hash; external pin must still FAIL. |
| SVC-02 parsed/effective properties | Run systemd-analyze verify and query the loaded unit with systemctl show after daemon-reload. Compare effective After, Wants, User, Group, ExecStart, WorkingDirectory, Restart, start-limit, kill/timeout, environment, UnsetEnvironment, output paths, writable paths, capability sets, and every frozen sandbox/resource property. Use systemd's loader semantics; comments/duplicate directives are not accepted as evidence. | PASS only for the exact effective property set and no parser warning/error. Any effective override/missing property FAILs. Manager/loader/query error or undecided resource property STOPs that property; resource contract remains BLOCKED. | Put accepted text in comments, add a later duplicate Restart=always, and add a drop-in changing User/ReadWritePaths; all must FAIL. |
| SVC-03 pre-start state | Query LoadState, UnitFileState, ActiveState, SubState, NRestarts, InvocationID, and all installed steady-unit paths. Verify exact /dev/null mask with FS-01. | PASS only when first-start is loaded, masked, inactive, never invoked, NRestarts=0, not enabled, no Install section effectively admits enablement, and steady unit is absent. Deviant state FAILs. Query/mask observation error STOPs. | Unmask/enable the fixture or install a steady drop-in/unit; FAIL. |
| SVC-04 runtime process/artifact and single start | Under the future one-start gate, bind MainPID/InvocationID/argv/cwd/exe/module/cgroup to §0.2 and NET-03. Record activation count from an independent event watcher plus systemd properties. | PASS only for one invocation, exact artifact, DISARMED/TESTNET evidence, one loopback listener, and no second activation. Wrong artifact/mode/network or activation count over one FAILs. Event-gap/PID race/incomplete mode evidence STOPs. | Execute a decoy artifact, override the mode, or trigger two starts; FAIL. |
| SVC-05 Restart=no and no loop | In an authorized expendable rehearsal, terminate the first-start process abnormally once. Observe for at least 600 seconds, exceeding the configured 300-second start-limit interval and restart delay. Require unchanged activation count, no new InvocationID/MainPID, NRestarts=0, and effective Restart=no. | PASS only when it remains inactive/failed without retry. Any automatic activation/restart FAILs. Watcher gap, manager reset, reboot, or incomplete interval STOPs. | Add Restart=on-failure or an external restart trigger; the new invocation must make the case FAIL. |
| SVC-06 graceful stop | From a running exact invocation, record monotonic stop request, SIGTERM delivery evidence, process exit, systemd Result/ExecMainCode/ExecMainStatus, InvocationID, MainPID, and NRestarts. | PASS only for SIGTERM first, normal status-0 exit before 45 seconds, no timeout/SIGKILL, and no new invocation/restart. Premature SIGKILL, timeout, nonzero abnormal exit, or restart FAILs. Missing signal/timing evidence STOPs. | Make the fixture ignore SIGTERM past 45 seconds and separately add a premature SIGKILL; both must FAIL. |
| SVC-07 restart throttling for later steady profile | Only after separate admission, drive four classified crash attempts inside 600 seconds and observe exact RestartSec=30 delay, maximum three admitted starts, then start-limit refusal, while preserving DISARMED/reconcile/single-writer invariants. | PASS only for the frozen interval/burst/delay and all safety invariants. Excess/early restart or invariant loss FAILs. Unadmitted profile or incomplete event trace STOPs. | Remove/change one throttle key or add an external restart trigger; FAIL. This case cannot authorize steady admission. |
| SVC-08 logrotate without restart | Before and after forced rotation, bind MainPID, InvocationID, NRestarts, activation count, open file descriptors, file numeric owner/mode, generation set, compression delay, and policy hash. | PASS only for the frozen rotation/retention result, same process/invocation, and no restart. Wrong files/modes/retention or any new invocation FAILs. Rotation/query/inventory error STOPs. | Add a postrotate restart, wrong create mode, or wrong retention; each must FAIL. |
| SVC-09 HL_LIVE_ACK boundary | Run all four enforcement layers and the complete synthetic mutation matrix in §4.2. Expected semantics come from §4.2, not from the installed unit or scanner output. | PASS only for zero forbidden forms, effective UnsetEnvironment defense, complete egress accounting, RED on every forbidden synthetic fixture, and GREEN on identifier-only fixtures. Forbidden form FAILs; inaccessible/incomplete surface STOPs. | The §4.2 mutation list is mandatory and discriminates assignment/value from policy-name mention. |
| SVC-10 resources | Compare effective resource properties and measured behavior with a future owner-accepted resource record independent of the unit renderer. | Currently BLOCKED / UNVERIFIED. Once frozen, mismatch FAILs and observation error STOPs. | Omit or override one frozen ceiling; the real effective-property and load probe must FAIL. |

The old directive grep and same-release template comparison remain useful
diagnostics but cannot establish effective state. The review specifically notes
that comments, duplicate directives, and external drop-ins can make them pass
while the service is deviant
(IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:155-201 @ 2ce41e34;
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PHASE2_CONTRACTS/PHASE2_CONTRACT_REVIEW_2026-08-15.md:133-151
@ 4e4d42fe).

### 4.4 Violation signature

Any unapproved unit source/drop-in/alias; wrong independent hash; enabled,
unmasked, active, previously invoked, or restart-enabled first-start state
before its gate; installed steady profile; wrong effective user/group/artifact;
missing network-online ordering; non-empty capabilities; weakened sandbox;
write path outside state/logs; effective Restart other than no; NRestarts other
than zero; more than one first-start activation; automatic retry; start not
proven DISARMED and TESTNET-only; premature SIGKILL or stop over 45 seconds;
restart-throttle drift; logrotate drift/restart; any forbidden HL_LIVE_ACK form;
invented/unapproved resource value; or any observation failure represented as
PASS violates this contract.

### 4.5 Out of scope

This document does not install, render on a host, daemon-reload, enable, unmask,
start, stop, kill, restart, fault-inject, rotate logs, provision credentials,
or contact any host/network/service/provider. It does not select a final
candidate, resource ceiling, wallet, steady profile, or later gate. It changes
no product code, unit, script, Pine, parity, MTC/trading behavior, broker/
exchange surface, ARM/order path, TESTNET/mainnet state, branch, or remote. It
issues no acceptance or authorization.

## 5. Present proof status

These are corrected design contracts, not executed evidence. No RED/GREEN
transcript, independent pin record, host observation, or owner decision was
created by this lane. Consequently:

- all current live identity, filesystem, network, and service state is UNKNOWN;
- SERVICE_UID/SERVICE_GID, complete identity/group/exposure universes, candidate
  hashes, protected 0444 release subset, and resource slices remain UNKNOWN;
- every affected case remains BLOCKED / UNVERIFIED until its prerequisite and
  separately authorized rehearsal exist; and
- nothing in this document is acceptance, deployment authority, first-start
  authority, secret authority, or economic authority.
