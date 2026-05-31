$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Venv = Join-Path $Root ".venv-pynecore"
$ReportDir = Join-Path $Root "reports"
New-Item -ItemType Directory -Force $ReportDir | Out-Null

python -m venv $Venv
if ($LASTEXITCODE -ne 0) {
  "venv creation failed with exit code $LASTEXITCODE" | Out-File -Encoding utf8 (Join-Path $ReportDir "pynecore_install_error.txt")
  exit $LASTEXITCODE
}

& (Join-Path $Venv "Scripts\python.exe") -m pip install --upgrade pip *> (Join-Path $ReportDir "pynecore_install_error.txt")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& (Join-Path $Venv "Scripts\pip.exe") install "pynesys-pynecore[cli,providers]" *>> (Join-Path $ReportDir "pynecore_install_error.txt")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& (Join-Path $Venv "Scripts\python.exe") (Join-Path $Root "scripts\ma_cross_strategy.py")
