# Read-only MTC Command Center dashboard server launcher (preview/dev).
# Serves the API + static web on http://127.0.0.1:8765 (dashboard at /dashboard).
$ErrorActionPreference = "Stop"
Set-Location -Path (Join-Path $PSScriptRoot "apps\api")
python -m mcc_readonly
