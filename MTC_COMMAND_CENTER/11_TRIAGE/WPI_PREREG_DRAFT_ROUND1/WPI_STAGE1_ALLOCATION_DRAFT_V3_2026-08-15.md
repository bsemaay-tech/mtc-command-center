Status: ALLOCATION RECORD V3 - SUPERSEDES V2 - NOT COMMITTED

| Prior finding | V3 disposition | Concrete world in which the check must go RED | Auditor reproduction and required RED signal |
|---|---|---|---|
| 1. Required allocation fields/results were not populated | **NOT CLOSED** | The candidate payload is missing one required field, contains a null/placeholder value, or lacks the literal command, stdout, stderr, or result bound to that field. This V3 has no minted `BASE`, RUNIDs, roots, ledger row, or execution transcript, so that is the present world. | Run the real record gate on the exact candidate bytes. Remove `P0_RUNID` from a known-good fixture, then replace `COLLISION_RESULT` with an unresolved value. Each mutation must produce `POPULATION_STOP` and make the record non-spendable. A validator, known-good fixture, and transcript do not yet exist, so closure remains unproved. |
| 2. Exact reason-token/stream grammar was bypassable | **NOT CLOSED — replacement contract specified; execution evidence absent** | The selected stream is the expected newline-terminated byte string except that one NUL is inserted inside `component_ok`, or one NUL is appended after the final LF. V2 accepted both states even though the byte stream was different. | Invoke the actual V3 stream checker, not a reimplementation, on the exact expected bytes, the embedded-NUL mutation, and the trailing-NUL mutation. Exact bytes must pass; both mutations must produce `STREAM_GRAMMAR_STOP`. The V2 auditor already reproduced false acceptance for both mutations. V3 has no executable checker or GREEN/RED transcript, so it does not claim closure. |
| 3. Collision check quantified over an unproved universe | **NOT CLOSED — independent authority is UNKNOWN** | An independently authoritative retained-root census contains `R1`, `R2`, and `R3`; the selected operator archive contains only `R1` and `R2`; a manifest generated from that incomplete archive declares only `R1` and `R2` and hashes consistently. The claimed complete universe is false. | Keep the authority census unchanged, remove `R3` from a known-good archive fixture, regenerate every archive-derived manifest/hash, and run the real gate. It must compare the independent census with observed archive membership and produce `COLLISION_UNIVERSE_STOP missing=R3` before minting. If it passes because the manifest also omitted `R3`, the gate is decorative. No source establishes the real independent census or remote-allocation authority, so this V3 does not ship a no-collision claim. |
| 4. Append-only was asserted rather than enforced | **NOT CLOSED — verifier and durable failure recovery are UNKNOWN** | Let immutable parent blob bytes be `P`. Create candidate `C` by changing one byte inside `P` and then appending an otherwise valid next row. The new row and chain labels look correct, but history was rewritten. | Feed the actual verifier `P` from the parent Git object and `C` as the candidate. It must produce `LEDGER_APPEND_STOP prefix_mismatch` before commit. Repeat with parent truncation, duplicate row ref, skipped sequence, wrong predecessor, and an extra suffix byte. Then force an append/commit failure and prove the canonical parent remains intact while the same identities become durably `BURNED` on a preregistered independent recovery surface. That executable verifier, canonical path, recovery surface, and RED/GREEN evidence do not yet exist. |
| 5. The checked predicate object was not bound to the object later sourced | **NOT CLOSED — real caller and transcript are UNKNOWN** | File `A` has the required 18,968 bytes and fixed SHA-256. File `B` has different bytes, exports the same function name, emits acceptance, and writes a marker. The caller verifies `A` but launches Bash with `B` as the source argument. | Drive the real top-level caller through its launch seam so the verified handle/path is `A` and the actual child argument/open target is `B`. The run must produce `PREDICATE_BINDING_STOP` before a grammar PASS; the marker must not be accepted as predicate evidence. A helper-only comparison is invalid. V3 contains no actual caller or transcript tying one concrete object identity to both operations, so it does not claim closure. |

The five findings remain open. V2's review reached the same result: population and exact stream grammar were not closed, while append-only and predicate binding existed only as designs without executable evidence (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:5-13`). This record is therefore a fail-closed allocation specification, not a spendable allocation, acceptance, authorization, or host instruction.

## 1. Governing falsifiability rule

A check is real only if the expected value is independent of the object being checked, its quantified universe is bounded by an independently authoritative source, and a mechanism rejects a constructed deviant state. A check that can fail only because of a typo is decorative (`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`). Review must try to make the check pass while its claimed property is false and must invoke the check under review rather than reimplement its logic (`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:73-81`).

Every V3 gate below therefore records five things:

1. the exact claim;
2. the independently sourced expectation;
3. the material outside the quantified universe;
4. the concrete RED world;
5. the command, streams, result, and object identities needed to reproduce RED and GREEN.

Until all five exist for the actual executable gate, the corresponding closure state is `NOT CLOSED`.

## 2. Facts established now

| Field or authority | V3 value | Basis |
|---|---|---|
| Audit classification | `T2` documentation/evidence artifact | The V2 review classified this allocation review as T2 (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:1-3`). |
| Generator grammar | `UTCSTAMP=[0-9]{8}T[0-9]{6}`; `NONCE=[0-9a-f]{8}`; `BASE=WPI-<UTCSTAMP>Z-<NONCE>`; 15, 8, and 29 ASCII bytes respectively | Fixed by the successor (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:76-94`). |
| P0 and RO stage IDs | `p0`, `ro` | Derived-component contract (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:96-106`). |
| Required predicate object | 18,968 bytes; SHA-256 `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` | Fixed by the successor (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-104`). |
| Required collision scope | Complete committed allocation-ledger history, every retained operator root, and retained remote allocation records; two historical roots alone are not a global proof | Successor collision contract and V1 review (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_REVIEW_2026-08-15.md:23-29`). |
| Live `UTCSTAMP`, `NONCE`, `BASE`, P0/RO RUNIDs, `REMOTE_BASE`, confirmation token, operator root | `UNKNOWN` | Neither review establishes live values; the earlier honest placeholders were blockers, not allocations (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_REVIEW_2026-08-15.md:41-45`). |
| Canonical ledger repo path and parent object | `UNKNOWN` | V2 still left the canonical path unresolved (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:56-69`). |
| Independent authoritative operator-root census | `UNKNOWN` | V2 derived its inventory from the archive being checked; the reviewer showed that the bundle can agree with itself while omitting a retained root (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:39-54`). |
| Independent authoritative remote-allocation snapshot and coverage-through marker | `UNKNOWN` | A self-authored completeness statement is not independent evidence (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:41-54`). |
| Exact Bash executable identity | `UNKNOWN` | V2 deferred the caller, Bash identity, and transcript rather than proving them (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:71-93`). |
| Executable append verifier and independent burn-recovery surface | `UNKNOWN` | V2 described validation but supplied neither a verifier nor a safe recovery location after append/commit failure (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:56-69`). |
| Allocation commit, allocation-record blob, and later child binding | `UNKNOWN` | V2's post-commit binding was self-referential or unspecified (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:95-100`). |

No live identifier may be generated while the independent collision authority and append/burn preflight remain `UNKNOWN`. No placeholder is tested as if it were concrete; the successor requires literal generation evidence and one-use handling (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:76-147`).

## 3. Required allocation payload

The eventual allocation payload must contain exactly one concrete value for every field below and bind each result to replayable evidence. This table records present fact, not a guessed future value.

| Required payload field | Current value |
|---|---|
| `UTCSTAMP` | `UNKNOWN` |
| `NONCE` | `UNKNOWN` |
| `BASE` / `BASE_RUN` | `UNKNOWN` |
| P0 `RUNID` | `UNKNOWN` |
| RO `RUNID` | `UNKNOWN` |
| P0 `EV_STAGE_ID` | `p0` |
| RO `EV_STAGE_ID` | `ro` |
| `REMOTE_BASE` and leaf | `UNKNOWN` |
| `CONFIRM_TOKEN` | `UNKNOWN` |
| `OPERATOR_RECORD_ROOT` and leaf | `UNKNOWN` |
| successor identity | `UNKNOWN` |
| canonical ledger repo path, parent commit, parent blob, bytes, SHA-256 | `UNKNOWN` |
| independent operator-census identity and provenance | `UNKNOWN` |
| independent remote-allocation authority/snapshot identity and provenance | `UNKNOWN` |
| predicate source path and verified object identity | `UNKNOWN` |
| exact Bash path, bytes, SHA-256, and provenance | `UNKNOWN` |
| exact grammar matrix command, stdout, stderr, result | `UNKNOWN` |
| exact collision gate command, full enumerated membership, stdout, stderr, result | `UNKNOWN` |
| exact append verifier command, parent/candidate identities, stdout, stderr, result | `UNKNOWN` |
| exact ledger row and disposition | `UNKNOWN` |
| real caller argv/open identity and pre/post object binding | `UNKNOWN` |
| later non-self-referential allocation-commit binding | `UNKNOWN` |

The original review required concrete identities, collision/grammar results, and an append-only disposition, not merely field names (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_REVIEW_2026-08-15.md:5-13`). A future candidate with any current `UNKNOWN` value is RED under Finding 1 and cannot be committed as spendable.

## 4. Failure demonstration F1 — population and evidence binding

### Claim

Every required field is concrete, derived once where required, and accompanied by the literal evidence that produced or checked it.

### Independent expectation

The required field set comes from the reconciliation/successor contract, not from whichever fields happen to be present in the candidate. The V1 review enumerated the missing identities and result classes and rejected placeholders (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_REVIEW_2026-08-15.md:5-13`).

### RED world and reproduction

Start from a fully populated known-good fixture accepted by the real gate. Apply these mutations separately:

1. delete the `P0_RUNID` key;
2. set `COLLISION_RESULT` to an unresolved value;
3. keep `BASE` but delete its generator stderr/result binding;
4. add a second independently typed `RO_RUNID` consumer with a different value.

Invoke the real record gate on the exact mutated bytes. Each case must produce `POPULATION_STOP`, identify the missing/unresolved/duplicate field, and prevent any allocation, ledger reservation, consumer fill, commit, or host step. The gate must enumerate against a fixed schema; deriving its expected field list from the candidate would repeat the self-confirming defect.

### Present evidence state

There is no executable record gate, known-good populated fixture, or mutation transcript in V3. Numeric result-code semantics are `UNKNOWN`. Finding 1 is not closed.

## 5. Failure demonstration F2 — byte-exact reason stream

### Claim

The selected predicate stream equals one independently constructed expected byte sequence exactly: same length, same byte at every offset, exactly one final LF, and no other byte. The other stream is zero bytes.

The expected reason tokens and refusal representatives come from the successor, not from observed output (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:116-135`). A shell variable or line reader may not be the comparison domain because V2's Bash reader discarded NUL bytes and falsely accepted two deviant streams (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:21-37`).

### RED world and reproduction

For one accepted concrete case, let `E` be the exact ASCII expected line plus LF. Drive the actual V3 checker with these byte arrays:

1. GREEN control: `E`;
2. RED-1: `E` with byte `00` inserted inside the bytes for `component_ok`;
3. RED-2: `E || 00`;
4. RED-3: `E` without its final LF;
5. RED-4: `E || E`;
6. RED-5: exact expected stdout plus one byte on stderr.

The control must pass. Every mutation must produce `STREAM_GRAMMAR_STOP`. The auditor must call the production checker and preserve the input length and hex, command, stdout, stderr, and result. A separate comparison script is supplemental only; the defect pattern specifically rejects a proof that reimplements rather than invokes the check under audit (`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:25-28`).

### Present evidence state

V2 already supplies RED evidence against the old reader: embedded and trailing NUL both returned rc 0 (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:25-35`). No replacement executable or GREEN/RED evidence exists in V3. Finding 2 is not closed.

## 6. Failure demonstration F3 — collision-universe completeness

### Claim boundary

No global or host-wide uniqueness claim is made by V3. The strongest permissible future claim is: no candidate byte sequence occurs in every member of a separately established, independently authoritative, parent-bound collision universe, and every authority member reached exactly one terminal scan disposition.

The expected member set must not be generated from the archive or snapshot being checked. Hashing an incomplete archive and a manifest derived from it only proves self-consistency. V2's reviewer constructed exactly that false-property/pass world (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:39-54`).

### Required independent anchors

Before minting, the real gate must receive all of the following from sources that predate and are independent of its scan:

1. the canonical ledger repo path and parent Git object;
2. an authoritative operator-root census with provenance and a coverage-through boundary;
3. an authoritative retained remote-allocation snapshot census with provenance and a coverage-through boundary;
4. the exact expected member identity for every census entry;
5. a rule that maps every expected member to exactly one terminal state: `SCANNED_NO_HIT`, `SCANNED_HIT`, or `UNRESOLVED_STOP`.

Those real anchors are `UNKNOWN`. A new V3-authored statement that they are complete would be circular and is not accepted.

### RED world and reproduction

Build a known-good local fixture in which the independent census is fixed first as:

```text
R1
R2
R3
```

and the observed archive initially contains the same three roots with every member readable. Confirm the real gate's GREEN control. Then delete only observed root `R3`; do not change the independent census. Regenerate every archive-derived inventory, manifest, count, and hash so they agree with the incomplete archive. Run the production completeness gate.

Required result: `COLLISION_UNIVERSE_STOP missing=R3`; no generator call and no `NO_COLLISION` result. A pass proves the gate still lets the checked bundle define its own universe. Repeat by adding an unexpected observed `R4`, making one expected file unreadable, adding a reparse point, and removing one remote-census member. Every admitted member must retain a terminal disposition; silent omission is forbidden by the conservation rule (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:936-972`).

### Present evidence state

The failure world is constructible, but the real authoritative census and the executable gate are not established. Therefore V3 makes no collision-completeness or no-hit claim. Finding 3 is not closed.

## 7. Failure demonstration F4 — append-only enforcement and recovery

### Claim boundary

For one candidate transition, immutable parent blob bytes `P` come from a separately committed parent Git object. The candidate is valid only if it is exactly `P || R`, where `R` is one validated LF-terminated next row, and the full chain has no duplicate, skipped, reordered, or illegal transition. Expected prior bytes may never come from the mutable working ledger.

V2 described this prefix/suffix/chain idea, but no executable verifier or run evidence existed (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:56-67`).

### RED world and reproduction

Start from a parent Git blob `P` and a valid next row `R`. Run the actual verifier once on `P || R` as the GREEN control. Then run these mutations independently:

1. flip one byte inside the `P` prefix, leaving `R` valid;
2. delete one byte from `P`;
3. insert one byte before the parent EOF;
4. duplicate the next row reference;
5. skip the next sequence number;
6. name a non-last global predecessor;
7. use an illegal identity transition;
8. append one extra byte after `R`;
9. commit bytes whose blob differs from the pre-commit candidate.

Each case must invoke the production verifier and produce a specific `LEDGER_APPEND_STOP` before the candidate can be called append-only. The auditor records parent commit/path/blob, parent length/SHA, candidate length/SHA, first mismatch offset where applicable, exact row bytes, command, streams, and result.

### Failure recovery demonstration

Force the production append/commit path to fail after identities exist: short-write the candidate, reject the commit parent, and substitute a different committed blob in separate runs. The canonical parent must remain byte-identical. The same identities must then appear as `BURNED` on a separately preregistered append-only recovery surface that did not depend on the invalid primary candidate. The auditor must verify the burn from its own immutable parent object.

V2 supplied no such safe recovery surface and acknowledged that a malformed primary suffix can make a valid chained burn impossible without forbidden repair (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:67-69`). The canonical path, production verifier, recovery surface, and mutation transcript are all `UNKNOWN`. Finding 4 is not closed.

## 8. Failure demonstration F5 — checked object equals sourced object

### Claim boundary

The actual top-level caller must bind the exact object it verifies to the exact object the child opens. A matching variable name or an instruction that the caller “must” pass a snapshot is not evidence. The V2 review found no caller, argv, open identity, or transcript proving sameness (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:71-93`).

### RED world and reproduction

Prepare two local files:

- `A`: the exact required 18,968-byte predicate object with the fixed SHA-256;
- `B`: different bytes that define the expected function name, emit an accepted grammar line, and create a harmless local marker.

Run the real top-level caller through an auditor-controlled launch seam with these cases:

1. GREEN control: verify `A`, pass/open `A`, source `A`;
2. RED-1: verify `A`, but substitute `B` as the child source argument;
3. RED-2: verify a pathname for `A`, then replace its directory entry with `B` before the child open;
4. RED-3: pass `A` to the child but cause the child to source `B` through an alternate environment/startup path.

The control must show one concrete stable object identity on verification and child open. Every mutation must produce `PREDICATE_BINDING_STOP` before predicate or stream acceptance. The marker may prove that deviant code ran, but its output may never be accepted as grammar evidence. The caller must record source identity, locked snapshot identity, actual argv, child-open identity, pre/post lengths and hashes, Bash identity, command, streams, and result.

The auditor must drive the production caller, not a helper that independently compares `A` and `B`. This follows the declared-versus-executed instrument rule: mutation must replace the declared instrument while driving the real top-level caller (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:860-895`). No such caller or transcript exists in V3. Finding 5 is not closed.

## 9. Non-self-referential commit binding

V2 required the record to contain identities that depended on the commit containing that record, an unattainable self-reference, and left the later binding mechanism unspecified (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:52-54,95-100`). V3 forbids a file from claiming its own final commit or blob identity.

A future binding may close only through an acyclic sequence:

1. finalize the allocation-record bytes without their own commit/blob identity;
2. commit those exact bytes with the ledger candidate under an independently pinned parent;
3. derive the allocation commit, record path, record blob, bytes, and SHA-256 from Git after that commit exists;
4. place that tuple in a later child artifact whose parent relation to the allocation commit is mechanically checked;
5. require every spender to verify the child-to-parent relation and re-derive the record blob from the named parent commit/path.

The later child artifact path, schema, and controlling authority are `UNKNOWN`. This section is a non-self-referential design constraint, not closure evidence or authorization.

## 10. Commit and spend gate

This V3 must not be represented as a populated or spendable allocation. A future candidate may cross the local commit gate only after all of the following are literal and reproducible:

1. every field in section 3 is concrete;
2. the real population gate passes and its four mutations go RED;
3. the real byte-stream gate passes exact bytes and rejects all NUL/length/extra-stream mutations;
4. independent collision authorities are established before minting, and the omission mutation goes RED even after every archive-derived manifest/hash is regenerated;
5. the real append verifier passes immutable-parent plus exact-row bytes and rejects every history mutation;
6. the durable burn-recovery mutation succeeds without repairing or deleting prior bytes;
7. the real caller binds the verified object to the child-opened object and rejects the `A`/`B` substitution;
8. the commit binding follows an acyclic later-child scheme;
9. every test record contains the literal command, fixture identity, stdout, stderr, result, and RED/GREEN disposition;
10. an independent reviewer invokes the actual gates and reproduces the mandatory tests.

The V1 review required actual values and actual results before commit, not template prose (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_REVIEW_2026-08-15.md:5-39`). V2's bottom line confirmed that all five findings remained open (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_V2_REVIEW_2026-08-15.md:103-105`). V3 deliberately preserves that block until evidence exists; it does not convert a better-looking design into an apparent closure.

No host, network, SSH, deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, economic action, acceptance, or authorization is performed or granted by this record.
