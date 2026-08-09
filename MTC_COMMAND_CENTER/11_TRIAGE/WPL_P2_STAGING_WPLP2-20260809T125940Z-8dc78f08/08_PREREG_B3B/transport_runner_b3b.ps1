# WP-L Phase 2 Stage 2B - operator-side transport recorder (PREREGISTERED).
# Default mode is dry run. Execution requires -Execute and the exact token.
# rc: 0 expected results, 1 unexpected op/bind result, 3 could not evaluate.
[CmdletBinding()]
param(
    [switch] $Execute,
    [string] $Confirm = ''
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$UNIT          = 'WPLP2B-20260809T210610Z-834380c5'
$BASE_RUN      = $UNIT
$CONFIRM_TOKEN = $UNIT + '-B3B-EXECUTE'
$PREREG_DIR    = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\08_PREREG_B3B'
$RUNKIT_DIR    = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\07_RUNKIT_B'
$RECORD_ROOT   = 'C:\WPI_ARTIFACTS\WPLP2B_TRANSPORT_' + $UNIT
$PLAN_NAME     = 'TRANSPORT_PLAN_B3B.tsv'
$PLAN_SHA256   = 'a518c2fe3cc15cd4892839dd29caa21c14a358577b4269d1ddf753a6ef9a447b'
$PLAN_HEADER   = "op_id`tkind`trun_when`texpect_rc`tcwd`tstdin_file`tstdin_sha256`targv`tpurpose"
$ARCHIVE_SHA   = '888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b'
$ALLOWED_KINDS = @('ssh_stdin', 'scp_up', 'scp_down', 'local_bind')
$ALLOWED_RUN_WHEN = @('sequence_ok', 'always')
$ALLOWED_PROGRAMS = @('ssh', 'scp')

$script:Log = New-Object System.Collections.ArrayList
$script:RecordReady = $false

function Write-TextFile([string] $Path, [string] $Text) {
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, ($Text + "`n"), $enc)
}

function Emit([string] $Line) {
    [void] $script:Log.Add($Line)
    Write-Host $Line
}

function Flush-Log {
    if ($script:RecordReady -ne $true) { return }
    Write-TextFile (Join-Path $RECORD_ROOT 'TRANSPORT_RECORD.txt') ($script:Log -join "`n")
}

function Stop-Run([string] $Reason) {
    Emit ('TR_STOP reason=' + $Reason)
    try { Flush-Log } catch { Write-Host ('TR_STOP reason=record_write_failed detail=' + $_.Exception.Message) }
    exit 3
}

function Get-Sha256([string] $Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-Sha256OfText([string] $Text) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { $hash = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Text)) }
    finally { $sha.Dispose() }
    $sb = New-Object System.Text.StringBuilder
    foreach ($b in $hash) { [void] $sb.Append($b.ToString('x2')) }
    return $sb.ToString()
}

function Test-Ascii([string] $Text) {
    foreach ($c in $Text.ToCharArray()) { if ([int] $c -gt 127) { return $false } }
    return $true
}

Emit ('TR_HEADER base_run=' + $BASE_RUN)
Emit ('TR_MODE execute=' + $Execute.IsPresent + ' confirm_supplied=' + [string](-not [string]::IsNullOrEmpty($Confirm)))
$here = Split-Path -Parent $PSCommandPath
if ($here -ne $PREREG_DIR) { Stop-Run ('runner_not_in_preregistered_directory here=' + $here + ' expected=' + $PREREG_DIR) }
Emit ('TR_LOCATION dir=' + $here)

$planPath = Join-Path $PREREG_DIR $PLAN_NAME
if (-not (Test-Path -LiteralPath $planPath -PathType Leaf)) { Stop-Run ('plan_missing path=' + $planPath) }
$planSha = Get-Sha256 $planPath
Emit ('TR_PLAN path=' + $planPath + ' sha256=' + $planSha)
if ($planSha -ne $PLAN_SHA256) { Stop-Run ('plan_sha256_mismatch actual=' + $planSha + ' expected=' + $PLAN_SHA256) }

$planLines = @(Get-Content -LiteralPath $planPath -Encoding UTF8)
if ($planLines.Count -lt 2) { Stop-Run 'plan_has_no_rows' }
if ($planLines[0] -ne $PLAN_HEADER) { Stop-Run ('plan_header_differs actual=[' + $planLines[0] + ']') }
$ops = New-Object System.Collections.ArrayList
for ($i = 1; $i -lt $planLines.Count; $i++) {
    $raw = $planLines[$i]
    if ($raw.Trim().Length -eq 0) { continue }
    if (-not (Test-Ascii $raw)) { Stop-Run ('plan_row_non_ascii row=' + ($i + 1)) }
    $f = $raw -split "`t"
    if ($f.Count -ne 9) { Stop-Run ('plan_row_field_count=' + $f.Count + ' row=' + ($i + 1)) }
    $argv = $f[7] -split ' '
    foreach ($a in $argv) { if ($a.Length -eq 0) { Stop-Run ('plan_row_empty_argv_element row=' + ($i + 1)) } }
    $op = @{
        Id = $f[0]; Kind = $f[1]; RunWhen = $f[2]; ExpectRc = [int] $f[3]
        Cwd = $f[4]; StdinRel = $f[5]; StdinSha = $f[6]; Argv = $argv; Purpose = $f[8]
    }
    if ($ALLOWED_KINDS -notcontains $op.Kind) { Stop-Run ('plan_row_bad_kind=' + $op.Kind) }
    if ($ALLOWED_RUN_WHEN -notcontains $op.RunWhen) { Stop-Run ('plan_row_bad_run_when=' + $op.RunWhen) }
    if ($op.Kind -ne 'local_bind' -and $ALLOWED_PROGRAMS -notcontains $op.Argv[0]) {
        Stop-Run ('plan_row_program_not_allowed=' + $op.Argv[0] + ' op=' + $op.Id)
    }
    [void] $ops.Add($op)
}
Emit ('TR_PLAN_ROWS count=' + $ops.Count)

foreach ($op in $ops) {
    if ($op.StdinRel -eq '-') { continue }
    $p = Join-Path $PREREG_DIR $op.StdinRel
    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { Stop-Run ('stdin_file_missing op=' + $op.Id + ' path=' + $p) }
    $s = Get-Sha256 $p
    Emit ('TR_STDIN op=' + $op.Id + ' file=' + $op.StdinRel + ' sha256=' + $s)
    if ($s -ne $op.StdinSha) { Stop-Run ('stdin_sha256_mismatch op=' + $op.Id + ' actual=' + $s + ' expected=' + $op.StdinSha) }
}

$archivePath = Join-Path $RUNKIT_DIR 'runkit_b.tar'
if (-not (Test-Path -LiteralPath $archivePath -PathType Leaf)) { Stop-Run ('pinned_file_missing path=' + $archivePath) }
$archiveSha = Get-Sha256 $archivePath
Emit ('TR_PINNED path=' + $archivePath + ' sha256=' + $archiveSha)
if ($archiveSha -ne $ARCHIVE_SHA) { Stop-Run ('pinned_file_sha256_mismatch path=' + $archivePath + ' actual=' + $archiveSha + ' expected=' + $ARCHIVE_SHA) }

foreach ($prog in $ALLOWED_PROGRAMS) {
    $cmd = Get-Command $prog -ErrorAction SilentlyContinue
    if ($null -eq $cmd) { Stop-Run ('program_not_found name=' + $prog) }
    Emit ('TR_PROGRAM name=' + $prog + ' resolved=' + $cmd.Source)
}
foreach ($op in $ops) {
    Emit ('TR_OP_PLANNED id=' + $op.Id + ' kind=' + $op.Kind + ' run_when=' + $op.RunWhen + ' expect_rc=' + $op.ExpectRc + ' stdin=' + $op.StdinRel)
    Emit ('TR_OP_ARGV id=' + $op.Id + ' argv=[' + ($op.Argv -join '] [') + ']')
}

if (-not $Execute.IsPresent -or $Confirm -ne $CONFIRM_TOKEN) {
    Emit 'TR_DRY_RUN no_process_was_started no_connection_was_opened'
    Emit ('TR_DRY_RUN to execute: -Execute -Confirm ' + $CONFIRM_TOKEN)
    exit 0
}

# Dispatch must replace every placeholder and re-freeze all dependent hashes.
if ($UNIT.Contains('<') -or $UNIT.Contains('>') -or $planLines -match 'PIN-BEFORE-EXECUTE|ALLOCATE-AT-DISPATCH') {
    Stop-Run 'dispatch_placeholders_unresolved; execution_refused_before_record_creation_or_process_start'
}

if (Test-Path -LiteralPath $RECORD_ROOT) { Stop-Run ('record_root_already_exists path=' + $RECORD_ROOT) }
try {
    [void] (New-Item -ItemType Directory -Path $RECORD_ROOT)
    [void] (New-Item -ItemType Directory -Path (Join-Path $RECORD_ROOT 'ops'))
    [void] (New-Item -ItemType Directory -Path (Join-Path $RECORD_ROOT 'evidence'))
} catch { Stop-Run ('record_root_creation_failed detail=' + $_.Exception.Message) }
$script:RecordReady = $true
Emit ('TR_RECORD_ROOT path=' + $RECORD_ROOT)
$opsDir = Join-Path $RECORD_ROOT 'ops'
$sequenceOk = $true
$anyMismatch = $false
$results = New-Object System.Collections.ArrayList

function Invoke-Process($Op, [string] $OutFile, [string] $ErrFile) {
    $exe = $Op.Argv[0]
    $rest = @()
    if ($Op.Argv.Count -gt 1) { $rest = $Op.Argv[1..($Op.Argv.Count - 1)] }
    $sp = @{
        FilePath = $exe; WorkingDirectory = $Op.Cwd
        RedirectStandardOutput = $OutFile; RedirectStandardError = $ErrFile
        NoNewWindow = $true; Wait = $true; PassThru = $true
    }
    if ($rest.Count -gt 0) { $sp['ArgumentList'] = $rest }
    if ($Op.StdinRel -ne '-') { $sp['RedirectStandardInput'] = (Join-Path $PREREG_DIR $Op.StdinRel) }
    $proc = Start-Process @sp
    $proc.WaitForExit()
    return $proc.ExitCode
}

function Read-RemoteDigestSet([string] $CloseOpId) {
    $path = Join-Path $opsDir ($CloseOpId + '.stdout')
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { return $null }
    $set = @{}
    foreach ($line in @(Get-Content -LiteralPath $path -Encoding UTF8)) {
        if (-not $line.StartsWith('CLOSE_DIGEST ')) { continue }
        $body = $line.Substring(13)
        if ($body.Length -lt 67 -or $body.Substring(64, 2) -ne '  ') { return $null }
        $sha = $body.Substring(0, 64); $rel = $body.Substring(66)
        if ($rel.Length -eq 0 -or $set.ContainsKey($rel)) { return $null }
        $set[$rel] = $sha
    }
    return $set
}

function Get-RemoteDigestSetSha([string] $CloseOpId) {
    $path = Join-Path $opsDir ($CloseOpId + '.stdout')
    foreach ($line in @(Get-Content -LiteralPath $path -Encoding UTF8)) {
        if ($line.StartsWith('CLOSE_DIGEST_SET_SHA256 ')) {
            $parts = $line -split ' '; return $parts[$parts.Count - 1]
        }
    }
    return ''
}

function Invoke-LocalBind($Op) {
    $closeOp = $Op.Argv[1]; $fetchOp = $Op.Argv[2]; $relDir = $Op.Argv[3]
    $localDir = Join-Path $RECORD_ROOT $relDir
    Emit ('TR_BIND op=' + $Op.Id + ' close_op=' + $closeOp + ' fetch_op=' + $fetchOp + ' local_dir=' + $localDir)
    $remote = Read-RemoteDigestSet $closeOp
    if ($null -eq $remote -or $remote.Count -eq 0) { Emit ('TR_BIND_STOP op=' + $Op.Id + ' reason=remote_digest_set_unparsable_or_empty'); return 3 }
    if (-not (Test-Path -LiteralPath $localDir -PathType Container)) { Emit ('TR_BIND_STOP op=' + $Op.Id + ' reason=local_dir_absent'); return 3 }
    $local = @{}; $prefix = $localDir
    if (-not $prefix.EndsWith('\')) { $prefix += '\' }
    foreach ($file in @(Get-ChildItem -LiteralPath $localDir -Recurse -File -Force)) {
        if (-not $file.FullName.StartsWith($prefix)) { Emit ('TR_BIND_STOP op=' + $Op.Id + ' reason=local_path_outside_dir'); return 3 }
        $rel = $file.FullName.Substring($prefix.Length).Replace('\', '/')
        $local[$rel] = Get-Sha256 $file.FullName
    }
    Emit ('TR_BIND_COUNTS op=' + $Op.Id + ' remote=' + $remote.Count + ' local=' + $local.Count)
    $ok = $true
    foreach ($rel in $remote.Keys) {
        if (-not $local.ContainsKey($rel)) { Emit ('TR_BIND_DIFF op=' + $Op.Id + ' missing_locally=' + $rel); $ok = $false }
        elseif ($local[$rel] -ne $remote[$rel]) { Emit ('TR_BIND_DIFF op=' + $Op.Id + ' digest_differs=' + $rel); $ok = $false }
    }
    foreach ($rel in $local.Keys) { if (-not $remote.ContainsKey($rel)) { Emit ('TR_BIND_DIFF op=' + $Op.Id + ' missing_remotely=' + $rel); $ok = $false } }
    if (-not $ok) { return 1 }
    $keys = [string[]] @($remote.Keys)
    foreach ($k in $keys) { if (-not (Test-Ascii $k)) { Emit ('TR_BIND_STOP op=' + $Op.Id + ' reason=non_ascii_evidence_name'); return 3 } }
    [Array]::Sort($keys, [System.StringComparer]::Ordinal)
    $sb = New-Object System.Text.StringBuilder
    foreach ($k in $keys) { [void] $sb.Append($remote[$k] + '  ' + $k + "`n") }
    $localSetSha = Get-Sha256OfText $sb.ToString()
    $remoteSetSha = Get-RemoteDigestSetSha $closeOp
    Emit ('TR_BIND_SET op=' + $Op.Id + ' remote_set_sha256=' + $remoteSetSha + ' reconstructed=' + $localSetSha)
    if ($remoteSetSha -ne $localSetSha) { Emit ('TR_BIND_STOP op=' + $Op.Id + ' reason=digest_set_rendering_differs'); return 3 }
    Emit ('TR_BIND_PASS op=' + $Op.Id + ' files=' + $remote.Count)
    return 0
}

foreach ($op in $ops) {
    $outFile = Join-Path $opsDir ($op.Id + '.stdout')
    $errFile = Join-Path $opsDir ($op.Id + '.stderr')
    $argvFile = Join-Path $opsDir ($op.Id + '.argv')
    $rcFile = Join-Path $opsDir ($op.Id + '.rc')
    Write-TextFile $argvFile ($op.Argv -join "`n")
    if ($op.RunWhen -eq 'sequence_ok' -and -not $sequenceOk) {
        Write-TextFile $outFile ''; Write-TextFile $errFile ''; Write-TextFile $rcFile 'skipped'
        Emit ('TR_OP_SKIPPED id=' + $op.Id + ' reason=prior_op_did_not_produce_its_preregistered_rc')
        [void] $results.Add(@{ Id = $op.Id; Rc = 'skipped'; Expect = $op.ExpectRc })
        continue
    }
    Emit ('TR_OP_BEGIN id=' + $op.Id + ' kind=' + $op.Kind + ' cwd=' + $op.Cwd)
    Emit ('TR_OP_SENT_ARGV id=' + $op.Id + ' ' + ($op.Argv -join ' '))
    $rc = 3
    if ($op.Kind -eq 'local_bind') {
        Write-TextFile $outFile ''; Write-TextFile $errFile ''
        try { $rc = Invoke-LocalBind $op } catch { Emit ('TR_OP_EXCEPTION id=' + $op.Id + ' detail=' + $_.Exception.Message); $rc = 3 }
    } elseif (-not (Test-Path -LiteralPath $op.Cwd -PathType Container)) {
        Write-TextFile $outFile ''; Write-TextFile $errFile ''
        Emit ('TR_OP_CWD_ABSENT id=' + $op.Id + ' path=' + $op.Cwd); $rc = 3
    } else {
        try { $rc = Invoke-Process $op $outFile $errFile } catch { Emit ('TR_OP_EXCEPTION id=' + $op.Id + ' detail=' + $_.Exception.Message); $rc = 3 }
    }
    Write-TextFile $rcFile ([string] $rc)
    $outSha = ''; $errSha = ''
    if (Test-Path -LiteralPath $outFile -PathType Leaf) { $outSha = Get-Sha256 $outFile }
    if (Test-Path -LiteralPath $errFile -PathType Leaf) { $errSha = Get-Sha256 $errFile }
    Emit ('TR_OP_END id=' + $op.Id + ' rc=' + $rc + ' expect_rc=' + $op.ExpectRc + ' stdout_sha256=' + $outSha + ' stderr_sha256=' + $errSha)
    [void] $results.Add(@{ Id = $op.Id; Rc = $rc; Expect = $op.ExpectRc })
    if ($rc -ne $op.ExpectRc) {
        $anyMismatch = $true; $sequenceOk = $false
        Emit ('TR_OP_MISMATCH id=' + $op.Id + ' rc=' + $rc + ' expected=' + $op.ExpectRc + ' first_fail_stopping=engaged')
    }
}

$sumLines = New-Object System.Collections.ArrayList
foreach ($f in @(Get-ChildItem -LiteralPath $RECORD_ROOT -Recurse -File -Force)) {
    if ($f.Name -in @('TRANSPORT_SHA256SUMS.txt', 'TRANSPORT_RECORD.txt')) { continue }
    $rel = $f.FullName.Substring($RECORD_ROOT.Length).TrimStart('\').Replace('\', '/')
    [void] $sumLines.Add((Get-Sha256 $f.FullName) + '  ' + $rel)
}
$sorted = [string[]] @($sumLines)
[Array]::Sort($sorted, [System.StringComparer]::Ordinal)
Write-TextFile (Join-Path $RECORD_ROOT 'TRANSPORT_SHA256SUMS.txt') ($sorted -join "`n")
foreach ($r in $results) { Emit ('TR_RESULT id=' + $r.Id + ' rc=' + $r.Rc + ' expect_rc=' + $r.Expect) }
if ($anyMismatch) { Emit ('TR_RUN FAIL base_run=' + $BASE_RUN + ' record=' + $RECORD_ROOT); Flush-Log; exit 1 }
Emit ('TR_RUN PASS base_run=' + $BASE_RUN + ' record=' + $RECORD_ROOT)
Flush-Log
exit 0
