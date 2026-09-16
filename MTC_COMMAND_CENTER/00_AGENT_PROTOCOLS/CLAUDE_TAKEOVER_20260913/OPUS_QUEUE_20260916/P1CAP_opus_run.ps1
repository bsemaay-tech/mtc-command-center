# Exact claude-opus-5 xhigh T0 review of the WP-P0-12 Path 1 capture tool candidate af921d75 on the Claude PRO profile (~/.claude), NOT the Max desktop session.
# PREPARED 2026-09-15 for the weekly reset (2026-09-16 20:00Z). Lead starts it; never while agy.exe runs; never two Pro lanes at once.
# The reviewer makes NO network call; HL_API_WALLET_KEY and ANTHROPIC_API_KEY are removed from the child environment.
$ErrorActionPreference = 'Continue'
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_API_WALLET_KEY -ErrorAction SilentlyContinue
$env:PYTHONUTF8='1'; $env:PYTHONDONTWRITEBYTECODE='1'
$lane = 'C:\tmp\OPUS_QUEUE_20260916\P1CAP\opus'
$tmp = Join-Path $env:LOCALAPPDATA 'Temp\opus_p1cap'
$env:TEMP = $tmp; $env:TMP = $tmp
New-Item -ItemType Directory -Force $tmp, "$lane\logs", 'C:\tmp\OPUS_P1CAP_SCRATCH' | Out-Null
$env:CLAUDE_CONFIG_DIR = (Join-Path $env:USERPROFILE '.claude')
Set-Location 'C:\tmp\P1CAP_20260914'
$head = (git -c safe.directory=* rev-parse HEAD).Trim()
if ($head -ne 'af921d75226932b11c5f0279b2cbf0b0de5be9e0') { "HEAD $head != af921d75: refuse" | Out-File "$lane\launch.exit" -Encoding ascii; exit 3 }
$start = Get-Date
& claude --print "Read and execute exactly $lane\BRIEF.md. Start by reading that file." --model claude-opus-5 --effort xhigh --permission-mode dontAsk --allowedTools 'Bash' 'PowerShell' 'Edit' 'Read' 'Write' 'Glob' 'Grep' --disallowedTools 'Agent' 'WebFetch' 'WebSearch' 'NotebookEdit' --add-dir 'C:\tmp\OPUS_QUEUE_20260916\P1CAP' 'C:\tmp\OPUS_P1CAP_SCRATCH' 'C:\tmp\P1CAP_20260914' 'C:\tmp\P012_FUNDING_PY312_20260911\Lib\site-packages\hyperliquid' 'C:\CT13' --strict-mcp-config --max-turns 100 --output-format stream-json --verbose 2>&1 | Out-File -FilePath "$lane\stream.jsonl" -Encoding utf8
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "$lane\launch.exit" -Encoding ascii
