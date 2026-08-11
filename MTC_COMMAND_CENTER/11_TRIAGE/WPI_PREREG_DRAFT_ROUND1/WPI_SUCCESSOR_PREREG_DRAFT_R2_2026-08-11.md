# WP-I SUCCESSOR PREREGISTRATION — DRAFT ROUND 2, LANE A

Date: 2026-08-11  
Authoring surface: T2 preregistration text only  
Base: `WPI_SUCCESSOR_PREREG_SKELETON_2026-08-10.md`  
Applied work-lists: `SKELETON_REVIEW_CODEX_2026-08-10.md` and `RUNID_MINTING_REVIEW_CODEX_2026-08-11.md`

This is a successor **draft**, not a dispatch record. It mints no identifier, fills no attestation, runs no block, contacts no host, and authorizes no operation. Every allocation remains `<ALLOCATE-AT-DISPATCH>` and every not-yet-accepted identity remains `<PIN-AT-FREEZE>`.

The accepted content of `WPI_PREREGISTRATION_DRAFT.md` remains the baseline except where this document explicitly supersedes it. The final successor must also merge the accepted Lane-B application for section 10.1 and attestation ordering; until that merge, this draft is not complete and freeze must STOP.

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

The new ledger entry must be committed in the pre-operation sequence selected by the accepted Lane-B ordering text. Evidence retention and checks against only two historical roots are supplemental; neither is a global uniqueness proof.

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

All section-1 values, every section-2 manifest member, every section-3 allocation consumer, block/wrapper/transport hashes, archive constants, and the accepted Lane-B attestation outputs are populated and conservation-checked. An unfilled, inert, duplicated, or unequal consumer is freeze STOP.

### 4.4 Composite path-scope proof

The Stage-1 proof unit is each complete frozen same-shell composition: `run_p0.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP6-P0.sh`, and `run_ro.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP7-WPI-RO.sh`, with the concrete allocation and freeze manifest applied; the RO graph also includes every executed inline program and the exact executed `verify_lock.py` source.

The accepted analyzer follows sourced values and registered production-call contracts; derives `RUNID`, `EV_STAGE_ID`, `EV_DIR`, and `EV_LOG` from the exact frozen `REMOTE_BASE`; enumerates every reachable path-bearing argument, redirection, test, executable object, endpoint, nested source, and closed runtime family; and assigns every admitted member exactly one terminal disposition.

Unknown commands, unconsumed options, unresolved/dynamic construction, unbound source edges, startup-source ambiguity, opaque sinks, unclosed runtime families, component hash mismatches, missing values, or conservation mismatches are rc 3 and prevent freeze. Zero resolved facts plus PASS is forbidden.

A block-only result is supplemental. The current prover's lower-bound output cannot satisfy this gate until its findings are repaired with exact composite RED/GREEN commands and real output and a fresh T1 review accepts the analyzer on the final proof semantics.

### 4.5 LANE-B placeholder — section 10.1 and access grammar

**LANE-B: INSERT THE ACCEPTED FINAL SECTION-10.1 APPLICATION HERE, INCLUDING ALL 11 EXTEND ITEMS, THE THREE EXPLICITLY DECIDED FAMILIES, THEIR JUSTIFICATIONS/FALSIFICATIONS, AND THE DEFAULT-DENY MULTI-CAPABILITY ACCESS GRAMMAR; LANE A MAKES NONE OF THOSE THREE FAMILY DECISIONS.**

Until that text is merged, no section-10.1 rule, access qualifier, or family is final, and the section-10.2 allowlist comparison must STOP.

No wildcard or arbitrary-prefix substitute may be inferred from this placeholder.

### 4.6 Section 8.2 rows 1–9 coverage gate

Owner decision: all nine existing section-8.2 rows are bound into `RP7-WPI-RO.sh` only after the currently reviewed RP7 bytes receive their dual flagship acceptance; this Lane-A draft does not restate or redesign those rows.

Operations 04 and 05 currently do not establish rows 1–9, and P0's `Manager.Version` readiness query is a premise only, not evidence for any B2/B4 row. Freeze remains blocked until the post-acceptance RP7 extension executes all nine in the already-preregistered first-divergence order, the plan invokes the accepted final bytes, and the changed artifact receives the required final-byte T0 acceptances.

### 4.7 Close-script contract and RUNID boundary

Freeze is blocked until the actual `remote_close_tree_wpi.sh`, plan rows 07/08, derivation contract, launch-domain claim, scratch-location semantics, and RED/GREEN evidence describe one byte-identical executable contract and the script reaches its RUNID/`EV_DIR` validation rather than failing earlier on argv shape.

If derivation classes 5 and 6 remain preregistered, the accepted script must implement the cleared launch domain and run-owned scratch semantics and the plan must pass the required `WORK_ROOT`; if final accepted bytes retain a two-argument inherited-TMPDIR contract, the successor must delete those claims and surface the weaker contract for T0 adjudication.

Hash agreement with a report whose prose or plan argv describes different behavior is not closure evidence. Ops 07 and 08 remain separate close invocations; no retrieval or local bind substitutes for this boundary.

### 4.8 P0 environment gate

Apply section 2.4 before artifact acceptance. The final successor's environment claim must be mechanically equal to what final RP6 production call paths establish; a stronger inherited sentence is prohibited.

### 4.9 Deterministic runkit and final identities

The deterministic `runkit.tar` member set is exactly `RP0-LIB.sh`, `RP0-BOOTSTRAP.sh`, `RP6-P0.sh`, `RP7-WPI-RO.sh`, `run_p0.sh`, and `run_ro.sh`; `RP1-B3.sh` is excluded.

Stage 1 fills the six member identities into the extractor, records archive bytes and SHA-256, re-hashes all blocks/wrappers/transport files, proves the extracted identities equal the manifest, and adds the completed successor plus its checksum set. Any hidden or extra member is STOP.

### 4.10 Final merge and pre-operation commit

**LANE-B: INSERT THE ACCEPTED TWO-COMMIT ATTESTATION ORDERING PROCEDURE AND ITS ORDER-VIOLATION CHECK HERE; LANE A DOES NOT CHOOSE OR RESTATE THAT SEQUENCE.**

The merged final successor must contain no unresolved Lane-B placeholder and must itself be committed with the final checksum set before op 01, any block/wrapper/transport process, or any host-side allocation begins.

## 5. External attestation scope

### 5.1 Owner-selected contract and residue removal

The owner-selected contract is option (a): the projection-v2 digest and row-8 namespace/root-mount identities are produced outside the ssh login domain they attest, through the separately preregistered read-only root command set covered by grant #6.

`WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`, both trusted-Python pins, the five row-8 execution-domain identities, and `EXPECT_PARENT_MOUNT` are produced only by the committed grant-#6 attestation procedure completed by the accepted Lane-B section 5.2 text.

The login session may not learn and re-pin its own namespace or mount identity. Equality with a PID visible from inside that login domain, including visible PID 1, is not a substitute for external attestation. If the external attestation is unavailable, malformed, incomplete, or unequal, P0 STOPs and no RO row runs.

No obsolete option branch, unresolved-status label, or standalone residue from the skeleton is part of this draft.

### 5.2 LANE-B placeholder — attestation ordering

**LANE-B: INSERT THE ACCEPTED ATTESTATION ORDERING APPLICATION HERE, INCLUDING COMMIT 1 CONTENTS, THE SINGLE ROOT ACQUISITION, VALUES THAT ONLY THEN BECOME COMPUTABLE, COMMIT 2 CONTENTS, AND THE MECHANICAL ORDER-VIOLATION CHECK.**

Until that text is merged and its invariant is satisfied, the attestation inputs in sections 2.1 and 4.3 remain uncomputable freeze inputs and the successor cannot become dispatchable.

## 6. Transport operations and observed-outcome semantics

The successor reproduces the exact current `TRANSPORT_PLAN.tsv` ops 01–12 and the current runner's first-mismatch semantics: after the first mismatching or not-evaluable `sequence_ok` operation, later `sequence_ok` operations are skipped and all `always` operations still run; results are classified by operation kind and provenance, not by rc alone; ssh rc 255, every nonzero scp rc, an rc outside a kind's grammar, or an ssh rc without a remote-program marker is not-evaluable; and an `always` failure caused by an earlier broken sequence is not-evaluable rather than a new host FAIL.

Ops 07/08 close via `remote_close_tree_wpi.sh`, ops 09/10 retrieve, ops 11/12 bind locally, and op 06 is the operator-side row-24 host contact. The runner's `-Execute` and `-Confirm` switches are technical interlocks, not authority.

## 7. Post-run sequence

After the preregistered operations complete: retrieve P0/RO evidence under ops 09/10; bind each digest set locally under ops 11/12; produce the WP-I closure record and unit/hour ledger; dispatch Audit 2 with the resolved supplemental-review flag; and later run the separately authorized `RPD-VERIFY` root-side procedure to close its deferred checks. None of those later steps repairs a failed freeze gate or retroactively validates a reused identifier.

## 8. Review-item disposition table

| Item | Disposition | Section anchor / reason |
|---|---|---|
| Skeleton Gap 1 | APPLIED | [§2.1 Exhaustive fill manifest](#21-exhaustive-fill-manifest) |
| Skeleton Gap 2 | APPLIED | [§2.2 Targeted fills only](#22-targeted-fills-only) |
| Skeleton Gap 3 | DEFERRED | [§5.2 Lane-B attestation ordering placeholder](#52-lane-b-placeholder--attestation-ordering); the kickoff assigns the two-commit order to Lane B |
| Skeleton Gap 4 | APPLIED | [§4.4 Composite path-scope proof](#44-composite-path-scope-proof) |
| Skeleton Gap 5 | DEFERRED | [§4.5 Lane-B section-10.1 placeholder](#45-lane-b-placeholder--section-101-and-access-grammar); Lane B owns the 11 extensions and three family decisions |
| Skeleton Gap 6 | DEFERRED | [§4.5 Lane-B section-10.1 placeholder](#45-lane-b-placeholder--section-101-and-access-grammar); Lane B owns the final access grammar |
| Skeleton Gap 7 | APPLIED | [§4.2 Pre-acceptance path repairs](#42-pre-acceptance-path-repairs) |
| Skeleton Gap 8 | APPLIED | [§4.6 Rows 1–9 coverage gate](#46-section-82-rows-19-coverage-gate) without redesigning the rows |
| Skeleton Gap 9 | APPLIED | [§2.4 P0 environment reconciliation](#24-p0-environment-reconciliation) and [§4.8](#48-p0-environment-gate) |
| Skeleton Gap 10 | APPLIED | [§6 Transport operations](#6-transport-operations-and-observed-outcome-semantics) |
| Skeleton Gap 11 | APPLIED | [§4.7 Close-script contract](#47-close-script-contract-and-runid-boundary) |
| Skeleton Gap 12 | APPLIED | [§2.3 No inert pins](#23-no-inert-pins) |
| Skeleton Gap 13 | APPLIED | [§5.1 Owner-selected contract](#51-owner-selected-contract-and-residue-removal) |
| RUNID item 1 | APPLIED | [§3.1 Exact grammar and width](#31-exact-generator-grammar-and-width) |
| RUNID item 2 | APPLIED | [§3.2 Derive once](#32-derive-once-then-validate-every-component) |
| RUNID item 3 | APPLIED | [§3.3 Per-consumer equality](#33-per-consumer-equality-hard-gate) |
| RUNID item 4 | APPLIED | [§3.4 Acceptance/refusal transcript](#34-acceptance-and-refusal-transcript) |
| RUNID item 5 | APPLIED | [§4.7 Close-script/RUNID boundary](#47-close-script-contract-and-runid-boundary) |
| RUNID item 6 | APPLIED | [§3.5 Append-only ledger](#35-append-only-allocation-and-burn-ledger) |

## 9. SELF-QA — one satisfying line per review item

This SELF-QA is a text-conservation check only. It did not execute any block, wrapper, generator, predicate, transport, host command, or network action.

### Skeleton review, 13 items

1. **Gap 1 — exhaustive fill manifest.**
   > Stage 1 maintains one per-consumer fill manifest and proves every entry is populated before any operation.
2. **Gap 2 — targeted fills.**
   > The freeze tool accepts an allowlist of exact `(file, constant-or-table-field)` edit sites and refuses a file-wide or repository-wide marker replacement.
3. **Gap 3 — attestation order, deferred to Lane B.**
   > **LANE-B: INSERT THE ACCEPTED ATTESTATION ORDERING APPLICATION HERE, INCLUDING COMMIT 1 CONTENTS, THE SINGLE ROOT ACQUISITION, VALUES THAT ONLY THEN BECOME COMPUTABLE, COMMIT 2 CONTENTS, AND THE MECHANICAL ORDER-VIOLATION CHECK.**
4. **Gap 4 — complete compositions.**
   > The Stage-1 proof unit is each complete frozen same-shell composition: `run_p0.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP6-P0.sh`, and `run_ro.sh + RP0-LIB.sh + RP0-BOOTSTRAP.sh + RP7-WPI-RO.sh`, with the concrete allocation and freeze manifest applied; the RO graph also includes every executed inline program and the exact executed `verify_lock.py` source.
5. **Gap 5 — section 10.1 extensions, deferred to Lane B.**
   > **LANE-B: INSERT THE ACCEPTED FINAL SECTION-10.1 APPLICATION HERE, INCLUDING ALL 11 EXTEND ITEMS, THE THREE EXPLICITLY DECIDED FAMILIES, THEIR JUSTIFICATIONS/FALSIFICATIONS, AND THE DEFAULT-DENY MULTI-CAPABILITY ACCESS GRAMMAR; LANE A MAKES NONE OF THOSE THREE FAMILY DECISIONS.**
6. **Gap 6 — access grammar, deferred to Lane B.**
   > Until that text is merged, no section-10.1 rule, access qualifier, or family is final, and the section-10.2 allowlist comparison must STOP.
7. **Gap 7 — repairs precede acceptance.**
   > Before the final T0 pair reviews the artifacts: remove every RP6/RP7 write-open of `/dev/null`; require the exact 12-entry `P0_TOOL_PINS` map with no PATH fallback and shared pins equal to RP7; and require `P0_VENV_ROOT` to equal `/opt/mtc-bridge/venvs/$P0_CAND` exactly.
8. **Gap 8 — rows 1–9 coverage without redesign.**
   > Owner decision: all nine existing section-8.2 rows are bound into `RP7-WPI-RO.sh` only after the currently reviewed RP7 bytes receive their dual flagship acceptance; this Lane-A draft does not restate or redesign those rows.
9. **Gap 9 — P0 environment reconciliation.**
   > Before freeze, either RP6 is repaired so every evidence-producing child satisfies the cleared-environment, fixed trusted cwd, run-owned TMPDIR, pinned-target-chain, and isolated-Python contract and the changed bytes are re-audited, or the successor is narrowed to the exact mixed environment the final RP6 bytes prove and that weaker claim receives explicit acceptance.
10. **Gap 10 — current transport semantics.**
    > The successor reproduces the exact current `TRANSPORT_PLAN.tsv` ops 01–12 and the current runner's first-mismatch semantics: after the first mismatching or not-evaluable `sequence_ok` operation, later `sequence_ok` operations are skipped and all `always` operations still run; results are classified by operation kind and provenance, not by rc alone; ssh rc 255, every nonzero scp rc, an rc outside a kind's grammar, or an ssh rc without a remote-program marker is not-evaluable; and an `always` failure caused by an earlier broken sequence is not-evaluable rather than a new host FAIL.
11. **Gap 11 — close-script contract.**
    > Freeze is blocked until the actual `remote_close_tree_wpi.sh`, plan rows 07/08, derivation contract, launch-domain claim, scratch-location semantics, and RED/GREEN evidence describe one byte-identical executable contract and the script reaches its RUNID/`EV_DIR` validation rather than failing earlier on argv shape.
12. **Gap 12 — no inert pin.**
    > `WPI_INTERPRETER_TARGET` must be absent from the final wrapper and fill ledger unless an accepted block gives it an explicit predicate and production consumer; a filled but unread value is not a preregistered check.
13. **Gap 13 — unresolved residue removed.**
    > No obsolete option branch, unresolved-status label, or standalone residue from the skeleton is part of this draft.

### RUNID minting review, 6 items

1. **Item 1 — exact grammar, generator, width.**
   > The Stage-1 generator grammar is exact: `UTCSTAMP := [0-9]{8}T[0-9]{6}` (15 ASCII bytes), `NONCE := [0-9a-f]{8}` (8 ASCII bytes), and `BASE := WPI-<UTCSTAMP>Z-<NONCE>` (29 ASCII bytes).
2. **Item 2 — derive once and validate before writes.**
   > From the one generated base, Stage 1 derives—never independently types—`<base>-P0`, `<base>-RO`, `p0`, `ro`, `wpi_staging_<base>`, `<base>-EXECUTE`, and `WPI_TRANSPORT_<base>` before any consumer is written.
3. **Item 3 — consumer equality including the runner boundary.**
   > This conservation proof is a pre-commit hard gate and is the selected protection for the Windows runner's early `$RECORD_ROOT` creation; no new local component validator is claimed, and the runner may not execute until the proof passes on its final bytes.
4. **Item 4 — literal acceptance/refusal evidence.**
   > The finite negative cases are called **refusal representatives**, never “the refusal set,” and are executed as follows against the exact pinned function:
5. **Item 5 — close argv reconciliation.**
   > If derivation classes 5 and 6 remain preregistered, the accepted script must implement the cleared launch domain and run-owned scratch semantics and the plan must pass the required `WORK_ROOT`; if final accepted bytes retain a two-argument inherited-TMPDIR contract, the successor must delete those claims and surface the weaker contract for T0 adjudication.
6. **Item 6 — durable global uniqueness.**
   > Stage 1 uses the committed append-only ledger `WPI_RUNID_ALLOCATION_BURN_LEDGER.md`; the candidate base and both derived RUNIDs must be absent from the complete ledger history and all retained operator/remote-root records before allocation can proceed.
