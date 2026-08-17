@echo off
rem One-click launcher for the Bridge dashboard tunnel.
rem Runs the PowerShell script beside this file with the policy bypass
rem Windows needs for double-click execution. No other change.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Open-BridgeDashboard.ps1"
