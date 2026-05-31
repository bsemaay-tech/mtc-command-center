param(
    [ValidateSet("init", "bootstrap", "build-from-v6", "baseline-freeze", "optimize", "sync-folders", "build-guide", "freeze", "route", "all")]
    [string]$Stage = "all",
    [string]$BaselineCaseId = "parity_core_001_baseline_touch",
    [string]$BaselineXlsx = "mtc_backtest/parity_suite_350/manifests/baseline_sources/baseline_tv_export_FILLED_v6.xlsx",
    [string]$SourceSuite = "",
    [switch]$Copy,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$SuiteRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptsDir = Join-Path $SuiteRoot "scripts"
$PythonExe = "python"

function Invoke-PythonScript {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ScriptPath,
        [string[]]$Args = @()
    )
    & $PythonExe $ScriptPath @Args
    if ($LASTEXITCODE -ne 0) {
        throw "Python script failed: $ScriptPath (exit=$LASTEXITCODE)"
    }
}

function Ensure-Dir([string]$Path) {
    if (-not (Test-Path $Path)) {
        New-Item -Path $Path -ItemType Directory -Force | Out-Null
    }
}

function Ensure-File([string]$Path, [string]$Content) {
    if (-not (Test-Path $Path)) {
        $Content | Out-File -FilePath $Path -Encoding utf8
    }
}

if ($Stage -in @("init", "all")) {
    Ensure-Dir (Join-Path $SuiteRoot "cases")
    Ensure-Dir (Join-Path $SuiteRoot "manifests")
    Ensure-Dir (Join-Path $SuiteRoot "manifests/baseline_sources")
    Ensure-Dir (Join-Path $SuiteRoot "tv_manual_inputs")
    Ensure-Dir (Join-Path $SuiteRoot "tv_manual_inputs/raw_tv_exports")
    Ensure-Dir (Join-Path $SuiteRoot "tv_manual_inputs/unmatched")
    Ensure-Dir (Join-Path $SuiteRoot "triage")
    Ensure-Dir (Join-Path $SuiteRoot "runs")
    Ensure-Dir (Join-Path $SuiteRoot "compare_runs")

    $manifestHeader = "run_order,pack,case_id,case_json,tv_preset_name,enabled,expected_trade_behavior,primary_change,ui_actions,depends_on,parent_required,canonical_config_hash,semantic_fingerprint,symbol,timeframe,start_date,end_date,notes"
    Ensure-File (Join-Path $SuiteRoot "manifests/cases_manifest_all.csv") $manifestHeader
    Ensure-File (Join-Path $SuiteRoot "manifests/cases_manifest_core.csv") $manifestHeader
    Ensure-File (Join-Path $SuiteRoot "manifests/cases_manifest_boundary.csv") $manifestHeader
    Ensure-File (Join-Path $SuiteRoot "manifests/cases_manifest_pairwise.csv") $manifestHeader
    Ensure-File (Join-Path $SuiteRoot "manifests/coverage_report.csv") "param_id,ui_key,testable,covered_in_core,covered_in_boundary,covered_in_pairwise,total_cases_covering,gap_flag,notes"
}

if ($Stage -in @("bootstrap")) {
    if ([string]::IsNullOrWhiteSpace($SourceSuite)) {
        throw "bootstrap stage requires -SourceSuite. Legacy parity_suite_340 default removed. Use -Stage build-from-v6 for current workflow."
    }
    $bootstrapScript = Join-Path $ScriptsDir "bootstrap_from_340.py"
    Invoke-PythonScript -ScriptPath $bootstrapScript -Args @("--workspace-root", ".", "--source-suite", $SourceSuite, "--target-suite", $SuiteRoot)
}

if ($Stage -in @("baseline-freeze", "freeze", "all")) {
    $freezeBaselineScript = Join-Path $ScriptsDir "freeze_baseline_record.py"
    Invoke-PythonScript -ScriptPath $freezeBaselineScript -Args @("--workspace-root", ".", "--suite-root", $SuiteRoot, "--baseline-case-id", $BaselineCaseId, "--baseline-xlsx", $BaselineXlsx)
}

if ($Stage -in @("optimize", "freeze")) {
    $optScript = Join-Path $ScriptsDir "optimize_ui_coverage_case_set.py"
    Invoke-PythonScript -ScriptPath $optScript -Args @("--suite-root", $SuiteRoot, "--baseline-case-id", $BaselineCaseId)
}

if ($Stage -in @("build-from-v6")) {
    $genScript = Join-Path $ScriptsDir "generate_case_set_from_input_map.py"
    Invoke-PythonScript -ScriptPath $genScript -Args @("--suite-root", $SuiteRoot, "--purge-cases")
}

if ($Stage -in @("build-guide", "freeze", "all")) {
    $guideScript = Join-Path $ScriptsDir "build_case_setup_guide.py"
    Invoke-PythonScript -ScriptPath $guideScript -Args @("--suite-root", $SuiteRoot)
}

if ($Stage -in @("sync-folders", "freeze", "all")) {
    $syncScript = Join-Path $ScriptsDir "sync_tv_case_folders.py"
    $syncArgs = @("--suite-root", $SuiteRoot)
    if ($DryRun) {
        $syncArgs += "--dry-run"
    }
    Invoke-PythonScript -ScriptPath $syncScript -Args $syncArgs
}

if ($Stage -in @("route", "all")) {
    $routeScript = Join-Path $ScriptsDir "route_tv_xlsx.py"
    $routeArgs = @("--suite-root", $SuiteRoot, "--update-guide", (Join-Path $SuiteRoot "CASE_SETUP_GUIDE.xlsx"))
    # 457-source set has many default-value cases; exact property matching can be ambiguous.
    # Sequential fallback routes to next pending run_order when strong match is not unique.
    $routeArgs += "--sequential-fallback"
    if ($Copy) {
        $routeArgs += "--copy"
    }
    if ($DryRun) {
        $routeArgs += "--dry-run"
    }
    Invoke-PythonScript -ScriptPath $routeScript -Args $routeArgs
}

Write-Output "stage=$Stage"
Write-Output "suite_root=$SuiteRoot"
Write-Output "status=ok"
