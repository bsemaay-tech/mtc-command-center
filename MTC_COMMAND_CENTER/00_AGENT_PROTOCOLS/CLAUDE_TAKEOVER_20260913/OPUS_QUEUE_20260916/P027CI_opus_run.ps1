# Exact claude-opus-5 xhigh T1 review of the WP-P0-27 CI workflow PRs #193 (a3325836) and #194 (63b7bbe0) on the Claude PRO profile (~/.claude), NOT the Max desktop session.
# PREPARED 2026-09-15 18:4xZ under the owner's word "we'd opus" (= Wed Opus, T1 of both PRs after lanes 1-4). LANE 5 = started BY HAND after lane 4; never while agy.exe runs; never two Pro lanes at once.
$ErrorActionPreference = 'Continue'
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_API_WALLET_KEY -ErrorAction SilentlyContinue
$env:PYTHONUTF8='1'; $env:PYTHONDONTWRITEBYTECODE='1'
$lane = 'C:\tmp\OPUS_QUEUE_20260916\P027CI\opus'
$tmp = Join-Path $env:LOCALAPPDATA 'Temp\opus_p027ci'
$env:TEMP = $tmp; $env:TMP = $tmp
New-Item -ItemType Directory -Force $tmp, "$lane\logs", 'C:\tmp\OPUS_P027CI_SCRATCH' | Out-Null
$env:CLAUDE_CONFIG_DIR = (Join-Path $env:USERPROFILE '.claude')
Set-Location 'C:\tmp\P027_CI_20260915'
$head = (git -c safe.directory=* rev-parse HEAD).Trim()
if ($head -ne 'a33258367739400017c11a7e498030238f9b1564') { "HEAD $head != a3325836: refuse" | Out-File "$lane\launch.exit" -Encoding ascii; exit 3 }
$head2 = (git -c safe.directory=* -C 'C:\tmp\P027_OPSA_CI_20260915' rev-parse HEAD).Trim()
if (-not $head2.StartsWith('63b7bbe0')) { "HEAD2 $head2 != 63b7bbe0: refuse" | Out-File "$lane\launch.exit" -Encoding ascii; exit 3 }
$start = Get-Date
& claude --print "Read and execute exactly $lane\BRIEF.md. Start by reading that file." --model claude-opus-5 --effort xhigh --permission-mode dontAsk --allowedTools 'Bash' 'Edit' 'Read' 'Write' 'Glob' 'Grep' --disallowedTools 'Agent' 'WebFetch' 'WebSearch' 'NotebookEdit' --add-dir 'C:\tmp\OPUS_QUEUE_20260916\P027CI' 'C:\tmp\OPUS_P027CI_SCRATCH' 'C:\tmp\P027_CI_20260915' 'C:\tmp\P027_OPSA_CI_20260915' 'C:\CT13' --strict-mcp-config --max-turns 100 --output-format stream-json --verbose 2>&1 | Out-File -FilePath "$lane\stream.jsonl" -Encoding utf8
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "$lane\launch.exit" -Encoding ascii
