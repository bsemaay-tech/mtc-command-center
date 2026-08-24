[CmdletBinding()]
param(
    [string]$RepoRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$ExpectedBranch = 'feature/wp-p0-02-tag-freezes-20260825'
$ExpectedEvidenceRefs = 174
$FreezeDate = '2026-08-25'
$BridgeAcceptedSha = 'be007fd802bbfd2eb181d66038c374865d1562ee'

if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..\..')).Path
}
else {
    $RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
}

$EvidenceInput = Join-Path $RepoRoot 'MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_01_INVENTORY_2026-08-24\evidence_branches.md'
$BeforeOutput = Join-Path $PSScriptRoot 'TAGS_BEFORE.txt'
$AfterOutput = Join-Path $PSScriptRoot 'TAGS_AFTER.txt'
$ManifestOutput = Join-Path $PSScriptRoot 'TAG_MANIFEST.txt'

function Invoke-GitRequired {
    param([Parameter(Mandatory)][string[]]$Arguments)

    $output = @(& git -C $RepoRoot @Arguments 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed (rc=$LASTEXITCODE): $($output -join [Environment]::NewLine)"
    }
    return $output
}

function Resolve-Commit {
    param([Parameter(Mandatory)][string]$Revision)

    $output = @(Invoke-GitRequired -Arguments @('rev-parse', '--verify', "$Revision`^{commit}"))
    $sha = ([string]$output[0]).Trim()
    if ($sha -notmatch '^[0-9a-f]{40}$') {
        throw "Revision did not resolve to one full commit SHA: $Revision -> $sha"
    }
    return $sha
}

function Resolve-PathHead {
    param(
        [Parameter(Mandatory)][string]$BaseRevision,
        [Parameter(Mandatory)][string]$Path
    )

    $output = @(Invoke-GitRequired -Arguments @('log', '-1', '--format=%H', $BaseRevision, '--', $Path))
    $sha = ([string]$output[0]).Trim()
    if ($sha -notmatch '^[0-9a-f]{40}$') {
        throw "No path HEAD commit resolved for $Path at $BaseRevision"
    }
    return $sha
}

function Get-Subject {
    param([Parameter(Mandatory)][string]$Commit)

    $output = @(Invoke-GitRequired -Arguments @('show', '-s', '--format=%s', $Commit))
    return (([string]$output[0]) -replace "[`r`n`t]", ' ').Trim()
}

function Write-TagListSnapshot {
    param([Parameter(Mandatory)][string]$Path)

    $tags = @(Invoke-GitRequired -Arguments @('tag', '--list', '--sort=refname'))
    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add('# Command: git tag --list --sort=refname')
    $lines.Add("# Count: $($tags.Count)")
    foreach ($tag in $tags) {
        $lines.Add([string]$tag)
    }
    [System.IO.File]::WriteAllLines($Path, $lines, $Utf8NoBom)
    return $tags
}

function Test-TagExists {
    param([Parameter(Mandatory)][string]$TagName)

    & git -C $RepoRoot show-ref --verify --quiet "refs/tags/$TagName"
    return ($LASTEXITCODE -eq 0)
}

function Assert-ValidTagName {
    param([Parameter(Mandatory)][string]$TagName)

    & git -C $RepoRoot check-ref-format "refs/tags/$TagName" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Invalid tag name derived during preflight: $TagName"
    }
}

$actualRootOutput = @(Invoke-GitRequired -Arguments @('rev-parse', '--show-toplevel'))
$actualRoot = ([string]$actualRootOutput[0]).Trim()
if ([System.IO.Path]::GetFullPath($actualRoot) -ne [System.IO.Path]::GetFullPath($RepoRoot)) {
    throw "Repo root mismatch: requested=$RepoRoot actual=$actualRoot"
}

$branchOutput = @(Invoke-GitRequired -Arguments @('branch', '--show-current'))
$branch = ([string]$branchOutput[0]).Trim()
if ($branch -ne $ExpectedBranch) {
    throw "Wrong branch: expected=$ExpectedBranch actual=$branch"
}

if (-not (Test-Path -LiteralPath $EvidenceInput -PathType Leaf)) {
    throw "Missing WP-P0-01 evidence input: $EvidenceInput"
}

# Parse the entire evidence table. The Evidence-bearing field is column 5.
$allEvidenceRows = [System.Collections.Generic.List[object]]::new()
foreach ($line in [System.IO.File]::ReadAllLines($EvidenceInput)) {
    if ($line -notmatch '^\| (refs/(?:heads|remotes)/[^|]+) \| ([0-9a-f]{40}) \|') {
        continue
    }
    $columns = $line.Split('|')
    if ($columns.Count -lt 8) {
        throw "Malformed evidence table row: $line"
    }
    $allEvidenceRows.Add([pscustomobject]@{
        Ref = $columns[1].Trim()
        DocumentedTip = $columns[2].Trim()
        Evidence = $columns[5].Trim()
    })
}

$evidenceRows = @($allEvidenceRows | Where-Object Evidence -eq 'YES')
if ($allEvidenceRows.Count -ne 317) {
    throw "WP-P0-01 ref census changed or failed to parse: expected=317 actual=$($allEvidenceRows.Count)"
}
if ($evidenceRows.Count -ne $ExpectedEvidenceRefs) {
    throw "WP-P0-01 evidence ref count changed: expected=$ExpectedEvidenceRefs actual=$($evidenceRows.Count)"
}

$masterRef = 'refs/heads/master'
$masterSha = Resolve-Commit -Revision $masterRef

$desired = [System.Collections.Generic.List[object]]::new()
function Add-DesiredTag {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Target,
        [Parameter(Mandatory)][string]$Description,
        [Parameter(Mandatory)][string]$Message,
        [string]$SourceRef = '',
        [string]$DocumentedTip = ''
    )

    Assert-ValidTagName -TagName $Name
    $desired.Add([pscustomobject]@{
        Name = $Name
        Target = $Target
        Description = $Description
        Message = $Message
        SourceRef = $SourceRef
        DocumentedTip = $DocumentedTip
    })
}

Add-DesiredTag -Name "legacy/master-freeze/$FreezeDate" -Target $masterSha `
    -Description "current local master ($masterRef); subject: $(Get-Subject -Commit $masterSha)" `
    -Message "WP-P0-02 freeze $FreezeDate`: current master"

$componentPaths = @(
    [pscustomobject]@{
        Name = "legacy/pine-controller/$FreezeDate"
        Path = 'MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine'
        Label = 'Pine controller path HEAD'
        Message = "WP-P0-02 freeze $FreezeDate`: Pine controller"
    },
    [pscustomobject]@{
        Name = "legacy/mtc-v2-kernel/$FreezeDate"
        Path = 'MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core'
        Label = 'MTC_V2 Python kernel core path HEAD'
        Message = "WP-P0-02 freeze $FreezeDate`: MTC_V2 kernel"
    },
    [pscustomobject]@{
        Name = "legacy/02-mtc-backtest/$FreezeDate"
        Path = 'MTC_COMMAND_CENTER/02_MTC_BACKTEST'
        Label = '02_MTC_BACKTEST tree path HEAD'
        Message = "WP-P0-02 freeze $FreezeDate`: 02_MTC_BACKTEST"
    },
    [pscustomobject]@{
        Name = "legacy/parity-oracles/$FreezeDate"
        Path = 'MTC_COMMAND_CENTER/12_PARITY_PINETS'
        Label = 'historical parity oracle set path HEAD'
        Message = "WP-P0-02 freeze $FreezeDate`: parity oracle set"
    }
)

foreach ($component in $componentPaths) {
    $sha = Resolve-PathHead -BaseRevision $masterRef -Path $component.Path
    Add-DesiredTag -Name $component.Name -Target $sha `
        -Description "$($component.Label): $($component.Path); subject: $(Get-Subject -Commit $sha)" `
        -Message $component.Message
}

$bridgeSha = Resolve-Commit -Revision $BridgeAcceptedSha
Add-DesiredTag -Name "legacy/bridge-v1-accepted/$FreezeDate" -Target $bridgeSha `
    -Description "accepted and deployed Bridge V1 release; recorded SHA $BridgeAcceptedSha; subject: $(Get-Subject -Commit $bridgeSha)" `
    -Message "WP-P0-02 freeze $FreezeDate`: accepted Bridge V1 candidate"

foreach ($row in $evidenceRows) {
    if ($row.Ref.StartsWith('refs/heads/')) {
        $branchName = $row.Ref.Substring('refs/heads/'.Length)
    }
    elseif ($row.Ref.StartsWith('refs/remotes/')) {
        # Preserve the remote name (for example origin/foo) so a local and its
        # remote-tracking ref receive distinct, auditable tags.
        $branchName = $row.Ref.Substring('refs/remotes/'.Length)
    }
    else {
        throw "Unsupported evidence ref namespace: $($row.Ref)"
    }

    $sanitized = $branchName -replace '/', '--'
    $tagName = "legacy/evbr/$sanitized/$FreezeDate"
    $currentTip = Resolve-Commit -Revision $row.Ref
    $drift = if ($currentTip -eq $row.DocumentedTip) { 'no' } else { "yes (WP-P0-01 tip $($row.DocumentedTip))" }
    Add-DesiredTag -Name $tagName -Target $currentTip `
        -Description "evidence-bearing branch $branchName; source ref $($row.Ref); tip drift since WP-P0-01: $drift; subject: $(Get-Subject -Commit $currentTip)" `
        -Message "WP-P0-02 freeze $FreezeDate`: evidence-bearing branch $branchName" `
        -SourceRef $row.Ref -DocumentedTip $row.DocumentedTip
}

$collisions = @($desired | Group-Object Name | Where-Object Count -gt 1)
if ($collisions.Count -ne 0) {
    throw "Tag-name collision(s) after sanitization: $($collisions.Name -join ', ')"
}
if ($desired.Count -ne ($ExpectedEvidenceRefs + 6)) {
    throw "Desired tag conservation failure: expected=$($ExpectedEvidenceRefs + 6) actual=$($desired.Count)"
}

$before = @(Write-TagListSnapshot -Path $BeforeOutput)
$manifestRows = [System.Collections.Generic.List[string]]::new()
$manifestRows.Add("status`ttag`ttarget_sha`ttarget_description")
$created = 0
$existingSame = 0
$existingDifferent = 0

foreach ($item in $desired) {
    $status = ''
    if (Test-TagExists -TagName $item.Name) {
        $existingTarget = Resolve-Commit -Revision "refs/tags/$($item.Name)"
        if ($existingTarget -eq $item.Target) {
            $status = 'EXISTING_SAME_TARGET'
            $existingSame++
        }
        else {
            $status = "SKIPPED_EXISTING_DIFFERENT_TARGET(actual=$existingTarget)"
            $existingDifferent++
        }
    }
    else {
        Invoke-GitRequired -Arguments @('tag', '-a', $item.Name, $item.Target, '-m', $item.Message) | Out-Null
        $objectTypeOutput = @(Invoke-GitRequired -Arguments @('cat-file', '-t', "refs/tags/$($item.Name)"))
        $objectType = ([string]$objectTypeOutput[0]).Trim()
        $createdTarget = Resolve-Commit -Revision "refs/tags/$($item.Name)"
        if ($objectType -ne 'tag' -or $createdTarget -ne $item.Target) {
            throw "Post-create verification failed for $($item.Name): type=$objectType target=$createdTarget expected=$($item.Target)"
        }
        $status = 'CREATED'
        $created++
    }

    $manifestRows.Add("$status`t$($item.Name)`t$($item.Target)`t$($item.Description)")
}

[System.IO.File]::WriteAllLines($ManifestOutput, $manifestRows, $Utf8NoBom)
$after = @(Write-TagListSnapshot -Path $AfterOutput)

$actualAdded = $after.Count - $before.Count
if ($actualAdded -ne $created) {
    throw "Tag count delta does not equal created count: before=$($before.Count) after=$($after.Count) created=$created"
}

Write-Output "WP-P0-02 tag run complete"
Write-Output "desired=$($desired.Count) evidence=$($evidenceRows.Count) created=$created existing_same=$existingSame existing_different=$existingDifferent"
Write-Output "tags_before=$($before.Count) tags_after=$($after.Count)"
