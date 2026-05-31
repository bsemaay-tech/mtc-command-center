$ErrorActionPreference = "Stop"

# Define path to the single source of truth
$strategyPath = Resolve-Path "$PSScriptRoot/../00_MASTER_TEMPLATE/MASTER_TEMPLATE_v2_RC1.pine"

if (-not (Test-Path $strategyPath)) {
    Write-Error "Strategy file not found at: $strategyPath"
    exit 1
}

# Read content and set to clipboard
Get-Content -Path $strategyPath -Raw | Set-Clipboard

Write-Host "✅ SUCCESS: Strategy copied to clipboard!"
Write-Host "   File: $strategyPath"
Write-Host "   Ready to paste into TradingView."
