# Exact gpt-5.6-sol xhigh review of DD06 at a46da0aa7a4ea3a58fb00c5e293e10b60307687d on the Codex Plus pool (account 'free'), generated from the Wednesday lane.
# Lead starts it BY HAND after the Friday reset; never while agy.exe runs; never two Codex lanes on one account at once.
$ErrorActionPreference = 'Continue'
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_API_WALLET_KEY -ErrorAction SilentlyContinue
$lane = 'C:\tmp\SOL_QUEUE_20260919\DD06\sol'
$wt = 'C:\tmp\P029_DD06_20260915'
$launcher = Join-Path $env:USERPROFILE 'AI_CLI_HELPERS\Invoke-CodexForClaude.ps1'
$env:PYTHONUTF8 = '1'; $env:PYTHONDONTWRITEBYTECODE = '1'; $env:TEMP = "$lane\tmp"; $env:TMP = "$lane\tmp"
New-Item -ItemType Directory -Force "$lane\tmp" | Out-Null
if (Get-Process agy -ErrorAction SilentlyContinue) { 'agy.exe running: refuse' | Out-File "$lane\launch.exit" -Encoding ascii; exit 4 }
$head = (git -c safe.directory=* -C $wt rev-parse HEAD).Trim()
if ($head -ne 'a46da0aa7a4ea3a58fb00c5e293e10b60307687d') { "HEAD $head != a46da0aa: refuse" | Out-File "$lane\launch.exit" -Encoding ascii; exit 3 }
$prompt = "Read the file $lane\BRIEF.md in full and execute it exactly. Start by reading that file."
$codexArgs = @('exec', '-m', 'gpt-5.6-sol', '-c', 'model_reasoning_effort=xhigh', '--ephemeral', '--sandbox', 'workspace-write', '--skip-git-repo-check', '-C', "C:\tmp\SOL_DD06_SCRATCH", '--add-dir', $lane, '--add-dir', $wt, '--add-dir', 'C:\CT13', '--add-dir', 'C:\tmp\OPUS_QUEUE_20260916\DD06', '--json', '--output-last-message', "$lane\SOL_LAST_MESSAGE.md", $prompt)
$start = Get-Date
& $launcher -Account free -CodexArgs $codexArgs 2>&1 | Out-File -FilePath "$lane\stream.jsonl" -Encoding utf8
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "$lane\launch.exit" -Encoding ascii
