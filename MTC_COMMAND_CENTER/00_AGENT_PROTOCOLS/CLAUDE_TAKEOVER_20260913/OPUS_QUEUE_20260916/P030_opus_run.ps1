# Exact claude-opus-5 xhigh T0 review of WP-P0-30 candidate daf6a43b on the Claude PRO profile (~/.claude), NOT the Max desktop session.
# PREPARED 2026-09-15 for the weekly reset (2026-09-16 20:00Z). Lead starts it; never while agy.exe runs; never two Pro lanes at once.
$ErrorActionPreference = 'Continue'
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_API_WALLET_KEY -ErrorAction SilentlyContinue
$env:PYTHONUTF8='1'; $env:PYTHONDONTWRITEBYTECODE='1'
$lane = 'C:\tmp\OPUS_QUEUE_20260916\P030\opus'
$tmp = Join-Path $env:LOCALAPPDATA 'Temp\opus_p030'
$env:TEMP = $tmp; $env:TMP = $tmp
New-Item -ItemType Directory -Force $tmp, "$lane\logs", 'C:\tmp\OPUS_P030_SCRATCH' | Out-Null
$env:CLAUDE_CONFIG_DIR = (Join-Path $env:USERPROFILE '.claude')
Set-Location 'C:\tmp\P030_INTEGRATION_20260913'
$head = (git -c safe.directory=* rev-parse HEAD).Trim()
if ($head -ne 'daf6a43b0c4eaafd78e84df776d30d3e41d81d7b') { "HEAD $head != daf6a43b: refuse" | Out-File "$lane\launch.exit" -Encoding ascii; exit 3 }
$start = Get-Date
& claude --print "Read and execute exactly $lane\BRIEF.md. Start by reading that file." --model claude-opus-5 --effort xhigh --permission-mode dontAsk --allowedTools 'Bash' 'Edit' 'Read' 'Write' 'Glob' 'Grep' --disallowedTools 'Agent' 'WebFetch' 'WebSearch' 'NotebookEdit' --add-dir 'C:\tmp\OPUS_QUEUE_20260916\P030' 'C:\tmp\OPUS_P030_SCRATCH' 'C:\tmp\P030_INTEGRATION_20260913' 'C:\CT13' --strict-mcp-config --max-turns 100 --output-format stream-json --verbose 2>&1 | Out-File -FilePath "$lane\stream.jsonl" -Encoding utf8
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "$lane\launch.exit" -Encoding ascii
