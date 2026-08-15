# Stage-1 allocation record — commit-time draft

Status: **DRAFT TEMPLATE — NOT AN ALLOCATION, NOT COMMITTED, AND NOT AUTHORITY.** This lane must not mint live identities; the real values are to be generated only in the allocation/commit session. (`C:\tmp\lane_kick\L1.md:55-59`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:8`)

Lane classification: **T3 process/template artifact; self-verification only.** No gate verdict or acceptance is made here. (`AGENTS.md:38`; `C:\tmp\lane_kick\L1.md:65-71`)

Purpose: supply the Lead with the concrete-field schema, minting procedure, grammar transcript, collision procedure, and append-only dispositions required for the later real Stage-1 allocation record. The required record does not yet exist. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-70`)

The owner-approved host grant is not spendable until the allocation record exists and the exact attestation-only preregistration is committed; the required order is allocation record, Commit 1, then the authorized capture. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-52`)

## 1. Allocation fields

The grammar is `UTCSTAMP := [0-9]{8}T[0-9]{6}`, `NONCE := [0-9a-f]{8}`, and `BASE := WPI-<UTCSTAMP>Z-<NONCE>` with exact widths of 15, 8, and 29 ASCII bytes respectively. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:76-96`)

| Field | Draft value/status | Exact derivation | Source |
|---|---|---|---|
| `UTCSTAMP` | **MUST BE MINTED AT COMMIT TIME** | `$utc` from §2 | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:80-94` |
| `NONCE` | **MUST BE MINTED AT COMMIT TIME** | `$nonce` from §2; exactly four cryptographic-random bytes rendered as eight lowercase hex characters | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:80-94` |
| `BASE` / `BASE_RUN` | **MUST BE MINTED AT COMMIT TIME** | `$base = "WPI-${utc}Z-${nonce}"` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:80-94`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/transport_runner.ps1:79-90` |
| P0 `RUNID` | **MUST BE MINTED AT COMMIT TIME** | `$p0Runid = "${base}-P0"` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-106`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh:112-117` |
| RO `RUNID` | **MUST BE MINTED AT COMMIT TIME** | `$roRunid = "${base}-RO"` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-106`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh:106-111` |
| P0 `EV_STAGE_ID` | Exact value derivable today: `p0` | `$p0StageId = 'p0'` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-106`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh:112-117` |
| RO `EV_STAGE_ID` | Exact value derivable today: `ro` | `$roStageId = 'ro'` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-106`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh:106-111` |
| remote-base leaf | **MUST BE MINTED AT COMMIT TIME** | `$remoteBaseLeaf = "wpi_staging_${base}"` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-106` |
| `REMOTE_BASE` | **MUST BE MINTED AT COMMIT TIME** | `$remoteBase = "/home/gatea/${remoteBaseLeaf}"` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md:120-129`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv:2-4` |
| confirmation token | **MUST BE MINTED AT COMMIT TIME** | `$confirmToken = "${base}-EXECUTE"` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-106`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/transport_runner.ps1:79-90` |
| operator-record leaf | **MUST BE MINTED AT COMMIT TIME** | `$operatorLeaf = "WPI_TRANSPORT_${base}"` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-106` |
| operator record root | **MUST BE MINTED AT COMMIT TIME** | `$operatorRoot = "C:\WPI_ARTIFACTS\${operatorLeaf}"` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md:675-690`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/transport_runner.ps1:79-90` |

All values derived from `BASE` must be derived once rather than independently typed, and all named components must pass the pinned component predicate before any consumer is populated. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-114`)

## 2. Exact commit-time generator and derivation

Run this block exactly once in the real allocation session. Preserve the literal command, PowerShell version, stdout, stderr, rc, and resulting values in the real record. The generator and those recording requirements are fixed by the successor draft. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:80-94`)

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

$p0Runid       = "${base}-P0"
$roRunid       = "${base}-RO"
$p0StageId     = 'p0'
$roStageId     = 'ro'
$remoteBaseLeaf = "wpi_staging_${base}"
$remoteBase    = "/home/gatea/${remoteBaseLeaf}"
$confirmToken  = "${base}-EXECUTE"
$operatorLeaf  = "WPI_TRANSPORT_${base}"
$operatorRoot  = "C:\WPI_ARTIFACTS\${operatorLeaf}"

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

Do not test the literal placeholder as if it were a concrete identifier. The component predicate has no length limit; the fixed generator widths provide the length contract. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:80-106`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:80-105`)

## 3. Grammar and predicate record

### 3.1 Pinned predicate identity

Before sourcing the predicate, the selected `RP0-LIB.sh` object must be exactly **18,968 bytes** with SHA-256 `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48`. Both wrappers pin that digest. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-104`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh:125-128`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh:119-122`)

Pinned `RP0-LIB.sh` materialized path at commit time: **UNKNOWN**. Settle it by selecting the exact final runkit source object and requiring the byte-count and SHA-256 checks below to pass before sourcing it. The review identifies the predicate semantics and explains that execution authority attaches to the extracted member matching the pinned digest, not to an unproved copy. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:17-49`)

```powershell
$PinnedRp0Lib = '<EXACT-MATERIALIZED-PATH-TO-PINNED-RP0-LIB.sh>'
if (-not (Test-Path -LiteralPath $PinnedRp0Lib -PathType Leaf)) { throw 'RP0_LIB_MISSING_STOP' }
if ((Get-Item -LiteralPath $PinnedRp0Lib).Length -ne 18968) { throw 'RP0_LIB_BYTES_STOP' }
$rp0Sha = (Get-FileHash -LiteralPath $PinnedRp0Lib -Algorithm SHA256).Hash.ToLowerInvariant()
if ($rp0Sha -cne '4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48') { throw 'RP0_LIB_SHA256_STOP' }
```

Under `LC_ALL=C`, the accepted language is one or more ASCII characters from `[A-Za-z0-9._-]`, with no leading `-`, excluding the complete strings `.` and `..`; there is no predicate length check. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:36-76`)

### 3.2 Required acceptance results

Each real result below is **MUST BE EXECUTED AT COMMIT TIME**. Preserve the literal invocation, separate stdout and stderr, and rc. Every row must return exactly rc `0` and contain the expected `component_ok` reason token. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:116-135`)

| Name passed to predicate | Value passed | Required result | Actual stdout | Actual stderr | Actual rc |
|---|---|---|---|---|---|
| `BASE` | `$base` | `component_ok`, rc 0 | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** |
| `P0_RUNID` | `$p0Runid` | `component_ok`, rc 0 | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** |
| `RO_RUNID` | `$roRunid` | `component_ok`, rc 0 | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** |
| `P0_EV_STAGE_ID` | `p0` | `component_ok`, rc 0 | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** |
| `RO_EV_STAGE_ID` | `ro` | `component_ok`, rc 0 | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** |
| `REMOTE_BASE_LEAF` | `$remoteBaseLeaf` | `component_ok`, rc 0 | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** |
| `CONFIRM_TOKEN` | `$confirmToken` | `component_ok`, rc 0 | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** |
| `OPERATOR_RECORD_LEAF` | `$operatorLeaf` | `component_ok`, rc 0 | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** | **MUST BE RECORDED AT COMMIT TIME** |

### 3.3 Required refusal representatives

These are finite refusal representatives, not the complete refusal set. The empty value must be supplied as an explicit empty second argument. Every row must preserve stdout, stderr, and rc and match the named token exactly. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:116-135`)

| Class | Exact Bash value expression | Required result | Actual result |
|---|---|---|---|
| empty | `''` | rc 1, `component_reserved` | **MUST BE RECORDED AT COMMIT TIME** |
| dot | `'.'` | rc 1, `component_reserved` | **MUST BE RECORDED AT COMMIT TIME** |
| dot-dot | `'..'` | rc 1, `component_reserved` | **MUST BE RECORDED AT COMMIT TIME** |
| leading dash | `'-lead'` | rc 1, `component_leading_dash` | **MUST BE RECORDED AT COMMIT TIME** |
| POSIX separator | `'a/b'` | rc 1, `component_charset` | **MUST BE RECORDED AT COMMIT TIME** |
| backslash | `'a\b'` | rc 1, `component_charset` | **MUST BE RECORDED AT COMMIT TIME** |
| whitespace | `'bad name'` | rc 1, `component_charset` | **MUST BE RECORDED AT COMMIT TIME** |
| control byte | `$'bad\x01name'` | rc 1, `component_charset` | **MUST BE RECORDED AT COMMIT TIME** |
| non-ASCII bytes under `LC_ALL=C` | `$'caf\xC3\xA9'` | rc 1, `component_charset` | **MUST BE RECORDED AT COMMIT TIME** |
| glob metacharacter | `'bad*name'` | rc 1, `component_charset` | **MUST BE RECORDED AT COMMIT TIME** |

After §2 has generated the values, run the complete matrix below through a pinned Bash executable. It preserves separate stdout/stderr files for every literal invocation and returns nonzero on the first rc/token mismatch. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:129-147`)

```powershell
$BashExe = '<PINNED-BASH-EXECUTABLE>'
$QaDir = '<RUN-OWNED-ALLOCATION-TRANSCRIPT-DIRECTORY>'
if (-not (Test-Path -LiteralPath $BashExe -PathType Leaf)) { throw 'BASH_MISSING_STOP' }
if (Test-Path -LiteralPath $QaDir) { throw 'QA_DIR_ALREADY_EXISTS_STOP' }
[void](New-Item -ItemType Directory -Path $QaDir)

$qaScript = @'
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

run_case() {
    case_name=$1
    value=$2
    expected_rc=$3
    expected_token=$4
    stdout_file="$out_dir/$case_name.stdout"
    stderr_file="$out_dir/$case_name.stderr"
    set +e
    rp0_require_safe_component "$case_name" "$value" >"$stdout_file" 2>"$stderr_file"
    actual_rc=$?
    set -e
    printf 'case=%s expected_rc=%s actual_rc=%s expected_token=%s\n' \
        "$case_name" "$expected_rc" "$actual_rc" "$expected_token"
    [ "$actual_rc" -eq "$expected_rc" ] || return 97
    token_seen=0
    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in *"$expected_token"*) token_seen=1 ;; esac
    done < "$stdout_file"
    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in *"$expected_token"*) token_seen=1 ;; esac
    done < "$stderr_file"
    [ "$token_seen" -eq 1 ] || return 98
}

run_case BASE                 "$base"          0 component_ok
run_case P0_RUNID             "$p0_runid"      0 component_ok
run_case RO_RUNID             "$ro_runid"      0 component_ok
run_case P0_EV_STAGE_ID       "$p0_stage"      0 component_ok
run_case RO_EV_STAGE_ID       "$ro_stage"      0 component_ok
run_case REMOTE_BASE_LEAF     "$remote_leaf"   0 component_ok
run_case CONFIRM_TOKEN        "$confirm_token" 0 component_ok
run_case OPERATOR_RECORD_LEAF "$operator_leaf" 0 component_ok

run_case REFUSE_EMPTY          ''                 1 component_reserved
run_case REFUSE_DOT            '.'                1 component_reserved
run_case REFUSE_DOT_DOT        '..'               1 component_reserved
run_case REFUSE_LEADING_DASH   '-lead'            1 component_leading_dash
run_case REFUSE_POSIX_SEP      'a/b'              1 component_charset
run_case REFUSE_BACKSLASH      'a\b'              1 component_charset
run_case REFUSE_WHITESPACE     'bad name'         1 component_charset
run_case REFUSE_CONTROL        $'bad\x01name'     1 component_charset
run_case REFUSE_NON_ASCII      $'caf\xC3\xA9'    1 component_charset
run_case REFUSE_GLOB           'bad*name'         1 component_charset
'@

& $BashExe --noprofile --norc -c $qaScript 'wpi-allocation-grammar' `
    $PinnedRp0Lib $QaDir $base $p0Runid $roRunid $p0StageId $roStageId `
    $remoteBaseLeaf $confirmToken $operatorLeaf `
    1>(Join-Path $QaDir 'matrix.stdout') 2>(Join-Path $QaDir 'matrix.stderr')
$matrixRc = $LASTEXITCODE
if ($matrixRc -ne 0) { throw "GRAMMAR_MATRIX_STOP rc=$matrixRc" }
```

Any wrong rc, missing/incorrect reason token, unrecorded stream, or non-replayable command is a grammar self-QA STOP. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:116-135`)

## 4. Collision record

### 4.1 Required collision universe

Before allocation proceeds, the candidate `BASE`, P0 RUNID, and RO RUNID must be absent from the complete append-only ledger history and all retained operator/remote-root records. The minimum named retained operator roots are `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08` and its `-R45B` successor, but those two roots alone are not a global uniqueness proof. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`)

Canonical repository path of `WPI_RUNID_ALLOCATION_BURN_LEDGER.md`: **UNKNOWN**. The read source mandates a committed ledger by filename but does not establish its canonical repo-relative location. Settle this before minting by having the Lead select the canonical path, establish its historical completeness, and commit the ledger contract; absence or incompleteness is `COLLISION_SCAN_STOP`, never “no collision.” (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-145`)

Authoritative retained remote-allocation record path and completeness proof: **UNKNOWN**. Settle this before minting by naming the exact retained record, proving its completeness, and making it available to the collision scan without performing unpreregistered host contact. The Stage-1 order requires allocation before Commit 1 and allows the exact host capture only after Commit 1. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:495-533`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-52`)

### 4.2 Exact pre-allocation collision procedure

Run this after generation and grammar acceptance but before writing the identifiers into any consumer or ledger row. Supply the two UNKNOWN paths only after the Lead has resolved them. The candidate operator root is create-once, and the remote base later remains protected by create-once allocation; neither substitutes for the global history scan. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:184-209`)

```powershell
param(
    [Parameter(Mandatory=$true)][string] $CanonicalLedgerPath,
    [Parameter(Mandatory=$true)][string] $RetainedRemoteAllocationRecord,
    [string] $OperatorArchiveRoot = 'C:\WPI_ARTIFACTS'
)

$ErrorActionPreference = 'Stop'
$ids = @($base, $p0Runid, $roRunid)

foreach ($required in @($CanonicalLedgerPath, $RetainedRemoteAllocationRecord)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "COLLISION_SCAN_STOP missing_required_record=$required"
    }
}
if (-not (Test-Path -LiteralPath $OperatorArchiveRoot -PathType Container)) {
    throw "COLLISION_SCAN_STOP missing_operator_archive=$OperatorArchiveRoot"
}

foreach ($id in $ids) {
    foreach ($record in @($CanonicalLedgerPath, $RetainedRemoteAllocationRecord)) {
        $hits = @(Select-String -LiteralPath $record -SimpleMatch -Pattern $id)
        if ($hits.Count -ne 0) {
            throw "COLLISION id=$id record=$record"
        }
    }

    $nameHits = @(Get-ChildItem -LiteralPath $OperatorArchiveRoot -Force -Recurse |
        Where-Object { $_.FullName.IndexOf($id, [StringComparison]::Ordinal) -ge 0 })
    if ($nameHits.Count -ne 0) {
        throw "COLLISION id=$id surface=operator_path"
    }

    & rg -a -n -F --hidden --no-messages -- $id $OperatorArchiveRoot
    $rgRc = $LASTEXITCODE
    if ($rgRc -eq 0) { throw "COLLISION id=$id surface=operator_content" }
    if ($rgRc -ne 1) { throw "COLLISION_SCAN_STOP id=$id rg_rc=$rgRc" }
}

if (Test-Path -LiteralPath $operatorRoot) {
    throw "COLLISION path=$operatorRoot"
}

'COLLISION_RESULT=NO_HIT_IN_DECLARED_UNIVERSE'
```

Record the real result here:

| Check | Actual result |
|---|---|
| canonical ledger current contents | **MUST BE RECORDED AT COMMIT TIME** |
| canonical ledger complete history | **MUST BE RECORDED AT COMMIT TIME** |
| retained remote-allocation record | **MUST BE RECORDED AT COMMIT TIME** |
| all retained operator path names | **MUST BE RECORDED AT COMMIT TIME** |
| all retained operator record contents | **MUST BE RECORDED AT COMMIT TIME** |
| exact candidate operator root | **MUST BE RECORDED AT COMMIT TIME** |

A collision, an incomplete scan, or an unevaluable scan means the generated base and both RUNIDs are unusable: append a `BURNED` disposition, do not retry any consumer with those identifiers, and require a fresh preregistration with newly generated identities. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`)

The later remote create-once result must also be appended to the disposition history. A pre-existing remote tree is not permission to reuse the spelling. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md:131-156`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_setup_wpi.sh:221-237`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_setup_wpi.sh:395-414`)

## 5. Append-only allocation dispositions

One ledger row must carry the base, both RUNIDs, generator timestamp, nonce, disposition (`RESERVED`, `BURNED`, or `SPENT`), reason, successor identity, and evidence/record roots. Existing rows are never edited or deleted; a state change appends a new row referring to its prior row. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`)

Use the following columns in the canonical ledger:

| Row ref | Prior row ref | `BASE` | P0 `RUNID` | RO `RUNID` | generator UTCSTAMP | nonce | disposition | reason | successor identity | remote evidence root | operator record root |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MUST BE ASSIGNED APPEND-ONLY** | `NONE` | **MUST BE MINTED AT COMMIT TIME** | **MUST BE MINTED AT COMMIT TIME** | **MUST BE MINTED AT COMMIT TIME** | **MUST BE MINTED AT COMMIT TIME** | **MUST BE MINTED AT COMMIT TIME** | `RESERVED` only after every pre-allocation check passes | exact reservation reason and check-record identity | **UNKNOWN — settle before commit as described below** | `$remoteBase/evidence` | `$operatorRoot` |

Meaning of `successor identity` for the initial `RESERVED` row: **UNKNOWN**. The read source requires the field but does not define whether it is a document-byte identity, a future Git object ID, or another non-self-referential identity. Settle before commit by defining an identity computable before the row is committed, or by preregistering an append-only post-commit binding row; never embed a commit's own not-yet-existing object ID. The two-commit design explicitly forbids commit-ID self-reference and instead binds each commit after creation through clean-current-`HEAD` evidence. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:550-579`)

Exact trigger for transition to `SPENT`: **UNKNOWN**. The read source names `SPENT` as a permitted disposition but does not define the event that causes that transition. Settle before commit by adding one exact, evidence-bound transition rule. Do not infer it from successful allocation or adjacent run facts. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`)

Required transition templates:

| Event | Append-only action |
|---|---|
| grammar, pinned-predicate, equality, collision, fill, commit, or remote create-once failure | Append a new `BURNED` row with the exact reason and prior-row reference; never edit the `RESERVED` row and never retry those identifiers. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`) |
| exact `SPENT` trigger | **UNKNOWN — MUST BE DEFINED BEFORE COMMIT**; once defined and evidenced, append a `SPENT` row with the prior-row reference. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`) |

## 6. Per-consumer equality result

The real record must name every consumer individually and prove declared count = observed count = equal count. Duplicate keys, unregistered occurrences, missing consumers, independently typed values, or a count mismatch are freeze STOP. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:108-114`)

Actual manifest/result: **MUST BE PRODUCED AT COMMIT TIME**. At minimum it covers both wrappers, the runner's `$BASE_RUN`, `$CONFIRM_TOKEN`, and `$RECORD_ROOT`, every `TRANSPORT_PLAN.tsv` occurrence, remote/retrieval/local-binding paths, record-root leaf, stage IDs, and evidence-tree leaves. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:34-52`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:108-114`)

Targeted fills must use an allowlist of exact `(file, constant-or-table-field)` sites; a file-wide or repository-wide marker replacement is forbidden. Guard literals remain byte-identical while no marker may remain in a consumer. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:54-60`)

## 7. Lead checklist to create the committed allocation record

- [ ] Confirm the work is still local-only and that no host, network, SSH, deployment, credential, trading, or economic action is being taken while producing the allocation record. (`C:\tmp\lane_kick\L1.md:65-71`)
- [ ] Resolve the canonical committed path and completeness contract for `WPI_RUNID_ALLOCATION_BURN_LEDGER.md`; STOP if it is missing or incomplete. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-145`)
- [ ] Resolve the authoritative retained remote-allocation record usable before Commit 1; STOP rather than contact the host under an uncommitted procedure. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:495-533`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-52`)
- [ ] Define the non-self-referential initial `successor identity` and the exact evidence-bound `SPENT` trigger; leave neither UNKNOWN in the committed record. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:550-579`)
- [ ] Start a transcript that preserves the literal generator command, PowerShell version, separate stdout/stderr, rc, and every generated/derived value. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:80-94`)
- [ ] Execute §2 exactly once; derive every field from the single `BASE`; do not independently type a RUNID, token, root, or leaf. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-106`)
- [ ] Verify the selected `RP0-LIB.sh` is exactly 18,968 bytes with SHA-256 `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` before sourcing it under `LC_ALL=C`. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-104`)
- [ ] Execute and preserve all eight acceptance rows and all ten refusal representatives; STOP on any wrong rc/token or missing stream. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:116-135`)
- [ ] Run the complete pre-allocation collision procedure against the canonical ledger, its complete history, every retained operator record/path, and the authoritative retained remote-allocation record. Record exact commands, inputs, outputs, and rc. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`)
- [ ] On any grammar, predicate, collision, equality, fill, or commit failure, append `BURNED`, stop, and do not retry the same identifiers. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`)
- [ ] After all pre-allocation checks pass, append the initial `RESERVED` ledger row with every required field; do not edit or delete any prior row. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-145`)
- [ ] Populate only the exact allowlisted consumer sites and generate the equality manifest with declared count = observed count = equal count. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:34-60`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:108-114`)
- [ ] Self-verify that the completed allocation record contains concrete values, generator evidence, grammar/refusal results, collision results, equality counts, and the append-only disposition row, with no unresolved token or UNKNOWN. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-70`; `C:\tmp\lane_kick\L1.md:45-62`)
- [ ] Commit the completed local allocation record and ledger update under the Lead's authorized Git sequence. This commit alone grants no host action; the exact attestation-only preregistration must still become Commit 1 before the owner-approved capture can run. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-52`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:495-533`)

Boundary: this draft performs and authorizes no host, network, SSH, deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or economic action. (`C:\tmp\lane_kick\L1.md:65-71`)
