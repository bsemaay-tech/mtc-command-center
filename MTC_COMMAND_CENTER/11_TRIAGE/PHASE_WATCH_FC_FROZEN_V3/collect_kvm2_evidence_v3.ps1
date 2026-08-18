# collect_kvm2_evidence_v3.ps1 — FROZEN V3 CLIENT. Replaces the live collector at
# APPLICATION time only (after provisioning + T/B/W acceptance); until then the
# live client keeps using the baris route. Changes vs the reviewed round-1 client:
#   * account: mtc-watch (dedicated, forced-command, restrict)
#   * only check IDs cross the wire — the frozen client table is the redundant
#     second allowlist; the server menu is the enforced first
#   * -BackupDir removed: check4 reads the root-owned status.json via the server
#     menu; the client cannot influence any path
# Everything else (modes, refusals, sanitizer, atomic evidence dir, COMPLETE
# marker, fail-closed exits) matches the reviewed round-1 client behavior.
param([switch]$Live, [string]$FixtureDir = '')
$ErrorActionPreference = 'Stop'
$SshExe              = 'C:\Windows\System32\OpenSSH\ssh.exe'
$SshAddExe           = 'C:\Windows\System32\OpenSSH\ssh-add.exe'
$HostAddr            = '152.239.123.231'
$HostUser            = 'mtc-watch'
$KnownHosts          = Join-Path $env:USERPROFILE '.ssh\known_hosts'
$ExpectedFingerprint = 'PASTE-MTC-WATCH-KEY-FINGERPRINT-AT-APPLICATION'
$PerCommandTimeoutS  = 60
$EvidenceRoot        = 'C:\LAB\HERMES_WATCH\evidence'
$FixtureRoot         = 'C:\LAB\HERMES_WATCH'
$MaxBytesPerCheck    = 20480
# FROZEN table: IDs only. Server menu (mtc-watch-collect) is authoritative.
$Checks = @(
    @{ N=1; Name='service-alive';  Id='check1' },
    @{ N=2; Name='disarmed-mode';  Id='check2' },
    @{ N=3; Name='logs-rotating';  Id='check3' },
    @{ N=4; Name='backup-bundle';  Id='check4' },
    @{ N=5; Name='memory-disk';    Id='check5' },
    @{ N=6; Name='error-scan';     Id='check6' },
    @{ N=7; Name='dashboard';      Id='' }        # manual launcher, never run here
)
if (-not $Live -and -not $FixtureDir) { Write-Host 'Refusing: pass -Live or -FixtureDir.'; exit 2 }
if ($Live -and $FixtureDir) { Write-Host 'Refusing: modes mutually exclusive.'; exit 2 }
function Test-IsReparse([string]$p) { try { return [bool]((Get-Item -LiteralPath $p -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) } catch { return $true } }
if ($FixtureDir) {
    if ($FixtureDir -like '\\*') { Write-Host 'Refusing: UNC fixture path.'; exit 2 }
    if (-not (Test-Path -LiteralPath $FixtureDir -PathType Container)) { Write-Host 'Refusing: fixture dir invalid.'; exit 2 }
    $full = (Resolve-Path -LiteralPath $FixtureDir).Path
    if ($full -notlike "$FixtureRoot*") { Write-Host "Refusing: fixtures must live under $FixtureRoot."; exit 2 }
    if (Test-IsReparse $full) { Write-Host 'Refusing: fixture dir is a reparse point.'; exit 2 }
}
function Sanitize([string]$text, [ref]$redactions) {
    $pats = @(
        '(?i)(secret|token|passw|private[_ ]?key|api[_-]?key)',
        '(?i)\bauthorization\b|\bbearer\b|\bcookie\b|set-cookie',
        'eyJ[A-Za-z0-9_-]{10,}',
        '-----BEGIN [A-Z ]+-----',
        '[A-Za-z0-9+/]{60,}={0,2}',
        '[a-z][a-z0-9+.\-]*://[^/\s:@]+:[^/\s@]+@'
    )
    $lines = $text -split "`r?`n"
    $out = foreach ($ln in $lines) {
        $hit = $false; foreach ($p in $pats) { if ($ln -match $p) { $hit = $true; break } }
        if ($hit) { $redactions.Value++; '[REDACTED LINE]' }
        elseif ($ln -match '[0-9a-fA-F]{32,}') { $redactions.Value++; ($ln -replace '[0-9a-fA-F]{32,}','[REDACTED-HEX]') }
        else { $ln }
    }
    $joined = $out -join "`n"
    $bytes = [Text.Encoding]::UTF8.GetBytes($joined)
    if ($bytes.Length -gt $MaxBytesPerCheck) {
        $joined = [Text.Encoding]::UTF8.GetString($bytes[0..($MaxBytesPerCheck-1)]) + "`n...(capped)"
    }
    return $joined
}
if ($Live) {
    $agentRows = & $SshAddExe -l 2>&1
    if ($LASTEXITCODE -ne 0 -or -not ($agentRows | Where-Object { $_ -match [regex]::Escape($ExpectedFingerprint) })) {
        Write-Host 'BLOCKER: mtc-watch key fingerprint not in ssh-agent. Nothing run.'; exit 3
    }
}
if (-not (Test-Path -LiteralPath $EvidenceRoot)) { New-Item -ItemType Directory -Force $EvidenceRoot | Out-Null }
if (Test-IsReparse $EvidenceRoot) { Write-Host 'Refusing: evidence root is a reparse point.'; exit 4 }
$stampUtc = (Get-Date).ToUniversalTime().ToString('yyyyMMdd_HHmmss') + 'Z_' + ([guid]::NewGuid().ToString('N').Substring(0,8))
$runDir = Join-Path $EvidenceRoot $stampUtc
try { $null = New-Item -ItemType Directory -Path $runDir -ErrorAction Stop } catch { Write-Host 'Refusing: run dir exists.'; exit 4 }
function Invoke-SshId([string]$checkId) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $SshExe
    $psi.UseShellExecute = $false; $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true; $psi.CreateNoWindow = $true
    foreach ($a in @('-F','NUL','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',"-o","UserKnownHostsFile=$KnownHosts",'-o','IdentitiesOnly=yes','-o','ClearAllForwardings=yes','-o','PermitLocalCommand=no','-o','ForwardAgent=no','-o','ConnectTimeout=15',"$HostUser@$HostAddr",$checkId)) { $psi.ArgumentList.Add($a) }
    $p = [System.Diagnostics.Process]::Start($psi)
    $so = $p.StandardOutput.ReadToEndAsync(); $se = $p.StandardError.ReadToEndAsync()
    if (-not $p.WaitForExit($PerCommandTimeoutS*1000)) { try { $p.Kill() } catch {}; return @{ Exit=-1; Out='(timeout)' } }
    $err = if ($se.Result) { "`n--- stderr ---`n" + $se.Result } else { '' }
    return @{ Exit=$p.ExitCode; Out=($so.Result + $err) }
}
$manifest = @(); $anyError = $false
foreach ($c in $Checks) {
    $name = "check$($c.N)_$($c.Name)"; $file = Join-Path $runDir "$name.txt"
    $entry = @{ n=$c.N; name=$c.Name; status=''; exit=$null; duration_ms=0; bytes_kept=0; redactions=0; command=$c.Id }
    if ($c.N -eq 7) {
        $entry.status='SKIPPED-MANUAL'
        Set-Content $file 'SKIPPED-MANUAL: dashboard via the audited launcher (manual owner/Lead action).'
    } else {
        $sw=[Diagnostics.Stopwatch]::StartNew(); $raw=''; $exit=$null
        if ($FixtureDir) {
            $fix = Join-Path $FixtureDir "$name.txt"
            if (Test-Path -LiteralPath $fix -PathType Leaf) { $raw = Get-Content -LiteralPath $fix -Raw; $exit=0 } else { $raw='(fixture missing)'; $exit=1 }
        } else { $r = Invoke-SshId $c.Id; $raw = $r.Out; $exit = $r.Exit }
        $sw.Stop(); $red=0; $clean = Sanitize $raw ([ref]$red)
        Set-Content -LiteralPath $file -Value $clean -Encoding utf8
        if ($exit -eq 0 -and $raw.Trim()) { $entry.status='COLLECTED' } elseif ($exit -eq 0) { $entry.status='EMPTY'; $anyError=$true } else { $entry.status='ERROR'; $anyError=$true }
        $entry.exit=$exit; $entry.duration_ms=$sw.ElapsedMilliseconds; $entry.bytes_kept=(Get-Item -LiteralPath $file).Length; $entry.redactions=$red
    }
    $manifest += [pscustomobject]$entry
}
$mode = if ($Live) { 'LIVE' } else { 'FIXTURE' }
[pscustomobject]@{ run_utc=$stampUtc; mode=$mode; host="KVM2 ($HostAddr)"; user=$HostUser; checks=$manifest } | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $runDir 'manifest.json') -Encoding utf8
Set-Content (Join-Path $runDir 'COMPLETE') 'ok' -Encoding ascii
"Evidence written: $runDir (mode=$mode)"
$manifest | ForEach-Object { "  check$($_.n) $($_.name): $($_.status)" }
if ($anyError) { exit 5 }
exit 0
