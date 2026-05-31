param(
    [ValidateSet("optimize", "validate", "promote")]
    [string]$Mode = "validate",
    [string]$Case = "configs/cases/full_jul2025_jan2026_parity.json",
    [int]$Iters = 200,
    [int]$Seed = 42,
    [int]$Workers = 1,
    [int]$TopK = 10,
    [int]$ShortlistK = 3,
    [switch]$DeterminismGate
)

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot
if (-not $ScriptDir) { $ScriptDir = (Get-Location).Path }
Set-Location $ScriptDir

function Resolve-CasePath([string]$PathText) {
    if ([System.IO.Path]::IsPathRooted($PathText)) { return $PathText }
    return (Join-Path $ScriptDir $PathText)
}

function Invoke-CheckedPython([string]$CmdLine) {
    Invoke-Expression $CmdLine
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $CmdLine"
    }
}

function New-RunLayout {
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $nonce = [Guid]::NewGuid().ToString("N").Substring(0, 8)
    $runId = "run_$stamp`_$nonce"
    $resultsRoot = Join-Path $ScriptDir "..\results"
    $runDir = Join-Path $resultsRoot $runId
    $candDir = Join-Path $runDir "candidates"
    $shortDir = Join-Path $runDir "shortlist"
    $blessedDir = Join-Path $runDir "blessed_candidates"

    New-Item -ItemType Directory -Force -Path $runDir | Out-Null
    New-Item -ItemType Directory -Force -Path $candDir | Out-Null
    New-Item -ItemType Directory -Force -Path $shortDir | Out-Null
    New-Item -ItemType Directory -Force -Path $blessedDir | Out-Null

    return @{
        RunId = $runId
        RunDir = $runDir
        TrialsCsv = (Join-Path $runDir "trials.csv")
        ParetoJson = (Join-Path $runDir "pareto.json")
        ReplaySummary = (Join-Path $runDir "replay_summary.csv")
        CandidatesDir = $candDir
        ShortlistDir = $shortDir
        BlessedDir = $blessedDir
        DbPath = (Join-Path $runDir "results.db")
        ReplayTarget1 = (Join-Path $runDir "replay_target_sepdec.csv")
        ReplayTarget2 = (Join-Path $runDir "replay_target_jan2026.csv")
        RankingCsv = (Join-Path $runDir "ranking.csv")
        ManifestJson = (Join-Path $runDir "manifest.json")
    }
}

function Ensure-Environment {
    $venvActivate = Join-Path $ScriptDir "venv\Scripts\Activate.ps1"
    if (Test-Path $venvActivate) {
        . $venvActivate
    } else {
        Write-Warning "Venv not found at $venvActivate. Using current environment."
    }
    $env:PYTHONPATH = $ScriptDir
}

function Invoke-DeterminismGate([hashtable]$Layout, [string]$CasePath) {
    Write-Host ">>> Determinism gate (optional) ..."
    $seqCsv = Join-Path $Layout.RunDir "determinism_seq.csv"
    $parCsv = Join-Path $Layout.RunDir "determinism_par.csv"
    $cmd1 = "python -m src.optimizer_v0 run --case `"$CasePath`" --mode random --iters 20 --seed $Seed --workers 1 --out `"$seqCsv`""
    $cmd2 = "python -m src.optimizer_v0 run --case `"$CasePath`" --mode random --iters 20 --seed $Seed --workers 4 --out `"$parCsv`""
    Invoke-CheckedPython $cmd1
    Invoke-CheckedPython $cmd2

    $py = @"
import pandas as pd
s = pd.read_csv(r"$seqCsv").drop(columns=["runtime_s"], errors="ignore").sort_values("idx").reset_index(drop=True)
p = pd.read_csv(r"$parCsv").drop(columns=["runtime_s"], errors="ignore").sort_values("idx").reset_index(drop=True)
pd.testing.assert_frame_equal(s, p)
print("Determinism gate: PASS")
"@
    $py | python -
    if ($LASTEXITCODE -ne 0) { throw "Determinism gate failed." }
}

function Build-Shortlist([hashtable]$Layout) {
    $py = @"
import pandas as pd, shutil
from pathlib import Path
summary = Path("$($Layout.ReplaySummary -replace '\\','/')")
cand = Path("$($Layout.CandidatesDir -replace '\\','/')")
short = Path("$($Layout.ShortlistDir -replace '\\','/')")
if not summary.exists():
    raise SystemExit("replay_summary.csv missing")
df = pd.read_csv(summary)
if "score" in df.columns:
    df = df.sort_values("score", ascending=False)
top = df.head($ShortlistK)
for f in top["candidate_file"].tolist():
    src = cand / Path(f).name
    if src.exists():
        shutil.copy2(src, short / src.name)
print("Shortlist copied:", len(list(short.glob("*.json"))))
"@
    $py | python -
    if ($LASTEXITCODE -ne 0) { throw "Shortlist build failed." }
}

function Invoke-Optimize([hashtable]$Layout, [string]$CasePath) {
    Write-Host ">>> Mode=optimize | run_id=$($Layout.RunId)"
    $cmdRun = "python -m src.optimizer_v0 run --case `"$CasePath`" --mode random --iters $Iters --seed $Seed --workers $Workers --db `"$($Layout.DbPath)`" --out `"$($Layout.TrialsCsv)`" --pareto-out `"$($Layout.ParetoJson)`""
    $cmdCand = "python -m src.optimizer_v0 export-candidates --pareto `"$($Layout.ParetoJson)`" --outdir `"$($Layout.CandidatesDir)`" --top-k $TopK --overwrite"
    $cmdReplay = "python -m src.optimizer_v0 replay-candidates --case `"$CasePath`" --candidates-dir `"$($Layout.CandidatesDir)`" --out `"$($Layout.ReplaySummary)`" --min-trades 10 --max-dd 40"
    Invoke-CheckedPython $cmdRun
    Invoke-CheckedPython $cmdCand
    Invoke-CheckedPython $cmdReplay
    $guardReplay = "python scripts/artifact_guard.py --required-csv `"$($Layout.ReplaySummary)`""
    Invoke-CheckedPython $guardReplay
    Build-Shortlist $Layout

    if ($DeterminismGate.IsPresent) {
        Invoke-DeterminismGate $Layout $CasePath
    }
}

function Invoke-Validate([hashtable]$Layout) {
    Write-Host ">>> Mode=validate | run_id=$($Layout.RunId)"
    if (-not (Test-Path $Layout.ReplaySummary)) {
        throw "Missing $($Layout.ReplaySummary). Run optimize mode first for this run."
    }
    Build-Shortlist $Layout

    $case1 = Resolve-CasePath "configs/cases/target_sep2025_dec2025.json"
    $case2 = Resolve-CasePath "configs/cases/target_jan2026.json"
    if (-not (Test-Path $case1)) { throw "Missing case: $case1" }
    if (-not (Test-Path $case2)) { throw "Missing case: $case2" }

    $cmdR1 = "python -m src.optimizer_v0 replay-candidates --case `"$case1`" --candidates-dir `"$($Layout.ShortlistDir)`" --out `"$($Layout.ReplayTarget1)`" --min-trades 10 --max-dd 40"
    $cmdR2 = "python -m src.optimizer_v0 replay-candidates --case `"$case2`" --candidates-dir `"$($Layout.ShortlistDir)`" --out `"$($Layout.ReplayTarget2)`" --min-trades 10 --max-dd 40"
    Invoke-CheckedPython $cmdR1
    Invoke-CheckedPython $cmdR2
    $guardTargets = "python scripts/artifact_guard.py --required-csv `"$($Layout.ReplayTarget1)`" --required-csv `"$($Layout.ReplayTarget2)`""
    Invoke-CheckedPython $guardTargets

    $py = @"
import pandas as pd
from pathlib import Path
f1=Path("$($Layout.ReplayTarget1 -replace '\\','/')")
f2=Path("$($Layout.ReplayTarget2 -replace '\\','/')")
o=Path("$($Layout.RankingCsv -replace '\\','/')")
df1=pd.read_csv(f1); df2=pd.read_csv(f2)
df1=df1[df1["status"]=="OK"]; df2=df2[df2["status"]=="OK"]
m=pd.merge(df1, df2, on="candidate_file", suffixes=("_1","_2"))
m["net_sum"]=m["net_profit_1"]+m["net_profit_2"]
m["dd_max"]=m[["max_dd_pct_1","max_dd_pct_2"]].max(axis=1)
m=m.sort_values(by=["net_sum","dd_max","candidate_file"], ascending=[False,True,True])
m.to_csv(o, index=False)
print("Ranking written:", o)
"@
    $py | python -
    if ($LASTEXITCODE -ne 0) { throw "Ranking build failed." }
}

function Invoke-Promote([hashtable]$Layout) {
    Write-Host ">>> Mode=promote | run_id=$($Layout.RunId)"
    if (-not (Test-Path $Layout.RankingCsv)) {
        throw "Missing $($Layout.RankingCsv). Run validate mode first for this run."
    }
    $py = @"
import json, shutil, pandas as pd
from pathlib import Path
rank=Path("$($Layout.RankingCsv -replace '\\','/')")
short=Path("$($Layout.ShortlistDir -replace '\\','/')")
dst=Path("$($Layout.BlessedDir -replace '\\','/')")
manifest=Path("$($Layout.ManifestJson -replace '\\','/')")
df=pd.read_csv(rank).head($ShortlistK)
items=[]
for _,r in df.iterrows():
    name=Path(r["candidate_file"]).name
    src=short/name
    if src.exists():
        shutil.copy2(src, dst/name)
        items.append({"candidate_file":name, "net_sum":float(r["net_sum"]), "dd_max":float(r["dd_max"])})
payload={"run_id":"$($Layout.RunId)","promoted_count":len(items),"items":items}
manifest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print("Manifest written:", manifest)
"@
    $py | python -
    if ($LASTEXITCODE -ne 0) { throw "Promote failed." }
}

Ensure-Environment
$layout = New-RunLayout
$casePath = Resolve-CasePath $Case

if ($Mode -eq "optimize") {
    Invoke-Optimize $layout $casePath
} elseif ($Mode -eq "validate") {
    # Validate mode needs existing artifacts from the same run dir.
    # If called standalone, run optimize first.
    Invoke-Optimize $layout $casePath
    Invoke-Validate $layout
} elseif ($Mode -eq "promote") {
    Invoke-Optimize $layout $casePath
    Invoke-Validate $layout
    Invoke-Promote $layout
}

Write-Host "Runbook complete. Mode=$Mode RunDir=$($layout.RunDir)"
