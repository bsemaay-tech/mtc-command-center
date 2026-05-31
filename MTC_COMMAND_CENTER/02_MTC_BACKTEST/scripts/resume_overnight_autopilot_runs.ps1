param(
    [string]$ManifestPath = (Join-Path $PSScriptRoot "..\results\overnight\active_autopilot_resume_manifest.json"),
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Write-ResumeLog {
    param(
        [string]$Path,
        [string]$Message
    )
    $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"
    Add-Content -Path $Path -Value "$timestamp $Message"
}

function Get-ExistingRunProcess {
    param(
        [string]$RunRoot
    )
    $escaped = $RunRoot.Replace("\", "\\")
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
        Where-Object { $_.CommandLine -like "*$escaped*" -or $_.CommandLine -like "*$RunRoot*" } |
        Select-Object -First 1
}

$manifestFile = [System.IO.Path]::GetFullPath($ManifestPath)
if (-not (Test-Path $manifestFile)) {
    throw "Manifest not found: $manifestFile"
}

$manifestDir = Split-Path -Parent $manifestFile
$logPath = Join-Path $manifestDir "active_autopilot_resume.log"
$manifest = Get-Content -Raw $manifestFile | ConvertFrom-Json

foreach ($run in $manifest.runs) {
    $existing = Get-ExistingRunProcess -RunRoot $run.run_root
    if ($existing -and -not $Force) {
        Write-ResumeLog -Path $logPath -Message "[skip] $($run.name) already running with PID $($existing.ProcessId)"
        continue
    }

    $stdoutDir = Split-Path -Parent $run.stdout_path
    $stderrDir = Split-Path -Parent $run.stderr_path
    if ($stdoutDir) {
        New-Item -ItemType Directory -Force -Path $stdoutDir | Out-Null
    }
    if ($stderrDir) {
        New-Item -ItemType Directory -Force -Path $stderrDir | Out-Null
    }

    $argumentList = @(
        $run.script_path,
        "--run-root", $run.run_root,
        "--base-case", $run.base_case,
        "--dataset", $run.dataset,
        "--holdout-end", $run.holdout_end
    )
    foreach ($arg in $run.extra_args) {
        $argumentList += [string]$arg
    }

    $process = Start-Process `
        -FilePath $run.python_exe `
        -ArgumentList $argumentList `
        -WorkingDirectory $run.working_directory `
        -RedirectStandardOutput $run.stdout_path `
        -RedirectStandardError $run.stderr_path `
        -WindowStyle Hidden `
        -PassThru

    Write-ResumeLog -Path $logPath -Message "[start] $($run.name) PID=$($process.Id) run_root=$($run.run_root)"
}
