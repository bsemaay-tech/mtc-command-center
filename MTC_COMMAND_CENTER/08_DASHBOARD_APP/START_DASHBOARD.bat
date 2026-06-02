@echo off
REM One-click launcher for the MTC Command Center dashboard.
REM Starts the read-only local API and opens the dashboard in your browser.
cd /d "%~dp0apps\api"
python -m mcc_readonly
pause
