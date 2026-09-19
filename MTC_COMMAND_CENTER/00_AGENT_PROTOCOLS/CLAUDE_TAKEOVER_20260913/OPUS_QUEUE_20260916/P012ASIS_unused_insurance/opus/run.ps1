# Exact claude-opus-5 xhigh review of WP-P0-12 funding intake NIT slice (NITs 1-9 + NIT-A + D6-START B) at
# candidate 8cbf4f1a on feature/p012-funding-intake-nit-20260919, base a871e429, worktree C:\tmp\P012_INTAKE_20260915
# (a SEPARATE worktree/branch from the a871e429 as-is candidate, which merges unchanged and must not be touched here)
# on the Claude PRO profile (~/.claude), NOT the Max desktop session.
# RE-PINNED 2026-09-19 ~11:5x UTC+3 (a871e429 -> 8cbf4f1a, the NIT slice, after attempt 3 PASS-WITH-NITS on a871e429
# archived as ATTEMPT3_PASS_WITH_NITS_a871e429/). Lane 8 (optional): only if Pro allowance remains; started BY HAND;
# never while agy.exe runs; never two Pro lanes at once; refuses on HEAD drift.
$ErrorActionPreference = 'Continue'
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_API_WALLET_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_ACCOUNT_ADDRESS -ErrorAction SilentlyContinue
Remove-Item Env:HL_LIVE_ACK -ErrorAction SilentlyContinue
$env:PYTHONUTF8='1'; $env:PYTHONDONTWRITEBYTECODE='1'
$lane = 'C:\tmp\OPUS_QUEUE_20260916\P012ASIS\opus'
$tmp = Join-Path $env:LOCALAPPDATA 'Temp\opus_p012intake'
$env:TEMP = $tmp; $env:TMP = $tmp
New-Item -ItemType Directory -Force $tmp, "$lane\logs", 'C:\tmp\OPUS_P012INTAKE_SCRATCH' | Out-Null
$env:CLAUDE_CONFIG_DIR = (Join-Path $env:USERPROFILE '.claude')
if (Get-Process agy -ErrorAction SilentlyContinue) { 'agy.exe running: refuse' | Out-File "$lane\launch.exit" -Encoding ascii; exit 4 }
Set-Location 'C:\tmp\P012_INTAKE_20260915'
$head = (git -c safe.directory=* rev-parse HEAD).Trim()
if ($head -ne 'a871e42965322d4fc66e317ef7067d6fca28972c') { "HEAD $head != a871e429: refuse" | Out-File "$lane\launch.exit" -Encoding ascii; exit 3 }
$start = Get-Date
& claude --print "Read and execute exactly $lane\BRIEF.md. Start by reading that file." --model claude-opus-5 --effort xhigh --permission-mode dontAsk --allowedTools 'Bash' 'PowerShell' 'Edit' 'Read' 'Write' 'Glob' 'Grep' --disallowedTools 'Agent' 'WebFetch' 'WebSearch' 'NotebookEdit' --add-dir 'C:\tmp\OPUS_QUEUE_20260916\P012ASIS' 'C:\tmp\OPUS_P012INTAKE_SCRATCH' 'C:\tmp\P012_INTAKE_20260915' 'C:\tmp\CLAUDE_P0_RUN_20260913\P012_FUNDING_INTAKE_20260915\NIT_SLICE_20260919' 'C:\CT13' --strict-mcp-config --max-turns 100 --output-format stream-json --verbose 2>&1 | Out-File -FilePath "$lane\stream.jsonl" -Encoding utf8
"exit=$LASTEXITCODE start=$($start.ToUniversalTime().ToString('o')) end=$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "$lane\launch.exit" -Encoding ascii
