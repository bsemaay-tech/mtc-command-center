# Open-BridgeDashboard.ps1 - one-click owner access to the KVM2 Bridge dashboard.
#
# What it does: opens a pinned SSH tunnel from this Windows PC to the Bridge's
# loopback-only listener on KVM2 (127.0.0.1:8790), verifies the dashboard
# answers through the tunnel, then opens it in the default browser. Closing
# this window closes the tunnel.
#
# Security contract (owner requirement 2026-08-16):
#   - Stores NO password and NO key passphrase. Authentication comes ONLY from
#     the already-loaded Windows ssh-agent (the owner runs ssh-add themselves).
#   - Strict host-key checking against the pinned known_hosts entry; a changed
#     host key is a hard failure, never auto-accepted.
#   - Fails with a clear message if the agent, authentication, port forward,
#     or local port is not usable.
#   - Contacts ONLY the pinned host below over SSH. No other network action.
#
# T0 note: this file is host-contacting and is audited with the deployment
# package (KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md).

$ErrorActionPreference = 'Stop'

# --- pinned configuration (no secrets) ---------------------------------------
$SshExe      = 'C:\Windows\System32\OpenSSH\ssh.exe'
$HostAddr    = '152.239.123.231'          # srv1856225 (Hostinger KVM2)
$HostUser    = 'baris'
$KnownHosts  = Join-Path $env:USERPROFILE '.ssh\known_hosts'
$LocalPort   = 18790                      # local end of the tunnel
$RemoteLoop  = '127.0.0.1:8790'           # Bridge loopback listener on KVM2
$DashboardUrl = "http://127.0.0.1:$LocalPort/"

function Fail([string]$Message) {
    Write-Host ''
    Write-Host "PROBLEM: $Message" -ForegroundColor Red
    Write-Host 'The dashboard was NOT opened. Nothing was changed anywhere.'
    Read-Host 'Press Enter to close'
    exit 1
}

# --- preflight ---------------------------------------------------------------
if (-not (Test-Path -LiteralPath $SshExe)) { Fail "Windows OpenSSH not found at $SshExe." }
if (-not (Test-Path -LiteralPath $KnownHosts)) { Fail "known_hosts not found at $KnownHosts - the host key pin is missing." }

# ssh-agent must be running and must hold at least one identity.
$agent = Get-Service ssh-agent -ErrorAction SilentlyContinue
if ($null -eq $agent -or $agent.Status -ne 'Running') {
    Fail 'The Windows ssh-agent service is not running. Start it and load the key: Start-Service ssh-agent; ssh-add $env:USERPROFILE\.ssh\hostinger_kvm2'
}
& $SshExe -o BatchMode=yes 2>$null | Out-Null   # no-op warmup; ignore
$agentList = & 'C:\Windows\System32\OpenSSH\ssh-add.exe' -l 2>&1
if ($LASTEXITCODE -ne 0) {
    Fail 'No key is loaded in ssh-agent. Load it yourself (the passphrase is typed only into the ssh-add prompt): ssh-add $env:USERPROFILE\.ssh\hostinger_kvm2'
}

# Local port must be free.
$portBusy = Get-NetTCPConnection -LocalPort $LocalPort -State Listen -ErrorAction SilentlyContinue
if ($portBusy) { Fail "Local port $LocalPort is already in use. Close the other program or an older tunnel window first." }

# --- open the tunnel ---------------------------------------------------------
Write-Host "Opening SSH tunnel  127.0.0.1:$LocalPort  ->  KVM2 $RemoteLoop ..." -ForegroundColor Cyan
$sshArgs = @(
    '-N',
    '-L', "127.0.0.1:${LocalPort}:${RemoteLoop}",
    '-o', 'BatchMode=yes',
    '-o', 'StrictHostKeyChecking=yes',
    '-o', "UserKnownHostsFile=$KnownHosts",
    '-o', 'ExitOnForwardFailure=yes',
    '-o', 'ConnectTimeout=10',
    "$HostUser@$HostAddr"
)
$tunnel = Start-Process -FilePath $SshExe -ArgumentList $sshArgs -NoNewWindow -PassThru

# Give it a moment, then check it did not die (bad auth / forward failure exits fast).
Start-Sleep -Seconds 3
if ($tunnel.HasExited) {
    Fail "The SSH tunnel exited immediately (code $($tunnel.ExitCode)). Usual causes: key not loaded in ssh-agent, changed host key (STOP - report it), or the forward was refused."
}

# --- verify the dashboard answers through the tunnel -------------------------
$ok = $false
for ($i = 0; $i -lt 5 -and -not $ok; $i++) {
    try {
        $resp = Invoke-WebRequest -Uri $DashboardUrl -UseBasicParsing -TimeoutSec 5
        if ($resp.StatusCode -eq 200) { $ok = $true }
    } catch { Start-Sleep -Seconds 2 }
}
if (-not $ok) {
    try { Stop-Process -Id $tunnel.Id -Force -ErrorAction SilentlyContinue } catch {}
    Fail "The tunnel is up but the dashboard did not answer at $DashboardUrl. Usual cause: the Bridge service is not running on KVM2 (it starts only under a separate owner authorization)."
}

# --- open the browser --------------------------------------------------------
Write-Host "Dashboard is answering. Opening $DashboardUrl" -ForegroundColor Green
Start-Process $DashboardUrl
Write-Host ''
Write-Host 'Tunnel is ACTIVE. Keep this window open while using the dashboard.'
Write-Host 'Close this window (or press Ctrl+C) to close the tunnel.'
Wait-Process -Id $tunnel.Id
