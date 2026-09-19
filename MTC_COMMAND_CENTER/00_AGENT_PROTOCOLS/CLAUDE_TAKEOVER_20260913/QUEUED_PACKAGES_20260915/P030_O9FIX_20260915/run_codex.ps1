$ErrorActionPreference = 'Continue'
$lane = 'C:\tmp\CLAUDE_P0_RUN_20260913\laneO9FIX_build'
$cwd = 'C:\tmp\P030_INTEGRATION_20260913'
$launcher = Join-Path $env:USERPROFILE 'AI_CLI_HELPERS\Invoke-CodexForClaude.ps1'
$env:PYTHONUTF8 = '1'; $env:PYTHONDONTWRITEBYTECODE = '1'; $env:TEMP = "$lane\tmp"; $env:TMP = "$lane\tmp"
New-Item -ItemType Directory -Force "$lane\tmp" | Out-Null
Copy-Item "$lane\TASK.md" "$cwd\TASK_O9FIX.md" -Force
$prompt = "Read the file TASK_O9FIX.md in the current working directory in full and execute it exactly. The Gemini review it cites is $lane\GEMINI_REPORT.md. Writable: cwd and $lane; everything else is read-only."
$codexArgs = @('exec', '-m', 'gpt-5.5', '-c', 'model_reasoning_effort=high', '--ephemeral', '--sandbox', 'workspace-write', '--skip-git-repo-check', '-C', $cwd, '--add-dir', $lane, '--json', '--output-last-message', "$lane\CODEX_LAST_MESSAGE.md", $prompt)
$start = Get-Date
& $launcher -Account secondary -CodexArgs $codexArgs 2>&1 | Out-File -FilePath "$lane\stream.jsonl" -Encoding utf8
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File -FilePath "$lane\launch.exit" -Encoding ascii
