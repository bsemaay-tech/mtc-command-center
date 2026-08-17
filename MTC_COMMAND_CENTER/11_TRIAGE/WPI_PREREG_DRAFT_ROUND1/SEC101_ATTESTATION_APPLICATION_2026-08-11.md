# §10.1 and attestation-ordering application text

Date: 2026-08-11  
Status: standalone merge input; no authority, identifier, attestation value, host contact,
freeze, or Git action is created by this document  
Audit tier: T2 (documentation/application text)

This document supplies two pieces of text for the successor preregistration:

1. a complete replacement for §10.1, including the eleven `EXTEND` dispositions from
   `SEC101_RECONCILIATION_CODEX_2026-08-10.md` and an access-qualified rule grammar; and
2. an exact two-commit procedure that preregisters the root-side attestation capture before
   the capture occurs, then freezes the captured values before any WP-I operation consumes
   them.

The three source families that cannot be closed by §10.1 alone are decided proposals, not
silent assumptions. Each is marked `PROPOSED — LEAD/OWNER DECISION REQUIRED`. Until all
three are accepted and implemented in the frozen composite, Stage 1 STOPs and no archive or
successor preregistration is dispatchable.

## Disposition conservation table

The admitted application universe is exactly 15 members: 11 `EXTEND` items, 3 unresolved
families, and 1 ordering fix. Every member below has exactly one terminal disposition and
one explicit anchor; none is absorbed into another row.

| ID | Source member | Terminal disposition | Application anchor |
|---|---|---|---|
| EXT-01 | `/` | INCLUDE as `read-exact` | [§10.1-E01](#sec101-e01) |
| EXT-02 | `/opt`, `/opt/mtc-bridge`, `/opt/mtc-bridge/releases`, `/opt/mtc-bridge/venvs` | INCLUDE as finite `read-exact` set | [§10.1-E02](#sec101-e02) |
| EXT-05 | `/usr`, `/usr/bin` | INCLUDE as finite `read-exact` set | [§10.1-E05](#sec101-e05) |
| EXT-06 | frozen RP6/RP7 executable objects | INCLUDE as finite `read-execute-exact` set, conditional on FAM-01 closure | [§10.1-E06](#sec101-e06) |
| EXT-08 | `/etc` | INCLUDE as `read-exact` | [§10.1-E08](#sec101-e08) |
| EXT-10 | `/var`, `/var/lib`, `/var/log` | INCLUDE as finite `read-exact` set | [§10.1-E10](#sec101-e10) |
| EXT-13 | `/proc/uptime` | INCLUDE as `read-exact` | [§10.1-E13](#sec101-e13) |
| EXT-14 | `/proc/self/mountinfo` | INCLUDE as `read-exact` | [§10.1-E14](#sec101-e14) |
| EXT-15 | `/proc/self/ns/{user,mnt,pid,net}` | INCLUDE as finite `read-exact` set | [§10.1-E15](#sec101-e15) |
| EXT-16 | exact `/proc/<WPI_MAINPID>/ns/net` | INCLUDE as `read-exact`; freeze to the preregistered PID | [§10.1-E16](#sec101-e16) |
| EXT-17 | `/proc/self/fd/8` | INCLUDE as `read-exact` | [§10.1-E17](#sec101-e17) |
| FAM-01 | RP6 inherited-PATH/optional-pin executable family | `PROPOSED — LEAD/OWNER DECISION REQUIRED`: close to twelve exact pins and delete fallback | [Decision F1](#decision-f1) |
| FAM-02 | RP6 arbitrary-prefix venv-root family | `PROPOSED — LEAD/OWNER DECISION REQUIRED`: bind the one exact per-candidate venv root | [Decision F2](#decision-f2) |
| FAM-03 | evidence-root provenance | `PROPOSED — LEAD/OWNER DECISION REQUIRED`: require a complete frozen-composite derivation | [Decision F3](#decision-f3) |
| ORDER-01 | circular attestation/preregistration/commit order | INCLUDE the two-commit capture-then-consume procedure | [Ordering fix](#ordering-fix) |

Conservation equation: `15 admitted = 11 INCLUDE extensions + 3 explicit proposed
decisions + 1 INCLUDE ordering fix`; terminal dispositions = 15; omitted/overwritten
members = 0.

## Replacement text for §10.1

### 10.1 Unprivileged path and endpoint allowlist

The P0 and RO stages may use only the rules in this section. The list is exhaustive for
source-controlled filesystem operands, network endpoints, and closed runtime-derived
families in the complete frozen stage composites defined by §10.2. A path match without a
matching access qualifier is not admission. Anything unmatched, dynamically unresolved,
or reached with a stronger access class is a Stage-1 STOP and prevents archive freeze.

This section does not claim to enumerate undocumented internal opens performed by Bash,
the dynamic loader, libc, Python, or other pinned external binaries. Those are the named
external-runtime boundary in §10.2. Runtime-selected descendants are admissible only when
the complete composite proof establishes that they remain inside a listed closed tree.

#### Access-qualifier grammar

Each rule has exactly one qualifier:

| Qualifier | Meaning |
|---|---|
| `read-exact` | The exact object may be examined by non-following metadata, read, or `readlink` operations as applicable. It grants no descendant access, execution, creation, or write. |
| `read-tree` | The named root and runtime-selected descendants lexically confined below it may be traversed, enumerated, metadata-read, and content-read. It grants no filesystem-object execution, creation, or write. |
| `read-terminal` | Only the terminal directory object may be metadata-read. The path may not be used as a prefix, and no child may be opened or enumerated. |
| `read-execute-exact` | The exact, separately bound filesystem object may be metadata-read, content-read, and invoked. It grants no descendant access or write. |
| `write-tree` | The run-owned root and descendants may be created, metadata-read, content-read, written, or appended under the create-once evidence/kit contract. It is the sole filesystem write authority. It does not authorize a filesystem-object invocation that is not otherwise exact-bound. |
| `connect` | A connection may be attempted only to the exact address and port. It grants no listener, alternate address, alternate port, or other network authority. |

For an operation to be admitted, at least one matching rule must carry the required access
class. A broader read rule never supplies execution or write authority. The
`read-execute-exact` rule for the venv interpreter is therefore a deliberate exact
exception inside the otherwise `read-tree` venv family. Brace notation below denotes a
finite enumerated set, not a wildcard. Every `<...>` freeze token must be replaced by one
exact value before Stage 1; an unfilled token is STOP.

#### Exhaustive rules

| Access | Exact path or closed family | Recorded premise and bounded purpose |
|---|---|---|
| `read-exact` | `/` | Canonical-root identity and ancestor-kind binding only; retained output is numeric metadata plus device/inode identity. |
| `read-exact` | `/opt`, `/opt/mtc-bridge`, `/opt/mtc-bridge/releases`, `/opt/mtc-bridge/venvs` | Fixed root-owned ancestors are `lstat`ed only to bind the two preregistered candidate trees through non-symlink directory components; directory contents are not enumerated by these rules. |
| `read-tree` | `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/**` | Candidate release root is numeric `0555 0:0`; traversal/readability and absence of DAC write bits remain separate runtime predicates. The verifier source is read as input to the trusted interpreter, not invoked as a filesystem executable. |
| `read-tree` | `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/**` | Candidate venv root is numeric `0555 0:0`; traversal/readability and absence of DAC write bits remain separate runtime predicates. |
| `read-execute-exact` | `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python` | The service interpreter may be invoked only after exact path-, object-, mount-, and bounded-exec checks. It does not adjudicate its own venv. |
| `read-exact` | `/usr`, `/usr/bin` | Fixed root-owned ancestors of the preregistered executable objects are metadata-read only; their contents are not enumerated. |
| `read-execute-exact` | `/usr/bin/stat`, `/usr/bin/readlink`, `/usr/bin/env`, `/usr/bin/find`, `/usr/bin/sha256sum`, `/usr/bin/systemctl`, `/usr/bin/ss`, `/usr/bin/curl`, `/usr/bin/timeout`, `/usr/bin/id`, `/usr/bin/getent`, and exact `<WPI_FIXED_TRUSTED_PYTHON>` | This is the complete proposed RP6/RP7 executable set after Decision F1. Every member is a root-owned, non-group/world-writable, exact-bound executable object. The trusted-Python token is replaced by its resolved non-symlink exact leaf at freeze. No PATH fallback or additional executable is admitted. |
| `read-exact` | `/usr/local/lib/systemd/system/mtc-bridge-first-start.service` | World-readable regular unit fragment, recorded mode `0644`, 3736 bytes. |
| `read-exact` | `/etc` | Fixed root-owned ancestor is `lstat`ed only to bind terminal `/etc/mtc-bridge`; `/etc` content is not read. |
| `read-terminal` | `/etc/mtc-bridge` | Numeric `0750 0:0`; terminal metadata only. No `/etc/mtc-bridge/` descendant access is admitted. |
| `read-exact` | `/var`, `/var/lib`, `/var/log` | Fixed root-owned ancestors are `lstat`ed only to bind the terminal state and log directories; contents are not read by these rules. |
| `read-terminal` | `/var/lib/mtc-bridge` | Numeric `0750 999:988`; terminal metadata only; rendered account name is diagnostic only. |
| `read-terminal` | `/var/log/mtc-bridge` | Numeric `0750 999:988`; terminal metadata only; rendered account name is diagnostic only. |
| `read-exact` | `/proc/uptime` | Read only for monotonic timestamps bounding probes; the host uptime value is not emitted. |
| `read-exact` | `/proc/self/mountinfo` | Read only to derive the preregistered mount-topology projection; the raw snapshot remains inside the run evidence tree and is not printed. |
| `read-exact` | `/proc/self/ns/user`, `/proc/self/ns/mnt`, `/proc/self/ns/pid`, `/proc/self/ns/net` | Namespace links are read only for deploy-attested namespace identity and namespace-object device checks; no descriptor or namespace authority is acquired. |
| `read-exact` | exact `/proc/<WPI_MAINPID>/ns/net` (frozen for this run only after `<WPI_MAINPID>` is replaced by the preregistered decimal PID; the current draft value is `/proc/189813/ns/net`) | Read only to compare the service network-namespace identifier with the caller's. A placeholder, changed PID, or any other `/proc/<pid>` path is not admitted. |
| `read-exact` | `/proc/self/fd/8` | Read only to prove the already-open stdout descriptor is the run's create-once evidence leaf; it opens no new target. |
| `write-tree` | exact `<REMOTE_BASE>/**` after dispatch allocation and frozen-composite provenance proof | Sole read/write/create family: the run's own numeric-euid:egid `0700` create-once kit and evidence tree. Decision F3 must prove every derived `EV_DIR`, `EV_LOG`, archive, extracted member, capture, projection, status body, and diagnostic leaf remains below this exact root. |
| `connect` | `127.0.0.1:8790` | Sole unprivileged network destination; one exact loopback endpoint for the status GET. |

`/dev/null` is intentionally absent. No block, wrapper, bootstrap, or nested source may
open it for reading or writing. Incidental suppression must use a closed descriptor or a
create-once leaf already covered by `write-tree`. No other filesystem rule carries write
authority, and no other endpoint carries `connect` authority.

<a id="sec101-e01"></a>
#### §10.1-E01 — canonical root

Applied by the `/` `read-exact` row; the rule retains only canonical-root metadata and
device/inode identity.

<a id="sec101-e02"></a>
#### §10.1-E02 — `/opt` ancestors

Applied by the finite `/opt` ancestor `read-exact` row; no content enumeration or wildcard
ancestor family is admitted.

<a id="sec101-e05"></a>
#### §10.1-E05 — `/usr` ancestors

Applied by the finite `/usr`, `/usr/bin` `read-exact` row; executable authority remains in
the separate exact tool rule.

<a id="sec101-e06"></a>
#### §10.1-E06 — exact executable objects

Applied by the finite `read-execute-exact` tool row. Its RP6 half is effective only after
Decision F1 is accepted and the complete frozen pin set is mechanically conserved.

<a id="sec101-e08"></a>
#### §10.1-E08 — `/etc` ancestor

Applied by the `/etc` `read-exact` row; `/etc/mtc-bridge` remains a separate terminal-only
rule.

<a id="sec101-e10"></a>
#### §10.1-E10 — `/var` ancestors

Applied by the finite `/var`, `/var/lib`, `/var/log` `read-exact` row; the state and log
directories remain separate terminal-only rules.

<a id="sec101-e13"></a>
#### §10.1-E13 — monotonic clock source

Applied by the `/proc/uptime` `read-exact` row.

<a id="sec101-e14"></a>
#### §10.1-E14 — mount-table source

Applied by the `/proc/self/mountinfo` `read-exact` row; only the normalized projection and
its evidence-tree copy leave the reader.

<a id="sec101-e15"></a>
#### §10.1-E15 — caller namespace links

Applied by the finite four-member `/proc/self/ns` `read-exact` row.

<a id="sec101-e16"></a>
#### §10.1-E16 — service network namespace

Applied by the exact preregistered-MainPID `read-exact` row; arbitrary or runtime-repinned
PID families are forbidden.

<a id="sec101-e17"></a>
#### §10.1-E17 — evidence descriptor identity

Applied by the `/proc/self/fd/8` `read-exact` row; it binds an existing descriptor and
creates no new path authority.

## Proposed decisions for the three unresolved families

<a id="decision-f1"></a>
### Decision F1 — RP6 executable family

**PROPOSED — LEAD/OWNER DECISION REQUIRED.** Require exactly one frozen pin for each of
`stat`, `readlink`, `env`, `find`, `sha256sum`, `systemctl`, `ss`, `curl`, `timeout`,
`python3`, `id`, and `getent`. The first eleven non-Python names must equal their exact
preregistered `/usr/bin/<name>` paths; `python3` must equal the exact resolved non-symlink
`<WPI_FIXED_TRUSTED_PYTHON>` leaf. Reject missing, duplicate, extra, non-absolute, nonexact,
or unfilled entries and delete every unpinned `command -v`/inherited-PATH fallback. The
production call graph, declared set, bound set, and executed set must be one-to-one.

Rationale: a §10.1 exact-path allowlist is meaningful only if the executable family is
finite before freeze. Allowing an omitted pin or an arbitrary absolute pin makes the
source-derived reachability set open, while a later tool-binding line cannot retroactively
bind a program selected earlier. Closing the twelve-member table preserves the narrow
unprivileged scope without adding a wildcard executable family.

Falsification: remove one required pin or place a marker-writing replacement first on
`PATH`, then drive the real P0 top-level caller. The proposal is wrong if the replacement
runs, its marker appears, or P0 reaches any accepting result instead of STOPping before the
first use. Also add one extra pin and two entries for one canonical tool name; either must
STOP rather than disappear or overwrite.

<a id="decision-f2"></a>
### Decision F2 — RP6 venv-root prefix

**PROPOSED — LEAD/OWNER DECISION REQUIRED.** Before the first path probe, require
`P0_VENV_ROOT` to equal exactly
`/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b`. Basename equality,
canonicality, and an absolute spelling are necessary but not sufficient. Do not widen the
existing venv `read-tree` rule to another prefix.

Rationale: an arbitrary canonical absolute directory whose basename equals the candidate
SHA can live under an operator-controlled or otherwise unpreregistered prefix. Exact
equality converts the runtime prefix family into the already admitted candidate venv tree
and keeps the service-interpreter exception confined to one exact leaf.

Falsification: construct a canonical decoy such as
`<outside-allowlist>/2ce41e34bceb599d80af24c5c33d835820ec321b` with a runnable
`bin/python` and pass it as `P0_VENV_ROOT`. The proposal is wrong if any metadata probe or
execution reaches the decoy, or if the result is anything other than STOP before first
path use.

<a id="decision-f3"></a>
### Decision F3 — evidence-root provenance

**PROPOSED — LEAD/OWNER DECISION REQUIRED.** Make the entrypoint-driven §10.2 composite
proof the only acceptance route. Allocate the exact `REMOTE_BASE` and the P0/RO RUNIDs,
render them into the wrappers and the RO frozen evidence-root constant, then analyze the
final hash-bound wrapper + reachable RP0 library + bootstrap + selected block + inline or
file-backed executed source as one stage composite. The proof must reduce `EV_PARENT`,
`EV_RUNKIT`, `EV_DIR`, `EV_LOG`, every archive/extraction path, and every capture leaf to
strict descendants of the one exact `<REMOTE_BASE>` `write-tree` rule. A missing component,
unresolved value, unbound source edge, or unexplained member is rc 3 and prevents freeze.
Do not accept block-local descendant checks as a substitute and do not widen §10.1.

Rationale: RP6 and RP7 see only values handed to them after wrapper/bootstrap derivation.
They can prove local relationships such as `EV_LOG` below `EV_DIR` while the root itself is
outside the preregistered tree. Only the complete frozen load/value flow can establish
source-to-root provenance without circularly trusting an operator-supplied endpoint.

Falsification: mutate the wrapper or bootstrap so that `EV_DIR` and `EV_LOG` remain
self-consistent but derive from a sibling path outside `<REMOTE_BASE>`, or omit one reachable
source member that performs the derivation. The proposal is wrong if the composite proof
still PASSes, if the mutated member receives no terminal disposition, or if any later block
allocates a leaf before the proof STOPs.

<a id="ordering-fix"></a>
## Attestation ordering fix — two commits, capture first and consume second

The attestation values cannot truthfully appear in a preregistration committed before they
exist, while the command that observes them cannot truthfully be called preregistered if it
runs before any committed procedure names it. The following two-commit sequence is
mandatory and contains no exception for an already-open root session.

### Commit 1 — attestation-capture preregistration

Before any attestation host contact:

1. Allocate the one-use attestation record identifier and the eventual WP-I
   `REMOTE_BASE`/P0/RO RUNID components. Validate their grammar and collision rules. The
   allocation itself performs no host contact.
2. Commit an **attestation-only, non-dispatchable-for-WP-I** document containing:
   - the exact candidate and staging-host identity, the already granted root-channel
     authority, and the statement that this commit authorizes only the read-only
     attestation capture, not WP-I ops 01–12;
   - the exact ordered read-only capture surface: one complete byte-preserved
     `/proc/self/mountinfo` capture from the external root domain; exact `readlink` results
     for `/proc/1/ns/user`, `/proc/1/ns/mnt`, `/proc/1/ns/pid`, and `/proc/1/ns/net`; the
     canonical root-mount identity; and the effective covering-mount identity for the
     preregistered allocation parent used by `EXPECT_PARENT_MOUNT`;
   - the pinned command/producer identity, argv, clean environment, working directory,
     output grammar, status-before-output rules, no-host-write rule, operator-side capture
     route, and production-time record/digest binding;
   - the projection-v2 algorithm and its fixed point/subtree/count universe, including
     later-record-wins tie handling and complete-reader requirements;
   - literal placeholders labelled `NOT-YET-OBSERVED — MUST NOT BE CONSUMED` for the four
     namespace identities, root-mount identity, `EXPECT_PARENT_MOUNT`, and projection-v2
     SHA-256; and
   - the mechanical post-commit binding rule: before it opens a socket or starts the root
     command, the capture recorder must require a clean checkout, derive its current Git
     `HEAD`, prove that `HEAD` contains the exact committed attestation procedure and
     package manifest, and emit that derived object ID as
     `attestation_prereg_commit=<COMMIT_1>`.
3. Verify that Commit 1 contains no attestation-derived value and that its attestation
   procedure has no unfilled command, path, grammar, authority, or producer-identity field.
   If that cannot be shown, the attestation capture does not run.

Only after Commit 1 exists may the exact committed read-only attestation procedure run.
The exact Commit-1 object ID is therefore known without self-reference and is supplied only
by the recorder's clean-current-`HEAD` derivation. The operator-side record must begin by
binding `attestation_prereg_commit=<COMMIT_1>`, must capture stdout/stderr/rc without
editing, and must hash the complete record at production. No WP-I transport op, including
op 01, runs in this interval.

### Values that become computable only after the committed capture

Only the Commit-1-bound capture makes these values available:

1. the exact user, mount, PID, and network namespace identity strings for the external
   staging-guest domain;
2. the canonical root-mount identity used by the P0 row-8 comparison;
3. the effective covering-mount identity for the allocation parent, used as
   `EXPECT_PARENT_MOUNT` by the create-once setup; and
4. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`, computed from the complete normalized
   projection-v2 record derived from the one byte-preserved mountinfo capture.

The attestation evidence record's own SHA-256 and byte count also become computable at this
point. None may be learned from or re-pinned by the later unprivileged login session.

### Commit 2 — consuming successor preregistration

After the attestation record is closed and bound, and before WP-I op 01:

1. Derive the values above exactly once from the captured bytes under the Commit-1
   algorithm. A read, parse, projection, status, completeness, or digest error is STOP and
   no Commit 2 is produced.
2. Complete and commit the dispatchable successor preregistration and frozen run kit. Commit
   2 must:
   - record `attestation_prereg_commit=<COMMIT_1>`, the attestation evidence record path,
     byte count, SHA-256, producer identity, and result status;
   - replace every attestation placeholder with the exact derived value and embed the same
     values in the relevant frozen blocks/wrappers;
   - contain the final exact `REMOTE_BASE`, P0/RO RUNIDs, block/support-script/archive
     hashes, tool pins, access-qualified §10.1 rules, and accepted §10.2 composite-proof
     record;
   - contain no `<PIN-AT-FREEZE>`, `<ALLOCATE-AT-DISPATCH>`,
     `NOT-YET-OBSERVED`, or other unresolved token on a dispatch path; and
   - require the transport preflight, after Commit 2 exists, to perform the same
     clean-current-`HEAD` derivation and emit the resulting object ID as
     `wpi_prereg_commit=<COMMIT_2>` before op 01.
3. Do not amend Commit 1 and do not change the committed capture procedure while inserting
   observed values. If the procedure must change, discard the capture for acceptance,
   create a new Commit 1, and repeat the capture under that new commit.

Only after Commit 2 exists and all ordinary authority/budget gates hold may op 01 run.
Neither commit embeds its own Git object ID; doing so would be an unsatisfiable hash
self-reference. Commit 2 may and must embed Commit 1's already-known ID. Each commit's own
ID is bound after that commit exists by the corresponding clean-current-`HEAD` recorder,
under a procedure already present in its committed bytes.

### Mechanical order-violation check

The pre-dispatch gate must STOP unless all of the following hold:

1. `attestation_prereg_commit` resolves to Commit 1 and is a strict Git ancestor of Commit
   2; the attestation recorder proves its clean current `HEAD` was Commit 1 before capture,
   and the transport preflight proves its clean current `HEAD` is Commit 2 before op 01.
   The latter is the exact `wpi_prereg_commit` emitted by the preflight.
2. The attestation record's first bound field equals the exact Commit-1 object ID, and its
   recomputed byte count and SHA-256 equal the values recorded by Commit 2.
3. The Commit-1 version contains the full capture procedure and no derived value; the
   Commit-2 version contains every derived value and no unresolved dispatch token.
4. The attestation-procedure bytes, projection algorithm, capture universe, and producer
   identity are byte-identical between Commit 1 and Commit 2. The allowed Commit-1-to-Commit-2
   delta is the insertion of captured values/evidence identity plus completion of the
   successor/run-kit freeze; it may not retroactively change how the values were observed.
5. No transport record for WP-I ops 01–12 predates or names anything other than Commit 2.
   The runner derives Commit 2 from a clean current `HEAD`, proves that object contains the
   exact successor and frozen package manifest, and emits it before starting op 01; a dirty
   checkout, missing object, content mismatch, or different `HEAD` is STOP before host
   contact.

Any failed predicate is `ORDER_STOP reason=attestation_prereg_order_violation
detail=<fixed-token>` and makes both the attestation values and the WP-I RUNIDs unusable for
dispatch. Commit timestamps alone are not evidence of order; the two recorded Git object
IDs, strict ancestry, byte identity, evidence digest binding, and runner preflight are the
binding chain.

### Invariant that breaks the circle

**The procedure that produces an observation is committed before the observation; the
value of that observation is committed before any operation consumes it. No commit both
authorizes an attestation observation and claims that its not-yet-observed value was already
frozen.**

## SELF-QA

This is manual document QA only. No proposed command, block, fixture, attestation, host
contact, archive build, or Git mutation was executed. One read-only baseline `git status`
was obtained during repository onboarding before the kickoff file, and therefore its
no-Git constraint, had been read; after that constraint was known, no Git command was run.

### One satisfying line per admitted member

| ID | The line that satisfies the member |
|---|---|
| EXT-01 | ``| `read-exact` | `/` | Canonical-root identity and ancestor-kind binding only … |`` |
| EXT-02 | ``| `read-exact` | `/opt`, `/opt/mtc-bridge`, `/opt/mtc-bridge/releases`, `/opt/mtc-bridge/venvs` | … |`` |
| EXT-05 | ``| `read-exact` | `/usr`, `/usr/bin` | Fixed root-owned ancestors … |`` |
| EXT-06 | ``| `read-execute-exact` | `/usr/bin/stat`, …, `/usr/bin/getent`, and exact `<WPI_FIXED_TRUSTED_PYTHON>` | … |`` |
| EXT-08 | ``| `read-exact` | `/etc` | Fixed root-owned ancestor … |`` |
| EXT-10 | ``| `read-exact` | `/var`, `/var/lib`, `/var/log` | Fixed root-owned ancestors … |`` |
| EXT-13 | ``| `read-exact` | `/proc/uptime` | Read only for monotonic timestamps … |`` |
| EXT-14 | ``| `read-exact` | `/proc/self/mountinfo` | Read only to derive … |`` |
| EXT-15 | ``| `read-exact` | `/proc/self/ns/user`, `/proc/self/ns/mnt`, `/proc/self/ns/pid`, `/proc/self/ns/net` | … |`` |
| EXT-16 | ``| `read-exact` | exact `/proc/<WPI_MAINPID>/ns/net` … | … |`` |
| EXT-17 | ``| `read-exact` | `/proc/self/fd/8` | Read only to prove … |`` |
| FAM-01 | “Require exactly one frozen pin for each of `stat` … `getent` … and delete every unpinned `command -v`/inherited-PATH fallback.” |
| FAM-02 | “Before the first path probe, require `P0_VENV_ROOT` to equal exactly `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b`.” |
| FAM-03 | “Make the entrypoint-driven §10.2 composite proof the only acceptance route.” |
| ORDER-01 | “The procedure that produces an observation is committed before the observation; the value of that observation is committed before any operation consumes it.” |

Disposition recount: 11 extension lines present; 3 proposed-family lines present and each
marked `PROPOSED — LEAD/OWNER DECISION REQUIRED`; 1 ordering line present; total 15/15.

### Two-commit sequence walk

1. Before Commit 1, the attestation values do not exist and no text needs them: Commit 1
   contains only the fully specified capture procedure, concrete identifiers/authority, and
   explicit non-consumable placeholders.
2. Commit 1 exists before capture. The recorder derives Commit 1's object ID from a clean
   current `HEAD`; the capture needs only that committed procedure and derived ID, not any
   value that it is about to observe.
3. The capture returns and is closed. Only now do the four namespace identities, root-mount
   identity, allocation-parent mount identity, projection-v2 digest, and evidence-record
   digest/bytes exist.
4. Commit 2 consumes exactly those now-existing values, freezes the final artifacts and
   successor, and records both the Commit-1 and evidence identities. It does not require a
   future host result.
5. Op 01 begins only after Commit 2. Its preflight derives the already-existing Commit-2
   ID from a clean current `HEAD` and uses the already-frozen values; no value is learned
   and retroactively preregistered, and no commit embeds its own ID.

Therefore no value is needed before it exists: Commit 1 needs zero attestation outcomes;
the attestation needs only Commit 1; Commit 2 needs the completed attestation; and the WP-I
run needs Commit 2.
