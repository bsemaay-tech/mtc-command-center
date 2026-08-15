# Lane L3 — Packet 9 producer/evidence contract and honest price

Status: planning and producer-contract material for the Lead and owner. This document performs no host action, creates no gate verdict, grants no authority, and does not claim Packet 9 exists. The governing scope is itself T2 scoping and explicitly does not create a packet, contact a host, execute WP-I, dispatch Audit 2, or create authority. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:3-7`

## 1. Executive answer

There are two different meanings of “exists,” and they must not be collapsed:

- **Defined production contract:** 16 of the 17 Packet-9 components have a producing step in the governing scope; P9-15 is the sole producer gap. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:23-45`
- **Completed evidence instance:** none of the 17 is instantiated in the named Packet-9 skeleton; every component is still under a `PENDING` heading, and the skeleton explicitly asserts no measurements or terminal outcomes. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:3-11,22-268`
- The current work catalogue independently says the Stage-1 allocation, Commit 1, grant-#6 capture, targeted fills, and Commit 2 do not exist, and Packet 9 still lacks its host run and closure. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:7-17`

This document closes the **design-definition gap** by specifying a P9-15 producer and replayable evidence grammar. It does not create the producer executable or a P9-15 result.

The honest R15 labour price remains **NO SOURCED ESTIMATE**. The catalogue supplies no bounded Packet-9/WP-I price and asks for the P9-15 contract plus an estimate of the frozen operation plan; the only available Stage-1 numeric range expressly ends at Commit 2 and excludes later WP-I execution, closure, and Packet-9 evidence. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-70,86`

## 2. Component-by-component status

“Definition” means the governing scope names a producing step. “Instance” means completed evidence rather than a schema placeholder.

| ID | Definition status | Completed instance status | Evidence |
|---|---|---|---|
| P9-01 | **EXISTS — defined** | **DOES NOT EXIST — pending** | The allocation producer is defined, while every allocation field remains pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:25`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:22-37` |
| P9-02 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Commit-1 production is defined; the object ID, procedure, producer identity, grammar, and bindings remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:26`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:39-49` |
| P9-03 | **EXISTS — defined** | **DOES NOT EXIST — pending** | The grant-#6 capture step is defined; its capture record fields remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:27`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:51-61` |
| P9-04 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Commit-2 consumption/order production is defined; all identities and proofs remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:28`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:63-74` |
| P9-05 | **EXISTS — defined** | **DOES NOT EXIST — pending** | The local-root/op-01 producer is defined; local and remote topology results remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:29`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:76-83` |
| P9-06 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Commit-2 freeze and transport-preflight production are defined; all digests and the order result remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:30`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:85-94` |
| P9-07 | **EXISTS — defined** | **DOES NOT EXIST — pending** | The runner defines the op 01–12 record family; the per-op records and final summaries remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:31`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:96-121` |
| P9-08 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Op 04 is the defined P0 producer; the log identity, outcome, and rows 1–9 remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:32`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:123-135` |
| P9-09 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Op 05 is the defined RO producer; the log identity, outcome, and rows 1–23 remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:33`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:137-163` |
| P9-10 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Op 06 is the defined row-24 producer; its command record and classified result remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:34`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:165-171` |
| P9-11 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Closure synthesis is defined; every evidence-bound summary field remains pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:35`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:173-185` |
| P9-12 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Ops 07/08 are the defined close producers; both branch records remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:36`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:187-207` |
| P9-13 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Ops 09/10 are the defined retrieval producers; paths, transferred members, bytes, and hashes remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:37`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:209-217` |
| P9-14 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Ops 11/12 are the defined local-binding producers; both binding records remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:38`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:219-230` |
| P9-15 | **DOES NOT EXIST — producer gap** | **DOES NOT EXIST — pending** | The scope names no command, author, output contract, or producing point; the skeleton retains `PENDING-PRODUCER-CONTRACT` for every field. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:39,43-45`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:232-242` |
| P9-16 | **EXISTS — defined** | **DOES NOT EXIST — pending** | WP-I closure is the defined index producer; every index field and completeness check remains pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:40`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:244-257` |
| P9-17 | **EXISTS — defined** | **DOES NOT EXIST — pending** | Lead-owned closure is defined; disposition, chain, index identity, compliance, and hours remain pending. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:41`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:259-268` |

An older governance artifact describes a static security result, but it is explicitly absent from the frozen product candidate and must not be represented as candidate source. It therefore cannot be substituted for a current P9-15 record at Commit 2. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:364-374`

## 3. Proposed P9-15 producer contract

### 3.1 Producer identity and production point

The future executable producer shall consist of three evidence-tool artifacts, all committed no later than Commit 2 and all included in P9-06’s tool/input identity set:

1. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_runner.ps1` — create-once envelope, tool pin checks, process capture, and finalization.
2. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_inventory.py` — Git-object enumeration, dependency inventory, content-redacted secret scan, static egress inventory, conservation checks, and canonical output.
3. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json` — versioned signature categories, modeled network constructs, expected disposition grammar, and exact source-universe rules.

These names are a **proposed contract**, not a claim that the files currently exist. The governing scope requires the missing producer to be defined before use and places its execution after ops 09–12 retrieval/binding and before P9-11/P9-16/P9-17 closure production. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:117-118`

The author identity is **UNKNOWN** until the Lead assigns the implementation. What settles it: Commit 2 must record `producer_author`, reviewer/self-QA evidence, and the three frozen blob identities in P9-06. P9-06 already requires final support-script/tool-pin identities and a clean-current-HEAD order result before op 01. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:28-30`

Execution is a local-static Packet-9 step. It does not contact the host or use credentials; the prior A3 classification is `local-static` with no authority/budget, and it explicitly distinguishes static inventory from runtime egress capture or Ubuntu evidence. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:375-382,403-423`

### 3.2 Exact command shape

After P9-14 completes, the operator substitutes only the six bracketed, already-frozen inputs and executes this exact argv shape from a clean Commit-2 worktree:

```powershell
& '<PINNED_POWERSHELL_EXE>' -NoLogo -NoProfile -NonInteractive `
  -File '<REPO_ROOT>\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\p9_15_runner.ps1' `
  -RepoRoot '<REPO_ROOT>' `
  -SourceSha '<COMMIT_2_FULL_40_HEX_SHA>' `
  -OutputRoot '<OPERATOR_RECORD_ROOT>\packet9\p9-15' `
  -GitExe '<PINNED_GIT_EXE>' `
  -PythonExe '<PINNED_PYTHON_EXE>'
```

The expanded argv, not the template above, is written verbatim to `command.json`. The source SHA is Commit 2 because Commit 2 freezes the final successor/runkit and the missing inventory is ordered after that freeze but before closure. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:112-118`

The runner invokes the child in this exact shape after verifying its own blob, the producer blob, the policy blob, and the pinned Git/Python executable identities against the Commit-2/P9-06 record:

```text
<PINNED_PYTHON_EXE> -I -B <REPO_ROOT>\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\p9_15_inventory.py produce --repo <REPO_ROOT> --source-sha <COMMIT_2_FULL_40_HEX_SHA> --policy-ref MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json --output-root <OPERATOR_RECORD_ROOT>\packet9\p9-15
```

The child must read subject content only through `git ls-tree`/`git cat-file` at `SOURCE_SHA`; it must not analyze worktree product bytes. This prevents a dirty or differently normalized checkout from impersonating the frozen Git objects, a problem already documented for the lock’s raw Git-blob hash versus a CRLF checkout hash. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:388-402`

### 3.3 Inputs and preconditions

| Input | Contract |
|---|---|
| `REPO_ROOT` | Absolute local repository path. Git object reads only; no index write. |
| `SOURCE_SHA` | Full 40-lowercase-hex Commit-2 commit ID; must resolve as a commit and equal the Commit-2 ID in P9-04/P9-06. The Commit-2 identity/order requirement is established upstream. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:28-30` |
| `OUTPUT_ROOT` | Exactly `<OPERATOR_RECORD_ROOT>\packet9\p9-15`; must not exist. Creation is atomic and create-once. Existing-path collision is `STOP`, never overwrite. No-clobber evidence paths are the standing evidence convention. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:1266-1277` |
| Producer/policy identities | Relative paths above plus Commit-2 blob OIDs and raw SHA-256 values; no unresolved placeholder is permitted. P9-06 already requires support-script and tool-pin identities. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:28-30` |
| Tool identities | Absolute PowerShell, Git, and Python paths; version, file bytes, and SHA-256; each must match P9-06 before subject output is interpreted. The repo defect catalogue requires every executed instrument to be dynamically bound, not merely declared. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:860-895` |
| Environment | Clean child environment containing only `SystemRoot`, `WINDIR`, `TEMP`, `TMP`, and locale values recorded in `environment.json`; proxy and credential variables are removed by name without reading values. The producer opens no socket and invokes no package installer. |
| Product paths | `IBKR_PAPER_BRIDGE/requirements.in`, `IBKR_PAPER_BRIDGE/requirements.lock`, and `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py` at `SOURCE_SHA`. Those are the candidate-side sources named for the dependency predicate. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:367-374` |

If any precondition cannot be evaluated, the runner emits `STOP`/rc 3 rather than a host- or source-state `FAIL`. The repo’s design rule distinguishes inability to observe from an observed deviation and requires status/stderr/completeness to be adjudicated before stdout is interpreted. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-107,368-420`

### 3.4 Exact scanned universe

The producer declares the universe once from `git ls-tree -r -z --full-tree --long SOURCE_SHA` and gives every regular tracked blob one terminal disposition; no worktree, untracked, ignored, history-only, process-environment, registry, credential-store, shell-history, or remote-host content is claimed. The earlier secret-scan contract covered every non-binary tracked blob in one exact frozen tree and explicitly disclosed the excluded domains. `52f33bdcb8470057a7131092d8a985ed03d7784b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:44-59,87-92`

The three sub-universes are:

1. **Tree/secret universe:** every regular tracked blob in the full Commit-2 tree. Every blob receives `scanned_text` or `excluded_binary` with a reason; every excluded binary remains counted and hashed.
2. **Dependency universe:** `requirements.in`, `requirements.lock`, `verify_lock.py`, and every parsed direct/locked member. The prior contract requires exact `==` pins, at least one SHA-256 artifact hash per distribution, and rejection of URLs, VCS references, and index overrides. `52f33bdcb8470057a7131092d8a985ed03d7784b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:20-42`
3. **Egress universe:** every text blob under `IBKR_PAPER_BRIDGE/`, not only files with known hits. Each receives `analyzed`, `not_executable_or_network_relevant`, or `unresolved`; zero facts plus PASS is forbidden. The analyzer must STOP on an unconsumed network-capable command, option, redirection, nested sink, import/call form, or endpoint-bearing construct. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:899-929,933-967`

The policy contains the existing high-confidence secret categories—private-key blocks, AWS, GitHub, Slack, OpenAI, Anthropic, xAI, Telegram bot tokens, and a 32-byte Ethereum private-key form—but records only category counts and paths, never matched text. `52f33bdcb8470057a7131092d8a985ed03d7784b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:44-54,196-225`

The egress output uses the prior six-class inventory only as a seed to be re-derived at Commit 2: runtime-required, runtime-optional, install-time-only, local-listener, forbidden/unselected, and unused-setting/no-endpoint. No prior destination or count is copied as a current result. `52f33bdcb8470057a7131092d8a985ed03d7784b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:94-108`

### 3.5 Output files and canonical grammar

All text is UTF-8 without BOM and LF-terminated. JSON uses sorted keys, no insignificant whitespace, lowercase hex, forward-slash relative paths, and one terminal LF. JSONL rows are sorted by `(record, path, stable_id)` and each line is one canonical JSON object.

The create-once root contains exactly these files:

| File | Required content |
|---|---|
| `command.json` | Expanded runner argv and child argv as arrays; cwd; start/end UTC; author identity from frozen metadata; execution-operator identity; no command template. |
| `environment.json` | Sorted environment-name/value records for the clean allowlist plus sorted removed variable **names**; no removed value. |
| `tools.json` | PowerShell/Git/Python absolute paths, versions, bytes, SHA-256, and producer/policy path/blob/SHA identities. |
| `source.json` | `source_sha`, commit object type, full tree OID, product-subtree OID, policy blob, producer blob, and universe-count fields derived from enumeration. |
| `universe.jsonl` | One `FILE` row for every regular tracked blob: `path`, `mode`, `blob_oid`, `bytes`, raw-content `sha256`, `content_class`, `secret_disposition`, `egress_disposition`, and `reason`. |
| `dependencies.jsonl` | One `DEPENDENCY` row per locked member and one `DIRECT_DEPENDENCY` row per direct member: stable canonical name, version/specifier, sorted hashes, source path/line, terminal disposition; plus source-file blob identities. |
| `secret_scan.jsonl` | One `SECRET_CATEGORY` row per policy category even when zero: `category`, `path_hits`, sorted `paths`; never matched text. |
| `egress.jsonl` | One `EGRESS` row per resolved class/destination/activation path: stable ID, class, destination, protocol/port, activation predicate, source path/blob/line/column/construct, credential **names only**, and disposition. Expected absence is an explicit row, not missing output. |
| `unresolved.jsonl` | Zero or more `UNRESOLVED` rows: axis, stable member identity, path, syntax/construct, and reason token. The file exists and is empty on a complete modeled scan. |
| `summary.json` | Schema `p9-15/v1`; source SHA; all derived counts; dependency/secret/egress axis results; overall class/rc/reason; scanned limitations; deterministic core SHA-256. |
| `stdout.bin` | Exact child stdout bytes. |
| `stderr.bin` | Exact child stderr bytes, content-redacted. Empty on PASS. |
| `rc.txt` | Exactly `0\n`, `1\n`, or `3\n`. |
| `elapsed_ms.txt` | One base-10 non-negative integer and LF; measured, never estimated. |
| `SHA256SUMS.txt` | Sorted lowercase SHA-256, two spaces, relative path for every preceding file; no self-entry. |
| `COMPLETE.json` | Written last: schema, source SHA, result class/rc/reason, `SHA256SUMS.txt` bytes/SHA-256, `summary.json` bytes/SHA-256, and final file count. Its existence distinguishes a finalized record from a partial directory. |

`universe.jsonl` enforces the repo conservation rule: input members equal scanned/analyzed plus explicitly excluded plus unresolved, with one and only one terminal disposition per blob. Silent filtering, duplicate-key overwrite, or unexplained count drift is `STOP`. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`

The child stdout grammar is exactly four LF-terminated ASCII lines in this order:

```text
P9_15_BEGIN schema=p9-15/v1 source_sha=<40_lower_hex>
P9_15_COUNTS files_total=<n> text_scanned=<n> binary_excluded=<n> dependencies=<n> secret_category_path_hits=<n> egress_rows=<n> unresolved=<n>
P9_15_OUTPUT relative_path=summary.json bytes=<n> sha256=<64_lower_hex>
P9_15_RESULT class=<PASS|FAIL|STOP> rc=<0|1|3> reason=<UPPER_SNAKE_TOKEN>
```

### 3.6 Result classification

- `PASS` / rc 0 means enumeration completed; every admitted member has one terminal disposition; dependency grammar is valid; every content-redacted secret category has zero path hits in the declared text universe; all egress constructs are resolved; no forbidden activation path is present; and no unresolved row exists.
- `FAIL` / rc 1 means evaluation completed and observed at least one source deviation: invalid/unpinned dependency, a secret category/path hit, or a resolved forbidden/unexpected egress activation. Match values remain suppressed.
- `STOP` / rc 3 means evaluation was incomplete or untrustworthy: source/tool/blob mismatch, output collision, Git/helper/read/decode error, unsupported grammar, malformed policy, duplicate/conservation error, partial traversal, timeout, or any unclassified helper status.

STOP takes precedence over FAIL when the complete universe was not evaluated. This follows the repo rule that a complete successful probe is required before output is interpreted as a state result. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:414-420`

### 3.7 Independent verifiability

Someone who did not run the producer can verify the result because the evidence binds the exact command, clean environment, tool bytes, producer/policy blobs, Commit-2 source SHA/tree, every admitted blob, every terminal disposition, every output’s bytes/SHA-256, and a final create-once manifest. These are the missing verifiability fields required by P9-15. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:39`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:232-242`

The independent verifier performs four checks:

1. Recompute `SHA256SUMS.txt`, `COMPLETE.json` links, and the P9-16 path/bytes/SHA entries without executing the producer.
2. Re-enumerate `SOURCE_SHA` with Git object commands and compare the sorted `(path, mode, blob_oid, bytes, sha256)` universe byte-for-byte.
3. Run the same frozen producer from a fresh detached Commit-2 worktree into a different create-once root and compare the deterministic core files (`source.json`, `universe.jsonl`, `dependencies.jsonl`, `secret_scan.jsonl`, `egress.jsonl`, `unresolved.jsonl`, and the deterministic portion of `summary.json`) byte-for-byte.
4. Execute preregistered falsifications before relying on the producer: replace/remove one declared instrument; add one secret-signature fixture whose match text must never print; add one unknown/nested network sink that must STOP; introduce one duplicate/canonicalized dependency; and make a blob read fail. The real top-level caller must turn each mutation red before the unmutated source is green. The repo requires real RED/GREEN output for regression evidence and specifically requires unknown static-analysis forms to become unresolved/STOP. `AGENTS.md:D026 — FALSIFIED-TEST RULE`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687,886-895,919-929,957-967`

The exact replay/verification command shape is:

```text
<PINNED_PYTHON_EXE> -I -B <FRESH_COMMIT2_WORKTREE>\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\p9_15_inventory.py verify --repo <FRESH_COMMIT2_WORKTREE> --source-sha <COMMIT_2_FULL_40_HEX_SHA> --policy-ref MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json --evidence-root <ORIGINAL_P9_15_OUTPUT_ROOT>
```

## 4. Dependency order and host-access boundary

### 4.1 Established partial order

The governing order is:

```text
exact-byte acceptances
  -> P9-01
  -> P9-02
  -> P9-03
  -> P9-04 + P9-06
  -> Commit-2 order/preflight
  -> P9-05 + begin P9-07 (ops 01-03)
  -> P9-08 (op 04)
  -> P9-09 (op 05, only while sequence_ok)
  -> P9-10 (op 06, only while sequence_ok)
  -> P9-12 (always ops 07/08 for any established branch)
  -> P9-13 (ops 09/10)
  -> P9-14 + complete P9-07 (ops 11/12)
  -> P9-15
  -> P9-11 + P9-16 + P9-17 closure family
```

The first five Stage-1 steps and the exact order check are specified at scope lines 108–113; transport/retrieval/binding and the closure-family order are specified at lines 114–118. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:106-118`

The exact byte-finalization order inside the final `P9-11 + P9-16 + P9-17` closure family is **UNKNOWN**. P9-16 requires no unindexed retained file, while P9-17 must reference the immutable P9-16 index identity; the scope groups them at closure without specifying how to avoid a closure/index self-reference. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:35,40-41,118`

What settles that unknown: a Lead-authored closure-finalization procedure must define either (a) P9-16’s exact retained-file universe and a separate packet-level final manifest that indexes P9-16 and P9-17, or (b) another acyclic two-level manifest scheme. No component may be called final while a retained file is silently outside its declared universe.

### 4.2 Local versus authorized host access

| Component | Boundary | Basis |
|---|---|---|
| P9-01 | **Local** | The Stage-1 estimate source classifies allocation as local work/no gate. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:66` |
| P9-02 | **Local** | Commit-1 authoring is classified local work/no gate. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:67` |
| P9-03 | **Authorized host access required** | The capture is classified as blocked on authorized host access. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:68` |
| P9-04 | **Local** | Targeted consumption/build/composite work and Commit-2 proof/freeze are local. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:69-70` |
| P9-05 | **Mixed** | Local create-once root plus remote op-01 allocation. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:29`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:2` |
| P9-06 | **Local** | Commit-2 freeze plus local transport preflight. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:30` |
| P9-07 | **Mixed** | It spans ops 01–12: SSH/SCP/TCP operations through op 10 and local binds in ops 11/12. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:1-13` |
| P9-08 | **Authorized host access required** | P0 is SSH op 04. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:5` |
| P9-09 | **Authorized host access required** | RO is SSH op 05. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:6` |
| P9-10 | **Authorized host/network access required** | Row 24 is an operator-side TCP connection to the staging host. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:7` |
| P9-11 | **Local after host evidence** | It synthesizes already captured P0/RO/op-06 results after local binding. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:35` |
| P9-12 | **Authorized host access required** | Both close records are SSH ops 07/08. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:8-9` |
| P9-13 | **Authorized host/network access required** | Both evidence-tree retrievals are SCP ops 09/10. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:10-11` |
| P9-14 | **Local** | Both remote/local comparisons are local-bind ops 11/12 with no host contact. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:12-13`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:38` |
| P9-15 | **Local** | A3 is static/local only and is not runtime capture or host proof. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:375-382,403-423` |
| P9-16 | **Local after all retained evidence is finalized** | The index is produced at WP-I closure after both local binds and record finalization. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:40` |
| P9-17 | **Local, Lead-owned** | The closure record is Lead-owned after retrieval, local binding, and indexing. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:41` |

The narrow host grant is approved but not yet spendable at the recorded state: Commit 1 and the allocation record do not exist, and the decision says host contact before those exact committed bytes would fall outside the grant. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-52`

## 5. Per-component estimates

The table distinguishes a sourced upstream range from an R15 price. R15 consumes R09–R14 rather than recreating them, so upstream hours must not be added to R15. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54,170-174,207`

| ID | Honest estimate | Included in R15? | What would produce a missing source |
|---|---|---|---|
| P9-01 | **1–2 h sourced** | No; R09/upstream | The allocation range is sourced directly. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:66` |
| P9-02 | **1–2 h sourced** | No; R10/upstream | The Commit-1 range is sourced directly. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:67` |
| P9-03 | **0.5–1.5 h sourced once access/inputs exist** | No; R12/upstream | The capture range is sourced directly and is conditional on access/inputs. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:68` |
| P9-04 | **NO SOURCED DISJOINT ESTIMATE.** A shared **3.5–7 h** source bucket covers P9-04 and P9-06 work together: 2–4 h consumption/build/composite plus 1.5–3 h final proof/review/Commit 2. | No; R13/R14 upstream | A component-tagged rehearsal/time ledger separating P9-04 work from P9-06 work. The source does not disaggregate them. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:69-70`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:28,30` |
| P9-05 | **NO SOURCED ESTIMATE** | Yes, to the extent produced by root creation/op 01 | A frozen-plan rehearsal or first authorized execution that records operator active labour separately from op-01 elapsed time. The plan defines the operation but gives no hour price. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:1-2`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-06 | **NO SOURCED DISJOINT ESTIMATE.** It shares the upstream 3.5–7 h P9-04/P9-06 bucket. | No; R13/R14 upstream | A component-tagged rehearsal/time ledger separating transport-input/preflight work from P9-04 consumption/order work. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:69-70`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:28,30` |
| P9-07 | **NO SOURCED ESTIMATE** | Yes | One exact frozen-plan rehearsal/authorized run plus closure labour ledger; use the required per-op `elapsed_ms` records for machine time and separately record operator active time. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:31`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-08 | **NO SOURCED ESTIMATE** | Yes | Timed exact op-04 execution/rehearsal plus operator evidence-review time. The source defines the op, not hours. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:5`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-09 | **NO SOURCED ESTIMATE** | Yes | Timed exact op-05 execution/rehearsal plus operator evidence-review time. The source defines the op, not hours. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:6`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-10 | **NO SOURCED ESTIMATE** | Yes | Timed exact op-06 execution/rehearsal plus classification/review time. The only numeric field in the plan row is the probe timeout, not a labour estimate. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:7`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-11 | **NO SOURCED ESTIMATE** | Yes | A local closure dry run against a complete synthetic/previously captured evidence tree, with active authoring and verification time recorded under P9-11. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:35`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-12 | **NO SOURCED ESTIMATE** | Yes | Timed exact ops 07/08 and operator review, preserving branch-specific values rather than averaging them. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:8-9`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-13 | **NO SOURCED ESTIMATE** | Yes | Timed exact ops 09/10, with transferred byte/file counts and operator review time recorded. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:10-11`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-14 | **NO SOURCED ESTIMATE** | Yes | Timed exact local-bind ops 11/12 plus review time; record P0 and RO separately. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:12-13`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-15 | **NO SOURCED ESTIMATE** | Yes | After this contract is frozen: time producer/policy implementation, RED/GREEN falsification, one full Commit-2-source production run, and one fresh independent replay. Prior focused test durations are not a full P9-15 producer/labour measurement and must not be substituted. `52f33bdcb8470057a7131092d8a985ed03d7784b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:228-245`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-16 | **NO SOURCED ESTIMATE** | Yes | Freeze the exact index/finalization grammar, then time a complete local indexing and independent recomputation over a realistic retained tree. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:40`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54` |
| P9-17 | **NO SOURCED ESTIMATE** | Yes | Freeze the acyclic closure/final-manifest procedure, then time one complete Lead closure and independent field/hash check; book actual hours prospectively. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:41`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:259-268` |

The upstream sourced ranges total **6–12.5 h** by arithmetic (1–2 + 1–2 + 0.5–1.5 + 2–4 + 1.5–3), but that total ends at the Stage-1 freeze and is not an R15 estimate. The source expressly excludes later WP-I execution/closure and Packet-9 host evidence. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:66-70,86`

## 6. R15 pricing disposition

**R15 — NO SOURCED ESTIMATE.** No defensible numeric lower or upper labour bound is present for the R15-only set: P9-05’s op-01 share; P9-07 through P9-17 production/closure; and the new P9-15 producer implementation, falsification, execution, and replay. The current catalogue says exactly that a bounded Packet-9/WP-I price is not supplied. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54`

What will turn R15 into a sourced range:

1. Freeze and implement the P9-15 producer contract before Commit 2, including executable RED/GREEN falsifications.
2. Freeze the P9-11/P9-16/P9-17 acyclic closure/final-manifest procedure.
3. Execute one exact frozen-plan rehearsal where safe, then use the first authorized exact run for host-dependent measurements; record per-op machine elapsed time and component-tagged operator active labour separately.
4. Time one complete P9-15 production plus independent replay and one complete closure/index recomputation.
5. Publish a measurement record listing component, actor, start/end UTC, active labour, machine elapsed time, wait time, overlap group, command/evidence path, bytes, SHA-256, and source SHA. Sum active labour once across overlapping components; do not add shared P9-04/P9-06 work or upstream R09–R14 into R15.

Until that record exists, any numeric R15 range would be invented rather than sourced.

## 7. Explicit unknowns for the Lead

- **Producer author/reviewer identity: UNKNOWN.** Settled by an assignment and frozen identity record before Commit 2. The current scope explicitly says the author is missing. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:39`
- **P9-11/P9-16/P9-17 byte-finalization order: UNKNOWN.** Settled by an acyclic closure/final-manifest procedure as described in §4.1. The scope groups those outputs at closure but does not state their internal finalization order. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:118`
- **R15 numeric labour range: NO SOURCED ESTIMATE.** Settled only by the component-tagged timed procedure in §6. The catalogue supplies no bounded Packet-9/WP-I price. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54`
- **Actual P9-15 result and counts: UNKNOWN.** Settled only by executing the frozen producer at the real Commit-2 SHA; the skeleton forbids inventing byte counts, file counts, SHA-256 values, or outcomes. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:7-11,232-242`

No acceptance decision or authorization is made here.
