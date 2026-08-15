# R16 and R23 freeze procedures

Status: procedure material for the Lead and owner; no gate verdict, acceptance,
authorization, host action, or deployment action is made here. The readiness
sources likewise say that Audit 2 reviews an already frozen checkpoint and does
not create it, and that the readiness package creates neither freeze nor
authority. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:5-7`;
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:3-6`

## 1. The distinction that must survive every handoff

| Row | Boundary and purpose | What follows it |
|---|---|---|
| **R16** | Freeze the **pre-WP-A checkpoint** only after Packet 9/WP-I closure is complete and immutable. It is the SHA and initial Packet-10 identity input that Audit 2 reviews; Audit 2 does not create it. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54-56`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:47-57,119-120` | Complete the remaining Packet-10/11 inputs, dispatch Audit 2, and only after an accepting Audit-2 close may WP-A begin. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:20-31` |
| **R23** | Freeze the **final exact release SHA/artifact after WP-A evidence** and after the ordered staging-host discard record. The final release contains accepted WP-S/WP-L/WP-I/WP-A material plus any permitted contingency repairs. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:973-977`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:61-63` | Audit 3 plus Gate 6 reviews that exact final SHA/artifact and the captured evidence; Gate B and any separately approved WP-V are later steps. `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:617-620`; `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:976-980` |

**Non-conflation rule:** R16 is a pre-WP-A audit checkpoint; R23 is a later,
post-WP-A final-release freeze. R16 cannot contain the not-yet-produced WP-A
evidence, while R23 must bind the captured WP-A evidence package and the exact
artifact that later reviews name. The catalogue itself calls R23 distinct from
R16. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55,61-63`

## 2. Identity rule shared by both freezes

The repository declares `* text=auto`. `.gitattributes:1-2` The documented
failure mode is that a text file can have different Git-object LF bytes and
Windows working-tree CRLF bytes; one prior table mixed the forms and could not be
reproduced by either one derivation method. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:8-27`

Accordingly, neither procedure publishes a bare `bytes / SHA-256` pair for a
tracked file. Every tracked row is labelled **`GIT_OBJECT`** and records the blob
OID, Git-object byte count, and SHA-256 of the exact blob bytes. Every artifact or
manifest that will be consumed from a Windows checkout additionally gets a
**`WORKTREE_RAW`** byte count and SHA-256. Every non-Git evidence file is labelled
**`RAW_EXTERNAL_FILE`**. This follows the repository's standing rule to state the
derivation mode and either give both forms or pin the blob OID.
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:46-64`

The following PowerShell helpers are the normative byte derivations used by both
procedures. They capture Git blob stdout as bytes and never pass it through a
text pipeline.

```powershell
function Get-GitBlobIdentity {
    param(
        [Parameter(Mandatory)][string]$Repo,
        [Parameter(Mandatory)][string]$Rev,
        [Parameter(Mandatory)][string]$Path
    )

    $spec = "${Rev}:$Path"
    $oid = (& git -C $Repo rev-parse --verify $spec).Trim()
    if ($LASTEXITCODE -ne 0 -or $oid -notmatch '^[0-9a-f]{40,64}$') {
        throw "Cannot resolve blob OID: $spec"
    }

    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = 'git'
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    foreach ($arg in @('-C', $Repo, 'cat-file', 'blob', $spec)) {
        [void]$psi.ArgumentList.Add($arg)
    }
    $proc = [Diagnostics.Process]::Start($psi)
    $buffer = [IO.MemoryStream]::new()
    $proc.StandardOutput.BaseStream.CopyTo($buffer)
    $stderr = $proc.StandardError.ReadToEnd()
    $proc.WaitForExit()
    if ($proc.ExitCode -ne 0) { throw "git cat-file failed: $stderr" }

    $bytes = $buffer.ToArray()
    $hasher = [Security.Cryptography.SHA256]::Create()
    try {
        $sha256 = [Convert]::ToHexString($hasher.ComputeHash($bytes)).ToLowerInvariant()
    } finally {
        $hasher.Dispose()
        $buffer.Dispose()
    }

    [pscustomobject]@{
        mode = 'GIT_OBJECT'
        path = $Path
        blob_oid = $oid
        bytes = $bytes.Length
        sha256 = $sha256
    }
}

function Get-RawFileIdentity {
    param(
        [Parameter(Mandatory)][string]$LiteralPath,
        [Parameter(Mandatory)][ValidateSet('WORKTREE_RAW','RAW_EXTERNAL_FILE')][string]$Mode,
        [Parameter(Mandatory)][string]$DisplayPath
    )
    $item = Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
    [pscustomobject]@{
        mode = $Mode
        path = $DisplayPath
        blob_oid = '-'
        bytes = $item.Length
        sha256 = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}

function Write-Utf8Lf {
    param([Parameter(Mandatory)][string]$Path, [Parameter(Mandatory)][string[]]$Lines)
    $utf8NoBom = [Text.UTF8Encoding]::new($false)
    [IO.File]::WriteAllText($Path, (($Lines -join "`n") + "`n"), $utf8NoBom)
}
```

For each freeze, create a new create-once evidence directory **outside the
repository**, replace every angle-bracket token below, record the literal command
transcript, stdout, stderr, and return code, and stop on any failed required
comparison. This document does not select or authorize a storage location.

## 3. R16 — pre-WP-A checkpoint freeze

### 3.1 Exact trigger condition

R16 may start only when all of the following are true:

1. Packet 9 is complete and immutable, including its WP-I closure record and final
   evidence index; the pre-WP-A checkpoint is frozen only afterward.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:39-41,106-120`
2. A concrete commit containing that closure is available as the proposed R16
   checkpoint; a pre-freeze working-tree description is not a substitute.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:72-77`;
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:180-185`
3. The Lead has pinned the comparison base, product-candidate commit, complete
   in-scope path list, complete artifact/manifest path list, Packet-9 closure and
   index paths, and an external create-once output root. Packet 10 requires every
   in-scope frozen file and every final artifact/manifest identity, but the read
   sources do not provide the future concrete member paths. Therefore those
   concrete paths are **UNKNOWN** until the Lead publishes the adopted scope and
   identity-path inputs; that publication settles the unknown.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-61,126-130`
4. The exact R16 comparison base is **UNKNOWN** in the read sources: they require
   a base SHA and exact base-to-freeze diff but do not name the future base. A
   Lead-adopted full base SHA in the freeze input record settles it; do not choose
   one from adjacency.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-56`;
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:51-56`

### 3.2 Required inputs

Prepare one UTF-8/LF input file, `R16_SCOPE_AND_IDENTITIES.tsv`, outside the
repository. Each non-comment line is `ROLE<TAB>REPO_RELATIVE_PATH`, where `ROLE`
is one of `scope`, `artifact`, or `manifest`. `artifact` and `manifest` rows are
also scope rows. The file must include the Packet-9 closure/index and every
in-scope file; it must not contain placeholders. The source requires the frozen
file list, every final artifact/manifest path/bytes/SHA-256, and their binding to
the full freeze SHA. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-60`

Set and record these values:

```powershell
$Repo          = '<isolated clean worktree at the proposed R16 commit>'
$Out           = '<new create-once external directory for R16 freeze records>'
$BaseSha       = '<full Lead-adopted R16 comparison-base commit>'
$CandidateSha  = '<full product-candidate commit>'
$ScopeInput    = '<absolute path to R16_SCOPE_AND_IDENTITIES.tsv>'
$Packet9Close  = '<repo-relative Packet-9 closure-record path>'
$Packet9Index  = '<repo-relative Packet-9 final-evidence-index path>'
```

### 3.3 Command sequence and published identity set

#### R16-1 — prove and publish the checkpoint SHA

```powershell
if (Test-Path -LiteralPath $Out) { throw "Create-once output already exists: $Out" }
[void](New-Item -ItemType Directory -Path $Out)

$FreezeSha = (& git -C $Repo rev-parse --verify 'HEAD^{commit}').Trim()
$ResolvedBase = (& git -C $Repo rev-parse --verify "$BaseSha^{commit}").Trim()
$ResolvedCandidate = (& git -C $Repo rev-parse --verify "$CandidateSha^{commit}").Trim()
if ($LASTEXITCODE -ne 0) { throw 'A required commit identity did not resolve' }

$status = @(& git -C $Repo status --porcelain=v1 --untracked-files=all)
if ($LASTEXITCODE -ne 0 -or $status.Count -ne 0) { throw 'Freeze worktree is not clean' }

Write-Utf8Lf (Join-Path $Out 'R16_COMMITS.txt') @(
    "R16_FREEZE_SHA=$FreezeSha",
    "R16_BASE_SHA=$ResolvedBase",
    "PRODUCT_CANDIDATE_SHA=$ResolvedCandidate"
)
```

The full checkpoint SHA must be repeated identically in the bundle manifest and
each later Audit-2 dispatch. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-53`

#### R16-2 — publish the exact base-to-freeze diff

```powershell
$BaseDiff = Join-Path $Out 'R16_BASE_TO_FREEZE.patch'
& git -C $Repo --no-pager diff --binary --full-index --no-ext-diff `
    --output=$BaseDiff $ResolvedBase $FreezeSha --
if ($LASTEXITCODE -ne 0) { throw 'Cannot generate base-to-freeze diff' }

& git -C $Repo --no-pager diff --quiet --no-ext-diff $ResolvedBase $FreezeSha --
$BaseDiffRc = $LASTEXITCODE
if ($BaseDiffRc -notin 0,1) { throw "Diff comparison failed rc=$BaseDiffRc" }
$BaseDiffId = Get-RawFileIdentity $BaseDiff 'RAW_EXTERNAL_FILE' 'R16_BASE_TO_FREEZE.patch'
Write-Utf8Lf (Join-Path $Out 'R16_BASE_TO_FREEZE_IDENTITY.tsv') @(
    "comparison`tbase`tfreeze`tdiff_rc`tpatch_bytes`tpatch_sha256",
    "R16_BASE_TO_FREEZE`t$ResolvedBase`t$FreezeSha`t$BaseDiffRc`t$($BaseDiffId.bytes)`t$($BaseDiffId.sha256)"
)
```

The patch is required even when empty; an unchanged conclusion follows from the
exact comparison and never replaces it. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:54,94-100`

#### R16-3 — publish the full tracked tree and frozen in-scope identity table

```powershell
$TrackedTree = Join-Path $Out 'R16_FULL_TRACKED_TREE.txt'
$trackedLines = @(& git -C $Repo ls-tree -r --full-tree $FreezeSha)
if ($LASTEXITCODE -ne 0) { throw 'Cannot enumerate full tracked tree' }
Write-Utf8Lf $TrackedTree $trackedLines

$rows = Get-Content -LiteralPath $ScopeInput |
    Where-Object { $_ -and -not $_.StartsWith('#') } |
    ForEach-Object {
        $parts = $_ -split "`t", 2
        if ($parts.Count -ne 2 -or $parts[0] -notin @('scope','artifact','manifest')) {
            throw "Invalid scope row: $_"
        }
        [pscustomobject]@{ role=$parts[0]; path=$parts[1] }
    }
$rows = @($rows | Sort-Object path,role -Unique)
if ($rows.Count -eq 0) { throw 'Empty frozen scope' }
if ($rows.path -notcontains $Packet9Close -or $rows.path -notcontains $Packet9Index) {
    throw 'Packet-9 closure/index absent from frozen scope'
}

$identityLines = [Collections.Generic.List[string]]::new()
[void]$identityLines.Add("freeze_sha`trole`tmode`tpath`tblob_oid`tbytes`tsha256")
foreach ($row in $rows) {
    $gitId = Get-GitBlobIdentity $Repo $FreezeSha $row.path
    [void]$identityLines.Add("$FreezeSha`t$($row.role)`t$($gitId.mode)`t$($row.path)`t$($gitId.blob_oid)`t$($gitId.bytes)`t$($gitId.sha256)")

    if ($row.role -in @('artifact','manifest')) {
        $raw = Get-RawFileIdentity (Join-Path $Repo $row.path) 'WORKTREE_RAW' $row.path
        [void]$identityLines.Add("$FreezeSha`t$($row.role)`t$($raw.mode)`t$($row.path)`t-`t$($raw.bytes)`t$($raw.sha256)")
    }
}
Write-Utf8Lf (Join-Path $Out 'R16_FROZEN_SCOPE_IDENTITIES.tsv') $identityLines
```

`R16_FULL_TRACKED_TREE.txt` is the complete commit tree (`mode type OID path`).
`R16_FROZEN_SCOPE_IDENTITIES.tsv` is the required frozen in-scope file list and
contains the candidate-adjacent artifacts/manifests in explicit Git-object and
materialized working-tree modes. The authoritative Audit-2 bundle must carry the
actual diff and frozen files, without unfrozen working-tree substitution.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:55-57`;
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:44-56`

#### R16-4 — bind Packet 9 and candidate ancestry

```powershell
& git -C $Repo cat-file -e "${FreezeSha}:$Packet9Close"
if ($LASTEXITCODE -ne 0) { throw 'Packet-9 closure is not in R16 freeze' }
& git -C $Repo cat-file -e "${FreezeSha}:$Packet9Index"
if ($LASTEXITCODE -ne 0) { throw 'Packet-9 evidence index is not in R16 freeze' }

& git -C $Repo merge-base --is-ancestor $ResolvedCandidate $FreezeSha
$CandidateAncestorRc = $LASTEXITCODE
if ($CandidateAncestorRc -notin 0,1) { throw 'Candidate ancestry check failed' }
Write-Utf8Lf (Join-Path $Out 'R16_BINDINGS.txt') @(
    "packet9_closure_path=$Packet9Close",
    "packet9_index_path=$Packet9Index",
    "candidate_is_ancestor_rc=$CandidateAncestorRc"
)
```

This records the observed binding result; it does not convert a non-ancestor
result into acceptance. Packet 10 must consume the already immutable Packet-9
closure/evidence rather than recreate it. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:58-60`

#### R16-5 — derive unchanged bits or publish the exact candidate diff

```powershell
$candidatePaths = @($rows | Where-Object role -in @('artifact','manifest') | Select-Object -ExpandProperty path -Unique)
if ($candidatePaths.Count -eq 0) { throw 'No artifact/manifest paths were pinned' }

$CandidateDiff = Join-Path $Out 'R16_CANDIDATE_TO_FREEZE.patch'
& git -C $Repo --no-pager diff --binary --full-index --no-ext-diff `
    --output=$CandidateDiff $ResolvedCandidate $FreezeSha -- @candidatePaths
if ($LASTEXITCODE -ne 0) { throw 'Cannot generate candidate-to-freeze diff' }

& git -C $Repo --no-pager diff --quiet --no-ext-diff `
    $ResolvedCandidate $FreezeSha -- @candidatePaths
$CandidateDiffRc = $LASTEXITCODE
if ($CandidateDiffRc -notin 0,1) { throw "Candidate comparison failed rc=$CandidateDiffRc" }

$conclusion = if ($CandidateDiffRc -eq 0) {
    'UNCHANGED: listed tracked artifact/manifest Git blobs are identical between PRODUCT_CANDIDATE_SHA and R16_FREEZE_SHA'
} else {
    'CHANGED: see R16_CANDIDATE_TO_FREEZE.patch and identity table; no unchanged-bits claim is made'
}
Write-Utf8Lf (Join-Path $Out 'R16_UNCHANGED_BITS.txt') @(
    "candidate=$ResolvedCandidate",
    "freeze=$FreezeSha",
    "diff_rc=$CandidateDiffRc",
    "conclusion=$conclusion"
)
```

The comparison must be against the frozen identities; a pre-freeze description
is unacceptable. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:72-77`

#### R16-6 — publish one manifest and its detached identity

```powershell
$members = Get-ChildItem -LiteralPath $Out -File | Sort-Object Name
$manifestLines = [Collections.Generic.List[string]]::new()
[void]$manifestLines.Add("freeze_sha`tderivation_mode`tmember`tbytes`tsha256")
foreach ($member in $members) {
    if ($member.Name -eq 'R16_FREEZE_MANIFEST.tsv' -or $member.Name -eq 'R16_FREEZE_MANIFEST.sha256') { continue }
    $id = Get-RawFileIdentity $member.FullName 'RAW_EXTERNAL_FILE' $member.Name
    [void]$manifestLines.Add("$FreezeSha`tRAW_EXTERNAL_FILE`t$($member.Name)`t$($id.bytes)`t$($id.sha256)")
}
$manifest = Join-Path $Out 'R16_FREEZE_MANIFEST.tsv'
Write-Utf8Lf $manifest $manifestLines
$manifestId = Get-RawFileIdentity $manifest 'RAW_EXTERNAL_FILE' 'R16_FREEZE_MANIFEST.tsv'
Write-Utf8Lf (Join-Path $Out 'R16_FREEZE_MANIFEST.sha256') @("$($manifestId.sha256)  R16_FREEZE_MANIFEST.tsv")
```

Packet 10 ultimately requires one authoritative dispatch manifest with the same
full frozen SHA and every handed input path/bytes/SHA and role for both auditors.
R16 supplies the initial freeze members; R17-R20 later add the still-missing
baseline, Packet-11 identity, and final bundle membership rather than pretending
R16 alone completes Packet 10. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-67,119-122`;
`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55-60`

### 3.4 R16 auditor honesty verification

An auditor independently performs all of these checks:

1. Create a separate audit-only worktree at `R16_FREEZE_SHA`; record exact HEAD
   equality and empty `git status --porcelain` before and after review. A SHA
   mismatch or non-empty result is BLOCK under the Audit-2 input contract.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`
2. Re-run R16-2 and byte-compare the independently generated patch with
   `R16_BASE_TO_FREEZE.patch`; independently recompute its bytes/SHA-256 and the
   diff return code. The unchanged statement is valid only if the exact diff and
   all listed artifact/manifest identities support it.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-57,94-100`
3. Re-run `git ls-tree -r --full-tree R16_FREEZE_SHA`; compare every line to the
   published tracked tree. Re-run `Get-GitBlobIdentity` for every scope row and
   require blob OID, blob byte count, and blob SHA-256 equality. For each artifact
   and manifest, also recompute `WORKTREE_RAW`; do not compare a CRLF hash to an
   LF hash. The earlier mixed-mode table demonstrates why this distinction is
   mandatory. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:15-27,48-64`
4. Verify the adopted scope input has no placeholder, duplicate, omitted Packet-9
   closure/index, or manifest member absent from the frozen identity table.
   Recompute the Packet-9 closure/index identities from the frozen commit and the
   immutable evidence members through the index; copied digest strings without
   recomputation access are insufficient.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:65-70`;
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:58-60`
5. Recompute `R16_FREEZE_MANIFEST.tsv` member-by-member and its detached SHA-256;
   require the same `R16_FREEZE_SHA` on every row. Each Audit-2 session must
   receive the actual diff/files and same authoritative frozen inputs, not an
   implementer transcript or the other auditor's output.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:16-18,44-49`

### 3.5 R16 estimate

**NO SOURCED ESTIMATE.** The catalogue gives no hours for R16 and directs the
future operator to produce an exact freeze procedure and time a dry run; no
numeric estimate is derived here. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55`

## 4. R23 — final exact SHA/artifact freeze

### 4.1 Exact trigger condition

R23 may start only when all of the following records already exist and are
identified by path/bytes/SHA-256:

1. The R16 freeze and later accepting Audit-2 close precede WP-A; the procedure
   verifies those records but makes no acceptance decision.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:81-83`;
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:24-31`
2. WP-A is complete and all required staging evidence has been captured.
   `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:973-975`
3. The staging-host discard record exists and says discard occurred only after
   WP-A completion and evidence capture. The ordered plan puts discard at step 6
   and final freeze at step 7.
   `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:974-977,1021-1023`
4. Every contingency repair intended for the final release is already present in
   the proposed commit. After host discard, a change outside WP-A runtime paths
   requires an explicit invariant-impact statement and Lead confirmation before
   refreeze/re-audit; a change that invalidates executed-Ubuntu evidence is BLOCK
   pending a new Gate-A-class authorization and must not enter this freeze as if
   the old evidence still applied.
   `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:982-984,1026-1028`
5. The Lead has pinned the complete final scope, artifact/manifest membership,
   WP-A evidence root, evidence-index path, discard-record path, R16 freeze SHA,
   exact WP-A-tested artifact identity, and a new create-once output root. The
   future concrete member paths and artifact identity are **UNKNOWN** in the read
   sources; an adopted final scope/identity input and closed WP-A evidence index
   settle them. The plan requires commit ancestry, exact path manifest, and
   artifact hash. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1021-1025`

For R23 the normative base is the published **R16 freeze SHA**, so the required
base-to-freeze comparison is explicitly `R16_FREEZE_SHA -> R23_FREEZE_SHA`. This
is a procedure definition, not a claim that the two are equal. Any owner/Lead
contract that chooses a different R23 comparison base must name it explicitly and
must still retain the separate R16-to-R23 comparison so the two freezes cannot be
merged. The sequence establishing R16 before Audit 2/WP-A and R23 afterward is
fixed. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55,60-63`;
`MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:617-620`

### 4.2 Required inputs

Prepare `R23_SCOPE_AND_IDENTITIES.tsv` in the same `ROLE<TAB>PATH` format as R16,
with no placeholder and with every final artifact and manifest. Prepare exact
paths to the prior records and immutable WP-A evidence root:

```powershell
$Repo              = '<isolated clean worktree at the proposed R23 commit>'
$Out               = '<new create-once external directory for R23 freeze records>'
$R16FreezeSha      = '<full SHA copied from verified R16 manifest>'
$CandidateSha      = '<full final product-candidate commit, if distinct from R23 commit>'
$ScopeInput        = '<absolute path to R23_SCOPE_AND_IDENTITIES.tsv>'
$Audit2Close       = '<repo-relative accepting Audit-2 close-record path>'
$WpaEvidenceRoot   = '<immutable read-only WP-A evidence root>'
$WpaEvidenceIndex  = '<path to WP-A evidence index>'
$DiscardRecord     = '<path to ordered staging-host discard record>'
$WpaArtifactPath   = '<artifact path named by WP-A evidence>'
$WpaArtifactBytes  = '<exact WP-A-tested raw artifact byte count>'
$WpaArtifactSha256 = '<exact WP-A-tested raw artifact SHA-256>'
```

### 4.3 Command sequence and published identity set

#### R23-1 — prove and publish the final SHA and ancestry

```powershell
if (Test-Path -LiteralPath $Out) { throw "Create-once output already exists: $Out" }
[void](New-Item -ItemType Directory -Path $Out)

$FreezeSha = (& git -C $Repo rev-parse --verify 'HEAD^{commit}').Trim()
$ResolvedBase = (& git -C $Repo rev-parse --verify "$R16FreezeSha^{commit}").Trim()
$ResolvedCandidate = (& git -C $Repo rev-parse --verify "$CandidateSha^{commit}").Trim()
$status = @(& git -C $Repo status --porcelain=v1 --untracked-files=all)
if ($LASTEXITCODE -ne 0 -or $status.Count -ne 0) { throw 'Final-freeze worktree is not clean' }

& git -C $Repo merge-base --is-ancestor $ResolvedBase $FreezeSha
$R16AncestorRc = $LASTEXITCODE
if ($R16AncestorRc -ne 0) { throw 'R16 freeze is not an ancestor of proposed R23 freeze' }

Write-Utf8Lf (Join-Path $Out 'R23_COMMITS.txt') @(
    "R23_FREEZE_SHA=$FreezeSha",
    "R23_BASE_R16_SHA=$ResolvedBase",
    "FINAL_PRODUCT_CANDIDATE_SHA=$ResolvedCandidate",
    "r16_is_ancestor_rc=$R16AncestorRc"
)
```

The final release identity later required by Gate B is the exact final SHA,
artifact, ancestry, path manifest, and artifact hash. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1021-1025`

#### R23-2 — publish the exact R16-to-R23 diff

Run R16-2 with `$ResolvedBase = $R16FreezeSha`, `$FreezeSha` equal to R23 HEAD,
and output names `R23_R16_TO_FINAL.patch` and
`R23_R16_TO_FINAL_IDENTITY.tsv`. Preserve the exact binary/full-index patch even
when it is empty. The resulting patch is the R23 base-to-freeze diff and is also
the first guard against silently treating R16 and R23 as one freeze. The required
order is R16/Audit 2, WP-A, then R23. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55,60-63`

#### R23-3 — publish the final tracked tree and final scope identities

Run R16-3 with `R23_SCOPE_AND_IDENTITIES.tsv` and output names
`R23_FULL_TRACKED_TREE.txt` and `R23_FROZEN_SCOPE_IDENTITIES.tsv`. Every tracked
scope row gets `GIT_OBJECT` blob OID/bytes/SHA-256; every final artifact/manifest
also gets `WORKTREE_RAW` bytes/SHA-256. The identity mode rule is mandatory
because `* text=auto` makes an unqualified text-file pair ambiguous.
`.gitattributes:1-2`;
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:59-64`

#### R23-4 — freeze the complete WP-A evidence package in raw external-file mode

```powershell
$evidenceLines = [Collections.Generic.List[string]]::new()
[void]$evidenceLines.Add("mode`trelative_path`tbytes`tsha256")
$evidenceFiles = @(Get-ChildItem -LiteralPath $WpaEvidenceRoot -Recurse -File |
    Sort-Object FullName)
if ($evidenceFiles.Count -eq 0) { throw 'WP-A evidence root is empty' }

foreach ($file in $evidenceFiles) {
    $relative = [IO.Path]::GetRelativePath($WpaEvidenceRoot, $file.FullName).Replace('\','/')
    $id = Get-RawFileIdentity $file.FullName 'RAW_EXTERNAL_FILE' $relative
    [void]$evidenceLines.Add("$($id.mode)`t$relative`t$($id.bytes)`t$($id.sha256)")
}
Write-Utf8Lf (Join-Path $Out 'R23_WPA_EVIDENCE_IDENTITIES.tsv') $evidenceLines

$indexId = Get-RawFileIdentity $WpaEvidenceIndex 'RAW_EXTERNAL_FILE' `
    ([IO.Path]::GetFileName($WpaEvidenceIndex))
$discardId = Get-RawFileIdentity $DiscardRecord 'RAW_EXTERNAL_FILE' `
    ([IO.Path]::GetFileName($DiscardRecord))
Write-Utf8Lf (Join-Path $Out 'R23_ORDER_RECORD_IDENTITIES.tsv') @(
    "role`tmode`tpath`tbytes`tsha256",
    "wpa_evidence_index`t$($indexId.mode)`t$($indexId.path)`t$($indexId.bytes)`t$($indexId.sha256)",
    "staging_host_discard_record`t$($discardId.mode)`t$($discardId.path)`t$($discardId.bytes)`t$($discardId.sha256)"
)
```

The later artifact/evidence reviews operate on the exact frozen SHA/artifact plus
the captured staging evidence and do not recreate Ubuntu evidence.
`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:976-977,1023-1025`

#### R23-5 — prove whether the final artifact is the WP-A-tested artifact

```powershell
$finalArtifact = Join-Path $Repo $WpaArtifactPath
$finalId = Get-RawFileIdentity $finalArtifact 'WORKTREE_RAW' $WpaArtifactPath
$matchesWpa = ($finalId.bytes -eq [int64]$WpaArtifactBytes -and
               $finalId.sha256 -eq $WpaArtifactSha256.ToLowerInvariant())

$artifactConclusion = if ($matchesWpa) {
    'UNCHANGED: final WORKTREE_RAW artifact bytes and SHA-256 equal the WP-A-tested identity'
} else {
    'CHANGED: final artifact does not equal the WP-A-tested identity; exact identities recorded; no evidence-validity claim is made'
}
Write-Utf8Lf (Join-Path $Out 'R23_WPA_TO_FINAL_ARTIFACT.tsv') @(
    "path`tcomparison_mode`twpa_bytes`twpa_sha256`tfinal_bytes`tfinal_sha256`tmatch",
    "$WpaArtifactPath`tWORKTREE_RAW`t$WpaArtifactBytes`t$($WpaArtifactSha256.ToLowerInvariant())`t$($finalId.bytes)`t$($finalId.sha256)`t$matchesWpa",
    "conclusion`t$artifactConclusion"
)
```

If `match=False`, publish the exact final identity and the applicable file/binary
diff; do not write an unchanged-bits statement. Before later gates, the Lead must
classify whether the change is provably outside WP-A runtime paths or invalidates
executed evidence. An evidence-invalidating change after discard blocks the path
rather than inheriting the old evidence. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:982-984,1026-1028`

#### R23-6 — derive the tracked unchanged-bits statement or exact diff

Run R16-5 twice:

1. Compare `$R16FreezeSha` to `$FreezeSha` across every R23 `artifact` and
   `manifest` path; publish `R23_R16_ARTIFACTS_TO_FINAL.patch` and a conclusion.
2. Compare `$ResolvedCandidate` to `$FreezeSha` across the same paths; publish
   `R23_CANDIDATE_TO_FINAL.patch` and a conclusion.

An `UNCHANGED` sentence is permitted only for a comparison whose exact patch is
empty **and** whose corresponding identity rows match. Otherwise the exact patch
and before/after identity rows are the result. The final release must contain any
accepted contingency repairs and cannot rely on acceptance from a previous
SHA/artifact. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:976-984`

#### R23-7 — publish the final manifest and detached identity

Run R16-6 with output names `R23_FREEZE_MANIFEST.tsv` and
`R23_FREEZE_MANIFEST.sha256`, including every R23 commit/diff/tree/scope,
WP-A-evidence, order-record, artifact-comparison, and unchanged/diff record. Every
manifest row carries the same `R23_FREEZE_SHA`; every member is explicitly
`RAW_EXTERNAL_FILE`, while the nested identity tables state `GIT_OBJECT`,
`WORKTREE_RAW`, or `RAW_EXTERNAL_FILE` for their subjects.

### 4.4 R23 auditor honesty verification

An auditor independently performs all of these checks:

1. Create an isolated worktree at `R23_FREEZE_SHA`; require exact HEAD, empty
   pre/post status, and `git merge-base --is-ancestor R16_FREEZE_SHA
   R23_FREEZE_SHA` rc 0. Exact-worktree and cleanliness checks are the established
   frozen-SHA audit contract. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`
2. Independently regenerate and byte-compare the full tracked tree, every
   `GIT_OBJECT` identity, every `WORKTREE_RAW` artifact/manifest identity, and all
   three tracked diffs: R16-to-R23 full diff, R16-to-final artifact/manifest diff,
   and candidate-to-final artifact/manifest diff. Require blob OIDs so no LF/CRLF
   ambiguity can be hidden. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:48-64`
3. Re-enumerate the immutable WP-A evidence root, recompute every
   `RAW_EXTERNAL_FILE` byte count/SHA-256, and compare the evidence index and
   discard-record identities. Access to recompute the immutable source is
   required; copied digests alone do not establish honesty.
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:65-70`
4. Verify from the frozen order records that Audit 2 closed before WP-A began,
   WP-A completed before discard, all required evidence was captured before
   discard, and discard preceded R23 publication. The ordered plan fixes these
   boundaries. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:973-977`;
   `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:81-83`
5. Independently hash the final materialized artifact and compare it with the
   WP-A-tested bytes/SHA-256. If different, reproduce the exact delta and require
   the recorded invariant-impact classification; never infer that old WP-A
   evidence covers new runtime-affecting bytes. A post-audit change that
   invalidates executed evidence blocks Gate B. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1023-1028`
6. Recompute `R23_FREEZE_MANIFEST.tsv` and its detached SHA-256 and require no
   missing or extra handed member. Audit 3 and Gate 6 must review this exact
   frozen SHA/artifact and captured evidence package, not R16 and not an
   unfrozen successor. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:976-980,1023-1025`

### 4.5 R23 estimate

**NO SOURCED ESTIMATE.** The catalogue gives no disjoint price for the final
exact-SHA/artifact freeze and directs the future operator to time a frozen
identity/build procedure. No numeric estimate is derived here.
`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:62`

## 5. Stop conditions common to both procedures

Stop without publishing the freeze as honest if any required input is still a
placeholder/UNKNOWN; a commit does not resolve; the worktree is dirty; the scope
or artifact/manifest list is empty/incomplete; a listed path is absent; any
identity fails to reproduce in its labelled derivation mode; the base diff cannot
be generated; the Packet-9/WP-A evidence source cannot be independently
recomputed; or an unchanged statement conflicts with a non-empty diff or unequal
identity. The frozen-SHA bundle must be derived from the exact checkpoint and
must not be inferred from a pre-freeze tree.
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:180-185`;
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:65-77`

For R23 specifically, stop if R16 is not an ancestor, the ordered WP-A/evidence/
discard records are missing, or any post-discard change invalidates executed
evidence. The plan requires a new owner Gate-A-class staging authorization for
the latter case; this procedure supplies none. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:982-984,1026-1028`
