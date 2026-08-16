Status: TWO-COMMIT CHAIN DESIGN V1 — NOT ACCEPTED — implements owner Option A of 2026-08-16

# Scope and authority boundary

This is a T2 design/evidence artifact. It creates no acceptance, host-contact authority, staging authority, grant-#6 binding, credential permission, deployment permission, or economic permission. The owner authorized design, drafting, and review only, and expressly did not authorize machine contact or a staging run. `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:3-12,28-38`

The design replaces the single-Commit-1 contract with two Git objects:

- **Commit 1a** is a mechanically verified procedure commit. It freezes stable candidate expectations, allocation, exact procedure bytes, schemas, and an explicit no-authority fence.
- A separately authorized fresh candidate-bound A-0..A-9 run then produces one immutable final checkpoint record.
- **Commit 1b** is the direct first-parent child of 1a. It adds the fresh candidate binding and independently verified non-candidate bindings without changing any procedure byte.
- Grant #6 may be bound only to verified Commit 1b.

The current single-commit contract is genuinely cyclic: old Step 8 requires verified Commit 1 while old Step 10 requires the Step-8-derived final checkpoint. Only the candidate-binding TSV is intrinsically Step-8-derived; allocation and root-channel inputs are not. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_DEPENDENCY_CYCLE_ANALYSIS_2026-08-16.md:20-67,102-112`

## 1. Commit 1a — procedure commit

### 1.1 Content rule

Commit 1a contains exact procedure and schema bytes, but it is intentionally not executable as the grant-#6 capture subject. The procedure must refuse to open a socket unless it is running from a verified Commit 1b whose direct parent is this exact 1a and whose concrete binding files pass all checks in sections 3, 4, and 7.

Commit 1a contains **no data value** for MainPID, process start time, active state, restart count, running-process executable path or digest, running-process network namespace, or any other live final-checkpoint observation. Field names may appear in a schema; no data row for those fields may appear. This is the required split between stable expectations and later observations. The present V2 contract puts those live values in the candidate row, which is precisely what creates the cycle. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:112-137`; `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_DEPENDENCY_CYCLE_ANALYSIS_2026-08-16.md:88-100,118-128`

The design-time values below that depend on a future accepted candidate are `UNKNOWN-until-frozen-T0-candidate`. They must be concrete before 1a is created; the token itself is not permitted in the committed 1a data row. The eight admin facts are different: their schema slots deliberately carry the exact 1a value `UNKNOWN-until-admin-review`, because the task requires their unresolved state to remain visible and non-executable.

### 1.2 `COMMIT1A_CHAIN_CONTROL.tsv`

One ASCII, LF-only, final-LF header and one data row. Every literal comes from this owner-selected design after acceptance; the builder is not its own policy source.

| Field | Commit-1a content | Independent source | Mechanical verification |
|---|---|---|---|
| `CHAIN_SCHEMA_VERSION` | `WPI_OPTION_A_TWO_COMMIT_V1` | Owner Option A plus the accepted design, not the builder | Parse the one-row TSV and require literal equality. |
| `COMMIT_ROLE` | `PROCEDURE_1A` | Accepted design | Require literal equality and reject the field in 1b if changed. |
| `FINAL_COMMIT_ROLE` | `FINAL_PREREGISTRATION_1B` | Owner Option A | Require literal equality. |
| `FINAL_PARENT_POLICY` | `DIRECT_FIRST_PARENT_IS_1A` | Accepted design, tightening the owner's required descendant relationship | At 1b, require `git rev-parse <1b>^1` to equal the independently frozen 1a OID; extra parent or intervening commit blocks. |
| `PROCEDURE_IMMUTABILITY_POLICY` | `ALL_1A_PROCEDURE_BLOBS_IDENTICAL_IN_1B` | Option A anti-self-confirmation rule | Compare every procedure-member blob OID in 1a and 1b; any change blocks. |
| `ALLOWED_1B_DELTA_PATHS_B64` | Canonical base64 of the sorted, NUL-terminated path list in §1.7 | Accepted design/path universe, not the 1b manifest | Decode, re-encode, compare to the fixed accepted list, then compare the actual 1a..1b diff to it. |
| `CANDIDATE_BINDING_SOURCE_POLICY` | `FRESH_GATEA_FINAL_RECORD_ONLY` | Owner Option A | Require the candidate TSV provenance to name only the sealed fresh record; reject any second source. |
| `ALLOCATION_SOURCE_PATH` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_ALLOCATION/STAGE1_ALLOCATION_RECORD.tsv` | Existing V2 exact source contract | Resolve that path in 1a, require one blob, and compare its OID to the 1a manifest row. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:89-110` |
| `STABLE_EXPECTATIONS_PATH` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT_CHAIN/STAGE1_STABLE_CANDIDATE_EXPECTATIONS.tsv` | Accepted design | Resolve from 1a and compare to the manifest row. |
| `FINAL_CANDIDATE_BINDING_PATH` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT_CHAIN/STAGE1_CANDIDATE_BINDING.tsv` | Existing candidate schema plus this split design | Require absence in 1a and presence only in 1b; a concrete candidate data row in 1a blocks. |
| `FINAL_ROOT_BINDING_PATH` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STAGE1_COMMIT_CHAIN/STAGE1_ROOT_CHANNEL_BINDING.tsv` | Existing root-channel schema plus this split design | Require absence in 1a and presence only in 1b. |
| `COMMIT1A_HOST_AUTHORITY` | `NONE` | Owner Option A design-only sentence | Require literal equality and scan every 1a authority field for no conflicting grant. |
| `COMMIT1A_GRANT6_BINDING_STATE` | `PROHIBITED` | Owner Option A: bind grant #6 only to final commit | Require literal equality; any grant record naming 1a blocks. |
| `GATE_A_AUTHORITY_REQUIREMENT` | `SEPARATE_OWNER_RECORD_REQUIRED` | Existing authority separation | Require literal equality and an independent Gate-A authority check before Step 8. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:83-105` |
| `UNKNOWN_POLICY` | `STOP_NEVER_FAIL` | Defect Pattern 1 and current transition rule | Schema-aware verifier must map absent/unreadable/unevaluable input to STOP, never host-state FAIL. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-107` |

### 1.3 `STAGE1_STABLE_CANDIDATE_EXPECTATIONS.tsv`

All values are stable and must be fixed from the exact frozen candidate/T0 package before 1a. Today they are `UNKNOWN-until-frozen-T0-candidate`; no value is guessed. The expected identity comes from the frozen candidate package, never from the later TSV producer, as Option A requires. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_DEPENDENCY_CYCLE_ANALYSIS_2026-08-16.md:118-128`

| Field | Required 1a content | Independent source | Mechanical verification |
|---|---|---|---|
| `STAGING_HOST` | `GATEA-STAGING` | Owner host boundary and integration contract | Literal comparison; also require `PRODUCTION_HOST_EXCLUSION=KVM2`. |
| `PRODUCTION_HOST_EXCLUSION` | `KVM2` | Disposable-host rule | Literal comparison; pre-run host identity must not equal production KVM2. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md:29-44` |
| `WPI_CANDIDATE_SHA` | Exact 40-lowercase-hex frozen candidate commit | Independently T0-accepted candidate record | Read the selected commit from the frozen source manifest and compare exact bytes. |
| `CANDIDATE_TREE_OID` | Exact Git tree OID | Frozen candidate Git object | Resolve `<candidate>^{tree}` and compare; any object-format inability is STOP. |
| `CANDIDATE_ARTIFACT_SHA256` | Exact 64-lowercase-hex artifact digest | Reproducible build/T0 evidence | Hash the independently frozen artifact twice through the accepted verifier and compare. |
| `CANDIDATE_MANIFEST_SHA256` | Exact 64-lowercase-hex manifest digest | Reproducible build/T0 evidence | Hash the force-enumerated manifest bytes and compare. |
| `CANDIDATE_MANIFEST_BLOB_OID` | Exact Git blob OID | Frozen candidate commit | Read the selected Git object and compare to the separately hashed on-disk form; do not assume LF/CR equality. |
| `UNIT_NAME` | `mtc-bridge-first-start.service` | Accepted integration/Gate-A contract | Literal comparison against the frozen unit/package input. |
| `EXPECTED_MAINPID_CWD` | `/opt/mtc-bridge/releases/<WPI_CANDIDATE_SHA>/IBKR_PAPER_BRIDGE` | Candidate SHA plus accepted path formula | Rebuild from the independently sourced SHA and require byte equality. |
| `EXPECTED_MAINPID_CMDLINE_B64` | Canonical base64 of `/opt/mtc-bridge/venvs/<sha>/bin/python\0-m\0bridge.app\0` | Candidate SHA plus accepted command contract | Rebuild the NUL-bearing bytes independently, base64-decode/re-encode, and compare. |
| `EXPECTED_MAINPID_CMDLINE_SHA256` | SHA-256 of the exact command-line bytes above | Independently rebuilt bytes | Recompute from decoded bytes; do not copy the digest from the candidate row. |
| `GATE_A_RUN_KIT_BLOB_OID` | Exact accepted run-kit blob/object identity | Independently accepted run-kit source manifest | Resolve and compare every run-kit member; a manifest-only universe is insufficient. |
| `T0_ACCEPTANCE_RECORD_BLOB_OID` | Exact two-flagship accepting record identity | Independent T0 auditors and frozen source manifest | Read back the record and verify exact model/effort/execution evidence; non-execution is not acceptance. |

No field in this table is MainPID, start time, active state, restart count, a running executable path/digest, or a live namespace identity.

### 1.4 Concrete allocation record included in 1a

The old Step 9 allocation is moved before 1a because its data is local and not intrinsically derived from A-0..A-9. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_DEPENDENCY_CYCLE_ANALYSIS_2026-08-16.md:35-39`

| Field | Source | Mechanical verification |
|---|---|---|
| `ATTESTATION_RECORD_ID` | Append-only allocator over the independent collision universe | Require `WPI-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}-ATT-01`; prove it absent from every independently enumerated source before minting. |
| `BASE` | Same single allocator event | Require `WPI-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}` and exact prefix relationship to the record ID. |
| `P0_RUNID` | Derived from independently allocated `BASE` | Require exact `<BASE>-P0`. |
| `RO_RUNID` | Derived from independently allocated `BASE` | Require exact `<BASE>-RO`. |
| `REMOTE_BASE` | Accepted path formula plus allocated `BASE` | Require exact `/home/gatea/wpi_staging_<BASE>`. |
| `CONFIRM_TOKEN` | Accepted token formula plus allocated `BASE` | Require exact `<BASE>-EXECUTE`. |
| `OPERATOR_RECORD_ROOT` | Accepted operator-root formula plus allocated `BASE` | Require exact `C:\WPI_ARTIFACTS\WPI_TRANSPORT_<BASE>` and non-reparse literal resolution. |
| `OPERATOR_RECORD_PATH` | Root, record ID, and accepted child rule | Rebuild once as `<root>\attestation\<record-id>.record`; independent typing is forbidden. |
| `OPERATOR_RECORD_PARENT_STATE` | Local filesystem preflight | Require literal `EXISTS_EMPTY_CREATE_ONCE` from an independently captured preflight; unreadable means STOP. |
| `COLLISION_RESULT` | Independent ledger/root/remote-allocation universe | Require `NO_COLLISION_ALL_CANONICAL_SOURCES` only after all source classes reconcile; the allocation candidate cannot define the universe. |
| `ALLOCATION_DISPOSITION` | Enforced append-only ledger transition | Require literal `RESERVED`, predecessor-prefix proof, and a durable burn path already accepted. |

These grammars preserve the existing exact allocation contract. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:89-110` Collision completeness and append-only enforcement must have real discriminating evidence; a declaration is not a check. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:16-23,45-63`

### 1.5 Frozen operator-tool identities

These are stable local inputs, not live target observations. They must be concrete in 1a.

| Field | Required 1a content | Independent source | Mechanical verification |
|---|---|---|---|
| `POWERSHELL_EXE_PATH` | `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe` | Accepted operator-tool inventory | Compare normalized absolute path to the independently frozen inventory. |
| `POWERSHELL_EXE_SHA256` | Concrete 64-lowercase-hex digest | Independently hashed tool bytes | Open the exact path read-only and recompute SHA-256 before launching. |
| `OPERATOR_PYTHON_PATH` | `C:\Python314\python.exe` | Accepted operator-tool inventory | Exact absolute-path comparison. |
| `OPERATOR_PYTHON_SHA256` | Concrete 64-lowercase-hex digest | Independently hashed tool bytes | Recompute before recorder start. |
| `GIT_EXE_PATH` | `C:\Program Files\Git\cmd\git.exe` | Accepted operator-tool inventory | Exact absolute-path comparison; no PATH lookup. |
| `GIT_EXE_SHA256` | Concrete 64-lowercase-hex digest | Independently hashed tool bytes | Recompute before any Git check. |
| `SSH_EXE_PATH` | `C:\Windows\System32\OpenSSH\ssh.exe` | Accepted operator-tool inventory | Exact absolute-path comparison; no PATH lookup. |
| `SSH_EXE_SHA256` | Concrete 64-lowercase-hex digest | Independently hashed tool bytes | Recompute before any socket may open. |

### 1.6 Procedure member manifest and schemas

The force-inclusive 1a member universe comes from the accepted design, not from the manifest it checks. It contains the chain-control TSV, stable-expectations TSV, allocation TSV, `COMMIT1A_OPERATOR_TOOLS.tsv`, parameterized target producer, parameterized operator recorder, launcher, candidate schema, root-channel schema, preregistration text, and the procedure manifest. The no-authority fields live in chain control; there is no second authority record that could disagree. The manifest excludes a self-digest row but the 1a Git object binds the manifest itself.

Each non-manifest row has these fields:

| Field | Independent source | Mechanical verification |
|---|---|---|
| `ordinal` | Accepted force-inclusive path list | Require canonical positive decimal and exact list order. |
| `path` | Accepted path list | Compare to force-inclusive `git ls-tree` output; extra/hidden/missing path blocks. |
| `bytes` | Actual member bytes, checked against reviewer-owned freeze evidence | Recount raw bytes; this proves identity, not correctness. |
| `sha256` | Reviewer-owned exact-byte freeze record | Recompute raw SHA-256 and compare. |
| `git_blob_oid` | Git object read-back | Resolve 1a:path and compare to `hash-object --no-filters`; also retain on-disk/Git dual forms. |
| `role` | Accepted design member-role map | Require one allowed role and one terminal disposition per path. |

The candidate schema lists all §3.2 fields but has no data row in 1a. The root-channel schema places the eight still-unknown facts exactly as follows:

| Admin fact | Exact 1a schema-slot value | Where the concrete value goes in 1b |
|---|---|---|
| SSH principal | `UNKNOWN-until-admin-review` | `SSH_TARGET` and `SERVER_AUTHORIZED_KEY_BINDING` |
| Account shell | `UNKNOWN-until-admin-review` | `ACCOUNT_UID_GID`, `ACCOUNT_SHELL_PATH`, `ACCOUNT_SHELL_SHA256` |
| Forced command | `UNKNOWN-until-admin-review` | `FORCED_COMMAND_MODE` and exact forced-command bytes/argv or proved `NONE` |
| Wrapper mapping | `UNKNOWN-until-admin-review` | `ROOT_WRAPPER_PATH`, `ROOT_WRAPPER_SHA256`, `ATT01_TARGET_PROCESS_CHAIN`, `ATT01_REMOTE_COMMAND` |
| Pre-`env` environment | `UNKNOWN-until-admin-review` | `ATT01_PRE_ENVIRONMENT_B64` |
| Initial cwd | `UNKNOWN-until-admin-review` | `ATT01_INITIAL_CWD` |
| Descriptor set | `UNKNOWN-until-admin-review` | `ATT01_STDIN_MAPPING` and `ATT01_FD_MAPPING` |
| Mutation-denial wrapper/control | `UNKNOWN-until-admin-review` | `TARGET_MUTATION_DENIAL_CONTROL` |

All eight are still unestablished today. The repository records 0/8 established and says they cannot be accepted merely because a launcher and recorder repeat values from the same TSV. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:172-187,197-214,230-236`

The adjacent, ninth root-channel prerequisite is not one of the eight: `INFRASTRUCTURE_CROSSOVER_RESULT`. Its 1a schema-slot value is `UNKNOWN-until-independent-crossover-proof`, and 1b requires the concrete literal `NO_ROTATION_NO_OUT_OF_STORE_ACTION_NO_SIDE_EFFECT_HOOK` from independent channel evidence. Resolving the eight facts alone does not resolve this blocker. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:189-195`

### 1.7 Exact 1b delta allowlist and 1a verification

Only these paths may be added or changed from 1a to 1b:

1. `STAGE1_GATEA_FINAL_RECORD.tsv` — sealed copy/provenance of the fresh record.
2. `STAGE1_CANDIDATE_BINDING.tsv` — concrete final candidate row.
3. `STAGE1_ROOT_CHANNEL_BINDING.tsv` — concrete independently verified root/tool/channel row.
4. `COMMIT1B_CHAIN_BINDING.tsv` — 1a/1b ancestry, delta, and input identities.
5. `COMMIT1B_FINAL_PREREGISTRATION.md` — final exact human-readable contract.
6. `COMMIT1B_PACKAGE_MANIFEST.tsv` — final complete package identity.

No producer, recorder, launcher, schema, allocation, stable-expectations, tool-identity, 1a authority-scope, or 1a procedure-manifest byte may change. A procedure change requires a new 1a, a new separately bound staging authority where applicable, a new fresh A-0..A-9 run, and a new 1b.

Commit 1a verification is: clean exact source state; schema-aware no-live-value check; force-inclusive member reconciliation; exact tool and candidate/T0 identity checks; D026 RED/GREEN for every executable check; exact-byte review; create 1a; read it back; prove dual-form identities and clean current state. Pre-create failure is `COMMIT1A_NOT_STARTED_STOP`. Any possible creation followed by failed read-back is `COMMIT1A_CREATED_UNVERIFIED_QUARANTINE`; preserve the observed object/reference and do not amend, reset, delete, rewrite, or use it.

## 2. The staging run

### 2.1 Separate authority

The fresh candidate-bound A-0..A-9 run is covered only by a separately owner-authored and mechanically bound `GATE_A_STAGE_AUTHORITY`. **No such exact authority sentence is currently established.** The current runbook says the value is `UNKNOWN` and requires the future sentence to name the exact candidate, disposable `GATEA-STAGING`, A-0..A-9 scope, credential/channel, permitted mutations, mandatory close/safe-state contract, time/use limit, and exclusions. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:83-92`

The Option A sentence is not that authority: it expressly authorizes design and review only. `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:28-38`

Grant #6 is also not that authority. Grant #6 is a one-command-set read-only attestation in the G3 root session; the later D2 sentence remains conditional on exact preregistered committed bytes and excludes writes and deployment. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:55-58`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-60` By contrast, fresh Gate-A includes install, service start, SIGKILL, and explicit restart activity. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:239-250`

### 2.2 Required fresh record

The staging runner must create one immutable, create-once final record after fresh A-0..A-9. Historical PASS transfers are forbidden. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:229-255`

The record must contain:

- record schema/version, run ID, byte count, SHA-256, create-once path, close/fsync result, and one terminal disposition;
- exact verified Commit-1a OID and procedure-manifest blob;
- exact `GATE_A_STAGE_AUTHORITY` source identity and binding result;
- exact `GATEA-STAGING` host identity plus explicit KVM2 exclusion;
- exact candidate commit/tree, artifact digest, candidate manifest identity, and Gate-A run-kit identity;
- one terminal disposition and evidence identity for each of A-0 through A-9, with no historical PASS reuse;
- safe-final-host-state predicate and result;
- `CHECKPOINT_ID=STAGE1_EXACT_CANDIDATE_A0_A9_FINAL`;
- all 13 candidate-binding fields in §3.2, captured at that final checkpoint;
- raw evidence identities from which the running executable digest, command line, namespace, state, and restart values can be independently recomputed; and
- an explicit staging-only verdict with no implication of grant #6, WP-I, production KVM2, merge, credential expansion, ARM, broker, order, TESTNET/mainnet, or economic authority.

The final record must bind the live observations to the independently frozen candidate expectations in 1a. The record cannot prove itself correct merely by repeating its own candidate SHA. Wrong candidate, wrong host, missing A-step, unsafe close, or incomplete read is STOP/FAIL as classified by the actual observation; inability to evaluate is STOP.

## 3. Commit 1b — final exact preregistration

### 3.1 Entry gate and immutable relationship to 1a

Commit 1b may be attempted only after:

1. Commit 1a is mechanically verified and independently frozen by OID.
2. The separate Gate-A authority, preflight, and safe-close contract passed before the staging socket opened.
3. Fresh A-0..A-9 closed with a sealed final PASS record for the exact 1a candidate.
4. Allocation remains reserved and unchanged.
5. All eight admin facts have moved from `UNKNOWN-until-admin-review` to concrete independently sourced values.
6. The separate crossover result, tool identities, mutation control, exact argv/environment/cwd/FD chain, D026 evidence, and exact-byte review all pass.

The candidate binding comes only from the fresh record. Every other required input has its own source and check. The final object must be the direct first-parent child of exact 1a, and the actual diff must equal the §1.7 allowlist. Option A specifically requires ancestry, candidate/host matching, an allowlisted delta, and no grant-#6 binding to 1a. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_DEPENDENCY_CYCLE_ANALYSIS_2026-08-16.md:118-128`

### 3.2 `STAGE1_CANDIDATE_BINDING.tsv`

Every value in this table is copied byte-for-byte from the sealed fresh A-0..A-9 final record; there is no fallback source.

| Field | Sole producer source | Independent verification |
|---|---|---|
| `STAGING_HOST` | Fresh final record | Require literal `GATEA-STAGING` and match 1a host expectation; reject KVM2. |
| `CHECKPOINT_ID` | Fresh final record | Require literal `STAGE1_EXACT_CANDIDATE_A0_A9_FINAL`. |
| `WPI_CANDIDATE_SHA` | Fresh final record | Require 40 lowercase hex and equality to 1a/T0 candidate, whose source predates the run. |
| `UNIT_NAME` | Fresh final record | Require `mtc-bridge-first-start.service` and equality to the frozen run kit. |
| `UNIT_ACTIVE_STATE` | Fresh final record | Require literal `active` from the final manager observation; no value appears in 1a. |
| `UNIT_NRESTARTS` | Fresh final record | Require canonical `0` from the final manager observation; no value appears in 1a. |
| `WPI_MAINPID` | Fresh final record | Require positive canonical decimal and bind its raw checkpoint evidence. |
| `WPI_MAINPID_STARTTIME_TICKS` | Fresh final record | Require positive canonical decimal from field 22 of the complete recorded `/proc/<pid>/stat` bytes. |
| `WPI_MAINPID_CWD` | Fresh final record | Require byte equality to independently derived 1a `EXPECTED_MAINPID_CWD`. |
| `WPI_MAINPID_CMDLINE_SHA256` | Fresh final record | Independently decode/rebuild expected NUL bytes from 1a and recompute their SHA-256; compare to the recorded raw cmdline evidence. |
| `WPI_MAINPID_EXE_PATH` | Fresh final record | Require exact absolute link result, ASCII, no whitespace, and no ` (deleted)` suffix; verify against recorded raw link evidence. |
| `WPI_MAINPID_EXE_SHA256` | Fresh final record | Recompute from the sealed executable-byte evidence captured at the checkpoint; never take the producer's digest alone as proof. |
| `WPI_MAINPID_NET_NS` | Fresh final record | Require `net:[<positive-canonical-decimal>]` and equality to sealed raw namespace-link evidence. |

The established field grammar is preserved from V2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:112-137`

### 3.3 All non-candidate inputs and their independent checks

| Input | Source independent of 1b builder | Required verification before create |
|---|---|---|
| Allocation fields | Verified append-only allocation record already in 1a | Blob unchanged from 1a; C6/C7 collision/append-only evidence still binds it. |
| Procedure, recorder, launcher, schemas | Verified 1a procedure manifest and 1a Git object | Blob-by-blob identity with 1a; zero procedure delta. |
| Stable candidate expectations | Frozen T0 candidate/package selected before staging | 1a blob unchanged; candidate record cross-checks to it. |
| Operator tool paths/digests | Independently frozen operator-tool inventory in 1a | Rehash exact absolute tools; no PATH resolution. |
| SSH principal/key mapping | Admin decision plus authoritative server-side configuration record | Compare concrete 1b fields to independently selected route and key-to-principal evidence. |
| Account shell | Authoritative provisioning/account record | Compare exact path, numeric identity, and executable digest. |
| Forced command | Effective sshd/authorized-key mapping | Require byte-exact argv or independently proved `NONE`. |
| Wrapper mapping/process chain | Admin-selected route plus configuration proof | Reconstruct one complete exec chain; no prose ellipsis or unbound program. |
| Pre-`env` environment | Independent first-process/configuration record | Decode canonical sorted `name=value\0` bytes and compare; missing observation is STOP. |
| Initial cwd | Independent first-process/configuration record | Compare exact absolute cwd before shell startup/import/`chdir`. |
| Descriptor set | Independent first-process FD inventory | Require exact 0/1/2 mapping and no additional inherited writable FD. |
| Mutation-denial control | Admin-selected enforcement policy and D026 exact-chain evidence | Demonstrate deliberate writes denied on success/failure paths while fd 1/2 remain usable. |
| Infrastructure crossover | Independent auth/audit/PAM/wrapper proof | Require no rotation, out-of-store action, or side-effect hook. |
| Final review/evidence | Reviewer/auditor independent of builder | Exact filled bytes, executable commands, actual RED/GREEN, and accepting required verdicts. |

The final `STAGE1_ROOT_CHANNEL_BINDING.tsv` is one ASCII/LF/final-LF row. Its fields are individually sourced and checked as follows; agreement between this row and the recorder is never sufficient by itself:

| Field | Independent source | Required 1b verification |
|---|---|---|
| `POWERSHELL_EXE_PATH` | Unchanged 1a tool inventory | Exact byte equality to 1a plus K28 live rehash. |
| `POWERSHELL_EXE_SHA256` | Unchanged 1a tool inventory | Recompute at the exact path and compare. |
| `OPERATOR_PYTHON_PATH` | Unchanged 1a tool inventory | Exact byte equality to 1a plus K28 path check. |
| `OPERATOR_PYTHON_SHA256` | Unchanged 1a tool inventory | Recompute at the exact path and compare. |
| `GIT_EXE_PATH` | Unchanged 1a tool inventory | Exact byte equality to 1a; prohibit PATH lookup. |
| `GIT_EXE_SHA256` | Unchanged 1a tool inventory | Recompute before Git use. |
| `SSH_EXE_PATH` | Unchanged 1a tool inventory | Exact byte equality to 1a; prohibit PATH lookup. |
| `SSH_EXE_SHA256` | Unchanged 1a tool inventory | Recompute before any socket. |
| `SSH_TARGET` | Admin-selected principal/address plus server configuration | Require exact configured principal/address and K19 key binding; this fills the SSH-principal slot. |
| `SERVER_AUTHORIZED_KEY_BINDING` | Authoritative server-side key mapping | Verify exact pinned identity maps only to the selected route; a client-side key label is insufficient. |
| `ACCOUNT_UID_GID` | Authoritative account/escalation configuration | Require exact numeric identity for each hop; rendered names are diagnostic only. |
| `ACCOUNT_SHELL_PATH` | Authoritative account record | Require exact absolute path, regular-file kind, numeric ownership/mode, and use by the selected account. |
| `ACCOUNT_SHELL_SHA256` | Independently read shell bytes | Recompute SHA-256; do not accept a value copied by the launcher. |
| `FORCED_COMMAND_MODE` | Effective sshd/authorized-key mapping | Require exactly `NONE` or `EXACT`; `NONE` must be proved, not assumed. |
| `FORCED_COMMAND_EXACT_ARGV_B64` | Effective mapping when mode is `EXACT` | Decode/re-encode canonical NUL-separated argv and compare byte-for-byte; require empty only for proved `NONE`. |
| `ROOT_WRAPPER_PATH` | Admin-selected route plus authoritative config | Require exact absolute path or proved `NONE`; no PATH resolution. |
| `ROOT_WRAPPER_SHA256` | Independently read wrapper bytes | Recompute when a wrapper exists; require literal `NONE` only when no wrapper is configured. |
| `ATT01_TARGET_PROCESS_CHAIN` | Independently verified account/sshd/wrapper execution mapping | Require a complete ordered exec chain from sshd child to `/usr/bin/env` and Python; no omitted hop or prose ellipsis. |
| `ATT01_INITIAL_CWD` | Independent first-target-process record/config | Require exact absolute cwd before startup/import/`chdir`. |
| `ATT01_PRE_ENVIRONMENT_B64` | Independent first-target-process environment record/config | Decode/re-encode sorted `name=value\0` bytes; reject unexpected startup/loader hooks. |
| `ATT01_POST_ENVIRONMENT_B64` | Accepted procedure contract | Rebuild exactly `HOME=/root\0LC_ALL=C\0PATH=/usr/bin:/bin\0PYTHONDONTWRITEBYTECODE=1\0` in sorted-key order and compare. |
| `ATT01_STDIN_MAPPING` | Accepted procedure plus independently verified channel mapping | Require literal `producer_blob_to_python_stdin_no_prefix_or_suffix` and prove no framing transformation. |
| `ATT01_FD_MAPPING` | Independent complete FD inventory | Require exact `0=ssh-stdin,1=ssh-stdout,2=ssh-stderr,all_other_fds=closed`. |
| `ATT01_REMOTE_COMMAND` | Effective forced-command/wrapper mapping plus accepted procedure | Compare complete command bytes; no placeholder, shell metavariable, or independently expanded copy. |
| `ATT01_OUTER_ARGV_B64` | Admin-selected route, 1a tool identity, and accepted procedure | Independently construct exact NUL-separated Windows argv with final NUL, then canonical-base64 compare. |
| `ATT01_OUTER_ARGV_SHA256` | Independently constructed outer argv bytes | Recompute SHA-256 from decoded bytes; never copy the recorder's own digest as expectation. |
| `TARGET_MUTATION_DENIAL_CONTROL` | Admin-selected policy plus exact-chain D026 evidence | Bind exact control identity and require success/failure write mutations to be denied while fd 1/2 remain usable. |
| `INFRASTRUCTURE_CROSSOVER_RESULT` | Independent channel/runtime evidence | Require literal `NO_ROTATION_NO_OUT_OF_STORE_ACTION_NO_SIDE_EFFECT_HOOK`; unreadable or partial evidence is STOP. |

The existing V2 review explains why the outer argv, end-to-end no-mutation boundary, recorder, canonical grammar, exact filler sources, MainPID binding, and clean-object rule all have to be exact before the final commit. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_REVIEW_2026-08-15.md:29-79,81-110`

### 3.4 `COMMIT1B_CHAIN_BINDING.tsv` and final package verification

The chain-binding row contains: `COMMIT1A_OID`, `COMMIT1A_PROCEDURE_MANIFEST_BLOB`, `COMMIT1B_PARENT_OID`, `ALLOWED_DELTA_PATHS_SHA256`, `ACTUAL_DELTA_PATHS_SHA256`, `GATEA_FINAL_RECORD_SHA256`, `CANDIDATE_BINDING_BLOB`, `ROOT_BINDING_BLOB`, `ALLOCATION_BLOB`, `FINAL_PACKAGE_MANIFEST_PATH`, `PROCEDURE_BLOBS_UNCHANGED`, and `GRANT6_ELIGIBILITY`.

Each field is verified as follows:

- the expected 1a OID comes from the pre-staging frozen 1a record, not from 1b;
- the parent OID comes from Git object read-back and must equal that expected OID;
- the expected allowlist comes from 1a chain control; the actual list comes from the force-inclusive 1a..1b diff;
- the Gate-A digest comes from the sealed final record identity produced before 1b;
- all listed blobs come from 1b object read-back and must reconcile to independent source records;
- `FINAL_PACKAGE_MANIFEST_PATH` comes from the accepted path universe; its blob OID is recorded only after 1b in the external read-back record, because embedding that OID in a chain-binding file which the manifest itself identifies would create a hash cycle;
- `PROCEDURE_BLOBS_UNCHANGED` may be `PASS` only after one-to-one blob comparison; and
- `GRANT6_ELIGIBILITY` is only `READY_FOR_SEPARATE_BINDING`, never `BOUND`. Commit creation cannot create owner authority.

Pre-create non-PASS is `COMMIT1B_NOT_STARTED_STOP`. If creation was attempted or may have succeeded but read-back/parent/delta/identity verification is not PASS, record `COMMIT1B_CREATED_UNVERIFIED_QUARANTINE`, preserve actual object/reference state, and do not amend, reset, delete, rewrite, or continue.

## 4. Grant #6 binding

Grant #6 binds only to the exact verified Commit-1b object. Step 11 is a local authority-binding check and opens no socket.

The check takes two independent inputs:

1. the owner-authored grant-#6/D2 authority source, including host, exact read-only action, pinned identity, and exclusions; and
2. the independently read-back verified 1b object and its exact final preregistration/package manifest.

It produces `GRANT6_CAPTURE_AUTHORITY_BOUND=PASS` only when all of the following hold:

- the named object is Commit 1b, not 1a;
- 1b's direct parent is the exact verified 1a;
- the allowed-delta and unchanged-procedure checks pass;
- all candidate/root/tool/allocation fields are concrete and independently verified;
- the host is `GATEA-STAGING`, the action is the exact committed read-only ATT-01 capture, and the credential and exclusions match the owner sentence;
- the recorder's first immutable record line is specified as `attestation_prereg_commit=<COMMIT_1B_OID>`; and
- clean current object/package checks pass again immediately before socket open.

The binding fails closed—classified as `GRANT6_AUTHORITY_UNBOUND_STOP`—if it names 1a, a different descendant, dirty bytes, a different host/action/identity, a broadened scope, a changed procedure blob, a missing/unknown input, or a candidate record not sourced solely from the fresh A-0..A-9 record. Inability to read or evaluate any input is STOP, never FAIL. The D2 sentence cannot be rebound by inference. The existing runbook already requires exact-object binding and says D2 cannot set Gate-A authority. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:292-306`

## 5. Runbook reordering

### 5.1 Old cycle and replacement order

The current V2 and its V3 patch are not operable. The patch review also found that literal application leaves one artifact simultaneously identified as V2 and V3 and that its proposed test does not prove the whole repair. A future integrated runbook must fix those seams as well as adopt this ordering. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_PATCH_REVIEW_2026-08-16.md:7-15,79-126`

| Existing location | Existing dependency | Option-A replacement |
|---|---|---|
| Step 7 | Cycle resolution is `UNKNOWN` | Accept and pin the owner-selected two-commit contract; this design alone is not acceptance. |
| Old Step 9 | Allocation waits procedurally on Step 8 | **Step 7A:** move local allocation before 1a; require independent collision/append-only checks. |
| New | None | **Step 7B:** create and verify procedure Commit 1a; it grants no host or grant-#6 authority. |
| New | None | **Step 7C:** bind separate `GATE_A_STAGE_AUTHORITY` and accepted safe-close contract to exact candidate/1a/run kit. |
| Old Step 8 / H-A | Requires final Commit 1, which itself needs Step 8 | **Step 8:** require verified 1a—not 1b—plus candidate T0 acceptance, separate Gate-A authority, exact disposable host, and safe-close preflight; run fresh A-0..A-9. |
| New | Step-8 record did not have its own local transition | **Step 8A:** seal and verify the fresh final record and derive the candidate TSV solely from it. |
| Old Step 9/10 join | Root/admin/tool inputs mixed into single commit step | **Step 9:** local final-input join; independently verify allocation, all eight admin facts, crossover, tools, mutation control, and D026 evidence. |
| Old Step 10 | Creates single Commit 1 and requires no prior host command | **Step 10:** create/read back Commit 1b as direct child of 1a; the only prior host action permitted is the separately authorized Step-8 A-0..A-9 run. |
| Step 11 | Binds grant #6 to Commit 1 | Bind grant #6 only to exact verified Commit 1b. |
| Step 12 / H-6 | Exact Commit-1-bound capture | Require exact verified 1b and its separate grant binding; run the unchanged read-only capture contract. |

This removes both directions of the old cycle: Step 8 no longer waits for 1b, and Step 10 no longer claims that no host command has run. It instead proves that the only intervening host action was the separately authorized, exact-candidate Gate-A run and that its final record is the sole candidate-binding source.

### 5.2 Full ordered-path walk

This is a documentary reachability proof for a compliant operator, not a mechanical interlock. I can demonstrate the ordering property below. I **cannot** demonstrate that the path is currently executable: the integrated runbook is not accepted/pinned, `GATE_A_STAGE_AUTHORITY` is `UNKNOWN`, all eight admin facts remain `UNKNOWN-until-admin-review`, and the crossover proof is absent. Therefore the real current path stops before any host action.

| Step | Walk and host guard |
|---|---|
| 1 | Local source freeze/review only. If the future integrated runbook is not accepted and pinned, STOP. No host edge. |
| 2 | Record the already owner-ratified cumulative plan reading. It creates no host edge. `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:40-45` |
| 3 | Locally verify the common KVM2 Phase-2 close record. Missing identity stops; no host action. |
| 4 | Record the owner's Pathscope supplemental/off-critical-path disposition. No repair or host action is inferred. `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:62-72` |
| 5 | Owner-bound branch-local integration decision plus dry local applicability/recovery preflight. No host action; a local partial is quarantined. |
| 6 | Local integration, tests, build, D026, and two T0 flagship acceptances for the exact candidate. No staging host action. |
| 7 | Accept/pin the Option-A contract and revised runbook. The owner selection is design authority only; until acceptance the path stops. |
| 7A | Local allocation with independent collision universe and append-only enforcement. No socket or host. |
| 7B | Local create/read-back verification of Commit 1a. 1a explicitly grants no authority. |
| 7C | Local binding of a separately owner-authored Gate-A authority and accepted safe-close contract to exact 1a/candidate/run kit/host. If any input is absent or unevaluable, STOP before socket open. Grant #6 has no edge here. |
| 8 / H-A | First possible host action. Reachable only after 7C PASS and all H-A predicates. It targets disposable `GATEA-STAGING`, never KVM2, and runs only exact A-0..A-9. Non-PASS reaches only the predeclared close and safe-state proof. |
| 8A | Local seal/verification of the fresh final record and candidate TSV. It performs no new host action. Incomplete or self-inconsistent evidence cannot advance. |
| 9 | Local join of allocation, eight admin/config facts, crossover, tools, mutation control, and exact evidence. Today this step stops because the eight facts and crossover remain unknown. |
| 10 | Local create/read-back verification of Commit 1b. Only allowed data/provenance/manifest paths may differ from 1a; all procedure blobs remain identical. |
| 11 | Local grant-#6 binding to exact 1b. It cannot bind 1a and opens no socket. |
| 12 / H-6 | Second possible host action. Reachable only after verified 1b, exact grant-#6 binding, root/mutation boundary, clean-current-object recheck, and create-once close preflight. It is the exact read-only capture, not Gate-A or WP-I authority. |
| 13 | Local targeted fills and one-to-one consumer conservation. A procedure change discards the capture and restarts at a new 1a/1b chain. |
| 14 | Local Commit-2 create/read-back verification. Pre/post-create half-states are distinct. |
| 14A | Local binding of the D2 WP-I clause and accepted always-close contract to exact Commit-2 run kit. No socket. The V3 patch correctly identifies this missing producer, though that patch is not accepted. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:134-143` |
| 15 / H-WPI | Third possible host action. Reachable only after Step-14A PASS, verified Commit 2, accepted P9-15, and WP-I close contract. It cannot inherit Gate-A authority. |
| 16 | Local Packet-9 closure. A non-PASS host run may write only P9-17 STOP; it cannot reach Step 17 or clear host quarantine. |
| 17 | Local pre-WP-A freeze, reachable only from Packet-9 PASS. |
| 18 | Local independent full-suite/runtime preflight and required RED arms. No host edge. |
| 19 | Local full-suite execution and anomaly adjudication. Probe inability is STOP; observed deviation is FAIL. |
| 20 | Local Packet-11 completion plus owner ratification of the measured actual. No host edge. |
| 21 | Local authoritative dispatch-bundle construction and conservation. |
| 22 | External model dispatch, not a staging/production host action. Both required routes preflight before either launches; a partial launch is invalid/supplemental. |

Thus no named host node is reachable before its own distinct authority and preconditions in the proposed documentary state machine. The proof does not claim mechanical enforcement or present executability. The existing runbook makes the same scope limitation explicit. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:152-192,382-401`

## 6. Failure and stop semantics

### 6.1 Per-step outcomes

| Step | Failure/STOP behavior and half-state closure |
|---|---|
| 1 | Missing, changed, or unevaluable source is `STEP_1_STOP`; no later step. No mutation. |
| 2 | Missing/ambiguous owner plan record is `STEP_2_STOP`; never infer the choice. |
| 3 | Missing, wrong, or unevaluable close identity is `STEP_3_STOP`. |
| 4 | Missing owner disposition is STOP; do not reopen a repair cycle or place Pathscope back on the critical path by inference. |
| 5 | Preflight problem is `INTEGRATION_NOT_STARTED_STOP`. After a possible local mutation, preserve exact partial state as `LOCAL_PARTIAL_QUARANTINED`; no improvised reset/abort. |
| 6 | Test/T0 non-acceptance is `CANDIDATE_LOCAL_OR_T0_STOP`. One-of-two auditor launch is `CANDIDATE_T0_PARTIAL_INVALID_STOP`; output is supplemental only. |
| 7 | Unaccepted/unpinned Option-A contract is `STAGE1_PREHOST_ORDERING_CONTRACT_STOP`. No host authority exists. |
| 7A | Before mint, inability to prove collision completeness is `ALLOCATION_UNIVERSE_STOP`. After mint, any failure uses the already accepted durable burn path and stops; if that path was unavailable, minting was ineligible. |
| 7B | Pre-create non-PASS is `COMMIT1A_NOT_STARTED_STOP`. Post-create/read-back uncertainty is `COMMIT1A_CREATED_UNVERIFIED_QUARANTINE`; preserve object/reference, no amend/reset/delete/rewrite. |
| 7C | Missing, mismatched, broad, expired, or unevaluable authority/close input is `GATEA_AUTHORITY_OR_CLOSE_UNBOUND_STOP` before socket open. Bound-but-unspent authority remains a safe idle half-state. |
| 8 | Pre-start non-PASS means no socket. After start, run only the preregistered `always` close. Safe-state PASS gives `HOST_SAFE_STOP`; inability or non-PASS gives `HOST_STATE_UNKNOWN_QUARANTINE`. No 8A PASS or later step. |
| 8A | Unsealed, incomplete, wrong-candidate, wrong-host, non-fresh, or unreadable final record is `GATEA_FINAL_RECORD_STOP`. Preserve raw evidence; never invent a field. |
| 9 | Any of the eight `UNKNOWN-until-admin-review` slots, crossover gap, missing tool identity, missing D026, or inability is `COMMIT1B_INPUT_JOIN_STOP`. No 1b creation. |
| 10 | Pre-create non-PASS is `COMMIT1B_NOT_STARTED_STOP`. Post-create uncertainty is `COMMIT1B_CREATED_UNVERIFIED_QUARANTINE`; preserve actual object/reference and stop before Step 11. |
| 11 | Any authority/object/scope mismatch or inability is `GRANT6_AUTHORITY_UNBOUND_STOP`. A verified 1b with unbound grant is a safe idle half-state. |
| 12 | Pre-start non-PASS means no socket. After start, preserve an immutable create-once PASS/STOP record. Unproved target close/mutation state is `HOST_STATE_UNKNOWN_QUARANTINE`; no retry or wider command. |
| 13 | Missing/duplicate/unresolved consumer is `TARGETED_FILL_CONSERVATION_STOP`. Preserve capture evidence. A procedure change invalidates the capture and requires a new chain/capture, not an in-place edit. |
| 14 | Pre-create non-PASS is `COMMIT2_NOT_STARTED_STOP`. Post-create uncertainty is `COMMIT2_CREATED_UNVERIFIED_QUARANTINE`; preserve object/reference and prohibit rewrite. |
| 14A | Missing/mismatched/unevaluable authority or close input is `WPI_PREHOST_AUTHORITY_OR_CLOSE_STOP`; Step 15 unreachable. |
| 15 | On non-PASS, execute only accepted branch-specific `always` actions. Safe close gives `HOST_SAFE_STOP`; unproved close gives `HOST_STATE_UNKNOWN_QUARANTINE`. Only Step-16 closure bookkeeping remains reachable. |
| 16 | PASS path may reach 17 only after Step-15 PASS. Non-PASS writes immutable P9-17 STOP and `PACKET9_STOP_CLOSED`, then ends; it does not clear quarantine. |
| 17 | Any missing/extra/duplicate/unresolved or single-form identity is `PRE_WPA_FREEZE_STOP`. |
| 18 | Missing exact command/runtime/universe or a RED arm that does not discriminate is `MANDATED_SUITE_CONTRACT_STOP`; suite does not start. |
| 19 | Tool/runtime/inability is STOP; completed observed unauthorized deviation is FAIL. Either makes Packet 10 non-authoritative and blocks 20. |
| 20 | Missing fresh owner ratification is `PACKET11_OWNER_STOP`; no carry-forward signature. |
| 21 | Missing/duplicate/unresolved member, different auditor bundle, or manifest-defined universe is `DISPATCH_BUNDLE_STOP`. |
| 22 | Failed paired preflight is `AUDIT2_NOT_DISPATCHED_STOP`; neither starts. Unexpected one-of-two start is `AUDIT2_PARTIAL_INVALID_STOP`; seal output as supplemental/non-accepting. |

### 6.2 Named chain half-states

| Half-state | Allowed closure |
|---|---|
| Verified 1a; no staging authority | Safe idle. 1a grants nothing. Obtain a separate exact owner authority or stop. |
| Gate-A authority bound; run not started | Safe idle; authority remains unspent and subject to its time/use limit. |
| Gate-A started; no final PASS | Run only accepted close. End `HOST_SAFE_STOP` or `HOST_STATE_UNKNOWN_QUARANTINE`. |
| Fresh final record sealed; 1b absent | Safe local evidence state. If the live process changes before capture, the later capture must STOP; the record is never rewritten. |
| 1b possibly created but not verified | `COMMIT1B_CREATED_UNVERIFIED_QUARANTINE`; no grant binding. |
| Verified 1b; grant #6 unbound | Safe idle; no socket. |
| Grant #6 bound; capture not started | Safe idle; grant remains unspent and exact-object scoped. |
| Capture started; no closed PASS | Preserve create-once STOP/partial record and classify safe/unknown host state; no retry. |

An inability to evaluate is always STOP. FAIL is reserved for a completed observation of deviant state. This follows the project's most expensive recurring defect rule. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-107`; `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`

## 7. Check inventory

For every check below, “independent” means the expected value is selected or recorded by a source other than the producer whose output is being checked. A hash/manifest emitted by the same builder is identity bookkeeping, not independent correctness evidence. Every check records input identities, exact command/procedure, stdout, stderr, rc, first divergence, and PASS/FAIL/STOP. A source or observation that cannot be read/evaluated yields STOP.

| ID | Check | Expected-value source | Independent? | What must be true for the check to go red / outcome |
|---|---|---|---|---|
| K01 | Governing-source freeze | Independently accepted source/authority manifest | Yes | Required source omitted, duplicated, substituted, changed, or single-form only → STOP. |
| K02 | Exact T0 candidate selection | Frozen T0 acceptance records and candidate Git object | Yes | Candidate/tree/artifact/manifest differs, either required auditor did not execute/accept, or evidence identity differs → STOP. |
| K03 | Stable-expectations row | K02 candidate plus accepted path/cmdline formulas | Yes | Any field fails grammar or derivation, or came from the Gate-A/TSV producer → STOP. |
| K04 | Allocation collision completeness | Complete independent ledger history, retained roots, authoritative allocation sources, accepted completeness policy | Yes | Known collision, omitted source class, unreadable member, canonical duplicate, or reparse redirect → STOP before mint. |
| K05 | Allocation append-only | Independently pinned predecessor ledger bytes/chain | Yes | Overwrite, truncate, insertion, reorder, hash break, duplicate sequence, or unavailable burn path → STOP/quarantine. |
| K06 | 1a no-live-value/schema check | Owner Option A and accepted banned-value/schema list | Yes | Any 1a data row contains MainPID/starttime/state/restart/running-exe/running-netns value; unparseable member → STOP. |
| K07 | 1a member conservation | Accepted force-inclusive path/role universe | Yes | Extra/hidden/missing/duplicate path or member without one role/disposition → STOP. Manifest cannot define this universe. |
| K08 | 1a exact object read-back | Reviewer-owned exact-byte freeze plus actual 1a Git object | Yes for expected bytes | Blob/byte/hash/dual-form/clean-state mismatch → pre-create STOP or post-create quarantine. |
| K09 | 1a authority fence | Owner Option A sentence | Yes | 1a says anything other than no host authority, grant-#6 prohibited, and separate Gate-A authority required → STOP. |
| K10 | Gate-A owner authority binding | Independently identified owner-authored Gate-A sentence | Yes | Sentence absent/expired/broad or exact candidate/host/A0..A9/channel/mutations/close/exclusions mismatch → STOP before socket. |
| K11 | Gate-A subject/host preflight | 1a stable expectations, exact run kit, disposable-host contract | Yes | Wrong candidate, wrong 1a, wrong run kit, KVM2 target, or host identity unavailable → STOP. |
| K12 | Gate-A safe-close preflight | Independently accepted C11 close contract | Yes | Missing branch close, unsafe/unevaluable final predicate, or run kit supplies its own expectation → STOP. |
| K13 | Fresh A-0..A-9 conservation | Independent A-0..A-9 contract and exact candidate | Yes | Any A-step missing/duplicated/unresolved, historical PASS reused, wrong bytes, or final state not safe → STOP/FAIL as observed. |
| K14 | Fresh final-record seal | Predeclared record schema/path plus OS create-once result | Yes for schema/path | Collision, write/fsync/close/reopen failure, byte/hash mismatch, or incomplete raw evidence → immutable STOP; never overwrite. |
| K15 | Candidate TSV provenance/copy | Sealed K14 final record | Yes relative to TSV builder | Any candidate field differs byte-for-byte, another source is cited, or the source record is mutable/unsealed → STOP. |
| K16 | Candidate stable cross-check | 1a/K02 expectations, not K14/K15 producer | Yes | Candidate/host/unit/cwd/cmdline differs from pre-run expectation → FAIL if observed, STOP if unevaluable. |
| K17 | 1b direct-parent ancestry | Independently frozen verified 1a OID | Yes | `1b^1` differs, extra parent exists, or ancestry cannot be read → STOP/quarantine. |
| K18 | Allowed delta and procedure immutability | 1a chain-control allowlist and 1a procedure blob map | Yes | Nonallowlisted path/field changes, missing required delta, or any procedure/schema/allocation/tool blob changes → STOP/quarantine. |
| K19 | SSH principal/key mapping | Admin decision plus server-side authoritative key/principal config | Yes | Concrete `SSH_TARGET` or key binding differs; absent config → STOP. Current slot is `UNKNOWN-until-admin-review`. |
| K20 | Account shell/identity | Authoritative provisioning/account record | Yes | UID/GID, shell path, kind, owner, mode, or digest differs; unavailable record → STOP. Current slot is `UNKNOWN-until-admin-review`. |
| K21 | Forced-command binding | Effective sshd/authorized-key configuration | Yes | Exact bytes differ, duplicate/ambiguous rule, or claimed `NONE` not proved → STOP. Current slot is `UNKNOWN-until-admin-review`. |
| K22 | Wrapper/process-chain binding | Admin-selected route plus independently verified config/tool identities | Yes | Missing hop, unbound executable, PATH lookup, prose ellipsis, or different exec chain → STOP. Current slot is `UNKNOWN-until-admin-review`. |
| K23 | Pre-`env` environment | Independent first-process/configuration record | Yes | Unexpected/missing entry, invalid encoding, startup hook/loader variable, or unreadability → STOP. Current slot is `UNKNOWN-until-admin-review`. |
| K24 | Initial cwd | Independent first-process/configuration record | Yes | First command starts elsewhere or cwd cannot be established before startup/import/`chdir` → STOP. Current slot is `UNKNOWN-until-admin-review`. |
| K25 | Descriptor set | Independent first-process FD inventory | Yes | Any mapping differs, extra writable FD survives, or complete enumeration is impossible → STOP. Current slot is `UNKNOWN-until-admin-review`. |
| K26 | Mutation-denial control | Admin-selected enforcement policy plus exact-chain D026 RED/GREEN | Yes | Deliberate content/config write succeeds, failure path writes, control starts too late/can be bypassed, or fd 1/2 unusable → STOP/BLOCK. Current slot is `UNKNOWN-until-admin-review`. |
| K27 | Infrastructure crossover | Independent sshd/PAM/audit/wrapper/runtime evidence | Yes | Authorized append triggers rotation/vacuum/out-of-store action or side-effecting hook; inability to observe → STOP. |
| K28 | Operator-tool identity | Independently frozen tool inventory | Yes | Absolute path/digest/kind differs or resolution uses PATH → STOP. |
| K29 | Final 1b member conservation | 1a allowlist plus accepted final path universe | Yes | Extra/hidden/missing/duplicate member or manifest-only universe → STOP. |
| K30 | No unresolved final input | Candidate/root/tool/allocation schemas accepted before 1b | Yes | Any `UNKNOWN`, `UNKNOWN-until-*`, placeholder, metavariable, unparsed byte, or absent required field → STOP. |
| K31 | Executable D026 and exact-byte review | Predeclared defects/mutations plus independent reviewer/auditor | Yes | Claimed regression test was not shown RED against pre-fix/mutation and GREEN on exact bytes, or review has a required finding/non-execution → STOP/BLOCK. |
| K32 | 1b object/read-back/clean state | Independent expected 1a/delta/input identities plus actual Git object | Yes | Parent, object, raw bytes, manifest, dual forms, current reference, index/worktree, or untracked set differs → pre-create STOP/post-create quarantine. |
| K33 | Grant-#6 binding | Owner D2/grant source plus verified K32 object | Yes | Target is 1a/different object, host/action/credential/exclusions differ, or input unevaluable → `GRANT6_AUTHORITY_UNBOUND_STOP`. |
| K34 | Immediate pre-H-6 clean/current check | K33 exact 1b OID and its committed package | Yes | HEAD/object/package changed, dirty/untracked state, recorder not exact, or first-line binding not to 1b → STOP before socket. |
| K35 | Capture create-once/close | Predeclared independent record path and accepted close contract | Yes | Collision, overwrite attempt, failed fsync/close/reopen, incomplete streams/rc, or host state not safely observable → immutable STOP/quarantine. |
| K36 | Targeted-fill/component conservation | Independent consumer inventory and canonical packet IDs | Yes | Any admitted value/member is dropped, duplicated, overwritten, or unresolved → STOP. |
| K37 | Full-suite/runtime contract | Owner-fixed full suite, frozen test inventory, independent node collection, exact runtime identities | Yes | Narrowed command, missing test, altered runtime/dependency/tool/fixture, unauthorized anomaly, or non-discriminating RED arm → STOP/FAIL. |
| K38 | Paired flagship dispatch readiness | Canonical roster plus independently frozen bundle/worktrees/routes | Yes | Either model/effort/route/suite access unavailable, bundle/SHA differs, worktree dirty, or one starts alone → no dispatch or partial-invalid STOP. |

The check design follows the governing rule: a check is real only when it has an input the checked producer does not control and a concrete world in which it goes red. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:30-63` No check above treats a producer-supplied hash, count, manifest, PASS token, or scope universe as independent proof of its own claim.
