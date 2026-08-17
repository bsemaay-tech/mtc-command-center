# WP-L Phase 2 Stage 2 - operator-side transport recorder (PREREGISTERED).
#
# Implements the accepted RP0 requirement 1.2: "The transport itself is
# evidence. The operator-side transport record MUST capture, from the first byte
# and independently of anything the remote side writes: the exact remote argv
# actually sent, the complete transport stdout, the complete transport stderr,
# and the transport exit status." Every failure BEFORE remote evidence
# allocation succeeds is invisible to a remote-only log, and those are exactly
# the failures that decide whether the run ID is burned.
#
# It executes TRANSPORT_PLAN.tsv and nothing else. It contains no host name, no
# path and no argument of its own: every argv comes from the plan, whose sha256
# is pinned below. Editing the plan therefore invalidates this runner until the
# pin is updated too, which is the intended immutability.
#
# DEFAULT MODE IS DRY RUN. Without BOTH -Execute and the exact -Confirm token
# this script verifies the preregistration and prints the plan. It opens no
# connection, spawns no ssh, and writes nothing outside its own record root.
#
# ASCII-only by construction (no em dash, no typographic quote, no non-ASCII
# byte anywhere), so the file survives any code page the operator console uses.
#
# Exit codes:
#   0  every executed op produced its preregistered rc (or dry run completed)
#   1  an op produced a different rc, or a binding did not hold
#   3  could not evaluate: a preregistration check refused, or a record could
#      not be written. Never re-read as success.
#
# Scope of what this script may do: run the plan's argv, write files under its
# own record root, and hash files. It never edits the repository, never touches
# a service, never reads a credential value, and never issues an HTTP request.

[CmdletBinding()]
param(
    [switch] $Execute,
    [string] $Confirm = ''
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------- pinned facts
$BASE_RUN      = 'WPLP2-20260809T125940Z-8dc78f08'
$CONFIRM_TOKEN = 'WPLP2-20260809T125940Z-8dc78f08-EXECUTE'
$PREREG_DIR    = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\02_PREREG'
$RUNKIT_DIR    = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\01_RUNKIT'
$RECORD_ROOT   = 'C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08'

$PLAN_NAME   = 'TRANSPORT_PLAN.tsv'
$PLAN_SHA256 = '0850f24fb2da47ea406ec328706a4ed2dc6d171af2032ac7cc32f032705a5239'
$PLAN_HEADER = 'op_id	kind	run_when	expect_rc	cwd	stdin_file	stdin_sha256	argv	purpose'

# Artifacts the plan transfers by name rather than on stdin, so their bytes are
# pinned here instead of in the plan's stdin_sha256 column.
$PINNED_FILES = @(
    @{ Path = (Join-Path $RUNKIT_DIR 'runkit.tar');
       Sha  = '618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53' },
    @{ Path = (Join-Path $PREREG_DIR 'R4_5_runner.py');
       Sha  = '8519e2bfc9bf2105bbb8e8c33fa4f271aa8852c7d7b18ad10286e19deddf68d5' }
)

$ALLOWED_KINDS      = @('ssh_stdin', 'scp_up', 'scp_down', 'local_bind')
$ALLOWED_RUN_WHEN   = @('sequence_ok', 'always')
$ALLOWED_PROGRAMS   = @('ssh', 'scp')

# ---------------------------------------------------------------------- output
$script:Log = New-Object System.Collections.ArrayList

function Emit([string] $line) {
    [void] $script:Log.Add($line)
    Write-Host $line
}

function Stop-Run([string] $reason) {
    Emit ("TR_STOP reason=" + $reason)
    Flush-Log
    exit 3
}

function Flush-Log {
    if ($script:RecordReady -ne $true) { return }
    $path = Join-Path $RECORD_ROOT 'TRANSPORT_RECORD.txt'
    try {
        Write-TextFile $path ($script:Log -join "`n")
    } catch {
        Write-Host ("TR_STOP reason=record_write_failed detail=" + $_.Exception.Message)
    }
}

function Write-TextFile([string] $path, [string] $text) {
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($path, ($text + "`n"), $enc)
}

function Get-Sha256([string] $path) {
    $h = Get-FileHash -LiteralPath $path -Algorithm SHA256
    return $h.Hash.ToLowerInvariant()
}

function Get-Sha256OfText([string] $text) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($text)
        $hash = $sha.ComputeHash($bytes)
    } finally {
        $sha.Dispose()
    }
    $sb = New-Object System.Text.StringBuilder
    foreach ($b in $hash) { [void] $sb.Append($b.ToString('x2')) }
    return $sb.ToString()
}

function Test-Ascii([string] $s) {
    foreach ($c in $s.ToCharArray()) {
        if ([int] $c -gt 127) { return $false }
    }
    return $true
}

# ------------------------------------------------------------------- preflight
$script:RecordReady = $false

Emit ("TR_HEADER base_run=" + $BASE_RUN)
Emit ("TR_MODE execute=" + $Execute.IsPresent + " confirm_supplied=" + [string](-not [string]::IsNullOrEmpty($Confirm)))

$here = Split-Path -Parent $PSCommandPath
if ($here -ne $PREREG_DIR) {
    Stop-Run ("runner_not_in_preregistered_directory here=" + $here + " expected=" + $PREREG_DIR)
}
Emit ("TR_LOCATION dir=" + $here)

$planPath = Join-Path $PREREG_DIR $PLAN_NAME
if (-not (Test-Path -LiteralPath $planPath -PathType Leaf)) {
    Stop-Run ("plan_missing path=" + $planPath)
}
$planSha = Get-Sha256 $planPath
Emit ("TR_PLAN path=" + $planPath + " sha256=" + $planSha)
if ($planSha -ne $PLAN_SHA256) {
    Stop-Run ("plan_sha256_mismatch actual=" + $planSha + " expected=" + $PLAN_SHA256)
}

$planLines = @(Get-Content -LiteralPath $planPath -Encoding UTF8)
if ($planLines.Count -lt 2) { Stop-Run 'plan_has_no_rows' }
if ($planLines[0] -ne $PLAN_HEADER) { Stop-Run ("plan_header_differs actual=[" + $planLines[0] + "]") }

$ops = New-Object System.Collections.ArrayList
for ($i = 1; $i -lt $planLines.Count; $i++) {
    $raw = $planLines[$i]
    if ($raw.Trim().Length -eq 0) { continue }
    $f = $raw -split "`t"
    if ($f.Count -ne 9) { Stop-Run ("plan_row_field_count=" + $f.Count + " row=" + ($i + 1)) }
    $argv = $f[7] -split ' '
    foreach ($a in $argv) {
        if ($a.Length -eq 0) { Stop-Run ("plan_row_empty_argv_element row=" + ($i + 1)) }
    }
    $op = @{
        Id       = $f[0]
        Kind     = $f[1]
        RunWhen  = $f[2]
        ExpectRc = [int] $f[3]
        Cwd      = $f[4]
        StdinRel = $f[5]
        StdinSha = $f[6]
        Argv     = $argv
        Purpose  = $f[8]
    }
    if ($ALLOWED_KINDS -notcontains $op.Kind) { Stop-Run ("plan_row_bad_kind=" + $op.Kind) }
    if ($ALLOWED_RUN_WHEN -notcontains $op.RunWhen) { Stop-Run ("plan_row_bad_run_when=" + $op.RunWhen) }
    if ($op.Kind -ne 'local_bind') {
        if ($ALLOWED_PROGRAMS -notcontains $op.Argv[0]) {
            Stop-Run ("plan_row_program_not_allowed=" + $op.Argv[0] + " op=" + $op.Id)
        }
    }
    [void] $ops.Add($op)
}
Emit ("TR_PLAN_ROWS count=" + $ops.Count)

# Every stdin payload is hashed here, before anything is sent, and the file that
# is opened for the send is the same path that was hashed.
foreach ($op in $ops) {
    if ($op.StdinRel -eq '-') { continue }
    $p = Join-Path $PREREG_DIR $op.StdinRel
    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) {
        Stop-Run ("stdin_file_missing op=" + $op.Id + " path=" + $p)
    }
    $s = Get-Sha256 $p
    Emit ("TR_STDIN op=" + $op.Id + " file=" + $op.StdinRel + " sha256=" + $s)
    if ($s -ne $op.StdinSha) {
        Stop-Run ("stdin_sha256_mismatch op=" + $op.Id + " actual=" + $s + " expected=" + $op.StdinSha)
    }
}

foreach ($pin in $PINNED_FILES) {
    if (-not (Test-Path -LiteralPath $pin.Path -PathType Leaf)) {
        Stop-Run ("pinned_file_missing path=" + $pin.Path)
    }
    $s = Get-Sha256 $pin.Path
    Emit ("TR_PINNED path=" + $pin.Path + " sha256=" + $s)
    if ($s -ne $pin.Sha) {
        Stop-Run ("pinned_file_sha256_mismatch path=" + $pin.Path + " actual=" + $s + " expected=" + $pin.Sha)
    }
}

foreach ($prog in $ALLOWED_PROGRAMS) {
    $cmd = Get-Command $prog -ErrorAction SilentlyContinue
    if ($null -eq $cmd) { Stop-Run ("program_not_found name=" + $prog) }
    Emit ("TR_PROGRAM name=" + $prog + " resolved=" + $cmd.Source)
}

foreach ($op in $ops) {
    Emit ("TR_OP_PLANNED id=" + $op.Id + " kind=" + $op.Kind + " run_when=" + $op.RunWhen +
          " expect_rc=" + $op.ExpectRc + " stdin=" + $op.StdinRel)
    Emit ("TR_OP_ARGV id=" + $op.Id + " argv=[" + ($op.Argv -join '] [') + "]")
}

if (-not $Execute.IsPresent -or $Confirm -ne $CONFIRM_TOKEN) {
    Emit 'TR_DRY_RUN no_process_was_started no_connection_was_opened'
    Emit ("TR_DRY_RUN to execute: -Execute -Confirm " + $CONFIRM_TOKEN)
    exit 0
}

# ------------------------------------------------------------------- execution
if (Test-Path -LiteralPath $RECORD_ROOT) {
    Stop-Run ("record_root_already_exists path=" + $RECORD_ROOT +
              " (the record root is create-once; a rerun needs a new preregistration)")
}
try {
    [void] (New-Item -ItemType Directory -Path $RECORD_ROOT)
    [void] (New-Item -ItemType Directory -Path (Join-Path $RECORD_ROOT 'ops'))
    [void] (New-Item -ItemType Directory -Path (Join-Path $RECORD_ROOT 'evidence'))
} catch {
    Stop-Run ("record_root_creation_failed detail=" + $_.Exception.Message)
}
$script:RecordReady = $true
Emit ("TR_RECORD_ROOT path=" + $RECORD_ROOT)

$opsDir = Join-Path $RECORD_ROOT 'ops'
$sequenceOk = $true
$anyMismatch = $false
$results = New-Object System.Collections.ArrayList

function Invoke-Process($op, [string] $outFile, [string] $errFile) {
    $exe = $op.Argv[0]
    $rest = @()
    if ($op.Argv.Count -gt 1) { $rest = $op.Argv[1..($op.Argv.Count - 1)] }
    $sp = @{
        FilePath               = $exe
        WorkingDirectory       = $op.Cwd
        RedirectStandardOutput = $outFile
        RedirectStandardError  = $errFile
        NoNewWindow            = $true
        Wait                   = $true
        PassThru               = $true
    }
    if ($rest.Count -gt 0) { $sp['ArgumentList'] = $rest }
    if ($op.StdinRel -ne '-') {
        $sp['RedirectStandardInput'] = (Join-Path $PREREG_DIR $op.StdinRel)
    }
    $proc = Start-Process @sp
    $proc.WaitForExit()
    return $proc.ExitCode
}

function Read-RemoteDigestSet([string] $closeOpId) {
    # Parse the CLOSE_DIGEST lines the remote close-tree op printed. Anything
    # unparsable is an evaluation failure, never an empty set.
    $path = Join-Path $opsDir ($closeOpId + '.stdout')
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { return $null }
    $set = @{}
    foreach ($line in @(Get-Content -LiteralPath $path -Encoding UTF8)) {
        if (-not $line.StartsWith('CLOSE_DIGEST ')) { continue }
        $body = $line.Substring(13)
        if ($body.Length -lt 67) { return $null }
        $sha = $body.Substring(0, 64)
        if ($body.Substring(64, 2) -ne '  ') { return $null }
        $rel = $body.Substring(66)
        if ($rel.Length -eq 0) { return $null }
        if ($set.ContainsKey($rel)) { return $null }
        $set[$rel] = $sha
    }
    return $set
}

function Get-RemoteDigestSetSha([string] $closeOpId) {
    $path = Join-Path $opsDir ($closeOpId + '.stdout')
    foreach ($line in @(Get-Content -LiteralPath $path -Encoding UTF8)) {
        if ($line.StartsWith('CLOSE_DIGEST_SET_SHA256 ')) {
            $parts = $line -split ' '
            return $parts[$parts.Count - 1]
        }
    }
    return ''
}

function Invoke-LocalBind($op) {
    $closeOp = $op.Argv[1]
    $fetchOp = $op.Argv[2]
    $relDir  = $op.Argv[3]
    $localDir = Join-Path $RECORD_ROOT $relDir
    Emit ("TR_BIND op=" + $op.Id + " close_op=" + $closeOp + " fetch_op=" + $fetchOp + " local_dir=" + $localDir)

    $remote = Read-RemoteDigestSet $closeOp
    if ($null -eq $remote) {
        Emit ("TR_BIND_STOP op=" + $op.Id + " reason=remote_digest_set_unparsable")
        return 3
    }
    if ($remote.Count -eq 0) {
        Emit ("TR_BIND_STOP op=" + $op.Id + " reason=remote_digest_set_empty")
        return 3
    }
    if (-not (Test-Path -LiteralPath $localDir -PathType Container)) {
        Emit ("TR_BIND_STOP op=" + $op.Id + " reason=local_dir_absent path=" + $localDir)
        return 3
    }

    $local = @{}
    $prefix = $localDir
    if (-not $prefix.EndsWith('\')) { $prefix = $prefix + '\' }
    foreach ($file in @(Get-ChildItem -LiteralPath $localDir -Recurse -File -Force)) {
        $full = $file.FullName
        if (-not $full.StartsWith($prefix)) {
            Emit ("TR_BIND_STOP op=" + $op.Id + " reason=local_path_outside_dir path=" + $full)
            return 3
        }
        $rel = $full.Substring($prefix.Length).Replace('\', '/')
        $local[$rel] = (Get-Sha256 $full)
    }
    Emit ("TR_BIND_COUNTS op=" + $op.Id + " remote=" + $remote.Count + " local=" + $local.Count)

    $ok = $true
    foreach ($rel in $remote.Keys) {
        if (-not $local.ContainsKey($rel)) {
            Emit ("TR_BIND_DIFF op=" + $op.Id + " missing_locally=" + $rel)
            $ok = $false
            continue
        }
        if ($local[$rel] -ne $remote[$rel]) {
            Emit ("TR_BIND_DIFF op=" + $op.Id + " digest_differs=" + $rel +
                  " remote=" + $remote[$rel] + " local=" + $local[$rel])
            $ok = $false
        }
    }
    foreach ($rel in $local.Keys) {
        if (-not $remote.ContainsKey($rel)) {
            Emit ("TR_BIND_DIFF op=" + $op.Id + " missing_remotely=" + $rel)
            $ok = $false
        }
    }
    if (-not $ok) { return 1 }

    # Reconstruct the remote digest FILE byte for byte and compare its sha256 to
    # the value the remote side printed. Equal names and digests already bind the
    # sets; this additionally binds the exact rendering.
    $keys = [string[]] @($remote.Keys)
    $allAscii = $true
    foreach ($k in $keys) { if (-not (Test-Ascii $k)) { $allAscii = $false } }
    if (-not $allAscii) {
        Emit ("TR_BIND_STOP op=" + $op.Id + " reason=non_ascii_evidence_name_ordering_not_reproducible")
        return 3
    }
    # The remote digest file is one `<sha256><2 spaces><relpath>` line per file,
    # each terminated by LF including the last. Reproduce it exactly: a trimmed
    # final newline would make this comparison disagree on every honest run.
    [Array]::Sort($keys, [System.StringComparer]::Ordinal)
    $sb = New-Object System.Text.StringBuilder
    foreach ($k in $keys) { [void] $sb.Append($remote[$k] + '  ' + $k + "`n") }
    $localSetSha = Get-Sha256OfText $sb.ToString()
    $remoteSetSha = Get-RemoteDigestSetSha $closeOp
    Emit ("TR_BIND_SET op=" + $op.Id + " remote_set_sha256=" + $remoteSetSha + " reconstructed=" + $localSetSha)
    if ($remoteSetSha -ne $localSetSha) {
        Emit ("TR_BIND_STOP op=" + $op.Id + " reason=digest_set_rendering_differs")
        return 3
    }
    Emit ("TR_BIND_PASS op=" + $op.Id + " files=" + $remote.Count)
    return 0
}

foreach ($op in $ops) {
    if ($op.RunWhen -eq 'sequence_ok' -and -not $sequenceOk) {
        Emit ("TR_OP_SKIPPED id=" + $op.Id + " reason=prior_op_did_not_produce_its_preregistered_rc")
        [void] $results.Add(@{ Id = $op.Id; Rc = 'skipped'; Expect = $op.ExpectRc })
        continue
    }

    $outFile = Join-Path $opsDir ($op.Id + '.stdout')
    $errFile = Join-Path $opsDir ($op.Id + '.stderr')
    $argvFile = Join-Path $opsDir ($op.Id + '.argv')
    Write-TextFile $argvFile (($op.Argv -join "`n"))

    Emit ("TR_OP_BEGIN id=" + $op.Id + " kind=" + $op.Kind + " cwd=" + $op.Cwd)
    Emit ("TR_OP_SENT_ARGV id=" + $op.Id + " " + ($op.Argv -join ' '))

    $rc = 3
    if ($op.Kind -eq 'local_bind') {
        Write-TextFile $outFile ''
        Write-TextFile $errFile ''
        try {
            $rc = Invoke-LocalBind $op
        } catch {
            Emit ("TR_OP_EXCEPTION id=" + $op.Id + " detail=" + $_.Exception.Message)
            $rc = 3
        }
    } else {
        if (-not (Test-Path -LiteralPath $op.Cwd -PathType Container)) {
            Emit ("TR_OP_CWD_ABSENT id=" + $op.Id + " path=" + $op.Cwd)
            $rc = 3
        } else {
            try {
                $rc = Invoke-Process $op $outFile $errFile
            } catch {
                Emit ("TR_OP_EXCEPTION id=" + $op.Id + " detail=" + $_.Exception.Message)
                $rc = 3
            }
        }
    }

    $outSha = ''
    $errSha = ''
    if (Test-Path -LiteralPath $outFile -PathType Leaf) { $outSha = Get-Sha256 $outFile }
    if (Test-Path -LiteralPath $errFile -PathType Leaf) { $errSha = Get-Sha256 $errFile }
    Emit ("TR_OP_END id=" + $op.Id + " rc=" + $rc + " expect_rc=" + $op.ExpectRc +
          " stdout_sha256=" + $outSha + " stderr_sha256=" + $errSha)
    [void] $results.Add(@{ Id = $op.Id; Rc = $rc; Expect = $op.ExpectRc })

    if ($rc -ne $op.ExpectRc) {
        $anyMismatch = $true
        $sequenceOk = $false
        Emit ("TR_OP_MISMATCH id=" + $op.Id + " rc=" + $rc + " expected=" + $op.ExpectRc +
              " first_fail_stopping=engaged")
    }
}

# ------------------------------------------------------------------ record set
$sumLines = New-Object System.Collections.ArrayList
foreach ($f in @(Get-ChildItem -LiteralPath $RECORD_ROOT -Recurse -File -Force)) {
    if ($f.Name -eq 'TRANSPORT_SHA256SUMS.txt') { continue }
    if ($f.Name -eq 'TRANSPORT_RECORD.txt') { continue }
    $rel = $f.FullName.Substring($RECORD_ROOT.Length).TrimStart('\').Replace('\', '/')
    [void] $sumLines.Add((Get-Sha256 $f.FullName) + '  ' + $rel)
}
$sorted = [string[]] @($sumLines)
[Array]::Sort($sorted, [System.StringComparer]::Ordinal)
Write-TextFile (Join-Path $RECORD_ROOT 'TRANSPORT_SHA256SUMS.txt') ($sorted -join "`n")

foreach ($r in $results) {
    Emit ("TR_RESULT id=" + $r.Id + " rc=" + $r.Rc + " expect_rc=" + $r.Expect)
}

if ($anyMismatch) {
    Emit ("TR_RUN FAIL base_run=" + $BASE_RUN + " record=" + $RECORD_ROOT)
    Flush-Log
    exit 1
}
Emit ("TR_RUN PASS base_run=" + $BASE_RUN + " record=" + $RECORD_ROOT)
Flush-Log
exit 0
