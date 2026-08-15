# P9-15 frozen-SHA inventory producer — implementable specification

Status: **SPECIFICATION ONLY — NOT IMPLEMENTED, NOT EXECUTED, NOT ACCEPTED, AND NOT AUTHORIZED**.

This document specifies the missing P9-15 local-static producer. P9-15 must record the exact command, scanned universe, stdout/stderr/rc, classification, output path/bytes/SHA-256, and source SHA; the governing packet scope presently identifies P9-15 as the sole component without a producing step. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:39-45`

The production point is after P9-14 retrieval/binding and before P9-11/P9-16/P9-17 closure. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:114-118`; `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:176-196`

The step is local and static. It reads Git objects only. It performs no host, network, credential, service, deployment, broker/exchange, order, ARM, TESTNET/mainnet, Pine, parity, MTC, trading, merge, push, or economic action. The static/local boundary is established at `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:364-382,403-423`, and the current work catalogue grants no authority at `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:1-17,200-212`.

Normative words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** define implementation requirements in this document. They are specification decisions, not claims that an implementation or result exists.

## 1. Deliverables and trust boundary

The implementation consists of exactly these three Commit-2-tracked artifacts:

1. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_runner.ps1`
2. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_inventory.py`
3. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json`

Those artifact names and their roles are inherited from the producer contract. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:43-53`

The runner is the evidence-envelope owner. It validates the invocation and pins, starts the child, captures raw process streams and rc, classifies wrapper failures, writes the run envelope, hashes the finalized files, and writes `COMPLETE.json` last. The Python child is the semantic producer. It enumerates Git objects, parses the declared dependency sources, performs the content-redacted scan, derives the static egress inventory under the frozen policy, enforces conservation, writes the deterministic core, and emits the four-line child protocol. The policy is data, not executable code.

P9-06 MUST bind the actual PowerShell, Git, Python, runner, inventory producer, and policy bytes before the process is launched. A self-check performed after an untrusted runner starts is supplemental rather than the root binding event; the repository rule requires every declared instrument to be connected to the real production caller. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:860-895`

## 2. Exact runner interface

### 2.1 Process argv

The caller MUST invoke the pinned PowerShell executable with the following expanded argv, in exactly this order:

```powershell
& '<PINNED_POWERSHELL_EXE>' -NoLogo -NoProfile -NonInteractive `
  -File '<REPO_ROOT>\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\p9_15_runner.ps1' `
  -RepoRoot '<REPO_ROOT>' `
  -SourceSha '<COMMIT_2_FULL_40_LOWER_HEX_SHA>' `
  -OutputRoot '<OPERATOR_RECORD_ROOT>\packet9\p9-15' `
  -GitExe '<PINNED_GIT_EXE>' `
  -PythonExe '<PINNED_PYTHON_EXE>' `
  -PinRecord '<ABSOLUTE_P9_06_PIN_RECORD_JSON>' `
  -PinRecordSha256 '<64_LOWER_HEX_SHA256>'
```

The first six substitutions preserve the contract's proposed command surface. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:59-73`

`-PinRecord` and `-PinRecordSha256` are mandatory clarifications. The contract requires comparison against P9-06 but gives the runner no path or expected digest for that evidence. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:75-95` The two added arguments remove that ambiguity: the path locates the record, and the separately supplied digest prevents the located record from authenticating itself.

The runner MUST use advanced-parameter binding with all eight named parameters mandatory. It MUST reject positional arguments, aliases, repeated parameters, unknown parameters, empty strings, wildcard expansion, and trailing operands as `STOP/3/ARGUMENT_ERROR`.

Argument requirements are exact:

| Parameter | Required grammar |
|---|---|
| `RepoRoot` | Existing absolute Windows directory. After full-path resolution, it MUST equal `git -C <RepoRoot> rev-parse --show-toplevel` under Windows ordinal-ignore-case comparison. It MUST NOT end with a separator except for a drive root, and a drive root is forbidden. |
| `SourceSha` | Exactly `[0-9a-f]{40}`. It MUST resolve to a Git object of type `commit`, and `git rev-parse <SourceSha>^{commit}` MUST return the identical 40-character value. |
| `OutputRoot` | Absolute path whose final two components are exactly `packet9\p9-15`. It and any finalization target of the same name MUST NOT exist. Its parent MUST already exist. |
| `GitExe`, `PythonExe` | Existing absolute regular-file paths, with no wildcard. Their raw bytes, length, SHA-256, and normalized version output MUST match the pin record. |
| `PinRecord` | Existing absolute regular-file path outside `OutputRoot`. It is read as raw bytes once. |
| `PinRecordSha256` | Exactly `[0-9a-f]{64}` and equal to SHA-256 of the raw `PinRecord` bytes. |

`SourceSha` is Commit 2 because the inventory is ordered after the Commit-2 freeze and before closure. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:112-118`

### 2.2 Pin-record grammar

`PinRecord` MUST be UTF-8 without BOM, canonical JSON under §5, with one terminal LF and this exact top-level schema:

```json
{"artifacts":[{"blob_oid":"<40_lower_hex>","bytes":0,"kind":"inventory","path":"MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_inventory.py","sha256":"<64_lower_hex>"},{"blob_oid":"<40_lower_hex>","bytes":0,"kind":"policy","path":"MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json","sha256":"<64_lower_hex>"},{"blob_oid":"<40_lower_hex>","bytes":0,"kind":"runner","path":"MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_runner.ps1","sha256":"<64_lower_hex>"}],"producer_author":"<nonempty_identity>","reviewer_identity":"<nonempty_identity>","schema":"p9-15-pins/v1","source_sha":"<40_lower_hex>","tools":[{"bytes":0,"kind":"git","path":"<absolute_path>","sha256":"<64_lower_hex>","version":"<normalized_version>"},{"bytes":0,"kind":"powershell","path":"<absolute_path>","sha256":"<64_lower_hex>","version":"<normalized_version>"},{"bytes":0,"kind":"python","path":"<absolute_path>","sha256":"<64_lower_hex>","version":"<normalized_version>"}]}
```

The displayed zero byte counts are grammar examples only; each real `bytes` value MUST be the measured non-negative raw-file length. `artifacts` MUST be sorted by `kind` and contain exactly `inventory`, `policy`, and `runner`. `tools` MUST be sorted by `kind` and contain exactly `git`, `powershell`, and `python`. No additional keys are permitted at any level. `producer_author` and `reviewer_identity` MUST NOT contain `UNKNOWN`, `PENDING`, angle-bracket placeholders, CR, LF, or NUL.

The actual producer author and reviewer are **UNKNOWN** in the available source. What settles them is a Lead assignment frozen into P9-06/Commit 2. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:53-55,266-271`

`version` is exact normalized stdout from the preregistered version probe: decode UTF-8 strictly, convert CRLF to LF, remove exactly one terminal LF, and reject NUL or more than one line. The version probes are `git --version`, `python --version`, and `$PSVersionTable.PSVersion.ToString()` for the already running PowerShell. Any nonzero probe, stderr, decode error, multiline result, or mismatch is `STOP/3/TOOL_IDENTITY_MISMATCH`.

### 2.3 Stdin

Runner stdin is **no input**. The caller MUST attach an empty/EOF stream. The runner MUST never read stdin and MUST start the child with stdin closed. Any future stdin-dependent mode is a schema-breaking `p9-15/v2` change.

### 2.4 Environment

The caller MUST start the runner with exactly these environment names and no others:

```text
LANG=C
LC_ALL=C
SystemRoot=<existing absolute Windows directory>
TEMP=<existing absolute local temporary directory>
TMP=<same bytes as TEMP>
TZ=UTC
WINDIR=<same resolved directory as SystemRoot>
```

Names are compared Windows ordinal-ignore-case; the canonical spellings above are written to evidence. `SystemRoot`, `WINDIR`, `TEMP`, and `TMP` are run-envelope data and are never copied into a deterministic core file. Proxy, credential, Python, Git, shell-startup, package-index, user-profile, and home variables are absent; values of removed variables are never read or recorded. The contract requires a clean allowlist and removal of proxy and credential variables by name without reading their values. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:83-95`

The runner MUST pass the same seven-name environment to the child and MUST use `UseShellExecute=false`; it MUST invoke all executables by the pinned absolute path. No `PATH` lookup, shell command string, package installer, module download, or socket operation is permitted.

### 2.5 Cwd

Before launch, the caller's cwd MUST be `RepoRoot`. The runner MUST reject any other cwd as `STOP/3/CWD_MISMATCH`; it MUST then set the child cwd to the same resolved `RepoRoot`. Paths placed in deterministic output are nevertheless Git-relative and use `/`, so replay from a different absolute checkout root does not alter compared bytes.

### 2.6 Exact child argv

After pin and source preflight, the runner MUST invoke the child directly, without a shell, in this exact argv order:

```text
<PINNED_PYTHON_EXE>
-I
-B
<REPO_ROOT>\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\p9_15_inventory.py
produce
--repo
<REPO_ROOT>
--source-sha
<COMMIT_2_FULL_40_LOWER_HEX_SHA>
--policy-ref
MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json
--output-root
<PRIVATE_STAGING_DIRECTORY>
--git-exe
<PINNED_GIT_EXE>
--pin-record
<ABSOLUTE_P9_06_PIN_RECORD_JSON>
--pin-record-sha256
<64_LOWER_HEX_SHA256>
```

`--git-exe` and the two pin-record operands are mandatory because the child must use the pinned Git binary and recheck its actual input binding; a bare `git` lookup is forbidden. The original contract requires Git-object reads and pinned-tool verification but its illustrative child argv did not carry those values. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:75-81,90-95`

The staging-directory name MAY contain a random nonce. It MUST be a sibling of final `OutputRoot`, MUST NOT pre-exist, MUST never appear in a deterministic core file, and MUST be absent after successful atomic finalization. A left-behind staging directory is partial evidence, never a P9-15 result.

## 3. Frozen source universe and semantic inputs

The child MUST read subject and policy content only with the pinned Git executable at `SourceSha`; it MUST NOT read product or policy bytes from the worktree. Raw Git-blob hashing is required because worktree line-ending conversion can produce a different byte stream from the frozen blob. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:388-402`; `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:75-81`

The exact enumeration command is the following argv, executed directly:

```text
<PINNED_GIT_EXE> -C <REPO_ROOT> ls-tree -r -z --full-tree --long <SOURCE_SHA>
```

The parser MUST consume the complete NUL-delimited stdout only after rc is 0 and stderr is empty. It MUST accept regular tracked blob modes `100644` and `100755`. It MUST count but not admit symlink mode `120000`, gitlink mode `160000`, and any other non-regular mode; an unknown mode is `STOP/3/TREE_MODE_UNSUPPORTED`. Every admitted blob MUST receive exactly one `FILE` row. Every blob body is read with exact argv `<GIT_EXE> -C <REPO_ROOT> cat-file blob <BLOB_OID>` and hashed as raw bytes. Helper status is adjudicated before stdout is interpreted. The status-before-output and conservation rules are established at `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-107,414-420,933-967`.

The three sub-universes are:

- **Tree/secret:** every admitted regular blob in the full Commit-2 tree. A blob is `text_utf8` only when it has no NUL byte and decodes as strict UTF-8; otherwise it is `binary` with reason `NUL_BYTE` or `NON_UTF8`. Every `text_utf8` blob is scanned. Every binary blob remains counted and hashed.
- **Dependency:** exactly `IBKR_PAPER_BRIDGE/requirements.in`, `IBKR_PAPER_BRIDGE/requirements.lock`, and `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py`, plus each parsed direct and locked member. These are the candidate-side sources named for the predicate. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:364-374`
- **Egress:** every `text_utf8` blob below `IBKR_PAPER_BRIDGE/`. Each receives exactly one of `analyzed`, `not_executable_or_network_relevant`, or `unresolved`. Zero resolved facts does not justify PASS; unsupported network-capable syntax is unresolved/STOP. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:899-929`

The lock predicate is exact: each locked distribution must have one exact `==` version and at least one SHA-256 artifact hash, and URL, VCS, and index-override forms are forbidden. `52f33bdcb8470057a7131092d8a985ed03d7784b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:20-42`

Dependency canonical names are computed by lowercasing ASCII and replacing every maximal run of `-`, `_`, or `.` with `-`. The stable identity of a member includes its source path and one-based source line before canonicalization; two admitted members that collapse to the same canonical dependency identity are not overwritten and cause `STOP/3/DUPLICATE_IDENTITY`.

The policy MUST contain exactly the nine sourced secret categories: private-key block, AWS access key, GitHub token, Slack token, OpenAI token, Anthropic token, xAI token, Telegram bot token, and 32-byte Ethereum private-key form. Matches record category and path only; matched text, line content, offsets, and surrounding bytes MUST NOT be emitted. The sourced categories and regex forms are at `52f33bdcb8470057a7131092d8a985ed03d7784b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:44-54,196-225`.

The policy MUST expose the six egress classes `runtime-required`, `runtime-optional`, `install-time-only`, `local-listener`, `forbidden-unselected`, and `unused-setting-no-endpoint`. They are classification labels, not expected current results; all current rows are re-derived at `SourceSha`. The six-class seed and the prohibition on copying prior counts/destinations are established at `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:107-109`.

The exhaustive egress grammar matrix—recognized languages, commands, APIs, options, redirections, nested forms, endpoint extractors, and activation-predicate rules—is **UNKNOWN** because the contract names that policy content but does not supply its bytes. What settles it is the actual canonical `p9_15_policy.json`, reviewed and frozen at Commit 2. The generic implementation MUST treat an absent category, unknown policy key, unconsumed network-capable token, unsupported nested form, or non-exhaustive policy declaration as `UNRESOLVED` and `STOP/3/POLICY_COVERAGE_INCOMPLETE`; it MUST NOT guess or silently omit the construct. This is implementable without selecting new semantics: the engine consumes a closed policy grammar and fails closed until that input exists. The contract assigns modeled constructs to the policy at `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:47-51`, and the fail-closed rule is at `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:919-929`.

## 4. Stable identities and ordering

All ordering comparisons use unsigned lexicographic comparison of the exact UTF-8 bytes of the compared field. Locale, filesystem collation, Windows case folding, dictionary insertion order, hash-table order, process scheduling, and Git's incoming traversal order MUST NOT influence output.

Git paths MUST decode as strict UTF-8, MUST be relative, MUST contain `/`, MUST NOT contain `\`, NUL, `.` or `..` path components, and MUST preserve their decoded code points exactly; Unicode normalization and case folding are forbidden. An invalid path causes `STOP/3/PATH_INVALID`. Hashes always use the original raw blob bytes.

Every JSONL row MUST contain `record` and `stable_id`. `stable_id` is lowercase SHA-256 of the concatenation below, with literal NUL separators and no terminal NUL:

```text
record UTF-8 bytes
NUL
primary Git-relative path UTF-8 bytes, or empty bytes when no path exists
NUL
the row's identity tuple fields in the order specified below, each UTF-8 encoded and NUL-separated
```

Identity tuples are exact:

| Record | Identity tuple after path |
|---|---|
| `FILE` | `mode`, `blob_oid` |
| `DIRECT_DEPENDENCY` | canonical name, one-based source line |
| `DEPENDENCY` | canonical name, exact version, one-based source line |
| `SECRET_CATEGORY` | category |
| `EGRESS` | class, destination-or-empty, source blob OID-or-empty, one-based line-or-`0`, one-based column-or-`0`, construct |
| `UNRESOLVED` | axis, syntax, reason |

Before serialization, every set MUST be copied to an array and sorted. Nested arrays (`hashes`, `paths`, `credential_names`, reason lists, member lists) sort by their element UTF-8 bytes; no array is emitted from a set or mapping iterator directly.

JSONL files sort rows by `(record, path-or-empty, stable_id)` under the same unsigned UTF-8 byte comparison. `SHA256SUMS.txt`, core-member lists, environment records, tool records, artifact records, and file-name checks sort by relative name or declared `kind` using the same rule. These requirements refine the contract's `(record, path, stable_id)` order and sorted-key requirement. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:111-136`

## 5. Canonical byte grammar

All text files are UTF-8 without BOM and end in exactly one LF byte. No output file contains CR. Binary capture files contain the exact specified byte stream.

Canonical JSON is restricted to objects, arrays, strings, non-negative integers, `true`, `false`, and `null`; floats are forbidden. Object keys are ASCII and sorted by unsigned UTF-8 bytes. Serialization uses no insignificant whitespace: comma is `,`, colon is `:`, and there is no indentation. Strings use JSON escapes for quote, backslash, and control characters; all non-ASCII Unicode scalar values are emitted as lowercase `\uXXXX` escapes, using a lowercase surrogate pair when required. `/` is not escaped. Integers use base 10 with no sign or leading zero except the single value `0`. Each JSON document has exactly one terminal LF. Each JSONL line is one canonical JSON object followed by LF; an empty JSONL file is zero bytes.

Paths inside deterministic files are Git-relative `/` paths. Absolute repo, output, temporary, pin-record, and tool paths occur only in `command.json`, `environment.json`, or `tools.json` and are excluded from deterministic comparison.

Source locations are one-based. Lines split only at LF; a preceding CR is part of the line content and is not counted in the column. Column is one plus the count of decoded Unicode scalar values preceding the construct on that line. A construct spanning lines uses the start line/column.

## 6. Exact output tree and schemas

A finalized `OutputRoot` contains exactly these 16 files and no directories:

```text
command.json
environment.json
tools.json
source.json
universe.jsonl
dependencies.jsonl
secret_scan.jsonl
egress.jsonl
unresolved.jsonl
summary.json
stdout.bin
stderr.bin
rc.txt
elapsed_ms.txt
SHA256SUMS.txt
COMPLETE.json
```

The contract establishes this create-once family and requires `COMPLETE.json` last. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:111-145`

### 6.1 Run-envelope files

`command.json` has exactly:

```text
schema                  "p9-15-command/v1"
runner_argv             array of the expanded runner argv strings, including argv[0]
child_argv              array of expanded child argv strings, including argv[0], or [] if not launched
cwd                     normalized absolute RepoRoot
started_utc             UTC timestamp
ended_utc               UTC timestamp
producer_author         copied from PinRecord
reviewer_identity       copied from PinRecord
execution_operator_id   exact Windows token identity returned by the OS
```

Timestamps use exactly `YYYY-MM-DDTHH:MM:SS.ffffffZ`, with six decimal digits. They are observations, not inputs, and are excluded from compared bytes.

`environment.json` has exactly `schema:"p9-15-environment/v1"`, `allowed` as seven objects `{"name":...,"value":...}` sorted by name, and `removed_names` as a sorted array of inherited names found and removed before child launch. Removed values are never read.

`tools.json` has exactly `schema:"p9-15-tools/v1"`, `pin_record` containing absolute path/bytes/SHA-256, `tools` containing the three measured tool records, and `artifacts` containing the three measured artifact records. Records use the PinRecord field grammar and add `match:true`; any mismatch prevents semantic interpretation.

`elapsed_ms.txt` is one non-negative base-10 integer plus LF. It is `floor(1000 * monotonic_elapsed_seconds)` measured from immediately before child process creation through stream drain and process exit. It is absent only when the child was not launched and a complete output root cannot be produced.

### 6.2 Deterministic semantic files

`source.json` has exactly these top-level keys:

```text
schema                  "p9-15-source/v1"
source_sha              40 lowercase hex
commit_object_type      "commit"
full_tree_oid           Git object ID
product_subtree_oid     Git object ID or null when the path is absent
policy                  {path,blob_oid,bytes,sha256}
producer                {path,blob_oid,bytes,sha256}
tree_counts             {entries_total,regular_blobs,symlinks,gitlinks,other}
universe_counts         {binary_excluded,text_scanned,files_total}
pin_record_sha256       64 lowercase hex
```

`universe.jsonl` contains one object per admitted regular blob, with exactly:

```text
record                  "FILE"
stable_id               64 lowercase hex
path                    Git-relative path
mode                    "100644" or "100755"
blob_oid                Git object ID
bytes                   non-negative integer
sha256                  raw-content SHA-256
content_class           "text_utf8" or "binary"
secret_disposition      "scanned_text" or "excluded_binary"
egress_disposition      "analyzed", "not_executable_or_network_relevant",
                        "unresolved", or "not_in_egress_universe"
reason                  uppercase-snake token or "OK"
```

`dependencies.jsonl` contains `DIRECT_DEPENDENCY` and `DEPENDENCY` rows. Every row has `record`, `stable_id`, `path`, `source_blob_oid`, `source_line`, `name_original`, `name_canonical`, `specifier`, `version`, `hashes`, and `disposition`. `hashes` is a sorted array of lowercase 64-hex SHA-256 values. A direct row uses `version:null`; a locked row uses `specifier:"=="` and its exact version. `disposition` is `accepted`, `invalid`, `forbidden_reference`, `duplicate`, or `unresolved`. The three dependency source identities are represented by their corresponding `FILE` rows and referenced through `source_blob_oid`.

`secret_scan.jsonl` contains exactly one `SECRET_CATEGORY` row for every policy category, even at zero. Each row has `record`, `stable_id`, `path:""`, `category`, `path_hits`, and `paths`. `paths` is the sorted unique path array and `path_hits` equals its length. Matched text and positions are forbidden.

`egress.jsonl` contains one `EGRESS` row per resolved inventory member and one explicit `expected_absent` row for every policy-declared absence. Each row has `record`, `stable_id`, `path`, `class`, `destination`, `protocol`, `port`, `activation_predicate`, `source_blob_oid`, `source_line`, `source_column`, `construct`, `credential_names`, and `disposition`. Nullable fields are JSON `null`, not empty strings, except `path` is `""` for an absence row. `port` is an integer from 1 through 65535 or null. `credential_names` is a sorted array of names only. `disposition` is `resolved_allowed`, `resolved_forbidden`, `resolved_unexpected`, or `expected_absent`.

`unresolved.jsonl` contains zero or more `UNRESOLVED` rows with exactly `record`, `stable_id`, `path`, `axis`, `member_identity`, `syntax`, and `reason`. It is zero bytes when no unresolved row exists.

`summary.json` has exactly:

```text
schema                  "p9-15/v1"
source_sha              40 lowercase hex
counts                  {files_total,text_scanned,binary_excluded,dependencies,
                         secret_category_path_hits,egress_rows,unresolved}
axis_results            {dependencies:{class,reason},secrets:{class,reason},
                         egress:{class,reason}}
overall                 {class,rc,reason}
limitations             sorted array of policy-declared limitation tokens
core_members            sorted array of {path,bytes,sha256}
deterministic_core_sha256 64 lowercase hex
```

`core_members` contains exactly `dependencies.jsonl`, `egress.jsonl`, `secret_scan.jsonl`, `source.json`, `universe.jsonl`, and `unresolved.jsonl`, sorted by path. `deterministic_core_sha256` is SHA-256 of the ASCII concatenation of one line per `core_members` entry in that same order:

```text
<64_lower_hex_sha256><two ASCII spaces><relative_path><LF>
```

This definition is acyclic: `summary.json` is not a member of the digest it carries.

### 6.3 Process-capture and finalization files

For a launched child, `stdout.bin` is its exact stdout bytes and MUST satisfy §7. `stderr.bin` is its captured stderr after deterministic redaction: replace exact occurrences of `RepoRoot`, `OutputRoot`, staging root, `TEMP`, tool paths, and `PinRecord` with `<REPO_ROOT>`, `<OUTPUT_ROOT>`, `<STAGING_ROOT>`, `<TEMP>`, `<TOOL_PATH>`, and `<PIN_RECORD>` respectively; then convert CRLF to LF. Secret-match text MUST never reach this stream. It is zero bytes on PASS.

`rc.txt` is exactly `0\n`, `1\n`, or `3\n` and equals the runner's process exit code after wrapper adjudication.

`SHA256SUMS.txt` contains exactly 14 lines—one for every file above it in the 16-file list. Each line is lowercase SHA-256, two ASCII spaces, relative file name, and LF. Lines sort by relative file-name bytes. It has no self-entry and no `COMPLETE.json` entry.

`COMPLETE.json` is written last and has exactly `schema:"p9-15-complete/v1"`, `source_sha`, `class`, `rc`, `reason`, `sha256sums:{path:"SHA256SUMS.txt",bytes,sha256}`, `summary:{path:"summary.json",bytes,sha256}`, and `final_file_count:16`. It has no self-hash. A directory without a valid `COMPLETE.json` is partial and MUST NOT be interpreted.

The runner MUST close every file, fsync file contents where the platform exposes it, write `COMPLETE.json`, fsync the staging directory where supported, and atomically rename the staging directory to the non-existing `OutputRoot`. It MUST never overwrite, merge into, append to, or repair an existing `OutputRoot`. No-clobber output is the standing evidence convention. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:1266-1277`

## 7. Exact stdout grammar

When the child launches far enough to classify the semantic run, its stdout is exactly four LF-terminated ASCII lines in this order, with single ASCII spaces and no leading or trailing spaces:

```text
P9_15_BEGIN schema=p9-15/v1 source_sha=<40_lower_hex>
P9_15_COUNTS files_total=<uint> text_scanned=<uint> binary_excluded=<uint> dependencies=<uint> secret_category_path_hits=<uint> egress_rows=<uint> unresolved=<uint>
P9_15_OUTPUT relative_path=summary.json bytes=<uint> sha256=<64_lower_hex>
P9_15_RESULT class=<PASS|FAIL|STOP> rc=<0|1|3> reason=<UPPER_SNAKE_TOKEN>
```

The source contract establishes these four records and their order. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:138-145`

`uint` is `0` or a base-10 integer beginning with `[1-9]`; signs and leading zeroes are forbidden. The output line's `bytes` and `sha256` describe the final canonical `summary.json`. The result line MUST agree with `summary.json`, `rc.txt`, `COMPLETE.json`, and the process exit code.

If the runner stops before a trustworthy child can be launched, process stdout is empty, process stderr is exactly `P9_15_RUNNER_STOP reason=<TOKEN> rc=3\n`, and the exit code is 3. `OUTPUT_ROOT_EXISTS` produces no files. For any other pre-child STOP, the runner MAY finalize a 16-file STOP bundle only if it can do so without executing an unbound helper; otherwise absence of `COMPLETE.json` is the evidence of incompleteness. A pre-child STOP is never converted to FAIL.

## 8. Result and exit-code contract

There are exactly three normal exit codes:

| Class | Exit | Meaning |
|---|---:|---|
| `PASS` | `0` | Full declared universe evaluated; every member has exactly one terminal disposition; dependencies satisfy policy; secret category/path hits are zero; all egress constructs are resolved; no forbidden/unexpected activation exists; no unresolved row exists. |
| `FAIL` | `1` | Evaluation completed over the full declared universe and found at least one understood source deviation. |
| `STOP` | `3` | Evaluation, binding, or evidence finalization is incomplete or untrustworthy. |

The class meanings and STOP-over-FAIL precedence come from the producer contract and repository status-before-output rule. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:147-153`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:414-420`

The exact failure mapping is:

| Condition | Class/exit | Reason token |
|---|---|---|
| Bad/missing/extra argv; invalid lexical grammar | STOP/3 | `ARGUMENT_ERROR` |
| Cwd is not resolved RepoRoot | STOP/3 | `CWD_MISMATCH` |
| Environment name/value set differs from §2.4 | STOP/3 | `ENVIRONMENT_INVALID` |
| RepoRoot invalid or not the Git top level | STOP/3 | `REPO_ROOT_INVALID` |
| Source SHA malformed, absent, ambiguous, not a commit, or resolves differently | STOP/3 | `SOURCE_IDENTITY_INVALID` |
| OutputRoot already exists | STOP/3 | `OUTPUT_ROOT_EXISTS` |
| Output parent/staging/create/atomic-rename operation fails | STOP/3 | `OUTPUT_CREATE_ERROR` |
| Pin record missing, hash mismatch, noncanonical, wrong schema/source/member set | STOP/3 | `PIN_RECORD_INVALID` |
| PowerShell/Git/Python path, bytes, hash, length, or version mismatch | STOP/3 | `TOOL_IDENTITY_MISMATCH` |
| Runner/inventory/policy worktree/Git-blob/pin identity mismatch | STOP/3 | `ARTIFACT_IDENTITY_MISMATCH` |
| Git helper nonzero, stderr, malformed output, partial output, or unclassified status | STOP/3 | `GIT_ERROR` |
| Tree output malformed, duplicated, unknown mode, or not fully consumed | STOP/3 | `TREE_ENUMERATION_ERROR` |
| Blob read missing, short, malformed, or hash/size conservation mismatch | STOP/3 | `BLOB_READ_ERROR` |
| Git path violates §4 | STOP/3 | `PATH_INVALID` |
| Policy malformed, has unknown/missing keys, or is noncanonical | STOP/3 | `POLICY_INVALID` |
| Dependency syntax cannot be classified under the frozen grammar | STOP/3 | `DEPENDENCY_GRAMMAR_UNSUPPORTED` |
| Any admitted identity disappears, duplicates, overwrites, or changes representation | STOP/3 | `CONSERVATION_ERROR` |
| Egress syntax/construct is unmodeled or tokens remain unconsumed | STOP/3 | `POLICY_COVERAGE_INCOMPLETE` |
| Child stdout is not exactly §7 or conflicts with captured/classified state | STOP/3 | `CHILD_PROTOCOL_ERROR` |
| Stream read/write, canonical serialization, hashing, manifest, or finalization fails | STOP/3 | `EVIDENCE_IO_ERROR` |
| Caught cancellation before completion | STOP/3 | `CANCELLED` |
| Understood lock/direct-dependency rule is violated | FAIL/1 | `DEPENDENCY_POLICY_DEVIATION` |
| One or more content-redacted secret category/path hits | FAIL/1 | `SECRET_SIGNATURE_HIT` |
| Resolved forbidden or unexpected egress activation path | FAIL/1 | `EGRESS_POLICY_DEVIATION` |
| No condition above | PASS/0 | `OK` |

The producer owns no numeric wall-clock timeout because no source establishes one; inventing a number is forbidden. A caught external cancellation is `CANCELLED`; a hard kill has no producer exit code and leaves no valid `COMPLETE.json`. A future timeout is allowed only if its exact duration and clock semantics are frozen in a new pin/policy revision; until then a numeric timeout is **UNKNOWN**. The contract names timeout as a STOP class but supplies no duration. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:147-153`

When multiple conditions exist, any STOP condition wins over every FAIL condition. Within the winning class, all reason tokens are sorted and stored in `summary.json` under the relevant axis limitation/detail supplied by policy; the top-level `reason` is the unsigned-ASCII-smallest token. This removes discovery-order dependence.

## 9. Worked synthetic example

The values below are deliberately synthetic grammar examples. They are not measured from Commit 2, are not hashes of a real bundle, and MUST NOT be cited as a P9-15 result. Actual counts, bytes, hashes, and result are **UNKNOWN** until the frozen producer runs; the packet skeleton forbids filling them prospectively. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:232-242`; `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:266-271`

Example `stdout.bin`:

```text
P9_15_BEGIN schema=p9-15/v1 source_sha=1111111111111111111111111111111111111111
P9_15_COUNTS files_total=2 text_scanned=2 binary_excluded=0 dependencies=1 secret_category_path_hits=0 egress_rows=1 unresolved=0
P9_15_OUTPUT relative_path=summary.json bytes=487 sha256=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
P9_15_RESULT class=PASS rc=0 reason=OK
```

Example canonical `universe.jsonl` rows, already sorted by `(record,path,stable_id)`:

```jsonl
{"blob_oid":"2222222222222222222222222222222222222222","bytes":12,"content_class":"text_utf8","egress_disposition":"analyzed","mode":"100644","path":"IBKR_PAPER_BRIDGE/example.py","reason":"OK","record":"FILE","secret_disposition":"scanned_text","sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","stable_id":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"}
{"blob_oid":"3333333333333333333333333333333333333333","bytes":9,"content_class":"text_utf8","egress_disposition":"not_in_egress_universe","mode":"100644","path":"README.md","reason":"OK","record":"FILE","secret_disposition":"scanned_text","sha256":"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd","stable_id":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"}
```

Example zero-hit category row:

```json
{"category":"openai_token","path":"","path_hits":0,"paths":[],"record":"SECRET_CATEGORY","stable_id":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"}
```

Example `rc.txt`:

```text
0
```

The synthetic `bytes` and hash fields intentionally demonstrate field grammar only; they are not asserted to cross-hash one another.

## 10. Determinism contract

Two completed runs with the same semantic inputs—identical `SourceSha` Git objects, policy blob, producer blob, pin-record bytes, and tool bytes—MUST produce byte-identical deterministic core files even when `RepoRoot`, `OutputRoot`, staging directory, operator, and run time differ.

The compared-byte set is exactly:

```text
dependencies.jsonl
egress.jsonl
rc.txt
secret_scan.jsonl
source.json
stderr.bin
stdout.bin
summary.json
universe.jsonl
unresolved.jsonl
```

For a PASS or source-derived FAIL, all ten MUST be byte-identical. For a STOP caused before complete source evaluation, determinism is checked only for whichever canonical semantic files were finalized; the STOP reason and missing/invalid `COMPLETE.json` prevent that run from serving as a successful replay.

Stability is achieved as follows:

| Source of drift | Normative treatment |
|---|---|
| Git traversal order | Parse the full NUL stream, then sort admitted members by raw UTF-8 path bytes. |
| Mapping/set iteration | Convert to arrays and sort as §4; never serialize direct set/dict iteration. |
| JSON object order/whitespace | Canonical grammar in §5. |
| Line endings/BOM | UTF-8, no BOM, LF only. |
| Worktree normalization | Subject/policy bytes come from `git cat-file`, never product worktree files. |
| Absolute repo/output/temp/tool paths | Appear only in excluded run-envelope files. |
| Timestamps and elapsed time | Appear only in excluded `command.json` and `elapsed_ms.txt`. |
| Operator identity | Appears only in excluded `command.json`. |
| Environment values/removed names | Appear only in excluded `environment.json`. |
| Tool absolute paths | Appear only in excluded `tools.json`; their byte identities remain semantic inputs through the pin digest. |
| Filesystem timestamps, ACLs, directory entry order | Never serialized or compared. |
| Temporary staging name | Never serialized in the deterministic core; normalized only in captured error text. |
| Error discovery order | STOP wins; reason arrays sort; top reason is the smallest token. |

`command.json`, `environment.json`, `tools.json`, `elapsed_ms.txt`, `SHA256SUMS.txt`, and `COMPLETE.json` are run-envelope files and are explicitly excluded from cross-run byte comparison. `SHA256SUMS.txt` and `COMPLETE.json` are excluded because they intentionally bind the volatile envelope as well as the deterministic core. They MUST still verify internally for each individual run.

No other nondeterministic field is permitted in the compared-byte set. If an implementation discovers one, it MUST return `STOP/3/EVIDENCE_IO_ERROR`; it MUST NOT add an unreviewed normalization or silently widen the exclusion list.

## 11. Independent verification procedure

The verifier does not need to have run the original producer. The contract requires re-hashing, Git-object re-enumeration, fresh replay, and preregistered falsification. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:155-170`

### 11.1 Offline structural and hash check

Without executing `p9_15_inventory.py`, the verifier MUST:

1. Confirm that `OutputRoot` has exactly the 16 names in §6, no directory, and a parseable canonical `COMPLETE.json`.
2. Recompute raw byte counts and SHA-256 for the 14 `SHA256SUMS.txt` members; require exact sorted lines, no duplicate, no missing member, no self-entry, and no `COMPLETE.json` entry.
3. Recompute the bytes/SHA links in `COMPLETE.json`, require `final_file_count=16`, and require class/rc/reason/source SHA equality across `summary.json`, `COMPLETE.json`, `rc.txt`, and the final stdout line.
4. Parse every JSON/JSONL document with duplicate-key rejection, re-emit it with §5, and require byte equality. Require zero bytes for an empty `unresolved.jsonl`.
5. Recompute every `stable_id`, every count, every nested-array order, every row order, every `core_members` entry, and `deterministic_core_sha256`.
6. Require `files_total = text_scanned + binary_excluded`; require one `FILE` row per admitted member; require `path_hits = len(paths)` for every secret category; and require the reported counts to equal the actual row sets.
7. Confirm that no secret matched text, forbidden absolute path, CR byte, BOM, timestamp, elapsed value, operator name, or staging name appears in any compared-byte file.
8. Compare the P9-16 retained-path/bytes/SHA entry for every P9-15 file against the recomputed values. P9-16 requires every retained relative path to be indexed with bytes and SHA-256. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:40`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:244-257`

Any mismatch is a verification FAIL if all bytes are readable and the contradiction is established; inability to read, parse, or enumerate is verification STOP.

### 11.2 Independent Git-object check

Using an independently pinned Git executable, the verifier MUST:

1. Prove `source_sha` is a commit and recompute its full-tree and `IBKR_PAPER_BRIDGE` subtree OIDs.
2. Run the exact §3 `ls-tree` argv and compare admitted modes, paths, object IDs, and sizes to `universe.jsonl`.
3. `cat-file blob` every admitted OID, recompute bytes and SHA-256, and compare all `FILE` rows.
4. Re-read the producer and policy blobs from `source_sha`, compare `source.json`, and compare them with the independently hashed pin record.
5. Recompute dependency membership, secret category/path sets, and egress terminal accounting under the frozen policy. Do not trust counts copied from `summary.json`.

The check reads Git objects rather than worktree product bytes because the source records a real CRLF-vs-blob hash failure mode. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:388-402`

### 11.3 Fresh replay command

From a fresh detached Commit-2 worktree, with the exact §2.4 environment and cwd set to that fresh root, run:

```text
<PINNED_PYTHON_EXE> -I -B <FRESH_COMMIT2_WORKTREE>\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\p9_15_inventory.py verify --repo <FRESH_COMMIT2_WORKTREE> --source-sha <COMMIT_2_FULL_40_LOWER_HEX_SHA> --policy-ref MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json --evidence-root <ORIGINAL_P9_15_OUTPUT_ROOT> --git-exe <PINNED_GIT_EXE> --pin-record <ABSOLUTE_P9_06_PIN_RECORD_JSON> --pin-record-sha256 <64_LOWER_HEX_SHA256>
```

Verifier stdin is closed. It does not alter `evidence-root`; it may use a private temporary directory whose path and metadata are excluded. Its stdout is exactly:

```text
P9_15_VERIFY_BEGIN schema=p9-15/v1 source_sha=<40_lower_hex>
P9_15_VERIFY_CHECK manifest=<PASS|FAIL|STOP> source=<PASS|FAIL|STOP> canonical=<PASS|FAIL|STOP> core=<PASS|FAIL|STOP>
P9_15_VERIFY_RESULT class=<PASS|FAIL|STOP> rc=<0|1|3> reason=<UPPER_SNAKE_TOKEN>
```

Verifier exit 0 means every structural, source, canonical, and compared-byte check passed. Exit 1 means a complete check established a mismatch. Exit 3 means a check could not be completed. The verifier MUST independently regenerate the compared-byte set and compare exact bytes; invoking the original result's claimed hash alone is insufficient.

### 11.4 Mandatory falsification before reliance

Before treating a new implementation's tests as closure evidence, record real RED and GREEN commands/output for all five mutations:

1. replace or remove one declared executable/artifact and drive the real top-level runner;
2. add one secret-signature fixture and prove the category/path is reported while match text never prints;
3. add one unknown or nested network sink and prove `UNRESOLVED` plus STOP/3;
4. add two dependency members that canonicalize to the same identity and prove STOP/3 rather than overwrite;
5. make one admitted blob read fail and prove STOP/3 rather than a reduced-universe PASS.

The repository requires executable RED/GREEN evidence and specifically requires instrument replacement, unknown static forms, and disappearing/duplicate members to turn red. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687,886-895,919-929,957-967`

## 12. Honest unknowns and boundary

- **Producer author/reviewer identity: UNKNOWN.** Settled by the Lead assignment and canonical P9-06 pin record before Commit 2. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:53-55,266-271`
- **Final egress policy grammar bytes: UNKNOWN.** Settled by the reviewed Commit-2 `p9_15_policy.json`; until then the engine is implementable but a real PASS is unavailable because unknown coverage must STOP. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:47-51,101-109`
- **Actual P9-15 counts, paths, hashes, class, and rc: UNKNOWN.** Settled only by executing the frozen producer against the real Commit-2 objects. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:232-242`
- **Numeric internal timeout: UNKNOWN and deliberately not invented.** There is no producer-owned timeout in v1; only caught cancellation is classified. What would settle a timeout is a separately frozen duration and clock contract in a pin/policy revision.
- **P9-15 labour: NO SOURCED ESTIMATE.** The work catalogue supplies no bounded R15/Packet-9/WP-I price. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54,196-198`

This specification does not implement the producer, create evidence, complete Packet 9, accept a result, open a gate, or authorize any action.
