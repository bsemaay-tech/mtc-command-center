# Gate A - A-8 host reachability probe (WINDOWS host side) (run-kit D, 2026-08-08)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED)
#
# AUTHORIZED ONLY FOR THE OWNER-APPROVED PREREGISTERED GATE A RERUN.
# Bounded TcpClient.ConnectAsync probes from the Windows host against the staging VM.
# Port 22 MUST succeed (reachability control); port 8790 MUST fail (binding is loopback
# only on the VM, so it is not reachable from the host). Prints booleans/errors only.
# Refuses to overwrite an existing evidence log.
#
# A-8 PASS requires BOTH: this host script (port22_ok=true AND port8790_ok=false) AND the
# remote gatea_A8.sh ending `A-8 PASS`. Neither alone passes the gate.
$ErrorActionPreference = 'Stop'

$vm = '172.24.55.233'
$log = 'C:\WPI_ARTIFACTS\gatea-A8-host-20260808D.log'
$timeoutMs = 3000

if (Test-Path -LiteralPath $log) {
    [Console]::Error.WriteLine("ERROR: evidence log already exists: $log; refusing to overwrite")
    exit 2
}

function Test-Port {
    param([string]$HostName, [int]$Port, [int]$TimeoutMs)
    $client = $null
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $task = $client.ConnectAsync($HostName, $Port)
        $completed = $task.Wait($TimeoutMs)
        if (-not $completed) {
            return @{ ok = $false; err = "timeout_${TimeoutMs}ms" }
        }
        if ($task.IsFaulted) {
            $msg = ""
            if ($task.Exception -ne $null -and $task.Exception.InnerException -ne $null) {
                $msg = $task.Exception.InnerException.Message
            } elseif ($task.Exception -ne $null) {
                $msg = $task.Exception.Message
            }
            return @{ ok = $false; err = $msg }
        }
        return @{ ok = [bool]$client.Connected; err = "" }
    } catch {
        return @{ ok = $false; err = $_.Exception.Message }
    } finally {
        if ($client -ne $null) { $client.Dispose() }
    }
}

$r22   = Test-Port -HostName $vm -Port 22   -TimeoutMs $timeoutMs
$r8790 = Test-Port -HostName $vm -Port 8790 -TimeoutMs $timeoutMs

$port22_ok   = [bool]$r22.ok
$port8790_ok = [bool]$r8790.ok
$host_probe_ok = ($port22_ok -and (-not $port8790_ok))

$boolLines = @(
    "port22_ok=$port22_ok",
    "port22_err=$($r22.err)",
    "port8790_ok=$port8790_ok",
    "port8790_err=$($r8790.err)",
    "host_probe_ok=$host_probe_ok"
)

$logLines = @(
    "host_vm_ip=$vm",
    "host_probe_timeout_ms=$timeoutMs",
    "host_candidate=2ce41e34bceb599d80af24c5c33d835820ec321b"
) + $boolLines + @(
    "host_note=port22 must be true (reachability control); port8790 must be false; A-8 gate PASS requires remote A-8 PASS too"
)

# Evidence log: UTF-8, no BOM, LF line endings.
$payload = ($logLines -join "`n") + "`n"
[System.IO.File]::WriteAllText($log, $payload, (New-Object System.Text.UTF8Encoding($false)))

# stdout: booleans/errors only.
$boolLines | ForEach-Object { Write-Output $_ }

# Verdict (host side of A-8): nonzero unless port 22 is reachable AND port 8790 is
# NOT reachable. Without this the script always exited 0 even on probe failure.
if (-not $host_probe_ok) {
    Write-Output "A8_HOST_FAIL"
    exit 1
}
Write-Output "A8_HOST_PASS"
exit 0
