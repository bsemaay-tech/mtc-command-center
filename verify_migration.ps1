$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$target = "C:\LAB\Tradingview_LAB_CLEAN"
$legacy = "C:\LAB\tradingview-lab"
$manifestDir = Join-Path $target "docs\migration_manifests"
$result = [ordered]@{}
$result.target_tree_created = Test-Path -LiteralPath $target
$beforePath = Join-Path $manifestDir "legacy_git_status_before.txt"
$afterPath = Join-Path $manifestDir "legacy_git_status_after_verify.txt"
$before = if (Test-Path -LiteralPath $beforePath) { Get-Content -LiteralPath $beforePath -Raw -Encoding UTF8 } else { "" }
$after = git -C $legacy status --short | Out-String
Set-Content -LiteralPath $afterPath -Value $after -Encoding UTF8
$beforeNorm = ($before -replace "`r`n","`n").Trim()
$afterNorm = ($after -replace "`r`n","`n").Trim()
$result.legacy_untouched_check = ($beforeNorm -eq $afterNorm)
$excludedNames = @("SECONDBRAIN","SECONDBRAIN_TEMP","BUDGET APP","node_modules","__pycache__",".git","debug",".pytest_cache",".venv","venv","dist","build",".tmp","temp","tmp")
$found = @()
foreach ($name in $excludedNames) {
  $found += Get-ChildItem -LiteralPath $target -Force -Recurse -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq $name } | Select-Object -ExpandProperty FullName
}
$dash = Join-Path $target "external\traderspost-command-dash"
if (Test-Path -LiteralPath $dash) { $found += $dash }
$result.excluded_folder_absent_check = ($found.Count -eq 0)
$result.excluded_folder_hits = @($found)
$copyManifest = Import-Csv -LiteralPath (Join-Path $manifestDir "copy_manifest.csv")
$mismatch = @()
foreach ($row in $copyManifest) {
  if (Test-Path -LiteralPath $row.target) {
    $hash = (Get-FileHash -LiteralPath $row.target -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $row.target_sha256.ToLowerInvariant()) { $mismatch += $row.target }
  } else {
    $mismatch += $row.target
  }
}
$result.copy_manifest_sha256_check = ($mismatch.Count -eq 0)
$result.copy_manifest_mismatches = @($mismatch)
$pineRows = @()
Get-ChildItem -LiteralPath $target -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in @(".pine",".pinescript") -or $_.Name -like "*.pine.txt" } | ForEach-Object {
  $pineRows += [pscustomobject]@{ Path=$_.FullName; Bytes=$_.Length; SHA256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
}
$pineManifest = Join-Path $manifestDir "pine_sha256_manifest.csv"
$pineRows | Export-Csv -LiteralPath $pineManifest -NoTypeInformation -Encoding UTF8
$result.pine_file_count = $pineRows.Count
$dedupeManifest = Join-Path $manifestDir "deduplication_manifest.csv"
$dedupeRows = if (Test-Path -LiteralPath $dedupeManifest) { Import-Csv -LiteralPath $dedupeManifest } else { @() }
$result.deduplication_skipped_count = @($dedupeRows).Count
$result.mtc_command_center_manifest_exists = Test-Path -LiteralPath (Join-Path $manifestDir "mtc_command_center_sha256_manifest.csv")
$result.status = if ($result.target_tree_created -and $result.legacy_untouched_check -and $result.excluded_folder_absent_check -and $result.copy_manifest_sha256_check) { "PASS" } else { "FAIL" }
$json = $result | ConvertTo-Json -Depth 6
Set-Content -LiteralPath (Join-Path $manifestDir "verify_migration_result.json") -Value $json -Encoding UTF8
$json
if ($result.status -ne "PASS") { exit 1 }
