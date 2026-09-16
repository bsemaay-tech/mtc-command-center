# Exact claude-opus-5 xhigh review of WP-P0-12 funding intake slice 4 — the ACCEPTING half of export_mtc_funding.py under D-1..D-6 (candidate 9ef072a8; parent b667dbcc format-only) on the Claude PRO profile (~/.claude), NOT the Max desktop session.
# PREPARED 2026-09-15 20:2xZ; RE-PINNED 2026-09-16 ~11:00 UTC+3 (4c802e9b -> 9ef072a8 after the day slice). OPTIONAL lane (6-8): only if allowance remains after lanes 1-5; started BY HAND; never while agy.exe runs; never two Pro lanes at once; refuses on HEAD drift.
$ErrorActionPreference = 'Continue'
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_API_WALLET_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_ACCOUNT_ADDRESS -ErrorAction SilentlyContinue
Remove-Item Env:HL_LIVE_ACK -ErrorAction SilentlyContinue
$env:PYTHONUTF8='1'; $env:PYTHONDONTWRITEBYTECODE='1'
$lane = 'C:\tmp\OPUS_QUEUE_20260916\P012INTAKE\opus'
$tmp = Join-Path $env:LOCALAPPDATA 'Temp\opus_p012intake'
$env:TEMP = $tmp; $env:TMP = $tmp
New-Item -ItemType Directory -Force $tmp, "$lane\logs", 'C:\tmp\OPUS_P012INTAKE_SCRATCH' | Out-Null
$env:CLAUDE_CONFIG_DIR = (Join-Path $env:USERPROFILE '.claude')
if (Get-Process agy -ErrorAction SilentlyContinue) { 'agy.exe running: refuse' | Out-File "$lane\launch.exit" -Encoding ascii; exit 4 }
Set-Location 'C:\tmp\P012_INTAKE_20260915'
$head = (git -c safe.directory=* rev-parse HEAD).Trim()
if ($head -ne '9ef072a8cbc83915679d0cfc4fb142fba449c8e0') { "HEAD $head != 9ef072a8: refuse" | Out-File "$lane\launch.exit" -Encoding ascii; exit 3 }
$start = Get-Date
& claude --print "Read and execute exactly $lane\BRIEF.md. Start by reading that file." --model claude-opus-5 --effort xhigh --permission-mode dontAsk --allowedTools 'Bash' 'Edit' 'Read' 'Write' 'Glob' 'Grep' --disallowedTools 'Agent' 'WebFetch' 'WebSearch' 'NotebookEdit' --add-dir 'C:\tmp\OPUS_QUEUE_20260916\P012INTAKE' 'C:\tmp\OPUS_P012INTAKE_SCRATCH' 'C:\tmp\P012_INTAKE_20260915' 'C:\tmp\CLAUDE_P0_RUN_20260913\P012_PATH1_REAL_CAPTURE_20260915' 'C:\CT13' --strict-mcp-config --max-turns 100 --output-format stream-json --verbose 2>&1 | Out-File -FilePath "$lane\stream.jsonl" -Encoding utf8
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "$lane\launch.exit" -Encoding ascii
