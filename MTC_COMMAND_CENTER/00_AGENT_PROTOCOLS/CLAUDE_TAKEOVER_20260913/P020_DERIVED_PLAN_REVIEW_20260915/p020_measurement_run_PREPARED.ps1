# WP-P0-20 bounded successor-path measurement: run_bounded_benchmark.py --run over the DERIVED plan d84b043a (ONE shot).
# PREPARED 2026-09-15 by Claude Opus 5 Lead (session tradingview-lab-clean-39 / 743291); runs only when the Lead starts it
# after the derived-plan roster accepts: exact Sol (VERDICT PASS / PASS-WITH-NITS), Gemini 3.7 corroboration SATISFIED,
# Lead trial-by-trial check ALL EQUAL, AND a Grok pre-screen of the derived plan adjudicated SATISFIED (owner OD-20260915-P020-MEASURE-GROK-1:
# "no, wait for Grok (Sep 18)" - the route answered 402 on 2026-09-15; the slot is NOT waivable by the Lead).
# Owner authorization: OD-20260914-P020-MEASURE-1 ("1. B YES") - once, after (a) roster, (b) PROFILE_ELIGIBLE_NOT_ACCEPTED, (c) plan review.
# Sol Q1 condition: the installed plan is ASSERTED equal to d84b043a before --validate-plan, immediately before --run and after the run.
# Sol/Gemini Q2 procedure (temporary substitution): base plan kept as BENCHMARK_PLAN_BASE_c6f07afd.json; derived bytes installed at
# BENCHMARK_PLAN.json; the plan line of SHA256SUMS_V16.txt updated for the interval; --validate-plan in place; --run once into a NEW
# output root; pre/post digests of plan, driver, manifest, compatibility, records + sidecars, implementation sources and every output;
# then the base plan and the checksum manifest restored byte-exact (unless -KeepDerivedInPlace). source_identity.plan_sha256 in the
# run report records which plan actually ran. Output is a MEASUREMENT record only (no acceptance, no ranking, no profitability).
param([switch]$KeepDerivedInPlace)
$ErrorActionPreference = 'Stop'
$BENCH = 'C:\tmp\P020_LEAD_20260912\benchmark'
$PY = 'C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe'
$OUT = 'C:\tmp\CLAUDE_P0_RUN_20260913\P020_MEASUREMENT_20260915'
$OUTPUT_ROOT = "$OUT\output"
$DERIVED = 'C:\tmp\CLAUDE_P0_RUN_20260913\P020_DERIVED_PLAN_20260914\BENCHMARK_PLAN_DERIVED.json'
$DERIVED_SHA = 'd84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580'
$BASE_SHA = 'c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7'
$DRIVER_SHA = '3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324'
$V3_SHA = '69b6f246ad721ccfde23f87c0b21b6470b8fb75b88552bfad004ef8c69d557f9'
$MANIFEST = 'C:\tmp\P020_DERIVED_20260912\selected_manifest.json'
$COMPAT = 'C:\tmp\P020_LEAD_20260912\dataset\STRATEGY_INPUT_COMPATIBILITY.json'
$SOL = 'C:\tmp\P020_DERIVED_PLAN_REVIEW_20260915\sol\SOL_DERIVED_REPORT.md'
$GEM = 'C:\tmp\P012_S16_REVIEWS_20260913\P020_DERIVED_G37\LEAD_ADJUDICATION.md'
$LEAD = 'C:\tmp\CLAUDE_P0_RUN_20260913\P020_DERIVED_PLAN_20260914\LEAD_TRIAL_CHECK_S4.txt'
$GROK = 'C:\tmp\CLAUDE_P0_RUN_20260913\laneGKDERIV_grok\LEAD_ADJUDICATION_GROK.md'
New-Item -ItemType Directory -Force $OUT | Out-Null
$log = "$OUT\run.log"
function Log($m) { $line = "$((Get-Date).ToUniversalTime().ToString('o')) $m"; $line | Out-File $log -Append -Encoding utf8; Write-Output $line }
function Sha($p) { (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLower() }
function AssertPlan($stage) { $s = Sha "$BENCH\BENCHMARK_PLAN.json"; if ($s -ne $DERIVED_SHA) { throw "ASSERT FAILED ($stage): installed plan $s != $DERIVED_SHA" }; Log "assert ($stage): installed BENCHMARK_PLAN.json == $DERIVED_SHA" }
if (Get-Process agy -ErrorAction SilentlyContinue) { throw 'agy.exe running (Gemini guard): refuse' }
if (Test-Path $OUTPUT_ROOT) { throw "output root already exists: $OUTPUT_ROOT (one shot only)" }
# roster gate (derived plan)
$sol = Get-Content $SOL -Raw -Encoding utf8
if ($sol -notmatch 'VERDICT: PASS(-WITH-NITS)?\s*$') { throw 'Sol derived-plan verdict is not PASS/PASS-WITH-NITS: refuse' }
$gem = Get-Content $GEM -Raw -Encoding utf8
if ($gem -notmatch 'slot SATISFIED for the derived plan') { throw 'Gemini derived-plan corroboration not SATISFIED: refuse' }
$lead = Get-Content $LEAD -Raw -Encoding utf8
if ($lead -notmatch 'RESULT: ALL EQUAL') { throw 'Lead trial-by-trial check not ALL EQUAL: refuse' }
if (-not (Test-Path -LiteralPath $GROK)) { throw 'Grok pre-screen adjudication absent (owner OD-20260915-P020-MEASURE-GROK-1: wait for Grok): refuse' }
$grok = Get-Content $GROK -Raw -Encoding utf8
if ($grok -notmatch 'Grok pre-screen slot SATISFIED for the derived plan') { throw 'Grok pre-screen not SATISFIED: refuse' }
Log "roster gate: Sol accepting (report sha256=$(Sha $SOL)); Gemini SATISFIED (adjudication sha256=$(Sha $GEM)); Lead ALL EQUAL; Grok pre-screen SATISFIED (adjudication sha256=$(Sha $GROK))"
# identities before anything is touched
$env:GIT_CONFIG_COUNT = '1'; $env:GIT_CONFIG_KEY_0 = 'safe.directory'; $env:GIT_CONFIG_VALUE_0 = 'C:/P020_IMPL_20260912'
$head = (git -C C:\P020_IMPL_20260912 rev-parse HEAD).Trim()
if ($head -ne 'b9b72f858dc830a9389517f79da5ea3c1fa6122c') { throw "HEAD $head != pinned" }
$d = Sha $DERIVED; if ($d -ne $DERIVED_SHA) { throw "derived plan digest $d != $DERIVED_SHA" }
$b = Sha "$BENCH\BENCHMARK_PLAN.json"; if ($b -ne $BASE_SHA) { throw "base plan digest $b != $BASE_SHA (not the V1.6 base plan; refuse)" }
$dr = Sha "$BENCH\run_bounded_benchmark.py"; if ($dr -ne $DRIVER_SHA) { throw "driver digest $dr drifted" }
$v3 = Sha "$BENCH\SYNTH-P020-BOUNDED-INSTRUMENT-V3.json"; if ($v3 -ne $V3_SHA) { throw "record V3 digest $v3 drifted" }
if (Test-Path "$BENCH\BENCHMARK_PLAN_BASE_c6f07afd.json") { throw 'BENCHMARK_PLAN_BASE_c6f07afd.json already exists: a swap is in progress or was not restored; refuse' }
Log "identities OK: HEAD=$head derived=$d base=$b driver=$dr instrumentV3=$v3"
# the full source set the reviewers asked to see hashed before and after (Gemini Q2 / Sol Q1 step 3-4)
$plan = Get-Content $DERIVED -Raw -Encoding utf8 | ConvertFrom-Json
$sources = @("$BENCH\run_bounded_benchmark.py", $MANIFEST, $COMPAT)
foreach ($k in 'instrument', 'cost', 'funding') { $p = $plan.p020_profile.records.$k.path; $sources += $p; $sources += "$p.sha256" }
foreach ($prop in $plan.implementation_sources.PSObject.Properties) { $sources += $prop.Value.path }
function LogSources($stage) { foreach ($p in $sources) { if (Test-Path -LiteralPath $p) { Log "source ($stage) $p sha256=$(Sha $p)" } else { Log "source ($stage) $p ABSENT" } } }
LogSources 'pre'
Set-Location $BENCH
$env:PYTHONUTF8 = '1'; $env:PYTHONDONTWRITEBYTECODE = '1'; $env:TEMP = "$OUT\tmp"; $env:TMP = "$OUT\tmp"; New-Item -ItemType Directory -Force "$OUT\tmp" | Out-Null
# plan swap (base kept under its digest name; derived copied over the driver's fixed PLAN_PATH; checksum manifest line updated for the interval)
$sumsPath = "$BENCH\SHA256SUMS_V16.txt"
$sumsBytes = [System.IO.File]::ReadAllBytes($sumsPath)
$sumsSha = Sha $sumsPath
Copy-Item -LiteralPath "$BENCH\BENCHMARK_PLAN.json" -Destination "$BENCH\BENCHMARK_PLAN_BASE_c6f07afd.json"
if ((Sha "$BENCH\BENCHMARK_PLAN_BASE_c6f07afd.json") -ne $BASE_SHA) { throw 'base plan backup digest mismatch' }
Copy-Item -LiteralPath $DERIVED -Destination "$BENCH\BENCHMARK_PLAN.json" -Force
AssertPlan 'after swap'
$sumsText = [System.Text.Encoding]::ASCII.GetString($sumsBytes)
$sumsSwapped = $sumsText.Replace("$BASE_SHA  BENCHMARK_PLAN.json", "$DERIVED_SHA  BENCHMARK_PLAN.json")
if ($sumsSwapped -eq $sumsText) { throw 'SHA256SUMS_V16.txt has no base plan line to update; refuse' }
[System.IO.File]::WriteAllBytes($sumsPath, [System.Text.Encoding]::ASCII.GetBytes($sumsSwapped))
Log "plan swap: BENCHMARK_PLAN.json now derived; base kept as BENCHMARK_PLAN_BASE_c6f07afd.json ($BASE_SHA); SHA256SUMS_V16.txt plan line -> derived (manifest was $sumsSha, now $(Sha $sumsPath))"
$restored = $false
try {
  Log 'step 1: --validate-plan in place'
  AssertPlan 'before validate-plan'
  $ErrorActionPreference = 'Continue'
  & $PY .\run_bounded_benchmark.py --validate-plan 2>&1 | Out-File "$OUT\validate_plan_stdout.txt" -Encoding utf8
  $c = $LASTEXITCODE; $ErrorActionPreference = 'Stop'
  Log "validate-plan exit=$c $(Get-Content "$OUT\validate_plan_stdout.txt" -Tail 1)"
  if ($c -ne 0 -or -not ((Get-Content "$OUT\validate_plan_stdout.txt" -Raw) -match 'PLAN_VALID')) { throw 'validate-plan did not return PLAN_VALID: refuse' }
  AssertPlan 'immediately before --run'
  if (Test-Path $OUTPUT_ROOT) { throw "output root appeared: $OUTPUT_ROOT" }
  Log "step 2: exact command: $PY .\run_bounded_benchmark.py --run --output-root $OUTPUT_ROOT (cwd $BENCH; ONE shot; interrupted/resumed vs uninterrupted reference; measurement record only; output root did not exist)"
  $t0 = Get-Date
  $ErrorActionPreference = 'Continue'
  & $PY .\run_bounded_benchmark.py --run --output-root $OUTPUT_ROOT 2>&1 | Out-File "$OUT\run_stdout.txt" -Encoding utf8
  $c = $LASTEXITCODE; $ErrorActionPreference = 'Stop'
  Log "run exit=$c elapsed=$([int]((Get-Date)-$t0).TotalSeconds)s last=$(Get-Content "$OUT\run_stdout.txt" -Tail 1)"
  AssertPlan 'after --run'
  LogSources 'post'
  if (Test-Path $OUTPUT_ROOT) {
    Get-ChildItem -LiteralPath $OUTPUT_ROOT -File -Recurse | ForEach-Object { Log "output $($_.FullName.Substring($OUTPUT_ROOT.Length + 1)) bytes=$($_.Length) sha256=$(Sha $_.FullName)" }
    if (Test-Path "$OUTPUT_ROOT\run_report.json") { $r = Get-Content "$OUTPUT_ROOT\run_report.json" -Raw | ConvertFrom-Json; Log "run_report status=$($r.status) acceptance_verdict=$($r.acceptance_verdict) plan_sha256=$($r.source_identity.plan_sha256) semantic_equal=$($r.semantic_comparison_timing_excluded.equal) failed_resumed=$($r.interrupted_resumed_summary.failed) failed_reference=$($r.uninterrupted_reference_summary.failed)" }
  } else { Log 'output root ABSENT after --run' }
  if ($c -ne 0) { Log (Get-Content "$OUT\run_stdout.txt" -Tail 8 | Out-String); Log 'run refused/blocked/failed: STOP (shot spent; no re-run without a new owner word)' }
}
finally {
  if (-not $KeepDerivedInPlace) {
    Copy-Item -LiteralPath "$BENCH\BENCHMARK_PLAN_BASE_c6f07afd.json" -Destination "$BENCH\BENCHMARK_PLAN.json" -Force
    [System.IO.File]::WriteAllBytes($sumsPath, $sumsBytes)
    $rs = Sha "$BENCH\BENCHMARK_PLAN.json"; $ss = Sha $sumsPath
    if ($rs -eq $BASE_SHA -and $ss -eq $sumsSha) { Remove-Item -LiteralPath "$BENCH\BENCHMARK_PLAN_BASE_c6f07afd.json" -Force; $restored = $true; Log "restored: BENCHMARK_PLAN.json $rs (base); SHA256SUMS_V16.txt $ss (original bytes); backup removed" } else { Log "restore FAILED: plan $rs manifest $ss; backup kept" }
  } else { Log "derived plan KEPT in place (-KeepDerivedInPlace); base remains BENCHMARK_PLAN_BASE_c6f07afd.json; SHA256SUMS_V16.txt carries the derived plan line" }
  $ErrorActionPreference = 'Continue'
  $bad = 0; $n = 0
  foreach ($line in (Get-Content $sumsPath)) {
    if ($line -match '^([0-9a-f]{64})\s+\*?(.+)$') { $n++; $want = $Matches[1]; $rel = $Matches[2].Trim(); $got = Sha (Join-Path $BENCH $rel); if ($got -ne $want) { $bad++; Log "SHA256SUMS_V16 MISMATCH $rel got=$got want=$want" } }
  }
  Log "SHA256SUMS_V16 check after run: $n entries, $bad mismatches"
  Log "final plan digest: $(Sha "$BENCH\BENCHMARK_PLAN.json")"
  Log 'done'
}
