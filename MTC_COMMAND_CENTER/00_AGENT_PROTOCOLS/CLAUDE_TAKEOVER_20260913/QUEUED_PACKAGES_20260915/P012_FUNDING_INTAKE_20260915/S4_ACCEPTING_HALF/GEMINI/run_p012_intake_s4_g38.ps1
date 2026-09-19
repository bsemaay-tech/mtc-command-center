param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$ReviewRoot
)

# PREPARED ONLY: Lead alone starts this after obtaining the required authorization.
$ErrorActionPreference = 'Stop'
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

$launcher = Join-Path $env:USERPROFILE 'AI_CLI_HELPERS/Invoke-GeminiProReadOnly.ps1'
$ownedParent = 'C:\tmp\P012_S16_REVIEWS_20260913'
$promptPath = Join-Path $ReviewRoot 'PROMPT.md'
$reviewLog = Join-Path $ReviewRoot 'REVIEW.log'
$launchExit = Join-Path $ReviewRoot 'launch.exit'
$holdAuthorization = Join-Path $ReviewRoot 'HOLD_AUTHORIZATION.txt'

$resolvedReviewRoot = [System.IO.Path]::GetFullPath($ReviewRoot).TrimEnd('\')
$resolvedOwnedParent = [System.IO.Path]::GetFullPath($ownedParent).TrimEnd('\')
if (-not $resolvedReviewRoot.StartsWith($resolvedOwnedParent + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "ReviewRoot must be a separately prepared owned directory under $ownedParent"
}
if (-not (Test-Path -LiteralPath $resolvedReviewRoot -PathType Container)) {
    throw "Missing prepared Gemini review directory: $resolvedReviewRoot"
}
if (-not (Test-Path -LiteralPath $promptPath -PathType Leaf)) {
    throw "Missing assembled Gemini prompt: $promptPath"
}
if (-not (Test-Path -LiteralPath $launcher -PathType Leaf)) {
    throw "Missing read-only Gemini launcher: $launcher"
}
if (-not (Test-Path -LiteralPath $holdAuthorization -PathType Leaf) -or
    [string]::IsNullOrWhiteSpace((Get-Content -LiteralPath $holdAuthorization -Raw -Encoding utf8))) {
    throw "Missing nonempty HOLD_AUTHORIZATION.txt: $holdAuthorization"
}
foreach ($path in @($reviewLog, $launchExit)) {
    if (Test-Path -LiteralPath $path) { throw "Refusing to overwrite Gemini output: $path" }
}

$prompt = Get-Content -LiteralPath $promptPath -Raw -Encoding utf8
if (-not $prompt.Contains('C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_S4_20260916') -or
    -not $prompt.Contains('Read ONLY files inside this packet')) {
    throw 'Prompt is missing the required packet boundary'
}

$start = Get-Date
$resultCode = 1
$actualExitCode = 1

try {
    Set-Location 'C:/LAB/Tradingview_LAB_CLEAN'
    $LASTEXITCODE = 0
    & $launcher -Prompt $prompt -Model gemini-3.8-flash-high -ExpectedBranch root/current-20260829 -TimeoutSeconds 1500 2>&1 |
        Out-File -LiteralPath $reviewLog -Encoding utf8
    $actualExitCode = if ($null -eq $LASTEXITCODE) { 1 } else { [int]$LASTEXITCODE }
    if ($actualExitCode -ne 0) { throw "launcher exited with code $actualExitCode" }
    $resultCode = 0
}
catch {
    $resultCode = if ($actualExitCode -ne 0) { $actualExitCode } else { 1 }
    $errorMessage = ($_.Exception.Message -replace '\s+', ' ').Trim()
    if ($errorMessage.Length -gt 240) { $errorMessage = $errorMessage.Substring(0, 240) }
    try { Add-Content -LiteralPath $reviewLog -Value "error=$($_.Exception.GetType().FullName): $errorMessage" -Encoding utf8 } catch { }
}
finally {
    $end = Get-Date
    "exit=$resultCode actual_exit=$actualExitCode start=$($start.ToUniversalTime().ToString('o')) end=$($end.ToUniversalTime().ToString('o'))" |
        Out-File -LiteralPath $launchExit -Encoding ascii
}

exit $resultCode
