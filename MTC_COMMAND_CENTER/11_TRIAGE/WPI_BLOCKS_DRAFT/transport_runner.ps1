# WP-I operator-side transport recorder (DRAFT - authoring only).
#
# Executes only the internally pinned TRANSPORT_PLAN.tsv. Default mode is a
# read-only dry run. Actual execution requires both -Execute and the exact
# allocation-time confirmation token; those switches are technical interlocks,
# not host-contact authority.
#
# Outcome grammar (round 3, Codex R2 F1 / Claude R2 F1):
#   0 = every executed operation matched its preregistered rc;
#   1 = at least one operation RAN and observed deviant state (FAIL);
#   3 = the plan, an operation, or an evidence binding could not be evaluated
#       (STOP). An operation rc 3 is NEVER rolled up into rc 1.
#
# FAIL is reserved for an operation that actually ran and returned the deviant
# value its own contract defines. It is decided by operation KIND and by
# PROVENANCE, never by the integer alone:
#   * ssh_stdin  - the remote program's outcome grammar is {0,1,3}. ssh's own
#                  rc 255 is a transport failure (host down, rejected key, DNS,
#                  dropped route, refused configuration) in which NOTHING was
#                  observed, and any other rc is outside the grammar; both are
#                  not-evaluable. Even inside the grammar the rc is read as a
#                  probe result only after the capture carries at least one
#                  preregistered remote-program marker, which is the local
#                  evidence that ssh really ran the delivered script.
#   * scp_up/down- a transfer is pure transport: it observes no host state, so
#                  ONLY rc 0 is a result and every non-zero rc is not-evaluable.
#                  scp's failure rc is 1, which collides with the FAIL class and
#                  cannot be separated by rc alone - hence the kind rule.
#   * tcp_probe /
#     local_bind - operator-side and runner-implemented, grammar {0,1,3}; rc 1
#                  is a genuine completed observation.
#   * an `always` cleanup op whose prerequisite sequence never completed is
#     closing evidence of an already-broken run. Its failure is a consequence of
#     that break, never an independent observation of deviant host state.
# Precedence, when both classes occur in one run: a completed deviant
# observation outranks a later inability to evaluate, so the run is FAIL - and
# every not-evaluable operation is still enumerated by TR_OP_NOT_EVALUABLE and
# counted in TR_RUN_CLASS, so the STOP is never silently absorbed.
#
# Program identity (Codex F3): ssh and scp execute only from frozen absolute
# paths whose SHA-256, reparse state, and full-chain write ACL (by numeric SID)
# are adjudicated before the first process starts. Inherited PATH is never
# consulted. Every child runs with a deliberately constructed environment, a
# run-owned TEMP, and a preregistered working directory.
#
# Configuration identity (Codex R2 F2): ambient OpenSSH configuration is
# disabled outright rather than inherited - `-F none` refuses BOTH the per-user
# and the system-wide ssh_config - and every configuration input is supplied as
# a pinned argument or a pinned file that is bound before the first process
# starts. PROGRAMDATA is set to a run-owned directory: OpenSSH for Windows
# resolves __PROGRAMDATA__ and exits 255 with no output at all when it is unset,
# so the round-2 environment could not run the real pinned program.
#
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
# Section 5 pins op 02's working directory to 01_RUNKIT. The kit directory is
# therefore a distinct frozen location, never the prereg/draft directory: a
# decoy runkit.tar dropped beside this runner cannot be selected (Codex F8).
$RUNKIT_DIR    = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\01_RUNKIT'
# remote_close_tree.sh travels byte-identical from the accepted Stage 2 set at
# its own immutable location; it is not re-copied into the draft (Codex F9).
$ACCEPTED_DIR  = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\02_PREREG'
$RECORD_ROOT   = 'C:\WPI_ARTIFACTS\WPI_TRANSPORT_<ALLOCATE-AT-DISPATCH>'

$PLAN_NAME   = 'TRANSPORT_PLAN.tsv'
$PLAN_SHA256 = '<PIN-AT-FREEZE>'
$PLAN_HEADER = 'op_id	kind	run_when	expect_rc	cwd	stdin_file	stdin_sha256	argv	purpose'

$PINNED_FILES = @(
    @{ Path = (Join-Path $RUNKIT_DIR 'runkit.tar'); Sha = '<PIN-AT-FREEZE>' }
)

# Every stdin file resolves against exactly one frozen absolute root, named by
# the plan row itself. There is no implicit "the directory I happen to be in".
$STDIN_ROOTS = @{ 'PREREG' = $PREREG_DIR; 'ACCEPTED' = $ACCEPTED_DIR }

$SYSTEM_ROOT_PIN = 'C:\Windows'
$PROGRAM_PINS = @(
    @{ Name = 'ssh'; Path = 'C:\Windows\System32\OpenSSH\ssh.exe'; Sha = '<PIN-AT-FREEZE>' },
    @{ Name = 'scp'; Path = 'C:\Windows\System32\OpenSSH\scp.exe'; Sha = '<PIN-AT-FREEZE>' }
)
# Numeric SIDs, never rendered names (Pattern 8): only these may hold a write,
# delete, or take-ownership grant anywhere on a transport program's chain.
$TRUSTED_WRITER_SIDS = @(
    'S-1-5-18',
    'S-1-5-32-544',
    'S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464'
)

# --- configuration identity: pinned inputs, no ambient configuration ---------
# Codex R2 F2. Under the round-2 environment the real pinned ssh.exe exited 255
# with zero bytes on both streams before evaluating anything, so the plan could
# never have reached a remote block. The repair does not carry the operator's
# ambient values: it disables ambient configuration and supplies every input the
# program needs as a pinned argument or a pinned file, each bound below.
$SSH_IDENTITY_FILE          = 'C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519'
$SSH_IDENTITY_SHA           = '<PIN-AT-FREEZE>'
$SSH_USER_KNOWN_HOSTS       = 'C:\HyperV\GATEA-STAGING\ssh\wpi_known_hosts'
$SSH_USER_KNOWN_HOSTS_SHA   = '<PIN-AT-FREEZE>'
$SSH_GLOBAL_KNOWN_HOSTS     = 'C:\HyperV\GATEA-STAGING\ssh\wpi_known_hosts_global'
$SSH_GLOBAL_KNOWN_HOSTS_SHA = '<PIN-AT-FREEZE>'

# Every ssh and scp op must carry exactly this block, immediately after the
# program name. A plan row that drops '-F none', re-points a known_hosts file,
# or reinstates ProxyCommand cannot run.
$SSH_PINNED_OPTIONS = @(
    '-F', 'none',
    '-i', $SSH_IDENTITY_FILE,
    '-o', 'BatchMode=yes',
    '-o', 'StrictHostKeyChecking=yes',
    '-o', 'IdentitiesOnly=yes',
    '-o', 'ConnectTimeout=20',
    '-o', ('UserKnownHostsFile=' + $SSH_USER_KNOWN_HOSTS),
    '-o', ('GlobalKnownHostsFile=' + $SSH_GLOBAL_KNOWN_HOSTS),
    '-o', 'ProxyCommand=none',
    '-o', 'ControlMaster=no',
    '-o', 'ControlPath=none',
    '-o', 'PermitLocalCommand=no',
    '-o', 'ForwardAgent=no',
    '-o', 'ForwardX11=no',
    '-o', 'ClearAllForwardings=yes'
)
$CONFIG_PINS = @(
    @{ Name = 'ssh_identity'; Path = $SSH_IDENTITY_FILE; Sha = $SSH_IDENTITY_SHA; Print = $false;
       Why = 'the_only_credential_-i_names_and_IdentitiesOnly=yes_admits' },
    @{ Name = 'user_known_hosts'; Path = $SSH_USER_KNOWN_HOSTS; Sha = $SSH_USER_KNOWN_HOSTS_SHA; Print = $true;
       Why = 'StrictHostKeyChecking=yes_decides_against_this_frozen_set_not_the_operator_profile' },
    @{ Name = 'global_known_hosts'; Path = $SSH_GLOBAL_KNOWN_HOSTS; Sha = $SSH_GLOBAL_KNOWN_HOSTS_SHA; Print = $true;
       Why = 'the_system_half_of_the_same_decision_so___PROGRAMDATA___supplies_nothing' }
)

# Why each constructed variable exists. Printed with the value, so the record
# states the reason rather than leaving the reader to infer it (Codex R2 F2).
$ENV_RATIONALE = @{
    'SystemRoot'  = 'the_pinned_system_root_every_program_chain_is_adjudicated_against';
    'windir'      = 'same_value_under_the_legacy_name_some_libraries_still_read';
    'ComSpec'     = 'pinned_absolute_so_no_inherited_value_can_name_another_interpreter';
    'PATHEXT'     = 'frozen_so_extension_search_order_is_not_inherited';
    'PATH'        = 'frozen_to_the_pinned_system_root_the_inherited_PATH_never_reaches_a_child';
    'TEMP'        = 'run_owned_under_the_record_root_not_the_operator_temp';
    'TMP'         = 'same_value_under_the_second_name';
    'PROGRAMDATA' = 'run_owned_and_empty_OpenSSH_for_Windows_exits_255_with_no_output_when_it_is_unset_and_would_otherwise_read_the_ambient___PROGRAMDATA___ssh_tree'
}

# --- observed-outcome grammar (Codex R2 F1 / Claude R2 F1) -------------------
$REMOTE_OUTCOME_RCS = @(0, 1, 3)
$SSH_TRANSPORT_RC   = 255
# The result-line prefixes the five preregistered remote programs emit. At least
# one must appear in a capture before an ssh op's rc is read as a probe result:
# it is the local evidence that ssh actually ran the delivered script rather
# than failing in transport.
$REMOTE_MARKER_PREFIXES = @(
    'SETUP_', 'SETUP ', 'EXTRACT_', 'EXTRACT ', 'P0W_', 'P0W ',
    'ROW_', 'ROW ', 'CLOSE_', 'CLOSE '
)

$ALLOWED_KINDS    = @('ssh_stdin', 'scp_up', 'scp_down', 'tcp_probe', 'local_bind')
$ALLOWED_RUN_WHEN = @('sequence_ok', 'always')
$ALLOWED_PROGRAMS = @('ssh', 'scp')
$KIND_PROGRAM     = @{ 'ssh_stdin' = 'ssh'; 'scp_up' = 'scp'; 'scp_down' = 'scp' }
$UNFILLED_MARKERS = @('<ALLOCATE-AT-DISPATCH>', '<PIN-AT-FREEZE>')

# --------------------------------------------------------------------- output
$script:Log = New-Object System.Collections.ArrayList
$script:RecordReady = $false
$script:LastElapsedMs = 0
$script:LastStdinState = 'none'
$script:StdinPathById = @{}
$script:ProgramByName = @{}
$script:ChildEnv = New-Object 'System.Collections.Generic.Dictionary[string,string]' ([System.StringComparer]::OrdinalIgnoreCase)

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

function Test-HexSha256([string] $value) {
    return $value -match '^[0-9a-f]{64}$'
}

function Test-ReparsePoint([string] $path) {
    $item = Get-Item -LiteralPath $path -Force
    return (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
}

# Fail-closed gate for unfilled freeze/allocation markers (Claude F6). Every
# frozen constant and every plan field passes through this before it is used,
# so a partially frozen set STOPs with a reason token instead of dying inside
# Test-Path with a localized .NET message.
function Test-MarkerFree([string] $value) {
    foreach ($m in $UNFILLED_MARKERS) { if ($value.Contains($m)) { return $false } }
    return $true
}

function Assert-MarkerFree([string] $name, [string] $value) {
    if (-not (Test-MarkerFree $value)) { Stop-Run ('unfilled_marker field=' + $name) }
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

# stdin_file grammar: '-' or '<ROOT>:<basename>' where <ROOT> is a frozen key of
# $STDIN_ROOTS and <basename> carries no separator.
function Resolve-StdinPath([string] $spec) {
    $idx = $spec.IndexOf(':')
    if ($idx -lt 1) { return [pscustomobject]@{ Ok = $false; Reason = 'stdin_spec_no_root_token' } }
    $rootKey = $spec.Substring(0, $idx)
    $leaf = $spec.Substring($idx + 1)
    if (-not $STDIN_ROOTS.ContainsKey($rootKey)) { return [pscustomobject]@{ Ok = $false; Reason = ('stdin_root_unknown=' + $rootKey) } }
    if ($leaf -notmatch '^[A-Za-z0-9._-]+$') { return [pscustomobject]@{ Ok = $false; Reason = 'stdin_leaf_unsafe' } }
    return [pscustomobject]@{ Ok = $true; Reason = 'ok'; Path = (Join-Path $STDIN_ROOTS[$rootKey] $leaf); Root = $rootKey }
}

function Get-PathChainToSystemRoot([string] $path) {
    $chain = New-Object System.Collections.ArrayList
    $cur = $path
    for ($i = 0; $i -lt 32; $i++) {
        [void] $chain.Add($cur)
        if ($cur -eq $SYSTEM_ROOT_PIN) { return [pscustomobject]@{ Ok = $true; Nodes = @($chain) } }
        $parent = Split-Path -Parent $cur
        if ([string]::IsNullOrEmpty($parent) -or $parent -eq $cur) { break }
        $cur = $parent
    }
    return [pscustomobject]@{ Ok = $false; Nodes = @($chain) }
}

$WRITE_RIGHTS_MASK =
    ([int][System.Security.AccessControl.FileSystemRights]::WriteData) -bor
    ([int][System.Security.AccessControl.FileSystemRights]::AppendData) -bor
    ([int][System.Security.AccessControl.FileSystemRights]::WriteExtendedAttributes) -bor
    ([int][System.Security.AccessControl.FileSystemRights]::WriteAttributes) -bor
    ([int][System.Security.AccessControl.FileSystemRights]::Delete) -bor
    ([int][System.Security.AccessControl.FileSystemRights]::DeleteSubdirectoriesAndFiles) -bor
    ([int][System.Security.AccessControl.FileSystemRights]::ChangePermissions) -bor
    ([int][System.Security.AccessControl.FileSystemRights]::TakeOwnership)

# Returns '' when the whole chain from the program up to %SystemRoot% is free of
# reparse points and grants write/delete/ownership only to trusted numeric SIDs.
function Test-TrustedProgramChain([string] $path) {
    $chain = Get-PathChainToSystemRoot $path
    if (-not $chain.Ok) { return ('not_under_pinned_system_root path=' + $path) }
    foreach ($node in $chain.Nodes) {
        if (-not (Test-Path -LiteralPath $node)) { return ('chain_component_missing=' + $node) }
        try { if (Test-ReparsePoint $node) { return ('chain_component_is_reparse_point=' + $node) } }
        catch { return ('chain_component_metadata_unreadable=' + $node) }
        $acl = $null
        try { $acl = Get-Acl -LiteralPath $node } catch { return ('chain_component_acl_unreadable=' + $node) }
        $ownerSid = ''
        try { $ownerSid = [string]$acl.GetOwner([System.Security.Principal.SecurityIdentifier]).Value }
        catch { return ('chain_owner_unresolvable=' + $node) }
        if ($TRUSTED_WRITER_SIDS -notcontains $ownerSid) { return ('chain_owner_sid_untrusted=' + $ownerSid + ' path=' + $node) }
        $rules = $null
        try { $rules = $acl.GetAccessRules($true, $true, [System.Security.Principal.SecurityIdentifier]) }
        catch { return ('chain_acl_rules_unreadable=' + $node) }
        foreach ($ace in $rules) {
            if ($ace.AccessControlType -ne [System.Security.AccessControl.AccessControlType]::Allow) { continue }
            if ((([int]$ace.FileSystemRights) -band $WRITE_RIGHTS_MASK) -eq 0) { continue }
            $sid = [string]$ace.IdentityReference.Value
            if ($TRUSTED_WRITER_SIDS -notcontains $sid) { return ('chain_write_ace_untrusted=' + $sid + ' path=' + $node) }
        }
    }
    return ''
}

# Any terminating error that escapes a specific handler becomes a reasoned STOP
# at the documented exit 3 instead of a raw localized .NET exit 1 (Claude F6).
trap {
    $detail = 'unknown'
    try { $detail = $_.Exception.GetType().FullName } catch { }
    try { Emit ('TR_STOP reason=runner_unhandled_error detail=' + $detail) }
    catch { Write-Host ('TR_STOP reason=runner_unhandled_error detail=' + $detail) }
    try { Flush-Log } catch { }
    exit 3
}

# ------------------------------------------------------------------ preflight
Emit ('TR_HEADER base_run=' + $BASE_RUN)
Emit ('TR_MODE execute=' + $Execute.IsPresent + ' confirm_supplied=' + [string](-not [string]::IsNullOrEmpty($Confirm)))

# Marker gate first: nothing below may consume a constant that still carries an
# allocation or freeze placeholder.
Assert-MarkerFree 'BASE_RUN' $BASE_RUN
Assert-MarkerFree 'CONFIRM_TOKEN' $CONFIRM_TOKEN
Assert-MarkerFree 'PREREG_DIR' $PREREG_DIR
Assert-MarkerFree 'RUNKIT_DIR' $RUNKIT_DIR
Assert-MarkerFree 'ACCEPTED_DIR' $ACCEPTED_DIR
Assert-MarkerFree 'RECORD_ROOT' $RECORD_ROOT
Assert-MarkerFree 'PLAN_SHA256' $PLAN_SHA256
foreach ($pin in $PINNED_FILES) {
    Assert-MarkerFree ('PINNED_FILES.Path[' + $pin.Path + ']') $pin.Path
    Assert-MarkerFree ('PINNED_FILES.Sha[' + $pin.Path + ']') $pin.Sha
}
foreach ($prog in $PROGRAM_PINS) {
    Assert-MarkerFree ('PROGRAM_PINS.Path[' + $prog.Name + ']') $prog.Path
    Assert-MarkerFree ('PROGRAM_PINS.Sha[' + $prog.Name + ']') $prog.Sha
}
foreach ($cfg in $CONFIG_PINS) {
    Assert-MarkerFree ('CONFIG_PINS.Path[' + $cfg.Name + ']') $cfg.Path
    Assert-MarkerFree ('CONFIG_PINS.Sha[' + $cfg.Name + ']') $cfg.Sha
}
foreach ($optElement in $SSH_PINNED_OPTIONS) {
    Assert-MarkerFree 'SSH_PINNED_OPTIONS' $optElement
}
Emit 'TR_MARKER_GATE constants=marker_free'

$here = Split-Path -Parent $PSCommandPath
if ($here -ne $PREREG_DIR) { Stop-Run ('runner_not_in_preregistered_directory here=' + $here + ' expected=' + $PREREG_DIR) }
Emit ('TR_LOCATION dir=' + $here)

$executeMode = ($Execute.IsPresent -and $Confirm -eq $CONFIRM_TOKEN)

# The record root is created before the remaining preflight so that a preflight
# STOP - precisely the failure class that decides whether a RUNID is burned -
# still leaves a TRANSPORT_RECORD.txt behind (section 6; Claude N4).
$opsDir = Join-Path $RECORD_ROOT 'ops'
$tmpDir = Join-Path $RECORD_ROOT 'tmp'
# The child's PROGRAMDATA. It is created empty and run-owned, so even a code
# path that still consults __PROGRAMDATA__ finds nothing ambient there.
$sshConfDir = Join-Path $RECORD_ROOT 'sshconf'
if ($executeMode) {
    if (Test-Path -LiteralPath $RECORD_ROOT) { Stop-Run ('record_root_already_exists path=' + $RECORD_ROOT) }
    try {
        [void](New-Item -ItemType Directory -Path $RECORD_ROOT)
        [void](New-Item -ItemType Directory -Path $opsDir)
        [void](New-Item -ItemType Directory -Path (Join-Path $RECORD_ROOT 'evidence'))
        [void](New-Item -ItemType Directory -Path $tmpDir)
        [void](New-Item -ItemType Directory -Path $sshConfDir)
        [void](New-Item -ItemType Directory -Path (Join-Path $sshConfDir 'ssh'))
    } catch { Stop-Run ('record_root_creation_failed detail=' + $_.Exception.GetType().FullName) }
    $script:RecordReady = $true
    Emit ('TR_RECORD_ROOT path=' + $RECORD_ROOT)
}

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

$evidenceDir = Join-Path $RECORD_ROOT 'evidence'
$ALLOWED_CWDS = @($PREREG_DIR, $RUNKIT_DIR, $RECORD_ROOT, $evidenceDir)

$ops = New-Object System.Collections.ArrayList
$seenIds = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
$previousId = -1
for ($i = 1; $i -lt $planLines.Count; $i++) {
    $raw = $planLines[$i]
    if ($raw.Length -eq 0) { Stop-Run ('plan_blank_record row=' + ($i + 1)) }
    Assert-MarkerFree ('plan_row_' + ($i + 1)) $raw
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
    if ($ALLOWED_CWDS -notcontains $f[4]) { Stop-Run ('plan_row_cwd_not_preregistered op=' + $f[0] + ' cwd=' + $f[4]) }
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
    # Kind and program agree element-for-element, not merely set-wise (Claude N3).
    if ($KIND_PROGRAM.ContainsKey($op.Kind)) {
        if ($ALLOWED_PROGRAMS -notcontains $op.Argv[0]) { Stop-Run ('plan_row_program_not_allowed=' + $op.Argv[0] + ' op=' + $op.Id) }
        if ($op.Argv[0] -ne $KIND_PROGRAM[$op.Kind]) { Stop-Run ('plan_row_kind_program_mismatch op=' + $op.Id + ' kind=' + $op.Kind + ' program=' + $op.Argv[0]) }
        # The frozen configuration block must follow the program name verbatim
        # (Codex R2 F2). This is what makes '-F none' and the pinned
        # known_hosts files a property of the runner rather than of whichever
        # plan happens to be present.
        if ($op.Argv.Count -lt (1 + $SSH_PINNED_OPTIONS.Count)) {
            Stop-Run ('plan_row_pinned_options_absent op=' + $op.Id + ' argc=' + $op.Argv.Count + ' required=' + (1 + $SSH_PINNED_OPTIONS.Count))
        }
        for ($k = 0; $k -lt $SSH_PINNED_OPTIONS.Count; $k++) {
            if ($op.Argv[$k + 1] -ne $SSH_PINNED_OPTIONS[$k]) {
                Stop-Run ('plan_row_pinned_option_differs op=' + $op.Id + ' index=' + ($k + 1) + ' actual=[' + $op.Argv[$k + 1] + '] expected=[' + $SSH_PINNED_OPTIONS[$k] + ']')
            }
        }
    }
    # Only ssh_stdin carries a stdin file; every other kind must declare none.
    if ($op.Kind -eq 'ssh_stdin') {
        if ($op.StdinRel -eq '-') { Stop-Run ('plan_row_ssh_stdin_without_file op=' + $op.Id) }
    } elseif ($op.StdinRel -ne '-') {
        Stop-Run ('plan_row_stdin_file_on_non_ssh_kind op=' + $op.Id + ' kind=' + $op.Kind)
    }
    [void] $ops.Add($op)
}
Emit ('TR_PLAN_ROWS count=' + $ops.Count)

foreach ($op in $ops) {
    if ($op.StdinRel -eq '-') {
        if ($op.StdinSha -ne '-') { Stop-Run ('stdin_sha_without_file op=' + $op.Id) }
        continue
    }
    $resolved = Resolve-StdinPath $op.StdinRel
    if (-not $resolved.Ok) { Stop-Run ($resolved.Reason + ' op=' + $op.Id + ' spec=' + $op.StdinRel) }
    if (-not (Test-HexSha256 $op.StdinSha)) { Stop-Run ('stdin_pin_unfilled_or_malformed op=' + $op.Id) }
    $stdinPath = $resolved.Path
    if (-not (Test-Path -LiteralPath $stdinPath -PathType Leaf)) { Stop-Run ('stdin_file_missing op=' + $op.Id + ' path=' + $stdinPath) }
    try {
        if (Test-ReparsePoint $stdinPath) { Stop-Run ('stdin_file_is_reparse_point op=' + $op.Id + ' path=' + $stdinPath) }
        $stdinSha = Get-Sha256 $stdinPath
    } catch { Stop-Run ('stdin_file_not_evaluable op=' + $op.Id + ' detail=' + $_.Exception.GetType().FullName) }
    Emit ('TR_STDIN op=' + $op.Id + ' root=' + $resolved.Root + ' path=' + $stdinPath + ' sha256=' + $stdinSha)
    if ($stdinSha -ne $op.StdinSha) { Stop-Run ('stdin_sha256_mismatch op=' + $op.Id + ' actual=' + $stdinSha + ' expected=' + $op.StdinSha) }
    $script:StdinPathById[$op.Id] = $stdinPath
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

# --- program identity: pinned absolute path, frozen digest, trusted chain -----
$requiredPrograms = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
foreach ($op in $ops) {
    if ($KIND_PROGRAM.ContainsKey($op.Kind)) { [void]$requiredPrograms.Add($op.Argv[0]) }
}
foreach ($prog in $PROGRAM_PINS) {
    if (-not $requiredPrograms.Contains($prog.Name)) { continue }
    if (-not (Test-HexSha256 $prog.Sha)) { Stop-Run ('program_pin_unfilled name=' + $prog.Name) }
    if (-not (Test-Path -LiteralPath $prog.Path -PathType Leaf)) { Stop-Run ('program_missing name=' + $prog.Name + ' path=' + $prog.Path) }
    try {
        if (Test-ReparsePoint $prog.Path) { Stop-Run ('program_is_reparse_point name=' + $prog.Name + ' path=' + $prog.Path) }
        $progSha = Get-Sha256 $prog.Path
    } catch { Stop-Run ('program_not_evaluable name=' + $prog.Name + ' detail=' + $_.Exception.GetType().FullName) }
    $chainProblem = Test-TrustedProgramChain $prog.Path
    if ($chainProblem -ne '') { Stop-Run ('program_chain_untrusted name=' + $prog.Name + ' detail=' + $chainProblem) }
    Emit ('TR_PROGRAM name=' + $prog.Name + ' path=' + $prog.Path + ' sha256=' + $progSha + ' resolution=pinned_absolute chain=trusted')
    if ($progSha -ne $prog.Sha) { Stop-Run ('program_sha256_mismatch name=' + $prog.Name + ' actual=' + $progSha + ' expected=' + $prog.Sha) }
    $script:ProgramByName[$prog.Name] = $prog.Path
}
foreach ($needed in $requiredPrograms) {
    if (-not $script:ProgramByName.ContainsKey($needed)) { Stop-Run ('program_not_pinned name=' + $needed) }
}

# --- configuration identity: every input the pinned options name is bound -----
# Each entry records WHY the transport needs it. The identity file's digest is
# compared but never printed: it is the one bound input that is key material.
# Scope, stated rather than implied: these three are bound by kind, reparse
# state and frozen digest. They are deliberately NOT held to the program
# chain's trusted-writer rule - they live in the operator's own credential
# directory, which the operator must be able to manage, so a write-ACL
# predicate there would assert something the deployment cannot honour.
if ($requiredPrograms.Count -gt 0) {
    foreach ($cfg in $CONFIG_PINS) {
        if (-not (Test-HexSha256 $cfg.Sha)) { Stop-Run ('config_pin_unfilled name=' + $cfg.Name) }
        if (-not (Test-Path -LiteralPath $cfg.Path -PathType Leaf)) { Stop-Run ('config_file_missing name=' + $cfg.Name + ' path=' + $cfg.Path) }
        try {
            if (Test-ReparsePoint $cfg.Path) { Stop-Run ('config_file_is_reparse_point name=' + $cfg.Name + ' path=' + $cfg.Path) }
            $cfgSha = Get-Sha256 $cfg.Path
        } catch { Stop-Run ('config_file_not_evaluable name=' + $cfg.Name + ' detail=' + $_.Exception.GetType().FullName) }
        $shown = $cfgSha
        if ($cfg.Print -ne $true) { $shown = 'withheld_key_material' }
        Emit ('TR_CONFIG name=' + $cfg.Name + ' path=' + $cfg.Path + ' sha256=' + $shown + ' why=' + $cfg.Why)
        if ($cfgSha -ne $cfg.Sha) {
            if ($cfg.Print -eq $true) { Stop-Run ('config_file_sha256_mismatch name=' + $cfg.Name + ' actual=' + $cfgSha + ' expected=' + $cfg.Sha) }
            Stop-Run ('config_file_sha256_mismatch name=' + $cfg.Name + ' actual=withheld expected=withheld')
        }
    }
}

# --- the environment every child receives, constructed rather than inherited --
# NOTHING is carried from the operator's environment (Codex R2 F2). The round-2
# runner carried USERPROFILE/HOMEDRIVE/HOMEPATH on the belief that ssh reads
# known_hosts under the operator profile; measurement showed OpenSSH for Windows
# resolves the home directory from the OS token, so carrying them never closed
# that channel - only '-F none' plus the pinned UserKnownHostsFile does. Every
# value below is a frozen constant or a run-owned path, and each carries the
# reason it is present.
$script:ChildEnv['SystemRoot'] = $SYSTEM_ROOT_PIN
$script:ChildEnv['windir'] = $SYSTEM_ROOT_PIN
$script:ChildEnv['ComSpec'] = (Join-Path $SYSTEM_ROOT_PIN 'System32\cmd.exe')
$script:ChildEnv['PATHEXT'] = '.COM;.EXE;.BAT;.CMD'
$script:ChildEnv['PATH'] = ((Join-Path $SYSTEM_ROOT_PIN 'System32') + ';' + $SYSTEM_ROOT_PIN)
$script:ChildEnv['TEMP'] = $tmpDir
$script:ChildEnv['TMP'] = $tmpDir
$script:ChildEnv['PROGRAMDATA'] = $sshConfDir
foreach ($name in ($script:ChildEnv.Keys | Sort-Object)) {
    $why = 'unstated'
    if ($ENV_RATIONALE.ContainsKey($name)) { $why = $ENV_RATIONALE[$name] }
    Emit ('TR_ENV name=' + $name + ' value=' + $script:ChildEnv[$name] + ' why=' + $why)
}
Emit ('TR_ENV_POLICY cleared=all carried=none inherited_path=never ambient_ssh_config=disabled_by_-F_none')

foreach ($op in $ops) {
    Emit ('TR_OP_PLANNED id=' + $op.Id + ' kind=' + $op.Kind + ' run_when=' + $op.RunWhen + ' expect_rc=' + $op.ExpectRc + ' stdin=' + $op.StdinRel)
    Emit ('TR_OP_ARGV id=' + $op.Id + ' argv=[' + ($op.Argv -join '] [') + ']')
}

if (-not $executeMode) {
    Emit 'TR_DRY_RUN no_process_was_started no_connection_was_opened'
    Emit ('TR_DRY_RUN to_execute=-Execute_-Confirm_' + $CONFIRM_TOKEN)
    exit 0
}

# ------------------------------------------------------------------ execution
$sequenceOk = $true
$anyDeviant = $false
$anyNotEvaluable = $false
$deviantCount = 0
$notEvaluableCount = 0
$firstMismatch = ''
$firstNotEvaluable = ''
$results = New-Object System.Collections.ArrayList

function Invoke-ExternalProcess($op, [string] $outFile, [string] $errFile) {
    $exe = $script:ProgramByName[$op.Argv[0]]
    $rest = @()
    if ($op.Argv.Count -gt 1) { $rest = $op.Argv[1..($op.Argv.Count - 1)] }
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $exe
    # Every argv element has already been proven free of whitespace and shell
    # metacharacters, so a single space join is faithful element-for-element.
    $psi.Arguments = ($rest -join ' ')
    $psi.WorkingDirectory = $op.Cwd
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.RedirectStandardInput = $true
    $psi.EnvironmentVariables.Clear()
    foreach ($k in $script:ChildEnv.Keys) { $psi.EnvironmentVariables[$k] = $script:ChildEnv[$k] }

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $proc = $null; $outFs = $null; $errFs = $null
    $script:LastStdinState = 'none'
    try {
        $outFs = [System.IO.File]::Create($outFile)
        $errFs = [System.IO.File]::Create($errFile)
        $proc = [System.Diagnostics.Process]::Start($psi)
        # Both capture streams are drained concurrently: a child that fills one
        # pipe while the runner waits on the other cannot deadlock the record.
        $outCopy = $proc.StandardOutput.BaseStream.CopyToAsync($outFs)
        $errCopy = $proc.StandardError.BaseStream.CopyToAsync($errFs)
        if ($op.StdinRel -ne '-') {
            $bytes = [System.IO.File]::ReadAllBytes($script:StdinPathById[$op.Id])
            try {
                $proc.StandardInput.BaseStream.Write($bytes, 0, $bytes.Length)
                $proc.StandardInput.BaseStream.Flush()
                $script:LastStdinState = 'complete'
            } catch {
                $script:LastStdinState = 'incomplete'
            }
        }
        $proc.StandardInput.Close()
        $proc.WaitForExit()
        $outCopy.Wait()
        $errCopy.Wait()
        if ($script:LastStdinState -eq 'incomplete') { return 3 }
        return $proc.ExitCode
    } finally {
        if ($null -ne $proc) { $proc.Dispose() }
        if ($null -ne $outFs) { $outFs.Dispose() }
        if ($null -ne $errFs) { $errFs.Dispose() }
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

# Every regex capture is latched into an ordinary local variable on the line
# after its own match, before any further -match/-notmatch can repopulate the
# automatic $Matches collection (Claude F1 / Codex F2).
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
            $capRunId = $matches[1]; $capFiles = $matches[3]
            if ($state -ne 'before' -or $capRunId -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_close_binding_mismatch'} }
            $declaredCount=[int]$capFiles; $state='binding'; continue
        }
        if ($line -match '^CLOSE_DIGEST_BEGIN runid=([^ ]+)$') {
            $capRunId = $matches[1]
            if ($state -ne 'binding' -or $capRunId -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_digest_begin_mismatch'} }
            $state='digests'; continue
        }
        if ($line -match '^CLOSE_DIGEST ([0-9a-f]{64})  (.+)$') {
            $capDigest = $matches[1]; $capRel = $matches[2]
            if ($state -ne 'digests') { return [pscustomobject]@{Ok=$false;Reason='remote_digest_out_of_order'} }
            if ($capRel -notmatch '^[A-Za-z0-9._/-]+$' -or $capRel.StartsWith('/') -or $capRel -match '(^|/)\.\.?(?:/|$)') { return [pscustomobject]@{Ok=$false;Reason='remote_digest_path_unsafe'} }
            if ($digests.ContainsKey($capRel)) { return [pscustomobject]@{Ok=$false;Reason='remote_digest_duplicate'} }
            $digests.Add($capRel,$capDigest); continue
        }
        if ($line -match '^CLOSE_DIGEST_END runid=([^ ]+)$') {
            $capRunId = $matches[1]
            if ($state -ne 'digests' -or $capRunId -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_digest_end_mismatch'} }
            $state='digest_end'; continue
        }
        if ($line -match '^CLOSE_SIZE_BEGIN runid=([^ ]+)$') {
            $capRunId = $matches[1]
            if ($state -ne 'digest_end' -or $capRunId -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_size_begin_mismatch'} }
            $state='sizes'; continue
        }
        if ($line -match '^CLOSE_SIZE ([A-Za-z0-9._/-]+) ([0-9]+)$') {
            $capRel = $matches[1]; $capSize = $matches[2]
            if ($state -ne 'sizes') { return [pscustomobject]@{Ok=$false;Reason='remote_size_out_of_order'} }
            if ($capRel.StartsWith('/') -or $capRel -match '(^|/)\.\.?(?:/|$)' -or $sizes.ContainsKey($capRel)) { return [pscustomobject]@{Ok=$false;Reason='remote_size_path_or_duplicate'} }
            $sizes.Add($capRel,[long]$capSize); continue
        }
        if ($line -match '^CLOSE_SIZE_END runid=([^ ]+)$') {
            $capRunId = $matches[1]
            if ($state -ne 'sizes' -or $capRunId -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_size_end_mismatch'} }
            $state='size_end'; continue
        }
        if ($line -match '^CLOSE_DIGEST_SET_SHA256 runid=([^ ]+) ([0-9a-f]{64})$') {
            $capRunId = $matches[1]; $capSetSha = $matches[2]
            if ($state -ne 'size_end' -or $capRunId -ne $expectedRunId -or $setCount -ne 0) { return [pscustomobject]@{Ok=$false;Reason='remote_set_mismatch'} }
            $setSha=$capSetSha; $setCount=1; $state='set'; continue
        }
        if ($line -match '^CLOSE PASS runid=([^ ]+) dir=([^ ]+) files=([0-9]+) wrote_into_evidence_tree=0$') {
            $capRunId = $matches[1]; $capFiles = $matches[3]
            if ($state -ne 'set' -or $capRunId -ne $expectedRunId) { return [pscustomobject]@{Ok=$false;Reason='remote_pass_mismatch'} }
            $passDeclaredCount=[int]$capFiles; $passCount=1; $state='done'; continue
        }
        return [pscustomobject]@{Ok=$false;Reason='remote_close_unknown_or_out_of_order_record'}
    }
    if ($state -ne 'done' -or $setCount -ne 1 -or $passCount -ne 1 -or $digests.Count -eq 0) { return [pscustomobject]@{Ok=$false;Reason='remote_close_incomplete'} }
    if ($digests.Count -ne $sizes.Count -or $digests.Count -ne $declaredCount -or $digests.Count -ne $passDeclaredCount) { return [pscustomobject]@{Ok=$false;Reason='remote_close_count_mismatch'} }
    foreach ($key in $digests.Keys) { if (-not $sizes.ContainsKey($key)) { return [pscustomobject]@{Ok=$false;Reason='remote_close_name_set_mismatch'} } }
    return [pscustomobject]@{Ok=$true;Reason='complete';Digests=$digests;Sizes=$sizes;SetSha=$setSha}
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
        $localSizes=New-Object 'System.Collections.Generic.Dictionary[string,long]' ([System.StringComparer]::Ordinal)
        $prefix=$localDir; if (-not $prefix.EndsWith('\')) { $prefix += '\' }
        foreach ($item in $items) {
            if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { [void]$bindingLog.Add('TR_BIND_STOP reason=local_reparse_point path=' + $item.FullName); return 3 }
            if ($item.PSIsContainer) { continue }
            $full=$item.FullName
            if (-not $full.StartsWith($prefix,[System.StringComparison]::OrdinalIgnoreCase)) { [void]$bindingLog.Add('TR_BIND_STOP reason=local_path_outside_dir path=' + $full); return 3 }
            $rel=$full.Substring($prefix.Length).Replace('\','/')
            if ($local.ContainsKey($rel)) { [void]$bindingLog.Add('TR_BIND_STOP reason=local_duplicate_name path=' + $rel); return 3 }
            try { $local.Add($rel,(Get-Sha256 $full)); $localSizes.Add($rel,[long]$item.Length) } catch { [void]$bindingLog.Add('TR_BIND_STOP reason=local_hash_error path=' + $rel); return 3 }
        }
        [void]$bindingLog.Add('TR_BIND_COUNTS remote=' + $remote.Digests.Count + ' local=' + $local.Count)
        $ok=$true
        foreach ($rel in $remote.Digests.Keys) {
            if (-not $local.ContainsKey($rel)) { [void]$bindingLog.Add('TR_BIND_DIFF missing_locally=' + $rel); $ok=$false }
            elseif ($local[$rel] -ne $remote.Digests[$rel]) { [void]$bindingLog.Add('TR_BIND_DIFF digest_differs=' + $rel); $ok=$false }
            elseif ($localSizes[$rel] -ne $remote.Sizes[$rel]) { [void]$bindingLog.Add('TR_BIND_DIFF size_differs=' + $rel + ' remote=' + $remote.Sizes[$rel] + ' local=' + $localSizes[$rel]); $ok=$false }
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
        foreach ($bl in $bindingLog) { Emit ('  | ' + $bl) }
        $sw.Stop(); $script:LastElapsedMs=$sw.ElapsedMilliseconds
    }
}

# --- provenance: did the remote program actually run? -----------------------
# ssh conveys the remote command's status faithfully EXCEPT when it never ran
# one. The captures are therefore scanned for a preregistered remote result-line
# prefix before an ssh op's rc is read as a probe result. Latin-1 keeps every
# byte a distinct character, so a marker is still found in a capture that also
# carries bytes the strict record reader would refuse - the test must not fail
# open on odd content, and must not fail closed on a legitimate marker.
function Test-RemoteProvenanceMarker([string] $outFile, [string] $errFile) {
    foreach ($f in @($outFile, $errFile)) {
        if (-not (Test-Path -LiteralPath $f -PathType Leaf)) { continue }
        $bytes = $null
        try { $bytes = [System.IO.File]::ReadAllBytes($f) } catch { continue }
        if ($bytes.Length -eq 0) { continue }
        $text = [System.Text.Encoding]::GetEncoding(28591).GetString($bytes)
        foreach ($rawLine in $text.Split([char]10)) {
            $line = $rawLine.TrimEnd([char]13)
            foreach ($prefix in $REMOTE_MARKER_PREFIXES) {
                if ($line.StartsWith($prefix, [System.StringComparison]::Ordinal)) { return $true }
            }
        }
    }
    return $false
}

# --- classify one observed outcome by KIND and PROVENANCE, not by integer ----
# Returns 'match', 'deviant' or 'not_evaluable' with the reason it was reached.
# 'deviant' - and therefore TR_RUN FAIL - is reachable only for an operation
# that ran and returned the deviant value its own contract defines.
function Get-OpOutcomeClass($op, $rc, [string] $outFile, [string] $errFile, [bool] $prerequisiteEstablished) {
    if ($op.Kind -eq 'ssh_stdin') {
        # ssh's own code for could-not-connect / could-not-authenticate /
        # connection-closed. Nothing was observed, so nothing is deviant.
        if ($rc -eq $SSH_TRANSPORT_RC) { return @{ Class = 'not_evaluable'; Reason = 'ssh_transport_failure_rc255' } }
        if ($REMOTE_OUTCOME_RCS -notcontains $rc) { return @{ Class = 'not_evaluable'; Reason = 'rc_outside_outcome_grammar' } }
        if (-not (Test-RemoteProvenanceMarker $outFile $errFile)) {
            return @{ Class = 'not_evaluable'; Reason = 'no_remote_program_marker_in_capture' }
        }
    } elseif ($op.Kind -eq 'scp_up' -or $op.Kind -eq 'scp_down') {
        # A transfer observes no host state. Its failure rc is 1, which collides
        # with the FAIL class and cannot be separated by rc alone, so the kind
        # decides: only a completed transfer is a result.
        if ($rc -ne 0) { return @{ Class = 'not_evaluable'; Reason = 'scp_transfer_did_not_complete' } }
    } else {
        if ($REMOTE_OUTCOME_RCS -notcontains $rc) { return @{ Class = 'not_evaluable'; Reason = 'rc_outside_outcome_grammar' } }
    }
    if ($rc -eq $op.ExpectRc) { return @{ Class = 'match'; Reason = 'preregistered_rc' } }
    if ($rc -eq 3) { return @{ Class = 'not_evaluable'; Reason = 'operation_reported_stop' } }
    # An `always` op runs unconditionally so that a broken run's evidence is
    # still closed, retrieved and bound. When the sequence that was supposed to
    # CREATE that evidence never completed, this op's failure is a consequence
    # of the earlier break - a cleanup with nothing to clean - and must not
    # outvote the truthful earlier STOP with a manufactured host-state FAIL.
    if ($op.RunWhen -eq 'always' -and -not $prerequisiteEstablished) {
        return @{ Class = 'not_evaluable'; Reason = 'cleanup_after_unestablished_prerequisite' }
    }
    return @{ Class = 'deviant'; Reason = 'operation_ran_and_observed_deviant_state' }
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

    # Captured before this operation can change it: whether every operation the
    # plan sequenced ahead of this one matched its preregistered rc.
    $prerequisiteEstablished = $sequenceOk

    Emit ('TR_OP_BEGIN id=' + $op.Id + ' kind=' + $op.Kind + ' cwd=' + $op.Cwd)
    Emit ('TR_OP_SENT_ARGV id=' + $op.Id + ' argv=[' + ($op.Argv -join '] [') + ']')
    $rc=3; $script:LastElapsedMs=0; $script:LastStdinState='none'
    try {
        if ($op.Kind -eq 'tcp_probe') { $rc=Invoke-TcpProbe $op $outFile $errFile }
        elseif ($op.Kind -eq 'local_bind') { $rc=Invoke-LocalBind $op $outFile $errFile }
        elseif (-not (Test-Path -LiteralPath $op.Cwd -PathType Container)) {
            Write-TextFile $outFile ''; Write-TextFile $errFile ('cwd_absent path=' + $op.Cwd); $rc=3
        } elseif (Test-ReparsePoint $op.Cwd) {
            Write-TextFile $outFile ''; Write-TextFile $errFile ('cwd_is_reparse_point path=' + $op.Cwd); $rc=3
        } else { $rc=Invoke-ExternalProcess $op $outFile $errFile }
    } catch {
        if (-not (Test-Path -LiteralPath $outFile)) { Write-TextFile $outFile '' }
        Write-TextFile $errFile ('operation_exception detail=' + $_.Exception.GetType().FullName)
        $rc=3
    }
    Write-TextFile $rcFile ([string]$rc)
    Write-TextFile $elapsedFile ([string]$script:LastElapsedMs)
    if ($script:LastStdinState -eq 'incomplete') { Emit ('TR_OP_STDIN id=' + $op.Id + ' state=incomplete detail=child_closed_input_before_all_bytes_were_written') }
    try { $outSha=Get-Sha256 $outFile; $errSha=Get-Sha256 $errFile } catch { Stop-Run ('capture_hash_failed op=' + $op.Id) }
    Emit ('TR_OP_END id=' + $op.Id + ' rc=' + $rc + ' expect_rc=' + $op.ExpectRc + ' elapsed_ms=' + $script:LastElapsedMs + ' stdout_sha256=' + $outSha + ' stderr_sha256=' + $errSha)
    [void]$results.Add(@{Id=$op.Id;Rc=$rc;Expect=$op.ExpectRc;Elapsed=$script:LastElapsedMs})

    # Classification is by operation kind and provenance, never by the integer
    # alone (Codex R2 F1 / Claude R2 F1).
    $outcome = Get-OpOutcomeClass $op $rc $outFile $errFile $prerequisiteEstablished
    Emit ('TR_OP_CLASS id=' + $op.Id + ' kind=' + $op.Kind + ' rc=' + $rc + ' expect_rc=' + $op.ExpectRc + ' class=' + $outcome.Class + ' reason=' + $outcome.Reason)
    if ($outcome.Class -ne 'match') {
        if ($firstMismatch -eq '') { $firstMismatch=$op.Id; $sequenceOk=$false; Emit ('TR_FIRST_MISMATCH id=' + $op.Id + ' rc=' + $rc + ' expected=' + $op.ExpectRc + ' class=' + $outcome.Class + ' later_sequence_ops=skip always_ops=run') }
        else { Emit ('TR_ADDITIONAL_MISMATCH id=' + $op.Id + ' first_mismatch=' + $firstMismatch) }
        if ($outcome.Class -eq 'not_evaluable') {
            $anyNotEvaluable=$true; $notEvaluableCount++
            if ($firstNotEvaluable -eq '') { $firstNotEvaluable=$op.Id }
            Emit ('TR_OP_NOT_EVALUABLE id=' + $op.Id + ' rc=' + $rc + ' expected=' + $op.ExpectRc + ' reason=' + $outcome.Reason)
        } else {
            $anyDeviant=$true; $deviantCount++
            Emit ('TR_OP_DEVIANT id=' + $op.Id + ' rc=' + $rc + ' expected=' + $op.ExpectRc + ' reason=' + $outcome.Reason)
        }
    }
}

foreach ($result in $results) { Emit ('TR_RESULT id=' + $result.Id + ' rc=' + $result.Rc + ' expect_rc=' + $result.Expect + ' elapsed_ms=' + $result.Elapsed) }
Emit ('TR_RUN_CLASS deviant=' + $deviantCount + ' not_evaluable=' + $notEvaluableCount + ' precedence=deviant_outranks_not_evaluable')

$exitCode = 0
if ($anyDeviant) {
    Emit ('TR_RUN FAIL base_run=' + $BASE_RUN + ' first_mismatch=' + $firstMismatch + ' first_not_evaluable=' + $firstNotEvaluable + ' record=' + $RECORD_ROOT)
    $exitCode = 1
} elseif ($anyNotEvaluable) {
    Emit ('TR_RUN STOP base_run=' + $BASE_RUN + ' first_mismatch=' + $firstMismatch + ' first_not_evaluable=' + $firstNotEvaluable + ' record=' + $RECORD_ROOT)
    $exitCode = 3
} else {
    Emit ('TR_RUN PASS base_run=' + $BASE_RUN + ' record=' + $RECORD_ROOT)
    $exitCode = 0
}

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

exit $exitCode
