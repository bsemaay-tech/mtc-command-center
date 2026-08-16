# Open-BridgeDashboard_v3.ps1 - pinned, agent-only KVM2 dashboard tunnel.
#
# Stores no password, passphrase, or private-key material. No identity key file
# is opened: the pinned expected fingerprint must already be present in the
# Windows ssh-agent. Closing this window or pressing Ctrl+C closes the tunnel.

$ErrorActionPreference = 'Stop'

$SshExe              = 'C:\Windows\System32\OpenSSH\ssh.exe'
$SshAddExe           = 'C:\Windows\System32\OpenSSH\ssh-add.exe'
$SshKeygenExe        = 'C:\Windows\System32\OpenSSH\ssh-keygen.exe'
$HostAddr            = '152.239.123.231'
$HostUser            = 'baris'
$KnownHosts          = Join-Path $env:USERPROFILE '.ssh\known_hosts'
$ExpectedFingerprint = 'SHA256:8b6bl/srDevzQ1rycf9FcQFgZXblSMddqak/9JsHBC8'
$LocalPort           = 18790
$RemoteLoop          = '127.0.0.1:8790'
$DashboardUrl        = "http://127.0.0.1:$LocalPort/"

function Fail([string]$Message) {
    Write-Host ''
    Write-Host "PROBLEM: $Message" -ForegroundColor Red
    Write-Host 'The dashboard was NOT opened. No password, passphrase, or private key was read.'
    Read-Host 'Press Enter to close'
    exit 1
}

function Invoke-NativeCapture {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    $previousEap = $ErrorActionPreference
    $output = @()
    $exitCode = -1
    try {
        # Windows PowerShell 5.1 turns native stderr into ErrorRecords. Native
        # calls therefore run under Continue, and the real rc is captured from
        # LASTEXITCODE before the caller makes any decision.
        $ErrorActionPreference = 'Continue'
        $output = @(& $FilePath @Arguments 2>&1)
        $exitCode = $LASTEXITCODE
    }
    catch {
        $output = @($_.Exception.Message)
    }
    finally {
        $ErrorActionPreference = $previousEap
    }
    [pscustomobject]@{
        ExitCode = $exitCode
        Output = @($output | ForEach-Object { $_.ToString() })
    }
}

function Get-Sha256Fingerprints([string[]]$Lines) {
    @(
        $Lines | ForEach-Object {
            [regex]::Matches($_, 'SHA256:[A-Za-z0-9+/=]+') | ForEach-Object { $_.Value }
        } | Select-Object -Unique
    )
}

function Get-SshExitMessage([System.Diagnostics.Process]$Process) {
    $Process.Refresh()
    $code = $Process.ExitCode
    $likely = switch ($code) {
        255 { 'authentication, pinned host-key, connection, or SSH forwarding failure; read the SSH line above. If it mentions a host key, STOP and report it' }
        1   { 'local SSH option or forwarding setup failure' }
        default { 'connection or forwarding failure; read the SSH line above for the exact class' }
    }
    "The SSH tunnel exited early with real exit code $code. Likely class: $likely."
}

function Test-DashboardReady([string]$Uri) {
    $response = $null
    $reader = $null
    try {
        $request = [System.Net.HttpWebRequest]::Create($Uri)
        $request.Proxy = $null
        $request.AllowAutoRedirect = $false
        $request.Timeout = 1500
        $request.ReadWriteTimeout = 1500
        $response = [System.Net.HttpWebResponse]$request.GetResponse()
        if ([int]$response.StatusCode -ne 200) { return $false }
        $reader = New-Object System.IO.StreamReader($response.GetResponseStream())
        return $reader.ReadToEnd().Contains('<title>Crypto Paper Bridge</title>')
    }
    catch {
        return $false
    }
    finally {
        if ($null -ne $reader) { $reader.Dispose() }
        if ($null -ne $response) { $response.Dispose() }
    }
}

foreach ($binary in ($SshExe, $SshAddExe, $SshKeygenExe)) {
    if (-not (Test-Path -LiteralPath $binary -PathType Leaf)) {
        Fail "Required Windows OpenSSH program not found: $binary"
    }
}
if (-not (Test-Path -LiteralPath $KnownHosts -PathType Leaf)) {
    Fail "Pinned known_hosts file not found at $KnownHosts. STOP and report; do not accept a new key."
}

$agent = Get-Service ssh-agent -ErrorAction SilentlyContinue
if ($null -eq $agent -or $agent.Status -ne 'Running') {
    Fail 'The Windows ssh-agent service is not running. Start it, then load hostinger_kvm2 yourself with ssh-add.'
}

$agentResult = Invoke-NativeCapture -FilePath $SshAddExe -Arguments @('-l', '-E', 'sha256')
if ($agentResult.ExitCode -eq 2) {
    Fail 'The ssh-agent service is running but its agent socket cannot be reached. Restart ssh-agent, reload the key, and retry.'
}
if ($agentResult.ExitCode -eq 1) {
    Fail 'The ssh-agent is reachable but has no identities. Load hostinger_kvm2 yourself with ssh-add, then retry.'
}
if ($agentResult.ExitCode -ne 0) {
    Fail "ssh-add could not list identities (exit code $($agentResult.ExitCode)). STOP and report."
}

$pinResult = Invoke-NativeCapture -FilePath $SshKeygenExe -Arguments @('-F', $HostAddr, '-f', $KnownHosts)
if ($pinResult.ExitCode -ne 0) {
    Fail "No pinned host key for $HostAddr exists in $KnownHosts. STOP and report; never accept a new key here."
}

$agentFingerprints = Get-Sha256Fingerprints -Lines $agentResult.Output
if ($agentFingerprints -notcontains $ExpectedFingerprint) {
    Fail "The expected public-key fingerprint $ExpectedFingerprint is not loaded in ssh-agent. Load that key yourself and retry."
}

$portBusy = Get-NetTCPConnection -LocalPort $LocalPort -State Listen -ErrorAction SilentlyContinue
if ($portBusy) {
    Fail "Local port $LocalPort is already in use. Close the other program or older tunnel window first."
}

# Windows OpenSSH parses this option set with `ssh -G -F NUL` without opening a
# connection. On Windows, NUL is the null device. `-F NUL` suppresses user and
# system ssh_config; the explicit NUL IdentityFile removes file identities while
# the default Windows agent remains available. `IdentitiesOnly no` is deliberate:
# authentication is agent-based, SSH may offer other loaded agent keys, and the
# server can accept only keys already present in its authorized_keys. `none` is
# the documented disable value for ProxyCommand/ProxyJump. The two known-host
# options isolate trust to the named pin file. Quoting preserves a USERPROFILE
# path containing spaces.
$knownHostsOption = 'UserKnownHostsFile="' + $KnownHosts + '"'
$sshArgs = @(
    '-F', 'NUL',
    '-N',
    '-L', "127.0.0.1:${LocalPort}:${RemoteLoop}",
    '-o', 'IdentityFile=NUL',
    '-o', 'ProxyCommand=none',
    '-o', 'ProxyJump=none',
    '-o', 'GlobalKnownHostsFile=NUL',
    '-o', $knownHostsOption,
    '-o', 'PasswordAuthentication=no',
    '-o', 'KbdInteractiveAuthentication=no',
    '-o', 'BatchMode=yes',
    '-o', 'StrictHostKeyChecking=yes',
    '-o', 'ExitOnForwardFailure=yes',
    '-o', 'ConnectTimeout=10',
    "$HostUser@$HostAddr"
)

Write-Host "Opening SSH tunnel 127.0.0.1:$LocalPort -> KVM2 $RemoteLoop ..." -ForegroundColor Cyan
$tunnel = $null
$failure = $null
try {
    try {
        $tunnel = Start-Process -FilePath $SshExe -ArgumentList $sshArgs -NoNewWindow -PassThru -ErrorAction Stop
    }
    catch {
        throw "Windows could not start ssh.exe: $($_.Exception.Message)"
    }

    $ready = $false
    for ($attempt = 1; $attempt -le 10 -and -not $ready; $attempt++) {
        $tunnel.Refresh()
        if ($tunnel.HasExited) { throw (Get-SshExitMessage -Process $tunnel) }
        $ready = Test-DashboardReady -Uri $DashboardUrl
        $tunnel.Refresh()
        if ($tunnel.HasExited) { throw (Get-SshExitMessage -Process $tunnel) }
        if (-not $ready) { Start-Sleep -Seconds 1 }
    }
    if (-not $ready) {
        throw "The SSH child is still running, but the dashboard did not return HTTP 200 with the expected Bridge page at $DashboardUrl. The Bridge service may not be running."
    }

    Write-Host "Dashboard is answering. Opening $DashboardUrl" -ForegroundColor Green
    try {
        Start-Process -FilePath $DashboardUrl -ErrorAction Stop | Out-Null
    }
    catch {
        throw "The dashboard answered, but Windows could not open the browser: $($_.Exception.Message)"
    }
    Write-Host ''
    Write-Host 'Tunnel is ACTIVE. Keep this window open while using the dashboard.'
    Write-Host 'Close this window or press Ctrl+C to close the tunnel.'
    Wait-Process -Id $tunnel.Id -ErrorAction Stop
    $tunnel.Refresh()
    if ($tunnel.ExitCode -ne 0) { throw (Get-SshExitMessage -Process $tunnel) }
}
catch {
    $failure = $_.Exception.Message
}
finally {
    if ($null -ne $tunnel) {
        $tunnel.Refresh()
        if (-not $tunnel.HasExited) {
            Stop-Process -Id $tunnel.Id -Force -ErrorAction SilentlyContinue
            Wait-Process -Id $tunnel.Id -ErrorAction SilentlyContinue
        }
    }
}

if ($failure) { Fail $failure }
