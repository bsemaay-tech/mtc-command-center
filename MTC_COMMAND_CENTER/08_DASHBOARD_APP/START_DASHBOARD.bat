@echo off
setlocal
REM One-click launcher for the MTC Command Center dashboard.
REM Starts a temporary Cloudflare tunnel, then starts the read-only local API
REM and opens the dashboard in your browser.

set "LOG_DIR=C:\LAB\MTC_CHATGPT_MENTOR_BUNDLES\2026-06-22\tunnel_logs"
set "LOG_FILE=%LOG_DIR%\cloudflared_mtc_dashboard_tunnel.log"

where cloudflared >nul 2>nul
if not errorlevel 1 (
  set "CLOUDFLARED_CMD=cloudflared"
  goto START_TUNNEL
)

set "CLOUDFLARED_CMD=%LOCALAPPDATA%\Microsoft\WinGet\Packages\Cloudflare.cloudflared_Microsoft.Winget.Source_8wekyb3d8bbwe\cloudflared.exe"
if not exist "%CLOUDFLARED_CMD%" (
  echo cloudflared was not found on PATH or in the WinGet package folder.
  echo Install it with: winget install --id Cloudflare.cloudflared -e
  goto START_DASHBOARD
)

:START_TUNNEL
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
start "MTC Cloudflare Tunnel" powershell -NoExit -Command "& '%CLOUDFLARED_CMD%' tunnel --url http://127.0.0.1:8765 2>&1 | Tee-Object -FilePath '%LOG_FILE%'"
echo Cloudflare tunnel starting in a separate PowerShell window.
echo Tunnel log: %LOG_FILE%
echo Share URL format: https://xxxxx.trycloudflare.com/dashboard

:START_DASHBOARD
cd /d "%~dp0apps\api"
python -m mcc_readonly
pause
