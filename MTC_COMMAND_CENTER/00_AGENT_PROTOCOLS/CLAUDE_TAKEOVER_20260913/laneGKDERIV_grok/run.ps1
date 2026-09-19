# Grok detection pre-screen of the P020 derived plan + derivation tool (PREPARED 2026-09-15; run after the SuperGrok weekly reset, 2026-09-18).
# Owner: OD-20260915-P020-MEASURE-GROK-1. No git anywhere while this runs is NOT required (Grok lane does not touch the repository),
# but never start it while agy.exe (Gemini) runs, and never run it against a moved package (digest checks in the BRIEF).
$ErrorActionPreference = 'Continue'
$lane = 'C:\tmp\CLAUDE_P0_RUN_20260913\laneGKDERIV_grok'
$scratch = 'C:\tmp\GROK_SCRATCH_GKDERIV'
New-Item -ItemType Directory -Force $scratch | Out-Null
$grok = Join-Path $env:USERPROFILE 'AI_CLI_HELPERS\Invoke-GrokSubscription.ps1'
$env:TEMP = $scratch; $env:TMP = $scratch; $env:PYTHONDONTWRITEBYTECODE = '1'; $env:PYTHONUTF8 = '1'
$prompt = "Read the file $lane\BRIEF.md in full. It is your complete task specification. Execute it exactly as written."
Set-Location $scratch
$start = Get-Date
& $grok --always-approve --disable-web-search --cwd $scratch -p $prompt *> "$lane\GROK_RUN.log"
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "$lane\launch.exit" -Encoding ascii
