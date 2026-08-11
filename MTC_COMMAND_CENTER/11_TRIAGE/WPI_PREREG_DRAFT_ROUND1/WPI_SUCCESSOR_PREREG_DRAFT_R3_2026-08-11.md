# WP-I SUCCESSOR PREREGISTRATION — DRAFT ROUND 3, MERGED LANES A+B

Date: 2026-08-11  
Authoring surface and recorded audit tier: T2 preregistration text only  
Base: `WPI_SUCCESSOR_PREREG_DRAFT_R2_2026-08-11.md` (commit `784693e4`)  
Merged input: `SEC101_ATTESTATION_APPLICATION_2026-08-11.md` (commit `c0dea12d`)

This is a successor **draft**, not a dispatch record. It mints no identifier, fills no attestation, runs no block, contacts no host, and authorizes no operation. Every allocation remains `<ALLOCATE-AT-DISPATCH>` and every not-yet-accepted identity remains `<PIN-AT-FREEZE>`.

The accepted content of `WPI_PREREGISTRATION_DRAFT.md` remains the baseline except where this document explicitly supersedes it. This draft merges the accepted Lane-B application for section 10.1 and attestation ordering. The three Lane-B family decisions remain proposed, and the three explicit `MERGE-CONFLICT` items in section 4.5.4 remain Lead/owner decision gates; until those decisions are made, this draft is not complete and freeze must STOP.

## 0. Scope and immutability

- Pine, parity, MTC, trading, broker, credential, deployment, and live/economic behavior are outside this document and unchanged.
- Section 8.2 rows 1–9 are not authored or redesigned here. Their existing preregistered definitions remain the only definitions, subject to the owner-selected coverage gate in section 4.6.
- The owner-selected external-to-login attestation option is retained. The rejected option branches and the skeleton's stray unresolved-status residue are not retained.
- No operation 01–12, block, wrapper, transport process, remote allocation, or host-side observation is authorized by this draft.

## 1. Values already resolvable

These values are carried into finalization from committed records; they are not learned from the object being attested.

| Variable | Value | Source and rule |
|---|---|---|
| `WPI_UNIT_FRAGMENT_SHA256` | `538c1c6038b475e87fb0e9b9c35fd4ebd8451b40ff93538f8fea5aa0b49279bd` | `LEAD_PIN_RESOLUTION_2026-08-10.md` R1; never re-pinned from the host observation |
| `WPI_LOG_DIR` | `/var/log/mtc-bridge` | `LEAD_PIN_RESOLUTION_2026-08-10.md` R2 |
| `WPI_EXPECTED_DROPIN_SET` | empty set | Source-derived expectation: zero drop-ins for `mtc-bridge-first-start.service`; a non-empty observed set is FAIL, inability to enumerate is STOP |
| `P0_STATE_UID` / `P0_STATE_GID` | `999` / `988` | Recorded `getent` preflight; numeric identity is authoritative |
| `P0_EXPECT_UID` / `P0_EXPECT_GID` | numeric uid/gid of the recorded `gatea` login | Filled from the recorded login identity, never from rendered names |
| Candidate, roots, lock identity, package count, endpoint, and sweep budget | exactly as `WPI_PREREGISTRATION_DRAFT.md` section 2 | unchanged |

## 2. Freeze-input conservation

### 2.1 Exhaustive fill manifest

Stage 1 maintains one per-consumer fill manifest and proves every entry is populated before any operation.

| Input family | Mandatory consumers and conservation rule |
|---|---|
| Allocation | One generated base supplies both derived RUNIDs, both wrappers, `$BASE_RUN`, `$CONFIRM_TOKEN`, `$RECORD_ROOT`, every `TRANSPORT_PLAN.tsv` occurrence, the remote-base suffix, retrieval paths, local binding paths, evidence roots, and all derived archive/record fields; every occurrence must equal the one validated source value. |
| Projection-v2 digest | The same digest fills `RP7-WPI-RO.sh:WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` and `run_ro.sh:WPI_ATTESTED_MOUNTINFO_SHA256`. |
| Trusted system Python | The same resolved non-symlink system-Python leaf fills `RP6-P0.sh:P0_FIXED_TRUSTED_PYTHON`, `RP7-WPI-RO.sh:WPI_FIXED_TRUSTED_PYTHON`, and the `python3=` entry of both `P0_TOOL_PINS` and `WPI_TOOL_PINS`. |
| Row-8 execution domain | All five values fill both the embedded `P0_FIXED_ATTESTED_{USER_NS,MNT_NS,PID_NS,NET_NS,ROOT_MOUNT_ID}` literals and the wrapper-supplied/exported `P0_ATTESTED_{USER_NS,MNT_NS,PID_NS,NET_NS,ROOT_MOUNT_ID}` inputs. `run_p0.sh` must define and export all five before it sources `RP6-P0.sh`; an omitted export is freeze STOP. |
| P0 tool pins | The exact 12-entry map is `stat readlink env find sha256sum systemctl ss curl timeout python3 id getent`; every entry is an absolute frozen path, no PATH fallback exists, and shared entries equal their RP7 counterparts. |
| RP7 tool pins | The exact 10-entry map is `stat readlink env find sha256sum systemctl ss curl timeout python3`; every entry is an absolute frozen path and no PATH fallback exists. |
| Parent mount | `remote_setup_wpi.sh:EXPECT_PARENT_MOUNT` is filled from the accepted source and compared with the attested projection; inability to compute or compare is STOP. |
| OpenSSH configuration | Record bytes and SHA-256 for `wpi_known_hosts`, bytes and SHA-256 for `wpi_known_hosts_global`, SHA-256 for `gatea_ed25519` without printing its bytes, and the frozen `ssh.exe` and `scp.exe` identities. |
| Close helper | Record bytes and SHA-256 for `remote_close_tree_wpi.sh`; its identity, argv, launch domain, work-root semantics, and plan rows must satisfy section 4.7. |
| Transport and archive | Record the plan digest, runner digest, deterministic runkit bytes/digest, five distinct stdin-file digests, `EXPECT_UID`/`EXPECT_GID`, archive bytes, six archive-member digests, every block digest, and both wrapper digests. |
| Carried allocation record | Record the one base, both RUNIDs, both stage IDs, remote and operator roots, confirmation token, allocation/burn-ledger entry, and every collision-check outcome. |

Equality across every duplicated consumer is checked mechanically, not assumed from shared spelling or marker absence. The manifest enforces a conservation equation for every family: declared consumers = populated consumers = equality-checked consumers, with no silent drop, overwrite, or extra consumer.

### 2.2 Targeted fills only

The freeze tool accepts an allowlist of exact `(file, constant-or-table-field)` edit sites and refuses a file-wide or repository-wide marker replacement.

It changes consumer assignments and table cells one at a time. After filling, it proves byte-for-byte that `$UNFILLED_MARKERS = @('<ALLOCATE-AT-DISPATCH>', '<PIN-AT-FREEZE>')` and every other marker-comparison guard is unchanged, while separately proving that no allocation or freeze marker remains in any consumer value, argv, plan field, archive constant, or hash field. Marker literals retained solely inside guards are expected and are not classified as unfilled inputs.

Any edit outside the allowlisted site set, any changed guard literal, any marker in a consumer, or any unclassified marker occurrence is freeze STOP.

### 2.3 No inert pins

`WPI_INTERPRETER_TARGET` must be absent from the final wrapper and fill ledger unless an accepted block gives it an explicit predicate and production consumer; a filled but unread value is not a preregistered check.

Row 18 continues to require the exact `<WPI_VENV_ROOT>/bin/python` object to be a non-symlink regular executable unless that row is explicitly redesigned and re-audited.

### 2.4 P0 environment reconciliation

The successor may not carry the blanket probe-execution-environment rule while the accepted RP6 bytes disclaim it.

Before freeze, either RP6 is repaired so every evidence-producing child satisfies the cleared-environment, fixed trusted cwd, run-owned TMPDIR, pinned-target-chain, and isolated-Python contract and the changed bytes are re-audited, or the successor is narrowed to the exact mixed environment the final RP6 bytes prove and that weaker claim receives explicit acceptance.

Silence, inherited wording, or a claim broader than the final RP6 predicates is freeze STOP.

## 3. Identifier minting and one-use discipline

### 3.1 Exact generator grammar and width

The Stage-1 generator grammar is exact: `UTCSTAMP := [0-9]{8}T[0-9]{6}` (15 ASCII bytes), `NONCE := [0-9a-f]{8}` (8 ASCII bytes), and `BASE := WPI-<UTCSTAMP>Z-<NONCE>` (29 ASCII bytes).

The only Stage-1 generator procedure is the following PowerShell procedure, whose literal command, stdout, stderr, rc, shell version, and resulting values are preserved in the Stage-1 record:

```powershell
$utc = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmss', [Globalization.CultureInfo]::InvariantCulture)
$nonceBytes = New-Object byte[] 4
$rng = [Security.Cryptography.RandomNumberGenerator]::Create()
try { $rng.GetBytes($nonceBytes) } finally { $rng.Dispose() }
$nonce = ([BitConverter]::ToString($nonceBytes)).Replace('-', '').ToLowerInvariant()
$base = "WPI-${utc}Z-${nonce}"
if ($utc -cnotmatch '^[0-9]{8}T[0-9]{6}$') { throw 'UTCSTAMP_GRAMMAR_STOP' }
if ($nonce -cnotmatch '^[0-9a-f]{8}$') { throw 'NONCE_GRAMMAR_STOP' }
if ($base -cnotmatch '^WPI-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$' -or $base.Length -ne 29) { throw 'BASE_GRAMMAR_STOP' }
```

No placeholder is tested as though it were a concrete identifier. The predicate has no length limit, so the fixed widths above—not predicate acceptance alone—supply the filesystem-component length contract.

### 3.2 Derive once, then validate every component

From the one generated base, Stage 1 derives—never independently types—`<base>-P0`, `<base>-RO`, `p0`, `ro`, `wpi_staging_<base>`, `<base>-EXECUTE`, and `WPI_TRANSPORT_<base>` before any consumer is written.

The exact pinned `RP0-LIB.sh` object is first verified as 18,968 bytes with SHA-256 `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48`; only then is its `rp0_require_safe_component` sourced under `LC_ALL=C` for the minting transcript.

Every derived path component listed above is passed as the explicit second argument to the pinned predicate and must return exactly rc 0 with the expected `component_ok` token before any wrapper, runner, plan, ledger consumer, or path field is populated.

The accepted language is one or more ASCII characters from `[A-Za-z0-9._-]`, with the first character not `-`, minus the complete strings `.` and `..`; predicate acceptance is necessary but not sufficient for allocation.

### 3.3 Per-consumer equality hard gate

Stage 1 proves that every wrapper constant, runner constant, plan occurrence, derived remote path, retrieval path, local bind path, record-root leaf, confirmation token, and evidence-tree leaf equals the value derived from the one tested base.

This conservation proof is a pre-commit hard gate and is the selected protection for the Windows runner's early `$RECORD_ROOT` creation; no new local component validator is claimed, and the runner may not execute until the proof passes on its final bytes.

The equality record names every consumer individually, records its exact parsed value, and ends with declared count = observed count = equal count. Duplicate keys, unregistered occurrences, missing consumers, independently typed values, or a count mismatch are freeze STOP.

### 3.4 Acceptance and refusal transcript

The self-QA transcript records literal invocations plus stdout, stderr, and rc for the concrete base, both derived RUNIDs, both stage IDs, the remote-base leaf, confirmation token, and operator-record leaf; every acceptance must be rc 0 with the expected reason token.

The finite negative cases are called **refusal representatives**, never “the refusal set,” and are executed as follows against the exact pinned function:

| Refusal class | Exact shell input expression | Expected result |
|---|---|---|
| empty | `''` | rc 1, `component_reserved` |
| dot | `'.'` | rc 1, `component_reserved` |
| dot-dot | `'..'` | rc 1, `component_reserved` |
| leading dash | `'-lead'` | rc 1, `component_leading_dash` |
| POSIX separator | `'a/b'` | rc 1, `component_charset` |
| backslash | `'a\b'` | rc 1, `component_charset` |
| whitespace | `'bad name'` | rc 1, `component_charset` |
| control byte | `$'bad\x01name'` | rc 1, `component_charset` |
| non-ASCII bytes | `$'caf\xC3\xA9'` under `LC_ALL=C` | rc 1, `component_charset` |
| glob metacharacter | `'bad*name'` | rc 1, `component_charset` |

The empty case is passed as an explicit empty second argument, not as a missing argument. A different rc, a missing/incorrect reason token, an unrecorded stream, or a command that requires editing before replay is self-QA STOP.

### 3.5 Append-only allocation and burn ledger

Stage 1 uses the committed append-only ledger `WPI_RUNID_ALLOCATION_BURN_LEDGER.md`; the candidate base and both derived RUNIDs must be absent from the complete ledger history and all retained operator/remote-root records before allocation can proceed.

The collision scan includes, at minimum, `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08`, its `-R45B` successor, every later retained operator record root, and the remote `/home/gatea/` allocation ledger; both the operator record root and remote base remain create-once.

One ledger row records the base, P0 RUNID, RO RUNID, generator timestamp, nonce, final disposition (`RESERVED`, `BURNED`, or `SPENT`), reason, successor identity, and evidence/record roots. Existing rows are never edited or deleted; state changes append a new row referring to the prior row.

The new ledger entry must be committed in the pre-operation sequence selected by the accepted attestation ordering text in section 5.2. Evidence retention and checks against only two historical roots are supplemental; neither is a global uniqueness proof.

If grammar, predicate, equality, collision, fill, commit, or remote create-once allocation fails, the base and both stage RUNIDs are appended as `BURNED`, no consumer is retried under those identifiers, and a new attempt requires a new preregistration rather than an in-document retry pool.

## 4. Ordered freeze gates

Each gate blocks every later gate. A STOP is inability to complete the freeze proof; it is not a host-state FAIL.

### 4.1 Final-byte acceptance floor

RP6-P0, RP7-WPI-RO, and the transport set must each hold both required fresh flagship T0 acceptances on the exact post-repair bytes that Stage 1 will freeze.

Any later executable-byte change supersedes the corresponding acceptance and returns that artifact to its required T0 review gate.

### 4.2 Pre-acceptance path repairs

Before the final T0 pair reviews the artifacts: remove every RP6/RP7 write-open of `/dev/null`; require the exact 12-entry `P0_TOOL_PINS` map with no PATH fallback and shared pins equal to RP7; and require `P0_VENV_ROOT` to equal `/opt/mtc-bridge/venvs/$P0_CAND` exactly.

The composite proof also enumerates wrapper/support-layer `/dev/null` opens: every write-open outside the evidence tree is removed, and any remaining read-open is separately justified and access-qualified or removed.

These changes occur before acceptance; their exact D026 falsifications are rerun RED against the pre-fix behavior or an equivalent mutation and GREEN on the final bytes, with literal commands and real output recorded. Acceptance of pre-repair bytes does not count.

### 4.3 Fill-input gate

All section-1 values, every section-2 manifest member, every section-3 allocation consumer, block/wrapper/transport hashes, archive constants, and the accepted attestation outputs are populated and conservation-checked. An unfilled, inert, duplicated, or unequal consumer is freeze STOP.

### 4.4 Composite path-scope proof

The Stage-1 proof unit is each complete frozen same-shell composition: `run_p0.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP6-P0.sh`, and `run_ro.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP7-WPI-RO.sh`, with the concrete allocation and freeze manifest applied; the RO graph also includes every executed inline program and the exact executed `verify_lock.py` source.

The accepted analyzer follows sourced values and registered production-call contracts; derives `RUNID`, `EV_STAGE_ID`, `EV_DIR`, and `EV_LOG` from the exact frozen `REMOTE_BASE`; enumerates every reachable path-bearing argument, redirection, test, executable object, endpoint, nested source, and closed runtime family; and assigns every admitted member exactly one terminal disposition.

Unknown commands, unconsumed options, unresolved/dynamic construction, unbound source edges, startup-source ambiguity, opaque sinks, unclosed runtime families, component hash mismatches, missing values, or conservation mismatches are rc 3 and prevent freeze. Zero resolved facts plus PASS is forbidden.

A block-only result is supplemental. The current prover's lower-bound output cannot satisfy this gate until its findings are repaired with exact composite RED/GREEN commands and real output and a fresh T1 review accepts the analyzer on the final proof semantics.

### 4.5 Section 10.1 application and access grammar

#### 4.5.1 Unprivileged path and endpoint allowlist

The P0 and RO stages may use only the rules in this section. The list is exhaustive for
source-controlled filesystem operands, network endpoints, and closed runtime-derived
families in the complete frozen stage composites defined by section 4.4. A path match without a
matching access qualifier is not admission. Anything unmatched, dynamically unresolved,
or reached with a stronger access class is a Stage-1 STOP and prevents archive freeze.

This section does not claim to enumerate undocumented internal opens performed by Bash,
the dynamic loader, libc, Python, or other pinned external binaries. Those are the named
external-runtime boundary in section 4.4. Runtime-selected descendants are admissible only when
the complete composite proof establishes that they remain inside a listed closed tree.

##### Access-qualifier grammar

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

##### Exhaustive rules

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
##### §10.1-E01 — canonical root

Applied by the `/` `read-exact` row; the rule retains only canonical-root metadata and
device/inode identity.

<a id="sec101-e02"></a>
##### §10.1-E02 — `/opt` ancestors

Applied by the finite `/opt` ancestor `read-exact` row; no content enumeration or wildcard
ancestor family is admitted.

<a id="sec101-e05"></a>
##### §10.1-E05 — `/usr` ancestors

Applied by the finite `/usr`, `/usr/bin` `read-exact` row; executable authority remains in
the separate exact tool rule.

<a id="sec101-e06"></a>
##### §10.1-E06 — exact executable objects

Applied by the finite `read-execute-exact` tool row. Its RP6 half is effective only after
Decision F1 is accepted and the complete frozen pin set is mechanically conserved.

<a id="sec101-e08"></a>
##### §10.1-E08 — `/etc` ancestor

Applied by the `/etc` `read-exact` row; `/etc/mtc-bridge` remains a separate terminal-only
rule.

<a id="sec101-e10"></a>
##### §10.1-E10 — `/var` ancestors

Applied by the finite `/var`, `/var/lib`, `/var/log` `read-exact` row; the state and log
directories remain separate terminal-only rules.

<a id="sec101-e13"></a>
##### §10.1-E13 — monotonic clock source

Applied by the `/proc/uptime` `read-exact` row.

<a id="sec101-e14"></a>
##### §10.1-E14 — mount-table source

Applied by the `/proc/self/mountinfo` `read-exact` row; only the normalized projection and
its evidence-tree copy leave the reader.

<a id="sec101-e15"></a>
##### §10.1-E15 — caller namespace links

Applied by the finite four-member `/proc/self/ns` `read-exact` row.

<a id="sec101-e16"></a>
##### §10.1-E16 — service network namespace

Applied by the exact preregistered-MainPID `read-exact` row; arbitrary or runtime-repinned
PID families are forbidden.

<a id="sec101-e17"></a>
##### §10.1-E17 — evidence descriptor identity

Applied by the `/proc/self/fd/8` `read-exact` row; it binds an existing descriptor and
creates no new path authority.

#### 4.5.2 Proposed decisions for the three unresolved families

The three source families that cannot be closed by section 4.5.1 alone are decided proposals, not
silent assumptions. Each is marked `PROPOSED — LEAD/OWNER DECISION REQUIRED`. Until all
three are accepted and implemented in the frozen composite, Stage 1 STOPs and no archive or
successor preregistration is dispatchable.

<a id="decision-f1"></a>
##### Decision F1 — RP6 executable family

**PROPOSED — LEAD/OWNER DECISION REQUIRED.** Require exactly one frozen pin for each of
`stat`, `readlink`, `env`, `find`, `sha256sum`, `systemctl`, `ss`, `curl`, `timeout`,
`python3`, `id`, and `getent`. The first eleven non-Python names must equal their exact
preregistered `/usr/bin/<name>` paths; `python3` must equal the exact resolved non-symlink
`<WPI_FIXED_TRUSTED_PYTHON>` leaf. Reject missing, duplicate, extra, non-absolute, nonexact,
or unfilled entries and delete every unpinned `command -v`/inherited-PATH fallback. The
production call graph, declared set, bound set, and executed set must be one-to-one.

Rationale: a section-10.1 exact-path allowlist is meaningful only if the executable family is
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
##### Decision F2 — RP6 venv-root prefix

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
##### Decision F3 — evidence-root provenance

**PROPOSED — LEAD/OWNER DECISION REQUIRED.** Make the entrypoint-driven section-4.4 composite
proof the only acceptance route. Allocate the exact `REMOTE_BASE` and the P0/RO RUNIDs,
render them into the wrappers and the RO frozen evidence-root constant, then analyze the
final hash-bound wrapper + reachable RP0 library + bootstrap + selected block + inline or
file-backed executed source as one stage composite. The proof must reduce `EV_PARENT`,
`EV_RUNKIT`, `EV_DIR`, `EV_LOG`, every archive/extraction path, and every capture leaf to
strict descendants of the one exact `<REMOTE_BASE>` `write-tree` rule. A missing component,
unresolved value, unbound source edge, or unexplained member is rc 3 and prevents freeze.
Do not accept block-local descendant checks as a substitute and do not widen section 4.5.1.

Rationale: RP6 and RP7 see only values handed to them after wrapper/bootstrap derivation.
They can prove local relationships such as `EV_LOG` below `EV_DIR` while the root itself is
outside the preregistered tree. Only the complete frozen load/value flow can establish
source-to-root provenance without circularly trusting an operator-supplied endpoint.

Falsification: mutate the wrapper or bootstrap so that `EV_DIR` and `EV_LOG` remain
self-consistent but derive from a sibling path outside `<REMOTE_BASE>`, or omit one reachable
source member that performs the derivation. The proposal is wrong if the composite proof
still PASSes, if the mutated member receives no terminal disposition, or if any later block
allocates a leaf before the proof STOPs.

#### 4.5.3 Lane-B application conservation

The admitted Lane-B application universe is exactly 15 members: 11 `EXTEND` items, 3 unresolved families, and 1 ordering fix. Every member has exactly one terminal disposition and one explicit anchor in the combined disposition table in section 8; none is absorbed into another row.

Conservation equation: `15 admitted = 11 INCLUDE extensions + 3 explicit proposed decisions + 1 INCLUDE ordering fix`; terminal dispositions = 15; omitted/overwritten members = 0.

#### 4.5.4 MERGE-CONFLICT register — no adjudication

The following contradictions are preserved rather than silently resolved:

1. **MERGE-CONFLICT MC-01 — RP6 executable family.** R2 sections 2.1 and 4.2 already require the exact 12-entry `P0_TOOL_PINS` map with no PATH fallback, while Lane-B Decision F1 keeps that same closure `PROPOSED — LEAD/OWNER DECISION REQUIRED`. This draft makes no decision; Lead/owner resolution is required before freeze.
2. **MERGE-CONFLICT MC-02 — RP6 venv-root family.** R2 section 4.2 already requires `P0_VENV_ROOT` to equal `/opt/mtc-bridge/venvs/$P0_CAND` exactly, while Lane-B Decision F2 keeps the exact-root closure `PROPOSED — LEAD/OWNER DECISION REQUIRED`. This draft makes no decision; Lead/owner resolution is required before freeze.
3. **MERGE-CONFLICT MC-03 — evidence-root provenance.** R2 section 4.4 already makes the complete frozen composite proof the acceptance route and classifies block-only results as supplemental, while Lane-B Decision F3 keeps that route `PROPOSED — LEAD/OWNER DECISION REQUIRED`. This draft makes no decision; Lead/owner resolution is required before freeze.

### 4.6 Section 8.2 rows 1–9 coverage gate

Owner decision: all nine existing section-8.2 rows are bound into `RP7-WPI-RO.sh` only after the currently reviewed RP7 bytes receive their dual flagship acceptance; this merged draft does not restate or redesign those rows.

Operations 04 and 05 currently do not establish rows 1–9, and P0's `Manager.Version` readiness query is a premise only, not evidence for any B2/B4 row. Freeze remains blocked until the post-acceptance RP7 extension executes all nine in the already-preregistered first-divergence order, the plan invokes the accepted final bytes, and the changed artifact receives the required final-byte T0 acceptances.

### 4.7 Close-script contract and RUNID boundary

Freeze is blocked until the actual `remote_close_tree_wpi.sh`, plan rows 07/08, derivation contract, launch-domain claim, scratch-location semantics, and RED/GREEN evidence describe one byte-identical executable contract and the script reaches its RUNID/`EV_DIR` validation rather than failing earlier on argv shape.

If derivation classes 5 and 6 remain preregistered, the accepted script must implement the cleared launch domain and run-owned scratch semantics and the plan must pass the required `WORK_ROOT`; if final accepted bytes retain a two-argument inherited-TMPDIR contract, the successor must delete those claims and surface the weaker contract for T0 adjudication. The cleared launch domain closes the inner child only; the outer SSH account-shell boundary (a server-supplied `BASH_ENV`/`ENV` acting before `env -i`) remains OPEN, and no successor text may present the cleared inner-child domain as an end-to-end F1 closure.

Hash agreement with a report whose prose or plan argv describes different behavior is not closure evidence. Ops 07 and 08 remain separate close invocations; no retrieval or local bind substitutes for this boundary.

### 4.8 P0 environment gate

Apply section 2.4 before artifact acceptance. The final successor's environment claim must be mechanically equal to what final RP6 production call paths establish; a stronger inherited sentence is prohibited.

### 4.9 Deterministic runkit and final identities

The deterministic `runkit.tar` member set is exactly `RP0-LIB.sh`, `RP0-BOOTSTRAP.sh`, `RP6-P0.sh`, `RP7-WPI-RO.sh`, `run_p0.sh`, and `run_ro.sh`; `RP1-B3.sh` is excluded.

Stage 1 fills the six member identities into the extractor, records archive bytes and SHA-256, re-hashes all blocks/wrappers/transport files, proves the extracted identities equal the manifest, and adds the completed successor plus its checksum set. Any hidden or extra member is STOP.

### 4.10 Final merge and pre-operation commit

The two-commit attestation ordering procedure in section 5.2 is mandatory and contains no exception for an already-open root session. Its mechanical order-violation check must pass before the final successor becomes dispatchable.

The merged final successor contains no unresolved Lane-B placeholder and must itself be committed with the final checksum set before op 01, any block/wrapper/transport process, or any host-side allocation begins.

## 5. External attestation scope

### 5.1 Owner-selected contract and residue removal

The owner-selected contract is option (a): the projection-v2 digest and row-8 namespace/root-mount identities are produced outside the ssh login domain they attest, through the separately preregistered read-only root command set covered by grant #6.

`WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`, both trusted-Python pins, the five row-8 execution-domain identities, and `EXPECT_PARENT_MOUNT` are produced only by the committed grant-#6 attestation procedure completed by the section-5.2 text.

The login session may not learn and re-pin its own namespace or mount identity. Equality with a PID visible from inside that login domain, including visible PID 1, is not a substitute for external attestation. If the external attestation is unavailable, malformed, incomplete, or unequal, P0 STOPs and no RO row runs.

No obsolete option branch, unresolved-status label, or standalone residue from the skeleton is part of this draft.

### 5.2 Attestation ordering fix — two commits, capture first and consume second

The attestation values cannot truthfully appear in a preregistration committed before they
exist, while the command that observes them cannot truthfully be called preregistered if it
runs before any committed procedure names it. The following two-commit sequence is
mandatory and contains no exception for an already-open root session.

#### Commit 1 — attestation-capture preregistration

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

#### Values that become computable only after the committed capture

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

#### Commit 2 — consuming successor preregistration

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
     hashes, tool pins, access-qualified section-4.5.1 rules, and accepted section-4.4 composite-proof
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

#### Mechanical order-violation check

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

#### Invariant that breaks the circle

**The procedure that produces an observation is committed before the observation; the
value of that observation is committed before any operation consumes it. No commit both
authorizes an attestation observation and claims that its not-yet-observed value was already
frozen.**

## 6. Transport operations and observed-outcome semantics

The successor reproduces the exact current `TRANSPORT_PLAN.tsv` ops 01–12 and the current runner's first-mismatch semantics: after the first mismatching or not-evaluable `sequence_ok` operation, later `sequence_ok` operations are skipped and all `always` operations still run; results are classified by operation kind and provenance, not by rc alone; ssh rc 255, every nonzero scp rc, an rc outside a kind's grammar, or an ssh rc without a remote-program marker is not-evaluable; and an `always` failure caused by an earlier broken sequence **on its own branch** is not-evaluable rather than a new host FAIL, with the first applicable reason recorded — a nonzero scp reports `scp_transfer_did_not_complete` and an rc 3 reports `operation_reported_stop` whatever its prerequisites, and only an rc-1 `always` failure reaches prerequisite adjudication and names which case it is (`cleanup_after_unestablished_prerequisite` or `cleanup_after_earlier_deviation`); every `always` operation emits `TR_OP_PREREQ_STATE` with each edge's resolved class regardless. Cleanup prerequisites are modelled per branch and per operation (07<-04, 08<-05, 09<-07, 10<-08, 11<-07+09, 12<-08+10), so an unrelated branch's failure never demotes a genuine marked rc 1 to not-evaluable; and an `ssh_stdin` operation's provenance marker must come from the family belonging to the stdin artifact that row sends, not from a global union of every program's prefixes.

Ops 07/08 close via `remote_close_tree_wpi.sh`, ops 09/10 retrieve, ops 11/12 bind locally, and op 06 is the operator-side row-24 host contact. The runner's `-Execute` and `-Confirm` switches are technical interlocks, not authority.

## 7. Post-run sequence

After the preregistered operations complete: retrieve P0/RO evidence under ops 09/10; bind each digest set locally under ops 11/12; produce the WP-I closure record and unit/hour ledger; dispatch Audit 2 with the resolved supplemental-review flag; and later run the separately authorized `RPD-VERIFY` root-side procedure to close its deferred checks. None of those later steps repairs a failed freeze gate or retroactively validates a reused identifier.

## 8. Combined disposition table — conservation 19 + 15

The R2 universe has 19 members and the Lane-B application universe has 15 members. Every source member appears once below with one terminal state. The three family proposals are not decided by this merge.

| Ledger | Item | Terminal disposition | Section anchor / reason |
|---|---|---|---|
| R2-01 | Skeleton Gap 1 | APPLIED | [§2.1 Exhaustive fill manifest](#21-exhaustive-fill-manifest) |
| R2-02 | Skeleton Gap 2 | APPLIED | [§2.2 Targeted fills only](#22-targeted-fills-only) |
| R2-03 | Skeleton Gap 3 | APPLIED — LANE-B TEXT MERGED | [§5.2 Attestation ordering fix](#52-attestation-ordering-fix--two-commits-capture-first-and-consume-second) |
| R2-04 | Skeleton Gap 4 | APPLIED | [§4.4 Composite path-scope proof](#44-composite-path-scope-proof) |
| R2-05 | Skeleton Gap 5 | APPLIED — LANE-B TEXT MERGED | [§4.5 Section 10.1 application](#45-section-101-application-and-access-grammar); the three family proposals remain undecided |
| R2-06 | Skeleton Gap 6 | APPLIED — LANE-B TEXT MERGED | [§4.5.1 Access grammar](#451-unprivileged-path-and-endpoint-allowlist) |
| R2-07 | Skeleton Gap 7 | APPLIED | [§4.2 Pre-acceptance path repairs](#42-pre-acceptance-path-repairs) |
| R2-08 | Skeleton Gap 8 | APPLIED | [§4.6 Rows 1–9 coverage gate](#46-section-82-rows-19-coverage-gate) without redesigning the rows |
| R2-09 | Skeleton Gap 9 | APPLIED | [§2.4 P0 environment reconciliation](#24-p0-environment-reconciliation) and [§4.8](#48-p0-environment-gate) |
| R2-10 | Skeleton Gap 10 | APPLIED | [§6 Transport operations](#6-transport-operations-and-observed-outcome-semantics) |
| R2-11 | Skeleton Gap 11 | APPLIED | [§4.7 Close-script contract](#47-close-script-contract-and-runid-boundary) |
| R2-12 | Skeleton Gap 12 | APPLIED | [§2.3 No inert pins](#23-no-inert-pins) |
| R2-13 | Skeleton Gap 13 | APPLIED | [§5.1 Owner-selected contract](#51-owner-selected-contract-and-residue-removal) |
| R2-14 | RUNID item 1 | APPLIED | [§3.1 Exact grammar and width](#31-exact-generator-grammar-and-width) |
| R2-15 | RUNID item 2 | APPLIED | [§3.2 Derive once](#32-derive-once-then-validate-every-component) |
| R2-16 | RUNID item 3 | APPLIED | [§3.3 Per-consumer equality](#33-per-consumer-equality-hard-gate) |
| R2-17 | RUNID item 4 | APPLIED | [§3.4 Acceptance/refusal transcript](#34-acceptance-and-refusal-transcript) |
| R2-18 | RUNID item 5 | APPLIED | [§4.7 Close-script/RUNID boundary](#47-close-script-contract-and-runid-boundary) |
| R2-19 | RUNID item 6 | APPLIED | [§3.5 Append-only ledger](#35-append-only-allocation-and-burn-ledger) |
| LB-01 | EXT-01 — `/` | INCLUDE as `read-exact` | [§10.1-E01](#sec101-e01) |
| LB-02 | EXT-02 — `/opt`, `/opt/mtc-bridge`, `/opt/mtc-bridge/releases`, `/opt/mtc-bridge/venvs` | INCLUDE as finite `read-exact` set | [§10.1-E02](#sec101-e02) |
| LB-03 | EXT-05 — `/usr`, `/usr/bin` | INCLUDE as finite `read-exact` set | [§10.1-E05](#sec101-e05) |
| LB-04 | EXT-06 — frozen RP6/RP7 executable objects | INCLUDE as finite `read-execute-exact` set, conditional on FAM-01 closure | [§10.1-E06](#sec101-e06) |
| LB-05 | EXT-08 — `/etc` | INCLUDE as `read-exact` | [§10.1-E08](#sec101-e08) |
| LB-06 | EXT-10 — `/var`, `/var/lib`, `/var/log` | INCLUDE as finite `read-exact` set | [§10.1-E10](#sec101-e10) |
| LB-07 | EXT-13 — `/proc/uptime` | INCLUDE as `read-exact` | [§10.1-E13](#sec101-e13) |
| LB-08 | EXT-14 — `/proc/self/mountinfo` | INCLUDE as `read-exact` | [§10.1-E14](#sec101-e14) |
| LB-09 | EXT-15 — `/proc/self/ns/{user,mnt,pid,net}` | INCLUDE as finite `read-exact` set | [§10.1-E15](#sec101-e15) |
| LB-10 | EXT-16 — exact `/proc/<WPI_MAINPID>/ns/net` | INCLUDE as `read-exact`; freeze to the preregistered PID | [§10.1-E16](#sec101-e16) |
| LB-11 | EXT-17 — `/proc/self/fd/8` | INCLUDE as `read-exact` | [§10.1-E17](#sec101-e17) |
| LB-12 | FAM-01 — RP6 inherited-PATH/optional-pin executable family | `PROPOSED — LEAD/OWNER DECISION REQUIRED`: close to twelve exact pins and delete fallback | [Decision F1](#decision-f1); [MERGE-CONFLICT MC-01](#454-merge-conflict-register--no-adjudication) |
| LB-13 | FAM-02 — RP6 arbitrary-prefix venv-root family | `PROPOSED — LEAD/OWNER DECISION REQUIRED`: bind the one exact per-candidate venv root | [Decision F2](#decision-f2); [MERGE-CONFLICT MC-02](#454-merge-conflict-register--no-adjudication) |
| LB-14 | FAM-03 — evidence-root provenance | `PROPOSED — LEAD/OWNER DECISION REQUIRED`: require a complete frozen-composite derivation | [Decision F3](#decision-f3); [MERGE-CONFLICT MC-03](#454-merge-conflict-register--no-adjudication) |
| LB-15 | ORDER-01 — circular attestation/preregistration/commit order | INCLUDE the two-commit capture-then-consume procedure | [§5.2 Ordering fix](#52-attestation-ordering-fix--two-commits-capture-first-and-consume-second) |

Conservation equation: `34 admitted = 19 R2 members + 15 Lane-B members`; terminal dispositions = 34; omitted/overwritten members = 0.

## 9. SELF-QA

This SELF-QA is a manual text-conservation check only. It did not execute any block, wrapper, generator, predicate, transport, host command, network action, attestation, archive build, or Git mutation.

### 9.1 Both semantic placeholders resolved — seam lines

R2 contained three literal Lane-B sites representing two semantic insertions: the section-10.1/access-grammar insertion and the attestation-ordering insertion repeated at sections 4.10 and 5.2. All three sites are resolved.

**Section-10.1/access-grammar opening seam:**

> A block-only result is supplemental. The current prover's lower-bound output cannot satisfy this gate until its findings are repaired with exact composite RED/GREEN commands and real output and a fresh T1 review accepts the analyzer on the final proof semantics.  
> ### 4.5 Section 10.1 application and access grammar

**Section-10.1/access-grammar closing seam:**

> 3. **MERGE-CONFLICT MC-03 — evidence-root provenance.** R2 section 4.4 already makes the complete frozen composite proof the acceptance route and classifies block-only results as supplemental, while Lane-B Decision F3 keeps that route `PROPOSED — LEAD/OWNER DECISION REQUIRED`. This draft makes no decision; Lead/owner resolution is required before freeze.  
> ### 4.6 Section 8.2 rows 1–9 coverage gate

**Section-4.10 attestation-order cross-reference seam:**

> Stage 1 fills the six member identities into the extractor, records archive bytes and SHA-256, re-hashes all blocks/wrappers/transport files, proves the extracted identities equal the manifest, and adds the completed successor plus its checksum set. Any hidden or extra member is STOP.  
> ### 4.10 Final merge and pre-operation commit  
> The two-commit attestation ordering procedure in section 5.2 is mandatory and contains no exception for an already-open root session. Its mechanical order-violation check must pass before the final successor becomes dispatchable.

**Section-5.2 attestation-ordering opening seam:**

> No obsolete option branch, unresolved-status label, or standalone residue from the skeleton is part of this draft.  
> ### 5.2 Attestation ordering fix — two commits, capture first and consume second

**Section-5.2 attestation-ordering closing seam:**

> **The procedure that produces an observation is committed before the observation; the value of that observation is committed before any operation consumes it. No commit both authorizes an attestation observation and claims that its not-yet-observed value was already frozen.**  
> ## 6. Transport operations and observed-outcome semantics

### 9.2 R2 review-item conservation — 19/19

#### Skeleton review, 13 items

1. **Gap 1 — exhaustive fill manifest.**
   > Stage 1 maintains one per-consumer fill manifest and proves every entry is populated before any operation.
2. **Gap 2 — targeted fills.**
   > The freeze tool accepts an allowlist of exact `(file, constant-or-table-field)` edit sites and refuses a file-wide or repository-wide marker replacement.
3. **Gap 3 — attestation order, Lane-B text merged.**
   > The following two-commit sequence is mandatory and contains no exception for an already-open root session.
4. **Gap 4 — complete compositions.**
   > The Stage-1 proof unit is each complete frozen same-shell composition: `run_p0.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP6-P0.sh`, and `run_ro.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP7-WPI-RO.sh`, with the concrete allocation and freeze manifest applied; the RO graph also includes every executed inline program and the exact executed `verify_lock.py` source.
5. **Gap 5 — section 10.1 extensions, Lane-B text merged.**
   > The admitted Lane-B application universe is exactly 15 members: 11 `EXTEND` items, 3 unresolved families, and 1 ordering fix.
6. **Gap 6 — access grammar, Lane-B text merged.**
   > A path match without a matching access qualifier is not admission.
7. **Gap 7 — repairs precede acceptance.**
   > Before the final T0 pair reviews the artifacts: remove every RP6/RP7 write-open of `/dev/null`; require the exact 12-entry `P0_TOOL_PINS` map with no PATH fallback and shared pins equal to RP7; and require `P0_VENV_ROOT` to equal `/opt/mtc-bridge/venvs/$P0_CAND` exactly.
8. **Gap 8 — rows 1–9 coverage without redesign.**
   > Owner decision: all nine existing section-8.2 rows are bound into `RP7-WPI-RO.sh` only after the currently reviewed RP7 bytes receive their dual flagship acceptance; this merged draft does not restate or redesign those rows.
9. **Gap 9 — P0 environment reconciliation.**
   > Before freeze, either RP6 is repaired so every evidence-producing child satisfies the cleared-environment, fixed trusted cwd, run-owned TMPDIR, pinned-target-chain, and isolated-Python contract and the changed bytes are re-audited, or the successor is narrowed to the exact mixed environment the final RP6 bytes prove and that weaker claim receives explicit acceptance.
10. **Gap 10 — current transport semantics.**
    > The successor reproduces the exact current `TRANSPORT_PLAN.tsv` ops 01–12 and the current runner's first-mismatch semantics: after the first mismatching or not-evaluable `sequence_ok` operation, later `sequence_ok` operations are skipped and all `always` operations still run; results are classified by operation kind and provenance, not by rc alone; ssh rc 255, every nonzero scp rc, an rc outside a kind's grammar, or an ssh rc without a remote-program marker is not-evaluable; and an `always` failure caused by an earlier broken sequence **on its own branch** is not-evaluable rather than a new host FAIL, with the first applicable reason recorded — a nonzero scp reports `scp_transfer_did_not_complete` and an rc 3 reports `operation_reported_stop` whatever its prerequisites, and only an rc-1 `always` failure reaches prerequisite adjudication and names which case it is (`cleanup_after_unestablished_prerequisite` or `cleanup_after_earlier_deviation`); every `always` operation emits `TR_OP_PREREQ_STATE` with each edge's resolved class regardless. Cleanup prerequisites are modelled per branch and per operation (07<-04, 08<-05, 09<-07, 10<-08, 11<-07+09, 12<-08+10), so an unrelated branch's failure never demotes a genuine marked rc 1 to not-evaluable; and an `ssh_stdin` operation's provenance marker must come from the family belonging to the stdin artifact that row sends, not from a global union of every program's prefixes.
11. **Gap 11 — close-script contract.**
    > Freeze is blocked until the actual `remote_close_tree_wpi.sh`, plan rows 07/08, derivation contract, launch-domain claim, scratch-location semantics, and RED/GREEN evidence describe one byte-identical executable contract and the script reaches its RUNID/`EV_DIR` validation rather than failing earlier on argv shape.
12. **Gap 12 — no inert pin.**
    > `WPI_INTERPRETER_TARGET` must be absent from the final wrapper and fill ledger unless an accepted block gives it an explicit predicate and production consumer; a filled but unread value is not a preregistered check.
13. **Gap 13 — unresolved residue removed.**
    > No obsolete option branch, unresolved-status label, or standalone residue from the skeleton is part of this draft.

#### RUNID minting review, 6 items

1. **Item 1 — exact grammar, generator, width.**
   > The Stage-1 generator grammar is exact: `UTCSTAMP := [0-9]{8}T[0-9]{6}` (15 ASCII bytes), `NONCE := [0-9a-f]{8}` (8 ASCII bytes), and `BASE := WPI-<UTCSTAMP>Z-<NONCE>` (29 ASCII bytes).
2. **Item 2 — derive once and validate before writes.**
   > From the one generated base, Stage 1 derives—never independently types—`<base>-P0`, `<base>-RO`, `p0`, `ro`, `wpi_staging_<base>`, `<base>-EXECUTE`, and `WPI_TRANSPORT_<base>` before any consumer is written.
3. **Item 3 — consumer equality including the runner boundary.**
   > This conservation proof is a pre-commit hard gate and is the selected protection for the Windows runner's early `$RECORD_ROOT` creation; no new local component validator is claimed, and the runner may not execute until the proof passes on its final bytes.
4. **Item 4 — literal acceptance/refusal evidence.**
   > The finite negative cases are called **refusal representatives**, never “the refusal set,” and are executed as follows against the exact pinned function:
5. **Item 5 — close argv reconciliation.**
   > If derivation classes 5 and 6 remain preregistered, the accepted script must implement the cleared launch domain and run-owned scratch semantics and the plan must pass the required `WORK_ROOT`; if final accepted bytes retain a two-argument inherited-TMPDIR contract, the successor must delete those claims and surface the weaker contract for T0 adjudication. The cleared launch domain closes the inner child only; the outer SSH account-shell boundary (a server-supplied `BASH_ENV`/`ENV` acting before `env -i`) remains OPEN, and no successor text may present the cleared inner-child domain as an end-to-end F1 closure.
6. **Item 6 — durable global uniqueness.**
   > Stage 1 uses the committed append-only ledger `WPI_RUNID_ALLOCATION_BURN_LEDGER.md`; the candidate base and both derived RUNIDs must be absent from the complete ledger history and all retained operator/remote-root records before allocation can proceed.

### 9.3 Lane-B conservation — 15/15

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
| FAM-01 | “Require exactly one frozen pin for each of `stat` … `getent` … and delete every unpinned `command -v`/inherited-PATH fallback.” The decision remains `PROPOSED — LEAD/OWNER DECISION REQUIRED`. |
| FAM-02 | “Before the first path probe, require `P0_VENV_ROOT` to equal exactly `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b`.” The decision remains `PROPOSED — LEAD/OWNER DECISION REQUIRED`. |
| FAM-03 | “Make the entrypoint-driven section-4.4 composite proof the only acceptance route.” The decision remains `PROPOSED — LEAD/OWNER DECISION REQUIRED`. |
| ORDER-01 | “The procedure that produces an observation is committed before the observation; the value of that observation is committed before any operation consumes it.” |

Disposition recount: 11 extension lines present; 3 proposed-family lines present and each marked `PROPOSED — LEAD/OWNER DECISION REQUIRED`; 1 ordering line present; total 15/15.

### 9.4 Two-commit sequence walk

1. Before Commit 1, the attestation values do not exist and no text needs them: Commit 1 contains only the fully specified capture procedure, concrete identifiers/authority, and explicit non-consumable placeholders.
2. Commit 1 exists before capture. The recorder derives Commit 1's object ID from a clean current `HEAD`; the capture needs only that committed procedure and derived ID, not any value that it is about to observe.
3. The capture returns and is closed. Only now do the four namespace identities, root-mount identity, allocation-parent mount identity, projection-v2 digest, and evidence-record digest/bytes exist.
4. Commit 2 consumes exactly those now-existing values, freezes the final artifacts and successor, and records both the Commit-1 and evidence identities. It does not require a future host result.
5. Op 01 begins only after Commit 2. Its preflight derives the already-existing Commit-2 ID from a clean current `HEAD` and uses the already-frozen values; no value is learned and retroactively preregistered, and no commit embeds its own ID.

Therefore no value is needed before it exists: Commit 1 needs zero attestation outcomes; the attestation needs only Commit 1; Commit 2 needs the completed attestation; and the WP-I run needs Commit 2.

### 9.5 Final conservation and conflict result

- Semantic placeholders resolved: 2/2; literal placeholder sites resolved: 3/3.
- R2 disposition conservation: 19/19.
- Lane-B member conservation: 15/15.
- Combined conservation: `19 + 15 = 34`; terminal dispositions: 34; silently dropped: 0.
- Proposed family decisions preserved without adjudication: FAM-01, FAM-02, FAM-03.
- MERGE-CONFLICT items: MC-01, MC-02, MC-03. None was resolved by the author.
