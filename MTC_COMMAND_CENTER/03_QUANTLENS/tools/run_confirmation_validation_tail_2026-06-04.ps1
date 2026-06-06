$ErrorActionPreference = "Stop"

$tools = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$results = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\confirm_2026-06-04"
$runs = Join-Path $tools "night_runs\confirm_2026-06-04"
$log = Join-Path $tools "overnight_runs\confirm_validation_tail_2026-06-04.log"
$heartbeat = Join-Path $tools "overnight_runs\_heartbeat_confirm_validation_tail.json"
$done = Join-Path $tools "overnight_runs\confirm_validation_tail_2026-06-04.DONE"
$failed = Join-Path $tools "overnight_runs\confirm_validation_tail_2026-06-04.FAILED"

New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
New-Item -ItemType Directory -Force -Path $results | Out-Null
New-Item -ItemType Directory -Force -Path $runs | Out-Null
Remove-Item -Path $done, $failed -ErrorAction SilentlyContinue

$env:OMP_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:NUMEXPR_NUM_THREADS = "1"
$env:MEGA_WORKERS = "2"

Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class AwakeConfirmTail {
    [DllImport("kernel32.dll")]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@

$ES_CONTINUOUS = [Convert]::ToUInt32("80000000", 16)
$ES_SYSTEM_REQUIRED = [uint32]0x00000001
$ES_AWAYMODE_REQUIRED = [uint32]0x00000040

function Keep-Awake {
    [AwakeConfirmTail]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_AWAYMODE_REQUIRED) | Out-Null
}

function Write-Status([string]$stage, [string]$status) {
    Keep-Awake
    $payload = [ordered]@{
        ts = (Get-Date).ToString("o")
        mode = "confirm_validation_tail_2026-06-04"
        stage = $stage
        status = $status
    } | ConvertTo-Json -Depth 3
    Set-Content -Path $heartbeat -Value $payload -Encoding ASCII
    Add-Content -Path $log -Value ("[{0}] {1} {2}" -f (Get-Date).ToString("s"), $stage, $status) -Encoding ASCII
}

function Run-Step([string]$stage, [string[]]$stepArgs) {
    Write-Status $stage "running"
    Add-Content -Path $log -Value ("> python " + ($stepArgs -join " ")) -Encoding ASCII
    & python @stepArgs 2>&1 | ForEach-Object { Add-Content -Path $log -Value $_ -Encoding UTF8 }
    if ($LASTEXITCODE -ne 0) {
        Write-Status $stage ("failed exit=" + $LASTEXITCODE)
        throw "$stage failed with exit $LASTEXITCODE"
    }
    Write-Status $stage "complete"
}

try {
    Set-Location $tools
    Write-Status "start" "running"

    Run-Step "aggregate" @(
        "aggregate_overnight_iters.py",
        "--runs-dir", $runs,
        "--out", (Join-Path $runs "AGGREGATE_night_confirm_2026-06-04.md")
    )

    Run-Step "cpcv" @(
        "cpcv_validator.py",
        "--input", (Join-Path $results "MEGA_walk_forward_results.json"),
        "--out-dir", (Join-Path $results "cpcv"),
        "--max-candidates", "16",
        "--v2"
    )

    Run-Step "pbo" @(
        "probabilistic_pbo.py",
        "--cpcv", (Join-Path $results "cpcv\cpcv_results.json"),
        "--out-dir", (Join-Path $results "pbo")
    )

    Run-Step "evaluation_artifacts" @(
        "build_evaluation_artifact.py",
        "--mega", (Join-Path $results "MEGA_walk_forward_results.json"),
        "--cpcv", (Join-Path $results "cpcv\cpcv_results.json"),
        "--pbo", (Join-Path $results "pbo\pbo_results.json"),
        "--out-dir", (Join-Path $results "evaluation_artifacts")
    )

    Run-Step "score_gate2" @(
        "score_gate2.py",
        "--in-dir", (Join-Path $results "evaluation_artifacts"),
        "--out-dir", (Join-Path $results "scorecards")
    )

    Write-Status "done" "complete"
    New-Item -ItemType File -Path $done -Force | Out-Null
} catch {
    Add-Content -Path $log -Value ("ERROR: " + $_.Exception.Message) -Encoding UTF8
    Write-Status "error" $_.Exception.Message
    New-Item -ItemType File -Path $failed -Force | Out-Null
    exit 1
} finally {
    [AwakeConfirmTail]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null
}
