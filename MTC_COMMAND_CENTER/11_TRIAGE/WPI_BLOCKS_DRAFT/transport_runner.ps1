# WP-I operator-side transport recorder (DRAFT - authoring only).
#
# Executes only the internally pinned TRANSPORT_PLAN.tsv. Default mode is a
# read-only dry run. Actual execution requires both -Execute and the exact
# allocation-time confirmation token; those switches are technical interlocks,
# not host-contact authority.
#
# Exit codes: 0 = every executed operation matched its preregistered rc;
#             1 = at least one operation did not match;
#             3 = could not evaluate the plan, operation, or evidence binding.
# ASCII-only and Windows PowerShell 5.1-compatible by construction.

[CmdletBinding()]
param(
    [switch] $Execute,
    [string] $Confirm = ''
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

# --------------------------------------------------------------- frozen facts
$BASE_RUN      = '<ALLOCATE-AT-DISPATCH>'
$CONFIRM_TOKEN = '<ALLOCATE-AT-DISPATCH>-EXECUTE'
$PREREG_DIR    = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT'
$RUNKIT_DIR    = $PREREG_DIR
$RECORD_ROOT   = 'C:\WPI_ARTIFACTS\WPI_TRANSPORT_<ALLOCATE-AT-DISPATCH>'

$PLAN_NAME   = 'TRANSPORT_PLAN.tsv'
$PLAN_SHA256 = '<PIN-AT-FREEZE>'
$PLAN_HEADER = 'op_id	kind	run_when	expect_rc	cwd	stdin_file	stdin_sha256	argv	purpose'

$PINNED_FILES = @(
    @{ Path = (Join-Path $RUNKIT_DIR 'runkit.tar'); Sha = '<PIN-AT-FREEZE>' }
)

$ALLOWED_KINDS    = @('ssh_stdin', 'scp_up', 'scp_down', 'tcp_probe', 'local_bind')
$ALLOWED_RUN_WHEN = @('sequence_ok', 'always')
$ALLOWED_PROGRAMS = @('ssh', 'scp')

# --------------------------------------------------------------------- output
$script:Log = New-Object System.Collections.ArrayList
$script:RecordReady = $false
$script:LastElapsedMs = 0

function Write-TextFile([string] $path, [string] $text) {
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($path, ($text + "`n"), $enc)
}

function Emit([string] $line) {
    [void] $script:Log.Add($line)
    Write-Host $line
}

function Flush-Log {
    if ($script:RecordReady -ne $true) { return }
    Write-TextFile (Join-Path $RECORD_ROOT 'TRANSPORT_RECORD.txt') ($script:Log -join "`n")
}

function Stop-Run([string] $reason) {
    Emit ('TR_STOP reason=' + $reason)
    try { Flush-Log } catch { Write-Host ('TR_STOP reason=record_write_failed detail=' + $_.Exception.Message) }
    exit 3
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

function Test-Ascii([string] $value) {
    foreach ($c in $value.ToCharArray()) {
        if ([int] $c -gt 127) { return $false }
    }
    return $true
}

function Test-HexSha256([string] $value) {
    return $value -match '^[0-9a-f]{64}$'
}

function Test-ReparsePoint([string] $path) {
    $item = Get-Item -LiteralPath $path -Force
    return (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
}

# Pattern 7 reader. It distinguishes: clean LF-terminated EOF, an unterminated
# populated final record, and any open/read failure. It also refuses CR, NUL,
# non-ASCII, and other control bytes before a consumer sees partial content.
function Read-StrictAsciiLines([string] $path) {
    try {
        $bytes = [System.IO.File]::ReadAllBytes($path)
    } catch {
        return [pscustomobject]@{ Ok = $false; Reason = ('read_error detail=' + $_.Exception.GetType().FullName); Lines = @() }
    }
    if ($bytes.Length -eq 0) {
        return [pscustomobject]@{ Ok = $false; Reason = 'empty_input'; Lines = @() }
    }
    foreach ($b in $bytes) {
        if ($b -gt 127) { return [pscustomobject]@{ Ok = $false; Reason = 'non_ascii_byte'; Lines = @() } }
        if ($b -eq 13) { return [pscustomobject]@{ Ok = $false; Reason = 'carriage_return_not_allowed'; Lines = @() } }
        if ($b -lt 32 -and $b -ne 9 -and $b -ne 10) {
            return [pscustomobject]@{ Ok = $false; Reason = ('control_byte_' + $b); Lines = @() }
        }
    }
    if ($bytes[$bytes.Length - 1] -ne 10) {
        return [pscustomobject]@{ Ok = $false; Reason = 'unterminated_final_record'; Lines = @() }
    }
    $text = [System.Text.Encoding]::ASCII.GetString($bytes)
    $parts = $text.Split([char]10)
    $lines = New-Object System.Collections.ArrayList
    for ($i = 0; $i -lt ($parts.Length - 1); $i++) { [void] $lines.Add($parts[$i]) }
    return [pscustomobject]@{ Ok = $true; Reason = 'clean_eof'; Lines = @($lines) }
}

function Test-SafeArg([string] $arg) {
    if ([string]::IsNullOrEmpty($arg)) { return $false }
    return ($arg -match '^[A-Za-z0-9._@:/\\=-]+$')
}

# ------------------------------------------------------------------ preflight
Emit ('TR_HEADER base_run=' + $BASE_RUN)
Emit ('TR_MODE execute=' + $Execute.IsPresent + ' confirm_supplied=' + [string](-not [string]::IsNullOrEmpty($Confirm)))

$here = Split-Path -Parent $PSCommandPath
if ($here -ne $PREREG_DIR) { Stop-Run ('runner_not_in_preregistered_directory here=' + $here + ' expected=' + $PREREG_DIR) }
Emit ('TR_LOCATION dir=' + $here)

$planPath = Join-Path $PREREG_DIR $PLAN_NAME
if (-not (Test-Path -LiteralPath $planPath)) { Stop-Run ('plan_missing path=' + $planPath) }
try {
    if (Test-ReparsePoint $planPath) { Stop-Run ('plan_is_reparse_point path=' + $planPath) }
} catch { Stop-Run ('plan_metadata_unreadable path=' + $planPath + ' detail=' + $_.Exception.GetType().FullName) }

$planRead = Read-StrictAsciiLines $planPath
if (-not $planRead.Ok) { Stop-Run ('plan_' + $planRead.Reason + ' path=' + $planPath) }
$planLines = @($planRead.Lines)
Emit ('TR_PLAN_READ completion=' + $planRead.Reason + ' records=' + $planLines.Count)

try { $planSha = Get-Sha256 $planPath } catch { Stop-Run ('plan_hash_failed detail=' + $_.Exception.GetType().FullName) }
Emit ('TR_PLAN path=' + $planPath + ' sha256=' + $planSha)
if (-not (Test-HexSha256 $PLAN_SHA256)) { Stop-Run 'plan_pin_unfilled expected=64_lower_hex' }
if ($planSha -ne $PLAN_SHA256) { Stop-Run ('plan_sha256_mismatch actual=' + $planSha + ' expected=' + $PLAN_SHA256) }

if ($planLines.Count -lt 2) { Stop-Run 'plan_has_no_rows' }
if ($planLines[0] -ne $PLAN_HEADER) { Stop-Run ('plan_header_differs actual=[' + $planLines[0] + ']') }

$ops = New-Object System.Collections.ArrayList
$seenIds = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
$previousId = -1
for ($i = 1; $i -lt $planLines.Count; $i++) {
    $raw = $planLines[$i]
    if ($raw.Length -eq 0) { Stop-Run ('plan_blank_record row=' + ($i + 1)) }
    $f = $raw.Split([char]9)
    if ($f.Count -ne 9) { Stop-Run ('plan_row_field_count=' + $f.Count + ' row=' + ($i + 1)) }
    if ($f[0] -notmatch '^[0-9]{2}$') { Stop-Run ('plan_row_bad_op_id row=' + ($i + 1) + ' value=' + $f[0]) }
    if (-not $seenIds.Add($f[0])) { Stop-Run ('plan_row_duplicate_op_id=' + $f[0]) }
    $idNumber = [int]$f[0]
    if ($idNumber -le $previousId) { Stop-Run ('plan_row_op_order id=' + $f[0]) }
    $previousId = $idNumber

    $expectRc = 0
    if (-not [int]::TryParse($f[3], [ref]$expectRc)) { Stop-Run ('plan_row_bad_expect_rc op=' + $f[0]) }
    if (@(0, 1, 3) -notcontains $expectRc) { Stop-Run ('plan_row_bad_expect_rc op=' + $f[0] + ' value=' + $expectRc) }
    if ([string]::IsNullOrEmpty($f[4])) { Stop-Run ('plan_row_empty_cwd op=' + $f[0]) }
    if ([string]::IsNullOrEmpty($f[8])) { Stop-Run ('plan_row_empty_purpose op=' + $f[0]) }

    $argv = @($f[7].Split([char]32))
    foreach ($a in $argv) {
        if (-not (Test-SafeArg $a)) { Stop-Run ('plan_row_unsafe_argv op=' + $f[0] + ' arg=[' + $a + ']') }
    }
    $op = @{
        Id = $f[0]; Kind = $f[1]; RunWhen = $f[2]; ExpectRc = $expectRc;
        Cwd = $f[4]; StdinRel = $f[5]; StdinSha = $f[6]; Argv = $argv; Purpose = $f[8]
    }
    if ($ALLOWED_KINDS -notcontains $op.Kind) { Stop-Run ('plan_row_bad_kind=' + $op.Kind + ' op=' + $op.Id) }
    if ($ALLOWED_RUN_WHEN -notcontains $op.RunWhen) { Stop-Run ('plan_row_bad_run_when=' + $op.RunWhen + ' op=' + $op.Id) }
    if ($op.Kind -eq 'local_bind' -and $op.Argv[0] -ne 'local_bind') { Stop-Run ('plan_row_local_bind_argv op=' + $op.Id) }
    if ($op.Kind -eq 'tcp_probe' -and $op.Argv[0] -ne 'tcp_probe') { Stop-Run ('plan_row_tcp_probe_argv op=' + $op.Id) }
    if (@('ssh_stdin', 'scp_up', 'scp_down') -contains $op.Kind) {
        if ($ALLOWED_PROGRAMS -notcontains $op.Argv[0]) { Stop-Run ('plan_row_program_not_allowed=' + $op.Argv[0] + ' op=' + $op.Id) }
    }
    [void] $ops.Add($op)
}
Emit ('TR_PLAN_ROWS count=' + $ops.Count)

foreach ($op in $ops) {
    if ($op.StdinRel -eq '-') {
        if ($op.StdinSha -ne '-') { Stop-Run ('stdin_sha_without_file op=' + $op.Id) }
        continue
    }
    if (-not (Test-SafeArg $op.StdinRel)) { Stop-Run ('stdin_file_name_unsafe op=' + $op.Id) }
    if (-not (Test-HexSha256 $op.StdinSha)) { Stop-Run ('stdin_pin_unfilled_or_malformed op=' + $op.Id) }
    $stdinPath = Join-Path $PREREG_DIR $op.StdinRel
    if (-not (Test-Path -LiteralPath $stdinPath -PathType Leaf)) { Stop-Run ('stdin_file_missing op=' + $op.Id + ' path=' + $stdinPath) }
    try {
        if (Test-ReparsePoint $stdinPath) { Stop-Run ('stdin_file_is_reparse_point op=' + $op.Id + ' path=' + $stdinPath) }
        $stdinSha = Get-Sha256 $stdinPath
    } catch { Stop-Run ('stdin_file_not_evaluable op=' + $op.Id + ' detail=' + $_.Exception.GetType().FullName) }
    Emit ('TR_STDIN op=' + $op.Id + ' file=' + $op.StdinRel + ' sha256=' + $stdinSha)
    if ($stdinSha -ne $op.StdinSha) { Stop-Run ('stdin_sha256_mismatch op=' + $op.Id + ' actual=' + $stdinSha + ' expected=' + $op.StdinSha) }
}

foreach ($pin in $PINNED_FILES) {
    if (-not (Test-HexSha256 $pin.Sha)) { Stop-Run ('pinned_file_pin_unfilled path=' + $pin.Path) }
    if (-not (Test-Path -LiteralPath $pin.Path -PathType Leaf)) { Stop-Run ('pinned_file_missing path=' + $pin.Path) }
    try {
        if (Test-ReparsePoint $pin.Path) { Stop-Run ('pinned_file_is_reparse_point path=' + $pin.Path) }
        $pinSha = Get-Sha256 $pin.Path
    } catch { Stop-Run ('pinned_file_not_evaluable path=' + $pin.Path + ' detail=' + $_.Exception.GetType().FullName) }
    Emit ('TR_PINNED path=' + $pin.Path + ' sha256=' + $pinSha)
    if ($pinSha -ne $pin.Sha) { Stop-Run ('pinned_file_sha256_mismatch path=' + $pin.Path + ' actual=' + $pinSha + ' expected=' + $pin.Sha) }
}

$requiredPrograms = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
foreach ($op in $ops) {
    if (@('ssh_stdin', 'scp_up', 'scp_down') -contains $op.Kind) { [void]$requiredPrograms.Add($op.Argv[0]) }
}
foreach ($prog in $requiredPrograms) {
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
    Emit ('TR_DRY_RUN to_execute=-Execute_-Confirm_' + $CONFIRM_TOKEN)
    exit 0
}

# ------------------------------------------------------------------ execution
if (Test-Path -LiteralPath $RECORD_ROOT) { Stop-Run ('record_root_already_exists path=' + $RECORD_ROOT) }
try {
    [void](New-Item -ItemType Directory -Path $RECORD_ROOT)
    [void](New-Item -ItemType Directory -Path (Join-Path $RECORD_ROOT 'ops'))
    [void](New-Item -ItemType Directory -Path (Join-Path $RECORD_ROOT 'evidence'))
} catch { Stop-Run ('record_root_creation_failed detail=' + $_.Exception.GetType().FullName) }
$script:RecordReady = $true
Emit ('TR_RECORD_ROOT path=' + $RECORD_ROOT)

$opsDir = Join-Path $RECORD_ROOT 'ops'
$sequenceOk = $true
$anyMismatch = $false
$firstMismatch = ''
$results = New-Object System.Collections.ArrayList

function Invoke-ExternalProcess($op, [string] $outFile, [string] $errFile) {
    $exe = $op.Argv[0]
    $rest = @()
    if ($op.Argv.Count -gt 1) { $rest = $op.Argv[1..($op.Argv.Count - 1)] }
    $sp = @{
        FilePath = $exe; WorkingDirectory = $op.Cwd;
        RedirectStandardOutput = $outFile; RedirectStandardError = $errFile;
        NoNewWindow = $true; Wait = $true; PassThru = $true
    }
    if ($rest.Count -gt 0) { $sp['ArgumentList'] = $rest }
    if ($op.StdinRel -ne '-') { $sp['RedirectStandardInput'] = (Join-Path $PREREG_DIR $op.StdinRel) }
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        $proc = Start-Process @sp
        $proc.WaitForExit()
        return $proc.ExitCode
    } finally {
        $sw.Stop(); $script:LastElapsedMs = $sw.ElapsedMilliseconds
    }
}

function Invoke-TcpProbe($op, [string] $outFile, [string] $errFile) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $client = $null
    $waitHandle = $null
    try {
        if ($op.Argv.Count -ne 4) {
            Write-TextFile $outFile 'B6_STOP reason=external_probe_not_evaluable outcome=argv_malformed rc=3 detail=expected_host_port_timeout'
            Write-TextFile $errFile ''
            return 3
        }
        $hostName = $op.Argv[1]
        $port = 0; $timeoutMs = 0
        if (-not [int]::TryParse($op.Argv[2], [ref]$port) -or $port -lt 1 -or $port -gt 65535) {
            Write-TextFile $outFile 'B6_STOP reason=external_probe_not_evaluable outcome=port_invalid rc=3 detail=port_range'
            Write-TextFile $errFile ''
            return 3
        }
        if (-not [int]::TryParse($op.Argv[3], [ref]$timeoutMs) -or $timeoutMs -lt 1 -or $timeoutMs -gt 60000) {
            Write-TextFile $outFile 'B6_STOP reason=external_probe_not_evaluable outcome=timeout_invalid rc=3 detail=timeout_range'
            Write-TextFile $errFile ''
            return 3
        }
        $client = New-Object System.Net.Sockets.TcpClient
        $async = $client.BeginConnect($hostName, $port, $null, $null)
        $waitHandle = $async.AsyncWaitHandle
        if (-not $waitHandle.WaitOne($timeoutMs, $false)) {
            Write-TextFile $outFile ('B6_external row=24 outcome=timeout host=' + $hostName + ' port=' + $port + ' payload_bytes=0')
            Write-TextFile $errFile ''
            return 0
        }
        try {
            $client.EndConnect($async)
        } catch {
            # Windows PowerShell 5.1 wraps EndConnect's SocketException in a
            # MethodInvocationException. Unwrap without matching localized text.
            $socketError = $_.Exception
            while ($null -ne $socketError.InnerException -and
                   -not ($socketError -is [System.Net.Sockets.SocketException])) {
                $socketError = $socketError.InnerException
            }
            if (($socketError -is [System.Net.Sockets.SocketException]) -and
                $socketError.SocketErrorCode -eq [System.Net.Sockets.SocketError]::ConnectionRefused) {
                Write-TextFile $outFile ('B6_external row=24 outcome=connection_refused host=' + $hostName + ' port=' + $port + ' payload_bytes=0')
                Write-TextFile $errFile ''
                return 0
            }
            $detail = $socketError.GetType().FullName
            if ($socketError -is [System.Net.Sockets.SocketException]) { $detail = [string]$socketError.SocketErrorCode }
            Write-TextFile $outFile ('B6_STOP reason=external_probe_not_evaluable outcome=socket_error rc=3 detail=' + $detail)
            Write-TextFile $errFile ''
            return 3
        }
        if ($client.Connected) {
            Write-TextFile $outFile ('B6_FAIL reason=host_reachable_8790 outcome=connected host=' + $hostName + ' port=' + $port + ' payload_bytes=0')
            Write-TextFile $errFile ''
            return 1
        }
        Write-TextFile $outFile 'B6_STOP reason=external_probe_not_evaluable outcome=connect_incomplete rc=3 detail=no_terminal_socket_state'
        Write-TextFile $errFile ''
        return 3
    } catch {
        Write-TextFile $outFile ('B6_STOP reason=external_probe_not_evaluable outcome=local_exception rc=3 detail=' + $_.Exception.GetType().FullName)
        Write-TextFile $errFile ''
        return 3
    } finally {
        if ($null -ne $waitHandle) { $waitHandle.Close() }
        if ($null -ne $client) { $client.Close() }
        $sw.Stop(); $script:LastElapsedMs = $sw.ElapsedMilliseconds
    }
}

function Read-RemoteCloseRecord([string] $closeOpId, [string] $expectedRunId) {
    $path = Join-Path $opsDir ($closeOpId + '.stdout')
    $read = Read-StrictAsciiLines $path
    if (-not $read.Ok) { return [pscustomobject]@{ Ok=$false; Reason=('remote_close_' + $read.Reason) } }
    $digests = New-Object 'System.Collections.Generic.Dictionary[string,string]' ([System.StringComparer]::Ordinal)
    $sizes = New-Object 'System.Collections.Generic.Dictionary[string,long]' ([System.StringComparer]::Ordinal)
    $state = 'before'; $setSha = ''; $setCount = 0; $passCount = 0
    $declaredCount = -1; $passDeclaredCount = -1
    foreach ($line in @($read.Lines)) {
        if ($line -match '^CLOSE_NOTE ') { if ($state -ne 'before') { return [pscustomobject]@{Ok=$false;Reason='remote_close_note_out_of_order'} }; continue }
        if ($line -match '^CLOSE_BINDING runid=([^ ]+) dir=([^ ]+) files=([0-9]+)$') {
            if ($state -ne 'before' -or $matches[1] -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_close_binding_mismatch'} }
            $declaredCount=[int]$matches[3]; $state='binding'; continue
        }
        if ($line -match '^CLOSE_DIGEST_BEGIN runid=([^ ]+)$') {
            if ($state -ne 'binding' -or $matches[1] -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_digest_begin_mismatch'} }
            $state='digests'; continue
        }
        if ($line -match '^CLOSE_DIGEST ([0-9a-f]{64})  (.+)$') {
            if ($state -ne 'digests') { return [pscustomobject]@{Ok=$false;Reason='remote_digest_out_of_order'} }
            $rel=$matches[2]
            if ($rel -notmatch '^[A-Za-z0-9._/-]+$' -or $rel.StartsWith('/') -or $rel -match '(^|/)\.\.?(?:/|$)') { return [pscustomobject]@{Ok=$false;Reason='remote_digest_path_unsafe'} }
            if ($digests.ContainsKey($rel)) { return [pscustomobject]@{Ok=$false;Reason='remote_digest_duplicate'} }
            $digests.Add($rel,$matches[1]); continue
        }
        if ($line -match '^CLOSE_DIGEST_END runid=([^ ]+)$') {
            if ($state -ne 'digests' -or $matches[1] -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_digest_end_mismatch'} }
            $state='digest_end'; continue
        }
        if ($line -match '^CLOSE_SIZE_BEGIN runid=([^ ]+)$') {
            if ($state -ne 'digest_end' -or $matches[1] -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_size_begin_mismatch'} }
            $state='sizes'; continue
        }
        if ($line -match '^CLOSE_SIZE ([A-Za-z0-9._/-]+) ([0-9]+)$') {
            if ($state -ne 'sizes') { return [pscustomobject]@{Ok=$false;Reason='remote_size_out_of_order'} }
            $rel=$matches[1]
            if ($rel.StartsWith('/') -or $rel -match '(^|/)\.\.?(?:/|$)' -or $sizes.ContainsKey($rel)) { return [pscustomobject]@{Ok=$false;Reason='remote_size_path_or_duplicate'} }
            $sizes.Add($rel,[long]$matches[2]); continue
        }
        if ($line -match '^CLOSE_SIZE_END runid=([^ ]+)$') {
            if ($state -ne 'sizes' -or $matches[1] -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_size_end_mismatch'} }
            $state='size_end'; continue
        }
        if ($line -match '^CLOSE_DIGEST_SET_SHA256 runid=([^ ]+) ([0-9a-f]{64})$') {
            if ($state -ne 'size_end' -or $matches[1] -ne $expectedRunId -or $setCount -ne 0) { return [pscustomobject]@{Ok=$false;Reason='remote_set_mismatch'} }
            $setSha=$matches[2]; $setCount=1; $state='set'; continue
        }
        if ($line -match '^CLOSE PASS runid=([^ ]+) dir=([^ ]+) files=([0-9]+) wrote_into_evidence_tree=0$') {
            if ($state -ne 'set' -or $matches[1] -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_pass_mismatch'} }
            $passDeclaredCount=[int]$matches[3]; $passCount=1; $state='done'; continue
        }
        return [pscustomobject]@{Ok=$false;Reason='remote_close_unknown_or_out_of_order_record'}
    }
    if ($state -ne 'done' -or $setCount -ne 1 -or $passCount -ne 1 -or $digests.Count -eq 0) { return [pscustomobject]@{Ok=$false;Reason='remote_close_incomplete'} }
    if ($digests.Count -ne $sizes.Count -or $digests.Count -ne $declaredCount -or $digests.Count -ne $passDeclaredCount) { return [pscustomobject]@{Ok=$false;Reason='remote_close_count_mismatch'} }
    foreach ($key in $digests.Keys) { if (-not $sizes.ContainsKey($key)) { return [pscustomobject]@{Ok=$false;Reason='remote_close_name_set_mismatch'} } }
    return [pscustomobject]@{Ok=$true;Reason='complete';Digests=$digests;SetSha=$setSha}
}

function Invoke-LocalBind($op, [string] $outFile, [string] $errFile) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $bindingLog = New-Object System.Collections.ArrayList
    try {
        if ($op.Argv.Count -ne 4) { [void]$bindingLog.Add('TR_BIND_STOP reason=argv_malformed'); return 3 }
        $closeOp=$op.Argv[1]; $fetchOp=$op.Argv[2]; $relDir=$op.Argv[3]
        $localDir=Join-Path $RECORD_ROOT $relDir
        $expectedRunId=Split-Path -Leaf $localDir
        [void]$bindingLog.Add('TR_BIND close_op=' + $closeOp + ' fetch_op=' + $fetchOp + ' local_dir=' + $localDir)
        $remote=Read-RemoteCloseRecord $closeOp $expectedRunId
        if (-not $remote.Ok) { [void]$bindingLog.Add('TR_BIND_STOP reason=' + $remote.Reason); return 3 }
        if (-not (Test-Path -LiteralPath $localDir -PathType Container)) { [void]$bindingLog.Add('TR_BIND_STOP reason=local_dir_absent path=' + $localDir); return 3 }
        try {
            $items=@(Get-ChildItem -LiteralPath $localDir -Recurse -Force)
        } catch { [void]$bindingLog.Add('TR_BIND_STOP reason=local_enumeration_error detail=' + $_.Exception.GetType().FullName); return 3 }
        $local=New-Object 'System.Collections.Generic.Dictionary[string,string]' ([System.StringComparer]::Ordinal)
        $prefix=$localDir; if (-not $prefix.EndsWith('\')) { $prefix += '\' }
        foreach ($item in $items) {
            if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { [void]$bindingLog.Add('TR_BIND_STOP reason=local_reparse_point path=' + $item.FullName); return 3 }
            if ($item.PSIsContainer) { continue }
            $full=$item.FullName
            if (-not $full.StartsWith($prefix,[System.StringComparison]::OrdinalIgnoreCase)) { [void]$bindingLog.Add('TR_BIND_STOP reason=local_path_outside_dir path=' + $full); return 3 }
            $rel=$full.Substring($prefix.Length).Replace('\','/')
            if ($local.ContainsKey($rel)) { [void]$bindingLog.Add('TR_BIND_STOP reason=local_duplicate_name path=' + $rel); return 3 }
            try { $local.Add($rel,(Get-Sha256 $full)) } catch { [void]$bindingLog.Add('TR_BIND_STOP reason=local_hash_error path=' + $rel); return 3 }
        }
        [void]$bindingLog.Add('TR_BIND_COUNTS remote=' + $remote.Digests.Count + ' local=' + $local.Count)
        $ok=$true
        foreach ($rel in $remote.Digests.Keys) {
            if (-not $local.ContainsKey($rel)) { [void]$bindingLog.Add('TR_BIND_DIFF missing_locally=' + $rel); $ok=$false }
            elseif ($local[$rel] -ne $remote.Digests[$rel]) { [void]$bindingLog.Add('TR_BIND_DIFF digest_differs=' + $rel); $ok=$false }
        }
        foreach ($rel in $local.Keys) { if (-not $remote.Digests.ContainsKey($rel)) { [void]$bindingLog.Add('TR_BIND_DIFF missing_remotely=' + $rel); $ok=$false } }
        if (-not $ok) { return 1 }
        $keys=[string[]]@($remote.Digests.Keys); [Array]::Sort($keys,[System.StringComparer]::Ordinal)
        $sb=New-Object System.Text.StringBuilder
        foreach ($key in $keys) { [void]$sb.Append($remote.Digests[$key] + '  ' + $key + "`n") }
        $localSetSha=Get-Sha256OfText $sb.ToString()
        [void]$bindingLog.Add('TR_BIND_SET remote_set_sha256=' + $remote.SetSha + ' reconstructed=' + $localSetSha)
        if ($remote.SetSha -ne $localSetSha) { [void]$bindingLog.Add('TR_BIND_STOP reason=digest_set_rendering_differs'); return 3 }
        [void]$bindingLog.Add('TR_BIND_PASS files=' + $remote.Digests.Count)
        return 0
    } catch {
        [void]$bindingLog.Add('TR_BIND_STOP reason=local_exception detail=' + $_.Exception.GetType().FullName)
        return 3
    } finally {
        Write-TextFile $outFile ($bindingLog -join "`n")
        Write-TextFile $errFile ''
        $sw.Stop(); $script:LastElapsedMs=$sw.ElapsedMilliseconds
    }
}

foreach ($op in $ops) {
    $outFile=Join-Path $opsDir ($op.Id + '.stdout')
    $errFile=Join-Path $opsDir ($op.Id + '.stderr')
    $argvFile=Join-Path $opsDir ($op.Id + '.argv')
    $rcFile=Join-Path $opsDir ($op.Id + '.rc')
    $elapsedFile=Join-Path $opsDir ($op.Id + '.elapsed_ms')
    Write-TextFile $argvFile ($op.Argv -join "`n")

    if ($op.RunWhen -eq 'sequence_ok' -and -not $sequenceOk) {
        Write-TextFile $outFile ''; Write-TextFile $errFile ''; Write-TextFile $rcFile 'skipped'; Write-TextFile $elapsedFile '0'
        Emit ('TR_OP_SKIPPED id=' + $op.Id + ' reason=prior_sequence_mismatch')
        [void]$results.Add(@{Id=$op.Id;Rc='skipped';Expect=$op.ExpectRc;Elapsed=0})
        continue
    }

    Emit ('TR_OP_BEGIN id=' + $op.Id + ' kind=' + $op.Kind + ' cwd=' + $op.Cwd)
    Emit ('TR_OP_SENT_ARGV id=' + $op.Id + ' argv=[' + ($op.Argv -join '] [') + ']')
    $rc=3; $script:LastElapsedMs=0
    try {
        if ($op.Kind -eq 'tcp_probe') { $rc=Invoke-TcpProbe $op $outFile $errFile }
        elseif ($op.Kind -eq 'local_bind') { $rc=Invoke-LocalBind $op $outFile $errFile }
        elseif (-not (Test-Path -LiteralPath $op.Cwd -PathType Container)) {
            Write-TextFile $outFile ''; Write-TextFile $errFile ('cwd_absent path=' + $op.Cwd); $rc=3
        } else { $rc=Invoke-ExternalProcess $op $outFile $errFile }
    } catch {
        if (-not (Test-Path -LiteralPath $outFile)) { Write-TextFile $outFile '' }
        Write-TextFile $errFile ('operation_exception detail=' + $_.Exception.GetType().FullName)
        $rc=3
    }
    Write-TextFile $rcFile ([string]$rc)
    Write-TextFile $elapsedFile ([string]$script:LastElapsedMs)
    try { $outSha=Get-Sha256 $outFile; $errSha=Get-Sha256 $errFile } catch { Stop-Run ('capture_hash_failed op=' + $op.Id) }
    Emit ('TR_OP_END id=' + $op.Id + ' rc=' + $rc + ' expect_rc=' + $op.ExpectRc + ' elapsed_ms=' + $script:LastElapsedMs + ' stdout_sha256=' + $outSha + ' stderr_sha256=' + $errSha)
    [void]$results.Add(@{Id=$op.Id;Rc=$rc;Expect=$op.ExpectRc;Elapsed=$script:LastElapsedMs})

    if ($rc -ne $op.ExpectRc) {
        $anyMismatch=$true
        if ($firstMismatch -eq '') { $firstMismatch=$op.Id; $sequenceOk=$false; Emit ('TR_FIRST_FAIL id=' + $op.Id + ' rc=' + $rc + ' expected=' + $op.ExpectRc + ' later_sequence_ops=skip always_ops=run') }
        else { Emit ('TR_ADDITIONAL_MISMATCH id=' + $op.Id + ' first_fail=' + $firstMismatch) }
    }
}

foreach ($result in $results) { Emit ('TR_RESULT id=' + $result.Id + ' rc=' + $result.Rc + ' expect_rc=' + $result.Expect + ' elapsed_ms=' + $result.Elapsed) }
if ($anyMismatch) { Emit ('TR_RUN FAIL base_run=' + $BASE_RUN + ' first_fail=' + $firstMismatch + ' record=' + $RECORD_ROOT) }
else { Emit ('TR_RUN PASS base_run=' + $BASE_RUN + ' record=' + $RECORD_ROOT) }

try {
    Flush-Log
    $sumLines=New-Object System.Collections.ArrayList
    foreach ($file in @(Get-ChildItem -LiteralPath $RECORD_ROOT -Recurse -File -Force)) {
        if ($file.Name -eq 'TRANSPORT_SHA256SUMS.txt') { continue }
        $rel=$file.FullName.Substring($RECORD_ROOT.Length).TrimStart('\').Replace('\','/')
        [void]$sumLines.Add((Get-Sha256 $file.FullName) + '  ' + $rel)
    }
    $sorted=[string[]]@($sumLines); [Array]::Sort($sorted,[System.StringComparer]::Ordinal)
    Write-TextFile (Join-Path $RECORD_ROOT 'TRANSPORT_SHA256SUMS.txt') ($sorted -join "`n")
} catch {
    Emit ('TR_STOP reason=record_finalize_failed detail=' + $_.Exception.GetType().FullName)
    try { Flush-Log } catch {}
    exit 3
}

if ($anyMismatch) { exit 1 }
exit 0
