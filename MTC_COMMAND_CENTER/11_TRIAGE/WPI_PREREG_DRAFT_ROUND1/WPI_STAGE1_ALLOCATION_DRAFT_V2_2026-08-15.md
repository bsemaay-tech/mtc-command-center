# Stage-1 allocation record — version 2 commit-time template

Status: **V2 COMMIT-TIME TEMPLATE — NOT A LIVE ALLOCATION, NOT COMMITTED, AND NOT HOST AUTHORITY.** This lane deliberately mints no live identity. Every live value is labelled `MUST BE MINTED AT COMMIT TIME`; every result is labelled `MUST BE RECORDED AT COMMIT TIME`. The eventual spendable record is this document with those labels replaced by literal values and evidence under the ordered checklist in §9. The Stage-1 record must exist before Commit 1, and D2 is not spendable until the exact read-only preregistration is committed. (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-58`; `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:495-533`)

**No review finding is rejected.** All five `MUST-FIX-BEFORE-COMMIT` findings are valid. This version closes them as follows:

| Review finding | Closure in v2 |
|---|---|
| Required fields/results were named but unpopulated | §2 gives every required field either its fixed value or an exact commit-time procedure and the mandatory status; §§4, 5, 6, and 7 give exact evidence procedures and replacement gates. |
| Reason token was only substring-matched | §4.3 compares the complete expected stdout/stderr line and rc, rejects every extra/conflicting byte or line, and records a replayable invocation. |
| Collision universe was unproved | §5.1 stops **before minting** unless a committed completeness manifest, complete chained ledger, retained remote-allocation snapshot, and exhaustive operator-root inventory are all established; §5.2 scans that established universe without ignore filtering and stops on unreadable or reparse-point content. |
| Append-only was asserted | §6 requires exact parent bytes as the candidate prefix, validates chained row order/state, appends with OS append mode, binds parent/candidate Git objects, and makes any failure a non-spendable STOP before progression. |
| Checked predicate differed from sourced object | §4.2 verifies the source bytes, writes those bytes once to a create-new snapshot, holds a no-write/no-delete sharing lock while Bash sources that exact snapshot, and verifies it again after Bash exits. |

The review accurately found the five defects at `W1_ALLOCATION_REVIEW.md:5-39`. The governing field list is reconciliation row 3, which requires concrete allocation identities plus grammar, collision, and append-only results (`AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-70`).

## 1. Non-negotiable completion rule

The template words `MUST BE MINTED AT COMMIT TIME`, `MUST BE RECORDED AT COMMIT TIME`, `MUST BE RESOLVED BEFORE MINTING`, and `UNKNOWN` are STOP tokens. A candidate containing any of them is not the Stage-1 allocation record and must not be committed as spendable, supplied to a consumer, or used for host contact. This preserves the successor's rule that unresolved or unequal consumers STOP and that allocation precedes any host contact (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:36-60,98-147,495-533`).

This document authorizes no host, network, deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or economic action. In particular, D2 excludes every host write; a future `SPENT` transition described in §6.4 needs separate authority and is not authorized here (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-60`).

## 2. Allocation field record

The only generator grammar is `UTCSTAMP := [0-9]{8}T[0-9]{6}` (15 ASCII bytes), `NONCE := [0-9a-f]{8}` (8 ASCII bytes), and `BASE := WPI-<UTCSTAMP>Z-<NONCE>` (29 ASCII bytes). All other identities are derived once from the one base, never typed independently (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:76-106`).

| Required field | V2 value/status | Exact commit-time procedure |
|---|---|---|
| `UTCSTAMP` | **MUST BE MINTED AT COMMIT TIME** | Execute §3 once; take `$utc`; require exact grammar and 15 ASCII bytes. |
| `NONCE` | **MUST BE MINTED AT COMMIT TIME** | Execute §3 once; generate exactly four cryptographic-random bytes and render eight lowercase hex characters. |
| `BASE` / `BASE_RUN` | **MUST BE MINTED AT COMMIT TIME** | `$base = "WPI-${utc}Z-${nonce}"`; require exact grammar and 29 ASCII bytes. |
| P0 `RUNID` | **MUST BE MINTED AT COMMIT TIME** | `$p0Runid = "${base}-P0"`. |
| RO `RUNID` | **MUST BE MINTED AT COMMIT TIME** | `$roRunid = "${base}-RO"`. |
| P0 `EV_STAGE_ID` | `p0` | Fixed literal; still pass it through the exact pinned predicate in §4.3. |
| RO `EV_STAGE_ID` | `ro` | Fixed literal; still pass it through the exact pinned predicate in §4.3. |
| remote-base leaf | **MUST BE MINTED AT COMMIT TIME** | `$remoteBaseLeaf = "wpi_staging_${base}"`. |
| `REMOTE_BASE` | **MUST BE MINTED AT COMMIT TIME** | `$remoteBase = "/home/gatea/${remoteBaseLeaf}"`. This is a value derivation only; it creates nothing. |
| `CONFIRM_TOKEN` | **MUST BE MINTED AT COMMIT TIME** | `$confirmToken = "${base}-EXECUTE"`. |
| operator-record leaf | **MUST BE MINTED AT COMMIT TIME** | `$operatorLeaf = "WPI_TRANSPORT_${base}"`. |
| `OPERATOR_RECORD_ROOT` | **MUST BE MINTED AT COMMIT TIME** | `$operatorRoot = "C:\WPI_ARTIFACTS\${operatorLeaf}"`. This is a value derivation only; it creates nothing. |
| initial successor identity | **UNKNOWN — MUST BE RESOLVED BEFORE MINTING** | Before §3, fix one normalized repo-relative path for the exact Commit-1 attestation-only preregistration and record `repo-path:<that path>`. The path locator is computable before its commit and creates no Git-object self-reference. The chosen interpretation must be present in the controlling final text; otherwise `SUCCESSOR_IDENTITY_STOP`. |
| canonical ledger repo path | **UNKNOWN — MUST BE RESOLVED BEFORE MINTING** | Resolve the committed canonical location of `WPI_RUNID_ALLOCATION_BURN_LEDGER.md`, bind it at `$ParentCommit`, and satisfy §§5.1 and 6. The sources name the ledger but do not establish its path (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:204-212`). |
| retained remote-allocation record | **UNKNOWN — MUST BE RESOLVED BEFORE MINTING** | Name a pre-existing retained local snapshot and committed authority/completeness record. No host contact may be used to fill it before Commit 1. If it cannot be established, §5.1 stops before minting. |
| grammar/predicate results | **MUST BE RECORDED AT COMMIT TIME** | Execute §4.3 against the locked §4.2 snapshot; insert every literal invocation, stdout, stderr, and rc into §7. |
| collision results | **MUST BE RECORDED AT COMMIT TIME** | Pass §5.1, execute §5.2, and insert the complete manifest identity and each actual result into §7. |
| append-only disposition and verification | **MUST BE RECORDED AT COMMIT TIME** | Execute §6; insert parent/candidate identities, exact appended row, pre-commit verifier result, and post-commit verifier result into §7. |
| per-consumer equality manifest | **MUST BE RECORDED AT COMMIT TIME** | Name every consumer and prove `declared = observed = equal`; any duplicate, extra, missing, independently typed, or unequal consumer is STOP (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:108-114`). |

## 3. Exact commit-time generator

The §5.1 universe-completeness preflight and §6 parent-ledger preflight must pass **before** this generator runs. Execute the block exactly once. Preserve its literal bytes, PowerShell version, stdout, stderr, rc, and all outputs. The generator itself is fixed by the successor (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:80-94`).

```powershell
$utc = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmss', [Globalization.CultureInfo]::InvariantCulture)
$nonceBytes = New-Object byte[] 4
$rng = [Security.Cryptography.RandomNumberGenerator]::Create()
try { $rng.GetBytes($nonceBytes) } finally { $rng.Dispose() }
$nonce = ([BitConverter]::ToString($nonceBytes)).Replace('-', '').ToLowerInvariant()
$base = "WPI-${utc}Z-${nonce}"

if ($utc -cnotmatch '^[0-9]{8}T[0-9]{6}$' -or [Text.Encoding]::ASCII.GetByteCount($utc) -ne 15) {
    throw 'UTCSTAMP_GRAMMAR_STOP'
}
if ($nonce -cnotmatch '^[0-9a-f]{8}$' -or [Text.Encoding]::ASCII.GetByteCount($nonce) -ne 8) {
    throw 'NONCE_GRAMMAR_STOP'
}
if ($base -cnotmatch '^WPI-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$' -or
    [Text.Encoding]::ASCII.GetByteCount($base) -ne 29) {
    throw 'BASE_GRAMMAR_STOP'
}

$p0Runid        = "${base}-P0"
$roRunid        = "${base}-RO"
$p0StageId      = 'p0'
$roStageId      = 'ro'
$remoteBaseLeaf = "wpi_staging_${base}"
$remoteBase     = "/home/gatea/${remoteBaseLeaf}"
$confirmToken   = "${base}-EXECUTE"
$operatorLeaf   = "WPI_TRANSPORT_${base}"
$operatorRoot   = "C:\WPI_ARTIFACTS\${operatorLeaf}"

$PSVersionTable.PSVersion.ToString()
"UTCSTAMP=$utc"
"NONCE=$nonce"
"BASE=$base"
"P0_RUNID=$p0Runid"
"RO_RUNID=$roRunid"
"P0_EV_STAGE_ID=$p0StageId"
"RO_EV_STAGE_ID=$roStageId"
"REMOTE_BASE_LEAF=$remoteBaseLeaf"
"REMOTE_BASE=$remoteBase"
"CONFIRM_TOKEN=$confirmToken"
"OPERATOR_RECORD_LEAF=$operatorLeaf"
"OPERATOR_RECORD_ROOT=$operatorRoot"
```

## 4. Predicate identity, immutable binding, and exact grammar matrix

### 4.1 Objects that must be pinned before minting

`RP0-LIB.sh` must be exactly 18,968 bytes with SHA-256 `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48`. The exact Bash executable path, byte count, SHA-256, and provenance are **UNKNOWN — MUST BE PINNED BEFORE MINTING**. The successor requires the exact library object to be verified before its predicate is sourced (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-104`). The predicate emits `RP0_NOTE component_ok ...` on stdout for acceptance and `RP0_FAIL reason=<token> ...` on stderr for refusal (`WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/01_RUNKIT/RP0-LIB.sh:11-13,85-93`).

### 4.2 Checked bytes are the sourced bytes

At commit time, set `$PinnedRp0Lib`, `$PinnedBashExe`, and a create-once `$QaDir`. The following binding is mandatory:

1. Open the selected library with `FileShare.Read`, which denies write/delete sharing while allowing reads.
2. Read exactly 18,968 bytes once; verify the fixed SHA-256.
3. Create `$QaDir\RP0-LIB.pinned.sh` with `FileMode.CreateNew`, write exactly those verified bytes, flush to disk, and keep that file open with `FileShare.Read` for the entire Bash process. This denies overwrite/delete while Bash may read it.
4. Re-read and hash the locked snapshot before Bash starts.
5. Pass the **snapshot path, not the original path**, as `$1`; the QA script sources only `$1`.
6. Re-read and hash the still-locked snapshot after Bash exits; both hashes and lengths must match the fixed identity. A lock failure, short read/write, changed hash, or inability of Bash to read the locked snapshot is `PREDICATE_BINDING_STOP`.

Preserve source path, source length/SHA, snapshot path, pre-source length/SHA, post-source length/SHA, Bash identity, Bash invocation, stdout, stderr, and rc. This closes the checked-versus-sourced gap identified at `W1_ALLOCATION_REVIEW.md:37-39` and follows the declared-instrument rule (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:860-895`).

### 4.3 Exact stream grammar — no substring acceptance

Run the following Bash body through the pinned Bash while the §4.2 snapshot lock remains held. `$1` is the locked snapshot path; `$2` is the create-once transcript directory; `$3` onward are the §3 values. The PowerShell caller must preserve `matrix.stdout`, `matrix.stderr`, and `$LASTEXITCODE` and then perform the post-source hash in §4.2.

```bash
set -euo pipefail
export LC_ALL=C
lib=$1
out_dir=$2
base=$3
p0_runid=$4
ro_runid=$5
p0_stage=$6
ro_stage=$7
remote_leaf=$8
confirm_token=$9
operator_leaf=${10}

. "$lib"

require_one_exact_line() {
    file=$1
    expected=$2
    first=''
    second=''
    exec 7<"$file" || return 91
    IFS= read -r first <&7
    first_rc=$?
    IFS= read -r second <&7
    second_rc=$?
    exec 7<&-
    [ "$first_rc" -eq 0 ] || return 92
    [ "$first" = "$expected" ] || return 93
    [ "$second_rc" -ne 0 ] || return 94
    [ -z "$second" ] || return 95
}

run_case() {
    case_name=$1
    value=$2
    expected_rc=$3
    expected_token=$4
    stdout_file="$out_dir/$case_name.stdout"
    stderr_file="$out_dir/$case_name.stderr"
    invocation_file="$out_dir/$case_name.invocation"

    printf 'rp0_require_safe_component %q %q\n' "$case_name" "$value" >"$invocation_file"
    set +e
    rp0_require_safe_component "$case_name" "$value" >"$stdout_file" 2>"$stderr_file"
    actual_rc=$?
    set -e

    [ "$actual_rc" -eq "$expected_rc" ] || return 96
    if [ "$expected_rc" -eq 0 ]; then
        [ "$expected_token" = component_ok ] || return 97
        require_one_exact_line "$stdout_file" \
            "RP0_NOTE component_ok name=$case_name value=$value" || return 98
        [ ! -s "$stderr_file" ] || return 99
    else
        [ ! -s "$stdout_file" ] || return 100
        require_one_exact_line "$stderr_file" \
            "RP0_FAIL reason=$expected_token name=$case_name value=[$value]" || return 101
    fi
    printf 'case=%s expected_rc=%s actual_rc=%s exact_reason=%s stream_grammar=PASS\n' \
        "$case_name" "$expected_rc" "$actual_rc" "$expected_token"
}

run_case BASE                 "$base"          0 component_ok
run_case P0_RUNID             "$p0_runid"      0 component_ok
run_case RO_RUNID             "$ro_runid"      0 component_ok
run_case P0_EV_STAGE_ID       "$p0_stage"      0 component_ok
run_case RO_EV_STAGE_ID       "$ro_stage"      0 component_ok
run_case REMOTE_BASE_LEAF     "$remote_leaf"   0 component_ok
run_case CONFIRM_TOKEN        "$confirm_token" 0 component_ok
run_case OPERATOR_RECORD_LEAF "$operator_leaf" 0 component_ok

run_case REFUSE_EMPTY        ''              1 component_reserved
run_case REFUSE_DOT          '.'             1 component_reserved
run_case REFUSE_DOT_DOT      '..'            1 component_reserved
run_case REFUSE_LEADING_DASH '-lead'         1 component_leading_dash
run_case REFUSE_POSIX_SEP    'a/b'           1 component_charset
run_case REFUSE_BACKSLASH    'a\b'           1 component_charset
run_case REFUSE_WHITESPACE   'bad name'      1 component_charset
run_case REFUSE_CONTROL      $'bad\x01name'  1 component_charset
run_case REFUSE_NON_ASCII    $'caf\xC3\xA9' 1 component_charset
run_case REFUSE_GLOB         'bad*name'      1 component_charset
```

This is deliberately stricter than token containment: acceptance permits exactly one newline-terminated stdout line and empty stderr; refusal permits empty stdout and exactly one newline-terminated stderr line. Therefore `not_component_ok`, a second reason, a conflicting reason, an extra line, a missing final newline, or any extra byte is rejected. Structured output must be parsed as a grammar rather than searched as a substring (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:303-364`), and rc/stream completeness is adjudicated before content (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:368-420`). The eighteen required cases and reason tokens come from `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:116-135`.

## 5. Fail-closed collision universe and scan

### 5.1 Completeness gate — before minting

The source establishes the required universe but not its canonical ledger path or the completeness of the retained remote record (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-145`; `WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:204-212`). Therefore v2 does **not** claim that the universe is complete today. The Lead must first create or select a committed, local, no-host-contact collision-universe manifest containing all of these concrete fields:

| Manifest field | Required proof |
|---|---|
| `parent_commit` | Exact clean local `HEAD` from which allocation begins. |
| `canonical_ledger_repo_path`, `parent_ledger_blob_oid`, `parent_ledger_bytes`, `parent_ledger_sha256` | The canonical committed ledger at `parent_commit`; §6 validation from genesis must pass. |
| `remote_allocation_snapshot_path`, bytes, SHA-256, coverage root, coverage-through marker | Exact retained local snapshot of the authoritative `/home/gatea/` allocation ledger plus a committed authority record saying this snapshot is complete for the required historical scope. |
| `operator_archive_root` | Exact authoritative retained operator archive root. |
| `operator_root_inventory` | Exact sorted list of every retained top-level operator record root, including the two minimum historical roots and every later retained root. |
| `operator_completeness_authority` | Committed record naming that archive root and inventory as complete for retained operator records. |
| `manifest_bytes`, `manifest_sha256`, `manifest_commit` | Immutable identity of the completeness declaration itself. |

No field may contain `UNKNOWN`, a placeholder, an empty value, or an uncommitted assertion. Every named file/root must exist locally, every expected byte count/SHA must match, every authority record must be contained by `parent_commit`, and the actual sorted top-level operator-root enumeration must equal the manifest inventory one-for-one. The inventory must include `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08` and its `-R45B` successor. Missing, extra, duplicate, unreadable, unhashable, reparse-point, stale, or non-authoritative material is `COLLISION_UNIVERSE_STOP`; **do not run §3 and do not infer “no collision.”** This is the required fail-closed alternative to an unproved universe (`W1_ALLOCATION_REVIEW.md:23-29`).

### 5.2 Exact scan after minting

After §5.1 passes and §3/§4 mint and accept the candidates, scan only the manifest-bound universe, but scan all of it:

1. Re-verify the manifest identity and every member's bytes/SHA immediately before scanning.
2. Validate the parent ledger's complete row chain under §6, then raw-byte search its entire current contents for exact ASCII bytes of `BASE`, P0 `RUNID`, and RO `RUNID`.
3. Raw-byte search the entire bound remote-allocation snapshot for all three identifiers.
4. Enumerate the operator archive with `Get-ChildItem -LiteralPath ... -Force -Recurse -ErrorAction Stop`; compare its top-level roots to the manifest inventory again. Reject every reparse point. Search every enumerated path with ordinal comparison and read every regular file with `[IO.File]::ReadAllBytes`; search its raw bytes. This deliberately has no ignore-file behavior. Any enumeration/read error is `COLLISION_SCAN_STOP`, not no-hit.
5. Require the exact candidate `$operatorRoot` not to exist.
6. Preserve exact inputs, commands/script bytes, stdout, stderr, rc, enumerated root/file counts, and per-surface results.

The byte matcher for each ASCII identifier is:

```powershell
function Test-ContainsBytes([byte[]]$Haystack, [byte[]]$Needle) {
    if ($Needle.Length -eq 0) { throw 'COLLISION_SCAN_STOP empty_needle' }
    if ($Haystack.Length -lt $Needle.Length) { return $false }
    for ($i = 0; $i -le $Haystack.Length - $Needle.Length; $i++) {
        $same = $true
        for ($j = 0; $j -lt $Needle.Length; $j++) {
            if ($Haystack[$i + $j] -ne $Needle[$j]) { $same = $false; break }
        }
        if ($same) { return $true }
    }
    return $false
}
```

Only a complete successful run may emit `COLLISION_RESULT=NO_HIT_IN_COMPLETE_DECLARED_UNIVERSE`. Any hit or any inability to establish/scan the universe burns the generated base and both RUNIDs under §6; they are never retried. The complete-ledger/operator/remote requirement and burn rule are fixed at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`.

## 6. Mechanically enforced append-only ledger

### 6.1 Canonical row contract

The canonical ledger must already exist and be committed before minting. If it does not, allocation stops; establish a separately committed genesis ledger first, then restart from a new clean parent. Each data row is one LF-terminated Markdown table row with these columns, in this order:

| Row ref | Global prior row ref | Identity prior row ref | `BASE` | P0 `RUNID` | RO `RUNID` | generator UTCSTAMP | nonce | disposition | reason token | successor identity | remote evidence root | operator record root | evidence identity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Rules:

- `Row ref` is `WPI-ALLOC-` plus a six-digit strictly increasing sequence.
- `Global prior row ref` equals the immediately preceding data row, or `GENESIS` only for sequence 000001.
- `Identity prior row ref` is `NONE` for an initial `RESERVED` or initial failure `BURNED` attempt; a later `BURNED` or `SPENT` row names the exact earlier `RESERVED` row for this attempt.
- No field may contain CR, LF, or `|`; no row ref may repeat; all 14 columns are nonempty.
- Legal transitions are `NONE -> RESERVED`, `NONE -> BURNED`, `RESERVED -> BURNED`, and `RESERVED -> SPENT`. `BURNED` and `SPENT` are terminal.
- An initial collision can therefore be recorded as its own `BURNED` attempt without changing the disposition of the older colliding identity.

### 6.2 Exact append mechanism

Before appending, record `$ParentCommit`, resolve the ledger blob at `$ParentCommit:$LedgerRepoPath`, materialize its raw blob bytes into a create-new parent snapshot, and record blob OID, length, and SHA-256. Validate the entire row chain. Require the current working ledger bytes to equal the parent snapshot exactly.

Construct the complete new row in memory, validate §6.1, encode it as UTF-8 **without BOM** plus one LF, then open the working ledger using `.NET FileMode.Append`, `FileAccess.Write`, and `FileShare.None`. Write exactly the row bytes once and flush. Re-read the candidate and require:

`candidate_length = parent_length + row_length`

`candidate[0..parent_length-1] = parent_bytes`

`candidate[parent_length..end] = exact_validated_row_bytes`

Then validate the entire candidate chain. Any prefix change, truncation, insertion before EOF, duplicate/out-of-order row ref, bad global link, bad identity transition, invalid column, or extra suffix byte is `LEDGER_APPEND_STOP`. Compute and record the candidate byte length/SHA and the Git blob OID that the exact candidate would produce under the ledger path's Git filters.

This makes an overwrite or out-of-order append detectable: prior bytes must remain an exact prefix, the global predecessor must be the last prior row, the sequence must be next, and the identity predecessor/state must be legal. The verifier—not prose—rejects every violation before commit. This is the required mechanism from `W1_ALLOCATION_REVIEW.md:31-35` and implements the successor's append-only rule (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`).

### 6.3 Commit and post-commit binding

The commit gate rejects progression unless the pre-commit verifier is rc 0. After the allocation commit exists, require all of the following before calling the record committed/spendable:

1. the commit has the pinned `$ParentCommit` as its parent;
2. `$ParentCommit:$LedgerRepoPath` resolves to the recorded parent blob OID;
3. `$AllocationCommit:$LedgerRepoPath` resolves to the recorded candidate blob OID;
4. the committed allocation-record blob equals the exact completed record verified before commit;
5. a fresh verifier over the committed parent/candidate blobs reproduces the exact prefix, suffix, chain, and transition result.

Failure is `POST_COMMIT_LEDGER_BINDING_STOP`; the commit grants no host action and must not be used as Commit 1 input. The parent/candidate object IDs plus byte hashes make later mutation or substitution detectable, while the pre/post gates reject it operationally.

### 6.4 Disposition rules

- Append initial `RESERVED` only after generator grammar, locked predicate matrix, complete-universe collision scan, and the pre-reservation equality manifest all pass.
- Append `BURNED` on any grammar, predicate, universe, collision, equality, fill, commit/order, attestation-capture, or future remote create-once failure; cite the exact evidence identity. Never retry those identities.
- The exact `SPENT` trigger is **successful future create-once allocation of the exact `REMOTE_BASE` under separately committed and separately authorized bytes**, with the accepted create-once marker, stdout, stderr, rc, record path, byte count, and SHA-256 bound in `evidence identity`. Only then append `SPENT` referencing the exact `RESERVED` row. The current D2 read-only grant excludes that write, so neither this lane nor the read-only attestation capture may append `SPENT` (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:54-58`).

The `SPENT` definition is a v2 proposed resolution of an ambiguity the source did not settle (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:289-298`). It must appear unchanged in the controlling committed successor text before it can govern; otherwise `SPENT_RULE_STOP` before minting.

## 7. Commit-time evidence slots

Every cell below must be replaced by literal evidence. A summary without the underlying replayable transcript is insufficient.

| Evidence field | V2 status | Exact replacement rule |
|---|---|---|
| Generator command/version/stdout/stderr/rc | **MUST BE RECORDED AT COMMIT TIME** | Insert the literal §3 invocation and real streams/rc. |
| Generated and derived fields | **MUST BE MINTED AT COMMIT TIME** | Insert every §2 live value from the single §3 execution. |
| Source library path/bytes/SHA | **MUST BE RECORDED AT COMMIT TIME** | Insert §4.2 source identity. |
| Locked snapshot path/pre-hash/post-hash | **MUST BE RECORDED AT COMMIT TIME** | Insert §4.2 binding evidence; pre and post must equal the fixed identity. |
| Bash path/bytes/SHA/provenance | **MUST BE RECORDED AT COMMIT TIME** | Insert the pinned executable identity. |
| Eight acceptance invocations/stdout/stderr/rc | **MUST BE RECORDED AT COMMIT TIME** | Insert all per-case files and matrix summary from §4.3. |
| Ten refusal invocations/stdout/stderr/rc | **MUST BE RECORDED AT COMMIT TIME** | Insert all per-case files and matrix summary from §4.3. |
| Collision-universe manifest identity | **MUST BE RECORDED AT COMMIT TIME** | Insert manifest path/commit/bytes/SHA and all concrete members from §5.1. |
| Ledger complete-chain result | **MUST BE RECORDED AT COMMIT TIME** | Insert validator command, counts, stdout/stderr/rc, parent blob/bytes/SHA. |
| Remote-allocation snapshot result | **MUST BE RECORDED AT COMMIT TIME** | Insert authority/completeness identity, snapshot bytes/SHA, search result and rc. |
| Operator inventory/path/content result | **MUST BE RECORDED AT COMMIT TIME** | Insert declared/observed/equal root counts, file count, raw-byte scan result and rc. |
| Exact candidate operator-root result | **MUST BE RECORDED AT COMMIT TIME** | Insert literal path, nonexistence result, and rc. |
| Overall collision result | **MUST BE RECORDED AT COMMIT TIME** | Must be exactly `NO_HIT_IN_COMPLETE_DECLARED_UNIVERSE`; anything else burns and stops. |
| Initial ledger row | **MUST BE RECORDED AT COMMIT TIME** | Insert the exact validated LF-terminated row and its row-byte SHA. |
| Append verifier pre-commit result | **MUST BE RECORDED AT COMMIT TIME** | Insert parent/candidate lengths, SHAs, blob OIDs, prefix/suffix/chain results, command, streams, rc. |
| Append verifier post-commit result | **MUST BE RECORDED AT COMMIT TIME** | Insert commit/parent/blob identities and fresh committed-blob validation result. |
| Per-consumer equality manifest | **MUST BE RECORDED AT COMMIT TIME** | Insert every consumer and its parsed value; end with concrete `declared = observed = equal`. |

## 8. Consumer conservation gate

Populate consumers only from the in-memory §3 values through an allowlist of exact `(file, constant-or-table-field)` sites. File-wide/repository-wide replacement is forbidden. The manifest must cover both wrappers, runner `$BASE_RUN`, `$CONFIRM_TOKEN`, `$RECORD_ROOT`, every plan occurrence, remote/retrieval/local-binding paths, record-root leaf, both stage IDs, and all evidence-tree leaves. It must prove declared consumers = populated consumers = equality-checked consumers, and must reject duplicates, extras, missing sites, independently typed values, changed marker guards, or unequal values (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:34-60,108-114`).

Run the conservation gate once before `RESERVED` over the allocation-record/ledger sites, and again after all targeted fills over the exact final candidate bytes. A later failure appends `BURNED`; it never edits the `RESERVED` row.

## 9. Lead execution checklist — v2 to committed Stage-1 record

1. Confirm the session is local-only. Do not contact a host or network, use a credential, deploy, run a service, trade, merge to master, or push. D2 remains unspendable until Commit 1 exists (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-58`).
2. Fix the exact allocation-record repo path, canonical ledger repo path, and normalized Commit-1 preregistration path. Put the §6.4 `SPENT` rule unchanged into the controlling successor text or STOP.
3. Require the canonical ledger to exist in the clean parent commit. If it does not, create and commit a genesis ledger in a separate authorized local step, then restart this checklist from that new clean parent; do not mint first.
4. Select §5.1's collision-universe manifest already committed in the clean parent. It must bind the complete chained ledger, authoritative retained remote-allocation snapshot, exhaustive operator-root inventory, and their completeness authorities. If no such manifest exists, create and commit it in a separate authorized local step and restart this checklist from that new clean parent. If completeness cannot be established without host contact, STOP before minting.
5. Pin the clean `$ParentCommit`, parent ledger blob/bytes/SHA, exact final-run-kit `RP0-LIB.sh`, and exact Bash executable identity. Start one create-once transcript root. Any missing or mismatched identity is STOP.
6. Execute §3 exactly once. Preserve literal command, PowerShell version, stdout, stderr, rc, and every minted/derived field. Do not re-run on an error under the same preregistration.
7. Execute §4.2 and §4.3: lock the verified bytes, source only the locked snapshot, run all eight acceptance and ten refusal cases, enforce exact whole-line stream grammar, and verify the locked snapshot again after Bash exits.
8. Execute the complete §5.2 collision scan. On an incomplete/unevaluable universe or any hit, append an initial `BURNED` row using §6, commit the burn evidence under the Lead's authorized local sequence, and stop. Never reuse the identities.
9. Produce the pre-reservation consumer manifest for the allocation record and ledger. Require concrete `declared = observed = equal` and no independent typing.
10. Construct and append the initial `RESERVED` row with §6's OS append mode. Run the exact parent-prefix, suffix, sequence, predecessor, state-transition, and candidate-chain checks. A failed append check stops and burns; no prior byte is edited.
11. Populate only allowlisted consumers from the one derived value set. Run the final equality manifest on exact final bytes. On any fill/equality failure, append a chained `BURNED` row and stop.
12. Replace every §2 and §7 status cell with literal values/evidence and remove the template-only status prose. Search the candidate allocation record for the exact unresolved tokens `UNKNOWN`, `MUST BE MINTED AT COMMIT TIME`, `MUST BE RECORDED AT COMMIT TIME`, `MUST BE RESOLVED BEFORE MINTING`, `MUST BE PINNED BEFORE MINTING`, `<ALLOCATE-AT-DISPATCH>`, `<PIN-AT-FREEZE>`, and `NOT-YET-OBSERVED`; any occurrence is STOP. Grammar metavariables such as `<UTCSTAMP>` are not unresolved fields. Verify that no live identity was invented outside the preserved §3 transcript.
13. Re-run the complete grammar, identity, collision-manifest, collision-result, append-only, and equality checks against the exact candidate bytes. Record all commands, stdout, stderr, and rc. The record is not ready unless every gate is evaluable and passes.
14. Compute the allocation-record candidate blob identity and ledger candidate blob identity. Commit only the exact allocation record, canonical ledger update, and their required local evidence under the Lead's authorized Git sequence. Do not push or merge.
15. Run §6.3 against the actual allocation commit and its parent. Insert or bind the post-commit evidence through the preregistered non-self-referential mechanism; if the committed blobs do not equal the verified candidates, mark the allocation non-spendable and STOP.
16. Only after the allocation record is concretely committed and post-commit-bound may the Lead finalize and commit the exact read-only attestation-only preregistration as Commit 1. Only after Commit 1 exists may D2 be considered for its exact committed read-only capture. This checklist itself performs and authorizes no such capture (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:495-533`).

Final boundary: version 2 is an honest template. Until steps 1–15 replace every status token with literal, reproducible evidence and bind the actual commit, it is not the Stage-1 allocation record and cannot be spent.
