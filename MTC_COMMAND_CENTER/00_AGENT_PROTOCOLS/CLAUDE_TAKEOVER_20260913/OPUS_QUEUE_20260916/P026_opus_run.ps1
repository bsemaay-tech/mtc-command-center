# Exact claude-opus-5 xhigh T0 review of WP-P0-26 candidate e114ed31 (6ac9cfb7 + adapter slice 8d4056c5 + findings slice d81b07f6 + README-only e114ed31) on the Claude PRO profile (~/.claude), NOT the Max desktop session.
# PREPARED 2026-09-15 for the weekly reset (2026-09-16 20:00Z). LANE 4 = optional: only if allowance remains after lanes 1-3.
# Lead starts it; never while agy.exe runs; never two Pro lanes at once. Option A landed 2026-09-15 10:58Z as 8d4056c5; the Gemini-findings slice 3 landed 11:33Z as d81b07f6; the README-only commit (owner item 7 "A") landed 18:39Z as e114ed31 (pin updated); the launcher refuses on any drift.
$ErrorActionPreference = 'Continue'
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_API_WALLET_KEY -ErrorAction SilentlyContinue
$env:PYTHONUTF8='1'; $env:PYTHONDONTWRITEBYTECODE='1'
$lane = 'C:\tmp\OPUS_QUEUE_20260916\P026\opus'
$tmp = Join-Path $env:LOCALAPPDATA 'Temp\opus_p026'
$env:TEMP = $tmp; $env:TMP = $tmp
New-Item -ItemType Directory -Force $tmp, "$lane\logs", 'C:\tmp\OPUS_P026_SCRATCH' | Out-Null
$env:CLAUDE_CONFIG_DIR = (Join-Path $env:USERPROFILE '.claude')
Set-Location 'C:\tmp\P026_REPAIR_20260915'
$head = (git -c safe.directory=* rev-parse HEAD).Trim()
if ($head -ne 'e114ed314fa2545b5c64399ddb024e4d75289c14') { "HEAD $head != e114ed31: refuse" | Out-File "$lane\launch.exit" -Encoding ascii; exit 3 }
$start = Get-Date
& claude --print "Read and execute exactly $lane\BRIEF.md. Start by reading that file." --model claude-opus-5 --effort xhigh --permission-mode dontAsk --allowedTools 'Bash' 'PowerShell' 'Edit' 'Read' 'Write' 'Glob' 'Grep' --disallowedTools 'Agent' 'WebFetch' 'WebSearch' 'NotebookEdit' --add-dir 'C:\tmp\OPUS_QUEUE_20260916\P026' 'C:\tmp\OPUS_P026_SCRATCH' 'C:\tmp\P026_REPAIR_20260915' 'C:\CT13' --strict-mcp-config --max-turns 100 --output-format stream-json --verbose 2>&1 | Out-File -FilePath "$lane\stream.jsonl" -Encoding utf8
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "$lane\launch.exit" -Encoding ascii
