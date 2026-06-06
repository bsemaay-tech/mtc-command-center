# monitor_overnight.ps1
# Yarinki gece calismasi icin harici saglik kontrolu.
# taskschd her 30dk firar — bagimsiz kanal (wakeup zincirinden ayri).

$ErrorActionPreference = "Continue"
$root      = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$runs      = Join-Path $root "overnight_runs"
$heartbeat = Join-Path $runs "_heartbeat.json"
$alertLog  = Join-Path $runs "_external_monitor.log"

function Write-Alert([string]$msg) {
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Add-Content -Path $alertLog -Value "[$ts] $msg" -Encoding UTF8
    # Balloon notification (taskbar)
    Add-Type -AssemblyName System.Windows.Forms
    $balloon = New-Object System.Windows.Forms.NotifyIcon
    $balloon.Icon = [System.Drawing.SystemIcons]::Warning
    $balloon.BalloonTipTitle = "MCC Overnight Monitor"
    $balloon.BalloonTipText  = $msg
    $balloon.Visible = $true
    $balloon.ShowBalloonTip(10000)
    Start-Sleep -Seconds 2
    $balloon.Dispose()
}

function Write-Info([string]$msg) {
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Add-Content -Path $alertLog -Value "[$ts] INFO $msg" -Encoding UTF8
}

# Check 1: heartbeat exists + fresh (< 60dk)
if (-not (Test-Path $heartbeat)) {
    Write-Alert "heartbeat dosyasi yok: $heartbeat"
    exit 1
}
$hbAge = ((Get-Date) - (Get-Item $heartbeat).LastWriteTime).TotalMinutes
if ($hbAge -gt 60) {
    Write-Alert "heartbeat $([int]$hbAge)dk eski — loop muhtemelen oldu"
    exit 1
}

# Check 2: heartbeat content parse
try {
    $hb = Get-Content $heartbeat -Raw | ConvertFrom-Json
} catch {
    Write-Alert "heartbeat JSON parse hatasi: $_"
    exit 1
}

# Check 3: 3+ ardisik crash, 0 pass -> structural issue
if ($hb.crashes -ge 3 -and $hb.passes -eq 0) {
    Write-Alert "$($hb.crashes) crash, 0 pass — yapisal sorun olabilir (iter=$($hb.iter))"
    exit 1
}

# Check 4: disk doluluk %90+ (sadece C: surucu)
$disk = Get-PSDrive C
$diskPct = [math]::Round(($disk.Used / ($disk.Used + $disk.Free)) * 100, 1)
if ($diskPct -gt 90) {
    Write-Alert "disk doluluk $diskPct% — overnight backtest hata verir"
    exit 1
}

# Check 5: deadline gecmis mi
$now = [int][double]::Parse((Get-Date -UFormat %s))
if ($hb.deadline_ts -lt $now) {
    Write-Info "deadline gecti (iter=$($hb.iter) passes=$($hb.passes) crashes=$($hb.crashes)) — loop normal sona ermis"
    exit 0
}

# Tum kontroller temiz
Write-Info "OK iter=$($hb.iter) passes=$($hb.passes) crashes=$($hb.crashes) hb_age=$([int]$hbAge)dk disk=$diskPct%"
exit 0
