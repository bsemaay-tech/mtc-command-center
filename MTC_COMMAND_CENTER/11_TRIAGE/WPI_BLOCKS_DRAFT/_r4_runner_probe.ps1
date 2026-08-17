# Transport round-4 runner probe: F1 marker family and F4 per-branch prerequisites.
#
# This is NOT a re-implementation of the runner. It EXTRACTS named regions of a
# transport_runner.ps1 file verbatim - the outcome-grammar constants, the marker
# family map, the prerequisite map, the provenance test, the prerequisite
# resolver, the classifier, the per-op classification/counter block and the
# run rollup - and executes those exact bytes against injected per-op (rc,
# capture) pairs. The SHA-256 and line range of every extracted region is
# printed, so the reader can confirm the code under test is the file's own.
#
# RED is produced by extracting the SAME regions from the round-3 accepted bytes
# (commit 78173bfd), not by narrating what round 3 would have done.
#
# No host is contacted, no ssh/scp process is started, and no plan is executed.
# Captures are written to real files under a temp directory because the
# provenance test reads files; that is the only side effect.
#
# Windows PowerShell 5.1 compatible.

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string] $RunnerPath,
    [Parameter(Mandatory=$true)][ValidateSet('round3','round4')][string] $Variant,
    [Parameter(Mandatory=$true)][string] $WorkDir
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$text = [System.IO.File]::ReadAllText($RunnerPath)
$allLines = $text.Split([char]10)

function Get-Sha256OfString([string] $s) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { $h = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($s)) } finally { $sha.Dispose() }
    $sb = New-Object System.Text.StringBuilder
    foreach ($b in $h) { [void]$sb.Append($b.ToString('x2')) }
    return $sb.ToString()
}

# Extract [startAnchor .. endAnchor+extra] as verbatim source. Both anchors must
# match exactly once, so a region cannot be silently mis-sliced.
function Extract-Region([string] $name, [string] $startAnchor, [string] $endAnchor, [int] $extra) {
    $startIdx = -1; $endIdx = -1; $startHits = 0; $endHits = 0
    for ($i = 0; $i -lt $allLines.Length; $i++) {
        $line = $allLines[$i].TrimEnd([char]13)
        if ($line -eq $startAnchor) { $startHits++; if ($startIdx -lt 0) { $startIdx = $i } }
        if ($line -eq $endAnchor) { $endHits++; if ($endIdx -lt 0 -and $i -ge $startIdx -and $startIdx -ge 0) { $endIdx = $i } }
    }
    if ($startHits -ne 1) { throw ('start anchor for ' + $name + ' matched ' + $startHits + ' times: ' + $startAnchor) }
    if ($endHits -ne 1) { throw ('end anchor for ' + $name + ' matched ' + $endHits + ' times: ' + $endAnchor) }
    if ($endIdx -lt $startIdx) { throw ('end anchor precedes start anchor for ' + $name) }
    $last = $endIdx + $extra
    $slice = @()
    for ($i = $startIdx; $i -le $last; $i++) { $slice += $allLines[$i].TrimEnd([char]13) }
    $src = ($slice -join "`n")
    # Written straight to the console, not to the pipeline: a Write-Output here
    # would be returned alongside the region source and corrupt it.
    [Console]::Out.WriteLine('REGION name=' + $name + ' lines=' + ($startIdx + 1) + '-' + ($last + 1) + ' sha256=' + (Get-Sha256OfString $src))
    return $src
}

# Extract from a unique start anchor until the brace nesting the region opened
# returns to zero. Used where the region's last line ('    }') is not unique.
function Extract-Balanced([string] $name, [string] $startAnchor) {
    $startIdx = -1; $startHits = 0
    for ($i = 0; $i -lt $allLines.Length; $i++) {
        if ($allLines[$i].TrimEnd([char]13) -eq $startAnchor) { $startHits++; if ($startIdx -lt 0) { $startIdx = $i } }
    }
    if ($startHits -ne 1) { throw ('start anchor for ' + $name + ' matched ' + $startHits + ' times: ' + $startAnchor) }
    $open = 0; $close = 0; $seen = $false; $last = -1
    for ($i = $startIdx; $i -lt $allLines.Length; $i++) {
        foreach ($ch in $allLines[$i].ToCharArray()) {
            if ($ch -eq '{') { $open++; $seen = $true } elseif ($ch -eq '}') { $close++ }
        }
        if ($seen -and $open -eq $close) { $last = $i; break }
    }
    if ($last -lt 0) { throw ('region ' + $name + ' never balanced') }
    $slice = @()
    for ($i = $startIdx; $i -le $last; $i++) { $slice += $allLines[$i].TrimEnd([char]13) }
    $src = ($slice -join "`n")
    # Written straight to the console, not to the pipeline: a Write-Output here
    # would be returned alongside the region source and corrupt it.
    [Console]::Out.WriteLine('REGION name=' + $name + ' lines=' + ($startIdx + 1) + '-' + ($last + 1) + ' sha256=' + (Get-Sha256OfString $src))
    return $src
}

Write-Output ('RUNNER path=' + $RunnerPath)
Write-Output ('RUNNER sha256=' + (Get-FileHash -LiteralPath $RunnerPath -Algorithm SHA256).Hash.ToLowerInvariant())
Write-Output ('VARIANT ' + $Variant)

if ($Variant -eq 'round4') {
    $rConstants = Extract-Region 'constants+marker_family+prereq_map' '$REMOTE_OUTCOME_RCS = @(0, 1, 3)' "    '12' = @('08', '10')" 1
    $rFunctions = Extract-Region 'provenance+prereq_resolver+classifier' 'function Test-RemoteProvenanceMarkerForOp($op, [string] $outFile, [string] $errFile) {' "    return @{ Class = 'deviant'; Reason = 'operation_ran_and_observed_deviant_state' }" 1
    $rPrereq    = Extract-Balanced 'per_op_prerequisite_resolution' "    if (`$op.RunWhen -eq 'always') {"
    $rClassify  = Extract-Balanced 'per_op_classification_and_counters' '    $outcome = Get-OpOutcomeClass $op $rc $outFile $errFile $prerequisite'
} else {
    $rConstants = Extract-Region 'constants+global_marker_set' '$REMOTE_OUTCOME_RCS = @(0, 1, 3)' "    'ROW_', 'ROW ', 'CLOSE_', 'CLOSE '" 1
    $rFunctions = Extract-Region 'provenance+classifier' 'function Test-RemoteProvenanceMarker([string] $outFile, [string] $errFile) {' "    return @{ Class = 'deviant'; Reason = 'operation_ran_and_observed_deviant_state' }" 1
    $rPrereq    = Extract-Region 'global_prerequisite_snapshot' '    $prerequisiteEstablished = $sequenceOk' '    $prerequisiteEstablished = $sequenceOk' 0
    $rClassify  = Extract-Balanced 'per_op_classification_and_counters' '    $outcome = Get-OpOutcomeClass $op $rc $outFile $errFile $prerequisiteEstablished'
}
$rRollup = Extract-Balanced 'run_class_and_rollup' "Emit ('TR_RUN_CLASS deviant=' + `$deviantCount + ' not_evaluable=' + `$notEvaluableCount + ' precedence=deviant_outranks_not_evaluable')"

# The classification region ends at the first line that is exactly four spaces
# and a closing brace; verify the slice is balanced before executing it.
function Assert-Balanced([string] $name, [string] $src) {
    $open = 0; $close = 0
    foreach ($ch in $src.ToCharArray()) { if ($ch -eq '{') { $open++ } elseif ($ch -eq '}') { $close++ } }
    if ($open -ne $close) { throw ('region ' + $name + ' is not brace-balanced: ' + $open + ' open, ' + $close + ' close') }
}
Assert-Balanced 'constants' $rConstants
Assert-Balanced 'functions' $rFunctions
Assert-Balanced 'prereq' $rPrereq
Assert-Balanced 'classify' $rClassify
Assert-Balanced 'rollup' $rRollup

# --- the harness's own scaffolding -------------------------------------------
# Emit is the runner's own name for its record writer; here it collects lines.
$script:Out = New-Object System.Collections.ArrayList
function Emit([string] $line) { [void]$script:Out.Add($line) }
$BASE_RUN = 'PROBE-BASE-RUN'
$RECORD_ROOT = $WorkDir

Invoke-Expression $rConstants
Invoke-Expression $rFunctions

# The 12 preregistered operations, in plan order, with the stdin leaf each row
# actually names. Only the fields the extracted code reads are modelled.
function New-ProbeOps {
    $rows = @(
        @('01','ssh_stdin','sequence_ok','remote_setup_wpi.sh'),
        @('02','scp_up','sequence_ok',''),
        @('03','ssh_stdin','sequence_ok','remote_extract_verify_wpi.sh'),
        @('04','ssh_stdin','sequence_ok','run_p0.sh'),
        @('05','ssh_stdin','sequence_ok','run_ro.sh'),
        @('06','tcp_probe','sequence_ok',''),
        @('07','ssh_stdin','always','remote_close_tree_wpi.sh'),
        @('08','ssh_stdin','always','remote_close_tree_wpi.sh'),
        @('09','scp_down','always',''),
        @('10','scp_down','always',''),
        @('11','local_bind','always',''),
        @('12','local_bind','always','')
    )
    $list = New-Object System.Collections.ArrayList
    foreach ($r in $rows) {
        [void]$list.Add(@{ Id=$r[0]; Kind=$r[1]; RunWhen=$r[2]; StdinLeaf=$r[3]; ExpectRc=0 })
    }
    return $list
}

function Invoke-ProbeFixture([string] $title, $injected) {
    $script:Out = New-Object System.Collections.ArrayList
    $ops = New-ProbeOps
    $sequenceOk = $true
    $anyDeviant = $false
    $anyNotEvaluable = $false
    $deviantCount = 0
    $notEvaluableCount = 0
    $firstMismatch = ''
    $firstNotEvaluable = ''
    $classById = @{}
    $prerequisite = $null
    $prerequisiteEstablished = $true

    foreach ($op in $ops) {
        $outFile = Join-Path $WorkDir ($op.Id + '.stdout')
        $errFile = Join-Path $WorkDir ($op.Id + '.stderr')
        if ($op.RunWhen -eq 'sequence_ok' -and -not $sequenceOk) {
            Emit ('TR_OP_SKIPPED id=' + $op.Id + ' reason=prior_sequence_mismatch')
            $classById[$op.Id] = 'skipped'
            continue
        }
        $rc = [int]$injected[$op.Id][0]
        [System.IO.File]::WriteAllText($outFile, ([string]$injected[$op.Id][1] + "`n"))
        [System.IO.File]::WriteAllText($errFile, "`n")
        Invoke-Expression $rPrereq
        Invoke-Expression $rClassify
    }
    Invoke-Expression $rRollup
    Write-Output ('=== ' + $title + ' [' + $Variant + '] ===')
    foreach ($l in $script:Out) { Write-Output ('  ' + $l) }
    Write-Output ('  PROBE_EXIT_CODE=' + $exitCode)
    Write-Output ''
}

# --- fixtures ----------------------------------------------------------------
$SETUP   = 'SETUP PASS base=/home/gatea/wpi_staging_X evidence=/home/gatea/wpi_staging_X/evidence runkit=/home/gatea/wpi_staging_X/evidence/runkit kit=/home/gatea/wpi_staging_X/kit work=/home/gatea/wpi_staging_X/work'
$EXTRACT = 'EXTRACT PASS archive=/home/gatea/wpi_staging_X/kit/runkit.tar'
$P0W     = 'P0W done runid=X-P0'
$P0WSTOP = 'P0W_STOP reason=execution_domain_unattested field=user_namespace detail=preregistered_value_missing'
$ROW     = 'ROW done runid=X-RO'
$ROWFAIL = 'ROW_FAIL reason=interpreter_is_symlink path=/opt/mtc-bridge/venvs/2ce41e34/bin/python'
$TCP     = 'B6_external row=24 outcome=connection_refused host=172.24.55.233 port=8790 payload_bytes=0'
$CLOSE_OK   = 'CLOSE PASS runid=X-P0 dir=/home/gatea/wpi_staging_X/evidence/runkit/X-P0 files=3 wrote_into_evidence_tree=0'
$CLOSE_STOP = 'CLOSE_STOP reason=work_root_missing_or_not_directory path=/home/gatea/wpi_staging_X/work'
$CLOSE_FAIL = 'CLOSE_FAIL reason=evidence_tree_non_regular_entries=[/home/gatea/wpi_staging_X/evidence/runkit/X-RO/straylink]'

# Fixture A - the decisive F4 case named in the Codex final audit and the Lead's
# adjudication: ops 01-06 all match, the P0 close STOPs, and the INDEPENDENT RO
# close returns a genuine marked CLOSE_FAIL rc 1. The RO deviation must be
# counted (deviant>=1, run FAIL), not erased by the unrelated P0 STOP.
$fixtureA = @{
    '01'=@(0,$SETUP); '02'=@(0,''); '03'=@(0,$EXTRACT); '04'=@(0,$P0W); '05'=@(0,$ROW); '06'=@(0,$TCP);
    '07'=@(3,$CLOSE_STOP); '08'=@(1,$CLOSE_FAIL); '09'=@(0,''); '10'=@(0,''); '11'=@(3,''); '12'=@(3,'')
}

# Fixture B - the scenario the accepting Claude audit defended: a genuinely
# unestablished prerequisite. The P0 stage (op 04) STOPs, so op 07 has nothing
# to close and its rc 1 must stay not-evaluable rather than becoming a FAIL.
$fixtureB = @{
    '01'=@(0,$SETUP); '02'=@(0,''); '03'=@(0,$EXTRACT); '04'=@(3,$P0WSTOP); '05'=@(0,$ROW); '06'=@(0,$TCP);
    '07'=@(1,'CLOSE_FAIL reason=evidence_dir_absent path=/home/gatea/wpi_staging_X/evidence/runkit/X-P0');
    '08'=@(1,'CLOSE_FAIL reason=evidence_dir_absent path=/home/gatea/wpi_staging_X/evidence/runkit/X-RO');
    '09'=@(1,''); '10'=@(1,''); '11'=@(3,''); '12'=@(3,'')
}

# Fixture C - the distinct-reason case (subsumes the Claude nit): the RO stage
# RAN and observed deviant state, so the RO close's own failure is downstream of
# a finding already counted and must say so with its own reason token, while the
# P0 branch is untouched and still passes.
$fixtureC = @{
    '01'=@(0,$SETUP); '02'=@(0,''); '03'=@(0,$EXTRACT); '04'=@(0,$P0W); '05'=@(1,$ROWFAIL); '06'=@(0,$TCP);
    '07'=@(0,$CLOSE_OK); '08'=@(1,$CLOSE_FAIL); '09'=@(0,''); '10'=@(0,''); '11'=@(0,''); '12'=@(1,'')
}

# Fixture D - F1 wrong marker family: the P0 close operation returns rc 0 and its
# capture carries only a SETUP marker. A close operation must not accept SETUP
# provenance as evidence that the close script ran.
$fixtureD = @{
    '01'=@(0,$SETUP); '02'=@(0,''); '03'=@(0,$EXTRACT); '04'=@(0,$P0W); '05'=@(0,$ROW); '06'=@(0,$TCP);
    '07'=@(0,'SETUP PASS base=forged'); '08'=@(0,$CLOSE_OK); '09'=@(0,''); '10'=@(0,''); '11'=@(0,''); '12'=@(0,'')
}

Invoke-ProbeFixture 'FIXTURE A - F4 decisive: independent RO close FAIL after unrelated P0 close STOP' $fixtureA
Invoke-ProbeFixture 'FIXTURE B - genuinely unestablished prerequisite stays not-evaluable' $fixtureB
Invoke-ProbeFixture 'FIXTURE C - cleanup after an earlier deviation on its own branch' $fixtureC
Invoke-ProbeFixture 'FIXTURE D - F1 wrong marker family on a close operation' $fixtureD
