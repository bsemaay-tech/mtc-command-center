# Friday exact-Sol queue generator (PREPARED 2026-09-15 night). Codex Plus pool (`secondary` = `fourth`) serves gpt-5.6-sol;
# the weekly cap resets Fri 2026-09-19 18:47 local. Nothing here runs a review: it writes a Sol lane from an existing
# Wednesday Opus lane (same REVIEW_BRIEF, same worktree + HEAD pin) so Friday's lanes are generated AFTER Wednesday's
# verdicts (a REQUEST_CHANGES on Wednesday changes the HEAD; regenerate, never reuse a stale pin).
#   powershell -NoProfile -ExecutionPolicy Bypass -File C:\tmp\SOL_QUEUE_20260919\make_sol_lane.ps1 -Pkg P031
# Then read <Pkg>\sol\BRIEF.md, verify the HEAD in <Pkg>\sol\run.ps1 against the worktree, and start it BY HAND:
#   powershell -NoProfile -ExecutionPolicy Bypass -File C:\tmp\SOL_QUEUE_20260919\<Pkg>\sol\run.ps1
param(
    [Parameter(Mandatory = $true)][string]$Pkg,
    [string]$Effort = 'xhigh',
    [string]$Account = 'secondary'
)
$ErrorActionPreference = 'Stop'
if (Get-Process agy -ErrorAction SilentlyContinue) { throw 'agy.exe (Gemini) is running: no git command anywhere until it ends - rerun later' }
$opus = "C:\tmp\OPUS_QUEUE_20260916\$Pkg"
if (-not (Test-Path "$opus\REVIEW_BRIEF.md")) { throw "no Wednesday brief for $Pkg at $opus" }
$opusRun = Get-Content "$opus\opus\run.ps1" -Raw
if ($opusRun -notmatch "Set-Location '([^']+)'") { throw "cannot find the worktree in $opus\opus\run.ps1" }
$wt = $Matches[1]
if ($opusRun -notmatch "-ne '([0-9a-f]{40})'") { throw "cannot find the HEAD pin in $opus\opus\run.ps1" }
$pin = $Matches[1]
$head = (git -c safe.directory=* -C $wt rev-parse HEAD).Trim()
if ($head -ne $pin) { throw "worktree $wt is at $head, the Wednesday pin is $pin - regenerate after re-pinning the Wednesday lane, never guess" }
$lane = "C:\tmp\SOL_QUEUE_20260919\$Pkg\sol"
New-Item -ItemType Directory -Force $lane, "$lane\logs", "C:\tmp\SOL_${Pkg}_SCRATCH" | Out-Null
$reportName = if ($Pkg -eq 'P027CI') { 'SOL_T1_REPORT.md' } else { 'SOL_T0_REPORT.md' }
$brief = @"
# Exact review slot: gpt-5.6-sol, $Effort (Codex Plus pool) - $Pkg, HEAD $($pin.Substring(0,8)) (generated $((Get-Date).ToUniversalTime().ToString('o')) from the Wednesday brief)

Read and execute ``$opus\REVIEW_BRIEF.md`` exactly, with these substitutions: where it names the exact ``claude-opus-5`` xhigh reviewer, that role is YOU (gpt-5.6-sol, $Effort) - you are the SECOND flagship, independent of the Wednesday Opus report; do NOT read any Opus report (``*OPUS_T*_REPORT.md``) or any Lead adjudication of it before writing your own verdict. Write your single report to ``$lane\$reportName`` (create it early with a skeleton and update it as you go). Write nothing else outside ``$lane`` except scratch copies under ``C:\tmp\SOL_${Pkg}_SCRATCH\`` for your RED arms. Never run git status/diff-with-working-tree/add/commit/checkout/push in any repository (``git -c safe.directory=* rev-parse HEAD``, ``git -c safe.directory=* show <rev>:<path>`` and ``git -c safe.directory=* diff <sha> <sha> -- <paths>`` only). End the report with the exact VERDICT line(s) the brief requires.
"@
Set-Content -Path "$lane\BRIEF.md" -Value $brief -Encoding utf8
$run = @"
# Exact gpt-5.6-sol $Effort review of $Pkg at $pin on the Codex Plus pool (account '$Account'), generated from the Wednesday lane.
# Lead starts it BY HAND after the Friday reset; never while agy.exe runs; never two Codex lanes on one account at once.
`$ErrorActionPreference = 'Continue'
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:HL_API_WALLET_KEY -ErrorAction SilentlyContinue
`$lane = '$lane'
`$wt = '$wt'
`$launcher = Join-Path `$env:USERPROFILE 'AI_CLI_HELPERS\Invoke-CodexForClaude.ps1'
`$env:PYTHONUTF8 = '1'; `$env:PYTHONDONTWRITEBYTECODE = '1'; `$env:TEMP = "`$lane\tmp"; `$env:TMP = "`$lane\tmp"
New-Item -ItemType Directory -Force "`$lane\tmp" | Out-Null
if (Get-Process agy -ErrorAction SilentlyContinue) { 'agy.exe running: refuse' | Out-File "`$lane\launch.exit" -Encoding ascii; exit 4 }
`$head = (git -c safe.directory=* -C `$wt rev-parse HEAD).Trim()
if (`$head -ne '$pin') { "HEAD `$head != $($pin.Substring(0,8)): refuse" | Out-File "`$lane\launch.exit" -Encoding ascii; exit 3 }
`$prompt = "Read the file `$lane\BRIEF.md in full and execute it exactly. Start by reading that file."
`$codexArgs = @('exec', '-m', 'gpt-5.6-sol', '-c', 'model_reasoning_effort=$Effort', '--ephemeral', '--sandbox', 'workspace-write', '--skip-git-repo-check', '-C', "C:\tmp\SOL_${Pkg}_SCRATCH", '--add-dir', `$lane, '--add-dir', `$wt, '--add-dir', 'C:\CT13', '--add-dir', 'C:\tmp\OPUS_QUEUE_20260916\$Pkg', '--json', '--output-last-message', "`$lane\SOL_LAST_MESSAGE.md", `$prompt)
`$start = Get-Date
& `$launcher -Account $Account -CodexArgs `$codexArgs 2>&1 | Out-File -FilePath "`$lane\stream.jsonl" -Encoding utf8
"exit=`$LASTEXITCODE start=`$(`$start.ToUniversalTime().ToString('o')) end=`$((Get-Date).ToUniversalTime().ToString('o'))" | Out-File "`$lane\launch.exit" -Encoding ascii
"@
Set-Content -Path "$lane\run.ps1" -Value $run -Encoding utf8
Write-Output "generated $lane (worktree $wt @ $($pin.Substring(0,8)); account $Account; effort $Effort)"
Write-Output "NOTE: --add-dir grants the reviewer WRITE access to the worktree under workspace-write; the brief forbids writes there, and the Lead verifies 'git status --porcelain' in the worktree after the lane (must be empty)."
