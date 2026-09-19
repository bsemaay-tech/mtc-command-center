# Exact gpt-5.6-sol xhigh review of P012INTAKE at 8cbf4f1a7b04afb5b011eb9fb609fbd03089b7f3 on the Codex Plus pool (account 'free'), generated from the Wednesday lane.
# Lead starts it BY HAND after the Friday reset; never while agy.exe runs; never two Codex lanes on one account at once.
$ErrorActionPreference = 'Continue'
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_API_WALLET_KEY -ErrorAction SilentlyContinue
$lane = 'C:\tmp\SOL_QUEUE_20260919\P012INTAKE\sol'
$wt = 'C:\tmp\P012_INTAKE_NIT_20260919'
$launcher = Join-Path $env:USERPROFILE 'AI_CLI_HELPERS\Invoke-CodexForClaude.ps1'
$env:PYTHONUTF8 = '1'; $env:PYTHONDONTWRITEBYTECODE = '1'; $env:TEMP = "$lane\tmp"; $env:TMP = "$lane\tmp"
New-Item -ItemType Directory -Force "$lane\tmp" | Out-Null
if (Get-Process agy -ErrorAction SilentlyContinue) { 'agy.exe running: refuse' | Out-File "$lane\launch.exit" -Encoding ascii; exit 4 }
$head = (git -c safe.directory=* -C $wt rev-parse HEAD).Trim()
if ($head -ne '8cbf4f1a7b04afb5b011eb9fb609fbd03089b7f3') { "HEAD $head != 8cbf4f1a: refuse" | Out-File "$lane\launch.exit" -Encoding ascii; exit 3 }
$prompt = "Read the file $lane\BRIEF.md in full and execute it exactly. Start by reading that file."
$codexArgs = @('exec', '-m', 'gpt-5.6-sol', '-c', 'model_reasoning_effort=xhigh', '--ephemeral', '--sandbox', 'workspace-write', '--skip-git-repo-check', '-C', "C:\tmp\SOL_P012INTAKE_SCRATCH", '--add-dir', $lane, '--add-dir', $wt, '--add-dir', 'C:\CT13', '--add-dir', 'C:\tmp\OPUS_QUEUE_20260916\P012INTAKE', '--json', '--output-last-message', "$lane\SOL_LAST_MESSAGE.md", $prompt)
$start = Get-Date
& $launcher -Account free -CodexArgs $codexArgs 2>&1 | Out-File -FilePath "$lane\stream.jsonl" -Encoding utf8
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "$lane\launch.exit" -Encoding ascii
