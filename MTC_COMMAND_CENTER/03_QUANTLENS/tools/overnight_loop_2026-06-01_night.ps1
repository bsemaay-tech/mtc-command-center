# overnight_loop_2026-06-01_night.ps1
# Overnight multi-iter sprint — iter 4+ (devam).
# 20 worker, OUTPUT_DIR env override, crash-safe checkpoint.
# Calisma suresi: launch'tan sabah 06:00'a kadar.

Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Definition)

$env:MEGA_WORKERS = "20"
$env:MEGA_OUTPUT_DIR = "C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS"

$Deadline = (Get-Date).Date.AddDays(1).AddHours(6)   # yarin 06:00
if ((Get-Date) -gt $Deadline) {
    $Deadline = (Get-Date).AddHours(8)  # eger coktan gectiyse 8 saat
}

New-Item -ItemType Directory -Force -Path "overnight_runs" | Out-Null
New-Item -ItemType Directory -Force -Path "sprint_runs"    | Out-Null

$LoopLog    = "overnight_runs/night_loop_2026-06-01.log"
$Heartbeat  = "overnight_runs/_heartbeat_night.json"

$Iter         = 0
$TotalPasses  = 0
$TotalCrashes = 0

function Write-Heartbeat($ExitCode) {
    $ts = (Get-Date -Format "o")
    @"
{
  "ts": "$ts",
  "mode": "night_20w",
  "iter": $Iter,
  "passes": $TotalPasses,
  "crashes": $TotalCrashes,
  "deadline": "$Deadline",
  "last_exit_code": $ExitCode
}
"@ | Set-Content -Encoding utf8 $Heartbeat
}

$msg = "[night] === LAUNCHED at $(Get-Date) | deadline=$Deadline | workers=$env:MEGA_WORKERS ==="
$msg | Tee-Object -FilePath $LoopLog -Append
Write-Heartbeat "null"

while ((Get-Date) -lt $Deadline) {
    $Iter++
    $ts  = (Get-Date -Format "yyyyMMdd_HHmmss")
    $Log = "sprint_runs/v2_night_iter_${Iter}_${ts}.log"

    $env:MEGA_HEARTBEAT_PATH     = $Heartbeat
    $env:MEGA_HEARTBEAT_MODE     = "night_20w"
    $env:MEGA_HEARTBEAT_ITER     = "$Iter"
    $env:MEGA_HEARTBEAT_PASSES   = "$TotalPasses"
    $env:MEGA_HEARTBEAT_CRASHES  = "$TotalCrashes"

    "[night] === Iter $Iter start at $(Get-Date) ===" | Tee-Object -FilePath $LoopLog -Append

    python overnight_v2_runner.py 2>&1 | Tee-Object -FilePath $Log
    $EC = $LASTEXITCODE

    "[night] Iter $Iter exit=$EC at $(Get-Date)" | Tee-Object -FilePath $LoopLog -Append

    if ($EC -ne 0) {
        $TotalCrashes++
        "[night] CRASH (EC=$EC). Son satirlar:" | Tee-Object -FilePath $LoopLog -Append
        Get-Content $Log -Tail 15 | Tee-Object -FilePath $LoopLog -Append
        Write-Heartbeat $EC
        Start-Sleep -Seconds 5
        continue
    }

    $Content = Get-Content $Log -Raw
    if ($Content -match "all jobs done") {
        $TotalPasses++
        $SrcJson = "$env:MEGA_OUTPUT_DIR/MEGA_walk_forward_results.json"
        $SrcMd   = "$env:MEGA_OUTPUT_DIR/MEGA_walk_forward_report.md"
        if (Test-Path $SrcJson) {
            Copy-Item $SrcJson "sprint_runs/MEGA_results_iter_${Iter}_${ts}.json"
        }
        if (Test-Path $SrcMd) {
            Copy-Item $SrcMd  "sprint_runs/MEGA_report_iter_${Iter}_${ts}.md"
        }
    }

    "[night] passes=$TotalPasses crashes=$TotalCrashes" | Tee-Object -FilePath $LoopLog -Append
    Write-Heartbeat $EC
    Start-Sleep -Seconds 2
}

$final = "[night] === DEADLINE at $(Get-Date). passes=$TotalPasses crashes=$TotalCrashes ==="
$final | Tee-Object -FilePath $LoopLog -Append
Write-Heartbeat "done"
