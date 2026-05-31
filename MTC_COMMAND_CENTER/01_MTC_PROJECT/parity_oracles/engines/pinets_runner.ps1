param(
  [Parameter(Mandatory=$true)][string]$Case,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [string]$Raw,
  [string]$Pine = "01_PINE/MTC_V2.pine",
  [string]$Data
)

$argsList = @("parity_oracles/engines/pinets_runner.py", "--case", $Case, "--out-dir", $OutDir, "--pine", $Pine)
if ($Raw) { $argsList += @("--raw", $Raw) }
if ($Data) { $argsList += @("--data", $Data) }
python @argsList
exit $LASTEXITCODE
